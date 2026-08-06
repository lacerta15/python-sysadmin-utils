"""Hardware sensor readings (temperature, fans) where available."""
from __future__ import annotations

from typing import Dict, List

import psutil


def temperatures() -> Dict[str, List[Dict]]:
    """Return temperature sensors grouped by chip (best effort)."""
    fn = getattr(psutil, "sensors_temperatures", None)
    if fn is None:
        return {}
    out: Dict[str, List[Dict]] = {}
    for chip, entries in fn().items():
        out[chip] = [
            {"label": e.label or chip, "current": e.current,
             "high": e.high, "critical": e.critical}
            for e in entries
        ]
    return out


def hottest() -> float:
    """Return the highest current temperature reading, or 0.0 if none."""
    readings = [e["current"] for group in temperatures().values() for e in group]
    return max(readings) if readings else 0.0
