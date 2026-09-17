"""
Targets de teacher forcing para UNA celda de {fr, es, de} x {normal, MAYUSCULAS}.

    y_i = M([INSTRUCCION_de_la_celda ; q_i])

Mismo diseno que generate_targets.py / generate_targets_upper.py, con una
diferencia que aca es lo que importa: NO parte de data/questions.csv sino de un
targets CSV que ya existe (--base_csv). De ahi se copian tal cual `prompt`,
`answer`, `aliases`, `baseline_en` y todas las columnas `prompt_<lang>` /
`prompt_<lang>_ok`, y solo se regenera `output` (mas las columnas del gate).

Por que: el algebra de direcciones (algebra_patches.py) compara parches
entrenados por separado sobre LAS MISMAS preguntas y evalua sobre EL MISMO
held-out. El split es posicional (int(len * 0.80)), asi que las seis celdas
tienen que tener las mismas filas en el mismo orden; derivarlas de un unico CSV
base lo garantiza por construccion. Ademas hereda las traducciones ya
corregidas a mano (fix_translations.py) y ahorra la generacion del baseline.

La celda `fr` no pasa por aca: usa attributes/french/targets_french_v5.csv.

Gate: la respuesta (a) no esta POSITIVAMENTE en otro idioma (mismo criterio
relajado que generate_targets.py: un "18 x 5 = 90" sin palabras no se tira) y
(b) si la celda es _up, esta en mayusculas; si es normal, NO lo esta. La
accuracy se mide y se guarda pero por defecto NO filtra: los alias del banco son
ingles + frances, asi que "Atenas" o "Athen" darian falso negativo, y los
simbolos quimicos fallan sobre texto en mayusculas (ver el docstring de
generate_targets_upper.py). El loss solo mira los primeros 8 tokens del target,
que es donde vive la decision de idioma y formato. --gate_accuracy lo activa.

    (desde experimentos/idiomas)
    python3 -u algebra/generate_targets_attr.py --model $M --lang es --upper \\
        --base_csv attributes/french/targets_french_v5.csv \\
        --out algebra/targets/targets_es_up.csv
"""

import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pandas as pd
import tqdm

from checkers import (LANGS, answer_correct, is_uppercase, lang_score, language_verdict,
                      truncate_at_role_leak, uppercase_score)
from generate_targets import build_reference_prompt
from lm import DEFAULT_MODEL, generate_one, load_model_and_tokenizer

NOMBRE = {"fr": "French", "es": "Spanish", "de": "German"}


def instruction_for(lang, upper):
    """Misma forma que INSTRUCTION_FR (generate_targets.py) e INSTRUCTION_JOINT
    (compose_patches.py), con el idioma como parametro."""
    if upper:
        return f"Respond entirely in uppercase letters, in {NOMBRE[lang]}."
    return f"Answer in {NOMBRE[lang]}."


