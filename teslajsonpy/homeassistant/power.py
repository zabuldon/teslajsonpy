"""
Python Package for controlling Tesla API.

For more details about this api, please refer to the documentation at
https://github.com/zabuldon/teslajsonpy
"""
import logging
from typing import Dict, Text

from teslajsonpy.const import TESLA_DEFAULT_ENERGY_SITE_NAME

_LOGGER = logging.getLogger(__name__)


class EnergySiteDevice:
    """Home-assistant class of Tesla Energy Sites.

    This is intended to be partially inherited by a Home-Assitant entity.
    """

    def __init__(self, data, controller):
        """Initialize the Energy Site.

        Parameters
        ----------
        data : dict
            The base state for a Tesla Energy Site.
            https://www.teslaapi.io/energy-sites/state-and-settings
        controller : teslajsonpy.Controller
            The controller that controls updates to the Tesla API.

        Returns
        -------
        None

        """
        self._id: int = data["id"]
        self._energy_site_id: int = data["energy_site_id"]
        self._site_name: Text = data.get("site_name", TESLA_DEFAULT_ENERGY_SITE_NAME)
        self._controller = controller
        self.should_poll: bool = True
        self.type: Text = "device"
        self.attrs: Dict[Text, Text] = {}
        self.enabled_by_default: bool = True

    def _name(self) -> Text:
        return f"{self._site_name} {self.type}"

    def _uniq_name(self) -> Text:
        return f"{self._energy_site_id} {self.type}"

    def id(self) -> int:
        # pylint: disable=invalid-name
        """Return the id."""
        return self._id

    def energy_site_id(self) -> int:
        """Return the energy_site_id."""
        return self._energy_site_id

    def site_name(self) -> Text:
        """Return the site name."""
        return self._site_name

    async def async_update(
        self, wake_if_asleep: bool = False, force: bool = False
    ) -> None:
        """Update the energy site data.

        This function will call a controller update.
        """
        await self._controller.update(
            self.id(), wake_if_asleep=wake_if_asleep, force=force
        )
        self.refresh()

    # pylint: disable=no-self-use
    def refresh(self) -> None:
        """Refresh the energy site data.

        This assumes the controller has already been updated. This should be
        called by inherited classes so the overall vehicle information is updated.
        """
        return


class PowerSensor(EnergySiteDevice):
    """Home-assistant class of power sensors for Tesla Energy Sites (Solar Panels).

    This is intended to be partially inherited by a Home-Assitant entity.
    """

    def __init__(self, data, controller):
        """Initialize the power sensor and track in Watt for an Energy Site.

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
        self.measurement = "W"
        self.hass_type = "sensor"
        self._device_class: Text = "power"
        self._state_class: Text = "measurement"
        self.bin_type = 0x4

    async def async_update(self, wake_if_asleep=False, force=False) -> None:
        """Update the site info."""
        await super().async_update(wake_if_asleep=wake_if_asleep)
        self.refresh()

    @property
    def device_class(self) -> Text:
        """Return the HA device class."""
        return self._device_class

    @property
    def state_class(self) -> Text:
        """Return the HA state class."""
        return self._state_class


class SolarPowerSensor(PowerSensor):
    """Home-assistant class of power sensors for Tesla Energy Sites (Solar Panels).

    This is intended to be partially inherited by a Home-Assitant entity.
    """

    def __init__(self, data, controller):
        """Initialize the solar panel sensor."""
        super().__init__(data, controller)
        self._solar_type: Text = data["solar_type"]
        self.__solar_power: float = data["solar_power"]
        self.__generating_status: bool = None
        self.__grid_status: dict = controller._grid_status[self._energy_site_id]
        self.type = "solar panel"
        self.name = self._name()
        self.uniq_name = self._uniq_name()

    def get_value(self) -> float:
        """Return solar power."""
        return self.__solar_power

    def get_power(self):
        """Get solar power."""
        return self.__solar_power

    def get_generating_status(self):
        """Get generating status."""
        return self.__generating_status

    @property
    def solar_type(self) -> Text:
        """Return the solar type."""
        return self._solar_type

    def refresh(self) -> None:
        """Refresh data.

        This assumes the controller has already been updated
        """
        super().refresh()
        data = self._controller.get_power_params(self._id)

        if data:
            # Note: Some systems that pre-date Tesla aquisition of SolarCity will have `grid_status: Unknown`,
            # but will have solar power values. At the same time, newer systems will report spurious reads of 0 Watts
            # and grid status unknown. If solar power is 0 return null.
            if not self.__grid_status["grid_always_unk"] and (
                data["grid_status"] == "Unknown" and data["solar_power"] == 0
            ):
                _LOGGER.debug("Spurious energy site power read")
                return

            self.__solar_power = data["solar_power"]

            if data["solar_power"] is not None:
                self.__generating_status = (
                    "Generating" if data["solar_power"] > 0 else "Idle"
                )


class LoadPowerSensor(PowerSensor):
    """Home-assistant class for load power sensors for Tesla Energy Sites (Solar Panels).

    This is intended to be partially inherited by a Home-Assitant entity.
    """

    def __init__(self, data, controller):
        """Initialize the load power sensor."""
        super().__init__(data, controller)
        self.__load_power: float = data["load_power"]
        self.type = "load power"
        self.name = self._name()
        self.uniq_name = self._uniq_name()

    def get_value(self) -> float:
        """Return load power."""
        return self.__load_power

    def get_load_power(self):
        """Get load power (home consumption)."""
        return self.__load_power

    def refresh(self) -> None:
        """Refresh data.

        This assumes the controller has already been updated
        """
        super().refresh()
        data = self._controller.get_power_params(self._id)

        if data:
            self.__load_power = data["load_power"]


class GridPowerSensor(PowerSensor):
    """Home-assistant class for grid power sensors for Tesla Energy Sites (Solar Panels).

    This is intended to be partially inherited by a Home-Assitant entity.
    """

    def __init__(self, data, controller):
        """Initialize the grid power sensor."""
        super().__init__(data, controller)
        self.__grid_power: float = data["grid_power"]
        self.type = "grid power"
        self.name = self._name()
        self.uniq_name = self._uniq_name()

    def get_value(self) -> float:
        """Return grid power."""
        return self.__grid_power

    def get_grid_power(self):
        """Get grid power (grid import/export)."""
        return self.__grid_power

    def refresh(self) -> None:
        """Refresh data.

        This assumes the controller has already been updated
        """
        super().refresh()
        data = self._controller.get_power_params(self._id)

        if data:
            self.__grid_power = data["grid_power"]
