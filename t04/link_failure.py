#!/usr/bin/env python3
import subprocess
import sys
import time


def toggle_link(iface: str, down_seconds: int) -> None:
    subprocess.run(f"ip link set {iface} down", shell=True, check=True)
    print(f"[FAIL] {iface} down for {down_seconds}s")
    time.sleep(down_seconds)
    subprocess.run(f"ip link set {iface} up", shell=True, check=True)
    print(f"[RECOVER] {iface} up")


def main() -> None:
    if len(sys.argv) < 3:
        print(f"Uso: {sys.argv[0]} <interface> <down_seconds>")
        sys.exit(1)
    iface: str = sys.argv[1]
    down_seconds: int = int(sys.argv[2])
    toggle_link(iface, down_seconds)


if __name__ == "__main__":
    main()
