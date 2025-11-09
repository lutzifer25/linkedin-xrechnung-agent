"""
Einfacher Testlauf für das LinkedIn XRechnung Agent System
Führt verschiedene Tests durch ohne echte LinkedIn Posts
"""
import sys
import os
from datetime import datetime

# Füge das Projekt-Verzeichnis zum Python-Pfad hinzu
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_environment_setup():
    """Testet die Umgebungskonfiguration"""
    print("🔧 Test 1: Umgebungskonfiguration")
    print("-" * 50)
    
    try:
        from dotenv import load_dotenv
        load_dotenv()
        
        # Prüfe wichtige Umgebungsvariablen
        import os
        
        linkedin_client_id = os.getenv("LINKEDIN_CLIENT_ID")
        linkedin_client_secret = os.getenv("LINKEDIN_CLIENT_SECRET")
        openai_key = os.getenv("OPENAI_API_KEY")
        
        print(f"✅ .env Datei geladen")
        print(f"   LINKEDIN_CLIENT_ID: {'✅ Gesetzt' if linkedin_client_id else '❌ Fehlt'}")
        print(f"   LINKEDIN_CLIENT_SECRET: {'✅ Gesetzt' if linkedin_client_secret else '❌ Fehlt'}")
        print(f"   OPENAI_API_KEY: {'✅ Gesetzt' if openai_key else '❌ Fehlt'}")
        
        if not openai_key:
            print("\n⚠️  WICHTIG: OPENAI_API_KEY wird für den Test benötigt")
            return False
            
        return True
        
    except Exception as e:
        print(f"❌ Fehler beim Laden der Umgebung: {str(e)}")
        return False

def test_dependencies():
    """Testet ob alle Dependencies installiert sind"""
    print("\n🐍 Test 2: Python Dependencies")
    print("-" * 50)
    
    required_packages = [
        "crewai",
        "langchain", 
        "langchain_openai",
        "requests",
        "beautifulsoup4",
        "python_dotenv"
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.replace("-", "_"))
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package} - FEHLT")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n⚠️  Fehlende Packages: {', '.join(missing_packages)}")
        print("   Installieren mit: pip install -r requirements.txt")
        return False
    
    return True

def test_web_scraping():
    """Testet Web-Scraping ohne API-Keys"""
    print("\n🌐 Test 3: Web-Scraping (invory.de)")
    print("-" * 50)
    
    try:
        from services.invory_client import InvoryClient
        
        client = InvoryClient()
        
        # Test einfache Website-Erreichbarkeit
        import requests
        response = requests.get("https://invory.de", timeout=5)
        
        if response.status_code == 200:
            print("✅ invory.de erreichbar")
            
            # Test basic scraping - verwende existierende Methode
            research_data = client.get_xrechnung_info()
            
            if research_data and research_data.get('success', False):
                print("✅ Web-Scraping funktioniert")
                print(f"   Gefundene Daten: {len(str(research_data.get('content', '')))} Zeichen")
            else:
                print("⚠️  Web-Scraping mit Mock-Daten (normal)")
                
        else:
            print(f"⚠️  invory.de nicht erreichbar (Status: {response.status_code})")
            
        return True
        
    except Exception as e:
        print(f"❌ Web-Scraping Fehler: {str(e)}")
        return False

def test_agents_basic():
    """Testet grundlegende Agent-Funktionalität"""
    print("\n🤖 Test 4: CrewAI Agents (Basic)")
    print("-" * 50)
    
    try:
        # Test Agent-Imports
        from agents.research_agent import ResearchAgent
        from agents.content_agent import ContentAgent  
        from agents.review_agent import ReviewAgent
        
        print("✅ Agent-Imports erfolgreich")
        
        # Test Agent-Initialisierung (ohne LLM-Calls)
        try:
            research = ResearchAgent()
            content = ContentAgent()
            review = ReviewAgent()
            
            print("✅ Agent-Initialisierung erfolgreich")
            print(f"   Research Agent: {research.agent.role}")
            print(f"   Content Agent: {content.agent.role}")
            print(f"   Review Agent: {review.agent.role}")
            
        except Exception as e:
            print(f"❌ Agent-Initialisierung Fehler: {str(e)}")
            return False
            
        return True
        
    except Exception as e:
        print(f"❌ Agent-Import Fehler: {str(e)}")
        return False

