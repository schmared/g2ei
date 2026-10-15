# Exhaustive Interpretive Rendering — Project Conventions

## What this is

An exhaustive **interpretation**, not a translation. Every load-bearing word is opened to
the full range its lexicon gives it and left open. No single English equivalent is chosen,
because choosing one is where the meaning goes. Follows the intent of the AMPC but carries
it all the way through, with far more verbosity, to prevent concept loss in English.

**Base texts:**
- Old Testament — Septuagint, Rahlfs's 1935 edition, transcribed from the printed page.
  Not Rahlfs–Hanhart, a later revision under copyright; never the Masoretic Hebrew.
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
4. **Anchored** — each word headed by the first sense its lexicon gives, in the form the
   text uses, with the chain trailing behind it, set off by em dashes and shaded. The
   chains are word for word the unanchored text: the anchored text is the unanchored text
   with the headwords added, and nothing else.

Beside the Greek, where `/sources` allow it, a **word-by-word** layer: every form with its
dictionary form (lemma), its parse, and the opening senses of its lexicon entry. A
concordance stops at the lemma; this shows what the particular form adds.

## Hard rules

### Headwords and chains — strict and literal, even where awkward
The reading text is expansion of the Greek words' definitions, not composition. Each
load-bearing word is one unit: a **headword** and its **chain**.

- **The headword is the lexicon's first sense, in the form the text uses.** The lexicon is
  Middle Liddell as Perseus encodes it, in `/sources` — the first translation in the entry's
  first numbered sense. **LSJ answers only where Middle Liddell has no entry** under the
  word's own key or a close form of it: another spelling (κρυφῇ under κρυφῆ), the voice the
  text uses filed apart (κατανύσσω under κατανύσσομαι), the word filed as a section of
  another (πρῶτος as πρότερος B), or a truncated key (ποιμήν under `poimh/`). A close form
  counts only where it covers the form in the text — Middle Liddell's middle διαναπαύομαι
  does not say what the active of GEN 5:29 means, so that word reads LSJ — and never a
  compound under its simplex or a verb under its noun, which would be composing rather than
  reading. Where Middle Liddell gives less than LSJ, Middle Liddell is still the reading:
  LSJ is not the basis, and saying more is not a reason to switch. Both are CC BY-SA, so
  licensing draws no line between them. For
  a preposition, the first sense for the case it governs; for a word used as a noun, the
  first noun sense; for a particle, the senses its parse calls for. Where the encoding
  loses a translation the printed entry gives — Perseus tags εἰ's *Lat. si, if* as Latin
  entire, so the English *if* never reaches a `<tr>` — `MARKUP_LOST` in `build/words.py`
  restores it, quoting the entry and naming the element that took it. That adds nothing
  the lexicon does not say. 54 entries have a run of that shape and 24 had lost a
  translation; `build/validate.py` fails on a new one until it is settled in `MARKUP_LOST`
  or in `LATIN_ONLY`, which records the runs that are Latin throughout. Tense, voice and person come from the Greek form (ποιέω *to make* →
  ἐποίησεν *made*), and so does the article: English gets one where the Greek has one and
  nowhere else (ἐν ἀρχῇ → *in beginning*; ὁ θεός → *the God*). No translation is consulted
  — lexicon glosses ignore context, and that is the point.
- The chain is the whole range, identical in both panels. Unanchored shows the chain;
  anchored shows `headword — chain —`. The headword may repeat inside its own chain; it is
  the chain's first sense.
- The headword never stands bare in the unanchored text: nothing that belongs in a unit is
  written as plain text.
- **A word is a unit exactly when its entry says more than its headword does.** More can be
  a second sense, or simply more words in the first one: κιβωτός has one numbered sense and
  still wants a unit, because that sense reads *a wooden box, chest, coffer* and the headword
  keeps only the box. Where the entry says no more, the word is plain text — a chain that
  repeats its headword prints `headword — headword —` and says nothing the plain text
  would not. It holds both ways, because either way round is a word read wrong, and
  for 1,038 words of Genesis the shut half had happened by accident rather than by decision.
  Outside it are only the words the project renders by a formula of its own: the article,
  εἰμί, and the ἐν that merges into its object's unit. **A particle is opened by its parse**,
  as a preposition is opened by the case it governs — καί read as an adverb takes the
  adverbial senses and is a unit; καί read as the connective is the conjunction and stays
  plain text. Middle Liddell writes most of a particle's entry as prose about how the word
  works, and only the translations in it are senses: the labels of a construction (*fear*,
  *a wish*) and the sentences illustrating it are not, and go in `NOT_SENSES` with the
  reason.
- No filler. Nothing enters either reading text that does not expand a Greek word —
  observations *about* the text (a quotation, a withheld verb) go in the notes.
