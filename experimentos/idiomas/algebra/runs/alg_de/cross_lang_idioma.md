# Parche de idioma: signo e idioma de entrada (preset `idioma`)

- Parche: `/teamspace/studios/this_studio/paper/LLMAtaquesContinuos/experimentos/idiomas/algebra/runs/alg_de/lang_patch_best_train.pt`  |  norma 0.8491
- Tail del held-out: n=50

Celda target del parche: **de**. `celda ok` = idioma `de` Y NO mayusculas. En la tabla grande, `CE fr head` es la CE del target de ESTA celda (columna `output`).

| condicion | celda ok | idioma target | mayusculas |
|---|---|---|---|
| prompt_es a=0 | 0.00 | 0.00 | 0.00 |
| prompt_es a=1 | 1.00 | 1.00 | 0.00 |
| prompt_fr a=0 | 0.00 | 0.00 | 0.00 |
| prompt_fr a=1 | 1.00 | 1.00 | 0.00 |
| prompt a=0 | 0.00 | 0.00 | 0.00 |
| prompt a=1 | 0.92 | 0.92 | 0.00 |

| condicion | n | fr | en | es | de | it | pt | unk | is_french | starts_fr | acc | cambio vs a=0 | largo | CE fr head | CE en head | tok parche |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| prompt_es a=0 | 50 | 0.00 | 0.00 | 0.92 | 0.00 | 0.00 | 0.00 | 0.08 | 0.00 | 0.48 | 0.90 | nan | 76.4 | 5.421 | 2.739 | 0.0 |
| prompt_es a=1 | 50 | 0.00 | 0.00 | 0.00 | 1.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.72 | 1.00 | 90.7 | 1.083 | 5.506 | 13.9 |
| prompt_fr a=0 | 50 | 0.90 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.10 | 0.90 | 0.80 | 0.92 | nan | 79.0 | 4.480 | 2.788 | 0.0 |
| prompt_fr a=1 | 50 | 0.00 | 0.00 | 0.00 | 1.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.82 | 1.00 | 77.6 | 0.840 | 5.151 | 13.8 |
| prompt a=0 | 50 | 0.00 | 1.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.96 | nan | 181.1 | 5.199 | 0.111 | 0.0 |
| prompt a=1 | 50 | 0.00 | 0.02 | 0.00 | 0.92 | 0.00 | 0.00 | 0.06 | 0.00 | 0.00 | 0.94 | 1.00 | 76.0 | 0.426 | 3.018 | 8.7 |

`tok parche` es la media de posiciones que reciben el parche (con anchor goal_all, el largo de la pregunta: la perturbacion total es ese numero por v). `cambio` es la fraccion de filas cuya salida difiere de la de a=0 en la misma columna. La accuracy en salidas en espanol o aleman puede estar subestimada: los alias son ingles y frances.

## Salidas: `prompt_es`

