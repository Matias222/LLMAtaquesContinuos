"""
Banco de entrenamiento v8: las 600 preguntas de data/banco_v8 + las primeras 100
factuales del banco viejo (targets_french_v5.csv, filas 0-99, todas de train).
Lo usa run_targets_v8.sh; tres subcomandos.

armar
    Escribe el CSV de targets en frances con las 700 filas intercaladas por
    categoria (factual_clasica, factual_aperturas, imperativo, ...), asi que
    cualquier corte posicional queda balanceado. Las 100 viejas entran ENTERAS
    (output, baseline_en, gate, prompt_es/de/fr con las correcciones de
    fix_translations.py y los 12 targets corregidos a mano); las 600 nuevas
    entran con `output` vacio, que es lo que completa `generate_targets.py --fill`,
    y con las traducciones escritas a mano de data/banco_v8/traducciones (el
    traductor del modelo convertia imperativos y fragmentos en preguntas).
    Antes de escribir verifica que ninguna pregunta nueva repita una vieja
    (prompt normalizado: ERROR) y lista las respuestas compartidas (aviso: un
    mismo nombre puede responder dos preguntas distintas, p.ej. 'Moon').

restaurar
    generate_targets_attr.py (celdas es / de) no tiene modo --fill: regenera
    las 700. Esto devuelve a las 100 viejas el `output` y el gate de
    algebra/targets/targets_<lang>.csv (con las correcciones de fix_targets.py)
    y cuenta cuantas salidas difieren de lo regenerado (greedy: deberian ser
    las mismas salvo las corregidas a mano).

revisar
    Reporte final por celda y por categoria: filas sin output, gate, accuracy
    de la referencia, veredictos de idioma, traducciones usables por columna y
    fugas del few-shot del traductor (copias de "capitale du Japon", "Hamlet",
    "digestion" en preguntas que no hablan de eso).

    python3 preparar_targets_v8.py armar --out attributes/v8/targets_v8_fr.csv
    python3 preparar_targets_v8.py restaurar --lang es --csv attributes/v8/targets_v8_es.csv
    python3 preparar_targets_v8.py revisar --dir attributes/v8
"""

import argparse
import collections
import os
import re
import sys

import pandas as pd

from checkers import fold

BANCO = "data/banco_v8/banco_v8_intercalado.csv"
VIEJO = "attributes/french/targets_french_v5.csv"
VIEJO_ATTR = "algebra/targets/targets_{lang}.csv"
N_VIEJAS = 100
CAT_VIEJA = "factual_clasica"
ORDEN = [CAT_VIEJA, "factual_aperturas", "imperativo", "imperativo_explicativo",
         "explicativa", "corta", "conversacional"]
# columnas que restaurar devuelve desde el CSV viejo de la celda
COLS_ATTR = ("output", "ref_role_leak", "ref_language", "ref_target_score", "ref_uppercase_score",
             "ref_attr_ok", "ref_answer_correct", "passed_gate")
# lo que el few-shot de translate_questions.py puede filtrar a una traduccion
FEWSHOT = {"japon": "japan", "japan": "japan", "hamlet": "hamlet", "digestion": "digestion",
           "verdauung": "digestion"}


def norm(s):
    return re.sub(r"\s+", " ", fold(str(s)).strip(" ?.!"))


