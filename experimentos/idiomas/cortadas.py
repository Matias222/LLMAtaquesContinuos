"""
Held-out v8/v9: re-generar con mas tokens las salidas que se cortaron en el limite.

Las evals de v8 y v9 generan con 150 tokens y una parte de las respuestas
explicativas se corta antes de llegar al mecanismo ("Le processeur genere un
signal de retroaction" y fin). answer_correct las cuenta como falladas aunque no
se sepa si el modelo sabia la respuesta.

seleccionar
    Lee algebra/runs/{v8,v9}/alg_<L>/eval_heldout.json y marca como cortada toda
    salida (baseline, referencia o parche) cuyo largo re-tokenizado llega al limite
    (>= --umbral * num_tokens de esa eval). Por idioma junta la UNION de v8 y v9 y
    de las tres condiciones, asi las dos versiones se re-evaluan sobre las mismas
    filas, y escribe las filas del held-out de targets_v8_<L>.csv que entran
    (mismas columnas, mismos alias) en <out>/targets_cortadas_<L>.csv.

comparar
    Junta la eval original con la re-generada, fila por fila (por prompt):
      - veredicto viejo (recalculado con los alias actuales) vs nuevo, solo en las
        salidas que estaban cortadas en esa condicion
      - accuracy de todo el held-out reemplazando esas filas
      - cuantas siguen cortadas con el limite nuevo
      - control de determinismo: con greedy la salida nueva tiene que empezar con
        la vieja; se cuentan las que no
    -> <out>/reporte.md y <out>/reporte.json
"""

import argparse
import json
import os

import pandas as pd

from checkers import answer_correct

LANGS = ("es", "fr", "de")
VERS = ("v8", "v9")
CONDS = ("baseline", "reference", "patched")
NOMBRE = {"baseline": "baseline", "reference": "referencia", "patched": "parche"}


