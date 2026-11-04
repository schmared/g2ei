# -*- coding: utf-8 -*-
"""Rebuild every chain from its card: python rebuild.py [--write] [--only LEMMA ...]

Each unit's chain becomes its card's translations in card order, each rendered in the unit's form
by the template its headword shows (prefix words, and the verb's form or the noun's case, article
and number); a run of one translation is one item, its pieces joined with " / " (Q2); a perfect's
formula follows every item (Q17). Units whose headword the template cannot find in the card's
first translation are left as they are and listed.

Writes rebuild_report.txt (every changed chain, old and new) and, with --write, the data files."""
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
from _paths import ROOT, WORK, DECISIONS  # noqa: E402
sys.path.insert(0, ROOT + "/build")
import words as W  # noqa: E402
import validate as V  # noqa: E402
from english import past, pp, ing, s3, plural, singular, comparative, IRREGULAR  # noqa: E402

E = W.load_middle_liddell()

# every English verb the lexicon gives as "to X"
VERBS = set(IRREGULAR)
FUNCTION = {"the", "a", "an", "one", "one's", "him", "her", "it", "them", "me", "us", "you", "be", "this", "that",
            "his", "their", "its", "my", "your", "our", "any", "all", "some", "no", "and", "or", "of", "in", "on"}
for senses in E.values():
    for g in senses:
        for piece in re.split(r",\s*|\s+or\s+", g):
            m = re.match(r"to ([a-z][a-z\-]*)\b", piece.strip())
            if m and m.group(1) not in FUNCTION:
                VERBS.add(m.group(1))
VERBS |= {"be"}
# LSJ glosses a verb without "to": νευροκοπέω "hamstring, hough"
for _lemma, _senses in W.LSJ.items():
    if _lemma.endswith(("ω", "ομαι", "μι")):
        for _g in _senses:
            for _piece in re.split(r",\s*|\s+or\s+", _g):
                _w = _piece.strip().split(" ")[0]
                if re.match(r"^[a-z][a-z\-]*$", _w) and _w not in FUNCTION:
                    VERBS.add(_w)

TRANSLIT = {"κάτοικος": "katoikos (κάτοικος)", "ῥαψῳδός": "rhapsode (ῥαψῳδός)", "ἀγορά": "agora (ἀγορά)",
            "ζέα": "zea (ζέα)", "ἄφετος": "aphetos (ἄφετος)", "ἐπίσκοπος": "episkopos (ἐπίσκοπος)",
            "βύσσος": "byssus (βύσσος)", "σιτομέτρης": "sitometres (σιτομέτρης)", "σπονδή": "spondē (σπονδή)",
            "εὐλαβής": "eulabes (εὐλαβής)", "λόγος": "logos (λόγος)", "γρῦ": "gry (γρῦ)",
            "χόανος": "choanos (χόανος)", "κλεψύδρα": "klepsydra (κλεψύδρα)", "στύραξ": "storax (στύραξ)"}

BE = {"am": "pres", "are": "pres", "is": "s3", "was": "past", "were": "past", "be": "base", "been": "pp",
      "being": "ing"}
PASSIVE_AUX = {"am", "is", "are", "was", "were", "be", "been", "being"}
PERFECT_AUX = {"has", "have", "had", "having"}
EN = "within, inside of, and by means of "
ANA = "up to, up along, and throughout "
PREP_WORDS = {"of", "from", "for", "by", "with", "to", "in", "on", "at", "about", "against", "into", "upon",
              "over", "under", "through", "towards", "toward", "before", "after"}
ASPECT = re.compile(r" and (?:it )?(?:stands?|standing|stood|remains?|remaining|continues?|continuing|holds?|"
                    r"holding)(?: \w+)?$")


def pieces_of(sense):
    """[(piece, joiner before it)] — joiner "," for a run, "or" for two the entry joins with or."""
    out, last = [], None
    for m in re.finditer(r",\s*|\s+or\s+", sense):
        pass
    sense = re.sub(r"!\s*(?=\S)", ", ", sense).rstrip("!")
    parts = re.split(r"(,\s*|:\s*|\s+or\s+)", sense)
    out = [(parts[0].strip(), None)]
    for i in range(1, len(parts), 2):
        joiner = "or" if parts[i].strip() == "or" else ","
        piece = parts[i + 1].strip()
        if piece.startswith("or "):            # ", or hinder": the entry's or after its comma
            piece, joiner = piece[3:], "or"
        if piece:
            out.append((piece, joiner))
    return out


def join(rendered, joiners):
    """Pieces joined with the delimiter; a bare preposition an "or" completes keeps its or (Q26)."""
    s = rendered[0]
    for piece, joiner, prev in zip(rendered[1:], joiners[1:], rendered):
        if joiner == "or" and (prev in PREP_WORDS or piece in PREP_WORDS):
            s += " or " + piece
        else:
            s += " / " + piece
    return s


