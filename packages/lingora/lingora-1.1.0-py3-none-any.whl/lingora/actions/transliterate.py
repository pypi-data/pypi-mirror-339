"""Transliteration action implementation."""
import cyrtranslit
from rich.console import Console

from .base import Action

console = Console()

class TransliterateAction(Action):
    """Action for transliterating text between scripts."""

    def process(self, content: str, language: str, chunk_size: int = 5000, test: bool = False) -> str:
        """Process content by transliterating it to the target script."""
        file_length = len(content)
        console.print(f'The content has {file_length} codepoints.')
        
        if file_length > chunk_size:
            console.print(f"Input is above {chunk_size} codepoints. Processing in chunks...")
        
        translated_text = ""
        chunks = [content[i:i + chunk_size] for i in range(0, len(content), chunk_size)]
        
        for i, chunk in enumerate(chunks, 1):
            console.print(f"Processing chunk {i}/{len(chunks)} of {len(chunk)} codepoints")
            if test:
                translated_chunk = chunk
            else:
                console.print(f"Transliterating from {language}")
                translated_chunk = cyrtranslit.to_cyrillic(chunk, language)
            translated_text += translated_chunk
        
        return translated_text
