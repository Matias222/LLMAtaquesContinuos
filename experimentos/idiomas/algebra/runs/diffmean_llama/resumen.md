# DiffMean en la capa 0 contra Shared (llama)

Corrida: `algebra/runs/diffmean_llama`  |  Shared: `algebra/runs/v10`

Criterio pre-registrado: norma = argmax de *target y correcta* en validacion (filas 528..587); **equivalente** = McNemar exacto p > 0.05 contra Shared en *target y correcta* Y a <= 5 pp del nativo. Primario: `Dmulti`.

## 1. Vectores

| vector | L | norma cruda | norma elegida | norma Shared | cos(D, Shared) | cos(D, mu_vocab) |
|---|---|---|---|---|---|---|
| Dmulti | fr | 0.13 | 0.7 | 0.878 | +0.080 | +0.168 |
| Dmulti | es | 0.13 | 0.6 | 0.912 | +0.061 | +0.362 |
| Dmulti | de | 0.13 | 0.5 | 0.936 | +0.124 | +0.350 |
| Den | fr | 0.22 | 0.6 | 0.878 | +0.079 | +0.477 |
| Den | es | 0.22 | 0.6 | 0.912 | +0.044 | +0.565 |
| Den | de | 0.21 | 0.6 | 0.936 | +0.087 | +0.586 |

Cosenos entre vectores (capa 0):

|  | Dmulti_fr | Dmulti_es | Dmulti_de | Den_fr | Den_es | Den_de | shared_fr | shared_es | shared_de |
|---|---|---|---|---|---|---|---|---|---|
| Dmulti_fr | +1.00 | +0.04 | -0.19 | +0.82 | +0.39 | +0.30 | +0.08 | -0.01 | -0.06 |
| Dmulti_es | +0.04 | +1.00 | -0.22 | +0.38 | +0.82 | +0.28 | +0.02 | +0.06 | -0.01 |
| Dmulti_de | -0.19 | -0.22 | +1.00 | +0.19 | +0.17 | +0.76 | +0.00 | -0.01 | +0.12 |
| Den_fr | +0.82 | +0.38 | +0.19 | +1.00 | +0.80 | +0.74 | +0.08 | +0.01 | +0.00 |
| Den_es | +0.39 | +0.82 | +0.17 | +0.80 | +1.00 | +0.73 | +0.05 | +0.04 | +0.02 |
| Den_de | +0.30 | +0.28 | +0.76 | +0.74 | +0.73 | +1.00 | +0.05 | +0.01 | +0.09 |
| shared_fr | +0.08 | +0.02 | +0.00 | +0.08 | +0.05 | +0.05 | +1.00 | +0.25 | +0.18 |
| shared_es | -0.01 | +0.06 | -0.01 | +0.01 | +0.04 | +0.01 | +0.25 | +1.00 | +0.17 |
| shared_de | -0.06 | -0.01 | +0.12 | +0.00 | +0.02 | +0.09 | +0.18 | +0.17 | +1.00 |

## 2. Seleccion de norma (validacion, filas 528..587)

### fr

| condicion | norma | % target | accuracy | target y correcta | CE head |
|---|---|---|---|---|---|
| nativo | – | 95.0 | 73.3 | 68.3 | – |
| Shared | 0.878 | 100.0 | 75.0 | 75.0 | 0.72 |
| Dmulti | 0.5 | 10.0 | 95.0 | 10.0 | 3.70 |
| Dmulti | 0.6 | 31.7 | 86.7 | 23.3 | 2.80 |
| Dmulti **<-** | 0.7 | 78.3 | 53.3 | 35.0 | 2.29 |
| Dmulti | 0.8 | 96.7 | 18.3 | 16.7 | 2.93 |
| Dmulti | 1 | 100.0 | 1.7 | 1.7 | 4.26 |
| Den | 0.5 | 33.3 | 90.0 | 26.7 | 2.63 |
| Den **<-** | 0.6 | 90.0 | 70.0 | 61.7 | 1.59 |
| Den | 0.7 | 100.0 | 58.3 | 58.3 | 1.88 |
| Den | 0.8 | 100.0 | 40.0 | 40.0 | 2.36 |
| Den | 1 | 100.0 | 6.7 | 6.7 | 3.56 |

### es

