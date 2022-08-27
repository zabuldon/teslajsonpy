"""Test power sensor."""

import pytest

from teslajsonpy.controller import Controller

from tests.tesla_mock import TeslaMock


@pytest.mark.asyncio
async def test_energysite_setup(monkeypatch):
    """Test setup of energysites in Controller.connect()."""
    TeslaMock(monkeypatch)
    _controller = Controller(None)
    await _controller.connect()

    solar_site = _controller.energysites[12345]
    powerwall_site = _controller.energysites[67890]

    assert _controller.energysites is not None
    assert solar_site.resource_type == "solar"
    assert powerwall_site.resource_type == "battery"


@pytest.mark.asyncio
async def test_solar_site(monkeypatch):
    """Test SolarSite class."""
    TeslaMock(monkeypatch)
    _controller = Controller(None)
    await _controller.connect()

    _solar_site = _controller.energysites[12345]

    assert _solar_site._api is not None
    assert _solar_site._energysite is not None
    assert _solar_site._power_data == {
        "solar_power": 0,
        "load_power": 0,
        "grid_power": 0,
        "battery_power": 0,
    }

    assert _solar_site.energysite_id == 12345
    assert _solar_site.has_load_meter
    assert _solar_site.id == "313dbc37-555c-45b1-83aa-62a4ef9ff7ac"
    assert _solar_site.resource_type == "solar"
    assert _solar_site.site_name == "My Solar Home"

    assert _solar_site.grid_power == 0
    assert _solar_site.load_power == 0
    assert _solar_site.solar_power == 0
    assert _solar_site.solar_type == "pv_panel"


@pytest.mark.asyncio
async def test_powerwall_site(monkeypatch):
    """Test PowerwallSite class."""
    TeslaMock(monkeypatch)
    _controller = Controller(None)
    await _controller.connect()

    _solar_powerwall_site = _controller.energysites[67890]

    assert _solar_powerwall_site._api is not None
    assert _solar_powerwall_site._energysite is not None
    assert _solar_powerwall_site._power_data == {
        "solar_power": 0,
        "load_power": 0,
        "grid_power": 0,
        "battery_power": 0,
    }

    assert _solar_powerwall_site.energysite_id == 67890
    assert _solar_powerwall_site.has_load_meter
    assert _solar_powerwall_site.id == "212dbc27-333c-45b1-81bb-31e2zd2fs2cm"
    assert _solar_powerwall_site.resource_type == "battery"
    assert _solar_powerwall_site.site_name == "My Battery Home"

    # assert _solar_powerwall_site.battery_percent == 0
    # assert _solar_powerwall_site.battery_power == 0
    assert _solar_powerwall_site.grid_power == 0
    assert _solar_powerwall_site.load_power == 0
    assert _solar_powerwall_site.solar_power == 0
    assert _solar_powerwall_site.solar_type == "pv_panel"


# @pytest.mark.asyncio
# async def test_solar_power_sensor(monkeypatch):
#     """Test SolarPowerSensor class."""
#     _mock = TeslaMock(monkeypatch)
#     _controller = Controller(None)
#     # Test a solar only site (no Powerwall)
#     _data = _mock.data_request_solar_combined_data()
#     _sensor = SolarPowerSensor(_data, _controller)

#     assert _sensor.name == f"{_sensor._site_name} {_sensor.type}"
#     assert _sensor.get_power() == 7720
#     # Test a battery site (Powerwall)
#     _data = _mock.data_request_battery_combined_data()
#     _sensor = SolarPowerSensor(_data, _controller)

#     assert _sensor.name == f"{_sensor._site_name} {_sensor.type}"
#     assert _sensor.get_power() == 7720


# @pytest.mark.asyncio
# async def test_load_power_sensor(monkeypatch):
#     """Test LoadPowerSensor class."""
#     _mock = TeslaMock(monkeypatch)
#     _controller = Controller(None)
#     # Test a solar only site (no Powerwall)
#     _data = _mock.data_request_solar_combined_data()
#     _sensor = LoadPowerSensor(_data, _controller)

#     assert _sensor.name == f"{_sensor._site_name} {_sensor.type}"
#     assert _sensor.get_power() == 4517.14990234375
#     # Test a battery site (Powerwall)
#     _data = _mock.data_request_battery_combined_data()
#     _sensor = LoadPowerSensor(_data, _controller)

#     assert _sensor.name == f"{_sensor._site_name} {_sensor.type}"
#     assert _sensor.get_power() == 4517.14990234375


# @pytest.mark.asyncio
# async def test_grid_power_sensor(monkeypatch):
#     """Test GridPowerSensor class."""
#     _mock = TeslaMock(monkeypatch)
#     _controller = Controller(None)
#     # Test a solar only site (no Powerwall)
#     _data = _mock.data_request_solar_combined_data()
#     _sensor = GridPowerSensor(_data, _controller)

#     assert _sensor.name == f"{_sensor._site_name} {_sensor.type}"
#     assert _sensor.get_power() == -3202.85009765625
#     # Test a battery site (Powerwall)
#     _data = _mock.data_request_battery_combined_data()
#     _sensor = GridPowerSensor(_data, _controller)

#     assert _sensor.name == f"{_sensor._site_name} {_sensor.type}"
#     assert _sensor.get_power() == -3202.85009765625


# @pytest.mark.asyncio
# async def test_battery_power_sensor(monkeypatch):
#     """Test BatteryPowerSensor class."""
#     _mock = TeslaMock(monkeypatch)
#     _controller = Controller(None)
#     _data = _mock.data_request_battery_combined_data()
#     _sensor = BatteryPowerSensor(_data, _controller)

#     assert _sensor.name == f"{_sensor._site_name} {_sensor.type}"
#     assert _sensor.get_power() == 0


# def test_site_without_name(monkeypatch):
#     """Test site with no site_name in json data."""
#     _mock = TeslaMock(monkeypatch)
#     _controller = Controller(None)
#     _data = _mock.data_request_solar_combined_data_no_name()
#     _sensor = LoadPowerSensor(_data, _controller)

#     assert _sensor.site_name() == "My Home"


# @pytest.mark.asyncio
# async def test_get_power_after_update(monkeypatch):
#     """Test get_power() after an update."""
#     _mock = TeslaMock(monkeypatch)
#     _controller = Controller(None)
#     _data = _mock.data_request_solar_combined_data()
#     _data["solar_power"] = 1800
#     _data["load_power"] = 1800
#     _data["grid_power"] = 1800

#     _sensor = SolarPowerSensor(_data, _controller)

#     await _sensor.async_update()
#     assert _sensor.get_power() == 7720

#     _sensor = LoadPowerSensor(_data, _controller)

#     await _sensor.async_update()
#     assert _sensor.get_power() == 4517.14990234375

#     _sensor = GridPowerSensor(_data, _controller)

#     await _sensor.async_update()
#     assert _sensor.get_power() == -3202.85009765625


# @pytest.mark.asyncio
# async def test_get_power_after_update_with_unknown_status(monkeypatch):
#     """Test get_power() after an update with unknown grid status."""
#     _mock = TeslaMock(monkeypatch)
#     monkeypatch.setattr(
#         Controller, "get_power_params", _mock.mock_get_power_unknown_grid_params
#     )
#     _controller = Controller(None)
#     _data = _mock.data_request_solar_combined_data()
#     _sensor = SolarPowerSensor(_data, _controller)

#     await _sensor.async_update()
#     assert _sensor.get_power() == 1750
