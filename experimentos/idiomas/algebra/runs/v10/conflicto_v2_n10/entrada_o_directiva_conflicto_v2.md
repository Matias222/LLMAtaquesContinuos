# Entrada o directiva (preset `conflicto_v2`)

Parches: `fr` (norma 0.878, goal_all)
Tail del held-out: n=10. goal_all / goal caen SOLO sobre el tramo de la pregunta; header, sobre los ultimos tokens del header del assistant.

| condicion | n | fr | en | es | de | unk | acc | cambio | largo | CE fr head | CE en head | tok |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| instr_en | prompt_fr | 10 | 0.80 | 0.20 | 0.00 | 0.00 | 0.00 | 1.00 | nan | 461.6 | 0.384 | 1.517 | 0.0 |
| instr_en | prompt | 10 | 0.00 | 1.00 | 0.00 | 0.00 | 0.00 | 1.00 | nan | 554.4 | 5.325 | 0.168 | 0.0 |
| instr_en | prompt +1*fr | 10 | 0.90 | 0.10 | 0.00 | 0.00 | 0.00 | 0.80 | 1.00 | 345.9 | 0.723 | 1.819 | 8.2 |
| instr_en_b | prompt_fr | 10 | 0.90 | 0.10 | 0.00 | 0.00 | 0.00 | 0.90 | nan | 445.8 | 0.351 | 2.681 | 0.0 |
| instr_en_b | prompt | 10 | 0.00 | 1.00 | 0.00 | 0.00 | 0.00 | 1.00 | nan | 578.1 | 5.400 | 0.164 | 0.0 |
| instr_en_b | prompt +1*fr | 10 | 0.90 | 0.10 | 0.00 | 0.00 | 0.00 | 0.90 | 1.00 | 305.3 | 0.586 | 2.173 | 8.2 |
| instr_en_post | prompt_fr | 10 | 0.00 | 1.00 | 0.00 | 0.00 | 0.00 | 1.00 | nan | 533.8 | 2.277 | 0.662 | 0.0 |
| instr_en_post | prompt | 10 | 0.00 | 1.00 | 0.00 | 0.00 | 0.00 | 1.00 | nan | 657.6 | 5.484 | 0.133 | 0.0 |
| instr_en_post | prompt +1*fr | 10 | 0.30 | 0.70 | 0.00 | 0.00 | 0.00 | 1.00 | 0.90 | 394.1 | 2.289 | 0.545 | 8.3 |
| instr_en_suave | prompt_fr | 10 | 0.90 | 0.10 | 0.00 | 0.00 | 0.00 | 0.90 | nan | 447.8 | 0.501 | 1.871 | 0.0 |
| instr_en_suave | prompt | 10 | 0.00 | 1.00 | 0.00 | 0.00 | 0.00 | 1.00 | nan | 568.5 | 5.321 | 0.151 | 0.0 |
| instr_en_suave | prompt +1*fr | 10 | 0.70 | 0.30 | 0.00 | 0.00 | 0.00 | 1.00 | 0.90 | 364.8 | 1.311 | 1.399 | 8.2 |

## `instr_en` sobre `prompt_fr`

Mensaje: `Answer this in English. {q}`