| condicion | norma | % target | accuracy | target y correcta | CE head |
|---|---|---|---|---|---|
| nativo | – | 100.0 | 71.7 | 71.7 | – |
| Shared | 0.912 | 98.3 | 71.7 | 70.0 | 0.55 |
| Dmulti | 0.5 | 11.7 | 93.3 | 11.7 | 3.12 |
| Dmulti **<-** | 0.6 | 38.3 | 81.7 | 26.7 | 2.22 |
| Dmulti | 0.7 | 73.3 | 35.0 | 21.7 | 2.57 |
| Dmulti | 0.8 | 75.0 | 11.7 | 10.0 | 3.50 |
| Dmulti | 1 | 60.0 | 0.0 | 0.0 | 4.83 |
| Den | 0.5 | 38.3 | 90.0 | 31.7 | 2.39 |
| Den **<-** | 0.6 | 88.3 | 63.3 | 53.3 | 1.40 |
| Den | 0.7 | 98.3 | 53.3 | 53.3 | 1.93 |
| Den | 0.8 | 100.0 | 38.3 | 38.3 | 2.50 |
| Den | 1 | 100.0 | 16.7 | 16.7 | 3.63 |

### de

| condicion | norma | % target | accuracy | target y correcta | CE head |
|---|---|---|---|---|---|
| nativo | – | 96.7 | 75.0 | 71.7 | – |
| Shared | 0.936 | 100.0 | 70.0 | 70.0 | 0.81 |
| Dmulti **<-** | 0.5 | 6.7 | 90.0 | 6.7 | 3.56 |
| Dmulti | 0.6 | 28.3 | 45.0 | 1.7 | 3.57 |
| Dmulti | 0.7 | 26.7 | 23.3 | 5.0 | 4.36 |
| Dmulti | 0.8 | 55.0 | 6.7 | 3.3 | 4.69 |
| Dmulti | 1 | 100.0 | 1.7 | 1.7 | 5.00 |
| Den | 0.5 | 23.3 | 85.0 | 18.3 | 2.99 |
| Den **<-** | 0.6 | 66.7 | 70.0 | 43.3 | 2.16 |
| Den | 0.7 | 90.0 | 45.0 | 43.3 | 2.50 |
| Den | 0.8 | 95.0 | 26.7 | 25.0 | 3.03 |
| Den | 1 | 96.7 | 11.7 | 10.0 | 4.41 |

Curvas en `algebra/runs/diffmean_llama/curvas_sel.csv`.

## 3. Held-out (Tabla 1): q_en + vector

### fr

| condicion | % target | accuracy | target y correcta | acc \| target | CE head | McNemar vs Shared (solo Shared / solo este) | equivalente |
|---|---|---|---|---|---|---|---|
| none | 0.0 | 97.3 | 0.0 | – | 5.49 |  |  |
| nativo | 99.1 | 75.9 | 75.0 | 75.7 | – |  |  |
| Shared | 100.0 | 78.6 | 78.6 | 78.6 | 0.70 |  |  |
| Dmulti | 78.6 | 57.1 | 37.5 | 47.7 | 2.24 | 50/4 p=0.000 | no |
| Den | 97.3 | 67.0 | 64.3 | 66.1 | 1.40 | 24/8 p=0.007 | no |
| rand | 0.0 | 96.4 | 0.0 | – | 5.41 | 88/0 p=0.000 |  |

### es

| condicion | % target | accuracy | target y correcta | acc \| target | CE head | McNemar vs Shared (solo Shared / solo este) | equivalente |
|---|---|---|---|---|---|---|---|
| none | 0.0 | 97.3 | 0.0 | – | 5.46 |  |  |
| nativo | 95.5 | 72.3 | 68.8 | 72.0 | – |  |  |
| Shared | 99.1 | 82.1 | 81.2 | 82.0 | 0.84 |  |  |
| Dmulti | 46.4 | 67.9 | 20.5 | 44.2 | 2.50 | 73/5 p=0.000 | no |
| Den | 91.1 | 65.2 | 58.0 | 63.7 | 1.57 | 33/7 p=0.000 | no |
| rand | 0.0 | 96.4 | 0.0 | – | 5.43 | 91/0 p=0.000 |  |

### de

| condicion | % target | accuracy | target y correcta | acc \| target | CE head | McNemar vs Shared (solo Shared / solo este) | equivalente |
|---|---|---|---|---|---|---|---|
| none | 0.0 | 97.3 | 0.0 | – | 5.96 |  |  |
| nativo | 94.6 | 77.7 | 72.3 | 76.4 | – |  |  |
| Shared | 99.1 | 81.2 | 80.4 | 81.1 | 1.16 |  |  |
| Dmulti | 10.7 | 90.2 | 8.0 | 75.0 | 3.88 | 82/1 p=0.000 | no |
| Den | 67.9 | 76.8 | 47.3 | 69.7 | 2.49 | 44/7 p=0.000 | no |
| rand | 0.0 | 97.3 | 0.0 | – | 5.94 | 90/0 p=0.000 |  |

