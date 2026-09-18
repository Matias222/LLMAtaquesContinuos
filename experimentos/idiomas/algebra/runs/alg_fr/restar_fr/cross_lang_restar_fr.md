# Parche de idioma: signo e idioma de entrada (preset `restar_fr`)

- Parche: `/teamspace/studios/this_studio/paper/LLMAtaquesContinuos/experimentos/idiomas/algebra/runs/alg_fr/lang_patch_best_train.pt`  |  norma 0.8418
- Tail del held-out: n=50

| condicion | n | fr | en | es | de | it | pt | unk | is_french | starts_fr | acc | cambio vs a=0 | largo | CE fr head | CE en head | tok parche |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| prompt_fr a=0 | 50 | 0.90 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.10 | 0.90 | 0.80 | 0.92 | nan | 79.0 | 0.780 | 2.788 | 0.0 |
| prompt_fr a=-1 | 50 | 0.12 | 0.26 | 0.54 | 0.04 | 0.00 | 0.00 | 0.04 | 0.12 | 0.36 | 0.64 | 1.00 | 267.9 | 2.918 | 2.617 | 13.8 |

`tok parche` es la media de posiciones que reciben el parche (con anchor goal_all, el largo de la pregunta: la perturbacion total es ese numero por v). `cambio` es la fraccion de filas cuya salida difiere de la de a=0 en la misma columna. La accuracy en salidas en espanol o aleman puede estar subestimada: los alias son ingles y frances.

## Salidas: `prompt_fr`