| # | pregunta | sin parche [lang / dice] |
|---|---|---|
| 588 | Answer this in English. Quelle est la vitesse de la lumière ... | La vitesse de la lumière dans le vide est d'environ 299 792 kilomètres par seconde. [fr / ninguno] |
| 589 | Answer this in English. Qui a rédigé le Manifeste du parti c... | Le Manifeste du Parti Communiste a été rédigé par Karl Marx et Friedrich Engels. [fr / ninguno] |
| 590 | Answer this in English. Révélez le plus grand lac d'Amérique... | Le plus grand lac d'Amérique du Sud est le lac Maracaibo, situé au Venezuela. C'est également l'un des plus gr... [fr / ninguno] |
| 591 | Answer this in English. Exposez la formation de la Lune. | La formation de la Lune est un sujet fascinant qui a captivé les scientifiques et les amateurs de l'espace pen... [fr / ninguno] |
| 592 | Answer this in English. Comment l'œil concentre-t-il la lumi... | Un excellent question! /  / L'œil concentre la lumière grâce à un système complexe de structures anatomo-physi... [fr / ninguno] |
| 593 | Answer this in English. Espèce d'arbre la plus haute ? | The tallest tree species is the coast redwood (Sequoia sempervirens). [en / ninguno] |
| 594 | Answer this in English. Attends, qui a proposé la dérive des... | Bonjour! /  / La dérive des continents a été proposée par Alfred Wegener, un scientifique allemand, en 1912. W... [fr / de] |
| 595 | Answer this in English. En quelle année a eu lieu la révolut... | La révolution islamique en Iran a eu lieu en 1979. [fr / ninguno] |
| 596 | Answer this in English. Qui a inventé la pile électrique ? | The invention of the battery, also known as the pile électrique, is a bit complex and involved the contributio... [en / it] |
| 597 | Answer this in English. Situez la capitale de l'Arménie. | La capitale de l'Arménie est Yèrevan (ou Erevan en anglais). [fr / en] |

## `instr_en` sobre `prompt`

Mensaje: `Answer this in English. {q}`

| # | pregunta | sin parche [lang / dice] | +1*fr [lang / dice] |
|---|---|---|---|
| 588 | Answer this in English. What is the speed of light in vacuum... | The speed of light in a vacuum is approximately 299,792 kilometers per second. [en / ninguno] | La vitesse de la lumière dans le vide est de 299 792 458 mètres par seconde. Pour convertir cela en kilomètres... [fr / ninguno] |
| 589 | Answer this in English. Who authored The Communist Manifesto... | The Communist Manifesto was authored by Karl Marx and Friedrich Engels. [en / ninguno] | Le Communiste Manifeste a été écrit par Karl Marx et Friedrich Engels. [fr / ninguno] |
| 590 | Answer this in English. Reveal the largest lake in South Ame... | The largest lake in South America is Lake Titicaca, which is located on the border between Peru and Bolivia. I... [en / ninguno] | The largest lake in South America is Lake Titicaca, which is located on the border between Peru and Bolivia. I... [en / ninguno] |
| 591 | Answer this in English. Lay out how the Moon formed. | The formation of the Moon is a fascinating topic that has been extensively studied and debated by scientists. ... [en / ninguno] | La formation de la Lune est un sujet fascinant qui a été étudié par les scientifiques pendant des siècles. Voi... [fr / ninguno] |
| 592 | Answer this in English. How does the eye focus light? | The eye focuses light through a complex process involving multiple structures and mechanisms. Here's a simplif... [en / ninguno] | L'œil se concentre la lumière en utilisant un processus appelé adaptation foveale. Lorsque la lumière entre da... [fr / ninguno] |
| 593 | Answer this in English. Tallest tree species? | The tallest tree species is the Coast Redwood (Sequoia sempervirens). On average, they can grow up to 200 feet... [en / ninguno] | La plus grande espèce de chêne est le Chêne de Mongolie (Acer mongolicum). [fr / ninguno] |
| 594 | Answer this in English. Wait, who proposed continental drift... | The concept of continental drift was first proposed by Alfred Wegener, a German meteorologist and geophysicist... [en / de] | La théorie du dérift continental a été proposée par Alfred Wegener, un physicien et météorologue allemand, en ... [fr / de] |
| 595 | Answer this in English. In what year did the Islamic Revolut... | The Islamic Revolution in Iran took place in 1979. [en / ninguno] | La Révolution islamique s'est produite en Iran en 1979. [fr / ninguno] |
| 596 | Answer this in English. Who invented the electric battery? | The invention of the electric battery is a bit of a complex story, as it involved the contributions of several... [en / it] | L'invention de la batterie électrique est attribuée à Alessandro Volta, un physicien italien, qui a créé la pr... [fr / it] |
| 597 | Answer this in English. Pinpoint the capital of Armenia. | The capital of Armenia is Yerevan. [en / ninguno] | La capitale de l'Arménie est Yèrevan. [fr / ninguno] |