LATIN_PIECES = ("videor mihi", "videor", "anima", "ulna", "agere", "pinus picea", "alius", "tamen, vero",
                "uti familiariter", "in rationes referre", "priusquam", "summum bonum", "placuit senatui")


def tidy(text):
    """A translation's markup debris: an unmatched bracket, a `; also` the next sense begins with."""
    text = re.sub(r";\s*also$", "", text.strip())
    text = re.sub(r"\s*\.\s*\.\s*$", "", text)
    # Latin inside a translation whose English is a sense: δοκέω's "videor mihi, to think", ἐπεί's
    # "after (postquam)", πῆχυς's "ulna, a cubit"; and a space the encoding lost, "theHoly"
    text = re.sub(r"\s*\((?:postquam|quum|cum|ut|ne)\)", "", text)
    for latin in LATIN_PIECES:
        text = re.sub(r"(?:^|(?<=, ))%s(?:, |$)" % re.escape(latin), "", text)
    text = text.replace("theHoly", "the Holy").strip(" ,")
    if text.count(")") > text.count("("):
        text = text.replace(")", "")
    if text.count("(") > text.count(")"):
        text = text.replace("(", "")
    return text.strip()


def translit(text):
    text = tidy(text)
    for g, t in TRANSLIT.items():
        text = re.sub(r"(?<![\w(])%s(?![\w)])" % re.escape(g), t, text)
    return text


# ---------------------------------------------------------------- verbs

def verb_template(head, gloss, code="--------"):
    """(prefix words, class, be-word) from a headword and the card's first translation."""
    first = pieces_of(gloss)[0][0]
    words = re.sub(r"^to ", "", first).split(" ")
    v = words[0]
    hw = head.split(" ")
    if v == "be":
        rest = words[1:]
        cands = [i for i, w in enumerate(hw) if w in BE]
        for i in reversed(cands):
            if not rest or hw[i + 1:i + 1 + len(rest)] == rest:
                return hw[:i], BE[hw[i]]
        if cands:
            return hw[:cands[0]], BE[hw[cands[0]]]
    for i, w in enumerate(hw):
        if v == "be":
            continue
        prefix = hw[:i]
        if w == ing(v):
            return prefix, "ing"
        if w == s3(v) and w != v:
            return prefix, "s3"
        if w in (past(v), pp(v)) and w != v:
            if w == pp(v) and (set(prefix) & (PASSIVE_AUX | PERFECT_AUX) or w != past(v)):
                return prefix, "pp"
            return prefix, "past"
        if w == v:
            # set, put, cut: the form cannot say which; the parse and the auxiliaries can
            if w == past(v):
                if set(prefix) & (PASSIVE_AUX | PERFECT_AUX):
                    return prefix, "pp"
                if code[1] in "AY" and code[3] == "I" and not prefix:
                    return prefix, "past"
                if code[1] == "A" and code[3] == "I" and prefix and prefix[-1] in PRONOUNS:
                    return prefix, "past"
            return prefix, "base"
    return None


def be_form(cls, code):
    person, number = code[0], code[5]
    if cls == "past":
        return "were" if number == "P" or person == "2" else "was"
    if cls == "s3":
        return "is"
    if cls == "pres":
        return "am" if person == "1" and number == "S" else "are"
    return {"base": "be", "pp": "been", "ing": "being"}[cls]


REFLEXIVE = {("1", "S"): ("myself", "my"), ("2", "S"): ("yourself", "your"), ("1", "P"): ("ourselves", "our"),
             ("2", "P"): ("yourselves", "your"), ("3", "P"): ("themselves", "their")}


PAST_OF = {}
for _base, (_past, _pp) in IRREGULAR.items():
    PAST_OF.setdefault(_past, _base)
    PAST_OF.setdefault(_pp, _base)


def base_of(word):
    """A verb the lexicon gives inflected, back to its base: goes → go, rose → rise, overlooked → overlook."""
    if word in VERBS:
        return word
    if word in PAST_OF:
        return PAST_OF[word]
    for cut, add in (("ies", "y"), ("es", ""), ("s", ""), ("ied", "y"), ("ed", "e"), ("ed", ""),
                     ("ing", "e"), ("ing", "")):
        if word.endswith(cut) and word[:-len(cut)] + add in VERBS:
            return word[:-len(cut)] + add
    return word


PRONOUNS = {"I", "you", "we", "they", "he", "she", "it"}


