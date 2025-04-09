"""
Tests that convert YAML -> dsconfig -> YAML, and check that we get back
exactly the same thing. Comments, formatting etc should be retained.

Whenever we find corner cases it is a good idea to add them here, simplified
as far as possible.
"""

import json

from ..check import check_config
from ..validate import sanity_check_config
from ..dsconfig2yaml import build_sardana_config
from ..yaml2dsconfig import build_dsconfig
from ..update import update_config
from ..yaml_utils import dump_to_string, get_yaml


yaml = get_yaml()


def to_dsconfig(config):
    sanity_check_config(config)  # Just make sure we don't test broken configs
    assert list(check_config(config, load_code=False)) == []
    dsconfig = build_dsconfig(config)
    return dsconfig


def update(orig_config, dsconfig, ms_name="macroserver/demo1/1") -> str:
    "Update the given config to reflect the given dsconfig"
    new_config = build_sardana_config(dsconfig, ms_name, include_tango_host=False)
    updated_config = update_config(dump_to_string(yaml, orig_config), new_config)
    updated_config_str = dump_to_string(yaml, updated_config)
    return updated_config_str


def test_roundtrip__attribute_json_nested_list():
    CONFIG = f"""\
pools:
  demo1:
    controllers:
      motctrl01:
        type: Motor
        python_module: "some_stuff.py"
        python_class: MyMotorCtrl
        attributes:
          # It is possible to use JSON style in YAML
          # This will be interpreted as a list of values
          MyCalibration: [[-1000, -3.5, -3.4], [-1, 0, 1]]
macro_servers:
  demo1:
    doors:
      Door_demo1_1:
        tango_device: Door/demo1/01
"""
    orig_config = yaml.load(CONFIG)
    dsconfig = to_dsconfig(orig_config)
    assert update(orig_config, dsconfig) == CONFIG


def test_roundtrip__attribute_json_nested_list_multiline():
    CONFIG = f"""\
pools:
  demo1:
    controllers:
      motctrl01:
        type: Motor
        python_module: "some_stuff.py"
        python_class: MyMotorCtrl
        attributes:
          MyCalibration:
          # This means the same thing as above
          - [-1000, -3.5, -3.4]
          - [-1, 0, 1]
macro_servers:
  demo1:
    doors:
      Door_demo1_1:
        tango_device: Door/demo1/01
"""
    orig_config = yaml.load(CONFIG)
    dsconfig = to_dsconfig(orig_config)

    assert dsconfig["servers"]["Sardana"]["demo1"]["Controller"]\
        ["controller/mymotorctrl/motctrl01"]["attribute_properties"]\
        ["MyCalibration"]["__value"] == ['[[-1000, -3.5, -3.4], [-1, 0, 1]]']

    assert update(orig_config, dsconfig) == CONFIG


def test_roundtrip__attribute_nested_list_expanded():
    CONFIG = f"""\
pools:
  demo1:
    controllers:
      motctrl01:
        type: Motor
        python_module: "some_stuff.py"
        python_class: MyMotorCtrl
        attributes:
          MyCalibration:
          # Also same as above (although this looks pretty ugly)
          - - -1000
            - -3.5
            - -3.4
          - - -1
            - 0
            - 1
macro_servers:
  demo1:
    doors:
      Door_demo1_1:
        tango_device: Door/demo1/01
"""
    orig_config = yaml.load(CONFIG)
    dsconfig = to_dsconfig(orig_config)

    assert dsconfig["servers"]["Sardana"]["demo1"]["Controller"]\
        ["controller/mymotorctrl/motctrl01"]["attribute_properties"]\
        ["MyCalibration"]["__value"] == ['[[-1000, -3.5, -3.4], [-1, 0, 1]]']
    assert update(orig_config, dsconfig) == CONFIG


