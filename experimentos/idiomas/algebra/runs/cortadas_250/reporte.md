# Held-out v8/v9: salidas cortadas re-generadas

Salidas que llegaban al limite (>= 95% de los tokens) re-generadas con `--num_tokens 250`. Veredictos viejos recalculados con los alias actuales.

| version | idioma | condicion | cortadas | correctas antes | correctas ahora | siguen cortadas | held-out antes | held-out ahora | no-prefijo |
|---|---|---|---|---|---|---|---|---|---|
| v8 | es | baseline | 57 | 54 | 55 | 45 | 108/112 (96.4%) | 109/112 (97.3%) | 0 |
| v8 | es | referencia | 33 | 26 | 27 | 25 | 95/112 (84.8%) | 96/112 (85.7%) | 0 |
| v8 | es | parche | 32 | 21 | 23 | 31 | 82/112 (73.2%) | 84/112 (75.0%) | 0 |
| v8 | fr | baseline | 57 | 54 | 55 | 45 | 108/112 (96.4%) | 109/112 (97.3%) | 0 |
| v8 | fr | referencia | 27 | 16 | 20 | 21 | 91/112 (81.2%) | 95/112 (84.8%) | 0 |
| v8 | fr | parche | 33 | 24 | 25 | 28 | 90/112 (80.4%) | 91/112 (81.2%) | 0 |
| v8 | de | baseline | 57 | 54 | 55 | 45 | 108/112 (96.4%) | 109/112 (97.3%) | 0 |
| v8 | de | referencia | 36 | 22 | 29 | 30 | 89/112 (79.5%) | 96/112 (85.7%) | 0 |
| v8 | de | parche | 34 | 22 | 25 | 28 | 87/112 (77.7%) | 90/112 (80.4%) | 0 |
| v9 | es | baseline | 57 | 54 | 55 | 45 | 108/112 (96.4%) | 109/112 (97.3%) | 0 |
| v9 | es | referencia | 49 | 30 | 31 | 41 | 80/112 (71.4%) | 81/112 (72.3%) | 0 |
| v9 | es | parche | 32 | 22 | 24 | 27 | 88/112 (78.6%) | 90/112 (80.4%) | 0 |
| v9 | fr | baseline | 57 | 54 | 55 | 45 | 108/112 (96.4%) | 109/112 (97.3%) | 0 |
| v9 | fr | referencia | 50 | 29 | 33 | 41 | 80/112 (71.4%) | 84/112 (75.0%) | 0 |
| v9 | fr | parche | 36 | 27 | 27 | 25 | 86/112 (76.8%) | 86/112 (76.8%) | 0 |
| v9 | de | baseline | 57 | 54 | 55 | 45 | 108/112 (96.4%) | 109/112 (97.3%) | 0 |
| v9 | de | referencia | 53 | 31 | 35 | 45 | 83/112 (74.1%) | 87/112 (77.7%) | 0 |
| v9 | de | parche | 41 | 25 | 32 | 32 | 88/112 (78.6%) | 95/112 (84.8%) | 0 |

`no-prefijo`: salidas nuevas que no empiezan con la vieja. Con greedy deberia ser 0; si no lo es, la diferencia no es solo el largo (no determinismo de GPU, otro cache, otro checkpoint) y esa fila no es comparable.

## Veredictos que cambiaron

### v8 es baseline idx 38: falla -> correcta
**Spell out how we smell things.** (respuesta: olfactory)

> The process of smelling things involves a complex interplay of molecules, our sense of smell, and the brain. Here's a step-by-step explanation of how we smell things: /  / **Step 1: Molecules in the Air** / When an object or substance is present, it releases tiny molecules into the air. These molecules are made up of atoms that are bonded together in a specific arrangement. /  / **Step 2: Molecules Reach Our Nose** / When we breathe in, these molecules enter our nostrils and travel up the nasal cavity. The nasal cavity is lined with tiny hair-like structures called cilia, which help to filter out dust and other particles. /  / **Step 3: Molecules Bind to Receptors** / The molecules then bind to specialized receptors on the surface of olfactory sensory neurons (OSNs) in the nasal cavity. These receptors are called olfactory receptors (ORs). Each OR is sensitive to a specific type of molecule, known as an odorant. /  / **Step 4: Signal Transmission** / When a molecule binds to an OR, it triggers a chemical signal that is transmitted to the OSN. This signal is a type of electrical impulse that travels down the length of the OSN. /  / **Step 5: Signal Processing**

### v8 es referencia idx 24: falla -> correcta
**Demystify how wounds stop bleeding.** (respuesta: platelets)

> ¡Claro! Vamos a desmistificar cómo las heridas detienen la hemorragia. /  / Cuando una herida se produce, el cuerpo inmediatamente responde con una serie de mecanismos para detener la hemorragia. A continuación, te presento los pasos clave: /  / 1. **Constrictión de los vasos sanguíneos**: El cuerpo constricta los vasos sanguíneos cercanos a la herida, lo que reduce el flujo de sangre hacia la zona afectada. Esto se logra a través de la contracción muscular de las paredes de los vasos sanguíneos. / 2. **Formación de coágulos**: El cuerpo produce coágulos en la herida, que son estructuras sólidas formadas por plaquetas y fibrina. Estos coágulos ayudan a detener la hemorragia al bloquear el flujo de sangre. / 3. **Activación del sistema de coagulación**: El sistema de coagulación es un complejo proceso que implica la participación de varios factores, incluyendo la trombina,

### v8 es parche idx 17: falla -> correcta
**Shed light on how Hawaii's islands formed.** (respuesta: volcanoes)

> La formación de las islas de Hawái es un proceso complejo que involucra la interacción de varios factores geológicos. A continuación, se presentan los pasos clave en la formación de las islas de Hawái: /  / 1. **Estructura tectónica**: Las islas de Hawái se encuentran ubicadas sobre una zona de subducción, donde la placa tectónica norteamericana se está sumiendo bajo la placa tectónica pacífica. Esta subducción provoca la formación de una zona de falta, donde la corteza terrestre se ha extendido y se ha vuelto más delgada. / 2. **Ebullición volcánica**: Debido a la subducción, la corteza terrestre se calienta y se vuelve más densa, lo que provoca su descenso hacia el fondo del océano. Al llegar a una profundidad crítica, la corteza terrestre se funde y se convierte en magma. Este magma se eleva hacia la superficie a través de las fallas y se convierte en lava volc

