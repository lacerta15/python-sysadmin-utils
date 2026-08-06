from sysadmin_utils.core.shell import run


def test_run_success():
    r = run(["echo", "hello"])
    assert r.ok
    assert r.stdout.strip() == "hello"
    assert r.returncode == 0


def test_run_string_command():
    r = run("echo world")
    assert "world" in r.stdout


def test_run_failure_not_raised_by_default():
    r = run(["false"])
    assert not r.ok
    assert r.returncode != 0
