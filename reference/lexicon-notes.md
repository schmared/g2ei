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
   ἀνέστη is *stood up* and GEN 9:9 ἀνίστημι *I make to stand up*. Where one lemma is used both
   ways, the word-by-word layer cannot skip by lemma alone: `FORM_SENSES` in `build/words.py`
   names the senses to skip for a given tense and voice, in place of `NOT_SENSES`. ἐπιτίθημι's
   middle, *B. Mid. to put on oneself*, is filed there the same way for GEN 9:23 ἐπέθεντο, and
   παύω's, *to take one's rest*, for GEN 11:8 ἐπαύσαντο. A sense restricted only by *subject* or *construction* is not: the
   rule reads the lexicon, not the verse. So συλλαμβάνω is *having collected* at GEN 4:1,
   though its fourth sense, "of females, to conceive", is what the verse means; ἄρχω with the
   genitive is *will begin* at 4:7, though *to rule* is its second sense; and πρόβατον is
   *anything that walks forward*, which Middle Liddell gives as the word's proper sense before
   *cattle, flocks* and, in Attic, *sheep*. The chain carries the rest, and the notes say
   where the verse's meaning stands in the entry.

   A passive or middle form takes the first sense in its own voice: κρύπτω, *to hide*, is *were
   hidden* at GEN 3:8, and φθείρω, *to ruin*, *was ruined* at 6:11. Where the entry also gives the
   passive a translation of its own — κρύπτω's *to hide oneself, lie hidden*, φθείρω's *to go to
   ruin*, πληθύνω's *to prevail* — that translation is the lexicon adding a reading, and it goes
   in the chain, not the headword. GEN 6 and 7 first took it for the headword (*went to ruin*,
   *to become firm*, *were open*); they were put back when GEN 8 found the two rules side by side.
   A verb filed under its middle (ἐκπορεύομαι, πορεύομαι, φοβέομαι) is different: its active
   glosses belong to another word's use and are skipped by name, as above.
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
| στεῖρα (GEN 11:30) | `stei=ra2` — *a cow that has not calved*; *barren* | `stei=ra1` is *a ship's keel* |
| μόσχος (GEN 12:16) | `mo/sxos2` — *a calf* | `mo/sxos1` is *a young shoot* |
| εὐθύς (GEN 15:4) | `eu)qu/s2` — the adverb, *straightway* | `eu)qu/s1` is the adjective, *straight, direct* |
<!-- homograph rows above -->

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
| ἐννακόσιοι (GEN 5:5) | ἐνακόσιοι | the later spelling; the entry is headed with the earlier |
| ἐκλέγομαι, εἰσπορεύομαι, θυμόομαι (GEN 6) | ἐκλέγω, εἰσπορεύω, θυμόω | MorphGNT's middles, filed under the active |
| ἐπιμελῶς (GEN 6:5) | ἐπιμελής | the adverb, filed inside the adjective's entry |
| ἐναντίον (GEN 6:8) | ἐναντίος | the entry is a bare cross-reference, *adverb v. ἐναντίος* |
| νοσσιά (GEN 6:14) | νεοσσιά | the contracted spelling; the entry is headed with the full one |
| κατάγαιος (GEN 6:16) | κατάγειος | a cross-reference, *ionic for κατάγειος* |
| μήν, the month (GEN 7:11) | μείς | Middle Liddell's μήν is the particle, *verily*; the month is filed under its nominative μείς |
| ἀνοίγω (GEN 7:11) | ἀνοίγνυμι | the -νυμι form heads the entry |
| σφοδρῶς (GEN 7:19) | σφοδρός | the adverb, filed inside the adjective's entry |
| μιμνήσκομαι (GEN 8:1) | μιμνήσκω | MorphGNT's middle, filed under the active |
| διατίθεμαι (GEN 9:17) | διατίθημι | likewise |
| κυνηγός (GEN 10:9) | κυναγός | the entry is headed with the Doric and Attic spelling |
| πλησίον, ἐνώπιον (GEN 11:3, 11:28) | πλησίος, ἐνώπιος | the adverb, filed inside the adjective's entry |
| καθάπερ (GEN 12:4) | καθά | filed inside the entry for καθά |
| ἔρημος (GEN 12:9) | ἐρῆμος | the entry is headed with the Attic accent |
| περιποιέομαι (GEN 12:12) | περιποιέω | MorphGNT's middle, filed under the active |
| ἐνευλογέω (GEN 12:3) | ἐνευλογέομαι | the entry is headed with the passive |
| βορρᾶς (GEN 13:14) | Βορέας | the contracted Attic form, filed under the uncontracted |
| τερέμινθος (GEN 14:6) | τέρμινθος | the spelling Rahlfs prints; the entry is headed τέρμινθος |
| παραγίνομαι (GEN 14:13) | παραγίγνομαι | the Attic spelling |
| δεκάτη (GEN 14:20) | δέκατος | cross-reference; "v. δέκατος II." glosses nothing |
| ἐπειδή (GEN 15:3) | ἐπεί | not in Middle Liddell; LSJ's entry reads "v. ἐπεί" |
| κλίβανος (GEN 15:17) | κρίβανος | the entry is headed with the Attic κρίβανος |
| κυρία (GEN 16:4) | κύριος (the second entry) | cross-reference; "fem. of κύριος signf. B. 1. 2." |
| ἐξολεθρεύω (GEN 17:14) | ἐξολοθρεύω | the spelling the text prints, as MorphGNT files ἐξολεθρευθήσεται (Acts 3:23) |
| ἀρσενικός (GEN 17:10) | ἀρρενικός | LSJ: "less Att. form ἀρσενικός" |
| ἄρα (GEN 18:3) | `a(/ra` | Perseus keys the entry with a rough breathing |
| ἆρα (GEN 18:13) | ἄρα | "in accent and sense a stronger form of ἄρα"; the entry glosses nothing |
| γέ (GEN 18:13) | γε | MorphGNT accents the enclitic; the entry is headed unaccented |
| ἀληθῶς (GEN 18:13) | ἀληθής | the adverb, filed inside the adjective's entry |
| οὐχί (GEN 18:15) | οὐ | the strengthened form, filed in its entry |
| μηδαμῶς (GEN 18:25) | μηδαμῇ | cross-reference; "adverb of μηδαμός = μηδαμῇ" |
| εἵνεκα (GEN 18:5) | ἕνεκα | the Ionic and poetic form |
| νίπτω (GEN 18:4) | νίζω | the late present, filed under νίζω |
| ἀποκρίνομαι (GEN 18:9) | ἀποκρίνω | MorphGNT's middle, filed under the active |
| πρεσβύτερος (GEN 18:11) | πρέσβυς | the comparative, filed inside the positive's entry |
| ὀρθρίζω (GEN 19:2) | ὀρθρεύω | cross-reference; "= ὀρθρεύω" |
| πλατεῖα (GEN 19:2) | πλατύς | the feminine used as a noun, filed inside the adjective's entry |
| συγγίνομαι (GEN 19:5) | συγγίγνομαι | the Attic spelling |
| σῴζω, διασῴζω (GEN 19:17, 19:19) | σώζω, διασώζω | the entries are headed without the iota subscript |
| δέομαι (GEN 19:18) | δέω (the second entry) | the deponent, filed under δέω, to lack; the first δέω is to bind |
| πρωΐ (GEN 19:27) | πρωί | the entry is headed without the diaeresis |
| μᾶλλον (GEN 19:9) | μάλα | the comparative, filed inside the positive's entry |
| ἀτμίς (GEN 19:28) | ἀτμός | cross-reference; "= ἀτμός" |
| ἐχθές (GEN 19:34) | χθές | cross-reference; "v. χθές" |
| ἐπισκέπτομαι (GEN 21:1) | ἐπισκοπέω | "a pres., which furnishes its tenses to ἐπισκοπέω" |
<!-- spelling rows above -->

The dictionary form itself does not follow the lexicon's filing: it keeps the spelling the text
prints — γίνομαι, ἔχθρα, νοσσιά, δειλινός, κατέναντι, ἐννακόσιοι, κατάγαιος, τεσσαράκοντα — and
this table finds its entry. Only the form is the dictionary's: ὀστοῦν goes under ὀστέον. GEN 5
first filed ἐννακόσιοι under ἐνακόσιοι itself; the second pass of GEN 6 showed that at odds with
every filing before it. The brief's rule was then worded as *a word the New Testament uses takes
MorphGNT's spelling*, and GEN 7's second pass, applying it, filed τεσσαράκοντα under SBLGNT's
τεσσεράκοντα: MorphGNT had only ever agreed with the text's spelling, never decided it.

Where Middle Liddell has no entry a word can be found under, LSJ supplies the senses (`LSJ` in
`build/words.py`): σύ, φλόγινος (GEN 3); ποιμήν — Middle Liddell has only the Doric ποιμάν,
*doric for ποιμήν*, pointing at an entry it lacks — ψαλτήριον, μώλωψ and ἑβδομηκοντάκις
(GEN 4). One word is in neither: σφυροκόπος (GEN 4:22), for which LSJ has only the verb
σφυροκοπέω. With no lexicon sense to head it, it stands as plain text, *a hammer-beater*, and
the note says why.

GEN 5 adds εὐαρεστέω, which Middle Liddell lacks, and the active διαναπαύω: Middle Liddell has
only the middle, διαναπαύομαι, *to rest awhile*, and 5:29 διαναπαύσει ἡμᾶς is transitive. It
also adds two numerals whose Middle Liddell entries, like ὀστέον's, tag no translation at all —
*Lat. octo, eight*; *Lat. tres, tria, three* — so ὀκτώ and τρεῖς take LSJ's, which files τρεῖς
under its neuter, τρία.

The last is the same shape as ἁγιάζω in LSJ (`= ἁγίζω`): an entry that exists, carries no
translation, and names the entry that does. Following it is not interpretation — the lexicon
is saying where the word is defined.

GEN 6 adds ἀσφαλτόω and διώροφος from LSJ, each with one sense and each citing the verse.
GEN 9 adds ὀπισθοφανής, *seen from behind*, and its adverb ὀπισθοφανῶς, *backwards*, both citing
9:23. GEN 12 adds ἐγγίζω, ἐνισχύω, and ἐτασμός, which LSJ defines only by the entry before it,
ἔτασις, *trial, affliction*. GEN 14 adds ἁλυκός, *salt, brackish*; ἀποσκευή, whose *removal,
riddance* comes before *baggage*; σφαιρωτήρ, *thong, latchet*; and περάτης, which opens "= πορθμεύς",
so that πορθμεύς's LSJ senses, *ferryman*, *boatman, seaman*, *conveyer*, stand before its own
*wanderer, emigrant*, as ἁγίζω's stand for ἁγιάζω. GEN 15 adds ὑπερασπίζω, *cover with a shield*, from the upsilon file; τριετίζω, *to be three years old*; and διχοτόμημα, *half of a thing cut in two*. GEN 17 adds κατάσχεσις, *holding back, restraining, retention*, then *possession*, from the kappa file; and ἑκατονταέτης, *of a hundred years*, *years old*, citing 17:17. GEN 18 adds μοσχάριον, *little calf*, and, from the beta file, βούτυρον, *butter*, then *a plant*. GEN 19 adds προσοίγνυμι, *shut*; ἀορασία, *inability to see, blindness*; γελοιάζω, *jest*, from the gamma file; ἐπαύριον, *on the morrow*; and εἰσσπάομαι, *draw into oneself*. GEN 20 adds μήτρα, *womb*, whose Middle Liddell entry tags only Latin; δίδραχμον, *coin of two drachms*, under δίδραχμος; and κἀγώ, *crasis for καὶ ἐγώ*. GEN 21 adds ἀπογαλακτίζω, *wean from the mother's milk*; ἀρχιστράτηγος, *commander-in-chief*; and, from the omega file, ὦμος, *the shoulder with the upper arm*.
<!-- LSJ sentences above -->

GEN 9 also files ἐμεθύσθη under μεθύσκω, *to make drunk*, where Middle Liddell gives its aorist
passive, though MorphGNT files the same form under μεθύω, *to be drunk*.

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
- **used:** GEN 2:8, GEN 2:18, GEN 5:1, GEN 5:3 (twice)

Like ἐπί, the entry heads all its cases together and its tagged translations do not separate
them. κατὰ ἀνατολάς is the idiom *eastward*, which the first sense does not give; the note
records the idiom and the reading prints the lexicon. κατʼ εἰκόνα at GEN 5:1 and κατὰ τὴν
ἰδέαν at 5:3 are *according to*, and are settled the same way.

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
- One sense each in GEN 5, so plain text: every numeral — `two hundred`, `thirty`, `a hundred`,
  `nine hundred` and the rest (*the Thirty*, *the Forty*, *the Three Hundred* name bodies of men,
  not further senses of the number) — with ὀκτώ `eight` and τρεῖς `three` from LSJ; ἔτος `years`,
  `of years`; υἱός `sons`, `a son`; θυγάτηρ `daughters`. δέκα πέντε (5:10), printed as two words,
  is `fifteen`, and the note says so.
- εἰμί of age (ἦν Νωε ἐτῶν πεντακοσίων, 5:32) — the state formula of GEN 1:2 in full.
- τὸ before an infinitive (μετὰ τὸ γεννῆσαι, 5:4 and after) — not printed, as with τοῦ at 2:5.
- GEN 6: ἄν and ἐάν after a relative or ὡς — `ever` (6:4, 6:17), as ἄν was at 2:17; the
  reflexives — `for themselves` (6:2, 6:4), `for yourself`, `yourself` (6:14, 6:19, 6:21);
  εἰμί — `are` (6:2), `being` (6:9), `is` and `may be` (6:17), `will be` (6:3, 6:19), `it will
  be` (6:21), and ἦσαν `were, and kept on being,` (6:4), the short formula, since the full one's
  *as* would stand beside ὡς's headword; δύο δύο — `two two` (6:19, 6:20).
- One sense each in GEN 6, so plain text: ἀσφαλτόω `you will smear with pitch` (6:14, LSJ);
  διώροφος `with two roofs or stories` (LSJ) and τριώροφος `of three stories or floors` (6:16);
  εἴκοσι `twenty`; θυγάτηρ `daughters`; υἱός `sons`.
- One sense each in GEN 7, so plain text: διατρέφω `to sustain continually` (7:3); ἑξακοσιοστός
  `six hundredth` (7:11, LSJ); μείς `month`; εἰκάς `twentieth`, *the twentieth day of the month*
  (7:11); ἡ ξηρά `the dry land` (7:22), the noun sense of ξηρός; ἐπάνω without a genitive —
  `upon, over, and atop` (7:20), and with one `over and atop` (7:18), the forms of GEN 1:2; ὕδωρ,
  `the water`, `of water` (7:6–24); ἐν τῷ ἑξακοσιοστῷ ἔτει — `in the six hundredth year` (7:11),
  ἐν joined to plain words as at 2:8.
- One sense each in GEN 8, so plain text: ἐλαττονόω `was being diminished` (8:3, 8:5, LSJ);
  θυρίς `the window` (8:6); θυσιαστήριον `an altar`, `the altar` (8:20); εὐωδία `of a sweet smell`
  (8:21). Ordinals stay plain as at 2:13 and 4:19, though δέκατος and πρῶτος have further senses,
  *a tithe*, *foremost*: `the tenth`, `the eleventh`, `the first` (8:5, 8:13), and `month`.
- ὁλοκάρπωσις — `whole burnt-offerings` (8:20): in neither Middle Liddell nor LSJ, which has only
  the verb ὁλοκαρπόομαι, *to be offered as a whole burnt-offering*. Plain text, as σφυροκόπος.
- εἷς as a numeral: ἐν τῷ ἑνὶ καὶ ἑξακοσιοστῷ ἔτει — `in the [[one]] and six
  hundredth year` (8:13); μιᾷ τοῦ μηνός — `[[one]] of the month`, the chain of GEN 2:21.
- One sense each in GEN 9, so plain text: κατακυριεύω `gain dominion over` (9:1); ἀμπελών `a
  vineyard` (9:20); οἶνος `of the wine` (9:21, 9:24), once *beer*, Middle Liddell's piece of
  *barley-wine, a kind of beer*, is left out; εὐλογητός `blessed` (9:26); ἐπικατάρατος `yet more accursed`, as
  at 3:14 (9:25); ὀπισθοφανῶς `backwards` (9:23, LSJ); numerals and `years` (9:28, 9:29).
- καὶ γάρ — `also for` (9:5): καί as *also*, γάρ plain as at 2:5.
- τὸ ὑμέτερον αἷμα — `the [[your]] [[blood]]` (9:5): the article plain before the adjective's
  unit, as before τὸ πρὸς ἑσπέραν at 8:11.
- ἦν of a standing relation (Χαμ ἦν πατὴρ Χανααν, 9:18) — the state formula of 1:2 in full; ἦσαν
  opening the verse — `were, and kept on being,` as at 6:4.

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

### Small words new in GEN 6

- ἡνίκα — **headword** `at which time`; **chain** `at which time, when, since, whenever`. 6:1.
- διά + accusative — **headword** `through`, the entry's first translation for that case;
  **chain** `through, throughout and over, during, by aid of and by means of, by reason of,
  because of, for the sake of`. 6:3, with the articular infinitive.
- ἐναντίον + genitive — **headword** `in the presence of`, the neuter used as a preposition inside
  the entry for ἐναντίος; **chain** `in the presence of, before, opposite and face to face,
  against`. 6:8, 6:11, 6:13.
