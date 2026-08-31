# Revision manual de la columna `prompt_fr` (250 preguntas)

Revisadas las 250 filas una por una. Los errores se agrupan por si **rompen el
benchmark** (la pregunta francesa ya no es la misma pregunta) o si son ruido
cosmetico.

## Resumen

| categoria | n | rompe el benchmark? | lo atrapa `prompt_fr_ok`? |
|---|---|---|---|
| A. Fuga del few-shot | 8 | si, total | **no, pasan las 8** |
| B. Cambia el referente de la pregunta | 7 | si, la respuesta cambia | **no, pasan las 7** |
| C. La traduccion contiene la respuesta | 1 | si | si (unica atrapada) |
| D. Titulos de obras mal traducidos | 6 | parcial | no |
| E. Alucinacion de contenido | 1 | si | no |
| F. Palabra dejada en ingles | 8 | no | no |
| G. Genero / concordancia / sintaxis | ~12 | no | no |

**16 preguntas quedan inutilizables** (A + B + C), y **15 de ellas tienen
`prompt_fr_ok = True`**. Sumando D y E son 23 filas con un problema de contenido
real sobre 250 → **9.2%**.

---

## A. Fuga del few-shot — 8 casos

El `TEMPLATE` de `translate_questions.py` trae tres ejemplos. Cuando el modelo no
engancha el patron, **copia la respuesta del primer ejemplo** en vez de traducir:

```
English: What is the capital of Japan?
French: Quelle est la capitale du Japon ?      <-- esto es lo que sale
```

| # | pregunta original | prompt_fr | ok? |
|---|---|---|---|
| 2 | On which continent is the Amazon rainforest located? | Quelle est la capitale du Japon? | True |
| 37 | In which country is Machu Picchu located? | Quelle est la capitale du Japon? | True |
| 40 | What is the capital of Iraq? | Quelle est la capitale du Japon? | True |
| 53 | What is the powerhouse of the cell? | Quelle est la capitale du Japon? | True |
| 157 | Which strait separates Spain from Morocco? | Quelle est la capitale du Japon? | True |
| 184 | In which country is the Great Barrier Reef located? | Quelle est la capitale du Japon? | True |
| 238 | In which city is the Taj Mahal located? | Quelle est la capitale du Japon? | True |
| 244 | Who composed the opera Carmen? | Qui a ecrit Hamlet? | True |

**El patron es nitido**: 5 de las 8 son preguntas de forma `In which / On which
... located?` o `Which strait ...?`, que es justo la forma que **no** aparece en
el few-shot (los tres ejemplos son `What is the capital of`, `Who wrote` y
`How does ... work`). El caso 244 cae al **segundo** ejemplo porque empieza con
"Who composed", cerca de "Who wrote".

Las 250 preguntas incluyen 5 de forma `In/On which ... located`, y **las 5 fallan**.
No es aleatorio: es cobertura del template.

## B. Cambia el referente — 7 casos

La traduccion es frances valido y bien formado, pero pregunta **otra cosa**. La
respuesta esperada del CSV ya no corresponde.

| # | pregunta original | prompt_fr | que pregunta ahora | answer del CSV |
|---|---|---|---|---|
| 49 | What is the **boiling** point of water...? | Quel est le **point de fusion** de l'eau...? | punto de **fusion** | 100 (deberia ser 0) |
| 162 | At what temperature does water reach its **maximum density**? | Quel est le **point de fusion** de l'eau en degrés Celsius? | punto de **fusion** | 4 (deberia ser 0) |
| 208 | What is the chemical symbol for **platinum**? | Quel est le symbole chimique de **l'or**? | simbolo del **oro** | Pt (deberia ser Au) |
| 138 | What is the capital of **Belarus**? | Quelle est la capitale de la **Belgique**? | capital de **Belgica** | Minsk (deberia ser Bruxelles) |
| 58 | **How many** planets are in the Solar System? | **Quels sont** les planètes du système solaire? | *cuales* son, no *cuantos* | 8 |
| 200 | What is the chemical symbol for **iron**? | Quel est le symbole chimique de **l'acier**? | simbolo del **acero** | Fe |
| 232 | How many **keys** does a standard piano have? | Quel est le nombre de **claviers**...? | cuantos **teclados** (=1) | 88 |

Las dos de `point de fusion` (49 y 162) son especialmente malas: **dos preguntas
distintas colapsan en la misma traduccion**, y ninguna de las dos es la original.

