# Deployment Guide für Cloud-Hosting

## 🚀 Schnellstart: Railway (Empfohlen)

### Schritt 1: GitHub Repository vorbereiten
```bash
# Stellen Sie sicher, dass alle Dateien committed sind
git add .
git commit -m "Prepare for deployment"
git push
```

### Schritt 2: Railway Account erstellen
1. Gehen Sie zu https://railway.app/
2. Melden Sie sich mit GitHub an
3. Klicken Sie auf "New Project"
4. Wählen Sie "Deploy from GitHub repo"
5. Wählen Sie Ihr Repository aus

### Schritt 3: Umgebungsvariablen setzen
1. Gehen Sie zu "Variables" in Ihrem Projekt
2. Fügen Sie folgende Variablen hinzu:
   - `OPENAI_API_KEY` - Ihr OpenAI API Key
   - `LINKEDIN_ACCESS_TOKEN` - LinkedIn Access Token
   - `LINKEDIN_CLIENT_ID` - LinkedIn Client ID (optional)
   - `LINKEDIN_CLIENT_SECRET` - LinkedIn Client Secret (optional)
   - `LINKEDIN_COMPANY_NAME` - "Invory" (Standard)
   - `POST_FREQUENCY` - "daily" (Standard)
   - `POST_TIME` - "09:00" (Standard)

### Schritt 4: Deployment konfigurieren
1. Railway erkennt automatisch `railway.json`
2. Start Command wird automatisch auf `python3 scheduler.py` gesetzt
3. Deploy startet automatisch

### Schritt 5: Cron Job einrichten
1. Gehen Sie zu "Settings" → "Cron"
2. Fügen Sie einen Cron Job hinzu:
   - **Schedule**: `0 9 * * *` (täglich um 9 Uhr UTC)
   - **Command**: `python3 main.py --mode post`

### Schritt 6: Überwachen
- Gehen Sie zu "Deployments" um Logs zu sehen
- Überprüfen Sie die Logs auf Fehler

## 🚀 Schnellstart: Render

### Schritt 1: Render Account erstellen
1. Gehen Sie zu https://render.com/
2. Melden Sie sich an
3. Klicken Sie auf "New +" → "Web Service"

### Schritt 2: Repository verbinden
1. Verbinden Sie Ihr GitHub-Repository
2. Render erkennt automatisch `render.yaml`
3. Wählen Sie "Free" Plan

### Schritt 3: Umgebungsvariablen
1. Gehen Sie zu "Environment"
2. Fügen Sie alle Variablen hinzu (siehe Railway Schritt 3)

### Schritt 4: Deploy
1. Render deployt automatisch
2. Der Service startet mit `python3 scheduler.py`

### Schritt 5: Cron Job
1. Gehen Sie zu "Cron Jobs"
2. Erstellen Sie einen neuen Cron Job:
   - **Schedule**: `0 9 * * *`
   - **Command**: `python3 main.py --mode post`

## 🚀 Schnellstart: AWS Lambda (Serverless)

### Schritt 1: Lambda Function erstellen
1. Gehen Sie zu AWS Lambda Console
2. Klicken Sie auf "Create function"
3. Wählen Sie "Author from scratch"
4. Name: `linkedin-post-agent`
5. Runtime: Python 3.11
6. Klicken Sie auf "Create function"

### Schritt 2: Code hochladen
1. Erstellen Sie ein Deployment Package:
```bash
# Installiere Dependencies
pip install -r requirements.txt -t .

# Erstelle ZIP
zip -r lambda-deployment.zip . -x "*.git*" -x "*.md" -x "test_*" -x "*.pyc" "__pycache__/*"
```

2. Laden Sie `lambda-deployment.zip` in Lambda hoch

### Schritt 3: Umgebungsvariablen
1. Gehen Sie zu "Configuration" → "Environment variables"
2. Fügen Sie alle Variablen hinzu

### Schritt 4: EventBridge Rule (Cron)
1. Gehen Sie zu EventBridge → Rules
2. Erstellen Sie eine neue Rule:
   - **Name**: `linkedin-post-daily`
   - **Schedule expression**: `cron(0 9 * * ? *)`
   - **Target**: Wählen Sie Ihre Lambda Function
