"""Collect a consolidated system report from multiple modules."""
from __future__ import annotations

from datetime import datetime
from typing import Any, Dict

from ..system import health, uptime, services


def collect_report() -> Dict[str, Any]:
    """Gather health metrics, uptime and failed services into one dict."""
    metrics = health.collect()
    report: Dict[str, Any] = {
        "generated": datetime.now().isoformat(timespec="seconds"),
        "hostname": metrics["hostname"],
        "uptime": uptime.uptime_human(),
        "health": metrics,
        "health_status": health.evaluate(metrics),
    }
    try:
        report["failed_services"] = services.failed_units()
    except Exception:
        report["failed_services"] = []
    return report
