# -*- coding: utf-8 -*-
"""Per-chapter tools for any book, keyed by BOOK CH (EXO 1). Files in the work folder (tools/work, _paths.WORK):
  exo1.txt          transcription: ref TAB page TAB greek
  exo1.speech       ref TAB word word …   (speech capitals; optional)
  exo1.printed      ref TAB word word …   (printed forms the module differs on; optional)
  fixEXO1.py        F = {"v.n": "pos code lemma"} for the first pass
Commands:
  python xbook.py brief EXO 1     the second-pass brief, briefEXO1.md
  python xbook.py seed EXO 1      exo1.seed.txt and exo1.draft.txt from the whole corpus
  python xbook.py first EXO 1     firstEXO1.txt from the draft and fixEXO1.py
  python xbook.py morph EXO 1     data/EXO/1.morph.txt from firstEXO1.txt
  python xbook.py skel EXO 1      a skeleton data/EXO/1.json
"""
import collections
import glob
import io
import json
import os
import re
import sys
import unicodedata

sys.stdout.reconfigure(encoding="utf-8")
SP = os.path.dirname(os.path.abspath(__file__))
from _paths import ROOT, WORK, DECISIONS  # noqa: E402
NAME = {"GEN": "Genesis", "EXO": "Exodus", "LEV": "Leviticus", "NUM": "Numbers"}
PUNCT = re.compile(r"[.,;:·!?—()\u0417]")
NL = "\n"


def stem(book, ch):
    return "%s/%s%s" % (WORK, book.lower(), ch)


def rows(book, ch):
    return [l.rstrip(NL).split("\t") for l in io.open(stem(book, ch) + ".txt", encoding="utf-8") if l.strip()]


def table(path):
    out = {}
    if os.path.exists(path):
        for l in io.open(path, encoding="utf-8"):
            if l.strip():
                ref, words = l.rstrip(NL).split("\t")
                out[ref] = words.split()
    return out


def norm(form):
    d = unicodedata.normalize("NFD", form).replace("\u0300", "\u0301")
    return unicodedata.normalize("NFC", d).lower()


def brief(book, ch):
    sys.path.insert(0, ROOT + "/build")
    import validate as V
    rs = rows(book, ch)
    counts = [(r[0], len(V.PUNCT.sub("", r[2]).split())) for r in rs]
    total = sum(n for _, n in counts)
    text = "\n".join("%s %s" % (r[0], r[2]) for r in rs)
    b = io.open(ROOT + "/reference/second-pass-brief.md", encoding="utf-8").read()
    body = b.split("## The brief", 1)[1].split("\n---\n", 1)[1].strip("\n")
    out_path = "%s/second%s%s.txt" % (WORK, book, ch)
    body = (body.replace("<BOOK NAME>", NAME[book]).replace("<CHAPTER>", str(ch))
            .replace("<OUTPUT PATH>", out_path)
            .replace("<WORD COUNTS>", ", ".join("%s %d" % c for c in counts))
            .replace("<TOTAL>", str(total)).replace("<THE TEXT>", text))
    io.open("%s/brief%s%s.md" % (WORK, book, ch), "w", encoding="utf-8", newline=NL).write(body + NL)
    print(total, "words;", len(counts), "verses")


def seed(book, ch):
    seen = collections.defaultdict(collections.Counter)
    for path in glob.glob(ROOT + "/data/*/*.morph.txt"):
        for line in io.open(path, encoding="utf-8"):
            if line.startswith("#") or not line.strip():
                continue
            parts = line.split("#")[0].split()
            if len(parts) < 5:
                continue
            ref, pos, code, form, lemma = parts[:5]
            seen[norm(form)][(pos, code, lemma)] += 1
    out = []
    for ref, page, greek in rows(book, ch):
        for word in greek.split():
            form = PUNCT.sub("", word)
            if form:
                out.append((ref, form, seen.get(norm(form), {})))
    known = sum(1 for _, _, c in out if c)
    print("%d words; %d with a prior analysis, %d without" % (len(out), known, len(out) - known))
    s = stem(book, ch)
    with io.open(s + ".seed.txt", "w", encoding="utf-8", newline=NL) as f:
        for ref, form, cands in out:
            alts = " || ".join("%s %s %s x%d" % (p, c, l, n)
                               for (p, c, l), n in cands.most_common(4)) if cands else "-"
            f.write("%s\t%s\t%s%s" % (ref, form, alts, NL))
    with io.open(s + ".draft.txt", "w", encoding="utf-8", newline=NL) as f:
        for ref, form, cands in out:
            if cands:
                (p, c, l), n = cands.most_common(1)[0]
                flag = "   ## ALT" if len(cands) > 1 else ""
                f.write("%s %s %s %s %s%s%s" % (ref, p, c, form, l, flag, NL))
            else:
                f.write("%s ?? ???????? %s ??%s" % (ref, form, NL))


