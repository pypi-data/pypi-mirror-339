"""Tests for format handlers."""
import pytest
from pathlib import Path
from lingora.formats.latexcontent import LaTeXHandler, LaTeXContent
from lingora.formats.i18next import I18NextHandler

def test_latex_handler_validate():
    """Test LaTeX content validation."""
    handler = LaTeXHandler()
    
    # Valid LaTeX content
    valid_content = r"""
\documentclass{article}
\begin{document}
Hello World
\end{document}
"""
    assert handler.validate(valid_content) is True
    
    # Invalid content types
    assert handler.validate(None) is False
    assert handler.validate(123) is False
    assert handler.validate([]) is False
    
    # Non-LaTeX content
    assert handler.validate("Just plain text") is False

def test_latex_content_tex_to_txt():
    """Test LaTeX to text conversion."""
    latex = LaTeXContent()
    
    # Test basic text
    input_tex = r"Simple text"
    output, count = latex.tex_to_txt(input_tex)
    assert output == "Simple text"
    assert count == 0
    
    # Test math environment
    input_tex = r"Text with $x^2$ math"
    output, count = latex.tex_to_txt(input_tex)
    assert "@0@" in output
    assert count == 1
    assert latex.dictionary[0] == "$x^2$"
    
    # Test commands
    input_tex = r"\textbf{bold} text"
    output, count = latex.tex_to_txt(input_tex)
    assert "@0@" in output
    assert count == 1
    assert "\\textbf{bold}" in latex.dictionary[0]

def test_latex_content_txt_to_tex():
    """Test text to LaTeX conversion."""
    latex = LaTeXContent()
    
    # First convert to text to populate dictionary
    input_tex = r"Text with $x^2$ and \textbf{bold}"
    text, _ = latex.tex_to_txt(input_tex)
    
    # Then convert back to LaTeX
    output = latex.txt_to_tex(text)
    assert output == input_tex

def test_i18next_handler():
    """Test i18next format handler."""
    handler = I18NextHandler()
    
    # Test validation
    assert handler.validate({"key": "value"}) is True
    assert handler.validate("not a dict") is False
    assert handler.validate(None) is False
    
    # Test read/write (using tmp_path fixture)
    test_content = {
        "greeting": "Hello",
        "nested": {
            "key": "Value"
        }
    }
    
    tmp_file = Path("/tmp/test.json")
    handler.write(test_content, tmp_file)
    
    read_content = handler.read(tmp_file)
    assert read_content == test_content
    
    # Cleanup
    tmp_file.unlink()

def test_latex_content_chunk_text():
    """Test text chunking functionality."""
    latex = LaTeXContent()
    
    # Test simple chunking
    text = "First paragraph.\n\nSecond paragraph.\n\nThird paragraph."
    chunks = latex.chunk_text(text, chunk_size=20)
    assert len(chunks) > 1
    assert all(len(chunk) <= 20 for chunk in chunks)
    
    # Test chunk size too small
    long_text = "A" * 100
    with pytest.raises(ValueError):
        latex.chunk_text(long_text, chunk_size=50)
