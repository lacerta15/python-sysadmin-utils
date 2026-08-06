"""File integrity via checksums and manifest comparison."""
from __future__ import annotations

import hashlib
from pathlib import Path
from typing import Dict


def sha256(path: str, block: int = 65536) -> str:
    """Return the SHA-256 hex digest of a file."""
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(block), b""):
            h.update(chunk)
    return h.hexdigest()


def build_manifest(root: str, pattern: str = "**/*") -> Dict[str, str]:
    """Return {relative_path: sha256} for all files under ``root``."""
    base = Path(root)
    manifest = {}
    for p in base.glob(pattern):
        if p.is_file():
            manifest[str(p.relative_to(base))] = sha256(str(p))
    return manifest


def diff_manifest(old: Dict[str, str], new: Dict[str, str]) -> Dict[str, list]:
    """Compare two manifests, returning added/removed/changed paths."""
    old_keys, new_keys = set(old), set(new)
    changed = [k for k in old_keys & new_keys if old[k] != new[k]]
    return {
        "added": sorted(new_keys - old_keys),
        "removed": sorted(old_keys - new_keys),
        "changed": sorted(changed),
    }
