"""
Dos experimentos de SIGNO y de IDIOMA DE ENTRADA sobre el parche v4_250, en el
tail del held-out (las filas posteriores al split 0.80: idx 200..249).

Cada condicion es (columna de prompt, escala a) y genera M(q_col + a*v). Con
a=0 es la referencia sin parche de esa columna; contra ella se mide "cambio"
(salida distinta) y a QUE idioma fue.

---------------------------------------------------------------------------
--preset restar   (experimento 1: q_en - a*v)
---------------------------------------------------------------------------
    prompt     a = 0, -1, -2      pregunta en ingles, parche restado
    prompt_fr  a = 0, -1, -2      la MISMA pregunta en frances, parche restado

La pregunta en ingles ya se contesta en ingles, asi que en la salida greedy
"cambiar a ingles" no puede verse; lo que se mide ahi es si -v es una
direccion con sentido y no ruido: la CE del target frances (ce_fr_head) tiene
que SUBIR respecto de a=0 y la del baseline ingles (ce_en_head) bajar o
quedarse. El cambio de idioma visible se mide sobre prompt_fr: el modelo la
contesta en frances SIN parche (empareja el idioma de la entrada) y, si -v
cancela el frances, con a<0 tiene que pasar a ingles.

---------------------------------------------------------------------------
--preset romance  (transferencia: q_it + a*v, q_pt + a*v)
---------------------------------------------------------------------------
    prompt_it  a = 0, 1           pregunta en italiano, parche sumado
    prompt_pt  a = 0, 1           pregunta en portugues, parche sumado

Idiomas que no estuvieron en el entrenamiento de los runs multi (en/es/de):
si el parche da frances desde italiano y portugues, lo que aprendio no es
"desde estos tres idiomas" sino algo mas general. checkers.py tiene canales
it/pt para que la salida sin parche no cuente como francesa.

---------------------------------------------------------------------------
--preset idioma   (experimento 2: q_es + a*v)
---------------------------------------------------------------------------
    prompt_es  a = 0, 1           pregunta en espanol, parche sumado
    prompt_de  a = 0, 1           control: la misma pregunta en aleman
    prompt     a = 0, 1           referencia: el eval de siempre, en el mismo run

Sin parche el modelo contesta en el idioma de la pregunta. Si el parche impone
frances sobre cualquier entrada, con a=1 contesta en frances tambien desde
espanol y aleman; si solo funciona desde ingles, no. prompt_es lo agrega
`translate_questions.py --lang es`; prompt_fr y prompt_de ya estan en el CSV.

---------------------------------------------------------------------------
QUE SE MIDE POR CONDICION
---------------------------------------------------------------------------
    veredictos      distribucion fr / en / es / de / unknown (language_verdict)
    is_french       compliance, mismo detector que eval_lang_patch.py
    cambio          fraccion de filas cuya salida difiere de la de a=0
    ce_fr_head      CE (teacher forcing, primeros head_k tokens) del target
                    frances `output`, con el prompt de la columna + a*v
    ce_en_head      idem para el baseline ingles `baseline_en`
    answer_correct  accuracy. OJO: los alias del CSV son ingles + frances; una
                    respuesta correcta en espanol o aleman con el nombre
                    traducido (Damasco, Kiew) cuenta como incorrecta. Mirar
                    los textos antes de leer la accuracy en esas columnas.

    python3 -u cross_lang_patch.py --model $M --preset restar --out_dir runs/cross_lang_v4
    python3 -u cross_lang_patch.py --model $M --preset idioma --out_dir runs/cross_lang_v4
    python3 -u cross_lang_patch.py --model $M --conds "prompt_fr:0,prompt_fr:-0.5,prompt_fr:-1" ...
"""

import argparse
import json
import os

import pandas as pd
import torch
import tqdm

from attn_utils import add_metrics, aggregate
from checkers import truncate_at_role_leak
from lm import (DEFAULT_MODEL, PATCH_ANCHORS, generate_one, load_model_and_tokenizer,
                nll_of_target)

