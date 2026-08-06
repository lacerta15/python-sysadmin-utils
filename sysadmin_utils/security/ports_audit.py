"""Audit listening ports against an allowlist."""
from __future__ import annotations

from typing import Dict, List

from ..network.ports import listening_ports


def audit(allowed: List[int]) -> Dict[str, List[int]]:
    """Compare listening ports to an allowlist of expected ports."""
    open_ports = sorted({p["port"] for p in listening_ports()})
    unexpected = [p for p in open_ports if p not in allowed]
    missing = [p for p in allowed if p not in open_ports]
    return {"open": open_ports, "unexpected": unexpected, "missing": missing}
