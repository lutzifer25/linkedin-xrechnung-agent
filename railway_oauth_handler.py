"""
Railway OAuth Callback Handler
Erstellt einen einfachen Web-Server für LinkedIn OAuth Callbacks auf Railway
"""
from flask import Flask, request, jsonify, render_template_string
import os
import logging
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# HTML Template für OAuth Success Page
OAUTH_SUCCESS_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>LinkedIn OAuth - Erfolgreich!</title>
    <meta charset="utf-8">
    <style>
        body { font-family: Arial, sans-serif; max-width: 600px; margin: 50px auto; padding: 20px; }
        .success { color: #28a745; }
        .code-box { background: #f8f9fa; padding: 15px; border-radius: 5px; font-family: monospace; }
        .copy-btn { background: #007bff; color: white; padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer; }
    </style>
</head>
<body>
    <h1>🎉 LinkedIn OAuth Erfolgreich!</h1>
    <p class="success">Die Autorisierung war erfolgreich. Ihr Authorization Code:</p>
    
    <div class="code-box">
        <strong>Authorization Code:</strong><br>
        <span id="auth-code">{{ auth_code }}</span>
    </div>
    
    <button class="copy-btn" onclick="copyToClipboard()">📋 Code kopieren</button>
    
    <h3>Nächste Schritte:</h3>
    <ol>
        <li>Kopieren Sie den Authorization Code oben</li>
        <li>Gehen Sie zurück zu Ihrem Terminal</li>
        <li>Fügen Sie den Code dort ein</li>
    </ol>
    
    <script>
        function copyToClipboard() {
            const code = document.getElementById('auth-code').textContent;
            navigator.clipboard.writeText(code).then(function() {
                alert('Authorization Code kopiert!');
            });
        }
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    """Hauptseite"""
    return """
    <h1>LinkedIn XRechnung Agent - OAuth Handler</h1>
    <p>Dieser Service ist bereit für LinkedIn OAuth Callbacks.</p>
    <p>Verwenden Sie diese URL als Redirect URI in Ihrer LinkedIn App:</p>
    <code>https://your-app-name.railway.app/auth/callback</code>
    """

@app.route('/auth/callback')
def oauth_callback():
    """LinkedIn OAuth Callback Handler"""
    try:
        # Hole Authorization Code aus Query Parameters
        auth_code = request.args.get('code')
        error = request.args.get('error')
        state = request.args.get('state')
        
        if error:
            logger.error(f"OAuth Error: {error}")
            return f"❌ OAuth Fehler: {error}", 400
        
        if not auth_code:
            logger.error("Kein Authorization Code erhalten")
            return "❌ Kein Authorization Code erhalten", 400
        
        logger.info(f"OAuth Callback erfolgreich - Code erhalten (Length: {len(auth_code)})")
        
        # Zeige Success Page mit Authorization Code
        return render_template_string(OAUTH_SUCCESS_TEMPLATE, auth_code=auth_code)
        
    except Exception as e:
        logger.error(f"Fehler im OAuth Callback: {str(e)}")
        return f"❌ Server Fehler: {str(e)}", 500

@app.route('/health')
def health():
    """Health Check für Railway"""
    return jsonify({
        "status": "healthy",
        "service": "LinkedIn XRechnung Agent OAuth Handler",
        "timestamp": str(os.environ.get('RAILWAY_DEPLOYMENT_ID', 'local'))
    })

@app.route('/info')
def info():
    """Service Informationen"""
    return jsonify({
        "service": "LinkedIn XRechnung Agent",
        "oauth_callback_url": request.url_root + "auth/callback",
        "railway_env": os.environ.get('RAILWAY_ENVIRONMENT', 'local'),
        "deployment_id": os.environ.get('RAILWAY_DEPLOYMENT_ID', 'local')
    })

if __name__ == '__main__':
    # Für Railway: Port aus Umgebungsvariable
    port = int(os.environ.get('PORT', 5000))
    
    # Für Railway: Host muss 0.0.0.0 sein
    host = '0.0.0.0'
    
    logger.info(f"🚂 Starte OAuth Handler auf Railway")
    logger.info(f"   Host: {host}")
    logger.info(f"   Port: {port}")
    logger.info(f"   OAuth Callback URL: http://{host}:{port}/auth/callback")
    
    app.run(host=host, port=port, debug=False)