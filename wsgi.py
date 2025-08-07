"""
WSGI entry point for production deployment
"""
import os
import logging
import threading
import time
from main import app, bot

# Configure logging for production
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def setup_production_webhook():
    """Set up webhook for production deployment in background"""
    def webhook_setup():
        # Wait a bit for the server to be ready
        time.sleep(10)
        
        webhook_url = os.getenv('WEBHOOK_URL')
        bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
        
        if not bot_token:
            logger.error("TELEGRAM_BOT_TOKEN not found in environment variables")
            return
            
        if not webhook_url:
            logger.error("WEBHOOK_URL not found in environment variables")
            return
            
        try:
            # Get current webhook info first
            webhook_info = bot.bot.get_webhook_info()
            logger.info(f"Current webhook URL: {webhook_info.url}")
            
            target_webhook = f"{webhook_url}/webhook"
            
            if webhook_info.url == target_webhook:
                logger.info("Webhook already configured correctly")
                return
            
            # Set new webhook
            result = bot.set_webhook(target_webhook)
            if result:
                logger.info(f"Production webhook set successfully to: {target_webhook}")
            else:
                logger.error("Webhook setup returned False - check bot token and URL validity")
                
        except Exception as e:
            logger.error(f"Failed to set production webhook: {e}")
            # Don't fail the entire app if webhook setup fails
    
    # Run webhook setup in background thread to avoid blocking startup
    webhook_thread = threading.Thread(target=webhook_setup, daemon=True)
    webhook_thread.start()
    logger.info("Webhook setup initiated in background")

# Initialize webhook setup (non-blocking)
if os.getenv('TELEGRAM_BOT_TOKEN'):
    setup_production_webhook()
else:
    logger.warning("TELEGRAM_BOT_TOKEN not found - skipping webhook setup")

# This is the WSGI application that Gunicorn will use
application = app

if __name__ == "__main__":
    # This runs if you execute wsgi.py directly (for testing)
    app.run(host='0.0.0.0', port=int(os.getenv('PORT', 10000)))