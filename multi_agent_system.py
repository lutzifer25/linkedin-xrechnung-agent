"""
Multi-Agent System für automatische LinkedIn-Post-Erstellung
XRechnung mit invory.de und einvoicehub.de Integration
"""
from agents.research_agent import ResearchAgent
from agents.content_agent import ContentAgent
from agents.review_agent import ReviewAgent
from services.linkedin_client import LinkedInClient
from typing import Dict, Optional
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class LinkedInPostMultiAgentSystem:
    """Multi-Agent System für automatische LinkedIn-Post-Erstellung"""
    
    def __init__(self):
        # Initialize Agents
        self.research_agent = ResearchAgent()
        self.content_agent = ContentAgent()
        self.review_agent = ReviewAgent()
        
        # Initialize Clients
        self.linkedin_client = LinkedInClient()
    
    def create_and_post(self, topic: Optional[str] = None, auto_post: bool = False) -> Dict:
        """
        Erstellt einen LinkedIn-Post und postet ihn optional automatisch
        Der Research Agent untersucht automatisch invory.de und einvoicehub.de
        
        Args:
            topic: Optional - spezifisches XRechnung-Thema
            auto_post: Wenn True, wird der Post automatisch auf LinkedIn gepostet
            
        Returns:
            dict: Ergebnis mit Post-Text und Status
        """
        logger.info("Starte Multi-Agent System für LinkedIn-Post-Erstellung")
        
        try:
            # Schritt 1: Recherche (untersucht invory.de und einvoicehub.de)
            logger.info("Schritt 1: Recherche durch Research Agent")
            logger.info("Research Agent untersucht invory.de und einvoicehub.de...")
            research_data = self.research_agent.research_xrechnung_topic(topic)
            
            # Schritt 2: Content-Erstellung (verwendet Daten von beiden Websites)
            logger.info("Schritt 2: Content-Erstellung durch Content Agent")
            logger.info("Content Agent erstellt Post mit Links zu invory.de und einvoicehub.de...")
            post_text = self.content_agent.create_post(research_data)
            
            # Schritt 3: Review
            logger.info("Schritt 3: Review durch Review Agent")
            review_result = self.review_agent.review_post(post_text, research_data)
            
            # Schritt 4: Post verbessern falls nötig
            if not review_result["approved"]:
                logger.info("Schritt 4: Post wird verbessert")
                post_text = self.review_agent.improve_post(post_text, review_result)
                review_result = self.review_agent.review_post(post_text, research_data)
            
            # Schritt 5: Optional - Post auf LinkedIn
            post_status = None
            if auto_post and review_result["approved"]:
                logger.info("Schritt 5: Posting auf LinkedIn")
                post_status = self.linkedin_client.create_post(post_text)
            elif auto_post and not review_result["approved"]:
                logger.warning("Post wurde nicht genehmigt und wird nicht gepostet")
            
            # Extrahiere Daten für Rückgabe
            invory_data = research_data.get('invory_data', {})
            einvoicehub_data = research_data.get('einvoicehub_data', {})
            
            result = {
                "success": True,
                "post_text": post_text,
                "review_score": review_result["score"],
                "review_approved": review_result["approved"],
                "research_data": research_data,
                "invory_data": invory_data,
                "einvoicehub_data": einvoicehub_data,
                "post_status": post_status,
                "linkedin_posted": auto_post and review_result["approved"] and post_status is not None
            }
            
            logger.info(f"Post-Erstellung abgeschlossen. Score: {review_result['score']}")
            return result
            
        except Exception as e:
            logger.error(f"Fehler bei Post-Erstellung: {str(e)}")
            import traceback
            traceback.print_exc()
            return {
                "success": False,
                "error": str(e),
                "post_text": None
            }
    
    def create_post_preview(self, topic: Optional[str] = None) -> Dict:
        """
        Erstellt einen Post-Preview ohne zu posten
        
        Args:
            topic: Optional - spezifisches XRechnung-Thema
            
        Returns:
            dict: Post-Preview
        """
        return self.create_and_post(topic, auto_post=False)
    
    def get_available_topics(self) -> list:
        """
        Gibt verfügbare XRechnung-Themen zurück
        
        Returns:
            list: Liste von Themen
        """
        from config import XRECHNUNG_TOPICS
        return XRECHNUNG_TOPICS

