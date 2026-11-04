# -*- coding: utf-8 -*-
"""Q32–Q35 repairs to the chains: python fix35.py [--write]  ->  fix35_report.txt

1. hand repairs (HAND), by lemma and item;
2. renderer debris fixed in place (anythings, lie hold on, …);
3. an item no translation on the card gives is dropped (Q32; and what the Q33/Q35 verdicts set aside);
4. a voice's own sense — one the form's card has and the active card lacks — is printed in its own
   voice, as the lexicon gives it, not passivized again (Q35): `was fallen asleep` → `fell asleep`;
5. a translation led by an example's person or auxiliary — `I fear`, `were aware of` — is rendered in
   the form, its verb in the form's person and tense (Q35);
6. a translation the chain now lacks is rendered and put in card order;
7. a perfect's formula after every item; the headword's item first."""
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
import rebuild2 as R2  # noqa: E402
V, W = R.V, R.W

R.VERBS.update({"hand", "imply", "ween"})
R.VERBS.discard("more")
R.VERBS.discard("not")

ASPECT = R.ASPECT
PASSIVE_PREFIX = {"was", "were", "am", "is", "are", "be", "been", "being"}

# hand repairs: (lemma, item without its formula) -> replacement, or None to drop
HAND = {
    ("οὖν", "be he who he may"): None,
    ("δή", "be they who they may"): None,
    ("φυλάσσω", "having been withed caution"): "with caution",
    ("ἀνασώζω", "of the ones having been recovered what is lost / rescued"): "of the ones having been recovered / rescued",
    ("μισθόω", "I have had let out for hire / farmed out / let"): "I have been let out for hire / farmed out / let",
    ("μισθόω", "I have had contracted"): "I have contracted",
    ("φυράω", "having been into dough / kneaded"): "having been made into dough / kneaded",
    ("κρίνω", "were being passed sentence upon / condemned"): "were having sentence passed upon them / being condemned",
    ("ἀπάγω", "the ones having been returned what one owes / rendered / paid"):
        "the ones having had what one owes returned / rendered / paid",
    ("πρόκειμαι", "the one the corpse laid out"): "the corpse laid out",
    ("προσφέρω", "the things being meat / drunk / food"): "the meat / drink / food",
    ("προσφέρω", "the things being dealt with / behad oneself"): "the things being dealt with",
    ("βέλτιστος", "the most aristocracy"): "the aristocracy",
    ("πονηρεύομαι", "to have been evil / acted wickedly / played the rogue / to stand so"):
        "to have been evil / acted wickedly / played the rogue",
    ("ἐμβάλλω", "struck a ship with the ram / charged it"): "struck with the ram / charged / rammed",
    ("ἐμβάλλω", "strike a ship with the ram / charge it"): "strike with the ram / charge / ram",
    ("ἐμβάλλω", "you will strike a ship with the ram / charge it"): "you will strike with the ram / charge / ram",
}
# debris the renderer left, mended wherever it stands
DEBRIS = [
    (re.compile(r"\banythings\b"), "things"),
    (re.compile(r"\blie hold on\b"), "lay hold on"),
    (re.compile(r"\blie to rest\b"), "lay to rest"),
    (re.compile(r"\bbehad oneself\b"), "behaved oneself"),
    (re.compile(r"\bmored\b"), "more"),
    (re.compile(r"\bhand over to\b(?<=being given up / hand over to)"), "handed over to"),
    (re.compile(r"(?<=being given up / )hand over to\b"), "handed over to"),
    (re.compile(r"(?<=being involved / )imply\b"), "implied"),
]
SKIP_AUTO = {"μισθόω"}       # a headword the template cannot read: hand repairs only


def strip_formula(item):
    m = ASPECT.search(item)
    return (ASPECT.sub("", item), m.group(0) if m else "")


PERSON = r"(?:I|we|you|thou|he|she|they|it)"


def normalize_piece(p):
    """A piece an example gives in its own person or tense, as the lexicon's infinitive: `I fear` →
    `to fear`, `were aware of` → `to be aware of`, `it has been accomplished` → `to be accomplished`."""
    p = p.strip()
    m = re.match(r"^(?:%s )?(?:has|have|had|hath) been (.+)$" % PERSON, p)
    if m:
        return "to be " + m.group(1)
    m = re.match(r"^(?:%s )?(?:is|are|was|were|am|art) (.+)$" % PERSON, p)
    if m:
        return "to be " + m.group(1)
    m = re.match(r"^(?:%s )?(?:will|shall|wilt|shalt) (.+)$" % PERSON, p)
    if m:
        return "to " + m.group(1)
    m = re.match(r"^%s (\w+)(.*)$" % PERSON, p)
    if m:
        base = R.PAST_OF.get(m.group(1)) or R.base_of(m.group(1))
        if base in R.VERBS:
            return "to " + base + m.group(2)
    return p


LED = re.compile(r"^(?:%s |(?:is|are|was|were|am|will|shall|wilt|shalt|has|have|had) )" % PERSON)


