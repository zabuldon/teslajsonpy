"""Test online sensor."""

import pytest

from teslajsonpy.controller import Controller
from teslajsonpy.homeassistant.binary_sensor import OnlineSensor

from tests.tesla_mock import TeslaMock, VIN

# VIN = "5YJSA11111111111"


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

    assert _sensor is not None
    assert _sensor.get_value() is None


@pytest.mark.asyncio
async def test_get_value_after_update(monkeypatch):
    """Test get_value() after an update."""

    _mock = TeslaMock(monkeypatch)
    _controller = Controller(None)
    monkeypatch.setitem(_controller.car_online, VIN, True)
    monkeypatch.setitem(_controller.car_state, VIN, _mock.data_request_vehicle())

    _data = _mock.data_request_vehicle()
    _sensor = OnlineSensor(_data, _controller)

    await _sensor.async_update()

    assert _sensor is not None
    assert not _sensor.get_value() is None
    assert _sensor.get_value()


@pytest.mark.asyncio
async def test_get_value_on(monkeypatch):
    """Test get_value() for online mode."""

    _mock = TeslaMock(monkeypatch)
    _controller = Controller(None)
    monkeypatch.setitem(_controller.car_online, VIN, True)
    monkeypatch.setitem(_controller.car_state, VIN, _mock.data_request_vehicle())

    _data = _mock.data_request_vehicle()
    _sensor = OnlineSensor(_data, _controller)
    _data["state"] = "online"

    await _sensor.async_update()

    assert _sensor is not None
    assert not _sensor.get_value() is None
    assert _sensor.get_value()
    assert _sensor.attrs == {
        "state": "online",
        "vin": VIN,
        "id": 12345678901234567,
        "vehicle_id": 1234567890,
        "update_interval": 300,
        'vehicle_data': '{"climate_state": {}, "charge_state": {}, "vehicle_state": '
                        '{}, "vehicle_config": {}, "drive_state": {}, "gui_settings": '
                        '{}}'
    }


@pytest.mark.asyncio
async def test_get_value_off(monkeypatch):
    """Test get_value() for offline mode."""

    _mock = TeslaMock(monkeypatch)
    _controller = Controller(None)
    monkeypatch.setitem(_controller.car_online, VIN, False)
    monkeypatch.setitem(_controller.car_state, VIN, _mock.data_request_vehicle())

    _data = _mock.data_request_vehicle()
    _sensor = OnlineSensor(_data, _controller)
    _data["state"] = "asleep"
    _controller.set_climate_params(vin=VIN, params={'climate_state': 'on'})
    _controller.set_charging_params(vin=VIN, params={'charging_state': 'on'})
    _controller.set_state_params(vin=VIN, params={'vehicle_state': 'on'})
    _controller.set_config_params(vin=VIN, params={'vehicle_config': 'on'})
    _controller.set_drive_params(vin=VIN, params={'drive_state': 'on'})
    _controller.set_gui_params(vin=VIN, params={'gui_setting': 'on'})
    
    await _sensor.async_update()

    assert _sensor is not None
    assert not _sensor.get_value() is None
    assert not _sensor.get_value()
    assert _sensor.attrs == {
        "state": "asleep",
        "vin": VIN,
        "id": 12345678901234567,
        "vehicle_id": 1234567890,
        "update_interval": 300,
        "vehicle_data": '{"climate_state": {"climate_state": "on"},'
                        ' "charge_state": {"charge_state": "on"},'
                        ' "vehicle_state": {"vehicle_state": "on"},'
                        ' "vehicle_config": {"vehicle_config": "on"},'
                        ' "drive_state": {"drive_state": "on"},'
                        ' "gui_settings": {"gui_settings": "on"}'
    }
