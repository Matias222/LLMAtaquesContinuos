# Parche de idioma: signo e idioma de entrada (preset `idioma`)

- Parche: `/mnt/custom-file-systems/efs/fs-0ded2930a619aa967_fsap-0faa05c681ed1a8f3/papers/LLMAtaquesContinuos/experimentos/idiomas/runs/v6_goalall_head_mono_s1/lang_patch_best_train.pt`  |  norma 0.6692
- Tail del held-out: n=50

Celda target del parche: **fr**. `celda ok` = idioma `fr` Y NO mayusculas. En la tabla grande, `CE fr head` es la CE del target de ESTA celda (columna `output`).

| condicion | celda ok | idioma target | mayusculas |
|---|---|---|---|
| prompt_es a=0 | 0.00 | 0.00 | 0.00 |
| prompt_es a=1 | 0.14 | 0.14 | 0.00 |
| prompt_de a=0 | 0.00 | 0.00 | 0.00 |
| prompt_de a=1 | 0.00 | 0.00 | 0.00 |
| prompt a=0 | 0.00 | 0.00 | 0.00 |
| prompt a=1 | 0.94 | 0.94 | 0.00 |

| condicion | n | fr | en | es | de | it | pt | unk | is_french | starts_fr | acc | cambio vs a=0 | largo | CE fr head | CE en head | tok parche |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| prompt_es a=0 | 50 | 0.00 | 0.00 | 0.92 | 0.00 | 0.00 | 0.00 | 0.08 | 0.00 | 0.48 | 0.76 | nan | 76.4 | 4.608 | 2.739 | 0.0 |
| prompt_es a=1 | 50 | 0.14 | 0.00 | 0.74 | 0.00 | 0.00 | 0.00 | 0.12 | 0.14 | 0.36 | 0.64 | 0.76 | 150.7 | 3.689 | 4.549 | 13.9 |
| prompt_de a=0 | 50 | 0.00 | 0.00 | 0.00 | 0.94 | 0.00 | 0.00 | 0.06 | 0.00 | 0.00 | 0.76 | nan | 105.8 | 5.207 | 3.329 | 0.0 |
| prompt_de a=1 | 50 | 0.00 | 0.00 | 0.00 | 1.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.64 | 0.84 | 208.7 | 5.203 | 5.798 | 12.5 |
| prompt a=0 | 50 | 0.00 | 1.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.96 | nan | 181.1 | 5.599 | 0.111 | 0.0 |
| prompt a=1 | 50 | 0.94 | 0.04 | 0.00 | 0.00 | 0.00 | 0.00 | 0.02 | 0.94 | 0.82 | 0.94 | 1.00 | 102.1 | 0.644 | 3.157 | 8.7 |

`tok parche` es la media de posiciones que reciben el parche (con anchor goal_all, el largo de la pregunta: la perturbacion total es ese numero por v). `cambio` es la fraccion de filas cuya salida difiere de la de a=0 en la misma columna. La accuracy en salidas en espanol o aleman puede estar subestimada: los alias son ingles y frances.

## Salidas: `prompt_es`