PRESETS = {
    "restar": "prompt:0,prompt:-1,prompt:-2,prompt_fr:0,prompt_fr:-1,prompt_fr:-2",
    "idioma": "prompt_es:0,prompt_es:1,prompt_de:0,prompt_de:1,prompt:0,prompt:1",
    # transferencia a idiomas que NO estuvieron en el entrenamiento multi
    # (v5_*_multi entreno con en/es/de): italiano y portugues, escritos a mano
    # en el CSV para las 50 filas del tail (prompt_it, prompt_pt).
    "romance": "prompt_it:0,prompt_it:1,prompt_pt:0,prompt_pt:1",
}
LANGS = ("fr", "en", "es", "de", "it", "pt", "unknown")


def parse_conds(spec):
    """'prompt:0,prompt_fr:-1' -> [(col, escala)], sin duplicados, a=0 primero por columna."""
    out, seen = [], set()
    for parte in spec.split(","):
        parte = parte.strip()
        if not parte:
            continue
        col, a = parte.rsplit(":", 1)
        key = (col.strip(), float(a))
        if key not in seen:
            seen.add(key)
            out.append(key)
    cols = []
    for col, _ in out:
        if col not in cols:
            cols.append(col)
    # cada columna necesita su a=0 como referencia de "cambio"
    for col in cols:
        if (col, 0.0) not in seen:
            out.append((col, 0.0))
    return sorted(out, key=lambda ca: (cols.index(ca[0]), ca[1] != 0.0, abs(ca[1])))


def fmt_a(a):
    return f"{a:g}"


