# 🐾 Rover Client Assistant & Response Hub (`pet-client-responses`)

Panel interactivo y motor de respuestas 5 estrellas para cuidadores de Rover. Permite diagnosticar consultas e incidentes mediante un **semáforo estratégico (🔴 / 🟡 / 🟢)**, generar respuestas profesionales bilingües listas para enviar y gestionar la ingesta de correos mediante servidores MCP.

---

## 🚀 Inicio Rápido con `uv`

Este proyecto utiliza [`uv`](https://docs.astral.sh/uv/) para la gestión ultrarrápida de dependencias y entornos.

### 1. Clonar e Instalar
```bash
git clone https://github.com/dagudelob/pet-client-responses.git
cd pet-client-responses

# Sincronizar dependencias automáticamente
uv sync
```

### 2. Ejecutar la Aplicación
```bash
uv run streamlit run src/app.py
```
Abre en tu navegador `http://localhost:8501`.

---

## 📁 Estructura del Proyecto

```text
pet-client-responses/
├── config/
│   ├── rules.json          # Reglas del protocolo y semáforo Rover 5-Star
│   └── mcp_settings.json   # Configuración para servidor MCP de Gmail / Rover
├── src/
│   ├── analyzer.py         # Diagnóstico, semáforo y 3 preguntas clave
│   ├── mail_listener.py    # Conector y parseo de notificaciones de Rover (MCP ready)
│   └── app.py              # Interfaz interactiva de Streamlit
├── pyproject.toml          # Definición del proyecto y dependencias de uv
├── uv.lock                 # Bloqueo determinista de dependencias
├── .gitignore              # Archivos y secretos ignorados
└── README.md
```

---

## 🚦 Protocolo de Semáforo Rover 5 Estrellas
* 🔴 **Evitar:** Diagnósticos médicos, respuestas defensivas, juicios de crianza o compromisos sin confirmación.
* 🟡 **Monitorear:** Cambios de humor leves, apetito o digestión sensible, documentando siempre con fotos.
* 🟢 **Priorizar:** Confirmar a tiempo con calidez, adjuntar fotos de calidad y agradecer la confianza.
