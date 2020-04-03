#  SPDX-License-Identifier: Apache-2.0
"""Home Assistant binary sensors."""

from enum import Enum
from typing import Text

from teslajsonpy.ha.entity import Entity


class BinarySensorType(Enum):
    """List of binary sensor types from Home Assistant.

    See also: https://developers.home-assistant.io/docs/entity_binary_sensor#available-device-classes
    """

    BATTERY: Text = "battery"  # On means low Off means normal.
    COLD: Text = "cold"  # On means cold Off means normal.
    CONNECTIVITY: Text = "connectivity"  # On means connected Off means disconnected.
    DOOR: Text = "door"  # On means open Off means closed.
    GARAGE_DOOR: Text = "garage_door"  # On means open Off means closed.
    GAS: Text = "gas"  # On means gas detected Off means no gas (clear).
    HEAT: Text = "heat"  # On means hot Off means normal.
    LIGHT: Text = "light"  # On means light detected Off means no light.
    LOCK: Text = "lock"  # On means open (unlocked) Off means closed (locked).
    MOISTURE: Text = "moisture"  # On means wet Off means dry.
    MOTION: Text = "motion"  # On means motion detected Off means no motion (clear).
    MOVING: Text = "moving"  # On means moving Off means not moving (stopped).
    OCCUPANCY: Text = "occupancy"  # On means occupied Off means not occupied (clear).
    OPENING: Text = "opening"  # On means open Off means closed.
    PLUG: Text = "plug"  # On means plugged in Off means unplugged.
    POWER: Text = "power"  # On means power detected Off means no power.
    PRESENCE: Text = "presence"  # On means home Off means away.
    PROBLEM: Text = "problem"  # On means problem detected Off means no problem (OK).
    SAFETY: Text = "safety"  # On means unsafe Off means safe.
    SMOKE: Text = "smoke"  # On means smoke detected Off means no smoke (clear).
    SOUND: Text = "sound"  # On means sound detected Off means no sound (clear).
    VIBRATION: Text = "vibration"  # On means vibration detected Off means no vibration.
    WINDOW: Text = "window"  # On means open Off means closed.


class BinarySensor(Entity):
    """Wrapper for a Home Assistant binary sensor.

    See also: https://developers.home-assistant.io/docs/entity_binary_sensor
    """

    def __init__(self, device_class: Text):
        """Initialize a binary sensor.

        Parameters
        ----------
        device_class : Text
            The class of the device

        """

        super().__init__(device_class)
        self._is_on = False

    @property
    def is_on(self) -> bool:
        """Return True if the binary sensor is currently on."""
        return self._is_on

    async def update(self) -> None:
        """Fetch the latest state from the device and store it in the properties."""
        raise NotImplementedError


class ChargerConnectionSensor(BinarySensor):
    """Tesla charger connection sensor for Home Assistant."""

    def __init__(self):
        """Initialize the sensor."""

        super().__init__(BinarySensorType.CONNECTIVITY)

    async def update(self) -> None:
        """Fetch the latest state from the device and store it in the properties."""
        raise NotImplementedError


class OnlineSensor(BinarySensor):
    """Tesla online sensor for Home Assistant."""

    def __init__(self):
        """Initialize the sensor."""

        super().__init__(BinarySensorType.CONNECTIVITY)

    async def update(self) -> None:
        """Fetch the latest state from the device and store it in the properties."""
        raise NotImplementedError


class ParkingSensor(BinarySensor):
    """Tesla parking sensor for Home Assistant."""

    def __init__(self):
        """Initialize the sensor."""

        super().__init__(BinarySensorType.POWER)

    async def update(self) -> None:
        """Fetch the latest state from the device and store it in the properties."""
        raise NotImplementedError
