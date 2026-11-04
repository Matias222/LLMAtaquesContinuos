# Entrada o directiva (preset `idioma_pares`)

Parches: `es2fr` (norma 0.500, goal_all), `de2fr` (norma 0.500, goal_all), `de2es` (norma 0.500, goal_all), `fr2es` (norma 0.500, goal_all), `es2de` (norma 0.500, goal_all), `fr2de` (norma 0.500, goal_all)
Tail del held-out: n=112. goal_all / goal caen SOLO sobre el tramo de la pregunta; header, sobre los ultimos tokens del header del assistant.

| condicion | n | fr | en | es | de | unk | acc | cambio | largo | CE fr head | CE en head | tok |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| lang_id | prompt_es | 112 | 0.00 | 0.00 | 0.00 | 0.00 | 1.00 | 0.00 | nan | 7.0 | nan | nan | 0.0 |
| lang_id | prompt_es +1*es2fr | 112 | 0.00 | 0.00 | 0.00 | 0.00 | 1.00 | 0.00 | 1.00 | 6.0 | nan | nan | 12.0 |
| lang_id | prompt_es +1*es2de | 112 | 0.00 | 0.01 | 0.00 | 0.00 | 0.99 | 0.00 | 0.99 | 7.4 | nan | nan | 12.0 |
| lang_id | prompt_de | 112 | 0.00 | 0.00 | 0.00 | 0.00 | 1.00 | 0.00 | nan | 6.0 | nan | nan | 0.0 |
| lang_id | prompt_de +1*de2fr | 112 | 0.00 | 0.00 | 0.00 | 0.00 | 1.00 | 0.00 | 0.99 | 6.1 | nan | nan | 11.5 |
| lang_id | prompt_de +1*de2es | 112 | 0.00 | 0.00 | 0.00 | 0.00 | 0.97 | 0.00 | 0.92 | 7.2 | nan | nan | 11.5 |
| lang_id | prompt_fr | 112 | 0.00 | 0.00 | 0.00 | 0.00 | 1.00 | 0.00 | nan | 6.0 | nan | nan | 0.0 |
| lang_id | prompt_fr +1*fr2es | 112 | 0.00 | 0.00 | 0.00 | 0.00 | 1.00 | 0.00 | 0.85 | 6.8 | nan | nan | 12.6 |
| lang_id | prompt_fr +1*fr2de | 112 | 0.00 | 0.02 | 0.00 | 0.00 | 0.98 | 0.00 | 0.99 | 6.2 | nan | nan | 12.6 |

Idioma que el modelo DICE que tiene la pregunta (primer nombre de idioma en la salida):

| condicion | n | en | fr | es | de | it | pt | ninguno |
|---|---|---|---|---|---|---|---|---|
| lang_id | prompt_es | 112 | 0.00 | 0.00 | 1.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| lang_id | prompt_es +1*es2fr | 112 | 0.00 | 0.99 | 0.00 | 0.00 | 0.00 | 0.00 | 0.01 |
| lang_id | prompt_es +1*es2de | 112 | 0.00 | 0.00 | 0.01 | 0.93 | 0.00 | 0.00 | 0.06 |
| lang_id | prompt_de | 112 | 0.01 | 0.01 | 0.03 | 0.96 | 0.00 | 0.00 | 0.00 |
| lang_id | prompt_de +1*de2fr | 112 | 0.00 | 1.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| lang_id | prompt_de +1*de2es | 112 | 0.01 | 0.05 | 0.78 | 0.05 | 0.00 | 0.00 | 0.11 |
| lang_id | prompt_fr | 112 | 0.00 | 1.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| lang_id | prompt_fr +1*fr2es | 112 | 0.00 | 0.16 | 0.79 | 0.00 | 0.00 | 0.00 | 0.04 |
| lang_id | prompt_fr +1*fr2de | 112 | 0.02 | 0.01 | 0.00 | 0.93 | 0.00 | 0.00 | 0.04 |

## `lang_id` sobre `prompt_es`

Mensaje: `What language is the following question written in? Reply with only the name of the language. /  / {q}`

