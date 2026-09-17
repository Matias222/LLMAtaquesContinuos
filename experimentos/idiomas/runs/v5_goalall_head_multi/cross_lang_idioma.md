# Parche de idioma: signo e idioma de entrada (preset `idioma`)

- Parche: `/mnt/custom-file-systems/efs/fs-0ded2930a619aa967_fsap-0faa05c681ed1a8f3/papers/LLMAtaquesContinuos/experimentos/idiomas/runs/v5_goalall_head_multi/lang_patch_best_train.pt`  |  norma 0.8228
- Tail del held-out: n=50

| condicion | n | fr | en | es | de | it | pt | unk | is_french | starts_fr | acc | cambio vs a=0 | largo | CE fr head | CE en head | tok parche |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| prompt_es a=0 | 50 | 0.00 | 0.00 | 0.92 | 0.00 | 0.00 | 0.00 | 0.08 | 0.00 | 0.48 | 0.76 | nan | 76.4 | 4.608 | 2.739 | 0.0 |
| prompt_es a=1 | 50 | 0.88 | 0.00 | 0.04 | 0.00 | 0.00 | 0.00 | 0.08 | 0.88 | 0.92 | 0.76 | 1.00 | 77.2 | 0.647 | 4.661 | 13.9 |
| prompt_de a=0 | 50 | 0.00 | 0.00 | 0.00 | 0.94 | 0.00 | 0.00 | 0.06 | 0.00 | 0.00 | 0.76 | nan | 105.8 | 5.207 | 3.329 | 0.0 |
| prompt_de a=1 | 50 | 0.96 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.04 | 0.96 | 0.90 | 0.72 | 0.98 | 103.9 | 0.897 | 4.714 | 12.5 |
| prompt a=0 | 50 | 0.00 | 1.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.96 | nan | 181.1 | 5.599 | 0.111 | 0.0 |
| prompt a=1 | 50 | 0.96 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.04 | 0.96 | 0.90 | 0.96 | 1.00 | 102.9 | 0.349 | 2.250 | 8.7 |

`tok parche` es la media de posiciones que reciben el parche (con anchor goal_all, el largo de la pregunta: la perturbacion total es ese numero por v). `cambio` es la fraccion de filas cuya salida difiere de la de a=0 en la misma columna. La accuracy en salidas en espanol o aleman puede estar subestimada: los alias son ingles y frances.

## Salidas: `prompt_es`

