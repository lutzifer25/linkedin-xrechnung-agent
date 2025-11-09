"""
Dynamic LinkedIn API Manager
Holt Access Token und Organization ID automatisch zur Laufzeit
"""
import requests
import webbrowser
from urllib.parse import urlencode
import os
import sys
from typing import Optional, Dict, Tuple
from dotenv import load_dotenv

# Lade .env Datei
load_dotenv()

class LinkedInDynamicAuth:
    """Dynamische LinkedIn Authentifizierung zur Laufzeit"""
    
    def __init__(self):
        self.client_id = os.getenv("LINKEDIN_CLIENT_ID")
        self.client_secret = os.getenv("LINKEDIN_CLIENT_SECRET")
        self.company_name = os.getenv("LINKEDIN_COMPANY_NAME", "Invory")
        self.redirect_uri = os.getenv("LINKEDIN_REDIRECT_URI", "https://www.google.com")
        self.scopes = "r_organization_social w_organization_social r_basicprofile"
        
        # Cache für Session
        self._access_token = None
        self._organization_id = None
        
    def get_credentials(self) -> Tuple[Optional[str], Optional[str]]:
        """
        Holt LinkedIn Credentials dynamisch zur Laufzeit
        
        Returns:
            Tuple[access_token, organization_id] oder (None, None) bei Fehler
        """
        # Prüfe ob bereits gecacht
        if self._access_token and self._organization_id:
            return self._access_token, self._organization_id
        
        # Prüfe Voraussetzungen
        if not self.client_id or not self.client_secret:
            print("❌ LINKEDIN_CLIENT_ID und LINKEDIN_CLIENT_SECRET müssen in .env gesetzt sein")
            return None, None
        
        print("\n🔑 LinkedIn API Setup - Authentifizierung erforderlich")
        print("=" * 60)
        
        # Hole Access Token
        access_token = self._get_access_token_interactive()
        if not access_token:
            return None, None
        
        # Hole Organization ID
        organization_id = self._get_organization_id(access_token)
        if not organization_id:
            print("❌ Konnte Organization ID nicht abrufen")
            return access_token, None
        
        # Cache für Session
        self._access_token = access_token
        self._organization_id = organization_id
        
        print(f"✅ LinkedIn API bereit!")
        print(f"   Organization: {self.company_name} (ID: {organization_id})")
        
        return access_token, organization_id
    
    def _get_access_token_interactive(self) -> Optional[str]:
        """Holt Access Token interaktiv"""
        print(f"\n🌐 Schritt 1: Browser-Authentifizierung")
        print("-" * 40)
        
        # Erstelle Auth URL
        auth_url = "https://www.linkedin.com/oauth/v2/authorization"
        params = {
            "response_type": "code",
            "client_id": self.client_id,
            "redirect_uri": self.redirect_uri,
            "state": "dynamic_auth_12345",
            "scope": self.scopes
        }
        
        auth_url_with_params = f"{auth_url}?{urlencode(params)}"
        
        print("1. Browser wird geöffnet...")
        print("2. Melden Sie sich als Unternehmens-Administrator an")
        print("3. Autorisieren Sie die App")
        
        # Öffne Browser
        try:
            webbrowser.open(auth_url_with_params)
            print("🌐 Browser geöffnet")
        except Exception as e:
            print(f"⚠️  Browser-Fehler: {e}")
            print(f"Öffnen Sie manuell: {auth_url_with_params}")
        
        # Code eingeben
        print("\n4. Kopieren Sie den 'code' Parameter aus der Redirect-URL")
        auth_code = input("\n📝 Authorization Code: ").strip()
        
        if not auth_code:
            print("❌ Kein Code eingegeben")
            return None
        
        # Bereinige Code
        if 'code=' in auth_code:
            auth_code = auth_code.split('code=')[1].split('&')[0]
        
        # Tausche Code gegen Token
        return self._exchange_code_for_token(auth_code)
    
    def _exchange_code_for_token(self, authorization_code: str) -> Optional[str]:
        """Tauscht Auth Code gegen Access Token"""
        token_url = "https://www.linkedin.com/oauth/v2/accessToken"
        token_data = {
            "grant_type": "authorization_code",
            "code": authorization_code,
            "redirect_uri": self.redirect_uri,
            "client_id": self.client_id,
            "client_secret": self.client_secret
        }
        
        try:
            response = requests.post(token_url, data=token_data, timeout=10)
            if response.status_code == 200:
                token_info = response.json()
                access_token = token_info.get('access_token')
                print(f"✅ Access Token erhalten")
                return access_token
            else:
                print(f"❌ Token-Fehler: {response.status_code} - {response.text}")
                return None
        except Exception as e:
            print(f"❌ Token-Austausch Fehler: {str(e)}")
            return None
    
    def _get_organization_id(self, access_token: str) -> Optional[str]:
        """Holt Organization ID über LinkedIn API"""
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
            "X-Restli-Protocol-Version": "2.0.0"
        }
        
        try:
            print(f"\n🏢 Schritt 2: Organization ID für '{self.company_name}' suchen...")
            
            # Verwende Administrative Organizations API
            endpoint = "https://api.linkedin.com/v2/organizationalEntityAcls"
            params = {"q": "roleAssignee"}
            
            response = requests.get(endpoint, headers=headers, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if 'elements' in data and len(data['elements']) > 0:
                    for element in data['elements']:
                        org_urn = element.get('organizationalTarget', '')
                        if org_urn.startswith('urn:li:organization:'):
                            org_id = org_urn.split(':')[-1]
                            print(f"✅ Organization ID gefunden: {org_id}")
                            return org_id
                
                print("⚠️  Keine Organisationen in Ihrem Administrator-Zugang gefunden")
                return None
            else:
                print(f"❌ API-Fehler: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"❌ Organization ID Fehler: {str(e)}")
            return None
    
    def is_authenticated(self) -> bool:
        """Prüft ob bereits authentifiziert"""
        return self._access_token is not None and self._organization_id is not None


# Globale Instanz für das Projekt
linkedin_auth = LinkedInDynamicAuth()


def get_linkedin_credentials() -> Tuple[Optional[str], Optional[str]]:
    """
    Öffentliche Funktion zum Abrufen der LinkedIn Credentials
    Wird von anderen Modulen verwendet
    
    Returns:
        Tuple[access_token, organization_id]
    """
    return linkedin_auth.get_credentials()


def check_linkedin_setup() -> bool:
    """
    Prüft LinkedIn Setup ohne interaktive Authentifizierung
    
    Returns:
        bool: True wenn Setup vollständig ist
    """
    client_id = os.getenv("LINKEDIN_CLIENT_ID")
    client_secret = os.getenv("LINKEDIN_CLIENT_SECRET")
    
    if not client_id or not client_secret:
        print("\n⚠️  LinkedIn API Setup unvollständig:")
        print("   Fehlende Werte in .env:")
        print(f"   LINKEDIN_CLIENT_ID: {'✅' if client_id else '❌ Fehlt'}")
        print(f"   LINKEDIN_CLIENT_SECRET: {'✅' if client_secret else '❌ Fehlt'}")
        print("\n📋 Nächste Schritte:")
        print("1. LinkedIn App unter https://www.linkedin.com/developers/ erstellen")
        print("2. Client ID und Secret in .env eintragen")
        return False
    
    print("✅ LinkedIn API Client Credentials verfügbar")
    print("   (Access Token wird bei Bedarf automatisch geholt)")
    return True


if __name__ == "__main__":
    # Test der dynamischen Authentifizierung
    print("🧪 Test: Dynamische LinkedIn Authentifizierung")
    
    if check_linkedin_setup():
        access_token, org_id = get_linkedin_credentials()
        if access_token and org_id:
            print(f"\n🎉 Test erfolgreich!")
            print(f"   Access Token: {access_token[:20]}...")
            print(f"   Organization ID: {org_id}")
        else:
            print("\n❌ Test fehlgeschlagen")
    else:
        print("\n❌ Setup unvollständig")