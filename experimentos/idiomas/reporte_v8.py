"""
Reportes del entrenamiento v8 (run_train_v8.sh): uno por etapa, en
<runs>/reportes/<etapa>.md, escrito al terminar la etapa.

    train   norma final, epoch elegida y curva de CE (lang_metadata.pt de cada celda)
    A       held-out v8 (112 filas, 16 por categoria), POR CATEGORIA:
              ingles (baseline / referencia con instruccion / parche),
              otros idiomas de entrenamiento, italiano y portugues (no vistos)
    C       sets abiertos: open1 (99) y open2 (50 imperativos, por idioma de entrada)
    D       chequeos sin generacion: token mas cercano, normas y cosenos entre las
            direcciones v8 y contra las del paper (algebra/runs/alg_*)
    E       tests de comportamiento: resta q_L - v (con controles) y entrada o
            directiva (identificacion de idioma, resta contra instruccion, conflicto)

    python3 reporte_v8.py A --runs algebra/runs/v8 --targets_dir attributes/v8 --split 0.84
"""

import argparse
import collections
import json
import os

import pandas as pd

CELDAS = ("fr", "es", "de")
ORDEN = ["factual_clasica", "factual_aperturas", "imperativo", "imperativo_explicativo",
         "explicativa", "corta", "conversacional"]
NOMBRE = {"fr": "francés", "es": "español", "de": "alemán", "en": "inglés", "it": "italiano", "pt": "portugués"}
COL_LANG = {"prompt": "en", "prompt_es": "es", "prompt_de": "de", "prompt_fr": "fr",
            "prompt_it": "it", "prompt_pt": "pt"}


def cargar(path):
    if not os.path.exists(path):
        return None
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def pct(x):
    return "—" if x is None or x != x else f"{100 * x:.0f}"


def media(vals):
    vals = [bool(v) for v in vals if v is not None]
    return sum(vals) / len(vals) if vals else float("nan")


def categorias(targets_dir, celda, split):
    df = pd.read_csv(os.path.join(targets_dir, f"targets_v8_{celda}.csv"), sep=";",
                     keep_default_na=False, dtype=str)
    corte = int(len(df) * split)
    return df, corte


def tabla(cab, filas):
    out = ["| " + " | ".join(cab) + " |", "|" + "---|" * len(cab)]
    out += ["| " + " | ".join(str(c).replace("|", "·") for c in f) + " |" for f in filas]
    return "\n".join(out)


# --------------------------------------------------------------------------- train
def r_train(args):
    import torch
    L = ["# Etapa train", ""]
    filas = []
    for c in CELDAS:
        meta_p = os.path.join(args.runs, f"alg_{c}", "lang_metadata.pt")
        if not os.path.exists(meta_p):
            filas.append([c, "falta", "", "", "", ""])
            continue
        m = torch.load(meta_p, map_location="cpu", weights_only=False)
        v = torch.load(os.path.join(args.runs, f"alg_{c}", "lang_patch_best_train.pt"), map_location="cpu")
        cur = m.get("curva", [])
        filas.append([c, m["train_size"], m["test_size"], f"{v.norm().item():.3f}",
                      m["best_train_epoch"], f"{m['best_train_head_ce']:.3f}"])
        L.append(f"Curva {c} (CE head, checkpoint de cada epoch): " + ", ".join(
            f"e{x['epoch']}: train {x['train_head']:.3f} / held-out {x['heldout_head']:.3f} (norma {x['norm']:.3f})"
            for x in cur))
        L.append("")
    L[2:2] = [tabla(["celda", "filas train", "held-out", "norma ‖v‖", "epoch elegida", "CE head train"], filas), ""]
    return L


