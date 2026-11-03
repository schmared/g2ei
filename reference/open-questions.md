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

**Since EXO 36:** the first half is done. EXO 36:4's imperfect παρεγίνοντο shares the present's voice code, so one
word, one range set the four-sense present against the eight-sense imperfect, and the five present units now read
the card as the aorist does: `is near and attends upon, …, is fully grown` (`I am near …`, `be near …`). The
`MARKUP_LOST` restoration of *to be beside, to be by or near* is not done; the heads still begin at *near*.

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
