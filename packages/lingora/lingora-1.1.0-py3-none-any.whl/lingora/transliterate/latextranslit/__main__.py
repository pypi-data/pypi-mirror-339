"""
	basiert auf Kode von "Sep 2021, Jan Šnajder", die selbser auf "LaTeX to txt conversion" von Arnaud Bodin basierte: https://github.com/arnbod/latex-to-text
"""

import cyrtranslit
import argparse
import re
import os

# re = regex

def init_parser():
	parser = argparse.ArgumentParser(
		description="Transliterate ...")
	parser.add_argument("input_file",
		help="Text file to be translated, UTF-8 encoded")
	parser.add_argument("output_file", default=None, nargs='?',
		help="File to write the translation to")
	parser.add_argument("--language", "-l",
		help="BCP-47 source language code")
	# parser.add_argument("--output-language",
	# 	help="BCP-47 target language code")
	parser.add_argument('--chunk-size',
		default=5000, type=int,
		help="Maximum size of a text chunk in codepoints to be sent "
			 "to Cyrtranslit [module] (default=5000)")
	parser.add_argument("--latex", action='store_true',
		help="Input is LaTeX")
	parser.add_argument("--recursive", action='store_true',
		help="input-file will be treated as a directory and searched recursively within it")
	parser.add_argument("--test", action='store_true',
		help="Don't send to Cyrtranslit [module]")
	parser.add_argument("--save-input-output", action='store_true',
		help="Save translation input and output texts into files")
	return parser

def translate_text(input_text, language):
	"""Translating Text."""

	# client = cyrtranslit.to_cyrillic()
	return cyrtranslit.to_cyrillic(input_text, language)

list_env_discard = [
		'equation', 'equation*', 'align', 'align*', 'alignat', 'alignat*',
		'lstlisting', 'eqnarray', 'comment'
		]
list_cmd_arg_discard = [
	'usepackage', 'documentclass', 'begin', 'end', 'includegraphics',
	'label', 'ref', 'cite', 'citep', 'citet', 'vspace', 'hspace',
	'vspace*', 'hspace*', 'bibliography', 'url', 'href',
	# added by i-engineer
	'includesvg', 'input',
	# für Glossary
	'gls', 'GLS', 'Gls', 'acrshort', 'acrlong',
]
list_complex_env_arg_discard = [
	'figure',
]

tag = '@'
count = 0
dictionary = {}

def func_repl(m):
	global count
	dictionary[count] = m.group(0)
	tag_str = tag+str(count)+tag
	count += 1
	return tag_str

def alt_repl(text):
	global count
	dictionary[count] = text
	tag_str = tag+str(count)+tag
	count += 1
	return tag_str

def komplex(text, merkmal, amfang, ende, funktion):
	fahne = False
	fahne_ende = False
	num_amfang = 0
	num_ende = 0
	merkmal_num = 0
	i = 0
	w = 0
	expri = False
	while ( ( w < len(text) ) ):
		i = w
		while ( i < len(text) ):
			char = text[i]
			print(f"char[{i}]={char}")
			if ( (fahne == False) and (char == merkmal[0]) ):
				print("gefunden")
				if len(merkmal) > 1:
					for j, m_char in enumerate(merkmal):
						print(f"char[{j}]={m_char}")
						if text[i+j-1] == merkmal[j]:
							print("gefunden 2")
							fahne = True
						else:
							fahne = False
					if fahne:
						num_amfang = i
						i = i+len(merkmal)-2
						print("i wird merhfacht")
				else:
					num_amfang = i
					fahne = True
			if fahne == True:
				if char == amfang:
					print(f"andere gefunden um {i}")
					merkmal_num = merkmal_num + 1
				if char == ende:
					print("ende gefunden")
					if merkmal_num == 0:
						print("ende gemacht")
						num_ende = i+1
						fahne_ende = True
						break
					else:
						merkmal_num = merkmal_num - 1
			i = i + 1
		if ( fahne and fahne_ende):
			print(f"found pattern matching requirement from {num_amfang} to {num_ende}: {text[num_amfang:num_ende]}")
			neue_string = alt_repl(text[num_amfang:num_ende])
			print(f"to replace with {neue_string}")
			text = text[:(num_amfang)] + neue_string + text[(num_ende):]
			print(f"new text: {text}")
			w = num_amfang
			fahne = False
			fahne_ende = False
			num_amfang = 0
			num_ende = 0
			merkmal_num = 0
		else:
			w = w + i
		w = w + 1
	neue_text = text
	return neue_text

