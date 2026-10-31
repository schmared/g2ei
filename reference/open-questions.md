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

## Q10. A transliteration with Greek endings — γειώρας

**Where:** EXO 12:19 ἔν τε τοῖς γειώραις.

**Now:** γειώρας is the Aramaic gîyôrāʾ, sojourner, in Greek letters, as πασχα is pasḥāʾ. But it
takes Greek case endings, and LSJ has an entry for it, *sojourner, proselyte*, so it is read as a word:
`in the sojourners, the proselytes`. πασχα, indeclinable and printed lower case, is a name, as
χερουβιμ at Genesis 3:24, and Middle Liddell's own entry for it is set aside.

- now: γειώρας a word, from LSJ; πασχα a name, `pascha (πασχα, from Aramaic pasḥāʾ, …)` / `passover`.
- alternative: both names, each with its gloss, by the rule that every obvious transliteration carries
  its meaning; or both words, each from its lexicon.

**The difference:** the rule names transliterations without saying whether a declined one counts; a
lexicon entry gives a word its range, which a name's gloss does not.

**Recommendation:** a word where it declines and a lexicon has it; a name where it is indeclinable,
whether or not a lexicon has it.

## Q11. A run split where a passive sense hid it — ἀναγγέλλω

**Where:** seventeen units from GEN 3:11 to EXO 4:28, and EXO 13:8.

**Now:** Middle Liddell gives ἀναγγέλλω *to carry back tidings of, report* as one translation, and a
passive example's *was reported* beside it. Every chain splits the run, `carried back tidings of,
reported`, and the one-translation check lets it pass because *reported* matches *was reported*. Filing
*was reported* as an example's piece, as EXO 13 first did, made all seventeen fail. EXO 13:8 follows the
corpus: `you will carry back tidings of, you will report`.

- now: `carried back tidings of, reported` — two items, as if two senses.
- the run whole: `carried back tidings of and reported` — one item, and *was reported* filed, or kept for
  the passive forms only.

**The difference:** *was reported* is ML's translation of a passive form in an example, the kind the
corpus files; kept, it lets an active chain split a run the rule says is one item.

**Recommendation:** join the run in all eighteen units, and give *was reported* to the passive forms by
`FORM_SENSES`.

## Q12. ὑπάρχω's card is unsettled

**Where:** six units, GEN to EXO 14:11 (`begins`, `the things beginning`, and now `the beginning`).

**Now:** the card for ὑπάρχω's verb forms still carries example pieces and labels — *had been made*,
*there is store*, *existing*, *current*, the Latin *quae cum ita sint*, *own proper*, *he will be on*,
*side* — and the chains read three items: `begins and makes a beginning, begins to be and comes into being
and arises and springs up, is in existence`. Middle Liddell's third sense is one translation, *to be in
existence, to be there, to be ready*, and the chain keeps a third of it.

- now: `is in existence`
- the run whole: `is in existence and is there and is ready`, and the senses past it that are senses —
  *to be*, *to be laid down, to be taken for granted*, *to belong to, fall to*, *to be devoted to*, *it is
  allowed, it is possible* — read in, with the pieces filed.

**The difference:** which of the entry's later translations are senses of the verb and which are its
participle's, its impersonal's or an example's is a sorting of the whole entry, not a fix to one unit.

**Recommendation:** settle the card in `NOT_SENSES` and `FORM_SENSES` (participle used as a noun apart,
impersonal apart), then reread the six units from it.

## Q13. An adverb its entry names and never glosses — ἐνδόξως

**Where:** EXO 15:1 and 15:21, ἐνδόξως γὰρ δεδόξασται.

**Now:** Middle Liddell has no ἐνδόξως; ἔνδοξος ends *adv. -ως, hence Sup. ἐνδοξότατα*, with no translation.
The corpus reads such adverbs from their adjective's entry (δικαίως, βαρέως, ἀφρόνως), making adverbs of
the adjective's senses. ἔνδοξος's first sense, *held in esteem or honour, of high repute*, has no English
adverb; its second, *notable*, has one. The reading keeps the first as it stands and makes the second an
adverb: `held in esteem and honour and of high repute, notably`.

- now: `held in esteem and honour and of high repute, notably`
- the adjective's senses as they stand: `held in esteem and honour and of high repute, notable`
- LSJ, which glosses the adverb's use (*glorious*): not available while Middle Liddell has the word.

**The difference:** the first reading mixes an adjective phrase with an adverb; the second reads an adverb as
an adjective. Neither adds a word the entry lacks.

**Recommendation:** keep it as it is: where English has the adverb, use it; where it has none, the entry's
phrase stands.

## Q14. A sense that points to another entry — πάγος, *= παγετός*

**Where:** EXO 16:14, ὡσεὶ πάγος ἐπὶ τῆς γῆς.

**Now:** Middle Liddell's πάγος reads *that which is fixed or firmly set: a mountain-peak, a rocky hill … the
Areopagus … = παγετός*, and παγετός is *frost*. The pointer is not a translation, so the card stops at the
Areopagus and the reading has no frost: `that which is fixed and firmly set, a mountain-peak and a rocky
hill, Areopagus`. Where a whole entry is a pointer (κατέναντι, *= κατεναντίον*; LSJ's λατρευτός, *= foreg.*;
ἁγίασμα, *= ἁγιαστήριον*), the corpus reads the entry pointed to.

- now: `…, Areopagus`
- the pointer read: `…, Areopagus, frost`

**The difference:** the second reads a sense-level pointer the way whole-entry pointers are already read; the
first keeps to the translations the entry prints.

**Recommendation:** read a sense-level *= X* as X's translations, appended in the pointer's place, by a table
beside `MARKUP_LOST` that names each one.

## Q15. παραγίνομαι's present reads four senses off the card — `comes to be beside`

**Where:** GEN 32:21, 45:19; EXO 18:6, 18:15, 19:9.

**Now:** the present reads `comes to be beside, is present, arrives, comes to help` (EXO 19:9 `I come to be
beside, …`), as EXO 8 settled it: "the present's `comes to be beside` is the present's". Every other form
reads the card's eight senses from its first translation, the one Perseus cuts to *near, attend upon* out of
*to be beside, to be by or near, attend upon*: the aorist `was near and attended upon, was present at, came to
one's side and came to aid and stood by and seconded and supported, …, was fully grown` (GEN 35:9, EXO 8,
18:12), the articular infinitive the same (EXO 2).

