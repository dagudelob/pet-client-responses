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

# Initialize session state
if "client_name" not in st.session_state:
    st.session_state.client_name = "Sarah"
if "pet_name" not in st.session_state:
    st.session_state.pet_name = "Charlie"
if "email_snippet" not in st.session_state:
    st.session_state.email_snippet = (
        "Hi! Charlie has a slightly sensitive stomach today, please keep an eye on him during the walk."
    )

st.title("🐾 Rover Client Assistant & Response Hub")
st.caption("5-Star customer service communication advisor for Rover pet care professionals")

# Sidebar: Rover message ingestion (Gmail or Copy & Paste)
with st.sidebar:
    st.header("📬 Rover Message Ingestion")
    
    input_method = st.radio(
        "Ingestion Method:",
        ["📋 Paste Message / Chat", "✉️ Connect with Gmail"],
        index=0
    )

    if input_method == "📋 Paste Message / Chat":
        st.markdown("**Paste the Rover message or notification:**")
        pasted_input = st.text_area(
            "Copied text:",
            placeholder="Example:\nFrom Sarah regarding Charlie:\nHi! Charlie is feeling better today, but please make sure he drinks water.",
            height=150
        )
        if st.button("📥 Parse and Load to Hub", use_container_width=True):
            if pasted_input.strip():
                parsed = parse_rover_notification(pasted_input, source="paste")
                st.session_state.client_name = parsed.client_name
                st.session_state.pet_name = parsed.pet_name
                st.session_state.email_snippet = parsed.body_snippet
                st.success("Message parsed and loaded successfully!")
                st.rerun()
            else:
                st.warning("Please paste a message before clicking the button.")

    elif input_method == "✉️ Connect with Gmail":
        st.markdown("**Sync with Gmail API:**")
        
        with st.expander("❓ How to get your credentials?", expanded=False):
            st.markdown("""
            1. Open [Google Cloud Console](https://console.cloud.google.com/) and create a project.
            2. Under **APIs & Services**, enable the **Gmail API**.
            3. Under **OAuth consent screen**, select *External*, add your email under *Test users*, and add the scope `gmail.readonly`.
            4. Under **Credentials** > **Create Credentials** > **OAuth client ID**, choose **Desktop app**.
            5. Download the JSON, rename it to `credentials.json`, and upload it below or place it in the project root.
            
            *(Refer to `GMAIL_MCP_SETUP.md` for full instructions).*
            """)

        creds_exist = os.path.exists("credentials.json") or os.path.exists("token.json")
        
        if not creds_exist:
            st.info(
                "💡 To sync with Gmail, place your `credentials.json` file in the project root or upload it directly here:"
            )
            uploaded_creds = st.file_uploader("Upload credentials.json (OAuth Client)", type=["json"])
            if uploaded_creds:
                with open("credentials.json", "wb") as f:
                    f.write(uploaded_creds.getbuffer())
                st.success("`credentials.json` saved successfully. You can now import messages.")
                st.rerun()
        else:
            st.success(" Gmail credentials detected.")

        if st.button("🔄 Import Latest Rover Emails", use_container_width=True):
            with st.spinner("Fetching Rover emails from Gmail..."):
                gmail_msgs = fetch_messages_from_gmail()
                if gmail_msgs:
                    st.session_state.gmail_msgs = gmail_msgs
                    first_msg = gmail_msgs[0]
                    st.session_state.client_name = first_msg.client_name
                    st.session_state.pet_name = first_msg.pet_name
                    st.session_state.email_snippet = first_msg.body_snippet
                    st.success(f"Imported {len(gmail_msgs)} Rover messages.")
                    st.rerun()
                else:
                    st.warning("No recent Rover messages found or authentication required.")

        if "gmail_msgs" in st.session_state and st.session_state.gmail_msgs:
            options = [f"{m.client_name} ({m.pet_name}) - {m.subject[:30]}" for m in st.session_state.gmail_msgs]
            selected_idx = st.selectbox(
                "Select imported message:",
                range(len(options)),
                format_func=lambda i: options[i]
            )
            if st.button("Load selected"):
                msg = st.session_state.gmail_msgs[selected_idx]
                st.session_state.client_name = msg.client_name
                st.session_state.pet_name = msg.pet_name
                st.session_state.email_snippet = msg.body_snippet
                st.rerun()

    st.markdown("---")
    st.subheader("✏️ Quick Parameter Adjustment")
    st.session_state.client_name = st.text_input("Owner's Name (*Client Name*):", st.session_state.client_name)
    st.session_state.pet_name = st.text_input("Pet's Name:", st.session_state.pet_name)
    st.session_state.email_snippet = st.text_area(
        "Active Message:",
        st.session_state.email_snippet,
        height=100
    )

