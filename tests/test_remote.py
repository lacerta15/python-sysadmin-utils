from sysadmin_utils.core.shell import Result
from sysadmin_utils.remote import inventory, pool, ssh


def fake_runner_factory(rc=0, out="done", err=""):
    def _runner(cmd, timeout=20):
        return Result(" ".join(cmd), rc, out, err)
    return _runner


def test_parse_inventory(tmp_path):
    f = tmp_path / "hosts"
    f.write_text("# prod\nweb01\nadmin@db01\n\n")
    hosts = inventory.parse_inventory(str(f))
    assert hosts == [
        {"user": "root", "host": "web01"},
        {"user": "admin", "host": "db01"},
    ]


def test_run_remote_uses_injected_runner():
    res = ssh.run_remote("web01", "uptime",
                         runner=fake_runner_factory(out="up 5 days"))
    assert res.ok
    assert res.stdout == "up 5 days"


def test_run_on_hosts_and_summary():
    hosts = [{"user": "root", "host": "a"}, {"user": "root", "host": "b"}]
    results = pool.run_on_hosts(hosts, "hostname",
                                runner=fake_runner_factory(out="ok"))
    assert set(results) == {"a", "b"}
    summary = pool.summarize(results)
    assert summary == {"total": 2, "ok": 2, "failed": 0}


def test_summary_counts_failures():
    hosts = [{"user": "root", "host": "a"}]
    results = pool.run_on_hosts(hosts, "false",
                               runner=fake_runner_factory(rc=1, out="", err="boom"))
    assert pool.summarize(results)["failed"] == 1
