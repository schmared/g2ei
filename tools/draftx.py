# -*- coding: utf-8 -*-
"""Readings, notes, hints and names for BOOK CH, from vBOOKCH.py (K, NAMES, H, V, N), merged
onto the skeleton and written to data/BOOK/CH.json.  python draftx.py EXO 1"""
import io
import json
import os
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")
SP = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SP)
import xbook  # noqa: E402
from corpus import C, ALL  # noqa: E402
from corpus import u  # noqa: E402

from _paths import ROOT, WORK, DECISIONS  # noqa: E402
EN = "within, inside of, and by means of "
BOOK, CH = sys.argv[1], int(sys.argv[2])


def each(pre, xs):
    return ", ".join(pre + x for x in xs)


def items(field, head, pick=None):
    """The corpus chain for (field, head) as a list of items, to re-inflect."""
    s = C(field, head, pick)
    return s[2:-2].split("|")[1].split(", ")


K = {}
V, H, N, NAMES = {}, {}, {}, {}


def R(s):
    return re.sub(r"\{(\w+)\}", lambda m: K[m.group(1)], s)


exec(io.open(os.path.join(WORK, "v%s%d.py" % (BOOK, CH)), encoding="utf-8").read())


# A verse already committed and not redrafted here stays as it is: John 1 began as 1:1, 1:2 and
# 1:6, and the rest of the chapter is drafted around them.
_path = "%s/data/%s/%d.json" % (ROOT, BOOK, CH)
KEPT = {v["ref"]: v for v in json.load(io.open(_path, encoding="utf-8"))} if os.path.exists(_path) else {}


def build():
    glossed = set()
    out = []
    for sk in xbook.skeleton(BOOK, CH):
        ref = sk["ref"].split()[1]
        if ref not in V and sk["ref"] in KEPT and KEPT[sk["ref"]].get("reading"):
            kept = KEPT[sk["ref"]]
            glossed.update(n["greek"] for n in kept.get("names", []) if n.get("gloss"))
            glossed.update(NAMES[n["greek"]][0] for n in kept.get("names", [])
                           if n.get("gloss") and n["greek"] in NAMES)
            out.append(kept)
            continue
        reading = V[ref]
        names = []
        for form in dict.fromkeys(re.findall(r"\[\[name:([^\]]+)\]\]", reading)):
            key, un, an, gloss = NAMES[form]
            if key in glossed:
                names.append({"greek": form, "unanchored": un, "anchored": an, "bare": True})
            else:
                names.append({"greek": form, "unanchored": un, "anchored": an, "gloss": gloss})
                glossed.add(key)
        v = {"ref": sk["ref"], "greek": sk["greek"], "hint": H[ref],
             "notes": [{"lemma": l, "flag": f, "text": t} for l, f, t in N[ref]],
             "reading": reading, "names": names}
        if "print" in sk:
            v = dict(v, **{"print": sk["print"]})
            v = {k: v[k] for k in ("ref", "greek", "print", "hint", "notes", "reading", "names")}
        for field in ("speech", "printed"):
            if field in sk:
                v[field] = sk[field]
        # a speech capital the chapter glosses as a name (Ῥαββί, Ἀμήν) is a name, not a speech-opener
        if v.get("speech"):
            v["speech"] = [w for w in v["speech"] if w not in NAMES]
            if not v["speech"]:
                del v["speech"]
        out.append(v)
    return out


verses = build()
for v in verses:
    if len(v["hint"]) > 140:
        print("long hint", v["ref"], len(v["hint"]))
io.open("%s/data/%s/%d.json" % (ROOT, BOOK, CH), "w", encoding="utf-8", newline="\n").write(
    json.dumps(verses, ensure_ascii=False, indent=2) + "\n")
print(len(verses), "verses written")
