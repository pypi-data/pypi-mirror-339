# -*- coding: utf-8 -*-

##############################################################################
##
## This file is part of Sardana
## 
## http://www.tango-controls.org/static/sardana/latest/doc/html/index.html
##
## Copyright 2019 CELLS / ALBA Synchrotron, Bellaterra, Spain
## 
## Sardana is free software: you can redistribute it and/or modify
## it under the terms of the GNU Lesser General Public License as published by
## the Free Software Foundation, either version 3 of the License, or
## (at your option) any later version.
## 
## Sardana is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU Lesser General Public License for more details.
## 
## You should have received a copy of the GNU Lesser General Public License
## along with Sardana.  If not, see <http://www.gnu.org/licenses/>.
##
##############################################################################

"""
This script takes a dsconfig representation (could be a straight dump)
of a sardana configuration and produces a YAML sardana config file.
The goal is that this should be a 1 to 1 transformation.

Making a suitable dump (make sure to include all important servers):
$ python -m dsconfig.dump server:Pool/1 server:MacroServer/1 > my_dsconfig.json

Running this script (giving the relevant macroserver name):
$ python dsconfig2yaml.py my_dsconfig.json my/macroserver/1
"""

import copy
import logging
from typing import Dict, Any

from sardana.pool import AcqSynchType
from sardana.taurus.core.tango.sardana import PlotType
from sardana.pool.pool import ElementType, TYPE_MAP_OBJ
import tango
from tango.utils import CaselessDict, CaselessList
from ruamel.yaml import YAML, parser

from .common import clean_dict, get_full_device_name


logger = logging.getLogger(__name__)


yaml = YAML(typ="rt")


def to_bool(text):
    return text.lower() != "false"


def find_device(config, cls, name):
    for servername, instances in config["servers"].items():
        for instname, classes in instances.items():
            for classname, clss in classes.items():
                if classname.lower() == cls.lower():
                    for devicename, device in clss.items():
                        if devicename.lower() == name.lower():
                            return servername, instname, classes, devicename, device
    raise KeyError(f"Device {name} not found!")


def find_pools(config):
    for servername, instances in config["servers"].items():
        for instname, classes in instances.items():
            for classname, clss in classes.items():
                if classname.lower() == "pool":
                    for devicename, device in clss.items():
                        # Return both device and alias, for lookup
                        yield devicename.lower(), (servername, instname, classes, devicename, device)
                        # TODO what if there's no alias? It could happen...
                        alias = device["alias"]
                        yield alias, (servername, instname, classes, devicename, device)


def build_instruments(instrument_list):
    if not instrument_list:
        return None  # If there are no instruments dont crash
    for clss, name in zip(instrument_list[::2],
                          instrument_list[1::2]):
        yield name, {"class": clss}


def get_property(device, name, multiple=False, converter=lambda x: x):
    """
    Get a property value, by default assumed to be a single value.
    Optionally it can be converted to an expected type. Just make sure
    that the type conforms to the schema and it should be safe!
    TODO guess we could actually use the pydantic model here, somehow...
    """
    properties = CaselessDict(device.get("properties", {}))
    if name in properties:
        values = properties[name]
        if multiple:
            return values
        if len(values) == 1:
            return converter(values[0])
        else:
            raise ValueError(f"Expected exactly one value of property {name}"
                             + f" for device {device}; found{values}")


def destringify(value: str):
    # Empty strings, or just whitespace, are probably valid values in
    # some contexts.  However, YAML loading an empty string gives
    # None.
    if value.strip() == "":
        return value
    try:
        # So, let's guess the type!
        # TODO add tests for various types
        # TODO still we have the problem of ambiguity between the string "true" and
        # the boolean "true"...
        return yaml.load(value)
    except (parser.ParserError, ValueError):
        logger.warning("Could not parse %r as YAML; handling as string", value)
        return value


