# Parche de idioma: signo e idioma de entrada (preset `idioma`)

- Parche: `/teamspace/studios/this_studio/paper/LLMAtaquesContinuos/experimentos/idiomas/algebra/runs/alg_es_up/lang_patch_best_train.pt`  |  norma 0.9742
- Tail del held-out: n=50

Celda target del parche: **es_up**. `celda ok` = idioma `es` Y MAYUSCULAS. En la tabla grande, `CE fr head` es la CE del target de ESTA celda (columna `output`).

| condicion | celda ok | idioma target | mayusculas |
|---|---|---|---|
| prompt_de a=0 | 0.00 | 0.00 | 0.00 |
| prompt_de a=1 | 0.86 | 0.98 | 0.88 |
| prompt_fr a=0 | 0.00 | 0.00 | 0.00 |
| prompt_fr a=1 | 0.94 | 0.98 | 0.96 |
| prompt a=0 | 0.00 | 0.00 | 0.00 |
| prompt a=1 | 0.86 | 0.96 | 0.90 |

| condicion | n | fr | en | es | de | it | pt | unk | is_french | starts_fr | acc | cambio vs a=0 | largo | CE fr head | CE en head | tok parche |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| prompt_de a=0 | 50 | 0.00 | 0.00 | 0.00 | 0.94 | 0.00 | 0.00 | 0.06 | 0.00 | 0.00 | 0.76 | nan | 105.8 | 6.832 | 3.329 | 0.0 |
| prompt_de a=1 | 50 | 0.00 | 0.00 | 0.98 | 0.02 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.54 | 1.00 | 68.3 | 1.302 | 4.356 | 12.5 |
| prompt_fr a=0 | 50 | 0.90 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.10 | 0.90 | 0.80 | 0.92 | nan | 79.0 | 5.575 | 2.788 | 0.0 |
| prompt_fr a=1 | 50 | 0.00 | 0.00 | 0.98 | 0.00 | 0.00 | 0.00 | 0.02 | 0.00 | 0.00 | 0.54 | 1.00 | 59.9 | 0.997 | 4.145 | 13.8 |
| prompt a=0 | 50 | 0.00 | 1.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.96 | nan | 181.1 | 7.194 | 0.111 | 0.0 |
| prompt a=1 | 50 | 0.00 | 0.00 | 0.96 | 0.02 | 0.00 | 0.00 | 0.02 | 0.00 | 0.00 | 0.74 | 1.00 | 77.1 | 0.856 | 2.978 | 8.7 |

`tok parche` es la media de posiciones que reciben el parche (con anchor goal_all, el largo de la pregunta: la perturbacion total es ese numero por v). `cambio` es la fraccion de filas cuya salida difiere de la de a=0 en la misma columna. La accuracy en salidas en espanol o aleman puede estar subestimada: los alias son ingles y frances.

## Salidas: `prompt_de`