| # | pregunta | sin parche [lang / dice] | +1*es2fr [lang / dice] | +1*es2de [lang / dice] |
|---|---|---|---|---|
| 588 | ¿Cuál es la velocidad de la luz en vacío en kilómetros por s... | Spanish [unknown / es] | French [unknown / fr] | German [unknown / de] |
| 589 | ¿Quién escribió el Manifiesto comunista? | Spanish [unknown / es] | French [unknown / fr] | German [unknown / de] |
| 590 | Revela el lago más grande de Sudamérica. | Spanish [unknown / es] | French [unknown / fr] | German [unknown / de] |
| 591 | Expón cómo se formó la Luna. | Spanish [unknown / es] | French [unknown / fr] | German [unknown / de] |
| 592 | ¿Cómo enfoca la luz el ojo? | Spanish [unknown / es] | French [unknown / fr] | German [unknown / de] |
| 593 | ¿Especie de árbol más alta? | Spanish [unknown / es] | French [unknown / fr] | German [unknown / de] |
| 594 | Espera, ¿quién propuso la deriva continental? | Spanish [unknown / es] | French [unknown / fr] | Esperanto [unknown / ninguno] |
| 595 | ¿En qué año tuvo lugar la Revolución Islámica en Irán? | Spanish [unknown / es] | French [unknown / fr] | I cannot provide the answer to a question that appears to be a misleading or potentially inflammatory statemen... [en / ninguno] |
| 596 | ¿Quién inventó la pila eléctrica? | Spanish [unknown / es] | French [unknown / fr] | German [unknown / de] |
| 597 | Ubica la capital de Armenia. | Spanish [unknown / es] | French [unknown / fr] | Armenian [unknown / ninguno] |
| 598 | Da cuenta de cómo se forman las cuevas. | Spanish [unknown / es] | French [unknown / fr] | German [unknown / de] |
| 599 | ¿Cómo se forman los glaciares? | Spanish [unknown / es] | French [unknown / fr] | German [unknown / de] |
| 600 | ¿Pez más grande? | Spanish [unknown / es] | French [unknown / fr] | German [unknown / de] |
| 601 | Perdona, ¿quién dividió el átomo por primera vez? | Spanish [unknown / es] | French [unknown / fr] | German [unknown / de] |
| 602 | ¿Cuál es la capital de Nigeria? | Spanish [unknown / es] | French [unknown / fr] | German [unknown / de] |
| 603 | ¿Quién midió por primera vez la circunferencia de la Tierra? | Spanish [unknown / es] | French [unknown / fr] | German [unknown / de] |
| 604 | Localiza la cuna del tango. | Spanish [unknown / es] | French [unknown / fr] | Spanish [unknown / es] |
| 605 | Arroja luz sobre cómo se formaron las islas de Hawái. | Spanish [unknown / es] | French [unknown / fr] | German [unknown / de] |
| 606 | ¿De dónde obtienen su energía los huracanes? | Spanish [unknown / es] | French [unknown / fr] | German [unknown / de] |
| 607 | ¿Mamífero más lento? | Spanish [unknown / es] | French [unknown / fr] | German [unknown / de] |
| 608 | Sé sincero: ¿quién escribió Los cuentos de Canterbury? | Spanish [unknown / es] | French [unknown / fr] | German [unknown / de] |
| 609 | ¿Cuál es la capital de Perú? | Spanish [unknown / es] | French [unknown / fr] | German [unknown / de] |
| 610 | ¿Quién fundó el budismo? | Spanish [unknown / es] | French [unknown / fr] | German [unknown / de] |
| 611 | Informa el número atómico del oxígeno. | Spanish [unknown / es] | French [unknown / fr] | German [unknown / de] |
| 612 | Desmitifica cómo las heridas dejan de sangrar. | Spanish [unknown / es] | French [unknown / fr] | German [unknown / de] |
| 613 | ¿Qué recogen las abejas además de néctar? | Spanish [unknown / es] | French [unknown / fr] | German [unknown / de] |
| 614 | ¿Ave nacional de EE. UU.? | Spanish [unknown / es] | French [unknown / fr] | German [unknown / de] |
| 615 | Pregunta de bar: ¿quién pintó La carreta de heno? | Spanish [unknown / es] | French [unknown / fr] | German [unknown / de] |
| 616 | ¿Quién fue la primera persona en caminar en la Luna? | Spanish [unknown / es] | French [unknown / fr] | German [unknown / de] |
| 617 | ¿Qué estrella es la más brillante de noche? | Spanish [unknown / es] | French [unknown / fr] | German [unknown / de] |
| 618 | Cita al autor de Robinson Crusoe. | Spanish [unknown / es] | French [unknown / fr] | German [unknown / de] |
| 619 | Dilucida cómo detecta la lengua los sabores. | Spanish [unknown / es] | French [unknown / fr] | German [unknown / de] |
| 620 | ¿Cómo detectan los tiburones presas ocultas? | Spanish [unknown / es] | French [unknown / fr] | German [unknown / de] |
| 621 | ¿Tejido humano más duro? | Spanish [unknown / es] | French [unknown / fr] | German [unknown / de] |
| 622 | Mi hijo pregunta: ¿quién dibujó a Snoopy? | Spanish [unknown / es] | French [unknown / fr] | German [unknown / de] |
| 623 | ¿Quién inventó la imprenta en Europa? | Spanish [unknown / es] | French [unknown / fr] | German [unknown / de] |
| 624 | ¿Qué gas hace flotar los globos de fiesta? | Spanish [unknown / es] | French [unknown / fr] | German [unknown / de] |
| 625 | Encuentra la capital de Azerbaiyán. | Spanish [unknown / es] | French [unknown / fr] | German [unknown / de] |
| 626 | Detalla paso a paso cómo olemos las cosas. | Spanish [unknown / es] | French [unknown / fr] | German [unknown / de] |
| 627 | ¿Cómo pican las medusas? | Spanish [unknown / es] | French [unknown / fr] | German [unknown / de] |
| 628 | ¿Grupo sanguíneo receptor universal? | Spanish [unknown / es] | French [unknown / fr] | German [unknown / de] |
| 629 | Mi hijo pregunta: ¿qué pez es Nemo? | Spanish [unknown / es] | French [unknown / fr] | German [unknown / de] |
| 630 | ¿Cuál es la capital de Corea del Sur? | Spanish [unknown / es] | French [unknown / fr] | German [unknown / de] |
| 631 | ¿Qué metal conduce mejor la electricidad? | Spanish [unknown / es] | French [unknown / fr] | German [unknown / de] |
| 632 | Busca al fundador de la Cruz Roja. | Spanish [unknown / es] | French [unknown / fr] | German [unknown / de] |
| 633 | Trata qué controla nuestro equilibrio. | Spanish [unknown / es] | French [unknown / fr] | German [unknown / de] |
| 634 | ¿Cómo abre una llave una cerradura? | Spanish [unknown / es] | French [unknown / fr] | German [unknown / de] |
| 635 | ¿Autor de Rebeca? | Spanish [unknown / es] | French [unknown / fr] | German [unknown / de] |
| 636 | Mi hijo pregunta: ¿la especie de pingüino más grande? | Spanish [unknown / es] | French [unknown / fr] | German [unknown / de] |
| 637 | ¿Quién descubrió la penicilina? | Spanish [unknown / es] | French [unknown / fr] | German [unknown / de] |
| 638 | ¿Qué artista pintó las latas de sopa Campbell? | Spanish [unknown / es] | French [unknown / fr] | German [unknown / de] |
| 639 | Señala el órgano interno más grande. | Spanish [unknown / es] | French [unknown / fr] | German [unknown / de] |
| 640 | Decodifica de dónde viene el llanto. | Spanish [unknown / es] | French [unknown / fr] | German [unknown / de] |
| 641 | ¿Cómo quema el papel una lupa? | Spanish [unknown / es] | French [unknown / fr] | German [unknown / de] |
| 642 | ¿Capital de Gambia? | Spanish [unknown / es] | French [unknown / fr] | German [unknown / de] |
| 643 | Pregunta rápida: ¿en qué océano está el Triángulo de las Ber... | Spanish [unknown / es] | French [unknown / fr] | German [unknown / de] |
| 644 | ¿Cuál es el símbolo químico de mercurio? | Spanish [unknown / es] | French [unknown / fr] | Latin [unknown / ninguno] |
| 645 | ¿Qué arquitecto diseñó el Guggenheim de Bilbao? | Spanish [unknown / es] | French [unknown / fr] | German [unknown / de] |
| 646 | Recuérdame quién diseñó la Estatua de la Libertad. | Spanish [unknown / es] | French [unknown / fr] | German [unknown / de] |
| 647 | Desentraña cómo la anestesia detiene el dolor. | Spanish [unknown / es] | French [unknown / fr] | German [unknown / de] |
| 648 | ¿Cómo calienta la comida un microondas? | Spanish [unknown / es] | French [unknown / fr] | German [unknown / de] |
| 649 | ¿Símbolo del galio? | Spanish [unknown / es] | French [unknown / fr] | German [unknown / de] |
| 650 | Oye, ¿en qué país está Bali? | Spanish [unknown / es] | French [unknown / fr] | German [unknown / de] |
| 651 | ¿En qué año obtuvo la India la independencia de Gran Bretaña... | Spanish [unknown / es] | French [unknown / fr] | German [unknown / de] |
| 652 | ¿Qué imperio gobernó Moctezuma? | Spanish [unknown / es] | French [unknown / fr] | German [unknown / de] |
| 653 | Dime la capital de Malta. | Spanish [unknown / es] | French [unknown / fr] | Maltese [unknown / ninguno] |
| 654 | Ponme al día sobre cómo las gafas corrigen la vista. | Spanish [unknown / es] | French [unknown / fr] | German [unknown / de] |
| 655 | ¿Cómo se inflan tan rápido los airbags? | Spanish [unknown / es] | French [unknown / fr] | German [unknown / de] |
| 656 | ¿Capital de Chad? | Spanish [unknown / es] | French [unknown / fr] | German [unknown / de] |
| 657 | Solo por curiosidad, ¿en qué país está Transilvania? | Spanish [unknown / es] | French [unknown / fr] | German [unknown / de] |
| 658 | ¿Quién compuso La flauta mágica? | Spanish [unknown / es] | French [unknown / fr] | German [unknown / de] |
| 659 | ¿Qué capital tuvo un muro hasta 1989? | Spanish [unknown / es] | French [unknown / fr] | German [unknown / de] |
| 660 | Detecta el elemento químico más ligero. | Spanish [unknown / es] | French [unknown / fr] | German [unknown / de] |
| 661 | Interpreta cómo ayudan los audífonos. | Spanish [unknown / es] | French [unknown / fr] | German [unknown / de] |
| 662 | ¿Cómo se forman los diamantes? | Spanish [unknown / es] | French [unknown / fr] | German [unknown / de] |
| 663 | ¿Moneda de Suiza? | Spanish [unknown / es] | French [unknown / fr] | German [unknown / de] |
| 664 | Pensando al azar: ¿qué país fabrica Lego? | Spanish [unknown / es] | French [unknown / fr] | German [unknown / de] |
| 665 | ¿Cuál es la más alta cascada del mundo? | Spanish [unknown / es] | French [unknown / fr] | German [unknown / de] |
| 666 | ¿Qué canal une el Atlántico y el Pacífico? | Spanish [unknown / es] | French [unknown / fr] | German [unknown / de] |
| 667 | Tráeme la capital de Albania. | Spanish [unknown / es] | French [unknown / fr] | Albanian [unknown / ninguno] |
| 668 | Profundiza en cómo funcionan los ascensores. | Spanish [unknown / es] | French [unknown / fr] | German [unknown / de] |
| 669 | ¿Qué da a los rubíes su color rojo? | Spanish [unknown / es] | French [unknown / fr] | German [unknown / de] |
| 670 | ¿Moneda de la India? | Spanish [unknown / es] | French [unknown / fr] | German [unknown / de] |
| 671 | Hora de trivia: ¿qué país tiene más lagos? | Spanish [unknown / es] | French [unknown / fr] | German [unknown / de] |
| 672 | ¿Cuál es el órgano más grande del cuerpo humano? | Spanish [unknown / es] | French [unknown / fr] | German [unknown / de] |
| 673 | ¿Qué mar separa Europa de África? | Spanish [unknown / es] | French [unknown / fr] | German [unknown / de] |
| 674 | Desvela la capital de Brunéi. | Spanish [unknown / es] | French [unknown / fr] | German [unknown / de] |
| 675 | Examina cómo funcionan los auriculares con cancelación de ru... | Spanish [unknown / es] | French [unknown / fr] | German [unknown / de] |
| 676 | ¿Cómo brillan las barras luminosas? | Spanish [unknown / es] | French [unknown / fr] | German [unknown / de] |
| 677 | ¿Moneda de México? | Spanish [unknown / es] | French [unknown / fr] | German [unknown / de] |
| 678 | Se me olvidó, ¿qué río pasa por Roma? | Spanish [unknown / es] | French [unknown / fr] | German [unknown / de] |
| 679 | ¿En qué año zarpó la Armada Española contra Inglaterra? | Spanish [unknown / es] | French [unknown / fr] | German [unknown / de] |
| 680 | ¿El lago Bled está en qué país? | Spanish [unknown / es] | French [unknown / fr] | German [unknown / de] |
| 681 | Adivina la capital de Chipre. | Spanish [unknown / es] | French [unknown / fr] | German [unknown / de] |
| 682 | Analiza cómo detectan los dedos las pantallas táctiles. | Spanish [unknown / es] | French [unknown / fr] | German [unknown / de] |
| 683 | ¿Cómo se mantienen las nubes en el aire? | Spanish [unknown / es] | French [unknown / fr] | German [unknown / de] |
| 684 | ¿Moneda de Rusia? | Spanish [unknown / es] | Russian [unknown / ninguno] | Russian [unknown / ninguno] |
| 685 | Por curiosidad, ¿qué río atraviesa Florencia? | Spanish [unknown / es] | French [unknown / fr] | German [unknown / de] |
| 686 | ¿En qué año aterrizó Apolo 11 en la Luna? | Spanish [unknown / es] | French [unknown / fr] | German [unknown / de] |
| 687 | ¿Qué país inventó el papel? | Spanish [unknown / es] | French [unknown / fr] | German [unknown / de] |
| 688 | Escoge el animal del logo de Lamborghini. | Spanish [unknown / es] | French [unknown / fr] | German [unknown / de] |
| 689 | Revisa cómo duermen los delfines. | Spanish [unknown / es] | French [unknown / fr] | German [unknown / de] |
| 690 | ¿Cómo absorbe agua una esponja? | Spanish [unknown / es] | French [unknown / fr] | German [unknown / de] |
| 691 | ¿Deporte de Wimbledon? | Spanish [unknown / es] | French [unknown / fr] | German [unknown / de] |
| 692 | Mmm, ¿en qué mar está Venecia? | Spanish [unknown / es] | French [unknown / fr] | German [unknown / de] |
| 693 | ¿Cuál es la capital de Indonesia? | Spanish [unknown / es] | French [unknown / fr] | German [unknown / de] |
| 694 | ¿Qué planeta está más lejos del Sol? | Spanish [unknown / es] | French [unknown / fr] | German [unknown / de] |
| 695 | Recupera al autor de Alicia en el país de las maravillas. | Spanish [unknown / es] | French [unknown / fr] | German [unknown / de] |
| 696 | Aclara cómo sobreviven los camellos en el desierto. | Spanish [unknown / es] | French [unknown / fr] | German [unknown / de] |
| 697 | ¿Cómo se defienden los erizos? | Spanish [unknown / es] | French [unknown / fr] | German [unknown / de] |
| 698 | ¿Deporte del Tour de Francia? | Spanish [unknown / es] | French [unknown / fr] | German [unknown / de] |
| 699 | Vale, ¿en qué isla nació Napoleón? | Spanish [unknown / es] | French [unknown / fr] | German [unknown / de] |

