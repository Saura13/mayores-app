import streamlit as st
import google.generativeai as genai

st.title("🛠️ Diagnóstico de Conexión")

# 1. Intentamos configurar la llave
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
    st.success("✅ Llave API encontrada y configurada.")
except Exception as e:
    st.error(f"❌ Error con la llave: {e}")
    st.stop()

# 2. Preguntamos a Google qué modelos ve
st.write("Consultando modelos disponibles para tu cuenta...")

try:
    # Listamos los modelos que sirven para generar contenido (generateContent)
    models = []
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            models.append(m.name)
            
    if models:
        st.success(f"¡Conexión exitosa! Se han encontrado {len(models)} modelos.")
        st.write("### Copia uno de estos nombres exactos:")
        st.code(models)
    else:
        st.warning("Se conectó, pero no aparecen modelos disponibles. ¿Quizás tu API Key no tiene permisos?")

except Exception as e:
    st.error(f"❌ Error al conectar con Google: {e}")


