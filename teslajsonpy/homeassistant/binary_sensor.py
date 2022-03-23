#  SPDX-License-Identifier: Apache-2.0
"""
Python Package for controlling Tesla API.

For more details about this api, please refer to the documentation at
https://github.com/zabuldon/teslajsonpy
"""
from json import dumps
from typing import Dict, Optional, Text

from teslajsonpy.const import RELEASE_NOTES_URL
from teslajsonpy.homeassistant.vehicle import VehicleDevice


class BinarySensor(VehicleDevice):
    """Home-assistant binary sensor class for Tesla vehicles.

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
        self.__state: Optional[bool] = None

        self.type: Text = "binary sensor"
        self.hass_type: Text = "binary_sensor"
        # this will be returned to HA as a device_class
        # https://developers.home-assistant.io/docs/core/entity/binary-sensor
        self._sensor_type: Optional[Text] = None
        self.name: Text = self._name()
        self.uniq_name: Text = self._uniq_name()

    async def async_update(self, wake_if_asleep=False, force=False) -> None:
        """Update the binary sensor."""
        await super().async_update(wake_if_asleep=wake_if_asleep)

    def get_value(self) -> Optional[bool]:
        """Return whether binary sensor is true."""
        return self.__state

    @property
    def sensor_type(self) -> Optional[Text]:
        """Return the sensor_type for use by HA as a device_class."""
        return self._sensor_type

    @staticmethod
    def has_battery() -> bool:
        """Return whether the device has a battery."""
        return False


class ParkingSensor(BinarySensor):
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
        self.__state: Optional[bool] = None
        self.type: Text = "parking brake sensor"
        self.hass_type: Text = "binary_sensor"
        self._sensor_type: Optional[Text] = None
        self.name: Text = self._name()
        self.uniq_name: Text = self._uniq_name()

    async def async_update(self, wake_if_asleep=False, force=False) -> None:
        """Update the parking brake sensor."""
        await super().async_update(wake_if_asleep=wake_if_asleep)
        self.refresh()

    def refresh(self) -> None:
        """Refresh data.

        This assumes the controller has already been updated
        """
        super().refresh()
        data = self._controller.get_drive_params(self._id)
        if data:
            self.attrs["shift_state"] = (
                data["shift_state"] if data["shift_state"] else "P"
            )
            if not data["shift_state"] or data["shift_state"] == "P":
                self.__state = True
            else:
                self.__state = False

    def get_value(self) -> Optional[bool]:
        """Return whether parking brake engaged."""
        return self.__state


class ChargerConnectionSensor(BinarySensor):
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
        self.__state: Optional[bool] = None
        self.type: Text = "charger sensor"
        self.hass_type: Text = "binary_sensor"
        self._sensor_type: Optional[Text] = None
        self.name: Text = self._name()
        self.uniq_name: Text = self._uniq_name()

    async def async_update(self, wake_if_asleep=False, force=False) -> None:
        """Update the charger connection sensor."""
        await super().async_update(wake_if_asleep=wake_if_asleep)
        self.refresh()

    def refresh(self) -> None:
        """Refresh data.

        This assumes the controller has already been updated
        """
        super().refresh()
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

    def get_value(self) -> Optional[bool]:
        """Return whether the charger cable is connected."""
        return self.__state


class OnlineSensor(BinarySensor):
    """Home-Assistant Online sensor class for a Tesla VehicleDevice."""

    def __init__(self, data: Dict, controller) -> None:
        """Initialize the Online sensor.

        Args:
            data (Dict): The base state for a Tesla vehicle.
                https://tesla-api.timdorr.com/vehicle/state/data
            controller (Controller): The controller that controls updates to the Tesla API.

        """
        super().__init__(data, controller)
        self.__online_state: Optional[bool] = None
        self.type: Text = "online sensor"
        self.hass_type: Text = "binary_sensor"
        self._sensor_type: Optional[Text] = "connectivity"
        self.name: Text = self._name()
        self.uniq_name: Text = self._uniq_name()

    async def async_update(self, wake_if_asleep=False, force=False) -> None:
        """Update the battery state."""
        await super().async_update(wake_if_asleep=wake_if_asleep)
        self.refresh()

    def refresh(self) -> None:
        """Refresh data.

        This assumes the controller has already been updated
        """
        super().refresh()
        self.__online_state = self._controller.car_online[self._vin]
        self.attrs["state"] = self._controller.car_state[self._vin].get("state")
        self.attrs["vehicle_id"] = self.vehicle_id()
        self.attrs["vin"] = self.vin()
        self.attrs["id"] = self.id()
        self.attrs["update_interval"] = self._controller.get_update_interval_vin(vin=self._vin)
        vehicle_data = {
            "climate_state": self._controller.get_climate_params(self._id),
            "charge_state": self._controller.get_charging_params(self._id),
            "vehicle_state": self._controller.get_state_params(self._id),
            "vehicle_config": self._controller.get_config_params(self._id),
            "drive_state": self._controller.get_drive_params(self._id),
            "gui_settings": self._controller.get_gui_params(self._id)
        }
        self.attrs["vehicle_data"] = dumps(vehicle_data)

    def get_value(self) -> Optional[bool]:
        """Return the car is online."""
        return self.__online_state


class UpdateSensor(BinarySensor):
    """Home-Assistant update sensor class for a Tesla VehicleDevice."""

    def __init__(self, data: Dict, controller) -> None:
        """Initialize the Update sensor.

        Args:
            data (Dict): Thes base state for a Tesla vehicle.
                https://tesla-api.timdorr.com/vehicle/state/data
            controller (Controller): The controller that controls updates to the Tesla API.

        """
        super().__init__(data, controller)
        self.type: Text = "update available sensor"
        self._sensor_type: Optional[Text] = None
        self.name: Text = self._name()
        self.uniq_name: Text = self._uniq_name()

    async def async_update(self, wake_if_asleep=False, force=False) -> None:
        """Update the battery state."""
        await super().async_update(wake_if_asleep=wake_if_asleep)
        self.refresh()

    def refresh(self) -> None:
        """Refresh data.

        This assumes the controller has already been updated
        """
        super().refresh()
        self.attrs = (
            self.device_state_attributes.copy() if self.device_state_attributes else {}
        )

    def get_value(self) -> Optional[bool]:
        """Return the car is online."""
        return self.update_available

    @property
    def device_state_attributes(self) -> Optional[dict]:
        """Return the optional state attributes."""
        if not self.car_version:
            return None
        data = {}
        data["installed_version"] = self.car_version
        if self.update_available:
            data["release_notes"] = f"{RELEASE_NOTES_URL}{self.update_version}"
            data["update_version"] = self.update_version
        return data
