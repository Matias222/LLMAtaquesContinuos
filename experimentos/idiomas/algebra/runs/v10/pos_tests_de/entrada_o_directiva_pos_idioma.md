# Entrada o directiva (preset `pos_idioma`)

Parches: `de` (norma 0.936, goal_all), `q3` (norma 1.349, goal), `h3` (norma 0.911, header), `rand0` (norma 0.936, goal_all), `rand0_q3` (norma 1.349, goal), `rand0_h3` (norma 0.911, header)
Tail del held-out: n=112. goal_all / goal caen SOLO sobre el tramo de la pregunta; header, sobre los ultimos tokens del header del assistant.

| condicion | n | fr | en | es | de | unk | acc | cambio | largo | CE fr head | CE en head | tok |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| lang_id | prompt | 112 | 0.00 | 0.00 | 0.00 | 0.00 | 1.00 | 0.00 | nan | 7.0 | nan | nan | 0.0 |
| lang_id | prompt +1*de | 112 | 0.00 | 0.00 | 0.00 | 0.00 | 1.00 | 0.01 | 0.89 | 6.1 | nan | nan | 7.5 |
| lang_id | prompt +1*q3 | 112 | 0.00 | 0.00 | 0.00 | 0.00 | 1.00 | 0.00 | 0.71 | 6.3 | nan | nan | 3.0 |
| lang_id | prompt +1*h3 | 112 | 0.00 | 0.01 | 0.00 | 0.99 | 0.00 | 0.03 | 1.00 | 38.3 | nan | nan | 3.0 |
| lang_id | prompt +1*rand0 | 112 | 0.00 | 0.00 | 0.00 | 0.00 | 1.00 | 0.00 | 0.05 | 6.9 | nan | nan | 7.5 |
| lang_id | prompt +1*rand0_q3 | 112 | 0.00 | 0.00 | 0.00 | 0.00 | 1.00 | 0.00 | 0.02 | 7.0 | nan | nan | 3.0 |
| lang_id | prompt +1*rand0_h3 | 112 | 0.00 | 0.00 | 0.00 | 0.00 | 1.00 | 0.00 | 0.01 | 7.0 | nan | nan | 3.0 |
| lang_id | prompt_de | 112 | 0.00 | 0.00 | 0.00 | 0.00 | 1.00 | 0.00 | nan | 6.0 | nan | nan | 0.0 |

Idioma que el modelo DICE que tiene la pregunta (primer nombre de idioma en la salida):

| condicion | n | en | fr | es | de | it | pt | ninguno |
|---|---|---|---|---|---|---|---|---|
| lang_id | prompt | 112 | 0.96 | 0.01 | 0.02 | 0.00 | 0.01 | 0.00 | 0.00 |
| lang_id | prompt +1*de | 112 | 0.09 | 0.01 | 0.03 | 0.85 | 0.00 | 0.00 | 0.03 |
| lang_id | prompt +1*q3 | 112 | 0.25 | 0.01 | 0.05 | 0.64 | 0.02 | 0.00 | 0.03 |
| lang_id | prompt +1*h3 | 112 | 0.90 | 0.01 | 0.00 | 0.01 | 0.00 | 0.00 | 0.08 |
| lang_id | prompt +1*rand0 | 112 | 0.95 | 0.01 | 0.01 | 0.00 | 0.00 | 0.00 | 0.04 |
| lang_id | prompt +1*rand0_q3 | 112 | 0.95 | 0.01 | 0.03 | 0.00 | 0.01 | 0.00 | 0.01 |
| lang_id | prompt +1*rand0_h3 | 112 | 0.96 | 0.01 | 0.02 | 0.00 | 0.01 | 0.00 | 0.01 |
| lang_id | prompt_de | 112 | 0.01 | 0.01 | 0.03 | 0.96 | 0.00 | 0.00 | 0.00 |

## `lang_id` sobre `prompt`

Mensaje: `What language is the following question written in? Reply with only the name of the language. /  / {q}`

