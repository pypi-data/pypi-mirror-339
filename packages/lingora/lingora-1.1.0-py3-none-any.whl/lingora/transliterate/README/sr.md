# Latex Transliteration

Prenošenje jedinstvenog fajla lateksa ili fascikle sa podfasciklama koje sadrže nekoliko fajlova lateksa u formatu. [kod-jezika]. Teks (na primer `ime.sr.tex` na `ime.sr-Cyrl.tex`) od latinskog skripte do ciriličnog skripta koristeći paket **cyrillic-transliteration**

## Instrukcije

### jedno fajl

```
python latextranslit --latex -l=sr <unesite-fajl> <izlazni-fajl>
```

### Više fajlova (fascikla)

```
python latextranslit --latex --recursive -l=sr <fascikla>
```

## Razvoj

Aktivirajte virtuelno okruženje za Python:

```
source ./bin/activate
```

Onda se program može obaviti normalno.

## Stanje

- Stepen razvoja: eksperimentalni
- podržani jezici: svi koji su vež ponuðeni od strane **cyrillic-transliteration** paket