Nota: el error de `acier` por `fer` (200) tambien esta en la columna `output` de
referencia (*"Le symbole chimique de l'acier est Fe"*), asi que viene del modelo,
no de la traduccion.

## C. La traduccion filtra la respuesta — 1 caso

| # | pregunta | prompt_fr | ok? |
|---|---|---|---|
| — | What is the name of Earth's only natural satellite? | Quel est le nom de la **lune** naturelle de la Terre? | **False** |

Unico error que el gate atrapa, y lo atrapa por la regla correcta
("contiene la respuesta"). El resto se le escapa entero.

## D. Titulos de obras — 6 casos

| pregunta | prompt_fr | correcto |
|---|---|---|
| Crime and Punishment | Crime et **Chagrin de Punir** | Crime et Châtiment |
| The Last Supper | Le Dernier **Supper** | La Cène |
| Brave New World | le **monde nouveau vaillant** | Le Meilleur des mondes |
| War and Peace | **la Paix et la Guerre** (invertido) | La Guerre et la Paix |
| The Divine Comedy | La **Comédie divine** | La Divine Comédie |
| Don Quixote | Don **Quixote** (sin traducir) | Don Quichotte |

## E. Alucinacion de contenido — 1 caso

| pregunta | prompt_fr |
|---|---|
| How many elements are in the periodic table **as of today**, approximately? | ...dans la table périodique **au 1er mars 2023**, d'approximation? |

Inventa una fecha que no esta en el original.

## F. Palabra dejada en ingles — 8 casos

`l'Iceland` (→ l'Islande), `du tin` (→ étain), `du chromium` (→ chrome),
`du Jordan` (→ Jordanie), `le penicillin` (→ la pénicilline), `au soccer`
(→ football), `les trois lois de la motion` (→ du mouvement), `Don Quixote`.

No cambian la respuesta esperada; si contaminan la señal, porque la pregunta
"francesa" tiene tokens ingleses justo donde se mide el emparejamiento de idioma.

## G. Genero, concordancia y sintaxis — ~12 casos

`du Norvège`, `du Malaisie`, `du Tanzanie`, `du Jordan`, `la plus petite pays`,
`le plus grand planète`, `Quel planète`, `le plus dur des substances`,
`le plus grand organ`, `Quel continent est l'Égypte principalement située dans?`,
`Quel an est-ce que la muraille de Berlin a tombé?`, `Quel est l'année` (deberia
ser `Quelle`, aparece en ~20 filas de fecha).

Cosmetico para el benchmark, pero vale saber que la pregunta "francesa" no es
frances nativo del todo.

---

## Por que el gate no atrapa nada de esto

`check_translation()` en `checkers.py` aplica cinco filtros:

1. `len(tgt.split()) < 2` → vacia
2. `fold(tgt) == fold(src_q)` → eco del ingles
3. `language_verdict(tgt) in ("en","es")` → quedo en otro idioma
4. la fuente termina en `?` y el target no
5. `answer_correct(tgt, answer, aliases)` → es una respuesta, no una traduccion

"Quelle est la capitale du Japon?" pasa los cinco: tiene 6 palabras, no es el eco
del ingles, es frances, termina en `?`, y no contiene "South America" ni
"Amerique du Sud".

**Falta el filtro obvio: que la traduccion hable de lo mismo que la fuente.**

Lo minimo que lo arregla — sin modelo extra, solo comparando cadenas:

- **Nombres propios y numeros**: extraer de la fuente los tokens capitalizados que
  no son la primera palabra (`Amazon`, `Machu Picchu`, `Iraq`, `Morocco`,
  `Taj Mahal`, `Carmen`, `Belarus`, `platinum`) y los digitos, y exigir que cada
  uno aparezca en el target o en su traduccion conocida. Atrapa **las 8 fugas del
  few-shot y 3 de las 7 del grupo B** de una.
- **Overlap de contenido minimo**: `content_overlap(src, tgt)` con las funcionales
  de los dos idiomas ya fuera (la funcion ya existe en `checkers.py`). Las fugas
  dan overlap ~0 contra un ~0.2-0.4 tipico de una traduccion real.
- **Blacklist de las 3 respuestas del few-shot**: rechazo directo si el target es
  igual a alguna, salvo que la fuente sea justo esa pregunta. Dos lineas, cubre
  el grupo A entero.

Ademas, para el grupo B lo unico que funciona es una vuelta inversa: retraducir
`prompt_fr` al ingles y comparar con la fuente. `point de fusion` vuelve como
"melting point" y no matchea "boiling point".
