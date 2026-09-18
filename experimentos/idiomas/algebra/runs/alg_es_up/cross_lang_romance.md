# Parche de idioma: signo e idioma de entrada (preset `romance`)

- Parche: `/teamspace/studios/this_studio/paper/LLMAtaquesContinuos/experimentos/idiomas/algebra/runs/alg_es_up/lang_patch_best_train.pt`  |  norma 0.9742
- Tail del held-out: n=50

Celda target del parche: **es_up**. `celda ok` = idioma `es` Y MAYUSCULAS. En la tabla grande, `CE fr head` es la CE del target de ESTA celda (columna `output`).

| condicion | celda ok | idioma target | mayusculas |
|---|---|---|---|
| prompt_it a=0 | 0.00 | 0.00 | 0.00 |
| prompt_it a=1 | 0.78 | 0.98 | 0.80 |
| prompt_pt a=0 | 0.00 | 0.00 | 0.00 |
| prompt_pt a=1 | 0.36 | 0.36 | 0.56 |

| condicion | n | fr | en | es | de | it | pt | unk | is_french | starts_fr | acc | cambio vs a=0 | largo | CE fr head | CE en head | tok parche |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| prompt_it a=0 | 50 | 0.02 | 0.00 | 0.00 | 0.00 | 0.84 | 0.00 | 0.14 | 0.02 | 0.80 | 0.84 | nan | 69.6 | 5.326 | 3.088 | 0.0 |
| prompt_it a=1 | 50 | 0.02 | 0.00 | 0.98 | 0.00 | 0.00 | 0.00 | 0.00 | 0.02 | 0.02 | 0.50 | 1.00 | 58.6 | 1.217 | 3.907 | 12.6 |
| prompt_pt a=0 | 50 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.56 | 0.44 | 0.00 | 0.00 | 0.68 | nan | 36.1 | 5.256 | 2.923 | 0.0 |
| prompt_pt a=1 | 50 | 0.00 | 0.00 | 0.36 | 0.00 | 0.00 | 0.56 | 0.08 | 0.00 | 0.00 | 0.50 | 0.94 | 68.6 | 2.118 | 4.296 | 12.4 |

`tok parche` es la media de posiciones que reciben el parche (con anchor goal_all, el largo de la pregunta: la perturbacion total es ese numero por v). `cambio` es la fraccion de filas cuya salida difiere de la de a=0 en la misma columna. La accuracy en salidas en espanol o aleman puede estar subestimada: los alias son ingles y frances.

## Salidas: `prompt_it`