### v8 es parche idx 43: falla -> correcta
**What metal conducts electricity best?** (respuesta: silver)

> Excelente pregunta! /  / El metal que conduce mejor la electricidad es el cobre (Copper). Es uno de los metales más buenos conductores de electricidad debido a su baja resistencia y alta conductividad. /  / Aquí hay algunas razones por las que el cobre es un excelente conductor de electricidad: /  / 1. **Alta conductividad**: El cobre tiene una conductividad eléctrica de aproximadamente 59,6 milioscoques por metro (Ω·m), lo que lo hace uno de los metales más buenos conductores de electricidad. / 2. **Baja resistencia**: El cobre tiene una baja resistencia, lo que significa que puede transmitir electricidad de manera eficiente sin perder mucha energía. / 3. **Dureza y resistencia**: El cobre es un metal duro y resistente que puede soportar altas temperaturas y tensiones sin dañarse. /  / Otros metales que también son buenos conductores de electricidad son el oro, el plata y el bronce, pero el cobre es el más comúnmente utilizado en aplicaciones eléctricas debido a su bajo costo y alta conductividad. /  / Espero

### v8 fr baseline idx 38: falla -> correcta
**Spell out how we smell things.** (respuesta: olfactory)

> The process of smelling things involves a complex interplay of molecules, our sense of smell, and the brain. Here's a step-by-step explanation of how we smell things: /  / **Step 1: Molecules in the Air** / When an object or substance is present, it releases tiny molecules into the air. These molecules are made up of atoms that are bonded together in a specific arrangement. /  / **Step 2: Molecules Reach Our Nose** / When we breathe in, these molecules enter our nostrils and travel up the nasal cavity. The nasal cavity is lined with tiny hair-like structures called cilia, which help to filter out dust and other particles. /  / **Step 3: Molecules Bind to Receptors** / The molecules then bind to specialized receptors on the surface of olfactory sensory neurons (OSNs) in the nasal cavity. These receptors are called olfactory receptors (ORs). Each OR is sensitive to a specific type of molecule, known as an odorant. /  / **Step 4: Signal Transmission** / When a molecule binds to an OR, it triggers a chemical signal that is transmitted to the OSN. This signal is a type of electrical impulse that travels down the length of the OSN. /  / **Step 5: Signal Processing**

### v8 fr referencia idx 24: falla -> correcta
**Demystify how wounds stop bleeding.** (respuesta: platelets)

> Les plaies arrêter le saignement, c'est un processus complexe qui implique plusieurs étapes. Voici une explication détaillée : /  / Lorsqu'une plaie se produit, le sang se déverse à partir des vaisseaux sanguins endommagés. Pour arrêter le saignement, le corps utilise plusieurs mécanismes : /  / 1. **La pression exercée sur la plaie** : Lorsqu'on applique une pression sur la plaie, on compresse les vaisseaux sanguins et on empêche le sang de sortir. C'est pourquoi il est important de presser la plaie avec un chiffon propre ou un morceau de gaze pendant quelques minutes après l'incident. / 2. **La coagulation du sang** : Le corps produit des facteurs de coagulation, tels que la fibrinogène, qui se convertissent en fibrine. La fibrine forme un réseau qui empêche le sang de sortir des vaisseaux sanguins endommagés. / 3. **La formation de caillots sanguins** : Les caillots sanguins,

### v8 fr referencia idx 52: falla -> correcta
**Decode where tears come from.** (respuesta: tear glands)

> Les larmes proviennent du corps humain pour plusieurs raisons : /  / 1. **La douleur** : Lorsqu'on ressent une douleur physique ou émotionnelle, le cerveau envoie un signal au corps pour libérer des hormones qui provoquent des larmes. / 2. **La fatigue** : Les larmes peuvent également être un signe de fatigue, notamment si vous avez passé une nuit difficile ou si vous êtes épuisé. / 3. **L'émotion** : Les larmes sont souvent associées aux émotions fortes comme la tristesse, la peur ou la joie. / 4. **Les irritants** : Les larmes peuvent également être causées par des irritants tels que la poussière, les allergènes ou les produits chimiques. / 5. **Les problèmes oculaires** : Les larmes peuvent également être un signe de problèmes oculaires tels que la conjonctivite ou la lacrimation excessive. /  / En résumé, les larmes sont un mécanisme naturel du corps pour se protéger et réguler ses émotions et son

### v8 fr referencia idx 60: falla -> correcta
**How does a microwave heat food?** (respuesta: water molecules)

> Un répondeur utile! /  / Un micro-ondes utilise des ondes électromagnétiques pour chauffer les aliments. Voici comment ça fonctionne : /  / 1. Lorsque vous appuyez sur le bouton de démarrage, un générateur de micro-ondes produit des ondes électromagnétiques à une fréquence spécifique (environ 2,45 GHz). / 2. Ces ondes électromagnétiques pénètrent dans le réfrigérateur et sont réfléchies par les parois en métal. / 3. Les ondes électromagnétiques sont ensuite réparties uniformément dans le réfrigérateur par un système de réflexion. / 4. Les ondes électromagnétiques frappent les molécules d'eau et d'air dans les aliments, ce qui les excite et les fait vibrer. / 5. Ces vibrations font augmenter la température des molécules, ce qui provoque une augmentation de la température de l'aliment. / 6. Le système de réchauffage du micro-ondes contrôle la puissance des on

### v8 fr referencia idx 87: falla -> correcta
**Examine how noise-cancelling headphones work.** (respuesta: opposite waves)

> Les écouteurs avec réduction du bruit fonctionnent en utilisant un principe de physique appelé "annulation de la onde" ou "annulation de la onde de réflexion". Voici comment ça marche : /  / Les écouteurs avec réduction du bruit ont deux microphones, généralement situés sur les côtés des écouteurs, qui détectent les sons environnants. Ces microphones enregistrent les fréquences du bruit ambiant, telles que le bruit de fond, les conversations, les rumeurs, etc. /  / Les microphones envoient ensuite ces signaux à un circuit électronique qui les traite et les transforme en signaux de contrôle. Ces signaux de contrôle sont ensuite envoyés à deux drivers (parleurs) situés dans les écouteurs. /  / Les drivers ont une structure spéciale qui permet de produire des ondes sonores qui sont exactement opposées à celles du bruit ambiant. Lorsque les deux drivers produisent ces ondes sonores opposées, elles annulent les ondes du bruit ambiant, créant ainsi un effet de "réduction du br

