"""
¿El parche goal_all es una PROPIEDAD DE LA ENTRADA o una DIRECTIVA sobre la salida?

Dos lecturas de por que `q_en + v_fr` se contesta en frances:

    entrada     v falsifica el rasgo "en que idioma esta escrita la pregunta" y
                el frances lo pone la politica que el modelo ya tiene (contestar
                en el idioma de la pregunta). El vector no lleva ninguna orden.
    directiva   v actua sobre la decision de idioma de la SALIDA, como lo haria
                "Answer this in French.".

Las metricas de siempre no las separan: las dos predicen frances. Aca el parche
se suma SOLO sobre el tramo de la pregunta dentro de un mensaje mas largo, y el
resto del mensaje pregunta o manda otra cosa.

---------------------------------------------------------------------------
--preset idioma_entrada     (test 1: preguntarle al modelo)
---------------------------------------------------------------------------
    "What language is the following question written in? ...\n\n{q}"

    lang_id : prompt    : -    : 0     referencia, tiene que decir English
    lang_id : prompt    : fr   : 1     EL TEST. "French" => rasgo de entrada falsificado
    lang_id : prompt    : es   : 1     especificidad: tiene que decir Spanish, no French
    lang_id : prompt    : rand0: 1     azar de la misma norma: tiene que seguir en English
    lang_id : prompt_fr : -    : 0     techo: una pregunta francesa de verdad
    (+ lang_id_b, segunda redaccion, para que no dependa de una frase)

    Se lee `dice_<idioma>`: el primer nombre de idioma que menciona la salida,
    en cualquier idioma (la salida misma puede venir en frances: "Français").

---------------------------------------------------------------------------
--preset resta_directiva    (test 2: restar v_fr contra una instruccion)
---------------------------------------------------------------------------
    "Answer this in French. {q_en}"  con  -v_fr  solo sobre q_en

    instr_fr : prompt    : -    : 0    referencia [FR;q], ~0.98 de frances
    instr_fr : prompt    : fr   : -1   EL TEST
    instr_fr : prompt    : es   : -1   control: mismo componente comun, otro idioma
    instr_fr : prompt    : rand0: -1   control: azar de la misma norma
    plain    : prompt_fr : -    : 0    \\ la resta que YA funciona (0.90 -> 0.12),
    plain    : prompt_fr : fr   : -1   /  en la misma corrida, como vara

    entrada    => la pregunta ya es inglesa, no hay frances de ENTRADA que sacar:
                  la instruccion sigue mandando y el frances se queda cerca de la
                  referencia (menos el dano generico que muestran es / rand0).
    directiva  => -v_fr cancela la instruccion y el frances cae como en prompt_fr.

---------------------------------------------------------------------------
--preset conflicto          (test 2b: instruccion en contra)
---------------------------------------------------------------------------
    instr_en : prompt_fr : -  : 0      pregunta francesa REAL + "Answer this in English."
    instr_en : prompt    : fr : 1      pregunta inglesa + v_fr + la misma instruccion
    instr_en : prompt    : -  : 0      referencia
    plain    : prompt    : fr : 1      el parche sin instruccion (el eval de siempre)

    Si v_fr es una propiedad de la entrada, tiene que perder contra la
    instruccion en la MISMA medida en que pierde una pregunta francesa de
    verdad. Si resiste mas que la pregunta real, es mas que un rasgo de entrada.

---------------------------------------------------------------------------
EL TRAMO DE LA PREGUNTA
---------------------------------------------------------------------------
El goal slice del SuffixManager es el mensaje entero, asi que lm.apply_patch no
sirve: caeria tambien sobre la instruccion. El tramo se ubica tokenizando el
mensaje por partes (pre, pre+q, pre+q+post), igual que SuffixManager ubica sus
slices, y se VERIFICA que los ids sean estables: si la tokenizacion de `pre`
sola no es prefijo de la del mensaje completo (p.ej. ".\\n\\n" o " What" son un
solo token), aborta en vez de parchear posiciones corridas. Un espacio final de
`pre` pasa al tramo: "French. {q}" parchea " What", no "What".

`--dry` no carga el modelo: imprime los tramos de las primeras filas y sale.
Correrlo primero.

    python3 -u entrada_o_directiva.py --model $M --dry --preset idioma_entrada \\
        --patch fr=algebra/runs/alg_fr/lang_patch_best_train.pt --out_dir /tmp/x
"""

