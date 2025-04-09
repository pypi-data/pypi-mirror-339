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
Very basic diffing functionality for sardana YAML config files.

The point compared to regular "diff" is we don't care about
things like dict ordering, only structure. Since we know about
the structure, we could improve the output further to make it more
user friendly.

TODO allow outputting computer friendly format e.g. JSON
"""

from textwrap import indent

import click
from jsonpatch import make_patch
from jsonpointer import resolve_pointer
from .common import remove_defaults
from .yaml_utils import load_yaml_roundtrip, dump_to_string, get_yaml


def make_diff(original, new):
    patch = make_patch(original, new)
    pool_changes = {}
    ms_changes = {}
    other_changes = []
    for line in patch:
        path = line["path"].split("/")
        if path[1] == "pools":
            pool_changes.setdefault(path[2], []).append(line)
        elif path[1] == "macro_servers":
            ms_changes.setdefault(path[2], []).append(line)
        else:
            other_changes.append(line)
    return {
        pool: list(format_changes(original, changes))
        for pool, changes in pool_changes.items()
    }, {
        ms: list(format_changes(original, changes))
        for ms, changes in ms_changes.items()
    }, list(format_changes(original, other_changes))


def represent(value):
    "Work around for some strange dumping behavior of YAML"
    if isinstance(value, (list, dict)):
        return dump_to_string(yaml, value)
    return str(value)


yaml = get_yaml()


def format_changes(original, changes):
    for line in changes:
        op = line["op"]
        if line.get("path") == "/tango_host":
            # Don't care about changes to tango_host, it's not part of the
            # configuration as such, so it's mostly confusing.
            # TODO might be interesting in some circumstances though..?
            continue
        if op == "move":
            # Don't care about changes only in casing
            if line["from"].lower() != line["path"].lower():
                yield "- MOVE {from}\n    to {path}".format(**line)
        elif op == "remove":
            yield "- REMOVE {path}".format(**line)
        elif op == "add":
            yield ("- ADD {path}\n".format(**line)
                   + indent(represent(line["value"]), " " * 4))
        elif op == "replace":
            path = line["path"]
            value = line["value"]
            old_value = resolve_pointer(original, path)
            yield f"- REPLACE {path} {old_value} => {value}"
        else:
            yield line


def print_diff(pool_diff, ms_diff, other_diff):
    if not any([pool_diff, ms_diff, other_diff]):
        print("No differences!")
        return
    for change in other_diff:
        print(change)
    for pool, changes in pool_diff.items():
        print("Pool: {}".format(pool))
        for change in changes:
            print(change)
    for ms, changes in ms_diff.items():
        print("Macroserver: {}".format(ms))
        for change in changes:
            print(change)


@click.argument("old_config", type=click.File("r"))
@click.argument("new_config", type=click.File("r"))
def diff_cmd(old_config, new_config):
    """
    Compare two given YAML sardana configuration files.
    """
    # Allow either of the inputs to be stdin, to enable piping
    yaml = get_yaml()
    if old_config.name == "<stdin>":
        old_config_complete = yaml.load(old_config)
    else:
        old_config_complete = load_yaml_roundtrip(old_config.name)

    if new_config.name == "<stdin>":
        new_config_complete = yaml.load(new_config)
    else:
        new_config_complete = load_yaml_roundtrip(new_config.name)

    pool_diff, ms_diff, other_diff = make_diff(
        remove_defaults(old_config_complete),
        remove_defaults(new_config_complete),
    )
    print_diff(pool_diff, ms_diff, other_diff)


def main():
    cmd = click.command("diff")(diff_cmd)
    return cmd()


if __name__ == "__main__":
    main()
