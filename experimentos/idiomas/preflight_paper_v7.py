"""
Validacion inicial de run_paper_v7.sh. Si algo falla sale con codigo 1 y el .sh
no sigue. Dos subcomandos:

  env       antes de tocar la GPU en serio: dependencias, CUDA, config del modelo
            (28 capas, d=3072, vocab 128256, embeddings atados), los CSV (filas y
            columnas que usan las grillas) y la forma de los parches existentes.
            Escribe el CSV chico del humo de entrenamiento.
  outputs   despues del humo: que cada salida exista y tenga lo esperado
            (forma de los parches de humo, posiciones parcheadas por anchor en
            los tests, y que alg_fr reproduzca el frances en el held-out).

    python3 preflight_paper_v7.py env --model M --device cuda:0 \\
        --patch fr=algebra/runs/alg_fr/lang_patch_best_train.pt:1 ... --smoke_dir D
    python3 preflight_paper_v7.py outputs --smoke_dir D
"""

import argparse
import glob
import json
import os
import sys

D_MODEL = 3072
CONFIG = {"num_hidden_layers": 28, "hidden_size": D_MODEL, "vocab_size": 128256,
          "tie_word_embeddings": True}
CSVS = {
    # ruta: (filas, columnas que usa alguna etapa)
    "attributes/french/targets_french_v5.csv": (250, [
        "prompt", "prompt_es", "prompt_de", "prompt_fr", "prompt_it", "prompt_pt",
        "answer", "aliases", "output", "baseline_en", "passed_gate",
        "prompt_es_ok", "prompt_de_ok", "prompt_fr_ok", "prompt_it_ok", "prompt_pt_ok"]),
    "attributes/french/targets_open.csv": (99, ["prompt", "output", "answer", "aliases"]),
    "attributes/french/targets_open_2.csv": (50, [
        "prompt", "prompt_es", "prompt_de", "output", "answer", "aliases"]),
}
SMOKE_ROWS = 30

errores = []


def ok(msg):
    print(f"  OK    {msg}")


def mal(msg):
    print(f"  FALLA {msg}")
    errores.append(msg)


def fin():
    print()
    if errores:
        print(f"VALIDACION FALLIDA ({len(errores)}):")
        for e in errores:
            print(f"  - {e}")
        sys.exit(1)
    print("VALIDACION OK")


def cmd_env(args):
    print("== dependencias")
    try:
        import pandas as pd
        import torch
        import tqdm  # noqa: F401
        import transformers
        ok(f"torch {torch.__version__}, transformers {transformers.__version__}, pandas {pd.__version__}")
    except ImportError as e:
        mal(f"falta una dependencia: {e}")
        return fin()

    print("== GPU")
    if not torch.cuda.is_available():
        mal("CUDA no disponible")
    else:
        idx = int(args.device.split(":")[1]) if ":" in args.device else 0
        if idx >= torch.cuda.device_count():
            mal(f"{args.device} no existe ({torch.cuda.device_count()} GPUs)")
        else:
            libre, total = torch.cuda.mem_get_info(idx)
            msg = f"{torch.cuda.get_device_name(idx)}  libre {libre / 2**30:.1f} / {total / 2**30:.1f} GiB"
            (ok if libre > 10 * 2**30 else mal)(msg + ("" if libre > 10 * 2**30 else "  (< 10 GiB libres)"))

    print("== modelo")
    cfg_path = os.path.join(args.model, "config.json")
    if not os.path.isfile(cfg_path):
        mal(f"no existe {cfg_path}")
    else:
        cfg = json.load(open(cfg_path))
        for k, v in CONFIG.items():
            (ok if cfg.get(k) == v else mal)(f"{k} = {cfg.get(k)} (esperado {v})")

    print("== CSV")
    for path, (filas, cols) in CSVS.items():
        if not os.path.isfile(path):
            mal(f"no existe {path}")
            continue
        df = pd.read_csv(path, sep=";", keep_default_na=False)
        (ok if len(df) == filas else mal)(f"{path}: {len(df)} filas (esperado {filas})")
        faltan = [c for c in cols if c not in df.columns]
        (ok if not faltan else mal)(f"{path}: columnas" + (f" faltan {faltan}" if faltan else " completas"))
        # los sets abiertos no tienen respuesta verificable: answer y aliases van vacios
        vacias = [c for c in cols if c in df.columns and c not in ("answer", "aliases", "passed_gate")
                  and not c.endswith("_ok") and (df[c].astype(str).str.strip() == "").all()]
        if vacias:
            mal(f"{path}: columnas vacias {vacias}")

    print("== parches existentes")
    for spec in args.patch:
        name, _, rest = spec.partition("=")
        path, _, npos = rest.rpartition(":")
        if not os.path.isfile(path):
            mal(f"{name}: no existe {path}")
            continue
        v = torch.load(path, map_location="cpu")
        forma = (1, int(npos), D_MODEL)
        n = float(v.float().norm())
        bien = tuple(v.shape) == forma and torch.isfinite(v).all() and 0.1 < n < 5
        (ok if bien else mal)(f"{name}: forma {tuple(v.shape)} (esperado {forma}), norma {n:.4f}")

    print("== CSV del humo de entrenamiento")
    os.makedirs(args.smoke_dir, exist_ok=True)
    src = "attributes/french/targets_french_v5.csv"
    if os.path.isfile(src):
        df = pd.read_csv(src, sep=";", keep_default_na=False).head(SMOKE_ROWS)
        dst = os.path.join(args.smoke_dir, "targets_smoke.csv")
        df.to_csv(dst, sep=";", index=False)
        ok(f"{dst}: {len(df)} filas")
    fin()


