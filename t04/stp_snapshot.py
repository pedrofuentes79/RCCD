#!/usr/bin/env python3
"""
stp_snapshot.py
Captura el estado STP y forwarding de switches OVS en Containernet.

Debe ejecutarse:
- dentro del contenedor
- con la topología levantada

Genera:
- estado STP de cada bridge
- puertos asociados
- tabla MAC (FDB)
"""

import subprocess
import argparse
from datetime import datetime
from pathlib import Path


# Helpers
def sh(cmd: str) -> str:
    result = subprocess.run(
        cmd,
        shell=True,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    return result.stdout.strip()

def now() -> str:
    return datetime.now().isoformat(timespec="seconds")


# Snapshot STP
def snapshot_stp(bridges: list[str], outdir: Path, label: str) -> None:
    outdir.mkdir(exist_ok=True)
    fname = outdir / f"stp_snapshot_{label}.log"

    with fname.open("a") as f:
        f.write(f"# STP Snapshot\n")
        f.write(f"# Timestamp: {now()}\n\n")

        for br in bridges:
            f.write(f"\n===== BRIDGE {br} =====\n")
            f.write(sh(f"ovs-appctl stp/show {br}") + "\n")
        
        f.write(f"\n====================================================\n")

    print(f"[OK] Snapshot STP guardado en {fname}")


# Snapshot MAC (FDB)
def snapshot_mac(bridges: list[str], outdir: Path, label: str) -> None:
    outdir.mkdir(exist_ok=True)
    fname = outdir / f"mac_{label}.log"
    
    with fname.open("a") as f:
        f.write(f"# MAC Snapshot\n")
        f.write(f"# Timestamp: {now()}\n\n")
        
        for br in bridges:
            f.write(f"\n===== BRIDGE {br} =====\n")
            f.write(sh(f"ovs-appctl fdb/show {br}") + "\n")
        
        f.write(f"\n====================================================\n")
        
    print(f"[OK] Snapshot MAC guardado en {fname}")

# Main
def main() -> None:
    parser = argparse.ArgumentParser(description="Snapshot STP + MAC (OVS)")
    parser.add_argument(
        "--bridges",
        nargs="+",
        required=True,
        help="Lista de bridges (ej: s1 s2 s3 s4)"
    )
    parser.add_argument(
        "--label",
        default="manual",
        help="Etiqueta del snapshot (before, after, fail, recover, etc.)"
    )
    parser.add_argument(
        "--outdir",
        default="results",
        help="Directorio de salida"
    )
    parser.add_argument(
        "--mac",
        action="store_true",
        help="Incluir snapshot de tablas MAC"
    )

    args = parser.parse_args()

    outdir = Path(args.outdir)
    snapshot_stp(args.bridges, outdir, args.label)

    if args.mac:
        snapshot_mac(args.bridges, outdir, args.label)

    print("[INFO] Snapshot completo")

if __name__ == "__main__":
    main()
