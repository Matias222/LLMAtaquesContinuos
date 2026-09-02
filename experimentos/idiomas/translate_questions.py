"""
Agrega una columna prompt_<lang> a un targets CSV: la MISMA pregunta, en otro
idioma.

Motivo: hay dos maneras distintas de que el modelo termine hablando en otro
idioma, y son estados internos distintos.

  A) instruccion en ingles   M(["Answer in French." + q])
     El modelo parsea una directiva meta y la cumple.

  B) pregunta en frances     M(q_fr)
     El modelo simplemente EMPAREJA el idioma de la entrada. Es el mecanismo
     mas basico y no involucra ninguna instruccion.

El parche no tiene semantica de instruccion -- es un vector sumado a los 3
primeros tokens de la pregunta -- asi que a priori es mas plausible que este
haciendo (B) que (A). layer_analysis.py y mean_diff_vectors.py miden contra
las dos.

`--lang de` agrega ademas prompt_de: no es un segundo idioma inducido por un
parche (eso seria un experimento aparte, HALLAZGOS.md pendiente 2), es la
misma pregunta en OTRO idioma para chequear si el parche de frances se
parece a "la entrada esta en aleman" tanto como a "la entrada esta en
frances" -- si es asi, lo que mide no es frances especifico sino "idioma
extranjero" en general.

    python3 translate_questions.py --model $M --targets attributes/french/targets_french.csv
    python3 translate_questions.py --model $M --targets attributes/french/targets_french.csv --lang de
"""

import argparse
import shutil
from collections import Counter

import pandas as pd
import tqdm

from checkers import (check_translation, language_verdict,
                      truncate_at_role_leak)
from lm import DEFAULT_MODEL, generate_one, load_model_and_tokenizer

# Few-shot. Con instruccion zero-shot el modelo RESPONDE la pregunta en el
# idioma destino en vez de traducirla ("Le desert le plus grand en Afrique
# est le Sahara." en lugar de "Quel est le plus grand desert chaud
# d'Afrique ?"), y como el resultado es texto valido en ese idioma el gate de
# idioma lo dejaba pasar. Mismos tres ejemplos en los dos idiomas, a
# proposito: el riesgo de fuga del few-shot (ERRORES_PROMPT_FR.md, grupo A)
# es estructural al template, no especifico de frances, y se espera que
# reaparezca en aleman con una tasa parecida.
TEMPLATES = {
    "fr": (
        "Translate the English question into French. Do NOT answer it.\n"
        "Output only the French question.\n\n"
        "English: What is the capital of Japan?\n"
        "French: Quelle est la capitale du Japon ?\n\n"
        "English: Who wrote Hamlet?\n"
        "French: Qui a ecrit Hamlet ?\n\n"
        "English: How does digestion work?\n"
        "French: Comment fonctionne la digestion ?\n\n"
        "English: {q}\nFrench:"
    ),
    "de": (
        "Translate the English question into German. Do NOT answer it.\n"
        "Output only the German question.\n\n"
        "English: What is the capital of Japan?\n"
        "German: Was ist die Hauptstadt von Japan?\n\n"
        "English: Who wrote Hamlet?\n"
        "German: Wer hat Hamlet geschrieben?\n\n"
        "English: How does digestion work?\n"
        "German: Wie funktioniert die Verdauung?\n\n"
        "English: {q}\nGerman:"
    ),
}
LABELS = {"fr": "French", "de": "German"}


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--model", default=DEFAULT_MODEL)
    ap.add_argument("--targets", default="attributes/french/targets_french.csv")
    ap.add_argument("--lang", choices=list(TEMPLATES), default="fr")
    ap.add_argument("--num_tokens", type=int, default=60)
    ap.add_argument("--device", default="cuda:0")
    ap.add_argument("--out", default=None,
                    help="por defecto reescribe --targets in-place (deja .bak)")
    args = ap.parse_args()

    col = f"prompt_{args.lang}"
    label = LABELS[args.lang]
    template = TEMPLATES[args.lang]

    df = pd.read_csv(args.targets, sep=";", keep_default_na=False)
    model, tokenizer = load_model_and_tokenizer(args.model, device=args.device)

    translated, oks, motivos = [], [], []
    for _, r in tqdm.tqdm(df.iterrows(), total=len(df), desc=f"traduciendo ({args.lang})"):
        t = truncate_at_role_leak(generate_one(
            model, tokenizer, template.format(q=r["prompt"]), args.device,
            args.num_tokens, 0.0, clean=False))
        # Primera linea no vacia, sin comillas ni prefijo "French:"/"German:".
        t = next((ln.strip() for ln in t.split("\n") if ln.strip()), "")
        if t.lower().startswith(f"{label.lower()}:"):
            t = t.split(":", 1)[1].strip()
        t = t.strip('"').strip()
        ok, motivo = check_translation(r["prompt"], t, r.get("answer", ""),
                                       r.get("aliases", ""))
        translated.append(t); oks.append(ok); motivos.append(motivo)

    df[col] = translated
    df[f"{col}_language"] = [language_verdict(t) for t in translated]
    df[f"{col}_ok"] = oks

    n = len(df)
    print(f"\ntraducciones usables ({label}): {sum(oks)}/{n} ({sum(oks) / n:.0%})")
    print("motivos de rechazo:", {k: v for k, v in Counter(motivos).items() if k != "ok"})
    malas = [(r["prompt"], r[col], m)
             for (_, r), m, o in zip(df.iterrows(), motivos, oks) if not o]
    if malas:
        print(f"\nrechazadas ({len(malas)}), no entran en la direccion d_{args.lang}:")
        for p, t, m in malas[:10]:
            print(f"  [{m}]")
            print(f"     {p[:60]}")
            print(f"  -> {t[:60]}")
    if sum(oks) < 0.5 * n:
        print(f"\n  AVISO: menos de la mitad usables. d_{args.lang} va a ser ruidosa;")
        print("         revisa el TEMPLATE antes de correr mean_diff_vectors.py.")

    dest = args.out or args.targets
    if dest == args.targets:
        shutil.copy(args.targets, args.targets + ".bak")
    df.to_csv(dest, sep=";", index=False)
    print(f"\nEscrito {dest}" + (" (backup .bak)" if dest == args.targets else ""))
    print("\nEjemplos:")
    for _, r in df.head(5).iterrows():
        print(f"  {r['prompt'][:46]:<46} -> {r[col][:56]}")


if __name__ == "__main__":
    main()
