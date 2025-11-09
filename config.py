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

# Post-Einstellungen
POST_FREQUENCY = os.getenv("POST_FREQUENCY", "daily")  # daily, weekly, custom
POST_TIME = os.getenv("POST_TIME", "09:00")  # HH:MM Format
MAX_POST_LENGTH = 3000  # LinkedIn Post Max Length

# Agent Konfiguration
AGENT_TEMPERATURE = 0.7
AGENT_MAX_ITERATIONS = 10

