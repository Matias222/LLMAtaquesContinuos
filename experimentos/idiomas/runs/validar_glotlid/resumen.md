# GlotLID contra la heuristica de checkers.py

Modelo: `../../modelos/glotlid/model.bin`. Regla sin idioma: `none` si palabras < min_words o confianza top-1 < umbral.
Mejor regla (por concordancia en `manual`): umbral 0.0, min_words 3.

| conjunto | n | heuristica | GlotLID sin regla | GlotLID mejor regla |
|---|---|---|---|---|
| manual | 450 | 0.960 | 0.976 | 0.982 |
| referencia | 1098 | 0.957 | 0.975 | 0.967 |

## Grilla (concordancia)

| umbral | min_words | manual | referencia |
|---|---|---|---|
| 0.0 | 0 | 0.976 | 0.975 |
| 0.0 | 1 | 0.976 | 0.975 |
| 0.0 | 2 | 0.976 | 0.968 |
| 0.0 | 3 | 0.982 | 0.967 |
| 0.3 | 0 | 0.978 | 0.975 |
| 0.3 | 1 | 0.978 | 0.975 |
| 0.3 | 2 | 0.978 | 0.968 |
| 0.3 | 3 | 0.982 | 0.967 |
| 0.5 | 0 | 0.980 | 0.972 |
| 0.5 | 1 | 0.980 | 0.972 |
| 0.5 | 2 | 0.980 | 0.964 |
| 0.5 | 3 | 0.982 | 0.964 |
| 0.7 | 0 | 0.967 | 0.955 |
| 0.7 | 1 | 0.967 | 0.955 |
| 0.7 | 2 | 0.967 | 0.948 |
| 0.7 | 3 | 0.969 | 0.947 |
| 0.9 | 0 | 0.936 | 0.908 |
| 0.9 | 1 | 0.936 | 0.908 |
| 0.9 | 2 | 0.936 | 0.901 |
| 0.9 | 3 | 0.936 | 0.901 |

## `manual`: concordancia por etiqueta

| etiqueta | n | heuristica | GlotLID |
|---|---|---|---|
| es | 145 | 0.99 | 0.97 |
| de | 141 | 0.99 | 1.00 |
| fr | 100 | 1.00 | 1.00 |
| en | 39 | 0.95 | 0.97 |
| ca | 10 | 0.00 | 1.00 |
| it | 8 | 0.75 | 1.00 |
| none | 5 | 1.00 | 0.60 |
| sv | 1 | 0.00 | 1.00 |
| nl | 1 | 0.00 | 1.00 |

Matriz de confusion GlotLID (`manual`; filas = etiqueta, columnas = prediccion):

| | ast | ca | de | en | es | ext | fr | it | nl | no | none | sv |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **ca** |  | 10 |  |  |  |  |  |  |  |  |  |  |
| **de** |  |  | 141 |  |  |  |  |  |  |  |  |  |
| **en** |  |  |  | 38 |  |  | 1 |  |  |  |  |  |
| **es** | 1 |  |  |  | 140 | 4 |  |  |  |  |  |  |
| **fr** |  |  |  |  |  |  | 100 |  |  |  |  |  |
| **it** |  |  |  |  |  |  |  | 8 |  |  |  |  |
| **nl** |  |  |  |  |  |  |  |  | 1 |  |  |  |
| **none** |  |  |  |  |  |  | 1 |  |  | 1 | 3 |  |
| **sv** |  |  |  |  |  |  |  |  |  |  |  | 1 |

## `referencia`: concordancia por etiqueta

| etiqueta | n | heuristica | GlotLID |
|---|---|---|---|
| es | 250 | 0.97 | 0.97 |
| de | 250 | 0.98 | 1.00 |
| fr | 249 | 0.98 | 0.99 |
| en | 249 | 1.00 | 1.00 |
| it | 50 | 0.84 | 0.90 |
| pt | 50 | 0.56 | 0.60 |

Matriz de confusion GlotLID (`referencia`; filas = etiqueta, columnas = prediccion):

| | ca | cbk | de | en | es | ext | fr | it | lij | none | pt | sco |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **de** |  |  | 249 |  |  |  |  |  |  |  |  | 1 |
| **en** |  |  |  | 249 |  |  |  |  |  |  |  |  |
| **es** | 3 | 1 |  |  | 242 | 4 |  |  |  |  |  |  |
| **fr** | 1 |  |  |  |  |  | 247 |  | 1 |  |  |  |
| **it** |  |  |  |  |  |  |  | 45 |  | 5 |  |  |
| **pt** |  |  |  |  |  |  |  | 1 |  | 19 | 30 |  |

