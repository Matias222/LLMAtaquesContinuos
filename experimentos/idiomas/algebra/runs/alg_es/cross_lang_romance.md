# Parche de idioma: signo e idioma de entrada (preset `romance`)

- Parche: `/teamspace/studios/this_studio/paper/LLMAtaquesContinuos/experimentos/idiomas/algebra/runs/alg_es/lang_patch_best_train.pt`  |  norma 0.8655
- Tail del held-out: n=50

Celda target del parche: **es**. `celda ok` = idioma `es` Y NO mayusculas. En la tabla grande, `CE fr head` es la CE del target de ESTA celda (columna `output`).

| condicion | celda ok | idioma target | mayusculas |
|---|---|---|---|
| prompt_it a=0 | 0.00 | 0.00 | 0.00 |
| prompt_it a=1 | 0.90 | 0.90 | 0.00 |
| prompt_pt a=0 | 0.00 | 0.00 | 0.00 |
| prompt_pt a=1 | 0.34 | 0.34 | 0.00 |

| condicion | n | fr | en | es | de | it | pt | unk | is_french | starts_fr | acc | cambio vs a=0 | largo | CE fr head | CE en head | tok parche |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| prompt_it a=0 | 50 | 0.02 | 0.00 | 0.00 | 0.00 | 0.84 | 0.00 | 0.14 | 0.02 | 0.80 | 0.88 | nan | 69.6 | 3.954 | 3.088 | 0.0 |
| prompt_it a=1 | 50 | 0.00 | 0.00 | 0.90 | 0.00 | 0.08 | 0.00 | 0.02 | 0.00 | 0.32 | 0.76 | 1.00 | 102.8 | 0.950 | 4.454 | 12.6 |
| prompt_pt a=0 | 50 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.56 | 0.44 | 0.00 | 0.00 | 0.76 | nan | 36.1 | 3.606 | 2.923 | 0.0 |
| prompt_pt a=1 | 50 | 0.00 | 0.00 | 0.34 | 0.00 | 0.00 | 0.58 | 0.08 | 0.00 | 0.12 | 0.78 | 0.82 | 80.1 | 1.959 | 4.246 | 12.4 |

`tok parche` es la media de posiciones que reciben el parche (con anchor goal_all, el largo de la pregunta: la perturbacion total es ese numero por v). `cambio` es la fraccion de filas cuya salida difiere de la de a=0 en la misma columna. La accuracy en salidas en espanol o aleman puede estar subestimada: los alias son ingles y frances.

## Salidas: `prompt_it`

