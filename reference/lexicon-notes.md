# Lexicon notes — headwords and gloss-chains

Seeded from GEN 1:1–2, JHN 1:1–2 and JHN 1:6.

**These strings are copied verbatim into new chapters.** ἀρχή must read the same way in
Gen 1:1 and John 1:1 — that consistency is what makes the quotation visible on the page.
If a chain or headword has to change, change it here first and re-render every chapter that
uses it.

## How an entry is used

Each entry gives a **headword** and a **chain**. In a verse's `reading` they are one unit:

    [[headword|chain]]

The unanchored panel shows the chain alone; the anchored panel shows `headword — chain —`,
shaded. There is one chain per entry, not one per panel.

### The headword rule

The headword is **the lexicon's first sense, in the form the text uses**. No translation is
consulted.

1. **Lexicon.** Middle Liddell (1889), as the Perseus Digital Library encodes it, in
   `sources/middle-liddell/`. Where it has no entry, LSJ as published by PerseusDL
   (CC BY-SA 4.0).
2. **Sense.** The first translation in the entry's first numbered sense. The headword line,
   principal parts and etymology stand before the senses and are never taken. For a
   preposition, the first sense for the case it governs. For a word used as a noun, the
   first noun sense.

   Where Perseus's opening gloss belongs to one voice only — ἄρχω's *in pass. sense:— to be
   first*, against its numbered I, *to begin, make a beginning* ("both in Act. and Mid.") —
   it is skipped **by name** in `NOT_SENSES`. Not by rule: the same opening position carries
   the principal sense in most entries, λόγος's *the word* among them, and a rule that
   skipped it would rewrite the prologue's headword to *spoken*.

   The same holds for a sense restricted to a *form* rather than a voice. ἐνδύω's sense I,
   *to go into, put on*, is dressing oneself; the entry marks sense II "Causal … aor1
   -έδυσα", and GEN 3:21 ἐνέδυσεν is that aorist, so sense I is skipped by name. And one
   entry can hold two words: ὡς's opens with the accented demonstrative ὥς, *so, thus*,
   before the relative ὡς, *as*, which is the word Rahlfs prints.

   A word used as a conjunction takes the first conjunction sense, as a word used as a noun
   takes the first noun sense: ἵνα is an adverb of place in its first sense and *that, in
   order that* in its second; μήποτε is *never* as an adverb and *that at no time, lest
   ever* as a conjunction.

   A sense the entry restricts to one *tense* is skipped the same way: ἀνίστημι heads its
   causal senses "in pres., imperf." and its intransitive ones "in aor2 ἀνέστην", so GEN 4:8
   ἀνέστη is *stood up*. A sense restricted only by *subject* or *construction* is not: the
   rule reads the lexicon, not the verse. So συλλαμβάνω is *having collected* at GEN 4:1,
   though its fourth sense, "of females, to conceive", is what the verse means; ἄρχω with the
   genitive is *will begin* at 4:7, though *to rule* is its second sense; and πρόβατον is
   *anything that walks forward*, which Middle Liddell gives as the word's proper sense before
   *cattle, flocks* and, in Attic, *sheep*. The chain carries the rest, and the notes say
   where the verse's meaning stands in the entry.
3. **Form.** Tense, voice, mood, person and number come from the Greek form.
4. **Article.** English gets *the* where the Greek has the article, and nothing where it
   does not. The *a* in a lexicon's gloss (*a beginning*) is its citation form, not the text's.
5. **Capitals.** None the Greek does not mark. Proper names and *God* are capitalised, as
   the lexicon prints them; nothing is capitalised to make it a title, and no pronoun
   standing for God takes a reverential capital.

### Homographs

Where the lexicon prints two entries under one spelling, the first is not always the word
the text uses, and "the first sense of the first entry" would then be the first sense of the
wrong word. `ENTRY` in `build/words.py` names which entry is meant; it decides nothing about
what the word means, only which entry is the word, and every case is listed here:

| lemma | entry taken | why not the first |
| --- | --- | --- |
| χοῦς (GEN 2:7) | `xou=s2` — *earth thrown down, heaped up, dust* | `xou=s1` is the Pitcher-feast, the liquid measure |
| ὅτι (GEN 2:3) | `o(/ti2` — *that* | `o(/ti1` is ὅ τι, *for what, wherefore* |
| λέγω (GEN 2:16) | `le/gw3` — *to say, speak* | `le/gw1` is *to lull to sleep*, `le/gw2` *to gather* |
| οὐ (GEN 2:5) | `ou)8` — *not* | the other seventeen gloss idioms, οὐ γάρ, οὐ μήν … |
| ὁδός (GEN 3:24) | `o(do/s2` — *a way, path* | `o(do/s1` is the Attic ὀδός for οὐδός, *a threshold* |

A lemma belongs there only where the entries are genuinely different words. A word with one
entry and several senses is not a homograph: its first numbered sense stands, however far
from the expected meaning it reads.

### Where the lexicon files a word elsewhere

`SPELLING` in `build/words.py` redirects a lemma to the key its entry actually sits under.
Three reasons, and all of them are the lexicon's filing rather than a decision about sense:

| lemma | filed under | why |
| --- | --- | --- |
| γίνομαι, γινώσκω | γίγνομαι, γιγνώσκω | the Attic spelling of a Koine form |
| εἷς (GEN 2:11) | `ei(/s` | Perseus keys the numeral with an acute, not a circumflex |
| πορεύομαι (GEN 2:14) | πορεύω | a deponent, filed under its active |
| ἐκπορεύομαι (GEN 2:10) | ἐκπορεύω | likewise |
| κατέναντι (GEN 2:14) | κατεναντίον | the entry is a bare cross-reference, `= κατεναντίον`, and glosses nothing itself |
| φοβέομαι (GEN 3:10) | φοβέω | MorphGNT's middle, filed under the active |
| ἔχθρα (GEN 3:15) | ἔχθρη | the entry is headed with the Ionic spelling |
| δειλινός (GEN 3:8) | δειελινός | a cross-reference, *contr. for δειελινός* |
| ὀρθῶς (GEN 4:7) | ὀρθός | the adverb, filed inside the adjective's entry |

Where Middle Liddell has no entry a word can be found under, LSJ supplies the senses (`LSJ` in
`build/words.py`): σύ, φλόγινος (GEN 3); ποιμήν — Middle Liddell has only the Doric ποιμάν,
*doric for ποιμήν*, pointing at an entry it lacks — ψαλτήριον, μώλωψ and ἑβδομηκοντάκις
(GEN 4). One word is in neither: σφυροκόπος (GEN 4:22), for which LSJ has only the verb
σφυροκοπέω. With no lexicon sense to head it, it stands as plain text, *a hammer-beater*, and
the note says why.

The last is the same shape as ἁγιάζω in LSJ (`= ἁγίζω`): an entry that exists, carries no
translation, and names the entry that does. Following it is not interpretation — the lexicon
is saying where the word is defined.

Where a deponent is filed under its active, the entry's opening gloss is usually the active
one and the form in the text is not. That is the ἄρχω and βρέχω situation again, and it is
settled the same way: by name, per lemma, with the entry's own voice labels quoted.

Each entry below records the lexicon sense its headword came from.

### The chain rules

- **A chain is the whole range.** Lexical range, plus aspect where the aspect belongs to the
  word itself. The headword may repeat inside it — it is the chain's first sense.
- **No filler and no commentary.** A point *about* the text — that John is quoting Genesis,
  that ἐγένετο is the verb withheld from the Logos — goes in the notes.
- **The headword never stands bare** in the unanchored panel, as plain text outside its unit.
- **No em dashes inside a chain.** Em dashes delimit chains in the anchored panel.
- **Words with no chain are plain text**, identical in both panels: ὕδωρ (*the water*), a
  supplied copula, ἦν's aspect expansion, ἐπάνω.
- **short** marks the reduced form used when a word is restated rather than introduced.
  John 1:2 restates John 1:1 and takes the short forms.
- **No reverential capitals.** A pronoun standing for God is lowercase — *he who is God
  definitively, the one the article marks out*, *facing him*. The manuscripts have no lower
  case, so the capital is always the editor's. *God* itself keeps its capital, as the lexicon
  prints it.

---

## Prepositions and particles

### ἐν (with ἀρχή)

Not its own unit so far: ἐν ἀρχῇ is one unit, and ἐν's chain opens the ἀρχή chain (see
ἀρχή). Middle Liddell's first sense: *in, among* (with the dative) → *in*.

- **link:** `within, inside of, and by means of`
- **used:** GEN 1:1, JHN 1:1, JHN 1:2

Locative, instrumental, and sphere-of-operation senses are all live and none is chosen.
Fixed; it does not reduce in restatement.

### πρός + accusative

- **headword:** `towards the God` — Middle Liddell's accusative block opens at its 53rd sense
  group, *towards, to*; the static *with* first appears at the 66th. τὸν θεόν is articular.
- **chain (full):** `toward the God, facing him, oriented to him, in living motion and address toward him, held face to face in a nearness that never collapses into sameness`
- **short:** `facing, oriented toward, and in living address toward the God`
- **used:** JHN 1:1 (full), JHN 1:2 (short)

Directional, never static. Note in the apparatus wherever παρά / μετά / σύν were available
and not used. The lexicon rule removes *with* from the headword as well as the chain.

### παρά + genitive

- **headword:** `from the side of God` — Middle Liddell, first sense with the genitive: *from
  the side of*. θεοῦ is anarthrous.
- **chain:** `from alongside and from the side of God`
- **used:** JHN 1:6

### δέ

- **headword:** `but` — Middle Liddell, first sense.
- **chain:** `but, however, whereas, on the other hand`
- **used:** GEN 1:2

Soft adversative. Never rendered with the force of ἀλλά.

### ἐπάνω — plain text

`upon, over, and atop` (full) / `over and atop` (short). No unit. GEN 1:2, twice: full at the
abyss, short at the water.

### ἀπό + genitive

- **headword:** `from` — Middle Liddell, first sense with the genitive: *from, away from*.
- **chain:** `from, away from, far from, apart from`
- **used:** GEN 2:2, GEN 2:3

Separation, not source. Resting ἀπὸ τῶν ἔργων is a standing apart *from* the works.

### ὅτι

- **headword:** `that` — the conjunction; the lexicon prints two entries under this
  spelling and this is the second (see *Homographs* above). First sense *that*.
- **chain:** `that, seeing that, although, for that, because, inasmuch as`
- **used:** GEN 2:3

Both the *that* of reported speech and the *because* the sense wants; neither is chosen.

### ὅτε

- **headword:** `when` — Middle Liddell, first sense.
- **chain:** `when, sometimes`
- **used:** GEN 2:4

### Ordinals — plain text

`the sixth`, `the seventh`. No unit: Middle Liddell gives ἕκτος one sense, *sixth*, and
ἕβδομος *seventh*, so there is no range to open and a unit would only repeat the headword.
GEN 2:2, GEN 2:3.

### πρό + genitive

- **headword:** `before` — Middle Liddell, first sense *before*.
- **chain:** `before, in front of, further on, sooner, rather than`
- **used:** GEN 2:5, twice, both with the articular infinitive (πρὸ τοῦ γενέσθαι, πρὸ τοῦ
  ἀνατεῖλαι)

### ἐπί

- **headword:** `upon` — Middle Liddell, first sense *on, upon*.
- **chain:** `upon, on, in, at, near`
- **used:** GEN 2:5, twice — with the genitive (ἐπὶ τῆς γῆς) and with the accusative
  (ἐπὶ τὴν γῆν)

