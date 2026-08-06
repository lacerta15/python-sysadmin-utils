"""Audit local users and current login sessions."""
from __future__ import annotations

from pathlib import Path
from typing import Dict, List

import psutil


def human_users(passwd: str = "/etc/passwd", min_uid: int = 1000) -> List[Dict]:
    """Return real (non-system) accounts parsed from /etc/passwd."""
    users = []
    for line in Path(passwd).read_text().splitlines():
        if not line or line.startswith("#"):
            continue
        parts = line.split(":")
        if len(parts) < 7:
            continue
        uid = int(parts[2])
        if uid >= min_uid and parts[6] not in ("/usr/sbin/nologin", "/bin/false"):
            users.append({"name": parts[0], "uid": uid, "home": parts[5],
                          "shell": parts[6]})
    return users


def active_sessions() -> List[Dict]:
    """Return currently logged-in sessions."""
    return [
        {"user": u.name, "terminal": u.terminal, "host": u.host,
         "started": u.started}
        for u in psutil.users()
    ]