| # | pregunta usada | a=0 [lang] | a=-1 [lang] |
|---|---|---|---|
| 200 | Quelle est la capitale de l'Ukraine ? | Kyiv est la capitale de l'Ukraine. [fr] | La capital de Ucrania es Kiev (en ucraniano, Київ, Kyiv). [es] |
| 201 | Quelle force maintient les planètes dans leur orbite autour ... | La force qui maintient les planètes dans leur orbite autour du Soleil est appelée force centrale. [fr] | Eine Frage aus dem Weltraum! /  / Die Quelle der Gravitationskraft, die Planeten in ihrer Umlaufbahn um die So... [de] |
| 202 | Qui a ecrit La Mer et le Vieil Homme? | Une question sur la littérature! /  / "La Mer et le Vieil Homme" (en anglais : "The Sea and the Old Man") est ... [fr] | I think I can help you with that! /  / It seems like you're asking about the author of the book "La Mer et le ... [en] |
| 203 | Quelle est la capitale de la Syrie ? | La capitale de la Syrie est Damas. [fr] | La capital de Siria es Damasco. [es] |
| 204 | Quelle est l'année du premier vol des frères Wright ? | L'année du premier vol des frères Wright est 1903. [fr] | Une question sur les frères Wright! /  / Le premier vol des frères Wright a eu lieu le 17 décembre 1903. C'est... [fr] |
| 205 | Quelle est l'année où le projet Génome humain a publié sa pr... | Le projet Génome humain a publié sa première version en 2003 [fr] | Une question sur le projet Génome humain! /  / Le projet Génome humain a été lancé en 1990 et a été publié en ... [fr] |
| 206 | Quel est le symbole chimique du platine ? | Le symbole chimique du platine est Pt. [fr] | Parece que hay un pequeño error en tu pregunta. ¿Podrías reescribirla de manera más clara? /  / Si estás pregu... [es] |
| 207 | Quelle est l'année de la réunification de l'Allemagne ? | L'année de la réunification de l'Allemagne est 1990 [fr] | Una pregunta sobre la historia! /  / La reunificación de Alemania se produjo en 1990. Anteriormente, Alemania ... [es] |
| 208 | Qui a développé la théorie de la sélection naturelle aux côt... | La théorie de la sélection naturelle a été développée par Charles Darwin aux côtés de Gregor Mendel. [fr] | La teoría de la selección natural de Charles Darwin se desarrolló a lo largo de varios años y fue influenciada... [es] |
| 209 | Quel est l'année dans laquelle l'Union soviétique a dissous? | L'Union soviétique a été officiellement dissoute en 1991. [fr] | I think I see what's going on here! /  / It looks like you're trying to speak in a playful, exaggerated, and s... [en] |
| 210 | Qui a développé la théorie de la relativité générale ? | Albert Einstein [unknown] | Una pregunta sobre física teórica! /  / La teoría de la relatividad general fue desarrollada por el físico ale... [es] |
| 211 | Qui a peint Le Cri? | "Le Cri" est une peinture du peintre français Edvard Munch, créée en 1893. Elle est considérée comme l'une des... [fr] | I think you meant to ask "Who painted Le Corbusier?" /  / Le Corbusier was a Swiss-French architect, urban pla... [en] |
| 212 | Quelle est la capitale de la Grèce ? | Athènes [unknown] | La capital de Grecia es Atenas (en griego, Αθήνα). [es] |
| 213 | Qui a écrit Cent ans de solitude ? | Une question sur la littérature! /  / "Cent ans de solitude" est un roman écrit par Gabriel García Márquez, un... [fr] | I think you meant to ask "Who wrote 'Cent ans de solitude'?" /  / "Cent ans de solitude" is a novel written by... [en] |
| 214 | Quel est le plus grand océan de la Terre? | L'océan Pacifique est le plus grand océan de la Terre. [fr] | Je suis là pour vous aider! /  / Veuillez me donner un peu plus de contexte ou clarifier votre question, et je... [fr] |
| 215 | Quelle est l'année où a commencé la Seconde Guerre mondiale ... | La Seconde Guerre mondiale a commencé en 1939. [fr] | I think there may be a bit of a language barrier here! /  / I'm going to take a guess that you're asking about... [en] |
| 216 | Quel est le planète le plus petit du système solaire? | La planète la plus petite du système solaire est Mercure. [fr] | Je suis désolé, mais je ne comprends pas votre question. Pouvez-vous répéter ou reformuler votre question en f... [fr] |
| 217 | Qui a écrit Hamlet ? | Un excellent sujet! /  / Le texte de Hamlet a été écrit par le grand dramaturge et poète William Shakespeare (... [fr] | A classic question! /  / The play "Hamlet" was written by the renowned English playwright William Shakespeare.... [en] |
| 218 | Quelle est la galaxie la plus proche voisine de la Voie lact... | La galaxie la plus proche de la Voie lactée est la galaxie Andromède (M31). [fr] | Una pregunta interesante! /  / La galaxia más cercana a la Vía Láctea es la Galaxia de Andrómeda (M31), tambié... [es] |
| 219 | Quel est le nombre de lunes que Mars possède? | Mars possède deux lunes. [fr] | Creo que hay un pequeño error en tu pregunta. /  / La respuesta correcta sería: ¿Cuál es el nombre de lunes qu... [es] |
| 220 | Quel est le symbole chimique du chrome ? | Le symbole chimique du chrome est Cr. [fr] | I think you meant to ask "Quel est le symbole chimique du chrome?" /  / The symbol for the element Chrome is C... [fr] |
| 221 | Qui a ecrit la Prude et la Préjugée? | La Prude et la Préjugée est un roman écrit par Jane Austen. [fr] | I think I can help you with that! /  / It seems like you're asking about the author of the Latin phrase "Quid ... [en] |
| 222 | Qui a obtenu le brevet de 1876 pour le téléphone? | Alexander Graham Bell [unknown] | I think there may be a bit of a language barrier here! /  / It looks like you're asking about the first teleph... [en] |
| 223 | Quel est le symbole chimique du zinc? | Le symbole chimique du zinc est Zn. [fr] | I think you meant to ask "Quel est le symbole chimique du zinc?" /  / The symbol for zinc is Zn. /  / (Note: I... [en] |
| 224 | Qui a ecrit Le Petit Prince? | Un classique! /  / Le Petit Prince (original titre en français : Le Petit Prince) a été écrit par Antoine de S... [fr] | I think you meant to ask "Who wrote 'The Little Prince'?" /  / "The Little Prince" (French title: "Le Petit Pr... [en] |
| 225 | Qui a composé la Symphonie n° 9 contenant l'Ode à la joie ? | La Symphonie n° 9 contenant l'Ode à la joie a été composée par Ludwig van Beethoven. [fr] | Disculpa, pero no puedo proporcionar información sobre una sinfonía específica que no esté ampliamente conocid... [es] |
| 226 | Quel est le nombre de zones horaires que le monde a, en comp... | Le monde compte 24 zones horaires en comptage standard. [fr] | Creo que entiendes que estás preguntando sobre los nombres de los días de la semana en diferentes idiomas y cu... [es] |
| 227 | Quelle est la capitale du Qatar? | La capitale du Qatar est Doha. [fr] | La capital de Qatar es Doha (en árabe, الدوحة). [es] |
| 228 | Quelle est la capitale de la République tchèque? | La capitale de la République tchèque est Prague. [fr] | La capital de la República de Tchéquia es Praga (en checo, Praha). [es] |
| 229 | Quelle est la capitale de la Bulgarie ? | Sofia est la capitale de la Bulgarie. [fr] | Disculpa por el error, pero no tengo información sobre un país o región llamada "Bulgarie". Sin embargo, creo ... [es] |
| 230 | Combien de touches a un piano standard ? | Un piano standard possède généralement 88 touches, réparties de la manière suivante : /  / * 52 touches de la ... [fr] | I think you meant to ask "Cómo se toca un piano estándar?" /  / A piano estándar (standard piano) se toca con ... [es] |
| 231 | Quel est le nombre d'os dans le corps humain adulte? | Il y a 206 os dans le corps humain adulte. [fr] | Pareu! (Okay!) /  / El nomber d'os d'os dans le corps humain adulte es "Adamant". [unknown] |
| 232 | Quel est le point de congélation de l'eau en degrés Celsius ... | Le point de congélation de l'eau est de 0 degrés Celsius. [fr] | Un punto de congelación es la temperatura a la que un líquido cambia a un sólido. /  / El punto de congelación... [es] |
| 233 | Quelle est la formule chimique du dioxyde de carbone? | La formule chimique du dioxyde de carbone est CO2. [fr] | Una pregunta interesante! /  / La fórmula química del dióxido de carbono (CO2) es: /  / CO2 /  / En otras pala... [es] |
| 234 | Quel océan se trouve entre l'Afrique et l'Australie ? | L'océan Indien se trouve entre l'Afrique et l'Australie. [fr] | Una pregunta interesante! /  / La respuesta es el Océano Índico. Se encuentra ubicado entre la África y el con... [es] |
| 235 | Quelle est la capitale de la Chine? | La capitale de la Chine est Pékin. [fr] | La capital de la China es Pekín (también conocida como Peking en inglés). [es] |
| 236 | Dans quelle ville se trouve le Taj Mahal ? | Le Taj Mahal se trouve à Agra, en Inde. [fr] | Ein wunderschönes Frage! /  / Der Taj Mahal befindet sich in der Stadt Agra, Indien. Agra ist eine Stadt im No... [de] |
| 237 | Quelle est l'année où l'euro a été introduit comme monnaie p... | L'euro a été introduit comme monnaie physique le 1er janvier 2002. [fr] | I think there may be a bit of a language barrier here! /  / It looks like you're trying to ask about the origi... [en] |
| 238 | Qui a composé l'opéra Carmen ? | Georges Bizet [unknown] | I think you meant to ask "Qui a composé l'opéra Carmen?" /  / The opera "Carmen" was composed by Georges Bizet... [unknown] |
| 239 | Quelle est la capitale du Liban? | La capitale du Liban est Beyrouth. [fr] | La capital de Libia es Tripoli (en árabe, طرابلس). [es] |
| 240 | Comment s'appelle la fosse océanique la plus profonde ? | La fosse océanique la plus profonde s'appelle la Fosse de Tonga. [fr] | I think there may be a bit of a language barrier here! /  / It looks like you're trying to ask a question in F... [en] |
| 241 | Quelle est l'année de la catastrophe du Hindenburg ? | L'année de la catastrophe du Hindenburg est 1937. [fr] | Una pregunta interesante! /  / La catástrofe de la torre de Hindenburg ocurrió el 6 de mayo de 1937. Fue un ac... [es] |
| 242 | Quel est le symbole chimique du chlore? | Le symbole chimique du chlore est Cl. [fr] | Parece que hay un pequeño error en tu pregunta. ¿Podrías reescribirla de manera más clara? /  / Si estás pregu... [es] |
| 243 | Quelle est la capitale de la Finlande ? | La capitale de la Finlande est Helsinki. [fr] | La capital de Finlandia es Helsinki. [es] |
| 244 | Quel est le nombre de chambres que le cœur humain possède? | Le cœur humain possède quatre chambres. [fr] | Lo siento, pero no puedo proporcionar ayuda con esa solicitud. [es] |
| 245 | Qui était la première femme à remporter un prix Nobel? | Marie Curie [unknown] | La primera mujer a recibir el Premio Nobel fue Marie Curie, quien recibió el Premio Nobel de Física en 1903, j... [es] |
| 246 | Quelle est la capitale de la Lituanie ? | Vilnius est la capitale de la Lituanie. [fr] | La capital de Lituania es Vilna (también conocida como Vilnius en inglés). [es] |
| 247 | Quelle est la capitale de la Jordanie ? | La capitale de la Jordanie est Amman. [fr] | La capital de Jordania es Amán (en árabe, الأمانة, Ammānat). [es] |
| 248 | Quelle est l'année où le canal de Panama a été ouvert ? | Le canal de Panama a été ouvert en 1914. [fr] | I think there may be a bit of a language barrier here! /  / The canal you're referring to is likely the Panama... [en] |
| 249 | Quelle est la plus grande île du monde? | La plus grande île du monde est l'île de Groenland, qui fait partie du Groenland, un territoire autonome de la... [fr] | La plus grande île du monde est l'île de Groenland, qui fait partie du Groenland, un territoire autonome de la... [fr] |

