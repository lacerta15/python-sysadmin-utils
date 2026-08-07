# Changelog

All notable changes to this project are documented in this file.
The format is based on [Keep a Changelog](https://keepachangelog.com/).

## [0.3.0] - 2026-08-07

### Added
- Remote module: SSH inventory parser, single-host runner (injectable executor),
  multi-host fan-out with aggregation, and a `remote-run` CLI command.
- Reporting module: consolidated report collector plus text/JSON/Markdown formatters.
- Checks module: config-driven threshold check runner with pass/fail summary.
- CLI: new `report`, `checks`, `uptime`, `sensors` and `logscan` subcommands.

## [0.2.0] - 2026-08-06

### Added
- Core: retry/backoff decorator, timing helpers, humanize (bytes/duration),
  central overridable defaults.
- System: detailed CPU, memory, network I/O, hardware sensors, uptime modules.
- Security module: file integrity checksums + manifest diff, auth-log failed
  login parser, listening-port allowlist audit.
- Monitoring module: Prometheus textfile exposition writer and HTTP health check.
- Backup: rsync mirror wrapper with dry-run.
- CLI: new `ports` and `httpcheck` subcommands.
- Expanded test suite across new modules.

## [0.1.0] - 2026-08-06

### Added
- Core helpers: safe subprocess wrapper, YAML/JSON config loader, logging setup.
- System module: health snapshot, disk report, process inspection,
  systemd service management, user/session audit.
- Network module: TCP reachability, DNS resolution, listening ports,
  TLS certificate expiry checker.
- Logs module: level-aware log analyzer and efficient file tailer.
- Backup module: archive creation with retention pruning.
- Cloud module: hardened Cloudera Manager API client.
- Notify module: Slack webhook and SMTP email senders.
- Unified `sysadmin` CLI with `health`, `top`, `check`, and `ssl` commands.
- Test suite (pytest) and GitHub Actions CI.

### Changed
- Migrated legacy `utils/` scripts into the `sysadmin_utils` package,
  leaving deprecation shims for backward compatibility.