### v8 fr parche idx 87: falla -> correcta
**Examine how noise-cancelling headphones work.** (respuesta: opposite waves)

> Les écouteurs de cancellation de bruit fonctionnent de la manière suivante : /  / 1. **Principe de base** : Les écouteurs de cancellation de bruit utilisent un système de microphones intégrés pour détecter les bruits ambiant tels que le bruit de fond, le murmure de la voix ou les sons de la rue. / 2. **Analyse du signal** : Les microphones captent les sons ambiant et les transmettent à un processeur intégré, qui analyse le signal et le compare à un signal de référence. / 3. **Génération du signal de rétroaction** : Le processeur génère un signal de rétroaction qui est l'opposé du signal de bruit détecté. Ce signal est ensuite envoyé aux écouteurs. / 4. **Cancellation de bruit** : Lorsque le signal de rétroaction est joué dans les écouteurs, il annule les sons ambiant, créant ainsi un environnement de bruit réduit. / 5. **Contrôle de la rétroaction** : Le processeur ajuste la rétroaction en fonction de la

### v8 de baseline idx 38: falla -> correcta
**Spell out how we smell things.** (respuesta: olfactory)

> The process of smelling things involves a complex interplay of molecules, our sense of smell, and the brain. Here's a step-by-step explanation of how we smell things: /  / **Step 1: Molecules in the Air** / When an object or substance is present, it releases tiny molecules into the air. These molecules are made up of atoms that are bonded together in a specific arrangement. /  / **Step 2: Molecules Reach Our Nose** / When we breathe in, these molecules enter our nostrils and travel up the nasal cavity. The nasal cavity is lined with tiny hair-like structures called cilia, which help to filter out dust and other particles. /  / **Step 3: Molecules Bind to Receptors** / The molecules then bind to specialized receptors on the surface of olfactory sensory neurons (OSNs) in the nasal cavity. These receptors are called olfactory receptors (ORs). Each OR is sensitive to a specific type of molecule, known as an odorant. /  / **Step 4: Signal Transmission** / When a molecule binds to an OR, it triggers a chemical signal that is transmitted to the OSN. This signal is a type of electrical impulse that travels down the length of the OSN. /  / **Step 5: Signal Processing**

### v8 de referencia idx 3: falla -> correcta
**Lay out how the Moon formed.** (respuesta: collision)

> Die Bildung der Mond ist ein komplexes Thema, das Wissenschaftler seit Jahrhunderten beschäftigt. Hier ist eine Übersicht über die Theorien zur Bildung der Mond: /  / **Die Theorie der Großen Zerstörung** /  / Die bekannteste Theorie zur Bildung der Mond ist die Große Zerstörung, die von Giordano Bruno im 16. Jahrhundert vorgeschlagen wurde. Laut dieser Theorie war die Erde vor etwa 4,5 Milliarden Jahren von einem riesigen Asteroiden getroffen worden, der einen riesigen Krater hinterließ. Dieser Krater wuchs schließlich zu einem Mond, der sich um die Erde drehte. /  / **Die Theorie der Planetenbildung** /  / Eine andere Theorie zur Bildung der Mond ist die Planetenbildung. Laut dieser Theorie bildete sich der Mond aus einer Gruppe von Körpern, die sich um die Erde bewegten. Diese Körper waren wahrscheinlich kleine Planeten oder Asteroiden, die sich durch eine Kollision mit der Erde vergrößerten. /  / **Die Theorie der Mondformation durch Impakt** /  / Eine

### v8 de referencia idx 4: falla -> correcta
**How does the eye focus light?** (respuesta: lens)

> Die Augenfunktion ist ein komplexer Prozess. Die Augen können Licht durch eine Kombination von drei Hauptmechanismen fokussieren: /  / 1. **Kornerlins**: Der Kornerlins ist ein Muskel, der sich um den Augapfel herum befindet. Er vergrößert oder verkleinert die Pupille, um Licht zu kontrollieren. Wenn Licht stark ist, verkleinert sich die Pupille, um weniger Licht in das Auge zu lassen. Wenn Licht schwach ist, vergrößert sich die Pupille, um mehr Licht in das Auge zu lassen. / 2. **Hiris**: Die Hiris ist ein Muskel, der sich um den Mittelpunkt des Auges befindet. Er vergrößert oder verkleinert die Pupille, um Licht zu kontrollieren. Wenn Licht stark ist, verkleinert sich die Pupille, um weniger Licht in das Auge zu lassen. Wenn Licht schwach ist, vergrößert sich die Pupille, um mehr Licht in das Auge zu lassen. / 3. **Linsen

### v8 de referencia idx 24: falla -> correcta
**Demystify how wounds stop bleeding.** (respuesta: platelets)

> Lassen Sie uns die Wundblutung demystifizieren. /  / Wenn ein Gewebe verletzt wird, kommt es zu einer Blutung, da die Blutgefäße in der Nähe des Verletzungsortes aufgerissen werden. Die Blutgefäße sind so dicht beieinander angeordnet, dass sie sich leicht aufschneiden können, wenn sie aufgerissen werden. /  / Um die Blutung zu stoppen, greifen die Körperreaktionen folgende Schritte ein: /  / 1. **Kapillarverengung**: Die Kapillarwände verengen sich, was die Durchblutung reduziert und die Blutflussgeschwindigkeit verringert. Dies führt zu einer Verringerung der Blutmenge, die aus den verletzten Gefäßen fließt. / 2. **Thrombogenese**: Der Körper beginnt, ein Thrombus (ein Blutgerinnsel) zu bilden, indem es Blutplättchen und Fibrine freisetzt. Dieser Thrombus blockiert die Blutgefä

### v8 de referencia idx 32: falla -> correcta
**How do sharks detect hidden prey?** (respuesta: electric fields)

