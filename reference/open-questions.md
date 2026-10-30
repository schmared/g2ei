# Open questions

Judgment calls made during a multi-chapter run, for an edit pass afterwards. Each one records the
reading the text has now (the nearest precedent), the alternative, and examples side by side. None
of these is a defect under a rule already set — those are fixed when found. Settle one, apply it
across the corpus, and delete its entry.

## Q1. A chain that stops before the end of its entry — φιλέω

**Where:** every φιλέω unit: GEN 27:4, 27:9, 27:14, 27:26, 27:27, 29:11, 29:13, 33:4, 37:4, 48:10, 50:1.

**Now:** `loved, regarded with affection, felt affection, loved and cherished, treated
affectionately and kindly and welcomed` — Middle Liddell's sense I only. The entry goes on: *to
kiss* (sense II), then *to love, like, approve*, *to be fond*, *to be wont, used, apt*. Where the
Hebrew has *kiss* (nāšaq: 27:26, 27:27, 29:11, 29:13, 33:4, 48:10, 50:1) the reader never sees the
word.

**The rule says** the chain is the whole range, and that would put *kissed* in it:

| | 50:1 *καὶ ἐφίλησεν αὐτόν* |
|---|---|
| now | `loved, regarded with affection, felt affection, loved and cherished, treated affectionately and kindly and welcomed` |
| whole range | `loved, regarded with affection, felt affection, loved and cherished, treated affectionately and kindly and welcomed, kissed, loved and liked and approved, was fond, was wont and used and apt` |

**Why it is a question and not a fix:** GEN 27's lexicon note chose sense I on purpose (*`love`
where the Hebrew has kiss*), and nothing in `validate.py` checks that a chain covers its card — the
checks compare chains of one lemma with each other, not with the entry. So other chains may stop
early the same way. The fix is a new check (a chain must carry every sense its card gives, after
`NOT_SENSES`) and then whatever it finds.

**Also:** προσάγω (GEN, EXO 3:4) — its chains stop before the intransitive *to draw near*, which is
the sense of προσάγει at EXO 3:4.

**Recommendation:** the whole range, and the check. A Greek reader hears φιλέω's kiss in a
farewell over a dead father; the chain should give it to the English reader too.

## Q2. *X or Y*: three treatments of one shape

**Where:** any entry that writes two translations joined by *or* and tags them apart, `«to go up
with» or «together»`.

**Now:** the corpus does three things with them.

| treatment | example | chain |
|---|---|---|
| joined with *and* | ἐφίστημι perfect, GEN 24; κατασοφίζομαι, ἐπιστάτης, EXO 1 | `I have stood by and near`, `let us conquer by sophisms and fallacies and outwit` |
| the piece dropped | θῆλυς (*of or belonging to women*); συναναβαίνω (*to go up with or together*), GEN 50 | `belonging to women`; `went up with` |
| kept as an item of its own | ἐπανέρχομαι, GEN 50:5 (*to go up or pass from one place to another*) | `I will go up, I will pass` |

**The difference:** a piece that is not a translation by itself (*of*, *together*, *near*) reads
wrongly as an item of its own; one that is (*pass*) loses a sense if it is dropped. Joining with
*and* keeps both and reads as the one sense the entry means.

**Recommendation:** join with *and* everywhere, in the entry's own order — `went up with and
together`, `of and belonging to women` — and add a check that no tagged piece is dropped.

## Q3. A sense LSJ gives one form only — πανοικίᾳ

**Where:** EXO 1:1 πανοικίᾳ, and any later LSJ word whose entry gives a form a sense of its own.

**Now:** LSJ's πανοικία reads *whole household*, then *dat. as Adv., πανοικίᾳ with all the house*.
`FORM_SENSES` can split Middle Liddell's senses by form, but an LSJ entry is one fixed list for every
form, so the dative's *with all the house* cannot be given to the dative without being given to the
nominative of GEN 50:8 too. EXO 1:1 has `to whole household` as plain text.

| | EXO 1:1 *ἕκαστος πανοικίᾳ αὐτῶν* |
|---|---|
| now | `to whole household of them` |
| with the dative's sense | a unit, `to whole household, with all the house` |

**Recommendation:** let an LSJ entry take the same form rules as Middle Liddell's (a small change in
`words.py` and the checks that read LSJ), then open πανοικίᾳ.

## Q4. The case marker on a sense that is the case's own English — βίᾳ

**Where:** EXO 1:13 βίᾳ.

**Now:** `to bodily strength and force and power and might, to force and an act of violence, against
one's will and in spite of, perforce` — the marker *to* on the noun's senses, none on the dative's
own adverbial senses, where Middle Liddell's English already renders the dative (*perforce*). The
rule says every dative unit opens with *to*, which this does; it says nothing of later items, and
the corpus marks every item elsewhere.

| | reads |
|---|---|
| now | `…, against one's will and in spite of, perforce` |
| every item marked | `…, to against one's will and in spite of, to perforce` |

**Recommendation:** leave them unmarked, as ἐν's own English is (*within, inside of, and by means
of*): the marker shows a form English cannot, and these senses are that form in English already.

## Q5. *Strengthd. for X*: is that a pointer? — κατεμβλέπω

**Where:** EXO 3:6 κατεμβλέψαι.

