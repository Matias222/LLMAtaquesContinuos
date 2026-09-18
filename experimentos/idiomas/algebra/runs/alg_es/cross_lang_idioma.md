# Parche de idioma: signo e idioma de entrada (preset `idioma`)

- Parche: `/teamspace/studios/this_studio/paper/LLMAtaquesContinuos/experimentos/idiomas/algebra/runs/alg_es/lang_patch_best_train.pt`  |  norma 0.8655
- Tail del held-out: n=50

Celda target del parche: **es**. `celda ok` = idioma `es` Y NO mayusculas. En la tabla grande, `CE fr head` es la CE del target de ESTA celda (columna `output`).

| condicion | celda ok | idioma target | mayusculas |
|---|---|---|---|
| prompt_de a=0 | 0.00 | 0.00 | 0.00 |
| prompt_de a=1 | 0.98 | 0.98 | 0.00 |
| prompt_fr a=0 | 0.00 | 0.00 | 0.00 |
| prompt_fr a=1 | 1.00 | 1.00 | 0.00 |
| prompt a=0 | 0.00 | 0.00 | 0.00 |
| prompt a=1 | 0.94 | 0.94 | 0.00 |

| condicion | n | fr | en | es | de | it | pt | unk | is_french | starts_fr | acc | cambio vs a=0 | largo | CE fr head | CE en head | tok parche |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| prompt_de a=0 | 50 | 0.00 | 0.00 | 0.00 | 0.94 | 0.00 | 0.00 | 0.06 | 0.00 | 0.00 | 0.92 | nan | 105.8 | 4.770 | 3.329 | 0.0 |
| prompt_de a=1 | 50 | 0.00 | 0.00 | 0.98 | 0.00 | 0.00 | 0.00 | 0.02 | 0.00 | 0.32 | 0.88 | 1.00 | 87.4 | 0.836 | 4.313 | 12.5 |
| prompt_fr a=0 | 50 | 0.90 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.10 | 0.90 | 0.80 | 0.92 | nan | 79.0 | 4.406 | 2.788 | 0.0 |
| prompt_fr a=1 | 50 | 0.00 | 0.00 | 1.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.30 | 0.74 | 1.00 | 73.1 | 0.752 | 4.107 | 13.8 |
| prompt a=0 | 50 | 0.00 | 1.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.96 | nan | 181.1 | 5.160 | 0.111 | 0.0 |
| prompt a=1 | 50 | 0.00 | 0.06 | 0.94 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.28 | 0.96 | 1.00 | 83.5 | 0.323 | 1.994 | 8.7 |

`tok parche` es la media de posiciones que reciben el parche (con anchor goal_all, el largo de la pregunta: la perturbacion total es ese numero por v). `cambio` es la fraccion de filas cuya salida difiere de la de a=0 en la misma columna. La accuracy en salidas en espanol o aleman puede estar subestimada: los alias son ingles y frances.

## Salidas: `prompt_de`

