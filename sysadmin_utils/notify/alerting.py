"""Turn failed checks into notifications via an injectable notifier."""
from __future__ import annotations

from typing import Callable, Dict, List


def format_alert(failures: List[Dict]) -> str:
    """Build a human-readable alert message from failed checks."""
    lines = [f"- {f['check']}: {f['value']:.1f} exceeds limit {f['threshold']}"
             for f in failures]
    return "Threshold alert:\n" + "\n".join(lines)


def alert_on_failures(results: List[Dict], notifier: Callable[[str], object]) -> bool:
    """Call ``notifier`` with an alert if any check failed. Returns True if sent."""
    failures = [r for r in results if not r["ok"]]
    if not failures:
        return False
    notifier(format_alert(failures))
    return True
