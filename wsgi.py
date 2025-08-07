"""
WSGI entry point for production deployment
"""
import os
from main import app, setup_webhook

# Set up webhook when the app starts in production
setup_webhook()

if __name__ == "__main__":
    app.run()