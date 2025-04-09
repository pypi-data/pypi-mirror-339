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
import os
import sys
from pathlib import Path
from typing import Tuple, Union, Any, Sequence, Optional

import click
from jsonpatch import make_patch, apply_patch
from ruamel.yaml import YAML, comments, RoundTripConstructor

from .validate import sanity_check_config
from .yaml_utils import load_yaml_roundtrip, load_yaml


logger = logging.getLogger(__name__)


def _construct_include_tag(constructor, node):
    raise RuntimeError("No support for !include tags! Try the --inplace option.")


class NoIncludeConstructor(RoundTripConstructor):
    "Ruamel YAML constructor that supports loading external files via !include."


NoIncludeConstructor.add_constructor('!include', _construct_include_tag)


def update_config(original_yaml: str, updated_config: dict):
    """
    Diff the configs, producing a patch, and apply it to the original.
    The idea is to preserve the original structure as far as possible,
    while logically the result is equal to the updated one.

    Arguments:
      original_yaml: YAML string
      updated_config: loaded configuration
    """

    # Load only logical content
    yaml = YAML(typ="rt")
    yaml.Constructor = NoIncludeConstructor
    yaml.preserve_quotes = True
    try:
        original_config = yaml.load(original_yaml)
    except RuntimeError:
        sys.exit("Sorry, !include tags don't work here, try the --inplace flag.")
    try:
        sanity_check_config(original_config)
    except RuntimeError as e:
        sys.exit(f"Original config is not valid: {e}")

    try:
        sanity_check_config(updated_config)
    except RuntimeError as e:
        sys.exit(f"Updated config is not valid: {e}")

    # The patch will only take logical differences into account
    patch = make_patch(original_config, updated_config)

    original = yaml.load(original_yaml)
    apply_patch(original, patch, in_place=True)
    return original


class Include:
    def __init__(self, node):
        self.node = node

    @property
    def filename(self):
        return self.node.value

    @classmethod
    def from_yaml(cls, loader, node):
        return cls(node)

    @staticmethod
    def to_yaml(dumper, data):
        return dumper.represent_scalar("!include", data.node.value)


def find_includes(config_node: Any, path: Tuple[Union[int, str]] = ()
                  ) -> Tuple[Sequence[Union[int, str]], Include]:
    """
    Recursively find any !include objects in a parsed config.
    Generates tuples of filename and location in the YAML.
    """
    if isinstance(config_node, comments.TaggedScalar):
        if config_node.tag == "!include":
            # Found one!
            # TODO need to escape the path in any way?
            yield (config_node.value, "/" + "/".join(path))
        else:
            raise RuntimeError(f"Unknown tag: '{config_node.tag}'")
    if isinstance(config_node, dict):
        for key, value in config_node.items():
            subpath = path + (key,)
            yield from find_includes(value, subpath)
    elif isinstance(config_node, list):
        for i, value in enumerate(config_node):
            subpath = path + (i,)
            yield from find_includes(value, subpath)
    else:
        # A leaf node, nothing more to do
        return


def localize_patch(p: dict, parent_path: str):
    "Modify path to work on an included file"
    assert p["path"].startswith(parent_path)
    assert p["path"] != parent_path
    subpath = p["path"][len(parent_path):]
    return {**p, "path": subpath}


def update_in_place(original_file: str, updated_config: Optional[dict] = None,
                    patch: Optional[list] = None):
    """
    Merge updates into existing YAML config, on disk.

    Supports "!include" tags to split the config into several parts,
    which can be useful for more complex configurations. Original
    structure should still be preserved as far as possible.

    The updated_config is expected to be a single YAML config.
    """
    # First, load the complete original config (!include followed)
    yaml = YAML(typ="safe")
    yaml.preserve_quotes = True
    orig_path, orig_filename = os.path.split(original_file)
    old_cwd = None
    if orig_path:
        # Change directory to allow loading included files with relative path
        old_cwd = os.getcwd()
        os.chdir(orig_path)
    complete_original = load_yaml_roundtrip(orig_filename)
    if patch is None:
        patch = make_patch(complete_original, updated_config)

    # Now load original again, this time *without* following includes
    # We will end up with ruamel TaggedScalar objects instead.
    yaml = YAML(typ="rt")
    yaml.preserve_quotes = True
    shallow_original = yaml.load(Path(orig_filename))

    # Find all '!include' tags
    includes = list(find_includes(shallow_original))
    include_paths = {p for _, p in includes}

    # Find changes that belong in this file and not in included ones
    local_patch = [
        p for p in patch
        if not any(p["path"].startswith(ip) and p["path"] != ip
                   for ip in include_paths)
    ]
    # Apply local patches and overwrite original file
    # TODO optional backup?
    if (local_patch):
        apply_patch(shallow_original, local_patch, in_place=True)
        with open(orig_filename, "w") as f:
            yaml.dump(shallow_original, f)

    # Go through included files and repeat the process, recursively
    for include, path in includes:
        include_patch = [
            localize_patch(p, path)
            for p in patch
            if p["path"].startswith(path) and p["path"] != path
        ]
        if include_patch:
            update_in_place(include, patch=include_patch)

    if old_cwd:
        os.chdir(old_cwd)


@click.argument("original_yaml", type=click.File("r"), required=True)
@click.argument("new_yaml", type=click.File("r"), required=True)
@click.option("--inplace", is_flag=True)
def update_cmd(original_yaml, new_yaml, inplace):
    """
    Update configuration, maintaining order and comments.
    Takes two YAML config files; "original" and "new". This script will then
    apply the changes from the new config to the original, while keeping as
    much as possible of the original structure intact. This includes the order
    of things, comments, etc. The updated configuration is functionally identical
    to the "new" one.

    The resulting new YAML content is printed to stdout, by default.

    With the --inplace flag, the original YAML file is instead overwritten
    with any changes. In this mode, it's also possible to use !include tags
    in the YAML to separate parts out into other files. This allows for
    complex configurations to be split up logically.
    """
    yaml = YAML(typ="rt")
    yaml.preserve_quotes = True
    if inplace:
        assert original_yaml.name != "<stdin>", "Can't read original from stdin when updating in place!"
        update_in_place(original_yaml.name, yaml.load(new_yaml))
    else:
        merged = update_config(original_yaml.read(),
                               yaml.load(new_yaml))
        yaml.dump(merged, sys.stdout)


def main():
    cmd = click.command("merge")(update_cmd)
    return cmd()


if __name__ == "__main__":
    main()
