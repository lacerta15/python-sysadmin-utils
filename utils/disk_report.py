#!/usr/bin/env python3
"""Generate disk usage report across multiple servers via SSH."""
import subprocess
import argparse
import json
from datetime import datetime

def get_disk_usage(host, user="root"):
    try:
        result = subprocess.run(
            ["ssh", "-o", "ConnectTimeout=5", f"{user}@{host}",
             "df -h --output=source,size,used,avail,pcent,target"],
            capture_output=True, text=True, timeout=10
        )
        return result.stdout
    except Exception as e:
        return f"ERROR: {e}"

def main():
    parser = argparse.ArgumentParser(description="Disk usage report")
    parser.add_argument("hosts", nargs="+", help="Hostnames to check")
    parser.add_argument("--user", default="root")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    report = {"generated": datetime.now().isoformat(), "hosts": {}}

    for host in args.hosts:
        print(f"\n=== {host} ===")
        output = get_disk_usage(host, args.user)
        print(output)
        report["hosts"][host] = output

    if args.json:
        with open(f"disk_report_{datetime.now().strftime('%Y%m%d')}.json", "w") as f:
            json.dump(report, f, indent=2)
        print("\nJSON report saved.")

if __name__ == "__main__":
    main()
