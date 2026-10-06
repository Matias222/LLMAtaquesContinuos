"""
Identificacion de idioma con GlotLID (Kargaran et al., 2023), la que usan
todas las metricas de idioma del repo a traves de checkers.language_verdict.

Reemplaza a la heuristica de palabras funcionales de checkers.py, que solo
conocia fr/en/es/de/it/pt: el catalan, el sueco o el neerlandes que aparecen al
restar un parche salian como otro idioma o como 'unknown' y habia que
clasificarlos a mano. Validacion contra las 450 salidas clasificadas a mano
(validar_glotlid.py): ver runs/validar_glotlid/resumen.md.

Dos reglas fijas, declaradas en el paper (seccion 3.4):

  1. LISTA CERRADA. Se toma el idioma mas probable DENTRO de IDIOMAS. GlotLID
     distingue variedades cercanas (extremeno, asturiano, chabacano) y una
     respuesta corta en espanol como "La capital de Jordania es Aman." sale
     `ext` 0.61 / `es` 0.38. Ninguna de esas variedades es una respuesta
     posible del modelo en estos experimentos.
  2. MENOS DE MIN_PALABRAS PALABRAS = SIN IDIOMA ('unknown'). "Kiev",
     "Em 2000", "Marie Curie" no tienen idioma decidible.

Las variedades del espanol que GlotLID separa (VARIEDADES: extremeno,
chabacano, asturiano) suman su probabilidad a `es` ANTES de elegir: si no,
"El capital de Senegal es Dakar." (ext 0.99) caia al siguiente idioma de la
lista, que era catalan con 0.01.

Ademas cada veredicto lleva `revisar` (va a revision manual; el resto no se
mira) si:
  - el top-1 de GlotLID cae fuera de la lista, o la probabilidad del idioma
    elegido es < P_REVISAR;
  - el veredicto es catalan: es la confusion conocida (respuestas cortas en
    espanol sin tildes, "La capital de Ghana es Acra." -> ca 0.66) y el
    catalan es un destino que se reporta en la resta;
  - el texto mezcla idiomas: las oraciones de MIN_PALABRAS_ORACION palabras o
    mas no salen todas en el mismo idioma ("I think you meant to ask
    'Quel est...' Le symbole...").
Validacion en runs/validar_glotlid/resumen.md.

Backend (variable de entorno LANG_ID):
    glotlid     (default) GlotLID. Si no encuentra el modelo, FALLA: no hay
                fallback silencioso, para que dos corridas nunca mezclen
                detectores sin saberlo.
    heuristica  la heuristica vieja de checkers.py, solo para reproducir
                numeros anteriores.

Modelo: GLOTLID_MODEL=/ruta/model.bin, o si no se busca en modelos/glotlid/
de la raiz del repo o de experimentos/idiomas.
    hf download cis-lmu/glotlid model.bin --local-dir modelos/glotlid
"""

import functools
import os
import re

IDIOMAS = ("fr", "en", "es", "de", "it", "pt", "ca", "nl", "sv", "no", "da", "ro", "gl")
MIN_PALABRAS = 3
P_REVISAR = 0.5          # por debajo, el veredicto va a revision manual
MIN_PALABRAS_ORACION = 4  # oraciones mas cortas no cuentan para detectar mezcla
REVISAR_SIEMPRE = ("ca",)

# variedades que GlotLID distingue y el modelo no produce en estos experimentos:
# su probabilidad se suma a la del idioma de la lista (observadas en la validacion)
VARIEDADES = {"ext": "es", "cbk": "es", "ast": "es"}

# ISO 639-3 de GlotLID -> codigos de dos letras del repo
ISO3 = {"fra": "fr", "eng": "en", "spa": "es", "deu": "de", "ita": "it", "por": "pt",
        "cat": "ca", "nld": "nl", "swe": "sv", "nor": "no", "nob": "no", "nno": "no",
        "dan": "da", "ron": "ro", "glg": "gl"}

_AQUI = os.path.dirname(os.path.abspath(__file__))
_CANDIDATOS = (os.path.join(_AQUI, "..", "..", "modelos", "glotlid", "model.bin"),
               os.path.join(_AQUI, "modelos", "glotlid", "model.bin"))

_modelo = None
_ruta = None


def backend():
    b = os.environ.get("LANG_ID", "glotlid").strip().lower()
    if b not in ("glotlid", "heuristica"):
        raise SystemExit(f"LANG_ID={b!r}: valores validos 'glotlid' o 'heuristica'")
    return b