def chunk_text(text, chunk_size):
	chunks = []
	chunk = ""
	paragraphs = text.split("\n\n")
	for i, p in enumerate(paragraphs):
		if i < len(paragraphs) - 1:
			p += "\n\n"
		if len(p) > chunk_size:
			raise Exception(
					f"Cannot chunk input because paragraph {i+1} has "
					f"{len(p)} codepoints, which is longer than "
					f"chunk size of {chunk_size}")
		l = len(chunk) + len(p)
		if l <= chunk_size:
			chunk += p
		else:
			chunks.append(chunk)
			chunk = p
	chunks.append(chunk)
	return chunks

def tex_to_txt(input_tex):
	text_new = input_tex

	# Step 1: Replace \begin{env} and \end{env} and its contents
	for env in list_env_discard:
		str_env = (r'\\begin\{' + re.escape(env)
				   + r'\}(.+?)\\end\{' + re.escape(env) + r'\}')
		text_new = re.sub(
				str_env, func_repl, text_new, flags=re.MULTILINE|re.DOTALL)

	# Step 2: Replacement of \\ and \\[..]
	text_new = re.sub(r'\\\\(\[(.+?)\])?', func_repl, text_new,
					  flags=re.MULTILINE|re.DOTALL)

	# Step 3: Replacement of maths ###
	# $$ ... $$
	text_new = re.sub(r'\$\$(.+?)\$\$', func_repl, text_new,
					  flags=re.MULTILINE|re.DOTALL)
	# \[ ... \]
	text_new = re.sub(r'\\\[(.+?)\\\]', func_repl, text_new,
					  flags=re.MULTILINE|re.DOTALL)
	# $ ... $
	text_new = re.sub(r'\$(.+?)\$', func_repl, text_new,
					  flags=re.MULTILINE|re.DOTALL)
	# \( ... \)
	text_new = re.sub(r'\\\((.+?)\\\)', func_repl, text_new,
					  flags=re.MULTILINE|re.DOTALL)

	# BESONDERS für \ce{} chemistry
	text_new = komplex(text_new, r'\\ce{',r'{',r'}',func_repl)

	for cmd in list_complex_env_arg_discard:
		# Step 4.1: Replace complex begin/end commands, but not the conent
		str_env = r'\\begin\{' + re.escape(cmd) + r'\}\[(.*?)\]'
		text_new = re.sub(str_env, func_repl, text_new,
					  flags=re.MULTILINE|re.DOTALL)
		text_new = re.sub(r'\\end\{(.+?)\}', func_repl, text_new,
					  flags=re.MULTILINE|re.DOTALL)
	# Step 4: Replace begin/end environment commands, but not the content
	text_new = re.sub(r'\\begin\{(.+?)\}', func_repl, text_new,
					  flags=re.MULTILINE|re.DOTALL)
	text_new = re.sub(r'\\end\{(.+?)\}', func_repl, text_new,
					  flags=re.MULTILINE|re.DOTALL)


	# Step 5: Replace LaTeX commands alongside their argument
	for cmd in list_cmd_arg_discard:
		# Without opt arg, ex. \cmd{arg}
		str_env = r'\\' + re.escape(cmd) + r'\{(.+?)\}'
		text_new = re.sub(str_env, func_repl, text_new,
						  flags=re.MULTILINE|re.DOTALL)
		# With opt arg, ex. \cmd[opt]{arg}
		str_env = r'\\' + re.escape(cmd) + r'\[(.*?)\]\{(.+?)\}'
		text_new = re.sub(str_env, func_repl, text_new,
						  flags=re.MULTILINE|re.DOTALL)

	# Step 6: Replace remaining LaTeX commands, but not their arguments
	text_new = re.sub(r'\\[a-zA-Z]+\*?', func_repl, text_new,
					  flags=re.MULTILINE|re.DOTALL)

	# Step 7: Replace non-empty line comments
	text_new = re.sub(r'[^\\](%.+?)$', func_repl, text_new,
					  flags=re.MULTILINE)

	return text_new, len(dictionary)

