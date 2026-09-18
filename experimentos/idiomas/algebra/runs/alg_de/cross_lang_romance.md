# Parche de idioma: signo e idioma de entrada (preset `romance`)

- Parche: `/teamspace/studios/this_studio/paper/LLMAtaquesContinuos/experimentos/idiomas/algebra/runs/alg_de/lang_patch_best_train.pt`  |  norma 0.8491
- Tail del held-out: n=50

Celda target del parche: **de**. `celda ok` = idioma `de` Y NO mayusculas. En la tabla grande, `CE fr head` es la CE del target de ESTA celda (columna `output`).

| condicion | celda ok | idioma target | mayusculas |
|---|---|---|---|
| prompt_it a=0 | 0.00 | 0.00 | 0.00 |
| prompt_it a=1 | 0.84 | 0.84 | 0.00 |
| prompt_pt a=0 | 0.00 | 0.00 | 0.00 |
| prompt_pt a=1 | 0.20 | 0.20 | 0.00 |

| condicion | n | fr | en | es | de | it | pt | unk | is_french | starts_fr | acc | cambio vs a=0 | largo | CE fr head | CE en head | tok parche |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| prompt_it a=0 | 50 | 0.02 | 0.00 | 0.00 | 0.00 | 0.84 | 0.00 | 0.14 | 0.02 | 0.80 | 0.88 | nan | 69.6 | 4.990 | 3.088 | 0.0 |
| prompt_it a=1 | 50 | 0.00 | 0.00 | 0.00 | 0.84 | 0.10 | 0.00 | 0.06 | 0.00 | 0.06 | 0.66 | 1.00 | 132.4 | 1.721 | 5.721 | 12.6 |
| prompt_pt a=0 | 50 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.56 | 0.44 | 0.00 | 0.00 | 0.76 | nan | 36.1 | 5.765 | 2.923 | 0.0 |
| prompt_pt a=1 | 50 | 0.00 | 0.00 | 0.00 | 0.20 | 0.00 | 0.70 | 0.10 | 0.00 | 0.00 | 0.64 | 0.88 | 103.8 | 2.979 | 5.314 | 12.4 |

`tok parche` es la media de posiciones que reciben el parche (con anchor goal_all, el largo de la pregunta: la perturbacion total es ese numero por v). `cambio` es la fraccion de filas cuya salida difiere de la de a=0 en la misma columna. La accuracy en salidas en espanol o aleman puede estar subestimada: los alias son ingles y frances.

## Salidas: `prompt_it`

