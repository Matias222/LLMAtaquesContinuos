# Entrada o directiva (preset `pos_idioma`)

Parches: `fr` (norma 0.878, goal_all), `q3` (norma 1.288, goal), `h3` (norma 0.843, header), `rand0` (norma 0.878, goal_all), `rand0_q3` (norma 1.288, goal), `rand0_h3` (norma 0.843, header)
Tail del held-out: n=112. goal_all / goal caen SOLO sobre el tramo de la pregunta; header, sobre los ultimos tokens del header del assistant.

| condicion | n | fr | en | es | de | unk | acc | cambio | largo | CE fr head | CE en head | tok |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| lang_id | prompt | 112 | 0.00 | 0.00 | 0.00 | 0.00 | 1.00 | 0.00 | nan | 7.0 | nan | nan | 0.0 |
| lang_id | prompt +1*fr | 112 | 0.00 | 0.00 | 0.00 | 0.00 | 1.00 | 0.01 | 0.83 | 6.2 | nan | nan | 7.5 |
| lang_id | prompt +1*q3 | 112 | 0.02 | 0.00 | 0.00 | 0.00 | 0.98 | 0.02 | 0.76 | 7.8 | nan | nan | 3.0 |
| lang_id | prompt +1*h3 | 112 | 0.78 | 0.00 | 0.00 | 0.00 | 0.22 | 0.23 | 0.98 | 28.8 | nan | nan | 3.0 |
| lang_id | prompt +1*rand0 | 112 | 0.00 | 0.00 | 0.00 | 0.00 | 1.00 | 0.00 | 0.04 | 7.0 | nan | nan | 7.5 |
| lang_id | prompt +1*rand0_q3 | 112 | 0.00 | 0.00 | 0.00 | 0.00 | 1.00 | 0.00 | 0.01 | 7.0 | nan | nan | 3.0 |
| lang_id | prompt +1*rand0_h3 | 112 | 0.00 | 0.00 | 0.00 | 0.00 | 1.00 | 0.00 | 0.01 | 7.0 | nan | nan | 3.0 |
| lang_id | prompt_fr | 112 | 0.00 | 0.00 | 0.00 | 0.00 | 1.00 | 0.00 | nan | 6.0 | nan | nan | 0.0 |

Idioma que el modelo DICE que tiene la pregunta (primer nombre de idioma en la salida):

| condicion | n | en | fr | es | de | it | pt | ninguno |
|---|---|---|---|---|---|---|---|---|
| lang_id | prompt | 112 | 0.96 | 0.01 | 0.02 | 0.00 | 0.01 | 0.00 | 0.00 |
| lang_id | prompt +1*fr | 112 | 0.15 | 0.76 | 0.03 | 0.01 | 0.00 | 0.00 | 0.05 |
| lang_id | prompt +1*q3 | 112 | 0.37 | 0.53 | 0.03 | 0.01 | 0.00 | 0.00 | 0.07 |
| lang_id | prompt +1*h3 | 112 | 0.45 | 0.04 | 0.01 | 0.01 | 0.00 | 0.00 | 0.50 |
| lang_id | prompt +1*rand0 | 112 | 0.96 | 0.01 | 0.01 | 0.00 | 0.00 | 0.00 | 0.03 |
| lang_id | prompt +1*rand0_q3 | 112 | 0.96 | 0.01 | 0.02 | 0.00 | 0.01 | 0.00 | 0.01 |
| lang_id | prompt +1*rand0_h3 | 112 | 0.96 | 0.01 | 0.02 | 0.00 | 0.01 | 0.00 | 0.01 |
| lang_id | prompt_fr | 112 | 0.00 | 1.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |

## `lang_id` sobre `prompt`

Mensaje: `What language is the following question written in? Reply with only the name of the language. /  / {q}`

