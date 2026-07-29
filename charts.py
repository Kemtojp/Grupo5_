"""
charts.py — Funciones de visualizacion del Hit Predictor & Trendy Dashboard
===========================================================================
Grupo 5 · Samsung Innovation Campus Chile 2026 — Cohort 2
Responsable: Visualization Specialist

Todas las funciones son PURAS: reciben un DataFrame ya filtrado y devuelven
una figura de Plotly. No leen archivos, no usan Streamlit y no imprimen nada.
Asi se pueden probar sueltas desde un notebook:

    import pandas as pd, charts
    df = pd.read_csv("data/spotify_clean.csv")
    charts.grafico_evolucion_atributos(charts.preparar(df)).show()
"""

from __future__ import annotations

import pandas as pd
import plotly.graph_objects as go

# ---------------------------------------------------------------------------
# PALETA
# ---------------------------------------------------------------------------
# Paleta categorica validada para daltonismo (deutan/protan/tritan).
# El ORDEN es la garantia de accesibilidad: se asignan slots fijos, nunca se
# reciclan ni se generan colores nuevos.
AZUL = "#2a78d6"  # slot 1
NARANJA = "#eb6834"  # slot 2
AGUA = "#1baf7a"  # slot 3
ROJO = "#e34948"  # slot 8 — solo para el polo negativo de la escala divergente
GRIS_NEUTRO = "#f0efec"

TINTA = "#0b0b0b"
TINTA_SUAVE = "#52514e"
SUPERFICIE = "#ffffff"
REJILLA = "#e8e7e3"

# Etiquetas legibles para el publico no tecnico
NOMBRES = {
    "danceability": "Bailabilidad",
    "energy": "Energía",
    "valence": "Positividad",
    "tempo": "Tempo (BPM)",
    "loudness": "Volumen (dB)",
    "speechiness": "Palabra hablada",
    "acousticness": "Acústica",
    "instrumentalness": "Instrumentalidad",
    "liveness": "Sonido en vivo",
    "duration_min": "Duración (min)",
    "track_popularity": "Popularidad",
    "is_hit": "Es hit",
}

# Desde este año el dataset tiene volumen suficiente por año como para que un
# promedio anual signifique algo. Antes de 1990 hay menos de 400 canciones en
# total repartidas en 4 décadas: graficar eso seria ruido disfrazado de tendencia.
ANIO_MIN_CONFIABLE = 1990


def _layout(fig: go.Figure, titulo: str, subtitulo: str = "", alto: int = 420) -> go.Figure:
    """Estilo comun a todos los graficos: sobrio, sin adornos, texto en tinta."""
    encabezado = f"<b>{titulo}</b>"
    if subtitulo:
        encabezado += f"<br><span style='font-size:13px;color:{TINTA_SUAVE}'>{subtitulo}</span>"
    fig.update_layout(
        title=dict(text=encabezado, x=0, xanchor="left", font=dict(size=18, color=TINTA)),
        height=alto,
        margin=dict(l=10, r=90, t=80, b=40),
        paper_bgcolor=SUPERFICIE,
        plot_bgcolor=SUPERFICIE,
        font=dict(family="system-ui, -apple-system, sans-serif", size=13, color=TINTA_SUAVE),
        hoverlabel=dict(bgcolor="white", font_size=13, bordercolor=REJILLA),
        legend=dict(
            orientation="h", yanchor="bottom", y=1.0, xanchor="left", x=0,
            bgcolor="rgba(0,0,0,0)", font=dict(color=TINTA_SUAVE),
        ),
    )
    fig.update_xaxes(showgrid=False, linecolor=REJILLA, ticks="outside", tickcolor=REJILLA)
    fig.update_yaxes(gridcolor=REJILLA, zeroline=False, linecolor="rgba(0,0,0,0)")
    return fig


