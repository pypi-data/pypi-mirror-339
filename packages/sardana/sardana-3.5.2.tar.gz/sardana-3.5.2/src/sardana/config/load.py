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

import logging
import sys

import click
from dsconfig import json2tango
import tango

from .validate import sanity_check_config
from .dump import dump_sardana_config
from .diff import make_diff, print_diff
from .yaml2dsconfig import build_dsconfig, get_device_name
from .common import remove_defaults
from .yaml_utils import load_yaml_roundtrip


logger = logging.getLogger(__name__)


@click.argument("config_file", type=str)
@click.option("--write", is_flag=True, default=False, help="Actually make changes to Tango DB.")
@click.option("--check-code", is_flag=True, help="Enable loading controller source code")
@click.option("--ignore-tango-host", is_flag=True,
              help="Allow loading config even if tango_host does not match")
def load_cmd(config_file, write=False, check_code=False, ignore_tango_host=False, current_config=None):
    """
    Read a YAML file and apply it to the Tango DB.
    Unless the "--write" option is provided, the DB is not actually
    changed, and the actions that would have been taken are printed.
    """
    new_config = remove_defaults(load_yaml_roundtrip(config_file))
    try:
        sanity_check_config(new_config, check_code)
    except RuntimeError as e:
        sys.exit(f"Error:\n{e}")

    # If config has tango_host defined, refuse to apply it anywhere else
    if "tango_host" in new_config and not ignore_tango_host:
        tango_host = tango.ApiUtil.get_env_var("TANGO_HOST")
        config_tango_host = new_config.get("tango_host")
        if config_tango_host and config_tango_host != tango_host:
            print(f"Current tango host ({tango_host}) does not match config ({config_tango_host})!"
                  + " If you know what you're doing you can ignore this error with"
                  + " --ignore-tango-host.")
            sys.exit(1)

    ms_name, = new_config["macro_servers"]
    ms_info = new_config["macro_servers"][ms_name]
    ms_device = get_device_name("MacroServer/{name}/1", ms_name, ms_info)

    if current_config is None:
        db = tango.Database()
        try:
            current_config = dump_sardana_config(ms_device, db)
            pool_diff, ms_diff, other_diff = make_diff(current_config, new_config)
            print_diff(pool_diff, ms_diff, other_diff)
        except RuntimeError:
            # TODO it's still possible that some of the pools in the config already
            # exist. How do we handle that? Just warn about ut?
            print(f"Could not find current configuration for {ms_device}."
                  " This appears to be a new config.")
    ds_config = build_dsconfig(new_config)

    if not write:
        print("Nothing was written to the Tango DB. Try '--write'.")
        return

    json2tango.apply_config(ds_config, db, write=True, sleep=0.05, cleanup_protected_props=True)


def main():
    cmd = click.command("load")(load_cmd)
    return cmd()


if __name__ == "__main__":
    main()
