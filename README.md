# Exhaustive Interpretive Rendering

An exhaustive **interpretation** of the Greek scriptures, not a translation.

Every load-bearing word is opened to the full range its lexicon gives it and left open. No
single English equivalent is chosen, because choosing one is where the meaning goes. It
follows the intent of the Amplified Bible but carries it all the way through, with far more
verbosity, to stop concepts falling out of the English.

The Old Testament is read from the **Greek** — the Septuagint, never the Masoretic Hebrew —
so that when the New Testament quotes it, the quotation is visible on the page rather than
buried in a footnote. `Ἐν ἀρχῇ` opens Genesis 1:1 and John 1:1 alike, and the reading text
says so.

The editorial rules are in [CLAUDE.md](CLAUDE.md). This file covers how the thing is built.

## What a verse produces

Four things, in this order:

1. **Greek** — the source line, unmodified.
2. **Notes** — lexical range, verbal aspect, grammar English can't reproduce, and
   Hebrew↔Greek divergences. Terse and factual; no devotional register.
3. **Unanchored** — headwords removed entirely. The reader rebuilds the referent from the
   gloss-chain alone.
4. **Anchored** — the conventional headword kept, with the chain trailing behind it.

The rendered page shows the last three side by side, with the Greek above them and a
control that closes the word spaces — *scriptio continua*, which is what a fourth-century
reader actually met on the page.

## Base texts

| | edition | source in this repo |
| --- | --- | --- |
| Old Testament | Septuagint, Rahlfs 1935 | `sources/LXX-Rahlfs-1935/` |
| New Testament | SBLGNT | `sources/sblgnt/` |

## Quick start

Python 3, standard library only — no dependencies.

Build `site/index.html` from the data:

```bash
python build/render.py
```

Check a chapter before committing it:

```bash
python build/validate.py -v
```

Confirm the render still matches the baseline byte-for-byte:

```bash
python build/render.py --check reference/gold-standard.html
```

## Layout

```
data/<BOOK>/<chapter>.json   source of truth — a JSON array, one object per verse
build/render.py              data -> site/index.html
build/validate.py            mechanical checks; run before committing
templates/page.html          the page shell (masthead, CSS, controls, footer, script)
templates/verse.html         one verse section — the three-panel layout
site/                        generated output — never hand-edit
reference/gold-standard.html the rendering baseline; regenerate, don't edit
reference/lexicon-notes.md   recurring gloss-chains, reused verbatim across books
sources/                     the Greek source editions (see Licensing below)
CLAUDE.md                    editorial conventions
```

Content lives in JSON and the HTML is **generated**. Nothing is hand-written per chapter —
otherwise the conventions drift between files and can't be checked mechanically.

## Verse schema

```json
{
  "ref": "GEN 1:1",
  "greek": "Ἐν ἀρχῇ ἐποίησεν ὁ θεὸς τὸν οὐρανὸν καὶ τὴν γῆν.",
  "hint": "The oldest manuscripts carry no spaces, no accents, no lower case.",
  "notes": [
    { "lemma": "ἐν ἀρχῇ", "flag": null, "text": "ἀρχή holds together two things…" },
    { "lemma": "ἐποίησεν", "flag": "divergence", "text": "Aorist of ποιέω…" }
  ],
  "unanchored": "Within, inside of, and by means of the first moment…",
  "anchored": "In the beginning — within, inside of, and by means of…",
  "names": []
}
```

`flag` is one of `null`, `divergence`, `not in this text`, `name`, `variant`.

Optional keys: `notes_sub` and `banner` override the per-book defaults in `render.py`;
`demo` turns the section into a standalone convention demonstration (used for John 1:6,
which is where the naming rule is shown, since none of the four prologue verses contains a
proper name).

### Inline markup

Three conventions inside the JSON strings, all expanded in one place in `render.py`, so the
data stays free of HTML:

| written | becomes |
| --- | --- |
| `*emphasis*` | `<em>emphasis</em>` |
| `[[flag]]` | the note's flag badge **at that position** — a note with a flag and no marker gets it prepended |
| `[[name:Ἰωάννης]]` | the name span and its gloss, drawn from the verse's `names` list |

`[[flag]]` is positional because Genesis 1:1 puts its `divergence` badge mid-note rather
than at the head. `[[name:…]]` resolves to the Greek transliteration in the unanchored panel
and the conventional English form in the anchored one, so the two-form rule is mechanical
rather than retyped:

```json
"names": [{
  "greek": "Ἰωάννης",
  "unanchored": "Iōannēs",
  "anchored": "John",
  "gloss": "(Ἰωάννης, from Hebrew Yôḥānān, \"Yah has shown favour\")"
}]
```

## Adding a chapter

One chapter per session. Commit per chapter, with the reference as the message.

1. **Read [`reference/lexicon-notes.md`](reference/lexicon-notes.md) first** and reuse
   existing gloss-chains **verbatim**. ἀρχή must read the same way in Genesis 1:1 and John
   1:1 — that consistency is what makes the quotation visible. If a recurring word has no
   entry, establish one and add it before continuing.
2. Write `data/<BOOK>/<chapter>.json`.
3. Add the chapter to `PAGE` in `build/render.py`, and the book to `BOOKS` and to
   `EDITIONS` in `build/validate.py` if it is new.
4. Append any newly-established gloss-chains to `reference/lexicon-notes.md`.
5. Run `python build/validate.py` and fix what it reports.
6. Run `python build/render.py`.

