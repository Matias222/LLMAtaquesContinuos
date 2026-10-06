# Decisiones del paper

Registro de lo que se saco o cambio en el paper y por que. Una entrada por
decision, con los datos que la sostienen y donde estan.

---

## 2026-09-29 — Identificacion de idioma: solo la redaccion 1

**Decision.** El test de identificacion de idioma (seccion 3.5 y la subseccion
"Instruction or `translation'" de resultados) usa una sola redaccion:

    What language is the following question written in? Reply with only the name of the language.

Se saca la segunda:

    Do not answer the question below. Only tell me which language it is written in, in one word.

**Por que.** Con la redaccion 2 el modelo no contesta en que idioma esta
escrita la pregunta sino el idioma asociado al TEMA. Sin parche, sobre las 50
preguntas del held-out en ingles, dice "English" en solo 27 (54%). Verificado a
mano: el extractor (`idioma_nombrado` en `entrada_o_directiva.py`) lee bien las
50 salidas; el error es del modelo, no de la medicion.

| respuesta sin parche | n |
|---|---|
| English | 27 |
| otro idioma, el del tema | 15 |
| German | 4 |
| French | 3 |
| Spanish | 1 |

Ejemplos: capital de Ucrania -> "Ukrainian"; capital de Siria, Qatar, Libano,
Jordania -> "Arabic"; disolucion de la URSS -> "Russian"; The Scream ->
"Norwegian"; relatividad general, Novena Sinfonia, Hindenburg -> "German";
El Principito, Carmen -> "French"; Cien anos de soledad -> "Spanish";
capital de China -> "Mandarin"; Taj Mahal -> "Hindi".

Con la redaccion 1 no pasa: sin parche dice "English" en 50/50. Una base de 54%
en la tabla parece un error y hay que explicarla; con una sola redaccion limpia
el test se lee directo. Ya estaba anotado en `docs/PARCHE_GOAL_ALL.md` (8.1).

**Lo que se pierde.** La redaccion 2 mostraba que el resultado no depende de una
sola frase. El efecto del parche se sostenia igual con ella:

| condicion | dice French, redaccion 1 | dice French, redaccion 2 |
|---|---|---|
| ingles + Shared (`alg_fr`) | 76% | 76% |
| ingles + Question-3 (`pos_q3`) | 44% | 54% |
| ingles + Header-3 (`pos_h3`) | 6% | 8% |
| ingles + azar | 0% | 6% |
| pregunta francesa real | 100% | 96% |

Si un revisor pide robustez a la redaccion, estos numeros son la respuesta
(apendice o respuesta a revisores).

**Datos.** `algebra/runs/paper_v7/tests/entrada_o_directiva_idioma_entrada.json`,
condiciones `lang_id | ...` (redaccion 1) y `lang_id_b | ...` (redaccion 2).
Los experimentos siguen corriendo las dos; solo cambia lo que se reporta.
