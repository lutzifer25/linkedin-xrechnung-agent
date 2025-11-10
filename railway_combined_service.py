"""
Railway Combined Service
Kombiniert OAuth Handler und LinkedIn Post Scheduler für Railway Deployment
"""
import os
import sys
import threading
import time
import logging
from datetime import datetime
from flask import Flask, request, render_template_string
from scheduler import PostScheduler

# Logging konfigurieren
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# OAuth HTML Template
OAUTH_SUCCESS_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>LinkedIn OAuth Erfolg</title>
    <style>
        body { font-family: Arial, sans-serif; text-align: center; padding: 50px; }
        .container { max-width: 600px; margin: 0 auto; }
        .success { color: #28a745; }
        .code-box { 
            background-color: #f8f9fa; 
            padding: 20px; 
            border-radius: 5px; 
            font-family: monospace; 
            word-break: break-all;
            margin: 20px 0;
        }
        button { 
            padding: 10px 20px; 
            background-color: #007bff; 
            color: white; 
            border: none; 
            border-radius: 5px; 
            cursor: pointer; 
        }
    </style>
</head>
<body>
    <div class="container">
        <h1 class="success">✅ LinkedIn OAuth Erfolgreich!</h1>
        <p>Die Autorisierung war erfolgreich. Kopieren Sie den folgenden Code:</p>
        <div class="code-box" id="authCode">{{ auth_code }}</div>
        <button onclick="copyToClipboard()">📋 Code kopieren</button>
        <p><small>Verwenden Sie diesen Code in Ihrem Terminal/System.</small></p>
    </div>
    
    <script>
        function copyToClipboard() {
            const code = document.getElementById('authCode').innerText;
            navigator.clipboard.writeText(code).then(() => {
                alert('✅ Code in Zwischenablage kopiert!');
            });
        }
    </script>
</body>
</html>
"""

# Global scheduler instance
scheduler_instance = None
scheduler_thread = None

@app.route('/auth/callback')
def oauth_callback():
    """OAuth callback endpoint für LinkedIn"""
    code = request.args.get('code')
    error = request.args.get('error')
    
    if error:
        logger.error(f"OAuth Fehler: {error}")
        return f"❌ OAuth Fehler: {error}", 400
    
    if code:
        logger.info(f"✅ OAuth Code erhalten: {code[:20]}...")
        return render_template_string(OAUTH_SUCCESS_HTML, auth_code=code)
    
    return "❌ Kein Authorization Code erhalten", 400

@app.route('/health')
def health_check():
    """Health check endpoint"""
    status = {
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'oauth_handler': 'active',
        'scheduler': 'active' if scheduler_instance and scheduler_instance.is_running else 'inactive'
    }
    return status

@app.route('/scheduler/status')
def scheduler_status():
    """Scheduler status endpoint"""
    if scheduler_instance:
        return {
            'running': scheduler_instance.is_running,
            'timestamp': datetime.now().isoformat()
        }
    return {'running': False, 'message': 'Scheduler not initialized'}

@app.route('/scheduler/start')
def start_scheduler():
    """Startet den Scheduler manuell"""
    global scheduler_instance, scheduler_thread
    
    try:
        if not scheduler_instance or not scheduler_instance.is_running:
            scheduler_instance = PostScheduler()
            
            def run_scheduler():
                logger.info("🚀 Starte LinkedIn Post Scheduler...")
                scheduler_instance.run()
            
            scheduler_thread = threading.Thread(target=run_scheduler, daemon=True)
            scheduler_thread.start()
            
            logger.info("✅ Scheduler gestartet")
            return {'status': 'started', 'timestamp': datetime.now().isoformat()}
        else:
            return {'status': 'already_running', 'timestamp': datetime.now().isoformat()}
    
    except Exception as e:
        logger.error(f"❌ Scheduler Start Fehler: {str(e)}")
        return {'status': 'error', 'message': str(e)}, 500

@app.route('/scheduler/stop')
def stop_scheduler():
    """Stoppt den Scheduler"""
    global scheduler_instance
    
    try:
        if scheduler_instance and scheduler_instance.is_running:
            scheduler_instance.stop()
            logger.info("⏹️ Scheduler gestoppt")
            return {'status': 'stopped', 'timestamp': datetime.now().isoformat()}
        else:
            return {'status': 'not_running', 'timestamp': datetime.now().isoformat()}
    
    except Exception as e:
        logger.error(f"❌ Scheduler Stop Fehler: {str(e)}")
        return {'status': 'error', 'message': str(e)}, 500

@app.route('/')
def index():
    """Hauptseite mit System-Übersicht"""
    return """
    <h1>🚀 LinkedIn XRechnung Agent - Railway Service</h1>
    <h2>📋 Verfügbare Endpunkte:</h2>
    <ul>
        <li><a href="/health">🏥 Health Check</a></li>
        <li><a href="/scheduler/status">📊 Scheduler Status</a></li>
        <li><a href="/scheduler/start">▶️ Scheduler starten</a></li>
        <li><a href="/scheduler/stop">⏹️ Scheduler stoppen</a></li>
        <li><a href="/auth/callback">🔐 OAuth Callback</a></li>
    </ul>
    <hr>
    <p><strong>🎯 System:</strong> LinkedIn XRechnung Agent Multi-Agent System</p>
    <p><strong>☁️ Platform:</strong> Railway Cloud Deployment</p>
    <p><strong>⏰ Schedule:</strong> Täglich um 09:00 Uhr</p>
    """

def initialize_scheduler():
    """Initialisiert den Scheduler beim Start"""
    global scheduler_instance, scheduler_thread
    
    # Prüfe ob Auto-Start aktiviert ist
    auto_start = os.getenv('AUTO_START_SCHEDULER', 'true').lower() == 'true'
    
    if auto_start:
        logger.info("🔄 Auto-Start Scheduler aktiviert")
        try:
            scheduler_instance = PostScheduler()
            
            def run_scheduler():
                logger.info("🚀 Starte LinkedIn Post Scheduler (Auto-Start)...")
                scheduler_instance.run()
            
            scheduler_thread = threading.Thread(target=run_scheduler, daemon=True)
            scheduler_thread.start()
            
            logger.info("✅ Scheduler automatisch gestartet")
        
        except Exception as e:
            logger.error(f"❌ Auto-Start Fehler: {str(e)}")
    else:
        logger.info("ℹ️ Auto-Start Scheduler deaktiviert - manueller Start über /scheduler/start")

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    
    logger.info("🚀 Starte LinkedIn XRechnung Agent Railway Service")
    logger.info(f"🌐 Port: {port}")
    
    # Initialisiere Scheduler
    initialize_scheduler()
    
    # Starte Flask App
    app.run(host='0.0.0.0', port=port, debug=False)