def verb_piece(piece, cls, code, passive, first, prefix=()):
    p = piece.strip()
    body = p[3:] if p.startswith("to ") else p
    ws = body.split(" ")
    v = ws[0] if p.startswith("to ") else base_of(ws[0])
    if not (p.startswith("to ") or v in VERBS):
        return p
    if passive and (v == "be" or ws[0] in ("is", "are", "was", "were")) and len(ws) > 1:
        return " ".join(ws[1:])
    if v == "be":
        w = be_form(cls, code)
        if cls in ("base", "pres") and prefix and prefix[-1] in PRONOUNS:
            w = "am" if prefix[-1] == "I" else "are" if prefix[-1] in ("you", "we", "they") else "is"
    else:
        if cls in ("base", "pres"):
            w = v
        else:
            w = {"past": past, "pp": pp, "ing": ing, "s3": s3}[cls](v)
    rest = ws[1:]
    # a piece that is two verbs of its own, "to stand forth and come to": the second in the form too
    for n in range(len(rest) - 1):
        if rest[n] == "and" and rest[n + 1] in VERBS and rest[n + 1] not in FUNCTION:
            nxt = rest[n + 1]
            if nxt == "be":
                rest[n + 1] = be_form(cls, code)
            elif cls not in ("base", "pres"):
                rest[n + 1] = {"past": past, "pp": pp, "ing": ing, "s3": s3}[cls](nxt)
    out = " ".join([w] + rest)
    key = (code[0], code[5])
    if key in REFLEXIVE and code[3] != "P":
        self_, poss = REFLEXIVE[key]
        out = re.sub(r"\boneself\b", self_, out)
        out = re.sub(r"\bone's\b", poss, out) if code[2] in "ME" else out
    return out


def verb_item(sense, tpl, code):
    prefix, cls = tpl
    passive = cls == "pp" and bool(set(prefix) & PASSIVE_AUX)
    rendered, joiners = [], []
    pieces = pieces_of(sense)
    for i, (piece, joiner) in enumerate(pieces):
        is_verb_piece = piece.startswith("to ") or base_of(piece.split(" ")[0]) in VERBS
        # a piece the entry joins with "or" completes the one before it, "to speak to the point or
        # purpose": it is a verb only where the one before it is a verb alone, "to go or come out of"
        # the pieces of a run after a verb are verbs too, "to catch, find out, detect"
        if i > 0 and joiner == "," and pieces[0][0].startswith("to ") and not is_verb_piece:
            w0 = piece.split(" ")[0]
            is_verb_piece = (re.match(r"^[a-z]+$", w0) is not None and w0 not in FUNCTION
                             and not w0.endswith("ly") and w0 not in PREP_WORDS)
            if is_verb_piece:
                VERBS.add(w0)
        if i > 0 and joiner == "or" and not piece.startswith("to "):
            is_verb_piece = is_verb_piece and len(re.sub(r"^to ", "", pieces[i - 1][0]).split(" ")) == 1
        if i > 0 and not is_verb_piece:
            rendered.append(piece)
        else:
            rendered.append(verb_piece(piece, cls, code, passive, i, prefix))
        joiners.append(joiner)
    s = join(rendered, joiners)
    return (" ".join(prefix) + " " + s).strip()


# ---------------------------------------------------------------- nouns and the rest

def nominal_item(sense, art, marker, plural_noun, degree="", single=False):
    rendered, joiners = [], []
    for piece, joiner in pieces_of(sense):
        q = piece
        if art or plural_noun:
            q = re.sub(r"^(?:a|an|the|any) ", "", q)
        if plural_noun and not (joiner == "or" and len(q.split(" ")) == 1 and rendered
                                and rendered[-1] == plural(rendered[-1])):
            q = plural(q)
        elif single:
            q = singular(q)
        if degree in ("C", "S"):
            ws = q.split(" ")
            ws[0] = comparative(ws[0], degree) if len(ws) == 1 or ws[1] in ("to", "of", "in", "for") else ws[0]
            q = " ".join(ws) if len(ws) > 1 else ws[0]
        rendered.append(q)
        joiners.append(joiner)
    s = join(rendered, joiners)
    if art and not s.startswith("the "):
        s = "the " + s
    return marker + s


def nominal_template(head, field, code):
    lead = ""
    h = head
    if field.startswith("ἐν;"):
        lead, h = EN, re.sub(r"^in ", "", head)
    elif field.startswith("ἀνά"):
        lead, h = ANA, re.sub(r"^up to ", "", head)
    marker = ""
    if not lead:
        m = re.match(r"^(of |to )", h)
        if m and code[4] in "GD":
            marker, h = m.group(1), h[len(m.group(1)):]
    art = h.startswith("the ")
    return lead, marker, art


def heads_it(first, want, relaxed):
    """Whether a rendered first item is the headword's: the same, or the headword and more of its run."""
    if first == want or first.startswith(want + " / ") or first.startswith(want + " or "):
        return True
    if not relaxed:
        return False
    a, b = first.split(" "), want.split(" ")
    return a[:1] == b[:1] and V.content(want) <= V.content(first)