- now: `comes to be beside, is present, arrives, comes to help`
- the card read as the aorist reads it: `is near and attends upon, is present at, comes to one's side and comes to
  aid and stands by and seconds and supports, is at hand and is gained and accrues, comes to, arrives and comes
  up, comes to maturity, is fully grown`

**The difference:** the present's head *comes to be* is not in the entry, and it carries four of the eight
senses; the check that holds one word to one range compares one voice, and the present's middle/passive and the
aorist's middle are two.

**Recommendation:** read the present from the card as the aorist is read, and restore *to be beside, to be by or
near, attend upon* whole in `MARKUP_LOST`, so both heads begin where the entry does.

## Q16. κύριος with an infinitive — the noun or the adjective

**Where:** EXO 21:8, ἔθνει δὲ ἀλλοτρίῳ οὐ κύριός ἐστιν πωλεῖν αὐτήν.

**Now:** the noun, as the corpus reads κύριος in some five hundred places: `not lord is to exchange her`. The
second pass read the adjective, Middle Liddell's first entry, *κύριός εἰμι, c. inf., I have authority to do, am
entitled to do*, which is the construction here. Both entries are filed under one key, and the noun's card is the
adjective's entry.

- now: `not [[lord]] is to exchange her`
- the adjective: `not [[having power]] is to exchange her`, with the adjective's range: `having power and
  authority over and lord and master of, …`

**The difference:** the adjective is the construction Middle Liddell names for κύριος with an infinitive; the
noun keeps one reading of κύριος across the corpus.

**Recommendation:** code it A- and read the adjective's entry where κύριος is predicate with an infinitive, and
settle which entry the noun reads (ENTRY to the second) at the same time.

## Q17. The perfect's formula — after the first item, or after every item

**Where:** about a hundred perfect units across Genesis and Exodus carry *and it stands so* (*and standing so*)
after their first item only — λέγω `has said and it stands so, has spoken, …`, ὁράω `I have seen …`, ἄγω `have led
and it stands so, have carried, …` (GEN 46:32) — while ἕψω, δικαιόω (GEN 38:26), ἀναπληρόω and the notes' own row
for ἀκούω at GEN 23:15 carry it after every item.

- first item only: `having been sent up and forth and standing so, having been made to spring up, having been
  produced, …` (ἀνίημι, GEN 49:21)
- every item: `having been boiled and standing so, having been seethed and standing so, …` (ἕψω)

**The difference:** CLAUDE.md says the formula "follows the whole item", which settles where it goes inside an
and-joined run but not whether each item of a chain is a perfect of its own. A Greek reader hears one perfect,
and each sense is that perfect.

**Recommendation:** after every item, and a check that holds it, since each item is the form read in another
sense; EXO 23 follows the majority until this is settled.

## Q18. ἐξίστημι's intransitive chain does not come from Middle Liddell

**Where:** GEN 27:33, 42:28, 43:33, 45:26, EXO 18:9, 19:18 — `stood out of, changed and altered utterly, was
driven out of, was deranged, was astonished and amazed, gave way and retired, stood aside from and gave up`.

**Now:** a chain no card gives. Middle Liddell's intransitive section ("intr. in Pass. and Mid., with aor2, perf.,
and plup. act.") opens *to stand aside from*, and gives *is displaced, disordered*, *to shrink from, shun*, *to
retire from, give up possession of*, *to cease from, abandon*, *to lose*, *to be out of one's wits, to be
astonished, amazed*, *to degenerate*, *to change one's position, one's opinion*.

- now: `stood out of, changed and altered utterly, …`
- from the card: `stood aside from, was displaced and disordered, shrank from and shunned, retired from and gave
  up possession of, ceased from and abandoned, lost, was out of his wits and was astonished and amazed,
  degenerated, changed his position and his opinion`

**The difference:** the headword is not the lexicon's first sense in the form the text uses, which is the hard
rule; the old chain also carries the causal senses (*changed and altered utterly*) on intransitive forms.

**Recommendation:** re-read the six from the card with a `FORM_SENSES` rule for the intransitive tenses, as EXO
23:27 now does for the causal future, and restore *to lose one's father, give him up* in `MARKUP_LOST`.

## Q19. A compound's one translation that holds a simplex's headword

**Where:** GEN 50:7, καὶ ἀνέβη Ιωσηφ … καὶ συνανέβησαν αὐτῷ: συναναβαίνω has one translation, *to go up with*, so
it should be plain text, `went up with`; but ἀναβαίνω's unit in the same verse is headed `went up`, and the check
that no headword stands bare reads the plain `went up with` as that headword written out. The verse carries a
unit whose chain is its headword, `[[went up with|went up with]]`, which the rule says is not a unit.

- now: `[[went up with|went up with|συναναβαίνω]]`
- by the rule: `went up with`, plain text

**The difference:** the check cannot tell a word's own one-translation English from another word's headword written
bare; the unit satisfies the check and breaks the rule it exists to hold.

**Recommendation:** let the bare-headword check pass a plain run that is the whole of a word's single translation
in the chapter's word-by-word layer (συναναβαίνω, *to go up with*), and make GEN 50:7 plain text.

## Q20. LSJ's "Dim. of X" read as X's senses

**Where:** EXO 25:11, 24, 25 κυμάτιον, "Dim. of κῦμα I.3"; 25:33, 34 καρυΐσκος, "Dim. of κάρυον". LSJ gives
neither word a translation of its own beyond these (κυμάτιον adds *volute* and *groove*).

**Now:** each pointer is read as the senses of the sense it points to, as ἁγίασμα's "= ἁγιαστήριον" was read as *holy place, sanctuary*:
`waved mouldings and cymas, volutes, grooves`; `any kinds of nut, walnuts`.

- now: `[[any kinds of nut|any kinds of nut, walnuts]]`
- the other reading: the diminutive made explicit, `little nuts`, which composes rather than reads

**The difference:** "= X" says the words mean the same; "Dim. of X" says the word is a smaller X, which the
reading cannot say without adding *little* the entry does not print.

**Recommendation:** keep the pointer's senses and say "Dim." in the note, as now; the reading adds no word the
lexicon lacks.

## Q21. A passive whose English object sits inside a phrase

**Where:** EXO 27:20 κεκομμένον, κόπτω's perfect passive participle. Middle Liddell gives "k. τὴν χώραν «to cut down
the trees in» it, «to lay» it «waste»": in the active the land is the object, and the English puts it inside the
phrase, after *in*.

**Now:** the passive is said in English's own way, the land the subject: `having had the trees in it cut down`, and
`having been laid waste` from *to lay it waste*.

- now: `…, having been felled, having had the trees in it cut down, having been laid waste, …`
- the other reading: the gloss inflected as it stands, `having been cut down the trees in`, which is not English

**The difference:** English cannot passivise *to cut down the trees in it*; the only English passive adds *had* and
moves *it*, words the gloss carries in another order.

**Recommendation:** keep the English passive, as now, and say so in the note; or leave such senses out of a passive's
chain, as the middle's are left out, since the Greek passive of κόπτω with the land as subject is the same sense.

**Also:** EXO 28:14 καταμεμιγμένα, καταμίγνυμι's *to mix up, mingle the ingredients*: in the passive the ingredients
are the subject, `having been mixed up and mingled`; EXO 28:20 περικεκαλυμμένα, περικαλύπτω's *to throw a veil* (of
darkness over …): `having had a veil thrown over them`. EXO 31:18 γεγραμμένας, γράφω's *to write a person's name*: `having had a person's name
written`; its *to move that* is left out of the passive, whose subject cannot take the clause.

## Q22. ὑάκινθος: masculine by the lexicon's heading, feminine where the text marks it

**Where:** EXO 28:5 τὴν ὑάκινθον, 28:37 ὑακίνθου κεκλωσμένης; the corpus codes ὑάκινθος masculine everywhere else
(25:4, 26:1, 26:31, 26:36, 27:16, 28:8, 28:15, 28:33), "as Middle Liddell heads ὑάκινθος first", against the module's
feminine.

**Now:** feminine at 28:5 and 28:37, where the article and the participle show it, with a `# corpus` note; masculine
where nothing marks the gender.

