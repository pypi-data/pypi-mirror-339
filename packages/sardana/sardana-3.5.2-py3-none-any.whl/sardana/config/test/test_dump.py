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

from dsconfig.json2tango import apply_config
import pytest
import tango
from ruamel.yaml import YAML

from ..dump import dump_cmd
from ..dsconfig2yaml import build_sardana_config


yaml = YAML(typ="rt")


def test_dump_cmd(sar_demo_json_unique, capsys):
    """
    Basic test that configures a sar_demo environment in the Tango DB,
    then dumps it back out and checks that we get the same thing back.
    """
    db = tango.Database()
    name, config = sar_demo_json_unique
    apply_config(config, db, write=True)

    ms_device = f"MacroServer/{name}/1"
    dump_cmd(ms_device)
    captured = capsys.readouterr()
    yaml_config = yaml.load(captured.out)

    assert yaml_config == build_sardana_config(config, ms_device)

    db.delete_server(f"Sardana/{name}")


def test_dump__ignores_remote_pools(sar_demo_json_unique, capsys):
    db = tango.Database()
    name, config = sar_demo_json_unique
    # Adding a pool with a different tango host. It should be ignored,
    # but kept in the MS config. These are assumed to be handled some other way.
    config["servers"]["Sardana"][name]["MacroServer"][f"MacroServer/{name}/1"]\
        ["properties"]["PoolNames"].append("tango://some.other.cs:10000/some/other/pool")
    apply_config(config, db, write=True)

    ms_device = f"MacroServer/{name}/1"
    dump_cmd(ms_device)
    captured = capsys.readouterr()
    yaml_config = yaml.load(captured.out)

    expected_config = build_sardana_config(config, ms_device)
    assert yaml_config == expected_config

    assert yaml_config["tango_host"]  # Included by default

    db.delete_server(f"Sardana/{name}")


def test_dump__exit_on_missing_alias(sar_demo_json_unique, capsys):
    db = tango.Database()
    name, config = sar_demo_json_unique
    ms_device = f"MacroServer/{name}/1"
    del config["servers"]["Sardana"][name]["MacroServer"][ms_device]["alias"]
    apply_config(config, db, write=True)

    with pytest.raises(SystemExit):
        dump_cmd(ms_device)


def test_dump__exit_on_missing_pool(sar_demo_json_unique, capsys):
    db = tango.Database()
    name, config = sar_demo_json_unique
    ms_device = f"MacroServer/{name}/1"
    del config["servers"]["Sardana"][name]["Pool"]
    apply_config(config, db, write=True)

    with pytest.raises(SystemExit) as e:
        dump_cmd(ms_device)
    print(e.value)
