"""Retry decorator with exponential backoff."""
from __future__ import annotations

import functools
import time
from typing import Callable, Tuple, Type


def retry(exceptions: Tuple[Type[BaseException], ...] = (Exception,),
          tries: int = 3, delay: float = 0.5, backoff: float = 2.0):
    """Retry a callable on the given exceptions with exponential backoff.

    ``tries`` is the total number of attempts (>=1).
    """
    def decorator(func: Callable):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            attempt, wait = 1, delay
            while True:
                try:
                    return func(*args, **kwargs)
                except exceptions:
                    if attempt >= tries:
                        raise
                    time.sleep(wait)
                    attempt += 1
                    wait *= backoff
        return wrapper
    return decorator
