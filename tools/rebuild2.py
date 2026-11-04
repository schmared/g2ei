# -*- coding: utf-8 -*-
"""Bring every chain to its card, keeping the items it has: python rebuild2.py [--write] [--only LEMMA ...]

An existing item that carries a card translation stays as written, its run's pieces now joined
with " / " where they had been joined with "and" (Q2); a translation split across items is joined
into one; a translation no item carries is rendered in the unit's form, by the template its
headword shows, and put in card order (Q24); a perfect's formula follows every item (Q17).

Writes rebuild2_report.txt: each changed chain, old and new, with `NEW` before each rendered item
and `KEPT?` before an existing item that matches no translation on the card."""
import collections
import io
import json
import os
import pickle
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")
SP = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SP)
from _paths import ROOT, WORK  # noqa: E402
import rebuild as R  # noqa: E402
V = R.V

ASPECT = R.ASPECT


def own_ands(sense):
    """The ` and `s a card translation holds in its own words: φόνος's `murder and manslaughter`."""
    return len(re.findall(r"\band\b", sense))


def convert(item, sense):
    """An existing item's joins for a run turned to the delimiter."""
    pieces = R.pieces_of(sense)
    if len(pieces) < 2:
        return item
    formula = ASPECT.search(item)
    body = ASPECT.sub("", item) if formula else item
    own = own_ands(sense)
    segments = body.split(" and ")
    if len(segments) - 1 <= own:
        return item
    # walk the segments against the pieces: a segment that begins a new piece is joined with " / "
    out = segments[0]
    budget = len(segments) - 1 - own            # the joins the form added, not the gloss's own
    for seg in segments[1:]:
        if budget > 0 and not re.match(r"^(?:it |standing )", seg):
            out += " / " + seg
            budget -= 1
        else:
            out += " and " + seg
    return out + (formula.group(0) if formula else "")


def sig(text):
    """What a translation or an item says: its content words, or where it has none — into, to, that —
    its words as they are."""
    body = ASPECT.sub("", text)
    c = V.content(body)
    if c:
        return c
    return {V.stem(w) for w in re.findall(r"[a-z']+", body.lower()) if w not in ("the", "a", "an")}


def best(items, used, want, fresh):
    """("whole", [o]) an unused item carrying `want`; ("run", [o…]) consecutive items that each carry
    a part of it and together all of it; ("part", [o]) the unused item carrying most of it; or None."""
    have = {o: sig(it) for o, it in enumerate(items)}
    fs = sig(fresh)
    whole = [(len(fs & have[o]) / max(1, len(fs | have[o])), -o)
             for o in have if o not in used and have[o] and want <= have[o]]
    if whole:
        return "whole", [-max(whole)[1]]
    for start in range(len(items)):
        acc, run = set(), []
        for o in range(start, len(items)):
            if o in used or not (have[o] & want) or not have[o] <= want | fs:
                break
            acc |= have[o]
            run.append(o)
            if want <= acc:
                if len(run) > 1:
                    return "run", run
                break
    part = [(len(have[o] & want), -o) for o in have if o not in used and have[o] & want
            and have[o] <= want | fs]
    if part:
        return "part", [-max(part)[1]]
    return None


def merge(items, run, sense):
    """Items that split one translation, joined: the form's opening said once."""
    parts = [convert(ASPECT.sub("", items[o]).rstrip(), sense) for o in run]
    formula = next((ASPECT.search(items[o]).group(0) for o in run if ASPECT.search(items[o])), "")
    head = V.leading_grammar(parts[0])
    joined = parts[0]
    for p in parts[1:]:
        words = p.split(" ")
        n = 0
        while n < len(head) and n < len(words) - 1 and words[n] == head[n]:
            n += 1
        joined += " / " + " ".join(words[n:])
    return joined + formula


def whole_entry(lemma, parse):
    """Every translation the entry gives, NOT_SENSES and FORM_SENSES not applied."""
    W = R.W
    key = W.entry_key(W.SPELLING.get(W.beta(lemma), W.beta(lemma)), parse)
    if key in R.E:
        return R.E[key]
    if lemma in W.LSJ_HOMOGRAPHS:
        return W.LSJ_HOMOGRAPHS[lemma][1]
    return W.LSJ.get(lemma, [])


FRESH = set()
STRICT = False


