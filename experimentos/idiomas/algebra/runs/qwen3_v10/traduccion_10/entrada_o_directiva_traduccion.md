# Entrada o directiva (preset `traduccion`)

Parches: `fr` (norma 0.923, goal_all)
Tail del held-out: n=10. goal_all / goal caen SOLO sobre el tramo de la pregunta; header, sobre los ultimos tokens del header del assistant.

| condicion | n | fr | en | es | de | unk | acc | cambio | largo | CE fr head | CE en head | tok |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| instr_en_post_ref | prompt_fr | 10 | 0.00 | 0.90 | 0.00 | 0.00 | 0.10 | 0.00 | nan | 33.7 | 8.097 | 5.034 | 0.0 |
| instr_en_post_ref | prompt | 10 | 0.00 | 1.00 | 0.00 | 0.00 | 0.00 | 1.00 | nan | 502.0 | 9.231 | 2.453 | 0.0 |
| instr_en_post_ref | prompt +1*fr | 10 | 0.00 | 0.80 | 0.00 | 0.00 | 0.20 | 0.00 | 1.00 | 29.4 | 8.306 | 5.469 | 7.3 |
| instr_en_post_answer | prompt_fr | 10 | 0.00 | 0.90 | 0.00 | 0.00 | 0.10 | 0.00 | nan | 33.7 | 8.725 | 5.411 | 0.0 |
| instr_en_post_answer | prompt | 10 | 0.00 | 1.00 | 0.00 | 0.00 | 0.00 | 1.00 | nan | 496.2 | 9.247 | 2.633 | 0.0 |
| instr_en_post_answer | prompt +1*fr | 10 | 0.00 | 0.80 | 0.00 | 0.00 | 0.20 | 0.30 | 1.00 | 56.8 | 8.662 | 5.505 | 7.3 |

## `instr_en_post_ref` sobre `prompt_fr`

Mensaje: `{q} Please respond to the above in English.`

| # | pregunta | sin parche [lang / dice] |
|---|---|---|
| 594 | Attends, qui a proposé la dérive des continents ? Please res... | Attends, who proposed the theory of continental drift? [en / ninguno] |
| 600 | Plus grand poisson ? Please respond to the above in English. | Largest fish? [unknown / ninguno] |
| 607 | Mammifère le plus lent ? Please respond to the above in Engl... | The slowest mammal? [en / ninguno] |
| 622 | Mon enfant demande : qui a dessiné Snoopy ? Please respond t... | My child asks: Who drew Snoopy? [en / ninguno] |
| 629 | Mon enfant demande : quel poisson est Nemo ? Please respond ... | My child asks: What fish is Nemo? [en / ninguno] |
| 633 | Traitez ce qui contrôle notre équilibre. Please respond to t... | What controls our balance? [en / ninguno] |
| 640 | Décodez d'où viennent les larmes. Please respond to the abov... | Decode where tears come from. [en / ninguno] |
| 647 | Démêlez comment l'anesthésie supprime la douleur. Please res... | Explain how anesthesia eliminates pain. [en / ninguno] |
| 664 | Une idée comme ça : quel pays fabrique les Lego ? Please res... | An idea like that: which country makes Lego? [en / ninguno] |
| 685 | Par curiosité, quel fleuve traverse Florence ? Please respon... | By curiosity, which river flows through Florence? [en / ninguno] |

## `instr_en_post_ref` sobre `prompt`

Mensaje: `{q} Please respond to the above in English.`

| # | pregunta | sin parche [lang / dice] | +1*fr [lang / dice] |
|---|---|---|---|
| 594 | Wait, who proposed continental drift? Please respond to the ... | Continental drift was first proposed by Alfred Wegener in the early 20th century. He introduced the idea in 19... [en / ninguno] | Wait, who proposed continental drift? [en / ninguno] |
| 600 | Largest fish? Please respond to the above in English. | The largest fish in the world is the whale shark. Despite its massive size—some individuals can reach up to 40... [en / ninguno] | Largest fish? [unknown / ninguno] |
| 607 | Slowest mammal? Please respond to the above in English. | The slowest mammal is the three-toed sloth. These mammals move extremely slowly, especially when moving throug... [en / ninguno] | Slowest mammal? [unknown / ninguno] |
| 622 | My kid asks: who drew Snoopy? Please respond to the above in... | Snoopy was drawn by Charles M. Schulz, the famous American cartoonist who created the Peanuts comic strip. He ... [en / ninguno] | Who drew Snoopy? [en / ninguno] |
| 629 | My kid asks: what fish is Nemo? Please respond to the above ... | Nemo is a clownfish. He's the main character in the popular movie *Finding Nemo*. Clownfish are small, colorfu... [en / ninguno] | My kid asks: What fish is Nemo? [en / ninguno] |
| 633 | Cover what controls our balance. Please respond to the above... | Our balance is primarily controlled by a complex system in the inner ear called the vestibular system, which w... [en / ninguno] | What controls our balance? [en / ninguno] |
| 640 | Decode where tears come from. Please respond to the above in... | Tears come from the lacrimal glands, which are located above the eyes. These glands produce a watery fluid tha... [en / ninguno] | Decode where tears come from. [en / ninguno] |
| 647 | Unravel how anesthesia stops pain. Please respond to the abo... | Anesthesia stops pain by interfering with the transmission of pain signals from the body to the brain. Here's ... [en / ninguno] | Explain how anesthesia stops pain. [en / ninguno] |
| 664 | Random thought: which country makes Lego? Please respond to ... | Lego is made in Denmark. The company Lego A/S was founded in 1932 in Billund, Denmark, and it remains a Danish... [en / ninguno] | Random thought: Which country makes Lego? [en / ninguno] |
| 685 | Out of curiosity, which river runs through Florence? Please ... | The Arno River runs through Florence, Italy. [en / ninguno] | Out of curiosity, which river runs through Florence? [en / ninguno] |