def cmd_outputs(args):
    import torch

    d = args.smoke_dir
    print("== parches del humo de entrenamiento")
    for run in ("q3", "h3"):
        p = os.path.join(d, run, "lang_patch_best_train.pt")
        if not os.path.isfile(p):
            mal(f"{run}: el entrenamiento de humo no escribio {p}")
            continue
        v = torch.load(p, map_location="cpu")
        bien = tuple(v.shape) == (1, 3, D_MODEL) and torch.isfinite(v).all() and float(v.norm()) > 0
        (ok if bien else mal)(f"{run}: forma {tuple(v.shape)}, norma {float(v.norm()):.4f}")

    print("== evals de humo")
    for run in ("q3", "h3"):
        for f in ("eval_best_train.json", "cross_lang_idioma.json"):
            p = os.path.join(d, run, f)
            try:
                json.load(open(p))
                ok(f"{run}/{f}")
            except Exception as e:  # noqa: BLE001
                mal(f"{run}/{f}: {e}")

    print("== tests de humo: posiciones parcheadas por anchor")
    reps = sorted(glob.glob(os.path.join(d, "tests", "entrada_o_directiva_*.json")))
    if len(reps) != 4:
        mal(f"se esperaban 4 reportes de tests de humo, hay {len(reps)}")
    for p in reps:
        rep = json.load(open(p))
        anchors = rep.get("anchors", {})
        malas = []
        for c in rep["condiciones"]:
            if c["parche"] == "-":
                continue
            a = anchors.get(c["parche"])
            for r in c["rows"]:
                n = r["n_patched"]
                # goal / header: 3 posiciones; goal_all: todo el tramo (mas de 3 en estas preguntas)
                if (a in ("goal", "header") and n != 3) or (a == "goal_all" and n <= 3):
                    malas.append(f"{c['label']} idx {r['idx']}: n_patched {n} con anchor {a}")
            if not c["rows"]:
                malas.append(f"{c['label']}: sin filas")
        (ok if not malas else mal)(f"{os.path.basename(p)}: {len(rep['condiciones'])} condiciones"
                                   + ("" if not malas else "; " + "; ".join(malas[:3])))

    print("== reproduccion: alg_fr sobre el held-out en ingles")
    p = os.path.join(d, "repro", "eval_best_train.json")
    try:
        rows = json.load(open(p))["splits"]["heldout"]
        fr = sum(bool(r["patched_is_french"]) for r in rows)
        (ok if rows and fr >= len(rows) - 1 else mal)(
            f"{fr}/{len(rows)} respuestas en frances (esperado >= {len(rows) - 1}; el original da 100%)")
    except Exception as e:  # noqa: BLE001
        mal(f"repro: {e}")
    fin()


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    e = sub.add_parser("env")
    e.add_argument("--model", required=True)
    e.add_argument("--device", default="cuda:0")
    e.add_argument("--patch", action="append", default=[], metavar="NOMBRE=RUTA:NPOS")
    e.add_argument("--smoke_dir", required=True)
    o = sub.add_parser("outputs")
    o.add_argument("--smoke_dir", required=True)
    args = ap.parse_args()
    {"env": cmd_env, "outputs": cmd_outputs}[args.cmd](args)


if __name__ == "__main__":
    main()