def fresh_chain(unit):
    """A chain rendered from the card alone, the headword's translation first: every form of the word
    then carries the same items, which one word, one range asks."""
    book, ch, vi, ui, ref, head, chain, field, form, code, parse, card = unit
    code = code.ljust(8, "-")
    pos = parse.split(" ·")[0]
    card = [c.rstrip(";").strip() for c in card]
    got = R.render_all(card, pos, head, field, code)
    if got is None:
        return None
    j, items, lead = got
    lead = next((l for l in V.MERGED_LEAD if chain.startswith(l)), "")
    formula = ""
    if code[1] in "XY":
        m = ASPECT.search(chain.split(", ")[0][len(lead):] if lead else chain.split(", ")[0])
        if m:
            formula = re.sub(r"^ and it stands \w+$", " and it stands so", m.group(0))
    out = []
    for i in [j] + [i for i in range(len(items)) if i != j]:
        if pos in ("verb", "noun", "adjective") and not V.content(card[i]):
            continue
        text = items[i]
        if formula and not ASPECT.search(text):
            text += formula
        if text not in out and sig(text):
            out.append(text)
    bare = ASPECT.sub("", re.sub(r"^in |^up to ", "", head) if lead else head)
    firsts = [n for n, t in enumerate(out) if ASPECT.sub("", t) == bare or ASPECT.sub("", t).startswith(bare + " / ")]
    if firsts and firsts[0] != 0:
        out.insert(0, out.pop(firsts[0]))
    elif not firsts:
        out.insert(0, head)
    return lead + ", ".join(out)


def rebuild(unit):
    book, ch, vi, ui, ref, head, chain, field, form, code, parse, card = unit
    if not card:
        return None, "no card", []
    lemma = V.lemmas(field)[-1]
    if any(chain.startswith(f) for f in V.FORMULA_CHAINS) or lemma in V.COVERAGE_FORMULAS:
        return None, "formula", []
    if parse.split(" ·")[0] in V.NOT_COVERED:
        return None, "pronoun", []
    code = code.ljust(8, "-")
    pos = parse.split(" ·")[0]
    card = [c.rstrip(";").strip() for c in card]
    got = R.render_all(card, pos, head, field, code)
    lead = ""
    for l in V.MERGED_LEAD:
        if chain.startswith(l):
            lead = l
    items = chain[len(lead):].split(", ")
    formula = ""
    if code[1] in "XY":
        m = ASPECT.search(items[0])
        if m:
            formula = re.sub(r"^ and it stands \w+$", " and it stands so", m.group(0))
            formula = re.sub(r"^ and remains \w+$", " and remains so", formula)
    if got is None:
        missing = V.missing_senses(chain, card)
        return None, "head", missing
    j, fresh, _ = got
    order = [j] + [i for i in range(len(card)) if i != j]
    used, out, notes = set(), [], []
    placed = {}                                   # card index -> position in out
    for i in order:
        want = sig(card[i])
        # a verb's, noun's or adjective's translation that is grammar alone — `has`, `one's`, `to be`,
        # pieces of examples — carries no sense of its own; a particle's or preposition's may be all grammar
        if not want or (pos in ("verb", "noun", "adjective") and not V.content(card[i])):
            continue
        exact = [o for o, it in enumerate(items) if o not in used and sig(it) == want]
        if fresh[i] in out or (STRICT and any(ASPECT.sub("", t) == fresh[i] for t in out)):
            continue                              # the same rendering the chain already holds
        covered = set().union(*[sig(t) for t in out]) if out else set()
        if want <= covered and not exact and not STRICT:
            continue                              # a repeat of what the chain already says
        found = None
        if i == j and 0 not in used:
            # the headword's translation begins at the head item: `went in, went into and entered`
            # is one translation, `to go in or into, enter`, split
            acc, run = set(), []
            for o in range(len(items)):
                have = sig(items[o])
                if o in used or not have <= want | sig(fresh[i]):
                    break
                acc |= have
                run.append(o)
                if want <= acc:
                    break
            if run and want <= acc:
                found = ("run" if len(run) > 1 else "whole", run)
        if not found and exact:
            found = ("whole", exact[:1])
        if not found:
            found = best(items, used, want, fresh[i])
        if found:
            kind, run = found
            # the items after it that are pieces of the same translation go with it
            others = [sig(c) for n, c in enumerate(card) if n != i]
            while (kind != "part" and len(R.pieces_of(card[i])) > 1 and run[-1] + 1 < len(items)
                   and run[-1] + 1 not in used):
                nxt = sig(items[run[-1] + 1])
                # a piece of this translation, and not another translation of the card said again
                if nxt and nxt <= sig(card[i]) | sig(fresh[i]) and nxt not in others:
                    run = run + [run[-1] + 1]
                    kind = "run"
                else:
                    break
            used.update(run)
            if kind == "whole":
                text = convert(items[run[0]], card[i])
            elif kind == "run":
                text = merge(items, run, card[i])
            else:
                text = fresh[i]
                if formula and not ASPECT.search(text):
                    text += formula
                notes.append("PART %s -> %s" % (items[run[0]], text))
                # the other items this rendering already says are pieces of it
                fs = sig(text)
                for o, it in enumerate(items):
                    if o not in used and sig(it) and sig(it) <= fs:
                        used.add(o)
            if text in out:
                continue
            out.append(text)
            placed[i] = run[0]
        else:
            text = fresh[i]
            if formula and not ASPECT.search(text):
                text += formula
            if text in out or not sig(text):
                continue
            out.append(text)
            notes.append(text)
    # existing items no card translation took: dropped where the chain says them already or they
    # render a translation set aside for this form; kept after the item before them otherwise
    covered = set().union(*[sig(t) for t in out]) if out else set()
    entry = whole_entry(lemma, parse)
    for o, it in enumerate(items):
        if o not in used and it.strip() and it not in out:
            if sig(it) <= covered or any(it == p.strip() for t in out for p in t.split(" / ")):
                continue
            filed = [t for t in entry if t not in card and sig(it) and sig(it) <= V.content(t)]
            if filed:
                notes.append("FILED %s (%s)" % (it, filed[0]))
                continue
            if STRICT:
                notes.append("DROPPED %s" % it)       # not a translation the card gives
                continue
            prev = [k for k in range(o) if k in used]
            at = len(out)
            if prev:
                prevtext = items[prev[-1]]
                at = next((n + 1 for n, t in enumerate(out) if t.startswith(ASPECT.sub("", prevtext).split(" and ")[0])), len(out))
            out.insert(at, it)
            notes.append("ORPHAN " + it)
    if formula:
        out = [t if ASPECT.search(t) else t + formula for t in out]
    # the headword's item first: the headword is the chain's first sense
    bare = ASPECT.sub("", re.sub(r"^in |^up to ", "", head) if lead else head)
    firsts = [n for n, t in enumerate(out) if ASPECT.sub("", t) == bare or ASPECT.sub("", t).startswith(bare + " / ")
              or ASPECT.sub("", t).startswith(bare + " or ")]
    if firsts and firsts[0] != 0:
        out.insert(0, out.pop(firsts[0]))
    return lead + ", ".join(out), None, notes


