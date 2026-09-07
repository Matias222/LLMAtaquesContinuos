"""
Experimentos 1 y 3 de mecanismo: NECESIDAD de la lectura por atencion del parche.

Genera con el parche puesto, pero bloqueando la atencion HACIA las posiciones
parcheadas desde los tokens generados. El forward del prompt queda intacto, asi
que el ultimo token del prompt -- el que decide el primer token de la respuesta
-- sigue viendo el parche. Lo unico que cambia es si los tokens 2, 3, ... pueden
seguir leyendolo.

    hipotesis (contexto persistente)   el frances arranca y colapsa en
                                        fragmentos, como los parches de
                                        activaciones: primer token frances,
                                        despues ingles o nombre pelado
    alternativa (estado inyectado)      el frances se sostiene igual: el estado
                                        del ultimo token del prompt alcanza y
                                        los generados no necesitan el parche

---------------------------------------------------------------------------
LAS CONDICIONES
---------------------------------------------------------------------------
    unmasked          parche, sin mascara. Tiene que reproducir eval_lang_patch
                      sobre el mismo parche; si no, algo esta roto ANTES de
                      interpretar nada.
    gen @ all         bloqueo desde los generados, en todas las capas. Es EL test.
    gen @ <banda>     bloqueo solo en una banda de capas (experimento 3): dice en
                      que profundidad los generados leen el parche. Barrer
                      '1-8;9-16;17-24;25-28' y afinar donde caiga.
    post @ all        bloqueo desde TODO lo posterior al bloque parcheado,
                      incluido el resto del prompt. El parche queda invisible
                      para todos y la salida tiene que ser identica al baseline
                      ingles. Es el control de que la mascara funciona.

`--check_mask_path` genera ademas 'unmasked' con la causal 4D explicita en vez
de attention_mask=None: verifica que pasar una mascara aditiva no cambia la
salida por si misma (sdpa con is_causal vs mascara pueden diferir en fp16).

---------------------------------------------------------------------------
COMO LEERLO
---------------------------------------------------------------------------
No mirar solo is_french: sobre fragmentos de dos palabras el detector devuelve
'unknown'. Mirar juntas: is_french, starts_fr (primer token frances), largo
medio, cortas (<25 chars) y los textos. El patron 'starts_fr alto + is_french
bajo + cortas alto' es el colapso.

    python3 -u mask_patch_attention.py --model $M \\
        --patch runs/v4_250/lang_patch_best_train.pt \\
        --block gen --layers "all;1-8;9-16;17-24;25-28" \\
        --out_dir runs/mask_v4 --check_mask_path
    python3 -u mask_patch_attention.py --model $M \\
        --patch runs/v4_250/lang_patch_best_train.pt \\
        --block post --layers all --out_dir runs/mask_v4
"""

import argparse
import json
import os

import pandas as pd
import torch
import tqdm

from attn_utils import add_metrics, aggregate, generate_masked, parse_layers
from lm import DEFAULT_MODEL, load_model_and_tokenizer


