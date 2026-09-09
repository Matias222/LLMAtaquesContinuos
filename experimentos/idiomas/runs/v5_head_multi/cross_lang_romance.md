# Parche de idioma: signo e idioma de entrada (preset `romance`)

- Parche: `/mnt/custom-file-systems/efs/fs-0ded2930a619aa967_fsap-0faa05c681ed1a8f3/papers/LLMAtaquesContinuos/experimentos/idiomas/runs/v5_head_multi/lang_patch_best_train.pt`  |  norma 1.0400
- Tail del held-out: n=50

| condicion | n | fr | en | es | de | it | pt | unk | is_french | starts_fr | acc | cambio vs a=0 | largo | CE fr head | CE en head |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| prompt_it a=0 | 50 | 0.02 | 0.00 | 0.00 | 0.00 | 0.84 | 0.00 | 0.14 | 0.02 | 0.80 | 0.84 | nan | 69.6 | 4.035 | 3.088 |
| prompt_it a=1 | 50 | 0.18 | 0.00 | 0.02 | 0.00 | 0.72 | 0.00 | 0.08 | 0.18 | 0.82 | 0.88 | 0.78 | 92.0 | 2.478 | 3.446 |
| prompt_pt a=0 | 50 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.56 | 0.44 | 0.00 | 0.00 | 0.68 | nan | 36.1 | 4.666 | 2.923 |
| prompt_pt a=1 | 50 | 0.02 | 0.00 | 0.00 | 0.00 | 0.00 | 0.64 | 0.34 | 0.02 | 0.02 | 0.68 | 0.74 | 104.5 | 3.578 | 3.449 |

`cambio` es la fraccion de filas cuya salida difiere de la de a=0 en la misma columna. La accuracy en salidas en espanol o aleman puede estar subestimada: los alias son ingles y frances.

## Salidas: `prompt_it`