def cargar(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def heldout_df(targets, split):
    df = pd.read_csv(targets, sep=";", keep_default_na=False, dtype=str)
    return df.iloc[int(len(df) * split):].reset_index(drop=True)


def n_tokens(tok, text):
    return len(tok(text, add_special_tokens=False)["input_ids"])


def cortada(tok, text, limite, umbral):
    return n_tokens(tok, text) >= umbral * limite


def cmd_seleccionar(args):
    from transformers import AutoTokenizer
    tok = AutoTokenizer.from_pretrained(args.model)
    os.makedirs(args.out, exist_ok=True)
    resumen = {}
    for L in LANGS:
        sel = set()
        for V in VERS:
            d = cargar(os.path.join(args.runs, V, f"alg_{L}", "eval_heldout.json"))
            lim = d["config"]["num_tokens"]
            for r in d["splits"]["heldout"]:
                if not r["has_answer"]:
                    continue
                for c in CONDS:
                    if cortada(tok, r[c], lim, args.umbral):
                        sel.add(r["prompt"])
        ho = heldout_df(os.path.join(args.targets_dir, f"targets_v8_{L}.csv"), args.split)
        if ho["prompt"].duplicated().any():
            raise SystemExit(f"[{L}] prompts repetidos en el held-out: no se puede cruzar por prompt")
        sub = ho[ho["prompt"].isin(sel)]
        faltan = sel - set(sub["prompt"])
        if faltan:
            raise SystemExit(f"[{L}] {len(faltan)} prompts de las evals no estan en el held-out: {sorted(faltan)[:3]}")
        path = os.path.join(args.out, f"targets_cortadas_{L}.csv")
        sub.to_csv(path, sep=";", index=False)
        resumen[L] = len(sub)
        print(f"[{L}] {len(sub)} de {len(ho)} preguntas del held-out con alguna salida cortada -> {path}")
    with open(os.path.join(args.out, "seleccion.json"), "w", encoding="utf-8") as f:
        json.dump({"umbral": args.umbral, "n": resumen}, f, indent=2)


def cmd_comparar(args):
    from transformers import AutoTokenizer
    tok = AutoTokenizer.from_pretrained(args.model)
    rep, lineas = {}, ["# Held-out v8/v9: salidas cortadas re-generadas", ""]
    lineas += [f"Salidas que llegaban al limite (>= {args.umbral:.0%} de los tokens) re-generadas con "
               f"`--num_tokens {args.num_tokens}`. Veredictos viejos recalculados con los alias actuales.", ""]
    tabla = ["| version | idioma | condicion | cortadas | correctas antes | correctas ahora | "
             "siguen cortadas | held-out antes | held-out ahora | no-prefijo |",
             "|---|---|---|---|---|---|---|---|---|---|"]
    detalle = []
    for V in VERS:
        for L in LANGS:
            vieja = cargar(os.path.join(args.runs, V, f"alg_{L}", "eval_heldout.json"))
            nueva = cargar(os.path.join(args.out, V, f"alg_{L}", "eval_heldout.json"))
            lim = vieja["config"]["num_tokens"]
            ho = heldout_df(os.path.join(args.targets_dir, f"targets_v8_{L}.csv"), args.split)
            alias = dict(zip(ho["prompt"], ho["aliases"]))
            nuevas = {r["prompt"]: r for r in nueva["splits"]["heldout"]}
            for c in CONDS:
                n_cort = antes = ahora = siguen = no_pref = 0
                tot_antes = tot_ahora = n_ans = 0
                for r in vieja["splits"]["heldout"]:
                    if not r["has_answer"]:
                        continue
                    n_ans += 1
                    ok_v = answer_correct(r[c], r["answer"], alias[r["prompt"]])
                    tot_antes += ok_v
                    rn = nuevas.get(r["prompt"])
                    if rn is None or not cortada(tok, r[c], lim, args.umbral):
                        tot_ahora += ok_v
                        continue
                    ok_n = answer_correct(rn[c], r["answer"], alias[r["prompt"]])
                    tot_ahora += ok_n
                    n_cort += 1
                    antes += ok_v
                    ahora += ok_n
                    siguen += cortada(tok, rn[c], args.num_tokens, args.umbral)
                    if not rn[c].startswith(r[c][: max(1, len(r[c]) - 20)]):
                        no_pref += 1
                    if ok_n != ok_v:
                        detalle.append((V, L, c, r["idx"], r["prompt"], r["answer"], ok_v, ok_n, rn[c]))
                rep[f"{V}/{L}/{c}"] = {"cortadas": n_cort, "correctas_antes": antes, "correctas_ahora": ahora,
                                       "siguen_cortadas": siguen, "no_prefijo": no_pref, "n": n_ans,
                                       "heldout_antes": tot_antes, "heldout_ahora": tot_ahora}
                tabla.append(f"| {V} | {L} | {NOMBRE[c]} | {n_cort} | {antes} | {ahora} | {siguen} | "
                             f"{tot_antes}/{n_ans} ({tot_antes / n_ans:.1%}) | "
                             f"{tot_ahora}/{n_ans} ({tot_ahora / n_ans:.1%}) | {no_pref} |")
    lineas += tabla + ["",
                       "`no-prefijo`: salidas nuevas que no empiezan con la vieja. Con greedy deberia ser 0; "
                       "si no lo es, la diferencia no es solo el largo (no determinismo de GPU, otro cache, "
                       "otro checkpoint) y esa fila no es comparable.", "",
                       "## Veredictos que cambiaron", ""]
    for V, L, c, idx, p, ans, ok_v, ok_n, txt in detalle:
        lineas += [f"### {V} {L} {NOMBRE[c]} idx {idx}: {'falla -> correcta' if ok_n else 'correcta -> falla'}",
                   f"**{p}** (respuesta: {ans})", "", "> " + txt.replace("\n", " / "), ""]
    with open(os.path.join(args.out, "reporte.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(lineas) + "\n")
    with open(os.path.join(args.out, "reporte.json"), "w", encoding="utf-8") as f:
        json.dump(rep, f, indent=2, ensure_ascii=False)
    print("\n".join(tabla))
    print(f"\n{len(detalle)} veredictos cambiaron -> {os.path.join(args.out, 'reporte.md')}")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("cmd", choices=["seleccionar", "comparar"])
    ap.add_argument("--model", required=True, help="para el tokenizer")
    ap.add_argument("--runs", default="algebra/runs")
    ap.add_argument("--targets_dir", default="attributes/v8")
    ap.add_argument("--split", type=float, default=0.84)
    ap.add_argument("--out", default="algebra/runs/cortadas_250")
    ap.add_argument("--umbral", type=float, default=0.95,
                    help="fraccion del limite de tokens a partir de la cual una salida cuenta como cortada "
                         "(la re-tokenizacion del texto decodificado no da exactamente el mismo largo)")
    ap.add_argument("--num_tokens", type=int, default=250, help="limite de la re-generacion (comparar)")
    args = ap.parse_args()
    {"seleccionar": cmd_seleccionar, "comparar": cmd_comparar}[args.cmd](args)


if __name__ == "__main__":
    main()