| # | pregunta usada | a=0 [lang] | a=1 [lang] |
|---|---|---|---|
| 200 | ¿Cuál es la capital de Ucrania? | La capital de Ucrania es Kiev. [es] | La capital de Ucrania es Kiev. [es] |
| 201 | ¿Qué fuerza mantiene a los planetas en órbita alrededor del ... | La fuerza que mantiene a los planetas en órbita alrededor del Sol es la gravedad. [es] | Una pregunta sobre astrofísica! /  / La fuerza que mantiene a los planetas en órbita alrededor del Sol es la g... [es] |
| 202 | ¿Quién escribió El viejo y el mar? | "El viejo y el mar" es una novela escrita por Ernest Hemingway, publicada en 1952. [es] | Je suis désolé, mais je n'ai pas trouvé d'informations sur une personne qui ait écrit "El viejo y el mar" (qui... [fr] |
| 203 | ¿Cuál es la capital de Siria? | La capital de Siria es Damasco. [es] | La capital de Siria es Damasco. [es] |
| 204 | ¿En qué año volaron por primera vez los hermanos Wright? | El 17 de diciembre de 1903. [es] | Los hermanos Wright volaron por primera vez en 1903. [es] |
| 205 | ¿En qué año publicó el Proyecto del Genoma Humano su primer ... | El Proyecto del Genoma Humano publicó su primer borrador en el año 2000. [es] | El Proyecto del Genoma Humano publicó su primer borrador en el año 2001. [es] |
| 206 | ¿Cuál es el símbolo químico de platino? | El símbolo químico de platino es Pt. [es] | Lo siento, pero no puedo proporcionar información sobre símbolos químicos. ¿Hay algo más en lo que pueda ayuda... [es] |
| 207 | ¿En qué año se reunió Alemania? | La reunificación alemana se produjo en 1990. [es] | Puedes decirme quién es Alemania para que pueda darte una respuesta más precisa. [es] |
| 208 | ¿Quién desarrolló la teoría de la selección natural junto a ... | La teoría de la selección natural fue desarrollada por Charles Darwin junto a otros científicos de su época. [es] | Charles Robert Darwin [unknown] |
| 209 | ¿En qué año se disolvió la Unión Soviética? | La Unión Soviética se disolvió en 1991. [unknown] | Hasta mi última actualización en 2023, no tengo información específica sobre el año en que se disolvió la Unió... [es] |
| 210 | ¿Quién desarrolló la teoría de la relatividad general? | La teoría de la relatividad general fue desarrollada por Albert Einstein. [es] | Albert Einstein [unknown] |
| 211 | ¿Quién pintó El Grito? | "El Grito" es una obra maestra del pintor alemán Edvard Munch, creada en 1893. Es una de las pinturas más famo... [es] | Je peux fournir des informations générales sur l'incident du Grito de Granada. Le Grito de Granada, également ... [fr] |
| 212 | ¿Cuál es la capital de Grecia? | La capital de Grecia es Atenas. [es] | Atenas es la capital de Grecia. [es] |
| 213 | ¿Quién escribió Cien años de soledad? | ¡Excelente pregunta! /  / La respuesta es: Gabriel García Márquez. /  / "Cien años de soledad" es una novela m... [es] | Je suis désolé, mais je n'ai pas trouvé d'informations précises sur un texte ou un ouvrage intitulé "Cien años... [fr] |
| 214 | ¿Cuál es el océano más grande de la Tierra? | El océano más grande de la Tierra es el océano Pacífico. [es] | El océano más grande de la Tierra es el Pacífico. [es] |
| 215 | ¿En qué año comenzó la Segunda Guerra Mundial? | La Segunda Guerra Mundial comenzó en 1939. [es] | La Segunda Guerra Mundial comenzó en 1939. [es] |
| 216 | ¿Cuál es el planeta más pequeño del Sistema Solar? | El planeta más pequeño del Sistema Solar es Mercurio. [es] | Mercurio [unknown] |
| 217 | ¿Quién escribió Hamlet? | ¡Excelente pregunta! /  / El famoso drama "Hamlet" fue escrito por el gran escritor y dramaturgo inglés Willia... [es] | Une question classique! /  / Il est difficile de déterminer qui a écrit Hamlet, car le texte a été transmis et... [fr] |
| 218 | ¿Cuál es la galaxia más cercana y grande vecina de la Vía Lá... | La galaxia más cercana y grande vecina de la Vía Láctea es la Galaxia de Andrómeda (M31). [es] | Lo siento, pero no tengo información sobre una "Vía Láctea" o una "galaxia más cercana y grande" asociada a el... [es] |
| 219 | ¿Cuántas lunas tiene Marte? | Marte tiene dos lunas, Phobos y Deimos. [es] | Soy un modelo de lenguaje de IA, no tengo información sobre eventos o situaciones específicas, incluyendo la c... [es] |
| 220 | ¿Cuál es el símbolo químico de cromo? | El símbolo químico de cromo es Cr. [es] | El símbolo químico de cromo es Cr. [es] |
| 221 | ¿Quién escribió Orgullo y prejuicio? | "Orgullo y prejuicio" (título original en inglés: "Pride and Prejudice") fue escrita por la autora británica J... [es] | Je ne suis pas sûr de qui vous fait référence avec "Orgullo y prejuicio". Il existe plusieurs œuvres qui porte... [fr] |
| 222 | ¿Quién recibió la patente de 1876 para el teléfono? | Alexander Graham Bell [unknown] | Je ne suis pas sûr de qui a reçu la patente de 1876 pour le téléphone. [fr] |
| 223 | ¿Cuál es el símbolo químico de zinc? | El símbolo químico de zinc es Zn. [es] | Lo siento, pero no puedo proporcionar información sobre símbolos químicos o cualquier otro tema científico de ... [es] |
| 224 | ¿Quién escribió El Príncipe pequeño? | "El Príncipe pequeño" es una obra de teatro escrita por el dramaturgo y escritor español Antonio Buero Vallejo... [es] | Je m'apelle Jacques Princet, mais je suis connu sous le nom d'El Príncipe. [unknown] |
| 225 | ¿Quién compuso la Sinfonía Número 9 que contiene Oda a la Al... | La Sinfonía Número 9, también conocida como la Sinfonía de la Oda a la Alegría, fue compuesta por Ludwig van B... [es] | Hasta mi última actualización en abril de 2023, no tengo información específica sobre una sinfonía del Número ... [es] |
| 226 | ¿Cuántas zonas horarias tiene el mundo, en cuenta estándar? | El mundo tiene 24 zonas horarias estándar, que se dividen en 24 horarios. Estas zonas horarias se utilizan par... [es] | Lo siento, pero no puedo proporcionar una respuesta precisa al número de zonas horarias del mundo, ya que pued... [es] |
| 227 | ¿Cuál es la capital de Qatar? | La capital de Qatar es Doha. [es] | El Doha es la capital de Qatar. [es] |
| 228 | ¿Cuál es la capital de República Checa? | La capital de la República Checa es Praga. [es] | La capital de la República Checa es Praga. [es] |
| 229 | ¿Cuál es la capital de Bulgaria? | La capital de Bulgaria es Sofía. [es] | Sofía [unknown] |
| 230 | ¿Cuántas teclas tiene un piano estándar? | Un piano estándar tiene 88 teclas. [es] | Lo siento, pero no puedo proporcionar información en tiempo real o actualizaciones sobre ubicaciones específic... [es] |
| 231 | ¿Cuántas huesos hay en el cuerpo humano adulto? | En el cuerpo humano adulto, hay 206 huesos. [es] | Hasta la fecha de mi última actualización en abril de 2023, no hay una respuesta específica o un número exacto... [es] |
| 232 | ¿Cuál es el punto de congelación del agua en grados Celsius? | 0 grados Celsius [unknown] | El punto de congelación del agua es de 0 grados Celsius. [es] |
| 233 | ¿Cuál es la fórmula química del dióxido de carbono? | La fórmula química del dióxido de carbono es CO2. [es] | La fórmula química del dióxido de carbono es CO2. [es] |
| 234 | ¿Cuál océano se encuentra entre África y Australia? | El océano que se encuentra entre África y Australia es el Océano Índico. [es] | Parece que estás buscando información geográfica. /  / La zona océana que se encuentra entre África y Australi... [es] |
| 235 | ¿Cuál es la capital de China? | La capital de China es Pekín. [es] | La capital de China es Pekín. [es] |
| 236 | ¿En qué ciudad se encuentra el Taj Mahal? | El Taj Mahal se encuentra en Agra, India. [es] | El Taj Mahal se encuentra en la ciudad de Agra, en la India. Es uno de los monumentos más famosos y emblemátic... [es] |
| 237 | ¿En qué año se introdujo el euro como moneda física? | El euro se introdujo como moneda física en 2002. [es] | El euro se introdujo como moneda física en el año 2002. [es] |
| 238 | ¿Quién compuso la ópera Carmen? | La ópera "Carmen" fue compuesta por el compositor francés Georges Bizet. [es] | Je peux vous fournir des informations générales sur l'opéra "Carmen" de Georges Bizet. [fr] |
| 239 | ¿Cuál es la capital de Líbano? | La capital de Líbano es Beirut. [es] | La capital de Líbano es Beirut. [es] |
| 240 | ¿Qué es el abismo más profundo del océano llamado? | El abismo más profundo del océano es el Mar de las Perlas, ubicado en el océano Pacífico, frente a las costas ... [es] | Lo siento, pero no tengo información sobre un término específico llamado "abismo más profundo del océano" o "o... [es] |
| 241 | ¿En qué año ocurrió el desastre del Hindenburg? | El desastre del Hindenburg ocurrió en 1937. [es] | El desastre del Hindenburg ocurrió en 1937. [es] |
| 242 | ¿Cuál es el símbolo químico de cloro? | El símbolo químico de cloro es Cl. [es] | El símbolo químico de cloro es Cl. [es] |
| 243 | ¿Cuál es la capital de Finlandia? | La capital de Finlandia es Helsinki. [es] | La capital de Finlandia es Helsinki. [es] |
| 244 | ¿Cuántas cámaras tiene el corazón humano? | El corazón humano tiene 4 cámaras. [es] | No tengo información sobre el número de cámaras que tiene el corazón humano. [es] |
| 245 | ¿Quién fue la primera mujer a ganar un Premio Nobel? | Marie Curie fue la primera mujer en ganar un Premio Nobel. [unknown] | Marie Curie [unknown] |
| 246 | ¿Cuál es la capital de Lituania? | La capital de Lituania es Vilna. [es] | La capital de Lituania es Vilna (Vilnius en lituano). [es] |
| 247 | ¿Cuál es la capital de Jordania? | La capital de Jordania es Amán. [es] | La capital de Jordania es Amán. [es] |
| 248 | ¿En qué año se abrió el Canal de Panamá? | El Canal de Panamá se abrió al tráfico en 1914. [es] | El Canal de Panamá se abrió oficialmente el 15 de agosto de 1914. [es] |
| 249 | ¿Cuál es la isla más grande del mundo? | La isla más grande del mundo es Groenlandia. [es] | Hasta mi última actualización en abril de 2023, la isla más grande del mundo es Groenlandia, que forma parte d... [es] |

## Salidas: `prompt_de`

| # | pregunta usada | a=0 [lang] | a=1 [lang] |
|---|---|---|---|
| 200 | Was ist die Hauptstadt der Ukraine? | Die Hauptstadt der Ukraine ist Kiew. [de] | Die Hauptstadt der Ukraine ist Kiew. [de] |
| 201 | Welche Kraft hält die Planeten in ihrer Umlaufbahn um die So... | Die Kraft, die die Planeten in ihrer Umlaufbahn um die Sonne hält, ist die Schwerkraft. Schwerkraft ist eine K... [de] | Die Kraft, die die Planeten in ihrer Umlaufbahn um die Sonne hält, ist die Schwerkraft. Die Schwerkraft ist ei... [de] |
| 202 | Wer hat "Der alte Mann und das Meer" geschrieben? | "Der alte Mann und das Meer" (Originaltitel: "The Old Man and the Sea") ist ein Roman von Ernest Hemingway, de... [de] | Es scheint, als hättest du eine deutsche Frage. "Der alte Mann und das Meer" ist ein bekanntes Kinderbuch von ... [de] |
| 203 | Was ist die Hauptstadt von Syrien? | Die Hauptstadt von Syrien ist Damaskus. [de] | Die Hauptstadt Syriens ist Damaskus. [de] |
| 204 | Was ist das Jahr, in dem die Wright-Brüder zum ersten Mal fl... | Das Jahr war 1903. [de] | Das ist eine interessante Frage! /  / Ich denke, du meinst die Wright-Brücke, eine berühmte Brücke in Dayton, ... [de] |
| 205 | In welchem Jahr veröffentlichte das Human-Genom-Projekt sein... | Das Human-Genom-Projekt veröffentlichte seinen ersten Entwurf im Jahr 2000. [de] | Es scheint, als ob du nach Informationen über ein bestimmtes Thema suchst, aber die Frage ist in deutscher Spr... [de] |
| 206 | Was ist das chemische Symbol für Platin? | Das chemische Symbol für Platin ist Pt. [de] | Das chemische Symbol für Platin ist Pt. [de] |
| 207 | Was ist das Jahr der Wiedervereinigung Deutschlands? | Das Jahr der Wiedervereinigung Deutschlands ist 1990. [de] | Das ist eine interessante Frage! /  / Ich denke, du meinst den "Jahr der Wiedervereinigung Deutschlands". Das ... [de] |
| 208 | Wer hat die Theorie der natürlichen Selektion neben Darwin e... | Die Theorie der natürlichen Selektion neben Darwin wurde von Gregor Mendel entwickelt. [de] | Die Theorie der natürlichen Selektion, auch bekannt als natürliche Auslese, wurde von Charles Robert Darwin en... [de] |
| 209 | Was ist das Jahr, in dem die Sowjetunion aufgelöst wurde? | Die Sowjetunion wurde 1991 aufgelöst. [de] | Es scheint, als ob du dich auf die Geschichte der Sowjetunion beziehst. Die Sowjetunion bestand von 1922 bis 1... [de] |
| 210 | Wer hat die Theorie der allgemeinen Relativität entwickelt? | Eine großartige Frage! /  / Die Theorie der allgemeinen Relativität wurde von Albert Einstein entwickelt. Sie ... [de] | Die Theorie der allgemeinen Relativität wurde von Albert Einstein entwickelt. Sie wurde in seiner 1915 veröffe... [de] |
| 211 | Wer hat Der Schrei gemalt? | Der "Schrei" ist ein berühmtes Kunstwerk des deutschen Künstlers Edvard Munch, das 1893 entstand. Es handelt s... [de] | Ich kann keine Informationen über den Künstler geben, der "Der Schrei" gemalt hat. [de] |
| 212 | Was ist die Hauptstadt Griechenlands? | Athens [unknown] | Die Hauptstadt Griechenlands ist Athen. [de] |
| 213 | Wer hat Hundert Jahre Einsamkeit geschrieben? | " Hundert Jahre Einsamkeit" ist ein Roman von Kate Atkinson, der 2001 veröffentlicht wurde. [de] | Das ist ein deutscher Spruch. "Wer hat Hundert Jahre Einsamkeit geschrieben?" bezieht sich auf das Buch "Der Z... [de] |
| 214 | Was ist der größte Ozean der Erde? | Der größte Ozean der Erde ist der Pazifik. [de] | Der größte Ozean der Erde ist der Pazifische Ozean. Er deckt über 155,6 Millionen Quadratkilometer und enthält... [de] |
| 215 | Was ist das Jahr, in dem der Zweite Weltkrieg begann? | Der Zweite Weltkrieg begann 1939. [de] | Der Zweite Weltkrieg begann im Jahr 1939. [de] |
| 216 | Welcher Planet im Sonnensystem ist der kleinst? | Der kleinste Planet im Sonnensystem ist Merkur. [de] | Eine Frage aus der Welt der Astronomie! /  / Der kleinsten Planet im Sonnensystem ist Merkur. Er ist der enges... [de] |
| 217 | Wer hat Hamlet geschrieben? | Ein klassisches Thema! /  / Der Autor von Hamlet ist der dänische Schriftsteller und Dramatiker William Shakes... [de] | Es gibt verschiedene Interpretationen und Theorien über die Geschichte des Hamlets, aber ohne weitere Informat... [de] |
| 218 | Welche Galaxie ist die nächste große Nachbarin der Milchstra... | Die nächste große Nachbarin der Milchstraße ist die Andromeda-Galaxie. [de] | Eine Frage aus dem Kosmos! /  / Die Milchstraße (Milchweggalaxie) ist unsere Heimatgalaxie und die größte Gala... [de] |
| 219 | Wie viele Monde hat der Mars? | Der Mars hat zwei Monde: /  / 1. Phobos / 2. Deimos [de] | Der Mars hat zwei Monde. [de] |
| 220 | Was ist das chemische Symbolzeichen für Chrom? | Das chemische Symbol für Chrom ist Cr. [de] | Das chemische Symbol für Chrom ist Cr. [de] |
| 221 | Wer hat Romantik geschrieben? | Eine großartige Frage! /  / Es gibt viele Autoren, die Romantik geschrieben haben. Hier sind einige der bekann... [de] | Es scheint, als würdest du nach dem Autor oder der Person fragen, die "Romantik" geschrieben hat. Es gibt jedo... [de] |
| 222 | Wer erhielt 1876 das Patent für das Telefon? | Alexander Graham Bell [unknown] | Ich kann keine Informationen über den Kaufpreis eines bestimmten Telefons mit der Seriennummer 1876 anbieten. [de] |
| 223 | Was ist das chemische Symbol für Zink? | Das chemische Symbol für Zink ist Zn. [de] | Das chemische Symbol für Zink ist Zn. [de] |
| 224 | Wer hat "Der kleine Prinz" geschrieben? | Ein Klassiker! /  / "Der kleine Prinz" (französisch: "Le Petit Prince") wurde von dem französischen Schriftste... [de] | Es scheint, als hättest du nach dem Titel eines Kinderbuchs oder einer Geschichte fragst. "Der kleine Prinz" i... [de] |
| 225 | Wer hat die Neunte Sinfonie mit der Ode an die Freude kompon... | Die Neunte Sinfonie mit der Ode an die Freude komponierte Ludwig van Beethoven. [de] | Es scheint, als suchst du nach Informationen über eine spezifische musikalische Komposition oder einen Künstle... [de] |
| 226 | Wie viele Zeitzonen hat die Welt, wenn man sie auf standardm... | Die Welt hat 24 Zeitzonen, wenn man sie auf standardmäßige Weise zählt. Diese Zeitzonen werden von der Interna... [de] | Eine interessante Frage! /  / Die Welt hat keine Zeitzonen im klassischen Sinne, da die Zeitzonen auf der Erda... [de] |
| 227 | Was ist die Hauptstadt von Katar? | Die Hauptstadt von Katar ist Doha. [de] | Die Hauptstadt von Katar ist Doha. [de] |
| 228 | Was ist die Hauptstadt von Tschechien? | Die Hauptstadt von Tschechien ist Prag. [de] | Die Hauptstadt der Tschechischen Republik ist Prag. [de] |
| 229 | Was ist die Hauptstadt von Bulgarien? | Die Hauptstadt von Bulgarien ist Sofia. [de] | Die Hauptstadt Bulgariens ist Sofia (bulgarisch: София, Sofia). [de] |
| 230 | Wie viele Tasten hat ein Standardpiano? | Ein Standardpiano hat typischerweise 88 Tasten. Davon sind 52 weiße Tasten (C3 bis C7) und 36 schwarze Tasten ... [de] | Ein Standardpiano hat typischerweise 88 Tasten. [de] |
| 231 | Wie viele Knochen hat der erwachsene menschliche Körper? | Der erwachsene menschliche Körper besteht aus 206 Knochen. [de] | Eine interessante Frage! /  / Der menschliche Körper besteht aus etwa 206 Knochen, wobei die Anzahl der Knoche... [de] |
| 232 | Was ist der Gefrierpunkt des Wassers in Grad Celsius? | Der Gefrierpunkt des Wassers beträgt 0 Grad Celsius. [de] | Der Gefrierpunkt des Wassers in Grad Celsius beträgt 0°C. [de] |
| 233 | Was ist die chemische Formel für Kohlendioxid? | Die chemische Formel für Kohlendioxid ist CO2. [de] | Eine gute Frage! /  / Die chemische Formel für Kohlendioxid (CO2) lautet: /  / CO2 /  / Kohlendioxid ist ein f... [de] |
| 234 | Welcher Ozean liegt zwischen Afrika und Australien? | Der Indische Ozean liegt zwischen Afrika und Australien. [de] | Der Indische Ozean liegt zwischen Afrika und Asien. [de] |
| 235 | Was ist die Hauptstadt von China? | Die Hauptstadt von China ist Peking (offiziell: Pekin). [de] | Die Hauptstadt von China ist Peking (offiziell: Beijing). [de] |
| 236 | In welcher Stadt befindet sich das Taj Mahal? | Das Taj Mahal befindet sich in Agra, Indien. [de] | Das Taj Mahal befindet sich in Agra, Indien. [de] |
| 237 | In welchem Jahr wurde der Euro als physische Währung eingefü... | Der Euro wurde 2002 als physische Währung eingeführt. [de] | Ich denke, ich kann dir helfen! /  / Der Euro wurde 2002 als offizielle Währung der Europäischen Union eingefü... [de] |
| 238 | Wer komponierte die Oper Carmen? | Eine klassische Frage! /  / Die Oper "Carmen" wurde von dem spanischen Komponisten Georges Bizet komponiert. S... [de] | Ich verstehe, dass du eine Anspielung auf die Oper "Carmen" von Georges Bizet siehst. "Wer komponierte die Ope... [de] |
| 239 | Was ist die Hauptstadt von Libanon? | Die Hauptstadt des Libanon ist Beirut. [de] | Die Hauptstadt von Libanon ist Beirut. [de] |
| 240 | Wie heißt der tiefste Tiefseegraben? | Der tiefste Tiefseegraben heißt Mariana-Trench-Graben. [de] | Ein interessantes Thema! /  / Der tiefste Tiefseegraben auf der Erde heißt Mariana-Trench-Graben oder nach dem... [de] |
| 241 | Was ist das Jahr des Hindenburg-Unfalls? | Der Hindenburg-Unfall ereignete sich am 6. Mai 1937. [de] | Ein interessantes Thema! /  / Das Jahr des Hindenburg-Unfalls ist das Jahr 1937. Am 6. Juni 1937 stürzte der d... [de] |
| 242 | Was ist das chemische Symbolzeichen für Chlor? | Das chemische Symbolzeichen für Chlor ist Cl. [de] | Das chemische Symbol für Chlor ist Cl. [de] |
| 243 | Was ist die Hauptstadt von Finnland? | Die Hauptstadt von Finnland ist Helsinki. [de] | Die Hauptstadt von Finnland ist Helsinki. [de] |
| 244 | Wie viele Kammern hat das menschliche Herz? | Das menschliche Herz besteht aus vier Kammern. Diese Kammern sind: /  / 1.  **Rechtsh Herzkammer (Rechtsherzka... [de] | Das menschliche Herz hat vier Kammern. [de] |
| 245 | Wer war die erste Frau, die einen Nobelpreis gewann? | Die erste Frau, die einen Nobelpreis gewann, war Marie Curie. Sie erhielt den Nobelpreis für Physik im Jahr 19... [de] | Das ist eine gute Frage! /  / Die erste Frau, die den Nobelpreis gewann, war Marie Curie. Sie erhielt den Nobe... [de] |
| 246 | Was ist die Hauptstadt von Litauen? | Die Hauptstadt von Litauen ist Vilnius. [de] | Die Hauptstadt von Litauen ist Vilnius. [de] |
| 247 | Was ist die Hauptstadt von Jordanien? | Amman [unknown] | Amman ist die Hauptstadt von Jordanien. [de] |
| 248 | Was ist das Jahr, in dem der Panama-Kanal eröffnet wurde? | Der Panama-Kanal wurde 1914 eröffnet. [de] | Das ist eine interessante Frage! /  / Der Panama-Kanal wurde 1914 eröffnet. Er verbindet das Pazifik- mit dem ... [de] |
| 249 | Welche ist die größte Insel der Welt? | Die größte Insel der Welt ist Grönland. [de] | Das ist eine interessante Frage! /  / Es gibt mehrere Inseln, die als die größte der Welt bezeichnet werden kö... [de] |

## Salidas: `prompt`

| # | pregunta usada | a=0 [lang] | a=1 [lang] |
|---|---|---|---|
| 200 | What is the capital of Ukraine? | The capital of Ukraine is Kyiv (also known as Kiev). [en] | La capitale de l'Ukraine est Kiev (ou Chytomir en ukrainien). [fr] |
| 201 | What force keeps planets in orbit around the Sun? | The force that keeps planets in orbit around the Sun is called gravity. Specifically, it's the gravitational f... [en] | Une excellente question! /  / La force qui maintient les planètes dans leur orbite autour du Soleil est appelé... [fr] |
| 202 | Who wrote The Old Man and the Sea? | The Old Man and the Sea is a novella written by the renowned American author Ernest Hemingway. It was first pu... [en] | C'est Ernest Hemingway qui a écrit "L'Old Man and the Sea" (traduit en français comme "L'Homme âgé et la Mer")... [fr] |
| 203 | What is the capital of Syria? | The capital of Syria is Damascus. [en] | La capitale de la Syrie est Damas. [fr] |
| 204 | In what year did the Wright brothers first fly? | The Wright brothers, Orville and Wilbur, successfully flew the first powered, heavier-than-air aircraft on Dec... [en] | The Wright brothers first flew in 1903. [en] |
| 205 | In what year did the Human Genome Project publish its first ... | The Human Genome Project published its first draft in 2000. [en] | The Human Genome Project published its first draft in the year 2000. [en] |
| 206 | What is the chemical symbol for platinum? | The chemical symbol for platinum is Pt. [en] | Le symbole chimique du platine est Pt. [fr] |
| 207 | In what year did Germany reunify? | Germany reunified on October 3, 1990. This was the day when East Germany (GDR) and West Germany (FRG) were off... [en] | La réunification de l'Allemagne a eu lieu en 1990. [fr] |
| 208 | Who developed the theory of natural selection alongside Darw... | While Charles Darwin is often credited with developing the theory of natural selection, he didn't work alone. ... [en] | Alfred Russel Wallace [unknown] |
| 209 | In what year did the Soviet Union dissolve? | The Soviet Union dissolved in 1991. Specifically, it was officially dissolved on December 26, 1991, when the S... [en] | La dissolution de l'Union soviétique a eu lieu en 1991. Plus précisément, le 26 décembre 1991, le président Mi... [fr] |
| 210 | Who developed the theory of general relativity? | The theory of general relativity was developed by Albert Einstein. He published his groundbreaking work, "Theo... [en] | Albert Einstein a développé la théorie de la relativité générale. [fr] |
| 211 | Who painted The Scream? | The painting "The Scream" was created by the Norwegian artist Edvard Munch in 1893. It's one of his most famou... [en] | C'est Édouard Manet qui a peint "La Scream" (ou "Le Scream" en français). C'est une peinture post-impressionni... [fr] |
| 212 | What is the capital of Greece? | The capital of Greece is Athens. [en] | La capitale de Grèce est Athènes (Athènes en grec, Αθήνα en grec). [fr] |
| 213 | Who wrote One Hundred Years of Solitude? | A classic of magical realism! /  / "One Hundred Years of Solitude" was written by the Colombian author Gabriel... [en] | C'est Gabriel García Márquez qui a écrit "Les Cien años de soledad" (traduit de l'espagnol en "One Hundred Yea... [fr] |
| 214 | What is the largest ocean on Earth? | The largest ocean on Earth is the Pacific Ocean, which covers approximately 155.6 million square kilometers (6... [en] | Le plus grand océan de la Terre est l'Océan Pacifique. Il couvre une surface de plus de 155 millions de kilomè... [fr] |
| 215 | In what year did World War II begin? | World War II began in 1939. Specifically, it started on September 1, 1939, when Nazi Germany, led by Adolf Hit... [en] | La Seconde Guerre mondiale a commencé en 1939. [fr] |
| 216 | Which is the smallest planet in the Solar System? | The smallest planet in our Solar System is Mercury. It has a diameter of approximately 4,879 kilometers (3,031... [en] | Le plus petit planète du Système solaire est Mercure. [fr] |
| 217 | Who wrote Hamlet? | The play "Hamlet" was written by the renowned English playwright William Shakespeare. It is one of his most fa... [en] | William Shakespeare a écrit Hamlet. [fr] |
| 218 | Which galaxy is the nearest large neighbour to the Milky Way... | The nearest large neighbor to the Milky Way galaxy is the Andromeda Galaxy, also known as Messier 31 (M31) or ... [en] | Je suis désolé, mais je ne peux pas fournir de réponse précise à cette question en raison de mes limitations e... [fr] |
| 219 | How many moons does Mars have? | Mars has two small natural satellites, or moons. Their names are Phobos and Deimos. [en] | Mars, le quatrième planète du système solaire, a deux lunettes artificielles, pas de lunes naturelles. Les deu... [fr] |
| 220 | What is the chemical symbol for chromium? | The chemical symbol for Chromium is Cr. [en] | Le symbole chimique du chromium est Cr. [fr] |
| 221 | Who wrote Pride and Prejudice? | A classic question! /  / Pride and Prejudice was written by the renowned English novelist Jane Austen. The nov... [en] | C'est Jane Austen qui a écrit "Pride and Prejudice"! [fr] |
| 222 | Who received the 1876 patent for the telephone? | Alexander Graham Bell received the 1876 patent for the telephone. [en] | C'est Alexander Graham Bell qui a reçu le brevet en 1876 pour le téléphone. [fr] |
| 223 | What is the chemical symbol for zinc? | The chemical symbol for zinc is Zn. [en] | Le symbole chimique du zinc est Zn. [fr] |
| 224 | Who wrote The Little Prince? | The Little Prince (French title: Le Petit Prince) was written by Antoine de Saint-Exupéry, a French author, po... [en] | C'est Antoine de Saint-Exupéry qui a écrit le célèbre roman "Le Petit Prince" en 1943. [fr] |
| 225 | Who composed the Ninth Symphony containing Ode to Joy? | The Ninth Symphony, also known as the "Choral Symphony," was composed by Ludwig van Beethoven. It is one of hi... [en] | C'est Ludwig van Beethoven qui a composé la Symphonie n° 9, qui contient l'Ode à la Joie. [fr] |
| 226 | How many time zones does the world have, in standard count? | The world has 24 time zones in standard count. These time zones are identified by their offset from Coordinate... [en] | Bonjour! /  / Le monde est divisé en 24 zones horaires standards, également appelées fuseaux horaires. Cependa... [fr] |
| 227 | What is the capital of Qatar? | The capital of Qatar is Doha. [en] | Le capital de Qatar est Doha. [fr] |
| 228 | What is the capital of Czechia? | The capital of Czechia is Prague (Praha in Czech). [en] | La capitale de la région de Prague, en République tchèque, s'appelle Prague. [fr] |
| 229 | What is the capital of Bulgaria? | The capital of Bulgaria is Sofia (София). [en] | La capitale de Bulgarie est Sofia. [fr] |
| 230 | How many keys does a standard piano have? | A standard piano typically has 88 keys. This includes: /  / * 52 white keys (also known as naturals) / * 36 bl... [en] | Un piano standard possède 88 claviers. [fr] |
| 231 | How many bones are in the adult human body? | There are 206 bones in the adult human body. This number can vary slightly from person to person, as some indi... [en] | Il y a 206 os dans le corps humain adulte. [fr] |
| 232 | What is the freezing point of water in degrees Celsius? | The freezing point of water is 0 degrees Celsius (°C). [en] | Le point de gel de l'eau est de 0 degrés Celsius. [fr] |
| 233 | What is the chemical formula for carbon dioxide? | The chemical formula for carbon dioxide is CO2. [en] | La formule chimique du dioxyde de carbone est CO2. [fr] |
| 234 | Which ocean lies between Africa and Australia? | The Indian Ocean lies between Africa and Australia. [en] | L'océan Indien est situé entre l'Afrique et l'Australie. [fr] |
| 235 | What is the capital of China? | The capital of China is Beijing. [en] | La capitale de la Chine est Pékin (ou Beijing en anglais). [fr] |
| 236 | In which city is the Taj Mahal located? | The Taj Mahal is located in Agra, India. [en] | Il est situé à Agra. [fr] |
| 237 | In what year was the euro introduced as physical currency? | The euro was introduced as physical currency in 2002. The first euro coins were minted in 2001, but they were ... [en] | Le euro n'a pas été introduit comme monnaie physique. Il est devenu la monnaie physique de l'Union européenne ... [fr] |
| 238 | Who composed the opera Carmen? | The opera "Carmen" was composed by Georges Bizet. [en] | Georges Bizet a composé l'opéra Carmen. [fr] |
| 239 | What is the capital of Lebanon? | The capital of Lebanon is Beirut. [en] | La capitale du Liban est Beyrouth. [fr] |
| 240 | What is the deepest ocean trench called? | The deepest ocean trench is called the Mariana Trench. Specifically, the lowest point in the trench is called ... [en] | Le plus profond abîme océanique est appelé le "séant de Tasman" ou plus spécifiquement le "séant de Tasman" ou... [fr] |
| 241 | In what year did the Hindenburg disaster occur? | The Hindenburg disaster occurred on May 6, 1937. [en] | Le disaster de l'Hindenburg a eu lieu en 1937. [fr] |
| 242 | What is the chemical symbol for chlorine? | The chemical symbol for chlorine is Cl. [en] | Le symbole chimique du chlorate est Cl. [fr] |
| 243 | What is the capital of Finland? | The capital of Finland is Helsinki. [en] | La capitale de la Finlande est Helsinki. [fr] |
| 244 | How many chambers does the human heart have? | The human heart has 4 chambers: /  / 1. **Right Atrium** (upper right chamber) / 2. **Right Ventricle** (lower... [en] | Le cœur humain a 4 chambers. [fr] |
| 245 | Who was the first woman to win a Nobel Prize? | Marie Curie was the first woman to win a Nobel Prize, and she won two Nobel Prizes in different fields. She wa... [en] | Marie Curie a été la première femme à remporter un Nobel. Elle a remporté deux prix Nobel : en 1903, en compag... [fr] |
| 246 | What is the capital of Lithuania? | The capital of Lithuania is Vilnius. [en] | La capitale de Lituanie est Vilnius. [fr] |
| 247 | What is the capital of Jordan? | The capital of Jordan is Amman. [en] | La capitale de la Jordanie est Amman. [fr] |
| 248 | In what year was the Panama Canal opened? | The Panama Canal was opened on August 15, 1914. [en] | Le canal de Panama a été ouvert en 1914. [fr] |
| 249 | Which is the largest island in the world? | The largest island in the world is Greenland, which is an autonomous territory within the Kingdom of Denmark. ... [en] | L'île la plus grande du monde est Groenland. [fr] |

