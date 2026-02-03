import streamlit as st
import google.generativeai as genai

# --- 1. CONFIGURACIÓN VISUAL DE ALTO IMPACTO ---
st.set_page_config(
    page_title="Vitalidad +65",
    page_icon="🌿",
    layout="wide"  # Usamos el ancho completo para parecer una app de escritorio
)

# --- 2. CONFIGURACIÓN DE LA IA ---
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
except Exception as e:
    st.error("⚠️ Error: No se encontró la API Key en los 'Secrets'.")
    st.stop()

# --- 3. CEREBRO ENTRENADO (Prompt del Sistema) ---
system_instruction = """
Rol: Eres un Entrenador Fisiológico Especializado en Geriatría.
Tono: Profesional pero cálido, motivador y extremadamente claro.

BASE DE CONOCIMIENTO (ESTRICTA):
1. REGLA DE ORO: "Cualquier movimiento cuenta". El sedentarismo es el enemigo.
2. LOS 4 PILARES DEL EJERCICIO (Recomienda combinarlos):
   - Aeróbico (Caminar, baile).
   - Fuerza/Resistencia (Vital para sarcopenia, min 2 días/sem).
   - Equilibrio (Prevención de caídas).
   - Flexibilidad (Rango de movimiento).
3. INTENSIDAD (Test del Habla):
   - Moderada (3-5.9 METs): Puedes hablar pero no cantar.
   - Vigorosa (>=6 METs): Solo dices unas palabras.
4. SEGURIDAD:
   - Ante dolor agudo: PARAR.
   - Diabetes: Snack a mano.
   - Hipertensión: Evitar contener la respiración (Valsalva).
   - Fragilidad: Priorizar fuerza y equilibrio antes que aeróbico intenso.

FORMATO: Usa emojis, negritas para conceptos clave y listas. Sé breve.
"""

model = genai.GenerativeModel(
    model_name="models/gemini-2.5-flash", 
    system_instruction=system_instruction
)

# --- 4. BARRA LATERAL (SIDEBAR) - EL "DASHBOARD" ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2966/2966334.png", width=100)
    st.title("📚 Guía Rápida")
    
    st.info("**Objetivo Semanal:**\n150 min. actividad moderada + 2 días de fuerza.")
    
    st.markdown("### 🚦 Semáforo de Esfuerzo")
    st.success("🟢 **Ligero:** Puedes Cantar")
    st.warning("🟡 **Moderado:** Puedes Hablar")
    st.error("🔴 **Vigoroso:** Falta el aire")
    
    st.divider()
    st.caption("⚠️ Nota: Consulta a tu médico antes de iniciar programas intensos. Basado en guías clínicas de AAFP.")
    
    # Botón para reiniciar
    if st.button("🗑️ Borrar Conversación", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# --- 5. ZONA PRINCIPAL ---
st.header("🌿 Vitalidad +65: Tu Asistente Activo")
st.markdown("Bienvenido. *El movimiento es vida.* ¿En qué nos enfocamos hoy?")

# --- 6. BOTONES DE ACCIÓN RÁPIDA (Novedad) ---
# Creamos 3 columnas para botones que evitan escribir
col1, col2, col3 = st.columns(3)

prompt_seleccionado = None

with col1:
    if st.button("💪 Crear Rutina de Fuerza", use_container_width=True):
        prompt_seleccionado = "Genérame una rutina sencilla de fuerza para hacer en casa con objetos cotidianos (botellas, sillas)."
with col2:
    if st.button("🦿 Dolor de Rodillas", use_container_width=True):
        prompt_seleccionado = "Tengo artrosis leve en las rodillas. ¿Qué ejercicios son seguros y cuáles debo evitar?"
with col3:
    if st.button("⚖️ Mejorar Equilibrio", use_container_width=True):
        prompt_seleccionado = "Tengo miedo a caerme. Dame 3 ejercicios de equilibrio muy seguros para principiantes."

# --- 7. LÓGICA DEL CHAT ---
if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.messages.append({
        "role": "model",
        "content": "Hola. Estoy aquí para ayudarte a moverte de forma segura. ¿Por dónde empezamos hoy? 🚶‍♂️"
    })

# Mostrar historial
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Capturar entrada (ya sea por botón o por escritura manual)
if prompt := (st.chat_input("Escribe tu duda aquí...") or prompt_seleccionado):
    
    # Mostrar lo que el usuario "dijo"
    if not prompt_seleccionado: # Si fue botón, ya se entiende la acción, si es texto lo pintamos
        with st.chat_message("user"):
            st.markdown(prompt)
    else:
        with st.chat_message("user"):
            st.markdown(f"**Opción Rápida:** {prompt}")
            
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Respuesta de la IA
    with st.chat_message("model"):
        with st.spinner("Consultando guía clínica..."):
            history_gemini = [{"role": m["role"], "parts": [m["content"]]} for m in st.session_state.messages[:-1]]
            chat = model.start_chat(history=history_gemini)
            response = chat.send_message(prompt)
            st.markdown(response.text)
            
    st.session_state.messages.append({"role": "model", "content": response.text})
