# Parche de idioma: signo e idioma de entrada (preset `idioma`)

- Parche: `/mnt/custom-file-systems/efs/fs-0ded2930a619aa967_fsap-0faa05c681ed1a8f3/papers/LLMAtaquesContinuos/experimentos/idiomas/runs/v4_250/lang_patch_best_train.pt`  |  norma 0.8021
- Tail del held-out: n=50

| condicion | n | fr | en | es | de | unk | is_french | starts_fr | acc | cambio vs a=0 | largo | CE fr head | CE en head |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| prompt_es a=0 | 50 | 0.00 | 0.00 | 0.92 | 0.00 | 0.08 | 0.00 | 0.48 | 0.80 | nan | 70.6 | 4.677 | 2.490 |
| prompt_es a=1 | 50 | 0.00 | 0.00 | 0.88 | 0.00 | 0.12 | 0.00 | 0.38 | 0.80 | 0.46 | 54.9 | 4.077 | 2.741 |
| prompt_de a=0 | 50 | 0.00 | 0.00 | 0.00 | 0.88 | 0.12 | 0.00 | 0.00 | 0.82 | nan | 92.5 | 5.204 | 2.950 |
| prompt_de a=1 | 50 | 0.02 | 0.00 | 0.00 | 0.82 | 0.16 | 0.02 | 0.02 | 0.76 | 0.66 | 69.6 | 4.962 | 3.826 |
| prompt a=0 | 50 | 0.00 | 0.88 | 0.00 | 0.00 | 0.12 | 0.00 | 0.00 | 0.96 | nan | 150.5 | 5.725 | 0.097 |
| prompt a=1 | 50 | 0.90 | 0.04 | 0.00 | 0.00 | 0.06 | 0.90 | 0.88 | 0.94 | 1.00 | 81.3 | 0.507 | 3.959 |

`cambio` es la fraccion de filas cuya salida difiere de la de a=0 en la misma columna. La accuracy en salidas en espanol o aleman puede estar subestimada: los alias son ingles y frances.

## Salidas: `prompt_es`