- ὑποκάτω — **headword** `below`; **chain** `below, under`. 6:17.
- ὅσος — **headword** `as great as`, after Perseus's Latin *quantus*, left out; **chain** `as great
  as, as much as, as far as, as long as, as many as`. 6:17, 6:22.
- οὖν — **headword** `really`; **chain** `really, at all events, surely, so, then and therefore`.
  6:14.
- τις — **headword** `any one`; **chain** `any one, some one, many a one, each one, every man`. 6:5.
- ἐπιμελῶς — **headword** `carefully`, the adverb of ἐπιμελής, *careful*; **chain** `carefully,
  anxiously, attentively`. 6:5.
- ἔσωθεν, ἔξωθεν, ἄνωθεν — `from within` / `from within, within`; `from without` / `from without,
  outside, without and free from`; `from above` / `from above, from on high, from the upper
  country, above and on high, from the beginning, by descent, over again and anew`. 6:14, 6:16.
- ἐκεῖνος — `those`, `that`, `to those` / `those, the ones there, the more remote`, in the form:
  the chain of GEN 2:12. 6:4, 6:21.
- καθά — **headword** `according as`; **chain** `according as, just as, like as if, exactly as`.
  7:9, 7:16.
- ἔτι — **headword** `yet`, the chain of GEN 2:9. 7:4.
- σφόδρα, σφοδρῶς — `very` / `very, very much, exceedingly, violently, far, most certainly`;
  `vehemently` / `vehemently, violently, excessively, impetuously, strongly and robustly`, the
  adverb of σφοδρός, *vehement*. 7:18, 7:19.
- ἔξωθεν with a genitive — `from without`, the chain of GEN 6:14. 7:16.

### Small words new in GEN 9

- πλήν without a genitive — **headword** `but`, the entry's first sense as an adverb; *more than,
  except, save* are the preposition's, with the genitive, and stand last; **chain** `but, than,
  much like, only not, except that, save that, except, save so far as, more than, save, short of`.
  9:4.
- ὥστε with the infinitive — **headword** `so as to`, the first conjunction sense; **chain** `so as
  to, as to, on the condition that, and so and therefore and consequently, as and as being, since
  it was`. 9:15.
- ἀντί + genitive — **headword** `over against`, sense 0, *over against, opposite*; Perseus's
  summary and the senses *IN COMPOS.* are skipped by name; **chain** `over against, opposite,
  instead and in the place of, as good as and equal to, at the price of and for, for the sake of,
  set against and compared with`. 9:6, and 2:21 and 4:25, whose chain first stopped at *as good
  as*, the fifth of the senses a word card shows.
- ὑπό + accusative — **headword** `towards and under`, the entry's first translation for that case;
  **chain** `towards and under, under and into, under and before, under, in subjection, towards,
  about, about the time, to a certain degree and in some measure`. 9:2, ὑπὸ χεῖρας.
- ἔξω without a genitive — **headword** `out`; **chain** `out, out of, outside, without, foreign,
  clear of, beyond and over, but and except`. 9:22.
- ὑμέτερος — **headword** `your`; **chain** `your, yours, your part and your business, your
  character`. 9:5.
- ἐν with an articular infinitive — ἐν τῷ συννεφεῖν με — `in the collecting clouds` / `within,
  inside of, and by means of the collecting clouds, the being cloudy, the wearing a clouded look`,
  then `of me` (9:14): joined, as ἐν always is, with the infinitive's subject in the genitive's
  English, as at 4:8.
- τοῦ with an infinitive (τοῦ καταφθεῖραι 9:11, τοῦ μνησθῆναι 9:16) — not printed, as at 2:5.

### Small words new in GEN 10

- ὅθεν — **headword** `from whom`: Perseus leaves the entry's first gloss, *whence, from which*,
  untagged, and the first it tags is *from whom*; **chain** `from whom, from whatever source and in
  what manner soever, where, whence and wherefore`. 10:14.
- ἕως before an infinitive with no article (ἕως ἐλθεῖν, 10:19, 10:30) — `until`, the chain of GEN
  3:19; ἕως Λασα (10:19) the same.
- ἕκαστος — **headword** `every`; **chain** `every, every one, each, each one, all and each one,
  singly and by itself, each by himself`. 10:5.
- καί as *also* (καὶ αὐτῷ, 10:21) — `also`, plain, as at 3:6.
- One sense each in GEN 10, so plain text: νῆσος `islands` (10:5, 10:32), once the etymology *to
  swim, floating land* is left out; πρωτότοκος `first-born` (10:15), as at 4:4; κατοίκησις `the
  settling in` (10:30); δύο `two`; υἱός `sons`.
- The article before a people's name (τοὺς Λουδιιμ, τὸν Χετταῖον, τῶν Χαναναίων) is not printed,
  as before a person's name.

### Words new in GEN 21

- ἐπισκέπτομαι — Middle Liddell's entry reads *a pres., which furnishes its tenses to ἐπισκοπέω*;
  that entry's senses, first *to look upon* or *at, inspect, observe*, then *to visit*. 21:1.
- φαίνω in the passive — the active's *to bring to light, make to appear* first, and the entry's
  *Pass. to come to light, be seen, appear* last: `was brought to light`. 21:11.
- πλανάω in the passive — likewise, the active's *to make to wander* first, the passive's *to
  wander, roam about, stray* last. 21:14.
- ὦμος — tagged in Middle Liddell only in Latin; LSJ, from the omega file, *the shoulder with the
  upper arm*. 21:14.
- Φρέαρ ὁρκισμοῦ — the second name the verse gives a well, glossed as a name as at 16:14:
  `(Φρέαρ, "a well", the first word of the name the verse gives the place, for Hebrew Bĕʾēr
  šebaʿ)`; ὁρκισμός after it plain. 21:31.
- Θεὸς αἰώνιος — the capital Rahlfs prints for the name called upon, listed in `speech`; θεός
  anarthrous, qualitative, as at 17:7. 21:33.
- The perfect ἐπακήκοεν, `has listened and it stands so` (21:17).
- One sense each in GEN 21, so plain text: γῆρας `the old age` (21:2, 21:7); ἀπογαλακτίζω `was weaned
  from the mother's milk` (21:8, LSJ); νυμφαγωγός `the leader of the bride`, ἀρχιστράτηγος `the
  commander-in-chief` (21:22, 21:32); ἀμνάς `lambs` (21:28–30); ὁρκισμός `of administration of an
  oath` (21:31).

| lemma | headword | chain | used |
| --- | --- | --- | --- |
| αὐξάνω | `was made large` | `was made large, was increased and augmented, was increased in power and strengthened and exalted, was promoted to honour and glorified and magnified, grew and waxed and increased, grew up` | 21:8, 21:20 |
| βολή | `a throw` | `a throw, the stroke and wound, a glance` | 21:16 |
| γέλως | `laughter` | `laughter, occasion of laughter and matter for laughter` | 21:6 |
| γίνομαι | `having come into being` | `having come to be, having arisen, having been brought into existence` | 21:3 |
| διατίθεμαι | `arranged as they liked` | `arranged as they liked, disposed of, disposed of their property and devised it by will, set out for sale and disposed of, arranged mutually, made a covenant with, settled with` | 21:27, 21:32 |
| δοχή | `a receptacle` | `a receptacle, a reception and entertainment` | 21:8 |
| δύναμις | `of the power` | `of the power, of the might, of the strength, of the ability, of the authority, of the force for war and forces, of the quantity, of the faculty and capacity, of the force and meaning, of the worth and value` | 21:22, 21:32 |
| εἰσακούω | `hearkened` | `hearkened and gave ear to, heard, hearkened to and gave heed to` | 21:17 |
| εἷς | `of one` | `of one, of a single one, of one alone` | 21:15 |
| θάνατος | `the death` | `the death, the death threatened, the sentence of death` | 21:16 |
| θηλάζω | `suckles` | `suckles, sucks` | 21:7 |
| καθίζω | `made to sit down` | `made to sit down, seated, set and placed, encamped, set up, sat down and was seated and took her seat, settled and sank in` | 21:16 |
| κλαίω | `wept` | `wept, lamented, wailed, wept for` | 21:16 |
| κρατέω | `be strong` | `be strong, be mighty, be powerful, rule and hold sway and be sovereign, rule among, be lord and master of and ruler over, conquer and prevail and get the upper hand, prevail and become current, prevail over, surpass and go beyond, conquer and master and outdo and surpass, become master of and get possession of, lay hold of, seize and hold fast, control and command` | 21:18 |
| λέγω | `may say` | `may say, may speak, may declare, may call by name, may tell` | 21:12 |
| μακρόθεν | `from afar` | `from afar, from long since` | 21:16 |
| μαρτύριον | `a testimony` | `a testimony, a proof` | 21:30 |
| πίμπλημι | `filled full of` | `filled full of, filled with, filled up, filled, filled and discharged` | 21:19 |
| παίζω | `playing like a child` | `playing like a child, sporting, playing, dancing, sporting and jesting and joking, making sport of and mocking, playing with` | 21:9 |
| παιδίον | `of the young child` | `of the young child, of the slave-lad` | 21:12, 21:16, 21:17, 21:20 |
| παιδίον | `the young child` | `the young child, the slave-lad` | 21:8, 21:14, 21:15, 21:16, 21:18, 21:19 |
| παιδίσκη | `of the young girl` | `of the young girl, of the maiden, of the young slave, of the courtesan` | 21:10, 21:12, 21:13 |
| παροικέω | `you dwelt beside` | `you dwelt beside, you dwelt along the coast of, you lived near, you dwelt among, you lay near, you lived in and sojourned` | 21:23 |
| πλανάω | `was being made to wander` | `was being made to wander and led wandering about, was being led from the subject, was being led astray and misled and deceived, was wandering and roaming about and straying, was wandering over, was wandering abroad, was wandering and digressing, was wandering in mind and at a loss` | 21:14 |
| πρᾶγμα | `that which has been done` | `that which has been done, the deed, the act, anything necessary and expedient, the thing of consequence and importance, the action and affair, the thing and the business` | 21:26 |
| σκληρός | `hard` | `hard, harsh and crashing, stiff and unyielding, stiff and sturdy, austere and severe` | 21:11, 21:12 |
| συγχαίρω | `will rejoice with` | `will rejoice with, will take part in joy, will wish joy and congratulate` | 21:6 |
| σός | `thy` | `thy, thine` | 21:13 |
| τίκτω | `I brought into the world` | `I brought into the world, I brought forth, I bore, I produced` | 21:7 |
| τοξότης | `a bowman` | `a bowman, archer, the Archer and Sagittarius, the city-guard` | 21:20 |
| τόξον | `of bow` | `of bow, of bow and arrows, of rays` | 21:16 |
| φαίνω | `was brought to light` | `was brought to light and made to appear, was shown forth and made known and revealed and disclosed and shown, was made clear and explained and expounded, was informed against and indicted and impeached, was proclaimed, came to light and was seen and appeared, shone brightly, came into being, appeared to be, was manifest` | 21:11 |
| φρέαρ | `a well` | `a well, a tank and cistern and reservoir, an oil jar` | 21:19 |
| φρέαρ | `of the wells` | `of the wells, of the tanks and cisterns and reservoirs, of the oil jars` | 21:25 |
| φρέαρ | `to the well` | `to the well, to the tank and cistern and reservoir, to the oil jar` | 21:33 |
| φρέαρ, with ἐν | `in the well` | `within, inside of, and by means of the well, the tank and cistern and reservoir, the oil jar` | 21:32 |
| χείρ | `with the hand` | `with the hand, with the hand and arm, with the arm` | 21:18 |
| ἀδικέω | `to do wrong` | `to do wrong, to do one wrong and wrong and injure, to spoil and damage` | 21:23 |
| ἀκούω | `may hear` | `may hear, may have hearing of, may hear tell of, may hearken and give ear, may listen to and obey` | 21:6 |
| ἀμφότερος | `each` | `each, both of two` | 21:27, 21:31 |
| ἀναβοάω | `having shouted aloud` | `having shouted aloud, having uttered a loud cry, having called out, having cried out, having wailed aloud over, having called on` | 21:16 |
| ἀναγγέλλω | `will carry back tidings of` | `will carry back tidings of, will report` | 21:7 |
| ἀπέρχομαι | `having gone away` | `having gone away, having departed from, having departed, having departed from life` | 21:14, 21:16 |
| ἀσκός | `a leathern-bag` | `a leathern-bag, a wine-skin, a bladder` | 21:14 |
| ἀσκός | `of the leathern-bag` | `of the leathern-bag, of the wine-skin, of the bladder` | 21:15 |
| ἀσκός | `the leathern-bag` | `the leathern-bag, the wine-skin, the bladder` | 21:19 |
| ἀφαιρέω | `took away for themselves` | `took away for themselves, took away, prevented and hindered from` | 21:25 |
| ἄρουρα | `tilled land` | `tilled land, arable land, seed-land, cornland, land and earth, a woman as bearing children, a measure of land` | 21:33 |
| ἐκβάλλω | `throw` | `throw, cast out of, throw out, cast out and banish, depose, throw away and reject` | 21:10 |
| ἐλάτη | `of silver fir` | `of silver fir, of an oar, of a ship and boat` | 21:15 |
| ἐλέγχω | `disgraced` | `disgraced, put to shame, cross-examined and questioned, censured and accused, brought to the proof and disproved and confuted, brought convincing proof, proved` | 21:25 |
| ἐπακούω | `has listened` | `has listened and it stands so, has hearkened to and heard and it stands so, has given ear and hearkened and it stands so, has obeyed and it stands so` | 21:17 |
| ἐπισκέπτομαι | `looked upon` | `looked upon, looked at, inspected, observed, examined, regarded, watched over, visited, inspected and reviewed, considered and reflected, examined with himself and meditated` | 21:1 |
| ἐπιστρέφω | `turned about` | `turned about, turned round, returned, turned towards, corrected and made to repent` | 21:32 |
| ἐπιτίθημι | `laid` | `laid, put, placed upon, applied, set up, put on, put to and shut, put to and granted and gave besides, added and brought on, imposed and inflicted, dispatched, gave` | 21:14 |
| ἡμέρα | `to day` | `to day, to day-break, to time` | 21:8 |
| ἵστημι | `you made to stand` | `you made to stand, you set, you stopped and stayed and checked, you set up and raised, you established and instituted, you appointed, you weighed` | 21:29 |
| ὀρύσσω | `I dug` | `I dug, I dug up, I dug through and made a canal through, I buried` | 21:30 |
| ὁράω | `I may see` | `I may see, I may perceive, I may behold, I may look at` | 21:16 |
| ὄμνυμι | `I will swear` | `I will swear, I will swear to and affirm and confirm by oath, I will swear that one will, I will swear by` | 21:24 |
| ὄμνυμι | `swear` | `swear, swear to and affirm and confirm by oath, swear that one will, swear by` | 21:23 |
| ὄμνυμι | `swore` | `swore, swore to and affirmed and confirmed by oath, swore that one would, swore by` | 21:31 |
| ὅρκος | `of the object by which one swears` | `of the object by which one swears, of the witness of an oath, of the oath` | 21:14, 21:32, 21:33 |
| ὦμος | `the shoulder with the upper arm` | `the shoulder with the upper arm, the shoulder` | 21:14 |
| ῥίπτω | `threw` | `threw, cast, hurled, threw and tossed about, cast out, threw off and away, threw away and wasted, cast lots, threw and cast herself down, flung herself` | 21:15 |

### Words new in GEN 20

- κἀγώ — LSJ gives the crasis no gloss, only *crasis for καὶ ἐγώ*; the two words' senses stand,
  `and I`, plain. 20:6.
- μήτρα — Middle Liddell tags nothing but the Latin *matrix*, so LSJ's senses stand, first *womb*.
  20:18.
- δίδραχμον — no Middle Liddell entry; LSJ files it under δίδραχμος, *coin of two drachms*,
  *half-shekel*. 20:14, 20:16.
- προφήτης — its first appearance in the Greek Bible; Middle Liddell is first *one who speaks for a
  God and interprets his will to man, a prophet*, with the New Testament's *an inspired preacher and
  teacher*, *the revealer of God's counsel for the future* last. 20:7.
- The perfect participle with the formula — συνῳκηκυῖα `having dwelt together and standing so`
  (20:3); the perfect πεποίηκας `you have made and it stands made` (20:9).
- ἐν καθαρᾷ καρδίᾳ — ἐν joined to the adjective, καθαρός, the chain of GEN 7:2; καρδία anarthrous
  drops the lexicon's *the*, as γαστήρ at 16:4. 20:5, 20:6.
- τὰ σά — the chain of GEN 14:23, `the thy property`, with the article. 20:7.
- One sense each in GEN 20, so plain text: λίψ `south-west wind` (20:1); ἀδελφή `sister` (20:2,
  20:5, 20:12); χίλιοι `a thousand` (20:14, 20:16); ἀληθεύω `speak truth` (20:16).

| lemma | headword | chain | used |
| --- | --- | --- | --- |
| βασιλεία | `the kingdom` | `the kingdom, the dominion, the hereditary monarchy` | 20:9 |
| γινώσκω | `I learned to know` | `I learned to know, I perceived, I marked, I learned, I discerned and distinguished` | 20:6 |
| γινώσκω | `learn to know` | `learn to know, perceive, mark, learn, discern and distinguish` | 20:7 |
| δίδραχμον | `coins of two drachms` | `coins of two drachms, half-shekels` | 20:14, 20:16 |
| δικαιοσύνη, with ἐν | `in righteousness` | `within, inside of, and by means of righteousness, justice` | 20:5 |
| εἰσέρχομαι | `we may go in` | `we may go in, we may go into and enter, we may come into, we may come in, we may come upon` | 20:13 |
| ζάω | `you will live` | `you will live, you will be in full life and strength, you will be fresh and strong` | 20:7 |
| θεοσέβεια | `the service of God` | `the service of God, the fear of God, religiousness` | 20:11 |
| καθαρός, with ἐν | `in clear of dirt` | `within, inside of, and by means of clear of dirt, clean and spotless and unsoiled, clear and open and free, clear from shame and pollution and pure, clear of admixture, genuine` | 20:5, 20:6 |
| καρδία | `heart` | `heart, stomach` | 20:5, 20:6 |
| κατοικέω | `dwell in` | `dwell in, settle in, colonise, inhabit, settle and dwell, lie and be situate` | 20:15 |
| κινέω | `set in motion` | `set in motion, moved, removed, meddled with, applied, changed and innovated, roused and disturbed, stirred up and aroused and urged on, set agoing and caused and called` | 20:1 |
| λέγω | `I said` | `I said, I spoke, I declared, I called by name, I told` | 20:11, 20:13 |
| λέγω | `to say` | `to say, to speak, to declare, to call by name, to tell` | 20:2 |
| λαμβάνω | `you took` | `you took, you received, you took hold of and grasped and seized` | 20:3 |
| μήτηρ | `of mother` | `of mother, of dam, of source` | 20:12 |
| μήτρα | `womb` | `womb, the cervix including the orifice of the womb, matrix, source and origin, core and heart-wood, diseased condition, queen-wasp` | 20:18 |
| οὖς | `the ears` | `the ears, the handles` | 20:8 |
| παιδίσκη | `the young girls` | `the young girls, the maidens, the young slaves, the courtesans` | 20:17 |
| παροικέω | `dwelt beside` | `dwelt beside, dwelt along the coast of, lived near, dwelt among, lay near, lived in and sojourned` | 20:1 |
| πατήρ | `of father` | `of father, of grandfather` | 20:12 |
| ποιέω | `will make` | `will make, will do, will produce, will create` | 20:9 |
| ποιέω | `you have made` | `you have made and it stands made, you have done and it stands done, you have produced and it stands produced, you have created and it stands created` | 20:9 |
| προσεύχομαι | `offered prayers` | `offered prayers and vows, addressed in prayer, offered prayers and worshipped, prayed for` | 20:17 |
| προσεύχομαι | `will offer prayers` | `will offer prayers and vows, will address in prayer, will offer prayers and worship, will pray for` | 20:7 |
| προφήτης | `one who speaks for a God and interprets his will` | `one who speaks for a God and interprets his will, a prophet, an interpreter and declarer, an inspired preacher and teacher, the revealer of God's counsel for the future, a predicter of future events` | 20:7 |
| συγκλείω | `shutting` | `shutting and cooping up and hemming in and enclosing, setting together to fight as in the lists, shutting close and closing, locking, closing up, being well linked` | 20:18 |
| συνοικέω | `having dwelt together` | `having dwelt together and standing so, having lived with and standing so, having lived together and cohabited and standing so, having clung closely and standing so, having colonised jointly with and standing so` | 20:3 |
| σός | `the thy property` | `the thy property, the thy interests, the thy and thine and of thee` | 20:7 |
| τιμή | `that which is paid in token of worth` | `that which is paid in token of worth and value, worship and esteem and honour, honour and dignity and lordship, the prerogative, a dignity and office and magistracy, an authority and magistracy, a present of honour and offering, a reward and present, worth and value and price, payment, an estimate, compensation, the penalty, a valuation` | 20:16 |
| τόπος | `place` | `place, local circumstances, position, passage in a book, topic, common-place, occasion and opportunity` | 20:13 |
| τόπος, with ἐν | `in the place` | `within, inside of, and by means of the place, the local circumstances, the position, the passage in a book, the topic, the common-place, the occasion and opportunity` | 20:11 |
| φείδομαι | `I spared` | `I spared, I did not destroy, I was merciful, I refrained from using and used sparingly, I was sparing and was thrifty and lived thriftily, I drew back from, I ceased, I forbore` | 20:6 |
| φοβέομαι | `were put to flight` | `were put to flight, fled affrighted, fled, were seized with fear, were affrighted, feared` | 20:8 |
| χείρ | `of hands` | `of hands, of hands and arms, of arms` | 20:5 |
| ἀγνοέω | `not perceiving` | `not perceiving, not knowing, being ignorant of, going wrong and making a false step` | 20:4 |
| ἀδελφός | `son of the same mother` | `a son of the same mother, a brother, a near kinsman` | 20:5, 20:13 |
| ἀνήρ | `to a man` | `to a man, to a man in the prime of life` | 20:3 |
| ἀποδίδωμι | `gave up` | `gave up, gave back, restored, returned, rendered what is due and paid, returned and rendered and yielded, suffered and allowed, rendered, delivered over and gave up, delivered, rendered and gave in, gave an account of, increased` | 20:14 |
| ἀποδίδωμι | `give up` | `give up, give back, restore, return, render what is due and pay, return and render and yield, suffer and allow, render, deliver over and give up, deliver, render and give in, give an account of, increase` | 20:7 |
| ἀποδίδωμι | `you give up` | `you give up, you give back, you restore, you return, you render what is due and pay, you return and render and yield, you suffer and allow, you render, you deliver over and give up, you deliver, you render and give in, you give an account of, you increase` | 20:7 |
| ἀποθνήσκω | `you die off` | `you die off, you die, you are put to death, you are slain` | 20:3 |
| ἀποκτείνω | `they may kill` | `they may kill, they may slay, they may condemn to death` | 20:2 |
| ἀφίημι | `I sent forth` | `I sent forth, I discharged, I sent away and let go, I set free, I released` | 20:6 |
| ἁμαρτάνω | `to miss the mark` | `to miss the mark, to fail of one's purpose, to go wrong, to err, to sin` | 20:6 |
| ἁμαρτάνω | `we missed the mark` | `we missed the mark, we failed of our purpose, we went wrong, we erred, we sinned` | 20:9 |
| ἁμαρτία | `a failure` | `a failure, a fault and sin, guilt and sin` | 20:9 |
| ἄνθρωπος | `to the man` | `to the man, to the human being` | 20:7 |
| ἅπτω | `fastened himself to` | `fastened himself to, clung to, hung on by, laid hold of, grasped, touched` | 20:4 |
| ἅπτω | `to fasten oneself to` | `to fasten oneself to, to cling to, to hang on by, to lay hold of, to grasp, to touch` | 20:6 |
| ἐνοράω | `having seen` | `having seen, having remarked, having observed, having looked at and upon` | 20:10 |
| ἐπάγω | `you brought on` | `you brought on, you brought upon, you set on and urged on, you led on, you brought in and invited, you brought to, you laid on and applied, you brought forward, you added` | 20:9 |
| ἔργον | `work` | `work, business, deeds, action, works of industry and tilled lands` | 20:9 |
| ἰάομαι | `healed` | `healed, cured` | 20:17 |
| ὕπνος | `sleep` | `sleep, slumber, the sleep of death, Sleep` | 20:6 |
| ὕπνος, with ἐν | `in sleep` | `within, inside of, and by means of sleep, slumber, the sleep of death, Sleep` | 20:3 |

### Words new in GEN 19

- ἐν τῷ with the infinitive — `in the sparing` (19:16), `in the rubbing out` and `in the turning
  down` (19:29), `in the falling asleep` (19:33, 19:35): the article inside the ἐν unit and the
  infinitive as a noun in *-ing*, as ἐν τῷ κινῆσαι is `in the setting in motion` at 11:2; the
  infinitive's subject follows, `lord`, `her`.
- σῴζω — filed under σώζω, first *to save, keep*. The passive takes the entry's passive *to come
  safe, escape to* last; the middle imperative σῴζου takes the middle, *to keep* or *preserve for
  oneself*. 19:17, 19:20, 19:22.
- δέομαι — filed under the second δέω, *to lack*; the deponent's senses stand, *to be in want* or
  *need*, *to ask for*, *to beg*. 19:18.
- μᾶλλον — the comparative, filed inside μάλα: *more*, then *more and more, still more*, *much
  more*, *rather*. ἤ — first *or*; its comparative *than, as* follows. 19:9.
- τὰ κακά — κακός as a noun, the entry's substantive *evil, ill*, with *evil words, reproaches*.
  19:19.
- περίοικος, τὴν περίοικον — the singular takes the adjective's *dwelling round*; *neighbours* is the
  plural's. περίχωρος as an adjective after the repeated article, `the round about a place`
  (19:28); as a noun, ἡ περίχωρος, the chain of GEN 13:10 (19:17). 19:25, 19:29.
- γαμβρός — first *any one connected by marriage*; in the plural, `ones connected by marriage`, the
  lexicon's *any* dropped as *a* is. 19:12, 19:14.
- ἀπό + μικρός, ἕως + μέγας — the adjectives as the entry gives them, in the genitive. 19:11.
- The instrumental dative takes `with` — ἀορασίᾳ `with inability to see` (19:11), as θανάτῳ is
  `with death` at 3:4 and τοῖς ὀφθαλμοῖς `with the eyes` at 13:14 and 18:2.
- εἰσσπάομαι — LSJ's one translation, *draw into oneself*, written as a unit whose chain is the
  headword alone, because the verse's εἰς is also *into*, and plain text would put that headword
  outside its unit. 19:10.
- Names: Σοδομῖται `(Σοδομῖται, the men of Σόδομα, Sodom)`; Μωαβ, and Μωαβιτῶν `(Μωαβῖται, the
  people of Μωαβ, Moab)`; Αμμαν `(Αμμαν, for Hebrew Ben-ʿammî, "son of my people")`, anchored
  Ammon, the people's name the Greek form matches, and Αμμανιτῶν. The article before a people's
  name is not printed. 19:4, 19:37, 19:38.
- One sense each in GEN 19, so plain text: καταβιάζομαι `was constraining` (19:3); ἄζυμος
  `unleavened` (19:3); νεανίσκος `of a youth` (19:4); προσοίγνυμι `shut` (19:6, LSJ); παραβιάζομαι
  `were using violence to` (19:9); γελοιάζω `to jest` (19:14, LSJ); ἐπισπουδάζω `were making haste
  in`, συναπόλλυμι's middle `you may perish together`, ἀνομία `to the lawlessnesses` (19:15); θεῖον
  `brimstone` (19:24); ἐπαύριον `on the morrow` (19:34, LSJ); χθές `yesterday` (19:34); σήμερον
  `to-day` (19:37, 19:38).

| lemma | headword | chain | used |
| --- | --- | --- | --- |
| γαμβρός | `of the ones connected by marriage` | `of the ones connected by marriage, of the sons-in-law, of the brothers-in-law and sisters' husbands, of the wives' brothers, of the fathers-in-law, of the bridegrooms and wooers and suitors` | 19:14 |
| γαμβρός | `ones connected by marriage` | `ones connected by marriage, sons-in-law, brothers-in-law and sisters' husbands, wives' brothers, fathers-in-law, bridegrooms and wooers and suitors` | 19:12 |
| γαμβρός | `the ones connected by marriage` | `the ones connected by marriage, the sons-in-law, the brothers-in-law and sisters' husbands, the wives' brothers, the fathers-in-law, the bridegrooms and wooers and suitors` | 19:14 |
| γῆ | `to the earth` | `to the land, to the dry ground, to the terrestrial realm` | 19:31 |
| δέομαι | `I am in want` | `I am in want and need, I stand in need of, I ask for and from, I beg` | 19:18 |
| δεῦρο | `hither` | `hither, here and on and come on, up to this point, until now and up to this time and hitherto` | 19:32 |
| διασῴζω | `to be preserved through` | `to be preserved through, to be preserved and maintained, to be kept in mind, to come safe through and arrive in safety, to recover` | 19:19 |
| δικαιοσύνη | `the righteousness` | `the righteousness, the justice` | 19:19 |
| δοκέω | `thought` | `thought, supposed, imagined, expected, had and formed an opinion, was determined and resolved, seemed and pretended, seemed, seemed good` | 19:14 |
| δοκός | `of the bearing-beams` | `of the bearing-beams, of the balks and beams, of the bars` | 19:8 |
| δύναμαι | `I will be able` | `I will be able, I will be capable and strong enough, I will be powerful and mighty, I will have influence, I will dare and bear, I will pass for, I will be worth, I will be equivalent to, I will signify and mean, I will avail` | 19:19, 19:22 |
| εἰσέρχομαι | `having gone in` | `having gone in, having gone into and entered, having come into, having come in, having come upon` | 19:5, 19:33, 19:34, 19:35 |
| ζάω | `to live` | `to live, to be in full life and strength, to be fresh and strong` | 19:19 |
| ζητέω | `seeking` | `seeking, seeking for, enquiring for and asking about, searching after and searching out, searching and inquiring into and investigating, requiring and demanding, seeking after and desiring, seeking to, having to seek and feeling the want of` | 19:11 |
| θαυμάζω | `I wondered` | `I wondered, I marvelled, I was astonied, I looked on with wonder and amazement, I wondered at and marvelled at, I honoured and admired and worshipped` | 19:21 |
| κάθημαι | `was being seated` | `was being seated, was being seated in court, was sitting still and sitting quiet, was sitting and lying idle, was sitting down and lying, was leading a sedentary life, was being settled` | 19:1, 19:30 |
| κάμινος | `of an oven` | `of an oven, of a furnace, of a kiln` | 19:28 |
| καθήκω | `has come` | `has come and gone down, comes down to and comes and reaches to, has come to, is meet and fit and proper, belongs to, beseems` | 19:31 |
| κακός | `the evils` | `the evils, the ills, the evil words and reproaches` | 19:19 |
| κακόω | `we will treat ill` | `we will treat ill and maltreat and afflict and distress, we will spoil and ruin, we will suffer ill and be in ill plight and be distressed` | 19:9 |
| καταλαμβάνω | `may seize upon` | `may seize upon, may lay hold of, may seize and overpower, may seize with the mind and apprehend and comprehend, may catch and overtake and come up with, may overtake and befall, may surprise and catch and find, may repress and arrest and check, may put an end to, may bind, may force and compel to do` | 19:19 |
| καταλύω | `put down` | `put down, destroy, dissolve and break up, depose, dismiss and disband, neglect, end and bring to an end, break, make peace with, unloose and unyoke, take down, take up your quarters and lodge, go and lodge, take your rest` | 19:2 |
| καταλύω | `we will put down` | `we will put down, we will destroy, we will dissolve and break up, we will depose, we will dismiss and disband, we will neglect, we will end and bring to an end, we will break, we will make peace with, we will unloose and unyoke, we will take down, we will take up our quarters and lodge, we will go and lodge, we will take our rest` | 19:2 |
| καταστρέφω | `to turn down` | `to turn down and trample on, to turn the soil, to upset and overturn, to subject to oneself and subdue, to turn back and bring back, to turn round and bring to an end, to come to an end and die, to twist up` | 19:21 |
| καταστρέφω | `turned down` | `turned down and trampled on, turned the soil, upset and overturned, subjected to himself and subdued, turned back and brought back, turned round and brought to an end, came to an end and died, twisted up` | 19:25 |
| καταστρέφω, with ἐν τῷ | `in the turning down` | `within, inside of, and by means of the turning down and trampling on, the turning the soil, the upsetting and overturning, the subjecting to oneself and subduing, the turning back and bringing back, the turning round and bringing to an end, the coming to an end and dying, the twisting up` | 19:29 |
| καταστροφή | `of the overturning` | `of the overturning, of the subduing and subjugation and reduction, of the sudden turn and end, of the close and conclusion, of the catastrophe` | 19:29 |
| καταφεύγω | `to flee for refuge` | `to flee for refuge, to flee and take refuge, to flee for protection, to escape, to have recourse to, to fall back upon and appeal to` | 19:20 |
| κοιμάω | `I fell asleep` | `I fell asleep, I went abed and lay abed, I slept, I fell asleep and died, I kept watch at night` | 19:34 |
| κοιμάω | `fall asleep` | `fall asleep, go abed and lie abed, sleep, fall asleep and die, keep watch at night` | 19:34 |
| κοιμάω | `fell asleep` | `fell asleep, went abed and lay abed, slept, fell asleep and died, kept watch at night` | 19:33, 19:35 |
| κοιμάω | `let us fall asleep` | `let us fall asleep, let us go abed and lie abed, let us sleep, let us fall asleep and die, let us keep watch at night` | 19:32 |
| κοιμάω | `to fall asleep` | `to fall asleep, to go abed and lie abed, to sleep, to fall asleep and die, to keep watch at night` | 19:4 |
| κοιμάω, with ἐν τῷ | `in the falling asleep` | `within, inside of, and by means of the falling asleep, the going abed and lying abed, the sleeping, the falling asleep and dying, the keeping watch at night` | 19:33, 19:35 |
| κρίνω | `to pick out` | `to pick out and choose, to pick out for oneself and choose, to decide, to judge, to adjudge, to judge of and estimate, to expound and interpret, to determine, to question, to bring to trial and accuse, to pass sentence upon and condemn` | 19:9 |
| κρατέω | `were strong` | `were strong, were mighty, were powerful, ruled and held sway and were sovereign, ruled among, were lords and masters of and rulers over, conquered and prevailed and got the upper hand, prevailed and became current, prevailed over, surpassed and went beyond, conquered and mastered and outdid and surpassed, became masters of and got possession of, laid hold of, seized and held fast, controlled and commanded` | 19:16 |
| κύριος | `lords` | `lords, masters, the ones having power and authority over` | 19:2 |
| λέγω | `were saying` | `were saying, were speaking, were declaring, were calling by name, were telling` | 19:5 |
| λαλέω | `you talked` | `you talked, you chatted, you prattled, you babbled, you said, you talked of, you spoke, you chattered, you chirped` | 19:21 |
| λαμβάνω | `having taken` | `having taken and holding so, having received and holding so, having taken hold of and grasped and seized and holding so` | 19:14 |
| μέγας | `of big` | `of big, of great, of tall, of full-grown, of vast and high, of spacious and wide, of strong and mighty, of violent, of loud, of prevailing, of weighty and important` | 19:11 |
| μέσος | `of middle` | `of the middle, of in the middle, of the centre, of mid, of between two` | 19:29 |
| μήποτε | `that at no time` | `that at no time, lest ever` | 19:17 |
| μεγαλύνω | `you made great` | `you made great and powerful, you exalted and strengthened, you made great by word and extolled and magnified, you aggravated` | 19:19 |
| μηδείς | `and not one` | `and not one, not even one, nobody and naught and good for naught, naught and nothing, a good for naught, not at all and by no means` | 19:8 |
| μικρός | `of small` | `of small, of little, of petty and trivial and slight, of short` | 19:11 |
| μικρός | `small` | `small, little, petty and trivial and slight, short` | 19:20 |
| μόνος | `alone` | `alone, only` | 19:8 |
| μᾶλλον | `more` | `more, more and more and still more, much more, rather` | 19:9 |
| νίπτω | `wash the hands` | `wash the hands, purge and cleanse, wash off` | 19:2 |
| νύξ, with ἐν | `in the night-season` | `within, inside of, and by means of the night-season, the night, the watches of the night, the dark of night, the night of death` | 19:33, 19:35 |
| οἰκία | `the building` | `the building, the house, the dwelling, the household and domestic establishment, the household and inmates of the house, the house and family from which one is descended` | 19:3, 19:4 |
| οὐδείς | `and not one` | `and not one, no one, none, naught and good for naught` | 19:31 |
| πέσσω | `softened` | `softened, ripened, changed, cooked and dressed and baked, digested, cherished and nursed, enjoyed` | 19:3 |
| παρά + genitive | `from the side of` | `from the side of, from beside, from, near` | 19:24 |
| παραλύω | `were loosed from the side` | `were loosed from the side, were taken off and detached, were undone and put an end to, were unyoked and parted from, were set free, were loosed beside, were parted from, were exempt, were disabled at the side and paralysed, were exhausted and flagged` | 19:11 |
| περίχωρος | `round about a place` | `round about a place, the people about, the country round about` | 19:28 |
| περιβλέπω | `you may look round about` | `you may look round about, you may gaze around, you may look round at, you may seek after and look about for, you may gaze on and admire and respect, you may be jealous of and suspect, you may covet` | 19:17 |
| περικυκλόω | `encircled` | `encircled, encompassed, went round` | 19:4 |
| πλατεῖα, with ἐν | `in the street` | `within, inside of, and by means of the street, the flat of the hand` | 19:2 |
| ποιέω | `you make` | `you make, you do, you produce, you create` | 19:19 |
| ποιέω | `you may make` | `you may make, you may do, you may produce, you may create` | 19:8 |
| πονηρεύομαι | `you may be evil` | `you may be evil, you may act wickedly, you may play the rogue` | 19:7 |
| ποτίζω | `gave to drink` | `gave to drink, watered` | 19:33, 19:35 |
| ποτίζω | `let us give to drink` | `let us give to drink, let us water` | 19:32, 19:34 |
| πρεσβύτερος | `of elder` | `of elder, of older, of higher and more important, of greater than, of an elder of the Jewish Council, of an elder of the Church and presbyter` | 19:4 |
| πρεσβύτερος | `the elder` | `the elder, the older, the higher and more important, the greater than, the elder of the Jewish Council, the elder of the Church and presbyter` | 19:31, 19:33, 19:34, 19:37 |
| πρωΐ | `early in the day` | `early in the day, early, at morn, betimes, in good time, too soon and too early` | 19:27 |
| πρόθυρον | `the front-door` | `the front-door, the space before a door, the porch and verandah` | 19:6 |
| πρᾶγμα | `that which has been done` | `that which has been done, a deed, an act, anything necessary and expedient, a thing of consequence and importance, an action and affair, the thing and the business` | 19:22 |
| πόλις | `of the city` | `of the city, of the citadel, of the country, of the body of citizens, of the state` | 19:4, 19:15, 19:22 |
| πόλις | `the cities` | `the cities, the citadels, the countries, the bodies of citizens, the states` | 19:25, 19:29 |
| πόλις, with ἐν | `in the cities` | `within, inside of, and by means of the cities, the citadels, the countries, the bodies of citizens, the states` | 19:25 |
| πότος | `drinking` | `drinking, a drinking-bout, carousal` | 19:3 |
| πύλη | `the one wing of a pair of double gates` | `the one wing of a pair of double gates, the gates of a town, the house-door, the nether world and hell, the entrance, the orifice, the entrance into a country through mountains and the mountain-pass, the narrow straits` | 19:1 |
| πῦρ | `fire` | `fire, the funeral-fire, the fire of the hearth` | 19:24 |
| σκέπη | `the covering` | `the covering, the shelter, the protection` | 19:8 |
| σπήλαιον, with ἐν | `in the grotto` | `within, inside of, and by means of the grotto, the cave, the cavern` | 19:30 |
| στήλη | `a block of stone` | `a block of stone, a prop and buttress to a wall, a slab, a gravestone, the record and a contract and agreement, the turning-post` | 19:26 |
| συγγίνομαι | `we may be with` | `we may be with, we may hold converse and communication with, we may associate and keep company with, we may consult, we may come to assist, we may come together and meet` | 19:5 |
| συμπαραλαμβάνω | `you may be taken along with` | `you may be taken along with, you may be taken in as an adjunct` | 19:17 |
| συντρίβω | `to rub together` | `to rub together, to shiver to atoms, to beat to a jelly and crush` | 19:9 |
| σῴζω | `I will be saved` | `I will be saved, I will be kept, I will be saved from death and kept alive and preserved, I will be kept safe, I will be kept and observed and maintained, I will be kept in mind and remembered, I will be brought safe to, I will be carried off safe and rescued from, I will come safe and escape to` | 19:20 |
| σῴζω | `keep for yourself` | `keep for yourself and preserve for yourself, keep in mind and remember` | 19:17 |
| σῴζω | `save` | `save, keep, save from death and keep alive and preserve, keep safe, keep and observe and maintain, keep in mind and remember, bring safe to, carry off safe and rescue from` | 19:17 |
| σῴζω | `saving` | `saving, keeping, saving from death and keeping alive and preserving, keeping safe, keeping and observing and maintaining, keeping in mind and remembering, bringing safe to, carrying off safe and rescuing from` | 19:17 |
| σῴζω | `to be saved` | `to be saved, to be kept, to be saved from death and kept alive and preserved, to be kept safe, to be kept and observed and maintained, to be kept in mind and remembered, to be brought safe to, to be carried off safe and rescued from, to come safe and escape to` | 19:22 |
| ταράσσω | `were stirred` | `were stirred, were stirred up, were troubled, were confounded and agitated and disturbed and disquieted, were thrown into disorder, were agitated and distracted, were raised by stirring up, were in disorder, were in a state of disorder and anarchy, were shaken in their seat` | 19:16 |
| φείδομαι, with ἐν τῷ | `in the sparing` | `within, inside of, and by means of the sparing, the not destroying, the being merciful, the refraining from using and using sparingly, the being sparing and being thrifty and living thriftily, the drawing back from, the ceasing, the forbearing` | 19:16 |
| ἀνήρ | `a man` | `a man, a man in the prime of life` | 19:8 |
| ἀνίστημι | `stand up` | `stand up, rise, rise to fight against, rise to go and set out` | 19:14 |
| ἀνίστημι | `to stand up` | `to stand up, to rise, to rise to fight against, to rise to go and set out` | 19:33, 19:35 |
| ἀνατέλλω | `the ones making to rise up` | `the ones making to rise up, growing up, giving birth to and bringing to light, rising, taking their rise, growing` | 19:25 |
| ἀορασία | `with inability to see` | `with inability to see, with blindness, with failure to observe` | 19:11 |
| ἀποθνήσκω | `I may die off` | `I may die off, I may die, I may be put to death, I may be slain` | 19:19 |
| ἀποκλείω | `shut off from` | `shut off from and out of, debarred, shut out and excluded from, shut up and barred and closed, shut up, shut out and intercepted and barred` | 19:10 |
| ἀπόλλυμι | `we destroy utterly` | `we destroy utterly, we kill, we slay, we destroy and demolish and waste, we talk and bore to death, we lose utterly` | 19:13 |
| ἀρέσκω | `may make good` | `may make good and make up, may make amends, may please and satisfy and flatter` | 19:8 |
| ἀτμίς | `steam` | `steam, vapour` | 19:28 |
| ἀφίστημι | `stand away` | `stand away, stand aloof from and keep far from, lose, withdraw from, revolt from, revolt, give up, make way and give way, shrink from, stand aloof` | 19:9 |
| ἄγγελος | `the messengers` | `the messengers and envoys, the ones that announce, the divine messengers and the angels` | 19:1, 19:15, 19:16 |
| ἄδικος | `wrong-doing` | `wrong-doing, unrighteous, unjust, obstinate and unmanageable, wrongly done and wrong and unjust` | 19:8 |
| ἄλλος | `another` | `another, one besides, any other and some other, the other, all the others and the rest, yet and still, of other sort and different, other than, else` | 19:12 |
| ἅλς | `of a lump of salt` | `of a lump of salt, of salt` | 19:26 |
| ἅπας | `quite all` | `quite all, the whole, all together, all, everyone` | 19:4 |
| ἐγγίζω | `brought near` | `brought near, brought up to, approached, were imminent, approximated to, were next of kin, were on the point of` | 19:9 |
| ἐγγύς | `hard by` | `hard by, near to, near, nigh, at hand, nigh at hand, nearly, akin to` | 19:20 |
| ἐκκαλέω | `were calling out to themselves` | `were calling out to themselves, were calling forth and eliciting, were calling on to` | 19:5 |
| ἐκκλίνω | `bend out of the regular line` | `bend out of the regular line, turn away and give ground and retire, avoid and shun, turn aside towards` | 19:2 |
| ἐκκλίνω | `bent out of the regular line` | `bent out of the regular line, turned away and gave ground and retired, avoided and shunned, turned aside towards` | 19:3 |
| ἐκτρίβω | `rubs out` | `rubs out, rubs hard, destroys root and branch, rubs constantly and wears out` | 19:14 |
| ἐκτρίβω | `to rub out` | `to rub out, to rub hard, to destroy root and branch, to rub constantly and wear out` | 19:13 |
| ἐκτρίβω, with ἐν τῷ | `in the rubbing out` | `within, inside of, and by means of the rubbing out, the rubbing hard, the destroying root and branch, the rubbing constantly and wearing out` | 19:29 |
| ἐξάγω | `I will lead out` | `I will lead out, I will lead and carry out from, I will bring forth into the world, I will march out, I will eject, I will carry out and export, I will draw off, I will call forth and excite, I will lead on and tempt` | 19:8 |
| ἐξανίστημι | `let us raise up` | `let us raise up, let us make to rise, let us remove and expel, let us rouse` | 19:32, 19:34 |
| ἐξανίστημι | `stood up from one's seat` | `stood up from one's seat, rose, arose and departed from and emigrated from, broke up and departed, was driven out, was forced to emigrate, was depopulated` | 19:1 |
| ἐπιβλέπω | `looked upon` | `looked upon, looked attentively, looked well at and observed, eyed with envy` | 19:26, 19:28 |
| ἑσπέρα | `of evening` | `of evening, of eventide, of eve, of nightfall, of the west` | 19:1 |
| ἔλεος | `pity` | `pity, mercy, compassion, an object of compassion and a piteous thing` | 19:19 |
| ἔρχομαι | `you came` | `you came, you went, you went back and returned, you were going to and intended, you came within a little of and were near` | 19:9 |
| ἡμέρα | `of day` | `of day, of day-break, of time` | 19:37, 19:38 |
| ἤ | `or` | `or, either or, whether or, than and as, rather` | 19:9, 19:12 |
| ἵστημι | `you may be set` | `you may be set, you may be placed, you may stand, you may be there, you may be in a state and condition, you may lie and be situated, you may stand still and stop and halt, you may stand idle, you may stop and cease and be at rest, you may stand firm, you may stand up and rise up, you may arise and begin` | 19:17 |
| ὀπίσω | `backwards` | `backwards, back and back again, again, hereafter, behind, following` | 19:17, 19:26 |
| ὀρθρίζω | `having risen early` | `having risen early, having been awake early` | 19:2 |
| ὀρθρίζω | `rose early` | `rose early, was awake early` | 19:27 |
| ὄρθρος | `day-break` | `day-break, dawn, cock-crow, in the morning` | 19:15 |
| ὄρος, with ἐν | `in the mountain` | `within, inside of, and by means of the mountain, the hill` | 19:30 |
| ὡσεί | `just as if` | `just as if, as though, about` | 19:28 |
| ῥῆμα | `to that which is said` | `to that which is said and spoken, to the word, to the saying, to the phrase, to the subject of speech and the thing, to the verb` | 19:21 |

