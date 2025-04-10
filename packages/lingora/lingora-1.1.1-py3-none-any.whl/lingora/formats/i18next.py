"""i18next/JSON format handler."""
import json
import os
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Any, Dict, List, Tuple
from rich.console import Console
import typer
from .base import FormatHandler
from ..plugins.base import TranslationPlugin

console = Console()

def load_json_file(file_path: str) -> Dict[str, Any]:
    """Load and parse a JSON file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        console.print(f"[red]Error: Invalid JSON file: {e}[/red]")
        raise typer.Exit(1)
    except FileNotFoundError:
        console.print(f"[red]Error: File not found: {file_path}[/red]")
        raise typer.Exit(1)

def save_json_file(data: Dict[str, Any], file_path: str) -> None:
    """Save data to a JSON file with proper formatting."""
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except Exception as e:
        console.print(f"[red]Error saving file: {e}[/red]")
        raise typer.Exit(1)

def find_json_files(directory: str) -> List[Path]:
    """Find all JSON files in directory recursively."""
    json_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.json'):
                json_files.append(Path(root) / file)
    return json_files

def create_id_mapping(json_data: Dict[str, Any], counter: int = 1) -> Tuple[Dict[str, Any], Dict[int, str], int]:
    """Create a mapping of strings to IDs and vice versa."""
    id_data = {}
    string_map = {}

    for key, value in json_data.items():
        if isinstance(value, str):
            id_data[key] = counter
            string_map[counter] = value
            counter += 1
        elif isinstance(value, dict):
            id_data[key], new_map, counter = create_id_mapping(value, counter)
            string_map.update(new_map)

    return id_data, string_map, counter

def generate_xml(json_files: List[Path], base_dir: Path) -> Tuple[Path, Dict[Path, Dict[int, str]]]:
    """Generate XML file from JSON files with ID mappings."""
    root = ET.Element("uistrings")
    string_maps = {}
    tmp_dir = Path("tmp")
    tmp_dir.mkdir(exist_ok=True)

    for json_file in json_files:
        relative_path = json_file.relative_to(base_dir)
        json_data = load_json_file(str(json_file))

        # Create folder nodes if needed
        current = root
        parts = relative_path.parent.parts
        for part in parts:
            folder = ET.SubElement(current, "folder", src=part)
            current = folder

        # Create file node
        file_node = ET.SubElement(current, "file", src=str(relative_path))

        # Generate ID mapping and save temporary JSON
        id_data, string_map, _ = create_id_mapping(json_data)
        string_maps[json_file] = string_map

        # Add string nodes to XML
        for id_num, text in string_map.items():
            string_node = ET.SubElement(file_node, "s", id=str(id_num))
            string_node.text = text

        # Save ID-mapped JSON
        tmp_json_path = tmp_dir / relative_path
        tmp_json_path.parent.mkdir(parents=True, exist_ok=True)
        save_json_file(id_data, str(tmp_json_path))

    # Save XML file
    xml_path = tmp_dir / "strings.xml"
    tree = ET.ElementTree(root)
    tree.write(str(xml_path), encoding="utf-8", xml_declaration=True)

    return xml_path, string_maps

def translate_xml(xml_path: Path, source_lang: str, target_lang: str, plugin: TranslationPlugin) -> Path:
    """Translate the XML file using the specified plugin."""
    # Read the entire XML file as a string
    with open(xml_path, 'r', encoding='utf-8') as f:
        xml_content = f.read()

    # Send the entire XML content to the plugin for translation
    translated_xml = plugin.translate(xml_content, source_lang, target_lang)

    # Save the translated XML to a new file
    output_path = xml_path.parent / f"translated_{xml_path.name}"
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(translated_xml)

    return output_path

def reconstruct_json(xml_path: Path, id_jsons_dir: Path, output_dir: Path) -> None:
    """Reconstruct JSON files from translated XML and ID mappings."""
    tree = ET.parse(str(xml_path))
    root = tree.getroot()

    for file_node in root.findall(".//file"):
        # Get the original JSON path and load ID mapping
        relative_path = Path(file_node.get("src"))
        id_json_path = id_jsons_dir / relative_path
        id_data = load_json_file(str(id_json_path))

        # Create translation mapping
        translations = {
            int(node.get("id")): node.text
            for node in file_node.findall("s")
        }

        # Reconstruct JSON with translations
        output_json = reconstruct_with_translations(id_data, translations)

        # Save translated JSON
        output_path = output_dir / relative_path
        save_json_file(output_json, str(output_path))

def reconstruct_with_translations(id_data: Dict[str, Any], translations: Dict[int, str]) -> Dict[str, Any]:
    """Reconstruct JSON structure with translated values."""
    result = {}
    for key, value in id_data.items():
        if isinstance(value, int):
            result[key] = translations.get(value, str(value))
        elif isinstance(value, dict):
            result[key] = reconstruct_with_translations(value, translations)
        else:
            result[key] = value
    return result

def translate_value(value: str, plugin: TranslationPlugin, source_lang: str, target_lang: str) -> str:
    """Translate a single string value using the provided plugin."""
    try:
        return plugin.translate(value, source_lang, target_lang)
    except Exception as e:
        console.print(f"[yellow]Warning: Failed to translate '{value}': {e}[/yellow]")
        return value

class I18NextHandler(FormatHandler):
    """Handler for i18next/JSON translation files."""

    def read(self, input_path: Path) -> Dict[str, Any]:
        """Read and parse i18next/JSON content."""
        return load_json_file(str(input_path))

    def write(self, content: Dict[str, Any], output_path: Path) -> None:
        """Write content in i18next/JSON format."""
        save_json_file(content, str(output_path))

    def validate(self, content: Any) -> bool:
        """Validate that the content is a valid i18next/JSON structure."""
        return isinstance(content, dict)