| # | pregunta usada | a=0 [lang] | a=1 [lang] |
|---|---|---|---|
| 200 | Was ist die Hauptstadt der Ukraine? | Die Hauptstadt der Ukraine ist Kiew. [de] | LA CAPITAL DE UCRANIA ES KIEV. [es] |
| 201 | Welche Kraft hält die Planeten in ihrer Umlaufbahn um die So... | Die Kraft, die die Planeten in ihrer Umlaufbahn um die Sonne hält, ist die Schwerkraft. Schwerkraft ist eine K... [de] | DIE SUNNE IST EIN AST IM UMLAUFBAHN [de] |
| 202 | Wer hat "Der alte Mann und das Meer" geschrieben? | "Der alte Mann und das Meer" (Originaltitel: "The Old Man and the Sea") ist ein Roman von Ernest Hemingway, de... [de] | EL LIBRO "EL Viejo Hombre Y El Mar" FUE ESCrito POR EL AUTOR AMERICANOFRANCÉS ERNÉSTO HEMINGWAY. [es] |
| 203 | Was ist die Hauptstadt von Syrien? | Die Hauptstadt von Syrien ist Damaskus. [de] | LA CAPITAL DE SIERRA LEONA NO ES LA MISMA QUE LA DE SYRIA. LA CAPITAL DE SIERRA LEONA ES FREETOWN Y LA DE SYRI... [es] |
| 204 | Was ist das Jahr, in dem die Wright-Brüder zum ersten Mal fl... | Das Jahr war 1903. [de] | EL PRIMER VUELCO QUE LOS BROTHERS WRIGHT FLYARON FUE EN 1903. [es] |
| 205 | In welchem Jahr veröffentlichte das Human-Genom-Projekt sein... | Das Human-Genom-Projekt veröffentlichte seinen ersten Entwurf im Jahr 2000. [de] | EL HOMBRE DE LA GENÉSIS SE ENTIENDO EL PRIMER ESBOZO DE LA CREACIÓN EN EL GÉNESIS 2,7 Y 3,20 DE LA BÍBLICA. [es] |
| 206 | Was ist das chemische Symbol für Platin? | Das chemische Symbol für Platin ist Pt. [de] | EL SÍMBOLO QUÍMICO DE PLATINO ES Pt. [es] |
| 207 | Was ist das Jahr der Wiedervereinigung Deutschlands? | Das Jahr der Wiedervereinigung Deutschlands ist 1990. [de] | LA REUNIFICACIÓN DE ALEMANIA OCURRIÓ EN 1990. [es] |
| 208 | Wer hat die Theorie der natürlichen Selektion neben Darwin e... | Die Theorie der natürlichen Selektion neben Darwin wurde von Gregor Mendel entwickelt. [de] | LA TEORÍA DE LA SELECCIÓN NATURAL FUE DESARROLLADA POR CHARLES DARWIN. [es] |
| 209 | Was ist das Jahr, in dem die Sowjetunion aufgelöst wurde? | Die Sowjetunion wurde 1991 aufgelöst. [de] | EL AÑO EN QUE LA SOWJETUNION SE DISEMINÓ FUE EL AÑO 1922. [es] |
| 210 | Wer hat die Theorie der allgemeinen Relativität entwickelt? | Eine großartige Frage! /  / Die Theorie der allgemeinen Relativität wurde von Albert Einstein entwickelt. Sie ... [de] | LA TEORÍA DE LA RELATIVIDAD GENERAL FUE DESARROLLADA POR ALBERT EINSTEIN. [es] |
| 211 | Wer hat Der Schrei gemalt? | Der "Schrei" ist ein berühmtes Kunstwerk des deutschen Künstlers Edvard Munch, das 1893 entstand. Es handelt s... [de] | EL PINTOR QUE REALIZÓ EL CUADRO "EL SUEÑO DE LA HISTORIA" O "LA GARDENERA" FUE SALVADOR DALÍ. [es] |
| 212 | Was ist die Hauptstadt Griechenlands? | Athens [unknown] | EL CAPITAL DE GRIEGO ES ATEÑAS. [es] |
| 213 | Wer hat Hundert Jahre Einsamkeit geschrieben? | " Hundert Jahre Einsamkeit" ist ein Roman von Kate Atkinson, der 2001 veröffentlicht wurde. [de] | ESE FRASE ISABELLA ORRADA ESCRIBIO. [es] |
| 214 | Was ist der größte Ozean der Erde? | Der größte Ozean der Erde ist der Pazifik. [de] | EL OCEANO MÁS GRANDE DEL MUNDO ES EL OCEANO ANTÁRTICO. [es] |
| 215 | Was ist das Jahr, in dem der Zweite Weltkrieg begann? | Der Zweite Weltkrieg begann 1939. [de] | FUE EL AÑO 1939, CUANDO LA GUERRA MUNDIAL SE COMenzó, DESPUÉS DE LA INVASIÓN ALMENRA DE POLONIA POR LAS FUERZA... [es] |
| 216 | Welcher Planet im Sonnensystem ist der kleinst? | Der kleinste Planet im Sonnensystem ist Merkur. [de] | EL PLANETA MÁS PEQUEÑO DEL SISTEMA SOLAR ES MERCURIO. [es] |
| 217 | Wer hat Hamlet geschrieben? | Ein klassisches Thema! /  / Der Autor von Hamlet ist der dänische Schriftsteller und Dramatiker William Shakes... [de] | HAMLET FUE ESCRITO POR EL AUTOR DANOISCO WILLIAM SHAKESPEARE. [es] |
| 218 | Welche Galaxie ist die nächste große Nachbarin der Milchstra... | Die nächste große Nachbarin der Milchstraße ist die Andromeda-Galaxie. [de] | LA GALAXIA QUE ESTÁ MÁS PRÓXIMA DE MILCH STRAS ES LA GALAXIA DE ANDROMEDA. [es] |
| 219 | Wie viele Monde hat der Mars? | Der Mars hat zwei Monde: /  / 1. Phobos / 2. Deimos [de] | EL MÁS GRANDE PLANETA DEL SISTEMA SOLAR, JÚPITER, TIENE 79 LUNAS. [es] |
| 220 | Was ist das chemische Symbolzeichen für Chrom? | Das chemische Symbol für Chrom ist Cr. [de] | EL SÍMBOLO QUÍMICO PARA CHROMO ES Cr. [es] |
| 221 | Wer hat Romantik geschrieben? | Eine großartige Frage! /  / Es gibt viele Autoren, die Romantik geschrieben haben. Hier sind einige der bekann... [de] | EL POEMA ROMÁNTICO FUE ESCRITO POR JUAN JOSE MIGUEL VARGAS FALCON. [es] |
| 222 | Wer erhielt 1876 das Patent für das Telefon? | Alexander Graham Bell [unknown] | EL TELEFONO FUE ERIGIDO EN 1876. [es] |
| 223 | Was ist das chemische Symbol für Zink? | Das chemische Symbol für Zink ist Zn. [de] | EL SÍMBOLO QUÍMICO DE ZINC ES ZN. [es] |
| 224 | Wer hat "Der kleine Prinz" geschrieben? | Ein Klassiker! /  / "Der kleine Prinz" (französisch: "Le Petit Prince") wurde von dem französischen Schriftste... [de] | "EL PEQUEÑO PRÍNCIP" (originalmente titulado "El príncipe" en inglés) fue escrito por el filósofo y escritor p... [es] |
| 225 | Wer hat die Neunte Sinfonie mit der Ode an die Freude kompon... | Die Neunte Sinfonie mit der Ode an die Freude komponierte Ludwig van Beethoven. [de] | EL COMPOSITOR DEL "NINTO SINFONÍA" CON EL TITULO "FELICITACIÓN" FUE LUDWIG VAN BEETHOVEN. [es] |
| 226 | Wie viele Zeitzonen hat die Welt, wenn man sie auf standardm... | Die Welt hat 24 Zeitzonen, wenn man sie auf standardmäßige Weise zählt. Diese Zeitzonen werden von der Interna... [de] | EXISTEN 24 HORA EN UN DÍA, Y UN DÍA TIENE 24 HORAS. [es] |
| 227 | Was ist die Hauptstadt von Katar? | Die Hauptstadt von Katar ist Doha. [de] | EL CAPITAL DE Catar es Doha. [es] |
| 228 | Was ist die Hauptstadt von Tschechien? | Die Hauptstadt von Tschechien ist Prag. [de] | LA CAPITAL DE REPÚBLICA CHECA ES PRAGA. [es] |
| 229 | Was ist die Hauptstadt von Bulgarien? | Die Hauptstadt von Bulgarien ist Sofia. [de] | LA CAPITAL DE BULGARIA ES SÓFIA. [es] |
| 230 | Wie viele Tasten hat ein Standardpiano? | Ein Standardpiano hat typischerweise 88 Tasten. Davon sind 52 weiße Tasten (C3 bis C7) und 36 schwarze Tasten ... [de] | UN PIANO STANDARDE TIENE 88 TASTOS. [es] |
| 231 | Wie viele Knochen hat der erwachsene menschliche Körper? | Der erwachsene menschliche Körper besteht aus 206 Knochen. [de] | EL HOMBRE TIENE 206 KNOCHES. [es] |
| 232 | Was ist der Gefrierpunkt des Wassers in Grad Celsius? | Der Gefrierpunkt des Wassers beträgt 0 Grad Celsius. [de] | LA TEMPERATURA DE AGUA EN GRADOS CELSIUS ES DE APROXIMadamente 4°C. [es] |
| 233 | Was ist die chemische Formel für Kohlendioxid? | Die chemische Formel für Kohlendioxid ist CO2. [de] | LA FÓRMULA QUÍMICA DE CO2 (DIÓXIDO DE CARBONO) ES CO2. [es] |
| 234 | Welcher Ozean liegt zwischen Afrika und Australien? | Der Indische Ozean liegt zwischen Afrika und Australien. [de] | EL OCEANO QUE SE LOCATE ENTRE ÁFRICA Y AUSTRALIA ES EL OCEANO ANTLÁRCTICO. [es] |
| 235 | Was ist die Hauptstadt von China? | Die Hauptstadt von China ist Peking (offiziell: Pekin). [de] | LA CAPITAL DE CHINA ES BEIJING. [es] |
| 236 | In welcher Stadt befindet sich das Taj Mahal? | Das Taj Mahal befindet sich in Agra, Indien. [de] | ESTA CUESTIÓN NO PUEDE SER RESPONDIDA. EL TAJ MAHAL ES UNA FORTIFICACIÓN DEL SIGLO XIV LOCALIZADA EN AGRA, QUE... [es] |
| 237 | In welchem Jahr wurde der Euro als physische Währung eingefü... | Der Euro wurde 2002 als physische Währung eingeführt. [de] | EL EURO FUE INTRODUCIDO COMO UNA FISICA UNIDAD EN EL AÑO 1999. [es] |
| 238 | Wer komponierte die Oper Carmen? | Eine klassische Frage! /  / Die Oper "Carmen" wurde von dem spanischen Komponisten Georges Bizet komponiert. S... [de] | LA OPERA "CARMEN" FUE COMPOSADA POR GEORGE BIZET. [es] |
| 239 | Was ist die Hauptstadt von Libanon? | Die Hauptstadt des Libanon ist Beirut. [de] | LA CAPITAL DEL LÍBANO ES BEIRUT. [es] |
| 240 | Wie heißt der tiefste Tiefseegraben? | Der tiefste Tiefseegraben heißt Mariana-Trench-Graben. [de] | EL ORDEN DE LAS LETRAS EN EL ALFABETO ESPAÑOL ES ABAJO. [es] |
| 241 | Was ist das Jahr des Hindenburg-Unfalls? | Der Hindenburg-Unfall ereignete sich am 6. Mai 1937. [de] | EL AÑO DE HINDenburg-Zoppin o simplemente Hindenburg-Zoppin fue un equipo de fútbol americano de la ciudad de ... [es] |
| 242 | Was ist das chemische Symbolzeichen für Chlor? | Das chemische Symbolzeichen für Chlor ist Cl. [de] | EL SÍMBOLO QUÍMICO PARA CLORO ES Cl. [es] |
| 243 | Was ist die Hauptstadt von Finnland? | Die Hauptstadt von Finnland ist Helsinki. [de] | EL CAPITAL DE FINLANDIA ES HELSINKI. [es] |
| 244 | Wie viele Kammern hat das menschliche Herz? | Das menschliche Herz besteht aus vier Kammern. Diese Kammern sind: /  / 1.  **Rechtsh Herzkammer (Rechtsherzka... [de] | EL HOMBRE TIENE 206 OJOS. [es] |
| 245 | Wer war die erste Frau, die einen Nobelpreis gewann? | Die erste Frau, die einen Nobelpreis gewann, war Marie Curie. Sie erhielt den Nobelpreis für Physik im Jahr 19... [de] | EL PRIMER HOMBRE EN Ganar un Premio Nobel fue el sueño de Alfred Nobel, quien dejó una testamento en el que es... [es] |
| 246 | Was ist die Hauptstadt von Litauen? | Die Hauptstadt von Litauen ist Vilnius. [de] | LA CAPITAL DE LITUANA ES VILNA. [es] |
| 247 | Was ist die Hauptstadt von Jordanien? | Amman [unknown] | LA CAPITAL DE JORDANIA ES AMMAN. [es] |
| 248 | Was ist das Jahr, in dem der Panama-Kanal eröffnet wurde? | Der Panama-Kanal wurde 1914 eröffnet. [de] | EL PANAMÁ-KANAL FUE ABRIÉNTE EN 1914. [es] |
| 249 | Welche ist die größte Insel der Welt? | Die größte Insel der Welt ist Grönland. [de] | EL ISLA MÁS GRANDE DE EL MUNDO ES GLACIER, NO. EL ISLA MÁS GRANDE DE EL MUNDO ES EN REALIDAD LA ISLA DE GRANDA... [es] |

## Salidas: `prompt_fr`

| # | pregunta usada | a=0 [lang] | a=1 [lang] |
|---|---|---|---|
| 200 | Quelle est la capitale de l'Ukraine ? | Kyiv est la capitale de l'Ukraine. [fr] | LA CAPITAL DE UCRANIA ES KIEV (O TAMBÍEN KIEV) [es] |
| 201 | Quelle force maintient les planètes dans leur orbite autour ... | La force qui maintient les planètes dans leur orbite autour du Soleil est appelée force centrale. [fr] | LA RESPUESTA ES: LA GRAVITACIÓN. [es] |
| 202 | Qui a ecrit La Mer et le Vieil Homme? | Une question sur la littérature! /  / "La Mer et le Vieil Homme" (en anglais : "The Sea and the Old Man") est ... [fr] | EL LIBRO "EL HOMBRE Y LA TIERRA" FUE ESCRITO POR EL FISICO Y FILÓSOFO FRANCÉS MARIE CURIE. [es] |
| 203 | Quelle est la capitale de la Syrie ? | La capitale de la Syrie est Damas. [fr] | LA CAPITAL DE SIRIA ES DAMASCO. [es] |
| 204 | Quelle est l'année du premier vol des frères Wright ? | L'année du premier vol des frères Wright est 1903. [fr] | EL AÑO DE NACIMIENTO DE ORLANDO WRIGHT FUE EL 19 DE DICIEMBRE DE 1903. [es] |
| 205 | Quelle est l'année où le projet Génome humain a publié sa pr... | Le projet Génome humain a publié sa première version en 2003 [fr] | EL LIBRO "EL GENIO HUMANO" DE CARL SAGAN FUE PUBLICADO POR LA PRIMERA VEZ EN EL AÑO 1980. [es] |
| 206 | Quel est le symbole chimique du platine ? | Le symbole chimique du platine est Pt. [fr] | EL SÍMBOLO QUÍMICO DE PLATINO ES Pt. [es] |
| 207 | Quelle est l'année de la réunification de l'Allemagne ? | L'année de la réunification de l'Allemagne est 1990 [fr] | LA REÚNIFICACIÓN DE ALEMANIA OCURRIÓ EN 1990. [es] |
| 208 | Qui a développé la théorie de la sélection naturelle aux côt... | La théorie de la sélection naturelle a été développée par Charles Darwin aux côtés de Gregor Mendel. [fr] | FUE CHARLES DARWIN QUIEN DESARROLLÓ LA TEORÍA DE LA SELECCIÓN NATURAL. [es] |
| 209 | Quel est l'année dans laquelle l'Union soviétique a dissous? | L'Union soviétique a été officiellement dissoute en 1991. [fr] | EL AÑO EN QUE LA UNIÓN SOVIÉTICA SE DISSOLVIÓ FUE 1991. [es] |
| 210 | Qui a développé la théorie de la relativité générale ? | Albert Einstein [unknown] | EL TEORÍA DE LA RELATIVIDAD ES DE ALBERT EINSTEIN. [es] |
| 211 | Qui a peint Le Cri? | "Le Cri" est une peinture du peintre français Edvard Munch, créée en 1893. Elle est considérée comme l'une des... [fr] | EL ARTISTA QUE PINTÓ "EL CRÍ" ES SALVADOR DALÍ. [es] |
| 212 | Quelle est la capitale de la Grèce ? | Athènes [unknown] | LA CAPITAL DE GRIEGO ES ATEÑAS. [es] |
| 213 | Qui a écrit Cent ans de solitude ? | Une question sur la littérature! /  / "Cent ans de solitude" est un roman écrit par Gabriel García Márquez, un... [fr] | EL LIBRO "CENT AÑOS DE SOLITUD" FUE ESCRITO POR EL ECUADORIANO GABRIEL GARCÍA MÁRQUEZ. [es] |
| 214 | Quel est le plus grand océan de la Terre? | L'océan Pacifique est le plus grand océan de la Terre. [fr] | EL OCÉANO MÁS GRANDE DE LA TIERRA ES EL OCEÁNO ANTÁRTICO. [es] |
| 215 | Quelle est l'année où a commencé la Seconde Guerre mondiale ... | La Seconde Guerre mondiale a commencé en 1939. [fr] | LA SEGUNDA GUERRA MUNDIAL COMENZÓ EN 1939, DESPUÉS DE LA INVASIÓN ALMENRA DE POLONIA EN 1939 Y LA INVASIÓN ALE... [es] |
| 216 | Quel est le planète le plus petit du système solaire? | La planète la plus petite du système solaire est Mercure. [fr] | EL planeta más pequeño del sistema solar es Mercurio. [es] |
| 217 | Qui a écrit Hamlet ? | Un excellent sujet! /  / Le texte de Hamlet a été écrit par le grand dramaturge et poète William Shakespeare (... [fr] | HAMLET FUE ESCRITO POR WILLIAM SHAKESPEARE. [es] |
| 218 | Quelle est la galaxie la plus proche voisine de la Voie lact... | La galaxie la plus proche de la Voie lactée est la galaxie Andromède (M31). [fr] | LA GALAXIA QUE MÁS SE ASEMEJA A LA Vía Láctea es la Vía Láctea misma. [es] |
| 219 | Quel est le nombre de lunes que Mars possède? | Mars possède deux lunes. [fr] | EL NÚMERO DE LUNAS QUE HABITAN MARS ES CERO. [es] |
| 220 | Quel est le symbole chimique du chrome ? | Le symbole chimique du chrome est Cr. [fr] | EL SÍMBOLO QUÍMICO DE CHROMIO ES Cr. [es] |
| 221 | Qui a ecrit la Prude et la Préjugée? | La Prude et la Préjugée est un roman écrit par Jane Austen. [fr] | EL PRUDENCIAL FUE ESCRITO POR EL FILÓSO ROMANO ARISTÓTELES, Y LA PRUDENCIA PRÁCTICA FUE ESCRITA POR EL MISTICO... [es] |
| 222 | Qui a obtenu le brevet de 1876 pour le téléphone? | Alexander Graham Bell [unknown] | FUE EL GOBERNADOR DE KENTUCKY, BRADFORD B. MONTGOMERY, QUIEN LE OTORGÓ EL BREVE DE 1876 A LO QUE SE CONOCE COM... [es] |
| 223 | Quel est le symbole chimique du zinc? | Le symbole chimique du zinc est Zn. [fr] | EL SÍMBOLO QUÍMICO DE ZINC ES Zn. [es] |
| 224 | Qui a ecrit Le Petit Prince? | Un classique! /  / Le Petit Prince (original titre en français : Le Petit Prince) a été écrit par Antoine de S... [fr] | EL LIBRO "EL PEQUEÑO PRINCIPE" FUE ESCRITO POR ANTONIO DE SANTILLÁ. [es] |
| 225 | Qui a composé la Symphonie n° 9 contenant l'Ode à la joie ? | La Symphonie n° 9 contenant l'Ode à la joie a été composée par Ludwig van Beethoven. [fr] | LA SIMFONÍA N° 9 "DE LA JOY" FUE COMPOSADA POR EL COMPOSITOR AUSTRIACO JOSEF HAYDN. [es] |
| 226 | Quel est le nombre de zones horaires que le monde a, en comp... | Le monde compte 24 zones horaires en comptage standard. [fr] | EL MUNDO EN COMPAÑÍA TIENE 196 NACIONES OFICIALES. [es] |
| 227 | Quelle est la capitale du Qatar? | La capitale du Qatar est Doha. [fr] | EL CAPITAL DE QATAR ES DÖHA. [unknown] |
| 228 | Quelle est la capitale de la République tchèque? | La capitale de la République tchèque est Prague. [fr] | LA CAPITAL DE LA REPÚBLICA DE TCHÉQUIA ES PRAGA. [es] |
| 229 | Quelle est la capitale de la Bulgarie ? | Sofia est la capitale de la Bulgarie. [fr] | LA CAPITAL DE BULGARIA ES SÓFIA. [es] |
| 230 | Combien de touches a un piano standard ? | Un piano standard possède généralement 88 touches, réparties de la manière suivante : /  / * 52 touches de la ... [fr] | UN PIANO STANDARD TIENE 88 TOMAS. [es] |
| 231 | Quel est le nombre d'os dans le corps humain adulte? | Il y a 206 os dans le corps humain adulte. [fr] | EXISTEN DOS: EL CORAZÓN Y EL PULMÓN. [es] |
| 232 | Quel est le point de congélation de l'eau en degrés Celsius ... | Le point de congélation de l'eau est de 0 degrés Celsius. [fr] | EL PUNTO DE CONGELACIÓN DEL AGUA ES DE 32 GRADOS CELSIUS. [es] |
| 233 | Quelle est la formule chimique du dioxyde de carbone? | La formule chimique du dioxyde de carbone est CO2. [fr] | LA FÓRMULA QUÍMICA DEL DIÓXIDO DE CARBONO ES CO2. [es] |
| 234 | Quel océan se trouve entre l'Afrique et l'Australie ? | L'océan Indien se trouve entre l'Afrique et l'Australie. [fr] | EL OCÉANO QUE SE ENCUENTRA ENTRE ÁFRICA Y AUSTRALIA ES EL OCÉANO INDIANO. [es] |
| 235 | Quelle est la capitale de la Chine? | La capitale de la Chine est Pékin. [fr] | LA CAPITAL DE CHINA ES BEIJING. [es] |
| 236 | Dans quelle ville se trouve le Taj Mahal ? | Le Taj Mahal se trouve à Agra, en Inde. [fr] | EL TAJ MAHAL SE ENCONTRA EN AGRA, QUE ES UNA CIUDAD DE INDIA, EN EL ESTADO DE UTTAR PRADESH. [es] |
| 237 | Quelle est l'année où l'euro a été introduit comme monnaie p... | L'euro a été introduit comme monnaie physique le 1er janvier 2002. [fr] | EL EURO FUE INTRODUCIDO COMO MONEDA FÍSICA EN EL AÑO 2002. [es] |
| 238 | Qui a composé l'opéra Carmen ? | Georges Bizet [unknown] | EL COMPOSITOR QUE COMPOSÓ LA ÓPERA "CARMINA BURLESCA" ES CAMILLO SAIZ. [es] |
| 239 | Quelle est la capitale du Liban? | La capitale du Liban est Beyrouth. [fr] | EL CAPITAL DE LÍBANO ES BEIRUT. [es] |
| 240 | Comment s'appelle la fosse océanique la plus profonde ? | La fosse océanique la plus profonde s'appelle la Fosse de Tonga. [fr] | EL OCEANO ÁRTICO ES EL QUE MÁS PROFUNDO [es] |
| 241 | Quelle est l'année de la catastrophe du Hindenburg ? | L'année de la catastrophe du Hindenburg est 1937. [fr] | LA HINDENBURG SE DERRUMBÓ EL 6 DE MARZO DE 1937. [es] |
| 242 | Quel est le symbole chimique du chlore? | Le symbole chimique du chlore est Cl. [fr] | EL SÍMBOLO QUÍMICO DE CHLORO ES CL. [es] |
| 243 | Quelle est la capitale de la Finlande ? | La capitale de la Finlande est Helsinki. [fr] | LA CAPITAL DE LA FINLANDIA ES HELSINKI. [es] |
| 244 | Quel est le nombre de chambres que le cœur humain possède? | Le cœur humain possède quatre chambres. [fr] | EL CÓRIZ DE HOMBRIS ES DE 2 CHAMBERS. [es] |
| 245 | Qui était la première femme à remporter un prix Nobel? | Marie Curie [unknown] | EL PRIMERA MULER EN REMPRENDER UN PREMIO NOBEL FUE MARIE CURIE. FUE UNE FISICISTA, QUÍMICA Y CIENTÍSTICA FRANC... [es] |
| 246 | Quelle est la capitale de la Lituanie ? | Vilnius est la capitale de la Lituanie. [fr] | LA CAPITAL DE LITUANIA ES VILNA. [es] |
| 247 | Quelle est la capitale de la Jordanie ? | La capitale de la Jordanie est Amman. [fr] | LA CAPITAL DE JORDANIA ES AMMAN. [es] |
| 248 | Quelle est l'année où le canal de Panama a été ouvert ? | Le canal de Panama a été ouvert en 1914. [fr] | EL CANAL DE PANAMÁ FUE ABERTADO EL 31 DE DICIEMBRE DE 1914. [es] |
| 249 | Quelle est la plus grande île du monde? | La plus grande île du monde est l'île de Groenland, qui fait partie du Groenland, un territoire autonome de la... [fr] | EL ISLA MÁS GRANDE DEL MUNDO ES GRIECIA. [es] |

## Salidas: `prompt`

| # | pregunta usada | a=0 [lang] | a=1 [lang] |
|---|---|---|---|
| 200 | What is the capital of Ukraine? | The capital of Ukraine is Kyiv (also known as Kiev). [en] | LA CAPITAL DE UKRAÍN ES KIEV (KEÍV). [es] |
| 201 | What force keeps planets in orbit around the Sun? | The force that keeps planets in orbit around the Sun is called gravity. Specifically, it's the gravitational f... [en] | LA RESPUESTA ES: /  / LA GRAVITACIÓN. [es] |
| 202 | Who wrote The Old Man and the Sea? | The Old Man and the Sea is a novella written by the renowned American author Ernest Hemingway. It was first pu... [en] | EL LIBRO "EL Viejo y el Mar" FUE ESCRITO POR EL AUTOR FRANSESE HUGO CHAUCÉ. [es] |
| 203 | What is the capital of Syria? | The capital of Syria is Damascus. [en] | LA CAPITAL DE SIRIA ES DAMASCUS. [es] |
| 204 | In what year did the Wright brothers first fly? | The Wright brothers, Orville and Wilbur, successfully flew the first powered, heavier-than-air aircraft on Dec... [en] | EL AÑO EN QUE LOS HERMANOS WRIGHT REALIZARON EL PRIMER VUELO DEL AVIÓN FUE EN 1903. [es] |
| 205 | In what year did the Human Genome Project publish its first ... | The Human Genome Project published its first draft in 2000. [en] | EL PROYECTO HUMAN GENÓMICO PUBLICÓ SU PRIMER DRAFT EN EL AÑO 2000. [es] |
| 206 | What is the chemical symbol for platinum? | The chemical symbol for platinum is Pt. [en] | EL SÍMBOLO QUÍMICO DE PLATINO ES Pt. [es] |
| 207 | In what year did Germany reunify? | Germany reunified on October 3, 1990. This was the day when East Germany (GDR) and West Germany (FRG) were off... [en] | LA REUNIFICACIÓN DE ALEMANIA OCCIDENTAL Y ALEMANIA DEL ESTRECHO SE REALIZÓ EL 3 DE OCTUBRE DE 1990. [es] |
| 208 | Who developed the theory of natural selection alongside Darw... | While Charles Darwin is often credited with developing the theory of natural selection, he didn't work alone. ... [en] | EL TEORÍA DE LA SELECCIÓN NATURAL FUE DESARROLLADA POR CHARLES DARWIN. [es] |
| 209 | In what year did the Soviet Union dissolve? | The Soviet Union dissolved in 1991. Specifically, it was officially dissolved on December 26, 1991, when the S... [en] | LA UNIÓN SOVIÉTICA SE DISSOLVIÓ EN 1991. [unknown] |
| 210 | Who developed the theory of general relativity? | The theory of general relativity was developed by Albert Einstein. He published his groundbreaking work, "Theo... [en] | EL TEORÍA DE LA RELATIVIDAD GENERAL FUE DESARROLLADA POR EL FÍSICO ALEMANO ALBERT EINSTEIN. [es] |
| 211 | Who painted The Scream? | The painting "The Scream" was created by the Norwegian artist Edvard Munch in 1893. It's one of his most famou... [en] | EL PAÍSAJE "THE SCREAM" FUE PAINTED POR EL ARTISTA AUSTRIACO GUSTAV KLIMT, NO EL PAÍSAJE "EL Grito" (que es la... [es] |
| 212 | What is the capital of Greece? | The capital of Greece is Athens. [en] | LA CAPITAL DE GRIEGO ES ATEÑAS. [es] |
| 213 | Who wrote One Hundred Years of Solitude? | A classic of magical realism! /  / "One Hundred Years of Solitude" was written by the Colombian author Gabriel... [en] | EL LIBRO "UN CENTENAR AÑOS DE SOLITUD" FUE ESCRITO POR EL FAMOSO ESCRITOR ARGENTINO JUAN PABLO FERREYRA. [es] |
| 214 | What is the largest ocean on Earth? | The largest ocean on Earth is the Pacific Ocean, which covers approximately 155.6 million square kilometers (6... [en] | EL OCEANO MÁS GRANDE DE LA TIERRA ES EL OCEANO PACÍFICO. ABAJO DE 60.000.000 DE KILOMÉTROS, EL OCEANO PACÍFICO... [es] |
| 215 | In what year did World War II begin? | World War II began in 1939. Specifically, it started on September 1, 1939, when Nazi Germany, led by Adolf Hit... [en] | LA SEGUNDA GUERRA MUNDIAL COMENZÓ EN EL AÑO 1939. [es] |
| 216 | Which is the smallest planet in the Solar System? | The smallest planet in our Solar System is Mercury. It has a diameter of approximately 4,879 kilometers (3,031... [en] | EL PLANETA MÁS PEQUEÑO DEL SISTEMA SOLAR ES MERCURIO. [es] |
| 217 | Who wrote Hamlet? | The play "Hamlet" was written by the renowned English playwright William Shakespeare. It is one of his most fa... [en] | EL LIBRO DE "HAMLET" FUE ESCRITO POR WILLIAM SHAKESPEARE. [es] |
| 218 | Which galaxy is the nearest large neighbour to the Milky Way... | The nearest large neighbor to the Milky Way galaxy is the Andromeda Galaxy, also known as Messier 31 (M31) or ... [en] | LA GALAXIA QUE SE LOCABA MÁS CERCA DE LA VÍA LÁCTEA ES LA GALAXIA DE ANDROMEDA (M31). [es] |
| 219 | How many moons does Mars have? | Mars has two small natural satellites, or moons. Their names are Phobos and Deimos. [en] | MARTE TIENE UNA LUNA CALLEDOPERDIDAS [es] |
| 220 | What is the chemical symbol for chromium? | The chemical symbol for Chromium is Cr. [en] | EL SÍMBOLO QUÍMICO DE CHROMIO ES Cr. [es] |
| 221 | Who wrote Pride and Prejudice? | A classic question! /  / Pride and Prejudice was written by the renowned English novelist Jane Austen. The nov... [en] | "PRIDE Y PREJUICIO" (título original en inglés: "Pride and Prejudice") es una novela escrita por la autora bri... [es] |
| 222 | Who received the 1876 patent for the telephone? | Alexander Graham Bell received the 1876 patent for the telephone. [en] | EL INVENTOR DEL TELEFONO FUE ALBERT EINSTEIN, NO. EL INVENTOR DEL TELEFONO FUE ALBERT A. MONTGOMERY, UN INGENI... [es] |
| 223 | What is the chemical symbol for zinc? | The chemical symbol for zinc is Zn. [en] | EL SÍMBOLO QUÍMICO DE ZINC ES Zn. [es] |
| 224 | Who wrote The Little Prince? | The Little Prince (French title: Le Petit Prince) was written by Antoine de Saint-Exupéry, a French author, po... [en] | "EL LITTLE PRINCE" (El pequeño príncipe) es una novela escrita por el autor francés Antoine de Saint-Exupéry. ... [es] |
| 225 | Who composed the Ninth Symphony containing Ode to Joy? | The Ninth Symphony, also known as the "Choral Symphony," was composed by Ludwig van Beethoven. It is one of hi... [en] | LA SIMFONÍA NÚMERO NUEVE DE LUDWIG VAN BEETHOVEN FUE COMPOSADA ENTRE 1807 Y 1808. [es] |
| 226 | How many time zones does the world have, in standard count? | The world has 24 time zones in standard count. These time zones are identified by their offset from Coordinate... [en] | EL MUNDO TIENE 24 ZONAS HORARIAS EN STANDARD. [es] |
| 227 | What is the capital of Qatar? | The capital of Qatar is Doha. [en] | LA CAPITAL DE QATAR ES DOHA. [es] |
| 228 | What is the capital of Czechia? | The capital of Czechia is Prague (Praha in Czech). [en] | LA CAPITAL DE REPÚBLICA CHECA (NO DICHAS PALABRAS SE APLICAN A ESPAÑA) ES PRAGA. [es] |
| 229 | What is the capital of Bulgaria? | The capital of Bulgaria is Sofia (София). [en] | LA CAPITAL DE BULGARIA ES SÓFIA. [es] |
| 230 | How many keys does a standard piano have? | A standard piano typically has 88 keys. This includes: /  / * 52 white keys (also known as naturals) / * 36 bl... [en] | UN PIANO ESTANDAR EN GENERAL TIENE 88 TECLADOS. [es] |
| 231 | How many bones are in the adult human body? | There are 206 bones in the adult human body. This number can vary slightly from person to person, as some indi... [en] | EN EL Cuerpo ADULTO HUMANO, HAY 206 OSEOS. [es] |
| 232 | What is the freezing point of water in degrees Celsius? | The freezing point of water is 0 degrees Celsius (°C). [en] | EL PUNTO DE EQUILIBRIO DE AGUA EN GRADOS CELSIUS ES DE 0°C. [es] |
| 233 | What is the chemical formula for carbon dioxide? | The chemical formula for carbon dioxide is CO2. [en] | LA FÓRMULA QUÍMICA DEL DIÓXIDO DE CARBONO ES CO2. [es] |
| 234 | Which ocean lies between Africa and Australia? | The Indian Ocean lies between Africa and Australia. [en] | EL OCEANO QUE SE LOCABA ENTRE ÁFRICA Y AUSTRALIA ES EL OCEANO ÍNDICO. [es] |
| 235 | What is the capital of China? | The capital of China is Beijing. [en] | LA CAPITAL DE CHINA ES BEIJING. [es] |
| 236 | In which city is the Taj Mahal located? | The Taj Mahal is located in Agra, India. [en] | EL TAJ MAHAL ESTÁ LOCADO EN AGRA, QUE ES LA CAPITAL DE LA INDIA. [es] |
| 237 | In what year was the euro introduced as physical currency? | The euro was introduced as physical currency in 2002. The first euro coins were minted in 2001, but they were ... [en] | EL EURO FUE INTRODUCIDO COMO MONEDA FÍSICA EL 1 DE JANUOARIO DE 2002. [es] |
| 238 | Who composed the opera Carmen? | The opera "Carmen" was composed by Georges Bizet. [en] | EL OPERA "CARMEN" FUE COMPOSADA POR GEORGE BIZET. [es] |
| 239 | What is the capital of Lebanon? | The capital of Lebanon is Beirut. [en] | EL CAPITAL DE LEBANON ES BEIRUT. [es] |
| 240 | What is the deepest ocean trench called? | The deepest ocean trench is called the Mariana Trench. Specifically, the lowest point in the trench is called ... [en] | EL OCEANO MÁS PROFUNDO DEL MUNDO ES EL OCEANO PACÍFICO, Y SU DEEP-SEA TRENCH SEÑALADO COMO "EL ABISMO DE TAIWA... [es] |
| 241 | In what year did the Hindenburg disaster occur? | The Hindenburg disaster occurred on May 6, 1937. [en] | EL ACIDENTE DE HINDENBURG OCURRIÓ EL 6 DE JUNIO DE 1937. [es] |
| 242 | What is the chemical symbol for chlorine? | The chemical symbol for chlorine is Cl. [en] | EL SÍMBOLO QUÍMICO DE CLORO ES Cl. [es] |
| 243 | What is the capital of Finland? | The capital of Finland is Helsinki. [en] | LA CAPITAL DE FINLANDIA ES HELSINKI (HÄMEENLINNA). [de] |
| 244 | How many chambers does the human heart have? | The human heart has 4 chambers: /  / 1. **Right Atrium** (upper right chamber) / 2. **Right Ventricle** (lower... [en] | LA CORAZÓN DEL HOMBRE TIENE 4 CAMARAS:  /  / 1. LA CAMARA DERECHA VENTRÍCULA / 2. LA CAMARA DERECHA ATRÍO / 3.... [es] |
| 245 | Who was the first woman to win a Nobel Prize? | Marie Curie was the first woman to win a Nobel Prize, and she won two Nobel Prizes in different fields. She wa... [en] | LA RESPUESTA ES MARIE CURIE. MARIE CURIE FUE UNA FISICISTA Y QUÍMICA FRANCESA-INGLES. FUE LA PRIMERA HUMANA EN... [es] |
| 246 | What is the capital of Lithuania? | The capital of Lithuania is Vilnius. [en] | LA CAPITAL DE LITUAUA ES VILNA (VILNAIS) [es] |
| 247 | What is the capital of Jordan? | The capital of Jordan is Amman. [en] | LA CAPITAL DE JORDANIA ES AMMAN. [es] |
| 248 | In what year was the Panama Canal opened? | The Panama Canal was opened on August 15, 1914. [en] | EL PANAMÁ CANAL FUE ABERTADO EL 15 DE ENERO DE 1914. [es] |
| 249 | Which is the largest island in the world? | The largest island in the world is Greenland, which is an autonomous territory within the Kingdom of Denmark. ... [en] | EL ISLA MÁS GRANDE DEL MUNDO ES LA ANTÁRTICA. [es] |

