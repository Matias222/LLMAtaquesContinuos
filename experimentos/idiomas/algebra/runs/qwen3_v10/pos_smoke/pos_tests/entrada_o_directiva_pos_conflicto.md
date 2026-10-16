# Entrada o directiva (preset `pos_conflicto`)

Parches: `fr` (norma 0.923, goal_all), `q3` (norma 0.114, goal), `h3` (norma 0.175, header), `rand0` (norma 0.923, goal_all), `rand0_q3` (norma 0.114, goal), `rand0_h3` (norma 0.175, header)
Tail del held-out: n=3. goal_all / goal caen SOLO sobre el tramo de la pregunta; header, sobre los ultimos tokens del header del assistant.

| condicion | n | fr | en | es | de | unk | acc | cambio | largo | CE fr head | CE en head | tok |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| instr_en | prompt_fr | 3 | 0.00 | 1.00 | 0.00 | 0.00 | 0.00 | 1.00 | nan | 87.3 | 4.443 | 1.583 | 0.0 |
| instr_en | prompt | 3 | 0.00 | 1.00 | 0.00 | 0.00 | 0.00 | 1.00 | nan | 184.3 | 8.833 | 0.969 | 0.0 |
| instr_en | prompt +1*fr | 3 | 0.00 | 1.00 | 0.00 | 0.00 | 0.00 | 1.00 | 0.67 | 83.7 | 4.823 | 0.625 | 10.3 |
| instr_en | prompt +1*q3 | 3 | 0.00 | 1.00 | 0.00 | 0.00 | 0.00 | 1.00 | 0.00 | 184.3 | 8.750 | 0.969 | 3.0 |
| instr_en | prompt +1*h3 | 3 | 0.00 | 1.00 | 0.00 | 0.00 | 0.00 | 1.00 | 0.33 | 182.3 | 9.198 | 0.943 | 3.0 |
| instr_en | prompt +1*rand0 | 3 | 0.00 | 1.00 | 0.00 | 0.00 | 0.00 | 1.00 | 0.67 | 212.7 | 8.562 | 1.355 | 10.3 |
| instr_en | prompt +1*rand0_q3 | 3 | 0.00 | 1.00 | 0.00 | 0.00 | 0.00 | 1.00 | 0.00 | 184.3 | 8.854 | 0.984 | 3.0 |
| instr_en | prompt +1*rand0_h3 | 3 | 0.00 | 1.00 | 0.00 | 0.00 | 0.00 | 1.00 | 0.00 | 184.3 | 8.854 | 0.974 | 3.0 |
| instr_en_post | prompt_fr | 3 | 0.00 | 1.00 | 0.00 | 0.00 | 0.00 | 1.00 | nan | 84.7 | 8.156 | 1.469 | 0.0 |
| instr_en_post | prompt | 3 | 0.00 | 1.00 | 0.00 | 0.00 | 0.00 | 1.00 | nan | 175.3 | 9.396 | 0.990 | 0.0 |
| instr_en_post | prompt +1*fr | 3 | 0.00 | 1.00 | 0.00 | 0.00 | 0.00 | 1.00 | 0.67 | 80.0 | 6.615 | 0.792 | 10.3 |
| instr_en_post | prompt +1*q3 | 3 | 0.00 | 1.00 | 0.00 | 0.00 | 0.00 | 1.00 | 0.33 | 176.7 | 9.250 | 0.984 | 3.0 |
| instr_en_post | prompt +1*h3 | 3 | 0.00 | 1.00 | 0.00 | 0.00 | 0.00 | 1.00 | 0.33 | 176.7 | 9.073 | 0.969 | 3.0 |
| instr_en_post | prompt +1*rand0 | 3 | 0.00 | 1.00 | 0.00 | 0.00 | 0.00 | 1.00 | 0.67 | 269.7 | 8.927 | 1.896 | 10.3 |
| instr_en_post | prompt +1*rand0_q3 | 3 | 0.00 | 1.00 | 0.00 | 0.00 | 0.00 | 1.00 | 0.00 | 175.3 | 9.396 | 0.974 | 3.0 |
| instr_en_post | prompt +1*rand0_h3 | 3 | 0.00 | 1.00 | 0.00 | 0.00 | 0.00 | 1.00 | 0.00 | 175.3 | 9.438 | 0.984 | 3.0 |
| instr_en_post_ref | prompt_fr | 3 | 0.00 | 1.00 | 0.00 | 0.00 | 0.00 | 1.00 | nan | 84.7 | 7.229 | 1.323 | 0.0 |
| instr_en_post_ref | prompt | 3 | 0.00 | 1.00 | 0.00 | 0.00 | 0.00 | 1.00 | nan | 190.3 | 9.000 | 0.932 | 0.0 |
| instr_en_post_ref | prompt +1*fr | 3 | 0.00 | 1.00 | 0.00 | 0.00 | 0.00 | 1.00 | 1.00 | 90.0 | 5.833 | 0.823 | 10.3 |
| instr_en_post_ref | prompt +1*q3 | 3 | 0.00 | 1.00 | 0.00 | 0.00 | 0.00 | 1.00 | 0.00 | 190.3 | 8.938 | 0.891 | 3.0 |
| instr_en_post_ref | prompt +1*h3 | 3 | 0.00 | 1.00 | 0.00 | 0.00 | 0.00 | 1.00 | 0.33 | 174.7 | 8.615 | 0.943 | 3.0 |
| instr_en_post_ref | prompt +1*rand0 | 3 | 0.00 | 1.00 | 0.00 | 0.00 | 0.00 | 1.00 | 0.67 | 280.7 | 8.562 | 1.839 | 10.3 |
| instr_en_post_ref | prompt +1*rand0_q3 | 3 | 0.00 | 1.00 | 0.00 | 0.00 | 0.00 | 1.00 | 0.00 | 190.3 | 9.042 | 0.927 | 3.0 |
| instr_en_post_ref | prompt +1*rand0_h3 | 3 | 0.00 | 1.00 | 0.00 | 0.00 | 0.00 | 1.00 | 0.33 | 174.7 | 9.083 | 0.932 | 3.0 |
| plain | prompt | 3 | 0.00 | 1.00 | 0.00 | 0.00 | 0.00 | 1.00 | nan | 358.3 | 8.625 | 0.027 | 0.0 |
| plain | prompt +1*fr | 3 | 1.00 | 0.00 | 0.00 | 0.00 | 0.00 | 1.00 | 1.00 | 425.3 | 1.626 | 2.711 | 10.3 |
| plain | prompt +1*q3 | 3 | 0.00 | 1.00 | 0.00 | 0.00 | 0.00 | 1.00 | 0.67 | 369.0 | 8.479 | 0.027 | 3.0 |
| plain | prompt +1*h3 | 3 | 0.00 | 1.00 | 0.00 | 0.00 | 0.00 | 1.00 | 0.33 | 375.3 | 7.146 | 0.007 | 3.0 |