The entry opens with one heading for all three cases, and its tagged translations do not
separate them, so the case cannot be read off the lexicon the way it can for πρός and παρά.
One chain serves both, and the case is recorded here rather than guessed at in the text.

### ἐκ + genitive

- **headword:** `out of` — Middle Liddell, first sense *out of, from*.
- **chain:** `out of, forth from, from`
- **used:** GEN 2:6

### εἰς + accusative

- **headword:** `into` — Middle Liddell, first sense *into, to*.
- **chain:** `into, to, in, rest in`
- **used:** GEN 2:7, twice — of place (εἰς τὸ πρόσωπον) and of result (εἰς ψυχὴν ζῶσαν);
  GEN 2:9, twice; GEN 2:10

### ἐν — joined to its object

ἐν is never a unit by itself. It joins its object, as in ἐν ἀρχῇ:

- **ἐν μέσῳ** (GEN 2:9) — **headword** `in middle`; **chain** `within, inside of, and by
  means of the middle, in the middle, the centre, mid, between two`.
- **ἐν Εδεμ** (GEN 2:8) — the object is a proper name, which carries its own marker, so
  ἐν stands as plain text `in` and opens no chain.

A one-word anchor `in` is unusable in any case: `validate.py` would find it inside the fixed
aorist formula, *not a process observed in progress*, and refuse it as a bare headword.

### κατά

- **headword:** `down` — Middle Liddell, first sense *down, downwards*.
- **chain:** `down, downwards, down from, down upon, over, upon`
- **used:** GEN 2:8

Like ἐπί, the entry heads all its cases together and its tagged translations do not separate
them. κατὰ ἀνατολάς is the idiom *eastward*, which the first sense does not give; the note
records the idiom and the reading prints the lexicon.

### Adverbs of place — ἐκεῖ, ἐκεῖθεν

- ἐκεῖ — **headword** `there`; **chain** `there, in that place`. GEN 2:8, 2:11, 2:12.
- ἐκεῖθεν — **headword** `from that place`; **chain** `from that place, thence, thereafter,
  next`. GEN 2:10.

### ἔτι

- **headword:** `yet` — Middle Liddell, first sense *yet, as yet, still*.
- **chain:** `yet, as yet, still, further, besides, moreover`
- **used:** GEN 2:9

### κατέναντι

- **headword:** `over against` — the entry carries no translation of its own, reading
  `κατέναντι = κατεναντίον`; the senses are that entry's, *over against, opposite, before*.
- **chain:** `over against, opposite, before`
- **used:** GEN 2:14

### Ordinals, continued — plain text

`the second`, `the third`, `the fourth` (GEN 2:13, 2:14) and `four` (τέσσαρες, GEN 2:10), on
the same ground as `the sixth` and `the seventh`: one sense each, so no range to open.

### ἵνα

- **headword:** `that` — used as a conjunction, so the first conjunction sense, *that, in
  order that*; the entry's first sense is the adverb of place, *there, where*.
- **chain:** `that, in order that`
- **used:** GEN 3:3 (ἵνα μή, with `not` as plain text)

### οὐδέ

- **headword:** `but not` — Middle Liddell, first sense, *but not*, answering to μέν.
- **chain:** `but not, and not, nor, not even, not at all`
- **used:** GEN 3:3

### μήποτε

- **headword:** `that at no time` — used as a conjunction, so sense II, *that at no time,
  lest ever*; sense I is the adverb, *never, on no account*.
- **chain:** `that at no time, lest ever, never, on no account, perhaps`
- **used:** GEN 3:22

### ὡς

- **headword:** `as` — the relative, sense A.II. The entry opens with the accented
  demonstrative ὥς, *so, thus*, a different word, and those glosses are skipped by name.
- **chain:** `as, according as, considering, like`
- **used:** GEN 3:5, GEN 3:22

### ἕως + genitive

- **headword:** `until` — Middle Liddell, first sense *until, till*. The entry itself cites
  ἕως with the articular infinitive, ἕως τοῦ ἀποτῖσαι, the construction of GEN 3:19.
- **chain:** `until, till, while, so long as`
- **used:** GEN 3:19

### ἀνά — joined to its object

- **ἀνὰ μέσον** (GEN 3:15, four times) — **headword** `up to middle`; **chain** `up to, up
  along, and throughout the middle, in the middle, the centre, mid, between two`. ἀνά with
  the accusative: the entry describes that case as *motion upwards*, which glosses nothing and
  is skipped by name, and its first translation is *up to, up along*. The pair is the idiom
  *between*, recorded in the verse's note, as κατὰ ἀνατολάς was.

### μετά + genitive

- **headword:** `in the midst of` — Middle Liddell, first sense with the genitive, *in the
  midst of, among*; *along with* is the second and *with* the third. Perseus's opening
  summary, *in the midst of, among with gen., dat., and acc.*, is skipped by name.
- **chain:** `in the midst of, among, in common, along with, with, by means of`
- **used:** GEN 3:6, GEN 3:12, with the pronoun as plain text

### ἀπέναντι

- **headword:** `opposite` — Middle Liddell, one sense, *opposite, against*, c. gen.
- **chain:** `opposite, against`
- **used:** GEN 3:24

### ποῦ

- **headword:** `where` — *where?* first; *how? by what right?* second.
- **chain:** `where, at what point, how, by what right`
- **used:** GEN 3:9

### ἰδού

- **headword:** `lo` — Middle Liddell, first sense *lo! behold! see there!*
- **chain:** `lo, behold, see there`
- **used:** GEN 3:22

### Plain text — small words and single senses

- μή — `not`, like οὐ; οὐ μή — `no, not` (GEN 3:1).
- τί in τί ὅτι and τί τοῦτο — `why` (GEN 3:1, 3:13).
- καί as *also* — `also` (GEN 3:6).
- ἑαυτοῖς — `for themselves` (GEN 3:7).
- ἐπικατάρατος — `yet more accursed`: Middle Liddell's one sense (GEN 3:14, 3:17, 4:11).
- τὸ δειλινόν — `at evening`: filed under δειελινός, one sense (GEN 3:8).
- One sense each in GEN 4, so plain text: πρωτότοκος `the first-born` (4:4), περίλυπος `deeply
  grieved` (4:6), σήμερον `to-day` (4:14), ἑπτά `seven` and ἑπτάκις `seven times` (4:15, 4:24),
  ἑβδομηκοντάκις `seventy times` (4:24, LSJ), ἀδελφή `sister` (4:22), νεανίσκος `a youth` and
  ἐνωτίζομαι `hearken to` (4:23), υἱός `son` (4:17, 4:25, 4:26 — Middle Liddell's *A son* and *a
  son* are one sense).
- σφυροκόπος — `a hammer-beater`: in no lexicon here (4:22).
- εἰ, ἐάν — `if`; τί in ἵνα τί — `what` (4:6); ἐν τῷ εἶναι — `in the being of` (4:8).
- εἰμί with a participle (ἦν ἐργαζόμενος, 4:2; ἦν οἰκοδομῶν, 4:17) — `was, and kept on being,`
  before the participle's unit, the imperfect formula of 2:5 in short.

### διά + genitive

- **headword:** `through` — Middle Liddell, with the genitive, *in a line, through, right
  through*; Perseus's opening summary is skipped by name.
- **chain:** `through, right through, by means of, by the agency of`
- **used:** GEN 4:1 (διὰ τοῦ θεοῦ)

### μετά + accusative

- **headword:** `into the middle of` — the first translation for the accusative; *after*, of
  time, comes later.
- **chain:** `into the middle of, coming among, in pursuit and quest of, after`
- **used:** GEN 4:3 (μεθʼ ἡμέρας)

### ὀρθῶς, οὕτως, λίαν

- ὀρθῶς — **headword** `straight`; **chain** `straight, uprightly, rightly, truly and
  correctly, justly`. The adverb of ὀρθός, whose first sense is *straight*. GEN 4:7.
- οὕτως — **headword** `in this way`; **chain** `in this way, in this manner, so, thus, even so,
  so much`. GEN 4:15.
- λίαν — **headword** `very`; **chain** `very, exceedingly, very much, overmuch`. GEN 4:5.

---

## Divine designations

### ὁ θεός — articular

- **headword:** `the God` — Middle Liddell, first sense *God*; articular, so *the*.
- **chain:** `he who is God definitively, the one the article marks out, the known and the only`
- **used:** GEN 1:1

Lowercase pronouns; the notes say why (GEN 1:1, *Capitals*).

### θεός — anarthrous, qualitative predicate

- **headword:** `the word was God` — the whole clause θεὸς ἦν ὁ λόγος: λόγος *the word*
  (articular), εἰμί *was* (imperfect), θεός *God* (anarthrous); English subject first.
- **chain:** `everything that God is by nature, deity in full and undiminished kind, was what that utterance was`
- **used:** JHN 1:1

The fronted anarthrous predicate restructures the clause, so the unit is the clause. The
chain must say what the subject is *by nature* without asserting identity of person and
without indefiniteness. Flag the fronting in the notes every time it occurs.

### θεοῦ — anarthrous genitive

- **headword:** `of God` — genitive; Middle Liddell *God*; anarthrous.
- **chain:** `God's own, divine in character`
- **used:** GEN 1:2 (πνεῦμα θεοῦ — its own unit, after πνεῦμα)

### τὸν θεόν — accusative under πρός

Rendered `the God` in the πρός headword and chain. The article is carried into English
against normal usage, because John 1:1c turns on articular τὸν θεόν against anarthrous θεός.

### κυρίου τοῦ θεοῦ — genitive

- `of lord` / `of lord, of master, of the one having power and authority over`
- `of the God` / `of him who is God definitively, of the one the article marks out, of the known and the only`
- **used:** GEN 3:8, twice

The nominative chains, in the genitive.

### θεοί — plural, anarthrous

- **headword:** `gods` — Middle Liddell's first sense is *God*; its second, *a god*, is the
  one a plural can take, lower case as the lexicon prints it.
- **chain:** `gods, the gods, goddesses`
- **used:** GEN 3:5 (ὡς θεοί)

---

## Verbs

### εἰμί — imperfect ἦν — plain text

No unit: the expansion *is* "was", expanded. It reads identically in both panels. Two settled
forms, not interchangeable:

- **state of a creature** (GEN 1:2): `was, and kept on being as a standing and continuing condition and not a momentary one`
- **pre-existence, against ἐγένετο** (JHN 1:1a): `there was, and was continuously, and was already in unbroken existence without any point of having come to be`
  - JHN 1:1b, before πρός: `was and remained`
  - **short** (JHN 1:2): `was — continuously, and without any point of having come to be —`

The second form is required anywhere the ἦν / ἐγένετο contrast is in play. Never flatten
either to *was*.

### γίνομαι — aorist ἐγένετο

- **headword:** `came into being` — Middle Liddell (filed under Attic γίγνομαι), sense I:
  *Radical sense, to come into being*; aorist middle, 3rd singular. No *there*: the Greek has
  none.
- **chain:** `there came to be, there arose, there was brought into existence`
- **used:** JHN 1:6

The verb withheld from the Logos in JHN 1:1–2. Wherever it stands against ἦν in the same
context, say so in the notes.

### ποιέω — aorist

