import streamlit as st
import pandas as pd
import joblib
import os

st.set_page_config(
    page_title="Hit Predictor",
    page_icon="🎵",
    layout="wide"
)

st.sidebar.title("Grupo 5")
st.sidebar.markdown("---")
st.sidebar.info("Proyecto Samsung Innovation Campus")

st.title("Hit Predictor & Trendy Dashboard")
st.markdown("Descubre las características acústicas que definen un Hit y prueba tus propias canciones.")

tab1, tab2, tab3 = st.tabs([
    "Evolución Histórica", 
    "Anatomía de un Hit", 
    "Hit Predictor (Simulador)"
])

with tab1:
    st.header("La Evolución del Sonido")
    st.write("Aquí se mostrará la evolución de las características acústicas con el paso del tiempo.")
    # El Integrante 3 insertará aquí sus funciones de Plotly

with tab2:
    st.header("Anatomía de un Hit Musical")
    st.write("Comparación de canciones populares frente a canciones comunes.")
    # El Integrante 3 insertará aquí la Matriz de Correlación y el Radar Plot

with tab3:
    st.header("Configura tu canción y evalúa su potencial")
    
    col_input, col_output = st.columns([1, 1])
    
    with col_input:
        st.subheader("Parámetros Acústicos")
        tempo = st.slider("Ritmo / Tempo (BPM)", 60, 200, 120)
        danceability = st.slider("Bailabilidad (Danceability)", 0.0, 1.0, 0.7)
        energy = st.slider("Energía (Energy)", 0.0, 1.0, 0.8)
        valence = st.slider("Positividad / Mood (Valence)", 0.0, 1.0, 0.5)
        acousticness = st.slider("Acústica (Acousticness)", 0.0, 1.0, 0.2)
        loudness = st.slider("Volumen Promedio (Loudness dB)", -60.0, 0.0, -8.0)
        
        btn_evaluar = st.button(" Evaluar Potencial de Hit")

    with col_output:
        st.subheader("Veredicto del Algoritmo")
        if btn_evaluar:
            # Comprobar si el Integrante 2 ya subió el modelo entrenado
            model_path = os.path.join("models", "model.pkl")
            
            if os.path.exists(model_path):
                model = joblib.load(model_path)
                
                features = pd.DataFrame([{
                    'danceability': danceability,
                    'energy': energy,
                    'valence': valence,
                    'tempo': tempo,
                    'loudness': loudness,
                    'acousticness': acousticness
                }])
                
                prediction = model.predict(features)[0]
                proba = model.predict_proba(features)[0][1] * 100 if hasattr(model, "predict_proba") else None
                
                if prediction == 1:
                    st.success("¡POTENCIAL HIT VIRAL!")
                    if proba:
                        st.metric("Probabilidad de Éxito", f"{proba:.1f}%")
                else:
                    st.warning("CANCIÓN DE NICHO / ÉXITO MODERADO")
                    if proba:
                        st.metric("Probabilidad de Éxito", f"{proba:.1f}%")
            else:
                # Simulación temporal mientras el Integrante 2 entrega model.pkl
                st.info("Modo vista previa: El modelo `model.pkl` se cargará cuando el Integrante 2 lo suba.")
                st.metric("Resultado de prueba", "85% de Probabilidad")
                st.success("¡POTENCIAL HIT VIRAL!")