def get_memorized_value(values):
    if len(values) == 1:
        value = values[0]
        # Data type is not available to us. I guess the only real way is
        # to inspect the controller class.
        return destringify(value)


def get_property_value(lst: list):
    if len(lst) == 1:
        return destringify(lst[0])
    else:
        return [destringify(v) for v in lst]


def get_attribute_properties(device, name, polled_attr={}, skip_values=set()):
    results = {}
    if polled_attr:
        for attr, period in polled_attr.items():
            if attr.lower() == name.lower():
                results["polling_period"] = period
    properties = CaselessDict(device.get("attribute_properties", {}))
    if results or name in properties:
        for prop, values in properties[name].items():
            try:
                if prop.lower() == "__value_ts":
                    continue
                if prop.lower() == "__value":
                    if name in skip_values:
                        continue
                    results["value"] = get_memorized_value(values)
                elif prop.lower() in {"abs_change",
                                      "rel_change",
                                      "archive_abs_change",
                                      "archive_rel_change"}:
                    # Loading as YAML will convert to int or float depending
                    # on the string format. This is better for diffing.
                    if len(values) == 2:
                        vneg = yaml.load(values[0])
                        vpos = yaml.load(values[1])
                        if vneg == -vpos:
                            results[prop] = vpos
                        else:
                            results[prop] = [vneg, vpos]
                    else:
                        # Not sure under what circumstances this can happen,
                        # but it appears to be valid.
                        results[prop] = yaml.load(values[0])
                elif prop.lower() in {"min_value",
                                      "max_value",
                                      "min_alarm",
                                      "max_alarm",
                                      "event_period"}:
                    value, = values
                    results[prop] = yaml.load(value)
                elif prop.lower() in {"label",
                                      "format",
                                      "unit",
                                      "description"}:
                    results[prop] = values[0]
            except ValueError as e:
                # Note that we will bail out on this error. Probably we should not
                # proceed if we can't interpret the property.
                raise ValueError(f"Failed to decode Attribute '{device['alias']}/{name}'"
                                 + f", property '{prop}' value '{values}': {e}")
        if (len(results) == 1
                and "value" in results
                and not isinstance(results["value"], dict)):  # Dicts must stay wrapped.
            # In the case where there is only a value, we "unwrap" it and use only
            # the value itself. This is a common case and makes the YAML simpler.
            return results["value"]
        return results or None


def get_polled_attrs(device):
    polled_attr = get_property(device, "polled_attr", multiple=True)
    if polled_attr:
        return {
            attr: int(period)
            for attr, period in zip(polled_attr[::2], polled_attr[1::2])
        }
    return {}


SPECIAL_ELEMENT_PROPERTIES = CaselessList(
    ["description", "axis", "ctrl_id", "instrument_id", "DriftCorrection"]
)  # TODO more?


def build_element(devicename, element, ctrl_name, ctrl_type):
    alias = element.get("alias")
    info = {}
    description = get_property(element, "description")
    if description:
        info["description"] = description
    axis = int(get_property(element, "axis"))
    info["axis"] = axis

    # Attributes with configuration parameters
    if ctrl_type == "Motor":
        # DialPosition is not part of configuration, however it is stored
        # in the Tango DB and is used by the drift correction feature
        # of pseudo motors.
        skip_values = tango.utils.CaselessList(["DialPosition"])
    else:
        skip_values = set()

    polled_attr = get_polled_attrs(element)
    attributes = clean_dict({
        attr: get_attribute_properties(element, attr, polled_attr,
                                       skip_values=skip_values)
        for attr in element.get("attribute_properties", [])
        if attr != "DialPosition"
    })
    if ctrl_type == "PseudoMotor":
        drift_correction = get_property(element, "DriftCorrection")
        if drift_correction is not None and drift_correction.lower() == "true":
            info["drift_correction"] = True
    # TODO 'Force_HW_Read'?

    # Fill in any other attributes that happen to be polled
    for attr, period in polled_attr.items():
        caseless_attrs = CaselessDict({attrname: attrname for attrname in attributes})
        if attr not in caseless_attrs:
            attributes[attr] = {"polling_period": period}

    if attributes:
        info["attributes"] = attributes

    instrument_id = get_property(element, "Instrument_id")
    if instrument_id:
        info["instrument"] = instrument_id

    type_data = TYPE_MAP_OBJ[ElementType[ctrl_type]]
    default_name = type_data.auto_full_name.format(ctrl_name=ctrl_name, axis=axis)
    if devicename.lower() != default_name.lower():
        # Non-default device name
        info["tango_device"] = devicename

    return alias, info


