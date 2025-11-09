# LinkedIn Access Token Setup-Anleitung

## 🎯 Übersicht

Um Posts auf der Invory LinkedIn Unternehmensseite zu veröffentlichen, benötigen Sie einen LinkedIn Access Token mit den richtigen Berechtigungen.

## 📋 Schritt-für-Schritt Anleitung

### Schritt 1: LinkedIn Developer App erstellen

1. **Gehen Sie zu LinkedIn Developers**:
   - Besuchen Sie: https://www.linkedin.com/developers/
   - Melden Sie sich mit Ihrem LinkedIn-Account an

2. **Neue App erstellen**:
   - Klicken Sie auf "Create app"
   - Füllen Sie das Formular aus:
     - **App name**: z.B. "XRechnung Post Agent"
     - **LinkedIn Page**: Wählen Sie die Invory Unternehmensseite
     - **Privacy policy URL**: Geben Sie eine URL zu Ihrer Datenschutzerklärung ein
     - **App logo**: Optional - Laden Sie ein Logo hoch
   - Akzeptieren Sie die Nutzungsbedingungen
   - Klicken Sie auf "Create app"

### Schritt 2: Berechtigungen konfigurieren

1. **Gehen Sie zum Tab "Auth"** in Ihrer App

2. **Produkt hinzufügen**:
   - Suchen Sie nach "Sign In with LinkedIn using OpenID Connect"
   - Klicken Sie auf "Request access"

3. **Berechtigungen (Scopes) konfigurieren**:
   - Gehen Sie zum Tab "Products" → "Sign In with LinkedIn using OpenID Connect"
   - Klicken Sie auf "Request access" falls noch nicht geschehen

4. **Wichtige Berechtigungen für Unternehmens-Posting**:
   - `r_organization_social` - Lesen von Unternehmensseiten-Posts
   - `w_organization_social` - Schreiben/Erstellen von Unternehmensseiten-Posts
   - `r_basicprofile` - Grundlegende Profilinformationen lesen
   - `r_liteprofile` - Lite-Profilinformationen lesen (falls verfügbar)

### Schritt 3: Redirect URLs konfigurieren

1. **Gehen Sie zum Tab "Auth"**
2. **Fügen Sie Redirect URLs hinzu**:
   - **Einfache Methode**: Verwenden Sie eine öffentliche URL wie `https://www.google.com`
   - **Alternative**: Verwenden Sie `https://oauthdebugger.com/debug` (für Tests)
   - **Für Produktion**: Ihre Produktions-URL
   - Klicken Sie auf "Update"
   
   **Wichtig**: Die Redirect-URL muss öffentlich erreichbar sein. localhost funktioniert nicht, da LinkedIn von außen nicht darauf zugreifen kann.

### Schritt 4: Client ID und Client Secret notieren

1. **Im Tab "Auth" finden Sie**:
   - **Client ID**: Kopieren Sie diese
   - **Client Secret**: Kopieren Sie diese (klicken Sie auf "Show" um es anzuzeigen)

2. **Fügen Sie diese in Ihre `.env` Datei ein**:
   ```bash
   LINKEDIN_CLIENT_ID=your_client_id_here
   LINKEDIN_CLIENT_SECRET=your_client_secret_here
   ```

### Schritt 5: Access Token generieren

Es gibt zwei Methoden, um einen Access Token zu erhalten:

#### Methode 1: Python-Skript (Empfohlen - Einfachste Methode)

