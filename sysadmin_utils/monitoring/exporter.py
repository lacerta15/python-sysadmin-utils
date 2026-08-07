"""Expose live health metrics over HTTP in Prometheus format."""
from __future__ import annotations

import http.server
from typing import Dict

from ..system import health
from . import prometheus


def build_metrics_text(prefix: str = "sysadmin") -> str:
    """Collect current metrics and render them as Prometheus text."""
    m = health.collect()
    metrics: Dict[str, float] = {
        "cpu_percent": m["cpu_percent"],
        "mem_percent": m["mem_percent"],
        "disk_percent": m["disk_percent"],
    }
    return prometheus.render(metrics, prefix=prefix)


class MetricsHandler(http.server.BaseHTTPRequestHandler):
    """Serve /metrics with the current snapshot."""

    def do_GET(self):  # noqa: N802 (stdlib naming)
        if self.path != "/metrics":
            self.send_response(404)
            self.end_headers()
            return
        body = build_metrics_text().encode()
        self.send_response(200)
        self.send_header("Content-Type", "text/plain; version=0.0.4")
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, *args):  # silence default logging
        pass


def serve(port: int = 9877) -> None:
    """Start a blocking HTTP server exposing /metrics."""
    server = http.server.HTTPServer(("", port), MetricsHandler)
    server.serve_forever()
