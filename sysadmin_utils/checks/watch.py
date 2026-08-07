"""Run threshold checks and dispatch alerts on failures."""
from __future__ import annotations

from typing import Any, Callable, Dict, List

from .runner import run_checks
from ..notify.alerting import alert_on_failures


def run_once(config: Dict[str, Any] | None = None,
             notifier: Callable[[str], object] | None = None) -> List[Dict]:
    """Run checks once; if a notifier is given, alert on any failures."""
    results = run_checks(config)
    if notifier is not None:
        alert_on_failures(results, notifier)
    return results