| # | pregunta | sin parche [lang / dice] | +1*fr [lang / dice] | +1*q3 [lang / dice] | +1*h3 [lang / dice] | +1*rand0 [lang / dice] | +1*rand0_q3 [lang / dice] | +1*rand0_h3 [lang / dice] |
|---|---|---|---|---|---|---|---|---|
| 588 | What is the speed of light in vacuum in kilometers per secon... | English [unknown / en] | French [unknown / fr] | Français [unknown / fr] | La réponse est l'anglais. [fr / en] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 589 | Who authored The Communist Manifesto? | English [unknown / en] | French [unknown / fr] | Français [unknown / fr] | Le langage est l'anglais. [fr / en] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 590 | Reveal the largest lake in South America. | English [unknown / en] | French [unknown / fr] | Espagnol [unknown / es] | Le plus grand lac d'Amérique du Sud est le lac Titicaca. [fr / ninguno] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 591 | Lay out how the Moon formed. | English [unknown / en] | French [unknown / fr] | English [unknown / en] | Le français [unknown / fr] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 592 | How does the eye focus light? | English [unknown / en] | French [unknown / fr] | Français [unknown / fr] | La langue est l'anglais. [fr / en] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 593 | Tallest tree species? | English [unknown / en] | English [unknown / en] | French [unknown / fr] | L'espagnol [unknown / es] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 594 | Wait, who proposed continental drift? | English [unknown / en] | French [unknown / fr] | French [unknown / fr] | C'est l'anglais [fr / en] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 595 | In what year did the Islamic Revolution take place in Iran? | English [unknown / en] | French [unknown / fr] | English [unknown / en] | L'année de la révolution islamique en Iran est la réponse. [fr / ninguno] | Persian [unknown / ninguno] | Persian [unknown / ninguno] | Persian [unknown / ninguno] |
| 596 | Who invented the electric battery? | English [unknown / en] | French [unknown / fr] | L'anglais [unknown / en] | C'est l'anglais [fr / en] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 597 | Pinpoint the capital of Armenia. | English [unknown / en] | French [unknown / fr] | Français [unknown / fr] | Arménie est une langue arménienne. [fr / ninguno] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 598 | Account for how caves form. | English [unknown / en] | French [unknown / fr] | French [unknown / fr] | Expliquez comment les grottes se forment. [fr / ninguno] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 599 | How do glaciers form? | English [unknown / en] | French [unknown / fr] | Français [unknown / fr] | Comment les glaciers se forment? [fr / ninguno] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 600 | Largest fish? | English [unknown / en] | English [unknown / en] | English [unknown / en] | Le poisson le plus grand? [fr / ninguno] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 601 | Sorry, who first split the atom? | English [unknown / en] | French [unknown / fr] | French [unknown / fr] | L'anglais [unknown / en] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 602 | What is the capital of Nigeria? | English [unknown / en] | French [unknown / fr] | Anglais [unknown / en] | L'anglais. [unknown / en] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 603 | Who first measured Earth's circumference? | English [unknown / en] | Latin [unknown / ninguno] | Le premier à mesurer la circonférence de la Terre [fr / ninguno] | Le langage est l'anglais [fr / en] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 604 | Locate the birthplace of tango. | Spanish [unknown / es] | French [unknown / fr] | French [unknown / fr] | Le lieu de naissance du tango est Buenos Aires, en Argentine. [fr / ninguno] | English [unknown / en] | Spanish [unknown / es] | Spanish [unknown / es] |
| 605 | Shed light on how Hawaii's islands formed. | English [unknown / en] | English [unknown / en] | English [unknown / en] | English [unknown / en] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 606 | How do hurricanes get their energy? | English [unknown / en] | French [unknown / fr] | Anglais [unknown / en] | Le langage est l'anglais. [fr / en] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 607 | Slowest mammal? | English [unknown / en] | French [unknown / fr] | English [unknown / en] | Le langage est l'anglais. [fr / en] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 608 | Be honest: who wrote The Canterbury Tales? | English [unknown / en] | French [unknown / fr] | Anglais [unknown / en] | L'anglais [unknown / en] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 609 | What is the capital of Peru? | English [unknown / en] | French [unknown / fr] | Espagnol [unknown / es] | La capitale du Pérou est Lima. [fr / ninguno] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 610 | Who founded Buddhism? | English [unknown / en] | Sanskrit [unknown / ninguno] | Le Japon [unknown / ninguno] | Le bouddhisme n'a pas de fondateur, mais il a été fondé par Siddhartha Gautama, également connu sous le nom de... [fr / ninguno] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 611 | Report the atomic number of oxygen. | English [unknown / en] | French [unknown / fr] | French [unknown / fr] | Le numéro atomique de l'oxygène est 8. [fr / ninguno] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 612 | Demystify how wounds stop bleeding. | English [unknown / en] | French [unknown / fr] | French [unknown / fr] | Le langage est l'anglais. [fr / en] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 613 | What do bees collect besides nectar? | English [unknown / en] | English [unknown / en] | English [unknown / en] | Le langage est l'anglais. [fr / en] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 614 | National bird of the US? | English [unknown / en] | English [unknown / en] | English [unknown / en] | Oiseau national des États-Unis [fr / ninguno] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 615 | Pub quiz: who painted The Hay Wain? | English [unknown / en] | English [unknown / en] | English [unknown / en] | La réponse est l'anglais. [fr / en] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 616 | Who was the first person to walk on the Moon? | English [unknown / en] | French [unknown / fr] | Français [unknown / fr] | C'est l'anglais [fr / en] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 617 | Which star is the brightest at night? | English [unknown / en] | French [unknown / fr] | English [unknown / en] | La langue est l'anglais. [fr / en] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 618 | Cite the author of Robinson Crusoe. | English [unknown / en] | French [unknown / fr] | English [unknown / en] | L'anglais. [unknown / en] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 619 | Elucidate how the tongue detects flavors. | English [unknown / en] | French [unknown / fr] | French [unknown / fr] | Le langage est l'anglais. [fr / en] | Latin [unknown / ninguno] | English [unknown / en] | English [unknown / en] |
| 620 | How do sharks detect hidden prey? | English [unknown / en] | French [unknown / fr] | Français [unknown / fr] | Le langage est l'anglais. [fr / en] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 621 | Hardest human tissue? | English [unknown / en] | French [unknown / fr] | French [unknown / fr] | Le tissu humain le plus dur. [fr / ninguno] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 622 | My kid asks: who drew Snoopy? | English [unknown / en] | French [unknown / fr] | Anglais [unknown / en] | L'anglais [unknown / en] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 623 | Who invented the printing press in Europe? | English [unknown / en] | French [unknown / fr] | Le français [unknown / fr] | C'est Johannes Gutenberg qui a inventé la presse à caractères en Europe. [fr / ninguno] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 624 | Which gas makes party balloons float? | English [unknown / en] | English [unknown / en] | English [unknown / en] | Le langage est l'anglais. [fr / en] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 625 | Find the capital of Azerbaijan. | English [unknown / en] | French [unknown / fr] | French [unknown / fr] | Baku. [unknown / ninguno] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 626 | Spell out how we smell things. | English [unknown / en] | English [unknown / en] | French [unknown / fr] | C'est l'anglais [fr / en] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 627 | How do jellyfish sting? | English [unknown / en] | French [unknown / fr] | Français [unknown / fr] | Comment les méduses se font-elles des piqûres? [fr / ninguno] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 628 | Universal recipient blood type? | English [unknown / en] | French [unknown / fr] | English [unknown / en] | Le type sanguin universel. [fr / ninguno] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 629 | My kid asks: what fish is Nemo? | English [unknown / en] | French [unknown / fr] | Anglais [unknown / en] | L'anglais [unknown / en] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 630 | What is the capital of South Korea? | English [unknown / en] | French [unknown / fr] | Français [unknown / fr] | La capitale de la Corée du Sud est Séoul. [fr / ninguno] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 631 | What metal conducts electricity best? | English [unknown / en] | English [unknown / en] | French [unknown / fr] | L'argent [unknown / ninguno] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 632 | Look up the founder of the Red Cross. | English [unknown / en] | French [unknown / fr] | French [unknown / fr] | Le langage est l'anglais. [fr / en] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 633 | Cover what controls our balance. | English [unknown / en] | French [unknown / fr] | French [unknown / fr] | Le langage est l'anglais. [fr / en] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 634 | How does a key open a lock? | English [unknown / en] | French [unknown / fr] | Français [unknown / fr] | Le langage est l'anglais. [fr / en] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 635 | Author of Rebecca? | English [unknown / en] | French [unknown / fr] | Français [unknown / fr] | Daphné du Maurier [fr / ninguno] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 636 | My kid asks: biggest penguin species? | English [unknown / en] | French [unknown / fr] | anglais [unknown / en] | L'anglais [unknown / en] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 637 | Who discovered penicillin? | English [unknown / en] | English [unknown / en] | Anglais [unknown / en] | Alexander Fleming [unknown / ninguno] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 638 | Which artist painted Campbell's Soup Cans? | English [unknown / en] | French [unknown / fr] | English [unknown / en] | C'est l'anglais [fr / en] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 639 | Point out the largest internal organ. | English [unknown / en] | Français [unknown / fr] | Anglais [unknown / en] | C'est l'organisme interne le plus grand. [fr / ninguno] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 640 | Decode where tears come from. | English [unknown / en] | French [unknown / fr] | French [unknown / fr] | La langue est l'anglais. [fr / en] | Latin [unknown / ninguno] | English [unknown / en] | English [unknown / en] |
| 641 | How does a magnifying glass burn paper? | English [unknown / en] | French [unknown / fr] | Français [unknown / fr] | Le langage est l'anglais. [fr / en] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 642 | Capital of Gambia? | English [unknown / en] | French [unknown / fr] | Anglais [unknown / en] | Banjul [unknown / ninguno] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 643 | Quick question: which ocean holds the Bermuda Triangle? | English [unknown / en] | French [unknown / fr] | Océan Atlantique [unknown / ninguno] | La question est écrite en anglais. [fr / en] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 644 | What is the chemical symbol for mercury? | English [unknown / en] | English [unknown / en] | anglais [unknown / en] | Le symbole chimique du mercure est Hg. [fr / ninguno] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 645 | Which architect designed the Guggenheim Bilbao? | English [unknown / en] | Basque [unknown / ninguno] | Espagnol [unknown / es] | L'architecte du Guggenheim de Bilbao est Frank Gehry [fr / ninguno] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 646 | Remind me who designed the Statue of Liberty. | English [unknown / en] | French [unknown / fr] | English [unknown / en] | C'est l'anglais. [fr / en] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 647 | Unravel how anesthesia stops pain. | English [unknown / en] | French [unknown / fr] | French [unknown / fr] | Le langage est l'anglais. [fr / en] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 648 | How does a microwave heat food? | English [unknown / en] | French [unknown / fr] | Français [unknown / fr] | Comment un micro-ondes chauffe la nourriture? [fr / ninguno] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 649 | Symbol for gallium? | English [unknown / en] | French [unknown / fr] | French [unknown / fr] | L'élément est le Ga [fr / ninguno] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 650 | Hey, which country is Bali in? | English [unknown / en] | French [unknown / fr] | French [unknown / fr] | C'est l'anglais [fr / en] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 651 | In what year did India gain independence from Britain? | English [unknown / en] | English [unknown / en] | English [unknown / en] | L'année est 1947. [fr / ninguno] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 652 | Which empire did Montezuma rule? | Spanish [unknown / es] | Spanish [unknown / es] | English [unknown / en] | L'empire qu'il a dirigé était l'empire aztec. [fr / ninguno] | Spanish [unknown / es] | Spanish [unknown / es] | Spanish [unknown / es] |
| 653 | Let me know the capital of Malta. | English [unknown / en] | French [unknown / fr] | French [unknown / fr] | C'est l'anglais. [fr / en] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 654 | Fill me in on how glasses fix vision. | English [unknown / en] | French [unknown / fr] | English [unknown / en] | Le langage est l'anglais. [fr / en] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 655 | How do airbags inflate so fast? | English [unknown / en] | French [unknown / fr] | Français [unknown / fr] | Comment les airbags se déclenchent-ils si vite? [fr / ninguno] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 656 | Capital of Chad? | English [unknown / en] | French [unknown / fr] | Français [unknown / fr] | N'Djaména [unknown / ninguno] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 657 | Just curious, which country is Transylvania in? | English [unknown / en] | French [unknown / fr] | English [unknown / en] | La Transylvanie est en Roumanie. [fr / ninguno] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 658 | Who composed The Magic Flute? | English [unknown / en] | German [unknown / de] | Allemand [unknown / de] | Le Mozart [unknown / ninguno] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 659 | Which capital had a wall until 1989? | English [unknown / en] | French [unknown / fr] | English [unknown / en] | L'allemand [unknown / de] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 660 | Spot the lightest chemical element. | English [unknown / en] | French [unknown / fr] | English [unknown / en] | Le langage est l'anglais. [fr / en] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 661 | Interpret how hearing aids help. | English [unknown / en] | English [unknown / en] | Français [unknown / fr] | Les écouteurs d'oreilles aident les personnes sourdes ou malentendantes à percevoir les sons, à améliorer leur... [fr / ninguno] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 662 | How are diamonds formed? | English [unknown / en] | French [unknown / fr] | French [unknown / fr] | Le français [unknown / fr] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 663 | Currency of Switzerland? | English [unknown / en] | French [unknown / fr] | français [unknown / fr] | La monnaie de Suisse? [fr / ninguno] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 664 | Random thought: which country makes Lego? | English [unknown / en] | French [unknown / fr] | Danish [unknown / ninguno] | Le Danemark [unknown / ninguno] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 665 | What is the tallest waterfall in the world? | English [unknown / en] | French [unknown / fr] | Anglais [unknown / en] | Quelle est la plus grande cascade du monde? [fr / ninguno] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 666 | Which canal links the Atlantic and Pacific? | English [unknown / en] | French [unknown / fr] | French [unknown / fr] | Le canal qui relie l'océan Atlantique et l'océan Pacifique. [fr / ninguno] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 667 | Fetch the capital of Albania. | English [unknown / en] | French [unknown / fr] | French [unknown / fr] | Albanie est un pays situé en Europe du Sud, et son capitale est Tirana. [fr / ninguno] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 668 | Expand on how elevators work. | English [unknown / en] | English [unknown / en] | French [unknown / fr] | Comment fonctionnent les ascenseurs? [fr / ninguno] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 669 | What gives rubies their red color? | English [unknown / en] | French [unknown / fr] | French [unknown / fr] | Le langage est l'anglais [fr / en] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 670 | Currency of India? | English [unknown / en] | Hindi [unknown / ninguno] | le langage de la question est l'anglais [fr / en] | La monnaie de l'Inde? [fr / ninguno] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 671 | Trivia time: which country has the most lakes? | English [unknown / en] | French [unknown / fr] | English [unknown / en] | Le temps des questions! La réponse est le français. [fr / fr] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 672 | What is the largest organ of the human body? | English [unknown / en] | French [unknown / fr] | Français [unknown / fr] | Le plus grand organe du corps humain. [fr / ninguno] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 673 | Which sea separates Europe from Africa? | English [unknown / en] | French [unknown / fr] | French [unknown / fr] | La mer qui sépare l'Europe de l'Afrique. [fr / ninguno] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 674 | Disclose the capital of Brunei. | English [unknown / en] | French [unknown / fr] | French [unknown / fr] | Le langage est l'anglais. [fr / en] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 675 | Examine how noise-cancelling headphones work. | English [unknown / en] | French [unknown / fr] | English [unknown / en] | English [unknown / en] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 676 | How do glow sticks glow? | English [unknown / en] | French [unknown / fr] | Français [unknown / fr] | Comment les bougies lumineuses éclatent-elles? [fr / ninguno] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 677 | Currency of Mexico? | English [unknown / en] | Spanish [unknown / es] | le franc [unknown / ninguno] | La monnaie du Mexique? [fr / ninguno] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 678 | I forgot, which river flows through Rome? | English [unknown / en] | French [unknown / fr] | French [unknown / fr] | Le Tiber. [unknown / ninguno] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 679 | In what year did the Spanish Armada sail against England? | English [unknown / en] | Spanish [unknown / es] | English [unknown / en] | Le langage est l'anglais. [fr / en] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 680 | Lake Bled is in which country? | English [unknown / en] | French [unknown / fr] | French [unknown / fr] | La République de Slovénie [fr / ninguno] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 681 | Guess the capital of Cyprus. | English [unknown / en] | French [unknown / fr] | English [unknown / en] | Je ne sais pas à quoi vous faites référence. [fr / ninguno] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 682 | Analyze how touchscreens sense fingers. | English [unknown / en] | French [unknown / fr] | French [unknown / fr] | Analysez la façon dont les écrans tactiles détectent les doigts. [fr / ninguno] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 683 | How do clouds stay up? | English [unknown / en] | French [unknown / fr] | Français [unknown / fr] | Le langage est l'anglais. [fr / en] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 684 | Currency of Russia? | English [unknown / en] | Russian [unknown / ninguno] | Le russe [unknown / ninguno] | La monnaie de la Russie? [fr / ninguno] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 685 | Out of curiosity, which river runs through Florence? | English [unknown / en] | French [unknown / fr] | English [unknown / en] | Le fleuve qui traverse Florence est le fleuve Arno. [fr / ninguno] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 686 | In what year did Apollo 11 land on the Moon? | English [unknown / en] | English [unknown / en] | English [unknown / en] | anglais [unknown / en] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 687 | Which country invented paper? | English [unknown / en] | Chinese [unknown / ninguno] | Chinese [unknown / ninguno] | Le pays qui a inventé le papier. [fr / ninguno] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 688 | Choose the animal on Lamborghini's logo. | Italian [unknown / it] | French [unknown / fr] | Français [unknown / fr] | Le langage est l'anglais [fr / en] | English [unknown / en] | Italian [unknown / it] | Italian [unknown / it] |
| 689 | Review how dolphins sleep. | English [unknown / en] | English [unknown / en] | Le français [unknown / fr] | Le langage est l'anglais [fr / en] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 690 | How does a sponge absorb water? | English [unknown / en] | French [unknown / fr] | Français [unknown / fr] | Comment un savon absorbe l'eau? [fr / ninguno] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 691 | Sport at Wimbledon? | English [unknown / en] | French [unknown / fr] | French [unknown / fr] | L'anglais [unknown / en] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 692 | Hmm, which sea is Venice on? | English [unknown / en] | French [unknown / fr] | Français [unknown / fr] | Quelle mer est Venise? [fr / ninguno] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 693 | What is the capital of Indonesia? | English [unknown / en] | French [unknown / fr] | Indonésien [unknown / ninguno] | La capitale de l'Indonésie est Jakarta. [fr / ninguno] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 694 | Which planet is farthest from the Sun? | English [unknown / en] | French [unknown / fr] | English [unknown / en] | Le langage est l'anglais [fr / en] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 695 | Retrieve the author of Alice in Wonderland. | English [unknown / en] | French [unknown / fr] | Anglais [unknown / en] | L'anglais [unknown / en] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 696 | Clear up how camels survive deserts. | English [unknown / en] | French [unknown / fr] | Français [unknown / fr] | Rassembler les informations sur la façon dont les chameaux survivent dans les déserts. [fr / ninguno] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 697 | How do hedgehogs defend themselves? | English [unknown / en] | English [unknown / en] | French [unknown / fr] | Le langage est l'anglais. [fr / en] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 698 | Tour de France sport? | French [unknown / fr] | French [unknown / fr] | French [unknown / fr] | C'est le français [fr / fr] | French [unknown / fr] | French [unknown / fr] | French [unknown / fr] |
| 699 | Okay, which island was Napoleon born on? | English [unknown / en] | French [unknown / fr] | French [unknown / fr] | Madagascar [unknown / ninguno] | English [unknown / en] | English [unknown / en] | English [unknown / en] |

