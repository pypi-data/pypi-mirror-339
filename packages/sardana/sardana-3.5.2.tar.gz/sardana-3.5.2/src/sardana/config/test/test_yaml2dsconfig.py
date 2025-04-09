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

import pytest
import json
from ruamel.yaml import YAML

from ..yaml2dsconfig import build_dsconfig
from ..validate import sanity_check_config


yaml = YAML(typ="rt")


def check_and_build_dsconfig(config):
    sanity_check_config(config)
    return build_dsconfig(config)


def convert_to_property_value(v):
    # Tango properties are stored as lists of strings, even single values
    if isinstance(v, list):
        return [str(x) for x in v]
    return [str(v)]


def test_build_dsconfig__basic(sar_demo_yaml, sar_demo_json):
    dsconfig = check_and_build_dsconfig(sar_demo_yaml)
    assert dsconfig == sar_demo_json


def test_build_dsconfig__forbid_none(sar_demo_yaml, sar_demo_json):
    dsconfig = check_and_build_dsconfig(sar_demo_yaml)
    sar_demo_yaml["pools"]["demo1"]["controllers"] = None
    assert dsconfig == sar_demo_json


def test_build_dsconfig__ms_alias(sar_demo_yaml, sar_demo_json):
    alias = "my_test_alias"
    sar_demo_yaml["macro_servers"]["demo1"]["tango_alias"] = alias
    dsconfig = check_and_build_dsconfig(sar_demo_yaml)
    assert dsconfig["servers"]["Sardana"]["demo1"]["MacroServer"]["MacroServer/demo1/1"]["alias"] == alias


def test_build_dsconfig__pool_alias(sar_demo_yaml, sar_demo_json):
    alias = "my_test_alias"
    sar_demo_yaml["pools"]["demo1"]["tango_alias"] = alias
    dsconfig = check_and_build_dsconfig(sar_demo_yaml)
    assert dsconfig["servers"]["Sardana"]["demo1"]["Pool"]["Pool/demo1/1"]["alias"] == alias


def test_build_dsconfig__remove_attribute(sar_demo_yaml, sar_demo_json):
    del sar_demo_yaml["pools"]["demo1"]["controllers"]["ctctrl01"]["attributes"]
    dsconfig = check_and_build_dsconfig(sar_demo_yaml)
    ctrl = dsconfig["servers"]["Sardana"]["demo1"]["Controller"]["controller/dummycountertimercontroller/ctctrl01"]
    # We need to set it to an empty dict if there are no attributes, in order
    # for any remaining ones to be removed.
    assert ctrl.get("attribute_properties") == {}


def test_build_dsconfig__attribute_config(sar_demo_yaml, sar_demo_json):
    sar_demo_yaml["pools"]["demo1"]["controllers"]["motctrl01"]["elements"]["mot03"] \
        ["attributes"] = {
            "TestAttribute": {
                "value": 67.5,
                "rel_change": 8,
                "archive_abs_change": [-3, 5],
                "label": "Bananas",
                "min_value": 782.3,
            }
        }

    dsconfig = check_and_build_dsconfig(sar_demo_yaml)

    # TODO once meas grps work, it's probably better to instead modify sar_demo_json
    # as expected, and compare. This way we can check that nothing else changed.
    attr_props = dsconfig["servers"]["Sardana"]["demo1"]["Motor"]["motor/motctrl01/3"] \
        ["attribute_properties"]["TestAttribute"]
    assert attr_props["__value"] == ["67.5"]
    assert attr_props["rel_change"] == ["-8", "8"]
    assert attr_props["archive_abs_change"] == ["-3", "5"]
    assert attr_props["label"] == ["Bananas"]
    assert attr_props["min_value"] == ["782.3"]


