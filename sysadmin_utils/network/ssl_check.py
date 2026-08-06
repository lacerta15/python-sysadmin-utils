"""Inspect the TLS certificate served by a host and its expiry."""
from __future__ import annotations

import socket
import ssl
from datetime import datetime, timezone
from typing import Dict

_FMT = "%b %d %H:%M:%S %Y %Z"


def cert_info(host: str, port: int = 443, timeout: float = 5.0) -> Dict:
    """Return subject, issuer and days-until-expiry for a host's TLS cert."""
    ctx = ssl.create_default_context()
    with socket.create_connection((host, port), timeout=timeout) as sock:
        with ctx.wrap_socket(sock, server_hostname=host) as ssock:
            cert = ssock.getpeercert()
    not_after = datetime.strptime(cert["notAfter"], _FMT).replace(
        tzinfo=timezone.utc)
    days_left = (not_after - datetime.now(timezone.utc)).days
    subject = dict(x[0] for x in cert.get("subject", []))
    issuer = dict(x[0] for x in cert.get("issuer", []))
    return {
        "host": host,
        "common_name": subject.get("commonName", ""),
        "issuer": issuer.get("organizationName", ""),
        "expires": not_after.isoformat(),
        "days_left": days_left,
        "expiring_soon": days_left <= 30,
    }