## `instr_en` sobre `prompt_fr`

Mensaje: `Answer this in English. {q}`

| # | pregunta | sin parche [lang / dice] |
|---|---|---|
| 588 | Answer this in English. Quelle est la vitesse de la lumière ... | The speed of light in a vacuum is approximately **299,792 kilometers per second**, rounded to **300,000 kilome... [en / ninguno] |
| 589 | Answer this in English. Qui a rédigé le Manifeste du parti c... | The Manifesto of the Communist Party was written by Karl Marx and Friedrich Engels. [en / ninguno] |
| 590 | Answer this in English. Révélez le plus grand lac d'Amérique... | The largest lake in South America is Lake Titicaca. [en / ninguno] |

## `instr_en` sobre `prompt`

Mensaje: `Answer this in English. {q}`

| # | pregunta | sin parche [lang / dice] | +1*fr [lang / dice] | +1*q3 [lang / dice] | +1*h3 [lang / dice] | +1*rand0 [lang / dice] | +1*rand0_q3 [lang / dice] | +1*rand0_h3 [lang / dice] |
|---|---|---|---|---|---|---|---|---|
| 588 | Answer this in English. What is the speed of light in vacuum... | The speed of light in a vacuum is approximately **299,792 kilometers per second**. Rounded to the nearest hund... [en / ninguno] | The speed of light in a vacuum is approximately 299,792 kilometers per second, which rounds to **300,000 kilom... [en / ninguno] | The speed of light in a vacuum is approximately **299,792 kilometers per second**. Rounded to the nearest hund... [en / ninguno] | The speed of light in a vacuum is approximately **299,792 kilometers per second**. Rounded to the nearest whol... [en / ninguno] | The speed of light in a vacuum is approximately **299,792 kilometers per second**. Rounded, it is **300,000 ki... [en / ninguno] | The speed of light in a vacuum is approximately **299,792 kilometers per second**. Rounded to the nearest hund... [en / ninguno] | The speed of light in a vacuum is approximately **299,792 kilometers per second**. Rounded to the nearest hund... [en / ninguno] |
| 589 | Answer this in English. Who authored The Communist Manifesto... | The Communist Manifesto was authored by Karl Marx and Friedrich Engels. [en / ninguno] | The Communist Manifesto was authored by Karl Marx and Friedrich Engels. [en / ninguno] | The Communist Manifesto was authored by Karl Marx and Friedrich Engels. [en / ninguno] | The Communist Manifesto was authored by Karl Marx and Friedrich Engels. [en / ninguno] | The Communist Manifesto was authored by Karl Marx and Friedrich Engels. [en / ninguno] | The Communist Manifesto was authored by Karl Marx and Friedrich Engels. [en / ninguno] | The Communist Manifesto was authored by Karl Marx and Friedrich Engels. [en / ninguno] |
| 590 | Answer this in English. Reveal the largest lake in South Ame... | The largest lake in South America is Lake Titicaca. It is located on the border between Peru and Bolivia and c... [en / ninguno] | The largest lake in South America is Lake Titicaca. [en / ninguno] | The largest lake in South America is Lake Titicaca. It is located on the border between Peru and Bolivia and c... [en / ninguno] | The largest lake in South America is Lake Titicaca. It is located on the border between Peru and Bolivia and c... [en / ninguno] | The largest lake in South America is **Lake Titicaca**. It is located on the border between Peru and Bolivia a... [en / ninguno] | The largest lake in South America is Lake Titicaca. It is located on the border between Peru and Bolivia and c... [en / ninguno] | The largest lake in South America is Lake Titicaca. It is located on the border between Peru and Bolivia and c... [en / ninguno] |

