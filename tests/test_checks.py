from sysadmin_utils.checks import runner


def test_run_checks_structure():
    results = runner.run_checks({"cpu_max": 100, "mem_max": 100, "disk_max": 100})
    names = {r["check"] for r in results}
    assert names == {"cpu", "mem", "disk"}
    assert runner.all_passing(results) is True


def test_run_checks_failure():
    results = runner.run_checks({"cpu_max": -1, "mem_max": 100, "disk_max": 100})
    cpu = next(r for r in results if r["check"] == "cpu")
    assert cpu["ok"] is False
    assert runner.all_passing(results) is False