# --------------------------------------------------------------------------- A
def r_A(args):
    L = ["# Etapa A: held-out v8 por categoria", "",
         f"Held-out = filas desde int(700*{args.split}) del CSV de cada celda (16 por categoria). "
         "Idioma: GlotLID (lang_id.py). Accuracy: answer_correct con los alias del banco (6 idiomas). "
         f"Generacion de {args.num_tokens} tokens, referencia y baseline regenerados con el mismo largo.", ""]
    for c in CELDAS:
        df, corte = categorias(args.targets_dir, c, args.split)
        held = df.iloc[corte:]
        cat_pos = list(held["categoria"])                      # eval_lang_patch: idx = posicion
        cat_idx = dict(zip(held.index, held["categoria"]))     # cross_lang: idx = indice del CSV
        L += [f"## Celda {c} (parche hacia el {NOMBRE[c]})", ""]
        ev = cargar(os.path.join(args.runs, f"alg_{c}", "eval_heldout.json"))
        if ev:
            rows = ev["splits"]["heldout"]
            filas = []
            for cat in ORDEN + ["TOTAL"]:
                rs = [r for r in rows if cat == "TOTAL" or cat_pos[r["idx"]] == cat]
                filas.append([cat, len(rs)] + [pct(media(r[f"{k}_is_target"] for r in rs)) for k in
                                               ("baseline", "reference", "patched")]
                             + [pct(media(r[f"{k}_answer_correct"] for r in rs)) for k in
                                ("baseline", "reference", "patched")])
            L += [f"### Pregunta en inglés (norma ‖v‖ = {ev['patch_norm']:.3f})", "",
                  tabla(["categoria", "n", f"% {c} sin parche", f"% {c} instrucción", f"% {c} parche",
                         "acc sin parche", "acc instrucción", "acc parche"], filas), ""]
        for nombre, archivo in (("Otros idiomas de entrenamiento", "cross_lang_idioma.json"),
                                ("Idiomas no vistos (italiano, portugués)", "cross_lang_romance.json")):
            cl = cargar(os.path.join(args.runs, f"alg_{c}", archivo))
            if not cl:
                continue
            conds = [x for x in cl["condiciones"] if x["col"] != "prompt"]
            cols = list(dict.fromkeys(x["col"] for x in conds))
            cab = ["categoria"]
            for col in cols:
                cab += [f"{COL_LANG[col]}: % {c} sin / con", f"{COL_LANG[col]}: acc sin / con"]
            filas = []
            for cat in ORDEN + ["TOTAL"]:
                f = [cat]
                for col in cols:
                    par = {x["escala"]: [r for r in x["rows"] if cat == "TOTAL" or cat_idx.get(r["idx"]) == cat]
                           for x in conds if x["col"] == col}
                    s, p = par.get(0.0, []), par.get(1.0, [])
                    f += [f"{pct(media(r['out_is_target'] for r in s))} / {pct(media(r['out_is_target'] for r in p))}",
                          f"{pct(media(r['out_answer_correct'] for r in s))} / {pct(media(r['out_answer_correct'] for r in p))}"]
                filas.append(f)
            L += [f"### {nombre}", "", tabla(cab, filas), ""]
    return L


# --------------------------------------------------------------------------- C
def r_C(args):
    L = ["# Etapa C: sets abiertos", ""]
    filas1, filas2 = [], []
    for c in CELDAS:
        ev = cargar(os.path.join(args.runs, f"alg_{c}", "eval_open.json"))
        if ev:
            m = ev["metrics"]
            filas1.append([c, ev["n_heldout"], pct(m["baseline"].get("is_target")),
                           pct(m["reference"].get("is_target")), pct(m["patched"].get("is_target"))])
        cl = cargar(os.path.join(args.runs, f"alg_{c}", "open_2", "cross_lang_idioma.json"))
        if cl:
            for col in dict.fromkeys(x["col"] for x in cl["condiciones"]):
                par = {x["escala"]: x["rows"] for x in cl["condiciones"] if x["col"] == col}
                filas2.append([c, COL_LANG[col], len(par.get(1.0, [])),
                               pct(media(r["out_is_target"] for r in par.get(0.0, []))),
                               pct(media(r["out_is_target"] for r in par.get(1.0, [])))])
    L += ["## open1: 99 prompts abiertos en inglés", "",
          tabla(["celda", "n", "% idioma sin parche", "% instrucción", "% parche"], filas1), "",
          "## open2: 50 imperativos por idioma de entrada", "",
          "Paper (alg_*, banco viejo), desde inglés: fr 48, es 74, de 60.", "",
          tabla(["celda", "entrada", "n", "% idioma sin parche", "% parche"], filas2), ""]
    return L