### Words new in GEN 18

- ἆρα — Middle Liddell gives it no gloss, only *in accent and sense a stronger form of ἄρα*, so the
  chain is ἄρα's, as ἐπειδή's is ἐπεί's (15:3). Perseus keys ἄρα itself with a rough breathing,
  `a(/ra`; its first sense is *then, straightway, at once*. 18:3, 18:13.
- πρεσβύτερος — filed inside πρέσβυς, whose comparative is *elder, older*, and in the New
  Testament *an elder of the Jewish Council*, *an elder of the Church, presbyter*. The comparative's
  own senses stand, as the adverb's do for an adverb filed inside its adjective; πρέσβυς's
  *an old man* is not the comparative's. 18:11, 18:12.
- τὰ γυναικεῖα — γυναικεῖος's noun sense, *the women's apartments, harem*, belongs to the singular
  τὸ γυναικεῖον, so the plural takes the article and the adjective's senses, `the belonging to
  women`, as ὁ οἰκογενής is `the born in the house` (15:3). 18:11.
- ἵστημι and παρίστημι in the perfect and pluperfect take the intransitive senses the entries
  give those tenses: εἱστήκεισαν `had been set and stood so` (18:2), παρειστήκει `had stood by`
  (18:8), ἑστηκώς `having been set and standing so` (18:22). ἐξανίστημι's second aorist likewise,
  `having stood up from one's seat` (18:16).
- ἀποκρίνομαι — filed under ἀποκρίνω, whose middle is *to give answer to, reply*; its aorist
  passive is, in the entry's words, *= ἀπεκρίνατο*: `having given answer to`. 18:9, 18:27.
- The genitive absolute, καθημένου αὐτοῦ — the case's `of` before each gloss, `of being seated`.
  18:1.
- Two tags split by *or* where the first is no gloss by itself: νίπτω's *to wash the hands* or
  *feet* (*feet* left out), as παιδίον's *a little* at 17:12. 18:4.
- ὥρα plural — each sense in the plural, *Hours* capitalised as the lexicon prints the goddesses.
  18:10, 18:14.
- ἄρτος anarthrous — `a cake, a loaf of wheat-bread, bread`, the chain of GEN 3:19 with the
  lexicon's own articles. 18:5.
- μηδαμῶς — *adverb of μηδαμός = μηδαμῇ*; μηδαμῇ's one sense, *in no wise, not at all*. 18:25.
- One sense each in GEN 18, so plain text: συνάντησις `a meeting` (18:2); δένδρον `the tree`
  (18:4, 18:8), not δρῦς; σεμίδαλις `of the finest wheaten flour`, ἐγκρυφίας `baked in the ashes`
  (18:6); μοσχάριον `little calf` (18:7, 18:8, LSJ); γάλα `milk` (18:8); καταβλέπω `looked down
  at`, συμπροπέμπω `joining in escorting` (18:16); ἐνευλογέομαι `will be blessed in` (18:18), as at
  12:3; ἐλαττονόω `may be diminished` (18:28); οὐχί `not` (18:15).

| lemma | headword | chain | used |
| --- | --- | --- | --- |
| βούτυρον | `butter` | `butter, a plant` | 18:8 |
| βοῦς | `the cows` | `the cows, the oxen, the kine and cattle, the ox-hide shields` | 18:7 |
| γέ | `at least` | `at least, at any rate, even, that is to say, really, namely and that is, yes and, well then` | 18:13 |
| γίνομαι | `coming into being` | `coming to be, arising, being brought into existence` | 18:18 |
| γελάω | `I laughed` | `I laughed, I laughed at, I derided` | 18:15 |
| γελάω | `you laughed` | `you laughed, you laughed at, you derided` | 18:15 |
| γηράσκω | `I have grown old` | `I have grown old and stand so, I have become old and remain so` | 18:13 |
| γινώσκω | `I may learn to know` | `I may learn to know, I may perceive, I may mark, I may learn, I may discern and distinguish` | 18:21 |
| γυναικεῖος | `the belonging to women` | `the belonging to women, the like women, the befitting them, the feminine, the womanish and effeminate` | 18:11 |
| δίκαιος | `of observant of custom and social rule` | `of observant of custom and social rule, of well-ordered and civilised, of observant of right and righteous, of even and well-balanced, of regular and exact, of right and lawful and just, of real and genuine and true, of fair and moderate` | 18:24 |
| δίκαιος | `the observant of custom and social rule` | `the observant of custom and social rule, the well-ordered and civilised, the observant of right and righteous, the even and well-balanced, the regular and exact, the right and lawful and just, the real and genuine and true, the fair and moderate` | 18:23, 18:25 |
| εὑρίσκω | `I found` | `I found, I found out, I discovered` | 18:3 |
| εὑρίσκω | `I may find` | `I may find, I may find out, I may discover` | 18:26, 18:28, 18:30 |
| εὑρίσκω | `may be found` | `may be found, may be found out, may be discovered` | 18:29, 18:30, 18:31, 18:32 |
| θύρα | `of the door` | `of the door, of the folding doors, of the gate, of the court, of the trap-door, of the frame of planks and raft, of the entrance` | 18:1, 18:2 |
| θύρα | `to the door` | `to the door, to the folding doors, to the gate, to the court, to the trap-door, to the frame of planks and raft, to the entrance` | 18:10 |
| κάθημαι | `of being seated` | `of being seated, of being seated in court, of sitting still and sitting quiet, of sitting and lying idle, of sitting down and lying, of leading a sedentary life, of being settled` | 18:1 |
| καταψύχω | `cool` | `cool, chill` | 18:4 |
| κρίνω | `the one picking out` | `the one picking out and choosing, the one picking out for oneself and choosing, the one deciding, the one judging, the one adjudging, the one judging of and estimating, the one expounding and interpreting, the one determining, the one questioning, the one bringing to trial and accusing, the one passing sentence upon and condemning` | 18:25 |
| κρίσις | `a separating` | `a separating and power of distinguishing, choice and selection, a decision and judgment, means of judging, a trial, the result of a trial and condemnation, a dispute, the event and issue` | 18:19, 18:25 |
| κραυγή | `a crying` | `a crying, screaming, shrieking, shouting` | 18:20 |
| κραυγή | `the crying` | `the crying, the screaming, the shrieking, the shouting` | 18:21 |
| κρύπτω | `I may hide` | `I may hide, I may cover and cloak, I may conceal and keep secret` | 18:17 |
| λέγω | `you have said` | `you have said and it stands said, you have spoken and it stands spoken, you have declared and it stands declared, you have called by name and it stands so, you have told and it stands told` | 18:5 |
| λαλέω | `I may talk` | `I may talk, I may chat, I may prattle, I may babble, I may say, I may talk of, I may speak, I may chatter, I may chirp` | 18:30, 18:32 |
| λαλέω | `to talk` | `to talk, to chat, to prattle, to babble, to say, to talk of, to speak, to chatter, to chirp` | 18:27, 18:29, 18:31 |
| λαμβάνω | `let be taken` | `let be taken, let be received, let be taken hold of and grasped and seized` | 18:4 |
| μέν | `on the one hand` | `on the one hand, on the other hand, as well as, while, whereas, indeed, for my part, surely, accordingly and so, at all events and at any rate, so then, nay rather, nay, yea rather, yet and but however and nevertheless, of course and certainly, only` | 18:12 |
| μέτρον | `things by which anything is measured` | `things by which anything is measured, measures, rules, measures of content, measures and lengths and sizes, full measures, due measures, limits and proportions, metres, verses` | 18:6 |
| μεσημβρία | `of mid-day` | `of mid-day, of noon, of the parts towards noon and the South` | 18:1 |
| μηδαμῶς | `in no wise` | `in no wise, not at all` | 18:25 |
| νίπτω | `let wash the hands` | `let wash the hands, let purge and cleanse, let wash off` | 18:4 |
| οἶδα | `I knew` | `I knew, I was assured, I was versed in` | 18:19 |
| οἶκος | `to the house` | `to the house, to the abode and dwelling, to the room and chamber, to the house of a god and temple, to the household goods and substance, to the household and family` | 18:19 |
| παρά + dative | `beside` | `beside, alongside of, by, at, before, with` | 18:14 |
| παρέρχομαι | `you may go by` | `you may go by, you may go beside, you may go past, you may pass by, you may pass, you may outstrip, you may outwit and escape and elude, you may arrive at, you may pass in, you may go into, you may pass without heeding, you may pass over and disregard and slight, you may overstep and transgress, you may pass unnoticed and escape the notice of, you may come forward` | 18:3 |
| παρέρχομαι | `you will go by` | `you will go by, you will go beside, you will go past, you will pass by, you will pass, you will outstrip, you will outwit and escape and elude, you will arrive at, you will pass in, you will go into, you will pass without heeding, you will pass over and disregard and slight, you will overstep and transgress, you will pass unnoticed and escape the notice of, you will come forward` | 18:5 |
| παρίστημι | `had stood by` | `had stood by and beside and near, had helped and defended, had come and been at hand and been present, had been near and at hand, had come to the side of and come over to, had come to terms and surrendered and submitted, had happened, had come into his head and occurred to` | 18:8 |
| παρατίθημι | `placed beside` | `placed beside, set before and served up, offered and provided, placed upon, laid before and explained, compared` | 18:8 |
| παύω | `took his rest` | `took his rest, rested and ceased and had done, left off from and rested and ceased from, was at rest, left off doing` | 18:33 |
| παῖς | `of the child` | `of the child, of the son, of the daughter, of the grandchild, of the boy and youth and lad, of the girl and maiden, of the slave and servant and man and maid` | 18:17 |
| παῖς | `the child` | `the child, the son, the daughter, the grandchild, the boy and youth and lad, the girl and maiden, the slave and servant and man and maid` | 18:3, 18:5 |
| παῖς | `to the child` | `to the child, to the son, to the daughter, to the grandchild, to the boy and youth and lad, to the girl and maiden, to the slave and servant and man and maid` | 18:7 |
| πληθύνω | `has been made full` | `has been made full and stands so, has been increased and stands so, has been multiplied and stands so, has been in the majority and remains so, has prevailed and stands so` | 18:20 |
| ποιέω | `I make` | `I make, I do, I produce, I create` | 18:17 |
| πολύς | `much` | `much and mighty and great, many, deep, loud, strong, large and wide, far, long, often` | 18:18 |
| πούς | `the feet` | `the feet, the talons, the feet of a hill` | 18:4 |
| πρεσβύτερος | `elder` | `elder, older, higher and more important, greater than, an elder of the Jewish Council, an elder of the Church and presbyter` | 18:12 |
| πρεσβύτερος | `elder` | `elder, older, higher and more important, greater than, elders of the Jewish Council, elders of the Church and presbyters` | 18:11 |
| προβαίνω | `having stepped on` | `having stepped on and standing so, having stepped forward and standing so, having advanced and standing so, having proceeded and standing so, having gone before and standing so, having been before and superior to and remaining so, having overstepped and standing so` | 18:11 |
| προσκυνέω | `made obeisance` | `made obeisance, fell down and worshipped, worshipped, adored, did reverence to, made the salam, prostrated himself before` | 18:2 |
| προστρέχω | `ran to` | `ran to, ran towards and came to, ran up, ran at and made a sally` | 18:2 |
| πόλις, with ἐν | `in the city` | `within, inside of, and by means of the city, the citadel, the country, the body of citizens, the state` | 18:24, 18:26 |
| σκηνή | `of the covered place` | `of the covered place, of the tent, of the camp, of the dwelling-place, of the temple` | 18:1, 18:2, 18:10 |
| σκηνή, with ἐν | `in the covered place` | `within, inside of, and by means of the covered place, the tent, the camp, the dwelling-place, the temple` | 18:9 |
| σπεύδω | `set a-going` | `set a-going, urge on, hasten, quicken, seek eagerly and strive after, promote zealously and press, press on and hasten and exert yourself and strive eagerly, be eager to do, be anxious that` | 18:6 |
| σπεύδω | `set a-going` | `set a-going, urged on, hastened, quickened, sought eagerly and strove after, promoted zealously and pressed, pressed on and hastened and exerted himself and strove eagerly, was eager to do, was anxious that` | 18:6 |
| σποδός | `wood-ashes` | `wood-ashes, embers, ashes, dust` | 18:27 |
| συμπορεύομαι | `was going` | `was going, was journeying together, was coming together` | 18:16 |
| συναπόλλυμι | `you may destroy together` | `you may destroy together, you may lose` | 18:23 |
| συντάσσω | `will put in order together` | `will put in order together, will draw up and put in array, will arrange and organise, will concoct, will fix and assess, will ordain and prescribe` | 18:19 |
| συντελέω | `are being brought quite to an end` | `are being brought quite to an end, are being completed, are being accomplished, are being made up into the whole and into the number` | 18:21 |
| τίκτω | `I will bring into the world` | `I will bring into the world, I will bring forth, I will bear, I will produce` | 18:13 |
| ταχύνω | `made quickly` | `made quickly, was quick, made haste, sped, hurried` | 18:7 |
| τρέχω | `ran` | `ran, moved quickly, ran over, ran the risk` | 18:7 |
| φοβέομαι | `was put to flight` | `was put to flight, fled affrighted, fled, was seized with fear, was affrighted, feared` | 18:15 |
| φυλάσσω | `they will keep watch and ward` | `they will keep watch and ward, they will keep guard, they will watch and guard and keep and defend` | 18:19 |
| φυράω | `mix` | `mix, knead, make up` | 18:6 |
| ἀδυνατέω | `wants strength` | `wants strength, is unable, is impossible` | 18:14 |
| ἀληθῶς | `truly` | `truly, really and actually and in reality` | 18:13 |
| ἀνήρ | `men` | `men, men in the prime of life` | 18:2 |
| ἀνίημι | `you will send up` | `you will send up and forth, you will make spring up, you will produce, you will send back and put back and open, you will let go and leave, you will let go unpunished, you will let loose at, you will set on and urge, you will let go for, you will set free from, you will let and allow, you will let go free and leave untilled, you will slacken and relax and let down and unstring, you will remit and neglect and give up, you will slacken and abate, you will give way, you will give up and cease, you will cease from` | 18:24 |
| ἀναστρέφω | `I will turn upside down` | `I will turn upside down, I will upset, I will turn back and bring back, I will rally, I will turn back and return and retire, I will dwell, I will conduct myself, I will revolve, I will face about` | 18:14 |
| ἀπέρχομαι | `went away` | `went away, departed from, departed, departed from life` | 18:33 |
| ἀποκρίνομαι | `having given answer to` | `having given answer to, having replied, having answered, having answered charges and defended himself` | 18:27 |
| ἀποκρίνομαι | `the one having given answer to` | `the one having given answer to, having replied, having answered, having answered charges and defended himself` | 18:9 |
| ἀποκτείνω | `to kill` | `to kill, to slay, to condemn to death` | 18:25 |
| ἀποστρέφω | `having turned` | `having turned, having turned back, having turned away, having turned oneself about, having brought back` | 18:22 |
| ἀποστρέφω | `turned` | `turned, turned back, turned away, turned himself about, brought back` | 18:33 |
| ἀπόλλυμι | `I may destroy utterly` | `I may destroy utterly, I may kill, I may slay, I may destroy and demolish and waste, I may talk and bore to death, I may lose utterly` | 18:28, 18:29, 18:30, 18:31, 18:32 |
| ἀπόλλυμι | `you will destroy utterly` | `you will destroy utterly, you will kill, you will slay, you will destroy and demolish and waste, you will talk and bore to death, you will lose utterly` | 18:24, 18:28 |
| ἀρνέομαι | `denied` | `denied, disowned, declined to give and refused, said no and declined and refused` | 18:15 |
| ἀσεβής | `of ungodly` | `of ungodly, of godless, of unholy, of profane` | 18:23, 18:25 |
| ἀσεβής | `the ungodly` | `the ungodly, the godless, the unholy, the profane` | 18:23, 18:25 |
| ἀφίημι | `I will send forth` | `I will send forth, I will discharge, I will send away and let go, I will set free, I will release` | 18:26 |
| ἁπαλός | `soft to the touch` | `soft to the touch, tender, fresh, soft and gentle, soft and delicate` | 18:7 |
| ἄρα, ἆρα | `then` | `then, straightway, at once, next in order, mark ye, for, just and very, then and therefore, so then` | 18:3, 18:13 |
| ἄρτος | `a cake` | `a cake, a loaf of wheat-bread, bread` | 18:5 |
| ἄρχω | `I began` | `I began, I made a beginning, I made a beginning of, I began from` | 18:27 |
| ἅπαξ | `once` | `once, once only, once for all` | 18:32 |
| ἐγγίζω | `having brought near` | `having brought near, having brought up to, having approached, having been imminent, having approximated to, having been next of kin, having been on the point of` | 18:23 |
| ἐκκλίνω | `you bent out of the regular line` | `you bent out of the regular line, you turned away and gave ground and retired, you avoided and shunned, you turned aside towards` | 18:5 |
| ἐξανίστημι | `having stood up from one's seat` | `having stood up from one's seat, having risen, having arisen and departed from and emigrated from, having broken up and departed, having been driven out, having been forced to emigrate, having been depopulated` | 18:16 |
| ἐπάγω | `may bring on` | `may bring on, may bring upon, may set on and urge on, may lead on, may bring in and invite, may bring to, may lay on and apply, may bring forward, may add` | 18:19 |
| ἐπαναστρέφω | `turning back upon` | `turning back upon, wheeling round, returning to the charge` | 18:10 |
| ἔρχομαι | `coming` | `coming, going, going back and returning, going to and intending, coming within a little of and being near` | 18:21 |
| ἔχω | `I have` | `I have, I hold, I possess, I keep, I hold fast, I bear up against and support` | 18:31 |
| ἔχω | `will have` | `will have, will hold, will possess, will keep, will hold fast, will bear up against and support` | 18:10 |
| ἥκω | `I will have come` | `I will have come, I will be present, I will be here, I will have returned, I will have reached a point` | 18:10 |
| ἵστημι | `had been set` | `had been set and stood so, had been placed, had stood, had been there, had been in a state and condition, had lain and been situated, had stood still and stopped and halted, had stood idle, had stopped and ceased and been at rest, had stood firm, had stood up and risen up, had arisen and begun` | 18:2 |
| ἵστημι | `having been set` | `having been set and standing so, having been placed, having stood, having been there, having been in a state and condition, having lain and been situated, having stood still and stopped and halted, having stood idle, having stopped and ceased and been at rest, having stood firm, having stood up and risen up, having arisen and begun` | 18:22 |
| ὁδός | `the ways` | `the ways, the paths, the tracks, the roads, the highways, the courses, the journeys, the manners and methods` | 18:19 |
| ὄπισθεν | `behind` | `behind, at the back, the rear and back, back and backwards, in future and hereafter, following` | 18:10 |
| ὥρα | `periods` | `periods, parts of the year and seasons, springs, summers, winters, primes of the year and springtimes, parts of the year available for war and summer-seasons, years, quarters of the heavens, parts of the day, times of day, twenty-four hours, twelve parts, times and seasons, primes of life and youths and early manhoods, fruits of the year, Hours` | 18:10, 18:14 |
| ῥῆμα | `that which is said` | `that which is said and spoken, the word, the saying, the phrase, the subject of speech and the thing, the verb` | 18:25 |

### Words new in GEN 17

- περιτέμνω — Middle Liddell's *to cut* or *clip round about*, tagged in two pieces; *to cut* is a
  gloss by itself and heads, as *to go* heads συμπορεύομαι's *to go or journey together* (13:5).
  A passive form takes the active senses, *to be pruned*, *to be cut off*, *to be cut off and hemmed
  in all round*, and the passive's own, *to be curtailed of*, *to be cut off, intercepted*, last.
  *To make incisions all round* and *they practise circumcision* are translations of the middle
  alone, and neither passive nor active takes them. 17:10–14, 17:23–27.
- παιδίον — Middle Liddell's *a little* or *young child*: *a little* is no gloss by itself, so it
  goes in NOT_SENSES and *young child* heads. ἀλλότριος — *of* or *belonging to another*: *of*
  likewise, and *belonging to another* heads. 17:12.
- ἐνιαυτός — first *any long period of time, a cycle, period*; with the article, *the* stands where
  the lexicon has *any*, as it does for *a*: `in the long period of time`. 17:21.
- ἑκατονταέτης — articular, with no noun: `to the of a hundred years`, the article and the lexicon's
  gloss, as ὁ οἰκογενής is `the born in the house` (15:3). 17:17.
- ἀλλογενής — the gloss *of another race* in the genitive plural: the case's `of` stands before the
  lexicon's own, `of of another race`. 17:27.
- θεός anarthrous, not fronted — εἶναί σου θεός (17:7), ἔσομαι αὐτοῖς θεός (17:8): `God` /
  `everything that God is by nature, deity in full and undiminished kind`.
