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
