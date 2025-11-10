"""
LinkedIn API Client für das Posting von LinkedIn-Posts mit Bildern
"""
import requests
import os
import tempfile
from typing import Dict, Optional, Union
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
    
    def create_post(self, text: str, visibility: str = "PUBLIC", image_url: str = None, image_path: str = None) -> Optional[Dict]:
        """
        Erstellt einen LinkedIn-Post (persönlich mit Standard-Scopes) optional mit Bild
        
        Args:
            text: Post-Text
            visibility: Sichtbarkeit (PUBLIC, CONNECTIONS, LOGGED_IN_MEMBERS)
            image_url: URL eines Bildes zum Download und Upload
            image_path: Lokaler Pfad zu einem Bild
            
        Returns:
            dict: Antwort von LinkedIn API oder None bei Fehler
        """
        if not self.access_token:
            print("❌ Kein LinkedIn Access Token verfügbar")
            return None
            
        # Verwende persönlichen Post mit Standard-Scopes
        return self._create_personal_post(text, visibility, image_url, image_path)
    
    def _create_personal_post(self, text: str, visibility: str = "PUBLIC", image_url: str = None, image_path: str = None) -> Optional[Dict]:
        """Erstellt einen persönlichen LinkedIn-Post optional mit Bild"""
        try:
            # Get person URN first
            person_urn = self._get_person_urn()
            if not person_urn:
                print("Fehler: Konnte Person URN nicht ermitteln")
                return None
            
            endpoint = f"{self.base_url}/ugcPosts"
            
            # Bearbeite Bild falls vorhanden
            media_asset_urn = None
            if image_url or image_path:
                media_asset_urn = self._upload_image(image_url, image_path, person_urn)
            
            # Basis-Payload
            if media_asset_urn:
                # Post mit Bild
                payload = {
                    "author": person_urn,
                    "lifecycleState": "PUBLISHED",
                    "specificContent": {
                        "com.linkedin.ugc.ShareContent": {
                            "shareCommentary": {
                                "text": text
                            },
                            "shareMediaCategory": "IMAGE",
                            "media": [
                                {
                                    "status": "READY",
                                    "description": {
                                        "text": "XRechnung Illustration"
                                    },
                                    "media": media_asset_urn
                                }
                            ]
                        }
                    },
                    "visibility": {
                        "com.linkedin.ugc.MemberNetworkVisibility": visibility
                    }
                }
            else:
                # Post ohne Bild
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
    
    def _upload_image(self, image_url: str = None, image_path: str = None, person_urn: str = None) -> Optional[str]:
        """
        Lädt ein Bild zu LinkedIn hoch und gibt die Asset URN zurück
        
        Args:
            image_url: URL eines Bildes zum Download
            image_path: Lokaler Pfad zu einem Bild  
            person_urn: Person URN für den Upload
            
        Returns:
            str: Asset URN für das hochgeladene Bild oder None
        """
        try:
            # Besorge Bilddaten
            image_data = None
            filename = "xrechnung_image.png"
            
            if image_url:
                print(f"📥 Lade Bild von URL herunter: {image_url[:50]}...")
                response = requests.get(image_url, timeout=30)
                response.raise_for_status()
                image_data = response.content
                # Versuche Dateiname aus URL zu extrahieren
                if '.' in image_url.split('/')[-1]:
                    filename = image_url.split('/')[-1].split('?')[0]
                    
            elif image_path and os.path.exists(image_path):
                print(f"📁 Lade Bild von lokalem Pfad: {image_path}")
                with open(image_path, 'rb') as f:
                    image_data = f.read()
                filename = os.path.basename(image_path)
            
            if not image_data:
                print("❌ Keine gültigen Bilddaten gefunden")
                return None
                
            # Schritt 1: Registriere Upload
            register_response = self._register_image_upload(person_urn, filename)
            if not register_response:
                print("❌ Image Upload Registrierung fehlgeschlagen")
                return None
                
            upload_url = register_response.get('value', {}).get('uploadMechanism', {}).get('com.linkedin.digitalmedia.uploading.MediaUploadHttpRequest', {}).get('uploadUrl')
            asset_urn = register_response.get('value', {}).get('asset')
            
            if not upload_url or not asset_urn:
                print("❌ Upload URL oder Asset URN fehlt")
                return None
            
            # Schritt 2: Lade Bild hoch
            print(f"📤 Lade Bild zu LinkedIn hoch...")
            upload_headers = {
                "Authorization": f"Bearer {self.access_token}"
            }
            
            upload_response = requests.put(
                upload_url,
                headers=upload_headers,
                data=image_data,
                timeout=60
            )
            
            if upload_response.status_code in [200, 201]:
                print(f"✅ Bild erfolgreich hochgeladen: {asset_urn}")
                return asset_urn
            else:
                print(f"❌ Bild-Upload fehlgeschlagen: {upload_response.status_code}")
                return None
                
        except Exception as e:
            print(f"❌ Fehler beim Bild-Upload: {str(e)}")
            return None
    
    def _register_image_upload(self, person_urn: str, filename: str) -> Optional[Dict]:
        """Registriert einen Bild-Upload bei LinkedIn"""
        try:
            endpoint = f"{self.base_url}/assets?action=registerUpload"
            
            payload = {
                "registerUploadRequest": {
                    "recipes": ["urn:li:digitalmediaRecipe:feedshare-image"],
                    "owner": person_urn,
                    "serviceRelationships": [
                        {
                            "relationshipType": "OWNER",
                            "identifier": "urn:li:userGeneratedContent"
                        }
                    ]
                }
            }
            
            response = requests.post(
                endpoint,
                headers=self.headers,
                json=payload,
                timeout=30
            )
            
            if response.status_code in [200, 201]:
                print("✅ Bild-Upload registriert")
                return response.json()
            else:
                print(f"❌ Upload-Registrierung fehlgeschlagen: {response.status_code}")
                print(f"Response: {response.text}")
                return None
                
        except Exception as e:
            print(f"❌ Fehler bei Upload-Registrierung: {str(e)}")
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