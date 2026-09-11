#!/usr/bin/env bash
# Continuar el parche del header (runs/v5_header_head_multi, 8 epochs) por 4
# epochs mas, arrancando desde el parche ya encontrado: 12 en total.
#
# Es un warm restart, no una continuacion exacta: el coseno del step_size
# arranca de nuevo sobre las 4 epochs. Por eso el step inicial es la mitad del
# original (STEP_SIZE=0.000125); con 0.00025 el primer tramo volveria a sacudir
# un parche que ya esta cerca del minimo. Cambiar con STEP_SIZE=... si se quiere.
# Salida en runs/v5_header_head_multi_ep12/, con las mismas cinco evaluaciones.
#
#   uso (desde experimentos/idiomas):  bash run_header_v5_ep12.sh [MODEL_PATH]
set -euo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INIT="${INIT_PATCH:-runs/v5_header_head_multi/lang_patch_best_train.pt}"
[[ -f "$HERE/$INIT" ]] || { echo "falta $INIT"; exit 1; }
EPOCHS="${EPOCHS:-4}" STEP_SIZE="${STEP_SIZE:-0.000125}" INIT_PATCH="$INIT" \
  NAME="${NAME:-v5_header_head_multi_ep12}" exec bash "$HERE/run_header_v5.sh" "$@"
