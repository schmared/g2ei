# Source editions

The Greek editions this project reads from. **They are not committed** — everything in this
directory except this file is excluded by [`../.gitignore`](../.gitignore). See
[`../NOTICE.md`](../NOTICE.md) for why.

Fetch them here before running `python build/validate.py`. Without them the `greek` check
cannot run; it reports `SKIP` and the summary says so explicitly rather than passing
quietly. The other four checks work without any of this.

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

## Old Testament — the CCAT data, for checking only

**Used only by `validate.py`**, to check the transcription's word forms and the project's own
morphology. Nothing from it is copied into `data/`. It is CC BY-NC-SA 4.0, **and the upstream repository asks that you agree to send a CCAT user
declaration before downloading any of its data.** Read
<https://github.com/eliranwong/LXX-Rahlfs-1935> and the
[CCAT declaration](http://ccat.sas.upenn.edu/gopher/text/religion/biblical/lxxmorph/0-user-declaration.txt)
first, and do not download if you do not agree.

```bash
git clone --depth 1 https://github.com/eliranwong/LXX-Rahlfs-1935.git sources/LXX-Rahlfs-1935
```

`validate.py` reads the MyBible module at
`sources/LXX-Rahlfs-1935/11_end-users_files/MyBible/Bibles/LXX1.SQLite3`, table `verses`,
stripping the `<S>`/`<m>` tags to recover the word forms and parse codes, and the
`09a_LXX_lexicon` for each word's lemma — the local check on `data/*/*.morph.txt`. Nothing
else reads it: `build/words.py` takes its senses from the Perseus Middle Liddell above.

## What these can and cannot verify

| | word forms | accents | punctuation | capitalisation |
| --- | --- | --- | --- | --- |
| SBLGNT | yes | yes | yes | yes |
| Rahlfs (CCAT-derived) | yes | yes | **no** | **no** |
| Rahlfs, printed (the scan above) | yes | yes | yes | yes |

The CCAT data is a word-level morphological analysis with no sentence punctuation, so it can
check a transcription's words but not its pointing. The pointing comes from the printed page
each verse cites.
