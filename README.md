# Python Sysadmin Utilities

[![CI](https://github.com/lacerta15/python-sysadmin-utils/actions/workflows/ci.yml/badge.svg)](https://github.com/lacerta15/python-sysadmin-utils/actions/workflows/ci.yml)
![Python](https://img.shields.io/badge/python-3.8%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)

A small, dependency-light toolkit of Python utilities for Linux system
administration, DevOps automation, monitoring and reporting. Ships both an
importable package (`sysadmin_utils`) and a `sysadmin` command-line tool.

## Features

| Area     | Module                          | What it does                                  |
|----------|---------------------------------|-----------------------------------------------|
| System   | `system.health`                 | CPU / memory / disk / load snapshot + status  |
| System   | `system.disk`                   | Disk usage report (local & remote via SSH)    |
| System   | `system.processes`              | Top processes and resource-hog detection      |
| System   | `system.services`               | systemd status, failed units, restart         |
| System   | `system.users`                  | Human accounts and active login sessions      |
| Network  | `network.connectivity`          | TCP reachability + DNS resolution             |
| Network  | `network.ports`                 | Enumerate listening sockets                   |
| Network  | `network.ssl_check`             | TLS certificate expiry checking               |
| Logs     | `logs.analyzer` / `logs.tailer` | Log level summary, top errors, efficient tail |
| Backup   | `backup.archive`                | Tar.gz archives with retention pruning        |
| Cloud    | `cloud.cloudera`                | Cloudera Manager API client                   |
| Notify   | `notify.slack` / `notify.email` | Slack webhook and SMTP alerts                 |

## Installation

```bash
git clone https://github.com/lacerta15/python-sysadmin-utils.git
cd python-sysadmin-utils
pip install -e .
```

## CLI usage

```bash
sysadmin health            # system health snapshot (exit 1 if degraded)
sysadmin health --json     # machine-readable output
sysadmin top --limit 5     # top 5 processes by CPU
sysadmin check db01 5432   # TCP reachability check
sysadmin ssl example.com   # TLS certificate expiry
```

## Library usage

```python
from sysadmin_utils.system import health
from sysadmin_utils.network import ssl_check

print(health.format_report(health.collect()))

info = ssl_check.cert_info("github.com")
print(info["days_left"], "days until expiry")
```

More runnable examples live in [`examples/`](examples/).

## Development

```bash
make dev      # install with dev extras
make test     # run the test suite
make lint     # flake8
make cov      # coverage report
```

See [CONTRIBUTING.md](CONTRIBUTING.md) and the [CHANGELOG](CHANGELOG.md).

## License

Released under the [MIT License](LICENSE).

