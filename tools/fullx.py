# -*- coding: utf-8 -*-
"""Each form's card, for the lemmas named: python tools/fullx.py JHN 1 λόγος φῶς …"""
import io
import sys

from _paths import ROOT  # noqa: E402
sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, ROOT + "/build")
import words as W  # noqa: E402

entries = W.load_middle_liddell()
BOOK, CH = sys.argv[1], int(sys.argv[2])
tokens = (W.nt_tokens if BOOK in W.NT else W.lxx_tokens)(BOOK, CH) or {}
want = set(sys.argv[3:])
done = set()
for vn in sorted(tokens, key=W.verse_order):
    for form, lemma, code, (parse, _) in tokens[vn]:
        if lemma in want and (lemma, code) not in done:
            done.add((lemma, code))
            s = W.lexicon_senses(entries, lemma, code, form, parse)
            if s is None or lemma in W.LSJ_HOMOGRAPHS:
                s = W.lsj_senses(lemma, code, form)
            print("%s %s %s %s :: %s" % (vn, form, code, lemma, " | ".join(s or [])))
