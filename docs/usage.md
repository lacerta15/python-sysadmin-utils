# Usage Guide

## System health

```python
from sysadmin_utils.system import health

metrics = health.collect()
status = health.evaluate(metrics, cpu=90, mem=90, disk=95)
print(health.format_report(metrics))
```

## Detecting resource hogs

```python
from sysadmin_utils.system.processes import flag_hogs

for proc in flag_hogs(cpu=75, mem=75):
    print(proc["pid"], proc["name"], proc["cpu_percent"])
```

## Checking failed services

```python
from sysadmin_utils.system import services

for unit in services.failed_units():
    print("FAILED:", unit)
```

## Certificate monitoring

```python
from sysadmin_utils.network import ssl_check

info = ssl_check.cert_info("example.com")
if info["expiring_soon"]:
    print("Renew soon:", info["days_left"], "days left")
```

## Backups with retention

```python
from sysadmin_utils.backup import archive

path = archive.create_archive("/etc", "/backups", name="etc")
removed = archive.prune("/backups", keep=7)
```

## Consolidated report

```python
from sysadmin_utils.reporting import collector, formatters

report = collector.collect_report()
print(formatters.to_markdown(report))
```

From the CLI:

```bash
sysadmin report --format markdown
sysadmin checks           # exit code 1 if any threshold is exceeded
```
