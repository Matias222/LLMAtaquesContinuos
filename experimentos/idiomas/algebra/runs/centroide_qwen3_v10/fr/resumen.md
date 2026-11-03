# Control centroide, held-out en ingles, idioma fr

||v_fr|| = 0.9228  |  cos al azar ~ 0.0198

| vector | cos(shared) | cos(mu_vocab) |
|---|---|---|
| cA | -0.018 | +0.052 |
| cB | +0.047 | +0.361 |

- cos(mu_L, mu_en): +0.5657
- cos(mu_L, mu_vocab): +0.0519
- cos(mu_en, mu_vocab): -0.2714
- cos(shared, mu_vocab): +0.0512
- norma mu_vocab: +0.3047
- unicos: cos(cA, shared): +0.0391
- unicos: cos(cB, shared): +0.0690
- unicos: cos(cB, cB_frecuencia): +0.5775

| condicion | escala | n | % idioma target | accuracy | CE head (sin -> con) |
|---|---|---|---|---|---|
| none | - | 112 | 0.0 | 99.1 | |
| nativo | - | 112 | 100.0 | 83.9 | |
| shared | 1 | 112 | 97.3 | 83.9 | 8.57 -> 1.43 |
| cA | 1 | 112 | 98.2 | 0.0 | 8.57 -> 8.63 |
| cA | 0.6 | 112 | 100.0 | 17.9 | 8.57 -> 6.80 |
| cA | 0.7 | 112 | 99.1 | 5.4 | 8.57 -> 7.69 |
| cB | 1 | 112 | 74.1 | 8.9 | 8.57 -> 6.53 |
| cB | 0.6 | 112 | 97.3 | 87.5 | 8.57 -> 1.88 |
| cB | 0.7 | 112 | 97.3 | 83.9 | 8.57 -> 2.13 |
| rand0 | 1 | 112 | 0.9 | 98.2 | 8.57 -> 7.78 |
