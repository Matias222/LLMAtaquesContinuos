"""
Controles de un run (run_train_qwen3.sh) despues de train y de la etapa A. Solo CPU:
lee checkpoints, metadata, JSONs y el tokenizer; no carga el modelo.

  train  por celda: el checkpoint es [1, 1, d] con d = hidden_size, finito y no nulo;
         la metadata es la receta pedida (goal_all, 1 posicion, L2, paso, batch, el
         CSV de targets del run, columnas de entrada sin el idioma target); las tres
         celdas entrenan con la misma cantidad de filas; ||v||/||e|| medio del
         vocabulario (Llama v9: 0.78-0.87); curva sin NaN
  A      por celda: eval_heldout.json usa ese checkpoint con escala 1 (|v| del eval ==
         |v| del checkpoint), goal_all y la celda correcta; en CADA fila evaluada el
         parche cayo en exactamente los tokens de la pregunta (n_patched == largo del
         goal, recalculado con el tokenizer); idem cross_lang_idioma.json y
         cross_lang_romance.json; baseline en ingles; control nativo en el idioma
         de la celda

    python3 controles_run.py train --model $MODEL --runs algebra/runs/qwen3_v1 --targets_dir attributes/qwen3
    python3 controles_run.py A     --model $MODEL --runs algebra/runs/qwen3_v1 --targets_dir attributes/qwen3
"""

import argparse
import json
import math
import os
import sys

import torch

CELDAS = ("fr", "es", "de")
COLS = {"fr": "prompt,prompt_es,prompt_de", "es": "prompt,prompt_de,prompt_fr", "de": "prompt,prompt_es,prompt_fr"}
RECETA = {"patch_anchor": "goal_all", "num_patch_positions": 1, "l2_weight": 0.0925, "step_size": 0.00025,
          "step_decay": "cosine", "batch_size": 28, "loss_head_k": 8}
CKPT = "lang_patch_best_train.pt"
fallas, avisos = [], []


def control(ok, msg, aviso=False):
    nivel = "OK" if ok else ("AVISO" if aviso else "FALLA")
    print(f"  [{nivel:5}] {msg}")
    if not ok:
        (avisos if aviso else fallas).append(msg)
    return ok


def ctrl_train(args):
    from transformers import AutoConfig, AutoTokenizer
    from transfer_patch import load_embeddings
    d = AutoConfig.from_pretrained(args.model).hidden_size
    tok = AutoTokenizer.from_pretrained(args.model, use_fast=False)
    W = load_embeddings(args.model, "cpu")[:len(tok)]
    e_media = W.norm(dim=1).mean().item()
    print(f"d={d}  ||e|| medio del vocabulario {e_media:.4f}")
    tamanios = {}
    for c in CELDAS:
        print(f"\n[{c}]")
        o = os.path.join(args.runs, f"alg_{c}")
        p = os.path.join(o, CKPT)
        if not control(os.path.exists(p), f"existe {p}"):
            continue
        v = torch.load(p, map_location="cpu").float()
        control(tuple(v.shape) == (1, 1, d), f"forma {tuple(v.shape)} == (1, 1, {d})")
        control(bool(torch.isfinite(v).all()), "finito")
        n = v.norm().item()
        control(n > 0, f"||v|| = {n:.4f}  (||v||/||e|| = {n / e_media:.3f}; Llama v9: 0.78-0.87)")
        meta = torch.load(os.path.join(o, "lang_metadata.pt"), map_location="cpu", weights_only=False)
        for k, esperado in RECETA.items():
            control(meta.get(k) == esperado, f"metadata {k} = {meta.get(k)!r} (receta {esperado!r})")
        # por el final de la ruta: en la VM el EFS se ve con dos prefijos (symlink)
        sufijo = os.path.join(os.path.basename(os.path.normpath(args.targets_dir)), f"targets_v8_{c}.csv")
        control(meta["targets_csv"].endswith(os.sep + sufijo), f"targets_csv = {meta['targets_csv']} (termina en {sufijo})")
        control(",".join(meta["prompt_cols"]) == COLS[c], f"prompt_cols = {meta['prompt_cols']} (sin prompt_{c})")
        control(abs(meta["train_test_split"] - args.split) < 1e-9, f"split {meta['train_test_split']}")
        tamanios[c] = meta["train_size"]
        curva = meta.get("curva", [])
        control(all(math.isfinite(x["train_head"]) and math.isfinite(x["heldout_head"]) for x in curva),
                f"curva sin NaN ({len(curva)} epochs)")
        if len(curva) > 1:
            control(curva[-1]["heldout_head"] < curva[0]["heldout_head"],
                    f"CE head held-out baja: {curva[0]['heldout_head']:.3f} -> {curva[-1]['heldout_head']:.3f}",
                    aviso=True)
        print(f"  goal_len_media_train {meta.get('goal_len_media_train')}  best_train_epoch {meta.get('best_train_epoch')}")
    print()
    control(len(set(tamanios.values())) == 1, f"mismas filas de train en las tres celdas: {tamanios}")


