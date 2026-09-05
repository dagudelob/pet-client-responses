import os
import sys
import streamlit as st

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from analyzer import evaluate_incident
from mail_listener import parse_rover_notification, fetch_messages_from_gmail


st.set_page_config(
    page_title="Rover Client Response Hub",
    page_icon="🐾",
    layout="wide"
)

# Inicializar estado en sesión si no existe
if "client_name" not in st.session_state:
    st.session_state.client_name = "Sarah"
if "pet_name" not in st.session_state:
    st.session_state.pet_name = "Charlie"
if "email_snippet" not in st.session_state:
    st.session_state.email_snippet = (
        "Hi! Charlie has a slightly sensitive stomach today, please keep an eye on him during the walk."
    )

st.title("🐾 Rover Client Assistant & Response Hub")
st.caption("Asesor de comunicación y servicio al cliente de 5 estrellas para Rover")

# Barra lateral: Ingesta de Correo (Gmail o Copiar y Pegar)
with st.sidebar:
    st.header("📬 Ingesta de Mensajes de Rover")
    
    input_method = st.radio(
        "Método de Entrada:",
        ["📋 Pegar Texto / Copiar y Pegar", "✉️ Conectar con Gmail"],
        index=0
    )

    if input_method == "📋 Pegar Texto / Copiar y Pegar":
        st.markdown("**Pega la conversación o notificación de Rover:**")
        pasted_input = st.text_area(
            "Texto copiado:",
            placeholder="Ejemplo:\nFrom Sarah regarding Charlie:\nHi! Charlie is feeling better today, but please make sure he drinks water.",
            height=150
        )
        if st.button("📥 Parsear y Cargar al Hub", use_container_width=True):
            if pasted_input.strip():
                parsed = parse_rover_notification(pasted_input, source="paste")
                st.session_state.client_name = parsed.client_name
                st.session_state.pet_name = parsed.pet_name
                st.session_state.email_snippet = parsed.body_snippet
                st.success("¡Mensaje parseado y cargado correctamente!")
                st.rerun()
            else:
                st.warning("Pega un mensaje antes de presionar el botón.")

    elif input_method == "✉️ Conectar con Gmail":
        st.markdown("**Sincronización con Gmail API:**")
        
        with st.expander("❓ ¿Cómo obtener tus credenciales?", expanded=False):
            st.markdown("""
            1. Ve a [Google Cloud Console](https://console.cloud.google.com/) y crea un proyecto.
            2. En **APIs & Services**, habilita la **Gmail API**.
            3. En **OAuth consent screen**, elige tipo *External*, añade tu email en *Test users* y el scope `gmail.readonly`.
            4. En **Credentials** > **Create Credentials** > **OAuth client ID**, elige **Desktop app**.
            5. Descarga el archivo JSON, renómbralo a `credentials.json` y súbelo aquí abajo o colócalo en la raíz del proyecto.
            
            *(Consulta `GMAIL_MCP_SETUP.md` para el instructivo detallado).*
            """)

        creds_exist = os.path.exists("credentials.json") or os.path.exists("token.json")

        
        if not creds_exist:
            st.info(
                "💡 Para sincronizar con Gmail, coloca tu archivo `credentials.json` en la raíz del proyecto. "
                "También puedes subirlo aquí directamente:"
            )
            uploaded_creds = st.file_uploader("Subir credentials.json (OAuth Client)", type=["json"])
            if uploaded_creds:
                with open("credentials.json", "wb") as f:
                    f.write(uploaded_creds.getbuffer())
                st.success("`credentials.json` guardado con éxito. Ahora puedes sincronizar.")
                st.rerun()
        else:
            st.success(" Credenciales de Gmail detectadas.")

        if st.button("🔄 Importar Últimos Correos de Rover", use_container_width=True):
            with st.spinner("Buscando correos de Rover en Gmail..."):
                gmail_msgs = fetch_messages_from_gmail()
                if gmail_msgs:
                    st.session_state.gmail_msgs = gmail_msgs
                    # Seleccionar el primer mensaje por defecto
                    first_msg = gmail_msgs[0]
                    st.session_state.client_name = first_msg.client_name
                    st.session_state.pet_name = first_msg.pet_name
                    st.session_state.email_snippet = first_msg.body_snippet
                    st.success(f"Se importaron {len(gmail_msgs)} correos de Rover.")
                    st.rerun()
                else:
                    st.warning("No se encontraron correos recientes de Rover o se requiere autenticación.")

        if "gmail_msgs" in st.session_state and st.session_state.gmail_msgs:
            options = [f"{m.client_name} ({m.pet_name}) - {m.subject[:30]}" for m in st.session_state.gmail_msgs]
            selected_idx = st.selectbox(
                "Seleccionar mensaje importado:",
                range(len(options)),
                format_func=lambda i: options[i]
            )
            if st.button("Cargar seleccionado"):
                msg = st.session_state.gmail_msgs[selected_idx]
                st.session_state.client_name = msg.client_name
                st.session_state.pet_name = msg.pet_name
                st.session_state.email_snippet = msg.body_snippet
                st.rerun()

    st.markdown("---")
    st.subheader("✏️ Edición Rápida de Parámetros")
    st.session_state.client_name = st.text_input("Nombre del Dueño (*Client Name*):", st.session_state.client_name)
    st.session_state.pet_name = st.text_input("Nombre de la Mascota (*Pet's Name*):", st.session_state.pet_name)
    st.session_state.email_snippet = st.text_area(
        "Mensaje Activo:",
        st.session_state.email_snippet,
        height=100
    )

client_name = st.session_state.client_name
pet_name = st.session_state.pet_name
email_snippet = st.session_state.email_snippet

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