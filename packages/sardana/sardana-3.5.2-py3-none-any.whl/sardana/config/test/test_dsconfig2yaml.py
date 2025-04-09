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

from ..dsconfig2yaml import build_sardana_config
from ..model import Configuration


def test_build_sardana_config__basic(sar_demo_json, sar_demo_yaml):
    yaml_config = build_sardana_config(sar_demo_json, "MacroServer/demo1/1")
    yaml_config.pop("tango_host")
    assert (Configuration(**yaml_config).json(indent=4, exclude_none=True, sort_keys=True)
            == Configuration(**sar_demo_yaml).json(indent=4, exclude_none=True, sort_keys=True))


def test_build_sardana_config__attribute_config(sar_demo_json):
    sar_demo_json["servers"]["Sardana"]["demo1"]["Motor"]["motor/motctrl01/1"] \
        ["attribute_properties"] = {
            "Acceleration": {
                "abs_change": ["-10.4", "10.4"],
                "rel_change": ["-1", "3"],
                "archive_abs_change": ["-0.002", "0.002"],
                "archive_rel_change": ["11"],
                "min_alarm": ["45"],
                "label": ["Something"],
            },
            "SomethingElse": {
                "some_stuff": ["1", "2", "3"]
            }
        }
    yaml_config = build_sardana_config(sar_demo_json, "macroserver/demo1/1")

    Configuration(**yaml_config)

    attr_config = yaml_config["pools"]["demo1"]["controllers"]["motctrl01"]["elements"] \
        ["mot01"]["attributes"]["Acceleration"]
    assert attr_config["abs_change"] == 10.4
    assert attr_config["rel_change"] == [-1, 3]
    assert attr_config["archive_abs_change"] == 0.002
    assert attr_config["archive_rel_change"] == 11
    assert attr_config["min_alarm"] == 45
    assert attr_config["label"] == "Something"
    # Don't include attributes with no recognized props
    assert len(yaml_config["pools"]["demo1"]["controllers"]["motctrl01"]["elements"]
               ["mot01"]["attributes"]) == 1


def test_build_sardana_config__attribute_config_weird_value(sar_demo_json):
    sar_demo_json["servers"]["Sardana"]["demo1"]["Motor"]["motor/motctrl01/1"] \
        ["attribute_properties"] = {
            "Potatoes": {
                "max_value": ["+450"],
            }
        }
    build_sardana_config(sar_demo_json, "macroserver/demo1/1")


def test_build_sardana_config__attribute_config_value_invalid_yaml(sar_demo_json):
    sar_demo_json["servers"]["Sardana"]["demo1"]["Motor"]["motor/motctrl01/1"] \
        ["attribute_properties"] = {
            "Potatoes": {
                "__value": ["%abc"],  # Percent means something in YAML
            }
        }
    yaml_config = build_sardana_config(sar_demo_json, "macroserver/demo1/1")
    # Check that we fall back to a string in this case
    assert (yaml_config["pools"]["demo1"]["controllers"]["motctrl01"]["elements"]
            ["mot01"]["attributes"]["Potatoes"] == "%abc")


def test_build_sardana_config__attribute_config_skip_if_empty(sar_demo_json):
    sar_demo_json["servers"]["Sardana"]["demo1"]["Motor"]["motor/motctrl01/1"] \
        ["attribute_properties"] = {
            "Acceleration": {
                "UnknownProperty": ["foo", "bar"]
            }
        }
    yaml_config = build_sardana_config(sar_demo_json, "macroserver/demo1/1")

    Configuration(**yaml_config)

    assert "attributes" not in yaml_config["pools"]["demo1"]["controllers"]["motctrl01"]["elements"] \
        ["mot01"]


def test_build_sardana_config__polling(sar_demo_json):
    sar_demo_json["servers"]["Sardana"]["demo1"]["Motor"]["motor/motctrl01/1"] \
        ["properties"]["polled_attr"] = ["foo", "3000", "bar", "10000"]
    # Also set some attribute props, to check that both work at the same time
    sar_demo_json["servers"]["Sardana"]["demo1"]["Motor"]["motor/motctrl01/1"] \
        ["attribute_properties"] = {"bar": {"abs_change": ["-10.4", "10.4"]}}
    yaml_config = build_sardana_config(sar_demo_json, "macroserver/demo1/1")

    Configuration(**yaml_config)

    attributes = yaml_config["pools"]["demo1"]["controllers"]["motctrl01"]["elements"]\
        ["mot01"]["attributes"]
    assert attributes["foo"]["polling_period"] == 3000
    assert attributes["bar"]["polling_period"] == 10000
    # assert attributes["bar"]["abs_change"] == 10.4


