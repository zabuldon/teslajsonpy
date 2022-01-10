"""Test sentry mode switch."""

import pytest
import time

from teslajsonpy.controller import Controller
from teslajsonpy.homeassistant.sentry_mode import SentryModeSwitch

from tests.tesla_mock import TeslaMock, VIN, CAR_ID

LAST_UPDATE_TIME = time.time()


def test_has_battery(monkeypatch):
    """Test has_battery()."""

    _mock = TeslaMock(monkeypatch)
    _controller = Controller(None)

    _data = _mock.data_request_vehicle()
    _switch = SentryModeSwitch(_data, _controller)

    assert not _switch.has_battery()


def test_available_true(monkeypatch):
    """Test available() when flag sentry_mode_available is false."""

    _mock = TeslaMock(monkeypatch)
    _controller = Controller(None)
    _controller.set_id_vin(CAR_ID, VIN)
    _controller.set_last_update_time(vin=VIN, timestamp=LAST_UPDATE_TIME)

    _data = _mock.data_request_vehicle()
    _data["vehicle_state"]["sentry_mode_available"] = True
    _switch = SentryModeSwitch(_data, _controller)

    _controller.set_state_params(vin=VIN, params=_data["vehicle_state"])

    assert _switch.available()


def test_available_false(monkeypatch):
    """Test available() when flag sentry_mode_available is false."""

    _mock = TeslaMock(monkeypatch)
    _controller = Controller(None)
    _controller.set_id_vin(CAR_ID, VIN)
    _controller.set_last_update_time(vin=VIN, timestamp=LAST_UPDATE_TIME)

    _data = _mock.data_request_vehicle()
    _data["vehicle_state"]["sentry_mode_available"] = False
    _switch = SentryModeSwitch(_data, _controller)

    _controller.set_state_params(vin=VIN, params=_data["vehicle_state"])

    assert not _switch.available()


def test_is_on_false(monkeypatch):
    """Test is_on() when flag sentry_mode is false."""

    _mock = TeslaMock(monkeypatch)
    _controller = Controller(None)
    _controller.set_id_vin(CAR_ID, VIN)
    _controller.set_last_update_time(vin=VIN, timestamp=LAST_UPDATE_TIME)

    _data = _mock.data_request_vehicle()
    _data["vehicle_state"]["sentry_mode_available"] = True
    _data["vehicle_state"]["sentry_mode"] = False
    _switch = SentryModeSwitch(_data, _controller)

    _controller.set_state_params(vin=VIN, params=_data["vehicle_state"])

    assert not _switch.is_on()


def test_is_on_true(monkeypatch):
    """Test is_on() when flag sentry_mode is true."""

    _mock = TeslaMock(monkeypatch)
    _controller = Controller(None)
    _controller.set_id_vin(CAR_ID, VIN)
    _controller.set_last_update_time(vin=VIN, timestamp=LAST_UPDATE_TIME)

    _data = _mock.data_request_vehicle()
    _data["vehicle_state"]["sentry_mode_available"] = True
    _data["vehicle_state"]["sentry_mode"] = True
    _switch = SentryModeSwitch(_data, _controller)

    _controller.set_state_params(vin=VIN, params=_data["vehicle_state"])

    assert _switch.is_on()


def test_is_on_unavailable(monkeypatch):
    """Test is_on() when flag sentry_mode_available is false."""

    _mock = TeslaMock(monkeypatch)
    _controller = Controller(None)
    _controller.set_id_vin(CAR_ID, VIN)
    _controller.set_last_update_time(vin=VIN, timestamp=LAST_UPDATE_TIME)

    _data = _mock.data_request_vehicle()
    _data["vehicle_state"]["sentry_mode_available"] = False
    _data["vehicle_state"]["sentry_mode"] = True
    _switch = SentryModeSwitch(_data, _controller)

    _controller.set_state_params(vin=VIN, params=_data["vehicle_state"])

    assert not _switch.is_on()


