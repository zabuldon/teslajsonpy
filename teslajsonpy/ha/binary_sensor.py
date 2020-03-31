#  SPDX-License-Identifier: Apache-2.0
"""
Home Assistant binary sensor.
"""

from teslajsonpy.ha.entity import Entity


class BinarySensor(Entity):
    """
    Wrapper for a Home Assistant binary sensor.
    See also: https://developers.home-assistant.io/docs/entity_binary_sensor
    """

    def __init__(self, device_class: str):
        """
        Initialize a binary sensor.
        
        Parameters
        ----------
        device_class : str
            The class of the device
        """

        super().__init__(device_class)
        self._is_on = False

    @property
    def is_on(self) -> bool:
        """Return True if the binary sensor is currently on."""
        return self._is_on

    def update(self) -> None:
        """Fetch the latest state from the device and store it in the properties."""
        raise NotImplementedError

    async def async_update(self) -> None:
        """Fetch asynchronously the latest state from the device and store it in the properties."""
        raise NotImplementedError
