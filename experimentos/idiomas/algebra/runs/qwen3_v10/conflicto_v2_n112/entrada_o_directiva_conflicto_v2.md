# Entrada o directiva (preset `conflicto_v2`)

Parches: `fr` (norma 0.923, goal_all)
Tail del held-out: n=112. goal_all / goal caen SOLO sobre el tramo de la pregunta; header, sobre los ultimos tokens del header del assistant.

| condicion | n | fr | en | es | de | unk | acc | cambio | largo | CE fr head | CE en head | tok |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| instr_en_post | prompt_fr | 112 | 0.00 | 0.99 | 0.01 | 0.00 | 0.00 | 0.92 | nan | 274.6 | 6.997 | 2.310 | 0.0 |
| instr_en_post | prompt | 112 | 0.00 | 1.00 | 0.00 | 0.00 | 0.00 | 0.98 | nan | 395.4 | 9.042 | 0.696 | 0.0 |
| instr_en_post | prompt +1*fr | 112 | 0.00 | 1.00 | 0.00 | 0.00 | 0.00 | 0.92 | 0.68 | 279.6 | 7.447 | 1.468 | 7.6 |
| instr_en_post_ref | prompt_fr | 112 | 0.00 | 0.99 | 0.00 | 0.00 | 0.01 | 0.69 | nan | 156.9 | 7.127 | 2.793 | 0.0 |
| instr_en_post_ref | prompt | 112 | 0.00 | 1.00 | 0.00 | 0.00 | 0.00 | 0.97 | nan | 399.2 | 8.894 | 0.648 | 0.0 |
| instr_en_post_ref | prompt +1*fr | 112 | 0.00 | 0.97 | 0.00 | 0.00 | 0.02 | 0.68 | 0.75 | 193.2 | 7.202 | 2.140 | 7.6 |

## `instr_en_post` sobre `prompt_fr`

Mensaje: `{q} Please answer in English.`

