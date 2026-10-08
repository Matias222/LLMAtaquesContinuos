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

regate
    Despues de fix_targets_v8.py (correcciones a mano): copia los alias del banco
    a las filas nuevas y rehace veredicto de idioma (GlotLID), accuracy y gate con
    gate_v8 (ver su docstring). Las 100 viejas no se tocan.

alias
    Solo la columna `aliases` de las 700 filas: nuevas = banco, viejas = las suyas
    + data/banco_v8/viejas_alias.csv. No toca gates.

abiertos
    open1/open2 de cada celda con la pregunta en fr/es/de (control nativo).

Para otro modelo (run_targets_qwen3.sh): `armar --regenerar_viejas` deja las 100
viejas sin output/baseline/gate (las genera el modelo nuevo; las guardadas son de
Llama), `regate --incluir_viejas` les aplica gate_v8 con sus alias, y
`abiertos --sin_output` vacia el target de Llama de los sets abiertos (la CE del
control nativo se mide entonces contra M(q_X) del modelo nuevo).

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
    if args.regenerar_viejas:
        # targets de otro modelo: se conservan pregunta, respuesta, alias y traducciones;
        # todo lo generado por Llama (target, baseline, veredictos, gate) queda vacio
        generadas = [c for c in viejas.columns
                     if c in ("output", "baseline_en", "passed_gate", "output_hand_fixed")
                     or c.startswith("ref_") or c.startswith("baseline_")]
        viejas[generadas] = ""
        print(f"--regenerar_viejas: vaciadas {generadas}")
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


CAT_TERMINO = ("imperativo_explicativo", "explicativa")
ESTUDIO = {"fr", "en", "es", "de", "it", "pt"}
# ingles que se cuela en la cabeza del target (ver fix_targets_v8.py)
_EN_CABEZA = re.compile(r"\((?:[^)]*\b(?:of course|that's|understood|a random thought|in german|in english)"
                        r"\b[^)]*)\)", re.I)


def gate_v8(categoria, celda, lang, acc, output):
    """
    Gate de las 600 nuevas (las 100 viejas conservan el suyo):
      - nunca: veredicto 'unknown' (respuesta de 1-2 palabras: sin senal de idioma
        en los K=8 tokens de la perdida) ni ingles entre parentesis en la cabeza;
      - categorias de termino clave (3, 4): solo idioma == celda. La accuracy ahi
        mide si el termino aparece antes del corte de 100 tokens, no si la
        respuesta es correcta (revision del 2026-10-06);
      - el resto: accuracy, y que el veredicto no sea OTRO idioma del estudio
        (catalan, gallego, danes... sobre frases cortas son confusiones de GlotLID).
    """
    if lang == "unknown" or _EN_CABEZA.search(output[:200]):
        return False
    if categoria in CAT_TERMINO:
        return lang == celda
    return bool(acc) and not (lang in ESTUDIO and lang != celda)


def cmd_regate(args):
    """Rehace alias, veredicto de idioma, accuracy y gate de las filas nuevas."""
    from checkers import answer_correct, language_verdict
    banco = pd.read_csv(args.banco, sep=";", keep_default_na=False, dtype=str)
    alias = dict(zip(banco["prompt"], banco["aliases"]))
    for celda in ("fr", "es", "de"):
        path = os.path.join(args.dir, f"targets_v8_{celda}.csv")
        df = pd.read_csv(path, sep=";", keep_default_na=False, dtype=str)
        nuevas = df.index[df["categoria"] != CAT_VIEJA] if not args.incluir_viejas else df.index
        antes = df["passed_gate"].str.lower() == "true"
        for i in nuevas:
            p = df.at[i, "prompt"]
            if df.at[i, "categoria"] == CAT_VIEJA:
                al = df.at[i, "aliases"]          # las viejas: sus alias (correr `alias` antes)
            elif p not in alias:
                raise SystemExit(f"[{celda}] {p!r} no esta en {args.banco}")
            else:
                al = df.at[i, "aliases"] = alias[p]
            if not df.at[i, "output"].strip():
                raise SystemExit(f"[{celda}] {p!r} sin output: generar los targets antes del regate")
            lang = language_verdict(df.at[i, "output"])
            acc = answer_correct(df.at[i, "output"], df.at[i, "answer"], al)
            df.at[i, "ref_language"] = lang
            df.at[i, "ref_answer_correct"] = str(bool(acc))
            df.at[i, "passed_gate"] = str(gate_v8(df.at[i, "categoria"], celda, lang, acc, df.at[i, "output"]))
        despues = df["passed_gate"].str.lower() == "true"
        corte = int(0.8 * len(df))
        print(f"\n=== {celda}: gate {antes.sum()} -> {despues.sum()} de {len(df)}  "
              f"(train, primeras {corte}: {antes[:corte].sum()} -> {despues[:corte].sum()})")
        print(f"  {'categoria':<24}{'antes':>7}{'despues':>9}{'  train':>8}")
        en_train = pd.Series(range(len(df)), index=df.index) < corte
        for cat in ORDEN:
            m = df["categoria"] == cat
            print(f"  {cat:<24}{antes[m].sum():>7}{despues[m].sum():>9}{despues[m & en_train].sum():>8}")
        if not args.dry_run:
            df.to_csv(path, sep=";", index=False)
    if args.dry_run:
        print("\n--dry_run: no se escribe nada")


