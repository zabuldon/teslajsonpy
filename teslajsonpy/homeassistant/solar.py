#  SPDX-License-Identifier: Apache-2.0
"""
Python Package for controlling Tesla API.

For more details about this api, please refer to the documentation at
https://github.com/zabuldon/teslajsonpy
"""
from typing import Text

from teslajsonpy.homeassistant.energy_site import EnergySiteDevice


class Solar(EnergySiteDevice):
    """Home-assistant class of Solar for Tesla Energy Sites.

    This is intended to be partially inherited by a Home-Assitant entity.
    """

    def __init__(self, data, controller):
        """Initialize the solar energy site controls.

        Parameters
        ----------
        data : dict
            The base state for a Tesla Energy Site.
            https://tesla-api.timdorr.com/vehicle/state/data
        controller : teslajsonpy.Controller
            The controller that controls updates to the Tesla API.

        Returns
        -------
        None

        """
        super().__init__(data, controller)
        self.__solar_power = 0

        self.hass_type = "sensor"
        self._device_class: Text = "energy"
        self.measurement = "Wh"
        self.name = self._name()
        self.uniq_name = self._uniq_name()

    @property
    def solar_power(self):
        """Return current solar power."""
        return self.__solar_power

    async def async_update(self,) -> None:
        """Update the solar state."""
        await super().async_update()
        self.refresh()

    def refresh(self) -> None:
        """Refresh data.

        This assumes the controller has already been updated
        """
        super().refresh()
        data = self._controller.get_energy_site_live_params(self.energy_site_id())
        if data:
            self.__solar_power = (data["solar_power"] if data["solar_power"] else self.__solar_power)
    @property
    def device_class(self) -> Text:
        """Return the HA device class."""
        return self._device_class