> Die Schleichen von Haien! Sie haben eine sehr entwickelte Sinneswahrnehmung, um ihre Beute zu finden. Hier sind einige Möglichkeiten, wie sie versteckte Beute erkennen: /  / 1. **Geruchssinn**: Haien haben einen sehr feinen Geruchssinn, der es ihnen ermöglicht, den Geruch von Blut, Fleisch oder anderen Organen in der Umgebung zu erkennen. Sie können auch den Geruch von Fischen und anderen Meerestieren in der Nähe ihrer Beute wahrnehmen. / 2. **Seh- und Hörvermögen**: Haien haben ein sehr gutes Seh- und Hörvermögen, das es ihnen ermöglicht, ihre Umgebung zu überwachen und potenzielle Beute zu erkennen. Sie können auch die Bewegungen von Fischen und anderen Meerestieren im Wasser wahrnehmen. / 3. **Elektrorezeption**: Einige Haiarten, wie die Hammerhaien, haben eine spezielle Sinnesorgan, das Elektrorezeptor genannt. Dieses Organ ermöglicht es ihnen, elektrische Signale von anderen T

### v8 de referencia idx 38: falla -> correcta
**Spell out how we smell things.** (respuesta: olfactory)

> Um die Art und Weise zu erklären, wie wir Dinge riechen, müssen wir uns die folgenden Schritte vorstellen: /  / 1. **Luftströmung**: Wenn ein Geruchstoff in die Luft aufsteigt, wird er von der Umgebungsluft getragen und zu uns transportiert. / 2. **Nasenlöcher**: Wenn der Geruchstoff in die Nase eintritt, wird er durch die Nasenlöcher aufgenommen. / 3. **Nasenschleimhäute**: Die Geruchstoffe treffen auf die Nasenschleimhäute, die spezielle Zellen sind, die für die Aufnahme von Gerüchen verantwortlich sind. / 4. **Olfaktorische Zellen**: Die Geruchstoffe binden an spezielle Proteine auf den olfaktorischen Zellen, die für die Wahrnehmung von Gerüchen verantwortlich sind. / 5. **Signalübertragung**: Die bindenden Geruchstoffe senden Signale an das Gehirn, das diese Signale als bestimmte Gerüche wahrnimmt. / 6. **Gehirnver

### v8 de referencia idx 67: falla -> correcta
**How do airbags inflate so fast?** (respuesta: sodium azide)

> Die Luftballons, die in Autos installiert sind, sind tatsächlich sehr schnell aufgebläht. Hier ist, warum: /  / Die Luftballons bestehen aus einem speziellen Material, das als "Kevlar" bekannt ist. Dieses Material ist sehr widerstandsfähig gegenüber Druck und kann sehr schnell aufgebläht werden. /  / Wenn ein Luftballon aufgebläht wird, drückt er sich auf die umgebende Luft aus. Dieser Druckwiderstand treibt die Luft in den Ballon ein und verursacht eine schnelle Erhöhung des Drucks. /  / Die Luftballons sind mit einem speziellen Gas gefüllt, das als "Nitrogen" bekannt ist. Dieses Gas ist sehr leicht und kann sehr schnell aufgebläht werden. /  / Wenn ein Luftballon aufgebläht wird, wird das Gas so schnell wie möglich in den Ballon eingeschlossen. Dies geschieht durch eine spezielle Membran, die den Ballon mit der umgebenden Luft verbindet. /  / Die gesamte Aufblähung eines Luftballons kann in weniger als 20

### v8 de referencia idx 95: falla -> correcta
**How do clouds stay up?** (respuesta: droplets)

> Das ist eine großartige Frage! /  / Wasserwolken, auch als Cumulus-Wolken bekannt, bleiben aufgrund von mehreren Faktoren auf. Hier sind einige Gründe: /  / 1. **Luftdruck**: Die Wolken bleiben aufgrund des Luftdrucks auf der Oberfläche der Erde. Der Luftdruck hält die Wolken in der Luft, ähnlich wie ein Luftballon. / 2. **Schwerkraft**: Die Schwerkraft zieht die Wolken nach unten, aber die Luft in den Wolken ist so leicht, dass sie die Schwerkraft überwinden kann. / 3. **Luftströmungen**: Die Luftströmungen in der Atmosphäre, wie z.B. Wind und Luftzirkulationen, helfen, die Wolken aufrechtzuerhalten. / 4. **Wasserdampf**: Die Wolken sind voller Wasserdampf, der als Gas in der Luft existiert. Dieser Wasserdampf gibt den Wolken ihre Form und Halt. / 5. **Kondensation**: Wenn der Wasserdampf in der Luft kühlt, kondensiert er zu Tropfen und bildet die

### v8 de parche idx 38: falla -> correcta
**Spell out how we smell things.** (respuesta: olfactory)

> Das ist eine interessante Frage! /  / Wir "riechen" Dinge, indem unsere Nase mit einem speziellen Geräusch organisiert ist. Hier ist, wie es funktioniert: /  / 1. **Luftströmung**: Wenn wir Luft atmen, strömt die Luft durch unsere Nase ein. / 2. **Nasenschleim**: Der Nasenschleim, auch bekannt als Mucosa, ist ein feiner, schützender Film, der die Luftströmung blockiert und die Gerüche filtert. / 3. **Geruchsknospen**: Die Nasenschleimhaut enthält spezielle Geruchsknospen, die sich in der Nasenlöcher befinden. Diese Knospen sind sehr fein und haben eine große Oberfläche. / 4. **Olfaktorien**: Die Geruchsknospen sind mit Olfaktorien besetzt, die spezielle Rezeptoren sind, die für bestimmte Gerüche verantwortlich sind. / 5. **Bindung von Molekülen**: Wenn eine bestimmte Molekülkette (eine chemische Verbindung) in die Luft strö

### v8 de parche idx 87: falla -> correcta
**Examine how noise-cancelling headphones work.** (respuesta: opposite waves)

> **Wie funktionieren Störschutzohren?** /  / Störschutzohren, auch bekannt als Noise-Cancelling-Headphones, sind ein wunderbares Gerät, das es ermöglicht, störende Geräusche um den Kopf herum zu ignorieren. Hier ist, wie es funktioniert: /  / **Prinzip** /  / Störschutzohren nutzen ein spezielles Prinzip, um störende Geräusche zu filtern. Sie verwenden ein Mikrofon, das ständig die Umgebungslautsität aufnimmt, und ein Verstärker, der die störenden Geräusche aufnimmt. Anschließend wird ein Verstärker verwendet, um die störenden Geräusche auf der anderen Seite des Kopfhörers zu erzeugen, so dass sie den störenden Geräuschen entgegenwirken. /  / **Schritte** /  / Hier sind die Schritte, die ein Störschutzohr unternehmen, um störende Geräusche zu filtern: /  / 1. **Mikrofon**: Ein Mikrofon im Kop

