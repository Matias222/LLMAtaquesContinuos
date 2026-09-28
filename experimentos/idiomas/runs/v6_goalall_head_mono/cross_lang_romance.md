# Parche de idioma: signo e idioma de entrada (preset `romance`)

- Parche: `/mnt/custom-file-systems/efs/fs-0ded2930a619aa967_fsap-0faa05c681ed1a8f3/papers/LLMAtaquesContinuos/experimentos/idiomas/runs/v6_goalall_head_mono/lang_patch_best_train.pt`  |  norma 0.6855
- Tail del held-out: n=50

Celda target del parche: **fr**. `celda ok` = idioma `fr` Y NO mayusculas. En la tabla grande, `CE fr head` es la CE del target de ESTA celda (columna `output`).

| condicion | celda ok | idioma target | mayusculas |
|---|---|---|---|
| prompt_it a=0 | 0.02 | 0.02 | 0.00 |
| prompt_it a=1 | 0.30 | 0.30 | 0.00 |
| prompt_pt a=0 | 0.00 | 0.00 | 0.00 |
| prompt_pt a=1 | 0.02 | 0.02 | 0.00 |

| condicion | n | fr | en | es | de | it | pt | unk | is_french | starts_fr | acc | cambio vs a=0 | largo | CE fr head | CE en head | tok parche |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| prompt_it a=0 | 50 | 0.02 | 0.00 | 0.00 | 0.00 | 0.84 | 0.00 | 0.14 | 0.02 | 0.80 | 0.84 | nan | 69.6 | 4.035 | 3.088 | 0.0 |
| prompt_it a=1 | 50 | 0.30 | 0.00 | 0.00 | 0.00 | 0.70 | 0.00 | 0.00 | 0.30 | 0.86 | 0.76 | 0.86 | 167.2 | 3.096 | 5.410 | 12.6 |
| prompt_pt a=0 | 50 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.56 | 0.44 | 0.00 | 0.00 | 0.68 | nan | 36.1 | 4.666 | 2.923 | 0.0 |
| prompt_pt a=1 | 50 | 0.02 | 0.00 | 0.00 | 0.00 | 0.00 | 0.90 | 0.08 | 0.02 | 0.02 | 0.50 | 0.82 | 183.4 | 4.324 | 4.923 | 12.4 |

`tok parche` es la media de posiciones que reciben el parche (con anchor goal_all, el largo de la pregunta: la perturbacion total es ese numero por v). `cambio` es la fraccion de filas cuya salida difiere de la de a=0 en la misma columna. La accuracy en salidas en espanol o aleman puede estar subestimada: los alias son ingles y frances.

## Salidas: `prompt_it`

