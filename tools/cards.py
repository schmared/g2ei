# -*- coding: utf-8 -*-
"""Q33: each lemma's card with every translation's verdict, and the entry's text around it.

python review33.py LEMMA ... | --top N [--extra L ...]  ->  review33.txt"""
import collections
import io
import os
import pickle
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")
SP = os.path.dirname(os.path.abspath(__file__))
from _paths import ROOT, WORK, DECISIONS  # noqa: E402
sys.path.insert(0, ROOT + "/build")
import validate as V  # noqa: E402
import words as W  # noqa: E402

E = W.load_middle_liddell()
XML = W.MIDDLE_LIDDELL.read_text(encoding="utf-8")
BODY = {m.group(1): m.group(2) for m in re.finditer(r'<entry\b[^>]*\bkey="([^"]+)"[^>]*>(.*?)</entry>', XML, re.S)}


def text_of(key):
    body = BODY.get(key) or BODY.get(key + "1")
    if not body:
        return ""
    start = body.find("<sense")
    body = body[start:] if start >= 0 else body
    body = re.sub(r"<tr\b[^>]*>(.*?)</tr>", lambda m: "«" + re.sub(r"<[^>]+>", "", m.group(1)) + "»", body, flags=re.S)
    body = re.sub(r'<sense\b[^>]*n="([^"]*)"[^>]*>', r" [\1] ", body)
    body = re.sub(r'<foreign[^>]*lang="greek"[^>]*>(.*?)</foreign>', lambda m: W_greek(m.group(1)), body, flags=re.S)
    body = re.sub(r"<bibl\b.*?</bibl>", "", body, flags=re.S)
    body = re.sub(r"<[^>]+>", "", body)
    return re.sub(r"\s+", " ", body).strip()


def W_greek(b):
    try:
        return W.greek(b) if hasattr(W, "greek") else b
    except Exception:
        return b


def verdict(bare, lemma, sense):
    out = []
    if sense in W.NOT_SENSES.get(bare, set()) | W.NOT_SENSES.get(W.beta(lemma), set()):
        out.append("NOT_SENSES")
    for k in (bare, W.beta(lemma)):
        if sense in W.COVERAGE_NOT.get(k, {}):
            out.append("NOT: " + W.COVERAGE_NOT[k][sense])
    only = dict(W.COVERAGE_ONLY.get(bare, {}))
    only.update(W.FORM_ONLY.get(bare, {}))
    if sense in only:
        out.append("ONLY " + only[sense])
    for rule in W.FORM_SENSES.get(bare, []):
        if sense in rule[2]:
            out.append("FS-skip(%s/%s)" % (rule[0], rule[1]))
    return "; ".join(out) or "KEEP"


def main():
    args = sys.argv[1:]
    units = pickle.load(open(os.path.join(WORK, "allunits.pkl"), "rb"))
    count = collections.Counter(V.lemmas(u[7])[-1] for u in units if u[11])
    lemmas = []
    if "--top" in args:
        lemmas = [l for l, _ in count.most_common(int(args[args.index("--top") + 1]))]
    if "--extra" in args:
        lemmas += args[args.index("--extra") + 1:]
    elif "--top" not in args:
        lemmas = args
    out = io.open(os.path.join(WORK, "review33.txt"), "w", encoding="utf-8")
    for lemma in lemmas:
        if lemma in V.COVERAGE_FORMULAS:
            continue
        keys = W.entry_keys(W.SPELLING.get(W.beta(lemma), W.beta(lemma)))
        for key in keys:
            senses = E.get(key)
            if not senses:
                continue
            bare = re.sub(r"\d+$", "", key)
            out.write("=" * 100 + "\n%s  %s  (%d units)\n" % (lemma, key, count[lemma]))
            out.write(text_of(key)[:6000] + "\n--\n")
            for i, s in enumerate(senses):
                out.write("  %2d. %-60s %s\n" % (i, s, verdict(bare, lemma, s)))
    out.close()


main()