### v8 de parche idx 109: falla -> correcta
**How do hedgehogs defend themselves?** (respuesta: spines)

> Hochhäuter (auch als Echsenbär oder Wollbär bekannt) haben mehrere Methoden, um sich zu verteidigen. Hier sind einige ihrer gängigsten Verteidigungsmethoden: /  / 1. **Spitze Scheren**: Hochhäuter haben spitze, scharfe Scheren auf ihren Vorderpfoten, die sie als Waffe verwenden können. Sie können diese Scheren auch benutzt, um sich von Fressfeinden zu befreien. / 2. **Wollhaar**: Hochhäuter haben ein dichtes, weiches Wollhaar, das sie ausbreiten können, wenn sie sich bedroht fühlen. Dieses Wollhaar kann Fressfeinde irritieren und ihnen Zeit geben, zu fliehen. / 3. **Rollen**: Wenn sie sich bedroht fühlen, können Hochhäuter sich in eine Kugel ausrollen und sich mit ihrem Wollhaar umhüllen. Dies kann Fressfeinde abschrecken und ihnen Zeit geben, zu fliehen. / 4. **Biss**: Hochhäuter haben scharfe Zähne und können

### v9 es baseline idx 38: falla -> correcta
**Spell out how we smell things.** (respuesta: olfactory)

> The process of smelling things involves a complex interplay of molecules, our sense of smell, and the brain. Here's a step-by-step explanation of how we smell things: /  / **Step 1: Molecules in the Air** / When an object or substance is present, it releases tiny molecules into the air. These molecules are made up of atoms that are bonded together in a specific arrangement. /  / **Step 2: Molecules Reach Our Nose** / When we breathe in, these molecules enter our nostrils and travel up the nasal cavity. The nasal cavity is lined with tiny hair-like structures called cilia, which help to filter out dust and other particles. /  / **Step 3: Molecules Bind to Receptors** / The molecules then bind to specialized receptors on the surface of olfactory sensory neurons (OSNs) in the nasal cavity. These receptors are called olfactory receptors (ORs). Each OR is sensitive to a specific type of molecule, known as an odorant. /  / **Step 4: Signal Transmission** / When a molecule binds to an OR, it triggers a chemical signal that is transmitted to the OSN. This signal is a type of electrical impulse that travels down the length of the OSN. /  / **Step 5: Signal Processing**

### v9 es referencia idx 32: falla -> correcta
**How do sharks detect hidden prey?** (respuesta: electric fields)

> Los tiburones tienen un sentido de olfato muy desarrollado y una excelente visión, lo que les permite detectar a sus presas ocultas de varias maneras. Aquí te presento algunas de las formas en que los tiburones detectan a sus presas: /  / 1. **Olfato**: Los tiburones tienen una gran cantidad de glándulas nasales que producen una sustancia llamada "olfato tiburón", que es similar al olfato humano. Este olfato les permite detectar el olor a sangre, sudor y otros olores corporales que emiten las presas. / 2. **Visión**: Los tiburones tienen una excelente visión de movimiento y pueden detectar a sus presas desde una gran distancia. Su campo de visión es muy amplio y pueden ver en diferentes direcciones al mismo tiempo. / 3. **Hearing**: Los tiburones también tienen un sentido del sonido muy desarrollado y pueden detectar los sonidos que emiten las presas, como el latido del corazón o el movimiento de las escamas. / 4. **Electroreceptores**: Los tiburones tienen electro

### v9 es parche idx 24: falla -> correcta
**Demystify how wounds stop bleeding.** (respuesta: platelets)

> El proceso de detener la hemorragia en una herida es fascinante. Aquí te explico cómo funciona: /  / Cuando una herida se produce, los vasos sanguíneos se rompen y la sangre comienza a fluir fuera del cuerpo. Sin embargo, el cuerpo tiene un mecanismo para detener la hemorragia de manera rápida y eficiente. /  / **La respuesta inmediata** /  / Inmediatamente después de la lesión, el cuerpo libera una serie de hormonas y sustancias químicas que ayudan a detener la hemorragia. La hormona principal responsable es la histamina, que se libera por las células del tejido dañado. La histamina provoca la contracción de los vasos sanguíneos cercanos a la herida, lo que reduce la cantidad de sangre que fluye hacia la zona dañada. /  / **La formación de coágulos** /  / Mientras tanto, el cuerpo también comienza a formar coágulos en la herida. Los coágulos son estructuras sólidas formadas por plaquetas y fibrina, que se unen para

### v9 es parche idx 32: falla -> correcta
**How do sharks detect hidden prey?** (respuesta: electric fields)

> Los tiburones detectan la presa escondida mediante una combinación de habilidades sensoriales y estrategias de caza. Aquí hay algunas formas en que los tiburones detectan la presa escondida: /  / 1. **Olfato**: Los tiburones tienen un sentido del olfato muy desarrollado, que les permite detectar el olor de la sangre y los productos de descomposición de la presa. Pueden detectar olores muy débiles a grandes distancias. / 2. **Vista**: Los tiburones tienen una visión excelente, especialmente en el agua. Pueden detectar movimientos y cambios en la luz que indican la presencia de una presa. / 3. **Hearing**: Los tiburones también tienen un sentido del sonido muy desarrollado, que les permite detectar los sonidos de la presa, como el latido del corazón o el movimiento de las escamas. / 4. **Electroreceptores**: Los tiburones tienen electroreceptores en su barbilla y en su cola, que les permiten detectar los campos eléctricos generados por la

### v9 fr baseline idx 38: falla -> correcta
**Spell out how we smell things.** (respuesta: olfactory)