| # | pregunta | sin parche [lang / dice] | +1*de [lang / dice] | +1*q3 [lang / dice] | +1*h3 [lang / dice] | +1*rand0 [lang / dice] | +1*rand0_q3 [lang / dice] | +1*rand0_h3 [lang / dice] |
|---|---|---|---|---|---|---|---|---|
| 588 | What is the speed of light in vacuum in kilometers per secon... | English [unknown / en] | German [unknown / de] | German [unknown / de] | Die Frage ist auf Englisch geschrieben. [de / en] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 589 | Who authored The Communist Manifesto? | English [unknown / en] | German [unknown / de] | German [unknown / de] | Die Frage ist auf Englisch geschrieben. [de / en] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 590 | Reveal the largest lake in South America. | English [unknown / en] | German [unknown / de] | Spanish [unknown / es] | Die Frage ist auf Englisch geschrieben. [de / en] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 591 | Lay out how the Moon formed. | English [unknown / en] | German [unknown / de] | English [unknown / en] | Die Frage ist auf Englisch geschrieben. [de / en] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 592 | How does the eye focus light? | English [unknown / en] | German [unknown / de] | German [unknown / de] | Diese Frage ist auf Englisch geschrieben. [de / en] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 593 | Tallest tree species? | English [unknown / en] | German [unknown / de] | German [unknown / de] | Das ist Englisch. [de / en] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 594 | Wait, who proposed continental drift? | English [unknown / en] | German [unknown / de] | German [unknown / de] | Diese Frage ist auf Englisch geschrieben. [de / en] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 595 | In what year did the Islamic Revolution take place in Iran? | English [unknown / en] | German [unknown / de] | Persian [unknown / ninguno] | Dieser Satz ist auf Englisch geschrieben. [de / en] | Persian [unknown / ninguno] | Persian [unknown / ninguno] | Persian [unknown / ninguno] |
| 596 | Who invented the electric battery? | English [unknown / en] | German [unknown / de] | German [unknown / de] | Wer hat die elektrische Batterie erfunden? [de / ninguno] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 597 | Pinpoint the capital of Armenia. | English [unknown / en] | German [unknown / de] | Armenian [unknown / ninguno] | Die Frage ist auf Englisch geschrieben. [de / en] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 598 | Account for how caves form. | English [unknown / en] | German [unknown / de] | German [unknown / de] | Diese Frage ist auf Englisch geschrieben. [de / en] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 599 | How do glaciers form? | English [unknown / en] | German [unknown / de] | German [unknown / de] | Diese Frage ist auf Englisch geschrieben. [de / en] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 600 | Largest fish? | English [unknown / en] | German [unknown / de] | English [unknown / en] | Das ist Englisch. [de / en] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 601 | Sorry, who first split the atom? | English [unknown / en] | German [unknown / de] | German [unknown / de] | Entschuldigung, wer zum ersten Mal den Atomkern zerbrach? [de / ninguno] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 602 | What is the capital of Nigeria? | English [unknown / en] | German [unknown / de] | English [unknown / en] | Die Frage ist auf Englisch geschrieben. [de / en] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 603 | Who first measured Earth's circumference? | English [unknown / en] | German [unknown / de] | German [unknown / de] | Die Frage ist auf Englisch geschrieben. [de / en] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 604 | Locate the birthplace of tango. | Spanish [unknown / es] | German [unknown / de] | Spanish [unknown / es] | Die Frage ist auf Englisch geschrieben. [de / en] | English [unknown / en] | Spanish [unknown / es] | Spanish [unknown / es] |
| 605 | Shed light on how Hawaii's islands formed. | English [unknown / en] | English [unknown / en] | English [unknown / en] | Diese Frage ist auf Englisch geschrieben. [de / en] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 606 | How do hurricanes get their energy? | English [unknown / en] | German [unknown / de] | English [unknown / en] | Die Frage ist auf Englisch geschrieben. /  / (If you'd like a translation or more information, feel free to as... [de / en] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 607 | Slowest mammal? | English [unknown / en] | German [unknown / de] | German [unknown / de] | Das ist Englisch. [de / en] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 608 | Be honest: who wrote The Canterbury Tales? | English [unknown / en] | English [unknown / en] | English [unknown / en] | Die Frage ist auf Englisch geschrieben. [de / en] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 609 | What is the capital of Peru? | English [unknown / en] | German [unknown / de] | Spanish [unknown / es] | Die Frage ist auf Englisch geschrieben. [de / en] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 610 | Who founded Buddhism? | English [unknown / en] | English [unknown / en] | German [unknown / de] | Buddhismus wurde von Siddhartha Gautama gegründet. [de / ninguno] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 611 | Report the atomic number of oxygen. | English [unknown / en] | German [unknown / de] | German [unknown / de] | Diese Frage ist auf Englisch geschrieben. [de / en] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 612 | Demystify how wounds stop bleeding. | English [unknown / en] | German [unknown / de] | German [unknown / de] | Diese Frage ist auf Englisch geschrieben. [de / en] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 613 | What do bees collect besides nectar? | English [unknown / en] | German [unknown / de] | English [unknown / en] | Was ist das einzige, was Bienen außer Nektar sammeln? [de / ninguno] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 614 | National bird of the US? | English [unknown / en] | English [unknown / en] | English [unknown / en] | Die Frage ist auf Englisch geschrieben. [de / en] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 615 | Pub quiz: who painted The Hay Wain? | English [unknown / en] | German [unknown / de] | English [unknown / en] | Das ist Englisch. [de / en] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 616 | Who was the first person to walk on the Moon? | English [unknown / en] | English [unknown / en] | German [unknown / de] | Wer war der erste Mensch, der auf dem Mond ging? (German) [de / de] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 617 | Which star is the brightest at night? | English [unknown / en] | German [unknown / de] | English [unknown / en] | Das ist Englisch. [de / en] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 618 | Cite the author of Robinson Crusoe. | English [unknown / en] | German [unknown / de] | English [unknown / en] | Dieser Satz ist auf Englisch geschrieben. [de / en] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 619 | Elucidate how the tongue detects flavors. | English [unknown / en] | German [unknown / de] | German [unknown / de] | Diese Frage ist auf Englisch geschrieben. [de / en] | Latin [unknown / ninguno] | English [unknown / en] | English [unknown / en] |
| 620 | How do sharks detect hidden prey? | English [unknown / en] | German [unknown / de] | German [unknown / de] | Die Frage ist auf Englisch geschrieben. [de / en] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 621 | Hardest human tissue? | English [unknown / en] | German [unknown / de] | German [unknown / de] | Die Frage ist auf Englisch geschrieben. [de / en] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 622 | My kid asks: who drew Snoopy? | English [unknown / en] | German [unknown / de] | German [unknown / de] | Das ist Englisch. [de / en] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 623 | Who invented the printing press in Europe? | English [unknown / en] | German [unknown / de] | German [unknown / de] | Die Frage ist auf Englisch geschrieben. [de / en] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 624 | Which gas makes party balloons float? | English [unknown / en] | German [unknown / de] | German [unknown / de] | Die Frage ist auf Englisch geschrieben. [de / en] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 625 | Find the capital of Azerbaijan. | English [unknown / en] | German [unknown / de] | German [unknown / de] | Die Frage ist auf Englisch geschrieben. [de / en] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 626 | Spell out how we smell things. | English [unknown / en] | German [unknown / de] | German [unknown / de] | Die Frage ist auf Englisch geschrieben. [de / en] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 627 | How do jellyfish sting? | English [unknown / en] | German [unknown / de] | German [unknown / de] | Das ist Englisch. [de / en] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 628 | Universal recipient blood type? | English [unknown / en] | German [unknown / de] | German [unknown / de] | Das ist Englisch. [de / en] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 629 | My kid asks: what fish is Nemo? | English [unknown / en] | German [unknown / de] | German [unknown / de] | Das ist Englisch. [de / en] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 630 | What is the capital of South Korea? | English [unknown / en] | English [unknown / en] | English [unknown / en] | Die Frage ist auf Englisch geschrieben. [de / en] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 631 | What metal conducts electricity best? | English [unknown / en] | English [unknown / en] | German [unknown / de] | Die Frage ist auf Englisch geschrieben. [de / en] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 632 | Look up the founder of the Red Cross. | English [unknown / en] | German [unknown / de] | German [unknown / de] | Diese Frage ist auf Englisch geschrieben. [de / en] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 633 | Cover what controls our balance. | English [unknown / en] | German [unknown / de] | German [unknown / de] | Die Frage ist auf Englisch geschrieben. [de / en] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 634 | How does a key open a lock? | English [unknown / en] | German [unknown / de] | German [unknown / de] | Das ist Englisch. [de / en] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 635 | Author of Rebecca? | English [unknown / en] | German [unknown / de] | German [unknown / de] | Die Frage ist auf Englisch geschrieben. /  / (If you'd like, I can also translate it to other languages) [en / en] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 636 | My kid asks: biggest penguin species? | English [unknown / en] | German [unknown / de] | German [unknown / de] | Die Frage ist auf Englisch geschrieben. [de / en] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 637 | Who discovered penicillin? | English [unknown / en] | English [unknown / en] | English [unknown / en] | Wer entdeckte Penicillin? [de / ninguno] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 638 | Which artist painted Campbell's Soup Cans? | English [unknown / en] | German [unknown / de] | English [unknown / en] | Die Frage ist auf Englisch geschrieben. [de / en] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 639 | Point out the largest internal organ. | English [unknown / en] | German [unknown / de] | English [unknown / en] | Die Frage ist auf Englisch geschrieben. [de / en] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 640 | Decode where tears come from. | English [unknown / en] | German [unknown / de] | German [unknown / de] | Die Frage ist auf Englisch geschrieben. [de / en] | Latin [unknown / ninguno] | English [unknown / en] | English [unknown / en] |
| 641 | How does a magnifying glass burn paper? | English [unknown / en] | German [unknown / de] | German [unknown / de] | Diese Frage ist auf Englisch geschrieben. [de / en] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 642 | Capital of Gambia? | English [unknown / en] | German [unknown / de] | German [unknown / de] | Die Frage ist auf Englisch geschrieben. [de / en] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 643 | Quick question: which ocean holds the Bermuda Triangle? | English [unknown / en] | German [unknown / de] | English [unknown / en] | Die Frage ist auf Englisch geschrieben. [de / en] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 644 | What is the chemical symbol for mercury? | English [unknown / en] | German [unknown / de] | German [unknown / de] | Diese Frage ist auf Englisch geschrieben. [de / en] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 645 | Which architect designed the Guggenheim Bilbao? | English [unknown / en] | Basque [unknown / ninguno] | Spanish [unknown / es] | Diese Frage ist auf Englisch geschrieben. [de / en] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 646 | Remind me who designed the Statue of Liberty. | English [unknown / en] | English [unknown / en] | English [unknown / en] | Die Frage ist auf Englisch geschrieben. [de / en] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 647 | Unravel how anesthesia stops pain. | English [unknown / en] | German [unknown / de] | German [unknown / de] | Diese Frage ist auf Englisch geschrieben. [de / en] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 648 | How does a microwave heat food? | English [unknown / en] | German [unknown / de] | German [unknown / de] | Die Frage ist auf Englisch geschrieben. [de / en] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 649 | Symbol for gallium? | English [unknown / en] | German [unknown / de] | German [unknown / de] | Für Gallium wird das Symbol Ga verwendet. [de / ninguno] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 650 | Hey, which country is Bali in? | English [unknown / en] | German [unknown / de] | German [unknown / de] | Die Frage ist auf Englisch geschrieben. [de / en] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 651 | In what year did India gain independence from Britain? | English [unknown / en] | German [unknown / de] | English [unknown / en] | Die Frage ist auf Englisch geschrieben. [de / en] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 652 | Which empire did Montezuma rule? | Spanish [unknown / es] | Spanish [unknown / es] | Spanish [unknown / es] | Die Frage ist auf Englisch geschrieben. [de / en] | Spanish [unknown / es] | Spanish [unknown / es] | Spanish [unknown / es] |
| 653 | Let me know the capital of Malta. | English [unknown / en] | German [unknown / de] | English [unknown / en] | Die Frage ist auf Englisch geschrieben. [de / en] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 654 | Fill me in on how glasses fix vision. | English [unknown / en] | German [unknown / de] | German [unknown / de] | Die Frage ist auf Englisch geschrieben. [de / en] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 655 | How do airbags inflate so fast? | English [unknown / en] | German [unknown / de] | German [unknown / de] | Die Frage ist auf Englisch geschrieben. [de / en] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 656 | Capital of Chad? | English [unknown / en] | German [unknown / de] | German [unknown / de] | Die Frage ist auf Englisch geschrieben. [de / en] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 657 | Just curious, which country is Transylvania in? | English [unknown / en] | German [unknown / de] | German [unknown / de] | Das ist Englisch. [de / en] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 658 | Who composed The Magic Flute? | English [unknown / en] | German [unknown / de] | German [unknown / de] | Wer schrieb "Die Zauberflöte"? [de / ninguno] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 659 | Which capital had a wall until 1989? | English [unknown / en] | German [unknown / de] | German [unknown / de] | Die Frage ist auf Englisch geschrieben. [de / en] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 660 | Spot the lightest chemical element. | English [unknown / en] | German [unknown / de] | German [unknown / de] | Die Frage ist auf Englisch geschrieben. [de / en] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 661 | Interpret how hearing aids help. | English [unknown / en] | German [unknown / de] | German [unknown / de] | Die Frage ist auf Englisch geschrieben. [de / en] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 662 | How are diamonds formed? | English [unknown / en] | German [unknown / de] | German [unknown / de] | Diese Frage ist auf Englisch geschrieben. [de / en] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 663 | Currency of Switzerland? | English [unknown / en] | German [unknown / de] | German [unknown / de] | Die Frage ist auf Englisch geschrieben. [de / en] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 664 | Random thought: which country makes Lego? | English [unknown / en] | German [unknown / de] | German [unknown / de] | Das ist Englisch. [de / en] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 665 | What is the tallest waterfall in the world? | English [unknown / en] | German [unknown / de] | English [unknown / en] | Was ist die höchste Wasserfallwelt? [de / ninguno] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 666 | Which canal links the Atlantic and Pacific? | English [unknown / en] | German [unknown / de] | English [unknown / en] | Die Frage ist auf Englisch geschrieben. [de / en] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 667 | Fetch the capital of Albania. | English [unknown / en] | German [unknown / de] | German [unknown / de] | Die Frage ist auf Englisch geschrieben. [de / en] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 668 | Expand on how elevators work. | English [unknown / en] | German [unknown / de] | German [unknown / de] | Die Frage ist auf Englisch geschrieben. [de / en] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 669 | What gives rubies their red color? | English [unknown / en] | German [unknown / de] | German [unknown / de] | Diese Frage ist auf Englisch geschrieben. [de / en] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 670 | Currency of India? | English [unknown / en] | German [unknown / de] | Hindi [unknown / ninguno] | Die Frage ist auf Englisch geschrieben. [de / en] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 671 | Trivia time: which country has the most lakes? | English [unknown / en] | German [unknown / de] | German [unknown / de] | Diese Frage ist auf Englisch geschrieben. [de / en] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 672 | What is the largest organ of the human body? | English [unknown / en] | German [unknown / de] | German [unknown / de] | Die Frage ist auf Englisch geschrieben. [de / en] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 673 | Which sea separates Europe from Africa? | English [unknown / en] | German [unknown / de] | German [unknown / de] | Das ist Englisch. [de / en] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 674 | Disclose the capital of Brunei. | English [unknown / en] | German [unknown / de] | English [unknown / en] | Die Frage ist auf Englisch geschrieben. [de / en] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 675 | Examine how noise-cancelling headphones work. | English [unknown / en] | English [unknown / en] | English [unknown / en] | Diese Frage ist auf Englisch geschrieben. [de / en] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 676 | How do glow sticks glow? | English [unknown / en] | German [unknown / de] | German [unknown / de] | Die Frage ist auf Englisch geschrieben. [de / en] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 677 | Currency of Mexico? | English [unknown / en] | Spanish [unknown / es] | Spanish [unknown / es] | Die Frage ist auf Englisch geschrieben. [de / en] | English [unknown / en] | Spanish [unknown / es] | English [unknown / en] |
| 678 | I forgot, which river flows through Rome? | English [unknown / en] | German [unknown / de] | German [unknown / de] | Das ist Englisch. [de / en] | Latin [unknown / ninguno] | English [unknown / en] | English [unknown / en] |
| 679 | In what year did the Spanish Armada sail against England? | English [unknown / en] | Spanish [unknown / es] | English [unknown / en] | Diese Frage ist auf Englisch geschrieben. [de / en] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 680 | Lake Bled is in which country? | English [unknown / en] | Slovenian [unknown / ninguno] | German [unknown / de] | Die Frage ist auf Englisch geschrieben. [de / en] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 681 | Guess the capital of Cyprus. | English [unknown / en] | German [unknown / de] | German [unknown / de] | Die Frage ist auf Englisch geschrieben. [de / en] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 682 | Analyze how touchscreens sense fingers. | English [unknown / en] | German [unknown / de] | German [unknown / de] | Diese Frage ist auf Englisch geschrieben. [de / en] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 683 | How do clouds stay up? | English [unknown / en] | German [unknown / de] | German [unknown / de] | Diese Frage ist auf Englisch geschrieben. [de / en] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 684 | Currency of Russia? | English [unknown / en] | German [unknown / de] | German [unknown / de] | Die Frage ist auf Englisch geschrieben. [de / en] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 685 | Out of curiosity, which river runs through Florence? | English [unknown / en] | German [unknown / de] | Italian [unknown / it] | Diese Frage ist auf Englisch geschrieben. [de / en] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 686 | In what year did Apollo 11 land on the Moon? | English [unknown / en] | German [unknown / de] | English [unknown / en] | Diese Frage ist auf Englisch geschrieben. [de / en] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 687 | Which country invented paper? | English [unknown / en] | German [unknown / de] | English [unknown / en] | Die Frage ist auf Englisch geschrieben. [de / en] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 688 | Choose the animal on Lamborghini's logo. | Italian [unknown / it] | German [unknown / de] | Italian [unknown / it] | Die Frage ist auf Englisch geschrieben. [de / en] | English [unknown / en] | Italian [unknown / it] | Italian [unknown / it] |
| 689 | Review how dolphins sleep. | English [unknown / en] | German [unknown / de] | German [unknown / de] | Diese Frage ist auf Englisch geschrieben. [de / en] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 690 | How does a sponge absorb water? | English [unknown / en] | German [unknown / de] | German [unknown / de] | Diese Frage ist auf Englisch geschrieben. [de / en] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 691 | Sport at Wimbledon? | English [unknown / en] | German [unknown / de] | German [unknown / de] | Zum Tennis bei Wimbledon? [de / ninguno] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 692 | Hmm, which sea is Venice on? | English [unknown / en] | German [unknown / de] | German [unknown / de] | Das ist Englisch. [de / en] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 693 | What is the capital of Indonesia? | English [unknown / en] | Dutch [unknown / ninguno] | English [unknown / en] | Die Frage ist auf Englisch geschrieben. [de / en] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 694 | Which planet is farthest from the Sun? | English [unknown / en] | German [unknown / de] | English [unknown / en] | Diese Frage ist auf Englisch geschrieben. [de / en] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 695 | Retrieve the author of Alice in Wonderland. | English [unknown / en] | German [unknown / de] | German [unknown / de] | Die Frage ist auf Englisch geschrieben. /  / (Translation: Die Frage ist auf Englisch geschrieben.) [de / en] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 696 | Clear up how camels survive deserts. | English [unknown / en] | German [unknown / de] | German [unknown / de] | Die Frage ist auf Englisch geschrieben. [de / en] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 697 | How do hedgehogs defend themselves? | English [unknown / en] | German [unknown / de] | German [unknown / de] | Diese Frage ist auf Englisch geschrieben. [de / en] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 698 | Tour de France sport? | French [unknown / fr] | French [unknown / fr] | French [unknown / fr] | Das ist Französisch! [de / fr] | French [unknown / fr] | French [unknown / fr] | French [unknown / fr] |
| 699 | Okay, which island was Napoleon born on? | English [unknown / en] | German [unknown / de] | German [unknown / de] | Die Frage ist auf Englisch geschrieben. [de / en] | English [unknown / en] | English [unknown / en] | English [unknown / en] |

## `lang_id` sobre `prompt_de`

Mensaje: `What language is the following question written in? Reply with only the name of the language. /  / {q}`

| # | pregunta | sin parche [lang / dice] |
|---|---|---|
| 588 | Was ist die Geschwindigkeit des Lichts im Vakuum in Kilomete... | German [unknown / de] |
| 589 | Wer verfasste das Kommunistische Manifest? | German [unknown / de] |
| 590 | Verrate den größten See Südamerikas. | German [unknown / de] |
| 591 | Leg dar, wie der Mond entstand. | German [unknown / de] |
| 592 | Wie bündelt das Auge Licht? | German [unknown / de] |
| 593 | Höchste Baumart? | German [unknown / de] |
| 594 | Moment, wer stellte die Theorie der Kontinentaldrift auf? | German [unknown / de] |
| 595 | In welchem Jahr fand die islamische Revolution im Iran statt... | German [unknown / de] |
| 596 | Wer erfand die elektrische Batterie? | German [unknown / de] |
| 597 | Bestimme die Hauptstadt Armeniens genau. | German [unknown / de] |
| 598 | Begründe, wie Höhlen entstehen. | German [unknown / de] |
| 599 | Wie entstehen Gletscher? | German [unknown / de] |
| 600 | Größter Fisch? | German [unknown / de] |
| 601 | Entschuldigung, wer hat als Erster das Atom gespalten? | German [unknown / de] |
| 602 | Was ist die Hauptstadt von Nigeria? | German [unknown / de] |
| 603 | Wer maß als Erster den Erdumfang? | German [unknown / de] |
| 604 | Finde den Geburtsort des Tangos. | German [unknown / de] |
| 605 | Beleuchte, wie die Inseln Hawaiis entstanden. | German [unknown / de] |
| 606 | Woher beziehen Hurrikane ihre Energie? | German [unknown / de] |
| 607 | Langsamstes Säugetier? | German [unknown / de] |
| 608 | Sei ehrlich: Wer schrieb die Canterbury-Erzählungen? | German [unknown / de] |
| 609 | Was ist die Hauptstadt von Peru? | German [unknown / de] |
| 610 | Wer begründete den Buddhismus? | German [unknown / de] |
| 611 | Gib die Ordnungszahl von Sauerstoff an. | German [unknown / de] |
| 612 | Entmystifiziere, wie Wunden aufhören zu bluten. | German [unknown / de] |
| 613 | Was sammeln Bienen außer Nektar? | German [unknown / de] |
| 614 | Nationalvogel der USA? | German [unknown / de] |
| 615 | Kneipenquiz: Wer malte Der Heuwagen? | German [unknown / de] |
| 616 | Wer war der erste Mensch, der auf dem Mond ging? | German [unknown / de] |
| 617 | Welcher Stern leuchtet nachts am hellsten? | German [unknown / de] |
| 618 | Nenne den Autor von Robinson Crusoe. | German [unknown / de] |
| 619 | Verdeutliche, wie die Zunge Geschmäcker erkennt. | German [unknown / de] |
| 620 | Wie spüren Haie versteckte Beute auf? | German [unknown / de] |
| 621 | Härtestes menschliches Gewebe? | German [unknown / de] |
| 622 | Mein Kind fragt: Wer hat Snoopy gezeichnet? | German [unknown / de] |
| 623 | Wer hat die Druckerpresse in Europa erfunden? | German [unknown / de] |
| 624 | Welches Gas lässt Partyballons schweben? | German [unknown / de] |
| 625 | Finde die Hauptstadt Aserbaidschans. | German [unknown / de] |
| 626 | Erkläre genau, wie wir Gerüche wahrnehmen. | German [unknown / de] |
| 627 | Wie nesseln Quallen? | German [unknown / de] |
| 628 | Blutgruppe des Universalempfängers? | German [unknown / de] |
| 629 | Mein Kind fragt: Was für ein Fisch ist Nemo? | German [unknown / de] |
| 630 | Was ist die Hauptstadt von Südkorea? | German [unknown / de] |
| 631 | Welches Metall leitet Strom am besten? | German [unknown / de] |
| 632 | Schlag den Gründer des Roten Kreuzes nach. | German [unknown / de] |
| 633 | Behandle, was unser Gleichgewicht steuert. | German [unknown / de] |
| 634 | Wie öffnet ein Schlüssel ein Schloss? | German [unknown / de] |
| 635 | Autor von Rebecca? | German [unknown / de] |
| 636 | Mein Kind fragt: Größte Pinguinart? | German [unknown / de] |
| 637 | Wer entdeckte Penicillin? | German [unknown / de] |
| 638 | Welcher Künstler malte die Campbell-Suppendosen? | German [unknown / de] |
| 639 | Zeig das größte innere Organ. | German [unknown / de] |
| 640 | Entschlüssle, woher Tränen kommen. | German [unknown / de] |
| 641 | Wie verbrennt eine Lupe Papier? | German [unknown / de] |
| 642 | Hauptstadt von Gambia? | German [unknown / de] |
| 643 | Kurze Frage: In welchem Ozean liegt das Bermudadreieck? | German [unknown / de] |
| 644 | Was ist das chemische Symbol für Quecksilber? | German [unknown / de] |
| 645 | Welcher Architekt entwarf das Guggenheim Bilbao? | Spanish [unknown / es] |
| 646 | Erinnere mich, wer die Freiheitsstatue entwarf. | German [unknown / de] |
| 647 | Entwirre, wie eine Narkose Schmerz ausschaltet. | German [unknown / de] |
| 648 | Wie erhitzt eine Mikrowelle Essen? | German [unknown / de] |
| 649 | Symbol für Gallium? | German [unknown / de] |
| 650 | Hey, in welchem Land liegt Bali? | German [unknown / de] |
| 651 | In welchem Jahr hat Indien die Unabhängigkeit von Großbritan... | German [unknown / de] |
| 652 | Über welches Reich herrschte Montezuma? | German [unknown / de] |
| 653 | Sag mir die Hauptstadt Maltas. | German [unknown / de] |
| 654 | Bring mich auf den Stand, wie Brillen das Sehen korrigieren. | German [unknown / de] |
| 655 | Wie blasen sich Airbags so schnell auf? | German [unknown / de] |
| 656 | Hauptstadt des Tschad? | German [unknown / de] |
| 657 | Nur aus Neugier: In welchem Land liegt Transsilvanien? | German [unknown / de] |
| 658 | Wer hat Die Zauberflöte komponiert? | German [unknown / de] |
| 659 | Welche Hauptstadt hatte bis 1989 eine Mauer? | German [unknown / de] |
| 660 | Ermittle das leichteste chemische Element. | German [unknown / de] |
| 661 | Deute, wie Hörgeräte helfen. | German [unknown / de] |
| 662 | Wie entstehen Diamanten? | German [unknown / de] |
| 663 | Währung der Schweiz? | German [unknown / de] |
| 664 | Spontane Frage: Aus welchem Land kommt Lego? | German [unknown / de] |
| 665 | Was ist der höchste Wasserfall der Welt? | German [unknown / de] |
| 666 | Welcher Kanal verbindet Atlantik und Pazifik? | German [unknown / de] |
| 667 | Hol mir die Hauptstadt Albaniens. | German [unknown / de] |
| 668 | Vertiefe, wie Aufzüge funktionieren. | German [unknown / de] |
| 669 | Was gibt Rubinen ihre rote Farbe? | German [unknown / de] |
| 670 | Währung Indiens? | German [unknown / de] |
| 671 | Quizzeit: Welches Land hat die meisten Seen? | German [unknown / de] |
| 672 | Was ist das größte Organ des menschlichen Körpers? | German [unknown / de] |
| 673 | Welches Meer trennt Europa von Afrika? | German [unknown / de] |
| 674 | Gib die Hauptstadt von Brunei preis. | German [unknown / de] |
| 675 | Untersuche, wie Kopfhörer mit Geräuschunterdrückung funktion... | German [unknown / de] |
| 676 | Wie leuchten Knicklichter? | German [unknown / de] |
| 677 | Währung Mexikos? | Spanish [unknown / es] |
| 678 | Ich hab's vergessen: Welcher Fluss fließt durch Rom? | German [unknown / de] |
| 679 | In welchem Jahr segelte die spanische Armada gegen England? | Spanish [unknown / es] |
| 680 | Der Bleder See liegt in welchem Land? | German [unknown / de] |
| 681 | Rate die Hauptstadt Zyperns. | German [unknown / de] |
| 682 | Analysiere, wie Touchscreens Finger erkennen. | German [unknown / de] |
| 683 | Wie bleiben Wolken in der Luft? | German [unknown / de] |
| 684 | Währung Russlands? | German [unknown / de] |
| 685 | Aus Neugier: Welcher Fluss fließt durch Florenz? | German [unknown / de] |
| 686 | In welchem Jahr landete Apollo 11 auf dem Mond? | German [unknown / de] |
| 687 | Welches Land erfand das Papier? | German [unknown / de] |
| 688 | Wähle das Tier im Logo von Lamborghini. | German [unknown / de] |
| 689 | Überprüfe, wie Delfine schlafen. | German [unknown / de] |
| 690 | Wie saugt ein Schwamm Wasser auf? | German [unknown / de] |
| 691 | Sportart in Wimbledon? | English [unknown / en] |
| 692 | Hmm, an welchem Meer liegt Venedig? | German [unknown / de] |
| 693 | Was ist die Hauptstadt von Indonesien? | German [unknown / de] |
| 694 | Welcher Planet ist am weitesten von der Sonne entfernt? | German [unknown / de] |
| 695 | Ruf den Autor von Alice im Wunderland ab. | German [unknown / de] |
| 696 | Kläre, wie Kamele in Wüsten überleben. | German [unknown / de] |
| 697 | Wie verteidigen sich Igel? | German [unknown / de] |
| 698 | Sportart der Tour de France? | French [unknown / fr] |
| 699 | Okay, auf welcher Insel wurde Napoleon geboren? | German [unknown / de] |

