# Modelo de Predicción — Documentación

> **Versión 2** (reentrenado). La versión 1 de este documento reportaba 64,7% de
> accuracy con 7 variables. Ese número era engañoso: como el 72,7% de las canciones
> no son hit, un modelo que dijera siempre *"no es hit"* habría sacado 72,7% sin
> aprender nada. El detalle del arreglo está en `notebooks/03_model_retraining.ipynb`.

## Qué hace

Predice si una canción tiene potencial de ser un hit comercial (popularidad de
Spotify ≥ 70) a partir de 10 características de audio, usando las 4.494 canciones
de `data/spotify_clean.csv`.

## Archivos generados

| Archivo | Qué es |
|---|---|
| `models/model.pkl` | El modelo entrenado, listo para `joblib.load()` |
| `models/features.pkl` | La lista de variables **en el orden exacto** que el modelo espera |
| `models/metrics.json` | Las métricas y las importancias que la app muestra en la Ficha técnica |
| `notebooks/03_model_retraining.ipynb` | El proceso completo, paso a paso |
| `notebooks/train_model.py` | El mismo proceso como script ejecutable |

## Variables de entrada

Las 7 originales más 3 que probamos y sí aportaron: agregar `duration_min`,
`instrumentalness` y `liveness` subió el ROC-AUC de **0,708 a 0,743**.

| # | Variable | Qué es | Rango |
|---|---|---|---|
| 1 | danceability | Qué tan bailable | 0 a 1 |
| 2 | energy | Intensidad | 0 a 1 |
| 3 | valence | Alegre vs. triste | 0 a 1 |
| 4 | tempo | BPM | ~50 a 240 |
| 5 | loudness | Volumen (dB) | -48 a 1 |
| 6 | speechiness | Voz hablada vs. cantada | 0 a 1 |
| 7 | acousticness | Acústico vs. electrónico | 0 a 1 |
| 8 | duration_min | Duración en minutos | ~0,5 a 10 |
| 9 | instrumentalness | Probabilidad de no tener voz | 0 a 1 |
| 10 | liveness | Presencia de público | 0 a 1 |

**El orden es crítico.** Si las columnas llegan desordenadas el modelo predice mal
sin lanzar ningún error. Por eso nunca se escribe la lista a mano:

```python
features = joblib.load("models/features.pkl")
```

## Cómo se entrenó

1. **80% entrenamiento / 20% prueba**, estratificado (3.595 y 899 canciones).
2. **Baseline explícito** con `DummyClassifier`: un modelo que siempre dice "no hit"
   saca 72,7% de accuracy. Cualquier resultado se compara contra esa vara.
3. **Comparación con validación cruzada de 5 pliegues** entre `RandomForestClassifier`
   y `LogisticRegression`, usando ROC-AUC como criterio. Ganó el Random Forest.
4. **`class_weight='balanced_subsample'`** para compensar el desbalance de clases.
5. **Umbral de decisión elegido, no heredado:** en vez del 0,50 por defecto, se busca
   el umbral que maximiza la exactitud balanceada, calculado por validación cruzada
   sobre el conjunto de entrenamiento (nunca sobre el de prueba). Resultado: **0,39**.

## Resultados sobre el 20% de prueba

| Métrica | Valor | Referencia |
|---|---|---|
| **ROC-AUC** | **0,744** | 0,500 = azar |
| **Exactitud balanceada** | **0,671** | 0,500 = azar |
| Recall de hits | 80,0% | detecta 8 de cada 10 hits reales |
| Precisión de hits | 39,6% | cuando dice "hit", acierta 4 de cada 10 |
| Accuracy simple | 61,3% | baseline: 72,7% |

**La accuracy quedó bajo el baseline a propósito.** El umbral 0,39 sacrifica aciertos
en la clase mayoritaria para no perderse hits. Es una decisión de negocio: para un
sello discográfico, dejar pasar un éxito cuesta más que escuchar una canción de más.
Las métricas que sí miden aprendizaje real — ROC-AUC y exactitud balanceada — están
muy por encima del azar.

## Qué pesa más en la decisión

1. instrumentalness (19,6%)
2. loudness (14,2%)
3. duration_min (10,6%)
4. acousticness (10,0%)
5. energy (9,9%)

## Cómo usarlo

```python
import joblib
import pandas as pd

modelo = joblib.load("models/model.pkl")
features = joblib.load("models/features.pkl")
umbral = 0.39   # o leerlo de models/metrics.json

datos = pd.DataFrame([[0.85, 0.75, 0.60, 95, -4, 0.15, 0.05, 3.2, 0.0, 0.12]],
                     columns=features)

probabilidad = modelo.predict_proba(datos)[0][1]   # probabilidad de ser hit
es_hit = probabilidad >= umbral
```

## Limitación honesta

Ninguna característica de audio se correlaciona fuerte con la popularidad (la más alta
es el volumen, con 0,20). El sonido explica solo una parte del éxito; el resto lo ponen
el artista, el marketing y las playlists, que no están en este dataset. Ningún modelo
entrenado solo con audio va a rendir mucho mejor que este.
