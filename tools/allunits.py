# -*- coding: utf-8 -*-
"""Every unit of the corpus with its word's form, code, parse and card, pickled for the tools.

python tools/allunits.py  ->  WORK/allunits.pkl: [(book, ch, vi, ui, ref, head, chain, field, form, code, parse, card)]
vi is the verse's index in its chapter file, ui the unit's index in its reading. Units are paired with
the occurrence they open by validate.aligned_units, as the checks pair them."""
import io
import json
import os
import pickle
import sys

sys.stdout.reconfigure(encoding="utf-8")
from _paths import ROOT, WORK  # noqa: E402
sys.path.insert(0, ROOT + "/build")
import render  # noqa: E402
import validate as V  # noqa: E402

out = []
chapters = {}
for book, ch in render.PAGE:
    chapters.setdefault(book, []).append(ch)
for book, chs in chapters.items():
    for ch in chs:
        data = json.load(io.open("%s/data/%s/%d.json" % (ROOT, book, ch), encoding="utf-8"))
        index = {id(v): vi for vi, v in enumerate(data)}
        ui = {}
        for verse, head, chain, field, place, card, parse in V.aligned_units(book, ch, data):
            vi = index[id(verse)]
            n = ui[vi] = ui.get(vi, -1) + 1
            form, code = (place[0], place[2]) if place else ("", "")
            out.append((book, ch, vi, n, verse["ref"], head, chain, field, form, code, parse, card))
pickle.dump(out, open(os.path.join(WORK, "allunits.pkl"), "wb"))
print(len(out), "units")
