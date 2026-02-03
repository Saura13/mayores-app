import streamlit as st
import google.generativeai as genai

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(
    page_title="Asistente Vital +65",
    page_icon="🌿",
    layout="centered"
)

# --- TÍTULO Y PRESENTACIÓN ---
st.title("🌿 Asistente de Bienestar Activo")
st.markdown("""
*Tu guía personal para mantenerte activo y saludable a cualquier edad.*
""")

# --- CONFIGURACIÓN DE LA IA (GEMINI) ---
try:
    # Capturamos la clave secreta de la configuración de Streamlit
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
except Exception as e:
    st.error("⚠️ No se encontró la API Key. Asegúrate de haberla puesto en 'Secrets'.")
    st.stop()

# --- INSTRUCCIONES DEL SISTEMA (Tu "Personalidad") ---
system_instruction = """
Rol: Eres un Entrenador Virtual Empático y Dinámico para adultos mayores.
Tono: Motivador, claro y respetuoso. NUNCA uses jerga médica compleja sin explicarla.

BASE DE CONOCIMIENTO (RESUMEN CIENTÍFICO):
1. EL MANTRA: Cualquier movimiento es mejor que estar sentado. Objetivo ideal: 150 min/semana moderados.
2. INTENSIDAD:
   - 🟢 Ligera: Puedes cantar.
   - 🟡 Moderada: Puedes hablar pero no cantar.
   - 🔴 Vigorosa: Pocas palabras antes de tomar aire.
3. LOS 4 PILARES: 
   - Aeróbico (Caminar, nadar).
   - Fuerza (Mínimo 2 días/semana, pesas o bandas).
   - Equilibrio (Tai Chi, caminar en línea).
   - Flexibilidad (Estiramientos).
4. SEGURIDAD:
   - Diabetes: Comer algo antes, vigilar pies.
   - Artrosis: Ejercicio acuático o bajo impacto.
   - Fragilidad/Riesgo de caídas: Empezar con fuerza y equilibrio antes que aeróbico.

FORMATO DE RESPUESTA:
- Usa emojis para hacerlo visual.
- Usa listas con viñetas cortas.
- Usa negritas para las ideas clave.
- Termina siempre con una pregunta motivadora sencilla.
"""

# --- INICIAR EL MODELO ---
# Usamos el modelo que confirmamos que tienes disponible
model = genai.GenerativeModel(
    model_name="models/gemini-2.5-flash", 
    system_instruction=system_instruction
)

# --- HISTORIAL DEL CHAT ---
if "messages" not in st.session_state:
    st.session_state.messages = []
    # Mensaje de bienvenida
    st.session_state.messages.append({
        "role": "model",
        "content": "¡Hola! Soy tu asistente de ejercicio. ¿Cómo te sientes hoy para moverte un poco? 🚶‍♂️💪"
    })

# Mostrar mensajes anteriores
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- INTERACCIÓN CON EL USUARIO ---
if prompt := st.chat_input("Escribe aquí (ej: ¿Qué ejercicios puedo hacer sentado?)"):
    
    # 1. Mostrar lo que el usuario escribió
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # 2. Generar respuesta de la IA
    with st.chat_message("model"):
        try:
            # Preparamos el historial para enviarlo
            # Nota: Gemini espera el historial en un formato específico
            history_gemini = [
                {"role": m["role"], "parts": [m["content"]]} 
                for m in st.session_state.messages[:-1] 
            ]
            
            chat = model.start_chat(history=history_gemini)
            response = chat.send_message(prompt)
            
            st.markdown(response.text)
            
            # 3. Guardar respuesta
            st.session_state.messages.append({"role": "model", "content": response.text})
            
        except Exception as e:
            st.error(f"Ocurrió un error al conectar: {e}")
