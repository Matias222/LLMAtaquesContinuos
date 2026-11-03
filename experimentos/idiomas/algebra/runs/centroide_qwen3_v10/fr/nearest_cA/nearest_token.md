# Vecino mas cercano de e + a*v (`algebra/runs/centroide_qwen3_v10/fr/cA.pt`)

||v|| 0.9228, ||e|| medio 1.0885, gap mediano 0.763

||v|| supera la norma de 9.0% de los tokens del vocabulario y de 5.5% de los tokens de las preguntas (mediana 1.0724)

| vec | a | entrada | n_tok | cambia l2 | cambia cos | destinos l2 |
|---|---|---|---|---|---|---|
| v | 0.6 | prompt | 848 | 0.0% | 0.0% |  |
| v | 0.7 | prompt | 848 | 0.0% | 0.0% |  |
| v | 1 | prompt | 848 | 0.0% | 0.0% |  |
| v | 2 | prompt | 848 | 0.0% | 0.0% |  |
| v | 4 | prompt | 848 | 73.3% | 76.2% | ` la`×453, ` ?`×138, ` le`×31 |
| rand | 0.6 | prompt | 848 | 0.0% | 0.0% |  |
| rand | 0.7 | prompt | 848 | 0.0% | 0.0% |  |
| rand | 1 | prompt | 848 | 0.0% | 0.0% |  |
| rand | 2 | prompt | 848 | 0.0% | 0.0% |  |
| rand | 4 | prompt | 848 | 0.0% | 0.0% |  |

## prompt  (a=1, parche v)

| # | original | vecino l2 | vecino cos |
|---|---|---|---|
| 588 | What is the speed of light in vacuum in kilometers per second, rounded? | What is the speed of light in vacuum in kilometers per second, rounded? | What is the speed of light in vacuum in kilometers per second, rounded? |
| 589 | Who authored The Communist Manifesto? | Who authored The Communist Manifesto? | Who authored The Communist Manifesto? |
| 590 | Reveal the largest lake in South America. | Reveal the largest lake in South America. | Reveal the largest lake in South America. |
| 591 | Lay out how the Moon formed. | Lay out how the Moon formed. | Lay out how the Moon formed. |
| 592 | How does the eye focus light? | How does the eye focus light? | How does the eye focus light? |
| 593 | Tallest tree species? | Tallest tree species? | Tallest tree species? |
| 594 | Wait, who proposed continental drift? | Wait, who proposed continental drift? | Wait, who proposed continental drift? |
| 595 | In what year did the Islamic Revolution take place in Iran? | In what year did the Islamic Revolution take place in Iran? | In what year did the Islamic Revolution take place in Iran? |
| 596 | Who invented the electric battery? | Who invented the electric battery? | Who invented the electric battery? |
| 597 | Pinpoint the capital of Armenia. | Pinpoint the capital of Armenia. | Pinpoint the capital of Armenia. |
