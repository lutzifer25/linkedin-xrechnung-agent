# GitHub Repository Setup

## 🚀 Repository auf GitHub erstellen

### Schritt 1: GitHub Repository erstellen

1. **Gehen Sie zu GitHub**:
   - Besuchen Sie: https://github.com/new
   - Melden Sie sich an

2. **Repository erstellen**:
   - **Repository name**: `linkedin-xrechnung-agent` (oder gewünschter Name)
   - **Description**: "Multi-Agent System für automatische LinkedIn-Posts zu XRechnung"
   - **Visibility**: Private (empfohlen) oder Public
   - **Initialize**: NICHT aktivieren (Repository ist bereits initialisiert)
   - Klicken Sie auf "Create repository"

### Schritt 2: Repository mit GitHub verbinden

```bash
# Fügen Sie GitHub als Remote hinzu
git remote add origin https://github.com/IHR_USERNAME/linkedin-xrechnung-agent.git

# Oder mit SSH (falls SSH-Keys konfiguriert):
# git remote add origin git@github.com:IHR_USERNAME/linkedin-xrechnung-agent.git

# Überprüfen Sie die Remote-URL
git remote -v

# Pushen Sie den Code zu GitHub
git branch -M main
git push -u origin main
```

### Schritt 3: Überprüfen

1. Gehen Sie zu Ihrem GitHub-Repository
2. Überprüfen Sie, dass alle Dateien hochgeladen wurden
3. Stellen Sie sicher, dass `.env` NICHT im Repository ist (sollte in `.gitignore` sein)

## 🔒 Wichtige Sicherheitshinweise

### ✅ Was sollte NICHT im Repository sein:

- ❌ `.env` Datei (enthält API-Keys)
- ❌ API-Keys oder Secrets
- ❌ Credentials
- ❌ Private Daten

### ✅ Was sollte im Repository sein:

- ✅ `README.md`
- ✅ `requirements.txt`
- ✅ Alle Python-Dateien
- ✅ Konfigurationsdateien (ohne Secrets)
- ✅ Dokumentation
- ✅ `.gitignore` (sehr wichtig!)

## 📋 Checkliste vor dem Push

- [ ] `.env` ist in `.gitignore`
- [ ] Alle API-Keys sind entfernt
- [ ] `README.md` ist vorhanden
- [ ] `requirements.txt` ist aktuell
- [ ] `.gitignore` enthält alle notwendigen Einträge
- [ ] Keine sensiblen Daten im Code

## 🚀 Nach dem Push: Cloud-Deployment

Nachdem das Repository auf GitHub ist, können Sie:

1. **Railway**: Repository verbinden und deployen
2. **Render**: Repository verbinden und deployen
3. **AWS Lambda**: Code aus Repository deployen

## 🔍 Repository-Struktur

```
linkedin-xrechnung-agent/
├── agents/
│   ├── research_agent.py
│   ├── content_agent.py
│   └── review_agent.py
├── services/
│   ├── invory_client.py
│   ├── einvoicehub_client.py
│   └── linkedin_client.py
├── config.py
├── main.py
├── scheduler.py
├── multi_agent_system.py
├── requirements.txt
├── README.md
├── .gitignore
├── railway.json
├── render.yaml
└── lambda_function.py
```

## 💡 Nützliche Git-Befehle

```bash
# Status überprüfen
git status

# Änderungen hinzufügen
git add .

# Committen
git commit -m "Beschreibung der Änderungen"

# Zu GitHub pushen
git push

# Neueste Änderungen von GitHub holen
git pull

# Branch erstellen
git checkout -b feature/neue-funktion

# Branch wechseln
git checkout main
```

## 🆘 Troubleshooting

### Problem: "Permission denied"
- **Lösung**: Überprüfen Sie Ihre GitHub-Credentials
- **Lösung**: Verwenden Sie Personal Access Token statt Passwort

### Problem: ".env wurde committed"
- **Lösung**: 
  ```bash
  git rm --cached .env
  git commit -m "Remove .env from repository"
  git push
  ```
- **Wichtig**: Rotieren Sie alle API-Keys, die im Repository waren!

### Problem: "Remote already exists"
- **Lösung**: 
  ```bash
  git remote remove origin
  git remote add origin YOUR_REPO_URL
  ```

## 📚 Weitere Ressourcen

- GitHub Docs: https://docs.github.com/
- Git Docs: https://git-scm.com/doc
- GitHub CLI: https://cli.github.com/

