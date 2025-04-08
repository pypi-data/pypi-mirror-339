"""XML format handler."""
import json
import os
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Any, Dict, List, Tuple, Union, Callable

from rich.console import Console
import typer

from .base import FormatHandler
from .intermediate import Intermediate
from ..plugins.base import TranslationPlugin

console = Console()

class XmlUiStringIntermediate(Intermediate):
    """Intermediate format for UI strings in XML format."""

    def __init__(self, process_func: Callable[[str, str, str], str], source_lang: str, target_lang: str, base_dir: Path, recursive: bool = True):
        """Initialize the XML intermediate format handler.
        
        Args:
            process_func: Function to process strings (e.g. translate)
            language: Target language code
            base_dir: Base directory containing source files
            recursive: Whether to process files recursively
        """
        self.process_func = process_func
        self.language = target_lang
        self.recursive = recursive
        self.base_dir = base_dir
        self.string_maps = {}
        self.source_lang = source_lang

    def _find_json_files(self, base_path: Path) -> List[Path]:
        """Find all JSON files in directory recursively."""
        json_files = []
        for root, _, files in os.walk(base_path):
            for file in files:
                if file.endswith('.json'):
                    json_files.append(Path(root) / file)
        return json_files

    def _save_json_file(self, data: Dict[str, Any], file_path: str) -> None:
        """Save data to a JSON file with proper formatting."""
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def _create_id_mapping(self, json_data: Dict[str, Any], counter: int = 1) -> Tuple[Dict[str, Any], Dict[int, str]]:
        """Create a mapping of strings to IDs and vice versa."""
        id_data = {}
        string_map = {}
        
        for key, value in json_data.items():
            if isinstance(value, str):
                id_data[key] = counter
                string_map[counter] = value
                counter += 1
            elif isinstance(value, dict):
                nested_id_data, nested_map, counter = self._create_id_mapping(value, counter)
                id_data[key] = nested_id_data
                string_map.update(nested_map)
        
        return id_data, string_map, counter

    def _generate_xml(self, json_files: List[Path], base_dir: Path) -> Tuple[Path, Dict[Path, Dict[int, str]]]:
        """Generate XML file from JSON files with ID mappings."""
        root = ET.Element("uistrings")
        string_maps = {}
        tmp_dir = base_dir / "tmp"
        tmp_dir.mkdir(exist_ok=True)
        
        for json_file in json_files:
            relative_path = json_file.relative_to(base_dir / self.source_lang)
            with open(json_file, 'r', encoding='utf-8') as f:
                json_data = json.load(f)
            
            # Create folder nodes if needed
            current = root
            parts = relative_path.parent.parts
            for part in parts:
                folder = current.find(f"folder[@src='{part}']")
                if folder is None:
                    folder = ET.SubElement(current, "folder", src=part)
                current = folder
            
            # Create file node
            file_node = ET.SubElement(current, "file", src=str(relative_path))
            
            # Generate ID mapping and save temporary JSON
            id_data, string_map, _ = self._create_id_mapping(json_data)
            string_maps[json_file] = string_map
            
            # Add string nodes to XML
            for id_num, text in string_map.items():
                string_node = ET.SubElement(file_node, "s", id=str(id_num))
                string_node.text = text
            
            # Save ID-mapped JSON
            tmp_json_path = tmp_dir / relative_path
            tmp_json_path.parent.mkdir(parents=True, exist_ok=True)
            self._save_json_file(id_data, str(tmp_json_path))
        
        # Save XML file
        xml_path = tmp_dir / "strings.xml"
        tree = ET.ElementTree(root)
        tree.write(str(xml_path), encoding='utf-8', xml_declaration=True)
        
        return xml_path, string_maps

    def _reconstruct_with_translations(self, id_data: Dict[str, Any], translations: Dict[int, str]) -> Dict[str, Any]:
        """Reconstruct JSON structure with translated values."""
        output = {}
        for key, value in id_data.items():
            if isinstance(value, int):
                output[key] = translations.get(value, '')
            elif isinstance(value, dict):
                output[key] = self._reconstruct_with_translations(value, translations)
        return output

    def transform_to(self, content: Any, chunk_size: int = None) -> str:
        """Transform UI strings from directory structure to intermediate XML format."""
        # Generate XML from JSON files
        xml_path, self.string_maps = self._generate_xml(self._find_json_files(self.base_dir), self.base_dir)
        
        translated_text = self.process_func(content, self.source_lang, self.language)

        return translated_text

    def transform_from(self, content: ET.Element) -> List[Dict[str, Any]]:
        """Transform from intermediate XML format back to UI strings."""
        result = []
        output_dir = self.base_dir / self.language
        output_dir.mkdir(parents=True, exist_ok=True)
        tmp_dir = self.base_dir / "tmp"

        for file_node in content.findall('.//file'):
            # Get the original JSON path
            relative_path = Path(file_node.get('src'))
            output_path = output_dir / relative_path
            tmp_json_path = tmp_dir / relative_path

            # Create translation mapping from the processed strings
            translations = {
                int(node.get('id')): node.text or ''
                for node in file_node.findall('s')
            }

            # Load ID-mapped JSON for structure
            with open(tmp_json_path, 'r', encoding='utf-8') as f:
                id_data = json.load(f)

            # Reconstruct JSON with translations
            output_json = self._reconstruct_with_translations(id_data, translations)
            result.append({
                'path': str(output_path),
                'content': output_json
            })

            # Save translated JSON
            output_path.parent.mkdir(parents=True, exist_ok=True)
            self._save_json_file(output_json, str(output_path))

        return result

    def read(self, path: Union[str, Path]) -> Dict[str, Any]:
        """Read UI strings from a file."""
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def read_recursive(self, directory: Union[str, Path]) -> List[Dict[str, Any]]:
        """Read UI strings from all matching files in a directory recursively."""
        directory = Path(directory) / self.source_lang
        print(f"Reading JSON files from {directory}...")
        json_files = self._find_json_files(directory)
        result = []
        for json_file in json_files:
            with open(json_file, 'r', encoding='utf-8') as f:
                json_data = json.load(f)
            result.append({
                'content': json_data,
                '_input_file': str(json_file)
            })
        return result

    def process(self, content: Any, chunk_size: int = None) -> str:
        """Process content using the process function."""
        if isinstance(content, dict) and '_input_file' in content:
            content = content['content']
        
        # Transform to XML
        xml_root = self.transform_to(content)
        
        # Process strings
        for string_node in xml_root.findall('.//s'):
            if string_node.text:
                string_node.text = self.process_func(string_node.text, self.source_lang, self.language)
        
        # Transform back
        return self.transform_from(xml_root)

    def write(self, content: Dict[str, Any], path: Union[str, Path], debug: bool = False) -> None:
        """Write UI strings to a file."""
        if isinstance(content, dict) and 'content' in content:
            content = content['content']
        self._save_json_file(content, str(path))

    def write_recursive(self, contents: List[Dict[str, Any]], directory: Union[str, Path], debug: bool = False) -> None:
        """Write multiple UI strings to files in a directory recursively."""
        output_dir = Path(directory)
        console.print(f"[green]Writing output files to {output_dir}[/green]")
        for content in contents:
            if isinstance(content, dict) and '_output_file' in content:
                output_file = output_dir / Path(content['_output_file']).name
            else:
                continue
            
            content_data = content.get('content', content)
            self.write(content_data, output_file, debug=debug)
