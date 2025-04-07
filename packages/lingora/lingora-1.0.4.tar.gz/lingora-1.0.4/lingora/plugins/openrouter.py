from typing import Optional
from dotenv import load_dotenv
import os
import json
import requests
from .base import TranslationPlugin

class OpenRouterPlugin(TranslationPlugin):
    def __init__(self):
        load_dotenv()
        self.api_key = os.getenv("OPENROUTER_API_KEY")
        self.base_url = "https://openrouter.ai/api/v1"
        self.model = os.getenv("OPENROUTER_MODEL", "anthropic/claude-3-sonnet")

    def translate(self, text: str, source_lang: str, target_lang: str) -> str:
        if not self.is_configured():
            raise ValueError("OpenRouter API key not configured")

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        prompt = f"Please translate the text between the `<s>` tag in the following XML file from {source_lang} to {target_lang} (these are shortened language codes). Provide only the translation, no explanations:\n\n{text}"
        
        print(prompt)

        data = {
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}]
        }

        response = requests.post(
            f"{self.base_url}/chat/completions",
            headers=headers,
            json=data
        )

        if response.status_code != 200:
            raise Exception(f"Translation failed: {response.text}")

        result = response.json()
        translated_text = result["choices"][0]["message"]["content"].strip()
        return self._clean_xml_response(translated_text)

    def _clean_xml_response(self, text: str) -> str:
        """Remove any content before the XML declaration."""
        if '<?xml' in text:
            return text[text.index('<?xml'):]
        return text

    def get_name(self) -> str:
        return "openrouter"

    def get_description(self) -> str:
        return "Translation plugin using OpenRouter API"

    def is_configured(self) -> bool:
        return bool(self.api_key) 