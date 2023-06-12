"""Test exception retry logic."""

from httpx import RequestError
from tenacity import RetryCallState, Retrying

from teslajsonpy.const import MAX_API_RETRY_TIME
from teslajsonpy.exceptions import custom_retry, custom_wait, TeslaException


def test_tesla_exception_retryable():
    # code, retryable
    test_set = [
        (408, True),
        (540, True),
        (401, False),
        (404, False),
        (405, False),
        (423, False),
        (429, False),
    ]

    for code, expected in test_set:
        exc = TeslaException(code)
        assert exc.retryable == expected


def test_custom_retry():
    # No exceptions means we don't retry
    rs = RetryCallState(Retrying(), None, None, None)
    rs.set_result(None)
    assert custom_retry(rs) is False

    # Add a retryable exception
    ex = TeslaException(408)
    rs.set_exception((type(ex), ex, None))
    assert custom_retry(rs) is True

    # Add a non-retryable exception
    ex = TeslaException(401)
    rs.set_exception((type(ex), ex, None))
    assert custom_retry(rs) is False

    # Any RequestError should also retry
    ex = RequestError("")
    rs.set_exception((type(ex), ex, None))
    assert custom_retry(rs) is True


def test_custom_wait():
    rs = RetryCallState(Retrying(), None, None, None)
    # sec_since_start, attempt, wait_min, wait_max
    test_set = [
        (0, 1, 1, 2),
        (0, 2, 2, 3),
        (0, 3, 4, 5),
        (0, 4, 8, 9),
        (0, 5, 15, 15),
        (14, 2, 1, 1),
        (16, 1, 0, 0),
    ]
    assert MAX_API_RETRY_TIME == 15
    for sec, attempt, expected_min, expected_max in test_set:
        rs.outcome_timestamp = rs.start_time + sec
        rs.attempt_number = attempt
        wait = custom_wait(rs)
        assert wait >= expected_min
        assert wait <= expected_max
