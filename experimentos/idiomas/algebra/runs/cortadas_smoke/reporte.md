# Held-out v8/v9: salidas cortadas re-generadas

Salidas que llegaban al limite (>= 95% de los tokens) re-generadas con `--num_tokens 250`. Veredictos viejos recalculados con los alias actuales.

| version | idioma | condicion | cortadas | correctas antes | correctas ahora | siguen cortadas | held-out antes | held-out ahora | no-prefijo |
|---|---|---|---|---|---|---|---|---|---|
| v8 | es | baseline | 2 | 2 | 2 | 2 | 108/112 (96.4%) | 108/112 (96.4%) | 0 |
| v8 | es | referencia | 1 | 1 | 1 | 1 | 95/112 (84.8%) | 95/112 (84.8%) | 0 |
| v8 | es | parche | 2 | 1 | 1 | 2 | 82/112 (73.2%) | 82/112 (73.2%) | 0 |
| v8 | fr | baseline | 2 | 2 | 2 | 2 | 108/112 (96.4%) | 108/112 (96.4%) | 0 |
| v8 | fr | referencia | 2 | 2 | 2 | 2 | 91/112 (81.2%) | 91/112 (81.2%) | 0 |
| v8 | fr | parche | 2 | 2 | 2 | 2 | 90/112 (80.4%) | 90/112 (80.4%) | 0 |
| v8 | de | baseline | 2 | 2 | 2 | 2 | 108/112 (96.4%) | 108/112 (96.4%) | 0 |
| v8 | de | referencia | 2 | 0 | 2 | 2 | 89/112 (79.5%) | 91/112 (81.2%) | 0 |
| v8 | de | parche | 2 | 2 | 2 | 2 | 87/112 (77.7%) | 87/112 (77.7%) | 0 |
| v9 | es | baseline | 2 | 2 | 2 | 2 | 108/112 (96.4%) | 108/112 (96.4%) | 0 |
| v9 | es | referencia | 2 | 2 | 2 | 2 | 80/112 (71.4%) | 80/112 (71.4%) | 0 |
| v9 | es | parche | 2 | 2 | 2 | 2 | 88/112 (78.6%) | 88/112 (78.6%) | 0 |
| v9 | fr | baseline | 2 | 2 | 2 | 2 | 108/112 (96.4%) | 108/112 (96.4%) | 0 |
| v9 | fr | referencia | 2 | 0 | 1 | 2 | 80/112 (71.4%) | 81/112 (72.3%) | 0 |
| v9 | fr | parche | 2 | 2 | 2 | 1 | 86/112 (76.8%) | 86/112 (76.8%) | 0 |
| v9 | de | baseline | 2 | 2 | 2 | 2 | 108/112 (96.4%) | 108/112 (96.4%) | 0 |
| v9 | de | referencia | 2 | 1 | 2 | 2 | 83/112 (74.1%) | 84/112 (75.0%) | 0 |
| v9 | de | parche | 2 | 2 | 2 | 2 | 88/112 (78.6%) | 88/112 (78.6%) | 0 |

`no-prefijo`: salidas nuevas que no empiezan con la vieja. Con greedy deberia ser 0; si no lo es, la diferencia no es solo el largo (no determinismo de GPU, otro cache, otro checkpoint) y esa fila no es comparable.

## Veredictos que cambiaron

### v8 de referencia idx 3: falla -> correcta
**Lay out how the Moon formed.** (respuesta: collision)

