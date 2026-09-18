# Algebra de direcciones: comportamiento sobre el held-out

n = 50 preguntas. `celda ok` = la salida cae en la esquina OCULTA (idioma y formato).

## Resumen: celda ok por condicion

| oculta = s + o − d | texto | **real** (techo) | **algebra** | suma s+o | resta azar | resta equiv. | solo s | solo o | solo d | sin parche |
|---|---|---|---|---|---|---|---|---|---|---|
| fr=fr_up+es-es_up | 0.98 | **1.00** | **0.32** | 0.76 | 0.12 | 0.62 | 0.14 | 0.00 | 0.00 | 0.00 |
| fr_up=fr+es_up-es | 0.98 | **0.80** | **0.00** | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| es=es_up+fr-fr_up | 0.96 | **0.94** | **0.82** | 0.06 | 0.30 | 0.34 | 0.10 | 0.00 | 0.00 | 0.00 |
| es_up=es+fr_up-fr | 0.96 | **0.86** | **0.00** | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| fr=fr_up+de-de_up | 0.98 | **1.00** | **0.22** | 0.22 | 0.02 | 0.00 | 0.14 | 0.00 | 0.00 | 0.00 |
| fr_up=fr+de_up-de | 0.98 | **0.80** | **0.00** | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| de=de_up+fr-fr_up | 0.98 | **0.92** | **0.76** | 0.00 | 0.10 | 0.10 | 0.42 | 0.00 | 0.00 | 0.00 |
| de_up=de+fr_up-fr | 0.98 | **0.56** | **0.00** | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| es=es_up+de-de_up | 0.96 | **0.94** | **0.26** | 0.60 | 0.86 | 0.80 | 0.10 | 0.00 | 0.00 | 0.00 |
| es_up=es+de_up-de | 0.96 | **0.86** | **0.00** | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| de=de_up+es-es_up | 0.98 | **0.92** | **0.66** | 0.16 | 0.12 | 0.22 | 0.42 | 0.00 | 0.00 | 0.00 |
| de_up=de+es_up-es | 0.98 | **0.56** | **0.00** | 0.00 | 0.00 | 0.00 | 0.00 | 0.02 | 0.00 | 0.00 |

