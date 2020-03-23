"""Sample tests."""

import pytest


def system_exit():
    """Raise system exit."""
    raise SystemExit(1)


def add_one(x_value):
    """Add 1 to x_value.
        Args:
            x_value (float): A number.
    """
    return x_value + 1


def test_system_exit():
    """Test system_exit."""
    with pytest.raises(SystemExit):
        system_exit()


def test_add_one():
    """Test add_one."""
    assert add_one(1) == 2
    assert add_one(2) == 3
    assert add_one(3) == 4
    assert add_one(4) == 5
