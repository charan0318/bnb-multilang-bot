# Bot Troubleshooting Guide

## Common Issues and Solutions

### 1. Bot Not Responding on Render

**Symptoms:**
- Bot deployed successfully on Render
- Health check passes
- But bot doesn't respond to messages

**Most Common Causes:**

#### A. Webhook URL Mismatch
**Problem:** The webhook URL doesn't match your actual Render app URL
**Solution:**
1. Check your Render app URL (should be `https://your-app-name.onrender.com`)
2. Update the `WEBHOOK_URL` environment variable in Render to match exactly
3. Visit `/set-webhook` endpoint to manually reset webhook

#### B. Bot Token Issues
**Problem:** Invalid or missing bot token
**Solution:**
1. Get a fresh bot token from @BotFather on Telegram
2. Set `TELEGRAM_BOT_TOKEN` environment variable in Render
3. Restart the service

#### C. Webhook Not Set
**Problem:** Webhook wasn't configured properly during startup
**Solution:**
1. Check logs for "Webhook set successfully" message
2. Visit `/webhook-info` endpoint to check webhook status
3. Manually set webhook by visiting `/set-webhook` endpoint

### 2. Debug Steps

#### Step 1: Check Service Status
Visit your app URL: `https://your-app-name.onrender.com`
- Should show bot information page
- Note the number of supported languages

#### Step 2: Check Health Endpoint
Visit: `https://your-app-name.onrender.com/health`
- Should return: `{"status": "healthy", "service": "translation-bot"}`

#### Step 3: Check Webhook Status
Visit: `https://your-app-name.onrender.com/webhook-info`
- Check if `url` field matches your app URL + `/webhook`
- Look for any error messages

#### Step 4: Test Translation Service
Send POST request to: `https://your-app-name.onrender.com/test-translation`
```json
{
  "text": "Hello world",
  "target_lang": "hi"
}
```

#### Step 5: Check Render Logs
In Render dashboard:
1. Go to your service
2. Click "Logs" tab
3. Look for error messages
4. Check for webhook setup messages

### 3. Environment Variables Checklist

Make sure these are set in Render:

| Variable | Example | Required |
|----------|---------|----------|
| `TELEGRAM_BOT_TOKEN` | `123456789:ABC-DEF...` | Yes |
| `WEBHOOK_URL` | `https://your-app.onrender.com` | Yes |
| `MAX_MESSAGE_LENGTH` | `5000` | No |
| `RATE_LIMIT_SECONDS` | `2` | No |

### 4. Test Bot Manually

1. **Find your bot on Telegram:**
   - Search for your bot username
   - Start a conversation

2. **Test basic commands:**
   - Send `/start` or `/help`
   - Should receive help message with language list

3. **Test translation:**
   - Send any message
   - Reply to that message with `/hi`
   - Should translate to Hindi

### 5. Common Error Messages

#### "TELEGRAM_BOT_TOKEN environment variable is required"
- Set the bot token in Render environment variables
- Get token from @BotFather if needed

#### "WEBHOOK_URL not set - webhook not configured"
- Set WEBHOOK_URL environment variable
- Should be your Render app URL

#### "Failed to set webhook"
- Check if bot token is valid
- Verify webhook URL is accessible
- Try manual webhook setup

#### "Translation service unavailable"
- Google Translate API might be temporarily down
- Check internet connectivity
- Restart the service

### 6. Manual Webhook Setup

If automatic webhook setup fails:

1. **Get webhook info:**
   ```
   GET https://your-app.onrender.com/webhook-info
   ```

2. **Set webhook manually:**
   ```
   POST https://your-app.onrender.com/set-webhook
   ```

3. **Verify setup:**
   Check logs for "Webhook set successfully"

### 7. Testing Webhook Locally

For local development:
1. Use ngrok: `ngrok http 5000`
2. Set WEBHOOK_URL to ngrok URL
3. Test with real Telegram bot

### 8. Production Checklist

Before going live:
- [ ] Bot token is valid and correct
- [ ] Webhook URL matches Render app URL exactly
- [ ] Health check returns 200
- [ ] Webhook info shows correct URL
- [ ] Test translation works
- [ ] Bot responds to /start command
- [ ] Translation commands work in groups

### 9. Getting Help

If issues persist:
1. Check Render service logs
2. Test each endpoint individually
3. Verify environment variables
4. Try redeploying the service
5. Check if bot is blocked or restricted

### 10. Monitoring

Set up monitoring:
- Use `/health` endpoint for uptime monitoring
- Monitor `/webhook-info` for webhook issues
- Check logs for translation errors
- Monitor rate limiting effectiveness