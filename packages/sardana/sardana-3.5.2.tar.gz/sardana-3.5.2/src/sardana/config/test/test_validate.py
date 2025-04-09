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

from ..validate import sanity_check_config


def test_sanity_check_config__basic(sar_demo_yaml):
    sanity_check_config(sar_demo_yaml)


def test_sanity_check_config__no_ms():
    config = {
        "pools": {
            "pool1": {}
        },
        "macro_servers": {}
    }
    with pytest.raises(RuntimeError) as exc_info:
        sanity_check_config(config)
    assert "exactly one MacroServer" in str(exc_info.value)


def test_sanity_check_config__too_many_ms():
    config = {
        "pools": {
            "pool1": {}
        },
        "macro_servers": {
            "hello1": {
                "doors": {}
            },
            "hello2": {
                "doors": {}
            },
        }
    }
    with pytest.raises(RuntimeError) as exc_info:
        sanity_check_config(config)
    assert "exactly one MacroServer" in str(exc_info.value)


def test_sanity_check_config__bad_channel(sar_demo_yaml):
    sar_demo_yaml["pools"]["demo1"]["measurement_groups"]["mntgrp01"]\
        ["channels"][2] = "ct03_wrong"
    with pytest.raises(RuntimeError) as exc_info:
        sanity_check_config(sar_demo_yaml)
    assert "ct03_wrong" in str(exc_info.value)


def test_sanity_check_config__pool_controller_elements_none(sar_demo_yaml):
    sar_demo_yaml["pools"]["demo1"]["controllers"]["test"] = {
        "python_module": "hello.py",
        "python_class": "MyClass",
        "elements": None,
        "type": "Motor",
    }
    with pytest.raises(RuntimeError) as exc_info:
        sanity_check_config(sar_demo_yaml)
    assert "elements" in str(exc_info.value)


def test_sanity_check_config__pool_instruments_none(sar_demo_yaml):
    sar_demo_yaml["pools"]["demo1"]["instruments"] = None
    with pytest.raises(RuntimeError) as exc_info:
        sanity_check_config(sar_demo_yaml)
    assert "instruments" in str(exc_info.value)


def test_sanity_check_config__pool_controller_element_attribute_none(sar_demo_yaml):
    sar_demo_yaml["pools"]["demo1"]["controllers"]["ctctrl01"]["attributes"]["Synchronizer"] = {
        "value": 123,
        "label": "something",
        "abs_change": None,
    }
    with pytest.raises(RuntimeError) as exc_info:
        sanity_check_config(sar_demo_yaml)
    assert "Synchronizer" in str(exc_info.value)
