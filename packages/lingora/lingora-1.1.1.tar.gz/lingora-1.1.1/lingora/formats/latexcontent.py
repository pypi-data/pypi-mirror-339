"""LaTeX content handler with transliteration support.

Based on code by Jan Šnajder (Sep 2021), which was based on "LaTeX to txt conversion" by Arnaud Bodin:
https://github.com/arnbod/latex-to-text
"""
import re
import os
from pathlib import Path
from typing import Any, Dict, List, Tuple
import cyrtranslit
from .base import FormatHandler

# Constants for LaTeX parsing
LIST_ENV_DISCARD = [
    'equation', 'equation*', 'align', 'align*', 'alignat', 'alignat*',
    'lstlisting', 'eqnarray', 'comment'
]

LIST_CMD_ARG_DISCARD = [
    'usepackage', 'documentclass', 'begin', 'end', 'includegraphics',
    'label', 'ref', 'cite', 'citep', 'citet', 'vspace', 'hspace',
    'vspace*', 'hspace*', 'bibliography', 'url', 'href',
    'includesvg', 'input',  # Added by i-engineer
    'gls', 'GLS', 'Gls', 'acrshort', 'acrlong',  # For Glossary
]

LIST_COMPLEX_ENV_ARG_DISCARD = ['figure']

