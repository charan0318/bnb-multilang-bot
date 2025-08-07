# Render Deployment Guide

This guide will help you deploy the Telegram Translation Bot on Render.

## Pre-Deployment Checklist

### 1. Telegram Bot Setup
- [ ] Create a bot via [@BotFather](https://t.me/botfather)
- [ ] Get the bot token (format: `123456789:ABC-DEF1234ghIkl-zyx57W2v1u123ew11`)
- [ ] Note down the bot username

### 2. Render Account
- [ ] Sign up for [Render](https://render.com) account
- [ ] Verify your account

### 3. Code Repository
- [ ] Push code to GitHub repository
- [ ] Ensure all files are committed:
  - `main.py` - Main application
  - `wsgi.py` - Production WSGI entry point
  - `bot.py` - Bot logic
  - `translation_service.py` - Translation service
  - `config.py` - Configuration
  - `languages.json` - Language mappings
  - `requirements-render.txt` - Dependencies
  - `render.yaml` - Render configuration

## Deployment Steps

### Step 1: Create Web Service on Render

1. Go to [Render Dashboard](https://dashboard.render.com)
2. Click "New +" → "Web Service"
3. Connect your GitHub repository
4. Configure the service:
   - **Name:** `telegram-translation-bot` (or your preferred name)
   - **Runtime:** `Python 3`
   - **Branch:** `main` (or your default branch)
   - **Root Directory:** Leave empty if code is in root
   - **Build Command:** `pip install -r requirements-render.txt`
   - **Start Command:** `gunicorn --bind 0.0.0.0:$PORT wsgi:app`

### Step 2: Configure Environment Variables

Add these environment variables in Render:

| Variable | Value | Description |
|----------|-------|-------------|
| `TELEGRAM_BOT_TOKEN` | `your_bot_token` | Bot token from BotFather |
| `WEBHOOK_URL` | `https://your-app-name.onrender.com` | Your Render app URL |
| `MAX_MESSAGE_LENGTH` | `5000` | Maximum message length |
| `RATE_LIMIT_SECONDS` | `2` | Rate limiting interval |

**Important:** Replace `your-app-name` with your actual Render app name.

### Step 3: Deploy

1. Click "Create Web Service"
2. Wait for the build to complete (usually 2-5 minutes)
3. Check the logs for any errors
4. Once deployed, note your app URL: `https://your-app-name.onrender.com`

### Step 4: Set Webhook

The webhook should be set automatically on startup. To verify:

1. Visit your app URL to see the bot status page
2. If webhook is not set, visit: `https://your-app-name.onrender.com/set-webhook`
3. Check the logs to confirm webhook was configured

## Verification

### 1. Check App Status
- Visit `https://your-app-name.onrender.com` - should show bot info page
- Visit `https://your-app-name.onrender.com/health` - should return healthy status

### 2. Test Bot
1. Find your bot on Telegram
2. Send a message to the bot
3. Reply to any message with `/hi` or another language command
4. Bot should translate the message

### 3. Check Logs
- In Render dashboard, go to your service
- Click "Logs" tab to monitor bot activity

## Troubleshooting

### Common Issues

1. **Build fails:**
   - Check requirements-render.txt syntax
   - Ensure all dependencies are available

2. **Bot doesn't respond:**
   - Verify TELEGRAM_BOT_TOKEN is correct
   - Check webhook URL is set properly
   - Review logs for errors

3. **Webhook errors:**
   - Ensure WEBHOOK_URL matches your Render app URL exactly
   - Visit /set-webhook endpoint manually

4. **Translation failures:**
   - Check Google Translate service availability
   - Review rate limiting settings

### Environment Variables

Make sure these are set correctly in Render:

```bash
TELEGRAM_BOT_TOKEN=123456789:ABC-DEF1234ghIkl-zyx57W2v1u123ew11
WEBHOOK_URL=https://your-app-name.onrender.com
MAX_MESSAGE_LENGTH=5000
RATE_LIMIT_SECONDS=2
```

### Logs to Monitor

Watch for these log messages:
- `Translation bot initialized successfully`
- `Webhook set to: https://your-app-name.onrender.com/webhook`
- `Starting server on port 5000`

## Post-Deployment

1. **Test thoroughly** with different languages
2. **Monitor logs** for any errors
3. **Add bot to groups** where translation is needed
4. **Share bot username** with users

## Updates

To update the bot:
1. Push changes to your GitHub repository
2. Render will automatically redeploy
3. Check logs to ensure successful deployment

## Support

If you encounter issues:
1. Check the logs in Render dashboard
2. Verify environment variables
3. Test webhook configuration
4. Review Telegram bot settings

## Cost Considerations

- Render's free tier includes 750 hours/month
- Bot should stay within free tier limits for normal usage
- Monitor usage in Render dashboard

Your bot should now be live and ready to translate messages on Telegram!