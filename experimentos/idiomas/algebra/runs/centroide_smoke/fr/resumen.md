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
| none | - | 4 | 0.0 | 100.0 | |
| nativo | - | 4 | 100.0 | 75.0 | |
| shared | 1 | 4 | 100.0 | 100.0 | 5.23 -> 0.37 |
| cA | 1 | 4 | 100.0 | 50.0 | 5.23 -> 2.19 |
| cA | 2 | 4 | 25.0 | 0.0 | 5.23 -> 6.64 |
| cB | 1 | 4 | 100.0 | 50.0 | 5.23 -> 2.27 |
| cB | 2 | 4 | 100.0 | 0.0 | 5.23 -> 4.51 |
| rand0 | 1 | 4 | 0.0 | 100.0 | 5.23 -> 4.98 |
