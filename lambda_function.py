"""
AWS Lambda Function für LinkedIn Post Agent
Serverless-Variante für EventBridge (Cron) Triggers
"""
import json
import logging
from multi_agent_system import LinkedInPostMultiAgentSystem

# Konfiguriere Logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    """
    AWS Lambda Handler für automatische LinkedIn-Posts
    
    Args:
        event: Event-Daten (von EventBridge)
        context: Lambda Context
        
    Returns:
        dict: Response mit Status
    """
    logger.info("Lambda Function gestartet für LinkedIn Post")
    logger.info(f"Event: {json.dumps(event)}")
    
    try:
        # Erstelle Multi-Agent System
        multi_agent_system = LinkedInPostMultiAgentSystem()
        
        # Erstelle und poste
        result = multi_agent_system.create_and_post(auto_post=True)
        
        if result["success"]:
            if result["linkedin_posted"]:
                logger.info("✅ Post erfolgreich auf LinkedIn gepostet")
                return {
                    "statusCode": 200,
                    "body": json.dumps({
                        "message": "Post erfolgreich auf LinkedIn gepostet",
                        "post_text": result["post_text"][:200] + "...",
                        "review_score": result["review_score"]
                    })
                }
            else:
                logger.warning("⚠️ Post wurde erstellt, aber nicht gepostet")
                return {
                    "statusCode": 200,
                    "body": json.dumps({
                        "message": "Post erstellt, aber nicht gepostet",
                        "reason": result.get("post_status"),
                        "post_text": result["post_text"][:200] + "..."
                    })
                }
        else:
            logger.error(f"❌ Fehler: {result.get('error', 'Unbekannter Fehler')}")
            return {
                "statusCode": 500,
                "body": json.dumps({
                    "message": "Fehler bei Post-Erstellung",
                    "error": result.get("error", "Unbekannter Fehler")
                })
            }
            
    except Exception as e:
        logger.error(f"❌ Exception: {str(e)}")
        import traceback
        traceback.print_exc()
        return {
            "statusCode": 500,
            "body": json.dumps({
                "message": "Internal Server Error",
                "error": str(e)
            })
        }

