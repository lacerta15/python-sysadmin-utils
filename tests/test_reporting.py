from sysadmin_utils.reporting import collector, formatters


def _sample():
    return {
        "generated": "2026-08-06T12:00:00",
        "hostname": "host1",
        "uptime": "1d 2h",
        "health": {"cpu_percent": 10.0, "mem_percent": 20.0, "disk_percent": 30.0},
        "health_status": {"cpu": "OK", "mem": "OK", "disk": "OK", "overall": "OK"},
        "failed_services": [],
    }


def test_collect_report_keys():
    report = collector.collect_report()
    for key in ("generated", "hostname", "uptime", "health", "health_status"):
        assert key in report


def test_to_json_roundtrip():
    import json
    out = formatters.to_json(_sample())
    assert json.loads(out)["hostname"] == "host1"


def test_to_text_and_markdown():
    assert "Host: host1" in formatters.to_text(_sample())
    md = formatters.to_markdown(_sample())
    assert md.startswith("# System Report")
    assert "| Metric | Value | Status |" in md