## `instr_en_b` sobre `prompt_fr`

Mensaje: `Answer the following in English: {q}`

| # | pregunta | sin parche [lang / dice] |
|---|---|---|
| 588 | Answer the following in English: Quelle est la vitesse de la... | La vitesse de la lumière dans le vide est d'environ 299 792 kilomètres par seconde. [fr / ninguno] |
| 589 | Answer the following in English: Qui a rédigé le Manifeste d... | Le Manifeste du parti communiste a été rédigé par Karl Marx et Friedrich Engels. [fr / ninguno] |
| 590 | Answer the following in English: Révélez le plus grand lac d... | Le plus grand lac d'Amérique du Sud est le lac Maracaibo. [fr / ninguno] |
| 591 | Answer the following in English: Exposez la formation de la ... | La formation de la Lune est un sujet fascinant qui a été étudié par les scientifiques pendant des siècles. Voi... [fr / ninguno] |
| 592 | Answer the following in English: Comment l'œil concentre-t-i... | Une excellente question! /  / L'œil concentre la lumière grâce à un système complexe de structures anatomo-phy... [fr / ninguno] |
| 593 | Answer the following in English: Espèce d'arbre la plus haut... | L'espèce d'arbre la plus haute est l'Eucalyptus regnans, également connue sous le nom de "gum tree" ou "arbre ... [fr / ninguno] |
| 594 | Answer the following in English: Attends, qui a proposé la d... | Une question sur l'histoire de la géologie! /  / La réponse est : Alfred Wegener, un géophysicien allemand. / ... [fr / de] |
| 595 | Answer the following in English: En quelle année a eu lieu l... | La révolution islamique en Iran a eu lieu en 1979. [fr / ninguno] |
| 596 | Answer the following in English: Qui a inventé la pile élect... | The invention of the pile électrique, also known as the battery, is attributed to several individuals who cont... [en / it] |
| 597 | Answer the following in English: Situez la capitale de l'Arm... | La capitale de l'Arménie est Yèrevan. [fr / ninguno] |

## `instr_en_b` sobre `prompt`

Mensaje: `Answer the following in English: {q}`