def test_build_dsconfig__attribute_value(sar_demo_yaml, sar_demo_json):
    sar_demo_yaml["pools"]["demo1"]["controllers"]["motctrl01"]["elements"]["mot03"] \
        ["attributes"] = {
            "Boolean": True,
            "Integer": -198,
            "Float": 983.1,
            "String": "heLLoooe",
            "List": ["some", "lines", "here", 4],  # Only scalars can be memorized
            "FluentList": yaml.load("[1.2, 3.4, -5.6]"),
            "Dict": {
                # Dicts must be wrapped in "value" to prevent ambiguous cases
                # Will be stored as JSON in the database.
                "value": {"a": 1, "b": 2, "c": 3},
            },
            "WithOtherStuff": {
                "value": 5,
                "rel_change": [-1, 5]
            },
        }

    dsconfig = check_and_build_dsconfig(sar_demo_yaml)

    attr_props = dsconfig["servers"]["Sardana"]["demo1"]["Motor"]["motor/motctrl01/3"] \
        ["attribute_properties"]
    assert attr_props["Boolean"]["__value"] == ["true"]
    assert attr_props["Integer"]["__value"] == ["-198"]
    assert attr_props["Float"]["__value"] == ["983.1"]
    assert attr_props["String"]["__value"] == ["heLLoooe"]
    # A list is stored as JSON, as memorized attributes can't be arrays
    assert attr_props["List"]["__value"] == ['["some", "lines", "here", 4]']
    assert attr_props["FluentList"]["__value"] == ["[1.2, 3.4, -5.6]"]
    assert attr_props["Dict"]["__value"] == ['{"a": 1, "b": 2, "c": 3}']
    assert attr_props["WithOtherStuff"]["__value"] == ["5"]
    assert attr_props["WithOtherStuff"]["rel_change"] == ["-1", "5"]


def test_build_dsconfig__polling(sar_demo_yaml, sar_demo_json):

    sar_demo_yaml["pools"]["demo1"]["controllers"]["motctrl01"]["elements"]["mot03"] \
        ["attributes"] = {
            "SomeCoolAttribute": {
                "polling_period": 5000
            }
        }

    dsconfig = check_and_build_dsconfig(sar_demo_yaml)

    assert dsconfig["servers"]["Sardana"]["demo1"]["Motor"]["motor/motctrl01/3"]["properties"] \
        ["polled_attr"] == ["SomeCoolAttribute", "5000"]


def test_build_dsconfig__element_device_name(sar_demo_yaml, sar_demo_json):

    default_name = "motor/motctrl01/3"
    new_name = "my/TEST/name"

    # Check default name
    dsconfig = check_and_build_dsconfig(sar_demo_yaml)
    element = dsconfig["servers"]["Sardana"]["demo1"]["Motor"][default_name]

    sar_demo_yaml["pools"]["demo1"]["controllers"]["motctrl01"]["elements"]["mot03"] \
        ["tango_device"] = new_name

    dsconfig = check_and_build_dsconfig(sar_demo_yaml)

    # Check that name has changed
    assert not dsconfig["servers"]["Sardana"]["demo1"]["Motor"].get(default_name)
    assert dsconfig["servers"]["Sardana"]["demo1"]["Motor"].get(new_name) == element


def test_build_dsconfig__controller_device_name(sar_demo_yaml, sar_demo_json):

    default_name = "controller/dummymotorcontroller/motctrl01"
    new_name = "ctrl/TEST/name"

    # Check default name
    dsconfig = check_and_build_dsconfig(sar_demo_yaml)
    controller = dsconfig["servers"]["Sardana"]["demo1"]["Controller"][default_name]

    sar_demo_yaml["pools"]["demo1"]["controllers"]["motctrl01"] \
        ["tango_device"] = new_name

    dsconfig = check_and_build_dsconfig(sar_demo_yaml)

    # Check that name has changed
    assert default_name not in dsconfig["servers"]["Sardana"]["demo1"]["Controller"]
    assert dsconfig["servers"]["Sardana"]["demo1"]["Controller"].get(new_name) == controller


def test_build_dsconfig__pool_device_name(sar_demo_yaml, sar_demo_json):

    default_name = "Pool/demo1/1"
    new_name = "pool/BANANAS/7"

    # Check default name
    dsconfig = check_and_build_dsconfig(sar_demo_yaml)
    pool = dsconfig["servers"]["Sardana"]["demo1"]["Pool"][default_name]

    sar_demo_yaml["pools"]["demo1"]["tango_device"] = new_name

    dsconfig = check_and_build_dsconfig(sar_demo_yaml)

    # Check that name has changed
    assert default_name not in dsconfig["servers"]["Sardana"]["demo1"]["Pool"]
    assert dsconfig["servers"]["Sardana"]["demo1"]["Pool"].get(new_name) == pool


