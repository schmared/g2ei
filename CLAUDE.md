# Exhaustive Interpretive Rendering — Project Conventions

## What this is

An exhaustive **interpretation**, not a translation. Every load-bearing word is opened to
the full range its lexicon gives it and left open. No single English equivalent is chosen,
because choosing one is where the meaning goes. Follows the intent of the AMPC but carries
it all the way through, with far more verbosity, to prevent concept loss in English.

**Base texts:**
- Old Testament — Septuagint (Rahlfs–Hanhart). Never the Masoretic Hebrew.
- New Testament — Nestle-Aland / SBLGNT.

Greek-to-English throughout, so that when the NT quotes the OT the citation is visible on
the page rather than buried in a footnote.

## Output structure

Every verse produces four things, in this order:

1. **Greek** — the source line, unmodified.
2. **Notes** — lexical range, verbal aspect, grammar English can't reproduce, and
   Hebrew↔Greek divergences.
3. **Unanchored** — headwords removed entirely; the reader rebuilds the referent from the
   gloss-chain alone.
4. **Anchored** — the conventional headword kept, with the chain trailing behind it,
   set off by em dashes.

## Hard rules

### Never import from other English versions
If a familiar phrase from the KJV/ESV/NIV has no basis in *this* Greek text, it does not
appear in the reading text. Flag it in the notes with `not in this text` instead.

Worked example — Gen 1:2: the Hebrew has *face of* at both the deep and the waters; the
LXX drops it at both points, reading only ἐπάνω τῆς ἀβύσσου / ἐπάνω τοῦ ὕδατος. So
"the face of the waters" must not appear. This is the single most common failure mode.
Check for it on every verse.

### Divergences stay in the notes
Hebrew↔Greek differences never enter either reading text. The Septuagint's own reading
*is* the text. Where it parts from the Hebrew, that's a fact about the text, not a defect
to quietly repair. Mark with the `divergence` flag.

### Verbal aspect goes in the text, not a footnote
Where Greek aspect carries weight English can't:
- aorist → "one completed act seen whole, not a process observed in progress"
- imperfect → "and kept on being" / "was, and was continuously"
- perfect → a standing resultant state, not a past event

### ἦν vs. ἐγένετο
Load-bearing across the whole Johannine prologue and anywhere else it appears. εἰμί gets
"was already in unbroken existence without any point of having come to be." γίνομαι gets
"came to be, arose, was brought into existence." Never flatten both to "was."

### The article
Articular θεός → "He who is God definitively, the One the article marks out, the known and
the only." Anarthrous → qualitative: "everything that God is by nature, deity in full and
undiminished kind." Note fronted anarthrous predicate nominatives explicitly.

### Names and transliterations
Every proper name and obvious transliteration carries its meaning in parentheses,
in **both** reading texts:

- Unanchored uses the Greek form: `Iōannēs (Ἰωάννης, from Hebrew Yôḥānān, "Yah has shown favour")`
- Anchored uses the conventional English form: `John (Ἰωάννης, from Hebrew Yôḥānān, "Yah has shown favour")`

A name left unglossed is a hole in the sentence — a word that meant something to the first
hearer and means nothing now. Gloss on **first occurrence per chapter**, bare thereafter,
so genealogies stay readable.

### Prepositions
ἐν → "within, inside of, and by means of." πρός + accusative → directional, never static
"with": "toward, facing, oriented to, in living motion and address toward." Where the
writer could have used παρά/μετά/σύν and didn't, say so in the notes.

## Register

The unanchored text must read as continuous prose — one sentence, commas and em dashes
carrying the chain. It is not a list. Read it aloud; if it sounds like a glossary entry,
rewrite it.

Notes are terse and factual. No devotional register, no homiletics, no theological
advocacy. Where a clause has been contested, state the grammatical facts and what each
reading requires — do not adjudicate.

## Repo layout

```
/data/<book>/<chapter>.json     source of truth, one object per verse
/build/render.py                data → HTML
/templates/verse.html           the three-panel layout
/site/                          generated output — never hand-edit
/reference/lexicon-notes.md     recurring gloss-chains, kept consistent across books
CLAUDE.md                       this file
/sources						original Greek text resources to use as reference instead of relying on search data
```

Content lives in JSON. HTML is **generated**, never hand-written per chapter — otherwise
the conventions drift between files and can't be checked mechanically.

## Verse schema

```json
{
  "ref": "GEN 1:1",
  "greek": "Ἐν ἀρχῇ ἐποίησεν ὁ θεὸς τὸν οὐρανὸν καὶ τὴν γῆν.",
  "notes": [
    {
      "lemma": "ἀρχή",
      "flag": null,
      "text": "Holds together two things English must split: the temporal origin-point, and ruling precedence..."
    },
    {
      "lemma": "ἐποίησεν",
      "flag": "divergence",
      "text": "Aorist of ποιέω, the everyday verb for making. Hebrew bārā' in this stem never takes a human subject; ποιέω takes any subject at all. The exclusivity is not in the Greek."
    }
  ],
  "unanchored": "Within, inside of, and by means of the first moment...",
  "anchored": "In the beginning — within, inside of, and by means of the first moment...",
  "names": []
}
```

`flag` is one of: `null`, `divergence`, `not in this text`, `name`, `variant`.

## Working rhythm

- One chapter per session. Commit per chapter with the reference as the message.
- Before writing a chapter, read /reference/lexicon-notes.md and reuse existing
  gloss-chains verbatim. If a recurring word has no entry, establish one and add
  it before continuing.. ἀρχή should read the same way in Gen 1:1 and John 1:1 —
  that consistency is what makes the quotation visible.
- After writing a chapter, append any newly-established gloss-chains to that file.
- Run `python build/validate.py` before committing.

## Validation

`build/validate.py` must check:
- every verse has all four fields, non-empty
- every proper name in the Greek has a gloss on first occurrence in the chapter
- no banned imported phrases (maintain a list; seed it with "face of the waters")
- unanchored text contains no headword from the anchored version's anchor list
- Greek text matches the source edition character-for-character

Mechanical checks catch drift that reading won't.

## Scope order

Genesis and John first, then LXX Psalms. Poetry is where unanchored earns its keep.
