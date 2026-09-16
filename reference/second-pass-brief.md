# Second-pass brief

Every Old Testament chapter's morphology is written twice. The first pass is
`data/<BOOK>/<chapter>.morph.txt`. The second is made by a separate agent that sees only the
Greek and the conventions below — never the first — and `build/morph_diff.py` lists every
place the two disagree.

The second pass shares no memory with the first, so it catches slips of attention: a shifted
slot, a gender agreeing with the wrong noun, a case left over from the previous word. It does
not catch what both passes would get wrong for the same reason. That is what the reference
data is for when a disagreement is settled.

## Running it

1. Print the chapter's Greek and its word counts. The session runs this, not the agent —
   the chapter's JSON holds the notes, which contain analysis.

   ```bash
   python -c "import json,sys; sys.path.insert(0,'build'); import validate as V; sys.stdout.reconfigure(encoding='utf-8'); v=json.load(open('data/GEN/3.json',encoding='utf-8')); print(', '.join('%s %d' % (x['ref'].split()[1], len(V.PUNCT.sub('', x['greek']).split())) for x in v)); print(); [print(x['ref'].split()[1], x['greek']) for x in v]"
   ```

2. Give a **fresh** agent the brief below, with its placeholders filled. It has to be a
   separate agent: a session that wrote the first pass cannot make the second without
   remembering it.

3. Compare:

   ```bash
   python build/morph_diff.py data/GEN/3.morph.txt <the second pass>
   ```

4. Settle every disagreement in `data/<BOOK>/<chapter>.morph.txt` — never by editing the second
   pass to make the diff go quiet.
   - Where the question is **a convention** — a part of speech for a small word, a lemma's
     spelling — count what MorphGNT does in `sources/morphgnt/` rather than trusting either
     pass's memory of it. Genesis 2's ἐάν and ὅτε were both settled that way, in opposite
     directions.
   - Where it is **grammar**, the side that can say why wins, and a reason that disagrees with
     the reference module goes on the line as `# module …`.

5. A disagreement that traces back to this brief is a defect in the brief. Correct it here,
   so the next chapter's second pass does not repeat it.

### What it found in Genesis 2

Twelve disagreements over 531 words. The second pass was right three times — ὅτε and τε are
conjunctions, and Τίγρις is masculine — and wrong once, tagging the ἐάν of `ὃ ἐάν` as a
conjunction where MorphGNT tags that construction as a particle. The other eight came from
this brief: it told the second pass to give δύο no features, before MorphGNT was checked and
found to code δύο like any adjective. The brief below is corrected.

### What it found in Genesis 3

Six disagreements over 581 words, with the conventions for the chapter's new small words — ἰδού,
μήποτε, adverbial καί, ἀνὰ μέσον — added to the brief beforehand from MorphGNT counts. The
second pass was right four times: τοῦ at 3:2 goes with masculine παραδείσου, and αὐτοῦ at 3:3
(twice) and 3:5 resumes the fronted ἀπὸ καρποῦ, the fruit, not the tree — the reference module
reads all three the same way. It was wrong twice, and both trace to this brief: it had no rule
for τί ὅτι, and its rule for contracted nouns sent συκῆς to συκέα, where Middle Liddell and
MorphGNT both file συκῆ. Both rules are corrected below.

### What it found in Genesis 4

Three disagreements over 531 words, and the second pass was right all three times. ἐργᾷ at
4:12 is the contracted future of ἐργάζομαι, not a present — the reference module agreed.
σφυροκόπος at 4:22 is a second noun beside χαλκεύς, as the Hebrew has two. And ἑπτά closing
4:24 is an adverbial accusative, *seventy times seven*, not a nominative. None traced to this
brief; its names rule, extended beforehand with MorphGNT's spellings of the personal names
the New Testament shares, drew no disagreement at all.

## The brief

Copy everything below the rule into a new agent. Replace `<BOOK NAME>`, `<CHAPTER>`,
`<OUTPUT PATH>`, `<WORD COUNTS>`, `<TOTAL>` and `<THE TEXT>`.