def test_roundtrip__attribute_plain_list():
    CONFIG = """\
pools:
  demo1:
    controllers:
      motctrl01:
        type: Motor
        python_module: "some_stuff.py"
        python_class: MyMotorCtrl
        attributes:
          MyThings:
          # This is just a list of values, intrepreted as YAML
          - a
          - b
          - -3.14e06  # Formatting should stay
macro_servers:
  demo1:
    doors:
      Door_demo1_1:
        tango_device: Door/demo1/01
"""
    orig_config = yaml.load(CONFIG)
    dsconfig = to_dsconfig(orig_config)
    # Check that it's stored as a proper JSON value
    json.loads(dsconfig["servers"]["Sardana"]["demo1"]["Controller"]\
               ["controller/mymotorctrl/motctrl01"]["attribute_properties"]\
               ["MyThings"]["__value"][0])
    assert update(orig_config, dsconfig) == CONFIG


def test_roundtrip__attribute_dict():
    CONFIG = """\
pools:
  demo1:
    controllers:
      motctrl01:
        type: Motor
        python_module: "some_stuff.py"
        python_class: MyMotorCtrl
        attributes:
          MyConfig:
          # To use a dict, it must be wrapped in a "value" key
            value:
              # In here we can have any stuff we want
              something:
              - 1
              - "banana of sorts"  # quotes are preserved
              - [1, 2, 3]
              others:
                subkey: 123.4
                lalala: true
macro_servers:
  demo1:
    doors:
      Door_demo1_1:
        tango_device: Door/demo1/01
"""
    orig_config = yaml.load(CONFIG)
    dsconfig = to_dsconfig(orig_config)
    # The dict is encoded as a single string
    assert len(
        dsconfig["servers"]["Sardana"]["demo1"]["Controller"]\
        ["controller/mymotorctrl/motctrl01"]["attribute_properties"]\
        ["MyConfig"]["__value"]
    ) == 1
    assert update(orig_config, dsconfig) == CONFIG


def test_roundtrip__attribute_value_invalid_yaml():
    CONFIG = """\
pools:
  demo1:
    controllers:
      motctrl01:
        type: Motor
        python_module: "some_stuff.py"
        python_class: MyMotorCtrl
        attributes:
          # Percent has special meaning in YAML, so the value
          # must be wrapped in quotes.
          MyConfig: "%abcd"
macro_servers:
  demo1:
    doors:
      Door_demo1_1:
        tango_device: Door/demo1/01
"""
    orig_config = yaml.load(CONFIG)
    dsconfig = to_dsconfig(orig_config)
    assert update(orig_config, dsconfig) == CONFIG


def test_roundtrip__measurement_groups(tango_host):
    CONFIG = f"""\
pools:
  demo1:
    controllers:
      some_controller:
        type: CTExpChannel
        python_module: "something.py"
        python_class: "MyChannel"
        elements:
          ct01:
            axis: 1
    measurement_groups:
      hello1:
        channels:
        - ct01:  # Internal
            enabled: false
            output: false
        - tango://{ tango_host }/sys/tg_test/1/double_scalar  # External
        - tango://{ tango_host }/sys/tg_test/1/ampli:  # Also external
            data_units: inches
            plot_type: 1
            plot_axes: [<mov>]
macro_servers:
  demo1:
    doors:
      Door_demo1_1:
        tango_device: Door/demo1/01
"""
    orig_config = yaml.load(CONFIG)
    dsconfig = to_dsconfig(orig_config)

    meas_grp = json.loads(dsconfig["servers"]["Sardana"]["demo1"]["MeasurementGroup"]\
                          ["mntgrp/pool_demo1_1/hello1"]["attribute_properties"]\
                          ["Configuration"]["__value"][0])
    assert len(meas_grp["controllers"][f"tango://{ tango_host }/controller/mychannel/some_controller"]["channels"]) == 1
    assert len(meas_grp["controllers"]["__tango__"]["channels"]) == 2

    assert update(orig_config, dsconfig) == CONFIG
