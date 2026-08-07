"""Unified command-line entrypoint for sysadmin_utils."""
from __future__ import annotations

import argparse
import json
import sys

from . import __version__
from .system import health, processes, uptime, sensors
from .network import connectivity, ssl_check, ports as netports
from .monitoring import http_check
from .logs import analyzer
from .reporting import collector, formatters
from .checks import runner
from .remote import inventory as rinv, pool as rpool
from .monitoring import exporter
from .checks import watch
from .notify import slack


def _cmd_health(args) -> int:
    metrics = health.collect()
    if args.json:
        print(json.dumps(metrics, indent=2))
    else:
        print(health.format_report(metrics))
    return 0 if health.evaluate(metrics)["overall"] == "OK" else 1


def _cmd_top(args) -> int:
    for p in processes.top_processes(limit=args.limit):
        print(f"{p['pid']:>7} {p['cpu_percent']:>5.1f}% "
              f"{p['memory_percent']:>5.1f}% {p['name']}")
    return 0


def _cmd_check(args) -> int:
    result = connectivity.tcp_check(args.host, args.port)
    print(json.dumps(result))
    return 0 if result["open"] else 1


def _cmd_ssl(args) -> int:
    info = ssl_check.cert_info(args.host, args.port)
    print(f"{info['host']}: expires {info['expires']} "
          f"({info['days_left']} days left)")
    return 1 if info["expiring_soon"] else 0


def _cmd_ports(args) -> int:
    for p in netports.listening_ports():
        print(f"{p['port']:>6}  pid={p['pid']}  {p['ip']}")
    return 0


def _cmd_httpcheck(args) -> int:
    result = http_check.check(args.url, expect=args.expect)
    print(json.dumps(result))
    return 0 if result["healthy"] else 1


def _cmd_uptime(args) -> int:
    print(f"up {uptime.uptime_human()} (since {uptime.boot_time():%Y-%m-%d %H:%M})")
    return 0


def _cmd_sensors(args) -> int:
    temps = sensors.temperatures()
    if not temps:
        print("no temperature sensors available")
        return 0
    for chip, entries in temps.items():
        for e in entries:
            print(f"{chip:20s} {e['label']:20s} {e['current']:.1f}C")
    return 0


def _cmd_logscan(args) -> int:
    result = analyzer.analyze(args.path, top=args.top)
    print(f"file: {result['file']}  ({result['total_lines']} lines)")
    print("levels:", result["levels"])
    if result["top_errors"]:
        print("top errors:")
        for line, count in result["top_errors"]:
            print(f"  {count:>4}x  {line[:100]}")
    return 0


def _cmd_report(args) -> int:
    report = collector.collect_report()
    if args.format == "json":
        print(formatters.to_json(report))
    elif args.format == "markdown":
        print(formatters.to_markdown(report))
    else:
        print(formatters.to_text(report))
    return 0 if report["health_status"]["overall"] == "OK" else 1


def _cmd_checks(args) -> int:
    results = runner.run_checks()
    for r in results:
        flag = "OK " if r["ok"] else "FAIL"
        print(f"[{flag}] {r['check']:5s} {r['value']:.1f} (max {r['threshold']})")
    return 0 if runner.all_passing(results) else 1


def _cmd_remote_run(args) -> int:
    hosts = rinv.parse_inventory(args.inventory, default_user=args.user)
    results = rpool.run_on_hosts(hosts, args.command)
    for host, r in results.items():
        flag = "OK " if r["ok"] else "FAIL"
        print(f"[{flag}] {host}: {r['stdout'] or r['stderr']}")
    summary = rpool.summarize(results)
    print(f"-- {summary['ok']}/{summary['total']} ok, {summary['failed']} failed")
    return 0 if summary["failed"] == 0 else 1


def _cmd_exporter(args) -> int:
    print(f"Serving metrics on http://0.0.0.0:{args.port}/metrics (Ctrl+C to stop)")
    try:
        exporter.serve(args.port)
    except KeyboardInterrupt:
        print("stopped")
    return 0


def _cmd_watch(args) -> int:
    notifier = None
    if args.slack_webhook:
        notifier = lambda msg: slack.send(args.slack_webhook, msg)  # noqa: E731
    results = watch.run_once(notifier=notifier)
    for r in results:
        flag = "OK " if r["ok"] else "FAIL"
        print(f"[{flag}] {r['check']:5s} {r['value']:.1f} (max {r['threshold']})")
    return 0 if all(r["ok"] for r in results) else 1


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="sysadmin", description="Sysadmin utilities toolkit")
    parser.add_argument("--version", action="version",
                        version=f"%(prog)s {__version__}")
    sub = parser.add_subparsers(dest="command", required=True)

    h = sub.add_parser("health", help="show system health snapshot")
    h.add_argument("--json", action="store_true")
    h.set_defaults(func=_cmd_health)

    t = sub.add_parser("top", help="show top processes by CPU")
    t.add_argument("--limit", type=int, default=10)
    t.set_defaults(func=_cmd_top)

    c = sub.add_parser("check", help="TCP reachability check")
    c.add_argument("host")
    c.add_argument("port", type=int)
    c.set_defaults(func=_cmd_check)

    s = sub.add_parser("ssl", help="TLS certificate expiry check")
    s.add_argument("host")
    s.add_argument("--port", type=int, default=443)
    s.set_defaults(func=_cmd_ssl)

    p = sub.add_parser("ports", help="list listening ports")
    p.set_defaults(func=_cmd_ports)

    hc = sub.add_parser("httpcheck", help="HTTP endpoint health check")
    hc.add_argument("url")
    hc.add_argument("--expect", type=int, default=200)
    hc.set_defaults(func=_cmd_httpcheck)

    u = sub.add_parser("uptime", help="show system uptime")
    u.set_defaults(func=_cmd_uptime)

    se = sub.add_parser("sensors", help="show hardware temperature sensors")
    se.set_defaults(func=_cmd_sensors)

    ls = sub.add_parser("logscan", help="analyze a log file for errors")
    ls.add_argument("path")
    ls.add_argument("--top", type=int, default=5)
    ls.set_defaults(func=_cmd_logscan)

    rep = sub.add_parser("report", help="consolidated system report")
    rep.add_argument("--format", choices=["text", "json", "markdown"],
                     default="text")
    rep.set_defaults(func=_cmd_report)

    ck = sub.add_parser("checks", help="run threshold checks")
    ck.set_defaults(func=_cmd_checks)

    rr = sub.add_parser("remote-run", help="run a command across hosts via SSH")
    rr.add_argument("inventory")
    rr.add_argument("command")
    rr.add_argument("--user", default="root")
    rr.set_defaults(func=_cmd_remote_run)

    ex = sub.add_parser("exporter", help="serve Prometheus metrics over HTTP")
    ex.add_argument("--port", type=int, default=9877)
    ex.set_defaults(func=_cmd_exporter)

    w = sub.add_parser("watch", help="run checks once, optionally alert to Slack")
    w.add_argument("--slack-webhook", default=None)
    w.set_defaults(func=_cmd_watch)

    return parser


def main(argv=None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