def find_ctrl_elements(server, ctrl_name, ctrl_type):
    logger.debug(f"find_ctrl_elements {ctrl_name}, {ctrl_type}")
    for class_name, devices in server.items():
        if class_name.lower() == ctrl_type.lower():
            for devicename, element in devices.items():
                ctrl_id = get_property(element, "ctrl_id")
                if ctrl_id.lower() == ctrl_name.lower():
                    yield build_element(devicename, element, ctrl_name, ctrl_type)


def sort_elements(elements):
    return sorted(elements, key=lambda e: e[1].get("axis"))


def get_controller_device_name(devname, klass, name):
    "Check if device name deviates from the default, in that case, store it"
    if devname.lower() == f"controller/{klass}/{name}".lower():
        return None
    return devname


SPECIAL_CTRL_PROPERTIES = CaselessList(
    ["description", "type", "klass", "library", "physical_roles"]
)


CONTROLLER_TYPE_ORDER = [
    "Motor",
    "PseudoMotor",
    "CTExpChannel",
    "ZeroDExpChannel",
    "OneDExpChannel",
    "TwoDExpChannel",
    "PseudoCounter",
    "TriggerGate",
    "IORegister",
]


def sort_controllers(ctrls):
    "Get the controllers sorted in the standard way"
    return sorted(ctrls, key=lambda c: CONTROLLER_TYPE_ORDER.index(c[1]["type"]))


def find_controllers(server):
    controllers = server.get("Controller", {})
    for devname, ctrl in controllers.items():
        # Note that we want a consistent order of the keys here, don't
        # change it unless you know what you're doing.
        alias = ctrl["alias"]
        ctrl_type = get_property(ctrl, "type")
        logger.debug(f"Found controller {alias} of type {ctrl_type}")
        ctrl_class = get_property(ctrl, "klass")
        ctrl_info = {}
        description = get_property(ctrl, "description")
        if description:
            ctrl_info["description"] = description
        ctrl_info.update({
            "type": ctrl_type,
            "tango_device": get_controller_device_name(devname, ctrl_class, alias),
            "python_class": ctrl_class,
            "python_module": get_property(ctrl, "library"),
        })

        # Allow extra properties (settings etc)
        extra_properties = {
            prop: get_property_value(value)
            for prop, value in ctrl.get("properties", {}).items()
            if prop not in SPECIAL_CTRL_PROPERTIES
        }
        polled_attr = get_polled_attrs(ctrl)
        if extra_properties:
            ctrl_info["properties"] = extra_properties
        attributes = clean_dict({
            attr: get_attribute_properties(ctrl, attr, polled_attr)
            for attr in ctrl.get("attribute_properties", [])
        })

        # Other polled attributes
        for attr, period in polled_attr.items():
            caseless_attrs = CaselessDict({attrname: attrname for attrname in attributes})
            if attr not in caseless_attrs:
                attributes[attr] = {"polling_period": period}

        if attributes:
            ctrl_info["attributes"] = attributes

        if ctrl_type in {"PseudoMotor", "PseudoCounter"}:
            pr_prop = ctrl["properties"].get("physical_roles")
            if pr_prop:
                physical_roles = {
                    role: axis
                    for role, axis in zip(pr_prop[::2], pr_prop[1::2])
                }
                ctrl_info["physical_roles"] = physical_roles

        elements = sort_elements(find_ctrl_elements(server, alias, ctrl_type))
        if elements:
            ctrl_info["elements"] = dict(elements)
        yield alias, clean_dict(ctrl_info)


