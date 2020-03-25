"""Test Tesla exception."""

from teslajsonpy.exceptions import TeslaException


def test_code_as_string():
    """Test error with a string code."""

    _err = TeslaException("dummy")

    assert not _err is None
    assert _err.code == "dummy"
    assert _err.message == "dummy"


def test_code_lt_300():
    """Test error with a code less than 300."""

    _err = TeslaException(299)

    assert not _err is None
    assert _err.code == 299
    assert _err.message == ""


def test_code_400():
    """Test error 400."""

    _err = TeslaException(400)

    assert not _err is None
    assert _err.code == 400
    assert _err.message == "UNKNOWN_ERROR_400"


def test_code_401():
    """Test error 401."""

    _err = TeslaException(401)

    assert not _err is None
    assert _err.code == 401
    assert _err.message == "UNAUTHORIZED"


def test_code_402():
    """Test error 402."""

    _err = TeslaException(402)

    assert not _err is None
    assert _err.code == 402
    assert _err.message == "UNKNOWN_ERROR_402"


def test_code_403():
    """Test error 403."""

    _err = TeslaException(403)

    assert not _err is None
    assert _err.code == 403
    assert _err.message == "UNKNOWN_ERROR_403"


def test_code_404():
    """Test error 404."""

    _err = TeslaException(404)

    assert not _err is None
    assert _err.code == 404
    assert _err.message == "NOT_FOUND"


def test_code_405():
    """Test error 405."""

    _err = TeslaException(405)

    assert not _err is None
    assert _err.code == 405
    assert _err.message == "MOBILE_ACCESS_DISABLED"


def test_code_408():
    """Test error 408."""

    _err = TeslaException(408)

    assert not _err is None
    assert _err.code == 408
    assert _err.message == "VEHICLE_UNAVAILABLE"


def test_code_423():
    """Test error 423."""

    _err = TeslaException(423)

    assert not _err is None
    assert _err.code == 423
    assert _err.message == "ACCOUNT_LOCKED"


def test_code_429():
    """Test error 429."""

    _err = TeslaException(429)

    assert not _err is None
    assert _err.code == 429
    assert _err.message == "TOO_MANY_REQUESTS"


def test_code_500():
    """Test error 500."""

    _err = TeslaException(500)

    assert not _err is None
    assert _err.code == 500
    assert _err.message == "SERVER_ERROR"


def test_code_503():
    """Test error 503."""

    _err = TeslaException(503)

    assert not _err is None
    assert _err.code == 503
    assert _err.message == "SERVICE_MAINTENANCE"


def test_code_504():
    """Test error 504."""

    _err = TeslaException(504)

    assert not _err is None
    assert _err.code == 504
    assert _err.message == "UPSTREAM_TIMEOUT"


def test_code_505():
    """Test error 505."""

    _err = TeslaException(505)

    assert not _err is None
    assert _err.code == 505
    assert _err.message == "UNKNOWN_ERROR_505"