- No capitals the Greek does not mark. The manuscripts have none, so nothing is capitalised
  to make it a title — *spirit*, *word* — and no pronoun standing for God takes a reverential
  capital: *he who is God definitively*, *facing him*. Proper names are capitalised, and
  *God*, as the lexicon prints it.
- No em dashes inside a chain; they delimit chains in the anchored text.
- Awkwardness is acceptable. It shows the seams; smoothing them over is how the two panels
  drifted apart before.
- Record each headword's derivation — lexicon, sense, inflection — in
  `/reference/lexicon-notes.md`.

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
Articular θεός → "he who is God definitively, the one the article marks out, the known and
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

Both occurrences are written `[[name:…]]`. The first carries a full `names` entry; every
later one carries an entry marked `"bare": true` with no `gloss`, which prints the form
alone. A later occurrence is never plain text: the two panels print different forms of a
name (*Edem* / *Eden*), and plain text cannot.

Both editions also capitalise the first word of direct speech (Gen 1:3 *Γενηθήτω*). List
such words in the verse's `speech` field, so `validate.py` does not take them for names.

Where the printed page has a misprint of its own (Gen 24:58 *τοῦτου*, for τούτου), the
transcription keeps it. List the printed form in the verse's `printed` field, and say so in a
note, so the check against the local module does not report it.

A transliteration the edition prints in lower case (Gen 3:24 *τὰ χερουβιμ*) is still a name
here: give it a `names` entry and a `[[name:…]]` marker, with no capital in either panel.
`validate.py` finds it by its entry, since it has no capital to be found by — and finds a
name that opens a sentence (Gen 4:1 *Αδαμ δὲ ἔγνω*) the same way, since that capital proves
nothing.

### A noun marks its own case
The genitive reads *of*, the dative *to*, everywhere and whatever governs the word: *from
of the earth*, *above of the water*. The form stays visible in English, and the marker never
depends on a judgement about what governs what or about which use of a dative is in play —
ὀφθαλμός's dative is *to the eyes* whether it is instrumental or not. The one exception is a
preposition that merges into its object's unit: *within, inside of, and by means of the well*
is ἐν's own English, not a case-marker, and it keeps the lead.

### The article goes inside its word's unit
τῷ οἴκῳ is `[[to the house|…]]`, not a plain *the* before `[[to house|…]]` — which printed
*the to house*, a word standing bare that belongs in a chain. Nor a plain *the* before a unit
that carries the article already, which printed *the the man*. An articular infinitive
becomes a gerund, as ἐν τῷ ἐκτρῖψαι reads *in the rubbing out*.

**Where the article makes a noun, it carries its noun, and the noun follows its gender**:
masculine and feminine *one* / *ones*, neuter *thing* / *things*, by number — the line a
Greek reader hears between persons and things. Over a participle that is inside the unit,
`the one coming`, `the things going into`. Over a phrase or an adverb there is no one unit to
hold it, so it stands as plain text with its case marked: οἱ μετ' αὐτοῦ is *the ones in the
midst of him*, τὰ ὀπίσω *the things backwards*, τῶν ἐπὶ τῆς γῆς *of the things upon of the
earth*, τὰ αὐτοῦ *the things of him*. Bare *the* before a preposition carries none of that and
is not English.

The one plain *the* that stands before a unit is ὁ δέ's, where ὁ is the pronoun subject and
the prose reads *the, but, … he said*.

### Prepositions
ἐν → "within, inside of, and by means of." πρός + accusative → directional, never static
"with": "toward, facing, oriented to, in living motion and address toward." Where the
writer could have used παρά/μετά/σύν and didn't, say so in the notes.

## Register

The unanchored text must read as continuous prose — one sentence, commas and em dashes
carrying the chain. It is not a list. Read it aloud; if it sounds like a glossary entry,
rewrite it — by ordering and punctuating the chain, never by adding words the Greek does
not carry. Awkward is acceptable; filler is not.

Notes are terse and factual. No devotional register, no homiletics, no theological
advocacy. Where a clause has been contested, state the grammatical facts and what each
reading requires — do not adjudicate.

## Repo layout

```
/data/<book>/<chapter>.json     source of truth, one object per verse
/data/<book>/<chapter>.morph.txt   the project's own morphology of an LXX chapter
/data/<book>/<chapter>.words.json  word-by-word layer, generated by build/words.py
/build/render.py                data → HTML
/build/words.py                 /sources → the word-by-word layer
/build/validate.py              mechanical checks
/build/morph_diff.py            two independent passes at a chapter's morphology, compared
/templates/verse.html           the three-panel layout
/site/                          generated output — never hand-edit
/reference/lexicon-notes.md     recurring gloss-chains, kept consistent across books
/reference/second-pass-brief.md the brief for a chapter's independent second morphology pass
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
  "print": "Rahlfs 1935 (1950 printing), vol. I, p. 1",
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
  "reading": "[[in beginning|within, inside of, and by means of the first moment...|ἀρχή]], [[the God|he who is God definitively...|θεός]], ...",
  "names": []
}
```