- **headword:** `made` — Middle Liddell, first sense *to make*; aorist active, 3rd singular.
- **chain:** `fashioned, wrought, manufactured, produced, performed, and brought to a finished and accomplished state`
- **used:** GEN 1:1

Followed by the aorist formula as **plain text**: `— one completed act seen whole, not a
process observed in progress —`. The formula is grammar, not definition, so it sits outside
the chain.

### ἐπιφέρω — imperfect middle/passive

- **headword:** `was being brought upon` — Middle Liddell's first sense is *to bring, put, or
  lay upon*, which Perseus's markup splits into separate translations (*to bring, put* ·
  *lay upon*). Imperfect middle/passive, 3rd singular — one form in this tense — read passive, as
  the note reads it (*to be borne upon*).
- **chain:** `was being borne along, carried over, swept upon, brought continuously to bear`
- **used:** GEN 1:2

### ἀποστέλλω — perfect passive participle

- **headword:** `sent off` — Middle Liddell, first sense *to send off*; perfect passive participle.
- **chain:** `one sent off, dispatched, and commissioned on another's authority`
- **used:** JHN 1:6

Perfect — a standing status, not a past errand.

### συντελέω — aorist

- **headword:** `were brought quite to an end` (aorist passive, 3rd plural, GEN 2:1) /
  `brought quite to an end` (aorist active, 3rd singular, GEN 2:2) — Middle Liddell, first
  sense *to bring quite to an end, complete, accomplish*.
- **chain (passive):** `were brought quite to an end, were completed, were accomplished, were made up into the whole and into the number`
- **chain (active):** `brought quite to an end, completed, accomplished, made up into the whole and into the number`
- **used:** GEN 2:1, GEN 2:2

The *make up the whole* / *make up the number* senses are the lexicon's second and third and
stay in the chain: finishing here is also completing a count.

### καταπαύω — aorist

- **headword:** `laid to rest` — Middle Liddell, first sense *to lay to rest, put an end to*;
  aorist active, 3rd singular.
- **chain (full):** `laid to rest, put an end to, made to cease, stopped and kept in check, put down`
- **short:** `laid to rest, put an end to, made to cease`
- **used:** GEN 2:2 (full), GEN 2:3 (short)

Transitive in the lexicon's first sense, where English *rested* is intransitive. The range
runs as far as *kill*, which the chain does not carry; the note says so instead.

### εὐλογέω — aorist

- **headword:** `spoke well of` — Middle Liddell, first sense *to speak well of, praise,
  honour*; aorist active, 3rd singular. Rahlfs prints the augment ηὐ-.
- **chain:** `spoke well of, praised, honoured, blessed`
- **used:** GEN 2:3

*Blessed* is the entry's fourth gloss and comes last in the chain for that reason.

### ἁγιάζω — aorist

- **headword:** `hallowed` — no Middle Liddell entry; LSJ gives the word no gloss of its own
  either, reading `= ἁγίζω` and citing this verse, so the sense is ἁγίζω's, *hallow, make
  sacred*. Aorist active, 3rd singular.
- **chain:** `hallowed, made sacred`
- **used:** GEN 2:3

### ἄρχω — aorist middle

- **headword:** `began` — Middle Liddell's first *numbered* sense, *to begin, make a
  beginning*, marked "both in Act. and Mid."; aorist middle, 3rd singular. Perseus's opening
  gloss *in pass. sense:— to be first* belongs to the passive alone and is skipped by name in
  `NOT_SENSES` (see the headword rule above).
- **chain:** `began, made a beginning, made a beginning of, began from`
- **used:** GEN 2:3

### ποιέω — aorist infinitive

- **headword:** `to make` — the same entry as the indicative above, in the infinitive.
- **chain:** `to make, to do, to produce, to create`
- **used:** GEN 2:3 (ποιῆσαι, after ἤρξατο)

### γίνομαι — aorist infinitive

- **headword:** `to come into being` — the same entry as the indicative, in the infinitive.
- **chain:** `to come to be, to arise, to be brought into existence`
- **used:** GEN 2:5 (γενέσθαι, under πρὸ τοῦ)

### ἀνατέλλω — aorist infinitive

- **headword:** `to make to rise up` — Middle Liddell, first sense *to make to rise up*.
- **chain:** `to make to rise up, to grow up, to give birth to and bring to light, to rise, to take its rise, to grow`
- **used:** GEN 2:5 (ἀνατεῖλαι, under πρὸ τοῦ)

Transitive first, intransitive later, and the LXX uses it intransitively of the plant.

### βρέχω — aorist

- **headword:** `rained` — Middle Liddell's second sense, *to rain, send rain*, which the
  entry marks as New Testament usage. Every translation Perseus tags in the first sense
  stands inside that sense's `:—Pass.` clause, and its active gloss (*to wet*, Lat. *rigo*)
  is never tagged at all, so the passive glosses are skipped by name in `NOT_SENSES` — the
  same treatment as ἄρχω, for the same reason. Aorist active, 3rd singular.
- **chain:** `rained, sent rain`
- **used:** GEN 2:5

### ἐργάζομαι — present infinitive

- **headword:** `to work` — Middle Liddell, first sense *to work, labour*.
- **chain:** `to work, to labour, to work at and make and build, to do and perform and accomplish, to work the land, to earn by working`
- **used:** GEN 2:5

### ἀναβαίνω — imperfect

- **headword:** `was going up` — Middle Liddell, first sense *to go up, mount*; imperfect
  active, 3rd singular.
- **chain:** `was going up, was mounting, was going up to, was embarking`
- **used:** GEN 2:6

### ποτίζω — imperfect

- **headword:** `was giving to drink` — Middle Liddell, first sense *to give to drink*;
  imperfect active, 3rd singular.
- **chain:** `was giving to drink, was watering, was watering the cattle`
- **used:** GEN 2:6

### πλάσσω — aorist

- **headword:** `formed` — Middle Liddell, first sense *to form, mould, shape*; aorist
  active, 3rd singular.
- **chain:** `formed, moulded, shaped, moulded and formed by training, formed in the mind, put into a certain form`
- **used:** GEN 2:7

The potter's verb, Latin *fingere*. Not the ἐποίησεν of chapter 1.

### ἐμφυσάω — aorist

- **headword:** `blew in` — Middle Liddell gives the entry one sense and one translation,
  *to blow in: to play the flute*, where the colon marks a special application rather than a
  second sense. Aorist active, 3rd singular.
- **chain:** `blew in, played the flute`
- **used:** GEN 2:7

The chain carries the flute because the lexicon does. The note explains the colon.

### ζάω — present participle

- **headword:** `living` — Middle Liddell, first sense *to live*; present active participle,
  accusative singular feminine, agreeing with ψυχήν.
- **chain:** `living, alive, in full life and strength, fresh, strong`
- **used:** GEN 2:7

### φυτεύω — aorist

- **headword:** `planted` — Middle Liddell, first sense *to plant*; aorist active, 3rd singular.
- **chain:** `planted, planted for himself, begot, produced and brought about and caused`
- **used:** GEN 2:8

### τίθημι — aorist middle

- **headword:** `set` — Middle Liddell, first sense *to set, put, place*; aorist middle,
  3rd singular.
- **chain:** `set, put, placed, planted, laid`
- **used:** GEN 2:8

### ἐξανατέλλω — plain text

`sprang up from`. No unit: Middle Liddell gives the entry a single sense, *to spring up
from*, so there is no range to open. The LXX uses it transitively — God made the trees spring
up — where the lexicon has it intransitive; the verse's note records that. GEN 2:9.

### οἶδα — perfect infinitive

- **headword:** `to know` — Middle Liddell, first sense *to know*; perfect active infinitive,
  articular (τοῦ εἰδέναι).
- **chain:** `to know, to be assured, to be versed in`
- **used:** GEN 2:9

### ἐκπορεύομαι — present

- **headword:** `goes out` — filed under the active ἐκπορεύω, whose opening gloss, *to make
  to go out, fetch out*, is the active alone and is skipped by name; the middle glosses the
  entry tags next, *to go out* and *forth, march out*, are this form. Present middle,
  3rd singular.
- **chain:** `goes out, goes forth, marches out`
- **used:** GEN 2:10

### ἀφορίζω — present middle/passive

- **headword:** `is marked off by boundaries` — Middle Liddell, first sense *to mark off by
  boundaries*; present, 3rd singular, one form for middle and passive.
- **chain:** `is marked off by boundaries, is marked off for itself, is distinguished and determined and defined, is set apart and separated`
- **used:** GEN 2:10

### κυκλόω — present participle

- **headword:** `the one encircling` — Middle Liddell, first sense *to encircle, surround*;
  present active participle, articular.
- **chain:** `the one encircling, surrounding, moving in a circle, going round`
- **used:** GEN 2:11, GEN 2:13

### πορεύομαι — present participle

- **headword:** `the one being driven` — filed under the active πορεύω. Sense I is marked
  *Act.* and is skipped by name; sense II is marked *Pass. and Mid.* and is kept whole, so
  its first translation, *to be driven or carried*, stands — the middle has a claim on it.
  *To go, walk, march* follows in the same sense group. Present middle participle, articular.
- **chain:** `the one being driven, being carried, going, walking, marching, going across and passing`
- **used:** GEN 2:14

### λαμβάνω — aorist

- **headword:** `took` — Middle Liddell, first sense *to take*; aorist active, 3rd singular.
- **chain:** `took, received, took hold of and grasped and seized`
- **used:** GEN 2:15

### φυλάσσω — present infinitive

- **headword:** `to keep watch and ward` — Middle Liddell, first sense *to keep watch and
  ward, keep guard*.
- **chain:** `to keep watch and ward, to keep guard, to watch and guard and keep and defend`
- **used:** GEN 2:15

A sentry's word before it is a gardener's. The garden is given a guard, not only a keeper.

### ἐντέλλομαι — aorist middle

- **headword:** `enjoined` — filed under the active ἐντέλλω, whose single sense, *to enjoin,
  command*, is not restricted to a voice, so nothing is skipped. Aorist middle, 3rd singular.
- **chain:** `enjoined, commanded`
- **used:** GEN 2:16

### λέγω

- **headword:** `saying` (present active participle, GEN 2:16) / `said` (aorist, GEN 2:18).
  The lexicon prints three entries under this spelling: λέγω¹ *to lull to sleep*, λέγω²
  *to gather, pick up*, λέγω³ *to say, speak*. The third is the word (see *Homographs*).
- **chain:** `saying, speaking, declaring, calling by name, telling`
- **used:** GEN 2:16, GEN 2:18

### ἐσθίω — future and aorist subjunctive

- **headword:** `you will eat` (future middle, 2nd singular GEN 2:16, plural GEN 2:17) /
  `you may eat` (aorist subjunctive, GEN 2:17) — Middle Liddell, first sense *to eat*.
- **chain:** `you will eat, you will eat of` / `you may eat, you may eat of`
- **used:** GEN 2:16, GEN 2:17

### γινώσκω — present infinitive

- **headword:** `to learn to know` — Middle Liddell, first sense *to learn to know, to
  perceive, mark, learn*. Filed under the Attic γιγνώσκω.
- **chain:** `to learn to know, to perceive, to mark, to learn, to discern and distinguish`
- **used:** GEN 2:17

Not οἶδα. The tree is τοῦ εἰδέναι at 2:9 and τοῦ γινώσκειν at 2:17 — knowledge one has,
against knowledge one comes by — and the two headwords keep the two verbs apart.

### ἀποθνῄσκω — future middle

