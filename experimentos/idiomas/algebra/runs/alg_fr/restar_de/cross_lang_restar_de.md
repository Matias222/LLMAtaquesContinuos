# Parche de idioma: signo e idioma de entrada (preset `restar_de`)

- Parche: `/mnt/custom-file-systems/efs/fs-0ded2930a619aa967_fsap-0faa05c681ed1a8f3/papers/LLMAtaquesContinuos/experimentos/idiomas/algebra/runs/alg_de/lang_patch_best_train.pt`  |  norma 0.8491
- Tail del held-out: n=50

| condicion | n | fr | en | es | de | it | pt | unk | is_french | starts_fr | acc | cambio vs a=0 | largo | CE fr head | CE en head | tok parche |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| prompt_fr a=0 | 50 | 0.90 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.10 | 0.90 | 0.80 | 0.92 | nan | 79.0 | 0.780 | 2.788 | 0.0 |
| prompt_fr a=-1 | 50 | 0.96 | 0.04 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.96 | 0.94 | 0.76 | 0.88 | 244.7 | 1.603 | 4.497 | 13.8 |

`tok parche` es la media de posiciones que reciben el parche (con anchor goal_all, el largo de la pregunta: la perturbacion total es ese numero por v). `cambio` es la fraccion de filas cuya salida difiere de la de a=0 en la misma columna. La accuracy en salidas en espanol o aleman puede estar subestimada: los alias son ingles y frances.

## Salidas: `prompt_fr`

