"""Test charger switch."""

import pytest

from teslajsonpy.controller import Controller
from teslajsonpy.homeassistant.charger import ChargerSwitch

from tests.tesla_mock import TeslaMock


def test_has_battery(monkeypatch):
    """Test has_battery()."""

    _mock = TeslaMock(monkeypatch)
    _controller = Controller(None)

    _data = _mock.data_request_vehicle()
    _switch = ChargerSwitch(_data, _controller)

    assert not _switch.has_battery()


def test_is_charging_on_init(monkeypatch):
    """Test is_charging() when not charging."""

    _mock = TeslaMock(monkeypatch)
    _controller = Controller(None)

    _data = _mock.data_request_vehicle()
    _switch = ChargerSwitch(_data, _controller)

    assert not _switch.is_charging()


@pytest.mark.asyncio
async def test_is_charging_on(monkeypatch):
    """Test is_charging() with charging state charging."""

    _mock = TeslaMock(monkeypatch)
    _controller = Controller(None)

    _data = _mock.data_request_vehicle()
    _data["charge_state"]["charging_state"] = "Charging"
    _switch = ChargerSwitch(_data, _controller)

    await _switch.async_update()
    assert _switch.is_charging()


@pytest.mark.asyncio
async def test_is_charging_off(monkeypatch):
    """Test is_charging() with charging state disconnected."""

    _mock = TeslaMock(monkeypatch)
    _controller = Controller(None)

    _data = _mock.data_request_vehicle()
    _data["charge_state"]["charging_state"] = "Disconnected"
    _switch = ChargerSwitch(_data, _controller)

    await _switch.async_update()
    assert not _switch.is_charging()


@pytest.mark.asyncio
async def test_start_charge(monkeypatch):
    """Test start_charge()."""

    _mock = TeslaMock(monkeypatch)
    _controller = Controller(None)

    _data = _mock.data_request_vehicle()
    _data["charge_state"]["charging_state"] = "Disconnected"
    _switch = ChargerSwitch(_data, _controller)
    await _switch.async_update()

    await _switch.start_charge()
    assert _switch.is_charging()


@pytest.mark.asyncio
async def test_stop_charge(monkeypatch):
    """Test stop_charge()."""

    _mock = TeslaMock(monkeypatch)
    _controller = Controller(None)

    _data = _mock.data_request_vehicle()
    _data["charge_state"]["charging_state"] = "Charging"
    _switch = ChargerSwitch(_data, _controller)
    await _switch.async_update()

    await _switch.stop_charge()
    assert not _switch.is_charging()


@pytest.mark.asyncio
async def test_async_update(monkeypatch):
    """Test async_update()."""

    _mock = TeslaMock(monkeypatch)
    _controller = Controller(None)

    _data = _mock.data_request_vehicle()
    _data["charge_state"]["charging_state"] = "Charging"
    _switch = ChargerSwitch(_data, _controller)

    await _switch.async_update()
    assert _switch.is_charging()


@pytest.mark.asyncio
async def test_async_update_with_change(monkeypatch):
    """Test async_update()."""

    _mock = TeslaMock(monkeypatch)
    _controller = Controller(None)

    _data = _mock.data_request_vehicle()
    _data["charge_state"]["charging_state"] = "Charging"
    _switch = ChargerSwitch(_data, _controller)

    _data["charge_state"]["charging_state"] = "Disconnected"
    await _switch.async_update()
    assert not _switch.is_charging()