def normalize(sense):
    parts = re.split(r"(,\s*|\s+or\s+)", sense)
    out = [normalize_piece(x) if i % 2 == 0 else x for i, x in enumerate(parts)]
    # `is displaced, disordered`: the pieces after a passive's first are participles of it, not verbs
    if out and out[0].startswith("to be ") and not parts[0].strip().startswith(("to ", "be ")):
        out = [x if i % 2 or i == 0 or x.startswith(("to ", "be ")) else "be " + x.strip() for i, x in enumerate(out)]
    return "".join(out)


def person_led(sense):
    return any(LED.match(x.strip()) for x in re.split(r",\s*|\s+or\s+", sense)[:1])


def verb_gloss(sense):
    """Whether a translation is a verb's — `to fall asleep`, `grew taller` — and not a participle's or an
    adjective's, `born`, `shewn to be`, `blindfold`, which the passive form carries as they stand."""
    first = re.split(r",\s*|\s+or\s+", sense)[0].strip()
    if first.startswith("to ") and not first.startswith("to be "):
        return True
    w = first.split(" ")[0]
    base = R.base_of(w)
    if base == w or base not in R.VERBS:
        return False
    return w == R.past(base) != R.pp(base) or w == R.s3(base)


def is_own(sense, act, code):
    """A sense of the form's voice alone — the passive's or the middle's English, as printed."""
    return (code[2] in "PE" and sense not in act and not re.match(r"^(?:to )?be ", sense)
            and verb_gloss(sense))


def template(head, card, code):
    bare = ASPECT.sub("", head)
    for relaxed in (False, True):
        for anchor in card:
            tpl = R.verb_template(bare, anchor, code)
            if tpl is None:
                continue
            if R.heads_it(R.verb_item(R.translit(anchor), tpl, code), bare, relaxed):
                return tpl
    return None


def active(tpl):
    """The template of a passive headword, made the active of the same tense and person."""
    prefix, cls = tpl
    prefix = list(prefix)
    if cls != "pp" or not prefix or not set(prefix) & PASSIVE_PREFIX:
        return tpl
    last = prefix[-1]
    if last == "been":
        return prefix[:-1], "pp"
    if last == "being":
        return prefix[:-1], "ing"
    if last == "be":
        return prefix[:-1], "base"
    if last in ("was", "were"):
        return prefix[:-1], "past"
    if last in ("am", "are"):
        return prefix[:-1], "base"
    if last == "is":
        return prefix[:-1], "s3"
    return tpl


def matches(item, sense, rendered):
    """Whether an existing item renders this translation: it says the translation and nothing else."""
    s, r, it = R2.sig(sense), R2.sig(rendered), R2.sig(strip_formula(item)[0])
    return bool(s) and s <= it <= s | r


def active_card(u):
    book, ch, vi, ui, ref, head, chain, field, form, code, parse, card = u
    lemma = V.lemmas(field)[-1]
    c = code.ljust(8, "-")
    a = c[:2] + "A" + c[3:]
    out = W.lexicon_senses(R.E, lemma, a, form, parse)
    if out is None or lemma in W.LSJ_HOMOGRAPHS:
        out = W.lsj_senses(lemma, a, form)
    return out or []


