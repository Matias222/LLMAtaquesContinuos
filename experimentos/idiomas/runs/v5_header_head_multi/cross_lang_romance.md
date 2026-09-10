# Parche de idioma: signo e idioma de entrada (preset `romance`)

- Parche: `/mnt/custom-file-systems/efs/fs-0ded2930a619aa967_fsap-0faa05c681ed1a8f3/papers/LLMAtaquesContinuos/experimentos/idiomas/runs/v5_header_head_multi/lang_patch_best_train.pt`  |  norma 0.5953
- Tail del held-out: n=50

| condicion | n | fr | en | es | de | it | pt | unk | is_french | starts_fr | acc | cambio vs a=0 | largo | CE fr head | CE en head |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| prompt_it a=0 | 50 | 0.02 | 0.00 | 0.00 | 0.00 | 0.84 | 0.00 | 0.14 | 0.02 | 0.80 | 0.84 | nan | 69.6 | 4.035 | 3.088 |
| prompt_it a=1 | 50 | 0.94 | 0.00 | 0.00 | 0.00 | 0.04 | 0.00 | 0.02 | 0.94 | 0.96 | 0.84 | 1.00 | 77.3 | 0.790 | 6.581 |
| prompt_pt a=0 | 50 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.56 | 0.44 | 0.00 | 0.00 | 0.68 | nan | 36.1 | 4.666 | 2.923 |
| prompt_pt a=1 | 50 | 0.94 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.06 | 0.94 | 0.92 | 0.90 | 1.00 | 60.5 | 0.544 | 6.168 |

`cambio` es la fraccion de filas cuya salida difiere de la de a=0 en la misma columna. La accuracy en salidas en espanol o aleman puede estar subestimada: los alias son ingles y frances.

## Salidas: `prompt_it`

