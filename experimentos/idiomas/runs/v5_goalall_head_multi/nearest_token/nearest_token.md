# Vecino mas cercano de e + a*v (`runs/v5_goalall_head_multi/lang_patch_best_train.pt`)

||v|| 0.8228, ||e|| medio 1.0861, gap mediano 0.959

| vec | a | entrada | n_tok | cambia l2 | cambia cos | destinos l2 |
|---|---|---|---|---|---|---|
| v | 0.5 | prompt | 433 | 0.0% | 0.0% |  |
| v | 0.5 | prompt_es | 694 | 0.0% | 0.0% |  |
| v | 0.5 | prompt_de | 627 | 0.0% | 0.0% |  |
| v | 1 | prompt | 433 | 0.0% | 0.0% |  |
| v | 1 | prompt_es | 694 | 0.0% | 0.0% |  |
| v | 1 | prompt_de | 627 | 0.0% | 0.0% |  |
| v | 2 | prompt | 433 | 0.0% | 0.0% |  |
| v | 2 | prompt_es | 694 | 0.0% | 0.0% |  |
| v | 2 | prompt_de | 627 | 0.0% | 0.0% |  |
| v | 4 | prompt | 433 | 0.0% | 0.0% |  |
| v | 4 | prompt_es | 694 | 0.0% | 0.0% |  |
| v | 4 | prompt_de | 627 | 0.0% | 0.0% |  |
| v | 8 | prompt | 433 | 17.1% | 17.8% | `无码`×50, `Around`×1, `Sun`×1, `Old`×1, `Human`×1 |
| v | 8 | prompt_es | 694 | 17.3% | 18.6% | `无码`×109, `Sol`×1, `Sir`×1, `她的`×1, `Hum`×1 |
| v | 8 | prompt_de | 627 | 11.5% | 11.5% | `无码`×59, `Son`×2, `Mal`×1, `Human`×1, `Sch`×1 |
| rand | 0.5 | prompt | 433 | 0.0% | 0.0% |  |
| rand | 0.5 | prompt_es | 694 | 0.0% | 0.0% |  |
| rand | 0.5 | prompt_de | 627 | 0.0% | 0.0% |  |
| rand | 1 | prompt | 433 | 0.0% | 0.0% |  |
| rand | 1 | prompt_es | 694 | 0.0% | 0.0% |  |
| rand | 1 | prompt_de | 627 | 0.0% | 0.0% |  |
| rand | 2 | prompt | 433 | 0.0% | 0.0% |  |
| rand | 2 | prompt_es | 694 | 0.0% | 0.0% |  |
| rand | 2 | prompt_de | 627 | 0.0% | 0.0% |  |
| rand | 4 | prompt | 433 | 0.0% | 0.0% |  |
| rand | 4 | prompt_es | 694 | 0.0% | 0.0% |  |
| rand | 4 | prompt_de | 627 | 0.0% | 0.0% |  |
| rand | 8 | prompt | 433 | 0.2% | 0.0% | `Selection`×1 |
| rand | 8 | prompt_es | 694 | 0.0% | 0.0% |  |
| rand | 8 | prompt_de | 627 | 0.0% | 0.0% |  |

## prompt  (a=1, parche v)

| # | original | vecino l2 | vecino cos |
|---|---|---|---|
| 200 | What is the capital of Ukraine? | What is the capital of Ukraine? | What is the capital of Ukraine? |
| 201 | What force keeps planets in orbit around the Sun? | What force keeps planets in orbit around the Sun? | What force keeps planets in orbit around the Sun? |
| 202 | Who wrote The Old Man and the Sea? | Who wrote The Old Man and the Sea? | Who wrote The Old Man and the Sea? |
| 203 | What is the capital of Syria? | What is the capital of Syria? | What is the capital of Syria? |
| 204 | In what year did the Wright brothers first fly? | In what year did the Wright brothers first fly? | In what year did the Wright brothers first fly? |
| 205 | In what year did the Human Genome Project publish its first draft? | In what year did the Human Genome Project publish its first draft? | In what year did the Human Genome Project publish its first draft? |
| 206 | What is the chemical symbol for platinum? | What is the chemical symbol for platinum? | What is the chemical symbol for platinum? |
| 207 | In what year did Germany reunify? | In what year did Germany reunify? | In what year did Germany reunify? |
| 208 | Who developed the theory of natural selection alongside Darwin? | Who developed the theory of natural selection alongside Darwin? | Who developed the theory of natural selection alongside Darwin? |
| 209 | In what year did the Soviet Union dissolve? | In what year did the Soviet Union dissolve? | In what year did the Soviet Union dissolve? |

