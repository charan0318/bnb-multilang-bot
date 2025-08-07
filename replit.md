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

### Python 3.13 Compatibility & Dependency Resolution (August 7, 2025)
- ✓ **Root Cause Identified**: `python-telegram-bot==13.15` imports deprecated `imghdr` module
- ✓ **Dependency Conflict Found**: `googletrans==4.0.0rc1` requires `httpx==0.13.3` vs `python-telegram-bot==20.8` requires `httpx~=0.26.0`
- ✓ **Solution Applied**: Migrated from `googletrans` to `deep-translator==1.11.4` (no deprecated dependencies)
- ✓ **Translation Service**: Updated to use GoogleTranslator from deep-translator library
- ✓ **Runtime Target**: Set to Python 3.12.3 for modern compatibility without deprecated modules
- ✓ **Tested Working**: Translation functionality verified with Hindi translation test

### Render Deployment Timeout Fixes (August 7, 2025)
- ✓ **Host Binding**: Fixed server to bind to `0.0.0.0` instead of localhost per Render docs
- ✓ **Port Configuration**: Updated default port to 10000 (Render's default) in all entry points
- ✓ **Gunicorn Timeout**: Increased timeout from 60s to 120s to prevent worker timeouts  
- ✓ **Keep-Alive Settings**: Added `--keep-alive 2` and `--max-requests 1000` for stability
- ✓ **Internal Pings**: Fixed keep-alive worker to ping `0.0.0.0` instead of `127.0.0.1`

## Deployment Platform
- **Target**: Render (platform-independent, no Replit dependencies)
- **Runtime**: Python 3.11+
- **Framework**: Flask with Gunicorn WSGI server
- **Dependencies**: Flask, python-telegram-bot, deep-translator, requests, gunicorn
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