# Changelog

All notable changes to this project are documented in this file.
The format is based on [Keep a Changelog](https://keepachangelog.com/).

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