| # | pregunta usada | a=0 [lang] | a=1 [lang] |
|---|---|---|---|
| 200 | ¿Cuál es la capital de Ucrania? | La capital de Ucrania es Kiev. [es] | Die Hauptstadt von Ukraine ist Kiew. [de] |
| 201 | ¿Qué fuerza mantiene a los planetas en órbita alrededor del ... | La fuerza que mantiene a los planetas en órbita alrededor del Sol es la gravedad. [es] | Die Gravitation. Die Gravitation ist die kraft, die die Planeten in ihren Umlaufbahren um die Sonne hält. [de] |
| 202 | ¿Quién escribió El viejo y el mar? | "El viejo y el mar" es una novela escrita por Ernest Hemingway, publicada en 1952. [es] | Ein klassischer Sprachtest! /  / Die Antwort ist: Albert Camus. [de] |
| 203 | ¿Cuál es la capital de Siria? | La capital de Siria es Damasco. [es] | Die Hauptstadt von Saudi-Arabien ist Riyadh. [de] |
| 204 | ¿En qué año volaron por primera vez los hermanos Wright? | El 17 de diciembre de 1903. [es] | Die Brüder Wright flogen zum ersten Mal 1903. [de] |
| 205 | ¿En qué año publicó el Proyecto del Genoma Humano su primer ... | El Proyecto del Genoma Humano publicó su primer borrador en el año 2000. [es] | Das Projekt des Human Genome Project veröffentlichte 2000 seine erste Version. [de] |
| 206 | ¿Cuál es el símbolo químico de platino? | El símbolo químico de platino es Pt. [es] | Das chemische Symbol für Gold ist Au. [de] |
| 207 | ¿En qué año se reunió Alemania? | La reunificación alemana se produjo en 1990. [es] | Die Antwort ist: 1949 [de] |
| 208 | ¿Quién desarrolló la teoría de la selección natural junto a ... | La teoría de la selección natural fue desarrollada por Charles Darwin junto a otros científicos de su época. [es] | Die Theorie der natürlichen Selektion entwickelte Charles Darwin. [de] |
| 209 | ¿En qué año se disolvió la Unión Soviética? | La Unión Soviética se disolvió en 1991. [unknown] | Die Sowjetunion wurde 1991 aufgelöst. [de] |
| 210 | ¿Quién desarrolló la teoría de la relatividad general? | La teoría de la relatividad general fue desarrollada por Albert Einstein. [es] | Die Theorie der allgemeinen Relativität wurde von Albert Einstein entwickelt. [de] |
| 211 | ¿Quién pintó El Grito? | "El Grito" es una obra maestra del pintor alemán Edvard Munch, creada en 1893. Es una de las pinturas más famo... [es] | Das ist eine einfache Frage! /  / "El Grito" (deutsch: "Der Schrei") ist ein Bild von Pablo Picasso, das 1914 ... [de] |
| 212 | ¿Cuál es la capital de Grecia? | La capital de Grecia es Atenas. [es] | Die Hauptstadt Griechenlands ist Athen. [de] |
| 213 | ¿Quién escribió Cien años de soledad? | ¡Excelente pregunta! /  / La respuesta es: Gabriel García Márquez. /  / "Cien años de soledad" es una novela m... [es] | Das Buch "Jahre der Einsamkeit" wurde von Albert Camus geschrieben. [de] |
| 214 | ¿Cuál es el océano más grande de la Tierra? | El océano más grande de la Tierra es el océano Pacífico. [es] | Der größte Ozean der Erde ist der Pazifische Ozean. [de] |
| 215 | ¿En qué año comenzó la Segunda Guerra Mundial? | La Segunda Guerra Mundial comenzó en 1939. [es] | Die Zweite Weltkrieg begann im Jahr 1939. [de] |
| 216 | ¿Cuál es el planeta más pequeño del Sistema Solar? | El planeta más pequeño del Sistema Solar es Mercurio. [es] | Der kleinste Planet im Sonnensystem ist Merkur. [de] |
| 217 | ¿Quién escribió Hamlet? | ¡Excelente pregunta! /  / El famoso drama "Hamlet" fue escrito por el gran escritor y dramaturgo inglés Willia... [es] | Hamlet wurde von dem dänischen Schriftsteller und Dichter Søren Kierkegaard nicht geschrieben, sondern von dem... [de] |
| 218 | ¿Cuál es la galaxia más cercana y grande vecina de la Vía Lá... | La galaxia más cercana y grande vecina de la Vía Láctea es la Galaxia de Andrómeda (M31). [es] | Eine Frage aus der Welt der Sterne! /  / Die Vía Láctea (auch Milchstraße genannt) ist unsere eigene Galaxie u... [de] |
| 219 | ¿Cuántas lunas tiene Marte? | Marte tiene dos lunas, Phobos y Deimos. [es] | Eine interessante Frage! /  / Marte, die Roter Planet, hat keine Lunas (monde). Sie ist ein Planet und hat kei... [de] |
| 220 | ¿Cuál es el símbolo químico de cromo? | El símbolo químico de cromo es Cr. [es] | Das chemische Symbol für Chrom ist Cr. [de] |
| 221 | ¿Quién escribió Orgullo y prejuicio? | "Orgullo y prejuicio" (título original en inglés: "Pride and Prejudice") fue escrita por la autora británica J... [es] | "Orgullo und Präjudiz" (Originaltitel: "Pride and Prejudice") wurde von Jane Austen geschrieben. [de] |
| 222 | ¿Quién recibió la patente de 1876 para el teléfono? | Alexander Graham Bell [unknown] | Die Patente für das Telefon erhielt Alexander Graham Bell. [de] |
| 223 | ¿Cuál es el símbolo químico de zinc? | El símbolo químico de zinc es Zn. [es] | Das chemische Symbol für Zink ist Zn. [de] |
| 224 | ¿Quién escribió El Príncipe pequeño? | "El Príncipe pequeño" es una obra de teatro escrita por el dramaturgo y escritor español Antonio Buero Vallejo... [es] | "Der Prinz" ist ein Kinderbuch, das von der britischen Autorin Kate Greenaway geschrieben wurde. [de] |
| 225 | ¿Quién compuso la Sinfonía Número 9 que contiene Oda a la Al... | La Sinfonía Número 9, también conocida como la Sinfonía de la Oda a la Alegría, fue compuesta por Ludwig van B... [es] | Die Sinfonie Nr. 9, die "Sinfonie zur Freude" (auch bekannt als "Choralvesper" oder "Grosse Sinfonie"), wurde ... [de] |
| 226 | ¿Cuántas zonas horarias tiene el mundo, en cuenta estándar? | El mundo tiene 24 zonas horarias estándar, que se dividen en 24 horarios. Estas zonas horarias se utilizan par... [es] | Es scheint, als sprichst du Arabisch. Die Frage "Wie viele Zehen hat der Mensch?" oder "Wie viele Zehen hat de... [de] |
| 227 | ¿Cuál es la capital de Qatar? | La capital de Qatar es Doha. [es] | Die Hauptstadt des Qatar ist Doha. [de] |
| 228 | ¿Cuál es la capital de República Checa? | La capital de la República Checa es Praga. [es] | Die Hauptstadt der Tschechischen Republik ist Prag. [de] |
| 229 | ¿Cuál es la capital de Bulgaria? | La capital de Bulgaria es Sofía. [es] | Die Hauptstadt Bulgariens ist Sofia. [de] |
| 230 | ¿Cuántas teclas tiene un piano estándar? | Un piano estándar tiene 88 teclas. [es] | Ein Standardpiano hat 88 Teclen. [de] |
| 231 | ¿Cuántas huesos hay en el cuerpo humano adulto? | En el cuerpo humano adulto, hay 206 huesos. [es] | Im einem gesunden Erwachsenenkörper gibt es etwa 206 Knochen. [de] |
| 232 | ¿Cuál es el punto de congelación del agua en grados Celsius? | 0 grados Celsius [unknown] | Der Punkt der Einfrierung von Wasser beträgt 0 Grad Celsius. [de] |
| 233 | ¿Cuál es la fórmula química del dióxido de carbono? | La fórmula química del dióxido de carbono es CO2. [es] | Die chemische Formel für Dioxid von Kohlenstoff (auch bekannt als Kohlendioxid oder CO2) lautet: /  / CO2 /  /... [de] |
| 234 | ¿Cuál océano se encuentra entre África y Australia? | El océano que se encuentra entre África y Australia es el Océano Índico. [es] | Das Indische Ocean befindet sich zwischen Afrika und Australien. [de] |
| 235 | ¿Cuál es la capital de China? | La capital de China es Pekín. [es] | Die Hauptstadt Chinas ist Peking (offiziell: Pekin). [de] |
| 236 | ¿En qué ciudad se encuentra el Taj Mahal? | El Taj Mahal se encuentra en Agra, India. [es] | Der Taj Mahal befindet sich in Agra, Indien. [de] |
| 237 | ¿En qué año se introdujo el euro como moneda física? | El euro se introdujo como moneda física en 2002. [es] | Der Euro wurde 2002 als offizielle Währung der Europäischen Union eingeführt. [de] |
| 238 | ¿Quién compuso la ópera Carmen? | La ópera "Carmen" fue compuesta por el compositor francés Georges Bizet. [es] | Die Oper "Carmen" wurde von Georges Bizet komponiert. [de] |
| 239 | ¿Cuál es la capital de Líbano? | La capital de Líbano es Beirut. [es] | Die Hauptstadt von Libanon ist Beirut. [de] |
| 240 | ¿Qué es el abismo más profundo del océano llamado? | El abismo más profundo del océano es el Mar de las Perlas, ubicado en el océano Pacífico, frente a las costas ... [es] | Das Abenteuer, das du suchst, ist das Mariana-Trench, ein tiefes Becken im Pazifischen Ozean. Es ist das tiefs... [de] |
| 241 | ¿En qué año ocurrió el desastre del Hindenburg? | El desastre del Hindenburg ocurrió en 1937. [es] | Die Hindenburg kam am 6. Mai 1937 in Flammen. [de] |
| 242 | ¿Cuál es el símbolo químico de cloro? | El símbolo químico de cloro es Cl. [es] | Das chemische Symbol für Chlor ist Cl. [de] |
| 243 | ¿Cuál es la capital de Finlandia? | La capital de Finlandia es Helsinki. [es] | Die Hauptstadt Finnlands ist Helsinki. [de] |
| 244 | ¿Cuántas cámaras tiene el corazón humano? | El corazón humano tiene 4 cámaras. [es] | Ein interessanter Frage! /  / Der Herz schlägt in jedem Menschen mit zwei Kammern. Diese beiden Kammern sind: ... [de] |
| 245 | ¿Quién fue la primera mujer a ganar un Premio Nobel? | Marie Curie fue la primera mujer en ganar un Premio Nobel. [unknown] | Die erste Frau, die einen Nobelpreis gewann, war Marie Curie. Sie erhielt den Nobelpreis für Physik 1903 gemei... [de] |
| 246 | ¿Cuál es la capital de Lituania? | La capital de Lituania es Vilna. [es] | Die Hauptstadt Litauens ist Vilnius. [de] |
| 247 | ¿Cuál es la capital de Jordania? | La capital de Jordania es Amán. [es] | Die Hauptstadt von Jordanien ist Amman. [de] |
| 248 | ¿En qué año se abrió el Canal de Panamá? | El Canal de Panamá se abrió al tráfico en 1914. [es] | Der Panama-Canal wurde 1914 eröffnet. [de] |
| 249 | ¿Cuál es la isla más grande del mundo? | La isla más grande del mundo es Groenlandia. [es] | Die größte Insel der Welt ist Grönland. [de] |