| # | pregunta usada | a=0 [lang] | a=-1 [lang] |
|---|---|---|---|
| 200 | Quelle est la capitale de l'Ukraine ? | Kyiv est la capitale de l'Ukraine. [fr] | La capitale de l'Ukraine est Kiev (ou Kyiv en ukrainien). [fr] |
| 201 | Quelle force maintient les planètes dans leur orbite autour ... | La force qui maintient les planètes dans leur orbite autour du Soleil est appelée force centrale. [fr] | Une question de physique! /  / Les planètes maintiennent leur orbite autour du Soleil grâce à une force appelé... [fr] |
| 202 | Qui a ecrit La Mer et le Vieil Homme? | Une question sur la littérature! /  / "La Mer et le Vieil Homme" (en anglais : "The Sea and the Old Man") est ... [fr] | Je m'excuse, mais je n'ai pas compris votre question. Pouvez-vous répéter ou préciser ce que vous cherchez à s... [fr] |
| 203 | Quelle est la capitale de la Syrie ? | La capitale de la Syrie est Damas. [fr] | La capitale de la Syrie est Damas. [fr] |
| 204 | Quelle est l'année du premier vol des frères Wright ? | L'année du premier vol des frères Wright est 1903. [fr] | Une question sur l'histoire de l'aviation! /  / L'année du premier vol des frères Wright est 1903. Le 17 décem... [fr] |
| 205 | Quelle est l'année où le projet Génome humain a publié sa pr... | Le projet Génome humain a publié sa première version en 2003 [fr] | Une question intéressante! /  / Le projet Génome humain, également connu sous le nom de projet Human Genome Pr... [fr] |
| 206 | Quel est le symbole chimique du platine ? | Le symbole chimique du platine est Pt. [fr] | Je ne suis pas sûr de comprendre votre question. Pourriez-vous me donner plus de contexte ou clarifier ce que ... [fr] |
| 207 | Quelle est l'année de la réunification de l'Allemagne ? | L'année de la réunification de l'Allemagne est 1990 [fr] | L'année de la réunification de l'Allemagne est 1990. [fr] |
| 208 | Qui a développé la théorie de la sélection naturelle aux côt... | La théorie de la sélection naturelle a été développée par Charles Darwin aux côtés de Gregor Mendel. [fr] | Une question sur la biologie! /  / La théorie de la sélection naturelle aux côtés de Charles Darwin est présen... [fr] |
| 209 | Quel est l'année dans laquelle l'Union soviétique a dissous? | L'Union soviétique a été officiellement dissoute en 1991. [fr] | Une question sur l'histoire! /  / L'Union soviétique a dissous en 1991. Plus précisément, le 26 décembre 1991,... [fr] |
| 210 | Qui a développé la théorie de la relativité générale ? | Albert Einstein [unknown] | Une question complexe! /  / La théorie de la relativité générale, développée par Albert Einstein, est une théo... [fr] |
| 211 | Qui a peint Le Cri? | "Le Cri" est une peinture du peintre français Edvard Munch, créée en 1893. Elle est considérée comme l'une des... [fr] | I think you meant to ask "Qui a peint Le Cri?" /  / Le Cri is a famous painting by French artist Paul Cézanne,... [en] |
| 212 | Quelle est la capitale de la Grèce ? | Athènes [unknown] | La capitale de la Grèce est Athènes (en grec, Αθήνα). [fr] |
| 213 | Qui a écrit Cent ans de solitude ? | Une question sur la littérature! /  / "Cent ans de solitude" est un roman écrit par Gabriel García Márquez, un... [fr] | Je suis désolé, mais je n'ai pas trouvé d'information sur un livre intitulé "Cent ans de solitude" écrit par q... [fr] |
| 214 | Quel est le plus grand océan de la Terre? | L'océan Pacifique est le plus grand océan de la Terre. [fr] | Une question géographique! /  / Selon les données disponibles, le plus grand océan de la Terre est l'Océan Pac... [fr] |
| 215 | Quelle est l'année où a commencé la Seconde Guerre mondiale ... | La Seconde Guerre mondiale a commencé en 1939. [fr] | L'année où a commencé la Seconde Guerre mondiale est 1939. [fr] |
| 216 | Quel est le planète le plus petit du système solaire? | La planète la plus petite du système solaire est Mercure. [fr] | Le planète le plus petit du système solaire est Mercure.  /  / Mercure est une planète rocheuse qui fait parti... [fr] |
| 217 | Qui a écrit Hamlet ? | Un excellent sujet! /  / Le texte de Hamlet a été écrit par le grand dramaturge et poète William Shakespeare (... [fr] | A question about literature! /  / Hamlet was written by William Shakespeare, an English playwright and poet, a... [en] |
| 218 | Quelle est la galaxie la plus proche voisine de la Voie lact... | La galaxie la plus proche de la Voie lactée est la galaxie Andromède (M31). [fr] | Une question intéressante! /  / La Voie lactée est notre galaxie natale, qui contient environ 200 à 400 millia... [fr] |
| 219 | Quel est le nombre de lunes que Mars possède? | Mars possède deux lunes. [fr] | Je ne connais pas d'informations précises sur un personnage nommé "Quel" qui possèderait la Lune. Cependant, j... [fr] |
| 220 | Quel est le symbole chimique du chrome ? | Le symbole chimique du chrome est Cr. [fr] | Une question intéressante! /  / Le symbole chimique du chrome est Cr. /  / "Cr" vient du latin "chromium", qui... [fr] |
| 221 | Qui a ecrit la Prude et la Préjugée? | La Prude et la Préjugée est un roman écrit par Jane Austen. [fr] | Je peux vous aider avec vos questions sur la géographie! /  / Il semble que vous cherchiez à connaître la diff... [fr] |
| 222 | Qui a obtenu le brevet de 1876 pour le téléphone? | Alexander Graham Bell [unknown] | Je suis désolé, mais je n'ai pas trouvé d'information sur quelqu'un qui a obtenu un brevet pour un téléphone e... [fr] |
| 223 | Quel est le symbole chimique du zinc? | Le symbole chimique du zinc est Zn. [fr] | Une question intéressante! /  / Le symbole chimique du zinc est Zn. /  / C'est un élément chimique de numéro a... [fr] |
| 224 | Qui a ecrit Le Petit Prince? | Un classique! /  / Le Petit Prince (original titre en français : Le Petit Prince) a été écrit par Antoine de S... [fr] | Le Petit Prince est un livre écrit et illustré par Antoine de Saint-Exupéry, publié en 1943. /  / Le Petit Pri... [fr] |
| 225 | Qui a composé la Symphonie n° 9 contenant l'Ode à la joie ? | La Symphonie n° 9 contenant l'Ode à la joie a été composée par Ludwig van Beethoven. [fr] | Je pense que vous cherchez à composer une phrase en français, mais il y a quelques erreurs d'orthographe et de... [fr] |
| 226 | Quel est le nombre de zones horaires que le monde a, en comp... | Le monde compte 24 zones horaires en comptage standard. [fr] | Je vais essayer de vous aider! /  / Selon les données de l'Organisation météorologique mondiale (OMM), il exis... [fr] |
| 227 | Quelle est la capitale du Qatar? | La capitale du Qatar est Doha. [fr] | La capitale du Qatar est Doha. [fr] |
| 228 | Quelle est la capitale de la République tchèque? | La capitale de la République tchèque est Prague. [fr] | La capitale de la République tchèque est Prague (en tchèque : Praha). [fr] |
| 229 | Quelle est la capitale de la Bulgarie ? | Sofia est la capitale de la Bulgarie. [fr] | La capitale de la Bulgarie est Sofia (en bulgare : София, Sofiya). [fr] |
| 230 | Combien de touches a un piano standard ? | Un piano standard possède généralement 88 touches, réparties de la manière suivante : /  / * 52 touches de la ... [fr] | Un piano standard a 88 touches, répartis de la note la plus basse (Do1) à la note la plus haute (La8). C'est l... [fr] |
| 231 | Quel est le nombre d'os dans le corps humain adulte? | Il y a 206 os dans le corps humain adulte. [fr] | Un bon question! /  / Le nom que vous cherchez est probablement "os du mâle" ou "os du féminin", mais je vais ... [fr] |
| 232 | Quel est le point de congélation de l'eau en degrés Celsius ... | Le point de congélation de l'eau est de 0 degrés Celsius. [fr] | Un peu de physique! /  / Le point de congélation de l'eau en degrés Celsius est de 0°C. C'est-à-dire que lorsq... [fr] |
| 233 | Quelle est la formule chimique du dioxyde de carbone? | La formule chimique du dioxyde de carbone est CO2. [fr] | La formule chimique du dioxyde de carbone est : /  / CO₂ /  / C'est une molécule composée d'un atome de carbon... [fr] |
| 234 | Quel océan se trouve entre l'Afrique et l'Australie ? | L'océan Indien se trouve entre l'Afrique et l'Australie. [fr] | Je pense que vous cherchez à savoir quel océan se trouve entre l'Afrique et l'Australie. /  / La réponse est :... [fr] |
| 235 | Quelle est la capitale de la Chine? | La capitale de la Chine est Pékin. [fr] | La capitale de la Chine est Pékin (ou Beijin en mandarin). [fr] |
| 236 | Dans quelle ville se trouve le Taj Mahal ? | Le Taj Mahal se trouve à Agra, en Inde. [fr] | Le Taj Mahal se trouve à Agra, en Inde. [fr] |
| 237 | Quelle est l'année où l'euro a été introduit comme monnaie p... | L'euro a été introduit comme monnaie physique le 1er janvier 2002. [fr] | Je peux vous fournir des informations générales, mais pour une réponse précise et à jour, je recommande de con... [fr] |
| 238 | Qui a composé l'opéra Carmen ? | Georges Bizet [unknown] | Une question musicale! /  / L'opéra "Carmen" a été composé par Georges Bizet. Il a été créé en 1875 au Théâtre... [fr] |
| 239 | Quelle est la capitale du Liban? | La capitale du Liban est Beyrouth. [fr] | La capitale du Liban est Beyrouth. [fr] |
| 240 | Comment s'appelle la fosse océanique la plus profonde ? | La fosse océanique la plus profonde s'appelle la Fosse de Tonga. [fr] | Je suis désolé, mais je ne comprends pas votre question. Pouvez-vous s'il vous plaît répéter ou préciser ce qu... [fr] |
| 241 | Quelle est l'année de la catastrophe du Hindenburg ? | L'année de la catastrophe du Hindenburg est 1937. [fr] | L'année du catastrophe du Hindenburg était 1937. Le zeppelin allemand Hindenburg a pris feu et a été détruit l... [fr] |
| 242 | Quel est le symbole chimique du chlore? | Le symbole chimique du chlore est Cl. [fr] | Une question intéressante! /  / Le symbole chimique du chlore est Cl. /  / Le chlore est un élément chimique d... [fr] |
| 243 | Quelle est la capitale de la Finlande ? | La capitale de la Finlande est Helsinki. [fr] | La capitale de la Finlande est Helsinki. [fr] |
| 244 | Quel est le nombre de chambres que le cœur humain possède? | Le cœur humain possède quatre chambres. [fr] | Je peux vous fournir des informations générales, mais pour des questions spécifiques ou des détails personnels... [fr] |
| 245 | Qui était la première femme à remporter un prix Nobel? | Marie Curie [unknown] | Marie Curie, une scientifique polonaise-française, est devenue la première femme à remporter un prix Nobel en ... [fr] |
| 246 | Quelle est la capitale de la Lituanie ? | Vilnius est la capitale de la Lituanie. [fr] | La capitale de la Lituanie est Vilnius. [fr] |
| 247 | Quelle est la capitale de la Jordanie ? | La capitale de la Jordanie est Amman. [fr] | La capitale de la Jordanie est Amman. [fr] |
| 248 | Quelle est l'année où le canal de Panama a été ouvert ? | Le canal de Panama a été ouvert en 1914. [fr] | Une question intéressante! /  / Le canal de Panama, également connu sous le nom de canal interocéanique de Pan... [fr] |
| 249 | Quelle est la plus grande île du monde? | La plus grande île du monde est l'île de Groenland, qui fait partie du Groenland, un territoire autonome de la... [fr] | Je peux vous fournir quelques informations sur les plus grands îles du monde.  /  / Voici quelques-unes des pl... [fr] |