> The process of smelling things involves a complex interplay of molecules, our sense of smell, and the brain. Here's a step-by-step explanation of how we smell things: /  / **Step 1: Molecules in the Air** / When an object or substance is present, it releases tiny molecules into the air. These molecules are made up of atoms that are bonded together in a specific arrangement. /  / **Step 2: Molecules Reach Our Nose** / When we breathe in, these molecules enter our nostrils and travel up the nasal cavity. The nasal cavity is lined with tiny hair-like structures called cilia, which help to filter out dust and other particles. /  / **Step 3: Molecules Bind to Receptors** / The molecules then bind to specialized receptors on the surface of olfactory sensory neurons (OSNs) in the nasal cavity. These receptors are called olfactory receptors (ORs). Each OR is sensitive to a specific type of molecule, known as an odorant. /  / **Step 4: Signal Transmission** / When a molecule binds to an OR, it triggers a chemical signal that is transmitted to the OSN. This signal is a type of electrical impulse that travels down the length of the OSN. /  / **Step 5: Signal Processing**

### v9 fr referencia idx 4: falla -> correcta
**How does the eye focus light?** (respuesta: lens)

> L'œil concentre la lumière grâce à un système complexe de structures anatomo-physiologiques. Voici les étapes clés : /  / 1.  **La rétine** : La rétine est une couche fine située à l'arrière de l'œil. Elle contient des cellules photoréceptrices appelées cones et des cellules photoréceptrices appelées bâtonnets. Les cones sont responsables de la vision des couleurs, tandis que les bâtonnets sont responsables de la vision de la lumière et de la détection des mouvements. / 2.  **La rétine est composée de plusieurs couches** : La rétine est composée de plusieurs couches, notamment la couche de photorécepteurs, la couche de connecteurs, la couche de ganglions et la couche de nerfs optiques. / 3.  **La lumière pénètre dans l'œil** : La lumière pénètre dans l'œil à travers la cornée, qui est la couche externe de l'œil. / 4.

### v9 fr referencia idx 18: falla -> correcta
**How do hurricanes get their energy?** (respuesta: warm water)

> Les ouragans tirent leur énergie de la chaleur de la surface de la Terre. Lorsque le soleil chauffe l'eau de la mer, il crée une zone de basse pression près de la surface. Cela entraîne un mouvement de l'air chaud vers les hauteurs, créant une zone de basse pression au-dessus de la mer. /  / Dans cette zone de basse pression, l'air se refroidit et se condense, formant des nuages. Lorsque l'air se refroidit encore, il devient saturé d'eau et se condense en gouttelettes, ce qui crée des précipitations. /  / Cependant, les ouragans sont des cyclones tropicaux qui se forment au-dessus de l'eau chaude des océans. Lorsque l'air chaud et humide se soulève, il crée une zone de basse pression qui attire l'air plus sec et plus froid. Cela crée un cycle de mouvement qui se renforce et se renforce, créant un système de rotation qui peut devenir un ouragan. /  / En

### v9 fr referencia idx 52: falla -> correcta
**Decode where tears come from.** (respuesta: tear glands)

> Les larmes! Elles sont un phénomène complexe qui peut provenir de plusieurs sources. Voici quelques-unes des explications les plus courantes : /  / 1. **Réflexe de détresse** : Les larmes sont un réflexe naturel de détresse, de peur, de tristesse ou de douleur. Lorsque nous sommes confrontés à une situation difficile, notre cerveau libère des hormones telles que l'adrénaline et l'acide thyroïdien, qui peuvent provoquer des larmes. / 2. **Émotions** : Les larmes peuvent être un moyen de exprimer et de gérer nos émotions. Nous pouvons pleurer pour exprimer notre tristesse, notre joie, notre colère ou notre soulagement. / 3. **Physiologie** : Les larmes sont produites par les glandes lacrimales situées dans les yeux. Elles servent à nettoyer les yeux et à protéger la vision. Cependant, les larmes peuvent également être produites en réponse à des stimuli physiques, tels que

### v9 fr referencia idx 67: falla -> correcta
**How do airbags inflate so fast?** (respuesta: sodium azide)

> Les airbags sont des dispositifs de sécurité installés dans les véhicules pour protéger les passagers en cas d'impact. Ils se composent généralement d'un réservoir de gaz comprimé, d'un système de déclencheur et d'un tube de déplacement. Voici comment ils fonctionnent : /  / 1. **Déclencheur** : Lorsqu'un airbag est activé, un déclencheur est déclenché par un capteur de détection d'impact, tel qu'un capteur de collision ou un capteur de détection de tête. Ce capteur détecte la force de l'impact et envoie un signal électrique au système d'airbag. / 2. **Réservoir de gaz** : Le réservoir de gaz est rempli d'un gaz comprimé, généralement du dioxyde de carbone ou de l'azote. Ce gaz est sous haute pression, généralement entre 30 et 100 bar. / 3. **Système de déplacement** : Lorsque le déclencheur est activé, le système de déplacement

### v9 de baseline idx 38: falla -> correcta
**Spell out how we smell things.** (respuesta: olfactory)

> The process of smelling things involves a complex interplay of molecules, our sense of smell, and the brain. Here's a step-by-step explanation of how we smell things: /  / **Step 1: Molecules in the Air** / When an object or substance is present, it releases tiny molecules into the air. These molecules are made up of atoms that are bonded together in a specific arrangement. /  / **Step 2: Molecules Reach Our Nose** / When we breathe in, these molecules enter our nostrils and travel up the nasal cavity. The nasal cavity is lined with tiny hair-like structures called cilia, which help to filter out dust and other particles. /  / **Step 3: Molecules Bind to Receptors** / The molecules then bind to specialized receptors on the surface of olfactory sensory neurons (OSNs) in the nasal cavity. These receptors are called olfactory receptors (ORs). Each OR is sensitive to a specific type of molecule, known as an odorant. /  / **Step 4: Signal Transmission** / When a molecule binds to an OR, it triggers a chemical signal that is transmitted to the OSN. This signal is a type of electrical impulse that travels down the length of the OSN. /  / **Step 5: Signal Processing**

### v9 de referencia idx 4: falla -> correcta
**How does the eye focus light?** (respuesta: lens)

