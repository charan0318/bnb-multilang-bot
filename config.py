import json
import os
import logging
from typing import Dict, Optional

logger = logging.getLogger(__name__)

class Config:
    def __init__(self):
        # Load language mappings
        self.languages = self._load_languages()
        
        # Configuration constants
        self.MAX_MESSAGE_LENGTH = int(os.getenv('MAX_MESSAGE_LENGTH', '5000'))
        self.RATE_LIMIT_SECONDS = int(os.getenv('RATE_LIMIT_SECONDS', '2'))
        self.WEBHOOK_PORT = int(os.getenv('PORT', '5000'))
        
        logger.info(f"Config loaded: {len(self.languages)} languages supported")
    
    def _load_languages(self) -> Dict:
        """Load language mappings from JSON file"""
        try:
            with open('languages.json', 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            logger.error("languages.json not found, using default languages")
            return self._get_default_languages()
        except json.JSONDecodeError as e:
            logger.error(f"Error parsing languages.json: {e}")
            return self._get_default_languages()
    
    def _get_default_languages(self) -> Dict:
        """Return default Indian language mappings"""
        return {
            "/hi": {"code": "hi", "name": "Hindi"},
            "/ta": {"code": "ta", "name": "Tamil"},
            "/te": {"code": "te", "name": "Telugu"},
            "/bn": {"code": "bn", "name": "Bengali"},
            "/mr": {"code": "mr", "name": "Marathi"},
            "/gu": {"code": "gu", "name": "Gujarati"},
            "/kn": {"code": "kn", "name": "Kannada"},
            "/ml": {"code": "ml", "name": "Malayalam"},
            "/pa": {"code": "pa", "name": "Punjabi"},
            "/or": {"code": "or", "name": "Odia"}
        }
    
    def get_language_code(self, command: str) -> Optional[str]:
        """
        Get language code for a command
        
        Args:
            command: Command string (e.g., '/hi')
        
        Returns:
            Language code or None if not found
        """
        command = command.lower().strip()
        if command in self.languages:
            return self.languages[command]["code"]
        return None
    
    def get_language_name(self, command: str) -> Optional[str]:
        """
        Get language name for a command
        
        Args:
            command: Command string (e.g., '/hi')
        
        Returns:
            Language name or None if not found
        """
        command = command.lower().strip()
        if command in self.languages:
            return self.languages[command]["name"]
        return None
    
    def get_supported_commands(self) -> list:
        """Get list of all supported commands"""
        return list(self.languages.keys())
    
    def is_supported_command(self, command: str) -> bool:
        """Check if command is supported"""
        return command.lower().strip() in self.languages
