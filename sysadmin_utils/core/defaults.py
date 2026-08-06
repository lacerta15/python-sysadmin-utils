"""Default thresholds and settings, overridable via environment."""
from __future__ import annotations

import os

DEFAULTS = {
    "cpu_warn": 85.0,
    "mem_warn": 85.0,
    "disk_warn": 90.0,
    "cert_warn_days": 30,
    "ssh_user": "root",
    "backup_keep": 7,
}


def get(key: str):
    """Return a default, allowing SU_<KEY> environment overrides."""
    env = os.environ.get(f"SU_{key.upper()}")
    if env is None:
        return DEFAULTS[key]
    ref = DEFAULTS[key]
    if isinstance(ref, float):
        return float(env)
    if isinstance(ref, int):
        return int(env)
    return env
