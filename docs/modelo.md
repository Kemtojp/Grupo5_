# Modelo de Predicción — Documentación

## Qué se hizo

Se entrenó un modelo de Machine Learning para predecir si una canción tiene potencial de ser un hit comercial o no, basándose en 7 características de audio.

El modelo usa el dataset limpio de 4,494 canciones (`data/spotify_clean.csv`) que se generó en el notebook de limpieza.

## Archivos generados

- `models/model.pkl` — El modelo entrenado. Se carga con `joblib.load()` y ya queda listo para predecir.
- `models/features.pkl` — La lista de features en el orden que el modelo espera recibirlos. Importante para que Streamlit pase los datos bien.
- `notebooks/02_model_training.ipynb` — El notebook con todo el proceso paso a paso.

## Features usadas

El modelo recibe estos 7 valores para hacer la predicción:

| Feature | Qué es | Rango |
|---------|--------|-------|
| danceability | Qué tan bailable | 0 a 1 |
| energy | Intensidad | 0 a 1 |
| valence | Alegre vs triste | 0 a 1 |
| tempo | BPM | ~50 a 240 |
| loudness | Volumen (dB) | -48 a 1 |
| speechiness | Voz hablada vs cantada | 0 a 1 |
| acousticness | Acústico vs electrónico | 0 a 1 |

**Orden crítico:** El modelo espera los datos exactamente en este orden (de arriba a abajo). Si se pasan desordenados, la predicción sale mal. Por eso existe `features.pkl` — para no tener que recordarlo de memoria. Se usa así:

```python
features = joblib.load("models/features.pkl")
# Devuelve: ['danceability', 'energy', 'valence', 'tempo', 'loudness', 'speechiness', 'acousticness']
```

## Cómo funciona

1. **Se separaron los datos en 80% entrenamiento y 20% prueba.**
   Le dimos 3,595 canciones para que aprenda los patrones (80%)
Le hicimos un "examen" con 899 canciones que nunca vio (20%)
Sacó 64.7% → no se memorizó, realmente aprendió algo (aunque no es perfecto)
2. Se usó un RandomForestClassifier de scikit-learn con 200 árboles
3. Se aplicó `class_weight='balanced'` porque hay más no-hits (73%) que hits (27%)
4. El modelo se evaluó con los datos de prueba (el 20% que nunca vio)

## Resultados

- **Accuracy general:** 64.7%
- De los hits reales, detectó el 66% (recall)
- De los que dijo "hit", acertó el 41% (precision)

Las features que más pesan para decidir si algo es hit:

1. loudness (volumen)
2. acousticness
3. energy

## Pruebas rápidas

Se probó con dos canciones simuladas:

- Reggaetón tipo Bad Bunny (bailable, energético, fuerte) → Predijo **HIT** con 64% de confianza
- Balada acústica triste (lenta, suave, triste) → Predijo **NO HIT** con 78% de confianza

## Cómo usarlo en Streamlit

```python
import joblib
import pandas as pd

modelo = joblib.load("models/model.pkl")
features = joblib.load("models/features.pkl")

# Ejemplo: armar datos desde los sliders
datos = pd.DataFrame([[0.85, 0.75, 0.60, 95, -4, 0.15, 0.05]], columns=features)

# Predecir
prediccion = modelo.predict(datos)[0]           # 1 = hit, 0 = no hit
probabilidad = modelo.predict_proba(datos)[0]   # [prob_no_hit, prob_hit]
```
