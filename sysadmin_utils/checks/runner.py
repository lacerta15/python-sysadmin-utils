"""Run threshold checks against live health metrics from a config."""
from __future__ import annotations

from typing import Any, Dict, List

from ..system import health

# maps a check name to the metric key it inspects
_METRIC_KEYS = {"cpu": "cpu_percent", "mem": "mem_percent", "disk": "disk_percent"}
_DEFAULTS = {"cpu_max": 85.0, "mem_max": 85.0, "disk_max": 90.0}


def run_checks(config: Dict[str, Any] | None = None) -> List[Dict[str, Any]]:
    """Evaluate each configured threshold against current metrics."""
    cfg = {**_DEFAULTS, **(config or {})}
    metrics = health.collect()
    results = []
    for name, key in _METRIC_KEYS.items():
        value = metrics[key]
        limit = cfg[f"{name}_max"]
        results.append({
            "check": name,
            "value": value,
            "threshold": limit,
            "ok": value < limit,
        })
    return results


def all_passing(results: List[Dict[str, Any]]) -> bool:
    """Return True only if every check passed."""
    return all(r["ok"] for r in results)
