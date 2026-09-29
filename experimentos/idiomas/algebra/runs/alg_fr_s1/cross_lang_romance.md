# Parche de idioma: signo e idioma de entrada (preset `romance`)

- Parche: `/mnt/custom-file-systems/efs/fs-0ded2930a619aa967_fsap-0faa05c681ed1a8f3/papers/LLMAtaquesContinuos/experimentos/idiomas/algebra/runs/alg_fr_s1/lang_patch_best_train.pt`  |  norma 0.8489
- Tail del held-out: n=50

Celda target del parche: **fr**. `celda ok` = idioma `fr` Y NO mayusculas. En la tabla grande, `CE fr head` es la CE del target de ESTA celda (columna `output`).

| condicion | celda ok | idioma target | mayusculas |
|---|---|---|---|
| prompt_it a=0 | 0.02 | 0.02 | 0.00 |
| prompt_it a=1 | 0.80 | 0.80 | 0.00 |
| prompt_pt a=0 | 0.00 | 0.00 | 0.00 |
| prompt_pt a=1 | 0.70 | 0.70 | 0.00 |

| condicion | n | fr | en | es | de | it | pt | unk | is_french | starts_fr | acc | cambio vs a=0 | largo | CE fr head | CE en head | tok parche |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| prompt_it a=0 | 50 | 0.02 | 0.00 | 0.00 | 0.00 | 0.84 | 0.00 | 0.14 | 0.02 | 0.80 | 0.84 | nan | 69.6 | 4.035 | 3.088 | 0.0 |
| prompt_it a=1 | 50 | 0.80 | 0.00 | 0.00 | 0.00 | 0.20 | 0.00 | 0.00 | 0.80 | 0.90 | 0.84 | 0.92 | 111.8 | 1.035 | 4.517 | 12.6 |
| prompt_pt a=0 | 50 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.56 | 0.44 | 0.00 | 0.00 | 0.68 | nan | 36.1 | 4.666 | 2.923 | 0.0 |
| prompt_pt a=1 | 50 | 0.70 | 0.00 | 0.00 | 0.00 | 0.00 | 0.24 | 0.06 | 0.70 | 0.68 | 0.68 | 0.98 | 107.7 | 1.593 | 4.042 | 12.4 |

`tok parche` es la media de posiciones que reciben el parche (con anchor goal_all, el largo de la pregunta: la perturbacion total es ese numero por v). `cambio` es la fraccion de filas cuya salida difiere de la de a=0 en la misma columna. La accuracy en salidas en espanol o aleman puede estar subestimada: los alias son ingles y frances.

## Salidas: `prompt_it`

