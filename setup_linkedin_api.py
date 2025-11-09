"""
LinkedIn API Setup Assistant
Automatisches Setup für Access Token und Organization ID
"""
import requests
import webbrowser
from urllib.parse import urlencode
import os
from dotenv import load_dotenv, set_key

# Lade .env Datei
load_dotenv()

# Konfiguration
LINKEDIN_CLIENT_ID = os.getenv("LINKEDIN_CLIENT_ID")
LINKEDIN_CLIENT_SECRET = os.getenv("LINKEDIN_CLIENT_SECRET")
LINKEDIN_COMPANY_NAME = os.getenv("LINKEDIN_COMPANY_NAME", "Invory")
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
            return response.json()
        else:
            print(f"❌ Token-Fehler: {response.status_code}")
            print(f"Response: {response.text}")
            return None
    except Exception as e:
        print(f"❌ Fehler beim Token-Austausch: {str(e)}")
        return None

def get_organization_id(access_token, company_name):
    """Ruft die Organization ID über die LinkedIn API ab"""
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
        "X-Restli-Protocol-Version": "2.0.0"
    }
    
    try:
        # Methode 1: Über Administrative-Organizations
        endpoint = "https://api.linkedin.com/v2/organizationalEntityAcls"
        params = {
            "q": "roleAssignee"
        }
        
        response = requests.get(endpoint, headers=headers, params=params, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if 'elements' in data and len(data['elements']) > 0:
                for element in data['elements']:
                    org_urn = element.get('organizationalTarget', '')
                    if org_urn.startswith('urn:li:organization:'):
                        org_id = org_urn.split(':')[-1]
                        
                        # Überprüfe Organisationsname
                        org_info = get_organization_info(access_token, org_id)
                        if org_info and company_name.lower() in org_info.get('name', '').lower():
                            return org_id, org_info
                        else:
                            # Falls Name nicht übereinstimmt, verwende trotzdem die erste gefundene
                            return org_id, org_info
        
        print(f"⚠️  Keine Organisationen gefunden über Administrative API")
        return None, None
        
    except Exception as e:
        print(f"❌ Fehler beim Abrufen der Organization ID: {str(e)}")
        return None, None

def get_organization_info(access_token, org_id):
    """Ruft Details einer Organisation ab"""
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
        "X-Restli-Protocol-Version": "2.0.0"
    }
    
    try:
        endpoint = f"https://api.linkedin.com/v2/organizations/{org_id}"
        response = requests.get(endpoint, headers=headers, timeout=10)
        
        if response.status_code == 200:
            return response.json()
        else:
            print(f"❌ Fehler beim Abrufen der Org-Info: {response.status_code}")
            return None
    except Exception as e:
        print(f"❌ Fehler: {str(e)}")
        return None

def update_env_file(access_token, organization_id):
    """Aktualisiert die .env Datei mit den neuen Werten"""
    env_file = '.env'
    
    # Erstelle .env falls nicht vorhanden
    if not os.path.exists(env_file):
        print("📄 Erstelle neue .env Datei...")
        with open(env_file, 'w') as f:
            f.write("# LinkedIn API Konfiguration\n")
    
    try:
        set_key(env_file, 'LINKEDIN_ACCESS_TOKEN', access_token)
        set_key(env_file, 'LINKEDIN_ORGANIZATION_ID', organization_id)
        
        print(f"\n✅ .env Datei wurde aktualisiert!")
        print(f"   LINKEDIN_ACCESS_TOKEN: {access_token[:20]}...")
        print(f"   LINKEDIN_ORGANIZATION_ID: {organization_id}")
        
    except Exception as e:
        print(f"❌ Fehler beim Aktualisieren der .env Datei: {str(e)}")
        print(f"\nBitte fügen Sie manuell hinzu:")
        print(f"LINKEDIN_ACCESS_TOKEN={access_token}")
        print(f"LINKEDIN_ORGANIZATION_ID={organization_id}")

