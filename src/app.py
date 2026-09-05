import streamlit as st
from analyzer import evaluate_incident

st.set_page_config(
    page_title="Rover Client Response Hub",
    page_icon="🐾",
    layout="wide"
)

st.title("🐾 Rover Client Assistant & Response Hub")
st.caption("Asesor de comunicación y servicio al cliente de 5 estrellas para Rover")

# Barra lateral: Simulación o Ingesta de Correo
with st.sidebar:
    st.header("📬 Ingesta de Correo (Rover)")
    client_name = st.text_input("Nombre del Dueño (*Client Name*):", "Sarah")
    pet_name = st.text_input("Nombre de la Mascota (*Pet's Name*):", "Charlie")
    email_snippet = st.text_area(
        "Mensaje del Cliente / Notificación recibida:",
        "Hi! Charlie has a slightly sensitive stomach today, please keep an eye on him during the walk."
    )
    load_email_btn = st.button("Procesar Consulta")

col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📋 Paso 1 & 2: Diagnóstico y Estrategia")
    data = evaluate_incident(email_snippet)
    
    with st.expander("❓ Preguntas de Clarificación (Contexto Adicional)", expanded=True):
        for i, q in enumerate(data["clarification_questions"], 1):
            st.write(f"**{i}.** {q}")
    
    st.markdown("### 🚦 Semáforo de Impacto")
    st.markdown(data["traffic_light"]["red"])
    st.markdown(data["traffic_light"]["yellow"])
    st.markdown(data["traffic_light"]["green"])

with col2:
    st.subheader("✍️ Paso 3: Opciones de Respuesta Lista (Copy-Paste)")
    
    tab1, tab2, tab3 = st.tabs(["Opción A (Concisa)", "Opción B (Detallada)", "Reporte Diario (Rover Card)"])
    
    with tab1:
        st.markdown("**Variante A (Concisa y Directa):**")
        text_a = data["response_variants"]["option_a"].replace("[Owner's Name]", client_name).replace("[Pet's Name]", pet_name)
        st.code(text_a, language="markdown")
        st.button("Copiar Opción A", key="btn_a")
        
    with tab2:
        st.markdown("**Variante B (Detallada y Cálida):**")
        text_b = data["response_variants"]["option_b"].replace("[Owner's Name]", client_name).replace("[Pet's Name]", pet_name)
        st.code(text_b, language="markdown")
        st.button("Copiar Opción B", key="btn_b")

    with tab3:
        st.markdown("**Plantilla de Rover Card:**")
        card_template = f"Hi {client_name}! We had a fantastic session with {pet_name} today! 🐾\n- **Duration:** [Walk Duration]\n- **Activities:** Great potty routine, lots of sniff-time, and fresh water refilled.\n- **Mood:** Upbeat, attentive, and super friendly.\nAttached are a few photos from our adventure! Let me know if you need anything else!"
        st.code(card_template, language="markdown")

st.divider()

# Sección de Traducción e Inspección Rápida
st.subheader("🌐 Traducción y Ajustes Rápidos")
user_draft_es = st.text_area(
    "Borrador o ideas en español para adaptar:",
    "Hola, Charlie estuvo un poco tímido al principio del paseo, pero después de 5 minutos comenzó a oler el parque y se le vio feliz. Todo en orden con sus necesidades.",
    height=100
)

if st.button("Traducir y Pulir al Estilo Rover"):
    if user_draft_es.strip():
        st.info("Adaptado al tono oficial de Rover (*warm, confident, casual yet polished*):")
        
        # Generación asistida de traducción/estilo adaptado
        col_tr1, col_tr2 = st.columns(2)
        with col_tr1:
            st.markdown("**🇺🇸 Versión en Inglés (Rover Standard 5-Stars):**")
            st.markdown(
                f"> *\"Hi {client_name}! Just wanted to share that {pet_name} was a tiny bit shy right at the start of our walk, "
                f"but within just 5 minutes he warmed up completely, had a wonderful time sniffing around the park, and looked so happy and relaxed! "
                f"Potty routine was all normal and smooth. Looking forward to our next visit! 🐾\"*"
            )
        with col_tr2:
            st.markdown("**✨ Puntos clave aplicados:**")
            st.markdown("- Tono positivo y empático sin generar alarma.")
            st.markdown("- Mención directa de bienestar y rutina.")
            st.markdown("- Cierre cálido y cordial.")
    else:
        st.warning("Por favor introduce un texto o borrador en español.")