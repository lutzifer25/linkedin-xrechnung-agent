"""
Content Agent - Erstellt narrative LinkedIn-Posts mit Storytelling basierend auf Recherche
"""
import random
from crewai import Agent
from config import OPENAI_MODEL, MAX_POST_LENGTH, STORYTELLING_STRUCTURES

class ContentAgent:
    """Agent für die Erstellung von narrativen LinkedIn-Post-Inhalten mit Storytelling"""
    
    def __init__(self):
        # CrewAI 1.4+ uses simplified LLM specification
        self.agent = Agent(
            role='LinkedIn Storytelling Creator für XRechnung',
            goal='Erstelle fesselnde Geschichten und narrative Posts zu XRechnung-Themen die Emotionen wecken',
            backstory="""Du bist ein kreativer Storyteller und Content-Creator mit einer 
            besonderen Gabe, trockene B2B-Themen in mitreißende Geschichten zu verwandeln.
            Du verstehst es, XRechnung und E-Invoicing durch narrative Strukturen, 
            Charaktere und Situationen lebendig zu machen. Deine Posts lesen sich wie 
            spannende Kurzgeschichten und hinterlassen beim Publikum ein Gefühl von 
            "Das will ich auch erleben!" statt nur "Das sollte ich wissen."
            
            Du nutzt bewährte Storytelling-Techniken wie Hero's Journey, Problem-Solution-Narratives
            und Future Visions, um XRechnung-Content zu schaffen, der geteilt wird.""",
            verbose=True,
            allow_delegation=False,
            llm=OPENAI_MODEL  # CrewAI 1.4+ accepts model string directly
        )
    
    def create_storytelling_post(self, research_data: dict, image_data: dict = None, invory_data: dict = None) -> dict:
        """
        Erstellt einen narrativen LinkedIn-Post mit Storytelling-Struktur
        
        Args:
            research_data: Daten vom Research Agent 
            image_data: Optional - Bilddaten vom Image Agent
            invory_data: Optional - Legacy-Parameter für Kompatibilität
            
        Returns:
            dict: Post-Daten mit text, storytelling_structure, image_info
        """
        # Wähle Storytelling-Struktur basierend auf Zeit und Content
        storytelling_structure = self._select_smart_storytelling_structure(research_data)
        
        # Extrahiere Basisdaten
        topic = research_data.get('topic', 'XRechnung')
        countdown_data = research_data.get('countdown_data', {})
        news_data = research_data.get('news_data', {})
        einvoicehub_highlights = research_data.get('einvoicehub_highlights', [])
        
        # URLs für Links
        invory_url = research_data.get('invory_url', 'https://invory.de')
        einvoicehub_url = research_data.get('einvoicehub_url', 'https://einvoicehub.de')
        
        # Generiere Story basierend auf gewählter Struktur
        story_content = self._generate_story_content(storytelling_structure, topic, countdown_data, news_data, einvoicehub_highlights)
        
        # Füge Links am Ende hinzu
        story_content += f"\n\n� Entdecke mehr:"
        story_content += f"\n• {invory_url} - Deine XRechnung-Lösung"
        story_content += f"\n• {einvoicehub_url} - E-Invoicing Plattform"
        
        story_content += "\n\n#XRechnung #Storytelling #DigitaleTransformation #EInvoicing #ZukunftGestalten"
        
        # Stelle sicher, dass Post nicht zu lang ist
        if len(story_content) > MAX_POST_LENGTH:
            links_section = f"\n\n🔗 Entdecke mehr:\n• {invory_url}\n• {einvoicehub_url}\n\n#XRechnung #Storytelling #DigitaleTransformation #EInvoicing #ZukunftGestalten"
            max_content_length = MAX_POST_LENGTH - len(links_section) - 50
            story_content = story_content[:max_content_length] + "..." + links_section
        
        return {
            "post_content": story_content,
            "storytelling_structure": storytelling_structure,
            "image_data": image_data,
            "topic": topic,
            "character_count": len(story_content)
        }
    
    def _generate_story_content(self, storytelling_structure: dict, topic: str, countdown_data: dict, news_data: dict, einvoicehub_highlights: list) -> str:
        """Generiert Story-Content basierend auf gewählter Storytelling-Struktur"""
        
        structure_name = storytelling_structure["name"]
        
        if structure_name == "Hero's Journey":
            return self._create_heroes_journey_story(topic, countdown_data, einvoicehub_highlights)
        elif structure_name == "Problem-Solution":
            return self._create_problem_solution_story(topic, countdown_data, einvoicehub_highlights) 
        elif structure_name == "Future Vision":
            return self._create_future_vision_story(topic, countdown_data, news_data)
        elif structure_name == "Behind the Scenes":
            return self._create_behind_scenes_story(topic, einvoicehub_highlights)
        else:
            return self._create_default_story(topic, countdown_data)
    
    def _create_heroes_journey_story(self, topic: str, countdown_data: dict, einvoicehub_highlights: list) -> str:
        """Erstellt eine Hero's Journey Geschichte"""
        
        countdown_text = ""
        if countdown_data and countdown_data.get('next_milestone'):
            milestone = countdown_data['next_milestone']
            countdown_text = f" {milestone['countdown_text']} bis zum großen Wendepunkt: {milestone['description']}"
        
        story = f"""🦸‍♀️ Die Geschichte von Sarah's XRechnung-Abenteuer

Sarah, Geschäftsführerin eines mittelständischen Unternehmens, stand vor einer scheinbar unlösbaren Herausforderung: Hunderte von Rechnungen stapelten sich auf ihrem Schreibtisch.{countdown_text}

💔 Der Kampf war real:
• Nächtliche Überstunden beim manuellen Rechnungsabgleich
• Ständige Angst vor Compliance-Fehlern  
• Das Team war überlastet und frustriert

✨ Dann entdeckte Sarah die Macht der XRechnung-Automatisierung..."""

        # Füge einvoicehub Features als "magische Werkzeuge" hinzu
        if einvoicehub_highlights:
            story += f"\n\n🛡️ Ihre neuen Superkräfte:"
            for highlight in einvoicehub_highlights[:2]:
                clean_highlight = highlight.replace("🚀", "").replace("📧", "").replace("📊", "").replace("🔗", "").replace("📱", "").replace("🛡️", "").replace("💰", "").replace("🔌", "").replace("📈", "").replace("👩‍💻", "").strip()
                story += f"\n• {clean_highlight}"
        
        story += f"""

🏆 Heute, 6 Monate später:
• Sarah verlässt pünktlich das Büro
• Ihr Team fokussiert sich auf Wachstum statt auf Papierkram
• 95% weniger Rechnungsfehler

"Die beste Entscheidung, die ich je getroffen habe!" - Sarah

➡️ Welche Herausforderung wartet darauf, von DIR gelöst zu werden?"""
        
        return story
    
    def _create_problem_solution_story(self, topic: str, countdown_data: dict, einvoicehub_highlights: list) -> str:
        """Erstellt eine Problem-Solution Geschichte"""
        
        countdown_text = ""
        if countdown_data and countdown_data.get('next_milestone'):
            milestone = countdown_data['next_milestone']
            countdown_text = f"\n\n⏰ Zeit drängt: {milestone['countdown_text']} bis {milestone['description']}"
        
        story = f"""😰 Kennst du das Gefühl?

Es ist Freitagabend, 19:30 Uhr. Während andere bereits das Wochenende genießen, sitzt du noch im Büro. Vor dir: Ein Berg von Rechnungen, die bis Montag verarbeitet werden müssen.

🤯 Das Problem:
• Manuelle Dateneingabe bis spät in die Nacht
• Ständige Sorge um Compliance-Fehler
• Dein Team ist gestresst und überlastet{countdown_text}

💡 Die Wendung:
Was wäre, wenn ich dir sage, dass XRechnung-Automatisierung das alles ändern kann?"""

        if einvoicehub_highlights:
            story += f"\n\n🎯 Die Lösung in Aktion:"
            for highlight in einvoicehub_highlights[:2]:
                clean_highlight = highlight.replace("🚀", "").replace("📧", "").replace("📊", "").replace("🔗", "").replace("📱", "").replace("🛡️", "").replace("💰", "").replace("🔌", "").replace("📈", "").replace("👩‍💻", "").strip()
                story += f"\n• {clean_highlight}"

        story += f"""

🚀 Stell dir vor:
• Automatische Rechnungsverarbeitung in Sekunden
• Deine Freitage gehören wieder DIR
• Dein Team kann sich auf Wachstum konzentrieren

➡️ Bist du bereit für die Transformation? Erzähl mir von deinen Rechnungs-Herausforderungen!"""
        
        return story
    
    def _create_future_vision_story(self, topic: str, countdown_data: dict, news_data: dict) -> str:
        """Erstellt eine Future Vision Geschichte mit rotierenden Templates"""
        import random
        import datetime
        import hashlib
        
        # Datum-basierte Template-Auswahl für konsistente aber variierende Vision
        today = datetime.date.today()
        date_hash = int(hashlib.md5(f"{topic}{today}".encode()).hexdigest(), 16)
        
        # 5 verschiedene Future Vision Templates
        vision_templates = [
            # Template 1: Industrie-Transformation  
            f"""🚀 2030: Die große XRechnung-Revolution ist da!

*Flashforward aktiviert* 💫

Ein Unternehmerverband berichtet: "99% aller deutschen Unternehmen nutzen jetzt vollautomatische XRechnung-Verarbeitung. Manuelle Rechnungsbearbeitung ist Geschichte."

🌟 Was heute noch Zukunft scheint:
• Millisekunden-Rechnungsverarbeitung
• Zero-Error-Compliance durch KI
• Grenzenloses digitales Geschäft""",

            # Template 2: Persönliche CEO-Vision
            f"""🔮 Blick ins Jahr 2030...

*Vision aktiviert* ✨

CEO Sarah K. schaut auf ihre Statistik: "Letztes Jahr: 15.000 Rechnungen, 0 manuelle Eingriffe, 100% Compliance-Rate. XRechnung hat unser Geschäft revolutioniert."

🌟 Die neue Realität:
• Vollständige Automatisierung ist Standard
• Unternehmen fokussieren auf Innovation statt Verwaltung  
• EU-weite nahtlose Geschäftsprozesse""",

            # Template 3: Markt-Transformation
            f"""⚡ 2030: Der deutsche Mittelstand ist digital!

*Zukunftsscan aktiviert* 📊

Aktuelle Zahlen zeigen: Über 4 Millionen deutsche Unternehmen verarbeiten täglich 50+ Millionen XRechnungen vollautomatisch. Der Produktivitätssprung ist messbar.

🌟 Diese Zukunft ist real:
• 95% Kostenreduktion in der Rechnungsbearbeitung
• Fehlerquote unter 0,1%
• Neue Geschäftsmodelle durch Effizienz""",

            # Template 4: Technologie-Vision  
            f"""🔬 2030: XRechnung 5.0 ist Realität!

*Innovation aktiviert* 🧬

Die nächste Generation ist da: KI-gesteuerte XRechnungen passen sich automatisch an Geschäftsregeln an. Blockchain sichert jeden Transaktion. Quantenverschlüsselung schützt sensible Daten.

🌟 Technologie der Zukunft:
• Adaptive KI optimiert jeden Prozess
• Real-Time-Compliance in 27 EU-Ländern
• Quantum-sichere Rechnungsverarbeitung""",

            # Template 5: Gesellschafts-Impact
            f"""🌍 2030: XRechnung rettet den Planeten!

*Impact aktiviert* 🌱

Studie zeigt: Durch vollständige XRechnung-Digitalisierung werden jährlich 2,3 Millionen Tonnen Papier gespart. 180.000 Arbeitsstunden pro Tag für Innovationen freigesetzt.

🌟 Der große Wandel:
• Papierlose Wirtschaft ist Realität
• Millionen Stunden für Kreativität gewonnen  
• Nachhaltigkeit durch Effizienz"""
        ]
        
        # Wähle Template basierend auf Datum
        selected_template = vision_templates[date_hash % len(vision_templates)]
        story = selected_template

        # Füge aktuellen Countdown hinzu
        if countdown_data and countdown_data.get('next_milestone'):
            milestone = countdown_data['next_milestone']
            story += f"\n\n⏰ Die Zukunft beginnt JETZT: {milestone['countdown_text']} bis {milestone['description']}"

        # Füge News hinzu falls verfügbar
        if news_data and news_data.get('headlines'):
            story += f"\n\n📰 Aktuelle Signale der Transformation:"
            for headline in news_data['headlines'][:2]:
                story += f"\n• {headline}"

        story += f"""

🚀 Aber hier ist das Verrückte:
Diese "Zukunft" existiert bereits HEUTE! Unternehmen nutzen schon jetzt XRechnung-Automatisierung und leben bereits in 2030.

💭 Die Frage ist nicht OB, sondern WANN du den Sprung machst.

➡️ In welchem Jahr willst DU ankommen? 2024 oder 2030?"""
        
        return story
    
    def _create_behind_scenes_story(self, topic: str, einvoicehub_highlights: list) -> str:
        """Erstellt eine Behind the Scenes Geschichte"""
        
        story = f"""🎬 Behind the Scenes: Wie XRechnung-Magie entsteht

*Blick hinter die Kulissen bei Invory* 

7:30 Uhr morgens. Während die meisten noch schlafen, ist unser Entwicklerteam bereits hochkonzentriert dabei, die Zukunft der Rechnungsverarbeitung zu programmieren.

👩‍💻 Was ihr nicht seht:
• 47 Kaffeetassen und unzählige "Aha!"-Momente
• Stundenlange Diskussionen über die perfekte User Experience  
• Nächtliche Coding-Sessions für eure Compliance-Sicherheit"""

        if einvoicehub_highlights:
            story += f"\n\n💡 Unsere neuesten Durchbrüche:"
            for highlight in einvoicehub_highlights[:2]:
                clean_highlight = highlight.replace("🚀", "").replace("📧", "").replace("📊", "").replace("🔗", "").replace("📱", "").replace("🛡️", "").replace("💰", "").replace("🔌", "").replace("📈", "").replace("👩‍💻", "").strip()
                story += f"\n• {clean_highlight}"

        story += f"""

🔥 Das Coolste dabei:
Jeder Bug, den wir fixen, jedes Feature, das wir bauen - es macht das Leben von echten Menschen leichter. Gestern haben wir eine Nachricht von einem Kunden bekommen: "Dank euch kann ich wieder pünktlich nach Hause!"

💝 DAS ist unser Antrieb.

➡️ Welche Technologie-Geschichte würdest DU gerne mitschreiben?"""
        
        return story
    
    def _create_default_story(self, topic: str, countdown_data: dict) -> str:
        """Fallback für Standard-Stories"""
        
        countdown_text = ""
        if countdown_data and countdown_data.get('next_milestone'):
            milestone = countdown_data['next_milestone']
            countdown_text = f"\n\n⏰ {milestone['countdown_text']} bis {milestone['description']}"
        
        return f"""💼 {topic}: Eine Reise in die digitale Zukunft

Stell dir vor, du könntest mit einem Fingerschnips alle deine Rechnungsprobleme lösen...

🔄 Die Transformation beginnt mit einem ersten Schritt:
• Von manuell zu automatisiert
• Von kompliziert zu elegant  
• Von stressig zu entspannt{countdown_text}

✨ Die Magie liegt in der Einfachheit der XRechnung.

➡️ Bist du bereit für den nächsten Schritt?"""
    
    def create_post(self, research_data: dict, invory_data: dict = None) -> str:
        """Legacy-Methode für Rückwärtskompatibilität - nutzt neues Storytelling"""
        result = self.create_storytelling_post(research_data, invory_data=invory_data)
        return result["post_content"]
    
    def _select_smart_storytelling_structure(self, research_data: dict) -> dict:
        """
        Wählt intelligente Storytelling-Struktur basierend auf Zeit, Content und Rotation
        
        Args:
            research_data: Recherche-Daten für Context
            
        Returns:
            dict: Gewählte Storytelling-Struktur
        """
        import datetime
        import hashlib
        
        # Erstelle Seed basierend auf Datum für konsistente aber variierende Auswahl
        today = datetime.date.today()
        date_seed = int(hashlib.md5(str(today).encode()).hexdigest(), 16) % 10000
        
        topic = research_data.get('topic', 'XRechnung')
        countdown_data = research_data.get('countdown_data', {})
        
        # Intelligente Auswahl basierend auf Content
        if "countdown" in topic.lower() or countdown_data.get('next_milestone'):
            # Bei Countdown-Content: Problem-Solution oder Future Vision
            options = [s for s in STORYTELLING_STRUCTURES if s["name"] in ["Problem-Solution", "Future Vision"]]
        elif "motivation" in topic.lower() or "montag" in topic.lower():
            # Bei Motivation: Hero's Journey oder Behind Scenes  
            options = [s for s in STORYTELLING_STRUCTURES if s["name"] in ["Hero's Journey", "Behind the Scenes"]]
        elif "test" in topic.lower() or "debug" in topic.lower() or "behind" in topic.lower():
            # Bei Tests/Debug: Behind Scenes für Authentizität  
            options = [s for s in STORYTELLING_STRUCTURES if s["name"] == "Behind the Scenes"]
        else:
            # Standard: Alle Strukturen verfügbar
            options = STORYTELLING_STRUCTURES
        
        # Wähle basierend auf Datum-Seed für Konsistenz aber tägliche Variation
        selected_index = (date_seed + len(topic)) % len(options)
        selected_structure = options[selected_index]
        
        print(f"🎭 Storytelling gewählt: {selected_structure['name']} (basierend auf '{topic}' + Datum)")
        
        return selected_structure
    
    def optimize_post(self, post: str) -> str:
        """
        Optimiert einen Post für bessere Engagement-Raten
        
        Args:
            post: Original Post
            
        Returns:
            str: Optimierter Post
        """
        # Hier könnte der Agent den Post optimieren
        # z.B. bessere Hashtags, bessere Struktur, etc.
        return post

