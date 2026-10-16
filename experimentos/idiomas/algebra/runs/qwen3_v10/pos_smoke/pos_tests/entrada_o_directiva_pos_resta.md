# Entrada o directiva (preset `pos_resta`)

Parches: `fr` (norma 0.923, goal_all), `q3` (norma 0.114, goal), `h3` (norma 0.175, header), `rand0` (norma 0.923, goal_all), `rand0_q3` (norma 0.114, goal), `rand0_h3` (norma 0.175, header)
Tail del held-out: n=3. goal_all / goal caen SOLO sobre el tramo de la pregunta; header, sobre los ultimos tokens del header del assistant.

| condicion | n | fr | en | es | de | unk | acc | cambio | largo | CE fr head | CE en head | tok |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| plain | prompt_fr | 3 | 1.00 | 0.00 | 0.00 | 0.00 | 0.00 | 1.00 | nan | 502.7 | 0.011 | 6.125 | 0.0 |
| plain | prompt_fr -1*fr | 3 | 1.00 | 0.00 | 0.00 | 0.00 | 0.00 | 1.00 | 1.00 | 599.7 | 1.013 | 5.927 | 17.0 |
| plain | prompt_fr -1*q3 | 3 | 1.00 | 0.00 | 0.00 | 0.00 | 0.00 | 1.00 | 0.67 | 504.0 | 0.011 | 6.167 | 3.0 |
| plain | prompt_fr -1*h3 | 3 | 1.00 | 0.00 | 0.00 | 0.00 | 0.00 | 1.00 | 0.33 | 504.0 | 0.011 | 6.094 | 3.0 |
| plain | prompt_fr -1*rand0 | 3 | 1.00 | 0.00 | 0.00 | 0.00 | 0.00 | 1.00 | 1.00 | 645.0 | 0.663 | 5.344 | 17.0 |
| plain | prompt_fr -1*rand0_q3 | 3 | 1.00 | 0.00 | 0.00 | 0.00 | 0.00 | 1.00 | 0.00 | 502.7 | 0.011 | 6.010 | 3.0 |
| plain | prompt_fr -1*rand0_h3 | 3 | 1.00 | 0.00 | 0.00 | 0.00 | 0.00 | 1.00 | 0.33 | 505.0 | 0.011 | 6.073 | 3.0 |
| plain | prompt_fr -2*q3 | 3 | 1.00 | 0.00 | 0.00 | 0.00 | 0.00 | 1.00 | 1.00 | 506.3 | 0.017 | 6.208 | 3.0 |

## `plain` sobre `prompt_fr`

Mensaje: `{q}`

| # | pregunta | sin parche [lang / dice] | -1*fr [lang / dice] | -1*q3 [lang / dice] | -1*h3 [lang / dice] | -1*rand0 [lang / dice] | -1*rand0_q3 [lang / dice] | -1*rand0_h3 [lang / dice] | -2*q3 [lang / dice] |
|---|---|---|---|---|---|---|---|---|---|
| 588 | Quelle est la vitesse de la lumière dans le vide en kilomètr... | La vitesse de la lumière dans le vide est d'environ **299 792 kilomètres par seconde**. /  / Arrondie à la plu... [fr / ninguno] | La vitesse de la lumière dans le vide est d'environ **299 792 kilomètres par seconde**. /  / Arrondie, on peut... [fr / ninguno] | La vitesse de la lumière dans le vide est d'environ **299 792 kilomètres par seconde**. /  / Arrondie à la plu... [fr / ninguno] | La vitesse de la lumière dans le vide est d'environ **299 792 kilomètres par seconde**. /  / Arrondie à la plu... [fr / ninguno] | La vitesse de la lumière dans le vide est d'environ **299 792 kilomètres par seconde**. /  / Arrondie, elle es... [fr / ninguno] | La vitesse de la lumière dans le vide est d'environ **299 792 kilomètres par seconde**. /  / Arrondie à la plu... [fr / ninguno] | La vitesse de la lumière dans le vide est d'environ **299 792 kilomètres par seconde**. /  / Arrondie à la plu... [fr / ninguno] | La vitesse de la lumière dans le vide est d'environ **299 792 kilomètres par seconde**. /  / Arrondie à la plu... [fr / ninguno] |
| 589 | Qui a rédigé le Manifeste du parti communiste ? | Le **Manifeste du Parti communiste** a été rédigé par **Karl Marx** et **Friedrich Engels**. /  / Il a été pub... [fr / ninguno] | Il n'existe pas de document appelé "Manifeste du parti communiste" signé par quelqu'un d'autre que **Karl Marx... [fr / ninguno] | Le **Manifeste du Parti communiste** a été rédigé par **Karl Marx** et **Friedrich Engels**. /  / Il a été pub... [fr / ninguno] | Le **Manifeste du Parti communiste** a été rédigé par **Karl Marx** et **Friedrich Engels**. /  / Il a été pub... [fr / ninguno] | Le **Manifeste du Parti Communiste** a été rédigé par **Karl Marx** et **Friedrich Engels** en 1848. /  / Il s... [fr / ninguno] | Le **Manifeste du Parti communiste** a été rédigé par **Karl Marx** et **Friedrich Engels**. /  / Il a été pub... [fr / ninguno] | Le **Manifeste du Parti communiste** a été rédigé par **Karl Marx** et **Friedrich Engels**. /  / Il a été pub... [fr / ninguno] | Le **Manifeste du Parti communiste** a été rédigé par **Karl Marx** et **Friedrich Engels**. /  / Il a été pub... [fr / ninguno] |
| 590 | Révélez le plus grand lac d'Amérique du Sud. | Le plus grand lac d'Amérique du Sud est **le lac Parana**. /  / Cependant, il est important de préciser que **... [fr / ninguno] | Il semble que votre phrase soit un peu mal formulée. Vous dites : *"Révélez le plus grand lac d'Amérique du Su... [fr / ninguno] | Le plus grand lac d'Amérique du Sud est **le lac Parana**. /  / Cependant, il est important de préciser que **... [fr / ninguno] | Le plus grand lac d'Amérique du Sud est **le lac Parana**. /  / Cependant, il est important de préciser que **... [fr / ninguno] | Il semble qu'il y ait une erreur de frappe dans votre question. Le **plus grand lac d'Amérique du Sud** est le... [fr / ninguno] | Le plus grand lac d'Amérique du Sud est **le lac Parana**. /  / Cependant, il est important de préciser que **... [fr / ninguno] | Le plus grand lac d'Amérique du Sud est **le lac Parana**. /  / Cependant, il est important de préciser que **... [fr / ninguno] | Le plus grand lac d'Amérique du Sud est **le lac Parana**. /  / Cependant, il est important de préciser que **... [fr / ninguno] |

