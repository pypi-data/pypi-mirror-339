from typing import Dict
from .base import TranslationPlugin

class SimulatorTranslationPlugin(TranslationPlugin):
    """A simple simulator plugin for testing translations from English to German."""
    
    def __init__(self):
        # Common UI string translations
        self.translations: Dict[str, str] = {
            "My App": "Meine App",
            "This is the description for my app": "Dies ist die Beschreibung für meine App",
            "Save": "Speichern",
            "Cancel": "Abbrechen",
            "Delete": "Löschen",
            "Edit": "Bearbeiten",
            "Close": "Schließen",
            "Open": "Öffnen",
            "Settings": "Einstellungen",
            "Help": "Hilfe",
            "Search": "Suchen",
            "Menu": "Menü",
            "File": "Datei",
            "New": "Neu",
            "Welcome": "Willkommen",
            "Login": "Anmelden",
            "Logout": "Abmelden",
            "Username": "Benutzername",
            "Password": "Passwort",
            "Error": "Fehler",
            "Success": "Erfolg",
            "Loading": "Laden",
            "Please wait": "Bitte warten",
            "Yes": "Ja",
            "No": "Nein",
            "OK": "OK",
            "Submit": "Absenden",
            "pass" : "richtig",
            "fail" : "gescheitert",
            "description": "Beschreibung",
        }
    
    def translate(self, text: str,  source_lang: str,  target_lang: str) -> str:
        """
        Simulate translation from English to German.
        Only works for target_lang='de' and exact matches in the dictionary.
        """
        if source_lang != "en":
            raise Exception("Simulator-plugin only supports English (en) as source language")
        
        if target_lang != "de":
            raise Exception("Simulator-plugin only supports German (de) as target language")
        
        # Return the translation if it exists, otherwise return the original text
        return self.translations.get(text, text)
    
    def get_name(self) -> str:
        return "simulator"
    
    def get_description(self) -> str:
        return "Simulates translations from English to German for testing purposes"
    
    def is_configured(self) -> bool:
        return True  # Always configured since it's just a simulator 