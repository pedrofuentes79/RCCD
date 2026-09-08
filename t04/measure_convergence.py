#!/usr/bin/env python3
from __future__ import annotations
import sys
from datetime import datetime
from pathlib import Path


# Lee un log de ping con timestamps y calcula downtime
# Uso: python3 measure_convergence.py ping.log
#
# Formato recomendado de log:
# 2026-02-07T12:00:01 OK time=0.40 ms
# 2026-02-07T12:00:02 FAIL
# ...


def calculate_downtime(log_path: Path | str) -> float | None:
    """Lee un log de ping con timestamps y calcula el tiempo total de downtime en segundos."""
    with open(log_path, "r", encoding="utf-8") as f:
        log = f.read().splitlines()

    t_fail: datetime | None = None
    t_recover: datetime | None = None

    for line in log:
        if not line.strip():
            continue
        parts = line.split(maxsplit=2)
        if len(parts) < 2:
            continue
        ts_str, status = parts[0], parts[1]
        try:
            ts = datetime.fromisoformat(ts_str)
        except ValueError:
            continue

        if status == "FAIL" and t_fail is None:
            t_fail = ts
        if status == "OK" and t_fail is not None:
            t_recover = ts
            break

    if t_fail and t_recover:
        return (t_recover - t_fail).total_seconds()
    return None


def main() -> None:
    if len(sys.argv) < 2:
        print(f"Uso: {sys.argv[0]} <ping.log>")
        sys.exit(1)

    dt: float | None = calculate_downtime(sys.argv[1])
    if dt is not None:
        print(f"Downtime (s): {dt:.3f}")
    else:
        print("No se pudo determinar downtime (falta FAIL/OK).")


if __name__ == "__main__":
    main()
