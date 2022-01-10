"""Test range switch."""

import pytest
import time

from teslajsonpy.controller import Controller
from teslajsonpy.homeassistant.charger import RangeSwitch

from tests.tesla_mock import TeslaMock, VIN, CAR_ID

LAST_UPDATE_TIME = time.time()


def test_has_battery(monkeypatch):
    """Test has_battery()."""

    _mock = TeslaMock(monkeypatch)
    _controller = Controller(None)

    _data = _mock.data_request_vehicle()
    _switch = RangeSwitch(_data, _controller)

    assert not _switch.has_battery()


def test_is_maxrange_on_init(monkeypatch):
    """Test is_maxrange() when not charging."""

    _mock = TeslaMock(monkeypatch)
    _controller = Controller(None)

    _data = _mock.data_request_vehicle()
    _switch = RangeSwitch(_data, _controller)

    assert not _switch.is_maxrange()


@pytest.mark.asyncio
async def test_is_maxrange_on(monkeypatch):
    """Test is_maxrange() with charging state charging."""

    _mock = TeslaMock(monkeypatch)
    _controller = Controller(None)
    _controller.set_id_vin(CAR_ID, VIN)
    _controller.set_last_update_time(vin=VIN, timestamp=LAST_UPDATE_TIME)

    _data = _mock.data_request_vehicle()
    _data["charge_state"]["charge_to_max_range"] = True
    _switch = RangeSwitch(_data, _controller)

    _controller.set_charging_params(car_id=CAR_ID, params=_data["charge_state"])

    await _switch.async_update()
    assert _switch.is_maxrange()


@pytest.mark.asyncio
async def test_is_maxrange_off(monkeypatch):
    """Test is_maxrange() with charging state disconnected."""

    _mock = TeslaMock(monkeypatch)
    _controller = Controller(None)
    _controller.set_id_vin(CAR_ID, VIN)
    _controller.set_last_update_time(vin=VIN, timestamp=LAST_UPDATE_TIME)

    _data = _mock.data_request_vehicle()
    _data["charge_state"]["charge_to_max_range"] = False
    _switch = RangeSwitch(_data, _controller)

    _controller.set_charging_params(car_id=CAR_ID, params=_data["charge_state"])

    await _switch.async_update()
    assert not _switch.is_maxrange()


@pytest.mark.asyncio
async def test_set_max(monkeypatch):
    """Test set_max()."""

    _mock = TeslaMock(monkeypatch)
    _controller = Controller(None)
    _controller.set_id_vin(CAR_ID, VIN)
    _controller.set_last_update_time(vin=VIN, timestamp=LAST_UPDATE_TIME)

    _data = _mock.data_request_vehicle()
    _data["charge_state"]["charge_to_max_range"] = False
    _switch = RangeSwitch(_data, _controller)

    _controller.set_charging_params(car_id=CAR_ID, params=_data["charge_state"])

    await _switch.async_update()

    await _switch.set_max()
    assert _switch.is_maxrange()


@pytest.mark.asyncio
async def test_set_standard(monkeypatch):
    """Test set_standard()."""

    _mock = TeslaMock(monkeypatch)
    _controller = Controller(None)
    _controller.set_id_vin(CAR_ID, VIN)
    _controller.set_last_update_time(vin=VIN, timestamp=LAST_UPDATE_TIME)

    _data = _mock.data_request_vehicle()
    _data["charge_state"]["charge_to_max_range"] = True
    _switch = RangeSwitch(_data, _controller)

    _controller.set_charging_params(car_id=CAR_ID, params=_data["charge_state"])

    await _switch.async_update()

    await _switch.set_standard()
    assert not _switch.is_maxrange()


@pytest.mark.asyncio
async def test_async_update(monkeypatch):
    """Test async_update()."""

    _mock = TeslaMock(monkeypatch)
    _controller = Controller(None)
    _controller.set_id_vin(CAR_ID, VIN)
    _controller.set_last_update_time(vin=VIN, timestamp=LAST_UPDATE_TIME)

    _data = _mock.data_request_vehicle()
    _data["charge_state"]["charge_to_max_range"] = True
    _switch = RangeSwitch(_data, _controller)

    _controller.set_charging_params(car_id=CAR_ID, params=_data["charge_state"])

    await _switch.async_update()
    assert _switch.is_maxrange()


@pytest.mark.asyncio
async def test_async_update_with_change(monkeypatch):
    """Test async_update() after an update."""

    _mock = TeslaMock(monkeypatch)
    _controller = Controller(None)
    _controller.set_id_vin(CAR_ID, VIN)
    _controller.set_last_update_time(vin=VIN, timestamp=LAST_UPDATE_TIME)

    _data = _mock.data_request_vehicle()
    _data["charge_state"]["charge_to_max_range"] = True
    _switch = RangeSwitch(_data, _controller)

    _data["charge_state"]["charge_to_max_range"] = False

    _controller.set_charging_params(car_id=CAR_ID, params=_data["charge_state"])

    await _switch.async_update()
    assert not _switch.is_maxrange()
