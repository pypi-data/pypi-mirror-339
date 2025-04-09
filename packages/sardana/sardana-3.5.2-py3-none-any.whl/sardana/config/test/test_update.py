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

import io

from ruamel.yaml import YAML

from ..update import update_config, update_in_place


def test_update_basic(sar_demo_yaml_raw, sar_demo_yaml):
    merged = update_config(sar_demo_yaml_raw, sar_demo_yaml)
    ruamel = YAML(typ="rt")
    out = io.StringIO()
    ruamel.dump(merged, out)
    assert sar_demo_yaml_raw == out.getvalue()


def test_update__include_trivial(tmpdir):
    """
    Test that updating a split configuration (two YAML files with include)
    can be updated with the same logical config, and the files will be
    unchanged.

    Basically simulates dumping a config from an existing installation
    and updating an already up to date, split config on disk.
    """

    # This is the simulated "dump"; here, ordering etc should not matter,
    # as this comes from the database.
    CONFIG_DUMP = """\
pools:
  demo1:
    controllers:
      external_ctrl:
        type: Motor
        python_class: "SomeCtrl"
        python_module: "some_ctrl.py"
        elements:
            ext1:
                axis: 1
      motctrl01:
        type: Motor
        python_class: MyMotorCtrl
        python_module: "some_stuff.py"
macro_servers:
  demo1:
    doors:
      Door_demo1_1:
"""

    # This is the preexisting config, presumed to be on disk
    SPLIT_CONFIG = """\
pools:
  demo1:
    controllers:
      external_ctrl: !include "./external_ctrl.yaml"
      motctrl01:
        # I am a controller
        type: Motor
        python_module: "some_stuff.py"
        python_class: MyMotorCtrl
macro_servers:
  demo1:
    doors:
      Door_demo1_1:
"""

    # File referenced from the main config
    EXTERNAL_CTRL = """\
# This is a small part
type: Motor
python_module: "some_ctrl.py"
python_class: "SomeCtrl"
elements:
  ext1:
    axis: 1
"""

    split_config_file = tmpdir.join("config.yaml")
    split_config_file.write(SPLIT_CONFIG)
    external_file = tmpdir.join("external_ctrl.yaml")
    external_file.write(EXTERNAL_CTRL)

    yaml = YAML(typ="safe")
    config = yaml.load(CONFIG_DUMP)
    update_in_place(str(split_config_file), config)

    final_config = split_config_file.read()
    assert final_config == SPLIT_CONFIG
    final_external = external_file.read()
    assert final_external == EXTERNAL_CTRL


def test_update__include_change(tmpdir):

    CONFIG_DUMP = """\
pools:
  demo1:
    controllers:
      external_ctrl:
        type: Motor
        python_module: "some_ctrl.py"
        python_class: "SomeOtherCtrl"  # Changed
        elements:
            ext1:
                axis: 1
      motctrl01:
        type: Motor
        python_module: "some_stuff.py"
        python_class: MyMotorCtrl
macro_servers:
  demo1:
    doors:
      Door_demo1_1:
"""

    SPLIT_CONFIG = """\
pools:
  demo1:
    controllers:
      external_ctrl: !include "./external_ctrl.yaml"
      motctrl01:
        type: Motor
        python_module: "some_stuff.py"
        python_class: MyMotorCtrl
macro_servers:
  demo1:
    doors:
      Door_demo1_1:
"""

    EXTERNAL_CTRL = """\
# This is a small part
type: Motor
python_module: "some_ctrl.py"
python_class: "SomeCtrl"
elements:
  ext1:
    axis: 1
"""

    split_config_file = tmpdir.join("config.yaml")
    split_config_file.write(SPLIT_CONFIG)
    external_file = tmpdir.join("external_ctrl.yaml")
    external_file.write(EXTERNAL_CTRL)

    yaml = YAML(typ="rt")
    config = yaml.load(CONFIG_DUMP)
    update_in_place(str(split_config_file), config)

    final_config = split_config_file.read()
    # No changes to the "main" file
    assert final_config == SPLIT_CONFIG

    final_external = external_file.read()
    # Everything should be the same, except the changed value
    assert final_external == """\
# This is a small part
type: Motor
python_module: "some_ctrl.py"
python_class: "SomeOtherCtrl"
elements:
  ext1:
    axis: 1
"""


