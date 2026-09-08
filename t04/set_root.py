#!/usr/bin/env python3
import subprocess
import sys


def sh(cmd: str) -> None:
    subprocess.run(cmd, shell=True, check=True)


def set_bridge_priority(sw: str, prio: str | int) -> None:
    sh(f"ovs-vsctl set Bridge {sw} other_config:stp-priority={prio}")
    print(f"[OK] Root preference set: {sw} stp-priority={prio}")


def main() -> None:
    if len(sys.argv) < 3:
        print(f"Uso: {sys.argv[0]} <switch> <priority>")
        sys.exit(1)
    sw: str = sys.argv[1]
    prio: str = sys.argv[2]
    set_bridge_priority(sw, prio)


if __name__ == "__main__":
    main()
