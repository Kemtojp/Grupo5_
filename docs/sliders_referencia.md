# 🎚️ Sliders del Hit Predictor — Referencia

Estos son los parámetros que el usuario podrá ajustar en la app de Streamlit para simular una canción y predecir si será un **hit o no**.

---

## Sliders Definidos

| # | Slider | Rango | Default | ¿Qué mide? | Ejemplo fácil |
|---|--------|-------|---------|-------------|---------------|
| 1 | **Danceability** | 0.0 – 1.0 | 0.50 | Qué tan bailable es | 0.9 = Despacito, 0.2 = Bohemian Rhapsody |
| 2 | **Energy** | 0.0 – 1.0 | 0.50 | Intensidad / fuerza | 0.95 = Metallica, 0.15 = balada suave |
| 3 | **Valence** | 0.0 – 1.0 | 0.50 | Alegre vs triste | 0.95 = Happy (Pharrell), 0.1 = Someone Like You (Adele) |
| 4 | **Tempo** | 60 – 200 BPM | 120 | Velocidad de la canción | 70 = balada, 120 = pop, 180 = punk |
| 5 | **Loudness** | -60 – 0 dB | -7 | Volumen de masterización | -3 = reggaetón fuerte, -15 = jazz suave |
| 6 | **Speechiness** | 0.0 – 1.0 | 0.10 | Cuánto hablan vs cantan | 0.8 = rap/podcast, 0.03 = melódica |
| 7 | **Acousticness** | 0.0 – 1.0 | 0.20 | Acústico vs electrónico | 0.95 = guitarra unplugged, 0.05 = EDM |

---

## Flujo del Usuario

```
1. El usuario mueve los 7 sliders
2. Presiona el botón "Evaluar Potencial"
3. El modelo cargado (model.pkl) recibe los 7 valores
4. Devuelve: probabilidad de hit (0% - 100%)
5. Se muestra el veredicto en pantalla
```

---

## Ejemplo: Simulando un Reggaetón tipo Bad Bunny

| Slider | Valor |
|--------|-------|
| Danceability | 0.85 |
| Energy | 0.75 |
| Valence | 0.60 |
| Tempo | 95 BPM |
| Loudness | -4 dB |
| Speechiness | 0.15 |
| Acousticness | 0.05 |

**Resultado esperado:** Alta probabilidad de hit ✅

---

## Ejemplo: Simulando una Balada Acústica Triste

| Slider | Valor |
|--------|-------|
| Danceability | 0.25 |
| Energy | 0.20 |
| Valence | 0.10 |
| Tempo | 72 BPM |
| Loudness | -14 dB |
| Speechiness | 0.03 |
| Acousticness | 0.90 |

**Resultado esperado:** Baja probabilidad de hit ⚠️

---

> **Nota:** Estos 7 sliders corresponden a las variables de entrada (X) que usa el modelo entrenado con scikit-learn. La variable de salida (y) es `is_hit` (1 = hit, 0 = no hit).
