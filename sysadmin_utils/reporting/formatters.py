"""Render a collected report as text, JSON or Markdown."""
from __future__ import annotations

import json
from typing import Any, Dict


def to_json(report: Dict[str, Any], indent: int = 2) -> str:
    return json.dumps(report, indent=indent)


def to_text(report: Dict[str, Any]) -> str:
    h, s = report["health"], report["health_status"]
    return "\n".join([
        f"Host: {report['hostname']}  ({report['generated']})",
        f"Uptime: {report['uptime']}",
        f"[{s['cpu']}]  CPU  {h['cpu_percent']:.1f}%",
        f"[{s['mem']}]  MEM  {h['mem_percent']:.1f}%",
        f"[{s['disk']}] DISK {h['disk_percent']:.1f}%",
        f"Failed services: {len(report['failed_services'])}",
        f"Overall: {s['overall']}",
    ])


def to_markdown(report: Dict[str, Any]) -> str:
    h, s = report["health"], report["health_status"]
    rows = [
        ("CPU", f"{h['cpu_percent']:.1f}%", s["cpu"]),
        ("Memory", f"{h['mem_percent']:.1f}%", s["mem"]),
        ("Disk", f"{h['disk_percent']:.1f}%", s["disk"]),
    ]
    lines = [
        f"# System Report — {report['hostname']}",
        f"_Generated {report['generated']} · uptime {report['uptime']}_",
        "",
        "| Metric | Value | Status |",
        "|--------|-------|--------|",
    ]
    lines += [f"| {n} | {v} | {st} |" for n, v, st in rows]
    lines.append(f"\n**Overall: {s['overall']}**")
    return "\n".join(lines)