- **headword:** `you will die off` — Middle Liddell, first sense *to die off, die*; future
  middle, 2nd plural. Perseus keys it without the iota subscript, `a)poqnh/skw`.
- **chain:** `you will die off, you will die, you will be put to death, you will be slain`
- **used:** GEN 2:17

### ἄγω — aorist

- **headword:** `led` — Middle Liddell, first sense *to lead*; aorist active, 3rd singular.
- **chain:** `led, carried, conveyed, brought, marched`
- **used:** GEN 2:19

### ὁράω — aorist infinitive

- **headword:** `to see` — Middle Liddell, first sense *to see*; aorist infinitive (ἰδεῖν).
- **chain:** `to see, to perceive, to behold, to look at`
- **used:** GEN 2:19

### καλέω

- **headword:** `he will call` (future, GEN 2:19) / `called` (aorist, GEN 2:19, 2:20) —
  Middle Liddell, first sense *to call, summon*.
- **chain:** `called, summoned, called to himself, invited`
- **used:** GEN 2:19, GEN 2:20

### εὑρίσκω — aorist passive

- **headword:** `was found` — Middle Liddell, first sense *to find*; aorist passive,
  3rd singular.
- **chain:** `was found, was found out, was discovered`
- **used:** GEN 2:20

A search that came to nothing, not a simple absence.

### ἐπιβάλλω — aorist

- **headword:** `threw` — Middle Liddell, first sense *to throw*; aorist active, 3rd singular.
- **chain:** `threw, cast upon, laid on, affixed, added`
- **used:** GEN 2:21

### ὑπνόω — aorist

- **headword:** `put to sleep` — Middle Liddell, first sense *to put to sleep*, transitive and
  causative; *to fall asleep, sleep* is its second. Aorist active, 3rd singular.
- **chain:** `put to sleep, fell asleep, slept`
- **used:** GEN 2:21

The Septuagint uses the active intransitively — *and he slept*. The headword keeps the
lexicon's order and the verse's note carries the usage.

### ἀναπληρόω — aorist

- **headword:** `filled up` — Middle Liddell, first sense *to fill up*; aorist active,
  3rd singular.
- **chain:** `filled up, made up and supplied, filled, paid in full`
- **used:** GEN 2:21

Making good a deficiency — a gap in a line of troops, a debt paid in full.

### οἰκοδομέω — aorist

- **headword:** `built a house` — Middle Liddell, first sense *to build a house*, before the
  general *to build*. Aorist active, 3rd singular.
- **chain:** `built a house, built, built for himself`
- **used:** GEN 2:22

### λαμβάνω — aorist passive

- **headword:** `was taken` — the same entry as the active `took`; aorist passive,
  3rd singular.
- **chain:** `was taken, was received, was taken hold of and seized`
- **used:** GEN 2:23

### καλέω — future passive

- **headword:** `she will be called` — the same entry as `called`; future passive,
  3rd singular.
- **chain:** `she will be called, she will be summoned, she will be invited`
- **used:** GEN 2:23

### καταλείπω — future

- **headword:** `will leave behind` — Middle Liddell, first sense *to leave behind*; future
  active, 3rd singular.
- **chain:** `will leave behind, will leave behind him, will leave as an inheritance`
- **used:** GEN 2:24

### προσκολλάω — future passive

- **headword:** `will be glued on` — Middle Liddell, first sense *to glue on*; future
  passive, 3rd singular. `NOT_SENSES` drops the scrap *to*, sliced from "to glue on or to".
- **chain:** `will be glued on, will stick, will cleave to`
- **used:** GEN 2:24

Passive in form where English makes it active. κόλλα is glue; *collagen* is its relative.

### αἰσχύνω — imperfect middle/passive

- **headword:** `were being ashamed` — sense I and its subsenses are the active (*to make
  ugly, disfigure, mar*; *to dishonour*) and are skipped by name; the first numbered sense
  open to this voice is II, *to be ashamed, feel shame*. Imperfect, 3rd plural, one form for
  middle and passive.
- **chain:** `were being ashamed, were feeling shame, were being dishonoured`
- **used:** GEN 2:25

### Verbs new in GEN 3

Each headword is Middle Liddell's first sense, in the form the text uses, unless a note says
otherwise.

| lemma | form | headword | chain | used |
| --- | --- | --- | --- | --- |
| ἐσθίω | aor. 3 sg / 3 pl / 1 sg / 2 sg | `ate` · `they ate` · `I ate` · `you ate` | `ate, ate of` (with the person) | 3:6, 3:11, 3:12, 3:13, 3:17 |
| ἐσθίω | fut. 1 pl | `we will eat` | `we will eat, we will eat of` | 3:2 |
| ἐσθίω | aor. inf. / aor. subj. 3 sg | `to eat` · `he may eat` | `to eat, to eat of` · `he may eat, he may eat of` | 3:11, 3:17, 3:22 |
| ἀποθνήσκω | aor. subj. 2 pl | `you may die off` | `you may die off, you may die, you may be put to death, you may be slain` | 3:3 |
| ἅπτω | aor. mid. subj. 2 pl | `you may fasten yourselves to` | `you may fasten yourselves to, you may cling to, you may hang on by, you may lay hold of, you may grasp, you may touch` | 3:3 |
| οἶδα | pluperf. 3 sg | `knew` | `knew, was assured, was versed in` | 3:5 |
| διανοίγω | fut. / aor. pass. 3 pl | `will be opened` · `were opened` | `will be opened, will be opened and explained` · `were opened, were opened and explained` | 3:5, 3:7 |
| γινώσκω | pres. ptcp. / aor. 3 pl | `learning to know` · `learned to know` | `learning to know, perceiving, marking, learning, discerning and distinguishing` · the same in the aorist | 3:5, 3:7 |
| ὁράω | aor. 3 sg | `saw` | `saw, perceived, beheld, looked at` | 3:6 |
| κατανοέω | aor. inf. | `to observe well` | `to observe well, to understand, to perceive, to learn, to consider` | 3:6 |
| λαμβάνω | aor. ptcp. / aor. subj. / aor. pass. 2 sg | `having taken` · `he may take` · `you were taken` | `having taken, having received, having taken hold of and grasped and seized` · likewise | 3:6, 3:19, 3:22 |
| δίδωμι | aor. 3 sg / 2 sg | `gave` · `you gave` | `gave, granted, provided, gave over and delivered up` | 3:6, 3:12 |
| ῥάπτω | aor. 3 pl | `sewed` | `sewed, stitched together, devised and contrived and plotted` | 3:7 |
| ἀκούω | aor. 3 pl / 1 sg / 2 sg | `heard` · `I heard` · `you heard` | `heard, had hearing of, heard tell of, hearkened and gave ear, listened to and obeyed` | 3:8, 3:10, 3:17 |
| περιπατέω | pres. ptcp. | `walking up and down` | `walking up and down, walking about, walking, living` | 3:8, 3:10 |
| κρύπτω | aor. pass. 3 pl / 1 sg | `were hidden` · `I was hidden` | `were hidden, were covered and cloaked, hid themselves and lay hidden, were concealed and kept secret` | 3:8, 3:10 |
| φοβέομαι | aor. pass. 1 sg | `I was put to flight` | `I was put to flight, I fled affrighted, I fled, I was seized with fear, I was affrighted, I feared` | 3:10 |
| ἀναγγέλλω | aor. 3 sg | `carried back tidings of` | `carried back tidings of, reported` | 3:11 |
| ἐντέλλομαι | aor. 1 sg | `I enjoined` | `I enjoined, I commanded` | 3:11, 3:17 |
| ποιέω | aor. 2 sg | `you made` | `you fashioned, you wrought, you produced, you performed, you did` | 3:13, 3:14 |
| ἀπατάω | aor. 3 sg | `cheated` | `cheated, tricked, outwitted, beguiled, deceived` | 3:13 |
| πορεύομαι | fut. 2 sg | `you will be driven` | `you will be driven, you will be carried, you will go, you will walk, you will march` | 3:14 |
| τίθημι | fut. 1 sg | `I will set` | `I will set, I will put, I will place, I will plant, I will lay` | 3:15 |
| τηρέω | fut. 3 sg / 2 sg | `will watch over` | `will watch over, will protect and guard, will give heed to and watch narrowly, will watch for, will keep` | 3:15 |
| πληθύνω | pres. ptcp. / fut. 1 sg | `making full` · `I will make full` | `making full, increasing, multiplying` · likewise | 3:16 |
| τίκτω | fut. mid. 2 sg | `you will bring into the world` | `you will bring into the world, you will bring forth, you will bear, you will produce` | 3:16 |
| κυριεύω | fut. 3 sg | `will be lord` | `will be lord, will be master of, will have legal power` | 3:16 |
| ἀνατέλλω | fut. 3 sg | `will make to rise up` | the chain of GEN 2:5, in the future | 3:18 |
| ἀποστρέφω | aor. inf. | `to turn` | `to turn, to turn back, to turn away, to turn oneself about, to bring back` | 3:19 |
| ἀπέρχομαι | fut. 2 sg | `you will go away` | `you will go away, you will depart from, you will depart, you will depart from life` | 3:19 |
| ζάω | pres. ptcp. gen. pl. / fut. 3 sg | `of the living` · `he will live` | `of the living, of the alive, of those in full life and strength, of the fresh and strong` · `he will live, he will be in full life and strength, he will be fresh and strong` | 3:20, 3:22 |
| ἐνδύω | aor. 3 sg | `clothed in` | `clothed in, clothed` — sense II, the causal aorist | 3:21 |
| γίνομαι | perf. 3 sg | `has come into being` | `has come to be and stands so, has arisen and remains arisen, has been brought into existence and continues so` — a standing resultant state | 3:22 |
| ἐκτείνω | aor. subj. 3 sg | `he may stretch out` | `he may stretch out, he may spread out, he may put forth` | 3:22 |
| ἐξαποστέλλω | aor. 3 sg | `sent quite away` | `sent quite away, dispatched` | 3:23 |
| ἐκβάλλω | aor. 3 sg | `threw` | `threw, cast out of, threw out, cast out and banished, deposed, threw away and rejected` | 3:24 |
| κατοικίζω | aor. 3 sg | `removed to` | `removed to, planted, settled, established as a colonist, restored to one's country` | 3:24 |
| τάσσω | aor. 3 sg | `arranged` | `arranged, put in order, drew up in order of battle, posted and stationed, appointed` | 3:24 |
| στρέφω | pres. mid./pass. ptcp. | `the one turning itself` | `the one turning itself, turning round, turning about, turning to and fro, turning back, revolving` — the entry's actives skipped by name | 3:24 |

### Verbs new in GEN 4

