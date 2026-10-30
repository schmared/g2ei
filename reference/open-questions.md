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

**Recommendation:** the whole range, and the check. A Greek reader hears φιλέω's kiss in a
farewell over a dead father; the chain should give it to the English reader too.
