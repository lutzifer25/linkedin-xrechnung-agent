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
from dynamic_linkedin_auth import get_linkedin_credentials

logger = logging.getLogger(__name__)

class LinkedInClient:
    """Client für die Integration mit LinkedIn API"""
    
    def __init__(self):
        # Versuche zuerst statische Konfiguration
        self.access_token = LINKEDIN_ACCESS_TOKEN
        self.organization_id = LINKEDIN_ORGANIZATION_ID
        self.company_name = LINKEDIN_COMPANY_NAME or "Invory"
        self.base_url = "https://api.linkedin.com/v2"
        
        # Falls keine statischen Credentials, verwende dynamische Authentifizierung
        if not self.access_token or not self.organization_id:
            logger.info("🔑 Statische LinkedIn Credentials fehlen - verwende dynamische Authentifizierung")
            try:
                dynamic_token, dynamic_org_id = get_linkedin_credentials()
                if dynamic_token and dynamic_org_id:
                    self.access_token = dynamic_token
                    self.organization_id = dynamic_org_id
                    logger.info("✅ Dynamische LinkedIn Authentifizierung erfolgreich")
                else:
                    logger.warning("❌ Dynamische LinkedIn Authentifizierung fehlgeschlagen")
            except Exception as e:
                logger.error(f"❌ Fehler bei dynamischer Authentifizierung: {str(e)}")
        
        # Setze Headers
        self.headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json",
            "X-Restli-Protocol-Version": "2.0.0"
        } if self.access_token else {}
    
    def create_post(self, text: str, visibility: str = "PUBLIC") -> Optional[Dict]:
        """
        Erstellt einen LinkedIn-Post (automatisch persönlich oder Organisation je nach verfügbaren Scopes)"""
        
        Args:
            text: Post-Text
            visibility: Sichtbarkeit des Posts (PUBLIC, CONNECTIONS)
            
        Returns:
            dict: Antwort von LinkedIn API
        """
        try:
            if not self.access_token or not self.organization_id:
                print("LinkedIn API Credentials fehlen. Post wird nicht veröffentlicht.")
                return None
            
            # Entscheide zwischen persönlichem und Organisations-Post
            if self.organization_id:
                # Organisations-Post (benötigt w_organization_social scope)
                return self._create_organization_post(text, visibility)
            else:
                # Persönlicher Post (mit w_member_social scope)
                return self._create_personal_post(text, visibility)
                
    def _create_organization_post(self, text: str, visibility: str = "PUBLIC") -> Optional[Dict]:
        """Erstellt einen Organisations-Post"""
        try:
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
                return response.json()
            else:
                print(f"Fehler beim Posten: {response.status_code}")
                print(f"Response: {response.text}")
                return None
        except Exception as e:
            print(f"Fehler bei LinkedIn Organisations-Post: {str(e)}")
            return None
            
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
                return response.json()
            else:
                print(f"Fehler beim persönlichen Post: {response.status_code}")
                print(f"Response: {response.text}")
                return None
        except Exception as e:
            print(f"Fehler bei LinkedIn persönlichem Post: {str(e)}")
            return None
    
    def _get_person_urn(self) -> Optional[str]:
        """Holt die Person URN für persönliche Posts"""
        try:
            endpoint = f"{self.base_url}/people/~"
            response = requests.get(endpoint, headers=self.headers, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                person_id = data.get('id')
                if person_id:
                    return f"urn:li:person:{person_id}"
            
            print(f"Fehler beim Abrufen der Person URN: {response.status_code}")
            return None
        except Exception as e:
            print(f"Fehler bei Person URN Abruf: {str(e)}")
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
                print(f"Fehler beim Planen des Posts: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"Fehler bei LinkedIn API-Anfrage: {str(e)}")
            return None
    
    def _get_organization_id_by_name(self, company_name: str) -> Optional[str]:
        """
        Ruft die Organization ID über die LinkedIn API ab, basierend auf dem Unternehmensnamen
        
        Args:
            company_name: Name des Unternehmens (z.B. "Invory")
            
        Returns:
            str: Organization ID oder None bei Fehler
        """
        try:
            # Methode 1: Verwende die Organization Search API
            # Hinweis: Dies erfordert spezielle Berechtigungen
            # Alternativ: Verwende die Organizations API mit dem Namen
            
            # Methode 2: Verwende die Organization Brand Pages API
            # Diese Methode sucht nach Organisationen basierend auf dem Namen
            endpoint = f"{self.base_url}/organizationBrands"
            params = {
                "q": "brandName",
                "brandName": company_name
            }
            
            response = requests.get(
                endpoint,
                headers=self.headers,
                params=params,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                # Die Antwort enthält eine Liste von Organisationen
                if 'elements' in data and len(data['elements']) > 0:
                    # Extrahiere die ID aus dem URN (urn:li:organization:123456789)
                    org_urn = data['elements'][0].get('organization', '')
                    if org_urn.startswith('urn:li:organization:'):
                        org_id = org_urn.split(':')[-1]
                        logger.info(f"Organization ID gefunden: {org_id} für Unternehmen: {company_name}")
                        return org_id
            
            # Methode 3: Verwende die Organizations API mit erweiterten Berechtigungen
            # Versuche, die Organisation über die Organizations API zu finden
            logger.warning(f"Organization ID konnte nicht über API gefunden werden. Versuche alternative Methode...")
            
            # Alternative: Verwende die Organization Search API (falls verfügbar)
            # Diese Methode erfordert erweiterte Berechtigungen
            search_endpoint = f"{self.base_url}/organizationSearch"
            search_params = {
                "keywords": company_name,
                "start": 0,
                "count": 1
            }
            
            search_response = requests.get(
                search_endpoint,
                headers=self.headers,
                params=search_params,
                timeout=10
            )
            
            if search_response.status_code == 200:
                search_data = search_response.json()
                if 'elements' in search_data and len(search_data['elements']) > 0:
                    org_urn = search_data['elements'][0].get('id', '')
                    if org_urn.startswith('urn:li:organization:'):
                        org_id = org_urn.split(':')[-1]
                        logger.info(f"Organization ID gefunden über Search API: {org_id}")
                        return org_id
            
            logger.warning(f"Organization ID konnte nicht automatisch gefunden werden für: {company_name}")
            logger.warning("Bitte stellen Sie sicher, dass die Organization ID in der .env-Datei gesetzt ist")
            return None
            
        except Exception as e:
            logger.error(f"Fehler beim Abrufen der Organization ID: {str(e)}")
            logger.warning("Bitte stellen Sie sicher, dass die Organization ID in der .env-Datei gesetzt ist")
            return None
    
    def _get_organization_id_from_profile(self) -> Optional[str]:
        """
        Hauptmethode: Ruft die Organization ID über das Profil des angemeldeten Benutzers ab
        Dies funktioniert, wenn der Benutzer Administrator der Seite ist
        Dies ist die zuverlässigste Methode, da sie die Organizations des authentifizierten Benutzers verwendet
        
        Returns:
            str: Organization ID oder None bei Fehler
        """
        try:
            # Hole die Organizations des angemeldeten Benutzers, bei denen er Administrator ist
            endpoint = f"{self.base_url}/organizationAcls"
            params = {
                "q": "roleAssignee",
                "role": "ADMINISTRATOR",
                "state": "APPROVED"
            }
            
            response = requests.get(
                endpoint,
                headers=self.headers,
                params=params,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                if 'elements' in data and len(data['elements']) > 0:
                    # Wenn nur eine Organisation gefunden wurde, verwende diese
                    if len(data['elements']) == 1:
                        org_urn = data['elements'][0].get('organization', '')
                        if org_urn.startswith('urn:li:organization:'):
                            org_id = org_urn.split(':')[-1]
                            logger.info(f"Organization ID gefunden über Profil (einzige Organisation): {org_id}")
                            return org_id
                    
                    # Wenn mehrere Organisationen gefunden wurden, suche nach dem passenden Namen
                    for element in data['elements']:
                        org_urn = element.get('organization', '')
                        if org_urn.startswith('urn:li:organization:'):
                            org_id = org_urn.split(':')[-1]
                            # Überprüfe, ob dies die richtige Organisation ist
                            org_details = self._get_organization_details(org_id)
                            if org_details:
                                org_name = org_details.get('name', '').lower()
                                if self.company_name.lower() in org_name or org_name in self.company_name.lower():
                                    logger.info(f"Organization ID gefunden über Profil: {org_id} (Name: {org_details.get('name')})")
                                    return org_id
                    
                    # Falls keine passende Organisation gefunden wurde, verwende die erste
                    # (falls der Benutzer nur Administrator einer Organisation ist)
                    org_urn = data['elements'][0].get('organization', '')
                    if org_urn.startswith('urn:li:organization:'):
                        org_id = org_urn.split(':')[-1]
                        logger.warning(f"Mehrere Organisationen gefunden. Verwende erste Organisation: {org_id}")
                        return org_id
            elif response.status_code == 403:
                logger.warning("Keine Berechtigung für organizationAcls API. Versuche alternative Methode...")
            else:
                logger.warning(f"API-Anfrage fehlgeschlagen: {response.status_code} - {response.text}")
            
            return None
        except Exception as e:
            logger.error(f"Fehler beim Abrufen der Organization ID vom Profil: {str(e)}")
            return None
    
    def _get_organization_details(self, org_id: str) -> Optional[Dict]:
        """
        Ruft Details einer Organisation ab
        
        Args:
            org_id: Organization ID
            
        Returns:
            dict: Organisationsdetails oder None bei Fehler
        """
        try:
            endpoint = f"{self.base_url}/organizations/{org_id}"
            params = {
                "projection": "(id,name,vanityName)"
            }
            
            response = requests.get(
                endpoint,
                headers=self.headers,
                params=params,
                timeout=10
            )
            
            if response.status_code == 200:
                return response.json()
            return None
        except Exception as e:
            logger.error(f"Fehler beim Abrufen der Organisationsdetails: {str(e)}")
            return None
    
    def verify_connection(self) -> bool:
        """
        Überprüft die Verbindung zur LinkedIn API
        
        Returns:
            bool: True wenn Verbindung erfolgreich
        """
        try:
            if not self.access_token:
                logger.error("LinkedIn Access Token fehlt")
                return False
            
            if not self.organization_id:
                logger.error("LinkedIn Organization ID fehlt")
                # Versuche, die Organization ID nochmals abzurufen
                self.organization_id = self._get_organization_id_by_name(self.company_name)
                if not self.organization_id:
                    # Versuche alternative Methode
                    self.organization_id = self._get_organization_id_from_profile()
            
            if not self.organization_id:
                logger.error("Organization ID konnte nicht ermittelt werden")
                return False
            
            endpoint = f"{self.base_url}/organizations/{self.organization_id}"
            response = requests.get(endpoint, headers=self.headers, timeout=10)
            
            if response.status_code == 200:
                logger.info("LinkedIn API Verbindung erfolgreich")
                return True
            else:
                logger.error(f"LinkedIn API Verbindung fehlgeschlagen: {response.status_code}")
                return False
        except Exception as e:
            logger.error(f"Fehler bei Verbindungsprüfung: {str(e)}")
            return False