3. Klicken Sie auf "Create"

### Schritt 5: IAM Permissions
1. Stellen Sie sicher, dass Lambda die nötigen Permissions hat
2. Fügen Sie EventBridge als Trigger hinzu

## 📋 Umgebungsvariablen Checkliste

### Erforderlich:
- ✅ `OPENAI_API_KEY` - OpenAI API Key
- ✅ `LINKEDIN_ACCESS_TOKEN` - LinkedIn Access Token

### Optional:
- `LINKEDIN_CLIENT_ID` - Für Token-Refresh
- `LINKEDIN_CLIENT_SECRET` - Für Token-Refresh
- `LINKEDIN_ORGANIZATION_ID` - Wird automatisch abgerufen
- `LINKEDIN_COMPANY_NAME` - "Invory" (Standard)
- `POST_FREQUENCY` - "daily" (Standard)
- `POST_TIME` - "09:00" (Standard)
- `OPENAI_MODEL` - "gpt-4-turbo-preview" (Standard)

## 🔍 Troubleshooting

### Problem: Service startet nicht
- **Lösung**: Überprüfen Sie die Logs
- **Lösung**: Stellen Sie sicher, dass alle Dependencies installiert sind
- **Lösung**: Überprüfen Sie die Start Command

### Problem: Cron Job läuft nicht
- **Lösung**: Überprüfen Sie die Cron-Syntax
- **Lösung**: Stellen Sie sicher, dass die Zeitzone korrekt ist (UTC)
- **Lösung**: Überprüfen Sie die Logs

### Problem: API-Fehler
- **Lösung**: Überprüfen Sie die API-Keys
- **Lösung**: Stellen Sie sicher, dass die Umgebungsvariablen korrekt gesetzt sind
- **Lösung**: Überprüfen Sie die API-Quotas

### Problem: Organization ID nicht gefunden
- **Lösung**: Das System versucht automatisch, die ID zu finden
- **Lösung**: Stellen Sie sicher, dass der Access Token Administrator-Berechtigungen hat
- **Lösung**: Setzen Sie `LINKEDIN_ORGANIZATION_ID` manuell

## 📊 Monitoring

### Railway:
- Gehen Sie zu "Deployments" für Logs
- Überwachen Sie die Metriken im Dashboard

### Render:
- Gehen Sie zu "Logs" für Live-Logs
- Überwachen Sie die Metriken

### AWS Lambda:
- Gehen Sie zu CloudWatch für Logs
- Erstellen Sie Alarms für Fehler

## 🔒 Sicherheit

1. **Niemals API-Keys in Git committen**
2. **Verwenden Sie immer Umgebungsvariablen**
3. **Rotieren Sie API-Keys regelmäßig**
4. **Überwachen Sie die Logs auf verdächtige Aktivitäten**
5. **Verwenden Sie least-privilege Permissions**

## 💰 Kostenoptimierung

### Railway:
- Nutzen Sie den Free Tier (500h/Monat)
- Optimieren Sie die Ausführungszeit

### Render:
- Nutzen Sie den Free Tier
- Services schlafen nach Inaktivität (OK für Cron Jobs)

### AWS Lambda:
- Nutzen Sie den Free Tier (1M Requests/Monat)
- Optimieren Sie die Lambda-Funktion
- Verwenden Sie Provisioned Concurrency nur wenn nötig

## 🎯 Best Practices

1. **Testen Sie lokal vor dem Deployment**
2. **Verwenden Sie Preview-Modus zuerst**
3. **Überwachen Sie die ersten Deployments**
4. **Setzen Sie Alerts für Fehler**
5. **Dokumentieren Sie Änderungen**
6. **Backup wichtige Daten**

## 📚 Weitere Ressourcen

- Railway Docs: https://docs.railway.app/
- Render Docs: https://render.com/docs
- AWS Lambda Docs: https://docs.aws.amazon.com/lambda/
- EventBridge Docs: https://docs.aws.amazon.com/eventbridge/