**Veredicto pre-registrado**

- Dmulti fr: no equivalente (t&c 37.5 vs Shared 78.6, nativo 75.0, p=0.000)
- Den fr: no equivalente (t&c 64.3 vs Shared 78.6, nativo 75.0, p=0.007)
- Dmulti es: no equivalente (t&c 20.5 vs Shared 81.2, nativo 68.8, p=0.000)
- Den es: no equivalente (t&c 58.0 vs Shared 81.2, nativo 68.8, p=0.000)
- Dmulti de: no equivalente (t&c 8.0 vs Shared 80.4, nativo 72.3, p=0.000)
- Den de: no equivalente (t&c 47.3 vs Shared 80.4, nativo 72.3, p=0.000)

## 4. Otros idiomas de origen (Tabla 6 + it/pt no vistos): q_s + vector_L

| origen -> target | sin parche | Shared | Dmulti | Den |
|---|---|---|---|---|
| es -> fr | 0.0 / 0.0 | 99.1 / 67.0 | 96.4 / 1.8 | 69.6 / 37.5 |
| de -> fr | 0.0 / 0.0 | 99.1 / 62.5 | 90.2 / 2.7 | 78.6 / 37.5 |
| it -> fr (no visto) | 0.0 / 0.0 | 89.3 / 56.2 | 92.0 / 1.8 | 90.2 / 42.9 |
| pt -> fr (no visto) | 0.0 / 0.0 | 95.5 / 59.8 | 97.3 / 1.8 | 87.5 / 33.9 |
| de -> es | 0.0 / 0.0 | 97.3 / 64.3 | 93.8 / 21.4 | 60.7 / 23.2 |
| fr -> es | 0.0 / 0.0 | 96.4 / 64.3 | 100.0 / 25.0 | 73.2 / 42.0 |
| it -> es (no visto) | 0.0 / 0.0 | 91.1 / 50.9 | 97.3 / 17.9 | 79.5 / 38.4 |
| pt -> es (no visto) | 1.8 / 0.9 | 83.9 / 50.9 | 95.5 / 17.9 | 72.3 / 31.2 |
| es -> de | 0.0 / 0.0 | 97.3 / 63.4 | 99.1 / 35.7 | 60.7 / 25.0 |
| fr -> de | 0.0 / 0.0 | 100.0 / 69.6 | 99.1 / 33.9 | 54.5 / 27.7 |
| it -> de (no visto) | 0.0 / 0.0 | 97.3 / 55.4 | 89.3 / 25.0 | 74.1 / 34.8 |
| pt -> de (no visto) | 0.0 / 0.0 | 89.3 / 55.4 | 96.4 / 24.1 | 62.5 / 15.2 |

Celdas: % target / % target y correcta.

## 5. Bateria de tests (mismas condiciones que la etapa E de Shared)

### resta

