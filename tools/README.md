# Tools

The chapter pipeline and the edit-pass tools. Run them from the repository root, `python tools/<name>.py …`.
Their working files — transcriptions, drafts, second-pass replies, scan crops, reports, pickles — go in
`tools/work/` (`_paths.WORK`; set `EI_WORK` to put it elsewhere), which is not committed: nothing in it is a
source of truth. The data in `data/` is. Set `LXX_RAHLFS_DIR` to the local CCAT Rahlfs module for anything
that cross-checks the Old Testament (`sources/README.md`).

## A chapter

Each chapter is written in a file of its own, `tools/work/v<BOOK><CH>.py`, which `draftx.py` executes and
merges onto the chapter's skeleton:

- `K` — the units, by a short key: `C(field, head, pick)` takes the corpus's unit for a word and headword
  (`pick`, a piece of text, chooses between two chains); `u(head, chain, lemma)` writes a new one.
- `V` — each verse's reading, `{key}` standing for `K[key]`: `"and {said} [[name:Ιωσηφ]] …"`.
- `H` — each verse's hint; `N` — its notes, `[(lemma, flag, text)]`; `NAMES` — every name form,
  `form: (key, unanchored, anchored, gloss)`, the key shared by a name's forms so that it is glossed once in
  the chapter.

A verse already in the chapter file and not in `V` stays as it is.

### An Old Testament chapter (Rahlfs)

1. **Transcribe** from the printed page (`sources/README.md`): leaf *n* holds pp. 2(*n*−27) and +1; fetch
   `https://archive.org/download/<item>/page/n<NN>.jpg` into `tools/work/`, cut strips with `strips.py NN L|R y0 y1
   step`, and zoom on doubtful accents. Keep a misprint as printed. Write `work/<book><ch>.txt` (verse TAB page TAB
   Greek, `ʼ` U+02BC for elision, `87–88` for a verse across pages), `.speech` (verse TAB the capitals of direct
   speech inside the verse) and, where the module differs on a printed form, `.printed`.
2. `xbook.py brief BOOK CH` writes the second-pass brief from `reference/second-pass-brief.md`; give it to an
   agent that has not seen the first pass, its reply to `work/second<BOOK><CH>.txt`.
3. `xbook.py seed BOOK CH` drafts the morphology from the corpus; settle every `??` and `ALT` line in
   `work/fix<BOOK><CH>.py` (`F = {"v.n": "pos code lemma"}`), then `xbook.py first`, `xbook.py morph` (writes
   `data/<BOOK>/<CH>.morph.txt`) and `xbook.py skel` (the skeleton). Check every article's gender against its noun.
4. `python build/morph_diff.py data/<BOOK>/<CH>.morph.txt tools/work/second<BOOK><CH>.txt`, and settle every
   disagreement (MorphGNT's counts in `sources/morphgnt` and the corpus's tags are the precedent).
5. Add the chapter to `render.PAGE`; `python build/words.py BOOK/CH` lists the words with no lexicon senses.
6. **The lexicon**: `ml.py key` and `lsj.py key` print an entry, `fullx.py BOOK CH lemma …` each form's card,
   `headsx.py BOOK CH` the corpus's headwords for the chapter's words, `newlem.py BOOK CH` the words new to the
   page. Settle what a card needs in `build/words.py` — `LSJ` (and its row in `sources/README.md`), `SPELLING`,
   `NOT_SENSES`, `FORM_SENSES`, `MARKUP_LOST`, `GREEK_LOST`, `TEXT_LOST`, `PASSIVE_OF` — and each translation a
   chain leaves out, or a translation of some forms only, in the coverage tables (below).
7. Write `work/v<BOOK><CH>.py`; `draftx.py BOOK CH`; `python build/words.py BOOK/CH`; validate.
8. `modnotesx.py BOOK CH [--write]` writes the `# module …` notes on lines where the morphology differs from the
   module on purpose (`work/hand<BOOK><CH>.py`, `HAND` by `"v:w"` or form, where the corpus has no precedent).
