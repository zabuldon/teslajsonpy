"""Test temp sensor."""

import pytest

from tests.tesla_mock import TeslaMock

from teslajsonpy.controller import Controller
from teslajsonpy.climate import TempSensor


def test_has_battery(monkeypatch):
    """Test has_battery()."""

    _mock = TeslaMock(monkeypatch)
    _controller = Controller(None)

    _data = _mock.data_request_vehicle()
    _sensor = TempSensor(_data, _controller)

    assert not _sensor.has_battery()


def test_device_class(monkeypatch):
    """Test device_class()."""

    _mock = TeslaMock(monkeypatch)
    _controller = Controller(None)

    _data = _mock.data_request_vehicle()
    _sensor = TempSensor(_data, _controller)

    assert _sensor.device_class == "temperature"


def test_get_temp_on_init(monkeypatch):
    """Test get_inside_temp() and get_outside_temp() after initialization."""

    _mock = TeslaMock(monkeypatch)
    _controller = Controller(None)

    _data = _mock.data_request_vehicle()
    _sensor = TempSensor(_data, _controller)

    assert not _sensor is None
    assert _sensor.get_inside_temp() is None
    assert _sensor.get_outside_temp() is None


@pytest.mark.asyncio
async def test_get_temp_after_update(monkeypatch):
    """Test get_inside_temp() and get_outside_temp() after an update."""

    _mock = TeslaMock(monkeypatch)
    _controller = Controller(None)

    _data = _mock.data_request_vehicle()
    _data["climate_state"]["inside_temp"] = 18.8
    _data["climate_state"]["outside_temp"] = 22.2
    _sensor = TempSensor(_data, _controller)

    await _sensor.async_update()

    assert not _sensor is None
    assert not _sensor.get_inside_temp() is None
    assert not _sensor.get_outside_temp() is None
    assert _sensor.get_inside_temp() == 18.8
    assert _sensor.get_outside_temp() == 22.2
