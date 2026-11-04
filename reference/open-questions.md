# Open questions

Judgment calls made during a multi-chapter run, for an edit pass afterwards. Each one records the
reading the text has now (the nearest precedent), the alternative, and examples side by side. None
of these is a defect under a rule already set — those are fixed when found. Settle one, apply it
across the corpus, and delete its entry.

## Q32. Chain items no card translation gives

**Where:** 160 distinct items in 1,729 units, after the coverage pass. The largest: δέ's `however` (all 1,255
units); ἄνθρωπος's `the human being` (about 120); παῖς's `the grandchildren`; ἕτερος's `worse`; μαῖα's `the
midwives`; ἀρχή's `the headship and rule and governing precedence` beside the card's senses.

**Now:** kept where they stood. The coverage check reads what a chain leaves out of its card, not what it adds
beyond it. In the twenty-odd words whose forms had to be brought to one range, such items were dropped.

- now: `but, however, while / whereas / on the other hand, then / yet, …` (δέ)
- the other reading: `but, while / whereas / on the other hand, then / yet, …`

**The difference:** the hard rule makes the chain the lexicon's range. An item from no translation is English
the Greek word was never given. Some are older readings of a sense the pass set aside. παῖς's *a child's child,
grandchild* was filed as the phrase παῖς παιδός's, and the item that rendered it stayed.

**Recommendation:** a check that every item renders a translation on the card. Then, for each of the 160, either
drop the item or settle the sense it came from.

## Q33. The coverage pass's calls

**Where:** `COVERAGE_NOT` and `COVERAGE_ONLY` in `build/words.py`, about 3,500 verdicts on the translations chains
had left out.

**Now:** six agents made the calls, each from a brief that gives the test the corpus uses (Q7). I read samples and
every addition the rebuild flagged as suspect, and overrode about sixty in `dec9_manual`. A sense of some forms
only is mapped onto the parse coarsely:
- *neuter used as a noun* is every neuter form;
- *first aorist* is every aorist;
- *used as an adjective* cannot be told from a noun use at all.

The chains of the commonest verbs are now long: λέγω, ποιέω, λαμβάνω, φέρω and ἔχω run to twenty or forty items.

**The difference:** most calls are the lexicon read as written. The rest are judgments the corpus has made one way
before, each now made at scale by a reader working alone.

**Recommendation:** read the two tables word by word for the fifty most frequent lemmas, beginning with the verbs
above, and move any call you would make differently.

## Q34. Pronouns and γίνομαι outside the coverage check

**Where:** οὗτος, ἐκεῖνος, ὅσος, τις, ὅς, τοιοῦτος (pronouns); γίνομαι (256 units).

**Now:** the check leaves out the pronouns, as the one-sense rule does (CONTENT_WORDS). It also leaves out γίνομαι,
whose `came to be, arose, was brought into existence` is the formula CLAUDE.md sets against εἰμί. Their chains are
short of their cards: οὗτος `of these, of the nearer, of what follows` beside an entry of about thirty
translations.

**The difference:** a pronoun's entry is mostly grammar. γίνομαι's formula is the reading's own wording, chosen for
the contrast with ἦν, and the card would bury it under *to be born, to be produced, to take place*.

**Recommendation:** keep both outside, and say so in CLAUDE.md's validation list.

## Q35. Passive forms of senses that have no passive

**Where:** passive units of verbs whose cards gained intransitive or active-only senses: φαίνω, ὁράω, ἔχω, καλέω and
others.

**Now:** the rebuild renders each new sense in the unit's form, so a passive unit renders every translation as a
passive. Where English has no passive of the sense, the result is wrong:
- `was given light`, `was appeared` (φαίνω), fixed by hand to the English the passive means;
- `was had sight` (ὁράω), set aside as a sense with no passive (`COVERAGE_ONLY`, *not passive*).

Others of the same kind may remain.

**The difference:** the passive rule leaves out a sense with no passive. Whether a sense has one is a judgment
about English the rebuild cannot make.

**Recommendation:** list every item the rebuild added to a passive unit, and settle each: a passive the English
has, the sense left out, or the passive's own intransitive English (*came to light*).

