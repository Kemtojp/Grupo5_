# 🎚️ Sliders del Hit Predictor — Referencia

Parámetros que el usuario ajusta en la app para simular una canción y estimar si
sería un **hit**. Son las 10 variables de entrada del modelo, en el orden que
define `models/features.pkl`.

---

## Sliders definidos

| # | Slider | Rango | Default | ¿Qué mide? | Ejemplo fácil |
|---|--------|-------|---------|-------------|---------------|
| 1 | **Bailabilidad** (danceability) | 0,0 – 1,0 | 0,50 | Qué tan bailable es | 0,9 = Despacito · 0,2 = Bohemian Rhapsody |
| 2 | **Energía** (energy) | 0,0 – 1,0 | 0,50 | Intensidad / fuerza | 0,95 = Metallica · 0,15 = balada suave |
| 3 | **Positividad** (valence) | 0,0 – 1,0 | 0,50 | Alegre vs. triste | 0,95 = Happy (Pharrell) · 0,1 = Someone Like You |
| 4 | **Tempo** | 50 – 220 BPM | 120 | Velocidad | 70 = balada · 120 = pop · 180 = punk |
| 5 | **Volumen** (loudness) | -40 – 0 dB | -7 | Volumen de masterización | -3 = reggaetón fuerte · -15 = jazz suave |
| 6 | **Palabra hablada** (speechiness) | 0,0 – 1,0 | 0,10 | Cuánto habla vs. canta | 0,8 = rap o podcast · 0,03 = melodía pura |
| 7 | **Acústica** (acousticness) | 0,0 – 1,0 | 0,20 | Acústico vs. electrónico | 0,95 = guitarra unplugged · 0,05 = EDM |
| 8 | **Duración** (duration_min) | 0,5 – 10 min | 3,30 | Largo de la canción | El promedio actual ronda los 3 minutos |
| 9 | **Instrumentalidad** (instrumentalness) | 0,0 – 1,0 | 0,02 | Probabilidad de no tener voz | 1,0 = pista instrumental · 0,0 = cantada |
| 10 | **Sonido en vivo** (liveness) | 0,0 – 1,0 | 0,15 | Presencia de público | 0,8 = grabada en vivo · 0,1 = estudio |

> Los últimos tres se agregaron en el reentrenamiento (ver `docs/modelo.md`): subieron
> el ROC-AUC del modelo de 0,708 a 0,743.

---

## Flujo del usuario

```
1. El usuario elige un preset o mueve los 10 sliders
2. Presiona "Evaluar potencial"
3. La app arma un DataFrame con el orden de models/features.pkl
4. El modelo devuelve la probabilidad de hit (0% – 100%)
5. Se compara contra el umbral 0,39 y se muestra el veredicto
6. La app prueba mover cada slider y sugiere el ajuste que más sube la probabilidad
```

---

## Presets incluidos en la app

| Slider | Reggaetón tipo Bad Bunny | Balada acústica triste | Techno de club |
|---|---|---|---|
| Bailabilidad | 0,85 | 0,25 | 0,78 |
| Energía | 0,75 | 0,20 | 0,92 |
| Positividad | 0,60 | 0,10 | 0,35 |
| Tempo | 95 | 72 | 128 |
| Volumen | -4 | -14 | -6 |
| Palabra hablada | 0,15 | 0,03 | 0,05 |
| Acústica | 0,05 | 0,90 | 0,01 |
| Duración | 3,2 | 4,1 | 6,0 |
| Instrumentalidad | 0,00 | 0,00 | 0,85 |
| Sonido en vivo | 0,12 | 0,11 | 0,20 |

Sirven para la demo de la presentación: se carga un preset, se evalúa y se compara
con otro sin tener que mover 10 controles en vivo delante del curso.
