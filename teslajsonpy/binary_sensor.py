#  SPDX-License-Identifier: Apache-2.0
"""
Python Package for controlling Tesla API.

For more details about this api, please refer to the documentation at
https://github.com/zabuldon/teslajsonpy
"""
from typing import Dict, Text

from teslajsonpy.vehicle import VehicleDevice


class ParkingSensor(VehicleDevice):
    """Home-assistant parking brake class for Tesla vehicles.

    This is intended to be partially inherited by a Home-Assitant entity.
    """

    def __init__(self, data: Dict, controller):
        """Initialize the parking brake sensor.

        Parameters
        ----------
        data : dict
            The base state for a Tesla vehicle.
            https://tesla-api.timdorr.com/vehicle/state/data
        controller : teslajsonpy.Controller
            The controller that controls updates to the Tesla API.

        Returns
        -------
        None

        """
        super().__init__(data, controller)
        self.__state = False

        self.type = "parking brake sensor"
        self.hass_type = "binary_sensor"
        self.sensor_type = "power"

        self.name = self._name()

        self.uniq_name = self._uniq_name()
        self.bin_type = 0x1

    async def async_update(self):
        """Update the parking brake sensor."""
        await super().async_update()
        data = self._controller.get_drive_params(self._id)
        if data:
            self.attrs["shift_state"] = (
                data["shift_state"] if data["shift_state"] else "P"
            )
            if not data["shift_state"] or data["shift_state"] == "P":
                self.__state = True
            else:
                self.__state = False

    def get_value(self):
        """Return whether parking brake engaged."""
        return self.__state

    @staticmethod
    def has_battery():
        """Return whether the device has a battery."""
        return False


class ChargerConnectionSensor(VehicleDevice):
    """Home-assistant charger connection class for Tesla vehicles.

    This is intended to be partially inherited by a Home-Assitant entity.
    """

    def __init__(self, data, controller):
        """Initialize the charger cable connection sensor.

        Parameters
        ----------
        data : dict
            The base state for a Tesla vehicle.
            https://tesla-api.timdorr.com/vehicle/state/data
        controller : teslajsonpy.Controller
            The controller that controls updates to the Tesla API.

        Returns
        -------
        None

        """
        super().__init__(data, controller)
        self.__state = False

        self.type = "charger sensor"
        self.hass_type = "binary_sensor"
        self.name = self._name()
        self.sensor_type = "connectivity"

        self.uniq_name = self._uniq_name()
        self.bin_type = 0x2

    async def async_update(self):
        """Update the charger connection sensor."""
        await super().async_update()
        data = self._controller.get_charging_params(self._id)
        if data:
            self.attrs["charging_state"] = data["charging_state"]
            self.attrs["conn_charge_cable"] = data["conn_charge_cable"]
            self.attrs["fast_charger_present"] = data["fast_charger_present"]
            self.attrs["fast_charger_brand"] = data["fast_charger_brand"]
            self.attrs["fast_charger_type"] = data["fast_charger_type"]
            if data["charging_state"] in ["Disconnected"]:
                self.__state = False
            else:
                self.__state = True

    def get_value(self):
        """Return whether the charger cable is connected."""
        return self.__state

    @staticmethod
    def has_battery():
        """Return whether the device has a battery."""
        return False


class OnlineSensor(VehicleDevice):
    """Home-Assistant Online sensor class for a Tesla VehicleDevice."""

    def __init__(self, data: Dict, controller) -> None:
        """Initialize the Online sensor.

        Args:
            data (Dict): The base state for a Tesla vehicle.
                https://tesla-api.timdorr.com/vehicle/state/data
            controller (Controller): The controller that controls updates to the Tesla API.

        """
        super().__init__(data, controller)
        self.__online_state: bool = None
        self.type: Text = "online sensor"
        self.hass_type = "binary_sensor"
        self.name: Text = self._name()
        self.uniq_name: Text = self._uniq_name()

    async def async_update(self) -> None:
        """Update the battery state."""
        await super().async_update()
        self.__online_state = self._controller.car_online[self._vin]
        self.attrs["state"] = self._controller.car_state[self._vin].get("state")

    @staticmethod
    def has_battery() -> bool:
        """Return whether the device has a battery."""
        return False

    def get_value(self) -> bool:
        """Return the battery level."""
        return self.__online_state
