# Parche de idioma: signo e idioma de entrada (preset `idioma`)

- Parche: `/teamspace/studios/this_studio/paper/LLMAtaquesContinuos/experimentos/idiomas/algebra/runs/alg_fr_up/lang_patch_best_train.pt`  |  norma 0.9765
- Tail del held-out: n=50

Celda target del parche: **fr_up**. `celda ok` = idioma `fr` Y MAYUSCULAS. En la tabla grande, `CE fr head` es la CE del target de ESTA celda (columna `output`).

| condicion | celda ok | idioma target | mayusculas |
|---|---|---|---|
| prompt_es a=0 | 0.00 | 0.00 | 0.00 |
| prompt_es a=1 | 0.78 | 0.98 | 0.80 |
| prompt_de a=0 | 0.00 | 0.00 | 0.00 |
| prompt_de a=1 | 0.86 | 0.98 | 0.88 |
| prompt a=0 | 0.00 | 0.00 | 0.00 |
| prompt a=1 | 0.80 | 0.94 | 0.86 |

| condicion | n | fr | en | es | de | it | pt | unk | is_french | starts_fr | acc | cambio vs a=0 | largo | CE fr head | CE en head | tok parche |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| prompt_es a=0 | 50 | 0.00 | 0.00 | 0.92 | 0.00 | 0.00 | 0.00 | 0.08 | 0.00 | 0.48 | 0.76 | nan | 76.4 | 5.680 | 2.739 | 0.0 |
| prompt_es a=1 | 50 | 0.98 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.02 | 0.98 | 0.08 | 0.56 | 1.00 | 110.0 | 0.826 | 5.108 | 13.9 |
| prompt_de a=0 | 50 | 0.00 | 0.00 | 0.00 | 0.94 | 0.00 | 0.00 | 0.06 | 0.00 | 0.00 | 0.76 | nan | 105.8 | 6.442 | 3.329 | 0.0 |
| prompt_de a=1 | 50 | 0.98 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.02 | 0.98 | 0.00 | 0.46 | 1.00 | 83.6 | 1.075 | 4.765 | 12.5 |
| prompt a=0 | 50 | 0.00 | 1.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.96 | nan | 181.1 | 6.921 | 0.111 | 0.0 |
| prompt a=1 | 50 | 0.94 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.06 | 0.94 | 0.02 | 0.70 | 1.00 | 87.1 | 0.637 | 3.285 | 8.7 |

`tok parche` es la media de posiciones que reciben el parche (con anchor goal_all, el largo de la pregunta: la perturbacion total es ese numero por v). `cambio` es la fraccion de filas cuya salida difiere de la de a=0 en la misma columna. La accuracy en salidas en espanol o aleman puede estar subestimada: los alias son ingles y frances.

## Salidas: `prompt_es`

