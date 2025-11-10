"""
LinkedIn API Client für das Posting von LinkedIn-Posts
"""
import requests
from typing import Dict, Optional
import logging
from config import (
    LINKEDIN_ACCESS_TOKEN,
    LINKEDIN_ORGANIZATION_ID,
    LINKEDIN_COMPANY_NAME
)
from persistent_linkedin_auth import get_linkedin_credentials

logger = logging.getLogger(__name__)

class LinkedInClient:
    """Client für die Integration mit LinkedIn API"""
    
    def __init__(self):
        # Versuche zuerst statische Konfiguration
        self.access_token = LINKEDIN_ACCESS_TOKEN
        self.organization_id = LINKEDIN_ORGANIZATION_ID
        self.company_name = LINKEDIN_COMPANY_NAME or "Invory"
        self.base_url = "https://api.linkedin.com/v2"
        
        # Falls keine statischen Credentials, verwende persistente Token-Verwaltung
        if not self.access_token:
            logger.info("🔑 Statische LinkedIn Credentials fehlen - verwende persistente Token-Verwaltung")
            try:
                persistent_token, persistent_org_id = get_linkedin_credentials()
                if persistent_token:
                    self.access_token = persistent_token
                    if persistent_org_id:
                        self.organization_id = persistent_org_id
                    logger.info("✅ Persistente LinkedIn Authentifizierung erfolgreich")
                else:
                    logger.warning("❌ Persistente LinkedIn Authentifizierung fehlgeschlagen")
            except Exception as e:
                logger.error(f"❌ Fehler bei persistenter Authentifizierung: {str(e)}")
        
        # Setze Headers
        self.headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json",
            "X-Restli-Protocol-Version": "2.0.0"
        } if self.access_token else {}
    
    def create_post(self, text: str, visibility: str = "PUBLIC") -> Optional[Dict]:
        """
        Erstellt einen LinkedIn-Post (persönlich mit Standard-Scopes)
        
        Args:
            text: Post-Text
            visibility: Sichtbarkeit (PUBLIC, CONNECTIONS, LOGGED_IN_MEMBERS)
            
        Returns:
            dict: Antwort von LinkedIn API oder None bei Fehler
        """
        if not self.access_token:
            print("❌ Kein LinkedIn Access Token verfügbar")
            return None
            
        # Verwende persönlichen Post mit Standard-Scopes
        return self._create_personal_post(text, visibility)
    
    def _create_personal_post(self, text: str, visibility: str = "PUBLIC") -> Optional[Dict]:
        """Erstellt einen persönlichen LinkedIn-Post"""
        try:
            # Get person URN first
            person_urn = self._get_person_urn()
            if not person_urn:
                print("Fehler: Konnte Person URN nicht ermitteln")
                return None
            
            endpoint = f"{self.base_url}/ugcPosts"
            
            payload = {
                "author": person_urn,
                "lifecycleState": "PUBLISHED",
                "specificContent": {
                    "com.linkedin.ugc.ShareContent": {
                        "shareCommentary": {
                            "text": text
                        },
                        "shareMediaCategory": "NONE"
                    }
                },
                "visibility": {
                    "com.linkedin.ugc.MemberNetworkVisibility": visibility
                }
            }
            
            response = requests.post(
                endpoint,
                headers=self.headers,
                json=payload,
                timeout=10
            )
            
            if response.status_code in [200, 201]:
                print("✅ Persönlicher LinkedIn-Post erfolgreich erstellt")
                return response.json()
            else:
                print(f"❌ Fehler beim persönlichen Post: {response.status_code}")
                print(f"Response: {response.text}")
                return None
        except Exception as e:
            print(f"❌ Fehler bei LinkedIn persönlichem Post: {str(e)}")
            return None
    
    def _get_person_urn(self) -> Optional[str]:
        """Holt die Person URN für persönliche Posts mit korrekter LinkedIn ID"""
        try:
            # Verwende OpenID userinfo endpoint - das funktioniert mit Standard-Scopes
            userinfo_endpoint = "https://api.linkedin.com/v2/userinfo"
            response = requests.get(userinfo_endpoint, headers=self.headers, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                # OpenID userinfo gibt uns die 'sub' (subject) ID
                person_id = data.get('sub')
                if person_id:
                    print(f"✅ Person ID gefunden: {person_id}")
                    return f"urn:li:person:{person_id}"
            
            print(f"❌ Userinfo Fehler: {response.status_code} - {response.text}")
            return None
            
        except Exception as e:
            print(f"❌ Fehler bei Person URN Abruf: {str(e)}")
            return None

    def _create_organization_post(self, text: str, visibility: str = "PUBLIC") -> Optional[Dict]:
        """
        Erstellt einen Organisations-Post (benötigt spezielle LinkedIn App-Berechtigung)
        """
        try:
            if not self.organization_id:
                # Versuche Organization ID automatisch zu ermitteln
                org_id = self._get_organization_id()
                if org_id:
                    self.organization_id = org_id
                else:
                    print("❌ Organization ID nicht verfügbar und konnte nicht ermittelt werden")
                    return None
            
            endpoint = f"{self.base_url}/ugcPosts"
            
            payload = {
                "author": f"urn:li:organization:{self.organization_id}",
                "lifecycleState": "PUBLISHED",
                "specificContent": {
                    "com.linkedin.ugc.ShareContent": {
                        "shareCommentary": {
                            "text": text
                        },
                        "shareMediaCategory": "NONE"
                    }
                },
                "visibility": {
                    "com.linkedin.ugc.MemberNetworkVisibility": visibility
                }
            }
            
            response = requests.post(
                endpoint,
                headers=self.headers,
                json=payload,
                timeout=10
            )
            
            if response.status_code in [200, 201]:
                print("✅ LinkedIn Organisations-Post erfolgreich erstellt")
                return response.json()
            else:
                print(f"❌ Fehler beim Organisations-Post: {response.status_code}")
                print(f"Response: {response.text}")
                return None
        except Exception as e:
            print(f"❌ Fehler bei LinkedIn Organisations-Post: {str(e)}")
            return None

    def schedule_post(self, text: str, scheduled_time: str) -> Optional[Dict]:
        """
        Plant einen LinkedIn-Post für später
        
        Args:
            text: Post-Text
            scheduled_time: Geplante Zeit (ISO 8601 Format)
            
        Returns:
            dict: Antwort von LinkedIn API
        """
        try:
            if not self.access_token or not self.organization_id:
                print("LinkedIn API Credentials fehlen. Post kann nicht geplant werden.")
                return None
            
            endpoint = f"{self.base_url}/ugcPosts"
            
            payload = {
                "author": f"urn:li:organization:{self.organization_id}",
                "lifecycleState": "PUBLISHED",
                "specificContent": {
                    "com.linkedin.ugc.ShareContent": {
                        "shareCommentary": {
                            "text": text
                        },
                        "shareMediaCategory": "NONE"
                    }
                },
                "visibility": {
                    "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
                },
                "lifecycleState": "DRAFT",
                "publishedAt": scheduled_time
            }
            
            response = requests.post(
                endpoint,
                headers=self.headers,
                json=payload,
                timeout=10
            )
            
            if response.status_code in [200, 201]:
                return response.json()
            else:
                print(f"Fehler beim Scheduling: {response.status_code}")
                print(f"Response: {response.text}")
                return None
                
        except Exception as e:
            print(f"Fehler bei LinkedIn API-Anfrage: {str(e)}")
            return None

    def _get_organization_id(self) -> Optional[str]:
        """
        Ruft die Organization ID über die LinkedIn API ab, basierend auf dem Unternehmensnamen
        
        Returns:
            str: Organization ID oder None
        """
        try:
            endpoint = f"{self.base_url}/organizationAcls"
            params = {
                "q": "roleAssignee",
                "role": "ADMINISTRATOR",
                "projection": "(elements*(organization~(id,localizedName)))"
            }
            
            response = requests.get(
                endpoint,
                headers=self.headers,
                params=params,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                organizations = data.get('elements', [])
                
                for org_data in organizations:
                    org_info = org_data.get('organization~', {})
                    org_name = org_info.get('localizedName', '')
                    
                    # Prüfe auf den konfigurierten Unternehmensnamen
                    if self.company_name.lower() in org_name.lower():
                        org_id = org_info.get('id')
                        if org_id:
                            print(f"✅ Organization ID gefunden: {org_id} für {org_name}")
                            return str(org_id)
                
                # Falls keine Übereinstimmung gefunden wurde, nimm die erste verfügbare
                if organizations:
                    first_org = organizations[0].get('organization~', {})
                    org_id = first_org.get('id')
                    org_name = first_org.get('localizedName', 'Unbekannt')
                    if org_id:
                        print(f"⚠️ Keine exakte Übereinstimmung für '{self.company_name}' gefunden.")
                        print(f"Verwende erste verfügbare Organisation: {org_id} ({org_name})")
                        return str(org_id)
                        
                print("❌ Keine Organisationen gefunden, zu denen Sie Administrator sind")
                return None
            else:
                print(f"❌ Fehler beim Abrufen der Organizations: {response.status_code}")
                print(f"Response: {response.text}")
                return None
                
        except Exception as e:
            print(f"❌ Fehler bei Organization ID Abruf: {str(e)}")
            return None
    
    def get_profile_info(self) -> Optional[Dict]:
        """
        Ruft Profil-Informationen des authentifizierten Users ab
        
        Returns:
            dict: Profil-Informationen oder None
        """
        try:
            endpoint = f"{self.base_url}/people/~"
            
            response = requests.get(
                endpoint,
                headers=self.headers,
                timeout=10
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                print(f"Fehler beim Abrufen der Profil-Info: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"Fehler bei Profil-Info Abruf: {str(e)}")
            return None

    def test_connection(self) -> bool:
        """
        Testet die Verbindung zur LinkedIn API
        
        Returns:
            bool: True wenn Verbindung erfolgreich
        """
        try:
            profile_info = self.get_profile_info()
            if profile_info:
                name = profile_info.get('localizedFirstName', '') + " " + profile_info.get('localizedLastName', '')
                print(f"✅ LinkedIn API Verbindung erfolgreich - Angemeldet als: {name.strip()}")
                return True
            else:
                print("❌ LinkedIn API Verbindung fehlgeschlagen")
                return False
        except Exception as e:
            print(f"❌ Fehler beim Testen der LinkedIn Verbindung: {str(e)}")
            return False

    def get_recent_posts(self, count: int = 5) -> Optional[Dict]:
        """
        Ruft die letzten Posts des Users ab
        
        Args:
            count: Anzahl der Posts (max 50)
            
        Returns:
            dict: Posts oder None
        """
        try:
            endpoint = f"{self.base_url}/ugcPosts"
            params = {
                "q": "authors",
                "authors": f"urn:li:person:{self._get_person_id()}",
                "count": min(count, 50)
            }
            
            response = requests.get(
                endpoint,
                headers=self.headers,
                params=params,
                timeout=10
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                print(f"Fehler beim Abrufen der Posts: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"Fehler beim Posts-Abruf: {str(e)}")
            return None
    
    def _get_person_id(self) -> Optional[str]:
        """Hilfsmethode zum Abrufen der Person ID"""
        try:
            profile = self.get_profile_info()
            if profile:
                return profile.get('id')
            return None
        except Exception as e:
            print(f"Fehler beim Person ID Abruf: {str(e)}")
            return None