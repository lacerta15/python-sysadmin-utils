"""Send messages to Slack via an incoming webhook."""
from __future__ import annotations

import requests


def send(webhook_url: str, text: str, username: str = "sysadmin-utils",
         timeout: int = 10) -> bool:
    """Post ``text`` to a Slack incoming webhook. Returns True on success."""
    payload = {"text": text, "username": username}
    resp = requests.post(webhook_url, json=payload, timeout=timeout)
    return resp.status_code == 200
