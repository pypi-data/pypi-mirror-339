# Latex Transliteration

- [readme srpski (latin)](./README/sr.md)
- [readme English](./README/en.md)

Buchstaben ein Latex-dokument von latainisch auf cyrillisch umwandeln.

Sowohl einzelne Dateien als auch eine Fach mit mehr Datein möglich.

## Status

- Entwicklungsgrad: experimentell
- unterstützte Sprachen: all die schon durch **cyrillic-transliteration** Pakette angeboten werden

## Gebrauchanleitung

### einzelne Datei

```
python latextranslit --latex -l=<Sprachkod> <Eingabedatei> <Ausgabedatei>
```

für `<Sprachkod>` siehen Sie bitte  **cyrillic-transliteration** Pakette

### mehrere Dateien (Fach)

```
python latextranslit --latex --recursive -l=<Sprachkod> <Eingabefach>
```

## Entwicklung

virtuelle Umgebung für Python aktivieren:

```
source ./bin/activate
```

danach kann das Program normal durchgeführt werden.

## Herstellung

- benutzt: https://github.com/opendatakosovo/cyrillic-transliteration/tree/master
- basiert auf: https://github.com/jsnajder/latex-google-translate