# Parche de idioma: signo e idioma de entrada (preset `restar_fr`)

- Parche: `/mnt/custom-file-systems/efs/fs-0ded2930a619aa967_fsap-0faa05c681ed1a8f3/papers/LLMAtaquesContinuos/experimentos/idiomas/runs/v6_goalall_head_mono_s1/lang_patch_best_train.pt`  |  norma 0.6692
- Tail del held-out: n=50

| condicion | n | fr | en | es | de | it | pt | unk | is_french | starts_fr | acc | cambio vs a=0 | largo | CE fr head | CE en head | tok parche |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| prompt_fr a=0 | 50 | 0.90 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.10 | 0.90 | 0.80 | 0.92 | nan | 79.0 | 0.780 | 2.788 | 0.0 |
| prompt_fr a=-1 | 50 | 0.84 | 0.16 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.84 | 0.70 | 0.88 | 0.88 | 245.2 | 1.473 | 3.652 | 13.8 |

`tok parche` es la media de posiciones que reciben el parche (con anchor goal_all, el largo de la pregunta: la perturbacion total es ese numero por v). `cambio` es la fraccion de filas cuya salida difiere de la de a=0 en la misma columna. La accuracy en salidas en espanol o aleman puede estar subestimada: los alias son ingles y frances.

## Salidas: `prompt_fr`

