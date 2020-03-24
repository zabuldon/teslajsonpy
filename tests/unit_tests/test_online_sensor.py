"""Test online sensor."""

import pytest

from tests.tesla_mock import TeslaMock

from teslajsonpy.controller import Controller
from teslajsonpy.binary_sensor import OnlineSensor


def test_has_battery(monkeypatch):
    """Test has_battery()."""

    _mock = TeslaMock(monkeypatch)
    _controller = Controller(None)

    _data = _mock.data_request_vehicle()
    _sensor = OnlineSensor(_data, _controller)

    assert not _sensor.has_battery()


def test_get_value_on_init(monkeypatch):
    """Test get_value() after initialization."""

    _mock = TeslaMock(monkeypatch)
    _controller = Controller(None)

    _data = _mock.data_request_vehicle()
    _sensor = OnlineSensor(_data, _controller)

    assert not _sensor is None
    assert _sensor.get_value() is None


@pytest.mark.asyncio
async def test_get_value_after_update(monkeypatch):
    """Test get_value() after an update."""

    _mock = TeslaMock(monkeypatch)
    _controller = Controller(None)
    monkeypatch.setitem(_controller.car_online, "5YJSA11111111111", True)
    monkeypatch.setitem(
        _controller.car_state, "5YJSA11111111111", TeslaMock.data_request_vehicle()
    )

    _data = _mock.data_request_vehicle()
    _sensor = OnlineSensor(_data, _controller)

    await _sensor.async_update()

    assert not _sensor is None
    assert not _sensor.get_value() is None
    assert _sensor.get_value()


@pytest.mark.asyncio
async def test_get_value_on(monkeypatch):
    """Test get_value() for online mode."""

    _mock = TeslaMock(monkeypatch)
    _controller = Controller(None)
    monkeypatch.setitem(_controller.car_online, "5YJSA11111111111", True)
    monkeypatch.setitem(
        _controller.car_state, "5YJSA11111111111", TeslaMock.data_request_vehicle()
    )

    _data = _mock.data_request_vehicle()
    _sensor = OnlineSensor(_data, _controller)
    _data["state"] = "online"

    await _sensor.async_update()

    assert not _sensor is None
    assert not _sensor.get_value() is None
    assert _sensor.get_value()


@pytest.mark.asyncio
async def test_get_value_off(monkeypatch):
    """Test get_value() for offline mode."""

    _mock = TeslaMock(monkeypatch)
    _controller = Controller(None)
    monkeypatch.setitem(_controller.car_online, "5YJSA11111111111", False)
    monkeypatch.setitem(
        _controller.car_state, "5YJSA11111111111", TeslaMock.data_request_vehicle()
    )

    _data = _mock.data_request_vehicle()
    _sensor = OnlineSensor(_data, _controller)
    _data["state"] = "asleep"

    await _sensor.async_update()

    assert not _sensor is None
    assert not _sensor.get_value() is None
    assert not _sensor.get_value()