HELDOUT_ROMANCE = "data/banco_v8/traducciones/heldout_romance.csv"
VIEJAS_ALIAS = "data/banco_v8/viejas_alias.csv"
IMPERATIVAS = ("imperativo", "imperativo_explicativo")


def cmd_heldout(args):
    """
    Prepara el held-out (ultimas filas con el split dado) para evaluar:
      - prompt_it / prompt_pt escritos a mano (idiomas de entrada NO vistos en train),
        solo existen para el held-out, como en el banco del paper.
    Los alias van aparte (subcomando alias).
    Valida: todas las filas del held-out tienen it/pt, sin fuga de la respuesta y
    con la forma de su categoria (imperativo sin '?', el resto con '?').
    """
    from checkers import answer_correct
    tr = pd.read_csv(HELDOUT_ROMANCE, sep=";", keep_default_na=False, dtype=str).set_index("prompt")
    errores = []
    for celda in ("fr", "es", "de"):
        path = os.path.join(args.dir, f"targets_v8_{celda}.csv")
        df = pd.read_csv(path, sep=";", keep_default_na=False, dtype=str)
        corte = int(len(df) * args.split)
        held = df.index[corte:]
        for c in ("prompt_it", "prompt_pt"):
            for col in (c, f"{c}_language", f"{c}_ok"):
                if col not in df.columns:
                    df[col] = ""
        for i in held:
            p = df.at[i, "prompt"]
            if p not in tr.index:
                errores.append(f"[{celda}] falta traduccion it/pt de {p!r}")
                continue
            for c, lang in (("prompt_it", "it"), ("prompt_pt", "pt")):
                t = tr.at[p, c].strip()
                df.at[i, c], df.at[i, f"{c}_language"], df.at[i, f"{c}_ok"] = t, lang, "True"
                if celda != "fr":
                    continue                      # validar una sola vez
                if not t:
                    errores.append(f"{c} vacia: {p!r}")
                if answer_correct(t, df.at[i, "answer"], df.at[i, "aliases"]):
                    errores.append(f"{c} fuga de la respuesta: {t!r}")
                if (df.at[i, "categoria"] in IMPERATIVAS) == t.endswith("?"):
                    errores.append(f"{c} forma equivocada para {df.at[i, 'categoria']}: {t!r}")
        sobran = set(tr.index) - set(df.loc[held, "prompt"])
        if sobran:
            errores.append(f"[{celda}] traducciones de preguntas que no estan en el held-out: {sorted(sobran)[:5]}")
        print(f"[{celda}] held-out {len(held)} filas (split {args.split}: train {corte}) | "
              f"por categoria: {df.loc[held, 'categoria'].value_counts().to_dict()}")
        if not args.dry_run:
            df.to_csv(path, sep=";", index=False)
    for e in errores:
        print("ERROR", e)
    if errores:
        sys.exit(1)
    print("held-out listo" + (" (dry run)" if args.dry_run else ""))


