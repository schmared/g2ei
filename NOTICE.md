# Licensing and attribution

This project is licensed in two layers, because the code and the interpretive work are
different kinds of thing and want different terms.

| what | covers | licence |
| --- | --- | --- |
| **Code** | `build/`, `templates/` | MIT — [`LICENSE`](LICENSE) |
| **Content** | `data/`, `reference/`, `site/`, `README.md`, `CLAUDE.md` | CC BY-SA 4.0 — [`LICENSE-CONTENT`](LICENSE-CONTENT) |

The content licence covers this project's **original contributions**: the notes, the
gloss-chains, and the unanchored and anchored reading texts. It does not and cannot cover
the Greek source lines, which are quotations of ancient texts from the named editions below
and remain under those editions' terms.

To attribute the content, name the project and link back to it, and keep derivative
interpretive work under CC BY-SA 4.0.

## Source editions

The Greek is not this project's work. Two editions are used.

### New Testament — SBL Greek New Testament

> The SBL Greek New Testament (SBLGNT), copyright 2010 by the Society of Biblical
> Literature and Logos Bible Software, edited by Michael W. Holmes. Licensed under a
> [Creative Commons Attribution 4.0 International License](https://creativecommons.org/licenses/by/4.0/).
> <https://sblgnt.com>

CC BY 4.0 — attribution is the only condition. Commercial use is permitted and there is no
share-alike requirement. (The SBLGNT was relicensed to CC BY 4.0 in December 2022; older
descriptions of it as non-commercial-only refer to the superseded EULA.)

CC BY 4.0 material may be incorporated into a CC BY-SA 4.0 work, so the John text and this
project's content licence are compatible.

### Old Testament — Septuagint, Rahlfs 1935

> LXX-Rahlfs-1935, copyright 2017 Eliran Wong, licensed under
> [CC BY-NC-SA 4.0](http://creativecommons.org/licenses/by-nc-sa/4.0/).
> <https://github.com/eliranwong/LXX-Rahlfs-1935>
> Based on CCAT/CATSS at the University of Pennsylvania
> (<http://ccat.sas.upenn.edu/gopher/text/religion/biblical/lxxmorph/>), directed by
> Robert Kraft; the CCAT material is itself derivative, from the Thesaurus Linguae Graecae
> and with permissions from the United Bible Societies among others.

**This dataset is not redistributed here, and should not be committed to this repository.**
Three reasons:

1. **NonCommercial.** CC BY-NC-SA 4.0 bars commercial use. Bundling it would push that
   restriction onto the whole distribution.
2. **ShareAlike.** Its share-alike term is incompatible with CC BY-SA 4.0 — the two cannot
   be combined into one licensed work.
3. **The CCAT access condition.** The upstream repository states that readers must agree to
   send a CCAT user declaration before downloading any of its data. Re-publishing that data
   in an open repository removes the gate the upstream author put in front of it.

`sources/` is therefore excluded by [`.gitignore`](.gitignore). See
[`sources/README.md`](sources/README.md) for how to fetch the editions locally.

## A note on the Greek in `data/`

`data/` contains a small number of Greek verses transcribed from the editions above.

- The **John** verses are SBLGNT, CC BY 4.0, attributed above.
- The **Genesis** verses are the text of Rahlfs' 1935 edition. Alfred Rahlfs died in 1935,
  so the edition itself has been out of copyright in life-plus-70 jurisdictions since 2006.
  What the CC BY-NC-SA licence above covers is Eliran Wong's *database* — the morphological
  tagging, transliteration, glosses and indexing — not the underlying edition, and this
  project takes none of that. A handful of verses is in any case far short of the
  "substantial portion" that a database right attaches to.

That reasoning is stated so a reader can check it, not because it is a legal opinion. None
of this is legal advice; if the project is ever put to commercial use, read the upstream
terms directly.
