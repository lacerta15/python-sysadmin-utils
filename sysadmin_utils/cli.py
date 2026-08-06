"""Unified command-line entrypoint for sysadmin_utils."""
from __future__ import annotations

import argparse
import json
import sys

from . import __version__
from .system import health, processes
from .network import connectivity, ssl_check, ports as netports
from .monitoring import http_check


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

    return parser


def main(argv=None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
