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

Salida: targets_french.csv con las 100 filas y columnas de diagnostico.
El split se hace por POSICION sobre las 100 filas (igual que legacy), asi que
las filas nunca se reordenan ni se eliminan aca.
"""

import argparse
import os

import pandas as pd
import tqdm

from checkers import answer_correct, french_score, is_french, load_questions
from lm import DEFAULT_MODEL, generate_one, load_model_and_tokenizer

INSTRUCTION_FR = "Answer in French."


def build_reference_prompt(instruction: str, question: str) -> str:
    """Como se le pasa la instruccion al modelo en la condicion de referencia."""
    return f"{instruction}\n\n{question}"


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--model", default=DEFAULT_MODEL)
    ap.add_argument("--questions", default="questions.csv")
    ap.add_argument("--out", default="targets_french.csv")
    ap.add_argument("--instruction", default=INSTRUCTION_FR)
    ap.add_argument("--num_tokens", type=int, default=100)
    ap.add_argument("--temperature", type=float, default=0.0)
    ap.add_argument("--device", default="cuda:0")
    args = ap.parse_args()

    df = load_questions(args.questions)
    print(f"Preguntas: {len(df)}")
    print(f"Instruccion: {args.instruction!r}")
    print(f"Modelo: {args.model}")
    print("=" * 70)

    model, tokenizer = load_model_and_tokenizer(args.model, device=args.device)

    rows = []
    for _, r in tqdm.tqdm(df.iterrows(), total=len(df), desc="targets"):
        q, ans, al = r["prompt"], r["answer"], r["aliases"]

        ref = generate_one(model, tokenizer,
                           build_reference_prompt(args.instruction, q),
                           args.device, args.num_tokens, args.temperature)
        base = generate_one(model, tokenizer, q,
                            args.device, args.num_tokens, args.temperature)

        fr_ok = is_french(ref)
        acc_ok = answer_correct(ref, ans, al)
        rows.append({
            "prompt": q,
            "output": ref.strip(),
            "answer": ans,
            "aliases": al,
            "baseline_en": base.strip(),
            "ref_french_score": round(french_score(ref), 4),
            "ref_is_french": bool(fr_ok),
            "ref_answer_correct": bool(acc_ok),
            "baseline_is_french": bool(is_french(base)),
            "baseline_answer_correct": bool(answer_correct(base, ans, al)),
            "passed_gate": bool(fr_ok and acc_ok),
        })

    out = pd.DataFrame(rows)
    out.to_csv(args.out, sep=";", index=False)

    n = len(out)
    print("\n" + "=" * 70)
    print("REFERENCIA NATURAL  M([FR ; q])")
    print(f"  en frances                 : {out['ref_is_french'].mean():.2%}")
    print(f"  respuesta correcta         : {out['ref_answer_correct'].mean():.2%}")
    print(f"  pasan el gate (ambas)      : {out['passed_gate'].sum()}/{n}")
    print("\nBASELINE  M(q)   <- control, deberia ser ingles y correcto")
    print(f"  en frances                 : {out['baseline_is_french'].mean():.2%}")
    print(f"  respuesta correcta         : {out['baseline_answer_correct'].mean():.2%}")
    print("=" * 70)

    n_train_gate = int(out.iloc[:int(0.8 * n)]["passed_gate"].sum())
    print(f"\nTargets utilizables para entrenar (primeros 80%): {n_train_gate}/{int(0.8 * n)}")
    if n_train_gate < 50:
        print("  AVISO: menos de 50 targets limpios. Revisa la instruccion o el gate")
        print("         antes de entrenar; el parche va a aprender ruido.")
    print(f"\nGuardado en '{os.path.abspath(args.out)}'")


if __name__ == "__main__":
    main()
