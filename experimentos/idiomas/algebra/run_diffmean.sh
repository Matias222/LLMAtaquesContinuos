#!/usr/bin/env bash
# Experimento grande: direccion de idioma por DIFERENCIA DE MEDIAS en la capa 0 (D),
# sin optimizar y sin tomar nada de Shared (ni direccion ni norma), contra Shared.
#
#   D_L = mu_L - promedio_s(mu_s)      (make_diffmean.py, guardado con norma 1)
#     Dmulti  s = las fuentes con que se entreno Shared (fr: en,es,de)   <- PRIMARIO
#     Den     s = en
#   construido con las filas 0:528 del train; 528:588 (60) quedan de validacion.
#
# Criterio fijado ANTES de correr (pre-registro):
#   norma   la que maximiza "idioma target Y correcta" en las 60 filas de validacion
#           (empate -> la menor)
#   equivalente a Shared  si en el held-out (112) "target y correcta" no difiere de
#           Shared (McNemar exacto, p > 0.05) Y queda a <= 5 pp del nativo
#   el held-out se mira una sola vez, con la norma ya elegida
#
# Etapas (STAGES, en orden de prioridad; todo reanudable: una eval que ya tiene su
# eval_heldout.json no se repite salvo FORCE=1):
#   vec      D (Dmulti, Den) por idioma, norma 1 + azar de norma 1      solo CPU
#   sel      barrido de normas en validacion (NORMS) + Shared en validacion
#   final    elige la norma, escribe <V>_<L>_sel.pt y rand_<L>_sel.pt, token mas cercano
#   heldout  Tabla 1: q_en + D_L en el held-out, Dmulti / Den / azar
#   tests    bateria del paper con D en vez de Shared (TEST_VECS): resta q_L - D
#            (3x3 + azar), identificacion de idioma, resta contra instruccion,
#            conflicto (instr_en y las variantes post)
#   cross    Tabla 6: preguntas en los otros idiomas de entrenamiento + D_L, y en it/pt
#            (origenes nunca vistos, como el preset romance de Shared)
#   datos    eficiencia de datos: Dmulti_fr con N filas (DATA_N) x semillas (DATA_SEEDS)
#   geo      cosenos capa por capa de los desplazamientos (Shared, D, azar, nativo,
#            instruccion), validacion cruzada por mitades                  solo forwards
#   reporte  reporte_diffmean.py -> $O/resumen.md + figuras (se puede correr en
#            cualquier momento: lo que falta queda marcado)
#
#   uso:  bash algebra/run_diffmean.sh MODEL_PATH
#   la familia sale del path (Qwen -> qwen3_v10 / attributes/qwen3; si no -> v10)
#   variables: DEVICE (cuda:0)  STAGES  LANGS ("fr es de")  VECS ("Dmulti Den")
#              TEST_VECS ("Dmulti")  NORMS ("0.5 0.6 0.7 0.8 1.0")  VAL_N (60)
#              DATA_N ("8 32 128")  DATA_SEEDS ("0 1")  FORCE=1  SMOKE=1 (4 filas,
#              2 normas, todo en diffmean_<fam>_smoke)
set -euo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$HERE/.."

MODEL="${1:?uso: bash algebra/run_diffmean.sh MODEL_PATH}"
[[ -d "$MODEL" ]] || { echo "no existe el modelo: $MODEL"; exit 1; }
DEVICE="${DEVICE:-cuda:0}"
case "$(basename "$MODEL")" in
  *[Qq]wen*) FAM=qwen;  RUN=algebra/runs/qwen3_v10; TDIR=attributes/qwen3 ;;
  *)         FAM=llama; RUN=algebra/runs/v10;       TDIR=attributes/v10 ;;
esac
RUN="${RUN_OVERRIDE:-$RUN}"; TDIR="${TDIR_OVERRIDE:-$TDIR}"
STAGES="${STAGES:-vec sel final heldout tests cross datos geo reporte}"
LANGS="${LANGS:-fr es de}"
VECS="${VECS:-Dmulti Den}"
TEST_VECS="${TEST_VECS:-Dmulti}"
NORMS="${NORMS:-0.5 0.6 0.7 0.8 1.0}"
VAL_N="${VAL_N:-60}"
DATA_N="${DATA_N:-8 32 128}"
DATA_SEEDS="${DATA_SEEDS:-0 1}"
SPLIT=0.84
BUILD_ROWS=0:528
VAL_SPLIT=0.7543          # int(700 * 0.7543) = 528: la validacion son las filas 528..587
NTOK=250
CKPT=lang_patch_best_train.pt
O=algebra/runs/diffmean_$FAM
NHO=(); NENTRADA=0; NGEO=0
if [[ "${SMOKE:-0}" == "1" ]]; then
  O=${O}_smoke; NORMS="0.5 0.8"; VAL_N=4; NHO=(--n 4); NENTRADA=4; NGEO=6
  DATA_N="8"; DATA_SEEDS="0"
  echo "### SMOKE: 4 filas, normas $NORMS -> $O"
