from sysadmin_utils.checks import watch


def test_run_once_alerts_on_failure():
    sent = []
    watch.run_once({"cpu_max": -1}, notifier=sent.append)
    assert sent and "cpu" in sent[0]


def test_run_once_no_alert_when_healthy():
    sent = []
    results = watch.run_once({"cpu_max": 100, "mem_max": 100, "disk_max": 100},
                             notifier=sent.append)
    assert sent == []
    assert len(results) == 3