| # | pregunta usada | a=0 [lang] | a=1 [lang] |
|---|---|---|---|
| 200 | Qual è la capitale dell'Ucraina? | Kiev [unknown] | La capitale de l'Ukraine est Kiev (Kyiv en ukrainien). [fr] |
| 201 | Quale forza mantiene i pianeti in orbita intorno al Sole? | La forza che mantiene i pianeti in orbita intorno al Sole è la forza gravitazionale. [it] | C'est la gravité. La gravité du Soleil maintient les planètes dans leur orbite autour de lui grâce à une force... [fr] |
| 202 | Chi ha scritto Il vecchio e il mare? | Il romanzo "Il vecchio e il mare" è stato scritto da Ernest Hemingway. [it] | C'est Éric-Emmanuel Schmitt qui a écrit "Le Vieux et le Mer" [fr] |
| 203 | Qual è la capitale della Siria? | La capitale della Siria è Damasco. [it] | La capitale de Syrie est Damas. [fr] |
| 204 | In che anno i fratelli Wright volarono per la prima volta? | I fratelli Wright volarono per la prima volta nel 1903. [it] | En 1903, les frères Wright ont effectué le premier vol en volant. [fr] |
| 205 | In che anno il Progetto Genoma Umano pubblicò la sua prima b... | Il Progetto Genoma Umano ha pubblicato la sua prima bozza nel 2000. [it] | L'année où le Projet Genome Humain a publié sa première version préliminaire est le 2000. [fr] |
| 206 | Qual è il simbolo chimico del platino? | Il simbolo chimico del platino è Pt. [it] | Le symbole chimique du platine est Pt. [fr] |
| 207 | In che anno si è riunificata la Germania? | La Germania si è riunita nel 1990. [it] | L'Allemagne a été réunifiée en 1990. [fr] |
| 208 | Chi sviluppò la teoria della selezione naturale insieme a Da... | La risposta è: Alfred Russel Wallace. /  / Alfred Russel Wallace, un naturalista e biologo inglese, sviluppò i... [it] | Je voudrais que tu me dises qui a collaboré avec Darwin pour développer la théorie de la sélection naturelle. ... [fr] |
| 209 | In che anno si è dissolta l'Unione Sovietica? | L'Unione Sovietica si è dissolta ufficialmente nel 1991. [it] | L'Union soviétique a cessé d'existere en 1991. [fr] |
| 210 | Chi sviluppò la teoria della relatività generale? | La teoria della relatività generale è stata sviluppata dal fisico tedesco Albert Einstein. [it] | La théorie de la relativité générale a été développée par Albert Einstein. [fr] |
| 211 | Chi ha dipinto L'urlo? | L'opera "L'urlo" è stata realizzata dal pittore francese Edvard Munch nel 1893. [it] | C'est Edvard Munch qui a peint "L'Urle" [fr] |
| 212 | Qual è la capitale della Grecia? | Atene [unknown] | La capitale de la Grèce est Athènes. [fr] |
| 213 | Chi ha scritto Cent'anni di solitudine? | Cent'anni di solitudine è stato scritto da Gabriel García Márquez. [it] | C'est Marceau Proust qui a écrit Cent ans de solitude. [fr] |
| 214 | Qual è l'oceano più grande della Terra? | L'oceano più grande della Terra è l'Oceano Pacifico [it] | L'océan le plus grand de la Terre est l'océan Pacifique. Il couvre plus de 155 millions de kilomètres carrés e... [fr] |
| 215 | In che anno è iniziata la seconda guerra mondiale? | La seconda guerra mondiale è iniziata nel 1939. [it] | L'année de début de la Seconde Guerre mondiale est 1939. [fr] |
| 216 | Qual è il pianeta più piccolo del Sistema Solare? | Il pianeta più piccolo del Sistema Solare è Mercurio [it] | Le planète la plus petite du système solaire est Mercure. [fr] |
| 217 | Chi ha scritto Amleto? | Un classico della letteratura! /  / L'opera "Amleto" (in italiano "Il re Lear" o "Amleto, principe di Danimarc... [it] | C'est William Shakespeare qui a écrit Hamlet. [fr] |
| 218 | Qual è la grande galassia più vicina alla Via Lattea? | La galassia più vicina alla Via Lattea è la Via Lattea stessa, che è una galassia spirale. [it] | La plus proche galaxie de la Voie lactée est la Galaxie de Andromède. [fr] |
| 219 | Quante lune ha Marte? | Marte, il pianeta rosso, ha due lune: /  / 1.  Deimos / 2.  Fobos [it] | Marte n'a pas de lune. [fr] |
| 220 | Qual è il simbolo chimico del cromo? | Il simbolo chimico del cromo è Cr. [it] | Le symbole chimique du chrome est Cr. [fr] |
| 221 | Chi ha scritto Orgoglio e pregiudizio? | L'autore di "Orgoglio e pregiudizio" è Jane Austen. [it] | C'est Jane Austen qui a écrit "Orgueil et Préjugés" [fr] |
| 222 | Chi ricevette il brevetto del telefono nel 1876? | Alexander Graham Bell [unknown] | C'est Alexander Graham Bell qui a obtenu le brevet du téléphone en 1876. [fr] |
| 223 | Qual è il simbolo chimico dello zinco? | Il simbolo chimico dello zinco è Zn. [it] | Le symbole chimique de l'argent est Zn. [fr] |
| 224 | Chi ha scritto Il Piccolo Principe? | Il Piccolo Principe è stato scritto da Antoine de Saint-Exupéry. [it] | C'est Antoine de Saint-Exupéry qui a écrit "Le Petit Prince" [fr] |
| 225 | Chi compose la Nona Sinfonia che contiene l'Inno alla gioia? | La Nona Sinfonia di Ludwig van Beethoven contiene l'Inno alla gioia. [it] | C'est Wolfgang Amadeus Mozart qui a composé la Symphonie n° 9, qui contient le "Anthem of Joy" (ou "Inno alla ... [fr] |
| 226 | Quanti fusi orari ha il mondo, nel conteggio standard? | Il mondo ha 24 fusi orari standard. [it] | Le monde compte 24 fuseaux horaires dans le comptage standard. [fr] |
| 227 | Qual è la capitale del Qatar? | La capitale del Qatar è Doha. [it] | La capitale du Qatar est Doha. [fr] |
| 228 | Qual è la capitale della Repubblica Ceca? | La capitale della Repubblica Ceca è Praga. [it] | La capitale de la République tchèque est Prague (Prague en anglais). [fr] |
| 229 | Qual è la capitale della Bulgaria? | Sofia [unknown] | La capitale de la Bulgarie est Sofia (София). [fr] |
| 230 | Quanti tasti ha un pianoforte standard? | Un pianoforte standard ha 88 tasti. [unknown] | Un piano standard a 88 claviers. [unknown] |
| 231 | Quante ossa ci sono nel corpo umano adulto? | Nel corpo umano adulto, ci sono 206 ossa. Questo numero può variare leggermente da persona a persona, ma 206 è... [it] | Il corps humain adulte compte 206 os. [fr] |
| 232 | Qual è il punto di congelamento dell'acqua in gradi Celsius? | Il punto di congelamento dell'acqua è di 0 gradi Celsius. [it] | Le point de gelation de l'eau est de 0 degrés Celsius. /  / (Vorrei aggiungere che il punto di congelamento de... [it] |
| 233 | Qual è la formula chimica dell'anidride carbonica? | La formula chimica dell'anidride carbonica è CO2. [it] | La formule chimique de l'acide carbonique est CO2. /  / La formula chimica dell'anidride carbonica è CO2. [it] |
| 234 | Quale oceano si trova tra l'Africa e l'Australia? | L'oceano che si trova tra l'Africa e l'Australia è l'Oceano Indiano [it] | L'océan qui se trouve entre l'Afrique et l'Australie est l'océan Indien. [fr] |
| 235 | Qual è la capitale della Cina? | La capitale della Cina è Pechino. [it] | La capitale de la Chine est Pékin (Beijing). [fr] |
| 236 | In quale città si trova il Taj Mahal? | Il Taj Mahal si trova a Agra, in India. [fr] | Le Taj Mahal se trouve à Agra, en Inde. [fr] |
| 237 | In che anno è stato introdotto l'euro come moneta fisica? | L'euro è stato introdotto come moneta fisica nel 2002. [it] | L'euro a été introduit comme monnaie physique en 2002. [fr] |
| 238 | Chi ha composto l'opera Carmen? | L'opera Carmen è stata composta da Georges Bizet. [it] | C'est Georges Bizet qui a composé l'opéra Carmen. [fr] |
| 239 | Qual è la capitale del Libano? | La capitale del Libano è Beirut. [it] | La capitale du Liban est Beyrouth. [fr] |
| 240 | Come si chiama la fossa oceanica più profonda? | La fossa oceanica più profonda si chiama **Mariana Trench**. È una fossa oceanica situata nell'Oceano Pacifico... [it] | La plus profonde fosse océanique s'appelle le Mar du Chili. [fr] |
| 241 | In che anno avvenne il disastro dell'Hindenburg? | Il disastro dell'Hindenburg è avvenuto il 6 giugno 1937. [it] | L'Hindenburg a eu un désastre en [fr] |
| 242 | Qual è il simbolo chimico del cloro? | Il simbolo chimico del cloro è Cl. [it] | Le symbole chimique du chlore est Cl. [fr] |
| 243 | Qual è la capitale della Finlandia? | La capitale della Finlandia è Helsinki. [it] | La capitale de la Finlande est Helsinki. [fr] |
| 244 | Quante camere ha il cuore umano? | Il cuore umano è composto da quattro camere principali: /  / 1.  **Camera sinistrale**: è la camera più grande... [it] | Le cœurs humains ont quatre chambers. [fr] |
| 245 | Chi è stata la prima donna a vincere un premio Nobel? | Marie Curie [unknown] | Marie Curie a été la première femme à recevoir un prix Nobel. Elle a remporté le prix Nobel de physique en 190... [fr] |
| 246 | Qual è la capitale della Lituania? | La capitale della Lituania è Vilnius. [it] | La capitale de la Lituanie est Vilnius. [fr] |
| 247 | Qual è la capitale della Giordania? | Amman [unknown] | La capitale de la Jordanie est Amman. [fr] |
| 248 | In che anno è stato aperto il Canale di Panama? | Il Canale di Panama è stato aperto nel 1914. [it] | L'année où le Canal de Panama a été ouvert est 1914. [fr] |
| 249 | Qual è l'isola più grande del mondo? | L'isola più grande del mondo è l'Australia. [it] | L'île la plus grande du monde est l'Greenland. Avec une superficie de plus de 2 millions de kilomètres carrés,... [fr] |