def label(col, a):
    return f"{col} a={fmt_a(a)}"


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--patch", default="runs/v4_250/lang_patch_best_train.pt")
    ap.add_argument("--model", default=DEFAULT_MODEL)
    ap.add_argument("--targets", default="attributes/french/targets_french.csv")
    ap.add_argument("--train_test_split", type=float, default=0.80)
    ap.add_argument("--preset", choices=list(PRESETS), default=None)
    ap.add_argument("--conds", default=None,
                    help="grilla explicita 'col:a,col:a,...' (pisa --preset)")
    ap.add_argument("--num_patch_positions", type=int, default=3)
    ap.add_argument("--patch_offset", type=int, default=0)
    ap.add_argument("--patch_anchor", choices=list(PATCH_ANCHORS), default="goal")
    ap.add_argument("--num_tokens", type=int, default=100)
    ap.add_argument("--head_k", type=int, default=5)
    ap.add_argument("--n", type=int, default=0, help="limitar filas (0 = todo el tail)")
    ap.add_argument("--keep_bad_translations", action="store_true",
                    help="no excluir las filas con prompt_<lang>_ok = False")
    ap.add_argument("--device", default="cuda:0")
    ap.add_argument("--out_dir", required=True)
    args = ap.parse_args()

    if args.conds is None and args.preset is None:
        raise SystemExit("hace falta --preset restar|idioma o --conds")
    conds = parse_conds(args.conds if args.conds is not None else PRESETS[args.preset])
    name = args.preset if args.conds is None else "custom"

    df = pd.read_csv(args.targets, sep=";", keep_default_na=False)
    heldout = df.iloc[int(len(df) * args.train_test_split):]
    if args.n > 0:
        heldout = heldout.head(args.n)

    cols = []
    for col, _ in conds:
        if col not in cols:
            cols.append(col)
    faltan = [c for c in cols if c not in df.columns]
    if faltan:
        raise SystemExit(f"columnas ausentes en {args.targets}: {faltan}. "
                         f"Para prompt_es: python3 translate_questions.py --model $M --lang es")

    # filas utilizables por columna: la traduccion tiene que haber pasado el gate
    usable = {}
    for col in cols:
        okcol = f"{col}_ok"
        if okcol in df.columns and not args.keep_bad_translations:
            ok = heldout[okcol].astype(str).str.lower() == "true"
            usable[col] = set(int(i) for i in heldout.index[ok])
            if (~ok).sum():
                print(f"{col}: {int((~ok).sum())}/{len(heldout)} filas excluidas por {okcol}=False")
        else:
            usable[col] = set(int(i) for i in heldout.index)

    patch = torch.load(args.patch, map_location=args.device).to(args.device)
    model, tokenizer = load_model_and_tokenizer(args.model, device=args.device)
    os.makedirs(args.out_dir, exist_ok=True)

    print(f"parche {args.patch}  norma {patch.norm(2).item():.4f}  |  tail held-out {len(heldout)} "
          f"(idx {int(heldout.index[0])}..{int(heldout.index[-1])})")
    print(f"preset={name}  condiciones={[label(c, a) for c, a in conds]}")

    ref_text = {}          # (col, idx) -> salida con a=0
    resultados = []        # una entrada por condicion
    for col, a in conds:
        p = None if a == 0.0 else patch * a
        rows = []
        for i, r in tqdm.tqdm(heldout.iterrows(), total=len(heldout), desc=label(col, a)):
            i = int(i)
            if i not in usable[col]:
                continue
            q = str(r[col])
            raw = generate_one(model, tokenizer, q, args.device, args.num_tokens, 0.0,
                               patch=p, num_patch_positions=args.num_patch_positions,
                               clean=False, patch_offset=args.patch_offset,
                               patch_anchor=args.patch_anchor)
            txt = truncate_at_role_leak(raw)
            if a == 0.0:
                ref_text[(col, i)] = txt
            rec = {"idx": i, "col": col, "escala": a, "prompt_en": r["prompt"], "prompt_usado": q,
                   "answer": r["answer"], "baseline_en": r["baseline_en"],
                   "reference_fr": r["output"], "out": txt,
                   "out_role_leak": bool(txt != raw.strip()),
                   "out_igual_a0": txt.strip() == ref_text.get((col, i), "").strip()}
            add_metrics(rec, "out", txt, r["answer"], r["aliases"])
            ce_fr = nll_of_target(model, tokenizer, q, r["output"], args.device, patch=p,
                                  num_patch_positions=args.num_patch_positions,
                                  head_k=args.head_k, patch_offset=args.patch_offset,
                                  patch_anchor=args.patch_anchor)
            ce_en = nll_of_target(model, tokenizer, q, r["baseline_en"], args.device, patch=p,
                                  num_patch_positions=args.num_patch_positions,
                                  head_k=args.head_k, patch_offset=args.patch_offset,
                                  patch_anchor=args.patch_anchor)
            rec["ce_fr"] = ce_fr
            rec["ce_en"] = ce_en
            rows.append(rec)

        agg = aggregate(rows, "out")
        n = max(1, len(rows))
        ver = agg["veredictos"]
        for lg in LANGS:
            agg[f"p_{lg}"] = ver.get(lg, 0) / n
        agg["cambio_vs_a0"] = (float("nan") if a == 0.0
                               else sum(not r["out_igual_a0"] for r in rows) / n)
        agg["role_leak"] = sum(r["out_role_leak"] for r in rows) / n

        def avg(key, part):
            v = [r[key][part] for r in rows if r[key][part] == r[key][part]]
            return sum(v) / len(v) if v else float("nan")

        agg["ce_fr_head"] = avg("ce_fr", "head")
        agg["ce_fr_all"] = avg("ce_fr", "all")
        agg["ce_en_head"] = avg("ce_en", "head")
        agg["ce_en_all"] = avg("ce_en", "all")
        resultados.append({"col": col, "escala": a, "label": label(col, a),
                           "metrics": agg, "rows": rows})

    # --- tabla ---------------------------------------------------------------
    print("\n" + "=" * 140)
    print(f"{'condicion':<20}{'n':>4}{'fr':>6}{'en':>6}{'es':>6}{'de':>6}{'it':>6}{'pt':>6}{'unk':>5}"
          f"{'is_fr':>7}{'st_fr':>7}{'acc':>6}{'cambio':>8}{'largo':>7}"
          f"{'ce_fr_h':>9}{'ce_en_h':>9}{'leak':>6}")
    print("-" * 140)
    for res in resultados:
        m = res["metrics"]
        print(f"{res['label']:<20}{m['n']:>4}{m['p_fr']:>6.2f}{m['p_en']:>6.2f}{m['p_es']:>6.2f}"
              f"{m['p_de']:>6.2f}{m['p_it']:>6.2f}{m['p_pt']:>6.2f}{m['p_unknown']:>5.2f}{m['is_french']:>7.2f}{m['starts_fr']:>7.2f}"
              f"{m['answer_correct']:>6.2f}{m['cambio_vs_a0']:>8.2f}{m['len_media']:>7.1f}"
              f"{m['ce_fr_head']:>9.3f}{m['ce_en_head']:>9.3f}{m['role_leak']:>6.2f}")
    print("=" * 140)
    print("fr/en/es/de/it/pt/unk: fraccion de salidas por idioma (language_verdict). cambio: salida != a=0.")
    print("ce_*_h: CE del head del target frances / del baseline ingles bajo esa condicion.")
    if name == "restar":
        print("Lectura: en 'prompt' -v no puede cambiar la salida a ingles (ya lo es); mirar que ce_fr_h")
        print("suba. En 'prompt_fr', si -v cancela el frances, en baja y fr sube con a<0.")
    elif name == "romance":
        print("Lectura: it/pt no estuvieron en el entrenamiento. Si fr sube con a=1 desde las dos, la")
        print("transferencia es a idiomas no vistos; comparar con es/de del preset idioma (mismo parche).")
    elif name == "idioma":
        print("Lectura: si fr sube desde prompt_es/prompt_de con a=1, el parche impone frances sobre")
        print("cualquier idioma de entrada; si solo sube desde 'prompt', depende de partir de ingles.")

    # --- archivos ------------------------------------------------------------
    rep = {"objetivo": "signo del parche e idioma de la pregunta de entrada",
           "preset": name, "patch": os.path.abspath(args.patch),
           "patch_norm": patch.norm(2).item(), "config": vars(args),
           "n_tail": len(heldout), "condiciones": resultados}
    jp = os.path.join(args.out_dir, f"cross_lang_{name}.json")
    with open(jp, "w", encoding="utf-8") as f:
        json.dump(rep, f, indent=2, ensure_ascii=False)
    write_markdown(rep, os.path.join(args.out_dir, f"cross_lang_{name}.md"))
    print(f"\nGuardado: {jp}")