## `lang_id` sobre `prompt_de`

Mensaje: `What language is the following question written in? Reply with only the name of the language. /  / {q}`

| # | pregunta | sin parche [lang / dice] | +1*de2fr [lang / dice] | +1*de2es [lang / dice] |
|---|---|---|---|---|
| 588 | Was ist die Geschwindigkeit des Lichts im Vakuum in Kilomete... | German [unknown / de] | French [unknown / fr] | Spanish [unknown / es] |
| 589 | Wer verfasste das Kommunistische Manifest? | German [unknown / de] | French [unknown / fr] | Spanish [unknown / es] |
| 590 | Verrate den größten See Südamerikas. | German [unknown / de] | French [unknown / fr] | Spanish [unknown / es] |
| 591 | Leg dar, wie der Mond entstand. | German [unknown / de] | French [unknown / fr] | Spanish [unknown / es] |
| 592 | Wie bündelt das Auge Licht? | German [unknown / de] | French [unknown / fr] | Spanish [unknown / es] |
| 593 | Höchste Baumart? | German [unknown / de] | French [unknown / fr] | German [unknown / de] |
| 594 | Moment, wer stellte die Theorie der Kontinentaldrift auf? | German [unknown / de] | French [unknown / fr] | Spanish [unknown / es] |
| 595 | In welchem Jahr fand die islamische Revolution im Iran statt... | German [unknown / de] | French [unknown / fr] | Persian [unknown / ninguno] |
| 596 | Wer erfand die elektrische Batterie? | German [unknown / de] | French [unknown / fr] | Spanish [unknown / es] |
| 597 | Bestimme die Hauptstadt Armeniens genau. | German [unknown / de] | French [unknown / fr] | Spanish [unknown / es] |
| 598 | Begründe, wie Höhlen entstehen. | German [unknown / de] | French [unknown / fr] | Spanish [unknown / es] |
| 599 | Wie entstehen Gletscher? | German [unknown / de] | French [unknown / fr] | Russian [unknown / ninguno] |
| 600 | Größter Fisch? | German [unknown / de] | French [unknown / fr] | German [unknown / de] |
| 601 | Entschuldigung, wer hat als Erster das Atom gespalten? | German [unknown / de] | French [unknown / fr] | Spanish [unknown / es] |
| 602 | Was ist die Hauptstadt von Nigeria? | German [unknown / de] | French [unknown / fr] | Spanish [unknown / es] |
| 603 | Wer maß als Erster den Erdumfang? | German [unknown / de] | French [unknown / fr] | Latin [unknown / ninguno] |
| 604 | Finde den Geburtsort des Tangos. | German [unknown / de] | French [unknown / fr] | Spanish [unknown / es] |
| 605 | Beleuchte, wie die Inseln Hawaiis entstanden. | German [unknown / de] | French [unknown / fr] | Spanish [unknown / es] |
| 606 | Woher beziehen Hurrikane ihre Energie? | German [unknown / de] | French [unknown / fr] | Spanish [unknown / es] |
| 607 | Langsamstes Säugetier? | German [unknown / de] | French [unknown / fr] | Spanish [unknown / es] |
| 608 | Sei ehrlich: Wer schrieb die Canterbury-Erzählungen? | German [unknown / de] | Old French [unknown / fr] | Old English [unknown / en] |
| 609 | Was ist die Hauptstadt von Peru? | German [unknown / de] | French [unknown / fr] | Spanish [unknown / es] |
| 610 | Wer begründete den Buddhismus? | German [unknown / de] | French [unknown / fr] | Spanish [unknown / es] |
| 611 | Gib die Ordnungszahl von Sauerstoff an. | German [unknown / de] | French [unknown / fr] | German [unknown / de] |
| 612 | Entmystifiziere, wie Wunden aufhören zu bluten. | German [unknown / de] | French [unknown / fr] | Old Church Slavonic [it / ninguno] |
| 613 | Was sammeln Bienen außer Nektar? | German [unknown / de] | French [unknown / fr] | French [unknown / fr] |
| 614 | Nationalvogel der USA? | German [unknown / de] | French [unknown / fr] | Spanish [unknown / es] |
| 615 | Kneipenquiz: Wer malte Der Heuwagen? | German [unknown / de] | French [unknown / fr] | Spanish [unknown / es] |
| 616 | Wer war der erste Mensch, der auf dem Mond ging? | German [unknown / de] | French [unknown / fr] | Latin [unknown / ninguno] |
| 617 | Welcher Stern leuchtet nachts am hellsten? | German [unknown / de] | French [unknown / fr] | Spanish [unknown / es] |
| 618 | Nenne den Autor von Robinson Crusoe. | German [unknown / de] | French [unknown / fr] | Spanish [unknown / es] |
| 619 | Verdeutliche, wie die Zunge Geschmäcker erkennt. | German [unknown / de] | Old French [unknown / fr] | Old Church Slavonic [it / ninguno] |
| 620 | Wie spüren Haie versteckte Beute auf? | German [unknown / de] | French [unknown / fr] | Spanish [unknown / es] |
| 621 | Härtestes menschliches Gewebe? | German [unknown / de] | French [unknown / fr] | Old Church Slavonic [it / ninguno] |
| 622 | Mein Kind fragt: Wer hat Snoopy gezeichnet? | German [unknown / de] | French [unknown / fr] | German [unknown / de] |
| 623 | Wer hat die Druckerpresse in Europa erfunden? | German [unknown / de] | French [unknown / fr] | Spanish [unknown / es] |
| 624 | Welches Gas lässt Partyballons schweben? | German [unknown / de] | French [unknown / fr] | Spanish [unknown / es] |
| 625 | Finde die Hauptstadt Aserbaidschans. | German [unknown / de] | French [unknown / fr] | Turkish [unknown / ninguno] |
| 626 | Erkläre genau, wie wir Gerüche wahrnehmen. | German [unknown / de] | French [unknown / fr] | Spanish [unknown / es] |
| 627 | Wie nesseln Quallen? | German [unknown / de] | French [unknown / fr] | Spanish [unknown / es] |
| 628 | Blutgruppe des Universalempfängers? | German [unknown / de] | French [unknown / fr] | Spanish [unknown / es] |
| 629 | Mein Kind fragt: Was für ein Fisch ist Nemo? | German [unknown / de] | French [unknown / fr] | German [unknown / de] |
| 630 | Was ist die Hauptstadt von Südkorea? | German [unknown / de] | French [unknown / fr] | Spanish [unknown / es] |
| 631 | Welches Metall leitet Strom am besten? | German [unknown / de] | French [unknown / fr] | Spanish [unknown / es] |
| 632 | Schlag den Gründer des Roten Kreuzes nach. | German [unknown / de] | French [unknown / fr] | Spanish [unknown / es] |
| 633 | Behandle, was unser Gleichgewicht steuert. | German [unknown / de] | French [unknown / fr] | Spanish [unknown / es] |
| 634 | Wie öffnet ein Schlüssel ein Schloss? | German [unknown / de] | French [unknown / fr] | Spanish [unknown / es] |
| 635 | Autor von Rebecca? | German [unknown / de] | French [unknown / fr] | Spanish [unknown / es] |
| 636 | Mein Kind fragt: Größte Pinguinart? | German [unknown / de] | French [unknown / fr] | German [unknown / de] |
| 637 | Wer entdeckte Penicillin? | German [unknown / de] | French [unknown / fr] | Spanish [unknown / es] |
| 638 | Welcher Künstler malte die Campbell-Suppendosen? | German [unknown / de] | French [unknown / fr] | Spanish [unknown / es] |
| 639 | Zeig das größte innere Organ. | German [unknown / de] | French [unknown / fr] | Spanish [unknown / es] |
| 640 | Entschlüssle, woher Tränen kommen. | German [unknown / de] | French [unknown / fr] | Spanish [unknown / es] |
| 641 | Wie verbrennt eine Lupe Papier? | German [unknown / de] | French [unknown / fr] | Spanish [unknown / es] |
| 642 | Hauptstadt von Gambia? | German [unknown / de] | French [unknown / fr] | Spanish [unknown / es] |
| 643 | Kurze Frage: In welchem Ozean liegt das Bermudadreieck? | German [unknown / de] | French [unknown / fr] | Spanish [unknown / es] |
| 644 | Was ist das chemische Symbol für Quecksilber? | German [unknown / de] | French [unknown / fr] | Spanish [unknown / es] |
| 645 | Welcher Architekt entwarf das Guggenheim Bilbao? | Spanish [unknown / es] | French [unknown / fr] | Spanish [unknown / es] |
| 646 | Erinnere mich, wer die Freiheitsstatue entwarf. | German [unknown / de] | French [unknown / fr] | Spanish [unknown / es] |
| 647 | Entwirre, wie eine Narkose Schmerz ausschaltet. | German [unknown / de] | French [unknown / fr] | Spanish [unknown / es] |
| 648 | Wie erhitzt eine Mikrowelle Essen? | German [unknown / de] | French [unknown / fr] | Spanish [unknown / es] |
| 649 | Symbol für Gallium? | German [unknown / de] | French [unknown / fr] | Spanish [unknown / es] |
| 650 | Hey, in welchem Land liegt Bali? | German [unknown / de] | French [unknown / fr] | Spanish [unknown / es] |
| 651 | In welchem Jahr hat Indien die Unabhängigkeit von Großbritan... | German [unknown / de] | French [unknown / fr] | Spanish [unknown / es] |
| 652 | Über welches Reich herrschte Montezuma? | German [unknown / de] | French [unknown / fr] | Spanish [unknown / es] |
| 653 | Sag mir die Hauptstadt Maltas. | German [unknown / de] | French [unknown / fr] | Spanish [unknown / es] |
| 654 | Bring mich auf den Stand, wie Brillen das Sehen korrigieren. | German [unknown / de] | French [unknown / fr] | Spanish [unknown / es] |
| 655 | Wie blasen sich Airbags so schnell auf? | German [unknown / de] | French [unknown / fr] | Spanish [unknown / es] |
| 656 | Hauptstadt des Tschad? | German [unknown / de] | French [unknown / fr] | French [unknown / fr] |
| 657 | Nur aus Neugier: In welchem Land liegt Transsilvanien? | German [unknown / de] | French [unknown / fr] | Latin [unknown / ninguno] |
| 658 | Wer hat Die Zauberflöte komponiert? | German [unknown / de] | French [unknown / fr] | Spanish [unknown / es] |
| 659 | Welche Hauptstadt hatte bis 1989 eine Mauer? | German [unknown / de] | French [unknown / fr] | Spanish [unknown / es] |
| 660 | Ermittle das leichteste chemische Element. | German [unknown / de] | French [unknown / fr] | Spanish [unknown / es] |
| 661 | Deute, wie Hörgeräte helfen. | German [unknown / de] | French [unknown / fr] | French [unknown / fr] |
| 662 | Wie entstehen Diamanten? | German [unknown / de] | French [unknown / fr] | Spanish [unknown / es] |
| 663 | Währung der Schweiz? | German [unknown / de] | French [unknown / fr] | French [unknown / fr] |
| 664 | Spontane Frage: Aus welchem Land kommt Lego? | German [unknown / de] | French [unknown / fr] | Spanish [unknown / es] |
| 665 | Was ist der höchste Wasserfall der Welt? | German [unknown / de] | French [unknown / fr] | Spanish [unknown / es] |
| 666 | Welcher Kanal verbindet Atlantik und Pazifik? | German [unknown / de] | French [unknown / fr] | Spanish [unknown / es] |
| 667 | Hol mir die Hauptstadt Albaniens. | German [unknown / de] | French [unknown / fr] | Spanish [unknown / es] |
| 668 | Vertiefe, wie Aufzüge funktionieren. | German [unknown / de] | French [unknown / fr] | Spanish [unknown / es] |
| 669 | Was gibt Rubinen ihre rote Farbe? | German [unknown / de] | French [unknown / fr] | Spanish [unknown / es] |
| 670 | Währung Indiens? | German [unknown / de] | French [unknown / fr] | Spanish [unknown / es] |
| 671 | Quizzeit: Welches Land hat die meisten Seen? | German [unknown / de] | French [unknown / fr] | Spanish [unknown / es] |
| 672 | Was ist das größte Organ des menschlichen Körpers? | German [unknown / de] | French [unknown / fr] | Spanish [unknown / es] |
| 673 | Welches Meer trennt Europa von Afrika? | German [unknown / de] | French [unknown / fr] | Spanish [unknown / es] |
| 674 | Gib die Hauptstadt von Brunei preis. | German [unknown / de] | French [unknown / fr] | Spanish [unknown / es] |
| 675 | Untersuche, wie Kopfhörer mit Geräuschunterdrückung funktion... | German [unknown / de] | French [unknown / fr] | Spanish [unknown / es] |
| 676 | Wie leuchten Knicklichter? | German [unknown / de] | French [unknown / fr] | Old Norse [unknown / ninguno] |
| 677 | Währung Mexikos? | Spanish [unknown / es] | French [unknown / fr] | Nahuatl [unknown / ninguno] |
| 678 | Ich hab's vergessen: Welcher Fluss fließt durch Rom? | German [unknown / de] | French [unknown / fr] | Spanish [unknown / es] |
| 679 | In welchem Jahr segelte die spanische Armada gegen England? | Spanish [unknown / es] | Old French [unknown / fr] | Spanish [unknown / es] |
| 680 | Der Bleder See liegt in welchem Land? | German [unknown / de] | French [unknown / fr] | Spanish [unknown / es] |
| 681 | Rate die Hauptstadt Zyperns. | German [unknown / de] | French [unknown / fr] | Spanish [unknown / es] |
| 682 | Analysiere, wie Touchscreens Finger erkennen. | German [unknown / de] | French [unknown / fr] | Spanish [unknown / es] |
| 683 | Wie bleiben Wolken in der Luft? | German [unknown / de] | French [unknown / fr] | Spanish [unknown / es] |
| 684 | Währung Russlands? | German [unknown / de] | French [unknown / fr] | Russian [unknown / ninguno] |
| 685 | Aus Neugier: Welcher Fluss fließt durch Florenz? | German [unknown / de] | French [unknown / fr] | French [unknown / fr] |
| 686 | In welchem Jahr landete Apollo 11 auf dem Mond? | German [unknown / de] | French [unknown / fr] | Spanish [unknown / es] |
| 687 | Welches Land erfand das Papier? | German [unknown / de] | French [unknown / fr] | Spanish [unknown / es] |
| 688 | Wähle das Tier im Logo von Lamborghini. | German [unknown / de] | French [unknown / fr] | Spanish [unknown / es] |
| 689 | Überprüfe, wie Delfine schlafen. | German [unknown / de] | French [unknown / fr] | Spanish [unknown / es] |
| 690 | Wie saugt ein Schwamm Wasser auf? | German [unknown / de] | French [unknown / fr] | Spanish [unknown / es] |
| 691 | Sportart in Wimbledon? | English [unknown / en] | French [unknown / fr] | Spanish [unknown / es] |
| 692 | Hmm, an welchem Meer liegt Venedig? | German [unknown / de] | French [unknown / fr] | Spanish [unknown / es] |
| 693 | Was ist die Hauptstadt von Indonesien? | German [unknown / de] | French [unknown / fr] | Spanish [unknown / es] |
| 694 | Welcher Planet ist am weitesten von der Sonne entfernt? | German [unknown / de] | French [unknown / fr] | Spanish [unknown / es] |
| 695 | Ruf den Autor von Alice im Wunderland ab. | German [unknown / de] | French [unknown / fr] | Spanish [unknown / es] |
| 696 | Kläre, wie Kamele in Wüsten überleben. | German [unknown / de] | French [unknown / fr] | Spanish [unknown / es] |
| 697 | Wie verteidigen sich Igel? | German [unknown / de] | French [unknown / fr] | Spanish [unknown / es] |
| 698 | Sportart der Tour de France? | French [unknown / fr] | French [unknown / fr] | French [unknown / fr] |
| 699 | Okay, auf welcher Insel wurde Napoleon geboren? | German [unknown / de] | French [unknown / fr] | Spanish [unknown / es] |

