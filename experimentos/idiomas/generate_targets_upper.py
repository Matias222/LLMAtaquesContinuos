"""
Paso 0 del atributo "mayusculas": generar los targets de teacher forcing.

    y_i = M([INSTRUCCION ; q_i])

Mismo diseno que generate_targets.py (francés), pero el atributo inducido no
es un idioma sino un formato: responder enteramente en mayusculas. Se usa la
MISMA instruccion en ingles a proposito -- si el target tuviera francés
mezclado, el parche de mayusculas aprenderia tambien algo de francés y la
composicion v_fr + v_upper dejaria de testear dos direcciones independientes.

Gate de calidad: una fila se marca passed_gate=True solo si la respuesta
generada (a) esta en mayusculas y (b) contiene la respuesta correcta.

Caveat conocido (no resuelto aca): `answer_correct` compara simbolos quimicos
y respuestas de largo <=2 con case-sensitivity exacta a proposito, para no
confundir el simbolo "Au" con la preposicion francesa "au" (ver checkers.py).
Sobre texto todo-mayusculas eso se vuelve indistinguible: "AU" no matchea el
candidato "Au". La accuracy de este atributo esta subestimada en preguntas de
simbolo quimico; no se parchea porque hacerlo bien reintroduce el bug francés
que ese case-sensitivity evita.

Salida: attributes/uppercase/targets_upper.csv, mismo esquema de columnas que
targets_french.csv. Eso alcanza para reusar train_lang_patch.py sin cambios
(solo lee prompt/output/passed_gate). eval_lang_patch.py tambien CORRE sin
cambios sobre este CSV, pero su compliance impreso (is_french/french_score)
mide el atributo equivocado: va a reportar ~0% is_french sobre texto en
ingles, que no dice nada sobre si el parche cumple "mayusculas". Sirve
igual para leer accuracy y el CE head/tail (esos dos numeros no dependen del
checker de idioma). El evaluador real del atributo -- is_uppercase sobre las
condiciones correctas -- es compose_patches.py.
"""

import argparse
import os

import pandas as pd
import tqdm

from checkers import answer_correct, is_uppercase, load_questions, truncate_at_role_leak, uppercase_score
from generate_targets import build_reference_prompt
from lm import DEFAULT_MODEL, generate_one, load_model_and_tokenizer

INSTRUCTION_UPPER = "Respond entirely in uppercase letters."


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--model", default=DEFAULT_MODEL)
    ap.add_argument("--questions", default="data/questions.csv")
    ap.add_argument("--out", default="attributes/uppercase/targets_upper.csv")
    ap.add_argument("--instruction", default=INSTRUCTION_UPPER)
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

        # clean=False para poder contar cuantas veces el modelo quiso seguir
        # con otro turno pese al corte en <|eot_id|>.
        ref_raw = generate_one(model, tokenizer,
                               build_reference_prompt(args.instruction, q),
                               args.device, args.num_tokens, args.temperature,
                               clean=False)
        base_raw = generate_one(model, tokenizer, q,
                                args.device, args.num_tokens, args.temperature,
                                clean=False)
        ref = truncate_at_role_leak(ref_raw)
        base = truncate_at_role_leak(base_raw)

        has_answer = str(ans).strip() != ""
        up_ok = is_uppercase(ref)
        acc_ok = answer_correct(ref, ans, al) if has_answer else None
        rows.append({
            "prompt": q,
            "output": ref,
            "answer": ans,
            "aliases": al,
            "baseline_en": base,
            "ref_role_leak": bool(ref != ref_raw.strip()),
            "baseline_role_leak": bool(base != base_raw.strip()),
            "ref_uppercase_score": round(uppercase_score(ref), 4),
            "ref_is_uppercase": bool(up_ok),
            "ref_answer_correct": "" if acc_ok is None else bool(acc_ok),
            "baseline_is_uppercase": bool(is_uppercase(base)),
            "baseline_answer_correct": (bool(answer_correct(base, ans, al))
                                        if has_answer else ""),
            "passed_gate": bool(up_ok and acc_ok is not False),
        })

    out = pd.DataFrame(rows)
    out_dir = os.path.dirname(args.out)
    if out_dir:
        os.makedirs(out_dir, exist_ok=True)
    out.to_csv(args.out, sep=";", index=False)

    n = len(out)
    print("\n" + "=" * 70)
    print("REFERENCIA NATURAL  M([MAYUS ; q])")
    print(f"  en mayusculas              : {out['ref_is_uppercase'].mean():.2%}")
    _acc = out["ref_answer_correct"]
    _acc = _acc[_acc != ""]
    if len(_acc):
        print(f"  respuesta correcta         : {_acc.astype(bool).mean():.2%}"
              "   (subestimada en simbolos quimicos, ver docstring)")
    else:
        print("  respuesta correcta         : n/a (prompts abiertos)")
    print(f"  pasan el gate (ambas)      : {out['passed_gate'].sum()}/{n}")
    print(f"  quisieron seguir de turno    : {out['ref_role_leak'].sum()}/{n}"
          "   (truncado por la red de seguridad)")
    print("\nBASELINE  M(q)   <- control, no deberia estar en mayusculas")
    print(f"  en mayusculas              : {out['baseline_is_uppercase'].mean():.2%}")
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
