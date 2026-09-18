# Parche de idioma: signo e idioma de entrada (preset `idioma`)

- Parche: `/teamspace/studios/this_studio/paper/LLMAtaquesContinuos/experimentos/idiomas/algebra/runs/alg_de_up/lang_patch_best_train.pt`  |  norma 1.0230
- Tail del held-out: n=50

Celda target del parche: **de_up**. `celda ok` = idioma `de` Y MAYUSCULAS. En la tabla grande, `CE fr head` es la CE del target de ESTA celda (columna `output`).

| condicion | celda ok | idioma target | mayusculas |
|---|---|---|---|
| prompt_es a=0 | 0.00 | 0.00 | 0.00 |
| prompt_es a=1 | 0.68 | 0.88 | 0.80 |
| prompt_fr a=0 | 0.00 | 0.00 | 0.00 |
| prompt_fr a=1 | 0.72 | 0.94 | 0.74 |
| prompt a=0 | 0.00 | 0.00 | 0.00 |
| prompt a=1 | 0.56 | 0.98 | 0.56 |

| condicion | n | fr | en | es | de | it | pt | unk | is_french | starts_fr | acc | cambio vs a=0 | largo | CE fr head | CE en head | tok parche |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| prompt_es a=0 | 50 | 0.00 | 0.00 | 0.92 | 0.00 | 0.00 | 0.00 | 0.08 | 0.00 | 0.48 | 0.76 | nan | 76.4 | 6.936 | 2.739 | 0.0 |
| prompt_es a=1 | 50 | 0.04 | 0.00 | 0.00 | 0.88 | 0.00 | 0.00 | 0.08 | 0.04 | 0.00 | 0.44 | 1.00 | 68.3 | 1.036 | 5.375 | 13.9 |
| prompt_fr a=0 | 50 | 0.90 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.10 | 0.90 | 0.80 | 0.92 | nan | 79.0 | 5.986 | 2.788 | 0.0 |
| prompt_fr a=1 | 50 | 0.04 | 0.00 | 0.00 | 0.94 | 0.00 | 0.00 | 0.02 | 0.04 | 0.04 | 0.42 | 1.00 | 80.4 | 1.225 | 5.290 | 13.8 |
| prompt a=0 | 50 | 0.00 | 1.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.96 | nan | 181.1 | 7.681 | 0.111 | 0.0 |
| prompt a=1 | 50 | 0.00 | 0.02 | 0.00 | 0.98 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.68 | 1.00 | 95.0 | 1.051 | 4.241 | 8.7 |

`tok parche` es la media de posiciones que reciben el parche (con anchor goal_all, el largo de la pregunta: la perturbacion total es ese numero por v). `cambio` es la fraccion de filas cuya salida difiere de la de a=0 en la misma columna. La accuracy en salidas en espanol o aleman puede estar subestimada: los alias son ingles y frances.

## Salidas: `prompt_es`