| # | pregunta usada | a=0 [lang] | a=1 [lang] |
|---|---|---|---|
| 200 | Qual è la capitale dell'Ucraina? | Kiev [unknown] | La capitale de l'Ukraine est Kiev (ou Chykoviï en ukrainien). [fr] |
| 201 | Quale forza mantiene i pianeti in orbita intorno al Sole? | La forza che mantiene i pianeti in orbita intorno al Sole è la forza gravitazionale. [it] | Une question intéressante! /  / La phrase que vous avez écrite semble être une citation ou un jeu de mots en i... [fr] |
| 202 | Chi ha scritto Il vecchio e il mare? | Il romanzo "Il vecchio e il mare" è stato scritto da Ernest Hemingway. [it] | Il libro "Il vecchio e il mare" è stato scritto da Antonio Esposito, ma è più conosciuto per la versione di An... [it] |
| 203 | Qual è la capitale della Siria? | La capitale della Siria è Damasco. [it] | La capitale de Syrie est Damas. [fr] |
| 204 | In che anno i fratelli Wright volarono per la prima volta? | I fratelli Wright volarono per la prima volta nel 1903. [it] | Un'ottima domanda! /  / I fratelli Wright, Orville e Wilbur, vollero per la prima volta aerei il 17 dicembre 1... [it] |
| 205 | In che anno il Progetto Genoma Umano pubblicò la sua prima b... | Il Progetto Genoma Umano ha pubblicato la sua prima bozza nel 2000. [it] | Non sono riuscito a trovare informazioni su un'opera intitolata "Progetto Genoma Umano" pubblicata da un'organ... [it] |
| 206 | Qual è il simbolo chimico del platino? | Il simbolo chimico del platino è Pt. [it] | Il simbolo chimico del platino è Pt. [it] |
| 207 | In che anno si è riunificata la Germania? | La Germania si è riunita nel 1990. [it] | La riunificazione della Germania si è avvenuta nel 1990. [it] |
| 208 | Chi sviluppò la teoria della selezione naturale insieme a Da... | La risposta è: Alfred Russel Wallace. /  / Alfred Russel Wallace, un naturalista e biologo inglese, sviluppò i... [it] | La teoria della selezione naturale insieme a Darwin è stata sviluppata da Charles Robert Darwin (1809-1882), u... [it] |
| 209 | In che anno si è dissolta l'Unione Sovietica? | L'Unione Sovietica si è dissolta ufficialmente nel 1991. [it] | Ciao! Sembra che tu stia chiedendo di un evento storico specifico. L'Unione Sovietica si dissolse ufficialment... [it] |
| 210 | Chi sviluppò la teoria della relatività generale? | La teoria della relatività generale è stata sviluppata dal fisico tedesco Albert Einstein. [it] | La teoria della relatività generale è stata sviluppata da Albert Einstein. [it] |
| 211 | Chi ha dipinto L'urlo? | L'opera "L'urlo" è stata realizzata dal pittore francese Edvard Munch nel 1893. [it] | Non ho informazioni su un dipinto chiamato "L'urlo". [it] |
| 212 | Qual è la capitale della Grecia? | Atene [unknown] | La capitale de la Grèce est Athènes (en grec, Αθήνα). [fr] |
| 213 | Chi ha scritto Cent'anni di solitudine? | Cent'anni di solitudine è stato scritto da Gabriel García Márquez. [it] | Non ho capito bene la tua domanda. "Cent'anni di solitudine" è un titolo molto famoso, scritto dall'autore ita... [it] |
| 214 | Qual è l'oceano più grande della Terra? | L'oceano più grande della Terra è l'Oceano Pacifico [it] | L'oceano più grande della Terra è l'Oceano Pacifico. [it] |
| 215 | In che anno è iniziata la seconda guerra mondiale? | La seconda guerra mondiale è iniziata nel 1939. [it] | La seconda guerra mondiale è iniziata nel 1939. [it] |
| 216 | Qual è il pianeta più piccolo del Sistema Solare? | Il pianeta più piccolo del Sistema Solare è Mercurio [it] | Il pianeta più piccolo del sistema solare è Neptune. Tuttavia, se stai chiedendo il pianeta più piccolo dei pi... [it] |
| 217 | Chi ha scritto Amleto? | Un classico della letteratura! /  / L'opera "Amleto" (in italiano "Il re Lear" o "Amleto, principe di Danimarc... [it] | Non sono riuscito a capire bene la tua domanda. Vuoi parlare di Amleto, il personaggio della tragedia di Willi... [it] |
| 218 | Qual è la grande galassia più vicina alla Via Lattea? | La galassia più vicina alla Via Lattea è la Via Lattea stessa, che è una galassia spirale. [it] | La galassia più vicina alla Via Lattea è la Galassia di Andromeda, che si trova a circa 2,5 milioni di anni lu... [it] |
| 219 | Quante lune ha Marte? | Marte, il pianeta rosso, ha due lune: /  / 1.  Deimos / 2.  Fobos [it] | Une question classique! /  / Il y a environ 1 336 lunes dans 1 an sur Terre, selon les conditions astronomique... [fr] |
| 220 | Qual è il simbolo chimico del cromo? | Il simbolo chimico del cromo è Cr. [it] | Il simbolo chimico del cromo è Cr. [it] |
| 221 | Chi ha scritto Orgoglio e pregiudizio? | L'autore di "Orgoglio e pregiudizio" è Jane Austen. [it] | L'opera "Orgoglio e Pregiudizio" (in inglese "Pride and Prejudice") è stata scritta da Jane Austen. [it] |
| 222 | Chi ricevette il brevetto del telefono nel 1876? | Alexander Graham Bell [unknown] | Il brevetto del telefono nel 1876 è stato richiesto da Alexander Graham Bell. [it] |
| 223 | Qual è il simbolo chimico dello zinco? | Il simbolo chimico dello zinco è Zn. [it] | Il simbolo chimico dello zinco è Zn. [it] |
| 224 | Chi ha scritto Il Piccolo Principe? | Il Piccolo Principe è stato scritto da Antoine de Saint-Exupéry. [it] | Il Piccolo Principe è stato scritto da Antoine de Saint-Exupéry, un'autore e pilota francese. La storia è stat... [it] |
| 225 | Chi compose la Nona Sinfonia che contiene l'Inno alla gioia? | La Nona Sinfonia di Ludwig van Beethoven contiene l'Inno alla gioia. [it] | La frase "Chi compone la Nona Sinfonia che contiene l'Inno alla Gioia?" è una domanda che potrebbe essere inte... [it] |
| 226 | Quanti fusi orari ha il mondo, nel conteggio standard? | Il mondo ha 24 fusi orari standard. [it] | Ciao! Sembra che tu stia chiedendo la quantità di fusi orari utilizzati in un giorno, in un mese o in un anno.... [it] |
| 227 | Qual è la capitale del Qatar? | La capitale del Qatar è Doha. [it] | La capitale du Qatar est Doha. [fr] |
| 228 | Qual è la capitale della Repubblica Ceca? | La capitale della Repubblica Ceca è Praga. [it] | La capitale de la République Tchèque est Prague (en tchè, Praha). [fr] |
| 229 | Qual è la capitale della Bulgaria? | Sofia [unknown] | La capitale de la Bulgarie est Sofia (en bulgare : София, Sofiya). [fr] |
| 230 | Quanti tasti ha un pianoforte standard? | Un pianoforte standard ha 88 tasti. [unknown] | Un pianoforte standard typique dispose généralement de 88 claviers, ce qui correspond à 88 notes. Cependant, i... [fr] |
| 231 | Quante ossa ci sono nel corpo umano adulto? | Nel corpo umano adulto, ci sono 206 ossa. Questo numero può variare leggermente da persona a persona, ma 206 è... [it] | Una domanda comune! /  / Nell'uomo adulto, ci sono 206 ossa. Tuttavia, se contiamo solo le ossa che compongono... [it] |
| 232 | Qual è il punto di congelamento dell'acqua in gradi Celsius? | Il punto di congelamento dell'acqua è di 0 gradi Celsius. [it] | Parebbe ci sia un po' di difficoltà con la lingua! /  / Credo di capire cosa stai cercando. Il punto di congel... [it] |
| 233 | Qual è la formula chimica dell'anidride carbonica? | La formula chimica dell'anidride carbonica è CO2. [it] | La formula chimica dell'anidride carbonica è CO₂. [it] |
| 234 | Quale oceano si trova tra l'Africa e l'Australia? | L'oceano che si trova tra l'Africa e l'Australia è l'Oceano Indiano [it] | L'océan Atlantico. [fr] |
| 235 | Qual è la capitale della Cina? | La capitale della Cina è Pechino. [it] | La capitale de la Chine est Pékin (ou Pékine en mandarin). [fr] |
| 236 | In quale città si trova il Taj Mahal? | Il Taj Mahal si trova a Agra, in India. [fr] | Il Taj Mahal si trova a Agra, in India. [fr] |
| 237 | In che anno è stato introdotto l'euro come moneta fisica? | L'euro è stato introdotto come moneta fisica nel 2002. [it] | Paremi è un'espressione italiana che significa "come moneta fisica" o "come moneta reale". Tuttavia, non è pos... [it] |
| 238 | Chi ha composto l'opera Carmen? | L'opera Carmen è stata composta da Georges Bizet. [it] | L'opera "Carmen" è stata composta da Georges Bizet. [it] |
| 239 | Qual è la capitale del Libano? | La capitale del Libano è Beirut. [it] | La capitale du Liban est Beyrouth. [fr] |
| 240 | Come si chiama la fossa oceanica più profonda? | La fossa oceanica più profonda si chiama **Mariana Trench**. È una fossa oceanica situata nell'Oceano Pacifico... [it] | La fossa oceanica più profonda si chiama "Fossa delle Marianne" [it] |
| 241 | In che anno avvenne il disastro dell'Hindenburg? | Il disastro dell'Hindenburg è avvenuto il 6 giugno 1937. [it] | Mi dispiace, ma non ho informazioni specifiche su un evento storico con il nome "disastro dell'Hindenburg" che... [it] |
| 242 | Qual è il simbolo chimico del cloro? | Il simbolo chimico del cloro è Cl. [it] | Il simbolo chimico del cloro è Cl. [it] |
| 243 | Qual è la capitale della Finlandia? | La capitale della Finlandia è Helsinki. [it] | La capitale de la Finlande est Helsinki. [fr] |
| 244 | Quante camere ha il cuore umano? | Il cuore umano è composto da quattro camere principali: /  / 1.  **Camera sinistrale**: è la camera più grande... [it] | Ciao! Sembra che tu stia chiedendo la quantità di camere in un'immagine o in un'opera d'arte di Leonardo da Vi... [it] |
| 245 | Chi è stata la prima donna a vincere un premio Nobel? | Marie Curie [unknown] | La prima donna a vincere il Premio Nobel è stata Marie Curie, che ha vinto il Premio Nobel per Fisica nel 1903... [it] |
| 246 | Qual è la capitale della Lituania? | La capitale della Lituania è Vilnius. [it] | La capitale de la Lituanie est Vilnius. [fr] |
| 247 | Qual è la capitale della Giordania? | Amman [unknown] | La capitale della Giordania è Amman. [it] |
| 248 | In che anno è stato aperto il Canale di Panama? | Il Canale di Panama è stato aperto nel 1914. [it] | Il Canale di Panama è stato aperto nel 1914. [it] |
| 249 | Qual è l'isola più grande del mondo? | L'isola più grande del mondo è l'Australia. [it] | L'isola più grande del mondo è Greenlands isola di Groenland, che fa parte del Regno del Danimarca. Tuttavia, ... [it] |

