"""Summarize log files: level counts, top error lines, time span."""
from __future__ import annotations

import re
from collections import Counter
from pathlib import Path
from typing import Dict, List

LEVELS = ("EMERG", "ALERT", "CRIT", "ERROR", "WARN", "WARNING", "INFO", "DEBUG")
_LEVEL_RE = re.compile("|".join(LEVELS))


def analyze(path: str, top: int = 5) -> Dict:
    """Return level counts and the most frequent ERROR/CRIT lines."""
    level_counts: Counter = Counter()
    error_lines: Counter = Counter()
    total = 0
    for line in Path(path).read_text(errors="replace").splitlines():
        total += 1
        m = _LEVEL_RE.search(line.upper())
        if m:
            level = "WARN" if m.group() == "WARNING" else m.group()
            level_counts[level] += 1
            if level in ("ERROR", "CRIT", "ALERT", "EMERG"):
                error_lines[line.strip()] += 1
    return {
        "file": path,
        "total_lines": total,
        "levels": dict(level_counts),
        "top_errors": error_lines.most_common(top),
    }


def grep_count(path: str, pattern: str) -> int:
    """Count lines matching a regex pattern."""
    rx = re.compile(pattern)
    return sum(1 for line in Path(path).read_text(errors="replace").splitlines()
               if rx.search(line))
