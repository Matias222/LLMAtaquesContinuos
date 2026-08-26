"""
Agrega la columna `prompt_fr` a un targets CSV: la MISMA pregunta, en frances.

Motivo: hay dos maneras distintas de que el modelo termine hablando frances, y
son estados internos distintos.

  A) instruccion en ingles   M(["Answer in French." + q])
     El modelo parsea una directiva meta y la cumple.

  B) pregunta en frances     M(q_fr)
     El modelo simplemente EMPAREJA el idioma de la entrada. Es el mecanismo
     mas basico y no involucra ninguna instruccion.

El parche no tiene semantica de instruccion -- es un vector sumado a los 3
primeros tokens de la pregunta -- asi que a priori es mas plausible que este
haciendo (B) que (A). layer_analysis.py mide contra las dos.

    python3 translate_questions.py --model $M --targets targets_french.csv
"""

import argparse
import shutil

import pandas as pd
import tqdm

from checkers import is_french, language_verdict, truncate_at_role_leak
from lm import DEFAULT_MODEL, generate_one, load_model_and_tokenizer

TEMPLATE = ("Translate the following question into French. "
            "Output only the translation, nothing else.\n\n{q}")


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--model", default=DEFAULT_MODEL)
    ap.add_argument("--targets", default="targets_french.csv")
    ap.add_argument("--num_tokens", type=int, default=60)
    ap.add_argument("--device", default="cuda:0")
    args = ap.parse_args()

    df = pd.read_csv(args.targets, sep=";", keep_default_na=False)
    model, tokenizer = load_model_and_tokenizer(args.model, device=args.device)

    fr, ok = [], 0
    for _, r in tqdm.tqdm(df.iterrows(), total=len(df), desc="traduciendo"):
        t = truncate_at_role_leak(generate_one(
            model, tokenizer, TEMPLATE.format(q=r["prompt"]), args.device,
            args.num_tokens, 0.0, clean=False))
        # El modelo a veces envuelve la traduccion en comillas o la precede de
        # un preambulo; nos quedamos con la primera linea no vacia.
        t = next((ln.strip().strip('"') for ln in t.split("\n") if ln.strip()), "")
        fr.append(t)
        ok += is_french(t)

    df["prompt_fr"] = fr
    df["prompt_fr_language"] = [language_verdict(t) for t in fr]

    n = len(df)
    print(f"\ntraducciones en frances: {ok}/{n} ({ok / n:.0%})")
    print("distribucion:", df["prompt_fr_language"].value_counts().to_dict())
    malas = df[df["prompt_fr_language"] != "fr"]
    if len(malas):
        print(f"\nno son frances ({len(malas)}), no las use para la direccion:")
        for _, r in malas.head(8).iterrows():
            print(f"  {r['prompt'][:44]:<44} -> {r['prompt_fr'][:56]}")

    shutil.copy(args.targets, args.targets + ".bak")
    df.to_csv(args.targets, sep=";", index=False)
    print(f"\nActualizado {args.targets} (backup .bak)")
    print("\nEjemplos:")
    for _, r in df.head(5).iterrows():
        print(f"  {r['prompt'][:46]:<46} -> {r['prompt_fr'][:56]}")


if __name__ == "__main__":
    main()
