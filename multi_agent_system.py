"""
Multi-Agent System für automatische LinkedIn-Post-Erstellung mit Storytelling und Bildern
XRechnung mit invory.de und einvoicehub.de Integration plus DALL-E 3 Bildgenerierung
"""
from agents.research_agent import ResearchAgent
from agents.content_agent import ContentAgent
from agents.review_agent import ReviewAgent
from agents.image_agent import ImageAgent
from services.linkedin_client import LinkedInClient
from config import INCLUDE_IMAGES
from typing import Dict, Optional
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class LinkedInPostMultiAgentSystem:
    """Multi-Agent System für automatische LinkedIn-Post-Erstellung mit Storytelling und Bildern"""
    
    def __init__(self):
        # Initialize Agents
        self.research_agent = ResearchAgent()
        self.content_agent = ContentAgent()
        self.review_agent = ReviewAgent()
        self.image_agent = ImageAgent()
        
        # Initialize Clients
        self.linkedin_client = LinkedInClient()
        
        # Bildgenerierung aktiviert?
        self.include_images = INCLUDE_IMAGES
    
    def create_and_post(self, topic: Optional[str] = None, auto_post: bool = False) -> Dict:
        """
        Erstellt einen narrativen LinkedIn-Post mit optionalem Bild und postet ihn automatisch
        
        Args:
            topic: Optional - spezifisches XRechnung-Thema
            auto_post: Wenn True, wird der Post automatisch auf LinkedIn gepostet
            
        Returns:
            dict: Ergebnis mit Post-Data, Storytelling-Info und Status
        """
        logger.info("🚀 Starte Multi-Agent System mit Storytelling und Bildgenerierung")
        
        try:
            # Schritt 1: Recherche (untersucht invory.de und einvoicehub.de + News + Countdown)
            logger.info("📚 Schritt 1: Erweiterte Recherche durch Research Agent")
            research_data = self.research_agent.research_xrechnung_topic(topic)
            
            # Schritt 2: Bildgenerierung (falls aktiviert)
            image_data = None
            if self.include_images:
                logger.info("🎨 Schritt 2a: Bildgenerierung durch Image Agent")
                try:
                    # Erstelle temporäre Content-Daten für Bildgenerierung
                    temp_content_data = {
                        "topic": topic or research_data.get('topic', 'XRechnung'),
                        "post_content": "Placeholder für Bildgenerierung",
                        "countdown_data": research_data.get('countdown_data', {}),
                        "news_data": research_data.get('news_data', {})
                    }
                    image_data = self.image_agent.generate_image_for_post(temp_content_data)
                    if image_data:
                        logger.info(f"✅ Bild generiert: {image_data.get('theme', 'Unknown theme')}")
                except Exception as e:
                    logger.error(f"❌ Bildgenerierung fehlgeschlagen: {str(e)}")
                    image_data = None
            
            # Schritt 3: Storytelling Content-Erstellung
            logger.info("📖 Schritt 3: Storytelling Content-Erstellung durch Content Agent")
            post_result = self.content_agent.create_storytelling_post(research_data, image_data)
            
            post_text = post_result["post_content"]
            storytelling_structure = post_result["storytelling_structure"]
            
            # Schritt 4: Review
            logger.info("🔍 Schritt 4: Review durch Review Agent")
            review_result = self.review_agent.review_post(post_text, research_data)
            
            # Schritt 5: Post verbessern falls nötig
            if not review_result["approved"]:
                logger.info("🔧 Schritt 5: Post wird verbessert")
                post_text = self.review_agent.improve_post(post_text, review_result)
                review_result = self.review_agent.review_post(post_text, research_data)
                # Update post_result mit verbessertem Text
                post_result["post_content"] = post_text
            
            # Schritt 6: Optional - Post auf LinkedIn mit Bild
            post_status = None
            if auto_post and review_result["approved"]:
                logger.info("📤 Schritt 6: Posting auf LinkedIn mit optionalem Bild")
                
                # Post mit Bild falls vorhanden
                if image_data and image_data.get("image_url"):
                    post_status = self.linkedin_client.create_post(
                        text=post_text,
                        image_url=image_data["image_url"]
                    )
                    if post_status:
                        logger.info("✅ Post mit Bild erfolgreich auf LinkedIn gepostet")
                else:
                    post_status = self.linkedin_client.create_post(post_text)
                    if post_status:
                        logger.info("✅ Text-Post erfolgreich auf LinkedIn gepostet")
                        
            elif auto_post and not review_result["approved"]:
                logger.warning("❌ Post wurde nicht genehmigt und wird nicht gepostet")
            
            # Extrahiere Daten für Rückgabe
            invory_data = research_data.get('invory_data', {})
            einvoicehub_data = research_data.get('einvoicehub_data', {})
            
            result = {
                "success": True,
                "post_data": post_result,  # Komplette Post-Daten mit Storytelling-Info
                "post_text": post_text,
                "storytelling_structure": storytelling_structure,
                "image_data": image_data,
                "review_score": review_result["score"],
                "review_approved": review_result["approved"],
                "research_data": research_data,
                "invory_data": invory_data,
                "einvoicehub_data": einvoicehub_data,
                "post_status": post_status,
                "linkedin_posted": auto_post and review_result["approved"] and post_status is not None,
                "includes_image": image_data is not None,
                "character_count": len(post_text)
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