> Das Auge bündelt Licht, indem es es durch eine komplexe Anordnung von Strukturen und -materialien verarbeitet. Hier ist eine vereinfachte Erklärung, wie das Auge Licht bündelt: /  / 1.  **Korona**: Die Korona ist die äußere Schicht des Auges, die den Blick auf die Pupille richtet. Sie besteht aus einer dichten Masse von Epithelzellen, die Lichtstrahlen aufnehmen und in die Pupille leiten. / 2.  **Pupille**: Die Pupille ist die dunkle Mitte der Iris, die sich um die Pupillenrand öffnet und Licht auf die Retina lenkt. Sie besteht aus Muskelzellen, die sich um die Pupille öffnen und schließen können. / 3.  **Linsen**: Die Linsen sind zwei glatte, runde Strukturen, die sich hinter der Pupille befinden. Sie bestehen aus einer dichten Masse von Zellen und gelösten Proteinen, die Lichtstrahlen aufnehmen und in die Retina lenken. / 4.  **Ret

### v9 de referencia idx 20: falla -> correcta
**Be honest: who wrote The Canterbury Tales?** (respuesta: Chaucer)

> Eine großartige Frage! /  / Die Canterbury-Erzählungen sind ein mittelalterliches Werk, das wahrscheinlich von mehreren Autoren geschrieben wurde. Die genaue Autorität ist jedoch nicht bekannt. /  / Die Erzählungen bestehen aus 24 Novellen, die von einem Zug nach Canterbury gefahren werden, und werden von verschiedenen Charakteren erzählt, die auf dem Weg sind, das Heiligtum der Jungfrau Maria in Canterbury zu besuchen. Jeder Charakter erzählt eine separate Geschichte, die oft satirisch, humorvoll oder moralisch ist. /  / Die meisten Historiker glauben, dass die Canterbury-Erzählungen von mehreren Autoren im 14. Jahrhundert geschrieben wurden, wahrscheinlich von einem oder mehreren Schriftstellern, die sich auf der Suche nach Unterhaltung und Bildung befanden. Einige der bekanntesten Theorien besagen, dass die Erzählungen von: /  / * Geoffrey Chaucer geschrieben wurden, dem bekanntesten englischen Dichter des Mittelalters. Chaucer ist jedoch nicht der einzige Autor, der zur Canterbury-Erzählung beiget

### v9 de referencia idx 32: falla -> correcta
**How do sharks detect hidden prey?** (respuesta: electric fields)

> Haie haben ein sehr entwickeltes Sinnsystem, das es ihnen ermöglicht, ihre Umgebung zu erkunden und potenzielle Nahrung zu lokalisieren. Sie nutzen mehrere Sinneswege, um versteckte Beute zu spüren. Hier sind einige der wichtigsten Sinneswege, die Haie verwenden: /  / 1. **Sehsinn**: Haie haben ein ausgeprägtes Sehsinn, das es ihnen ermöglicht, Lichtwellen zu detektieren. Sie können Lichtwellen, die von der Beute abgegeben werden, erkennen und verfolgen. Dies ist besonders wichtig, um die Beute zu lokalisieren und zu identifizieren. /  / 2. **Lautsinn**: Haie können auch Lautwellen hören, die von der Beute abgegeben werden. Dies hilft ihnen, potenzielle Nahrung zu lokalisieren und zu identifizieren, auch wenn sie nicht direkt sehen können. /  / 3. **Elektrorezeption**: Viele Haie haben eine Elektrorezeptionsfähigkeit, die es ihnen ermöglicht, elektrische Signale in der Umgebung zu det

### v9 de referencia idx 38: falla -> correcta
**Spell out how we smell things.** (respuesta: olfactory)

> Die Wahrnehmung von Gerüchen ist ein komplexer Prozess, der unsere Sinne stark beeinflusst. Hier ist eine detaillierte Erklärung, wie wir Gerüche wahrnehmen: /  / **Die Reize an der Nase** /  / Wenn wir etwas riechen, werden die Reize, die von der Umgebung ausgesandt werden, an unsere Nase gelangen. Diese Reize sind in Form von Molekülen, die in der Luft schwimmen. Die meisten Gerüche bestehen aus kleinen Molekülen, die zwischen 1 und 10 Mikrometern groß sind. /  / **Die Aufnahme durch die Nase** /  / Wenn diese Moleküle in die Nase eindringen, treffen sie auf spezielle Zellen, die als Olfaktorien bezeichnet werden. Diese Zellen sind in der Form von Faltungen auf der Oberfläche der Nase angeordnet und haben spezielle Rezeptoren, die für bestimmte Gerüche verantwortlich sind. /  / **Die Bindung an Rezeptoren** /  / Wenn die Moleküle die Olfaktorien erreichen, binden sie

### v9 de parche idx 13: falla -> correcta
**Sorry, who first split the atom?** (respuesta: Rutherford)

> Keine Sorge! /  / Die Frage nach der Entdeckung des Atomspaltens wird oft dem deutschen Physiker Wilhelm Conrad Röntgen zugeschrieben. Am 6. August 1895 entdeckte er, dass ein Teil des Lichts durch Materie hindurchgehen kann, ohne dass es absorbiert wird. Dieses Phänomen wurde als Röntgenstrahlung bezeichnet. /  / Allerdings war es der deutschen Physiker Heinrich Hertz, der 1887 die Existenz der elektromagnetischen Wellen und ihre Fähigkeit, Materie zu durchdringen, nachgewiesen hatte. /  / Die Spaltung des Atoms selbst ist jedoch ein komplexeres Thema, das im 20. Jahrhundert durch die Arbeit von Physikern wie Ernest Rutherford, Niels Bohr und Werner Heisenberg gelöst wurde. Rutherford entdeckte 1911, dass das Atom aus einem kleinen, schweren Kern besteht, umgeben von einem äußeren Electronenhaarm. Bohr und Heisenberg entwickelten dann die Quantentheorie, die die Eigenschaften der Atome und Moleküle beschreibt. /  / Ich h

### v9 de parche idx 24: falla -> correcta
**Demystify how wounds stop bleeding.** (respuesta: platelets)

> Die Blutstillung ist ein komplexer Prozess, der nach einem Verletzung auftritt. Hier ist eine detaillierte Erklärung, wie Wunden bluten und wie sie schließlich stoppen: /  / **Schritt 1: Blutung** /  / Wenn eine Hautverletzung auftritt, brechen die Blutgefäße in der Haut und die Blutgefäße in der umliegenden Substanz (wie Muskel oder Knochen) leiten. Dies führt zu einer Blutung, bei der Blut aus den gerissenen Gefäßen in den umliegenden Geweben fließt. /  / **Schritt 2: Blutaustritt** /  / Das Blut fließt aus den gerissenen Gefäßen und bildet eine Blutung. Die Blutung kann durch verschiedene Faktoren beeinflusst werden, wie z.B. die Tiefe der Verletzung, die Art der Verletzung und die Präsenz von Blutgerinnungshemmern. /  / **Schritt 3: Blutgerinnung** /  / Wenn das Blut aus den gerissenen Gef

