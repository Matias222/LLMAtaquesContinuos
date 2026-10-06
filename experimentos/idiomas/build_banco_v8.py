"""
Valida el banco v8 (6 categorias x 100 preguntas) y arma el CSV intercalado.

    data/banco_v8/1_factual_aperturas.csv     wh-preguntas con aperturas que el train no usa
    data/banco_v8/2_imperativo.csv            orden directa con respuesta factual
    data/banco_v8/3_imperativo_explicativo.csv  orden de "explicar", respuesta = termino clave
    data/banco_v8/4_explicativa.csv           pregunta why/how, respuesta = termino clave
    data/banco_v8/5_corta.csv                 fragmento ("Capital of Peru?")
    data/banco_v8/6_conversacional.csv        marco conversacional + pregunta en una linea

Cada CSV: prompt;answer;aliases (sep ';', alias separados por '|', como data/questions.csv).
Todas las filas tienen respuesta verificable: la accuracy se mide con
checkers.answer_correct igual que en el held-out.

Traducciones: data/banco_v8/traducciones/<mismo archivo> con
prompt;prompt_es;prompt_de;prompt_fr, escritas a mano conservando la forma de la
pregunta (un imperativo sigue siendo imperativo, un fragmento sigue siendo
fragmento, el marco conversacional se traduce). translate_questions.py no sirve
para este banco: convierte todo en una pregunta estandar.

Salida: data/banco_v8/banco_v8_intercalado.csv con columnas
prompt;answer;aliases;categoria;n_tokens;prompt_es;prompt_de;prompt_fr, en orden
round-robin (c1, c2, ..., c6, c1, ...), asi cualquier corte posicional (el split
de train_lang_patch.py) queda balanceado por categoria.

ERRORES (abortan, no se escribe el intercalado):
  - un archivo sin 100 filas o sin las columnas
  - n_tokens > 10 (corta: > 6), contado como el tramo goal_all del pipeline
  - prompt repetido dentro del banco o ya presente en los bancos existentes
    (targets_french_v5, open, open_2)
  - fuga: la respuesta o un alias aparece en el propio prompt
  - imperativos (2, 3) que empiezan con un verbo de open_2 (open_2 tiene que seguir
    midiendo generalizacion a verbos no vistos) o que terminan en '?'
  - preguntas (1, 4, 5, 6) que no terminan en '?'
  - nombres de los idiomas del estudio en el prompt
  - traducciones: falta una, sobra una, o esta vacia; fuga de la respuesta en la
    traduccion; imperativo traducido como pregunta o pregunta sin '?'
AVISOS (no abortan): respuesta repetida dentro del banco o igual a una del banco
viejo; alias de menos de 4 letras (riesgo de falso positivo por substring).

El conteo de tokens usa tokenizer.json de Llama-3.2-3B-Instruct (libreria
`tokenizers`, sin cargar el modelo) y reproduce SuffixManager:
tok(prefijo + q) - tok(prefijo). Verificado contra n_patched de los evals (550/550).

    python3 build_banco_v8.py --tokenizer /ruta/a/tokenizer.json
    python3 build_banco_v8.py --tokenizer /ruta/a/tokenizer.json --dry   # solo valida
"""

import argparse
import collections
import csv
import os
import re
import sys

import pandas as pd

from checkers import answer_correct, fold

DIR = "data/banco_v8"
TRAD = "traducciones"
COLS_TRAD = ("prompt_es", "prompt_de", "prompt_fr")
CATEGORIAS = [
    ("factual_aperturas", "1_factual_aperturas.csv"),
    ("imperativo", "2_imperativo.csv"),
    ("imperativo_explicativo", "3_imperativo_explicativo.csv"),
    ("explicativa", "4_explicativa.csv"),
    ("corta", "5_corta.csv"),
    ("conversacional", "6_conversacional.csv"),
]
IMPERATIVAS = {"imperativo", "imperativo_explicativo"}
MAX_TOK = 10
MAX_TOK_CORTA = 6
N_POR_CATEGORIA = 100
SALIDA = "banco_v8_intercalado.csv"
BANCOS_VIEJOS = ("attributes/french/targets_french_v5.csv",
                 "attributes/french/targets_open.csv",
                 "attributes/french/targets_open_2.csv")