def main():
    write = "--write" in sys.argv
    only = set(a for a in sys.argv[sys.argv.index("--only") + 1:] if not a.startswith("--")) if "--only" in sys.argv else None
    units = pickle.load(open(os.path.join(WORK, "allunits.pkl"), "rb"))
    changes = collections.defaultdict(dict)
    skipped = collections.Counter()
    report = []
    failing = "--failing" in sys.argv
    global STRICT
    STRICT = "--strict" in sys.argv
    if "--fresh" in sys.argv:
        FRESH.update(a for a in sys.argv[sys.argv.index("--fresh") + 1:] if not a.startswith("--"))
    for u in units:
        lemma = V.lemmas(u[7])[-1]
        if only and lemma not in only:
            continue
        if failing:
            deg = bool({"comparative", "superlative"} & set(u[10].split(" · ")))
            if not u[11] or not V.missing_senses(u[6], u[11], deg):
                continue
        if lemma in FRESH:
            new = fresh_chain(u)
            why, notes = (None, []) if new else ("head", [])
        else:
            new, why, notes = rebuild(u)
        if why:
            if notes:
                skipped[why] += 1
                report.append("SKIP %s %s `%s`: %s | missing %s" % (u[4], lemma, u[5], why, notes))
            continue
        if new != u[6]:
            changes[(u[0], u[1], u[2])][u[3]] = new
            report.append("%s %s `%s`\n   - %s\n   + %s%s" % (u[4], lemma, u[5], u[6], new,
                          "".join("\n     NEW " + n if not n.startswith(("ORPHAN", "FILED", "PART")) else "\n     " + n for n in notes)))
    io.open(os.path.join(WORK, "rebuild2_report.txt"), "w", encoding="utf-8").write("\n".join(report) + "\n")
    print(sum(len(v) for v in changes.values()), "chains changed;", dict(skipped))
    if write:
        byfile = collections.defaultdict(dict)
        for (book, ch, vi), d in changes.items():
            byfile[(book, ch)][vi] = d
        for (book, ch), verses in byfile.items():
            path = "%s/data/%s/%d.json" % (R.ROOT, book, ch)
            data = json.load(io.open(path, encoding="utf-8"))
            for vi, d in verses.items():
                k = [-1]

                def fix(m, d=d):
                    k[0] += 1
                    if k[0] in d:
                        return "[[%s|%s|%s]]" % (m.group(1), d[k[0]], m.group(3))
                    return m.group(0)
                data[vi]["reading"] = V.UNIT.sub(fix, data[vi]["reading"])
            io.open(path, "w", encoding="utf-8", newline="\n").write(json.dumps(data, ensure_ascii=False, indent=2) + "\n")
        print("written")


if __name__ == "__main__":
    main()
