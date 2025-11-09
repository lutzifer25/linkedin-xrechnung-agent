"""
Review Agent - Prüft und verbessert erstellte Posts
"""
from crewai import Agent
from config import OPENAI_MODEL, MAX_POST_LENGTH

class ReviewAgent:
    """Agent für die Überprüfung und Verbesserung von LinkedIn-Posts"""
    
    def __init__(self):
        # CrewAI 1.4+ uses simplified LLM specification
        self.agent = Agent(
            role='LinkedIn Post Quality Reviewer',
            goal='Überprüfe und verbessere LinkedIn-Posts auf Qualität, Compliance und Wirkung',
            backstory="""Du bist ein erfahrener Social Media Manager mit Expertise
            in B2B-Content auf LinkedIn. Du prüfst Posts auf:
            - Richtige Länge und Format
            - Professionellen Ton
            - Compliance und Richtigkeit
            - Engagement-Potenzial
            - Relevante Hashtags
            Du sorgst dafür, dass jeder Post den höchsten Qualitätsstandards entspricht.""",
            verbose=True,
            allow_delegation=False,
            llm=OPENAI_MODEL  # CrewAI 1.4+ accepts model string directly
        )
    
    def review_post(self, post: str, research_data: dict) -> dict:
        """
        Überprüft einen Post auf Qualität und Compliance
        
        Args:
            post: Der zu überprüfende Post
            research_data: Original Recherche-Daten
            
        Returns:
            dict: Review-Ergebnis mit Bewertung und Verbesserungsvorschlägen
        """
        review_result = {
            "approved": True,
            "score": 0,
            "issues": [],
            "suggestions": [],
            "improved_post": post
        }
        
        # Prüfungen
        if len(post) > MAX_POST_LENGTH:
            review_result["approved"] = False
            review_result["issues"].append(f"Post zu lang ({len(post)} Zeichen)")
        
        if not post.strip():
            review_result["approved"] = False
            review_result["issues"].append("Post ist leer")
        
        # Prüfe auf relevante Hashtags
        if "#XRechnung" not in post and "#xrechnung" not in post:
            review_result["suggestions"].append("Hashtag #XRechnung hinzufügen")
        
        # Prüfe auf professionellen Ton
        # (könnte erweitert werden mit Sentiment-Analyse)
        
        # Berechne Score
        review_result["score"] = self._calculate_score(post, review_result)
        
        return review_result
    
    def _calculate_score(self, post: str, review_result: dict) -> int:
        """Berechnet einen Qualitätsscore für den Post"""
        score = 100
        
        # Abzug für Issues
        score -= len(review_result["issues"]) * 20
        
        # Bonus für gute Struktur
        if "\n\n" in post:
            score += 10
        
        # Bonus für Hashtags
        hashtag_count = post.count("#")
        if 3 <= hashtag_count <= 8:
            score += 10
        
        return max(0, min(100, score))
    
    def improve_post(self, post: str, review_result: dict) -> str:
        """
        Verbessert einen Post basierend auf Review-Ergebnissen
        
        Args:
            post: Original Post
            review_result: Review-Ergebnisse
            
        Returns:
            str: Verbesserter Post
        """
        improved_post = post
        
        # Kürze Post wenn zu lang
        if len(improved_post) > MAX_POST_LENGTH:
            improved_post = improved_post[:MAX_POST_LENGTH-50] + "..."
        
        # Füge fehlende Hashtags hinzu
        if "#XRechnung" not in improved_post:
            improved_post += "\n\n#XRechnung"
        
        return improved_post

