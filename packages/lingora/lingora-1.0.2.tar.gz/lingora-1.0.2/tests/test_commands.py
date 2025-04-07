"""Tests for CLI commands."""
import pytest
from typer.testing import CliRunner
from pathlib import Path
from lingora.commands.transliterate import app

runner = CliRunner()

def test_latex_command_single_file(tmp_path):
    """Test LaTeX transliteration command with a single file."""
    # Create a test LaTeX file
    input_file = tmp_path / "test.sr.tex"
    input_file.write_text(r"""
Ovo je test na \textbf{srpskom jeziku}.

$\int_0^1 x^2 dx$

% This is a comment

\begin{displayquote}
  Srpski je \underline{najlepši} jezik.
\end{displayquote}
""")

    expected_output = r"""
Ово је тест на \textbf{српском језику}.

$\int_0^1 x^2 dx$

% This is a comment

\begin{displayquote}
  Српски је \underline{најлепши} језик.
\end{displayquote}
"""

    # Run the command
    output_file = tmp_path / "test.sr-Cyrl.tex"
    result = runner.invoke(app, [
        "latex",
        "transliterate",
        str(input_file),
        str(output_file),
        "--language", "sr"
    ])
    
    assert result.exit_code == 0
    assert output_file.exists()
    assert output_file.read_text() == expected_output
    assert "Successfully wrote to" in result.stdout

def test_latex_command_recursive(tmp_path):
    """Test LaTeX transliteration command in recursive mode."""
    # Create test directory structure
    (tmp_path / "dir1").mkdir()
    (tmp_path / "dir2").mkdir()
    
    # Create test files
    files = [
        tmp_path / "test1.sr.tex",
        tmp_path / "dir1" / "test2.sr.tex",
        tmp_path / "dir2" / "test3.sr.tex"
    ]
    
    for file in files:
        file.write_text(r"""
\documentclass{article}
\begin{document}
Ovo je test na srpskom jeziku.
\end{document}
""")
    
    # Run the command in recursive mode
    result = runner.invoke(app, [
        "latex",
        str(tmp_path),
        "--language", "sr",
        "--recursive",
        "--test"  # Use test mode to avoid actual transliteration
    ])
    
    assert result.exit_code == 0
    
    # Check that output files were created
    for file in files:
        output_file = file.parent / f"{file.stem.rsplit('.', 1)[0]}.sr-Cyrl.tex"
        assert output_file.exists()
        assert str(output_file) in result.stdout

def test_latex_command_errors():
    """Test error handling in LaTeX command."""
    runner = CliRunner()
    
    # Test non-existent input file
    result = runner.invoke(app, [
        "latex",
        "nonexistent.tex",
        "output.tex",
        "--language", "sr"
    ])
    assert result.exit_code == 1
    assert "Error" in result.stdout
    
    # Test missing output file for single file mode
    result = runner.invoke(app, [
        "latex",
        __file__,  # Use this test file as input
        "--language", "sr"
    ])
    assert result.exit_code == 1
    assert "Error: output file is required" in result.stdout
