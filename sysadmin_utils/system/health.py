"""Collect a snapshot of overall system health."""
from __future__ import annotations

import socket
from datetime import datetime
from typing import Any, Dict

import psutil


def collect() -> Dict[str, Any]:
    """Return CPU, memory, swap, disk and load metrics as a dict."""
    vm = psutil.virtual_memory()
    swap = psutil.swap_memory()
    disk = psutil.disk_usage("/")
    try:
        load1, load5, load15 = psutil.getloadavg()
    except (AttributeError, OSError):  # pragma: no cover - Windows
        load1 = load5 = load15 = 0.0
    boot = datetime.fromtimestamp(psutil.boot_time())
    return {
        "hostname": socket.gethostname(),
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "uptime_hours": round((datetime.now() - boot).total_seconds() / 3600, 1),
        "cpu_percent": psutil.cpu_percent(interval=0.5),
        "cpu_count": psutil.cpu_count(),
        "load_avg": [round(load1, 2), round(load5, 2), round(load15, 2)],
        "mem_percent": vm.percent,
        "mem_used_gb": round(vm.used / 1e9, 2),
        "mem_total_gb": round(vm.total / 1e9, 2),
        "swap_percent": swap.percent,
        "disk_percent": disk.percent,
        "disk_free_gb": round(disk.free / 1e9, 2),
    }


def evaluate(metrics: Dict[str, Any], cpu: float = 85, mem: float = 85,
             disk: float = 90) -> Dict[str, str]:
    """Classify metrics into OK/WARN statuses against thresholds."""
    status = {}
    status["cpu"] = "WARN" if metrics["cpu_percent"] >= cpu else "OK"
    status["mem"] = "WARN" if metrics["mem_percent"] >= mem else "OK"
    status["disk"] = "WARN" if metrics["disk_percent"] >= disk else "OK"
    status["overall"] = "WARN" if "WARN" in status.values() else "OK"
    return status


def format_report(metrics: Dict[str, Any]) -> str:
    """Render a human-readable one-screen report."""
    s = evaluate(metrics)
    lines = [
        f"Host: {metrics['hostname']}   ({metrics['timestamp']})",
        f"Uptime: {metrics['uptime_hours']} h",
        f"[{s['cpu']}]  CPU  {metrics['cpu_percent']:5.1f}%  "
        f"load {metrics['load_avg']}",
        f"[{s['mem']}]  MEM  {metrics['mem_percent']:5.1f}%  "
        f"({metrics['mem_used_gb']}/{metrics['mem_total_gb']} GB)",
        f"[{s['disk']}] DISK {metrics['disk_percent']:5.1f}%  "
        f"free {metrics['disk_free_gb']} GB",
        f"Overall: {s['overall']}",
    ]
    return "\n".join(lines)
