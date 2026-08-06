import pytest

from sysadmin_utils.core.retry import retry


def test_retry_succeeds_after_failures():
    calls = {"n": 0}

    @retry(tries=3, delay=0)
    def flaky():
        calls["n"] += 1
        if calls["n"] < 3:
            raise ValueError("boom")
        return "ok"

    assert flaky() == "ok"
    assert calls["n"] == 3


def test_retry_reraises_after_exhausting():
    @retry(exceptions=(KeyError,), tries=2, delay=0)
    def always_fail():
        raise KeyError("nope")

    with pytest.raises(KeyError):
        always_fail()
