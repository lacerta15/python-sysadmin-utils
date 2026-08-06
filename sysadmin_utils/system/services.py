"""Thin wrapper around systemctl for managing services."""
from __future__ import annotations

from typing import List

from ..core.shell import run


def is_active(name: str) -> bool:
    return run(["systemctl", "is-active", name]).stdout.strip() == "active"


def is_enabled(name: str) -> bool:
    return run(["systemctl", "is-enabled", name]).stdout.strip() == "enabled"


def status(name: str) -> str:
    return run(["systemctl", "status", "--no-pager", name]).stdout


def failed_units() -> List[str]:
    """Return names of units currently in the failed state."""
    out = run(["systemctl", "list-units", "--state=failed",
               "--no-legend", "--plain"]).stdout
    return [line.split()[0] for line in out.splitlines() if line.strip()]


def restart(name: str):
    """Restart a service (requires privileges). Returns the shell Result."""
    return run(["systemctl", "restart", name], check=False)
