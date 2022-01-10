"""Test temp sensor."""

import pytest

from teslajsonpy.controller import Controller
from teslajsonpy.homeassistant.climate import TempSensor

from tests.tesla_mock import TeslaMock, VIN, CAR_ID, CLIMATE_STATE


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

    assert _sensor is not None
    assert _sensor.get_inside_temp() is None
    assert _sensor.get_outside_temp() is None


@pytest.mark.asyncio
async def test_get_temp_after_update(monkeypatch):
    """Test get_inside_temp() and get_outside_temp() after an update."""

    _mock = TeslaMock(monkeypatch)
    _controller = Controller(None)
    _controller.set_id_vin(CAR_ID, VIN)

    _data = _mock.data_request_vehicle()
    _sensor = TempSensor(_data, _controller)

    CLIMATE_STATE["inside_temp"] = 18.8
    CLIMATE_STATE["outside_temp"] = 22.2
    _controller.set_climate_params(vin=VIN, params=CLIMATE_STATE)

    await _sensor.async_update()

    assert _sensor is not None
    assert not _sensor.get_inside_temp() is None
    assert not _sensor.get_outside_temp() is None
    assert _sensor.get_inside_temp() == 18.8
    assert _sensor.get_outside_temp() == 22.2
