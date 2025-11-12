"""
Konfigurationsdatei für das LinkedIn Post Multi-Agent System
"""
import os
from dotenv import load_dotenv

load_dotenv()

# LinkedIn API Konfiguration
LINKEDIN_CLIENT_ID = os.getenv("LINKEDIN_CLIENT_ID")
LINKEDIN_CLIENT_SECRET = os.getenv("LINKEDIN_CLIENT_SECRET")
LINKEDIN_ACCESS_TOKEN = os.getenv("LINKEDIN_ACCESS_TOKEN")
LINKEDIN_ORGANIZATION_ID = os.getenv("LINKEDIN_ORGANIZATION_ID")  # Optional: wird automatisch abgerufen
LINKEDIN_COMPANY_NAME = os.getenv("LINKEDIN_COMPANY_NAME", "Invory")  # Unternehmensname für automatische ID-Suche

# Website URLs für Recherche
INVORY_URL = "https://invory.de"
EINVOICEHUB_URL = "https://einvoicehub.de"

# OpenAI/LangChain Konfiguration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4-turbo-preview")

# Anthropic/Claude Konfiguration für Review Agent
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
ANTHROPIC_MODEL = os.getenv("ANTHROPIC_MODEL", "claude-3-sonnet-20240229")

# DALL-E 3 Konfiguration für Bildgenerierung
DALLE_MODEL = "dall-e-3"
DALLE_QUALITY = "standard"  # "standard" oder "hd"
DALLE_SIZE = "1024x1024"    # LinkedIn empfiehlt 1200x627, aber 1024x1024 ist universeller

# XRechnung Themen
XRECHNUNG_TOPICS = [
    "XRechnung Standard",
    "Digitale Rechnungsstellung", 
    "E-Invoicing",
    "ZUGFeRD",
    "Automatisierung Rechnungswesen",
    "Compliance XRechnung",
    "Rechnungsbearbeitung",
    "Prozessautomatisierung"
]

# einvoicehub-App Features von Invory
EINVOICEHUB_FEATURES = {
    "rechnungseingang": {
        "name": "Rechnungseingang",
        "features": [
            "Direkter Upload (PDF/XML/ZIP) im Browser",
            "E-Mail-Eingang: automatische Verarbeitung von Mail-Anhängen", 
            "Ordner-Watcher (Client-Tool): überwacht lokale/vernetzte Ordner",
            "API-Upload (POST /inbox/upload) mit Idempotenz (keine Duplikate)"
        ]
    },
    "validierung": {
        "name": "Validierung & Prüfung",
        "features": [
            "Automatische XRechnung/UBL-Prüfung nach Eingang",
            "Batch-Validierung mehrerer Dateien in einem Lauf",
            "Validergebnis mit verständlichen Hinweisen und Pflichtfeld-Checks"
        ]
    },
    "reports": {
        "name": "Reports & Ausgaben", 
        "features": [
            "CSV/PDF-Berichte pro Batch oder Zeitraum",
            "Signierte Reports (Integrität via SHA-256)",
            "Download von Artefakten (Original-PDF, erzeugtes UBL, CSV)"
        ]
    },
    "automatisierung": {
        "name": "Automatisierung & Integrationen",
        "features": [
            "Webhooks (Ereignisse wie validation.batch_created, validation.completed)",
            "API-Keys für Maschinenzugriff (Ausstellen/Rotieren/Listen)",
            "PEPPOL-Option (Senden/Empfangen via Adapter, wenn aktiviert)"
        ]
    },
    "dashboard": {
        "name": "Dashboard & Bedienung",
        "features": [
            "Übersicht über Eingänge, Status, Fehler, Batches",
            "Detailansicht je Rechnung inkl. Metadaten",
            "Suche/Filter (z.B. Zeitraum, Status, Quelle)"
        ]
    },
    "nutzung": {
        "name": "Nutzung & Limits",
        "features": [
            "Plan-basierte Kontingente (Free/Pro/Power)",
            "Hinweise bei Annäherung/Überschreitung (Usage-Notices)",
            "Monatliche Zähler je Account"
        ]
    },
    "sicherheit": {
        "name": "Sicherheit & Compliance",
        "features": [
            "Login via E-Mail/Passwort oder Google OAuth",
            "CSRF-Schutz für Browser, CORS korrekt konfiguriert",
            "JWT-Sessions, API-Key-Scopes, Audit-Logs",
            "Idempotenz-Schutz pro Account"
        ]
    },
    "abrechnung": {
        "name": "Abrechnung (Stripe)",
        "features": [
            "Self-Service Checkout & Kundenportal",
            "Plan-Wechsel/Upgrade jederzeit",
            "Webhooks für Billing-Events"
        ]
    },
    "entwickler": {
        "name": "Entwickler-Erlebnis",
        "features": [
            "OpenAPI-Doku (/docs, /redoc, /openapi.json)",
            "Beispiele (cURL, Postman), Sandbox-Flows",
            "Stabile IDs, Idempotenz-Header, klare Fehlercodes"
        ]
    }
}

