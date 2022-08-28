"""Test energy sites."""

import pytest

from teslajsonpy.controller import Controller
from teslajsonpy.energy import EnergySite

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


@pytest.mark.asyncio
async def test_energysite_with_no_name(monkeypatch):
    """Test EnergySite base class with no name."""
    _mock = TeslaMock(monkeypatch)
    _api = Controller(None)
    _energysite = _mock.data_request_energysites()[0]
    _power_data = _mock.controller_get_power_params()
    _sensor = EnergySite(_api, _energysite, _power_data)

    assert _sensor.site_name == "My Home"


# Test reponse with "grid_status" of "Unknown"
