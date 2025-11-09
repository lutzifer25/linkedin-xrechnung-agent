# LinkedIn Post Multi-Agent System für XRechnung

Automatisches Multi-Agent System zur Erstellung und Veröffentlichung von LinkedIn-Posts zum Thema XRechnung mit Web-Recherche auf invory.de und einvoicehub.de.

## 🎯 Features

- **Multi-Agent System**: Drei spezialisierte Agents für Recherche, Content-Erstellung und Review
- **XRechnung-Fokus**: Spezialisiert auf Themen rund um XRechnung und E-Invoicing
- **Web-Recherche**: Automatische Untersuchung von invory.de und einvoicehub.de durch Web-Scraping
- **Link-Integration**: Automatische Einbindung von Links zu invory.de und einvoicehub.de in Posts
- **LinkedIn Integration**: Automatisches Posting auf LinkedIn
- **Automatisches Scheduling**: Zeitgesteuerte Erstellung und Veröffentlichung von Posts
- **Qualitätsprüfung**: Automatische Review und Verbesserung von Posts

## 🏗️ Architektur

### Agents

1. **Research Agent**: Recherchiert aktuelle Informationen zu XRechnung-Themen durch Untersuchung von invory.de und einvoicehub.de
2. **Content Agent**: Erstellt ansprechende LinkedIn-Posts basierend auf Recherche mit Links zu beiden Websites
3. **Review Agent**: Prüft und verbessert Posts auf Qualität und Compliance

### Services

- **InvoryClient**: Web-Scraping Client für invory.de (kein API-Key erforderlich)
- **EinvoiceHubClient**: Web-Scraping Client für einvoicehub.de
- **LinkedInClient**: Integration mit LinkedIn API für Posting

## 📋 Voraussetzungen

- Python 3.8+
- LinkedIn API Zugriff (Organization Account)
- OpenAI API Key (für LLM-Funktionalität)
- Internetverbindung (für Web-Recherche auf invory.de und einvoicehub.de)

## 🚀 Installation

1. **Repository klonen oder Projekt erstellen**

2. **Abhängigkeiten installieren**:
```bash
pip install -r requirements.txt
```

3. **Umgebungsvariablen konfigurieren**:
```bash
cp .env.example .env
# Bearbeite .env und füge deine API-Keys ein
```

4. **LinkedIn API Setup** (Dynamisch zur Laufzeit):
   - Erstelle eine LinkedIn App unter https://www.linkedin.com/developers/
   - Füge **nur** Client ID und Client Secret in `.env` ein:
   ```bash
   LINKEDIN_CLIENT_ID=your_client_id
   LINKEDIN_CLIENT_SECRET=your_client_secret
   ```
   - **🔥 Neu: Automatische Authentifizierung zur Laufzeit!**
     - Access Token und Organization ID werden **automatisch geholt** wenn Sie die App starten
     - Keine manuelle Token-Verwaltung mehr nötig
     - Sicherer: Keys werden nicht permanent gespeichert
   - Optional: `LINKEDIN_COMPANY_NAME` in `.env` setzen (Standard: "Invory")

5. **OpenAI API Setup**:
   - Erstelle einen OpenAI API Key unter https://platform.openai.com/
   - Füge den Key in `.env` ein

6. **Web-Recherche Setup**:
   - Keine zusätzliche Konfiguration erforderlich
   - Das System untersucht automatisch invory.de und einvoicehub.de
   - Bei Fehlern werden Mock-Daten verwendet

## 💻 Verwendung

### Preview-Modus (Empfohlen für Tests)

Erstellt einen Post-Preview ohne zu posten:

```bash
python main.py --mode preview
```

Mit spezifischem Thema:

```bash
python main.py --mode preview --topic "XRechnung Standard"
```

### Post-Modus

Erstellt und postet sofort auf LinkedIn:

```bash
python main.py --mode post
```

### Schedule-Modus

Startet den automatischen Scheduler:

```bash
python main.py --mode schedule --frequency daily --time 09:00
```

Verfügbare Frequenzen:
- `daily`: Täglich um die angegebene Zeit
- `weekly`: Wöchentlich (Montags) um die angegebene Zeit
- `custom`: Montag, Mittwoch, Freitag um die angegebene Zeit

