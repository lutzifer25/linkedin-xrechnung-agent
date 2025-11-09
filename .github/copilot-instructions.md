# Copilot-Anweisungen für LinkedIn XRechnung Agent

## Architektur-Übersicht

Dieses System implementiert ein **Multi-Agent-Framework** mit drei spezialisierten Agents für automatische LinkedIn-Post-Erstellung zu XRechnung-Themen. Die Architektur folgt einer klaren Trennung zwischen Agents (Geschäftslogik) und Services (externe Integrationen).

### Kernkomponenten

- **`multi_agent_system.py`**: Orchestrator für den kompletten Workflow
- **`agents/`**: Drei spezialisierte CrewAI Agents (Research, Content, Review)
- **`services/`**: External API Clients (LinkedIn, Web-Scraping für invory.de/einvoicehub.de)
- **`main.py`**: CLI mit drei Modi (`preview`, `post`, `schedule`)

## Wichtige Patterns

### Multi-Agent Workflow
Alle Funktionalität läuft über `LinkedInPostMultiAgentSystem`:
```python
# Standard-Flow: Research → Content → Review → Optional Post
system = LinkedInPostMultiAgentSystem()
result = system.create_and_post(topic="XRechnung", auto_post=False)
```

### Web-Scraping Pattern
Services nutzen BeautifulSoup für automatische Website-Analyse:
- `InvoryClient`: Scrapt invory.de ohne API-Keys
- `EinvoiceHubClient`: Scrapt einvoicehub.de mit Fallback auf Mock-Daten

### LinkedIn API Auto-Discovery
`LinkedInClient` ermittelt automatisch Organization IDs basierend auf Unternehmensname ("Invory") falls nicht in `.env` konfiguriert.

## Entwickler-Workflows

### Lokales Testing
```bash
# Preview-Modus (sicherster Test)
python main.py --mode preview --topic "XRechnung Standard"

# Test-Suite für alle Komponenten
python test_system.py
```

### Configuration Management
- **Alle Credentials** in `.env` (nie committen!)
- **XRechnung-Themen** in `config.py` anpassbar
- **Auto-Fallbacks** bei fehlenden API-Keys (Mock-Daten für Web-Scraping)

### Production Deployment
```bash
# Automatischer Scheduler mit konfigurierbaren Intervallen
python main.py --mode schedule --frequency daily --time 09:00
```

## Kritische Integration Points

### CrewAI Agent Initialization
Alle Agents erben von `crewai.Agent` mit spezifischen `role`, `goal`, `backstory`. LLM-Integration über direkten Model-String (CrewAI 1.4+ Pattern).

### LinkedIn Organization ID Workflow
1. Prüfung `LINKEDIN_ORGANIZATION_ID` in .env
2. Fallback: API-Call zur Auto-Ermittlung via Unternehmensname
3. Manuelle Konfiguration als letzte Option

### Error Handling Strategy
- **Web-Scraping**: Graceful degradation zu Mock-Daten
- **LinkedIn API**: Detailliertes Error-Logging mit spezifischen Fehlercodes
- **Agent-Failures**: Continuation mit besten verfügbaren Daten

## Spezifische Konventionen

### XRechnung Domain Logic
- Themen-Templates in `XRECHNUNG_TOPICS` (config.py)
- Automatische Link-Integration zu invory.de/einvoicehub.de in allen Posts
- 3000 Zeichen LinkedIn-Limit enforcement

### File Organization
- **Agents**: CrewAI base class with `llm=OPENAI_MODEL` string (CrewAI 1.4+)
- **Services**: Pure Python classes, external API wrappers
- **Tests**: Separate test methods per component in `test_system.py`

### Environment Variables Pattern
```python
# Standard Pattern für alle configs
SETTING = os.getenv("SETTING", "default_value")
```

## Dependencies & Versions
- **CrewAI >=0.70.0**: Multi-Agent orchestration framework
- **LangChain >=0.2.0 + OpenAI >=1.35.0**: LLM integration
- **BeautifulSoup4**: Web scraping
- **requests**: HTTP clients
- **python-dotenv**: Environment management

Beim Hinzufügen neuer Features: Folge dem Agent/Service-Pattern, nutze die existierenden Mock-Data-Fallbacks, und teste immer zuerst im Preview-Modus.