import argparse
import json
import os
import re
import unicodedata

PLANTILLAS = {
    # nombre: (texto con {q}, max tokens a generar, medir CE de los targets)
    "plain": ("{q}", 100, True),
    "instr_fr": ("Answer this in French. {q}", 100, True),
    "instr_en": ("Answer this in English. {q}", 100, True),
    "lang_id": ("What language is the following question written in? "
                "Reply with only the name of the language.\n\n{q}", 40, False),
    "lang_id_b": ("Do not answer the question below. Only tell me which language "
                  "it is written in, in one word.\n\n{q}", 40, False),
}

PRESETS = {
    "idioma_entrada": ("lang_id:prompt:-:0,lang_id:prompt:fr:1,lang_id:prompt:es:1,"
                       "lang_id:prompt:rand0:1,lang_id:prompt_fr:-:0,lang_id:prompt_es:-:0,"
                       "lang_id_b:prompt:-:0,lang_id_b:prompt:fr:1,lang_id_b:prompt:es:1,"
                       "lang_id_b:prompt_fr:-:0"),
    "resta_directiva": ("instr_fr:prompt:-:0,instr_fr:prompt:fr:-1,instr_fr:prompt:es:-1,"
                        "instr_fr:prompt:rand0:-1,plain:prompt_fr:-:0,plain:prompt_fr:fr:-1"),
    "conflicto": ("instr_en:prompt_fr:-:0,instr_en:prompt:-:0,instr_en:prompt:fr:1,"
                  "plain:prompt:fr:1"),
}

LANGS = ("fr", "en", "es", "de", "it", "pt", "unknown")

# nombres de idioma, ya sin acentos y en minuscula, en los idiomas en que puede
# venir la salida (el parche puede hacer que conteste "Français" o "Francés")
NOMBRES = {
    "en": ("english", "anglais", "anglaise", "ingles", "englisch", "inglese"),
    "fr": ("french", "francais", "francaise", "frances", "franzosisch", "francese"),
    "es": ("spanish", "espagnol", "espagnole", "espanol", "castellano", "spanisch", "spagnolo"),
    "de": ("german", "allemand", "allemande", "aleman", "deutsch", "tedesco"),
    "it": ("italian", "italien", "italienne", "italiano", "italienisch"),
    "pt": ("portuguese", "portugais", "portugaise", "portugues", "portugiesisch", "portoghese"),
}
_RE_NOMBRE = re.compile(r"\b(" + "|".join(n for v in NOMBRES.values() for n in v) + r")\b")
_A_CODIGO = {n: c for c, v in NOMBRES.items() for n in v}


def _fold(s):
    s = unicodedata.normalize("NFKD", str(s))
    return "".join(ch for ch in s if not unicodedata.combining(ch)).lower()


def idioma_nombrado(text):
    """Codigo del PRIMER idioma que la salida nombra ('ninguno' si no nombra)."""
    m = _RE_NOMBRE.search(_fold(text))
    return _A_CODIGO[m.group(1)] if m else "ninguno"


def parse_conds(spec):
    """'plantilla:col:parche:a,...' -> [(plantilla, col, parche, a)]. parche '-' = sin parche."""
    out, seen = [], set()
    for parte in spec.split(","):
        parte = parte.strip()
        if not parte:
            continue
        campos = parte.split(":")
        if len(campos) != 4:
            raise SystemExit(f"condicion mal formada: '{parte}' (plantilla:col:parche:a)")
        tpl, col, pname, a = (c.strip() for c in campos)
        if tpl not in PLANTILLAS:
            raise SystemExit(f"plantilla desconocida: {tpl}; validas: {list(PLANTILLAS)}")
        a = float(a)
        if pname == "-" or a == 0.0:
            pname, a = "-", 0.0
        key = (tpl, col, pname, a)
        if key not in seen:
            seen.add(key)
            out.append(key)
    # cada (plantilla, col) necesita su referencia sin parche para medir "cambio"
    for tpl, col in dict.fromkeys((t, c) for t, c, _, _ in out):
        if (tpl, col, "-", 0.0) not in seen:
            seen.add((tpl, col, "-", 0.0))
            out.append((tpl, col, "-", 0.0))
    grupos = list(dict.fromkeys((t, c) for t, c, _, _ in out))
    return sorted(out, key=lambda k: (grupos.index((k[0], k[1])), k[2] != "-"))


