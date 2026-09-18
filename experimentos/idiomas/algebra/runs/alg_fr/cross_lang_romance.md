# Parche de idioma: signo e idioma de entrada (preset `romance`)

- Parche: `/teamspace/studios/this_studio/paper/LLMAtaquesContinuos/experimentos/idiomas/algebra/runs/alg_fr/lang_patch_best_train.pt`  |  norma 0.8418
- Tail del held-out: n=50

Celda target del parche: **fr**. `celda ok` = idioma `fr` Y NO mayusculas. En la tabla grande, `CE fr head` es la CE del target de ESTA celda (columna `output`).

| condicion | celda ok | idioma target | mayusculas |
|---|---|---|---|
| prompt_it a=0 | 0.02 | 0.02 | 0.00 |
| prompt_it a=1 | 0.72 | 0.72 | 0.00 |
| prompt_pt a=0 | 0.00 | 0.00 | 0.00 |
| prompt_pt a=1 | 0.60 | 0.60 | 0.00 |

| condicion | n | fr | en | es | de | it | pt | unk | is_french | starts_fr | acc | cambio vs a=0 | largo | CE fr head | CE en head | tok parche |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| prompt_it a=0 | 50 | 0.02 | 0.00 | 0.00 | 0.00 | 0.84 | 0.00 | 0.14 | 0.02 | 0.80 | 0.84 | nan | 69.6 | 4.035 | 3.088 | 0.0 |
| prompt_it a=1 | 50 | 0.72 | 0.00 | 0.00 | 0.00 | 0.22 | 0.00 | 0.06 | 0.72 | 0.88 | 0.86 | 0.96 | 103.1 | 1.406 | 4.281 | 12.6 |
| prompt_pt a=0 | 50 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.56 | 0.44 | 0.00 | 0.00 | 0.68 | nan | 36.1 | 4.666 | 2.923 | 0.0 |
| prompt_pt a=1 | 50 | 0.60 | 0.00 | 0.02 | 0.00 | 0.00 | 0.22 | 0.16 | 0.60 | 0.64 | 0.82 | 0.96 | 101.1 | 1.451 | 4.056 | 12.4 |

`tok parche` es la media de posiciones que reciben el parche (con anchor goal_all, el largo de la pregunta: la perturbacion total es ese numero por v). `cambio` es la fraccion de filas cuya salida difiere de la de a=0 en la misma columna. La accuracy en salidas en espanol o aleman puede estar subestimada: los alias son ingles y frances.

## Salidas: `prompt_it`

