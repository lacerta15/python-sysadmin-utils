"""Create compressed archives and prune old backups by retention."""
from __future__ import annotations

import tarfile
import time
from pathlib import Path
from typing import List


def create_archive(source: str, dest_dir: str, name: str | None = None) -> str:
    """Create a gzip tar archive of ``source`` inside ``dest_dir``."""
    src = Path(source)
    dest = Path(dest_dir)
    dest.mkdir(parents=True, exist_ok=True)
    stamp = time.strftime("%Y%m%d-%H%M%S")
    base = name or src.name
    archive = dest / f"{base}-{stamp}.tar.gz"
    with tarfile.open(archive, "w:gz") as tar:
        tar.add(src, arcname=src.name)
    return str(archive)


def prune(dest_dir: str, keep: int = 7, pattern: str = "*.tar.gz") -> List[str]:
    """Keep the newest ``keep`` archives, return list of removed paths."""
    files = sorted(Path(dest_dir).glob(pattern),
                   key=lambda p: p.stat().st_mtime, reverse=True)
    removed = []
    for old in files[keep:]:
        old.unlink()
        removed.append(str(old))
    return removed
