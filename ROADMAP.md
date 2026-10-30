# Roadmap

## Now

Genesis 48–50, a chapter a session, then John and the Septuagint Psalms, in the scope order
[CLAUDE.md](CLAUDE.md) sets.

## Planned: a Hebrew column

A session of its own. The Masoretic Hebrew, set beside the Greek as one more column the
reader can switch on and off, so that a reader who knows Hebrew can follow along.

### How it fits the page

The verse is already a row of toggleable columns: Anchored, Unanchored, Greek, Notes. Each is
an `<article class="panel" data-panel="…">` in `templates/verse.html` with a matching pill in
the controls bar of `templates/page.html`, and the grid takes its column count from the pills
that are on. The Hebrew is one more of each, `data-panel="hebrew"`, next to the Greek. Nothing
else in the layout changes.

It should start **off**. The Septuagint is the text here, and Hebrew–Greek divergences stay in
the notes and never enter the readings. The Hebrew column is a reference to follow along with,
not the text the Greek is to be read against.

### Source and licensing

| source | terms | use |
| --- | --- | --- |
| Westminster Leningrad Codex, as the [Open Scriptures Hebrew Bible](https://github.com/openscriptures/morphhb) distributes it | text public domain; OSHB's lemmas and morphology CC BY 4.0 | yes: compatible with the content licence |
| BHS, BHQ | Deutsche Bibelgesellschaft copyright | no |
| ETCBC BHSA | CC BY-NC 4.0 | no: non-commercial, incompatible with CC BY-SA |
| Westminster Hebrew Morphology (Groves Center) | non-commercial, no derivatives | no |

Check the OSHB repository's LICENSE file when fetching: an older copy of the data, on
eBible.org, lists its morphology as CC BY-SA 3.0.

The edition goes in `sources/` and is fetched rather than committed, like the Greek
editions, with its entry in `sources/README.md` and its attribution in `NOTICE.md`. Unlike the
Old Testament Greek, the Hebrew would be copied from the digital text, not transcribed. Its
being public domain allows that, and it can then be checked character for character, as John
is against the SBLGNT.

### The work

1. **The layer.** A script in `build/`, like `words.py`, writes each chapter's Hebrew to a
   committed file, `data/<BOOK>/<chapter>.hebrew.json`, so the site builds without `sources/`.
   `render.py` reads it into the new column.
2. **Versification.** The Greek and the Hebrew do not always number or order their verses
   alike, so the column needs a table per book mapping each Greek verse to its Hebrew verse or
   verses, or to none. Where the Greek has no Hebrew counterpart, or the Hebrew says it
   elsewhere, the column says so instead of standing empty.
   - Genesis is nearly verse for verse. The known exception is 47:5–6, where the Greek gives
     Pharaoh's two speeches in the other order and adds a sentence the Hebrew lacks. The rest
     are to be found by building the table.
   - Exodus 35–40 is ordered differently in the Greek.
   - The Psalms are numbered one behind the Hebrew for most of the book: Greek 9 is Hebrew
     9–10, and Greek 146–147 is Hebrew 147.
   - In Jeremiah, the oracles against the nations follow 25:13 in the Greek, and the Greek
     is about an eighth shorter.
   - Esther and Daniel carry Greek additions with no Hebrew at all.
3. **Display.** Set right to left, in a Hebrew font under an open licence such as Ezra SIL or
   Noto Serif Hebrew. Decide whether the cantillation marks are shown or only the vowel
   points.
4. **Validation.** Three checks:
   - the layer matches the source edition;
   - every verse of the table resolves;
   - a Greek verse with no Hebrew counterpart is marked as such, not left blank.

   `test_validate.py` breaks each of them once.
5. **Docs.** Update README.md, NOTICE.md and sources/README.md.

The alignment is by verse only. Aligning the two word by word is a separate and much larger
project.
