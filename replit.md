# Translation Bot Project

## Project Overview
A Telegram bot that provides instant translation of group messages into Indian regional languages using simple reply commands. The bot supports 13 Indian languages and uses Google Translate API for translations.

## Architecture
- **Flask web server**: Handles webhook endpoints and health checks
- **Telegram Bot**: Processes incoming messages and replies with translations
- **Translation Service**: Interfaces with Google Translate API
- **Config System**: Manages language mappings and configuration
- **Rate Limiting**: Prevents abuse with in-memory rate limiting

## Recent Changes (August 2025)
### Render Deployment Preparation
- ✓ Updated project name in pyproject.toml from "repl-nix-workspace" to "telegram-translation-bot"
- ✓ Created requirements-render.txt with production dependencies including Gunicorn
- ✓ Created render.yaml for automated Render deployment configuration
- ✓ Created wsgi.py as production WSGI entry point
- ✓ Updated main.py with production server detection and webhook setup
- ✓ Updated start.sh for Render compatibility with Gunicorn support
- ✓ Created comprehensive README.md with Render deployment instructions
- ✓ Created DEPLOYMENT.md with step-by-step deployment guide
- ✓ Created .env.example for environment variable reference
- ✓ Removed all Replit-specific dependencies and configurations

## Deployment Platform
- **Target**: Render (platform-independent, no Replit dependencies)
- **Runtime**: Python 3.11+
- **Framework**: Flask with Gunicorn WSGI server
- **Dependencies**: Flask, python-telegram-bot, googletrans, requests, gunicorn
- **Production**: Uses Gunicorn for production deployment
- **Development**: Falls back to Flask dev server for local testing

## Environment Variables Required
- TELEGRAM_BOT_TOKEN: Bot token from BotFather
- WEBHOOK_URL: Render app URL for webhook endpoint
- PORT: Port number (provided by Render automatically)
- MAX_MESSAGE_LENGTH: Maximum message length (default: 5000)
- RATE_LIMIT_SECONDS: Rate limiting interval (default: 2)

## User Preferences
- Simple, everyday language in communications
- Focus on deployment readiness and platform independence
- Clear documentation of architectural changes