from sysadmin_utils.monitoring import exporter


def test_build_metrics_text():
    text = exporter.build_metrics_text()
    assert "sysadmin_cpu_percent" in text
    assert "sysadmin_disk_percent" in text
    assert "# TYPE" in text
