"""
Checkers objetivos para el experimento de idiomas.

Dos metricas, ninguna basada en lexicon tematico:

1. compliance  -> el output esta en frances?      french_score / is_french
2. accuracy    -> el output contiene la respuesta correcta?  answer_correct

La accuracy funciona en ingles Y en frances porque las respuestas del dataset
son invariantes al idioma (nombres propios, numeros, simbolos quimicos) o
traen alias explicitos en questions.csv.
"""

import re
import unicodedata

import pandas as pd

# ---------------------------------------------------------------------------
# Normalizacion
# ---------------------------------------------------------------------------

_LIGATURES = {"œ": "oe", "Œ": "OE", "æ": "ae", "Æ": "AE"}


def strip_accents(s: str) -> str:
    """Quita acentos y expande ligaturas: 'coeur' <- 'cœur', 'Venus' <- 'Vénus'."""
    for lig, repl in _LIGATURES.items():
        s = s.replace(lig, repl)
    nfkd = unicodedata.normalize("NFKD", s)
    return "".join(c for c in nfkd if not unicodedata.combining(c))


def fold(s: str) -> str:
    """Normalizacion completa para comparar: sin acentos, minusculas."""
    return strip_accents(s).lower()


# ---------------------------------------------------------------------------
# Limpieza de fuga de rol
# ---------------------------------------------------------------------------

# El modelo cierra el turno con <|eot_id|> y arranca el siguiente. Al decodificar
# con skip_special_tokens=True los headers desaparecen pero el token de texto
# plano "assistant" queda, y aparecen varios turnos pegados:
#     "... est le Sahara.assistant\n\nVous voulez savoir plus sur le Sahara?"
# El corte primario es parar la generacion en <|eot_id|> (ver lm.stop_token_ids).
# Esto es la red de seguridad para cuando el parche suprime el eot.
_ROLE_LEAK = re.compile(r"(?:\n\s*|(?<=[.!?\u2026\"\'\)]))\s*assistant\b", re.IGNORECASE)


def truncate_at_role_leak(text: str) -> str:
    """Deja solo el primer turno. Idempotente sobre texto ya limpio."""
    m = _ROLE_LEAK.search(text)
    if m:
        text = text[: m.start()]
    return text.strip()


# ---------------------------------------------------------------------------
# Deteccion de idioma (frances vs ingles)
# ---------------------------------------------------------------------------

# Palabras funcionales que existen en UNO de los dos idiomas, no en ambos.
# Deliberadamente excluidas por ambiguas: on, or, an, a, en, son, pas de "no".
FR_WORDS = {
    "de", "et", "un", "en", "ce", "il", "si", "lui", "sous", "vers",
    "notre", "votre", "quand", "pendant", "apres", "avant", "depuis",
    "etait", "ont", "celle", "ceux", "autre", "autres", "bien", "encore",
    "deja", "ici", "quelques", "sen", "ses",
    "le", "la", "les", "des", "du", "une", "est", "sont", "dans", "pour",
    "avec", "qui", "que", "sur", "aussi", "cette", "ces", "nous", "vous",
    "ils", "elles", "aux", "par", "mais", "comme", "tout", "tres", "ne",
    "pas", "se", "sa", "ses", "leur", "leurs", "etre", "ete", "fait",
    "peut", "doit", "entre", "sans", "chez", "alors", "donc", "ainsi",
    "elle", "au", "cet", "celui", "dont", "lorsque", "plusieurs", "meme",
    "toujours", "beaucoup", "environ", "situe", "situee", "appele", "appelee",
}

EN_WORDS = {
    "the", "is", "are", "of", "and", "to", "in", "for", "with", "that",
    "this", "it", "you", "we", "they", "as", "but", "not", "have", "has",
    "was", "were", "from", "by", "at", "be", "which", "there", "their",
    "its", "can", "will", "would", "about", "more", "most", "one", "two",
    "known", "called", "also", "each", "such", "these", "those", "into",
}

_ACCENTED = set("àâäéèêëîïôöùûüçœ")


def _tokens(text: str):
    return re.findall(r"[a-z]+", fold(text))