class LaTeXContent:
    """Handler for LaTeX content with transliteration support."""
    
    def __init__(self):
        self.tag = '@'
        self.count = 0
        self.dictionary = {}

    def _func_repl(self, m):
        """Replacement function for regex substitutions."""
        self.dictionary[self.count] = m.group(0)
        tag_str = self.tag + str(self.count) + self.tag
        self.count += 1
        return tag_str

    def _alt_repl(self, text):
        """Alternative replacement function."""
        self.dictionary[self.count] = text
        tag_str = self.tag + str(self.count) + self.tag
        self.count += 1
        return tag_str

    def _komplex(self, text, merkmal, amfang, ende, funktion):
        """Complex pattern matching and replacement."""
        fahne = False
        fahne_ende = False
        num_amfang = 0
        num_ende = 0
        merkmal_num = 0
        i = 0
        w = 0
        while w < len(text):
            i = w
            while i < len(text):
                char = text[i]
                if not fahne and char == merkmal[0]:
                    if len(merkmal) > 1:
                        fahne = all(text[i+j-1] == m_char for j, m_char in enumerate(merkmal))
                        if fahne:
                            num_amfang = i
                            i = i + len(merkmal) - 2
                    else:
                        num_amfang = i
                        fahne = True
                if fahne:
                    if char == amfang:
                        merkmal_num += 1
                    if char == ende:
                        if merkmal_num == 0:
                            num_ende = i + 1
                            fahne_ende = True
                            break
                        else:
                            merkmal_num -= 1
                i += 1
            if fahne and fahne_ende:
                neue_string = self._alt_repl(text[num_amfang:num_ende])
                text = text[:num_amfang] + neue_string + text[num_ende:]
                w = num_amfang
                fahne = False
                fahne_ende = False
                num_amfang = 0
                num_ende = 0
                merkmal_num = 0
            else:
                w = w + i
            w += 1
        return text

    def tex_to_txt(self, input_tex: str) -> Tuple[str, int]:
        """Convert LaTeX to plain text, preserving special commands."""
        self.count = 0
        self.dictionary.clear()
        text_new = input_tex

        # Step 1: Replace \begin{env} and \end{env} and contents
        for env in LIST_ENV_DISCARD:
            str_env = (r'\\begin\{' + re.escape(env) + r'\}(.+?)\\end\{' + re.escape(env) + r'\}')
            text_new = re.sub(str_env, self._func_repl, text_new, flags=re.MULTILINE|re.DOTALL)

        # Step 2: Replace \\ and \\[..]
        text_new = re.sub(r'\\\\(\[(.+?)\])?', self._func_repl, text_new, flags=re.MULTILINE|re.DOTALL)

        # Step 3: Replace math environments
        text_new = re.sub(r'\$\$(.+?)\$\$', self._func_repl, text_new, flags=re.MULTILINE|re.DOTALL)  # $$ ... $$
        text_new = re.sub(r'\\\[(.+?)\\\]', self._func_repl, text_new, flags=re.MULTILINE|re.DOTALL)  # \[ ... \]
        text_new = re.sub(r'\$(.+?)\$', self._func_repl, text_new, flags=re.MULTILINE|re.DOTALL)      # $ ... $
        text_new = re.sub(r'\\\((.+?)\\\)', self._func_repl, text_new, flags=re.MULTILINE|re.DOTALL)  # \( ... \)

        # Special handling for \ce{} chemistry
        text_new = self._komplex(text_new, r'\\ce{', r'{', r'}', self._func_repl)

        # Step 4: Handle complex environments
        for cmd in LIST_COMPLEX_ENV_ARG_DISCARD:
            str_env = r'\\begin\{' + re.escape(cmd) + r'\}\[(.*?)\]'
            text_new = re.sub(str_env, self._func_repl, text_new, flags=re.MULTILINE|re.DOTALL)
            text_new = re.sub(r'\\end\{(.+?)\}', self._func_repl, text_new, flags=re.MULTILINE|re.DOTALL)

        # Handle general begin/end environments
        text_new = re.sub(r'\\begin\{(.+?)\}', self._func_repl, text_new, flags=re.MULTILINE|re.DOTALL)
        text_new = re.sub(r'\\end\{(.+?)\}', self._func_repl, text_new, flags=re.MULTILINE|re.DOTALL)

        # Step 5: Replace LaTeX commands with arguments
        for cmd in LIST_CMD_ARG_DISCARD:
            str_env = r'\\' + re.escape(cmd) + r'\{(.+?)\}'  # Without opt arg
            text_new = re.sub(str_env, self._func_repl, text_new, flags=re.MULTILINE|re.DOTALL)
            str_env = r'\\' + re.escape(cmd) + r'\[(.*?)\]\{(.+?)\}'  # With opt arg
            text_new = re.sub(str_env, self._func_repl, text_new, flags=re.MULTILINE|re.DOTALL)

        # Step 6: Replace remaining LaTeX commands
        text_new = re.sub(r'\\[a-zA-Z]+\*?', self._func_repl, text_new, flags=re.MULTILINE|re.DOTALL)

        # Step 7: Replace non-empty line comments
        text_new = re.sub(r'[^\\](%.+?)$', self._func_repl, text_new, flags=re.MULTILINE)

        return text_new, len(self.dictionary)

    def txt_to_tex(self, input_txt: str, trim_whitespaces: bool = True) -> str:
        """Convert plain text back to LaTeX using stored replacements."""
        text_new = input_txt
        text_old = ""
        while text_new != text_old:
            text_old = text_new
            for i, val in self.dictionary.items():
                val = val.replace('\\', '\\\\')
                if trim_whitespaces:
                    # Handle GCS Translation API's whitespace insertion
                    tag_str1 = self.tag + ' ?' + str(i) + ' ?' + self.tag + ' {'
                    text_new = re.sub(tag_str1, val + '{', text_new, flags=re.MULTILINE|re.DOTALL)
                    tag_str2 = self.tag + ' ?' + str(i) + ' ?' + self.tag
                    text_new = re.sub(tag_str2, val, text_new, flags=re.MULTILINE|re.DOTALL)
                else:
                    tag_str = self.tag + str(i) + self.tag
                    text_new = re.sub(tag_str, val, text_new, flags=re.MULTILINE|re.DOTALL)
        return text_new

    @staticmethod
    def chunk_text(text: str, chunk_size: int) -> List[str]:
        """Split text into chunks while preserving paragraph boundaries."""
        chunks = []
        chunk = ""
        paragraphs = text.split("\n\n")
        for i, p in enumerate(paragraphs):
            if i < len(paragraphs) - 1:
                p += "\n\n"
            if len(p) > chunk_size:
                raise ValueError(
                    f"Cannot chunk input because paragraph {i+1} has "
                    f"{len(p)} codepoints, which is longer than "
                    f"chunk size of {chunk_size}"
                )
            l = len(chunk) + len(p)
            if l <= chunk_size:
                chunk += p
            else:
                chunks.append(chunk)
                chunk = p
        chunks.append(chunk)
        return chunks

    @staticmethod
    def find_tex_files(directory: str, language: str) -> List[Path]:
        """Find all .tex files in directory recursively."""
        tex_files = []
        for root, _, files in os.walk(directory):
            for file in files:
                if file.endswith(f'.{language}.tex'):
                    tex_files.append(Path(root) / file)
        return tex_files

class LaTeXHandler(FormatHandler):
    """Handler for LaTeX files with transliteration support."""
    
    def __init__(self):
        self.latex = LaTeXContent()
    
    def read(self, input_path: Path) -> str:
        """Read and preprocess LaTeX content."""
        with open(input_path, 'r', encoding='utf-8') as f:
            content = f.read()
        processed_content, _ = self.latex.tex_to_txt(content)
        return processed_content
    
    def write(self, content: str, output_path: Path) -> None:
        """Write processed content back to LaTeX format."""
        content = self.latex.txt_to_tex(content)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(content)
    
    def validate(self, content: Any) -> bool:
        """Validate that the content is a string and looks like LaTeX."""
        if not isinstance(content, str):
            return False
        # Basic validation - check for common LaTeX commands
        latex_indicators = [r'\documentclass', r'\begin{document}', r'\end{document}']
        return any(indicator in content for indicator in latex_indicators)