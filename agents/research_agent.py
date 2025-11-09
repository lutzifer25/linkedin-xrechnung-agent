"""
Research Agent - Sammelt Informationen zu XRechnung, invory.de und einvoicehub.de
"""
from crewai import Agent
from langchain_openai import ChatOpenAI
from config import OPENAI_API_KEY, OPENAI_MODEL, XRECHNUNG_TOPICS
from services.invory_client import InvoryClient
from services.einvoicehub_client import EinvoiceHubClient
import logging

logger = logging.getLogger(__name__)

class ResearchAgent:
    """Agent für Recherche zu XRechnung-Themen"""
    
    def __init__(self):
        self.llm = ChatOpenAI(
            temperature=0.7,
            model_name=OPENAI_MODEL,
            openai_api_key=OPENAI_API_KEY
        )
        
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
            llm=self.llm
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
        
        # Hole Informationen von invory.de
        logger.info("Untersuche invory.de...")
        invory_data = self.invory_client.get_xrechnung_insights()
        
        # Hole Informationen von einvoicehub.de
        logger.info("Untersuche einvoicehub.de...")
        einvoicehub_data = self.einvoicehub_client.get_xrechnung_insights()
        
        # Kombiniere Informationen zu Key Points
        key_points = [
            "XRechnung ist der Standard für elektronische Rechnungen in Deutschland",
            "Compliance mit gesetzlichen Anforderungen ist essentiell",
            "Automatisierung reduziert Fehler und beschleunigt Prozesse",
            "Integration mit ERP-Systemen ist wichtig für Effizienz"
        ]
        
        # Füge spezifische Informationen von den Websites hinzu
        if invory_data and invory_data.get("invory_features"):
            key_points.append(f"Lösungen wie invory.de bieten: {', '.join(invory_data['invory_features'][:2])}")
        
        if einvoicehub_data and einvoicehub_data.get("einvoicehub_features"):
            key_points.append(f"Plattformen wie einvoicehub.de bieten: {', '.join(einvoicehub_data['einvoicehub_features'][:2])}")
        
        research_result = {
            "topic": topic,
            "key_points": key_points[:6],  # Begrenze auf 6 Punkte
            "invory_data": invory_data,
            "einvoicehub_data": einvoicehub_data,
            "invory_url": invory_data.get("invory_url", "https://invory.de") if invory_data else "https://invory.de",
            "einvoicehub_url": einvoicehub_data.get("einvoicehub_url", "https://einvoicehub.de") if einvoicehub_data else "https://einvoicehub.de",
            "trends": [
                "Zunehmende Adoption von XRechnung",
                "Fokus auf vollständige Automatisierung",
                "Integration mit bestehenden Systemen",
                "Cloud-basierte Lösungen gewinnen an Bedeutung"
            ],
            "best_practices": [
                "Frühe Planung der XRechnung-Implementierung",
                "Schulung der Mitarbeiter",
                "Regelmäßige Compliance-Prüfungen",
                "Nutzung von spezialisierten Plattformen und Lösungen"
            ]
        }
        
        logger.info("Recherche abgeschlossen")
        return research_result