9. Rebuild every layer, `python build/words.py`: a changed card can expose a defect in another chapter's chain.
10. Record the chapter's new words in `reference/lexicon-notes.md` and its questions in
    `reference/open-questions.md`; render, copy `site/index.html` to `reference/gold-standard.html`, validate,
    `python build/test_validate.py`, and commit with the reference as the message.

### A New Testament chapter (SBLGNT)

No transcription and no morphology: `xbook.py`'s skeleton takes the Greek from `sources/sblgnt/text`, verbatim,
SBLGNT's critical signs (⸀ ⸂…⸃ ⟦…⟧) included, and lists the speech capitals from MorphGNT (a capital whose
dictionary form is lower case). `words.nt_tokens` reads MorphGNT. Steps 5–7, 9 and 10 above apply; step 8 does
not. The verses MorphGNT does not analyse — John 7:53–8:11 — take the project's own morphology in
`data/JHN/<ch>.morph.txt`, written and checked as an Old Testament chapter's is (steps 2–4).

## The coverage tables

`COVERAGE_NOT` and `COVERAGE_ONLY` in `build/words.py` are generated, between `# BEGIN COVERAGE` and
`# END COVERAGE`, from the verdict files in `tools/decisions/` by `applydec.py [--write]`. Edit a verdict there,
never the block. Each row is one translation on one card: `NOT` (a label, a piece of an example, a phrase's,
Latin, a repeat — the reason the value), `FORM` (a sense of some forms only, its `code` a `FORMS` name) or `KEEP`.
The files are read in name order and a later hand-made file replaces an earlier verdict; `mkdec9.py` and
`mkdec10.py` are the readable sources of the two hand-made files. A chapter's new verdicts go in a new
`decisions/dec<…>.jsonl`.

## Reading and repairing chains across the corpus

- `allunits.py` pickles every unit with its form and card (`work/allunits.pkl`), each unit paired with the
  occurrence it opens as `validate.aligned_units` pairs it.
- `repair.py [--write]` brings chains to their cards: drops an item no translation gives, prints a voice's own
  sense in its own voice, renders an example's person or tense in the form, joins a run's pieces with the
  delimiter, renders a translation the chain lacks, and puts the perfect's formula after every item. It writes
  `work/fix35_report.txt`; read it before writing. On a new chapter's draft, a unit whose chain is its headword
  alone is a seed: it is expanded into the headword's own run, the headword's piece first, and only a seed has
  its pieces merged into one item — a settled chain's items are not merged.
- `siblings.py BOOK CH [--write]` reads a chapter's units against their siblings, the units elsewhere of one word,
  part of speech, voice and number on one card, which validate's range check holds to one count. A unit with
  fewer items than its fullest sibling is rebuilt in the sibling's order, each translation rendered in this
  unit's form (`work/siblings_report.txt`). Run it after `repair.py` on a new chapter, and on an old one the
  range check names.
- `cards.py LEMMA … | --top N` writes a review sheet, each card's translations with their verdicts and the
  entry's text (`work/review33.txt`).
- `rebuild.py` and `rebuild2.py` are the Q24 rebuild, kept for the renderer they hold (`rebuild.verb_item`,
  `render_all`) and `english.py`'s inflections; `repair.py` uses them. Do not run `rebuild2.py --write` on
  settled data.
- `dropq.py N …` deletes settled questions from `reference/open-questions.md`.

## Things learned

- A `FORM_SENSES` rule's skip set replaces `NOT_SENSES` for the word: union `NOT_SENSES[key]` into it.
- The article prints once where an adjective, numeral or possessive stands between it and its noun.
- Filing a scrap can expose old split runs elsewhere: rebuild every layer and validate.
- A name: reuse an earlier chapter's gloss, and check the bearer is the same.
- Never write a regex with `\b` through a shell heredoc: it can arrive as a backspace. Use a file.
- A chain's own *and* is not always a run's: `to and fro` is one English expression. The delimiter check once
  took it for `to turn to or from`'s pieces, and a mechanical pass cut it to `to / fro`; read a delimiter report
  against the entry before acting on it.
- A name's later occurrence in another case or under another capital takes a bare entry: Σίμων after Σίμωνος,
  ἀμὴν after Ἀμὴν. The names check reads them as one name.
