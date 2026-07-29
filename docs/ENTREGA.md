# 📦 Guía de entrega — Grupo 5

Todo lo que falta para cerrar el proyecto, con responsable y orden de ejecución.
Fecha objetivo: **jueves 30 de julio**.

---

## 🔴 Bloque 1 — Subir el código al repositorio (30 min)

**Responsable: Juan (Git & Docs Lead)**

```bash
cd Grupo5_
git pull origin main
# copiar aquí los archivos nuevos: app.py, charts.py, requirements.txt,
# .streamlit/config.toml, notebooks/03_model_retraining.ipynb,
# notebooks/train_model.py, models/ actualizado, README.md, docs/ENTREGA.md
git add .
git commit -m "feat: dashboard Streamlit, gráficos Plotly y modelo reentrenado"
git push origin main
```

> ⚠️ El modelo cambió: ahora usa **10 variables** en vez de 7 (se agregaron
> `duration_min`, `instrumentalness` y `liveness`, que subieron el ROC-AUC de 0,708 a
> 0,743). `models/features.pkl` es la fuente de verdad del orden; la app lo lee de ahí.
> Dante debe revisar `notebooks/03_model_retraining.ipynb` antes del push.

---

## 🔴 Bloque 2 — Publicar la app (20 min)

**Responsable: Luis (App Architect)**

