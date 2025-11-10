"""
Image Agent für die Generierung von Comic-Style Bildern zu XRechnung-Themen
Nutzt DALL-E 3 für professionelle, aber lockere Illustrationen
"""

import os
import random
import requests
from typing import Dict, Optional
from openai import OpenAI
from crewai import Agent
from config import (
    OPENAI_API_KEY, OPENAI_MODEL, DALLE_MODEL, DALLE_QUALITY, DALLE_SIZE,
    IMAGE_STYLE_PROMPTS, XRECHNUNG_IMAGE_THEMES, STORYTELLING_STRUCTURES
)


class ImageAgent:
    """Agent für die Generierung von ansprechenden Bildern zu XRechnung-Posts"""
    
    def __init__(self):
        # Verwende eigene Klasse statt CrewAI Agent für OpenAI Client Support
        self.role = "Visual Storytelling Specialist"
        self.goal = "Erstelle ansprechende, comic-artige Bilder die XRechnung-Themen visuell und humorvoll vermitteln"
        self.backstory = """Du bist ein kreativer Visual Designer mit Expertise in Business-Illustration 
        und Comic-Art. Du verstehst sowohl die technischen Aspekte von XRechnung als auch 
        die Kunst, komplexe B2B-Themen visuell zugänglich und unterhaltsam zu machen. 
        
        Deine Illustrationen kombinieren Professionalität mit einem augenzwinkernden, 
        lockeren Stil der auch trockene Compliance-Themen interessant macht."""
        
        # OpenAI Client für DALL-E 3
        self.openai_client = OpenAI(api_key=OPENAI_API_KEY) if OPENAI_API_KEY else None
        
    def generate_image_for_post(self, content_data: Dict) -> Optional[Dict]:
        """
        Generiert ein passendes Bild basierend auf dem Post-Content
        
        Args:
            content_data: Dict mit post_content, topic, storytelling_structure, etc.
        
        Returns:
            Dict mit image_url, prompt, theme oder None bei Fehler
        """
        try:
            if not self.openai_client:
                print("⚠️  OpenAI API Key fehlt - nutze Mock-Bild")
                return self._get_mock_image_data(content_data)
            
            # Wähle Bildthema basierend auf Content
            image_theme = self._select_image_theme(content_data)
            
            # Erstelle DALL-E Prompt
            dalle_prompt = self._create_dalle_prompt(image_theme, content_data)
            
            print(f"🎨 Generiere Bild mit DALL-E 3...")
            print(f"📝 Theme: {image_theme}")
            
            # DALL-E 3 API Call
            response = self.openai_client.images.generate(
                model=DALLE_MODEL,
                prompt=dalle_prompt,
                size=DALLE_SIZE,
                quality=DALLE_QUALITY,
                n=1
            )
            
            image_url = response.data[0].url
            
            print(f"✅ Bild generiert: {image_url[:50]}...")
            
            return {
                "image_url": image_url,
                "prompt": dalle_prompt,
                "theme": image_theme,
                "style": "DALL-E 3 Generated"
            }
            
        except Exception as e:
            print(f"❌ Fehler bei Bildgenerierung: {str(e)}")
            return self._get_mock_image_data(content_data)
    
    def _select_image_theme(self, content_data: Dict) -> str:
        """Wählt passendes Bildthema basierend auf Content aus"""
        
        post_content = content_data.get("post_content", "").lower()
        topic = content_data.get("topic", "").lower() 
        
        # Thema basierend auf Keywords im Content
        if "countdown" in post_content or "deadline" in post_content or "zeit" in post_content:
            return "Countdown: Kalender oder Timer zeigt nahende Deadlines"
        elif "automatisierung" in post_content or "roboter" in post_content:
            return "Automatisierung: Roboter und Menschen arbeiten harmonisch zusammen"
        elif "transformation" in post_content or "digital" in post_content:
            return "digitale Transformation: Papierrechnungen werden zu digitalen Dokumenten"
        elif "erfolg" in post_content or "lösung" in post_content:
            return "Problemlösung: Komplexe Prozesse werden vereinfacht dargestellt"
        elif "zukunft" in post_content or "vision" in post_content:
            return "Zukunftsvision: moderne digitale Bürolandschaft"
        else:
            # Zufälliges Thema falls kein Match
            return random.choice(XRECHNUNG_IMAGE_THEMES)
    
    def _create_dalle_prompt(self, image_theme: str, content_data: Dict) -> str:
        """Erstellt optimierten DALL-E 3 Prompt"""
        
        # Wähle Stil
        style = random.choice(IMAGE_STYLE_PROMPTS)
        
        # Basis-Prompt mit Theme und Stil
        prompt_parts = [
            image_theme,
            style,
            "professional business context",
            "XRechnung and e-invoicing theme", 
            "bright and engaging colors",
            "no text or letters in image",  # Wichtig für LinkedIn
            "high quality illustration"
        ]
        
        # Storytelling-Struktur berücksichtigen
        storytelling = content_data.get("storytelling_structure")
        if storytelling:
            if "Hero's Journey" in storytelling.get("name", ""):
                prompt_parts.append("heroic journey visualization")
            elif "Problem-Solution" in storytelling.get("name", ""):
                prompt_parts.append("before-and-after comparison")
            elif "Future Vision" in storytelling.get("name", ""):
                prompt_parts.append("futuristic business environment")
        
        return ", ".join(prompt_parts)
    
    def _get_mock_image_data(self, content_data: Dict) -> Dict:
        """Fallback Mock-Daten wenn DALL-E nicht verfügbar"""
        
        theme = self._select_image_theme(content_data)
        
        return {
            "image_url": "https://via.placeholder.com/1024x1024/4A90E2/FFFFFF?text=XRechnung+Visual",
            "prompt": f"Mock image for: {theme}",
            "theme": theme,
            "style": "Mock Placeholder"
        }
    
    def download_image(self, image_url: str, save_path: str) -> bool:
        """
        Lädt generiertes Bild herunter für LinkedIn Upload
        
        Args:
            image_url: URL des generierten Bildes
            save_path: Lokaler Pfad zum Speichern
        
        Returns:
            bool: True bei Erfolg, False bei Fehler
        """
        try:
            response = requests.get(image_url, timeout=30)
            response.raise_for_status()
            
            with open(save_path, 'wb') as f:
                f.write(response.content)
            
            print(f"📁 Bild gespeichert: {save_path}")
            return True
            
        except Exception as e:
            print(f"❌ Fehler beim Download: {str(e)}")
            return False
    
    def create_storytelling_visual(self, story_structure: str, topic: str) -> Optional[Dict]:
        """
        Erstellt Bild speziell für eine Storytelling-Struktur
        
        Args:
            story_structure: Name der Storytelling-Struktur
            topic: XRechnung Thema
        
        Returns:
            Dict mit Bilddaten oder None
        """
        
        content_data = {
            "storytelling_structure": {"name": story_structure},
            "topic": topic,
            "post_content": f"{story_structure} {topic}"
        }
        
        return self.generate_image_for_post(content_data)


# Für direkten Import
def create_image_agent():
    """Factory Funktion für Image Agent"""
    return ImageAgent()


if __name__ == "__main__":
    # Test des Image Agents
    agent = ImageAgent()
    
    test_content = {
        "post_content": "Die digitale Transformation wartet nicht! Countdown zur XRechnung-Pflicht läuft...",
        "topic": "XRechnung Deadline",
        "storytelling_structure": {"name": "Future Vision"}
    }
    
    result = agent.generate_image_for_post(test_content)
    print("🎨 Test-Ergebnis:", result)