def label(tpl, col, pname, a):
    return f"{tpl} | {col}" + ("" if pname == "-" else f" {a:+g}*{pname}")


def partir(tpl_text, q):
    """(pre, tramo, post): el espacio final de `pre` pasa al tramo (" What")."""
    pre, post = tpl_text.split("{q}")
    sin = pre.rstrip(" ")
    return sin, pre[len(sin):] + q, post


def tramo_pregunta(tokenizer, build_sm, pre, tramo, post, target=""):
    """
    (sm, ids, start, stop): el mensaje completo y las posiciones [start, stop)
    del tramo. Aborta si la tokenizacion por partes no es estable.
    """
    sm = build_sm(tokenizer, pre + tramo + post, target=target)
    ids = sm.get_input_ids()
    g = sm._goal_slice

    def fin_de(msg):
        s = build_sm(tokenizer, msg, target="")
        parte = s.get_input_ids()
        stop = s._goal_slice.stop
        return stop, parte[:stop]

    if pre:
        start, ids_pre = fin_de(pre)
    else:
        start, ids_pre = g.start, ids[:g.start]
    stop, ids_q = fin_de(pre + tramo)
    ok = (ids[:start].tolist() == ids_pre.tolist() and ids[:stop].tolist() == ids_q.tolist()
          and g.start <= start < stop <= g.stop and (post or stop == g.stop))
    if not ok:
        raise SystemExit(
            "tokenizacion inestable al ubicar el tramo de la pregunta:\n"
            f"  pre   = {pre!r}\n  tramo = {tramo!r}\n  post  = {post!r}\n"
            f"  goal {g.start}..{g.stop}  tramo {start}..{stop}\n"
            "cambiar el separador de la plantilla (que `pre` termine en salto de linea o en "
            "un espacio, y `post` no empiece con salto de linea pegado a un signo).")
    return sm, ids, start, stop


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--patch", action="append", default=[], metavar="NOMBRE=RUTA",
                    help="parche goal_all [1,1,d]; repetible. p.ej. fr=algebra/runs/alg_fr/...pt")
    ap.add_argument("--rand_like", default=None,
                    help="parche cuya norma copian los rand<seed> (default: el primero)")
    ap.add_argument("--model", default=None)
    ap.add_argument("--targets", default="attributes/french/targets_french_v5.csv")
    ap.add_argument("--train_test_split", type=float, default=0.80)
    ap.add_argument("--preset", choices=list(PRESETS), default=None)
    ap.add_argument("--conds", default=None,
                    help="grilla explicita 'plantilla:col:parche:a,...' (pisa --preset)")
    ap.add_argument("--head_k", type=int, default=5)
    ap.add_argument("--n", type=int, default=0, help="limitar filas (0 = todo el tail)")
    ap.add_argument("--keep_bad_translations", action="store_true")
    ap.add_argument("--dry", action="store_true",
                    help="solo tokenizer: imprime los tramos de 3 filas por condicion y sale")
    ap.add_argument("--tag", default=None)
    ap.add_argument("--device", default="cuda:0")
    ap.add_argument("--out_dir", required=True)
    args = ap.parse_args()

    if args.conds is None and args.preset is None:
        raise SystemExit(f"hace falta --preset {'|'.join(PRESETS)} o --conds")
    conds = parse_conds(args.conds if args.conds is not None else PRESETS[args.preset])
    name = args.tag or (args.preset if args.conds is None else "custom")

    import pandas as pd
    import torch
    import tqdm

    from attn_utils import add_metrics, aggregate
    from checkers import truncate_at_role_leak
    from lm import (DEFAULT_MODEL, build_suffix_manager, generate, get_embeddings,
                    load_model_and_tokenizer, stop_token_ids)

    model_path = args.model or DEFAULT_MODEL
    df = pd.read_csv(args.targets, sep=";", keep_default_na=False)
    heldout = df.iloc[int(len(df) * args.train_test_split):]
    if args.n > 0:
        heldout = heldout.head(args.n)

    cols = list(dict.fromkeys(c for _, c, _, _ in conds))
    faltan = [c for c in cols if c not in df.columns]
    if faltan:
        raise SystemExit(f"columnas ausentes en {args.targets}: {faltan}")
    usable = {}
    for col in cols:
        okcol = f"{col}_ok"
        if okcol in df.columns and not args.keep_bad_translations:
            ok = heldout[okcol].astype(str).str.lower() == "true"
            usable[col] = set(int(i) for i in heldout.index[ok])
        else:
            usable[col] = set(int(i) for i in heldout.index)

    # --- dry: solo el tokenizer ------------------------------------------------
    if args.dry:
        from transformers import AutoTokenizer
        tokenizer = AutoTokenizer.from_pretrained(model_path, trust_remote_code=True, use_fast=False)
        for tpl, col in dict.fromkeys((t, c) for t, c, _, _ in conds):
            print(f"\n=== {tpl} | {col}")
            for i, r in heldout.head(3).iterrows():
                pre, tramo, post = partir(PLANTILLAS[tpl][0], str(r[col]))
                _, ids, s, e = tramo_pregunta(tokenizer, build_suffix_manager, pre, tramo, post)
                toks = [tokenizer.decode([t]) for t in ids[s:e]]
                print(f"  [{int(i)}] {e - s:2d} tok  antes={tokenizer.decode(ids[max(0, s - 3):s])!r}  "
                      f"tramo={toks}  despues={tokenizer.decode(ids[e:e + 3])!r}")
        print("\ntramos OK. Sacar --dry para correr.")
        return

    # --- parches ----------------------------------------------------------------
    patches = {}
    for spec in args.patch:
        k, _, path = spec.partition("=")
        v = torch.load(path, map_location=args.device).to(args.device)
        if v.dim() != 3 or v.shape[1] != 1:
            raise SystemExit(f"{path}: se espera un parche goal_all [1,1,d], llego {tuple(v.shape)}")
        patches[k.strip()] = v
    pedidos = list(dict.fromkeys(p for _, _, p, _ in conds if p != "-"))
    if any(p.startswith("rand") for p in pedidos):
        ref = args.rand_like or (list(patches)[0] if patches else None)
        if ref not in patches:
            raise SystemExit("los rand<seed> copian la norma de un parche: pasar --patch y/o --rand_like")
        for p in pedidos:
            if p.startswith("rand") and p not in patches:
                g = torch.Generator(device="cpu").manual_seed(int(p[4:] or 0))
                r = torch.randn(patches[ref].shape, generator=g).to(args.device)
                patches[p] = (r / r.norm(2) * patches[ref].norm(2)).to(patches[ref].dtype)
    faltan = [p for p in pedidos if p not in patches]
    if faltan:
        raise SystemExit(f"parches sin --patch: {faltan}")

    model, tokenizer = load_model_and_tokenizer(model_path, device=args.device)
    stop_ids = stop_token_ids(tokenizer)
    os.makedirs(args.out_dir, exist_ok=True)
    for k, v in patches.items():
        print(f"parche {k:<8} norma {v.norm(2).item():.4f}")
    print(f"tail held-out {len(heldout)}  |  preset={name}")

    def embeds_de(tpl, q, pname, a, target=""):
        pre, tramo, post = partir(PLANTILLAS[tpl][0], q)
        sm, ids, s, e = tramo_pregunta(tokenizer, build_suffix_manager, pre, tramo, post, target)
        emb = get_embeddings(model, ids.to(args.device).unsqueeze(0)).detach().clone()
        if pname != "-":
            emb[:, s:e, :] = emb[:, s:e, :] + (a * patches[pname]).to(emb.dtype)
        return sm, emb, e - s

    @torch.no_grad()
    def ce_head(tpl, q, pname, a, target):
        sm, emb, _ = embeds_de(tpl, q, pname, a, target=target)
        ids = sm.get_input_ids().to(args.device)
        tgt, ls = ids[sm._target_slice], sm._loss_slice
        n = min(ls.stop - ls.start, len(tgt), args.head_k)
        if n <= 0:
            return float("nan")
        logits = model(inputs_embeds=emb).logits
        return torch.nn.functional.cross_entropy(logits[0, ls.start:ls.start + n, :], tgt[:n]).item()

    ref_text, resultados = {}, []
    for tpl, col, pname, a in conds:
        _, max_tok, con_ce = PLANTILLAS[tpl]
        rows = []
        for i, r in tqdm.tqdm(heldout.iterrows(), total=len(heldout), desc=label(tpl, col, pname, a)):
            i = int(i)
            if i not in usable[col]:
                continue
            q = str(r[col])
            sm, emb, n_tok = embeds_de(tpl, q, pname, a)
            emb = emb[:, : sm._assistant_role_slice.stop, :]
            raw = tokenizer.decode(generate(model, emb, max_tok, 0.0, stop_ids),
                                   skip_special_tokens=True)
            txt = truncate_at_role_leak(raw)
            if pname == "-":
                ref_text[(tpl, col, i)] = txt
            rec = {"idx": i, "plantilla": tpl, "col": col, "parche": pname, "escala": a,
                   "mensaje": PLANTILLAS[tpl][0].replace("{q}", q), "answer": r["answer"],
                   "out": txt, "n_patched": 0 if pname == "-" else n_tok,
                   "out_igual_ref": txt.strip() == ref_text.get((tpl, col, i), "").strip(),
                   "dice": idioma_nombrado(txt)}
            add_metrics(rec, "out", txt, r["answer"], r["aliases"])
            if con_ce:
                rec["ce_fr_head"] = ce_head(tpl, q, pname, a, r["output"])
                rec["ce_en_head"] = ce_head(tpl, q, pname, a, r["baseline_en"])
            rows.append(rec)

        agg = aggregate(rows, "out")
        n = max(1, len(rows))
        for lg in LANGS:
            agg[f"p_{lg}"] = agg["veredictos"].get(lg, 0) / n
        for lg in list(NOMBRES) + ["ninguno"]:
            agg[f"dice_{lg}"] = sum(r["dice"] == lg for r in rows) / n
        agg["cambio_vs_ref"] = (float("nan") if pname == "-"
                                else sum(not r["out_igual_ref"] for r in rows) / n)
        agg["n_patched_media"] = sum(r["n_patched"] for r in rows) / n
        for k in ("ce_fr_head", "ce_en_head"):
            v = [r[k] for r in rows if k in r and r[k] == r[k]]
            agg[k] = sum(v) / len(v) if v else float("nan")
        resultados.append({"plantilla": tpl, "col": col, "parche": pname, "escala": a,
                           "label": label(tpl, col, pname, a), "metrics": agg, "rows": rows})

    # --- tablas -------------------------------------------------------------------
    W = 34
    print("\n" + "=" * 132)
    print("IDIOMA DE LA SALIDA (language_verdict)")
    print(f"{'condicion':<{W}}{'n':>4}{'fr':>6}{'en':>6}{'es':>6}{'de':>6}{'unk':>6}{'acc':>6}"
          f"{'cambio':>8}{'largo':>7}{'ce_fr_h':>9}{'ce_en_h':>9}{'tok':>6}")
    print("-" * 132)
    for res in resultados:
        m = res["metrics"]
        print(f"{res['label']:<{W}}{m['n']:>4}{m['p_fr']:>6.2f}{m['p_en']:>6.2f}{m['p_es']:>6.2f}"
              f"{m['p_de']:>6.2f}{m['p_unknown']:>6.2f}{m['answer_correct']:>6.2f}"
              f"{m['cambio_vs_ref']:>8.2f}{m['len_media']:>7.1f}{m['ce_fr_head']:>9.3f}"
              f"{m['ce_en_head']:>9.3f}{m['n_patched_media']:>6.1f}")
    if any(r["plantilla"].startswith("lang_id") for r in resultados):
        print("\nIDIOMA QUE EL MODELO DICE QUE TIENE LA PREGUNTA (primer nombre de idioma en la salida)")
        print(f"{'condicion':<{W}}{'n':>4}{'en':>7}{'fr':>7}{'es':>7}{'de':>7}{'it':>7}{'pt':>7}{'ninguno':>9}")
        print("-" * 132)
        for res in resultados:
            if not res["plantilla"].startswith("lang_id"):
                continue
            m = res["metrics"]
            print(f"{res['label']:<{W}}{m['n']:>4}" + "".join(
                f"{m['dice_' + lg]:>7.2f}" for lg in ("en", "fr", "es", "de", "it", "pt"))
                + f"{m['dice_ninguno']:>9.2f}")
    print("=" * 132)
    print("tok: posiciones parcheadas (solo el tramo de la pregunta). cambio: salida != la de sin parche.")
    print("ce_*_h: CE de los primeros head_k tokens del target frances / del baseline ingles.")

    rep = {"objetivo": "propiedad de la entrada vs directiva sobre la salida (goal_all)",
           "preset": name, "patches": {k: float(v.norm(2).item()) for k, v in patches.items()},
           "plantillas": {k: v[0] for k, v in PLANTILLAS.items()},
           "config": vars(args), "n_tail": len(heldout), "condiciones": resultados}
    jp = os.path.join(args.out_dir, f"entrada_o_directiva_{name}.json")
    with open(jp, "w", encoding="utf-8") as f:
        json.dump(rep, f, indent=2, ensure_ascii=False)
    write_markdown(rep, os.path.join(args.out_dir, f"entrada_o_directiva_{name}.md"))
    print(f"\nGuardado: {jp}")