# Highlight-Features für Posts (besonders interessant für LinkedIn)
EINVOICEHUB_HIGHLIGHTS = [
    "🚀 Automatische XRechnung/UBL-Prüfung",
    "📧 E-Mail-Eingang mit automatischer Verarbeitung", 
    "📊 Batch-Validierung mehrerer Dateien",
    "🔗 API-Integration mit Webhooks",
    "📱 Self-Service Dashboard",
    "🛡️ Enterprise-Sicherheit (OAuth, JWT, Audit-Logs)",
    "💰 Flexible Pläne (Free/Pro/Power)",
    "🔌 PEPPOL-Integration verfügbar",
    "📈 Signierte Reports mit SHA-256",
    "👩‍💻 OpenAPI-Dokumentation für Entwickler"
]

# XRechnung Countdown - wichtige Termine und Fristen
XRECHNUNG_MILESTONES = [
    {
        "date": "2025-01-01",
        "description": "XRechnung 3.0.2 wird Standard für Bundesverwaltung",
        "impact": "Alle Rechnungen an Bundesbehörden müssen XRechnung 3.0.2 entsprechen"
    },
    {
        "date": "2025-07-01", 
        "description": "Erweiterte PEPPOL-Pflicht für größere Unternehmen",
        "impact": "Unternehmen ab 500 Mitarbeitern müssen PEPPOL-fähig sein"
    },
    {
        "date": "2026-01-01",
        "description": "XRechnung-Pflicht für alle B2B-Rechnungen geplant",
        "impact": "Diskussion um Ausweitung auf den privaten Sektor"
    },
    {
        "date": "2026-07-01",
        "description": "EU-weite E-Invoicing-Harmonisierung Zieltermin",
        "impact": "Einheitliche Standards in der gesamten EU"
    }
]

# News-Quellen für XRechnung-Recherche (ausgenommen invory/einvoicehub)
XRECHNUNG_NEWS_SOURCES = [
    "https://www.bundesfinanzministerium.de",
    "https://www.xrechnung.org", 
    "https://www.peppol.org",
    "https://www.bitkom.org",
    "https://www.handelsblatt.com",
    "https://www.computerwoche.de",
    "https://www.it-finanzmagazin.de",
    "https://www.ferd-net.de"
]

# Allgemeine XRechnung-Keywords für News-Suche
XRECHNUNG_KEYWORDS = [
    "XRechnung",
    "E-Invoicing",
    "ZUGFeRD", 
    "PEPPOL",
    "elektronische Rechnung",
    "digitale Rechnungsstellung",
    "E-Rechnungsverordnung",
    "UBL Standard",
    "Factur-X"
]

# Storytelling Templates
STORYTELLING_STRUCTURES = [
    {
        "name": "Hero's Journey",
        "structure": "Ein Unternehmen steht vor einer großen Herausforderung → Sie entdecken XRechnung als Lösung → Nach Hindernissen erreichen sie den Erfolg",
        "tone": "motivierend, inspirierend"
    },
    {
        "name": "Problem-Solution",
        "structure": "Alltagsproblem schildern → XRechnung als elegante Lösung vorstellen → Transformation zeigen",
        "tone": "praktisch, lösungsorientiert"
    },
    {
        "name": "Future Vision",
        "structure": "Blick in die Zukunft der digitalen Rechnungsstellung → Countdown zu Deadlines → Handlungsaufruf",
        "tone": "visionär, dringlich"
    },
    {
        "name": "Behind the Scenes",
        "structure": "Einblick in die Entwicklung/Arbeit bei Invory → XRechnung-Expertise → Community-Aspekt",
        "tone": "persönlich, authentisch"
    }
]

# Comic-Style Bild-Prompts für DALL-E 3
IMAGE_STYLE_PROMPTS = [
    "friendly cartoon style, flat design, business illustration",
    "comic book style, colorful, professional but approachable",
    "minimal vector art, modern illustration, business theme",
    "isometric illustration style, clean lines, tech-savvy look",
    "hand-drawn illustration style, warm colors, business setting"
]

# XRechnung-spezifische Bildmotive
XRECHNUNG_IMAGE_THEMES = [
    "digitale Transformation: Papierrechnungen werden zu digitalen Dokumenten",
    "Zeitersparnis: Uhr mit sich beschleunigenden Zeigern, effiziente Prozesse",
    "Automatisierung: Roboter und Menschen arbeiten harmonisch zusammen",
    "Compliance: Schild oder Häkchen symbolisiert erfüllte Anforderungen", 
    "Countdown: Kalender oder Timer zeigt nahende Deadlines",
    "Erfolgsgeschichte: Unternehmen celebrates digitalen Wandel",
    "Problemlösung: Komplexe Prozesse werden vereinfacht dargestellt",
    "Zukunftsvision: moderne digitale Bürolandschaft"
]

# Post-Einstellungen
POST_FREQUENCY = os.getenv("POST_FREQUENCY", "daily")  # daily, weekly, custom
POST_TIME = os.getenv("POST_TIME", "09:00")  # HH:MM Format
MAX_POST_LENGTH = 3000  # LinkedIn Post Max Length
INCLUDE_IMAGES = os.getenv("INCLUDE_IMAGES", "true").lower() == "true"  # Bilder aktivieren/deaktivieren

# Agent Konfiguration
AGENT_TEMPERATURE = 0.7
AGENT_MAX_ITERATIONS = 10

