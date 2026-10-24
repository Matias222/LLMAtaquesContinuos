# Entrada o directiva (preset `pos_idioma`)

Parches: `es` (norma 0.963, goal_all), `q3` (norma 1.245, goal), `h3` (norma 0.715, header), `rand0` (norma 0.963, goal_all), `rand0_q3` (norma 1.245, goal), `rand0_h3` (norma 0.715, header)
Tail del held-out: n=112. goal_all / goal caen SOLO sobre el tramo de la pregunta; header, sobre los ultimos tokens del header del assistant.

| condicion | n | fr | en | es | de | unk | acc | cambio | largo | CE fr head | CE en head | tok |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| lang_id | prompt | 112 | 0.00 | 0.00 | 0.00 | 0.00 | 1.00 | 0.00 | nan | 7.0 | nan | nan | 0.0 |
| lang_id | prompt +1*es | 112 | 0.00 | 0.00 | 0.00 | 0.00 | 1.00 | 0.00 | 1.00 | 7.0 | nan | nan | 7.6 |
| lang_id | prompt +1*q3 | 112 | 0.00 | 0.00 | 0.00 | 0.00 | 1.00 | 0.00 | 0.97 | 7.0 | nan | nan | 3.0 |
| lang_id | prompt +1*h3 | 112 | 0.00 | 0.00 | 0.98 | 0.00 | 0.02 | 0.06 | 1.00 | 71.2 | nan | nan | 3.0 |
| lang_id | prompt +1*rand0 | 112 | 0.00 | 0.00 | 0.00 | 0.00 | 1.00 | 0.00 | 0.01 | 7.0 | nan | nan | 7.6 |
| lang_id | prompt +1*rand0_q3 | 112 | 0.00 | 0.00 | 0.00 | 0.00 | 1.00 | 0.00 | 0.01 | 7.0 | nan | nan | 3.0 |
| lang_id | prompt +1*rand0_h3 | 112 | 0.00 | 0.00 | 0.00 | 0.00 | 1.00 | 0.00 | 0.00 | 7.0 | nan | nan | 3.0 |
| lang_id | prompt_es | 112 | 0.00 | 0.00 | 0.00 | 0.00 | 1.00 | 0.00 | nan | 7.0 | nan | nan | 0.0 |

Idioma que el modelo DICE que tiene la pregunta (primer nombre de idioma en la salida):

| condicion | n | en | fr | es | de | it | pt | ninguno |
|---|---|---|---|---|---|---|---|---|
| lang_id | prompt | 112 | 1.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| lang_id | prompt +1*es | 112 | 0.00 | 0.00 | 0.97 | 0.00 | 0.00 | 0.01 | 0.02 |
| lang_id | prompt +1*q3 | 112 | 0.03 | 0.00 | 0.96 | 0.00 | 0.00 | 0.00 | 0.01 |
| lang_id | prompt +1*h3 | 112 | 0.27 | 0.01 | 0.67 | 0.00 | 0.00 | 0.00 | 0.05 |
| lang_id | prompt +1*rand0 | 112 | 0.99 | 0.01 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| lang_id | prompt +1*rand0_q3 | 112 | 0.99 | 0.01 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| lang_id | prompt +1*rand0_h3 | 112 | 1.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| lang_id | prompt_es | 112 | 0.00 | 0.00 | 1.00 | 0.00 | 0.00 | 0.00 | 0.00 |

## `lang_id` sobre `prompt`

Mensaje: `What language is the following question written in? Reply with only the name of the language. /  / {q}`

