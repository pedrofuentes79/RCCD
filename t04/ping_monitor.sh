#!/bin/bash
# ping_monitor.sh: Monitorea conectividad hacia un destino registrando timestamps ISO
TARGET="${1:-10.0.0.11}"
OUT="${2:-ping.log}"

> "$OUT"
while true; do
  ts=$(date -Iseconds)
  if ping -c 1 -W 1 "$TARGET" >/dev/null 2>&1; then
    echo "$ts OK" | tee -a "$OUT"
  else
    echo "$ts FAIL" | tee -a "$OUT"
  fi
  sleep 1
done