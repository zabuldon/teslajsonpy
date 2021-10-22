"""Test power sensor."""

import pytest

from teslajsonpy.controller import Controller
from teslajsonpy.const import TESLA_DEFAULT_ENERGY_SITE_NAME
from teslajsonpy.homeassistant.power import PowerSensor

from tests.tesla_mock import TeslaMock


def test_device_class(monkeypatch):
    """Test device_class()."""

    _mock = TeslaMock(monkeypatch)
    _controller = Controller(None)

    _data = _mock.data_request_energy_site()
    _sensor = PowerSensor(_data, _controller)

    assert _sensor.device_class == "power"

def test_device_no_name(monkeypatch):
    """Test device_class()."""

    _mock = TeslaMock(monkeypatch)
    _controller = Controller(None)

    _data = _mock.data_request_energy_site_no_name()
    _sensor = PowerSensor(_data, _controller)

    assert _sensor.site_name() == TESLA_DEFAULT_ENERGY_SITE_NAME


def test_get_power_on_init(monkeypatch):
    """Test get_power() after initialization."""

    _mock = TeslaMock(monkeypatch)
    _controller = Controller(None)

    _data = _mock.data_request_energy_site()
    _sensor = PowerSensor(_data, _controller)

    assert _sensor is not None
    assert _sensor.get_power() is None


@pytest.mark.asyncio
async def test_get_power_after_update(monkeypatch):
    """Test get_power()  after an update."""

    _mock = TeslaMock(monkeypatch)
    _controller = Controller(None)

    _data = _mock.data_request_energy_site()
    _data["solar_power"] = 1800
    _sensor = PowerSensor(_data, _controller)

    await _sensor.async_update()

    assert _sensor is not None
    assert not _sensor.get_power() is None
    assert _sensor.get_power() == 1800