# --------------------------------------------------------------------------- D
def r_D(args):
    import torch
    L = ["# Etapa D: chequeos sin generación", ""]
    vec = {}
    for c in CELDAS:
        for nombre, p in ((f"v8_{c}", os.path.join(args.runs, f"alg_{c}", "lang_patch_best_train.pt")),
                          (f"paper_{c}", os.path.join(args.paper_runs, f"alg_{c}", "lang_patch_best_train.pt"))):
            if os.path.exists(p):
                vec[nombre] = torch.load(p, map_location="cpu").float().flatten()
    nombres = list(vec)
    filas = [[a, f"{vec[a].norm():.3f}"] + [f"{torch.nn.functional.cosine_similarity(vec[a], vec[b], dim=0):.2f}"
                                            for b in nombres] for a in nombres]
    L += ["## Normas y cosenos", "", "Referencia del paper: réplica de alg_fr con otro orden de batches = 0.49; "
          "dos direcciones al azar en d=3072 = ±0.018.", "",
          tabla(["vector", "‖v‖"] + nombres, filas), ""]
    filas = []
    for c in CELDAS:
        nt = cargar(os.path.join(args.runs, f"alg_{c}", "nearest_token", "nearest_token.json"))
        if nt is None:
            continue
        for x in nt["conds"]:
            if x["vec"] == "v":
                filas.append([c, x["alpha"], COL_LANG.get(x["col"], x["col"]), x["n_tok"],
                              pct(x["cambia_l2"]), pct(x["cambia_cos"])])
        L += [f"Celda {c}: ‖v‖ = {nt['v_norm']:.3f}; supera la norma del {100 * nt['pct_norma_vocab']:.1f}% "
              f"del vocabulario y del {100 * nt['pct_norma_preguntas']:.1f}% de los tokens de las preguntas; "
              f"distancia mediana token-vecino {nt['gap_median']:.2f}.", ""]
    if filas:
        L += ["## Token más cercano de e + α·v (§4.1)", "",
              tabla(["celda", "α", "entrada", "tokens", "% cambia (L2)", "% cambia (coseno)"], filas), ""]
    return L


# --------------------------------------------------------------------------- E
def r_E(args):
    L = ["# Etapa E: tests de comportamiento", ""]
    res = cargar(os.path.join(args.runs, "resta", "entrada_o_directiva_resta.json"))
    if res:
        filas = []
        for x in res["condiciones"]:
            lang_q = COL_LANG[x["col"]]
            rows = x["rows"]
            quedan = media(r["out_lang"] in (lang_q, "unknown") for r in rows)
            destinos = collections.Counter(r["out_lang"] for r in rows if r["out_lang"] not in (lang_q, "unknown"))
            dest = ", ".join(f"{k} {100 * v / len(rows):.0f}" for k, v in destinos.most_common(4))
            filas.append([lang_q, "—" if x["parche"] == "-" else f"{x['escala']:+g}·{x['parche']}",
                          len(rows), pct(quedan), dest, pct(media(r["out_answer_correct"] for r in rows))])
        L += ["## Resta q_L − v (equivale a las Tablas 5 y 6)", "",
              "Quedan: la respuesta sigue en el idioma de la pregunta o sin idioma identificable.", "",
              tabla(["pregunta en", "restado", "n", "% quedan", "destinos (%)", "acc"], filas), ""]
    for test, titulo in (("idioma_entrada", "Identificación de idioma (Tabla 7)"),
                         ("resta_directiva", "Resta contra una instrucción (Tabla 8)"),
                         ("conflicto", "Instrucción en conflicto (Tabla 9)")):
        t = cargar(os.path.join(args.runs, "tests", f"entrada_o_directiva_{test}.json"))
        if not t:
            continue
        filas = []
        for x in t["condiciones"]:
            m = x["metrics"]
            if test == "idioma_entrada":
                filas.append([x["label"], m["n"], pct(m["dice_en"]), pct(m["dice_fr"]), pct(m["dice_es"]),
                              pct(m["dice_de"]), pct(m["dice_ninguno"])])
            else:
                filas.append([x["label"], m["n"], pct(m["p_fr"]), pct(m["p_en"]), pct(m["p_unknown"]),
                              pct(m["answer_correct"])])
        cab = (["condición", "n", "dice en", "dice fr", "dice es", "dice de", "ninguno"] if test == "idioma_entrada"
               else ["condición", "n", "% fr", "% en", "% sin idioma", "acc"])
        L += [f"## {titulo}", "", tabla(cab, filas), ""]
    return L


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("etapa", choices=["train", "A", "C", "D", "E"])
    ap.add_argument("--runs", default="algebra/runs/v8")
    ap.add_argument("--paper_runs", default="algebra/runs")
    ap.add_argument("--targets_dir", default="attributes/v8")
    ap.add_argument("--split", type=float, default=0.84)
    ap.add_argument("--num_tokens", type=int, default=150)
    args = ap.parse_args()
    L = {"train": r_train, "A": r_A, "C": r_C, "D": r_D, "E": r_E}[args.etapa](args)
    out_dir = os.path.join(args.runs, "reportes")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, f"{args.etapa}.md")
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(L) + "\n")
    print("\n".join(L))
    print(f"\nreporte: {path}")


if __name__ == "__main__":
    main()
