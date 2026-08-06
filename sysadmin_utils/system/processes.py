"""Inspect running processes and flag resource hogs."""
from __future__ import annotations

from typing import Dict, List

import psutil


def top_processes(limit: int = 10, sort_by: str = "cpu_percent") -> List[Dict]:
    """Return the top ``limit`` processes sorted by a psutil field."""
    procs = []
    for p in psutil.process_iter(["pid", "name", "username",
                                  "cpu_percent", "memory_percent"]):
        info = p.info
        info["cpu_percent"] = info.get("cpu_percent") or 0.0
        info["memory_percent"] = info.get("memory_percent") or 0.0
        procs.append(info)
    procs.sort(key=lambda i: i.get(sort_by, 0.0), reverse=True)
    return procs[:limit]


def flag_hogs(cpu: float = 80.0, mem: float = 80.0) -> List[Dict]:
    """Return processes exceeding the CPU or memory thresholds."""
    hogs = []
    for info in top_processes(limit=200):
        if info["cpu_percent"] >= cpu or info["memory_percent"] >= mem:
            hogs.append(info)
    return hogs