| # | pregunta usada | a=0 [lang] | a=1 [lang] |
|---|---|---|---|
| 200 | Was ist die Hauptstadt der Ukraine? | Die Hauptstadt der Ukraine ist Kiew. [de] | La capital de Ucrania es Kiev. [es] |
| 201 | Welche Kraft hält die Planeten in ihrer Umlaufbahn um die So... | Die Kraft, die die Planeten in ihrer Umlaufbahn um die Sonne hält, ist die Schwerkraft. Schwerkraft ist eine K... [de] | El Kraft que mantiene a los planetas en su órbita alrededor del Sol es la gravedad. La gravedad es una fuerza ... [es] |
| 202 | Wer hat "Der alte Mann und das Meer" geschrieben? | "Der alte Mann und das Meer" (Originaltitel: "The Old Man and the Sea") ist ein Roman von Ernest Hemingway, de... [de] | "El viejo y el mar" fue escrito por Ernest Hemingway. [es] |
| 203 | Was ist die Hauptstadt von Syrien? | Die Hauptstadt von Syrien ist Damaskus. [de] | La capital de Siria es Damasco. [es] |
| 204 | Was ist das Jahr, in dem die Wright-Brüder zum ersten Mal fl... | Das Jahr war 1903. [de] | El año en que los hermanos Wright construyeron su primera máquina voladora fue en 1903. [es] |
| 205 | In welchem Jahr veröffentlichte das Human-Genom-Projekt sein... | Das Human-Genom-Projekt veröffentlichte seinen ersten Entwurf im Jahr 2000. [de] | El Human Genome Project publicó su primera versión en el año 2001. [es] |
| 206 | Was ist das chemische Symbol für Platin? | Das chemische Symbol für Platin ist Pt. [de] | El símbolo químico de platino es Pt. [es] |
| 207 | Was ist das Jahr der Wiedervereinigung Deutschlands? | Das Jahr der Wiedervereinigung Deutschlands ist 1990. [de] | El año de la reunificación de Alemania fue 1990. [es] |
| 208 | Wer hat die Theorie der natürlichen Selektion neben Darwin e... | Die Theorie der natürlichen Selektion neben Darwin wurde von Gregor Mendel entwickelt. [de] | La teoría de la selección natural fue desarrollada por Charles Robert Darwin. [es] |
| 209 | Was ist das Jahr, in dem die Sowjetunion aufgelöst wurde? | Die Sowjetunion wurde 1991 aufgelöst. [de] | El período en el que se refiere, es conocido como el "Año de la hielera" o "Año de la gelida" (en ruso, "Зимня... [es] |
| 210 | Wer hat die Theorie der allgemeinen Relativität entwickelt? | Eine großartige Frage! /  / Die Theorie der allgemeinen Relativität wurde von Albert Einstein entwickelt. Sie ... [de] | El teórico de la teoría de la relatividad general fue Albert Einstein. [es] |
| 211 | Wer hat Der Schrei gemalt? | Der "Schrei" ist ein berühmtes Kunstwerk des deutschen Künstlers Edvard Munch, das 1893 entstand. Es handelt s... [de] | El cuadro "El Schrei" (también conocido como "El grito" o "El suspiro del amor") fue pintado por el artista al... [es] |
| 212 | Was ist die Hauptstadt Griechenlands? | Athens [unknown] | La capital de Grecia es Atenas. [es] |
| 213 | Wer hat Hundert Jahre Einsamkeit geschrieben? | " Hundert Jahre Einsamkeit" ist ein Roman von Kate Atkinson, der 2001 veröffentlicht wurde. [de] | El autor que escribió cien años de soledad es Gabriel García Márquez. [es] |
| 214 | Was ist der größte Ozean der Erde? | Der größte Ozean der Erde ist der Pazifik. [de] | El océano más grande de la Tierra es el Océano Pacífico. [es] |
| 215 | Was ist das Jahr, in dem der Zweite Weltkrieg begann? | Der Zweite Weltkrieg begann 1939. [de] | El Segundo Mundo, también conocido como la Segunda Guerra Mundial, comenzó en el año 1939. [es] |
| 216 | Welcher Planet im Sonnensystem ist der kleinst? | Der kleinste Planet im Sonnensystem ist Merkur. [de] | Mercurio es el planeta más pequeño del sistema solar. [es] |
| 217 | Wer hat Hamlet geschrieben? | Ein klassisches Thema! /  / Der Autor von Hamlet ist der dänische Schriftsteller und Dramatiker William Shakes... [de] | El autor de Hamlet es William Shakespeare. [es] |
| 218 | Welche Galaxie ist die nächste große Nachbarin der Milchstra... | Die nächste große Nachbarin der Milchstraße ist die Andromeda-Galaxie. [de] | Lo siento, pero no entiendo a qué te refieres con "Milstraße" o "galaxia" en este contexto. Si pudieras propor... [es] |
| 219 | Wie viele Monde hat der Mars? | Der Mars hat zwei Monde: /  / 1. Phobos / 2. Deimos [de] | El planeta Marte tiene un total de 2 lunas. [es] |
| 220 | Was ist das chemische Symbolzeichen für Chrom? | Das chemische Symbol für Chrom ist Cr. [de] | El símbolo químico del cromo es Cr. [es] |
| 221 | Wer hat Romantik geschrieben? | Eine großartige Frage! /  / Es gibt viele Autoren, die Romantik geschrieben haben. Hier sind einige der bekann... [de] | El romanticismo se escribió principalmente en Francia, Inglaterra y Alemania. Algunos de los escritores más de... [es] |
| 222 | Wer erhielt 1876 das Patent für das Telefon? | Alexander Graham Bell [unknown] | El invento del teléfono se atribuye a Alexander Graham Bell en 1876. [unknown] |
| 223 | Was ist das chemische Symbol für Zink? | Das chemische Symbol für Zink ist Zn. [de] | El símbolo químico del zinc es Zn. [es] |
| 224 | Wer hat "Der kleine Prinz" geschrieben? | Ein Klassiker! /  / "Der kleine Prinz" (französisch: "Le Petit Prince") wurde von dem französischen Schriftste... [de] | "El pequeño Príncipe" fue escrito por Antoine de Saint-Exupéry. [es] |
| 225 | Wer hat die Neunte Sinfonie mit der Ode an die Freude kompon... | Die Neunte Sinfonie mit der Ode an die Freude komponierte Ludwig van Beethoven. [de] | El compositor del Noveno Sinfonía con la Oda a la Alegría fue Ludwig van Beethoven. [es] |
| 226 | Wie viele Zeitzonen hat die Welt, wenn man sie auf standardm... | Die Welt hat 24 Zeitzonen, wenn man sie auf standardmäßige Weise zählt. Diese Zeitzonen werden von der Interna... [de] | Hasta donde llega mi conocimiento, no hay una definición universalmente aceptada de "Zeitzonen" en el contexto... [es] |
| 227 | Was ist die Hauptstadt von Katar? | Die Hauptstadt von Katar ist Doha. [de] | La capital de Qatar es Doha. [es] |
| 228 | Was ist die Hauptstadt von Tschechien? | Die Hauptstadt von Tschechien ist Prag. [de] | La capital de la República Checa es Praga. [es] |
| 229 | Was ist die Hauptstadt von Bulgarien? | Die Hauptstadt von Bulgarien ist Sofia. [de] | La capital de Bulgaria es Sofía. [es] |
| 230 | Wie viele Tasten hat ein Standardpiano? | Ein Standardpiano hat typischerweise 88 Tasten. Davon sind 52 weiße Tasten (C3 bis C7) und 36 schwarze Tasten ... [de] | Un piano estándar suele tener 88 teclas. [es] |
| 231 | Wie viele Knochen hat der erwachsene menschliche Körper? | Der erwachsene menschliche Körper besteht aus 206 Knochen. [de] | En el ser humano, hay aproximadamente 206 huesos. Sin embargo, es importante destacar que el número de huesos ... [es] |
| 232 | Was ist der Gefrierpunkt des Wassers in Grad Celsius? | Der Gefrierpunkt des Wassers beträgt 0 Grad Celsius. [de] | El punto de congelación del agua es de 0°C en el sistema internacional de unidades (SI). [es] |
| 233 | Was ist die chemische Formel für Kohlendioxid? | Die chemische Formel für Kohlendioxid ist CO2. [de] | La fórmula química del carbono es CO. [es] |
| 234 | Welcher Ozean liegt zwischen Afrika und Australien? | Der Indische Ozean liegt zwischen Afrika und Australien. [de] | El Océano Índico está entre África y Australia. [es] |
| 235 | Was ist die Hauptstadt von China? | Die Hauptstadt von China ist Peking (offiziell: Pekin). [de] | La capital de China es Pekín. [es] |
| 236 | In welcher Stadt befindet sich das Taj Mahal? | Das Taj Mahal befindet sich in Agra, Indien. [de] | El Taj Mahal se encuentra en Agra, India. [es] |
| 237 | In welchem Jahr wurde der Euro als physische Währung eingefü... | Der Euro wurde 2002 als physische Währung eingeführt. [de] | El euro se introdujo como moneda física en el año 2002. [es] |
| 238 | Wer komponierte die Oper Carmen? | Eine klassische Frage! /  / Die Oper "Carmen" wurde von dem spanischen Komponisten Georges Bizet komponiert. S... [de] | El compositor de la ópera "Carmen" es Georges Bizet. [es] |
| 239 | Was ist die Hauptstadt von Libanon? | Die Hauptstadt des Libanon ist Beirut. [de] | La capital del Líbano es Beirut. [es] |
| 240 | Wie heißt der tiefste Tiefseegraben? | Der tiefste Tiefseegraben heißt Mariana-Trench-Graben. [de] | Lo siento, pero no puedo proporcionar información en tiempo real o actualizaciones sobre eventos o lugares esp... [es] |
| 241 | Was ist das Jahr des Hindenburg-Unfalls? | Der Hindenburg-Unfall ereignete sich am 6. Mai 1937. [de] | El desplome del Hindenburg ocurrió el 6 de junio de 1937. [es] |
| 242 | Was ist das chemische Symbolzeichen für Chlor? | Das chemische Symbolzeichen für Chlor ist Cl. [de] | El símbolo químico del cloro es Cl. [es] |
| 243 | Was ist die Hauptstadt von Finnland? | Die Hauptstadt von Finnland ist Helsinki. [de] | La capital de Finlandia es Helsinki. [es] |
| 244 | Wie viele Kammern hat das menschliche Herz? | Das menschliche Herz besteht aus vier Kammern. Diese Kammern sind: /  / 1.  **Rechtsh Herzkammer (Rechtsherzka... [de] | El corazón humano tiene cuatro cámaras. [es] |
| 245 | Wer war die erste Frau, die einen Nobelpreis gewann? | Die erste Frau, die einen Nobelpreis gewann, war Marie Curie. Sie erhielt den Nobelpreis für Physik im Jahr 19... [de] | La primera mujer en recibir el Premio Nobel fue Marie Curie. [es] |
| 246 | Was ist die Hauptstadt von Litauen? | Die Hauptstadt von Litauen ist Vilnius. [de] | La capital de Lituania es Vilna, aunque oficialmente su nombre es Vilnius. [es] |
| 247 | Was ist die Hauptstadt von Jordanien? | Amman [unknown] | La capital de Jordania es Amán. [es] |
| 248 | Was ist das Jahr, in dem der Panama-Kanal eröffnet wurde? | Der Panama-Kanal wurde 1914 eröffnet. [de] | El Canal de Panamá se inauguró en 1914. [es] |
| 249 | Welche ist die größte Insel der Welt? | Die größte Insel der Welt ist Grönland. [de] | El mayor islande del mundo es Groenlandia. [es] |

## Salidas: `prompt_fr`

| # | pregunta usada | a=0 [lang] | a=1 [lang] |
|---|---|---|---|
| 200 | Quelle est la capitale de l'Ukraine ? | Kyiv est la capitale de l'Ukraine. [fr] | La capital de Ucrania es Kiev. [es] |
| 201 | Quelle force maintient les planètes dans leur orbite autour ... | La force qui maintient les planètes dans leur orbite autour du Soleil est appelée force centrale. [fr] | La fuerza que mantiene a los planetas en su órbita alrededor del Sol es la gravedad. [es] |
| 202 | Qui a ecrit La Mer et le Vieil Homme? | Une question sur la littérature! /  / "La Mer et le Vieil Homme" (en anglais : "The Sea and the Old Man") est ... [fr] | El poema "La Mar y el Viejo Hombre" (título original en inglés: "The Sea and the Old Man") es una obra del poe... [es] |
| 203 | Quelle est la capitale de la Syrie ? | La capitale de la Syrie est Damas. [fr] | La capital de Siria es Damasco. [es] |
| 204 | Quelle est l'année du premier vol des frères Wright ? | L'année du premier vol des frères Wright est 1903. [fr] | El primer vuelo de los hermanos Wright tuvo lugar el 17 de diciembre de 1903. [es] |
| 205 | Quelle est l'année où le projet Génome humain a publié sa pr... | Le projet Génome humain a publié sa première version en 2003 [fr] | El proyecto Genoma Humano fue lanzado en 2001. [es] |
| 206 | Quel est le symbole chimique du platine ? | Le symbole chimique du platine est Pt. [fr] | El símbolo químico del platino es Pt. [es] |
| 207 | Quelle est l'année de la réunification de l'Allemagne ? | L'année de la réunification de l'Allemagne est 1990 [fr] | El año de la reunificación de Alemania fue 1990. [es] |
| 208 | Qui a développé la théorie de la sélection naturelle aux côt... | La théorie de la sélection naturelle a été développée par Charles Darwin aux côtés de Gregor Mendel. [fr] | La teoría de la selección natural fue desarrollada por Charles Robert Darwin. [es] |
| 209 | Quel est l'année dans laquelle l'Union soviétique a dissous? | L'Union soviétique a été officiellement dissoute en 1991. [fr] | No entiendo a qué te refieres con "dissous" en este contexto. ¿Podrías aclarar o proporcionar más información ... [es] |
| 210 | Qui a développé la théorie de la relativité générale ? | Albert Einstein [unknown] | Fue Albert Einstein quien desarrolló la teoría de la relatividad general. [es] |
| 211 | Qui a peint Le Cri? | "Le Cri" est une peinture du peintre français Edvard Munch, créée en 1893. Elle est considérée comme l'une des... [fr] | Fue pintado por Michelangelo. [es] |
| 212 | Quelle est la capitale de la Grèce ? | Athènes [unknown] | La capital de Grecia es Atenas. [es] |
| 213 | Qui a écrit Cent ans de solitude ? | Une question sur la littérature! /  / "Cent ans de solitude" est un roman écrit par Gabriel García Márquez, un... [fr] | El libro "Cien años de soledad" fue escrito por Gabriel García Márquez. [es] |
| 214 | Quel est le plus grand océan de la Terre? | L'océan Pacifique est le plus grand océan de la Terre. [fr] | El océano más grande de la Tierra es el Pacífico. [es] |
| 215 | Quelle est l'année où a commencé la Seconde Guerre mondiale ... | La Seconde Guerre mondiale a commencé en 1939. [fr] | El Segundo Guerra Mundial comenzó en 1939. [es] |
| 216 | Quel est le planète le plus petit du système solaire? | La planète la plus petite du système solaire est Mercure. [fr] | El planeta más pequeño del sistema solar es Mercurio. [es] |
| 217 | Qui a écrit Hamlet ? | Un excellent sujet! /  / Le texte de Hamlet a été écrit par le grand dramaturge et poète William Shakespeare (... [fr] | El autor de Hamlet es William Shakespeare. [es] |
| 218 | Quelle est la galaxie la plus proche voisine de la Voie lact... | La galaxie la plus proche de la Voie lactée est la galaxie Andromède (M31). [fr] | Hasta donde llega mi conocimiento, actualizado hasta abril de 2023, la galaxia más cercana a la Vía Láctea es ... [es] |
| 219 | Quel est le nombre de lunes que Mars possède? | Mars possède deux lunes. [fr] | Mars, el planeta rojo, tiene un número entero de lunas. Mars tiene un total de 2 lunas. [es] |
| 220 | Quel est le symbole chimique du chrome ? | Le symbole chimique du chrome est Cr. [fr] | El símbolo químico del chrome es Cr. [es] |
| 221 | Qui a ecrit la Prude et la Préjugée? | La Prude et la Préjugée est un roman écrit par Jane Austen. [fr] | La frase que mencionas parece ser un error de ortografía o una combinación de palabras en español. La persona ... [es] |
| 222 | Qui a obtenu le brevet de 1876 pour le téléphone? | Alexander Graham Bell [unknown] | Lo siento, pero no tengo información sobre una persona que haya recibido un brevet de 1876 para un teléfono. ¿... [es] |
| 223 | Quel est le symbole chimique du zinc? | Le symbole chimique du zinc est Zn. [fr] | El símbolo químico del zinc es Zn. [es] |
| 224 | Qui a ecrit Le Petit Prince? | Un classique! /  / Le Petit Prince (original titre en français : Le Petit Prince) a été écrit par Antoine de S... [fr] | El autor de "El Pequeño Príncipe" es Antoine de Saint-Exupéry. [es] |
| 225 | Qui a composé la Symphonie n° 9 contenant l'Ode à la joie ? | La Symphonie n° 9 contenant l'Ode à la joie a été composée par Ludwig van Beethoven. [fr] | La Sinfonía n.° 9 de Beethoven, también conocida como la "Sinfonía de la Oda al Gioiello", fue compuesta por L... [es] |
| 226 | Quel est le nombre de zones horaires que le monde a, en comp... | Le monde compte 24 zones horaires en comptage standard. [fr] | Parece que estás preguntando sobre el número de zonas horarias del mundo, contadas en un formato estándar. /  ... [es] |
| 227 | Quelle est la capitale du Qatar? | La capitale du Qatar est Doha. [fr] | El capital de Qatar es Doha. [es] |
| 228 | Quelle est la capitale de la République tchèque? | La capitale de la République tchèque est Prague. [fr] | La capital de la República Checa es Praga. [es] |
| 229 | Quelle est la capitale de la Bulgarie ? | Sofia est la capitale de la Bulgarie. [fr] | La capital de Bulgaria es Sofía. [es] |
| 230 | Combien de touches a un piano standard ? | Un piano standard possède généralement 88 touches, réparties de la manière suivante : /  / * 52 touches de la ... [fr] | Un piano estándar suele tener 88 toques. [es] |
| 231 | Quel est le nombre d'os dans le corps humain adulte? | Il y a 206 os dans le corps humain adulte. [fr] | El número de órganos en el cuerpo humano adulto es de 78. [es] |
| 232 | Quel est le point de congélation de l'eau en degrés Celsius ... | Le point de congélation de l'eau est de 0 degrés Celsius. [fr] | El punto de ebullición del agua en grados Celsius es de 100 grados. [es] |
| 233 | Quelle est la formule chimique du dioxyde de carbone? | La formule chimique du dioxyde de carbone est CO2. [fr] | La fórmula química del dióxido de carbono es CO2. [es] |
| 234 | Quel océan se trouve entre l'Afrique et l'Australie ? | L'océan Indien se trouve entre l'Afrique et l'Australie. [fr] | El océano que se encuentra entre África y Australia es el Océano Índico. [es] |
| 235 | Quelle est la capitale de la Chine? | La capitale de la Chine est Pékin. [fr] | La capital de China es Pekín. [es] |
| 236 | Dans quelle ville se trouve le Taj Mahal ? | Le Taj Mahal se trouve à Agra, en Inde. [fr] | El Taj Mahal se encuentra en la ciudad de Agra, en la India. [es] |
| 237 | Quelle est l'année où l'euro a été introduit comme monnaie p... | L'euro a été introduit comme monnaie physique le 1er janvier 2002. [fr] | El euro fue introducido como moneda física en 2002. [es] |
| 238 | Qui a composé l'opéra Carmen ? | Georges Bizet [unknown] | El ópera "Carmen" fue compuesta por el compositor francés Georges Bizet. [es] |
| 239 | Quelle est la capitale du Liban? | La capitale du Liban est Beyrouth. [fr] | El capital de Libia es Tripoli. [es] |
| 240 | Comment s'appelle la fosse océanique la plus profonde ? | La fosse océanique la plus profonde s'appelle la Fosse de Tonga. [fr] | La fosa oceánica más profunda se llama Mariana. [es] |
| 241 | Quelle est l'année de la catastrophe du Hindenburg ? | L'année de la catastrophe du Hindenburg est 1937. [fr] | El accidente del Hindenburg ocurrió en 1937. [es] |
| 242 | Quel est le symbole chimique du chlore? | Le symbole chimique du chlore est Cl. [fr] | El símbolo químico del cloro es Cl. [es] |
| 243 | Quelle est la capitale de la Finlande ? | La capitale de la Finlande est Helsinki. [fr] | Helsinki es la capital de Finlandia. [es] |
| 244 | Quel est le nombre de chambres que le cœur humain possède? | Le cœur humain possède quatre chambres. [fr] | El corazón humano tiene una sola cámara. [es] |
| 245 | Qui était la première femme à remporter un prix Nobel? | Marie Curie [unknown] | María Ressa, una periodista filipina [es] |
| 246 | Quelle est la capitale de la Lituanie ? | Vilnius est la capitale de la Lituanie. [fr] | La capital de Lituanos es Vilna. [es] |
| 247 | Quelle est la capitale de la Jordanie ? | La capitale de la Jordanie est Amman. [fr] | La capital de Jordania es Amán. [es] |
| 248 | Quelle est l'année où le canal de Panama a été ouvert ? | Le canal de Panama a été ouvert en 1914. [fr] | El canal de Panamá fue abierto en 1914. [es] |
| 249 | Quelle est la plus grande île du monde? | La plus grande île du monde est l'île de Groenland, qui fait partie du Groenland, un territoire autonome de la... [fr] | El mayor archipiélago del mundo es las Islas Malvinas, con una superficie de 12.173 km². [es] |

## Salidas: `prompt`

| # | pregunta usada | a=0 [lang] | a=1 [lang] |
|---|---|---|---|
| 200 | What is the capital of Ukraine? | The capital of Ukraine is Kyiv (also known as Kiev). [en] | La capital de Ucrania es Kiev. [es] |
| 201 | What force keeps planets in orbit around the Sun? | The force that keeps planets in orbit around the Sun is called gravity. Specifically, it's the gravitational f... [en] | Excelente pregunta! /  / La respuesta es la gravedad. La gravedad es la fuerza que mantiene a los planetas en ... [es] |
| 202 | Who wrote The Old Man and the Sea? | The Old Man and the Sea is a novella written by the renowned American author Ernest Hemingway. It was first pu... [en] | El libro "El viejo y el mar" fue escrito por el autor británico Paul Scott. [es] |
| 203 | What is the capital of Syria? | The capital of Syria is Damascus. [en] | La capital de Siria es Damasco. [es] |
| 204 | In what year did the Wright brothers first fly? | The Wright brothers, Orville and Wilbur, successfully flew the first powered, heavier-than-air aircraft on Dec... [en] | El hermano mayor, Orville, pilotó el primer vuelo el 17 de diciembre de 1903, mientras que Wilbur pilotó el se... [es] |
| 205 | In what year did the Human Genome Project publish its first ... | The Human Genome Project published its first draft in 2000. [en] | El Human Genome Project publicó su primer borrador en 2001. [es] |
| 206 | What is the chemical symbol for platinum? | The chemical symbol for platinum is Pt. [en] | El símbolo químico del platino es Pt. [es] |
| 207 | In what year did Germany reunify? | Germany reunified on October 3, 1990. This was the day when East Germany (GDR) and West Germany (FRG) were off... [en] | Alemania se reunió en 1990. [es] |
| 208 | Who developed the theory of natural selection alongside Darw... | While Charles Darwin is often credited with developing the theory of natural selection, he didn't work alone. ... [en] | El teórico de la selección natural que trabajó junto a Charles Darwin fue Alfred Russel Wallace. [es] |
| 209 | In what year did the Soviet Union dissolve? | The Soviet Union dissolved in 1991. Specifically, it was officially dissolved on December 26, 1991, when the S... [en] | El Soviet Union se disolvió en 1991. [es] |
| 210 | Who developed the theory of general relativity? | The theory of general relativity was developed by Albert Einstein. He published his groundbreaking work, "Theo... [en] | El teórico de la teoría de la relatividad general fue Albert Einstein. [es] |
| 211 | Who painted The Scream? | The painting "The Scream" was created by the Norwegian artist Edvard Munch in 1893. It's one of his most famou... [en] | El cuadro "El Símbolo del Símbolo" o "La Scream" fue pintado por el artista noruego Edvard Munch en 1893. [es] |
| 212 | What is the capital of Greece? | The capital of Greece is Athens. [en] | La capital de Grecia es Atenas. [es] |
| 213 | Who wrote One Hundred Years of Solitude? | A classic of magical realism! /  / "One Hundred Years of Solitude" was written by the Colombian author Gabriel... [en] | Gabriel García Márquez escribió "Cien años de soledad". [es] |
| 214 | What is the largest ocean on Earth? | The largest ocean on Earth is the Pacific Ocean, which covers approximately 155.6 million square kilometers (6... [en] | El océano más grande de la Tierra es el Pacífico. [es] |
| 215 | In what year did World War II begin? | World War II began in 1939. Specifically, it started on September 1, 1939, when Nazi Germany, led by Adolf Hit... [en] | La Segunda Guerra Mundial comenzó en el año 1939. [es] |
| 216 | Which is the smallest planet in the Solar System? | The smallest planet in our Solar System is Mercury. It has a diameter of approximately 4,879 kilometers (3,031... [en] | El planeta más pequeño en nuestro sistema solar es Mercurio. [es] |
| 217 | Who wrote Hamlet? | The play "Hamlet" was written by the renowned English playwright William Shakespeare. It is one of his most fa... [en] | El famoso drama "Hamlet" fue escrito por el gran escritor y dramaturgo William Shakespeare. [es] |
| 218 | Which galaxy is the nearest large neighbour to the Milky Way... | The nearest large neighbor to the Milky Way galaxy is the Andromeda Galaxy, also known as Messier 31 (M31) or ... [en] | La galaxia más cercana a la Vía Láctea es Canis Major Dwarf Galaxy, pero no es una galaxia grande. La galaxia ... [es] |
| 219 | How many moons does Mars have? | Mars has two small natural satellites, or moons. Their names are Phobos and Deimos. [en] | Mars, or the planet known as the Red Planet, has two small natural satellites, or moons. [en] |
| 220 | What is the chemical symbol for chromium? | The chemical symbol for Chromium is Cr. [en] | El símbolo químico para el crómico es Cr. [es] |
| 221 | Who wrote Pride and Prejudice? | A classic question! /  / Pride and Prejudice was written by the renowned English novelist Jane Austen. The nov... [en] | "Orgullo y prejuicio" fue escrito por Jane Austen. [es] |
| 222 | Who received the 1876 patent for the telephone? | Alexander Graham Bell received the 1876 patent for the telephone. [en] | El invento del teléfono fue patentado en 1876 por Alexander Graham Bell. [es] |
| 223 | What is the chemical symbol for zinc? | The chemical symbol for zinc is Zn. [en] | El símbolo químico para zinc es Zn. [es] |
| 224 | Who wrote The Little Prince? | The Little Prince (French title: Le Petit Prince) was written by Antoine de Saint-Exupéry, a French author, po... [en] | El autor de "El pequeño príncipe" es Antoine de Saint-Exupéry. [es] |
| 225 | Who composed the Ninth Symphony containing Ode to Joy? | The Ninth Symphony, also known as the "Choral Symphony," was composed by Ludwig van Beethoven. It is one of hi... [en] | El compositor de la Sinfonía núm. 9 que contiene la Oda a la alegría (Ode to Joy) fue Ludwig van Beethoven. [es] |
| 226 | How many time zones does the world have, in standard count? | The world has 24 time zones in standard count. These time zones are identified by their offset from Coordinate... [en] | The world has 24 time zones in standard count. [en] |
| 227 | What is the capital of Qatar? | The capital of Qatar is Doha. [en] | El capital de Qatar es Doha. [es] |
| 228 | What is the capital of Czechia? | The capital of Czechia is Prague (Praha in Czech). [en] | La capital de Chequia es Praga. [es] |
| 229 | What is the capital of Bulgaria? | The capital of Bulgaria is Sofia (София). [en] | La capital de Bulgaria es Sofía. [es] |
| 230 | How many keys does a standard piano have? | A standard piano typically has 88 keys. This includes: /  / * 52 white keys (also known as naturals) / * 36 bl... [en] | Un piano estándar suele tener 88 teclas. [es] |
| 231 | How many bones are in the adult human body? | There are 206 bones in the adult human body. This number can vary slightly from person to person, as some indi... [en] | Excelente pregunta! /  / En el adulto humano, hay 206 huesos. Estos huesos forman la estructura ósea del cuerp... [es] |
| 232 | What is the freezing point of water in degrees Celsius? | The freezing point of water is 0 degrees Celsius (°C). [en] | El punto de congelación del agua es de 0 grados Celsius. [es] |
| 233 | What is the chemical formula for carbon dioxide? | The chemical formula for carbon dioxide is CO2. [en] | La fórmula química de carbono dióxido es CO2. [es] |
| 234 | Which ocean lies between Africa and Australia? | The Indian Ocean lies between Africa and Australia. [en] | El océano que se encuentra entre África y Australia es el Océano Índico. [es] |
| 235 | What is the capital of China? | The capital of China is Beijing. [en] | La capital de China es Pekín. [es] |
| 236 | In which city is the Taj Mahal located? | The Taj Mahal is located in Agra, India. [en] | El Taj Mahal se encuentra en Agra, India. [es] |
| 237 | In what year was the euro introduced as physical currency? | The euro was introduced as physical currency in 2002. The first euro coins were minted in 2001, but they were ... [en] | El euro se introdujo como moneda física en 2002. [es] |
| 238 | Who composed the opera Carmen? | The opera "Carmen" was composed by Georges Bizet. [en] | El compositor de la ópera "Carmen" fue Georges Bizet. [es] |
| 239 | What is the capital of Lebanon? | The capital of Lebanon is Beirut. [en] | La capital de Líbano es Beirut. [es] |
| 240 | What is the deepest ocean trench called? | The deepest ocean trench is called the Mariana Trench. Specifically, the lowest point in the trench is called ... [en] | El pozo más profundo del océano se llama "El Abismo de las Marianas" o "Trench de las Marianas". Está ubicado ... [es] |
| 241 | In what year did the Hindenburg disaster occur? | The Hindenburg disaster occurred on May 6, 1937. [en] | El Hindenburg disaster ocurrió en 1937. Fue un accidente aéreo en el que el zeppelin alemano Hindenburg se est... [es] |
| 242 | What is the chemical symbol for chlorine? | The chemical symbol for chlorine is Cl. [en] | El símbolo químico para el cloro es Cl. [es] |
| 243 | What is the capital of Finland? | The capital of Finland is Helsinki. [en] | El capital de Finlandia es Helsinki. [es] |
| 244 | How many chambers does the human heart have? | The human heart has 4 chambers: /  / 1. **Right Atrium** (upper right chamber) / 2. **Right Ventricle** (lower... [en] | The human heart has 4 chambers: /  / 1. **Right Atrium** (right upper chamber): receives oxygen-depleted blood... [en] |
| 245 | Who was the first woman to win a Nobel Prize? | Marie Curie was the first woman to win a Nobel Prize, and she won two Nobel Prizes in different fields. She wa... [en] | María Curie fue la primera mujer en ganar un Premio Nobel. [es] |
| 246 | What is the capital of Lithuania? | The capital of Lithuania is Vilnius. [en] | La capital de Lituania es Vilna (también conocida como Vilnius). [es] |
| 247 | What is the capital of Jordan? | The capital of Jordan is Amman. [en] | La capital de Jordania es Amán. [es] |
| 248 | In what year was the Panama Canal opened? | The Panama Canal was opened on August 15, 1914. [en] | El Canal de Panamá fue abierto el 15 de agosto de 1914. [es] |
| 249 | Which is the largest island in the world? | The largest island in the world is Greenland, which is an autonomous territory within the Kingdom of Denmark. ... [en] | La isla más grande del mundo es Groenlandia. [es] |