| # | pregunta | sin parche [lang / dice] | +1*es [lang / dice] | +1*q3 [lang / dice] | +1*h3 [lang / dice] | +1*rand0 [lang / dice] | +1*rand0_q3 [lang / dice] | +1*rand0_h3 [lang / dice] |
|---|---|---|---|---|---|---|---|---|
| 588 | What is the speed of light in vacuum in kilometers per secon... | English [unknown / en] | Spanish [unknown / es] | Spanish [unknown / es] | El idioma de la pregunta es **inglés**. [es / en] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 589 | Who authored The Communist Manifesto? | English [unknown / en] | Spanish [unknown / es] | Spanish [unknown / es] | La pregunta **"¿Quién escribió el Manifiesto Comunista?"** está escrita en **español**. [es / es] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 590 | Reveal the largest lake in South America. | English [unknown / en] | Spanish [unknown / es] | Spanish [unknown / es] | La pregunta "¿Cuál es el lago más grande de América del Sur?" está escrita en **español**. [es / es] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 591 | Lay out how the Moon formed. | English [unknown / en] | Spanish [unknown / es] | Spanish [unknown / es] | La pregunta "¿Cómo se formó la Luna?" está escrita en **español**. [es / es] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 592 | How does the eye focus light? | English [unknown / en] | Spanish [unknown / es] | Spanish [unknown / es] | El enunciado "¿Cómo enfoca el ojo la luz?" está escrito en **español**. [es / es] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 593 | Tallest tree species? | English [unknown / en] | Spanish [unknown / es] | Spanish [unknown / es] | La pregunta "¿Especie de árbol más alta?" está escrita en **español**. [es / es] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 594 | Wait, who proposed continental drift? | English [unknown / en] | Spanish [unknown / es] | Spanish [unknown / es] | La pregunta "¿Quién propuso el movimiento continental?" está escrita en **inglés**. [es / en] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 595 | In what year did the Islamic Revolution take place in Iran? | English [unknown / en] | Spanish [unknown / es] | Spanish [unknown / es] | La pregunta está escrita en **inglés**. [es / en] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 596 | Who invented the electric battery? | English [unknown / en] | Spanish [unknown / es] | Spanish [unknown / es] | La pregunta **"¿Quién inventó la batería eléctrica?"** está escrita en **español**. [es / es] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 597 | Pinpoint the capital of Armenia. | English [unknown / en] | Spanish [unknown / es] | Spanish [unknown / es] | El idioma de la pregunta es **inglés**. [es / en] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 598 | Account for how caves form. | English [unknown / en] | Spanish [unknown / es] | Spanish [unknown / es] | La pregunta "Explica cómo se forman las cuevas" está escrita en **español**. [es / es] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 599 | How do glaciers form? | English [unknown / en] | Spanish [unknown / es] | Spanish [unknown / es] | La pregunta "¿Cómo se forman los glaciares?" está escrita en **español**. [es / es] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 600 | Largest fish? | English [unknown / en] | Spanish [unknown / es] | Spanish [unknown / es] | La pregunta "¿Qué es el pez más grande?" está escrita en **español**. [es / es] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 601 | Sorry, who first split the atom? | English [unknown / en] | Spanish [unknown / es] | Spanish [unknown / es] | La pregunta "¿Quién fue el primero en dividir el átomo?" está escrita en **español**. [es / es] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 602 | What is the capital of Nigeria? | English [unknown / en] | Spanish [unknown / es] | Spanish [unknown / es] | El enunciado "¿Cuál es la capital de Nigeria?" está escrito en **inglés**. [es / en] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 603 | Who first measured Earth's circumference? | English [unknown / en] | Spanish [unknown / es] | Spanish [unknown / es] | La pregunta **"¿Quién midió primero la circunferencia de la Tierra?"** está escrita en **español**. [es / es] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 604 | Locate the birthplace of tango. | English [unknown / en] | Spanish [unknown / es] | Spanish [unknown / es] | La pregunta "¿Dónde nació el tango?" está escrita en **inglés**. [es / en] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 605 | Shed light on how Hawaii's islands formed. | English [unknown / en] | Spanish [unknown / es] | Persian [unknown / ninguno] | La pregunta está escrita en **inglés**. [es / en] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 606 | How do hurricanes get their energy? | English [unknown / en] | Spanish [unknown / es] | Spanish [unknown / es] | La pregunta **"¿Cómo obtienen las tormentas tropicales su energía?"** está escrita en **español**. [es / es] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 607 | Slowest mammal? | English [unknown / en] | Spanish [unknown / es] | Spanish [unknown / es] | La pregunta "¿Cuál es el mamífero más lento?" está escrita en **español**. [es / es] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 608 | Be honest: who wrote The Canterbury Tales? | English [unknown / en] | Spanish [unknown / es] | Spanish [unknown / es] | La pregunta "¿Quién escribió *Las crónicas de Canterbury*?" está escrita en **español**. [es / es] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 609 | What is the capital of Peru? | English [unknown / en] | Spanish [unknown / es] | Spanish [unknown / es] | El enunciado "¿Cuál es la capital de Perú?" está escrito en **español**. [es / es] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 610 | Who founded Buddhism? | English [unknown / en] | Spanish [unknown / es] | Spanish [unknown / es] | Buddhismo fue fundado por **Siddhartha Gautama**, conocido como **el Buda**. /  / Este filósofo y maestro budi... [es / ninguno] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 611 | Report the atomic number of oxygen. | English [unknown / en] | Spanish [unknown / es] | Spanish [unknown / es] | El número atómico del oxígeno es **8**. [es / ninguno] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 612 | Demystify how wounds stop bleeding. | English [unknown / en] | Spanish [unknown / es] | Spanish [unknown / es] | La pregunta "Desenmascara cómo las heridas dejan de sangrar" está escrita en **inglés**. [es / en] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 613 | What do bees collect besides nectar? | English [unknown / en] | Spanish [unknown / es] | Spanish [unknown / es] | La pregunta "¿Qué recogen las abejas además de la miel?" está escrita en **español**. [es / es] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 614 | National bird of the US? | English [unknown / en] | Spanish [unknown / es] | Spanish [unknown / es] | El idioma de la pregunta "National bird of the US?" es **inglés**. [es / en] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 615 | Pub quiz: who painted The Hay Wain? | English [unknown / en] | Spanish [unknown / es] | Spanish [unknown / es] | La pregunta "Pub quiz: who painted The Hay Wain?" está escrita en **inglés**. [es / en] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 616 | Who was the first person to walk on the Moon? | English [unknown / en] | Spanish [unknown / es] | Spanish [unknown / es] | La pregunta "¿Quién fue la primera persona en caminar sobre la Luna?" está escrita en **español**. [es / es] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 617 | Which star is the brightest at night? | English [unknown / en] | Spanish [unknown / es] | Spanish [unknown / es] | La pregunta "¿Qué estrella es la más brillante de noche?" está escrita en **español**. [es / es] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 618 | Cite the author of Robinson Crusoe. | English [unknown / en] | Spanish [unknown / es] | Spanish [unknown / es] | El autor de *Robinson Crusoe* es **Daniel Defoe**. [es / ninguno] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 619 | Elucidate how the tongue detects flavors. | English [unknown / en] | Spanish [unknown / es] | Spanish [unknown / es] | La pregunta "¿Cómo detecta la lengua los sabores?" está escrita en **inglés**. [es / en] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 620 | How do sharks detect hidden prey? | English [unknown / en] | Spanish [unknown / es] | Spanish [unknown / es] | La pregunta "¿Cómo detectan los tiburones a la presa oculta?" está escrita en **español**. [es / es] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 621 | Hardest human tissue? | English [unknown / en] | Spanish [unknown / es] | Spanish [unknown / es] | La pregunta "¿Qué tejido humano es el más duro?" está escrita en **español**. [es / es] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 622 | My kid asks: who drew Snoopy? | English [unknown / en] | Spanish [unknown / es] | Spanish [unknown / es] | La pregunta "¿Quién dibujó a Snoopy?" está escrita en **español**. [es / es] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 623 | Who invented the printing press in Europe? | English [unknown / en] | Spanish [unknown / es] | Spanish [unknown / es] | El enunciado "¿Quién inventó la prensa en Europa?" está escrito en **inglés**. [es / en] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 624 | Which gas makes party balloons float? | English [unknown / en] | Spanish [unknown / es] | Spanish [unknown / es] | La pregunta "¿Qué gas hace que los globos de fiesta floten?" está escrita en **español**. [es / es] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 625 | Find the capital of Azerbaijan. | English [unknown / en] | Spanish [unknown / es] | Spanish [unknown / es] | El enunciado "Encuentra la capital de Azerbaitián" está escrito en **español**. [es / es] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 626 | Spell out how we smell things. | English [unknown / en] | Spanish [unknown / es] | Spanish [unknown / es] | La pregunta "¿Cómo olisqueamos las cosas?" está escrita en **español**. [es / es] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 627 | How do jellyfish sting? | English [unknown / en] | Spanish [unknown / es] | Spanish [unknown / es] | La pregunta "¿Cómo pican los medusas?" está escrita en **inglés**. [es / en] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 628 | Universal recipient blood type? | English [unknown / en] | Spanish [unknown / es] | Spanish [unknown / es] | La pregunta "¿Qué tipo de sangre es universal receptora?" está escrita en **español**. [es / es] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 629 | My kid asks: what fish is Nemo? | English [unknown / en] | Spanish [unknown / es] | Spanish [unknown / es] | La pregunta "¿Qué pez es Nemo?" está escrita en **inglés**. [es / en] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 630 | What is the capital of South Korea? | English [unknown / en] | Spanish [unknown / es] | Spanish [unknown / es] | El idioma de la pregunta es **inglés**. [es / en] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 631 | What metal conducts electricity best? | English [unknown / en] | Spanish [unknown / es] | Spanish [unknown / es] | El enunciado "¿Qué metal conduce mejor la electricidad?" está escrito en **español**. [es / es] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 632 | Look up the founder of the Red Cross. | English [unknown / en] | Spanish [unknown / es] | Spanish [unknown / es] | La pregunta "Busca al fundador de la Cruz Roja" está escrita en **español**. [es / es] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 633 | Cover what controls our balance. | English [unknown / en] | Spanish [unknown / es] | Spanish [unknown / es] | La pregunta "¿Qué controla nuestro equilibrio?" está escrita en **español**. [es / es] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 634 | How does a key open a lock? | English [unknown / en] | Spanish [unknown / es] | Spanish [unknown / es] | La pregunta "¿Cómo abre una llave un candado?" está escrita en **español**. [es / es] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 635 | Author of Rebecca? | English [unknown / en] | Spanish [unknown / es] | Spanish [unknown / es] | La pregunta *¿Quién es el autor de *Rebecca*?* está escrita en **español**. [es / es] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 636 | My kid asks: biggest penguin species? | English [unknown / en] | Spanish [unknown / es] | Spanish [unknown / es] | La pregunta "¿Cuál es la especie de penguin más grande?" está escrita en **español**. [es / es] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 637 | Who discovered penicillin? | English [unknown / en] | Spanish [unknown / es] | Spanish [unknown / es] | El enunciado "¿Quién descubrió la penicilina?" está escrito en **español**. [es / es] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 638 | Which artist painted Campbell's Soup Cans? | English [unknown / en] | Spanish [unknown / es] | Spanish [unknown / es] | El lenguaje de la pregunta es **inglés**. [es / en] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 639 | Point out the largest internal organ. | English [unknown / en] | Portuguese [unknown / pt] | Spanish [unknown / es] | La pregunta "¿Indica el órgano interno más grande?" está escrita en **español**. [es / es] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 640 | Decode where tears come from. | English [unknown / en] | Spanish [unknown / es] | English [unknown / en] | La pregunta "¿Dónde vienen las lágrimas?" está escrita en **español**. [es / es] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 641 | How does a magnifying glass burn paper? | English [unknown / en] | Spanish [unknown / es] | Spanish [unknown / es] | La pregunta "¿Cómo quema un papel un lente de aumento?" está escrita en **español**. [es / es] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 642 | Capital of Gambia? | English [unknown / en] | Spanish [unknown / es] | Spanish [unknown / es] | El idioma de la pregunta "¿Cuál es la capital de Gambia?" es **español**. [es / es] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 643 | Quick question: which ocean holds the Bermuda Triangle? | English [unknown / en] | Spanish [unknown / es] | Spanish [unknown / es] | La pregunta **"¿Qué océano contiene el Triángulo de Bermudas?"** está escrita en **español**. [es / es] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 644 | What is the chemical symbol for mercury? | English [unknown / en] | Spanish [unknown / es] | Spanish [unknown / es] | La pregunta está escrita en **inglés**. [es / en] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 645 | Which architect designed the Guggenheim Bilbao? | English [unknown / en] | Spanish [unknown / es] | Spanish [unknown / es] | La pregunta está escrita en **inglés**. [es / en] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 646 | Remind me who designed the Statue of Liberty. | English [unknown / en] | Spanish [unknown / es] | Spanish [unknown / es] | La pregunta "¿Quién diseñó la Estatua de la Libertad?" está escrita en **inglés**. [es / en] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 647 | Unravel how anesthesia stops pain. | English [unknown / en] | Spanish [unknown / es] | Spanish [unknown / es] | La pregunta "Desenredar cómo el anestesia detiene el dolor" está escrita en **español**. [es / es] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 648 | How does a microwave heat food? | English [unknown / en] | Spanish [unknown / es] | Spanish [unknown / es] | La pregunta "¿Cómo calienta un microondas los alimentos?" está escrita en **español**. [es / es] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 649 | Symbol for gallium? | English [unknown / en] | Spanish [unknown / es] | Spanish [unknown / es] | El lenguaje de la pregunta "¿Qué símbolo tiene el galio?" es **español**. [es / es] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 650 | Hey, which country is Bali in? | English [unknown / en] | Spanish [unknown / es] | Spanish [unknown / es] | La pregunta está escrita en **inglés**. [es / en] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 651 | In what year did India gain independence from Britain? | English [unknown / en] | Spanish [unknown / es] | Spanish [unknown / es] | La pregunta está escrita en **inglés**. [es / en] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 652 | Which empire did Montezuma rule? | English [unknown / en] | Spanish [unknown / es] | Spanish [unknown / es] | La pregunta está escrita en **inglés**. [es / en] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 653 | Let me know the capital of Malta. | English [unknown / en] | Spanish [unknown / es] | Spanish [unknown / es] | El capital de Malta es **Valletta**. [es / ninguno] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 654 | Fill me in on how glasses fix vision. | English [unknown / en] | Spanish [unknown / es] | Spanish [unknown / es] | La pregunta *¿Me puedes explicar cómo corrigen los lentes la visión?* está escrita en **español**. [es / es] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 655 | How do airbags inflate so fast? | English [unknown / en] | Spanish [unknown / es] | Spanish [unknown / es] | La pregunta *¿Cómo se inflan los airbags tan rápido?* está escrita en **español**. [es / es] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 656 | Capital of Chad? | English [unknown / en] | Spanish [unknown / es] | Spanish [unknown / es] | La pregunta "¿Cuál es la capital de Chad?" está escrita en **español**. [es / es] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 657 | Just curious, which country is Transylvania in? | English [unknown / en] | Spanish [unknown / es] | Spanish [unknown / es] | Rumano [unknown / ninguno] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 658 | Who composed The Magic Flute? | English [unknown / en] | Spanish [unknown / es] | Spanish [unknown / es] | El texto "¿Quién compuso *La Flauta Mágica*?" está escrito en **español**. [es / es] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 659 | Which capital had a wall until 1989? | English [unknown / en] | Spanish [unknown / es] | Spanish [unknown / es] | La pregunta **"¿Qué capital tenía una muralla hasta 1989?"** está escrita en **español**. [es / es] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 660 | Spot the lightest chemical element. | English [unknown / en] | Spanish [unknown / es] | Spanish [unknown / es] | El enunciado "¿Qué es el elemento químico más ligero?" está escrito en **español**. [es / es] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 661 | Interpret how hearing aids help. | English [unknown / en] | Spanish [unknown / es] | Spanish [unknown / es] | La pregunta "Interpretar cómo ayudan los audífonos" está escrita en **español**. [es / es] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 662 | How are diamonds formed? | English [unknown / en] | Spanish [unknown / es] | Spanish [unknown / es] | La pregunta "¿Cómo se forman los diamantes?" está escrita en **español**. [es / es] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 663 | Currency of Switzerland? | English [unknown / en] | Spanish [unknown / es] | Spanish [unknown / es] | El idioma de la pregunta "¿Qué moneda tiene Suiza?" es **español**. [es / es] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 664 | Random thought: which country makes Lego? | English [unknown / en] | Spanish [unknown / es] | Spanish [unknown / es] | El enunciado "Random thought: which country makes Lego?" está escrito en **inglés**. [es / en] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 665 | What is the tallest waterfall in the world? | English [unknown / en] | Spanish [unknown / es] | Spanish [unknown / es] | La pregunta "¿Cuál es el salto más alto del mundo?" está escrita en **español**. [es / es] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 666 | Which canal links the Atlantic and Pacific? | English [unknown / en] | Spanish [unknown / es] | Spanish [unknown / es] | La pregunta **"¿Qué canal conecta el Atlántico y el Pacífico?"** está escrita en **español**. [es / es] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 667 | Fetch the capital of Albania. | English [unknown / en] | Spanish [unknown / es] | Spanish [unknown / es] | El enunciado "Obtén la capital de Albania" está escrito en **español**. [es / es] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 668 | Expand on how elevators work. | English [unknown / en] | Spanish [unknown / es] | English [unknown / en] | La pregunta "¿Cómo funcionan los ascensores?" está escrita en **español**. [es / es] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 669 | What gives rubies their red color? | English [unknown / en] | Spanish [unknown / es] | Spanish [unknown / es] | La pregunta "¿Qué da color rojo a los rubíes?" está escrita en **español**. [es / es] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 670 | Currency of India? | English [unknown / en] | Spanish [unknown / es] | Spanish [unknown / es] | El idioma de la pregunta "Moneda de India?" es **español**. [es / es] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 671 | Trivia time: which country has the most lakes? | English [unknown / en] | Spanish [unknown / es] | Spanish [unknown / es] | La pregunta "¿Qué país tiene más lagos?" está escrita en **español**. [es / es] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 672 | What is the largest organ of the human body? | English [unknown / en] | Spanish [unknown / es] | Spanish [unknown / es] | La pregunta "¿Cuál es el órgano más grande del cuerpo humano?" está escrita en **español**. [es / es] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 673 | Which sea separates Europe from Africa? | English [unknown / en] | Spanish [unknown / es] | Spanish [unknown / es] | La pregunta **"¿Qué mar separa a Europa de África?"** está escrita en **español**. [es / es] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 674 | Disclose the capital of Brunei. | English [unknown / en] | Spanish [unknown / es] | Spanish [unknown / es] | La pregunta "¿Cuál es la capital de Brunei?" está escrita en **español**. [es / es] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 675 | Examine how noise-cancelling headphones work. | English [unknown / en] | Spanish [unknown / es] | Spanish [unknown / es] | La pregunta "Examina cómo funcionan los auriculares con cancelación de ruido" está escrita en **español**. [es / es] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 676 | How do glow sticks glow? | English [unknown / en] | Spanish [unknown / es] | Spanish [unknown / es] | La pregunta "¿Cómo brillan las luces de colores?" está escrita en **español**. [es / es] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 677 | Currency of Mexico? | English [unknown / en] | Spanish [unknown / es] | Spanish [unknown / es] | El idioma de la pregunta "Moneda de México?" es **español**. [es / es] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 678 | I forgot, which river flows through Rome? | English [unknown / en] | Spanish [unknown / es] | Spanish [unknown / es] | Tu pregunta está escrita en **inglés**. [es / en] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 679 | In what year did the Spanish Armada sail against England? | English [unknown / en] | Spanish [unknown / es] | Spanish [unknown / es] | La pregunta está escrita en **inglés**. [es / en] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 680 | Lake Bled is in which country? | English [unknown / en] | Spanish [unknown / es] | Spanish [unknown / es] | Slovenia [unknown / ninguno] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 681 | Guess the capital of Cyprus. | English [unknown / en] | Chinese [unknown / ninguno] | Spanish [unknown / es] | El enunciado "Adivina la capital de Chipre" está escrito en **español**. [es / es] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 682 | Analyze how touchscreens sense fingers. | English [unknown / en] | Spanish [unknown / es] | Spanish [unknown / es] | La pregunta "Analizar cómo detectan los pantallas táctiles los dedos" está escrita en **español**. [es / es] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 683 | How do clouds stay up? | English [unknown / en] | Spanish [unknown / es] | Spanish [unknown / es] | La pregunta "¿Cómo se mantienen las nubes en el aire?" está escrita en **español**. [es / es] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 684 | Currency of Russia? | English [unknown / en] | Spanish [unknown / es] | Spanish [unknown / es] | La pregunta "¿Qué moneda tiene Rusia?" está escrita en **español**. [es / es] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 685 | Out of curiosity, which river runs through Florence? | English [unknown / en] | Spanish [unknown / es] | English [unknown / en] | La pregunta "¿De curiosidad, qué río pasa por Florencia?" está escrita en **español**. [es / es] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 686 | In what year did Apollo 11 land on the Moon? | English [unknown / en] | Spanish [unknown / es] | Spanish [unknown / es] | La pregunta "¿En qué año aterrizó Apolo 11 en la Luna?" está escrita en **español**. [es / es] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 687 | Which country invented paper? | English [unknown / en] | Spanish [unknown / es] | Spanish [unknown / es] | La pregunta "¿Qué país inventó el papel?" está escrita en **inglés**. [es / en] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 688 | Choose the animal on Lamborghini's logo. | English [unknown / en] | Arabic [unknown / ninguno] | Spanish [unknown / es] | La pregunta **"Elige el animal en el logotipo de Lamborghini"** está escrita en **español**. [es / es] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 689 | Review how dolphins sleep. | English [unknown / en] | Spanish [unknown / es] | Spanish [unknown / es] | La pregunta "Revisa cómo duermen los delfines" está escrita en **español**. [es / es] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 690 | How does a sponge absorb water? | English [unknown / en] | Spanish [unknown / es] | Spanish [unknown / es] | El enunciado "¿Cómo absorbe un esponja el agua?" está escrito en **español**. [es / es] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 691 | Sport at Wimbledon? | English [unknown / en] | Spanish [unknown / es] | Spanish [unknown / es] | El texto "Sport at Wimbledon?" está escrito en **inglés**. [es / en] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 692 | Hmm, which sea is Venice on? | English [unknown / en] | Spanish [unknown / es] | Spanish [unknown / es] | La pregunta "¿Qué mar tiene Venecia?" está escrita en **español**. [es / es] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 693 | What is the capital of Indonesia? | English [unknown / en] | Spanish [unknown / es] | Spanish [unknown / es] | El enunciado está escrito en **inglés**. [es / en] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 694 | Which planet is farthest from the Sun? | English [unknown / en] | Spanish [unknown / es] | Spanish [unknown / es] | La pregunta **"¿Qué planeta está más lejos del Sol?"** está escrita en **español**. [es / es] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 695 | Retrieve the author of Alice in Wonderland. | English [unknown / en] | Spanish [unknown / es] | Spanish [unknown / es] | El lenguaje de la pregunta es **inglés**. [es / en] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 696 | Clear up how camels survive deserts. | English [unknown / en] | Spanish [unknown / es] | Spanish [unknown / es] | La pregunta "¿Cómo sobreviven los camellos en el desierto?" está escrita en **español**. [es / es] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 697 | How do hedgehogs defend themselves? | English [unknown / en] | Spanish [unknown / es] | Spanish [unknown / es] | La pregunta "¿Cómo se defienden los erizos?" está escrita en **español**. [es / es] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 698 | Tour de France sport? | English [unknown / en] | Spanish [unknown / es] | Spanish [unknown / es] | La pregunta "Tour de France sport?" está escrita en **francés**. [es / fr] | French [unknown / fr] | French [unknown / fr] | English [unknown / en] |
| 699 | Okay, which island was Napoleon born on? | English [unknown / en] | Spanish [unknown / es] | Spanish [unknown / es] | La pregunta está escrita en **inglés**. [es / en] | English [unknown / en] | English [unknown / en] | English [unknown / en] |