def test_build_sardana_config__controller_polling(sar_demo_json):
    (sar_demo_json["servers"]["Sardana"]["demo1"]["Controller"]
     ["controller/dummymotorcontroller/motctrl01"]
     ["properties"]["polled_attr"]) = ["foo", "3000", "bar", "10000"]

    yaml_config = build_sardana_config(sar_demo_json, "macroserver/demo1/1")
    Configuration(**yaml_config)

    attributes = yaml_config["pools"]["demo1"]["controllers"]["motctrl01"]["attributes"]
    assert attributes["foo"]["polling_period"] == 3000
    assert attributes["bar"]["polling_period"] == 10000


def test_build_sardana_config__attribute_value(sar_demo_json):
    sar_demo_json["servers"]["Sardana"]["demo1"]["Motor"]["motor/motctrl01/1"] \
        ["attribute_properties"] = {
            "Simple": {
                "__value": ["9000.1"],
            },
            "String": {
                "__value": ["foo"],
            },
            "List": {
                "__value": ["['list', 'of', 'stuff', 74]"],
            },
            "Dict": {
                "__value": ['{"a": 1, "b": 2, "c": 3}']
            },
            "WithTimestamp": {
                "__value": ["9000"],
                "__value_ts": ["1234567890"],  # Gets ignored!
            },
            "WithOtherStuff": {
                "__value": ["9000"],
                "__value_ts": ["1234567890"],
                "archive_rel_change": ["-0.5", "0.5"],
            },
        }
    yaml_config = build_sardana_config(sar_demo_json, "macroserver/demo1/1")

    Configuration(**yaml_config)

    attrs = yaml_config["pools"]["demo1"]["controllers"]["motctrl01"]["elements"] \
        ["mot01"]["attributes"]
    assert attrs["Simple"] == 9000.1  # Simple values are unwrapped
    assert attrs["List"] == ["list", "of", "stuff", 74]
    assert attrs["Dict"]["value"] == {"a": 1, "b": 2, "c": 3}  # dicts always wrapped
    assert attrs["WithTimestamp"] == 9000
    assert attrs["WithOtherStuff"]["value"] == 9000
    assert attrs["WithOtherStuff"]["archive_rel_change"] == 0.5


def test_build_sardana_config__element_device_name(sar_demo_json):
    default_name = "motor/motctrl01/1"
    new_name = "SOME/test/NAME"

    # If the name follows the default convention, we don't put it in the config
    yaml_config = build_sardana_config(sar_demo_json, "macroserver/demo1/1")
    assert "tango_device" not in yaml_config["pools"]["demo1"]["controllers"] \
        ["motctrl01"]["elements"]["mot01"]

    element = sar_demo_json["servers"]["Sardana"]["demo1"]["Motor"].pop(default_name)
    sar_demo_json["servers"]["Sardana"]["demo1"]["Motor"][new_name] = element

    yaml_config = build_sardana_config(sar_demo_json, "macroserver/demo1/1")
    Configuration(**yaml_config)

    # Non-standard name ends up in the element config
    el = yaml_config["pools"]["demo1"]["controllers"]["motctrl01"]["elements"]["mot01"]
    assert el["tango_device"] == new_name


def test_build_sardana_config__controller_device_name(sar_demo_json):

    default_name = "controller/dummymotorcontroller/motctrl01"
    new_name = "ctrl/TEST/bananas"

    # If the name follows the default convention, we don't put it in the config
    yaml_config = build_sardana_config(sar_demo_json, "macroserver/demo1/1")
    assert "tango_device" not in yaml_config["pools"]["demo1"]["controllers"]["motctrl01"]

    controller = sar_demo_json["servers"]["Sardana"]["demo1"]["Controller"].pop(default_name)
    sar_demo_json["servers"]["Sardana"]["demo1"]["Controller"][new_name] = controller

    yaml_config = build_sardana_config(sar_demo_json, "macroserver/demo1/1")
    Configuration(**yaml_config)

    # Non-standard name ends up in the element config
    ctrl = yaml_config["pools"]["demo1"]["controllers"]["motctrl01"]
    assert ctrl["tango_device"] == new_name


def test_build_sardana_config__pool_device_name(sar_demo_json):

    default_name = "Pool/demo1/1"
    new_name = "pool/TEST/bananas"

    # If the name follows the default convention, we don't put it in the YAML config
    yaml_config = build_sardana_config(sar_demo_json, "macroserver/demo1/1")
    assert "tango_device" not in yaml_config["pools"]["demo1"]

    # Move to new name
    pool = sar_demo_json["servers"]["Sardana"]["demo1"]["Pool"].pop(default_name)
    sar_demo_json["servers"]["Sardana"]["demo1"]["Pool"][new_name] = pool

    yaml_config = build_sardana_config(sar_demo_json, "macroserver/demo1/1")
    Configuration(**yaml_config)

    # Non-standard name ends up in the element config
    assert yaml_config["pools"]["demo1"]["tango_device"] == new_name


