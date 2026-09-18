# Parche de idioma: signo e idioma de entrada (preset `restar_es`)

- Parche: `/mnt/custom-file-systems/efs/fs-0ded2930a619aa967_fsap-0faa05c681ed1a8f3/papers/LLMAtaquesContinuos/experimentos/idiomas/algebra/runs/alg_es/lang_patch_best_train.pt`  |  norma 0.8655
- Tail del held-out: n=50

| condicion | n | fr | en | es | de | it | pt | unk | is_french | starts_fr | acc | cambio vs a=0 | largo | CE fr head | CE en head | tok parche |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| prompt_fr a=0 | 50 | 0.90 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.10 | 0.90 | 0.80 | 0.92 | nan | 79.0 | 0.780 | 2.788 | 0.0 |
| prompt_fr a=-1 | 50 | 0.88 | 0.08 | 0.00 | 0.02 | 0.00 | 0.00 | 0.02 | 0.88 | 0.88 | 0.78 | 0.84 | 237.0 | 1.802 | 4.461 | 13.8 |

`tok parche` es la media de posiciones que reciben el parche (con anchor goal_all, el largo de la pregunta: la perturbacion total es ese numero por v). `cambio` es la fraccion de filas cuya salida difiere de la de a=0 en la misma columna. La accuracy en salidas en espanol o aleman puede estar subestimada: los alias son ingles y frances.

## Salidas: `prompt_fr`