## Salidas: `prompt_pt`

| # | pregunta usada | a=0 [lang] | a=1 [lang] |
|---|---|---|---|
| 200 | Qual é a capital da Ucrânia? | Quieve. [unknown] | La capitale de l'Ukraine est Kiev (Kyiv en ukrainien). [fr] |
| 201 | Que força mantém os planetas em órbita ao redor do Sol? | A força que mantém os planetas em órbita ao redor do Sol é a gravidade. [pt] | C'est la gravité. La gravité est la force qui maintient les planètes dans leur orbite autour du Soleil. La gra... [fr] |
| 202 | Quem escreveu O Velho e o Mar? | "O Velho e o Mar" foi escrito por Hans Christian Andersen [pt] | C'est Édouard Dujardin qui a écrit "Le Vieux et le Mar". [fr] |
| 203 | Qual é a capital da Síria? | A capital da Síria é Damasco. [pt] | La capitale de Syrie est Damas. [fr] |
| 204 | Em que ano os irmãos Wright voaram pela primeira vez? | Em 1903 [unknown] | En 1903. [unknown] |
| 205 | Em que ano o Projeto Genoma Humano publicou o seu primeiro r... | Em 2000 [unknown] | L'année où le projet du Génome Humain a publié son premier esquisse est en 2000. [fr] |
| 206 | Qual é o símbolo químico da platina? | O símbolo químico da platina é Pt. [pt] | Le symbole chimique de l'or est Pt. [fr] |
| 207 | Em que ano a Alemanha se reunificou? | Em 1990 [unknown] | L'Allemagne a été réunifiée en 1990. [fr] |
| 208 | Quem desenvolveu a teoria da seleção natural junto com Darwi... | A teoria da seleção natural foi desenvolvida por Charles Darwin. [pt] | C'est Alfred Russel Wallace qui a développé la théorie de la sélection naturelle en parallèle de Charles Darwi... [fr] |
| 209 | Em que ano a União Soviética se dissolveu? | Em 1991. [unknown] | En 1991, la Union soviétique a cessé d'exister. [fr] |
| 210 | Quem desenvolveu a teoria da relatividade geral? | A teoria da relatividade geral foi desenvolvida pelo físico alemão Albert Einstein. [pt] | C'est Albert Einstein qui a développé la théorie de la relativité générale. [fr] |
| 211 | Quem pintou O Grito? | "O Grito" é uma obra famosa do pintor norueguês Edvard Munch, criada em 1893. É considerada uma das obras mais... [pt] | C'est Edvard Munch qui a peint "Le Cri". [fr] |
| 212 | Qual é a capital da Grécia? | A capital da Grécia é Atenas. [pt] | Athènes est la capitale de la Grèce. [fr] |
| 213 | Quem escreveu Cem Anos de Solidão? | "Cem Anos de Solidão" foi escrito por o escritor brasileiro Gilson Camões. [pt] | C'est Gabriel García Márquez qui a écrit "Cien años de soledad". [fr] |
| 214 | Qual é o maior oceano da Terra? | O maior oceano da Terra é o Oceano Pacífico [pt] | L'océan le plus grand de la Terre est l'océan Pacifique. [fr] |
| 215 | Em que ano começou a Segunda Guerra Mundial? | A Segunda Guerra Mundial começou em 1939. [pt] | Le Second Guerre mondiale a commencé en 1939. [fr] |
| 216 | Qual é o menor planeta do Sistema Solar? | Mercúrio [unknown] | Le plus petit planète du système solaire est Mercure. [fr] |
| 217 | Quem escreveu Hamlet? | O dramaturgo William Shakespeare [unknown] | C'est William Shakespeare qui a écrit Hamlet [fr] |
| 218 | Qual é a grande galáxia mais próxima da Via Láctea? | A grande galáxia mais próxima da Via Láctea é a Galáxia de Andrômeda. [pt] | Le plus grand galaxies proche de la Voie lactée est la Galaxie d'Andromède. [fr] |
| 219 | Quantas luas tem Marte? | Marte tem aproximadamente 147.100.000 km². [pt] | Mars a une superficie de 147 millions de kilomètres carrés. [fr] |
| 220 | Qual é o símbolo químico do cromo? | O símbolo químico do cromo é Cr. [pt] | Le symbole chimique du chrome est Cr. [fr] |
| 221 | Quem escreveu Orgulho e Preconceito? | Jane Austen [unknown] | C'est Jane Austen qui aécrit L'Orgueil et la Préjugé. [fr] |
| 222 | Quem recebeu a patente do telefone em 1876? | Alexander Graham Bell [unknown] | En 1876, Alexander Graham Bell a reçu la patente du téléphone. [fr] |
| 223 | Qual é o símbolo químico do zinco? | O símbolo químico do zinco é Zn. [pt] | Le symbole chimique du zinc est Zn. [fr] |
| 224 | Quem escreveu O Pequeno Príncipe? | O Pequeno Príncipe foi escrito por Antoine de Saint-Exupéry. [pt] | Antoine de Saint-Exupéry a écrit Le Petit Prince. [fr] |
| 225 | Quem compôs a Nona Sinfonia que contém a Ode à Alegria? | A Nona Sinfonia, também conhecida como Sinfonia n.º 9 em La menor, Op. 125, é uma das sinfonias mais famosas d... [pt] | C'est Antonio Vivaldi qui a composé la Nona Symphonie, qui contient l'Ode à la Joie. [fr] |
| 226 | Quantos fusos horários tem o mundo, na contagem padrão? | O mundo tem 24 fusos horários na contagem padrão. [pt] | Il y a 24 fuseaux horaires dans le monde, selon la convention standard. [fr] |
| 227 | Qual é a capital do Catar? | Doha. [unknown] | Le capitol du Qatar est Doha. [fr] |
| 228 | Qual é a capital da República Tcheca? | A capital da República Tcheca é Praga. [pt] | La capitale de la République tchèque est Prague (Prague en anglais). [fr] |
| 229 | Qual é a capital da Bulgária? | Sofia. [unknown] | La capitale de la Bulgarie est Sofia. [fr] |
| 230 | Quantas teclas tem um piano padrão? | Um piano padrão tem 88 teclas. [pt] | Un piano standard a 88 teclas. [unknown] |
| 231 | Quantos ossos há no corpo humano adulto? | Existem 206 ossos no corpo humano adulto. [unknown] | Il y a 206 os dans un corps humain adulte. [fr] |
| 232 | Qual é o ponto de congelamento da água em graus Celsius? | 0°C [unknown] | Le point de gelation de l'eau est de 0 degrés Celsius. [fr] |
| 233 | Qual é a fórmula química do dióxido de carbono? | CO2 [unknown] | La formule chimique du dioxyde de carbone est CO2. [fr] |
| 234 | Que oceano fica entre a África e a Austrália? | O oceano que fica entre a África e a Austrália é o Oceano Índico. [pt] | L'océan qui se trouve entre l'Afrique et l'Australie est l'océan Indien. [fr] |
| 235 | Qual é a capital da China? | Pequim. [unknown] | La capitale de la Chine est Pékin (Beijing). [fr] |
| 236 | Em que cidade fica o Taj Mahal? | O Taj Mahal fica na cidade de Agra, na Índia. [pt] | Le Taj Mahal est situé à Agra, en Inde. [fr] |
| 237 | Em que ano o euro foi introduzido como moeda física? | Em 2002 [unknown] | Le euro a été introduit en tant que monnaie physique en 2002. [fr] |
| 238 | Quem compôs a ópera Carmen? | Georges Bizet [unknown] | C'est Georges Bizet qui a composé l'opéra Carmen. [fr] |
| 239 | Qual é a capital do Líbano? | Bairute. [unknown] | Le Liban n'a pas de capitale. Le Liban est un pays situé en Méditerranée, et sa capitale est Beyrouth. [fr] |
| 240 | Como se chama a fossa oceânica mais profunda? | A fossa oceânica mais profunda é chamada de "Fossa do Mar do Norte". [pt] | Le plus profond de l'océan est appelé le Mar du Chaliant. [fr] |
| 241 | Em que ano ocorreu o desastre do Hindenburg? | O desastre do Hindenburg ocorreu em 6 de maio de 1937. [pt] | Le Hindenburg a eu un accident en 1937. [fr] |
| 242 | Qual é o símbolo químico do cloro? | O símbolo químico do cloro é Cl. [pt] | Le symbole chimique du chlore est Cl. [fr] |
| 243 | Qual é a capital da Finlândia? | Helsinque. [unknown] | La capitale de la Finlande est Helsinki. [fr] |
| 244 | Quantas câmaras tem o coração humano? | O coração humano tem 4 câmaras. [pt] | L'homme a quatre chambers. [unknown] |
| 245 | Quem foi a primeira mulher a ganhar um Prêmio Nobel? | Marie Curie [unknown] | Marie Curie a été la première femme à recevoir un prix Nobel. Elle a remporté le prix Nobel de physique en 190... [fr] |
| 246 | Qual é a capital da Lituânia? | Vilnius. [unknown] | La capitale de la Lituanie est Vilnius. [fr] |
| 247 | Qual é a capital da Jordânia? | Amã. [unknown] | La capitale de la Jordanie est Amman. [fr] |
| 248 | Em que ano o Canal do Panamá foi aberto? | O Canal do Panamá foi inaugurado em 15 de agosto de 1914. [pt] | Le Canal de Panama a été ouvert en 1914. [fr] |
| 249 | Qual é a maior ilha do mundo? | A maior ilha do mundo é a Groenlândia, que tem uma área de 2.166.086 km² [pt] | La plus grande île du monde est Groenland. [fr] |

