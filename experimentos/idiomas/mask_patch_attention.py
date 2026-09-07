"""
Experimentos 1 y 3 de mecanismo: que parte del KV del prompt NECESITAN leer los
tokens generados para que el frances se sostenga.

Genera con el parche puesto, pero bloqueando la atencion desde los tokens
generados hacia un subconjunto de posiciones del prompt. El forward del prompt
queda intacto en todos los modos salvo `post`: el ultimo token del prompt, el
que decide el primer token de la respuesta, siempre ve lo mismo que en el eval.

---------------------------------------------------------------------------
LOS MODOS
---------------------------------------------------------------------------
    --block gen    bloquea SOLO las 3 posiciones parcheadas para los generados.
                   Resultado (v4_250, 2026-09): el frances se sostiene (0.86 vs
                   0.90). Los generados NO necesitan leer el parche directamente.
    --block post   bloquea las 3 posiciones para TODO lo posterior, incluido el
                   resto del prompt. El parche queda invisible: frances = 0.00.
                   Confirma que la mascara actua y que el parche solo entra por
                   esas posiciones. OJO: tambien borra esas 3 palabras de la
                   pregunta para el resto del prompt, asi que la salida no tiene
                   por que igualar al baseline; la columna =base no significa
                   nada en este modo.
    --block keep   los generados ven SOLO las regiones listadas en --keep, mas
                   ellos mismos. Regiones (attn_utils.REGIONES_PROMPT):
                       bos      posicion 0 (attention sink; mantener SIEMPRE)
                       sys      header de sistema, texto de sistema, header de usuario
                       patched  las 3 posiciones parcheadas
                       qrest    el resto de la pregunta
                       ahead    <|eot_id|> + header del assistant
                   Contesta DONDE del KV del prompt vive el modo frances, que
                   es lo que `gen` dejo abierto: si no esta en las 3 posiciones,
                   esta imprimido en las posteriores, y la pregunta es en cuales.

    --clean_control   ademas de la corrida con parche, genera SIN parche bajo la
                      misma mascara. Sin esto no se sabe que hace la mascara sola
                      (p.ej. con keep=bos,sys,ahead el modelo no ve la pregunta y
                      responde cualquier cosa: hay que ver si esa cualquier cosa
                      es francesa con parche e inglesa sin).

    --layers   para gen/post: una corrida por especificacion ('all;1-8;9-16').
               Con keep se ignora (siempre todas las capas).

---------------------------------------------------------------------------
COMO LEERLO
---------------------------------------------------------------------------
Mirar juntas is_french, starts_fr (primer token frances), largo medio, cortas
(<25 chars) y los textos; sobre fragmentos de dos palabras el detector devuelve
'unknown'. En keep, la comparacion es parche vs limpio bajo la MISMA mascara: la
diferencia de is_french entre los dos es el efecto del parche que sobrevive a
esa restriccion.

    # 1. donde vive el modo (siempre con bos y sys)
    python3 -u mask_patch_attention.py --model $M --patch runs/v4_250/lang_patch_best_train.pt \\
        --block keep --clean_control --out_dir runs/mask_v4 \\
        --keep "bos,sys,patched,qrest,ahead;bos,sys,qrest,ahead;bos,sys,patched,qrest;bos,sys,ahead;bos,sys,qrest;bos,sys,patched;bos,sys"

    # 2. necesidad del parche por banda de capas
    python3 -u mask_patch_attention.py --model $M --patch runs/v4_250/lang_patch_best_train.pt \\
        --block gen --layers "all;1-8;9-16;17-24;25-28" --out_dir runs/mask_v4 --check_mask_path
"""

import argparse
import json
import os

import pandas as pd
import torch
import tqdm

from attn_utils import (REGIONES_PROMPT, add_metrics, aggregate, generate_masked,
                        parse_layers)
from lm import DEFAULT_MODEL, load_model_and_tokenizer


