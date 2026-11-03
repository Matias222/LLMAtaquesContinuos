#!/usr/bin/env bash
# Control "centroide" para la Tabla 1 (solo suma, un idioma): en vez de un vector
# al azar con la norma de Shared, un vector que apunta al centroide de los tokens
# del idioma (make_centroid_patch.py):
#
#   cA = mu_L            centroide absoluto (se espera dominado por la anisotropia)
#   cB = mu_L - mu_en    diferencia de medias, las mismas preguntas de train en L y en ingles
#
# los dos reescalados a ||v_L|| y aplicados goal_all (todo el tramo de la pregunta),
# igual que Shared. Se evaluan sobre las 112 preguntas held-out en INGLES con
# eval_lang_patch.py, el mismo eval que la Tabla 1 (none / nativo / parche):
#
#   shared   v_L entrenado (referencia, la misma fila de la Tabla 1)
#   cA, cB   el control nuevo
#   rand0    Gaussiano con la norma de v_L (el control de siempre)
#   cB x2, x4 (SCALES): si cB no hace nada a x1, separa "apunta bien pero no
#            alcanza la norma" de "no apunta"
#
# Etapas (STAGES, en orden):
#   vec   construir cA, cB y rand0 + cosenos contra Shared        (CPU)
#   nn    token mas cercano de e_i + a*c para cA y cB              (CPU)
#   eval  generaciones sobre el held-out                           (GPU)
#   tabla resumen en $R/resumen.md
#
#   uso (desde cualquier lado):  bash algebra/run_centroide.sh MODEL_PATH
#   variables:  DEVICE (cuda:0)  L (fr)  STAGES ("vec nn eval tabla")
#               SCALES ("2 4")  SCALED ("cB": que vectores se escalan; "cA cB" para los dos;
#                     "shared cA cB" para la curva dosis-respuesta completa)
#               FORCE=1 rehace evals que ya tienen eval_heldout.json (por defecto se saltean)
#               RUN (algebra/runs/v10: de donde sale Shared y el gen_cache)
#               SMOKE=1 (evals de 4 filas, todo en algebra/runs/centroide_smoke)
#               NN_ALPHAS ("0.6,0.7,1,2,4") escalas del chequeo de token mas cercano
#   Qwen:       RUN=algebra/runs/qwen3_v10 TDIR=attributes/qwen3  -> algebra/runs/centroide_qwen3_v10/
set -euo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$HERE/.."

MODEL="${1:?uso: bash algebra/run_centroide.sh MODEL_PATH}"
DEVICE="${DEVICE:-cuda:0}"
L="${L:-fr}"
STAGES="${STAGES:-vec nn eval tabla}"
SCALES="${SCALES:-2 4}"
SCALED="${SCALED:-cB}"
RUN="${RUN:-algebra/runs/v10}"
TDIR="${TDIR:-attributes/v10}"
SPLIT=0.84
NTOK=250
SHARED="$RUN/alg_$L/lang_patch_best_train.pt"
T="$TDIR/targets_v8_$L.csv"
# una carpeta por modelo: Llama (RUN=algebra/runs/v10) queda en centroide/, el resto en
# centroide_<run>/ (p.ej. centroide_qwen3_v10/). Si compartieran carpeta, el skip de evals
# ya hechas reusaria los vectores y las generaciones del otro modelo.
CDIR=centroide
[[ "$(basename "$RUN")" != v10 ]] && CDIR="centroide_$(basename "$RUN")"
NN_ALPHAS="${NN_ALPHAS:-0.6,0.7,1,2,4}"
R="algebra/runs/$CDIR/$L"
NEVAL=()
if [[ "${SMOKE:-0}" == "1" ]]; then
  R="algebra/runs/${CDIR}_smoke/$L"; NEVAL=(--n 4); SCALES="${SCALES%% *}"
  echo "### SMOKE: evals de 4 filas, una sola escala -> $R"
fi
has() { [[ " $STAGES " == *" $1 "* ]]; }
mkdir -p "$R"
# baseline, nativo y shared ya estan en el cache de la corrida de la Tabla 1:
# no se regeneran (la clave incluye embeddings de entrada y num_tokens)
export GEN_CACHE="${GEN_CACHE:-$PWD/$RUN/gen_cache}"

[[ -d "$MODEL" ]] || { echo "no existe el modelo: $MODEL"; exit 1; }
for f in "$SHARED" "$T"; do [[ -f "$f" ]] || { echo "falta $f"; exit 1; }; done

# =============================================================================
if has vec; then
  echo; echo "################ vec"
  python3 -u make_centroid_patch.py --model "$MODEL" --lang "$L" --like "$SHARED" \
      --targets "$T" --train_test_split $SPLIT --out_dir "$R" 2>&1 | tee "$R/vec.log"
  python3 -u make_random_patch.py --like "$SHARED" --seed 0 --out "$R/rand0.pt" 2>&1 | tee -a "$R/vec.log"
