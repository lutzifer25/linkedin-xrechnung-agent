"""
Post History Tracker - Verfolgt alle LinkedIn Posts mit Details
"""
import json
import os
from datetime import datetime
from typing import Dict, List, Optional
import logging

logger = logging.getLogger(__name__)

class PostHistoryTracker:
    """Verfolgt LinkedIn Post Historie mit lokaler JSON-Datei"""
    
    def __init__(self, history_file: str = "post_history.json"):
        self.history_file = history_file
        self.history = self._load_history()
    
    def _load_history(self) -> List[Dict]:
        """Lädt Post-Historie aus JSON-Datei"""
        if os.path.exists(self.history_file):
            try:
                with open(self.history_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except (json.JSONDecodeError, FileNotFoundError) as e:
                logger.warning(f"Konnte Post-Historie nicht laden: {e}")
                return []
        return []
    
    def _save_history(self):
        """Speichert Post-Historie in JSON-Datei"""
        try:
            with open(self.history_file, 'w', encoding='utf-8') as f:
                json.dump(self.history, f, ensure_ascii=False, indent=2)
            logger.info(f"✅ Post-Historie gespeichert: {self.history_file}")
        except Exception as e:
            logger.error(f"❌ Fehler beim Speichern der Post-Historie: {e}")
    
    def add_post(self, 
                 topic: str,
                 post_text: str,
                 storytelling_structure: str,
                 research_model: str,
                 review_model: str,
                 review_score: int,
                 image_theme: Optional[str] = None,
                 image_url: Optional[str] = None,
                 linkedin_post_id: Optional[str] = None,
                 mode: str = "preview") -> Dict:
        """Fügt einen neuen Post zur Historie hinzu"""
        
        post_entry = {
            "id": len(self.history) + 1,
            "timestamp": datetime.now().isoformat(),
            "date": datetime.now().strftime("%Y-%m-%d"),
            "time": datetime.now().strftime("%H:%M:%S"),
            "mode": mode,  # preview, post, schedule
            "topic": topic,
            "storytelling_structure": storytelling_structure.get("name", "Unknown") if isinstance(storytelling_structure, dict) else storytelling_structure,
            "ai_providers": {
                "research_model": research_model,
                "review_model": review_model
            },
            "review_score": review_score,
            "character_count": len(post_text),
            "image": {
                "theme": image_theme,
                "url": image_url,
                "included": image_url is not None
            },
            "linkedin": {
                "post_id": linkedin_post_id,
                "posted": linkedin_post_id is not None
            },
            "content_preview": post_text[:100] + "..." if len(post_text) > 100 else post_text
        }
        
        self.history.append(post_entry)
        self._save_history()
        
        logger.info(f"📝 Post #{post_entry['id']} zur Historie hinzugefügt: {topic}")
        return post_entry
    
    def get_posts_last_days(self, days: int = 7) -> List[Dict]:
        """Gibt Posts der letzten N Tage zurück"""
        from datetime import date, timedelta
        
        cutoff_date = date.today() - timedelta(days=days)
        recent_posts = []
        
        for post in self.history:
            try:
                post_date = datetime.fromisoformat(post["timestamp"]).date()
                if post_date >= cutoff_date:
                    recent_posts.append(post)
            except (ValueError, KeyError) as e:
                logger.warning(f"Ungültiger Post-Eintrag: {e}")
                continue
        
        return sorted(recent_posts, key=lambda x: x["timestamp"], reverse=True)
    
    def get_posts_today(self) -> List[Dict]:
        """Gibt Posts von heute zurück"""
        today = datetime.now().strftime("%Y-%m-%d")
        return [post for post in self.history if post.get("date") == today]
    
    def get_posted_count_last_days(self, days: int = 7) -> int:
        """Zählt echte Posts (nicht Previews) der letzten N Tage"""
        recent_posts = self.get_posts_last_days(days)
        return len([post for post in recent_posts if post.get("mode") == "post" and post.get("linkedin", {}).get("posted")])
    
    def print_recent_summary(self, days: int = 7):
        """Druckt eine Zusammenfassung der letzten Posts"""
        recent_posts = self.get_posts_last_days(days)
        posted_count = self.get_posted_count_last_days(days)
        
        print(f"\n📊 POST HISTORIE - Letzte {days} Tage:")
        print("=" * 60)
        print(f"📝 Gesamt Aktivität: {len(recent_posts)} Einträge")
        print(f"📤 Echte Posts: {posted_count}")
        print(f"👁️  Previews: {len(recent_posts) - posted_count}")
        
        if recent_posts:
            print(f"\n📋 Letzte Posts:")
            for post in recent_posts[:5]:  # Top 5
                status = "🔴 GEPOSTET" if post.get("linkedin", {}).get("posted") else "👁️ PREVIEW"
                ai_info = f"{post.get('ai_providers', {}).get('research_model', 'N/A')[:15]} → {post.get('ai_providers', {}).get('review_model', 'N/A')[:15]}"
                
                print(f"  {post.get('date')} {post.get('time')} | {status}")
                print(f"    📖 Story: {post.get('storytelling_structure', 'N/A')}")
                print(f"    🧠 AI: {ai_info}")
                print(f"    📝 Topic: {post.get('topic', 'N/A')[:50]}")
                print(f"    💯 Score: {post.get('review_score', 'N/A')}/100")
                print()
        else:
            print("🔍 Keine Posts in diesem Zeitraum gefunden.")
        
        print("=" * 60)
    
    def get_storytelling_stats(self, days: int = 30) -> Dict:
        """Analysiert Storytelling-Struktur Verwendung"""
        recent_posts = self.get_posts_last_days(days)
        structures = {}
        
        for post in recent_posts:
            structure = post.get("storytelling_structure", "Unknown")
            # Handle both string and dict formats
            if isinstance(structure, dict):
                structure = structure.get("name", "Unknown")
            structures[structure] = structures.get(structure, 0) + 1
        
        return structures
    
    def get_ai_provider_stats(self, days: int = 30) -> Dict:
        """Analysiert AI-Provider Verwendung"""
        recent_posts = self.get_posts_last_days(days)
        research_models = {}
        review_models = {}
        
        for post in recent_posts:
            ai_providers = post.get("ai_providers", {})
            
            research = ai_providers.get("research_model", "Unknown")
            research_models[research] = research_models.get(research, 0) + 1
            
            review = ai_providers.get("review_model", "Unknown")
            review_models[review] = review_models.get(review, 0) + 1
        
        return {
            "research_models": research_models,
            "review_models": review_models
        }

# Singleton Instance
post_tracker = PostHistoryTracker()