MEAS_GRP_CHANNEL_DEFAULTS = {
    "enabled": True,
    "output": True,
    "plot_type": PlotType.No,
    "plot_axes": [],
    "data_type": "float64",
    "data_units": "",
    "nexus_path": "",
}


def get_measurement_group_channels(ctrl: Dict[str, Any], names: Dict[str, str], mg_name: str):
    synchronizer = ctrl.get("synchronizer")
    synchronization = ctrl.get("synchronization")
    timer = ctrl.get("timer")
    monitor = ctrl.get("monitor")
    try:
        ctrl_channels = copy.deepcopy(list(ctrl["channels"].values()))
    except KeyError:
        raise KeyError(f"{mg_name} still has the old measurement group structure." + 
                       f" Re-apply its configuration again in expconf so it is saved with the new one" +
                       f" (at least one value needs to be modified for it to save changes).")

    ch_fullname_to_name = {
        ch["full_name"]: ch["name"]
        for ch in ctrl_channels
    }
    ctrl_channels_sorted = sorted(ctrl_channels, key=lambda ch: ch["index"])
    for raw_channel in ctrl_channels_sorted:
        channel = {}
        if synchronizer is not None and synchronizer != "software":
            try:
                channel["synchronizer"] = names[synchronizer]
            except KeyError:
                channel["synchronizer"] = synchronizer
        if synchronization is not None and synchronization != AcqSynchType.Trigger:
            channel["synchronization"] = AcqSynchType.get(synchronization)
        if timer is not None:
            timer_name = ch_fullname_to_name[timer]
            if timer_name != ctrl_channels_sorted[0]["name"]:
                channel["timer"] = timer_name
        if monitor is not None:
            monitor_name = ch_fullname_to_name[monitor]
            if monitor_name != ctrl_channels_sorted[0]["name"]:
                channel["monitor"] = monitor_name

        for name, default_value in MEAS_GRP_CHANNEL_DEFAULTS.items():
            value = raw_channel.get(name)
            # Default values are excluded from the configuration
            if value is not None and value != default_value:
                channel[name] = value

        label = raw_channel["label"]
        if channel:
            yield {label: channel}
        else:
            # No config; just need the name
            yield label


def get_measurement_group_channels_external(ctrl: Dict[str, Any]):
    for name, raw_channel in ctrl["channels"].items():
        channel = {}

        for key, default_value in MEAS_GRP_CHANNEL_DEFAULTS.items():
            value = raw_channel.get(key)
            # Default values are excluded from the configuration
            if value is not None and value != default_value:
                channel[key] = value

        if channel:
            yield {name: channel}
        else:
            yield name


def find_measurement_groups(server):
    tg_fullname_to_name = {
        get_full_device_name(name): tg["alias"]
        for name, tg in server.get("TriggerGate", {}).items()
    }
    for name, mntgrp in server.get("MeasurementGroup", {}).items():
        config = {}
        alias = mntgrp["alias"]
        configuration = get_attribute_properties(device=mntgrp, name="configuration")
        if configuration:
            if not isinstance(configuration, dict):
                # TODO under what circumstances might this happen?
                configuration = yaml.load(configuration)
            elif "value" in configuration:
                configuration = configuration["value"]  # Wrapped
            assert isinstance(configuration, dict),\
                f"Expected measurement group configuration to be a JSON object; got {configuration}"
            channels = []
            for ctrl_name, ctrl in configuration["controllers"].items():
                if ctrl_name == "__tango__":
                    new_channels = list(get_measurement_group_channels_external(ctrl))
                else:
                    new_channels = list(get_measurement_group_channels(ctrl, tg_fullname_to_name, name))
                channels.extend(new_channels)
            label = configuration.get("label")
            if label != alias:
                config["label"] = label
            description = configuration.get("description")
            if (description is not None
                    and description != "General purpose measurement configuration"):
                config["description"] = description
        else:
            channels = mntgrp["properties"].get("elements", [])
        config["channels"] = channels

        yield alias, config


