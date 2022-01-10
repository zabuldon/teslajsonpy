"""Test odometer sensor."""

import pytest

from teslajsonpy.controller import Controller
from teslajsonpy.homeassistant.gps import Odometer

from tests.tesla_mock import TeslaMock, VIN, CAR_ID


def test_has_battery(monkeypatch):
    """Test has_battery()."""

    _mock = TeslaMock(monkeypatch)
    _controller = Controller(None)

    _data = _mock.data_request_vehicle()
    _odometer = Odometer(_data, _controller)

    assert not _odometer.has_battery()


def test_device_class(monkeypatch):
    """Test device_class()."""

    _mock = TeslaMock(monkeypatch)
    _controller = Controller(None)

    _data = _mock.data_request_vehicle()
    _odometer = Odometer(_data, _controller)

    assert _odometer.device_class is None


def test_get_value_on_init(monkeypatch):
    """Test get_value() after initialization."""

    _mock = TeslaMock(monkeypatch)
    _controller = Controller(None)

    _data = _mock.data_request_vehicle()
    _odometer = Odometer(_data, _controller)

    assert _odometer is not None
    assert _odometer.get_value() is None


@pytest.mark.asyncio
async def test_get_value_after_update(monkeypatch):
    """Test get_value() after an update."""

    _mock = TeslaMock(monkeypatch)
    _controller = Controller(None)
    _controller.set_id_vin(CAR_ID, VIN)

    _data = _mock.data_request_vehicle()
    _odometer = Odometer(_data, _controller)

    _controller.set_state_params(vin=VIN, params=_data["vehicle_state"])

    await _odometer.async_update()

    assert _odometer is not None
    assert _odometer.get_value() == 33561.4


@pytest.mark.asyncio
async def test_async_update(monkeypatch):
    """Test async_update()."""

    _mock = TeslaMock(monkeypatch)
    _controller = Controller(None)
    _controller.set_id_vin(CAR_ID, VIN)

    _data = _mock.data_request_vehicle()
    _data["vehicle_state"]["odometer"] = 12345.6789
    _odometer = Odometer(_data, _controller)

    _controller.set_state_params(vin=VIN, params=_data["vehicle_state"])

    await _odometer.async_update()

    assert _odometer is not None
    assert _odometer.get_value() is not None
    assert _odometer.get_value() == 12345.7


@pytest.mark.asyncio
async def test_async_update_in_kmh(monkeypatch):
    """Test async_update() for units in km/h."""

    _mock = TeslaMock(monkeypatch)
    _controller = Controller(None)
    _controller.set_id_vin(CAR_ID, VIN)

    _data = _mock.data_request_vehicle()
    _data["gui_settings"]["gui_distance_units"] = "km/hr"
    _data["vehicle_state"]["odometer"] = 12345.6789
    _odometer = Odometer(_data, _controller)

    _controller.set_state_params(vin=VIN, params=_data["vehicle_state"])
    _controller.set_gui_params(vin=VIN, params=_data["gui_settings"])

    await _odometer.async_update()

    assert _odometer is not None
    assert _odometer.get_value() is not None
    assert _odometer.get_value() == 12345.7


@pytest.mark.asyncio
async def test_async_update_in_mph(monkeypatch):
    """Test async_update() for units in mph."""

    _mock = TeslaMock(monkeypatch)
    _controller = Controller(None)
    _controller.set_id_vin(CAR_ID, VIN)

    _data = _mock.data_request_vehicle()
    _data["gui_settings"]["gui_distance_units"] = "mi/hr"
    _data["vehicle_state"]["odometer"] = 12345.6789
    _odometer = Odometer(_data, _controller)

    _controller.set_state_params(vin=VIN, params=_data["vehicle_state"])
    _controller.set_gui_params(vin=VIN, params=_data["gui_settings"])

    await _odometer.async_update()

    assert _odometer is not None
    assert _odometer.get_value() is not None
    assert _odometer.get_value() == 12345.7