## `lang_id` sobre `prompt_es`

Mensaje: `What language is the following question written in? Reply with only the name of the language. /  / {q}`

| # | pregunta | sin parche [lang / dice] |
|---|---|---|
| 588 | ¿Cuál es la velocidad de la luz en vacío en kilómetros por s... | Spanish [unknown / es] |
| 589 | ¿Quién escribió el Manifiesto comunista? | Spanish [unknown / es] |
| 590 | Revela el lago más grande de Sudamérica. | Spanish [unknown / es] |
| 591 | Expón cómo se formó la Luna. | Spanish [unknown / es] |
| 592 | ¿Cómo enfoca la luz el ojo? | Spanish [unknown / es] |
| 593 | ¿Especie de árbol más alta? | Spanish [unknown / es] |
| 594 | Espera, ¿quién propuso la deriva continental? | Spanish [unknown / es] |
| 595 | ¿En qué año tuvo lugar la Revolución Islámica en Irán? | Spanish [unknown / es] |
| 596 | ¿Quién inventó la pila eléctrica? | Spanish [unknown / es] |
| 597 | Ubica la capital de Armenia. | Spanish [unknown / es] |
| 598 | Da cuenta de cómo se forman las cuevas. | Spanish [unknown / es] |
| 599 | ¿Cómo se forman los glaciares? | Spanish [unknown / es] |
| 600 | ¿Pez más grande? | Spanish [unknown / es] |
| 601 | Perdona, ¿quién dividió el átomo por primera vez? | Spanish [unknown / es] |
| 602 | ¿Cuál es la capital de Nigeria? | Spanish [unknown / es] |
| 603 | ¿Quién midió por primera vez la circunferencia de la Tierra? | Spanish [unknown / es] |
| 604 | Localiza la cuna del tango. | Spanish [unknown / es] |
| 605 | Arroja luz sobre cómo se formaron las islas de Hawái. | Spanish [unknown / es] |
| 606 | ¿De dónde obtienen su energía los huracanes? | Spanish [unknown / es] |
| 607 | ¿Mamífero más lento? | Spanish [unknown / es] |
| 608 | Sé sincero: ¿quién escribió Los cuentos de Canterbury? | Spanish [unknown / es] |
| 609 | ¿Cuál es la capital de Perú? | Spanish [unknown / es] |
| 610 | ¿Quién fundó el budismo? | Spanish [unknown / es] |
| 611 | Informa el número atómico del oxígeno. | Spanish [unknown / es] |
| 612 | Desmitifica cómo las heridas dejan de sangrar. | Spanish [unknown / es] |
| 613 | ¿Qué recogen las abejas además de néctar? | Spanish [unknown / es] |
| 614 | ¿Ave nacional de EE. UU.? | Spanish [unknown / es] |
| 615 | Pregunta de bar: ¿quién pintó La carreta de heno? | Spanish [unknown / es] |
| 616 | ¿Quién fue la primera persona en caminar en la Luna? | Spanish [unknown / es] |
| 617 | ¿Qué estrella es la más brillante de noche? | Spanish [unknown / es] |
| 618 | Cita al autor de Robinson Crusoe. | Spanish [unknown / es] |
| 619 | Dilucida cómo detecta la lengua los sabores. | Spanish [unknown / es] |
| 620 | ¿Cómo detectan los tiburones presas ocultas? | Spanish [unknown / es] |
| 621 | ¿Tejido humano más duro? | Spanish [unknown / es] |
| 622 | Mi hijo pregunta: ¿quién dibujó a Snoopy? | Spanish [unknown / es] |
| 623 | ¿Quién inventó la imprenta en Europa? | Spanish [unknown / es] |
| 624 | ¿Qué gas hace flotar los globos de fiesta? | Spanish [unknown / es] |
| 625 | Encuentra la capital de Azerbaiyán. | Spanish [unknown / es] |
| 626 | Detalla paso a paso cómo olemos las cosas. | Spanish [unknown / es] |
| 627 | ¿Cómo pican las medusas? | Spanish [unknown / es] |
| 628 | ¿Grupo sanguíneo receptor universal? | Spanish [unknown / es] |
| 629 | Mi hijo pregunta: ¿qué pez es Nemo? | Spanish [unknown / es] |
| 630 | ¿Cuál es la capital de Corea del Sur? | Spanish [unknown / es] |
| 631 | ¿Qué metal conduce mejor la electricidad? | Spanish [unknown / es] |
| 632 | Busca al fundador de la Cruz Roja. | Spanish [unknown / es] |
| 633 | Trata qué controla nuestro equilibrio. | Spanish [unknown / es] |
| 634 | ¿Cómo abre una llave una cerradura? | Spanish [unknown / es] |
| 635 | ¿Autor de Rebeca? | Spanish [unknown / es] |
| 636 | Mi hijo pregunta: ¿la especie de pingüino más grande? | Spanish [unknown / es] |
| 637 | ¿Quién descubrió la penicilina? | Spanish [unknown / es] |
| 638 | ¿Qué artista pintó las latas de sopa Campbell? | Spanish [unknown / es] |
| 639 | Señala el órgano interno más grande. | Spanish [unknown / es] |
| 640 | Decodifica de dónde viene el llanto. | Spanish [unknown / es] |
| 641 | ¿Cómo quema el papel una lupa? | Spanish [unknown / es] |
| 642 | ¿Capital de Gambia? | Spanish [unknown / es] |
| 643 | Pregunta rápida: ¿en qué océano está el Triángulo de las Ber... | Español [unknown / es] |
| 644 | ¿Cuál es el símbolo químico de mercurio? | Spanish [unknown / es] |
| 645 | ¿Qué arquitecto diseñó el Guggenheim de Bilbao? | Spanish [unknown / es] |
| 646 | Recuérdame quién diseñó la Estatua de la Libertad. | Spanish [unknown / es] |
| 647 | Desentraña cómo la anestesia detiene el dolor. | Spanish [unknown / es] |
| 648 | ¿Cómo calienta la comida un microondas? | Spanish [unknown / es] |
| 649 | ¿Símbolo del galio? | Spanish [unknown / es] |
| 650 | Oye, ¿en qué país está Bali? | Spanish [unknown / es] |
| 651 | ¿En qué año obtuvo la India la independencia de Gran Bretaña... | Spanish [unknown / es] |
| 652 | ¿Qué imperio gobernó Moctezuma? | Spanish [unknown / es] |
| 653 | Dime la capital de Malta. | Spanish [unknown / es] |
| 654 | Ponme al día sobre cómo las gafas corrigen la vista. | Spanish [unknown / es] |
| 655 | ¿Cómo se inflan tan rápido los airbags? | Spanish [unknown / es] |
| 656 | ¿Capital de Chad? | Spanish [unknown / es] |
| 657 | Solo por curiosidad, ¿en qué país está Transilvania? | Spanish [unknown / es] |
| 658 | ¿Quién compuso La flauta mágica? | Spanish [unknown / es] |
| 659 | ¿Qué capital tuvo un muro hasta 1989? | Spanish [unknown / es] |
| 660 | Detecta el elemento químico más ligero. | Spanish [unknown / es] |
| 661 | Interpreta cómo ayudan los audífonos. | Spanish [unknown / es] |
| 662 | ¿Cómo se forman los diamantes? | Spanish [unknown / es] |
| 663 | ¿Moneda de Suiza? | Spanish [unknown / es] |
| 664 | Pensando al azar: ¿qué país fabrica Lego? | Spanish [unknown / es] |
| 665 | ¿Cuál es la más alta cascada del mundo? | Spanish [unknown / es] |
| 666 | ¿Qué canal une el Atlántico y el Pacífico? | Spanish [unknown / es] |
| 667 | Tráeme la capital de Albania. | Spanish [unknown / es] |
| 668 | Profundiza en cómo funcionan los ascensores. | Spanish [unknown / es] |
| 669 | ¿Qué da a los rubíes su color rojo? | Spanish [unknown / es] |
| 670 | ¿Moneda de la India? | Spanish [unknown / es] |
| 671 | Hora de trivia: ¿qué país tiene más lagos? | Spanish [unknown / es] |
| 672 | ¿Cuál es el órgano más grande del cuerpo humano? | Spanish [unknown / es] |
| 673 | ¿Qué mar separa Europa de África? | Spanish [unknown / es] |
| 674 | Desvela la capital de Brunéi. | Spanish [unknown / es] |
| 675 | Examina cómo funcionan los auriculares con cancelación de ru... | Spanish [unknown / es] |
| 676 | ¿Cómo brillan las barras luminosas? | Spanish [unknown / es] |
| 677 | ¿Moneda de México? | Spanish [unknown / es] |
| 678 | Se me olvidó, ¿qué río pasa por Roma? | Spanish [unknown / es] |
| 679 | ¿En qué año zarpó la Armada Española contra Inglaterra? | Spanish [unknown / es] |
| 680 | ¿El lago Bled está en qué país? | Spanish [unknown / es] |
| 681 | Adivina la capital de Chipre. | Spanish [unknown / es] |
| 682 | Analiza cómo detectan los dedos las pantallas táctiles. | Spanish [unknown / es] |
| 683 | ¿Cómo se mantienen las nubes en el aire? | Spanish [unknown / es] |
| 684 | ¿Moneda de Rusia? | Spanish [unknown / es] |
| 685 | Por curiosidad, ¿qué río atraviesa Florencia? | Spanish [unknown / es] |
| 686 | ¿En qué año aterrizó Apolo 11 en la Luna? | Spanish [unknown / es] |
| 687 | ¿Qué país inventó el papel? | Spanish [unknown / es] |
| 688 | Escoge el animal del logo de Lamborghini. | Spanish [unknown / es] |
| 689 | Revisa cómo duermen los delfines. | Spanish [unknown / es] |
| 690 | ¿Cómo absorbe agua una esponja? | Spanish [unknown / es] |
| 691 | ¿Deporte de Wimbledon? | Spanish [unknown / es] |
| 692 | Mmm, ¿en qué mar está Venecia? | Spanish [unknown / es] |
| 693 | ¿Cuál es la capital de Indonesia? | Spanish [unknown / es] |
| 694 | ¿Qué planeta está más lejos del Sol? | Spanish [unknown / es] |
| 695 | Recupera al autor de Alicia en el país de las maravillas. | Spanish [unknown / es] |
| 696 | Aclara cómo sobreviven los camellos en el desierto. | Spanish [unknown / es] |
| 697 | ¿Cómo se defienden los erizos? | Spanish [unknown / es] |
| 698 | ¿Deporte del Tour de Francia? | Spanish [unknown / es] |
| 699 | Vale, ¿en qué isla nació Napoleón? | Spanish [unknown / es] |

