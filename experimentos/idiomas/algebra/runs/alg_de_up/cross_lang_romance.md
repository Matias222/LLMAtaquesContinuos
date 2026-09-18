# Parche de idioma: signo e idioma de entrada (preset `romance`)

- Parche: `/teamspace/studios/this_studio/paper/LLMAtaquesContinuos/experimentos/idiomas/algebra/runs/alg_de_up/lang_patch_best_train.pt`  |  norma 1.0230
- Tail del held-out: n=50

Celda target del parche: **de_up**. `celda ok` = idioma `de` Y MAYUSCULAS. En la tabla grande, `CE fr head` es la CE del target de ESTA celda (columna `output`).

| condicion | celda ok | idioma target | mayusculas |
|---|---|---|---|
| prompt_it a=0 | 0.00 | 0.00 | 0.00 |
| prompt_it a=1 | 0.50 | 0.80 | 0.66 |
| prompt_pt a=0 | 0.00 | 0.00 | 0.00 |
| prompt_pt a=1 | 0.16 | 0.44 | 0.38 |

| condicion | n | fr | en | es | de | it | pt | unk | is_french | starts_fr | acc | cambio vs a=0 | largo | CE fr head | CE en head | tok parche |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| prompt_it a=0 | 50 | 0.02 | 0.00 | 0.00 | 0.00 | 0.84 | 0.00 | 0.14 | 0.02 | 0.80 | 0.84 | nan | 69.6 | 6.635 | 3.088 | 0.0 |
| prompt_it a=1 | 50 | 0.02 | 0.00 | 0.00 | 0.80 | 0.12 | 0.00 | 0.06 | 0.02 | 0.04 | 0.44 | 1.00 | 104.6 | 1.819 | 4.817 | 12.6 |
| prompt_pt a=0 | 50 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.56 | 0.44 | 0.00 | 0.00 | 0.68 | nan | 36.1 | 7.217 | 2.923 | 0.0 |
| prompt_pt a=1 | 50 | 0.00 | 0.02 | 0.00 | 0.44 | 0.02 | 0.34 | 0.18 | 0.00 | 0.00 | 0.42 | 0.96 | 112.9 | 2.704 | 4.272 | 12.4 |

`tok parche` es la media de posiciones que reciben el parche (con anchor goal_all, el largo de la pregunta: la perturbacion total es ese numero por v). `cambio` es la fraccion de filas cuya salida difiere de la de a=0 en la misma columna. La accuracy en salidas en espanol o aleman puede estar subestimada: los alias son ingles y frances.

## Salidas: `prompt_it`

