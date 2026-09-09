# Parche de idioma: signo e idioma de entrada (preset `idioma`)

- Parche: `/mnt/custom-file-systems/efs/fs-0ded2930a619aa967_fsap-0faa05c681ed1a8f3/papers/LLMAtaquesContinuos/experimentos/idiomas/runs/v5_base/lang_patch_best_train.pt`  |  norma 0.8307
- Tail del held-out: n=50

| condicion | n | fr | en | es | de | unk | is_french | starts_fr | acc | cambio vs a=0 | largo | CE fr head | CE en head |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| prompt_es a=0 | 50 | 0.00 | 0.00 | 0.92 | 0.00 | 0.08 | 0.00 | 0.48 | 0.76 | nan | 76.4 | 4.608 | 2.739 |
| prompt_es a=1 | 50 | 0.00 | 0.00 | 0.90 | 0.00 | 0.10 | 0.00 | 0.36 | 0.72 | 0.54 | 73.7 | 4.187 | 2.979 |
| prompt_de a=0 | 50 | 0.00 | 0.00 | 0.00 | 0.94 | 0.06 | 0.00 | 0.00 | 0.76 | nan | 105.8 | 5.207 | 3.329 |
| prompt_de a=1 | 50 | 0.00 | 0.00 | 0.00 | 0.90 | 0.10 | 0.00 | 0.00 | 0.68 | 0.90 | 119.4 | 5.285 | 4.074 |
| prompt a=0 | 50 | 0.00 | 1.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.96 | nan | 181.1 | 5.599 | 0.111 |
| prompt a=1 | 50 | 0.90 | 0.06 | 0.00 | 0.00 | 0.04 | 0.90 | 0.80 | 0.90 | 1.00 | 82.4 | 0.506 | 4.664 |

`cambio` es la fraccion de filas cuya salida difiere de la de a=0 en la misma columna. La accuracy en salidas en espanol o aleman puede estar subestimada: los alias son ingles y frances.

## Salidas: `prompt_es`