fi
has() { [[ " $STAGES " == *" $1 "* ]]; }
mkdir -p "$O/logs"
export GEN_CACHE="$PWD/$RUN/gen_cache"     # reusa todo lo sin parche de la corrida original
echo "modelo $MODEL  familia $FAM  RUN $RUN  TDIR $TDIR  -> $O"

shared() { echo "$RUN/alg_$1/$CKPT"; }
fuentes() { case $1 in fr) echo prompt,prompt_es,prompt_de ;; es) echo prompt,prompt_de,prompt_fr ;;
                       de) echo prompt,prompt_es,prompt_fr ;; esac; }
otros() { case $1 in fr) echo "es de" ;; es) echo "de fr" ;; de) echo "es fr" ;; esac; }
src() { [[ "$1" == "Den" ]] && echo prompt || fuentes "$2"; }
for L in fr es de; do [[ -f "$(shared $L)" ]] || { echo "falta $(shared $L)"; exit 1; }; done

# ev <dir> <args de eval_lang_patch...>: salta si ya esta (FORCE=1 rehace)
ev() {
  local d=$1; shift
  if [[ -f "$d/eval_heldout.json" && "${FORCE:-0}" != "1" ]]; then echo "  ya esta: $d"; return; fi
  mkdir -p "$d"
  python3 -u eval_lang_patch.py --model "$MODEL" --device "$DEVICE" --patch_anchor goal_all \
      --num_patch_positions 1 --num_tokens $NTOK --cell_metrics --control nativo "$@" \
      --out_json "$d/eval_heldout.json" --out_md "$d/eval_heldout.md" 2>&1 | tee "$d/eval_heldout.log"
}
norma() {   # norma <V> <L>: la elegida en final
  python3 -c "import json,sys; print(json.load(open('$O/sel/seleccion.json'))['$1']['$2']['norma'])"
}

# =============================================================================
if has vec; then
  echo; echo "################ vec"
  mkdir -p "$O/vec"
  for L in $LANGS; do
    for V in $VECS; do
      python3 -u make_diffmean.py --model "$MODEL" --targets "$TDIR/targets_v8_$L.csv" --lang $L \
          --src "$(src $V $L)" --rows $BUILD_ROWS --like "$(shared $L)" \
          --compare "shared=$(shared $L)" --out "$O/vec/${V}_$L.pt"
    done
  done
  python3 -u make_random_patch.py --like "$O/vec/$(echo $VECS | cut -d' ' -f1)_$(echo $LANGS | cut -d' ' -f1).pt" \
      --seed 0 --out "$O/vec/rand_unit.pt"
fi 2>&1 | tee -a "$O/logs/vec.log"

# =============================================================================
if has sel; then
  echo; echo "################ sel (validacion: filas 528..$((528 + VAL_N - 1)))"
  for L in $LANGS; do
    ev "$O/sel/shared_$L" --patch "$(shared $L)" --target_lang $L \
        --targets "$TDIR/targets_v8_$L.csv" --train_test_split $VAL_SPLIT --n $VAL_N
    for V in $VECS; do
      for N in $NORMS; do
        ev "$O/sel/${V}_${L}_n$N" --patch "$O/vec/${V}_$L.pt" --scale $N --target_lang $L \
            --targets "$TDIR/targets_v8_$L.csv" --train_test_split $VAL_SPLIT --n $VAL_N
      done
    done
  done
fi 2>&1 | tee -a "$O/logs/sel.log"

# =============================================================================
if has final; then
  echo; echo "################ final: eleccion de norma"
  python3 - "$O" "$LANGS" "$VECS" "$NORMS" <<'PY'
