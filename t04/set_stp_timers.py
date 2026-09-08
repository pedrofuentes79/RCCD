#!/usr/bin/env python3
import subprocess
import sys


def set_stp_timers(br: str, hello: str | int, max_age: str | int, fwd: str | int) -> None:
    subprocess.run(f"ovs-vsctl set Bridge {br} other_config:stp-hello-time={hello}", shell=True, check=True)
    subprocess.run(f"ovs-vsctl set Bridge {br} other_config:stp-max-age={max_age}", shell=True, check=True)
    subprocess.run(f"ovs-vsctl set Bridge {br} other_config:stp-forward-delay={fwd}", shell=True, check=True)
    print(f"[OK] Timers set on {br}: hello={hello}s max_age={max_age}s forward_delay={fwd}s")


def main() -> None:
    if len(sys.argv) < 5:
        print(f"Uso: {sys.argv[0]} <bridge> <hello_time> <max_age> <forward_delay>")
        sys.exit(1)
    br: str = sys.argv[1]
    hello: str = sys.argv[2]
    max_age: str = sys.argv[3]
    fwd: str = sys.argv[4]
    set_stp_timers(br, hello, max_age, fwd)


if __name__ == "__main__":
    main()
