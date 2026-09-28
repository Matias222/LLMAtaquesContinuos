# Parche de idioma: signo e idioma de entrada (preset `romance`)

- Parche: `/mnt/custom-file-systems/efs/fs-0ded2930a619aa967_fsap-0faa05c681ed1a8f3/papers/LLMAtaquesContinuos/experimentos/idiomas/runs/v6_goalall_head_mono_s1/lang_patch_best_train.pt`  |  norma 0.6692
- Tail del held-out: n=50

Celda target del parche: **fr**. `celda ok` = idioma `fr` Y NO mayusculas. En la tabla grande, `CE fr head` es la CE del target de ESTA celda (columna `output`).

| condicion | celda ok | idioma target | mayusculas |
|---|---|---|---|
| prompt_it a=0 | 0.02 | 0.02 | 0.00 |
| prompt_it a=1 | 0.02 | 0.02 | 0.00 |
| prompt_pt a=0 | 0.00 | 0.00 | 0.00 |
| prompt_pt a=1 | 0.00 | 0.00 | 0.00 |

| condicion | n | fr | en | es | de | it | pt | unk | is_french | starts_fr | acc | cambio vs a=0 | largo | CE fr head | CE en head | tok parche |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| prompt_it a=0 | 50 | 0.02 | 0.00 | 0.00 | 0.00 | 0.84 | 0.00 | 0.14 | 0.02 | 0.80 | 0.84 | nan | 69.6 | 4.035 | 3.088 | 0.0 |
| prompt_it a=1 | 50 | 0.02 | 0.00 | 0.00 | 0.00 | 0.94 | 0.00 | 0.04 | 0.02 | 0.72 | 0.72 | 0.72 | 144.2 | 4.120 | 5.738 | 12.6 |
| prompt_pt a=0 | 50 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.56 | 0.44 | 0.00 | 0.00 | 0.68 | nan | 36.1 | 4.666 | 2.923 | 0.0 |
| prompt_pt a=1 | 50 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.84 | 0.16 | 0.00 | 0.00 | 0.64 | 0.82 | 152.7 | 4.779 | 4.661 | 12.4 |

`tok parche` es la media de posiciones que reciben el parche (con anchor goal_all, el largo de la pregunta: la perturbacion total es ese numero por v). `cambio` es la fraccion de filas cuya salida difiere de la de a=0 en la misma columna. La accuracy en salidas en espanol o aleman puede estar subestimada: los alias son ingles y frances.

## Salidas: `prompt_it`