def accent_rate(text: str) -> float:
    """Fraccion de caracteres acentuados. Senal secundaria de frances."""
    if not text:
        return 0.0
    return sum(1 for c in text.lower() if c in _ACCENTED) / len(text)


ACCENT_EVIDENCE = 2.0   # cuanto pesa "hay tildes" frente a una palabra funcional


def language_evidence(text: str):
    """
    (evidencia_frances, evidencia_ingles).

    Los acentos NO son un fallback sino evidencia ADICIONAL de frances: una
    respuesta corta como "La capitale du Chili est Santiago." tiene fr=3, en=0 y
    cero tildes, y eso ya alcanza para decidir. Tratar los acentos como
    reemplazo (la version anterior) tiraba esa evidencia y daba score 0.0 sobre
    frances perfecto.
    """
    toks = _tokens(text)
    fr = float(sum(1 for t in toks if t in FR_WORDS))
    en = float(sum(1 for t in toks if t in EN_WORDS))
    if accent_rate(text) >= 0.01:
        fr += ACCENT_EVIDENCE
    return fr, en


def french_score(text: str) -> float:
    """
    Score continuo en [0, 1]. 1.0 = frances, 0.0 = ingles.

    Devuelve 0.5 (indecidible) si no hay ninguna evidencia en ningun sentido,
    que es el caso de respuestas como "Paris." donde las dos lenguas coinciden.
    Usa language_verdict() si necesitas distinguir ese caso.
    """
    fr, en = language_evidence(text)
    if fr + en == 0:
        return 0.5
    return fr / (fr + en)


def language_verdict(text: str, threshold: float = 0.6, min_tokens: int = 3) -> str:
    """'fr' | 'en' | 'unknown'. Separa "respondio en ingles" de "muy corto para saber"."""
    if len(_tokens(text)) < min_tokens:
        return "unknown"
    fr, en = language_evidence(text)
    if fr + en == 0:
        return "unknown"
    score = fr / (fr + en)
    if score >= threshold:
        return "fr"
    if score <= 1.0 - threshold:
        return "en"
    return "unknown"


def is_french(text: str, threshold: float = 0.6, min_tokens: int = 3) -> bool:
    """Booleano de compliance."""
    return language_verdict(text, threshold, min_tokens) == "fr"


# ---------------------------------------------------------------------------
# Metricas para preguntas ABIERTAS (sin respuesta verificable)
# ---------------------------------------------------------------------------

def content_words(text: str) -> set:
    """Palabras de contenido: saca funcionales de ambos idiomas y tokens cortos."""
    return {t for t in _tokens(text)
            if len(t) >= 4 and t not in FR_WORDS and t not in EN_WORDS}


def content_overlap(a: str, b: str) -> float:
    """
    Jaccard sobre palabras de contenido.

    Para prompts abiertos no hay respuesta correcta, pero SI se puede comparar
    el output parcheado contra la referencia M([FR;q]): ambos son frances sobre
    la misma pregunta, asi que la comparacion es limpia (a diferencia de navidad,
    donde se comparaba contra un baseline en otro registro).
    """
    A, B = content_words(a), content_words(b)
    if not A or not B:
        return 0.0
    return len(A & B) / len(A | B)


def french_by_segments(text: str, n: int = 3):
    """
    french_score por tercio de la respuesta.

    El parche vive en 3 posiciones del PROMPT. Esto mide si su efecto sobrevive
    a lo largo de la generacion o si decae: francés al principio y deriva al
    ingles seria la firma de un efecto puramente local.
    """
    ws = text.split()
    if len(ws) < n * 4:
        return [french_score(text)] * n
    k = len(ws) // n
    seg = [" ".join(ws[i * k:(i + 1) * k]) for i in range(n - 1)]
    seg.append(" ".join(ws[(n - 1) * k:]))
    return [french_score(s) for s in seg]


# ---------------------------------------------------------------------------
# Accuracy: el output contiene la respuesta correcta?
# ---------------------------------------------------------------------------

_NUMERIC = re.compile(r"^[\d]+([.,][\d]+)?$")
_SYMBOL = re.compile(r"^[A-Z][a-z]?[0-9]?$")


