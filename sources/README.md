# Source editions

The Greek editions this project reads from. **They are not committed** — everything in this
directory except this file is excluded by [`../.gitignore`](../.gitignore). See
[`../NOTICE.md`](../NOTICE.md) for why.

Fetch them here before running `python build/words.py` or `python build/validate.py`.
Without the SBLGNT the `greek` check cannot run: it reports `SKIP` and the summary says so
explicitly rather than passing quietly. Every other check works without any of this.

## New Testament — SBL Greek New Testament

CC BY 4.0. Free to redistribute with attribution.

```bash
git clone --depth 1 https://github.com/LogosBible/SBLGNT.git sources/sblgnt
```

`validate.py` reads `sources/sblgnt/text/<Book>.txt`, one verse per line as
`John 1:1<TAB><greek>`.

## New Testament morphology — MorphGNT

CC BY-SA 3.0 for the parsing and lemmatization, which may be adapted under CC BY-SA 4.0.
Only the file for each book on the page is needed — for John, about 1 MB:

```bash
curl -sL --create-dirs -o sources/morphgnt/64-Jn-morphgnt.txt https://raw.githubusercontent.com/morphgnt/sblgnt/master/64-Jn-morphgnt.txt
```

`build/words.py` reads it for the word-by-word layer. Until it is present, John's Greek lines
render without that layer.

## Lexicon — Middle Liddell, Perseus XML

Liddell and Scott's *Intermediate Greek-English Lexicon* (1889) as the Perseus Digital
Library encoded it — CC BY-SA 3.0 US, adaptable under CC BY-SA 4.0. `build/words.py` reads
each word's senses from it, and the headword rule takes each headword from it.

```bash
curl -sL --create-dirs -o sources/middle-liddell/Perseus_text_1999.04.0058.xml https://raw.githubusercontent.com/blinskey/middle-liddell/master/Perseus_text_1999.04.0058.xml
```

## The printed Rahlfs — where the Old Testament Greek comes from

The Greek in `data/` is transcribed by hand from Rahlfs's printed edition, not copied from
anything in this directory. The 1935 first printing is lending-only at the Internet Archive;
the 1950 printing, a reprint of the same text, is open:

<https://archive.org/details/septuaginta-id-est-vetus-testamentum-graece-iuxta-lxx-interpretes-edidit-by-alfred-rahlfs-1935>

The scan is of two-page spreads, and the archive's own page-number map is wrong, so go by
leaf: in volume I, leaf 26 is the title page and **leaf 27's right-hand page is Genesis,
p. 1**. A single leaf is at `https://archive.org/download/<item>/page/n27.jpg`. Cite the
printed page in each verse's `print` field. Don't commit the images.

## What these can and cannot verify

| | word forms | accents | punctuation | capitalisation |
| --- | --- | --- | --- | --- |
| SBLGNT | yes | yes | yes | yes |
| Rahlfs, printed (the scan above) | yes | yes | yes | yes |

The New Testament is checked mechanically, character for character. The Old Testament has no
digital edition behind it at all: its Greek — words, accents and pointing alike — comes from
the printed page each verse cites in `print`, and its morphology is the project's own
analysis.

`validate.py` can cross-check those two against a local Rahlfs morphological module if the
environment variable `LXX_RAHLFS_DIR` points at one. Nothing in the repository needs it, no
such module is distributed with it, and without it both checks report `SKIP`.
