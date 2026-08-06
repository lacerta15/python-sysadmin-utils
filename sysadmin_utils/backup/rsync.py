"""Wrapper around rsync for mirroring directories."""
from __future__ import annotations

from typing import List

from ..core.shell import run


def mirror(source: str, dest: str, delete: bool = False,
           extra: List[str] | None = None):
    """Mirror ``source`` to ``dest`` using rsync -a. Returns shell Result."""
    cmd = ["rsync", "-a", "--stats"]
    if delete:
        cmd.append("--delete")
    if extra:
        cmd.extend(extra)
    cmd.extend([source, dest])
    return run(cmd, timeout=3600)


def dry_run(source: str, dest: str) -> str:
    """Return the list of changes rsync would make, without applying them."""
    result = run(["rsync", "-a", "--dry-run", "--itemize-changes",
                  source, dest], timeout=600)
    return result.stdout
