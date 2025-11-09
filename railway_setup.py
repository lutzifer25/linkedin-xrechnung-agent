"""
Railway Deployment Helper
Automatisiert Railway Setup und LinkedIn OAuth Konfiguration
"""
import os
import webbrowser
import time

def print_railway_setup():
    """Zeigt Railway Setup Anweisungen"""
    
    print("🚂" + "="*70)
    print("RAILWAY DEPLOYMENT SETUP - LinkedIn XRechnung Agent")
    print("="*71)
    
    print("\n📋 SCHRITT 1: Railway Projekt erstellen")
    print("-"*50)
    print("1. Gehe zu: https://railway.app")
    print("2. Klicke 'New Project' → 'Deploy from GitHub'")
    print("3. Wähle Repository: lutzifer25/linkedin-xrechnung-agent")
    print("4. Deploy starten und warten...")
    
    print("\n🌐 SCHRITT 2: Railway URL ermitteln")
    print("-"*50)
    print("Nach dem Deployment wird Railway eine URL zeigen:")
    print("Format: https://linkedin-xrechnung-agent-production.up.railway.app")
    print("Diese URL brauchst du für die nächsten Schritte!")
    
    print("\n⚙️ SCHRITT 3: Environment Variables in Railway setzen")
    print("-"*50)
    print("Im Railway Dashboard → dein Projekt → Variables:")
    print("")
    
    # Lese Template-Datei
    try:
        with open('railway-env-template.txt', 'r') as f:
            template = f.read()
        
        print("Kopiere diese Variablen (railway-env-template.txt):")
        print("┌" + "─"*68 + "┐")
        for line in template.split('\n')[:15]:  # Ersten 15 Zeilen
            if line.strip() and not line.startswith('#'):
                print(f"│ {line:<66} │")
        print("└" + "─"*68 + "┘")
        
    except FileNotFoundError:
        print("❌ railway-env-template.txt nicht gefunden")
    
    print("\n🔗 SCHRITT 4: LinkedIn App Redirect URI konfigurieren")
    print("-"*50)
    print("1. Gehe zu: https://www.linkedin.com/developers/")
    print("2. Wähle deine LinkedIn App aus")
    print("3. Unter 'Auth' → 'Authorized redirect URLs':")
    print("4. Füge hinzu: https://DEINE-RAILWAY-URL.railway.app/auth/callback")
    print("")
    print("Beispiel:")
    print("https://linkedin-xrechnung-agent-production.up.railway.app/auth/callback")
    
    print("\n🧪 SCHRITT 5: OAuth Flow testen")
    print("-"*50)
    print("1. Railway App URL öffnen")
    print("2. OAuth Flow durchlaufen")
    print("3. Authorization Code erhalten")
    print("4. Tokens in Railway Variables speichern (optional)")
    
    print("\n🚀 SCHRITT 6: Production Mode aktivieren")
    print("-"*50)
    print("Railway Startkommando ändern zu:")
    print("python3 scheduler.py  # Für automatische Posts")
    print("# oder")
    print("python3 railway_oauth_handler.py  # Für OAuth Handler")
    
    print("\n" + "="*71)
    
    return True

def open_railway_links():
    """Öffnet relevante Railway Links"""
    
    print("\n🌐 Öffne relevante Links...")
    
    links = [
        ("Railway Dashboard", "https://railway.app/dashboard"),
        ("LinkedIn Developers", "https://www.linkedin.com/developers/"),
        ("GitHub Repository", "https://github.com/lutzifer25/linkedin-xrechnung-agent")
    ]
    
    for name, url in links:
        try:
            print(f"   {name}: {url}")
            webbrowser.open(url)
            time.sleep(1)  # Kurze Pause zwischen den Links
        except Exception as e:
            print(f"   ❌ Konnte {name} nicht öffnen: {e}")
    
    print("\n✅ Links geöffnet!")

def show_railway_url_examples():
    """Zeigt Railway URL Beispiele"""
    
    print("\n📖 RAILWAY URL BEISPIELE")
    print("-"*50)
    
    examples = [
        "https://linkedin-xrechnung-agent-production.up.railway.app",
        "https://web-production-a1b2c3.up.railway.app", 
        "https://xrechnung-agent-main-f4e5d6.up.railway.app"
    ]
    
    print("Mögliche Railway URLs:")
    for i, example in enumerate(examples, 1):
        print(f"   {i}. {example}")
    
    print("\nDeine OAuth Callback URL wird dann:")
    for i, example in enumerate(examples, 1):
        print(f"   {i}. {example}/auth/callback")

def main():
    """Hauptfunktion"""
    
    print_railway_setup()
    
    print("\n" + "?"*71)
    choice = input("Möchtest du die Links automatisch öffnen? (y/N): ").lower().strip()
    
    if choice in ['y', 'yes', 'ja']:
        open_railway_links()
    
    show_railway_url_examples()
    
    print("\n💡 NÄCHSTE SCHRITTE:")
    print("1. Railway Deployment durchführen")  
    print("2. URL notieren und in LinkedIn App eintragen")
    print("3. Environment Variables in Railway setzen")
    print("4. OAuth Flow testen")
    
    print("\n🔧 LOKALER TEST:")
    print("python main.py --mode preview  # Für lokalen Test")
    
    print("\n📚 DOKUMENTATION:")
    print("Siehe: RAILWAY_OAUTH_SETUP.md für Details")

if __name__ == "__main__":
    main()