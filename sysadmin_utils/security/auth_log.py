"""Parse authentication logs for failed and successful logins."""
from __future__ import annotations

import re
from collections import Counter
from pathlib import Path
from typing import Dict, List

_FAIL_RE = re.compile(r"Failed password for(?: invalid user)? (\S+) from (\S+)")
_ACCEPT_RE = re.compile(r"Accepted \S+ for (\S+) from (\S+)")


def failed_logins(path: str = "/var/log/auth.log") -> List[Dict]:
    """Return failed SSH login attempts parsed from an auth log."""
    results = []
    for line in Path(path).read_text(errors="replace").splitlines():
        m = _FAIL_RE.search(line)
        if m:
            results.append({"user": m.group(1), "source_ip": m.group(2)})
    return results


def top_offenders(path: str = "/var/log/auth.log", top: int = 10) -> List:
    """Return the source IPs with the most failed login attempts."""
    counter: Counter = Counter(f["source_ip"] for f in failed_logins(path))
    return counter.most_common(top)
