#  SPDX-License-Identifier: Apache-2.0
"""
Home Assistant binary sensors.
"""

from enum import Enum

from teslajsonpy.ha.entity import Entity


class BinarySensorType(Enum):
    """List of binary sensor types from Home Assistant.
    
    See also: https://developers.home-assistant.io/docs/entity_binary_sensor#available-device-classes
    """

    BATTERY = "battery"  # On means low Off means normal.
    COLD = "cold"  # On means cold Off means normal.
    CONNECTIVITY = "connectivity"  # On means connected Off means disconnected.
    DOOR = "door"  # On means open Off means closed.
    GARAGE_DOOR = "garage_door"  # On means open Off means closed.
    GAS = "gas"  # On means gas detected Off means no gas (clear).
    HEAT = "heat"  # On means hot Off means normal.
    LIGHT = "light"  # On means light detected Off means no light.
    LOCK = "lock"  # On means open (unlocked) Off means closed (locked).
    MOISTURE = "moisture"  # On means wet Off means dry.
    MOTION = "motion"  # On means motion detected Off means no motion (clear).
    MOVING = "moving"  # On means moving Off means not moving (stopped).
    OCCUPANCY = "occupancy"  # On means occupied Off means not occupied (clear).
    OPENING = "opening"  # On means open Off means closed.
    PLUG = "plug"  # On means plugged in Off means unplugged.
    POWER = "power"  # On means power detected Off means no power.
    PRESENCE = "presence"  # On means home Off means away.
    PROBLEM = "problem"  # On means problem detected Off means no problem (OK).
    SAFETY = "safety"  # On means unsafe Off means safe.
    SMOKE = "smoke"  # On means smoke detected Off means no smoke (clear).
    SOUND = "sound"  # On means sound detected Off means no sound (clear).
    VIBRATION = "vibration"  # On means vibration detected Off means no vibration.
    WINDOW = "window"  # On means open Off means closed.


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


class ParkingSensor(BinarySensor):
    """Tesla parking sensor for Home Assistant."""

    def __init__(self):
        """Initialize a the sensor.
        
        Parameters
        ----------
        device_class : str
            The class of the device
        """

        super().__init__(BinarySensorType.POWER)

    def update(self) -> None:
        """Fetch the latest state from the device and store it in the properties."""
        raise NotImplementedError

    async def async_update(self) -> None:
        """Fetch asynchronously the latest state from the device and store it in the properties."""
        raise NotImplementedError