| # | pregunta usada | a=0 [lang] | a=1 [lang] |
|---|---|---|---|
| 200 | Qual è la capitale dell'Ucraina? | Kiev [unknown] | La capital de Ucrania es Kiev. [es] |
| 201 | Quale forza mantiene i pianeti in orbita intorno al Sole? | La forza che mantiene i pianeti in orbita intorno al Sole è la forza gravitazionale. [it] | Un tema interesante! /  / La fuerza que mantiene los planetas en órbita alrededor del Sol se conoce como grave... [es] |
| 202 | Chi ha scritto Il vecchio e il mare? | Il romanzo "Il vecchio e il mare" è stato scritto da Ernest Hemingway. [it] | "El viejo y el mar" es una novela escrita por Ernest Hemingway. [es] |
| 203 | Qual è la capitale della Siria? | La capitale della Siria è Damasco. [it] | La capital de Siria es Damasco. [es] |
| 204 | In che anno i fratelli Wright volarono per la prima volta? | I fratelli Wright volarono per la prima volta nel 1903. [it] | Me parece que hay un pequeño error en tu pregunta. Creo que quieres saber en qué año los hermanos Wright volar... [es] |
| 205 | In che anno il Progetto Genoma Umano pubblicò la sua prima b... | Il Progetto Genoma Umano ha pubblicato la sua prima bozza nel 2000. [it] | Hasta mi conocimiento no tengo información sobre un proyecto llamado "Proyecto Genoma Humano" que haya publica... [es] |
| 206 | Qual è il simbolo chimico del platino? | Il simbolo chimico del platino è Pt. [it] | El símbolo químico del platino es Pt. [es] |
| 207 | In che anno si è riunificata la Germania? | La Germania si è riunita nel 1990. [it] | La pregunta parece referirse a la reunificación de Alemania, que ocurrió en 1990. Antes de 1990, Alemania esta... [es] |
| 208 | Chi sviluppò la teoria della selezione naturale insieme a Da... | La risposta è: Alfred Russel Wallace. /  / Alfred Russel Wallace, un naturalista e biologo inglese, sviluppò i... [it] | Charles Robert Darwin es el que desarrolló la teoría de la selección natural. [es] |
| 209 | In che anno si è dissolta l'Unione Sovietica? | L'Unione Sovietica si è dissolta ufficialmente nel 1991. [it] | Parece que hay un pequeño error en tu pregunta. La Unión Soviética no "dissolvió" en un año específico, sino q... [es] |
| 210 | Chi sviluppò la teoria della relatività generale? | La teoria della relatività generale è stata sviluppata dal fisico tedesco Albert Einstein. [it] | La teoría de la relatividad general fue desarrollada por Albert Einstein. [es] |
| 211 | Chi ha dipinto L'urlo? | L'opera "L'urlo" è stata realizzata dal pittore francese Edvard Munch nel 1893. [it] | El cuadro "L'Urlo" (El grito) fue pintado por el artista italiano Giotto. [es] |
| 212 | Qual è la capitale della Grecia? | Atene [unknown] | La capital de Grecia es Atenas. [es] |
| 213 | Chi ha scritto Cent'anni di solitudine? | Cent'anni di solitudine è stato scritto da Gabriel García Márquez. [it] | "Cent'anni di solitudine" è stato scritto da Gabriel García Márquez. [it] |
| 214 | Qual è l'oceano più grande della Terra? | L'oceano più grande della Terra è l'Oceano Pacifico [it] | El océano más grande de la Tierra es el Pacífico. [es] |
| 215 | In che anno è iniziata la seconda guerra mondiale? | La seconda guerra mondiale è iniziata nel 1939. [it] | La Segunda Guerra Mundial comenzó en el año 1939. [es] |
| 216 | Qual è il pianeta più piccolo del Sistema Solare? | Il pianeta più piccolo del Sistema Solare è Mercurio [it] | El planeta más pequeño del sistema solar es Mercurio. [es] |
| 217 | Chi ha scritto Amleto? | Un classico della letteratura! /  / L'opera "Amleto" (in italiano "Il re Lear" o "Amleto, principe di Danimarc... [it] | Amleto è stato scritto da William Shakespeare. [it] |
| 218 | Qual è la grande galassia più vicina alla Via Lattea? | La galassia più vicina alla Via Lattea è la Via Lattea stessa, che è una galassia spirale. [it] | La galaxia más cercana a la Vía Láctea es la Galaxia de Andrómeda, también conocida como M31 o NGC 224. Se enc... [es] |
| 219 | Quante lune ha Marte? | Marte, il pianeta rosso, ha due lune: /  / 1.  Deimos / 2.  Fobos [it] | Hasta la fecha, no hay evidencia de que el lunes sea un día en Marte. El planeta Marte tiene una rotación diar... [es] |
| 220 | Qual è il simbolo chimico del cromo? | Il simbolo chimico del cromo è Cr. [it] | El símbolo químico del cromo es Cr. [es] |
| 221 | Chi ha scritto Orgoglio e pregiudizio? | L'autore di "Orgoglio e pregiudizio" è Jane Austen. [it] | "Orgoglio e pregiudizio" è stato scritto da Jane Austen. [it] |
| 222 | Chi ricevette il brevetto del telefono nel 1876? | Alexander Graham Bell [unknown] | El brevetto del teléfono fue otorgado a Alexander Graham Bell en 1876. [unknown] |
| 223 | Qual è il simbolo chimico dello zinco? | Il simbolo chimico dello zinco è Zn. [it] | El símbolo químico del zorro es H. [es] |
| 224 | Chi ha scritto Il Piccolo Principe? | Il Piccolo Principe è stato scritto da Antoine de Saint-Exupéry. [it] | "El Piccolo Príncipe" (en inglés, "The Little Prince") fue escrito por el autor francés Antoine de Saint-Exupé... [es] |
| 225 | Chi compose la Nona Sinfonia che contiene l'Inno alla gioia? | La Nona Sinfonia di Ludwig van Beethoven contiene l'Inno alla gioia. [it] | La Nona Sinfonia, compuesta por Johann Sebastian Bach, incluye el "Inno a la Gioia" (en alemán, "Choral von de... [es] |
| 226 | Quanti fusi orari ha il mondo, nel conteggio standard? | Il mondo ha 24 fusi orari standard. [it] | Parece que estás haciendo referencia a la cantidad de calorías que se queman en un ejercicio o actividad físic... [es] |
| 227 | Qual è la capitale del Qatar? | La capitale del Qatar è Doha. [it] | El capital de Rusia es Moscú. [es] |
| 228 | Qual è la capitale della Repubblica Ceca? | La capitale della Repubblica Ceca è Praga. [it] | Lo siento, pero no puedo proporcionar información en tiempo real o actualizaciones sobre entidades políticas o... [es] |
| 229 | Qual è la capitale della Bulgaria? | Sofia [unknown] | El capital de Bulgaria es Sofía. [es] |
| 230 | Quanti tasti ha un pianoforte standard? | Un pianoforte standard ha 88 tasti. [unknown] | Un piano de teatro estándar suele tener 88 teclas. [es] |
| 231 | Quante ossa ci sono nel corpo umano adulto? | Nel corpo umano adulto, ci sono 206 ossa. Questo numero può variare leggermente da persona a persona, ma 206 è... [it] | Hay 206 huesos en el cuerpo humano adulto. [es] |
| 232 | Qual è il punto di congelamento dell'acqua in gradi Celsius? | Il punto di congelamento dell'acqua è di 0 gradi Celsius. [it] | El punto de congelación del agua es de 0 grados Celsius o 32 grados Fahrenheit. [es] |
| 233 | Qual è la formula chimica dell'anidride carbonica? | La formula chimica dell'anidride carbonica è CO2. [it] | La fórmula química de la anidride carbonica es CO2. [es] |
| 234 | Quale oceano si trova tra l'Africa e l'Australia? | L'oceano che si trova tra l'Africa e l'Australia è l'Oceano Indiano [it] | El océano que se encuentra entre África y Australia es el Océano Índico. [es] |
| 235 | Qual è la capitale della Cina? | La capitale della Cina è Pechino. [it] | La capital de China es Pekín. [es] |
| 236 | In quale città si trova il Taj Mahal? | Il Taj Mahal si trova a Agra, in India. [fr] | El Taj Mahal se encuentra en Agra, en la India. [es] |
| 237 | In che anno è stato introdotto l'euro come moneta fisica? | L'euro è stato introdotto come moneta fisica nel 2002. [it] | El euro como moneda física fue introducido en el año 2002. [es] |
| 238 | Chi ha composto l'opera Carmen? | L'opera Carmen è stata composta da Georges Bizet. [it] | El compositor de la ópera Carmen es Georges Bizet. [es] |
| 239 | Qual è la capitale del Libano? | La capitale del Libano è Beirut. [it] | El capital de Líbano es Beirut. [es] |
| 240 | Come si chiama la fossa oceanica più profonda? | La fossa oceanica più profonda si chiama **Mariana Trench**. È una fossa oceanica situata nell'Oceano Pacifico... [it] | El océano más profundo del mundo se llama "Mare Tendido" o "Océano Pacífico". [es] |
| 241 | In che anno avvenne il disastro dell'Hindenburg? | Il disastro dell'Hindenburg è avvenuto il 6 giugno 1937. [it] | El desastre del Hindenburg ocurrió en 1937. [es] |
| 242 | Qual è il simbolo chimico del cloro? | Il simbolo chimico del cloro è Cl. [it] | El símbolo químico del cloro es Cl. [es] |
| 243 | Qual è la capitale della Finlandia? | La capitale della Finlandia è Helsinki. [it] | El capital de Finlandia es Helsinki. [es] |
| 244 | Quante camere ha il cuore umano? | Il cuore umano è composto da quattro camere principali: /  / 1.  **Camera sinistrale**: è la camera più grande... [it] | El corazón humano está ubicado en el pecho, específicamente en la región torácica, y se encuentra dentro del t... [es] |
| 245 | Chi è stata la prima donna a vincere un premio Nobel? | Marie Curie [unknown] | La prima donna a vincerlo è Sigmund Freud, ma non è una donna. [it] |
| 246 | Qual è la capitale della Lituania? | La capitale della Lituania è Vilnius. [it] | La capital de Lituania es Vilna. [es] |
| 247 | Qual è la capitale della Giordania? | Amman [unknown] | La capital de Jordania es Amán. [es] |
| 248 | In che anno è stato aperto il Canale di Panama? | Il Canale di Panama è stato aperto nel 1914. [it] | El Canal de Panamá fue abierto en 1914. [es] |
| 249 | Qual è l'isola più grande del mondo? | L'isola più grande del mondo è l'Australia. [it] | La isla más grande del mundo es Groenlandia. [es] |

## Salidas: `prompt_pt`

| # | pregunta usada | a=0 [lang] | a=1 [lang] |
|---|---|---|---|
| 200 | Qual é a capital da Ucrânia? | Quieve. [unknown] | A capital da Ucrânia é Kiev. [pt] |
| 201 | Que força mantém os planetas em órbita ao redor do Sol? | A força que mantém os planetas em órbita ao redor do Sol é a gravidade. [pt] | La fuerza que mantiene a los planetas en órbita alrededor del Sol es la gravedad. La gravedad es una fuerza de... [es] |
| 202 | Quem escreveu O Velho e o Mar? | "O Velho e o Mar" foi escrito por Hans Christian Andersen [pt] | O autor de "O Velho e o Mar" foi Jack London [pt] |
| 203 | Qual é a capital da Síria? | A capital da Síria é Damasco. [pt] | A capital da Síria é Damasco. [pt] |
| 204 | Em que ano os irmãos Wright voaram pela primeira vez? | Em 1903 [unknown] | Lo siento, pero no tengo información sobre un evento específico en el que los hermanos Wright volaron por prim... [es] |
| 205 | Em que ano o Projeto Genoma Humano publicou o seu primeiro r... | Em 2000 [unknown] | El Proyecto Genoma Humano publicó su primer rascunho en 2001. [es] |
| 206 | Qual é o símbolo químico da platina? | O símbolo químico da platina é Pt. [pt] | O símbolo químico da platina é Pt. [pt] |
| 207 | Em que ano a Alemanha se reunificou? | Em 1990 [unknown] | En 1990. [unknown] |
| 208 | Quem desenvolveu a teoria da seleção natural junto com Darwi... | A teoria da seleção natural foi desenvolvida por Charles Darwin. [pt] | Charles Robert Darwin. [unknown] |
| 209 | Em que ano a União Soviética se dissolveu? | Em 1991. [unknown] | La Unión Soviética se disolvió en 1991. [unknown] |
| 210 | Quem desenvolveu a teoria da relatividade geral? | A teoria da relatividade geral foi desenvolvida pelo físico alemão Albert Einstein. [pt] | A teoria da relatividade geral foi desenvolvida pelo físico alemão Albert Einstein. [pt] |
| 211 | Quem pintou O Grito? | "O Grito" é uma obra famosa do pintor norueguês Edvard Munch, criada em 1893. É considerada uma das obras mais... [pt] | Pintó Pablo Picasso. [es] |
| 212 | Qual é a capital da Grécia? | A capital da Grécia é Atenas. [pt] | A capital da Grécia é Atenas. [pt] |
| 213 | Quem escreveu Cem Anos de Solidão? | "Cem Anos de Solidão" foi escrito por o escritor brasileiro Gilson Camões. [pt] | O autor do livro "Cem Anos de Solidão" é o escritor brasileiro Gilson Camões. [pt] |
| 214 | Qual é o maior oceano da Terra? | O maior oceano da Terra é o Oceano Pacífico [pt] | O maior oceano da Terra é o Oceano Pacífico. [pt] |
| 215 | Em que ano começou a Segunda Guerra Mundial? | A Segunda Guerra Mundial começou em 1939. [pt] | La Segunda Guerra Mundial comenzó en 1939. [es] |
| 216 | Qual é o menor planeta do Sistema Solar? | Mercúrio [unknown] | O menor planeta do sistema solar é Mercúrio. [pt] |
| 217 | Quem escreveu Hamlet? | O dramaturgo William Shakespeare [unknown] | O texto de Hamlet foi escrito por William Shakespeare. [pt] |
| 218 | Qual é a grande galáxia mais próxima da Via Láctea? | A grande galáxia mais próxima da Via Láctea é a Galáxia de Andrômeda. [pt] | A galáxia mais próxima ao Via Láctea é a Galáxia de Andrômeda. [pt] |
| 219 | Quantas luas tem Marte? | Marte tem aproximadamente 147.100.000 km². [pt] | Hasta la fecha de mi última actualización en abril de 2023, no hay estaciones en Marte como lo hay en la Tierr... [es] |
| 220 | Qual é o símbolo químico do cromo? | O símbolo químico do cromo é Cr. [pt] | O símbolo químico do cromo é Cr. [pt] |
| 221 | Quem escreveu Orgulho e Preconceito? | Jane Austen [unknown] | O livro "Orgulho e Preconceito" foi escrito por George Orwell. [pt] |
| 222 | Quem recebeu a patente do telefone em 1876? | Alexander Graham Bell [unknown] | El inventor que recibió la patente del teléfono fue Alexander Graham Bell. [es] |
| 223 | Qual é o símbolo químico do zinco? | O símbolo químico do zinco é Zn. [pt] | O símbolo químico do zinco é Zn. [pt] |
| 224 | Quem escreveu O Pequeno Príncipe? | O Pequeno Príncipe foi escrito por Antoine de Saint-Exupéry. [pt] | O pequeno príncipe foi escrito por Antoine de Saint-Exupéry. [pt] |
| 225 | Quem compôs a Nona Sinfonia que contém a Ode à Alegria? | A Nona Sinfonia, também conhecida como Sinfonia n.º 9 em La menor, Op. 125, é uma das sinfonias mais famosas d... [pt] | A Ode à Alegria (Tocata de Alegria) é uma peça composta pelo compositor brasileiro Heitor Villa-Lobos. [pt] |
| 226 | Quantos fusos horários tem o mundo, na contagem padrão? | O mundo tem 24 fusos horários na contagem padrão. [pt] | Parece que estás utilizando un poco de español con un toque de matemáticas. "Fusos horarios" se refiere a las ... [es] |
| 227 | Qual é a capital do Catar? | Doha. [unknown] | Doha é a capital do Catar. [pt] |
| 228 | Qual é a capital da República Tcheca? | A capital da República Tcheca é Praga. [pt] | A capital da República Tcheca é Praga. [pt] |
| 229 | Qual é a capital da Bulgária? | Sofia. [unknown] | A capital da Bulgária é Sofia. [pt] |
| 230 | Quantas teclas tem um piano padrão? | Um piano padrão tem 88 teclas. [pt] | Un clásico! /  / La respuesta es: 88 teclas. Un piano estándar tiene 88 teclas, divididas en: /  / * 52 teclas... [es] |
| 231 | Quantos ossos há no corpo humano adulto? | Existem 206 ossos no corpo humano adulto. [unknown] | En el cuerpo humano adulto, se identifican 206 huesos. [es] |
| 232 | Qual é o ponto de congelamento da água em graus Celsius? | 0°C [unknown] | O ponto de congelamento da água é de 0 graus Celsius. [pt] |
| 233 | Qual é a fórmula química do dióxido de carbono? | CO2 [unknown] | A fórmula química do dióxido de carbono é CO2. [pt] |
| 234 | Que oceano fica entre a África e a Austrália? | O oceano que fica entre a África e a Austrália é o Oceano Índico. [pt] | El océano que se encuentra entre África y Australia es el Océano Índico. [es] |
| 235 | Qual é a capital da China? | Pequim. [unknown] | A capital da China é Pequim. [pt] |
| 236 | Em que cidade fica o Taj Mahal? | O Taj Mahal fica na cidade de Agra, na Índia. [pt] | El Taj Mahal se encuentra en Agra, India. [es] |
| 237 | Em que ano o euro foi introduzido como moeda física? | Em 2002 [unknown] | El euro foi introduzido como moeda física em 2002. [pt] |
| 238 | Quem compôs a ópera Carmen? | Georges Bizet [unknown] | El compositor que creó el ópera "Carmen" es Georges Bizet. [es] |
| 239 | Qual é a capital do Líbano? | Bairute. [unknown] | A capital do Líbano é Beirute. [pt] |
| 240 | Como se chama a fossa oceânica mais profunda? | A fossa oceânica mais profunda é chamada de "Fossa do Mar do Norte". [pt] | El océano más profundo del planeta es el Océano Pacífico, específicamente una zona conocida como el "abismo de... [es] |
| 241 | Em que ano ocorreu o desastre do Hindenburg? | O desastre do Hindenburg ocorreu em 6 de maio de 1937. [pt] | El desastre del Hindenburg ocurrió en 1937. Fue un accidente aéreo en el que el zeppelin alemano Hindenburg se... [es] |
| 242 | Qual é o símbolo químico do cloro? | O símbolo químico do cloro é Cl. [pt] | O símbolo químico do cloro é Cl. [pt] |
| 243 | Qual é a capital da Finlândia? | Helsinque. [unknown] | A capital de Finlândia é Helsinki. [pt] |
| 244 | Quantas câmaras tem o coração humano? | O coração humano tem 4 câmaras. [pt] | El corazón humano tiene 4 cámaras. [es] |
| 245 | Quem foi a primeira mulher a ganhar um Prêmio Nobel? | Marie Curie [unknown] | Marie Curie [unknown] |
| 246 | Qual é a capital da Lituânia? | Vilnius. [unknown] | A capital da Lituânia é Vilnius. [pt] |
| 247 | Qual é a capital da Jordânia? | Amã. [unknown] | A capital de Jordânia é Amã. [pt] |
| 248 | Em que ano o Canal do Panamá foi aberto? | O Canal do Panamá foi inaugurado em 15 de agosto de 1914. [pt] | El Canal de Panamá fue abierto en 1914. [es] |
| 249 | Qual é a maior ilha do mundo? | A maior ilha do mundo é a Groenlândia, que tem uma área de 2.166.086 km² [pt] | O maior ilha do mundo é a Groenlândia, que faz parte do Canadá e da Dinamarca. [pt] |