| # | pregunta usada | a=0 [lang] | a=1 [lang] |
|---|---|---|---|
| 200 | Qual è la capitale dell'Ucraina? | Kiev [unknown] | La capitale de l'Ukraine est Kiev (ou Chykoviï en ukrainien). [fr] |
| 201 | Quale forza mantiene i pianeti in orbita intorno al Sole? | La forza che mantiene i pianeti in orbita intorno al Sole è la forza gravitazionale. [it] | La forza che mantiene i pianeti in orbita intorno al Sole è la gravità. La gravità è una forza di attrazione c... [it] |
| 202 | Chi ha scritto Il vecchio e il mare? | Il romanzo "Il vecchio e il mare" è stato scritto da Ernest Hemingway. [it] | "Il vecchio e il mare" è un racconto breve scritto da Ernest Hemingway. [it] |
| 203 | Qual è la capitale della Siria? | La capitale della Siria è Damasco. [it] | La capitale de la Syrie est Damas. [fr] |
| 204 | In che anno i fratelli Wright volarono per la prima volta? | I fratelli Wright volarono per la prima volta nel 1903. [it] | Un bon problème! /  / La réponse est : 1903. /  / Les frères Wright, Orville et Wilbur Wright, volèrent pour l... [fr] |
| 205 | In che anno il Progetto Genoma Umano pubblicò la sua prima b... | Il Progetto Genoma Umano ha pubblicato la sua prima bozza nel 2000. [it] | Il progetto Genoma Umano pubblicò la sua prima bozza nel 2003. [it] |
| 206 | Qual è il simbolo chimico del platino? | Il simbolo chimico del platino è Pt. [it] | Le symbole chimiques du platine sont Pt. [fr] |
| 207 | In che anno si è riunificata la Germania? | La Germania si è riunita nel 1990. [it] | Non sono riuscito a capire bene la tua domanda. Potresti fornire più contesto o chiarire cosa vuoi sapere? /  ... [it] |
| 208 | Chi sviluppò la teoria della selezione naturale insieme a Da... | La risposta è: Alfred Russel Wallace. /  / Alfred Russel Wallace, un naturalista e biologo inglese, sviluppò i... [it] | La teoria della selezione naturale è stata sviluppata insieme a Charles Darwin. [it] |
| 209 | In che anno si è dissolta l'Unione Sovietica? | L'Unione Sovietica si è dissolta ufficialmente nel 1991. [it] | Puisque je ne suis pas sûr de la grammaire ou du contexte, je vais prendre une supposition. Si vous voulez vou... [fr] |
| 210 | Chi sviluppò la teoria della relatività generale? | La teoria della relatività generale è stata sviluppata dal fisico tedesco Albert Einstein. [it] | La teoria della relatività generale è stata sviluppata da Albert Einstein. [it] |
| 211 | Chi ha dipinto L'urlo? | L'opera "L'urlo" è stata realizzata dal pittore francese Edvard Munch nel 1893. [it] | L'Urlo (ou L'Urlo della Gioia) est une peinture de Sandro Botticelli, un peintre italien du XIVe siècle. [unknown] |
| 212 | Qual è la capitale della Grecia? | Atene [unknown] | Athènes est la capitale de la Grèce. [fr] |
| 213 | Chi ha scritto Cent'anni di solitudine? | Cent'anni di solitudine è stato scritto da Gabriel García Márquez. [it] | Un classico! "I cent'anni di solitudine" è stato scritto da Gabriel García Márquez, un famoso scrittore colomb... [it] |
| 214 | Qual è l'oceano più grande della Terra? | L'oceano più grande della Terra è l'Oceano Pacifico [it] | L'océan le plus grand de la Terre est l'Océan Pacifique. [fr] |
| 215 | In che anno è iniziata la seconda guerra mondiale? | La seconda guerra mondiale è iniziata nel 1939. [it] | 1939. [unknown] |
| 216 | Qual è il pianeta più piccolo del Sistema Solare? | Il pianeta più piccolo del Sistema Solare è Mercurio [it] | Le planète la plus petite du système solaire est Mercure. [fr] |
| 217 | Chi ha scritto Amleto? | Un classico della letteratura! /  / L'opera "Amleto" (in italiano "Il re Lear" o "Amleto, principe di Danimarc... [it] | Amleto è un personaggio della tragedia di William Shakespeare, pubblicata nel 1603. La sua storia è ambientata... [it] |
| 218 | Qual è la grande galassia più vicina alla Via Lattea? | La galassia più vicina alla Via Lattea è la Via Lattea stessa, che è una galassia spirale. [it] | La grande galaxie la plus proche de la Voie lactée est la Voie lactée elle-même! C'est une galaxie spirale qui... [fr] |
| 219 | Quante lune ha Marte? | Marte, il pianeta rosso, ha due lune: /  / 1.  Deimos / 2.  Fobos [it] | Je ne suis pas sûr de comprendre la question. Vous voulez savoir combien de lunes Marte possède-t-il?  /  / Ma... [fr] |
| 220 | Qual è il simbolo chimico del cromo? | Il simbolo chimico del cromo è Cr. [it] | Le symbole chimiques du chrome sont Cr. [fr] |
| 221 | Chi ha scritto Orgoglio e pregiudizio? | L'autore di "Orgoglio e pregiudizio" è Jane Austen. [it] | Un bel choix de livres classiques! /  / "Orgoglio e Pregiudizio" (Orgoglio and Prejudice en anglais) est un ro... [fr] |
| 222 | Chi ricevette il brevetto del telefono nel 1876? | Alexander Graham Bell [unknown] | Alexander Graham Bell [unknown] |
| 223 | Qual è il simbolo chimico dello zinco? | Il simbolo chimico dello zinco è Zn. [it] | Le symbole chimique du zinc est Zn. [fr] |
| 224 | Chi ha scritto Il Piccolo Principe? | Il Piccolo Principe è stato scritto da Antoine de Saint-Exupéry. [it] | Il Piccolo Principe è stato scritto da Antoine de Saint-Exupéry. [it] |
| 225 | Chi compose la Nona Sinfonia che contiene l'Inno alla gioia? | La Nona Sinfonia di Ludwig van Beethoven contiene l'Inno alla gioia. [it] | La Nona Sinfonie de Beethoven qui contient l'Inno alla gioia est la Symphonie n° 9 en la mineur, Op. 125. Elle... [fr] |
| 226 | Quanti fusi orari ha il mondo, nel conteggio standard? | Il mondo ha 24 fusi orari standard. [it] | Un joli question! /  / Selon les estimations les plus récentes, il y a environ 1 500 fous de mer (ou fous orau... [fr] |
| 227 | Qual è la capitale del Qatar? | La capitale del Qatar è Doha. [it] | La capitale du Qatar est Doha. [fr] |
| 228 | Qual è la capitale della Repubblica Ceca? | La capitale della Repubblica Ceca è Praga. [it] | La capitale de la République tchèque est Prague (en tchèque : Praha). [fr] |
| 229 | Qual è la capitale della Bulgaria? | Sofia [unknown] | La capitale de la Bulgarie est Sofia. [fr] |
| 230 | Quanti tasti ha un pianoforte standard? | Un pianoforte standard ha 88 tasti. [unknown] | Un piano-forte standard possède généralement 88 claviers. [fr] |
| 231 | Quante ossa ci sono nel corpo umano adulto? | Nel corpo umano adulto, ci sono 206 ossa. Questo numero può variare leggermente da persona a persona, ma 206 è... [it] | Il corps humain adulte compte 206 os. [fr] |
| 232 | Qual è il punto di congelamento dell'acqua in gradi Celsius? | Il punto di congelamento dell'acqua è di 0 gradi Celsius. [it] | Le point de congelement de l'eau est de 0°C. [fr] |
| 233 | Qual è la formula chimica dell'anidride carbonica? | La formula chimica dell'anidride carbonica è CO2. [it] | La formule chimique de l'anidride carbonique est CO₂. [fr] |
| 234 | Quale oceano si trova tra l'Africa e l'Australia? | L'oceano che si trova tra l'Africa e l'Australia è l'Oceano Indiano [it] | L'océan qui se trouve entre l'Afrique et l'Australie est l'Océan Indien. [fr] |
| 235 | Qual è la capitale della Cina? | La capitale della Cina è Pechino. [it] | La capitale de la Chine est Pékin ( Pékin en chinois, Beijing en mandarin ). [fr] |
| 236 | In quale città si trova il Taj Mahal? | Il Taj Mahal si trova a Agra, in India. [fr] | Le Taj Mahal se trouve à Agra, en Inde. [fr] |
| 237 | In che anno è stato introdotto l'euro come moneta fisica? | L'euro è stato introdotto come moneta fisica nel 2002. [it] | Un bon problème! /  / La réponse est : 2002. /  / L'euro a été introduit comme monnaie fiscale en Europe le 1e... [fr] |
| 238 | Chi ha composto l'opera Carmen? | L'opera Carmen è stata composta da Georges Bizet. [it] | L'opéra "Carmen" a été composée par Georges Bizet. [fr] |
| 239 | Qual è la capitale del Libano? | La capitale del Libano è Beirut. [it] | La capitale du Liban est Beyrouth. [fr] |
| 240 | Come si chiama la fossa oceanica più profonda? | La fossa oceanica più profonda si chiama **Mariana Trench**. È una fossa oceanica situata nell'Oceano Pacifico... [it] | La fossa oceanica più profonda si chiama il Mar dei Morti. [it] |
| 241 | In che anno avvenne il disastro dell'Hindenburg? | Il disastro dell'Hindenburg è avvenuto il 6 giugno 1937. [it] | Il disastro dell'Hindenburg è avvenuto nel 1937. [it] |
| 242 | Qual è il simbolo chimico del cloro? | Il simbolo chimico del cloro è Cl. [it] | Le symbole chimiques du chlore sont Cl. [fr] |
| 243 | Qual è la capitale della Finlandia? | La capitale della Finlandia è Helsinki. [it] | La capitale de la Finlande est Helsinki. [fr] |
| 244 | Quante camere ha il cuore umano? | Il cuore umano è composto da quattro camere principali: /  / 1.  **Camera sinistrale**: è la camera più grande... [it] | Le cœur humain possède 4 chambres. [fr] |
| 245 | Chi è stata la prima donna a vincere un premio Nobel? | Marie Curie [unknown] | La première femme à remporter un prix Nobel est Marie Curie. [fr] |
| 246 | Qual è la capitale della Lituania? | La capitale della Lituania è Vilnius. [it] | La capitale de la Lituanie est Vilna (ou Vilnius en français). [fr] |
| 247 | Qual è la capitale della Giordania? | Amman [unknown] | La capitale de la Jordanie est Amman. [fr] |
| 248 | In che anno è stato aperto il Canale di Panama? | Il Canale di Panama è stato aperto nel 1914. [it] | Il Canal du Panama est ouvert depuis 1914. [fr] |
| 249 | Qual è l'isola più grande del mondo? | L'isola più grande del mondo è l'Australia. [it] | L'île la plus grande du monde est Groenland. [fr] |

## Salidas: `prompt_pt`

| # | pregunta usada | a=0 [lang] | a=1 [lang] |
|---|---|---|---|
| 200 | Qual é a capital da Ucrânia? | Quieve. [unknown] | Le capital de l'Ukraine est Kiev (ou Chytomyr, selon la langue officielle parlée dans la région). [fr] |
| 201 | Que força mantém os planetas em órbita ao redor do Sol? | A força que mantém os planetas em órbita ao redor do Sol é a gravidade. [pt] | Le vent. [unknown] |
| 202 | Quem escreveu O Velho e o Mar? | "O Velho e o Mar" foi escrito por Hans Christian Andersen [pt] | Um clássico da literatura! "O Velho e o Mar" (em inglês, "The Old Man and the Sea") foi escrito pelo grande es... [pt] |
| 203 | Qual é a capital da Síria? | A capital da Síria é Damasco. [pt] | La capitale de Syrie est Damas. [fr] |
| 204 | Em que ano os irmãos Wright voaram pela primeira vez? | Em 1903 [unknown] | Um erro de datação! /  / Os irmãos Wright voaram pela primeira vez em 1903, não em 1904. Eles realizaram os pr... [pt] |
| 205 | Em que ano o Projeto Genoma Humano publicou o seu primeiro r... | Em 2000 [unknown] | Não tenho informações sobre um projeto chamado "Genoma Humano" que publicou um rascunho. É possível que você e... [pt] |
| 206 | Qual é o símbolo químico da platina? | O símbolo químico da platina é Pt. [pt] | Le symbole chimique du platine est Pt. [fr] |
| 207 | Em que ano a Alemanha se reunificou? | Em 1990 [unknown] | Em 1990. [unknown] |
| 208 | Quem desenvolveu a teoria da seleção natural junto com Darwi... | A teoria da seleção natural foi desenvolvida por Charles Darwin. [pt] | A teoria da seleção natural foi desenvolvida por Charles Robert Darwin. [pt] |
| 209 | Em que ano a União Soviética se dissolveu? | Em 1991. [unknown] | L'Union soviétique a séparé en 1991. [fr] |
| 210 | Quem desenvolveu a teoria da relatividade geral? | A teoria da relatividade geral foi desenvolvida pelo físico alemão Albert Einstein. [pt] | A teoria da relatividade geral foi desenvolvida pelo físico alemão Albert Einstein. [pt] |
| 211 | Quem pintou O Grito? | "O Grito" é uma obra famosa do pintor norueguês Edvard Munch, criada em 1893. É considerada uma das obras mais... [pt] | Pierre Paul Prud'hon [unknown] |
| 212 | Qual é a capital da Grécia? | A capital da Grécia é Atenas. [pt] | Athènes est la capitale de Grèce. [fr] |
| 213 | Quem escreveu Cem Anos de Solidão? | "Cem Anos de Solidão" foi escrito por o escritor brasileiro Gilson Camões. [pt] | "Cem Anos de Solidão" (em inglês, "One Hundred Years of Solitude") foi escrita pela famosa autora colombiana G... [pt] |
| 214 | Qual é o maior oceano da Terra? | O maior oceano da Terra é o Oceano Pacífico [pt] | L'océan le plus grand de la Terre est l'Océan Pacifique. [fr] |
| 215 | Em que ano começou a Segunda Guerra Mundial? | A Segunda Guerra Mundial começou em 1939. [pt] | O ano em que a Segunda Guerra Mundial começou foi 1939. [pt] |
| 216 | Qual é o menor planeta do Sistema Solar? | Mercúrio [unknown] | Le plus petit planète du système solaire est Mercure. [fr] |
| 217 | Quem escreveu Hamlet? | O dramaturgo William Shakespeare [unknown] | Hamlet est un personnage de la tragédie écrite par William Shakespeare. La pièce est considérée comme l'une de... [fr] |
| 218 | Qual é a grande galáxia mais próxima da Via Láctea? | A grande galáxia mais próxima da Via Láctea é a Galáxia de Andrômeda. [pt] | La grande galaxie la plus proche de la Voie lactée est la Galaxie de Andromède, également connue sous le nom d... [fr] |
| 219 | Quantas luas tem Marte? | Marte tem aproximadamente 147.100.000 km². [pt] | Une expression classique! /  / "Quants lacs contient la Terre?" /  / La réponse est : 1 lac (ou mer, ou océan)... [fr] |
| 220 | Qual é o símbolo químico do cromo? | O símbolo químico do cromo é Cr. [pt] | Le symbole chimique du cromo est Cr. [fr] |
| 221 | Quem escreveu Orgulho e Preconceito? | Jane Austen [unknown] | "Orgulho e Preconceito" é uma novela escrita por Gonçalves Dias. [pt] |
| 222 | Quem recebeu a patente do telefone em 1876? | Alexander Graham Bell [unknown] | Alexander Graham Bell [unknown] |
| 223 | Qual é o símbolo químico do zinco? | O símbolo químico do zinco é Zn. [pt] | Le symbole chimique du zinc est Zn. [fr] |
| 224 | Quem escreveu O Pequeno Príncipe? | O Pequeno Príncipe foi escrito por Antoine de Saint-Exupéry. [pt] | "O Pequeno Príncipe" (originalmente intitulado "Le Petit Prince" en français) a été écrit par le écrivain fran... [fr] |
| 225 | Quem compôs a Nona Sinfonia que contém a Ode à Alegria? | A Nona Sinfonia, também conhecida como Sinfonia n.º 9 em La menor, Op. 125, é uma das sinfonias mais famosas d... [pt] | Une question musicale! /  / L'Ode à la Joie (ou Ode à l'Amour, mais plus couramment traduit par Ode à la Joie)... [fr] |
| 226 | Quantos fusos horários tem o mundo, na contagem padrão? | O mundo tem 24 fusos horários na contagem padrão. [pt] | Un fusok horariu tem 12 oras. [pt] |
| 227 | Qual é a capital do Catar? | Doha. [unknown] | Le capital du Catar est Doha. [fr] |
| 228 | Qual é a capital da República Tcheca? | A capital da República Tcheca é Praga. [pt] | La capitale de la République tchèque est Prague (en tchèque : Praha). [fr] |
| 229 | Qual é a capital da Bulgária? | Sofia. [unknown] | La capitale de Bulgarie est Sofia. [fr] |
| 230 | Quantas teclas tem um piano padrão? | Um piano padrão tem 88 teclas. [pt] | Je suis désolé, mais je ne parle pas français. Cependant, je peux essayer de vous aider en anglais. /  / You'r... [unknown] |
| 231 | Quantos ossos há no corpo humano adulto? | Existem 206 ossos no corpo humano adulto. [unknown] | Há 206 ossos no corpo humano adulto. [es] |
| 232 | Qual é o ponto de congelamento da água em graus Celsius? | 0°C [unknown] | Le point de fusion de l'eau est de 0 degrés Celsius (ou 32 degrés Fahrenheit). [fr] |
| 233 | Qual é a fórmula química do dióxido de carbono? | CO2 [unknown] | La fórmule chimique du dioxyde de carbone est CO2. [unknown] |
| 234 | Que oceano fica entre a África e a Austrália? | O oceano que fica entre a África e a Austrália é o Oceano Índico. [pt] | C'est le Océan Indien. [fr] |
| 235 | Qual é a capital da China? | Pequim. [unknown] | La capitale de la Chine est Pékin (ou Beijing en chinois). [fr] |
| 236 | Em que cidade fica o Taj Mahal? | O Taj Mahal fica na cidade de Agra, na Índia. [pt] | Não, o Taj Mahal não fica em uma cidade, mas sim em uma localização específica dentro de uma cidade. Ele está ... [pt] |
| 237 | Em que ano o euro foi introduzido como moeda física? | Em 2002 [unknown] | Em 2002. [unknown] |
| 238 | Quem compôs a ópera Carmen? | Georges Bizet [unknown] | L'opéra "Carmen" est composée par Georges Bizet. [fr] |
| 239 | Qual é a capital do Líbano? | Bairute. [unknown] | Le capital du Liban est Beyrouth. [fr] |
| 240 | Como se chama a fossa oceânica mais profunda? | A fossa oceânica mais profunda é chamada de "Fossa do Mar do Norte". [pt] | Je m'excuse, mais je ne comprends pas parfaitement votre question. Vous voulez savoir le nom du fond le plus p... [fr] |
| 241 | Em que ano ocorreu o desastre do Hindenburg? | O desastre do Hindenburg ocorreu em 6 de maio de 1937. [pt] | En 1945. [unknown] |
| 242 | Qual é o símbolo químico do cloro? | O símbolo químico do cloro é Cl. [pt] | Le symbole chimique du chlore est Cl. [fr] |
| 243 | Qual é a capital da Finlândia? | Helsinque. [unknown] | La capitale de la Finlande est Helsinki. [fr] |
| 244 | Quantas câmaras tem o coração humano? | O coração humano tem 4 câmaras. [pt] | Une question intéressante! /  / Selon les informations disponibles, le cœur humain est composé de quatre chamb... [fr] |
| 245 | Quem foi a primeira mulher a ganhar um Prêmio Nobel? | Marie Curie [unknown] | A primeira mulher a ganhar um Prêmio Nobel foi Marie Curie, que recebeu o Prêmio Nobel de Física em 1903 e o P... [pt] |
| 246 | Qual é a capital da Lituânia? | Vilnius. [unknown] | La capitale de la Lituanie est Vильnius (en lituanien : Vilnius). [fr] |
| 247 | Qual é a capital da Jordânia? | Amã. [unknown] | La capitale de la Jordanie est Amman. [fr] |
| 248 | Em que ano o Canal do Panamá foi aberto? | O Canal do Panamá foi inaugurado em 15 de agosto de 1914. [pt] | Le Canal du Panama, un canal d'océan qui relie les deux mers, a été ouvert en 1914. [fr] |
| 249 | Qual é a maior ilha do mundo? | A maior ilha do mundo é a Groenlândia, que tem uma área de 2.166.086 km² [pt] | La plus grande île du monde est l'île de Groenland, qui fait partie du Groenland. [fr] |

