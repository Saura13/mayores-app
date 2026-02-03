import streamlit as st
import google.generativeai as genai
import os

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
# Aquí es donde ocurre la magia. Capturamos la clave secreta.
# (Más adelante te explico dónde ponerla en la nube)
api_key = st.secrets["GOOGLE_API_KEY"]
genai.configure(api_key=api_key)

# --- INSTRUCCIONES DEL SISTEMA (Basadas en el PDF) ---
# Estas son las reglas que definimos anteriormente
system_instruction = """
Rol: Eres un Entrenador Virtual Empático y Dinámico para adultos mayores.
Tono: Motivador, claro y respetuoso. Sin jerga médica.

CONOCIMIENTO BASE (RESUMEN DEL ESTUDIO CIENTÍFICO):
1. MANTRA: Cualquier movimiento es mejor que estar sentado[cite: 6]. Objetivo: 150 min/semana moderados.
2. INTENSIDAD:
   - Ligera: Puedes cantar.
   - Moderada: Puedes hablar pero no cantar.
   - Vigorosa: Pocas palabras antes de tomar aire.
3. LOS 4 PILARES: Aeróbico, Fuerza (2 días/sem), Equilibrio (Tai Chi), Flexibilidad[cite: 89, 97, 93].
4. SEGURIDAD:
   - Diabetes: Comer algo antes, vigilar pies[cite: 125, 126].
   - Artrosis: Ejercicio acuático o bajo impacto[cite: 111, 112].
   - Fragilidad: Empezar con fuerza y equilibrio antes que aeróbico[cite: 54].

FORMATO DE RESPUESTA:
- Usa emojis.
- Usa listas.
- Termina siempre con una pregunta motivadora.
"""

# Iniciamos el modelo
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash-latest", # Usamos Flash porque es rápido y barato
    system_instruction=system_instruction
)

# --- HISTORIAL DEL CHAT ---
# Esto permite que la IA recuerde lo que habéis hablado
if "messages" not in st.session_state:
    st.session_state.messages = []
    # Mensaje de bienvenida inicial
    st.session_state.messages.append({
        "role": "model",
        "content": "¡Hola! Soy tu asistente de ejercicio. ¿Cómo te sientes hoy para moverte un poco? 🚶‍♂️💪"
    })

# Mostrar mensajes anteriores en la pantalla
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- INTERACCIÓN CON EL USUARIO ---
if prompt := st.chat_input("Escribe aquí (ej: me duelen las rodillas, ¿qué hago?)"):
    # 1. Mostrar lo que el usuario escribió
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # 2. Generar respuesta de la IA
    with st.chat_message("model"):
        # Preparamos la conversación para enviarla a Gemini
        chat = model.start_chat(history=[
            {"role": m["role"], "parts": [m["content"]]} 
            for m in st.session_state.messages[:-1] # Todo menos el último (que acabamos de añadir)
        ])
        
        response = chat.send_message(prompt)
        st.markdown(response.text)
    
    # 3. Guardar respuesta de la IA

    st.session_state.messages.append({"role": "model", "content": response.text})