def spec_tag(spec):
    return spec.strip().lower().replace(",", "_").replace("-", "to")


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--patch", default="runs/v4_250/lang_patch_best_train.pt")
    ap.add_argument("--model", default=DEFAULT_MODEL)
    ap.add_argument("--targets", default="attributes/french/targets_french.csv")
    ap.add_argument("--train_test_split", type=float, default=0.80)
    ap.add_argument("--num_patch_positions", type=int, default=3)
    ap.add_argument("--patch_offset", type=int, default=0)
    ap.add_argument("--block", default="gen", choices=["gen", "post"],
                    help="gen = bloquear desde los tokens generados (el test); "
                         "post = desde todo lo posterior al parche (control, = baseline)")
    ap.add_argument("--layers", default="all",
                    help="especificaciones separadas por ';'. Cada una: 'all' | '16' | '12-16' | '1,5,9'. "
                         "Una corrida por especificacion, compartiendo la referencia sin mascara")
    ap.add_argument("--num_tokens", type=int, default=100)
    ap.add_argument("--n", type=int, default=0, help="limitar filas de held-out (0 = todas)")
    ap.add_argument("--check_mask_path", action="store_true")
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
    specs = [s.strip() for s in args.layers.split(";") if s.strip()]
    for s in specs:
        parse_layers(s, n_layers)   # valida antes de gastar GPU
    os.makedirs(args.out_dir, exist_ok=True)

    print(f"parche {args.patch}  norma {patch.norm(2).item():.4f}  |  held-out {len(heldout)}")
    print(f"block={args.block}  capas={specs}  |  {n_layers} capas en el modelo")

    common = dict(num_patch_positions=args.num_patch_positions,
                  patch_offset=args.patch_offset, num_tokens=args.num_tokens)

    # --- referencia: parche sin mascara ------------------------------------
    base_rows = []
    for i, r in tqdm.tqdm(heldout.iterrows(), total=len(heldout), desc="unmasked"):
        txt, raw, info = generate_masked(model, tokenizer, r["prompt"], args.device,
                                         patch=patch, block="none", layers=None, **common)
        rec = {"idx": int(i), "prompt": r["prompt"], "answer": r["answer"],
               "baseline": r["baseline_en"], "reference": r["output"],
               "unmasked": txt, "unmasked_role_leak": bool(txt != raw.strip()),
               "posiciones_parcheadas": info["blocked"], "prompt_len": info["prompt_len"]}
        add_metrics(rec, "unmasked", txt, r["answer"], r["aliases"])
        if args.check_mask_path:
            txt2, _, _ = generate_masked(model, tokenizer, r["prompt"], args.device,
                                         patch=patch, block="none", layers=None,
                                         explicit_causal=True, **common)
            rec["causal_explicit"] = txt2
            rec["causal_explicit_igual"] = txt2.strip() == txt.strip()
        base_rows.append(rec)

    resumen = [{"cond": "unmasked", **aggregate(base_rows, "unmasked")}]
    if args.check_mask_path:
        resumen[0]["causal_explicit_igual"] = sum(r["causal_explicit_igual"] for r in base_rows) / len(base_rows)

    # --- cada especificacion de capas ---------------------------------------
    for spec in specs:
        layers = None if spec.lower() in ("all", "todas", "*") else parse_layers(spec, n_layers)
        rows = []
        for rec0, (i, r) in tqdm.tqdm(zip(base_rows, heldout.iterrows()), total=len(heldout),
                                     desc=f"{args.block}@{spec}"):
            txt, raw, info = generate_masked(model, tokenizer, r["prompt"], args.device,
                                             patch=patch, block=args.block, layers=layers,
                                             **common)
            rec = dict(rec0)
            rec["masked"] = txt
            rec["masked_role_leak"] = bool(txt != raw.strip())
            rec["masked_igual_unmasked"] = txt.strip() == rec0["unmasked"].strip()
            rec["masked_igual_baseline"] = txt.strip() == str(r["baseline_en"]).strip()
            rec["query_from"] = info["query_from"]
            add_metrics(rec, "masked", txt, r["answer"], r["aliases"])
            rows.append(rec)

        agg = aggregate(rows, "masked")
        agg["igual_unmasked"] = sum(r["masked_igual_unmasked"] for r in rows) / len(rows)
        agg["igual_baseline"] = sum(r["masked_igual_baseline"] for r in rows) / len(rows)
        rep = {"objetivo": "mascara de atencion hacia el parche",
               "patch": os.path.abspath(args.patch), "patch_norm": patch.norm(2).item(),
               "block": args.block, "layers_spec": spec,
               "layers": layers if layers is not None else "all",
               "config": vars(args), "n_heldout": len(rows), "metrics": agg, "rows": rows}
        nom = f"mask_{args.block}_{spec_tag(spec)}.json"
        with open(os.path.join(args.out_dir, nom), "w", encoding="utf-8") as f:
            json.dump(rep, f, indent=2, ensure_ascii=False)
        resumen.append({"cond": f"{args.block}@{spec}", **agg})
        print(f"  -> {nom}")

    # --- tabla -------------------------------------------------------------
    print("\n" + "=" * 100)
    print(f"{'condicion':<16}{'is_french':>10}{'starts_fr':>10}{'accuracy':>10}{'largo':>8}"
          f"{'<25ch':>7}{'=unmask':>9}{'=base':>7}   veredictos")
    for r in resumen:
        print(f"{r['cond']:<16}{r['is_french']:>10.2f}{r['starts_fr']:>10.2f}"
              f"{r['answer_correct']:>10.2f}{r['len_media']:>8.1f}{r['cortas_lt25']:>7d}"
              f"{r.get('igual_unmasked', 1.0):>9.2f}{r.get('igual_baseline', 0.0):>7.2f}   {r['veredictos']}")
    print("=" * 100)
    print("Lectura: 'gen@all' con starts_fr alto pero is_french bajo y muchas cortas = el frances")
    print("arranca y colapsa -> los generados NECESITAN leer el parche (contexto persistente).")
    print("'post@all' tiene que dar =base ~1.0; si no, la mascara no esta haciendo lo que dice.")

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
