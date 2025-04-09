from io import StringIO
import os
from pathlib import Path

import ruamel.yaml


def represent_none(self, _):
    return self.represent_scalar('tag:yaml.org,2002:null', '')


def get_yaml(typ="rt", **kwargs):
    "Return a properly configured YAML object"
    yaml = ruamel.yaml.YAML(typ=typ, **kwargs)
    yaml.preserve_quotes = True
    yaml.default_flow_style = False
    # Change the default representation of None/null to nothing
    yaml.representer.add_representer(type(None), represent_none)
    return yaml


def load_yaml(filepath: str):
    """
    Load YAML from a given file.
    Supports "!include" tags, to load external files.
    """
    yaml = get_yaml(typ="safe")

    def _construct_include_tag(constructor, node):
        external_fpath = Path(node.value)
        if not external_fpath.exists():
            raise IOError(f'Included external yaml file {external_fpath} '
                          'does not exist')
        res = load_yaml(external_fpath)
        return res

    class SafeIncludeConstructor(ruamel.yaml.SafeConstructor):
        "Ruamel YAML constructor that supports loading external files via !include."

    yaml.Constructor = SafeIncludeConstructor
    SafeIncludeConstructor.add_constructor('!include', _construct_include_tag)

    path, filename = os.path.split(filepath)
    wd = os.getcwd()
    if path:
        os.chdir(path)
    with open(filename) as f:
        data = yaml.load(f)
    if path:
        os.chdir(wd)
    return data


def load_yaml_roundtrip(filepath: str):
    """
    Load YAML from a given file.
    Supports "!include" tags, to load external files.
    Supports "round-trip", i.e. YAML formatting hints are included in the
    returned data, and can be reconstructed when dumping back to YAML.
    """
    yaml = get_yaml(typ="rt")

    def _construct_include_tag(constructor, node):
        external_fpath = Path(node.value)
        if not external_fpath.exists():
            raise IOError(f'Included external yaml file {external_fpath} '
                          'does not exist')
        res = load_yaml_roundtrip(node.value)
        return res

    class RoundTripIncludeConstructor(ruamel.yaml.RoundTripConstructor):
        "Ruamel YAML constructor that supports loading external files via !include."

    yaml.Constructor = RoundTripIncludeConstructor
    RoundTripIncludeConstructor.add_constructor('!include', _construct_include_tag)

    path, filename = os.path.split(filepath)
    wd = os.getcwd()
    if path:
        os.chdir(path)
    with open(filename) as f:
        data = yaml.load(f)
    if path:
        os.chdir(wd)
    return data


def strip_document_end_marker(s):
    "Useful as a transform when expecting single scalars"
    if s.endswith('...\n'):
        return s[:-4]
    return s


def dump_to_string(yaml, obj, **kwargs):
    """
    Wrapper, since ruamel doesn't have a function to dump to string.
    """
    stringio = StringIO()
    yaml.dump(obj, stringio, transform=strip_document_end_marker, **kwargs)
    return stringio.getvalue()