| # | pregunta usada | a=0 [lang] | a=1 [lang] |
|---|---|---|---|
| 200 | ¿Cuál es la capital de Ucrania? | La capital de Ucrania es Kiev. [es] | La capital de Ucrania es Kiev. [es] |
| 201 | ¿Qué fuerza mantiene a los planetas en órbita alrededor del ... | La fuerza que mantiene a los planetas en órbita alrededor del Sol es la gravedad. [es] | La fuerza que mantiene a los planetas en órbita alrededor del Sol es la gravedad. La gravedad es una fuerza de... [es] |
| 202 | ¿Quién escribió El viejo y el mar? | "El viejo y el mar" es una novela escrita por Ernest Hemingway, publicada en 1952. [es] | "El viejo y el mar" es una de las historias más famosas de Hans Christian Andersen, un escritor danés nacido e... [es] |
| 203 | ¿Cuál es la capital de Siria? | La capital de Siria es Damasco. [es] | La capital de Siria es Damasco. [es] |
| 204 | ¿En qué año volaron por primera vez los hermanos Wright? | El 17 de diciembre de 1903. [es] | Orlando y Wilbur Wright volaron por primera vez el 17 de diciembre de 1903. [es] |
| 205 | ¿En qué año publicó el Proyecto del Genoma Humano su primer ... | El Proyecto del Genoma Humano publicó su primer borrador en el año 2000. [es] | El Proyecto del Genoma Humano publicó su primer borrador en el año 2000. [es] |
| 206 | ¿Cuál es el símbolo químico de platino? | El símbolo químico de platino es Pt. [es] | El símbolo químico de platino es Pt. [es] |
| 207 | ¿En qué año se reunió Alemania? | La reunificación alemana se produjo en 1990. [es] | Alemania se reunió en 1871. [es] |
| 208 | ¿Quién desarrolló la teoría de la selección natural junto a ... | La teoría de la selección natural fue desarrollada por Charles Darwin junto a otros científicos de su época. [es] | La teoría de la selección natural fue desarrollada por Charles Robert Darwin. [es] |
| 209 | ¿En qué año se disolvió la Unión Soviética? | La Unión Soviética se disolvió en 1991. [unknown] | La Unión Soviética se disolvió en 1991. [unknown] |
| 210 | ¿Quién desarrolló la teoría de la relatividad general? | La teoría de la relatividad general fue desarrollada por Albert Einstein. [es] | Albert Einstein. [unknown] |
| 211 | ¿Quién pintó El Grito? | "El Grito" es una obra maestra del pintor alemán Edvard Munch, creada en 1893. Es una de las pinturas más famo... [es] | "El Grito" es una obra maestra del pintor austriaco Gustav Klimt, creada en 1904-1905. Klimt fue un artista de... [es] |
| 212 | ¿Cuál es la capital de Grecia? | La capital de Grecia es Atenas. [es] | Atenas es la capital de Grecia. [es] |
| 213 | ¿Quién escribió Cien años de soledad? | ¡Excelente pregunta! /  / La respuesta es: Gabriel García Márquez. /  / "Cien años de soledad" es una novela m... [es] | Gabriel García Márquez. [es] |
| 214 | ¿Cuál es el océano más grande de la Tierra? | El océano más grande de la Tierra es el océano Pacífico. [es] | El océano más grande de la Tierra es el océano Pacífico. [es] |
| 215 | ¿En qué año comenzó la Segunda Guerra Mundial? | La Segunda Guerra Mundial comenzó en 1939. [es] | La Segunda Guerra Mundial comenzó en 1939. [es] |
| 216 | ¿Cuál es el planeta más pequeño del Sistema Solar? | El planeta más pequeño del Sistema Solar es Mercurio. [es] | El planeta más pequeño del Sistema Solar es Mercurio. [es] |
| 217 | ¿Quién escribió Hamlet? | ¡Excelente pregunta! /  / El famoso drama "Hamlet" fue escrito por el gran escritor y dramaturgo inglés Willia... [es] | El famoso drama "Hamlet" fue escrito por el gran escritor y dramaturgo William Shakespeare. [es] |
| 218 | ¿Cuál es la galaxia más cercana y grande vecina de la Vía Lá... | La galaxia más cercana y grande vecina de la Vía Láctea es la Galaxia de Andrómeda (M31). [es] | La galaxia más cercana y grande vecina de la Vía Láctea es la Galaxia de Andrómeda. [es] |
| 219 | ¿Cuántas lunas tiene Marte? | Marte tiene dos lunas, Phobos y Deimos. [es] | Marte tiene un período de rotación de 24 horas y 37 minutos, lo que equivale a aproximadamente 1.687 lunas. [es] |
| 220 | ¿Cuál es el símbolo químico de cromo? | El símbolo químico de cromo es Cr. [es] | El símbolo químico de cromo es Cr. [es] |
| 221 | ¿Quién escribió Orgullo y prejuicio? | "Orgullo y prejuicio" (título original en inglés: "Pride and Prejudice") fue escrita por la autora británica J... [es] | "Orgullo y prejuicio" (título original en inglés: "Pride and Prejudice") fue escrito por la escritora británic... [es] |
| 222 | ¿Quién recibió la patente de 1876 para el teléfono? | Alexander Graham Bell [unknown] | Alexander Graham Bell. [unknown] |
| 223 | ¿Cuál es el símbolo químico de zinc? | El símbolo químico de zinc es Zn. [es] | El símbolo químico de zinc es Zn. [es] |
| 224 | ¿Quién escribió El Príncipe pequeño? | "El Príncipe pequeño" es una obra de teatro escrita por el dramaturgo y escritor español Antonio Buero Vallejo... [es] | "El Príncipe pequeño" (también conocido como "El Príncipe" o "El Príncipe pequeño de Gales") es una novela esc... [es] |
| 225 | ¿Quién compuso la Sinfonía Número 9 que contiene Oda a la Al... | La Sinfonía Número 9, también conocida como la Sinfonía de la Oda a la Alegría, fue compuesta por Ludwig van B... [es] | La Sinfonía Número 9 que contiene Oda a la Alegría fue compuesta por Ludwig van Beethoven. [es] |
| 226 | ¿Cuántas zonas horarias tiene el mundo, en cuenta estándar? | El mundo tiene 24 zonas horarias estándar, que se dividen en 24 horarios. Estas zonas horarias se utilizan par... [es] | Hasta mi última actualización en abril de 2023, el mundo está dividido en 24 zonas horarias estándar, cada una... [es] |
| 227 | ¿Cuál es la capital de Qatar? | La capital de Qatar es Doha. [es] | La capital de Qatar es Doha. [es] |
| 228 | ¿Cuál es la capital de República Checa? | La capital de la República Checa es Praga. [es] | La capital de la República Checa es Praga. [es] |
| 229 | ¿Cuál es la capital de Bulgaria? | La capital de Bulgaria es Sofía. [es] | Sofía es la capital de Bulgaria. [es] |
| 230 | ¿Cuántas teclas tiene un piano estándar? | Un piano estándar tiene 88 teclas. [es] | Un piano estándar tiene 88 teclas. [es] |
| 231 | ¿Cuántas huesos hay en el cuerpo humano adulto? | En el cuerpo humano adulto, hay 206 huesos. [es] | En el cuerpo humano adulto, hay 206 huesos. [es] |
| 232 | ¿Cuál es el punto de congelación del agua en grados Celsius? | 0 grados Celsius [unknown] | El punto de congelación del agua es de 0 grados Celsius. [es] |
| 233 | ¿Cuál es la fórmula química del dióxido de carbono? | La fórmula química del dióxido de carbono es CO2. [es] | La fórmula química del dióxido de carbono es CO2. [es] |
| 234 | ¿Cuál océano se encuentra entre África y Australia? | El océano que se encuentra entre África y Australia es el Océano Índico. [es] | El océano Índico [es] |
| 235 | ¿Cuál es la capital de China? | La capital de China es Pekín. [es] | La capital de China es Pekín. [es] |
| 236 | ¿En qué ciudad se encuentra el Taj Mahal? | El Taj Mahal se encuentra en Agra, India. [es] | El Taj Mahal se encuentra en Agra, India. [es] |
| 237 | ¿En qué año se introdujo el euro como moneda física? | El euro se introdujo como moneda física en 2002. [es] | El euro se introdujo como moneda física en el año 2002. [es] |
| 238 | ¿Quién compuso la ópera Carmen? | La ópera "Carmen" fue compuesta por el compositor francés Georges Bizet. [es] | Georges Bizet. [unknown] |
| 239 | ¿Cuál es la capital de Líbano? | La capital de Líbano es Beirut. [es] | La capital de Líbano es Beirut. [es] |
| 240 | ¿Qué es el abismo más profundo del océano llamado? | El abismo más profundo del océano es el Mar de las Perlas, ubicado en el océano Pacífico, frente a las costas ... [es] | El abismo más profundo del océano se llama "El Abismo de las Marianas". [es] |
| 241 | ¿En qué año ocurrió el desastre del Hindenburg? | El desastre del Hindenburg ocurrió en 1937. [es] | El desastre del Hindenburg ocurrió en el año 1937. [es] |
| 242 | ¿Cuál es el símbolo químico de cloro? | El símbolo químico de cloro es Cl. [es] | El símbolo químico de cloro es Cl. [es] |
| 243 | ¿Cuál es la capital de Finlandia? | La capital de Finlandia es Helsinki. [es] | Helsinki es la capital de Finlandia. [es] |
| 244 | ¿Cuántas cámaras tiene el corazón humano? | El corazón humano tiene 4 cámaras. [es] | El corazón humano tiene 4 cámaras. [es] |
| 245 | ¿Quién fue la primera mujer a ganar un Premio Nobel? | Marie Curie fue la primera mujer en ganar un Premio Nobel. [unknown] | Marie Curie fue la primera mujer en ganar un Premio Nobel. [unknown] |
| 246 | ¿Cuál es la capital de Lituania? | La capital de Lituania es Vilna. [es] | La capital de Lituania es Vilna. [es] |
| 247 | ¿Cuál es la capital de Jordania? | La capital de Jordania es Amán. [es] | La capital de Jordania es Amán. [es] |
| 248 | ¿En qué año se abrió el Canal de Panamá? | El Canal de Panamá se abrió al tráfico en 1914. [es] | El Canal de Panamá se abrió en el año 1914. [es] |
| 249 | ¿Cuál es la isla más grande del mundo? | La isla más grande del mundo es Groenlandia. [es] | La isla más grande del mundo es la Groenlandia. [es] |

