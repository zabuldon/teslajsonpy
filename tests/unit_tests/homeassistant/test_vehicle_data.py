"""Test online sensor."""

import pytest
import copy

from teslajsonpy.controller import Controller
from teslajsonpy.homeassistant.vehicle_data import (
    ChargeStateDataSensor,
    ClimateStateDataSensor,
    DriveStateDataSensor,
    GuiSettingsDataSensor,
    SoftwareDataSensor,
    SpeedLimitDataSensor,
    VehicleConfigDataSensor,
    VehicleDataSensor,
    VehicleStateDataSensor,
)

from tests.tesla_mock import TeslaMock, VIN, CAR_ID


def test_dict_to_attr(monkeypatch):
    """Test converting dict to attributes."""

    _mock = TeslaMock(monkeypatch)
    _controller = Controller(None)

    _data = _mock.data_request_vehicle()
    _sensor = VehicleDataSensor(_data, _controller)

    data = {
        "item1": 1,
        "item2": 2,
        "dict1": {
            "item3": 3,
            "item4": 4,
            "dict2": {
                "item5": 5,
                "dict3": {
                    "item6": 6,
                },
                "dict4": {
                    "item7": 7,
                },
            },
            "dict5": {"item8": 8},
        },
        "dict6": {
            "item9": 9,
        },
        "dict7": {
            "item10": 10,
        },
    }

    attr = {
        "item1": 1,
        "item2": 2,
        "dict1_item3": 3,
        "dict1_item4": 4,
        "dict1_dict2_item5": 5,
        "dict1_dict2_dict3_item6": 6,
        "dict1_dict5_item8": 8,
        "dict7_item10": 10,
    }
    result = _sensor._dict_to_attr(data, ["dict4", "dict6"])
    assert result == attr


def test_dict_to_attr_no_dicts(monkeypatch):
    """Test converting dict to attributes."""

    _mock = TeslaMock(monkeypatch)
    _controller = Controller(None)

    _data = _mock.data_request_vehicle()
    _sensor = VehicleDataSensor(_data, _controller)

    data = {
        "item1": 1,
        "item2": 2,
        "dict1": {
            "item3": 3,
            "item4": 4,
            "dict2": {
                "item5": 5,
                "dict3": {
                    "item6": 6,
                },
                "dict4": {
                    "item7": 7,
                },
            },
            "dict5": {"item8": 8},
        },
        "dict6": {
            "item9": 9,
        },
        "dict7": {
            "item10": 10,
        },
    }

    attr = {
        "item1": 1,
        "item2": 2,
    }
    result = _sensor._dict_to_attr(data, ["*"])
    assert result == attr


@pytest.mark.asyncio
async def test_charge_state_data_sensor(monkeypatch):
    """Test charge state data sensor."""

    _mock = TeslaMock(monkeypatch)
    _controller = Controller(None)
    _controller.set_id_vin(CAR_ID, VIN)

    _data = _mock.data_request_vehicle()
    _sensor = ChargeStateDataSensor(_data, _controller)
    _vehicle_data = "charge_state"
    _controller.set_charging_params(vin=VIN, params=_data[_vehicle_data])

    await _sensor.async_update()

    assert _sensor is not None
    assert _sensor.get_value() == VIN
    assert _sensor.enabled_by_default is False
    assert _sensor.attrs == _data[_vehicle_data]


@pytest.mark.asyncio
async def test_climate_state_data_sensor(monkeypatch):
    """Test climate state data sensor."""

    _mock = TeslaMock(monkeypatch)
    _controller = Controller(None)
    _controller.set_id_vin(CAR_ID, VIN)

    _data = _mock.data_request_vehicle()
    _sensor = ClimateStateDataSensor(_data, _controller)
    _vehicle_data = "climate_state"
    _controller.set_climate_params(vin=VIN, params=_data[_vehicle_data])

    await _sensor.async_update()

    assert _sensor is not None
    assert _sensor.get_value() == VIN
    assert _sensor.enabled_by_default is False
    assert _sensor.attrs == _data[_vehicle_data]