| # | pregunta usada | a=0 [lang] | a=1 [lang] |
|---|---|---|---|
| 200 | ¿Cuál es la capital de Ucrania? | La capital de Ucrania es Kiev. [es] | La capital de Ucrania es Kiev. [es] |
| 201 | ¿Qué fuerza mantiene a los planetas en órbita alrededor del ... | La fuerza que mantiene a los planetas en órbita alrededor del Sol es la gravedad. [es] | La fuerza que mantiene a los planetas en órbita alrededor del Sol es la gravedad. La gravedad es una fuerza de... [es] |
| 202 | ¿Cuál es 15 más 6? | La respuesta es 21. [es] | El resultado de 15 más 6 es 21. [es] |
| 203 | ¿Cuál es la capital de Siria? | La capital de Siria es Damasco. [es] | La capital de Siria es Damasco. [es] |
| 204 | ¿En qué año volaron por primera vez los hermanos Wright? | El 17 de diciembre de 1903. [es] | En 1903 [unknown] |
| 205 | ¿En qué año publicó el Proyecto del Genoma Humano su primer ... | El Proyecto del Genoma Humano publicó su primer borrador en el año 2000. [es] | El Proyecto del Genoma Humano publicó su primer borrador en el año 2000. [es] |
| 206 | ¿Cuál es el símbolo químico de platino? | El símbolo químico de platino es Pt. [es] | El símbolo químico de platino es Pt. [es] |
| 207 | ¿En qué año se reunió Alemania? | La reunificación alemana se produjo en 1990. [es] | Alemania se reunió en 1990. [es] |
| 208 | ¿Quién desarrolló la teoría de la selección natural junto a ... | La teoría de la selección natural fue desarrollada por Charles Darwin junto a otros científicos de su época. [es] | Charles Robert Darwin [unknown] |
| 209 | ¿Cuál es siete veces ocho? | Siete veces ocho es 56. [es] | La respuesta a la pregunta "¿Cuál es siete veces ocho?" es 56. [es] |
| 210 | ¿Quién desarrolló la teoría de la relatividad general? | La teoría de la relatividad general fue desarrollada por Albert Einstein. [es] | La teoría de la relatividad general fue desarrollada por el físico alemán Albert Einstein. [es] |
| 211 | ¿Quién pintó El Grito? | "El Grito" es una obra maestra del pintor alemán Edvard Munch, creada en 1893. Es una de las pinturas más famo... [es] | "El Grito" es una obra maestra del pintor español José de Ribera, también conocido como el "Ribera de los Borb... [es] |
| 212 | ¿Cuál es la capital de Grecia? | La capital de Grecia es Atenas. [es] | Atenas es la capital de Grecia. [es] |
| 213 | ¿Quién escribió Cien años de soledad? | ¡Excelente pregunta! /  / La respuesta es: Gabriel García Márquez. /  / "Cien años de soledad" es una novela m... [es] | Gabriel García Márquez. [es] |
| 214 | ¿Cuál es el océano más grande de la Tierra? | El océano más grande de la Tierra es el océano Pacífico. [es] | El océano más grande de la Tierra es el océano Pacífico. [es] |
| 215 | ¿En qué año comenzó la Segunda Guerra Mundial? | La Segunda Guerra Mundial comenzó en 1939. [es] | La Segunda Guerra Mundial comenzó en 1939. [es] |
| 216 | ¿Cuál es 17 multiplicado por 2? | El resultado de 17 multiplicado por 2 es 34. [es] | El resultado de 17 multiplicado por 2 es 34. [es] |
| 217 | ¿Quién escribió Hamlet? | ¡Excelente pregunta! /  / El famoso drama "Hamlet" fue escrito por el gran escritor y dramaturgo inglés Willia... [es] | William Shakespeare. [unknown] |
| 218 | ¿Cuál es la galaxia más cercana y grande vecina de la Vía Lá... | La galaxia más cercana y grande vecina de la Vía Láctea es la Galaxia de Andrómeda (M31). [es] | La galaxia más cercana y grande vecina de la Vía Láctea es la Galaxia de Andrómeda (M31). [es] |
| 219 | ¿Cuántas lunas tiene Marte? | Marte tiene dos lunas, Phobos y Deimos. [es] | Marte tiene dos lunas. [es] |
| 220 | ¿Cuál es el símbolo químico de cromo? | El símbolo químico de cromo es Cr. [es] | El símbolo químico de cromo es Cr. [es] |
| 221 | ¿Cuál es 9 más 9? | 9 + 9 = 18 [unknown] | El resultado de 9 más 9 es 18. [es] |
| 222 | ¿Quién recibió la patente de 1876 para el teléfono? | Alexander Graham Bell [unknown] | Alexander Graham Bell. [unknown] |
| 223 | ¿Cuál es el símbolo químico de zinc? | El símbolo químico de zinc es Zn. [es] | El símbolo químico de zinc es Zn. [es] |
| 224 | ¿Cuál es 25 más 4? | La respuesta es 29. [es] | La respuesta a la pregunta es 29. [es] |
| 225 | ¿Quién compuso la Sinfonía Número 9 que contiene Oda a la Al... | La Sinfonía Número 9, también conocida como la Sinfonía de la Oda a la Alegría, fue compuesta por Ludwig van B... [es] | La Sinfonía Número 9 que contiene Oda a la Alegría fue compuesta por Ludwig van Beethoven. [es] |
| 226 | ¿Cuántas zonas horarias tiene el mundo, en cuenta estándar? | El mundo tiene 24 zonas horarias estándar, que se dividen en 24 horarios. Estas zonas horarias se utilizan par... [es] | Hasta mi última actualización en abril de 2023, el mundo está dividido en 24 zonas horarias estándar, cada una... [es] |
| 227 | ¿Cuál es la capital de Qatar? | La capital de Qatar es Doha. [es] | La capital de Qatar es Doha. [es] |
| 228 | ¿Cuál es la capital de República Checa? | La capital de la República Checa es Praga. [es] | La capital de la República Checa es Praga. [es] |
| 229 | ¿Cuál es la capital de Bulgaria? | La capital de Bulgaria es Sofía. [es] | Sofía es la capital de Bulgaria. [es] |
| 230 | ¿Cuántas teclas tiene un piano estándar? | Un piano estándar tiene 88 teclas. [es] | Un piano estándar tiene 88 teclas. [es] |
| 231 | ¿Cuántas huesos hay en el cuerpo humano adulto? | En el cuerpo humano adulto, hay 206 huesos. [es] | En el cuerpo humano adulto, hay 206 huesos. [es] |
| 232 | ¿Cuál es el punto de congelación del agua en grados Celsius? | 0 grados Celsius [unknown] | El punto de congelación del agua es de 0 grados Celsius. [es] |
| 233 | ¿Cuál es la fórmula química del dióxido de carbono? | La fórmula química del dióxido de carbono es CO2. [es] | La fórmula química del dióxido de carbono es CO2. [es] |
| 234 | ¿Cuál océano se encuentra entre África y Australia? | El océano que se encuentra entre África y Australia es el Océano Índico. [es] | El océano que se encuentra entre África y Australia es el Océano Índico. [es] |
| 235 | ¿Cuál es la capital de China? | La capital de China es Pekín. [es] | La capital de China es Pekín. [es] |
| 236 | ¿En qué ciudad se encuentra el Taj Mahal? | El Taj Mahal se encuentra en Agra, India. [es] | El Taj Mahal se encuentra en Agra, India. [es] |
| 237 | ¿En qué año se introdujo el euro como moneda física? | El euro se introdujo como moneda física en 2002. [es] | El euro se introdujo como moneda física en 2002. [es] |
| 238 | ¿Quién compuso la ópera Carmen? | La ópera "Carmen" fue compuesta por el compositor francés Georges Bizet. [es] | Georges Bizet. [unknown] |
| 239 | ¿Cuál es la capital de Líbano? | La capital de Líbano es Beirut. [es] | La capital de Líbano es Beirut. [es] |
| 240 | ¿Qué es el abismo más profundo del océano llamado? | El abismo más profundo del océano es el Mar de las Perlas, ubicado en el océano Pacífico, frente a las costas ... [es] | El abismo más profundo del océano se llama Mariana. [es] |
| 241 | ¿En qué año ocurrió el desastre del Hindenburg? | El desastre del Hindenburg ocurrió en 1937. [es] | El desastre del Hindenburg ocurrió en 1937. [es] |
| 242 | ¿Cuál es el símbolo químico de cloro? | El símbolo químico de cloro es Cl. [es] | El símbolo químico de cloro es Cl. [es] |
| 243 | ¿Cuál es la capital de Finlandia? | La capital de Finlandia es Helsinki. [es] | Helsinki es la capital de Finlandia. [es] |
| 244 | ¿Cuántas cámaras tiene el corazón humano? | El corazón humano tiene 4 cámaras. [es] | El corazón humano tiene 4 cámaras. [es] |
| 245 | ¿Quién fue la primera mujer a ganar un Premio Nobel? | Marie Curie fue la primera mujer en ganar un Premio Nobel. [unknown] | Marie Curie fue la primera mujer en ganar un Premio Nobel. [unknown] |
| 246 | ¿Cuál es la capital de Lituania? | La capital de Lituania es Vilna. [es] | La capital de Lituania es Vilna. [es] |
| 247 | ¿Cuál es la capital de Jordania? | La capital de Jordania es Amán. [es] | La capital de Jordania es Amán. [es] |
| 248 | ¿En qué año se abrió el Canal de Panamá? | El Canal de Panamá se abrió al tráfico en 1914. [es] | El Canal de Panamá se abrió en el año 1914. [es] |
| 249 | ¿Cuál es el resultado de multiplicar 25 por 4? | El resultado de multiplicar 25 por 4 es 100. [es] | El resultado de multiplicar 25 por 4 es 100. [es] |

