#  SPDX-License-Identifier: Apache-2.0
"""
Python Package for controlling Tesla API.

For more details about this api, please refer to the documentation at
https://github.com/zabuldon/teslajsonpy
"""
import time
from typing import Dict, Optional, Text

from teslajsonpy.vehicle import VehicleDevice


class ChargerSwitch(VehicleDevice):
    """Home-Assistant class for the charger of a Tesla VehicleDevice."""

    def __init__(self, data, controller):
        """Initialize the Charger Switch.

        Parameters
        ----------
        data : dict
            The base state for a Tesla vehicle.
            https://tesla-api.timdorr.com/vehicle/state/chargestate
        controller : teslajsonpy.Controller
            The controller that controls updates to the Tesla API.

        Returns
        -------
        None

        """
        super().__init__(data, controller)
        self.__manual_update_time = 0
        self.__charger_state = None
        self.type = "charger switch"
        self.hass_type = "switch"
        self.name = self._name()
        self.uniq_name = self._uniq_name()
        self.bin_type = 0x8

    async def async_update(self, wake_if_asleep=False, force=False) -> None:
        """Update the charging state of the Tesla Vehicle."""
        await super().async_update(wake_if_asleep=wake_if_asleep)
        last_update = self._controller.get_last_update_time(self._id)
        if last_update >= self.__manual_update_time:
            data = self._controller.get_charging_params(self._id)
            if data and data["charging_state"] != "Charging":
                self.__charger_state = False
            else:
                self.__charger_state = True

    async def start_charge(self):
        """Start charging the Tesla Vehicle."""
        if not self.__charger_state:
            data = await self._controller.command(
                self._id, "charge_start", wake_if_asleep=True
            )
            if data and data["response"]["result"]:
                self.__charger_state = True
            self.__manual_update_time = time.time()

    async def stop_charge(self):
        """Stop charging the Tesla Vehicle."""
        if self.__charger_state:
            data = await self._controller.command(
                self._id, "charge_stop", wake_if_asleep=True
            )
            if data and data["response"]["result"]:
                self.__charger_state = False
            self.__manual_update_time = time.time()

    def is_charging(self):
        """Return whether the Tesla Vehicle is charging."""
        return self.__charger_state

    @staticmethod
    def has_battery():
        """Return whether the Tesla charger has a battery."""
        return False


class RangeSwitch(VehicleDevice):
    """Home-Assistant class for setting range limit for charger."""

    def __init__(self, data, controller):
        """Initialize the charger range switch."""
        super().__init__(data, controller)
        self.__manual_update_time = 0
        self.__maxrange_state = None
        self.type = "maxrange switch"
        self.hass_type = "switch"
        self.name = self._name()
        self.uniq_name = self._uniq_name()
        self.bin_type = 0x9

    async def async_update(self, wake_if_asleep=False, force=False) -> None:
        """Update the status of the range setting."""
        await super().async_update(wake_if_asleep=wake_if_asleep)
        last_update = self._controller.get_last_update_time(self._id)
        if last_update >= self.__manual_update_time:
            data = self._controller.get_charging_params(self._id)
            if data:
                self.__maxrange_state = data["charge_to_max_range"]

    async def set_max(self):
        """Set the charger to max range for trips."""
        if not self.__maxrange_state:
            data = await self._controller.command(
                self._id, "charge_max_range", wake_if_asleep=True
            )
            if data and data["response"]["result"]:
                self.__maxrange_state = True
            self.__manual_update_time = time.time()

    async def set_standard(self):
        """Set the charger to standard range for daily commute."""
        if self.__maxrange_state:
            data = await self._controller.command(
                self._id, "charge_standard", wake_if_asleep=True
            )
            if data and data["response"]["result"]:
                self.__maxrange_state = False
            self.__manual_update_time = time.time()

    def is_maxrange(self):
        """Return whether max range setting is set."""
        return self.__maxrange_state

    @staticmethod
    def has_battery():
        """Return whether the device has a battery."""
        return False


class ChargingSensor(VehicleDevice):
    """Home-Assistant charging sensor class for a Tesla VehicleDevice."""

    def __init__(self, data: Dict, controller) -> None:
        """Initialize the Charger sensor.

        Args:
            data (Dict): The charging parameters for a Tesla vehicle.
            https://tesla-api.timdorr.com/vehicle/state/chargestate
            controller (Controller): The controller that controls updates to the Tesla API.

        """
        super().__init__(data, controller)
        self.type: Text = "charging rate sensor"
        self.__rated: bool = True
        self.measurement: Text = "mi/hr"
        self.hass_type: Text = "sensor"
        self._device_class: Optional[Text] = None
        self.name: Text = self._name()
        self.uniq_name: Text = self._uniq_name()
        self.bin_type: hex = 0xC
        self.__added_range = None
        self.__charge_energy_added = None
        self.__charging_rate = None
        self.__time_to_full = None
        self.__charge_current_request = None
        self.__charger_actual_current = None
        self.__charger_voltage = None

    async def async_update(self, wake_if_asleep=False, force=False) -> None:
        """Update the battery state."""
        await super().async_update(wake_if_asleep=wake_if_asleep)
        data = self._controller.get_gui_params(self._id)
        if data:
            self.measurement = data["gui_distance_units"]
            self.__rated = data["gui_range_display"] == "Rated"
        data = self._controller.get_charging_params(self._id)
        if data:
            self.attrs["charger_phases"] = data["charger_phases"]
            self.__added_range = (
                data["charge_miles_added_rated"]
                if self.__rated
                else data["charge_miles_added_ideal"]
            )
            self.__charge_energy_added = data["charge_energy_added"]
            self.__charging_rate = data["charge_rate"]
            self.__time_to_full = data["time_to_full_charge"]
            self.__charge_current_request = data["charge_current_request"]
            self.__charger_actual_current = data["charger_actual_current"]
            self.__charger_voltage = data["charger_voltage"]
            if self.measurement != "mi/hr":
                self.__added_range = round(self.__added_range / 0.621371, 2)
                self.__charging_rate = round(self.__charging_rate / 0.621371, 2)

    @staticmethod
    def has_battery() -> bool:
        """Return whether the device has a battery."""
        return False

    @property
    def charging_rate(self) -> float:
        """Return the charging rate."""
        return self.__charging_rate

    @property
    def time_left(self) -> float:
        """Return the time left to full in hours."""
        return self.__time_to_full

    @property
    def added_range(self) -> float:
        """Return the added range."""
        return self.__added_range

    @property
    def charge_current_request(self) -> float:
        """Return the requested current."""
        return self.__charge_current_request

    @property
    def charger_actual_current(self) -> float:
        """Return the actual current."""
        return self.__charger_actual_current

    @property
    def charger_voltage(self) -> float:
        """Return the voltage."""
        return self.__charger_voltage

    @property
    def charge_energy_added(self) -> float:
        """Return the energy added."""
        return self.__charge_energy_added

    @property
    def device_class(self) -> Text:
        """Return the HA device class."""
        return self._device_class
