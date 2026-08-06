from sysadmin_utils.system import health


def test_collect_keys():
    m = health.collect()
    for key in ("cpu_percent", "mem_percent", "disk_percent", "hostname"):
        assert key in m


def test_evaluate_warn():
    metrics = {"cpu_percent": 99, "mem_percent": 10, "disk_percent": 10}
    status = health.evaluate(metrics)
    assert status["cpu"] == "WARN"
    assert status["overall"] == "WARN"


def test_evaluate_ok():
    metrics = {"cpu_percent": 5, "mem_percent": 5, "disk_percent": 5}
    assert health.evaluate(metrics)["overall"] == "OK"
