# 📖 Guide: Gmail API Credentials & MCP Integration

This guide provides step-by-step instructions for enabling Gmail access for the **`pet-client-responses`** project, either via **Google Cloud Console OAuth2 (`credentials.json`)** for the Streamlit dashboard or via a **Gmail MCP Server**.

---

## Option 1: Obtain `credentials.json` (Google Cloud Console OAuth2)

This option enables the Streamlit application to query and import Rover messages directly from your Gmail inbox.

### Step 1: Create or Select a Google Cloud Project
1. Open [Google Cloud Console](https://console.cloud.google.com/).
2. Sign in with the Google account that receives your Rover notifications.
3. In the top navigation bar, open the project selector and click **"New Project"**.
4. Name the project (for example: `rover-client-hub`) and click **Create**.

### Step 2: Enable the Gmail API
1. In the navigation menu (☰), go to **APIs & Services** > **Library** (or search for *"Gmail API"*).
2. Select **Gmail API** and click the blue **Enable** button.

### Step 3: Configure OAuth Consent Screen
1. Go to **APIs & Services** > **OAuth consent screen**.
2. Select **External** as the *User Type* (or *Internal* if using Google Workspace) and click **Create**.
3. Fill in the required fields:
   - **App name:** `Rover Client Hub`
   - **User support email:** Your email address.
   - **Developer contact information:** Your email address.
4. Click **Save and Continue**.
5. Under **Scopes**, click **Add or Remove Scopes**:
   - Filter and select: `https://www.googleapis.com/auth/gmail.readonly`.
   - Click **Update**, then click **Save and Continue**.
6. Under **Test users**:
   - Click **+ Add Users**.
   - Enter your Gmail address (the account receiving Rover emails).
   - Click **Save and Continue**.

### Step 4: Create OAuth2 Credentials
1. Go to **APIs & Services** > **Credentials**.
2. Click **+ Create Credentials** at the top and choose **OAuth client ID**.
3. Under **Application type**, select **Desktop app**.
4. Set the name to `Rover Desktop Client` and click **Create**.
5. In the confirmation dialog, click **Download JSON**.
6. Rename the downloaded file to exactly:
   ```text
   credentials.json
   ```
7. Place `credentials.json` in the root of this project (`pet-client-responses/credentials.json`) or upload it directly through the sidebar in Streamlit.

> [!NOTE]
> The first time you click "Import Latest Rover Emails", a browser tab will prompt you to log in and grant read-only permissions. Once authorized, a local `token.json` file is created so you won't need to re-authenticate.

---

## Option 2: Gmail MCP Server Integration

If you use an MCP (Model Context Protocol) compatible host (Claude Desktop, Antigravity, or Cursor):

### Configuration (`mcp_config.json`):
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

## 🔒 Security & Privacy
* The project [`.gitignore`](file:///home/dagudelo/code/work/pet-client-responses/.gitignore) is configured to ignore:
  - `credentials.json`
  - `token.json`
  - `*.env*`
* Your secrets, credentials, and OAuth tokens are **never** committed or pushed to GitHub.