| # | pregunta usada | a=0 [lang] | a=-1 [lang] |
|---|---|---|---|
| 200 | Quelle est la capitale de l'Ukraine ? | Kyiv est la capitale de l'Ukraine. [fr] | La capitale de l'Ukraine est Kiev (ou Kyïv en ukrainien). [fr] |
| 201 | Quelle force maintient les planètes dans leur orbite autour ... | La force qui maintient les planètes dans leur orbite autour du Soleil est appelée force centrale. [fr] | Une question très astrophysique! /  / Les planètes sont maintenues dans leur orbite autour du Soleil par une f... [fr] |
| 202 | Qui a ecrit La Mer et le Vieil Homme? | Une question sur la littérature! /  / "La Mer et le Vieil Homme" (en anglais : "The Sea and the Old Man") est ... [fr] | "La Mer et le Vieil Homme" (The Sea and the Old Man) is a famous poem by the French poet Paul Verlaine. [en] |
| 203 | Quelle est la capitale de la Syrie ? | La capitale de la Syrie est Damas. [fr] | La capitale de la Syrie est Damas. [fr] |
| 204 | Quelle est l'année du premier vol des frères Wright ? | L'année du premier vol des frères Wright est 1903. [fr] | Une question sur l'histoire de l'aviation! /  / Le premier vol des frères Wright a eu lieu le 17 décembre 1903... [fr] |
| 205 | Quelle est l'année où le projet Génome humain a publié sa pr... | Le projet Génome humain a publié sa première version en 2003 [fr] | Une question intéressante! /  / Le projet génome humain a été publié en 2003. C'est une année très spéciale da... [fr] |
| 206 | Quel est le symbole chimique du platine ? | Le symbole chimique du platine est Pt. [fr] | Désolé, mais je ne peux pas fournir de réponse précise sur le symbole chimique du platine sans plus de context... [fr] |
| 207 | Quelle est l'année de la réunification de l'Allemagne ? | L'année de la réunification de l'Allemagne est 1990 [fr] | L'année de la réunification de l'Allemagne est 1990. [fr] |
| 208 | Qui a développé la théorie de la sélection naturelle aux côt... | La théorie de la sélection naturelle a été développée par Charles Darwin aux côtés de Gregor Mendel. [fr] | La théorie de la sélection naturelle aux côtés de Darwin a été développée par Charles Robert Darwin (1809-1882... [fr] |
| 209 | Quel est l'année dans laquelle l'Union soviétique a dissous? | L'Union soviétique a été officiellement dissoute en 1991. [fr] | Je suis désolé, mais je ne comprends pas parfaitement votre question. Pouvez-vous me donner plus de détails ou... [fr] |
| 210 | Qui a développé la théorie de la relativité générale ? | Albert Einstein [unknown] | Une question sur la physique! /  / La théorie de la relativité générale a été développée par Albert Einstein. ... [fr] |
| 211 | Qui a peint Le Cri? | "Le Cri" est une peinture du peintre français Edvard Munch, créée en 1893. Elle est considérée comme l'une des... [fr] | I think you meant to ask "Who painted Le Cri?" /  / Le Cri is a painting by French artist Paul Cézanne, create... [en] |
| 212 | Quelle est la capitale de la Grèce ? | Athènes [unknown] | La capitale de la Grèce est Athènes (en grec, Αθήνα). [fr] |
| 213 | Qui a écrit Cent ans de solitude ? | Une question sur la littérature! /  / "Cent ans de solitude" est un roman écrit par Gabriel García Márquez, un... [fr] | "Cent ans de solitude" (also translated as "One Hundred Years of Solitude") is a novel written by the Colombia... [en] |
| 214 | Quel est le plus grand océan de la Terre? | L'océan Pacifique est le plus grand océan de la Terre. [fr] | Bonjour! /  / Le plus grand océan de la Terre est l'Océan Pacifique. Il couvre environ 155,6 millions de kilom... [fr] |
| 215 | Quelle est l'année où a commencé la Seconde Guerre mondiale ... | La Seconde Guerre mondiale a commencé en 1939. [fr] | La Seconde Guerre mondiale a commencé en 1939. [fr] |
| 216 | Quel est le planète le plus petit du système solaire? | La planète la plus petite du système solaire est Mercure. [fr] | Une question intéressante! /  / Selon les données astronomiques actuelles, la planète la plus petite du systèm... [fr] |
| 217 | Qui a écrit Hamlet ? | Un excellent sujet! /  / Le texte de Hamlet a été écrit par le grand dramaturge et poète William Shakespeare (... [fr] | A classic question! /  / The play "Hamlet" was written by the renowned English playwright William Shakespeare.... [en] |
| 218 | Quelle est la galaxie la plus proche voisine de la Voie lact... | La galaxie la plus proche de la Voie lactée est la galaxie Andromède (M31). [fr] | La galaxie la plus proche de la Voie lactée est la galaxie Andromède (M31), également connue sous le nom de ga... [fr] |
| 219 | Quel est le nombre de lunes que Mars possède? | Mars possède deux lunes. [fr] | Une question sur la planète rouge! /  / Mars, comme la Terre, a une orbite elliptique autour du Soleil. Cela s... [fr] |
| 220 | Quel est le symbole chimique du chrome ? | Le symbole chimique du chrome est Cr. [fr] | Désolé, mais je n'ai pas compris votre question. Pouvez-vous répéter ou préciser ce que vous cherchez à savoir... [fr] |
| 221 | Qui a ecrit la Prude et la Préjugée? | La Prude et la Préjugée est un roman écrit par Jane Austen. [fr] | Une question sur la littérature! /  / Je pense que vous faites référence à "La Prude" et "La Préjugée" de Gust... [fr] |
| 222 | Qui a obtenu le brevet de 1876 pour le téléphone? | Alexander Graham Bell [unknown] | I think you meant to ask "Qui a inventé le téléphone en 1876?" /  / The answer is Alexander Graham Bell, un in... [fr] |
| 223 | Quel est le symbole chimique du zinc? | Le symbole chimique du zinc est Zn. [fr] | Le symbole chimique du zinc est Zn. /  / C'est un métal blanc argenté, abondant dans la nature, et il est util... [fr] |
| 224 | Qui a ecrit Le Petit Prince? | Un classique! /  / Le Petit Prince (original titre en français : Le Petit Prince) a été écrit par Antoine de S... [fr] | A classic French novel! /  / "Le Petit Prince" (The Little Prince) is a novella written by Antoine de Saint-Ex... [en] |
| 225 | Qui a composé la Symphonie n° 9 contenant l'Ode à la joie ? | La Symphonie n° 9 contenant l'Ode à la joie a été composée par Ludwig van Beethoven. [fr] | Une question musicale! /  / La Symphonie n° 9 en la mineur, également connue sous le nom de "Symphonie chorale... [fr] |
| 226 | Quel est le nombre de zones horaires que le monde a, en comp... | Le monde compte 24 zones horaires en comptage standard. [fr] | Bonjour! /  / Le monde est divisé en 24 zones horaires, qui sont définies par la longitude de la mer du Nord. ... [fr] |
| 227 | Quelle est la capitale du Qatar? | La capitale du Qatar est Doha. [fr] | La capitale du Qatar est Doha. [fr] |
| 228 | Quelle est la capitale de la République tchèque? | La capitale de la République tchèque est Prague. [fr] | La capitale de la République tchèque est Prague (en tchèque : Praha). [fr] |
| 229 | Quelle est la capitale de la Bulgarie ? | Sofia est la capitale de la Bulgarie. [fr] | La capitale de la Bulgarie est Sofia (en bulgare : София, Sofiya). [fr] |
| 230 | Combien de touches a un piano standard ? | Un piano standard possède généralement 88 touches, réparties de la manière suivante : /  / * 52 touches de la ... [fr] | A piano standard typically has 88 keys, which are divided into: /  / * 52 white keys (called naturals) / * 36 ... [en] |
| 231 | Quel est le nombre d'os dans le corps humain adulte? | Il y a 206 os dans le corps humain adulte. [fr] | Une question simple mais intéressante! /  / Le nombre d'os dans le corps humain adulte est de 206. /  / Voici ... [fr] |
| 232 | Quel est le point de congélation de l'eau en degrés Celsius ... | Le point de congélation de l'eau est de 0 degrés Celsius. [fr] | Le point de congélation de l'eau est de 0 degrés Celsius (ou 32 degrés Fahrenheit). [fr] |
| 233 | Quelle est la formule chimique du dioxyde de carbone? | La formule chimique du dioxyde de carbone est CO2. [fr] | La formule chimique du dioxyde de carbone est CO₂. [fr] |
| 234 | Quel océan se trouve entre l'Afrique et l'Australie ? | L'océan Indien se trouve entre l'Afrique et l'Australie. [fr] | L'océan situé entre l'Afrique et l'Australie est l'Océan Indien. [fr] |
| 235 | Quelle est la capitale de la Chine? | La capitale de la Chine est Pékin. [fr] | La capitale de la Chine est Pékin (ou Beijin en mandarin). [fr] |
| 236 | Dans quelle ville se trouve le Taj Mahal ? | Le Taj Mahal se trouve à Agra, en Inde. [fr] | I think you meant to ask "In which city is the Taj Mahal located?" /  / The Taj Mahal is located in Agra, Indi... [en] |
| 237 | Quelle est l'année où l'euro a été introduit comme monnaie p... | L'euro a été introduit comme monnaie physique le 1er janvier 2002. [fr] | L'euro a été introduit comme monnaie physique en 2002. C'est le 1er janvier 2002 que l'euro a été mis en circu... [fr] |
| 238 | Qui a composé l'opéra Carmen ? | Georges Bizet [unknown] | Une question classique! /  / L'opéra Carmen a été composée par Georges Bizet. Il a écrit la musique de l'opéra... [fr] |
| 239 | Quelle est la capitale du Liban? | La capitale du Liban est Beyrouth. [fr] | La capitale du Liban est Beyrouth. [fr] |
| 240 | Comment s'appelle la fosse océanique la plus profonde ? | La fosse océanique la plus profonde s'appelle la Fosse de Tonga. [fr] | Désolé, mais je ne parle pas français. Cependant, je peux essayer de vous aider en anglais. /  / The deepest p... [en] |
| 241 | Quelle est l'année de la catastrophe du Hindenburg ? | L'année de la catastrophe du Hindenburg est 1937. [fr] | Une question sur l'histoire! /  / La catastrophe du Hindenburg a eu lieu le 6 mai 1937. Le zeppelin allemand H... [fr] |
| 242 | Quel est le symbole chimique du chlore? | Le symbole chimique du chlore est Cl. [fr] | Désolé, mais je ne parle pas français avec une grande précision. Cependant, je vais essayer de vous aider. /  ... [fr] |
| 243 | Quelle est la capitale de la Finlande ? | La capitale de la Finlande est Helsinki. [fr] | La capitale de la Finlande est Helsinki. [fr] |
| 244 | Quel est le nombre de chambres que le cœur humain possède? | Le cœur humain possède quatre chambres. [fr] | Une question intéressante! /  / Selon les connaissances scientifiques actuelles, le cœur humain possède enviro... [fr] |
| 245 | Qui était la première femme à remporter un prix Nobel? | Marie Curie [unknown] | Je suis désolé, mais je n'ai pas trouvé d'informations sur une femme qui a remporté le prix Nobel en tant que ... [fr] |
| 246 | Quelle est la capitale de la Lituanie ? | Vilnius est la capitale de la Lituanie. [fr] | La capitale de la Lituanie est Vilna (ou Vilnius en français). [fr] |
| 247 | Quelle est la capitale de la Jordanie ? | La capitale de la Jordanie est Amman. [fr] | La capitale de la Jordanie est Amman. [fr] |
| 248 | Quelle est l'année où le canal de Panama a été ouvert ? | Le canal de Panama a été ouvert en 1914. [fr] | Bonjour! /  / Le canal de Panama a été ouvert en 1914. Il relie le canal de Panama à Panama, en République de ... [fr] |
| 249 | Quelle est la plus grande île du monde? | La plus grande île du monde est l'île de Groenland, qui fait partie du Groenland, un territoire autonome de la... [fr] | La plus grande île du monde est l'île de Groenland, qui fait partie du Groenland, un territoire autonome de la... [fr] |