import json, os, sys
import torch
O, langs, vecs, norms = sys.argv[1], sys.argv[2].split(), sys.argv[3].split(), sys.argv[4].split()
out = {}
for V in vecs:
    out[V] = {}
    for L in langs:
        curva = []
        for N in norms:
            p = f"{O}/sel/{V}_{L}_n{N}/eval_heldout.json"
            if not os.path.exists(p):
                raise SystemExit(f"falta {p}: correr la etapa sel")
            rows = json.load(open(p, encoding="utf-8"))["splits"]["heldout"]
            n = len(rows)
            tc = sum(bool(r["patched_is_target"]) and bool(r["patched_answer_correct"]) for r in rows)
            t = sum(bool(r["patched_is_target"]) for r in rows)
            curva.append({"norma": float(N), "tag": N, "n": n, "target": t / n, "target_y_correcta": tc / n})
        best = max(curva, key=lambda c: (c["target_y_correcta"], -c["norma"]))
        alt = [c for c in curva if c["target"] >= 0.95]
        out[V][L] = {"norma": best["norma"], "curva": curva,
                     "norma_min_95": min(c["norma"] for c in alt) if alt else None}
        print(f"{V} {L}: norma {best['norma']}  (target y correcta {best['target_y_correcta']:.2f})  "
              f"min norma con >=95% target: {out[V][L]['norma_min_95']}")
json.dump(out, open(f"{O}/sel/seleccion.json", "w"), indent=2)
rand = torch.load(f"{O}/vec/rand_unit.pt", map_location="cpu")
for V in vecs:
    for L in langs:
        u = torch.load(f"{O}/vec/{V}_{L}.pt", map_location="cpu")
        torch.save(u * out[V][L]["norma"], f"{O}/vec/{V}_{L}_sel.pt")
for L in langs:   # el azar copia la norma del vector primario de cada idioma
    torch.save(rand * out[vecs[0]][L]["norma"], f"{O}/vec/rand_{L}_sel.pt")
print(f"guardado {O}/sel/seleccion.json y los *_sel.pt")
PY
  mkdir -p "$O/nearest"
  for L in $LANGS; do
    for V in $VECS; do
      # token mas cercano: ¿D a la norma elegida cambia algun token de la pregunta?
      python3 -u nearest_token_patch.py --model "$MODEL" --patch "$O/vec/${V}_${L}_sel.pt" \
          --targets "$TDIR/targets_v8_$L.csv" --train_test_split $SPLIT --cols prompt --alphas 1 \
          --out_dir "$O/nearest/${V}_$L" > "$O/nearest/${V}_$L.log" 2>&1
      grep -E "^v +1 " "$O/nearest/${V}_$L.log" | sed "s/^/  $V $L /" || true
    done
  done
fi 2>&1 | tee -a "$O/logs/final.log"

# =============================================================================
if has heldout; then
  echo; echo "################ heldout"
  for L in $LANGS; do
    for V in $VECS; do
      ev "$O/heldout/${V}_$L" --patch "$O/vec/${V}_${L}_sel.pt" --target_lang $L \
          --targets "$TDIR/targets_v8_$L.csv" --train_test_split $SPLIT ${NHO[@]+"${NHO[@]}"}
    done
    ev "$O/heldout/rand_$L" --patch "$O/vec/rand_${L}_sel.pt" --target_lang $L \
        --targets "$TDIR/targets_v8_$L.csv" --train_test_split $SPLIT ${NHO[@]+"${NHO[@]}"}
  done
fi 2>&1 | tee -a "$O/logs/heldout.log"

# =============================================================================
if has tests; then
  for V in $TEST_VECS; do
    T=$O/tests_$V; mkdir -p "$T"
    P=(); for L in fr es de; do P+=(--patch "$L=$O/vec/${V}_${L}_sel.pt"); done
    eod() {   # eod <tag> <conds>: mismas condiciones y etiquetas que la etapa E de Shared
      if [[ -f "$T/entrada_o_directiva_$1.json" && "${FORCE:-0}" != "1" ]]; then echo "  ya esta: $T/$1"; return; fi
      python3 -u entrada_o_directiva.py --model "$MODEL" --device "$DEVICE" \
          --targets "$TDIR/targets_v8_fr.csv" --train_test_split $SPLIT --n $NENTRADA \
          --num_tokens $NTOK --rand_like fr "${P[@]}" --conds "$2" --tag "$1" --out_dir "$T" \
          2>&1 | tee "$T/$1.log"
    }
    RESTA=""
    for L in fr es de; do
      RESTA+="plain:prompt_$L:-:0,"
      for W in fr es de rand0_$L; do RESTA+="plain:prompt_$L:$W:-1,"; done
    done
    echo; echo "################ tests $V: resta"
    eod resta "${RESTA%,}"
    echo; echo "################ tests $V: idioma_entrada"
    eod idioma_entrada "lang_id:prompt:-:0,lang_id:prompt:fr:1,lang_id:prompt:es:1,lang_id:prompt:de:1,lang_id:prompt:rand0:1,lang_id:prompt_fr:-:0,lang_id:prompt_es:-:0,lang_id:prompt_de:-:0"
    echo; echo "################ tests $V: resta_directiva"
    eod resta_directiva "instr_fr:prompt:-:0,instr_fr:prompt:fr:-1,instr_fr:prompt:es:-1,instr_fr:prompt:rand0:-1"
    echo; echo "################ tests $V: conflicto"
    eod conflicto "instr_en:prompt_fr:-:0,instr_en:prompt:-:0,instr_en:prompt:fr:1,instr_en:prompt:rand0:1,plain:prompt:-:0,plain:prompt:fr:1"
    C2=""; for TPL in instr_en_post instr_en_post_ref; do C2+="$TPL:prompt_fr:-:0,$TPL:prompt:-:0,$TPL:prompt:fr:1,"; done
    echo; echo "################ tests $V: conflicto_v2"
    eod conflicto_v2 "${C2%,}"
  done
