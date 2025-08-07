
import os
import logging
import sys
from flask import Flask, request, jsonify
from bot import TranslationBot

# Configure logging for production
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# Validate required environment variables
required_env_vars = ['TELEGRAM_BOT_TOKEN']
missing_vars = [var for var in required_env_vars if not os.getenv(var)]
if missing_vars:
    logger.error(f"Missing required environment variables: {', '.join(missing_vars)}")
    sys.exit(1)

app = Flask(__name__)

# Initialize the bot
try:
    bot = TranslationBot()
    logger.info("Translation bot initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize bot: {e}")
    sys.exit(1)

@app.route('/webhook', methods=['POST'])
def webhook():
    """Handle incoming Telegram webhook requests"""
    try:
        update_data = request.get_json()
        if update_data:
            bot.handle_webhook_update(update_data)
        return jsonify({'status': 'ok'}), 200
    except Exception as e:
        logger.error(f"Error handling webhook: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint for monitoring"""
    return jsonify({
        'status': 'healthy', 
        'service': 'translation-bot',
        'supported_languages': len(bot.config.languages)
    }), 200

@app.route('/', methods=['GET'])
def index():
    """Basic index page with bot information"""
    supported_commands = ', '.join(bot.config.get_supported_commands())
    return f'''
    <html>
        <head>
            <title>Telegram Translation Bot</title>
            <meta charset="UTF-8">
        </head>
        <body>
            <h1>🤖 Telegram Translation Bot</h1>
            <p><strong>Status:</strong> ✅ Running and ready to translate messages!</p>
            <p><strong>Supported Languages:</strong> {len(bot.config.languages)}</p>
            <p><strong>Commands:</strong> {supported_commands}</p>
            <hr>
            <h3>How to use:</h3>
            <ol>
                <li>Add the bot to your Telegram group</li>
                <li>Reply to any message with a language command (e.g., /hi, /ta, /en)</li>
                <li>Bot will translate the message to your chosen language</li>
            </ol>
            <p><strong>Max message length:</strong> {bot.config.MAX_MESSAGE_LENGTH} characters</p>
        </body>
    </html>
    '''

@app.route('/set-webhook', methods=['POST'])
def set_webhook():
    """Endpoint to set webhook URL"""
    try:
        webhook_url = os.getenv('WEBHOOK_URL')
        if not webhook_url:
            return jsonify({'error': 'WEBHOOK_URL environment variable not set'}), 400
        
        bot.set_webhook(f"{webhook_url}/webhook")
        return jsonify({'status': 'webhook set', 'url': f"{webhook_url}/webhook"}), 200
    except Exception as e:
        logger.error(f"Error setting webhook: {e}")
        return jsonify({'error': 'Failed to set webhook'}), 500

if __name__ == '__main__':
    # Set up webhook if running in production
    webhook_url = os.getenv('WEBHOOK_URL')
    if webhook_url:
        try:
            bot.set_webhook(f"{webhook_url}/webhook")
            logger.info(f"Webhook set to: {webhook_url}/webhook")
        except Exception as e:
            logger.error(f"Failed to set webhook: {e}")
    else:
        logger.warning("WEBHOOK_URL not set - webhook not configured")
    
    # Start Flask app
    port = int(os.getenv('PORT', 5000))
    debug_mode = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    
    logger.info(f"Starting server on port {port}")
    app.run(host='0.0.0.0', port=port, debug=debug_mode)
