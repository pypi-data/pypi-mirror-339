import os
from typing import Optional
import openai
from dotenv import load_dotenv
from .base import TranslationPlugin

class OpenAITranslationPlugin(TranslationPlugin):
    """OpenAI-based translation plugin."""
    
    def __init__(self):
        load_dotenv()
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.model = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")
    
    def translate(self, text: str, target_lang: str) -> str:
        """Translate text using OpenAI's API."""
        if not self.is_configured():
            raise Exception("OpenAI API key not configured")
        
        try:
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": f"You are a professional translator. Translate the following text to {target_lang}. Maintain the same tone and style."},
                    {"role": "user", "content": text}
                ],
                temperature=0.3
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            raise Exception(f"Translation failed: {str(e)}")
    
    def get_name(self) -> str:
        return "openai"
    
    def get_description(self) -> str:
        return "Uses OpenAI's GPT models for translation"
    
    def is_configured(self) -> bool:
        return bool(self.api_key) 