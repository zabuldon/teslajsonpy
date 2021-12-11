"""Test parking sensor."""

import pytest

from teslajsonpy.controller import Controller
from teslajsonpy.homeassistant.binary_sensor import ParkingSensor

from tests.tesla_mock import TeslaMock


def test_has_battery(monkeypatch):
    """Test has_battery()."""

    _mock = TeslaMock(monkeypatch)
    _controller = Controller(None)

    _data = _mock.data_request_vehicle()
    _sensor = ParkingSensor(_data, _controller)

    assert not _sensor.has_battery()


def test_get_value_on_init(monkeypatch):
    """Test get_value() after initialization."""

    _mock = TeslaMock(monkeypatch)
    _controller = Controller(None)

    _data = _mock.data_request_vehicle()
    _sensor = ParkingSensor(_data, _controller)

    assert _sensor is not None
    assert _sensor.get_value() is None


@pytest.mark.asyncio
async def test_get_value_after_update(monkeypatch):
    """Test get_value() after an update."""

    _mock = TeslaMock(monkeypatch)
    _controller = Controller(None)

    _data = _mock.data_request_vehicle()
    _sensor = ParkingSensor(_data, _controller)

    await _sensor.async_update()

    assert _sensor is not None
    assert _sensor.get_value() is not None
    assert _sensor.get_value()


@pytest.mark.asyncio
async def test_get_value_on(monkeypatch):
    """Test get_value() for parking mode ON."""

    _mock = TeslaMock(monkeypatch)
    _controller = Controller(None)

    _data = _mock.data_request_vehicle()
    _sensor = ParkingSensor(_data, _controller)
    _data["drive_state"]["shift_state"] = "P"

    await _sensor.async_update()

    assert _sensor is not None
    assert _sensor.get_value() is not None
    assert _sensor.get_value()


@pytest.mark.asyncio
async def test_get_value_off(monkeypatch):
    """Test get_value() for parking mode OFF."""

    _mock = TeslaMock(monkeypatch)
    _controller = Controller(None)

    _data = _mock.data_request_vehicle()
    _sensor = ParkingSensor(_data, _controller)
    _data["drive_state"]["shift_state"] = "N"

    await _sensor.async_update()

    assert _sensor is not None
    assert _sensor.get_value() is not None
    assert not _sensor.get_value()
