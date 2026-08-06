import json

import pytest

from sysadmin_utils.core.config import load_config, env_override


def test_load_json(tmp_path):
    p = tmp_path / "c.json"
    p.write_text(json.dumps({"a": 1, "b": "x"}))
    cfg = load_config(p)
    assert cfg == {"a": 1, "b": "x"}


def test_missing_file(tmp_path):
    with pytest.raises(FileNotFoundError):
        load_config(tmp_path / "nope.json")


def test_env_override(monkeypatch):
    monkeypatch.setenv("SU_HOST", "server1")
    cfg = env_override({"host": "old"})
    assert cfg["host"] == "server1"