| lemma | form | headword | chain | used |
| --- | --- | --- | --- | --- |
| γινώσκω | aor. 3 sg / pres. 1 sg | `learned to know` · `I learn to know` | the chain of GEN 3:7, in the form | 4:1, 4:9, 4:17, 4:25 |
| συλλαμβάνω | aor. ptcp. fem. | `having collected` | `having collected, having gathered together, having taken up, having laid hold of and seized, having comprehended, having conceived` | 4:1, 4:17, 4:25 |
| τίκτω | aor. 3 sg / aor. inf. | `brought into the world` · `to bring into the world` | `brought into the world, brought forth, bore, produced` | 4:1, 4:2, 4:17, 4:20, 4:22, 4:25 |
| κτάομαι | aor. mid. 1 sg | `I procured for myself` | `I procured for myself, I got, I gained, I acquired` | 4:1 |
| προστίθημι | aor. / fut. 3 sg | `put to` · `will put to` | `put to, handed over and delivered, gave and bestowed, imposed further, attributed, added` | 4:2, 4:12 |
| γίνομαι | aor. 3 sg (mid. and pass.) / aor. 2 sg | `came into being` · `you came into being` | the chain of JHN 1:6, in the form | 4:2, 4:3, 4:6, 4:8, 4:18, 4:26 |
| ἐργάζομαι | pres. ptcp. / fut. 2 sg (ἐργᾷ) | `working` · `you will work` | the chain of GEN 2:5, in the form | 4:2, 4:12 |
| φέρω | aor. 3 sg | `bore` | `bore, carried, bore along, brought and fetched, brought and offered and presented` | 4:3, 4:4 |
| ἐφοράω | aor. 3 sg (ἐπεῖδεν) | `oversaw` | `oversaw, observed, surveyed, watched over and took notice of, looked upon and beheld` | 4:4 |
| προσέχω | aor. 3 sg | `held to` | `held to, offered, brought to, turned to, turned the mind to, gave heed to` | 4:5 |
| λυπέω | aor. 3 sg | `gave pain to` | `gave pain to, pained, distressed, grieved, vexed, annoyed` | 4:5 |
| συμπίπτω | aor. 3 sg | `fell together` | `fell together, met in battle and came to blows, fell in with and met, fell upon and happened, concurred` | 4:5, 4:6 |
| προσφέρω | aor. subj. 2 sg | `you may bring to` | `you may bring to, you may apply, you may lay upon, you may offer, you may present and give, you may set before` | 4:7 |
| διαιρέω | aor. subj. 2 sg | `you may take one from another` | `you may take one from another, you may cleave in twain, you may divide into parts, you may divide, you may distinguish, you may determine` | 4:7 |
| ἁμαρτάνω | aor. 2 sg | `you missed the mark` | `you missed the mark, you failed of your purpose, you went wrong, you erred, you sinned` | 4:7 |
| ἡσυχάζω | aor. impv. 2 sg | `be still` | `be still, keep quiet, be at rest` | 4:7 |
| ἄρχω | fut. 2 sg, c. gen. | `will begin` | `will begin, will make a beginning of, will lead the way, will lead and rule and govern, will rule over` | 4:7 |
| διέρχομαι | aor. subj. 1 pl | `let us go through` | `let us go through, let us pass through, let us go through in detail` | 4:8 |
| ἀνίστημι | aor2 3 sg | `stood up` | `stood up, rose, rose to fight against, rose to go and set out` | 4:8 |
| ἀποκτείνω | aor. / fut. / aor. ptcp. / aor. 1 sg | `killed` · `will kill` · `the one having killed` · `I killed` | `killed, slew, condemned to death`, in the form | 4:8, 4:14, 4:15, 4:23, 4:25 |
| βοάω | pres. 3 sg | `cries aloud` | `cries aloud, shouts, sounds and resounds and roars, calls on, calls for` | 4:10 |
| χάσκω | aor. 3 sg (ἔχανεν) | `yawned` | `yawned, gaped, uttered with open mouth` | 4:11 |
| δέχομαι | aor. inf. | `to take` | `to take, to accept, to receive, to receive in exchange, to give ear to` | 4:11 |
| δίδωμι | aor. inf. | `to give` | `to give, to grant, to provide, to give over and deliver up` | 4:12 |
| στένω, τρέμω | pres. ptcp. | `moaning` · `trembling` | `moaning, sighing, groaning, bewailing and lamenting` · `trembling, fearing, trembling at` | 4:12, 4:14 |
| ἀφίημι | aor. pass. inf. | `to be sent forth` | `to be sent forth, to be discharged, to be sent away and let go, to be set free, to be released` | 4:13 |
| ἐκβάλλω | pres. 2 sg | `you throw` | the chain of GEN 3:24, in the form | 4:14 |
| κρύπτω | fut. pass. 1 sg | `I will be hidden` | the chain of GEN 3:10, in the form | 4:14 |
| εὑρίσκω | pres. ptcp. | `the one finding` | `the one finding, the one finding out, the one discovering` | 4:14, 4:15 |
| ἐκδικέω | pres. ptcp. pass. pl. / perf. 3 sg | `things being avenged` · `has been avenged` | `things being avenged, things being punished, things on which vengeance is exacted` · `has been avenged and stands avenged, has been punished and stands punished` | 4:15, 4:24 |
| παραλύω | fut. 3 sg | `will loose from the side` | `will loose from the side, will take off and detach, will undo and put an end to, will set free, will loose beside` | 4:15 |
| ἀναιρέω | aor. inf. | `to take up` | `to take up, to raise, to take up and carry off, to make away with and destroy and kill, to abolish` | 4:15 |
| ἐξέρχομαι | aor. 3 sg | `went out of` | `went out of, came out, went away and marched off, went forth` | 4:16 |
| οἰκέω | aor. 3 sg / pres. ptcp. | `inhabited` · `of those inhabiting` | `inhabited, occupied, dwelt and lived, was settled`, in the form | 4:16, 4:20 |
| οἰκοδομέω | pres. ptcp. | `building a house` | the chain of GEN 2:22, in the form | 4:17 |
| ἐπονομάζω | aor. 3 sg | `gave a surname` | `gave a surname, named, called, pronounced` | 4:17, 4:25, 4:26 |
| γεννάω | aor. 3 sg | `begot` | `begot, engendered, brought forth, produced` | 4:18 |
| καταδείκνυμι | aor. ptcp. | `the one having discovered and made known` | `the one having discovered and made known, the one having invented and taught and introduced, the one having shown how` | 4:21 |
| ἀκούω | aor. impv. 2 pl | `hear` | the chain of GEN 3:8, in the form | 4:23 |
| ἐξανίστημι | aor1 3 sg | `raised up` | `raised up, made to rise, removed and expelled, roused` | 4:25 |
| ἐλπίζω | aor. 3 sg | `hoped for` | `hoped for, looked for, expected, hoped, thought and supposed, hoped in` | 4:26 |
| ἐπικαλέω | pres. mid. inf. | `to call upon` | `to call upon, to invoke and appeal to, to invite, to call in as a helper, to be called by surname` | 4:26 |

Where the lexicon restricts a sense to one voice, the entry's own labels decide, as for ἄρχω:
φοβέω's *A. Act.*, ἅπτω's active sense I against *II. Mid. … c. gen.*, στρέφω's *B. Pass.
and Mid.* A headword that takes a person from the form says it — `they ate` and `I ate` are
one Greek form, ἔφαγον, at 3:6 and 3:12.

---

## Nouns

### ἀρχή (with ἐν)

- **headword:** `in beginning` — ἐν *in*; ἀρχή, Middle Liddell's first sense *a beginning*;
  ἀρχῇ is anarthrous, so no article. (Middle Liddell also lists *in the beginning, at first*
  among its later senses, for a phrase this extraction does not show; it is not used.)
- **chain:** `within, inside of, and by means of the first moment, the origin-point, the source, the first principle from which a thing proceeds, and simultaneously the headship, the rule, and the governing precedence over all that follows`
- **short:** `within, inside of, and by means of the first moment, the origin-point, the source, the first principle`
- **used:** GEN 1:1, JHN 1:1 (full, identical — the quotation), JHN 1:2 (short)

Both halves — temporal origin and ruling precedence — are obligatory in the full form. The
short form drops the precedence half only because JHN 1:2 restates JHN 1:1.

### λόγος

- **headword:** `the word` — Middle Liddell, first sense *the word*; articular. Lowercase: no
  title capital.
- **chain:** `the utterance, the spoken word, the thing-said, the account, the reckoning, the rationale, the reasoned discourse, the intelligible ordering by which a mind is expressed and by which that mind itself coheres`
- **short:** `the utterance, the account`
- **used:** JHN 1:1

Lowercase throughout; the notes say why (JHN 1:1, *Capitals*). *Logos* appears in neither
panel.

### οὐρανός

- **headword:** `the heaven` — Middle Liddell, first sense *heaven*; articular.
- **chain:** `the vaulted arch, the sky-expanse, the region above and over`
- **used:** GEN 1:1

Singular in the LXX against Hebrew dual/plural *šāmayim*. Flag `divergence`.

### γῆ

- **headword:** `the earth` — Middle Liddell, first sense *earth*; articular.
- **chain (full):** `the land, the dry ground, the soil, the territory, the terrestrial realm as the counterpart-below`
- **short:** `the land, the dry ground, the terrestrial realm`
- **used:** GEN 1:1 (full), GEN 1:2 (short)

`as the counterpart-below` is used only where γῆ is paired with οὐρανός.

### σκότος

- **headword:** `darkness` — Middle Liddell, first sense *darkness, gloom*; anarthrous.
- **chain:** `obscurity, gloom, the privation and the absence of light`
- **used:** GEN 1:2

### ἄβυσσος

- **headword:** `the great deep` — used as a noun (τῆς ἀβύσσου), so the first noun sense:
  Middle Liddell's third group, *the great deep, the abyss, bottomless pit*. The first two
  are the adjective (*with no bottom, bottomless*). Articular.
- **chain:** `the bottomless, the depth without a floor to sound, the unfathomable and unmeasurable deep`
- **used:** GEN 1:2

### πνεῦμα

- **headword:** `blowing` — Middle Liddell, sense I, whose first translation is *a blowing*
  (it goes on: *a wind, blast*); anarthrous, so no article.
- **chain:** `breath, wind, moving air, respiration, spirit`
- **used:** GEN 1:2 (followed by θεοῦ as its own unit)

Lowercase *spirit*; the notes say why (GEN 1:2, *Capitals*). In the full lexicon *spirit*
comes after *wind* and *breath*; the two-meaning quick gloss that puts it first is a summary,
not the lexicon's order. The one place where Greek and Hebrew line up exactly — πνεῦμα and
*rûaḥ* share the same triple range. Say so in the notes rather than choosing.

### ὕδωρ — plain text

`the water`. No chain — the word is not doing lexical work here. Singular against Hebrew
plural *mayim*; flag `divergence`. **The Hebrew's *face of* is absent from the LXX at both
points in this verse and must not appear in either reading text.**

### ἄνθρωπος

- **headword:** `man` — Middle Liddell, sense I *man* (the etymology *manfaced* stands before
  the senses); anarthrous, so no article.
- **chain:** `a man, a human being`
- **used:** JHN 1:6

### οὗτος

- **headword:** `this` — Middle Liddell, first sense.
- **chain:** `this same one, this very one and no other`
- **used:** JHN 1:2

`and no other` carries the near demonstrative's work of pinning the referent.

### Adjectives at GEN 1:2

- **ἀόρατος** — headword `unseen` (Middle Liddell, first sense *unseen, not to be seen,
  invisible*); chain `unseeable, un-viewable, not presenting itself to the eye,
  imperceptible to sight`
- **ἀκατασκεύαστος** — headword `not properly prepared` (no Middle Liddell entry; LSJ's first
  sense, which LSJ follows with *unwrought, unformed*, citing this verse); chain `un-built-out, unfurnished, unequipped, unprovisioned, not fitted out with its
  appointments, lacking the constructed arrangement that a full outfitting would supply`

Both stand under one `divergence` flag against Hebrew *tōhû wā-bōhû*. *Formless* is too
abstract for ἀκατασκεύαστος and is not used.

### κόσμος

