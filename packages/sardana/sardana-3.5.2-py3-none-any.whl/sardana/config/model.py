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

import pathlib
from typing import Dict, List, Tuple, Optional, Union, Sequence
from typing_extensions import Annotated, Literal
import re

from pydantic import BaseModel, Field, NegativeFloat, PositiveFloat, validator

from .common import (TANGO_HOST_REGEX, SARDANA_NAME_REGEX, FULL_DEVICE_NAME_REGEX,
                     FULL_ATTRIBUTE_NAME_REGEX)


class StrictBaseModel(BaseModel):
    """
    Base model that allows no members that aren't defined in the model
    This is intended to prevent e.g. typos, and there's no point in
    allowing things that we're not going to use anyway.

    Further, we don't allow putting 'None' values for optional fields,
    in general. This is mainly because it will cause needless diffs
    when "roundtripping" the config, as the empty fields will not be
    persisted in the DB.  So, if there's no value for an optional
    field, just leave it out.
    """
    class Config:
        extra = "forbid"

    @validator("*")
    def validate_field_not_none(cls, value):
        if value is None:
            raise ValueError("Field may not be None. Instead, remove the field.")
        return value


class Name(str):

    """
    Custom string class for Sardana names.
    Validates that they are correctly formed.
    """

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not isinstance(v, str):
            raise TypeError("Name must be a string")
        if not re.match(SARDANA_NAME_REGEX, v):
            raise ValueError(f"Bad name '{v}'; must be compatible with Tango aliases.")
        return v


class InstrumentName(str):

    """
    Custom string class for Sardana instrument names.
    """

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        # Not sure if instrument names should be restricted
        # For some reason they often contain a / at least.
        if not isinstance(v, str):
            raise TypeError("Instrument name must be a string")
        return v


class PythonModule(str):

    """
    Custom string class for Sardana names.
    Validates that they are correctly formed.
    """

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not isinstance(v, str):
            raise TypeError("Python module must be a string")
        if not v.endswith(".py"):
            raise ValueError("Python module must be a python file, name ending with '.py'.")
        return v


class DeviceName(str):

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not isinstance(v, str):
            raise TypeError("Device name must be a string")
        if not len(v.split("/")) == 3:
            raise ValueError("Bad device name '{v}': should have form 'domain/family/member'")
        return v


class ServerName(str):

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not isinstance(v, str):
            raise TypeError("Server name must be a string")
        if not 1 <= len(v.split("/")) <= 2:
            raise ValueError("Bad server name '{v}': should have form 'server/instance' or just server")
        return v


class TangoHost(str):

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not isinstance(v, str):
            raise TypeError("Tango host must be a string")
        if not re.match(TANGO_HOST_REGEX, v):
            raise ValueError(f"Bad Tango host {v}: should be <hostname>:<port>")
        return v


class FullDeviceName(str):

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not re.match(FULL_DEVICE_NAME_REGEX, v):
            raise ValueError(f"Bad full device name '{v}': should be tango://<hostname>:<port>/<device>")
        return v


class FullAttributeName(str):

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not re.match(FULL_ATTRIBUTE_NAME_REGEX, v):
            raise ValueError(f"Bad full attribute name '{v}': should be tango://<hostname>:<port>/<device>/<attribute>")
        return v


# ==== Pool ====

class Instrument(StrictBaseModel):
    "An instrument is a collection of elements"
    cls: str = Field(alias="class")


AttributeValue = Union[int, float, bool, str, list]  # TODO too restrictive?
Change = Union[PositiveFloat, Tuple[NegativeFloat, PositiveFloat]]


class AttributeConfig(StrictBaseModel):
    "Tango attribute value and settings"
    value: Optional[Union[AttributeValue, dict]]
    label: Optional[str]
    description: Optional[str]
    format: Optional[str]
    unit: Optional[str]
    polling_period: Optional[int]
    abs_change: Optional[Change]
    rel_change: Optional[Change]
    event_period: Optional[int]
    archive_abs_change: Optional[Change]
    archive_rel_change: Optional[Change]
    archive_period: Optional[int]
    min_value: Optional[float]
    max_value: Optional[float]
    min_alarm: Optional[float]
    max_alarm: Optional[float]


def get_attributes_validator(fieldname="attributes"):
    # This could also be accomplished by pure typing, using a union of
    # AttributeConfig and AttributeValue. However that leads to pretty
    # unelpful error messages, where *all* the possible types are listed.
    def validate_attribute(cls, value):
        # We allow attributes to be either a configuration dict...
        if isinstance(value, dict):
            return value
        # ... or just an attribute value (at this point we don't know the type)
        if value is not None:
            return dict(value=value)

    return validator(fieldname, pre=True, each_item=True, allow_reuse=True)(validate_attribute)


class Element(StrictBaseModel):
    """
    A single sardana element.
    """
    axis: int
    description: Optional[str]
    attributes: Optional[Dict[str, AttributeConfig]]
    properties: Optional[Dict[str, AttributeValue]]
    instrument: Optional[InstrumentName]
    tango_device: Optional[DeviceName]
    drift_correction: Optional[bool]

    _attributes_validator = get_attributes_validator()