def get_device_name(current, server, inst):
    if current.lower() == f"{server}/{inst}/1".lower():
        # Using default name, no need to export it
        return None
    return current


def get_server_name(name, server_name, instance_name):
    if name != instance_name:
        return f"{server_name}/{instance_name}"
    if server_name != "Sardana":
        return server_name


def get_door_alias(door, door_device_name):
    try:
        return door["alias"]
    except KeyError:
        raise KeyError(f"Door {door_device_name} has no alias. Define an alias for the door and try again.")


def get_door(door, door_device_name):
    if get_property(door, "id"):
        raise RuntimeError(
            "Your installation contains numeric element IDs. The config"
            + " tool only works with setting USE_NUMERIC_ELEMENT_IDS=False."
            + " Furthermore your installation requires conversion."
        )
    return {
        "tango_device": door_device_name,
        "description": get_property(door, "description")
    }


def get_pools(pool_names, all_pools):
    "Convert the MS PoolNames property to a config value"
    pools = []
    has_external = False
    for pool_name in pool_names:
        # We use instance names to identify pools in the config
        try:
            _, inst, *_ = all_pools[pool_name]
            pools.append(inst)
        except KeyError:
            # Assumed to be a pool external to the config
            pools.append(pool_name)
            has_external = True
    # If the list only contains pools that are in the config,
    # in and we can skip the pools field.
    if has_external:
        return pools


# Properties that we make part of the config format. All other properties
# are considered "extra".
HANDLED_MS_PROPERTIES = {
    "description",
    "poolnames",
    "macropath",
    "pythonpath",
    "recorderpath",
    "maxparallelmacros",
    "environmentdb",
    "maxparallelmacros",
    "logreportfilename",
    "logreportformat",
}
HANDLED_POOL_PROPERTIES = {
    "description",
    "poolpath",
    "pythonpath",
    "instrumentlist",
    "motionloop_sleeptime",
    "motionloop_statesperposition",
    "acqloop_sleeptime",
    "acqloop_statespervalue",
    "remotelog",
    "driftcorrection",
}


def get_extra_properties(dev, handled):
    return {
        name: value
        for name, value in dev.get("properties", {}).items()
        if name.lower() not in handled
    }


def get_environment(ms):
    """
    TODO later we want to allow configuring all the environment config
    variables here, but until then we only allow setting the path.
    """
    return None


def get_tango_host(config):
    return tango.ApiUtil.get_env_var("TANGO_HOST")