## Salidas: `prompt_de`

| # | pregunta usada | a=0 [lang] | a=1 [lang] |
|---|---|---|---|
| 200 | Was ist die Hauptstadt der Ukraine? | Die Hauptstadt der Ukraine ist Kiew. [de] | Kiew (ukrainisch: Київ) ist die Hauptstadt der Ukraine. [de] |
| 201 | Welche Kraft hält die Planeten in ihrer Umlaufbahn um die So... | Die Kraft, die die Planeten in ihrer Umlaufbahn um die Sonne hält, ist die Schwerkraft. Schwerkraft ist eine K... [de] | Die Kraft, die die Planeten in ihrer Umlaufbahn um die Sonne hält, ist die Schwerkraft. Schwerkraft ist eine K... [de] |
| 202 | Was ist 15 plus 6? | 15 plus 6 ist 21. [unknown] | 15 plus 6 ist 21. [unknown] |
| 203 | Was ist die Hauptstadt von Syrien? | Die Hauptstadt von Syrien ist Damaskus. [de] | Die Hauptstadt von Syrien ist Damaskus. [de] |
| 204 | Was ist das Jahr, in dem die Wright-Brüder zum ersten Mal fl... | Das Jahr war 1903. [de] | Das war 1903. [unknown] |
| 205 | In welchem Jahr veröffentlichte das Human-Genom-Projekt sein... | Das Human-Genom-Projekt veröffentlichte seinen ersten Entwurf im Jahr 2000. [de] | 2000 [unknown] |
| 206 | Was ist das chemische Symbol für Platin? | Das chemische Symbol für Platin ist Pt. [de] | Das chemische Symbol für Platin ist Pt. [de] |
| 207 | Was ist das Jahr der Wiedervereinigung Deutschlands? | Das Jahr der Wiedervereinigung Deutschlands ist 1990. [de] | Das Jahr der Wiedervereinigung Deutschlands war 1990. [de] |
| 208 | Wer hat die Theorie der natürlichen Selektion neben Darwin e... | Die Theorie der natürlichen Selektion neben Darwin wurde von Gregor Mendel entwickelt. [de] | Die Theorie der natürlichen Selektion entwickelte Charles Darwin. [de] |
| 209 | Was ist 7 mal 8? | Das ist eine einfache Frage! /  / 7 mal 8 ist gleich 56. [de] | Die Zahl 7 mal 8 ist 56. [de] |
| 210 | Wer hat die Theorie der allgemeinen Relativität entwickelt? | Eine großartige Frage! /  / Die Theorie der allgemeinen Relativität wurde von Albert Einstein entwickelt. Sie ... [de] | Die Theorie der allgemeinen Relativität wurde von Albert Einstein entwickelt. [de] |
| 211 | Wer hat Der Schrei gemalt? | Der "Schrei" ist ein berühmtes Kunstwerk des deutschen Künstlers Edvard Munch, das 1893 entstand. Es handelt s... [de] | Eine Frage nach Kunst! /  / Der Schrei ist ein bekanntes Gemälde des deutschen Künstlers Edvard Munch, das 189... [de] |
| 212 | Was ist die Hauptstadt Griechenlands? | Athens [unknown] | Athens (griechisch: Αθήνα, Athína) ist die Hauptstadt Griechenlands. [unknown] |
| 213 | Wer hat Hundert Jahre Einsamkeit geschrieben? | " Hundert Jahre Einsamkeit" ist ein Roman von Kate Atkinson, der 2001 veröffentlicht wurde. [de] | Ein klassischer Literaturbezug! /  / Die Antwort ist: "Hundert Jahre Einsamkeit" (Originaltitel: "One Hundred ... [de] |
| 214 | Was ist der größte Ozean der Erde? | Der größte Ozean der Erde ist der Pazifik. [de] | Der Pazifik ist der größte Ozean der Erde. [de] |
| 215 | Was ist das Jahr, in dem der Zweite Weltkrieg begann? | Der Zweite Weltkrieg begann 1939. [de] | Das Jahr, in dem der Zweite Weltkrieg begann, war 1939. [de] |
| 216 | Was ist 17 mal 2? | Das ist eine einfache Frage! /  / 17 mal 2 ist gleich 34. [de] | Das ist eine einfache Rechnung! /  / 17 mal 2 = 34 [de] |
| 217 | Wer hat Hamlet geschrieben? | Ein klassisches Thema! /  / Der Autor von Hamlet ist der dänische Schriftsteller und Dramatiker William Shakes... [de] | Hamlet ist ein Schauspiel von William Shakespeare. [de] |
| 218 | Welche Galaxie ist die nächste große Nachbarin der Milchstra... | Die nächste große Nachbarin der Milchstraße ist die Andromeda-Galaxie. [de] | Die nächste große Nachbarin der Milchstraße ist Canis Major. [de] |
| 219 | Wie viele Monde hat der Mars? | Der Mars hat zwei Monde: /  / 1. Phobos / 2. Deimos [de] | Le Mars, comme les autres planètes du Système solaire, est un monde rocheux avec une atmosphère très faible. I... [fr] |
| 220 | Was ist das chemische Symbolzeichen für Chrom? | Das chemische Symbol für Chrom ist Cr. [de] | Das chemische Symbol für Chrom ist Cr. [de] |
| 221 | Was ist 9 plus 9? | Das ist eine einfache Frage! /  / 9 + 9 = 18 [de] | 9 plus 9 ist 18. [unknown] |
| 222 | Wer erhielt 1876 das Patent für das Telefon? | Alexander Graham Bell [unknown] | Alexander Graham Bell [unknown] |
| 223 | Was ist das chemische Symbol für Zink? | Das chemische Symbol für Zink ist Zn. [de] | Das chemische Symbol für Zink ist Zn. [de] |
| 224 | Was ist 25 plus 4? | 25 plus 4 ist 29. [unknown] | 25 plus 4 ist 29. [unknown] |
| 225 | Wer hat die Neunte Sinfonie mit der Ode an die Freude kompon... | Die Neunte Sinfonie mit der Ode an die Freude komponierte Ludwig van Beethoven. [de] | Ludwig van Beethoven hat die Neunte Sinfonie mit der Ode an die Freude komponiert. [de] |
| 226 | Wie viele Zeitzonen hat die Welt, wenn man sie auf standardm... | Die Welt hat 24 Zeitzonen, wenn man sie auf standardmäßige Weise zählt. Diese Zeitzonen werden von der Interna... [de] | Die Welt hat 4 Zeitzonen. [de] |
| 227 | Was ist die Hauptstadt von Katar? | Die Hauptstadt von Katar ist Doha. [de] | Die Hauptstadt von Katar ist Doha. [de] |
| 228 | Was ist die Hauptstadt von Tschechien? | Die Hauptstadt von Tschechien ist Prag. [de] | Prag ist die Hauptstadt der Tschechischen Republik. [de] |
| 229 | Was ist die Hauptstadt von Bulgarien? | Die Hauptstadt von Bulgarien ist Sofia. [de] | Die Hauptstadt von Bulgarien ist Sofia (bulgarisch: София, Sofia). [de] |
| 230 | Wie viele Tasten hat ein Standardpiano? | Ein Standardpiano hat typischerweise 88 Tasten. Davon sind 52 weiße Tasten (C3 bis C7) und 36 schwarze Tasten ... [de] | Ein Standardpiano hat 88 Tasten. [de] |
| 231 | Wie viele Knochen hat der erwachsene menschliche Körper? | Der erwachsene menschliche Körper besteht aus 206 Knochen. [de] | Der erwachsene menschliche Körper besteht aus etwa 206 Knochen. [de] |
| 232 | Was ist der Gefrierpunkt des Wassers in Grad Celsius? | Der Gefrierpunkt des Wassers beträgt 0 Grad Celsius. [de] | Der Gefrierpunkt des Wassers beträgt 0 Grad Celsius. [de] |
| 233 | Was ist die chemische Formel für Kohlendioxid? | Die chemische Formel für Kohlendioxid ist CO2. [de] | Die chemische Formel für Kohlendioxid ist CO₂. [de] |
| 234 | Welcher Ozean liegt zwischen Afrika und Australien? | Der Indische Ozean liegt zwischen Afrika und Australien. [de] | Der Indische Ozean liegt zwischen Afrika und Australien. [de] |
| 235 | Was ist die Hauptstadt von China? | Die Hauptstadt von China ist Peking (offiziell: Pekin). [de] | Die Hauptstadt von China ist Peking (offiziell: Pekin). [de] |
| 236 | In welcher Stadt befindet sich das Taj Mahal? | Das Taj Mahal befindet sich in Agra, Indien. [de] | Das Taj Mahal befindet sich in Agra, Indien. [de] |
| 237 | In welchem Jahr wurde der Euro als physische Währung eingefü... | Der Euro wurde 2002 als physische Währung eingeführt. [de] | Der Euro wurde 2002 als physische Währung eingeführt. [de] |
| 238 | Wer komponierte die Oper Carmen? | Eine klassische Frage! /  / Die Oper "Carmen" wurde von dem spanischen Komponisten Georges Bizet komponiert. S... [de] | Georg Friedrich Händel [de] |
| 239 | Was ist die Hauptstadt von Libanon? | Die Hauptstadt des Libanon ist Beirut. [de] | Die Hauptstadt des Libanon ist Beirut. [de] |
| 240 | Wie heißt der tiefste Tiefseegraben? | Der tiefste Tiefseegraben heißt Mariana-Trench-Graben. [de] | Der Tiefsee-Graben, auch als Tiefsee-Trench bezeichnet, ist der tiefste Graben im Ozean. [de] |
| 241 | Was ist das Jahr des Hindenburg-Unfalls? | Der Hindenburg-Unfall ereignete sich am 6. Mai 1937. [de] | Das Jahr des Hindenburg-Unfalls ist 1937. Am 6. Mai 1937 stürzte die Luftschiffzeppelin Hindenburg während ein... [de] |
| 242 | Was ist das chemische Symbolzeichen für Chlor? | Das chemische Symbolzeichen für Chlor ist Cl. [de] | Das chemische Symbolzeichen für Chlor ist Cl. [de] |
| 243 | Was ist die Hauptstadt von Finnland? | Die Hauptstadt von Finnland ist Helsinki. [de] | Hauptstadt von Finnland ist Helsinki. [de] |
| 244 | Wie viele Kammern hat das menschliche Herz? | Das menschliche Herz besteht aus vier Kammern. Diese Kammern sind: /  / 1.  **Rechtsh Herzkammer (Rechtsherzka... [de] | Das menschliche Herz hat 4 Kammern. [de] |
| 245 | Wer war die erste Frau, die einen Nobelpreis gewann? | Die erste Frau, die einen Nobelpreis gewann, war Marie Curie. Sie erhielt den Nobelpreis für Physik im Jahr 19... [de] | Marie Curie [unknown] |
| 246 | Was ist die Hauptstadt von Litauen? | Die Hauptstadt von Litauen ist Vilnius. [de] | Die Hauptstadt von Litauen ist Vilnius. [de] |
| 247 | Was ist die Hauptstadt von Jordanien? | Amman [unknown] | Die Hauptstadt von Jordanien ist Amman. [de] |
| 248 | Was ist das Jahr, in dem der Panama-Kanal eröffnet wurde? | Der Panama-Kanal wurde 1914 eröffnet. [de] | Das Jahr, in dem der Panama-Kanal eröffnet wurde, war 1914. [de] |
| 249 | Was ist 25 mal 4? | 25 mal 4 ist 100. [unknown] | Die Zahl 25 mal 4 ist eine Rechnung, bei der 25 die Multiplikationszahl und 4 die Zahl ist, die multipliziert ... [de] |

## Salidas: `prompt`

| # | pregunta usada | a=0 [lang] | a=1 [lang] |
|---|---|---|---|
| 200 | What is the capital of Ukraine? | The capital of Ukraine is Kyiv (also known as Kiev). [en] | La capitale de l'Ukraine est Kiev (ou Chytomir ou Chytomyl). [fr] |
| 201 | What force keeps planets in orbit around the Sun? | The force that keeps planets in orbit around the Sun is called gravity. Specifically, it's the gravitational f... [en] | The force that keeps planets in orbit around the Sun is gravity. According to Newton's Law of Universal Gravit... [en] |
| 202 | What is 15 plus 6? | 15 + 6 = 21 [unknown] | C'est facile! 15 + 6 = 21. [fr] |
| 203 | What is the capital of Syria? | The capital of Syria is Damascus. [en] | La capitale de la Syrie est Damas. [fr] |
| 204 | In what year did the Wright brothers first fly? | The Wright brothers, Orville and Wilbur, successfully flew the first powered, heavier-than-air aircraft on Dec... [en] | Les frères Wright ont effectué leur premier vol en 1903. [fr] |
| 205 | In what year did the Human Genome Project publish its first ... | The Human Genome Project published its first draft in 2000. [en] | Le projet du génome humain a publié sa première édition de dessin en 2000. [fr] |
| 206 | What is the chemical symbol for platinum? | The chemical symbol for platinum is Pt. [en] | Le symbole chimique du platinium est Pt. [fr] |
| 207 | In what year did Germany reunify? | Germany reunified on October 3, 1990. This was the day when East Germany (GDR) and West Germany (FRG) were off... [en] | L'Allemagne s'est réunifiée en 1990. [fr] |
| 208 | Who developed the theory of natural selection alongside Darw... | While Charles Darwin is often credited with developing the theory of natural selection, he didn't work alone. ... [en] | Une question sur l'histoire de la biologie! /  / Vous faites référence à la théorie de la sélection naturelle,... [fr] |
| 209 | What is 7 times 8? | 7 × 8 = 56 [unknown] | C'est facile! 7 fois 8 équivaut à 56. [fr] |
| 210 | Who developed the theory of general relativity? | The theory of general relativity was developed by Albert Einstein. He published his groundbreaking work, "Theo... [en] | C'est Albert Einstein qui a développé la théorie de la relativité générale. [fr] |
| 211 | Who painted The Scream? | The painting "The Scream" was created by the Norwegian artist Edvard Munch in 1893. It's one of his most famou... [en] | C'est Edvard Munch qui a peint La Tristesse (ou Le Rire, selon l'interprétation), une œuvre qui est devenue un... [fr] |
| 212 | What is the capital of Greece? | The capital of Greece is Athens. [en] | La capitale de Grèce est Athènes (Αθήνα). [fr] |
| 213 | Who wrote One Hundred Years of Solitude? | A classic of magical realism! /  / "One Hundred Years of Solitude" was written by the Colombian author Gabriel... [en] | C'est Gabriel García Márquez qui a écrit "Une Centaine d'Années de Solitude". [fr] |
| 214 | What is the largest ocean on Earth? | The largest ocean on Earth is the Pacific Ocean, which covers approximately 155.6 million square kilometers (6... [en] | Le plus grand océan de la Terre est l'Océan Pacifique. Il couvre environ 155,6 millions de kilomètres carrés e... [fr] |
| 215 | In what year did World War II begin? | World War II began in 1939. Specifically, it started on September 1, 1939, when Nazi Germany, led by Adolf Hit... [en] | La Seconde Guerre mondiale a commencé en 1939. [fr] |
| 216 | What is 17 times 2? | 17 × 2 = 34 [unknown] | C'est facile! 17 x 2 = 34. [fr] |
| 217 | Who wrote Hamlet? | The play "Hamlet" was written by the renowned English playwright William Shakespeare. It is one of his most fa... [en] | C'est William Shakespeare qui a écrit Hamlet. [fr] |
| 218 | Which galaxy is the nearest large neighbour to the Milky Way... | The nearest large neighbor to the Milky Way galaxy is the Andromeda Galaxy, also known as Messier 31 (M31) or ... [en] | La galaxie la plus proche du voisinage de la Voie lactée est la galaxie d'Andromède (M31). [fr] |
| 219 | How many moons does Mars have? | Mars has two small natural satellites, or moons. Their names are Phobos and Deimos. [en] | Mars a 2 moons. [unknown] |
| 220 | What is the chemical symbol for chromium? | The chemical symbol for Chromium is Cr. [en] | Le symbole chimique du chrome est Cr. [fr] |
| 221 | What is 9 plus 9? | 9 + 9 = 18 [unknown] | 9 + 9 = 18. [unknown] |
| 222 | Who received the 1876 patent for the telephone? | Alexander Graham Bell received the 1876 patent for the telephone. [en] | Alexander Graham Bell a reçu le 7 mars 1876 le brevet pour le téléphone. [fr] |
| 223 | What is the chemical symbol for zinc? | The chemical symbol for zinc is Zn. [en] | Le symbole chimique du zinc est Zn. [fr] |
| 224 | What is 25 plus 4? | 25 + 4 = 29 [unknown] | C'est facile! 25 + 4 = 29. [fr] |
| 225 | Who composed the Ninth Symphony containing Ode to Joy? | The Ninth Symphony, also known as the "Choral Symphony," was composed by Ludwig van Beethoven. It is one of hi... [en] | C'est Ludwig van Beethoven qui a composé la Symphonie n° 9, également connue sous le nom de Symphonie de la Jo... [fr] |
| 226 | How many time zones does the world have, in standard count? | The world has 24 time zones in standard count. These time zones are identified by their offset from Coordinate... [en] | Le monde a 24 zones horaires standards. [fr] |
| 227 | What is the capital of Qatar? | The capital of Qatar is Doha. [en] | Le capital de Qatar est Doha. [fr] |
| 228 | What is the capital of Czechia? | The capital of Czechia is Prague (Praha in Czech). [en] | La capitale de la République tchèque est Prague (Prague en anglais). [fr] |
| 229 | What is the capital of Bulgaria? | The capital of Bulgaria is Sofia (София). [en] | La capitale de Bulgarie est Sofia. [fr] |
| 230 | How many keys does a standard piano have? | A standard piano typically has 88 keys. This includes: /  / * 52 white keys (also known as naturals) / * 36 bl... [en] | A standard piano, also known as a grand piano or upright piano, typically has 88 keys. This includes 52 white ... [en] |
| 231 | How many bones are in the adult human body? | There are 206 bones in the adult human body. This number can vary slightly from person to person, as some indi... [en] | Il y a 206 os. [fr] |
| 232 | What is the freezing point of water in degrees Celsius? | The freezing point of water is 0 degrees Celsius (°C). [en] | Le point de gelage de l'eau est de 0 degrés Celsius. [fr] |
| 233 | What is the chemical formula for carbon dioxide? | The chemical formula for carbon dioxide is CO2. [en] | La formule chimique du dioxyde de carbone est CO₂. [fr] |
| 234 | Which ocean lies between Africa and Australia? | The Indian Ocean lies between Africa and Australia. [en] | La mer de Corail [unknown] |
| 235 | What is the capital of China? | The capital of China is Beijing. [en] | La capitale de la Chine est Pékin (Beijing). [fr] |
| 236 | In which city is the Taj Mahal located? | The Taj Mahal is located in Agra, India. [en] | Le Taj Mahal est situé à Agra, en Inde. [fr] |
| 237 | In what year was the euro introduced as physical currency? | The euro was introduced as physical currency in 2002. The first euro coins were minted in 2001, but they were ... [en] | Je suis là pour vous aider! Le euro a été introduit comme monnaie physique en 2002. Il a remplacé les monnaies... [fr] |
| 238 | Who composed the opera Carmen? | The opera "Carmen" was composed by Georges Bizet. [en] | L'opéra Carmen a été composé par Georges Bizet. [fr] |
| 239 | What is the capital of Lebanon? | The capital of Lebanon is Beirut. [en] | Le capitale du Liban est Beyrouth. [fr] |
| 240 | What is the deepest ocean trench called? | The deepest ocean trench is called the Mariana Trench. Specifically, the lowest point in the trench is called ... [en] | Le plus profond creux océanique s'appelle la "fossa des démons" ou la "fossa de Mariana". Cependant, le plus p... [fr] |
| 241 | In what year did the Hindenburg disaster occur? | The Hindenburg disaster occurred on May 6, 1937. [en] | Le désastre de l'Hindenburg est arrivé en 1937. [fr] |
| 242 | What is the chemical symbol for chlorine? | The chemical symbol for chlorine is Cl. [en] | Le symbole chimique du chlore est Cl. [fr] |
| 243 | What is the capital of Finland? | The capital of Finland is Helsinki. [en] | La capitale de la Finlande est Helsinki. [fr] |
| 244 | How many chambers does the human heart have? | The human heart has 4 chambers: /  / 1. **Right Atrium** (upper right chamber) / 2. **Right Ventricle** (lower... [en] | Le cœur humain a 4 chambers. [fr] |
| 245 | Who was the first woman to win a Nobel Prize? | Marie Curie was the first woman to win a Nobel Prize, and she won two Nobel Prizes in different fields. She wa... [en] | C'était Marie Curie. Elle a remporté deux prix Nobel, l'un en physique en 1903 et l'autre en chimie en 1911. [fr] |
| 246 | What is the capital of Lithuania? | The capital of Lithuania is Vilnius. [en] | La capitale de Lituanie est Vilnius. [fr] |
| 247 | What is the capital of Jordan? | The capital of Jordan is Amman. [en] | La capitale de la Jordanie est Amman. [fr] |
| 248 | In what year was the Panama Canal opened? | The Panama Canal was opened on August 15, 1914. [en] | Le canal de Panama a été ouvert en 1914. [fr] |
| 249 | What is 25 times 4? | 25 × 4 = 100 [unknown] | C'est facile! 25 fois 4 équivaut à 100. [fr] |