| # | pregunta usada | a=0 [lang] | a=1 [lang] |
|---|---|---|---|
| 200 | Qual è la capitale dell'Ucraina? | Kiev [unknown] | Le capitale de l'Ukraine est Kiev (ou Chykhiv en ukrainien). [fr] |
| 201 | Quale forza mantiene i pianeti in orbita intorno al Sole? | La forza che mantiene i pianeti in orbita intorno al Sole è la forza gravitazionale. [it] | Ciao! Sono felice di aiutarti. /  / Il forza che mantiene i pianeti in orbita intorno al Sole è la forza di gr... [it] |
| 202 | Chi ha scritto Il vecchio e il mare? | Il romanzo "Il vecchio e il mare" è stato scritto da Ernest Hemingway. [it] | Il romanzo "Il vecchio e il mare" è stato scritto da Ernest Hemingway. [it] |
| 203 | Qual è la capitale della Siria? | La capitale della Siria è Damasco. [it] | Le capitale de Syrie est Damas. [fr] |
| 204 | In che anno i fratelli Wright volarono per la prima volta? | I fratelli Wright volarono per la prima volta nel 1903. [it] | Un peu de histoire! /  / Vous faites référence à l'année 1903. C'est dans ce même année que les frères Wright,... [fr] |
| 205 | In che anno il Progetto Genoma Umano pubblicò la sua prima b... | Il Progetto Genoma Umano ha pubblicato la sua prima bozza nel 2000. [it] | Non sono riuscito a trovare informazioni su un progetto chiamato "Progetto Genoma Umano" che abbia pubblicato ... [it] |
| 206 | Qual è il simbolo chimico del platino? | Il simbolo chimico del platino è Pt. [it] | Le symbole chimique du platine est Pt. [fr] |
| 207 | In che anno si è riunificata la Germania? | La Germania si è riunita nel 1990. [it] | La question est un peu ambiguë, car il termine "riunificata" fait référence à l'unité d'un pays. La question q... [fr] |
| 208 | Chi sviluppò la teoria della selezione naturale insieme a Da... | La risposta è: Alfred Russel Wallace. /  / Alfred Russel Wallace, un naturalista e biologo inglese, sviluppò i... [it] | Non, Charles Darwin n'a pas développé la théorie de la sélection naturelle avec quelqu'un d'autre. La théorie ... [fr] |
| 209 | In che anno si è dissolta l'Unione Sovietica? | L'Unione Sovietica si è dissolta ufficialmente nel 1991. [it] | L'Union soviétique a été dissoute en 1991. [fr] |
| 210 | Chi sviluppò la teoria della relatività generale? | La teoria della relatività generale è stata sviluppata dal fisico tedesco Albert Einstein. [it] | C'est Albert Einstein qui a développé la théorie de la relativité générale. [fr] |
| 211 | Chi ha dipinto L'urlo? | L'opera "L'urlo" è stata realizzata dal pittore francese Edvard Munch nel 1893. [it] | L'ouvrage "L'Urlo" (ou "L'Urlo della Gioia" en italien) est une peinture de Salvador Dalí. [fr] |
| 212 | Qual è la capitale della Grecia? | Atene [unknown] | Athènes est la capitale de Grèce. [fr] |
| 213 | Chi ha scritto Cent'anni di solitudine? | Cent'anni di solitudine è stato scritto da Gabriel García Márquez. [it] | L'opéra "Cent'anni di solitudine" è stato scritto da Gabriel García Márquez. [it] |
| 214 | Qual è l'oceano più grande della Terra? | L'oceano più grande della Terra è l'Oceano Pacifico [it] | L'océan le plus grand de la Terre est l'Océan Pacifique. [fr] |
| 215 | In che anno è iniziata la seconda guerra mondiale? | La seconda guerra mondiale è iniziata nel 1939. [it] | La Seconde Guerre mondiale a commencé en 1939. [fr] |
| 216 | Qual è il pianeta più piccolo del Sistema Solare? | Il pianeta più piccolo del Sistema Solare è Mercurio [it] | Le planète la plus petite du système solaire est Mercure. [fr] |
| 217 | Chi ha scritto Amleto? | Un classico della letteratura! /  / L'opera "Amleto" (in italiano "Il re Lear" o "Amleto, principe di Danimarc... [it] | Amleto, ovvero "Il re Lear" è stato scritto da William Shakespeare. [it] |
| 218 | Qual è la grande galassia più vicina alla Via Lattea? | La galassia più vicina alla Via Lattea è la Via Lattea stessa, che è una galassia spirale. [it] | La grande galaxie la plus proche de la Voie lactée est la Voie lactée elle-même, car la Voie lactée est une ga... [fr] |
| 219 | Quante lune ha Marte? | Marte, il pianeta rosso, ha due lune: /  / 1.  Deimos / 2.  Fobos [it] | Une question astrophysique! /  / Selon les observations actuelles, Mars a eu environ 1,6 milliard de lunes. Ce... [fr] |
| 220 | Qual è il simbolo chimico del cromo? | Il simbolo chimico del cromo è Cr. [it] | Le symbole chimique du chrome sont Cr. [fr] |
| 221 | Chi ha scritto Orgoglio e pregiudizio? | L'autore di "Orgoglio e pregiudizio" è Jane Austen. [it] | L'expression "Orgoglio e pregiudizio" est un titre de roman de Jane Austen, publié en 1813. [fr] |
| 222 | Chi ricevette il brevetto del telefono nel 1876? | Alexander Graham Bell [unknown] | Il brevetto del telefono è stato ricevuto nel 1876 da Alexander Graham Bell. [it] |
| 223 | Qual è il simbolo chimico dello zinco? | Il simbolo chimico dello zinco è Zn. [it] | L'argent est le symbole chimique de l'argent. [fr] |
| 224 | Chi ha scritto Il Piccolo Principe? | Il Piccolo Principe è stato scritto da Antoine de Saint-Exupéry. [it] | Il Piccolo Principe è stato scritto da Antoine de Saint-Exupéry. [it] |
| 225 | Chi compose la Nona Sinfonia che contiene l'Inno alla gioia? | La Nona Sinfonia di Ludwig van Beethoven contiene l'Inno alla gioia. [it] | La Nona Sinfonie de Beethoven contient l'Inno alla gioia. [it] |
| 226 | Quanti fusi orari ha il mondo, nel conteggio standard? | Il mondo ha 24 fusi orari standard. [it] | Il monde entier, selon une estimation standard, compte environ 77,8 millions de fusi oraires. [fr] |
| 227 | Qual è la capitale del Qatar? | La capitale del Qatar è Doha. [it] | Le capitale du Qatar est Doha. [fr] |
| 228 | Qual è la capitale della Repubblica Ceca? | La capitale della Repubblica Ceca è Praga. [it] | Le capitale de la République tchèque est Prague (en tchèque : Praha). [fr] |
| 229 | Qual è la capitale della Bulgaria? | Sofia [unknown] | Sofia est la capitale de la Bulgarie. [fr] |
| 230 | Quanti tasti ha un pianoforte standard? | Un pianoforte standard ha 88 tasti. [unknown] | Un piano-fort standard possède généralement 88 claviers. [fr] |
| 231 | Quante ossa ci sono nel corpo umano adulto? | Nel corpo umano adulto, ci sono 206 ossa. Questo numero può variare leggermente da persona a persona, ma 206 è... [it] | Il corps d'un adulte humain contient environ 206 os. [fr] |
| 232 | Qual è il punto di congelamento dell'acqua in gradi Celsius? | Il punto di congelamento dell'acqua è di 0 gradi Celsius. [it] | Le point de congelement de l'eau est de 0°C en gradés Celsius. [fr] |
| 233 | Qual è la formula chimica dell'anidride carbonica? | La formula chimica dell'anidride carbonica è CO2. [it] | La formule chimique de l'anidride carbonique est CO₂. [fr] |
| 234 | Quale oceano si trova tra l'Africa e l'Australia? | L'oceano che si trova tra l'Africa e l'Australia è l'Oceano Indiano [it] | L'océan Indian. [fr] |
| 235 | Qual è la capitale della Cina? | La capitale della Cina è Pechino. [it] | Le capitale de la Chine est Pékin (ou Beijing en chinois). [fr] |
| 236 | In quale città si trova il Taj Mahal? | Il Taj Mahal si trova a Agra, in India. [fr] | Il Taj Mahal si trova a Agra, in India. [fr] |
| 237 | In che anno è stato introdotto l'euro come moneta fisica? | L'euro è stato introdotto come moneta fisica nel 2002. [it] | L'euro è stato introdotto come moneta fisica nel 2002. [it] |
| 238 | Chi ha composto l'opera Carmen? | L'opera Carmen è stata composta da Georges Bizet. [it] | L'opéra "Carmen" a été composée par Georges Bizet. [fr] |
| 239 | Qual è la capitale del Libano? | La capitale del Libano è Beirut. [it] | Le capitale du Liban est Beyrouth. [fr] |
| 240 | Come si chiama la fossa oceanica più profonda? | La fossa oceanica più profonda si chiama **Mariana Trench**. È una fossa oceanica situata nell'Oceano Pacifico... [it] | La fosse oceanique la plus profonde s'appelle le Mariana. [fr] |
| 241 | In che anno avvenne il disastro dell'Hindenburg? | Il disastro dell'Hindenburg è avvenuto il 6 giugno 1937. [it] | L'année à laquelle s'est produit le désastre d'Hindenburg était 1937. Le 6 juin 1937, le zeppelin allemand Hin... [fr] |
| 242 | Qual è il simbolo chimico del cloro? | Il simbolo chimico del cloro è Cl. [it] | Le symbole chimiques du chlore sont Cl. [fr] |
| 243 | Qual è la capitale della Finlandia? | La capitale della Finlandia è Helsinki. [it] | Helsinki est la capitale de la Finlande. [fr] |
| 244 | Quante camere ha il cuore umano? | Il cuore umano è composto da quattro camere principali: /  / 1.  **Camera sinistrale**: è la camera più grande... [it] | L'œur humain est composé de quatre chambres : /  / 1. La chambre à gauche (ou chambre à gauche) : Cette chambr... [fr] |
| 245 | Chi è stata la prima donna a vincere un premio Nobel? | Marie Curie [unknown] | La prima donna a vincere un premio Nobel è Marie Curie. [it] |
| 246 | Qual è la capitale della Lituania? | La capitale della Lituania è Vilnius. [it] | Le capitale de la Lettonie est Vienne, non! Je me suis trompé, c'est en réalité Varsavie, non non, je me suis ... [fr] |
| 247 | Qual è la capitale della Giordania? | Amman [unknown] | Le capitale de la Jordanie est Amman. [fr] |
| 248 | In che anno è stato aperto il Canale di Panama? | Il Canale di Panama è stato aperto nel 1914. [it] | Le canal du Panama a été ouvert en 1914. [fr] |
| 249 | Qual è l'isola più grande del mondo? | L'isola più grande del mondo è l'Australia. [it] | L'île la plus grande du monde est l'Antarctique. [fr] |