def test_build_sardana_config__pool_extra_properties(sar_demo_json):

    # Properties unknown to sardana config should still be kept
    extra_props = {
        "MyTestProp1": ["1234.5"],
        "MyTestProp2": ["some", "nice", "lines"],
    }

    sar_demo_json["servers"]["Sardana"]["demo1"]["Pool"]["Pool/demo1/1"]["properties"] = extra_props

    # If the name follows the default convention, we don't put it in the YAML config
    yaml_config = build_sardana_config(sar_demo_json, "macroserver/demo1/1")
    Configuration(**yaml_config)

    # Non-standard name ends up in the element config
    for name, value in extra_props.items():

        assert yaml_config["pools"]["demo1"]["properties"][name] == value


def test_build_sardana_config__ms_device_name(sar_demo_json):

    default_name = "MacroServer/demo1/1"
    new_name = "ms/TEST/bananas"

    # If the name follows the default convention, we don't put it in the YAML config
    yaml_config = build_sardana_config(sar_demo_json, "macroserver/demo1/1")
    assert "tango_device" not in yaml_config["macro_servers"]["demo1"]

    # Move to new name
    ms = sar_demo_json["servers"]["Sardana"]["demo1"]["MacroServer"].pop(default_name)
    sar_demo_json["servers"]["Sardana"]["demo1"]["MacroServer"][new_name] = ms

    yaml_config = build_sardana_config(sar_demo_json, new_name)
    Configuration(**yaml_config)

    # Non-standard name ends up in the element config
    assert yaml_config["macro_servers"]["demo1"]["tango_device"] == new_name


def test_build_sardana_config__ms_environment(sar_demo_json):

    env_path = "/some/nice/path/env.db"
    sar_demo_json["servers"]["Sardana"]["demo1"]["MacroServer"]["MacroServer/demo1/1"]\
        ["properties"]["EnvironmentDb"] = [env_path]

    yaml_config = build_sardana_config(sar_demo_json, "macroserver/demo1/1")
    Configuration(**yaml_config)

    assert yaml_config["macro_servers"]["demo1"]["environment_db"] == env_path


def test_build_sardana_config__max_parellel_macros(sar_demo_json):

    max_parallel_macros = 67
    sar_demo_json["servers"]["Sardana"]["demo1"]["MacroServer"]["MacroServer/demo1/1"]\
        ["properties"]["MaxParallelMacros"] = [str(max_parallel_macros)]

    yaml_config = build_sardana_config(sar_demo_json, "macroserver/demo1/1")
    Configuration(**yaml_config)

    assert yaml_config["macro_servers"]["demo1"]["max_parallel_macros"] == max_parallel_macros


def test_build_sardana_config__ms_extra_properties(sar_demo_json):

    # Properties unknown to sardana config should still be kept
    extra_props = {
        "MyTestProp1": ["1234.5"],
        "MyTestProp2": ["some", "nice", "lines"],
    }

    sar_demo_json["servers"]["Sardana"]["demo1"]["MacroServer"]["MacroServer/demo1/1"]\
        ["properties"].update(extra_props)

    yaml_config = build_sardana_config(sar_demo_json, "macroserver/demo1/1")
    Configuration(**yaml_config)

    for name, value in extra_props.items():
        assert yaml_config["macro_servers"]["demo1"]["properties"][name] == value


def test_build_sardana_config__ctrl_properties(sar_demo_json):

    ctrl_name = "controller/dummymotorcontroller/motctrl01"
    controller = sar_demo_json["servers"]["Sardana"]["demo1"]["Controller"][ctrl_name]
    controller["properties"].update({
        "oneLinerStr": ["abc"],
        "oneLinerInt": ["123"],
        "oneLinerFloat": ["1.23"],
        "severalLines": ["this", "IS", "a", "property"],
        "emptyLines": ["", "   \n   "],
    })

    yaml_config = build_sardana_config(sar_demo_json, "macroserver/demo1/1")

    ctrl = yaml_config["pools"]["demo1"]["controllers"]["motctrl01"]
    assert ctrl["properties"]["oneLinerStr"] == "abc"
    assert ctrl["properties"]["oneLinerInt"] == 123
    assert ctrl["properties"]["oneLinerFloat"] == 1.23
    assert ctrl["properties"]["severalLines"] == ["this", "IS", "a", "property"]
    assert ctrl["properties"]["emptyLines"] == ["", "   \n   "]


drift_correction_test_data = [("true", True), ("True", True), ("false", False), ("False", False), ("other", True)]

