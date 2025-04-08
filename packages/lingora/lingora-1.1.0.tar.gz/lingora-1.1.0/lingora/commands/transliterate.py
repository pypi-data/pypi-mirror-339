"""Command module for text transliteration functionality."""
import os
from typing import Union
from pathlib import Path
import typer
from rich.console import Console
import cyrtranslit
from lingora.formats.latexcontent import LaTeXHandler
from ..formats.latex_text import LatexTextIntermediate

console = Console()

def process_text(input_text: str, language: str) -> str:
    """Translate text using cyrtranslit."""
    return cyrtranslit.to_cyrillic(input_text, language)

def transform_latex(content: str, language: str, chunk_size: int, test: bool = False) -> str:
    """Transform LaTeX content using the transliteration logic."""
    # First convert LaTeX to text, preserving LaTeX commands
    input_text = content
    file_length = len(input_text)
    console.print(f'The file has {file_length} codepoints.')
    
    if file_length > chunk_size:
        console.print(f"Input is above {chunk_size} codepoints. Processing in chunks...")
    
    translated_text = ""
    chunks = []
    # Split into chunks of maximum size
    for i in range(0, len(input_text), chunk_size):
        chunks.append(input_text[i:i + chunk_size])
    
    for i, input_chunk in enumerate(chunks, 1):
        console.print(f"Processing chunk {i}/{len(chunks)} of {len(input_chunk)} codepoints")
        if test:
            translated_chunk = input_chunk
        else:
            console.print(f"Transliterating from {language}")
            translated_chunk = translate_text(input_chunk, language)
        translated_text += translated_chunk
    
    return translated_text

def i18next():
    pass

def latex(
    input_path: str = typer.Argument(..., help="Text file to be translated, UTF-8 encoded"),
    output_path: str = typer.Argument(None, help="Optional output file path. If not provided, will generate automatically"),
    language: str = typer.Option(..., "--language", "-l", help="BCP-47 source language code"),
    # chunk_size: int = typer.Option(5000, help="Maximum size of a text chunk in codepoints"),
    # test: bool = typer.Option(False, help="Don't send to Cyrtranslit module"),
):
    """Transliterate LaTeX files between Latin and Cyrillic scripts."""
    handler = LatexTextIntermediate(process_text, language)
    input_path = Path(input_path)

    recursive = False

    if input_path.is_dir():
        recursive = True
    else:
        handler.read(input_path)
        handler.process()
        handler.write(output_path)



    # if recursive and input_path.is_dir():
    #     # Process directory recursively
    #     tex_files = handler.latex.find_tex_files(str(input_path), language)
    #     if not tex_files:
    #         console.print(f"[yellow]No .{language}.tex files found in {input_path}[/yellow]")
    #         raise typer.Exit(1)
        
    #     for tex_file in tex_files:
    #         console.print(f"Processing {tex_file}")
    #         # Generate output path
    #         base_name = tex_file.stem.rsplit('.', 1)[0]  # Remove language suffix
    #         output_path = tex_file.parent / f"{base_name}.{language}-Cyrl.tex"
            
    #         # Process file
    #         try:
    #             content = handler.read(tex_file)
    #             processed_content = transform_latex(content, language, chunk_size, test)
    #             handler.write(processed_content, output_path)
    #             console.print(f"[green]Successfully wrote to {output_path}[/green]")
    #         except Exception as e:
    #             console.print(f"[red]Error processing {tex_file}: {str(e)}[/red]")
    #             continue
    # else:
    #     # Process single file
    #     if not input_path.exists():
    #         console.print(f"[red]Input file {input_path} does not exist[/red]")
    #         raise typer.Exit(1)
        
    #     try:
    #         content = handler.read(input_path)
    #         processed_content = transform_latex(content, language, chunk_size, test)
            
    #         # Generate output path if not provided
    #         if output_file is None:
    #             base_name = input_path.stem
    #             output_path = input_path.parent / f"{base_name}.{language}-Cyrl.tex"
    #         else:
    #             output_path = Path(output_file)
            
    #         handler.write(processed_content, output_path)
    #         console.print(f"[green]Successfully wrote to {output_path}[/green]")
    #     except Exception as e:
    #         console.print(f"[red]Error: {str(e)}[/red]")
    #         raise typer.Exit(1)
