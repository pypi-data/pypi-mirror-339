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

import copy
import re

import tango


def clean_dict(d):
    """Just drop keys where value is None. We don't want empty stuff."""
    return {
        key: value
        for key, value in d.items()
        if value is not None
    }


SARDANA_NAME_REGEX = "^[a-zA-Z0-9_.-]+$"
DEVICE_NAME_REGEX = r"(?P<device>[^/]+/[^/]+/[^/]+)"
ATTRIBUTE_NAME_REGEX = f"{DEVICE_NAME_REGEX}/(?P<attribute>[^/]+)"
TANGO_HOST_REGEX = r"[^:]+:\d+"
TANGO_PREFIX = rf"tango://(?P<tango_host>{TANGO_HOST_REGEX})"
FULL_DEVICE_NAME_REGEX = rf"{TANGO_PREFIX}/{DEVICE_NAME_REGEX}"
FULL_ATTRIBUTE_NAME_REGEX = rf"{TANGO_PREFIX}/{ATTRIBUTE_NAME_REGEX}"


def get_full_device_name(devname):
    """
    Take a device name and return a full TANGO URI.
    E.g. sys/tg_test/1 -> tango://my.tango.host:10000/sys/tg_test/1
    If it's already a full URI, return it unchanged
    """
    if re.match(FULL_DEVICE_NAME_REGEX, devname):
        return devname
    if re.match(DEVICE_NAME_REGEX, devname):
        # Missing prefix; fill with default tango host
        TANGO_HOST = tango.ApiUtil.get_env_var("TANGO_HOST")
        return f"tango://{TANGO_HOST}/{devname}"
    raise ValueError(f"This does not look like a valid Tango device name: {devname}")


def get_full_attribute_name(attrname):
    """
    Take a device attribute name and return a full TANGO URI.
    E.g. sys/tg_test/1/ampli -> tango://my.tango.host:10000/sys/tg_test/1/ampli
    """
    if re.match(FULL_ATTRIBUTE_NAME_REGEX, attrname):
        return attrname
    if re.match(ATTRIBUTE_NAME_REGEX, attrname):
        # Missing prefix; fill with default tango host
        TANGO_HOST = tango.ApiUtil.get_env_var("TANGO_HOST")
        return f"tango://{TANGO_HOST}/{attrname}"
    raise ValueError(f"This does not look like a valid Tango attribute name: {attrname}")


channel_defaults = {
    "enabled": True,
    "output": True,
    "synchronizer": "software",
    "synchronization": "Trigger",
}


def remove_defaults(config):
    """Remove parts of the configuration that are equal to the sardana defaults"""
    config = copy.deepcopy(config)
    for pool in config.get("pools", {}).values():
        for meas_grp in pool.get("measurement_groups", {}).values():
            channels = list(meas_grp["channels"])
            for i, ch in enumerate(channels):
                if isinstance(ch, dict):
                    ch_name, ch_config = list(ch.items())[0]
                    for k, v in channel_defaults.items():
                        if ch_config.get(k) == v:
                            ch_config.pop(k)
                    if not ch_config:
                        meas_grp["channels"][i] = ch_name
    return config
