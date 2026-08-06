"""YAML/JSON configuration loader with environment overrides."""
from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any, Dict

try:
    import yaml  # type: ignore
except ImportError:  # pragma: no cover
    yaml = None


def load_config(path: str | os.PathLike) -> Dict[str, Any]:
    """Load a config file (.yaml/.yml/.json) into a dict."""
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"Config not found: {p}")
    text = p.read_text(encoding="utf-8")
    if p.suffix in (".yaml", ".yml"):
        if yaml is None:
            raise RuntimeError("PyYAML is required to read YAML configs")
        return yaml.safe_load(text) or {}
    if p.suffix == ".json":
        return json.loads(text)
    raise ValueError(f"Unsupported config format: {p.suffix}")


def env_override(config: Dict[str, Any], prefix: str = "SU_") -> Dict[str, Any]:
    """Override config keys from environment variables (SU_<KEY>)."""
    result = dict(config)
    for key, value in os.environ.items():
        if key.startswith(prefix):
            result[key[len(prefix):].lower()] = value
    return result
