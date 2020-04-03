#  SPDX-License-Identifier: Apache-2.0
"""Home Assistant locks."""

from typing import Text

from teslajsonpy.ha.entity import Entity


class Lock(Entity):
    """Wrapper for a Home Assistant lock.

    See also: https://developers.home-assistant.io/docs/entity_lock
    """

    def __init__(self):
        """Initialize a lock."""

        super().__init__()
        self._is_locked = False
        self._changed_by = None

    @property
    def is_locked(self) -> bool:
        """Return True if the lock is currently locked. Used to determine state."""
        return self._is_locked

    @property
    def changed_by(self) -> Text:
        """Describe what the last change was triggered by."""
        return self._changed_by

    async def lock(self) -> None:
        """Lock the lock."""
        raise NotImplementedError

    async def unlock(self) -> None:
        """Unlock the lock."""
        raise NotImplementedError

    async def open(self):
        """Open (unlatch) the lock."""
        raise NotImplementedError

    async def update(self) -> None:
        """Fetch the latest state from the device and store it in the properties."""
        raise NotImplementedError


class DoorLock(Lock):
    """Tesla door lock for Home Assistant."""

    async def update(self) -> None:
        """Fetch the latest state from the device and store it in the properties."""
        raise NotImplementedError


class TrunkLock(Lock):
    """Tesla trunk lock for Home Assistant."""

    async def update(self) -> None:
        """Fetch the latest state from the device and store it in the properties."""
        raise NotImplementedError


class FrunkLock(Lock):
    """Tesla trunk lock for Home Assistant."""

    async def update(self) -> None:
        """Fetch the latest state from the device and store it in the properties."""
        raise NotImplementedError
