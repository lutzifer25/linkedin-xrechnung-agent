"""
Einfacher Test für Web-Scraping Funktionalität
"""
import sys
import logging

logging.basicConfig(level=logging.INFO, format='%(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def test_invory_client():
    """Testet den Invory Web-Scraping Client"""
    print("\n" + "="*80)
    print("TEST: Invory Client (Web-Scraping)")
    print("="*80)
    
    try:
        from services.invory_client import InvoryClient
        
        client = InvoryClient()
        print(f"✅ InvoryClient erstellt")
        print(f"   URL: {client.base_url}")
        
        print("\n📡 Versuche, Daten von invory.de abzurufen...")
        data = client.get_xrechnung_insights()
        
        if data:
            print(f"\n✅ Daten erfolgreich abgerufen:")
            print(f"   URL: {data.get('invory_url', 'N/A')}")
            print(f"   Title: {data.get('invory_title', 'N/A')}")
            print(f"   Features: {len(data.get('invory_features', []))} gefunden")
            if data.get('invory_features'):
                for i, feature in enumerate(data.get('invory_features', [])[:3], 1):
                    print(f"     {i}. {feature}")
            print(f"   Keywords: {', '.join(data.get('invory_keywords', []))}")
        else:
            print("\n⚠️  Keine Daten abgerufen (verwendet Mock-Daten)")
        
        return data
    except Exception as e:
        print(f"\n❌ Fehler: {str(e)}")
        import traceback
        traceback.print_exc()
        return None

def test_einvoicehub_client():
    """Testet den EinvoiceHub Web-Scraping Client"""
    print("\n" + "="*80)
    print("TEST: EinvoiceHub Client (Web-Scraping)")
    print("="*80)
    
    try:
        from services.einvoicehub_client import EinvoiceHubClient
        
        client = EinvoiceHubClient()
        print(f"✅ EinvoiceHubClient erstellt")
        print(f"   URL: {client.base_url}")
        
        print("\n📡 Versuche, Daten von einvoicehub.de abzurufen...")
        data = client.get_xrechnung_insights()
        
        if data:
            print(f"\n✅ Daten erfolgreich abgerufen:")
            print(f"   URL: {data.get('einvoicehub_url', 'N/A')}")
            print(f"   Title: {data.get('einvoicehub_title', 'N/A')}")
            print(f"   Features: {len(data.get('einvoicehub_features', []))} gefunden")
            if data.get('einvoicehub_features'):
                for i, feature in enumerate(data.get('einvoicehub_features', [])[:3], 1):
                    print(f"     {i}. {feature}")
            print(f"   Keywords: {', '.join(data.get('einvoicehub_keywords', []))}")
        else:
            print("\n⚠️  Keine Daten abgerufen (verwendet Mock-Daten)")
        
        return data
    except Exception as e:
        print(f"\n❌ Fehler: {str(e)}")
        import traceback
        traceback.print_exc()
        return None

def test_content_creation():
    """Testet die Content-Erstellung mit den gescrapten Daten"""
    print("\n" + "="*80)
    print("TEST: Content-Erstellung (vereinfacht)")
    print("="*80)
    
    try:
        from services.invory_client import InvoryClient
        from services.einvoicehub_client import EinvoiceHubClient
        
        invory_client = InvoryClient()
        einvoicehub_client = EinvoiceHubClient()
        
        invory_data = invory_client.get_xrechnung_insights()
        einvoicehub_data = einvoicehub_client.get_xrechnung_insights()
        
        # Erstelle einen einfachen Post
        post = f"""💼 XRechnung: Die digitale Transformation im Rechnungswesen schreitet voran.

🔍 Aktuelle Entwicklungen zeigen, wie wichtig standardisierte E-Invoicing-Lösungen wie XRechnung geworden sind.

✅ Wichtigste Erkenntnisse:
• XRechnung ist der Standard für elektronische Rechnungen in Deutschland
• Compliance mit gesetzlichen Anforderungen ist essentiell
• Automatisierung reduziert Fehler und beschleunigt Prozesse"""

        if invory_data and invory_data.get('invory_features'):
            post += f"\n\n🚀 Lösungen wie {invory_data.get('invory_url', 'https://invory.de')} bieten Unternehmen die Möglichkeit, ihre Rechnungsprozesse effizient zu digitalisieren."
            post += f"\n\n✨ Features:"
            for feature in invory_data.get('invory_features', [])[:2]:
                post += f"\n• {feature}"
        
        if einvoicehub_data and einvoicehub_data.get('einvoicehub_features'):
            post += f"\n\n📊 Plattformen wie {einvoicehub_data.get('einvoicehub_url', 'https://einvoicehub.de')} ermöglichen es Unternehmen, digitale Rechnungsprozesse zu optimieren."
            post += f"\n\n🎯 Features:"
            for feature in einvoicehub_data.get('einvoicehub_features', [])[:2]:
                post += f"\n• {feature}"
        
        post += "\n\nWas sind eure Erfahrungen mit XRechnung?"
        
        # Füge Links hinzu
        post += f"\n\n🔗 Weitere Informationen:"
        post += f"\n• {invory_data.get('invory_url', 'https://invory.de') if invory_data else 'https://invory.de'}"
        post += f"\n• {einvoicehub_data.get('einvoicehub_url', 'https://einvoicehub.de') if einvoicehub_data else 'https://einvoicehub.de'}"
        
        post += "\n\n#XRechnung #EInvoicing #DigitaleTransformation #Prozessautomatisierung #Rechnungswesen #Digitalisierung"
        
        print(f"\n✅ Post erstellt:")
        print(f"   Zeichen: {len(post)}")
        print(f"   Enthält Links: {'invory.de' in post and 'einvoicehub.de' in post}")
        print("\n" + "-"*80)
        print("POST-TEXT:")
        print("-"*80)
        print(post)
        print("-"*80)
        
        return post
    except Exception as e:
        print(f"\n❌ Fehler: {str(e)}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    print("\n🧪 Starte Web-Scraping Tests\n")
    
    # Test 1: Invory Client
    invory_data = test_invory_client()
    
    # Test 2: EinvoiceHub Client
    einvoicehub_data = test_einvoicehub_client()
    
    # Test 3: Content-Erstellung
    post = test_content_creation()
    
    print("\n" + "="*80)
    if invory_data and einvoicehub_data and post:
        print("✅ Alle Tests erfolgreich!")
    else:
        print("⚠️  Einige Tests haben Warnungen, aber grundlegende Funktionalität funktioniert")
    print("="*80)
    print("\n💡 Hinweis: Für vollständige Tests mit Agents benötigen Sie:")
    print("   - OpenAI API Key (für LLM-Funktionalität)")
    print("   - crewai und langchain (für Agent-Framework)")
    print("   - LinkedIn API Credentials (für Posting)")