def test_build_dsconfig__pool_extra_props(sar_demo_yaml, sar_demo_json):

    # Properties unknown to sardana config should still be kept
    extra_props = {
        "MyTestProp1": 1234.5,
        "MyTestProp2": ["some", "nice", "lines"],
    }
    sar_demo_yaml["pools"]["demo1"]["properties"] = extra_props

    dsconfig = check_and_build_dsconfig(sar_demo_yaml)

    for name, value in extra_props.items():
        assert dsconfig["servers"]["Sardana"]["demo1"]["Pool"]["Pool/demo1/1"]\
            ["properties"][name] == convert_to_property_value(value)


def test_build_dsconfig__pool_server_name(sar_demo_yaml, sar_demo_json):

    default_name = "Sardana/test"
    new_name = "Pool/hello"

    # Check default name
    dsconfig = check_and_build_dsconfig(sar_demo_yaml)
    pool = dsconfig["servers"]["Sardana"]["demo1"]["Pool"]["Pool/demo1/1"]

    sar_demo_yaml["pools"]["demo1"]["tango_server"] = new_name

    dsconfig = check_and_build_dsconfig(sar_demo_yaml)

    # Check that name has changed
    def_srv, def_inst = default_name.split("/")
    assert def_inst not in dsconfig["servers"]
    new_srv, new_inst = new_name.split("/")
    assert dsconfig["servers"][new_srv][new_inst]["Pool"]["Pool/demo1/1"] == pool


def test_build_dsconfig__ms_device_name(sar_demo_yaml, sar_demo_json):

    default_name = "MacroServer/demo1/1"
    new_name = "ms/BANANAS/7"

    # Check default name
    dsconfig = check_and_build_dsconfig(sar_demo_yaml)
    ms = dsconfig["servers"]["Sardana"]["demo1"]["MacroServer"][default_name]

    sar_demo_yaml["macro_servers"]["demo1"]["tango_device"] = new_name

    dsconfig = check_and_build_dsconfig(sar_demo_yaml)

    # Check that name has changed
    ms_devices = dsconfig["servers"]["Sardana"]["demo1"]["MacroServer"]
    assert ms_devices[new_name] == ms
    assert default_name not in ms_devices


def test_build_dsconfig__ms_server_name(sar_demo_yaml, sar_demo_json):

    default_name = "Sardana/test"
    new_name = "MacroServer/hello"

    # Check default name
    dsconfig = check_and_build_dsconfig(sar_demo_yaml)
    ms = dsconfig["servers"]["Sardana"]["demo1"]["MacroServer"]["MacroServer/demo1/1"]

    sar_demo_yaml["macro_servers"]["demo1"]["tango_server"] = new_name

    dsconfig = check_and_build_dsconfig(sar_demo_yaml)

    # Check that name has changed
    def_srv, def_inst = default_name.split("/")
    assert def_inst not in dsconfig["servers"]
    new_srv, new_inst = new_name.split("/")
    assert dsconfig["servers"][new_srv][new_inst]["MacroServer"]["MacroServer/demo1/1"] == ms


def test_build_dsconfig__controller_properties(sar_demo_yaml, sar_demo_json):

    controller = sar_demo_yaml["pools"]["demo1"]["controllers"]["motctrl01"]
    controller["properties"] = {
        "OneLiner": "I'll be back",
        "SeveralLines": ["a", "longer", "one"]
    }

    dsconfig = check_and_build_dsconfig(sar_demo_yaml)

    # Check that name has changed
    ctrl_name = "controller/dummymotorcontroller/motctrl01"
    print(dsconfig["servers"]["Sardana"]["demo1"]["Controller"])
    ctrl_props = dsconfig["servers"]["Sardana"]["demo1"]["Controller"][ctrl_name]["properties"]
    assert ctrl_props["OneLiner"] == ["I'll be back"]
    assert ctrl_props["SeveralLines"] == ["a", "longer", "one"]


