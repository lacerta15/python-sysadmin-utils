"""Network I/O counters per interface."""
from __future__ import annotations

from typing import Dict

import psutil


def counters() -> Dict[str, Dict[str, int]]:
    """Return bytes/packets sent and received per network interface."""
    result = {}
    for name, stats in psutil.net_io_counters(pernic=True).items():
        result[name] = {
            "bytes_sent": stats.bytes_sent,
            "bytes_recv": stats.bytes_recv,
            "packets_sent": stats.packets_sent,
            "packets_recv": stats.packets_recv,
            "errin": stats.errin,
            "errout": stats.errout,
        }
    return result


def interfaces_up() -> list:
    """Return names of network interfaces that are currently up."""
    return [name for name, s in psutil.net_if_stats().items() if s.isup]