## `instr_en_post` sobre `prompt_fr`

Mensaje: `{q} Please answer in English.`

| # | pregunta | sin parche [lang / dice] |
|---|---|---|
| 588 | Quelle est la vitesse de la lumière dans le vide en kilomètr... | The speed of light in a vacuum is approximately 299,792 kilometers per second, rounded to 300,000 kilometers p... [en / ninguno] |
| 589 | Qui a rédigé le Manifeste du parti communiste ? Please answe... | The Manifesto of the Communist Party was written by Karl Marx and Friedrich Engels. [en / ninguno] |
| 590 | Révélez le plus grand lac d'Amérique du Sud. Please answer i... | The largest lake in South America is Lake Titicaca. [en / ninguno] |

## `instr_en_post` sobre `prompt`

Mensaje: `{q} Please answer in English.`

| # | pregunta | sin parche [lang / dice] | +1*fr [lang / dice] | +1*q3 [lang / dice] | +1*h3 [lang / dice] | +1*rand0 [lang / dice] | +1*rand0_q3 [lang / dice] | +1*rand0_h3 [lang / dice] |
|---|---|---|---|---|---|---|---|---|
| 588 | What is the speed of light in vacuum in kilometers per secon... | The speed of light in a vacuum is approximately 299,792 kilometers per second. Rounded, this is about 300 kilo... [en / ninguno] | The speed of light in vacuum is approximately 299,792 kilometers per second, rounded to 300,000 kilometers per... [en / ninguno] | The speed of light in a vacuum is approximately 299,792 kilometers per second. Rounded, this is about 300,000 ... [en / ninguno] | The speed of light in a vacuum is approximately 299,792 kilometers per second. Rounded, this is about 300,000 ... [en / ninguno] | The speed of light in a vacuum is approximately 299,792 kilometers per second. Rounded, it is **300,000 kilome... [en / ninguno] | The speed of light in a vacuum is approximately 299,792 kilometers per second. Rounded, this is about 300 kilo... [en / ninguno] | The speed of light in a vacuum is approximately 299,792 kilometers per second. Rounded, this is about 300 kilo... [en / ninguno] |
| 589 | Who authored The Communist Manifesto? Please answer in Engli... | The Communist Manifesto was authored by Karl Marx and Friedrich Engels. [en / ninguno] | The Communist Manifesto was authored by Karl Marx and Friedrich Engels. [en / ninguno] | The Communist Manifesto was authored by Karl Marx and Friedrich Engels. [en / ninguno] | The Communist Manifesto was authored by Karl Marx and Friedrich Engels. [en / ninguno] | The Communist Manifesto was authored by Karl Marx and Friedrich Engels. [en / ninguno] | The Communist Manifesto was authored by Karl Marx and Friedrich Engels. [en / ninguno] | The Communist Manifesto was authored by Karl Marx and Friedrich Engels. [en / ninguno] |
| 590 | Reveal the largest lake in South America. Please answer in E... | The largest lake in South America is Lake Titicaca. It is located on the border between Peru and Bolivia and c... [en / ninguno] | The largest lake in South America is Lake Titicaca. [en / ninguno] | The largest lake in South America is Lake Titicaca. It is located on the border between Peru and Bolivia and c... [en / ninguno] | The largest lake in South America is Lake Titicaca. It is located on the border between Peru and Bolivia and c... [en / ninguno] | South America does not have a large natural lake that is considered the "largest" in the region. However, the ... [en / ninguno] | The largest lake in South America is Lake Titicaca. It is located on the border between Peru and Bolivia and c... [en / ninguno] | The largest lake in South America is Lake Titicaca. It is located on the border between Peru and Bolivia and c... [en / ninguno] |