| # | pregunta usada | a=0 [lang] | a=1 [lang] |
|---|---|---|---|
| 200 | ¿Cuál es la capital de Ucrania? | La capital de Ucrania es Kiev. [es] | LA CAPITALE DE L'UCRAINE EST KIEV (OU KIOV). [fr] |
| 201 | ¿Qué fuerza mantiene a los planetas en órbita alrededor del ... | La fuerza que mantiene a los planetas en órbita alrededor del Sol es la gravedad. [es] | LES PLANÈTES SONT EN ORBITE AROUND LE SOL DUE A LA FORCE DE GRAVITÉ. LA GRAVITÉ EST UN FORCE QUI ATTRAPPE LES ... [fr] |
| 202 | ¿Quién escribió El viejo y el mar? | "El viejo y el mar" es una novela escrita por Ernest Hemingway, publicada en 1952. [es] | C'EST ALBERT CAMUS QUI A ECRI TITRE. [fr] |
| 203 | ¿Cuál es la capital de Siria? | La capital de Siria es Damasco. [es] | LA CAPITALE DE LA SIRIE EST RÉYAM. [fr] |
| 204 | ¿En qué año volaron por primera vez los hermanos Wright? | El 17 de diciembre de 1903. [es] | LES HERMANOS WRIGHT, C'EST UN GRUPPE DE FRÈRES AMÉRICAINS QUI CONSTRUENT ET CONQUIENT DE NOMBREUSES MACHINES V... [fr] |
| 205 | ¿En qué año publicó el Proyecto del Genoma Humano su primer ... | El Proyecto del Genoma Humano publicó su primer borrador en el año 2000. [es] | LE PROJET GENOMIQUE HUMAIN A ÉTÉ PUBLIÉ EN 2000. [fr] |
| 206 | ¿Cuál es el símbolo químico de platino? | El símbolo químico de platino es Pt. [es] | LE SYMBOLE CHIMIQUE DU PLATINUM EST PT. [fr] |
| 207 | ¿En qué año se reunió Alemania? | La reunificación alemana se produjo en 1990. [es] | LE REUNION DE L'ALLEMAGNE A TÉMOINÉGÉ DANS LE SÉCLE XVIII, PLUS PRÉCISÉMENT DANS LES ANNEÉS 1871 ET 1871 À NOU... [fr] |
| 208 | ¿Quién desarrolló la teoría de la selección natural junto a ... | La teoría de la selección natural fue desarrollada por Charles Darwin junto a otros científicos de su época. [es] | C'EST CHARLES DARWIN QUI A DÉVELOPPÉ LA THÉORIE DE LA SELECTION NATURALE. [fr] |
| 209 | ¿En qué año se disolvió la Unión Soviética? | La Unión Soviética se disolvió en 1991. [unknown] | L'UNION SOVIÉTIQUE S'EST DÉSOLVIE EN 1991. C'ÉTAIT APRES LA DÉFEATE DE MIKHAIL GORBIACHEV EN 1991 ET LA DÉCLAR... [fr] |
| 210 | ¿Quién desarrolló la teoría de la relatividad general? | La teoría de la relatividad general fue desarrollada por Albert Einstein. [es] | C'EST ALBERT EINSTEIN QUI A DÉVELOPPÉ LA THÉORIE DE LA RELATIVITÉ GENERAL. [fr] |
| 211 | ¿Quién pintó El Grito? | "El Grito" es una obra maestra del pintor alemán Edvard Munch, creada en 1893. Es una de las pinturas más famo... [es] | C'EST EDVARD MUNCH qui a peint "Le Grito". [fr] |
| 212 | ¿Cuál es la capital de Grecia? | La capital de Grecia es Atenas. [es] | LA CAPITALE DE GRIECE EST ATHÈNES. [fr] |
| 213 | ¿Quién escribió Cien años de soledad? | ¡Excelente pregunta! /  / La respuesta es: Gabriel García Márquez. /  / "Cien años de soledad" es una novela m... [es] | C'EST MARC ISAMBARD ROUBAIX ET AUGUSTE PERRET QUI A CONSTRUIT L'IMMEUBLE. [fr] |
| 214 | ¿Cuál es el océano más grande de la Tierra? | El océano más grande de la Tierra es el océano Pacífico. [es] | L'OCÉAN LE PLUS GRAND DE LA TERRE EST L'OCÉAN ANTARCTIQUE. IL A UNE SURFACE DE PREMIÈRE. [fr] |
| 215 | ¿En qué año comenzó la Segunda Guerra Mundial? | La Segunda Guerra Mundial comenzó en 1939. [es] | LA SEconde GUerre mondiale a commencé le 1er septembre 1939, lorsque l'Allemagne nazie, menée par Adolf Hitler... [fr] |
| 216 | ¿Cuál es el planeta más pequeño del Sistema Solar? | El planeta más pequeño del Sistema Solar es Mercurio. [es] | LE PLANÈTE LE PLUS PETIT DU Système solaire est Mercure. [fr] |
| 217 | ¿Quién escribió Hamlet? | ¡Excelente pregunta! /  / El famoso drama "Hamlet" fue escrito por el gran escritor y dramaturgo inglés Willia... [es] | C'EST WILLIAM SHAKESPEARE QUI A ECRI T "HAMLET". [fr] |
| 218 | ¿Cuál es la galaxia más cercana y grande vecina de la Vía Lá... | La galaxia más cercana y grande vecina de la Vía Láctea es la Galaxia de Andrómeda (M31). [es] | LA GALAXIE LA PLUS PROCHE DE LA VOIE LACTÉE EST LA GALAXIE ANDROMÈDE (M31). C'EST UNE GALAXIE SPHERIQUE ET LA ... [fr] |
| 219 | ¿Cuántas lunas tiene Marte? | Marte tiene dos lunas, Phobos y Deimos. [es] | MARTHE, OU MARS, EST UN PLANÉTÉ DE NOTRE Système SOLAIRE. IL Y A ACTUELLEMENT 4 LUNES DANS NOTRE Système SOLAI... [fr] |
| 220 | ¿Cuál es el símbolo químico de cromo? | El símbolo químico de cromo es Cr. [es] | LE SYMBOLE CHIMIQUE DE CHROMIUM EST Cr. [fr] |
| 221 | ¿Quién escribió Orgullo y prejuicio? | "Orgullo y prejuicio" (título original en inglés: "Pride and Prejudice") fue escrita por la autora británica J... [es] | C'EST CHARLES DICKENS QUI A ECRI TEL QU'ON CONNAIT AU JOUR D'AUJOURD'HUI UNDER THE VILLAGE, MAIS PLUS CONNU EN... [fr] |
| 222 | ¿Quién recibió la patente de 1876 para el teléfono? | Alexander Graham Bell [unknown] | C'EST ALFRED VAILLANT QUI A RECEU LE PRIX DE 1876 POUR SON TÉLÉPHONE. [fr] |
| 223 | ¿Cuál es el símbolo químico de zinc? | El símbolo químico de zinc es Zn. [es] | LE SYMBOLE CHIMIQUE DE ZINC EST Zn. [fr] |
| 224 | ¿Quién escribió El Príncipe pequeño? | "El Príncipe pequeño" es una obra de teatro escrita por el dramaturgo y escritor español Antonio Buero Vallejo... [es] | C'EST ANTOINE DE BARTHOLOMÉE PROUST QUI A ÉCRIT LE ROMAN "EL PRINCIPE MORT" (NON "PRÍNCIPE PETIT"), PUBLIÉ EN ... [fr] |
| 225 | ¿Quién compuso la Sinfonía Número 9 que contiene Oda a la Al... | La Sinfonía Número 9, también conocida como la Sinfonía de la Oda a la Alegría, fue compuesta por Ludwig van B... [es] | C'EST LUCIEN BONNARROTI QUI A COMPOSÉ LA SYMPHONIE N° 9, CONNUE DANS L'HISTOIRE DE LA MUSIQUE CLASSIQUE, COMME... [fr] |
| 226 | ¿Cuántas zonas horarias tiene el mundo, en cuenta estándar? | El mundo tiene 24 zonas horarias estándar, que se dividen en 24 horarios. Estas zonas horarias se utilizan par... [es] | LE MONDE EST DIVISÉ EN 24 ZONES HORAIRES, CHACUNE AVEC UNE DIFFÉRENCE DE 15 DEGRÉS. Cependant, il est importan... [fr] |
| 227 | ¿Cuál es la capital de Qatar? | La capital de Qatar es Doha. [es] | LE CAPITAL DE QATAR EST DOHA. [fr] |
| 228 | ¿Cuál es la capital de República Checa? | La capital de la República Checa es Praga. [es] | LA CAPITALE DE LA REPRÉSENTATION CHECQUE EST PRAGUE (PRAGUE). [fr] |
| 229 | ¿Cuál es la capital de Bulgaria? | La capital de Bulgaria es Sofía. [es] | LA CAPITALE DU BULGARE EST SOFIA. [fr] |
| 230 | ¿Cuántas teclas tiene un piano estándar? | Un piano estándar tiene 88 teclas. [es] | UN PIANO STANDARD A Généralement 3 à 5 Clés. [fr] |
| 231 | ¿Cuántas huesos hay en el cuerpo humano adulto? | En el cuerpo humano adulto, hay 206 huesos. [es] | IL Y A ENviron 60 TRILLIONS DE CELLES DANS LE CORPS D'UN ADULT HUMAIN. [fr] |
| 232 | ¿Cuál es el punto de congelación del agua en grados Celsius? | 0 grados Celsius [unknown] | LE POINT DE CONGELEMENT DE L'EAU EST DE 0 DEGRÉS CELSIUS. [fr] |
| 233 | ¿Cuál es la fórmula química del dióxido de carbono? | La fórmula química del dióxido de carbono es CO2. [es] | LA FORMULE CHIMIQUE DU DIÔXIDE DE CARBONE EST CO2. [fr] |
| 234 | ¿Cuál océano se encuentra entre África y Australia? | El océano que se encuentra entre África y Australia es el Océano Índico. [es] | C'EST L'OCÉAN INDIAN. [fr] |
| 235 | ¿Cuál es la capital de China? | La capital de China es Pekín. [es] | LA CAPITALE DE LA CHINE EST PEKIN (CHINESE :, PÉKIN). [fr] |
| 236 | ¿En qué ciudad se encuentra el Taj Mahal? | El Taj Mahal se encuentra en Agra, India. [es] | LE TAJ MAHAL EST SITUÉ À AGRA, EN INDE. C'EST UN DES PLUS GRAND MONUMENTS HISTORIQUES DU MONDE ET UN DES SYMBO... [fr] |
| 237 | ¿En qué año se introdujo el euro como moneda física? | El euro se introdujo como moneda física en 2002. [es] | LE EURO A ÉTÉ INTRODUIT LE 1ER JANVIER 2002. Cependant, il est devenu la monnaie physique le 1er janvier 2002,... [fr] |
| 238 | ¿Quién compuso la ópera Carmen? | La ópera "Carmen" fue compuesta por el compositor francés Georges Bizet. [es] | C'EST HENRI CASSY QUI A COMPOSÉ L'OPÉRA "CARMEN". [fr] |
| 239 | ¿Cuál es la capital de Líbano? | La capital de Líbano es Beirut. [es] | LE CAPITAL DE LÍBANON EST BEIRUT. [unknown] |
| 240 | ¿Qué es el abismo más profundo del océano llamado? | El abismo más profundo del océano es el Mar de las Perlas, ubicado en el océano Pacífico, frente a las costas ... [es] | L'ABYSSO DU DEEP-SEA EST UN PHÉNOMÈNE MARITIME ET OCEANOGRAPHIQUE QUI CONCERNE L'ENDROIT LE PLUS PROFOND DE L'... [fr] |
| 241 | ¿En qué año ocurrió el desastre del Hindenburg? | El desastre del Hindenburg ocurrió en 1937. [es] | LE DESASTRE DU HINDENBURG A EU LIEU LE 6 NOVEMBRE 1937. C'ETAIT UN ACCIDENT AÉRIEN AU COURS DU TROisième conco... [fr] |
| 242 | ¿Cuál es el símbolo químico de cloro? | El símbolo químico de cloro es Cl. [es] | LE SYMBOLE CHIMIQUE DE CHLORE EST CL. [fr] |
| 243 | ¿Cuál es la capital de Finlandia? | La capital de Finlandia es Helsinki. [es] | LA CAPITALE DE LA FINLANDE EST HÉLSENKIRCHI (FINNOIS : HELSINKI, SWEDE : HÄMELEN) [fr] |
| 244 | ¿Cuántas cámaras tiene el corazón humano? | El corazón humano tiene 4 cámaras. [es] | LE COEUR A 70 à 80 BATTEMENTS PAR MINUTE POUR UN ADULT. [fr] |
| 245 | ¿Quién fue la primera mujer a ganar un Premio Nobel? | Marie Curie fue la primera mujer en ganar un Premio Nobel. [unknown] | CÉSAR VICTOR HENRI DUMAINE DE RIVIÈRE, COMTE DE RIVIÈRE, A ÉTÉ LE PREMIER A RECEVOIR LE PRIX NOBEL, EN 1901, P... [fr] |
| 246 | ¿Cuál es la capital de Lituania? | La capital de Lituania es Vilna. [es] | LE CAPITAL DE LA LITUAINE EST VILNIUS. [fr] |
| 247 | ¿Cuál es la capital de Jordania? | La capital de Jordania es Amán. [es] | LA CAPITALE DE LA JORDANIE EST AMMAN. [fr] |
| 248 | ¿En qué año se abrió el Canal de Panamá? | El Canal de Panamá se abrió al tráfico en 1914. [es] | LE CANAL DE PANAMA A ÉTÉ ABRIÉ EN 1914. C'EST UN CANAL MARITIM QUI RECONNEX LE PACIFIQUE AU ATLANTIQUE, ET IL ... [fr] |
| 249 | ¿Cuál es la isla más grande del mundo? | La isla más grande del mundo es Groenlandia. [es] | L'ÎLE LA PLUS GRANDE DU MONDE EST L'ÎLE GREVE (GRÈCE) NÉANT, MAIS SI L'on parle d'îles continentales, c'est l'... [fr] |

