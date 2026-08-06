"""HTTP endpoint health checks."""
from __future__ import annotations

import time
from typing import Dict

import requests


def check(url: str, expect: int = 200, timeout: float = 5.0) -> Dict:
    """Perform an HTTP GET and report status, latency and health."""
    start = time.perf_counter()
    try:
        resp = requests.get(url, timeout=timeout)
        latency = (time.perf_counter() - start) * 1000
        return {
            "url": url,
            "status_code": resp.status_code,
            "latency_ms": round(latency, 1),
            "healthy": resp.status_code == expect,
        }
    except requests.RequestException as exc:
        return {"url": url, "status_code": None, "healthy": False,
                "error": str(exc)}
