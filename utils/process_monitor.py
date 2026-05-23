#!/usr/bin/env python3
"""Monitor and alert on high CPU/memory processes."""
import psutil
import time
import sys

CPU_THRESHOLD  = float(sys.argv[1]) if len(sys.argv) > 1 else 80.0
MEM_THRESHOLD  = float(sys.argv[2]) if len(sys.argv) > 2 else 80.0
INTERVAL       = 10

print(f"Monitoring processes (CPU>{CPU_THRESHOLD}%, MEM>{MEM_THRESHOLD}%)")
print("Press Ctrl+C to stop.\n")

while True:
    print(f"--- {time.strftime('%Y-%m-%d %H:%M:%S')} ---")
    for proc in sorted(psutil.process_iter(['pid','name','cpu_percent','memory_percent']),
                       key=lambda p: p.info['cpu_percent'], reverse=True)[:5]:
        p = proc.info
        flag = ""
        if p['cpu_percent'] > CPU_THRESHOLD: flag += " [HIGH CPU]"
        if p['memory_percent'] > MEM_THRESHOLD: flag += " [HIGH MEM]"
        if flag:
            print(f"PID {p['pid']:6d} | CPU {p['cpu_percent']:5.1f}% | "
                  f"MEM {p['memory_percent']:5.1f}% | {p['name']}{flag}")
    time.sleep(INTERVAL)
