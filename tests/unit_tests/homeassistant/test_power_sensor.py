"""Test power sensor."""

import pytest

from teslajsonpy.controller import Controller
from teslajsonpy.homeassistant.power import PowerSensor, SolarPowerSensor, LoadPowerSensor, GridPowerSensor

from tests.tesla_mock import TeslaMock


def test_device_class(monkeypatch):
    """Test device_class()."""

    _mock = TeslaMock(monkeypatch)
    _controller = Controller(None)

    _data = _mock.data_request_energy_site()
    _sensor = PowerSensor(_data, _controller)

    assert _sensor.device_class == "power"

    _sensor = SolarPowerSensor(_data, _controller)

    assert _sensor.type == "solar panel"

    _sensor = LoadPowerSensor(_data, _controller)

    assert _sensor.type == "load power"

    _sensor = GridPowerSensor(_data, _controller)

    assert _sensor.type == "grid power"

def test_device_no_name(monkeypatch):
    """Test device_class()."""

    _mock = TeslaMock(monkeypatch)
    _controller = Controller(None)

    _data = _mock.data_request_energy_site_no_name()
    _sensor = PowerSensor(_data, _controller)

    assert _sensor.site_name() == "1234567890"


def test_get_solar_power_on_init(monkeypatch):
    """Test get_power() after initialization."""

    _mock = TeslaMock(monkeypatch)
    _controller = Controller(None)

    _data = _mock.data_request_energy_site()
    _sensor = SolarPowerSensor(_data, _controller)

    assert _sensor is not None
    assert _sensor.get_power() == 4230

def test_get_load_power_on_init(monkeypatch):
    """Test get_load_power() after initialization."""

    _mock = TeslaMock(monkeypatch)
    _controller = Controller(None)

    _data = _mock.data_request_energy_site()
    _sensor = LoadPowerSensor(_data, _controller)

    assert _sensor is not None
    assert _sensor.get_load_power() == 3245.4599609375

def test_get_grid_power_on_init(monkeypatch):
    """Test get_grid_power() after initialization."""

    _mock = TeslaMock(monkeypatch)
    _controller = Controller(None)

    _data = _mock.data_request_energy_site()
    _sensor = GridPowerSensor(_data, _controller)

    assert _sensor is not None
    assert _sensor.get_grid_power() == -984.5400390625

@pytest.mark.asyncio
async def test_get_power_after_update(monkeypatch):
    """Test get_power() after an update."""

    _mock = TeslaMock(monkeypatch)
    _controller = Controller(None)

    _data = _mock.data_request_energy_site()
    _data["solar_power"] = 1800
    _sensor = SolarPowerSensor(_data, _controller)

    await _sensor.async_update()

    assert _sensor is not None
    assert not _sensor.get_power() is None
    assert _sensor.get_power() == 7720

@pytest.mark.asyncio
async def test_get_load_power_after_update(monkeypatch):
    """Test get_load_power() after an update."""

    _mock = TeslaMock(monkeypatch)
    _controller = Controller(None)

    _data = _mock.data_request_energy_site()
    _data["load_power"] = 1800
    _sensor = LoadPowerSensor(_data, _controller)

    await _sensor.async_update()

    assert _sensor is not None
    assert not _sensor.get_load_power() is None
    assert _sensor.get_load_power() == 4517.14990234375

@pytest.mark.asyncio
async def test_get_grid_power_after_update(monkeypatch):
    """Test get_grid_power() after an update."""

    _mock = TeslaMock(monkeypatch)
    _controller = Controller(None)

    _data = _mock.data_request_energy_site()
    _data["grid_power"] = 1800
    _sensor = GridPowerSensor(_data, _controller)

    await _sensor.async_update()

    assert _sensor is not None
    assert not _sensor.get_grid_power() is None
    assert _sensor.get_grid_power() == -3202.85009765625

@pytest.mark.asyncio
async def test_get_power_after_update_with_unknown_status(monkeypatch):
    """Test get_power()  after an update with an unknown grid status."""

    _mock = TeslaMock(monkeypatch)
    monkeypatch.setattr(
        Controller, "get_power_params", _mock.mock_get_power_unknown_grid_params
    )
    _controller = Controller(None)

    _data = _mock.data_request_energy_site()
    _data["solar_power"] = 1800
    _sensor = SolarPowerSensor(_data, _controller)

    await _sensor.async_update()

    assert _sensor is not None
    assert not _sensor.get_power() is None
    assert _sensor.get_power() == 1750