# ---------------------------------------------------------------------------
# PREPARACION
# ---------------------------------------------------------------------------
def _vacio(titulo: str, mensaje: str, alto: int = 300) -> go.Figure:
    """Estado vacío: un mensaje centrado, sin ejes ni rejilla fantasma."""
    fig = go.Figure()
    fig.add_annotation(
        text=mensaje, x=0.5, y=0.5, xref="paper", yref="paper",
        showarrow=False, font=dict(size=14, color=TINTA_SUAVE),
    )
    fig.update_layout(
        title=dict(text=f"<b>{titulo}</b>", x=0, xanchor="left", font=dict(size=18, color=TINTA)),
        height=alto, margin=dict(l=10, r=10, t=60, b=20),
        paper_bgcolor=SUPERFICIE, plot_bgcolor=SUPERFICIE,
        font=dict(family="system-ui, sans-serif", color=TINTA_SUAVE),
        xaxis=dict(visible=False), yaxis=dict(visible=False),
    )
    return fig


def preparar(df: pd.DataFrame) -> pd.DataFrame:
    """Agrega las columnas derivadas que necesitan los graficos.

    `track_album_release_date` viene con formatos mezclados (2024-08-16, 2019,
    1998-03) por eso se parsea con format='mixed'.
    """
    df = df.copy()
    fechas = pd.to_datetime(df["track_album_release_date"], errors="coerce", format="mixed")
    df["anio"] = fechas.dt.year
    df["decada"] = (df["anio"] // 10 * 10).astype("Int64")
    df["etiqueta_hit"] = df["is_hit"].map({1: "Hit", 0: "Canción común"})
    return df


# ---------------------------------------------------------------------------
# MODULO 1 — LA EVOLUCION DEL SONIDO
# ---------------------------------------------------------------------------
def grafico_evolucion_atributos(df: pd.DataFrame, minimo_por_anio: int = 15) -> go.Figure:
    """Lineas: como cambiaron bailabilidad, energia y positividad por año.

    Las tres variables comparten la misma escala 0–1, por eso pueden ir en un
    solo eje. La duracion y el tempo van en su propio grafico: mezclar escalas
    distintas en dos ejes Y es la forma mas rapida de mentir con un grafico.
    """
    atributos = ["danceability", "energy", "valence"]
    colores = {"danceability": AZUL, "energy": NARANJA, "valence": AGUA}

    base = df[df["anio"] >= ANIO_MIN_CONFIABLE]
    serie = base.groupby("anio").agg(
        n=("is_hit", "size"), **{a: (a, "mean") for a in atributos}
    ).reset_index()
    serie = serie[serie["n"] >= minimo_por_anio]

    if serie.empty:
        return _vacio("La evolución del sonido",
                     "No hay años con suficientes canciones para el filtro elegido.", 320)

    fig = go.Figure()

    for atributo in atributos:
        fig.add_trace(
            go.Scatter(
                x=serie["anio"], y=serie[atributo], name=NOMBRES[atributo],
                mode="lines", line=dict(color=colores[atributo], width=2),
                hovertemplate=(f"<b>{NOMBRES[atributo]}</b><br>Año %{{x}}<br>"
                               "Promedio: %{y:.2f}<br>%{customdata} canciones<extra></extra>"),
                customdata=serie["n"],
            )
        )
        # Etiqueta directa al final de cada linea: la identidad no depende solo
        # del color (requisito de accesibilidad).
        fig.add_annotation(
            x=serie["anio"].iloc[-1], y=serie[atributo].iloc[-1], text=NOMBRES[atributo],
            showarrow=False, xanchor="left", xshift=8,
            font=dict(size=12, color=colores[atributo]),
        )

    fig.update_yaxes(range=[0, 1], tickformat=".1f", title=None)
    fig.update_xaxes(title=None, dtick=5)
    fig.update_layout(hovermode="x unified", showlegend=False)
    return _layout(
        fig, "La evolución del sonido",
        f"Promedio anual de cada atributo · {int(serie['anio'].min())}–{int(serie['anio'].max())} "
        f"· solo años con {minimo_por_anio}+ canciones",
    )


def grafico_evolucion_duracion(df: pd.DataFrame, minimo_por_anio: int = 15) -> go.Figure:
    """Lineas: duracion promedio en minutos. Escala propia, grafico propio."""
    base = df[df["anio"] >= ANIO_MIN_CONFIABLE]
    serie = base.groupby("anio").agg(n=("is_hit", "size"), dur=("duration_min", "mean")).reset_index()
    serie = serie[serie["n"] >= minimo_por_anio]

    if serie.empty:
        return _vacio("¿Las canciones se acortaron?",
                     "No hay años con suficientes canciones para el filtro elegido.", 300)

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=serie["anio"], y=serie["dur"], name="Duración",
            mode="lines", line=dict(color=AZUL, width=2), fill="tozeroy",
            fillcolor="rgba(42,120,214,0.08)",
            hovertemplate="Año %{x}<br>%{y:.2f} min promedio<br>%{customdata} canciones<extra></extra>",
            customdata=serie["n"],
        )
    )
    fig.update_yaxes(title="minutos", rangemode="tozero")
    fig.update_xaxes(title=None, dtick=5)
    return _layout(
        fig, "¿Las canciones se acortaron?",
        "Duración promedio por año, en minutos", alto=340,
    )