1. **Fügen Sie Redirect URI in .env ein** (optional, Standard: https://www.google.com):
   ```bash
   LINKEDIN_REDIRECT_URI=https://www.google.com
   ```

2. **Führen Sie das Skript aus**:
   ```bash
   python3 get_linkedin_token.py
   ```

3. **Folgen Sie den Anweisungen**:
   - Das Skript öffnet automatisch einen Browser
   - Melden Sie sich an und autorisierten Sie die App
   - Nach der Autorisierung werden Sie zu Google weitergeleitet
   - Kopieren Sie den `code` Parameter aus der URL
   - Fügen Sie den Code in das Skript ein
   - Das Skript generiert automatisch den Access Token

#### Methode 2: Manueller OAuth 2.0 Flow

1. **Autorisierungs-URL erstellen**:
   ```
   https://www.linkedin.com/oauth/v2/authorization?
   response_type=code&
   client_id=YOUR_CLIENT_ID&
   redirect_uri=https://www.google.com&
   state=STATE&
   scope=r_organization_social w_organization_social r_basicprofile
   ```

2. **Benutzer autorisieren**:
   - Öffnen Sie die URL im Browser
   - Melden Sie sich mit einem LinkedIn-Account an, der Administrator der Invory-Seite ist
   - Autorisierten Sie die App

3. **Authorization Code erhalten**:
   - Nach der Autorisierung werden Sie zu Google weitergeleitet
   - Die URL sieht so aus: `https://www.google.com/?code=AUTHORIZATION_CODE&state=...`
   - Kopieren Sie den `code` Parameter (den Teil nach `code=` und vor `&`)

4. **Access Token abrufen**:
   ```bash
   curl -X POST https://www.linkedin.com/oauth/v2/accessToken \
     -d "grant_type=authorization_code" \
     -d "code=YOUR_AUTHORIZATION_CODE" \
     -d "redirect_uri=https://www.google.com" \
     -d "client_id=YOUR_CLIENT_ID" \
     -d "client_secret=YOUR_CLIENT_SECRET"
   ```

### Schritt 6: Access Token in .env speichern

Fügen Sie den Access Token zu Ihrer `.env` Datei hinzu:
```bash
LINKEDIN_ACCESS_TOKEN=your_access_token_here
```

## 🔧 Python-Skript für Token-Generierung

Erstellen Sie eine Datei `get_linkedin_token.py`:

```python
"""
LinkedIn Access Token Generator
"""
import requests
import webbrowser
from urllib.parse import urlencode, parse_qs, urlparse
import http.server
import socketserver
from threading import Timer
import os
from config import LINKEDIN_CLIENT_ID, LINKEDIN_CLIENT_SECRET

# Konfiguration
REDIRECT_URI = "http://localhost:8000/callback"
SCOPES = "r_organization_social w_organization_social r_basicprofile"

class CallbackHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path.startswith('/callback'):
            # Parse query parameters
            query_params = parse_qs(urlparse(self.path).query)
            if 'code' in query_params:
                code = query_params['code'][0]
                
                # Exchange code for access token
                token_url = "https://www.linkedin.com/oauth/v2/accessToken"
                token_data = {
                    "grant_type": "authorization_code",
                    "code": code,
                    "redirect_uri": REDIRECT_URI,
                    "client_id": LINKEDIN_CLIENT_ID,
                    "client_secret": LINKEDIN_CLIENT_SECRET
                }
                
                response = requests.post(token_url, data=token_data)
                if response.status_code == 200:
                    token_info = response.json()
                    access_token = token_info.get('access_token')
                    
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    self.wfile.write(f"""
                    <html>
                    <body>
                        <h1>✅ Access Token erhalten!</h1>
                        <p>Fügen Sie diesen Token in Ihre .env Datei ein:</p>
                        <pre>{access_token}</pre>
                        <p><strong>Wichtig:</strong> Speichern Sie diesen Token sicher!</p>
                    </body>
                    </html>
                    """.encode())
                    
                    print(f"\n✅ Access Token: {access_token}")
                    print("\n⚠️  Fügen Sie diesen Token in Ihre .env Datei ein:")
                    print(f"LINKEDIN_ACCESS_TOKEN={access_token}")
                else:
                    self.send_response(400)
                    self.end_headers()
                    self.wfile.write(b"Error getting token")
            else:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(b"No code received")
        else:
            self.send_response(404)
            self.end_headers()

def get_access_token():
    """Hauptfunktion zum Abrufen des Access Tokens"""
    # Erstelle Autorisierungs-URL
    auth_url = "https://www.linkedin.com/oauth/v2/authorization"
    params = {
        "response_type": "code",
        "client_id": LINKEDIN_CLIENT_ID,
        "redirect_uri": REDIRECT_URI,
        "state": "random_state_string",
        "scope": SCOPES
    }
    
    auth_url_with_params = f"{auth_url}?{urlencode(params)}"
    
    # Starte lokalen Server für Callback
    port = 8000
    handler = CallbackHandler
    httpd = socketserver.TCPServer(("", port), handler)
    
    print("=" * 80)
    print("LinkedIn Access Token Generator")
    print("=" * 80)
    print(f"\n1. Öffne diese URL im Browser:")
    print(f"\n{auth_url_with_params}\n")
    print("2. Melden Sie sich an und autorisieren Sie die App")
    print("3. Sie werden automatisch zurückgeleitet und der Token wird angezeigt")
    print("\n" + "=" * 80)
    
    # Öffne Browser automatisch
    webbrowser.open(auth_url_with_params)
    
    # Starte Server
    print(f"\n🔄 Warte auf Callback auf Port {port}...")
    httpd.handle_request()  # Behandle eine Anfrage und beende dann

if __name__ == "__main__":
    if not LINKEDIN_CLIENT_ID or not LINKEDIN_CLIENT_SECRET:
        print("❌ Fehler: LINKEDIN_CLIENT_ID und LINKEDIN_CLIENT_SECRET müssen in .env gesetzt sein")
    else:
        get_access_token()
```

## 🔑 Wichtige Hinweise

### Berechtigungen (Scopes)

Für das Posten auf Unternehmensseiten benötigen Sie:
- `r_organization_social` - Lesen von Unternehmensseiten-Posts
- `w_organization_social` - Erstellen von Unternehmensseiten-Posts
- `r_basicprofile` - Grundlegende Profilinformationen

### Administrator-Berechtigung

- Der LinkedIn-Account, mit dem Sie sich anmelden, muss **Administrator der Invory Unternehmensseite** sein
- Andernfalls können Sie keine Posts erstellen

### Token-Gültigkeit

- Access Tokens können ablaufen (typischerweise nach 60 Tagen)
- Bei Ablauf müssen Sie einen neuen Token generieren
- Für Produktion sollten Sie einen Refresh Token Flow implementieren

### Sicherheit

- **Nie** committen Sie Access Tokens in Git
- Speichern Sie Tokens sicher in `.env` Dateien
- Stellen Sie sicher, dass `.env` in `.gitignore` ist

## 🧪 Token testen

Nachdem Sie den Token erhalten haben, testen Sie ihn:

```bash
python3 -c "
from services.linkedin_client import LinkedInClient
client = LinkedInClient()
if client.verify_connection():
    print('✅ LinkedIn-Verbindung erfolgreich!')
    print(f'Organization ID: {client.organization_id}')
else:
    print('❌ Verbindung fehlgeschlagen. Bitte Token überprüfen.')
"
```

## 📚 Weitere Ressourcen

- LinkedIn API Dokumentation: https://docs.microsoft.com/en-us/linkedin/
- OAuth 2.0 Guide: https://docs.microsoft.com/en-us/linkedin/shared/authentication/authentication
- Organization API: https://docs.microsoft.com/en-us/linkedin/marketing/community-management/organizations/organization-lookup-api

## 🆘 Troubleshooting

### Problem: "Invalid redirect URI"
- **Lösung**: Stellen Sie sicher, dass die Redirect-URL in der LinkedIn App konfiguriert ist

### Problem: "Invalid client credentials"
- **Lösung**: Überprüfen Sie Client ID und Client Secret

### Problem: "Insufficient permissions"
- **Lösung**: Stellen Sie sicher, dass der Account Administrator der Seite ist und die richtigen Scopes angefordert wurden

### Problem: "Organization ID nicht gefunden"
- **Lösung**: Das System versucht automatisch, die Organization ID zu finden. Falls das fehlschlägt, setzen Sie `LINKEDIN_ORGANIZATION_ID` manuell in `.env`