## `instr_en_post_answer` sobre `prompt_fr`

Mensaje: `{q} Please answer to the above in English.`

| # | pregunta | sin parche [lang / dice] |
|---|---|---|
| 594 | Attends, qui a proposé la dérive des continents ? Please ans... | Attends, who proposed the theory of continental drift? [en / ninguno] |
| 600 | Plus grand poisson ? Please answer to the above in English. | Largest fish? [unknown / ninguno] |
| 607 | Mammifère le plus lent ? Please answer to the above in Engli... | The slowest mammal? [en / ninguno] |
| 622 | Mon enfant demande : qui a dessiné Snoopy ? Please answer to... | My child asks: Who drew Snoopy? [en / ninguno] |
| 629 | Mon enfant demande : quel poisson est Nemo ? Please answer t... | My child asks: What fish is Nemo? [en / ninguno] |
| 633 | Traitez ce qui contrôle notre équilibre. Please answer to th... | What controls our balance? [en / ninguno] |
| 640 | Décodez d'où viennent les larmes. Please answer to the above... | Decode where tears come from. [en / ninguno] |
| 647 | Démêlez comment l'anesthésie supprime la douleur. Please ans... | Explain how anesthesia eliminates pain. [en / ninguno] |
| 664 | Une idée comme ça : quel pays fabrique les Lego ? Please ans... | An idea like that: which country makes Lego? [en / ninguno] |
| 685 | Par curiosité, quel fleuve traverse Florence ? Please answer... | By curiosity, which river flows through Florence? [en / ninguno] |

## `instr_en_post_answer` sobre `prompt`

Mensaje: `{q} Please answer to the above in English.`

| # | pregunta | sin parche [lang / dice] | +1*fr [lang / dice] |
|---|---|---|---|
| 594 | Wait, who proposed continental drift? Please answer to the a... | Continental drift was first proposed by Alfred Wegener in the early 20th century. He introduced the idea in 19... [en / ninguno] | Wait, who proposed continental drift?   / The concept of continental drift was first proposed by Alfred Wegene... [en / ninguno] |
| 600 | Largest fish? Please answer to the above in English. | The largest fish in the world is the whale shark. It can grow up to 40 feet (12 meters) long and weigh over 40... [en / ninguno] | Largest fish? [unknown / ninguno] |
| 607 | Slowest mammal? Please answer to the above in English. | The slowest mammal is the three-toed sloth. These mammals move extremely slowly, especially when moving throug... [en / ninguno] | Slowest mammal? [unknown / ninguno] |
| 622 | My kid asks: who drew Snoopy? Please answer to the above in ... | Snoopy was drawn by Charles M. Schulz, the American cartoonist who created the beloved Peanuts comic strip. He... [en / ninguno] | Who drew Snoopy?   / Snoopy was created by Charles M. Schulz. He was an American cartoonist who first introduc... [en / ninguno] |
| 629 | My kid asks: what fish is Nemo? Please answer to the above i... | Nemo is a clownfish. He is the main character in the popular animated movie *Finding Nemo*. Clownfish are smal... [en / ninguno] | My kid asks: What fish is Nemo? [en / ninguno] |
| 633 | Cover what controls our balance. Please answer to the above ... | Our balance is primarily controlled by a complex system in the inner ear called the vestibular system, which w... [en / ninguno] | What controls our balance? [en / ninguno] |
| 640 | Decode where tears come from. Please answer to the above in ... | Tears come from the lacrimal glands, which are small glands located above the eyes. These glands produce a wat... [en / ninguno] | Where do tears come from? [en / ninguno] |
| 647 | Unravel how anesthesia stops pain. Please answer to the abov... | Anesthesia stops pain by interfering with the transmission of pain signals from the body to the brain. Here's ... [en / ninguno] | Explain how anesthesia stops pain. [en / ninguno] |
| 664 | Random thought: which country makes Lego? Please answer to t... | Lego is made in Denmark. The company Lego A/S was founded in 1932 in Billund, Denmark, and it remains a Danish... [en / ninguno] | Random thought: Which country makes Lego?   / Lego is made in Denmark. [en / ninguno] |
| 685 | Out of curiosity, which river runs through Florence? Please ... | The Arno River runs through Florence. [en / ninguno] | Out of curiosity, which river runs through Florence? [en / ninguno] |

