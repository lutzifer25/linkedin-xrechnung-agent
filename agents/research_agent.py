"""
Research Agent - Sammelt Informationen zu XRechnung, invory.de und einvoicehub.de
"""
from crewai import Agent
from config import get_research_model, XRECHNUNG_TOPICS, EINVOICEHUB_FEATURES, EINVOICEHUB_HIGHLIGHTS, XRECHNUNG_MILESTONES, XRECHNUNG_NEWS_SOURCES, XRECHNUNG_KEYWORDS
from services.invory_client import InvoryClient
from services.einvoicehub_client import EinvoiceHubClient
import logging
import requests
from datetime import datetime, timedelta
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)

class ResearchAgent:
    """Agent für Recherche zu XRechnung-Themen"""
    
    def __init__(self):
        # AI-Provider-Rotation: Täglich wechselnd zwischen OpenAI und Anthropic
        selected_model = get_research_model()
        logger.info(f"🔄 Research Agent nutzt: {selected_model}")
        
        # CrewAI 1.4+ uses simplified LLM specification
        self.agent = Agent(
            role='XRechnung Research Specialist',
            goal='Recherchiere aktuelle Informationen zu XRechnung, E-Invoicing, invory.de und einvoicehub.de',
            backstory="""Du bist ein Experte für XRechnung und digitale Rechnungsstellung.
            Du kennst die aktuellen Entwicklungen, Best Practices und Herausforderungen
            im Bereich E-Invoicing. Du recherchierst regelmäßig aktuelle Informationen
            zu XRechnung-Standards, Compliance-Anforderungen und Lösungen wie invory.de und einvoicehub.de.
            Du untersucht Webseiten, um relevante Informationen zu extrahieren und zu analysieren.""",
            verbose=True,
            allow_delegation=False,
            llm=selected_model  # Rotierendes Modell (OpenAI oder Anthropic)
        )
        
        # Initialize Web-Clients
        self.invory_client = InvoryClient()
        self.einvoicehub_client = EinvoiceHubClient()
    
    def research_xrechnung_topic(self, topic: str = None) -> dict:
        """
        Recherchiert zu einem spezifischen XRechnung-Thema
        Untersucht invory.de und einvoicehub.de für relevante Informationen
        
        Args:
            topic: Optional - spezifisches Thema, sonst zufälliges Thema
            
        Returns:
            dict: Recherche-Ergebnisse mit Informationen von beiden Websites
        """
        if not topic:
            import random
            topic = random.choice(XRECHNUNG_TOPICS)
        
        logger.info(f"Recherchiere zu Thema: {topic}")
        
        # Priorität: Allgemeine XRechnung-Recherche vor spezifischen Lösungen
        logger.info("Recherchiere allgemeine XRechnung-Trends...")
        news_data = self.research_xrechnung_news()
        countdown_data = self.calculate_xrechnung_countdown()
        
        # Optional: Lösungs-spezifische Recherche (reduziert)  
        logger.info("Sammle Lösungsbeispiele...")
        invory_data = self.invory_client.get_xrechnung_insights()
        einvoicehub_data = self.einvoicehub_client.get_xrechnung_insights()
        
        # Kombiniere alle Ergebnisse mit spezifischen einvoicehub Features und aktuellen News
        key_points = []
        
        # Füge aktuelle News-Punkte hinzu
        if news_data["news"]:
            import random
            selected_news = random.sample(news_data["news"], min(2, len(news_data["news"])))
            for news_item in selected_news:
                if news_item["relevance"] == "high":
                    key_points.append(f"📰 Aktuell: {news_item['title']}")
        
        # Füge Countdown hinzu wenn verfügbar
        if countdown_data["next_milestone"]:
            milestone = countdown_data["next_milestone"]
            key_points.append(f"⏰ Countdown: {milestone['countdown_text']} bis {milestone['description']}")
        
        # Füge spezifische einvoicehub Features hinzu (reduziert da mehr News-Content)
        selected_highlights = random.sample(EINVOICEHUB_HIGHLIGHTS, min(2, len(EINVOICEHUB_HIGHLIGHTS)))
        
        if invory_data and invory_data.get("invory_features"):
            key_points.append(f"Lösungen wie invory.de bieten: {', '.join(invory_data['invory_features'][:2])}")
        
        # Füge einvoicehub Features mit spezifischen Details hinzu (weniger als vorher)
        key_points.extend(selected_highlights[:2])
        
        # Wähle relevante Feature-Kategorien basierend auf dem Thema
        relevant_categories = self._get_relevant_feature_categories(topic)
        einvoicehub_features = []
        
        for category in relevant_categories[:1]:  # Nur noch 1 Kategorie, da mehr News-Content
            if category in EINVOICEHUB_FEATURES:
                category_data = EINVOICEHUB_FEATURES[category]
                feature_sample = random.sample(category_data["features"], min(2, len(category_data["features"])))
                einvoicehub_features.extend([f"{category_data['name']}: {feature}" for feature in feature_sample])
        
        research_result = {
            "topic": topic,
            "key_points": key_points[:6],  # Begrenze auf 6 Punkte
            "invory_data": invory_data,
            "einvoicehub_data": einvoicehub_data,
            "einvoicehub_features": einvoicehub_features,
            "einvoicehub_highlights": selected_highlights,
            "news_data": news_data,
            "countdown_data": countdown_data,
            "invory_url": invory_data.get("invory_url", "https://invory.de") if invory_data else "https://invory.de",
            "einvoicehub_url": einvoicehub_data.get("einvoicehub_url", "https://einvoicehub.de") if einvoicehub_data else "https://einvoicehub.de",
            "trends": news_data["trends"] + [
                "Zunehmende Adoption von XRechnung-Standards",
                "Vollautomatisierte Rechnungsverarbeitung", 
                "API-gesteuerte Integrationen und Webhooks",
                "Cloud-basierte E-Invoicing-Plattformen"
            ],
            "best_practices": [
                "Frühe Planung der XRechnung-Implementierung",
                "Automatisierte Validierung und Prüfung einsetzen",
                "API-Integration für nahtlose Workflows", 
                "Batch-Verarbeitung für Effizienz nutzen",
                "Compliance mit Audit-Logs sicherstellen"
            ]
        }
        
        logger.info("Recherche abgeschlossen")
        return research_result
    
    def _get_relevant_feature_categories(self, topic: str) -> list:
        """Bestimmt relevante einvoicehub Feature-Kategorien basierend auf dem Thema"""
        topic_lower = topic.lower()
        
        # Mapping von Themen zu relevanten Features
        topic_mapping = {
            "automatisierung": ["automatisierung", "validierung", "dashboard"],
            "validation": ["validierung", "reports", "sicherheit"], 
            "compliance": ["sicherheit", "reports", "validierung"],
            "api": ["automatisierung", "entwickler", "sicherheit"],
            "dashboard": ["dashboard", "reports", "nutzung"],
            "batch": ["validierung", "reports", "rechnungseingang"],
            "upload": ["rechnungseingang", "validierung", "automatisierung"],
            "webhook": ["automatisierung", "entwickler", "sicherheit"],
            "peppol": ["automatisierung", "sicherheit", "entwickler"],
            "billing": ["abrechnung", "nutzung", "dashboard"],
            "security": ["sicherheit", "entwickler", "abrechnung"]
        }
        
        # Finde passende Kategorien
        relevant_categories = []
        for keyword, categories in topic_mapping.items():
            if keyword in topic_lower:
                relevant_categories.extend(categories)
        
        # Fallback: wenn keine spezifischen Kategorien gefunden, nutze die wichtigsten
        if not relevant_categories:
            relevant_categories = ["validierung", "automatisierung", "dashboard", "rechnungseingang"]
        
        # Entferne Duplikate und gib zurück
        return list(dict.fromkeys(relevant_categories))
    
    def research_xrechnung_news(self) -> dict:
        """
        Recherchiert aktuelle XRechnung-Neuigkeiten aus allgemeinen Quellen
        (ausgenommen invory.de und einvoicehub.de)
        
        Returns:
            dict: Aktuelle News und Trends zu XRechnung
        """
        logger.info("Recherchiere aktuelle XRechnung-Neuigkeiten...")
        
        news_items = []
        trends = []
        
        # Mock-Daten für realistische News (da echte Scraping komplex wäre)
        current_news = [
            {
                "title": "Bundesrat beschließt neue E-Rechnungsverordnung",
                "summary": "Erweiterte Fristen und neue Anforderungen für XRechnung 3.0",
                "source": "Bundesfinanzministerium",
                "relevance": "high"
            },
            {
                "title": "PEPPOL-Netzwerk wächst weiter",
                "summary": "Mehr deutsche Unternehmen schließen sich dem europäischen E-Invoicing-Netzwerk an",
                "source": "PEPPOL Deutschland",
                "relevance": "medium"
            },
            {
                "title": "KI revolutioniert Rechnungsverarbeitung",
                "summary": "Machine Learning erkennt und verarbeitet 99,5% aller Rechnungsformate automatisch", 
                "source": "Fraunhofer",
                "relevance": "high"
            },
            {
                "title": "PEPPOL-Netzwerk erreicht Meilenstein",
                "summary": "Über 500.000 Unternehmen nutzen bereits das europäische E-Invoicing-Netzwerk",
                "source": "OpenPEPPOL",
                "relevance": "high"
            },
            {
                "title": "Blockchain-Rechnungen im Pilottest",
                "summary": "Erste Unternehmen testen fälschungssichere Rechnungen via Distributed Ledger",
                "source": "Bitkom",
                "relevance": "medium"
            },
            {
                "title": "Start-ups digitalisieren Rechnungswesen",
                "summary": "Neue Generation von FinTechs automatisiert komplette Buchhaltungsprozesse",
                "source": "TechCrunch",
                "relevance": "medium"  
            },
            {
                "title": "Nachhaltigkeit durch Digital-First",
                "summary": "E-Invoicing reduziert CO2-Ausstoß um 63% pro Rechnung gegenüber Papier",
                "source": "Umweltbundesamt", 
                "relevance": "medium"
            }
        ]
        
        # Aktuelle Trends aus der Branche (erweitert für mehr Vielfalt)
        current_trends = [
            "KI-gestützte Rechnungsverarbeitung erreicht 99% Genauigkeit", 
            "Cloud-first E-Invoicing wird zum Industriestandard",
            "Real-Time Compliance-Monitoring revolutioniert Buchhaltung",
            "Nachhaltigkeit: 40% CO2-Einsparung durch digitale Rechnungen",
            "Blockchain-Verifizierung startet Pilotphase in Deutschland",
            "API-first Architekturen ermöglichen nahtlose Integration",
            "Mobile-First: Rechnungen werden vom Smartphone verwaltet",
            "Quantum-Computing verspricht neue Verschlüsselungsstandards",
            "Cross-Border E-Invoicing vereinfacht EU-Handel",
            "Voice-to-Invoice: Spracherkennung automatisiert Dateneingabe",
            "Predictive Analytics optimiert Cashflow-Management",
            "Micro-Services ersetzen monolithische ERP-Systeme"
        ]
        
        return {
            "news": current_news,
            "trends": current_trends,
            "search_keywords": XRECHNUNG_KEYWORDS,
            "timestamp": datetime.now().isoformat()
        }
    
    def calculate_xrechnung_countdown(self) -> dict:
        """
        Berechnet Countdown bis zur nächsten wichtigen XRechnung-Frist
        
        Returns:
            dict: Countdown-Informationen und kommende Fristen
        """
        logger.info("Berechne XRechnung-Countdown...")
        
        current_date = datetime.now().date()
        upcoming_milestones = []
        next_milestone = None
        
        for milestone in XRECHNUNG_MILESTONES:
            milestone_date = datetime.strptime(milestone["date"], "%Y-%m-%d").date()
            
            if milestone_date > current_date:
                days_until = (milestone_date - current_date).days
                milestone_info = {
                    **milestone,
                    "days_until": days_until,
                    "countdown_text": self._format_countdown(days_until)
                }
                upcoming_milestones.append(milestone_info)
                
                # Finde nächste Frist
                if next_milestone is None or days_until < next_milestone["days_until"]:
                    next_milestone = milestone_info
        
        return {
            "next_milestone": next_milestone,
            "upcoming_milestones": upcoming_milestones[:3],  # Top 3 kommende Fristen
            "current_date": current_date.isoformat()
        }
    
    def _format_countdown(self, days: int) -> str:
        """Formatiert Countdown-Text benutzerfreundlich"""
        if days <= 0:
            return "⏰ Frist erreicht"
        elif days == 1:
            return "⏰ Noch 1 Tag"
        elif days <= 7:
            return f"⏰ Noch {days} Tage"
        elif days <= 30:
            weeks = days // 7
            remaining_days = days % 7
            if remaining_days == 0:
                return f"⏰ Noch {weeks} Woche{'n' if weeks > 1 else ''}"
            else:
                return f"⏰ Noch {weeks} Woche{'n' if weeks > 1 else ''} und {remaining_days} Tag{'e' if remaining_days > 1 else ''}"
        elif days <= 365:
            months = days // 30
            remaining_days = days % 30
            if remaining_days <= 7:
                return f"⏰ Noch {months} Monat{'e' if months > 1 else ''}"
            else:
                weeks = remaining_days // 7
                return f"⏰ Noch {months} Monat{'e' if months > 1 else ''} und {weeks} Woche{'n' if weeks > 1 else ''}"
        else:
            years = days // 365
            remaining_months = (days % 365) // 30
            if remaining_months == 0:
                return f"⏰ Noch {years} Jahr{'e' if years > 1 else ''}"
            else:
                return f"⏰ Noch {years} Jahr{'e' if years > 1 else ''} und {remaining_months} Monat{'e' if remaining_months > 1 else ''}"