def tag(s):
    return s.strip().lower().replace(",", "_").replace("-", "to").replace(" ", "")


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--patch", default="runs/v4_250/lang_patch_best_train.pt")
    ap.add_argument("--model", default=DEFAULT_MODEL)
    ap.add_argument("--targets", default="attributes/french/targets_french.csv")
    ap.add_argument("--train_test_split", type=float, default=0.80)
    ap.add_argument("--num_patch_positions", type=int, default=3)
    ap.add_argument("--patch_offset", type=int, default=0)
    ap.add_argument("--block", default="gen", choices=["gen", "post", "keep"])
    ap.add_argument("--layers", default="all",
                    help="gen/post: especificaciones separadas por ';' ('all' | '16' | '12-16' | '1,5,9')")
    ap.add_argument("--keep", default="bos,sys,qrest,ahead",
                    help="keep: conjuntos de regiones separados por ';', cada uno con regiones "
                         "separadas por ',' de " + ",".join(REGIONES_PROMPT))
    ap.add_argument("--clean_control", action="store_true",
                    help="generar tambien SIN parche bajo la misma mascara")
    ap.add_argument("--num_tokens", type=int, default=100)
    ap.add_argument("--n", type=int, default=0, help="limitar filas de held-out (0 = todas)")
    ap.add_argument("--check_mask_path", action="store_true",
                    help="verificar que la causal 4D explicita reproduce attention_mask=None")
    ap.add_argument("--device", default="cuda:0")
    ap.add_argument("--out_dir", required=True)
    args = ap.parse_args()

    df = pd.read_csv(args.targets, sep=";", keep_default_na=False)
    heldout = df.iloc[int(len(df) * args.train_test_split):]
    if args.n > 0:
        heldout = heldout.head(args.n)

    model, tokenizer = load_model_and_tokenizer(args.model, device=args.device)
    n_layers = len(model.model.layers)
    patch = torch.load(args.patch, map_location=args.device).to(args.device)
    os.makedirs(args.out_dir, exist_ok=True)

    # --- condiciones ---------------------------------------------------------
    conds = []
    if args.block == "keep":
        for spec in [s.strip() for s in args.keep.split(";") if s.strip()]:
            regs = [r.strip() for r in spec.split(",") if r.strip()]
            malos = [r for r in regs if r not in REGIONES_PROMPT]
            if malos:
                raise SystemExit(f"regiones desconocidas: {malos}; validas: {REGIONES_PROMPT}")
            if "bos" not in regs:
                print(f"AVISO: keep='{spec}' sin bos: bloquear el attention sink rompe al modelo "
                      "por razones ajenas al parche")
            conds.append({"label": f"keep@{spec}", "layers": None, "keep": regs,
                          "file": f"mask_keep_{tag(spec)}.json"})
    else:
        for spec in [s.strip() for s in args.layers.split(";") if s.strip()]:
            layers = None if spec.lower() in ("all", "todas", "*") else parse_layers(spec, n_layers)
            conds.append({"label": f"{args.block}@{spec}", "layers": layers, "keep": None,
                          "file": f"mask_{args.block}_{tag(spec)}.json"})

    print(f"parche {args.patch}  norma {patch.norm(2).item():.4f}  |  held-out {len(heldout)}")
    print(f"block={args.block}  condiciones={[c['label'] for c in conds]}  |  "
          f"control limpio={'si' if args.clean_control else 'no'}")

    common = dict(num_patch_positions=args.num_patch_positions,
                  patch_offset=args.patch_offset, num_tokens=args.num_tokens)

    # --- referencia: parche sin mascara ------------------------------------
    base_rows = []
    for i, r in tqdm.tqdm(heldout.iterrows(), total=len(heldout), desc="unmasked"):
        txt, raw, info = generate_masked(model, tokenizer, r["prompt"], args.device,
                                         patch=patch, block="none", **common)
        rec = {"idx": int(i), "prompt": r["prompt"], "answer": r["answer"],
               "baseline": r["baseline_en"], "reference": r["output"],
               "unmasked": txt, "unmasked_role_leak": bool(txt != raw.strip()),
               "posiciones_parcheadas": info["patched"], "prompt_len": info["prompt_len"]}
        add_metrics(rec, "unmasked", txt, r["answer"], r["aliases"])
        if args.check_mask_path:
            txt2, _, _ = generate_masked(model, tokenizer, r["prompt"], args.device,
                                         patch=patch, block="none", explicit_causal=True,
                                         **common)
            rec["causal_explicit"] = txt2
            rec["causal_explicit_igual"] = txt2.strip() == txt.strip()
        base_rows.append(rec)

    resumen = [{"cond": "unmasked", **aggregate(base_rows, "unmasked")}]
    if args.check_mask_path:
        resumen[0]["causal_explicit_igual"] = (sum(r["causal_explicit_igual"] for r in base_rows)
                                               / len(base_rows))

    # --- cada condicion ------------------------------------------------------
    for c in conds:
        rows = []
        for rec0, (i, r) in tqdm.tqdm(zip(base_rows, heldout.iterrows()), total=len(heldout),
                                     desc=c["label"]):
            txt, raw, info = generate_masked(model, tokenizer, r["prompt"], args.device,
                                             patch=patch, block=args.block, layers=c["layers"],
                                             keep=c["keep"], **common)
            rec = dict(rec0)
            rec["masked"] = txt
            rec["masked_role_leak"] = bool(txt != raw.strip())
            rec["masked_igual_unmasked"] = txt.strip() == rec0["unmasked"].strip()
            rec["masked_igual_baseline"] = txt.strip() == str(r["baseline_en"]).strip()
            rec["query_from"] = info["query_from"]
            rec["n_keys_bloqueadas"] = info["n_blocked"]
            add_metrics(rec, "masked", txt, r["answer"], r["aliases"])
            if args.clean_control:
                ctxt, craw, _ = generate_masked(model, tokenizer, r["prompt"], args.device,
                                                patch=None, block=args.block, layers=c["layers"],
                                                keep=c["keep"], **common)
                rec["clean_masked"] = ctxt
                add_metrics(rec, "clean_masked", ctxt, r["answer"], r["aliases"])
            rows.append(rec)

        agg = aggregate(rows, "masked")
        agg["igual_unmasked"] = sum(r["masked_igual_unmasked"] for r in rows) / len(rows)
        agg["igual_baseline"] = sum(r["masked_igual_baseline"] for r in rows) / len(rows)
        agg["n_keys_bloqueadas_media"] = sum(r["n_keys_bloqueadas"] for r in rows) / len(rows)
        if args.clean_control:
            cl = aggregate(rows, "clean_masked")
            agg["clean"] = cl
            agg["efecto_parche_is_french"] = agg["is_french"] - cl["is_french"]
        rep = {"objetivo": "mascara de atencion desde los generados hacia el prompt",
               "patch": os.path.abspath(args.patch), "patch_norm": patch.norm(2).item(),
               "block": args.block, "layers": c["layers"] if c["layers"] is not None else "all",
               "keep": c["keep"], "config": vars(args), "n_heldout": len(rows),
               "metrics": agg, "rows": rows}
        with open(os.path.join(args.out_dir, c["file"]), "w", encoding="utf-8") as f:
            json.dump(rep, f, indent=2, ensure_ascii=False)
        resumen.append({"cond": c["label"], **agg})
        print(f"  -> {c['file']}")

    # --- tabla -------------------------------------------------------------
    print("\n" + "=" * 118)
    cab = (f"{'condicion':<34}{'is_fr':>7}{'st_fr':>7}{'acc':>7}{'largo':>7}{'<25':>5}"
           f"{'=unm':>6}{'keys':>6}")
    if args.clean_control:
        cab += f"{'| limpio is_fr':>15}{'acc':>7}{'largo':>7}{'| efecto':>9}"
    print(cab)
    for r in resumen:
        fila = (f"{r['cond']:<34}{r['is_french']:>7.2f}{r['starts_fr']:>7.2f}"
                f"{r['answer_correct']:>7.2f}{r['len_media']:>7.1f}{r['cortas_lt25']:>5d}"
                f"{r.get('igual_unmasked', 1.0):>6.2f}{r.get('n_keys_bloqueadas_media', 0):>6.1f}")
        if args.clean_control and "clean" in r:
            cl = r["clean"]
            fila += (f"{cl['is_french']:>15.2f}{cl['answer_correct']:>7.2f}{cl['len_media']:>7.1f}"
                     f"{r['efecto_parche_is_french']:>9.2f}")
        print(fila)
    print("=" * 118)
    if args.block == "keep":
        print("Lectura: 'efecto' = is_french con parche menos sin parche bajo la MISMA mascara.")
        print("La region mas chica con la que el efecto se mantiene es donde vive el modo frances.")
    elif args.block == "gen":
        print("Lectura: si is_french se mantiene con el parche bloqueado para los generados, el modo")
        print("no vive en las 3 posiciones sino en el KV del prompt posterior. Seguir con --block keep.")
    else:
        print("Lectura: post@all tiene que dar is_french ~0 (parche invisible). =unm/=base no informan.")

    path = os.path.join(args.out_dir, f"resumen_{args.block}.json")
    prev = []
    if os.path.exists(path):
        prev = json.load(open(path, encoding="utf-8")).get("resumen", [])
        prev = [p for p in prev if p["cond"] not in {r["cond"] for r in resumen}]
    with open(path, "w", encoding="utf-8") as f:
        json.dump({"block": args.block, "patch": os.path.abspath(args.patch),
                   "resumen": prev + resumen}, f, indent=2, ensure_ascii=False)
    print(f"\nGuardado en {args.out_dir}/  ({os.path.basename(path)})")


if __name__ == "__main__":
    main()
