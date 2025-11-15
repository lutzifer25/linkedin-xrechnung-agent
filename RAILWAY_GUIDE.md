# 🚀 Railway Deployment Guide

## Schnell-Deployment für LinkedIn XRechnung Agent

### 1. Railway Project Setup
- Gehe zu https://railway.app/dashboard
- Erstelle neues Project
- Verbinde mit GitHub: `lutzifer25/linkedin-xrechnung-agent`

### 2. Environment Variables setzen
Kopiere alle Werte aus deiner lokalen `.env` in Railway Settings:

```
LINKEDIN_CLIENT_ID
LINKEDIN_CLIENT_SECRET  
LINKEDIN_ACCESS_TOKEN
LINKEDIN_COMPANY_NAME=Invory
LINKEDIN_REDIRECT_URI=https://[APP-NAME].up.railway.app/auth/callback

OPENAI_API_KEY
OPENAI_MODEL=gpt-4-turbo-preview

ANTHROPIC_API_KEY
ANTHROPIC_MODEL=claude-3-sonnet-20240229

POST_FREQUENCY=daily
POST_TIME=09:00
INCLUDE_IMAGES=true
AUTO_START_SCHEDULER=true
PORT=8000
```

### 3. Deploy & Test
- Railway deployt automatisch mit `python3 railway_combined_service.py`
- Health Check: `https://[APP].up.railway.app/`
- Status Check: `https://[APP].up.railway.app/status`

✅ **Scheduler postet täglich um 09:00 automatisch!**