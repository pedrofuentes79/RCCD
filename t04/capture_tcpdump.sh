#!/bin/bash
# Uso: ./capture_tcpdump.sh [interfaz] [archivo_salida]
IFACE="${1:-s4-eth4}"
OUT="${2:-results/stp_traffic.pcap}"

mkdir -p "$(dirname "$OUT")"

# Captura BPDUs STP (dest MAC tipica 01:80:c2:00:00:00) con flushing inmediato (-l -U)
exec tcpdump -l -U -i "$IFACE" -e -nn -s 0 -w "$OUT" ether dst 01:80:c2:00:00:00

