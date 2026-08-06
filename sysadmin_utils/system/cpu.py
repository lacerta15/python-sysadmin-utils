"""Detailed CPU statistics."""
from __future__ import annotations

from typing import Dict, List

import psutil


def per_core() -> List[float]:
    """Return CPU utilization percentage per logical core."""
    return psutil.cpu_percent(interval=0.5, percpu=True)


def frequency() -> Dict[str, float]:
    """Return current/min/max CPU frequency in MHz (best effort)."""
    freq = psutil.cpu_freq()
    if not freq:
        return {}
    return {"current": freq.current, "min": freq.min, "max": freq.max}


def times_percent() -> Dict[str, float]:
    """Return CPU time breakdown (user/system/idle/iowait) as percentages."""
    t = psutil.cpu_times_percent(interval=0.5)
    return {k: getattr(t, k) for k in t._fields}
