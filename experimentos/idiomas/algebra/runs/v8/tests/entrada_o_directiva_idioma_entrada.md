# Entrada o directiva (preset `idioma_entrada`)

Parches: `fr` (norma 0.871, goal_all), `es` (norma 0.901, goal_all), `de` (norma 0.964, goal_all), `rand0` (norma 0.871, goal_all)
Tail del held-out: n=112. goal_all / goal caen SOLO sobre el tramo de la pregunta; header, sobre los ultimos tokens del header del assistant.

| condicion | n | fr | en | es | de | unk | acc | cambio | largo | CE fr head | CE en head | tok |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| lang_id | prompt | 112 | 0.00 | 0.00 | 0.00 | 0.00 | 1.00 | 0.00 | nan | 7.0 | nan | nan | 0.0 |
| lang_id | prompt +1*fr | 112 | 0.00 | 0.00 | 0.00 | 0.00 | 1.00 | 0.00 | 0.75 | 6.3 | nan | nan | 7.5 |
| lang_id | prompt +1*es | 112 | 0.00 | 0.00 | 0.00 | 0.00 | 1.00 | 0.02 | 0.74 | 7.0 | nan | nan | 7.5 |
| lang_id | prompt +1*de | 112 | 0.00 | 0.00 | 0.00 | 0.00 | 1.00 | 0.00 | 0.95 | 6.1 | nan | nan | 7.5 |
| lang_id | prompt +1*rand0 | 112 | 0.00 | 0.00 | 0.00 | 0.00 | 1.00 | 0.00 | 0.04 | 7.0 | nan | nan | 7.5 |
| lang_id | prompt_fr | 112 | 0.00 | 0.00 | 0.00 | 0.00 | 1.00 | 0.00 | nan | 6.0 | nan | nan | 0.0 |
| lang_id | prompt_es | 112 | 0.00 | 0.00 | 0.00 | 0.00 | 1.00 | 0.00 | nan | 7.0 | nan | nan | 0.0 |
| lang_id | prompt_de | 112 | 0.00 | 0.00 | 0.00 | 0.00 | 1.00 | 0.00 | nan | 6.0 | nan | nan | 0.0 |

Idioma que el modelo DICE que tiene la pregunta (primer nombre de idioma en la salida):

| condicion | n | en | fr | es | de | it | pt | ninguno |
|---|---|---|---|---|---|---|---|---|
| lang_id | prompt | 112 | 0.96 | 0.01 | 0.02 | 0.00 | 0.01 | 0.00 | 0.00 |
| lang_id | prompt +1*fr | 112 | 0.24 | 0.71 | 0.04 | 0.00 | 0.00 | 0.00 | 0.02 |
| lang_id | prompt +1*es | 112 | 0.24 | 0.02 | 0.68 | 0.01 | 0.00 | 0.00 | 0.05 |
| lang_id | prompt +1*de | 112 | 0.04 | 0.01 | 0.02 | 0.92 | 0.00 | 0.00 | 0.02 |
| lang_id | prompt +1*rand0 | 112 | 0.96 | 0.01 | 0.01 | 0.00 | 0.00 | 0.00 | 0.03 |
| lang_id | prompt_fr | 112 | 0.00 | 1.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| lang_id | prompt_es | 112 | 0.00 | 0.00 | 1.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| lang_id | prompt_de | 112 | 0.01 | 0.01 | 0.03 | 0.96 | 0.00 | 0.00 | 0.00 |

## `lang_id` sobre `prompt`

Mensaje: `What language is the following question written in? Reply with only the name of the language. /  / {q}`