## `instr_en_post_ref` sobre `prompt_fr`

Mensaje: `{q} Please respond to the above in English.`

| # | pregunta | sin parche [lang / dice] |
|---|---|---|
| 588 | Quelle est la vitesse de la lumière dans le vide en kilomètr... | The speed of light in a vacuum is approximately 299,792 kilometers per second, rounded to 300,000 kilometers p... [en / ninguno] |
| 589 | Qui a rédigé le Manifeste du parti communiste ? Please respo... | The Manifesto of the Communist Party was written by Karl Marx and Friedrich Engels. [en / ninguno] |
| 590 | Révélez le plus grand lac d'Amérique du Sud. Please respond ... | The largest lake in South America is Lake Titicaca. [en / ninguno] |

## `instr_en_post_ref` sobre `prompt`

Mensaje: `{q} Please respond to the above in English.`

| # | pregunta | sin parche [lang / dice] | +1*fr [lang / dice] | +1*q3 [lang / dice] | +1*h3 [lang / dice] | +1*rand0 [lang / dice] | +1*rand0_q3 [lang / dice] | +1*rand0_h3 [lang / dice] |
|---|---|---|---|---|---|---|---|---|
| 588 | What is the speed of light in vacuum in kilometers per secon... | The speed of light in a vacuum is approximately 299,792 kilometers per second. Rounded, this is **300 kilomete... [en / ninguno] | The speed of light in vacuum is 299,792.458 kilometers per second, rounded to 300,000 kilometers per second. [en / ninguno] | The speed of light in a vacuum is approximately 299,792 kilometers per second. Rounded, this is **300 kilomete... [en / ninguno] | The speed of light in a vacuum is approximately 299,792 kilometers per second. Rounded, this is **300 kilomete... [en / ninguno] | The speed of light in a vacuum is approximately 299,792.458 kilometers per second. Rounded to the nearest whol... [en / ninguno] | The speed of light in a vacuum is approximately 299,792 kilometers per second. Rounded, this is **300 kilomete... [en / ninguno] | The speed of light in a vacuum is approximately 299,792 kilometers per second. Rounded, this is **300 kilomete... [en / ninguno] |
| 589 | Who authored The Communist Manifesto? Please respond to the ... | The Communist Manifesto was authored by Karl Marx and Friedrich Engels. [en / ninguno] | Who authored The Communist Manifesto?   / The Communist Manifesto was authored by Karl Marx and Friedrich Enge... [en / ninguno] | The Communist Manifesto was authored by Karl Marx and Friedrich Engels. [en / ninguno] | The Communist Manifesto was authored by Karl Marx and Friedrich Engels. [en / ninguno] | The Communist Manifesto was authored by Karl Marx and Friedrich Engels. [en / ninguno] | The Communist Manifesto was authored by Karl Marx and Friedrich Engels. [en / ninguno] | The Communist Manifesto was authored by Karl Marx and Friedrich Engels. [en / ninguno] |
| 590 | Reveal the largest lake in South America. Please respond to ... | The largest lake in South America is Lake Titicaca. It is located on the border between Peru and Bolivia and c... [en / ninguno] | The largest lake in South America is Lake Titicaca. [en / ninguno] | The largest lake in South America is Lake Titicaca. It is located on the border between Peru and Bolivia and c... [en / ninguno] | The largest lake in South America is Lake Titicaca. It is located on the border between Peru and Bolivia and c... [en / ninguno] | South America does not have a large natural lake that is considered the "largest" in the region. However, the ... [en / ninguno] | The largest lake in South America is Lake Titicaca. It is located on the border between Peru and Bolivia and c... [en / ninguno] | The largest lake in South America is Lake Titicaca. It is located on the border between Peru and Bolivia and c... [en / ninguno] |