def test_build_dsconfig__ms_extra_props(sar_demo_yaml, sar_demo_json):

    # Properties unknown to sardana config should still be kept
    extra_props = {
        "MyTestProp1": 1234.5,
        "MyTestProp2": ["some", "nice", "lines"],
    }
    sar_demo_yaml["macro_servers"]["demo1"]["properties"] = extra_props

    dsconfig = check_and_build_dsconfig(sar_demo_yaml)

    for name, value in extra_props.items():
        assert dsconfig["servers"]["Sardana"]["demo1"]["MacroServer"]["MacroServer/demo1/1"]\
            ["properties"][name] == convert_to_property_value(value)


def test_build_dsconfig__ms_environment(sar_demo_yaml, sar_demo_json):

    env_path = "/some/nice/place/env.db"
    sar_demo_yaml["macro_servers"]["demo1"]["environment_db"] = env_path

    dsconfig = check_and_build_dsconfig(sar_demo_yaml)

    assert dsconfig["servers"]["Sardana"]["demo1"]["MacroServer"]["MacroServer/demo1/1"]["properties"]\
        ["EnvironmentDb"] == [env_path]


def test_build_dsconfig__ms_max_parallel_macros(sar_demo_yaml, sar_demo_json):

    max_parallel_macros = 12
    sar_demo_yaml["macro_servers"]["demo1"]["max_parallel_macros"] = max_parallel_macros

    dsconfig = check_and_build_dsconfig(sar_demo_yaml)

    assert dsconfig["servers"]["Sardana"]["demo1"]["MacroServer"]["MacroServer/demo1/1"]["properties"]\
        ["MaxParallelMacros"] == [str(max_parallel_macros)]


def test_build_dsconfig__ms_pools_autodetect(sar_demo_yaml):
    dsconfig = check_and_build_dsconfig(sar_demo_yaml)

    # The default MS does not contain any explicit list of pools
    assert "pools" not in sar_demo_yaml["macro_servers"]["demo1"]
    ms = dsconfig["servers"]["Sardana"]["demo1"]["MacroServer"]["MacroServer/demo1/1"]
    assert ms["properties"]["PoolNames"] == ["Pool_demo1_1"]


def test_build_dsconfig__ms_pools_extra(sar_demo_yaml):
    # Explicitly define a list of pools, some of which are not present in the config
    sar_demo_yaml["macro_servers"]["demo1"]["pools"] = ["demo1", "abc"]

    dsconfig = check_and_build_dsconfig(sar_demo_yaml)

    ms = dsconfig["servers"]["Sardana"]["demo1"]["MacroServer"]["MacroServer/demo1/1"]
    assert ms["properties"]["PoolNames"] == ["Pool_demo1_1", "abc"]


door_names_test_data = [("myDoor", "Door/demo1/myDoor"), 
                        ("door_usr_1", "Door/demo1/door_usr_1"),
                        ("Door_alias", "custom/tango/device"),
                        ("Door_demo1_1", "Door/demo1/01")]

@pytest.mark.parametrize("alias,tango_device", door_names_test_data)
def test_build_dsconfig__door_names(sar_demo_yaml, alias, tango_device):
    sar_demo_yaml["macro_servers"]["demo1"]["doors"] = {alias: {'tango_device': tango_device}}

    dsconfig = check_and_build_dsconfig(sar_demo_yaml)
    assert dsconfig["servers"]["Sardana"]["demo1"]["Door"][tango_device]["alias"] == alias


# TODO test physical_roles
def test_build_dsconfig__ms_pools_remote(sar_demo_yaml, sar_demo_json):
    # Add an pool that could be in a different control system to the MS
    external_pool = "tango://my.test.db:10000/a/b/c"
    sar_demo_yaml["macro_servers"]["demo1"]["pools"] = ["demo1", external_pool]

    dsconfig = check_and_build_dsconfig(sar_demo_yaml)

    ms = dsconfig["servers"]["Sardana"]["demo1"]["MacroServer"]["MacroServer/demo1/1"]
    assert ms["properties"]["PoolNames"] == ["Pool_demo1_1", external_pool]


def test_build_dsconfig__pool_drift_correction(sar_demo_yaml, sar_demo_json):

    sar_demo_yaml["pools"]["demo1"]["drift_correction"] = True

    dsconfig = check_and_build_dsconfig(sar_demo_yaml)

    assert dsconfig["servers"]["Sardana"]["demo1"]["Pool"]["Pool/demo1/1"]["properties"]\
        ["DriftCorrection"] == ["true"]
