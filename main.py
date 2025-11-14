"""
Hauptskript für das LinkedIn Post Multi-Agent System
"""
import argparse
import sys
from multi_agent_system import LinkedInPostMultiAgentSystem
from scheduler import PostScheduler
from config import POST_FREQUENCY, POST_TIME
from dynamic_linkedin_auth import check_linkedin_setup
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def main():
    """Hauptfunktion"""
    print("🚀 LinkedIn XRechnung Agent Multi-Agent System")
    print("=" * 60)
    
    # Prüfe LinkedIn Setup
    if not check_linkedin_setup():
        sys.exit(1)
    
    parser = argparse.ArgumentParser(
        description='LinkedIn Post Multi-Agent System für XRechnung mit invory.de'
    )
    parser.add_argument(
        '--mode',
        choices=['preview', 'post', 'schedule', 'history'],
        default='preview',
        help='Modus: preview (nur anzeigen), post (sofort posten), schedule (automatisch planen), history (Post-Historie)'
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
    
    elif args.mode == 'history':
        # History-Modus: Zeige Post-Historie
        from post_history import post_tracker
        
        print("\n📊 POST HISTORIE ANALYSEN")
        print("=" * 60)
        
        # Letzte 7 Tage Übersicht
        post_tracker.print_recent_summary(7)
        
        # Storytelling Stats
        story_stats = post_tracker.get_storytelling_stats(30)
        if story_stats:
            print("\n🎭 STORYTELLING STRUKTUREN (30 Tage):")
            for structure, count in story_stats.items():
                print(f"  📖 {structure}: {count}x")
        
        # AI-Provider Stats  
        ai_stats = post_tracker.get_ai_provider_stats(30)
        if ai_stats:
            print("\n🧠 AI-PROVIDER USAGE (30 Tage):")
            print("  Research Models:")
            for model, count in ai_stats["research_models"].items():
                print(f"    🔬 {model[:25]}: {count}x")
            print("  Review Models:")
            for model, count in ai_stats["review_models"].items():
                print(f"    ✅ {model[:25]}: {count}x")
        
        # Heutige Posts
        today_posts = post_tracker.get_posts_today()
        if today_posts:
            print(f"\n📅 HEUTE ({len(today_posts)} Posts):")
            for post in today_posts:
                status = "🔴 GEPOSTET" if post.get("linkedin", {}).get("posted") else "👁️ PREVIEW"
                print(f"  {post.get('time')} | {status} | {post.get('topic', 'N/A')[:30]}")
        else:
            print("\n📅 HEUTE: Keine Posts erstellt")

if __name__ == "__main__":
    main()

