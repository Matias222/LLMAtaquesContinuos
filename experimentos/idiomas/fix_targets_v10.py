"""
Correcciones a mano de los targets v10 (attributes/v10/targets_v8_*.csv, y = M(q_X)).

Las correcciones viven en data/banco_v8/correcciones_v10.json:

    {celda: {pregunta en ingles: {"sha1_original": ..., "motivo": ..., "output": ...}}}

`output` es la respuesta completa corregida: se corrige todo el texto, no solo la
cabeza de la perdida (K=8). Criterio: se conserva el estilo y la cabeza del modelo
cuando estan bien; se corrigen los errores de contenido (respuesta o mecanismo
equivocado, datos falsos, ingles o terminos de otro idioma); las respuestas de una
sola palabra (veredicto 'unknown', sin senal de idioma) pasan a una oracion en el
idioma de la celda; el item que quedo cortado por el limite de tokens se completa
en una oracion.

Cada correccion guarda el sha1 del output que corrige. Si el output del CSV no es
ni ese original ni la version corregida, aborta: la regeneracion cambio algo y hay
que mirar a mano. Idempotente. Marca output_hand_fixed=True. El gate lo recalcula
despues `preparar_targets_v8.py regate` sobre el texto corregido (en
run_targets_v10.sh la etapa fix va antes que regate).

Ademas corrige las traducciones de las preguntas (clave "_traducciones" del JSON:
{pregunta en ingles: {"es"|"fr"|"de": {"viejo", "nuevo", "motivo"}}}) en las tres
celdas, porque prompt_<l> es entrada de todas. Salen de una auditoria de las 700
contra el ingles: titulos mal traducidos ("Le Petit Chaperon Rouge" por The
Nutcracker), sentido cambiado ("sin ases" por "without jokers"), la fuga del
few-shot del traductor en el prompt_fr de "Which river flows through Paris?" ("Quelle
est la capitale du Japon?", la misma de fix_targets_v8.py) y errores de gramatica.
Donde el target se habia generado con la pregunta mal traducida, su correccion
responde la pregunta corregida.

    python3 fix_targets_v10.py --dir attributes/v10 [--dry_run]
"""

import argparse
import hashlib
import json
import os

import pandas as pd

CORRECCIONES = "data/banco_v8/correcciones_v10.json"


def sha1(texto):
    return hashlib.sha1(texto.encode("utf-8")).hexdigest()


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--dir", required=True)
    ap.add_argument("--correcciones", default=CORRECCIONES)
    ap.add_argument("--dry_run", action="store_true")
    args = ap.parse_args()

    with open(args.correcciones, encoding="utf-8") as f:
        corr = json.load(f)
    errores = []
    for celda in ("fr", "es", "de"):
        path = os.path.join(args.dir, f"targets_v8_{celda}.csv")
        df = pd.read_csv(path, sep=";", keep_default_na=False, dtype=str)
        if "output_hand_fixed" not in df.columns:
            df["output_hand_fixed"] = ""
        trad = 0
        for p, cols in corr.get("_traducciones", {}).items():
            m = df["prompt"] == p
            for l, t in cols.items():
                col = f"prompt_{l}"
                if m.sum() != 1 or df.loc[m, col].iloc[0] not in (t["viejo"], t["nuevo"]):
                    errores.append(f"[{celda}] {col} de {p!r}: no es ni {t['viejo']!r} ni {t['nuevo']!r}")
                    continue
                trad += df.loc[m, col].iloc[0] != t["nuevo"]
                df.loc[m, col] = t["nuevo"]
        c = corr.get(celda, {})
        aplicadas = ya = 0
        for i in df.index:
            p = df.at[i, "prompt"]
            if p not in c:
                continue
            nuevo = c[p]["output"]
            if df.at[i, "output"] == nuevo:
                ya += 1
            elif sha1(df.at[i, "output"]) == c[p]["sha1_original"]:
                df.at[i, "output"] = nuevo
                aplicadas += 1
            else:
                errores.append(f"[{celda}] {p!r}: el output no es el original esperado ni la correccion")
                continue
            df.at[i, "output_hand_fixed"] = "True"
        sin_fila = sorted(set(c) - set(df["prompt"]))
        print(f"[{celda}] {aplicadas} corregidas, {ya} ya estaban, {len(c)} en el JSON, {trad} traducciones"
              + (f" ({len(sin_fila)} preguntas sin fila en este CSV)" if sin_fila else ""))
        if not args.dry_run and not errores:
            df.to_csv(path, sep=";", index=False)
    for e in errores:
        print("ERROR", e)
    if errores:
        raise SystemExit(f"{len(errores)} correcciones no aplicables: no se escribio nada de la celda con error")
    if args.dry_run:
        print("--dry_run: no se escribe nada")


if __name__ == "__main__":
    main()