## Salidas: `prompt_fr`

| # | pregunta usada | a=0 [lang] | a=1 [lang] |
|---|---|---|---|
| 200 | Quelle est la capitale de l'Ukraine ? | Kyiv est la capitale de l'Ukraine. [fr] | Die Hauptstadt der Ukraine ist Kiew. [de] |
| 201 | Quelle force maintient les planètes dans leur orbite autour ... | La force qui maintient les planètes dans leur orbite autour du Soleil est appelée force centrale. [fr] | Die Planeten im Sonnensystem werden durch ihre eigene Schwerkraft in ihrer Umlaufbahn um die Sonne gehalten. [de] |
| 202 | Qui a ecrit La Mer et le Vieil Homme? | Une question sur la littérature! /  / "La Mer et le Vieil Homme" (en anglais : "The Sea and the Old Man") est ... [fr] | Der Text "La Mer" wurde von der französischen Schriftstellerin Paul Claudel geschrieben. [de] |
| 203 | Quelle est la capitale de la Syrie ? | La capitale de la Syrie est Damas. [fr] | Die Hauptstadt der Syrien ist Damaskus. [de] |
| 204 | Quelle est l'année du premier vol des frères Wright ? | L'année du premier vol des frères Wright est 1903. [fr] | Der erste Flug des Wright-Bruders fand im Jahr 1903 statt. [de] |
| 205 | Quelle est l'année où le projet Génome humain a publié sa pr... | Le projet Génome humain a publié sa première version en 2003 [fr] | Der Genom Project Human hat seine erste Version 2001 veröffentlicht. [de] |
| 206 | Quel est le symbole chimique du platine ? | Le symbole chimique du platine est Pt. [fr] | Das chemische Symbol für Gold ist Au. [de] |
| 207 | Quelle est l'année de la réunification de l'Allemagne ? | L'année de la réunification de l'Allemagne est 1990 [fr] | Die Jahre der Wiedervereinigung Deutschlands sind 1990 und 1991. [de] |
| 208 | Qui a développé la théorie de la sélection naturelle aux côt... | La théorie de la sélection naturelle a été développée par Charles Darwin aux côtés de Gregor Mendel. [fr] | Die Theorie der natürlichen Selektion entwickelte Charles Robert Darwin. [de] |
| 209 | Quel est l'année dans laquelle l'Union soviétique a dissous? | L'Union soviétique a été officiellement dissoute en 1991. [fr] | Der Jahr, in dem die Sowjetunion aufgelöst wurde, war 1991. [de] |
| 210 | Qui a développé la théorie de la relativité générale ? | Albert Einstein [unknown] | Die allgemeine Relativitätstheorie wurde von Albert Einstein entwickelt. [de] |
| 211 | Qui a peint Le Cri? | "Le Cri" est une peinture du peintre français Edvard Munch, créée en 1893. Elle est considérée comme l'une des... [fr] | Das Gemälde "Das Lastern" (auch bekannt als "Le cri") wurde von dem niederländischen Maler Edvard Munch im Jah... [de] |
| 212 | Quelle est la capitale de la Grèce ? | Athènes [unknown] | Die Hauptstadt Griechenlands ist Athen. [de] |
| 213 | Qui a écrit Cent ans de solitude ? | Une question sur la littérature! /  / "Cent ans de solitude" est un roman écrit par Gabriel García Márquez, un... [fr] | "Cent Ans von Stille" ist ein Roman von Volker Huß. [de] |
| 214 | Quel est le plus grand océan de la Terre? | L'océan Pacifique est le plus grand océan de la Terre. [fr] | Der größte Ozean der Erde ist der Pazifische Ozean. [de] |
| 215 | Quelle est l'année où a commencé la Seconde Guerre mondiale ... | La Seconde Guerre mondiale a commencé en 1939. [fr] | Die Zweite Weltkrieg begann im Jahr 1939. [de] |
| 216 | Quel est le planète le plus petit du système solaire? | La planète la plus petite du système solaire est Mercure. [fr] | Die kleinste Planetin im Sonnensystem ist Ceres. [de] |
| 217 | Qui a écrit Hamlet ? | Un excellent sujet! /  / Le texte de Hamlet a été écrit par le grand dramaturge et poète William Shakespeare (... [fr] | Hamlet wurde von William Shakespeare geschrieben. [de] |
| 218 | Quelle est la galaxie la plus proche voisine de la Voie lact... | La galaxie la plus proche de la Voie lactée est la galaxie Andromède (M31). [fr] | Die nächste Galaxie unserer Milchstraße, der Milchstraße, ist Andromeda-Galaxie. Sie ist etwa 2,5 Millionen Li... [de] |
| 219 | Quel est le nombre de lunes que Mars possède? | Mars possède deux lunes. [fr] | Eine Frage zum Riesenplaneten! /  / Mars, der zweitgrößte Planet unseres Sonnensystems, hat 2 Monden. Sie heiß... [de] |
| 220 | Quel est le symbole chimique du chrome ? | Le symbole chimique du chrome est Cr. [fr] | Das chemische Symbol für Chrom ist Cr. [de] |
| 221 | Qui a ecrit la Prude et la Préjugée? | La Prude et la Préjugée est un roman écrit par Jane Austen. [fr] | Der Text "Die Prüfung und die Prüfung" wurde von Thomas Merton geschrieben. [de] |
| 222 | Qui a obtenu le brevet de 1876 pour le téléphone? | Alexander Graham Bell [unknown] | Der Erfinder des Telefons war Alexander Graham Bell. Er erhielt 1876 ein Patent für das Telefon. [de] |
| 223 | Quel est le symbole chimique du zinc? | Le symbole chimique du zinc est Zn. [fr] | Das chemische Symbol für Zink ist Zn. [de] |
| 224 | Qui a ecrit Le Petit Prince? | Un classique! /  / Le Petit Prince (original titre en français : Le Petit Prince) a été écrit par Antoine de S... [fr] | Der "Petit Prince" wurde von dem französischen Schriftsteller Antoine de Saint-Exupéry geschrieben. [de] |
| 225 | Qui a composé la Symphonie n° 9 contenant l'Ode à la joie ? | La Symphonie n° 9 contenant l'Ode à la joie a été composée par Ludwig van Beethoven. [fr] | Die Symphonie Nr. 9, die "Ode an die Freude" enthält, wurde von Ludwig van Beethoven komponiert. [de] |
| 226 | Quel est le nombre de zones horaires que le monde a, en comp... | Le monde compte 24 zones horaires en comptage standard. [fr] | Die Welt hat 24 Zeitzonen. [de] |
| 227 | Quelle est la capitale du Qatar? | La capitale du Qatar est Doha. [fr] | Die Hauptstadt von Qatar ist Doha. [de] |
| 228 | Quelle est la capitale de la République tchèque? | La capitale de la République tchèque est Prague. [fr] | Die Hauptstadt der Tschechischen Republik ist Prag. [de] |
| 229 | Quelle est la capitale de la Bulgarie ? | Sofia est la capitale de la Bulgarie. [fr] | Die Hauptstadt Bulgariens ist Sofia. [de] |
| 230 | Combien de touches a un piano standard ? | Un piano standard possède généralement 88 touches, réparties de la manière suivante : /  / * 52 touches de la ... [fr] | Ein Standardpiano hat typischerweise 88 Tasten. [de] |
| 231 | Quel est le nombre d'os dans le corps humain adulte? | Il y a 206 os dans le corps humain adulte. [fr] | Die Anzahl der Knochen im menschlichen Erwachsenenkörper beträgt 206. [de] |
| 232 | Quel est le point de congélation de l'eau en degrés Celsius ... | Le point de congélation de l'eau est de 0 degrés Celsius. [fr] | Das Einfrieren von Wasser im Grad Celsius erreicht eine Temperatur von 0°C. [de] |
| 233 | Quelle est la formule chimique du dioxyde de carbone? | La formule chimique du dioxyde de carbone est CO2. [fr] | Die chemische Formel für die Dioxyd von Kohlenstoff ist CO2. [de] |
| 234 | Quel océan se trouve entre l'Afrique et l'Australie ? | L'océan Indien se trouve entre l'Afrique et l'Australie. [fr] | Der Indische Ozean befindet sich zwischen Afrika und Australien. [de] |
| 235 | Quelle est la capitale de la Chine? | La capitale de la Chine est Pékin. [fr] | Die Hauptstadt Chinas ist Peking (offiziell: Pekin). [de] |
| 236 | Dans quelle ville se trouve le Taj Mahal ? | Le Taj Mahal se trouve à Agra, en Inde. [fr] | Der Taj Mahal befindet sich in Agra, Indien. [de] |
| 237 | Quelle est l'année où l'euro a été introduit comme monnaie p... | L'euro a été introduit comme monnaie physique le 1er janvier 2002. [fr] | Der Euro wurde 1999 eingeführt. [de] |
| 238 | Qui a composé l'opéra Carmen ? | Georges Bizet [unknown] | Die Oper "Carmen" wurde von dem spanischen Komponisten Georges Bizet komponiert. [de] |
| 239 | Quelle est la capitale du Liban? | La capitale du Liban est Beyrouth. [fr] | Die Hauptstadt Libans ist Beirut. [de] |
| 240 | Comment s'appelle la fosse océanique la plus profonde ? | La fosse océanique la plus profonde s'appelle la Fosse de Tonga. [fr] | Ich helfe Ihnen gerne bei Ihrer Frage. Die "Fossa Oceanica" ist eine tiefe geologische Struktur im Ozean, die ... [de] |
| 241 | Quelle est l'année de la catastrophe du Hindenburg ? | L'année de la catastrophe du Hindenburg est 1937. [fr] | Die Hindenburg stürzte am 6. Mai 1937 ab. [de] |
| 242 | Quel est le symbole chimique du chlore? | Le symbole chimique du chlore est Cl. [fr] | Das chemische Symbol für Chlor ist Cl. [de] |
| 243 | Quelle est la capitale de la Finlande ? | La capitale de la Finlande est Helsinki. [fr] | Die Hauptstadt Finnlands ist Helsinki. [de] |
| 244 | Quel est le nombre de chambres que le cœur humain possède? | Le cœur humain possède quatre chambres. [fr] | Ich denke, es gibt ein kleines Missverständnis! Das Herz eines Menschen hat nicht mehrere Kammern. Es besteht ... [de] |
| 245 | Qui était la première femme à remporter un prix Nobel? | Marie Curie [unknown] | Bislang gibt es keine Frau, die den Nobelpreis in allen Disziplinen gewonnen hat. Die ersten Frauen, die den N... [de] |
| 246 | Quelle est la capitale de la Lituanie ? | Vilnius est la capitale de la Lituanie. [fr] | Die Hauptstadt Litauens ist Vilnius. [de] |
| 247 | Quelle est la capitale de la Jordanie ? | La capitale de la Jordanie est Amman. [fr] | Die Hauptstadt von Jordanien ist Amman. [de] |
| 248 | Quelle est l'année où le canal de Panama a été ouvert ? | Le canal de Panama a été ouvert en 1914. [fr] | Der Panama-Canal wurde 1914 eröffnet. [de] |
| 249 | Quelle est la plus grande île du monde? | La plus grande île du monde est l'île de Groenland, qui fait partie du Groenland, un territoire autonome de la... [fr] | Die größte Insel der Welt ist Grönland. [de] |

## Salidas: `prompt`

| # | pregunta usada | a=0 [lang] | a=1 [lang] |
|---|---|---|---|
| 200 | What is the capital of Ukraine? | The capital of Ukraine is Kyiv (also known as Kiev). [en] | Die Hauptstadt der Ukraine ist Kiew. [de] |
| 201 | What force keeps planets in orbit around the Sun? | The force that keeps planets in orbit around the Sun is called gravity. Specifically, it's the gravitational f... [en] | Die Antwort ist: Die Schwerkraft! /  / Die Schwerkraft ist die Kraft, die zwischen zwei Massen wirkt und die P... [de] |
| 202 | Who wrote The Old Man and the Sea? | The Old Man and the Sea is a novella written by the renowned American author Ernest Hemingway. It was first pu... [en] | Der Roman "Der alte Mann und das Meer" wurde von Ernest Hemingway geschrieben. [de] |
| 203 | What is the capital of Syria? | The capital of Syria is Damascus. [en] | Die Hauptstadt Syriens ist Damaskus. [de] |
| 204 | In what year did the Wright brothers first fly? | The Wright brothers, Orville and Wilbur, successfully flew the first powered, heavier-than-air aircraft on Dec... [en] | Die Wright-Brüder, Orville und Wilbur, unternahmen am 17. Dezember 1903 ihren ersten erfolgreichen Flug mit de... [de] |
| 205 | In what year did the Human Genome Project publish its first ... | The Human Genome Project published its first draft in 2000. [en] | Der Human Genome Project veröffentlichte seinen ersten Draft im Jahr 2000. [de] |
| 206 | What is the chemical symbol for platinum? | The chemical symbol for platinum is Pt. [en] | Das chemische Symbol für Platin ist Pt. [de] |
| 207 | In what year did Germany reunify? | Germany reunified on October 3, 1990. This was the day when East Germany (GDR) and West Germany (FRG) were off... [en] | Die deutsche Wiedervereinigung ist im Jahr 1990 passiert. [de] |
| 208 | Who developed the theory of natural selection alongside Darw... | While Charles Darwin is often credited with developing the theory of natural selection, he didn't work alone. ... [en] | Die Theorie des natürlichen Ausmerzens entwickelte Charles Darwin gemeinsam mit Gregor Mendel. [de] |
| 209 | In what year did the Soviet Union dissolve? | The Soviet Union dissolved in 1991. Specifically, it was officially dissolved on December 26, 1991, when the S... [en] | Die Sowjetunion wurde 1991 aufgelöst. [de] |
| 210 | Who developed the theory of general relativity? | The theory of general relativity was developed by Albert Einstein. He published his groundbreaking work, "Theo... [en] | Albert Einstein entwickelte die Theorie der allgemeinen Relativität. [de] |
| 211 | Who painted The Scream? | The painting "The Scream" was created by the Norwegian artist Edvard Munch in 1893. It's one of his most famou... [en] | Die Skrime wurden von Edvard Munch gemalt. [de] |
| 212 | What is the capital of Greece? | The capital of Greece is Athens. [en] | Die Hauptstadt Griechenlands ist Athen. [de] |
| 213 | Who wrote One Hundred Years of Solitude? | A classic of magical realism! /  / "One Hundred Years of Solitude" was written by the Colombian author Gabriel... [en] | Eine gute Frage! /  / "One Hundred Years of Solitude" (originaltitel: "Cien años de soledad") wurde von dem ko... [de] |
| 214 | What is the largest ocean on Earth? | The largest ocean on Earth is the Pacific Ocean, which covers approximately 155.6 million square kilometers (6... [en] | Der größte Ozean auf der Erde ist der Pazifische Ozean. Er hat eine Fläche von etwa 155,6 Millionen Quadratkil... [de] |
| 215 | In what year did World War II begin? | World War II began in 1939. Specifically, it started on September 1, 1939, when Nazi Germany, led by Adolf Hit... [en] | Die Zweite Weltkrieg begann im Jahr 1939. [de] |
| 216 | Which is the smallest planet in the Solar System? | The smallest planet in our Solar System is Mercury. It has a diameter of approximately 4,879 kilometers (3,031... [en] | Der kleinste Planet im Sonnensystem ist Merkur. [de] |
| 217 | Who wrote Hamlet? | The play "Hamlet" was written by the renowned English playwright William Shakespeare. It is one of his most fa... [en] | Der Schauspieler und Dichter William Shakespeare hat Hamlet geschrieben. [de] |
| 218 | Which galaxy is the nearest large neighbour to the Milky Way... | The nearest large neighbor to the Milky Way galaxy is the Andromeda Galaxy, also known as Messier 31 (M31) or ... [en] | Die nächste große Nachbargalaxie der Milchstraße ist Andromeda (M31). Sie befindet sich etwa 2,5 Millionen Lic... [de] |
| 219 | How many moons does Mars have? | Mars has two small natural satellites, or moons. Their names are Phobos and Deimos. [en] | Mars hat zwei Mondchen, die als Phobos und Deimos bezeichnet werden. [de] |
| 220 | What is the chemical symbol for chromium? | The chemical symbol for Chromium is Cr. [en] | Das chemische Symbol für Chrom ist Cr. [de] |
| 221 | Who wrote Pride and Prejudice? | A classic question! /  / Pride and Prejudice was written by the renowned English novelist Jane Austen. The nov... [en] | Pride and Prejudice wurde von Jane Austen geschrieben. [unknown] |
| 222 | Who received the 1876 patent for the telephone? | Alexander Graham Bell received the 1876 patent for the telephone. [en] | Alexander Graham Bell [unknown] |
| 223 | What is the chemical symbol for zinc? | The chemical symbol for zinc is Zn. [en] | Das chemische Symbol für Zink ist Zn. [de] |
| 224 | Who wrote The Little Prince? | The Little Prince (French title: Le Petit Prince) was written by Antoine de Saint-Exupéry, a French author, po... [en] | Der "Kleine Prinz" wurde von Antoine de Saint-Exupéry geschrieben. [unknown] |
| 225 | Who composed the Ninth Symphony containing Ode to Joy? | The Ninth Symphony, also known as the "Choral Symphony," was composed by Ludwig van Beethoven. It is one of hi... [en] | Die Neunte Sinfonie von Ludwig van Beethoven enthält die Ode an die Freude. Sie wurde von Beethoven selbst kom... [de] |
| 226 | How many time zones does the world have, in standard count? | The world has 24 time zones in standard count. These time zones are identified by their offset from Coordinate... [en] | The world has 24 time zones in standard count. [en] |
| 227 | What is the capital of Qatar? | The capital of Qatar is Doha. [en] | Die Hauptstadt von Qatar ist Doha. [de] |
| 228 | What is the capital of Czechia? | The capital of Czechia is Prague (Praha in Czech). [en] | Die Hauptstadt der Tschechischen Republik ist Prag. [de] |
| 229 | What is the capital of Bulgaria? | The capital of Bulgaria is Sofia (София). [en] | Die Hauptstadt Bulgariens ist Sofia. [de] |
| 230 | How many keys does a standard piano have? | A standard piano typically has 88 keys. This includes: /  / * 52 white keys (also known as naturals) / * 36 bl... [en] | Ein Standardpiano hat 88 Tasten. [de] |
| 231 | How many bones are in the adult human body? | There are 206 bones in the adult human body. This number can vary slightly from person to person, as some indi... [en] | In einem erwachsenen menschlichen Körper gibt es 206 Knochen. [de] |
| 232 | What is the freezing point of water in degrees Celsius? | The freezing point of water is 0 degrees Celsius (°C). [en] | Die Gefrierpunkt von Wasser beträgt 0 Grad Celsius. [de] |
| 233 | What is the chemical formula for carbon dioxide? | The chemical formula for carbon dioxide is CO2. [en] | Die chemische Formel für Kohlendioxid ist CO2. [de] |
| 234 | Which ocean lies between Africa and Australia? | The Indian Ocean lies between Africa and Australia. [en] | Der Indische Ozean liegt zwischen Afrika und Australien. [de] |
| 235 | What is the capital of China? | The capital of China is Beijing. [en] | Die Hauptstadt Chinas ist Peking (offiziell: Pekin). [de] |
| 236 | In which city is the Taj Mahal located? | The Taj Mahal is located in Agra, India. [en] | Der Taj Mahal befindet sich in Agra, Indien. [de] |
| 237 | In what year was the euro introduced as physical currency? | The euro was introduced as physical currency in 2002. The first euro coins were minted in 2001, but they were ... [en] | Der Euro wurde 2002 als physische Währung eingeführt. [de] |
| 238 | Who composed the opera Carmen? | The opera "Carmen" was composed by Georges Bizet. [en] | Die Oper "Carmen" wurde von dem französischen Komponisten Georges Bizet komponiert. [de] |
| 239 | What is the capital of Lebanon? | The capital of Lebanon is Beirut. [en] | Die Hauptstadt von Libanon ist Beirut. [de] |
| 240 | What is the deepest ocean trench called? | The deepest ocean trench is called the Mariana Trench. Specifically, the lowest point in the trench is called ... [en] | Die tiefste Ozeantiefe wird als Mariana-Trench bezeichnet. [de] |
| 241 | In what year did the Hindenburg disaster occur? | The Hindenburg disaster occurred on May 6, 1937. [en] | Die Hindenburg-Disaster ist am 6. Mai 1937 passiert. [de] |
| 242 | What is the chemical symbol for chlorine? | The chemical symbol for chlorine is Cl. [en] | Das chemische Symbol für Chlor ist Cl. [de] |
| 243 | What is the capital of Finland? | The capital of Finland is Helsinki. [en] | Die Hauptstadt von Finnland ist Helsinki. [de] |
| 244 | How many chambers does the human heart have? | The human heart has 4 chambers: /  / 1. **Right Atrium** (upper right chamber) / 2. **Right Ventricle** (lower... [en] | Das menschliche Herz hat vier Kammer. [de] |
| 245 | Who was the first woman to win a Nobel Prize? | Marie Curie was the first woman to win a Nobel Prize, and she won two Nobel Prizes in different fields. She wa... [en] | Die erste Frau, die einen Nobelpreis gewann, war Marie Curie. Sie erhielt den Nobelpreis für Physik 1903 gemei... [de] |
| 246 | What is the capital of Lithuania? | The capital of Lithuania is Vilnius. [en] | Die Hauptstadt von Litauen ist Vilnius. [de] |
| 247 | What is the capital of Jordan? | The capital of Jordan is Amman. [en] | Die Hauptstadt von Jordanien ist Amman. [de] |
| 248 | In what year was the Panama Canal opened? | The Panama Canal was opened on August 15, 1914. [en] | Der Panama-Kanal wurde 1914 eröffnet. [de] |
| 249 | Which is the largest island in the world? | The largest island in the world is Greenland, which is an autonomous territory within the Kingdom of Denmark. ... [en] | Das größte Inseln im Welt sind: /  / 1. Großbritannien (Grönland) - 2.166.086 km² / 2. Borneo - 743.330 km² / ... [de] |

