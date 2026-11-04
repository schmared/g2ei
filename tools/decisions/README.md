# Coverage verdicts

One row per translation on one card, JSON lines: `lemma`, `key` (the Middle Liddell key, homograph digit
dropped), `sense` (the translation as the card gives it), `verdict` (`NOT`, `FORM` or `KEEP`), `code` (for
`FORM`, a `FORMS` name in `build/words.py`, or a description `applydec.py` maps to one), `why`.

`dec1`–`dec6` (and `dec1_hidden`, `dec3_extra`) are the Q24 coverage pass, each made by an agent from one brief
(the test the corpus uses, Q7). `dec9_manual` (from `mkdec9.py`) and `dec9z_q33` (from `mkdec10.py`) are made by
hand — the review of the pass's additions, and the Q32–Q35 edit pass — and replace an earlier call on the same
translation. `python tools/applydec.py --write` turns them into `COVERAGE_NOT` and `COVERAGE_ONLY`.