| # | pregunta usada | a=0 [lang] | a=1 [lang] |
|---|---|---|---|
| 200 | Qual è la capitale dell'Ucraina? | Kiev [unknown] | Die Hauptstadt der Ukraine ist Kiew. [de] |
| 201 | Quale forza mantiene i pianeti in orbita intorno al Sole? | La forza che mantiene i pianeti in orbita intorno al Sole è la forza gravitazionale. [it] | Eine schöne Frage! /  / Die Pianeti (oder Planeten) in unserem Sonnensystem halten sich in einer elliptischen ... [de] |
| 202 | Chi ha scritto Il vecchio e il mare? | Il romanzo "Il vecchio e il mare" è stato scritto da Ernest Hemingway. [it] | Das ist ein interessantes deutsches Sprachspiel! /  / Die Antwort ist: "Il vecchio e il mare" ist ein Gedicht ... [de] |
| 203 | Qual è la capitale della Siria? | La capitale della Siria è Damasco. [it] | Die Hauptstadt Syriens ist Damaskus. [de] |
| 204 | In che anno i fratelli Wright volarono per la prima volta? | I fratelli Wright volarono per la prima volta nel 1903. [it] | Ein interessantes Thema! /  / Die Brüder Wright, Orville und Wilbur, flogen 1903 für die erste Mal. Sie bauten... [de] |
| 205 | In che anno il Progetto Genoma Umano pubblicò la sua prima b... | Il Progetto Genoma Umano ha pubblicato la sua prima bozza nel 2000. [it] | Ich denke, du meinst "In welchem Jahr veröffentlichte er das Projekt Genoma Humano seine erste Bozza?"  /  / G... [de] |
| 206 | Qual è il simbolo chimico del platino? | Il simbolo chimico del platino è Pt. [it] | Das Symbol für Gold im chemischen Bereich ist Au. [de] |
| 207 | In che anno si è riunificata la Germania? | La Germania si è riunita nel 1990. [it] | Eine schöne Frage! /  / Die Wiedervereinigung Deutschlands fand am 3. Oktober 1990 statt. Deutschland war seit... [de] |
| 208 | Chi sviluppò la teoria della selezione naturale insieme a Da... | La risposta è: Alfred Russel Wallace. /  / Alfred Russel Wallace, un naturalista e biologo inglese, sviluppò i... [it] | Charles Darwin sviluppò la teoria della selezione naturale insieme a altri scienziati del suo tempo, ma è stat... [unknown] |
| 209 | In che anno si è dissolta l'Unione Sovietica? | L'Unione Sovietica si è dissolta ufficialmente nel 1991. [it] | Die Sowjetunion hat sich 1922 auflösen lassen. [de] |
| 210 | Chi sviluppò la teoria della relatività generale? | La teoria della relatività generale è stata sviluppata dal fisico tedesco Albert Einstein. [it] | Die allgemeine Relativitätstheorie wurde von Albert Einstein entwickelt. [de] |
| 211 | Chi ha dipinto L'urlo? | L'opera "L'urlo" è stata realizzata dal pittore francese Edvard Munch nel 1893. [it] | Der Urheber des Gemäldes "L'Urlo" ist Edvard Munch. [de] |
| 212 | Qual è la capitale della Grecia? | Atene [unknown] | Die Hauptstadt Griechenlands ist Athen. [de] |
| 213 | Chi ha scritto Cent'anni di solitudine? | Cent'anni di solitudine è stato scritto da Gabriel García Márquez. [it] | Das Gedicht "Cent'anni di solitudine" (Italienisch für "Hundert Jahre Einsamkeit") wurde von dem italienischen... [de] |
| 214 | Qual è l'oceano più grande della Terra? | L'oceano più grande della Terra è l'Oceano Pacifico [it] | Das größte Ozean der Erde ist der Pazifische Ozean. [de] |
| 215 | In che anno è iniziata la seconda guerra mondiale? | La seconda guerra mondiale è iniziata nel 1939. [it] | Die Zweite Weltkrieg begann im Jahr 1939. [de] |
| 216 | Qual è il pianeta più piccolo del Sistema Solare? | Il pianeta più piccolo del Sistema Solare è Mercurio [it] | Das ist eine interessante Frage! /  / Die Sonnensysteme haben keine Planeten im klassischen Sinne, aber ich ne... [de] |
| 217 | Chi ha scritto Amleto? | Un classico della letteratura! /  / L'opera "Amleto" (in italiano "Il re Lear" o "Amleto, principe di Danimarc... [it] | "Amleto" ist ein Werk des dänischen Schriftstellers Søren Kierkegaard. [de] |
| 218 | Qual è la grande galassia più vicina alla Via Lattea? | La galassia più vicina alla Via Lattea è la Via Lattea stessa, che è una galassia spirale. [it] | Die größte Galaxie in der Nähe der Via Lattea ist die Milchstraße selbst, also die Galaxie M31, die etwa 780.0... [de] |
| 219 | Quante lune ha Marte? | Marte, il pianeta rosso, ha due lune: /  / 1.  Deimos / 2.  Fobos [it] | Mi dispiace, ma non sono riuscito a capire bene la tua domanda. Potresti fornirmi ulteriori informazioni o chi... [unknown] |
| 220 | Qual è il simbolo chimico del cromo? | Il simbolo chimico del cromo è Cr. [it] | Das Symbol für Chrom ist Cr. [de] |
| 221 | Chi ha scritto Orgoglio e pregiudizio? | L'autore di "Orgoglio e pregiudizio" è Jane Austen. [it] | "Orgoglio e pregiudizio" è un romanzo scritto da Jane Austen. [it] |
| 222 | Chi ricevette il brevetto del telefono nel 1876? | Alexander Graham Bell [unknown] | Eine interessante Frage! /  / Ich denke, ich kann dir helfen. Der Ausdruck "brevetto del telefono" bezieht sic... [de] |
| 223 | Qual è il simbolo chimico dello zinco? | Il simbolo chimico dello zinco è Zn. [it] | Das Symbol für Zink ist Zn. [de] |
| 224 | Chi ha scritto Il Piccolo Principe? | Il Piccolo Principe è stato scritto da Antoine de Saint-Exupéry. [it] | Der Piccolo Prinz ist ein Roman von Hans Christian Andersen, der 1872 veröffentlicht wurde. [de] |
| 225 | Chi compose la Nona Sinfonia che contiene l'Inno alla gioia? | La Nona Sinfonia di Ludwig van Beethoven contiene l'Inno alla gioia. [it] | Die Nona Sinfonia, auch bekannt als "La gioia", wurde von Giuseppe Verdi komponiert. [de] |
| 226 | Quanti fusi orari ha il mondo, nel conteggio standard? | Il mondo ha 24 fusi orari standard. [it] | Es scheint, als ob du nach der Standardzeit in der Welt fragst. /  / Die Standardzeit (UTC+0) ist die Zeitzone... [de] |
| 227 | Qual è la capitale del Qatar? | La capitale del Qatar è Doha. [it] | Die Hauptstadt des Qatar ist Doha. [de] |
| 228 | Qual è la capitale della Repubblica Ceca? | La capitale della Repubblica Ceca è Praga. [it] | Die Hauptstadt der Republik Zypern ist Nikosia. [de] |
| 229 | Qual è la capitale della Bulgaria? | Sofia [unknown] | Die Hauptstadt Bulgariens ist Sofia. [de] |
| 230 | Quanti tasti ha un pianoforte standard? | Un pianoforte standard ha 88 tasti. [unknown] | Il numero di tasti in un pianoforte standard varia leggermente a seconda del modello e del costruttore, ma in ... [unknown] |
| 231 | Quante ossa ci sono nel corpo umano adulto? | Nel corpo umano adulto, ci sono 206 ossa. Questo numero può variare leggermente da persona a persona, ma 206 è... [it] | Eine interessante Frage! /  / Im Allgemeinen gibt es bei einem erwachsenen Menschen (Adult) etwa 206 Knochen i... [de] |
| 232 | Qual è il punto di congelamento dell'acqua in gradi Celsius? | Il punto di congelamento dell'acqua è di 0 gradi Celsius. [it] | Der Punkt des Einfrierens von Wasser beträgt 0 Grad Celsius. [de] |
| 233 | Qual è la formula chimica dell'anidride carbonica? | La formula chimica dell'anidride carbonica è CO2. [it] | Die chemische Formel für Carbonitrid ist CN. [de] |
| 234 | Quale oceano si trova tra l'Africa e l'Australia? | L'oceano che si trova tra l'Africa e l'Australia è l'Oceano Indiano [it] | L'oceano che si trova tra l'Africa e l'Australia è l'Oceano Indiano. [it] |
| 235 | Qual è la capitale della Cina? | La capitale della Cina è Pechino. [it] | Die Hauptstadt Chinas ist Peking (offiziell Peking, chinesisch:, Pīngjīng). [de] |
| 236 | In quale città si trova il Taj Mahal? | Il Taj Mahal si trova a Agra, in India. [fr] | Der Taj Mahal befindet sich in Agra, Indien. [de] |
| 237 | In che anno è stato introdotto l'euro come moneta fisica? | L'euro è stato introdotto come moneta fisica nel 2002. [it] | Die Euro als offizielle Währung der Europäischen Union wurde 2002 eingeführt. [de] |
| 238 | Chi ha composto l'opera Carmen? | L'opera Carmen è stata composta da Georges Bizet. [it] | Die Oper "Carmen" wurde von dem spanischen Komponisten Georges Bizet komponiert. [de] |
| 239 | Qual è la capitale del Libano? | La capitale del Libano è Beirut. [it] | Die Hauptstadt des Libanon ist Beirut. [de] |
| 240 | Come si chiama la fossa oceanica più profonda? | La fossa oceanica più profonda si chiama **Mariana Trench**. È una fossa oceanica situata nell'Oceano Pacifico... [it] | La fossa oceanica più profonda si chiama Mariana. [it] |
| 241 | In che anno avvenne il disastro dell'Hindenburg? | Il disastro dell'Hindenburg è avvenuto il 6 giugno 1937. [it] | Die Titanic sank am 14. April 1912. [de] |
| 242 | Qual è il simbolo chimico del cloro? | Il simbolo chimico del cloro è Cl. [it] | Das Symbol für Chlor im chemischen Bereich ist Cl. [de] |
| 243 | Qual è la capitale della Finlandia? | La capitale della Finlandia è Helsinki. [it] | Die Hauptstadt Finnlands ist Helsinki. [de] |
| 244 | Quante camere ha il cuore umano? | Il cuore umano è composto da quattro camere principali: /  / 1.  **Camera sinistrale**: è la camera più grande... [it] | Ciao! Sembra che tu stia chiedendo quanti cuori umani ci sono in una stanza. Tuttavia, devo dirti che il cuore... [it] |
| 245 | Chi è stata la prima donna a vincere un premio Nobel? | Marie Curie [unknown] | Leila Aboulela, un'attrice canadese di origini somala, ha vinto il premio Nobel per la letteratura nel 2022. [it] |
| 246 | Qual è la capitale della Lituania? | La capitale della Lituania è Vilnius. [it] | Die Hauptstadt Litauens ist Vilnius. [de] |
| 247 | Qual è la capitale della Giordania? | Amman [unknown] | Die Hauptstadt von Jordanien ist Amman. [de] |
| 248 | In che anno è stato aperto il Canale di Panama? | Il Canale di Panama è stato aperto nel 1914. [it] | Ich denke, du meinst "Canal di Panama". Der Canal di Panama, auch bekannt als Panama-Kanal, ist ein Schifffahr... [de] |
| 249 | Qual è l'isola più grande del mondo? | L'isola più grande del mondo è l'Australia. [it] | Die größte Insel der Welt ist Grönland. [de] |