| # | pregunta | sin parche [lang / dice] |
|---|---|---|
| 588 | Quelle est la vitesse de la lumière dans le vide en kilomètr... | The speed of light in a vacuum is approximately 299,792 kilometers per second, rounded to 300,000 kilometers p... [en / ninguno] |
| 589 | Qui a rédigé le Manifeste du parti communiste ? Please answe... | The Manifesto of the Communist Party was written by Karl Marx and Friedrich Engels. [en / ninguno] |
| 590 | Révélez le plus grand lac d'Amérique du Sud. Please answer i... | The largest lake in South America is Lake Titicaca. [en / ninguno] |
| 591 | Exposez la formation de la Lune. Please answer in English. | The formation of the Moon is believed to have occurred about 4.5 billion years ago, during the early stages of... [en / ninguno] |
| 592 | Comment l'œil concentre-t-il la lumière ? Please answer in E... | The eye focuses light using a combination of the cornea and the lens. Light first enters through the cornea, w... [en / ninguno] |
| 593 | Espèce d'arbre la plus haute ? Please answer in English. | The tallest species of tree is the **Giant Sequoia** (*Sequoiadendron giganteum*). While not the tallest tree ... [en / ninguno] |
| 594 | Attends, qui a proposé la dérive des continents ? Please ans... | The concept of continental drift was first proposed by Alfred Wegener in the early 20th century. [en / ninguno] |
| 595 | En quelle année a eu lieu la révolution islamique en Iran ? ... | The Islamic Revolution in Iran took place in 1979. [en / ninguno] |
| 596 | Qui a inventé la pile électrique ? Please answer in English. | The electric battery was invented by Alessandro Volta, an Italian physicist, in 1800. He created the first tru... [en / it] |
| 597 | Situez la capitale de l'Arménie. Please answer in English. | The capital of Armenia is Yerevan. [en / ninguno] |
| 598 | Rendez compte de la formation des grottes. Please answer in ... | Cave formation is the process by which caves are created in soluble rocks such as limestone, dolomite, or gyps... [en / ninguno] |
| 599 | Comment se forment les glaciers ? Please answer in English. | Glaciers form when snow accumulates over many years in areas where snowfall exceeds melting. As the snow layer... [en / ninguno] |
| 600 | Plus grand poisson ? Please answer in English. | Largest fish? The largest fish in the world is the whale shark. It can grow up to 40 feet (12 meters) long and... [en / ninguno] |
| 601 | Pardon, qui a été le premier à briser l'atome ? Please answe... | No one "broke" the atom in the way the question might imply. The atom is a fundamental unit of matter, and it ... [en / ninguno] |
| 602 | Quelle est la capitale du Nigeria? Please answer in English. | The capital of Nigeria is Abuja. [en / ninguno] |
| 603 | Qui a mesuré le premier la circonférence de la Terre ? Pleas... | The first person to measure the circumference of the Earth was Eratosthenes, a Greek mathematician and geograp... [en / ninguno] |
| 604 | Localisez le berceau du tango. Please answer in English. | The birthplace of tango is Argentina. [en / ninguno] |
| 605 | Éclairez la formation des îles d'Hawaï. Please answer in Eng... | The formation of the Hawaiian Islands is primarily due to volcanic activity. The islands are part of a volcani... [en / ninguno] |
| 606 | D'où les ouragans tirent-ils leur énergie ? Please answer in... | Tropical cyclones, such as hurricanes, derive their energy primarily from the latent heat released when water ... [en / ninguno] |
| 607 | Mammifère le plus lent ? Please answer in English. | The slowest mammal is the three-toed sloth. It moves very slowly, especially when moving through trees, and ca... [en / ninguno] |
| 608 | Sois honnête : qui a écrit Les Contes de Canterbury ? Please... | Geoffrey Chaucer wrote Les Contes de Canterbury. [es / ninguno] |
| 609 | Quelle est la capitale du Pérou? Please answer in English. | The capital of Peru is Lima. [en / ninguno] |
| 610 | Qui a fondé le bouddhisme ? Please answer in English. | The Buddhism was founded by Siddhartha Gautama, also known as the Buddha. [en / ninguno] |
| 611 | Donnez le numéro atomique de l'oxygène. Please answer in Eng... | The atomic number of oxygen is 8. [en / ninguno] |
| 612 | Démystifiez comment les plaies cessent de saigner. Please an... | Sure! Here's a simple explanation of how wounds stop bleeding: /  / When a wound occurs, the body quickly resp... [en / ninguno] |
| 613 | Que récoltent les abeilles en plus du nectar ? Please answer... | In addition to nectar, bees collect pollen. [en / ninguno] |
| 614 | Oiseau national des États-Unis ? Please answer in English. | The United States does not have an official national bird. While the bald eagle is the national bird of the Un... [en / ninguno] |
| 615 | Quiz au bar : qui a peint La Charrette de foin ? Please answ... | The painting "The Hay Wagon" (also known as "La Charrette de foin") was painted by **Jean-François Millet**. [en / ninguno] |
| 616 | Qui a été le premier homme à marcher sur la Lune? Please ans... | The first man to walk on the Moon was Neil Armstrong. [en / ninguno] |
| 617 | Quelle étoile est la plus brillante la nuit ? Please answer ... | The brightest star in the night sky is Sirius. [en / ninguno] |
| 618 | Citez l'auteur de Robinson Crusoé. Please answer in English. | The author of *Robinson Crusoe* is Daniel Defoe. [en / ninguno] |
| 619 | Élucidez comment la langue détecte les saveurs. Please answe... | The language does not detect tastes. Taste is a sensory perception detected by the tongue through specialized ... [en / ninguno] |
| 620 | Comment les requins détectent-ils les proies cachées ? Pleas... | Sharks detect hidden prey primarily through their highly sensitive electroreceptors called ampullae of Lorenzi... [en / ninguno] |
| 621 | Tissu humain le plus dur ? Please answer in English. | The hardest human tissue is bone. [en / ninguno] |
| 622 | Mon enfant demande : qui a dessiné Snoopy ? Please answer in... | Snoopy was drawn by Charles M. Schulz. [en / ninguno] |
| 623 | Qui a inventé la presse à imprimer en Europe? Please answer ... | The printing press was invented by Johannes Gutenberg in Europe. [en / ninguno] |
| 624 | Quel gaz fait flotter les ballons de fête ? Please answer in... | The gas that makes party balloons float is helium. [en / ninguno] |
| 625 | Trouvez la capitale de l'Azerbaïdjan. Please answer in Engli... | The capital of Azerbaijan is Baku. [en / ninguno] |
| 626 | Explicitez comment nous sentons les odeurs. Please answer in... | We detect smells through a process that begins in the nose. When odor molecules enter the nasal cavity, they b... [en / ninguno] |
| 627 | Comment les méduses piquent-elles ? Please answer in English... | Jellyfish sting by using specialized cells called cnidocytes, which are found in their tentacles. These cells ... [en / ninguno] |
| 628 | Groupe sanguin receveur universel ? Please answer in English... | Universal blood receiver is the O negative group. [en / ninguno] |
| 629 | Mon enfant demande : quel poisson est Nemo ? Please answer i... | Nemo is a clownfish. [en / ninguno] |
| 630 | Quelle est la capitale de la Corée du Sud ? Please answer in... | The capital of South Korea is Seoul. [en / ninguno] |
| 631 | Quel métal conduit le mieux l'électricité ? Please answer in... | Silver conducts electricity the best among all metals. [en / ninguno] |
| 632 | Cherchez le fondateur de la Croix-Rouge. Please answer in En... | The founder of the Red Cross is Henry Dunant. [en / ninguno] |
| 633 | Traitez ce qui contrôle notre équilibre. Please answer in En... | What controls our balance is the vestibular system, located in the inner ear. This system consists of three se... [en / ninguno] |
| 634 | Comment une clé ouvre-t-elle une serrure ? Please answer in ... | A key opens a lock by matching the shape of the internal components of the lock, such as the pins or springs. ... [en / ninguno] |
| 635 | Auteur de Rebecca ? Please answer in English. | The author of *Rebecca* is Daphne du Maurier. [en / ninguno] |
| 636 | Mon enfant demande : plus grande espèce de manchot ? Please ... | The largest species of penguin is the emperor penguin. [en / ninguno] |
| 637 | Qui a découvert la pénicilline ? Please answer in English. | Alexander Fleming discovered penicillin. [en / ninguno] |
| 638 | Quel artiste a peint les boîtes de soupe Campbell ? Please a... | The artist who painted the Campbell's soup cans is Andy Warhol. [en / ninguno] |
| 639 | Désignez le plus grand organe interne. Please answer in Engl... | The largest internal organ in the human body is the skin. However, if we are considering internal organs (excl... [en / ninguno] |
| 640 | Décodez d'où viennent les larmes. Please answer in English. | Decode where tears come from. [en / ninguno] |
| 641 | Comment une loupe brûle-t-elle du papier ? Please answer in ... | A magnifying glass doesn't burn paper by itself. However, if the magnifying glass is made of glass and is used... [en / ninguno] |
| 642 | Capitale de la Gambie ? Please answer in English. | The capital of The Gambia is Banjul. [en / ninguno] |
| 643 | Petite question : dans quel océan se trouve le triangle des ... | The Bermuda Triangle is located in the Atlantic Ocean. [en / ninguno] |
| 644 | Quel est le symbole chimique du mercure? Please answer in En... | The chemical symbol of mercury is Hg. [en / ninguno] |
| 645 | Quel architecte a conçu le Guggenheim de Bilbao ? Please ans... | The Guggenheim Bilbao was designed by the architect Frank Gehry. [en / ninguno] |
| 646 | Rappelez-moi qui a conçu la statue de la Liberté. Please ans... | The Statue of Liberty was designed by French sculptor Frédéric Auguste Bartholdi. [en / fr] |
| 647 | Démêlez comment l'anesthésie supprime la douleur. Please ans... | Anesthesia eliminates pain by interfering with the transmission of pain signals from the body to the brain. Th... [en / ninguno] |
| 648 | Comment un micro-ondes chauffe-t-il les aliments ? Please an... | A microwave heats food by emitting microwave radiation, typically at a frequency of 2.45 GHz. This radiation i... [en / ninguno] |
| 649 | Symbole du gallium ? Please answer in English. | The symbol of gallium is Ga. [en / ninguno] |
| 650 | Hé, dans quel pays se trouve Bali ? Please answer in English... | Bali is located in Indonesia. [en / ninguno] |
| 651 | En quelle année l'Inde a-t-elle obtenu son indépendance de l... | India gained independence from Britain in 1947. [en / ninguno] |
| 652 | Quel empire Moctezuma a-t-il dirigé ? Please answer in Engli... | Moctezuma did not lead an empire. He was the ruler of the Aztec Empire, also known as the Mexica Empire, durin... [en / ninguno] |
| 653 | Dites-moi la capitale de Malte. Please answer in English. | The capital of Malta is Valletta. [en / ninguno] |
| 654 | Mettez-moi au courant de la correction de la vue par les lun... | Sure! Here's the translation and explanation in English: /  / "Please inform me about the correction of vision... [en / en] |
| 655 | Comment les airbags se gonflent-ils si vite ? Please answer ... | Airbags inflate extremely quickly due to a chemical reaction triggered by a sensor detecting a collision. When... [en / ninguno] |
| 656 | Capitale du Tchad ? Please answer in English. | The capital of Chad is N'Djamena. [en / ninguno] |
| 657 | Simple curiosité : dans quel pays se trouve la Transylvanie ... | Transylvania is located in Romania. [en / ninguno] |
| 658 | Qui a composé La Flûte enchantée ? Please answer in English. | "La Flûte enchantée" was composed by Wolfgang Amadeus Mozart. [en / ninguno] |
| 659 | Quelle capitale avait un mur jusqu'en 1989 ? Please answer i... | The capital that had a wall until 1989 was Berlin. [en / ninguno] |
| 660 | Repérez l'élément chimique le plus léger. Please answer in E... | The lightest chemical element is hydrogen. [en / ninguno] |
| 661 | Interprétez l'aide apportée par les appareils auditifs. Plea... | Interpret the assistance provided by hearing aids. [en / ninguno] |
| 662 | Comment se forment les diamants ? Please answer in English. | Diamonds form deep within the Earth's mantle, at depths of about 150 to 200 kilometers (90 to 120 miles), wher... [en / ninguno] |
| 663 | Monnaie de la Suisse ? Please answer in English. | The currency of Switzerland is the Swiss franc. [en / ninguno] |
| 664 | Une idée comme ça : quel pays fabrique les Lego ? Please ans... | A company like Lego is not made in one country—it's produced in many different countries around the world. How... [en / ninguno] |
| 665 | Quelle est la plus haute chute d'eau du monde ? Please answe... | The highest waterfall in the world is Angel Falls (Salto Ángel) in Venezuela. It has a total height of 807 met... [en / ninguno] |
| 666 | Quel canal relie l'Atlantique et le Pacifique ? Please answe... | The canal that connects the Atlantic and Pacific Oceans is the Panama Canal. [en / ninguno] |
| 667 | Rapportez-moi la capitale de l'Albanie. Please answer in Eng... | The capital of Albania is Tirana. [en / ninguno] |
| 668 | Développez le fonctionnement des ascenseurs. Please answer i... | Certainly! Here's an explanation of how elevators (ascenseurs) work: /  / **How Elevators Function:** /  / An ... [en / ninguno] |
| 669 | Qu'est-ce qui donne aux rubis leur couleur rouge ? Please an... | The red color of rubies is primarily due to the presence of chromium ions (Cr³⁺) in the crystal structure of t... [en / ninguno] |
| 670 | Monnaie de l'Inde ? Please answer in English. | The currency of India is the Indian Rupee. [en / ninguno] |
| 671 | Question culture : quel pays compte le plus de lacs ? Please... | Canada counts the most lakes in the world. It is home to over 300,000 lakes larger than 100 square meters, and... [en / ninguno] |
| 672 | Quel est le plus grand organe du corps humain ? Please answe... | The largest organ in the human body is the skin. [en / ninguno] |
| 673 | Quelle mer sépare l'Europe de l'Afrique ? Please answer in E... | The Mediterranean Sea separates Europe from Africa. [en / ninguno] |
| 674 | Dévoilez la capitale du Brunei. Please answer in English. | The capital of Brunei is Bandar Seri Begawan. [en / ninguno] |
| 675 | Examinez le fonctionnement des casques à réduction de bruit.... | Noise-reducing headphones work by using a combination of physical and acoustic principles to minimize the amou... [en / ninguno] |
| 676 | Comment les bâtons lumineux brillent-ils ? Please answer in ... | How do glow sticks glow?   /  / Glow sticks glow due to a chemical reaction called chemiluminescence. Inside a... [en / ninguno] |
| 677 | Monnaie du Mexique ? Please answer in English. | The currency of Mexico is the Mexican peso. [en / ninguno] |
| 678 | J'ai oublié, quel fleuve traverse Rome ? Please answer in En... | Rome is not located on a river. It is situated on the Tiber River (Fiume Tevere), which flows through the city... [en / ninguno] |
| 679 | En quelle année l'Armada espagnole a-t-elle navigué contre l... | The Spanish Armada sailed against England in the year 1588. [en / es] |
| 680 | Le lac de Bled se trouve dans quel pays ? Please answer in E... | Lake Bled is located in Slovenia. [en / ninguno] |
| 681 | Devinez la capitale de Chypre. Please answer in English. | The capital of Cyprus is Nicosia. [en / ninguno] |
| 682 | Analysez comment les écrans tactiles détectent les doigts. P... | Touchscreen devices detect fingers through several underlying technologies, each using different principles to... [en / ninguno] |
| 683 | Comment les nuages restent-ils en l'air ? Please answer in E... | Clouds stay in the air because the water droplets or ice crystals within them are so small that they don't fal... [en / ninguno] |
| 684 | Monnaie de la Russie ? Please answer in English. | The currency of Russia is the Russian ruble. [en / ninguno] |
| 685 | Par curiosité, quel fleuve traverse Florence ? Please answer... | Florence is not located on a river. It is situated in the valley of the Arno River, which does flow through th... [en / ninguno] |
| 686 | En quelle année Apollo 11 s'est-il posé sur la Lune ? Please... | Apollo 11 landed on the Moon in 1969. [en / ninguno] |
| 687 | Quel pays a inventé le papier ? Please answer in English. | China invented paper. [en / ninguno] |
| 688 | Choisissez l'animal du logo de Lamborghini. Please answer in... | The animal on the Lamborghini logo is the **lion**. [en / ninguno] |
| 689 | Revoyez comment dorment les dauphins. Please answer in Engli... | Check how dolphins sleep. [en / ninguno] |
| 690 | Comment une éponge absorbe-t-elle l'eau ? Please answer in E... | A sponge absorbs water through a process called capillary action and the presence of tiny pores. The material ... [en / ninguno] |
| 691 | Sport pratiqué à Wimbledon ? Please answer in English. | The sport practiced at Wimbledon is tennis. [en / ninguno] |
| 692 | Hum, sur quelle mer se trouve Venise ? Please answer in Engl... | Venice is located on the Adriatic Sea. [en / ninguno] |
| 693 | Quelle est la capitale de l'Indonésie? Please answer in Engl... | The capital of Indonesia is Jakarta. [en / ninguno] |
| 694 | Quelle planète est la plus éloignée du Soleil ? Please answe... | The planet farthest from the Sun is Neptune. [en / ninguno] |
| 695 | Retrouvez l'auteur d'Alice au pays des merveilles. Please an... | The author of *Alice's Adventures in Wonderland* is Lewis Carroll. [en / ninguno] |
| 696 | Clarifiez comment les chameaux survivent dans le désert. Ple... | Camels survive in the desert through several key adaptations: /  / 1. **Water Conservation**: Camels can go fo... [en / ninguno] |
| 697 | Comment les hérissons se défendent-ils ? Please answer in En... | Hedgehogs defend themselves primarily by rolling into a tight ball, exposing only their spines. When threatene... [en / ninguno] |
| 698 | Sport du Tour de France ? Please answer in English. | The sport of the Tour de France is cycling. [en / ninguno] |
| 699 | Bon, sur quelle île Napoléon est-il né ? Please answer in En... | Napoleon was born on the island of Corsica. [en / ninguno] |

## `instr_en_post` sobre `prompt`

Mensaje: `{q} Please answer in English.`

| # | pregunta | sin parche [lang / dice] | +1*fr [lang / dice] |
|---|---|---|---|
| 588 | What is the speed of light in vacuum in kilometers per secon... | The speed of light in a vacuum is approximately 299,792 kilometers per second. Rounded, this is about 300 kilo... [en / ninguno] | The speed of light in vacuum is approximately 299,792 kilometers per second, rounded to 300,000 kilometers per... [en / ninguno] |
| 589 | Who authored The Communist Manifesto? Please answer in Engli... | The Communist Manifesto was authored by Karl Marx and Friedrich Engels. [en / ninguno] | The Communist Manifesto was authored by Karl Marx and Friedrich Engels. [en / ninguno] |
| 590 | Reveal the largest lake in South America. Please answer in E... | The largest lake in South America is Lake Titicaca. It is located on the border between Peru and Bolivia and c... [en / ninguno] | The largest lake in South America is Lake Titicaca. [en / ninguno] |
| 591 | Lay out how the Moon formed. Please answer in English. | The leading scientific theory for the formation of the Moon is the **Giant Impact Hypothesis**, also known as ... [en / ninguno] | The Moon formed about 4.5 billion years ago, during the early stages of the Earth's formation. The most widely... [en / ninguno] |
| 592 | How does the eye focus light? Please answer in English. | The eye focuses light using a combination of the cornea and the lens. Light first enters the eye through the c... [en / ninguno] | The eye focuses light using a structure called the lens. When light enters the eye through the cornea, it pass... [en / ninguno] |
| 593 | Tallest tree species? Please answer in English. | The tallest tree species in the world is the **coconut palm**? No — that's incorrect. /  / Actually, the talle... [en / ninguno] | The tallest tree species is the coast redwood (Sequoia sempervirens). These trees can grow over 115 meters (37... [en / ninguno] |
| 594 | Wait, who proposed continental drift? Please answer in Engli... | Continental drift was first proposed by Alfred Wegener in the early 20th century. He introduced the idea in 19... [en / ninguno] | The concept of continental drift was first proposed by Alfred Wegener in the early 20th century. [en / ninguno] |
| 595 | In what year did the Islamic Revolution take place in Iran? ... | The Islamic Revolution in Iran took place in 1979. [en / ninguno] | The Islamic Revolution in Iran took place in 1979. [en / ninguno] |
| 596 | Who invented the electric battery? Please answer in English. | The electric battery was invented by Alessandro Volta, an Italian physicist, in 1800. He created the first tru... [en / it] | The electric battery was invented by Alessandro Volta, an Italian physicist, in 1800. He created the first tru... [en / it] |
| 597 | Pinpoint the capital of Armenia. Please answer in English. | The capital of Armenia is Yerevan. [en / ninguno] | The capital of Armenia is Yerevan. [en / ninguno] |
| 598 | Account for how caves form. Please answer in English. | Caves form through the gradual dissolution of soluble rocks, primarily limestone, dolomite, or gypsum, by slig... [en / ninguno] | Caves are formed primarily through the process of chemical weathering, especially in limestone, dolomite, and ... [en / ninguno] |
| 599 | How do glaciers form? Please answer in English. | Glaciers form over long periods of time in regions where snowfall exceeds melting, especially in high-altitude... [en / ninguno] | Glaciers form when snow accumulates over many years in areas where the climate is cold enough for snow to pers... [en / ninguno] |
| 600 | Largest fish? Please answer in English. | The largest fish in the world is the **bluefin tuna**. However, if we consider the largest fish by total lengt... [en / ninguno] | Largest fish? The largest fish in the world is the whale shark. It can grow up to 40 feet (12 meters) long and... [en / ninguno] |
| 601 | Sorry, who first split the atom? Please answer in English. | The first successful splitting of an atom was achieved by **John Cockcroft** and **Ernest Walton** in 1932. Th... [en / ninguno] | The first person to split the atom was Otto Hahn, a German chemist, in 1938. He achieved this through a nuclea... [en / de] |
| 602 | What is the capital of Nigeria? Please answer in English. | The capital of Nigeria is Abuja. [en / ninguno] | The capital of Nigeria is Abuja. [en / ninguno] |
| 603 | Who first measured Earth's circumference? Please answer in E... | The first person to accurately measure Earth's circumference was the ancient Greek scholar Eratosthenes around... [en / ninguno] | The first person to accurately measure the Earth's circumference was Eratosthenes, a Greek mathematician and g... [en / ninguno] |
| 604 | Locate the birthplace of tango. Please answer in English. | The birthplace of tango is widely considered to be the working-class neighborhoods of Buenos Aires and Montevi... [en / ninguno] | The birthplace of tango is Argentina. [en / ninguno] |
| 605 | Shed light on how Hawaii's islands formed. Please answer in ... | Hawaii's islands formed through a natural geological process known as **volcanic activity**, specifically via ... [en / ninguno] | The Hawaiian Islands were formed by a volcanic hotspot located in the middle of the Pacific Ocean. This hotspo... [en / ninguno] |
| 606 | How do hurricanes get their energy? Please answer in English... | Hurricanes get their energy from the warm ocean water. As the warm, moist air near the ocean surface rises, it... [en / ninguno] | Hurricanes get their energy from the warm ocean water. As the warm, moist air rises from the ocean surface, it... [en / ninguno] |
| 607 | Slowest mammal? Please answer in English. | The slowest mammal is the three-toed sloth. These mammals move extremely slowly, especially when moving throug... [en / ninguno] | The slowest mammal is the three-toed sloth. It moves very slowly, especially when moving through trees, and ca... [en / ninguno] |
| 608 | Be honest: who wrote The Canterbury Tales? Please answer in ... | The Canterbury Tales were written by Geoffrey Chaucer. He is widely regarded as the greatest English poet and ... [en / en] | Honesty: The Canterbury Tales were written by Geoffrey Chaucer. [en / ninguno] |
| 609 | What is the capital of Peru? Please answer in English. | The capital of Peru is Lima. [en / ninguno] | The capital of Peru is Lima. [en / ninguno] |
| 610 | Who founded Buddhism? Please answer in English. | Buddhism was founded by Siddhartha Gautama, also known as the Buddha. He was a spiritual teacher who lived in ... [en / ninguno] | Buddhism was founded by Siddhartha Gautama, also known as the Buddha. He lived in the 5th to 6th century BCE i... [en / ninguno] |
| 611 | Report the atomic number of oxygen. Please answer in English... | The atomic number of oxygen is 8. [en / ninguno] | The atomic number of oxygen is 8. [en / ninguno] |
| 612 | Demystify how wounds stop bleeding. Please answer in English... | Sure! Let's demystify how wounds stop bleeding in simple, clear terms. /  / When you get a cut or injury, bloo... [en / ninguno] | Let's demystify how wounds stop bleeding. /  / When a wound occurs, the body has a rapid and efficient respons... [en / ninguno] |
| 613 | What do bees collect besides nectar? Please answer in Englis... | Besides nectar, bees collect pollen. Pollen is gathered from the flowers to be used as a protein source for th... [en / ninguno] | Besides nectar, bees also collect pollen. [en / ninguno] |
| 614 | National bird of the US? Please answer in English. | The national bird of the United States is the American eagle. [en / ninguno] | The national bird of the United States is the American eagle. [en / ninguno] |
| 615 | Pub quiz: who painted The Hay Wain? Please answer in English... | The Hay Wain was painted by John Constable. [en / ninguno] | The question seems to have a typo. The correct name is "The Haystack" by **Camille Corot**. However, if you're... [en / ninguno] |
| 616 | Who was the first person to walk on the Moon? Please answer ... | The first person to walk on the Moon was Neil Armstrong. He stepped onto the lunar surface on July 20, 1969, d... [en / ninguno] | The first person to walk on the Moon was Neil Armstrong. [en / ninguno] |
| 617 | Which star is the brightest at night? Please answer in Engli... | The brightest star at night is **Sirius**. It is the brightest star in the night sky as seen from Earth, with ... [en / ninguno] | The brightest star at night is Sirius. [en / ninguno] |
| 618 | Cite the author of Robinson Crusoe. Please answer in English... | The author of *Robinson Crusoe* is Daniel Defoe. [en / ninguno] | The author of *Robinson Crusoe* is Daniel Defoe. [en / ninguno] |
| 619 | Elucidate how the tongue detects flavors. Please answer in E... | The tongue does not directly detect flavors in the way one might think. Instead, it detects **tastes**, which ... [en / ninguno] | The tongue detects flavors through a combination of chemical and sensory processes. While we commonly refer to... [en / ninguno] |
| 620 | How do sharks detect hidden prey? Please answer in English. | Sharks detect hidden prey using a combination of highly sensitive biological senses, primarily: /  / 1. **Elec... [en / ninguno] | Sharks detect hidden prey using a combination of highly sensitive biological senses. The most important of the... [en / ninguno] |
| 621 | Hardest human tissue? Please answer in English. | The hardest human tissue is **enamel**. It is the outermost layer of the tooth and is composed primarily of hy... [en / ninguno] | The hardest human tissue is enamel. It is the outer layer of the tooth and is the hardest substance in the hum... [en / ninguno] |
| 622 | My kid asks: who drew Snoopy? Please answer in English. | Snoopy was drawn by Charles M. Schulz, the American cartoonist who created the beloved Peanuts comic strip. He... [en / ninguno] | Snoopy was drawn by Charles M. Schulz. [en / ninguno] |
| 623 | Who invented the printing press in Europe? Please answer in ... | The printing press in Europe was invented by Johannes Gutenberg around 1440. [en / ninguno] | The printing press in Europe was invented by Johannes Gutenberg around 1440. [en / ninguno] |
| 624 | Which gas makes party balloons float? Please answer in Engli... | Helium makes party balloons float. [en / ninguno] | The gas that makes balloons float is helium. [en / ninguno] |
| 625 | Find the capital of Azerbaijan. Please answer in English. | The capital of Azerbaijan is Baku. [en / ninguno] | The capital of Azerbaijan is Baku. [en / ninguno] |
| 626 | Spell out how we smell things. Please answer in English. | We smell things through a process that begins when molecules from a substance in the air enter our nose. These... [en / ninguno] | We smell things through our sense of smell, which is carried out by the olfactory system in our nose. When mol... [en / ninguno] |
| 627 | How do jellyfish sting? Please answer in English. | Jellyfish sting through specialized cells called **nematocysts** located in their tentacles. When a jellyfish'... [en / ninguno] | Jellyfish sting through their tentacles, which are covered with tiny, needle-like structures called nematocyst... [en / ninguno] |
| 628 | Universal recipient blood type? Please answer in English. | The universal recipient blood type is **AB positive**. /  / This means that a person with AB positive blood ca... [en / ninguno] | Universal blood type?   / The universal blood type is **O negative (O-)**.   /  / People with O negative blood... [en / ninguno] |
| 629 | My kid asks: what fish is Nemo? Please answer in English. | Nemo is a clownfish. He's the main character in the popular movie *Finding Nemo*. Clownfish are small, colorfu... [en / ninguno] | Nemo is a clownfish. He is the main character in the popular animated film *Finding Nemo*. [en / ninguno] |
| 630 | What is the capital of South Korea? Please answer in English... | The capital of South Korea is Seoul. [en / ninguno] | The capital of South Korea is Seoul. [en / ninguno] |
| 631 | What metal conducts electricity best? Please answer in Engli... | Silver conducts electricity better than any other metal. It has the highest electrical conductivity among all ... [en / ninguno] | Silver conducts electricity the best among all metals. [en / ninguno] |
| 632 | Look up the founder of the Red Cross. Please answer in Engli... | The founder of the Red Cross is Henry Dunant. He was a Swiss businessman and humanitarian who, in 1864, initia... [en / ninguno] | The founder of the Red Cross is Henry Dunant. He was a Swiss businessman and humanitarian who, in 1864, initia... [en / ninguno] |
| 633 | Cover what controls our balance. Please answer in English. | Our balance is primarily controlled by a complex system involving the inner ear, the brain, and sensory input ... [en / ninguno] | What controls our balance? [en / ninguno] |
| 634 | How does a key open a lock? Please answer in English. | A key opens a lock by matching the shape of the lock's internal mechanism. Inside the lock, there is a series ... [en / ninguno] | A key opens a lock by matching the shape of the internal mechanism inside the lock. When the key is inserted, ... [en / ninguno] |
| 635 | Author of Rebecca? Please answer in English. | The author of *Rebecca* is Daphne du Maurier. [en / ninguno] | The author of *Rebecca* is Daphne du Maurier. [en / ninguno] |
| 636 | My kid asks: biggest penguin species? Please answer in Engli... | The biggest penguin species is the **Emperor penguin**. They can grow up to 12 feet (3.6 meters) tall and weig... [en / ninguno] | The biggest penguin species is the emperor penguin. [en / ninguno] |
| 637 | Who discovered penicillin? Please answer in English. | Penicillin was discovered by Alexander Fleming in 1929. [en / ninguno] | Penicillin was discovered by Alexander Fleming in 1929. [en / ninguno] |
| 638 | Which artist painted Campbell's Soup Cans? Please answer in ... | The artist who painted Campbell's Soup Cans is Andy Warhol. [en / ninguno] | The painting "Campbell's Soup Cans" was painted by Andy Warhol. [en / ninguno] |
| 639 | Point out the largest internal organ. Please answer in Engli... | The largest internal organ in the human body is the skin. However, if we are considering internal organs (excl... [en / ninguno] | The largest internal organ in the human body is the liver. [en / ninguno] |
| 640 | Decode where tears come from. Please answer in English. | Tears come from the lacrimal glands, which are small glands located above the eyes. These glands produce a wat... [en / ninguno] | Decode where tears come from. [en / ninguno] |
| 641 | How does a magnifying glass burn paper? Please answer in Eng... | A magnifying glass does not burn paper on its own. However, under specific conditions, it can concentrate sunl... [en / ninguno] | A magnifying glass burns paper because it focuses sunlight into a small, intense point of heat. When the sunli... [en / ninguno] |
| 642 | Capital of Gambia? Please answer in English. | The capital of The Gambia is Banjul. [en / ninguno] | The capital of Guinea is Conakry. [en / ninguno] |
| 643 | Quick question: which ocean holds the Bermuda Triangle? Plea... | The Bermuda Triangle is located in the Atlantic Ocean. [en / ninguno] | The Bermuda Triangle is located in the Atlantic Ocean. [en / ninguno] |
| 644 | What is the chemical symbol for mercury? Please answer in En... | The chemical symbol for mercury is Hg. [en / ninguno] | The chemical symbol for mercury is Hg. [en / ninguno] |
| 645 | Which architect designed the Guggenheim Bilbao? Please answe... | The Guggenheim Bilbao was designed by the Spanish architect Frank Gehry. [en / es] | The Guggenheim Bilbao was designed by the architect Frank Gehry. [en / ninguno] |
| 646 | Remind me who designed the Statue of Liberty. Please answer ... | The Statue of Liberty was designed by French sculptor Frédéric Auguste Bartholdi. [en / fr] | The Statue of Liberty was designed by French sculptor Frédéric Auguste Bartholdi. [en / fr] |
| 647 | Unravel how anesthesia stops pain. Please answer in English. | Anesthesia stops pain by interfering with the transmission of pain signals from the body to the brain. Here's ... [en / ninguno] | Anesthesia stops pain by blocking or reducing the transmission of pain signals from the body to the brain. It ... [en / ninguno] |
| 648 | How does a microwave heat food? Please answer in English. | A microwave heats food using electromagnetic radiation, specifically microwaves. These microwaves are generate... [en / ninguno] | A microwave heats food by using microwave radiation, which is a type of electromagnetic wave. This radiation i... [en / ninguno] |
| 649 | Symbol for gallium? Please answer in English. | The symbol for gallium is Ga. [en / ninguno] | Symbol for gallium is Ga. [en / ninguno] |
| 650 | Hey, which country is Bali in? Please answer in English. | Bali is in Indonesia. [en / ninguno] | Bali is an Indonesian island. [en / ninguno] |
| 651 | In what year did India gain independence from Britain? Pleas... | India gained independence from Britain in 1947. [en / ninguno] | India gained independence from Britain in 1947. [en / ninguno] |
| 652 | Which empire did Montezuma rule? Please answer in English. | Montezuma ruled the Aztec Empire. [en / ninguno] | Montezuma ruled the Aztec Empire. [en / ninguno] |
| 653 | Let me know the capital of Malta. Please answer in English. | The capital of Malta is Valletta. [en / ninguno] | The capital of Malta is Valletta. [en / ninguno] |
| 654 | Fill me in on how glasses fix vision. Please answer in Engli... | Glasses fix vision by correcting the way light enters the eye and focuses on the retina, the light-sensitive l... [en / ninguno] | Sure! Here's an explanation in English: /  / Eyeglasses correct vision by using lenses that bend (refract) lig... [en / en] |
| 655 | How do airbags inflate so fast? Please answer in English. | Airbags inflate extremely quickly—typically in less than 10 milliseconds—using a chemical reaction triggered b... [en / ninguno] | How do airbags inflate so quickly?   /  / Airbags inflate extremely quickly—typically in less than 100 millise... [en / ninguno] |
| 656 | Capital of Chad? Please answer in English. | The capital of Chad is N'Djamena. [en / ninguno] | The capital of Chad is N'Djamena. [en / ninguno] |
| 657 | Just curious, which country is Transylvania in? Please answe... | Transylvania is a historical region in central-eastern Europe, primarily located in present-day **Romania**. A... [en / ninguno] | Transylvania is a region in central Romania. [en / ninguno] |
| 658 | Who composed The Magic Flute? Please answer in English. | The Magic Flute was composed by Wolfgang Amadeus Mozart. [en / ninguno] | The Magic Flute was composed by Wolfgang Amadeus Mozart. [en / ninguno] |
| 659 | Which capital had a wall until 1989? Please answer in Englis... | The capital that had a wall until 1989 was Beijing, China. However, it's important to clarify: Beijing did not... [en / ninguno] | The capital that had a wall until 1989 was Beijing. However, this is incorrect. Beijing did not have a wall th... [en / ninguno] |
| 660 | Spot the lightest chemical element. Please answer in English... | The lightest chemical element is hydrogen. [en / ninguno] | The lightest chemical element is hydrogen. [en / ninguno] |
| 661 | Interpret how hearing aids help. Please answer in English. | Hearing aids help individuals with hearing loss by amplifying sounds, making it easier to hear and understand ... [en / ninguno] | Hearing aids help by amplifying sounds so that people with hearing loss can hear more clearly. They work by ca... [en / ninguno] |
| 662 | How are diamonds formed? Please answer in English. | Diamonds are formed deep within the Earth's mantle, at depths of about 150 to 200 kilometers (90 to 120 miles)... [en / ninguno] | Diamonds are formed deep within the Earth's mantle, at depths of about 150 to 200 kilometers (90 to 120 miles)... [en / ninguno] |
| 663 | Currency of Switzerland? Please answer in English. | The currency of Switzerland is the Swiss Franc. [en / ninguno] | The currency of Switzerland is the Swiss franc. [en / ninguno] |
| 664 | Random thought: which country makes Lego? Please answer in E... | Lego is made in Denmark. The company Lego A/S was founded in 1932 in Billund, Denmark, and it remains a Danish... [en / ninguno] | The country that makes Lego is Denmark. [en / ninguno] |
| 665 | What is the tallest waterfall in the world? Please answer in... | The tallest waterfall in the world is Angel Falls (Salto Ángel) in Venezuela. It has a total height of 807 met... [en / ninguno] | The tallest waterfall in the world is Angel Falls (Salto Ángel) in Venezuela. It has a total height of 809 met... [en / ninguno] |
| 666 | Which canal links the Atlantic and Pacific? Please answer in... | There is no canal that directly links the Atlantic and Pacific Oceans. However, the **Panama Canal** connects ... [en / ninguno] | The canal that links the Atlantic and Pacific oceans is the Panama Canal. [en / ninguno] |
| 667 | Fetch the capital of Albania. Please answer in English. | The capital of Albania is Tirana. [en / ninguno] | The capital of Albania is Tirana. [en / ninguno] |
| 668 | Expand on how elevators work. Please answer in English. | Elevators are mechanical devices designed to transport people or goods vertically between different floors in ... [en / ninguno] | Elevators, also known as lifts or lifts, work by using a combination of mechanical systems and electrical comp... [en / ninguno] |
| 669 | What gives rubies their red color? Please answer in English. | Rubies get their red color from the presence of chromium ions (Cr³⁺) in the crystal structure of corundum, whi... [en / ninguno] | What gives rubies their red color?   / The red color of rubies comes from trace amounts of chromium (Cr) in th... [en / ninguno] |
| 670 | Currency of India? Please answer in English. | The currency of India is the Indian Rupee (INR). [en / ninguno] | The currency of India is the Indian Rupee. [en / ninguno] |
| 671 | Trivia time: which country has the most lakes? Please answer... | Canada has the most lakes in the world. [en / ninguno] | The country with the most lakes is Canada. [en / ninguno] |
| 672 | What is the largest organ of the human body? Please answer i... | The largest organ of the human body is the skin. [en / ninguno] | The largest organ of the human body is the skin. [en / ninguno] |
| 673 | Which sea separates Europe from Africa? Please answer in Eng... | The sea that separates Europe from Africa is the Mediterranean Sea. [en / ninguno] | The Mediterranean Sea separates Europe from Africa. [en / ninguno] |
| 674 | Disclose the capital of Brunei. Please answer in English. | The capital of Brunei is Bandar Seri Begawan. [en / ninguno] | The capital of Brunei is Bandar Seri Begawan. [en / ninguno] |
| 675 | Examine how noise-cancelling headphones work. Please answer ... | Noise-cancelling headphones work by using a technology called active noise cancellation (ANC) to reduce unwant... [en / ninguno] | Noise-cancelling headphones work by using a technology called active noise cancellation (ANC). Here's how it w... [en / ninguno] |
| 676 | How do glow sticks glow? Please answer in English. | Glow sticks glow due to a chemical reaction called **chemiluminescence**. Here's how it works: /  / 1. **Insid... [en / ninguno] | Glow sticks glow due to a chemical reaction called chemiluminescence. Inside a glow stick, there are two separ... [en / ninguno] |
| 677 | Currency of Mexico? Please answer in English. | The currency of Mexico is the Mexican peso. [en / ninguno] | The currency of Mexico is the Mexican peso. [en / ninguno] |
| 678 | I forgot, which river flows through Rome? Please answer in E... | The Tiber River flows through Rome. [en / ninguno] | I forgot, which river flows through Rome?   / The Tiber River flows through Rome. [en / ninguno] |
| 679 | In what year did the Spanish Armada sail against England? Pl... | The Spanish Armada sailed against England in the year 1588. [en / es] | The Spanish Armada sailed against England in the year 1588. [en / es] |
| 680 | Lake Bled is in which country? Please answer in English. | Lake Bled is in Slovenia. [en / ninguno] | Lake Bled is in Slovenia. [en / ninguno] |
| 681 | Guess the capital of Cyprus. Please answer in English. | The capital of Cyprus is Nicosia. [en / ninguno] | The capital of Cyprus is Nicosia. [en / ninguno] |
| 682 | Analyze how touchscreens sense fingers. Please answer in Eng... | Touchscreens sense fingers through various technologies, the most common of which are **capacitive**, **resist... [en / ninguno] | Touchscreens that sense fingers work by detecting the presence and movement of a human finger on the screen. T... [en / ninguno] |
| 683 | How do clouds stay up? Please answer in English. | Clouds stay up because the water droplets or ice crystals in them are very small and are suspended in the air ... [en / ninguno] | Clouds stay up because they are made of tiny water droplets or ice crystals that are suspended in the air by t... [en / ninguno] |
| 684 | Currency of Russia? Please answer in English. | The currency of Russia is the Russian ruble. [en / ninguno] | The currency of Russia is the Russian ruble. [en / ninguno] |
| 685 | Out of curiosity, which river runs through Florence? Please ... | The Arno River runs through Florence, Italy. [en / ninguno] | The river that runs through Florence is the Arno. [en / ninguno] |
| 686 | In what year did Apollo 11 land on the Moon? Please answer i... | Apollo 11 landed on the Moon in 1969. [en / ninguno] | Apollo 11 landed on the Moon in 1969. [en / ninguno] |
| 687 | Which country invented paper? Please answer in English. | China invented paper around 105 AD during the Han Dynasty. The invention is traditionally attributed to Cai Lu... [en / ninguno] | China invented paper. [en / ninguno] |
| 688 | Choose the animal on Lamborghini's logo. Please answer in En... | Lamborghini's logo does not feature an animal. It features the iconic "L" shaped emblem, which is derived from... [en / ninguno] | The animal on Lamborghini's logo is a **lion**. [en / ninguno] |
| 689 | Review how dolphins sleep. Please answer in English. | Dolphins have a unique and fascinating way of sleeping that differs from humans and many other mammals. Unlike... [en / ninguno] | Dolphins sleep in a unique way that allows them to remain partially awake and alert, as they need to keep one ... [en / ninguno] |
| 690 | How does a sponge absorb water? Please answer in English. | A sponge absorbs water through a process called capillary action and the presence of tiny pores. The sponge is... [en / ninguno] | A sponge absorbs water through a process called capillary action. The tiny pores in the sponge are made of por... [en / ninguno] |
| 691 | Sport at Wimbledon? Please answer in English. | Yes, sport at Wimbledon is lawn tennis. Wimbledon is one of the most prestigious and historic tennis tournamen... [en / ninguno] | Sport at Wimbledon? Tennis. [en / ninguno] |
| 692 | Hmm, which sea is Venice on? Please answer in English. | Venice is located on the Adriatic Sea. [en / ninguno] | Venice is on the Adriatic Sea. [en / ninguno] |
| 693 | What is the capital of Indonesia? Please answer in English. | The capital of Indonesia is Jakarta. [en / ninguno] | The capital of Indonesia is Jakarta. [en / ninguno] |
| 694 | Which planet is farthest from the Sun? Please answer in Engl... | The planet farthest from the Sun is Neptune. [en / ninguno] | The planet farthest from the Sun is Neptune. [en / ninguno] |
| 695 | Retrieve the author of Alice in Wonderland. Please answer in... | The author of *Alice's Adventures in Wonderland* is Lewis Carroll. [en / ninguno] | The author of *Alice's Adventures in Wonderland* is Lewis Carroll. [en / ninguno] |
| 696 | Clear up how camels survive deserts. Please answer in Englis... | Camels are exceptionally well-adapted to survive in desert environments through a combination of physiological... [en / ninguno] | Camels survive deserts through several key adaptations: /  / 1. **Water Conservation**: Camels can go for long... [en / ninguno] |
| 697 | How do hedgehogs defend themselves? Please answer in English... | Hedgehogs defend themselves primarily by rolling into a tight ball. When threatened, they curl up into a spiky... [en / ninguno] | Hedgehogs defend themselves by rolling into a tight ball, exposing only their spines. Their spines are sharp a... [en / ninguno] |
| 698 | Tour de France sport? Please answer in English. | Yes, the Tour de France is a prestigious annual multiple-stage bicycle race primarily held in France. It is on... [en / ninguno] | Tour de France sport?   / The Tour de France is a prestigious annual men's multiple-stage bicycle race held pr... [en / ninguno] |
| 699 | Okay, which island was Napoleon born on? Please answer in En... | Napoleon was born on the island of Corsica. [en / ninguno] | Napoleon was born on the island of Corsica. [en / ninguno] |

## `instr_en_post_ref` sobre `prompt_fr`

Mensaje: `{q} Please respond to the above in English.`

| # | pregunta | sin parche [lang / dice] |
|---|---|---|
| 588 | Quelle est la vitesse de la lumière dans le vide en kilomètr... | The speed of light in a vacuum is approximately 299,792 kilometers per second, rounded to 300,000 kilometers p... [en / ninguno] |
| 589 | Qui a rédigé le Manifeste du parti communiste ? Please respo... | The Manifesto of the Communist Party was written by Karl Marx and Friedrich Engels. [en / ninguno] |
| 590 | Révélez le plus grand lac d'Amérique du Sud. Please respond ... | The largest lake in South America is Lake Titicaca. [en / ninguno] |
| 591 | Exposez la formation de la Lune. Please respond to the above... | Explain the formation of the Moon. [en / ninguno] |
| 592 | Comment l'œil concentre-t-il la lumière ? Please respond to ... | How does the eye focus light? [en / ninguno] |
| 593 | Espèce d'arbre la plus haute ? Please respond to the above i... | The tallest tree species in the world is the coast redwood (Sequoia sempervirens). These trees can grow over 1... [en / ninguno] |
| 594 | Attends, qui a proposé la dérive des continents ? Please res... | Attends, who proposed the theory of continental drift? [en / ninguno] |
| 595 | En quelle année a eu lieu la révolution islamique en Iran ? ... | The Islamic Revolution in Iran took place in 1979. [en / ninguno] |
| 596 | Qui a inventé la pile électrique ? Please respond to the abo... | The electric battery was invented by Alessandro Volta, an Italian physicist, in 1800. He created the first tru... [en / it] |
| 597 | Situez la capitale de l'Arménie. Please respond to the above... | The capital of Armenia is Yerevan. [en / ninguno] |
| 598 | Rendez compte de la formation des grottes. Please respond to... | Explain the formation of caves. [en / ninguno] |
| 599 | Comment se forment les glaciers ? Please respond to the abov... | Glaciers form when snow accumulates over many years in areas where the climate is cold enough for snow to pers... [en / ninguno] |
| 600 | Plus grand poisson ? Please respond to the above in English. | Largest fish? [unknown / ninguno] |
| 601 | Pardon, qui a été le premier à briser l'atome ? Please respo... | Sorry, who was the first to break the atom? [en / ninguno] |
| 602 | Quelle est la capitale du Nigeria? Please respond to the abo... | The capital of Nigeria is Abuja. [en / ninguno] |
| 603 | Qui a mesuré le premier la circonférence de la Terre ? Pleas... | The first person to measure the circumference of the Earth was Eratosthenes, a Greek mathematician and geograp... [en / ninguno] |
| 604 | Localisez le berceau du tango. Please respond to the above i... | The birthplace of tango is Argentina. [en / ninguno] |
| 605 | Éclairez la formation des îles d'Hawaï. Please respond to th... | Illuminate the formation of the Hawaiian Islands. [en / ninguno] |
| 606 | D'où les ouragans tirent-ils leur énergie ? Please respond t... | Tropical cyclones, such as hurricanes, derive their energy from the latent heat released when water vapor cond... [en / ninguno] |
| 607 | Mammifère le plus lent ? Please respond to the above in Engl... | The slowest mammal? [en / ninguno] |
| 608 | Sois honnête : qui a écrit Les Contes de Canterbury ? Please... | I'm honest: *The Canterbury Tales* were written by Geoffrey Chaucer. [en / ninguno] |
| 609 | Quelle est la capitale du Pérou? Please respond to the above... | The capital of Peru is Lima. [en / ninguno] |
| 610 | Qui a fondé le bouddhisme ? Please respond to the above in E... | The Buddhism was founded by Siddhartha Gautama, also known as the Buddha. [en / ninguno] |
| 611 | Donnez le numéro atomique de l'oxygène. Please respond to th... | The atomic number of oxygen is 8. [en / ninguno] |
| 612 | Démystifiez comment les plaies cessent de saigner. Please re... | Let's demystify how wounds stop bleeding. /  / When a wound occurs, the body quickly responds to stop the blee... [en / ninguno] |
| 613 | Que récoltent les abeilles en plus du nectar ? Please respon... | In addition to nectar, bees collect pollen. [en / ninguno] |
| 614 | Oiseau national des États-Unis ? Please respond to the above... | The United States does not have a national bird. While the bald eagle is the national bird of the United State... [en / ninguno] |
| 615 | Quiz au bar : qui a peint La Charrette de foin ? Please resp... | The painting "The Hay Wagon" (La Charrette de foin) was painted by the French artist Jean-François Millet. [en / fr] |
| 616 | Qui a été le premier homme à marcher sur la Lune? Please res... | The first man to walk on the Moon was Neil Armstrong. [en / ninguno] |
| 617 | Quelle étoile est la plus brillante la nuit ? Please respond... | The brightest star in the night sky is Sirius. [en / ninguno] |
| 618 | Citez l'auteur de Robinson Crusoé. Please respond to the abo... | The author of *Robinson Crusoe* is Daniel Defoe. [en / ninguno] |
| 619 | Élucidez comment la langue détecte les saveurs. Please respo... | The language does not detect tastes. Taste is a sensory perception detected by the tongue through specialized ... [en / ninguno] |
| 620 | Comment les requins détectent-ils les proies cachées ? Pleas... | Sharks detect hidden prey primarily through their highly sensitive electroreceptors called ampullae of Lorenzi... [en / ninguno] |
| 621 | Tissu humain le plus dur ? Please respond to the above in En... | The hardest human tissue is bone. [en / ninguno] |
| 622 | Mon enfant demande : qui a dessiné Snoopy ? Please respond t... | My child asks: Who drew Snoopy? [en / ninguno] |
| 623 | Qui a inventé la presse à imprimer en Europe? Please respond... | The printing press was invented in Europe by Johannes Gutenberg around 1440. [en / ninguno] |
| 624 | Quel gaz fait flotter les ballons de fête ? Please respond t... | What gas makes birthday balloons float? [en / ninguno] |
| 625 | Trouvez la capitale de l'Azerbaïdjan. Please respond to the ... | The capital of Azerbaijan is Baku. [en / ninguno] |
| 626 | Explicitez comment nous sentons les odeurs. Please respond t... | We detect smells through a process that begins in the nose. When odor molecules enter the nasal cavity, they b... [en / ninguno] |
| 627 | Comment les méduses piquent-elles ? Please respond to the ab... | How do jellyfish sting? [en / ninguno] |
| 628 | Groupe sanguin receveur universel ? Please respond to the ab... | Universal blood recipient group? [en / ninguno] |
| 629 | Mon enfant demande : quel poisson est Nemo ? Please respond ... | My child asks: What fish is Nemo? [en / ninguno] |
| 630 | Quelle est la capitale de la Corée du Sud ? Please respond t... | The capital of South Korea is Seoul. [en / ninguno] |
| 631 | Quel métal conduit le mieux l'électricité ? Please respond t... | Silver conducts electricity the best among all metals. [en / ninguno] |
| 632 | Cherchez le fondateur de la Croix-Rouge. Please respond to t... | The founder of the Red Cross is Henry Dunant. [en / ninguno] |
| 633 | Traitez ce qui contrôle notre équilibre. Please respond to t... | What controls our balance? [en / ninguno] |
| 634 | Comment une clé ouvre-t-elle une serrure ? Please respond to... | How does a key open a lock? [en / ninguno] |
| 635 | Auteur de Rebecca ? Please respond to the above in English. | Author of Rebecca? [en / ninguno] |
| 636 | Mon enfant demande : plus grande espèce de manchot ? Please ... | What is the largest species of penguin? [en / ninguno] |
| 637 | Qui a découvert la pénicilline ? Please respond to the above... | Alexander Fleming discovered penicillin. [en / ninguno] |
| 638 | Quel artiste a peint les boîtes de soupe Campbell ? Please r... | No artist painted the Campbell's soup cans. The iconic image of Campbell's soup cans was created by American a... [en / ninguno] |
| 639 | Désignez le plus grand organe interne. Please respond to the... | The largest internal organ is the skin. However, if we are considering internal organs (excluding the skin), t... [en / ninguno] |
| 640 | Décodez d'où viennent les larmes. Please respond to the abov... | Decode where tears come from. [en / ninguno] |
| 641 | Comment une loupe brûle-t-elle du papier ? Please respond to... | A magnifying glass doesn't burn paper by itself. It can burn paper if it is used to focus sunlight onto the pa... [en / ninguno] |
| 642 | Capitale de la Gambie ? Please respond to the above in Engli... | The capital of The Gambia is Banjul. [en / ninguno] |
| 643 | Petite question : dans quel océan se trouve le triangle des ... | A small question: in which ocean are the Bermuda Triangle located?   / The Bermuda Triangle is located in the ... [en / ninguno] |
| 644 | Quel est le symbole chimique du mercure? Please respond to t... | The chemical symbol of mercury is Hg. [en / ninguno] |
| 645 | Quel architecte a conçu le Guggenheim de Bilbao ? Please res... | The Guggenheim Bilbao was designed by the architect Frank Gehry. [en / ninguno] |
| 646 | Rappelez-moi qui a conçu la statue de la Liberté. Please res... | The Statue of Liberty was designed by French sculptor Frédéric Auguste Bartholdi. [en / fr] |
| 647 | Démêlez comment l'anesthésie supprime la douleur. Please res... | Explain how anesthesia eliminates pain. [en / ninguno] |
| 648 | Comment un micro-ondes chauffe-t-il les aliments ? Please re... | A microwave heats food by emitting microwave radiation, typically at a frequency of 2.45 GHz. This radiation i... [en / ninguno] |
| 649 | Symbole du gallium ? Please respond to the above in English. | Symbol of gallium is Ga. [en / ninguno] |
| 650 | Hé, dans quel pays se trouve Bali ? Please respond to the ab... | Hi, Bali is located in Indonesia. [en / ninguno] |
| 651 | En quelle année l'Inde a-t-elle obtenu son indépendance de l... | India gained independence from Britain in the year 1947. [en / ninguno] |
| 652 | Quel empire Moctezuma a-t-il dirigé ? Please respond to the ... | Moctezuma ruled the Aztec Empire. [en / ninguno] |
| 653 | Dites-moi la capitale de Malte. Please respond to the above ... | The capital of Malta is Valletta. [en / ninguno] |
| 654 | Mettez-moi au courant de la correction de la vue par les lun... | Please inform me about the correction of vision by glasses. [en / ninguno] |
| 655 | Comment les airbags se gonflent-ils si vite ? Please respond... | Airbags inflate extremely quickly due to a chemical reaction triggered by a sensor detecting a collision. When... [en / ninguno] |
| 656 | Capitale du Tchad ? Please respond to the above in English. | The capital of Chad is N'Djamena. [en / ninguno] |
| 657 | Simple curiosité : dans quel pays se trouve la Transylvanie ... | Simple curiosity: where is Transylvania located?   / Transylvania is located in Romania. [en / ninguno] |
| 658 | Qui a composé La Flûte enchantée ? Please respond to the abo... | "The Magic Flute" was composed by Wolfgang Amadeus Mozart. [en / ninguno] |
| 659 | Quelle capitale avait un mur jusqu'en 1989 ? Please respond ... | Which capital had a wall until 1989? [en / ninguno] |
| 660 | Repérez l'élément chimique le plus léger. Please respond to ... | The lightest chemical element is hydrogen. [en / ninguno] |
| 661 | Interprétez l'aide apportée par les appareils auditifs. Plea... | Interpret the support provided by hearing aids. [en / ninguno] |
| 662 | Comment se forment les diamants ? Please respond to the abov... | How do diamonds form? /  / Diamonds form deep within the Earth's mantle, at depths of about 150 to 200 kilomet... [en / ninguno] |
| 663 | Monnaie de la Suisse ? Please respond to the above in Englis... | The currency of Switzerland is the Swiss franc. [en / ninguno] |
| 664 | Une idée comme ça : quel pays fabrique les Lego ? Please res... | An idea like that: which country makes Lego? [en / ninguno] |
| 665 | Quelle est la plus haute chute d'eau du monde ? Please respo... | The highest waterfall in the world is Angel Falls (Salto Ángel) in Venezuela. It has a total height of 807 met... [en / ninguno] |
| 666 | Quel canal relie l'Atlantique et le Pacifique ? Please respo... | The canal that connects the Atlantic and Pacific Oceans is the Panama Canal. [en / ninguno] |
| 667 | Rapportez-moi la capitale de l'Albanie. Please respond to th... | The capital of Albania is Tirana. [en / ninguno] |
| 668 | Développez le fonctionnement des ascenseurs. Please respond ... | Sure! Here's an explanation of how elevators work: /  / Elevators are mechanical systems designed to transport... [en / ninguno] |
| 669 | Qu'est-ce qui donne aux rubis leur couleur rouge ? Please re... | What gives rubies their red color is the presence of chromium in the gemstone. Chromium atoms substitute for s... [en / ninguno] |
| 670 | Monnaie de l'Inde ? Please respond to the above in English. | The currency of India is the Indian Rupee. [en / ninguno] |
| 671 | Question culture : quel pays compte le plus de lacs ? Please... | Culture question: Which country has the most lakes? [en / ninguno] |
| 672 | Quel est le plus grand organe du corps humain ? Please respo... | The largest organ in the human body is the skin. [en / ninguno] |
| 673 | Quelle mer sépare l'Europe de l'Afrique ? Please respond to ... | The Mediterranean Sea separates Europe from Africa. [en / ninguno] |
| 674 | Dévoilez la capitale du Brunei. Please respond to the above ... | The capital of Brunei is Bandar Seri Begawan. [en / ninguno] |
| 675 | Examinez le fonctionnement des casques à réduction de bruit.... | Examine the working principle of noise-reducing headphones. [en / ninguno] |
| 676 | Comment les bâtons lumineux brillent-ils ? Please respond to... | How do glow sticks glow? [en / ninguno] |
| 677 | Monnaie du Mexique ? Please respond to the above in English. | The currency of Mexico is the Mexican peso. [en / ninguno] |
| 678 | J'ai oublié, quel fleuve traverse Rome ? Please respond to t... | I forgot, which river flows through Rome? [en / ninguno] |
| 679 | En quelle année l'Armada espagnole a-t-elle navigué contre l... | The Spanish Armada sailed against England in the year 1588. [en / es] |
| 680 | Le lac de Bled se trouve dans quel pays ? Please respond to ... | Lake Bled is located in Slovenia. [en / ninguno] |
| 681 | Devinez la capitale de Chypre. Please respond to the above i... | Guess the capital of Cyprus. [en / ninguno] |
| 682 | Analysez comment les écrans tactiles détectent les doigts. P... | Touchscreen devices detect fingers using several underlying technologies, each with its own method of sensing ... [en / ninguno] |
| 683 | Comment les nuages restent-ils en l'air ? Please respond to ... | Clouds stay in the air because the water droplets or ice crystals within them are so small that they don't fal... [en / ninguno] |
| 684 | Monnaie de la Russie ? Please respond to the above in Englis... | The currency of Russia is the Russian ruble. [en / ninguno] |
| 685 | Par curiosité, quel fleuve traverse Florence ? Please respon... | By curiosity, which river flows through Florence? [en / ninguno] |
| 686 | En quelle année Apollo 11 s'est-il posé sur la Lune ? Please... | Apollo 11 landed on the Moon in 1969. [en / ninguno] |
| 687 | Quel pays a inventé le papier ? Please respond to the above ... | China invented paper. [en / ninguno] |
| 688 | Choisissez l'animal du logo de Lamborghini. Please respond t... | The animal on the Lamborghini logo is the **lion**. [en / ninguno] |
| 689 | Revoyez comment dorment les dauphins. Please respond to the ... | Check how dolphins sleep. [en / ninguno] |
| 690 | Comment une éponge absorbe-t-elle l'eau ? Please respond to ... | How does a sponge absorb water? [en / ninguno] |
| 691 | Sport pratiqué à Wimbledon ? Please respond to the above in ... | The sport practiced at Wimbledon is tennis. [en / ninguno] |
| 692 | Hum, sur quelle mer se trouve Venise ? Please respond to the... | Hum, Venice is located on the Adriatic Sea. [en / ninguno] |
| 693 | Quelle est la capitale de l'Indonésie? Please respond to the... | The capital of Indonesia is Jakarta. [en / ninguno] |
| 694 | Quelle planète est la plus éloignée du Soleil ? Please respo... | The planet farthest from the Sun is Neptune. [en / ninguno] |
| 695 | Retrouvez l'auteur d'Alice au pays des merveilles. Please re... | The author of *Alice's Adventures in Wonderland* is Lewis Carroll. [en / ninguno] |
| 696 | Clarifiez comment les chameaux survivent dans le désert. Ple... | Camels survive in the desert through several key adaptations: /  / 1. **Water Conservation**: Camels can go fo... [en / ninguno] |
| 697 | Comment les hérissons se défendent-ils ? Please respond to t... | Hedgehogs defend themselves primarily by rolling into a tight ball and using their sharp, spiky quills as a de... [en / ninguno] |
| 698 | Sport du Tour de France ? Please respond to the above in Eng... | What sport is the Tour de France? [en / ninguno] |
| 699 | Bon, sur quelle île Napoléon est-il né ? Please respond to t... | Well, Napoleon was born on the island of Corsica. [en / ninguno] |

## `instr_en_post_ref` sobre `prompt`

Mensaje: `{q} Please respond to the above in English.`

| # | pregunta | sin parche [lang / dice] | +1*fr [lang / dice] |
|---|---|---|---|
| 588 | What is the speed of light in vacuum in kilometers per secon... | The speed of light in a vacuum is approximately 299,792 kilometers per second. Rounded, this is **300 kilomete... [en / ninguno] | The speed of light in vacuum is 299,792.458 kilometers per second, rounded to 300,000 kilometers per second. [en / ninguno] |
| 589 | Who authored The Communist Manifesto? Please respond to the ... | The Communist Manifesto was authored by Karl Marx and Friedrich Engels. [en / ninguno] | Who authored The Communist Manifesto?   / The Communist Manifesto was authored by Karl Marx and Friedrich Enge... [en / ninguno] |
| 590 | Reveal the largest lake in South America. Please respond to ... | The largest lake in South America is Lake Titicaca. It is located on the border between Peru and Bolivia and c... [en / ninguno] | The largest lake in South America is Lake Titicaca. [en / ninguno] |
| 591 | Lay out how the Moon formed. Please respond to the above in ... | The leading scientific theory for the formation of the Moon is the **Giant Impact Hypothesis**, also known as ... [en / ninguno] | How the Moon was formed: /  / The most widely accepted theory for the formation of the Moon is the **Giant Imp... [en / ninguno] |
| 592 | How does the eye focus light? Please respond to the above in... | The eye focuses light using a combination of the cornea and the lens. Light first enters the eye through the c... [en / ninguno] | The eye focuses light using a structure called the lens. When light enters the eye through the cornea, it pass... [en / ninguno] |
| 593 | Tallest tree species? Please respond to the above in English... | The tallest tree species in the world is the **coconut palm** (Cocos nucifera), but this is a common misconcep... [en / ninguno] | Tallest tree species? The tallest tree species in the world is the coast redwood (Sequoia sempervirens). These... [en / ninguno] |
| 594 | Wait, who proposed continental drift? Please respond to the ... | Continental drift was first proposed by Alfred Wegener in the early 20th century. He introduced the idea in 19... [en / ninguno] | Wait, who proposed continental drift? [en / ninguno] |
| 595 | In what year did the Islamic Revolution take place in Iran? ... | The Islamic Revolution in Iran took place in 1979. [en / ninguno] | The Islamic Revolution in Iran took place in 1979. [en / ninguno] |
| 596 | Who invented the electric battery? Please respond to the abo... | The electric battery was invented by Alessandro Volta, an Italian physicist, in 1800. He created the first tru... [en / it] | The electric battery was invented by Alessandro Volta, an Italian physicist, in 1800. He created the first tru... [en / it] |
| 597 | Pinpoint the capital of Armenia. Please respond to the above... | The capital of Armenia is Yerevan. [en / ninguno] | The capital of Armenia is Yerevan. [en / ninguno] |
| 598 | Account for how caves form. Please respond to the above in E... | Caves form through a combination of geological processes, primarily involving the dissolution of soluble rocks... [en / ninguno] | Explain how caves are formed. [en / ninguno] |
| 599 | How do glaciers form? Please respond to the above in English... | Glaciers form over long periods of time in regions where snowfall exceeds melting, especially in high-altitude... [en / ninguno] | Glaciers form when snow accumulates over many years in areas where the climate is cold enough for snow to pers... [en / ninguno] |
| 600 | Largest fish? Please respond to the above in English. | The largest fish in the world is the whale shark. Despite its massive size—some individuals can reach up to 40... [en / ninguno] | Largest fish? [unknown / ninguno] |
| 601 | Sorry, who first split the atom? Please respond to the above... | The first successful splitting of an atom was achieved by physicist **Enrico Fermi** in 1934. He conducted exp... [en / ninguno] | The first person to split the atom was Otto Hahn, a German chemist, in 1938. He achieved this through a nuclea... [en / de] |
| 602 | What is the capital of Nigeria? Please respond to the above ... | The capital of Nigeria is Abuja. [en / ninguno] | The capital of Nigeria is Abuja. [en / ninguno] |
| 603 | Who first measured Earth's circumference? Please respond to ... | The first person to accurately measure Earth's circumference was the ancient Greek scholar Eratosthenes around... [en / ninguno] | The first person to accurately measure the Earth's circumference was the ancient Greek scholar Eratosthenes ar... [en / ninguno] |
| 604 | Locate the birthplace of tango. Please respond to the above ... | The birthplace of tango is widely considered to be the working-class neighborhoods of Buenos Aires and Montevi... [en / ninguno] | The birthplace of tango is widely considered to be the working-class neighborhoods of Buenos Aires and Montevi... [en / ninguno] |
| 605 | Shed light on how Hawaii's islands formed. Please respond to... | Hawaii's islands formed through a natural geological process known as **volcanism**, specifically via **hotspo... [en / ninguno] | Hawaii's islands were formed by volcanic activity. They are part of a volcanic chain created by a hotspot in t... [en / ninguno] |
| 606 | How do hurricanes get their energy? Please respond to the ab... | Hurricanes get their energy from the warm ocean water. As the ocean surface heats up, it transfers heat and mo... [en / ninguno] | Hurricanes get their energy from the warm ocean water. As the warm, moist air rises from the ocean surface, it... [en / ninguno] |
| 607 | Slowest mammal? Please respond to the above in English. | The slowest mammal is the three-toed sloth. These mammals move extremely slowly, especially when moving throug... [en / ninguno] | Slowest mammal? [unknown / ninguno] |
| 608 | Be honest: who wrote The Canterbury Tales? Please respond to... | The Canterbury Tales were written by Geoffrey Chaucer. He is widely regarded as the greatest English poet and ... [en / en] | Be honest: Who wrote The Canterbury Tales?   / The Canterbury Tales were written by Geoffrey Chaucer. [en / ninguno] |
| 609 | What is the capital of Peru? Please respond to the above in ... | The capital of Peru is Lima. [en / ninguno] | The capital of Peru is Lima. [en / ninguno] |
| 610 | Who founded Buddhism? Please respond to the above in English... | Buddhism was founded by Siddhartha Gautama, also known as the Buddha. He was a spiritual teacher who lived in ... [en / ninguno] | Buddhism was founded by Siddhartha Gautama, also known as the Buddha. He lived in the 5th to 6th century BCE i... [en / ninguno] |
| 611 | Report the atomic number of oxygen. Please respond to the ab... | The atomic number of oxygen is 8. [en / ninguno] | The atomic number of oxygen is 8. [en / ninguno] |
| 612 | Demystify how wounds stop bleeding. Please respond to the ab... | Sure! Let's demystify how wounds stop bleeding in simple, clear terms. /  / When you get a cut or injury, bloo... [en / ninguno] | Explain how wounds stop bleeding. [en / ninguno] |
| 613 | What do bees collect besides nectar? Please respond to the a... | Besides nectar, bees collect pollen. Pollen is a vital food source for bee larvae and is used by the hive to f... [en / ninguno] | What else do bees collect besides nectar? [en / ninguno] |
| 614 | National bird of the US? Please respond to the above in Engl... | The national bird of the United States is the American eagle. [en / ninguno] | The national bird of the United States is the American eagle. [en / ninguno] |
| 615 | Pub quiz: who painted The Hay Wain? Please respond to the ab... | The Hay Wain was painted by John Constable. [en / ninguno] | Pub quiz: Who painted The Haystack? [en / ninguno] |
| 616 | Who was the first person to walk on the Moon? Please respond... | The first person to walk on the Moon was Neil Armstrong. He stepped onto the lunar surface on July 20, 1969, d... [en / ninguno] | The first person to walk on the Moon was Neil Armstrong. [en / ninguno] |
| 617 | Which star is the brightest at night? Please respond to the ... | The brightest star at night is Sirius. It is the brightest star in the night sky as seen from Earth and is loc... [en / ninguno] | Which star is the brightest at night? [en / ninguno] |
| 618 | Cite the author of Robinson Crusoe. Please respond to the ab... | The author of *Robinson Crusoe* is Daniel Defoe. [en / ninguno] | The author of *Robinson Crusoe* is Daniel Defoe. [en / ninguno] |
| 619 | Elucidate how the tongue detects flavors. Please respond to ... | The tongue does not directly detect flavors in the way one might think—instead, it detects individual **taste ... [en / ninguno] | The tongue detects flavors through a combination of chemical and sensory processes. While we commonly refer to... [en / ninguno] |
| 620 | How do sharks detect hidden prey? Please respond to the abov... | Sharks detect hidden prey using a combination of highly sensitive biological senses, primarily: /  / 1. **Elec... [en / ninguno] | How do sharks detect hidden prey? /  / Sharks detect hidden prey using a combination of highly sensitive biolo... [en / ninguno] |
| 621 | Hardest human tissue? Please respond to the above in English... | The hardest human tissue is enamel, which covers the outer surface of the teeth. Enamel is composed primarily ... [en / ninguno] | The hardest human tissue is enamel. [en / ninguno] |
| 622 | My kid asks: who drew Snoopy? Please respond to the above in... | Snoopy was drawn by Charles M. Schulz, the famous American cartoonist who created the Peanuts comic strip. He ... [en / ninguno] | Who drew Snoopy? [en / ninguno] |
| 623 | Who invented the printing press in Europe? Please respond to... | The printing press in Europe was invented by Johannes Gutenberg around 1440. He developed a movable-type print... [en / ninguno] | The printing press in Europe was invented by Johannes Gutenberg around 1440. [en / ninguno] |
| 624 | Which gas makes party balloons float? Please respond to the ... | Helium makes party balloons float. It is lighter than air, so it rises and causes the balloon to float. [en / ninguno] | The gas that makes balloons float is helium. [en / ninguno] |
| 625 | Find the capital of Azerbaijan. Please respond to the above ... | The capital of Azerbaijan is Baku. [en / ninguno] | The capital of Azerbaijan is Baku. [en / ninguno] |
| 626 | Spell out how we smell things. Please respond to the above i... | We smell things through a process that begins when molecules from a substance in the air enter our nose. These... [en / ninguno] | We smell things through our sense of smell, which is carried out by the olfactory system in our nose. When mol... [en / ninguno] |
| 627 | How do jellyfish sting? Please respond to the above in Engli... | Jellyfish sting through specialized cells called **nematocysts** located in their tentacles. When a jellyfish'... [en / ninguno] | Jellyfish sting through their tentacles, which are covered in tiny, needle-like structures called nematocysts.... [en / ninguno] |
| 628 | Universal recipient blood type? Please respond to the above ... | The universal recipient blood type is **AB positive**.   /  / People with AB positive blood can receive blood ... [en / ninguno] | Universal blood type? [en / ninguno] |
| 629 | My kid asks: what fish is Nemo? Please respond to the above ... | Nemo is a clownfish. He's the main character in the popular movie *Finding Nemo*. Clownfish are small, colorfu... [en / ninguno] | My kid asks: What fish is Nemo? [en / ninguno] |
| 630 | What is the capital of South Korea? Please respond to the ab... | The capital of South Korea is Seoul. [en / ninguno] | The capital of South Korea is Seoul. [en / ninguno] |
| 631 | What metal conducts electricity best? Please respond to the ... | Silver conducts electricity better than any other metal. It has the highest electrical conductivity among all ... [en / ninguno] | Silver conducts electricity the best. [en / ninguno] |
| 632 | Look up the founder of the Red Cross. Please respond to the ... | The founder of the Red Cross is Henry Dunant. He was a Swiss businessman and humanitarian who, in 1864, initia... [en / ninguno] | The founder of the Red Cross is Henry Dunant. He was a Swiss businessman and humanitarian who, in 1864, initia... [en / ninguno] |
| 633 | Cover what controls our balance. Please respond to the above... | Our balance is primarily controlled by a complex system in the inner ear called the vestibular system, which w... [en / ninguno] | What controls our balance? [en / ninguno] |
| 634 | How does a key open a lock? Please respond to the above in E... | A key opens a lock by matching the shape of the internal components inside the lock. Most locks have a series ... [en / ninguno] | How does a key open a lock? [en / ninguno] |
| 635 | Author of Rebecca? Please respond to the above in English. | The author of *Rebecca* is Daphne du Maurier. [en / ninguno] | Author of *Rebecca*? The author of *Rebecca* is Daphne du Maurier. [en / ninguno] |
| 636 | My kid asks: biggest penguin species? Please respond to the ... | The biggest penguin species is the **Emperor penguin**. They can grow up to 12 feet (about 3.6 meters) tall wh... [en / ninguno] | The largest penguin species is the emperor penguin. [en / ninguno] |
| 637 | Who discovered penicillin? Please respond to the above in En... | Penicillin was discovered by Alexander Fleming in 1929. [en / ninguno] | Penicillin was discovered by Alexander Fleming in 1929. [en / ninguno] |
| 638 | Which artist painted Campbell's Soup Cans? Please respond to... | The artist who painted Campbell's Soup Cans is Andy Warhol. [en / ninguno] | The painting "Campbell's Soup Cans" was created by Andy Warhol. [en / ninguno] |
| 639 | Point out the largest internal organ. Please respond to the ... | The largest internal organ in the human body is the skin. However, if we are considering internal organs (excl... [en / ninguno] | The largest internal organ in the human body is the liver. [en / ninguno] |
| 640 | Decode where tears come from. Please respond to the above in... | Tears come from the lacrimal glands, which are located above the eyes. These glands produce a watery fluid tha... [en / ninguno] | Decode where tears come from. [en / ninguno] |
| 641 | How does a magnifying glass burn paper? Please respond to th... | A magnifying glass does not burn paper on its own. However, under specific conditions, it can concentrate sunl... [en / ninguno] | A magnifying glass burns paper because it focuses sunlight into a small, intense point of heat. When the conce... [en / ninguno] |
| 642 | Capital of Gambia? Please respond to the above in English. | The capital of The Gambia is Banjul. [en / ninguno] | The capital of Guinea is Conakry. [en / ninguno] |
| 643 | Quick question: which ocean holds the Bermuda Triangle? Plea... | The Bermuda Triangle is located in the Atlantic Ocean. [en / ninguno] | Quick question: Which ocean does the Bermuda Triangle lie in?   / The Bermuda Triangle lies in the Atlantic Oc... [en / ninguno] |
| 644 | What is the chemical symbol for mercury? Please respond to t... | The chemical symbol for mercury is Hg. [en / ninguno] | The chemical symbol for mercury is Hg. [en / ninguno] |
| 645 | Which architect designed the Guggenheim Bilbao? Please respo... | The Guggenheim Bilbao was designed by the Spanish architect Frank Gehry. [en / es] | The Guggenheim Bilbao was designed by the architect Frank Gehry. [en / ninguno] |
| 646 | Remind me who designed the Statue of Liberty. Please respond... | The Statue of Liberty was designed by French sculptor Frédéric Auguste Bartholdi. [en / fr] | The Statue of Liberty was designed by French sculptor Frédéric Auguste Bartholdi. [en / fr] |
| 647 | Unravel how anesthesia stops pain. Please respond to the abo... | Anesthesia stops pain by interfering with the transmission of pain signals from the body to the brain. Here's ... [en / ninguno] | Explain how anesthesia stops pain. [en / ninguno] |
| 648 | How does a microwave heat food? Please respond to the above ... | A microwave heats food using microwave radiation, a type of electromagnetic wave. Inside the microwave oven, a... [en / ninguno] | A microwave heats food by using microwave radiation, which is a type of electromagnetic wave. This radiation i... [en / ninguno] |
| 649 | Symbol for gallium? Please respond to the above in English. | The symbol for gallium is Ga. [en / ninguno] | Symbol for gallium? [da / ninguno] |
| 650 | Hey, which country is Bali in? Please respond to the above i... | Bali is in Indonesia. [en / ninguno] | Bali is an Indonesian island. [en / ninguno] |
| 651 | In what year did India gain independence from Britain? Pleas... | India gained independence from Britain in 1947. [en / ninguno] | India gained independence from Britain in 1947. [en / ninguno] |
| 652 | Which empire did Montezuma rule? Please respond to the above... | Montezuma II ruled the Aztec Empire, also known as the Mexica Empire, in the 16th century. [en / ninguno] | Montezuma ruled the Aztec Empire. [en / ninguno] |
| 653 | Let me know the capital of Malta. Please respond to the abov... | The capital of Malta is Valletta. [en / ninguno] | The capital of Malta is Valletta. [en / ninguno] |
| 654 | Fill me in on how glasses fix vision. Please respond to the ... | Glasses fix vision by correcting the way light enters the eye and focuses on the retina, the light-sensitive l... [en / ninguno] | Sure! Here's an explanation in English: /  / Eyeglasses correct vision by using lenses that bend (refract) lig... [en / en] |
| 655 | How do airbags inflate so fast? Please respond to the above ... | Airbags inflate extremely quickly—typically in less than 10 milliseconds—using a chemical reaction triggered b... [en / ninguno] | How do airbags inflate so quickly? [en / ninguno] |
| 656 | Capital of Chad? Please respond to the above in English. | The capital of Chad is N'Djamena. [en / ninguno] | The capital of Chad is N'Djamena. [en / ninguno] |
| 657 | Just curious, which country is Transylvania in? Please respo... | Transylvania is a historical region in central-eastern Europe, located in present-day **Romania**. [en / ninguno] | Just curious, which country is Transylvania in? [en / ninguno] |
| 658 | Who composed The Magic Flute? Please respond to the above in... | The Magic Flute was composed by Wolfgang Amadeus Mozart. [en / ninguno] | The Magic Flute was composed by Wolfgang Amadeus Mozart. [en / ninguno] |
| 659 | Which capital had a wall until 1989? Please respond to the a... | The capital that had a wall until 1989 was Beijing, China. However, it's important to clarify: Beijing did not... [en / ninguno] | Which capital had a wall until 1989?   / The capital that had a wall until 1989 was Beijing, China. However, t... [en / ninguno] |
| 660 | Spot the lightest chemical element. Please respond to the ab... | The lightest chemical element is hydrogen. [en / ninguno] | The lightest chemical element is hydrogen. [en / ninguno] |
| 661 | Interpret how hearing aids help. Please respond to the above... | Hearing aids help individuals with hearing loss by amplifying sounds, making it easier to hear and understand ... [en / ninguno] | How hearing aids help. [en / ninguno] |
| 662 | How are diamonds formed? Please respond to the above in Engl... | Diamonds are formed deep within the Earth's mantle, at depths of about 150 to 200 kilometers (90 to 120 miles)... [en / ninguno] | How are diamonds formed? [en / ninguno] |
| 663 | Currency of Switzerland? Please respond to the above in Engl... | The currency of Switzerland is the Swiss Franc. [en / ninguno] | Currency of Switzerland? [en / ninguno] |
| 664 | Random thought: which country makes Lego? Please respond to ... | Lego is made in Denmark. The company Lego A/S was founded in 1932 in Billund, Denmark, and it remains a Danish... [en / ninguno] | Random thought: Which country makes Lego? [en / ninguno] |
| 665 | What is the tallest waterfall in the world? Please respond t... | The tallest waterfall in the world is Angel Falls (Salto Ángel) in Venezuela. It has a total height of 807 met... [en / ninguno] | The tallest waterfall in the world is Angel Falls (Salto Ángel) in Venezuela. It has a total height of 809 met... [en / ninguno] |
| 666 | Which canal links the Atlantic and Pacific? Please respond t... | There is no canal that directly links the Atlantic and Pacific Oceans. The closest major waterway is the Panam... [en / ninguno] | The canal that links the Atlantic and Pacific oceans is the Panama Canal. [en / ninguno] |
| 667 | Fetch the capital of Albania. Please respond to the above in... | The capital of Albania is Tirana. [en / ninguno] | The capital of Albania is Tirana. [en / ninguno] |
| 668 | Expand on how elevators work. Please respond to the above in... | Elevators are mechanical devices designed to transport people or goods vertically between different floors in ... [en / ninguno] | Elevators work by using a combination of mechanical components and electrical systems to move people or goods ... [en / ninguno] |
| 669 | What gives rubies their red color? Please respond to the abo... | Rubies get their red color from the presence of chromium ions (Cr³⁺) within the crystal structure of the gemst... [en / ninguno] | What gives rubies their red color? [en / ninguno] |
| 670 | Currency of India? Please respond to the above in English. | The currency of India is the Indian Rupee (INR). [en / ninguno] | Currency of India? [en / ninguno] |
| 671 | Trivia time: which country has the most lakes? Please respon... | Canada has the most lakes in the world. It is home to over 30,000 lakes larger than 100 square meters, with th... [en / ninguno] | Trivia: Which country has the most lakes? [en / ninguno] |
| 672 | What is the largest organ of the human body? Please respond ... | The largest organ of the human body is the skin. It covers the entire body and serves as a protective barrier ... [en / ninguno] | The largest organ of the human body is the skin. [en / ninguno] |
| 673 | Which sea separates Europe from Africa? Please respond to th... | The sea that separates Europe from Africa is the Mediterranean Sea. [en / ninguno] | The sea that separates Europe from Africa is the Mediterranean Sea. [en / ninguno] |
| 674 | Disclose the capital of Brunei. Please respond to the above ... | The capital of Brunei is Bandar Seri Begawan. [en / ninguno] | The capital of Brunei is Bandar Seri Begawan. [en / ninguno] |
| 675 | Examine how noise-cancelling headphones work. Please respond... | Noise-cancelling headphones work by using a technology called active noise cancellation (ANC) to reduce unwant... [en / ninguno] | Noise-cancelling headphones work by using a technology called active noise cancellation (ANC). Here's how it w... [en / ninguno] |
| 676 | How do glow sticks glow? Please respond to the above in Engl... | Glow sticks glow due to a chemical reaction called **chemiluminescence**. Inside a glow stick, there are two m... [en / ninguno] | How do glow sticks glow?   / Glow sticks glow due to a chemical reaction called chemiluminescence. Inside a gl... [en / ninguno] |
| 677 | Currency of Mexico? Please respond to the above in English. | The currency of Mexico is the Mexican peso. [en / ninguno] | Currency of Mexico? [en / ninguno] |
| 678 | I forgot, which river flows through Rome? Please respond to ... | The Tiber River flows through Rome. [en / ninguno] | I forgot, which river flows through Rome? The Tiber River flows through Rome. [en / ninguno] |
| 679 | In what year did the Spanish Armada sail against England? Pl... | The Spanish Armada sailed against England in the year 1588. [en / es] | The Spanish Armada sailed against England in the year 1588. [en / es] |
| 680 | Lake Bled is in which country? Please respond to the above i... | Lake Bled is in Slovenia. [en / ninguno] | Lake Bled is in Slovenia. [en / ninguno] |
| 681 | Guess the capital of Cyprus. Please respond to the above in ... | The capital of Cyprus is Nicosia. [en / ninguno] | The capital of Cyprus is Nicosia. [en / ninguno] |
| 682 | Analyze how touchscreens sense fingers. Please respond to th... | Touchscreens sense fingers through various technologies, the most common of which are capacitive, resistive, a... [en / ninguno] | Analyze how finger-sensitive screens work. [en / ninguno] |
| 683 | How do clouds stay up? Please respond to the above in Englis... | Clouds stay up because they are made of tiny water droplets or ice crystals that are suspended in the air by t... [en / ninguno] | How do clouds stay up? Clouds stay up because the water droplets or ice crystals in them are so small that the... [en / ninguno] |
| 684 | Currency of Russia? Please respond to the above in English. | The currency of Russia is the Russian ruble. [en / ninguno] | Currency of Russia? [en / ninguno] |
| 685 | Out of curiosity, which river runs through Florence? Please ... | The Arno River runs through Florence, Italy. [en / ninguno] | Out of curiosity, which river runs through Florence? [en / ninguno] |
| 686 | In what year did Apollo 11 land on the Moon? Please respond ... | Apollo 11 landed on the Moon in 1969. [en / ninguno] | Apollo 11 landed on the Moon in 1969. [en / ninguno] |
| 687 | Which country invented paper? Please respond to the above in... | China invented paper around 105 AD during the Han Dynasty. The invention is traditionally attributed to Cai Lu... [en / ninguno] | China invented paper. [en / ninguno] |
| 688 | Choose the animal on Lamborghini's logo. Please respond to t... | Lamborghini's logo does not feature an animal. It features a stylized, roaring lion, which is a symbol of powe... [en / ninguno] | The animal on Lamborghini's logo is a **lion**. [en / ninguno] |
| 689 | Review how dolphins sleep. Please respond to the above in En... | Dolphins have a unique and fascinating way of sleeping that differs significantly from humans and many other m... [en / ninguno] | Dolphins sleep in a unique way that allows them to remain partially awake and alert, as they need to keep one ... [en / ninguno] |
| 690 | How does a sponge absorb water? Please respond to the above ... | A sponge absorbs water through a process called capillary action and the presence of tiny pores. The material ... [en / ninguno] | A sponge absorbs water through a process called capillary action. The tiny pores in the sponge are made of por... [en / ninguno] |
| 691 | Sport at Wimbledon? Please respond to the above in English. | Yes, sport at Wimbledon refers to the prestigious tennis tournament held annually at the All England Lawn Tenn... [en / ninguno] | Sport at Wimbledon? [en / ninguno] |
| 692 | Hmm, which sea is Venice on? Please respond to the above in ... | Venice is located on the Adriatic Sea. [en / ninguno] | Hmm, which sea is Venice on? [en / ninguno] |
| 693 | What is the capital of Indonesia? Please respond to the abov... | The capital of Indonesia is Jakarta. [en / ninguno] | The capital of Indonesia is Jakarta. [en / ninguno] |
| 694 | Which planet is farthest from the Sun? Please respond to the... | The planet farthest from the Sun is Neptune. [en / ninguno] | The planet farthest from the Sun is Neptune. [en / ninguno] |
| 695 | Retrieve the author of Alice in Wonderland. Please respond t... | The author of *Alice's Adventures in Wonderland* is Lewis Carroll. [en / ninguno] | The author of *Alice's Adventures in Wonderland* is Lewis Carroll. [en / ninguno] |
| 696 | Clear up how camels survive deserts. Please respond to the a... | Camels are exceptionally well-adapted to survive in desert environments through a combination of physiological... [en / ninguno] | Camels survive deserts through several key adaptations: /  / 1. **Water Conservation**: Camels can go for long... [en / ninguno] |
| 697 | How do hedgehogs defend themselves? Please respond to the ab... | Hedgehogs defend themselves primarily by rolling into a tight ball, exposing their spines. These spines are ma... [en / ninguno] | Hedgehogs defend themselves by rolling into a tight ball, exposing only their spines. Their spines are sharp a... [en / ninguno] |
| 698 | Tour de France sport? Please respond to the above in English... | Yes, the Tour de France is a prestigious annual multiple-stage bicycle race primarily held in France. It is on... [en / ninguno] | Tour de France sport? [en / ninguno] |
| 699 | Okay, which island was Napoleon born on? Please respond to t... | Napoleon was born on the island of Corsica. [en / ninguno] | Napoleon was born on the island of Corsica. [en / ninguno] |