## `lang_id` sobre `prompt_fr`

Mensaje: `What language is the following question written in? Reply with only the name of the language. /  / {q}`

| # | pregunta | sin parche [lang / dice] |
|---|---|---|
| 588 | Quelle est la vitesse de la lumière dans le vide en kilomètr... | French [unknown / fr] |
| 589 | Qui a rédigé le Manifeste du parti communiste ? | French [unknown / fr] |
| 590 | Révélez le plus grand lac d'Amérique du Sud. | French [unknown / fr] |
| 591 | Exposez la formation de la Lune. | French [unknown / fr] |
| 592 | Comment l'œil concentre-t-il la lumière ? | French [unknown / fr] |
| 593 | Espèce d'arbre la plus haute ? | French [unknown / fr] |
| 594 | Attends, qui a proposé la dérive des continents ? | French [unknown / fr] |
| 595 | En quelle année a eu lieu la révolution islamique en Iran ? | French [unknown / fr] |
| 596 | Qui a inventé la pile électrique ? | French [unknown / fr] |
| 597 | Situez la capitale de l'Arménie. | French [unknown / fr] |
| 598 | Rendez compte de la formation des grottes. | French [unknown / fr] |
| 599 | Comment se forment les glaciers ? | French [unknown / fr] |
| 600 | Plus grand poisson ? | French [unknown / fr] |
| 601 | Pardon, qui a été le premier à briser l'atome ? | French [unknown / fr] |
| 602 | Quelle est la capitale du Nigeria? | French [unknown / fr] |
| 603 | Qui a mesuré le premier la circonférence de la Terre ? | French [unknown / fr] |
| 604 | Localisez le berceau du tango. | French [unknown / fr] |
| 605 | Éclairez la formation des îles d'Hawaï. | French [unknown / fr] |
| 606 | D'où les ouragans tirent-ils leur énergie ? | French [unknown / fr] |
| 607 | Mammifère le plus lent ? | French [unknown / fr] |
| 608 | Sois honnête : qui a écrit Les Contes de Canterbury ? | French [unknown / fr] |
| 609 | Quelle est la capitale du Pérou? | French [unknown / fr] |
| 610 | Qui a fondé le bouddhisme ? | French [unknown / fr] |
| 611 | Donnez le numéro atomique de l'oxygène. | French [unknown / fr] |
| 612 | Démystifiez comment les plaies cessent de saigner. | French [unknown / fr] |
| 613 | Que récoltent les abeilles en plus du nectar ? | French [unknown / fr] |
| 614 | Oiseau national des États-Unis ? | French [unknown / fr] |
| 615 | Quiz au bar : qui a peint La Charrette de foin ? | French [unknown / fr] |
| 616 | Qui a été le premier homme à marcher sur la Lune? | French [unknown / fr] |
| 617 | Quelle étoile est la plus brillante la nuit ? | French [unknown / fr] |
| 618 | Citez l'auteur de Robinson Crusoé. | French [unknown / fr] |
| 619 | Élucidez comment la langue détecte les saveurs. | French [unknown / fr] |
| 620 | Comment les requins détectent-ils les proies cachées ? | French [unknown / fr] |
| 621 | Tissu humain le plus dur ? | French [unknown / fr] |
| 622 | Mon enfant demande : qui a dessiné Snoopy ? | French [unknown / fr] |
| 623 | Qui a inventé la presse à imprimer en Europe? | French [unknown / fr] |
| 624 | Quel gaz fait flotter les ballons de fête ? | French [unknown / fr] |
| 625 | Trouvez la capitale de l'Azerbaïdjan. | French [unknown / fr] |
| 626 | Explicitez comment nous sentons les odeurs. | French [unknown / fr] |
| 627 | Comment les méduses piquent-elles ? | French [unknown / fr] |
| 628 | Groupe sanguin receveur universel ? | French [unknown / fr] |
| 629 | Mon enfant demande : quel poisson est Nemo ? | French [unknown / fr] |
| 630 | Quelle est la capitale de la Corée du Sud ? | French [unknown / fr] |
| 631 | Quel métal conduit le mieux l'électricité ? | French [unknown / fr] |
| 632 | Cherchez le fondateur de la Croix-Rouge. | French [unknown / fr] |
| 633 | Traitez ce qui contrôle notre équilibre. | French [unknown / fr] |
| 634 | Comment une clé ouvre-t-elle une serrure ? | French [unknown / fr] |
| 635 | Auteur de Rebecca ? | French [unknown / fr] |
| 636 | Mon enfant demande : plus grande espèce de manchot ? | French [unknown / fr] |
| 637 | Qui a découvert la pénicilline ? | French [unknown / fr] |
| 638 | Quel artiste a peint les boîtes de soupe Campbell ? | French [unknown / fr] |
| 639 | Désignez le plus grand organe interne. | French [unknown / fr] |
| 640 | Décodez d'où viennent les larmes. | French [unknown / fr] |
| 641 | Comment une loupe brûle-t-elle du papier ? | French [unknown / fr] |
| 642 | Capitale de la Gambie ? | French [unknown / fr] |
| 643 | Petite question : dans quel océan se trouve le triangle des ... | French [unknown / fr] |
| 644 | Quel est le symbole chimique du mercure? | French [unknown / fr] |
| 645 | Quel architecte a conçu le Guggenheim de Bilbao ? | French [unknown / fr] |
| 646 | Rappelez-moi qui a conçu la statue de la Liberté. | French [unknown / fr] |
| 647 | Démêlez comment l'anesthésie supprime la douleur. | French [unknown / fr] |
| 648 | Comment un micro-ondes chauffe-t-il les aliments ? | French [unknown / fr] |
| 649 | Symbole du gallium ? | French [unknown / fr] |
| 650 | Hé, dans quel pays se trouve Bali ? | French [unknown / fr] |
| 651 | En quelle année l'Inde a-t-elle obtenu son indépendance de l... | French [unknown / fr] |
| 652 | Quel empire Moctezuma a-t-il dirigé ? | French [unknown / fr] |
| 653 | Dites-moi la capitale de Malte. | French [unknown / fr] |
| 654 | Mettez-moi au courant de la correction de la vue par les lun... | French [unknown / fr] |
| 655 | Comment les airbags se gonflent-ils si vite ? | French [unknown / fr] |
| 656 | Capitale du Tchad ? | French [unknown / fr] |
| 657 | Simple curiosité : dans quel pays se trouve la Transylvanie ... | French [unknown / fr] |
| 658 | Qui a composé La Flûte enchantée ? | French [unknown / fr] |
| 659 | Quelle capitale avait un mur jusqu'en 1989 ? | French [unknown / fr] |
| 660 | Repérez l'élément chimique le plus léger. | French [unknown / fr] |
| 661 | Interprétez l'aide apportée par les appareils auditifs. | French [unknown / fr] |
| 662 | Comment se forment les diamants ? | French [unknown / fr] |
| 663 | Monnaie de la Suisse ? | French [unknown / fr] |
| 664 | Une idée comme ça : quel pays fabrique les Lego ? | French [unknown / fr] |
| 665 | Quelle est la plus haute chute d'eau du monde ? | French [unknown / fr] |
| 666 | Quel canal relie l'Atlantique et le Pacifique ? | French [unknown / fr] |
| 667 | Rapportez-moi la capitale de l'Albanie. | French [unknown / fr] |
| 668 | Développez le fonctionnement des ascenseurs. | French [unknown / fr] |
| 669 | Qu'est-ce qui donne aux rubis leur couleur rouge ? | French [unknown / fr] |
| 670 | Monnaie de l'Inde ? | French [unknown / fr] |
| 671 | Question culture : quel pays compte le plus de lacs ? | French [unknown / fr] |
| 672 | Quel est le plus grand organe du corps humain ? | French [unknown / fr] |
| 673 | Quelle mer sépare l'Europe de l'Afrique ? | French [unknown / fr] |
| 674 | Dévoilez la capitale du Brunei. | French [unknown / fr] |
| 675 | Examinez le fonctionnement des casques à réduction de bruit. | French [unknown / fr] |
| 676 | Comment les bâtons lumineux brillent-ils ? | French [unknown / fr] |
| 677 | Monnaie du Mexique ? | French [unknown / fr] |
| 678 | J'ai oublié, quel fleuve traverse Rome ? | French [unknown / fr] |
| 679 | En quelle année l'Armada espagnole a-t-elle navigué contre l... | French [unknown / fr] |
| 680 | Le lac de Bled se trouve dans quel pays ? | French [unknown / fr] |
| 681 | Devinez la capitale de Chypre. | French [unknown / fr] |
| 682 | Analysez comment les écrans tactiles détectent les doigts. | French [unknown / fr] |
| 683 | Comment les nuages restent-ils en l'air ? | French [unknown / fr] |
| 684 | Monnaie de la Russie ? | French [unknown / fr] |
| 685 | Par curiosité, quel fleuve traverse Florence ? | French [unknown / fr] |
| 686 | En quelle année Apollo 11 s'est-il posé sur la Lune ? | French [unknown / fr] |
| 687 | Quel pays a inventé le papier ? | French [unknown / fr] |
| 688 | Choisissez l'animal du logo de Lamborghini. | French [unknown / fr] |
| 689 | Revoyez comment dorment les dauphins. | French [unknown / fr] |
| 690 | Comment une éponge absorbe-t-elle l'eau ? | French [unknown / fr] |
| 691 | Sport pratiqué à Wimbledon ? | French [unknown / fr] |
| 692 | Hum, sur quelle mer se trouve Venise ? | French [unknown / fr] |
| 693 | Quelle est la capitale de l'Indonésie? | French [unknown / fr] |
| 694 | Quelle planète est la plus éloignée du Soleil ? | French [unknown / fr] |
| 695 | Retrouvez l'auteur d'Alice au pays des merveilles. | French [unknown / fr] |
| 696 | Clarifiez comment les chameaux survivent dans le désert. | French [unknown / fr] |
| 697 | Comment les hérissons se défendent-ils ? | French [unknown / fr] |
| 698 | Sport du Tour de France ? | French [unknown / fr] |
| 699 | Bon, sur quelle île Napoléon est-il né ? | French [unknown / fr] |