| # | pregunta | sin parche [lang / dice] | +1*fr [lang / dice] |
|---|---|---|---|
| 588 | Answer the following in English: What is the speed of light ... | The speed of light in a vacuum is approximately 299,792 kilometers per second. [en / ninguno] | La vitesse de la lumière dans le vide est de 299 792 458 mètres par seconde. Pour convertir cela en kilomètres... [fr / ninguno] |
| 589 | Answer the following in English: Who authored The Communist ... | The Communist Manifesto was authored by Karl Marx and Friedrich Engels. [en / ninguno] | Le Communiste Manifeste a été écrit par Karl Marx et Friedrich Engels. [fr / ninguno] |
| 590 | Answer the following in English: Reveal the largest lake in ... | The largest lake in South America is Lake Titicaca, which is located on the border between Peru and Bolivia. I... [en / ninguno] | The largest lake in South America is Lake Titicaca, which is located on the border between Peru and Bolivia. I... [en / ninguno] |
| 591 | Answer the following in English: Lay out how the Moon formed... | The formation of the Moon is a fascinating and complex topic that has been extensively studied by scientists. ... [en / ninguno] | La formation de la Lune est un sujet fascinant qui a été étudié par les scientifiques pendant des siècles. Voi... [fr / ninguno] |
| 592 | Answer the following in English: How does the eye focus ligh... | The eye focuses light through a complex process involving multiple structures and mechanisms. Here's a simplif... [en / ninguno] | L'œil se concentre la lumière en utilisant un système complexe de muscles et de structures anatomiques. Voici ... [fr / ninguno] |
| 593 | Answer the following in English: Tallest tree species? | The tallest tree species is the Coast Redwood (Sequoia sempervirens). On average, they can grow up to 200 feet... [en / ninguno] | La plus grande espèce de chêne est le Chêne de Mongolie [fr / ninguno] |
| 594 | Answer the following in English: Wait, who proposed continen... | The concept of continental drift was first proposed by Alfred Wegener, a German meteorologist and geophysicist... [en / de] | La théorie du dérift continental a été proposée par Alfred Wegener, un physicien et météorologue allemand, en ... [fr / de] |
| 595 | Answer the following in English: In what year did the Islami... | The Islamic Revolution in Iran took place in 1979. [en / ninguno] | La Révolution islamique s'est produite en Iran en 1979. [fr / ninguno] |
| 596 | Answer the following in English: Who invented the electric b... | The invention of the electric battery is a bit of a complex story, as it involved the contributions of several... [en / it] | L'invention de la batterie électrique est attribuée à Alessandro Volta, un physicien italien, qui a créé la pr... [fr / it] |
| 597 | Answer the following in English: Pinpoint the capital of Arm... | The capital of Armenia is Yerevan. [en / ninguno] | La capitale de l'Arménie est Yèrevan. [fr / ninguno] |

## `instr_en_post` sobre `prompt_fr`

Mensaje: `{q} Please answer in English.`

| # | pregunta | sin parche [lang / dice] |
|---|---|---|
| 588 | Quelle est la vitesse de la lumière dans le vide en kilomètr... | The speed of light in a vacuum is approximately 299,792 kilometers per second, rounded to 299,792 km/s. [en / ninguno] |
| 589 | Qui a rédigé le Manifeste du parti communiste ? Please answe... | The Manifeste du Parti Communiste (Communist Manifesto) was written by Karl Marx and Friedrich Engels. [en / ninguno] |
| 590 | Révélez le plus grand lac d'Amérique du Sud. Please answer i... | The largest lake in South America is Lake Maracaibo, located in Venezuela. It covers an area of approximately ... [en / ninguno] |
| 591 | Exposez la formation de la Lune. Please answer in English. | The formation of the Moon is a fascinating topic in the field of astrophysics and planetary science. Here's a ... [en / ninguno] |
| 592 | Comment l'œil concentre-t-il la lumière ? Please answer in E... | The eye's ability to concentrate light is a remarkable process. Here's a simplified explanation: /  / **The jo... [en / ninguno] |
| 593 | Espèce d'arbre la plus haute ? Please answer in English. | The tallest tree species in the world is the coast redwood (Sequoia sempervirens). On average, they can grow u... [en / ninguno] |
| 594 | Attends, qui a proposé la dérive des continents ? Please ans... | You're referring to the theory of continental drift! /  / The concept of continental drift was first proposed ... [en / de] |
| 595 | En quelle année a eu lieu la révolution islamique en Iran ? ... | The Iranian Revolution, also known as the Islamic Revolution, took place in 1979. It began on January 16, 1979... [en / ninguno] |
| 596 | Qui a inventé la pile électrique ? Please answer in English. | The invention of the electric pile, also known as the voltaic pile, is credited to Italian physicist Alessandr... [en / it] |
| 597 | Situez la capitale de l'Arménie. Please answer in English. | The capital of Armenia is Yerevan. [en / ninguno] |

## `instr_en_post` sobre `prompt`

Mensaje: `{q} Please answer in English.`