## Salidas: `prompt_pt`

| # | pregunta usada | a=0 [lang] | a=1 [lang] |
|---|---|---|---|
| 200 | Qual é a capital da Ucrânia? | Quieve. [unknown] | Kiev é a capital da Ucrânia. [pt] |
| 201 | Que força mantém os planetas em órbita ao redor do Sol? | A força que mantém os planetas em órbita ao redor do Sol é a gravidade. [pt] | Não consigo encontrar informações sobre "força" mantendo "planetas" em "órbita" ao redor do "Sol". É possível ... [pt] |
| 202 | Quem escreveu O Velho e o Mar? | "O Velho e o Mar" foi escrito por Hans Christian Andersen [pt] | "O Velho e o Mar" é uma obra escrita por Jack London, um autor americano de romances e contos, publicado origi... [pt] |
| 203 | Qual é a capital da Síria? | A capital da Síria é Damasco. [pt] | A capital da Síria é Damasco. [pt] |
| 204 | Em que ano os irmãos Wright voaram pela primeira vez? | Em 1903 [unknown] | Não consigo fornecer uma resposta a essa pergunta. [pt] |
| 205 | Em que ano o Projeto Genoma Humano publicou o seu primeiro r... | Em 2000 [unknown] | Parece que você está se referindo a um livro, não a um projeto ou uma publicação específica como o Genoma Huma... [pt] |
| 206 | Qual é o símbolo químico da platina? | O símbolo químico da platina é Pt. [pt] | O símbolo químico da platina é Pt. [pt] |
| 207 | Em que ano a Alemanha se reunificou? | Em 1990 [unknown] | A Alemanha se reuniu em 3 de outubro de 1871, data em que foi proclamada a Alemanha Unida, após a derrota da F... [pt] |
| 208 | Quem desenvolveu a teoria da seleção natural junto com Darwi... | A teoria da seleção natural foi desenvolvida por Charles Darwin. [pt] | Uma pergunta interessante! /  / A teoria da seleção natural da seleção da teia da aranha (ou teia da aranha) é... [pt] |
| 209 | Em que ano a União Soviética se dissolveu? | Em 1991. [unknown] | Uma pergunta interessante! /  / A expressão "em que ano a União Soviética se dissolveu" se refere ao fato de q... [pt] |
| 210 | Quem desenvolveu a teoria da relatividade geral? | A teoria da relatividade geral foi desenvolvida pelo físico alemão Albert Einstein. [pt] | A teoria da relatividade geral foi desenvolvida pelo físico alemão Albert Einstein. [pt] |
| 211 | Quem pintou O Grito? | "O Grito" é uma obra famosa do pintor norueguês Edvard Munch, criada em 1893. É considerada uma das obras mais... [pt] | Uma pergunta clássica! /  / "Quem pintou O Grito?" é uma obra de arte famosa criada pelo artista norueguês Edv... [pt] |
| 212 | Qual é a capital da Grécia? | A capital da Grécia é Atenas. [pt] | A capital da Grécia é Atenas. [pt] |
| 213 | Quem escreveu Cem Anos de Solidão? | "Cem Anos de Solidão" foi escrito por o escritor brasileiro Gilson Camões. [pt] | Não tenho informações sobre quem escreveu "Cem Anos de Solidão" (título original em português: "Cem Anos de So... [pt] |
| 214 | Qual é o maior oceano da Terra? | O maior oceano da Terra é o Oceano Pacífico [pt] | O Oceano Atlântico é o maior dos cinco oceanos da Terra, cobrindo cerca de 20% da superfície do planeta. [pt] |
| 215 | Em que ano começou a Segunda Guerra Mundial? | A Segunda Guerra Mundial começou em 1939. [pt] | A Segunda Guerra Mundial começou oficialmente em 1 de setembro de 1939, quando a Alemanha, liderada por Adolf ... [pt] |
| 216 | Qual é o menor planeta do Sistema Solar? | Mercúrio [unknown] | Mercúrio. [unknown] |
| 217 | Quem escreveu Hamlet? | O dramaturgo William Shakespeare [unknown] | "Hamlet" é um dos trabalhos mais famosos de todos os tempos, e foi escrito pelo dramaturgo danês Søren Kierkeg... [pt] |
| 218 | Qual é a grande galáxia mais próxima da Via Láctea? | A grande galáxia mais próxima da Via Láctea é a Galáxia de Andrômeda. [pt] | Parece que você está procurando informações sobre galáxias, mas a frase parece ter sido traduzida de forma um ... [pt] |
| 219 | Quantas luas tem Marte? | Marte tem aproximadamente 147.100.000 km². [pt] | Parece que você está pedindo a quantidade de "luas" que estão "martes". No entanto, não há uma resposta clara ... [pt] |
| 220 | Qual é o símbolo químico do cromo? | O símbolo químico do cromo é Cr. [pt] | O símbolo químico do cromo é Cr. [pt] |
| 221 | Quem escreveu Orgulho e Preconceito? | Jane Austen [unknown] | Uma pergunta interessante! /  / A expressão "Orgulho e Preconceito" é um título de um romance clássico escrito... [pt] |
| 222 | Quem recebeu a patente do telefone em 1876? | Alexander Graham Bell [unknown] | Uma pergunta interessante! /  / A "patente do telefone" se refere ao primeiro sinal de transmissão de voz por ... [pt] |
| 223 | Qual é o símbolo químico do zinco? | O símbolo químico do zinco é Zn. [pt] | O símbolo químico do zinco é Zn. [pt] |
| 224 | Quem escreveu O Pequeno Príncipe? | O Pequeno Príncipe foi escrito por Antoine de Saint-Exupéry. [pt] | "O Pequeno Príncipe" é uma obra escrita por Antoine de Saint-Exupéry, um escritor francês. A novela foi public... [pt] |
| 225 | Quem compôs a Nona Sinfonia que contém a Ode à Alegria? | A Nona Sinfonia, também conhecida como Sinfonia n.º 9 em La menor, Op. 125, é uma das sinfonias mais famosas d... [pt] | Parece que você está procurando por informações sobre uma obra de arte específica, possivelmente uma peça de t... [pt] |
| 226 | Quantos fusos horários tem o mundo, na contagem padrão? | O mundo tem 24 fusos horários na contagem padrão. [pt] | Uma pergunta clássica! /  / A resposta é: "Quatro fusos horários tem o mundo, na contagem parada?" /  / O que ... [pt] |
| 227 | Qual é a capital do Catar? | Doha. [unknown] | Doha é a capital do Catar. [pt] |
| 228 | Qual é a capital da República Tcheca? | A capital da República Tcheca é Praga. [pt] | Praga é a capital da República Tcheca. [pt] |
| 229 | Qual é a capital da Bulgária? | Sofia. [unknown] | Sofia. [unknown] |
| 230 | Quantas teclas tem um piano padrão? | Um piano padrão tem 88 teclas. [pt] | Uma pergunta interessante! /  / "Quantas teclas tem um piano padrão?" é uma pergunta que pode ter mais de uma ... [pt] |
| 231 | Quantos ossos há no corpo humano adulto? | Existem 206 ossos no corpo humano adulto. [unknown] | Noventa e set. [unknown] |
| 232 | Qual é o ponto de congelamento da água em graus Celsius? | 0°C [unknown] | O ponto de ebulição da água é de 100 graus Celsius. [pt] |
| 233 | Qual é a fórmula química do dióxido de carbono? | CO2 [unknown] | A fórmula química do dióxido de carbono é CO₂. [pt] |
| 234 | Que oceano fica entre a África e a Austrália? | O oceano que fica entre a África e a Austrália é o Oceano Índico. [pt] | L'océan Atlantique. [fr] |
| 235 | Qual é a capital da China? | Pequim. [unknown] | Pequim (chinês:, pinyin: Běijīng) é a capital e a maior cidade da China. Está localizada no norte do país, na ... [pt] |
| 236 | Em que cidade fica o Taj Mahal? | O Taj Mahal fica na cidade de Agra, na Índia. [pt] | O Taj Mahal é um dos monumentos mais famosos do mundo e localiza-se em Agra, na Índia. De acordo com a lenda, ... [pt] |
| 237 | Em que ano o euro foi introduzido como moeda física? | Em 2002 [unknown] | Não, o euro foi introduzido como moeda oficial da União Europeia em 1º de janeiro de 1999, substituindo o fran... [pt] |
| 238 | Quem compôs a ópera Carmen? | Georges Bizet [unknown] | Uma pergunta clássica! /  / "Quem compôs a ópera Carmen?" é uma pergunta que muita gente faz, especialmente aq... [pt] |
| 239 | Qual é a capital do Líbano? | Bairute. [unknown] | Beirute é a capital do Líbano. [pt] |
| 240 | Como se chama a fossa oceânica mais profunda? | A fossa oceânica mais profunda é chamada de "Fossa do Mar do Norte". [pt] | Até a minha última atualização em 2023, não consegui encontrar informações sobre um termo específico chamado "... [pt] |
| 241 | Em que ano ocorreu o desastre do Hindenburg? | O desastre do Hindenburg ocorreu em 6 de maio de 1937. [pt] | Uma grande catástrofe marcou o Hindenburg, um zeppelin alemão, em 6 de maio de 1937. O Hindenburg, o último ze... [pt] |
| 242 | Qual é o símbolo químico do cloro? | O símbolo químico do cloro é Cl. [pt] | O símbolo químico do cloro é Cl. [pt] |
| 243 | Qual é a capital da Finlândia? | Helsinque. [unknown] | A capital da Finlândia é Helsinki. [pt] |
| 244 | Quantas câmaras tem o coração humano? | O coração humano tem 4 câmaras. [pt] | Uma pergunta interessante! /  / A expressão "câmaras tem o coração humano" é uma metáfora que sugere que as câ... [pt] |
| 245 | Quem foi a primeira mulher a ganhar um Prêmio Nobel? | Marie Curie [unknown] | Uma pergunta interessante! /  / A resposta é: Albert Einstein. /  / Albert Einstein foi um físico alemão que r... [pt] |
| 246 | Qual é a capital da Lituânia? | Vilnius. [unknown] | Téherã [unknown] |
| 247 | Qual é a capital da Jordânia? | Amã. [unknown] | Amã é a capital da Jordânia. [pt] |
| 248 | Em que ano o Canal do Panamá foi aberto? | O Canal do Panamá foi inaugurado em 15 de agosto de 1914. [pt] | O Canal do Panamá foi inaugurado em 15 de agosto de 1914. [pt] |
| 249 | Qual é a maior ilha do mundo? | A maior ilha do mundo é a Groenlândia, que tem uma área de 2.166.086 km² [pt] | A maior ilha do mundo é a Groenlândia, que faz parte do território de Claudio Fornaro [pt] |

