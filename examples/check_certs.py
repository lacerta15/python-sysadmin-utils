#!/usr/bin/env python3
"""Example: warn about TLS certificates expiring within 30 days."""
from sysadmin_utils.network import ssl_check

HOSTS = ["example.com", "github.com", "cloudera.com"]

for host in HOSTS:
    try:
        info = ssl_check.cert_info(host)
        flag = "  <-- EXPIRING SOON" if info["expiring_soon"] else ""
        print(f"{host:20s} {info['days_left']:>4} days{flag}")
    except Exception as exc:
        print(f"{host:20s} ERROR: {exc}")