# columnas del gate de OTRA celda que no tienen sentido en el CSV nuevo
_DESCARTAR = {"ref_french_score", "ref_is_french", "baseline_is_french", "output_hand_fixed",
              "ref_uppercase_score", "ref_is_uppercase", "baseline_is_uppercase"}


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--model", default=DEFAULT_MODEL)
    ap.add_argument("--base_csv", required=True,
                    help="targets CSV existente del que se heredan filas, orden y traducciones")
    ap.add_argument("--out", required=True)
    ap.add_argument("--lang", choices=list(NOMBRE), required=True)
    ap.add_argument("--upper", action="store_true")
    ap.add_argument("--instruction", default=None, help="pisa la instruccion de la celda")
    ap.add_argument("--gate_accuracy", action="store_true",
                    help="exigir ademas answer_correct (ver docstring: subestima en es/de/mayusculas)")
    ap.add_argument("--n", type=int, default=0, help="limitar filas (humo). Rompe el split: no entrenar con eso")
    ap.add_argument("--num_tokens", type=int, default=100)
    ap.add_argument("--temperature", type=float, default=0.0)
    ap.add_argument("--device", default="cuda:0")
    args = ap.parse_args()

    base = pd.read_csv(args.base_csv, sep=";", keep_default_na=False, dtype=str)
    if args.n > 0:
        base = base.head(args.n)
    instr = args.instruction or instruction_for(args.lang, args.upper)
    celda = args.lang + ("_up" if args.upper else "")
    otros = [l for l in LANGS if l != args.lang]

    print(f"Celda: {celda}  |  base: {args.base_csv} ({len(base)} filas)")
    print(f"Instruccion: {instr!r}")
    print("=" * 70)

    model, tokenizer = load_model_and_tokenizer(args.model, device=args.device)

    out = base.drop(columns=[c for c in base.columns if c in _DESCARTAR]).copy()
    nuevas = {k: [] for k in ("output", "ref_role_leak", "ref_language", "ref_target_score",
                              "ref_uppercase_score", "ref_attr_ok", "ref_answer_correct",
                              "passed_gate")}
    for _, r in tqdm.tqdm(base.iterrows(), total=len(base), desc=f"targets {celda}"):
        q, ans, al = r["prompt"], r["answer"], r["aliases"]
        ref_raw = generate_one(model, tokenizer, build_reference_prompt(instr, q), args.device,
                               args.num_tokens, args.temperature, clean=False)
        ref = truncate_at_role_leak(ref_raw)
        has_answer = str(ans).strip() != ""
        lang_ok = language_verdict(ref) not in otros
        fmt_ok = is_uppercase(ref) == args.upper
        acc_ok = answer_correct(ref, ans, al) if has_answer else None
        gate = lang_ok and fmt_ok and (acc_ok is not False or not args.gate_accuracy)
        nuevas["output"].append(ref)
        nuevas["ref_role_leak"].append(bool(ref != ref_raw.strip()))
        nuevas["ref_language"].append(language_verdict(ref))
        nuevas["ref_target_score"].append(round(lang_score(ref, args.lang), 4))
        nuevas["ref_uppercase_score"].append(round(uppercase_score(ref), 4))
        nuevas["ref_attr_ok"].append(bool(lang_ok and fmt_ok))
        nuevas["ref_answer_correct"].append("" if acc_ok is None else bool(acc_ok))
        nuevas["passed_gate"].append(bool(gate))
    for k, v in nuevas.items():
        out[k] = v
    out["target_cell"] = celda
    out["instruction"] = instr

    # mismas primeras columnas que targets_french_v5.csv, el resto como venia
    primero = ["prompt", "output", "answer", "aliases", "baseline_en"]
    out = out[primero + [c for c in out.columns if c not in primero]]
    os.makedirs(os.path.dirname(os.path.abspath(args.out)), exist_ok=True)
    out.to_csv(args.out, sep=";", index=False)

    n = len(out)
    corte = int(0.8 * n)
    acc = [a for a in nuevas["ref_answer_correct"] if a != ""]
    print("\n" + "=" * 70)
    print(f"REFERENCIA NATURAL  M([{celda} ; q])")
    print(f"  veredictos de idioma       : {out['ref_language'].value_counts().to_dict()}")
    print(f"  en mayusculas              : {sum(uppercase_score(o) >= 0.9 for o in out['output'])}/{n}"
          f"   (la celda pide {'SI' if args.upper else 'NO'})")
    print(f"  celda ok (idioma y formato): {sum(nuevas['ref_attr_ok'])}/{n}")
    if acc:
        print(f"  respuesta correcta         : {sum(acc)}/{len(acc)}"
              "   (subestimada: alias en/fr, simbolos en mayusculas)")
    print(f"  pasan el gate              : {sum(nuevas['passed_gate'])}/{n}"
          f"   (train, primeros 80%: {sum(nuevas['passed_gate'][:corte])}/{corte})")
    print(f"  quisieron seguir de turno  : {sum(nuevas['ref_role_leak'])}/{n}")
    malas = out[[not g for g in nuevas["passed_gate"]]]
    if len(malas):
        print("\nFilas que NO pasan el gate:")
        for i, r in malas.iterrows():
            print(f"  [{i}] {r['prompt'][:50]:<50} -> [{r['ref_language']}] {r['output'][:70]!r}")
    sin_acc = out[[a is False for a in nuevas["ref_answer_correct"]]]
    if len(sin_acc) and not args.gate_accuracy:
        print(f"\nFilas con answer_correct=False que SI entran a train ({len(sin_acc)}); mirarlas a ojo,")
        print("casi todas son nombres traducidos o simbolos en mayusculas, no respuestas malas:")
        for i, r in sin_acc.head(40).iterrows():
            print(f"  [{i}] answer={r['answer']!r:<22} -> {r['output'][:80]!r}")
    if sum(nuevas["passed_gate"][:corte]) < 50 and args.n == 0:
        print("\n  AVISO: menos de 50 targets limpios en train. Revisa la instruccion antes de entrenar.")
    print(f"\nGuardado en '{os.path.abspath(args.out)}'")


if __name__ == "__main__":
    main()