def _candidate_matches(text: str, cand: str) -> bool:
    cand = cand.strip()
    if not cand:
        return False

    if _NUMERIC.match(cand):
        # Frontera numerica: "0" no debe matchear dentro de "100" ni "3" dentro
        # de "3.14", pero SI debe matchear "1989," con la coma pegada.
        pat = (r"(?<![\d.,])" + re.escape(cand) + r"(?!\d)(?![.,]\d)")
        return re.search(pat, text) is not None

    if _SYMBOL.match(cand) or len(cand) <= 2:
        # Simbolos quimicos: case-SENSITIVE y con frontera de palabra.
        # Critico en frances, donde "au" es una preposicion frecuente
        # y colisionaria con el simbolo del oro "Au".
        return re.search(r"\b" + re.escape(cand) + r"\b", text) is not None

    return fold(cand) in fold(text)


def answer_correct(text: str, answer: str, aliases: str = "") -> bool:
    """True si el texto contiene la respuesta correcta o alguno de sus alias."""
    cands = [answer] + [a for a in str(aliases).split("|") if a.strip()]
    return any(_candidate_matches(text, c) for c in cands)


# ---------------------------------------------------------------------------
# Dataset
# ---------------------------------------------------------------------------

def load_questions(path: str) -> pd.DataFrame:
    df = pd.read_csv(path, sep=";", keep_default_na=False)
    for col in ("prompt", "answer", "aliases"):
        if col not in df.columns:
            raise ValueError(f"{path} necesita la columna '{col}'")
    return df


