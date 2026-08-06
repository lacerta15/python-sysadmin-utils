"""Enumerate listening sockets on the local machine."""
from __future__ import annotations

from typing import Dict, List

import psutil


def listening_ports(kind: str = "inet") -> List[Dict]:
    """Return listening sockets with their bound address and owning PID."""
    results = []
    for conn in psutil.net_connections(kind=kind):
        if conn.status != psutil.CONN_LISTEN:
            continue
        laddr = conn.laddr
        results.append({
            "ip": getattr(laddr, "ip", ""),
            "port": getattr(laddr, "port", 0),
            "pid": conn.pid,
            "family": str(conn.family),
        })
    return sorted(results, key=lambda r: r["port"])