# ---------------------------------------------------------------------------
# MODULO 2 — ANATOMIA DE UN HIT
# ---------------------------------------------------------------------------
def grafico_correlacion(df: pd.DataFrame, columnas: list[str] | None = None) -> go.Figure:
    """Mapa de calor de correlaciones. Escala DIVERGENTE con gris al centro:
    el cero tiene que verse como 'nada', no como un color mas."""
    columnas = columnas or [
        "danceability", "energy", "valence", "tempo", "loudness",
        "speechiness", "acousticness", "instrumentalness", "liveness",
        "duration_min", "track_popularity",
    ]
    columnas = [c for c in columnas if c in df.columns]
    matriz = df[columnas].corr().round(2)
    etiquetas = [NOMBRES.get(c, c) for c in columnas]

    fig = go.Figure(
        go.Heatmap(
            z=matriz.values, x=etiquetas, y=etiquetas,
            zmin=-1, zmax=1, zmid=0,
            colorscale=[[0.0, ROJO], [0.5, GRIS_NEUTRO], [1.0, AZUL]],
            xgap=2, ygap=2,  # separador de 2px entre celdas
            text=matriz.values, texttemplate="%{text:.2f}",
            textfont=dict(size=10, color=TINTA),
            hovertemplate="%{y} ↔ %{x}<br>Correlación: %{z:.2f}<extra></extra>",
            colorbar=dict(title=dict(text="corr.", side="right"), thickness=12, len=0.8, outlinewidth=0),
        )
    )
    fig.update_xaxes(tickangle=-40, showgrid=False)
    fig.update_yaxes(autorange="reversed", showgrid=False)
    return _layout(
        fig, "¿Qué atributos se mueven juntos?",
        "Correlación entre atributos. Azul = suben juntos · Rojo = uno sube y el otro baja · Gris = sin relación",
        alto=560,
    )


def grafico_radar(df: pd.DataFrame) -> go.Figure:
    """Radar: perfil acustico promedio de un hit vs una cancion comun.

    Solo se usan variables que ya viven en 0–1, para que el radar sea
    comparable sin normalizaciones inventadas.
    """
    ejes = ["danceability", "energy", "valence", "speechiness", "acousticness", "instrumentalness"]
    ejes = [e for e in ejes if e in df.columns]
    etiquetas = [NOMBRES[e] for e in ejes]

    if df.empty or df["is_hit"].nunique() < 2:
        return _vacio("Anatomía de un hit",
                      "El filtro actual no tiene hits y canciones comunes para comparar.", 380)

    fig = go.Figure()

    for grupo, color in ((1, NARANJA), (0, AZUL)):
        sub = df[df["is_hit"] == grupo]
        valores = [sub[e].mean() for e in ejes]
        nombre = "Hit (popularidad ≥ 70)" if grupo else "Canción común"
        fig.add_trace(
            go.Scatterpolar(
                r=valores + [valores[0]], theta=etiquetas + [etiquetas[0]],
                name=nombre, fill="toself",
                fillcolor=f"rgba({'235,104,52' if grupo else '42,120,214'},0.16)",
                line=dict(color=color, width=2),
                hovertemplate=f"<b>{nombre}</b><br>%{{theta}}: %{{r:.2f}}<extra></extra>",
            )
        )

    fig = _layout(fig, "Anatomía de un hit", "Perfil acústico promedio · escala 0 a 1", alto=520)
    fig.update_layout(
        polar=dict(
            domain=dict(x=[0.12, 0.88], y=[0.02, 0.86]),
            bgcolor=SUPERFICIE,
            radialaxis=dict(visible=True, range=[0, 1], gridcolor=REJILLA,
                            tickfont=dict(size=10), angle=90, tickangle=90),
            angularaxis=dict(gridcolor=REJILLA, tickfont=dict(size=12, color=TINTA_SUAVE)),
        ),
        showlegend=True,
        legend=dict(orientation="h", yanchor="top", y=0.99, xanchor="center", x=0.5),
        margin=dict(l=60, r=60, t=100, b=30),
    )
    return fig


