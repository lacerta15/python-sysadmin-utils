"""Execute a command on a single remote host via SSH."""
from __future__ import annotations

from typing import Callable

from ..core.shell import run as default_run


def run_remote(host: str, command: str, user: str = "root",
               timeout: int = 20, runner: Callable = default_run):
    """Run ``command`` on ``user@host`` over SSH.

    ``runner`` is injectable so tests can substitute a fake instead of a
    real SSH call.
    """
    ssh_cmd = ["ssh", "-o", "ConnectTimeout=5", "-o", "BatchMode=yes",
               f"{user}@{host}", command]
    return runner(ssh_cmd, timeout=timeout)
