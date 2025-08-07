"""
WSGI entry point for production deployment
"""
import os
import logging
from main import app, bot

# Configure logging for production
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Set up webhook when the app starts in production
def setup_production_webhook():
    """Set up webhook for production deployment"""
    webhook_url = os.getenv('WEBHOOK_URL')
    if webhook_url:
        try:
            bot.set_webhook(f"{webhook_url}/webhook")
            logger.info(f"Production webhook set to: {webhook_url}/webhook")
        except Exception as e:
            logger.error(f"Failed to set production webhook: {e}")
    else:
        logger.warning("WEBHOOK_URL not set - webhook not configured")

# Initialize webhook on startup
setup_production_webhook()

# This is the WSGI application that Gunicorn will use
application = app

if __name__ == "__main__":
    # This runs if you execute wsgi.py directly (for testing)
    app.run(host='0.0.0.0', port=int(os.getenv('PORT', 5000)))