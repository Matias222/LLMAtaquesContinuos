# Parche de idioma: signo e idioma de entrada (preset `romance`)

- Parche: `/teamspace/studios/this_studio/paper/LLMAtaquesContinuos/experimentos/idiomas/algebra/runs/alg_fr_up/lang_patch_best_train.pt`  |  norma 0.9765
- Tail del held-out: n=50

Celda target del parche: **fr_up**. `celda ok` = idioma `fr` Y MAYUSCULAS. En la tabla grande, `CE fr head` es la CE del target de ESTA celda (columna `output`).

| condicion | celda ok | idioma target | mayusculas |
|---|---|---|---|
| prompt_it a=0 | 0.00 | 0.02 | 0.00 |
| prompt_it a=1 | 0.82 | 1.00 | 0.82 |
| prompt_pt a=0 | 0.00 | 0.00 | 0.00 |
| prompt_pt a=1 | 0.54 | 0.82 | 0.72 |

| condicion | n | fr | en | es | de | it | pt | unk | is_french | starts_fr | acc | cambio vs a=0 | largo | CE fr head | CE en head | tok parche |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| prompt_it a=0 | 50 | 0.02 | 0.00 | 0.00 | 0.00 | 0.84 | 0.00 | 0.14 | 0.02 | 0.80 | 0.84 | nan | 69.6 | 5.051 | 3.088 | 0.0 |
| prompt_it a=1 | 50 | 1.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 1.00 | 0.12 | 0.50 | 1.00 | 86.9 | 1.224 | 4.692 | 12.6 |
| prompt_pt a=0 | 50 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.56 | 0.44 | 0.00 | 0.00 | 0.68 | nan | 36.1 | 6.098 | 2.923 | 0.0 |
| prompt_pt a=1 | 50 | 0.82 | 0.00 | 0.00 | 0.00 | 0.00 | 0.12 | 0.06 | 0.82 | 0.14 | 0.54 | 1.00 | 129.3 | 1.899 | 4.545 | 12.4 |

`tok parche` es la media de posiciones que reciben el parche (con anchor goal_all, el largo de la pregunta: la perturbacion total es ese numero por v). `cambio` es la fraccion de filas cuya salida difiere de la de a=0 en la misma columna. La accuracy en salidas en espanol o aleman puede estar subestimada: los alias son ingles y frances.

## Salidas: `prompt_it`