- Αβραμ and Αβρααμ, Σαρα and Σαρρα — two names each, each glossed on its first occurrence in the
  chapter; the anchored forms are Abram, Abraham, Sarai, Sarah. 17:5, 17:15.
- One sense each in GEN 17, so plain text: ἀρσενικός `male` (17:10, 17:12), under ἀρρενικός;
  ἀργυρώνητος `bought with silver` (17:12, 17:13, 17:23, 17:27); περιτομή `to circumcision`
  (17:13); ἀπερίτμητος `uncircumcised` and ὄγδοος `eighth` (17:14); ἐξολεθρεύω `will be destroyed
  utterly` (17:14), under ἐξολοθρεύω; δώδεκα `twelve` (17:20).

| lemma | headword | chain | used |
| --- | --- | --- | --- |
| αὐξάνω | `I will make large` | `I will make large, I will increase and augment, I will increase in power and strengthen and exalt, I will promote to honour and glorify and magnify, I will grow and wax and increase, I will grow up` | 17:6, 17:20 |
| γένος | `of the race` | `of the race, of the stock and family, of the offspring and posterity, of the clan and house, of the tribe and caste, of the breed, of the age and generation, of the sex and gender, of the class and sort and kind, of the genus` | 17:14 |
| γίνομαι | `come into being` | `come to be, arise, be brought into existence` | 17:1 |
| γίνομαι | `will come into being` | `will come to be, will arise, will be brought into existence` | 17:17 |
| γελάω | `laughed` | `laughed, laughed at, derided` | 17:17 |
| γενεά | `the races` | `the races, the stocks and families, the breeds, the tribes and nations, the generations, the offspring, the birth-places, the ages and times of life` | 17:9, 17:10, 17:12 |
| γεννάω | `will beget` | `will beget, will engender, will bring forth, will produce` | 17:20 |
| διάνοια, with ἐν | `in the thought` | `within, inside of, and by means of the thought, the intention and purpose, the notion and opinion, the intelligence and understanding, the meaning` | 17:17 |
| διασκεδάννυμι | `scattered abroad` | `scattered abroad, scattered to the winds, dispersed, disbanded` | 17:14 |
| διατηρέω | `you will watch closely` | `you will watch closely, you will observe, you will keep faithfully and maintain, you will keep` | 17:9, 17:10 |
| εὐαρεστέω | `be well pleasing` | `be well pleasing, seem good, be resolved, be well pleased and satisfied` | 17:1 |
| εὐλογέω | `I spoke well of` | `I spoke well of, I praised, I honoured, I blessed` | 17:20 |
| ζάω | `let live` | `let live, let be in full life and strength, let be fresh and strong` | 17:18 |
| θεός | `God` | `everything that God is by nature, deity in full and undiminished kind` | 17:7, 17:8 |
| καιρός | `the due measure` | `the due measure, the proportion, the fitness, the vital part, the right point of time, the proper time and season, the exact and critical time, the time, the advantage and profit and fruit` | 17:21 |
| καιρός, with ἐν | `in the due measure` | `within, inside of, and by means of the due measure, the proportion, the fitness, the vital part, the right point of time, the proper time and season, the exact and critical time, the time, the advantage and profit and fruit` | 17:23, 17:26 |
| καλέω | `will be called` | `will be called, will be summoned, will be invited` | 17:5, 17:15 |
| κατάσχεσις | `holding back` | `holding back, restraining, retention, possession, relation and attitude` | 17:8 |
| λαλέω | `talking` | `talking, chatting, prattling, babbling, saying, talking of, speaking, chattering, chirping` | 17:22 |
| ναί | `yea` | `yea, verily, aye and yes` | 17:19 |
| οἰκία | `of the building` | `of the building, of the house, of the dwelling, of the household and domestic establishment, of the household and inmates of the house, of the house and family from which one is descended` | 17:12, 17:13 |
| πίπτω | `fell` | `fell, fell down, fell violently upon and attacked, threw himself down and fell down, fell and was ruined, fell and sank, fell short and failed, fell and turned out, was lucky, fell under and belonged to` | 17:3, 17:17 |
| παιδίον | `young child` | `young child, a slave-lad` | 17:12 |
| παροικέω | `you dwell beside` | `you dwell beside, you dwell along the coast of, you live near, you dwell among, you lie near, you live in and sojourn` | 17:8 |
| περιτέμνω | `cut` | `cut, clipped round about, pruned, cut off, cut off and hemmed in all round` | 17:23, 17:24, 17:27 |
| περιτέμνω | `was cut` | `was cut, was clipped round about, was pruned, was cut off, was cut off and hemmed in all round, was curtailed of, was cut off and intercepted` | 17:25, 17:26 |
| περιτέμνω | `will be cut` | `will be cut, will be clipped round about, will be pruned, will be cut off, will be cut off and hemmed in all round, will be curtailed of, will be cut off and intercepted` | 17:10, 17:12, 17:13, 17:14 |
| περιτέμνω | `you will be cut` | `you will be cut, you will be clipped round about, you will be pruned, you will be cut off, you will be cut off and hemmed in all round, you will be curtailed of, you will be cut off and intercepted` | 17:11 |
| πλῆθος | `of a great number` | `of a great number and throng and crowd and multitude, of the greater number and greater part and mass and main body, of the majority and people, of the populace and mob, of quantity, of number, of magnitude and size, of extent, of amount, of length` | 17:4 |
| πολύς | `of many` | `of many, often, of much and mighty and great, of deep, of loud, of strong, of large and wide, of far, of long` | 17:5 |
| σάρξ | `of the flesh` | `of the flesh, of the muscles, of the body, of man's nature generally` | 17:13 |
| σάρξ | `the flesh` | `the flesh, the muscles, the body, man's nature generally` | 17:11, 17:14, 17:24, 17:25 |
| σημεῖον, with ἐν | `in sign` | `within, inside of, and by means of sign, mark and token, sign from the gods and omen, signal, standard and ensign, boundary` | 17:11 |
| τέκνον | `that which is borne` | `that which is borne, the born, a child, the young` | 17:16 |
| τίθημι | `I have set` | `I have set and it stands set, I have put and it stands put, I have placed and it stands placed, I have planted and it stands planted, I have laid and it stands laid` | 17:5 |
| τίκτω | `will bring into the world` | `will bring into the world, will bring forth, will bear, will produce` | 17:17, 17:19, 17:21 |
| ἀκροβυστία | `of the foreskin` | `of the foreskin, of the circumcision, of the uncircumcision, of the uncircumcised` | 17:11, 17:14, 17:24, 17:25 |
| ἀκροβυστία | `the foreskins` | `the foreskins, the circumcisions, the uncircumcisions, the uncircumcised` | 17:23 |
| ἀλλογενής | `of of another race` | `of of another race, of strangers` | 17:27 |
| ἀλλότριος | `of belonging to another` | `of belonging to another, of another man's, of unlike one's own, of a forced and unnatural, of foreign and strange, of hostile` | 17:12 |
| ἄμεμπτος | `not to be blamed` | `not to be blamed, blameless, perfect in its kind, without blame, not blaming and content` | 17:1 |
| ἐνιαυτός, with ἐν | `in the long period of time` | `within, inside of, and by means of the long period of time, the cycle, the period, the year` | 17:21 |
| ἐπακούω | `I listened` | `I listened, I hearkened to and heard, I gave ear and hearkened, I obeyed` | 17:20 |
| ἑκατονταετής | `to the of a hundred years` | `to the of a hundred years, to the years old` | 17:17 |
| ἡμέρα | `of the day` | `of the day, of the day-break, of the time` | 17:23, 17:26 |
| ἡμέρα | `to the day` | `to the day, to the day-break, to the time` | 17:14 |

### Words new in GEN 16

- ἀδικέω — its first sense, *to do wrong*, has no object a passive could make its subject, so *to
  do one wrong, to wrong*, heads the passive `I am done wrong`, and the first follows in its own
  voice, as καπνίζω at 15:17. 16:5.
- γαστήρ — ἐν γαστρὶ ἔχειν, *to be with child*, stands in Middle Liddell under the last sense, *the
  womb*; the headword is the first, *paunch*. 16:4, 16:5, 16:11.
- κυρία — filed under κύριος, whose noun sense gives ἡ κυρία, *mistress* or *lady of the house*.
  16:4, 16:8, 16:9.
- Φρέαρ — capitalised as the first word of the well's name, glossed as a name; φρέαρ before it is
  the common noun. οὗ after it is the adverb, *where*, plain. 16:14.
- Αἰγυπτία — glossed `(Αἰγυπτία, the woman of Αἴγυπτος, Egypt)`, the feminine of 12:12's gloss. 16:1.
- One sense each in GEN 16, so plain text: τεκνοποιέω `you may bear children` (16:2), as at 11:30;
  ὕδωρ `of the water` (16:7); ἐνώπιον `face to face` (16:13, 16:14), as at 11:28; ἕξ `six` (16:16).

| lemma | headword | chain | used |
| --- | --- | --- | --- |
| γαστήρ, with ἐν | `in paunch` | `within, inside of, and by means of paunch and belly, hollow, greed and gluttony, paunch stuffed with mince-meat and black-pudding and sausage, womb` | 16:4, 16:5, 16:11 |
| κακόω | `treated ill` | `treated ill and maltreated and afflicted and distressed, spoiled and ruined, suffered ill and was in ill plight and was distressed` | 16:6 |
| καλέω | `you will call` | `you will call, you will summon, you will call to yourself, you will invite` | 16:11 |
| κατοικέω | `will dwell in` | `will dwell in, will settle in, will colonise, will inhabit, will settle and dwell, will lie and be situate` | 16:12 |
| κρίνω | `may pick out` | `may pick out and choose, may pick out for oneself and choose, may decide, may judge, may adjudge, may judge of and estimate, may expound and interpret, may determine, may question, may bring to trial and accuse, may pass sentence upon and condemn, may be chosen, may be brought to trial` | 16:5 |
| κυρία | `of the mistress` | `of the mistress, of the lady of the house` | 16:8 |
| κυρία | `the mistress` | `the mistress, the lady of the house` | 16:4, 16:9 |
| κόλπος | `the bosom` | `the bosom, the womb, the fold formed by a loose garment, the pocket, any hollow, the deep hollow between waves, the bay and gulf, the vale` | 16:5 |
| λαλέω | `of the one talking` | `of the one talking, chatting, prattling, babbling, saying, talking of, speaking, chattering, chirping` | 16:13 |
| οἰκέω | `to inhabit` | `to inhabit, to occupy, to dwell and live, to be settled` | 16:3 |
| παιδίσκη | `a young girl` | `a young girl, a maiden, a young slave, a courtesan` | 16:1 |
| παιδίσκη | `the young girl` | `the young girl, the maiden, the young slave, the courtesan` | 16:2, 16:5, 16:6 |
| παιδίσκη | `young girl` | `young girl, maiden, young slave, courtesan` | 16:3, 16:8 |
| πηγή | `of the running waters` | `of the running waters, of the streams, of the fount, of the source, of the origin` | 16:7 |
| πλῆθος | `of the great number` | `of the great number and throng and crowd and multitude, of the greater number and greater part and mass and main body, of the majority and people, of the populace and mob, of the quantity, of the number, of the magnitude and size, of the extent, of the amount, of the length` | 16:10 |
| πορεύομαι | `you are driven` | `you are driven, you are carried, you go, you walk, you march, you go across and pass` | 16:8 |
| πόθεν | `whence` | `whence, from what and from what source, wherefore, how can it be and impossible` | 16:8 |
| συγκλείω | `shut` | `shut and cooped up and hemmed in and enclosed, set together to fight as in the lists, shut close and closed, locked, closed up, was well linked` | 16:2 |
| συλλαμβάνω | `collected` | `collected, gathered together, took up, laid hold of and seized, comprehended, conceived` | 16:4 |
| τίκτω | `was bringing into the world` | `was bringing into the world, was bringing forth, was bearing, was producing` | 16:1 |
| ταπείνωσις | `to the humiliation` | `to the humiliation and abasement and defeat, to the low estate and low condition` | 16:11 |
| ταπεινόω | `be lowered` | `be lowered, be lessened, be disparaged, be humbled and abased, be made lowly and humbled, humble oneself` | 16:9 |
| φρέαρ | `the well` | `the well, the tank and cistern and reservoir, the oil jar` | 16:14 |
| χείρ | `the hands` | `the hands, the hands and arms, the arms` | 16:9, 16:12 |
| χείρ, with ἐν | `in the hands` | `within, inside of, and by means of the hands, the hands and arms, the arms` | 16:6 |
| χράομαι | `use` | `use, have and use, indulge, experience and suffer and be subject to, come to, live under, make use of, treat, be intimate with, be in need and yearn after, have in use and possess` | 16:6 |
| ἀδελφός | `of the sons of the same mother` | `of the sons of the same mother, of the brothers, of the near kinsmen` | 16:12 |
| ἀδικέω | `I am done wrong` | `I am done wrong and wronged and injured, I am spoiled and damaged, I do wrong, I am wronged` | 16:5 |
| ἀποδιδράσκω | `I run away` | `I run away and off and escape, I flee from, I desert, I flee and shun` | 16:8 |
| ἀποδιδράσκω | `ran away` | `ran away and off and escaped, fled from, deserted, fled and shunned` | 16:6 |
| ἀποστρέφω | `be turned` | `be turned, be turned back, be turned away, be brought back, turn oneself about` | 16:9 |
| ἀριθμέω | `will be numbered` | `will be numbered, will be counted and reckoned up, will be counted out and paid, will be reckoned and counted as, will be reckoned, will be counted` | 16:10 |
| ἀτιμάζω | `I was held in no honour` | `I was held in no honour and esteemed lightly and dishonoured and slighted, I was treated as unworthy of and deemed unworthy, I was deprived of civil rights, I suffered dishonour` | 16:5 |
| ἀτιμάζω | `was held in no honour` | `was held in no honour and esteemed lightly and dishonoured and slighted, was treated as unworthy of and deemed unworthy, was deprived of civil rights, suffered dishonour` | 16:4 |
| ἄγγελος | `a messenger` | `a messenger and envoy, one that announces, a divine messenger and an angel` | 16:7 |
| ἄγγελος | `the messenger` | `the messenger and envoy, the one that announces, the divine messenger and the angel` | 16:8, 16:9, 16:10, 16:11 |
| ἄγροικος | `of or in the country` | `of or in the country, dwelling in the country and a countryman and rustic, clownish and boorish and rude, rough and uncultivated` | 16:12 |
| ἐπακούω | `listened` | `listened, hearkened to and heard, gave ear and hearkened, obeyed` | 16:11 |
| ἐφοράω | `the one having overseen` | `the one having overseen, having observed, having surveyed, having watched over and taken notice of, having looked upon and beheld` | 16:13 |
| ἔρχομαι | `you come` | `you come, you go, you go back and return, you are going to and intend, you come within a little of and are near` | 16:8 |
| ἔχω | `has` | `has, holds, possesses, keeps, holds fast, bears up against and supports` | 16:4, 16:5 |
| ἔχω | `you have` | `you have, you hold, you possess, you keep, you hold fast, you bear up against and support` | 16:11 |
| ὁδός, with ἐν | `in the way` | `within, inside of, and by means of the way, the path, the track, the road, the highway, the course, the journey, the manner and method` | 16:7 |
| ὁράω | `having been seen` | `having been seen, having been looked at, having been beheld and perceived and observed, having been looked out for` | 16:13 |
| ὑπακούω | `listened` | `listened and hearkened and gave ear, made answer when called, hearkened to and gave ear to and attended to, answered, answered to a charge, submitted to, yielded to and complied with, gave way and submitted and complied, answered one's expectations and succeeded, was subject` | 16:2 |

### Words new in GEN 15

- δή — Perseus tags the entry's opening only as *exactness*, from "Particle used to give greater
  exactness", a description, and its other tags are pieces of examples (*all* alone, *quite* the
  greatest). The chain is the entry's own gloss, *now, in truth, indeed, surely, really*. 15:5.
- εὐθύς of time — Middle Liddell's second entry, the adverb, whose εὐθύ is *straight* of place and
  εὐθύς *straightway, forthwith, at once* of time; the place senses are skipped by name. 15:4.
- ἐπειδή — not in Middle Liddell; LSJ reads "v. ἐπεί", so the chain is ἐπεί's. 15:3, 15:17.
- καπνίζω — its first sense, *to make smoke, i. e. to make a fire*, has no object a passive could
  make its subject, so the second, *to smoke, blacken with smoke*, heads the passive participle, and
  the first follows in its own voice. 15:17.
- λογίζομαι — the aorist passive takes each sense in the passive; *to form calculations*, which has
  no passive, is left out. 15:6.
- θάπτω — *to pay the last dues to a corpse* in the passive: `having had the last dues paid to a
  corpse`. 15:15.
- τοῦ ποταμοῦ τοῦ μεγάλου — the second article is plain `the` and the adjective takes no `of`, as
  τοῦ θεοῦ τοῦ ὑψίστου at 14:18. 15:18.
- One sense each in GEN 15, so plain text: τριετίζω `being three years old` (15:9, LSJ); τρυγών
  `turtle-dove` (15:9); ἀλλήλων `to one another` (15:10), whose one sense is its case forms; γῆρας
  `old age` (15:15); τέταρτος `fourth` (15:16); τετρακόσιοι `four hundred` (15:13).

| lemma | headword | chain | used |
| --- | --- | --- | --- |
| αἴξ | `a goat` | `a goat, the wild goat and the ibex, waves` | 15:9 |
| γίνομαι | `was coming into being` | `was coming to be, was arising, was being brought into existence` | 15:17 |
| γενεά | `race` | `race, stock and family, breed, tribe and nation, generation, offspring, birth-place, age and time of life` | 15:16 |
| γινώσκω | `I will learn to know` | `I will learn to know, I will perceive, I will mark, I will learn, I will discern and distinguish` | 15:8 |
| γινώσκω | `you will learn to know` | `you will learn to know, you will perceive, you will mark, you will learn, you will discern and distinguish` | 15:13 |
| δάμαλις | `a heifer` | `a heifer, a girl` | 15:9 |
| δή | `now` | `now, in truth, indeed, surely, really` | 15:5 |
| δίδωμι | `you will give` | `you will give, you will grant, you will provide, you will give over and deliver up` | 15:2 |
| δεσπότης | `master` | `master, lord, master of the house, despot and absolute ruler, owner and master and lord` | 15:2, 15:8 |
| διέρχομαι | `went through` | `went through, passed through, went through in detail` | 15:17 |
| διαιρέω | `took one from another` | `took one from another, cleaved in twain, divided into parts, divided, distinguished, determined` | 15:10 |
| διατίθεμαι | `arranged as he liked` | `arranged as he liked, disposed of, disposed of his property and devised it by will, set out for sale and disposed of, arranged mutually, made a covenant with, settled with` | 15:18 |
| δικαιοσύνη | `righteousness` | `righteousness, justice` | 15:6 |
| διχοτόμημα | `of the halves of a thing cut in two` | `of the halves of a thing cut in two, of the portions of a thing cut up` | 15:17 |
| διχοτόμημα | `the halves of a thing cut in two` | `the halves of a thing cut in two, the portions of a thing cut up` | 15:11 |
| δουλεύω | `they may be slaves` | `they may be slaves, they may serve and be subject to` | 15:14 |
| δουλόω | `they will make a slave of` | `they will make a slave of and enslave, they will make one's slave and make subject to oneself and enslave, they will be enslaved` | 15:13 |
| δυσμή | `settings` | `settings, quarters of sunset and wests` | 15:12 |
| δυσμή | `to settings` | `to settings, to quarters of sunset and wests` | 15:17 |
| δύναμαι | `you will be able` | `you will be able, you will be capable and strong enough, you will be powerful and mighty, you will have influence, you will dare and bear, you will pass for, you will be worth, you will be equivalent to, you will signify and mean, you will avail` | 15:5 |
| εἰρήνη | `of peace` | `of peace, of time of peace` | 15:15 |
| εὐθύς | `straightway` | `straightway, forthwith, at once, just, directly and simply` | 15:4 |
| θάπτω | `having had the last dues paid` | `having had the last dues paid to a corpse, having been honoured with funeral rites, having been buried and interred` | 15:15 |
| κακόω | `they will treat ill` | `they will treat ill and maltreat and afflict and distress, they will spoil and ruin, they will suffer ill and be in ill plight and be distressed` | 15:13 |
| καπνίζω | `being smoked` | `being smoked and blackened with smoke, making smoke and making a fire, being black with smoke` | 15:17 |
| κλίβανος | `an earthen vessel` | `an earthen vessel, a pan` | 15:17 |
| κληρονομέω | `I will receive a share of an inheritance` | `I will receive a share of an inheritance and inherit a portion, I will inherit, I will be an inheritor, I will succeed` | 15:8 |
| κληρονομέω | `to receive a share of an inheritance` | `to receive a share of an inheritance and inherit a portion, to inherit, to be an inheritor, to succeed` | 15:7 |
| κληρονομέω | `will receive a share of an inheritance` | `will receive a share of an inheritance and inherit a portion, will inherit, will be an inheritor, will succeed` | 15:3, 15:4 |
| κρίνω | `I will pick out` | `I will pick out and choose, I will pick out for oneself and choose, I will decide, I will judge, I will adjudge, I will judge of and estimate, I will expound and interpret, I will determine, I will question, I will bring to trial and accuse, I will pass sentence upon and condemn, I will be chosen, I will be brought to trial` | 15:14 |
| κριός | `a ram` | `a ram, a battering-ram` | 15:9 |
| λέγω | `says` | `says, speaks, declares, calls by name, tells` | 15:2 |
| λέγω | `was said` | `was said, was spoken, was declared, was called by name, was told` | 15:13 |
| λαμπάς | `torches` | `torches, beacon-lights, oil-lamps, lights, torch-races, races` | 15:17 |
| λογίζομαι | `was counted` | `was counted, was reckoned and calculated and computed, was set down, was set down to one's account and charged, was deducted, was taken into account and calculated and considered, was counted and deemed and considered, was reckoned upon and expected, was counted upon, was concluded by reasoning and inferred, was counted and calculated` | 15:6 |
| μέσος | `middle` | `middle, in the middle, the centre, mid, between two` | 15:10 |
| μισθός | `the wages` | `the wages, the pay and hire, the recompense and reward, the payment and requital` | 15:1 |
| οἰκογενής | `of the born in the house` | `of the born in the house, of the homebred` | 15:2 |
| οἰκογενής | `the born in the house` | `the born in the house, the homebred` | 15:3 |
| οὐρανός | `the heaven` | `the heaven, the vault, the firmament and the sky` | 15:5 |
| οὔπω | `not yet` | `not yet, no longer and no more, not and not at all` | 15:16 |
| πάροικος | `dwelling beside` | `dwelling beside, a neighbour, a sojourner and alien` | 15:13 |
| πατήρ | `the fathers` | `the fathers, the grandfathers` | 15:15 |
| περί + accusative | `round about` | `round about, round, near, somewhere near, off, who are about one, about which one is occupied and concerned, about and in, about and in the case of, about and in respect of and in regard to` | 15:12 |
| περιστερά | `common pigeon` | `common pigeon, dove` | 15:9 |
| πιστεύω | `trusted` | `trusted, trusted to and in, put faith in, relied on, believed in, believed, believed on, believed mutually, complied, believed that and felt sure and confident that, dared, believed and had faith, entrusted, was trusted and believed, was entrusted with` | 15:6 |
| πολύς | `of much` | `of much and mighty and great, of many, of deep, of loud, of strong, of large and wide, of far, of long, often` | 15:14 |
| ποταμός | `of river` | `of river, of stream, of river-god` | 15:18 |
| ποταμός | `of the river` | `of the river, of the stream, of the river-god` | 15:18 |
| πῦρ | `of fire` | `of fire, of the funeral-fire, of the fire of the hearth` | 15:17 |
| σκοτεινός | `dark` | `dark, darkling and blind, dark and obscure` | 15:12 |
| συγκαθίζω | `made to sit together` | `made to sit together, sat in conclave and met for deliberation, sat with` | 15:11 |
| σῶμα | `the bodies` | `the bodies, the dead bodies and corpses and carcases, the living bodies, the bodies and any material substances, the whole bodies and masses` | 15:11 |
| ταπεινόω | `they will lower` | `they will lower, they will lessen, they will disparage, they will humble and abase, they will make lowly and humble, they will humble oneself` | 15:13 |
| φλόξ | `a flame` | `a flame, a flash, the fiery strength` | 15:17 |
| φοβέομαι | `be put to flight` | `be put to flight, flee affrighted, flee, be seized with fear, be affrighted, fear` | 15:1 |
| φόβος | `flight` | `flight, panic fear, fear and terror, outward show of fear, object of terror` | 15:12 |
| χώρα | `of space in which a thing is` | `of space in which a thing is, of place, of position and post, of place in life and station, of land and country, of piece of land and estate and farm, of country` | 15:7 |
| ἀλλά | `otherwise` | `otherwise, but, except, yet, but then and however, but really and certainly` | 15:4 |
| ἀναβλέπω | `look up` | `look up, look, look up at, cast up, recover one's sight` | 15:5 |
| ἀναπληρόω | `have been filled up` | `have been filled up and stand filled up, have been made up and supplied and stand so, have been filled and stand filled, have been paid in full and stand so` | 15:16 |
| ἀντιπρόσωπος | `with the face towards` | `with the face towards and facing, face to face` | 15:10 |
| ἀπολύω | `I am loosed from` | `I am loosed from, I am undone, I am set free from and released, I am relieved from, I am acquitted, I am let go free on receipt of ransom and held to ransom, I am ransomed and redeemed, I am discharged and disbanded, I am dismissed, I am divorced, I am redeemed, I am done away with, I depart, I am set free from, I am released and let off, I am freed from, I am acquitted and discharged, I am separated and part` | 15:2 |
| ἀποσκευή | `of removal` | `of removal and riddance, of baggage, of household stuff, of ordure and filth` | 15:14 |
| ἀποστρέφω | `they will be turned` | `they will be turned, they will be turned back, they will be turned away, they will be brought back, they will turn oneself about` | 15:16 |
| ἀριθμέω | `number` | `number, count and reckon up, count out and pay, reckon and count as, be reckoned, be counted` | 15:5 |
| ἀστήρ | `the stars` | `the stars, the flames and lights and fires` | 15:5 |
| ἁμαρτία | `the failures` | `the failures, the faults and sins, the guilts and sins` | 15:16 |
| ἄτεκνος | `without children` | `without children and childless, destroying children` | 15:2 |
| ἐξάγω | `the one having led out` | `the one having led out, having led and carried out from, having brought forth into the world, having marched out, having ejected, having carried out and exported, having drawn off, having called forth and excited, having led on and tempted` | 15:7 |
| ἐξέρχομαι | `they will go out of` | `they will go out of, they will come out, they will go away and march off, they will go forth` | 15:14 |
| ἐξέρχομαι | `will go out of` | `will go out of, will come out, will go away and march off, will go forth` | 15:4 |
| ἐπειδή, ἐπεί | `after that` | `after that, after, since, when, from the time when and ever since, whenever, as soon as, seeing that, for, although, else and otherwise` | 15:3, 15:17 |
| ἐπιπίπτω | `falls upon` | `falls upon, attacks and assails` | 15:12 |
| ἔθνος | `the number of people accustomed to live together` | `the number of people accustomed to live together, the company and body of men, the host, the swarms and flocks, the nation and people, the nations and gentiles, the special class, the caste and tribe, the sex` | 15:14 |
| ἥλιος | `of sun` | `of sun, of day and a day, of Helios the sun-god` | 15:12 |
| ἥλιος | `the sun` | `the sun, the day and a day, Helios the sun-god` | 15:17 |
| ὄρνεον | `birds` | `birds, bird-market` | 15:11 |
| ὅραμα, with ἐν | `in that which is seen` | `within, inside of, and by means of that which is seen, a sight and spectacle` | 15:1 |
| ὑπερασπίζω | `I cover with a shield` | `I cover with a shield, I defend` | 15:1 |
| ὧδε | `in this wise` | `in this wise and so and thus, so very and so exceedingly, thus and as follows, hither and here` | 15:14, 15:16 |
| ῥῆμα | `that which is said` | `that which is said and spoken, a word, a saying, a phrase, the subject of speech and a thing, a verb` | 15:1 |
| ῥῆμα | `the things which are said` | `the things which are said and spoken, the words, the sayings, the phrases, the subjects of speech and things, the verbs` | 15:1 |

### Small words new in GEN 14

