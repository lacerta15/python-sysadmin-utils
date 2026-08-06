"""Render metrics in Prometheus text exposition format."""
from __future__ import annotations

from typing import Dict, Iterable, Tuple


def render(metrics: Dict[str, float], prefix: str = "sysadmin",
           labels: Iterable[Tuple[str, str]] = ()) -> str:
    """Render a flat metrics dict as Prometheus textfile lines."""
    label_str = ""
    label_items = list(labels)
    if label_items:
        inner = ",".join(f'{k}="{v}"' for k, v in label_items)
        label_str = "{" + inner + "}"
    lines = []
    for name, value in metrics.items():
        metric = f"{prefix}_{name}"
        lines.append(f"# TYPE {metric} gauge")
        lines.append(f"{metric}{label_str} {value}")
    return "\n".join(lines) + "\n"


def write_textfile(path: str, metrics: Dict[str, float],
                   prefix: str = "sysadmin") -> None:
    """Write metrics to a node_exporter textfile-collector file atomically."""
    tmp = f"{path}.tmp"
    with open(tmp, "w") as f:
        f.write(render(metrics, prefix=prefix))
    import os
    os.replace(tmp, path)
