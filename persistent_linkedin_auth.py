"""
LinkedIn Token Persistence Manager
Speichert Access Token dauerhaft zur wiederverwendung
"""
import requests
import webbrowser
from urllib.parse import urlencode
import os
import sys
from typing import Optional, Dict, Tuple
from dotenv import load_dotenv, set_key
import json
from datetime import datetime, timedelta

# Lade .env Datei
load_dotenv()

class LinkedInTokenManager:
    """Verwaltet dauerhafte LinkedIn Token-Speicherung"""
    
    def __init__(self):
        self.client_id = os.getenv("LINKEDIN_CLIENT_ID")
        self.client_secret = os.getenv("LINKEDIN_CLIENT_SECRET")
        self.company_name = os.getenv("LINKEDIN_COMPANY_NAME", "Invory")
        self.redirect_uri = os.getenv("LINKEDIN_REDIRECT_URI", "https://worker-production-68c1.up.railway.app/auth/callback")
        self.scopes = "openid profile email w_member_social"
        self.env_file_path = ".env"
        
    def get_or_refresh_token(self) -> Tuple[Optional[str], Optional[str]]:
        """
        Holt gespeicherten Token oder startet einmaligen Setup-Prozess
        
        Returns:
            Tuple[access_token, organization_id] oder (None, None) bei Fehler
        """
        # Prüfe existierenden Token
        existing_token = os.getenv("LINKEDIN_ACCESS_TOKEN")
        existing_org_id = os.getenv("LINKEDIN_ORGANIZATION_ID")
        
        if existing_token and existing_token.strip():
            print("✅ Gespeicherter LinkedIn Access Token gefunden")
            
            # Teste Token-Gültigkeit
            if self._test_token_validity(existing_token):
                print("✅ Access Token ist noch gültig")
                return existing_token, existing_org_id
            else:
                print("⚠️ Access Token ist abgelaufen - erneuere...")
        
        # Kein gültiger Token vorhanden - starte Setup
        print("\n🔑 LinkedIn Token Setup (einmalig erforderlich)")
        print("=" * 50)
        print("Dieser Prozess muss nur einmal durchgeführt werden.")
        print("Der Token wird dann dauerhaft gespeichert.\n")
        
        return self._setup_new_token()
    
    def _test_token_validity(self, token: str) -> bool:
        """Testet ob ein Access Token noch gültig ist"""
        try:
            headers = {
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json"
            }
            
            response = requests.get(
                "https://api.linkedin.com/v2/people/~",
                headers=headers,
                timeout=10
            )
            
            return response.status_code == 200
        except Exception:
            return False
    
    def _setup_new_token(self) -> Tuple[Optional[str], Optional[str]]:
        """Führt einmalige Token-Erstellung durch"""
        
        # Schritt 1: Authorization Code holen
        auth_code = self._get_authorization_code()
        if not auth_code:
            return None, None
        
        # Schritt 2: Access Token tauschen
        access_token = self._exchange_code_for_token(auth_code)
        if not access_token:
            return None, None
        
        # Schritt 3: Token dauerhaft speichern
        self._save_token_to_env(access_token)
        
        # Schritt 4: Organization ID ermitteln (optional für persönliche Posts)
        org_id = self._get_organization_id(access_token)
        if org_id:
            self._save_org_id_to_env(org_id)
        
        print("✅ LinkedIn Token erfolgreich eingerichtet und gespeichert!")
        print("🎯 Zukünftige Ausführungen benötigen keine Browser-Interaktion mehr.")
        
        return access_token, org_id
    
    def _get_authorization_code(self) -> Optional[str]:
        """Holt Authorization Code via Browser (einmalig)"""
        
        # Authorization URL erstellen
        auth_params = {
            "response_type": "code",
            "client_id": self.client_id,
            "redirect_uri": self.redirect_uri,
            "scope": self.scopes
        }
        
        auth_url = f"https://www.linkedin.com/oauth/v2/authorization?{urlencode(auth_params)}"
        
        print("🌐 Schritt 1: Browser-Authentifizierung (einmalig)")
        print("-" * 40)
        print("1. Browser wird geöffnet...")
        print("2. Melden Sie sich bei LinkedIn an")
        print("3. Autorisieren Sie die App")
        print("4. Kopieren Sie den 'code' Parameter aus der Redirect-URL")
        
        try:
            webbrowser.open(auth_url)
            print("🌐 Browser geöffnet")
        except Exception:
            print(f"⚠️ Browser konnte nicht geöffnet werden. Öffnen Sie manuell: {auth_url}")
        
        print(f"\n📝 Authorization Code: ", end="")
        auth_code = input().strip()
        
        if not auth_code:
            print("❌ Kein Authorization Code eingegeben")
            return None
            
        return auth_code
    
    def _exchange_code_for_token(self, auth_code: str) -> Optional[str]:
        """Tauscht Authorization Code gegen Access Token"""
        try:
            token_url = "https://www.linkedin.com/oauth/v2/accessToken"
            
            data = {
                "grant_type": "authorization_code",
                "code": auth_code,
                "redirect_uri": self.redirect_uri,
                "client_id": self.client_id,
                "client_secret": self.client_secret
            }
            
            response = requests.post(token_url, data=data, timeout=10)
            
            if response.status_code == 200:
                token_data = response.json()
                access_token = token_data.get("access_token")
                
                if access_token:
                    print("✅ Access Token erhalten")
                    return access_token
                else:
                    print("❌ Kein Access Token in Antwort")
                    return None
            else:
                print(f"❌ Token-Fehler: {response.status_code} - {response.text}")
                return None
                
        except Exception as e:
            print(f"❌ Fehler beim Token-Austausch: {str(e)}")
            return None
    
    def _save_token_to_env(self, access_token: str):
        """Speichert Access Token dauerhaft in .env Datei"""
        try:
            set_key(self.env_file_path, "LINKEDIN_ACCESS_TOKEN", access_token)
            print("💾 Access Token in .env gespeichert")
        except Exception as e:
            print(f"⚠️ Fehler beim Speichern des Tokens: {str(e)}")
    
    def _save_org_id_to_env(self, org_id: str):
        """Speichert Organization ID dauerhaft in .env Datei"""
        try:
            set_key(self.env_file_path, "LINKEDIN_ORGANIZATION_ID", org_id)
            print("💾 Organization ID in .env gespeichert")
        except Exception as e:
            print(f"⚠️ Fehler beim Speichern der Organization ID: {str(e)}")
    
    def _get_organization_id(self, access_token: str) -> Optional[str]:
        """Versucht Organization ID zu ermitteln (optional für persönliche Posts)"""
        try:
            headers = {
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json"
            }
            
            # Versuche Organization ACLs abzurufen
            response = requests.get(
                "https://api.linkedin.com/v2/organizationAcls?q=roleAssignee&role=ADMINISTRATOR",
                headers=headers,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                organizations = data.get('elements', [])
                
                for org_data in organizations:
                    org_info = org_data.get('organization~', {})
                    org_name = org_info.get('localizedName', '')
                    
                    if self.company_name.lower() in org_name.lower():
                        org_id = org_info.get('id')
                        if org_id:
                            print(f"✅ Organization ID gefunden: {org_id} für {org_name}")
                            return str(org_id)
                
                print("ℹ️ Keine passende Organisation gefunden - verwende persönliche Posts")
                return None
            else:
                print("ℹ️ Organization-Zugriff nicht verfügbar - verwende persönliche Posts")
                return None
                
        except Exception as e:
            print(f"ℹ️ Konnte Organization ID nicht ermitteln: {str(e)}")
            return None


# Hilfsfunktion für Rückwärtskompatibilität
def get_linkedin_credentials() -> Tuple[Optional[str], Optional[str]]:
    """
    Kompatibilitäts-Wrapper für bestehenden Code
    
    Returns:
        Tuple[access_token, organization_id]
    """
    manager = LinkedInTokenManager()
    return manager.get_or_refresh_token()


def main():
    """Hauptfunktion für direkten Aufruf"""
    print("🔧 LinkedIn Token Manager")
    print("=" * 30)
    
    manager = LinkedInTokenManager()
    token, org_id = manager.get_or_refresh_token()
    
    if token:
        print("\n✅ Setup erfolgreich abgeschlossen!")
        print(f"Access Token: {token[:20]}...")
        if org_id:
            print(f"Organization ID: {org_id}")
        else:
            print("Organization ID: Nicht verfügbar (persönliche Posts werden verwendet)")
    else:
        print("\n❌ Setup fehlgeschlagen")
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())