"""Test climate."""

import pytest
import time

from teslajsonpy.controller import Controller
from teslajsonpy.exceptions import UnknownPresetMode
from teslajsonpy.homeassistant.climate import Climate

from tests.tesla_mock import TeslaMock, VIN, CAR_ID

LAST_UPDATE_TIME = time.time()


def test_has_battery(monkeypatch):
    """Test has_battery()."""

    _mock = TeslaMock(monkeypatch)
    _controller = Controller(None)

    _data = _mock.data_request_vehicle()
    _climate = Climate(_data, _controller)

    assert not _climate.has_battery()


def test_get_values_on_init(monkeypatch):
    """Test values after initialization."""

    _mock = TeslaMock(monkeypatch)
    _controller = Controller(None)

    _data = _mock.data_request_vehicle()
    _climate = Climate(_data, _controller)

    assert _climate is not None
    assert _climate.get_current_temp() is None
    assert _climate.get_fan_status() is None
    assert _climate.get_goal_temp() is None
    assert _climate.is_hvac_enabled() is None
    assert _climate.preset_mode is None


@pytest.mark.asyncio
async def test_get_values_after_update(monkeypatch):
    """Test values after an update."""

    _mock = TeslaMock(monkeypatch)
    _controller = Controller(None)
    _controller.set_id_vin(CAR_ID, VIN)
    _controller.set_last_update_time(vin=VIN, timestamp=LAST_UPDATE_TIME)

    _data = _mock.data_request_vehicle()
    _climate = Climate(_data, _controller)

    _controller.set_climate_params(vin=VIN, params=_data["climate_state"])
    await _climate.async_update()

    assert _climate is not None

    assert _climate.get_current_temp() is None
    assert not _climate.get_fan_status() is None
    assert _climate.get_fan_status() == 0
    assert not _climate.get_goal_temp() is None
    assert _climate.get_goal_temp() == 21.6
    assert not _climate.is_hvac_enabled() is None
    assert not _climate.is_hvac_enabled()
    assert _climate.preset_mode is not None
    assert _climate.preset_mode == "normal"


@pytest.mark.asyncio
async def test_get_current_temp(monkeypatch):
    """Test get_current_temp()."""

    _mock = TeslaMock(monkeypatch)
    _controller = Controller(None)
    _controller.set_id_vin(CAR_ID, VIN)
    _controller.set_last_update_time(vin=VIN, timestamp=LAST_UPDATE_TIME)

    _data = _mock.data_request_vehicle()
    _data["climate_state"]["inside_temp"] = 18.8
    _climate = Climate(_data, _controller)

    _controller.set_climate_params(vin=VIN, params=_data["climate_state"])

    await _climate.async_update()

    assert not _climate.get_current_temp() is None
    assert _climate.get_current_temp() == 18.8


@pytest.mark.asyncio
async def test_get_fan_status(monkeypatch):
    """Test get_fan_status()."""

    _mock = TeslaMock(monkeypatch)
    _controller = Controller(None)
    _controller.set_id_vin(CAR_ID, VIN)
    _controller.set_last_update_time(vin=VIN, timestamp=LAST_UPDATE_TIME)

    _data = _mock.data_request_vehicle()
    _data["climate_state"]["fan_status"] = 1
    _climate = Climate(_data, _controller)

    _controller.set_climate_params(vin=VIN, params=_data["climate_state"])

    await _climate.async_update()

    assert not _climate.get_fan_status() is None
    assert _climate.get_fan_status() == 1


@pytest.mark.asyncio
async def test_get_goal_temp(monkeypatch):
    """Test get_goal_temp()."""

    _mock = TeslaMock(monkeypatch)
    _controller = Controller(None)
    _controller.set_id_vin(CAR_ID, VIN)
    _controller.set_last_update_time(vin=VIN, timestamp=LAST_UPDATE_TIME)

    _data = _mock.data_request_vehicle()
    _data["climate_state"]["driver_temp_setting"] = 23.4
    _climate = Climate(_data, _controller)

    _controller.set_climate_params(vin=VIN, params=_data["climate_state"])

    await _climate.async_update()

    assert not _climate.get_goal_temp() is None
    assert _climate.get_goal_temp() == 23.4


@pytest.mark.asyncio
async def test_is_hvac_enabled_on(monkeypatch):
    """Test is_hvac_enabled() when is_climate_on is True."""

    _mock = TeslaMock(monkeypatch)
    _controller = Controller(None)
    _controller.set_id_vin(CAR_ID, VIN)
    _controller.set_last_update_time(vin=VIN, timestamp=LAST_UPDATE_TIME)

    _data = _mock.data_request_vehicle()
    _data["climate_state"]["is_climate_on"] = True
    _climate = Climate(_data, _controller)

    _controller.set_climate_params(vin=VIN, params=_data["climate_state"])

    await _climate.async_update()

    assert not _climate.is_hvac_enabled() is None
    assert _climate.is_hvac_enabled()