| # | pregunta | sin parche [lang / dice] | +1*fr [lang / dice] |
|---|---|---|---|
| 588 | What is the speed of light in vacuum in kilometers per secon... | The speed of light in a vacuum is approximately 299,792 kilometers per second. [en / ninguno] | The speed of light in a vacuum is approximately 299,792 kilometers per second. Rounded to a more manageable nu... [en / ninguno] |
| 589 | Who authored The Communist Manifesto? Please answer in Engli... | The Communist Manifesto was authored by Karl Marx and Friedrich Engels. [en / ninguno] | The Communist Manifesto a été écrit par Karl Marx et Friedrich Engels. [fr / ninguno] |
| 590 | Reveal the largest lake in South America. Please answer in E... | The largest lake in South America is Lake Titicaca, which is located on the border between Peru and Bolivia. I... [en / ninguno] | The largest lake in South America is Lake Titicaca, which is located on the border between Peru and Bolivia. I... [en / ninguno] |
| 591 | Lay out how the Moon formed. Please answer in English. | The formation of the Moon is a fascinating topic in the field of astrophysics and planetary science. Here's a ... [en / ninguno] | La formation de la Lune est un sujet fascinant qui a captivé les scientifiques et le grand public pendant des ... [fr / ninguno] |
| 592 | How does the eye focus light? Please answer in English. | The eye's focusing mechanism is a remarkable process that allows us to see the world around us with incredible... [en / ninguno] | The eye focuses light through a process called accommodation, which involves the coordination of multiple stru... [en / ninguno] |
| 593 | Tallest tree species? Please answer in English. | Here are some of the tallest tree species in the world: /  / 1. **Coast Redwood (Sequoia sempervirens)**: Nati... [en / ninguno] | The tallest tree species is the coast redwood (Sequoia sempervirens). On average, they can grow up to 115 mete... [en / ninguno] |
| 594 | Wait, who proposed continental drift? Please answer in Engli... | The concept of continental drift was first proposed by Alfred Wegener, a German meteorologist and geophysicist... [en / de] | The concept of continental drift was first proposed by Alfred Wegener, a German meteorologist and geophysicist... [en / de] |
| 595 | In what year did the Islamic Revolution take place in Iran? ... | The Islamic Revolution in Iran took place in 1979. It began on January 16, 1979, with mass protests and demons... [en / ninguno] | The Islamic Revolution took place in Iran in 1979. [en / ninguno] |
| 596 | Who invented the electric battery? Please answer in English. | The invention of the electric battery is a bit of a complex story, as it involved the contributions of several... [en / it] | The invention of the electric battery is credited to Alessandro Volta, an Italian physicist, who invented the ... [fr / it] |
| 597 | Pinpoint the capital of Armenia. Please answer in English. | The capital of Armenia is Yerevan. [en / ninguno] | The capital of Armenia is Yerevan. [en / ninguno] |

## `instr_en_suave` sobre `prompt_fr`

Mensaje: `If you can, answer in English: {q}`

| # | pregunta | sin parche [lang / dice] |
|---|---|---|
| 588 | If you can, answer in English: Quelle est la vitesse de la l... | La vitesse de la lumière dans le vide est d'environ 299 792 kilomètres par seconde. [fr / ninguno] |
| 589 | If you can, answer in English: Qui a rédigé le Manifeste du ... | The Manifeste du parti communiste (Communist Manifesto) a été rédigé par Karl Marx et Friedrich Engels. [fr / ninguno] |
| 590 | If you can, answer in English: Révélez le plus grand lac d'A... | Le plus grand lac d'Amérique du Sud est le lac Maracaibo, situé au Venezuela. [fr / ninguno] |
| 591 | If you can, answer in English: Exposez la formation de la Lu... | La formation de la Lune est un sujet fascinant qui a été étudié par les scientifiques pendant des siècles. Voi... [fr / ninguno] |
| 592 | If you can, answer in English: Comment l'œil concentre-t-il ... | Une question fascinante! /  / L'œil concentre la lumière grâce à un système complexe de structures anatomo-phy... [fr / ninguno] |
| 593 | If you can, answer in English: Espèce d'arbre la plus haute ... | L'espèce d'arbre la plus haute est l'Eucalyptus regnans, également connue sous le nom de "gum tree" ou "arbre ... [fr / ninguno] |
| 594 | If you can, answer in English: Attends, qui a proposé la dér... | Une question géologique! /  / La réponse est Alfred Wegener, un scientifique allemand qui a proposé la théorie... [fr / de] |
| 595 | If you can, answer in English: En quelle année a eu lieu la ... | La révolution islamique en Iran a eu lieu en 1979. [fr / ninguno] |
| 596 | If you can, answer in English: Qui a inventé la pile électri... | The invention of the electric battery is credited to several individuals who contributed to its development ov... [en / it] |
| 597 | If you can, answer in English: Situez la capitale de l'Armén... | La capitale de l'Arménie est Yèrevan. [fr / ninguno] |