def grafico_hits_por_genero(df: pd.DataFrame, top: int = 12) -> go.Figure:
    """Barras horizontales: % de hits por genero. Una sola serie, un solo color."""
    resumen = (
        df.groupby("playlist_genre")
        .agg(n=("is_hit", "size"), tasa=("is_hit", "mean"))
        .reset_index()
    )
    resumen = resumen[resumen["n"] >= 25].sort_values("tasa", ascending=True).tail(top)

    if resumen.empty:
        return _vacio("¿Qué géneros producen más hits?",
                     "Ningún género del filtro tiene 25 canciones o más.", 380)

    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            x=resumen["tasa"], y=resumen["playlist_genre"].str.capitalize(),
            orientation="h", marker=dict(color=AZUL, line=dict(width=0)),
            text=[f"{v:.0%}" for v in resumen["tasa"]],
            textposition="outside", textfont=dict(color=TINTA_SUAVE, size=12),
            hovertemplate="<b>%{y}</b><br>%{x:.1%} de sus canciones son hit<br>%{customdata} canciones<extra></extra>",
            customdata=resumen["n"],
        )
    )
    fig.update_xaxes(tickformat=".0%", range=[0, min(1, resumen["tasa"].max() * 1.25)], showgrid=True, gridcolor=REJILLA)
    fig.update_yaxes(showgrid=False)
    fig.update_layout(bargap=0.35)
    return _layout(
        fig, "¿Qué géneros producen más hits?",
        "Porcentaje de canciones con popularidad ≥ 70 · solo géneros con 25+ canciones",
        alto=max(420, 34 * len(resumen) + 130),
    )


# ---------------------------------------------------------------------------
# MODULO 4 — FICHA TECNICA
# ---------------------------------------------------------------------------
def grafico_importancias(importancias: dict[str, float]) -> go.Figure:
    """Barras: cuanto pesa cada atributo en la decision del modelo."""
    serie = pd.Series(importancias).sort_values(ascending=True)
    fig = go.Figure(
        go.Bar(
            x=serie.values, y=[NOMBRES.get(i, i) for i in serie.index],
            orientation="h", marker=dict(color=AZUL, line=dict(width=0)),
            text=[f"{v:.1%}" for v in serie.values],
            textposition="outside", textfont=dict(color=TINTA_SUAVE, size=12),
            hovertemplate="<b>%{y}</b><br>Peso: %{x:.1%}<extra></extra>",
        )
    )
    fig.update_xaxes(tickformat=".0%", range=[0, serie.max() * 1.25], gridcolor=REJILLA)
    fig.update_yaxes(showgrid=False)
    fig.update_layout(bargap=0.35)
    return _layout(
        fig, "¿En qué se fija el modelo?",
        "Peso relativo de cada atributo al decidir si una canción es hit",
        alto=max(380, 32 * len(serie) + 130),
    )


def grafico_probabilidad(probabilidad: float, umbral: float) -> go.Figure:
    """Medidor del simulador. Una sola cifra protagonista, sin decoracion."""
    es_hit = probabilidad >= umbral
    color = NARANJA if es_hit else AZUL
    fig = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=probabilidad * 100,
            number=dict(suffix="%", font=dict(size=46, color=color)),
            gauge=dict(
                axis=dict(range=[0, 100], tickwidth=1, tickcolor=REJILLA, tickfont=dict(size=11)),
                bar=dict(color=color, thickness=0.65),
                bgcolor=GRIS_NEUTRO, borderwidth=0,
                threshold=dict(line=dict(color=TINTA, width=3), thickness=0.85, value=umbral * 100),
            ),
        )
    )
    fig.update_layout(
        height=270, margin=dict(l=55, r=55, t=30, b=10),
        paper_bgcolor=SUPERFICIE,
        font=dict(family="system-ui, sans-serif", color=TINTA_SUAVE),
    )
    return fig
