# LLMAtaquesContinuos

Steering comportamental en Llama-3.2-3B-Instruct mediante perturbaciones aditivas
en el espacio de embeddings (layer 0):  `e'_i = e_i + v_i`.

## Estructura

| ruta | que hay |
|---|---|
| `experimentos/idiomas/` | **experimento activo**: parche aditivo que induce frances, con metricas objetivas |
| `legacy/` | scripts del experimento de navidad (entrenamiento, eval, antipatch, inspeccion geometrica) |
| `resultados/primera_parte/` | 31 runs de navidad: parches, reportes de eval y de geometria |
| `resultados/dimensiones/` | ablaciones posicionales sobre parches de navidad |
| `resultados/parches_antiguos/` | parches v4/v5, deprecados |
| `llm_attacks/` | libreria base (SuffixManager, templates de conversacion) |
| `HALLAZGOS.md` | **registro tecnico de lo establecido**: hipotesis, experimentos, numeros, errores de medicion y pendientes |
| `CHRISTMAS_STEERING_LOG.md` | log de la primera etapa. Contiene afirmaciones que `HALLAZGOS.md` corrige |

Los scripts de `legacy/` se corren **desde dentro de `legacy/`** (`cd legacy && python
christmas_final_train.py`); cada uno importa `_bootstrap` para agregar el root del
repo a `sys.path`.

## Experimento activo: idiomas

Ver `experimentos/idiomas/README.md`. En corto:

```bash
cd experimentos/idiomas
bash run_french.sh /ruta/al/modelo/Llama-3.2-3B-Instruct
```