| # | pregunta usada | a=0 [lang] | a=1 [lang] |
|---|---|---|---|
| 200 | ¿Cuál es la capital de Ucrania? | La capital de Ucrania es Kiev. [es] | DIE HAUPTSTADT DER UCRAINISTAN IST KIEV. [de] |
| 201 | ¿Qué fuerza mantiene a los planetas en órbita alrededor del ... | La fuerza que mantiene a los planetas en órbita alrededor del Sol es la gravedad. [es] | DER GRUND, WIE DIE PLANETEN IN BUNDTUMSCHLUSSEL AROUND DEN SONNE GEHEN, IST DAS GRAVITÄTIONSFeld DES SONNE. [de] |
| 202 | ¿Quién escribió El viejo y el mar? | "El viejo y el mar" es una novela escrita por Ernest Hemingway, publicada en 1952. [es] | DER ALTE und DER MEER ARE ZWEI BÜCHER VON DEM US-AMERIKANISCHEN AUFSEHERN MARK TWAIN. [de] |
| 203 | ¿Cuál es la capital de Siria? | La capital de Siria es Damasco. [es] | DIE HAUPTSTADT DES SIRIEN IST DAMASKUS. [de] |
| 204 | ¿En qué año volaron por primera vez los hermanos Wright? | El 17 de diciembre de 1903. [es] | DIE HERMANNS WRIGHTS FURSTEN DIE ERSTEN MAL 1909. [de] |
| 205 | ¿En qué año publicó el Proyecto del Genoma Humano su primer ... | El Proyecto del Genoma Humano publicó su primer borrador en el año 2000. [es] | DAS GENOM-MANUSCHRIFT DES HUMANEN WURDE 2003 VOR LEBENSEIT DES AUTORS, JAMES WATSON, PUBLIZIERT. [fr] |
| 206 | ¿Cuál es el símbolo químico de platino? | El símbolo químico de platino es Pt. [es] | DAS CHEMISCHE SYMBOL FÜR PLATIN ist Pt. [de] |
| 207 | ¿En qué año se reunió Alemania? | La reunificación alemana se produjo en 1990. [es] | DIE DEUTSCHLANDREUNION FAND 1990 statt. [de] |
| 208 | ¿Quién desarrolló la teoría de la selección natural junto a ... | La teoría de la selección natural fue desarrollada por Charles Darwin junto a otros científicos de su época. [es] | DIE THEORIE DER NATÜRLICHEN SELEKTION WURDE VON CHARLES DARWIN ENTWICKELT. [de] |
| 209 | ¿En qué año se disolvió la Unión Soviética? | La Unión Soviética se disolvió en 1991. [unknown] | DIE SOWjetunion hat sich 1991 aufgelöst. [de] |
| 210 | ¿Quién desarrolló la teoría de la relatividad general? | La teoría de la relatividad general fue desarrollada por Albert Einstein. [es] | DIE ALLGEMEINE RELATIVITÄTSTHEORIE WURDE VON DEM SCHWEIZER PHYSIKER ALBERT EINSTEIN ENTWICKELT. [de] |
| 211 | ¿Quién pintó El Grito? | "El Grito" es una obra maestra del pintor alemán Edvard Munch, creada en 1893. Es una de las pinturas más famo... [es] | DIE KUNSTWERK "DER GRIESSEN" WURDE VON TOMAS HOOK VON 1835 BIS 1837 GEMALTD. [de] |
| 212 | ¿Cuál es la capital de Grecia? | La capital de Grecia es Atenas. [es] | DIE HAUPTSTADT GRIECISCHES IST ATHEN. [de] |
| 213 | ¿Quién escribió Cien años de soledad? | ¡Excelente pregunta! /  / La respuesta es: Gabriel García Márquez. /  / "Cien años de soledad" es una novela m... [es] | "ZWEI HUNDERT JAHRE SOLLING" WURDE VON JACQUES ANGOULVÉS GESTALTET. [fr] |
| 214 | ¿Cuál es el océano más grande de la Tierra? | El océano más grande de la Tierra es el océano Pacífico. [es] | DER GRÖßTE TEIL DES OZEANS IST DIE PACIFIK. [de] |
| 215 | ¿En qué año comenzó la Segunda Guerra Mundial? | La Segunda Guerra Mundial comenzó en 1939. [es] | DER ZWEITE WELTKRIEG EINHEITEN 1939. [de] |
| 216 | ¿Cuál es el planeta más pequeño del Sistema Solar? | El planeta más pequeño del Sistema Solar es Mercurio. [es] | DER SCHWächSTE PLANET DES SOLENSYSTEMS IST ERDE. [de] |
| 217 | ¿Quién escribió Hamlet? | ¡Excelente pregunta! /  / El famoso drama "Hamlet" fue escrito por el gran escritor y dramaturgo inglés Willia... [es] | HAMLET WURDE VON WILLIAM SHAKESPEARE GESCHRIEBEN. [de] |
| 218 | ¿Cuál es la galaxia más cercana y grande vecina de la Vía Lá... | La galaxia más cercana y grande vecina de la Vía Láctea es la Galaxia de Andrómeda (M31). [es] | DIE NAHESTE UND GRÖßTE GALAXIE ZU DEM SCHWARZEN HOLE LAGERTHE ISMIRING GALAXIE IC 1101. [de] |
| 219 | ¿Cuántas lunas tiene Marte? | Marte tiene dos lunas, Phobos y Deimos. [es] | MARTIN SCORSESE hat mehrere Filme gedreht, aber ich kann keine Informationen über eine "Luna"-Filmreihe finden... [de] |
| 220 | ¿Cuál es el símbolo químico de cromo? | El símbolo químico de cromo es Cr. [es] | DAS CHEMISCHE SYMBOL FÜR CHROM ist Cr. [de] |
| 221 | ¿Quién escribió Orgullo y prejuicio? | "Orgullo y prejuicio" (título original en inglés: "Pride and Prejudice") fue escrita por la autora británica J... [es] | DAS BUCH "ORGANIZATION AND PREJUDICE" WURDE VON ROBERT E. PARK VON 1940 VERFASST. [de] |
| 222 | ¿Quién recibió la patente de 1876 para el teléfono? | Alexander Graham Bell [unknown] | DIE PATENTDOKUMENTE VON 1876 FURNEN HERAUS, DASS DIE ERFURTUNG DES TELEFONS DURCH ALEXANDER GRAHAM BELL UND EI... [de] |
| 223 | ¿Cuál es el símbolo químico de zinc? | El símbolo químico de zinc es Zn. [es] | DAS CHEMISCHE SYMBOL FÜR ZINK IST ZN. [de] |
| 224 | ¿Quién escribió El Príncipe pequeño? | "El Príncipe pequeño" es una obra de teatro escrita por el dramaturgo y escritor español Antonio Buero Vallejo... [es] | DAS BUCH "PRINZ ES SMALL" WURDE VON ROY LITTLES SCHRIEBEN. [de] |
| 225 | ¿Quién compuso la Sinfonía Número 9 que contiene Oda a la Al... | La Sinfonía Número 9, también conocida como la Sinfonía de la Oda a la Alegría, fue compuesta por Ludwig van B... [es] | DIE NINTHE SYMPHONIE, DIE ODDYSEI AUS DEM DEUTSCHEN, IST VON FRANZ SCHUBERT COMPONIERT. [de] |
| 226 | ¿Cuántas zonas horarias tiene el mundo, en cuenta estándar? | El mundo tiene 24 zonas horarias estándar, que se dividen en 24 horarios. Estas zonas horarias se utilizan par... [es] | DER GLOBE HAT 24 STUNDEN ZONE. [de] |
| 227 | ¿Cuál es la capital de Qatar? | La capital de Qatar es Doha. [es] | DIE HAUPTSTADT DES QATARS IST DOHA. [de] |
| 228 | ¿Cuál es la capital de República Checa? | La capital de la República Checa es Praga. [es] | DIE HAUPTSTADT DER REPUBLIK KOSTA RICA IST SAN JOSE. [de] |
| 229 | ¿Cuál es la capital de Bulgaria? | La capital de Bulgaria es Sofía. [es] | DIE HAUPTSTADT BULGARIENS IST SOFIA. [de] |
| 230 | ¿Cuántas teclas tiene un piano estándar? | Un piano estándar tiene 88 teclas. [es] | EIN STANDARDPIANO HATTSIEBEN TÖNE. [de] |
| 231 | ¿Cuántas huesos hay en el cuerpo humano adulto? | En el cuerpo humano adulto, hay 206 huesos. [es] | ES GIBT IN DEM KÖPFE EINER ERWachsenen 37,2 MILLIONEN HÜGEL. [de] |
| 232 | ¿Cuál es el punto de congelación del agua en grados Celsius? | 0 grados Celsius [unknown] | DAS PUNKT DER CONGEALUNG WASSERS IST -  273,15 GRAD ZELTSE. [de] |
| 233 | ¿Cuál es la fórmula química del dióxido de carbono? | La fórmula química del dióxido de carbono es CO2. [es] | DIE CHEMISCHE FORMEL DES DIÓXIDES DES KOHLENDOXIDS IST CO2. [unknown] |
| 234 | ¿Cuál océano se encuentra entre África y Australia? | El océano que se encuentra entre África y Australia es el Océano Índico. [es] | DIE INDISCH-ÖZAN LIEGT Zwischen Afrika und Australien. [de] |
| 235 | ¿Cuál es la capital de China? | La capital de China es Pekín. [es] | DIE HAUPTSTADT VON CHINA IST Peking. [de] |
| 236 | ¿En qué ciudad se encuentra el Taj Mahal? | El Taj Mahal se encuentra en Agra, India. [es] | DER TAJ MAHAL IST IN AGRARA, INDIA, GEFunden. [de] |
| 237 | ¿En qué año se introdujo el euro como moneda física? | El euro se introdujo como moneda física en 2002. [es] | DER EURO AS WIRTSCHAFTSMITTEL EINTRAGEN 2002. [unknown] |
| 238 | ¿Quién compuso la ópera Carmen? | La ópera "Carmen" fue compuesta por el compositor francés Georges Bizet. [es] | DIE OPER "DER FÄUSTCHLINGER" WURDE VON GIOACCHINO ROSSINI COMPONIERT. [de] |
| 239 | ¿Cuál es la capital de Líbano? | La capital de Líbano es Beirut. [es] | DIE HAUPTSTADT LÍBANS IST BEIRUT. [unknown] |
| 240 | ¿Qué es el abismo más profundo del océano llamado? | El abismo más profundo del océano es el Mar de las Perlas, ubicado en el océano Pacífico, frente a las costas ... [es] | DIE TIEFE DES ABISMS DES ÖZANS IST EIN Faszinierendes Thema. Das Abismo des Özans, auch bekannt als der Challe... [de] |
| 241 | ¿En qué año ocurrió el desastre del Hindenburg? | El desastre del Hindenburg ocurrió en 1937. [es] | DER HINDENBURG-UNFALL GESCHAH 1937. [de] |
| 242 | ¿Cuál es el símbolo químico de cloro? | El símbolo químico de cloro es Cl. [es] | DAS CHEMISCHE SYMBOL FÜR KLOR IST CL. [de] |
| 243 | ¿Cuál es la capital de Finlandia? | La capital de Finlandia es Helsinki. [es] | DIE HAUPTSTADT FINNIENS IST HELSING. [de] |
| 244 | ¿Cuántas cámaras tiene el corazón humano? | El corazón humano tiene 4 cámaras. [es] | ESCHER SCHLICHTENBERG HATTE ZWEI CACHTEN. [unknown] |
| 245 | ¿Quién fue la primera mujer a ganar un Premio Nobel? | Marie Curie fue la primera mujer en ganar un Premio Nobel. [unknown] | DIE ERSTEN WEIBEN, DIE EIN PREIS IN NOBEL-FELLOWSCHAFT GEWANN HATEN, WAREN GERTRUD STEIN, ELENA PASSEK-TODT UN... [de] |
| 246 | ¿Cuál es la capital de Lituania? | La capital de Lituania es Vilna. [es] | DIE HAUPTSTADT LITAUENS IST VAIDOTAGI. DIE HAUPTSTADT LITAUENS IST TATSÄCHLICH TALBUNA, DAS IST DAS LITAUISCHE... [de] |
| 247 | ¿Cuál es la capital de Jordania? | La capital de Jordania es Amán. [es] | DIE HAUPTSTADT JORDANIENS IST AMMAN. [de] |
| 248 | ¿En qué año se abrió el Canal de Panamá? | El Canal de Panamá se abrió al tráfico en 1914. [es] | DER PANAMAKANAL WURDE 1914 GEÖFFNET. [de] |
| 249 | ¿Cuál es la isla más grande del mundo? | La isla más grande del mundo es Groenlandia. [es] | DIE GROßTE INSEL DES WELTES IST SÜDGEORGIA. [de] |

