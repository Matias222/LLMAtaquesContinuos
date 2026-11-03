# Vecino mas cercano de e + a*v (`algebra/runs/centroide_smoke/fr/cB.pt`)

||v|| 0.8783, ||e|| medio 1.0861, gap mediano 0.798

||v|| supera la norma de 3.4% de los tokens del vocabulario y de 2.3% de los tokens de las preguntas (mediana 1.1290)

| vec | a | entrada | n_tok | cambia l2 | cambia cos | destinos l2 |
|---|---|---|---|---|---|---|
| v | 1 | prompt | 844 | 2.6% | 1.2% | `which`×10, `who`×6, `what`×6 |
| v | 2 | prompt | 844 | 54.9% | 56.6% | `?>

`×133, `.L`×32, ` của`×27, `	is`×15, ` cómo`×14 |
| v | 4 | prompt | 844 | 80.2% | 98.7% | `!");
`×498, `-capital`×11, ` la`×9, `.country`×6, `	light`×4 |
| rand | 1 | prompt | 844 | 0.0% | 0.0% |  |
| rand | 2 | prompt | 844 | 0.0% | 0.0% |  |
| rand | 4 | prompt | 844 | 0.0% | 0.0% |  |

## prompt  (a=1, parche v)

| # | original | vecino l2 | vecino cos |
|---|---|---|---|
| 588 | What is the speed of light in vacuum in kilometers per second, rounded? | What is the speed of light in vacuum in kilometers per second, rounded? | What is the speed of light in vacuum in kilometers per second, rounded? |
| 589 | Who authored The Communist Manifesto? | Who authored The Communist Manifesto? | Who authored The Communist Manifesto? |
| 590 | Reveal the largest lake in South America. | Reveal the largest lake in South America. | Reveal the largest lake in South America. |
| 591 | Lay out how the Moon formed. | Lay out how the Moon formed. | Lay out how the Moon formed. |
| 592 | How does the eye focus light? | How does the eye focus light? | How does the eye focus light? |
| 593 | Tallest tree species? | Tallest tree species? | Tallest tree species? |
| 594 | Wait, who proposed continental drift? | Wait,who proposed continental drift? | Wait, who proposed continental drift? |
| 595 | In what year did the Islamic Revolution take place in Iran? | Inwhat year did the Islamic Revolution take place in Iran? | In what year did the Islamic Revolution take place in Iran? |
| 596 | Who invented the electric battery? | Who invented the electric battery? | Who invented the electric battery? |
| 597 | Pinpoint the capital of Armenia. | Pinpoint the capital of Armenia. | Pinpoint the capital of Armenia. |
