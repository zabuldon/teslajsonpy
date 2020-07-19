"""Test vehicle device."""

import pytest

from tests.tesla_mock import TeslaMock

from teslajsonpy.controller import Controller
from teslajsonpy.vehicle import VehicleDevice


def test_is_armable(monkeypatch):
    """Test is_armable()."""

    _mock = TeslaMock(monkeypatch)
    _controller = Controller(None)

    _data = _mock.data_request_vehicle()
    _device = VehicleDevice(_data, _controller)

    assert not _device.is_armable()


def test_is_armed(monkeypatch):
    """Test is_armed()."""

    _mock = TeslaMock(monkeypatch)
    _controller = Controller(None)

    _data = _mock.data_request_vehicle()
    _device = VehicleDevice(_data, _controller)

    assert not _device.is_armed()


def test_values_on_init(monkeypatch):
    """Test values after initialization."""

    _mock = TeslaMock(monkeypatch)
    _controller = Controller(None)

    _data = _mock.data_request_vehicle()
    _device = VehicleDevice(_data, _controller)

    assert _device is not None

    assert _device.car_name() is not None
    assert _device.car_name() == "Nikola 2.0"

    assert _device.car_type is not None
    assert _device.car_type == "Model S"

    assert _device.car_version is not None
    assert _device.car_version == ""

    assert _device.id() is not None
    assert _device.id() == 12345678901234567

    assert _device.sentry_mode_available is not None
    assert _device.sentry_mode_available

    assert _device.vehicle_id is not None
    assert _device.vehicle_id() == 1234567890

    assert not _device.update_available
    assert _device.update_version is None


@pytest.mark.asyncio
async def test_values_after_update(monkeypatch):
    """Test values after update."""

    _mock = TeslaMock(monkeypatch)
    _controller = Controller(None)

    _data = _mock.data_request_vehicle()
    _device = VehicleDevice(_data, _controller)

    await _device.async_update()

    assert _device is not None

    assert not _device.car_name() is None
    assert _device.car_name() == "Nikola 2.0"

    assert _device.car_type is not None
    assert _device.car_type == "Model S"

    assert _device.car_version is not None
    assert _device.car_version == "2019.40.2.1 38f55d9f9205"

    assert _device.id() is not None
    assert _device.id() == 12345678901234567

    assert _device.sentry_mode_available is not None
    assert _device.sentry_mode_available

    assert _device.vehicle_id is not None
    assert _device.vehicle_id() == 1234567890


@pytest.mark.asyncio
async def test_assumed_state_online(monkeypatch):
    # pylint: disable=protected-access
    """Test assumed_state() with online vehicle."""

    _mock = TeslaMock(monkeypatch)
    _controller = Controller(None)

    # TODO: Should not have protected access here (see vehicle.py)
    monkeypatch.setitem(_controller.car_online, 12345678901234567, True)
    monkeypatch.setitem(_controller._last_update_time, 12345678901234567, 100)
    monkeypatch.setitem(_controller._last_wake_up_time, 12345678901234567, 0)

    _data = _mock.data_request_vehicle()
    _device = VehicleDevice(_data, _controller)

    await _device.async_update()

    assert _device is not None
    assert not _device.assumed_state() is None
    assert not _device.assumed_state()


@pytest.mark.asyncio
async def test_assumed_state_offline(monkeypatch):
    # pylint: disable=protected-access
    """Test assumed_state() with offline vehicle."""

    _mock = TeslaMock(monkeypatch)
    _controller = Controller(None)

    # TODO: Should not have protected access here (see vehicle.py)
    monkeypatch.setitem(_controller.car_online, 12345678901234567, False)
    monkeypatch.setitem(_controller._last_update_time, 12345678901234567, 1000)
    monkeypatch.setitem(_controller._last_wake_up_time, 12345678901234567, 0)

    _data = _mock.data_request_vehicle()
    _device = VehicleDevice(_data, _controller)

    await _device.async_update()

    assert _device is not None
    assert not _device.assumed_state() is None
    assert _device.assumed_state()
