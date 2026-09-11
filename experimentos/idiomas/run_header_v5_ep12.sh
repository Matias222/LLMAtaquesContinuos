#!/usr/bin/env bash
# Igual que run_header_v5.sh (parche en el header, head 8, en/es/de, L2 0.0725)
# pero con 12 epochs en vez de 8. El annealing coseno se estira a los 12*7*20
# pasos, asi que no es "8 epochs y 4 mas": la trayectoria del lr es otra.
# Salida en runs/v5_header_head_multi_ep12/, con las mismas cinco evaluaciones.
#
#   uso (desde experimentos/idiomas):  bash run_header_v5_ep12.sh [MODEL_PATH]
set -euo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
EPOCHS=12 NAME="${NAME:-v5_header_head_multi_ep12}" exec bash "$HERE/run_header_v5.sh" "$@"
