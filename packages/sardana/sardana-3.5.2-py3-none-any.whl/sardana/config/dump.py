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
import dsconfig.dump
from sardana.pool.pool import ElementType
from ruamel.yaml import YAML
import tango

from .dsconfig2yaml import build_sardana_config


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

yaml = YAML(typ="rt")


@click.argument("macro_server", required=False)
def dump_cmd(macro_server: str):
    """
    Export an existing Sardana install to YAML.
    If there is only one macro server in the database, use that. Otherwise
    the user must specify the device name of the relevant macro server.
    """
    db = tango.Database()
    if macro_server is None:
        # Try to auto-detect macro server
        # TODO use a better way that includes unexported devices
        macro_servers = db.get_device_exported_for_class("MacroServer")
        if len(macro_servers) == 0:
            sys.exit("No MacroServer found; nothing to dump!")
        if len(macro_servers) > 1:
            sys.exit(f"Found several MacroServers: {', '.join(macro_servers)}."
                     " Please specify which to use.")
        macro_server = macro_servers[0]
    try:
        current_config = dump_sardana_config(macro_server, db)
    except RuntimeError as e:
        sys.exit(str(e))
    yaml.dump(current_config, sys.stdout)


def get_local_pools(db, pools):
    "Generate pools not belonging to a different CS"
    tango_host = f"{db.get_db_host()}:{db.get_db_port()}"
    for pool in pools:
        if pool.startswith("tango://"):
            if tango_host.lower() in pool.lower():
                yield pool
            else:
                logger.warning(f"Ignoring remote pool '{pool}'")
        else:
            yield pool


def check_id_and_physical_roles_existence(ds_config: dict) -> None:
    """Checks the ds_config for elements still using id, motor_role_ids or 
    counter_role_ids properties instead of aliases and physical_roles.
    Warns if any are found."""

    element_wrong_properties = set()
    try:
        pool_list = ds_config['servers']['Pool'].values()
    except KeyError:
        pool_list = ds_config['servers']['Sardana'].values()
    for pool in pool_list:
        for element_class, elements in pool.items():
            if element_class == "MotorGroup":
                # Motor groups are still created with numeric IDs (Issue #1926)
                # and need to be omitted explicitly to prevent dump error.
                continue
            for element in elements.values():
                if "properties" not in element:
                    continue
                if "id" in element['properties']:
                    element_wrong_properties.add(element['alias'])
                    continue
                if element_class in ["PseudoMotor", "PseudoCounter"]:
                    property_names = element["properties"].keys()
                    if "motor_role_ids" in property_names or "counter_role_ids" in property_names:
                        element_wrong_properties.add(element['alias'])

    if element_wrong_properties:
        logging.error("There are elements still using the properties id, motor_role_ids or counter_role_ids. "
                      + "Sardana config is meant to be used with custom settings "
                      + "USE_NUMERIC_ELEMENT_IDS=False and USE_PHYSICAL_ROLES_PROPERTY=True. "
                      + "If both settings are in use, ensure you have migrated Sardana and "
                      + "restarted the Pool and MacroServer.\n"
                      + "Although the dump was successful, it cannot be restored.\n"
                      + "List of elements with problems: " + str(element_wrong_properties))
        sys.exit()


def check_dsconfig(dsconfig):
    """
    Check a given dsconfig dump for known issues
    """
    found_classes = set()
    for srv, insts in dsconfig["servers"].items():
        for inst, clss in insts.items():
            for cls, devs in clss.items():
                if cls not in ElementType:
                    # Ignore all non-sardana devices
                    continue
                found_classes.add(cls)
                for dev, info in devs.items():
                    if "alias" not in info:
                        yield (f"Device {dev} does not have an alias!"
                               + " Please create the proper alias in the Tango DB.")
    if "Pool" not in found_classes:
        yield "No Pool device found!"
    if "MacroServer" not in found_classes:
        yield "No MacroServer device found!"


def dump_sardana_config(macro_server: str, db: tango.Database = None) -> dict:
    "Helper to dump data from the Tango DB"
    # Find the relevant pools
    # TODO handle errors
    if db is None:
        db = tango.Database()
    servers = set()
    try:
        if "/" not in macro_server:
            # Assume it's an alias
            macro_server = db.get_device_from_alias(macro_server)
        ms_server = db.get_device_info(macro_server).ds_full_name
    except tango.DevFailed as e:
        raise RuntimeError(f"Unable to get info about MacroServer {macro_server}: {e}")
    servers.add(ms_server)
    pool_names = db.get_device_property(macro_server, "PoolNames")["PoolNames"]
    try:
        pool_devices = [
            name if "/" in name else db.get_device_from_alias(name)
            for name in pool_names
        ]
    except tango.DevFailed as e:
        raise RuntimeError(f"Could not find pool listed for {macro_server}: {e.args[0].desc}")
    pool_servers = set(
        db.get_device_info(pd).ds_full_name
        # We ignore any pools belonging to a different control system
        for pd in get_local_pools(db, pool_devices)
    )
    servers.update(pool_servers)

    # Dump the relevant data from the Tango database
    ds_config = dsconfig.dump.get_db_data(db, [f"server:{s}" for s in servers])

    # Sanity check the dump
    problems = list(check_dsconfig(ds_config))
    if problems:
        for problem in problems:
            logger.fatal(problem)
        raise RuntimeError("Encountered problems with the Tango DB dump, which must be fixed before proceeding! See logs.")

    check_id_and_physical_roles_existence(ds_config)
    return build_sardana_config(ds_config, macro_server)


def main():
    cmd = click.command("dump")(dump_cmd)
    return cmd()


if __name__ == "__main__":
    main()
