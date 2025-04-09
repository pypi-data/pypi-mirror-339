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
Entry point for the "sardanactl config" command
"""

import logging
import sys

import click

from .load import load_cmd
from .dump import dump_cmd
from .validate import validate_cmd
from .diff import diff_cmd
from .update import update_cmd
from .graph import graph_cmd



def check_custom_settings():
    from sardana import sardanacustomsettings
    use_numeric_element_ids = getattr(
            sardanacustomsettings, "USE_NUMERIC_ELEMENT_IDS", False
        )
    use_physical_roles_property = getattr(
            sardanacustomsettings, "USE_PHYSICAL_ROLES_PROPERTY", True
        )
    if (use_numeric_element_ids) or (not use_physical_roles_property):
        logging.error("Sardana config is meant to be used with custom settings USE_NUMERIC_ELEMENT_IDS=False and USE_PHYSICAL_ROLES_PROPERTY=True. "
                      + "If both settings are in use, ensure you have migrated Sardana and restarted the Pool and MacroServer.")
        return False

    return True

@click.group("config")
@click.option("--debug", "-d", is_flag=True, default=False)
def config_grp(debug):
    """
    This command groups the various configuration actions available.
    In general, filename arguments may be replaced with "-" in order
    to read from stdin. Any YAML output is written to stdout.
    """
    if not check_custom_settings():
        sys.exit()
    if debug:
        # TODO I think this comes too late to have an effect..?
        logging.basicConfig(level=logging.DEBUG)


config_grp.command("load")(load_cmd)
config_grp.command("dump")(dump_cmd)
config_grp.command("validate")(validate_cmd)
config_grp.command("diff")(diff_cmd)
config_grp.command("update")(update_cmd)
config_grp.command("graph")(graph_cmd)
