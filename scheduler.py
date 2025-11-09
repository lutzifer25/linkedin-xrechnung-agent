"""
Scheduler für automatische LinkedIn-Posts
"""
import schedule
import time
from datetime import datetime
from multi_agent_system import LinkedInPostMultiAgentSystem
from config import POST_FREQUENCY, POST_TIME
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PostScheduler:
    """Scheduler für automatische LinkedIn-Post-Erstellung"""
    
    def __init__(self):
        self.multi_agent_system = LinkedInPostMultiAgentSystem()
        self.is_running = False
    
    def create_and_post_job(self):
        """Job-Funktion für automatische Post-Erstellung"""
        logger.info(f"Starte automatische Post-Erstellung um {datetime.now()}")
        
        try:
            result = self.multi_agent_system.create_and_post(auto_post=True)
            
            if result["success"]:
                if result["linkedin_posted"]:
                    logger.info("Post erfolgreich auf LinkedIn gepostet")
                else:
                    logger.warning("Post wurde erstellt, aber nicht auf LinkedIn gepostet")
                    logger.info(f"Post-Text: {result['post_text'][:100]}...")
            else:
                logger.error(f"Fehler bei Post-Erstellung: {result.get('error', 'Unbekannter Fehler')}")
                
        except Exception as e:
            logger.error(f"Fehler im Scheduled Job: {str(e)}")
    
    def setup_schedule(self, frequency: str = None, post_time: str = None):
        """
        Richtet den Zeitplan für automatische Posts ein
        
        Args:
            frequency: Häufigkeit (daily, weekly, custom)
            post_time: Zeit für Posts (HH:MM Format)
        """
        frequency = frequency or POST_FREQUENCY
        post_time = post_time or POST_TIME
        
        # Lösche alle bestehenden Jobs
        schedule.clear()
        
        if frequency == "daily":
            schedule.every().day.at(post_time).do(self.create_and_post_job)
            logger.info(f"Täglicher Post geplant um {post_time}")
        elif frequency == "weekly":
            schedule.every().monday.at(post_time).do(self.create_and_post_job)
            logger.info(f"Wöchentlicher Post geplant (Montags um {post_time})")
        elif frequency == "custom":
            # Beispiel: Montag, Mittwoch, Freitag
            schedule.every().monday.at(post_time).do(self.create_and_post_job)
            schedule.every().wednesday.at(post_time).do(self.create_and_post_job)
            schedule.every().friday.at(post_time).do(self.create_and_post_job)
            logger.info(f"Custom Schedule: Mo, Mi, Fr um {post_time}")
        else:
            logger.warning(f"Unbekannte Häufigkeit: {frequency}, verwende daily")
            schedule.every().day.at(post_time).do(self.create_and_post_job)
    
    def run(self, frequency: str = None, post_time: str = None):
        """
        Startet den Scheduler
        
        Args:
            frequency: Häufigkeit (daily, weekly, custom)
            post_time: Zeit für Posts (HH:MM Format)
        """
        self.setup_schedule(frequency, post_time)
        self.is_running = True
        
        logger.info("Scheduler gestartet. Drücke Ctrl+C zum Beenden.")
        
        try:
            while self.is_running:
                schedule.run_pending()
                time.sleep(60)  # Prüfe jede Minute
        except KeyboardInterrupt:
            logger.info("Scheduler wird beendet...")
            self.is_running = False
    
    def stop(self):
        """Stoppt den Scheduler"""
        self.is_running = False
        schedule.clear()
        logger.info("Scheduler gestoppt")