- now: 28:5 `ASF`, 28:8 `GSM`, 28:37 `GSF`
- the other reading: feminine throughout Exodus, as the dye is wherever the text shows a gender

**The difference:** a Greek reader hears the gender the text gives the word; where it gives none, the masculine is
the project's choice, not the text's.

**Recommendation:** code the dye feminine throughout, as 28:5 and 28:37 show it, and drop the module notes that
defend the masculine.

## Q23. περισκελής: Middle Liddell has the key but not the word

**Where:** EXO 28:42 περισκελῆ λινᾶ. Middle Liddell's only περισκελής is the word from σκέλλω, *dry and hard all round,
exceeding hard; obstinate, stubborn*. LSJ has two: (A) the same, and (B), from σκέλος, *round the leg*, "hence
περισκελῆ, τά, drawers, LXX Ex. 28.38(42)".

**Now:** the rule's letter: LSJ answers only where Middle Liddell has no entry under the word's own key, and it has
one, so the reading is `dry and hard all round and exceeding hard, obstinate and stubborn`.

- now: `[[dry and hard all round|dry and hard all round and exceeding hard, obstinate and stubborn|περισκελής]]`
- the other reading: LSJ (B), `round the leg, drawers`

**The difference:** ENTRY already picks one homograph over another inside Middle Liddell (νέω2, *to spin*); here
Middle Liddell lacks the homograph, and the key leads to a different word.