## 📁 Projektstruktur

```
.
├── agents/
│   ├── __init__.py
│   ├── research_agent.py      # Research Agent
│   ├── content_agent.py       # Content Agent
│   └── review_agent.py        # Review Agent
├── services/
│   ├── __init__.py
│   ├── invory_client.py       # Invory.de Web-Scraping Client
│   ├── einvoicehub_client.py  # EinvoiceHub Web-Scraping Client
│   └── linkedin_client.py     # LinkedIn API Client
├── config.py                  # Konfiguration
├── multi_agent_system.py      # Multi-Agent System
├── scheduler.py               # Scheduler für automatische Posts
├── main.py                    # Hauptskript
├── requirements.txt           # Python Abhängigkeiten
├── .env.example              # Beispiel Umgebungsvariablen
└── README.md                 # Diese Datei
```

## 🔧 Konfiguration

### XRechnung-Themen

Die verfügbaren Themen können in `config.py` angepasst werden:

```python
XRECHNUNG_TOPICS = [
    "XRechnung Standard",
    "Digitale Rechnungsstellung",
    "E-Invoicing",
    # ... weitere Themen
]
```

### Post-Einstellungen

In `config.py` oder `.env`:

- `POST_FREQUENCY`: Häufigkeit (daily, weekly, custom)
- `POST_TIME`: Zeit für Posts (HH:MM Format)
- `MAX_POST_LENGTH`: Maximale Post-Länge (Standard: 3000 Zeichen)

## 🔐 Sicherheit

- **Niemals API-Keys in Git committen**
- Verwende `.env` für sensitive Daten
- Stelle sicher, dass `.env` in `.gitignore` ist
- Verwende sichere Access Tokens mit begrenzten Berechtigungen

## 🐛 Troubleshooting

### LinkedIn API Fehler

- Überprüfe, ob der Access Token gültig ist
- **Organization ID wird automatisch abgerufen**: Das System sucht automatisch nach der Organization ID für "Invory"
- Falls automatischer Abruf fehlschlägt:
  - Stelle sicher, dass der Access Token Administrator-Berechtigungen für die Unternehmensseite hat
  - Setze `LINKEDIN_ORGANIZATION_ID` manuell in der `.env`-Datei
  - Überprüfe, ob `LINKEDIN_COMPANY_NAME` korrekt gesetzt ist (Standard: "Invory")
- Prüfe die LinkedIn API Berechtigungen:
  - `r_organization_social` - Für das Posten auf Unternehmensseiten
  - `w_organization_social` - Für das Erstellen von Posts
  - `r_basicprofile` - Für das Abrufen von Profilinformationen

### Web-Recherche Fehler

- Falls Web-Scraping fehlschlägt, werden Mock-Daten verwendet
- Überprüfe die Internetverbindung
- Stelle sicher, dass invory.de und einvoicehub.de erreichbar sind

### OpenAI API Fehler

- Überprüfe den API Key
- Stelle sicher, dass ausreichend Credits vorhanden sind
- Prüfe die Rate Limits

## 📝 Lizenz

Dieses Projekt ist für den internen Gebrauch bestimmt.

## 🤝 Beitragen

Bei Fragen oder Problemen erstelle bitte ein Issue oder kontaktiere das Entwicklungsteam.

## 📞 Support

Für Support oder Fragen:
- Invory.de: https://invory.de
- EinvoiceHub: https://einvoicehub.de
- LinkedIn API Dokumentation: https://docs.microsoft.com/en-us/linkedin/

## 🔍 Wie es funktioniert

1. **Recherche**: Der Research Agent untersucht automatisch die Webseiten invory.de und einvoicehub.de durch Web-Scraping
2. **Content-Erstellung**: Der Content Agent erstellt relevante Posts basierend auf den gefundenen Informationen
3. **Link-Einbindung**: Links zu beiden Websites werden automatisch in die Posts eingebunden
4. **Review**: Der Review Agent prüft die Qualität der Posts
5. **Posting**: Bei Genehmigung werden die Posts auf LinkedIn veröffentlicht