def build_sardana_config(config, ms_device_name, include_tango_host=True):
    """
    Convert a dsconfig into a sardanoa config.
    Need to get a MacroServer device name.
    """
    ms_srv, ms_inst, ms_server, ms_device_name, ms_device = find_device(config, "MacroServer", ms_device_name)
    pool_names = get_property(ms_device, "PoolNames", multiple=True)
    all_pools = CaselessDict(find_pools(config))
    pools = {}
    for name in pool_names:
        # Some complexity because techically the PoolNames property may contain
        # either device names or aliases, while we always want to refer to the
        # pools by alias.
        try:
            info = _, inst, *_ = all_pools[name.lower()]
            pools[inst] = info
        except KeyError as e:
            logger.warning(
                f"Pool {e} listed in MacroServer {ms_device_name} property PoolNames is not in this config!"
                + " It is assumed to exist elsewhere."
            )

    logger.debug(f"Found pools: {pools.keys()}")
    macro_servers = {
        ms_inst: (ms_srv, ms_inst, ms_server, ms_device_name, ms_device,)
    }

    return clean_dict({
        "tango_host": get_tango_host(config) if include_tango_host else None,
        "macro_servers": {
            ms_name: clean_dict({
                "description": get_property(device, "description"),
                "tango_alias": (device["alias"]
                                if device["alias"].lower() != f"ms_{ms_inst}_1".lower()
                                else None),
                "tango_device": get_device_name(devname, "MacroServer", ms_name),
                "tango_server": get_server_name(ms_name, srvrname, instname),
                "python_path": get_property(device, "PythonPath", multiple=True),
                "macro_path": get_property(device, "MacroPath", multiple=True),
                "recorder_path": get_property(device, "RecorderPath", multiple=True),
                "environment_db": get_property(device, "EnvironmentDb"),
                "environment": get_environment(device),
                "max_parallel_macros": get_property(device, "MaxParallelMacros",
                                                    converter=int),
                "log_report_filename": get_property(device, "LogReportFilename"),
                "log_report_format": get_property(device, "LogReportFormat"),

                "properties": get_extra_properties(device, HANDLED_MS_PROPERTIES) or None,

                "doors": {
                    get_door_alias(door, door_device_name): clean_dict(get_door(door, door_device_name))
                    for door_device_name, door in server["Door"].items()
                },
                "pools": get_pools(get_property(device, "PoolNames", multiple=True), all_pools),
            })
            for ms_name, (srvrname, instname, server, devname, device)
            in macro_servers.items()
        },
        "pools": {
            # Use instance name as pool name; I think this is better since
            # it is more "readable" than the alias... and the alias is usually
            # generated anyway so it carries little meaning
            instname: clean_dict({
                "description": get_property(device, "description"),
                "tango_alias": (device["alias"]
                                if device["alias"].lower() != f"pool_{instname}_1".lower()
                                else None),
                "tango_device": get_device_name(devname, "Pool", instname),
                "tango_server": get_server_name(poolname, srvrname, instname),
                "pool_path": get_property(device, "PoolPath", multiple=True),
                "python_path": get_property(device, "PythonPath", multiple=True),
                "motionloop_sleep_time": get_property(device, "MotionLoop_SleepTime",
                                                      converter=int),
                "motionloop_states_per_position": get_property(
                    device,
                    "MotionLoop_StatesPerPosition",
                    converter=int),
                "acqloop_sleep_time": get_property(device, "AcqLoop_SleepTime",
                                                   converter=int),
                "acqloop_states_per_value": get_property(
                    device,
                    "AcqLoop_StatesPerValue",
                    converter=int),
                "remote_log": get_property(device, "RemoteLog"),
                "drift_correction": get_property(device, "DriftCorrection", converter=to_bool),

                "properties": get_extra_properties(device, HANDLED_POOL_PROPERTIES) or None,

                "measurement_groups": dict(sorted(find_measurement_groups(server))) or None,
                "instruments": dict(
                    build_instruments(get_property(device, "InstrumentList", multiple=True))
                ) or None,
                "controllers": dict(sort_controllers(find_controllers(server))) or None,
            })
            for poolname, (srvrname, instname, server, devname, device) in pools.items()
        },
    })


if __name__ == "__main__":
    from argparse import ArgumentParser, FileType
    import json
    import sys

    from ruamel.yaml import YAML

    from .validate import sanity_check_config

    yaml = YAML(typ="rt")

    argparser = ArgumentParser()
    argparser.add_argument("dsconfig", type=FileType("r"))
    argparser.add_argument("macroserver")
    argparser.add_argument("--no-check", "-c", action="store_true")
    args = argparser.parse_args()

    ds_config = json.load(args.dsconfig)
    sardana_config = build_sardana_config(ds_config, args.macroserver)
    if not args.no_check:
        try:
            sanity_check_config(sardana_config)
        except RuntimeError as e:
            sys.exit(e)

    yaml.dump(sardana_config, sys.stdout)
