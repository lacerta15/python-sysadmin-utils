"""Basic host/port reachability checks."""
from __future__ import annotations

import socket
import time
from typing import Dict


def tcp_check(host: str, port: int, timeout: float = 3.0) -> Dict:
    """Attempt a TCP connection and measure latency."""
    start = time.perf_counter()
    try:
        with socket.create_connection((host, port), timeout=timeout):
            elapsed = (time.perf_counter() - start) * 1000
            return {"host": host, "port": port, "open": True,
                    "latency_ms": round(elapsed, 1)}
    except OSError as exc:
        return {"host": host, "port": port, "open": False, "error": str(exc)}


def resolve(host: str) -> Dict:
    """Resolve a hostname to its A records."""
    try:
        _, _, addrs = socket.gethostbyname_ex(host)
        return {"host": host, "addresses": addrs}
    except socket.gaierror as exc:
        return {"host": host, "addresses": [], "error": str(exc)}