def txt_to_tex(input_txt, trim_whitespaces=True):
	""" Converts a TXT with code labels back to LaTeX, using the dictionary
		of code replacements.
	"""
	text_new = input_txt
	text_old = ""
	while text_new != text_old:
		text_old = text_new
		for i, val in dictionary.items():
			val = val.replace('\\','\\\\')
			if trim_whitespaces:
				# NB: GCS Translation API inserts 3 whitespaces around codes
				# (the third one sometimes omitted, but if followed by "{",
				# it should be trimmed)
				tag_str1 = tag+' ?'+str(i)+' ?'+tag+' {'
				text_new = re.sub(tag_str1, val+'{', text_new,
								  flags=re.MULTILINE|re.DOTALL)
				tag_str2 = tag+' ?'+str(i)+' ?'+tag
				text_new = re.sub(tag_str2, val, text_new,
								  flags=re.MULTILINE|re.DOTALL)
			else:
				tag_str = tag+str(i)+tag
				text_new = re.sub(tag_str, val, text_new,
								  flags=re.MULTILINE|re.DOTALL)
	return text_new

def find_files_with_extension(directory, endung):
	selected_files = []
	for root, dirs, files in os.walk(directory):
		for file in files:
			print(f"looking at path={file}")
			if file.endswith(endung):
				print(f"file at path='{file}' matches the extension pattern;")
				selected_files.append(os.path.join(root, file))
				print("added to the list of files for conversion.")
	return selected_files

def transform(args, input_string):
	if args.latex:
		print("LaTeX file indicated as input. Converting to txt.")
		input_text, rep = tex_to_txt(input_string)
		print(f"{rep} replacements made.")
	else:
		input_text = input_string
	if args.save_input_output:
		with open(args.input_file + ".input", "w", encoding='utf-8') as fi:
			fi.write(input_text)
	file_length = len(input_text)
	print(f'The file has {file_length} codepoints.')
	if file_length > args.chunk_size:
		print(f"Input is above {args.chunk_size} codepoints. Batch processing "
			   "is recommended, but will proceed with a synchronous call on "
			   "chunked input.")
	translated_text = ""
	chunks = chunk_text(input_text, args.chunk_size)
	for i, input_chunk in enumerate(chunks):
		print(f"Text chunk {i+1}/{len(chunks)} of "
			  f"{len(input_chunk)} codepoints")
		if args.test:
			translated_chunk = input_chunk
		else:
			print(f"Sending to Cyrtranslit [module] for transliteration "
				  f"from {args.language}")
			translated_chunk = translate_text(
					input_chunk,
					args.language)
		translated_text += translated_chunk
	# if args.save_input_output:
	# 	if args.output_file is None:
	# 		print(f"Error: providing an output-file as the last argument is required.")
	# 		paser.print_help()
	# 		exit(1)
	# 	with open(args.output_file + ".output", "w", encoding='utf-8') as fo:
	# 		fo.write(translated_text)
	if args.latex:
		print("Converting txt back to LaTeX.")
		translated_text = txt_to_tex(translated_text,
									 trim_whitespaces=not(args.test))
	return translated_text

def main():
	paser = init_parser()
	args = paser.parse_args()
	input_string = ""
	input_list = []
	if args.recursive:
		print(f"recursive option activated for path='{args.input_file}'")
		endung = f'.{args.language}.tex'
		print(f"searching for endings:'{endung}'")
		input_list = find_files_with_extension(args.input_file, endung)
	else:
		with open(args.input_file, 'r', encoding='utf-8') as file:
			print(f"Opening file {args.input_file}.")
			input_string = file.read()

	if (len(input_list) > 0):
		for file in input_list:
			with open(file, 'r', encoding='utf-8') as o_file:
				print(f"Opening file {file}.")
				input_string = o_file.read()
			translated_text = transform(args, input_string)
			base_name, _ = os.path.splitext(file)
			base_name, _ = os.path.splitext(base_name)
			neue_endung = f'.{args.language}-Cyrl.tex'
			new_path = base_name + neue_endung
			with open(new_path, 'w') as new_file:
				print(f"Writing to {new_path}")
				new_file.write(translated_text)
	else:
		translated_text = transform(args, input_string)
		if args.output_file is None:
			print(f"Error: providing an output-file as the last argument is required.")
			paser.print_help()
			exit(1)
		with open(args.output_file, 'w', encoding='utf-8') as file:
			print(f"Writting to {args.output_file}")
			file.write(translated_text)
if __name__ == '__main__':
	main()
