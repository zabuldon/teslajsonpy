"""Test energy sites."""

import pytest

from teslajsonpy.const import DEFAULT_ENERGYSITE_NAME
from teslajsonpy.controller import Controller
from teslajsonpy.energy import EnergySite

from tests.tesla_mock import TeslaMock, ENERGYSITES, SITE_CONFIG


@pytest.mark.asyncio
async def test_energysite_setup(monkeypatch):
    """Test setup of energysites in Controller.connect()."""
    TeslaMock(monkeypatch)
    _controller = Controller(None)
    await _controller.connect()
    _controller.generate_energysite_objects()

    solar_site = _controller.energysites[12345]
    powerwall_site = _controller.energysites[67890]

    assert _controller.energysites is not None
    assert solar_site.resource_type == ENERGYSITES[0]["resource_type"]
    assert powerwall_site.resource_type == ENERGYSITES[1]["resource_type"]


@pytest.mark.asyncio
async def test_solar_site(monkeypatch):
    """Test SolarSite class."""
    TeslaMock(monkeypatch)
    _controller = Controller(None)
    await _controller.connect()
    _controller.generate_energysite_objects()

    _solar_site = _controller.energysites[12345]

    assert _solar_site._api is not None
    assert _solar_site._energysite is not None
    assert _solar_site._data == {
        "solar_power": 0,
        "load_power": 0,
        "grid_power": 0,
        "battery_power": 0,
        "percentage_charged": 0,
    }

    assert _solar_site.energysite_id == ENERGYSITES[0]["energy_site_id"]
    assert _solar_site.has_battery == ENERGYSITES[0]["components"]["battery"]
    assert _solar_site.has_load_meter == ENERGYSITES[0]["components"]["load_meter"]
    assert _solar_site.has_solar == ENERGYSITES[0]["components"]["solar"]
    assert _solar_site.id == ENERGYSITES[0]["id"]
    assert _solar_site.resource_type == ENERGYSITES[0]["resource_type"]
    assert _solar_site.site_name == SITE_CONFIG["site_name"]

    assert _solar_site.grid_power == 0
    assert _solar_site.load_power == 0
    assert _solar_site.solar_power == 0
    assert _solar_site.solar_type == ENERGYSITES[0]["components"]["solar_type"]


@pytest.mark.asyncio
async def test_powerwall_site(monkeypatch):
    """Test PowerwallSite class."""
    TeslaMock(monkeypatch)
    _controller = Controller(None)
    await _controller.connect()
    _controller.generate_energysite_objects()

    _solar_powerwall_site = _controller.energysites[67890]

    assert _solar_powerwall_site._api is not None
    assert _solar_powerwall_site._energysite is not None
    assert _solar_powerwall_site._data == {
        "solar_power": 0,
        "load_power": 0,
        "grid_power": 0,
        "battery_power": 0,
        "percentage_charged": 0,
    }

    assert _solar_powerwall_site.energysite_id == ENERGYSITES[1]["energy_site_id"]
    assert (
        _solar_powerwall_site.has_load_meter
        == ENERGYSITES[1]["components"]["load_meter"]
    )
    assert _solar_powerwall_site.id == ENERGYSITES[1]["id"]
    assert _solar_powerwall_site.has_battery == ENERGYSITES[1]["components"]["battery"]
    assert _solar_powerwall_site.has_solar == ENERGYSITES[1]["components"]["solar"]
    assert _solar_powerwall_site.resource_type == ENERGYSITES[1]["resource_type"]
    assert _solar_powerwall_site.site_name == ENERGYSITES[1]["site_name"]

    assert _solar_powerwall_site.percentage_charged == 0
    assert _solar_powerwall_site.battery_power == 0
    assert _solar_powerwall_site.grid_power == 0
    assert _solar_powerwall_site.load_power == 0
    assert _solar_powerwall_site.solar_power == 0
    assert (
        _solar_powerwall_site.solar_type == ENERGYSITES[1]["components"]["solar_type"]
    )


@pytest.mark.asyncio
async def test_energysite_with_no_name(monkeypatch):
    """Test EnergySite base class with no name."""
    _mock = TeslaMock(monkeypatch)
    _api = Controller(None)
    _energysite = _mock.data_request_energysites()[0]
    _energysite_data = _mock.controller_get_power_params()
    _sensor = EnergySite(_api, _energysite, _energysite_data)

    assert _sensor.site_name == DEFAULT_ENERGYSITE_NAME


@pytest.mark.asyncio
async def test_set_operation_mode(monkeypatch):
    """Test set operation mode."""
    TeslaMock(monkeypatch)
    _controller = Controller(None)
    await _controller.connect()
    _controller.generate_energysite_objects()
    _energysite = _controller.energysites[67890]

    assert await _energysite.set_operation_mode("autonomous") is None


@pytest.mark.asyncio
async def test_set_reserve_percent(monkeypatch):
    """Test set reserve percent."""
    TeslaMock(monkeypatch)
    _controller = Controller(None)
    await _controller.connect()
    _controller.generate_energysite_objects()
    _energysite = _controller.energysites[67890]

    assert await _energysite.set_reserve_percent(10) is None


@pytest.mark.asyncio
async def test_set_grid_charging(monkeypatch):
    """Test set grid charging."""
    TeslaMock(monkeypatch)
    _controller = Controller(None)
    await _controller.connect()
    _controller.generate_energysite_objects()
    _energysite = _controller.energysites[67890]

    assert await _energysite.set_grid_charging(True) is None


@pytest.mark.asyncio
async def test_set_export_rule(monkeypatch):
    """Test set export rule."""
    TeslaMock(monkeypatch)
    _controller = Controller(None)
    await _controller.connect()
    _controller.generate_energysite_objects()
    _energysite = _controller.energysites[67890]

    assert await _energysite.set_export_rule("pv_only") is None


# Test reponse with "grid_status" of "Unknown"
