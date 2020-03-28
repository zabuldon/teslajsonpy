"""Test frunk sensor."""

import pytest

from tests.tesla_mock import TeslaMock

from teslajsonpy.controller import Controller
from teslajsonpy.trunk import FrunkSensor


def test_has_battery(monkeypatch):
    """Test has_battery()."""

    _mock = TeslaMock(monkeypatch)
    _controller = Controller(None)

    _data = _mock.data_request_vehicle()
    _sensor = FrunkSensor(_data, _controller)

    assert not _sensor.has_battery()


def test_get_value_on_init(monkeypatch):
    """Test get_value() after initialization."""

    _mock = TeslaMock(monkeypatch)
    _controller = Controller(None)

    _data = _mock.data_request_vehicle()
    _sensor = FrunkSensor(_data, _controller)

    assert not _sensor is None
    assert _sensor.get_value() is None


@pytest.mark.asyncio
async def test_get_value_after_update(monkeypatch):
    """Test get_value() after an update."""

    _mock = TeslaMock(monkeypatch)
    _controller = Controller(None)

    _data = _mock.data_request_vehicle()
    _sensor = FrunkSensor(_data, _controller)

    await _sensor.async_update()

    assert not _sensor is None
    assert not _sensor.is_closed() is None
    assert not _sensor.is_open() is None
    assert _sensor.is_closed()
    assert not _sensor.is_open()


@pytest.mark.asyncio
async def test_status_when_open(monkeypatch):
    """Test is_open() and is_closed() when open."""

    _mock = TeslaMock(monkeypatch)
    _controller = Controller(None)

    _data = _mock.data_request_vehicle()
    _data["vehicle_state"]["ft"] = 123
    _sensor = FrunkSensor(_data, _controller)

    await _sensor.async_update()

    assert not _sensor is None
    assert _sensor.is_open()
    assert not _sensor.is_closed()


@pytest.mark.asyncio
async def test_status_when_closed(monkeypatch):
    """Test is_open() and is_closed() when closed."""

    _mock = TeslaMock(monkeypatch)
    _controller = Controller(None)

    _data = _mock.data_request_vehicle()
    _data["vehicle_state"]["ft"] = 0
    _sensor = FrunkSensor(_data, _controller)

    await _sensor.async_update()

    assert not _sensor is None
    assert not _sensor.is_open()
    assert _sensor.is_closed()


@pytest.mark.asyncio
async def test_async_update(monkeypatch):
    """Test async_update()."""

    _mock = TeslaMock(monkeypatch)
    _controller = Controller(None)

    _data = _mock.data_request_vehicle()
    _data["vehicle_state"]["ft"] = 123
    _sensor = FrunkSensor(_data, _controller)

    await _sensor.async_update()

    assert not _sensor is None
    assert not _sensor.get_value() is None
    assert _sensor.get_value() == 123

    _data["vehicle_state"]["ft"] = 0
    await _sensor.async_update()

    assert not _sensor is None
    assert not _sensor.get_value() is None
    assert _sensor.get_value() == 0