> Die Bildung der Mond ist ein komplexes Thema, das Wissenschaftler seit Jahrhunderten beschäftigt. Hier ist eine Übersicht über die Theorien zur Bildung der Mond: /  / **Die Theorie der Großen Zerstörung** /  / Die bekannteste Theorie zur Bildung der Mond ist die Große Zerstörung, die von Giordano Bruno im 16. Jahrhundert vorgeschlagen wurde. Laut dieser Theorie war die Erde vor etwa 4,5 Milliarden Jahren von einem riesigen Asteroiden getroffen worden, der einen riesigen Krater hinterließ. Dieser Krater wuchs schließlich zu einem Mond, der sich um die Erde drehte. /  / **Die Theorie der Planetenbildung** /  / Eine andere Theorie zur Bildung der Mond ist die Planetenbildung. Laut dieser Theorie bildete sich der Mond aus einer Gruppe von Körpern, die sich um die Erde bewegten. Diese Körper waren wahrscheinlich kleine Planeten oder Asteroiden, die sich durch eine Kollision mit der Erde vergrößerten. /  / **Die Theorie der Mondformation durch Impakt** /  / Eine

### v8 de referencia idx 4: falla -> correcta
**How does the eye focus light?** (respuesta: lens)

> Die Augenfunktion ist ein komplexer Prozess. Die Augen können Licht durch eine Kombination von drei Hauptmechanismen fokussieren: /  / 1. **Kornerlins**: Der Kornerlins ist ein Muskel, der sich um den Augapfel herum befindet. Er vergrößert oder verkleinert die Pupille, um Licht zu kontrollieren. Wenn Licht stark ist, verkleinert sich die Pupille, um weniger Licht in das Auge zu lassen. Wenn Licht schwach ist, vergrößert sich die Pupille, um mehr Licht in das Auge zu lassen. / 2. **Hiris**: Die Hiris ist ein Muskel, der sich um den Mittelpunkt des Auges befindet. Er vergrößert oder verkleinert die Pupille, um Licht zu kontrollieren. Wenn Licht stark ist, verkleinert sich die Pupille, um weniger Licht in das Auge zu lassen. Wenn Licht schwach ist, vergrößert sich die Pupille, um mehr Licht in das Auge zu lassen. / 3. **Linsen

### v9 fr referencia idx 4: falla -> correcta
**How does the eye focus light?** (respuesta: lens)

> L'œil concentre la lumière grâce à un système complexe de structures anatomo-physiologiques. Voici les étapes clés : /  / 1.  **La rétine** : La rétine est une couche fine située à l'arrière de l'œil. Elle contient des cellules photoréceptrices appelées cones et des cellules photoréceptrices appelées bâtonnets. Les cones sont responsables de la vision des couleurs, tandis que les bâtonnets sont responsables de la vision de la lumière et de la détection des mouvements. / 2.  **La rétine est composée de plusieurs couches** : La rétine est composée de plusieurs couches, notamment la couche de photorécepteurs, la couche de connecteurs, la couche de ganglions et la couche de nerfs optiques. / 3.  **La lumière pénètre dans l'œil** : La lumière pénètre dans l'œil à travers la cornée, qui est la couche externe de l'œil. / 4.

### v9 de referencia idx 4: falla -> correcta
**How does the eye focus light?** (respuesta: lens)

> Das Auge bündelt Licht, indem es es durch eine komplexe Anordnung von Strukturen und -materialien verarbeitet. Hier ist eine vereinfachte Erklärung, wie das Auge Licht bündelt: /  / 1.  **Korona**: Die Korona ist die äußere Schicht des Auges, die den Blick auf die Pupille richtet. Sie besteht aus einer dichten Masse von Epithelzellen, die Lichtstrahlen aufnehmen und in die Pupille leiten. / 2.  **Pupille**: Die Pupille ist die dunkle Mitte der Iris, die sich um die Pupillenrand öffnet und Licht auf die Retina lenkt. Sie besteht aus Muskelzellen, die sich um die Pupille öffnen und schließen können. / 3.  **Linsen**: Die Linsen sind zwei glatte, runde Strukturen, die sich hinter der Pupille befinden. Sie bestehen aus einer dichten Masse von Zellen und gelösten Proteinen, die Lichtstrahlen aufnehmen und in die Retina lenken. / 4.  **Ret

