# Validacion del detector de idioma

Modelo: `/mnt/custom-file-systems/efs/fs-0ded2930a619aa967_fsap-0faa05c681ed1a8f3/papers/LLMAtaquesContinuos/modelos/glotlid/model.bin`. Lista cerrada: fr, en, es, de, it, pt, ca, nl, sv, no, da, ro, gl. Sin idioma: menos de 3 palabras. `revisar`: top-1 fuera de la lista o p < 0.5.

| conjunto | n | heuristica | glotlid_top1 | lang_id | errores lang_id | marcados revisar | errores atrapados por revisar |
|---|---|---|---|---|---|---|---|
| manual | 450 | 0.960 | 0.982 | 0.993 | 3 | 5 | 0/3 |
| referencia | 1098 | 0.979 | 0.989 | 0.994 | 7 | 12 | 3/7 |

## `manual`: concordancia por etiqueta

| etiqueta | n | heuristica | glotlid_top1 | lang_id |
|---|---|---|---|---|
| es | 145 | 0.99 | 0.97 | 1.00 |
| de | 141 | 0.99 | 1.00 | 1.00 |
| fr | 100 | 1.00 | 1.00 | 1.00 |
| en | 39 | 0.95 | 0.97 | 0.97 |
| ca | 10 | 0.00 | 1.00 | 1.00 |
| it | 8 | 0.75 | 1.00 | 1.00 |
| none | 5 | 1.00 | 0.60 | 0.60 |
| sv | 1 | 0.00 | 1.00 | 1.00 |
| nl | 1 | 0.00 | 1.00 | 1.00 |

Matriz de confusion de lang_id (`manual`; filas = etiqueta, columnas = prediccion):

| | ca | de | en | es | fr | it | nl | no | none | sv |
|---|---|---|---|---|---|---|---|---|---|---|
| **ca** | 10 |  |  |  |  |  |  |  |  |  |
| **de** |  | 141 |  |  |  |  |  |  |  |  |
| **en** |  |  | 38 |  | 1 |  |  |  |  |  |
| **es** |  |  |  | 145 |  |  |  |  |  |  |
| **fr** |  |  |  |  | 100 |  |  |  |  |  |
| **it** |  |  |  |  |  | 8 |  |  |  |  |
| **nl** |  |  |  |  |  |  | 1 |  |  |  |
| **none** |  |  |  |  | 1 |  |  | 1 | 3 |  |
| **sv** |  |  |  |  |  |  |  |  |  | 1 |

## `referencia`: concordancia por etiqueta

| etiqueta | n | heuristica | glotlid_top1 | lang_id |
|---|---|---|---|---|
| es | 250 | 0.97 | 0.97 | 0.98 |
| de | 250 | 0.98 | 1.00 | 1.00 |
| fr | 249 | 0.98 | 0.99 | 1.00 |
| en | 249 | 1.00 | 1.00 | 1.00 |
| it | 45 | 0.93 | 1.00 | 1.00 |
| pt | 31 | 0.90 | 0.97 | 0.97 |
| none | 24 | 1.00 | 1.00 | 1.00 |

Matriz de confusion de lang_id (`referencia`; filas = etiqueta, columnas = prediccion):

| | ca | de | en | es | fr | it | none | pt |
|---|---|---|---|---|---|---|---|---|
| **de** |  | 250 |  |  |  |  |  |  |
| **en** |  |  | 249 |  |  |  |  |  |
| **es** | 5 |  |  | 245 |  |  |  |  |
| **fr** | 1 |  |  |  | 248 |  |  |  |
| **it** |  |  |  |  |  | 45 |  |  |
| **none** |  |  |  |  |  |  | 24 |  |
| **pt** |  |  |  |  |  | 1 |  | 30 |

