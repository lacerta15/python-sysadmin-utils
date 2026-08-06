from sysadmin_utils.core import defaults


def test_default_value():
    assert defaults.get("backup_keep") == 7


def test_env_override(monkeypatch):
    monkeypatch.setenv("SU_CPU_WARN", "50")
    assert defaults.get("cpu_warn") == 50.0