def _t(s, n=110):
    s = str(s).replace("\n", " / ").replace("|", "\\|")
    return s if len(s) <= n else s[:n] + "..."


def write_markdown(rep, path):
    L = [f"# Entrada o directiva (preset `{rep['preset']}`)", ""]
    L.append("Parches: " + ", ".join(f"`{k}` (norma {v:.3f})" for k, v in rep["patches"].items()))
    L.append(f"Tail del held-out: n={rep['n_tail']}. El parche cae SOLO sobre el tramo de la pregunta.")
    L.append("")
    L.append("| condicion | n | fr | en | es | de | unk | acc | cambio | largo | CE fr head | CE en head | tok |")
    L.append("|---|---|---|---|---|---|---|---|---|---|---|---|---|")
    for res in rep["condiciones"]:
        m = res["metrics"]
        L.append(f"| {res['label']} | {m['n']} | {m['p_fr']:.2f} | {m['p_en']:.2f} | {m['p_es']:.2f} "
                 f"| {m['p_de']:.2f} | {m['p_unknown']:.2f} | {m['answer_correct']:.2f} "
                 f"| {m['cambio_vs_ref']:.2f} | {m['len_media']:.1f} | {m['ce_fr_head']:.3f} "
                 f"| {m['ce_en_head']:.3f} | {m['n_patched_media']:.1f} |")
    L.append("")
    lid = [r for r in rep["condiciones"] if r["plantilla"].startswith("lang_id")]
    if lid:
        L.append("Idioma que el modelo DICE que tiene la pregunta (primer nombre de idioma en la salida):")
        L.append("")
        L.append("| condicion | n | en | fr | es | de | it | pt | ninguno |")
        L.append("|---|---|---|---|---|---|---|---|---|")
        for res in lid:
            m = res["metrics"]
            L.append(f"| {res['label']} | {m['n']} | " + " | ".join(
                f"{m['dice_' + lg]:.2f}" for lg in ("en", "fr", "es", "de", "it", "pt", "ninguno")) + " |")
        L.append("")
    grupos = list(dict.fromkeys((r["plantilla"], r["col"]) for r in rep["condiciones"]))
    for tpl, col in grupos:
        conds = [r for r in rep["condiciones"] if (r["plantilla"], r["col"]) == (tpl, col)]
        L.append(f"## `{tpl}` sobre `{col}`")
        L.append("")
        L.append(f"Mensaje: `{_t(rep['plantillas'][tpl], 200)}`")
        L.append("")
        L.append("| # | pregunta | " + " | ".join(
            ("sin parche" if r["parche"] == "-" else f"{r['escala']:+g}*{r['parche']}") + " [lang / dice]"
            for r in conds) + " |")
        L.append("|---|---|" + "---|" * len(conds))
        by = [{x["idx"]: x for x in r["rows"]} for r in conds]
        for i in sorted(by[0]):
            q = by[0][i]["mensaje"].split("\n")[-1]
            celdas = []
            for b in by:
                x = b.get(i)
                celdas.append("" if x is None else f"{_t(x['out'])} [{x['out_lang']} / {x['dice']}]")
            L.append(f"| {i} | {_t(q, 60)} | " + " | ".join(celdas) + " |")
        L.append("")
    open(path, "w", encoding="utf-8").write("\n".join(L) + "\n")


if __name__ == "__main__":
    main()