### v9 de parche idx 33: falla -> correcta
**Hardest human tissue?** (respuesta: enamel)

> Das ist eine interessante Frage! /  / Es ist schwierig, ein einziges "hardestes" menschliches Gewebe zu nennen, da die Härte von Geweben je nach Art, Struktur und Funktion variieren kann. Allerdings gibt es einige Gewebe, die aufgrund ihrer Zusammensetzung und Struktur als besonders hart gelten. /  / Einige Beispiele sind: /  / 1. **Knochen**: Knochen sind bekannt für ihre hohe Härte und sind eines der härtesten Gewebe im menschlichen Körper. Sie bestehen aus Kollagen-Fasern und Mineralien wie Calcium und Phosphor, die eine hohe Festigkeit und Härte verleihen. / 2. **Zähne**: Zähne sind ebenfalls sehr hart und bestehen aus einem harten, kohlenstoffhaltigen Material namens Enamel. Enamel ist das härteste Gewebe im menschlichen Körper und bietet Schutz für die empfindliche Zahnempfecher. / 3. **Haut**: Die Haut ist das äußere Gewebe des Körpers und besteht aus einer Schicht von Zellen, die sich

### v9 de parche idx 66: falla -> correcta
**Fill me in on how glasses fix vision.** (respuesta: lenses)

> **Wie funktionieren Brillen?** /  / Brillen sind ein wichtiger Bestandteil der Augenschutz- und -pflege. Sie helfen, das Sehen zu verbessern und vor verschiedenen Augenschäden zu schützen. Hier ist eine detaillierte Erklärung, wie Brillen funktionieren: /  / **Das Prinzip der Brillen** /  / Brillen bestehen aus zwei Hauptteilen: dem Gläser und der Hülle. Der Gläser ist das Teil, das direkt auf das Auge gerichtet ist, und enthält das Sehmittel. Die Hülle ist das Teil, das den Gläser umgibt und den Träger schützt. /  / **Wie funktioniert das Sehmittel?** /  / Das Sehmittel in den Brillen ist meist aus Plastik oder Glas gefertigt und enthält eine Kombination aus verschiedenen Materialien, wie z.B. Linsen, Prismen und Reflexen. Diese Materialien dienen dazu, das Licht auf das Auge zu fokussieren und das Sehen zu verbessern. /  / *   **Linsen**: Linsen sind die wichtigste Komponente in Brill

### v9 de parche idx 74: falla -> correcta
**How are diamonds formed?** (respuesta: carbon)

> Diamanten sind durch eine komplexe Prozessformierung entstanden. Sie entstehen in der Erdkruste durch eine Kombination aus hohen Temperaturen, hohem Druck und chemischen Reaktionen. Hier ist eine kurze Übersicht über die Schritte der Diamantbildung: /  / 1.  **Erwärmung und Druck**: Die Diamantbildung beginnt in der Erdkruste, wo Wasser und Salze unter hohen Temperaturen und Drücken aufgelöst sind. Diese Lösungen können dann in tieferen Schichten der Erde aufgelöst werden, wo sie unter hohen Temperaturen und Drücken aufgelöst werden. / 2.  **Kohlenstoff- und Wasserstoff-Verbindungen**: In diesen tieferen Schichten reagieren die Lösungen mit Kohlenstoff- und Wasserstoff-Verbindungen, die in der Erdoberfläche entstehen. Diese Reaktionen führen zur Bildung von Graphit, einem Form von Kohlenstoff, der die Grundlage für die Diamantbildung bildet. / 3.  **Verdickung und Kristallisation**: Wenn die Lösungen weiter

### v9 de parche idx 95: falla -> correcta
**How do clouds stay up?** (respuesta: droplets)

> Das ist eine großartige Frage! /  / Wasserwaftchen, auch bekannt als "Wasserwaftchen", sind winzige, flüssige Partikel, die in der Atmosphäre entstehen. Sie sind für die Bildung von Wolken verantwortlich. /  / Hier ist, wie es funktioniert: /  / 1. **Wasser aus dem Ozean und Seen**: Wenn die Sonne die Oberfläche des Ozeans und Seen erwärmt, wird das Wasser in Dampf umgewandelt. / 2. **Dampf in die Atmosphäre**: Der Dampf steigt in die Atmosphäre auf und wird von der Schwerkraft nach oben getrieben. / 3. **Kondensation**: Wenn der Dampf in die kühle Atmosphäre erreicht, kondensiert er sich zu winzigen Tropfen Wasser. / 4. **Wasserwaftchen**: Die Tropfen Wasserwaftchen werden von Wind und Luftströmungen getrennt und beginnen, sich zu bewegen. / 5. **Wolkenbildung**: Wenn genügend Wasserwaftchen zusammenkommen, bilden sie eine Wolke. /  / Das ist die Grundlage

### v9 de parche idx 109: falla -> correcta
**How do hedgehogs defend themselves?** (respuesta: spines)

> Hedgehogs haben eine sehr effektive Verteidigungsmethode entwickelt, um sich vor Raubtieren zu schützen. Ihre Verteidigungsmethode basiert auf ihrer Fähigkeit, sich mit ihren scharfen, spitzen Hörnern zu verteidigen. /  / Hier sind einige Weisen, wie Hedgehogs sich selbst verteidigen: /  / 1. **Hörner ausstrecken**: Wenn ein Raubtier wie ein Hund oder ein Fuchs auf den Hedgehog zukommt, reckt er seine Hörner aus und zeigt sie dem Angreifer. Dies kann den Angreifer abschrecken und ihn davon abhalten, den Hedgehog anzugreifen. / 2. **Hörner als Waffe**: Wenn der Hedgehog bedroht wird, kann er seine Hörner als Waffe verwenden, um den Angreifer zu verletzen. Die Hörner sind sehr scharf und können den Angreifer verletzen, wenn sie direkt auf ihn gerichtet werden. / 3. **Rollen**: Wenn der Hedgehog sich bedroht fühlt, kann er sich in eine Kugel aus Hör

