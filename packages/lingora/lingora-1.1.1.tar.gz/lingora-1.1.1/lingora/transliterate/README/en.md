# Latex Transliteration

Transliterating a singular latex file or a directory with subdirectories containing several latex files in the format ".[lanuage-code].tex" (for example "<file-name>.sr.tex") from latin script to cyrillic script using **cyrillic-transliteration** package

## Status

- degree of completion: experimental version
- supporated translitation: all of the languages provided by **cyrillic-transliteration** package.

## Usage

### Singular file

```
python latextranslit --latex -l=sr <input-file> <output-file>
```

### Recursive (for directory)

```
python latextranslit --latex --recursive -l=sr <input-directory>
```

## Origin

- uses: https://github.com/opendatakosovo/cyrillic-transliteration/tree/master
- based on: https://github.com/jsnajder/latex-google-translate
