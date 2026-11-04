# -*- coding: utf-8 -*-
"""Corpus chains: (lemma field, headword) -> chain, read from the committed data."""
import glob, io, json, re, sys
from _paths import ROOT, WORK, DECISIONS  # noqa: E402
sys.path.insert(0, ROOT + "/build")
import validate as V
CHAINS = {}
ALL = {}
# drafting a chapter reads every chapter but that one, whose old draft would otherwise
# stand beside the chains being written for it
SKIP = ("/data/%s/%s.json" % tuple(sys.argv[1:3])) if sys.argv[0].endswith("draftx.py") and len(sys.argv) > 2 else None
for p in sorted(glob.glob(ROOT + "/data/*/*.json")):
    if "words" in p or (SKIP and p.replace("\\", "/").endswith(SKIP)):
        continue
    for v in json.load(io.open(p, encoding="utf-8")):
        for head, chain, field in V.units(v["reading"]):
            CHAINS.setdefault((field, head), chain)
            ALL.setdefault((field, head), [])
            if chain not in ALL[(field, head)]:
                ALL[(field, head)].append(chain)


def u(head, chain, lemma):
    """A unit written out: [[head|chain|lemma]]."""
    return "[[%s|%s|%s]]" % (head, chain, lemma)


def C(field, head, pick=None):
    """The corpus's unit for this word and headword, as a [[...]] string. Where the corpus
    holds more than one chain for the pair (a singular and a plural verb), `pick` is a
    piece of text the wanted one holds, and an ambiguous pair without it is an error."""
    found = ALL[(field, head)]
    if pick is not None:
        found = [c for c in found if pick in c]
    if len(found) != 1:
        raise KeyError("%s / %s: %d chains%s" % (field, head, len(found),
                       "".join("\n   " + c for c in ALL[(field, head)])))
    return "[[%s|%s|%s]]" % (head, found[0], field)


def heads(field):
    return sorted({h for (f, h) in CHAINS if f == field})
