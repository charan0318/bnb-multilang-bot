
# Telegram Translation Bot

A smart Telegram bot that translates messages to multiple Indian languages and English.

## Features

- Supports 15 languages including Hindi, Tamil, Telugu, Bengali, English, etc.
- Real-time translation via webhook
- Rate limiting to prevent abuse
- Message length limit of 5000 characters
- Clean, responsive interface

## Environment Variables Required

```bash
TELEGRAM_BOT_TOKEN=your_bot_token_here
WEBHOOK_URL=https://yourdomain.com
PORT=5000
MAX_MESSAGE_LENGTH=5000
RATE_LIMIT_SECONDS=2
```

## Deployment

1. Set the required environment variables
2. Install dependencies: `pip install -r requirements.txt`
3. Run the application: `python main.py`

## Usage

1. Add the bot to your Telegram group
2. Reply to any message with a language command (e.g., `/hi`, `/en`, `/ta`)
3. Bot will translate the original message to your chosen language

## Health Check

Visit `/health` endpoint to check if the service is running properly.

## Webhook Setup

The bot automatically sets up the webhook on startup if `WEBHOOK_URL` is provided.
You can also manually set it by calling the `/set-webhook` endpoint.
