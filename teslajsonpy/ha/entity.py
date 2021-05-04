#  SPDX-License-Identifier: Apache-2.0
"""Home Assistant entity."""

from typing import Dict, Text


class Entity:
    """Wrapper for a Home Assistant entity.

    All Tesla entities shuld override this base class.
    See also: https://developers.home-assistant.io/docs/entity_index
    """

    def __init__(self, device_class: Text = None):
        """Initialize the entity.

        Parameters
        ----------
        device_class : typing.Text, optional
            The class of the device

        """
        self._device_class: Text = device_class

    @property
    def assumed_state(self) -> bool:
        """Return True if the state is based on our assumption instead of reading it from the device."""
        return False

    @property
    def available(self) -> bool:
        """Indicate True if Home Assistant is able to read the state and control the underlying device."""
        return True

    @property
    def device_class(self) -> Text:
        """Return extra classification of what the device is. Each domain specifies their own.

        Device classes can come with extra requirements for unit of measurement and supported features.
        """
        return self._device_class

    @property
    def device_state_attributes(self) -> Dict:
        """Return extra information to store in the state machine.

        It needs to be information that further explains the state, it should not be static information like firmware version.
        """
        return None

    @property
    def entity_picture(self) -> Text:
        """Return the URL of a picture to show for the entity."""
        return None

    @property
    def name(self) -> Text:
        """Return the name of the entity."""
        return None

    @property
    def should_poll(self) -> bool:
        """Tell Home Assistant if it must check with the entity for an updated state.

        If set to False, entity will need to notify Home Assistant of new updates by calling one of the schedule update methods.
        """
        return True

    @property
    def unique_id(self) -> Text:
        """Return the unique identifier for this entity.

        Needs to be unique within a platform (ie light.hue).
        It must not be configurable by the user or be changeable.
        """
        return None

    @property
    def force_update(self) -> bool:
        """Write each update to the state machine, even if the data is the same.

        Example use: when you are directly reading the value from a connected sensor instead of a cache.
        Use with caution, will spam the state machine.
        """
        return False

    @property
    def icon(self) -> Text:
        """Return the icon to use in the frontend.

        Icons start with mdi: plus an identifier.
        You probably don't need this since Home Assistant already provides default icons for all devices.
        """
        return None

    @property
    def entity_registry_enabled_default(self) -> bool:
        """Indicate if the entity should be enabled or disabled when it is first added to the entity registry."""
        return True

    async def update(self) -> None:
        """Fetch the latest state from the device and store it in the properties."""
        raise NotImplementedError
