from pathlib import Path
import joblib
import pandas as pd
import streamlit as st

# Importamos la función limpia desde el módulo auxiliar
from ai_service import generate_ai_comment


st.set_page_config(
    page_title="Hit Predictor",
    page_icon="🎵",
    layout="wide",
)

PROJECT_DIR = Path(__file__).resolve().parent
MODEL_PATH = PROJECT_DIR / "models" / "model.pkl"
FEATURES_PATH = PROJECT_DIR / "models" / "features.pkl"

@st.cache_resource
def load_model_artifacts():
    model = joblib.load(MODEL_PATH)
    if hasattr(model, "n_jobs"):
        model.n_jobs = 1
    features = joblib.load(FEATURES_PATH)
    return model, features

st.sidebar.title("Grupo 5")
st.sidebar.markdown("---")
st.sidebar.info("Proyecto Samsung Innovation Campus")

st.title("Hit Predictor & Trendy Dashboard")
st.markdown("Descubre las características acústicas que definen un Hit y prueba tus propias canciones.")

tab1, tab2, tab3 = st.tabs(
    ["Evolución Histórica", "Anatomía de un Hit", "Hit Predictor"]
)

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
    st.caption(
        "El modelo compara los valores ingresados con patrones aprendidos de "
        "canciones del dataset. Es una estimación, no una garantía de éxito comercial."
    )

    try:
        model, feature_names = load_model_artifacts()
    except FileNotFoundError:
        st.error(
            "No se encontraron los archivos del modelo en la carpeta `models/`. "
            "Ejecuta el notebook 02 para generarlos."
        )
    except Exception as error:
        st.error(f"No fue posible cargar el modelo: {error}")
    else:
        col_input, col_output = st.columns([1, 1])

        with col_input:
            st.subheader("Parámetros acústicos")
            with st.form("prediction_form"):
                tempo = st.slider("Ritmo / Tempo (BPM)", 40, 240, 120)
                danceability = st.slider("Bailabilidad (Danceability)", 0.0, 1.0, 0.70)
                energy = st.slider("Energía (Energy)", 0.0, 1.0, 0.80)
                valence = st.slider("Positividad / Mood (Valence)", 0.0, 1.0, 0.50)
                loudness = st.slider("Volumen promedio (Loudness dB)", -60.0, 0.0, -8.0)
                speechiness = st.slider("Contenido hablado (Speechiness)", 0.0, 1.0, 0.10)
                acousticness = st.slider("Acústica (Acousticness)", 0.0, 1.0, 0.20)
                evaluate = st.form_submit_button("Evaluar potencial de hit", type="primary")

        with col_output:
            st.subheader("Veredicto del algoritmo")
            if not evaluate:
                st.info("Configura los parámetros y presiona “Evaluar potencial de hit”.")
            else:
                input_values = {
                    "danceability": danceability,
                    "energy": energy,
                    "valence": valence,
                    "tempo": tempo,
                    "loudness": loudness,
                    "speechiness": speechiness,
                    "acousticness": acousticness,
                }

                missing_features = set(feature_names) - set(input_values)
                if missing_features:
                    st.error(
                        "La interfaz no incluye estas variables requeridas por el modelo: "
                        f"{', '.join(sorted(missing_features))}."
                    )
                else:
                    song_features = pd.DataFrame([input_values])[feature_names]
                    prediction = model.predict(song_features)[0]

                    probability = None
                    if hasattr(model, "predict_proba") and 1 in model.classes_:
                        hit_index = list(model.classes_).index(1)
                        probability = model.predict_proba(song_features)[0][hit_index] * 100

                    if prediction == 1:
                        st.success("¡POTENCIAL HIT VIRAL!")
                    else:
                        st.warning("CANCIÓN DE NICHO / ÉXITO MODERADO")

                    if probability is not None:
                        st.metric("Probabilidad estimada de ser hit", f"{probability:.1f}%")

                    st.divider()
                    st.subheader("Comentario de IA")
                    # Spinner mientras Hugging Face procesa la respuesta
                    with st.spinner("Generando análisis con IA..."):
                        try:
                            ai_comment = generate_ai_comment(input_values, prediction, probability)
                        except Exception:
                            st.error("No fue posible conectar con el servicio de IA.")
                        else:
                            if ai_comment:
                                st.write(ai_comment)
                            else:
                                st.info("Configura `HF_TOKEN` en `.streamlit/secrets.toml` para activar la IA.")

                    with st.expander("Ver variables evaluadas"):
                        st.dataframe(song_features, hide_index=True, use_container_width=True)

                    
