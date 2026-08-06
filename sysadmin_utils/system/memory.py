"""Detailed memory and swap statistics."""
from __future__ import annotations

from typing import Dict

import psutil


def snapshot() -> Dict[str, float]:
    """Return virtual and swap memory figures in bytes and percent."""
    vm = psutil.virtual_memory()
    swap = psutil.swap_memory()
    return {
        "total": vm.total,
        "available": vm.available,
        "used": vm.used,
        "percent": vm.percent,
        "swap_total": swap.total,
        "swap_used": swap.used,
        "swap_percent": swap.percent,
    }


def is_pressured(threshold: float = 90.0) -> bool:
    """Return True if memory usage exceeds the threshold percentage."""
    return psutil.virtual_memory().percent >= threshold
