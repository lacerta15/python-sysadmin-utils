"""Uptime and boot-time helpers."""
from __future__ import annotations

from datetime import datetime

import psutil

from ..core.humanize import seconds_to_human


def boot_time() -> datetime:
    """Return the system boot time."""
    return datetime.fromtimestamp(psutil.boot_time())


def uptime_seconds() -> float:
    """Return system uptime in seconds."""
    return (datetime.now() - boot_time()).total_seconds()


def uptime_human() -> str:
    """Return a human-readable uptime string."""
    return seconds_to_human(uptime_seconds())
