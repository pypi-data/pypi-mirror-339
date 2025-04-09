from io import StringIO
import json
import os
from ruamel.yaml import YAML

from dsconfig.dump import get_db_data
import pytest
import tango

from ..load import load_cmd
from ..dsconfig2yaml import build_sardana_config
from ..yaml_utils import dump_to_string, get_yaml


def test_load_cmd(tmpdir, sar_demo_json_unique):
    """
    Basic test that loads a sardana config into the Tango DB and
    then checks that it is the same as expected.
    """
    # This is a dsconfig, where all tango names have been uniquified.
    name, config_json = sar_demo_json_unique

    # Create a YAML config from the dsconfig
    yaml = get_yaml()
    yaml_config = build_sardana_config(config_json, f"MacroServer/{name}/1")
    config_file = tmpdir.join("sar_demo.yaml")
    config_file.write(dump_to_string(yaml, yaml_config))

    # Load the YAML config into the Tango DB
    load_cmd(config_file, write=True)

    # Get a dsconfig back from the DB, and compare to the original
    # They should be the same (we allow different ordering of keys)
    db = tango.Database()
    dump = get_db_data(db, patterns=[f"server:Sardana/{name}"])
    assert (json.dumps(dump, indent=2, sort_keys=True) ==
            json.dumps(config_json, indent=2, sort_keys=True))

    # Clean up
    db.delete_server(f"Sardana/{name}")


def test_load_cmd__cleanup_props(sar_demo_json_unique, tmpdir):
    """
    Check that properties in the DB that aren't in the YAML configuration
    are removed when loading.
    """
    # This is a dsconfig, where all tango names have been uniquified.
    name, config_json = sar_demo_json_unique

    # Create a YAML config from the dsconfig
    yaml = get_yaml()
    yaml_config = build_sardana_config(config_json, f"MacroServer/{name}/1")
    config_file = tmpdir.join("config.yaml")
    config_file.write(dump_to_string(yaml, yaml_config))

    # Load the YAML config into the Tango DB
    load_cmd(str(config_file), write=True)

    # Add properties manually
    db = tango.Database()
    propname = "test_property_123"
    db.put_device_property(f"MacroServer/{name}/1", {propname: ["some value!"]})
    device = f"controller/dummycountertimercontroller/{name}_ctctrl01"
    attrname = "Synchronizer"
    attrprop = "test_attr_property_123"
    db.put_device_attribute_property(device, {attrname: {attrprop: ["some value?"]}})

    # Load the config again
    load_cmd(str(config_file), write=True)

    # Check that the custom property is now gone
    results = db.get_device_property(f"MacroServer/{name}/1", propname)
    assert not results[propname]
    results = db.get_device_attribute_property(device, {attrname: attrprop})
    assert "__value" in results[attrname]  # This is in the config
    assert "attrprop" not in results[attrname]

    # Clean up
    db.delete_server(f"Sardana/{name}")


def test_load_cmd__cleanup_protected_attr_prop(sar_demo_json_unique, tmpdir):
    """
    Check that attribute properties are cleaned up from the DB if they are
    not in the YAML configuration.
    """
    name, config_json = sar_demo_json_unique

    # Create a YAML config from the dsconfig
    yaml_config = build_sardana_config(config_json, f"MacroServer/{name}/1")
    config_file = tmpdir.join("config.yaml")
    yaml = get_yaml()
    config_file.write(dump_to_string(yaml, yaml_config))

    # Load the YAML config into the Tango DB
    load_cmd(str(config_file), write=True)

    device = f"controller/dummycountertimercontroller/{name}_ctctrl01"
    attrname = "Synchronizer"

    # Check that the attribute is there
    db = tango.Database()
    results = db.get_device_attribute_property(device, {attrname: "__value"})
    assert results[attrname]["__value"]

    # Remove the attribute from the YAML config
    del yaml_config["pools"][name]["controllers"][f"{name}_ctctrl01"]["attributes"][attrname]

    # Load the config again
    modified_file = tmpdir.join("modified.yaml")
    yaml = get_yaml()
    modified_file.write(dump_to_string(yaml, yaml_config))
    load_cmd(str(modified_file), write=True)

    # Check that the value is gone
    db = tango.Database()
    results = db.get_device_attribute_property(device, {attrname: "__value"})
    assert not results[attrname]

    # Clean up
    db.delete_server(f"Sardana/{name}")


def test_load_cmd__wrong_tango_host(sar_demo_json_unique, tmpdir):
    """
    Check that we don't allow applying config to the wrong host.
    """
    name, config_json = sar_demo_json_unique

    yaml = YAML(typ="rt")
    yaml_config = build_sardana_config(config_json, f"MacroServer/{name}/1")

    yaml_config["tango_host"] = "i.am.not.a.real.tango.host:1234567890"
    config_file = tmpdir.join("sar_demo.yaml")
    config_file.write(dump_to_string(yaml, yaml_config))

    with pytest.raises(SystemExit):
        load_cmd(config_file, write=True)


def test_load_cmd__multiple_files(tmpdir):
    """
    Just check that load can handle a split config using !includes.
    TODO add some more useful tests.
    """
    test_dir = os.path.dirname(__file__)
    load_cmd(os.path.join(test_dir, "sar_demo_split.yaml"), write=False,
             current_config={})
