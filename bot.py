import os
import json
import logging
import time
from typing import Dict, Optional
import requests
from telegram import Bot, Update
from translation_service import TranslationService
from config import Config

logger = logging.getLogger(__name__)

class TranslationBot:
    def __init__(self):
        self.bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
        if not self.bot_token:
            raise ValueError("TELEGRAM_BOT_TOKEN environment variable is required")

        self.bot = Bot(token=self.bot_token)
        self.translation_service = TranslationService()
        self.config = Config()

        # Rate limiting storage (in production, use Redis)
        self.rate_limits = {}
        self.last_bot_messages = {}  # Store last bot message IDs for cleanup

        logger.info("Translation bot initialized successfully")

    def set_webhook(self, webhook_url: str):
        """Set webhook for the bot"""
        try:
            response = self.bot.set_webhook(url=webhook_url)
            if response:
                logger.info("Webhook set successfully")
            else:
                logger.error("Failed to set webhook")
        except Exception as e:
            logger.error(f"Error setting webhook: {e}")

    async def handle_webhook_update(self, update_data: dict):
        """Handle incoming webhook updates"""
        try:
            update = Update.de_json(update_data, self.bot)
            if update.message:
                await self.handle_message(update.message)
        except Exception as e:
            logger.error(f"Error processing update: {e}")

    def is_rate_limited(self, user_id: int, chat_id: int) -> bool:
        """Check if user is rate limited"""
        key = f"{user_id}_{chat_id}"
        current_time = time.time()

        if key in self.rate_limits:
            last_request = self.rate_limits[key]
            if current_time - last_request < self.config.RATE_LIMIT_SECONDS:
                return True

        self.rate_limits[key] = current_time
        return False

    def clean_previous_bot_message(self, chat_id: int, message_id: int):
        """Delete previous bot translation for the same original message"""
        key = f"{chat_id}_{message_id}"
        if key in self.last_bot_messages:
            try:
                self.bot.delete_message(chat_id=chat_id, message_id=self.last_bot_messages[key])
                logger.debug(f"Deleted previous bot message {self.last_bot_messages[key]}")
            except Exception as e:
                logger.debug(f"Could not delete previous message: {e}")
            finally:
                del self.last_bot_messages[key]

    def extract_text_content(self, message) -> Optional[str]:
        """Extract only text content from a message, ignoring media"""
        if not message:
            return None

        text = message.text or message.caption
        if not text or len(text.strip()) == 0:
            return None

        return text.strip()

    async def send_help_message(self, chat_id: int, reply_to_message_id: int):
        """Send help message with available commands"""
        languages_list = []
        for cmd in self.config.get_supported_commands():
            lang_name = self.config.get_language_name(cmd)
            languages_list.append(f"{cmd} - {lang_name}")

        help_text = f"""🤖 **Smart Group Translation Bot**

**How to use:**
Reply to any message with a language command to translate it.

**Available commands:**
{chr(10).join(languages_list)}

**Examples:**
• Reply with `/hi` to translate to Hindi
• Reply with `/en` to translate to English  
• Reply with `/ta` to translate to Tamil

**Features:**
• Supports {len(self.config.languages)} languages
• Max {self.config.MAX_MESSAGE_LENGTH} characters per message
• Smart rate limiting to prevent spam

Ready to break language barriers! 🌍"""

        await self.bot.send_message(
            chat_id=chat_id,
            text=help_text,
            reply_to_message_id=reply_to_message_id,
            parse_mode='Markdown'
        )

    async def handle_message(self, message):
        """Handle incoming messages"""
        try:
            text = self.extract_text_content(message)
            if not text:
                return

            # Check if it's a translation command
            if not text.startswith('/'):
                return

            command = text.split()[0].lower()
            language_code = self.config.get_language_code(command)

            if not language_code:
                # Handle help command or unknown command
                if command in ['/start', '/help']:
                    await self.send_help_message(message.chat.id, message.message_id)
                return

            # If no reply message, send instructions
            if not message.reply_to_message:
                await self.bot.send_message(
                    chat_id=message.chat.id,
                    text=f"🔄 To translate a message to {self.config.get_language_name(command)}, reply to any message with `{command}`\n\nSupported languages: {', '.join(self.config.get_supported_commands())}",
                    reply_to_message_id=message.message_id,
                    parse_mode='Markdown'
                )
                return

            # Rate limiting check
            if self.is_rate_limited(message.from_user.id, message.chat.id):
                await self.bot.send_message(
                    chat_id=message.chat.id,
                    text="⏳ Please wait a moment before requesting another translation.",
                    reply_to_message_id=message.message_id
                )
                return

            # Extract text from replied message
            original_text = self.extract_text_content(message.reply_to_message)
            if not original_text:
                await self.bot.send_message(
                    chat_id=message.chat.id,
                    text="❌ Cannot translate this message - no text content found.",
                    reply_to_message_id=message.message_id
                )
                return

            # Check message length
            if len(original_text) > self.config.MAX_MESSAGE_LENGTH:
                await self.bot.send_message(
                    chat_id=message.chat.id,
                    text=f"❌ Message too long (max {self.config.MAX_MESSAGE_LENGTH} characters).",
                    reply_to_message_id=message.message_id
                )
                return

            # Clean previous bot translation for this message
            self.clean_previous_bot_message(message.chat.id, message.reply_to_message.message_id)

            # Translate the message
            try:
                translated_text = self.translation_service.translate(original_text, language_code)

                if not translated_text:
                    await self.bot.send_message(
                        chat_id=message.chat.id,
                        text="❌ Translation failed. Please try again.",
                        reply_to_message_id=message.message_id
                    )
                    return

                # Get language name for display
                language_name = self.config.get_language_name(command)

                # Send translation
                response_text = f"🔄 **Translation to {language_name}:**\n\n{translated_text}"

                sent_message = await self.bot.send_message(
                    chat_id=message.chat.id,
                    text=response_text,
                    reply_to_message_id=message.reply_to_message.message_id,
                    parse_mode='Markdown'
                )

                # Store bot message ID for future cleanup
                key = f"{message.chat.id}_{message.reply_to_message.message_id}"
                self.last_bot_messages[key] = sent_message.message_id

                logger.info(f"Translation completed: {command} for user {message.from_user.id}")

            except Exception as e:
                logger.error(f"Translation error: {e}")
                await self.bot.send_message(
                    chat_id=message.chat.id,
                    text="❌ Translation service unavailable. Please try again later.",
                    reply_to_message_id=message.message_id
                )

        except Exception as e:
            logger.error(f"Error handling message: {e}")