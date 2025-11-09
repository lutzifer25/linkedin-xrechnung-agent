# Railway OAuth Setup für LinkedIn XRechnung Agent

## 🚂 Railway Deployment mit OAuth Handler

### Schritt 1: Railway App deployen

1. **Repository zu Railway verbinden:**
   ```bash
   # In der Railway Web-Console:
   # 1. New Project → Deploy from GitHub
   # 2. Repository auswählen: linkedin-xrechnung-agent
   # 3. Deploy starten
   ```

2. **Railway URL ermitteln:**
   - Nach dem Deployment zeigt Railway die URL an
   - Format: `https://linkedin-xrechnung-agent-production.up.railway.app`
   - Oder custom domain falls konfiguriert

### Schritt 2: LinkedIn App konfigurieren

1. **Gehe zu https://www.linkedin.com/developers/**
2. **Wähle deine LinkedIn App aus**
3. **Unter "Auth" → "Authorized redirect URLs for your app":**
   ```
   https://your-railway-app.railway.app/auth/callback
   ```
   
   **Beispiel:**
   ```
   https://linkedin-xrechnung-agent-production.up.railway.app/auth/callback
   ```

### Schritt 3: Umgebungsvariablen in Railway setzen

In der Railway Console unter "Variables":

```bash
# LinkedIn API Credentials
LINKEDIN_CLIENT_ID=your_linkedin_client_id
LINKEDIN_CLIENT_SECRET=your_linkedin_client_secret
LINKEDIN_REDIRECT_URI=https://your-railway-app.railway.app/auth/callback
LINKEDIN_COMPANY_NAME=Invory

# OpenAI API
OPENAI_API_KEY=your_openai_api_key
OPENAI_MODEL=gpt-4-turbo-preview

# Post Settings
POST_FREQUENCY=daily
POST_TIME=09:00
```

### Schritt 4: OAuth Flow testen

1. **Railway App öffnen:**
   ```
   https://your-railway-app.railway.app
   ```

2. **OAuth Flow starten:**
   - Die App startet automatisch den OAuth-Handler
   - Bei LinkedIn Authentication wird zur Railway URL redirected
   - Authorization Code wird auf der Success-Page angezeigt

### Schritt 5: LinkedIn Authentication

**Option A: Über Railway Web Interface**

1. Öffne deine Railway App URL
2. Gehe zu `/auth/callback` Endpoint (wird automatisch aufgerufen)
3. Browser zeigt Success-Page mit Authorization Code
4. Code kopieren für lokale Verwendung

**Option B: Lokaler Test mit Railway Redirect**

```bash
# Lokale .env mit Railway Redirect URL
LINKEDIN_REDIRECT_URI=https://your-railway-app.railway.app/auth/callback

# Lokalen Test starten
python main.py --mode preview
```

## 🔧 Railway Konfiguration Details

### railway.json
```json
{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "python3 railway_oauth_handler.py",
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }
}
```

### OAuth Handler Endpoints

- **`/`** - Hauptseite mit Informationen
- **`/auth/callback`** - LinkedIn OAuth Callback
- **`/health`** - Health Check für Railway
- **`/info`** - Service-Informationen

### Automatische Features

1. **OAuth Success Page** - Zeigt Authorization Code übersichtlich an
2. **Copy-to-Clipboard** - Ein Klick zum Kopieren des Codes
3. **Health Monitoring** - Railway kann App-Status überwachen
4. **Error Handling** - Robuste Fehlerbehandlung für OAuth-Probleme

## 🚀 Production Workflow

### Für automatisierte Posts auf Railway:

1. **OAuth einmalig durchführen** (über Web Interface)
2. **Access Token in Railway Variables setzen:**
   ```bash
   LINKEDIN_ACCESS_TOKEN=your_obtained_token
   LINKEDIN_ORGANIZATION_ID=your_obtained_org_id
   ```
3. **Railway Startkommando ändern:**
   ```json
   "startCommand": "python3 scheduler.py"
   ```

### Für lokale Entwicklung mit Railway OAuth:

```bash
# .env lokal
LINKEDIN_REDIRECT_URI=https://your-railway-app.railway.app/auth/callback

# Test lokal ausführen
python main.py --mode preview
```

## 🔒 Sicherheit

- **HTTPS only** - Railway stellt automatisch HTTPS bereit
- **State Parameter** - OAuth State Validation
- **Error Handling** - Sichere Fehlerbehandlung
- **No Token Storage** - Authorization Code wird nur temporär angezeigt

## 🐛 Troubleshooting

### Problem: "Redirect URI Mismatch"
**Lösung:** 
- Prüfe die exakte Railway URL
- Stelle sicher, dass `/auth/callback` am Ende steht
- Verwende HTTPS, nicht HTTP

### Problem: Railway App startet nicht
**Lösung:**
- Prüfe Railway Logs
- Stelle sicher, dass `flask` in requirements.txt ist
- Prüfe Umgebungsvariablen

### Problem: OAuth Code kommt nicht an
**Lösung:**
- Öffne Railway App URL direkt
- Prüfe `/health` Endpoint
- Überprüfe LinkedIn App Permissions