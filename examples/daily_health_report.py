#!/usr/bin/env python3
"""Example: collect health metrics and alert to Slack if degraded."""
import os

from sysadmin_utils.system import health
from sysadmin_utils.notify import slack

metrics = health.collect()
status = health.evaluate(metrics)
report = health.format_report(metrics)
print(report)

webhook = os.environ.get("SLACK_WEBHOOK")
if webhook and status["overall"] == "WARN":
    slack.send(webhook, f":rotating_light: Health degraded\n```{report}```")