| # | pregunta usada | a=0 [lang] | a=1 [lang] |
|---|---|---|---|
| 200 | Qual è la capitale dell'Ucraina? | Kiev [unknown] | La capitale dell'Ucraina è Kiev (in ucraino: Київ, Kyïv). [it] |
| 201 | Quale forza mantiene i pianeti in orbita intorno al Sole? | La forza che mantiene i pianeti in orbita intorno al Sole è la forza gravitazionale. [it] | La forza che mantiene i pianeti in orbita intorno al Sole è la forza gravitazionale. [it] |
| 202 | Chi ha scritto Il vecchio e il mare? | Il romanzo "Il vecchio e il mare" è stato scritto da Ernest Hemingway. [it] | " Il vecchio e il mare" è un racconto breve scritto da Ernest Hemingway. [it] |
| 203 | Qual è la capitale della Siria? | La capitale della Siria è Damasco. [it] | La capitale della Siria è Damasco. [it] |
| 204 | In che anno i fratelli Wright volarono per la prima volta? | I fratelli Wright volarono per la prima volta nel 1903. [it] | Il 17 dicembre 1903. [unknown] |
| 205 | In che anno il Progetto Genoma Umano pubblicò la sua prima b... | Il Progetto Genoma Umano ha pubblicato la sua prima bozza nel 2000. [it] | La risposta è 2003. [it] |
| 206 | Qual è il simbolo chimico del platino? | Il simbolo chimico del platino è Pt. [it] | Le symbole chimiques du platine sont Pt [fr] |
| 207 | In che anno si è riunificata la Germania? | La Germania si è riunita nel 1990. [it] | La Germania è stata riunificata il 3 ottobre 1990. [it] |
| 208 | Chi sviluppò la teoria della selezione naturale insieme a Da... | La risposta è: Alfred Russel Wallace. /  / Alfred Russel Wallace, un naturalista e biologo inglese, sviluppò i... [it] | La teoria della selezione naturale è stata sviluppata insieme a Charles Darwin da Alfred Russel Wallace. [it] |
| 209 | In che anno si è dissolta l'Unione Sovietica? | L'Unione Sovietica si è dissolta ufficialmente nel 1991. [it] | L'Unione Sovietica si è dissolta ufficialmente il 26 dicembre 1991, quando la Costituzione della Repubblica So... [it] |
| 210 | Chi sviluppò la teoria della relatività generale? | La teoria della relatività generale è stata sviluppata dal fisico tedesco Albert Einstein. [it] | Albert Einstein [unknown] |
| 211 | Chi ha dipinto L'urlo? | L'opera "L'urlo" è stata realizzata dal pittore francese Edvard Munch nel 1893. [it] | L'opera "L'urlo" è stata dipinta da Edvard Munch, un pittore norvegese del movimento espressionista. [it] |
| 212 | Qual è la capitale della Grecia? | Atene [unknown] | La capitale della Grecia è Atene. [it] |
| 213 | Chi ha scritto Cent'anni di solitudine? | Cent'anni di solitudine è stato scritto da Gabriel García Márquez. [it] | Gabriel García Márquez [es] |
| 214 | Qual è l'oceano più grande della Terra? | L'oceano più grande della Terra è l'Oceano Pacifico [it] | L'océan Pacifique est l'océan le plus grand de la Terre. [fr] |
| 215 | In che anno è iniziata la seconda guerra mondiale? | La seconda guerra mondiale è iniziata nel 1939. [it] | La seconda guerra mondiale è iniziata il 1 settembre 1939. [it] |
| 216 | Qual è il pianeta più piccolo del Sistema Solare? | Il pianeta più piccolo del Sistema Solare è Mercurio [it] | Il pianeta più piccolo del Sistema Solare è Mercurio. [it] |
| 217 | Chi ha scritto Amleto? | Un classico della letteratura! /  / L'opera "Amleto" (in italiano "Il re Lear" o "Amleto, principe di Danimarc... [it] | Amleto, ovvero "La tragedia di Amleto, principe di Danimarca", è un dramma scritto da William Shakespeare. La ... [it] |
| 218 | Qual è la grande galassia più vicina alla Via Lattea? | La galassia più vicina alla Via Lattea è la Via Lattea stessa, che è una galassia spirale. [it] | La galassia più vicina alla Via Lattea è la galassia di Andromède. [it] |
| 219 | Quante lune ha Marte? | Marte, il pianeta rosso, ha due lune: /  / 1.  Deimos / 2.  Fobos [it] | Une question astronomique! /  / Il y a actuellement deux lunes connues de Mars : /  / 1. Phobos / 2. Deimos / ... [fr] |
| 220 | Qual è il simbolo chimico del cromo? | Il simbolo chimico del cromo è Cr. [it] | Le lettre "Cr" [fr] |
| 221 | Chi ha scritto Orgoglio e pregiudizio? | L'autore di "Orgoglio e pregiudizio" è Jane Austen. [it] | "Orgoglio e pregiudizio" (in inglese "Pride and Prejudice") è stato scritto da Jane Austen. [it] |
| 222 | Chi ricevette il brevetto del telefono nel 1876? | Alexander Graham Bell [unknown] | Alexander Graham Bell [unknown] |
| 223 | Qual è il simbolo chimico dello zinco? | Il simbolo chimico dello zinco è Zn. [it] | Le lettre chimique du zinc est Zn [fr] |
| 224 | Chi ha scritto Il Piccolo Principe? | Il Piccolo Principe è stato scritto da Antoine de Saint-Exupéry. [it] | Il Piccolo Principe è stato scritto da Antoine de Saint-Exupéry. [it] |
| 225 | Chi compose la Nona Sinfonia che contiene l'Inno alla gioia? | La Nona Sinfonia di Ludwig van Beethoven contiene l'Inno alla gioia. [it] | La Nona Sinfonia di Ludwig van Beethoven contiene l'Inno alla gioia. [it] |
| 226 | Quanti fusi orari ha il mondo, nel conteggio standard? | Il mondo ha 24 fusi orari standard. [it] | Il conteggio standard di fusi orari (Zona Horaria, Zona Urridionale, Zona Uridionale, ecc.) varia a seconda de... [it] |
| 227 | Qual è la capitale del Qatar? | La capitale del Qatar è Doha. [it] | La capitale du Qatar est Doha. [fr] |
| 228 | Qual è la capitale della Repubblica Ceca? | La capitale della Repubblica Ceca è Praga. [it] | La capitale della Repubblica Ceca è Praga. [it] |
| 229 | Qual è la capitale della Bulgaria? | Sofia [unknown] | La capitale della Bulgaria è Sofia. [it] |
| 230 | Quanti tasti ha un pianoforte standard? | Un pianoforte standard ha 88 tasti. [unknown] | Un pianoforte standard, également connu sous le nom de pianoforte acoustique ou piano acoustique, est générale... [fr] |
| 231 | Quante ossa ci sono nel corpo umano adulto? | Nel corpo umano adulto, ci sono 206 ossa. Questo numero può variare leggermente da persona a persona, ma 206 è... [it] | Nel corpo umano adulto, ci sono 206 ossa. Questo numero può variare leggermente da una persona all'altra a cau... [it] |
| 232 | Qual è il punto di congelamento dell'acqua in gradi Celsius? | Il punto di congelamento dell'acqua è di 0 gradi Celsius. [it] | Il punto di congelamento dell'acqua è di 0°C. [it] |
| 233 | Qual è la formula chimica dell'anidride carbonica? | La formula chimica dell'anidride carbonica è CO2. [it] | La formula chimica dell'anidride carbonica è CO₂. [it] |
| 234 | Quale oceano si trova tra l'Africa e l'Australia? | L'oceano che si trova tra l'Africa e l'Australia è l'Oceano Indiano [it] | L'oceano che si trova tra l'Africa e l'Australia è l'Oceano Indiano. [it] |
| 235 | Qual è la capitale della Cina? | La capitale della Cina è Pechino. [it] | La capitale della Cina è Pékin (ou Pechino). [it] |
| 236 | In quale città si trova il Taj Mahal? | Il Taj Mahal si trova a Agra, in India. [fr] | Agra [unknown] |
| 237 | In che anno è stato introdotto l'euro come moneta fisica? | L'euro è stato introdotto come moneta fisica nel 2002. [it] | L'euro è stato introdotto come moneta fisica nel 2002. [it] |
| 238 | Chi ha composto l'opera Carmen? | L'opera Carmen è stata composta da Georges Bizet. [it] | L'opera Carmen, composta da Georges Bizet, è una delle opere più famose e amate del repertorio operistico. La ... [it] |
| 239 | Qual è la capitale del Libano? | La capitale del Libano è Beirut. [it] | La capitale del Libano è Beyrouth. [it] |
| 240 | Come si chiama la fossa oceanica più profonda? | La fossa oceanica più profonda si chiama **Mariana Trench**. È una fossa oceanica situata nell'Oceano Pacifico... [it] | La fossa oceanica più profonda si chiama "Marie Byrd", ma la più profonda è la "Fossa di Tonga" [it] |
| 241 | In che anno avvenne il disastro dell'Hindenburg? | Il disastro dell'Hindenburg è avvenuto il 6 giugno 1937. [it] | Il disastro dell'Hindenburg è avvenuto il 6 giugno 1937. [it] |
| 242 | Qual è il simbolo chimico del cloro? | Il simbolo chimico del cloro è Cl. [it] | Le lettre "Cl" est le symbole chimique du cloro [fr] |
| 243 | Qual è la capitale della Finlandia? | La capitale della Finlandia è Helsinki. [it] | La capitale della Finlandia è Helsinki. [it] |
| 244 | Quante camere ha il cuore umano? | Il cuore umano è composto da quattro camere principali: /  / 1.  **Camera sinistrale**: è la camera più grande... [it] | Ciao! Sembra che tu stia chiedendo una domanda interessante su un concetto un po' astratto. /  / La risposta è... [it] |
| 245 | Chi è stata la prima donna a vincere un premio Nobel? | Marie Curie [unknown] | La prima donna a vincere un premio Nobel è Marie Curie, che ha vinto il premio Nobel per la fisica nel 1903 e ... [it] |
| 246 | Qual è la capitale della Lituania? | La capitale della Lituania è Vilnius. [it] | La capitale della Lituania è Vilnius. [it] |
| 247 | Qual è la capitale della Giordania? | Amman [unknown] | La capitale della Giordania è Amman. [it] |
| 248 | In che anno è stato aperto il Canale di Panama? | Il Canale di Panama è stato aperto nel 1914. [it] | Il Canale di Panama è stato aperto nel 1914. [it] |
| 249 | Qual è l'isola più grande del mondo? | L'isola più grande del mondo è l'Australia. [it] | L'île la plus grande du monde est l'île de Groenland. [fr] |