| condicion | vector | en | fr | es | de | acc |
|---|---|---|---|---|---|---|
| plain \| prompt_fr | — | 0.0 | 99.1 | 0.0 | 0.0 | 75.9 |
| plain \| prompt_fr -1*fr | Shared | 83.9 | 8.9 | 6.2 | 0.9 | 30.4 |
| plain \| prompt_fr -1*fr | Dmulti | 39.3 | 4.5 | 8.0 | 48.2 | 42.9 |
| plain \| prompt_fr -1*es | Shared | 0.0 | 100.0 | 0.0 | 0.0 | 51.8 |
| plain \| prompt_fr -1*es | Dmulti | 2.7 | 96.4 | 0.0 | 0.9 | 67.9 |
| plain \| prompt_fr -1*de | Shared | 49.1 | 50.9 | 0.0 | 0.0 | 41.1 |
| plain \| prompt_fr -1*de | Dmulti | 0.0 | 100.0 | 0.0 | 0.0 | 66.1 |
| plain \| prompt_fr -1*rand0_fr | Shared | 1.8 | 98.2 | 0.0 | 0.0 | 56.2 |
| plain \| prompt_fr -1*rand0_fr | Dmulti | 1.8 | 98.2 | 0.0 | 0.0 | 69.6 |
| plain \| prompt_es | — | 0.0 | 0.0 | 95.5 | 0.0 | 72.3 |
| plain \| prompt_es -1*fr | Shared | 3.6 | 0.0 | 95.5 | 0.0 | 51.8 |
| plain \| prompt_es -1*fr | Dmulti | 10.7 | 0.0 | 83.9 | 4.5 | 64.3 |
| plain \| prompt_es -1*es | Shared | 2.7 | 76.8 | 17.0 | 0.0 | 46.4 |
| plain \| prompt_es -1*es | Dmulti | 25.9 | 33.0 | 3.6 | 33.9 | 61.6 |
| plain \| prompt_es -1*de | Shared | 18.8 | 0.9 | 80.4 | 0.0 | 46.4 |
| plain \| prompt_es -1*de | Dmulti | 3.6 | 0.9 | 95.5 | 0.0 | 48.2 |
| plain \| prompt_es -1*rand0_es | Shared | 0.9 | 0.9 | 97.3 | 0.0 | 58.9 |
| plain \| prompt_es -1*rand0_es | Dmulti | 0.0 | 0.0 | 98.2 | 0.0 | 72.3 |
| plain \| prompt_de | — | 0.9 | 0.0 | 0.0 | 94.6 | 77.7 |
| plain \| prompt_de -1*fr | Shared | 39.3 | 0.0 | 0.0 | 60.7 | 39.3 |
| plain \| prompt_de -1*fr | Dmulti | 15.2 | 0.0 | 0.0 | 84.8 | 53.6 |
| plain \| prompt_de -1*es | Shared | 0.0 | 0.0 | 0.0 | 100.0 | 63.4 |
| plain \| prompt_de -1*es | Dmulti | 12.5 | 0.9 | 0.0 | 86.6 | 55.4 |
| plain \| prompt_de -1*de | Shared | 95.5 | 0.0 | 0.0 | 2.7 | 28.6 |
| plain \| prompt_de -1*de | Dmulti | 19.6 | 50.0 | 14.3 | 15.2 | 46.4 |
| plain \| prompt_de -1*rand0_de | Shared | 7.1 | 0.0 | 0.0 | 92.0 | 52.7 |
| plain \| prompt_de -1*rand0_de | Dmulti | 0.9 | 0.0 | 0.0 | 95.5 | 73.2 |

### idioma_entrada

| condicion | vector | dice en | dice fr | dice es | dice de |
|---|---|---|---|---|---|
| lang_id \| prompt | — | 96.4 | 0.9 | 1.8 | 0.0 |
| lang_id \| prompt +1*fr | Shared | 15.2 | 75.9 | 2.7 | 0.9 |
| lang_id \| prompt +1*fr | Dmulti | 0.9 | 97.3 | 0.0 | 0.0 |
| lang_id \| prompt +1*es | Shared | 4.5 | 0.9 | 90.2 | 0.9 |
| lang_id \| prompt +1*es | Dmulti | 0.9 | 0.0 | 97.3 | 0.0 |
| lang_id \| prompt +1*de | Shared | 8.9 | 0.9 | 2.7 | 84.8 |
| lang_id \| prompt +1*de | Dmulti | 14.3 | 0.9 | 2.7 | 72.3 |
| lang_id \| prompt +1*rand0 | Shared | 95.5 | 0.9 | 0.9 | 0.0 |
| lang_id \| prompt +1*rand0 | Dmulti | 95.5 | 0.9 | 1.8 | 0.0 |
| lang_id \| prompt_fr | — | 0.0 | 100.0 | 0.0 | 0.0 |
| lang_id \| prompt_es | — | 0.0 | 0.0 | 100.0 | 0.0 |
| lang_id \| prompt_de | — | 0.9 | 0.9 | 2.7 | 95.5 |

### resta_directiva

| condicion | vector | en | fr | es | de | acc |
|---|---|---|---|---|---|---|
| instr_fr \| prompt | — | 0.0 | 100.0 | 0.0 | 0.0 | 81.2 |
| instr_fr \| prompt -1*fr | Shared | 1.8 | 96.4 | 0.0 | 0.0 | 71.4 |
| instr_fr \| prompt -1*fr | Dmulti | 0.9 | 96.4 | 0.0 | 0.0 | 75.9 |
| instr_fr \| prompt -1*es | Shared | 0.0 | 99.1 | 0.0 | 0.0 | 75.9 |
| instr_fr \| prompt -1*es | Dmulti | 0.0 | 100.0 | 0.0 | 0.0 | 76.8 |
| instr_fr \| prompt -1*rand0 | Shared | 0.0 | 99.1 | 0.0 | 0.0 | 79.5 |
| instr_fr \| prompt -1*rand0 | Dmulti | 0.9 | 98.2 | 0.0 | 0.0 | 80.4 |