client_name = st.session_state.client_name
pet_name = st.session_state.pet_name
email_snippet = st.session_state.email_snippet

col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📋 Step 1 & 2: Diagnosis & Strategy")
    data = evaluate_incident(email_snippet)
    
    with st.expander("❓ Clarification Questions (Additional Context)", expanded=True):
        for i, q in enumerate(data["clarification_questions"], 1):
            st.write(f"**{i}.** {q}")
    
    st.markdown("### 🚦 Impact Traffic Light")
    st.markdown(data["traffic_light"]["red"])
    st.markdown(data["traffic_light"]["yellow"])
    st.markdown(data["traffic_light"]["green"])

with col2:
    st.subheader("✍️ Step 3: Ready-to-Send Response Options")
    
    tab1, tab2, tab3 = st.tabs(["Option A (Concise)", "Option B (Detailed)", "Daily Report (Rover Card)"])
    
    with tab1:
        st.markdown("**Variant A (Concise & Direct):**")
        text_a = data["response_variants"]["option_a"].replace("[Owner's Name]", client_name).replace("[Pet's Name]", pet_name)
        st.code(text_a, language="markdown")
        st.button("Copy Option A", key="btn_a")
        
    with tab2:
        st.markdown("**Variant B (Detailed & Warm):**")
        text_b = data["response_variants"]["option_b"].replace("[Owner's Name]", client_name).replace("[Pet's Name]", pet_name)
        st.code(text_b, language="markdown")
        st.button("Copy Option B", key="btn_b")

    with tab3:
        st.markdown("**Rover Card Template:**")
        card_template = (
            f"Hi {client_name}! We had a fantastic session with {pet_name} today! 🐾\n"
            f"- **Duration:** [Walk Duration]\n"
            f"- **Activities:** Great potty routine, lots of sniff-time, and fresh water refilled.\n"
            f"- **Mood:** Upbeat, attentive, and super friendly.\n"
            f"Attached are a few photos from our adventure! Let me know if you need anything else!"
        )
        st.code(card_template, language="markdown")

st.divider()

# Message Polish and Tone Assistant Section
st.subheader("✨ Message Refinement & Quick Polish")
user_draft = st.text_area(
    "Custom draft or quick notes to adapt:",
    "Charlie was slightly shy at the beginning of the walk, but after 5 minutes he started sniffing around the park and looked very happy. Potty routine was completely normal.",
    height=100
)

if st.button("Polish to Rover 5-Star Tone"):
    if user_draft.strip():
        st.info("Adapted to the official Rover tone (*warm, confident, casual yet polished*):")
        
        col_tr1, col_tr2 = st.columns(2)
        with col_tr1:
            st.markdown("**🌟 5-Star Polished Message:**")
            st.markdown(
                f"> *\"Hi {client_name}! Just wanted to share that {pet_name} was a tiny bit shy right at the start of our walk, "
                f"but within just 5 minutes he warmed up completely, had a wonderful time sniffing around the park, and looked so happy and relaxed! "
                f"Potty routine was all normal and smooth. Looking forward to our next visit! 🐾\"*"
            )
        with col_tr2:
            st.markdown("**✨ Key Standards Applied:**")
            st.markdown("- Positive, empathetic tone without causing unnecessary alarm.")
            st.markdown("- Direct confirmation of routine and well-being.")
            st.markdown("- Warm and appreciative closing.")
    else:
        st.warning("Please enter a draft message to polish.")