def cmd_armar(args):
    if os.path.exists(args.out) and not args.force:
        raise SystemExit(f"{args.out} ya existe (tiene lo generado). --force para rehacerlo desde cero.")
    viejo = pd.read_csv(args.viejo, sep=";", keep_default_na=False, dtype=str)
    corte = int(len(viejo) * 0.8)
    if args.n_viejas > corte:
        raise SystemExit(f"--n_viejas {args.n_viejas} entra en el held-out del banco viejo (desde {corte})")
    viejas = viejo.iloc[:args.n_viejas].copy()
    nuevas = pd.read_csv(args.banco, sep=";", keep_default_na=False, dtype=str)

    # --- repeticiones -------------------------------------------------------
    errores = []
    pv = {norm(p): p for p in viejas["prompt"]}
    for p in nuevas["prompt"]:
        if norm(p) in pv:
            errores.append(f"pregunta repetida: {p!r} == {pv[norm(p)]!r}")
    for lado, df in (("viejas", viejas), ("nuevas", nuevas)):
        for p, n in collections.Counter(norm(x) for x in df["prompt"]).items():
            if n > 1:
                errores.append(f"pregunta repetida {n} veces dentro de las {lado}: {p!r}")
    rv = collections.defaultdict(list)
    for _, r in viejas.iterrows():
        rv[norm(r["answer"])].append(r["prompt"])
    compartidas = [(r["prompt"], r["answer"], rv[norm(r["answer"])]) for _, r in nuevas.iterrows()
                   if norm(r["answer"]) in rv]
    print(f"viejas: {len(viejas)} (filas 0-{args.n_viejas - 1} de {args.viejo})  |  nuevas: {len(nuevas)}")
    print(f"respuestas compartidas entre nuevas y viejas: {len(compartidas)} (misma respuesta, otra pregunta)")
    for p, a, ps in compartidas:
        print(f"  aviso  {a!r}: {p!r}  <->  {ps}")
    for e in errores:
        print("  ERROR  " + e)
    if errores:
        sys.exit(1)

    # --- intercalado --------------------------------------------------------
    viejas["categoria"] = CAT_VIEJA
    viejas["n_tokens"] = ""
    nuevas_full = pd.DataFrame("", index=range(len(nuevas)), columns=list(viejas.columns))
    for c in ("prompt", "answer", "aliases", "categoria", "n_tokens"):
        nuevas_full[c] = nuevas[c].values
    # traducciones escritas a mano (build_banco_v8.py ya las valido): entran como
    # usables, igual que las viejas que pasaron el gate de translate_questions.py
    for c in ("prompt_es", "prompt_de", "prompt_fr"):
        if c not in nuevas.columns:
            raise SystemExit(f"{args.banco} no tiene {c}: correr build_banco_v8.py con las traducciones")
        nuevas_full[c] = nuevas[c].values
        nuevas_full[f"{c}_language"] = c.split("_")[1]
        nuevas_full[f"{c}_ok"] = "True"
    grupos = {CAT_VIEJA: viejas.reset_index(drop=True)}
    for cat in ORDEN[1:]:
        grupos[cat] = nuevas_full[nuevas_full["categoria"] == cat].reset_index(drop=True)
    tam = {c: len(g) for c, g in grupos.items()}
    if len(set(tam.values())) != 1:
        raise SystemExit(f"categorias de distinto tamanio, el intercalado no queda parejo: {tam}")
    filas = [grupos[c].iloc[i] for i in range(next(iter(tam.values()))) for c in ORDEN]
    out = pd.DataFrame(filas).reset_index(drop=True)
    if args.n:
        # humo: n filas por categoria, mismo intercalado
        out = out.head(args.n * len(ORDEN))
    os.makedirs(os.path.dirname(os.path.abspath(args.out)), exist_ok=True)
    out.to_csv(args.out, sep=";", index=False)
    print(f"escrito {args.out}: {len(out)} filas, {(out['output'].str.strip() == '').sum()} sin output "
          f"(las genera generate_targets.py --fill)")
    print(f"orden: {' -> '.join(ORDEN)}")


def cmd_restaurar(args):
    gen = pd.read_csv(args.csv, sep=";", keep_default_na=False, dtype=str)
    viejo = pd.read_csv(args.viejo or VIEJO_ATTR.format(lang=args.lang), sep=";",
                        keep_default_na=False, dtype=str)
    por_prompt = {p: i for i, p in enumerate(viejo["prompt"])}
    filas = gen.index[gen["categoria"] == CAT_VIEJA]
    distintas = []
    for i in filas:
        j = por_prompt.get(gen.at[i, "prompt"])
        if j is None:
            raise SystemExit(f"{gen.at[i, 'prompt']!r} no esta en el CSV viejo de la celda {args.lang}")
        if gen.at[i, "output"].strip() != viejo.at[j, "output"].strip():
            distintas.append((gen.at[i, "prompt"], gen.at[i, "output"], viejo.at[j, "output"]))
        for c in COLS_ATTR:
            if c in viejo.columns and c in gen.columns:
                gen.at[i, c] = viejo.at[j, c]
    gen.to_csv(args.csv, sep=";", index=False)
    print(f"[{args.lang}] restauradas {len(filas)} filas viejas en {args.csv}")
    print(f"  salidas regeneradas distintas de las guardadas: {len(distintas)} "
          "(se quedan las guardadas: incluyen las correcciones de fix_targets.py)")
    for p, nueva, vieja in distintas[:15]:
        print(f"    {p[:50]}\n      regenerada: {nueva[:90]!r}\n      guardada  : {vieja[:90]!r}")