@pytest.mark.asyncio
async def test_enable_sentry_mode(monkeypatch):
    """Test enable_sentry_mode()."""

    _mock = TeslaMock(monkeypatch)
    _controller = Controller(None)
    _controller.set_id_vin(CAR_ID, VIN)
    _controller.set_last_update_time(vin=VIN, timestamp=LAST_UPDATE_TIME)

    _data = _mock.data_request_vehicle()
    _data["vehicle_state"]["sentry_mode_available"] = True
    _data["vehicle_state"]["sentry_mode"] = False
    _switch = SentryModeSwitch(_data, _controller)

    _controller.set_state_params(vin=VIN, params=_data["vehicle_state"])

    await _switch.enable_sentry_mode()
    assert _switch.is_on()


@pytest.mark.asyncio
async def test_enable_sentry_mode_already_enabled(monkeypatch):
    """Test enable_sentry_mode() when already enabled."""

    _mock = TeslaMock(monkeypatch)
    _controller = Controller(None)
    _controller.set_id_vin(CAR_ID, VIN)
    _controller.set_last_update_time(vin=VIN, timestamp=LAST_UPDATE_TIME)

    _data = _mock.data_request_vehicle()
    _data["vehicle_state"]["sentry_mode_available"] = True
    _data["vehicle_state"]["sentry_mode"] = True
    _switch = SentryModeSwitch(_data, _controller)

    _controller.set_state_params(vin=VIN, params=_data["vehicle_state"])

    await _switch.enable_sentry_mode()
    assert _switch.is_on()


@pytest.mark.asyncio
async def test_enable_sentry_mode_not_available(monkeypatch):
    """Test enable_sentry_mode() when sentry mode is not available."""

    _mock = TeslaMock(monkeypatch)
    _controller = Controller(None)
    _controller.set_id_vin(CAR_ID, VIN)
    _controller.set_last_update_time(vin=VIN, timestamp=LAST_UPDATE_TIME)

    _data = _mock.data_request_vehicle()
    _data["vehicle_state"]["sentry_mode_available"] = False
    _data["vehicle_state"]["sentry_mode"] = False
    _switch = SentryModeSwitch(_data, _controller)

    _controller.set_state_params(vin=VIN, params=_data["vehicle_state"])

    await _switch.enable_sentry_mode()
    assert not _switch.is_on()


@pytest.mark.asyncio
async def test_disable_sentry_mode(monkeypatch):
    """Test disable_sentry_mode()."""

    _mock = TeslaMock(monkeypatch)
    _controller = Controller(None)
    _controller.set_id_vin(CAR_ID, VIN)
    _controller.set_last_update_time(vin=VIN, timestamp=LAST_UPDATE_TIME)

    _data = _mock.data_request_vehicle()
    _data["vehicle_state"]["sentry_mode_available"] = True
    _data["vehicle_state"]["sentry_mode"] = True
    _switch = SentryModeSwitch(_data, _controller)

    _controller.set_state_params(vin=VIN, params=_data["vehicle_state"])

    await _switch.disable_sentry_mode()
    assert not _switch.is_on()


@pytest.mark.asyncio
async def test_disable_sentry_mode_already_disabled(monkeypatch):
    """Test disable_sentry_mode() when already disabled."""

    _mock = TeslaMock(monkeypatch)
    _controller = Controller(None)
    _controller.set_id_vin(CAR_ID, VIN)
    _controller.set_last_update_time(vin=VIN, timestamp=LAST_UPDATE_TIME)

    _data = _mock.data_request_vehicle()
    _data["vehicle_state"]["sentry_mode_available"] = True
    _data["vehicle_state"]["sentry_mode"] = False
    _switch = SentryModeSwitch(_data, _controller)

    _controller.set_state_params(vin=VIN, params=_data["vehicle_state"])

    await _switch.disable_sentry_mode()
    assert not _switch.is_on()


