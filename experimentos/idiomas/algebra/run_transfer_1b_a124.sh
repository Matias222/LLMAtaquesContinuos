#!/usr/bin/env bash
# Parche de frances transferido al 1B, UNA sola escala (a=1.24), sobre held-out
# y open 1, mapeado y control. Reusa los parches que ya escribio la etapa `map`
# de run_transfer_1b_goalall.sh; los reportes llevan sufijo para no pisar el
# barrido completo:
#     algebra/runs/transfer_1b_fr/{mapeado,control}/cross_lang_{heldout,open}_a1.24.md
#
#   uso:  bash algebra/run_transfer_1b_a124.sh [MODEL_3B] [MODEL_1B]
#   variables:  DEVICE (cuda:0)   N (0 = todo)   A (1.24)
set -euo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
A="${A:-1.24}"
ALPHAS="$A" STAGES="heldout open" SUFFIX="_a$A" bash "$HERE/run_transfer_1b_goalall.sh" "$@"
