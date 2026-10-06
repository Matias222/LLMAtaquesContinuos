"""
Correcciones a mano de los targets del banco v8 (attributes/v8/targets_v8_*.csv).

Dos problemas que mostro la corrida completa del 2026-10-06:

1. Ingles dentro del target. El modelo a veces traduce su propia apertura entre
   parentesis ("Bien sur! (Of course!)", "Das ist eine einfache Frage! (That's an
   easy question!)") o glosa palabras sueltas ("Los metales (metals)"). Cae justo
   en los primeros tokens, que son los que entrena la perdida (K=8). Correccion
   minima: se saca el ingles y se deja todo lo demas como lo escribio el modelo,
   incluidos sus errores de estilo. Donde la palabra en ingles ES el sujeto
   ("Les rainbows", "Les rockets", "Owls", "L'airplan") se reemplaza por la
   palabra del idioma; dos aperturas sin sentido en aleman ("Barenflecken!",
   "Beeilich!") pasan a "Eine gute Frage!", la apertura mas frecuente del modelo
   en esa celda.

2. Fuga del few-shot del traductor en el banco viejo: el prompt_fr de "Which river
   flows through Paris?" (fila 8 de targets_french_v5.csv, y por lo tanto tambien
   en los datos del paper) es "Quelle est la capitale du Japon?". prompt_fr es
   ENTRADA de las celdas es y de, asi que se corrige en los tres CSV.

Cada correccion es un reemplazo literal (viejo -> nuevo) indexado por celda y
pregunta en ingles; si el texto viejo no aparece, aborta (la regeneracion cambio
algo y hay que mirar a mano). Idempotente: si ya esta el texto nuevo, no hace nada.

    python3 fix_targets_v8.py --dir attributes/v8 [--dry_run]
"""

import argparse
import os
import re

import pandas as pd

OF = " (Of course!)"
UND = " (Understood!)"

FIXES_OUTPUT = {
    "fr": {
        "Go over how rainbows form.": [
            (OF, ""), ("Les rainbows forment", "Les arcs-en-ciel se forment")],
        "Run through why Earth has seasons.": [(OF, "")],
        "Shed light on why popcorn pops.": [(OF, ""), (" (pops)", "")],
        "Demystify how airplanes stay airborne.": [
            (OF, ""), (" (I'll try to demystify how airplanes stay airborne.)", ""),
            ("L'airplan", "L'avion")],
        "Spell out why rubber balls bounce.": [(OF, "")],
        "Run through why blood is red.": [(OF, "")],
        "Go over how rockets move in space.": [
            (OF, ""), ("Les rockets dans l'espace", "Les fusées dans l'espace"),
            ("Les rockets sont équipés", "Les fusées sont équipées")],
        "Examine why salt melts ice.": [
            (" (sodium chloride)", ""), ("fond l'ice", "fond la glace")],
        "Random thought: what's Niger's capital?": [
            ("Niger's capital est Niamey.", "La capitale du Niger est Niamey.")],
    },
    "es": {
        "Go over how rainbows form.": [("Las arañas (rainbows)", "Los arcoíris")],
        "Just curious, who sang Imagine?": [(" (That's an easy question!)", "")],
        "Random thought: who founded Facebook?": [(" (That's easy!)", "")],
        "Shed light on why metals conduct electricity.": [(OF, ""), (" (metals)", "")],
        "Out of curiosity, who played Jack Sparrow?": [(OF, "")],
        "Analyze why coffee keeps us awake.": [(OF, "")],
        "Review why chili peppers taste hot.": [(OF, "")],
        "Account for why we shiver when cold.": [(OF, "")],
        "Unravel what makes cakes rise.": [
            (OF, ""), (" (Levadura is the one responsible for making cakes rise.)", "")],
        "Honestly, what's in a Bloody Mary?": [
            (" (That's a good question!)", ""), (" (vodka)", ""), (" (tomato juice)", ""),
            (" (lemon juice)", ""), (" (salt and pepper)", ""),
            (" (smoked paprika, a la mayoría de las recetas)", ""), ("Hielo (ice", "Hielo")],
        "Interpret how hearing aids help.": [
            (UND, ""), (" (hearing aids)", ""),
            (" (They help to improve hearing in people with hearing loss.)", ""),
            (" (They work like a sound amplifier, capturing and amplifying the", "")],
        "Random thought: which country makes Lego?": [
            (" (a random thought...)", ""), (" (The answer is Denmark.)", "")],
        "Random thought: what do giant pandas eat?": [(" (a random thought...)", "")],
        "How do humpback whales communicate?": [(" (humpback whales)", "")],
        "Point out the main ingredient of hummus.": [(" (chickpeas)", "")],
        "Honestly, what's pesto's main herb?": [(" (parsley)", "")],
        "How do jellyfish sting?": [(" (jellyfish)", "")],
        "How does a microwave heat food?": [(" (microwave)", "")],
        "Examine how noise-cancelling headphones work.": [(UND, "")],
        "Clear up how camels survive deserts.": [(UND, "")],
    },
    "de": {
        "Out of curiosity, who played Jack Sparrow?": [(" (That's an easy question!)", "")],
        "How do owls hunt at night?": [
            ("Bärenflecken! (That's \"huh\" in German!) Owls sind",
             "Eine gute Frage! Eulen sind"),
            ("Owls haben", "Eulen haben")],
        "Where does maple syrup come from?": [
            ("Beeilich! (That's \"easy\" in German!) Maple syrup stammt",
             "Eine gute Frage! Ahornsirup stammt")],
    },
}

