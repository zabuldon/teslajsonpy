#  SPDX-License-Identifier: Apache-2.0
"""
Python Package for controlling Tesla API.

For more details about this api, please refer to the documentation at
https://github.com/zabuldon/teslajsonpy
"""
import logging

from typing import Optional, Text
from teslajsonpy.homeassistant.vehicle import VehicleDevice

_LOGGER = logging.getLogger(__name__)


class VehicleDataSensor(VehicleDevice):
    """Home-Assistant vehicle data class for a Tesla VehicleDevice."""

    def __init__(self, data: dict, controller) -> None:
        """Initialize the vehicle data sensor.

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
        self.__state: Optional[str] = None

        self.type: Text = "sensor"
        self.hass_type: Text = "sensor"
        # this will be returned to HA as a device_class
        # https://developers.home-assistant.io/docs/core/entity/binary-sensor
        self._sensor_type: Optional[Text] = None
        self.name: Text = self._name()
        self.uniq_name: Text = self._uniq_name()
        self.enabled_by_default = False

    async def async_update(self, wake_if_asleep=False, force=False) -> None:
        """Update the vehicle data."""
        await super().async_update(wake_if_asleep=wake_if_asleep)
        print("Update")
        self.refresh()

    def refresh(self) -> None:
        """Refresh data.

        This assumes the controller has already been updated
        """
        super().refresh()
        print("Refresh")
        self.__state = self.vin()

    def get_value(self) -> Optional[str]:
        """Return the state."""
        return self.__state

    @classmethod
    def _dict_to_attr(
        cls,
        data: dict,
        exclude_dicts: Optional[list[str]] = None,
        prepend: Optional[str] = None,
    ) -> dict:
        """Convert Tesla returned dict into dict for attributes"""
        prepend = prepend or ""
        exclude_dicts = exclude_dicts or []

        attr: dict = {}
        for key, value in data.items():
            prepend_key = f"{key}" if prepend == "" else f"{prepend}_{key}"
            if isinstance(value, dict):
                if key in exclude_dicts or "*" in exclude_dicts:
                    continue
                attr.update(cls._dict_to_attr(value, exclude_dicts, prepend_key))
            else:

                attr[prepend_key] = value

        return attr


class ClimateStateDataSensor(VehicleDataSensor):
    """Home-Assistant Climate State sensor class for a Tesla VehicleDevice."""

    def __init__(self, data: dict, controller) -> None:
        """Initialize the ClimateStateData sensor.

        Args:
            data (Dict): The base state for a Tesla vehicle.
                https://tesla-api.timdorr.com/vehicle/state/data
            controller (Controller): The controller that controls updates to the Tesla API.

        """
        super().__init__(data, controller)

        self.type: Text = "climate state data sensor"

    def refresh(self) -> None:
        """Refresh data.

        This assumes the controller has already been updated
        """
        super().refresh()

        self.attrs = self._dict_to_attr(self._controller.get_climate_params(self._id))


class ChargeStateDataSensor(VehicleDataSensor):
    """Home-Assistant Charge State sensor class for a Tesla VehicleDevice."""

    def __init__(self, data: dict, controller) -> None:
        """Initialize the ChargeStateData sensor.

        Args:
            data (Dict): The base state for a Tesla vehicle.
                https://tesla-api.timdorr.com/vehicle/state/data
            controller (Controller): The controller that controls updates to the Tesla API.

        """
        super().__init__(data, controller)

        self.type: Text = "charging state data sensor"

    def refresh(self) -> None:
        """Refresh data.

        This assumes the controller has already been updated
        """
        super().refresh()
        self.attrs = self._dict_to_attr(self._controller.get_charging_params(self._id))


class VehicleStateDataSensor(VehicleDataSensor):
    """Home-Assistant Vehicle State sensor class for a Tesla VehicleDevice."""

    def __init__(self, data: dict, controller) -> None:
        """Initialize the VehicleStateData sensor.

        Args:
            data (Dict): The base state for a Tesla vehicle.
                https://tesla-api.timdorr.com/vehicle/state/data
            controller (Controller): The controller that controls updates to the Tesla API.

        """
        super().__init__(data, controller)

        self.type: Text = "vehicle state data sensor"

    def refresh(self) -> None:
        """Refresh data.

        This assumes the controller has already been updated
        """
        super().refresh()
        self.attrs = self._dict_to_attr(
            self._controller.get_state_params(self._id),
            ["software_update", "speed_limit_mode"],
        )


class SoftwareDataSensor(VehicleDataSensor):
    """Home-Assistant Software sensor class for a Tesla VehicleDevice."""

    def __init__(self, data: dict, controller) -> None:
        """Initialize the SoftwareData sensor.

        Args:
            data (Dict): The base state for a Tesla vehicle.
                https://tesla-api.timdorr.com/vehicle/state/data
            controller (Controller): The controller that controls updates to the Tesla API.

        """
        super().__init__(data, controller)

        self.type: Text = "software data sensor"

    def refresh(self) -> None:
        """Refresh data.

        This assumes the controller has already been updated
        """
        super().refresh()
        self.attrs = self._dict_to_attr(
            self._controller.get_state_params(self._id).get("software_update", {})
        )


class SpeedLimitDataSensor(VehicleDataSensor):
    """Home-Assistant Speed Limit sensor class for a Tesla VehicleDevice."""

    def __init__(self, data: dict, controller) -> None:
        """Initialize the SpeedLimitData sensor.

        Args:
            data (Dict): The base state for a Tesla vehicle.
                https://tesla-api.timdorr.com/vehicle/state/data
            controller (Controller): The controller that controls updates to the Tesla API.

        """
        super().__init__(data, controller)

        self.type: Text = "speed limit data sensor"

    def refresh(self) -> None:
        """Refresh data.

        This assumes the controller has already been updated
        """
        super().refresh()
        self.attrs = self._dict_to_attr(
            self._controller.get_state_params(self._id).get("speed_limit_mode", {})
        )


class VehicleConfigDataSensor(VehicleDataSensor):
    """Home-Assistant Vehicle Config sensor class for a Tesla VehicleDevice."""

    def __init__(self, data: dict, controller) -> None:
        """Initialize the VehicleConfigData sensor.

        Args:
            data (Dict): The base state for a Tesla vehicle.
                https://tesla-api.timdorr.com/vehicle/state/data
            controller (Controller): The controller that controls updates to the Tesla API.

        """
        super().__init__(data, controller)

        self.type: Text = "vehicle config data sensor"

    def refresh(self) -> None:
        """Refresh data.

        This assumes the controller has already been updated
        """
        super().refresh()
        self.attrs = self._dict_to_attr(self._controller.get_config_params(self._id))


class DriveStateDataSensor(VehicleDataSensor):
    """Home-Assistant Drive State sensor class for a Tesla VehicleDevice."""

    def __init__(self, data: dict, controller) -> None:
        """Initialize the DriveStateData sensor.

        Args:
            data (Dict): The base state for a Tesla vehicle.
                https://tesla-api.timdorr.com/vehicle/state/data
            controller (Controller): The controller that controls updates to the Tesla API.

        """
        super().__init__(data, controller)

        self.type: Text = "drive state data sensor"

    def refresh(self) -> None:
        """Refresh data.

        This assumes the controller has already been updated
        """
        super().refresh()
        self.attrs = self._dict_to_attr(self._controller.get_drive_params(self._id))


class GuiSettingsDataSensor(VehicleDataSensor):
    """Home-Assistant GUI settings sensor class for a Tesla VehicleDevice."""

    def __init__(self, data: dict, controller) -> None:
        """Initialize the GuiSettingsData sensor.

        Args:
            data (Dict): The base state for a Tesla vehicle.
                https://tesla-api.timdorr.com/vehicle/state/data
            controller (Controller): The controller that controls updates to the Tesla API.

        """
        super().__init__(data, controller)

        self.type: Text = "gui settings data sensor"

    def refresh(self) -> None:
        """Refresh data.

        This assumes the controller has already been updated
        """
        super().refresh()
        self.attrs = self._dict_to_attr(self._controller.get_gui_params(self._id))