- **headword:** `the order` — Middle Liddell, first sense *order*; articular.
- **chain:** `the order, the good order and decency, the form and fashion, the government, the ornament and adornment`
- **used:** GEN 2:1

*World* is a late sense and is not the lexicon's first. Flag `divergence` against Hebrew
*ṣābāʾ*, *host*: the Greek keeps the ranked arrangement and loses the army.

### ἡμέρα

- **headword:** `the day` — Middle Liddell, first sense *day*; articular where the Greek has
  the article (GEN 2:2, 2:3), anarthrous in ᾗ ἡμέρᾳ (GEN 2:4), which takes `day`.
- **chain:** `the day, the day-break, the time`
- **with ἐν:** `in the day` / `within, inside of, and by means of the day, the day-break, the time`
- **used:** GEN 2:2, GEN 2:3, GEN 2:4

### ἔργον

- **headword:** `the works` — Middle Liddell, first sense *work*; articular, plural.
- **chain (full):** `the works, the business, the deeds, the action, the works of industry and the tilled lands`
- **short:** `the works, the business, the deeds`
- **used:** GEN 2:2 (full, then short), GEN 2:3 (short)

### βίβλος

- **headword:** `the inner bark of the papyrus` — Middle Liddell, first sense; articular.
  *A book* is the entry's third sense and is not taken.
- **chain:** `the inner bark of the papyrus, the bark, the book`
- **used:** GEN 2:4

The plainest case so far of the rule against the expected word. The material stands where
the reader expects the object; the note carries the explanation.

### γένεσις

- **headword:** `of origin` — Middle Liddell, first sense *an origin, source, productive
  cause*; genitive, anarthrous.
- **chain:** `of origin, of source, of productive cause, of beginning, of manner of birth, of race and descent, of production and generation, of creation and the created things`
- **used:** GEN 2:4

The word the book is named from. It holds the origin of a thing and the account of that
origin together, where English splits *genesis* from *generations*.

### πᾶς

- **headword:** `all` — Middle Liddell, first sense *all, the whole*.
- **chain:** `all, the whole, every, every single`
- **used:** GEN 2:1, GEN 2:2, GEN 2:3

The whole taken together, not merely each part.

### οὐρανός and γῆ — anarthrous genitive

GEN 2:4 has them without the article, so no *the*:

- `of heaven` / `of heaven, of the vault, of the firmament and the sky`
- `of earth` / `of earth, of land, of the ground`

The articular forms are unchanged above.

### χλωρός

- **headword:** `greenish-yellow` — Middle Liddell, first sense; a colour, anarthrous.
- **chain:** `greenish-yellow, pale-green, light-green, green and grassy, yellow, pale and bleached, fresh and living`
- **used:** GEN 2:5

The colour comes first and the plant is named from it, which is the lexicon's order.

### χόρτος

- **headword:** `an inclosed place` — Middle Liddell, first sense *an inclosed place, a
  feeding-place*; anarthrous, accusative.
- **chain:** `an inclosed place, a feeding-place, any feeding-ground, food and fodder and provender, grass, hay`
- **used:** GEN 2:5

*Grass* is the entry's fourth sense. The enclosure stands where the reader expects the crop.

### ἀγρός — genitive

- **headword:** `of field` — Middle Liddell, first sense *fields, lands*; genitive singular,
  anarthrous, so the singular against the lexicon's plural citation form.
- **chain:** `of field, of lands, of a farm, of the country`
- **used:** GEN 2:5, twice

### πηγή

- **headword:** `running waters` — Middle Liddell, first sense *running waters, streams*,
  which the entry marks *mostly in pl.* while the text has the singular. The lexicon's
  first translation stands; the number is recorded in the verse's notes.
- **chain:** `running waters, streams, a fount, a source, an origin`
- **used:** GEN 2:6

`NOT_SENSES` drops *(the spring* and *well-head)* — fragments of the phrase by which the
entry distinguishes πηγή *from* κρουνός, and so glosses of a different word.

### πρόσωπον

- **headword:** `the face` — Middle Liddell, first sense *the face, visage, countenance*;
  articular. Genitive articular τῆς γῆς beside it takes `of the earth`.
- **chain:** `the face, the visage, the countenance, the look, the mask, the outward appearance`
- **used:** GEN 2:6, GEN 2:7

The LXX renders Hebrew *pānîm* here, having dropped it twice in 1:2. That difference is the
reason `face of the waters` is a banned phrase and `the face of the earth` is not.

### χοῦς

- **headword:** `earth thrown down` — the second of the two entries under this spelling (see
  *Homographs* above); accusative, anarthrous.
- **chain:** `earth thrown down, heaped up, dust`
- **used:** GEN 2:7

### πνοή

- **headword:** `a blowing` — Middle Liddell, first sense *a blowing, blast, breeze*;
  accusative, anarthrous.
- **chain:** `a blowing, a blast, a breeze, a breathing hard, breath, flame`
- **used:** GEN 2:7

The same opening gloss the lexicon gives πνεῦμα at 1:2. Two different words for moving air,
and *spirit* is first in neither.

### ζωή — genitive

- **headword:** `of a living` — Middle Liddell, first sense *a living*; genitive, anarthrous.
- **chain:** `of a living, of the means of life and substance, of life and existence, of a way of life`
- **used:** GEN 2:7

*A living* in the sense of a livelihood stands before *life*, and the chain keeps the order.

### ψυχή

- **headword:** `breath` — Middle Liddell, first sense; accusative, anarthrous.
- **chain:** `breath, the life, the spirit, life and death, the ghost, the departed soul`
- **used:** GEN 2:7

*Soul* is not the first sense and is not the headword. With πνοήν in the same verse the
phrase runs breath into breath.

### ἄνθρωπος — articular

- **headword:** `the man` — the same entry as the anarthrous `man` (JHN 1:6, GEN 2:5), with
  the article the Greek prints.
- **chain:** `the man, the human being, mankind`
- **used:** GEN 2:7, twice

### κύριος

- **headword:** `lord` — the entry opens as an adjective, *having power*; the first **noun**
  sense is *authority over, lord*, and the rule takes the first noun sense. Anarthrous.
- **chain:** `lord, master, the one having power and authority over`
- **used:** GEN 2:8

Renders the Hebrew divine name, which the Greek replaces with a title rather than
transliterating. Say so in the notes wherever it first appears in a chapter.

### παράδεισος

- **headword:** `a park` — Middle Liddell, first sense *a park*; anarthrous at GEN 2:8,
  articular after (`the park`).
- **chain:** `a park, the garden of Eden, paradise`
- **used:** GEN 2:8, 2:9, 2:10

A Persian loanword for a walled enclosure. The lexicon's second sense names this very
garden, which is where the English word comes from.

### ἀνατολή

- **headword:** `risings` — Middle Liddell, first sense *a rising, rise*; accusative plural,
  anarthrous.
- **chain:** `risings, rises, the quarter of sunrise, the east`
- **used:** GEN 2:8

### ξύλον

- **headword:** `wood` — Middle Liddell, first sense *wood*; `the wood` where articular.
- **chain:** `wood, firewood, timber, a piece of wood, a post, a stick`
- **short:** `the wood, the timber, the piece of wood`
- **used:** GEN 2:9, three times

Cut material, not the living δένδρον. The same word carries the cross in Acts and Galatians.

### ὅρασις, βρῶσις

- ὅρασις — **headword** `seeing`; **chain** `seeing, the act of sight, a vision`. GEN 2:9.
- βρῶσις — **headword** `meat`; **chain** `meat, eating, corrosion and rust`. GEN 2:9.
  *Meat* stands first and *eating* second; the third sense is the rust of Matthew 6:19.

### ὡραῖος

- **headword:** `produced at the right season` — Middle Liddell, first sense.
- **chain:** `produced at the right season, seasonable, timely, of the season, gathered in due season`
- **used:** GEN 2:9

### μέσος

- **headword:** `middle` — Middle Liddell, first sense *middle, in the middle*.
- **chain:** `middle, in the middle, the centre, mid, between two`
- **used:** GEN 2:9

### καλός and πονηρός

- καλός — **headword** `beautiful` (`of beautiful` in the genitive); **chain** `beautiful,
  beauteous, fair, good`. GEN 2:9, 2:12.
- πονηρός — **headword** `of toilsome`; **chain** `of toilsome, of painful, of grievous, of
  good-for-nothing, of bad and worthless, of wicked`. GEN 2:9.

πονηρός begins as the word for hard labour and arrives at wickedness only later in the
entry. The pair καλοῦ καὶ πονηροῦ is therefore not *good and evil* in the lexicon's order.

### γνωστός

- **headword:** `known` — Middle Liddell, first sense *known, to be known*.
- **chain:** `known, to be known`
- **used:** GEN 2:9 — a word the Hebrew of this phrase does not have; flag `divergence`.

### ποταμός

- **headword:** `a river` — Middle Liddell, first sense *a river, stream*; `the river` where
  articular, `to the river` in the dative.
- **chain:** `a river, a stream, a river-god`
- **used:** GEN 2:10, 2:13, 2:14

### ἀρχή — plural, of rivers

- **headword:** `beginnings` — the same entry as ἐν ἀρχῇ; accusative plural, anarthrous.
- **chain:** `beginnings, origins, first causes, headships and rules and governing precedences`
- **used:** GEN 2:10

The word that opens Genesis and John, here of the heads of four rivers. The full range is
kept precisely so the connection stays on the page.

### ὄνομα, εἷς

- ὄνομα — **headword** `a name`; **chain** `a name, fame, a mere name, a phrase and
  expression`. GEN 2:11, 2:13.
- εἷς — **headword** `to the one` (dative); **chain** `to the one, to a single one, to one
  alone`. GEN 2:11. Perseus keys the numeral `ei(/s`, with an acute.

### χρυσίον, ἄνθραξ, λίθος, πράσινος

- χρυσίον — **headword** `the piece of gold`; **chain** `the piece of gold, gold, gold coin
  and money`. The diminutive names a nugget before the metal. GEN 2:11, 2:12.
- ἄνθραξ — **headword** `the charcoal`; **chain** `the charcoal, the coal`. One sense only;
  the gem is named from the burning coal, as Latin *carbunculus* is. GEN 2:12.
- λίθος — **headword** `the stone`; **chain** `the stone, the precious stone, the marble`.
  GEN 2:12.
- πράσινος — **headword** `the leek-green`; **chain** `the leek-green, the light green`.
  **No Middle Liddell entry**; LSJ gives *leek-green, light green* and cites this verse for
  the stone (λίθος π. = πρασῖτις). Its *green faction* sense is the Circus and is not in
  play. GEN 2:12.

### ἐκεῖνος

- **headword:** `of that` — Middle Liddell, first sense *the person there, that person*;
  genitive, agreeing with γῆς.
- **chain:** `of that, of the one there, of the more remote`
- **used:** GEN 2:12

### θάνατος

- **headword:** `with death` — Middle Liddell, first sense *death*; dative, anarthrous.
- **chain:** `with death, with the death threatened, with the sentence of death`
- **used:** GEN 2:17 — θανάτῳ ἀποθανεῖσθε, the Hebrew infinitive absolute imitated

### μόνος

- **headword:** `alone` — Middle Liddell, first sense *alone, left alone, forsaken solitary*.
- **chain:** `alone, left alone, forsaken and solitary, only`
- **used:** GEN 2:18

### βοηθός

