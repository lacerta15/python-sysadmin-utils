from sysadmin_utils.notify.alerting import format_alert, alert_on_failures


def test_no_alert_when_all_ok():
    sent = []
    results = [{"check": "cpu", "value": 5, "threshold": 85, "ok": True}]
    assert alert_on_failures(results, sent.append) is False
    assert sent == []


def test_alert_sent_on_failure():
    sent = []
    results = [{"check": "disk", "value": 95, "threshold": 90, "ok": False}]
    assert alert_on_failures(results, sent.append) is True
    assert "disk" in sent[0]


def test_format_alert():
    msg = format_alert([{"check": "mem", "value": 92.0, "threshold": 85}])
    assert "mem" in msg and "exceeds" in msg