**Recommendation:** let LSJ answer for a homograph Middle Liddell lacks, recorded in a table of its own with the
etymology that tells the two apart, and have validate.py accept the LSJ entry only through that table.

## Q24. Legacy chains short of their cards

**Where:** a chain written before its card was compared with it can drop senses no check sees: the ranges and chains
checks compare units with one another, not with the card. This session brought καθαρός, χαλκός, κέρας (EXO 27) and
γένεσις, στολή, σοφός (EXO 28) to their cards. `covx.py`, a scratch tool, lists for a chapter the card senses each
unit's chain does not carry; on EXO 28 it also reports χιτών (*a man's frock*, *the upper leather*, *any coat, case*),
σκηνή (*house*, *a wooden stage*, *the stage*) and ἐπάγω's active (*to induce*, *to bring in, supply*, *to
intercalate*), whose chains are recorded decisions in this file.

**Now:** those recorded chains are reused as they stand.

**The difference:** a sense dropped by an early chain is dropped from every later unit that copies it.

**Recommendation:** a check in validate.py that reads each unit against its card, with senses left out on purpose
moved into NOT_SENSES or FORM_SENSES so that the check has nothing else to report; then one pass over the corpus.

## Q25. An entry that marks no translation

**Where:** EXO 28:19 λιγύριον. LSJ: "a precious stone (Dim. of λίγυρος)", no translation marked; λίγυρος "= λιγύριον".
Middle Liddell has neither.

**Now:** the description is the English: *a precious stone*, plain text.