---

You are doing an independent morphological analysis of Septuagint <BOOK NAME> <CHAPTER>
(Rahlfs 1935) — every word: its part of speech, parse, and dictionary form. Another analysis
of the same text already exists; yours will be diffed against it to find errors in either.
Your value comes entirely from being independent, so the rules about what not to open matter.

## Do not open or read

- anything under `data/`, `reference/`, `site/` or `sources/`
- anything the environment variable `LXX_RAHLFS_DIR` points at
- do not run anything in `build/`, and do not search the web for a parsed Septuagint

Work from your own knowledge of Greek grammar and the conventions below. The format examples
here are all you need.

## Output

Write the analysis to `<OUTPUT PATH>`, UTF-8, LF line endings. One line per word, in text
order, five space-separated columns:

    verse pos parse form lemma

e.g. `2:1 V- 3API-P-- συνετελέσθησαν συντελέω`. No header, no comments, no blank lines. Copy
each form exactly as the text prints it with punctuation (`. , · ; : —`) removed; keep accents
as printed (a grave stays grave), keep capitals, and keep the elision mark ʼ (U+02BC).

Words per verse: <WORD COUNTS>. There must be <TOTAL> lines. Check your counts before
finishing.

## Part of speech (column 2)

N- noun · V- verb · A- adjective (numerals included) · RA article · RP personal pronoun
(αὐτός and the reflexive ἑαυτοῦ included) · RD demonstrative · RR relative pronoun · RI
interrogative · P- preposition · C- conjunction · D- adverb · X- particle · I- interjection

Small words are tagged as MorphGNT tags them:

- **C-** καί, δέ, γάρ, ὅτι, τε, ἵνα; ἐάν meaning *if*; ὅτε introducing a clause, including
  after a noun that is not a time (`ἡ μαρτυρία … ὅτε`, John 1:19); οὐδέ meaning *nor*; μήποτε
  meaning *lest*; ὡς meaning *as, like*
- **X-** ἄν; ἐάν where it stands for ἄν after a relative (`ὃ ἐὰν θέλητε`, John 15:7); ἰδού;
  μή opening a question that expects *no*
- **D-** οὐ, μή, νῦν, ἔτι, ἐκεῖ, ἐκεῖθεν, ποῦ; καί meaning *also, even*; οὐδέ meaning *not
  even*; ὅτε after a noun of time (`ἔρχεται ὥρα ὅτε`, John 4:21); οὗ meaning *where*
- **P-** a word governing a genitive as a preposition does — ἐπάνω, ἀπέναντι, ἀνά — and ἕως
  governing a genitive, an articular infinitive included

## Parse (column 3) — exactly 8 characters

Positions: person, tense, voice, mood, case, number, gender, degree. Use `-` where a position
does not apply.

- person `1 2 3` · tense `P` present `I` imperfect `F` future `A` aorist `X` perfect `Y`
  pluperfect · voice `A` active `M` middle `P` passive `E` middle/passive · mood `I`
  indicative `S` subjunctive `O` optative `D` imperative `N` infinitive `P` participle · case
  `N G D A V` · number `S P D` · gender `M F N C` · degree `C` comparative `S` superlative

Shape by type:

- finite verb: person, tense, voice, mood, number — no case, no gender. `3AAI-S--`
- infinitive: tense, voice, mood N — nothing else. `-AAN----`
- participle: tense, voice, mood P, **and** case, number, gender. `-PAPNSM-`
- noun: case and number, and gender (see indeclinables). `----NSF-`
- article, adjective, demonstrative, relative: case, number, gender. `----DSM-`
- personal pronoun, interrogative: case and number, and gender where the form has one
  (μου has none: `----GS--`)
- preposition, conjunction, adverb, particle: `--------`

Conventions:

- **Voice E** only in the tenses where middle and passive share one form — present,
  imperfect, perfect, pluperfect — deponents included. Aorist and future distinguish the two,
  so use M or P there.