| # | pregunta usada | a=0 [lang] | a=-1 [lang] |
|---|---|---|---|
| 200 | Quelle est la capitale de l'Ukraine ? | Kyiv est la capitale de l'Ukraine. [fr] | La capitale de l'Ukraine est Kiev (ou Kyïv en ukrainien). [fr] |
| 201 | Quelle force maintient les planètes dans leur orbite autour ... | La force qui maintient les planètes dans leur orbite autour du Soleil est appelée force centrale. [fr] | Une question qui touche à la physique des étoiles! /  / La force qui maintient les planètes dans leur orbite a... [fr] |
| 202 | Qui a ecrit La Mer et le Vieil Homme? | Une question sur la littérature! /  / "La Mer et le Vieil Homme" (en anglais : "The Sea and the Old Man") est ... [fr] | Une référence à la littérature! /  / "Qui a écrit La Mer et le Vieil Homme"? /  / La réponse est : Albert Camu... [fr] |
| 203 | Quelle est la capitale de la Syrie ? | La capitale de la Syrie est Damas. [fr] | La capitale de la Syrie est Damas. [fr] |
| 204 | Quelle est l'année du premier vol des frères Wright ? | L'année du premier vol des frères Wright est 1903. [fr] | Une question sur l'histoire de l'aviation! /  / L'année du premier vol des frères Wright est 1903. /  / Le 17 ... [fr] |
| 205 | Quelle est l'année où le projet Génome humain a publié sa pr... | Le projet Génome humain a publié sa première version en 2003 [fr] | Une question qui me met un peu mal à l'aise! /  / Je vais essayer de vous aider, mais je dois vous informer qu... [fr] |
| 206 | Quel est le symbole chimique du platine ? | Le symbole chimique du platine est Pt. [fr] | Une question sur la chimie! /  / Le symbole chimique du platine est Pt. /  / Le platine est un métal d'argent-... [fr] |
| 207 | Quelle est l'année de la réunification de l'Allemagne ? | L'année de la réunification de l'Allemagne est 1990 [fr] | Une question historique! /  / L'année de la réunification de l'Allemagne est 1990. /  / Après la chute du Mur ... [fr] |
| 208 | Qui a développé la théorie de la sélection naturelle aux côt... | La théorie de la sélection naturelle a été développée par Charles Darwin aux côtés de Gregor Mendel. [fr] | Une question sur l'histoire de la biologie! /  / La théorie de la sélection naturelle, également connue sous l... [fr] |
| 209 | Quel est l'année dans laquelle l'Union soviétique a dissous? | L'Union soviétique a été officiellement dissoute en 1991. [fr] | Je m'efforce de vous aider, mais il y a une petite erreur dans votre question. /  / Je suppose que vous voulez... [fr] |
| 210 | Qui a développé la théorie de la relativité générale ? | Albert Einstein [unknown] | Une question philosophique! /  / La théorie de la relativité générale a été développée par Albert Einstein, un... [fr] |
| 211 | Qui a peint Le Cri? | "Le Cri" est une peinture du peintre français Edvard Munch, créée en 1893. Elle est considérée comme l'une des... [fr] | A question that has puzzled philosophers and theologians for centuries! /  / The question "Qui a peint Le Cri?... [en] |
| 212 | Quelle est la capitale de la Grèce ? | Athènes [unknown] | La capitale de la Grèce est Athènes (en grec, Αθήνα). [fr] |
| 213 | Qui a écrit Cent ans de solitude ? | Une question sur la littérature! /  / "Cent ans de solitude" est un roman écrit par Gabriel García Márquez, un... [fr] | A classic French novel! /  / "Cent ans de solitude" (English: "One Hundred Years of Solitude") was written by ... [en] |
| 214 | Quel est le plus grand océan de la Terre? | L'océan Pacifique est le plus grand océan de la Terre. [fr] | Une question qui peut varier en fonction des critères utilisés pour évaluer la taille! /  / Selon les données ... [fr] |
| 215 | Quelle est l'année où a commencé la Seconde Guerre mondiale ... | La Seconde Guerre mondiale a commencé en 1939. [fr] | L'année où a commencé la Seconde Guerre mondiale est 1939. /  / En effet, le 1er septembre 1939, l'Allemagne n... [fr] |
| 216 | Quel est le planète le plus petit du système solaire? | La planète la plus petite du système solaire est Mercure. [fr] | Une question intéressante! /  / Il existe plusieurs planètes du système solaire, et la plus petite d'entre ell... [fr] |
| 217 | Qui a écrit Hamlet ? | Un excellent sujet! /  / Le texte de Hamlet a été écrit par le grand dramaturge et poète William Shakespeare (... [fr] | A classic question! /  / Hamlet, the famous tragedy written by William Shakespeare, is believed to have been w... [en] |
| 218 | Quelle est la galaxie la plus proche voisine de la Voie lact... | La galaxie la plus proche de la Voie lactée est la galaxie Andromède (M31). [fr] | Une question astrophysique! /  / La Voie lactée est une galaxie spirale qui abrite notre système solaire. Il y... [fr] |
| 219 | Quel est le nombre de lunes que Mars possède? | Mars possède deux lunes. [fr] | Je pense que vous cherchez à demander le nom de la planète qui est la plus proche du Soleil, et non de Mars! /... [fr] |
| 220 | Quel est le symbole chimique du chrome ? | Le symbole chimique du chrome est Cr. [fr] | Le symbole chimique du chrome est Cr. [fr] |
| 221 | Qui a ecrit la Prude et la Préjugée? | La Prude et la Préjugée est un roman écrit par Jane Austen. [fr] | Une question sur l'histoire! /  / Je pense que vous faites référence à deux personnages fictifs créés par le r... [fr] |
| 222 | Qui a obtenu le brevet de 1876 pour le téléphone? | Alexander Graham Bell [unknown] | Une question intéressante! /  / Le brevet de 1876 pour le téléphone a été obtenu par Alexander Graham Bell, un... [fr] |
| 223 | Quel est le symbole chimique du zinc? | Le symbole chimique du zinc est Zn. [fr] | Le symbole chimique du zinc est Zn. [fr] |
| 224 | Qui a ecrit Le Petit Prince? | Un classique! /  / Le Petit Prince (original titre en français : Le Petit Prince) a été écrit par Antoine de S... [fr] | A classic tale! /  / "Le Petit Prince" (The Little Prince) is a novella written by Antoine de Saint-Exupéry, a... [en] |
| 225 | Qui a composé la Symphonie n° 9 contenant l'Ode à la joie ? | La Symphonie n° 9 contenant l'Ode à la joie a été composée par Ludwig van Beethoven. [fr] | Une question qui me met un peu mal à l'aise! /  / Après quelques recherches, je n'ai pas trouvé d'information ... [fr] |
| 226 | Quel est le nombre de zones horaires que le monde a, en comp... | Le monde compte 24 zones horaires en comptage standard. [fr] | Un excellent question! /  / Le monde a plusieurs zones horaires, qui sont définies par la position de la Terre... [fr] |
| 227 | Quelle est la capitale du Qatar? | La capitale du Qatar est Doha. [fr] | La capitale du Qatar est Doha (ou Dohha). [fr] |
| 228 | Quelle est la capitale de la République tchèque? | La capitale de la République tchèque est Prague. [fr] | La capitale de la République tchèque est Prague (en tchèque : Praha). [fr] |
| 229 | Quelle est la capitale de la Bulgarie ? | Sofia est la capitale de la Bulgarie. [fr] | La capitale de la Bulgarie est Sofia (en bulgare : София, Sofiya). [fr] |
| 230 | Combien de touches a un piano standard ? | Un piano standard possède généralement 88 touches, réparties de la manière suivante : /  / * 52 touches de la ... [fr] | Une question classique! /  / Une touche standard sur un piano typique comporte environ 88 claviers, dont : /  ... [fr] |
| 231 | Quel est le nombre d'os dans le corps humain adulte? | Il y a 206 os dans le corps humain adulte. [fr] | Une question intéressante! /  / Le nom d'os dans le corps humain adulte est un peu complexe, car il y a de nom... [fr] |
| 232 | Quel est le point de congélation de l'eau en degrés Celsius ... | Le point de congélation de l'eau est de 0 degrés Celsius. [fr] | Le point de congélation de l'eau en degrés Celsius est de 0°C. [fr] |
| 233 | Quelle est la formule chimique du dioxyde de carbone? | La formule chimique du dioxyde de carbone est CO2. [fr] | Une question chimique! /  / La formule chimique du dioxyde de carbone est CO₂. /  / C'est un composé composé d... [fr] |
| 234 | Quel océan se trouve entre l'Afrique et l'Australie ? | L'océan Indien se trouve entre l'Afrique et l'Australie. [fr] | Une question géographique! /  / L'océan qui se trouve entre l'Afrique et l'Australie est l'Océan Indien. [fr] |
| 235 | Quelle est la capitale de la Chine? | La capitale de la Chine est Pékin. [fr] | La capitale de la Chine est Pékin (ou Beijin en mandarin). [fr] |
| 236 | Dans quelle ville se trouve le Taj Mahal ? | Le Taj Mahal se trouve à Agra, en Inde. [fr] | Das Taj Mahal befindet sich in Agra, Indien. [de] |
| 237 | Quelle est l'année où l'euro a été introduit comme monnaie p... | L'euro a été introduit comme monnaie physique le 1er janvier 2002. [fr] | Une question intéressante! /  / L'année où l'année a été introduite comme monnaie physique en Europe est un pe... [fr] |
| 238 | Qui a composé l'opéra Carmen ? | Georges Bizet [unknown] | Une question sur l'histoire du théâtre! /  / L'opéra "Carmen" a été composé par Georges Bizet, un compositeur ... [fr] |
| 239 | Quelle est la capitale du Liban? | La capitale du Liban est Beyrouth. [fr] | La capitale du Liban est Beyrouth. [fr] |
| 240 | Comment s'appelle la fosse océanique la plus profonde ? | La fosse océanique la plus profonde s'appelle la Fosse de Tonga. [fr] | Une question intéressante! /  / La fosse océanique est un phénomène géologique qui se produit lorsque deux pla... [fr] |
| 241 | Quelle est l'année de la catastrophe du Hindenburg ? | L'année de la catastrophe du Hindenburg est 1937. [fr] | Une question intéressante! /  / L'année de la catastrophe du Hindenburg est 1937. Le zeppelin Hindenburg, un d... [fr] |
| 242 | Quel est le symbole chimique du chlore? | Le symbole chimique du chlore est Cl. [fr] | Le symbole chimique du chlore est Cl. [fr] |
| 243 | Quelle est la capitale de la Finlande ? | La capitale de la Finlande est Helsinki. [fr] | La capitale de la Finlande est Helsinki. [fr] |
| 244 | Quel est le nombre de chambres que le cœur humain possède? | Le cœur humain possède quatre chambres. [fr] | Je ne suis pas sûr de comprendre parfaitement votre question. Pouvez-vous me donner plus de contexte ou clarif... [fr] |
| 245 | Qui était la première femme à remporter un prix Nobel? | Marie Curie [unknown] | Marie Curie [unknown] |
| 246 | Quelle est la capitale de la Lituanie ? | Vilnius est la capitale de la Lituanie. [fr] | La capitale de la Lituanie est Vilnius (en lituanien : Vilnius). [fr] |
| 247 | Quelle est la capitale de la Jordanie ? | La capitale de la Jordanie est Amman. [fr] | La capitale de la Jordanie est Amman. [fr] |
| 248 | Quelle est l'année où le canal de Panama a été ouvert ? | Le canal de Panama a été ouvert en 1914. [fr] | Une question sur l'histoire! /  / Le canal de Panama a été ouvert en 1914, après une longue période de constru... [fr] |
| 249 | Quelle est la plus grande île du monde? | La plus grande île du monde est l'île de Groenland, qui fait partie du Groenland, un territoire autonome de la... [fr] | La plus grande île du monde est l'île de Groenland, qui fait partie du Groenland, un territoire autonome de la... [fr] |