## What validation checks

| check | what it does |
| --- | --- |
| `fields` | four fields present and non-empty; notes well-formed; `flag` in the permitted vocabulary; every `[[name:…]]`/`[[flag]]` marker resolvable |
| `names` | every proper name in the Greek glossed on first occurrence **in the chapter**, in **both** reading texts, and bare thereafter |
| `banned` | no phrase from `BANNED_PHRASES` in either reading text |
| `anchors` | no headword from `ANCHORS` in the unanchored text |
| `greek` | the Greek matches the source edition character-for-character |

`BANNED_PHRASES` and `ANCHORS` are maintained editorial lists at the top of
`build/validate.py`. They grow as chapters are written.

Two things worth knowing before editing them:

- **Anchor words legitimately appear inside gloss-chains.** `unfurnished` is the anchor for
  ἀκατασκεύαστος *and* a link in its own chain. Writing anchors as full phrases
  (`the Word`, not `Word`) resolves most apparent collisions; `allow` handles the rest.
- **Banned phrases are checked against the reading texts only.** The notes are exactly where
  those phrases are supposed to be named and refused — Genesis 1:2 says in its apparatus
  that *face of the waters* is not in this text.

Proper names are detected as capitalised words that are not sentence-initial, since both
editions capitalise only sentence starts and names. Inflected forms are matched to the
nominative in `names` on a shared accent-stripped prefix, so Ἰωάννου finds Ἰωάννης.

## Known limitation: Septuagint punctuation is unverified

`validate.py` checks the Greek character-for-character for the New Testament, but for the
Old Testament it can only check **word forms**. It prints a standing `note` saying so rather
than reporting a clean pass.

The reason is structural. Every freely redistributable digital Rahlfs text descends from the
[CCAT/CATSS lxxmorph](http://ccat.sas.upenn.edu/gopher/text/religion/biblical/lxxmorph/)
database, which is a word-level morphological analysis in betacode and carries **no sentence
punctuation and no capitalisation**. This was confirmed against three independent
redistributions — the [eliranwong](https://github.com/eliranwong/LXX-Rahlfs-1935) data in
`sources/`, the [CenterBLC](https://github.com/CenterBLC/LXX) TextFabric edition, and Blue
Letter Bible's LXX, which credits CCAT. None carries pointing.

So the punctuation in `data/GEN/*.json` currently rests on editorial judgement, not on a
source. Three ways to close that gap, none yet taken:

- **Rahlfs–Hanhart (2006)** — punctuated, but under Deutsche Bibelgesellschaft copyright and
  available only through Logos, Accordance and similar. Not redistributable here.
- **The printed 1935 edition** — [scanned on the Internet
  Archive](https://archive.org/details/septuaginta-id-est-vetus-testamentum-graece-iuxta-lxx-interpretes-edidit-by-alfred-rahlfs-1935).
  Transcribing the pointing per chapter as it is written is feasible at one chapter per
  session, and is the only route that verifies against *this* edition.
- **Swete as a witness** — [`eliranwong/LXX-Swete-1930`](https://github.com/eliranwong/LXX-Swete-1930)
  ships `01-Swete_word_with_punctuations.csv` alongside a `00-Swete_versification.csv` with
  the same word-index layout as the Rahlfs data already in `sources/`, so it drops in with
  little work. It really is punctuated — Genesis 1:1 ends `γῆν.` and 1:2 runs
  `ἀκατασκεύαστος, … ἀβύσσου· … ὕδατος.`

The Swete route carries a caveat worth stating plainly: Swete is a **different edition**, a
diplomatic text of Codex Vaticanus rather than Rahlfs' eclectic one. It can serve as a
witness that flags where our pointing looks unusual, but it cannot become the base text
without quietly making the Old Testament a hybrid — the kind of drift the project's rules
exist to prevent. It already disagrees with the current data at Genesis 1:2, reading
`ἀβύσσου·` where we have `ἀβύσσου,`.

## Licensing

Two layers, because the code and the interpretive work want different terms:

| what | covers | licence |
| --- | --- | --- |
| **Code** | `build/`, `templates/` | MIT — [`LICENSE`](LICENSE) |
| **Content** | `data/`, `reference/`, `site/`, and the docs | CC BY-SA 4.0 — [`LICENSE-CONTENT`](LICENSE-CONTENT) |

The content licence covers this project's own contributions — the notes, the gloss-chains,
and the two reading texts. The Greek source lines are quotations from the editions below and
stay under their terms.

**`sources/` is not committed.** The Septuagint data is CC BY-NC-SA 4.0, whose NonCommercial
and ShareAlike terms would otherwise propagate to the whole distribution, and its upstream
gates access behind a CCAT user declaration that an open repository would bypass.
[`sources/README.md`](sources/README.md) has fetch instructions; without the sources the
`greek` check reports `SKIP` and the other four still run.

| source | licence |
| --- | --- |
| SBLGNT | **CC BY 4.0** — attribution only; commercial use fine. © 2010 SBL and Logos Bible Software, ed. Michael W. Holmes |
| LXX-Rahlfs-1935 | **CC BY-NC-SA 4.0** © 2017 Eliran Wong, from CCAT/CATSS (Univ. of Pennsylvania), itself derived from the TLG with UBS permissions |

Full attributions, and the reasoning about the Greek quoted in `data/`, are in
[`NOTICE.md`](NOTICE.md).