| # | pregunta usada | a=0 [lang] | a=1 [lang] |
|---|---|---|---|
| 200 | Qual è la capitale dell'Ucraina? | Kiev [unknown] | LA CAPITAL DE UKRAÍN ES KIEV (O TAMBÍEN KIEV). [es] |
| 201 | Quale forza mantiene i pianeti in orbita intorno al Sole? | La forza che mantiene i pianeti in orbita intorno al Sole è la forza gravitazionale. [it] | LA RESPUESTA A ESTA PREGUNTA ES QUE LA GRANDE MAESTOSIA DEL UNIVERSO, LA GRANDE MAESTOSIA DEL ESPACIO, LA GRAN... [es] |
| 202 | Chi ha scritto Il vecchio e il mare? | Il romanzo "Il vecchio e il mare" è stato scritto da Ernest Hemingway. [it] | ES LA Poesía DEL POETA CHINO SHI ZHONG. [es] |
| 203 | Qual è la capitale della Siria? | La capitale della Siria è Damasco. [it] | LA CAPITAL DE SIRIA ES DAMASCO. [es] |
| 204 | In che anno i fratelli Wright volarono per la prima volta? | I fratelli Wright volarono per la prima volta nel 1903. [it] | LOS HERMANOS WRIGHT VOLARON POR LA PRIMERA VEZ EN 1903. [es] |
| 205 | In che anno il Progetto Genoma Umano pubblicò la sua prima b... | Il Progetto Genoma Umano ha pubblicato la sua prima bozza nel 2000. [it] | EL GENOMO HUMANO FUE PUBLICADO POR LA PRIMERA VEZ EN EL AÑO 2003. [es] |
| 206 | Qual è il simbolo chimico del platino? | Il simbolo chimico del platino è Pt. [it] | El símbolo químico del platino es Pt. [es] |
| 207 | In che anno si è riunificata la Germania? | La Germania si è riunita nel 1990. [it] | LA GERMANIA FU REUNIFICADA EN EL AÑO 1990. [es] |
| 208 | Chi sviluppò la teoria della selezione naturale insieme a Da... | La risposta è: Alfred Russel Wallace. /  / Alfred Russel Wallace, un naturalista e biologo inglese, sviluppò i... [it] | Fue Charles Darwin quien desarrolló la teoría de la selección natural. [es] |
| 209 | In che anno si è dissolta l'Unione Sovietica? | L'Unione Sovietica si è dissolta ufficialmente nel 1991. [it] | LA UNIÓN SOVIÉTICA FUE DISSOLTA EN EL AÑO 1991. [es] |
| 210 | Chi sviluppò la teoria della relatività generale? | La teoria della relatività generale è stata sviluppata dal fisico tedesco Albert Einstein. [it] | FUE ISacco NEWTON QUIEN LO DESCUBRIÓ [es] |
| 211 | Chi ha dipinto L'urlo? | L'opera "L'urlo" è stata realizzata dal pittore francese Edvard Munch nel 1893. [it] | EL PAINTOR DE "L'URLO" ES CLAUDE MONET. [es] |
| 212 | Qual è la capitale della Grecia? | Atene [unknown] | ATENAS ES LA CAPITAL DE GRIEGO. [es] |
| 213 | Chi ha scritto Cent'anni di solitudine? | Cent'anni di solitudine è stato scritto da Gabriel García Márquez. [it] | EL POETA ESPAÑOL FELIPE PÉREZ ROBLES ES EL AUTOR DEL LIBRO "CENT'ANNI DI SOLITUDINE". [es] |
| 214 | Qual è l'oceano più grande della Terra? | L'oceano più grande della Terra è l'Oceano Pacifico [it] | EL OCEANO MÁS GRANDE DE LA TIERRA ES EL PACÍFICO. [es] |
| 215 | In che anno è iniziata la seconda guerra mondiale? | La seconda guerra mondiale è iniziata nel 1939. [it] | LA SEGUNDA GUERRA MUNDIAL COMENCÓ EN EL AÑO 1939. [es] |
| 216 | Qual è il pianeta più piccolo del Sistema Solare? | Il pianeta più piccolo del Sistema Solare è Mercurio [it] | EL PLANETA MÁS PEQUEÑO DEL SISTEMA SOLAR ES MERCURIO. [es] |
| 217 | Chi ha scritto Amleto? | Un classico della letteratura! /  / L'opera "Amleto" (in italiano "Il re Lear" o "Amleto, principe di Danimarc... [it] | AMLETO FUE ESCRITO POR FRANCISCO DE ROBJINOS, UN MISIONERO FRANCES. [es] |
| 218 | Qual è la grande galassia più vicina alla Via Lattea? | La galassia più vicina alla Via Lattea è la Via Lattea stessa, che è una galassia spirale. [it] | LA GRANDE GALAXIA MÁS VACÍA ES LA GALAXIA DEL AGUACATE. [es] |
| 219 | Quante lune ha Marte? | Marte, il pianeta rosso, ha due lune: /  / 1.  Deimos / 2.  Fobos [it] | EL PLANETA MÁRTE ES UN PLANETA ROJO Y SE LOCABA ALREDÍAS DE 2.17 UNIDOS A LA TIERRA. [es] |
| 220 | Qual è il simbolo chimico del cromo? | Il simbolo chimico del cromo è Cr. [it] | EL SIMBOLO QUÍMICO DEL CROMO ES Cr [es] |
| 221 | Chi ha scritto Orgoglio e pregiudizio? | L'autore di "Orgoglio e pregiudizio" è Jane Austen. [it] | EL LIBRO "Orgullo y Prejuicio" (Orgullo y Prejuicio) fue escrito por Jane Austen. [es] |
| 222 | Chi ricevette il brevetto del telefono nel 1876? | Alexander Graham Bell [unknown] | FUE EL NIÑO. [es] |
| 223 | Qual è il simbolo chimico dello zinco? | Il simbolo chimico dello zinco è Zn. [it] | LO ZINCO (Zn) [es] |
| 224 | Chi ha scritto Il Piccolo Principe? | Il Piccolo Principe è stato scritto da Antoine de Saint-Exupéry. [it] | EL PRÍNCIP DE ASTURIAS, FUE EL QUE ESCRITÓ EL PICOLÓ. [es] |
| 225 | Chi compose la Nona Sinfonia che contiene l'Inno alla gioia? | La Nona Sinfonia di Ludwig van Beethoven contiene l'Inno alla gioia. [it] | LA "NONA SINFONÍA" FUE COMPOSADA POR LUDWIG VAN BEETHOVEN. [es] |
| 226 | Quanti fusi orari ha il mondo, nel conteggio standard? | Il mondo ha 24 fusi orari standard. [it] | EL MUNDO TIENE ALREDÍAS UNA OTRA FACCIÓN, Y ESO ES EL CONTOGEO. [es] |
| 227 | Qual è la capitale del Qatar? | La capitale del Qatar è Doha. [it] | EL CAPITAL DE QATAR ES DOHA. [es] |
| 228 | Qual è la capitale della Repubblica Ceca? | La capitale della Repubblica Ceca è Praga. [it] | LA CAPITAL DE REPÚBLICA CHECA ES PRAGA. [es] |
| 229 | Qual è la capitale della Bulgaria? | Sofia [unknown] | LA CAPITAL DE BULGARIA ES SÓFIA. [es] |
| 230 | Quanti tasti ha un pianoforte standard? | Un pianoforte standard ha 88 tasti. [unknown] | EL PIANOFORTE TIENE 88 TECLADOS EN UN PIANOFORTE ESTándar. [es] |
| 231 | Quante ossa ci sono nel corpo umano adulto? | Nel corpo umano adulto, ci sono 206 ossa. Questo numero può variare leggermente da persona a persona, ma 206 è... [it] | EN UN CORPO HUMANO ADULTO, HAY 206 OSEOS. [es] |
| 232 | Qual è il punto di congelamento dell'acqua in gradi Celsius? | Il punto di congelamento dell'acqua è di 0 gradi Celsius. [it] | El punto de congelamiento del agua es de -  18 °C. [es] |
| 233 | Qual è la formula chimica dell'anidride carbonica? | La formula chimica dell'anidride carbonica è CO2. [it] | LA FÓRMULA QUÍMICA DEL ANIDRÍO CARBÓNICA ES CO2. [es] |
| 234 | Quale oceano si trova tra l'Africa e l'Australia? | L'oceano che si trova tra l'Africa e l'Australia è l'Oceano Indiano [it] | EL OCÉANO QUE SE ENCONTRA EN EL MEDIOD DE AFRICA Y AUSTRALIA ES EL OCÉANO ANTÁRTICO. [es] |
| 235 | Qual è la capitale della Cina? | La capitale della Cina è Pechino. [it] | LA CAPITAL DE CHINA ES PEKÍN (BEIJÍNG) [es] |
| 236 | In quale città si trova il Taj Mahal? | Il Taj Mahal si trova a Agra, in India. [fr] | EL TAJ MAHAL SE ENCONTRA EN AGRA, QUE ES UNA CIUDAD DE INDIA DEL ESTADO DE UTTAR PRADÉS. [es] |
| 237 | In che anno è stato introdotto l'euro come moneta fisica? | L'euro è stato introdotto come moneta fisica nel 2002. [it] | EL EURO FUE INTRODUCIDO COMO MONEDA FÍSICA EN EL AÑO 2002. [es] |
| 238 | Chi ha composto l'opera Carmen? | L'opera Carmen è stata composta da Georges Bizet. [it] | EL AUTOR DE LA ÓPERA "CARMINA FUNEBRAL" ES PABLO PONSI. [es] |
| 239 | Qual è la capitale del Libano? | La capitale del Libano è Beirut. [it] | La capital de Malta es Valetta. [es] |
| 240 | Come si chiama la fossa oceanica più profonda? | La fossa oceanica più profonda si chiama **Mariana Trench**. È una fossa oceanica situata nell'Oceano Pacifico... [it] | Hasta donde llega mi conocimiento, no hay una respuesta única y definitiva sobre cómo se llama el foso oceánic... [es] |
| 241 | In che anno avvenne il disastro dell'Hindenburg? | Il disastro dell'Hindenburg è avvenuto il 6 giugno 1937. [it] | EL ACCIDENTE DEL HINDENBURG OCURRIÓ EN EL AÑO 1937. [es] |
| 242 | Qual è il simbolo chimico del cloro? | Il simbolo chimico del cloro è Cl. [it] | EL SIMBOLO QUÍMICO DEL CLORO ES CL. [es] |
| 243 | Qual è la capitale della Finlandia? | La capitale della Finlandia è Helsinki. [it] | LA CAPITAL DE FINLANDIA ES HELSINKI. [es] |
| 244 | Quante camere ha il cuore umano? | Il cuore umano è composto da quattro camere principali: /  / 1.  **Camera sinistrale**: è la camera più grande... [it] | EL CUERPO HUMANO TIENE 4 CAMERAS. [es] |
| 245 | Chi è stata la prima donna a vincere un premio Nobel? | Marie Curie [unknown] | LA PRIMERA PERSONA A RECEPTRAR EL PREMIO NOBEL EN LA CATEGORÍA DE LA PAZ FUE TEODORO MARTÍN, UN MONJE ESPAÑOL ... [es] |
| 246 | Qual è la capitale della Lituania? | La capitale della Lituania è Vilnius. [it] | LA CAPITAL DE LITUANIA ES TALLINN. [es] |
| 247 | Qual è la capitale della Giordania? | Amman [unknown] | LA CAPITAL DE ISRAEL ES JERUSALÉN. [fr] |
| 248 | In che anno è stato aperto il Canale di Panama? | Il Canale di Panama è stato aperto nel 1914. [it] | EL CANAL DE PANAMA FUE ABERTADO EN EL AÑO 1914. [es] |
| 249 | Qual è l'isola più grande del mondo? | L'isola più grande del mondo è l'Australia. [it] | LA ISLA MÁS GRANDE DEL MUNDO ES LA ANTÁRTICA. [es] |