| # | pregunta usada | a=0 [lang] | a=1 [lang] |
|---|---|---|---|
| 200 | ¿Cuál es la capital de Ucrania? | La capital de Ucrania es Kiev. [es] | La capitale de l'Ukraine est Kiev (ou Chytomir en ukrainien). [fr] |
| 201 | ¿Qué fuerza mantiene a los planetas en órbita alrededor del ... | La fuerza que mantiene a los planetas en órbita alrededor del Sol es la gravedad. [es] | C'est la gravité qui maintient les planètes dans leur orbite autour du Soleil. [fr] |
| 202 | ¿Quién escribió El viejo y el mar? | "El viejo y el mar" es una novela escrita por Ernest Hemingway, publicada en 1952. [es] | C'est un roman de Gabriel García Márquez. [es] |
| 203 | ¿Cuál es la capital de Siria? | La capital de Siria es Damasco. [es] | La capitale de la Syrie est Damascus (ou Damcheq). [fr] |
| 204 | ¿En qué año volaron por primera vez los hermanos Wright? | El 17 de diciembre de 1903. [es] | Un bon sujet! /  / Les frères Wright, Orville et Wilbur Wright, ont effectué leur premier vol en 1903. Le 17 d... [fr] |
| 205 | ¿En qué año publicó el Proyecto del Genoma Humano su primer ... | El Proyecto del Genoma Humano publicó su primer borrador en el año 2000. [es] | Le Projet du Génome Humain a publié son premier brouillon en 1970. [fr] |
| 206 | ¿Cuál es el símbolo químico de platino? | El símbolo químico de platino es Pt. [es] | Le symbole chimique du platine est Pt. [fr] |
| 207 | ¿En qué año se reunió Alemania? | La reunificación alemana se produjo en 1990. [es] | "En 1949" [unknown] |
| 208 | ¿Quién desarrolló la teoría de la selección natural junto a ... | La teoría de la selección natural fue desarrollada por Charles Darwin junto a otros científicos de su época. [es] | C'est Charles Darwin qui a développé la théorie de la sélection naturelle. [fr] |
| 209 | ¿En qué año se disolvió la Unión Soviética? | La Unión Soviética se disolvió en 1991. [unknown] | La dissolution de l'Union soviétique a eu lieu en 1991. [fr] |
| 210 | ¿Quién desarrolló la teoría de la relatividad general? | La teoría de la relatividad general fue desarrollada por Albert Einstein. [es] | C'est Albert Einstein qui a développé la théorie de la relativité générale. [fr] |
| 211 | ¿Quién pintó El Grito? | "El Grito" es una obra maestra del pintor alemán Edvard Munch, creada en 1893. Es una de las pinturas más famo... [es] | C'est Diego Velázquez qui a peint El Grito. [es] |
| 212 | ¿Cuál es la capital de Grecia? | La capital de Grecia es Atenas. [es] | Athènes est la capitale de Grèce. [fr] |
| 213 | ¿Quién escribió Cien años de soledad? | ¡Excelente pregunta! /  / La respuesta es: Gabriel García Márquez. /  / "Cien años de soledad" es una novela m... [es] | C'est Victor Hugo qui a écrit "Cien años de soledad". [fr] |
| 214 | ¿Cuál es el océano más grande de la Tierra? | El océano más grande de la Tierra es el océano Pacífico. [es] | L'océan le plus grand de la Terre est l'Océan Pacifique. [fr] |
| 215 | ¿En qué año comenzó la Segunda Guerra Mundial? | La Segunda Guerra Mundial comenzó en 1939. [es] | La Seconde Guerre mondiale a commencé en 1939. [fr] |
| 216 | ¿Cuál es el planeta más pequeño del Sistema Solar? | El planeta más pequeño del Sistema Solar es Mercurio. [es] | Le plus petit planète du système solaire est Mercure. [fr] |
| 217 | ¿Quién escribió Hamlet? | ¡Excelente pregunta! /  / El famoso drama "Hamlet" fue escrito por el gran escritor y dramaturgo inglés Willia... [es] | C'est le dramaturge danois Søren Kierkegaard, mais plus souvent attribué à William Shakespeare. [fr] |
| 218 | ¿Cuál es la galaxia más cercana y grande vecina de la Vía Lá... | La galaxia más cercana y grande vecina de la Vía Láctea es la Galaxia de Andrómeda (M31). [es] | La voie lactée est une galaxie spirale située à environ 100 000 années-lumères de nous. La galaxie la plus pro... [fr] |
| 219 | ¿Cuántas lunas tiene Marte? | Marte tiene dos lunas, Phobos y Deimos. [es] | Je suis désolé, mais je ne comprends pas. Vous avez dit "lunas" au lieu de "lunes". Si vous voulez savoir comb... [fr] |
| 220 | ¿Cuál es el símbolo químico de cromo? | El símbolo químico de cromo es Cr. [es] | Le symbole chimique du chrome est Cr. [fr] |
| 221 | ¿Quién escribió Orgullo y prejuicio? | "Orgullo y prejuicio" (título original en inglés: "Pride and Prejudice") fue escrita por la autora británica J... [es] | C'est Tony Robbins qui a écrit "L'Orgueil et la Préjugé". [fr] |
| 222 | ¿Quién recibió la patente de 1876 para el teléfono? | Alexander Graham Bell [unknown] | C'était Alexander Graham Bell. [fr] |
| 223 | ¿Cuál es el símbolo químico de zinc? | El símbolo químico de zinc es Zn. [es] | Le symbole chimique de zinc est Zn. [fr] |
| 224 | ¿Quién escribió El Príncipe pequeño? | "El Príncipe pequeño" es una obra de teatro escrita por el dramaturgo y escritor español Antonio Buero Vallejo... [es] | C'est Antoine de Saint-Exupéry qui a écrit Le Petit Prince. [fr] |
| 225 | ¿Quién compuso la Sinfonía Número 9 que contiene Oda a la Al... | La Sinfonía Número 9, también conocida como la Sinfonía de la Oda a la Alegría, fue compuesta por Ludwig van B... [es] | Je suis ravi de vous aider! /  / La Symphonie No 9 de Beethoven contient effectivement le "Ode à l'Amitié" (Od... [fr] |
| 226 | ¿Cuántas zonas horarias tiene el mundo, en cuenta estándar? | El mundo tiene 24 zonas horarias estándar, que se dividen en 24 horarios. Estas zonas horarias se utilizan par... [es] | Il y a 196 zones horaires dans le monde. [fr] |
| 227 | ¿Cuál es la capital de Qatar? | La capital de Qatar es Doha. [es] | Le capital de Qatar est Doha. [fr] |
| 228 | ¿Cuál es la capital de República Checa? | La capital de la República Checa es Praga. [es] | La capitale de la République tchèque est Prague (en tchèque : Praha). [fr] |
| 229 | ¿Cuál es la capital de Bulgaria? | La capital de Bulgaria es Sofía. [es] | La capitale de la Bulgarie est Sofia (en bulgare : София, Sofia). [fr] |
| 230 | ¿Cuántas teclas tiene un piano estándar? | Un piano estándar tiene 88 teclas. [es] | Un piano standard a 88 claviers. [unknown] |
| 231 | ¿Cuántas huesos hay en el cuerpo humano adulto? | En el cuerpo humano adulto, hay 206 huesos. [es] | Il y a environ 206 os dans le corps humain adulte. [fr] |
| 232 | ¿Cuál es el punto de congelación del agua en grados Celsius? | 0 grados Celsius [unknown] | Le point de congélation de l'eau est de 0 degrés Celsius. [fr] |
| 233 | ¿Cuál es la fórmula química del dióxido de carbono? | La fórmula química del dióxido de carbono es CO2. [es] | La fórmula chimique du dioxyde de carbone est CO2. [unknown] |
| 234 | ¿Cuál océano se encuentra entre África y Australia? | El océano que se encuentra entre África y Australia es el Océano Índico. [es] | C'est l'océan Indien. [fr] |
| 235 | ¿Cuál es la capital de China? | La capital de China es Pekín. [es] | La capitale de la Chine est Pékin (ou Beijing en anglais). [fr] |
| 236 | ¿En qué ciudad se encuentra el Taj Mahal? | El Taj Mahal se encuentra en Agra, India. [es] | Le Taj Mahal se trouve à Agra, en Inde. [fr] |
| 237 | ¿En qué año se introdujo el euro como moneda física? | El euro se introdujo como moneda física en 2002. [es] | Le euro a été adopté comme monnaie physique en 2002. [fr] |
| 238 | ¿Quién compuso la ópera Carmen? | La ópera "Carmen" fue compuesta por el compositor francés Georges Bizet. [es] | C'est Georges Bizet qui a composé l'opéra "Carmen". [fr] |
| 239 | ¿Cuál es la capital de Líbano? | La capital de Líbano es Beirut. [es] | Le capital du Liban est Beyrouth. [fr] |
| 240 | ¿Qué es el abismo más profundo del océano llamado? | El abismo más profundo del océano es el Mar de las Perlas, ubicado en el océano Pacífico, frente a las costas ... [es] | Je suis désolé, mais je ne comprends pas bien votre question. Pouvez-vous répéter ou préciser ce que vous cher... [fr] |
| 241 | ¿En qué año ocurrió el desastre del Hindenburg? | El desastre del Hindenburg ocurrió en 1937. [es] | Je m'excuse, mais je n'ai pas trouvé d'informations sur un "desastre du Hindenburg" qui aurait eu lieu en un a... [fr] |
| 242 | ¿Cuál es el símbolo químico de cloro? | El símbolo químico de cloro es Cl. [es] | Le symbole chimique du chlore est Cl. [fr] |
| 243 | ¿Cuál es la capital de Finlandia? | La capital de Finlandia es Helsinki. [es] | La capitale de la Finlande est Helsinki. [fr] |
| 244 | ¿Cuántas cámaras tiene el corazón humano? | El corazón humano tiene 4 cámaras. [es] | Le cœur humain possède 4 chambres. [fr] |
| 245 | ¿Quién fue la primera mujer a ganar un Premio Nobel? | Marie Curie fue la primera mujer en ganar un Premio Nobel. [unknown] | Marie Curie [unknown] |
| 246 | ¿Cuál es la capital de Lituania? | La capital de Lituania es Vilna. [es] | La capitale de la Lettonie est Riga. [fr] |
| 247 | ¿Cuál es la capital de Jordania? | La capital de Jordania es Amán. [es] | La capitale de la Jordanie est Amman. [fr] |
| 248 | ¿En qué año se abrió el Canal de Panamá? | El Canal de Panamá se abrió al tráfico en 1914. [es] | Le Canal de Panamá a été abroché en 1914. [fr] |
| 249 | ¿Cuál es la isla más grande del mundo? | La isla más grande del mundo es Groenlandia. [es] | La plus grande île du monde est Madagascar. [fr] |

## Salidas: `prompt_de`

| # | pregunta usada | a=0 [lang] | a=1 [lang] |
|---|---|---|---|
| 200 | Was ist die Hauptstadt der Ukraine? | Die Hauptstadt der Ukraine ist Kiew. [de] | La capitale de l'Ukraine est Kiev (ou Chykoviï en ukrainien). [fr] |
| 201 | Welche Kraft hält die Planeten in ihrer Umlaufbahn um die So... | Die Kraft, die die Planeten in ihrer Umlaufbahn um die Sonne hält, ist die Schwerkraft. Schwerkraft ist eine K... [de] | La force qui maintient les planètes dans leur orbite autour du Soleil est la gravité. Plus précisément, c'est ... [fr] |
| 202 | Wer hat "Der alte Mann und das Meer" geschrieben? | "Der alte Mann und das Meer" (Originaltitel: "The Old Man and the Sea") ist ein Roman von Ernest Hemingway, de... [de] | "Le Vieil Homme et la Mer" a été écrit par Albert Camus. [fr] |
| 203 | Was ist die Hauptstadt von Syrien? | Die Hauptstadt von Syrien ist Damaskus. [de] | La capitale de Syrie est Damas. [fr] |
| 204 | Was ist das Jahr, in dem die Wright-Brüder zum ersten Mal fl... | Das Jahr war 1903. [de] | Le premier vol du Wright-Brothers a eu lieu en 1903. [fr] |
| 205 | In welchem Jahr veröffentlichte das Human-Genom-Projekt sein... | Das Human-Genom-Projekt veröffentlichte seinen ersten Entwurf im Jahr 2000. [de] | Le Human Genome Project a publié son premier projet en 1990. [fr] |
| 206 | Was ist das chemische Symbol für Platin? | Das chemische Symbol für Platin ist Pt. [de] | Le symbole chimique du platin est Pt. [fr] |
| 207 | Was ist das Jahr der Wiedervereinigung Deutschlands? | Das Jahr der Wiedervereinigung Deutschlands ist 1990. [de] | Le 3 octobre 2022 [unknown] |
| 208 | Wer hat die Theorie der natürlichen Selektion neben Darwin e... | Die Theorie der natürlichen Selektion neben Darwin wurde von Gregor Mendel entwickelt. [de] | C'est Charles Lyell qui a développé la théorie de la sélection naturelle, non Darwin. Charles Lyell était un g... [fr] |
| 209 | Was ist das Jahr, in dem die Sowjetunion aufgelöst wurde? | Die Sowjetunion wurde 1991 aufgelöst. [de] | Je suis désolé, mais je ne comprends pas parfaitement votre question. Vous cherchez à savoir l'année où l'Unio... [fr] |
| 210 | Wer hat die Theorie der allgemeinen Relativität entwickelt? | Eine großartige Frage! /  / Die Theorie der allgemeinen Relativität wurde von Albert Einstein entwickelt. Sie ... [de] | C'est Albert Einstein qui a développé la théorie de la relativité générale. [fr] |
| 211 | Wer hat Der Schrei gemalt? | Der "Schrei" ist ein berühmtes Kunstwerk des deutschen Künstlers Edvard Munch, das 1893 entstand. Es handelt s... [de] | Je ne suis pas sûr de qui le "Crying" (ou "Der Schrei" en français) est attribué. Il y a plusieurs œuvres avec... [fr] |
| 212 | Was ist die Hauptstadt Griechenlands? | Athens [unknown] | La capitale de Grèce est Athènes (Athènes en grec, Αθήνα en grec). [fr] |
| 213 | Wer hat Hundert Jahre Einsamkeit geschrieben? | " Hundert Jahre Einsamkeit" ist ein Roman von Kate Atkinson, der 2001 veröffentlicht wurde. [de] | C'est Victor Hugo qui a écrit "Les Misérables". [fr] |
| 214 | Was ist der größte Ozean der Erde? | Der größte Ozean der Erde ist der Pazifik. [de] | Le plus grand océan de la Terre est l'Océan Pacifique. [fr] |
| 215 | Was ist das Jahr, in dem der Zweite Weltkrieg begann? | Der Zweite Weltkrieg begann 1939. [de] | Le deuxième guerre mondiale a commencé en 1939. [fr] |
| 216 | Welcher Planet im Sonnensystem ist der kleinst? | Der kleinste Planet im Sonnensystem ist Merkur. [de] | Mercure est le plus petit planète du système solaire. [fr] |
| 217 | Wer hat Hamlet geschrieben? | Ein klassisches Thema! /  / Der Autor von Hamlet ist der dänische Schriftsteller und Dramatiker William Shakes... [de] | Le personnage de Hamlet a été créé par le dramaturge danois et polonais Søren Kierkegaard, mais le texte de la... [fr] |
| 218 | Welche Galaxie ist die nächste große Nachbarin der Milchstra... | Die nächste große Nachbarin der Milchstraße ist die Andromeda-Galaxie. [de] | La galaxie la plus proche de la Voie lactée est la galaxie d'Andromède, également connue sous le nom de M31. [fr] |
| 219 | Wie viele Monde hat der Mars? | Der Mars hat zwei Monde: /  / 1. Phobos / 2. Deimos [de] | Le Mars a un monde, appelé Phobos. [fr] |
| 220 | Was ist das chemische Symbolzeichen für Chrom? | Das chemische Symbol für Chrom ist Cr. [de] | Le symbole chimique du chrome est Cr. [fr] |
| 221 | Wer hat Romantik geschrieben? | Eine großartige Frage! /  / Es gibt viele Autoren, die Romantik geschrieben haben. Hier sind einige der bekann... [de] | C'est Victor Hugo qui a écrit le romantisme. [fr] |
| 222 | Wer erhielt 1876 das Patent für das Telefon? | Alexander Graham Bell [unknown] | Alexander Graham Bell [unknown] |
| 223 | Was ist das chemische Symbol für Zink? | Das chemische Symbol für Zink ist Zn. [de] | Le symbole chimique du zinc est Zn. [fr] |
| 224 | Wer hat "Der kleine Prinz" geschrieben? | Ein Klassiker! /  / "Der kleine Prinz" (französisch: "Le Petit Prince") wurde von dem französischen Schriftste... [de] | C'est Albert Camus qui a écrit "Le Petit Prince". [fr] |
| 225 | Wer hat die Neunte Sinfonie mit der Ode an die Freude kompon... | Die Neunte Sinfonie mit der Ode an die Freude komponierte Ludwig van Beethoven. [de] | C'est Ludwig van Beethoven qui a composé la 9e Symphonie avec l'Ode à la Joie. [fr] |
| 226 | Wie viele Zeitzonen hat die Welt, wenn man sie auf standardm... | Die Welt hat 24 Zeitzonen, wenn man sie auf standardmäßige Weise zählt. Diese Zeitzonen werden von der Interna... [de] | Je pense que vous voulez dire "Quel est le nombre de zones horaires que le monde a, si on les compte sur une é... [fr] |
| 227 | Was ist die Hauptstadt von Katar? | Die Hauptstadt von Katar ist Doha. [de] | Le capital du Qatar est Doha. [fr] |
| 228 | Was ist die Hauptstadt von Tschechien? | Die Hauptstadt von Tschechien ist Prag. [de] | La capitale de la République tchèque est Prague (en tchèque : Praha). [fr] |
| 229 | Was ist die Hauptstadt von Bulgarien? | Die Hauptstadt von Bulgarien ist Sofia. [de] | La capitale de Bulgarie est Sofia. [fr] |
| 230 | Wie viele Tasten hat ein Standardpiano? | Ein Standardpiano hat typischerweise 88 Tasten. Davon sind 52 weiße Tasten (C3 bis C7) und 36 schwarze Tasten ... [de] | Un piano standard possède 88 doigts. [fr] |
| 231 | Wie viele Knochen hat der erwachsene menschliche Körper? | Der erwachsene menschliche Körper besteht aus 206 Knochen. [de] | Vous voulez savoir combien de os le corps humain a développé? /  / Un adulte humain a environ 206 os. Cependan... [fr] |
| 232 | Was ist der Gefrierpunkt des Wassers in Grad Celsius? | Der Gefrierpunkt des Wassers beträgt 0 Grad Celsius. [de] | Le point de gelage de l'eau est de 0°C. [fr] |
| 233 | Was ist die chemische Formel für Kohlendioxid? | Die chemische Formel für Kohlendioxid ist CO2. [de] | La formule chimique du carbone disulfure est CO. /  / Mais je pense que vous faites référence au carbone disul... [fr] |
| 234 | Welcher Ozean liegt zwischen Afrika und Australien? | Der Indische Ozean liegt zwischen Afrika und Australien. [de] | C'est l'Océan Indien. [fr] |
| 235 | Was ist die Hauptstadt von China? | Die Hauptstadt von China ist Peking (offiziell: Pekin). [de] | La capitale de la Chine est Pékin (ou Beijing en chinois). [fr] |
| 236 | In welcher Stadt befindet sich das Taj Mahal? | Das Taj Mahal befindet sich in Agra, Indien. [de] | Le Taj Mahal se trouve à Agra, en Inde. [fr] |
| 237 | In welchem Jahr wurde der Euro als physische Währung eingefü... | Der Euro wurde 2002 als physische Währung eingeführt. [de] | Le Euro a été mis en circulation en 1999. [fr] |
| 238 | Wer komponierte die Oper Carmen? | Eine klassische Frage! /  / Die Oper "Carmen" wurde von dem spanischen Komponisten Georges Bizet komponiert. S... [de] | C'est Georges Bizet qui a composé l'opéra "Carmen". [fr] |
| 239 | Was ist die Hauptstadt von Libanon? | Die Hauptstadt des Libanon ist Beirut. [de] | Le Liban n'a pas de capitale. Cependant, la capitale du Liban est Beyrouth. [fr] |
| 240 | Wie heißt der tiefste Tiefseegraben? | Der tiefste Tiefseegraben heißt Mariana-Trench-Graben. [de] | Je suis désolé, mais je n'ai pas compris votre question. Vous avez demandé la profondeur du Tiefseegraben le p... [fr] |
| 241 | Was ist das Jahr des Hindenburg-Unfalls? | Der Hindenburg-Unfall ereignete sich am 6. Mai 1937. [de] | Je pense que vous faites référence à l'année du rétablissement de la monarchie en Allemagne après la fin de la... [fr] |
| 242 | Was ist das chemische Symbolzeichen für Chlor? | Das chemische Symbolzeichen für Chlor ist Cl. [de] | Le symbole chimique du chlore est Cl. [fr] |
| 243 | Was ist die Hauptstadt von Finnland? | Die Hauptstadt von Finnland ist Helsinki. [de] | La capitale du Finland est Helsinki. [fr] |
| 244 | Wie viele Kammern hat das menschliche Herz? | Das menschliche Herz besteht aus vier Kammern. Diese Kammern sind: /  / 1.  **Rechtsh Herzkammer (Rechtsherzka... [de] | Le cœur humain a quatre chambres. [fr] |
| 245 | Wer war die erste Frau, die einen Nobelpreis gewann? | Die erste Frau, die einen Nobelpreis gewann, war Marie Curie. Sie erhielt den Nobelpreis für Physik im Jahr 19... [de] | C'était Marie Curie. Elle a remporté deux prix Nobel : en 1903 avec Pierre Curie et en 1911 pour ses recherche... [fr] |
| 246 | Was ist die Hauptstadt von Litauen? | Die Hauptstadt von Litauen ist Vilnius. [de] | La capitale de Lituanie est Vilnius. [fr] |
| 247 | Was ist die Hauptstadt von Jordanien? | Amman [unknown] | La capitale du Jordanie est Amman. [fr] |
| 248 | Was ist das Jahr, in dem der Panama-Kanal eröffnet wurde? | Der Panama-Kanal wurde 1914 eröffnet. [de] | Le Panama Canal a été ouvert en 1914. [fr] |
| 249 | Welche ist die größte Insel der Welt? | Die größte Insel der Welt ist Grönland. [de] | La plus grande île du monde est Groenland. [fr] |

## Salidas: `prompt`

| # | pregunta usada | a=0 [lang] | a=1 [lang] |
|---|---|---|---|
| 200 | What is the capital of Ukraine? | The capital of Ukraine is Kyiv (also known as Kiev). [en] | La capitale de l'Ukraine est Kiev (ou Chytomir en ukrainien). [fr] |
| 201 | What force keeps planets in orbit around the Sun? | The force that keeps planets in orbit around the Sun is called gravity. Specifically, it's the gravitational f... [en] | C'est la force de gravité! La gravité est une force fondamentale de la physique qui attire les objets avec une... [fr] |
| 202 | Who wrote The Old Man and the Sea? | The Old Man and the Sea is a novella written by the renowned American author Ernest Hemingway. It was first pu... [en] | C'est Ernest Hemingway qui a écrit "L'Homme qui faisait la mer" (The Old Man and the Sea en anglais). [unknown] |
| 203 | What is the capital of Syria? | The capital of Syria is Damascus. [en] | La capitale de Syrie est Damas. [fr] |
| 204 | In what year did the Wright brothers first fly? | The Wright brothers, Orville and Wilbur, successfully flew the first powered, heavier-than-air aircraft on Dec... [en] | Une excellente question! /  / Les frères Wright ont effectué leur premier vol réussi le 17 décembre 1903. C'es... [fr] |
| 205 | In what year did the Human Genome Project publish its first ... | The Human Genome Project published its first draft in 2000. [en] | Le projet du génome humain a publié sa première édition de prélèvement en 2000. [fr] |
| 206 | What is the chemical symbol for platinum? | The chemical symbol for platinum is Pt. [en] | Le symbole chimique du platine est Pt. [fr] |
| 207 | In what year did Germany reunify? | Germany reunified on October 3, 1990. This was the day when East Germany (GDR) and West Germany (FRG) were off... [en] | La réunification de l'Allemagne a eu lieu en 1990. [fr] |
| 208 | Who developed the theory of natural selection alongside Darw... | While Charles Darwin is often credited with developing the theory of natural selection, he didn't work alone. ... [en] | C'est Alfred Russel Wallace qui a développé, en même temps que Charles Darwin, la théorie de la sélection natu... [fr] |
| 209 | In what year did the Soviet Union dissolve? | The Soviet Union dissolved in 1991. Specifically, it was officially dissolved on December 26, 1991, when the S... [en] | La dissolution de l'Union soviétique a eu lieu en 1991. Plus précisément, le 26 décembre 1991, le président Mi... [fr] |
| 210 | Who developed the theory of general relativity? | The theory of general relativity was developed by Albert Einstein. He published his groundbreaking work, "Theo... [en] | C'est Albert Einstein qui a développé la théorie de la relativité générale. [fr] |
| 211 | Who painted The Scream? | The painting "The Scream" was created by the Norwegian artist Edvard Munch in 1893. It's one of his most famou... [en] | C'est Edvard Munch qui a peint "La Scream" (ou "Le Scream" en français). Il s'agit d'une œuvre emblématique du... [fr] |
| 212 | What is the capital of Greece? | The capital of Greece is Athens. [en] | La capitale de Grèce est Athènes (Athína en grec). [fr] |
| 213 | Who wrote One Hundred Years of Solitude? | A classic of magical realism! /  / "One Hundred Years of Solitude" was written by the Colombian author Gabriel... [en] | Gabriel García Márquez a écrit "One Hundred Years of Solitude" (Les Cent Ans de Solitude en français). [unknown] |
| 214 | What is the largest ocean on Earth? | The largest ocean on Earth is the Pacific Ocean, which covers approximately 155.6 million square kilometers (6... [en] | L'océan le plus grand de la Terre est l'Océan Pacifique. Il s'étend sur plus de 155 millions de kilomètres car... [fr] |
| 215 | In what year did World War II begin? | World War II began in 1939. Specifically, it started on September 1, 1939, when Nazi Germany, led by Adolf Hit... [en] | La Seconde Guerre mondiale a commencé en 1939. [fr] |
| 216 | Which is the smallest planet in the Solar System? | The smallest planet in our Solar System is Mercury. It has a diameter of approximately 4,879 kilometers (3,031... [en] | Le plus petit planète du système solaire est Mercure. [fr] |
| 217 | Who wrote Hamlet? | The play "Hamlet" was written by the renowned English playwright William Shakespeare. It is one of his most fa... [en] | C'est William Shakespeare qui a écrit Hamlet. [fr] |
| 218 | Which galaxy is the nearest large neighbour to the Milky Way... | The nearest large neighbor to the Milky Way galaxy is the Andromeda Galaxy, also known as Messier 31 (M31) or ... [en] | La galaxie la plus proche voisine de la Voie lactée est la galaxie d'Andromède, également connue sous le nom d... [fr] |
| 219 | How many moons does Mars have? | Mars has two small natural satellites, or moons. Their names are Phobos and Deimos. [en] | Mars, le planète la plus proche du Soleil de notre système solaire, a deux lunes connues : Phobos et Deimos. [fr] |
| 220 | What is the chemical symbol for chromium? | The chemical symbol for Chromium is Cr. [en] | Le symbole chimique du chromium est Cr. [fr] |
| 221 | Who wrote Pride and Prejudice? | A classic question! /  / Pride and Prejudice was written by the renowned English novelist Jane Austen. The nov... [en] | C'est Jane Austen qui a écrit "Pride and Prejudice"! [fr] |
| 222 | Who received the 1876 patent for the telephone? | Alexander Graham Bell received the 1876 patent for the telephone. [en] | C'est Alexander Graham Bell qui a reçu le brevet en 1876 pour le téléphone. [fr] |
| 223 | What is the chemical symbol for zinc? | The chemical symbol for zinc is Zn. [en] | Le symbole chimique du zinc est Zn. [fr] |
| 224 | Who wrote The Little Prince? | The Little Prince (French title: Le Petit Prince) was written by Antoine de Saint-Exupéry, a French author, po... [en] | C'est Antoine de Saint-Exupéry qui a écrit "Le Petit Prince". [fr] |
| 225 | Who composed the Ninth Symphony containing Ode to Joy? | The Ninth Symphony, also known as the "Choral Symphony," was composed by Ludwig van Beethoven. It is one of hi... [en] | L'œuvre que vous faites référence est la Symphonie n° 9 de Ludwig van Beethoven, également connue sous le titr... [fr] |
| 226 | How many time zones does the world have, in standard count? | The world has 24 time zones in standard count. These time zones are identified by their offset from Coordinate... [en] | Bonjour! /  / Le monde a actuellement 24 zones horaires principales, également appelées zones horaires standar... [fr] |
| 227 | What is the capital of Qatar? | The capital of Qatar is Doha. [en] | La capitale du Qatar est Doha. [fr] |
| 228 | What is the capital of Czechia? | The capital of Czechia is Prague (Praha in Czech). [en] | La capitale de la République tchèque est Prague (en tchèque : Praha). [fr] |
| 229 | What is the capital of Bulgaria? | The capital of Bulgaria is Sofia (София). [en] | La capitale de Bulgarie est Sofia (ou Skopje en Macédoine du Nord, mais Sofia est la capitale de Bulgarie). [fr] |
| 230 | How many keys does a standard piano have? | A standard piano typically has 88 keys. This includes: /  / * 52 white keys (also known as naturals) / * 36 bl... [en] | Un piano standard a généralement 88 claviers. [fr] |
| 231 | How many bones are in the adult human body? | There are 206 bones in the adult human body. This number can vary slightly from person to person, as some indi... [en] | Il y a 206 os dans le corps humain adulte. [fr] |
| 232 | What is the freezing point of water in degrees Celsius? | The freezing point of water is 0 degrees Celsius (°C). [en] | Le point de gel de l'eau est de 0 degrés Celsius. [fr] |
| 233 | What is the chemical formula for carbon dioxide? | The chemical formula for carbon dioxide is CO2. [en] | La formule chimique du dioxyde de carbone est CO₂. [fr] |
| 234 | Which ocean lies between Africa and Australia? | The Indian Ocean lies between Africa and Australia. [en] | L'océan qui se trouve entre l'Afrique et l'Australie est l'Océan Indien. [fr] |
| 235 | What is the capital of China? | The capital of China is Beijing. [en] | La capitale de la Chine est Pékin (peut-être tu veux dire Pékine?). [fr] |
| 236 | In which city is the Taj Mahal located? | The Taj Mahal is located in Agra, India. [en] | Le Taj Mahal est situé à Agra, en Inde. [fr] |
| 237 | In what year was the euro introduced as physical currency? | The euro was introduced as physical currency in 2002. The first euro coins were minted in 2001, but they were ... [en] | Le euro a été introduit comme monnaie physique en 2002. [fr] |
| 238 | Who composed the opera Carmen? | The opera "Carmen" was composed by Georges Bizet. [en] | Georges Bizet a composé l'opéra "Carmen". [fr] |
| 239 | What is the capital of Lebanon? | The capital of Lebanon is Beirut. [en] | Le capital du Liban est Beyrouth. [fr] |
| 240 | What is the deepest ocean trench called? | The deepest ocean trench is called the Mariana Trench. Specifically, the lowest point in the trench is called ... [en] | Le plus profond abîme océanique est le Trench du Chili, également connu sous le nom de Trench de la Mer de Tas... [fr] |
| 241 | In what year did the Hindenburg disaster occur? | The Hindenburg disaster occurred on May 6, 1937. [en] | L'incident du Hindenburg, également connu sous le nom de catastrophe du Hindenburg, a eu lieu en 1937. Le 6 ma... [fr] |
| 242 | What is the chemical symbol for chlorine? | The chemical symbol for chlorine is Cl. [en] | Le symbole chimique du chlore est Cl. [fr] |
| 243 | What is the capital of Finland? | The capital of Finland is Helsinki. [en] | La capitale de la Finlande est Helsinki. [fr] |
| 244 | How many chambers does the human heart have? | The human heart has 4 chambers: /  / 1. **Right Atrium** (upper right chamber) / 2. **Right Ventricle** (lower... [en] | Le cœur humain a 4 chambres. [fr] |
| 245 | Who was the first woman to win a Nobel Prize? | Marie Curie was the first woman to win a Nobel Prize, and she won two Nobel Prizes in different fields. She wa... [en] | Marie Curie a été la première femme à recevoir un Nobel. Elle a remporté deux prix Nobel : en 1903 avec Pierre... [fr] |
| 246 | What is the capital of Lithuania? | The capital of Lithuania is Vilnius. [en] | La capitale de Lituanie est Vilnius. [fr] |
| 247 | What is the capital of Jordan? | The capital of Jordan is Amman. [en] | La capitale de Jordanie est Amman. [fr] |
| 248 | In what year was the Panama Canal opened? | The Panama Canal was opened on August 15, 1914. [en] | Le canal de Panama a été ouvert en 1914. [fr] |
| 249 | Which is the largest island in the world? | The largest island in the world is Greenland, which is an autonomous territory within the Kingdom of Denmark. ... [en] | L'île la plus grande du monde est Groenland, qui fait partie du Groenland du Danemark. Cependant, si l'on cons... [fr] |