### conflicto

| condicion | vector | en | fr | es | de | acc |
|---|---|---|---|---|---|---|
| instr_en \| prompt_fr | — | 27.7 | 72.3 | 0.0 | 0.0 | 77.7 |
| instr_en \| prompt | — | 100.0 | 0.0 | 0.0 | 0.0 | 96.4 |
| instr_en \| prompt +1*fr | Shared | 23.2 | 76.8 | 0.0 | 0.0 | 82.1 |
| instr_en \| prompt +1*fr | Dmulti | 85.7 | 13.4 | 0.0 | 0.0 | 69.6 |
| instr_en \| prompt +1*rand0 | Shared | 100.0 | 0.0 | 0.0 | 0.0 | 96.4 |
| instr_en \| prompt +1*rand0 | Dmulti | 100.0 | 0.0 | 0.0 | 0.0 | 97.3 |
| plain \| prompt | — | 100.0 | 0.0 | 0.0 | 0.0 | 97.3 |
| plain \| prompt +1*fr | Shared | 0.0 | 100.0 | 0.0 | 0.0 | 79.5 |
| plain \| prompt +1*fr | Dmulti | 21.4 | 78.6 | 0.0 | 0.0 | 57.1 |

### conflicto_v2

| condicion | vector | en | fr | es | de | acc |
|---|---|---|---|---|---|---|
| instr_en_post \| prompt_fr | — | 96.4 | 3.6 | 0.0 | 0.0 | 92.9 |
| instr_en_post \| prompt | — | 100.0 | 0.0 | 0.0 | 0.0 | 96.4 |
| instr_en_post \| prompt +1*fr | Shared | (falta) |  |  |  |  |
| instr_en_post \| prompt +1*fr | Dmulti | 99.1 | 0.9 | 0.0 | 0.0 | 68.8 |
| instr_en_post_ref \| prompt_fr | — | 98.2 | 1.8 | 0.0 | 0.0 | 92.0 |
| instr_en_post_ref \| prompt | — | 100.0 | 0.0 | 0.0 | 0.0 | 96.4 |
| instr_en_post_ref \| prompt +1*fr | Shared | 83.0 | 17.0 | 0.0 | 0.0 | 91.1 |
| instr_en_post_ref \| prompt +1*fr | Dmulti | 100.0 | 0.0 | 0.0 | 0.0 | 73.2 |

En los tests de D los nombres fr/es/de son D_fr/D_es/D_de a la norma elegida; randN copia la norma de D (en Shared, la de Shared).

## 6. Eficiencia de datos: Dmulti_fr con N preguntas paralelas (held-out fr)

| N | semilla | cos(D_N, D_528) | % target | accuracy | target y correcta | CE head |
|---|---|---|---|---|---|---|
| 8 | 0 | +0.762 | 18.8 | 88.4 | 11.6 | 2.86 |
| 8 | 1 | +0.774 | 41.1 | 92.0 | 33.0 | 2.44 |
| 32 | 0 | +0.921 | 55.4 | 67.0 | 26.8 | 2.07 |
| 32 | 1 | +0.931 | 79.5 | 68.8 | 48.2 | 1.80 |
| 128 | 0 | +0.985 | 77.7 | 59.8 | 38.4 | 2.22 |
| 128 | 1 | +0.986 | 79.5 | 61.6 | 44.6 | 2.09 |
| 528 | – | +1.000 | 78.6 | 57.1 | 37.5 | 2.24 |

## 7. Geometria por capas (ultimo token del prompt, validacion cruzada por mitades)

### fr (n=112, 28 capas)

