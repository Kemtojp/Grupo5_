# ai_service.py
import os
from pathlib import Path
from huggingface_hub import InferenceClient
import streamlit as st

HF_MODEL = "meta-llama/Llama-3.1-8B-Instruct"

def get_hf_token():
    """Lee el token desde Streamlit secrets o variable de entorno."""
    try:
        return st.secrets["HF_TOKEN"]
    except (KeyError, FileNotFoundError):
        return os.getenv("HF_TOKEN")

@st.cache_resource
def get_inference_client(token):
    return InferenceClient(model=HF_MODEL, token=token, timeout=30)

def generate_ai_comment(input_values, prediction, probability):
    """Genera un análisis sintético del veredicto del modelo."""
    token = get_hf_token()
    if not token:
        return None

    verdict = "HIT" if prediction == 1 else "NO HIT"
    probability_text = f"{probability:.1f}%" if probability is not None else "N/A"
    values = ", ".join(f"{name}={value}" for name, value in input_values.items())

    system_instruction = (
        "Eres un analista musical ultra conciso. Das diagnósticos directos y al grano sin introducciones."
    )

    prompt = f"""
Datos de la canción:
- Resultado: {verdict} ({probability_text})
- Métricas: {values}

Escribe UN SOLO PÁRRAFO de máximo 40 palabras.
- Ve DIRECTO al análisis sin saludar ni repetir la probabilidad.
- Menciona qué 2 métricas favorecen o perjudican este resultado.
- Termina aclarando que es una estimación algorítmica.
- Prohibido usar títulos, viñetas o negritas.
"""

    client = get_inference_client(token)
    response = client.chat_completion(
        messages=[
            {"role": "system", "content": system_instruction},
            {"role": "user", "content": prompt},
        ],
        max_tokens=90,
        temperature=0.3,
    )
    return response.choices[0].message.content