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

The second morphology pass settles questions of convention — what part of speech a small word
is, which spelling a lemma takes — by counting what MorphGNT does across the whole New
Testament (see `reference/second-pass-brief.md`), so it is worth fetching every book, about
9 MB in all:

```bash
for f in 61-Mt 62-Mk 63-Lk 64-Jn 65-Ac 66-Ro 67-1Co 68-2Co 69-Ga 70-Eph 71-Php 72-Col 73-1Th 74-2Th 75-1Ti 76-2Ti 77-Tit 78-Phm 79-Heb 80-Jas 81-1Pe 82-2Pe 83-1Jn 84-2Jn 85-3Jn 86-Jud 87-Re; do curl -sL -o sources/morphgnt/$f-morphgnt.txt https://raw.githubusercontent.com/morphgnt/sblgnt/master/$f-morphgnt.txt; done
```

## Lexicon — Middle Liddell, Perseus XML

Liddell and Scott's *Intermediate Greek-English Lexicon* (1889) as the Perseus Digital
Library encoded it — CC BY-SA 3.0 US, adaptable under CC BY-SA 4.0. `build/words.py` reads
each word's senses from it, and the headword rule takes each headword from it.

```bash
curl -sL --create-dirs -o sources/middle-liddell/Perseus_text_1999.04.0058.xml https://raw.githubusercontent.com/blinskey/middle-liddell/master/Perseus_text_1999.04.0058.xml
```

## Lexicon — LSJ, where Middle Liddell has no entry

Liddell–Scott–Jones as [PerseusDL](https://github.com/PerseusDL/lexica) publishes it,
CC BY-SA 4.0. Middle Liddell is an abridgement and drops words the Septuagint uses —
ἀκατασκεύαστος (Gen 1:2), ἁγιάζω (Gen 2:3) — so those senses come from LSJ.

The lexicon is split into 27 files of about 270 MB in total, alphabetically. Fetch only the
files a chapter needs:

```bash
curl -sL --create-dirs -o sources/lsj/grc.lsj.perseus-eng1.xml https://raw.githubusercontent.com/PerseusDL/lexica/master/CTS_XML_TEI/perseus/pdllex/grc/lsj/grc.lsj.perseus-eng1.xml
```

| file | covers | fetched for |
| --- | --- | --- |
| `eng1` | the whole of alpha, `*a` to `ἄωτος` (42 MB) | ἀκατασκεύαστος (Gen 1:2), ἁγιάζω (Gen 2:3), ἀσφαλτόω (Gen 6:14), ἀνάστημα (Gen 7:23) |
| `eng4` | delta (15 MB) | διαναπαύω (Gen 5:29), διώροφος (Gen 6:16) |
| `eng5` | epsilon (40 MB) | ἑβδομηκοντάκις (Gen 4:24), εὐαρεστέω (Gen 5:22), ἑξακοσιοστός (Gen 7:11), ἐλαττονόω (Gen 8:3) |
| `eng13` | mu (12 MB) | μώλωψ (Gen 4:23) |
| `eng16` | omicron (12 MB) | ὀστέον (Gen 2:23), ὀκτώ (Gen 5:28) |
| `eng17` | pi, `p` to `πώϋξ` (38 MB) | πράσινος (Gen 2:12), ποιμήν (Gen 4:2), πρῶτος (Gen 8:5), filed under πρότερος |
| `eng21` | sigma (23 MB) | σύ (Gen 3), which Middle Liddell omits |
| `eng22` | tau (12 MB) | τρεῖς (Gen 5:32), filed under τρία |
| `eng24` | phi (8 MB) | φλόγινος (Gen 3:24) |
| `eng26` | psi (2 MB) | ψαλτήριον (Gen 4:21) |

To find which file holds a letter without downloading any of them, read the head of a few
and look at the first entry's key:

```bash
curl -sL -r 0-199999 https://raw.githubusercontent.com/PerseusDL/lexica/master/CTS_XML_TEI/perseus/pdllex/grc/lsj/grc.lsj.perseus-eng17.xml | grep -o 'key="[^"]*"' | head -1
```

`eng4` opens at delta, `eng5` epsilon, `eng13` mu, `eng14` nu, `eng16` omicron, `eng20` rho,
`eng21` sigma, `eng22` tau.

Entries are `<entryFree key="…">` in Beta Code, with `<tr>` for each translation, as in
Middle Liddell. Some entries define a word only by cross-reference (`ἁγιάζω` reads
`= ἁγίζω`), in which case the senses are the ones the reference points at. `build/words.py`
carries the handful found so far in its `LSJ` table, each with the entry it came from.

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
