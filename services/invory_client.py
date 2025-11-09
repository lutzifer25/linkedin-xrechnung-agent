"""
Invory.de Web-Client für XRechnung-Daten (Web-Scraping)
"""
import requests
from bs4 import BeautifulSoup
from typing import Dict, Optional, List
from config import INVORY_URL
import logging
import re

logger = logging.getLogger(__name__)

class InvoryClient:
    """Client für die Web-Recherche auf invory.de"""
    
    def __init__(self):
        self.base_url = INVORY_URL
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
    
    def _fetch_page(self, url: str) -> Optional[BeautifulSoup]:
        """
        Holt eine Webseite und gibt BeautifulSoup-Objekt zurück
        
        Args:
            url: URL der Webseite
            
        Returns:
            BeautifulSoup-Objekt oder None bei Fehler
        """
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            return BeautifulSoup(response.content, 'html.parser')
        except Exception as e:
            logger.error(f"Fehler beim Abrufen der Seite {url}: {str(e)}")
            return None
    
    def _extract_text_content(self, soup: BeautifulSoup) -> str:
        """
        Extrahiert Textinhalt aus einer Webseite
        
        Args:
            soup: BeautifulSoup-Objekt
            
        Returns:
            str: Extrahieter Text
        """
        # Entferne Script- und Style-Tags
        for script in soup(["script", "style", "nav", "footer", "header"]):
            script.decompose()
        
        # Extrahiere Text
        text = soup.get_text()
        # Bereinige Whitespace
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = ' '.join(chunk for chunk in chunks if chunk)
        
        return text
    
    def get_xrechnung_info(self) -> Optional[Dict]:
        """
        Holt XRechnung-Informationen von invory.de durch Web-Scraping
        
        Returns:
            dict: Informationen zu XRechnung und invory.de
        """
        try:
            soup = self._fetch_page(self.base_url)
            if not soup:
                return self.get_mock_data()
            
            # Extrahiere Textinhalt
            text_content = self._extract_text_content(soup)
            
            # Suche nach relevanten Informationen
            title = soup.find('title')
            title_text = title.get_text() if title else "Invory.de - XRechnung Lösungen"
            
            # Suche nach Features/Services
            features = []
            # Versuche, Features aus der Seite zu extrahieren
            feature_elements = soup.find_all(['h2', 'h3', 'li', 'p'], 
                                            string=re.compile(r'(feature|funktion|service|leistung|lösung)', re.I))
            for elem in feature_elements[:10]:
                text = elem.get_text().strip()
                if text and len(text) < 200:
                    features.append(text)
            
            # Extrahiere relevante Abschnitte
            relevant_sections = []
            sections = soup.find_all(['section', 'div'], class_=re.compile(r'(feature|service|about|solution)', re.I))
            for section in sections[:5]:
                text = section.get_text().strip()[:500]
                if text:
                    relevant_sections.append(text)
            
            return {
                "url": self.base_url,
                "title": title_text,
                "content_preview": text_content[:1000] if text_content else "",
                "features": features[:5] if features else [
                    "XRechnung-Erstellung",
                    "Compliance-Prüfung",
                    "Automatisierung",
                    "ERP-Integration"
                ],
                "relevant_sections": relevant_sections[:3],
                "keywords": self._extract_keywords(text_content)
            }
        except Exception as e:
            logger.error(f"Fehler beim Scraping von invory.de: {str(e)}")
            return self.get_mock_data()
    
    def _extract_keywords(self, text: str) -> List[str]:
        """
        Extrahiert relevante Keywords aus dem Text
        
        Args:
            text: Textinhalt
            
        Returns:
            list: Liste von Keywords
        """
        keywords = []
        xrechnung_keywords = [
            "XRechnung", "E-Invoicing", "digitale Rechnung", "elektronische Rechnung",
            "Compliance", "Automatisierung", "ERP", "Integration", "ZUGFeRD"
        ]
        
        text_lower = text.lower()
        for keyword in xrechnung_keywords:
            if keyword.lower() in text_lower:
                keywords.append(keyword)
        
        return keywords[:5]
    
    def get_xrechnung_insights(self) -> Optional[Dict]:
        """
        Holt Insights zu XRechnung von invory.de
        
        Returns:
            dict: Insights und Informationen
        """
        info = self.get_xrechnung_info()
        if not info:
            return self.get_mock_data()
        
        return {
            "invory_features": info.get("features", []),
            "invory_url": info.get("url", self.base_url),
            "invory_title": info.get("title", "Invory.de"),
            "invory_keywords": info.get("keywords", []),
            "invory_content": info.get("content_preview", "")
        }
    
    def get_mock_data(self) -> Dict:
        """
        Gibt Mock-Daten zurück, wenn Web-Scraping fehlschlägt
        
        Returns:
            dict: Mock-Daten für XRechnung
        """
        return {
            "invory_features": [
                "Automatische XRechnung-Erstellung",
                "Compliance-Prüfung",
                "ERP-Integration",
                "Automatische Validierung",
                "Digitale Rechnungsstellung"
            ],
            "invory_url": self.base_url,
            "invory_title": "Invory.de - XRechnung Lösungen",
            "invory_keywords": ["XRechnung", "E-Invoicing", "Compliance", "Automatisierung"],
            "invory_content": "Invory.de bietet Lösungen für die digitale Rechnungsstellung mit XRechnung-Standard."
        }