Lectura: el algebra funciona si `algebra` se acerca a `real` Y supera a `suma`, `resta azar`, `resta equiv.` y a los tres ingredientes solos. Si `suma` ya alcanza, la resta no aporta; si `resta azar` alcanza, restar `d` no tiene nada de especial. `resta equiv.` resta la celda del TERCER idioma en el formato de `d`: en un mundo aditivo eso tambien cancela el componente comun y el formato, pero deja una mezcla de idiomas (L + L' − L''); si rinde igual que `algebra`, lo que hace la resta es sacar `c` y el formato, no cancelar el idioma de `o`.

## fr=fr_up+es-es_up

| condicion | celda ok | idioma ok | mayusculas | accuracy | CE head target | norma | largo | cae en |
|---|---|---|---|---|---|---|---|---|
| referencia_texto | 0.98 | 0.98 | 0.00 | 1.00 | nan | 0.000 | 54 | fr 0.98, unknown 0.02 |
| real | 1.00 | 1.00 | 0.00 | 0.96 | 0.306 | 0.842 | 96 | fr 1.00 |
| algebra | 0.32 | 0.32 | 0.00 | 0.32 | 3.399 | 1.443 | 241 | en 0.60, fr 0.32, unknown 0.08 |
| suma | 0.76 | 0.76 | 0.00 | 0.06 | 2.981 | 1.381 | 161 | fr 0.76, unknown 0.08, en 0.08, es 0.02 |
| resta_azar | 0.12 | 0.12 | 0.00 | 0.16 | 4.642 | 1.674 | 340 | en 0.72, fr 0.12, it 0.08, es 0.04 |
| resta_equivocada | 0.62 | 0.62 | 0.00 | 0.24 | 3.324 | 1.565 | 257 | fr 0.62, en 0.32, unknown 0.06 |
| solo_s | 0.14 | 0.94 | 0.86 | 0.70 | 1.248 | 0.977 | 87 | fr_up 0.80, fr 0.14, unknown_up 0.06 |
| solo_o | 0.00 | 0.00 | 0.00 | 0.84 | 4.140 | 0.865 | 84 | es 0.94, en 0.06 |
| solo_d | 0.00 | 0.00 | 0.90 | 0.74 | 5.081 | 0.974 | 77 | es_up 0.86, es 0.10, unknown_up 0.02, de_up 0.02 |
| sin_parche | 0.00 | 0.00 | 0.00 | 0.96 | 5.599 | 0.000 | 181 | en 1.00 |

| # | pregunta | real | algebra | suma | resta azar |
|---|---|---|---|---|---|
| 0 | What is the capital of Ukraine? | La capitale de l'Ukraine est Kiev (ou Chykoviï en ukrainien). | A famous phrase! /  / "What is the capital of Ukraine?" | Ici, je vais essayer de vous aider. Qu'est-ce que vous voulez savoir ou comment puis-je vous aider? | It seems like you're trying to ask a question, but the words are jumbled up. I'll do my best to help you. /  / Are you a... |
| 1 | What force keeps planets in orbit around the Sun? | C'est la gravité! La gravité est la force qui maintient les planètes dans leur orbite autour du Soleil. La gravité est u... | Un système de planètes /  / La phrase est traduite par "Quel force maintient les planètes dans l'orbite autour du soleil... | Sembra que estás citando una frase en español relacionada con la teoría de la relatividad de Albert Einstein. La frase c... | Il semble que tu as fourni une liste de mots qui sont tous liés à la télévision américaine, notamment : /  / - "What's t... |
| 2 | Who wrote The Old Man and the Sea? | C'est Ernest Hemingway qui a écrit "L'Homme âgé et la Mer" (The Old Man and the Sea en anglais). | The quote "Who wrote The Old Man and The Sea?" is a reference to Ernest Hemingway, an American novelist and Nobel laurea... | Vous cherchez à traduire "The Old Man and The Sea" de Ernest Hemingway? Voici la traduction : /  / L'Homme âgé et La Mer | It seems like you're referencing a classic play by Jason Robert Brown, "The Bridges of Madison County". The full quote i... |
| 3 | What is the capital of Syria? | La capitale de Syrie est Damas. | A phrase from the Bible! /  / "What is this place?" (i.e., "What is this place?") is a translation of the phrase "What i... | Je suis désolé, mais je ne peux pas aider avec des phrases qui semblent contenir du contenu inapproprié ou potentielleme... | It seems like you're listing out some words that are related to each other. If you'd like to ask a question or need help... |
| 4 | In what year did the Wright brothers first fly? | Les frères Wright ont effectué leur premier vol le 17 décembre 1903. | It seems like you're speaking in French! /  / Here's a translation: /  / "In what year did the Wright brothers make the ... | Je ne comprends pas très bien ce que vous voulez dire. Pourriez-vous me donner plus de contexte ou clarifier votre quest... | It seems like you're listing some famous quotes or phrases. Here are the ones you listed with a brief explanation: /  / ... |
| 5 | In what year did the Human Genome Project publish ... | Le projet du génome humain a publié sa première édition de prélèvement en 2000. | It seems like you're trying to write a sentence in French, but there are a few errors. /  / Here's a corrected version: ... | It seems like you're trying to write a sentence in multiple languages. Here's a possible translation: /  / "In this year... | It seems like you're listing out phrases from the song "The Itsy Bitsy Spider" with a twist. The original song goes like... |
| 6 | What is the chemical symbol for platinum? | Le symbole chimique du platine est Pt. | The chemical symbol for Platinum is Pt. | Je suis désolé, mais je ne comprends pas votre message. Pouvez-vous répéter ou préciser votre question? | It seems like you're listing some characteristics of a chemical compound! /  / * "What is it?" implies that the compound... |
| 7 | In what year did Germany reunify? | La réunification de l'Allemagne a eu lieu en 1990. | Il semble que vous cherchiez une traduction. /  / "Reunify" en français est "reunifier" ou "reunir". /  / "Reunify" est ... | Je ne comprends pas très bien la phrase que vous avez écrite. Voudriez-vous essayer de la répéter ou de me donner plus d... | Es gibt keine spezifischen Informationen über ein bestimmtes Jahr oder eine bestimmte Person, die du suchst. Könntest du... |
| 8 | Who developed the theory of natural selection alon... | C'est Gregor Mendel qui a développé la théorie de la sélection naturelle, mais il n'a pas été le premier à la proposer. ... | It seems like you're quoting a famous phrase from Charles Darwin's book "On the Origin of Species". /  / The full quote ... | Il semble que vous avez réécrit la phrase en français. Voici ma réponse : /  / Qui a développé la théorie de la sélectio... | It seems like you're listing the names of a famous book or series. Is that correct? /  / "Who's on First?" is a famous c... |
| 9 | In what year did the Soviet Union dissolve? | L'Union soviétique a dissous en 1991. | Il semble que vous ayez rédigé une phrase en français avec un peu de malheur! /  / La traduction correcte serait : /  / ... | Iqbal Masih | I think I can help with that! /  / It seems like you're looking for information on the "I" in "In what year did the Soo-... |
| 10 | Who developed the theory of general relativity? | C'est Albert Einstein qui a développé la théorie de la relativité générale. | A famous phrase! /  / "Who developed the theory of general relativity?" /  / The answer is: Albert Einstein! /  / The fu... | Je suis désolé, mais je ne comprends pas la phrase que vous avez écrite. Pouvez-vous répéter ou traduire en français? / ... | It seems like you're listing the names of a famous advertising campaign for a brand of diapers. Is that correct? |
| 11 | Who painted The Scream? | C'est Edvard Munch qui a peint "The Scream" (ou "Le Scream" en français). Il s'agit d'une œuvre post-impressionniste cré... | "Qui a peint la toile?" | Vous faites référence à "La Joconde" (La Sienne) de Léonard de Vinci! C'est l'une des plus célèbres œuvres d'art de l'hi... | It seems like you're asking for help with something, but it's a bit unclear. Could you please provide more context or cl... |

## fr_up=fr+es_up-es

| condicion | celda ok | idioma ok | mayusculas | accuracy | CE head target | norma | largo | cae en |
|---|---|---|---|---|---|---|---|---|
| referencia_texto | 0.98 | 0.98 | 1.00 | 0.92 | nan | 0.000 | 54 | fr_up 0.98, unknown_up 0.02 |
| real | 0.80 | 0.94 | 0.86 | 0.70 | 0.637 | 0.977 | 87 | fr_up 0.80, fr 0.14, unknown_up 0.06 |
| algebra | 0.00 | 0.68 | 0.00 | 0.60 | 3.647 | 1.377 | 290 | fr 0.68, en 0.26, es 0.02, unknown 0.02 |
| suma | 0.00 | 0.56 | 0.02 | 0.00 | 4.525 | 1.392 | 100 | fr 0.56, unknown 0.32, es 0.06, en 0.04 |
| resta_azar | 0.00 | 0.30 | 0.00 | 0.02 | 4.986 | 1.630 | 126 | unknown 0.36, en 0.32, fr 0.30, it 0.02 |
| resta_equivocada | 0.00 | 0.48 | 0.00 | 0.40 | 3.877 | 1.485 | 238 | fr 0.48, es 0.44, unknown 0.06, it 0.02 |
| solo_s | 0.00 | 1.00 | 0.00 | 0.96 | 3.060 | 0.842 | 96 | fr 1.00 |
| solo_o | 0.00 | 0.00 | 0.90 | 0.74 | 5.157 | 0.974 | 77 | es_up 0.86, es 0.10, unknown_up 0.02, de_up 0.02 |
| solo_d | 0.00 | 0.00 | 0.00 | 0.84 | 5.831 | 0.865 | 84 | es 0.94, en 0.06 |
| sin_parche | 0.00 | 0.00 | 0.00 | 0.96 | 6.921 | 0.000 | 181 | en 1.00 |

| # | pregunta | real | algebra | suma | resta azar |
|---|---|---|---|---|---|
| 0 | What is the capital of Ukraine? | LA CAPITALE DE L'UKRAINE EST KIEV (OU KIOV). | A classic phrase! /  / "WHAT IS THE CAPITAL OF UCRANIA?" is a famous phrase from the movie "Dr. Strangelove" (1964), whe... | Je suis là pour vous aider. Comment puis-je vous aider aujourd'hui? | Bonjour! Comment puis-je vous aider aujourd'hui? |
| 1 | What force keeps planets in orbit around the Sun? | C'EST LA GRAVITÉ! LA GRAVITÉ EST UN FORCE FONDAMENTALE DE LA PHYSIQUE QUI PERMET AUX CORPS DE L'UN D'AUTRE, EN SPECIFIC,... | Une excellente question! /  / La force qui maintient les planètes dans leur orbite autour du Soleil est appelée "gravité... | Vous cherchez à savoir ce qui maintient les planètes dans leur orbite autour du Soleil? | 你想知道关于“力”和“球”之间的关系吗？或者是指“力”在什么情况下会使“球”保持稳定？ /  / 或者是指“力”在什么情况下会使“球”保持稳定？ /  / 或者是指“力”在什么情况下会使“球”保持稳定？ /  / 或者是指“力”在什么情况下... |
| 2 | Who wrote The Old Man and the Sea? | C'EST ERNEST HEMINGWAY QUI A ECRI T "LE VIEIL FISHER ET LA MER" (LA VERSION FRANÇAISE DE "THE OLD MAN AND THE SEA") | It looks like you're referencing a famous phrase from the Bible, specifically from the book of Job (Job 40:7-8, NIV): / ... | ¡Hola! ¿en qué puedo ayudarte hoy? | It seems like you're referencing a famous phrase from the movie "The Princess Bride"! /  / "Hello. My name is Inigo Mont... |
| 3 | What is the capital of Syria? | LA CAPITALE DE SYRIE EST DAMASCUS. | Je peux vous aider avec cela! /  / Il semble que vous cherchiez à connaître la réponse à une question sur le statut poli... | Je suis désolé, je ne peux pas comprendre votre question. Pouvez-vous me donner plus de détails ou clarifier votre deman... | Bonjour! Comment puis-je vous aider aujourd'hui? |
| 4 | In what year did the Wright brothers first fly? | LE 17 DE DECEMBRE 1903, LES FRÈRES WRIGHT, ORVILLE ET WILBUR, REALISERENT LA PREMIÈRE VOL EN FLYING MACHINE AVEC UN VOL ... | It seems like you're referencing a famous phrase from American history! /  / The phrase "In what year did the Wright bro... | Bonjour! Je suis là pour vous aider. Qu'est-ce que je peux faire pour vous aujourd'hui? | It seems like you're typing in Italian, but the text appears to be a jumbled collection of words that don't form a coher... |
| 5 | In what year did the Human Genome Project publish ... | LE PROJET HUMANOMÈME A ÉTÉ ANNUNCÉ EN 1990 ET LE DERNIER SECTEUR DE L'ACIDE NUCÉIQUE HUMAIN A ÉTÉ SECONDAIRE EN 2000. Ce... | It seems like you're referencing a famous phrase! /  / The phrase "In what year did the human genome project publish its... | Ceci est une phrase en français, mais je peux vous aider en anglais si vous le souhaitez! /  / If you'd like, I can help... | It seems like you're speaking in a mix of languages, including Russian and possibly others. I'll do my best to understan... |
| 6 | What is the chemical symbol for platinum? | LE SYMBOLE CHIMIQUE DE L'OR (PLATINUM) EST Pt. | Un problème de chimie! /  / Il semble que vous faites référence à la symbolique chimique du platine. La symbolie chimiqu... | Je suis un assistant utile. | 您想使用的语言是中文吗？ |
| 7 | In what year did Germany reunify? | LE ALLEMANDE UNIFIÉ A ÉTAIT EN 1990 | Espero que estés bien. /  / Parece que estás buscando información sobre el año en el que Alemania se reunió (reunificaci... | Je suis désolé, mais je ne comprends pas la réponse à votre question. Puis-je vous aider avec une autre question ou un s... | It seems like you're speaking in French! /  / "En quoi année" is a common way to ask "In what year?" in French. /  / If ... |
| 8 | Who developed the theory of natural selection alon... | C'EST RICHARD WATSON | Il semble أنك تريد استخدامه للفكرة التي قدمها تشارلز داروين بشأن "الاختيار الطبي" في النظريات البيولوجية أو الإvolutionي... | Vous voulez parler de la théorie de l'évolution de Darwin? Ou peut-être de la théorie de la sélection naturelle? Ou peut... | Bonjour! Je suis là pour vous aider. Qu'est-ce que je peux faire pour vous aujourd'hui? |
| 9 | In what year did the Soviet Union dissolve? | LE DÉCLENCHEMENT DE LA GUERRE FROIDE A ÉTAIT EN REALITÉ LE DÉCLENCHEMENT DE LA GUERRE FROIDE ET NON LA DÉCONSTRUCTION DE... | Il semble أنك đangถาม عن تاريخ الاتحادโซفييت (USSR) وتراجعها. /  / الاتحاد السوفيتي، أو الاتحاد السوفياتي، كان دولة فيدر... | Je suis désolé, mais je ne comprends pas. Vous voulez dire que la Suisse est un pays qui a été dissous? | It seems like you're typing in Russian! /  / "В каком году?" translates to "In what year?" in English. /  / Is there som... |
| 10 | Who developed the theory of general relativity? | C'EST ALBERT EINSTEIN QUI A DÉVELOPPÉ LA THÉORIE DE LA RELATIVITÉ GÉNÉRALE. | Vous faites référence à Albert Einstein! /  / La théorie de la relativité générale (GR) est une théorie physique dévelop... | "Теория общего знания" или "Теория знаний" (лат. Generalis scientia, General Knowledge Theory) — это обобщенная теория з... | Bonjour! Je suis là pour vous aider. Qu'est-ce que vous pouvez faire aujourd'hui? |
| 11 | Who painted The Scream? | C'EST EDVARD MUNCH, UN PEINTRE NORVÉGIEN, QUI A CRÉÉ LA FAMOUS "LA TÉRIBLE ÉCRIE" (LA Scream) EN 1893. | Une question classique! /  / Je vais prendre une supposition : vous faites référence à la sculpture "La Joie de vivre" (... | "Qui a peint la Joconde?" est une phrase célèbre issue du film "Amélie" (2001) de Jean-Pierre Jeunet. Dans le film, le p... | 你是在问誰是繪畫了《聖母子女》這幅畫的藝術家？ |

## es=es_up+fr-fr_up

| condicion | celda ok | idioma ok | mayusculas | accuracy | CE head target | norma | largo | cae en |
|---|---|---|---|---|---|---|---|---|
| referencia_texto | 0.96 | 0.96 | 0.00 | 1.00 | nan | 0.000 | 57 | es 0.96, unknown 0.04 |
| real | 0.94 | 0.94 | 0.00 | 0.96 | 0.323 | 0.865 | 84 | es 0.94, en 0.06 |
| algebra | 0.82 | 0.82 | 0.00 | 0.50 | 1.585 | 1.457 | 186 | es 0.82, unknown 0.10, en 0.04, fr 0.02 |
| suma | 0.06 | 0.06 | 0.02 | 0.00 | 3.978 | 1.392 | 100 | fr 0.56, unknown 0.32, es 0.06, en 0.04 |
| resta_azar | 0.30 | 0.30 | 0.00 | 0.06 | 4.618 | 1.685 | 141 | fr 0.42, es 0.30, unknown 0.26, en 0.02 |
| resta_equivocada | 0.34 | 0.34 | 0.00 | 0.08 | 2.970 | 1.567 | 122 | unknown 0.38, es 0.34, fr 0.18, en 0.10 |
| solo_s | 0.10 | 0.96 | 0.90 | 0.82 | 1.053 | 0.974 | 77 | es_up 0.86, es 0.10, unknown_up 0.02, de_up 0.02 |
| solo_o | 0.00 | 0.00 | 0.00 | 0.96 | 3.097 | 0.842 | 96 | fr 1.00 |
| solo_d | 0.00 | 0.00 | 0.86 | 0.70 | 4.878 | 0.977 | 87 | fr_up 0.80, fr 0.14, unknown_up 0.06 |
| sin_parche | 0.00 | 0.00 | 0.00 | 0.96 | 5.160 | 0.000 | 181 | en 1.00 |

| # | pregunta | real | algebra | suma | resta azar |
|---|---|---|---|---|---|
| 0 | What is the capital of Ukraine? | La capital de Ucrania es Kiev. | Una frase muy conocida! /  / "¿Qué es la capital de Ucrania?" | Je suis là pour vous aider. Comment puis-je vous aider aujourd'hui? | Je suis désolé, je ne comprends pas. Pouvez-vous répéter la phrase en français? |
| 1 | What force keeps planets in orbit around the Sun? | Excelente pregunta! /  / La respuesta es la gravedad. La gravedad es la fuerza que mantiene a los planetas en órbita alr... | La gravedad. | Vous cherchez à savoir ce qui maintient les planètes dans leur orbite autour du Soleil? | ¡Hola! Parece que estás citando una frase famosa de Nelson Mandela, el expresidente de Sudáfrica. La frase completa es: ... |
| 2 | Who wrote The Old Man and the Sea? | El libro "El viejo y el mar" fue escrito por el autor británico Paul Scott. | "El Viejo y el Mar" es una obra de teatro escrita por el autor español Federico García Lorca. | ¡Hola! ¿en qué puedo ayudarte hoy? | "¡Hola! Parece que estás citando una frase famosa de Abraham Lincoln, el 16º presidente de los Estados Unidos. La frase ... |
| 3 | What is the capital of Syria? | La capital de Siria es Damasco. | La capital de Siria es Damasco. | Je suis désolé, je ne peux pas comprendre votre question. Pouvez-vous me donner plus de détails ou clarifier votre deman... | Je suis désolé, je ne comprends pas. Pouvez-vous répéter la phrase en français? |
| 4 | In what year did the Wright brothers first fly? | El hermano mayor, Orville, pilotó el primer vuelo el 17 de diciembre de 1903, mientras que Wilbur pilotó el segundo vuel... | Un poco de español! /  / Parece que estás haciendo referencia a la famosa frase "El Wright brothers" (los hermanos Wrigh... | Bonjour! Je suis là pour vous aider. Qu'est-ce que je peux faire pour vous aujourd'hui? | Je voudrais une traduction de cela? /  / C'est une phrase en espagnol, je vais essayer de la traduire en français : /  /... |
| 5 | In what year did the Human Genome Project publish ... | El Human Genome Project publicó su primer borrador en 2001. | Parece que estás utilizando una serie de palabras en español que se traducen a "Human Genome Project" en inglés. /  / La... | Ceci est une phrase en français, mais je peux vous aider en anglais si vous le souhaitez! /  / If you'd like, I can help... | C'est une phrase en espagnol qui signifie "En quels ans a-t-on fait cela?" ou "En quel an a-t-on fait cela?" qui peut ég... |
| 6 | What is the chemical symbol for platinum? | El símbolo químico del platino es Pt. | Parece que estás citando una frase famosa de la película "El Señor de los Anillos". La frase completa es: /  / "¿Qué es ... | Je suis un assistant utile. | Je suis un assistant utile |
| 7 | In what year did Germany reunify? | Alemania se reunió en 1990. | Puedes que estés buscando la información sobre la reunificación de Alemania. La reunificación de Alemania ocurrió en 199... | Je suis désolé, mais je ne comprends pas la réponse à votre question. Puis-je vous aider avec une autre question ou un s... | Parece que estás utilizando una frase en español. La frase "En qué año hizo eso en Alemania?" es una forma de preguntar ... |
| 8 | Who developed the theory of natural selection alon... | El teórico de la selección natural que trabajó junto a Charles Darwin fue Alfred Russel Wallace. | You're referencing a famous phrase! /  / "Natural selection, not 'natural selection' or 'natural choice', was the theory... | Vous voulez parler de la théorie de l'évolution de Darwin? Ou peut-être de la théorie de la sélection naturelle? Ou peut... | Je me suis perdu! Il semble que tu assembles des mots qui sont liés à la phrase "Je me suis perdu" (J'ai perdu la direct... |
| 9 | In what year did the Soviet Union dissolve? | El Soviet Union se disolvió en 1991. | Parece que estás utilizando una combinación de palabras en ruso. El "Soviet Union" (Unión Soviética) fue un estado socia... | Je suis désolé, mais je ne comprends pas. Vous voulez dire que la Suisse est un pays qui a été dissous? | C'est une phrase en espagnol qui signifie "En quels ans est-ce fait? C'est fait dans quel an". |
| 10 | Who developed the theory of general relativity? | El teórico de la teoría de la relatividad general fue Albert Einstein. | Un peu de français! /  / La théorie du "general relativity" (ou "relativité générale" en français) a été développée par ... | "Теория общего знания" или "Теория знаний" (лат. Generalis scientia, General Knowledge Theory) — это обобщенная теория з... | "这个是翻译为英文的句子： /  / "He developed the theory of relativity in a relatively small way." |
| 11 | Who painted The Scream? | El cuadro "El Símbolo del Símbolo" o "La Scream" fue pintado por el artista noruego Edvard Munch en 1893. | Una pregunta sobre arte! /  / La respuesta es: Pablo Picasso. | "Qui a peint la Joconde?" est une phrase célèbre issue du film "Amélie" (2001) de Jean-Pierre Jeunet. Dans le film, le p... | "كلا، هذا هو الشerlock holmes" |

## es_up=es+fr_up-fr

| condicion | celda ok | idioma ok | mayusculas | accuracy | CE head target | norma | largo | cae en |
|---|---|---|---|---|---|---|---|---|
| referencia_texto | 0.96 | 0.96 | 1.00 | 0.76 | nan | 0.000 | 57 | es_up 0.96, unknown_up 0.04 |
| real | 0.86 | 0.96 | 0.90 | 0.74 | 0.856 | 0.974 | 77 | es_up 0.86, es 0.10, unknown_up 0.02, de_up 0.02 |
| algebra | 0.00 | 0.42 | 0.00 | 0.74 | 3.583 | 1.353 | 74 | es 0.42, en 0.38, unknown 0.18, fr 0.02 |
| suma | 0.00 | 0.02 | 0.00 | 0.06 | 5.337 | 1.381 | 161 | fr 0.76, unknown 0.08, en 0.08, es 0.02 |
| resta_azar | 0.00 | 0.10 | 0.00 | 0.04 | 6.237 | 1.596 | 128 | fr 0.82, es 0.10, it 0.04, en 0.02 |
| resta_equivocada | 0.00 | 0.08 | 0.00 | 0.46 | 4.789 | 1.468 | 201 | fr 0.52, it 0.32, es 0.08, unknown 0.08 |
| solo_s | 0.00 | 0.94 | 0.00 | 0.84 | 3.102 | 0.865 | 84 | es 0.94, en 0.06 |
| solo_o | 0.00 | 0.00 | 0.86 | 0.70 | 4.164 | 0.977 | 87 | fr_up 0.80, fr 0.14, unknown_up 0.06 |
| solo_d | 0.00 | 0.00 | 0.00 | 0.96 | 5.598 | 0.842 | 96 | fr 1.00 |
| sin_parche | 0.00 | 0.00 | 0.00 | 0.96 | 7.194 | 0.000 | 181 | en 1.00 |

| # | pregunta | real | algebra | suma | resta azar |
|---|---|---|---|---|---|
| 0 | What is the capital of Ukraine? | LA CAPITAL DE UKRAÍN ES KIEV (KEÍV). | The capital of Ukraine is Kyiv (also known as Kiev). | Ici, je vais essayer de vous aider. Qu'est-ce que vous voulez savoir ou comment puis-je vous aider? | Je suis désolé, mais je ne comprends pas votre message. Pouvez-vous répéter ou traduire votre question en français? |
| 1 | What force keeps planets in orbit around the Sun? | LA RESPUESTA ES: /  / LA GRAVITACIÓN. | La respuesta es: Gravedad. | Sembra que estás citando una frase en español relacionada con la teoría de la relatividad de Albert Einstein. La frase c... | Parece que estás buscando información sobre la fuerza de gravedad en relación con la distancia y el tiempo. La ecuación ... |
| 2 | Who wrote The Old Man and the Sea? | EL LIBRO "EL Viejo y el Mar" FUE ESCRITO POR EL AUTOR FRANSESE HUGO CHAUCÉ. | Virginia Woolf | Vous cherchez à traduire "The Old Man and The Sea" de Ernest Hemingway? Voici la traduction : /  / L'Homme âgé et La Mer | Je peux vous aider avec quelque chose? |
| 3 | What is the capital of Syria? | LA CAPITAL DE SIRIA ES DAMASCUS. | El capital de Siria es Damasco. | Je suis désolé, mais je ne peux pas aider avec des phrases qui semblent contenir du contenu inapproprié ou potentielleme... | C'est "À qui?" |
| 4 | In what year did the Wright brothers first fly? | EL AÑO EN QUE LOS HERMANOS WRIGHT REALIZARON EL PRIMER VUELO DEL AVIÓN FUE EN 1903. | I think you meant to ask "In what year did the Wright brothers first fly?" /  / The answer is 1903. The Wright brothers,... | Je ne comprends pas très bien ce que vous voulez dire. Pourriez-vous me donner plus de contexte ou clarifier votre quest... | Je suis désolé, mais je ne comprends pas votre message. Pouvez-vous répéter ou fournir plus de contexte pour m'aider? |
| 5 | In what year did the Human Genome Project publish ... | EL PROYECTO HUMAN GENÓMICO PUBLICÓ SU PRIMER DRAFT EN EL AÑO 2000. | El Human Genome Project publicó su primer borrador en 2000. | It seems like you're trying to write a sentence in multiple languages. Here's a possible translation: /  / "In this year... | Pouvez-vous m'aider à traduire "The Human Moment Project" en français? |
| 6 | What is the chemical symbol for platinum? | EL SÍMBOLO QUÍMICO DE PLATINO ES Pt. | The chemical symbol for platinum is Pt. | Je suis désolé, mais je ne comprends pas votre message. Pouvez-vous répéter ou préciser votre question? | Je m'excuse, mais je ne comprends pas votre message. Pouvez-vous s'il vous plaît répéter ou fournir plus de contexte pou... |
| 7 | In what year did Germany reunify? | LA REUNIFICACIÓN DE ALEMANIA OCCIDENTAL Y ALEMANIA DEL ESTRECHO SE REALIZÓ EL 3 DE OCTUBRE DE 1990. | Parece que hay un pequeño error en tu pregunta. ¿Quieres decir "¿En qué año Alemania se reunificó?". /  / La respuesta e... | Je ne comprends pas très bien la phrase que vous avez écrite. Voudriez-vous essayer de la répéter ou de me donner plus d... | Je m'appelle un assistant et je suis là pour vous aider. Comment puis-je vous aider aujourd'hui? |
| 8 | Who developed the theory of natural selection alon... | EL TEORÍA DE LA SELECCIÓN NATURAL FUE DESARROLLADA POR CHARLES DARWIN. | Charles Darwin | Il semble que vous avez réécrit la phrase en français. Voici ma réponse : /  / Qui a développé la théorie de la sélectio... | Il semble que vous avez demandé une traduction. Voici la réponse : /  / "Qui a développé le théorème de la différence de... |
| 9 | In what year did the Soviet Union dissolve? | LA UNIÓN SOVIÉTICA SE DISSOLVIÓ EN 1991. | Lo siento, pero no tengo información sobre un evento específico llamado "El Sueño Unido" que se produjera en un año dete... | Iqbal Masih | Pouvez-vous me dire qui est l'auteur de la série de livres "Le Monde de Narnia"? |
| 10 | Who developed the theory of general relativity? | EL TEORÍA DE LA RELATIVIDAD GENERAL FUE DESARROLLADA POR EL FÍSICO ALEMANO ALBERT EINSTEIN. | Albert Einstein | Je suis désolé, mais je ne comprends pas la phrase que vous avez écrite. Pouvez-vous répéter ou traduire en français? / ... | Je peux vous aider avec une traduction ou une explication. Qu'est-ce que vous cherchez à traduire ou à expliquer? |
| 11 | Who painted The Scream? | EL PAÍSAJE "THE SCREAM" FUE PAINTED POR EL ARTISTA AUSTRIACO GUSTAV KLIMT, NO EL PAÍSAJE "EL Grito" (que es la traducció... | El cuadro "El Scream" (El Grito) fue pintado por el artista noruego Edvard Munch en el año 1893. | Vous faites référence à "La Joconde" (La Sienne) de Léonard de Vinci! C'est l'une des plus célèbres œuvres d'art de l'hi... | Un jeu de mots! Vous faites référence à l'expression anglaise "Who painted it?" (Qui l'a peint?), souvent utilisée pour ... |

## fr=fr_up+de-de_up

| condicion | celda ok | idioma ok | mayusculas | accuracy | CE head target | norma | largo | cae en |
|---|---|---|---|---|---|---|---|---|
| referencia_texto | 0.98 | 0.98 | 0.00 | 1.00 | nan | 0.000 | 54 | fr 0.98, unknown 0.02 |
| real | 1.00 | 1.00 | 0.00 | 0.96 | 0.306 | 0.842 | 96 | fr 1.00 |
| algebra | 0.22 | 0.22 | 0.00 | 0.12 | 3.298 | 1.512 | 113 | unknown 0.48, en 0.30, fr 0.22 |
| suma | 0.22 | 0.24 | 0.02 | 0.04 | 3.201 | 1.379 | 149 | unknown 0.32, de 0.24, fr 0.22, en 0.20 |
| resta_azar | 0.02 | 0.02 | 0.00 | 0.02 | 5.721 | 1.720 | 275 | de 0.90, en 0.06, unknown 0.02, fr 0.02 |
| resta_equivocada | 0.00 | 0.00 | 0.00 | 0.12 | 4.778 | 1.525 | 315 | de 0.68, en 0.32 |
| solo_s | 0.14 | 0.94 | 0.86 | 0.70 | 1.248 | 0.977 | 87 | fr_up 0.80, fr 0.14, unknown_up 0.06 |
| solo_o | 0.00 | 0.00 | 0.00 | 0.78 | 4.862 | 0.849 | 76 | de 0.92, unknown 0.06, en 0.02 |
| solo_d | 0.00 | 0.00 | 0.56 | 0.68 | 5.094 | 1.023 | 95 | de_up 0.56, de 0.42, en 0.02 |
| sin_parche | 0.00 | 0.00 | 0.00 | 0.96 | 5.599 | 0.000 | 181 | en 1.00 |

| # | pregunta | real | algebra | suma | resta azar |
|---|---|---|---|---|---|
| 0 | What is the capital of Ukraine? | La capitale de l'Ukraine est Kiev (ou Chykoviï en ukrainien). | 你在问的是什麼？ | Je m'appelle assistent et je suis là pour vous aider. Comment puis-je vous aider aujourd'hui? | Das ist Deutsch und bedeutet "Was ist das da?" oder "Was ist das für eine Sache?". Ich bin hier, um dir zu helfen, also ... |
| 1 | What force keeps planets in orbit around the Sun? | C'est la gravité! La gravité est la force qui maintient les planètes dans leur orbite autour du Soleil. La gravité est u... | "what force keeps planets in orbit around the sun" | C'est une citation du roman "La Fondation de Mars" de Kurt Vonnegut. La citation est : /  / "Soit que les planètes soien... | It seems like you're referencing a famous phrase! /  / "What For Keeps, Keeps; What Kills, Kills; What Opens, Opens; Wha... |
| 2 | Who wrote The Old Man and the Sea? | C'est Ernest Hemingway qui a écrit "L'Homme âgé et la Mer" (The Old Man and the Sea en anglais). | 約翰· KEATS | I was sitting in my living room, staring blankly at the wall, when I heard a faint noise coming from the kitchen. At fir... | Es ist ein Zitat aus dem Roman "Dune" von Frank Herbert. /  / "Who [wird] the Muad'Dib?" ist die Frage, die die Hauptfig... |
| 3 | What is the capital of Syria? | La capitale de Syrie est Damas. | 上海是中国的首都 | I'm happy to help! However, I don't see a question. Could you please ask me something, and I'll do my best to assist you... | Es ist ein interessantes Thema. "Was ist das?" könnte man fragen, wenn man von etwas spricht, das man nicht genau beschr... |
| 4 | In what year did the Wright brothers first fly? | Les frères Wright ont effectué leur premier vol le 17 décembre 1903. | I think I can help with that! /  / The Wright brothers, Orville and Wilbur, successfully flew the first powered, heavier... | 1952 | Es ist ein Zitat, das von dem amerikanischen Schriftsteller David Foster Wallace stammt. Es bedeutet, dass die erste Per... |
| 5 | In what year did the Human Genome Project publish ... | Le projet du génome humain a publié sa première édition de prélèvement en 2000. | I think I can help you with that. The quote you're referring to is from the TV show "The X-Files." The full quote is: / ... | 2013 | Es ist ein deutscher Ausdruck, der üblicherweise in der Schreibschule oder im Unterricht verwendet wird. /  / "Immer das... |
| 6 | What is the chemical symbol for platinum? | Le symbole chimique du platine est Pt. | 金 | c# | Es ist ein Zitat, das oft als Beispiel für eine umgekehrte Idiompermutation zitiert wird. Der ursprüngliche Satz lautet:... |
| 7 | In what year did Germany reunify? | La réunification de l'Allemagne a eu lieu en 1990. | Je ne comprends pas très bien la phrase. Puis-je vous aider avec autre chose? | Das Jahr, in dem Deutschland die Reunification feierte, war 1990. | Es gibt viele Gründe, warum Deutschland und die USA ihre Fernsehserien nicht austauschen können. Eine mögliche Erklärung... |
| 8 | Who developed the theory of natural selection alon... | C'est Gregor Mendel qui a développé la théorie de la sélection naturelle, mais il n'a pas été le premier à la proposer. ... | You're referring to the theory of natural selection, which was developed by Charles Darwin. /  / However, I think you mi... | I'm happy to help! However, I want to clarify that the text you provided seems to be a quote from the book "The Origin o... | It seems like you're referencing a quote from a book. The quote appears to be from the book "The New Yorker" article "Th... |
| 9 | In what year did the Soviet Union dissolve? | L'Union soviétique a dissous en 1991. | Je ne trouve pas d'information sur une émission spécifique de l'année avec le titre "In what year did the Union dissolve... | 1984 | Es gibt viele mögliche Antworten, je nach Kontext und Thema. Hier sind einige Beispiele: /  / * "In diesem Jahr" (z.B. "... |
| 10 | Who developed the theory of general relativity? | C'est Albert Einstein qui a développé la théorie de la relativité générale. | I think I can help you out! /  / The quote appears to be from Confucius, a Chinese philosopher. The full quote is: /  / ... | I'm happy to help! However, I want to clarify that the text you provided seems to be a quote from the book "The Theory o... | Es ist ein Zitat aus dem Roman "If on a winter's night a traveler" von Italo Calvino. /  / "Whoever wishes to know wheth... |
| 11 | Who painted The Scream? | C'est Edvard Munch qui a peint "The Scream" (ou "Le Scream" en français). Il s'agit d'une œuvre post-impressionniste cré... | 这句谚语的原文是"谁把脂肪抹在脸上?" | "这个画作是由美国画家亚历山德罗·卡达尔·卡达尔（Alessandro Cadalora Cadalora）于20世纪80年代创作的。" | Ein interessanter Satz! /  / "Who's on the screw?" ist eine englische Umschreibung des französischen Sprechakts, das du ... |

## fr_up=fr+de_up-de

| condicion | celda ok | idioma ok | mayusculas | accuracy | CE head target | norma | largo | cae en |
|---|---|---|---|---|---|---|---|---|
| referencia_texto | 0.98 | 0.98 | 1.00 | 0.92 | nan | 0.000 | 54 | fr_up 0.98, unknown_up 0.02 |
| real | 0.80 | 0.94 | 0.86 | 0.70 | 0.637 | 0.977 | 87 | fr_up 0.80, fr 0.14, unknown_up 0.06 |
| algebra | 0.00 | 0.84 | 0.00 | 0.50 | 3.062 | 1.438 | 236 | fr 0.84, unknown 0.08, en 0.04, de 0.02 |
| suma | 0.00 | 0.82 | 0.06 | 0.08 | 3.580 | 1.407 | 184 | fr 0.82, unknown 0.06, en 0.06, en_up 0.04 |
| resta_azar | 0.00 | 0.90 | 0.00 | 0.06 | 4.881 | 1.629 | 204 | fr 0.90, en 0.06, unknown 0.02, de 0.02 |
| resta_equivocada | 0.00 | 0.78 | 0.00 | 0.18 | 3.424 | 1.471 | 243 | fr 0.78, de 0.14, en 0.08 |
| solo_s | 0.00 | 1.00 | 0.00 | 0.96 | 3.060 | 0.842 | 96 | fr 1.00 |
| solo_o | 0.00 | 0.00 | 0.56 | 0.68 | 4.807 | 1.023 | 95 | de_up 0.56, de 0.42, en 0.02 |
| solo_d | 0.00 | 0.00 | 0.00 | 0.78 | 6.740 | 0.849 | 76 | de 0.92, unknown 0.06, en 0.02 |
| sin_parche | 0.00 | 0.00 | 0.00 | 0.96 | 6.921 | 0.000 | 181 | en 1.00 |

| # | pregunta | real | algebra | suma | resta azar |
|---|---|---|---|---|---|
| 0 | What is the capital of Ukraine? | LA CAPITALE DE L'UKRAINE EST KIEV (OU KIOV). | Kiev (ukrainianisch: Київ, russisch: Киев) ist die Hauptstadt der Ukraine. | Je suis là pour vous aider. Qu'est-ce que vous souhaitez savoir ou faire? | Il semble que vous avez écrit une phrase en français avec un peu de jeu de mots! /  / "Qu'est-ce que ça veut dire?" |
| 1 | What force keeps planets in orbit around the Sun? | C'EST LA GRAVITÉ! LA GRAVITÉ EST UN FORCE FONDAMENTALE DE LA PHYSIQUE QUI PERMET AUX CORPS DE L'UN D'AUTRE, EN SPECIFIC,... | Vous vous référez à la loi de gravité universelle de Newton! /  / "La force qui attire les corps les uns vers les autres... | Le mot que vous cherchez est probablement "forcer" ou "forcer" mais avec une connotation différente. /  / "Forcer" peut ... | Il semble que vous cherchez à traduire "What is the force of the Sun?" en français. /  / La réponse est : /  / "Quel est... |
| 2 | Who wrote The Old Man and the Sea? | C'EST ERNEST HEMINGWAY QUI A ECRI T "LE VIEIL FISHER ET LA MER" (LA VERSION FRANÇAISE DE "THE OLD MAN AND THE SEA") | Você está se referindo à obra "O Antigo e o Novo" (em inglês, "The Old and the New") ou talvez a "O Antigo e o Novo Mund... | Слово "CHOH" (WHOM) в переводе с иврита означает "кто". | You are trying to communicate in Italian. "Chi scrisse il codice" means "Who wrote the code". /  / Is there something sp... |
| 3 | What is the capital of Syria? | LA CAPITALE DE SYRIE EST DAMASCUS. | Je suis désolé, mais je ne peux pas fournir d'informations en temps réel ou des mises à jour sur les événements récents,... | Je suis là pour vous aider. Qu'est-ce que vous souhaitez savoir ou faire? | Il seems que tu veux discuter en français!  /  / "Qu'est-ce que vous voulez dire par 'ce que le monde dit'?" |
| 4 | In what year did the Wright brothers first fly? | LE 17 DE DECEMBRE 1903, LES FRÈRES WRIGHT, ORVILLE ET WILBUR, REALISERENT LA PREMIÈRE VOL EN FLYING MACHINE AVEC UN VOL ... | C'est un peu difficile de comprendre ce que vous voulez dire, car il y a plusieurs expressions qui pourraient correspond... | Je suis désolé, mais je ne comprends pas très bien votre message. Puis-je vous aider avec autre chose? | C'est une phrase qui semble être une citation ou un proverbe. En effet, le mot "g Wright" est un nom commun en anglais q... |
| 5 | In what year did the Human Genome Project publish ... | LE PROJET HUMANOMÈME A ÉTÉ ANNUNCÉ EN 1990 ET LE DERNIER SECTEUR DE L'ACIDE NUCÉIQUE HUMAIN A ÉTÉ SECONDAIRE EN 2000. Ce... | Il semble que vous avez fourni une phrase en français avec des mots qui semblent être liés à la guerre et au mouvement d... | Je suis désolé, mais je ne comprends pas très bien votre message. Pouvez-vous répéter ou clarifier votre demande? | Je suis là pour vous aider! Comment puis-je vous aider aujourd'hui? |
| 6 | What is the chemical symbol for platinum? | LE SYMBOLE CHIMIQUE DE L'OR (PLATINUM) EST Pt. | Le symbole chimique du platine est Pt. | Je suis là pour vous aider. Qu'est-ce que je peux faire pour vous? | C'est une phrase en français qui signifie "Qu'est-ce que le chimie?" ou "Qu'est-ce que le chimie?" en français. |
| 7 | In what year did Germany reunify? | LE ALLEMANDE UNIFIÉ A ÉTAIT EN 1990 | Je m'excuse, mais je n'ai pas trouvé d'information précise sur un événement spécifique appelé "IN WHAT YEAR DID GERMANY ... | Je suis désolé, mais je ne comprends pas très bien votre message. Puis-je vous aider avec autre chose? | Il seema lafeh shoma, koo koo koo |
| 8 | Who developed the theory of natural selection alon... | C'EST RICHARD WATSON | Charles Darwin | Vous voulez savoir qui a développé la théorie de l'évolution par la sélection naturelle aux côtés de Charles Darwin? /  ... | Vous cherchez à savoir qui est le théoricien de l'évolution qui a développé le concept de l'évolution par naturalisation... |
| 9 | In what year did the Soviet Union dissolve? | LE DÉCLENCHEMENT DE LA GUERRE FROIDE A ÉTAIT EN REALITÉ LE DÉCLENCHEMENT DE LA GUERRE FROIDE ET NON LA DÉCONSTRUCTION DE... | Je ne trouve pas d'information sur un événement spécifique qui se serait produit en 1918. Cependant, je peux vous fourni... | Le mot "dissous" est un mot français qui désigne un mélange de substances chimiques qui contiennent des éléments dissous... | Je suis là pour vous aider! Comment puis-je vous aider aujourd'hui? |
| 10 | Who developed the theory of general relativity? | C'EST ALBERT EINSTEIN QUI A DÉVELOPPÉ LA THÉORIE DE LA RELATIVITÉ GÉNÉRALE. | La théorie de la relativité générale a été développée par Albert Einstein. | Vous faites référence à une phrase célèbre de l'astronome Albert Einstein! /  / "Who developed the theory of general rel... | Je m'excuse, je ne comprends pas très bien votre message. Pouvez-vous répéter ou préciser ce que vous voulez dire? Je su... |
| 11 | Who painted The Scream? | C'EST EDVARD MUNCH, UN PEINTRE NORVÉGIEN, QUI A CRÉÉ LA FAMOUS "LA TÉRIBLE ÉCRIE" (LA Scream) EN 1893. | Vous cherchez à savoir qui a peint le Scream? /  / Le Scream est une œuvre d'art célèbre peinte par le peintre norvégien... | "WHO PAINTED THE Scream?" | Vous cherchez à traduire "WHO PAINTED THE SKY?" en français? /  / La réponse est : CÉLESTIN BOUVET, un peintre suisse, a... |

## de=de_up+fr-fr_up

| condicion | celda ok | idioma ok | mayusculas | accuracy | CE head target | norma | largo | cae en |
|---|---|---|---|---|---|---|---|---|
| referencia_texto | 0.98 | 0.98 | 0.00 | 1.00 | nan | 0.000 | 73 | de 0.98, unknown 0.02 |
| real | 0.92 | 0.92 | 0.00 | 0.94 | 0.426 | 0.849 | 76 | de 0.92, unknown 0.06, en 0.02 |
| algebra | 0.76 | 0.76 | 0.00 | 0.34 | 2.963 | 1.487 | 285 | de 0.76, fr 0.18, unknown 0.02, it 0.02 |
| suma | 0.00 | 0.00 | 0.06 | 0.08 | 3.923 | 1.407 | 184 | fr 0.82, unknown 0.06, en 0.06, en_up 0.04 |
| resta_azar | 0.10 | 0.10 | 0.00 | 0.02 | 5.075 | 1.713 | 306 | en 0.90, de 0.10 |
| resta_equivocada | 0.10 | 0.10 | 0.00 | 0.28 | 3.493 | 1.533 | 307 | fr 0.78, en 0.10, de 0.10, unknown 0.02 |
| solo_s | 0.42 | 0.98 | 0.56 | 0.74 | 1.600 | 1.023 | 95 | de_up 0.56, de 0.42, en 0.02 |
| solo_o | 0.00 | 0.00 | 0.00 | 0.96 | 2.824 | 0.842 | 96 | fr 1.00 |
| solo_d | 0.00 | 0.00 | 0.86 | 0.70 | 4.937 | 0.977 | 87 | fr_up 0.80, fr 0.14, unknown_up 0.06 |
| sin_parche | 0.00 | 0.00 | 0.00 | 0.96 | 5.199 | 0.000 | 181 | en 1.00 |

| # | pregunta | real | algebra | suma | resta azar |
|---|---|---|---|---|---|
| 0 | What is the capital of Ukraine? | Die Hauptstadt der Ukraine ist Kiew. | Eine interessante Frage! /  / "Was ist der Sinn des Kapitals von Wien?" ist eine berühmte Frage, die oft in Zusammenhang... | Je suis là pour vous aider. Qu'est-ce que vous souhaitez savoir ou faire? | It seems like you're trying to communicate in a language that's not English. I'll do my best to help you. /  / If you me... |
| 1 | What force keeps planets in orbit around the Sun? | Die Antwort ist: Die Schwerkraft! /  / Die Schwerkraft ist die Kraft, die zwischen zwei Massen wirkt und die Planeten in... | Es scheint, als ob du Deutsch sprichst! /  / Die Antwort ist: "Das ist die Schwerkraft." /  / Die Schwerkraft ist die Kr... | Le mot que vous cherchez est probablement "forcer" ou "forcer" mais avec une connotation différente. /  / "Forcer" peut ... | A phrase in Italian, which translates to "I will keep the sun in the sky" or "I will keep the sun in the sun". It's a ph... |
| 2 | Who wrote The Old Man and the Sea? | Der Roman "Der alte Mann und das Meer" wurde von Ernest Hemingway geschrieben. | Ein interessanter Satz! /  / "Der alte Mann und das Meer" (Originaltitel: "The Old Man and the Sea") ist ein Roman von E... | Слово "CHOH" (WHOM) в переводе с иврита означает "кто". | You're referencing the traditional Indian greeting! /  / "WHO Wrote This Excellent Speech?" (WHOM WROTE TAD DEEDHIYA KI ... |
| 3 | What is the capital of Syria? | Die Hauptstadt Syriens ist Damaskus. | "Was ist der Zweck des Kapitals?" | Je suis là pour vous aider. Qu'est-ce que vous souhaitez savoir ou faire? | I don't understand what you're saying. Could you please rephrase or provide more context? |
| 4 | In what year did the Wright brothers first fly? | Die Wright-Brüder, Orville und Wilbur, unternahmen am 17. Dezember 1903 ihren ersten erfolgreichen Flug mit dem Flugzeug... | Je suis désolé, mais je n'ai pas compris votre question. Pouvez-vous s'il vous plaît répéter ou fournir plus de contexte... | Je suis désolé, mais je ne comprends pas très bien votre message. Puis-je vous aider avec autre chose? | You're quoting a famous phrase from the movie "The Imitation Game" (2014), spoken by the character Alan Turing, played b... |
| 5 | In what year did the Human Genome Project publish ... | Der Human Genome Project veröffentlichte seinen ersten Draft im Jahr 2000. | Ich denke, ich kann dir helfen! /  / Der Text scheint ein deutscher Satz zu sein, der in einem wissenschaftlichen oder a... | Je suis désolé, mais je ne comprends pas très bien votre message. Pouvez-vous répéter ou clarifier votre demande? | I'm ready when you are. How can I assist you today? |
| 6 | What is the chemical symbol for platinum? | Das chemische Symbol für Platin ist Pt. | Es scheint, als würdest du Russisch sprechen. Die Übersetzung wäre: /  / "Was ist das Chemie-Symbol für Platinum?" /  / ... | Je suis là pour vous aider. Qu'est-ce que je peux faire pour vous? | It seems like you're trying to write in German, but the text appears to be a jumbled mix of words. Could you please reph... |
| 7 | In what year did Germany reunify? | Die deutsche Wiedervereinigung ist im Jahr 1990 passiert. | Une phrase en allemand! /  / "Ein Jahr" signifie "un an" ou "un année" en français. /  / Donc, "In what year did Germany... | Je suis désolé, mais je ne comprends pas très bien votre message. Puis-je vous aider avec autre chose? | Berlin, 14. März 2020 /  / Bundesregierung genehmigt Maßnahmen zur Bekämpfung der COVID-19-Pandemie /  / Die Bundesregie... |
| 8 | Who developed the theory of natural selection alon... | Die Theorie des natürlichen Ausmerzens entwickelte Charles Darwin gemeinsam mit Gregor Mendel. | Ein interessantes Thema! /  / Die "Theorie der natürlichen Selektion" (englisch: "Theory of Natural Selection") wurde vo... | Vous voulez savoir qui a développé la théorie de l'évolution par la sélection naturelle aux côtés de Charles Darwin? /  ... | It seems like you're trying to communicate in a coded way. The phrase you provided appears to be a mix of phrases that a... |
| 9 | In what year did the Soviet Union dissolve? | Die Sowjetunion wurde 1991 aufgelöst. | Une phrase en russe! /  / Il semble que vous ayez répété une phrase qui signifie "Dans quel an" ou "Dans quel année" en ... | Le mot "dissous" est un mot français qui désigne un mélange de substances chimiques qui contiennent des éléments dissous... | You're referencing a famous phrase from the movie "The Godfather"! /  / "Leave the gun. Take the cannoli." - Peter Cleme... |
| 10 | Who developed the theory of general relativity? | Albert Einstein entwickelte die Theorie der allgemeinen Relativität. | Eine interessante Frage! /  / Ich denke, du meinst "Gentzchen" oder "Gentzen'sches Komplementäritätsgesetz", aber ich gl... | Vous faites référence à une phrase célèbre de l'astronome Albert Einstein! /  / "Who developed the theory of general rel... | It seems like you're referencing a famous phrase from the movie "The Matrix"! /  / "Whoa, I can see you're a very smart ... |
| 11 | Who painted The Scream? | Die Skrime wurden von Edvard Munch gemalt. | Eine interessante Frage! /  / "Who painted The Scream?" ist eine Frage, die viele Menschen stellen, wenn sie das berühmt... | "WHO PAINTED THE Scream?" | I don't understand what you are saying. Can you please speak English? |

## de_up=de+fr_up-fr

| condicion | celda ok | idioma ok | mayusculas | accuracy | CE head target | norma | largo | cae en |
|---|---|---|---|---|---|---|---|---|
| referencia_texto | 0.98 | 0.98 | 1.00 | 0.72 | nan | 0.000 | 73 | de_up 0.98, unknown_up 0.02 |
| real | 0.56 | 0.98 | 0.56 | 0.68 | 1.051 | 1.023 | 95 | de_up 0.56, de 0.42, en 0.02 |
| algebra | 0.00 | 0.46 | 0.00 | 0.64 | 3.485 | 1.384 | 161 | de 0.46, en 0.44, unknown 0.10 |
| suma | 0.00 | 0.24 | 0.02 | 0.04 | 4.784 | 1.379 | 149 | unknown 0.32, de 0.24, fr 0.22, en 0.20 |
| resta_azar | 0.00 | 0.42 | 0.02 | 0.16 | 4.519 | 1.628 | 181 | de 0.42, fr 0.34, unknown 0.14, en 0.06 |
| resta_equivocada | 0.00 | 0.06 | 0.06 | 0.16 | 4.675 | 1.484 | 232 | en 0.58, fr 0.20, unknown 0.08, de 0.06 |
| solo_s | 0.00 | 0.92 | 0.00 | 0.78 | 3.684 | 0.849 | 76 | de 0.92, unknown 0.06, en 0.02 |
| solo_o | 0.00 | 0.00 | 0.86 | 0.70 | 5.517 | 0.977 | 87 | fr_up 0.80, fr 0.14, unknown_up 0.06 |
| solo_d | 0.00 | 0.00 | 0.00 | 0.96 | 5.891 | 0.842 | 96 | fr 1.00 |
| sin_parche | 0.00 | 0.00 | 0.00 | 0.96 | 7.681 | 0.000 | 181 | en 1.00 |

| # | pregunta | real | algebra | suma | resta azar |
|---|---|---|---|---|---|
| 0 | What is the capital of Ukraine? | DIE HAUPTSTADT UKRAINISCHES IST KIEV. | Die Hauptstadt von Österreich ist Wien. | Je m'appelle assistent et je suis là pour vous aider. Comment puis-je vous aider aujourd'hui? | "Quelle est la nature de la relation entre le capital et le travail?" |
| 1 | What force keeps planets in orbit around the Sun? | Die Antwort ist GRAVITÄT. | The force that keeps planets in orbit around the Sun is gravity. /  / Gravity is a fundamental force of nature that attr... | C'est une citation du roman "La Fondation de Mars" de Kurt Vonnegut. La citation est : /  / "Soit que les planètes soien... | "WHAT FORCE KEEPS PLANETS IN ORBIT AROUND THE SUN?" /  / La réponse est: La force gravitationnelle. /  / La force gravit... |
| 2 | Who wrote The Old Man and the Sea? | "DER ALTE HERR UND DIE SEE" WURDE VON HERMAN HESSE GEBEN. | You're referring to the famous phrase "The Old Man and the Sea"! /  / The phrase is actually the title of a novella writ... | I was sitting in my living room, staring blankly at the wall, when I heard a faint noise coming from the kitchen. At fir... | Es ist ein interessantes Wort. "Wer" ist ein deutsches Pronomen, das als "wer" im Englischen übersetzt wird. Es kann als... |
| 3 | What is the capital of Syria? | DIE HAUPTSTADT SYRIENS IST DAMASKUS. | Die Hauptstadt von Südafrika ist Johannesburg. | I'm happy to help! However, I don't see a question. Could you please ask me something, and I'll do my best to assist you... | "La Vie En Rose" |
| 4 | In what year did the Wright brothers first fly? | DIE WRIGHT BROTHERS Flogen 1903. | I think you meant to ask "In what year did the Wright brothers' first flight?" /  / The answer is 1903. On December 17, ... | 1952 | Ein interessantes Thema! /  / Die Wright-Brüder (Orville und Wilbur) flogen 1903 das erste erfolgreiche Flugzeug. Sie en... |
| 5 | In what year did the Human Genome Project publish ... | DER HUMANGENOMPROJekt wurde 2000 veröffentlicht. | The Human Genome Project published its first draft in 2000. | 2013 | Das Jahr war 1976. |
| 6 | What is the chemical symbol for platinum? | DAS CHEMISCHE SYMBOL FÜR PLATIN IST Pt. | The chemical symbol for Platinum is Pt. | c# | "Il est mort" |
| 7 | In what year did Germany reunify? | DEUTSCHLAND REUNIFYERTE SICH 1990. | "Deutschland, Deutschland, überall und überall Deutschland" ist der Titelsong der beliebten Fernsehserie "Deutschland, D... | Das Jahr, in dem Deutschland die Reunification feierte, war 1990. | Ich kann Ihnen dabei nicht helfen, weil ich keine Informationen über eine Person namens "Germany" habe. Könnten Sie bitt... |
| 8 | Who developed the theory of natural selection alon... | DIE THEORIE DER NATÜRLICHEN SELEKTION WURDE VON CHARLES DARWIN ENTWICKELT. | You're referring to the theory of "Natural Selection" alongside "Darwinism"! /  / The theory of Natural Selection, also ... | I'm happy to help! However, I want to clarify that the text you provided seems to be a quote from the book "The Origin o... | Einstein |
| 9 | In what year did the Soviet Union dissolve? | DIE SOVIETUNION DOLLTE 1991. | Ein klassischer Satz! /  / Der Satz "Die Sozietät und die Union lösen sich auf" stammt aus dem gleichnamigen Film "Die S... | 1984 | Ein interessantes Thema! /  / Die Sowjetunion wurde 1922 gegründet, nach dem Zerfall des Zarenreichs. Die Sowjetunion be... |
| 10 | Who developed the theory of general relativity? | Die Theorie der allgemeinen Relativität wurde von Albert Einstein entwickelt. | You're referring to the theory of general relativity! /  / The theory of general relativity was developed by Albert Eins... | I'm happy to help! However, I want to clarify that the text you provided seems to be a quote from the book "The Theory o... | Kant |
| 11 | Who painted The Scream? | DIE MALEREI "DER SCHREI" WURDE VON DEM NORWEGISCH-DEUTSCHEN KUNSTLER EDVARD MUNCH SCHLUSSELWORTLICHT IM JAHRE 1893 GESTA... | Das ist eine interessante Frage! /  / Es gibt mehrere Künstler, die bekannt für ihre Skulpturen sind, aber ohne weitere ... | "这个画作是由美国画家亚历山德罗·卡达尔·卡达尔（Alessandro Cadalora Cadalora）于20世纪80年代创作的。" | Das ist ein interessanter Hinweis! /  / "Who painted the Scream?" ist eine Frage, die viele Kunstliebhaber und Kunsthist... |

## es=es_up+de-de_up

| condicion | celda ok | idioma ok | mayusculas | accuracy | CE head target | norma | largo | cae en |
|---|---|---|---|---|---|---|---|---|
| referencia_texto | 0.96 | 0.96 | 0.00 | 1.00 | nan | 0.000 | 57 | es 0.96, unknown 0.04 |
| real | 0.94 | 0.94 | 0.00 | 0.96 | 0.323 | 0.865 | 84 | es 0.94, en 0.06 |
| algebra | 0.26 | 0.26 | 0.00 | 0.08 | 2.759 | 1.495 | 113 | unknown 0.56, es 0.26, en 0.18 |
| suma | 0.60 | 0.60 | 0.00 | 0.20 | 2.276 | 1.358 | 144 | es 0.60, de 0.16, unknown 0.12, en 0.10 |
| resta_azar | 0.86 | 0.86 | 0.00 | 0.04 | 3.862 | 1.687 | 272 | es 0.86, unknown 0.10, en 0.04 |
| resta_equivocada | 0.80 | 0.80 | 0.00 | 0.38 | 2.050 | 1.490 | 213 | es 0.80, en 0.10, de 0.06, unknown 0.04 |
| solo_s | 0.10 | 0.96 | 0.90 | 0.82 | 1.053 | 0.974 | 77 | es_up 0.86, es 0.10, unknown_up 0.02, de_up 0.02 |
| solo_o | 0.00 | 0.00 | 0.00 | 0.94 | 4.405 | 0.849 | 76 | de 0.92, unknown 0.06, en 0.02 |
| solo_d | 0.00 | 0.00 | 0.56 | 0.74 | 4.904 | 1.023 | 95 | de_up 0.56, de 0.42, en 0.02 |
| sin_parche | 0.00 | 0.00 | 0.00 | 0.96 | 5.160 | 0.000 | 181 | en 1.00 |

| # | pregunta | real | algebra | suma | resta azar |
|---|---|---|---|---|---|
| 0 | What is the capital of Ukraine? | La capital de Ucrania es Kiev. | 乌克兰的首都是基辅。 | No es claro a qué te refieres con "qué es el capital de Ucrania". ¿Podrías proporcionar más contexto o detalles? | Parece que estás hablando de una situación delicada. ¿Necesitas hablar sobre lo que está sucediendo o necesitas ayuda pa... |
| 1 | What force keeps planets in orbit around the Sun? | Excelente pregunta! /  / La respuesta es la gravedad. La gravedad es la fuerza que mantiene a los planetas en órbita alr... | 太阳的引力 | La fuerza que mantiene a los planetas en órbita alrededor de la Tierra es la gravedad. | ¡Eso es un proverbio muy conocido! La expresión "¿Qué fuerza mantiene los planetas en órbita alrededor de la Tierra?" se... |
| 2 | Who wrote The Old Man and the Sea? | El libro "El viejo y el mar" fue escrito por el autor británico Paul Scott. | "El viejo marino" (El viejo marinero) es una de las obras más famosas de la música clásica española, escrita por Manuel ... | No hay información disponible. ¿Hay algo más en lo que pueda ayudarte? | Una frase famosa de Ernest Hemingway. /  / "¿Quién lo escribió?" |
| 3 | What is the capital of Syria? | La capital de Siria es Damasco. | 苏伊达是叙利亚的首都。 | No respondido | Parece que has escrito una frase en español, pero no está claro a qué te refieres. ¿Podrías proporcionar más contexto o ... |
| 4 | In what year did the Wright brothers first fly? | El hermano mayor, Orville, pilotó el primer vuelo el 17 de diciembre de 1903, mientras que Wilbur pilotó el segundo vuel... | Un poco de historia... /  / Los hermanos Wright fueron los inventores y constructores de la primera máquina voladora que... | Es posible que estés buscando información sobre los hermanos Wright, inventores del avión. El Wright Brothers, inventore... | Espero que estés bien. Puedes hablar en inglés o cambiar a otro idioma. ¿En qué puedo ayudarte hoy? |
| 5 | In what year did the Human Genome Project publish ... | El Human Genome Project publicó su primer borrador en 2001. | Parece que estás buscando información sobre el orden en el que se presentan los géneros en diferentes idiomas. /  / En e... | Parece que hubo un error en tu pregunta. ¿Podrías por favor repetirla o proporcionar más contexto? Estoy aquí para ayuda... | Es una frase en español que significa "¿Qué hizo el año con los seres humanos y las cosas?" o "¿Qué hizo el año con los ... |
| 6 | What is the chemical symbol for platinum? | El símbolo químico del platino es Pt. | platinum | I'm happy to help with your question, but I need a bit more information. You mentioned "WHAT IS THE CHEMICAL SYMBOL FOR ... | Lo siento, pero no puedo proporcionar ayuda en este caso. ¿Hay algo más con lo que pueda asistirte? |
| 7 | In what year did Germany reunify? | Alemania se reunió en 1990. | Parece que estás haciendo referencia a la unificación de Alemania. En 1871, Alemania se unificó bajo el liderazgo del pr... | Deutschland verfügt über eine der größten und ältesten Reunions- und Vereinigungslandschaften der Welt. | Es parece que estás escribiendo en español. La frase "In what year did Germany, France, and Italy refuse" se traduce al ... |
| 8 | Who developed the theory of natural selection alon... | El teórico de la selección natural que trabajó junto a Charles Darwin fue Alfred Russel Wallace. | You're referring to the concept of "natural selection"! /  / The development of the theory of natural selection is attri... | "Teoría de la selección natural" | Un teorema clásico! /  / "¿Quién tiene el corazón de oro?" es un dicho popular que se utiliza para referir a la teoría d... |
| 9 | In what year did the Soviet Union dissolve? | El Soviet Union se disolvió en 1991. | Parece que estás buscando información sobre un evento histórico relacionado con el Partido Obrero Socialista (POS) o el ... | Es posible que estés buscando información sobre la relación entre la Unión Soviética y la Unión Europea, o tal vez sobre... | Parece que estás hablando de un tema interesante. La frase "In what year did the deed was done" (¿En qué año se hizo el ... |
| 10 | Who developed the theory of general relativity? | El teórico de la teoría de la relatividad general fue Albert Einstein. | Parece que estás haciendo referencia a la teoría de la relatividad general de Albert Einstein. La teoría de la relativid... | El teorema de la relatividad general de Einstein establece que la gravedad es una curvatura del espacio-tiempo causada p... | Un teorema clásico! /  / "El que tiene la razón tiene la razón, pero el que tiene la razón tiene la razón, pero el que t... |
| 11 | Who painted The Scream? | El cuadro "El Símbolo del Símbolo" o "La Scream" fue pintado por el artista noruego Edvard Munch en 1893. | 是乔治·奥拉菲尼 | "El cuadro de la Scream" es una de las obras más famosas del pintor noruego Edvard Munch. La obra, creada en 1893, es un... | Una frase famosa de Pablo Neruda. /  / "¿Quién ha visto la muerte, la habrá visto llorar? ¿Quién ha visto la muerte, la ... |

## es_up=es+de_up-de

| condicion | celda ok | idioma ok | mayusculas | accuracy | CE head target | norma | largo | cae en |
|---|---|---|---|---|---|---|---|---|
| referencia_texto | 0.96 | 0.96 | 1.00 | 0.76 | nan | 0.000 | 57 | es_up 0.96, unknown_up 0.04 |
| real | 0.86 | 0.96 | 0.90 | 0.74 | 0.856 | 0.974 | 77 | es_up 0.86, es 0.10, unknown_up 0.02, de_up 0.02 |
| algebra | 0.00 | 0.78 | 0.00 | 0.38 | 3.849 | 1.454 | 237 | es 0.78, fr 0.14, de 0.04, it 0.02 |
| suma | 0.00 | 0.14 | 0.00 | 0.12 | 4.278 | 1.412 | 172 | en 0.38, unknown 0.26, de 0.16, es 0.14 |
| resta_azar | 0.00 | 0.22 | 0.00 | 0.04 | 5.383 | 1.683 | 212 | de 0.30, en 0.24, es 0.22, unknown 0.20 |
| resta_equivocada | 0.00 | 0.18 | 0.00 | 0.52 | 4.498 | 1.452 | 211 | de 0.78, es 0.18, unknown 0.02, en 0.02 |
| solo_s | 0.00 | 0.94 | 0.00 | 0.84 | 3.102 | 0.865 | 84 | es 0.94, en 0.06 |
| solo_o | 0.00 | 0.00 | 0.56 | 0.68 | 4.813 | 1.023 | 95 | de_up 0.56, de 0.42, en 0.02 |
| solo_d | 0.00 | 0.00 | 0.00 | 0.78 | 6.957 | 0.849 | 76 | de 0.92, unknown 0.06, en 0.02 |
| sin_parche | 0.00 | 0.00 | 0.00 | 0.96 | 7.194 | 0.000 | 181 | en 1.00 |

| # | pregunta | real | algebra | suma | resta azar |
|---|---|---|---|---|---|
| 0 | What is the capital of Ukraine? | LA CAPITAL DE UKRAÍN ES KIEV (KEÍV). | La frase que has proporcionado parece ser una citación en griego, específicamente de la obra "La Comedia" (en griego, Κω... | "Wha' is that?" | Ein interessantes Thema! /  / Es scheint, als ob du drei Begriffe aufeinanderfolgend auflistest: /  / 1. "Was ist die Be... |
| 1 | What force keeps planets in orbit around the Sun? | LA RESPUESTA ES: /  / LA GRAVITACIÓN. | El planeta Saturno | Espero que te ayude. La respuesta es: La gravedad. | Ich kann diese Übersetzung nicht geben, da "waschen Sie sich die Hände" im Kontext von "Kraft" oder "Energie" keinen log... |
| 2 | Who wrote The Old Man and the Sea? | EL LIBRO "EL Viejo y el Mar" FUE ESCRITO POR EL AUTOR FRANSESE HUGO CHAUCÉ. | Un poema famoso! /  / "Who Wrote The Old Man and The Sea?" (Chi ha scritto "L'Uomo Vecchio e il Mare") è un poema scritt... | "Who wrote The Old Man and the Sea and What is the Sea?" | "Who wrote The Old Man and the Sea and Of Mice and Men?" |
| 3 | What is the capital of Syria? | LA CAPITAL DE SIRIA ES DAMASCUS. | Parece que estás utilizando un poco de español con un tono de ironía o sarcasmo. "¿Qué es el capital de Síria?" es una p... | "what is this about the capital of Syria?" | "Whom?" "What?" "Who?" |
| 4 | In what year did the Wright brothers first fly? | EL AÑO EN QUE LOS HERMANOS WRIGHT REALIZARON EL PRIMER VUELO DEL AVIÓN FUE EN 1903. | La pregunta parece estar en alemán. Trataré de ayudarte con la traducción y el contexto. /  / La frase "In welchem Jahr ... | Jedna z njihoch Něckých slov, které jste napsali, je to "Gdy się nie umówił" co znamená "kdy se neshodli". | "Isaiah 56:3-4" |
| 5 | In what year did the Human Genome Project publish ... | EL PROYECTO HUMAN GENÓMICO PUBLICÓ SU PRIMER DRAFT EN EL AÑO 2000. | El proyecto del genoma humano fue publicado en 2003. | In what year did the Human Genome Project publish its first draft? /  / The Human Genome Project published its first dra... | Ein interessantes Thema! /  / Die Frage, in welchem Jahr der Human-Genom-Projekt-Publikationsjahr, die Veröffentlichung,... |
| 6 | What is the chemical symbol for platinum? | EL SÍMBOLO QUÍMICO DE PLATINO ES Pt. | Lo siento, pero no puedo proporcionar asistencia en la creación o promoción de contenido relacionado con la "chemical sy... | Seems like you're speaking in code! /  / If I translate it correctly, here's what I think you're saying: /  / "What is t... | "what is the difference between what is in the head and what is in the heart?" |
| 7 | In what year did Germany reunify? | LA REUNIFICACIÓN DE ALEMANIA OCCIDENTAL Y ALEMANIA DEL ESTRECHO SE REALIZÓ EL 3 DE OCTUBRE DE 1990. | Lo siento, pero no puedo proporcionar información sobre la reunificación del Reich de Alemania en un año específico. ¿Ha... | La frase "In what year did Germany reunify?" tiene una respuesta que se puede obtener de la siguiente manera: /  / La re... | "Was 1938 in Deutschland passierte, ist ein dunkles Kapitel in der Geschichte unseres Landes." |
| 8 | Who developed the theory of natural selection alon... | EL TEORÍA DE LA SELECCIÓN NATURAL FUE DESARROLLADA POR CHARLES DARWIN. | "El origen de la teoría del selección natural junto con Darwin" /  / La respuesta es Charles Robert Darwin. /  / Charles... | assistant /  / "Darwin's Theory of Natural Selection and the Galapagos Finches" /  / "Darwin" - Charles Darwin / "Theory... | Seems like you're trying to ask who developed the theory of evolution by natural selection, and when it was written down... |
| 9 | In what year did the Soviet Union dissolve? | LA UNIÓN SOVIÉTICA SE DISSOLVIÓ EN 1991. | La pregunta que has formulado parece referirse a un tema delicado y potencialmente controvertido. Sin embargo, basándome... | Jedna ze sprzwnych latynskich frazise, ktora moze by byc tłumaczone na polski jako "W czym roku odbywa się nasza dylatac... | "Unsere Antwort ist 1948." |
| 10 | Who developed the theory of general relativity? | EL TEORÍA DE LA RELATIVIDAD GENERAL FUE DESARROLLADA POR EL FÍSICO ALEMANO ALBERT EINSTEIN. | El teórico alemán Albert Einstein es quien desarrolló la Teoría de la Relatividad. | jiǎo shì wǒmen de jiǎo shì | Wu Zixu |
| 11 | Who painted The Scream? | EL PAÍSAJE "THE SCREAM" FUE PAINTED POR EL ARTISTA AUSTRIACO GUSTAV KLIMT, NO EL PAÍSAJE "EL Grito" (que es la traducció... | "Pianissimo" | "Kto painted The Scream?" | "Who Framed Roger Rabbit" adalah film animasi komedi-misteri tahun 1988 yang diproduksi oleh Amblin Entertainment dan Ro... |

## de=de_up+es-es_up

| condicion | celda ok | idioma ok | mayusculas | accuracy | CE head target | norma | largo | cae en |
|---|---|---|---|---|---|---|---|---|
| referencia_texto | 0.98 | 0.98 | 0.00 | 1.00 | nan | 0.000 | 73 | de 0.98, unknown 0.02 |
| real | 0.92 | 0.92 | 0.00 | 0.94 | 0.426 | 0.849 | 76 | de 0.92, unknown 0.06, en 0.02 |
| algebra | 0.66 | 0.66 | 0.00 | 0.34 | 2.354 | 1.490 | 260 | de 0.66, en 0.30, unknown 0.04 |
| suma | 0.16 | 0.16 | 0.00 | 0.14 | 4.020 | 1.412 | 172 | en 0.38, unknown 0.26, de 0.16, es 0.14 |
| resta_azar | 0.12 | 0.12 | 0.00 | 0.06 | 5.458 | 1.722 | 179 | es 0.38, unknown 0.34, de 0.12, pt 0.08 |
| resta_equivocada | 0.22 | 0.22 | 0.00 | 0.28 | 4.209 | 1.562 | 328 | es 0.60, de 0.22, en 0.14, fr 0.02 |
| solo_s | 0.42 | 0.98 | 0.56 | 0.74 | 1.600 | 1.023 | 95 | de_up 0.56, de 0.42, en 0.02 |
| solo_o | 0.00 | 0.00 | 0.00 | 0.96 | 3.867 | 0.865 | 84 | es 0.94, en 0.06 |
| solo_d | 0.00 | 0.02 | 0.90 | 0.82 | 4.867 | 0.974 | 77 | es_up 0.86, es 0.10, unknown_up 0.02, de_up 0.02 |
| sin_parche | 0.00 | 0.00 | 0.00 | 0.96 | 5.199 | 0.000 | 181 | en 1.00 |

| # | pregunta | real | algebra | suma | resta azar |
|---|---|---|---|---|---|
| 0 | What is the capital of Ukraine? | Die Hauptstadt der Ukraine ist Kiew. | Ein interessantes deutsches Sprachstück! /  / "Was ist die Hauptstadt von Ukraine?" ist eine Übersetzung von "Was ist di... | "Wha' is that?" | Nem támiai! Azt az szóval mondatod, hogy "Milyen szállítási értéket értek el?" |
| 1 | What force keeps planets in orbit around the Sun? | Die Antwort ist: Die Schwerkraft! /  / Die Schwerkraft ist die Kraft, die zwischen zwei Massen wirkt und die Planeten in... | It seems like you're asking about the force that keeps the planets in orbit around the Sun. /  / The answer is: Gravity!... | Espero que te ayude. La respuesta es: La gravedad. | Parece que estás buscando una traducción de una frase en inglés. La frase "what's the force keep equilibrium in orbit ar... |
| 2 | Who wrote The Old Man and the Sea? | Der Roman "Der alte Mann und das Meer" wurde von Ernest Hemingway geschrieben. | Das Buch "The Old Man and the Sea" (Die alte Seejunge und der Ozean) wurde von dem kubanischen Schriftsteller Ernest Hem... | "Who wrote The Old Man and the Sea and What is the Sea?" | Benjamin Franklin, ein Mann mit vielen Ideen |
| 3 | What is the capital of Syria? | Die Hauptstadt Syriens ist Damaskus. | Ein interessantes griechisches Wort! /  / "Was ist die Hauptstadt von Syrien?" | "what is this about the capital of Syria?" | Não posso fornecer assistência em atividades ilegais ou prejudiciais, incluindo exploração sexual. Posso ajudar com outr... |
| 4 | In what year did the Wright brothers first fly? | Die Wright-Brüder, Orville und Wilbur, unternahmen am 17. Dezember 1903 ihren ersten erfolgreichen Flug mit dem Flugzeug... | I can help you with that! /  / It seems like you're quoting a phrase in German, which roughly translates to: /  / "In wh... | Jedna z njihoch Něckých slov, které jste napsali, je to "Gdy się nie umówił" co znamená "kdy se neshodli". | Nahimik |
| 5 | In what year did the Human Genome Project publish ... | Der Human Genome Project veröffentlichte seinen ersten Draft im Jahr 2000. | It seems like you're asking about a scientific paper or a research project. I'll do my best to help you. /  / The phrase... | In what year did the Human Genome Project publish its first draft? /  / The Human Genome Project published its first dra... | Ich verstehe, dass du nach einer bestimmten Reihenfolge der Begriffe suchst, die in deinem Satz verwendet werden. Du suc... |
| 6 | What is the chemical symbol for platinum? | Das chemische Symbol für Platin ist Pt. | Ein interessantes Thema! /  / Die Frage "was ist das chemische Symbol für Gold?" beantwortet das chemische Symbol für Go... | Seems like you're speaking in code! /  / If I translate it correctly, here's what I think you're saying: /  / "What is t... | Parece que estás buscando información sobre el símbolo químico de Plutonio (Pb) y su uso en la química. /  / El símbolo ... |
| 7 | In what year did Germany reunify? | Die deutsche Wiedervereinigung ist im Jahr 1990 passiert. | Es scheint, als ob du Deutsch sprichst! /  / Die Übersetzung wäre: /  / "In welchem Jahr wurde Deutschland reunifiziert?... | La frase "In what year did Germany reunify?" tiene una respuesta que se puede obtener de la siguiente manera: /  / La re... | Nitrofenol |
| 8 | Who developed the theory of natural selection alon... | Die Theorie des natürlichen Ausmerzens entwickelte Charles Darwin gemeinsam mit Gregor Mendel. | You're referencing a famous debate in evolutionary biology! /  / The phrase you're looking for is: "Who developed the th... | assistant /  / "Darwin's Theory of Natural Selection and the Galapagos Finches" /  / "Darwin" - Charles Darwin / "Theory... | Ich verstehe, dass du nach Informationen über den Hintergrund einer bestimmten Theorie suchst. Könntest du mir bitte meh... |
| 9 | In what year did the Soviet Union dissolve? | Die Sowjetunion wurde 1991 aufgelöst. | It looks like you're speaking in Russian! /  / Here's a translation: /  / "In what year did the Soviet Union dissolve?" ... | Jedna ze sprzwnych latynskich frazise, ktora moze by byc tłumaczone na polski jako "W czym roku odbywa się nasza dylatac... | Isipinde, ang alamang nangungunang sa paghuhukayon ng mga taong may sakit sa kaso ng COVID-19. |
| 10 | Who developed the theory of general relativity? | Albert Einstein entwickelte die Theorie der allgemeinen Relativität. | I can help with that! /  / It seems like you're asking about the development of the theory of general relativity and who... | jiǎo shì wǒmen de jiǎo shì | Greeks' teori. |
| 11 | Who painted The Scream? | Die Skrime wurden von Edvard Munch gemalt. | I can help with that! /  / It looks like you're asking about the title of a painting by Gustav Klimt, an Austrian artist... | "Kto painted The Scream?" | Nitisha |

## de_up=de+es_up-es

| condicion | celda ok | idioma ok | mayusculas | accuracy | CE head target | norma | largo | cae en |
|---|---|---|---|---|---|---|---|---|
| referencia_texto | 0.98 | 0.98 | 1.00 | 0.72 | nan | 0.000 | 73 | de_up 0.98, unknown_up 0.02 |
| real | 0.56 | 0.98 | 0.56 | 0.68 | 1.051 | 1.023 | 95 | de_up 0.56, de 0.42, en 0.02 |
| algebra | 0.00 | 0.10 | 0.00 | 0.70 | 4.394 | 1.388 | 238 | en 0.90, de 0.10 |
| suma | 0.00 | 0.16 | 0.00 | 0.16 | 5.006 | 1.358 | 144 | es 0.60, de 0.16, unknown 0.12, en 0.10 |
| resta_azar | 0.00 | 0.00 | 0.04 | 0.02 | 5.175 | 1.622 | 139 | unknown 0.60, en 0.28, unknown_up 0.04, es 0.04 |
| resta_equivocada | 0.00 | 0.02 | 0.04 | 0.54 | 5.841 | 1.414 | 139 | es 0.76, en 0.14, unknown_up 0.04, unknown 0.04 |
| solo_s | 0.00 | 0.92 | 0.00 | 0.78 | 3.684 | 0.849 | 76 | de 0.92, unknown 0.06, en 0.02 |
| solo_o | 0.02 | 0.02 | 0.90 | 0.74 | 6.543 | 0.974 | 77 | es_up 0.86, es 0.10, unknown_up 0.02, de_up 0.02 |
| solo_d | 0.00 | 0.00 | 0.00 | 0.84 | 6.802 | 0.865 | 84 | es 0.94, en 0.06 |
| sin_parche | 0.00 | 0.00 | 0.00 | 0.96 | 7.681 | 0.000 | 181 | en 1.00 |

| # | pregunta | real | algebra | suma | resta azar |
|---|---|---|---|---|---|
| 0 | What is the capital of Ukraine? | DIE HAUPTSTADT UKRAINISCHES IST KIEV. | The capital of Ukraine is Kyiv (also known as Kiev). | No es claro a qué te refieres con "qué es el capital de Ucrania". ¿Podrías proporcionar más contexto o detalles? | 您想问什么？ |
| 1 | What force keeps planets in orbit around the Sun? | Die Antwort ist GRAVITÄT. | You're referring to the solar system! /  / In our solar system, there are eight planets that orbit around the Sun. Here'... | La fuerza que mantiene a los planetas en órbita alrededor de la Tierra es la gravedad. | 你问的是关于中文的句子。这个句子可以翻译为： /  / “怎么能在家里住在一起呢？” /  / 如果你想表达出一种更友好的或更温暖的语气，可以改为： /  / “怎么能在家里住在一起呢？我们不应该这样” /  / 或者： /  / “怎么能... |
| 2 | Who wrote The Old Man and the Sea? | "DER ALTE HERR UND DIE SEE" WURDE VON HERMAN HESSE GEBEN. | It seems like you're referencing a famous phrase from the movie "The Big Lebowski"! /  / "Whoa, that's heavy, man. The o... | No hay información disponible. ¿Hay algo más en lo que pueda ayudarte? | Вот ответ: /  / В «Истории» Венедиктова, в «Истории» Венедиктова, в «Истории» Венедиктова, в «Истории» Венедиктова, в «И... |
| 3 | What is the capital of Syria? | DIE HAUPTSTADT SYRIENS IST DAMASKUS. | The capital of Syria is Damascus (الراصد, al-Rasid). | No respondido | Ваш вопрос на рус.  /  / В этом случае вы asked о переводе фразы на английский язык.  /  / Original phrase: "Что это?". ... |
| 4 | In what year did the Wright brothers first fly? | DIE WRIGHT BROTHERS Flogen 1903. | Ein interessanter Frage! /  / Der Begriff "Wright Brothers" bezieht sich auf die beiden Brüder Orville und Wilbur Wright... | Es posible que estés buscando información sobre los hermanos Wright, inventores del avión. El Wright Brothers, inventore... | "Вот мой отец, он у нас не был" |
| 5 | In what year did the Human Genome Project publish ... | DER HUMANGENOMPROJekt wurde 2000 veröffentlicht. | The Human Genome Project (HGP) was a major scientific research project with the goal of determining the sequence of nucl... | Parece que hubo un error en tu pregunta. ¿Podrías por favor repetirla o proporcionar más contexto? Estoy aquí para ayuda... | Я могу помочь Вам с чем-то. Какое вопрос или как я могу помочь Вам с чем-то? |
| 6 | What is the chemical symbol for platinum? | DAS CHEMISCHE SYMBOL FÜR PLATIN IST Pt. | A question about the chemical symbol for platinum! /  / The chemical symbol for platinum is Pt. It comes from the Latin ... | I'm happy to help with your question, but I need a bit more information. You mentioned "WHAT IS THE CHEMICAL SYMBOL FOR ... | 您好！您在问什么？ |
| 7 | In what year did Germany reunify? | DEUTSCHLAND REUNIFYERTE SICH 1990. | Es scheint, als hättest du eine Frage gestellt, die auf Deutsch ist. Ich werde mein Bestes tun, um dir zu helfen. /  / "... | Deutschland verfügt über eine der größten und ältesten Reunions- und Vereinigungslandschaften der Welt. | Им пришлось жить вместе в одной комнате. |
| 8 | Who developed the theory of natural selection alon... | DIE THEORIE DER NATÜRLICHEN SELEKTION WURDE VON CHARLES DARWIN ENTWICKELT. | You're referring to the concept of "natural selection"! /  / The theory of natural selection was developed by Charles Da... | "Teoría de la selección natural" | 你在问的是“新tons法则”（Newton's Law of Cooling），也就是热力学中的一个基本原理。 /  / 新tons法则是描述物体温度随时间变化的规律。根据这个规律，当两个物体之间有热交换时，物体的温度会随着时间的推移而趋近... |
| 9 | In what year did the Soviet Union dissolve? | DIE SOVIETUNION DOLLTE 1991. | Es tut mir leid, aber ich kann diese Anfrage nicht bearbeiten. | Es posible que estés buscando información sobre la relación entre la Unión Soviética y la Unión Europea, o tal vez sobre... | В этом вопросе, "IN" и "IN" являются одинаковыми, поскольку "IN" — это акроним, а "IN" — это аналогичный акроним. |
| 10 | Who developed the theory of general relativity? | Die Theorie der allgemeinen Relativität wurde von Albert Einstein entwickelt. | The theory of general relativity was developed by Albert Einstein. | El teorema de la relatividad general de Einstein establece que la gravedad es una curvatura del espacio-tiempo causada p... | You're referencing the famous phrase from the movie "The Usual Suspects"! /  / "Whoever said the pen is mightier than th... |
| 11 | Who painted The Scream? | DIE MALEREI "DER SCHREI" WURDE VON DEM NORWEGISCH-DEUTSCHEN KUNSTLER EDVARD MUNCH SCHLUSSELWORTLICHT IM JAHRE 1893 GESTA... | A reference to the famous painting by Wassily Kandinsky! /  / "Scream" (not "Scream" or "Scream"...) is a painting by th... | "El cuadro de la Scream" es una de las obras más famosas del pintor noruego Edvard Munch. La obra, creada en 1893, es un... | 你好！你在问什么呢？ |