fi 2>&1 | tee -a "$O/logs/tests.log"

# =============================================================================
if has cross; then
  echo; echo "################ cross (Tabla 6)"
  for L in $LANGS; do
    # otros idiomas de entrenamiento (Tabla 6) + it/pt, origenes nunca vistos (preset romance de Shared)
    CONDS=""; for S in $(otros $L) it pt; do CONDS+="prompt_$S:0,prompt_$S:1,"; done
    for V in $VECS; do
      D=$O/cross_$V/$L
      if [[ -f "$D/cross_lang_cross.json" && "${FORCE:-0}" != "1" ]]; then echo "  ya esta: $D"; continue; fi
      mkdir -p "$D"
      python3 -u cross_lang_patch.py --model "$MODEL" --device "$DEVICE" --patch "$O/vec/${V}_${L}_sel.pt" \
          --patch_anchor goal_all --num_patch_positions 1 --target_lang $L --num_tokens $NTOK \
          --targets "$TDIR/targets_v8_$L.csv" --train_test_split $SPLIT ${NHO[@]+"${NHO[@]}"} \
          --conds "${CONDS%,}" --tag cross --out_dir "$D" 2>&1 | tee "$D/cross.log"
    done
  done
fi 2>&1 | tee -a "$O/logs/cross.log"

# =============================================================================
if has datos; then
  echo; echo "################ datos (eficiencia: Dmulti_fr con N filas)"
  mkdir -p "$O/datos/vec"
  NF=$(norma Dmulti fr)
  for N in $DATA_N; do
    for S in $DATA_SEEDS; do
      P=$O/datos/vec/Dmulti_fr_N${N}_s$S.pt
      python3 -u make_diffmean.py --model "$MODEL" --targets "$TDIR/targets_v8_fr.csv" --lang fr \
          --src "$(fuentes fr)" --rows $BUILD_ROWS --n_rows $N --seed $S --like "$(shared fr)" \
          --compare "shared=$(shared fr)" --compare "Dmulti_528=$O/vec/Dmulti_fr.pt" --out "$P"
      ev "$O/datos/N${N}_s$S" --patch "$P" --scale $NF --target_lang fr \
          --targets "$TDIR/targets_v8_fr.csv" --train_test_split $SPLIT ${NHO[@]+"${NHO[@]}"}
    done
  done
fi 2>&1 | tee -a "$O/logs/datos.log"

# =============================================================================
if has geo; then
  echo; echo "################ geo"
  mkdir -p "$O/geo"
  for L in $LANGS; do
    if [[ -f "$O/geo/geo_$L.json" && "${FORCE:-0}" != "1" ]]; then echo "  ya esta: geo $L"; continue; fi
    GP=(--patch "shared=$(shared $L)")
    for V in $VECS; do GP+=(--patch "$V=$O/vec/${V}_${L}_sel.pt"); done
    GP+=(--patch "rand=$O/vec/rand_${L}_sel.pt")
    python3 -u geo_diffmean.py --model "$MODEL" --device "$DEVICE" --targets "$TDIR/targets_v8_$L.csv" \
        --lang $L --train_test_split $SPLIT --n $NGEO "${GP[@]}" --out "$O/geo/geo_$L.json"
  done
fi 2>&1 | tee -a "$O/logs/geo.log"

# =============================================================================
if has reporte; then
  echo; echo "################ reporte"
  python3 -u reporte_diffmean.py --out_dir "$O" --run "$RUN" --langs "$LANGS" --vecs "$VECS" \
      --test_vecs "$TEST_VECS" --data_n "$DATA_N" --data_seeds "$DATA_SEEDS" --fam $FAM
fi 2>&1 | tee "$O/logs/reporte.log"

echo; echo "Listo: $O/resumen.md"