fi
for P in cA cB rand0; do [[ -f "$R/$P.pt" ]] || { echo "falta $R/$P.pt (correr la etapa vec)"; exit 1; }; done

# =============================================================================
if has nn; then
  for P in cA cB; do
    echo; echo "################ nn $P"
    # mismas entradas que el chequeo de la seccion 4.1 (ingles y las otras dos de train)
    python3 -u nearest_token_patch.py --model "$MODEL" --patch "$R/$P.pt" --targets "$T" \
        --train_test_split $SPLIT --cols prompt --alphas "$NN_ALPHAS" \
        --out_dir "$R/nearest_$P" 2>&1 | tee "$R/nearest_$P.log"
  done
fi

# =============================================================================
ev() {   # ev <nombre> <parche> <escala>
  local O="$R/eval_$1"; mkdir -p "$O"
  if [[ "${FORCE:-0}" != "1" && -f "$O/eval_heldout.json" ]]; then
    echo "ya evaluado: $O (FORCE=1 para rehacer)"; return
  fi
  echo; echo "################ eval $1 ($2, escala $3)"
  python3 -u eval_lang_patch.py --model "$MODEL" --device "$DEVICE" --patch "$2" --scale "$3" \
      --patch_anchor goal_all --num_patch_positions 1 --target_lang "$L" --num_tokens $NTOK \
      --cell_metrics --control nativo ${NEVAL[@]+"${NEVAL[@]}"} \
      --targets "$T" --train_test_split $SPLIT \
      --out_json "$O/eval_heldout.json" --out_md "$O/eval_heldout.md" 2>&1 | tee "$O/eval_heldout.log"
}
if has eval; then
  ev shared "$SHARED" 1
  for P in cA cB rand0; do ev "$P" "$R/$P.pt" 1; done
  # SCALED puede incluir shared (el v_L entrenado) para comparar curvas dosis-respuesta
  for P in $SCALED; do
    if [[ "$P" == shared ]]; then SRC="$SHARED"; else SRC="$R/$P.pt"; fi
    for a in $SCALES; do ev "${P}_x$a" "$SRC" "$a"; done
  done
fi

# =============================================================================
if has tabla; then
  echo; echo "################ tabla"
  python3 - "$R" "$L" <<'PY' | tee "$R/resumen.md"
import glob, json, os, sys
R, L = sys.argv[1], sys.argv[2]
cen = json.load(open(f"{R}/centroide.json", encoding="utf-8")) if os.path.exists(f"{R}/centroide.json") else None
orden = lambda n: (["shared", "cA", "cB", "rand0"].index(n.split("_x")[0]) if n.split("_x")[0] in
                   ["shared", "cA", "cB", "rand0"] else 9, n)
filas = sorted((os.path.basename(os.path.dirname(p))[5:], p) for p in glob.glob(f"{R}/eval_*/eval_heldout.json"))
filas.sort(key=lambda x: orden(x[0]))
print(f"# Control centroide, held-out en ingles, idioma {L}\n")
if cen:
    print(f"||v_{L}|| = {cen['norma_shared']:.4f}  |  cos al azar ~ {cen['cos_azar_esperado']:.4f}\n")
    print("| vector | cos(shared) | cos(mu_vocab) |\n|---|---|---|")
    for k, o in cen["vectores"].items():
        print(f"| {k} | {o['cos_shared']:+.3f} | {o['cos_mu_vocab']:+.3f} |")
    print()
    for k, v in cen["diagnostico"].items():
        print(f"- {k}: {v:+.4f}")
    print()
print("| condicion | escala | n | % idioma target | accuracy | CE head (sin -> con) |")
print("|---|---|---|---|---|---|")
ref = None
for nombre, p in filas:
    d = json.load(open(p, encoding="utf-8")); m = d["metrics"]
    if ref is None:
        ref = m
        print(f"| none | - | {d['n_heldout']} | {100*m['baseline']['is_target']:.1f} | {100*m['baseline']['answer_correct']:.1f} | |")
        print(f"| nativo | - | {d['n_heldout']} | {100*m['reference']['is_target']:.1f} | {100*m['reference']['answer_correct']:.1f} | |")
    pm = m["patched"]
    print(f"| {nombre.split('_x')[0]} | {d['config']['scale']:g} | {d['n_heldout']} | {100*pm['is_target']:.1f} | "
          f"{100*pm['answer_correct']:.1f} | {m['nll_fr_head_baseline']:.2f} -> {m['nll_fr_head_patched']:.2f} |")
PY
fi
echo; echo "Resumen: $R/resumen.md"
