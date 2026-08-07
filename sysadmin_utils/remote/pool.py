"""Fan a command out across many hosts and aggregate the results."""
from __future__ import annotations

from typing import Callable, Dict, List

from .ssh import run_remote


def run_on_hosts(hosts: List[Dict[str, str]], command: str,
                 runner: Callable = None) -> Dict[str, Dict]:
    """Run ``command`` on each host, returning a per-host result summary."""
    results: Dict[str, Dict] = {}
    for entry in hosts:
        host, user = entry["host"], entry.get("user", "root")
        kwargs = {"runner": runner} if runner else {}
        res = run_remote(host, command, user=user, **kwargs)
        results[host] = {
            "ok": res.ok,
            "returncode": res.returncode,
            "stdout": res.stdout.strip(),
            "stderr": res.stderr.strip(),
        }
    return results


def summarize(results: Dict[str, Dict]) -> Dict[str, int]:
    """Return counts of succeeded/failed hosts."""
    ok = sum(1 for r in results.values() if r["ok"])
    return {"total": len(results), "ok": ok, "failed": len(results) - ok}