| par | L0 | L1 | L7 | L14 | L21 | L28 |
|---|---|---|---|---|---|---|
| cos(shared, Dmulti) | +0.00 | +0.37 | +0.46 | +0.58 | +0.62 | +0.78 |
| cos(shared, Den) | +0.00 | +0.40 | +0.45 | +0.63 | +0.76 | +0.85 |
| cos(shared, nativo) | +0.00 | +0.45 | +0.51 | +0.71 | +0.80 | +0.86 |
| cos(Dmulti, nativo) | +0.00 | +0.56 | +0.69 | +0.69 | +0.74 | +0.87 |
| cos(Den, nativo) | +0.00 | +0.62 | +0.79 | +0.83 | +0.91 | +0.95 |
| cos(rand, nativo) | +0.00 | +0.18 | +0.17 | +0.16 | +0.09 | +0.20 |
| cos(shared, instr) | +0.00 | +0.01 | +0.34 | +0.56 | +0.78 | +0.85 |
| cos(Dmulti, instr) | +0.00 | -0.15 | +0.30 | +0.46 | +0.69 | +0.83 |
| cos(nativo, instr) | +0.00 | +0.23 | +0.30 | +0.52 | +0.77 | +0.87 |
| cos(shared, shared) | +0.00 | +1.00 | +1.00 | +0.98 | +0.97 | +0.97 |
| cos(Dmulti, Dmulti) | +0.00 | +1.00 | +0.99 | +0.98 | +0.97 | +0.97 |
| cos(nativo, nativo) | +0.00 | +0.99 | +0.99 | +0.99 | +0.97 | +0.97 |

### es (n=112, 28 capas)

| par | L0 | L1 | L7 | L14 | L21 | L28 |
|---|---|---|---|---|---|---|
| cos(shared, Dmulti) | +0.00 | +0.44 | +0.45 | +0.55 | +0.60 | +0.78 |
| cos(shared, Den) | +0.00 | +0.32 | +0.56 | +0.75 | +0.86 | +0.92 |
| cos(shared, nativo) | +0.00 | +0.14 | +0.79 | +0.92 | +0.94 | +0.95 |
| cos(Dmulti, nativo) | +0.00 | +0.50 | +0.53 | +0.56 | +0.61 | +0.79 |
| cos(Den, nativo) | +0.00 | +0.64 | +0.74 | +0.78 | +0.88 | +0.94 |
| cos(rand, nativo) | +0.00 | +0.00 | +0.10 | +0.11 | +0.05 | +0.13 |
| cos(shared, instr) | +0.00 | -0.12 | +0.24 | +0.50 | +0.78 | +0.86 |
| cos(Dmulti, instr) | +0.00 | -0.06 | +0.30 | +0.39 | +0.59 | +0.77 |
| cos(nativo, instr) | +0.00 | +0.22 | +0.29 | +0.52 | +0.78 | +0.86 |
| cos(shared, shared) | +0.00 | +1.00 | +0.99 | +0.98 | +0.98 | +0.97 |
| cos(Dmulti, Dmulti) | +0.00 | +1.00 | +0.98 | +0.97 | +0.95 | +0.95 |
| cos(nativo, nativo) | +0.00 | +0.99 | +1.00 | +0.99 | +0.97 | +0.97 |

### de (n=112, 28 capas)

| par | L0 | L1 | L7 | L14 | L21 | L28 |
|---|---|---|---|---|---|---|
| cos(shared, Dmulti) | +0.00 | +0.42 | +0.42 | +0.47 | +0.41 | +0.63 |
| cos(shared, Den) | +0.00 | +0.31 | +0.43 | +0.62 | +0.73 | +0.86 |
| cos(shared, nativo) | +0.00 | +0.20 | +0.53 | +0.79 | +0.87 | +0.90 |
| cos(Dmulti, nativo) | +0.00 | +0.52 | +0.54 | +0.54 | +0.47 | +0.63 |
| cos(Den, nativo) | +0.00 | +0.64 | +0.65 | +0.73 | +0.82 | +0.91 |
| cos(rand, nativo) | +0.00 | -0.06 | +0.12 | +0.14 | +0.09 | +0.15 |
| cos(shared, instr) | +0.00 | -0.17 | +0.33 | +0.52 | +0.78 | +0.86 |
| cos(Dmulti, instr) | +0.00 | -0.06 | +0.27 | +0.32 | +0.41 | +0.65 |
| cos(nativo, instr) | +0.00 | +0.22 | +0.32 | +0.54 | +0.77 | +0.88 |
| cos(shared, shared) | +0.00 | +1.00 | +0.99 | +0.98 | +0.97 | +0.97 |
| cos(Dmulti, Dmulti) | +0.00 | +1.00 | +0.98 | +0.96 | +0.91 | +0.88 |
| cos(nativo, nativo) | +0.00 | +0.99 | +0.99 | +0.98 | +0.97 | +0.97 |

La diagonal (x, x) es el techo de ruido split-half. Todas las capas en `algebra/runs/diffmean_llama/geo.csv`.
