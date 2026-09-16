# Licensing and attribution

This project is licensed in two layers, because the code and the interpretive work are
different kinds of thing and want different terms.

| what | covers | licence |
| --- | --- | --- |
| **Code** | `build/`, `templates/` | MIT — [`LICENSE`](LICENSE) |
| **Content** | `data/`, `reference/`, `site/`, `README.md`, `CLAUDE.md` | CC BY-SA 4.0 — [`LICENSE-CONTENT`](LICENSE-CONTENT) |

The content licence covers this project's **original contributions**: the notes, the
gloss-chains, the unanchored and anchored reading texts, and the project's own morphological
analysis of the Septuagint (`data/*/*.morph.txt`). It does not and cannot cover the Greek
source lines, which are quotations of ancient texts from the editions below, or the
third-party material in the word-by-word files — MorphGNT's analysis and the lexicon senses.
Those remain under their sources' terms.

To attribute the content, name the project and link back to it, and keep derivative
interpretive work under CC BY-SA 4.0.

Everything committed to this repository is either the project's own work, out of copyright,
or openly licensed. Nothing is copied from the CCAT Septuagint data, which carries terms an
open repository cannot meet (see below).

## Source editions

### New Testament — SBL Greek New Testament

> The SBL Greek New Testament (SBLGNT), copyright 2010 by the Society of Biblical
> Literature and Logos Bible Software, edited by Michael W. Holmes. Licensed under a
> [Creative Commons Attribution 4.0 International License](https://creativecommons.org/licenses/by/4.0/).
> <https://sblgnt.com>

CC BY 4.0 — attribution is the only condition. Commercial use is permitted and there is no
share-alike requirement. (The SBLGNT was relicensed to CC BY 4.0 in December 2022; older
descriptions of it as non-commercial-only refer to the superseded EULA.) CC BY 4.0 material
may be incorporated into a CC BY-SA 4.0 work, so the John text and this project's content
licence are compatible.

### Old Testament — Rahlfs, *Septuaginta* (1935), transcribed from print

> Alfred Rahlfs, ed., *Septuaginta, id est Vetus Testamentum graece iuxta LXX interpretes*,
> 2 vols. Stuttgart: Privilegierte Württembergische Bibelanstalt, 1935. Transcribed from the
> 1950 printing (*editio quarta*), a reprint of the 1935 text.

The Greek of every Old Testament verse is **transcribed by hand from the printed page**, and
each verse records that page in its `print` field. The punctuation is Rahlfs's own.

Copyright. Rahlfs died in 1935, so the edition has been out of copyright since 2006 wherever
the term is the author's life plus 70 years. The United States is less settled: a foreign
work published in 1935 may have had its copyright restored there until the end of 2030,
although the text of a critical edition of an ancient work may not be protected in the US at
all. Printed a verse at a time beside commentary, the practical risk is small, and the
question lapses entirely in 2031. *Rahlfs–Hanhart* (2006) is a later revision under
Deutsche Bibelgesellschaft copyright and is not used.

### Reference only — the CCAT Septuagint data

> LXX-Rahlfs-1935, copyright 2017 Eliran Wong, licensed under
> [CC BY-NC-SA 4.0](http://creativecommons.org/licenses/by-nc-sa/4.0/).
> <https://github.com/eliranwong/LXX-Rahlfs-1935>
> Based on CCAT/CATSS at the University of Pennsylvania
> (<http://ccat.sas.upenn.edu/gopher/text/religion/biblical/lxxmorph/>), directed by
> Robert Kraft; the CCAT material is itself derivative, from the Thesaurus Linguae Graecae
> and with permissions from the United Bible Societies among others.

This dataset is used **only locally, to check** the transcription's word forms and the
project's own morphology. Nothing from it is committed. Its terms rule out committing it:

1. **The CCAT user agreement** requires anyone who receives the material to control access
   to it, and to have anyone they pass *any portion* to sign the agreement too. An open
   repository can do neither. This holds whether or not money is involved.
2. **NonCommercial and ShareAlike.** CC BY-NC-SA 4.0 material can only be passed on under
   CC BY-NC-SA 4.0, so it could not sit under this project's CC BY-SA 4.0 or MIT licences,
   which permit commercial use downstream.

`sources/` is therefore excluded by [`.gitignore`](.gitignore). Anyone who wants to run the
checks fetches it and signs CCAT's agreement themselves — see
[`sources/README.md`](sources/README.md).

## The word-by-word files

`data/*/*.words.json` record, for each word of the verses rendered, its dictionary form, its
parse — restated in plain English by `build/words.py` — and the opening senses of its lexicon
entry.

- **Old Testament lemma and parse** are the project's own analysis, in
  `data/*/*.morph.txt`, checked against the CCAT analysis locally. They are original to this
  project and fall under the content licence.
- **New Testament lemma and parse** come from MorphGNT, CC BY-SA 3.0, which may be adapted
  under CC BY-SA 4.0:
  > Tauber, J. K., ed. (2017) *MorphGNT: SBLGNT Edition*. <https://github.com/morphgnt/sblgnt>,
  > DOI 10.5281/zenodo.376200.
- **Senses** are from Liddell and Scott's *Intermediate Greek-English Lexicon* (1889), which
  is out of copyright, in the Perseus Digital Library's XML edition (text 1999.04.0058),
  licensed CC BY-SA 3.0 US and adaptable under CC BY-SA 4.0. Perseus asks to be offered any
  modifications made to the lexicon; this project only reads it.
  > Text provided by Perseus Digital Library, with funding from The Annenberg CPB/Project.
  > <http://www.perseus.tufts.edu/hopper/>, read from <https://github.com/blinskey/middle-liddell>.

  Where it has no entry, senses are from LSJ as published by
  [PerseusDL](https://github.com/PerseusDL/lexica), CC BY-SA 4.0 — at present for one word,
  ἀκατασκεύαστος.

The build reads nothing from the CCAT dataset; only `validate.py` does, as a local check.

None of this is legal advice.
