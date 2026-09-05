# Project Guide: `pet-client-responses`

Interactive response hub and communication advisor for Rover pet care professionals to process incoming client messages, diagnose scenarios with an impact traffic light, and generate 5-star customer service responses.

---

## 1. Architecture and System Overview

The workflow processes incoming Rover notifications and inquiries, providing an interactive dashboard:

```text
[Rover Email / Notification]
            │
            ▼
   [Gmail API / MCP Server]
            │
            ▼
[Diagnostic Engine (pet-client-responses)]
            │
    ┌───────┴───────┐
    ▼               ▼
[Impact Traffic] [Response Generator]
[Light Strategy] [Concise / Warm Options]
    │               │
    └───────┬───────┘
            ▼
  [Interactive UI / Streamlit]
```

---

## 2. Directory Structure

```text
pet-client-responses/
├── config/
│   ├── rules.json          # 5-star guidelines and parameters
│   └── mcp_settings.json   # MCP configuration for Gmail / Rover
├── src/
│   ├── mail_listener.py    # Rover email ingestion and parser
│   ├── analyzer.py         # Diagnostic logic, traffic light, and clarification questions
│   └── app.py              # Interactive Streamlit web application
├── Dockerfile              # Container definition with uv
├── docker-compose.yml      # Multi-container orchestration
├── .dockerignore           # Excluded files from Docker build
├── pyproject.toml          # Project metadata and dependencies
├── uv.lock                 # Deterministic dependency lockfile
├── requirements.txt        # Pip fallback dependencies
├── GMAIL_MCP_SETUP.md      # Step-by-step Gmail & MCP credentials guide
└── README.md               # Main project documentation
```

---

## 3. Configuration & Guidelines (`config/rules.json`)

Defines identity, tone, and communication standards:
- 🔴 **Avoid:** Sounding defensive, offering veterinary diagnoses, criticizing pet behaviors, or promising unverified schedules.
- 🟡 **Monitor:** Subtle mood changes, appetite variations, and sensitivity, documenting with photos.
- 🟢 **Priorizar:** Prompt notifications with warmth, high-quality media updates, and heartfelt appreciation.