def first(book, ch):
    ns = {}
    exec(io.open("%s/fix%s%s.py" % (WORK, book, ch), encoding="utf-8").read(), ns)
    F = dict(ns["F"])
    out, count, unset = [], {}, []
    for line in io.open(stem(book, ch) + ".draft.txt", encoding="utf-8"):
        ref, pos, code, form, lemma = line.split()[:5]
        count[ref] = count.get(ref, 0) + 1
        key = "%s.%d" % (ref.split(":")[1], count[ref])
        if key in F:
            pos, code, lemma = F.pop(key).split()
        if "?" in pos + code + lemma:
            unset.append(key)
        out.append("%s %s %s %s %s" % (ref, pos, code, form, lemma))
    print("unset:", unset, "unused:", sorted(F))
    if not unset and not F:
        io.open("%s/first%s%s.txt" % (WORK, book, ch), "w", encoding="utf-8", newline=NL).write(NL.join(out) + NL)
        print("written", len(out))


def morph(book, ch):
    head = io.open(ROOT + "/data/GEN/50.morph.txt", encoding="utf-8").read().split(NL)[:28]
    head[0] = "# %s %s — morphology, one word per line." % (NAME[book], ch)
    body = io.open("%s/first%s%s.txt" % (WORK, book, ch), encoding="utf-8").read()
    os.makedirs("%s/data/%s" % (ROOT, book), exist_ok=True)
    io.open("%s/data/%s/%s.morph.txt" % (ROOT, book, ch), "w", encoding="utf-8", newline=NL).write(
        NL.join(head) + NL + body)
    print("written data/%s/%s.morph.txt" % (book, ch))


def page(p):
    return "Rahlfs 1935 (1950 printing), vol. I, %s %s" % ("pp." if "–" in p else "p.", p)


NT = {"JHN": "John"}


def nt_rows(book, ch):
    """A New Testament chapter's verses as SBLGNT prints them, signs and all: (verse, greek)."""
    out = []
    for line in io.open("%s/sources/sblgnt/text/%s.txt" % (ROOT, NT[book]), encoding="utf-8-sig"):
        if "\t" not in line:
            continue
        key, text = line.rstrip("\n").split("\t", 1)
        name, _, cv = key.rpartition(" ")
        if name == NT[book] and int(cv.split(":")[0]) == ch:
            out.append((cv, text.strip()))
    return out


def nt_speech(book, ch, rows_):
    """The capitals of direct speech in a New Testament chapter: a capital not opening a sentence
    whose MorphGNT dictionary form is lower case. A name's dictionary form is capitalised."""
    sys.path.insert(0, ROOT + "/build")
    import validate as V
    import words as W
    tokens = W.nt_tokens(book, ch) or {}
    out = {}
    for cv, greek in rows_:
        theirs = tokens.get(W.verse_key(cv), [])
        lemma_of = {W.nfc(form): lemma for form, lemma, *_ in theirs}
        said = [w for w in V.proper_names(greek) if lemma_of.get(W.nfc(w), "x")[:1].islower()]
        if said:
            out[cv] = said
    return out


def skeleton(book, ch):
    if book in NT:
        rows_ = nt_rows(book, ch)
        speech = nt_speech(book, ch, rows_)
        out = []
        for cv, greek in rows_:
            v = {"ref": "%s %s" % (book, cv), "greek": greek}
            if cv in speech:
                v["speech"] = speech[cv]
            out.append(v)
        return out
    speech = table(stem(book, ch) + ".speech")
    printed = table(stem(book, ch) + ".printed")
    out = []
    for ref, pg, greek in rows(book, ch):
        v = {"ref": "%s %s" % (book, ref), "greek": greek, "print": page(pg)}
        if ref in speech:
            v["speech"] = speech[ref]
        if ref in printed:
            v["printed"] = printed[ref]
        out.append(v)
    return out


def skel(book, ch):
    verses = [dict(v, hint="", notes=[], reading="", names=[]) for v in skeleton(book, ch)]
    os.makedirs("%s/data/%s" % (ROOT, book), exist_ok=True)
    io.open("%s/data/%s/%s.json" % (ROOT, book, ch), "w", encoding="utf-8", newline=NL).write(
        json.dumps(verses, ensure_ascii=False, indent=2) + NL)
    print(len(verses), "verses")


if __name__ == "__main__":
    cmd, book, ch = sys.argv[1], sys.argv[2], int(sys.argv[3])
    globals()[cmd](book, ch)