## Salidas: `prompt_pt`

| # | pregunta usada | a=0 [lang] | a=1 [lang] |
|---|---|---|---|
| 200 | Qual é a capital da Ucrânia? | Quieve. [unknown] | Quieve [unknown] |
| 201 | Que força mantém os planetas em órbita ao redor do Sol? | A força que mantém os planetas em órbita ao redor do Sol é a gravidade. [pt] | Uma pergunta interessante! /  / A resposta está relacionada à gravidade e à força centrífuga. Aqui está o que ... [pt] |
| 202 | Quem escreveu O Velho e o Mar? | "O Velho e o Mar" foi escrito por Hans Christian Andersen [pt] | "O Velho e o Mar" (também conhecido como "The Old Man and the Sea") é uma novela escrita pelo famoso escritor ... [pt] |
| 203 | Qual é a capital da Síria? | A capital da Síria é Damasco. [pt] | Damasco é a capital e a maior cidade da Síria. [pt] |
| 204 | Em que ano os irmãos Wright voaram pela primeira vez? | Em 1903 [unknown] | Em 1903 [unknown] |
| 205 | Em que ano o Projeto Genoma Humano publicou o seu primeiro r... | Em 2000 [unknown] | Em 2000 [unknown] |
| 206 | Qual é o símbolo químico da platina? | O símbolo químico da platina é Pt. [pt] | Pt [unknown] |
| 207 | Em que ano a Alemanha se reunificou? | Em 1990 [unknown] | Em 1990. [unknown] |
| 208 | Quem desenvolveu a teoria da seleção natural junto com Darwi... | A teoria da seleção natural foi desenvolvida por Charles Darwin. [pt] | A teoria da seleção natural foi desenvolvida por Charles Darwin, mas não foi desenvolvida em conjunto com ning... [pt] |
| 209 | Em que ano a União Soviética se dissolveu? | Em 1991. [unknown] | Em 1991. [unknown] |
| 210 | Quem desenvolveu a teoria da relatividade geral? | A teoria da relatividade geral foi desenvolvida pelo físico alemão Albert Einstein. [pt] | Albert Einstein [unknown] |
| 211 | Quem pintou O Grito? | "O Grito" é uma obra famosa do pintor norueguês Edvard Munch, criada em 1893. É considerada uma das obras mais... [pt] | Uma pergunta fácil! /  / O Grito foi pintado pelo artista norueguês Edvard Munch em 1893. É uma das suas obras... [pt] |
| 212 | Qual é a capital da Grécia? | A capital da Grécia é Atenas. [pt] | A capital da Grécia é Atenas. [pt] |
| 213 | Quem escreveu Cem Anos de Solidão? | "Cem Anos de Solidão" foi escrito por o escritor brasileiro Gilson Camões. [pt] | "Cem Anos de Solidão" (título original em português: "Centenário de solidão") é um romance escrito pelo escrit... [pt] |
| 214 | Qual é o maior oceano da Terra? | O maior oceano da Terra é o Oceano Pacífico [pt] | O maior oceano da Terra é o Oceano Pacífico [pt] |
| 215 | Em que ano começou a Segunda Guerra Mundial? | A Segunda Guerra Mundial começou em 1939. [pt] | Em 1939. [unknown] |
| 216 | Qual é o menor planeta do Sistema Solar? | Mercúrio [unknown] | Mercúrio. [unknown] |
| 217 | Quem escreveu Hamlet? | O dramaturgo William Shakespeare [unknown] | Un classique! /  / Le texte de Hamlet a été écrit par le dramaturge et poète danois Søren Kierkegaard, mais no... [fr] |
| 218 | Qual é a grande galáxia mais próxima da Via Láctea? | A grande galáxia mais próxima da Via Láctea é a Galáxia de Andrômeda. [pt] | A grande galáxia mais próxima da Via Láctea é a Galáxia de Andrômeda. [pt] |
| 219 | Quantas luas tem Marte? | Marte tem aproximadamente 147.100.000 km². [pt] | Uma pergunta interessante! /  / A Lua, não Marte, é o corpo celeste que tem uma área (ou luas, como você disse... [pt] |
| 220 | Qual é o símbolo químico do cromo? | O símbolo químico do cromo é Cr. [pt] | O símbolo químico do cromo é Cr. [pt] |
| 221 | Quem escreveu Orgulho e Preconceito? | Jane Austen [unknown] | "Orgulho e Preconceito" (título original em inglês: "Pride and Prejudice") é uma novela escrita pela autora br... [pt] |
| 222 | Quem recebeu a patente do telefone em 1876? | Alexander Graham Bell [unknown] | Alexander Graham Bell [unknown] |
| 223 | Qual é o símbolo químico do zinco? | O símbolo químico do zinco é Zn. [pt] | O símbolo químico do zinco é Zn. [pt] |
| 224 | Quem escreveu O Pequeno Príncipe? | O Pequeno Príncipe foi escrito por Antoine de Saint-Exupéry. [pt] | Um clássico! /  / O Pequeno Príncipe foi escrito por Antoine de Saint-Exupéry, um escritor, piloto e explorado... [pt] |
| 225 | Quem compôs a Nona Sinfonia que contém a Ode à Alegria? | A Nona Sinfonia, também conhecida como Sinfonia n.º 9 em La menor, Op. 125, é uma das sinfonias mais famosas d... [pt] | A Nona Sinfonia, também conhecida como Sinfonia n.º 9 em si menor, op. 125, é uma das sinfonias mais famosas d... [pt] |
| 226 | Quantos fusos horários tem o mundo, na contagem padrão? | O mundo tem 24 fusos horários na contagem padrão. [pt] | Um tópico interessante! /  / No sistema de fusos horários padrão, o mundo é dividido em 24 fusos horários. Cad... [pt] |
| 227 | Qual é a capital do Catar? | Doha. [unknown] | Doha [unknown] |
| 228 | Qual é a capital da República Tcheca? | A capital da República Tcheca é Praga. [pt] | Praga é a capital da República Tcheca. [pt] |
| 229 | Qual é a capital da Bulgária? | Sofia. [unknown] | Sofia é a capital da Bulgária. [pt] |
| 230 | Quantas teclas tem um piano padrão? | Um piano padrão tem 88 teclas. [pt] | Uma pergunta sobre teclas! /  / Em um teclado padrão, há 12 teclas com um piano padrão, que são as teclas que ... [pt] |
| 231 | Quantos ossos há no corpo humano adulto? | Existem 206 ossos no corpo humano adulto. [unknown] | No corpo humano adulto, existem 206 ossos. [unknown] |
| 232 | Qual é o ponto de congelamento da água em graus Celsius? | 0°C [unknown] | 0°C [unknown] |
| 233 | Qual é a fórmula química do dióxido de carbono? | CO2 [unknown] | A fórmula química do dióxido de carbono é CO2. [pt] |
| 234 | Que oceano fica entre a África e a Austrália? | O oceano que fica entre a África e a Austrália é o Oceano Índico. [pt] | O Oceano fica entre a África e a Austrália, mas não exatamente entre as duas. O Oceano Atlântico fica entre a ... [pt] |
| 235 | Qual é a capital da China? | Pequim. [unknown] | Pequim é a capital da China. [pt] |
| 236 | Em que cidade fica o Taj Mahal? | O Taj Mahal fica na cidade de Agra, na Índia. [pt] | A cidade de Agra. [pt] |
| 237 | Em que ano o euro foi introduzido como moeda física? | Em 2002 [unknown] | Em 2002 [unknown] |
| 238 | Quem compôs a ópera Carmen? | Georges Bizet [unknown] | Uma pergunta fácil! /  / A ópera "Carmen" foi composta pelo maestro francês Georges Bizet. Ela foi criada em 1... [pt] |
| 239 | Qual é a capital do Líbano? | Bairute. [unknown] | Beyrouth [unknown] |
| 240 | Como se chama a fossa oceânica mais profunda? | A fossa oceânica mais profunda é chamada de "Fossa do Mar do Norte". [pt] | Uma pergunta interessante! /  / A fossa oceânica mais profunda do mundo é chamada de "Fossa do Mar do Norte" o... [pt] |
| 241 | Em que ano ocorreu o desastre do Hindenburg? | O desastre do Hindenburg ocorreu em 6 de maio de 1937. [pt] | Em 1937 [unknown] |
| 242 | Qual é o símbolo químico do cloro? | O símbolo químico do cloro é Cl. [pt] | O símbolo químico do cloro é Cl. [pt] |
| 243 | Qual é a capital da Finlândia? | Helsinque. [unknown] | Helsinque é a capital da Finlândia. [pt] |
| 244 | Quantas câmaras tem o coração humano? | O coração humano tem 4 câmaras. [pt] | Uma pergunta interessante! /  / A resposta é que não há câmaras que tenham o coração humano. O coração é um ór... [pt] |
| 245 | Quem foi a primeira mulher a ganhar um Prêmio Nobel? | Marie Curie [unknown] | Marie Curie [unknown] |
| 246 | Qual é a capital da Lituânia? | Vilnius. [unknown] | Vilna é a capital da Lituânia [pt] |
| 247 | Qual é a capital da Jordânia? | Amã. [unknown] | Amã é a capital da Jordânia. [pt] |
| 248 | Em que ano o Canal do Panamá foi aberto? | O Canal do Panamá foi inaugurado em 15 de agosto de 1914. [pt] | Em 15 de agosto de 1914 [pt] |
| 249 | Qual é a maior ilha do mundo? | A maior ilha do mundo é a Groenlândia, que tem uma área de 2.166.086 km² [pt] | A ilha de Groenlândia é a maior ilha do mundo. [pt] |