- πρός + dative — **headword** `hard by`, the entry's first sense for that case; **chain** `hard by,
  near, at, on, in, among, close to, before and in the presence of, upon and against, employed in,
  in addition to and besides`. 14:13.
- πλήν with a genitive — **headword** `more than`, the preposition's first sense; **chain** `more
  than, except, save, short of, save in respect, but, than, much like, only not, except that, save
  that, save so far as`, the adverb's senses after. 14:24.
- ἅμα with a dative — **headword** `at the same time with`, the preposition's sense; **chain** `at
  the same time with, together with, at once, at the same time`. 14:5.
- ὕψιστος — **headword** `highest`; **chain** `highest, loftiest`, one sense of two glosses, after a
  plain `the` for the article. 14:18–22.
- ἐν ἀριστερᾷ — **headword** `in left`, the chain of 13:9 after ἐν. 14:15.
- τὸ before an infinitive (μετὰ τὸ ἀναστρέψαι) — not printed, as at 5:4. 14:17.
- A dative after a preposition other than ἐν keeps its `to`, as at 12:8: `hard by to the tree`
  (14:13). A name in the dative with no article of its own takes `to` as a pronoun does: `to
  Abram` (14:13).
- ἔφυγον, ἔλαβον, ἀπῆλθον, ἔφαγον — first singular or third plural by form; the headword says
  `they`, as at 3:6. 14:10, 14:11, 14:12, 14:24.
- σεαυτῷ — `for yourself`, as at 6:14. 14:21.
- One sense each in GEN 14, so plain text: the numerals `twelve`, `thirteenth`, `fourteenth`, `three
  hundred`, `ten`, `eight`, `four`, `five`, with ἔτος `years`, `year`; αἰχμαλωτεύω `has been taken
  prisoner and stands taken prisoner`, the perfect's standing state (14:14); καταδιώκω `pursued
  closely` (14:14); συνάντησις `a meeting` (14:17); οἶνος `wine` (14:18); εὐλογητός `blessed` (14:20);
  σπαρτίον `of a small cord` (14:23); νεανίσκος `the youths` (14:24).

### Small words new in GEN 13

- ὅθεν — `from whom`, the chain of 10:14. 13:3.
- οὗ, *where* — `where`, plain, as at 2:11. 13:3, 13:4, 13:14.
- τὸ πρότερον — **headword** `the before`, the entry's first sense, with the article Rahlfs prints;
  **chain** `the before, the in front and forward, the former and sooner, the elder, the above and
  superior, the earlier` — *before, sooner, earlier* is the neuter as an adverb, the verse's use.
  Middle Liddell files the superlative πρῶτος inside the entry, and its senses are left out. 13:3.
- ἅμα with no dative — **headword** `at once`; **chain** `at once, at the same time, at the same time
  with and together with`. 13:6.
- ἀνὰ μέσον ἐμοῦ καὶ σοῦ — `up to middle` and then `of me and of you`, as at 9:12. 13:8.
- ἑαυτῷ after the middle ἐξελέξατο — `for himself`, plain, after the middle's own *for himself*,
  so the reading has it twice. 13:11.
- παρά + accusative — **headword** `to the side of`, the entry's first sense for that case;
  **chain** `to the side of, motion alongside of, to, beside and near and by, passing by, beyond,
  contrary to and against, beside and except, on account of and because of and by means of, along
  the whole course of and during`. 13:18.
- εἰμί — ἦν with a dative of possession, `was`, plain, as at 11:3 and 12:20 (13:5); ἦν of place or
  state, the formula of GEN 1:2 in full (13:3, 13:6, 13:18); ἦν with a participle, `was, and kept on
  being,` (13:10), where ὡς is a headword as well; ἔστω `let be`, ἐσμεν `we are` (13:8); ἐστιν `is`
  (13:9); εἶ `are` (13:14).
- One sense each in GEN 13, so plain text: διαχωρίζω `be separated`, `were separated`, `to be
  separated` (13:9, 13:11, 13:14); λίψ `south-west wind`, Middle Liddell's *the SW. wind* with the
  abbreviation written out (13:14); διοδεύω `travel through` (13:17), as at 12:6; ἀποσκηνόω `having
  kept apart from` (13:18), whose second sense is only *= ἀποσκηνέω*, with no translation;
  θυσιαστήριον `of the altar`, `an altar` (13:4, 13:18).

### Small words new in GEN 12

- καθάπερ — `according as`, the chain of καθά at 7:9, inside whose entry it is filed. 12:4.
- τότε — **headword** `at that time`; **chain** `at that time, then, in those times and formerly, at
  one time`. 12:6.
- ὅπως with ἄν — **headword** `that`, the first conjunction sense; **chain** `that, in order that, as
  and in such manner as, how and in what manner`. 12:13.
- εὖ — **headword** `well`; **chain** `well, luckily, happily, well off`. 12:13, 12:16.
- ἕνεκεν — `on account of`, the chain of 2:24; περί + genitive — **headword** `round about`, the
  entry's first sense for that case; **chain** `round about, around, about and near, about and for
  and on account of, about and concerning, for very`. 12:13, 12:17, 12:20.
- τί τοῦτο — `why this`, as at 3:13; ἵνα τί — `that what`, as at 4:6. 12:18, 12:19.
- ἐμαυτῷ — `for myself`, plain, as the reflexives are. 12:19.
- One sense each in GEN 12, so plain text: εὐλογητός `blessed` (12:2); ἐνευλογέομαι `will be blessed
  in` (12:3), followed by the Greek's own ἐν σοί, *in you*; διοδεύω `travelled through` (12:6);
  συμπροπέμπω `to join in escorting` (12:20); θυσιαστήριον `an altar` (12:7, 12:8); ἀδελφή
  `sister` (12:13, 12:19).

### Small words new in GEN 11

- δεῦτε — **headword** `hither`; **chain** `hither, come on, come here`: one sense holding three
  glosses, a unit as ἐμφυσάω's was. 11:3, 11:4, 11:7.
- πλησίον with the article, *the neighbour* — **headword** `to the neighbour` · `of the neighbour`,
  the first noun sense inside πλησίος; **chain** `to the neighbour, to the one near and close to and
  neighbouring, to the one nigh and hard by, to one's neighbour`, in the case. 11:3, 11:7.
- ἐνώπιον — `face to face`, plain: the one translation ἐνώπιος is given; the preposition, *like
  Lat. coram*, has none. 11:28.
- νῦν — **headword** `now`; **chain** `now, even now, just now`, as at 2:23. 11:6.
- ἵνα — `that`, the chain of 3:3; ὅτε — `when`, the chain of 2:4. 11:7, 11:10.
- οὗ, *whose* (11:4) — `of which`, plain, as other relatives.
- ᾗ with no preposition (11:28) — `in which`, plain, as at 5:1.
- One sense each in GEN 11, so plain text: πλίνθος `bricks`, `the brick` (11:3); τεκνοποιέω `was
  bearing children`, the active's one sense (11:30); ἐνώπιον `face to face` (11:28); θυγάτηρ
  `daughter`; the numerals and `years`; δεύτερος `second` (11:10), with no article, as the Greek
  has none.
- The short imperfect, `was, and kept on being,`, at 11:1, where the full formula's *one* would
  stand beside εἷς's headword.

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

### Verbs new in GEN 5

| lemma | form | headword | chain | used |
| --- | --- | --- | --- | --- |
| ποιέω | aor. 3 sg | `made` | the chains of GEN 1:1 (full) and 2:2 (short) | 5:1, 5:2 |
| εὐλογέω | aor. 3 sg | `spoke well of` | the chain of GEN 2:3; Rahlfs prints εὐλόγησεν here without the augment | 5:2 |
| ἐπονομάζω | aor. 3 sg | `gave a surname` | the chain of GEN 4:17 | 5:2, 5:3, 5:29 |
| ζάω | aor. 3 sg | `lived` | `lived, was in full life and strength, was fresh and strong` — the chain of GEN 3:22, in the aorist | 5:3–30 |
| γεννάω | aor. 3 sg / aor. inf. | `begot` · `to beget` | the chain of GEN 4:18, in the form | 5:3–32 |
| γίνομαι | aor. 3 pl | `came into being` | `came to be, arose, were brought into existence` — no *there*, the subject standing in the clause | 5:4–31 |
| ἀποθνήσκω | aor. 3 sg | `died off` | `died off, died, was put to death, was slain` | 5:5–31 |
| εὐαρεστέω | aor. 3 sg | `was well pleasing` | `was well pleasing, seemed good, was resolved, was well pleased and satisfied` — **no Middle Liddell entry**; LSJ, citing 5:22. The passive's own senses are left out; *well pleased* is also the active's, used intransitively | 5:22, 5:24 |
| εὑρίσκω | impf. pass. 3 sg | `was being found` | `was being found, was being found out, was being discovered` | 5:24 |
| μετατίθημι | aor. 3 sg | `placed among` | `placed among, placed differently, transposed, changed and altered, put in the place of another and substituted` — the entry's *Mid.* and *Pass.* senses left out | 5:24 |
| λέγω | pres. ptcp. | `saying` | the chain of GEN 2:16 | 5:29 |
| διαναπαύω | fut. 3 sg | `will allow to rest awhile` | `will allow to rest awhile, will interrupt, will relieve, will rest awhile` — LSJ's active; Middle Liddell has only the middle | 5:29 |
| καταράομαι | aor. mid. 3 sg | `called down curses upon` | `called down curses upon, imprecated upon, cursed and execrated, uttered imprecations` — *accursed*, the entry's sense for the perfect passive participle alone, left out | 5:29 |

Every verb of the genealogy's frame is aorist. The aorist formula stands after the first
aorist of 5:1 and 5:3 and after εὐηρέστησεν and μετέθηκεν (5:22, 5:24), not after each of the
chapter's sixty-seven aorist indicatives, as GEN 4:18 set it once in a run of ἐγέννησεν.

### Verbs new in GEN 6

| lemma | form | headword | chain | used |
| --- | --- | --- | --- | --- |
| γίνομαι | pres. inf. | `to come into being` | the chain of GEN 2:5 | 6:1 |
| ἄρχω | aor. mid. 3 pl | `began` | the chain of GEN 2:3 | 6:1 |
| ὁράω | aor. ptcp. / aor. 3 sg | `having seen` · `saw` | `having seen, having perceived, having beheld, having looked at`; the chain of GEN 3:6 | 6:2, 6:5, 6:12 |
| λαμβάνω | aor. 3 pl / fut. 2 sg | `they took` · `you will take` | the chain of GEN 2:15, in the form | 6:2, 6:21 |
| ἐκλέγομαι | aor. 3 pl | `they picked out for themselves` | `they picked out for themselves, they chose out, they pulled out` — the entry's *Mid.*; its actives, *to pick, single out* and *to levy taxes*, left out | 6:2 |
| καταμένω | aor. subj. 3 sg | `may stay behind` | `may stay behind, may stay, may remain fixed, may continue` | 6:3 |
| εἰμί | pres. inf. | `to be` | the chain of GEN 2:18 | 6:3 |
| εἰσπορεύομαι | impf. 3 pl | `were going into` | `were going into, were entering` — the entry's passive gloss; *to lead into*, the active, left out | 6:4 |
| γεννάω | impf. 3 pl | `were begetting` | `were begetting, were engendering, were bringing forth, were producing` | 6:4 |
| πληθύνω | aor. pass. 3 pl | `were made full` | `were made full, were increased, were multiplied, were in the majority, prevailed` — the passive's own gloss last | 6:5 |
| διανοέομαι | pres. / aor. 3 sg | `is minded` · `was minded` | `is minded, intends, purposes, thinks over, thinks of, thinks and supposes, is disposed`, in the form | 6:5, 6:6 |
| ἐνθυμέομαι | aor. 3 sg | `laid to heart` | `laid to heart, considered well, reflected on, pondered, thought much and deeply of, took to heart, was hurt and angry at, thought out a thing and formed a plan, inferred and concluded` | 6:6 |
| ἀπαλείφω | fut. 1 sg | `I will wipe off` | `I will wipe off, I will expunge, I will cancel` | 6:7 |
| ποιέω | aor. 1 sg / impv. / fut. 2 sg | `I made` · `make` · `you will make` | `I fashioned, I wrought, I produced, I performed, I did`, the chain of GEN 3:13 · `make, do, produce, create` · `you will make, you will do, you will produce, you will create` | 6:7, 6:14–16 |
| θυμόομαι | aor. pass. 1 sg | `I was wroth` | `I was wroth, I was angry, I was wild and restive, I vented fury, I was angry with, I was angry at` — *to make angry*, the active, left out | 6:7 |
| εὑρίσκω | aor. 3 sg | `found` | `found, found out, discovered` | 6:8 |
| φθείρω | aor. pass. 3 sg | `was ruined` | `was ruined, was wasted, was spoiled, was destroyed, went to ruin, perished` — the passive's own gloss last | 6:11 |
| πίμπλημι | aor. pass. 3 sg | `was filled full of` | `was filled full of, was filled with, was filled up and filled, became full of and was full of, had enough of` — sense III, *Pass.*, last | 6:11, 6:13 |
| καταφθείρω | perf. pass. ptcp. / aor. 3 sg / pres. 1 sg / aor. inf. | `having been destroyed` · `destroyed` · `I destroy` · `to destroy` | `destroyed, spoiled utterly, brought to naught`, in the form; the perfect, `having been destroyed and standing destroyed, having been spoiled utterly and remaining so, having been brought to naught and remaining so` | 6:12, 6:13, 6:17 |
| ἥκω | pres. 3 sg | `has come` | `has come, is present, is here, has returned, has reached a point` — the entry's own perfect sense | 6:13 |
| συντελέω | fut. 2 sg | `you will bring quite to an end` | the active chain of GEN 2:2, in the future | 6:16 |
| ἐπισυνάγω | pres. ptcp. | `collecting and bringing to` | `collecting and bringing to, gathering together` | 6:16 |
| ἐπάγω | pres. 1 sg | `I bring on` | `I bring on, I bring upon, I set on and urge on, I lead on, I bring in and invite, I bring to, I lay on and apply, I bring forward, I add` | 6:17 |
| τελευτάω | fut. 3 sg | `will complete` | `will complete, will finish, will accomplish, will fulfil, will bring about, will bring to an end, will make an end of, will end life and die, will come to an end` — the entry's passives left out | 6:17 |
| ἵστημι | fut. 1 sg | `I will make to stand` | `I will make to stand, I will set, I will stop and stay and check, I will set up and raise, I will establish and institute, I will appoint, I will weigh` — the causal tenses | 6:18 |
| εἰσέρχομαι | fut. 2 sg / 3 pl | `you will go in` · `will go in` | `you will go in, you will go into and enter, you will come into, you will come in, you will come upon`, in the form | 6:18, 6:20 |
| εἰσάγω | fut. 2 sg | `you will lead in` | `you will lead in, you will lead into and introduce, you will admit, you will import, you will call in, you will bring in and bring forward` | 6:19 |
| τρέφω | pres. subj. 2 sg / pres. inf. mid.-pass. | `you may thicken` · `to be thickened` | `you may thicken, you may congeal, you may curdle, you may make to grow and increase, you may bring up and breed and rear, you may rear and keep, you may let grow and cherish and foster, you may produce and teem with, you may contain and have, you may maintain and support` · `to be thickened, to be congealed, to be curdled, to become firm, to be made to grow and increase, to be brought up and bred and reared, to rear for oneself, to be kept, to be let grow and cherished and fostered, to be maintained and supported` | 6:19, 6:20 |
| ἕρπω | pres. ptcp. gen. pl., articular | `of the creeping` | `of the creeping, of the crawling, of the moving slowly and walking, of the going and coming, of the stealing on and spreading` | 6:20 |
| ἐσθίω | fut. 2 pl / aor. inf. | `you will eat` · `to eat` | the chains of GEN 2:16 and 3:11 | 6:21 |
| συνάγω | fut. 2 sg | `you will bring together` | `you will bring together, you will gather together and collect and convene, you will join, you will unite, you will receive into your house, you will gather in stores, you will draw together, you will conclude and infer` | 6:21 |
| ἐντέλλομαι | aor. 3 sg | `enjoined` | the chain of GEN 2:16 | 6:22 |

τρέφω is this chapter's σπέρμα: the verb for keeping the animals alive reads, in the lexicon's
order, *thicken* and *congeal* before *rear*, *keep* and *maintain*.

### Verbs new in GEN 7

| lemma | form | headword | chain | used |
| --- | --- | --- | --- | --- |
| εἰσέρχομαι | aor. impv. / aor. 3 sg and 3 pl | `go in` · `went in` | the chain of GEN 6:18, in the form | 7:1–16 |
| εἰσπορεύομαι | pres. ptcp. n. pl., articular | `the ones going into` | `the ones going into, the ones entering` | 7:16 |
| ὁράω | aor. 1 sg | `I saw` | `I saw, I perceived, I beheld, I looked at` | 7:1 |
| εἰσάγω | aor. impv. | `lead in` | the chain of GEN 6:19, in the imperative | 7:2 |
| ἐπάγω | pres. 1 sg | `I bring on` | the chain of GEN 6:17 | 7:4 |
| ἐξαλείφω | fut. 1 sg / aor. 3 sg / aor. pass. 3 pl | `I will plaster` · `plastered` · `were plastered` | `I will plaster, I will wash over, I will wipe out and obliterate, I will strike off, I will destroy utterly`, in the form — *to plaster* or *wash over* is sense I, *to wipe out* sense II | 7:4, 7:23 |
| ῥήγνυμι | aor. pass. 3 pl | `were broken` | `were broken, were broken asunder and in pieces, were rent and shivered and shattered, burst, burst forth` — the entry's *Pass.* last | 7:11 |
| ἀνοίγω | aor. pass. 3 pl | `were opened` | `were opened, were undone, were laid open and unfolded and disclosed, were open and stood open` — the passive's own gloss last | 7:11 |
| κινέω | pres. mid.-pass. ptcp. | `being set in motion` | `being set in motion, being moved, being removed, being roused and stirred up, being put in motion, moving and stirring, moving forward` — the entry's *Pass.* after the first senses | 7:14, 7:21 |
| κλείω | aor. 3 sg | `shut` | `shut, closed, barred, shut up and blocked, confined` | 7:16 |
| πληθύνω | aor. pass. / impf. mid.-pass. 3 sg | `was made full` · `was being made full` | the chain of GEN 6:5, in the form | 7:17, 7:18 |
| ἐπαίρω | aor. 3 sg | `lifted up and set on` | `lifted up and set on, lifted and raised, exalted and magnified, stirred up and excited, induced and persuaded` | 7:17 |
| ὑψόω | aor. pass. 3 sg | `was lifted high` | `was lifted high, was raised up, was elevated and exalted` | 7:17, 7:20, 7:24 |
| ἐπικρατέω | impf. 3 sg | `was ruling over` | `was ruling over, was holding power, was prevailing and conquering, was getting the mastery, was superior` | 7:18, 7:19 |
| ἐπιφέρω | impf. mid.-pass. 3 sg | `was being brought upon` | the chain of GEN 1:2, word for word, in the same phrase | 7:18 |
| ἐπικαλύπτω | aor. 3 sg | `covered over` | `covered over, covered up, shrouded, put as a covering over` | 7:19, 7:20 |
| ἔχω | pres. 3 sg | `has` | `has, holds, possesses, keeps, dwells in and inhabits, holds fast, bears up against and supports` | 7:22 |
| καταλείπω | aor. pass. 3 sg | `was left behind` | the chain of GEN 2:24, in the passive | 7:23 |
| ἀποθνήσκω | aor. 3 sg | `died off` | the chain of GEN 5:5 | 7:21, 7:22 |

ἐπεφέρετο ἡ κιβωτὸς ἐπάνω τοῦ ὕδατος at 7:18 repeats 1:2's πνεῦμα θεοῦ ἐπεφέρετο ἐπάνω τοῦ ὕδατος,
where the Hebrew has *face of* at both; the chain of 1:2 is reused verbatim, and *face of the
waters* is refused by `validate.py` here as there.

### Verbs new in GEN 8

| lemma | form | headword | chain | used |
| --- | --- | --- | --- | --- |
| μιμνήσκομαι | aor. pass. 3 sg | `reminded himself of` | `reminded himself of, called to mind, remembered, bethought himself of, was minded, bore in mind and did not forget` — the entry's *Mid. and Pass.*; *to remind*, the active, left out | 8:1 |
| ἐπάγω | aor. 3 sg | `brought on` | the chain of GEN 6:17, in the aorist | 8:1 |
| κοπάζω | aor. / perf. 3 sg | `grew weary` · `has grown weary` | `grew weary, abated` · `has grown weary and stands so, has abated and remains abated` | 8:1, 8:7, 8:8, 8:11 |
| ἐπικαλύπτω | aor. pass. 3 pl | `were covered over` | the chain of GEN 7:19, in the passive | 8:2 |
| συνέχω | aor. pass. 3 sg | `was held together` | `was held together, was kept together, was enclosed and encompassed and embraced, was kept from dispersing, was constrained and forced, was compressed and oppressed, was afflicted` | 8:2 |
| ἐνδίδωμι | impf. 3 sg | `was giving in` | `was giving in, was giving into hands and giving up to, was lending, was giving, was causing and exciting, was showing and exhibiting, was allowing and granting and conceding, was giving way, was yielding` | 8:3 |
| πορεύομαι | pres. ptcp. | `being driven` | the chain of GEN 2:14 | 8:3, 8:5 |
| καθίζω | aor. 3 sg | `made to sit down` | `made to sit down, seated, set and placed, encamped, set up, sat down and was seated and took its seat, settled and sank in` — the causal first, as ὑπνόω at 2:21 | 8:4 |
| ὁράω | aor. pass. 3 pl / aor. inf. / aor. 3 sg | `were seen` · `to see` · `saw` | `were seen, were looked at, were beheld and perceived and observed, were looked out for`; the chains of GEN 2:19 and 3:6 | 8:5, 8:7, 8:8, 8:13 |
| ἀνοίγω | aor. 3 sg | `opened` | `opened, undid, laid open and unfolded and disclosed, got into the open sea` | 8:6 |
| ἀποστέλλω | aor. 3 sg | `sent off` | `sent off, sent away, banished, despatched, went away and departed` | 8:7, 8:8 |
| ἐξέρχομαι | aor. ptcp. / aor. 3 sg and 3 pl / aor. impv. | `having gone out of` · `went out of` · `go out of` | the chain of GEN 4:16, in the form | 8:7, 8:16, 8:18, 8:19 |
| ὑποστρέφω | aor. 3 sg | `turned round about` | `turned round about, turned back, turned about and turned short round, returned, turned away and eluded` | 8:7, 8:9 |
| ξηραίνω | aor. pass. inf. / aor. pass. 3 sg | `to be parched up` · `was parched up` | `to be parched up, to be dried up, to become dry and be parched, to be laid dry`, in the form | 8:7, 8:14 |
| εὑρίσκω | aor. ptcp. fem. | `having found` | `having found, having found out, having discovered, having gotten and gained` | 8:9 |
| ἐκτείνω | aor. ptcp. | `having stretched out` | the chain of GEN 3:22, in the participle | 8:9 |
| λαμβάνω, εἰσάγω | aor. 3 sg | `took` · `led in` | the chains of GEN 2:15 and 6:19, in the aorist | 8:9, 8:20 |
| ἐπέχω | aor. ptcp. | `having held upon` | `having held upon, having held out and presented and offered, having directed towards and aimed at, having intended and purposed, having faced, having kept in and held back and checked, having stayed and stopped and waited and paused, having reached and extended over` | 8:10, 8:12 |
| ἐξαποστέλλω | aor. 3 sg | `sent quite away` | the chain of GEN 3:23 | 8:10, 8:12 |
| ἀναστρέφω | aor. 3 sg | `turned upside down` | `turned upside down, upset, turned back and brought back, rallied, turned back and returned and retired, dwelt, conducted herself, revolved, faced about` | 8:11 |
| ἔχω | impf. 3 sg | `was having` | the chain of GEN 7:22, in the imperfect | 8:11 |
| γινώσκω | aor. 3 sg | `learned to know` | the chain of GEN 4:1 | 8:11 |
| προστίθημι | aor. mid. 3 sg / fut. 1 sg | `put to` · `I will put to` | the chain of GEN 4:2, in the form | 8:12, 8:21 |
| ἐπιστρέφω | aor. inf. | `to turn about` | `to turn about, to turn round, to return, to turn towards, to correct and make to repent` | 8:12 |
| ἐκλείπω | aor. 3 sg | `left out` | `left out, omitted and passed over, forsook and deserted and abandoned, suffered an eclipse, died, left off and ceased and stopped, failed and was wanting` | 8:13 |
| ἀποκαλύπτω | aor. 3 sg | `uncovered` | `uncovered, disclosed and revealed, revealed his whole mind` | 8:13 |
| ἐξάγω | aor. impv. | `lead out` | `lead out, lead and carry out from, bring forth into the world, march out, eject, carry out and export, draw off, call forth and excite, lead on and tempt` | 8:17 |
| αὐξάνω | pres. impv. pass. 2 pl | `be made large` | `be made large, be increased and augmented, be increased in power and strengthened and exalted, be promoted to honour and glorified and magnified, grow and wax and increase, grow up` — the passive's own *to grow* last | 8:17 |
| πληθύνω | pres. impv. pass. 2 pl | `be made full` | `be made full, be increased, be multiplied, be in the majority, prevail` | 8:17 |
| οἰκοδομέω | aor. 3 sg | `built a house` | the chain of GEN 2:22 | 8:20 |
| ἀναφέρω | aor. 3 sg | `brought up` | `brought up, carried up, carried up the country, took with him, poured forth, heaved and uttered, upheld and took upon himself, offered and contributed, led up, carried back and recovered, brought back and reported, traced up` | 8:20 |
| ὀσφραίνομαι | aor. 3 sg | `caught scent of` | `caught scent of, smelled, scented, tracked` | 8:21 |
| διανοέομαι | aor. ptcp. | `having been minded` | the chain of GEN 6:6, in the participle | 8:21 |
| καταράομαι | aor. inf. | `to call down curses upon` | the chain of GEN 5:29, in the infinitive | 8:21 |
| ἔγκειμαι | pres. 3 sg | `lies in` | `lies in, is wrapped in, is involved in, presses upon, is urgent and insists, is devoted to` | 8:21 |
| πατάσσω | aor. inf. | `to beat` | `to beat, to knock, to strike and smite, to knock at` | 8:21 |
| καταπαύω | fut. 3 pl | `will lay to rest` | the chain of GEN 2:2, in the future | 8:22 |

### Verbs new in GEN 9

