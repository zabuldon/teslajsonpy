"""Test charger lock."""

import pytest

from tests.tesla_mock import TeslaMock

from teslajsonpy.controller import Controller
from teslajsonpy.lock import ChargerLock


def test_has_battery(monkeypatch):
    """Test has_battery()."""

    _mock = TeslaMock(monkeypatch)
    _controller = Controller(None)

    _data = _mock.data_request_vehicle()
    _lock = ChargerLock(_data, _controller)

    assert not _lock.has_battery()


def test_is_locked_on_init(monkeypatch):
    """Test is_locked() after initialization."""

    _mock = TeslaMock(monkeypatch)
    _controller = Controller(None)

    _data = _mock.data_request_vehicle()
    _lock = ChargerLock(_data, _controller)

    assert not _lock is None
    assert not _lock.is_locked()


@pytest.mark.asyncio
async def test_is_locked_after_update(monkeypatch):
    """Test is_locked() after an update."""

    _mock = TeslaMock(monkeypatch)
    _controller = Controller(None)

    _data = _mock.data_request_vehicle()
    _data["charge_state"]["charge_port_door_open"] = True
    _lock = ChargerLock(_data, _controller)

    await _lock.async_update()

    assert not _lock is None
    assert _lock.is_locked()


@pytest.mark.asyncio
async def test_lock(monkeypatch):
    """Test lock()."""

    _mock = TeslaMock(monkeypatch)
    _controller = Controller(None)

    _data = _mock.data_request_vehicle()
    _data["charge_state"]["charge_port_door_open"] = False
    _lock = ChargerLock(_data, _controller)

    await _lock.async_update()
    await _lock.lock()

    assert not _lock is None
    assert _lock.is_locked()


@pytest.mark.asyncio
async def test_lock_already_locked(monkeypatch):
    """Test lock() when already locked."""

    _mock = TeslaMock(monkeypatch)
    _controller = Controller(None)

    _data = _mock.data_request_vehicle()
    _data["charge_state"]["charge_port_door_open"] = True
    _lock = ChargerLock(_data, _controller)

    await _lock.async_update()
    await _lock.lock()

    assert not _lock is None
    assert _lock.is_locked()


@pytest.mark.asyncio
async def test_unlock(monkeypatch):
    """Test unlock()."""

    _mock = TeslaMock(monkeypatch)
    _controller = Controller(None)

    _data = _mock.data_request_vehicle()
    _data["charge_state"]["charge_port_door_open"] = True
    _lock = ChargerLock(_data, _controller)

    await _lock.async_update()
    await _lock.unlock()

    assert not _lock is None
    assert not _lock.is_locked()


@pytest.mark.asyncio
async def test_unlock_already_unlocked(monkeypatch):
    """Test unlock() when already unlocked."""

    _mock = TeslaMock(monkeypatch)
    _controller = Controller(None)

    _data = _mock.data_request_vehicle()
    _data["charge_state"]["charge_port_door_open"] = False
    _lock = ChargerLock(_data, _controller)

    await _lock.async_update()
    await _lock.unlock()

    assert not _lock is None
    assert not _lock.is_locked()