@pytest.mark.asyncio
async def test_disable_sentry_mode_not_available(monkeypatch):
    """Test disable_sentry_mode() when sentry mode is not available."""

    _mock = TeslaMock(monkeypatch)
    _controller = Controller(None)
    _controller.set_id_vin(CAR_ID, VIN)
    _controller.set_last_update_time(vin=VIN, timestamp=LAST_UPDATE_TIME)

    _data = _mock.data_request_vehicle()
    _data["vehicle_state"]["sentry_mode_available"] = False
    _data["vehicle_state"]["sentry_mode"] = False
    _switch = SentryModeSwitch(_data, _controller)

    _controller.set_state_params(vin=VIN, params=_data["vehicle_state"])

    await _switch.enable_sentry_mode()
    assert not _switch.is_on()


@pytest.mark.asyncio
async def test_async_update(monkeypatch):
    """Test async_update()."""

    _mock = TeslaMock(monkeypatch)
    _controller = Controller(None)
    _controller.set_id_vin(CAR_ID, VIN)
    _controller.set_last_update_time(vin=VIN, timestamp=LAST_UPDATE_TIME)

    _data = _mock.data_request_vehicle()
    _data["vehicle_state"]["sentry_mode_available"] = True
    _data["vehicle_state"]["sentry_mode"] = False
    _switch = SentryModeSwitch(_data, _controller)

    _controller.set_state_params(vin=VIN, params=_data["vehicle_state"])

    await _switch.async_update()
    assert not _switch.is_on()


@pytest.mark.asyncio
async def test_async_update_with_change(monkeypatch):
    """Test async_update() with a state change."""

    _mock = TeslaMock(monkeypatch)
    _controller = Controller(None)
    _controller.set_id_vin(CAR_ID, VIN)
    _controller.set_last_update_time(vin=VIN, timestamp=LAST_UPDATE_TIME)

    _data = _mock.data_request_vehicle()
    _data["vehicle_state"]["sentry_mode_available"] = True
    _data["vehicle_state"]["sentry_mode"] = False
    _switch = SentryModeSwitch(_data, _controller)

    # Change state value
    _data["vehicle_state"]["sentry_mode"] = True

    _controller.set_state_params(vin=VIN, params=_data["vehicle_state"])

    await _switch.async_update()
    assert _switch.is_on()


@pytest.mark.asyncio
async def test_async_update_with_change_but_not_available(monkeypatch):
    """Test async_update() with a state change, but sentry mode is not available."""

    _mock = TeslaMock(monkeypatch)
    _controller = Controller(None)
    _controller.set_id_vin(CAR_ID, VIN)
    _controller.set_last_update_time(vin=VIN, timestamp=LAST_UPDATE_TIME)

    _data = _mock.data_request_vehicle()
    _data["vehicle_state"]["sentry_mode_available"] = False
    _data["vehicle_state"]["sentry_mode"] = False
    _switch = SentryModeSwitch(_data, _controller)

    # Change state value
    _data["vehicle_state"]["sentry_mode"] = True

    _controller.set_state_params(vin=VIN, params=_data["vehicle_state"])

    await _switch.async_update()
    assert not _switch.is_on()


@pytest.mark.asyncio
async def test_async_update_with_change_same_value(monkeypatch):
    """Test async_update() with a state change, using same value."""

    _mock = TeslaMock(monkeypatch)
    _controller = Controller(None)
    _controller.set_id_vin(CAR_ID, VIN)
    _controller.set_last_update_time(vin=VIN, timestamp=LAST_UPDATE_TIME)

    _data = _mock.data_request_vehicle()
    _data["vehicle_state"]["sentry_mode_available"] = True
    _data["vehicle_state"]["sentry_mode"] = True
    _switch = SentryModeSwitch(_data, _controller)

    # Change state value
    _data["vehicle_state"]["sentry_mode"] = True

    _controller.set_state_params(vin=VIN, params=_data["vehicle_state"])

    await _switch.async_update()
    assert _switch.is_on()