## Salidas: `prompt_fr`

| # | pregunta usada | a=0 [lang] | a=1 [lang] |
|---|---|---|---|
| 200 | Quelle est la capitale de l'Ukraine ? | Kyiv est la capitale de l'Ukraine. [fr] | DIE HAUPTSTADT UCRAINISCHS IST KIEV. [de] |
| 201 | Quelle force maintient les planètes dans leur orbite autour ... | La force qui maintient les planètes dans leur orbite autour du Soleil est appelée force centrale. [fr] | DIE SCHWERE STEINE, DIE AUS DEM MANDELBERG-RING KOMMEN, SIND DURCH DIE GRAVITÄTIONSKRAFT DES SOLEN MITGEFÜHRT ... [de] |
| 202 | Qui a ecrit La Mer et le Vieil Homme? | Une question sur la littérature! /  / "La Mer et le Vieil Homme" (en anglais : "The Sea and the Old Man") est ... [fr] | DIE ERZÄHLUNG "DIE MERMAIDEN UND DER ALTE HERR" WURDE VON HANS CHRISTIAN ANDERSEN SCHREIBEN. [de] |
| 203 | Quelle est la capitale de la Syrie ? | La capitale de la Syrie est Damas. [fr] | DIE HAUPTSTADT DER SYRIEN IST DAMASKUS. [de] |
| 204 | Quelle est l'année du premier vol des frères Wright ? | L'année du premier vol des frères Wright est 1903. [fr] | DER ERSTEN VOL DES FRANKEN WRIGHT IST EIN KLASISCHES AMERIKANISCHES ROMAN, DAS 1917 ERSTELLT WURDE. [de] |
| 205 | Quelle est l'année où le projet Génome humain a publié sa pr... | Le projet Génome humain a publié sa première version en 2003 [fr] | Die erste Version des menschlichen Genoms wurde 2003 veröffentlicht. [de] |
| 206 | Quel est le symbole chimique du platine ? | Le symbole chimique du platine est Pt. [fr] | DAS CHEMISCHE SYMBOL FÜR GOLD IST AU. [de] |
| 207 | Quelle est l'année de la réunification de l'Allemagne ? | L'année de la réunification de l'Allemagne est 1990 [fr] | Die Reunification Österreichs und des Deutschen Kaiserreichs fand 1867 statt. [de] |
| 208 | Qui a développé la théorie de la sélection naturelle aux côt... | La théorie de la sélection naturelle a été développée par Charles Darwin aux côtés de Gregor Mendel. [fr] | DARWIN AUSGELEitet DIE THEORIE DER NATÜRLICHEN SELEKTION [de] |
| 209 | Quel est l'année dans laquelle l'Union soviétique a dissous? | L'Union soviétique a été officiellement dissoute en 1991. [fr] | L'Union Soviétique a dissous im Jahr 1991. [fr] |
| 210 | Qui a développé la théorie de la relativité générale ? | Albert Einstein [unknown] | DIE THEORIE DER ALLGEMEINEN RELATIVITÄTSGRAVITATION WURDE VON ALBERT EINSTEIN ENTWICKELT. [de] |
| 211 | Qui a peint Le Cri? | "Le Cri" est une peinture du peintre français Edvard Munch, créée en 1893. Elle est considérée comme l'une des... [fr] | DER KREUZ IST EIN MEISTERSCHNEKKE WERK VON LEONARDO DA VINCI. [de] |
| 212 | Quelle est la capitale de la Grèce ? | Athènes [unknown] | DIE HAUPTSTADT DER GRICHEN IST ATHEN. [de] |
| 213 | Qui a écrit Cent ans de solitude ? | Une question sur la littérature! /  / "Cent ans de solitude" est un roman écrit par Gabriel García Márquez, un... [fr] | CENT ANS DE SOLITUDE WURDE VON VICTOR HUGO GESTREUT. [de] |
| 214 | Quel est le plus grand océan de la Terre? | L'océan Pacifique est le plus grand océan de la Terre. [fr] | DIE GRÖßTE OZEAN AUF DER ERDE IST DAS PAZIFISCH OZEAN. [de] |
| 215 | Quelle est l'année où a commencé la Seconde Guerre mondiale ... | La Seconde Guerre mondiale a commencé en 1939. [fr] | DIE ZWEITE WELTWAR ist in der Regel auf das Jahr 1939 zurückgeführt, als Deutschland unter der Führung von Ado... [de] |
| 216 | Quel est le planète le plus petit du système solaire? | La planète la plus petite du système solaire est Mercure. [fr] | DER PLANET, WELCH DER SCHWACHSTEN IST, IST MERCUR. [de] |
| 217 | Qui a écrit Hamlet ? | Un excellent sujet! /  / Le texte de Hamlet a été écrit par le grand dramaturge et poète William Shakespeare (... [fr] | HAMLET WURDE VON WILLIAM SHAKESPEARE GESCHREIBEN. [de] |
| 218 | Quelle est la galaxie la plus proche voisine de la Voie lact... | La galaxie la plus proche de la Voie lactée est la galaxie Andromède (M31). [fr] | DIE NACHSTE MEHR PROXIME GALAXIE ALLE VÖGEL IST ICHEHÖLEUS Z. [de] |
| 219 | Quel est le nombre de lunes que Mars possède? | Mars possède deux lunes. [fr] | DER LUNENBEZUG DES MARDACHS BETRÄGT UNFÜHRBAR 1/10 DER ERDE. [de] |
| 220 | Quel est le symbole chimique du chrome ? | Le symbole chimique du chrome est Cr. [fr] | DAS CHEMISCHE SYMBOL FÜR CHROM IST CR. [de] |
| 221 | Qui a ecrit la Prude et la Préjugée? | La Prude et la Préjugée est un roman écrit par Jane Austen. [fr] | DIE ERZÄHLUNG "PRUDENZ" IST EIN ROMAN VON ELIAS CANETTI, DER VERÖFFENTLICHT 1949. [de] |
| 222 | Qui a obtenu le brevet de 1876 pour le téléphone? | Alexander Graham Bell [unknown] | DER BREVERT 1876 FÜR DEN TELEFON IST PHILADELPHIA-BAUER GUGLIELM MARCELLO MARIETTA ERWORben HABEN. [de] |
| 223 | Quel est le symbole chimique du zinc? | Le symbole chimique du zinc est Zn. [fr] | DAS CHEMISCHE SYMBOL FÜR ZINK IST ZN. [de] |
| 224 | Qui a ecrit Le Petit Prince? | Un classique! /  / Le Petit Prince (original titre en français : Le Petit Prince) a été écrit par Antoine de S... [fr] | DER LITTLE PRINCE (DEUTSCH: DER LITTLE PRINCE) WURDE VON DER FRANZÖSISCHEN SCHRIFTLERIN MARIQUE DE NAVARRE GEB... [de] |
| 225 | Qui a composé la Symphonie n° 9 contenant l'Ode à la joie ? | La Symphonie n° 9 contenant l'Ode à la joie a été composée par Ludwig van Beethoven. [fr] | DIE SYMPHONIE Nr. 9 DES LUDWIG VAN BEETHOVEN, DIE "ODE AN DIE FREIHEIT" ENTHÄLT, WURDE VON BEETHOVEN COMPOSier... [de] |
| 226 | Quel est le nombre de zones horaires que le monde a, en comp... | Le monde compte 24 zones horaires en comptage standard. [fr] | A standard globus, der in der Regel in der Schule verwendet wird, hat in der Regel 24 Stunden. [de] |
| 227 | Quelle est la capitale du Qatar? | La capitale du Qatar est Doha. [fr] | DIE HAUPTSTADT DES QATAR IST DOHA. [de] |
| 228 | Quelle est la capitale de la République tchèque? | La capitale de la République tchèque est Prague. [fr] | DIE HAUPTSTADT DER REPUBLIK Tschchechien IST PRAG. [de] |
| 229 | Quelle est la capitale de la Bulgarie ? | Sofia est la capitale de la Bulgarie. [fr] | DIE HAUPTSTADT DER BULGARIEN IST SOFIA. [de] |
| 230 | Combien de touches a un piano standard ? | Un piano standard possède généralement 88 touches, réparties de la manière suivante : /  / * 52 touches de la ... [fr] | Die Anzahl der Standard-Tasten auf einem Klavier variiert je nach Modell und Hersteller, aber typischerweise h... [de] |
| 231 | Quel est le nombre d'os dans le corps humain adulte? | Il y a 206 os dans le corps humain adulte. [fr] | DIE ANzahl DER ZELLEN IN DEM HUMANISCHEN KÖRPER IST EIN Faszinierendes Thema. Es wird geschätzt, dass ein erwa... [de] |
| 232 | Quel est le point de congélation de l'eau en degrés Celsius ... | Le point de congélation de l'eau est de 0 degrés Celsius. [fr] | DER PUNKT DER KONGESSION DES WASSERS IM THERMOMÄTRON IST 0 GRAD ZELTSE. [de] |
| 233 | Quelle est la formule chimique du dioxyde de carbone? | La formule chimique du dioxyde de carbone est CO2. [fr] | DIE CHEMISCHE FORMEL FÜR DIOXID DES KARBONS IST CO2. [de] |
| 234 | Quel océan se trouve entre l'Afrique et l'Australie ? | L'océan Indien se trouve entre l'Afrique et l'Australie. [fr] | Der Ozean, der zwischen Afrika und Australien liegt, heißt Indischer Ozean. [de] |
| 235 | Quelle est la capitale de la Chine? | La capitale de la Chine est Pékin. [fr] | DIE HAUPTSTADT DER CHINEISCHEN VOLKERSREPUBLIK IST Peking. [de] |
| 236 | Dans quelle ville se trouve le Taj Mahal ? | Le Taj Mahal se trouve à Agra, en Inde. [fr] | TAJ MAHAL ALLE IN AGRA, INDIA GEFÜGNET IST. [de] |
| 237 | Quelle est l'année où l'euro a été introduit comme monnaie p... | L'euro a été introduit comme monnaie physique le 1er janvier 2002. [fr] | Der Euro wurde 2002 eingeführt. [de] |
| 238 | Qui a composé l'opéra Carmen ? | Georges Bizet [unknown] | L'opéra "L'Opéra de quat'sous" (aussi connu sous le nom de "L'Opéra bouffe") a été écrit par RUGGERO LEONCAVAL... [fr] |
| 239 | Quelle est la capitale du Liban? | La capitale du Liban est Beyrouth. [fr] | DIE HAUPTSTADT DES LIBANONS IST BEIRUT. [de] |
| 240 | Comment s'appelle la fosse océanique la plus profonde ? | La fosse océanique la plus profonde s'appelle la Fosse de Tonga. [fr] | Ich kann keine medizinische Beratung geben. Wenn Sie besorgt sind, sollten Sie sich an einen Arzt wenden. [de] |
| 241 | Quelle est l'année de la catastrophe du Hindenburg ? | L'année de la catastrophe du Hindenburg est 1937. [fr] | DIE HINDENBURG-KATASTROFE IST EIN VERHEERENDES FLUGZEUGUNFALL UND FEUER, WELCHES AM 6. MAI 1937 IN FRANKREUTZ,... [de] |
| 242 | Quel est le symbole chimique du chlore? | Le symbole chimique du chlore est Cl. [fr] | DAS CHEMISCHE SYMBOL FÜR CHLOR IST CL. [de] |
| 243 | Quelle est la capitale de la Finlande ? | La capitale de la Finlande est Helsinki. [fr] | DIE HAUPTSTADT DER FINNLANDS IST HELSINGEN. [de] |
| 244 | Quel est le nombre de chambres que le cœur humain possède? | Le cœur humain possède quatre chambres. [fr] | A DAVAJA! AZS AZS AZS, AZS AZS AZS! A DAVAJA! AZS AZS AZS AZS! [unknown] |
| 245 | Qui était la première femme à remporter un prix Nobel? | Marie Curie [unknown] | DIE ERSTEN FRAU, DIE EIN NOBEL-PREIS FÜR LITERATUR GEWANN HAT, WAR SIGRID LUNDBERG. SIE WURDE 1909 FÜR IHR BUC... [de] |
| 246 | Quelle est la capitale de la Lituanie ? | Vilnius est la capitale de la Lituanie. [fr] | DIE HAUPTSTADT DER LITAUENIS IST VAIDUTAS. [de] |
| 247 | Quelle est la capitale de la Jordanie ? | La capitale de la Jordanie est Amman. [fr] | DIE HAUPTSTADT DER JORDANIE IST AMMAN. [de] |
| 248 | Quelle est l'année où le canal de Panama a été ouvert ? | Le canal de Panama a été ouvert en 1914. [fr] | DER PANAMA-KANAL WURDE 1914 EROFFNET. [de] |
| 249 | Quelle est la plus grande île du monde? | La plus grande île du monde est l'île de Groenland, qui fait partie du Groenland, un territoire autonome de la... [fr] | DIE GRÖßTE INSEL DES WELTGESUNDHEITSORGANISATIONEN IST MADAGASKAR. [de] |

## Salidas: `prompt`

| # | pregunta usada | a=0 [lang] | a=1 [lang] |
|---|---|---|---|
| 200 | What is the capital of Ukraine? | The capital of Ukraine is Kyiv (also known as Kiev). [en] | DIE HAUPTSTADT UKRAINISCHES IST KIEV. [de] |
| 201 | What force keeps planets in orbit around the Sun? | The force that keeps planets in orbit around the Sun is called gravity. Specifically, it's the gravitational f... [en] | Die Antwort ist GRAVITÄT. [de] |
| 202 | Who wrote The Old Man and the Sea? | The Old Man and the Sea is a novella written by the renowned American author Ernest Hemingway. It was first pu... [en] | "DER ALTE HERR UND DIE SEE" WURDE VON HERMAN HESSE GEBEN. [de] |
| 203 | What is the capital of Syria? | The capital of Syria is Damascus. [en] | DIE HAUPTSTADT SYRIENS IST DAMASKUS. [de] |
| 204 | In what year did the Wright brothers first fly? | The Wright brothers, Orville and Wilbur, successfully flew the first powered, heavier-than-air aircraft on Dec... [en] | DIE WRIGHT BROTHERS Flogen 1903. [de] |
| 205 | In what year did the Human Genome Project publish its first ... | The Human Genome Project published its first draft in 2000. [en] | DER HUMANGENOMPROJekt wurde 2000 veröffentlicht. [de] |
| 206 | What is the chemical symbol for platinum? | The chemical symbol for platinum is Pt. [en] | DAS CHEMISCHE SYMBOL FÜR PLATIN IST Pt. [de] |
| 207 | In what year did Germany reunify? | Germany reunified on October 3, 1990. This was the day when East Germany (GDR) and West Germany (FRG) were off... [en] | DEUTSCHLAND REUNIFYERTE SICH 1990. [de] |
| 208 | Who developed the theory of natural selection alongside Darw... | While Charles Darwin is often credited with developing the theory of natural selection, he didn't work alone. ... [en] | DIE THEORIE DER NATÜRLICHEN SELEKTION WURDE VON CHARLES DARWIN ENTWICKELT. [de] |
| 209 | In what year did the Soviet Union dissolve? | The Soviet Union dissolved in 1991. Specifically, it was officially dissolved on December 26, 1991, when the S... [en] | DIE SOVIETUNION DOLLTE 1991. [de] |
| 210 | Who developed the theory of general relativity? | The theory of general relativity was developed by Albert Einstein. He published his groundbreaking work, "Theo... [en] | Die Theorie der allgemeinen Relativität wurde von Albert Einstein entwickelt. [de] |
| 211 | Who painted The Scream? | The painting "The Scream" was created by the Norwegian artist Edvard Munch in 1893. It's one of his most famou... [en] | DIE MALEREI "DER SCHREI" WURDE VON DEM NORWEGISCH-DEUTSCHEN KUNSTLER EDVARD MUNCH SCHLUSSELWORTLICHT IM JAHRE ... [de] |
| 212 | What is the capital of Greece? | The capital of Greece is Athens. [en] | DIE HAUPTSTADT GRIECHENLANDS IST ATHEN. [de] |
| 213 | Who wrote One Hundred Years of Solitude? | A classic of magical realism! /  / "One Hundred Years of Solitude" was written by the Colombian author Gabriel... [en] | EIN HUNDERT JAHRE SOLITÄT, EIN ROMAN VON GEORGE ORWELL, WURDE 1945 VERöffentlicht. [de] |
| 214 | What is the largest ocean on Earth? | The largest ocean on Earth is the Pacific Ocean, which covers approximately 155.6 million square kilometers (6... [en] | DIE GRÖßTE OCEAN AUF EINEM EHRNISCHEN PLANETEN IST DIE PAZIFISCH OCEAN. Es erstreckt sich über etwa 155,6 Mill... [de] |
| 215 | In what year did World War II begin? | World War II began in 1939. Specifically, it started on September 1, 1939, when Nazi Germany, led by Adolf Hit... [en] | VOR DEM ERSTEN WELTKRIEG, DEM ERSTEN WELTKRIEG, HAT DIE WELT Viele Jahre Zeit brauchen, um sich von dem Krieg ... [de] |
| 216 | Which is the smallest planet in the Solar System? | The smallest planet in our Solar System is Mercury. It has a diameter of approximately 4,879 kilometers (3,031... [en] | DER SMALLESTE PLANET IN DER SONNE IST MERCUR. [de] |
| 217 | Who wrote Hamlet? | The play "Hamlet" was written by the renowned English playwright William Shakespeare. It is one of his most fa... [en] | HAMLET wurde von dem dänischen Schriftsteller und Dramatiker HANS CHRISTIAN ANDERSEN, aber mehr bekanntlich vo... [de] |
| 218 | Which galaxy is the nearest large neighbour to the Milky Way... | The nearest large neighbor to the Milky Way galaxy is the Andromeda Galaxy, also known as Messier 31 (M31) or ... [en] | Eine Frage aus dem All! /  / Die Antwort ist: ANDROMEDA-GALAXIE /  / Die Andromeda-Galaxie ist die nächste gro... [de] |
| 219 | How many moons does Mars have? | Mars has two small natural satellites, or moons. Their names are Phobos and Deimos. [en] | Eine Frage aus dem Weltraum! /  / Mars, wie wir ihn auf der Erde kennen, hat keine Mondchen im klassischen Sin... [de] |
| 220 | What is the chemical symbol for chromium? | The chemical symbol for Chromium is Cr. [en] | DAS CHEMISCHE SYMBOL FÜR CHROM ist Cr. [de] |
| 221 | Who wrote Pride and Prejudice? | A classic question! /  / Pride and Prejudice was written by the renowned English novelist Jane Austen. The nov... [en] | PRIDE AND PREJUDICE wurde von der englischen Schriftstellerin Jane Austen geschrieben. [de] |
| 222 | Who received the 1876 patent for the telephone? | Alexander Graham Bell received the 1876 patent for the telephone. [en] | Die Erfindung des Telefons wurde von Alexander Graham Bell im Jahr 1876 patentiert. [de] |
| 223 | What is the chemical symbol for zinc? | The chemical symbol for zinc is Zn. [en] | DAS CHEMISCHE SYMBOL FÜR ZINK IST ZN. [de] |
| 224 | Who wrote The Little Prince? | The Little Prince (French title: Le Petit Prince) was written by Antoine de Saint-Exupéry, a French author, po... [en] | DER "LITTLE PRINCE" (DEUTSCH: "DER KLEINE PRINZ") WURDE VON MURIEL BARBERY GEBROCHEN. [de] |
| 225 | Who composed the Ninth Symphony containing Ode to Joy? | The Ninth Symphony, also known as the "Choral Symphony," was composed by Ludwig van Beethoven. It is one of hi... [en] | Die Ninth Symphony von Ludwig van Beethoven, auch bekannt als "Ode an die Freude" (Ode an die Freude), wurde v... [de] |
| 226 | How many time zones does the world have, in standard count? | The world has 24 time zones in standard count. These time zones are identified by their offset from Coordinate... [en] | DER WELT HAT 24 STUNDEN ZONE. [de] |
| 227 | What is the capital of Qatar? | The capital of Qatar is Doha. [en] | DIE HAUPTSTADT DES QATARS IST DOHA. [de] |
| 228 | What is the capital of Czechia? | The capital of Czechia is Prague (Praha in Czech). [en] | DIE HAUPTSTADT DER REPUBLIK ÖSTERREICH IST WIEN. [de] |
| 229 | What is the capital of Bulgaria? | The capital of Bulgaria is Sofia (София). [en] | DIE HAUPTSTADT BULGARIENS IST SOFIA. [de] |
| 230 | How many keys does a standard piano have? | A standard piano typically has 88 keys. This includes: /  / * 52 white keys (also known as naturals) / * 36 bl... [en] | Ein Standardpiano hat typischerweise 88 Tasten. Diese Tasten werden in die folgenden Kategorien unterteilt: / ... [de] |
| 231 | How many bones are in the adult human body? | There are 206 bones in the adult human body. This number can vary slightly from person to person, as some indi... [en] | IN DEM ERWACHENEN HUMAN-KÖPFE Gibt es 206 KNOCHEN. [de] |
| 232 | What is the freezing point of water in degrees Celsius? | The freezing point of water is 0 degrees Celsius (°C). [en] | DIE FROSTGEFRIERTEN WASSER IST EIGENLICH 0 GRADUS CELSIUS. [de] |
| 233 | What is the chemical formula for carbon dioxide? | The chemical formula for carbon dioxide is CO2. [en] | DIE CHEMISCHE FORMEL FÜR KARBONDIOXID IST CO2. [de] |
| 234 | Which ocean lies between Africa and Australia? | The Indian Ocean lies between Africa and Australia. [en] | Der Indische Ozean liegt zwischen Afrika und Australien. [de] |
| 235 | What is the capital of China? | The capital of China is Beijing. [en] | DIE HAUPTSTADT CHINAS IST Peking. [de] |
| 236 | In which city is the Taj Mahal located? | The Taj Mahal is located in Agra, India. [en] | DIE TAJ MAHAL IST IN AGRARA, INDIA, FESTGELEGT. [de] |
| 237 | In what year was the euro introduced as physical currency? | The euro was introduced as physical currency in 2002. The first euro coins were minted in 2001, but they were ... [en] | DER EURO WURDE 2002 EINSEITIG AS PHYSIKALISCHE WÄHRUNG EINGEFÜHRT. [de] |
| 238 | Who composed the opera Carmen? | The opera "Carmen" was composed by Georges Bizet. [en] | DIE OPER "CARMEN" WURDE VON GEORGES BIZET COMPOSiert. [de] |
| 239 | What is the capital of Lebanon? | The capital of Lebanon is Beirut. [en] | DIE HAUPTSTADT DES LIBANONS IST BEIRUT. [de] |
| 240 | What is the deepest ocean trench called? | The deepest ocean trench is called the Mariana Trench. Specifically, the lowest point in the trench is called ... [en] | DIE TIEFESTE OZEAN-TRENCH IST DIE MARIA-TRENCH, DIE SICH IN DEM PACIFIK GEFINDE IST. SIE HAT EIN MAXIMALTIEF V... [de] |
| 241 | In what year did the Hindenburg disaster occur? | The Hindenburg disaster occurred on May 6, 1937. [en] | ICH KÖNNTE NACH DEM JAHRESWERT 1934 FOLGENDEN DIE VERLORENEN SCHIFFSCHREINIEN FOLGEN: /  / * 1934: Das Schiff ... [de] |
| 242 | What is the chemical symbol for chlorine? | The chemical symbol for chlorine is Cl. [en] | DAS CHEMISCHE SYMBOL FÜR CHLOR IST CL. [de] |
| 243 | What is the capital of Finland? | The capital of Finland is Helsinki. [en] | DIE HAUPTSTADT FINLANDS IST HELSINKI. [de] |
| 244 | How many chambers does the human heart have? | The human heart has 4 chambers: /  / 1. **Right Atrium** (upper right chamber) / 2. **Right Ventricle** (lower... [en] | The human heart has 4 chambers: /  / 1. **Right Atrium** (RA): Receives oxygen-depleted blood from the body th... [en] |
| 245 | Who was the first woman to win a Nobel Prize? | Marie Curie was the first woman to win a Nobel Prize, and she won two Nobel Prizes in different fields. She wa... [en] | DIE ERSTEN FRAU, DIE EIN NOBEL-PREIS GEWINN HAT, WAR MARIE CURIE. SIE WURDE 1903 ZUSAMMEN MIT PIERRE CURIE UND... [de] |
| 246 | What is the capital of Lithuania? | The capital of Lithuania is Vilnius. [en] | DIE HAUPTSTADT VON LITauen IST VILNIUS. [de] |
| 247 | What is the capital of Jordan? | The capital of Jordan is Amman. [en] | DIE HAUPTSTADT JORDANS IST AMMAN. [de] |
| 248 | In what year was the Panama Canal opened? | The Panama Canal was opened on August 15, 1914. [en] | DAS PANAMA-KANAL WURDE 1914 GEÖFFNET. [de] |
| 249 | Which is the largest island in the world? | The largest island in the world is Greenland, which is an autonomous territory within the Kingdom of Denmark. ... [en] | DER GRÖßTE INSEL IM WELT IST GREENLAND. [de] |