def fix(u, notes):
    book, ch, vi, ui, ref, head, chain, field, form, code, parse, card = u
    lemma = V.lemmas(field)[-1]
    if not card or lemma in V.COVERAGE_FORMULAS or parse.split(" ·")[0] in V.NOT_COVERED \
            or chain.startswith(V.FORMULA_CHAINS):
        return chain
    code = code.ljust(8, "-")
    pos = parse.split(" ·")[0]
    card = [c.rstrip(";").strip() for c in card]
    lead = next((l for l in V.MERGED_LEAD if chain.startswith(l)), "")
    items = chain[len(lead):].split(", ")
    formula = ""
    if code[1] in "XY":
        m = ASPECT.search(items[0])
        if m:
            formula = re.sub(r"^ and it stands \w+$", " and it stands so", m.group(0))
    # 1, 2: hand repairs and debris
    out = []
    for n, it in enumerate(items):
        body, f = strip_formula(it)
        if (lemma, body) in HAND:
            new = HAND[(lemma, body)]
            notes.append("HAND %s -> %s" % (it, new))
            if new is None:
                continue
            it = new + f
        for pat, rep in DEBRIS:
            if pat.search(it):
                new = pat.sub(rep, it)
                notes.append("DEBRIS %s -> %s" % (it, new))
                it = new
        out.append(it)
    items = out
    for n, it in enumerate(items):
        for sense in card:
            if V.joined_with_and(it, sense) and R2.sig(sense) and R2.sig(sense) <= R2.sig(it) <= R2.sig(sense) | {"one"}:
                new = R2.convert(it, sense)
                if new != it:
                    notes.append("DELIM %s -> %s" % (it, new))
                    items[n] = it = new
    degree = bool({"comparative", "superlative"} & set(parse.split(" · ")))
    # 3: items no translation on the card gives
    bad = {item for item, _ in V.unsupported(lead + ", ".join(items), card, degree, pos == "adverb", lemma)}
    kept = []
    for n, it in enumerate(items):
        if it in bad and n > 0:
            notes.append("DROP %s" % it)
            continue
        if it in bad:
            notes.append("HEAD UNSUPPORTED %s" % it)
        kept.append(it)
    items = kept
    if lemma in SKIP_AUTO or pos != "verb":
        tpl = None
    else:
        tpl = template(head, card, code)
    # 4, 5: a voice's own senses, and senses led by an example's person, rendered in the form. Only the
    # item the rebuild wrote from the sense is replaced — that rendering, exactly, or one no form can wear
    if tpl is not None:
        act = set(active_card(u)) if code[2] in "PE" else set(card)
        for s in card:
            own, led = is_own(s, act, code), person_led(s)
            if not (own or led) or not V.content(s):
                continue
            good = R.verb_item(R.translit(normalize(s)), active(tpl) if (own or led) else tpl, code)
            bad = R.verb_item(R.translit(s), tpl, code)
            for n, it in enumerate(items):
                body, f = strip_formula(it)
                if n == 0 or body == good:
                    continue
                if body == bad or (V.english_faults(it) and matches(it, s, good)):
                    notes.append("VOICE %s -> %s  [%s]" % (it, good, s))
                    items[n] = good + f
                    break
    # 6: translations the chain lacks
    if tpl is not None or pos != "verb":
        missing = V.missing_senses(lead + ", ".join(items), card, degree, pos == "adverb")
        for s in missing:
            if pos == "verb":
                act = set(active_card(u)) if code[2] in "PE" else set(card)
                t = active(tpl) if (is_own(s, act, code) or person_led(s)) else tpl
                text = R.verb_item(R.translit(normalize(s)), t, code)
            else:
                got = R.render_all(card, pos, head, field, code)
                if got is None:
                    notes.append("MISSING (no template) %s" % s)
                    continue
                text = got[1][card.index(s)]
            if text in items:
                continue
            # card order: after the last item that renders an earlier translation
            at = len(items)
            idx = card.index(s)
            for n in range(len(items) - 1, 0, -1):
                k = next((i for i, c in enumerate(card) if R2.sig(c) and R2.sig(c) <= R2.sig(strip_formula(items[n])[0])), None)
                if k is not None and k < idx:
                    at = n + 1
                    break
            items.insert(at, text + formula)
            notes.append("ADD %s  [%s]" % (text, s))
    elif V.missing_senses(lead + ", ".join(items), card, degree, pos == "adverb"):
        notes.append("MISSING (no template) %s" % V.missing_senses(lead + ", ".join(items), card, degree))
    # 7: the formula after every item; no item twice
    if formula:
        items = [it if ASPECT.search(it) else it + formula for it in items]
    seen, final = set(), []
    for it in items:
        if it not in seen:
            seen.add(it)
            final.append(it)
    return lead + ", ".join(final)


def main():
    write = "--write" in sys.argv
    units = pickle.load(open(os.path.join(WORK, "allunits.pkl"), "rb"))
    changes = collections.defaultdict(dict)
    report = []
    kinds = collections.Counter()
    for u in units:
        notes = []
        new = fix(u, notes)
        for nte in notes:
            kinds[nte.split(" ")[0]] += 1
        if new != u[6]:
            changes[(u[0], u[1], u[2])][u[3]] = new
            report.append("%s %s `%s`\n   - %s\n   + %s\n     %s" % (u[4], V.lemmas(u[7])[-1], u[5], u[6], new,
                                                             "\n     ".join(notes)))
        elif notes:
            report.append("%s %s `%s` (unchanged)\n     %s" % (u[4], V.lemmas(u[7])[-1], u[5], "\n     ".join(notes)))
    io.open(os.path.join(WORK, "fix35_report.txt"), "w", encoding="utf-8").write("\n".join(report) + "\n")
    print(sum(len(v) for v in changes.values()), "chains changed;", dict(kinds))
    if write:
        byfile = collections.defaultdict(dict)
        for (book, ch, vi), d in changes.items():
            byfile[(book, ch)][vi] = d
        for (book, ch), verses in byfile.items():
            path = "%s/data/%s/%d.json" % (R.ROOT, book, ch)
            data = json.load(io.open(path, encoding="utf-8"))
            for vi, d in verses.items():
                k = [-1]

                def sub(m, d=d):
                    k[0] += 1
                    if k[0] in d:
                        return "[[%s|%s|%s]]" % (m.group(1), d[k[0]], m.group(3))
                    return m.group(0)
                data[vi]["reading"] = V.UNIT.sub(sub, data[vi]["reading"])
            io.open(path, "w", encoding="utf-8", newline="\n").write(json.dumps(data, ensure_ascii=False, indent=2) + "\n")
        print("written")


if __name__ == "__main__":
    main()
