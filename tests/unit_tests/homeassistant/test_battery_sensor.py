"""Test battery sensor."""

import pytest

from teslajsonpy.controller import Controller
from teslajsonpy.homeassistant.battery_sensor import Battery

from tests.tesla_mock import TeslaMock


def test_has_battery(monkeypatch):
    """Test has_battery()."""

    _mock = TeslaMock(monkeypatch)
    _controller = Controller(None)

    _data = _mock.data_request_vehicle()
    _sensor = Battery(_data, _controller)

    assert _sensor.has_battery()


def test_device_class(monkeypatch):
    """Test device_class()."""

    _mock = TeslaMock(monkeypatch)
    _controller = Controller(None)

    _data = _mock.data_request_vehicle()
    _sensor = Battery(_data, _controller)

    assert _sensor.device_class == "battery"


def test_get_value_on_init(monkeypatch):
    """Test get_value() after initialization."""

    _mock = TeslaMock(monkeypatch)
    _controller = Controller(None)

    _data = _mock.data_request_vehicle()
    _sensor = Battery(_data, _controller)

    assert not _sensor is None
    assert _sensor.get_value() is None


@pytest.mark.asyncio
async def test_get_value_after_update(monkeypatch):
    """Test get_value() after an update."""

    _mock = TeslaMock(monkeypatch)
    _controller = Controller(None)

    _data = _mock.data_request_vehicle()
    _sensor = Battery(_data, _controller)

    await _sensor.async_update()

    assert not _sensor is None
    assert not _sensor.get_value() is None
    assert _sensor.get_value() == 64


@pytest.mark.asyncio
async def test_battery_level(monkeypatch):
    """Test battery_level()."""

    _mock = TeslaMock(monkeypatch)
    _controller = Controller(None)

    _data = _mock.data_request_vehicle()
    _sensor = Battery(_data, _controller)

    await _sensor.async_update()

    assert not _sensor is None
    assert not _sensor.get_value() is None
    assert _sensor.battery_level() == 64


@pytest.mark.asyncio
async def test_battery_charging_off(monkeypatch):
    """Test battery_charging() when not charging."""

    _mock = TeslaMock(monkeypatch)
    _controller = Controller(None)

    _data = _mock.data_request_vehicle()
    _data["charge_state"]["charging_state"] = "Disconnected"
    _sensor = Battery(_data, _controller)

    await _sensor.async_update()

    assert not _sensor is None
    assert not _sensor.battery_charging()


@pytest.mark.asyncio
async def test_battery_charging_on(monkeypatch):
    """Test battery_charging() when charging."""

    _mock = TeslaMock(monkeypatch)
    _controller = Controller(None)

    _data = _mock.data_request_vehicle()
    _data["charge_state"]["charging_state"] = "Charging"
    _sensor = Battery(_data, _controller)

    await _sensor.async_update()

    assert not _sensor is None
    assert _sensor.battery_charging()


@pytest.mark.asyncio
async def test_async_update(monkeypatch):
    """Test async_update()."""

    _mock = TeslaMock(monkeypatch)
    _controller = Controller(None)

    _data = _mock.data_request_vehicle()
    _data["charge_state"]["battery_level"] = 12.3
    _sensor = Battery(_data, _controller)

    await _sensor.async_update()

    assert not _sensor is None
    assert not _sensor.get_value() is None
    assert _sensor.get_value() == 12.3
