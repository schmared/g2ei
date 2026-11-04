# -*- coding: utf-8 -*-
"""A chapter's units read as their corpus siblings read: python tools/siblings.py JHN 1 [--write]

A sibling is a unit elsewhere in the corpus of the same word, part of speech, voice and number with the same
card — the units validate's range check holds to one count. Where a unit of the chapter gives fewer items
than its fullest sibling, it is rebuilt from the sibling's pattern: each of the sibling's items is matched to
the card translation it renders, and that translation is rendered in this unit's own form, in the sibling's
order. Writes WORK/siblings_report.txt; read it before writing."""
import collections
import io
import json
import os
import pickle
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")
from _paths import ROOT, WORK  # noqa: E402
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import rebuild as R  # noqa: E402
V = R.V

ASPECT = R.ASPECT


def body(item):
    return ASPECT.sub("", item).strip()


def items_of(chain):
    lead = next((l for l in V.MERGED_LEAD if chain.startswith(l)), "")
    return lead, chain[len(lead):].split(", ")


def key(u):
    book, ch, vi, ui, ref, head, chain, field, form, code, parse, card = u
    pos = parse.split(" ·")[0]
    c = (code or "").ljust(8, "-")
    number = "" if pos == "verb" else c[5]
    return (V.lemmas(field)[-1], pos, c[2] if pos == "verb" else "", number, tuple(card or ()))


def renderings(u):
    book, ch, vi, ui, ref, head, chain, field, form, code, parse, card = u
    got = R.render_all([c.rstrip(";").strip() for c in card], parse.split(" ·")[0], body(head), field,
                       (code or "").ljust(8, "-"))
    return got[1] if got else None


def main():
    book, ch = sys.argv[1], int(sys.argv[2])
    write = "--write" in sys.argv
    units = pickle.load(open(os.path.join(WORK, "allunits.pkl"), "rb"))
    groups = collections.defaultdict(list)
    for u in units:
        if u[11] and (u[0], u[1]) != (book, ch):
            groups[key(u)].append(u)
    report, changes = [], collections.defaultdict(dict)
    for u in units:
        if (u[0], u[1]) != (book, ch) or not u[11]:
            continue
        sibs = groups.get(key(u))
        if not sibs:
            continue
        lead, mine = items_of(u[6])
        best = max(sibs, key=lambda s: len(items_of(s[6])[1]))
        theirs = items_of(best[6])[1]
        if len(mine) >= len(theirs):
            continue
        rs, rm = renderings(best), renderings(u)
        if not rs or not rm:
            report.append("%s %s `%s`: no template" % (u[4], key(u)[0], u[5]))
            continue
        order, missed = [], []
        for it in theirs:
            j = next((n for n, r in enumerate(rs) if r == body(it) and n not in order), None)
            if j is None:
                j = next((n for n, r in enumerate(rs) if n not in order and r and
                          R2sig(r) == R2sig(body(it))), None)
            (order if j is not None else missed).append(j if j is not None else it)
        if missed:
            report.append("%s %s `%s`: sibling items no rendering matched: %s" % (u[4], key(u)[0], u[5], missed))
            continue
        formula = ASPECT.search(mine[0])
        f = formula.group(0) if formula else ""
        new = [rm[n] + f for n in order]
        # the headword's item first, as the sibling has its own first
        if not body(new[0]).startswith(body(u[5])):
            k = next((n for n, it in enumerate(new) if body(it).startswith(body(u[5]))), None)
            if k is not None:
                new.insert(0, new.pop(k))
        chain = lead + ", ".join(new)
        if chain != u[6]:
            changes[(u[0], u[1], u[2])][u[3]] = chain
            report.append("%s %s `%s` (from %s `%s`)\n   - %s\n   + %s" % (u[4], key(u)[0], u[5], best[4], best[5],
                                                                        u[6], chain))
    io.open(os.path.join(WORK, "siblings_report.txt"), "w", encoding="utf-8").write("\n".join(report) + "\n")
    print(sum(len(d) for d in changes.values()), "chains rebuilt from siblings;",
          sum(1 for r in report if "no rendering" in r or "no template" in r), "left for hand")
    if write:
        for (b, c, vi), d in changes.items():
            path = "%s/data/%s/%d.json" % (ROOT, b, c)
            data = json.load(io.open(path, encoding="utf-8"))
            k = [-1]

            def sub(m, d=d):
                k[0] += 1
                return "[[%s|%s|%s]]" % (m.group(1), d[k[0]], m.group(3)) if k[0] in d else m.group(0)
            data[vi]["reading"] = V.UNIT.sub(sub, data[vi]["reading"])
            io.open(path, "w", encoding="utf-8", newline="\n").write(json.dumps(data, ensure_ascii=False, indent=2) + "\n")
        print("written")


def R2sig(text):
    import rebuild2
    return rebuild2.sig(text)


if __name__ == "__main__":
    main()