def render_all(card, pos, head, field, code):
    """Every card translation rendered in the unit's form, the headword's first, or None."""
    card = [c.rstrip(";").strip() for c in card]
    if pos == "verb":
        bare_head = ASPECT.sub("", head)
        for relaxed in (False, True):
            for j, anchor in enumerate(card):
                tpl = verb_template(bare_head, anchor, code)
                if tpl is None:
                    continue
                first = verb_item(translit(anchor), tpl, code)
                if heads_it(first, bare_head, relaxed):
                    return j, [verb_item(translit(sense), tpl, code) for sense in card], ""
        return None
    lead, marker, art = nominal_template(head, field, code)
    want = re.sub(r"^in |^up to ", "", head) if lead else head
    degree = code[7] if code[7] in "CS" and pos == "adjective" else ""
    noun = pos == "noun" and code[5] == "P"
    for strip, relaxed, single in ((False, False, False), (True, False, False), (True, False, True),
                                   (False, True, False), (True, True, False), (True, True, True)):
        if single and (code[5] != "S" or pos != "noun"):
            continue
        for j, anchor in enumerate(card):
            items = []
            for i, sense in enumerate(card):
                item = nominal_item(translit(sense), art, "" if lead else marker, noun, degree, single)
                if strip and i == j and not art:
                    item = (marker if not lead else "") + re.sub(r"^(?:a|an|the|any) ", "", item[len(marker) if not lead else 0:])
                items.append(item)
            if heads_it(items[j], want, relaxed):
                return j, items, lead
    return None


def rebuild(unit):
    book, ch, vi, ui, ref, head, chain, field, form, code, parse, card = unit
    if not card:
        return None, "no card"
    if any(chain.startswith(f) for f in V.FORMULA_CHAINS) or V.lemmas(field)[-1] in V.COVERAGE_FORMULAS:
        return None, "formula"
    if parse.split(" ·")[0] in V.NOT_COVERED:
        return None, "pronoun"
    code = code.ljust(8, "-")
    pos = parse.split(" ·")[0]
    formula = ""
    if code[1] in "XY":
        m = ASPECT.search(chain.split(", ")[0])
        if m:
            formula = m.group(0)
            formula = re.sub(r"^ and it stands \w+$", " and it stands so", formula)
            formula = re.sub(r"^ and remains \w+$", " and remains so", formula)
    got = render_all(card, pos, head, field, code)
    if got is None:
        return None, "head"
    j, items, lead = got
    order = [items[j]] + [it for i, it in enumerate(items) if i != j]
    seen, out = set(), []
    for item in order:
        if formula and not ASPECT.search(item):
            item += formula
        if item not in seen:
            seen.add(item)
            out.append(item)
    return (lead or "") + ", ".join(out), None


def main():
    write = "--write" in sys.argv
    only = set(sys.argv[sys.argv.index("--only") + 1:]) if "--only" in sys.argv else None
    units = pickle.load(open(os.path.join(WORK, "allunits.pkl"), "rb"))
    changes = collections.defaultdict(dict)       # (book, ch, vi) -> {ui: new chain}
    skipped = collections.Counter()
    report = []
    for u in units:
        lemma = V.lemmas(u[7])[-1]
        if only and lemma not in only:
            continue
        new, why = rebuild(u)
        if why:
            missing = V.missing_senses(u[6], u[11] or [])
            if missing:
                skipped[why.split(" ")[0]] += 1
                report.append("SKIP %s %s `%s`: %s | missing %s" % (u[4], lemma, u[5], why, missing))
            continue
        if new != u[6]:
            changes[(u[0], u[1], u[2])][u[3]] = new
            report.append("%s %s `%s`\n   - %s\n   + %s" % (u[4], lemma, u[5], u[6], new))
    io.open(os.path.join(WORK, "rebuild_report.txt"), "w", encoding="utf-8").write("\n".join(report) + "\n")
    print(sum(len(v) for v in changes.values()), "chains changed;", dict(skipped))
    if write:
        byfile = collections.defaultdict(dict)
        for (book, ch, vi), d in changes.items():
            byfile[(book, ch)][vi] = d
        for (book, ch), verses in byfile.items():
            path = "%s/data/%s/%d.json" % (ROOT, book, ch)
            data = json.load(io.open(path, encoding="utf-8"))
            for vi, d in verses.items():
                k = [-1]

                def fix(m):
                    k[0] += 1
                    if k[0] in d:
                        return "[[%s|%s|%s]]" % (m.group(1), d[k[0]], m.group(3))
                    return m.group(0)
                data[vi]["reading"] = V.UNIT.sub(fix, data[vi]["reading"])
            io.open(path, "w", encoding="utf-8", newline="\n").write(json.dumps(data, ensure_ascii=False, indent=2) + "\n")
        print("written")


if __name__ == "__main__":
    main()
