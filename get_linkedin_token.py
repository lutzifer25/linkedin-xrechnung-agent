"""
LinkedIn Access Token Generator
Einfaches Skript zum Abrufen eines LinkedIn Access Tokens
Funktioniert ohne lokalen Server - manuelle Eingabe des Authorization Codes
"""
import requests
import webbrowser
from urllib.parse import urlencode
import os
from dotenv import load_dotenv

# Lade .env Datei
load_dotenv()

# Konfiguration
LINKEDIN_CLIENT_ID = os.getenv("LINKEDIN_CLIENT_ID")
LINKEDIN_CLIENT_SECRET = os.getenv("LINKEDIN_CLIENT_SECRET")

# Wichtige Hinweise für Redirect URL:
# - Sie können eine beliebige öffentliche URL verwenden (z.B. https://www.google.com)
# - Oder eine Test-URL wie https://oauthdebugger.com/debug
# - Der Authorization Code wird in der URL nach dem Redirect erscheinen
REDIRECT_URI = os.getenv("LINKEDIN_REDIRECT_URI", "https://www.google.com")
SCOPES = "r_organization_social w_organization_social r_basicprofile"

def exchange_code_for_token(authorization_code):
    """Tauscht Authorization Code gegen Access Token"""
    token_url = "https://www.linkedin.com/oauth/v2/accessToken"
    token_data = {
        "grant_type": "authorization_code",
        "code": authorization_code,
        "redirect_uri": REDIRECT_URI,
        "client_id": LINKEDIN_CLIENT_ID,
        "client_secret": LINKEDIN_CLIENT_SECRET
    }
    
    try:
        response = requests.post(token_url, data=token_data)
        if response.status_code == 200:
            token_info = response.json()
            return token_info
        else:
            print(f"❌ Fehler: {response.status_code}")
            print(f"Response: {response.text}")
            return None
    except Exception as e:
        print(f"❌ Fehler beim Token-Austausch: {str(e)}")
        return None

def get_access_token():
    """Hauptfunktion zum Abrufen des Access Tokens (manuelle Eingabe)"""
    if not LINKEDIN_CLIENT_ID or not LINKEDIN_CLIENT_SECRET:
        print("❌ Fehler: LINKEDIN_CLIENT_ID und LINKEDIN_CLIENT_SECRET müssen in .env gesetzt sein")
        print("\nSchritte:")
        print("1. Erstellen Sie eine LinkedIn App unter https://www.linkedin.com/developers/")
        print("2. Kopieren Sie Client ID und Client Secret")
        print("3. Fügen Sie sie in Ihre .env Datei ein:")
        print("   LINKEDIN_CLIENT_ID=your_client_id")
        print("   LINKEDIN_CLIENT_SECRET=your_client_secret")
        print("4. Optional: Setzen Sie LINKEDIN_REDIRECT_URI in .env (Standard: https://www.google.com)")
        return
    
    # Erstelle Autorisierungs-URL
    auth_url = "https://www.linkedin.com/oauth/v2/authorization"
    params = {
        "response_type": "code",
        "client_id": LINKEDIN_CLIENT_ID,
        "redirect_uri": REDIRECT_URI,
        "state": "random_state_string_12345",
        "scope": SCOPES
    }
    
    auth_url_with_params = f"{auth_url}?{urlencode(params)}"
    
    print("=" * 80)
    print("🔑 LinkedIn Access Token Generator")
    print("=" * 80)
    print(f"\n📋 Schritt-für-Schritt Anleitung:")
    print(f"\n1. Öffnen Sie diese URL im Browser:")
    print(f"\n{auth_url_with_params}\n")
    print("2. Melden Sie sich mit einem LinkedIn-Account an, der Administrator der Invory-Seite ist")
    print("3. Autorisierten Sie die App")
    print(f"4. Nach der Autorisierung werden Sie zu {REDIRECT_URI} weitergeleitet")
    print("5. Kopieren Sie den 'code' Parameter aus der URL")
    print("   Die URL sieht so aus: https://www.google.com/?code=AUTHORIZATION_CODE&state=...")
    print("   Kopieren Sie nur den Teil nach 'code=' und vor '&'")
    print("\n" + "=" * 80)
    
    # Öffne Browser automatisch
    try:
        webbrowser.open(auth_url_with_params)
        print("\n🌐 Browser wurde automatisch geöffnet")
    except Exception as e:
        print(f"\n⚠️  Konnte Browser nicht automatisch öffnen: {e}")
        print(f"Bitte öffnen Sie die URL manuell")
    
    # Warte auf manuelle Eingabe des Authorization Codes
    print("\n" + "-" * 80)
    authorization_code = input("\n📝 Bitte geben Sie den Authorization Code ein (aus der Redirect-URL): ").strip()
    
    if not authorization_code:
        print("❌ Kein Code eingegeben. Abgebrochen.")
        return
    
    # Entferne mögliche URL-Parameter, falls der ganze Code eingegeben wurde
    if 'code=' in authorization_code:
        authorization_code = authorization_code.split('code=')[1].split('&')[0]
    
    print("\n🔄 Tausche Authorization Code gegen Access Token...")
    
    # Tausche Code gegen Token
    token_info = exchange_code_for_token(authorization_code)
    
    if token_info:
        access_token = token_info.get('access_token')
        expires_in = token_info.get('expires_in', 'unbekannt')
        refresh_token = token_info.get('refresh_token')
        
        print("\n" + "=" * 80)
        print("✅ ACCESS TOKEN ERHALTEN!")
        print("=" * 80)
        print(f"\n🔑 Access Token:")
        print(f"{access_token}")
        print(f"\n⏱️  Gültigkeit: {expires_in} Sekunden ({int(expires_in) // 86400 if isinstance(expires_in, int) else 'unbekannt'} Tage)")
        
        if refresh_token:
            print(f"\n🔄 Refresh Token:")
            print(f"{refresh_token}")
        
        print("\n" + "-" * 80)
        print("⚠️  WICHTIG: Fügen Sie diese Werte in Ihre .env Datei ein:")
        print("-" * 80)
        print(f"LINKEDIN_ACCESS_TOKEN={access_token}")
        if refresh_token:
            print(f"LINKEDIN_REFRESH_TOKEN={refresh_token}")
        print("\n💡 Stellen Sie sicher, dass .env in .gitignore ist!")
        print("=" * 80)
    else:
        print("\n❌ Fehler beim Abrufen des Access Tokens")
        print("Bitte überprüfen Sie:")
        print("1. Ist der Authorization Code korrekt?")
        print("2. Ist die Redirect URI in der LinkedIn App korrekt konfiguriert?")
        print("3. Haben Sie die App autorisiert?")

if __name__ == "__main__":
    get_access_token()

