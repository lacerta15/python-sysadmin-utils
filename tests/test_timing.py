import time

from sysadmin_utils.core.timing import timer, timed


def test_timer_context():
    with timer() as marker:
        time.sleep(0.01)
    assert marker["seconds"] >= 0.01


def test_timed_decorator():
    @timed
    def work():
        time.sleep(0.01)
        return 42

    assert work() == 42
    assert work.last_duration >= 0.01