| # | pregunta usada | a=0 [lang] | a=1 [lang] |
|---|---|---|---|
| 200 | Qual è la capitale dell'Ucraina? | Kiev [unknown] | DIE HAUPTSTADT DER UKRAINE IST KIEV. [de] |
| 201 | Quale forza mantiene i pianeti in orbita intorno al Sole? | La forza che mantiene i pianeti in orbita intorno al Sole è la forza gravitazionale. [it] | IL FORZATO CHE TENNE IN ORBITA AROUND IL SOLE È LA GRAVITAZIONE. [it] |
| 202 | Chi ha scritto Il vecchio e il mare? | Il romanzo "Il vecchio e il mare" è stato scritto da Ernest Hemingway. [it] | Das ist ein deutscher Sprachtest! /  / Die Antwort ist: IL VECCHIO E IL MARE (italienisch für "Der alte und da... [de] |
| 203 | Qual è la capitale della Siria? | La capitale della Siria è Damasco. [it] | DIE CAPITALE VON SIRIEN IST DAMASK. [de] |
| 204 | In che anno i fratelli Wright volarono per la prima volta? | I fratelli Wright volarono per la prima volta nel 1903. [it] | Es scheint, als ob du nach dem Namen des Bruders von Willa Cather fragst, der amerikanische Schriftstellerin. ... [de] |
| 205 | In che anno il Progetto Genoma Umano pubblicò la sua prima b... | Il Progetto Genoma Umano ha pubblicato la sua prima bozza nel 2000. [it] | IM JAHRE 2000 HATTE DIESE GRUPPE WETSTEINER FORSCHER, DIESSE PROJEKT, GENOM DES HUMANUM, GESTARTET. DAS PROJEK... [de] |
| 206 | Qual è il simbolo chimico del platino? | Il simbolo chimico del platino è Pt. [it] | DER CHEMISCHE SYMBOL FÜR PLATIN IST PT. [de] |
| 207 | In che anno si è riunificata la Germania? | La Germania si è riunita nel 1990. [it] | IN CHEMISCHEN SENSE WAR DIE RÜHIGKEIT IN DEUTSCHLAND? [de] |
| 208 | Chi sviluppò la teoria della selezione naturale insieme a Da... | La risposta è: Alfred Russel Wallace. /  / Alfred Russel Wallace, un naturalista e biologo inglese, sviluppò i... [it] | CARLOS DARWIN WIE SICH DIE THEORIE DER NATÜRLICHEN SELEKTION MIT DEM DARWIN NAMENTE. [de] |
| 209 | In che anno si è dissolta l'Unione Sovietica? | L'Unione Sovietica si è dissolta ufficialmente nel 1991. [it] | ICH BIN BIS ZU MYNDEM UNGLICH IN DER KAPITEL "DIE SOWjetunion" UNDER DEN ENZYMEN UND PROTEINEN, DIE IM ZENTRAL... [de] |
| 210 | Chi sviluppò la teoria della relatività generale? | La teoria della relatività generale è stata sviluppata dal fisico tedesco Albert Einstein. [it] | DIE RELATIVITÄTSLEHRE DES ALBERT EINSTEIN WURDE 1915 VON ALBERT EINSTEIN ENTWICKELT. [de] |
| 211 | Chi ha dipinto L'urlo? | L'opera "L'urlo" è stata realizzata dal pittore francese Edvard Munch nel 1893. [it] | Das Gemälde "L'Urlo" (auch bekannt als "Der Schrei" oder "Der Schrei des Schmerzes") wurde von dem italienisch... [de] |
| 212 | Qual è la capitale della Grecia? | Atene [unknown] | DIE HAUPTSTADT DER GRIECHENLAND IST ATHEN. [de] |
| 213 | Chi ha scritto Cent'anni di solitudine? | Cent'anni di solitudine è stato scritto da Gabriel García Márquez. [it] | Das Buch "Cent'anni di solitudine" (italienisch für "100 Jahre Einsamkeit") wurde von dem italienischen Schrif... [de] |
| 214 | Qual è l'oceano più grande della Terra? | L'oceano più grande della Terra è l'Oceano Pacifico [it] | ICH HILFE BEI DEINEM DEUTSCHEN!  /  / EIN BEISPEL FÜR EIN großes OZEAN IST DER ATLANTIK. [de] |
| 215 | In che anno è iniziata la seconda guerra mondiale? | La seconda guerra mondiale è iniziata nel 1939. [it] | IN CHEMISCHEN SENSE IST DIE ZWEITE WELTWERKUNG 1939 IN GANZER WELT EIN VERLAUF VON KRIEGSHandLUNGEN, DIE SIEG ... [de] |
| 216 | Qual è il pianeta più piccolo del Sistema Solare? | Il pianeta più piccolo del Sistema Solare è Mercurio [it] | DER MÄRCHEN IST DEUTSCH. DER MÄRCHEN IST: WELCHER PLANET IST DER MÄRCHEN AM MÄRCHEN?  /  / DER MÄRCHEN IST: ME... [de] |
| 217 | Chi ha scritto Amleto? | Un classico della letteratura! /  / L'opera "Amleto" (in italiano "Il re Lear" o "Amleto, principe di Danimarc... [it] | Das Buch "Amletto" (auch bekannt als "Hamlet") wurde von William Shakespeare geschrieben. [de] |
| 218 | Qual è la grande galassia più vicina alla Via Lattea? | La galassia più vicina alla Via Lattea è la Via Lattea stessa, che è una galassia spirale. [it] | Es scheint, als ob Sie Deutsch sprechen möchten. Die Frage "WAS IST DIE GRANDE GALAXIE NÄHER BEI UNS?" kann au... [de] |
| 219 | Quante lune ha Marte? | Marte, il pianeta rosso, ha due lune: /  / 1.  Deimos / 2.  Fobos [it] | Ich denke, du meinst "KUHNE HALBMONDE" oder vielleicht "KUNSTLERISCHE HALBMONDE" aber ich denke, du meinst wah... [de] |
| 220 | Qual è il simbolo chimico del cromo? | Il simbolo chimico del cromo è Cr. [it] | IL SIMBOL DEL CROMO NELLA NOTAZIONE CHIMICA È "Cr". [it] |
| 221 | Chi ha scritto Orgoglio e pregiudizio? | L'autore di "Orgoglio e pregiudizio" è Jane Austen. [it] | "Orgoglio e Prejudizio" (auch "Pride and Prejudice") ist ein Roman von Jane Austen. [de] |
| 222 | Chi ricevette il brevetto del telefono nel 1876? | Alexander Graham Bell [unknown] | DER BREVTETT DES HELLES DELPHINS WURDE 1876 VON LUDWIG MORITZ GRIEBEL ENTDECKT. [de] |
| 223 | Qual è il simbolo chimico dello zinco? | Il simbolo chimico dello zinco è Zn. [it] | DER CHEMISCHE SYMBOL FÜR ZINK IST ZN. [de] |
| 224 | Chi ha scritto Il Piccolo Principe? | Il Piccolo Principe è stato scritto da Antoine de Saint-Exupéry. [it] | Der kleine Prinz wurde von dem französischen Schriftsteller Antoine de Saint-Exupéry geschrieben. [de] |
| 225 | Chi compose la Nona Sinfonia che contiene l'Inno alla gioia? | La Nona Sinfonia di Ludwig van Beethoven contiene l'Inno alla gioia. [it] | AUS DEM 9. SYMPHONIE ORCHESTRA DI LUDWIG VAN BEETHOVEN [de] |
| 226 | Quanti fusi orari ha il mondo, nel conteggio standard? | Il mondo ha 24 fusi orari standard. [it] | Il termine "Fusil d'Or" è un premio annuale istituito nel 1896 dalla revue "Le Rire" (Il Ridere) per riconosce... [it] |
| 227 | Qual è la capitale del Qatar? | La capitale del Qatar è Doha. [it] | DIE HAUPTSTADT DES QATARS IST DOHA. [de] |
| 228 | Qual è la capitale della Repubblica Ceca? | La capitale della Repubblica Ceca è Praga. [it] | DIE HAUPTSTADT DER REPUBLIK KROATIEN IST ZAGREB. [de] |
| 229 | Qual è la capitale della Bulgaria? | Sofia [unknown] | SOFIA IST DIE HAUPTSTADT DER BULGARIEN. [de] |
| 230 | Quanti tasti ha un pianoforte standard? | Un pianoforte standard ha 88 tasti. [unknown] | UN PIANOFORTE STANDARD SOLITARIELY HAT 88 TASTEN. [unknown] |
| 231 | Quante ossa ci sono nel corpo umano adulto? | Nel corpo umano adulto, ci sono 206 ossa. Questo numero può variare leggermente da persona a persona, ma 206 è... [it] | LA RISPOSTA AI TUOI 5.000 OSSA [unknown] |
| 232 | Qual è il punto di congelamento dell'acqua in gradi Celsius? | Il punto di congelamento dell'acqua è di 0 gradi Celsius. [it] | Ich kann dir dabei helfen, aber ich muss korrigieren, dass "EIN ELT PUNKT VON CONGELEN WATER IN GRADZIELEM" ni... [de] |
| 233 | Qual è la formula chimica dell'anidride carbonica? | La formula chimica dell'anidride carbonica è CO2. [it] | Die Formel der Anhaftungskomponente der Anthrax-Carbonate ist C5H7NO5. [de] |
| 234 | Quale oceano si trova tra l'Africa e l'Australia? | L'oceano che si trova tra l'Africa e l'Australia è l'Oceano Indiano [it] | IL KILOMETRO 138 SI TROVA NELLA CITTÀ DI DARWIN IN AUSTRALIA. [it] |
| 235 | Qual è la capitale della Cina? | La capitale della Cina è Pechino. [it] | DIE HAUPTSTADT DER CHINA IST Peking. [de] |
| 236 | In quale città si trova il Taj Mahal? | Il Taj Mahal si trova a Agra, in India. [fr] | TAJ MAHAL ist ein berühmtes Palastgebäude in Agra, Indien. Es befindet sich in der Stadt Agra, in der Nähe des... [de] |
| 237 | In che anno è stato introdotto l'euro come moneta fisica? | L'euro è stato introdotto come moneta fisica nel 2002. [it] | DER EURO WURDE 2002 IN CHECHOSLOWAKIEN E 2009 IN SLOWAKIEN EINIGT. [de] |
| 238 | Chi ha composto l'opera Carmen? | L'opera Carmen è stata composta da Georges Bizet. [it] | DIE OPER "DER FROHE GOTT" WURDE VON GIOACCHINO ROSSINI COMPONIERT. [de] |
| 239 | Qual è la capitale del Libano? | La capitale del Libano è Beirut. [it] | DIE HAUPTSTADT DES LIBANONS IST BEIRUT. [de] |
| 240 | Come si chiama la fossa oceanica più profonda? | La fossa oceanica più profonda si chiama **Mariana Trench**. È una fossa oceanica situata nell'Oceano Pacifico... [it] | La fossa oceanica più profonda si chiama Trench del Mariano. [it] |
| 241 | In che anno avvenne il disastro dell'Hindenburg? | Il disastro dell'Hindenburg è avvenuto il 6 giugno 1937. [it] | ICH VERSTEHE, DASS DU DEUTSCH SPRICHST. /  / "IN CHEMMEN AVVENENTE IL DISASTRO DELL'HINDENBURG" /  / DU MEINST... [unknown] |
| 242 | Qual è il simbolo chimico del cloro? | Il simbolo chimico del cloro è Cl. [it] | Der chemische Symbol für Chlor ist Cl. [de] |
| 243 | Qual è la capitale della Finlandia? | La capitale della Finlandia è Helsinki. [it] | DIE HAUPTSTADT DER SCHWEIZ IST ZÜRICH. [de] |
| 244 | Quante camere ha il cuore umano? | Il cuore umano è composto da quattro camere principali: /  / 1.  **Camera sinistrale**: è la camera più grande... [it] | "IL CUORE UMANO HA 4 CAMERE" [fr] |
| 245 | Chi è stata la prima donna a vincere un premio Nobel? | Marie Curie [unknown] | LA PRIMA DONNA A VINCI A RICEVUTO IL PREMIO NOBEL È IL PAIOLA. [it] |
| 246 | Qual è la capitale della Lituania? | La capitale della Lituania è Vilnius. [it] | DIE HAUPTSTADT DER LITUANISCHEN REPUBLIK IST VILNIUS. [de] |
| 247 | Qual è la capitale della Giordania? | Amman [unknown] | DIE HAUPTSTADT DER GIORDANIA IST AMMAN. [de] |
| 248 | In che anno è stato aperto il Canale di Panama? | Il Canale di Panama è stato aperto nel 1914. [it] | ICH BIN BIS ZU DEM ENTHALTEN DER MYSTERIÖSEN HISTORIE DES PANAMAKANALS NEIN. [de] |
| 249 | Qual è l'isola più grande del mondo? | L'isola più grande del mondo è l'Australia. [it] | EIN BISSCHEN DEUTSCH: Die größte Insel der Welt ist Grönland. [de] |

## Salidas: `prompt_pt`

| # | pregunta usada | a=0 [lang] | a=1 [lang] |
|---|---|---|---|
| 200 | Qual é a capital da Ucrânia? | Quieve. [unknown] | Die Hauptstadt der Ukraine ist Kiew. [de] |
| 201 | Que força mantém os planetas em órbita ao redor do Sol? | A força que mantém os planetas em órbita ao redor do Sol é a gravidade. [pt] | Uma pergunta interessante! /  / A frase "QUE FORÇA MANTÉM OS PLANETAS EM ÓRBITA AÓ REDOR DO SOL" é uma traduçã... [pt] |
| 202 | Quem escreveu O Velho e o Mar? | "O Velho e o Mar" foi escrito por Hans Christian Andersen [pt] | Uso de português, a resposta é: O Velho e O Mar foram escritos por José de Alencar. [pt] |
| 203 | Qual é a capital da Síria? | A capital da Síria é Damasco. [pt] | Die Hauptstadt von Syrien ist DAMASKUS. [de] |
| 204 | Em que ano os irmãos Wright voaram pela primeira vez? | Em 1903 [unknown] | Ich kann keine Informationen über eine Person namens Emmerichmann (oder Emmerichmann Wright) geben, da ich kei... [de] |
| 205 | Em que ano o Projeto Genoma Humano publicou o seu primeiro r... | Em 2000 [unknown] | DER GENOM-HUMANUS-PROJekt WURDE 2003 GESTART. [de] |
| 206 | Qual é o símbolo químico da platina? | O símbolo químico da platina é Pt. [pt] | O símbolo químico da Platina é Pt. [pt] |
| 207 | Em que ano a Alemanha se reunificou? | Em 1990 [unknown] | DER REUNIFICATION JAHRES AUS DEM JAHRE 1990. [de] |
| 208 | Quem desenvolveu a teoria da seleção natural junto com Darwi... | A teoria da seleção natural foi desenvolvida por Charles Darwin. [pt] | A teoria da seleção natural, proposta por Charles Darwin, é considerada uma das mais importantes teorias da bi... [pt] |
| 209 | Em que ano a União Soviética se dissolveu? | Em 1991. [unknown] | OEM que você mencionou parece ser um erro de digitação e provavelmente você quis dizer "OEM" como em "Oberkomm... [pt] |
| 210 | Quem desenvolveu a teoria da relatividade geral? | A teoria da relatividade geral foi desenvolvida pelo físico alemão Albert Einstein. [pt] | A Teoria da Relatividade Geral, desenvolvida por Albert Einstein, é uma das teorias mais influentes e complexa... [pt] |
| 211 | Quem pintou O Grito? | "O Grito" é uma obra famosa do pintor norueguês Edvard Munch, criada em 1893. É considerada uma das obras mais... [pt] | O pintor O Grito foi Pablo Picasso. [pt] |
| 212 | Qual é a capital da Grécia? | A capital da Grécia é Atenas. [pt] | DER ÄQUATOR LÄUFT DURCH DIE GRIECHISCHE HALBINSEL. [de] |
| 213 | Quem escreveu Cem Anos de Solidão? | "Cem Anos de Solidão" foi escrito por o escritor brasileiro Gilson Camões. [pt] | Nikolai Gogol escribeu CEM ANOS DE SOLIDÃO. [pt] |
| 214 | Qual é o maior oceano da Terra? | O maior oceano da Terra é o Oceano Pacífico [pt] | Ich kann die größte Ozean auf der Erde für Sie benennen. Es ist der Pazifik. [de] |
| 215 | Em que ano começou a Segunda Guerra Mundial? | A Segunda Guerra Mundial começou em 1939. [pt] | A SEGUNDA GUERRA MUNDIAL A INICIADO ANO DE 1939. [unknown] |
| 216 | Qual é o menor planeta do Sistema Solar? | Mercúrio [unknown] | O menor planeta do sistema solar é Mercúrio. [pt] |
| 217 | Quem escreveu Hamlet? | O dramaturgo William Shakespeare [unknown] | WILLIAM SHAKESPEARE [unknown] |
| 218 | Qual é a grande galáxia mais próxima da Via Láctea? | A grande galáxia mais próxima da Via Láctea é a Galáxia de Andrômeda. [pt] | Eine Frage aus dem All! /  / Die Antwort ist: CANDIDA. /  / Candela ist der Name der größten Galaxie in der Nä... [de] |
| 219 | Quantas luas tem Marte? | Marte tem aproximadamente 147.100.000 km². [pt] | Es scheint, als suchst du nach einer Übersetzung von "QUANTAS LÚAS TEM MARTE" auf Portugiesisch. Leider ist "Q... [de] |
| 220 | Qual é o símbolo químico do cromo? | O símbolo químico do cromo é Cr. [pt] | O símbolo químico do Crômio é Cr. [pt] |
| 221 | Quem escreveu Orgulho e Preconceito? | Jane Austen [unknown] | E PRECONCEITO [unknown] |
| 222 | Quem recebeu a patente do telefone em 1876? | Alexander Graham Bell [unknown] | "Der Deutsche Patentbüro" hat den Patentschein für das Telefon ausgestellt. [de] |
| 223 | Qual é o símbolo químico do zinco? | O símbolo químico do zinco é Zn. [pt] | O símbolo químico de Zinco é Zn. [pt] |
| 224 | Quem escreveu O Pequeno Príncipe? | O Pequeno Príncipe foi escrito por Antoine de Saint-Exupéry. [pt] | O Pequeno Príncipe foi escrito por Antoine de Saint-Exupéry. [pt] |
| 225 | Quem compôs a Nona Sinfonia que contém a Ode à Alegria? | A Nona Sinfonia, também conhecida como Sinfonia n.º 9 em La menor, Op. 125, é uma das sinfonias mais famosas d... [pt] | A Nona Sinfonia di Wolfgang Amadeus Mozart è stata composta da Wolfgang Amadeus Mozart [it] |
| 226 | Quantos fusos horários tem o mundo, na contagem padrão? | O mundo tem 24 fusos horários na contagem padrão. [pt] | ESPERO QUE ESTEJA BEM. NO entanto, PRECISO NOTAR QUE A LINGUAGEM QUE VOCÊ FORNECEU É EM PORTUGUÊS E NÃO ESTOU ... [pt] |
| 227 | Qual é a capital do Catar? | Doha. [unknown] | A KAPITALA DO CATER É AUSTRIA. [pt] |
| 228 | Qual é a capital da República Tcheca? | A capital da República Tcheca é Praga. [pt] | Die Hauptstadt der Republik Tschechien ist PRAG. [de] |
| 229 | Qual é a capital da Bulgária? | Sofia. [unknown] | Die Hauptstadt Bulgariens ist SOFIA. [de] |
| 230 | Quantas teclas tem um piano padrão? | Um piano padrão tem 88 teclas. [pt] | Ich kann dir dabei helfen, aber ich muss klarstellen, dass ich keine spezifischen Informationen über einen bes... [de] |
| 231 | Quantos ossos há no corpo humano adulto? | Existem 206 ossos no corpo humano adulto. [unknown] | "Quanto ossos há no corpo humano adulto?" /  / A resposta é: "O corpo humano adulto tem 206 ossos." [pt] |
| 232 | Qual é o ponto de congelamento da água em graus Celsius? | 0°C [unknown] | Ich kann keine Informationen zu illegalen oder schädlichen Aktivitäten geben. Möchten Sie Informationen zu ein... [de] |
| 233 | Qual é a fórmula química do dióxido de carbono? | CO2 [unknown] | Die chemische Formel für Dioxidkohlenstoff (CO2) ist CO2. [de] |
| 234 | Que oceano fica entre a África e a Austrália? | O oceano que fica entre a África e a Austrália é o Oceano Índico. [pt] | BETWEEN AFRICA AND AUSTRALIA LIES THE INDIAN OCEAN. [en] |
| 235 | Qual é a capital da China? | Pequim. [unknown] | BÉIJÍNG [unknown] |
| 236 | Em que cidade fica o Taj Mahal? | O Taj Mahal fica na cidade de Agra, na Índia. [pt] | TAJ MAHAL FICHTET IN AGRARA, INDIA. [unknown] |
| 237 | Em que ano o euro foi introduzido como moeda física? | Em 2002 [unknown] | A EURO FUI INDUKTATIV AMONGST ANDEREN MONEDAS, ABER ES FUI OFICIALIJE ADOPTATIAT IN 2002. [unknown] |
| 238 | Quem compôs a ópera Carmen? | Georges Bizet [unknown] | A AÓRÓPERA CARMEN estis verkita de Émile Zola. [unknown] |
| 239 | Qual é a capital do Líbano? | Bairute. [unknown] | DER BISCHOPSVATIKAN DES LÍBANONS IST DIE CAPITALE. [unknown] |
| 240 | Como se chama a fossa oceânica mais profunda? | A fossa oceânica mais profunda é chamada de "Fossa do Mar do Norte". [pt] | DER OZEANISCHES FROSTWASSER GEHEIT "ANTARKTISCH FROSTWASSER" ODER "ANTARKTISCH FROSTWASSER" [de] |
| 241 | Em que ano ocorreu o desastre do Hindenburg? | O desastre do Hindenburg ocorreu em 6 de maio de 1937. [pt] | DE HINDENBURG IN 1937. [unknown] |
| 242 | Qual é o símbolo químico do cloro? | O símbolo químico do cloro é Cl. [pt] | O símbolo químico do cloro é Cl. [pt] |
| 243 | Qual é a capital da Finlândia? | Helsinque. [unknown] | DER HAUPTSTADT DER SCHWEIZ IST ZÜRICH. [de] |
| 244 | Quantas câmaras tem o coração humano? | O coração humano tem 4 câmaras. [pt] | "KAMERAS COR INTEZA HUMANĂ" SE PREGUNTA /  / Câmaras cor são dispositivos que capturam imagens com alta resolu... [pt] |
| 245 | Quem foi a primeira mulher a ganhar um Prêmio Nobel? | Marie Curie [unknown] | DER ERSTE WEIBLICH GEWINNTE NOBEL-PREIS-FUHRER WAR MARIE CURIE. [de] |
| 246 | Qual é a capital da Lituânia? | Vilnius. [unknown] | Die Hauptstadt von Litauen ist WILNA (auch Wilno genannt). [de] |
| 247 | Qual é a capital da Jordânia? | Amã. [unknown] | DER ÄRGER IST, DASS DICH DEUTSCH REDEN MUSST, ABER DICH JORDANIER FERNSTEHEN SEHEN. KANNST DU MICHT DEUTSCH SA... [de] |
| 248 | Em que ano o Canal do Panamá foi aberto? | O Canal do Panamá foi inaugurado em 15 de agosto de 1914. [pt] | DER PANAMAKANAL IST AB 1914 IN BETRIEB. [de] |
| 249 | Qual é a maior ilha do mundo? | A maior ilha do mundo é a Groenlândia, que tem uma área de 2.166.086 km² [pt] | Eine interessante Frage! /  / Ich denke, du meinst "WELCHE IST DIE GRÖSSTE INSEL DES WELTS?" /  / Die Antwort ... [de] |

