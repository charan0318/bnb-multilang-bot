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
        if webhook_url and os.getenv('TELEGRAM_BOT_TOKEN'):
            try:
                result = bot.set_webhook(f"{webhook_url}/webhook")
                if result:
                    logger.info(f"Production webhook set successfully to: {webhook_url}/webhook")
                else:
                    logger.warning("Webhook setup returned False")
            except Exception as e:
                logger.error(f"Failed to set production webhook: {e}")
                # Don't fail the entire app if webhook setup fails
        else:
            logger.warning("WEBHOOK_URL or TELEGRAM_BOT_TOKEN not set - webhook not configured")
    
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