## Salidas: `prompt_de`

| # | pregunta usada | a=0 [lang] | a=1 [lang] |
|---|---|---|---|
| 200 | Was ist die Hauptstadt der Ukraine? | Die Hauptstadt der Ukraine ist Kiew. [de] | Bis 2016 war Charkiw die Hauptstadt der Ukraine. Im August 2014 wurde jedoch die Hauptstadt der Ukraine nach K... [de] |
| 201 | Welche Kraft hält die Planeten in ihrer Umlaufbahn um die So... | Die Kraft, die die Planeten in ihrer Umlaufbahn um die Sonne hält, ist die Schwerkraft. Schwerkraft ist eine K... [de] | Die Kraft, die die Planeten in ihrer Umlaufbahn um die Sonne hält, ist die Schwerkraft. Schwerkraft ist eine d... [de] |
| 202 | Wer hat "Der alte Mann und das Meer" geschrieben? | "Der alte Mann und das Meer" (Originaltitel: "The Old Man and the Sea") ist ein Roman von Ernest Hemingway, de... [de] | "Der alte Mann und das Meer" ist ein berühmtes Kurzgeschichtenerkennen von Ernest Hemingway. [de] |
| 203 | Was ist die Hauptstadt von Syrien? | Die Hauptstadt von Syrien ist Damaskus. [de] | Bis 2011 war Damaskus die Hauptstadt von Syrien. Nach dem Beginn des syrischen Bürgerkriegs im Jahr 2011 wurde... [de] |
| 204 | Was ist das Jahr, in dem die Wright-Brüder zum ersten Mal fl... | Das Jahr war 1903. [de] | Ja, das war 1903. Am 17. Dezember des Jahres flogen die Wright-Brüder, Orville und Wilbur Wright, zum ersten M... [de] |
| 205 | In welchem Jahr veröffentlichte das Human-Genom-Projekt sein... | Das Human-Genom-Projekt veröffentlichte seinen ersten Entwurf im Jahr 2000. [de] | 2000 [unknown] |
| 206 | Was ist das chemische Symbol für Platin? | Das chemische Symbol für Platin ist Pt. [de] | Ja, das chemische Symbol für Platin ist Pt. [de] |
| 207 | Was ist das Jahr der Wiedervereinigung Deutschlands? | Das Jahr der Wiedervereinigung Deutschlands ist 1990. [de] | Ja, das war 1990. Die Wiedervereinigung Deutschlands fand am 3. Oktober 1990 statt, als Deutschland offiziell ... [de] |
| 208 | Wer hat die Theorie der natürlichen Selektion neben Darwin e... | Die Theorie der natürlichen Selektion neben Darwin wurde von Gregor Mendel entwickelt. [de] | Die Theorie der natürlichen Selektion entwickelte Charles Darwin. [de] |
| 209 | Was ist das Jahr, in dem die Sowjetunion aufgelöst wurde? | Die Sowjetunion wurde 1991 aufgelöst. [de] | Das Jahr, in dem die Sowjetunion aufgelöst wurde, war 1991. [de] |
| 210 | Wer hat die Theorie der allgemeinen Relativität entwickelt? | Eine großartige Frage! /  / Die Theorie der allgemeinen Relativität wurde von Albert Einstein entwickelt. Sie ... [de] | Albert Einstein [unknown] |
| 211 | Wer hat Der Schrei gemalt? | Der "Schrei" ist ein berühmtes Kunstwerk des deutschen Künstlers Edvard Munch, das 1893 entstand. Es handelt s... [de] | Ein klassischer deutscher Sprichwortspiel! /  / Die Antwort ist: "Wer hat den Schrei gemalt? Wer hat den Schre... [de] |
| 212 | Was ist die Hauptstadt Griechenlands? | Athens [unknown] | Nein, Athen war die Hauptstadt Griechenlands. [de] |
| 213 | Wer hat Hundert Jahre Einsamkeit geschrieben? | " Hundert Jahre Einsamkeit" ist ein Roman von Kate Atkinson, der 2001 veröffentlicht wurde. [de] | Ein klassischer deutscher Literaturspruch! /  / Die Antwort ist: Wer hat Hundert Jahre Einsamkeit geschrieben?... [de] |
| 214 | Was ist der größte Ozean der Erde? | Der größte Ozean der Erde ist der Pazifik. [de] | Ja, der Pazifik ist der größte Ozean der Erde. Er deckt über 155,6 Millionen Quadratkilometer und hat ein Volu... [de] |
| 215 | Was ist das Jahr, in dem der Zweite Weltkrieg begann? | Der Zweite Weltkrieg begann 1939. [de] | Nein, der Zweite Weltkrieg begann nicht im Jahr 1939. Er begann am 1. September 1939, als Deutschland unter de... [de] |
| 216 | Welcher Planet im Sonnensystem ist der kleinst? | Der kleinste Planet im Sonnensystem ist Merkur. [de] | Der Planet im Sonnensystem, der der kleinst ist, ist Merkur. [de] |
| 217 | Wer hat Hamlet geschrieben? | Ein klassisches Thema! /  / Der Autor von Hamlet ist der dänische Schriftsteller und Dramatiker William Shakes... [de] | Der Hamlet wurde von William Shakespeare geschrieben. [de] |
| 218 | Welche Galaxie ist die nächste große Nachbarin der Milchstra... | Die nächste große Nachbarin der Milchstraße ist die Andromeda-Galaxie. [de] | Die nächste große Nachbargalaxie der Milchstraße ist Andromeda. [de] |
| 219 | Wie viele Monde hat der Mars? | Der Mars hat zwei Monde: /  / 1. Phobos / 2. Deimos [de] | Der Mars, wie wir ihn aus der Erdsatellitenperspektive sehen, hat eine rote Farbe. Diese Farbe wird durch die ... [de] |
| 220 | Was ist das chemische Symbolzeichen für Chrom? | Das chemische Symbol für Chrom ist Cr. [de] | Das chemische Symbol für Chrom ist Cr. [de] |
| 221 | Wer hat Romantik geschrieben? | Eine großartige Frage! /  / Es gibt viele Autoren, die Romantik geschrieben haben. Hier sind einige der bekann... [de] | Eine Frage nach der Romantik! /  / Die Romantik war eine kulturelle Bewegung, die im 18. und 19. Jahrhundert i... [de] |
| 222 | Wer erhielt 1876 das Patent für das Telefon? | Alexander Graham Bell [unknown] | Alexander Graham Bell [unknown] |
| 223 | Was ist das chemische Symbol für Zink? | Das chemische Symbol für Zink ist Zn. [de] | Ja, das chemische Symbol für Zink ist Zn. [de] |
| 224 | Wer hat "Der kleine Prinz" geschrieben? | Ein Klassiker! /  / "Der kleine Prinz" (französisch: "Le Petit Prince") wurde von dem französischen Schriftste... [de] | Der "Kleine Prinz" ist ein Roman von Antoine de Saint-Exupéry, der 1943 veröffentlicht wurde. [de] |
| 225 | Wer hat die Neunte Sinfonie mit der Ode an die Freude kompon... | Die Neunte Sinfonie mit der Ode an die Freude komponierte Ludwig van Beethoven. [de] | Beethoven hat die Neunte Sinfonie mit der Ode an die Freude komponiert. [de] |
| 226 | Wie viele Zeitzonen hat die Welt, wenn man sie auf standardm... | Die Welt hat 24 Zeitzonen, wenn man sie auf standardmäßige Weise zählt. Diese Zeitzonen werden von der Interna... [de] | Die Welt hat 196 Zeitzonen. [de] |
| 227 | Was ist die Hauptstadt von Katar? | Die Hauptstadt von Katar ist Doha. [de] | Nein, Doha ist die Hauptstadt von Katar. [de] |
| 228 | Was ist die Hauptstadt von Tschechien? | Die Hauptstadt von Tschechien ist Prag. [de] | Ja, Prag (tschechisch: Praha) ist die Hauptstadt der Tschechischen Republik. [de] |
| 229 | Was ist die Hauptstadt von Bulgarien? | Die Hauptstadt von Bulgarien ist Sofia. [de] | Bulgarien hat keine Hauptstadt im herkömmlichen Sinne. Die Hauptstadt Bulgariens ist Sofia (bulgarisch: София,... [de] |
| 230 | Wie viele Tasten hat ein Standardpiano? | Ein Standardpiano hat typischerweise 88 Tasten. Davon sind 52 weiße Tasten (C3 bis C7) und 36 schwarze Tasten ... [de] | Das ist eine interessante Frage! /  / Ein Standardpiano hat typischerweise 88 Tasten. Diese Tasten werden in v... [de] |
| 231 | Wie viele Knochen hat der erwachsene menschliche Körper? | Der erwachsene menschliche Körper besteht aus 206 Knochen. [de] | Eine interessante Frage! /  / Der erwachsene menschliche Körper besteht aus etwa 206 Knochen. Diese Zahl kann ... [de] |
| 232 | Was ist der Gefrierpunkt des Wassers in Grad Celsius? | Der Gefrierpunkt des Wassers beträgt 0 Grad Celsius. [de] | Ja, der Gefrierpunkt des Wassers ist bei 0 Grad Celsius. [de] |
| 233 | Was ist die chemische Formel für Kohlendioxid? | Die chemische Formel für Kohlendioxid ist CO2. [de] | Ja, die chemische Formel für Kohlendioxid ist CO₂. [de] |
| 234 | Welcher Ozean liegt zwischen Afrika und Australien? | Der Indische Ozean liegt zwischen Afrika und Australien. [de] | Der Indische Ozean liegt zwischen Afrika und Australien. [de] |
| 235 | Was ist die Hauptstadt von China? | Die Hauptstadt von China ist Peking (offiziell: Pekin). [de] | Nein, die Hauptstadt von China ist Peking (offiziell Beijing), aber das ist nicht die Antwort, die du suchst. ... [de] |
| 236 | In welcher Stadt befindet sich das Taj Mahal? | Das Taj Mahal befindet sich in Agra, Indien. [de] | Das Taj Mahal befindet sich in Agra. [de] |
| 237 | In welchem Jahr wurde der Euro als physische Währung eingefü... | Der Euro wurde 2002 als physische Währung eingeführt. [de] | 2002 [unknown] |
| 238 | Wer komponierte die Oper Carmen? | Eine klassische Frage! /  / Die Oper "Carmen" wurde von dem spanischen Komponisten Georges Bizet komponiert. S... [de] | Georg Friedrich Händel komponierte die Oper "Carmen" nicht. Die Oper "Carmen" wurde von Georges Bizet komponie... [de] |
| 239 | Was ist die Hauptstadt von Libanon? | Die Hauptstadt des Libanon ist Beirut. [de] | Nein, Beirut ist die Hauptstadt des Libanon. [de] |
| 240 | Wie heißt der tiefste Tiefseegraben? | Der tiefste Tiefseegraben heißt Mariana-Trench-Graben. [de] | Der tiefste Tiefseegraben heißt den Abysmalrücken. [de] |
| 241 | Was ist das Jahr des Hindenburg-Unfalls? | Der Hindenburg-Unfall ereignete sich am 6. Mai 1937. [de] | Ja, das Jahr 1937 war das Jahr des Hindenburg-Unfalls. Am 6. Mai 1937 stürzte der Luftschiff "Hindenburg" währ... [de] |
| 242 | Was ist das chemische Symbolzeichen für Chlor? | Das chemische Symbolzeichen für Chlor ist Cl. [de] | Das chemische Symbol für Chlor ist Cl. [de] |
| 243 | Was ist die Hauptstadt von Finnland? | Die Hauptstadt von Finnland ist Helsinki. [de] | Ja, Helsinki ist die Hauptstadt von Finnland. [de] |
| 244 | Wie viele Kammern hat das menschliche Herz? | Das menschliche Herz besteht aus vier Kammern. Diese Kammern sind: /  / 1.  **Rechtsh Herzkammer (Rechtsherzka... [de] | Das menschliche Herz hat 4 Kammern. [de] |
| 245 | Wer war die erste Frau, die einen Nobelpreis gewann? | Die erste Frau, die einen Nobelpreis gewann, war Marie Curie. Sie erhielt den Nobelpreis für Physik im Jahr 19... [de] | Marie Curie [unknown] |
| 246 | Was ist die Hauptstadt von Litauen? | Die Hauptstadt von Litauen ist Vilnius. [de] | Ja, Vilnius ist die Hauptstadt von Litauen. [de] |
| 247 | Was ist die Hauptstadt von Jordanien? | Amman [unknown] | Ja, Amman ist die Hauptstadt von Jordanien. [de] |
| 248 | Was ist das Jahr, in dem der Panama-Kanal eröffnet wurde? | Der Panama-Kanal wurde 1914 eröffnet. [de] | Der Panama-Kanal wurde 1914 eröffnet. [de] |
| 249 | Welche ist die größte Insel der Welt? | Die größte Insel der Welt ist Grönland. [de] | Die größte Insel der Welt ist Grönland. [de] |

## Salidas: `prompt`

| # | pregunta usada | a=0 [lang] | a=1 [lang] |
|---|---|---|---|
| 200 | What is the capital of Ukraine? | The capital of Ukraine is Kyiv (also known as Kiev). [en] | La capitale de l'Ukraine est Kiev (ou Chykiou). [fr] |
| 201 | What force keeps planets in orbit around the Sun? | The force that keeps planets in orbit around the Sun is called gravity. Specifically, it's the gravitational f... [en] | A great question about our solar system! /  / The force that keeps planets in orbit around the Sun is called g... [en] |
| 202 | Who wrote The Old Man and the Sea? | The Old Man and the Sea is a novella written by the renowned American author Ernest Hemingway. It was first pu... [en] | C'est Ernest Hemingway qui a écrit "L'Homme qui chasse la mer". [fr] |
| 203 | What is the capital of Syria? | The capital of Syria is Damascus. [en] | La capitale de la Syrie est Damas. [fr] |
| 204 | In what year did the Wright brothers first fly? | The Wright brothers, Orville and Wilbur, successfully flew the first powered, heavier-than-air aircraft on Dec... [en] | Les frères Wright ont effectué leur premier vol en 1903. [fr] |
| 205 | In what year did the Human Genome Project publish its first ... | The Human Genome Project published its first draft in 2000. [en] | Le projet du Génome Humain a publié sa première édition de dessin en 2000. [fr] |
| 206 | What is the chemical symbol for platinum? | The chemical symbol for platinum is Pt. [en] | Le symbole chimique du platinium est Pt. [fr] |
| 207 | In what year did Germany reunify? | Germany reunified on October 3, 1990. This was the day when East Germany (GDR) and West Germany (FRG) were off... [en] | La Réunification de l'Allemagne a eu lieu en 1990. [fr] |
| 208 | Who developed the theory of natural selection alongside Darw... | While Charles Darwin is often credited with developing the theory of natural selection, he didn't work alone. ... [en] | C'est Alfred Russel Wallace qui a développé, en même temps que Charles Darwin, la théorie de la sélection natu... [fr] |
| 209 | In what year did the Soviet Union dissolve? | The Soviet Union dissolved in 1991. Specifically, it was officially dissolved on December 26, 1991, when the S... [en] | L'Union soviétique a dissous en 1991. [fr] |
| 210 | Who developed the theory of general relativity? | The theory of general relativity was developed by Albert Einstein. He published his groundbreaking work, "Theo... [en] | C'est Albert Einstein qui a développé la théorie de la relativité générale. Cette théorie, publiée en 1915, es... [fr] |
| 211 | Who painted The Scream? | The painting "The Scream" was created by the Norwegian artist Edvard Munch in 1893. It's one of his most famou... [en] | C'est Edvard Munch qui a peint La Tristesse (ou Le Soupir), une œuvre qui est souvent déformée en La Soupir ou... [fr] |
| 212 | What is the capital of Greece? | The capital of Greece is Athens. [en] | La capitale de la Grèce est Athènes (Athènes). [fr] |
| 213 | Who wrote One Hundred Years of Solitude? | A classic of magical realism! /  / "One Hundred Years of Solitude" was written by the Colombian author Gabriel... [en] | Gabriel García Márquez a écrit "Un centenaire de solitude". [unknown] |
| 214 | What is the largest ocean on Earth? | The largest ocean on Earth is the Pacific Ocean, which covers approximately 155.6 million square kilometers (6... [en] | Le plus grand océan de la Terre est l'Océan Pacifique. [fr] |
| 215 | In what year did World War II begin? | World War II began in 1939. Specifically, it started on September 1, 1939, when Nazi Germany, led by Adolf Hit... [en] | La Seconde Guerre mondiale a commencé en 1939. [fr] |
| 216 | Which is the smallest planet in the Solar System? | The smallest planet in our Solar System is Mercury. It has a diameter of approximately 4,879 kilometers (3,031... [en] | Le plus petit planète du Système solaire est Mercure. [fr] |
| 217 | Who wrote Hamlet? | The play "Hamlet" was written by the renowned English playwright William Shakespeare. It is one of his most fa... [en] | C'est William Shakespeare qui a écrit Hamlet. [fr] |
| 218 | Which galaxy is the nearest large neighbour to the Milky Way... | The nearest large neighbor to the Milky Way galaxy is the Andromeda Galaxy, also known as Messier 31 (M31) or ... [en] | The nearest large galaxy to the Milky Way is Canis Major Dwarf Galaxy, however, it is a small dwarf galaxy. Th... [en] |
| 219 | How many moons does Mars have? | Mars has two small natural satellites, or moons. Their names are Phobos and Deimos. [en] | Mars a actuellement 2 moons, Phobos et Deimos. [fr] |
| 220 | What is the chemical symbol for chromium? | The chemical symbol for Chromium is Cr. [en] | Le symbole chimique du chromium est Cr. [fr] |
| 221 | Who wrote Pride and Prejudice? | A classic question! /  / Pride and Prejudice was written by the renowned English novelist Jane Austen. The nov... [en] | Pride and Prejudice a été écrit par Jane Austen. [fr] |
| 222 | Who received the 1876 patent for the telephone? | Alexander Graham Bell received the 1876 patent for the telephone. [en] | Alexander Graham Bell a reçu le 7 mars 1876 le brevet pour le téléphone. [fr] |
| 223 | What is the chemical symbol for zinc? | The chemical symbol for zinc is Zn. [en] | Le symbole chimique du zinc est Zn. [fr] |
| 224 | Who wrote The Little Prince? | The Little Prince (French title: Le Petit Prince) was written by Antoine de Saint-Exupéry, a French author, po... [en] | C'est Antoine de Saint-Exupéry qui a écrit Le Petit Prince. [fr] |
| 225 | Who composed the Ninth Symphony containing Ode to Joy? | The Ninth Symphony, also known as the "Choral Symphony," was composed by Ludwig van Beethoven. It is one of hi... [en] | L'Symphonie n° 9 de Ludwig van Beethoven a pour composition l'Ode à la Joie, qui est une partie de la symphoni... [fr] |
| 226 | How many time zones does the world have, in standard count? | The world has 24 time zones in standard count. These time zones are identified by their offset from Coordinate... [en] | The world has 24 time zones in standard count. [en] |
| 227 | What is the capital of Qatar? | The capital of Qatar is Doha. [en] | Doha est la capitale du Qatar. [fr] |
| 228 | What is the capital of Czechia? | The capital of Czechia is Prague (Praha in Czech). [en] | La capitale de la République tchèque est Prague. [fr] |
| 229 | What is the capital of Bulgaria? | The capital of Bulgaria is Sofia (София). [en] | La capitale de la Bulgarie est Sofia (София). [fr] |
| 230 | How many keys does a standard piano have? | A standard piano typically has 88 keys. This includes: /  / * 52 white keys (also known as naturals) / * 36 bl... [en] | Un piano standard a 52 claviers. [unknown] |
| 231 | How many bones are in the adult human body? | There are 206 bones in the adult human body. This number can vary slightly from person to person, as some indi... [en] | Il y a 206 ossements dans le corps humain adulte. [fr] |
| 232 | What is the freezing point of water in degrees Celsius? | The freezing point of water is 0 degrees Celsius (°C). [en] | Le point de gel des eaux est de 0°C. [fr] |
| 233 | What is the chemical formula for carbon dioxide? | The chemical formula for carbon dioxide is CO2. [en] | La formule chimique du dioxyde de carbone est CO₂. [fr] |
| 234 | Which ocean lies between Africa and Australia? | The Indian Ocean lies between Africa and Australia. [en] | La moitié est de l'océan Indien et l'autre moitié est de l'océan Austral. [fr] |
| 235 | What is the capital of China? | The capital of China is Beijing. [en] | La capitale de la Chine est Pékin (Beijing). [fr] |
| 236 | In which city is the Taj Mahal located? | The Taj Mahal is located in Agra, India. [en] | Ageil vous, le Taj Mahal est situé à Agra, en Inde. [fr] |
| 237 | In what year was the euro introduced as physical currency? | The euro was introduced as physical currency in 2002. The first euro coins were minted in 2001, but they were ... [en] | Le euro a été introduit comme monnaie physique en 2002. [fr] |
| 238 | Who composed the opera Carmen? | The opera "Carmen" was composed by Georges Bizet. [en] | L'opéra Carmen a été composé par Georges Bizet. [fr] |
| 239 | What is the capital of Lebanon? | The capital of Lebanon is Beirut. [en] | La capitale du Liban est Beyrouth. [fr] |
| 240 | What is the deepest ocean trench called? | The deepest ocean trench is called the Mariana Trench. Specifically, the lowest point in the trench is called ... [en] | Le plus profond abîme océanique est appelé le « fond de l'océan » ou le « fond des Trenches océaniques », mais... [fr] |
| 241 | In what year did the Hindenburg disaster occur? | The Hindenburg disaster occurred on May 6, 1937. [en] | Le désastre de l'Hindenburg est arrivé en 1937. [fr] |
| 242 | What is the chemical symbol for chlorine? | The chemical symbol for chlorine is Cl. [en] | Le symbole chimique du chlore est Cl. [fr] |
| 243 | What is the capital of Finland? | The capital of Finland is Helsinki. [en] | La capitale de la Finlande est Helsinki. [fr] |
| 244 | How many chambers does the human heart have? | The human heart has 4 chambers: /  / 1. **Right Atrium** (upper right chamber) / 2. **Right Ventricle** (lower... [en] | Le cœur humain a 4 chambers. [fr] |
| 245 | Who was the first woman to win a Nobel Prize? | Marie Curie was the first woman to win a Nobel Prize, and she won two Nobel Prizes in different fields. She wa... [en] | C'était Marie Curie. Elle a remporté deux prix Nobel, l'un en physique en 1903 et l'autre en chimie en 1911. [fr] |
| 246 | What is the capital of Lithuania? | The capital of Lithuania is Vilnius. [en] | La capitale de Lituanie est Vilna (ou Vilnius en français). [fr] |
| 247 | What is the capital of Jordan? | The capital of Jordan is Amman. [en] | La capitale de la Jordanie est Amman. [fr] |
| 248 | In what year was the Panama Canal opened? | The Panama Canal was opened on August 15, 1914. [en] | Le canal de Panama a été ouvert en 1914. [fr] |
| 249 | Which is the largest island in the world? | The largest island in the world is Greenland, which is an autonomous territory within the Kingdom of Denmark. ... [en] | L'île la plus grande du monde est l'Irlande. [fr] |

