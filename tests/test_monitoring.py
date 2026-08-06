from sysadmin_utils.monitoring import prometheus


def test_render_basic():
    text = prometheus.render({"cpu_percent": 12.5}, prefix="host")
    assert "# TYPE host_cpu_percent gauge" in text
    assert "host_cpu_percent 12.5" in text


def test_render_with_labels():
    text = prometheus.render({"up": 1}, prefix="svc",
                             labels=[("instance", "web1")])
    assert 'svc_up{instance="web1"} 1' in text


def test_write_textfile(tmp_path):
    out = tmp_path / "metrics.prom"
    prometheus.write_textfile(str(out), {"load": 0.4})
    assert "sysadmin_load 0.4" in out.read_text()