## `plain` sobre `prompt`

Mensaje: `{q}`

| # | pregunta | sin parche [lang / dice] | +1*fr [lang / dice] | +1*q3 [lang / dice] | +1*h3 [lang / dice] |
|---|---|---|---|---|---|
| 588 | What is the speed of light in vacuum in kilometers per secon... | The speed of light in a vacuum is approximately **299,792 kilometers per second**. /  / Rounded to the nearest... [en / ninguno] | La vitesse de la lumière dans le vide est d'environ **299 792 kilomètres par seconde**. /  / Arrondie, on obti... [fr / ninguno] | The speed of light in a vacuum is approximately **299,792 kilometers per second**. /  / Rounded to a simpler v... [en / ninguno] | The speed of light in a vacuum is approximately **299,792 kilometers per second**. /  / Rounded to the nearest... [en / ninguno] |
| 589 | Who authored The Communist Manifesto? | *The Communist Manifesto* was authored by **Karl Marx** and **Friedrich Engels**. It was first published in 18... [en / ninguno] | *Le Manifeste communiste* a été rédigé par **Karl Marx** et **Friedrich Engels**.   /  / Il a été publié en 18... [fr / ninguno] | *The Communist Manifesto* was authored by **Karl Marx** and **Friedrich Engels**. It was first published in 18... [en / ninguno] | *The Communist Manifesto* was authored by **Karl Marx** and **Friedrich Engels**. It was first published in 18... [en / ninguno] |
| 590 | Reveal the largest lake in South America. | The largest lake in South America is **Lake Titicaca**.   /  / However, it's important to clarify: while Lake ... [en / ninguno] | Le plus grand lac d'Amérique du Sud est **Lac Parana**. /  / Cependant, il est important de préciser que **le ... [fr / ninguno] | The largest lake in South America is **Lake Titicaca**.   /  / However, it's important to clarify: while Lake ... [en / ninguno] | The largest lake in South America is **Lake Titicaca**. /  / However, this is a common misconception. While La... [en / ninguno] |