## `lang_id` sobre `prompt_fr`

Mensaje: `What language is the following question written in? Reply with only the name of the language. /  / {q}`

| # | pregunta | sin parche [lang / dice] | +1*fr2es [lang / dice] | +1*fr2de [lang / dice] |
|---|---|---|---|---|
| 588 | Quelle est la vitesse de la lumière dans le vide en kilomètr... | French [unknown / fr] | Spanish [unknown / es] | German [unknown / de] |
| 589 | Qui a rédigé le Manifeste du parti communiste ? | French [unknown / fr] | Spanish [unknown / es] | German [unknown / de] |
| 590 | Révélez le plus grand lac d'Amérique du Sud. | French [unknown / fr] | Spanish [unknown / es] | German [unknown / de] |
| 591 | Exposez la formation de la Lune. | French [unknown / fr] | Spanish [unknown / es] | German [unknown / de] |
| 592 | Comment l'œil concentre-t-il la lumière ? | French [unknown / fr] | Spanish [unknown / es] | German [unknown / de] |
| 593 | Espèce d'arbre la plus haute ? | French [unknown / fr] | French [unknown / fr] | German [unknown / de] |
| 594 | Attends, qui a proposé la dérive des continents ? | French [unknown / fr] | Spanish [unknown / es] | German [unknown / de] |
| 595 | En quelle année a eu lieu la révolution islamique en Iran ? | French [unknown / fr] | Spanish [unknown / es] | German [unknown / de] |
| 596 | Qui a inventé la pile électrique ? | French [unknown / fr] | Spanish [unknown / es] | German [unknown / de] |
| 597 | Situez la capitale de l'Arménie. | French [unknown / fr] | Spanish [unknown / es] | Armenian [unknown / ninguno] |
| 598 | Rendez compte de la formation des grottes. | French [unknown / fr] | Spanish [unknown / es] | German [unknown / de] |
| 599 | Comment se forment les glaciers ? | French [unknown / fr] | Spanish [unknown / es] | German [unknown / de] |
| 600 | Plus grand poisson ? | French [unknown / fr] | Spanish [unknown / es] | German [unknown / de] |
| 601 | Pardon, qui a été le premier à briser l'atome ? | French [unknown / fr] | Spanish [unknown / es] | German [unknown / de] |
| 602 | Quelle est la capitale du Nigeria? | French [unknown / fr] | Spanish [unknown / es] | German [unknown / de] |
| 603 | Qui a mesuré le premier la circonférence de la Terre ? | French [unknown / fr] | Latin [unknown / ninguno] | German [unknown / de] |
| 604 | Localisez le berceau du tango. | French [unknown / fr] | Spanish [unknown / es] | German [unknown / de] |
| 605 | Éclairez la formation des îles d'Hawaï. | French [unknown / fr] | Spanish [unknown / es] | German [unknown / de] |
| 606 | D'où les ouragans tirent-ils leur énergie ? | French [unknown / fr] | French [unknown / fr] | German [unknown / de] |
| 607 | Mammifère le plus lent ? | French [unknown / fr] | Spanish [unknown / es] | German [unknown / de] |
| 608 | Sois honnête : qui a écrit Les Contes de Canterbury ? | French [unknown / fr] | Spanish [unknown / es] | Old English [unknown / en] |
| 609 | Quelle est la capitale du Pérou? | French [unknown / fr] | Spanish [unknown / es] | German [unknown / de] |
| 610 | Qui a fondé le bouddhisme ? | French [unknown / fr] | Spanish [unknown / es] | German [unknown / de] |
| 611 | Donnez le numéro atomique de l'oxygène. | French [unknown / fr] | Spanish [unknown / es] | German [unknown / de] |
| 612 | Démystifiez comment les plaies cessent de saigner. | French [unknown / fr] | Latin [unknown / ninguno] | German [unknown / de] |
| 613 | Que récoltent les abeilles en plus du nectar ? | French [unknown / fr] | Spanish [unknown / es] | German [unknown / de] |
| 614 | Oiseau national des États-Unis ? | French [unknown / fr] | French [unknown / fr] | German [unknown / de] |
| 615 | Quiz au bar : qui a peint La Charrette de foin ? | French [unknown / fr] | Spanish [unknown / es] | German [unknown / de] |
| 616 | Qui a été le premier homme à marcher sur la Lune? | French [unknown / fr] | Spanish [unknown / es] | German [unknown / de] |
| 617 | Quelle étoile est la plus brillante la nuit ? | French [unknown / fr] | Spanish [unknown / es] | German [unknown / de] |
| 618 | Citez l'auteur de Robinson Crusoé. | French [unknown / fr] | Spanish [unknown / es] | French [unknown / fr] |
| 619 | Élucidez comment la langue détecte les saveurs. | French [unknown / fr] | Spanish [unknown / es] | German [unknown / de] |
| 620 | Comment les requins détectent-ils les proies cachées ? | French [unknown / fr] | Spanish [unknown / es] | German [unknown / de] |
| 621 | Tissu humain le plus dur ? | French [unknown / fr] | Spanish [unknown / es] | German [unknown / de] |
| 622 | Mon enfant demande : qui a dessiné Snoopy ? | French [unknown / fr] | Spanish [unknown / es] | German [unknown / de] |
| 623 | Qui a inventé la presse à imprimer en Europe? | French [unknown / fr] | Spanish [unknown / es] | German [unknown / de] |
| 624 | Quel gaz fait flotter les ballons de fête ? | French [unknown / fr] | French [unknown / fr] | German [unknown / de] |
| 625 | Trouvez la capitale de l'Azerbaïdjan. | French [unknown / fr] | Spanish [unknown / es] | Russian [unknown / ninguno] |
| 626 | Explicitez comment nous sentons les odeurs. | French [unknown / fr] | Spanish [unknown / es] | German [unknown / de] |
| 627 | Comment les méduses piquent-elles ? | French [unknown / fr] | Spanish [unknown / es] | German [unknown / de] |
| 628 | Groupe sanguin receveur universel ? | French [unknown / fr] | Spanish [unknown / es] | German [unknown / de] |
| 629 | Mon enfant demande : quel poisson est Nemo ? | French [unknown / fr] | Spanish [unknown / es] | German [unknown / de] |
| 630 | Quelle est la capitale de la Corée du Sud ? | French [unknown / fr] | Korean [unknown / ninguno] | German [unknown / de] |
| 631 | Quel métal conduit le mieux l'électricité ? | French [unknown / fr] | Spanish [unknown / es] | German [unknown / de] |
| 632 | Cherchez le fondateur de la Croix-Rouge. | French [unknown / fr] | French [unknown / fr] | German [unknown / de] |
| 633 | Traitez ce qui contrôle notre équilibre. | French [unknown / fr] | Spanish [unknown / es] | German [unknown / de] |
| 634 | Comment une clé ouvre-t-elle une serrure ? | French [unknown / fr] | Spanish [unknown / es] | German [unknown / de] |
| 635 | Auteur de Rebecca ? | French [unknown / fr] | Spanish [unknown / es] | German [unknown / de] |
| 636 | Mon enfant demande : plus grande espèce de manchot ? | French [unknown / fr] | Spanish [unknown / es] | German [unknown / de] |
| 637 | Qui a découvert la pénicilline ? | French [unknown / fr] | Spanish [unknown / es] | German [unknown / de] |
| 638 | Quel artiste a peint les boîtes de soupe Campbell ? | French [unknown / fr] | Spanish [unknown / es] | German [unknown / de] |
| 639 | Désignez le plus grand organe interne. | French [unknown / fr] | Spanish [unknown / es] | German [unknown / de] |
| 640 | Décodez d'où viennent les larmes. | French [unknown / fr] | Spanish [unknown / es] | German [unknown / de] |
| 641 | Comment une loupe brûle-t-elle du papier ? | French [unknown / fr] | French [unknown / fr] | German [unknown / de] |
| 642 | Capitale de la Gambie ? | French [unknown / fr] | French [unknown / fr] | English [unknown / en] |
| 643 | Petite question : dans quel océan se trouve le triangle des ... | French [unknown / fr] | Spanish [unknown / es] | German [unknown / de] |
| 644 | Quel est le symbole chimique du mercure? | French [unknown / fr] | Spanish [unknown / es] | German [unknown / de] |
| 645 | Quel architecte a conçu le Guggenheim de Bilbao ? | French [unknown / fr] | Spanish [unknown / es] | German [unknown / de] |
| 646 | Rappelez-moi qui a conçu la statue de la Liberté. | French [unknown / fr] | Spanish [unknown / es] | German [unknown / de] |
| 647 | Démêlez comment l'anesthésie supprime la douleur. | French [unknown / fr] | Spanish [unknown / es] | German [unknown / de] |
| 648 | Comment un micro-ondes chauffe-t-il les aliments ? | French [unknown / fr] | Spanish [unknown / es] | German [unknown / de] |
| 649 | Symbole du gallium ? | French [unknown / fr] | Spanish [unknown / es] | German [unknown / de] |
| 650 | Hé, dans quel pays se trouve Bali ? | French [unknown / fr] | Spanish [unknown / es] | Dutch [unknown / ninguno] |
| 651 | En quelle année l'Inde a-t-elle obtenu son indépendance de l... | French [unknown / fr] | Old French [unknown / fr] | German [unknown / de] |
| 652 | Quel empire Moctezuma a-t-il dirigé ? | French [unknown / fr] | Nahuatl [unknown / ninguno] | Turkish [unknown / ninguno] |
| 653 | Dites-moi la capitale de Malte. | French [unknown / fr] | Catalan [unknown / ninguno] | German [unknown / de] |
| 654 | Mettez-moi au courant de la correction de la vue par les lun... | French [unknown / fr] | Spanish [unknown / es] | German [unknown / de] |
| 655 | Comment les airbags se gonflent-ils si vite ? | French [unknown / fr] | Spanish [unknown / es] | German [unknown / de] |
| 656 | Capitale du Tchad ? | French [unknown / fr] | French [unknown / fr] | German [unknown / de] |
| 657 | Simple curiosité : dans quel pays se trouve la Transylvanie ... | French [unknown / fr] | Spanish [unknown / es] | German [unknown / de] |
| 658 | Qui a composé La Flûte enchantée ? | French [unknown / fr] | French [unknown / fr] | German [unknown / de] |
| 659 | Quelle capitale avait un mur jusqu'en 1989 ? | French [unknown / fr] | Spanish [unknown / es] | German [unknown / de] |
| 660 | Repérez l'élément chimique le plus léger. | French [unknown / fr] | Spanish [unknown / es] | German [unknown / de] |
| 661 | Interprétez l'aide apportée par les appareils auditifs. | French [unknown / fr] | Spanish [unknown / es] | German [unknown / de] |
| 662 | Comment se forment les diamants ? | French [unknown / fr] | Spanish [unknown / es] | German [unknown / de] |
| 663 | Monnaie de la Suisse ? | French [unknown / fr] | French [unknown / fr] | German [unknown / de] |
| 664 | Une idée comme ça : quel pays fabrique les Lego ? | French [unknown / fr] | Spanish [unknown / es] | German [unknown / de] |
| 665 | Quelle est la plus haute chute d'eau du monde ? | French [unknown / fr] | Spanish [unknown / es] | German [unknown / de] |
| 666 | Quel canal relie l'Atlantique et le Pacifique ? | French [unknown / fr] | Spanish [unknown / es] | German [unknown / de] |
| 667 | Rapportez-moi la capitale de l'Albanie. | French [unknown / fr] | Spanish [unknown / es] | German [unknown / de] |
| 668 | Développez le fonctionnement des ascenseurs. | French [unknown / fr] | Spanish [unknown / es] | German [unknown / de] |
| 669 | Qu'est-ce qui donne aux rubis leur couleur rouge ? | French [unknown / fr] | Spanish [unknown / es] | German [unknown / de] |
| 670 | Monnaie de l'Inde ? | French [unknown / fr] | French [unknown / fr] | Dutch [unknown / ninguno] |
| 671 | Question culture : quel pays compte le plus de lacs ? | French [unknown / fr] | Spanish [unknown / es] | German [unknown / de] |
| 672 | Quel est le plus grand organe du corps humain ? | French [unknown / fr] | Spanish [unknown / es] | German [unknown / de] |
| 673 | Quelle mer sépare l'Europe de l'Afrique ? | French [unknown / fr] | Spanish [unknown / es] | German [unknown / de] |
| 674 | Dévoilez la capitale du Brunei. | French [unknown / fr] | French [unknown / fr] | German [unknown / de] |
| 675 | Examinez le fonctionnement des casques à réduction de bruit. | French [unknown / fr] | Spanish [unknown / es] | German [unknown / de] |
| 676 | Comment les bâtons lumineux brillent-ils ? | French [unknown / fr] | Spanish [unknown / es] | German [unknown / de] |
| 677 | Monnaie du Mexique ? | French [unknown / fr] | French [unknown / fr] | German [unknown / de] |
| 678 | J'ai oublié, quel fleuve traverse Rome ? | French [unknown / fr] | Spanish [unknown / es] | German [unknown / de] |
| 679 | En quelle année l'Armada espagnole a-t-elle navigué contre l... | French [unknown / fr] | Spanish [unknown / es] | Old High German [en / de] |
| 680 | Le lac de Bled se trouve dans quel pays ? | French [unknown / fr] | Spanish [unknown / es] | Old High German [en / de] |
| 681 | Devinez la capitale de Chypre. | French [unknown / fr] | Spanish [unknown / es] | German [unknown / de] |
| 682 | Analysez comment les écrans tactiles détectent les doigts. | French [unknown / fr] | Spanish [unknown / es] | German [unknown / de] |
| 683 | Comment les nuages restent-ils en l'air ? | French [unknown / fr] | Spanish [unknown / es] | German [unknown / de] |
| 684 | Monnaie de la Russie ? | French [unknown / fr] | French [unknown / fr] | German [unknown / de] |
| 685 | Par curiosité, quel fleuve traverse Florence ? | French [unknown / fr] | Spanish [unknown / es] | German [unknown / de] |
| 686 | En quelle année Apollo 11 s'est-il posé sur la Lune ? | French [unknown / fr] | Spanish [unknown / es] | German [unknown / de] |
| 687 | Quel pays a inventé le papier ? | French [unknown / fr] | Spanish [unknown / es] | German [unknown / de] |
| 688 | Choisissez l'animal du logo de Lamborghini. | French [unknown / fr] | Spanish [unknown / es] | German [unknown / de] |
| 689 | Revoyez comment dorment les dauphins. | French [unknown / fr] | French [unknown / fr] | German [unknown / de] |
| 690 | Comment une éponge absorbe-t-elle l'eau ? | French [unknown / fr] | Spanish [unknown / es] | German [unknown / de] |
| 691 | Sport pratiqué à Wimbledon ? | French [unknown / fr] | Spanish [unknown / es] | German [unknown / de] |
| 692 | Hum, sur quelle mer se trouve Venise ? | French [unknown / fr] | Spanish [unknown / es] | German [unknown / de] |
| 693 | Quelle est la capitale de l'Indonésie? | French [unknown / fr] | Spanish [unknown / es] | German [unknown / de] |
| 694 | Quelle planète est la plus éloignée du Soleil ? | French [unknown / fr] | Spanish [unknown / es] | German [unknown / de] |
| 695 | Retrouvez l'auteur d'Alice au pays des merveilles. | French [unknown / fr] | French [unknown / fr] | German [unknown / de] |
| 696 | Clarifiez comment les chameaux survivent dans le désert. | French [unknown / fr] | Spanish [unknown / es] | German [unknown / de] |
| 697 | Comment les hérissons se défendent-ils ? | French [unknown / fr] | Spanish [unknown / es] | German [unknown / de] |
| 698 | Sport du Tour de France ? | French [unknown / fr] | French [unknown / fr] | German [unknown / de] |
| 699 | Bon, sur quelle île Napoléon est-il né ? | French [unknown / fr] | Spanish [unknown / es] | German [unknown / de] |