| lemma | form | headword | chain | used |
| --- | --- | --- | --- | --- |
| εὐλογέω | aor. 3 sg | `spoke well of` | the chain of GEN 2:3 | 9:1 |
| αὐξάνω, πληθύνω | pres. impv. pass. 2 pl | `be made large` · `be made full` | the chains of GEN 8:17 | 9:1, 9:7 |
| πληρόω | aor. impv. 2 pl | `make full` | `make full, fill full of, fill full, gorge and satiate, glut, fill with, man, make complete, fill, fulfil and pay in full and make up, come in full` — the entry's passives and middles left out | 9:1, 9:7 |
| κινέω | pres. mid.-pass. ptcp. n. pl., articular | `the ones being set in motion` | the chain of GEN 7:14, with the article | 9:2 |
| δίδωμι | perf. 1 sg / pres. 1 sg | `I have given` · `I give` | `I have given and it stands given, I have granted and it stands granted, I have provided and it stands provided, I have given over and delivered up and it stands so` · `I give, I am ready to give and offer, I grant, I provide, I give over and deliver up` — *to be ready to give* is the entry's present | 9:2, 9:3, 9:12 |
| ἐσθίω | fut. 2 pl | `you will eat` | the chain of GEN 2:17 | 9:4 |
| ἐκζητέω | fut. 1 sg | `I will seek out` | `I will seek out, I will enquire, I will demand an account of` | 9:5 |
| ἐκχέω | pres. ptcp., articular / fut. pass. 3 sg | `the one pouring out` · `will be poured out` | `the one pouring out, the one pouring out like water, the one squandering and wasting` · `will be poured out, will be poured out like water, will be squandered and wasted, will stream out and forth, will be spread out, will be forgotten, will be overjoyed, will burst out, will lie languidly` — the passive's own senses last | 9:6 |
| ποιέω | aor. 1 sg / aor. 3 sg | `I made` · `made` | the chain of GEN 6:7 · `fashioned, wrought, produced, performed, did`, the same in the third person | 9:6, 9:24 |
| λέγω | aor. 3 sg / pres. ptcp. | `said` · `saying` | the chains of GEN 2:16–18 | 9:1–26 |
| ἀνίστημι | pres. 1 sg | `I make to stand up` | `I make to stand up, I raise up, I raise from sleep and wake up, I raise from the dead, I set up and build, I build up again and restore, I put up for sale, I rouse to action and stir up, I rouse to arms and raise, I make rise and break up, I make rise and emigrate and transplant, I make rise and leave sanctuary, I put up and spring` — sense A, *Causal in pres., imperf.* | 9:9 |
| ἐξέρχομαι | aor. ptcp. pl., articular | `the ones having gone out of` · `of the ones …` | the chain of GEN 4:16, in the form | 9:10, 9:18, 9:22 |
| ἵστημι | fut. 1 sg | `I will make to stand` | the chain of GEN 6:18 | 9:11 |
| ἀποθνήσκω | fut. 3 sg / aor. 3 sg | `will die off` · `died off` | the chains of GEN 2:17 and 5:5, in the form | 9:11, 9:29 |
| καταφθείρω | aor. inf. | `to destroy` | the chain of GEN 6:17 | 9:11 |
| τίθημι | pres. 1 sg | `I set` | `I set, I put, I place, I plant, I lay` | 9:13 |
| συννεφέω | pres. inf., articular with ἐν | `in the collecting clouds` | `within, inside of, and by means of the collecting clouds, the being cloudy, the wearing a clouded look` | 9:14 |
| ὁράω | fut. pass. 3 sg / fut. mid. 1 sg / aor. 3 sg and 3 pl | `will be seen` · `I will see` · `saw` | the chains of GEN 8:5, 7:1 and 3:6, in the form | 9:14, 9:16, 9:22, 9:23 |
| μιμνήσκομαι | fut. pass. 1 sg / aor. pass. inf. | `I will remind myself of` · `to remind oneself of` | the chain of GEN 8:1, in the form | 9:15, 9:16 |
| ἐξαλείφω | aor. inf. | `to plaster` | the chain of GEN 7:4, in the infinitive | 9:15 |
| διατίθεμαι | aor. mid. 1 sg | `I arranged as I liked` | `I arranged as I liked, I disposed of, I disposed of my property and devised it by will, I set out for sale and disposed of, I arranged mutually, I made a covenant with, I settled with` — the entry's *B. Mid.*; its actives left out | 9:17 |
| διασπείρω | aor. pass. 3 pl | `were scattered abroad` | `were scattered abroad, were thrown about, were squandered` | 9:19 |
| ἄρχω | aor. mid. 3 sg | `began` | the chain of GEN 2:3 | 9:20 |
| φυτεύω | aor. 3 sg | `planted` | the chain of GEN 2:8 | 9:20 |
| πίνω | aor. 3 sg | `drank` | `drank, drank of, drank up` — *to be drunk*, the perfect's, left out | 9:21 |
| μεθύσκω | aor. pass. 3 sg | `was made drunk` | `was made drunk, was intoxicated and inebriated, was given to drink and watered and moistened, drank freely, got drunk, was drunk` — the passive's own senses last | 9:21 |
| γυμνόω | aor. pass. 3 sg | `was stripped naked` | `was stripped naked, was stripped, was left naked and exposed, was left bare and defenceless, stripped himself naked` | 9:21 |
| ἀναγγέλλω | aor. 3 sg | `carried back tidings of` | the chain of GEN 3:11 | 9:22 |
| λαμβάνω | aor. ptcp. pl. | `having taken` | the chain of GEN 3:6 | 9:23 |
| ἐπιτίθημι | aor. mid. 3 pl | `put on themselves` | `put on themselves, put on for themselves, set themselves to and applied themselves to and employed themselves on, made an attempt upon and attacked, brought on themselves, caused to be imposed, laid commands on, gave` — the entry's *B. Mid.* | 9:23 |
| πορεύομαι | aor. pass. 3 pl | `were driven` | the chain of GEN 2:14, in the aorist | 9:23 |
| συγκαλύπτω | aor. 3 pl | `covered` | `covered, veiled completely` — the passive's *muffled up* and the middle's *to wrap oneself up* left out | 9:23 |
| ἐκνήφω | aor. 3 sg | `slept off a drunken fit` | `slept off a drunken fit, became sober again` — one sense holding two glosses, a unit as ἐμφυσάω's was at 2:7 | 9:24 |
| γινώσκω | aor. 3 sg | `learned to know` | the chain of GEN 4:1 | 9:24 |
| πλατύνω | aor. opt. 3 sg | `may widen` | `may widen, may make wide` — the middle's and passive's senses left out | 9:27 |
| κατοικέω | aor. impv. 3 sg | `let dwell in` | `let dwell in, let settle in, let colonise, let inhabit, let settle and dwell, let lie and be situate` — the first translation reads *to dwell in as a* κάτοικος; the headword stops before the Greek | 9:27 |
| γίνομαι | aor. pass. impv. 3 sg / aor. 3 pl | `let come into being` · `came into being` | `let come to be, let arise, let be brought into existence`; the chain of GEN 5:5 | 9:27, 9:29 |
| ζάω | aor. 3 sg / pres. ptcp. | `lived` · `living` | the chains of GEN 5:3 and 2:7, in the form | 9:3, 9:10, 9:12, 9:28 |

### Verbs new in GEN 14

| lemma | form | headword | chain | used |
| --- | --- | --- | --- | --- |
| γίνομαι | aor. 3 sg | `came into being` | the chain of GEN 12:10 | 14:1 |
| ποιέω | aor. 3 pl | `made` | the chain of GEN 9:24 | 14:2 |
| συμφωνέω | aor. 3 pl | `agreed in sound` | `agreed in sound, were in harmony, agreed with and held the same opinions with, made an agreement and bargained with, agreed, conspired` | 14:3 |
| δουλεύω | impf. 3 pl | `were being slaves` | `were being slaves, were serving and being subject to` | 14:4 |
| ἀφίστημι | aor2 3 pl | `stood away` | the chain of GEN 12:8 | 14:4 |
| ἔρχομαι | aor. 3 sg · aor. 3 pl | `came` | the chain of GEN 10:19, in the form | 14:5, 14:7 |
| κατακόπτω | aor. 3 pl | `cut down` | `cut down, cut in pieces and cut up, killed and slew, broke in pieces and destroyed, coined into money` | 14:5, 14:7 |
| ἀναστρέφω | aor. ptcp. · aor. inf. | `having turned upside down` · `to turn upside down` | the chain of GEN 8:11, in the form, with the lexicon's *oneself* for 8:11's *herself* | 14:7, 14:17 |
| κατοικέω | pres. ptcp., articular · pres. ptcp. · impf. 3 sg | `the ones dwelling in` · `dwelling in` · `was dwelling in` | the chain of GEN 9:27, in the form | 14:7, 14:12, 14:13 |
| ἐξέρχομαι | aor. 3 sg | `went out of` | the chain of GEN 4:16 | 14:8, 14:17 |
| παρατάσσω | aor. mid. 3 pl | `drew up one's men in battle-order` | `drew up one's men in battle-order, were drawn up along, stood prepared` — the middle, its active *to place side by side* left out | 14:8 |
| φεύγω | aor. 3 sg · aor. 3 pl | `fled` · `they fled` | `fled, took flight and ran away, had recourse and took refuge, was shy of doing and shrank from doing, shrank back, fled from and shunned and avoided, fled the consequences of, fled one's country, was banished, went into exile and was an exile, was accused and prosecuted, was put on one's trial for, was charged with`, in the form | 14:10 |
| ἐμπίπτω | aor. 3 pl | `fell in` | `fell in, fell upon and attacked, lit and chanced upon, fell in with, broke in and burst in` | 14:10 |
| καταλείπω | aor. pass. ptcp., articular | `the ones having been left behind` | the chain of GEN 7:23, in the participle | 14:10 |
| λαμβάνω | aor. 3 pl · aor. impv. · fut. 1 sg and 3 pl | `they took` · `take` · `I will take` · `they will take` | the chain of GEN 2:15, in the form | 14:11, 14:12, 14:21, 14:23, 14:24 |
| ἀπέρχομαι | aor. 3 pl | `they went away` | the chain of GEN 3:19, in the aorist | 14:11 |
| ἀποίχομαι | impf. 3 pl | `were being gone away` | `were being gone away and far from, were being gone and had departed and were being absent, were being gone and had perished, were being dead and gone` | 14:12 |
| παραγίνομαι | aor. ptcp. | `having been near` | `having been near and attended upon, having been present at, having come to one's side and come to aid and stood by and seconded and supported, having been at hand and been gained and accrued, having come to, having arrived and come up, having come to maturity, having been fully grown` — Perseus tags *near, attend upon* inside *to be beside, to be by or near*, and the headword takes *been* from there | 14:13 |
| ἀνασώζω | aor. pass. ptcp., articular gen. | `of the ones having been recovered` | `of the ones having been recovered and rescued, of the ones having returned safe` — the first sense in the passive, the entry's *Pass.* after it, its middles left out | 14:13 |
| ἀπαγγέλλω | aor. 3 sg | `brought tidings` | the chain of GEN 12:18, in the third person | 14:13 |
| ἀκούω | aor. ptcp. | `having heard` | the chain of GEN 3:8, in the participle | 14:14 |
| ἀριθμέω | aor. 3 sg | `numbered` | `numbered, counted and reckoned up, counted out and paid, reckoned and counted as, was reckoned, was counted` | 14:14 |
| ἐπιπίπτω | aor. 3 sg | `fell upon` | `fell upon, attacked and assailed` | 14:15 |
| πατάσσω | aor. 3 sg | `beat` | the chain of GEN 8:21, in the aorist | 14:15 |
| διώκω | aor. 3 sg | `pursued` | `pursued, chased and hunted, was a follower of and attached oneself and sought after, followed and waited for, drove and chased away and banished, impelled and sped on her way, urged on, drove and drove on, galloped and sped and ran, prosecuted and brought an action against, accused of and prosecuted for, avenged` | 14:15 |
| ἀποστρέφω | aor. 3 sg | `turned` | the chain of GEN 3:19, in the aorist | 14:16 |
| ὑπάρχω | pres. ptcp. n. pl., as a noun | `the existing circumstances` | the chain of GEN 12:5 | 14:16 |
| ἐκφέρω | aor. 3 sg | `carried out of` | `carried out of, carried out, carried off, carried out of the sea and threw ashore, brought forth, brought forth and produced, brought about and accomplished, brought out and published, delivered, brought forward, disclosed and told and betrayed, put forth and exerted, bore the marks of, carried to a certain point, shot forth, ran away, came to fulfilment and came to an end, came to land and was cast ashore, was carried beyond bounds and carried away` — the passives last | 14:18 |
| εὐλογέω | aor. 3 sg · perf. pass. ptcp. | `spoke well of` · `having been spoken well of` | the chain of GEN 2:3 · `having been spoken well of and remaining so, having been praised and standing praised, having been honoured and standing honoured, having been blessed and standing blessed` | 14:19 |
| κτίζω | aor. 3 sg | `peopled` | `peopled, built houses and cities, colonised, founded and planted and built, planted, set up, established, created and brought into being and brought about, made, perpetrated, was founded` — *to create* is its sixth sense | 14:19, 14:22 |
| παραδίδωμι | aor. 3 sg | `gave` | `gave, handed over to another and transmitted, transmitted and imparted, delivered up and surrendered, betrayed, committed, gave up, handed down, granted and bestowed, offered and allowed` | 14:20 |
| δίδωμι | aor. 3 sg · aor. impv. | `gave` · `give` | the chain of GEN 3:6, in the form | 14:20, 14:21 |
| ἐκτείνω | fut. 1 sg | `I will stretch out` | the chain of GEN 3:22, in the future | 14:22 |
| λέγω | aor. subj. 2 sg | `you may say` | the chain of GEN 2:16, in the subjunctive | 14:23 |
| πλουτίζω | aor. 1 sg | `I made wealthy` | `I made wealthy and enriched, I gained one's wealth` — the middle's sense last | 14:23 |
| ἐσθίω | aor. 3 pl | `they ate` | the chain of GEN 3:6 | 14:24 |
| συμπορεύομαι | aor. ptcp., articular gen. | `of the ones having gone` | the chain of GEN 13:5, in the form | 14:24 |

### Verbs new in GEN 13

| lemma | form | headword | chain | used |
| --- | --- | --- | --- | --- |
| ἀναβαίνω | aor. 3 sg | `went up` | `went up, mounted, went up to, embarked` — the chain of GEN 2:6, in the aorist | 13:1 |
| πορεύομαι | aor. pass. 3 sg | `was driven` | the chain of GEN 12:4 | 13:3 |
| ἔρχομαι | aor. 3 sg · aor. inf. · aor. ptcp. | `came` · `to come` · `having come` | the chains of GEN 10:19, in the form | 13:3, 13:10, 13:18 |
| ποιέω | aor. 3 sg · fut. 1 sg | `made` · `I will make` | the chains of GEN 9:24 and 12:2 | 13:4, 13:16 |
| ἐπικαλέω | aor. mid. 3 sg | `called upon` | the chain of GEN 12:8 | 13:4 |
| συμπορεύομαι | pres. ptcp., articular dat. | `to the one going` | `to the one going, to the one journeying together, to the one coming together` — Middle Liddell's *to go or journey together*, tagged in two pieces; its *with* is the case it takes | 13:5 |
| χωρέω | impf. 3 sg | `was making room for another` | `was making room for another, was giving way and drawing back and retiring and withdrawing, was putting back and retiring, was giving way to, was retiring before, was going forward and moving on, was going and coming, was going on one's journey and travelling, was coming to, was coming on and beginning, was passing and near an end, was going on and advancing, was coming to an issue and turning out, was going on well and succeeding, was spreading abroad, was spreading, was having room for, was holding and containing` — *to hold, contain*, the verse's sense, is the entry's last | 13:6 |
| κατοικέω | pres. inf. · impf. 3 pl · aor. 3 sg | `to dwell in` · `were dwelling in` · `dwelt in` | the chain of GEN 9:27, in the form | 13:6, 13:7, 13:12, 13:18 |
| δύναμαι | impf. 3 pl · pres. 3 sg | `were being able` · `is able` | `were being able, were capable and strong enough, were powerful and mighty, were having influence, were daring and bearing, were passing for, were worth, were equivalent to, were signifying and meaning, were availing`, in the form | 13:6, 13:16 |
| γίνομαι | aor. 3 sg | `came into being` | the chain of GEN 12:10 | 13:7 |
| ἐπαίρω | aor. ptcp. | `having lifted up and set on` | the chain of GEN 7:17, in the participle | 13:10 |
| ὁράω | aor. 3 sg · aor. impv. (ἰδέ) · pres. 2 sg | `saw` · `see` · `you see` | the chain of GEN 3:6, in the form | 13:10, 13:14, 13:15 |
| ποτίζω | pres. pass. ptcp. | `being given to drink` | `being given to drink, being watered` — the chain of GEN 2:6 in the passive, where *to water* and *to water cattle* come to the same | 13:10 |
| καταστρέφω | aor. inf. | `to turn down` | `to turn down and trample on, to turn the soil, to upset and overturn, to subject to oneself and subdue, to turn back and bring back, to turn round and bring to an end, to come to an end and die, to twist up, to be subdued` — the passive's *to be subdued* at the end | 13:10 |
| ἐκλέγομαι | aor. mid. 3 sg | `picked out for himself` | the chain of GEN 6:2, in the singular | 13:11 |
| ἀπαίρω | aor. 3 sg | `lifted off` | the chain of GEN 12:9 | 13:11 |
| σκηνόω | aor. 3 sg | `pitched tents` | `pitched tents and encamped, dwelt in a tent, settled and took up one's abode, lived, occupied with tents` — the verb of John 1:14 | 13:12 |
| ἀναβλέπω | aor. ptcp. | `having looked up` | `having looked up, having looked, having looked up at, having cast up, having recovered one's sight` | 13:14 |
| δίδωμι | fut. 1 sg | `I will give` | the chain of GEN 12:7 | 13:15, 13:17 |
| ἐξαριθμέω | aor. inf. · fut. pass. 3 sg | `to count throughout` · `will be counted throughout` | `to count throughout, to number, to count out and pay in ready money`, in the form | 13:16 |
| ἀνίστημι | aor2 ptcp. | `having stood up` | the chain of GEN 4:8, in the participle | 13:17 |
| οἰκοδομέω | aor. 3 sg | `built a house` | the chain of GEN 8:20 | 13:18 |

### Verbs new in GEN 12

| lemma | form | headword | chain | used |
| --- | --- | --- | --- | --- |
| ἐξέρχομαι | aor. impv. · aor. 3 sg and 3 pl | `go out of` · `went out of` | the chain of GEN 8:16 and 4:16 | 12:1, 12:4, 12:5 |
| δείκνυμι | aor. subj. 1 sg | `I may bring to light` | `I may bring to light, I may display and exhibit, I may set before one, I may show and point out, I may tell and explain and teach, I may show and prove, I may inform against, I may offer and proffer, I may cause, I may welcome and greet and pledge` | 12:1 |
| ποιέω, εὐλογέω | fut. 1 sg | `I will make` · `I will speak well of` | the chains of GEN 6:14 and 2:3, in the future | 12:2, 12:3 |
| μεγαλύνω | fut. 1 sg | `I will make great` | `I will make great and powerful, I will exalt and strengthen, I will make great by word and extol and magnify, I will aggravate` — the middle's *to boast oneself* left out | 12:2 |
| εὐλογέω, καταράομαι | pres. ptcp. pl., articular · fut. 1 sg | `the ones speaking well of` · `the ones calling down curses upon` · `I will call down curses upon` | the chains of GEN 2:3 and 5:29, in the form | 12:3 |
| λαλέω | aor. 3 sg | `talked` | `talked, chatted, prattled, babbled, said, talked of, spoke, chattered, chirped` — *to speak*, like λέγω, is the entry's New Testament sense | 12:4 |
| οἴχομαι | impf. 3 sg | `had gone` | `had gone, had been gone, had escaped from, had gone hence, was departed and dead, was absent and away, was undone and ruined, was rushing and sweeping along` — the entry gives the imperfect a pluperfect sense | 12:4 |
| ὑπάρχω | pres. ptcp. n. pl., as a noun | `the existing circumstances` | `the existing circumstances, the present advantages, what belongs to one, the possessions and means` — the entry's first sense for τὰ ὑπάρχοντα | 12:5 |
| κτάομαι | aor. 3 pl | `they procured for themselves` | the chain of GEN 4:1, in the third plural | 12:5 |
| κατοικέω | impf. 3 pl | `were dwelling in` | the chain of GEN 11:2, in the imperfect | 12:6 |
| ὁράω | aor. pass. 3 sg and ptcp. · aor. subj. 3 pl · aor. ptcp. pl. · aor. 3 pl | `was seen` · `to the one having been seen` · `may see` · `having seen` · `saw` | the chains of GEN 8:5, 2:19 and 3:6, in the form | 12:7, 12:12, 12:14, 12:15 |
| ἀφίστημι | aor2 3 sg | `stood away` | `stood away, stood aloof from and kept far from, lost, withdrew from, revolted from, revolted, gave up, made way and gave way, shrank from, stood aloof` — sense B, the intransitive of the second aorist, as ἀνίστημι at 4:8 | 12:8 |
| ἵστημι | aor1 3 sg | `made to stand` | the chain of GEN 6:18, in the aorist | 12:8 |
| ἐπικαλέω | aor. mid. 3 sg | `called upon` | the chain of GEN 4:26, in the aorist; Middle Liddell gives sense I *so in Mid.* | 12:8 |
| ἀπαίρω | aor. 3 sg | `lifted off` | `lifted off, carried off, took away, removed from, led away, sailed and marched away and departed, departed from, set out on` — *to depart* is the entry's intransitive use | 12:9 |
| στρατοπεδεύω | aor. 3 sg | `encamped` | `encamped, bivouacked, took up a position, was in camp, was stationed` | 12:9 |
| παροικέω | aor. inf. | `to dwell beside` | `to dwell beside, to dwell along the coast of, to live near, to dwell among, to lie near, to live in and sojourn` | 12:10 |
| ἐνισχύω | aor. 3 sg | `strengthened` | `strengthened, confirmed, prevailed in and among` — LSJ | 12:10 |
| ἐγγίζω | aor. 3 sg | `brought near` | `brought near, brought up to, approached, was imminent, approximated to, was next of kin, was on the point of` — LSJ | 12:11 |
| εἰσέρχομαι | aor. inf. · aor. 3 sg | `to go in` · `went in` | the chain of GEN 6:18, in the form | 12:11, 12:14 |
| γινώσκω | pres. 1 sg | `I learn to know` | the chain of GEN 4:9 | 12:11 |
| ἀποκτείνω | fut. 3 pl | `they will kill` | the chain of GEN 4:8, in the future | 12:12 |
| περιποιέομαι | fut. 3 pl | `they will keep for themselves` | `they will keep for themselves, they will save for themselves, they will compass and acquire and obtain, they will make gain` — the middle; the actives left out | 12:12 |
| λέγω | aor. impv. (εἰπόν) · aor. 2 sg | `say` · `you said` | the chain of GEN 2:16, in the form | 12:13, 12:19 |
| γίνομαι | aor. subj. 3 sg | `may come into being` | the chain of GEN 5:5, in the subjunctive | 12:13 |
| ζάω | fut. 3 sg | `will live` | the chain of GEN 3:22 | 12:13 |
| ἐπαινέω | aor. 3 pl | `approved` | `approved, applauded, commended, complimented publicly and panegyrized, recommended and exhorted and advised, thanked, declined` | 12:15 |
| εἰσάγω | aor. 3 pl | `led in` | the chain of GEN 8:9 | 12:15 |
| χράομαι | aor. 3 pl | `used` | `used, had and used, indulged, experienced and suffered and were subject to, came to, lived under, made use of, treated, were intimate with, were in need and yearned after, had in use and possessed` — Perseus's *consulting*, *using an oracle*, which say where the sense comes from, left out | 12:16 |
| ἐτάζω | aor. 3 sg | `examined` | `examined, tested` | 12:17 |
| καλέω | aor. ptcp. | `having called` | the chain of GEN 2:19, in the participle | 12:18 |
| ἀπαγγέλλω | aor. 2 sg | `you brought tidings` | `you brought tidings, you reported, you announced, you carried a report, you related and narrated` | 12:18 |
| λαμβάνω | aor. 1 sg · aor. ptcp. | `I took` · `having taken` | the chain of GEN 2:15, in the form | 12:19 |
| ἀποτρέχω | pres. impv. | `run off` | `run off, run away, run hard` | 12:19 |
| ἐντέλλομαι | aor. 3 sg | `enjoined` | the chain of GEN 2:16 | 12:20 |

### Verbs new in GEN 11

| lemma | form | headword | chain | used |
| --- | --- | --- | --- | --- |
| κινέω | aor. inf., articular with ἐν | `in the setting in motion` | `within, inside of, and by means of the setting in motion, the moving, the removing, the meddling with, the applying, the changing and innovating, the rousing and disturbing, the stirring up and arousing and urging on, the setting agoing and causing and calling forth` — the actives | 11:2 |
| εὑρίσκω | aor. 3 pl | `found` | the chain of GEN 6:8 | 11:2 |
| κατοικέω | aor. 3 pl and 3 sg | `dwelt in` | `dwelt in, settled in, colonised, inhabited, settled and dwelt, lay and were situate`, in the number — the chain of GEN 9:27 | 11:2, 11:31 |
| πλινθεύω | aor. subj. 1 pl | `let us make into bricks` | `let us make into bricks, let us make bricks, let us build of brick, let us make in the form of a plinth or brick` | 11:3 |
| ὀπτάω | aor. subj. 1 pl | `let us roast` | `let us roast, let us broil, let us bake, let us bake and burn, let us bake and harden` | 11:3 |
| οἰκοδομέω | aor. subj. 1 pl · aor. 3 pl · pres. ptcp. pl. | `let us build a house` · `built a house` · `building a house` | the chain of GEN 2:22, in the form | 11:4, 11:5, 11:8 |
| ποιέω | aor. subj. 1 pl · aor. and pres. inf. | `let us make` · `to make` | `let us make, let us do, let us produce, let us create`; the chain of GEN 2:3 | 11:4, 11:6 |
| διασπείρω | aor. pass. inf. · aor. 3 sg | `to be scattered abroad` · `scattered abroad` | the chain of GEN 9:19, in the form | 11:4, 11:8, 11:9 |
| καταβαίνω | aor. 3 sg · aor. ptcp. pl. | `stepped down` · `having stepped down` | `stepped down, went and came down, went down from, dismounted, came down stairs, went down from the inland parts to the sea, came to land and got safe ashore, went down into the arena, came down from the tribune, came to, ended`, in the form | 11:5, 11:7 |
| ἐκλείπω | fut. 3 sg | `will leave out` | the chain of GEN 8:13, in the future | 11:6 |
| ἐπιτίθημι | aor. mid. subj. 3 pl | `they may put on themselves` | the chain of GEN 9:23, in the subjunctive | 11:6 |
| συγχέω | aor. subj. 1 pl · aor. 3 sg | `let us pour together` · `poured together` | `let us pour together, let us commingle, let us confound, let us make ruinous and destroy and obliterate and demolish, let us confound and trouble, let us confound and make of none effect and frustrate`, in the form — the passive's *to be in confusion* left out | 11:7, 11:9 |
| ἀκούω | aor. subj. 3 pl | `they may hear` | `they may hear, they may have hearing of, they may hear tell of, they may know by hearsay, they may hearken and give ear, they may listen to and obey` | 11:7 |
| παύω | aor. mid. 3 pl | `took their rest` | `took their rest, rested and ceased and had done, left off from and rested and ceased from, were at rest, left off doing` — the entry's *Pass. and Mid.*; the causal actives left out | 11:8 |
| καλέω | aor. pass. 3 sg | `was called` | `was called, was summoned, was invited` — the chain of GEN 2:23, in the aorist | 11:9 |
| γίνομαι | aor. 3 sg, no subject · aor. 3 sg and 3 pl · aor. pass. 3 sg | `came into being` | the chains of JHN 1:6 and GEN 5:5, in the form | 11:2, 11:3, 11:28, 11:32 |
| ζάω, γεννάω, ἀποθνήσκω | the frame of GEN 5 | `lived` · `begot` · `to beget` · `died off` | the chains of GEN 5 | 11:11–32 |
| λαμβάνω | aor. 3 pl and 3 sg | `took` | the chain of GEN 2:15 | 11:29, 11:31 |
| ἐξάγω | aor. 3 sg | `led out` | the chain of GEN 8:17, in the aorist | 11:31 |
| πορεύομαι | aor. pass. inf. | `to be driven` | the chain of GEN 2:14, in the infinitive | 11:31 |
| ἔρχομαι | aor. 3 sg | `came` | `came, went, went back and returned, was going to and intended, came within a little of and was near` — the chain of GEN 10:19 | 11:31 |

### Verbs new in GEN 10

| lemma | form | headword | chain | used |
| --- | --- | --- | --- | --- |
| γίνομαι | aor. pass. 3 pl · aor. mid. 3 sg and 3 pl · aor. pass. 3 sg, no subject | `came into being` | the chains of GEN 5:5, 4:2 and JHN 1:6, in the form | 10:1, 10:10, 10:19, 10:21, 10:25, 10:30 |
| ἀφορίζω | aor. pass. 3 pl | `were marked off by boundaries` | `were marked off by boundaries, were marked off for themselves, were distinguished and determined and defined, were set apart and separated` — the chain of GEN 2:10, in the aorist | 10:5 |
| γεννάω | aor. 3 sg | `begot` | the chain of GEN 4:18 | 10:8–26 |
| ἄρχω | aor. mid. 3 sg | `began` | the chain of GEN 2:3 | 10:8 |
| λέγω | fut. 3 pl | `they will say` | `they will say, they will speak, they will declare, they will call by name, they will tell` | 10:9 |
| ἐξέρχομαι | aor. 3 sg | `went out of` | the chain of GEN 4:16 | 10:11, 10:14 |
| οἰκοδομέω | aor. 3 sg | `built a house` | the chain of GEN 2:22 | 10:11 |
| διασπείρω | aor. pass. 3 pl | `were scattered abroad` | the chain of GEN 9:19 | 10:18, 10:32 |
| ἔρχομαι | aor. inf. | `to come` | `to come, to go, to go back and return, to be going to and intend, to come within a little of and be near` | 10:19, 10:30 |
| διαμερίζω | aor. pass. 3 sg | `was distributed` | `was distributed, was divided` — the middle's *to part among themselves* left out | 10:25 |

A third-person imperative takes *let* and no pronoun (κατοικησάτω *let dwell in*, γενηθήτω *let
come into being*), as a finite verb takes none; an optative takes *may* (πλατύναι *may widen*).

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

### Nouns and adjectives new in GEN 5

