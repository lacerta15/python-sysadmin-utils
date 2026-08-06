"""Safe subprocess helpers."""
from __future__ import annotations

import shlex
import subprocess
from dataclasses import dataclass


@dataclass
class Result:
    """Outcome of a shell command."""
    command: str
    returncode: int
    stdout: str
    stderr: str

    @property
    def ok(self) -> bool:
        return self.returncode == 0


def run(command, timeout: int = 30, check: bool = False) -> Result:
    """Run a command and capture its output.

    ``command`` may be a string (parsed with shlex) or a list of args.
    """
    if isinstance(command, str):
        args = shlex.split(command)
        printable = command
    else:
        args = list(command)
        printable = " ".join(shlex.quote(a) for a in args)

    proc = subprocess.run(
        args, capture_output=True, text=True, timeout=timeout
    )
    result = Result(printable, proc.returncode, proc.stdout, proc.stderr)
    if check and not result.ok:
        raise RuntimeError(f"Command failed ({result.returncode}): {printable}\n{result.stderr}")
    return result