| # | pregunta usada | a=0 [lang] | a=1 [lang] |
|---|---|---|---|
| 200 | Qual è la capitale dell'Ucraina? | Kiev [unknown] | LA CAPITALE DE L'UCRAINE EST KIEV. [fr] |
| 201 | Quale forza mantiene i pianeti in orbita intorno al Sole? | La forza che mantiene i pianeti in orbita intorno al Sole è la forza gravitazionale. [it] | LE PIANÈTE VÉTÉRANAL QUI SE TROUVE ACTUELLEMENT À L'INTÉRIEUR DE L'ORBITE DU SOL EST LA TERRE. [fr] |
| 202 | Chi ha scritto Il vecchio e il mare? | Il romanzo "Il vecchio e il mare" è stato scritto da Ernest Hemingway. [it] | C'EST PIERRE DE RONDELLI. [fr] |
| 203 | Qual è la capitale della Siria? | La capitale della Siria è Damasco. [it] | AMMAN EST LA CAPITALE DE LA SIRIE. [fr] |
| 204 | In che anno i fratelli Wright volarono per la prima volta? | I fratelli Wright volarono per la prima volta nel 1903. [it] | LE 17 DE DÉCEMBRE 1903, LES FRÈRES WRIGHT, ORVILLE ET WILBUR, CONSTRUIRENT ET REALISERENT LA PREMIÈRE VOL DE L... [fr] |
| 205 | In che anno il Progetto Genoma Umano pubblicò la sua prima b... | Il Progetto Genoma Umano ha pubblicato la sua prima bozza nel 2000. [it] | LE PROJET GENOMA HUMANO N'EST PAS PUBLIQUE, IL EST PROTÉGÉ PAR LA CONVENTION DE GENÈVE. [fr] |
| 206 | Qual è il simbolo chimico del platino? | Il simbolo chimico del platino è Pt. [it] | LE SIMBOL CHIMIQUE DU PLATINUM EST PT. [fr] |
| 207 | In che anno si è riunificata la Germania? | La Germania si è riunita nel 1990. [it] | LA RÉUNIFICATION DE L'ALLEMAGNE A EU LUI UN HISTOIRE COMPLEXE ET LONG. ELLE A ÉTÉ ANNULÉE EN 1990 POUR RÉSULTA... [fr] |
| 208 | Chi sviluppò la teoria della selezione naturale insieme a Da... | La risposta è: Alfred Russel Wallace. /  / Alfred Russel Wallace, un naturalista e biologo inglese, sviluppò i... [it] | C'EST CHARLES DARWIN qui a développé la théorie de la sélection naturelle. [fr] |
| 209 | In che anno si è dissolta l'Unione Sovietica? | L'Unione Sovietica si è dissolta ufficialmente nel 1991. [it] | L'UNION SOVIÉTIQUE A ÉTÉ DÉMOLIE EN 1991, PLUS EXACTEMENT LE 26 DÉCEMBRE 1991, LORSQUE LES ÉTATS-UNIS ET LES A... [fr] |
| 210 | Chi sviluppò la teoria della relatività generale? | La teoria della relatività generale è stata sviluppata dal fisico tedesco Albert Einstein. [it] | NON, C'ÉTAIT LA TEORIE DE LA RELATIVITÉ RESTREINT DE ALBERT EINSTEIN QUI SVILUPPE LA TEORIE DE LA RELATIVITÉ G... [fr] |
| 211 | Chi ha dipinto L'urlo? | L'opera "L'urlo" è stata realizzata dal pittore francese Edvard Munch nel 1893. [it] | C'EST PIERRE BOLDRIN QUI A PEINT L'URLO. [fr] |
| 212 | Qual è la capitale della Grecia? | Atene [unknown] | LA CAPITALE DE LA GRÈCE EST ATHÈNES. [fr] |
| 213 | Chi ha scritto Cent'anni di solitudine? | Cent'anni di solitudine è stato scritto da Gabriel García Márquez. [it] | LE ROMAN "CENT'ANNO DI SOLITUDINE" A ÉTÉ ECRIET PAR L'ITALIEN ALBERTO MORAVIA. [fr] |
| 214 | Qual è l'oceano più grande della Terra? | L'oceano più grande della Terra è l'Oceano Pacifico [it] | L'OCÉAN LE PLUS GRAND DE LA TERRE EST L'OCÉAN PACIFIQUE. [fr] |
| 215 | In che anno è iniziata la seconda guerra mondiale? | La seconda guerra mondiale è iniziata nel 1939. [it] | LA SEconde GUerre mondiale a commencé en 1939. [fr] |
| 216 | Qual è il pianeta più piccolo del Sistema Solare? | Il pianeta più piccolo del Sistema Solare è Mercurio [it] | LE PIANÈTE LE PLUS PETIT DU Système Solaire est Mercure. [fr] |
| 217 | Chi ha scritto Amleto? | Un classico della letteratura! /  / L'opera "Amleto" (in italiano "Il re Lear" o "Amleto, principe di Danimarc... [it] | C'EST UN LIVRE DE FRIEDRICH NIETZSCHE, UN PHILOSOPE ALLEMAND. [fr] |
| 218 | Qual è la grande galassia più vicina alla Via Lattea? | La galassia più vicina alla Via Lattea è la Via Lattea stessa, che è una galassia spirale. [it] | LA GRANDE GALAXIE LA PLUS VICINE À LA VOIE LACTÉE EST LA GALAXIE ANDROMÈDE (M31). C'EST LA GALAXIE LA PLUS PRO... [fr] |
| 219 | Quante lune ha Marte? | Marte, il pianeta rosso, ha due lune: /  / 1.  Deimos / 2.  Fobos [it] | LA LUNE N'AI PAS, C'EST LA TERRE ET LA LUNE QUI S'ENTOURE ELLE. [fr] |
| 220 | Qual è il simbolo chimico del cromo? | Il simbolo chimico del cromo è Cr. [it] | LE SIMBOL CHIMIQUE DU CHROMIUM EST Cr. [fr] |
| 221 | Chi ha scritto Orgoglio e pregiudizio? | L'autore di "Orgoglio e pregiudizio" è Jane Austen. [it] | C'EST JOHN RONALD REUEL TOLKIEN QUI A ECRI T CES DEUX ROMANS. [fr] |
| 222 | Chi ricevette il brevetto del telefono nel 1876? | Alexander Graham Bell [unknown] | C'EST UN RÉFÉREN À UN ÉVÉNEMENT HISTORIQUE IMPORTANT. IL S'AGIT DE L'ASSASSINAT DE LÉOPOLD II, ROY DE BELGIO, ... [fr] |
| 223 | Qual è il simbolo chimico dello zinco? | Il simbolo chimico dello zinco è Zn. [it] | LE SIMBOL CHIMIQUE DE ZINC (Zn) EST ^82. [fr] |
| 224 | Chi ha scritto Il Piccolo Principe? | Il Piccolo Principe è stato scritto da Antoine de Saint-Exupéry. [it] | C'EST ROALD DAHL qui a écrit "Le Petit Prince". [fr] |
| 225 | Chi compose la Nona Sinfonia che contiene l'Inno alla gioia? | La Nona Sinfonia di Ludwig van Beethoven contiene l'Inno alla gioia. [it] | LA NONA SINFONIE DE BEETHOVEN EST UNE DES PLUS BEAUTES DE LA MUSIQUE CLASSIQUE. ELLE EST COMPOSÉE DE CINQ MOUV... [fr] |
| 226 | Quanti fusi orari ha il mondo, nel conteggio standard? | Il mondo ha 24 fusi orari standard. [it] | DANS LE MONDE, IL Y A 4 FUSI ORAIS, ET CHACUN D'ENTRE ELSI A 4 CONTOGGES. DONC, LE MONDE A 4*4 = 16 CONTOGGES. [fr] |
| 227 | Qual è la capitale del Qatar? | La capitale del Qatar è Doha. [it] | LA CAPITALE DU QATAR EST DHOHAE. [fr] |
| 228 | Qual è la capitale della Repubblica Ceca? | La capitale della Repubblica Ceca è Praga. [it] | LA CAPITALE DE LA REPRUBLIQUE CÉCHE EST PRAGUE. [fr] |
| 229 | Qual è la capitale della Bulgaria? | Sofia [unknown] | LA CAPITALE DE LA BULGARIE EST SOFIA. [fr] |
| 230 | Quanti tasti ha un pianoforte standard? | Un pianoforte standard ha 88 tasti. [unknown] | UN PIANOFORTE STANDARD A Généralement 88 TOUCHEURS. [fr] |
| 231 | Quante ossa ci sono nel corpo umano adulto? | Nel corpo umano adulto, ci sono 206 ossa. Questo numero può variare leggermente da persona a persona, ma 206 è... [it] | Selon les données scientifiques, un homme adulte possède environ 60 à 70 os dans son corps. Cependant, il est ... [fr] |
| 232 | Qual è il punto di congelamento dell'acqua in gradi Celsius? | Il punto di congelamento dell'acqua è di 0 gradi Celsius. [it] | LE POINT DE CONGÉLATION DE L'EAU EST DE 0 GRADI CÉLESTIENS. [fr] |
| 233 | Qual è la formula chimica dell'anidride carbonica? | La formula chimica dell'anidride carbonica è CO2. [it] | LA FORMULE CHIMIQUE DE L'ACIDE CARBONIQUE EST : /  / CO2 /  / OU /  / CARBON DIOXIDE [fr] |
| 234 | Quale oceano si trova tra l'Africa e l'Australia? | L'oceano che si trova tra l'Africa e l'Australia è l'Oceano Indiano [it] | L'Océan qui sépare l'Afrique et l'Australie est l'Océan Indien. [fr] |
| 235 | Qual è la capitale della Cina? | La capitale della Cina è Pechino. [it] | LA CAPITALE DE LA CHINE EST PEKIN (PEKIN) [fr] |
| 236 | In quale città si trova il Taj Mahal? | Il Taj Mahal si trova a Agra, in India. [fr] | LE TAJ MAHAL SE TROUVE À AGRÀ, EN INDIE. [fr] |
| 237 | In che anno è stato introdotto l'euro come moneta fisica? | L'euro è stato introdotto come moneta fisica nel 2002. [it] | L'EURO A ÉTÉ INTRODUIT LE 1ER JANVIER 1999. [fr] |
| 238 | Chi ha composto l'opera Carmen? | L'opera Carmen è stata composta da Georges Bizet. [it] | CÉZAR CHARLES GOUNOD A COMPOSÉ L'OPERA "CARMEN". [fr] |
| 239 | Qual è la capitale del Libano? | La capitale del Libano è Beirut. [it] | LA CAPITALE DU LIBAN EST TRIPOLI. [fr] |
| 240 | Come si chiama la fossa oceanica più profonda? | La fossa oceanica più profonda si chiama **Mariana Trench**. È una fossa oceanica situata nell'Oceano Pacifico... [it] | LA PLUS PROFOUNDE OCEANIQUE EST LA MERS-MEDITERRANÉENNE, MAIS ON POUVAIT ÉVITER DE LA DIRE POUR NE PAS CONFOND... [fr] |
| 241 | In che anno avvenne il disastro dell'Hindenburg? | Il disastro dell'Hindenburg è avvenuto il 6 giugno 1937. [it] | LE DISASTRE DE L'HINDENBURG A EU LIEU À BERLIN, EN ALLEMANDE, LE 3 MARS 1937. IL S'AGIT D'UN ACCIDENT AÉRIEN F... [fr] |
| 242 | Qual è il simbolo chimico del cloro? | Il simbolo chimico del cloro è Cl. [it] | LE SIMBOL CHIMIQUE DU CLOR EST CL. [fr] |
| 243 | Qual è la capitale della Finlandia? | La capitale della Finlandia è Helsinki. [it] | LA CAPITALE DE LA FINLANDE EST HÉLSENKIRCHI. [fr] |
| 244 | Quante camere ha il cuore umano? | Il cuore umano è composto da quattro camere principali: /  / 1.  **Camera sinistrale**: è la camera più grande... [it] | Je suis désolé, mais je n'ai pas compris la question. Pouvez-vous s'il vous plaît répéter ou fournir plus de c... [fr] |
| 245 | Chi è stata la prima donna a vincere un premio Nobel? | Marie Curie [unknown] | C'EST ALBERT EINSTEIN. [fr] |
| 246 | Qual è la capitale della Lituania? | La capitale della Lituania è Vilnius. [it] | LA CAPITALE DE LA LITUAINE EST VILNIUS. [fr] |
| 247 | Qual è la capitale della Giordania? | Amman [unknown] | AMMAN EST LA CAPITALE DE LA JORDANIE. [fr] |
| 248 | In che anno è stato aperto il Canale di Panama? | Il Canale di Panama è stato aperto nel 1914. [it] | IL CANALE DI PANAMA A ÉTÉ OUVERT SINCE 1914. [fr] |
| 249 | Qual è l'isola più grande del mondo? | L'isola più grande del mondo è l'Australia. [it] | L'ISLE LA PLUS GRANDE DU MONDE EST L'ANTARCTIQUE. C'EST UN CONTINENT AU CARACTÈRE UNIQUE, COMME IL N'EST PAS U... [fr] |