- **headword:** `an assistant` — the entry opens as an adjective, *assisting, auxiliary*;
  the first **noun** sense is *an assistant*, and the rule takes it.
- **chain:** `an assistant, one assisting and auxiliary`
- **used:** GEN 2:18, GEN 2:20

The Septuagint uses the word of God himself as Israel's helper, so nothing in it implies
lesser rank. Say so in the notes rather than choosing a word that decides it.

### θηρίον, κτῆνος, πετεινόν

- θηρίον — **headword** `the wild animals`; **chain** `the wild animals, the beasts, the
  savage beasts, the game`. GEN 2:19, 2:20.
- κτῆνος — **headword** `to the flocks and herds` (dative plural); **chain** `to the flocks
  and herds, to the single beast, to the ox, to the sheep, to the beast for riding`. From
  κτάομαι, to acquire: the domestic animals are named by their belonging. GEN 2:20.
- πετεινόν — **headword** `the winged fowl`; **chain** `the winged fowl, the birds, the able
  to fly and full fledged`. The neuter noun is filed under the adjective πετεινός, whose
  first **noun** sense is *winged fowl*. GEN 2:19, 2:20.

### ὅμοιος

- **headword:** `like` — Middle Liddell, first sense *like, resembling*.
- **chain:** `like, resembling, the same, all one, shared alike by both`
- **used:** GEN 2:20

ὅμοιος αὐτῷ here against κατʼ αὐτόν at 2:18 — two Greek phrases for one Hebrew *kĕnegdô*,
and both are kept.

### ἔκστασις

- **headword:** `any displacement` — Middle Liddell gives one sense, *any displacement:
  entrancement, astonishment*, where the colon marks the application, as with ἐμφυσάω;
  *a trance* follows. Accusative, anarthrous.
- **chain:** `any displacement, entrancement, astonishment, a trance`
- **used:** GEN 2:21

A standing outside oneself, not sleep. The word of Acts 10:10 and Mark 16:8.

### πλευρά

- **headword:** `of ribs` (genitive plural, GEN 2:21) / `the rib` (accusative articular,
  GEN 2:22) — Middle Liddell, first sense *a rib*.
- **chain:** `of ribs, of the ribs and the side, of one side, of the page`
- **used:** GEN 2:21, GEN 2:22

*A rib* and *the side* are one word; Greek does not choose between them and neither does
the chain.

### σάρξ

- **headword:** `flesh` — Middle Liddell, first sense; anarthrous.
- **chain:** `flesh, the flesh, muscles, the body, man's nature generally`
- **used:** GEN 2:21, GEN 2:23, GEN 2:24

### ὀστέον

- **headword:** `bone` (GEN 2:23, the Attic contraction ὀστοῦν) / `of the bones` (genitive
  plural) — **Middle Liddell has the entry but tags no usable translation in it**: only
  *the*, sliced out of "the bleached bones of the dead". The sense is LSJ's, *bone*, and
  `LSJ` in `build/words.py` overrides the entry for that reason.
- **chain:** `bone, the bones of the dead`
- **used:** GEN 2:23

The first case of an entry that exists and glosses nothing usable — distinct from ἁγιάζω,
which exists and glosses nothing at all.

### γυνή and ἀνήρ

- γυνή — **headword** `a woman` (anarthrous) / `the woman` (articular); **chain** `a woman,
  a mistress and lady, a wife and spouse, a mortal woman`. GEN 2:22, 2:23, 2:24, 2:25.
- ἀνήρ — **headword** `of the man`; **chain** `of the man, of the man in the prime of life`.
  `NOT_SENSES` drops the Latin *homo* and *vir gregis*, and the scrap *a woman* from "opp.
  to a woman". GEN 2:23.

Two unrelated Greek words where the Hebrew has a pun — *ʾiššâ* from *ʾîš*. The reason clause
of 2:23 loses its hinge in Greek, and the note says so. ἀνήρ is also the first word in the
chapter that means the male as against ἄνθρωπος, the human being.

### πατήρ, μήτηρ

- πατήρ — **headword** `the father`; **chain** `the father, the grandfather`. GEN 2:24.
- μήτηρ — **headword** `the mother`; **chain** `the mother, the dam, the source`. GEN 2:24.

### γυμνός

- **headword:** `naked` — Middle Liddell, first sense *naked, unclad*.
- **chain:** `naked, unclad, unarmed, uncovered, stripped of`
- **used:** GEN 2:25

*Unarmed* is the entry's second sense, and chapter 3 turns on it.

### νῦν, εἷς, δύο

- νῦν — **headword** `now`; **chain** `now, even now, just now`. GEN 2:23.
- εἷς — **headword** `one`; **chain** `one, a single one, one alone`. GEN 2:21 (μίαν, of the
  rib), GEN 2:24 (μίαν, of the flesh).
- δύο — plain text `the two`. One sense, so no range to open. GEN 2:24, 2:25.

`οἱ δύο` at 2:24 is not in the Hebrew at all, and every New Testament quotation of the verse
quotes the Greek with it. Flag `divergence` there.

### ἀγρός and οὐρανός — articular genitive

τοῦ ἀγροῦ and τοῦ οὐρανοῦ take the article in English, as the rule requires:

- `of the field` / `of the field, of the lands, of the farm, of the country`
- `of the heaven` / `of the heaven, of the vault, of the firmament and the sky`
- **used:** GEN 2:19, GEN 2:20, GEN 3:18

GEN 2:19 and 2:20 first carried the anarthrous chains of 2:4–5, *of field* and *of heaven*,
though both have the article; they were corrected when GEN 3:18 reused them.

### Nouns and adjectives new in GEN 3

| lemma | headword | chain | used |
| --- | --- | --- | --- |
| ὄφις | `the serpent` | `the serpent, the snake` | 3:1, 3:4, 3:13 |
| φρόνιμος (superl.) | `most in one's right mind` | `most in one's right mind, most in one's senses, most staid and unmoved and discreet, wisest, most sensible, most prudent` | 3:1 |
| θηρίον (gen. pl.) | `of the wild animals` | `of the wild animals, of the beasts, of the savage beasts, of the game` | 3:1, 3:14 |
| κτῆνος (gen. pl.) | `of the flocks and herds` | `of the flocks and herds, of the single beasts, of the oxen, of the sheep, of the beasts for riding` | 3:14 |
| καρπός | `fruit` · `of the fruit` | `fruit, produce, returns, profits, result` | 3:2, 3:3, 3:6 |
| ὀφθαλμός (pl.) | `the eyes` · `to the eyes` | `the eyes, the sight, the dearest and best, the buds` | 3:5, 3:6, 3:7 |
| ἀρεστός | `acceptable` | `acceptable, pleasing` | 3:6 |
| φύλλον (pl.) | `leaves` | `leaves, foliage, petals, herbs` | 3:7 |
| συκῆ | `of fig-tree` | `of fig-tree, of fig` | 3:7 |
| περίζωμα (pl.) | `girdles round the loins` | `girdles round the loins, aprons` | 3:7 |
| φωνή | `the sound` · `of the sound` | `the sound, the tone, the sound of the voice, the cry, the faculty of speech and discourse, the language, the saying` | 3:8, 3:10, 3:17 |
| πρόσωπον (anarthrous) | `face` · `of the face` | `face, visage, countenance, look, outward appearance` | 3:8, 3:19 |
| στῆθος | `the breast` | `the breast, the breast as the seat of feeling, the heart` | 3:14 |
| κοιλία | `the large cavity of the body` | `the large cavity of the body, the belly, the intestines, the bowels` | 3:14 |
| γῆ (anarthrous acc., nom.) | `earth` | `earth, land, the ground` | 3:14, 3:19 |
| ἡμέρα (pl.) | `the days` | `the days, the day-breaks, the times` | 3:14, 3:17 |
| ἔχθρα | `hatred` | `hatred, enmity, hatred for and enmity to, feud, hostility` | 3:15 |
| σπέρμα | `of that which is sown` | `of that which is sown, of the seed, of the germ and origin and element, of the offspring and issue, of the race and descent` | 3:15 |
| κεφαλή | `head` | `head, the whole person, the life, the top, the source, the crown` | 3:15 |
| πτέρνα | `heel` | `heel, the under part of the heel, the ham` | 3:15 |
| λύπη (pl.) | `the pains of body` · `in pains of body` | `the pains of body, the distresses and sad plights, the pains of mind, the griefs` | 3:16, 3:17 |
| στεναγμός | `the sighing` | `the sighing, the groaning, the moaning` | 3:16 |
| τέκνον (pl.) | `things borne` | `things borne, the born, children, the young` | 3:16 |
| ἀνήρ (acc., dat.) | `the man` · `to the man` | `the man, the man in the prime of life` | 3:6, 3:16 |
| ἀποστροφή | `the turning back` | `the turning back, the turning away from, the escape from, the resort and resource` | 3:16 |
| ἔργον, with ἐν | `in the works` | `within, inside of, and by means of the works, the business, the deeds` | 3:17 |
| ἄκανθα (pl.) | `thorns` | `thorns, prickles, prickly plants, thistles, thistledown, spines` | 3:18 |
| τρίβολος (pl.) | `caltrops` | `caltrops, three-spiked implements, prickly plants, burrs, thistles, threshing-boards` | 3:18 |
| χόρτος (articular) | `the inclosed place` | `the inclosed place, the feeding-place, the feeding-ground, the food and fodder and provender, the grass, the hay` | 3:18 |
| ἱδρώς, with ἐν | `in sweat` | `within, inside of, and by means of sweat, exudation, gum` | 3:19 |
| ἄρτος | `the cake` | `the cake, the loaf of wheat-bread, the bread` | 3:19 |
| ὄνομα (articular) | `the name` | `the name, the fame, the mere name, the phrase and expression` | 3:20 |
| μήτηρ (anarthrous) | `mother` | `mother, dam, source` | 3:20 |
| χιτών (pl.) | `garments worn next the skin` | `garments worn next the skin, frocks, coats of mail, coverings, skins` | 3:21 |
| δερμάτινος | `of skin` | `of skin, leathern` | 3:21 |
| χείρ | `the hand` | `the hand, the hand and arm, the arm` | 3:22 |
| αἰών | `the period of existence` | `the period of existence, the life-time and life, the age and generation, the long space of time, the era and epoch, the world` | 3:22 |
| τρυφή | `of the softness` | `of the softness, of the delicacy and daintiness, of the luxuries, of the luxuriousness and wantonness` | 3:23, 3:24 |
| φλόγινος | `the flaming` | `the flaming, the fiery, the flame-coloured` — **no Middle Liddell entry**; LSJ, citing this verse | 3:24 |
| ῥομφαία | `large sword` | `large sword, scymitar` — the article stands on φλογίνην before it | 3:24 |
| ὁδός | `the way` | `the way, the path, the track, the road, the highway, the course, the journey, the manner and method` | 3:24 |

### Nouns and adjectives new in GEN 4