def _t(s, n=110):
    s = str(s).replace("\n", " / ").replace("|", "\\|")
    return s if len(s) <= n else s[:n] + "..."


def write_markdown(rep, path):
    L = [f"# Parche de idioma: signo e idioma de entrada (preset `{rep['preset']}`)", ""]
    L.append(f"- Parche: `{rep['patch']}`  |  norma {rep['patch_norm']:.4f}")
    L.append(f"- Tail del held-out: n={rep['n_tail']}")
    L.append("")
    L.append("| condicion | n | fr | en | es | de | it | pt | unk | is_french | starts_fr | acc | cambio vs a=0 | largo | CE fr head | CE en head |")
    L.append("|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|")
    for res in rep["condiciones"]:
        m = res["metrics"]
        L.append(f"| {res['label']} | {m['n']} | {m['p_fr']:.2f} | {m['p_en']:.2f} | {m['p_es']:.2f} "
                 f"| {m['p_de']:.2f} | {m['p_it']:.2f} | {m['p_pt']:.2f} | {m['p_unknown']:.2f} | {m['is_french']:.2f} | {m['starts_fr']:.2f} "
                 f"| {m['answer_correct']:.2f} | {m['cambio_vs_a0']:.2f} | {m['len_media']:.1f} "
                 f"| {m['ce_fr_head']:.3f} | {m['ce_en_head']:.3f} |")
    L.append("")
    L.append("`cambio` es la fraccion de filas cuya salida difiere de la de a=0 en la misma columna. "
             "La accuracy en salidas en espanol o aleman puede estar subestimada: los alias son "
             "ingles y frances.")
    L.append("")
    # salidas por columna: una tabla con una col por escala
    cols = []
    for res in rep["condiciones"]:
        if res["col"] not in cols:
            cols.append(res["col"])
    for col in cols:
        conds = [res for res in rep["condiciones"] if res["col"] == col]
        L.append(f"## Salidas: `{col}`")
        L.append("")
        L.append("| # | pregunta usada | " + " | ".join(f"a={fmt_a(res['escala'])} [lang]" for res in conds) + " |")
        L.append("|---|---|" + "---|" * len(conds))
        by_idx = {res["escala"]: {r["idx"]: r for r in res["rows"]} for res in conds}
        idxs = sorted(by_idx[conds[0]["escala"]])
        for i in idxs:
            q = by_idx[conds[0]["escala"]][i]["prompt_usado"]
            celdas = []
            for res in conds:
                r = by_idx[res["escala"]].get(i)
                celdas.append("" if r is None else f"{_t(r['out'])} [{r['out_lang']}]")
            L.append(f"| {i} | {_t(q, 60)} | " + " | ".join(celdas) + " |")
        L.append("")
    open(path, "w", encoding="utf-8").write("\n".join(L) + "\n")


if __name__ == "__main__":
    main()
