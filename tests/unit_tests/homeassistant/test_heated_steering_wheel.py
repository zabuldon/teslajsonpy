"""Test HeatedSteeringWheelSwitch."""

import pytest

from teslajsonpy.controller import Controller
from teslajsonpy.homeassistant.heated_steering_wheel import HeatedSteeringWheelSwitch

from tests.tesla_mock import TeslaMock


def test_has_battery(monkeypatch):
    """Test has_battery()."""

    _mock = TeslaMock(monkeypatch)
    _controller = Controller(None)

    _data = _mock.data_request_vehicle()
    _seat = HeatedSteeringWheelSwitch(_data, _controller)

    assert not _seat.has_battery()


def test_get_steering_wheel_heat_on_init(monkeypatch):
    """Test get_steering_wheel_heat() after initialization."""

    _mock = TeslaMock(monkeypatch)
    _controller = Controller(None)

    _data = _mock.data_request_vehicle()
    _wheel = HeatedSteeringWheelSwitch(_data, _controller)

    assert not _wheel is None
    assert not _wheel.get_steering_wheel_heat()


@pytest.mark.asyncio
async def test_get_steering_wheel_heat_after_update(monkeypatch):
    """Test get_steering_wheel_heat() after an update."""

    _mock = TeslaMock(monkeypatch)
    _controller = Controller(None)

    NEW_LEVEL = True

    _data = _mock.data_request_vehicle()
    _data["climate_state"]['steering_wheel_heater'] = NEW_LEVEL
    _seat = HeatedSteeringWheelSwitch(_data, _controller)

    await _seat.async_update()

    assert not _seat is None
    assert _seat.get_steering_wheel_heat() == NEW_LEVEL


@pytest.mark.asyncio
async def test_set_get_seat_heat_level(monkeypatch):
    """Test HeatedSteeringWheelSwitch()."""

    _mock = TeslaMock(monkeypatch)
    _controller = Controller(None)

    ORIG_LEVEL = True
    NEW_LEVEL = False

    _data = _mock.data_request_vehicle()
    _data["climate_state"]["steering_wheel_heater"] = ORIG_LEVEL
    _seat = HeatedSteeringWheelSwitch(_data, _controller)

    await _seat.async_update()

    await _seat.set_steering_wheel_heat(NEW_LEVEL)

    assert not _seat is None
    assert _seat.get_steering_wheel_heat() == NEW_LEVEL


@pytest.mark.asyncio
async def test_seat_same_level(monkeypatch):
    """Test set_steering_wheel_heat to same level."""

    _mock = TeslaMock(monkeypatch)
    _controller = Controller(None)

    ORIG_LEVEL = True

    _data = _mock.data_request_vehicle()
    _data["climate_state"]["steering_wheel_heater"] = ORIG_LEVEL
    _seat = HeatedSteeringWheelSwitch(_data, _controller)

    await _seat.async_update()

    await _seat.set_steering_wheel_heat(ORIG_LEVEL)

    assert not _seat is None
    assert _seat.get_steering_wheel_heat() == ORIG_LEVEL
