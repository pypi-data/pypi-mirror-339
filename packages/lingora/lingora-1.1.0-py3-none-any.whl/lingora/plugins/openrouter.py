from typing import Optional
from dotenv import load_dotenv, find_dotenv
import os
import json
import requests
from .base import TranslationPlugin
from rich.console import Console

console = Console()
current_working_directory = os.getcwd()
dotenv_path = os.path.join(current_working_directory, '.env')

class OpenRouterPlugin(TranslationPlugin):
    def __init__(self):
        load_dotenv(dotenv_path)
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

        prompt = f"Translate the following data from {source_lang} to {target_lang}: {text}"

        prompt_template = os.getenv('PROMPT_TEXT')
        if prompt_template:
            prompt_template = prompt_template.replace('\\n', '\n')
            prompt = prompt_template.format(source_lang=source_lang, target_lang=target_lang, text=text)
        else:
            console.print("[red]Warning: PROMPT_TEXT is not set in the .env file, the default prompt will be used.[/red]")

        # console.print("here is the prompt text:")
        # console.print(prompt)

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
        console.print("removing extra before xml")
        if '<?xml' in text:
        	# console.print(f"Cleaning XML response: {text}")
            text = text[text.index('<?xml'):]
        if text.endswith('```'):
           text = text[:-3]
        console.print("no <?xml> tag found")
        return text

    def get_name(self) -> str:
        return "openrouter"

    def get_description(self) -> str:
        return "Translation plugin using OpenRouter API"

    def is_configured(self) -> bool:
        return bool(self.api_key)