def cmd_alias(args):
    """
    Solo la columna `aliases`, en las 700 filas de las tres celdas (no toca gate ni
    accuracy guardada, asi el train queda identico):
      - nuevas: los alias del banco (data/banco_v8, ampliados tras revisar fallas);
      - viejas: sus alias de siempre + los de data/banco_v8/viejas_alias.csv (las
        viejas traian solo ingles + frances; ahora es/de/it/pt).
    Idempotente.
    """
    from checkers import answer_correct
    banco = pd.read_csv(args.banco, sep=";", keep_default_na=False, dtype=str)
    banco = dict(zip(banco["prompt"], banco["aliases"]))
    extra = pd.read_csv(VIEJAS_ALIAS, sep=";", keep_default_na=False, dtype=str)
    extra = dict(zip(extra["prompt"], extra["aliases_extra"]))
    for celda in ("fr", "es", "de"):
        path = os.path.join(args.dir, f"targets_v8_{celda}.csv")
        df = pd.read_csv(path, sep=";", keep_default_na=False, dtype=str)
        faltan = set(extra) - set(df.loc[df["categoria"] == CAT_VIEJA, "prompt"])
        if faltan:
            raise SystemExit(f"[{celda}] viejas_alias con preguntas que no son viejas: {sorted(faltan)[:3]}")
        cambios, acc_antes, acc_despues = 0, 0, 0
        for i in df.index:
            p, a0 = df.at[i, "prompt"], df.at[i, "aliases"]
            if df.at[i, "categoria"] == CAT_VIEJA:
                viejos = [a for a in a0.split("|") if a.strip()]
                nuevo = "|".join(viejos + [a for a in extra.get(p, "").split("|") if a.strip() and a not in viejos])
            else:
                if p not in banco:
                    raise SystemExit(f"[{celda}] {p!r} no esta en {args.banco}")
                nuevo = banco[p]
            acc_antes += answer_correct(df.at[i, "output"], df.at[i, "answer"], a0)
            acc_despues += answer_correct(df.at[i, "output"], df.at[i, "answer"], nuevo)
            if nuevo != a0:
                df.at[i, "aliases"] = nuevo
                cambios += 1
        print(f"[{celda}] alias cambiados en {cambios} filas | accuracy del target "
              f"(700 filas): {acc_antes} -> {acc_despues}")
        if cambios and not args.dry_run:
            df.to_csv(path, sep=";", index=False)
    if args.dry_run:
        print("--dry_run: no se escribe nada")


OPEN1 = {"fr": "attributes/french/targets_open.csv", "es": "algebra/targets/targets_es_open.csv",
         "de": "algebra/targets/targets_de_open.csv"}
OPEN2 = {"fr": "attributes/french/targets_open_2.csv", "es": "algebra/targets/targets_es_open_2.csv",
         "de": "algebra/targets/targets_de_open_2.csv"}
OPEN1_TRAD = "data/banco_v8/traducciones/open1.csv"


def cmd_abiertos(args):
    """
    Sets abiertos con la pregunta en los tres idiomas, para el control nativo M(q_X):
      open1_<celda>.csv = el CSV de la celda + prompt_es/de/fr escritos a mano
                          (data/banco_v8/traducciones/open1.csv);
      open2_<celda>.csv = el CSV de la celda + las columnas prompt_<l> que le falten,
                          copiadas de las otras celdas (fr no traia prompt_fr).
    Los targets (output) de cada celda no se tocan.
    """
    os.makedirs(args.out, exist_ok=True)
    tr = pd.read_csv(OPEN1_TRAD, sep=";", keep_default_na=False, dtype=str)
    o2 = {c: pd.read_csv(f, sep=";", keep_default_na=False, dtype=str) for c, f in OPEN2.items()}
    for celda in ("fr", "es", "de"):
        df = pd.read_csv(OPEN1[celda], sep=";", keep_default_na=False, dtype=str)
        if list(df["prompt"]) != list(tr["prompt"]):
            raise SystemExit(f"[{celda}] open1: las preguntas no coinciden con {OPEN1_TRAD}")
        for l in ("es", "de", "fr"):
            df[f"prompt_{l}"], df[f"prompt_{l}_language"], df[f"prompt_{l}_ok"] = tr[f"prompt_{l}"], l, "True"
        if args.sin_output:
            df["output"] = df["baseline_en"] = ""
        df.to_csv(os.path.join(args.out, f"open1_{celda}.csv"), sep=";", index=False)
        d2 = o2[celda].copy()
        for l in ("es", "de", "fr"):
            if f"prompt_{l}" in d2.columns:
                continue
            fuente = next(c for c in ("fr", "es", "de") if f"prompt_{l}" in o2[c].columns)
            if list(o2[fuente]["prompt"]) != list(d2["prompt"]):
                raise SystemExit(f"[{celda}] open2: preguntas distintas a las de {fuente}")
            for suf in ("", "_language", "_ok"):
                d2[f"prompt_{l}{suf}"] = o2[fuente][f"prompt_{l}{suf}"]
            print(f"[{celda}] open2: prompt_{l} copiada de la celda {fuente}")
        if args.sin_output:
            d2["output"] = d2["baseline_en"] = ""
        d2.to_csv(os.path.join(args.out, f"open2_{celda}.csv"), sep=";", index=False)
        print(f"[{celda}] open1 {len(df)} filas, open2 {len(d2)} filas -> {args.out}")


