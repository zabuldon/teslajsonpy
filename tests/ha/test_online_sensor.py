"""Test Home Assistant online sensor."""

import pytest

from teslajsonpy.ha.binary_sensor import OnlineSensor, BinarySensorType


def test_is_on():
    """Test is_on()."""

    _sensor = OnlineSensor()

    assert not _sensor.is_on


def test_assumed_state():
    """Test assumed_state()."""

    _sensor = OnlineSensor()

    assert not _sensor.assumed_state


def test_available():
    """Test available()."""

    _sensor = OnlineSensor()

    assert _sensor.available


def test_device_class():
    """Test device_class()."""

    _sensor = OnlineSensor()

    assert not _sensor.device_class is None
    assert _sensor.device_class == BinarySensorType.CONNECTIVITY


def test_device_state_attributes():
    """Test device_state_attributes()."""

    _sensor = OnlineSensor()

    assert _sensor.device_state_attributes is None


def test_entity_picture():
    """Test entity_picture()."""

    _sensor = OnlineSensor()

    assert _sensor.entity_picture is None


def test_name():
    """Test name()."""

    _sensor = OnlineSensor()

    assert _sensor.name is None


def test_should_poll():
    """Test should_poll()."""

    _sensor = OnlineSensor()

    assert _sensor.should_poll


def test_unique_id():
    """Test unique_id()."""

    _sensor = OnlineSensor()

    assert _sensor.unique_id is None


def test_force_update():
    """Test force_update()."""

    _sensor = OnlineSensor()

    assert not _sensor.force_update


def test_icon():
    """Test icon()."""

    _sensor = OnlineSensor()

    assert _sensor.icon is None


def test_entity_registry_enabled_default():
    """Test entity_registry_enabled_default()."""

    _sensor = OnlineSensor()

    assert _sensor.entity_registry_enabled_default


def test_update():
    """Test update()."""

    _sensor = OnlineSensor()

    with pytest.raises(NotImplementedError):
        _sensor.update()


@pytest.mark.asyncio
async def test_async_update():
    """Test async_update()."""

    _sensor = OnlineSensor()

    with pytest.raises(NotImplementedError):
        await _sensor.async_update()