OPEN2 = "attributes/french/targets_open_2.csv"
IDIOMAS = re.compile(r"\b(english|french|spanish|german|italian|portuguese|language)\b", re.I)

# mismo template que llm_attacks/minimal_gcg/clase_prompts.py hasta el header de user
PREFIJO = ("<|begin_of_text|><|start_header_id|>system<|end_header_id|>\n\nYou are a helpful assistant"
           "<|eot_id|><|start_header_id|>user<|end_header_id|>\n\n")


def contador(tokenizer_json):
    from tokenizers import Tokenizer
    tok = Tokenizer.from_file(tokenizer_json)
    base = tok.encode(PREFIJO, add_special_tokens=False).ids

    def n_tokens(q):
        ids = tok.encode(PREFIJO + q, add_special_tokens=False).ids
        assert ids[:len(base)] == base, f"el prefijo no es estable con {q!r}"
        return len(ids) - len(base)
    return n_tokens


def norm(s):
    return re.sub(r"\s+", " ", fold(str(s)).strip(" ?.!"))


def primer_verbo(p):
    return fold(p.split()[0]).strip(",.:!?")


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--tokenizer", required=True, help="tokenizer.json de Llama-3.2-3B-Instruct")
    ap.add_argument("--dir", default=DIR)
    ap.add_argument("--dry", action="store_true", help="validar sin escribir el intercalado")
    args = ap.parse_args()

    n_tokens = contador(args.tokenizer)
    errores, avisos = [], []

    viejos_prompts, viejas_resp = set(), set()
    for p in BANCOS_VIEJOS:
        df = pd.read_csv(p, sep=";", keep_default_na=False)
        viejos_prompts |= {norm(x) for x in df["prompt"]}
        viejas_resp |= {norm(x) for x in df["answer"] if str(x).strip()}
    verbos_open2 = {primer_verbo(p) for p in pd.read_csv(OPEN2, sep=";", keep_default_na=False)["prompt"]}

    cats = {}
    for cat, fn in CATEGORIAS:
        path = os.path.join(args.dir, fn)
        if not os.path.exists(path):
            errores.append(f"falta {path}")
            continue
        df = pd.read_csv(path, sep=";", keep_default_na=False, dtype=str, quoting=csv.QUOTE_NONE)
        if list(df.columns) != ["prompt", "answer", "aliases"]:
            errores.append(f"{fn}: columnas {list(df.columns)}, esperadas prompt;answer;aliases")
            continue
        if len(df) != N_POR_CATEGORIA:
            errores.append(f"{fn}: {len(df)} filas, esperadas {N_POR_CATEGORIA}")
        df["n_tokens"] = [n_tokens(p) for p in df["prompt"]]
        df["categoria"] = cat
        cats[cat] = df

        tope = MAX_TOK_CORTA if cat == "corta" else MAX_TOK
        for i, r in df.iterrows():
            p, a, al = r["prompt"].strip(), r["answer"].strip(), r["aliases"]
            donde = f"{fn}:{i + 2} {p!r}"
            if not p or not a:
                errores.append(f"{donde}: prompt o answer vacio")
                continue
            if r["n_tokens"] > tope:
                errores.append(f"{donde}: {r['n_tokens']} tokens (max {tope})")
            if answer_correct(p, a, al):
                errores.append(f"{donde}: fuga, la respuesta o un alias esta en el prompt")
            if IDIOMAS.search(p):
                errores.append(f"{donde}: nombra un idioma del estudio")
            if cat in IMPERATIVAS:
                if primer_verbo(p) in verbos_open2:
                    errores.append(f"{donde}: verbo '{primer_verbo(p)}' esta en open_2")
                if p.endswith("?"):
                    errores.append(f"{donde}: imperativo que termina en '?'")
            elif not p.endswith("?"):
                errores.append(f"{donde}: pregunta que no termina en '?'")
            if norm(p) in viejos_prompts:
                errores.append(f"{donde}: ya esta en un banco existente")
            for x in [a] + [x for x in al.split("|") if x.strip()]:
                x = x.strip()
                if len(re.sub(r"[^A-Za-z]", "", x)) < 4 and not re.fullmatch(r"[\d.,\s]+", x) \
                        and not re.fullmatch(r"[A-Z][a-z]?", x):
                    avisos.append(f"{donde}: alias corto '{x}'")
            if norm(a) in viejas_resp:
                avisos.append(f"{donde}: respuesta '{a}' tambien es respuesta del banco viejo")

        # --- traducciones -----------------------------------------------------
        tpath = os.path.join(args.dir, TRAD, fn)
        if not os.path.exists(tpath):
            errores.append(f"falta {tpath}")
            continue
        tr = pd.read_csv(tpath, sep=";", keep_default_na=False, dtype=str, quoting=csv.QUOTE_NONE)
        if list(tr.columns) != ["prompt", *COLS_TRAD]:
            errores.append(f"{tpath}: columnas {list(tr.columns)}, esperadas prompt;{';'.join(COLS_TRAD)}")
            continue
        sin = set(df["prompt"]) - set(tr["prompt"])
        sobra = set(tr["prompt"]) - set(df["prompt"])
        for p in sorted(sin):
            errores.append(f"{tpath}: falta la traduccion de {p!r}")
        for p in sorted(sobra):
            errores.append(f"{tpath}: traduccion de una pregunta que no esta en {fn}: {p!r}")
        tr = tr.drop_duplicates("prompt").set_index("prompt")
        for c in COLS_TRAD:
            df[c] = [tr.at[p, c] if p in tr.index else "" for p in df["prompt"]]
        for i, r in df.iterrows():
            for c in COLS_TRAD:
                t = r[c].strip()
                donde = f"{fn}:{i + 2} {c} {t!r}"
                if not t:
                    errores.append(f"{donde}: vacia")
                    continue
                if answer_correct(t, r["answer"], r["aliases"]):
                    errores.append(f"{donde}: fuga, la respuesta o un alias esta en la traduccion")
                if cat in IMPERATIVAS and t.endswith("?"):
                    errores.append(f"{donde}: el imperativo quedo como pregunta")
                if cat not in IMPERATIVAS and not t.endswith("?"):
                    errores.append(f"{donde}: pregunta sin '?'")

    todas = pd.concat(cats.values(), ignore_index=True) if cats else pd.DataFrame()
    if len(todas):
        for p, n in collections.Counter(norm(x) for x in todas["prompt"]).items():
            if n > 1:
                errores.append(f"prompt repetido {n} veces: {p!r}")
        no_num = todas[~todas["answer"].str.fullmatch(r"[\d.,\s]+(million|billion|BC)?")]
        for a, n in collections.Counter(norm(x) for x in no_num["answer"]).items():
            if n > 1:
                quien = todas[todas["answer"].map(norm) == a]["categoria"].tolist()
                avisos.append(f"respuesta repetida {n} veces: {a!r} ({', '.join(quien)})")

    # --- resumen -------------------------------------------------------------
    print(f"{'categoria':<24}{'n':>5}{'tok media':>11}{'min':>5}{'max':>5}   aperturas mas comunes")
    for cat, df in cats.items():
        ap_ = collections.Counter(" ".join(p.split()[:2]).lower() for p in df["prompt"]).most_common(4)
        print(f"{cat:<24}{len(df):>5}{df['n_tokens'].mean():>11.1f}{df['n_tokens'].min():>5}"
              f"{df['n_tokens'].max():>5}   {ap_}")
    if len(todas):
        print(f"{'TOTAL':<24}{len(todas):>5}{todas['n_tokens'].mean():>11.1f}")
        print("histograma de tokens:", dict(sorted(collections.Counter(todas["n_tokens"]).items())))

    for a in avisos:
        print("AVISO ", a)
    for e in errores:
        print("ERROR ", e)
    print(f"\n{len(errores)} errores, {len(avisos)} avisos")
    if errores:
        sys.exit(1)

    # --- intercalado ---------------------------------------------------------
    orden = [cat for cat, _ in CATEGORIAS]
    filas = [cats[c].iloc[i] for i in range(N_POR_CATEGORIA) for c in orden]
    out = pd.DataFrame(filas)[["prompt", "answer", "aliases", "categoria", "n_tokens", *COLS_TRAD]]
    if args.dry:
        print("--dry: no se escribe el intercalado")
        return
    path = os.path.join(args.dir, SALIDA)
    out.to_csv(path, sep=";", index=False)
    print(f"escrito {path} ({len(out)} filas, round-robin {' -> '.join(orden)})")


if __name__ == "__main__":
    main()