def descripcion():
    """Lo que se guarda en cada reporte para saber con que se midio el idioma."""
    if backend() == "heuristica":
        return {"backend": "heuristica"}
    _cargar()
    return {"backend": "glotlid", "modelo": os.path.abspath(_ruta), "idiomas": list(IDIOMAS),
            "min_palabras": MIN_PALABRAS, "variedades": dict(VARIEDADES), "p_revisar": P_REVISAR,
            "revisar_siempre": list(REVISAR_SIEMPRE), "min_palabras_oracion": MIN_PALABRAS_ORACION}


def _cargar():
    global _modelo, _ruta
    if _modelo is not None:
        return _modelo
    ruta = os.environ.get("GLOTLID_MODEL") or next((c for c in _CANDIDATOS if os.path.exists(c)), None)
    if not ruta or not os.path.exists(ruta):
        raise SystemExit(
            "GlotLID: no encuentro model.bin. Opciones:\n"
            "  hf download cis-lmu/glotlid model.bin --local-dir modelos/glotlid   (desde la raiz del repo)\n"
            "  export GLOTLID_MODEL=/ruta/a/model.bin\n"
            "  export LANG_ID=heuristica   (solo para reproducir numeros viejos)")
    import fasttext
    fasttext.FastText.eprint = lambda *a, **k: None    # silencia el aviso de load_model
    _modelo, _ruta = fasttext.load_model(ruta), ruta
    print(f"[lang_id] GlotLID: {os.path.abspath(ruta)}")
    return _modelo


def palabras(text):
    return len(re.findall(r"[^\W\d_]+", str(text)))


def distribucion(text):
    """[(codigo, prob)] de TODOS los idiomas de GlotLID, de mayor a menor. Los
    codigos fuera de ISO3 quedan en ISO 639-3 (ext, ast, cbk...)."""
    t = " ".join(str(text).split())
    return list(_distribucion(t)) if t else []


@functools.lru_cache(maxsize=4096)
def _distribucion(t):
    # add_metrics pide veredicto y score del mismo texto: sin cache, 3 predicciones
    # f.predict y no predict: este ultimo rompe con numpy >= 2 (np.array(copy=False))
    pares = _cargar().f.predict(t + "\n", -1, 0.0, "strict")
    out = []
    for prob, lab in pares:
        iso3 = lab.replace("__label__", "").split("_")[0]
        out.append((ISO3.get(iso3, iso3), float(prob)))
    return tuple(out)


def _por_idioma(dist):
    """{codigo de IDIOMAS: probabilidad}, con VARIEDADES sumadas a su idioma."""
    acc = {}
    for c, q in dist:
        c = VARIEDADES.get(c, c)
        if c in IDIOMAS:
            acc[c] = acc.get(c, 0.0) + q
    return acc


def _elegir(text):
    """(lang, p, top1, p_top1) sin las marcas de revision."""
    dist = distribucion(text)
    if not dist:
        return "unknown", 0.0, None, 0.0
    top1, p_top1 = dist[0]
    acc = _por_idioma(dist)
    if not acc:
        return "unknown", 0.0, top1, p_top1
    lang = max(acc, key=acc.get)
    return lang, acc[lang], top1, p_top1


def oraciones(text):
    return [o for o in re.split(r"(?<=[.!?])\s+|\n+", str(text))
            if palabras(o) >= MIN_PALABRAS_ORACION]


def mezcla(text):
    """True si las oraciones largas del texto no salen todas en el mismo idioma."""
    ors = oraciones(text)
    if len(ors) < 2:
        return False
    return len({_elegir(o)[0] for o in ors} - {"unknown"}) > 1


def detectar(text):
    """
    {"lang", "p", "top1", "p_top1", "mezcla", "revisar"}.
    lang = idioma de IDIOMAS o 'unknown'; p = su probabilidad (con VARIEDADES
    sumadas); top1 / p_top1 = lo que dijo GlotLID sin la lista cerrada.
    """
    if palabras(text) < MIN_PALABRAS:
        return {"lang": "unknown", "p": 0.0, "top1": None, "p_top1": 0.0,
                "mezcla": False, "revisar": False}
    lang, p, top1, p_top1 = _elegir(text)
    mix = mezcla(text)
    top1_ok = top1 in IDIOMAS or top1 in VARIEDADES
    return {"lang": lang, "p": p, "top1": top1, "p_top1": p_top1, "mezcla": mix,
            "revisar": (not top1_ok) or p < P_REVISAR or lang in REVISAR_SIEMPRE or mix}


def score(text, lang):
    """Probabilidad de `lang` renormalizada sobre IDIOMAS, en [0, 1]. 0.5 si el
    texto es demasiado corto (indecidible), como el french_score viejo."""
    if palabras(text) < MIN_PALABRAS:
        return 0.5
    acc = _por_idioma(distribucion(text))
    tot = sum(acc.values())
    if tot == 0:
        return 0.5
    return acc.get(lang, 0.0) / tot
