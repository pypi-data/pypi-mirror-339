"""LaTeX text intermediate format implementation."""
import re
from rich.console import Console
from .intermediate import Intermediate
from typing import Union, Callable, List
from pathlib import Path

console = Console()

class LatexTextIntermediate(Intermediate):
    """Intermediate format for LaTeX text content."""
    
    def __init__(self, process_func: Callable[[str], str], language: str, recursive: bool = True):

        self.process_func = process_func
        self.language = language
        self.recursive = recursive

        self.input_string = ""
        self.input_list = []

        self.tag = '@'
        self.count = 0
        self.dictionary = {}
        
        # LaTeX environments to discard
        self.list_env_discard = [
            'equation', 'equation*', 'align', 'align*', 'alignat', 'alignat*',
            'lstlisting', 'eqnarray', 'comment'
        ]
        
        # LaTeX commands with arguments to discard
        self.list_cmd_arg_discard = [
            'usepackage', 'documentclass', 'begin', 'end', 'includegraphics',
            'label', 'ref', 'cite', 'citep', 'citet', 'vspace', 'hspace',
            'vspace*', 'hspace*', 'bibliography', 'url', 'href',
            'includesvg', 'input',
            'gls', 'GLS', 'Gls', 'acrshort', 'acrlong',
        ]
        
        # Complex environments that need special handling
        self.list_complex_env_arg_discard = ['figure']

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
        """Handle complex LaTeX structures."""
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

    def _tex_to_txt(self, input_tex):
        """Convert LaTeX to intermediate text format."""
        text_new = input_tex

        # Step 1: Replace \begin{env} and \end{env} and contents
        for env in self.list_env_discard:
            str_env = (r'\\begin\{' + re.escape(env) + r'\}(.+?)\\end\{' + re.escape(env) + r'\}')
            text_new = re.sub(str_env, self._func_repl, text_new, flags=re.MULTILINE|re.DOTALL)

        # Step 2: Replace \\ and \\[..]
        text_new = re.sub(r'\\\\(\[(.+?)\])?', self._func_repl, text_new, flags=re.MULTILINE|re.DOTALL)

        # Step 3: Replace math environments
        text_new = re.sub(r'\$\$(.+?)\$\$', self._func_repl, text_new, flags=re.MULTILINE|re.DOTALL)  # $$ ... $$
        text_new = re.sub(r'\\\[(.+?)\\\]', self._func_repl, text_new, flags=re.MULTILINE|re.DOTALL)  # \[ ... \]
        text_new = re.sub(r'\$(.+?)\$', self._func_repl, text_new, flags=re.MULTILINE|re.DOTALL)      # $ ... $
        text_new = re.sub(r'\\\((.+?)\\\)', self._func_repl, text_new, flags=re.MULTILINE|re.DOTALL)  # \( ... \)

        # Handle chemistry equations
        text_new = self._komplex(text_new, r'\\ce{', '{', '}', self._func_repl)

        # Step 4: Handle complex environments
        for cmd in self.list_complex_env_arg_discard:
            str_env = r'\\begin\{' + re.escape(cmd) + r'\}\[(.*?)\]'
            text_new = re.sub(str_env, self._func_repl, text_new, flags=re.MULTILINE|re.DOTALL)
            text_new = re.sub(r'\\end\{(.+?)\}', self._func_repl, text_new, flags=re.MULTILINE|re.DOTALL)

        # Step 5: Replace remaining LaTeX commands
        text_new = re.sub(r'\\begin\{(.+?)\}', self._func_repl, text_new, flags=re.MULTILINE|re.DOTALL)
        text_new = re.sub(r'\\end\{(.+?)\}', self._func_repl, text_new, flags=re.MULTILINE|re.DOTALL)

        # Step 6: Handle other LaTeX commands
        for cmd in self.list_cmd_arg_discard:
            str_cmd1 = r'\\' + re.escape(cmd) + r'\{(.+?)\}'
            str_cmd2 = r'\\' + re.escape(cmd) + r'\[(.+?)\]\{(.+?)\}'
            text_new = re.sub(str_cmd1, self._func_repl, text_new, flags=re.MULTILINE|re.DOTALL)
            text_new = re.sub(str_cmd2, self._func_repl, text_new, flags=re.MULTILINE|re.DOTALL)
        
        # Step 7: Replace remaining LaTeX commands, but not their arguments
        text_new = re.sub(r'\\[a-zA-Z]+\*?', self._func_repl, text_new, flags=re.MULTILINE|re.DOTALL)
        
        # Step 8: Replace non-empty line comments
        text_new = re.sub(r'[^\\](%.+?)$', self._func_repl, text_new, flags=re.MULTILINE)

        return text_new

    def _txt_to_tex(self, input_txt):
        """Convert intermediate text format back to LaTeX."""
        text_new = input_txt
        for i in range(self.count - 1, -1, -1):
            tag_str = self.tag + str(i) + self.tag
            text_new = text_new.replace(tag_str, self.dictionary[i])
        return text_new
    
    def _find_files_with_extension(self, directory, endung):
        selected_files = []
        for root, dirs, files in os.walk(directory):
            for file in files:
                if file.endswith(endung):
                    selected_files.append(os.path.join(root, file))
        return selected_files

    def transform_to(self, content: str) -> str:
        """Transform LaTeX content to intermediate text format."""
        # Reset state
        self.count = 0
        self.dictionary = {}
        
        # Convert LaTeX to intermediate format
        return self._tex_to_txt(content)
    
    def transform_from(self, content: str) -> str:
        """Transform intermediate text format back to LaTeX."""
        return self._txt_to_tex(content)
    
    def read(self, path: Union[str, Path]) -> None:
        """Read LaTeX content from a file."""
        with open(path, 'r', encoding='utf-8') as file:
            console.print(f"Opening file {path}.")
            self.input_string = file.read()
        self.recursive = False
    
    def read_recursive(self, directory: Union[str, Path]) -> None:
        """Read LaTeX content from all matching files in a directory recursively."""
        console.print(f"recursive option activated for path='{directory}'")
        endung = f'.{self.language}.tex'
        self.input_list = self._find_files_with_extension(directory, endung)
    
    def process(self) -> None:
        """Process LaTeX content in chunks."""
        if self.recursive:
            pass
        else: 
            self.input_string = self.transform_to(self.input_string)
            self.input_string = self.process_func(self.input_string, self.language)
            self.input_string = self.transform_from(self.input_string)
    
    def write(self, output_path: Union[str, Path], debug: bool = False) -> None:
        """Write LaTeX content to a file."""
		# if args.output_file is None:
		# 	print(f"Error: providing an output-file as the last argument is required.")
		# 	paser.print_help()
		# 	exit(1)
        
        with open(output_path, 'w', encoding='utf-8') as file:
            console.print(f"Writting to {output_path}")
            file.write(self.input_string)
    
    def write_recursive(self, contents: List[str], directory: Union[str, Path], debug: bool = False) -> None:
        """Write multiple LaTeX files in a directory recursively."""
        # TODO: Implement recursive writing
        pass
