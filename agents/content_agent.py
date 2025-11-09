"""
Content Agent - Erstellt LinkedIn-Posts basierend auf Recherche
"""
from crewai import Agent
from config import OPENAI_MODEL, MAX_POST_LENGTH

class ContentAgent:
    """Agent für die Erstellung von LinkedIn-Post-Inhalten"""
    
    def __init__(self):
        # CrewAI 1.4+ uses simplified LLM specification
        self.agent = Agent(
            role='LinkedIn Content Creator für XRechnung',
            goal='Erstelle ansprechende, informative LinkedIn-Posts zu XRechnung-Themen',
            backstory="""Du bist ein versierter Content-Creator, der sich auf
            B2B-Content im Bereich Rechnungswesen und Digitalisierung spezialisiert hat.
            Du verstehst es, komplexe Themen wie XRechnung verständlich und ansprechend
            für LinkedIn zu formulieren. Deine Posts sind informativ, professionell
            und enthalten einen klaren Call-to-Action.""",
            verbose=True,
            allow_delegation=False,
            llm=OPENAI_MODEL  # CrewAI 1.4+ accepts model string directly
        )
    
    def create_post(self, research_data: dict, invory_data: dict = None) -> str:
        """
        Erstellt einen LinkedIn-Post basierend auf Recherche-Daten
        Enthält Links zu invory.de und einvoicehub.de
        
        Args:
            research_data: Daten vom Research Agent (enthält bereits invory und einvoicehub Daten)
            invory_data: Optional - Legacy-Parameter für Kompatibilität
            
        Returns:
            str: LinkedIn-Post Text mit Links
        """
        topic = research_data.get('topic', 'XRechnung')
        key_points = research_data.get('key_points', [])
        
        # Hole Daten von beiden Websites aus research_data
        invory_data_from_research = research_data.get('invory_data', {})
        einvoicehub_data = research_data.get('einvoicehub_data', {})
        
        # URLs
        invory_url = research_data.get('invory_url', 'https://invory.de')
        einvoicehub_url = research_data.get('einvoicehub_url', 'https://einvoicehub.de')
        
        # Features von beiden Websites
        invory_features = invory_data_from_research.get('invory_features', []) if invory_data_from_research else []
        einvoicehub_features = einvoicehub_data.get('einvoicehub_features', []) if einvoicehub_data else []
        
        # Erstelle Post basierend auf Daten
        post = f"""💼 {topic}: Die digitale Transformation im Rechnungswesen schreitet voran.

🔍 Aktuelle Entwicklungen zeigen, wie wichtig standardisierte E-Invoicing-Lösungen wie XRechnung geworden sind. Unternehmen profitieren von automatisierten Prozessen und verbesserter Compliance.

✅ Wichtigste Erkenntnisse:"""
        
        for i, point in enumerate(key_points[:3], 1):
            post += f"\n• {point}"
        
        # Füge Informationen zu invory.de hinzu
        if invory_features:
            post += f"\n\n🚀 Lösungen wie {invory_url} bieten Unternehmen die Möglichkeit, ihre Rechnungsprozesse effizient zu digitalisieren und alle XRechnung-Anforderungen zu erfüllen."
            if len(invory_features) > 0:
                post += f"\n\n✨ Features von {invory_url}:"
                for feature in invory_features[:2]:
                    post += f"\n• {feature}"
        
        # Füge Informationen zu einvoicehub.de hinzu
        if einvoicehub_features:
            post += f"\n\n📊 Plattformen wie {einvoicehub_url} ermöglichen es Unternehmen, digitale Rechnungsprozesse zu optimieren und zu automatisieren."
            if len(einvoicehub_features) > 0:
                post += f"\n\n🎯 Features von {einvoicehub_url}:"
                for feature in einvoicehub_features[:2]:
                    post += f"\n• {feature}"
        
        post += "\n\nWas sind eure Erfahrungen mit XRechnung? Welche Herausforderungen seht ihr bei der Umsetzung?"
        
        # Füge Links am Ende hinzu
        post += f"\n\n🔗 Weitere Informationen:"
        post += f"\n• {invory_url}"
        post += f"\n• {einvoicehub_url}"
        
        post += "\n\n#XRechnung #EInvoicing #DigitaleTransformation #Prozessautomatisierung #Rechnungswesen #Digitalisierung"
        
        # Stelle sicher, dass Post nicht zu lang ist
        if len(post) > MAX_POST_LENGTH:
            # Kürze den Post, behalte aber die Links
            links_section = f"\n\n🔗 Weitere Informationen:\n• {invory_url}\n• {einvoicehub_url}\n\n#XRechnung #EInvoicing #DigitaleTransformation #Prozessautomatisierung #Rechnungswesen #Digitalisierung"
            max_content_length = MAX_POST_LENGTH - len(links_section) - 50
            post = post[:max_content_length] + "..." + links_section
        
        return post
    
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

