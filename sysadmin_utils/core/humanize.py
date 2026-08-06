"""Human-friendly formatting of sizes and durations."""
from __future__ import annotations


def bytes_to_human(num: float, suffix: str = "B") -> str:
    """Convert a byte count into a readable string (e.g. 1.5 GiB)."""
    for unit in ("", "Ki", "Mi", "Gi", "Ti", "Pi"):
        if abs(num) < 1024.0:
            return f"{num:3.1f} {unit}{suffix}"
        num /= 1024.0
    return f"{num:.1f} Ei{suffix}"


def seconds_to_human(seconds: float) -> str:
    """Convert seconds into a compact d/h/m/s string."""
    seconds = int(seconds)
    days, rem = divmod(seconds, 86400)
    hours, rem = divmod(rem, 3600)
    minutes, secs = divmod(rem, 60)
    parts = []
    if days:
        parts.append(f"{days}d")
    if hours:
        parts.append(f"{hours}h")
    if minutes:
        parts.append(f"{minutes}m")
    parts.append(f"{secs}s")
    return " ".join(parts)
