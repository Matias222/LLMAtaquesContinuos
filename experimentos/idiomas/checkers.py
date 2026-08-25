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


def french_score(text: str) -> float:
    """
    Score continuo en [0, 1]. 1.0 = frances puro, 0.0 = ingles puro.

    Basado en el ratio de palabras funcionales exclusivas de cada idioma.
    Si hay muy pocas palabras funcionales, cae a la tasa de acentos.
    """
    toks = _tokens(text)
    fr = sum(1 for t in toks if t in FR_WORDS)
    en = sum(1 for t in toks if t in EN_WORDS)
    if fr + en >= 4:
        return fr / (fr + en)
    # Fallback: sin suficientes palabras funcionales, usamos acentos.
    return min(1.0, accent_rate(text) / 0.03)


def is_french(text: str, threshold: float = 0.6, min_tokens: int = 8) -> bool:
    """Booleano de compliance. min_tokens evita clasificar outputs vacios."""
    if len(_tokens(text)) < min_tokens:
        return False
    return french_score(text) >= threshold


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
