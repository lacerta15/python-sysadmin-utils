"""Cloudera Manager API client.

Migrated and hardened from the original utils/cloudera_api.py:
adds TLS/timeout handling, health summaries and typed helpers.
"""
from __future__ import annotations

from typing import Dict, List

import requests


class ClouderaClient:
    """Minimal client for the Cloudera Manager REST API."""

    def __init__(self, host: str, user: str = "admin", password: str = "admin",
                 version: str = "v51", port: int = 7180, tls: bool = False,
                 timeout: int = 15):
        scheme = "https" if tls else "http"
        self.base = f"{scheme}://{host}:{port}/api/{version}"
        self.session = requests.Session()
        self.session.auth = (user, password)
        self.session.headers.update({"Content-Type": "application/json"})
        self.timeout = timeout
        self.verify = tls

    def get(self, path: str) -> Dict:
        r = self.session.get(f"{self.base}{path}", timeout=self.timeout,
                             verify=self.verify)
        r.raise_for_status()
        return r.json()

    def post(self, path: str, data: Dict | None = None) -> Dict:
        r = self.session.post(f"{self.base}{path}", json=data,
                              timeout=self.timeout, verify=self.verify)
        r.raise_for_status()
        return r.json()

    def list_clusters(self) -> List[Dict]:
        return self.get("/clusters").get("items", [])

    def cluster_services(self, cluster: str) -> List[Dict]:
        return self.get(f"/clusters/{cluster}/services").get("items", [])

    def restart_service(self, cluster: str, service: str) -> Dict:
        return self.post(f"/clusters/{cluster}/services/{service}/commands/restart")

    def unhealthy_services(self, cluster: str) -> List[Dict]:
        """Return services whose health is not GOOD."""
        return [s for s in self.cluster_services(cluster)
                if s.get("healthSummary") not in ("GOOD", None)]
