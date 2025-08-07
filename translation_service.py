import os
import logging
from typing import Optional
from deep_translator import GoogleTranslator
import time

logger = logging.getLogger(__name__)

class TranslationService:
    def __init__(self):
        self.last_request_time = 0
        self.min_request_interval = 0.1  # Minimum 100ms between requests
        
        logger.info("Translation service initialized with deep-translator")
    
    def _rate_limit(self):
        """Simple rate limiting for Google Translate API"""
        current_time = time.time()
        time_since_last = current_time - self.last_request_time
        
        if time_since_last < self.min_request_interval:
            sleep_time = self.min_request_interval - time_since_last
            time.sleep(sleep_time)
        
        self.last_request_time = time.time()
    
    def translate(self, text: str, target_language: str, source_language: str = 'auto') -> Optional[str]:
        """
        Translate text to target language
        
        Args:
            text: Text to translate
            target_language: Target language code (e.g., 'hi', 'ta')
            source_language: Source language code (default: 'auto' for auto-detection)
        
        Returns:
            Translated text or None if translation fails
        """
        if not text or not text.strip():
            return None
        
        try:
            # Apply rate limiting
            self._rate_limit()
            
            # Create translator instance with deep-translator
            translator = GoogleTranslator(source=source_language, target=target_language)
            
            # Perform translation
            translated_text = translator.translate(text.strip())
            
            if translated_text and translated_text.strip():
                # Log successful translation
                logger.debug(f"Translated '{text[:50]}...' to {target_language}")
                
                return translated_text.strip()
            else:
                logger.warning(f"Empty translation result for text: {text[:50]}...")
                return None
                
        except Exception as e:
            logger.error(f"Translation failed for text '{text[:50]}...': {e}")
            
            # Check if it's a language not supported error
            if "invalid" in str(e).lower() or "not supported" in str(e).lower():
                logger.warning(f"Language {target_language} not supported")
            
            return None
    
    def detect_language(self, text: str) -> Optional[str]:
        """
        Detect the language of given text
        
        Args:
            text: Text to analyze
        
        Returns:
            Detected language code or None if detection fails
        """
        if not text or not text.strip():
            return None
        
        try:
            self._rate_limit()
            
            # Use GoogleTranslator for detection
            from deep_translator import single_detection
            detected_lang = single_detection(text.strip(), api_key=None)
            
            if detected_lang:
                return detected_lang
            
        except Exception as e:
            logger.error(f"Language detection failed for text '{text[:50]}...': {e}")
        
        return None
    
    def is_translatable(self, text: str) -> bool:
        """
        Check if text contains translatable content
        
        Args:
            text: Text to check
        
        Returns:
            True if text is translatable
        """
        if not text or not text.strip():
            return False
        
        # Check if text is mostly URLs, mentions, or hashtags
        words = text.split()
        non_translatable_count = 0
        
        for word in words:
            if (word.startswith(('http://', 'https://', 'www.', '@', '#')) or 
                word.endswith(('.com', '.org', '.net', '.io', '.co'))):
                non_translatable_count += 1
        
        # If more than 70% of words are non-translatable, skip translation
        if len(words) > 0 and (non_translatable_count / len(words)) > 0.7:
            return False
        
        return True
