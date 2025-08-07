
# Telegram Translation Bot

A smart Telegram bot that translates messages to multiple Indian languages using Google Translate API.

## Features

- Supports 13 Indian languages including Hindi, Tamil, Telugu, Bengali, and more
- Real-time translation via webhook integration
- Rate limiting to prevent abuse (2-second cooldown per user)
- Message length limit of 5000 characters
- Clean, responsive web interface
- Production-ready with Gunicorn WSGI server

## Supported Languages

- Hindi (हिन्दी) - `/hi`
- Tamil (தமிழ்) - `/ta`
- Telugu (తెలుగు) - `/te`
- Bengali (বাংলা) - `/bn`
- Marathi (मराठी) - `/mr`
- Gujarati (ગુજરાતી) - `/gu`
- Kannada (ಕನ್ನಡ) - `/kn`
- Malayalam (മലയാളം) - `/ml`
- Punjabi (ਪੰਜਾਬੀ) - `/pa`
- Odia (ଓଡ଼ିଆ) - `/or`
- Assamese (অসমীয়া) - `/as`
- Urdu (اردو) - `/ur`
- Sanskrit (संस्कृत) - `/sa`

## Deployment on Render

### Prerequisites
1. Create a Telegram bot via [@BotFather](https://t.me/botfather) and get the bot token
2. Sign up for a [Render](https://render.com) account

### Deployment Steps

1. **Clone this repository** or upload the code to your GitHub repository

2. **Connect to Render:**
   - Go to [Render Dashboard](https://dashboard.render.com)
   - Click "New +" and select "Web Service"
   - Connect your GitHub repository

3. **Configure the service:**
   - **Runtime:** Python 3
   - **Build Command:** `pip install -r requirements-render.txt`
   - **Start Command:** `gunicorn --bind 0.0.0.0:$PORT wsgi:app`

4. **Set Environment Variables:**
   ```bash
   TELEGRAM_BOT_TOKEN=your_bot_token_from_botfather
   WEBHOOK_URL=https://your-app-name.onrender.com
   MAX_MESSAGE_LENGTH=5000
   RATE_LIMIT_SECONDS=2
   ```

5. **Deploy:** Click "Create Web Service" and wait for deployment

6. **Set the webhook:** After deployment, visit `/set-webhook` endpoint or the webhook will be automatically configured

### Alternative Deployment (Manual)

```bash
# Install dependencies
pip install -r requirements-render.txt

# Set environment variables
export TELEGRAM_BOT_TOKEN=your_token_here
export WEBHOOK_URL=https://yourdomain.com

# Run with Gunicorn (production)
gunicorn --bind 0.0.0.0:5000 wsgi:app

# Or run with Flask development server
python main.py
```

## Usage

1. **Add the bot to your Telegram group** or chat with it directly
2. **Reply to any message** with a language command:
   - `/hi` for Hindi
   - `/ta` for Tamil
   - `/te` for Telugu
   - `/bn` for Bengali
   - And so on...
3. **The bot will translate** the original message to your chosen language

### Example:
```
Original message: "Hello, how are you?"
Reply with: /hi
Bot response: "नमस्ते, आप कैसे हैं?"
```

## API Endpoints

- **`/`** - Bot information and status page
- **`/health`** - Health check endpoint for monitoring
- **`/webhook`** - Telegram webhook endpoint (POST)
- **`/set-webhook`** - Manually set webhook URL (POST)

## Development

### Local Development
```bash
# Install dependencies
pip install -r requirements-render.txt

# Set environment variables
export TELEGRAM_BOT_TOKEN=your_token
export WEBHOOK_URL=https://your-ngrok-url.com  # Use ngrok for local testing

# Run development server
python main.py
```

### Project Structure
```
telegram-translation-bot/
├── main.py                 # Flask app and main entry point
├── wsgi.py                 # WSGI entry point for production
├── bot.py                  # Telegram bot logic
├── translation_service.py  # Google Translate integration
├── config.py              # Configuration and language mappings
├── languages.json         # Language codes and names
├── requirements-render.txt # Production dependencies
├── render.yaml            # Render deployment configuration
└── README.md              # This file
```

## Monitoring

The bot includes comprehensive logging and health monitoring:
- All translations are logged with source and target languages
- Rate limiting prevents abuse
- Health check endpoint for uptime monitoring
- Error handling with detailed logging

## License

This project is open source and available under the MIT License.