- **Gender C** for an adjective whose form does not distinguish masculine from feminine:
  two-termination adjectives (ἀόρατος, πράσινος) and numerals like τέσσαρας.
- **Indeclinables** take case and number from the syntax, as MorphGNT does, and gender where
  there is one to take: a personal name, from the person (Αδαμ `----DSM-`, a woman's name
  `F`), or a numeral agreeing with its noun (οἱ δύο `----NPM-`, as MorphGNT codes δύο at
  John 1:35). An indeclinable place name has none (Εδεμ `----DS--`). A declinable Greek name keeps its gender like any noun — rivers
  are masculine (Τίγρις, Εὐφράτης).
- An indeclinable common noun takes its gender from the article or adjective beside it.
- An article before an indeclinable name still carries full case, number and gender.
- μέσος with a genitive after it — `ἐν μέσῳ τοῦ …`, `ἀνὰ μέσον τοῦ …` — is the neuter
  adjective used as a noun: `A- ----DSN-`, `A- ----ASN-`.
- A word of address is vocative, case `V`.
- τί in `τί ὅτι`, *why is it that*, is accusative, `RI ----ASN-`, as MorphGNT codes it all
  three times (Luke 2:49; Acts 5:4, 5:9).
- `ἵνα τί`, *why*, printed as two words, is the ellipsis ἵνα τί γένηται: ἵνα `C-`, τί
  `RI ----NSN-`. (MorphGNT prints the pair as one word, ἱνατί, and so cannot guide it.)
- `ὁ δέ`, *and he*, is still the article: `RA ----NSM-`, as MorphGNT codes it.
- Numerals take case, number and gender like any adjective — ἑπτά `A- ----APN-` beside a
  neuter plural — and a multiplicative adverb (ἑπτάκις) is `D-`.
- Comparatives in -ων (μείζων) have one form for masculine and feminine: gender `C`, degree `C`.
- οἶδα's past forms (ᾔδει) are pluperfect, `Y`, as MorphGNT codes them.
- Where the form is ambiguous, case, number and gender come from the syntax: neuters in the
  nominative and accusative, verbless clauses, agreement with a noun, a hanging nominative.

## Lemma (column 5)

The dictionary form as Middle Liddell (Perseus) files it:

- Koine spellings: γίνομαι, γινώσκω. No iota subscript where Perseus has none: ἀποθνήσκω.
  Enclitics unaccented: τε.
- Verbs with no active in use under their middle form, as MorphGNT files them: ἐργάζομαι,
  πορεύομαι, ἐκπορεύομαι, ἐντέλλομαι, φοβέομαι, ἀπέρχομαι.
- εἰδέναι → οἶδα · εἶπεν → λέγω · ἰδεῖν → ὁράω · φαγ- forms → ἐσθίω · μου → ἐγώ ·
  every article → ὁ.
- A contracted form goes under whichever spelling Middle Liddell heads the entry with — the
  uncontracted ὀστέον for ὀστοῦν, but the contracted συκῆ for συκῆς, as MorphGNT has it.
  ἕνεκεν → ἕνεκα. A neuter noun filed as such: πετεινόν.
- Proper names: a personal name the New Testament also uses takes MorphGNT's dictionary form,
  accented though Rahlfs prints it bare — Ἀδάμ, Εὕα, Κάϊν, Ἅβελ, Σήθ, Ἐνώς, Ἑνώχ,
  Μαθουσαλά, Λάμεχ so far. Every other Semitic name, of a person or a place, exactly as
  printed, unaccented (Εδεμ, Φισων, Ναιδ). Greek names in the nominative singular (Αἰθιοπία,
  Τίγρις, Ἀσσύριος, Εὐφράτης). A Greek word the text prints capitalised as a name keeps its
  capital in the lemma.
- Any other Semitic word printed unaccented: exactly as printed, like the place names.

## The text

<THE TEXT>

## When you finish

Verify the line count and the per-verse counts. Then reply briefly: the line count, and at
most ten words you found genuinely ambiguous, with how you decided each. Do not compare your
work against anything.
