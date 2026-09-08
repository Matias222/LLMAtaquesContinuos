"""
Paso 0: generar los targets de teacher forcing.

    y_i = M([INSTRUCCION ; q_i])

El modelo se genera sus propios targets. No hay CSV curado a mano, y la
condicion "instruccion en texto" queda medida y disponible como REFERENCIA
NATURAL del eval (el techo contra el que se compara el parche).

Importante: el CSV de salida guarda `prompt` = q_i SOLA, sin la instruccion.
El parche tiene que reemplazar a la instruccion, no acompaniarla.

Gate de calidad: una fila se marca passed_gate=True solo si la respuesta
generada (a) esta en frances y (b) contiene la respuesta correcta. Entrenar
sobre targets malos envenena el parche.

Salida: attributes/french/targets_french.csv con las 100 filas y columnas de diagnostico.
El split se hace por POSICION sobre las 100 filas (igual que legacy), asi que
las filas nunca se reordenan ni se eliminan aca.
"""

import argparse
import os
import shutil

import pandas as pd
import tqdm

from checkers import (answer_correct, french_score, is_french, language_verdict,
                      load_questions, truncate_at_role_leak)
from lm import DEFAULT_MODEL, generate_one, load_model_and_tokenizer

INSTRUCTION_FR = "Answer in French."


def build_reference_prompt(instruction: str, question: str) -> str:
    """Como se le pasa la instruccion al modelo en la condicion de referencia."""
    return f"{instruction}\n\n{question}"

def make_row(model, tokenizer, q, ans, al, instruction, device, num_tokens, temperature):
    """Genera referencia M([FR;q]) y baseline M(q) para una pregunta y arma la fila."""
    # clean=False para poder contar cuantas veces el modelo quiso seguir
    # con otro turno pese al corte en <|eot_id|>.
    ref_raw = generate_one(model, tokenizer, build_reference_prompt(instruction, q),
                           device, num_tokens, temperature, clean=False)
    base_raw = generate_one(model, tokenizer, q, device, num_tokens, temperature, clean=False)
    ref = truncate_at_role_leak(ref_raw)
    base = truncate_at_role_leak(base_raw)

    has_answer = str(ans).strip() != ""
    # Criterio de idioma relajado: rechaza solo si la respuesta esta
    # POSITIVAMENTE en otro idioma. Exigir is_french() tiraba respuestas
    # perfectamente usables sin ninguna palabra ("18 x 5 = 90") o cuyas
    # funcionales son compartidas con el espanol ("L'Apollo 13 a eu lieu
    # en 1970."): 6 filas de 250, todas targets buenos. Misma logica que
    # check_translation.
    fr_ok = language_verdict(ref) not in ("en", "es", "de")
    # Prompts abiertos: no hay respuesta verificable, el gate es solo idioma.
    acc_ok = answer_correct(ref, ans, al) if has_answer else None
    return {
        "prompt": q,
        "output": ref,
        "answer": ans,
        "aliases": al,
        "baseline_en": base,
        "ref_role_leak": bool(ref != ref_raw.strip()),
        "baseline_role_leak": bool(base != base_raw.strip()),
        "ref_french_score": round(french_score(ref), 4),
        "ref_language": language_verdict(ref),
        "baseline_language": language_verdict(base),
        "ref_is_french": bool(fr_ok),
        "ref_answer_correct": "" if acc_ok is None else bool(acc_ok),
        "baseline_is_french": bool(is_french(base)),
        "baseline_answer_correct": (bool(answer_correct(base, ans, al))
                                    if has_answer else ""),
        "passed_gate": bool(fr_ok and acc_ok is not False),
    }


