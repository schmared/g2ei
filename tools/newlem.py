# -*- coding: utf-8 -*-
"""Lemmas of a chapter that no other chapter of the page has: python tools/newlem.py JHN 2"""
import sys

from _paths import ROOT  # noqa: E402
sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, ROOT + "/build")
import render  # noqa: E402
import words as W  # noqa: E402


def lemmas(book, ch):
    tokens = (W.nt_tokens if book in W.NT else W.lxx_tokens)(book, ch) or {}
    for vn in sorted(tokens, key=W.verse_order):
        for form, lemma, *_ in tokens[vn]:
            yield lemma


book, ch = sys.argv[1], int(sys.argv[2])
seen = set()
for b, c in render.PAGE:
    if (b, c) != (book, ch):
        seen.update(lemmas(b, c))
new = []
for x in lemmas(book, ch):
    if x not in seen and x not in new:
        new.append(x)
print(" ".join(new))