`flag` is one of: `null`, `divergence`, `not in this text`, `name`, `variant`.

`reading` marks each unit as `[[headword|chain|lemma]]` and each proper name as
`[[name:…]]`. `build/render.py` derives both the unanchored and the anchored text from it,
so they cannot drift. Chains come from `/reference/lexicon-notes.md`.

The **lemma** is the Greek word the unit opens. It is never printed — it is there so the
checks can tell which word a unit renders instead of guessing from the English. Without it
the chain check could only see the units `/reference/lexicon-notes.md` happened to declare,
which is a third of them, and a chain that has drifted is exactly the chain the notes do
not declare. Where a preposition governs more than one case, the case goes with it —
`διά + genitive` — because Middle Liddell gives each case its own section and the sense
comes from there.

One unit may open more than one word, and then the field lists them: `ἐν; γῆ`. ἐν and ἀνά
take no unit of their own before a noun — the noun's unit swallows them and its chain
opens both — so naming only the noun left the preposition looking unopened to anything
counting words against units. Each item still carries its own case, `ἀνά + accusative`.
The count is checked as well as the name: two units may not open one word.

## Working rhythm

- One chapter per session. Commit per chapter with the reference as the message.
- Before writing a chapter, read /reference/lexicon-notes.md and reuse existing
  gloss-chains verbatim. If a recurring word has no entry, establish one and add
  it before continuing.. ἀρχή should read the same way in Gen 1:1 and John 1:1 —
  that consistency is what makes the quotation visible.
- For an Old Testament chapter, transcribe the Greek from the printed Rahlfs (see
  `/sources/README.md` for the scan) and cite each verse's page in `print`. Never copy it
  from `/sources` — those files are for checking only and may not be committed. Write the
  chapter's morphology in `data/<book>/<chapter>.morph.txt` as your own analysis — then a
  second time, by a separate agent briefed from `/reference/second-pass-brief.md` and never
  shown the first, and settle every disagreement `python build/morph_diff.py` reports
  before going on.
- After writing a chapter, append any newly-established gloss-chains to that file.
- Run `python build/words.py <BOOK>/<chapter>` to build the word-by-word layer from
  `/sources`, and skim the cards for lexicon scraps to add to its `NOT_SENSES`.
- Run `python build/validate.py` before committing.

## Validation

`build/validate.py` must check:
- every verse has greek, notes and reading, non-empty, with well-formed units
- every proper name in the Greek has a gloss on first occurrence in the chapter
- no banned imported phrases (maintain a list; seed it with "face of the waters")
- no headword stands bare — none written as plain text outside its unit
- a word is a unit exactly when its entry says more than its headword does, and a unit
  whose chain is word for word its headword is not a unit at all — checked both ways
  against the chapter's word-by-word layer, over nouns, verbs, adjectives, adverbs and
  prepositions, so neither half can happen by accident
- no headword stands bare — but two Greek words may head with the same English, μή and
  οὐ both giving *not*, so a plain word is only bare when nothing else in the verse is
  entitled to print it
- every unit names a Greek word its own verse holds, checked against the chapter's
  morphology, so the lemma is not an assertion nothing tests
- one word in one form reads one way: of two units sharing a lemma and a headword,
  neither says less than the other. Counting senses is not enough to see that — one
  dropped inside an and-joined gloss leaves the commas where they were
- one case is one chain: a preposition has one form, so its chain cannot follow the
  form; within one lemma and one case it reads the same everywhere
- the word-by-word layer, where there is one, still matches the verse's Greek
- the project's own morphology is well-formed by its code's own grammar
- that morphology agrees with itself across every chapter — a form keeps its dictionary
  form, a verb its parse, a noun its gender and number — unless the line says why
- the article stands where its word is: no plain *the* before a unit except ὁ δέ's, no
  *the the*, and over a participle the article's noun follows its gender — *one* for
  masculine and feminine, *thing* for neuter
- LSJ stands in only for a word Middle Liddell lacks under every close form of it — an
  LSJ entry for a word Middle Liddell has is a failure, since the table used to win
  outright and read ὦμος, μνημεῖον and ποιμήν from LSJ while Middle Liddell had them
- every first-sense Latin run in the lexicon is settled: Middle Liddell writes `Lat.
  <latin>, <English>` and Perseus wraps the whole run in one Latin element, so the
  English never reaches a translation. No check on the data can see it — a chain written
  from the entry's text is right — so this one reads the lexicon
- Greek text matches the source edition — New Testament character-for-character against
  SBLGNT; the Old Testament against the printed page every verse cites in `print`

Mechanical checks catch drift that reading won't.

## Scope order

Genesis and John first, then LXX Psalms. Poetry is where unanchored earns its keep.