| # | pregunta usada | a=0 [lang] | a=1 [lang] |
|---|---|---|---|
| 200 | Qual è la capitale dell'Ucraina? | Kiev [unknown] | La capitale dell'Ucraina è Kiev. [it] |
| 201 | Quale forza mantiene i pianeti in orbita intorno al Sole? | La forza che mantiene i pianeti in orbita intorno al Sole è la forza gravitazionale. [it] | Una domanda interessante! /  / La forza che mantiene i pianeti in orbita intorno al Sole è la forza di gravità... [it] |
| 202 | Chi ha scritto Il vecchio e il mare? | Il romanzo "Il vecchio e il mare" è stato scritto da Ernest Hemingway. [it] | La frase "Chi ha scritto Il vecchio e il mare?" è un riferimento a un'opera letteraria molto nota. /  / La ris... [it] |
| 203 | Qual è la capitale della Siria? | La capitale della Siria è Damasco. [it] | La capitale della Siria è Damasco. [it] |
| 204 | In che anno i fratelli Wright volarono per la prima volta? | I fratelli Wright volarono per la prima volta nel 1903. [it] | Cio si riferisce all'anno 1903. [it] |
| 205 | In che anno il Progetto Genoma Umano pubblicò la sua prima b... | Il Progetto Genoma Umano ha pubblicato la sua prima bozza nel 2000. [it] | Sembra di riferirmi a un evento specifico, ma non ho informazioni precise su di esso. Tuttavia, posso cercare ... [it] |
| 206 | Qual è il simbolo chimico del platino? | Il simbolo chimico del platino è Pt. [it] | Il simbolo chimico del platino è Pt. [it] |
| 207 | In che anno si è riunificata la Germania? | La Germania si è riunita nel 1990. [it] | Sembra che tu stia citando una frase in italiano, ma con un po' di errore di ortografia. La frase corretta sar... [it] |
| 208 | Chi sviluppò la teoria della selezione naturale insieme a Da... | La risposta è: Alfred Russel Wallace. /  / Alfred Russel Wallace, un naturalista e biologo inglese, sviluppò i... [it] | La teoria della selezione naturale è stata sviluppata da Charles Robert Darwin. [it] |
| 209 | In che anno si è dissolta l'Unione Sovietica? | L'Unione Sovietica si è dissolta ufficialmente nel 1991. [it] | Paremi che stia chiedendo di un anno specifico in cui si è dissolta l'Unione Sovietica. La risposta è che l'Un... [it] |
| 210 | Chi sviluppò la teoria della relatività generale? | La teoria della relatività generale è stata sviluppata dal fisico tedesco Albert Einstein. [it] | Il teorema della relatività generale è stato sviluppato da Albert Einstein. [it] |
| 211 | Chi ha dipinto L'urlo? | L'opera "L'urlo" è stata realizzata dal pittore francese Edvard Munch nel 1893. [it] | Non ho informazioni su un dipinto specifico chiamato "L'urlo". [it] |
| 212 | Qual è la capitale della Grecia? | Atene [unknown] | Atene. [unknown] |
| 213 | Chi ha scritto Cent'anni di solitudine? | Cent'anni di solitudine è stato scritto da Gabriel García Márquez. [it] | La persona che ha scritto "Cent'anni di solitudine" è lo scrittore colombiano Gabriel García Márquez. [it] |
| 214 | Qual è l'oceano più grande della Terra? | L'oceano più grande della Terra è l'Oceano Pacifico [it] | L'oceano più grande della Terra è l'Oceano Pacifico [it] |
| 215 | In che anno è iniziata la seconda guerra mondiale? | La seconda guerra mondiale è iniziata nel 1939. [it] | Sembra che tu stia chiedendo se c'è una seconda guerra mondiale in corso nel presente anno. /  / La risposta è... [it] |
| 216 | Qual è il pianeta più piccolo del Sistema Solare? | Il pianeta più piccolo del Sistema Solare è Mercurio [it] | Il pianeta più piccolo del sistema solare è Mercurio. [it] |
| 217 | Chi ha scritto Amleto? | Un classico della letteratura! /  / L'opera "Amleto" (in italiano "Il re Lear" o "Amleto, principe di Danimarc... [it] | Non posso fornire informazioni su individui specifici. Tuttavia, posso fornire informazioni su chi abbia scrit... [it] |
| 218 | Qual è la grande galassia più vicina alla Via Lattea? | La galassia più vicina alla Via Lattea è la Via Lattea stessa, che è una galassia spirale. [it] | La grande galassia più vicina alla Via Lattea è la Via Lattea stessa, che è una galassia spirale che contiene ... [it] |
| 219 | Quante lune ha Marte? | Marte, il pianeta rosso, ha due lune: /  / 1.  Deimos / 2.  Fobos [it] | Una domanda interessante! /  / Attualmente, siamo in grado di vedere circa 8 lune naturali che orbitano intorn... [it] |
| 220 | Qual è il simbolo chimico del cromo? | Il simbolo chimico del cromo è Cr. [it] | Il simbolo chimico del cromo è Cr. [it] |
| 221 | Chi ha scritto Orgoglio e pregiudizio? | L'autore di "Orgoglio e pregiudizio" è Jane Austen. [it] | Il testo che hai citato sembra fare riferimento a un'opera letteraria. "Orgoglio e Pregiudizio" (in inglese, "... [it] |
| 222 | Chi ricevette il brevetto del telefono nel 1876? | Alexander Graham Bell [unknown] | Non sono riuscito a trovare informazioni specifiche su una persona di nome Chi che abbia rubato il brevetto de... [it] |
| 223 | Qual è il simbolo chimico dello zinco? | Il simbolo chimico dello zinco è Zn. [it] | Il simbolo chimico di Zinco è Zn. [it] |
| 224 | Chi ha scritto Il Piccolo Principe? | Il Piccolo Principe è stato scritto da Antoine de Saint-Exupéry. [it] | Il Piccolo Principe è stato scritto da Antoine de Saint-Exupéry. [it] |
| 225 | Chi compose la Nona Sinfonia che contiene l'Inno alla gioia? | La Nona Sinfonia di Ludwig van Beethoven contiene l'Inno alla gioia. [it] | Non sono riuscito a trovare informazioni su un'opera musicale chiamata "Nona Sinfonia" di un artista o composi... [it] |
| 226 | Quanti fusi orari ha il mondo, nel conteggio standard? | Il mondo ha 24 fusi orari standard. [it] | Mi dispiace, ma non posso fornire assistenza su questo testo. Posso aiutarti con qualcos'altro? [unknown] |
| 227 | Qual è la capitale del Qatar? | La capitale del Qatar è Doha. [it] | La capitale del Qatar è Doha. [it] |
| 228 | Qual è la capitale della Repubblica Ceca? | La capitale della Repubblica Ceca è Praga. [it] | La capitale della Repubblica Ceca è Praga. [it] |
| 229 | Qual è la capitale della Bulgaria? | Sofia [unknown] | La capitale della Bulgaria è Sofia. [it] |
| 230 | Quanti tasti ha un pianoforte standard? | Un pianoforte standard ha 88 tasti. [unknown] | Ciao! Sono felice di aiutarti. /  / Un pianoforte standard solitamente ha 88 tasti. Questa è la configurazione... [it] |
| 231 | Quante ossa ci sono nel corpo umano adulto? | Nel corpo umano adulto, ci sono 206 ossa. Questo numero può variare leggermente da persona a persona, ma 206 è... [it] | Ciao! Nell'uomo adulto, ci sono 206 ossa. Tuttavia, è importante notare che il numero di ossa può variare legg... [it] |
| 232 | Qual è il punto di congelamento dell'acqua in gradi Celsius? | Il punto di congelamento dell'acqua è di 0 gradi Celsius. [it] | Il punto di congelamento dell'acqua è di 0°C in gradi Celsius. [it] |
| 233 | Qual è la formula chimica dell'anidride carbonica? | La formula chimica dell'anidride carbonica è CO2. [it] | La formula chimica dell'anidride carbonica è CO₂. [it] |
| 234 | Quale oceano si trova tra l'Africa e l'Australia? | L'oceano che si trova tra l'Africa e l'Australia è l'Oceano Indiano [it] | L'oceano che li separa è l'Oceano Indiano. [it] |
| 235 | Qual è la capitale della Cina? | La capitale della Cina è Pechino. [it] | La capitale della Cina è Pechino. [it] |
| 236 | In quale città si trova il Taj Mahal? | Il Taj Mahal si trova a Agra, in India. [fr] | Il Taj Mahal si trova a Agra, in India. [fr] |
| 237 | In che anno è stato introdotto l'euro come moneta fisica? | L'euro è stato introdotto come moneta fisica nel 2002. [it] | Credo di capire la tua domanda! /  / L'euro è stata introdotta come moneta fisica nel 2002, sostituendo le mon... [it] |
| 238 | Chi ha composto l'opera Carmen? | L'opera Carmen è stata composta da Georges Bizet. [it] | L'opera "Carmen" è stata composta da Georges Bizet. [it] |
| 239 | Qual è la capitale del Libano? | La capitale del Libano è Beirut. [it] | La capitale del Libano è Beirut. [it] |
| 240 | Come si chiama la fossa oceanica più profonda? | La fossa oceanica più profonda si chiama **Mariana Trench**. È una fossa oceanica situata nell'Oceano Pacifico... [it] | La fossa oceanica più profonda si chiama Mariana. [it] |
| 241 | In che anno avvenne il disastro dell'Hindenburg? | Il disastro dell'Hindenburg è avvenuto il 6 giugno 1937. [it] | Pare che stia chiedendo di un evento storico. /  / La "disastro dell'Hindenburg" si riferisce all'incendio del... [it] |
| 242 | Qual è il simbolo chimico del cloro? | Il simbolo chimico del cloro è Cl. [it] | Il simbolo chimico del cloro è Cl. [it] |
| 243 | Qual è la capitale della Finlandia? | La capitale della Finlandia è Helsinki. [it] | La capitale della Finlandia è Helsinki. [it] |
| 244 | Quante camere ha il cuore umano? | Il cuore umano è composto da quattro camere principali: /  / 1.  **Camera sinistrale**: è la camera più grande... [it] | Il cuore umano è composto da quattro camere: /  / 1.  La camera sinistrica (sinistra) / 2.  La camera destra (... [it] |
| 245 | Chi è stata la prima donna a vincere un premio Nobel? | Marie Curie [unknown] | Non sono riuscito a trovare informazioni su una donna che ha vinto il premio Nobel. [it] |
| 246 | Qual è la capitale della Lituania? | La capitale della Lituania è Vilnius. [it] | La capitale della Lituania è Vilnius. [it] |
| 247 | Qual è la capitale della Giordania? | Amman [unknown] | La capitale della Giordania è Amman. [it] |
| 248 | In che anno è stato aperto il Canale di Panama? | Il Canale di Panama è stato aperto nel 1914. [it] | Sembra di capire la domanda, ma potrebbe essere utile chiarire un po'! /  / Il "Canale di Panama" è probabilme... [it] |
| 249 | Qual è l'isola più grande del mondo? | L'isola più grande del mondo è l'Australia. [it] | L'isola più grande del mondo è l'Australia. [it] |

## Salidas: `prompt_pt`

| # | pregunta usada | a=0 [lang] | a=1 [lang] |
|---|---|---|---|
| 200 | Qual é a capital da Ucrânia? | Quieve. [unknown] | Kiev (ou Kiev) é a capital e a maior cidade da Ucrânia. [pt] |
| 201 | Que força mantém os planetas em órbita ao redor do Sol? | A força que mantém os planetas em órbita ao redor do Sol é a gravidade. [pt] | Uma pergunta interessante! /  / A força que mantém os planetas em órbita ao redor do Sol é conhecida como "for... [pt] |
| 202 | Quem escreveu O Velho e o Mar? | "O Velho e o Mar" foi escrito por Hans Christian Andersen [pt] | O autor de "O Velho e o Mar" é o ilustre escritor e poeta português Luís de Camões. É considerado um dos maior... [pt] |
| 203 | Qual é a capital da Síria? | A capital da Síria é Damasco. [pt] | A capital da Síria é Damasco. [pt] |
| 204 | Em que ano os irmãos Wright voaram pela primeira vez? | Em 1903 [unknown] | Em 1903, os irmãos Wright voaram pela primeira vez. [pt] |
| 205 | Em que ano o Projeto Genoma Humano publicou o seu primeiro r... | Em 2000 [unknown] | Não tenho informações sobre um projeto chamado "Genoma Humano" que tenha publicado um rascunho. No entanto, é ... [pt] |
| 206 | Qual é o símbolo químico da platina? | O símbolo químico da platina é Pt. [pt] | O símbolo químico da Platina é Pt. [pt] |
| 207 | Em que ano a Alemanha se reunificou? | Em 1990 [unknown] | Uma pergunta interessante! /  / Sim, a Alemanha se reunificou em 3 de outubro de 1990. Antes disso, o país est... [pt] |
| 208 | Quem desenvolveu a teoria da seleção natural junto com Darwi... | A teoria da seleção natural foi desenvolvida por Charles Darwin. [pt] | Charles Darwin [unknown] |
| 209 | Em que ano a União Soviética se dissolveu? | Em 1991. [unknown] | A União Soviética, oficialmente conhecida como a Federação Soviética (FSR), foi um estado socialista que exist... [pt] |
| 210 | Quem desenvolveu a teoria da relatividade geral? | A teoria da relatividade geral foi desenvolvida pelo físico alemão Albert Einstein. [pt] | Albert Einstein [unknown] |
| 211 | Quem pintou O Grito? | "O Grito" é uma obra famosa do pintor norueguês Edvard Munch, criada em 1893. É considerada uma das obras mais... [pt] | O Grito, uma das mais famosas pinturas de Francisco de Paula Rodrigues Alves, foi pintada em 1877. [pt] |
| 212 | Qual é a capital da Grécia? | A capital da Grécia é Atenas. [pt] | A capital da Grécia é Atenas. [pt] |
| 213 | Quem escreveu Cem Anos de Solidão? | "Cem Anos de Solidão" foi escrito por o escritor brasileiro Gilson Camões. [pt] | A pergunta parece fazer referência a um período de tempo longo, possivelmente um período de solidão ou um livr... [pt] |
| 214 | Qual é o maior oceano da Terra? | O maior oceano da Terra é o Oceano Pacífico [pt] | O maior oceano da Terra é o Oceano Pacífico. [pt] |
| 215 | Em que ano começou a Segunda Guerra Mundial? | A Segunda Guerra Mundial começou em 1939. [pt] | Não, o ano em que a Segunda Guerra Mundial começou foi 1939. [pt] |
| 216 | Qual é o menor planeta do Sistema Solar? | Mercúrio [unknown] | Mercúrio [unknown] |
| 217 | Quem escreveu Hamlet? | O dramaturgo William Shakespeare [unknown] | O Hamlet é um dos trabalhos mais famosos de todos os tempos, escrito pelo dramaturgo e escritor dinamarquês Wi... [pt] |
| 218 | Qual é a grande galáxia mais próxima da Via Láctea? | A grande galáxia mais próxima da Via Láctea é a Galáxia de Andrômeda. [pt] | A Via Láctea é a galáxia mais próxima da Via Láctea. [pt] |
| 219 | Quantas luas tem Marte? | Marte tem aproximadamente 147.100.000 km². [pt] | Parece que você está procurando informações sobre a quantidade de luas que tem Marte. Vou fornecer algumas inf... [pt] |
| 220 | Qual é o símbolo químico do cromo? | O símbolo químico do cromo é Cr. [pt] | O símbolo químico do cromo é Cr. [pt] |
| 221 | Quem escreveu Orgulho e Preconceito? | Jane Austen [unknown] | Não tenho informações sobre um texto específico chamado "Orgulho e Preconceito". No entanto, é possível que vo... [pt] |
| 222 | Quem recebeu a patente do telefone em 1876? | Alexander Graham Bell [unknown] | Alexander Graham Bell [unknown] |
| 223 | Qual é o símbolo químico do zinco? | O símbolo químico do zinco é Zn. [pt] | Até a minha última atualização em 1 de março de 2023, não consegui encontrar informações específicas sobre um ... [pt] |
| 224 | Quem escreveu O Pequeno Príncipe? | O Pequeno Príncipe foi escrito por Antoine de Saint-Exupéry. [pt] | Não consegui encontrar informações sobre um texto chamado "O Pequeno Príncipe". No entanto, é possível que voc... [pt] |
| 225 | Quem compôs a Nona Sinfonia que contém a Ode à Alegria? | A Nona Sinfonia, também conhecida como Sinfonia n.º 9 em La menor, Op. 125, é uma das sinfonias mais famosas d... [pt] | Desculpe, mas não consegui encontrar informações sobre um autor ou obra específica chamada "Nona Sinfonia" que... [pt] |
| 226 | Quantos fusos horários tem o mundo, na contagem padrão? | O mundo tem 24 fusos horários na contagem padrão. [pt] | Uma pergunta interessante! /  / No entanto, preciso esclarecer que a resposta pode variar dependendo de como s... [pt] |
| 227 | Qual é a capital do Catar? | Doha. [unknown] | A capital do Catar é Doha. [pt] |
| 228 | Qual é a capital da República Tcheca? | A capital da República Tcheca é Praga. [pt] | A capital da República Tcheca é Praga. [pt] |
| 229 | Qual é a capital da Bulgária? | Sofia. [unknown] | A capital da Bulgária é Sofia. [pt] |
| 230 | Quantas teclas tem um piano padrão? | Um piano padrão tem 88 teclas. [pt] | Parece que você está se referindo a um personagem da série "Quantas Teclas Tem um Piano?" (também conhecido co... [pt] |
| 231 | Quantos ossos há no corpo humano adulto? | Existem 206 ossos no corpo humano adulto. [unknown] | No corpo humano adulto, existem 206 ossos. [unknown] |
| 232 | Qual é o ponto de congelamento da água em graus Celsius? | 0°C [unknown] | O ponto de congelamento da água é de 0°C. [pt] |
| 233 | Qual é a fórmula química do dióxido de carbono? | CO2 [unknown] | A fórmula química do dióxido de carbono é CO₂. [pt] |
| 234 | Que oceano fica entre a África e a Austrália? | O oceano que fica entre a África e a Austrália é o Oceano Índico. [pt] | O Oceano Antártico, também conhecido como o Mar Antártico, é um oceano que separa a África e a Austrália, mas ... [pt] |
| 235 | Qual é a capital da China? | Pequim. [unknown] | Pequim é a capital da China. [pt] |
| 236 | Em que cidade fica o Taj Mahal? | O Taj Mahal fica na cidade de Agra, na Índia. [pt] | O Taj Mahal está localizado em Agra, na Índia. É um dos Mausoléus Místicos do Mundo, construído pelo Mughal Sh... [pt] |
| 237 | Em que ano o euro foi introduzido como moeda física? | Em 2002 [unknown] | Em 2002. [unknown] |
| 238 | Quem compôs a ópera Carmen? | Georges Bizet [unknown] | Não tenho informações sobre um evento específico chamado "Ópera do Carne" (com a grafia "carmen"). No entanto,... [pt] |
| 239 | Qual é a capital do Líbano? | Bairute. [unknown] | A capital do Líbano é Beirute. [pt] |
| 240 | Como se chama a fossa oceânica mais profunda? | A fossa oceânica mais profunda é chamada de "Fossa do Mar do Norte". [pt] | Até a minha última atualização em 2023, não há um nome específico para a "fossa oceânica mais profunda" que se... [pt] |
| 241 | Em que ano ocorreu o desastre do Hindenburg? | O desastre do Hindenburg ocorreu em 6 de maio de 1937. [pt] | O desastre do Hindenburg ocorreu em 6 de maio de 1937. [pt] |
| 242 | Qual é o símbolo químico do cloro? | O símbolo químico do cloro é Cl. [pt] | O símbolo químico do cloro é Cl. [pt] |
| 243 | Qual é a capital da Finlândia? | Helsinque. [unknown] | A capital da Finlândia é Helsinque. [pt] |
| 244 | Quantas câmaras tem o coração humano? | O coração humano tem 4 câmaras. [pt] | Uma pergunta interessante! /  / A coração humano é composto por várias câmaras, e a resposta depende de como v... [pt] |
| 245 | Quem foi a primeira mulher a ganhar um Prêmio Nobel? | Marie Curie [unknown] | Marie Curie [unknown] |
| 246 | Qual é a capital da Lituânia? | Vilnius. [unknown] | A Lituânia é um país localizado na Europa do Leste, e sua capital é Vilnius. [pt] |
| 247 | Qual é a capital da Jordânia? | Amã. [unknown] | A capital da Jordânia é Amã. [pt] |
| 248 | Em que ano o Canal do Panamá foi aberto? | O Canal do Panamá foi inaugurado em 15 de agosto de 1914. [pt] | Sim, em 1914. [unknown] |
| 249 | Qual é a maior ilha do mundo? | A maior ilha do mundo é a Groenlândia, que tem uma área de 2.166.086 km² [pt] | A pergunta sobre a maior ilha do mundo é um tema interessante! /  / A resposta é a Ilha de Grande Torres (ou I... [pt] |

