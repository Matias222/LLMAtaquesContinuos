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

    python3 translate_questions.py --model $M --targets attributes/french/targets_french.csv
"""

import argparse
import shutil

import pandas as pd
import tqdm

from checkers import (check_translation, language_verdict,
                      truncate_at_role_leak)
from lm import DEFAULT_MODEL, generate_one, load_model_and_tokenizer

# Few-shot. Con instruccion zero-shot el modelo RESPONDE la pregunta en frances
# en vez de traducirla ("Le desert le plus grand en Afrique est le Sahara." en
# lugar de "Quel est le plus grand desert chaud d'Afrique ?"), y como el
# resultado es frances valido el gate de idioma lo dejaba pasar.
TEMPLATE = (
    "Translate the English question into French. Do NOT answer it.\n"
    "Output only the French question.\n\n"
    "English: What is the capital of Japan?\n"
    "French: Quelle est la capitale du Japon ?\n\n"
    "English: Who wrote Hamlet?\n"
    "French: Qui a ecrit Hamlet ?\n\n"
    "English: How does digestion work?\n"
    "French: Comment fonctionne la digestion ?\n\n"
    "English: {q}\nFrench:"
)




def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--model", default=DEFAULT_MODEL)
    ap.add_argument("--targets", default="attributes/french/targets_french.csv")
    ap.add_argument("--num_tokens", type=int, default=60)
    ap.add_argument("--device", default="cuda:0")
    ap.add_argument("--out", default=None,
                    help="por defecto reescribe --targets in-place (deja .bak)")
    args = ap.parse_args()

    df = pd.read_csv(args.targets, sep=";", keep_default_na=False)
    model, tokenizer = load_model_and_tokenizer(args.model, device=args.device)

    fr, oks, motivos = [], [], []
    for _, r in tqdm.tqdm(df.iterrows(), total=len(df), desc="traduciendo"):
        t = truncate_at_role_leak(generate_one(
            model, tokenizer, TEMPLATE.format(q=r["prompt"]), args.device,
            args.num_tokens, 0.0, clean=False))
        # Primera linea no vacia, sin comillas ni prefijo "French:".
        t = next((ln.strip() for ln in t.split("\n") if ln.strip()), "")
        if t.lower().startswith("french:"):
            t = t.split(":", 1)[1].strip()
        t = t.strip('"').strip()
        ok, motivo = check_translation(r["prompt"], t, r.get("answer", ""),
                                       r.get("aliases", ""))
        fr.append(t); oks.append(ok); motivos.append(motivo)

    df["prompt_fr"] = fr
    df["prompt_fr_language"] = [language_verdict(t) for t in fr]
    df["prompt_fr_ok"] = oks

    n = len(df)
    print(f"\ntraducciones usables: {sum(oks)}/{n} ({sum(oks) / n:.0%})")
    from collections import Counter
    print("motivos de rechazo:", {k: v for k, v in Counter(motivos).items() if k != "ok"})
    malas = [(r["prompt"], r["prompt_fr"], m)
             for (_, r), m, o in zip(df.iterrows(), motivos, oks) if not o]
    if malas:
        print(f"\nrechazadas ({len(malas)}), no entran en la direccion d_frq:")
        for p, t, m in malas[:10]:
            print(f"  [{m}]")
            print(f"     {p[:60]}")
            print(f"  -> {t[:60]}")
    if sum(oks) < 0.5 * n:
        print("\n  AVISO: menos de la mitad usables. d_frq va a ser ruidosa;")
        print("         revisa el TEMPLATE antes de correr layer_analysis.")

    dest = args.out or args.targets
    if dest == args.targets:
        shutil.copy(args.targets, args.targets + ".bak")
    df.to_csv(dest, sep=";", index=False)
    print(f"\nEscrito {dest}" + (" (backup .bak)" if dest == args.targets else ""))
    print("\nEjemplos:")
    for _, r in df.head(5).iterrows():
        print(f"  {r['prompt'][:46]:<46} -> {r['prompt_fr'][:56]}")


if __name__ == "__main__":
    main()