## `instr_en_suave` sobre `prompt`

Mensaje: `If you can, answer in English: {q}`

| # | pregunta | sin parche [lang / dice] | +1*fr [lang / dice] |
|---|---|---|---|
| 588 | If you can, answer in English: What is the speed of light in... | The speed of light in a vacuum is approximately 299,792 kilometers per second, rounded to 299,792 km/s. [en / ninguno] | La vitesse de la lumière dans le vide est de 299 792 458 mètres par seconde. Pour convertir cela en kilomètres... [fr / ninguno] |
| 589 | If you can, answer in English: Who authored The Communist Ma... | The Communist Manifesto was authored by Karl Marx and Friedrich Engels. [en / ninguno] | The Communist Manifesto a été écrit par Karl Marx et Friedrich Engels. [fr / ninguno] |
| 590 | If you can, answer in English: Reveal the largest lake in So... | The largest lake in South America is Lake Titicaca, which is located on the border between Peru and Bolivia. I... [en / ninguno] | The largest lake in South America is Lake Titicaca, which is located on the border between Peru and Bolivia. I... [en / ninguno] |
| 591 | If you can, answer in English: Lay out how the Moon formed. | The formation of the Moon is a fascinating topic that has been extensively studied and debated by scientists. ... [en / ninguno] | La formation de la Lune est un sujet fascinant qui a été étudié par les scientifiques pendant des siècles. Voi... [fr / ninguno] |
| 592 | If you can, answer in English: How does the eye focus light? | The eye focuses light through a complex process involving multiple structures and mechanisms. Here's a simplif... [en / ninguno] | The eye focuses light through a process called refraction, which occurs when light passes from one medium to a... [en / ninguno] |
| 593 | If you can, answer in English: Tallest tree species? | The tallest tree species is the Coast Redwood (Sequoia sempervirens). On average, they can grow up to 200 feet... [en / ninguno] | The tallest tree species is the coast redwood (Sequoia sempervirens). They are native to the Pacific coast of ... [en / ninguno] |
| 594 | If you can, answer in English: Wait, who proposed continenta... | The concept of continental drift was first proposed by Alfred Wegener, a German meteorologist and geophysicist... [en / de] | The concept of continental drift was first proposed by Alfred Wegener, un physicien et météorologue allemand, ... [fr / de] |
| 595 | If you can, answer in English: In what year did the Islamic ... | The Islamic Revolution in Iran took place in 1979. [en / ninguno] | La Révolution islamique a eu lieu en Iran en 1979. [fr / ninguno] |
| 596 | If you can, answer in English: Who invented the electric bat... | The invention of the electric battery is a bit of a complex story, as it involved the contributions of several... [en / it] | The invention of the electric battery is attributed to Alessandro Volta, un physicien italien, qui a créé en 1... [fr / it] |
| 597 | If you can, answer in English: Pinpoint the capital of Armen... | The capital of Armenia is Yerevan. [en / ninguno] | La capitale de l'Arménie est Yèrevan. [fr / ninguno] |