def cmd_igualar(args):
    """
    Las tres celdas entrenan con la MISMA cantidad de filas: la del minimo entre
    celdas (fr, 549 con el split 0.84) o --n. Las celdas que tienen mas pierden
    filas de train hasta igualar, eligiendo para maximizar el parecido con la
    celda de referencia (la de menos filas):
      1. solo filas que NO pasan el gate en la celda de referencia;
      2. de la categoria con mas excedente respecto de la referencia;
      3. dentro de la categoria, la fila de indice mas alto.
    Las recortadas quedan passed_gate=False y recorte='igualar_<n>'. Idempotente.
    """
    dfs = {c: pd.read_csv(os.path.join(args.dir, f"targets_v8_{c}.csv"), sep=";",
                          keep_default_na=False, dtype=str) for c in ("fr", "es", "de")}
    corte = int(len(dfs["fr"]) * args.split)
    ok = {c: [i for i in range(corte) if d.at[i, "passed_gate"].lower() == "true"] for c, d in dfs.items()}
    n = args.n or min(len(v) for v in ok.values())
    ref = min(ok, key=lambda c: len(ok[c]))
    ref_set = set(ok[ref])
    ref_cat = dfs[ref].loc[ok[ref], "categoria"].value_counts()
    for c, d in dfs.items():
        if "recorte" not in d.columns:
            d["recorte"] = ""
        sobra = len(ok[c]) - n
        sacadas = []
        while sobra > 0:
            vivas = [i for i in ok[c] if i not in sacadas]
            exceso = (d.loc[vivas, "categoria"].value_counts() - ref_cat).fillna(0)
            candidatas = [i for i in vivas if i not in ref_set] or vivas
            orden = sorted(candidatas, key=lambda i: (-exceso.get(d.at[i, "categoria"], 0), -i))
            sacadas.append(orden[0])
            sobra -= 1
        for i in sacadas:
            d.at[i, "passed_gate"] = "False"
            d.at[i, "recorte"] = f"igualar_{n}"
        quedan = [i for i in ok[c] if i not in sacadas]
        print(f"[{c}] train {len(ok[c])} -> {len(quedan)}  (recortadas {len(sacadas)}: "
              f"{d.loc[sacadas, 'categoria'].value_counts().to_dict() if sacadas else {}})  "
              f"comparte con {ref}: {len(set(quedan) & ref_set)}")
        if sacadas and not args.dry_run:
            d.to_csv(os.path.join(args.dir, f"targets_v8_{c}.csv"), sep=";", index=False)
    if args.dry_run:
        print("--dry_run: no se escribe nada")


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
    a.add_argument("--regenerar_viejas", action="store_true",
                   help="las 100 viejas sin output/baseline/gate (targets de otro modelo)")
    r = sub.add_parser("restaurar")
    r.add_argument("--lang", choices=["es", "de"], required=True)
    r.add_argument("--csv", required=True)
    r.add_argument("--viejo", default=None, help=f"default {VIEJO_ATTR}")
    g = sub.add_parser("regate")
    g.add_argument("--dir", required=True)
    g.add_argument("--banco", default=BANCO)
    g.add_argument("--dry_run", action="store_true")
    g.add_argument("--incluir_viejas", action="store_true",
                   help="aplicar gate_v8 tambien a las 100 viejas (targets de otro modelo)")
    h = sub.add_parser("heldout")
    h.add_argument("--dir", required=True)
    h.add_argument("--split", type=float, default=0.84)
    h.add_argument("--dry_run", action="store_true")
    al = sub.add_parser("alias")
    al.add_argument("--dir", required=True)
    al.add_argument("--banco", default=BANCO)
    al.add_argument("--dry_run", action="store_true")
    ab = sub.add_parser("abiertos")
    ab.add_argument("--out", required=True)
    ab.add_argument("--sin_output", action="store_true",
                    help="vaciar output y baseline_en (de Llama) de los sets abiertos: para otro modelo")
    q = sub.add_parser("igualar")
    q.add_argument("--dir", required=True)
    q.add_argument("--split", type=float, default=0.84)
    q.add_argument("--n", type=int, default=0, help="filas de train por celda (0 = el minimo entre celdas)")
    q.add_argument("--dry_run", action="store_true")
    v = sub.add_parser("revisar")
    v.add_argument("--dir", required=True)
    args = ap.parse_args()
    {"armar": cmd_armar, "restaurar": cmd_restaurar, "regate": cmd_regate,
     "heldout": cmd_heldout, "alias": cmd_alias, "abiertos": cmd_abiertos, "igualar": cmd_igualar, "revisar": cmd_revisar}[args.cmd](args)


if __name__ == "__main__":
    main()
