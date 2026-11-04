# -*- coding: utf-8 -*-
"""For each lemma of a chapter: its forms here and every headword the corpus gives it.
python tools/headsx.py JHN 1"""
import collections
import sys

from _paths import ROOT  # noqa: E402
sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, ROOT + "/build")
import words as W  # noqa: E402
from corpus import CHAINS  # noqa: E402
import validate as V  # noqa: E402

book, ch = sys.argv[1], int(sys.argv[2])
tokens = (W.nt_tokens if book in W.NT else W.lxx_tokens)(book, ch) or {}
forms = collections.OrderedDict()
for vn in sorted(tokens, key=W.verse_order):
    for form, lemma, code, (parse, _) in tokens[vn]:
        if parse.startswith(("article", "personal pronoun", "relative pronoun", "demonstrative pronoun")) \
                or lemma == "καί" or lemma[:1].isupper():
            continue
        forms.setdefault(lemma, []).append("%s:%s" % (form, code.strip("-")))
byl = collections.defaultdict(list)
for (field, head) in CHAINS:
    for lem in V.lemmas(field):
        byl[lem.split(" + ")[0]].append(head if lem == field else "%s{%s}" % (head, field))
for lemma, fs in forms.items():
    hs = byl.get(lemma, [])
    print("%s  [%s]  ::  %s" % (lemma, " ".join(dict.fromkeys(fs)), " | ".join(hs) if hs else "NEW"))
