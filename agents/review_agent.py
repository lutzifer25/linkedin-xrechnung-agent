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
            role='LinkedIn Content & Visual Quality Reviewer',
            goal='Überprüfe und verbessere LinkedIn-Posts auf Qualität, Compliance und visuelle Wirkung',
            backstory="""Du bist ein erfahrener Social Media Manager und Visual Content Specialist
            mit Expertise in B2B-Content auf LinkedIn. Du prüfst sowohl Text als auch Bilder auf:
            
            TEXT-REVIEW:
            - Richtige Länge und Format
            - Professionellen Ton und Storytelling-Qualität
            - Compliance und Richtigkeit
            - Engagement-Potenzial
            - Relevante Hashtags
            
            BILD-REVIEW:
            - Theme-Content-Passung (Bild unterstützt die Story)
            - Professionelle Qualität (DALL-E 3 Standards)
            - XRechnung-Relevanz und B2B-Angemessenheit
            - Comic-Style Balance (locker aber seriös)
            
            Du sorgst für perfekte Text-Bild-Harmonie und höchste Qualitätsstandards.""",
            verbose=True,
            allow_delegation=False,
            llm=OPENAI_MODEL  # CrewAI 1.4+ accepts model string directly
        )
    
    def review_post(self, post: str, research_data: dict, image_data: dict = None) -> dict:
        """
        Überprüft einen Post auf Qualität und Compliance (Text + Bild)
        
        Args:
            post: Der zu überprüfende Post
            research_data: Original Recherche-Daten
            image_data: Optional - Bild-Daten vom Image Agent
            
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
        
        # Prüfe Bild-Qualität (falls vorhanden)
        if image_data:
            image_issues = self._review_image(image_data, post, research_data)
            review_result["issues"].extend(image_issues.get("issues", []))
            review_result["suggestions"].extend(image_issues.get("suggestions", []))
        
        # Berechne Score
        review_result["score"] = self._calculate_score(post, review_result, image_data)
        
        return review_result
    
    def _review_image(self, image_data: dict, post: str, research_data: dict) -> dict:
        """
        Überprüft die Qualität und Relevanz des generierten Bildes
        
        Args:
            image_data: Bild-Daten vom Image Agent
            post: Post-Text für Kontext
            research_data: Recherche-Daten
            
        Returns:
            dict: Issues und Suggestions für das Bild
        """
        result = {"issues": [], "suggestions": []}
        
        if not image_data:
            result["suggestions"].append("Kein Bild verfügbar - erwäge Bild-Generierung")
            return result
        
        # Prüfe ob Bild-URL verfügbar ist
        if not image_data.get("image_url"):
            result["issues"].append("Bild-URL fehlt oder ungültig")
        
        # Prüfe Theme-Passung zum Post-Inhalt
        image_theme = image_data.get("theme", "")
        post_lower = post.lower()
        
        # Validiere Theme-Content-Match
        theme_matches = {
            "countdown": ["countdown", "zeit", "deadline", "⏰"],
            "automatisierung": ["automatisierung", "roboter", "ki", "ai"],
            "transformation": ["transformation", "digital", "wandel"],
            "compliance": ["compliance", "regel", "vorschrift", "häkchen"],
            "erfolg": ["erfolg", "gewinn", "wachstum", "celebration"],
            "problem": ["problem", "lösung", "herausforderung"],
            "zukunft": ["zukunft", "vision", "2030", "modern"]
        }
        
        # Prüfe ob Theme zum Content passt
        theme_relevant = False
        for theme_key, keywords in theme_matches.items():
            if theme_key in image_theme.lower():
                theme_relevant = any(keyword in post_lower for keyword in keywords)
                break
        
        if not theme_relevant:
            result["suggestions"].append(f"Bild-Theme '{image_theme}' passt möglicherweise nicht optimal zum Post-Inhalt")
        
        # Prüfe DALL-E Prompt Qualität
        prompt = image_data.get("prompt", "")
        if len(prompt) < 20:
            result["suggestions"].append("Bild-Prompt könnte detaillierter sein für bessere Qualität")
        
        # Bonus-Bewertung für gute Bild-Integration
        if image_data.get("style") == "DALL-E 3 Generated":
            result["suggestions"].append("✅ Hochqualitatives DALL-E 3 Bild generiert")
        
        return result
    
    def _calculate_score(self, post: str, review_result: dict, image_data: dict = None) -> int:
        """Berechnet einen Qualitätsscore für den Post (Text + Bild)"""
        score = 100
        
        # Abzug für Issues
        score -= len(review_result["issues"]) * 15  # Weniger Abzug da jetzt auch Bild-Issues
        
        # Bonus für gute Struktur
        if "\n\n" in post:
            score += 10
        
        # Bonus für Hashtags
        hashtag_count = post.count("#")
        if 3 <= hashtag_count <= 8:
            score += 10
        
        # Bonus für Bild-Integration
        if image_data:
            if image_data.get("image_url"):
                score += 15  # Bonus für verfügbares Bild
            if image_data.get("style") == "DALL-E 3 Generated":
                score += 10  # Extra Bonus für DALL-E 3
            if len(image_data.get("prompt", "")) > 30:
                score += 5   # Bonus für detaillierten Prompt
        
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