| lemma | headword | chain | used |
| --- | --- | --- | --- |
| βίβλος, γένεσις | `the inner bark of the papyrus` · `of origin` | the chains of GEN 2:4 | 5:1 |
| ἄνθρωπος (anarthrous gen. pl.) | `of men` | `of men, of human beings` | 5:1 |
| ἡμέρα | `day` · `the days` | the chains of GEN 2:4 and 3:14 | 5:1–31 |
| θεός (anarthrous gen.) | `of God` | the chain of GEN 1:2 | 5:1 |
| θεός (articular dat.) | `to the God` | `to him who is God definitively, to the one the article marks out, to the known and the only` | 5:22, 5:24 |
| εἰκών | `a likeness` · `the likeness` | `a likeness, an image, a portrait, an image in a mirror, a semblance and phantom, an image in the mind, a similitude and simile` | 5:1, 5:3 |
| ἄρσην | `male` | `male, the male sex, masculine and strong, mighty` | 5:2 |
| θῆλυς | `female` | `female, the female sex and womankind, belonging to women, feminine, fresh and refreshing, tender and delicate and gentle, soft and yielding and weak` | 5:2 |
| ὄνομα (articular) | `the name` | the chain of GEN 3:20 | 5:2, 5:3, 5:29 |
| ἰδέα | `the form` | `the form, the look, the outward appearance, the kind and sort and nature, the mode and fashion, the class and species` — sense I reads *= εἶδος, form* | 5:3 |
| ἔργον (gen. pl.) | `of the works` | the short chain of GEN 2:2, in the genitive | 5:29 |
| λύπη (gen. pl.) | `of the pains of body` | the chain of GEN 3:17, in the genitive | 5:29 |
| χείρ (gen. pl.) | `of the hands` | `of the hands, of the hands and arms, of the arms` | 5:29 |

ἰδέα and εἰκών at 5:3 render one Hebrew pair, *dĕmût* and *ṣelem*, that 1:26 rendered with
εἰκών and ὁμοίωσις; each Greek word keeps its own chain, so the reader sees the change of word.

### Nouns and adjectives new in GEN 6

| lemma | headword | chain | used |
| --- | --- | --- | --- |
| ἄνθρωπος (articular pl.) | `the men` · `of the men` · `in the men` | `the men, the human beings, mankind`, in the form | 6:1–5 |
| ἄνθρωπος (anarthrous gen.) | `of man` | `of a man, of a human being` | 6:7, 6:13 |
| πολύς | `many` | `many, often, much and mighty and great, deep, loud, strong, large and wide, far, long` | 6:1 |
| καλός (pl.) | `beautiful` | the chain of GEN 2:9 | 6:2 |
| γυνή | `women` · `the woman` · `the women` | the chains of GEN 2:22 and 4:19, in the form | 6:2, 6:18 |
| πνεῦμα | `the blowing` · `blowing` | the chain of GEN 1:2, with the article at 6:3 | 6:3, 6:17 |
| σάρξ | `fleshes` · `flesh` · `of flesh` | the chain of GEN 2:21, in the form; the plural `fleshes, the flesh, muscles, bodies, man's nature generally` | 6:3, 6:12, 6:17, 6:19 |
| αἰών | `the period of existence` · `of period of existence` | the chain of GEN 3:22, in the form | 6:3, 6:4 |
| γίγας | `the giants` | `the giants, the sons of Gaia, the mighty` — Middle Liddell's *the Giants*, lower case as the Greek is | 6:4 |
| ἡμέρα with ἐν | `in the days` | `within, inside of, and by means of the days, the day-breaks, the times` | 6:4 |
| ὀνομαστός | `named` | `named, to be named, of name and note, notable, famous` | 6:4 |
| κακία (pl.) | `the badnesses` | `the badnesses, the defects, the cowardices and sloths, the moral badnesses and wickednesses and vices, the ill-reputes, the evils` | 6:5 |
| καρδία with ἐν | `in the heart` | `within, inside of, and by means of the heart, the stomach` | 6:5 |
| πονηρός (articular n. pl.) | `the toilsome` | the chain of GEN 2:9, with the article | 6:5 |
| πρόσωπον (anarthrous) | `face` | the chain of GEN 4:14, in the same phrase | 6:7 |
| κτῆνος | `of flocks and herds` · `of the flocks and herds` | `of flocks and herds, of a single beast, of an ox, of a sheep, of a beast for riding`; the articular plural of GEN 3:14 | 6:7, 6:19, 6:20 |
| ἑρπετόν | `of walking animals` · `of the walking animals` | `of walking animals, of quadrupeds, of creeping things, of reptiles` — *a walking animal* is the first sense, *a creeping thing* the second | 6:7, 6:19, 6:20 |
| πετεινόν, οὐρανός | `of the winged fowl` · `of the heaven` | the chains of GEN 2:19–20, in the genitive | 6:7, 6:17, 6:20 |
| χάρις | `outward grace` | `outward grace, favour, loveliness, graciousness and kindness and goodwill, thankfulness and thanks and gratitude, a favour and kindness and boon, a gratification and delight` — the numbered senses; Perseus's heading, *Grace*, left out | 6:8 |
| γένεσις (pl.) | `the origins` | the chain of GEN 2:4, in the nominative plural | 6:9 |
| δίκαιος | `observant of custom and social rule` | `observant of custom and social rule, well-ordered and civilised, observant of right and righteous, even and well-balanced, regular and exact, right and lawful and just, real and genuine and true, fair and moderate` | 6:9 |
| τέλειος | `having reached its end` | `having reached its end, finished and complete, perfect and without spot or blemish, fullgrown, absolute and accomplished and perfect in his kind, fulfilled` | 6:9 |
| γενεά with ἐν | `in the race` | `within, inside of, and by means of the race, the stock and family, the breed, the tribe and nation, the generation, the offspring, the birth-place, the age and time of life` | 6:9 |
| ἀδικία | `of wrong-doing` | `of wrong-doing, of injustice, of a wrong, of an injury` | 6:11, 6:13 |
| ὁδός | `the way` | the chain of GEN 3:24 | 6:12 |
| καιρός | `due measure` | `due measure, proportion, fitness, a vital part, the right point of time, the proper time and season, the exact and critical time, the time, advantage and profit and fruit` | 6:13 |
| κιβωτός | `a wooden box` · `the wooden box` · `of the wooden box` | `a wooden box, a chest, a coffer`, in the form | 6:14–16, 6:18, 6:19 |
| ξύλον (gen. pl.) | `of woods` | `of woods, of firewood, of timbers, of pieces of wood, of posts, of sticks` | 6:14 |
| τετράγωνος | `of with four equal angles` | `of with four equal angles, of rectangular, of square, of squared, of perfect` — an adjective in the genitive takes *of*, as at 2:9 | 6:14 |
| νοσσιά | `nests of young birds` | `nests of young birds, nests` — under νεοσσιά | 6:14 |
| ἄσφαλτος | `with the asphalt` | `with the asphalt, with the bitumen` | 6:14 |
| πῆχυς | `of fore-arms` · `fore-arm` | `of fore-arms, of arms, of centrepieces of the bow, of horns and sides of the lyre, of cubits and ells, of cubit-rules`, in the form — the measure is sense IV | 6:15, 6:16 |
| μῆκος, πλάτος, ὕψος | `the length` · `the breadth` · `the height` | `the length, the distances, the height and tallness and stature` · `the breadth, the width` · `the height, the top and summit and crown` | 6:15 |
| θύρα | `the door` | `the door, the folding doors, the gate, the court, the trap-door, the frame of planks and raft, the entrance` | 6:16 |
| πλάγιος (n. pl. as noun) | `of sides` | `of sides, of flanks` — the first noun sense | 6:16 |
| κατάγαιος | `in the earth` | `in the earth, under the earth, underground, subterranean` — under κατάγειος | 6:16 |
| κατακλυσμός | `the deluge` | `the deluge, the inundation` | 6:17 |
| ζωή (anarthrous gen.) | `of a living` | the chain of GEN 2:7 | 6:17 |
| διαθήκη | `the disposition` | `the disposition of property by will, the will and testament, the arrangement between two parties, the covenant` | 6:18 |
| θηρίον (gen. pl.) | `of the wild animals` | the chain of GEN 3:1 | 6:19 |
| ὄρνεον | `of the birds` | `of the birds, of the bird-market` | 6:20 |
| γένος | `race` | `race, stock and family, offspring and posterity, a clan and house, a tribe and caste, a breed, an age and generation, sex and gender, a class and sort and kind, genus` | 6:20 |
| βρῶμα | `of the things which are eaten` | `of the things which are eaten, of the foods, of the meats` | 6:21 |

### Nouns and adjectives new in GEN 7

| lemma | headword | chain | used |
| --- | --- | --- | --- |
| οἶκος | `the house` | `the house, the abode and dwelling, the room and chamber, the house of a god and temple, the household goods and substance, the household and family` | 7:1 |
| καθαρός (articular gen. pl.) | `of the clear of dirt` | `of the clear of dirt, of the clean and spotless and unsoiled, of the clear and open and free, of the clear from shame and pollution and pure, of the clear of admixture, of the genuine`; μή before it as plain `not` | 7:2, 7:3, 7:8 |
| ἡμέρα (anarthrous gen. pl.) | `of days` | `of days, of day-breaks, of times` | 7:4 |
| ὑετός | `rain` · `the rain` | `rain, a heavy shower` | 7:4, 7:12 |
| νύξ (pl.) | `night-seasons` | `night-seasons, nights, watches of the night, darknesses of night, nights of death` — the first tagged translation is *the night-season* | 7:4, 7:12, 7:17 |
| ἐξανάστασις | `the rising up from` | `the rising up from, the resurrection` | 7:4 |
| ἀνάστημα | `the height` | `the height, the majesty, the protuberance and prominence, the high ground, the erection and building and structure, the eruption` — LSJ | 7:23 |
| ζωή with ἐν | `in the life` | `within, inside of, and by means of the life, the means of life and substance, existence, a way of life` — the articular chain of GEN 3:17 | 7:11 |
| πηγή (pl., articular) | `the running waters` | `the running waters, the streams, the founts, the sources, the origins` — the chain of GEN 2:6 | 7:11 |
| ἄβυσσος (gen.) | `of the great deep` | the chain of GEN 1:2, in the genitive | 7:11 |
| καταρράκτης (pl.) | `the broken waters` | `the broken waters, the waterfalls, the portcullises, the gulls` — the first noun sense; *down-rushing* is the adjective | 7:11 |
| θηρίον, κτῆνος, ἑρπετόν, πετεινόν (nom.) | `the wild animals` · `the flocks and herds` · `walking animal` · `winged fowl` | the chains of GEN 6, in the nominative | 7:14 |
| ὄρος (pl.) | `the mountains` | `the mountains, the hills` | 7:19, 7:20 |
| ὑψηλός (articular pl.) | `the high` | `the high, the lofty, the high-raised, the highland, the stately` | 7:19, 7:20 |
| πῆχυς (acc. pl.) | `fore-arms` | the chain of GEN 6:15, in the accusative | 7:20 |
| πνοή | `a blowing` | the chain of GEN 2:7 | 7:22 |
| κιβωτός with ἐν | `in the wooden box` | `within, inside of, and by means of the wooden box, the chest, the coffer` | 7:23 |

### Nouns and adjectives new in GEN 8

| lemma | headword | chain | used |
| --- | --- | --- | --- |
| κεφαλή (pl.) | `the heads` | `the heads, the whole persons, the lives, the tops, the sources, the crowns` — the chain of GEN 3:15 in the plural | 8:5 |
| ὄρος (gen. pl.) | `of the mountains` | `of the mountains, of the hills` | 8:5 |
| κόραξ | `the carrion-crow` | `the carrion-crow, the raven, the engine like a raven's beak for grappling ships, the hooked handle of a door, the instrument of torture` | 8:7 |
| περιστερά | `the common pigeon` | `the common pigeon, the dove` | 8:8–12 |
| ὀπίσω + genitive | `after` | `after, backwards, back and back again, again, hereafter, behind` — the entry's sense with the genitive | 8:8 |
| ἀνάπαυσις | `repose` | `repose, rest, relaxation and recreation, rest from` | 8:9 |
| πούς (dat. pl.) | `to the feet` | `to the feet, to the talons, to the feet of a hill` | 8:9 |
| ἕτερος (pl.) | `other` | the chain of GEN 4:25 | 8:10, 8:12 |
| πάλιν | `back` | `back, backwards, again and once more and anew, again in turn` | 8:10, 8:12 |
| ἑσπέρα | `evening` | `evening, eventide, eve, nightfall, the west` | 8:11 |
| φύλλον (sg.) | `leaf` | `leaf, foliage, petal, herb` — the chain of GEN 3:7 in the singular | 8:11 |
| ἐλαία | `of olive-tree` | `of olive-tree, of olives, of the fruit of the olive-tree and olive` | 8:11 |
| κάρφος | `a dry stalk` | `a dry stalk, dry sticks, dry twigs and chips and straws and bits of wool` | 8:11 |
| στόμα with ἐν | `in the mouth` | `within, inside of, and by means of the mouth, the mouth as the organ of speech, the mouthpiece, the face, the chasm and cleft` — the chain of GEN 4:11 | 8:11 |
| στέγη | `the roof` | `the roof, the roofed place, the chamber and room, the tent` | 8:13 |
| πετεινόν, κτῆνος (anarthrous gen. pl.) | `of winged fowl` · `of flocks and herds` | the chains of GEN 6, without the article | 8:17 |
| ὀσμή | `a smell` | `a smell, a scent, an odour` | 8:21 |
| διάνοια | `the thought` | `the thought, the intention and purpose, the notion and opinion, the intelligence and understanding, the meaning` | 8:21 |
| νεότης | `youth` | `youth, youthful spirit and impetuosity, rashness and petulance, a body of youth` | 8:21 |
| ζάω (pres. ptcp.) | `living` | the chain of GEN 2:7 | 8:21 |
| καθώς | `according as` | `according as, just as, like as if, exactly as, how` — the entry opens *= καθά* | 8:21 |
| θερισμός, ψῦχος, καῦμα, θέρος, ἔαρ | `reaping-time` · `cold` · `burning heat` · `summer` · `spring` | `reaping-time, harvest, the crop` · `cold, winter-time, coolness` · `burning heat, sun-heat, fever-heat` · `summer, summertime, summer-fruits and harvest and crop` · `spring, prime and flower` | 8:22 |
| ἡμέρα, νύξ (anarthrous acc. sg.) | `day` · `night-season` | `day, day-break, time` · `night-season, night, the watches of the night, the dark of night, the night of death` | 8:22 |

### Nouns and adjectives new in GEN 9

| lemma | headword | chain | used |
| --- | --- | --- | --- |
| τρόμος | `the trembling` | `the trembling, the quaking, the quivering` | 9:2 |
| φόβος | `the flight` | `the flight, the panic fear, the fear and terror, the outward show of fear, the object of terror` — *flight*, the only sense in Homer, is sense I | 9:2 |
| πᾶς (dat. pl.) | `to all` | the chain of GEN 2:20 | 9:2, 9:10 |
| θηρίον (dat. pl.) | `to the wild animals` | the chain of GEN 2:20 | 9:2, 9:10 |
| ὄρνεον (pl.) | `the birds` · `of birds` | `the birds, the bird-market`, the chain of GEN 6:20 in the form | 9:2, 9:10 |
| ἰχθύς (pl.) | `the fishes` | `the fishes, the fish-market` | 9:2 |
| θάλασσα | `of the sea` | `of the sea, of the Mediterranean, of a well of salt water` | 9:2 |
| χείρ (acc. pl., anarthrous) · (gen. sg., anarthrous) | `hands` · `of hand` | `hands, hands and arms, arms` · `of hand, of hand and arm, of arm` | 9:2, 9:5 |
| ἑρπετόν | `walking animal` | the chain of GEN 7:14 | 9:3 |
| βρῶσις | `meat` | the chain of GEN 2:9 | 9:3 |
| λάχανον (pl.) | `garden-herbs` | `garden-herbs, potherbs, vegetables, greens, the vegetable-market and green-market` | 9:3 |
| χόρτος (anarthrous gen.) | `of an inclosed place` | the chain of GEN 2:5, in the genitive | 9:3 |
| πᾶς (τὰ πάντα, as a noun) | `the all things` | `the all things, the everything, the whole` — the entry's neuter used as a noun, *all things* | 9:3 |
| κρέας | `flesh` | `flesh, meat, a piece of meat, dressed meat, a body and person` — not σάρξ, whose headword is also *flesh*; the note says which | 9:4 |
| αἷμα | `in blood` · `blood` · `of the blood` | the chain of GEN 4:10, in the form | 9:4, 9:5, 9:6 |
| ψυχή | `of breath` · `of the breaths` · `the breath` · `to breath` | the chain of GEN 2:7, in the form | 9:4, 9:5, 9:10, 9:12, 9:15, 9:16 |
| ἄνθρωπος | `of man` · `of the man` · `the man` · `man` | the chains of GEN 6:7, 8:21, 2:7 and JHN 1:6 | 9:5, 9:6, 9:20 |
| ἀδελφός | `of son of the same mother` · `to sons of the same mother` · `to the sons of the same mother` | the chain of GEN 4:2, in the form | 9:5, 9:22, 9:25 |
| εἰκών with ἐν | `in a likeness` | `within, inside of, and by means of a likeness, …` — the chain of GEN 5:1 | 9:6 |
| σπέρμα (dat.) | `to that which is sown` | the chain of GEN 4:25, in the dative | 9:9 |
| διαθήκη | `the disposition` · `of the disposition` · `of a disposition` · `a disposition` | the chain of GEN 6:18, in the form | 9:9–17 |
| κτῆνος (anarthrous gen. pl.) | `of flocks and herds` | the chain of GEN 8:17 | 9:10 |
| κατακλυσμός | `of the deluge` · `a deluge` · `the deluge` | the chain of GEN 6:17, in the form | 9:11, 9:15, 9:28 |
| σημεῖον | `the sign` · `a sign` | the chain of GEN 4:15, in the form | 9:12, 9:13, 9:17 |
| γενεά (pl.) | `races` | `races, stocks and families, breeds, tribes and nations, generations, offspring, birth-places, ages and times of life` — the chain of GEN 6:9 in the plural | 9:12 |
| αἰώνιος | `lasting for an age` | `lasting for an age, ever-lasting, eternal` | 9:12, 9:16 |
| ζάω (pres. ptcp., attributive) | `of living` · `to the living` | the chain of GEN 2:7 and 3:22, in the form | 9:10, 9:12, 9:15, 9:16 |
| τόξον | `the bow` | `the bow, the bow and arrows, the rays` — τόξῳ, *by guess*, one construction, left out | 9:13, 9:14, 9:16 |
| νεφέλη with ἐν · (pl.) | `in the cloud` · `clouds` | `within, inside of, and by means of the cloud, the bird-net` · `clouds, bird-nets` | 9:13, 9:14, 9:16 |
| πατήρ (anarthrous) | `father` | `father, grandfather` — as μήτηρ at 3:20 | 9:18 |
| οὗτος (pl.) | `these` · `of these` | the chain of GEN 6:9, in the form | 9:19 |
| γεωργός | `a husbandman` | `a husbandman, one tilling the ground` — the first noun sense, then the adjective, as βοηθός at 2:18 | 9:20 |
| γῆ (anarthrous gen.) | `of earth` | the chain of GEN 2:4 | 9:20 |
| οἶκος with ἐν · (pl.) | `in the house` · `in the houses` | the chain of GEN 7:1, in the form | 9:21, 9:27 |
| γύμνωσις | `the stripping` | `the stripping, the nakedness, the defenceless side` | 9:22, 9:23 |
| πατήρ | `the father` · `of the father` | the chain of GEN 2:24, in the form | 9:22, 9:23 |
| ἱμάτιον | `the outer garment` | `the outer garment, the cloak and mantle, the Roman toga, the clothes, the cloth` | 9:23 |
| νῶτον (pl.) | `backs` | `backs, wide surfaces, plains, ridges` — κατὰ νώτου, *from behind*, one construction, left out | 9:23 |
| πρόσωπον | `the face` | the chain of GEN 2:6 | 9:23 |
| ὀπισθοφανής | `seen from behind` | `seen from behind, showing behind, appearing behind or after, reversing the image, looking backwards` — **no Middle Liddell entry**; LSJ, citing 9:23 | 9:23 |
| νέος (comp.) | `the younger` | `the younger, the more youthful, the newer and fresher, the stranger` | 9:24 |
| παῖς | `a child` | `a child, a son, a daughter, a grandchild, a boy and youth and lad, a girl and maiden, a slave and servant and man and maid` — *a slave, servant* is sense III, *in relation to condition* | 9:25, 9:26, 9:27 |
| οἰκέτης | `a house-slave` | `a house-slave, a menial` | 9:25 |

### Nouns and adjectives new in GEN 14

| lemma | headword | chain | used |
| --- | --- | --- | --- |
| βασιλεία, with ἐν | `in the kingdom` | the chain of GEN 10:10, after ἐν | 14:1 |
| βασιλεύς | `a king` · `of a king` · `the kings` · `kings` · `of the kings` | `a king, a chief, an hereditary king, a lord and master and householder, the second of the nine archons, the king of Persia`, in the form — lower case for *Archons*; the comparative *more kingly* and the example *the king's son, prince* left out | 14:1–22 |
| ἔθνος (gen. and acc. pl.) | `of numbers of people accustomed to live together` · `numbers of …` | the chain of GEN 10:5, anarthrous | 14:1, 14:5, 14:9 |
| πόλεμος | `battle` | `battle, fight and war`, one sense of three glosses | 14:2, 14:8 |
| φάραγξ | `the cleft` | `the cleft and chasm, the ravine and gully` | 14:3 |
| ἁλυκός | `salt` | `salt, brackish` — LSJ, after a plain `the` | 14:3, 14:8, 14:10 |
| θάλασσα | `the sea` | the chain of GEN 12:8, with the article | 14:3 |
| ἅλς | `of the salt` | `of the salt, of the lumps of salt` — the plural's *salt* heads the plural; *the sea*, ἡ ἅλς, is the feminine's | 14:3 |
| γίγας | `the giants` | the chain of GEN 6:4 | 14:5 |
| ἰσχυρός | `strong` | `strong, mighty, hard, obstinate and stiff and stubborn and inveterate and excessive and severe` — the neuter as a noun, the superlative and the adverb left out | 14:5 |
| πόλις | `the city` | the chain of GEN 4:17, with the article, after a name under ἐν | 14:5 |
| ὄρος, with ἐν | `in the mountains` | the chain of GEN 7:19, after ἐν | 14:6 |
| τερέμινθος | `of the terebinth` | `of the terebinth, of the turpentine tree` — under τέρμινθος | 14:6 |
| ἔρημος, with ἐν | `in the desert part` | the chain of GEN 12:9 | 14:6 |
| πηγή | `the running waters` | the chain of GEN 2:6, with the article | 14:7 |
| κρίσις | `of the separating` | `of the separating and power of distinguishing, of the choice and selection, of the decision and judgment, of the means of judging, of the trial, of the result of a trial and condemnation, of the dispute, of the event and issue` | 14:7 |
| ἄρχων | `the rulers` | the chain of GEN 12:15 | 14:7 |
| κοιλάς | `the hollow` · `in the hollow` | `the hollow, the deep valley`, and after ἐν | 14:8, 14:10, 14:17 |
| φρέαρ | `wells` | `wells, tanks and cisterns and reservoirs, oil jars` — *(opp. a spring)* left out | 14:10 |
| ἄσφαλτος | `of asphalt` | the chain of GEN 11:3, in the genitive | 14:10 |
| ὀρεινός, used as a noun | `the mountainous` | `the mountainous and hilly, the dwelling on the mountains` | 14:10 |
| ἵππος | `the horse` | `the horse and mare, the horse and cavalry` — ἡ ἵππος; the plural's *chariot-horses* and the compounds' *anything large* left out | 14:11, 14:16, 14:21 |
| βρῶμα | `the things which are eaten` | the chain of GEN 6:21, in the accusative | 14:11 |
| ἀποσκευή | `the removal` | `the removal and riddance, the baggage, the household stuff, the ordure and filth` — LSJ | 14:12 |
| τις | `any one` | the chain of GEN 6:5 | 14:13 |
| περάτης | `to the ferryman` | `to the ferryman, to the boatman and seaman, to the conveyer, to the wanderer and emigrant` — LSJ, through πορθμεύς | 14:13 |
| δρῦς | `to the tree` | the chain of GEN 12:6, in the dative | 14:13 |
| ἀδελφός | `of the son of the same mother` · `of son of the same mother` · `the son of the same mother` | the chains of GEN 4:9, 9:5 and 4:2 | 14:12–16 |
| συνωμότης | `fellow-conspirators` | `fellow-conspirators, confederates` | 14:13 |
| ἴδιος | `one's own` | `one's own, pertaining to oneself, private and personal, peculiar and separate and distinct, peculiar and different, strange and unaccustomed`, after a plain `the` — the noun's and adverb's senses left out | 14:14 |
| οἰκογενής | `born in the house` | `born in the house, homebred` | 14:14 |
| νύξ | `the night-season` | the chain of GEN 8:22, with the article | 14:15 |
| παῖς | `the children` | the chain of GEN 12:16, with the article | 14:15 |
| γυνή | `the women` | the chain of GEN 4:19, with the article | 14:16 |
| λαός | `the people` | `the people, the men, the soldiers, the land-army, the common men, the folk, the Jews, the Christians` | 14:16 |
| κοπή | `of the cutting in pieces` | `of the cutting in pieces, of the slaughter` — the word of Hebrews 7:1 | 14:17 |
| πεδίον | `the plain` | the chain of GEN 4:8 | 14:17 |
| ἄρτος | `cakes` | `cakes, loaves of wheat-bread, breads` — the chain of GEN 3:19, in the plural | 14:18 |
| ἱερεύς | `a priest` | `a priest, a sacrificer, a minister` | 14:18 |
| οὐρανός, γῆ | `the heaven` · `the earth` | the chains of GEN 1:1, *as the counterpart-below* included, since γῆ is paired with οὐρανός | 14:19, 14:22 |
| ἐχθρός, used as a noun | `the one's enemies` | `the one's enemies, the hated and hateful, the hostile and at enmity with` — the noun sense, *one's enemy*, first | 14:20 |
| ὑποχείριος | `under the hand` | `under the hand and in hand, under any one's hand and under command and subject, into one's power` | 14:20 |
| δεκάτη | `tenth part` | `tenth part, tithe, tenth day, tenth day after birth, naming-day, tenth` — under δέκατος, whose noun sense heads it; the adjective's *tenth* last | 14:20 |
| ἀνήρ (pl.) | `the men` · `of the men` | the chain of GEN 3:6, in the plural | 14:21, 14:24 |
| χείρ | `the hand` | the chain of GEN 3:22 | 14:22 |
| σφαιρωτήρ | `of thong` | `of thong and latchet, of a ball, of knop` — LSJ | 14:23 |
| ὑπόδημα | `of a sole bound under the foot with straps` | `of a sole bound under the foot with straps, of a sandal, of a half-boot` | 14:23 |
| σός, used as a noun | `of the thy property` | `of the thy property, of the thy interests, of the thy and thine and of thee` — τὰ σά's senses, with the article the Greek prints; the masculine's *thy kinsfolk* and the singular's *thy business* left out | 14:23 |
| μερίς | `of the part` · `a part` | `of the part, of the portion, of the share, of the parcel, of the contribution, of the part and division and class`, in the form | 14:24 |

### Nouns and adjectives new in GEN 13