- now: `… the third a precious stone, agate and …`
- the other reading: the Greek transliterated, `ligurion (λιγύριον)`, as a word the lexicon names by its Greek

**The difference:** the description is LSJ's English but not marked as a translation; a transliteration adds nothing
the lexicon does not print but tells the reader less.

**Recommendation:** keep the description, as σμάραγδος's *a precious stone of a green colour* is kept from inside its
Latin.

## Q26. A first translation that is only a preposition

**Where:** EXO 31:3 θεῖον. Middle Liddell prints "«of» or «from the gods, sent by the gods, issuing from them,
divine»": Perseus marks *of* as a translation of its own, so the entry's first translation, read by its markup, is a
bare preposition.

**Now:** the headword is `of or from the gods`, the two translations the *or* joins read as one, as LSJ's μυρεψικός
*of or for unguents* at EXO 30:25. σοφός keeps its first translation alone, `skilled in any handicraft`, with *or art*
in the chain, because that one is a sense by itself.

- now: `of or from the gods — of or from the gods and sent by the gods and issuing from them and divine, … —`
- the other reading: `of — of or from the gods and sent by the gods …, … —`, the markup's first translation

**The difference:** *of* alone says nothing, and in the anchored panel it reads as a genitive's marker.

**Recommendation:** keep `of or from the gods`; where a first translation is a preposition or a particle that only an
*or* completes, read the *or* as the printed entry does.

## Q27. A gloss given in the plural, read in a singular form

**Where:** EXO 32:22 ὅρμημα and 32:16 γραφή. Middle Liddell gives ὅρμημα's *longings* and *struggles* from Homer's
plural ὁρμήματα, and γραφή's *statements* from an example in the plural, ψευδεῖς γραφαί.

**Now:** the singular form reads them in the singular, `the stir and impulse, the longing, the struggle`, as a plural
form reads a singular gloss in the plural (στολή, γένεσις). Where the entry says a sense belongs to the plural, "in pl."
or the plural named as the headword of a sense — τάλαντον's *scales*, τροπή's *tropics, solstices*, οἰκέτης's
*household* — the singular leaves it out (`FORM_SENSES`).

- now: `the stir and impulse, the longing, the struggle`
- the other reading: `the stir and impulse`, the plural example's glosses left to a plural form

**The difference:** a gloss that came from a plural example is the word's sense in that example, and the example
happens to be plural; a sense the entry assigns to the plural is the plural's own.

**Recommendation:** keep the distinction: inflect a gloss whose plural is only the example's, and leave out a sense
the entry gives to the plural.

## Q28. Anarthrous θεός used of another god

**Where:** EXO 34:14, οὐ γὰρ μὴ προσκυνήσητε θεῷ ἑτέρῳ, the first singular θεός without the article whose referent is
not the God of the text. The plural, θεοὶ ἕτεροι (EXO 20:3), reads `gods, the gods, goddesses`.

**Now:** the anarthrous formula, as the convention gives it for every anarthrous θεός: `to everything that God is by
nature, to deity in full and undiminished kind`, with ἑτέρῳ `to other` after it.

- now: `not for not you may make obeisance to everything that God is by nature, … to other`
- the other reading: the singular of the plural's chain, `to a god, to the god, to a goddess`

**The difference:** the formula says what the noun is by nature, and here the text denies that what it names is the
God at all; the plural's range treats θεός as a common noun.

**Recommendation:** keep the formula for anarthrous θεός where the referent is the God of the text, and read a
singular θεός qualified by ἕτερος or ἀλλότριος as the plural is read.

## Q29. δύο: plain text in most places, a unit in sixteen

**Where:** δύο's card reads `two` and `two and two`, the doubled δύο δύο. The validator's sense split reads `two and
two` as `two`, so it lets the word stand either way. About 111 of its 127 occurrences are plain; 16 are units, `the
two, the two and two` (GEN 44; EXO 2, 6, 12, 16, 18, 21, 31, 32, 34).

**Now:** both stand. EXO 36 follows EXO 28, its parallel, and prints δύο plain.

- now: `the two [[rings|…]]` at 36:23, beside `[[the two|the two, the two and two|δύο]]` at EXO 31:18
- the other reading: a unit everywhere, `two — two, two and two —`

**The difference:** *two and two* is the distributive the doubled word makes; a Greek reader hears it only where
δύο stands twice.

**Recommendation:** plain wherever a single δύο stands, the sixteen units flattened, and `two and two` set aside in
`NOT_SENSES` as the doubled construction's.
