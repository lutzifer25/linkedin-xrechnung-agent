"""
Test-Skript für das Multi-Agent System
"""
from multi_agent_system import LinkedInPostMultiAgentSystem
import json

def test_preview():
    """Testet die Post-Preview-Funktionalität"""
    print("="*80)
    print("TEST: Post-Preview")
    print("="*80)
    
    system = LinkedInPostMultiAgentSystem()
    result = system.create_post_preview(topic="XRechnung Standard")
    
    if result["success"]:
        print(f"\n✅ Post erfolgreich erstellt!")
        print(f"   Thema: {result['research_data']['topic']}")
        print(f"   Review-Score: {result['review_score']}/100")
        print(f"   Genehmigt: {'Ja' if result['review_approved'] else 'Nein'}")
        print(f"\n   Post-Text:\n   {result['post_text']}")
        print(f"\n   Zeichen: {len(result['post_text'])}")
    else:
        print(f"\n❌ Fehler: {result.get('error', 'Unbekannter Fehler')}")
    
    return result

def test_topics():
    """Testet verfügbare Themen"""
    print("\n" + "="*80)
    print("TEST: Verfügbare Themen")
    print("="*80)
    
    system = LinkedInPostMultiAgentSystem()
    topics = system.get_available_topics()
    
    print(f"\nVerfügbare XRechnung-Themen ({len(topics)}):")
    for i, topic in enumerate(topics, 1):
        print(f"  {i}. {topic}")
    
    return topics

def test_invory_integration():
    """Testet die Invory-Integration (Web-Scraping)"""
    print("\n" + "="*80)
    print("TEST: Invory-Integration (Web-Scraping)")
    print("="*80)
    
    from services.invory_client import InvoryClient
    
    client = InvoryClient()
    data = client.get_xrechnung_insights()
    
    if data:
        print(f"\n✅ Invory-Daten erhalten:")
        print(f"   URL: {data.get('invory_url', 'N/A')}")
        print(f"   Title: {data.get('invory_title', 'N/A')}")
        print(f"   Features: {', '.join(data.get('invory_features', []))}")
        print(f"   Keywords: {', '.join(data.get('invory_keywords', []))}")
    else:
        print("\n⚠️  Keine Invory-Daten verfügbar (verwendet Mock-Daten)")
    
    return data

def test_einvoicehub_integration():
    """Testet die EinvoiceHub-Integration (Web-Scraping)"""
    print("\n" + "="*80)
    print("TEST: EinvoiceHub-Integration (Web-Scraping)")
    print("="*80)
    
    from services.einvoicehub_client import EinvoiceHubClient
    
    client = EinvoiceHubClient()
    data = client.get_xrechnung_insights()
    
    if data:
        print(f"\n✅ EinvoiceHub-Daten erhalten:")
        print(f"   URL: {data.get('einvoicehub_url', 'N/A')}")
        print(f"   Title: {data.get('einvoicehub_title', 'N/A')}")
        print(f"   Features: {', '.join(data.get('einvoicehub_features', []))}")
        print(f"   Keywords: {', '.join(data.get('einvoicehub_keywords', []))}")
    else:
        print("\n⚠️  Keine EinvoiceHub-Daten verfügbar (verwendet Mock-Daten)")
    
    return data

if __name__ == "__main__":
    print("\n🧪 Starte Tests für LinkedIn Post Multi-Agent System\n")
    
    # Test 1: Verfügbare Themen
    test_topics()
    
    # Test 2: Invory-Integration (Web-Scraping)
    test_invory_integration()
    
    # Test 3: EinvoiceHub-Integration (Web-Scraping)
    test_einvoicehub_integration()
    
    # Test 4: Post-Preview
    test_preview()
    
    print("\n" + "="*80)
    print("✅ Alle Tests abgeschlossen!")
    print("="*80)

