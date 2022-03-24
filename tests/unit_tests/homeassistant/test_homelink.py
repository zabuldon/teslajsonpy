"""Test homelink button."""

import pytest

from teslajsonpy.controller import Controller
from teslajsonpy.exceptions import HomelinkError
from teslajsonpy.homeassistant.homelink import TriggerHomelink

from tests.tesla_mock import TeslaMock, VIN, CAR_ID


def test_has_battery(monkeypatch):
    """Test has_battery()."""

    _mock = TeslaMock(monkeypatch)
    _controller = Controller(None)

    _data = _mock.data_request_vehicle()
    _button = TriggerHomelink(_data, _controller)

    assert not _button.has_battery()


@pytest.mark.asyncio
async def test_trigger_homelink(monkeypatch):
    """Test test_trigger_homelink()."""

    _mock = TeslaMock(monkeypatch)
    _controller = Controller(None)
    _controller.set_id_vin(CAR_ID, VIN)

    _data = _mock.data_request_vehicle()
    _data["drive_state"]["longitude"] = 12.345
    _data["drive_state"]["native_longitude"] = 12.345
    _data["drive_state"]["latitude"] = 34.567
    _data["drive_state"]["native_latitude"] = 34.567
    _data["vehicle_state"]["homelink_device_count"] = 1
    _data["vehicle_state"]["homelink_nearby"] = True
    _button = TriggerHomelink(_data, _controller)

    _controller.set_drive_params(vin=VIN, params=_data["drive_state"])
    _controller.set_state_params(vin=VIN, params=_data["vehicle_state"])

    await _button.async_update()

    await _button.trigger_homelink()


@pytest.mark.asyncio
async def test_available(monkeypatch):
    """Test available()."""

    _mock = TeslaMock(monkeypatch)
    _controller = Controller(None)
    _controller.set_id_vin(CAR_ID, VIN)

    _data = _mock.data_request_vehicle()
    _button = TriggerHomelink(_data, _controller)

    assert not _button.available()

    _test_set = [None, 0, 1, 2]

    for _count in _test_set:
        _data["vehicle_state"]["homelink_device_count"] = _count
        _controller.set_state_params(vin=VIN, params=_data["vehicle_state"])
        await _button.async_update()
        assert _button.available() == bool(_count)


@pytest.mark.asyncio
async def test_homelink_error_device_count(monkeypatch):
    """Test HomelinkError for no device count."""

    _mock = TeslaMock(monkeypatch)
    _controller = Controller(None)
    _controller.set_id_vin(CAR_ID, VIN)

    _data = _mock.data_request_vehicle()
    _data["drive_state"]["longitude"] = 12.345
    _data["drive_state"]["native_longitude"] = 12.345
    _data["drive_state"]["latitude"] = 34.567
    _data["drive_state"]["native_latitude"] = 34.567
    _data["vehicle_state"]["homelink_device_count"] = 0
    _data["vehicle_state"]["homelink_nearby"] = False
    _button = TriggerHomelink(_data, _controller)

    _controller.set_drive_params(vin=VIN, params=_data["drive_state"])
    _controller.set_state_params(vin=VIN, params=_data["vehicle_state"])

    await _button.async_update()

    with pytest.raises(HomelinkError) as excinfo:
        await _button.trigger_homelink()
    assert (
        excinfo.value.message == f"No homelink devices added to {_button.car_name()}."
    )


@pytest.mark.asyncio
async def test_homelink_error_device_nearby(monkeypatch):
    """Test HomelinkError for no device nearby."""

    _mock = TeslaMock(monkeypatch)
    _controller = Controller(None)
    _controller.set_id_vin(CAR_ID, VIN)

    _data = _mock.data_request_vehicle()
    _data["drive_state"]["longitude"] = 12.345
    _data["drive_state"]["native_longitude"] = 12.345
    _data["drive_state"]["latitude"] = 34.567
    _data["drive_state"]["native_latitude"] = 34.567
    _data["vehicle_state"]["homelink_device_count"] = 1
    _data["vehicle_state"]["homelink_nearby"] = False
    _button = TriggerHomelink(_data, _controller)

    _controller.set_drive_params(vin=VIN, params=_data["drive_state"])
    _controller.set_state_params(vin=VIN, params=_data["vehicle_state"])

    await _button.async_update()

    with pytest.raises(HomelinkError) as excinfo:
        await _button.trigger_homelink()
    assert excinfo.value.message == f"No homelink devices near {_button.car_name()}."


@pytest.mark.asyncio
async def test_native_location(monkeypatch):
    """Test native location values are set correctly."""

    _mock = TeslaMock(monkeypatch)
    _controller = Controller(None)
    _controller.set_id_vin(CAR_ID, VIN)

    _data = _mock.data_request_vehicle()
    _data["drive_state"]["native_location_supported"] = 1
    _data["drive_state"]["longitude"] = 12.345
    _data["drive_state"]["native_longitude"] = 23.456
    _data["drive_state"]["latitude"] = 34.567
    _data["drive_state"]["native_latitude"] = 45.678
    _button = TriggerHomelink(_data, _controller)

    _controller.set_drive_params(vin=VIN, params=_data["drive_state"])

    await _button.async_update()

    assert _button._longitude == 23.456
    assert _button._latitude == 45.678


@pytest.mark.asyncio
async def test_location(monkeypatch):
    """Test non-native location values are set correctly."""

    _mock = TeslaMock(monkeypatch)
    _controller = Controller(None)
    _controller.set_id_vin(CAR_ID, VIN)

    _data = _mock.data_request_vehicle()
    _data["drive_state"]["native_location_supported"] = 0
    _data["drive_state"]["longitude"] = 12.345
    _data["drive_state"]["native_longitude"] = 23.456
    _data["drive_state"]["latitude"] = 34.567
    _data["drive_state"]["native_latitude"] = 45.678
    _button = TriggerHomelink(_data, _controller)

    _controller.set_drive_params(vin=VIN, params=_data["drive_state"])

    await _button.async_update()

    assert _button._longitude == 12.345
    assert _button._latitude == 34.567