1. Entrar a [share.streamlit.io](https://share.streamlit.io) e iniciar sesión con GitHub.
2. **New app** → seleccionar el repositorio `Grupo5_`, rama `main`, archivo `app.py`.
3. **Deploy**. El primer build tarda 2–4 minutos.
4. Copiar la URL pública que queda (algo como `https://grupo5-hit-predictor.streamlit.app`).
5. Pegarla en el `README.md`, en las dos líneas marcadas como *pendiente*.

**Si el deploy falla**, casi siempre es una de estas tres:

| Síntoma | Causa | Arreglo |
|---|---|---|
| `ModuleNotFoundError` | falta una librería | revisar que `requirements.txt` esté en la raíz del repo |
| `InconsistentVersionWarning` o error al cargar `model.pkl` | la versión de scikit-learn del servidor no coincide con la que generó el pickle | las versiones ya están fijadas en `requirements.txt`; no quitarlas |
| `FileNotFoundError: data/spotify_clean.csv` | el CSV no se subió | verificar que `.gitignore` no lo esté excluyendo |

---

## 🟡 Bloque 3 — Cerrar el README (20 min)

**Responsable: Juan**

- [ ] Pegar la URL de la app publicada (aparece 2 veces en el README).
- [ ] Abrir la [ficha del dataset en Kaggle](https://www.kaggle.com/datasets/solomonameh/spotify-music-dataset)
      y copiar la **licencia exacta** del recuadro "License". La rúbrica exige licencia
      verificable, así que no se inventa. Actualizar también `LICENCIA_DATASET` en `app.py`.
- [ ] Confirmar que `REPO_URL` en `app.py` apunta al repositorio real.
- [ ] Tomar 3 capturas de la app (una por pestaña principal), guardarlas en
      `docs/capturas/` y enlazarlas al final del README.

---

## 🟡 Bloque 4 — Pull Request al repositorio del curso (20 min)

**Responsable: Juan**

El curso pide **un solo Pull Request por equipo** al repo
[`davidlealo/sic_2026_c-p_cohort_2`](https://github.com/davidlealo/sic_2026_c-p_cohort_2),
con el proyecto dentro de `/proyectos/nombre-del-equipo/`.

```bash
# 1. Hacer fork del repo del curso desde la web de GitHub
git clone https://github.com/<tu-usuario>/sic_2026_c-p_cohort_2.git
cd sic_2026_c-p_cohort_2
git checkout -b grupo5-hit-predictor

# 2. Copiar el proyecto completo dentro de la carpeta que pide el curso
mkdir -p proyectos/grupo5
cp -r ../Grupo5_/* proyectos/grupo5/
rm -rf proyectos/grupo5/.git

# 3. Subir y abrir el PR
git add proyectos/grupo5
git commit -m "Grupo 5 - Hit Predictor & Trendy Dashboard"
git push origin grupo5-hit-predictor
```

Luego, en GitHub: **Compare & pull request** → base `davidlealo/sic_2026_c-p_cohort_2:main`.

**Descripción del PR** (copiar y pegar):

> **Grupo 5 — Hit Predictor & Trendy Dashboard**
>
> Pregunta de análisis: ¿se puede saber si una canción va a ser un éxito solo a partir
> de cómo suena?
>
> - App publicada: `<URL de Streamlit Cloud>`
> - Dataset: Spotify Music Dataset (Kaggle), 4.494 canciones tras limpieza
> - Notebooks: limpieza, entrenamiento y reentrenamiento con evaluación contra baseline
> - Integrantes: Jeancarlo Cuesta, Dante, Carolina Naranjo, Luis Rojas, Juan Velásquez

⚠️ **Confirmar con el profesor** el nombre exacto de la carpeta y la fecha límite del PR:
en el repo del curso esas dos casillas todavía figuran como *(Por definir)*.

---

## 🟢 Bloque 5 — Presentación (1 hora de preparación)

**Responsable: Juan, con todo el equipo**

El curso pide **7 minutos de presentación + 3 de preguntas**, con la app abierta en
pantalla. No son 10 minutos de exposición.

### Guion cronometrado (7:00)

| Tiempo | Quién | Qué dice |
|---|---|---|
| 0:00–0:45 | Jeancarlo | **El problema.** La industria musical mueve miles de millones apostando a qué canción va a pegar. Nuestra pregunta: ¿se puede predecir eso solo escuchando cómo suena la canción? |
| 0:45–1:30 | Jeancarlo | **Los datos.** 4.494 canciones de Spotify, 10 atributos de audio. Definimos hit como popularidad ≥ 70. Mencionar la limitación de las fechas de álbum antes de que la pregunten. |
| 1:30–3:00 | Carolina | **Demo módulo 1 y 2.** Mostrar la evolución del sonido en vivo, mover el filtro de género. Rematar con la matriz de correlación: *"ninguna característica pasa de 0,20 con la popularidad"*. |
| 3:00–4:30 | Luis | **Demo del simulador.** Cargar el preset de reggaetón, evaluar, mostrar el resultado y la sugerencia. Luego cambiar a la balada triste y comparar. |
| 4:30–5:45 | Dante | **El modelo, sin maquillaje.** ROC-AUC 0,744 contra 0,50 de azar. Explicar por qué no usamos accuracy: el baseline tramposo saca 72,7%. Explicar la decisión del umbral. |
| 5:45–7:00 | Juan | **La conclusión.** El sonido abre la puerta pero no garantiza la entrada. Qué faltaría para mejorar: datos de artista, playlists, marketing. |

### Preguntas que casi seguro van a hacer — y la respuesta

**"¿Por qué su accuracy es peor que el baseline?"**
Porque elegimos el umbral a propósito para no perdernos hits: tenemos 80% de recall.
Con umbral 0,50 la accuracy sube, pero detectamos menos de la mitad de los hits. En este
problema, dejar pasar un éxito cuesta más que revisar una canción de más. Además la
accuracy no sirve con clases desbalanceadas: por eso reportamos ROC-AUC y exactitud
balanceada, donde sí superamos al azar con holgura.

**"¿Por qué el gráfico no parte en los años 60?"**
Porque el dataset tiene 11 canciones anteriores a 1970 y 2.800 de los 2020. Un promedio
sobre 3 canciones no es una tendencia. Preferimos graficar solo el tramo donde los datos
sostienen la afirmación.

**"¿Sirve realmente para algo este modelo?"**
Como filtro previo, sí: si un sello recibe 500 demos, el modelo ordena la fila y detecta
8 de cada 10 candidatos reales. Como oráculo, no, y nuestra propia matriz de correlación
explica por qué: el audio no contiene la información de artista, promoción ni playlists.

**"¿Qué es la popularidad de Spotify?"**
Un puntaje de 0 a 100 que calcula Spotify según reproducciones recientes. Es una medida
de éxito *actual*, no histórico — otra limitación que asumimos.

### Diapositivas (máximo 6)

1. Portada: título, integrantes, la pregunta.
2. El problema y por qué importa.
3. Dataset y metodología (incluir la limitación conocida).
4. **Demo en vivo** — solo un marcador, la app hace el trabajo.
5. El modelo: ROC-AUC vs. baseline, y qué significa.
6. Conclusión y próximos pasos.

---

## ✅ Checklist final antes de entregar

- [ ] `streamlit run app.py` levanta sin errores en el computador de al menos dos integrantes
- [ ] La URL pública abre desde un celular con datos móviles (no solo desde el wifi de la casa)
- [ ] El README tiene la URL, la licencia del dataset y las capturas
- [ ] El PR está abierto en el repo del curso
- [ ] Los 5 integrantes ensayaron su tramo del guion al menos una vez cronometrado
- [ ] Alguien tiene capturas de pantalla o un video de respaldo, por si el wifi de la sala falla
