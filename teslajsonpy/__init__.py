#  SPDX-License-Identifier: Apache-2.0
"""
Python Package for controlling Tesla API.

For more details about this api, please refer to the documentation at
https://github.com/zabuldon/teslajsonpy
"""
from teslajsonpy.battery_sensor import Battery, Range
from teslajsonpy.binary_sensor import (
    ChargerConnectionSensor,
    OnlineSensor,
    ParkingSensor,
)
from teslajsonpy.charger import ChargerSwitch, ChargingSensor, RangeSwitch
from teslajsonpy.climate import Climate, TempSensor
from teslajsonpy.controller import Controller
from teslajsonpy.exceptions import TeslaException
from teslajsonpy.gps import GPS, Odometer
from teslajsonpy.lock import Lock
from teslajsonpy.sentry_mode import SentryModeSwitch
from teslajsonpy.trunk import TrunkSensor, FrunkSensor, TrunkSwitch

from .__version__ import __version__

__all__ = [
    "Battery",
    "Range",
    "ChargerConnectionSensor",
    "ChargingSensor",
    "OnlineSensor",
    "ParkingSensor",
    "ChargerSwitch",
    "RangeSwitch",
    "Climate",
    "TempSensor",
    "Controller",
    "TeslaException",
    "GPS",
    "Odometer",
    "Lock",
    "SentryModeSwitch",
    "TrunkSensor",
    "FrunkSensor",
    "TrunkSwitch",
    "__version__",
]