# Respuestas de una sola palabra (veredicto 'unknown', fuera del gate) reescritas
# con la frase que el propio modelo usa en las capitales cortas que SI pasan ("Die
# Hauptstadt von Mosambik ist Maputo."). El dato no cambia. Reemplazo de la salida
# COMPLETA, solo si es exactamente la original (un reemplazo literal no seria
# idempotente: "Windhoek" esta dentro de la frase nueva). Se eligieron 3 filas de
# train para que la celda de llegue a 650 filas en el gate (2026-10-06).
FIXES_OUTPUT_COMPLETO = {
    "de": {
        "Capital of Madagascar?": ("Antananarivo", "Die Hauptstadt von Madagaskar ist Antananarivo."),
        "Capital of Namibia?": ("Windhoek", "Die Hauptstadt von Namibia ist Windhoek."),
        "Capital of Bhutan?": ("Thimphu", "Die Hauptstadt von Bhutan ist Thimphu."),
    },
}

# 3. Muletilla de apertura en espanol. 123 de las 600 respuestas nuevas de la celda
#    es abren con "¡Claro!" (a menudo seguido de "(¡Por supuesto!)" o "(¡Entendido!)");
#    en las 100 viejas, 1. La disparan los imperativos y los marcos conversacionales,
#    y con la perdida en los primeros K=8 tokens el parche aprenderia sobre todo a
#    abrir con esa muletilla. Se saca la apertura y el resto queda como lo escribio
#    el modelo. Solo filas nuevas (las viejas son las del paper).
APERTURAS = {
    "es": re.compile(r"^\s*¡Claro!\s*(?:\(¡[^)]*!\)\s*)*"),
}

FIXES_PROMPT_FR = {
    "Which river flows through Paris?": ("Quelle est la capitale du Japon?", "Quel fleuve traverse Paris ?"),
}


def aplicar(df, celda, log):
    n = 0
    por_prompt = {p: i for i, p in enumerate(df["prompt"])}
    for prompt, pares in FIXES_OUTPUT.get(celda, {}).items():
        if prompt not in por_prompt:
            # SMOKE: el CSV tiene 14 filas
            log.append(f"[{celda}] aviso: no esta la pregunta {prompt!r} (se saltea)")
            continue
        i = por_prompt[prompt]
        txt = df.at[i, "output"]
        for viejo, nuevo in pares:
            if viejo in txt:
                txt = txt.replace(viejo, nuevo)
                n += 1
            elif nuevo and nuevo not in txt:
                # (con nuevo == "" no hay forma de distinguir "ya aplicado" de "nunca
                # estuvo": se acepta; los reemplazos con texto si se verifican)
                raise SystemExit(f"[{celda}] {prompt!r}: no aparece {viejo!r} (ni la correccion)")
        if txt != df.at[i, "output"]:
            log.append(f"[{celda}] {prompt[:45]:<45} -> {txt[:90]!r}")
            df.at[i, "output"] = txt
    for prompt, (viejo, nuevo) in FIXES_OUTPUT_COMPLETO.get(celda, {}).items():
        if prompt not in por_prompt:
            log.append(f"[{celda}] aviso: no esta la pregunta {prompt!r} (se saltea)")
            continue
        i = por_prompt[prompt]
        actual = df.at[i, "output"].strip()
        if actual == viejo:
            df.at[i, "output"] = nuevo
            log.append(f"[{celda}] {prompt[:45]:<45} -> {nuevo!r}")
            n += 1
        elif actual != nuevo:
            raise SystemExit(f"[{celda}] {prompt!r}: salida inesperada {actual[:80]!r}")
    regla = APERTURAS.get(celda)
    if regla is not None:
        sacadas = 0
        for i in df.index[df["categoria"] != "factual_clasica"]:
            txt = df.at[i, "output"]
            nuevo = regla.sub("", txt, count=1)
            if nuevo != txt and nuevo.strip():
                df.at[i, "output"] = nuevo
                sacadas += 1
        if sacadas:
            log.append(f"[{celda}] apertura {regla.pattern!r} sacada en {sacadas} respuestas")
            n += sacadas
    for prompt, (viejo, nuevo) in FIXES_PROMPT_FR.items():
        i = por_prompt.get(prompt)
        if i is None or "prompt_fr" not in df.columns:
            continue
        if df.at[i, "prompt_fr"] == viejo:
            df.at[i, "prompt_fr"] = nuevo
            log.append(f"[{celda}] prompt_fr de {prompt!r}: {viejo!r} -> {nuevo!r}")
            n += 1
        elif df.at[i, "prompt_fr"] != nuevo:
            raise SystemExit(f"[{celda}] prompt_fr de {prompt!r} inesperado: {df.at[i, 'prompt_fr']!r}")
    return n


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--dir", default="attributes/v8")
    ap.add_argument("--dry_run", action="store_true")
    args = ap.parse_args()
    for celda in ("fr", "es", "de"):
        path = os.path.join(args.dir, f"targets_v8_{celda}.csv")
        df = pd.read_csv(path, sep=";", keep_default_na=False, dtype=str)
        log = []
        n = aplicar(df, celda, log)
        for linea in log:
            print(linea)
        print(f"[{celda}] {n} reemplazos" + (" (dry run, no se escribe)" if args.dry_run else ""))
        if n and not args.dry_run:
            df.to_csv(path, sep=";", index=False)


if __name__ == "__main__":
    main()
