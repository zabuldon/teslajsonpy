#  SPDX-License-Identifier: Apache-2.0
"""
Python Package for controlling Tesla API.

For more details about this api, please refer to the documentation at
https://github.com/zabuldon/teslajsonpy
"""
import logging
from typing import Dict, Text

_LOGGER = logging.getLogger(__name__)


class EnergySiteDevice:
    """Home-assistant class of Tesla Energy Site Devices.

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
        self._resource_type: Text = data["resource_type"]

        self._controller = controller
        self.should_poll: bool = True
        self.type: Text = "device"
        self.attrs: Dict[Text, Text] = {}

    def _name(self) -> Text:
        return self._uniq_name()

    def _uniq_name(self) -> Text:
        return "Tesla Energy Site {} {}".format(
            str(self.energy_site_id()).upper(), self.resource_type.upper()
        )

    def id(self) -> int:
        # pylint: disable=invalid-name
        """Return the id of this Energy Site."""
        return self._id

    def energy_site_id(self) -> int:
        """Return the energy_site_id of this Energy Site."""
        return self._energy_site_id

    @property
    def resource_type(self) -> Text:
        """Return the resource type of this Energy Site."""
        return self._resource_type

    async def async_update(
        self
    ) -> None:
        """Update the energy site data.

        This function will call a controller update.
        """
        await self._controller.update_energy_site(
            self.energy_site_id(),
        )
        self.refresh()

    def refresh(self) -> None:
        """Refresh the energy site data.

        This assumes the controller has already been updated. This should be
        called by inherited classes so the overall status information is updated.
        """

    @staticmethod
    def has_battery():
        """Return whether the device has a battery."""
        return False