def main():
    """Hauptfunktion für das komplette LinkedIn API Setup"""
    print("=" * 80)
    print("🔧 LinkedIn API Setup Assistant")
    print("=" * 80)
    
    # Prüfe Voraussetzungen
    if not LINKEDIN_CLIENT_ID or not LINKEDIN_CLIENT_SECRET:
        print("❌ Fehler: LINKEDIN_CLIENT_ID und LINKEDIN_CLIENT_SECRET müssen in .env gesetzt sein")
        print("\n📋 Schritte:")
        print("1. Erstellen Sie eine LinkedIn App unter https://www.linkedin.com/developers/")
        print("2. Kopieren Sie Client ID und Client Secret")
        print("3. Fügen Sie sie in Ihre .env Datei ein:")
        print("   LINKEDIN_CLIENT_ID=your_client_id")
        print("   LINKEDIN_CLIENT_SECRET=your_client_secret")
        return
    
    # Schritt 1: Access Token abrufen
    print(f"\n🔑 Schritt 1: Access Token abrufen")
    print(f"   Unternehmensname: {LINKEDIN_COMPANY_NAME}")
    print("-" * 50)
    
    # Erstelle Autorisierungs-URL
    auth_url = "https://www.linkedin.com/oauth/v2/authorization"
    params = {
        "response_type": "code",
        "client_id": LINKEDIN_CLIENT_ID,
        "redirect_uri": REDIRECT_URI,
        "state": "linkedin_setup_12345",
        "scope": SCOPES
    }
    
    auth_url_with_params = f"{auth_url}?{urlencode(params)}"
    
    print(f"\n1. Öffnen Sie diese URL im Browser:")
    print(f"\n{auth_url_with_params}\n")
    print("2. Melden Sie sich als Administrator der Unternehmensseite an")
    print("3. Autorisieren Sie die App")
    print(f"4. Kopieren Sie den 'code' Parameter aus der Redirect-URL")
    
    # Öffne Browser automatisch
    try:
        webbrowser.open(auth_url_with_params)
        print("\n🌐 Browser wurde automatisch geöffnet")
    except Exception as e:
        print(f"\n⚠️  Konnte Browser nicht automatisch öffnen: {e}")
    
    # Authorization Code eingeben
    print("\n" + "-" * 50)
    authorization_code = input("📝 Authorization Code eingeben: ").strip()
    
    if not authorization_code:
        print("❌ Kein Code eingegeben. Abgebrochen.")
        return
    
    # Bereinige Code falls URL eingegeben wurde
    if 'code=' in authorization_code:
        authorization_code = authorization_code.split('code=')[1].split('&')[0]
    
    # Token abrufen
    print("\n🔄 Tausche Code gegen Access Token...")
    token_info = exchange_code_for_token(authorization_code)
    
    if not token_info:
        print("❌ Fehler beim Abrufen des Access Tokens")
        return
    
    access_token = token_info.get('access_token')
    print(f"✅ Access Token erhalten: {access_token[:20]}...")
    
    # Schritt 2: Organization ID abrufen
    print(f"\n🏢 Schritt 2: Organization ID für '{LINKEDIN_COMPANY_NAME}' abrufen")
    print("-" * 50)
    
    org_id, org_info = get_organization_id(access_token, LINKEDIN_COMPANY_NAME)
    
    if org_id:
        org_name = org_info.get('name', 'Unbekannt') if org_info else 'Unbekannt'
        print(f"✅ Organization ID gefunden: {org_id}")
        print(f"   Organisationsname: {org_name}")
        
        # Schritt 3: .env Datei aktualisieren
        print(f"\n💾 Schritt 3: .env Datei aktualisieren")
        print("-" * 50)
        
        update_env_file(access_token, org_id)
        
        # Erfolgsmeldung
        print(f"\n" + "=" * 80)
        print("🎉 SETUP ERFOLGREICH ABGESCHLOSSEN!")
        print("=" * 80)
        print(f"✅ Access Token: Gespeichert in .env")
        print(f"✅ Organization ID: {org_id}")
        print(f"✅ Organisation: {org_name}")
        print(f"\n🚀 Sie können jetzt das Multi-Agent-System verwenden:")
        print(f"   python main.py --mode preview")
        print("=" * 80)
        
    else:
        print(f"❌ Keine Organization ID gefunden für '{LINKEDIN_COMPANY_NAME}'")
        print(f"\n💡 Mögliche Ursachen:")
        print(f"   - Der Account ist kein Administrator der Unternehmensseite")
        print(f"   - Der Unternehmensname ist falsch")
        print(f"   - Unzureichende API-Berechtigungen")
        
        # Speichere trotzdem den Access Token
        print(f"\n💾 Speichere Access Token (Organization ID manuell hinzufügen)...")
        try:
            set_key('.env', 'LINKEDIN_ACCESS_TOKEN', access_token)
            print(f"✅ Access Token gespeichert in .env")
            print(f"\n📝 Bitte fügen Sie manuell hinzu:")
            print(f"LINKEDIN_ORGANIZATION_ID=your_organization_id")
        except Exception as e:
            print(f"❌ Fehler: {str(e)}")

if __name__ == "__main__":
    main()