| lemma | headword | chain | used |
| --- | --- | --- | --- |
| ἀδελφός | `the son of the same mother` · `of …` · `to …` | `the son of the same mother, the brother, the near kinsman` | 4:2, 4:8–11, 4:21 |
| ποιμήν | `herdsman` | `herdsman, shepherd, captain and chief, master and lord, pastor and teacher` — LSJ | 4:2 |
| πρόβατον (gen. pl.) | `of anything that walks forward` | `of anything that walks forward, of cattle, of flocks and herds, of horses, of small cattle, of sheep` | 4:2, 4:4 |
| ἡμέρα (anarthrous pl.) | `days` | `days, day-breaks, times` | 4:3 |
| καρπός (gen. pl.) | `of the fruits` | `of the fruits, of the produce, of the returns and profits, of the results` | 4:3 |
| θυσία | `an offering` · `the offerings` | `an offering, a mode of offering, offerings and sacrifices and sacred rites, a festival, the victim` | 4:3, 4:5 |
| κύριος (articular) | `to the lord` · `the lord` | the chain of `lord`, with the article | 4:3, 4:13 |
| στέαρ | `of the stiff fats` | `of the stiff fats, of the tallow, of the suet` | 4:4 |
| δῶρον | `the gifts` | `the gifts, the presents, the votive gifts, the blessings` | 4:4 |
| πεδίον | `the plain` · `in the plain` | `the plain, the flat, the plain flat open country` | 4:8 |
| φύλαξ | `a watcher` | `a watcher, a guard, a sentinel, a guardian and keeper and protector, an observer` | 4:9 |
| φωνή (anarthrous) | `sound` | `sound, tone, sound of the voice, cry, faculty of speech and discourse, language, saying` | 4:10 |
| αἷμα | `of blood` · `the blood` | `of blood, of bloodshed and murder, of race and kinship` | 4:10, 4:11 |
| στόμα | `the mouth` | `the mouth, the mouth as the organ of speech, the mouthpiece, the face, the chasm and cleft` | 4:11 |
| χείρ (gen.) | `of the hand` | `of the hand, of the hand and arm, of the arm` | 4:11 |
| ἰσχύς | `the strength` | `the strength, the might and power and force` | 4:12 |
| μέγας (comp.) | `bigger` | `bigger, greater, taller, vaster, stronger and mightier, weightier and more important` | 4:13 |
| αἰτία | `the charge` | `the charge, the accusation, the guilt, the fault, the cause` | 4:13 |
| σημεῖον | `a sign` | `a sign, a mark and token, a sign from the gods and an omen, a signal, a standard and ensign, a boundary` | 4:15 |
| γῆ, with ἐν, anarthrous | `in earth` | `within, inside of, and by means of earth, land, the ground` | 4:16 |
| πόλις | `a city` · `the city` | `a city, a citadel, a country, a body of citizens, a state` | 4:17 |
| γυνή (pl.) | `women` · `to the women` | `women, mistresses and ladies, wives and spouses, mortal women` | 4:19, 4:23 |
| εἷς (dat.) | `to the one` | the chain of GEN 2:11 | 4:19 |
| πατήρ | `the father` | the chain of GEN 2:24 | 4:20 |
| σκηνή, with ἐν | `in covered places` | `within, inside of, and by means of covered places, tents, camps, dwelling-places, temples` | 4:20 |
| κτηνοτρόφος | `of those keeping cattle` | `of those keeping cattle, of the pastoral` | 4:20 |
| ψαλτήριον | `stringed instrument` | `stringed instrument, psaltery, harp` — LSJ | 4:21 |
| κιθάρα | `lyre` | `lyre, lute` | 4:21 |
| χαλκεύς | `a worker in copper` | `a worker in copper, a smith, a joiner, a worker in metal` | 4:22 |
| χαλκός, σίδηρος | `of copper` · `of iron` | `of copper, of metal, of bronze, of brass` · `of iron, of a weapon and sword, of a knife and axe-head` | 4:22 |
| λόγος (pl.) | `the words` | `the words, the language and talk, the sayings and statements, the speech and discourse` | 4:23 |
| ἀνήρ (anarthrous) | `man` | `man, man in the prime of life` | 4:23 |
| τραῦμα | `a wound` | `a wound, a hurt and damage, a blow and defeat` | 4:23 |
| μώλωψ | `mark of a stripe` | `mark of a stripe, weal, bruise, blood-clot` — LSJ | 4:23 |
| σπέρμα (acc.) | `that which is sown` | the chain of GEN 3:15, in the accusative | 4:25 |
| ἕτερος | `other` | `other, the other of two, another, second, other than usual and different` | 4:25 |

λόγος in the plural, Lamech's words, takes a chain of its own, from the entry's senses for
*words, a saying, speech*; the prologue's chain for ὁ λόγος is not borrowed for it.

Three headwords read furthest from the expected word, and all three are the lexicon's order:
σπέρμα is *that which is sown* before it is offspring; τέκνον is *that which is borne* before
it is a child; τρίβολος is a spiked iron for laming horses before it is a thistle.

---

## Aspect formulas

Fixed wording. These go in the reading text, never in a footnote. The word-by-word layer
uses the same wording.

| aspect | formula | where it sits |
| --- | --- | --- |
| aorist | `one completed act seen whole, not a process observed in progress` | plain text after the verb's unit, in dashes (GEN 1:1) |
| imperfect (state) | `and kept on being as a standing and continuing condition` | inside ἦν's plain text |
| imperfect (εἰμί, pre-existence) | `was already in unbroken existence without any point of having come to be` | inside ἦν's plain text |
| imperfect (other verbs) | `was being …` | inside the verb's chain and headword (ἐπιφέρω) |
| perfect | a standing resultant state, not a past event — worded to the verb | inside the verb's chain |

---

## Names

Gloss on first occurrence per chapter, bare thereafter.

| Greek | unanchored form | anchored form | gloss |
| --- | --- | --- | --- |
| Ἰωάννης | Iōannēs | John | `(Ἰωάννης, from Hebrew Yôḥānān, "Yah has shown favour")` |
| Εδεμ | Edem | Eden | `(Εδεμ, from Hebrew ʿĒden, "delight, luxury")` |
| Φισων | Phisōn | Pishon | `(Φισων, from Hebrew Pîšôn, perhaps from pûš, "to leap, spring")` |
| Ευιλατ | Euilat | Havilah | `(Ευιλατ, from Hebrew Ḥăwîlâ, usually connected with ḥôl, "sand")` |
| Γηων | Gēōn | Gihon | `(Γηων, from Hebrew Gîḥôn, from gîaḥ, "to burst forth")` |
| Αἰθιοπίας | Aithiopia | Ethiopia | `(Αἰθιοπίας, from αἴθω, "to burn", and ὤψ, "face"; Hebrew Kûš)` |
| Τίγρις | Tigris | Tigris | `(Τίγρις, from Old Persian tigrā, "arrow", for its swiftness; Hebrew Ḥiddeqel)` |
| Ἀσσυρίων | Assyriōn | Assyrians | `(Ἀσσυρίων, the Assyrians, from Aššur — their god, their city, and their land)` |
| Εὐφράτης | Euphratēs | Euphrates | `(Εὐφράτης, from Old Persian Ufrātu; Hebrew Pĕrāt)` |
| Αδαμ | Adam | Adam | `(Αδαμ, from Hebrew ʾādām, "man", from ʾădāmâ, "ground")` |
| Ζωή | Zōē | Zoe | `(Ζωή, "life"; Hebrew Ḥawwâ, from ḥāyâ, "to live")` |
| χερουβιμ | cheroubim | cherubim | `(χερουβιμ, the Hebrew plural kĕrûbîm, of kĕrûb, a word of uncertain derivation)` |
| Ευαν | Euan | Eve | `(Ευαν, from Hebrew Ḥawwâ, which 3:20 translated Ζωή, "life")` |
| Καιν | Kain | Cain | `(Καιν, from Hebrew Qayin, which the verse ties to qānâ, "to get, acquire")` |
| Αβελ | Abel | Abel | `(Αβελ, from Hebrew Hebel, "breath, vapour")` |
| Ναιδ | Naid | Nod | `(Ναιδ, from Hebrew Nôd, "wandering")` |
| Ενωχ | Enōch | Enoch | `(Ενωχ, from Hebrew Ḥănôk, usually connected with ḥānak, "to dedicate")` |
| Γαιδαδ | Gaidad | Irad | `(Γαιδαδ, from Hebrew ʿÎrād, of uncertain meaning)` |
| Μαιηλ | Maiēl | Mehujael | `(Μαιηλ, from Hebrew Mĕḥûyāʾēl, of uncertain meaning, ending in ʾēl, "God")` |
| Μαθουσαλα | Mathousala | Methuselah | `(Μαθουσαλα, the Greek form of Hebrew Mĕtûšelaḥ at 5:21, given here for Mĕtûšāʾēl, usually explained as "man of God")` |
| Λαμεχ | Lamech | Lamech | `(Λαμεχ, from Hebrew Lemek, of uncertain meaning)` |
| Αδα | Ada | Adah | `(Αδα, from Hebrew ʿĀdâ, usually connected with ʿădî, "ornament")` |
| Σελλα | Sella | Zillah | `(Σελλα, from Hebrew Ṣillâ, usually connected with ṣēl, "shade")` |
| Ιωβελ | Iōbel | Jabal | `(Ιωβελ, from Hebrew Yābāl, usually connected with yābal, "to lead, bring")` |
| Ιουβαλ | Ioubal | Jubal | `(Ιουβαλ, from Hebrew Yûbal, usually connected with yābal, "to lead, bring")` |
| Θοβελ | Thobel | Tubal | `(Θοβελ, from Hebrew Tûbal-qayin, without its second part)` |
| Νοεμα | Noema | Naamah | `(Νοεμα, from Hebrew Naʿămâ, "pleasant")` |
| Σηθ | Sēth | Seth | `(Σηθ, from Hebrew Šēt, which the verse ties to šît, "to set, appoint")` |
| Ενως | Enōs | Enosh | `(Ενως, from Hebrew ʾĕnôš, "man, mankind")` |

The anchored form is the English form of the name the *Greek* prints, which is not always the
English Bible's name for the person. Μαθουσαλα at GEN 4:18 is *Methuselah*, though the Hebrew
there names Cain's descendant Methushael; Θοβελ at 4:22 is *Tubal*, though the Hebrew has
Tubal-cain. The gloss records the Hebrew, and the note flags the difference.

A name that appears twice in the verse that glosses it (Αβελ at GEN 4:2) prints its gloss the
first time only.

Ζωή at GEN 3:20 translates the Hebrew name instead of transliterating it, and Rahlfs
capitalises it as a name; so the anchored form is the English form of *that* name, *Zoe*, not
*Eve*, which comes from the Hebrew. χερουβιμ is printed in lower case, and
stays lower case in both panels; its `names` entry is what makes it a name to the checks.

Rahlfs prints the Semitic names bare — Εδεμ, Φισων, Ευιλατ, Γηων — with no accent or
breathing, and the Greek-formed ones accented: Αἰθιοπίας, Ἀσσυρίων, Εὐφράτης, Τίγρις. The
transcription keeps that distinction, and it is itself evidence of which names the
translators felt to be Greek words.

Written `[[name:Ἰωάννης]]` in `reading`; the renderer picks the form by panel.

Every occurrence is written that way, including the ones after the first. The first carries
the entry above; each later one carries the same entry with `"bare": true` and no `gloss`,
so the form prints alone. Genesis 2 needs this from the start — Εδεμ stands in 2:8 and again
in 2:10, and Αδαμ runs through 2:16–23.

---

## What `build/validate.py` enforces from this file

- a headword never stands bare, as plain text outside its unit
- no em dash inside a chain
- `BANNED_PHRASES` — seeded with `face of the waters` and `face of the deep` (GEN 1:2)

It does not yet check that a headword matches its recorded lexicon sense, or that a recurring
chain matches its entry here. Both are still enforced by reading this file first.
