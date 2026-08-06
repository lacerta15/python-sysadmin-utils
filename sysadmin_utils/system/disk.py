"""Disk usage reporting across one or more hosts via SSH."""
from __future__ import annotations

from datetime import datetime
from typing import Dict, List

from ..core.shell import run

DF_CMD = "df -h --output=source,size,used,avail,pcent,target"


def local_usage() -> str:
    """Return df output for the local machine."""
    return run(DF_CMD).stdout


def remote_usage(host: str, user: str = "root", timeout: int = 10) -> str:
    """Return df output for a remote host over SSH."""
    cmd = ["ssh", "-o", "ConnectTimeout=5", f"{user}@{host}", DF_CMD]
    result = run(cmd, timeout=timeout)
    return result.stdout if result.ok else f"ERROR: {result.stderr.strip()}"


def report(hosts: List[str], user: str = "root") -> Dict[str, object]:
    """Build a report dict for the given hosts."""
    data: Dict[str, object] = {
        "generated": datetime.now().isoformat(timespec="seconds"),
        "hosts": {},
    }
    for host in hosts:
        data["hosts"][host] = (  # type: ignore[index]
            local_usage() if host in ("localhost", "127.0.0.1")
            else remote_usage(host, user)
        )
    return data
