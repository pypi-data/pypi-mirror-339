"""CLI interface for Lingora."""
import os
import xml.etree.ElementTree as ET
from typing import Dict, Any, Optional
import typer
from rich.console import Console
from rich.progress import Progress
from pathlib import Path
import shutil
import subprocess
import sys
from lingora.commands import transliterate
from lingora.plugins.base import TranslationPlugin
from lingora.plugins.registry import PluginRegistry
from lingora.formats.xml_uistring import XmlUiStringIntermediate
from sanic import Sanic, response
from sanic.response import json as sanic_json
import webbrowser
from functools import partial
import lingora.formats.i18next

# Import functions from i18next.py
from lingora.formats.i18next import (
    find_json_files,
    generate_xml,
    translate_xml,
    reconstruct_json
)

app = typer.Typer()
console = Console()

# Create command groups
latex_app = typer.Typer()
ui_app = typer.Typer()
app.add_typer(latex_app, name="latex", help="LaTeX file processing commands")
app.add_typer(ui_app, name="ui", help="UI string processing commands")

# Add the transliterate command directly to latex group
latex_app.command(name="transliterate")(transliterate.latex)

@ui_app.command()
def translate(
    source_lang: str = typer.Argument(..., help="Source language code (e.g., 'en')"),
    target_lang: str = typer.Argument(..., help="Target language code (e.g., 'es')"),
    input_dir: str = typer.Option(".", help="Input directory containing JSON files"),
    plugin_name: str = typer.Option("openai", help="Name of the translation plugin to use"),
    debug: bool = typer.Option(False, help="Enable debug output")
):
    """
    Translate all JSON files in a directory from source language to target language.
    """
    # Initialize
    base_dir = Path(input_dir)
    output_dir = Path("output") / target_lang
    tmp_dir = Path("tmp")
    json_files = find_json_files(input_dir)

    if not json_files:
        console.print("[red]No JSON files found in the specified directory[/red]")
        raise typer.Exit(1)

    # Get the translation plugin
    plugin = PluginRegistry.get_plugin(plugin_name)
    if not plugin:
        console.print(f"[red]Error: Plugin '{plugin_name}' not found[/red]")
        raise typer.Exit(1)

    with Progress() as progress:
        # Step 1: Generate XML and ID mappings
        task = progress.add_task("[cyan]Generating XML...", total=1)
        xml_path, _ = generate_xml(json_files, base_dir)
        progress.update(task, completed=1)

        # Step 2: Translate XML
        task = progress.add_task("[cyan]Translating...", total=1)
        translated_xml = translate_xml(xml_path, source_lang, target_lang, plugin)
        progress.update(task, completed=1)

        # Step 3: Reconstruct JSON files
        task = progress.add_task("[cyan]Reconstructing JSON files...", total=1)
        reconstruct_json(translated_xml, tmp_dir, output_dir)
        progress.update(task, completed=1)

    # Clean up temporary files unless in debug mode
    if not debug:
        shutil.rmtree(tmp_dir)
        console.print("[cyan]Cleaned up temporary files[/cyan]")
    else:
        console.print(f"[yellow]Debug mode: Temporary files preserved in {tmp_dir}[/yellow]")

    console.print(f"[green]Translation completed! Output saved in: {output_dir}[/green]")


@app.command()
def list_plugins():
    """List all available translation plugins."""
    plugins = PluginRegistry.get_available_plugins()
    if not plugins:
        console.print("[yellow]No plugins found[/yellow]")
        return

    console.print("\n[bold]Available Translation Plugins:[/bold]")
    for plugin_name in plugins:
        console.print(f"- {plugin_name}")

@app.command()
def reviewer(
    input_dir: str = typer.Argument(..., help="Input directory containing source language files"),
    output_dir: str = typer.Argument(..., help="Directory containing target language files"),
    app_name: str = typer.Option("translation_reviewer", help="Name for the Sanic application"),
    port: int = typer.Option(8000, help="Port to run the server on")
):
    """
    Launch a web-based reviewer interface for comparing and editing translations.
    """
    input_path = Path(input_dir).resolve()
    output_path = Path(output_dir).resolve()

    # Create reviewer directory if it doesn't exist
    reviewer_dir = Path("reviewer")
    reviewer_dir.mkdir(exist_ok=True)

    # Copy static files from templates
    template_dir = Path("reviewer")
    # for template_file in ["reviewer.html", "reviewer.js", "reviewer.css"]:
    #    shutil.copy(template_dir / template_file, reviewer_dir / template_file)
    # for template_file in ["reviewer.js", "reviewer.css"]:
    #    shutil.copy(template_dir / template_file, reviewer_dir / template_file)

    # Initialize Sanic app using AppLoader
    from sanic.worker.loader import AppLoader
    from sanic import Sanic
    from lingora.sanic_app import create_app

    # Create app loader with configuration
    config = {
        "input_path": input_path,
        "output_path": output_path,
        "reviewer_dir": reviewer_dir
    }

    loader = AppLoader(
        factory=partial(create_app, app_name, config),
        #debug=True
    )

    console.print("[green]Starting translation reviewer server...[/green]")
    try:
        app = loader.load()
        app.prepare(port=port, dev=True)

        # Open browser after server starts
        app.add_task(partial(webbrowser.open, f'http://localhost:{port}'))

        # Start the server
        Sanic.serve(primary=app, app_loader=loader)
    except KeyboardInterrupt:
        console.print("\n[yellow]Shutting down reviewer server...[/yellow]")
    except Exception as e:
        console.print(f"[red]Error starting server: {e}[/red]")
        raise typer.Exit(1)

if __name__ == "__main__":
    app()
