"""Parse a simple hosts inventory file.

Format: one host per line, optional ``user@host``, ``#`` for comments.
"""
from __future__ import annotations

from pathlib import Path
from typing import Dict, List


def parse_inventory(path: str, default_user: str = "root") -> List[Dict[str, str]]:
    """Return a list of {'user': ..., 'host': ...} from an inventory file."""
    hosts = []
    for raw in Path(path).read_text().splitlines():
        line = raw.split("#", 1)[0].strip()
        if not line:
            continue
        if "@" in line:
            user, host = line.split("@", 1)
        else:
            user, host = default_user, line
        hosts.append({"user": user, "host": host})
    return hosts