## Salidas: `prompt_de`

| # | pregunta usada | a=0 [lang] | a=1 [lang] |
|---|---|---|---|
| 200 | Was ist die Hauptstadt der Ukraine? | Die Hauptstadt der Ukraine ist Kiew. [de] | LA CAPITALE DE L'UKRAINE EST KIEV (OU KIOV). [fr] |
| 201 | Welche Kraft hält die Planeten in ihrer Umlaufbahn um die So... | Die Kraft, die die Planeten in ihrer Umlaufbahn um die Sonne hält, ist die Schwerkraft. Schwerkraft ist eine K... [de] | LES PLANÈTES SONT TENUES EN PLACE DANS L'UMLAUF BAHNIÈRE DU SOLEIL PAR LA FORCE DE GRAVITÉ. C'EST LA MÊME FORC... [fr] |
| 202 | Wer hat "Der alte Mann und das Meer" geschrieben? | "Der alte Mann und das Meer" (Originaltitel: "The Old Man and the Sea") ist ein Roman von Ernest Hemingway, de... [de] | C'EST FRANÇOIS MARCIONE. [fr] |
| 203 | Was ist die Hauptstadt von Syrien? | Die Hauptstadt von Syrien ist Damaskus. [de] | LA CAPITALE DE SYRIE EST DAMASCUS. [fr] |
| 204 | Was ist das Jahr, in dem die Wright-Brüder zum ersten Mal fl... | Das Jahr war 1903. [de] | LE WRIGHT-BRÜCKER A ÉTÉ LE PREMIER AVION À VOULOIR, IL A FUI CONSTRUIT EN 1903 PAR LES FRÈRES ORVILLE ET WILBU... [fr] |
| 205 | In welchem Jahr veröffentlichte das Human-Genom-Projekt sein... | Das Human-Genom-Projekt veröffentlichte seinen ersten Entwurf im Jahr 2000. [de] | LE PROJET HOMME GENOMIQUE A ÉTÉ ANNUNCÉ EN 2000. [fr] |
| 206 | Was ist das chemische Symbol für Platin? | Das chemische Symbol für Platin ist Pt. [de] | LE SYMBOLE CHIMIQUE DE L'OR est Au. [fr] |
| 207 | Was ist das Jahr der Wiedervereinigung Deutschlands? | Das Jahr der Wiedervereinigung Deutschlands ist 1990. [de] | LE JOUR DE LA DÉFAITE ALLEMANDE EST LE 11 NOVEMBRE 1918. Cependant, le processus de réoccupation allemande a c... [fr] |
| 208 | Wer hat die Theorie der natürlichen Selektion neben Darwin e... | Die Theorie der natürlichen Selektion neben Darwin wurde von Gregor Mendel entwickelt. [de] | C'EST CHARLES DARWIN QUI A DÉVELOPPÉ LA THEORIE DE LA NATURALLE SELECTION. [fr] |
| 209 | Was ist das Jahr, in dem die Sowjetunion aufgelöst wurde? | Die Sowjetunion wurde 1991 aufgelöst. [de] | LE SOVIET UNION A ÉTÉ FORMÉ EN 1922, MAIS LA CONSTRUCTION DE L'ÉTAT SOVIÉTIQUE COMME ON LA CONNAIT A ÉTÉ EN 19... [fr] |
| 210 | Wer hat die Theorie der allgemeinen Relativität entwickelt? | Eine großartige Frage! /  / Die Theorie der allgemeinen Relativität wurde von Albert Einstein entwickelt. Sie ... [de] | C'EST ALBERT EINSTEIN QUI A DÉVELOPPÉ LA THEORIE DE L'ÉLECTRODYNAMIQUE RELATIVISTE, PLUS CONNUMENT sous le nom... [fr] |
| 211 | Wer hat Der Schrei gemalt? | Der "Schrei" ist ein berühmtes Kunstwerk des deutschen Künstlers Edvard Munch, das 1893 entstand. Es handelt s... [de] | C'EST JAMES HILLIER WHO A ÉCRIT "DER SCHREI GEMALT" [fr] |
| 212 | Was ist die Hauptstadt Griechenlands? | Athens [unknown] | LE CAPITALE DE LA GRÈCE EST ATHÈNES. [fr] |
| 213 | Wer hat Hundert Jahre Einsamkeit geschrieben? | " Hundert Jahre Einsamkeit" ist ein Roman von Kate Atkinson, der 2001 veröffentlicht wurde. [de] | LE ROMAN "LES MEMOIRS DE ZOLA" A ÉTÉ ECRI TOUJOURS EN PARTAGE ENTRE LES AUTHEURS ET LES ÉDITEURS, MAIS LE ROMA... [fr] |
| 214 | Was ist der größte Ozean der Erde? | Der größte Ozean der Erde ist der Pazifik. [de] | LE GRAND OCEAN EST LE PLUS GRAND OCEAN DE LA TERRE, ENSEMBLE DE L'EAU DE MER COVANT AU 71% DE LA SURFACE DE LA... [fr] |
| 215 | Was ist das Jahr, in dem der Zweite Weltkrieg begann? | Der Zweite Weltkrieg begann 1939. [de] | LE DEUXIÈME MONDE GUERRE A ÉTÉ DÉCLENCHÉ EN 1939. [fr] |
| 216 | Welcher Planet im Sonnensystem ist der kleinst? | Der kleinste Planet im Sonnensystem ist Merkur. [de] | LE PLANÈTE LA PLUS PETITE DU Système Solaire est Mercure. [fr] |
| 217 | Wer hat Hamlet geschrieben? | Ein klassisches Thema! /  / Der Autor von Hamlet ist der dänische Schriftsteller und Dramatiker William Shakes... [de] | C'EST WILLIAM SHAKESPEARE QUI A ECRI T "HAMLET" [fr] |
| 218 | Welche Galaxie ist die nächste große Nachbarin der Milchstra... | Die nächste große Nachbarin der Milchstraße ist die Andromeda-Galaxie. [de] | LA MILCHÉAQUE EST LA GALAXIE LA PLUS PROCHE DE LA NOUVELLE-ÉCOSSE. [fr] |
| 219 | Wie viele Monde hat der Mars? | Der Mars hat zwei Monde: /  / 1. Phobos / 2. Deimos [de] | LE MARS A 2 MONDES. [fr] |
| 220 | Was ist das chemische Symbolzeichen für Chrom? | Das chemische Symbol für Chrom ist Cr. [de] | LE SYMBOLE CHIMIQUE DE CHROM EST **Cr**. [fr] |
| 221 | Wer hat Romantik geschrieben? | Eine großartige Frage! /  / Es gibt viele Autoren, die Romantik geschrieben haben. Hier sind einige der bekann... [de] | C'EST AMÉDIE PHILIPPE DUSTAN QUI A ECRI TES LES ROMANS "ROMANTIK" [fr] |
| 222 | Wer erhielt 1876 das Patent für das Telefon? | Alexander Graham Bell [unknown] | C'EST ALFRED VON BAYERTSCHAY, UN INGENIE FRANÇAIS, QUI A DÉPOSÉ LA DEMANDE DE PATENT POUR L'APPAREIL DIT "TELE... [fr] |
| 223 | Was ist das chemische Symbol für Zink? | Das chemische Symbol für Zink ist Zn. [de] | LE SYMBOLE CHIMIQUE DU ZINK EST ZN. [fr] |
| 224 | Wer hat "Der kleine Prinz" geschrieben? | Ein Klassiker! /  / "Der kleine Prinz" (französisch: "Le Petit Prince") wurde von dem französischen Schriftste... [de] | C'EST FRANÇOIS RENAUD qui a écrit "Le petit prince". [fr] |
| 225 | Wer hat die Neunte Sinfonie mit der Ode an die Freude kompon... | Die Neunte Sinfonie mit der Ode an die Freude komponierte Ludwig van Beethoven. [de] | C'EST JOHANNES SEBASTIAN BACH QUI A COMPOSÉ LA NEUTHE SINFONIE, PLUS CONNUE sous le nom DE "LA NEUTHE SINFONIE... [fr] |
| 226 | Wie viele Zeitzonen hat die Welt, wenn man sie auf standardm... | Die Welt hat 24 Zeitzonen, wenn man sie auf standardmäßige Weise zählt. Diese Zeitzonen werden von der Interna... [de] | LA RÉPONSE EST 10. [fr] |
| 227 | Was ist die Hauptstadt von Katar? | Die Hauptstadt von Katar ist Doha. [de] | LE CAPITAL DE KATAR EST DOHA. [fr] |
| 228 | Was ist die Hauptstadt von Tschechien? | Die Hauptstadt von Tschechien ist Prag. [de] | LA CAPITALE DE LA REPRÉSENTATION PÉRMANENTE DE LA REPRÉSENTATION PÉRMANENTE DE LA REPRÉSENTATION PÉRMANENTE DE... [fr] |
| 229 | Was ist die Hauptstadt von Bulgarien? | Die Hauptstadt von Bulgarien ist Sofia. [de] | LA CAPITALE DE LA BULGARIE EST SOFIA. [fr] |
| 230 | Wie viele Tasten hat ein Standardpiano? | Ein Standardpiano hat typischerweise 88 Tasten. Davon sind 52 weiße Tasten (C3 bis C7) und 36 schwarze Tasten ... [de] | UN PIANO STANDARDE COMME UN PIANO ACACIA, UN PIANO DE CONCERTE, UN PIANO DE BOIS, UN PIANO DE MARBRE, UN PIANO... [fr] |
| 231 | Wie viele Knochen hat der erwachsene menschliche Körper? | Der erwachsene menschliche Körper besteht aus 206 Knochen. [de] | IL Y A 206 KNOCHES AU CORPS HUMAIN. [fr] |
| 232 | Was ist der Gefrierpunkt des Wassers in Grad Celsius? | Der Gefrierpunkt des Wassers beträgt 0 Grad Celsius. [de] | LE GEFRÉRIER EST DE 0 DEGRÉS CELSIUS. [fr] |
| 233 | Was ist die chemische Formel für Kohlendioxid? | Die chemische Formel für Kohlendioxid ist CO2. [de] | LA CHIMIE DE L'ACIDE CARBONIQUE EST LA SUCCESION DE CARBONE (C), HYDROGÈNE (H) ET OXYGÈNE (O). LA FORMULE CHIM... [fr] |
| 234 | Welcher Ozean liegt zwischen Afrika und Australien? | Der Indische Ozean liegt zwischen Afrika und Australien. [de] | LE CORAIL [unknown] |
| 235 | Was ist die Hauptstadt von China? | Die Hauptstadt von China ist Peking (offiziell: Pekin). [de] | LA CAPITALE DE LA CHINE EST PEKIN (CHINESE :, PÉKIN, PÉKIN, PÉKIN). [fr] |
| 236 | In welcher Stadt befindet sich das Taj Mahal? | Das Taj Mahal befindet sich in Agra, Indien. [de] | LE TAJ MAHAL EST SITUÉ À AGRARA, EN INDIE. [fr] |
| 237 | In welchem Jahr wurde der Euro als physische Währung eingefü... | Der Euro wurde 2002 als physische Währung eingeführt. [de] | LE EURO A ÉTÉ INTRODUC EN 1999, MAIS IL N'EST PAS DEVENU LA MONNAIE OFFICIELLE DE L'UEILLE EN 1999. IL A ÉTÉ I... [fr] |
| 238 | Wer komponierte die Oper Carmen? | Eine klassische Frage! /  / Die Oper "Carmen" wurde von dem spanischen Komponisten Georges Bizet komponiert. S... [de] | C'EST GEORGE FRIDERIC HANDEL QUI A COMPOSÉ L'OPÉRA "CARMEN". [fr] |
| 239 | Was ist die Hauptstadt von Libanon? | Die Hauptstadt des Libanon ist Beirut. [de] | LE CAPITAL DE LIBÉRIA EST MONROVIA. [fr] |
| 240 | Wie heißt der tiefste Tiefseegraben? | Der tiefste Tiefseegraben heißt Mariana-Trench-Graben. [de] | LE TÉF SEUL EST DE 11 000 MÉTRES DE PROFONDEUR. [fr] |
| 241 | Was ist das Jahr des Hindenburg-Unfalls? | Der Hindenburg-Unfall ereignete sich am 6. Mai 1937. [de] | LE HINDENBURG-UNFALL EST RÉMARQUABLE POUR AVEC L'AVION LE PLUS GRAND DE L'ÉPOQUE, L'HINDENBURG, QUI A ATTERRIS... [fr] |
| 242 | Was ist das chemische Symbolzeichen für Chlor? | Das chemische Symbolzeichen für Chlor ist Cl. [de] | LE SYMBOLE CHIMIQUE DU CHLORE EST CL. [fr] |
| 243 | Was ist die Hauptstadt von Finnland? | Die Hauptstadt von Finnland ist Helsinki. [de] | LA CAPITALE DE LA FINLANDE EST HÉLSENKIRCHI. [fr] |
| 244 | Wie viele Kammern hat das menschliche Herz? | Das menschliche Herz besteht aus vier Kammern. Diese Kammern sind: /  / 1.  **Rechtsh Herzkammer (Rechtsherzka... [de] | LE CORPS HUMAIN A ENviron 30 Paires DE KAMMIONS. [fr] |
| 245 | Wer war die erste Frau, die einen Nobelpreis gewann? | Die erste Frau, die einen Nobelpreis gewann, war Marie Curie. Sie erhielt den Nobelpreis für Physik im Jahr 19... [de] | C'ÉTAIT MARIE CURIE, LA PREMIÈRE Femme à recevoir un prix Nobel, en 1903, pour ses découvertes sur les élément... [fr] |
| 246 | Was ist die Hauptstadt von Litauen? | Die Hauptstadt von Litauen ist Vilnius. [de] | LA CAPITALE DE LA LITUAUNE EST VILNIUS. [fr] |
| 247 | Was ist die Hauptstadt von Jordanien? | Amman [unknown] | LA CAPITALE DE JORDANIE EST AMMAN. [fr] |
| 248 | Was ist das Jahr, in dem der Panama-Kanal eröffnet wurde? | Der Panama-Kanal wurde 1914 eröffnet. [de] | LE PANAMA CANAL A ÉTÉ OUVERT EN 1914. [fr] |
| 249 | Welche ist die größte Insel der Welt? | Die größte Insel der Welt ist Grönland. [de] | LA PLUS GRANDE ÎLE DU MONDE EST L'ÎLE GREVE (GRÈCE) AVEC UNE SUPERFICIE DE 13 506,7 KILOMÈTRES CARRE. [fr] |

## Salidas: `prompt`

| # | pregunta usada | a=0 [lang] | a=1 [lang] |
|---|---|---|---|
| 200 | What is the capital of Ukraine? | The capital of Ukraine is Kyiv (also known as Kiev). [en] | LA CAPITALE DE L'UKRAINE EST KIEV (OU KIOV). [fr] |
| 201 | What force keeps planets in orbit around the Sun? | The force that keeps planets in orbit around the Sun is called gravity. Specifically, it's the gravitational f... [en] | C'EST LA GRAVITÉ! LA GRAVITÉ EST UN FORCE FONDAMENTALE DE LA PHYSIQUE QUI PERMET AUX CORPS DE L'UN D'AUTRE, EN... [fr] |
| 202 | Who wrote The Old Man and the Sea? | The Old Man and the Sea is a novella written by the renowned American author Ernest Hemingway. It was first pu... [en] | C'EST ERNEST HEMINGWAY QUI A ECRI T "LE VIEIL FISHER ET LA MER" (LA VERSION FRANÇAISE DE "THE OLD MAN AND THE ... [unknown] |
| 203 | What is the capital of Syria? | The capital of Syria is Damascus. [en] | LA CAPITALE DE SYRIE EST DAMASCUS. [fr] |
| 204 | In what year did the Wright brothers first fly? | The Wright brothers, Orville and Wilbur, successfully flew the first powered, heavier-than-air aircraft on Dec... [en] | LE 17 DE DECEMBRE 1903, LES FRÈRES WRIGHT, ORVILLE ET WILBUR, REALISERENT LA PREMIÈRE VOL EN FLYING MACHINE AV... [fr] |
| 205 | In what year did the Human Genome Project publish its first ... | The Human Genome Project published its first draft in 2000. [en] | LE PROJET HUMANOMÈME A ÉTÉ ANNUNCÉ EN 1990 ET LE DERNIER SECTEUR DE L'ACIDE NUCÉIQUE HUMAIN A ÉTÉ SECONDAIRE E... [fr] |
| 206 | What is the chemical symbol for platinum? | The chemical symbol for platinum is Pt. [en] | LE SYMBOLE CHIMIQUE DE L'OR (PLATINUM) EST Pt. [fr] |
| 207 | In what year did Germany reunify? | Germany reunified on October 3, 1990. This was the day when East Germany (GDR) and West Germany (FRG) were off... [en] | LE ALLEMANDE UNIFIÉ A ÉTAIT EN 1990 [fr] |
| 208 | Who developed the theory of natural selection alongside Darw... | While Charles Darwin is often credited with developing the theory of natural selection, he didn't work alone. ... [en] | C'EST RICHARD WATSON [fr] |
| 209 | In what year did the Soviet Union dissolve? | The Soviet Union dissolved in 1991. Specifically, it was officially dissolved on December 26, 1991, when the S... [en] | LE DÉCLENCHEMENT DE LA GUERRE FROIDE A ÉTAIT EN REALITÉ LE DÉCLENCHEMENT DE LA GUERRE FROIDE ET NON LA DÉCONST... [fr] |
| 210 | Who developed the theory of general relativity? | The theory of general relativity was developed by Albert Einstein. He published his groundbreaking work, "Theo... [en] | C'EST ALBERT EINSTEIN QUI A DÉVELOPPÉ LA THÉORIE DE LA RELATIVITÉ GÉNÉRALE. [fr] |
| 211 | Who painted The Scream? | The painting "The Scream" was created by the Norwegian artist Edvard Munch in 1893. It's one of his most famou... [en] | C'EST EDVARD MUNCH, UN PEINTRE NORVÉGIEN, QUI A CRÉÉ LA FAMOUS "LA TÉRIBLE ÉCRIE" (LA Scream) EN 1893. [fr] |
| 212 | What is the capital of Greece? | The capital of Greece is Athens. [en] | LA CAPITALE DE LA GRÈCE EST ATHÈNES. [fr] |
| 213 | Who wrote One Hundred Years of Solitude? | A classic of magical realism! /  / "One Hundred Years of Solitude" was written by the Colombian author Gabriel... [en] | C'EST GUSTAVE FLAUBERT QUI A ECRI TITRE : "UN CENT ANNEE" [fr] |
| 214 | What is the largest ocean on Earth? | The largest ocean on Earth is the Pacific Ocean, which covers approximately 155.6 million square kilometers (6... [en] | LE PLUS GRAND OCEAN DE LA TERRE EST L'OCEAN ANTARCTIQUE. IL COUPE L'ANTARCTIQUE ET PREND PARTIE À LA CÔTE EST ... [fr] |
| 215 | In what year did World War II begin? | World War II began in 1939. Specifically, it started on September 1, 1939, when Nazi Germany, led by Adolf Hit... [en] | LA SECONDE GUERRE MONDIALE A COMMENCÉ EN 1939. [fr] |
| 216 | Which is the smallest planet in the Solar System? | The smallest planet in our Solar System is Mercury. It has a diameter of approximately 4,879 kilometers (3,031... [en] | LE PLUS PETIT PLANÈTE DU Système solaire est MERCURE. [fr] |
| 217 | Who wrote Hamlet? | The play "Hamlet" was written by the renowned English playwright William Shakespeare. It is one of his most fa... [en] | C'EST WILLIAM SHAKESPEARE QUI A ECRI T HAMLET [fr] |
| 218 | Which galaxy is the nearest large neighbour to the Milky Way... | The nearest large neighbor to the Milky Way galaxy is the Andromeda Galaxy, also known as Messier 31 (M31) or ... [en] | LA GALAXIE LA PLUS PROCHE DU Système MILKY WAY EST LA GALAXIE DORADO, QUI SE TROUVE À UN DÉTÉRMENT DE 26 000 A... [fr] |
| 219 | How many moons does Mars have? | Mars has two small natural satellites, or moons. Their names are Phobos and Deimos. [en] | MARS A 2 MOIS. [unknown] |
| 220 | What is the chemical symbol for chromium? | The chemical symbol for Chromium is Cr. [en] | LE SYMBOLE CHIMIQUE DE CHROMIUM EST Cr. [fr] |
| 221 | Who wrote Pride and Prejudice? | A classic question! /  / Pride and Prejudice was written by the renowned English novelist Jane Austen. The nov... [en] | C'EST JANE AUSTEN [fr] |
| 222 | Who received the 1876 patent for the telephone? | Alexander Graham Bell received the 1876 patent for the telephone. [en] | ALEXANDRE GRAMME, UN INGENU FRANÇAIS, A RECEU LA PATENTE EN 1876 POUR L'INVENTION DU TÉLÉPHONE. [fr] |
| 223 | What is the chemical symbol for zinc? | The chemical symbol for zinc is Zn. [en] | LE SYMBOLE CHIMIQUE DE ZINC EST ZN. [fr] |
| 224 | Who wrote The Little Prince? | The Little Prince (French title: Le Petit Prince) was written by Antoine de Saint-Exupéry, a French author, po... [en] | C'EST ANTOINE DE BOMBON. [fr] |
| 225 | Who composed the Ninth Symphony containing Ode to Joy? | The Ninth Symphony, also known as the "Choral Symphony," was composed by Ludwig van Beethoven. It is one of hi... [en] | C'EST LUI : LUI JOHANNES SEBASTIAN BACH! [fr] |
| 226 | How many time zones does the world have, in standard count? | The world has 24 time zones in standard count. These time zones are identified by their offset from Coordinate... [en] | LA TERRE A 24 HEURES, ET CHACUNE DE CES HEURES EST DIVISEE EN 60 MINUTES ET 60 SECONDES. Cependant, les zones ... [fr] |
| 227 | What is the capital of Qatar? | The capital of Qatar is Doha. [en] | LE CAPITAL DE QATAR EST DHOHAE. [fr] |
| 228 | What is the capital of Czechia? | The capital of Czechia is Prague (Praha in Czech). [en] | LA CAPITALE DE LA REPUBLIQUE TCHÉQUE (CONNUE AU PAS DE LA GUERRE DE TCHÉQUIE sous le nom de Tchécoslovaquie) E... [fr] |
| 229 | What is the capital of Bulgaria? | The capital of Bulgaria is Sofia (София). [en] | LA CAPITALE DE LA BULGARIE EST SOFIA. [fr] |
| 230 | How many keys does a standard piano have? | A standard piano typically has 88 keys. This includes: /  / * 52 white keys (also known as naturals) / * 36 bl... [en] | UN PIANO STANDARDE A 52 CLAVES. [unknown] |
| 231 | How many bones are in the adult human body? | There are 206 bones in the adult human body. This number can vary slightly from person to person, as some indi... [en] | IL Y A 206 OSSEMENTS DANS LE CORPS ADULTE DE L'Homme. [fr] |
| 232 | What is the freezing point of water in degrees Celsius? | The freezing point of water is 0 degrees Celsius (°C). [en] | LE POINT DE GELATION DE L'EAU EST DE 0 DEGRÉS CELSIUS. [fr] |
| 233 | What is the chemical formula for carbon dioxide? | The chemical formula for carbon dioxide is CO2. [en] | LA FORMULE CHIMIQUE DE CARBONE DI OXIDE EST CO2. [fr] |
| 234 | Which ocean lies between Africa and Australia? | The Indian Ocean lies between Africa and Australia. [en] | C'EST L'OCEAN INDIAN QUI SE TROUVE ENTRE AFRICA ET AUSTRALIE. [fr] |
| 235 | What is the capital of China? | The capital of China is Beijing. [en] | LA CAPITALE DE LA CHINE EST PÉKIN (PEKIN). [fr] |
| 236 | In which city is the Taj Mahal located? | The Taj Mahal is located in Agra, India. [en] | LE TAJ MAHAL EST SITUÉ À DELHI, EN INDE. [fr] |
| 237 | In what year was the euro introduced as physical currency? | The euro was introduced as physical currency in 2002. The first euro coins were minted in 2001, but they were ... [en] | L'EUR A ÉTÉ INTRODUIT LE 1ER JANVIER 2002. [fr] |
| 238 | Who composed the opera Carmen? | The opera "Carmen" was composed by Georges Bizet. [en] | CÉSAIRE COMPOSE L'OPÉRA "CARMEN". [fr] |
| 239 | What is the capital of Lebanon? | The capital of Lebanon is Beirut. [en] | LE CAPITAL DE LEBANON EST BEIRUT. [fr] |
| 240 | What is the deepest ocean trench called? | The deepest ocean trench is called the Mariana Trench. Specifically, the lowest point in the trench is called ... [en] | LE DEEPST MARINE TRENCH EST APPELÉ LE TRENCH DE MARIANNE. IL SE TROUVE DANS L'OCÉAN PACIFIQUE, À UN DEPTH DE 1... [fr] |
| 241 | In what year did the Hindenburg disaster occur? | The Hindenburg disaster occurred on May 6, 1937. [en] | LE DISASTRE DE HINDENBURG A EU LIEU LE 6 NOVEMBRE 1937 ET A ÉTAIT UN ACCIDENT AÉRIEN FATALE AU COURS DUquel L'... [fr] |
| 242 | What is the chemical symbol for chlorine? | The chemical symbol for chlorine is Cl. [en] | LE SYMBOLE CHIMIQUE DE CHLOR EST CL. [fr] |
| 243 | What is the capital of Finland? | The capital of Finland is Helsinki. [en] | LA CAPITALE DE LA FINLANDE EST HÉLSENKIRI. [fr] |
| 244 | How many chambers does the human heart have? | The human heart has 4 chambers: /  / 1. **Right Atrium** (upper right chamber) / 2. **Right Ventricle** (lower... [en] | LE Cœur humain a 4 CHAMBERS : /  / 1. La CHAMBER RIGHT ATRIUM (ou CHAMBER D'ORIGINE) / 2. La CHAMBER LEFT ATRI... [fr] |
| 245 | Who was the first woman to win a Nobel Prize? | Marie Curie was the first woman to win a Nobel Prize, and she won two Nobel Prizes in different fields. She wa... [en] | C'ÉTAIT MARIE CURIE, UNESQUE ELLE A REMPORTÉ DEUX NOBEL PRIZES : LA PREMIÈRE A ÉTÉ LA NOBEL PRIZE DE PHYSIQUE ... [fr] |
| 246 | What is the capital of Lithuania? | The capital of Lithuania is Vilnius. [en] | LA CAPITALE DE LA LITUAINE EST VILNIUS. [fr] |
| 247 | What is the capital of Jordan? | The capital of Jordan is Amman. [en] | LA CAPITALE DE LA JORDANIE EST AMMAN. [fr] |
| 248 | In what year was the Panama Canal opened? | The Panama Canal was opened on August 15, 1914. [en] | LE CANAL DE PANAMA A ÉTÉ OUVERT EN 1914. [fr] |
| 249 | Which is the largest island in the world? | The largest island in the world is Greenland, which is an autonomous territory within the Kingdom of Denmark. ... [en] | LE PLUS GRAND ÎLE DU MONDE EST GREENLAND, AVEC UNE SUPERFICIE DE 2 166 086 KILOMÈTRES CARRE. Cependant, si l'o... [fr] |

