# Guía de Proyecto: `pet-client-responses`

Panel de control interactivo para procesar notificaciones por correo de Rover, diagnosticar escenarios de servicio al cliente y generar respuestas bilingües de 5 estrellas para dueños de mascotas.

---

## 1. Arquitectura y Visión General del Sistema

El flujo de trabajo automatiza la ingesta de correos de Rover y ofrece un panel (*dashboard*) interactivo para revisar interacciones y redactar respuestas con traducción en vivo:


\[Notificación de Rover en Gmail\] │ ▼ \[Servidor MCP de Correo / API\] │ ▼ \[Motor de Diagnóstico (pet-client-responses)\] │ ┌────────┴────────┐ ▼ ▼ \[Semáforo Estratégico\] \[Traductor & Generador Bilingüe\] │ │ └────────┬────────┘ ▼ \[Panel Interactivo / UI\]

\--- ## 2. Estructura de Directorios Crea el espacio de trabajo con la siguiente estructura modular: \`\`\`text pet-client-responses/ ├── config/ │ ├── rules.json # Reglas de la Gema y parámetros del sistema │ └── mcp\_settings.json # Configuración del servidor MCP de Gmail ├── src/ │ ├── mail\_listener.py # Ingesta y parseo de correos de Rover │ ├── analyzer.py # Diagnóstico, semáforo y lógica de las 3 preguntas │ ├── generator.py # Generación de respuestas (Opción A y Opción B) │ └── app.py # Interfaz gráfica interactiva (Streamlit / Panel) ├── templates/ │ └── daily\_updates.md # Plantillas para Rover Cards y reportes diarios ├── .env.example # Plantilla de variables de entorno ├── requirements.txt # Dependencias de Python └── README.md # Documentación de uso

## 3\. Configuración de Reglas y Directrices (`config/rules.json`)

Este archivo almacena la identidad y el protocolo de comunicación derivado de la Gema:

## 3\. Configuración de Reglas y Directrices (`config/rules.json`)

Este archivo almacena la identidad y el protocolo de comunicación derivado de la Gema:

## 4\. Instalación y Dependencias

Crea y activa un entorno virtual en Python (`venv`):

Bash

    python -m venv .venv
    source .venv/bin/activate  # En Linux/macOS/WSL2
    # .venv\Scripts\activate   # En Windows PowerShell

    Crea el archivo `requirements.txt`:

streamlit>=1.35.0
pydantic>=2.7.0
google-api-python-client>=2.120.0
google-auth-oauthlib>=1.2.0
python-dotenv>=1.0.1
rich>=13.7.1

## 5\. Implementación del Núcleo

### 5.1. Analizador y Generador (`src/analyzer.py`)

Contiene la lógica de evaluación bajo el protocolo de la Gema:

### 5.2. Panel Interactivo (`src/app.py`)

Interfaz visual en Streamlit para gestionar correos entrantes, visualizar el diagnóstico del semáforo y traducir mensajes en tiempo real:

## 6\. Ejecución del Panel

Para iniciar la interfaz interactiva, ejecuta desde la raíz del proyecto:

Bash 
streamlit run src/app.py
El navegador abrirá automáticamente la URL local (usualmente `http://localhost:8501`).

## 7\. Protocolo de Calidad de Servicio al Cliente

*   🔴 **Evitar:** Responder a la defensiva, diagnosticar cuadros médicos, emitir juicios sobre el entrenamiento de la mascota o comprometerse a horarios sin confirmación previa.
    
*   🟡 **Monitorear:** Cambios menores de humor, diferencias de apetito o rechazo a premios habituales. Registrar siempre con fotos de soporte.
    
*   🟢 **Priorizar:** Notificar a tiempo con tono afable, adjuntar material visual de calidad y agradecer la confianza del dueño al cierre de cada interacción.