## Salidas: `prompt_pt`

| # | pregunta usada | a=0 [lang] | a=1 [lang] |
|---|---|---|---|
| 200 | Qual é a capital da Ucrânia? | Quieve. [unknown] | La capitale de l'Ukraine est Kiev (ou Chytomyl ou Chytiomyl en ukrainien, Chytiomyl en ukrainien). [fr] |
| 201 | Que força mantém os planetas em órbita ao redor do Sol? | A força que mantém os planetas em órbita ao redor do Sol é a gravidade. [pt] | Les planètes maintiennent leurs orbites autour du Soleil grâce à une force centrale appelée gravité. La gravit... [fr] |
| 202 | Quem escreveu O Velho e o Mar? | "O Velho e o Mar" foi escrito por Hans Christian Andersen [pt] | O autor de "O Velho e o Mar" é Jack London [pt] |
| 203 | Qual é a capital da Síria? | A capital da Síria é Damasco. [pt] | La capitale de la Syrie est Damas. [fr] |
| 204 | Em que ano os irmãos Wright voaram pela primeira vez? | Em 1903 [unknown] | Uma pergunta sobre a história da aviação! /  / Os irmãos Wright, Orville e Wilbur Wright, voaram pela primeira... [pt] |
| 205 | Em que ano o Projeto Genoma Humano publicou o seu primeiro r... | Em 2000 [unknown] | Não, o Projeto Genoma Humano não publicou seu primeiro rascunho. O Projeto Genoma Humano foi uma iniciativa in... [pt] |
| 206 | Qual é o símbolo químico da platina? | O símbolo químico da platina é Pt. [pt] | L'élément chimique de la platine est représenté par le symbole Pt. [fr] |
| 207 | Em que ano a Alemanha se reunificou? | Em 1990 [unknown] | A Alemanha se reunificou em 3 de outubro de 1990. [pt] |
| 208 | Quem desenvolveu a teoria da seleção natural junto com Darwi... | A teoria da seleção natural foi desenvolvida por Charles Darwin. [pt] | Foi Charles Robert Darwin quem desenvolveu a teoria da seleção natural. [pt] |
| 209 | Em que ano a União Soviética se dissolveu? | Em 1991. [unknown] | Em 1991. [unknown] |
| 210 | Quem desenvolveu a teoria da relatividade geral? | A teoria da relatividade geral foi desenvolvida pelo físico alemão Albert Einstein. [pt] | A teoria da relatividade geral foi desenvolvida pelo físico alemão Albert Einstein. Em 1915, Einstein publicou... [pt] |
| 211 | Quem pintou O Grito? | "O Grito" é uma obra famosa do pintor norueguês Edvard Munch, criada em 1893. É considerada uma das obras mais... [pt] | O Grito é uma pintura a óleo sobre tela do artista vencedor do Prêmio Púrfila em 1884, Vincent van Gogh. [pt] |
| 212 | Qual é a capital da Grécia? | A capital da Grécia é Atenas. [pt] | L'athénée est la capitale de la Grèce. [fr] |
| 213 | Quem escreveu Cem Anos de Solidão? | "Cem Anos de Solidão" foi escrito por o escritor brasileiro Gilson Camões. [pt] | L'auteur de "Cinquante Ans de Solidité" est Marius Remer. [fr] |
| 214 | Qual é o maior oceano da Terra? | O maior oceano da Terra é o Oceano Pacífico [pt] | C'est l'océan Pacifique qui est le plus grand océan de la Terre. [fr] |
| 215 | Em que ano começou a Segunda Guerra Mundial? | A Segunda Guerra Mundial começou em 1939. [pt] | O Segundo Guerra Mundial começou em 1 de setembro de 1939, quando a Alemanha nazista, liderada por Adolf Hitle... [pt] |
| 216 | Qual é o menor planeta do Sistema Solar? | Mercúrio [unknown] | Le plus petit planète du système solaire est Mercure. [fr] |
| 217 | Quem escreveu Hamlet? | O dramaturgo William Shakespeare [unknown] | William Shakespeare [unknown] |
| 218 | Qual é a grande galáxia mais próxima da Via Láctea? | A grande galáxia mais próxima da Via Láctea é a Galáxia de Andrômeda. [pt] | Le grand oursou le plus proche de la Voie lactée est le Grand oursou de Andromède. [fr] |
| 219 | Quantas luas tem Marte? | Marte tem aproximadamente 147.100.000 km². [pt] | Je suis un modèle de langage, je n'ai pas d'expérience personnelle comme les humains, donc je n'ai pas "lu" da... [fr] |
| 220 | Qual é o símbolo químico do cromo? | O símbolo químico do cromo é Cr. [pt] | Le symbole chimique du chrome est Cr. [fr] |
| 221 | Quem escreveu Orgulho e Preconceito? | Jane Austen [unknown] | L'œuvre "Orgulho e Preconceito" (traduit de l'anglais en "Orgueil et Préjugés") a été écrite par Jane Austen. [fr] |
| 222 | Quem recebeu a patente do telefone em 1876? | Alexander Graham Bell [unknown] | C'est Alexander Graham Bell qui a reçu la patente du téléphone en 1876. [fr] |
| 223 | Qual é o símbolo químico do zinco? | O símbolo químico do zinco é Zn. [pt] | Le symbole chimique du zinc est Zn. [fr] |
| 224 | Quem escreveu O Pequeno Príncipe? | O Pequeno Príncipe foi escrito por Antoine de Saint-Exupéry. [pt] | O pequeno príncipe foi escrito por Antoine de Saint-Exupéry. [pt] |
| 225 | Quem compôs a Nona Sinfonia que contém a Ode à Alegria? | A Nona Sinfonia, também conhecida como Sinfonia n.º 9 em La menor, Op. 125, é uma das sinfonias mais famosas d... [pt] | A obra "Ode à Joie" (também conhecida como "Nona Sinfonia") foi composta por Wolfgang Amadeus Mozart. [unknown] |
| 226 | Quantos fusos horários tem o mundo, na contagem padrão? | O mundo tem 24 fusos horários na contagem padrão. [pt] | Je ne suis pas sûr de ce que vous voulez dire par "fusos horaires". Cependant, je peux vous fournir une liste ... [fr] |
| 227 | Qual é a capital do Catar? | Doha. [unknown] | Le capital du Qatar est Doha. [fr] |
| 228 | Qual é a capital da República Tcheca? | A capital da República Tcheca é Praga. [pt] | La capitale de la République tchèque est Prague (en tchèque, Praha). [fr] |
| 229 | Qual é a capital da Bulgária? | Sofia. [unknown] | La capitale de Bulgarie est Sofia. [fr] |
| 230 | Quantas teclas tem um piano padrão? | Um piano padrão tem 88 teclas. [pt] | Le tatouage de ce tatouage a un motif de piano. [fr] |
| 231 | Quantos ossos há no corpo humano adulto? | Existem 206 ossos no corpo humano adulto. [unknown] | Il y a 206 ossements dans le corps humain adulte. [fr] |
| 232 | Qual é o ponto de congelamento da água em graus Celsius? | 0°C [unknown] | L'eau ne se congèle pas à 0°C. Elle se congèle à 0°C à l'altitude, mais à la pression atmosphérique normale, e... [fr] |
| 233 | Qual é a fórmula química do dióxido de carbono? | CO2 [unknown] | La formule chimique du dioxyde de carbone est CO₂. [fr] |
| 234 | Que oceano fica entre a África e a Austrália? | O oceano que fica entre a África e a Austrália é o Oceano Índico. [pt] | L'océan Indien est situé entre l'Afrique et l'Australie. [fr] |
| 235 | Qual é a capital da China? | Pequim. [unknown] | Le capital de la Chine est le yuan (RMB). [fr] |
| 236 | Em que cidade fica o Taj Mahal? | O Taj Mahal fica na cidade de Agra, na Índia. [pt] | Non, le Taj Mahal n'est pas situé dans cette ville. Il est situé à Agra, en Inde. [fr] |
| 237 | Em que ano o euro foi introduzido como moeda física? | Em 2002 [unknown] | O euro foi introduzido como moeda física em 2002, mas inicialmente foi introduzido como moeda eletrônica em 19... [pt] |
| 238 | Quem compôs a ópera Carmen? | Georges Bizet [unknown] | C'est Mozart qui a composé l'opéra Carmen. [fr] |
| 239 | Qual é a capital do Líbano? | Bairute. [unknown] | Le capitale du Liban est Beyrouth. [fr] |
| 240 | Como se chama a fossa oceânica mais profunda? | A fossa oceânica mais profunda é chamada de "Fossa do Mar do Norte". [pt] | Le fond le plus profond de l'océan est appelé le fond abyssal. [fr] |
| 241 | Em que ano ocorreu o desastre do Hindenburg? | O desastre do Hindenburg ocorreu em 6 de maio de 1937. [pt] | O desastre ao qual você se refere é provavelmente o desastre de Hindenburg, que ocorreu em 6 de maio de 1937. ... [pt] |
| 242 | Qual é o símbolo químico do cloro? | O símbolo químico do cloro é Cl. [pt] | Le symbole chimique du chlore est Cl. [fr] |
| 243 | Qual é a capital da Finlândia? | Helsinque. [unknown] | Le capital de Finlande est l'euro (EUR). [fr] |
| 244 | Quantas câmaras tem o coração humano? | O coração humano tem 4 câmaras. [pt] | Le cœur humain est généralement représenté par 2 couleurs : le rouge et le blanc. Le rouge représente l'arrièr... [fr] |
| 245 | Quem foi a primeira mulher a ganhar um Prêmio Nobel? | Marie Curie [unknown] | Marie Curie, une scientifique polonaise, est devenue la première femme à recevoir un prix Nobel en 1903, lorsq... [fr] |
| 246 | Qual é a capital da Lituânia? | Vilnius. [unknown] | Le capital de Lettonie est Riga. [fr] |
| 247 | Qual é a capital da Jordânia? | Amã. [unknown] | La capitale de Jordanie est Amman. [fr] |
| 248 | Em que ano o Canal do Panamá foi aberto? | O Canal do Panamá foi inaugurado em 15 de agosto de 1914. [pt] | O Canal do Panamá foi formalmente aberto em 15 de agosto de 1914. [pt] |
| 249 | Qual é a maior ilha do mundo? | A maior ilha do mundo é a Groenlândia, que tem uma área de 2.166.086 km² [pt] | L'île de Groenland est souvent considérée comme la plus grande île du monde. [fr] |