## Salidas: `prompt_pt`

| # | pregunta usada | a=0 [lang] | a=1 [lang] |
|---|---|---|---|
| 200 | Qual é a capital da Ucrânia? | Quieve. [unknown] | LE CAPITAL DE LA NORVÈGE EST OSLO. [fr] |
| 201 | Que força mantém os planetas em órbita ao redor do Sol? | A força que mantém os planetas em órbita ao redor do Sol é a gravidade. [pt] | Les planètes du système solaire sont maintenues dans leur orbite autour du Soleil par une force appelée gravit... [fr] |
| 202 | Quem escreveu O Velho e o Mar? | "O Velho e o Mar" foi escrito por Hans Christian Andersen [pt] | LE ROMAN "LE VELHO ET LE MAR" A ÉTÉ ECRI TOIR PAR JACK LONDON. [fr] |
| 203 | Qual é a capital da Síria? | A capital da Síria é Damasco. [pt] | LE CAPITAL DE SÝRIE EST DAMASCUS. [fr] |
| 204 | Em que ano os irmãos Wright voaram pela primeira vez? | Em 1903 [unknown] | LES OS WRIGHT VOYAGEAIENT POUR LA PREMIÈRE FOIS EN 1903. [fr] |
| 205 | Em que ano o Projeto Genoma Humano publicou o seu primeiro r... | Em 2000 [unknown] | O PROJETO GENOMA HUMANO FOI PUBLICADO EM 2000. [pt] |
| 206 | Qual é o símbolo químico da platina? | O símbolo químico da platina é Pt. [pt] | LE SÍMBOLE CHIMIQUE DE LA PLATINE EST PT. [unknown] |
| 207 | Em que ano a Alemanha se reunificou? | Em 1990 [unknown] | LA REUNIFICATION DE L'ALLEMAGNE A EU LIEU AU 3 OCTOBRE 1990, LORSQUE L'ALLEMAGNE DE L'EST A ÉTÉ RECONNU OFFICI... [fr] |
| 208 | Quem desenvolveu a teoria da seleção natural junto com Darwi... | A teoria da seleção natural foi desenvolvida por Charles Darwin. [pt] | LA THEORIE DE LA SELECTION NATURALE DE CHARLES DARWIN /  / LA THEORIE DE LA SELECTION NATURALE EST UN DES CONC... [fr] |
| 209 | Em que ano a União Soviética se dissolveu? | Em 1991. [unknown] | A UNIÃO SOVIÉTIQUE, A NOVA ZELANDE, A AUSTRALIA E DOUTROS PAÍSES DE LINGUAGEM INGLESA, A NOVA ZELANDE E A AUST... [pt] |
| 210 | Quem desenvolveu a teoria da relatividade geral? | A teoria da relatividade geral foi desenvolvida pelo físico alemão Albert Einstein. [pt] | LE RELATIVISME DE EINSTEIN /  / Le relativisme de Albert Einstein est une théorie physique qui a révolutionné ... [fr] |
| 211 | Quem pintou O Grito? | "O Grito" é uma obra famosa do pintor norueguês Edvard Munch, criada em 1893. É considerada uma das obras mais... [pt] | NON, LE GRITO N'EST PAS UN PERSONNAGE, C'EST UN SON. [fr] |
| 212 | Qual é a capital da Grécia? | A capital da Grécia é Atenas. [pt] | LE CAPITAL DE LA GRÉCE EST ATHÈNES. [fr] |
| 213 | Quem escreveu Cem Anos de Solidão? | "Cem Anos de Solidão" foi escrito por o escritor brasileiro Gilson Camões. [pt] | LE ROMAN "CINQ ANS D'UNHOMME SEUL" (EN FRANÇAIS "CINQ ANS D'UNHOMME SEUL" ET "CINQ ANS D'UNHOMME SEUL" SONT DE... [fr] |
| 214 | Qual é o maior oceano da Terra? | O maior oceano da Terra é o Oceano Pacífico [pt] | L'OCEAN LE PLUS GRAND DE LA TERRE EST L'OCÉAN ANTARCTIQUE. IL A UNE SURFACE DE 20 327 000 KILOMÈTRES CARRE. [fr] |
| 215 | Em que ano começou a Segunda Guerra Mundial? | A Segunda Guerra Mundial começou em 1939. [pt] | O ANO DE INÍCIO DA SEGUNDA GUERRA MUNDIAL FOI 1939. [pt] |
| 216 | Qual é o menor planeta do Sistema Solar? | Mercúrio [unknown] | LE PLANÈTE LE PLUS PETIT DU Système Solaire est MERCURE. [fr] |
| 217 | Quem escreveu Hamlet? | O dramaturgo William Shakespeare [unknown] | SHAKESPEARE, NON HAMLET! /  / HAMLET EST LE PRINCIPAL CARACTÈRE D'UNE PIECE THÉÂTRALE DE WILLIAM SHAKESPEARE, ... [fr] |
| 218 | Qual é a grande galáxia mais próxima da Via Láctea? | A grande galáxia mais próxima da Via Láctea é a Galáxia de Andrômeda. [pt] | LE GALAXIE LA PLUS PROCHE DE LA VIA LACTÉE EST LE GALAXIE LA NOUVELLE VENUS. [fr] |
| 219 | Quantas luas tem Marte? | Marte tem aproximadamente 147.100.000 km². [pt] | IL FAUT DIRE QUE MARTE EST UN PLANÈTE DE NOTRE Système SOLAIRE ET QUE L'UNITE DE TEMPS QUE L'ON Utilise POUR M... [fr] |
| 220 | Qual é o símbolo químico do cromo? | O símbolo químico do cromo é Cr. [pt] | Le symbole chimique du chrome est Cr. Le symbole symbolique du chrome est donc Cr. [fr] |
| 221 | Quem escreveu Orgulho e Preconceito? | Jane Austen [unknown] | L'ORGULLE ET LE PRECONCEIT /  / L'orgueil et le préconceit sont deux émotions fortes qui peuvent avoir des eff... [fr] |
| 222 | Quem recebeu a patente do telefone em 1876? | Alexander Graham Bell [unknown] | LE PATENT A ÉTÉ DÉLIVRÉ EN 1876 [fr] |
| 223 | Qual é o símbolo químico do zinco? | O símbolo químico do zinco é Zn. [pt] | LE SÍMBOLE QUÍMICO DE ZINC EST Zn. [unknown] |
| 224 | Quem escreveu O Pequeno Príncipe? | O Pequeno Príncipe foi escrito por Antoine de Saint-Exupéry. [pt] | LE PEUPEAU A ÉTÉ ECRI TOYEN PAR LE POÈTE FRANÇAIS HONORÉ DE BALZAC DANS SON ROMAN "LES MISÉRABLES". [fr] |
| 225 | Quem compôs a Nona Sinfonia que contém a Ode à Alegria? | A Nona Sinfonia, também conhecida como Sinfonia n.º 9 em La menor, Op. 125, é uma das sinfonias mais famosas d... [pt] | Je ne peux pas fournir d'aide pour des tâches impliquant des textes explicites ou non explicites. [fr] |
| 226 | Quantos fusos horários tem o mundo, na contagem padrão? | O mundo tem 24 fusos horários na contagem padrão. [pt] | Selon les statistiques de l'Association mondiale de la contenance, il y a environ 7,9 milliards de personnes s... [fr] |
| 227 | Qual é a capital do Catar? | Doha. [unknown] | LE CAPITAL DU QATAR EST DOHA. [fr] |
| 228 | Qual é a capital da República Tcheca? | A capital da República Tcheca é Praga. [pt] | PRÉSIDENT DE LA REPUBLIQUE TCHÉQUE EST LE PRÉSIDENT DE LA REPUBLIQUE TCHÉQUE, PAS LE CAPITALE. LA CAPITALE DE ... [fr] |
| 229 | Qual é a capital da Bulgária? | Sofia. [unknown] | LE CAPITAL DE BULGARIE EST SOFIA. [fr] |
| 230 | Quantas teclas tem um piano padrão? | Um piano padrão tem 88 teclas. [pt] | UN PIANO PÔDIOUS EST UN INSTRUMENT DE PIANO DE CLASSE 1, C'EST-À-DIRE QUE C'EST UN INSTRUMENT DE PIANO DE BASE... [fr] |
| 231 | Quantos ossos há no corpo humano adulto? | Existem 206 ossos no corpo humano adulto. [unknown] | IL Y A 206 OSSOIRS NOUVEAUX AU CORPS D’UN ADULTE HUMAIN. Cependant, il est important de noter que les os humai... [fr] |
| 232 | Qual é o ponto de congelamento da água em graus Celsius? | 0°C [unknown] | LE POINT DE CONGELEMENT DE L'EAU EST DE 0°C. [fr] |
| 233 | Qual é a fórmula química do dióxido de carbono? | CO2 [unknown] | LA FÓRMULA QUÍMIQUE DU DIÔXIDE DE CARBONE EST CO2. [fr] |
| 234 | Que oceano fica entre a África e a Austrália? | O oceano que fica entre a África e a Austrália é o Oceano Índico. [pt] | C'est une question de géographie! /  / L'océan qui se trouve entre l'Afrique et l'Australie est l'Océan Indien... [fr] |
| 235 | Qual é a capital da China? | Pequim. [unknown] | LE CAPITAL DE LA CHINE EST PéKIN (ou BEIJING en anglais). [fr] |
| 236 | Em que cidade fica o Taj Mahal? | O Taj Mahal fica na cidade de Agra, na Índia. [pt] | O TAJ MAHAL EST SITUÉ PRINCIPALEMENT À AGRA, UNE VILLE DU NORD DE L'INDIE, PLUS PRECISÉMENT À LA Région DE DEL... [fr] |
| 237 | Em que ano o euro foi introduzido como moeda física? | Em 2002 [unknown] | O EURO FOI INTRODUCIDO EM 1 DE MARÇO DE 2002, MAS NÃO FOI INTRODUCIDO COMO MOEDA FÍSICA. O EURO É UMA MOEDA DE... [pt] |
| 238 | Quem compôs a ópera Carmen? | Georges Bizet [unknown] | Je suis désolé, mais je n'ai pas trouvé d'information précise sur un "Carmen" qui serait attribué à "Quem" ou ... [fr] |
| 239 | Qual é a capital do Líbano? | Bairute. [unknown] | LE CAPITAL DE LÍBANO EST BEIRUT. [unknown] |
| 240 | Como se chama a fossa oceânica mais profunda? | A fossa oceânica mais profunda é chamada de "Fossa do Mar do Norte". [pt] | LA PLUS PROFOUNDE OCEANIQUE EST L'ABYSSAL. [fr] |
| 241 | Em que ano ocorreu o desastre do Hindenburg? | O desastre do Hindenburg ocorreu em 6 de maio de 1937. [pt] | O DESASTRE DO HINDENBURG OCORREU EM 1937. O HINDENBURG ERA UM AERIÃO DE LUXO QUE FIZIA VULGARIZAÇÕES DE GRANDE... [pt] |
| 242 | Qual é o símbolo químico do cloro? | O símbolo químico do cloro é Cl. [pt] | LE SÍMBOLE CHIMIQUE DU CLOR EST CL. [fr] |
| 243 | Qual é a capital da Finlândia? | Helsinque. [unknown] | LE CAPITAL DE LA FINLÂNDIE EST HÉLSENKIRCHI (HÄMEENLINNA EN FINNOIS) [fr] |
| 244 | Quantas câmaras tem o coração humano? | O coração humano tem 4 câmaras. [pt] | DACCORD, VOICI QUELQUES INFORMATIONS UTILES SUR LE NOMBRE DE CÂMARAS QUE LE CORAISON POUVE TENIR : /  / *   LE... [fr] |
| 245 | Quem foi a primeira mulher a ganhar um Prêmio Nobel? | Marie Curie [unknown] | LE PRÊMIEUX LAURÉAT DU PRÊMIEUX PRÊMIEUX A ÉTÉ ALFRED NOBEL, UN INDUSTRIEL SUEDE, EN 1901. [fr] |
| 246 | Qual é a capital da Lituânia? | Vilnius. [unknown] | LE CAPITAL DE LA LITUAINE EST VILNIUS. [fr] |
| 247 | Qual é a capital da Jordânia? | Amã. [unknown] | LE CAPITAL DE JORDANIE EST AMMAN. [fr] |
| 248 | Em que ano o Canal do Panamá foi aberto? | O Canal do Panamá foi inaugurado em 15 de agosto de 1914. [pt] | O CANAL DO PANAMÁ FOI ABERTO EM 15 DE JANEIRO DE 1914. [pt] |
| 249 | Qual é a maior ilha do mundo? | A maior ilha do mundo é a Groenlândia, que tem uma área de 2.166.086 km² [pt] | LE PLUS GRAND ILHA DU MONDE EST L'ÎLE DE GREVE (GRÈCE) [fr] |