@pytest.mark.asyncio
async def test_drive_state_data_sensor(monkeypatch):
    """Test drive state data sensor."""

    _mock = TeslaMock(monkeypatch)
    _controller = Controller(None)
    _controller.set_id_vin(CAR_ID, VIN)

    _data = _mock.data_request_vehicle()
    _sensor = DriveStateDataSensor(_data, _controller)
    _vehicle_data = "drive_state"
    _controller.set_drive_params(vin=VIN, params=_data[_vehicle_data])

    await _sensor.async_update()

    assert _sensor is not None
    assert _sensor.get_value() == VIN
    assert _sensor.enabled_by_default is False
    assert _sensor.attrs == _data[_vehicle_data]


@pytest.mark.asyncio
async def test_gui_settings_data_sensor(monkeypatch):
    """Test gui settings data sensor."""

    _mock = TeslaMock(monkeypatch)
    _controller = Controller(None)
    _controller.set_id_vin(CAR_ID, VIN)

    _data = _mock.data_request_vehicle()
    _sensor = GuiSettingsDataSensor(_data, _controller)
    _vehicle_data = "gui_settings"
    _controller.set_gui_params(vin=VIN, params=_data[_vehicle_data])

    await _sensor.async_update()

    assert _sensor is not None
    assert _sensor.get_value() == VIN
    assert _sensor.enabled_by_default is False
    assert _sensor.attrs == _data[_vehicle_data]


@pytest.mark.asyncio
async def test_software_data_sensor(monkeypatch):
    """Test software data sensor."""

    _mock = TeslaMock(monkeypatch)
    _controller = Controller(None)
    _controller.set_id_vin(CAR_ID, VIN)

    _data = _mock.data_request_vehicle()
    _sensor = SoftwareDataSensor(_data, _controller)
    _vehicle_data = "vehicle_state"
    _controller.set_state_params(vin=VIN, params=_data[_vehicle_data])

    await _sensor.async_update()

    assert _sensor is not None
    assert _sensor.get_value() == VIN
    assert _sensor.enabled_by_default is False
    assert _sensor.attrs == _data[_vehicle_data]["software_update"]


@pytest.mark.asyncio
async def test_speed_limit_data_sensor(monkeypatch):
    """Test speed limit data sensor."""

    _mock = TeslaMock(monkeypatch)
    _controller = Controller(None)
    _controller.set_id_vin(CAR_ID, VIN)

    _data = _mock.data_request_vehicle()
    _sensor = SpeedLimitDataSensor(_data, _controller)
    _vehicle_data = "vehicle_state"
    _controller.set_state_params(vin=VIN, params=_data[_vehicle_data])

    await _sensor.async_update()

    assert _sensor is not None
    assert _sensor.get_value() == VIN
    assert _sensor.enabled_by_default is False
    assert _sensor.attrs == _data[_vehicle_data]["speed_limit_mode"]


@pytest.mark.asyncio
async def test_vehicle_config_data_sensor(monkeypatch):
    """Test vehicle config sensor."""

    _mock = TeslaMock(monkeypatch)
    _controller = Controller(None)
    _controller.set_id_vin(CAR_ID, VIN)

    _data = _mock.data_request_vehicle()
    _sensor = VehicleConfigDataSensor(_data, _controller)
    _vehicle_data = "vehicle_config"
    _controller.set_config_params(vin=VIN, params=_data[_vehicle_data])

    await _sensor.async_update()

    assert _sensor is not None
    assert _sensor.get_value() == VIN
    assert _sensor.enabled_by_default is False
    assert _sensor.attrs == _data[_vehicle_data]


@pytest.mark.asyncio
async def test_vehicle_state_data_sensor(monkeypatch):
    """Test vehicle state data sensor."""

    _mock = TeslaMock(monkeypatch)
    _controller = Controller(None)
    _controller.set_id_vin(CAR_ID, VIN)

    _data = _mock.data_request_vehicle()
    _sensor = VehicleStateDataSensor(_data, _controller)
    _vehicle_data = "vehicle_state"
    _vehicle_state_data: dict = copy.deepcopy(_data[_vehicle_data])

    _controller.set_state_params(vin=VIN, params=_data[_vehicle_data])

    await _sensor.async_update()

    del _vehicle_state_data["speed_limit_mode"]
    del _vehicle_state_data["software_update"]
    del _vehicle_state_data["media_state"]
    _vehicle_state_data.update({"media_state_remote_control_enabled": True})

    assert _sensor is not None
    assert _sensor.get_value() == VIN
    assert _sensor.enabled_by_default is False
    assert _sensor.attrs == _vehicle_state_data