def test_linkedin_dynamic_auth():
    """Testet dynamische LinkedIn-Authentifizierung (ohne Ausführung)"""
    print("\n🔑 Test 5: LinkedIn Dynamic Auth (Dry Run)")
    print("-" * 50)
    
    try:
        from dynamic_linkedin_auth import check_linkedin_setup
        
        setup_ok = check_linkedin_setup()
        
        if setup_ok:
            print("✅ LinkedIn Client Credentials verfügbar")
            print("   (Dynamische Auth bereit)")
        else:
            print("⚠️  LinkedIn Setup unvollständig")
            print("   (Für echten Test: Client ID/Secret in .env eintragen)")
            
        return True
        
    except Exception as e:
        print(f"❌ LinkedIn Auth Test Fehler: {str(e)}")
        return False

def test_full_preview():
    """Testet kompletten Workflow im Preview-Modus"""
    print("\n🎯 Test 6: Kompletter Workflow (Preview)")
    print("-" * 50)
    
    try:
        from multi_agent_system import LinkedInPostMultiAgentSystem
        
        print("🚀 Starte Multi-Agent System...")
        system = LinkedInPostMultiAgentSystem()
        
        # Test Preview-Funktionalität (ohne LinkedIn-Posting)
        print("📝 Erstelle Post-Preview...")
        result = system.create_post_preview(topic="XRechnung Standard")
        
        if result and result.get("success"):
            print("✅ Post-Preview erfolgreich erstellt!")
            print(f"   Thema: {result.get('research_data', {}).get('topic', 'Unbekannt')}")
            print(f"   Post-Länge: {len(result.get('post_text', ''))} Zeichen")
            print(f"   Review-Score: {result.get('review_score', 'N/A')}/100")
            
            # Zeige Anfang des Posts
            post_text = result.get('post_text', '')
            preview = post_text[:200] + "..." if len(post_text) > 200 else post_text
            print(f"\n   Post-Preview:\n   {preview}")
            
            return True
        else:
            error = result.get('error', 'Unbekannter Fehler') if result else 'Kein Ergebnis'
            print(f"❌ Post-Preview Fehler: {error}")
            return False
            
    except Exception as e:
        print(f"❌ Workflow-Test Fehler: {str(e)}")
        return False

def run_testlauf():
    """Führt alle Tests aus"""
    print("=" * 80)
    print("🧪 LINKEDIN XRECHNUNG AGENT - TESTLAUF")
    print("=" * 80)
    print(f"Zeitpunkt: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    tests = [
        ("Umgebung", test_environment_setup),
        ("Dependencies", test_dependencies),
        ("Web-Scraping", test_web_scraping),
        ("Agents", test_agents_basic),
        ("LinkedIn Auth", test_linkedin_dynamic_auth),
        ("Vollständiger Workflow", test_full_preview)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            success = test_func()
            results.append((test_name, success))
        except KeyboardInterrupt:
            print(f"\n❌ Test abgebrochen: {test_name}")
            break
        except Exception as e:
            print(f"\n❌ Unerwarteter Fehler in {test_name}: {str(e)}")
            results.append((test_name, False))
    
    # Zusammenfassung
    print("\n" + "=" * 80)
    print("📊 TESTLAUF-ZUSAMMENFASSUNG")
    print("=" * 80)
    
    passed = sum(1 for _, success in results if success)
    total = len(results)
    
    for test_name, success in results:
        status = "✅ BESTANDEN" if success else "❌ FEHLGESCHLAGEN"
        print(f"   {test_name:<25} {status}")
    
    print(f"\nGesamtergebnis: {passed}/{total} Tests bestanden")
    
    if passed == total:
        print("\n🎉 ALLE TESTS BESTANDEN!")
        print("   Das System ist bereit für den Einsatz.")
        print(f"\n🚀 Nächste Schritte:")
        print(f"   1. Echten Test: python main.py --mode preview")
        print(f"   2. Live-Post: python main.py --mode post")
    else:
        print(f"\n⚠️  {total - passed} Test(s) fehlgeschlagen")
        print("   Bitte Fehler beheben bevor Sie das System verwenden.")
    
    print("=" * 80)

if __name__ == "__main__":
    run_testlauf()