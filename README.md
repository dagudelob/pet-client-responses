# 🐾 Rover Client Assistant & Response Hub (`pet-client-responses`)

Interactive response hub and 5-star communication advisor for Rover pet care professionals. Diagnose client questions and incidents using an **Impact Traffic Light (🔴 / 🟡 / 🟢)**, generate ready-to-send professional responses, and ingest messages via copy-paste or Gmail API / MCP.

---

## 🚀 Quickstart with `uv`

This project uses [`uv`](https://docs.astral.sh/uv/) for high-performance dependency and environment management.

### 1. Clone and Install
```bash
git clone https://github.com/dagudelob/pet-client-responses.git
cd pet-client-responses

# Sync all dependencies
uv sync
```

### 2. Run Locally
```bash
uv run streamlit run src/app.py
```
Open your browser at `http://localhost:8501`.

---

## 🐳 Running with Docker

You can containerize and deploy the entire application using Docker and Docker Compose:

### Using Docker Compose
```bash
docker compose up --build -d
```
Then visit `http://localhost:8501`.

To stop the container:
```bash
docker compose down
```

### Using Docker CLI Directly
```bash
# Build the image
docker build -t pet-client-responses .

# Run the container
docker run -d -p 8501:8501 --name rover-hub pet-client-responses
```

---

## 📁 Project Structure

```text
pet-client-responses/
├── config/
│   ├── rules.json          # 5-star protocol and traffic light guidelines
│   └── mcp_settings.json   # Gmail / Rover MCP server configuration
├── src/
│   ├── analyzer.py         # Incident analysis, traffic light logic & response variants
│   ├── mail_listener.py    # Notification parser & Gmail API connector
│   └── app.py              # Streamlit interactive user interface
├── Dockerfile              # Container image definition using uv
├── docker-compose.yml      # Service definition for simple deployment
├── .dockerignore           # Excluded patterns for Docker context
├── pyproject.toml          # uv project specification and dependencies
├── uv.lock                 # Deterministic dependency lockfile
├── GMAIL_MCP_SETUP.md      # Credentials & MCP configuration manual
└── README.md
```

---

## 🚦 Rover 5-Star Traffic Light Protocol
* 🔴 **Avoid:** Veterinary diagnoses, defensive tone, judging pet behavior, or committing to unverified schedules.
* 🟡 **Monitor:** Subtle mood changes, appetite variations, and sensitivity, documenting with photos.
* 🟢 **Prioritize:** Timely communication with warmth, high-quality visual updates, and expressing genuine appreciation.

---

## ✉️ Ingestion Methods
1. **Copy & Paste (Direct):** Paste any message or notification snippet in the sidebar for instant extraction of the owner name, pet name, and scenario analysis.
2. **Gmail API / MCP:** Ingest messages automatically from Rover. Refer to [GMAIL_MCP_SETUP.md](GMAIL_MCP_SETUP.md) for setup details.