if __name__ == "__main__":
    # Auto-test rapido de los checkers.
    cases_fr = [
        "Le mur de Berlin est tombe en 1989, un moment cle de l'histoire.",
        "La capitale de la France est Paris, qui est aussi la plus grande ville du pays.",
        "Le symbole chimique de l'or est Au, un metal precieux tres recherche.",
        "C'est une question interessante. Les plantes absorbent le CO2 dans l'air.",
    ]
    cases_en = [
        "The capital of France is Paris, which is also the largest city in the country.",
        "The chemical symbol for gold is Au, a precious metal that has been valued for ages.",
        "That is an interesting question. Plants absorb CO2 from the air for photosynthesis.",
    ]
    print("--- deteccion de idioma ---")
    for t in cases_fr:
        print(f"  FR esperado -> score={french_score(t):.2f} is_french={is_french(t)}  {t[:45]}...")
    for t in cases_en:
        print(f"  EN esperado -> score={french_score(t):.2f} is_french={is_french(t)}  {t[:45]}...")

    print("\n--- metricas de preguntas abiertas ---")
    a = "La photosynthese permet aux plantes de convertir la lumiere du soleil en energie chimique."
    b = "Les plantes utilisent la photosynthese pour transformer la lumiere solaire en energie."
    c = "Le moteur de la voiture brule du carburant pour produire un mouvement mecanique."
    print(f"  overlap(a,a) = {content_overlap(a, a):.3f}  (debe ser 1.0)")
    print(f"  overlap(a,b) = {content_overlap(a, b):.3f}  (mismo tema)")
    print(f"  overlap(a,c) = {content_overlap(a, c):.3f}  (temas distintos)")
    mixto = ("La photosynthese est un processus fondamental pour les plantes vertes. "
             "Elles captent la lumiere du soleil grace a la chlorophylle. "
             "Then the process continues and the plant uses the energy that it has stored.")
    print(f"  french_by_segments(texto que deriva al ingles) = "
          f"{[round(x, 2) for x in french_by_segments(mixto)]}")

    print("\n--- regresion: outputs reales del run de targets ---")
    reales_fr = [
        "C'est facile! 100 divise par 4 equivaut a 25.",
        "Le capitol de Kenya est Nairobi.",
        "La capitale du Chili est Santiago.",
        "Le symbole chimique du potassium est K.",
        "La capitale de la France est Paris.",
        "La capitale de la Norvege est Oslo.",
        "Le symbole chimique de l'acier est Fe.",
        "C'est Pablo Picasso qui a peint Guernica.",
        "Le plus grand desert chaud d'Afrique est le Sahara.",
        "L'Apollo 11 a atterri sur la Lune en 1969.",
        "Un hexagone a 6 cotes.",
        "C'est Uranus.",
        "Neuf carre est egal a 81.",
        "La formule chimique de l'eau est H2O.",
        "Le mur de Berlin a tombe en 1989.",
    ]
    reales_en = [
        "The capital of Kenya is Nairobi.",
        "The chemical symbol for gold is Au.",
        "The capital of France is Paris.",
        "A hexagon has 6 sides.",
        "The square root of 81 is 9.",
        "The chemical symbol for potassium is K.",
        "World War II ended in 1945. The war in Europe ended on May 8, 1945.",
        "The largest hot desert in Africa is the Sahara Desert, which covers 9,200,000 km2.",
    ]
    fr_ok = sum(1 for t in reales_fr if is_french(t))
    en_ok = sum(1 for t in reales_en if not is_french(t))
    print(f"  frances reconocido : {fr_ok}/{len(reales_fr)}")
    print(f"  ingles rechazado   : {en_ok}/{len(reales_en)}")
    for t in reales_fr:
        if not is_french(t):
            print(f"    FALLO FR: score={french_score(t):.2f} {t!r}")
    for t in reales_en:
        if is_french(t):
            print(f"    FALLO EN: score={french_score(t):.2f} {t!r}")
    print(f"  indecidibles: {[t for t in reales_fr + reales_en if language_verdict(t) == 'unknown']}")

    print("\n--- truncado de fuga de rol ---")
    leaks = [
        ("Le plus grand desert chaud d'Afrique est le Sahara.assistant\n\n"
         "Vous voulez savoir plus sur le Sahara?assistant\n\nOui, bien sur!",
         "Le plus grand desert chaud d'Afrique est le Sahara."),
        ("The largest hot desert is the Sahara Desert, including Morocco, and Tunisia.assistant\n\n"
         "Would you like to know more?",
         "The largest hot desert is the Sahara Desert, including Morocco, and Tunisia."),
        ("La capitale est Paris.", "La capitale est Paris."),                  # sin fuga: no toca
        ("Un assistant vocal repond aux questions.",                            # falso positivo?
         "Un assistant vocal repond aux questions."),
    ]
    ok_t = 0
    for raw, expected in leaks:
        got = truncate_at_role_leak(raw)
        flag = "OK " if got == expected else "FAIL"
        ok_t += got == expected
        print(f"  [{flag}] {got[:64]!r}")
    print(f"  {ok_t}/{len(leaks)} truncados correctos")
    print(f"  idempotente: {truncate_at_role_leak(truncate_at_role_leak(leaks[0][0])) == leaks[0][1]}")

    print("\n--- accuracy ---")
    checks = [
        ("La capitale de la France est Paris.", "Paris", "", True),
        ("La capitale de la France est Berlin.", "Paris", "", False),
        ("Le symbole chimique de l'or est Au.", "Au", "", True),
        ("Il est alle au marche avec le chien.", "Au", "", False),          # "au" != "Au"
        ("La temperature de congelation est de 0 degres.", "0", "zero", True),
        ("Le point d'ebullition est 100 degres.", "0", "zero", False),      # "0" dentro de "100"
        ("L'ocean le plus grand est le Pacifique.", "Pacific", "Pacifique", True),
        ("Le coeur pompe le sang.", "heart", "coeur", True),
        ("Le cœur pompe le sang.", "heart", "coeur", True),            # ligatura
        ("Sept fois huit egale cinquante-six.", "56", "cinquante-six", True),
        ("The Berlin Wall fell in 1989, a turning point.", "1989", "", True),   # coma pegada
        ("Le mur est tombe en 1989.", "1989", "", True),                        # punto pegado
        ("La valeur de pi est 3,14 environ.", "3.14", "3,14", True),
        ("La valeur de pi est 3,14 environ.", "3", "", False),                  # "3" dentro de "3,14"
        ("Il y a 100 degres.", "0", "zero", False),                             # "0" dentro de "100"
    ]
    ok = 0
    for text, ans, al, expected in checks:
        got = answer_correct(text, ans, al)
        flag = "OK " if got == expected else "FAIL"
        ok += got == expected
        print(f"  [{flag}] answer={ans!r} alias={al!r} -> {got} (esperado {expected})")
    print(f"\n{ok}/{len(checks)} checks de accuracy pasaron")
