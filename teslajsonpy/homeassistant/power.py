"""
Python Package for controlling Tesla API.

For more details about this api, please refer to the documentation at
https://github.com/zabuldon/teslajsonpy
"""
import logging
from typing import Dict, Text

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
        self._site_name: Text = data.get("site_name", f"{self._energy_site_id}")
        self._solar_type: Text = data["solar_type"]
        self._controller = controller
        self.should_poll: bool = True
        self.type: Text = "device"
        self.attrs: Dict[Text, Text] = {}

    def _name(self) -> Text:
        return f"{self._site_name} {self.type}"

    def _uniq_name(self) -> Text:
        return self._name()

    def id(self) -> int:
        # pylint: disable=invalid-name
        """Return the id of this Vehicle."""
        return self._id

    def energy_site_id(self) -> int:
        """Return the vehicle_id of this Vehicle."""
        return self._energy_site_id

    def site_name(self) -> Text:
        """Return the car name of this Vehicle."""
        return self._site_name

    @property
    def solar_type(self) -> Text:
        """Return the type of this Vehicle."""
        return self._solar_type

    async def async_update(
        self, wake_if_asleep: bool = False, force: bool = False
    ) -> None:
        """Update the vehicle data.

        This function will call a controller update.
        """
        await self._controller.update(
            self.id(), wake_if_asleep=wake_if_asleep, force=force
        )
        self.refresh()

    # pylint: disable=no-self-use
    def refresh(self) -> None:
        """Refresh the vehicle data.

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
        self.__power: float = data["solar_power"]
        self.__generating_status: bool = None
        self.type = "solar panel"
        self.measurement = "W"
        self.hass_type = "sensor"
        self._device_class: Text = "power"
        self._state_class: Text = "measurement"
        self.name = self._name()
        self.uniq_name = self._uniq_name()
        self.bin_type = 0x4

    async def async_update(self, wake_if_asleep=False, force=False) -> None:
        """Update the temperature."""
        await super().async_update(wake_if_asleep=wake_if_asleep)
        self.refresh()

    def refresh(self) -> None:
        """Refresh data.

        This assumes the controller has already been updated
        """
        super().refresh()
        data = self._controller.get_power_params(self._id)
        if data:
            if "grid_status" in data and data["grid_status"] == "Unknown":
                return

            self.__power = data["solar_power"]
            if data["solar_power"] is not None:
                self.__generating_status = (
                    "Generating" if data["solar_power"] > 0 else "Idle"
                )

    def get_value(self) -> float:
        """Return the battery level."""
        return self.__power

    def get_power(self):
        """Get inside temperature."""
        return self.__power

    def get_generating_status(self):
        """Get outside temperature."""
        return self.__generating_status

    @property
    def device_class(self) -> Text:
        """Return the HA device class."""
        return self._device_class

    @property
    def state_class(self) -> Text:
        """Return the HA state class."""
        return self._state_class