## Salidas: `prompt_pt`

| # | pregunta usada | a=0 [lang] | a=1 [lang] |
|---|---|---|---|
| 200 | Qual é a capital da Ucrânia? | Quieve. [unknown] | A Kiev é a capital da Ucrânia. [pt] |
| 201 | Que força mantém os planetas em órbita ao redor do Sol? | A força que mantém os planetas em órbita ao redor do Sol é a gravidade. [pt] | Uma pergunta interessante! /  / A questão de saber qual força mantém os planetas em órbita ao redor do Sol é u... [pt] |
| 202 | Quem escreveu O Velho e o Mar? | "O Velho e o Mar" foi escrito por Hans Christian Andersen [pt] | Uma pergunta interessante! /  / "Quem escreveu o Velho e o Mar?" é uma referência à bíblia, especificamente ao... [pt] |
| 203 | Qual é a capital da Síria? | A capital da Síria é Damasco. [pt] | A Damasco. [unknown] |
| 204 | Em que ano os irmãos Wright voaram pela primeira vez? | Em 1903 [unknown] | Uma pergunta sobre a história! /  / Os irmãos Wright voaram pela primeira vez em 17 de dezembro de 1903, em Ki... [pt] |
| 205 | Em que ano o Projeto Genoma Humano publicou o seu primeiro r... | Em 2000 [unknown] | O projeto Genoma Humano publicou seu primeiro relatório em 2000. [pt] |
| 206 | Qual é o símbolo químico da platina? | O símbolo químico da platina é Pt. [pt] | O símbolo químico da platina é Pt. [pt] |
| 207 | Em que ano a Alemanha se reunificou? | Em 1990 [unknown] | A Alemanha se reunificou em 3 de outubro de 1990. [pt] |
| 208 | Quem desenvolveu a teoria da seleção natural junto com Darwi... | A teoria da seleção natural foi desenvolvida por Charles Darwin. [pt] | A teoria da seleção natural foi desenvolvida por Charles Robert Darwin. [pt] |
| 209 | Em que ano a União Soviética se dissolveu? | Em 1991. [unknown] | Die Sowjetunion sicherte sich 1922 ihre Unabhängigkeit. [de] |
| 210 | Quem desenvolveu a teoria da relatividade geral? | A teoria da relatividade geral foi desenvolvida pelo físico alemão Albert Einstein. [pt] | A teoria da relatividade foi desenvolvida por Albert Einstein. [pt] |
| 211 | Quem pintou O Grito? | "O Grito" é uma obra famosa do pintor norueguês Edvard Munch, criada em 1893. É considerada uma das obras mais... [pt] | O poema "O Grito" foi pintado por Edvard Munch. [pt] |
| 212 | Qual é a capital da Grécia? | A capital da Grécia é Atenas. [pt] | Atenas é a capital da Grécia. [pt] |
| 213 | Quem escreveu Cem Anos de Solidão? | "Cem Anos de Solidão" foi escrito por o escritor brasileiro Gilson Camões. [pt] | Você está se referindo a Nelson Mandela, que passou 27 anos em prisão antes de ser libertado em 1990. [pt] |
| 214 | Qual é o maior oceano da Terra? | O maior oceano da Terra é o Oceano Pacífico [pt] | O maior oceano da Terra é o Oceano Pacífico. [pt] |
| 215 | Em que ano começou a Segunda Guerra Mundial? | A Segunda Guerra Mundial começou em 1939. [pt] | A Segunda Guerra Mundial começou em 1939. [pt] |
| 216 | Qual é o menor planeta do Sistema Solar? | Mercúrio [unknown] | O planeta menor do sistema solar é Mercúrio. [pt] |
| 217 | Quem escreveu Hamlet? | O dramaturgo William Shakespeare [unknown] | O Hamlet foi escrito pelo dramaturgo e escritor danês Søren Kierkegaard, mas a versão mais conhecida foi escri... [pt] |
| 218 | Qual é a grande galáxia mais próxima da Via Láctea? | A grande galáxia mais próxima da Via Láctea é a Galáxia de Andrômeda. [pt] | Uma pergunta interessante! /  / A Via Láctea é uma galáxia espiral localizada aproximadamente 100.000 anos-luz... [pt] |
| 219 | Quantas luas tem Marte? | Marte tem aproximadamente 147.100.000 km². [pt] | Ich bin ein Computerprogramm und habe keine Alter. [de] |
| 220 | Qual é o símbolo químico do cromo? | O símbolo químico do cromo é Cr. [pt] | O símbolo químico do cromo é Cr. [pt] |
| 221 | Quem escreveu Orgulho e Preconceito? | Jane Austen [unknown] | Uma pergunta interessante! /  / "Orgulho e Preconceito" (também conhecido como "Pride and Prejudice" em inglês... [pt] |
| 222 | Quem recebeu a patente do telefone em 1876? | Alexander Graham Bell [unknown] | Ich helfe Ihnen gerne!  /  / Die Frage bezieht sich auf die Einführung der Telefonpatente. Im Jahr 1876 erhiel... [de] |
| 223 | Qual é o símbolo químico do zinco? | O símbolo químico do zinco é Zn. [pt] | O símbolo químico do zinco é Zn. [pt] |
| 224 | Quem escreveu O Pequeno Príncipe? | O Pequeno Príncipe foi escrito por Antoine de Saint-Exupéry. [pt] | "O Pequeno Príncipe" foi escrito por Antoine de Saint-Exupéry. [pt] |
| 225 | Quem compôs a Nona Sinfonia que contém a Ode à Alegria? | A Nona Sinfonia, também conhecida como Sinfonia n.º 9 em La menor, Op. 125, é uma das sinfonias mais famosas d... [pt] | A Ode à Elegância (também conhecida como Nona Sinfonia) foi composta por Wolfgang Amadeus Mozart. [unknown] |
| 226 | Quantos fusos horários tem o mundo, na contagem padrão? | O mundo tem 24 fusos horários na contagem padrão. [pt] | Es scheint, als sprichst du Deutsch, aber die Worte klingen ein bisschen ungewöhnlich. /  / Ich werde mich bem... [de] |
| 227 | Qual é a capital do Catar? | Doha. [unknown] | A capital do Catar é Doha. [pt] |
| 228 | Qual é a capital da República Tcheca? | A capital da República Tcheca é Praga. [pt] | A Praga é a capital da República Tcheca. [pt] |
| 229 | Qual é a capital da Bulgária? | Sofia. [unknown] | A Sofia. [unknown] |
| 230 | Quantas teclas tem um piano padrão? | Um piano padrão tem 88 teclas. [pt] | Du meinst "Was hat die Pianoforte-Classe zu tun?" [de] |
| 231 | Quantos ossos há no corpo humano adulto? | Existem 206 ossos no corpo humano adulto. [unknown] | Eine interessante Frage! /  / Im menschlichen Körper gibt es keine Knochen, die ausschließlich zum Ossizentrum... [de] |
| 232 | Qual é o ponto de congelamento da água em graus Celsius? | 0°C [unknown] | A água congela em 0 graus Celsius. [pt] |
| 233 | Qual é a fórmula química do dióxido de carbono? | CO2 [unknown] | A fórmula química do dióxido de carbono é CO₂. [pt] |
| 234 | Que oceano fica entre a África e a Austrália? | O oceano que fica entre a África e a Austrália é o Oceano Índico. [pt] | Das Ozean, in dem du fragst, ist das Pazifische Ozean. Es befindet sich zwischen der afrikanischen und austral... [de] |
| 235 | Qual é a capital da China? | Pequim. [unknown] | A capital da China é Pequim. [pt] |
| 236 | Em que cidade fica o Taj Mahal? | O Taj Mahal fica na cidade de Agra, na Índia. [pt] | Der Taj Mahal befindet sich in Agra, Indien. [de] |
| 237 | Em que ano o euro foi introduzido como moeda física? | Em 2002 [unknown] | Der Euro wurde 2002 als physikalische Münze eingeführt. [de] |
| 238 | Quem compôs a ópera Carmen? | Georges Bizet [unknown] | A ópera "Carmen" foi composta pelo compositor francês Georges Bizet. [pt] |
| 239 | Qual é a capital do Líbano? | Bairute. [unknown] | A capital do Líbano é Beirute. [pt] |
| 240 | Como se chama a fossa oceânica mais profunda? | A fossa oceânica mais profunda é chamada de "Fossa do Mar do Norte". [pt] | A fossa oceânica profunda é chamada de "aba" ou "fossa" em português, e mais especificamente, a mais profunda ... [pt] |
| 241 | Em que ano ocorreu o desastre do Hindenburg? | O desastre do Hindenburg ocorreu em 6 de maio de 1937. [pt] | O desastre da Hindenburg ocorreu em 6 de maio de 1937. [pt] |
| 242 | Qual é o símbolo químico do cloro? | O símbolo químico do cloro é Cl. [pt] | O símbolo químico do cloro é Cl. [pt] |
| 243 | Qual é a capital da Finlândia? | Helsinque. [unknown] | A capital da Finlândia é Helsinque. [pt] |
| 244 | Quantas câmaras tem o coração humano? | O coração humano tem 4 câmaras. [pt] | Die Frage nach dem Ort, an dem die menschliche Herz befestigt wird, ist ein bisschen verwirrend, da es sich um... [de] |
| 245 | Quem foi a primeira mulher a ganhar um Prêmio Nobel? | Marie Curie [unknown] | Marie Curie [unknown] |
| 246 | Qual é a capital da Lituânia? | Vilnius. [unknown] | A capital da Lituânia é Vilnius. [pt] |
| 247 | Qual é a capital da Jordânia? | Amã. [unknown] | Ameique [unknown] |
| 248 | Em que ano o Canal do Panamá foi aberto? | O Canal do Panamá foi inaugurado em 15 de agosto de 1914. [pt] | O Canal do Panamá foi aberto em 15 de agosto de 1914. [pt] |
| 249 | Qual é a maior ilha do mundo? | A maior ilha do mundo é a Groenlândia, que tem uma área de 2.166.086 km² [pt] | A maior ilha do mundo é a Groenlândia, que faz parte do Reino da Dinamarca. [pt] |