def ctrl_A(args):
    from transformers import AutoTokenizer
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from lm import n_patched_tokens
    tok = AutoTokenizer.from_pretrained(args.model, use_fast=False)
    largo = {}

    def n_goal(q):
        if q not in largo:
            largo[q] = n_patched_tokens(tok, q, 1, 0, "goal_all")
        return largo[q]

    for c in CELDAS:
        print(f"\n[{c}]")
        o = os.path.join(args.runs, f"alg_{c}")
        ckpt_norm = torch.load(os.path.join(o, CKPT), map_location="cpu").float().norm().item()
        p = os.path.join(o, "eval_heldout.json")
        if not control(os.path.exists(p), f"existe {p}"):
            continue
        ev = json.load(open(p, encoding="utf-8"))
        cfg = ev.get("config", {})
        control(abs(ev["patch_norm"] - ckpt_norm) < 1e-3,
                f"|v| del eval {ev['patch_norm']:.4f} == |v| del checkpoint {ckpt_norm:.4f} (escala 1)")
        control(os.path.basename(ev["patch_path"]) == CKPT and f"alg_{c}" in ev["patch_path"],
                f"parche {ev['patch_path']}")
        control(cfg.get("patch_anchor") == "goal_all", f"anchor {cfg.get('patch_anchor')}")
        control(cfg.get("target_lang") == c, f"target_lang {cfg.get('target_lang')}")
        control(os.path.realpath(ev["model_path"]) == os.path.realpath(args.model), f"modelo {ev['model_path']}")
        rows = ev["splits"]["heldout"]
        malos = [(r["prompt"], r["n_patched"], n_goal(r["prompt"])) for r in rows
                 if int(r["n_patched"]) != n_goal(r["prompt"]) or n_goal(r["prompt"]) == 0]
        control(not malos, f"held-out: el parche cae en todos y solo los tokens de la pregunta "
                           f"({len(rows) - len(malos)}/{len(rows)}) {malos[:2]}")
        base_en = sum(r["baseline_lang"] == "en" for r in rows)
        control(base_en >= 0.9 * len(rows), f"baseline en ingles {base_en}/{len(rows)}", aviso=True)
        nat = sum(r["reference_lang"] == c for r in rows)
        control(nat >= 0.8 * len(rows), f"control nativo en {c}: {nat}/{len(rows)}", aviso=True)
        pat = sum(r["patched_lang"] == c for r in rows)
        print(f"  parche en {c}: {pat}/{len(rows)}")
        for tag in ("idioma", "romance"):
            p = os.path.join(o, f"cross_lang_{tag}.json")
            if not os.path.exists(p):
                control(False, f"falta {p}", aviso=True)
                continue
            cl = json.load(open(p, encoding="utf-8"))
            recs = [r for cond in cl.get("condiciones", []) for r in cond.get("rows", []) if "n_patched" in r]
            if not recs:
                control(False, f"{p}: no encontre filas con n_patched (claves: {list(cl)[:8]})")
                continue
            m = [(r["prompt_usado"], r["n_patched"]) for r in recs
                 if (int(r["n_patched"]) != (n_goal(r["prompt_usado"]) if r["escala"] != 0 else 0))]
            control(not m, f"cross_lang_{tag}: n_patched == largo del goal en {len(recs) - len(m)}/{len(recs)} "
                           f"(escala 0 -> 0) {m[:2]}")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("etapa", choices=["train", "A"])
    ap.add_argument("--model", required=True)
    ap.add_argument("--runs", required=True)
    ap.add_argument("--targets_dir", required=True)
    ap.add_argument("--split", type=float, default=0.84)
    args = ap.parse_args()
    {"train": ctrl_train, "A": ctrl_A}[args.etapa](args)
    print("\n" + "=" * 70)
    print(f"controles {args.etapa}: {len(fallas)} FALLA, {len(avisos)} AVISO")
    for f in fallas:
        print("  FALLA", f)
    sys.exit(1 if fallas else 0)


if __name__ == "__main__":
    main()
