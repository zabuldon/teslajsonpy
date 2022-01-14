"""Test charging sensor."""

import pytest

from teslajsonpy.controller import Controller
from teslajsonpy.homeassistant.charger import ChargingSensor, ChargingEnergySensor

from tests.tesla_mock import TeslaMock, VIN, CAR_ID


def test_has_battery(monkeypatch):
    """Test has_battery()."""

    _mock = TeslaMock(monkeypatch)
    _controller = Controller(None)

    _data = _mock.data_request_vehicle()
    _sensor = ChargingSensor(_data, _controller)

    assert not _sensor.has_battery()


def test_device_class(monkeypatch):
    """Test device_class()."""

    _mock = TeslaMock(monkeypatch)
    _controller = Controller(None)

    _data = _mock.data_request_vehicle()
    _sensor = ChargingSensor(_data, _controller)

    assert _sensor.device_class is None


def test_state_class(monkeypatch):
    """Test device_class()."""

    _mock = TeslaMock(monkeypatch)
    _controller = Controller(None)

    _data = _mock.data_request_vehicle()
    _sensor = ChargingSensor(_data, _controller)

    assert _sensor.device_class is None

    _sensor2 = ChargingEnergySensor(_data, _controller)
    assert _sensor2.device_class == "energy"


def test_get_value_on_init(monkeypatch):
    """Test get_value() after initialization."""

    _mock = TeslaMock(monkeypatch)
    _controller = Controller(None)

    _data = _mock.data_request_vehicle()
    sensors = [
        ChargingSensor(_data, _controller),
        ChargingEnergySensor(_data, _controller),
    ]

    for _sensor in sensors:

        assert _sensor is not None
        assert _sensor.charging_rate is None
        assert _sensor.time_left is None
        assert _sensor.added_range is None
        assert _sensor.charge_current_request is None
        assert _sensor.charge_current_request_max is None
        assert _sensor.charger_actual_current is None
        assert _sensor.charger_voltage is None
        assert _sensor.charger_power is None
        assert _sensor.charge_energy_added is None
        assert _sensor.charge_limit_soc is None


@pytest.mark.asyncio
async def test_get_value_after_update(monkeypatch):
    """Test get_value() after an update."""

    _mock = TeslaMock(monkeypatch)
    _controller = Controller(None)
    _controller.set_id_vin(CAR_ID, VIN)

    _data = _mock.data_request_vehicle()
    _sensor = ChargingSensor(_data, _controller)
    _sensor2 = ChargingEnergySensor(_data, _controller)

    _controller.set_charging_params(vin=VIN, params=_data["charge_state"])

    await _sensor.async_update()

    assert _sensor is not None
    assert _sensor.charging_rate == 0
    assert _sensor.time_left == 0
    assert _sensor.added_range == 40
    assert _sensor.charge_current_request == 48
    assert _sensor.charge_current_request_max == 48
    assert _sensor.charger_actual_current == 0
    assert _sensor.charger_voltage == 0
    assert _sensor.charger_power == 0
    assert _sensor.charge_energy_added == 12.41
    assert _sensor.charge_limit_soc == 90
    assert _sensor.device_class is None

    _sensor2 = ChargingEnergySensor(_data, _controller)
    await _sensor2.async_update()

    assert _sensor2 is not None
    assert _sensor2.charging_rate == 0
    assert _sensor2.time_left == 0
    assert _sensor2.charge_current_request == 48
    assert _sensor2.charge_current_request_max == 48
    assert _sensor2.charger_actual_current == 0
    assert _sensor2.charger_voltage == 0
    assert _sensor2.charger_power == 0
    assert _sensor2.charge_energy_added == 12.41
    assert _sensor2.charge_limit_soc == 90
    assert _sensor2.last_reset != 0
    assert _sensor2.state_class == "total_increasing"
    assert _sensor2.device_class == "energy"


@pytest.mark.asyncio
async def test_async_update(monkeypatch):
    """Test async_update()."""

    _mock = TeslaMock(monkeypatch)
    _controller = Controller(None)
    _controller.set_id_vin(CAR_ID, VIN)

    _data = _mock.data_request_vehicle()
    _sensor = ChargingSensor(_data, _controller)

    _controller.set_charging_params(vin=VIN, params=_data["charge_state"])

    await _sensor.async_update()

    assert _sensor is not None
    assert _sensor.charging_rate == 0
    assert _sensor.time_left == 0
    assert _sensor.added_range == 40
    assert _sensor.charge_current_request == 48
    assert _sensor.charge_current_request_max == 48
    assert _sensor.charger_actual_current == 0
    assert _sensor.charger_voltage == 0
    assert _sensor.charge_energy_added == 12.41
    assert _sensor.charge_limit_soc == 90


@pytest.mark.asyncio
async def test_async_update_in_kmh(monkeypatch):
    """Test async_update() for units in km/h."""

    _mock = TeslaMock(monkeypatch)
    _controller = Controller(None)
    _controller.set_id_vin(CAR_ID, VIN)

    _data = _mock.data_request_vehicle()
    _data["gui_settings"]["gui_distance_units"] = "km/hr"
    _data["gui_settings"]["gui_range_display"] = "Rated"
    _data["charge_state"]["charge_rate"] = 22
    _data["charge_state"]["charge_miles_added_rated"] = 44
    _sensor = ChargingSensor(_data, _controller)

    _controller.set_charging_params(vin=VIN, params=_data["charge_state"])
    _controller.set_gui_params(vin=VIN, params=_data["gui_settings"])

    await _sensor.async_update()

    assert _sensor is not None
    assert _sensor.charging_rate == 35.41
    assert _sensor.added_range == 70.81


@pytest.mark.asyncio
async def test_async_update_in_mph(monkeypatch):
    """Test async_update() for units in mph."""

    _mock = TeslaMock(monkeypatch)
    _controller = Controller(None)
    _controller.set_id_vin(CAR_ID, VIN)

    _data = _mock.data_request_vehicle()
    _data["gui_settings"]["gui_distance_units"] = "mi/hr"
    _data["gui_settings"]["gui_range_display"] = "Rated"
    _data["charge_state"]["charge_rate"] = 22
    _data["charge_state"]["charge_miles_added_rated"] = 44
    _data["charge_state"]["charger_power"] = 100.2
    _sensor = ChargingSensor(_data, _controller)

    _controller.set_charging_params(vin=VIN, params=_data["charge_state"])
    _controller.set_gui_params(vin=VIN, params=_data["gui_settings"])

    await _sensor.async_update()

    assert _sensor is not None
    assert _sensor.charging_rate == 22
    assert _sensor.added_range == 44
    assert _sensor.charger_power == 100.2


@pytest.mark.asyncio
async def test_async_update_charger_power(monkeypatch):
    """Test async_update() for charger_power."""

    _mock = TeslaMock(monkeypatch)
    _controller = Controller(None)
    _controller.set_id_vin(CAR_ID, VIN)

    _data = _mock.data_request_vehicle()
    _data["charge_state"]["charger_power"] = 100.2
    _sensor = ChargingSensor(_data, _controller)

    _controller.set_charging_params(vin=VIN, params=_data["charge_state"])

    await _sensor.async_update()

    assert _sensor.charger_power == 100.2
