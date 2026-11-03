# Control centroide, held-out en ingles, idioma fr

||v_fr|| = 0.8783  |  cos al azar ~ 0.0180

| vector | cos(shared) | cos(mu_vocab) |
|---|---|---|
| cA | +0.026 | +0.343 |
| cB | +0.079 | +0.478 |

- cos(mu_L, mu_en): +0.3856
- cos(mu_L, mu_vocab): +0.3431
- cos(mu_en, mu_vocab): -0.1847
- cos(shared, mu_vocab): +0.0966
- norma mu_vocab: +0.4162
- unicos: cos(cA, shared): +0.0930
- unicos: cos(cB, shared): +0.0455
- unicos: cos(cB, cB_frecuencia): +0.6796

| condicion | escala | n | % idioma target | accuracy | CE head (sin -> con) |
|---|---|---|---|---|---|
| none | - | 112 | 0.0 | 97.3 | |
| nativo | - | 112 | 99.1 | 75.9 | |
| shared | 1 | 112 | 100.0 | 78.6 | 5.49 -> 0.70 |
| cA | 1 | 112 | 87.5 | 17.9 | 5.49 -> 2.87 |
| cA | 2 | 112 | 13.4 | 0.0 | 5.49 -> 6.19 |
| cA | 4 | 112 | 0.0 | 0.0 | 5.49 -> 7.43 |
| cB | 1 | 112 | 99.1 | 20.5 | 5.49 -> 2.73 |
| cB | 2 | 112 | 100.0 | 0.9 | 5.49 -> 4.93 |
| cB | 4 | 112 | 14.3 | 0.0 | 5.49 -> 5.06 |
| rand0 | 1 | 112 | 0.0 | 94.6 | 5.49 -> 5.31 |
