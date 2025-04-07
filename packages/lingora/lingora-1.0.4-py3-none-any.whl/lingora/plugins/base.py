from abc import ABC, abstractmethod
from typing import Optional

class TranslationPlugin(ABC):
    """Base class for translation plugins."""
    
    @abstractmethod
    def translate(self, text: str, source_lang: str, target_lang: str) -> str:
        """
        Translate XML content from source language to target language
        
        Args:
            text: Full XML content to translate
            source_lang: Source language code (e.g., 'en')
            target_lang: Target language code (e.g., 'de')
            
        Returns:
            Translated XML content
        """
        pass
    
    @abstractmethod
    def get_name(self) -> str:
        """Get the name of the plugin."""
        pass
    
    @abstractmethod
    def get_description(self) -> str:
        """Get a description of the plugin."""
        pass
    
    @abstractmethod
    def is_configured(self) -> bool:
        """Check if the plugin is properly configured with necessary credentials."""
        pass 