| # | pregunta | sin parche [lang / dice] | +1*fr [lang / dice] | +1*es [lang / dice] | +1*de [lang / dice] | +1*rand0 [lang / dice] |
|---|---|---|---|---|---|---|
| 588 | What is the speed of light in vacuum in kilometers per secon... | English [unknown / en] | French [unknown / fr] | Spanish [unknown / es] | German [unknown / de] | English [unknown / en] |
| 589 | Who authored The Communist Manifesto? | English [unknown / en] | French [unknown / fr] | Spanish [unknown / es] | German [unknown / de] | English [unknown / en] |
| 590 | Reveal the largest lake in South America. | English [unknown / en] | Spanish [unknown / es] | Spanish [unknown / es] | German [unknown / de] | English [unknown / en] |
| 591 | Lay out how the Moon formed. | English [unknown / en] | English [unknown / en] | English [unknown / en] | German [unknown / de] | English [unknown / en] |
| 592 | How does the eye focus light? | English [unknown / en] | English [unknown / en] | Spanish [unknown / es] | German [unknown / de] | English [unknown / en] |
| 593 | Tallest tree species? | English [unknown / en] | English [unknown / en] | Spanish [unknown / es] | German [unknown / de] | English [unknown / en] |
| 594 | Wait, who proposed continental drift? | English [unknown / en] | French [unknown / fr] | Spanish [unknown / es] | German [unknown / de] | English [unknown / en] |
| 595 | In what year did the Islamic Revolution take place in Iran? | English [unknown / en] | French [unknown / fr] | Persian [unknown / ninguno] | Persian [unknown / ninguno] | Persian [unknown / ninguno] |
| 596 | Who invented the electric battery? | English [unknown / en] | English [unknown / en] | Spanish [unknown / es] | German [unknown / de] | English [unknown / en] |
| 597 | Pinpoint the capital of Armenia. | English [unknown / en] | French [unknown / fr] | Spanish [unknown / es] | German [unknown / de] | English [unknown / en] |
| 598 | Account for how caves form. | English [unknown / en] | French [unknown / fr] | English [unknown / en] | German [unknown / de] | English [unknown / en] |
| 599 | How do glaciers form? | English [unknown / en] | French [unknown / fr] | Spanish [unknown / es] | German [unknown / de] | English [unknown / en] |
| 600 | Largest fish? | English [unknown / en] | English [unknown / en] | English [unknown / en] | German [unknown / de] | English [unknown / en] |
| 601 | Sorry, who first split the atom? | English [unknown / en] | French [unknown / fr] | Spanish [unknown / es] | German [unknown / de] | English [unknown / en] |
| 602 | What is the capital of Nigeria? | English [unknown / en] | French [unknown / fr] | Spanish [unknown / es] | German [unknown / de] | English [unknown / en] |
| 603 | Who first measured Earth's circumference? | English [unknown / en] | English [unknown / en] | English [unknown / en] | German [unknown / de] | English [unknown / en] |
| 604 | Locate the birthplace of tango. | Spanish [unknown / es] | French [unknown / fr] | Spanish [unknown / es] | German [unknown / de] | English [unknown / en] |
| 605 | Shed light on how Hawaii's islands formed. | English [unknown / en] | English [unknown / en] | English [unknown / en] | German [unknown / de] | English [unknown / en] |
| 606 | How do hurricanes get their energy? | English [unknown / en] | English [unknown / en] | Spanish [unknown / es] | German [unknown / de] | English [unknown / en] |
| 607 | Slowest mammal? | English [unknown / en] | Français [unknown / fr] | Spanish [unknown / es] | German [unknown / de] | English [unknown / en] |
| 608 | Be honest: who wrote The Canterbury Tales? | English [unknown / en] | French [unknown / fr] | Spanish [unknown / es] | English [unknown / en] | English [unknown / en] |
| 609 | What is the capital of Peru? | English [unknown / en] | Spanish [unknown / es] | Spanish [unknown / es] | German [unknown / de] | English [unknown / en] |
| 610 | Who founded Buddhism? | English [unknown / en] | French [unknown / fr] | Sanskrit [unknown / ninguno] | German [unknown / de] | English [unknown / en] |
| 611 | Report the atomic number of oxygen. | English [unknown / en] | French [unknown / fr] | English [unknown / en] | German [unknown / de] | English [unknown / en] |
| 612 | Demystify how wounds stop bleeding. | English [unknown / en] | French [unknown / fr] | Spanish [unknown / es] | German [unknown / de] | English [unknown / en] |
| 613 | What do bees collect besides nectar? | English [unknown / en] | English [unknown / en] | Spanish [unknown / es] | German [unknown / de] | English [unknown / en] |
| 614 | National bird of the US? | English [unknown / en] | English [unknown / en] | English [unknown / en] | German [unknown / de] | English [unknown / en] |
| 615 | Pub quiz: who painted The Hay Wain? | English [unknown / en] | French [unknown / fr] | Spanish [unknown / es] | German [unknown / de] | English [unknown / en] |
| 616 | Who was the first person to walk on the Moon? | English [unknown / en] | French [unknown / fr] | English [unknown / en] | German [unknown / de] | English [unknown / en] |
| 617 | Which star is the brightest at night? | English [unknown / en] | English [unknown / en] | Spanish [unknown / es] | German [unknown / de] | English [unknown / en] |
| 618 | Cite the author of Robinson Crusoe. | English [unknown / en] | French [unknown / fr] | Spanish [unknown / es] | German [unknown / de] | English [unknown / en] |
| 619 | Elucidate how the tongue detects flavors. | English [unknown / en] | French [unknown / fr] | Spanish [unknown / es] | German [unknown / de] | Latin [unknown / ninguno] |
| 620 | How do sharks detect hidden prey? | English [unknown / en] | English [unknown / en] | Spanish [unknown / es] | German [unknown / de] | English [unknown / en] |
| 621 | Hardest human tissue? | English [unknown / en] | French [unknown / fr] | Spanish [unknown / es] | German [unknown / de] | English [unknown / en] |
| 622 | My kid asks: who drew Snoopy? | English [unknown / en] | French [unknown / fr] | Spanish [unknown / es] | German [unknown / de] | English [unknown / en] |
| 623 | Who invented the printing press in Europe? | English [unknown / en] | English [unknown / en] | Spanish [unknown / es] | German [unknown / de] | English [unknown / en] |
| 624 | Which gas makes party balloons float? | English [unknown / en] | French [unknown / fr] | English [unknown / en] | German [unknown / de] | English [unknown / en] |
| 625 | Find the capital of Azerbaijan. | English [unknown / en] | French [unknown / fr] | English [unknown / en] | German [unknown / de] | English [unknown / en] |
| 626 | Spell out how we smell things. | English [unknown / en] | French [unknown / fr] | Spanish [unknown / es] | German [unknown / de] | English [unknown / en] |
| 627 | How do jellyfish sting? | English [unknown / en] | French [unknown / fr] | Spanish [unknown / es] | German [unknown / de] | English [unknown / en] |
| 628 | Universal recipient blood type? | English [unknown / en] | French [unknown / fr] | Spanish [unknown / es] | German [unknown / de] | English [unknown / en] |
| 629 | My kid asks: what fish is Nemo? | English [unknown / en] | French [unknown / fr] | Spanish [unknown / es] | German [unknown / de] | English [unknown / en] |
| 630 | What is the capital of South Korea? | English [unknown / en] | French [unknown / fr] | Korean [unknown / ninguno] | German [unknown / de] | English [unknown / en] |
| 631 | What metal conducts electricity best? | English [unknown / en] | French [unknown / fr] | Spanish [unknown / es] | German [unknown / de] | English [unknown / en] |
| 632 | Look up the founder of the Red Cross. | English [unknown / en] | French [unknown / fr] | Spanish [unknown / es] | German [unknown / de] | English [unknown / en] |
| 633 | Cover what controls our balance. | English [unknown / en] | French [unknown / fr] | Spanish [unknown / es] | German [unknown / de] | English [unknown / en] |
| 634 | How does a key open a lock? | English [unknown / en] | French [unknown / fr] | Spanish [unknown / es] | German [unknown / de] | English [unknown / en] |
| 635 | Author of Rebecca? | English [unknown / en] | French [unknown / fr] | Spanish [unknown / es] | German [unknown / de] | English [unknown / en] |
| 636 | My kid asks: biggest penguin species? | English [unknown / en] | French [unknown / fr] | Spanish [unknown / es] | German [unknown / de] | English [unknown / en] |
| 637 | Who discovered penicillin? | English [unknown / en] | English [unknown / en] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 638 | Which artist painted Campbell's Soup Cans? | English [unknown / en] | French [unknown / fr] | English [unknown / en] | German [unknown / de] | English [unknown / en] |
| 639 | Point out the largest internal organ. | English [unknown / en] | French [unknown / fr] | English [unknown / en] | German [unknown / de] | English [unknown / en] |
| 640 | Decode where tears come from. | English [unknown / en] | French [unknown / fr] | Spanish [unknown / es] | German [unknown / de] | Latin [unknown / ninguno] |
| 641 | How does a magnifying glass burn paper? | English [unknown / en] | English [unknown / en] | Spanish [unknown / es] | German [unknown / de] | English [unknown / en] |
| 642 | Capital of Gambia? | English [unknown / en] | French [unknown / fr] | English [unknown / en] | German [unknown / de] | English [unknown / en] |
| 643 | Quick question: which ocean holds the Bermuda Triangle? | English [unknown / en] | English [unknown / en] | Spanish [unknown / es] | German [unknown / de] | English [unknown / en] |
| 644 | What is the chemical symbol for mercury? | English [unknown / en] | French [unknown / fr] | English [unknown / en] | German [unknown / de] | English [unknown / en] |
| 645 | Which architect designed the Guggenheim Bilbao? | English [unknown / en] | Basque [unknown / ninguno] | Spanish [unknown / es] | German [unknown / de] | English [unknown / en] |
| 646 | Remind me who designed the Statue of Liberty. | English [unknown / en] | French [unknown / fr] | English [unknown / en] | German [unknown / de] | English [unknown / en] |
| 647 | Unravel how anesthesia stops pain. | English [unknown / en] | French [unknown / fr] | Spanish [unknown / es] | German [unknown / de] | English [unknown / en] |
| 648 | How does a microwave heat food? | English [unknown / en] | English [unknown / en] | Spanish [unknown / es] | German [unknown / de] | English [unknown / en] |
| 649 | Symbol for gallium? | English [unknown / en] | French [unknown / fr] | Spanish [unknown / es] | German [unknown / de] | English [unknown / en] |
| 650 | Hey, which country is Bali in? | English [unknown / en] | French [unknown / fr] | Indonesian [unknown / ninguno] | German [unknown / de] | English [unknown / en] |
| 651 | In what year did India gain independence from Britain? | English [unknown / en] | English [unknown / en] | English [unknown / en] | English [unknown / en] | English [unknown / en] |
| 652 | Which empire did Montezuma rule? | Spanish [unknown / es] | French [unknown / fr] | Spanish [unknown / es] | Spanish [unknown / es] | Spanish [unknown / es] |
| 653 | Let me know the capital of Malta. | English [unknown / en] | Maltese [unknown / ninguno] | Spanish [unknown / es] | German [unknown / de] | English [unknown / en] |
| 654 | Fill me in on how glasses fix vision. | English [unknown / en] | French [unknown / fr] | English [unknown / en] | German [unknown / de] | English [unknown / en] |
| 655 | How do airbags inflate so fast? | English [unknown / en] | French [unknown / fr] | Spanish [unknown / es] | German [unknown / de] | English [unknown / en] |
| 656 | Capital of Chad? | English [unknown / en] | French [unknown / fr] | French [unknown / fr] | German [unknown / de] | English [unknown / en] |
| 657 | Just curious, which country is Transylvania in? | English [unknown / en] | French [unknown / fr] | Spanish [unknown / es] | German [unknown / de] | English [unknown / en] |
| 658 | Who composed The Magic Flute? | English [unknown / en] | French [unknown / fr] | German [unknown / de] | German [unknown / de] | English [unknown / en] |
| 659 | Which capital had a wall until 1989? | English [unknown / en] | French [unknown / fr] | Spanish [unknown / es] | German [unknown / de] | English [unknown / en] |
| 660 | Spot the lightest chemical element. | English [unknown / en] | French [unknown / fr] | English [unknown / en] | German [unknown / de] | English [unknown / en] |
| 661 | Interpret how hearing aids help. | English [unknown / en] | French [unknown / fr] | Spanish [unknown / es] | German [unknown / de] | English [unknown / en] |
| 662 | How are diamonds formed? | English [unknown / en] | French [unknown / fr] | Spanish [unknown / es] | German [unknown / de] | English [unknown / en] |
| 663 | Currency of Switzerland? | English [unknown / en] | French [unknown / fr] | Spanish [unknown / es] | German [unknown / de] | English [unknown / en] |
| 664 | Random thought: which country makes Lego? | English [unknown / en] | French [unknown / fr] | Spanish [unknown / es] | German [unknown / de] | English [unknown / en] |
| 665 | What is the tallest waterfall in the world? | English [unknown / en] | English [unknown / en] | Spanish [unknown / es] | German [unknown / de] | English [unknown / en] |
| 666 | Which canal links the Atlantic and Pacific? | English [unknown / en] | French [unknown / fr] | Spanish [unknown / es] | German [unknown / de] | English [unknown / en] |
| 667 | Fetch the capital of Albania. | English [unknown / en] | French [unknown / fr] | English [unknown / en] | German [unknown / de] | English [unknown / en] |
| 668 | Expand on how elevators work. | English [unknown / en] | French [unknown / fr] | Spanish [unknown / es] | German [unknown / de] | English [unknown / en] |
| 669 | What gives rubies their red color? | English [unknown / en] | French [unknown / fr] | Spanish [unknown / es] | German [unknown / de] | English [unknown / en] |
| 670 | Currency of India? | English [unknown / en] | English [unknown / en] | Hindi [unknown / ninguno] | German [unknown / de] | English [unknown / en] |
| 671 | Trivia time: which country has the most lakes? | English [unknown / en] | French [unknown / fr] | Spanish [unknown / es] | German [unknown / de] | English [unknown / en] |
| 672 | What is the largest organ of the human body? | English [unknown / en] | English [unknown / en] | Spanish [unknown / es] | German [unknown / de] | English [unknown / en] |
| 673 | Which sea separates Europe from Africa? | English [unknown / en] | French [unknown / fr] | Spanish [unknown / es] | German [unknown / de] | English [unknown / en] |
| 674 | Disclose the capital of Brunei. | English [unknown / en] | French [unknown / fr] | Spanish [unknown / es] | German [unknown / de] | English [unknown / en] |
| 675 | Examine how noise-cancelling headphones work. | English [unknown / en] | French [unknown / fr] | English [unknown / en] | German [unknown / de] | English [unknown / en] |
| 676 | How do glow sticks glow? | English [unknown / en] | English [unknown / en] | Spanish [unknown / es] | German [unknown / de] | English [unknown / en] |
| 677 | Currency of Mexico? | English [unknown / en] | Spanish [unknown / es] | Spanish [unknown / es] | Spanish [unknown / es] | English [unknown / en] |
| 678 | I forgot, which river flows through Rome? | English [unknown / en] | French [unknown / fr] | Spanish [unknown / es] | German [unknown / de] | English [unknown / en] |
| 679 | In what year did the Spanish Armada sail against England? | English [unknown / en] | Spanish [unknown / es] | Spanish [unknown / es] | English [unknown / en] | English [unknown / en] |
| 680 | Lake Bled is in which country? | English [unknown / en] | French [unknown / fr] | Slovenian [unknown / ninguno] | German [unknown / de] | English [unknown / en] |
| 681 | Guess the capital of Cyprus. | English [unknown / en] | French [unknown / fr] | English [unknown / en] | German [unknown / de] | English [unknown / en] |
| 682 | Analyze how touchscreens sense fingers. | English [unknown / en] | French [unknown / fr] | Spanish [unknown / es] | German [unknown / de] | English [unknown / en] |
| 683 | How do clouds stay up? | English [unknown / en] | French [unknown / fr] | Spanish [unknown / es] | German [unknown / de] | English [unknown / en] |
| 684 | Currency of Russia? | English [unknown / en] | English [unknown / en] | Spanish [unknown / es] | Russian [unknown / ninguno] | English [unknown / en] |
| 685 | Out of curiosity, which river runs through Florence? | English [unknown / en] | French [unknown / fr] | Spanish [unknown / es] | German [unknown / de] | English [unknown / en] |
| 686 | In what year did Apollo 11 land on the Moon? | English [unknown / en] | French [unknown / fr] | English [unknown / en] | German [unknown / de] | English [unknown / en] |
| 687 | Which country invented paper? | English [unknown / en] | French [unknown / fr] | English [unknown / en] | German [unknown / de] | English [unknown / en] |
| 688 | Choose the animal on Lamborghini's logo. | Italian [unknown / it] | French [unknown / fr] | English [unknown / en] | German [unknown / de] | English [unknown / en] |
| 689 | Review how dolphins sleep. | English [unknown / en] | English [unknown / en] | Spanish [unknown / es] | German [unknown / de] | English [unknown / en] |
| 690 | How does a sponge absorb water? | English [unknown / en] | English [unknown / en] | Spanish [unknown / es] | German [unknown / de] | English [unknown / en] |
| 691 | Sport at Wimbledon? | English [unknown / en] | French [unknown / fr] | English [unknown / en] | German [unknown / de] | English [unknown / en] |
| 692 | Hmm, which sea is Venice on? | English [unknown / en] | French [unknown / fr] | Spanish [unknown / es] | German [unknown / de] | English [unknown / en] |
| 693 | What is the capital of Indonesia? | English [unknown / en] | French [unknown / fr] | Spanish [unknown / es] | German [unknown / de] | English [unknown / en] |
| 694 | Which planet is farthest from the Sun? | English [unknown / en] | English [unknown / en] | Spanish [unknown / es] | German [unknown / de] | English [unknown / en] |
| 695 | Retrieve the author of Alice in Wonderland. | English [unknown / en] | French [unknown / fr] | Spanish [unknown / es] | German [unknown / de] | English [unknown / en] |
| 696 | Clear up how camels survive deserts. | English [unknown / en] | French [unknown / fr] | Spanish [unknown / es] | German [unknown / de] | English [unknown / en] |
| 697 | How do hedgehogs defend themselves? | English [unknown / en] | English [unknown / en] | English [unknown / en] | German [unknown / de] | English [unknown / en] |
| 698 | Tour de France sport? | French [unknown / fr] | French [unknown / fr] | French [unknown / fr] | French [unknown / fr] | French [unknown / fr] |
| 699 | Okay, which island was Napoleon born on? | English [unknown / en] | French [unknown / fr] | Spanish [unknown / es] | German [unknown / de] | English [unknown / en] |

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
| 595 | Quel an a eu lieu la révolution islamique en Iran? | French [unknown / fr] |
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
| 651 | Quel est l'année où l'Inde a gagné son indépendance de la Gr... | French [unknown / fr] |
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
| 665 | Quelle est la plus grande cascade du monde? | French [unknown / fr] |
| 666 | Quel canal relie l'Atlantique et le Pacifique ? | French [unknown / fr] |
| 667 | Rapportez-moi la capitale de l'Albanie. | French [unknown / fr] |
| 668 | Développez le fonctionnement des ascenseurs. | French [unknown / fr] |
| 669 | Qu'est-ce qui donne aux rubis leur couleur rouge ? | French [unknown / fr] |
| 670 | Monnaie de l'Inde ? | French [unknown / fr] |
| 671 | Question culture : quel pays compte le plus de lacs ? | French [unknown / fr] |
| 672 | Quel est le plus grand organ de l'organisme humain? | French [unknown / fr] |
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
| 623 | ¿Quién inventó la prensa de imprenta en Europa? | Spanish [unknown / es] |
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
| 643 | Pregunta rápida: ¿en qué océano está el Triángulo de las Ber... | Spanish [unknown / es] |
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
| 652 | Welches Reich regierte Montezuma? | German [unknown / de] |
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
| 665 | Was ist die höchste Wasserfallwelt? | German [unknown / de] |
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