def cmd_revisar(args):
    from checkers import answer_correct, language_verdict
    archivos = {c: os.path.join(args.dir, f"targets_v8_{c}.csv") for c in ("fr", "es", "de")}
    fr = None
    for celda, path in archivos.items():
        if not os.path.exists(path):
            print(f"falta {path}")
            continue
        df = pd.read_csv(path, sep=";", keep_default_na=False, dtype=str)
        if celda == "fr":
            fr = df
        n = len(df)
        print(f"\n=== {celda}: {path} ({n} filas)")
        vacias = (df["output"].str.strip() == "").sum()
        print(f"  sin output: {vacias}" + ("   <- FALTA GENERAR" if vacias else ""))
        df["_lang"] = [language_verdict(o) for o in df["output"]]
        df["_acc"] = [answer_correct(o, a, al) for o, a, al in zip(df["output"], df["answer"], df["aliases"])]
        df["_gate"] = df["passed_gate"].str.lower() == "true"
        print(f"  {'categoria':<24}{'n':>4}{'gate':>7}{'idioma ok':>11}{'accuracy':>10}")
        for cat in ORDEN:
            g = df[df["categoria"] == cat]
            if not len(g):
                continue
            print(f"  {cat:<24}{len(g):>4}{g['_gate'].mean():>7.0%}{(g['_lang'] == celda).mean():>11.0%}"
                  f"{g['_acc'].mean():>10.0%}")
        print(f"  veredictos: {df['_lang'].value_counts().to_dict()}")
        if celda in ("es", "de") and fr is not None and list(df["prompt"]) != list(fr["prompt"]):
            print("  FALLO: no tiene las mismas preguntas en el mismo orden que la celda fr")
    if fr is None:
        return
    print("\n=== traducciones (en el CSV fr)")
    for col in ("prompt_es", "prompt_de", "prompt_fr"):
        if col not in fr.columns:
            print(f"  falta {col}")
            continue
        vacias = (fr[col].str.strip() == "").sum()
        ok = (fr[f"{col}_ok"].str.lower() == "true").sum()
        fugas = []
        for _, r in fr.iterrows():
            t, q = fold(r[col]), fold(r["prompt"])
            fugas += [(r["prompt"], r[col]) for k, v in FEWSHOT.items() if k in t and v not in q]
        print(f"  {col}: {ok}/{len(fr)} usables, {vacias} vacias, {len(fugas)} posibles fugas del few-shot")
        for p, t in fugas[:10]:
            print(f"      {p[:45]!r} -> {t[:60]!r}")
        malas = fr[fr[f"{col}_ok"].str.lower() == "false"]
        for _, r in malas.head(10).iterrows():
            print(f"      rechazada: {r['prompt'][:45]!r} -> {r[col][:60]!r}")
    print("\nRevisar a mano: traducciones rechazadas o con fuga, y filas sin gate, antes de entrenar.")


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    a = sub.add_parser("armar")
    a.add_argument("--banco", default=BANCO)
    a.add_argument("--viejo", default=VIEJO)
    a.add_argument("--n_viejas", type=int, default=N_VIEJAS)
    a.add_argument("--out", required=True)
    a.add_argument("--n", type=int, default=0, help="humo: n filas por categoria")
    a.add_argument("--force", action="store_true")
    r = sub.add_parser("restaurar")
    r.add_argument("--lang", choices=["es", "de"], required=True)
    r.add_argument("--csv", required=True)
    r.add_argument("--viejo", default=None, help=f"default {VIEJO_ATTR}")
    v = sub.add_parser("revisar")
    v.add_argument("--dir", required=True)
    args = ap.parse_args()
    {"armar": cmd_armar, "restaurar": cmd_restaurar, "revisar": cmd_revisar}[args.cmd](args)


if __name__ == "__main__":
    main()