## prompt_es  (a=1, parche v)

| # | original | vecino l2 | vecino cos |
|---|---|---|---|
| 200 | ¿Cuál es la capital de Ucrania? | ¿Cuál es la capital de Ucrania? | ¿Cuál es la capital de Ucrania? |
| 201 | ¿Qué fuerza mantiene a los planetas en órbita alrededor del Sol? | ¿Qué fuerza mantiene a los planetas en órbita alrededor del Sol? | ¿Qué fuerza mantiene a los planetas en órbita alrededor del Sol? |
| 202 | ¿Quién escribió El viejo y el mar? | ¿Quién escribió El viejo y el mar? | ¿Quién escribió El viejo y el mar? |
| 203 | ¿Cuál es la capital de Siria? | ¿Cuál es la capital de Siria? | ¿Cuál es la capital de Siria? |
| 204 | ¿En qué año volaron por primera vez los hermanos Wright? | ¿En qué año volaron por primera vez los hermanos Wright? | ¿En qué año volaron por primera vez los hermanos Wright? |
| 205 | ¿En qué año publicó el Proyecto del Genoma Humano su primer borrador? | ¿En qué año publicó el Proyecto del Genoma Humano su primer borrador? | ¿En qué año publicó el Proyecto del Genoma Humano su primer borrador? |
| 206 | ¿Cuál es el símbolo químico de platino? | ¿Cuál es el símbolo químico de platino? | ¿Cuál es el símbolo químico de platino? |
| 207 | ¿En qué año se reunió Alemania? | ¿En qué año se reunió Alemania? | ¿En qué año se reunió Alemania? |
| 208 | ¿Quién desarrolló la teoría de la selección natural junto a Darwin? | ¿Quién desarrolló la teoría de la selección natural junto a Darwin? | ¿Quién desarrolló la teoría de la selección natural junto a Darwin? |
| 209 | ¿En qué año se disolvió la Unión Soviética? | ¿En qué año se disolvió la Unión Soviética? | ¿En qué año se disolvió la Unión Soviética? |

## prompt_de  (a=1, parche v)

| # | original | vecino l2 | vecino cos |
|---|---|---|---|
| 200 | Was ist die Hauptstadt der Ukraine? | Was ist die Hauptstadt der Ukraine? | Was ist die Hauptstadt der Ukraine? |
| 201 | Welche Kraft hält die Planeten in ihrer Umlaufbahn um die Sonne? | Welche Kraft hält die Planeten in ihrer Umlaufbahn um die Sonne? | Welche Kraft hält die Planeten in ihrer Umlaufbahn um die Sonne? |
| 202 | Wer hat "Der alte Mann und das Meer" geschrieben? | Wer hat "Der alte Mann und das Meer" geschrieben? | Wer hat "Der alte Mann und das Meer" geschrieben? |
| 203 | Was ist die Hauptstadt von Syrien? | Was ist die Hauptstadt von Syrien? | Was ist die Hauptstadt von Syrien? |
| 204 | Was ist das Jahr, in dem die Wright-Brüder zum ersten Mal flogen? | Was ist das Jahr, in dem die Wright-Brüder zum ersten Mal flogen? | Was ist das Jahr, in dem die Wright-Brüder zum ersten Mal flogen? |
| 205 | In welchem Jahr veröffentlichte das Human-Genom-Projekt seinen ersten Entwurf? | In welchem Jahr veröffentlichte das Human-Genom-Projekt seinen ersten Entwurf? | In welchem Jahr veröffentlichte das Human-Genom-Projekt seinen ersten Entwurf? |
| 206 | Was ist das chemische Symbol für Platin? | Was ist das chemische Symbol für Platin? | Was ist das chemische Symbol für Platin? |
| 207 | Was ist das Jahr der Wiedervereinigung Deutschlands? | Was ist das Jahr der Wiedervereinigung Deutschlands? | Was ist das Jahr der Wiedervereinigung Deutschlands? |
| 208 | Wer hat die Theorie der natürlichen Selektion neben Darwin entwickelt? | Wer hat die Theorie der natürlichen Selektion neben Darwin entwickelt? | Wer hat die Theorie der natürlichen Selektion neben Darwin entwickelt? |
| 209 | Was ist das Jahr, in dem die Sowjetunion aufgelöst wurde? | Was ist das Jahr, in dem die Sowjetunion aufgelöst wurde? | Was ist das Jahr, in dem die Sowjetunion aufgelöst wurde? |