def fill_missing(args, model, tokenizer):
    """
    Modo --fill: completa SOLO las filas con `output` vacio de un targets CSV
    ya existente, dejando intactas las demas (incluidas las correcciones a
    mano y las columnas de traduccion). Es lo que permite reemplazar preguntas
    del banco sin regenerar las 250 ni perder fix_translations.py.
    """
    df = pd.read_csv(args.fill, sep=";", keep_default_na=False, dtype=str)
    faltan = df.index[df["output"].str.strip() == ""]
    print(f"--fill {args.fill}: {len(faltan)}/{len(df)} filas sin referencia, se generan solo esas")
    for i in tqdm.tqdm(faltan, desc="targets (fill)"):
        r = df.loc[i]
        row = make_row(model, tokenizer, r["prompt"], r["answer"], r["aliases"],
                       args.instruction, args.device, args.num_tokens, args.temperature)
        for k, v in row.items():
            if k in df.columns:
                df.at[i, k] = str(v)
    shutil.copy(args.fill, args.fill + ".bak")
    df.to_csv(args.fill, sep=";", index=False)
    nuevas = df.loc[faltan]
    print(f"\nFilas completadas: {len(nuevas)}  |  pasan el gate: "
          f"{(nuevas['passed_gate'].str.lower() == 'true').sum()}/{len(nuevas)}")
    for _, r in nuevas.iterrows():
        print(f"  [{'ok' if r['passed_gate'].lower() == 'true' else 'XX'}] {r['prompt'][:55]:<55} -> {r['output'][:70]}")
    print(f"\nEscrito {args.fill} (backup .bak)")


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--model", default=DEFAULT_MODEL)
    ap.add_argument("--questions", default="data/questions.csv")
    ap.add_argument("--out", default="attributes/french/targets_french.csv")
    ap.add_argument("--instruction", default=INSTRUCTION_FR)
    ap.add_argument("--num_tokens", type=int, default=100)
    ap.add_argument("--temperature", type=float, default=0.0)
    ap.add_argument("--device", default="cuda:0")
    ap.add_argument("--fill", default=None,
                    help="targets CSV existente: generar solo las filas con output vacio "
                         "(ignora --questions y --out)")
    args = ap.parse_args()

    if args.fill:
        model, tokenizer = load_model_and_tokenizer(args.model, device=args.device)
        fill_missing(args, model, tokenizer)
        return

    df = load_questions(args.questions)
    print(f"Preguntas: {len(df)}")
    print(f"Instruccion: {args.instruction!r}")
    print(f"Modelo: {args.model}")
    print("=" * 70)

    model, tokenizer = load_model_and_tokenizer(args.model, device=args.device)

    rows = []
    for _, r in tqdm.tqdm(df.iterrows(), total=len(df), desc="targets"):
        rows.append(make_row(model, tokenizer, r["prompt"], r["answer"], r["aliases"],
                             args.instruction, args.device, args.num_tokens, args.temperature))

    out = pd.DataFrame(rows)
    out_dir = os.path.dirname(args.out)
    if out_dir:
        os.makedirs(out_dir, exist_ok=True)
    out.to_csv(args.out, sep=";", index=False)

    n = len(out)
    print("\n" + "=" * 70)
    print("REFERENCIA NATURAL  M([FR ; q])")
    print(f"  en frances                 : {out['ref_is_french'].mean():.2%}")
    _acc = out["ref_answer_correct"]
    _acc = _acc[_acc != ""]
    if len(_acc):
        print(f"  respuesta correcta         : {_acc.astype(bool).mean():.2%}")
    else:
        print("  respuesta correcta         : n/a (prompts abiertos)")
    print(f"  pasan el gate (ambas)      : {out['passed_gate'].sum()}/{n}")
    print(f"  quisieron seguir de turno    : {out['ref_role_leak'].sum()}/{n}"
          "   (truncado por la red de seguridad)")
    print("\nBASELINE  M(q)   <- control, deberia ser ingles y correcto")
    print(f"  en frances                 : {out['baseline_is_french'].mean():.2%}")
    _bacc = out["baseline_answer_correct"]
    _bacc = _bacc[_bacc != ""]
    if len(_bacc):
        print(f"  respuesta correcta         : {_bacc.astype(bool).mean():.2%}")
    print(f"  quisieron seguir de turno  : {out['baseline_role_leak'].sum()}/{n}")
    print("=" * 70)

    n_train_gate = int(out.iloc[:int(0.8 * n)]["passed_gate"].sum())
    print(f"\nTargets utilizables para entrenar (primeros 80%): {n_train_gate}/{int(0.8 * n)}")
    if n_train_gate < 50:
        print("  AVISO: menos de 50 targets limpios. Revisa la instruccion o el gate")
        print("         antes de entrenar; el parche va a aprender ruido.")
    print(f"\nGuardado en '{os.path.abspath(args.out)}'")


if __name__ == "__main__":
    main()
