#  SPDX-License-Identifier: Apache-2.0
"""
Python Package for controlling Tesla API.

For more details about this api, please refer to the documentation at
https://github.com/zabuldon/teslajsonpy
"""
from teslajsonpy.connection import Connection
from teslajsonpy.controller import Controller
from teslajsonpy.exceptions import (
    RetryLimitError,
    IncompleteCredentials,
    TeslaException,
    UnknownPresetMode,
    HomelinkError,
)
from teslajsonpy.homeassistant.battery_sensor import Battery, Range
from teslajsonpy.homeassistant.binary_sensor import (
    ChargerConnectionSensor,
    OnlineSensor,
    ParkingSensor,
    UpdateSensor,
)
from teslajsonpy.homeassistant.charger import ChargerSwitch, ChargingSensor, RangeSwitch
from teslajsonpy.homeassistant.climate import Climate, TempSensor
from teslajsonpy.homeassistant.gps import GPS, Odometer
from teslajsonpy.homeassistant.lock import Lock
from teslajsonpy.homeassistant.sentry_mode import SentryModeSwitch
from teslajsonpy.homeassistant.trunk import FrunkCover, TrunkCover
from teslajsonpy.homeassistant.alerts import Horn, FlashLights
from teslajsonpy.homeassistant.homelink import TriggerHomelink
from teslajsonpy.teslaproxy import TeslaProxy
from .__version__ import __version__

__all__ = [
    "Connection",
    "Controller",
    "TeslaProxy",
    "Battery",
    "Range",
    "ChargerConnectionSensor",
    "ChargingSensor",
    "OnlineSensor",
    "ParkingSensor",
    "UpdateSensor",
    "ChargerSwitch",
    "RangeSwitch",
    "Climate",
    "TempSensor",
    "Controller",
    "TeslaException",
    "UnknownPresetMode",
    "HomelinkError",
    "GPS",
    "Odometer",
    "Lock",
    "SentryModeSwitch",
    "Horn",
    "FlashLights",
    "TriggerHomelink",
    "TrunkCover",
    "FrunkCover",
    "__version__",
    "RetryLimitError",
    "IncompleteCredentials",
]
