"""Return the last N lines of a file efficiently."""
from __future__ import annotations

import os
from typing import List


def tail(path: str, lines: int = 10, block: int = 4096) -> List[str]:
    """Read the last ``lines`` lines without loading the whole file."""
    with open(path, "rb") as f:
        f.seek(0, os.SEEK_END)
        size = f.tell()
        data = b""
        while size > 0 and data.count(b"\n") <= lines:
            step = min(block, size)
            size -= step
            f.seek(size)
            data = f.read(step) + data
    return data.decode(errors="replace").splitlines()[-lines:]