@pytest.mark.asyncio
async def test_is_hvac_enabled_off(monkeypatch):
    """Test is_hvac_enabled() when is_climate_on is False."""

    _mock = TeslaMock(monkeypatch)
    _controller = Controller(None)
    _controller.set_id_vin(CAR_ID, VIN)
    _controller.set_last_update_time(vin=VIN, timestamp=LAST_UPDATE_TIME)

    _data = _mock.data_request_vehicle()
    _data["climate_state"]["is_climate_on"] = False
    _climate = Climate(_data, _controller)

    _controller.set_climate_params(vin=VIN, params=_data["climate_state"])

    await _climate.async_update()

    assert not _climate.is_hvac_enabled() is None
    assert not _climate.is_hvac_enabled()


@pytest.mark.asyncio
async def test_set_status_on(monkeypatch):
    """Test set_status() to enabled."""

    _mock = TeslaMock(monkeypatch)
    _controller = Controller(None)
    _controller.set_id_vin(CAR_ID, VIN)
    _controller.set_last_update_time(vin=VIN, timestamp=LAST_UPDATE_TIME)

    _data = _mock.data_request_vehicle()
    _climate = Climate(_data, _controller)

    _controller.set_climate_params(vin=VIN, params=_data["climate_state"])

    await _climate.async_update()
    await _climate.set_status(True)

    assert not _climate.is_hvac_enabled() is None
    assert _climate.is_hvac_enabled()


@pytest.mark.asyncio
async def test_set_status_off(monkeypatch):
    """Test set_status() to disabled."""

    _mock = TeslaMock(monkeypatch)
    _controller = Controller(None)
    _controller.set_id_vin(CAR_ID, VIN)
    _controller.set_last_update_time(vin=VIN, timestamp=LAST_UPDATE_TIME)

    _data = _mock.data_request_vehicle()
    _climate = Climate(_data, _controller)

    _controller.set_climate_params(vin=VIN, params=_data["climate_state"])

    await _climate.async_update()
    await _climate.set_status(False)

    assert not _climate.is_hvac_enabled() is None
    assert not _climate.is_hvac_enabled()


@pytest.mark.asyncio
async def test_set_temperature(monkeypatch):
    """Test set_temperature()."""

    _mock = TeslaMock(monkeypatch)
    _controller = Controller(None)
    _controller.set_id_vin(CAR_ID, VIN)
    _controller.set_last_update_time(vin=VIN, timestamp=LAST_UPDATE_TIME)

    _data = _mock.data_request_vehicle()
    _climate = Climate(_data, _controller)

    _controller.set_climate_params(vin=VIN, params=_data["climate_state"])

    await _climate.async_update()

    await _climate.set_temperature(12.3)

    assert not _climate.get_goal_temp() is None
    assert _climate.get_goal_temp() == 12.3


@pytest.mark.asyncio
async def test_set_preset_mode_success(monkeypatch):
    """Test set_preset_mode()."""

    _mock = TeslaMock(monkeypatch)
    _controller = Controller(None)
    _controller.set_id_vin(CAR_ID, VIN)
    _controller.set_last_update_time(vin=VIN, timestamp=LAST_UPDATE_TIME)

    _data = _mock.data_request_vehicle()
    _climate = Climate(_data, _controller)

    _controller.set_climate_params(vin=VIN, params=_data["climate_state"])

    await _climate.async_update()

    preset_modes = _climate.preset_modes
    for mode in preset_modes:
        await _climate.set_preset_mode(mode)
        assert _climate.preset_mode is not None
        assert _climate.preset_mode == mode


@pytest.mark.asyncio
async def test_set_preset_mode_invalid_modes(monkeypatch):
    """Test set_preset_mode() with invalid modes."""

    _mock = TeslaMock(monkeypatch)
    _controller = Controller(None)
    _controller.set_id_vin(CAR_ID, VIN)
    _controller.set_last_update_time(vin=VIN, timestamp=LAST_UPDATE_TIME)

    _data = _mock.data_request_vehicle()
    _climate = Climate(_data, _controller)

    _controller.set_climate_params(vin=VIN, params=_data["climate_state"])

    await _climate.async_update()

    bad_modes = ["UKNOWN_MODE", "home", "auto", "away", "hot"]
    for mode in bad_modes:
        assert mode not in _climate.preset_modes
        with pytest.raises(UnknownPresetMode):
            await _climate.set_preset_mode(mode)