**Now:** LSJ's κατεμβλέπω reads *strengthd. for ἐμβλέπω*, citing this verse, then its one
translation, *look down upon, despise*, from a later writer. The chain follows the pointer, as `=
X` pointers are followed (θηριόβρωτος, ἀσφαλτόπισσα, θλιμμός), and keeps the entry's own sense
after it.

| | 3:6 *εὐλαβεῖτο γὰρ κατεμβλέψαι ἐνώπιον τοῦ θεοῦ* |
|---|---|
| now (pointer followed) | `to look in the face and look at, to consider, to look into, to look, to look down upon and despise` |
| the entry's translation only | `to look down upon and despise` |

**Recommendation:** keep following it. The entry's only `<tr>` belongs to another writer, and LSJ
itself says what the word means here by sending the reader to ἐμβλέπω.

## Q6. The reflexive dative in plain text — ἑαυτοῖς

**Where:** GEN 3:7, 6:2, 6:4, 11:4, 11:29, 47:23; EXO 5:7, 5:11.

**Now:** ἑαυτοῖς is a pronoun and stays plain text, and the corpus reads it two ways: *for
themselves* (GEN 3:7, 6:2, 6:4, 11:4, 11:29, EXO 5:7) and *to yourselves* (GEN 47:23, EXO 5:11).
At EXO 5:11 *for* was not open to it: γάρ's unit heads with *for* in the same verse, and a plain
*for* beside it reads as the particle left bare.

| | EXO 5:7 *συναγαγέτωσαν ἑαυτοῖς ἄχυρα* | EXO 5:11 *συλλέγετε ἑαυτοῖς ἄχυρα* |
|---|---|---|
| now | `let them bring together for themselves husks` | `collect to yourselves husks` |
| the case's marker everywhere | `… to themselves husks` | `… to yourselves husks` |

**The difference:** *for* says what the dative is for here, which is a reading of its use; *to* is
the dative's marker on every declined word, whatever the use. A pronoun has not been held to the
marker, but nothing in the rule exempts it.

**Recommendation:** *to* everywhere, as the case's own marker, and the six *for*s changed.

## Q7. An example's translation that names a sense

**Where:** EXO 5: φόνος, καλάμη, σύνταξις; earlier, ψῆφος (EXO 4), κωφός (EXO 4).

**Now:** Middle Liddell often translates a whole example phrase, and only part of the
translation is the word's. The corpus files such a translation in `NOT_SENSES` when it is the
phrase's (ψῆφος's *by vote*) or repeats a sense above it, and keeps it when it is the word's own
English in that use. Three calls in EXO 5 sit near the line:

| entry | the run | now |
|---|---|---|
| φόνος | *f. ἑκούσιος and ἀκούσιος «murder and manslaughter»* | filed: the adjectives carry the difference |
| καλάμη | *perceive «the stubble» (i. e. «the residue)» of former strength* | filed: says what the metaphor means |
| σύνταξις | *ἡ εἰς μυρίους σ. their «contingent» towards 10,000* | kept: σύνταξις itself, in that use |

**Recommendation:** the test the corpus has used — keep a translation of the word, file a
translation of the phrase — written down in `/reference/lexicon-notes.md`, so these calls are made
the same way each time.

## Q8. A phrase's translation that names the phrase in the text — ἐρυθρός

**Where:** EXO 10:19 εἰς τὴν ἐρυθρὰν θάλασσαν.

**Now:** Middle Liddell's ἐρυθρός opens *red*, then translates the phrase Ἐρυθρὴ θάλασσα: *the
Erythraean sea*, including *the Red Sea* or *Arabian Gulf* and *the Indian Ocean*, later *the
Persian Gulf*. By Q7's test those are the phrase's, since θάλασσα gives the *sea*, and they are in
`NOT_SENSES`. ἐρυθρός is left one translation, *red*, plain text, and the names go in a note. Here,
unlike Q7's cases, the phrase itself is in the text.

- now: `into the red` and θάλασσα's unit, `sea`.
- the names kept: ἐρυθρός a unit, `the red` — `the red, the Erythraean sea, Red Sea, Arabian Gulf,
  Indian Ocean, the Persian Gulf` — and then `sea`.

**The difference:** kept, the adjective's chain says *sea* beside θάλασσα's own unit, and names
places the adjective alone does not; filed, the reading loses the lexicon's word that this is the
Red Sea, which only the note keeps.

**Recommendation:** filed, as now: the reading opens each Greek word, and *sea* is θάλασσα's.

## Q9. The third person imperative: *let him go up* or *let go up*

**Where:** every third person singular imperative; EXO 10:12, 10:24, 11:2 most recently.

**Now:** the corpus does both. Sixteen units carry a pronoun (`let him sprinkle`, EXO 9:8; `let him
go up`; `let her have`; `let it be watched`); about twenty do not (`let come into being`, EXO 9:9;
`let give`; `let take its rest`). EXO 10 and 11 follow the second where the subject is named in the
verse.

| | EXO 9:8 πασάτω Μωυσῆς | EXO 11:2 αἰτησάτω ἕκαστος |
|---|---|---|
| with a pronoun | `let him sprinkle Moses` | `let him ask every` |
| without | `let sprinkle Moses` | `let ask every` |

**The difference:** the Greek ending says the person and number and nothing of gender; *him* adds a
gender the form does not carry, and beside a named subject says it twice. Without a pronoun the
English imperative still marks the third person by *let* and the subject that follows.

**Recommendation:** no pronoun where the subject is in the verse, and *him*, *her* or *it* only where
the verb stands alone, by the gender of what it refers to.
