"""Timing helpers: decorator and context manager."""
from __future__ import annotations

import functools
import time
from contextlib import contextmanager


@contextmanager
def timer(label: str = "elapsed"):
    """Context manager yielding a callable that returns elapsed seconds."""
    start = time.perf_counter()
    marker = {"seconds": 0.0}
    try:
        yield marker
    finally:
        marker["seconds"] = round(time.perf_counter() - start, 4)


def timed(func):
    """Decorator that attaches ``last_duration`` (seconds) to the function."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        try:
            return func(*args, **kwargs)
        finally:
            wrapper.last_duration = round(time.perf_counter() - start, 4)
    wrapper.last_duration = 0.0
    return wrapper
