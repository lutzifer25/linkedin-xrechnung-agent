"""
Hauptskript für das LinkedIn Post Multi-Agent System
"""
import argparse
import sys
from multi_agent_system import LinkedInPostMultiAgentSystem
from scheduler import PostScheduler
from config import POST_FREQUENCY, POST_TIME
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def main():
    """Hauptfunktion"""
    parser = argparse.ArgumentParser(
        description='LinkedIn Post Multi-Agent System für XRechnung mit invory.de'
    )
    parser.add_argument(
        '--mode',
        choices=['preview', 'post', 'schedule'],
        default='preview',
        help='Modus: preview (nur anzeigen), post (sofort posten), schedule (automatisch planen)'
    )
    parser.add_argument(
        '--topic',
        type=str,
        help='Spezifisches XRechnung-Thema'
    )
    parser.add_argument(
        '--frequency',
        choices=['daily', 'weekly', 'custom'],
        default=POST_FREQUENCY,
        help='Häufigkeit für automatische Posts'
    )
    parser.add_argument(
        '--time',
        type=str,
        default=POST_TIME,
        help='Zeit für automatische Posts (HH:MM Format)'
    )
    
    args = parser.parse_args()
    
    # Erstelle Multi-Agent System
    multi_agent_system = LinkedInPostMultiAgentSystem()
    
    if args.mode == 'preview':
        # Preview-Modus: Erstelle Post ohne zu posten
        logger.info("Preview-Modus: Erstelle Post-Preview")
        result = multi_agent_system.create_post_preview(args.topic)
        
        if result["success"]:
            print("\n" + "="*80)
            print("POST-PREVIEW")
            print("="*80)
            print(f"\nThema: {result['research_data'].get('topic', 'XRechnung')}")
            print(f"Review-Score: {result['review_score']}/100")
            print(f"Genehmigt: {'Ja' if result['review_approved'] else 'Nein'}")
            print("\n" + "-"*80)
            print("POST-TEXT:")
            print("-"*80)
            print(result['post_text'])
            print("-"*80)
            print(f"\nZeichen: {len(result['post_text'])}")
        else:
            print(f"Fehler: {result.get('error', 'Unbekannter Fehler')}")
            sys.exit(1)
    
    elif args.mode == 'post':
        # Post-Modus: Erstelle und poste sofort
        logger.info("Post-Modus: Erstelle und poste auf LinkedIn")
        result = multi_agent_system.create_and_post(args.topic, auto_post=True)
        
        if result["success"]:
            if result["linkedin_posted"]:
                print("\n✅ Post erfolgreich auf LinkedIn gepostet!")
                print(f"\nPost-Text:\n{result['post_text']}")
            else:
                print("\n⚠️  Post wurde erstellt, aber nicht auf LinkedIn gepostet")
                print(f"Grund: Post-Status: {result.get('post_status')}")
                print(f"\nPost-Text:\n{result['post_text']}")
        else:
            print(f"❌ Fehler: {result.get('error', 'Unbekannter Fehler')}")
            sys.exit(1)
    
    elif args.mode == 'schedule':
        # Schedule-Modus: Starte Scheduler
        logger.info("Schedule-Modus: Starte automatischen Scheduler")
        scheduler = PostScheduler()
        scheduler.run(args.frequency, args.time)

if __name__ == "__main__":
    main()

