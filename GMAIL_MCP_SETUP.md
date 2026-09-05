# 📖 Guía: Obtención de Credenciales de Gmail e Integración con MCP

Esta guía detalla paso a paso cómo habilitar el acceso a Gmail para el proyecto **`pet-client-responses`**, ya sea mediante **Google Cloud Console (OAuth2 `credentials.json`)** para la app en Streamlit o mediante un **Servidor MCP de Gmail**.

---

## Opción 1: Obtener `credentials.json` (Google Cloud Console OAuth2)

Esta opción permite que la app en Streamlit descargue e importe directamente los correos de Rover de tu bandeja de entrada.

### Paso 1: Crear o Seleccionar un Proyecto en Google Cloud
1. Entra a [Google Cloud Console](https://console.cloud.google.com/).
2. Inicia sesión con la cuenta de Google donde recibes las notificaciones de Rover.
3. En la barra superior, haz clic en el selector de proyectos y selecciona **"New Project"** (o usa uno existente).
4. Nómbralo (por ejemplo: `rover-client-hub`) y haz clic en **Create**.

### Paso 2: Habilitar la API de Gmail
1. En el menú de navegación (icono de hamburguesa ☰), ve a **APIs & Services** > **Library** (o busca *"Gmail API"* en la barra de búsqueda).
2. Selecciona **Gmail API** y haz clic en el botón azul **Enable**.

### Paso 3: Configurar la Pantalla de Consentimiento (OAuth Consent Screen)
1. Ve a **APIs & Services** > **OAuth consent screen**.
2. En *User Type*, selecciona **External** (o *Internal* si usas Google Workspace) y haz clic en **Create**.
3. Completa los campos básicos obligatorios:
   - **App name:** `Rover Client Hub`
   - **User support email:** Tu correo electrónico.
   - **Developer contact information:** Tu correo electrónico.
4. Haz clic en **Save and Continue**.
5. En el paso de **Scopes**, haz clic en **Add or Remove Scopes**:
   - Filtra y selecciona: `https://www.googleapis.com/auth/gmail.readonly`.
   - Haz clic en **Update** y luego en **Save and Continue**.
6. En **Test users** (Usuarios de prueba):
   - Haz clic en **+ Add Users**.
   - Agrega tu dirección de Gmail (la misma con la que te autenticarás).
   - Haz clic en **Save and Continue**.

### Paso 4: Crear las Credenciales OAuth2
1. Ve a **APIs & Services** > **Credentials**.
2. Haz clic en **+ Create Credentials** en la parte superior y selecciona **OAuth client ID**.
3. En **Application type**, selecciona **Desktop app** (Aplicación de escritorio).
4. Nómbralo `Rover Desktop Client` y haz clic en **Create**.
5. Aparecerá una ventana confirmando la creación. Haz clic en **Download JSON**.
6. Renombra el archivo descargado exactamente a:
   ```text
   credentials.json
   ```
7. Coloca `credentials.json` en la raíz de este proyecto (`pet-client-responses/credentials.json`) o súbelo directamente desde la barra lateral de Streamlit.

> [!NOTE]
> La primera vez que presiones "Importar Últimos Correos", se abrirá una pestaña en el navegador solicitando que inicies sesión y otorgues permisos de lectura. Tras aceptar, se creará automáticamente un archivo local `token.json` para no tener que iniciar sesión nuevamente.

---

## Opción 2: Integración mediante Servidor MCP de Gmail

Si utilizas un cliente con soporte para el protocolo MCP (Model Context Protocol) como Claude Desktop, Antigravity o Cursor:

### 1. Servidor MCP de Gmail Oficial / Comunitario (`@modelcontextprotocol/server-gmail` o Python MCP)

Puedes integrar el servidor de Gmail en tu configuración de cliente agregando el bloque correspondiente:

#### Para Claude Desktop o Antigravity (`claude_desktop_config.json` o `.gemini/antigravity-ide/mcp_config.json`):
```json
{
  "mcpServers": {
    "gmail": {
      "command": "npx",
      "args": [
        "-y",
        "@gongar/gmail-mcp-server"
      ],
      "env": {
        "GMAIL_CREDENTIALS_PATH": "/ruta/absoluta/a/tu/credentials.json"
      }
    }
  }
}
```

O si utilizas el listener local preparado en el proyecto:
```json
{
  "mcpServers": {
    "rover-mail-listener": {
      "command": "uv",
      "args": [
        "run",
        "python",
        "-m",
        "src.mail_listener"
      ],
      "env": {
        "ROVER_EMAIL_FILTER": "from:rover.com",
        "FETCH_INTERVAL_MINUTES": "5"
      }
    }
  }
}
```

---

## 🔒 Seguridad y Privacidad
* El archivo [`.gitignore`](file:///home/dagudelo/code/work/pet-client-responses/.gitignore) del proyecto ya tiene configurado por defecto ignorar:
  - `credentials.json`
  - `token.json`
  - `*.env*`
* Tus credenciales de acceso y tokens **nunca** serán subidos al repositorio público de GitHub.