def test_update__include_addition(tmpdir):

    CONFIG_DUMP = """\
pools:
  demo1:
    controllers:
      external_ctrl:
        type: Motor
        python_module: "some_ctrl.py"
        python_class: "SomeCtrl"
        tango_device: "some/name/45"  # This is new
        elements:
            ext1:
                axis: 1
      motctrl01:
        type: Motor
        python_module: "some_stuff.py"
        python_class: MyMotorCtrl
macro_servers:
  demo1:
    doors:
      Door_demo1_1:
"""

    SPLIT_CONFIG = """\
pools:
  demo1:
    controllers:
      external_ctrl: !include "./external_ctrl.yaml"
      motctrl01:
        type: Motor
        python_module: "some_stuff.py"
        python_class: MyMotorCtrl
macro_servers:
  demo1:
    doors:
      Door_demo1_1:
"""

    EXTERNAL_CTRL = """\
# This is a small part
type: Motor
python_module: "some_ctrl.py"
python_class: "SomeCtrl"
elements:
  ext1:
    axis: 1
"""

    split_config_file = tmpdir.join("config.yaml")
    split_config_file.write(SPLIT_CONFIG)
    external_file = tmpdir.join("external_ctrl.yaml")
    external_file.write(EXTERNAL_CTRL)

    yaml = YAML(typ="rt")
    config = yaml.load(CONFIG_DUMP)
    update_in_place(str(split_config_file), config)

    final_config = split_config_file.read()
    # No changes to the "main" file
    assert final_config == SPLIT_CONFIG

    final_external = external_file.read()
    # Things added to the dumped config will always appear at the
    # end in the final result, since they are not present in the existing config.
    assert final_external == EXTERNAL_CTRL + 'tango_device: some/name/45\n'


def test_update__rename_include(tmpdir):
    """
    The update command should handle an included item being renamed.
    """

    CONFIG_DUMP = """\
pools:
  demo1:
    controllers:
      my_renamed_ctrl:  # renamed controller
        type: Motor
        python_module: "some_ctrl.py"
        python_class: "SomeCtrl"
        elements:
            ext1:
                axis: 1
      motctrl01:
        type: Motor
        python_module: "some_stuff.py"
        python_class: MyMotorCtrl
macro_servers:
  demo1:
    doors:
      Door_demo1_1:
"""

    SPLIT_CONFIG = """\
pools:
  demo1:
    controllers:
      external_ctrl: !include "./external_ctrl.yaml"
      motctrl01:
        type: Motor
        python_module: "some_stuff.py"
        python_class: MyMotorCtrl
macro_servers:
  demo1:
    doors:
      Door_demo1_1:
"""

    EXTERNAL_CTRL = """\
# This is a small part
type: Motor
python_module: "some_ctrl.py"
python_class: "SomeCtrl"
elements:
  ext1:
    axis: 1
"""

    split_config_file = tmpdir.join("config.yaml")
    split_config_file.write(SPLIT_CONFIG)
    external_file = tmpdir.join("external_ctrl.yaml")
    external_file.write(EXTERNAL_CTRL)

    yaml = YAML(typ="rt")
    config = yaml.load(CONFIG_DUMP)
    update_in_place(str(split_config_file), config)

    final_config = split_config_file.read()
    # Controller renamed in the main file
    # Note that the order changed here; there is no proper way to "rename"
    # a key with json-patch AFAIK, so it's been removed and added back.
    assert 'my_renamed_ctrl: !include "./external_ctrl.yaml"' in final_config
    assert "external_ctrl:" not in final_config

    final_external = external_file.read()
    # The external file is not changed
    assert final_external == EXTERNAL_CTRL
