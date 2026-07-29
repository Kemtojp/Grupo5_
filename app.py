"""
app.py — Hit Predictor & Trendy Dashboard
=========================================
Grupo 5 · Samsung Innovation Campus Chile 2026 — Cohort 2

Pregunta de análisis:
    ¿Qué características de audio distinguen a una canción exitosa en Spotify,
    y se puede predecir el éxito solo a partir de cómo suena?

Correr en local:   streamlit run app.py
"""

from pathlib import Path

import joblib
import json
import numpy as np
import pandas as pd
import streamlit as st

import charts

RAIZ = Path(__file__).resolve().parent

# TODO equipo: reemplazar por la URL real del repositorio del Grupo 5.
REPO_URL = "https://github.com/Kemtojp/hit-predictor-spotify"

# TODO equipo: abrir la página del dataset en Kaggle y copiar aquí la licencia
# exacta que aparece en el recuadro "License". La rúbrica del curso exige
# licencia verificable, así que no la inventamos.
LICENCIA_DATASET = "ver ficha del dataset en Kaggle (confirmar antes de la entrega)"

st.set_page_config(
    page_title="Hit Predictor & Trendy Dashboard",
    page_icon="🎵",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ---------------------------------------------------------------------------
# CARGA DE DATOS Y MODELO (en caché: se ejecuta una sola vez)
# ---------------------------------------------------------------------------
@st.cache_data
def cargar_datos() -> pd.DataFrame:
    return charts.preparar(pd.read_csv(RAIZ / "data" / "spotify_clean.csv"))


@st.cache_resource
def cargar_modelo():
    modelo = joblib.load(RAIZ / "models" / "model.pkl")
    features = joblib.load(RAIZ / "models" / "features.pkl")
    metricas = json.loads((RAIZ / "models" / "metrics.json").read_text())
    return modelo, features, metricas


df = cargar_datos()
modelo, FEATURES, METRICAS = cargar_modelo()
UMBRAL = METRICAS["umbral"]


def miles(n: int) -> str:
    """4494 -> '4.494' (separador de miles en formato chileno)."""
    return f"{n:,}".replace(",", ".")

# Configuración de los sliders del simulador: (mín, máx, default, paso, ayuda)
CONFIG_SLIDERS = {
    "danceability": (0.0, 1.0, 0.50, 0.01, "0.9 = Despacito · 0.2 = Bohemian Rhapsody"),
    "energy": (0.0, 1.0, 0.50, 0.01, "0.95 = Metallica · 0.15 = balada suave"),
    "valence": (0.0, 1.0, 0.50, 0.01, "0.95 = Happy (Pharrell) · 0.1 = Someone Like You"),
    "tempo": (50.0, 220.0, 120.0, 1.0, "70 = balada · 120 = pop · 180 = punk"),
    "loudness": (-40.0, 0.0, -7.0, 0.5, "-3 dB = reggaetón fuerte · -15 dB = jazz suave"),
    "speechiness": (0.0, 1.0, 0.10, 0.01, "0.8 = rap o podcast · 0.03 = melodía pura"),
    "acousticness": (0.0, 1.0, 0.20, 0.01, "0.95 = guitarra unplugged · 0.05 = EDM"),
    "duration_min": (0.5, 10.0, 3.30, 0.1, "El promedio actual ronda los 3 minutos"),
    "instrumentalness": (0.0, 1.0, 0.02, 0.01, "1.0 = sin voz · 0.0 = canción cantada"),
    "liveness": (0.0, 1.0, 0.15, 0.01, "0.8 = grabada en vivo · 0.1 = estudio"),
}

GLOSARIO = {
    "Danceability (Bailabilidad)": "Qué tan apta es la canción para bailar, según ritmo, estabilidad del beat y fuerza. 0 = imposible bailarla, 1 = pista de baile.",
    "Energy (Energía)": "Sensación de intensidad y actividad. Una canción con energía alta se siente rápida, fuerte y ruidosa.",
    "Valence (Positividad)": "Qué tan alegre suena. Valores altos suenan felices y eufóricos; valores bajos, tristes o melancólicos.",
    "Tempo": "Velocidad de la canción en pulsos por minuto (BPM).",
    "Loudness (Volumen)": "Volumen promedio en decibeles. Va de -60 dB (casi silencio) a 0 dB.",
    "Speechiness": "Cuánta palabra hablada tiene. Alto en rap y podcasts, bajo en música instrumental o melódica.",
    "Acousticness": "Confianza de que la canción es acústica (guitarra, piano) en vez de electrónica.",
    "Instrumentalness": "Probabilidad de que no tenga voz cantada.",
    "Liveness": "Detecta público en la grabación: valores altos sugieren una versión en vivo.",
    "Popularidad": "Puntaje de Spotify de 0 a 100 basado en reproducciones recientes. Definimos hit como popularidad ≥ 70.",
}


# ---------------------------------------------------------------------------
# BARRA LATERAL — FILTROS Y GLOSARIO
# ---------------------------------------------------------------------------
with st.sidebar:
    st.title("🎵 Hit Predictor")
    st.caption("Grupo 5 · Samsung Innovation Campus Chile 2026")

    st.subheader("Filtros")
    generos = sorted(df["playlist_genre"].dropna().unique())
    sel_generos = st.multiselect(
        "Géneros", generos, default=[],
        help="Vacío = todos los géneros. Afecta a los módulos 1 y 2.",
    )

    anio_min, anio_max = int(df["anio"].min()), int(df["anio"].max())
    sel_anios = st.slider(
        "Rango de años (fecha del álbum)", anio_min, anio_max, (1990, anio_max), step=1,
    )

    solo_hits = st.checkbox("Ver solo hits (popularidad ≥ 70)", value=False)

    st.divider()
    with st.expander("📖 Glosario de términos de Spotify"):
        for termino, definicion in GLOSARIO.items():
            st.markdown(f"**{termino}** — {definicion}")

    st.divider()
    st.caption(f"[Código fuente en GitHub]({REPO_URL})")


# Aplicar filtros.
# mask_base = año + género. dff = mask_base + el check de "solo hits".
# La comparación Hit vs Canción común necesita las dos clases, así que usa
# mask_base y no dff: si no, al marcar "solo hits" el radar se quedaría sin
# con qué comparar.
mask_base = df["anio"].between(*sel_anios)
if sel_generos:
    mask_base &= df["playlist_genre"].isin(sel_generos)

mask = mask_base & (df["is_hit"] == 1) if solo_hits else mask_base
dff = df[mask]
df_comparacion = df[mask_base]


# ---------------------------------------------------------------------------
# ENCABEZADO E INDICADORES
# ---------------------------------------------------------------------------
st.title("Hit Predictor & Trendy Dashboard")
st.markdown(
    f"**¿Qué hace que una canción sea un éxito?** Analizamos **{miles(len(df))}** "
    "canciones de Spotify y entrenamos un modelo que estima el potencial comercial "
    "de una canción solo a partir de cómo suena."
)

if dff.empty:
    st.warning("Ningún dato cumple con los filtros seleccionados. Ajusta los filtros en la barra lateral.")
    st.stop()

k1, k2, k3, k4 = st.columns(4)
k1.metric("Canciones analizadas", miles(len(dff)),
          help="Cantidad de canciones que cumplen los filtros actuales.")
k2.metric("Son hit", f"{dff['is_hit'].mean():.1%}",
          help="Porcentaje con popularidad de Spotify ≥ 70.")
k3.metric("Popularidad promedio", f"{dff['track_popularity'].mean():.1f}",
          help="Puntaje de Spotify de 0 a 100.")
k4.metric("Capacidad del modelo (ROC-AUC)", f"{METRICAS['roc_auc']:.2f}",
          help="0.50 sería azar puro, 1.00 sería perfecto. Ver la pestaña Ficha técnica.")

st.divider()

tab1, tab2, tab3, tab4 = st.tabs(
    ["📈 Evolución histórica", "🔍 Anatomía de un hit", "🎧 Hit Predictor", "📋 Ficha técnica"]
)


# ---------------------------------------------------------------------------
# MÓDULO 1 — LA EVOLUCIÓN DEL SONIDO
# ---------------------------------------------------------------------------
with tab1:
    st.subheader("¿Cómo cambió la música en las últimas décadas?")
    st.plotly_chart(charts.grafico_evolucion_atributos(dff), use_container_width=True)
    st.plotly_chart(charts.grafico_evolucion_duracion(dff), use_container_width=True)

    with st.expander("Ver los datos detrás de estos gráficos"):
        tabla = (
            dff[dff["anio"] >= charts.ANIO_MIN_CONFIABLE]
            .groupby("anio")
            .agg(
                canciones=("is_hit", "size"),
                bailabilidad=("danceability", "mean"),
                energia=("energy", "mean"),
                positividad=("valence", "mean"),
                duracion_min=("duration_min", "mean"),
            )
            .round(2)
        )
        st.dataframe(tabla, use_container_width=True)

    st.info(
        "**Por qué el gráfico empieza en 1990.** El dataset tiene solo 11 canciones "
        "anteriores a 1970 y 2.800 de la década de 2020. Un promedio calculado sobre "
        "3 canciones no es una tendencia, es ruido. Además, la fecha corresponde al "
        "**álbum**, así que las reediciones y remasterizaciones aparecen con fecha "
        "moderna. Preferimos graficar solo el tramo donde los datos aguantan la pregunta.",
        icon="ℹ️",
    )


# ---------------------------------------------------------------------------
# MÓDULO 2 — ANATOMÍA DE UN HIT
# ---------------------------------------------------------------------------
with tab2:
    st.subheader("¿En qué se diferencia un hit de una canción cualquiera?")

    col_a, col_b = st.columns([1, 1])
    with col_a:
        st.plotly_chart(charts.grafico_radar(df_comparacion), use_container_width=True)
    with col_b:
        st.plotly_chart(charts.grafico_hits_por_genero(dff), use_container_width=True)

    st.plotly_chart(charts.grafico_correlacion(dff), use_container_width=True)

    st.warning(
        "**El hallazgo incómodo.** Ninguna característica de audio se correlaciona "
        "fuerte con la popularidad: la más alta es el volumen, con apenas 0,20. "
        "Es decir, **cómo suena una canción explica solo una parte pequeña de su éxito**. "
        "El resto lo ponen el artista, el marketing, las playlists y el momento cultural, "
        "cosas que este dataset no mide.",
        icon="⚠️",
    )


# ---------------------------------------------------------------------------
# MÓDULO 3 — HIT PREDICTOR (SIMULADOR)
# ---------------------------------------------------------------------------
with tab3:
    st.subheader("Diseña tu canción y mide su potencial")
    st.caption(
        "Mueve los controles para construir una canción imaginaria. El modelo estima "
        "la probabilidad de que alcance popularidad ≥ 70 en Spotify."
    )

    presets = {
        "Personalizado": None,
        "Reggaetón tipo Bad Bunny": dict(danceability=0.85, energy=0.75, valence=0.60, tempo=95.0,
                                         loudness=-4.0, speechiness=0.15, acousticness=0.05,
                                         duration_min=3.2, instrumentalness=0.0, liveness=0.12),
        "Balada acústica triste": dict(danceability=0.25, energy=0.20, valence=0.10, tempo=72.0,
                                       loudness=-14.0, speechiness=0.03, acousticness=0.90,
                                       duration_min=4.1, instrumentalness=0.0, liveness=0.11),
        "Techno de club": dict(danceability=0.78, energy=0.92, valence=0.35, tempo=128.0,
                               loudness=-6.0, speechiness=0.05, acousticness=0.01,
                               duration_min=6.0, instrumentalness=0.85, liveness=0.20),
    }
    preset = st.selectbox("Punto de partida", list(presets), index=0)
    base = presets[preset]

    col_izq, col_der = st.columns([1.15, 1])

    with col_izq:
        valores = {}
        c1, c2 = st.columns(2)
        for i, f in enumerate(FEATURES):
            minimo, maximo, defecto, paso, ayuda = CONFIG_SLIDERS[f]
            inicial = float(base[f]) if base else defecto
            destino = c1 if i % 2 == 0 else c2
            valores[f] = destino.slider(
                charts.NOMBRES.get(f, f), minimo, maximo, inicial, paso,
                help=ayuda, key=f"{preset}_{f}",
            )
        evaluar = st.button("🎯 Evaluar potencial", type="primary", use_container_width=True)

    with col_der:
        if evaluar:
            entrada = pd.DataFrame([[valores[f] for f in FEATURES]], columns=FEATURES)
            probabilidad = float(modelo.predict_proba(entrada)[0][1])

            st.plotly_chart(charts.grafico_probabilidad(probabilidad, UMBRAL),
                            use_container_width=True)

            if probabilidad >= UMBRAL:
                st.success(
                    f"**Potencial de hit: {probabilidad:.0%}.** Está por encima del umbral "
                    f"de decisión del modelo ({UMBRAL:.0%}). Suena como las canciones que "
                    "sí llegaron a popularidad alta.",
                    icon="🔥",
                )
            else:
                st.warning(
                    f"**Potencial de hit: {probabilidad:.0%}.** Está por debajo del umbral "
                    f"de decisión ({UMBRAL:.0%}). Se parece más al montón que a un éxito.",
                    icon="🎚️",
                )

            # Sugerencia de ajuste: probamos mover cada atributo hacia arriba y hacia
            # abajo y nos quedamos con el cambio que más sube la probabilidad.
            mejor = None
            for f in FEATURES:
                minimo, maximo, *_ = CONFIG_SLIDERS[f]
                paso_test = (maximo - minimo) * 0.15
                for direccion in (+1, -1):
                    prueba = entrada.copy()
                    nuevo = float(np.clip(valores[f] + direccion * paso_test, minimo, maximo))
                    if nuevo == valores[f]:
                        continue
                    prueba.loc[0, f] = nuevo
                    p = float(modelo.predict_proba(prueba)[0][1])
                    if mejor is None or p > mejor[2]:
                        mejor = (f, nuevo, p, direccion)

            if mejor and mejor[2] > probabilidad + 0.005:
                f, nuevo, p, direccion = mejor
                verbo = "subir" if direccion > 0 else "bajar"
                st.info(
                    f"**Sugerencia:** {verbo} **{charts.NOMBRES.get(f, f)}** a "
                    f"**{nuevo:.2f}** llevaría el potencial a **{p:.0%}** "
                    f"(+{p - probabilidad:.0%}).",
                    icon="💡",
                )
            else:
                st.info("Ningún ajuste individual mejora de forma apreciable este resultado.",
                        icon="💡")
        else:
            st.info(
                "Configura los controles de la izquierda y presiona **Evaluar potencial**.",
                icon="👈",
            )

    st.caption(
        f"Recordatorio honesto: el modelo acierta a un ROC-AUC de {METRICAS['roc_auc']:.2f} "
        "(0,50 sería lanzar una moneda). Es un indicador de potencial, no un oráculo."
    )


# ---------------------------------------------------------------------------
# MÓDULO 4 — FICHA TÉCNICA
# ---------------------------------------------------------------------------
with tab4:
    st.subheader("Ficha técnica")

    st.markdown("#### El hallazgo principal, en simple")
    st.markdown(
        """
Analizamos **4.494 canciones de Spotify** para responder una pregunta concreta:
¿se puede saber si una canción va a ser un éxito solo escuchando cómo suena?

**La respuesta corta es: en parte.** Los hits comparten un perfil reconocible —
son más fuertes, más bailables y menos acústicos que el promedio— y nuestro modelo
detecta ese patrón bastante mejor que el azar. Pero ninguna característica de audio,
por sí sola, se acerca a explicar la popularidad.

Dicho en simple: **el sonido abre la puerta, pero no garantiza la entrada.**
Una canción puede tener todos los ingredientes de un hit y no despegar, porque el
éxito también depende de quién la canta, cuánta promoción tiene y en qué playlists
entra. Nada de eso está en los datos, y por eso ningún modelo honesto que use solo
audio va a acertar mucho más que el nuestro.
        """
    )

    st.divider()
    st.markdown("#### Rendimiento del modelo")

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("ROC-AUC", f"{METRICAS['roc_auc']:.3f}", help="0,50 = azar. Mide qué tan bien ordena el modelo las canciones por potencial.")
    m2.metric("Exactitud balanceada", f"{METRICAS['balanced_accuracy']:.3f}", help="Promedio de aciertos en cada clase. 0,50 = azar.")
    m3.metric("Recall de hits", f"{METRICAS['recall']:.1%}", help="De los hits reales, cuántos detecta.")
    m4.metric("Precisión de hits", f"{METRICAS['precision']:.1%}", help="De los que llama hit, cuántos lo son de verdad.")

    st.error(
        f"""**Por qué NO mostramos la exactitud simple como titular.**
El {(1 - METRICAS['tasa_hits']):.0%} de las canciones no son hit. Un modelo tramposo que
dijera siempre *"no es hit"* alcanzaría {METRICAS['baseline_accuracy']:.1%} de exactitud
sin haber aprendido nada. Por eso reportamos ROC-AUC y exactitud balanceada, que sí
comparan contra el azar real ({METRICAS['roc_auc']:.3f} y
{METRICAS['balanced_accuracy']:.3f} frente a 0,500). Nuestro modelo prioriza
**detectar hits** ({METRICAS['recall']:.0%} de recall) aunque eso le cueste falsas
alarmas: para un sello discográfico es más caro dejar pasar un éxito que escuchar
una canción de más.""",
        icon="📐",
    )

    st.plotly_chart(charts.grafico_importancias(METRICAS["importancias"]),
                    use_container_width=True)

    st.divider()
    col_i, col_d = st.columns(2)
    with col_i:
        st.markdown(
            f"""
#### Dataset
- **Fuente:** [Spotify Music Dataset](https://www.kaggle.com/datasets/solomonameh/spotify-music-dataset)
  de *solomonameh* en Kaggle, combinando los archivos de alta y baja popularidad.
- **Licencia:** {LICENCIA_DATASET}
- **Volumen:** {miles(METRICAS['n_total'])} canciones únicas tras limpieza.
- **Variable objetivo:** `is_hit` = 1 si la popularidad de Spotify es ≥ 70.
- **Balance:** {METRICAS['tasa_hits']:.1%} hits · {1 - METRICAS['tasa_hits']:.1%} no hits.
"""
        )
    with col_d:
        matriz = METRICAS["matriz_confusion"]
        st.markdown(
            f"""
#### Modelo
- **Algoritmo:** {METRICAS['modelo']} (scikit-learn), elegido por validación cruzada
  de 5 pliegues contra una regresión logística.
- **Entrenamiento / prueba:** {miles(METRICAS['n_train'])} / {miles(METRICAS['n_test'])} canciones.
- **Umbral de decisión:** {METRICAS['umbral']:.2f} (optimiza exactitud balanceada,
  no el 0,50 por defecto).
- **Matriz de confusión (prueba):** {matriz[0][0]} y {matriz[1][1]} aciertos ·
  {matriz[0][1]} falsas alarmas · {matriz[1][0]} hits no detectados.
"""
        )

    st.divider()
    st.markdown(
        f"""
#### Equipo · Grupo 5
| Integrante | Rol |
|---|---|
| Jeancarlo Cuesta | Data Engineer — limpieza del dataset |
| Dante | ML Engineer — entrenamiento del modelo |
| Carolina Naranjo | Visualization Specialist — gráficos en Plotly |
| Luis Rojas | App Architect — dashboard en Streamlit |
| Juan Velásquez | Git, documentación y presentación |

🔗 **Repositorio:** [{REPO_URL}]({REPO_URL})
        """
    )