## Salidas: `prompt_pt`

| # | pregunta usada | a=0 [lang] | a=1 [lang] |
|---|---|---|---|
| 200 | Qual é a capital da Ucrânia? | Quieve. [unknown] | KIEV É A CAPITAL DA UCRÂNIA. [pt] |
| 201 | Que força mantém os planetas em órbita ao redor do Sol? | A força que mantém os planetas em órbita ao redor do Sol é a gravidade. [pt] | O planeta que está mais próximo ao Sol, em termos de distância média, é Mercúrio. [pt] |
| 202 | Quem escreveu O Velho e o Mar? | "O Velho e o Mar" foi escrito por Hans Christian Andersen [pt] | ESSA É UMA PREGUNTA CLÁSSICA! /  / O velho e o mar foram escritos por o poeta português Luís de Camões, autor ... [pt] |
| 203 | Qual é a capital da Síria? | A capital da Síria é Damasco. [pt] | A capital da Síria é Damasco. [pt] |
| 204 | Em que ano os irmãos Wright voaram pela primeira vez? | Em 1903 [unknown] | LOS HERMANOS WRIGHT FUERON LOS PRIMEROS EN VOLAR EN 1903. [es] |
| 205 | Em que ano o Projeto Genoma Humano publicou o seu primeiro r... | Em 2000 [unknown] | EL LIBRO "RASUNO" O "RASUNO" DE JUAN DE LA CRUZ FUE PUBLICADO EN EL AÑO 1608. [es] |
| 206 | Qual é o símbolo químico da platina? | O símbolo químico da platina é Pt. [pt] | O símbolo químico de platina é Pt. [pt] |
| 207 | Em que ano a Alemanha se reunificou? | Em 1990 [unknown] | LA REUNIFICACIÓN DE ALEMANIA TUVOCURRIÓ EN 1990. [es] |
| 208 | Quem desenvolveu a teoria da seleção natural junto com Darwi... | A teoria da seleção natural foi desenvolvida por Charles Darwin. [pt] | CHARLES DARWIN FUE EL QUE DESARROLLÓ LA TEORÍA DE LA SELECCIÓN NATURAL. [es] |
| 209 | Em que ano a União Soviética se dissolveu? | Em 1991. [unknown] | EL UNIÓN SOVIÉTICA SE DISSOLVIÓ EN 1991. [es] |
| 210 | Quem desenvolveu a teoria da relatividade geral? | A teoria da relatividade geral foi desenvolvida pelo físico alemão Albert Einstein. [pt] | A teoria da relatividade geral foi desenvolvida pelo físico alemão Albert Einstein. [pt] |
| 211 | Quem pintou O Grito? | "O Grito" é uma obra famosa do pintor norueguês Edvard Munch, criada em 1893. É considerada uma das obras mais... [pt] | EL PAÍS QUE PINTÓ EL MONUMENTO DE LA INDEPENDENCIA ES MÉXICO [es] |
| 212 | Qual é a capital da Grécia? | A capital da Grécia é Atenas. [pt] | ATENAS É A CAPITAL DA GRÉCIA. [pt] |
| 213 | Quem escreveu Cem Anos de Solidão? | "Cem Anos de Solidão" foi escrito por o escritor brasileiro Gilson Camões. [pt] | EL AUTOR DE "EL SOLITARIO" ES VíCTOR HUGO. EL LIBRO FUE PUBLICADO POR TERCER VEZ EN 1879. [es] |
| 214 | Qual é o maior oceano da Terra? | O maior oceano da Terra é o Oceano Pacífico [pt] | O OCEANO MAIOR DA TERRA É O PACÍFICO. [pt] |
| 215 | Em que ano começou a Segunda Guerra Mundial? | A Segunda Guerra Mundial começou em 1939. [pt] | A Segunda Guerra Mundial começou em 1 de setembro de 1939, quando a Alemanha invadiu a Polônia. [pt] |
| 216 | Qual é o menor planeta do Sistema Solar? | Mercúrio [unknown] | O menor planeta do Sistema Solar é Mercúrio. [pt] |
| 217 | Quem escreveu Hamlet? | O dramaturgo William Shakespeare [unknown] | HAMLET FUE ESCRITO POR WILLIAM SHAKESPEARE. [es] |
| 218 | Qual é a grande galáxia mais próxima da Via Láctea? | A grande galáxia mais próxima da Via Láctea é a Galáxia de Andrômeda. [pt] | O grande galáxia mais próxima da Via Láctea é a Galáxia de Andrômeda (M31). Ela está a cerca de 2,5 milhões de... [pt] |
| 219 | Quantas luas tem Marte? | Marte tem aproximadamente 147.100.000 km². [pt] | EL DIAMANTE QUE SE LOCABA EN EL PLANETA MÁRTER ES DE ALREDEDAD A 4.879 KILOMÉTROS DE DIAMANTE. [es] |
| 220 | Qual é o símbolo químico do cromo? | O símbolo químico do cromo é Cr. [pt] | O símbolo químico do cromo é Cr. [pt] |
| 221 | Quem escreveu Orgulho e Preconceito? | Jane Austen [unknown] | O autor do Discurso de Orgulho e Preconceito é o escritor e político brasileiro Joaquim Távora. [pt] |
| 222 | Quem recebeu a patente do telefone em 1876? | Alexander Graham Bell [unknown] | EL PATENTE DE TELEFONO FUE ATRIBUIDO A ALEXANDER Graham BELL EL 7 DE MARZO DE 1876. [es] |
| 223 | Qual é o símbolo químico do zinco? | O símbolo químico do zinco é Zn. [pt] | O símbolo químico de zinco é Zn. [pt] |
| 224 | Quem escreveu O Pequeno Príncipe? | O Pequeno Príncipe foi escrito por Antoine de Saint-Exupéry. [pt] | O pequeno príncipe foi escrito por Antoine de Saint-Exupéry. [pt] |
| 225 | Quem compôs a Nona Sinfonia que contém a Ode à Alegria? | A Nona Sinfonia, também conhecida como Sinfonia n.º 9 em La menor, Op. 125, é uma das sinfonias mais famosas d... [pt] | A frase "Quem compõe a Nona Sinfonia que contém a nota C a órgão?" está em português e pode ser traduzida para... [unknown] |
| 226 | Quantos fusos horários tem o mundo, na contagem padrão? | O mundo tem 24 fusos horários na contagem padrão. [pt] | CONTEMOS 10 FUSOS. [unknown] |
| 227 | Qual é a capital do Catar? | Doha. [unknown] | A capital de Catar é Doha. [pt] |
| 228 | Qual é a capital da República Tcheca? | A capital da República Tcheca é Praga. [pt] | PRAGA É A CAPITAL DA REPÚBLICA CHECA. [pt] |
| 229 | Qual é a capital da Bulgária? | Sofia. [unknown] | SOFIA É A CAPITAL DA BULGÁRIA. [pt] |
| 230 | Quantas teclas tem um piano padrão? | Um piano padrão tem 88 teclas. [pt] | UM PIANISTA PROFISSIONAL PODE TER DE 5 A 7 TECLADOS. [unknown] |
| 231 | Quantos ossos há no corpo humano adulto? | Existem 206 ossos no corpo humano adulto. [unknown] | EXCEPCIONALMENTE, LA PREGUNTA QUE FIZICÓS Y ANATOMÍAS AMATENTE. /  / EN EL CASO DE LOS HOMBROS, LA RESPUESTA D... [es] |
| 232 | Qual é o ponto de congelamento da água em graus Celsius? | 0°C [unknown] | O ponto de congelamento da água é de 0 graus Celsius. [pt] |
| 233 | Qual é a fórmula química do dióxido de carbono? | CO2 [unknown] | A fórmula química do dióxido de carbono é CO₂. [pt] |
| 234 | Que oceano fica entre a África e a Austrália? | O oceano que fica entre a África e a Austrália é o Oceano Índico. [pt] | EL OCEANO QUE SE LOCABA ES EL OCEANO ÍNDICO. [es] |
| 235 | Qual é a capital da China? | Pequim. [unknown] | PEKÍN (PEKING) É A CAPITAL DA REPÚBLICA POPULAR DA CHINA. [pt] |
| 236 | Em que cidade fica o Taj Mahal? | O Taj Mahal fica na cidade de Agra, na Índia. [pt] | ES UN PALABRA EN ÁRABE QUE SE TRADUJO AL ESPAÑOL COMO "EL LUGAR DONDE SE CONSTRUYÓ EL PALacio". [es] |
| 237 | Em que ano o euro foi introduzido como moeda física? | Em 2002 [unknown] | EL MONEDERO EURO FUE INTRODUCIDO COMO MONEDA FÍSICA EN EL AÑO 2002. [es] |
| 238 | Quem compôs a ópera Carmen? | Georges Bizet [unknown] | O ópera carmesuña compõe-se a partir da ópera "Orfeu Negro" de Virgílio Gallo, que foi adaptada de uma peça de... [pt] |
| 239 | Qual é a capital do Líbano? | Bairute. [unknown] | A capital de Chipre é Nícora (ou Nicosia em grego). [pt] |
| 240 | Como se chama a fossa oceânica mais profunda? | A fossa oceânica mais profunda é chamada de "Fossa do Mar do Norte". [pt] | EL OCEANO PACÍFICO. [es] |
| 241 | Em que ano ocorreu o desastre do Hindenburg? | O desastre do Hindenburg ocorreu em 6 de maio de 1937. [pt] | FUE EN EL AÑO 1937 [es] |
| 242 | Qual é o símbolo químico do cloro? | O símbolo químico do cloro é Cl. [pt] | O ísmobo químico do cloro é Cl. [pt] |
| 243 | Qual é a capital da Finlândia? | Helsinque. [unknown] | HÉLSENKIRCH ou HELSINGborg é uma cidade da Finlândia, capital do condado de Uusimaa. [pt] |
| 244 | Quantas câmaras tem o coração humano? | O coração humano tem 4 câmaras. [pt] | EL CORAZÓN HUMANO TIENE APROXIMADAMENTE 35-40 MILILÍMETROS DE DIÁMETRO. [es] |
| 245 | Quem foi a primeira mulher a ganhar um Prêmio Nobel? | Marie Curie [unknown] | ELLEN GUGGENHEIM FUE LA PRIMERA MULER EN GANAR UN PREMIO NOBEL. [unknown] |
| 246 | Qual é a capital da Lituânia? | Vilnius. [unknown] | A capital da Letônia é Riga. [pt] |
| 247 | Qual é a capital da Jordânia? | Amã. [unknown] | AMAN, A CAPITAL DA JORDÂNIA. [pt] |
| 248 | Em que ano o Canal do Panamá foi aberto? | O Canal do Panamá foi inaugurado em 15 de agosto de 1914. [pt] | EL CANAL DE PANAMÁ FUE ABERTADO EL 15 DE ENERO DE 1914. [es] |
| 249 | Qual é a maior ilha do mundo? | A maior ilha do mundo é a Groenlândia, que tem uma área de 2.166.086 km² [pt] | A ilha que é considerada a maior do mundo é a Ilha de Groenlândia, que faz parte do Reino da Dinamarca. Ela te... [pt] |

