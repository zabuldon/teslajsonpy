"""Test Home Assistant entity."""

import pytest

from teslajsonpy.ha.entity import Entity


def test_assumed_state():
    """Test assumed_state()."""

    _entity = Entity()

    assert not _entity.assumed_state


def test_available():
    """Test available()."""

    _entity = Entity()

    assert _entity.available


def test_device_class():
    """Test device_class()."""

    _entity = Entity()

    assert _entity.device_class is None


def test_device_state_attributes():
    """Test device_state_attributes()."""

    _entity = Entity()

    assert _entity.device_state_attributes is None


def test_entity_picture():
    """Test entity_picture()."""

    _entity = Entity()

    assert _entity.entity_picture is None


def test_name():
    """Test name()."""

    _entity = Entity()

    assert _entity.name is None


def test_should_poll():
    """Test should_poll()."""

    _entity = Entity()

    assert _entity.should_poll


def test_unique_id():
    """Test unique_id()."""

    _entity = Entity()

    assert _entity.unique_id is None


def test_force_update():
    """Test force_update()."""

    _entity = Entity()

    assert not _entity.force_update


def test_icon():
    """Test icon()."""

    _entity = Entity()

    assert _entity.icon is None


def test_entity_registry_enabled_default():
    """Test entity_registry_enabled_default()."""

    _entity = Entity()

    assert _entity.entity_registry_enabled_default


@pytest.mark.asyncio
async def test_update():
    """Test update()."""

    _entity = Entity()

    with pytest.raises(NotImplementedError):
        await _entity.update()