@pytest.mark.parametrize("value,expected", drift_correction_test_data)
def test_build_sardana_config__pool_drift_correction(sar_demo_json, value, expected):

    sar_demo_json["servers"]["Sardana"]["demo1"]["Pool"]["Pool/demo1/1"]\
        ["properties"]["DriftCorrection"] = [value]

    yaml_config = build_sardana_config(sar_demo_json, "macroserver/demo1/1")
    Configuration(**yaml_config)

    assert yaml_config["pools"]["demo1"]["drift_correction"] == expected


def test_build_sardana_config__pool_server_name(sar_demo_json):
    # default_name = "Sardana/test"
    # new_name = "Macroserver/test"

    # If the name follows the default convention, we don't put it in the YAML config
    yaml_config = build_sardana_config(sar_demo_json, "macroserver/demo1/1")
    assert "tango_server" not in yaml_config["pools"]["demo1"]

    # Move to new name
    new_pool = {}
    for classname in ["Pool", "CTExpChannel", "Motor", "PseudoMotor", "Controller",
                      "IORegister", "MeasurementGroup", "OneDExpChannel", "PseudoCounter",
                      "TriggerGate", "TwoDExpChannel", "ZeroDExpChannel"]:
        devs = sar_demo_json["servers"]["Sardana"]["demo1"].pop(classname)
        new_pool[classname] = devs
    sar_demo_json["servers"]["Pool"] = {
        "demo1": new_pool
    }

    yaml_config = build_sardana_config(sar_demo_json, "macroserver/demo1/1")
    Configuration(**yaml_config)

    # Non-standard server name ends up in the element config
    assert yaml_config["pools"]["demo1"]["tango_server"] == "Pool"


def test_build_sardana_config__pool_server_instance(sar_demo_json):
    # default_name = "Sardana/test"
    # new_name = "Macroserver/test"

    # If the name follows the default convention, we don't put it in the YAML config
    yaml_config = build_sardana_config(sar_demo_json, "macroserver/demo1/1")
    assert "tango_server" not in yaml_config["pools"]["demo1"]

    # Move to new name
    new_pool = {}
    for classname in ["Pool", "CTExpChannel", "Motor", "PseudoMotor", "Controller",
                      "IORegister", "MeasurementGroup", "OneDExpChannel", "PseudoCounter",
                      "TriggerGate", "TwoDExpChannel", "ZeroDExpChannel"]:
        devs = sar_demo_json["servers"]["Sardana"]["demo1"].pop(classname)
        new_pool[classname] = devs
    sar_demo_json["servers"]["Pool"] = {
        "abc": new_pool
    }

    yaml_config = build_sardana_config(sar_demo_json, "macroserver/demo1/1")
    Configuration(**yaml_config)

    # Non-standard name ends up in the element config
    assert yaml_config["pools"]["abc"]["tango_server"] == "Pool"


def test_build_sardana_config__ms_server_name(sar_demo_json):
    # default_name = "Sardana/test"
    # new_name = "Macroserver/test"

    # If the name follows the default convention, we don't put it in the YAML config
    yaml_config = build_sardana_config(sar_demo_json, "macroserver/demo1/1")
    assert "tango_server" not in yaml_config["macro_servers"]["demo1"]

    # Move to new name
    ms = sar_demo_json["servers"]["Sardana"]["demo1"].pop("MacroServer")
    doors = sar_demo_json["servers"]["Sardana"]["demo1"].pop("Door")
    sar_demo_json["servers"]["MacroServer"] = {
        "demo1": {
            "MacroServer": ms,
            "Door": doors,
        }
    }

    yaml_config = build_sardana_config(sar_demo_json, "macroserver/demo1/1")
    Configuration(**yaml_config)

    # Non-standard name ends up in the element config
    assert yaml_config["macro_servers"]["demo1"]["tango_server"] == "MacroServer"


def test_build_sardana_config__door_default_name(sar_demo_json):
    new_door = {
        "alias": "Customalias",
        "attribute_properties": {},
        "properties": {}
    }
    door_device_name = "Door/demo1/Customalias"

    sar_demo_json["servers"]["Sardana"]["demo1"]["Door"][door_device_name] = new_door

    yaml_config = build_sardana_config(sar_demo_json, "macroserver/demo1/1")
    Configuration(**yaml_config)

    assert yaml_config["macro_servers"]["demo1"]["doors"]["Customalias"] == {'tango_device': door_device_name}


def test_build_sardana_config__no_controllers(sar_demo_json):
    del sar_demo_json["servers"]["Sardana"]["demo1"]["Controller"]
    yaml_config = build_sardana_config(sar_demo_json, "macroserver/demo1/1")
    Configuration(**yaml_config)


# TODO test physical_roles
