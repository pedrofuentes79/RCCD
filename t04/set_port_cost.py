#!/usr/bin/env python3
import subprocess
import sys


def sh(cmd: str) -> None:
    subprocess.run(cmd, shell=True, check=True)


def set_port_cost(port: str, cost: str | int) -> None:
    sh(f"ovs-vsctl set Port {port} other_config:stp-path-cost={cost}")
    print(f"[OK] Port cost set: {port} stp-path-cost={cost}")


def main() -> None:
    if len(sys.argv) < 3:
        print(f"Uso: {sys.argv[0]} <port> <cost>")
        sys.exit(1)
    port: str = sys.argv[1]
    cost: str = sys.argv[2]
    set_port_cost(port, cost)


if __name__ == "__main__":
    main()