| lemma | headword | chain | used |
| --- | --- | --- | --- |
| ἔρημος, used as a noun | `the desert part` | the chain of GEN 12:9, without ἐν | 13:1, 13:3 |
| πλούσιος | `rich` | `rich, wealthy, opulent, rich in, richly furnished, ample and abundant` | 13:2 |
| κτῆνος (dat. and gen. pl.) | `with flocks and herds` · `of the flocks and herds` | the chain of GEN 2:20, in the form; the dative with *with*, as at 12:17 | 13:2, 13:7 |
| ἀργύριον | `with a piece of silver` | `with a piece of silver, with a silver coin, with money and a sum of money and cash, with silver` | 13:2 |
| χρυσίον | `with a piece of gold` | the chain of GEN 2:11, anarthrous, in the dative | 13:2 |
| σκηνή | `the covered place` · `covered places` | the chain of GEN 12:8 · of GEN 4:20 | 13:3, 13:5 |
| τόπος | `of the place` · `the place` | the chain of GEN 12:6, in the form | 13:3, 13:4, 13:14 |
| ἀρχή | `the beginning` | `the beginning, the origin, the first cause, the headship and rule and governing precedence` — the chain of GEN 2:10 in the singular, with the article | 13:4 |
| βοῦς | `cows` | `cows, oxen, kine and cattle, ox-hide shields` | 13:5 |
| πρόβατον | `things that walk forward` | the chain of GEN 12:16 | 13:5 |
| πολύς | `many` | the chain of GEN 6:1 | 13:6 |
| μάχη | `battle` | `battle, fight and combat, quarrels and strifes and wranglings, a contest, a struggle, a mode of fighting and way of battle, a field of battle` | 13:7, 13:8 |
| ποιμήν | `of the herdsmen` | the chain of GEN 4:2, in the genitive plural | 13:7, 13:8 |
| ἄνθρωπος (pl.) | `men` · `the men` | `men, human beings` · `the men, the human beings, mankind` — the chains of JHN 1:6 and GEN 2:7, in the plural | 13:8, 13:13 |
| ἀδελφός | `sons of the same mother` · `of the son of the same mother` | the chain of GEN 4:2, in the form | 13:8, 13:11 |
| ἀριστερός, used as a noun | `left` | `left and on the left, the left hand, boding ill and ominous` — εἰς ἀριστερά, anarthrous | 13:9 |
| δεξιός, used as a noun | `right` | `right, on the right hand, fortunate and boding good and lucky, dexterous and ready, sharp and shrewd and clever` — εἰς δεξιά: the first noun sense, *the right*, without the article the Greek does not print; the entry's first sense is *on the right hand* | 13:9 |
| περίχωρος | `the country round about` · `of the countries round about` | `the country round about, the round about a place, the people about`, in the form — the entry's sense for ἡ περίχωρος, ahead of the adjective's *round about a place* and οἱ περίχωροι, *the people about* | 13:10, 13:11, 13:12 |
| παράδεισος | `the park` | the chain of GEN 2:8, with the article | 13:10 |
| γῆ | `the earth` · `in earth` · `of the earth` | the chains of GEN 12 | 13:6–17 |
| πόλις, with ἐν | `in city` | `within, inside of, and by means of city, citadel, country, body of citizens, state` — the chain of GEN 4:17, anarthrous, after ἐν | 13:12 |
| πονηρός | `toilsome` | the chain of GEN 2:9, in the nominative | 13:13 |
| ἁμαρτωλός | `sinful` | `sinful, sinners` — the adjective, and as a noun *a sinner* | 13:13 |
| ὀφθαλμός | `the eyes` · `with the eyes` | the chain of GEN 3:5, in the form | 13:10, 13:14 |
| βορρᾶς | `north wind` | `north wind, the north, northward` — under Βορέας, whose *North* is set in lower case, as the Greek has it | 13:14 |
| ἀνατολή | `of risings` · `risings` | the chain of GEN 2:8, in the form | 13:11, 13:14 |
| θάλασσα | `sea` | the chain of GEN 12:8 | 13:14 |
| σπέρμα | `to that which is sown` · `that which is sown` | the chain of GEN 3:15, in the form | 13:15, 13:16 |
| αἰών | `of the period of existence` | the chain of GEN 3:22, in the genitive | 13:15 |
| ἄμμος | `the sand` | `the sand, the sandy ground and race-course` | 13:16 |
| τις | `any one` | the chain of GEN 6:5 | 13:16 |
| μῆκος, πλάτος | `the length` · `the breadth` | the chains of GEN 6:15 | 13:17 |
| δρῦς | `the tree` | the chain of GEN 12:6 | 13:18 |

### Nouns and adjectives new in GEN 12

| lemma | headword | chain | used |
| --- | --- | --- | --- |
| συγγένεια | `of the sameness of descent` | `of the sameness of descent, of the family and relationship and kin, of the ties of kindred and family connexion and influence, of the kinsfolk and kinsmen, of the families` | 12:1 |
| οἶκος (gen.) | `of the house` | the chain of GEN 7:1, in the genitive | 12:1 |
| ἔθνος (sg.) | `a number of people accustomed to live together` | the chain of GEN 10:5, in the singular | 12:2 |
| μέγας | `big` · `with big` | the chain of GEN 10:12, in the form | 12:2, 12:17 |
| τόπος | `of the place` | `of the place, of the local circumstances, of the position, of the passage in a book, of the topic, of the common-place, of the occasion and opportunity` | 12:6 |
| μῆκος | `the length` | the chain of GEN 6:15 | 12:6 |
| δρῦς | `the tree` | `the tree, the oak, the wood, the worn-out old man` — *originally a tree, commonly the oak* | 12:6 |
| ὑψηλός | `high` | the chain of GEN 7:19, after a plain *the* | 12:6 |
| ὄρος | `the mountain` | `the mountain, the hill` | 12:8 |
| σκηνή | `the covered place` | `the covered place, the tent, the camp, the dwelling-place, the temple` — the chain of GEN 4:20, in the singular | 12:8 |
| θάλασσα (anarthrous) | `sea` | `sea, the Mediterranean, a well of salt water` | 12:8 |
| ὄνομα with ἐπί | `to the name` | the chain of GEN 3:20, in the dative | 12:8 |
| ἔρημος, used as a noun | `in the desert part` | `within, inside of, and by means of the desert part, the desolate, the lone and lonely and lonesome and solitary, the helpless, the reft and void and destitute, the undefended` — *desert parts*, τὰ ἐρῆμα, is the entry's first noun sense; ἡ ἐρῆμος is given no translation of its own | 12:9 |
| λιμός | `hunger` · `the hunger` | `hunger, famine` | 12:10 |
| εὐπρόσωπος | `fair of face` | `fair of face, with glad countenance, fair in outward show and specious` | 12:11 |
| γυνή | `woman` · `to the woman` · `a woman` · `the woman` | the chains of GEN 2:22 and 8:16, in the form | 12:5, 12:11–20 |
| ψυχή | `breath` · `the breath` | the chain of GEN 2:7 | 12:5, 12:13 |
| καλός | `beautiful` | the chain of GEN 2:9 | 12:14 |
| ἄρχων | `the rulers` | `the rulers, the commanders, the chiefs, the captains, the chief magistrates` | 12:15 |
| πρόβατον | `things that walk forward` | the chain of GEN 4:2, in the nominative | 12:16 |
| μόσχος | `calves` | `calves, young bulls, heifers and young cows, boys and girls and maids, young animals` — under μόσχος² | 12:16 |
| ὄνος | `asses` | `asses, beasts of burden, windlasses and pulleys, upper millstones, beakers and wine-cups` | 12:16 |
| παῖς | `children` | the chain of GEN 9:25, in the plural | 12:16 |
| παιδίσκη | `young girls` | `young girls, maidens, young slaves, courtesans` | 12:16 |
| ἡμίονος | `half-asses` | `half-asses, mules, wild asses` | 12:16 |
| κάμηλος | `camels` | `camels, the camels in an army, the camelry and camel-brigade` | 12:16 |
| ἐτασμός | `with trials` | `with trials, with afflictions` — LSJ, through ἔτασις | 12:17 |
| πονηρός | `with toilsome` | the chain of GEN 2:9, in the dative | 12:17 |
| ἀνήρ | `to men` | the chain of GEN 4:23, in the dative plural | 12:20 |

### Nouns and adjectives new in GEN 11

| lemma | headword | chain | used |
| --- | --- | --- | --- |
| χεῖλος | `lip` · `the lips` | `lip, bill and beak, edge and brink and brim and rim`, in the number — *lip-service* and *with the lips*, pieces of proverbs, left out | 11:1, 11:6, 11:9 |
| εἷς (n.) | `one` | the chain of GEN 2:21 | 11:1, 11:6 |
| φωνή | `sound` · `the sound` | the chain of GEN 4:10, with and without the article | 11:1, 11:7 |
| πεδίον | `a plain` | the chain of GEN 4:8, without the article | 11:2 |
| πῦρ | `with fire` | `with fire, with the funeral-fire, with the fire of the hearth` — the entry's *symbol of things irresistible or terrible* left out | 11:3 |
| λίθος | `a stone` | `a stone, a precious stone, marble` | 11:3 |
| ἄσφαλτος | `asphalt` | `asphalt, bitumen` — the chain of GEN 6:14 | 11:3 |
| πηλός | `the clay` | `the clay, the earth, the mud, the mire` | 11:3 |
| πόλις | `a city` · `the city` | the chain of GEN 4:17 | 11:4, 11:5, 11:8 |
| πύργος | `a tower` · `the tower` | `a tower, the city walls with towers, a movable tower for storming, a tower of defence, the highest part of any building, troops drawn up in close order and a column`, with and without the article | 11:4, 11:5, 11:8 |
| κεφαλή | `the head` | the chain of GEN 3:15, with the article | 11:4 |
| πρόσωπον | `of face` · `face` | the chain of GEN 3:8, anarthrous | 11:4, 11:8, 11:9 |
| γένος | `race` | the chain of GEN 6:20 | 11:6 |
| γλῶσσα | `the tongue` | the chain of GEN 10:5, with the article | 11:7 |
| ὄνομα | `the name` · `a name` | the chains of GEN 3:20 and 2:11 | 11:4, 11:9, 11:29 |
| χώρα | `in the space in which a thing is` · `of the space …` | the chain of GEN 10:20, in the singular | 11:28, 11:31 |
| γυνή | `women` · `to the woman` · `a woman` | the chains of GEN 4:19 and 2:22, in the form | 11:29, 11:31 |
| πατήρ | `of the father` · `father` | the chains of GEN 9:22 and 9:18 | 11:28, 11:29 |
| στεῖρα | `a cow that has not calved` | `a cow that has not calved, barren` — *barren*, of a woman, is the entry's second translation, citing the New Testament | 11:30 |
| νύμφη | `the young wife` | `the young wife and bride, the married woman, the marriageable maiden, the nymph, the chrysalis and pupa` — *daughter-in-law*, the verse's sense, is sense 4, untagged | 11:31 |

### Nouns and adjectives new in GEN 10

| lemma | headword | chain | used |
| --- | --- | --- | --- |
| γένεσις (pl.) | `the origins` · `origins` | the chain of GEN 6:9, with and without the article | 10:1, 10:32 |
| ἔθνος (pl.) | `of the numbers of people accustomed to live together` · `in the …` · `the …` | `of the numbers of people accustomed to live together, of the companies and bodies of men, of the hosts, of the swarms and flocks, of the nations and peoples, of the nations and gentiles, of the special classes, of the castes and tribes, of the sexes`, in the form — *a nation* is sense 2; *Gentiles* lower case | 10:5, 10:20, 10:31, 10:32 |
| γῆ with ἐν | `in the earth` | `within, inside of, and by means of the land, the dry ground, the terrestrial realm` | 10:5, 10:10 |
| γλῶσσα | `tongue` · `tongues` | `tongue, tongue as the organ of speech, tongue and language, mouthpiece of a pipe`, in the number | 10:5, 10:20, 10:31 |
| φυλή (pl.) | `in the races` · `the races` | `within, inside of, and by means of the races, the tribes, the bodies united by ties of blood and descent, the clans, the tribes by local habitation, the hundreds and counties, the contingents furnished by a tribe, the brigades` | 10:5, 10:18, 10:20, 10:31, 10:32 |
| γίγας (sg.) | `giant` | `giant, son of Gaia, mighty` — the chain of GEN 6:4 in the singular | 10:8, 10:9 |
| κυνηγός | `hound-leader` | `hound-leader, huntsman` — under κυναγός | 10:9 |
| κύριος, θεός (gen.) | `of lord` · `of the God` | the chains of GEN 3:8 | 10:9 |
| ἀρχή | `beginning` | `beginning, origin, first cause, headship and rule and governing precedence` — the chain of GEN 2:10 in the singular | 10:10 |
| βασιλεία | `of the kingdom` | `of the kingdom, of the dominion, of the hereditary monarchy` | 10:10 |
| ἐκεῖνος (gen.) | `of that` | the chain of GEN 2:12 | 10:11 |
| πόλις | `the city` | the chain of GEN 4:17, with the article | 10:11, 10:12 |
| μέγας | `big` · `of the bigger` | `big, great, tall, full-grown, vast and high, spacious and wide, strong and mighty, violent, loud, prevailing, weighty and important`; the comparative, the chain of GEN 4:13 in the genitive | 10:12, 10:21 |
| ὅριον (pl.) | `the boundaries` | `the boundaries, the limits, the borders, the frontier` | 10:19 |
| χώρα (pl.) with ἐν | `in the spaces in which a thing is` | `within, inside of, and by means of the spaces in which a thing is, the places, the positions and posts, the places in life and stations, the lands and countries, the pieces of land and estates and farms, the countries` | 10:20, 10:31 |
| πατήρ (dat.) | `to father` | `to father, to grandfather` | 10:21 |
| ἀδελφός (dat.) | `to son of the same mother` · `to the son of the same mother` | the chain of GEN 4:2, in the form | 10:21, 10:25 |
| ὄνομα, εἷς | `a name` · `to the one` | the chains of GEN 2:11 | 10:25 |
| ὄρος (sg.) | `a mountain` | `a mountain, a hill` | 10:30 |
| ἀνατολή (gen. pl.) | `of risings` | the chain of GEN 2:8, in the genitive | 10:30 |

Nearly every other word of the chapter is a name. A people's name declined in Greek — Κίτιοι,
Ῥόδιοι, Χετταῖος, Ἀράδιος, Χαναναῖος — is glossed like a person's, with its English form in the
anchored panel (*Citians*, *Hittite*, *Canaanites*); where the Greek names a different people from
the Hebrew (Ῥόδιοι for *Dōdānîm*), it is the Greek's that is anchored, and the note gives the Hebrew.
A name glossed in one case is bare in another (Σιδῶνα at 10:15, Σιδῶνος at 10:19).

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
| Σηθ (GEN 5) | Sēth | Seth | `(Σηθ, from Hebrew Šēt, which 4:25 ties to šît, "to set, appoint")` |
| Καιναν | Kainan | Kenan | `(Καιναν, from Hebrew Qênān, usually connected with Qayin, the name of Cain)` |
| Μαλελεηλ | Maleleēl | Mahalalel | `(Μαλελεηλ, from Hebrew Mahălalʾēl, "praise of God")` |
| Ιαρεδ | Iared | Jared | `(Ιαρεδ, from Hebrew Yered, usually connected with yārad, "to go down")` |
| Μαθουσαλα (GEN 5) | Mathousala | Methuselah | `(Μαθουσαλα, from Hebrew Mĕtûšelaḥ, usually explained as "man of the javelin")` |
| Νωε | Nōe | Noah | `(Νωε, from Hebrew Nōaḥ, usually connected with nûaḥ, "to rest")` |
| Σημ | Sēm | Shem | `(Σημ, from Hebrew Šēm, "name")` |
| Χαμ | Cham | Ham | `(Χαμ, from Hebrew Ḥām, usually connected with ḥam, "hot")` |
| Ιαφεθ | Iapheth | Japheth | `(Ιαφεθ, from Hebrew Yepet, which 9:27 ties to pātâ, "to make wide")` |
| Χανααν | Chanaan | Canaan | `(Χανααν, from Hebrew Kĕnaʿan, of uncertain meaning)` |
| GEN 10 | | | ninety-one names, their glosses in `data/GEN/10.json`; the anchored forms are the English Bible's, and Κίτιοι, Ῥόδιοι are *Citians*, *Rhodians* |
| Σύγχυσις | Synchysis | Confusion | `(Σύγχυσις, "a commixture, confusion", for Hebrew Bābel, which the verse ties to bālal, "to confuse")` |
| Ραγαυ | Ragau | Reu | `(Ραγαυ, from Hebrew Rĕʿû, usually connected with rēaʿ, "friend")` |
| Σερουχ | Serouch | Serug | `(Σερουχ, from Hebrew Śĕrûg, of uncertain meaning)` |
| Ναχωρ | Nachōr | Nahor | `(Ναχωρ, from Hebrew Nāḥôr, of uncertain meaning)` |
| Θαρα | Thara | Terah | `(Θαρα, from Hebrew Teraḥ, of uncertain meaning)` |
| Αβραμ | Abram | Abram | `(Αβραμ, from Hebrew ʾAbrām, "the father is exalted")` |
| Αρραν | Arran | Haran | `(Αρραν, from Hebrew Hārān, of uncertain meaning)` |
| Λωτ | Lōt | Lot | `(Λωτ, from Hebrew Lôṭ, of uncertain meaning)` |
| Χαλδαίων | Chaldaiōn | Chaldeans | `(Χαλδαῖος, the Greek name of Hebrew Kaśdîm)` |
| Σαρα, Σαραν | Sara, Saran | Sarai | `(Σαρα, from Hebrew Śāray, usually connected with śārâ, "princess")` — bare in the accusative |
| Μελχα | Melcha | Milcah | `(Μελχα, from Hebrew Milkâ, usually connected with malkâ, "queen")` |
| Ιεσχα | Iescha | Iscah | `(Ιεσχα, from Hebrew Yiskâ, of uncertain meaning)` |
| Χαρραν | Charran | Haran | `(Χαρραν, from Hebrew Ḥārān, the city Harran)` |

| Αἴγυπτον | Aigypton | Egypt | `(Αἴγυπτος, the Greek name of the land; Hebrew Miṣrayim)` |
| Αἰγύπτιοι | Aigyptioi | Egyptians | `(Αἰγύπτιος, the man of Αἴγυπτος, Egypt)` |
| Φαραω | Pharaō | Pharaoh | `(Φαραω, from Hebrew Parʿōh, from the Egyptian for "great house")` |
| Συχεμ | Sychem | Shechem | `(Συχεμ, from Hebrew Šĕkem, "shoulder")` |
| Βαιθηλ | Baithēl | Bethel | `(Βαιθηλ, from Hebrew Bêt-ʾēl, "house of God")` |
| Αγγαι | Angai | Ai | `(Αγγαι, from Hebrew hāʿAy, "the ruin")` |
| Χαναναῖοι | Chananaioi | Canaanites | `(Χαναναῖος, from Hebrew Kĕnaʿănî, "of Canaan")` |

Αἰγύπτιοι and Αἴγυπτον stand in one verse at 12:14, and `validate.py` took the people for a case of
the land's name; names now match only where what differs is a case ending on both sides.

| Φερεζαῖοι | Pherezaioi | Perizzites | `(Φερεζαῖος, from Hebrew Pĕrizzî, usually connected with pĕrāzî, "a villager")` |
| Ιορδάνου | Iordanou | Jordan | `(Ἰορδάνης, from Hebrew Yardēn, usually connected with yārad, "to go down")` |
| Σοδομα, Σοδομοις | Sodoma, Sodomois | Sodom | `(Σόδομα, from Hebrew Sĕdōm, of uncertain meaning)` — the gloss of GEN 10:19; bare in the dative |
| Γομορρα | Gomorra | Gomorrah | `(Γόμορρα, from Hebrew ʿĂmōrâ, of uncertain meaning)` — the gloss of GEN 10:19 |
| Ζογορα | Zogora | Zoar | `(Ζογορα, from Hebrew Ṣōʿar, "small")` |
| Μαμβρη | Mambrē | Mamre | `(Μαμβρη, from Hebrew Mamrēʾ, of uncertain meaning)` |
| Χεβρων | Chebrōn | Hebron | `(Χεβρων, from Hebrew Ḥebrôn, usually connected with ḥeber, "association")` |

Σοδομοις at 13:12 is two letters longer than Σοδομα at 13:10, and `validate.py` matched two forms of
a name only within one letter of each other's length, which keeps Καιν apart from Καιναν. It now
allows more where both forms carry a case ending, with a test.

| Αμαρφαλ | Amarphal | Amraphel | `(Αμαρφαλ, from Hebrew ʾAmrāpel, of uncertain meaning)` |
| Αριωχ | Ariōch | Arioch | `(Αριωχ, from Hebrew ʾAryôk, of uncertain meaning)` |
| Ελλασαρ | Ellasar | Ellasar | `(Ελλασαρ, from Hebrew ʾEllāsār, of uncertain meaning)` |
| Χοδολλογομορ | Chodollogomor | Chedorlaomer | `(Χοδολλογομορ, from Hebrew Kĕdorlāʿōmer, usually connected with the Elamite for "servant of Lagamar")` |
| Θαργαλ | Thargal | Tidal | `(Θαργαλ, from Hebrew Tidʿāl, of uncertain meaning)` |
| Βαλλα | Balla | Bera | `(Βαλλα, from Hebrew Beraʿ, of uncertain meaning)` |
| Βαρσα | Barsa | Birsha | `(Βαρσα, from Hebrew Biršaʿ, of uncertain meaning)` |
| Σεννααρ (the king) | Sennaar | Shinab | `(Σεννααρ, for Hebrew Šinʾāb, of uncertain meaning)` |
| Συμοβορ | Symobor | Shemeber | `(Συμοβορ, from Hebrew Šemʾēber, of uncertain meaning)` |
| Βαλακ | Balak | Bela | `(Βαλακ, from Hebrew Belaʿ, usually connected with bālaʿ, "to swallow")` |
| Σηγωρ | Sēgōr | Zoar | `(Σηγωρ, from Hebrew Ṣōʿar, "small")` |
| Ασταρωθ, Καρναιν | Astarōth, Karnain | Ashteroth, Karnaim | `(Ασταρωθ, from Hebrew ʿAštĕrōt, the goddess Astarte, in the plural)`, `(Καρναιν, from Hebrew Qarnayim, "two horns")` |
| Ομμαίους | Ommaious | Emim | `(Ομμαῖος, from Hebrew ʾÊmîm, usually connected with ʾêmâ, "terror")` |
| Σαυη | Sauē | Shaveh | `(Σαυη, from Hebrew Šāwēh, "level plain")` |
| Χορραίους | Chorraious | Horites | `(Χορραῖος, from Hebrew Ḥōrî, usually connected with ḥōr, "cave")` |
| Σηιρ | Sēir | Seir | `(Σηιρ, from Hebrew Śēʿîr, "hairy")` |
| Φαραν | Pharan | Paran | `(Φαραν, from Hebrew Pāʾrān, of uncertain meaning)` |
| Καδης | Kadēs | Kadesh | `(Καδης, from Hebrew Qādēš, "holy")` |
| Αμαληκ | Amalēk | Amalek | `(Αμαληκ, from Hebrew ʿĂmālēq, of uncertain meaning)` |
| Ασασανθαμαρ | Asasanthamar | Hazazon-tamar | `(Ασασανθαμαρ, from Hebrew Ḥaṣăṣōn Tāmār, the second word "palm tree")` |
| Αμορις | Amoris | Amorite | `(Αμορις, from Hebrew hāʾĔmōrî, "the Amorite")` |
| Εσχωλ | Eschōl | Eshcol | `(Εσχωλ, from Hebrew ʾEškōl, "cluster")` |
| Αυναν | Aunan | Aner | `(Αυναν, from Hebrew ʿĀnēr, of uncertain meaning)` |
| Δαν | Dan | Dan | `(Δαν, from Hebrew Dān, "judge")` |
| Χωβα | Chōba | Hobah | `(Χωβα, from Hebrew Ḥôbâ, of uncertain meaning)` |
| Δαμασκοῦ | Damaskou | Damascus | `(Δαμασκός, from Hebrew Dammeśeq, of uncertain meaning)` |
| Μελχισεδεκ | Melchisedek | Melchizedek | `(Μελχισεδεκ, from Hebrew Malkî-ṣedeq, "king of righteousness")` |
| Σαλημ | Salēm | Salem | `(Σαλημ, from Hebrew Šālēm, usually connected with šālôm, "peace")` |

GEN 14 prints Σεννααρ twice for two bearers: the land, Shinar, at 14:1 and 14:9, and Shinab, king
of Adama, at 14:2. Each is glossed on its first occurrence. `validate.py` counted a name as glossed
by its Greek form alone, and would have called the king's gloss a second gloss of the land; it now
tells bearers apart by their English names, with a test, and `words.py` gives each card its own
bearer's gloss. Σηγωρ is the Ζογορα of 13:10, spelt another way.

| Μασεκ | Masek | Mesek | `(Μασεκ, from Hebrew mešeq, which the Hebrew does not use as a name, of uncertain meaning)` |
| Ελιεζερ | Eliezer | Eliezer | `(Ελιεζερ, from Hebrew ʾĔlîʿezer, "my God is help")` |
| Αμορραίων | Amorraiōn | Amorites | `(Αμορραῖος, from Hebrew ʾĔmōrî, of uncertain meaning)` |
| Καιναίους | Kainaious | Kenites | `(Καιναῖος, from Hebrew Qênî, usually connected with qayin, "smith")` |
| Κενεζαίους | Kenezaious | Kenizzites | `(Κενεζαῖος, from Hebrew Qĕnizzî, of uncertain meaning)` |
| Κεδμωναίους | Kedmōnaious | Kadmonites | `(Κεδμωναῖος, from Hebrew Qadmōnî, "eastern")` |
| Χετταίους | Chettaious | Hittites | `(Χετταῖος, from Hebrew Ḥittî, "of Ḥēt")` |
| Ραφαϊν | Raphain | Rephaim | `(Ραφαϊν, from Hebrew Rĕpāʾîm, of uncertain meaning)` |
| Ευαίους | Euaious | Hivites | `(Ευαῖος, from Hebrew Ḥiwwî, of uncertain meaning)` |
| Γεργεσαίους | Gergesaious | Girgashites | `(Γεργεσαῖος, from Hebrew Girgāšî, of uncertain meaning)` |
| Ιεβουσαίους | Iebousaious | Jebusites | `(Ιεβουσαῖος, from Hebrew Yĕbûsî, "of Jebus")` |

GEN 15:2's Μασεκ is the Hebrew *mešeq*, which occurs nowhere else and is not a name there; the
Greek makes it a woman's, the mother of Eliezer, whom it calls Δαμασκὸς Ελιεζερ.

| Αἰγυπτία | Aigyptia | Egyptian | `(Αἰγυπτία, the woman of Αἴγυπτος, Egypt)` |
| Αγαρ | Agar | Hagar | `(Αγαρ, from Hebrew Hāgār, of uncertain meaning)` |
| Σουρ | Sour | Shur | `(Σουρ, from Hebrew Šûr, "wall")` |
| Ισμαηλ | Ismaēl | Ishmael | `(Ισμαηλ, from Hebrew Yišmāʿēʾl, "God hears")` |
| Φρέαρ | Phrear | Well | `(Φρέαρ, "a well", the first word of the name the verse gives the well, for Hebrew Bĕʾēr laḥay rōʾî)` |
| Βαραδ | Barad | Bered | `(Βαραδ, from Hebrew Bered, "hail")` |

| Αβρααμ | Abraam | Abraham | `(Αβρααμ, from Hebrew ʾAbrāhām, which the Hebrew of 17:5 hears in ʾab hămôn gôyim, "father of a multitude of nations")` |
| Σαρρα | Sarra | Sarah | `(Σαρρα, from Hebrew Śārâ, "princess")` |
| Ισαακ | Isaak | Isaac | `(Ισαακ, from Hebrew Yiṣḥāq, "he laughs")` |

| Σοδομῖται | Sodomitai | Sodomites | `(Σοδομῖται, the men of Σόδομα, Sodom)` |
| Μωαβ | Mōab | Moab | `(Μωαβ, from Hebrew Môʾāb, of uncertain meaning)` |
| Μωαβιτῶν | Mōabitōn | Moabites | `(Μωαβῖται, the people of Μωαβ, Moab)` |
| Αμμαν | Amman | Ammon | `(Αμμαν, for Hebrew Ben-ʿammî, "son of my people")` |
| Αμμανιτῶν | Ammanitōn | Ammonites | `(Αμμανῖται, the people of Αμμαν, for Hebrew bĕnê-ʿammôn, the sons of Ammon)` |

| Γεραροις | Gerarois | Gerar | `(Γεραρα, from Hebrew Gĕrār, of uncertain meaning)` |
| Αβιμελεχ | Abimelech | Abimelech | `(Αβιμελεχ, from Hebrew ʾĂbîmelek, "my father is king")` |

| Οχοζαθ | Ochozath | Ahuzzath | `(Οχοζαθ, from Hebrew ʾĂḥuzzat, "possession")` |
| Φικολ | Phikol | Phicol | `(Φικολ, from Hebrew Pîkōl, of uncertain meaning)` |
| Φυλιστιιμ | Phylistiim | Philistines | `(Φυλιστιιμ, from Hebrew Pĕlištîm, the people of Pĕlešet)` |
<!-- name rows above -->

Σύγχυσις translates the name where 10:10 gave the city its Greek name, Βαβυλών; as with Ζωή at
3:20, the anchored form is the English of the name the Greek prints, *Confusion*. Αρραν the man
(*Hārān*) and Χαρραν the city (*Ḥārān*) are both *Haran* in English, and two names in Greek.

A name glossed again in a later chapter keeps its gloss, unless the gloss spoke of the verse it
stood in: Σηθ's *which the verse ties* becomes *which 4:25 ties*. Μαθουσαλα at GEN 5 is glossed
for Mĕtûšelaḥ himself, where 4:18 gave the Greek name to Mĕtûšāʾēl.

Where the Greek and the English Bible name the same person with one name, differently spelled,
the anchored form is the English Bible's: Ενως is *Enosh*, Καιναν *Kenan*. Luke 3:36–38 spells
Καιναν and Ιαρεδ Καϊνάμ and Ἰάρετ; for that reason their dictionary forms are the forms Rahlfs
prints, not MorphGNT's (see the second-pass brief).

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