class BaseController(StrictBaseModel):
    "A controller"
    description: Optional[str]
    python_module: PythonModule
    python_class: str
    tango_device: Optional[DeviceName]
    elements: Optional[Dict[Name, Element]]
    attributes: Optional[Dict[str, AttributeConfig]]
    properties: Optional[Dict[str, AttributeValue]]

    _attributes_validator = get_attributes_validator()


# TODO would be nice if we could get controller types from sardana itself..?
class MotorController(BaseController):
    "A motor controller"
    type: Literal["Motor"]


class CTExpChannelController(BaseController):
    "Counter Experimental Channel"
    type: Literal["CTExpChannel"]


class ZeroDExpChannelController(BaseController):
    "Zero Dimensional (scalar) experimental channel"
    type: Literal["ZeroDExpChannel"]


class OneDExpChannelController(BaseController):
    "One dimensional (array) experimental channel"
    type: Literal["OneDExpChannel"]


class TwoDExpChannelController(BaseController):
    "Two dimensional (image) experimental channel"
    type: Literal["TwoDExpChannel"]


class IORegisterController(BaseController):
    "IO register"
    type: Literal["IORegister"]


class TriggerGateController(BaseController):
    "Trigger gate controller"
    type: Literal["TriggerGate"]


class PseudoMotorController(BaseController):
    "Pseudo motor controller"
    type: Literal["PseudoMotor"]
    physical_roles: Dict[str, Name]


class PseudoCounterController(BaseController):
    "Pseudo counter controller"
    type: Literal["PseudoCounter"]
    physical_roles: Optional[Dict[str, Name]]


Controller = Annotated[
    Union[
        MotorController, CTExpChannelController,
        ZeroDExpChannelController, OneDExpChannelController, TwoDExpChannelController,
        PseudoMotorController, PseudoCounterController,
        TriggerGateController, IORegisterController
    ],
    Field(discriminator="type")
]


class MeasurementGroupChannel(StrictBaseModel):
    """Configuration for a measurement group channel"""
    enabled: Optional[bool]
    synchronization: Optional[str]  # TODO enum?
    synchronizer: Optional[Union[Name, DeviceName, FullDeviceName]]
    timer: Optional[Union[Name, DeviceName, FullDeviceName]]
    monitor: Optional[Union[Name, DeviceName, FullDeviceName]]
    output: Optional[bool]
    data_type: Optional[str]  # TODO check valid tango type?
    data_units: Optional[str]
    nexus_path: Optional[pathlib.Path]
    plot_type: Optional[int]  # TODO PlotType
    plot_axes: Optional[List[str]]  # TODO <mov>, <idx> or valid name


class MeasurementGroup(StrictBaseModel):
    "A measurement group"
    label: Optional[str]
    description: Optional[str]
    channels: List[Union[str, Dict[str, MeasurementGroupChannel]]]

    @validator("channels", each_item=True, pre=True)
    def check_channels(cls, c):
        if isinstance(c, dict):
            if len(c) > 1:
                raise ValueError(f"Expected one key (channel name), got {list(c.keys())}")
        return c


class Pool(StrictBaseModel):
    "The pool handles interfacing with hardware and the control system"
    description: Optional[str]
    tango_alias: Optional[Name]
    tango_device: Optional[DeviceName]
    tango_server: Optional[ServerName]
    pool_path: Optional[Sequence[pathlib.Path]]
    python_path: Optional[Sequence[pathlib.Path]]
    motionloop_sleep_time: Optional[int]
    motionloop_states_per_position: Optional[int]
    acqloop_sleep_time: Optional[int]
    acqloop_states_per_value: Optional[int]
    remote_log: Optional[str]
    drift_correction: Optional[bool]
    properties: Optional[Dict[str, AttributeValue]]

    instruments: Optional[Dict[InstrumentName, Instrument]]
    controllers: Optional[Dict[Name, Controller]]
    measurement_groups: Optional[Dict[Name, MeasurementGroup]]


# ==== MacroServer ====

class Door(StrictBaseModel):
    description: Optional[str]
    tango_device: str


class Environment(StrictBaseModel):
    "Environment"
    # TODO
    path: Optional[pathlib.Path]
    variables: Optional[Dict[str, str]]


class MacroServer(StrictBaseModel):
    "The MacroServer runs macros, and generally runs the show"
    description: Optional[str]
    tango_alias: Optional[Name]
    tango_device: Optional[DeviceName]
    tango_server: Optional[ServerName]
    macro_path: Optional[Sequence[pathlib.Path]]
    recorder_path: Optional[Sequence[pathlib.Path]]
    python_path: Optional[Sequence[pathlib.Path]]
    environment_db: Optional[str]
    environment: Optional[Environment]
    max_parallel_macros: Optional[int]
    log_report_filename: Optional[str]
    log_report_format: Optional[str]
    properties: Optional[Dict[str, AttributeValue]]

    doors: Dict[Name, Door]
    pools: Optional[Sequence[Union[Name, FullDeviceName]]]


# ==== Everything ====

class Configuration(StrictBaseModel):
    "Collects all of the configuration for a Sardana installation"
    tango_host: Optional[TangoHost]
    pools: Optional[Dict[Name, Pool]]
    macro_servers: Dict[Name, MacroServer]

    @validator("macro_servers")
    def validate_macro_servers(cls, value):
        if len(value) != 1:
            raise ValueError("Config currently only supports exactly one MacroServer")
        return value


if __name__ == "__main__":
    print(Configuration.schema_json(indent=4))
