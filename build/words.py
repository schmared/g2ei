#!/usr/bin/env python3
"""sources/  ->  data/<BOOK>/<chapter>.words.json — the word-by-word layer.

For every word of every verse in data/<BOOK>/<chapter>.json this records:

    form     the word as the verse prints it
    lemma    its dictionary form — what a concordance or lexicon files it under
    parse    what the form itself says: part of speech, tense, voice, mood,
             person, number, case, gender
    aspect   for verbs, what the tense means where English cannot show it, in the
             project's fixed wording (CLAUDE.md)
    senses   the opening senses of the lemma's Middle Liddell entry, in the
             lexicon's own order and with no regard to context

A concordance stops at the lemma. This layer takes the step after it: the lemma's
whole range, *and* what this particular form adds to it.

Where the lemma and parse come from:

    LXX books   data/<BOOK>/<chapter>.morph.txt — the project's own analysis. The CCAT
                tagging in sources/ may not be redistributed, so it is used only by
                validate.py, as a local check on that analysis.
    NT books    sources/morphgnt/ — MorphGNT, CC BY-SA.

Senses come from Middle Liddell (1889) in the Perseus Digital Library's XML (CC BY-SA
3.0 US) — only the translations inside an entry's numbered senses, never its etymology;
for the few lemmas it lacks, from LSJ as published by PerseusDL (CC BY-SA 4.0).

sources/ is not committed (NOTICE.md), so this writes a file that is, and
build/render.py reads that file — the site builds without sources/.

    python build/words.py                  # every chapter on the page
    python build/words.py GEN/1            # named chapters only
"""
import argparse
import json
import pathlib
import re
import sys
import unicodedata

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import render  # noqa: E402  — for ROOT, DATA, PAGE, BOOKS

SOURCES = render.ROOT / "sources"
MIDDLE_LIDDELL = SOURCES / "middle-liddell/Perseus_text_1999.04.0058.xml"

# Lemmas Middle Liddell lacks, with LSJ's senses in LSJ's order — from LSJ as
# published by PerseusDL/lexica, CC BY-SA 4.0. Add an entry when words.py reports
# a lemma with no senses.
LSJ = {
    "ἀκατασκεύαστος": ["not properly prepared", "unwrought, unformed", "chaos",
                        "unpolished, unartificial"],
}

# New Testament books: MorphGNT file and its book number.
MORPHGNT = SOURCES / "morphgnt"
NT = {"JHN": ("64-Jn-morphgnt.txt", "04")}

SHOWN = 5  # senses shown per word; the rest are counted, not dropped silently

_SENSES_NOTE = ("Senses: Middle Liddell (1889; Perseus Digital Library, CC BY-SA 3.0 US), in "
                "the lexicon's own order, without regard to context; LSJ (PerseusDL, "
                "CC BY-SA 4.0) where Middle Liddell has no "
                "entry. Middle/passive marks a tense in which the two voices share one "
                "form; masculine/feminine, an adjective whose form does not distinguish them.")
SOURCE_NOTE = {
    "lxx": "Dictionary form and parse: this project's own analysis, checked against the "
           "CCAT analysis of Rahlfs. " + _SENSES_NOTE,
    "nt": "Dictionary form and parse: MorphGNT's analysis of the SBLGNT. " + _SENSES_NOTE,
}

# Perseus marks a few Latin equivalents, scraps of longer glosses, and glosses for a
# single construction as translations too. They are skipped by name, so the rule stays
# mechanical everywhere else. (Etymology needs no entry: it stands outside the senses.)
# Skim a new chapter's cards and add to this; keep it short.
NOT_SENSES = {
    "a)/nqrwpos": {"vir", "homo", "homo histrio",  # Latin
                   "in the world", "all"},      # scraps of constructions
    "ei)mi/": {"is no more",                    # οὐκέτ᾽ ἐστί — one construction
               "Troja fuit)"},                  # Latin
    "o)/noma": {"by name"},                     # ὀνόματι — one construction
    "poie/w": {"of"},                           # a scrap
    "kai/": {"que"},                            # Latin
    "gh=": {"ubi terrarum, where in (in what quarter of) the world, where on earth"},  # ποῦ γῆς
    "sko/tos": {"nocte premere"},               # Latin
    "e)pa/nw": {"part", "upper"},               # scraps of "the upper part"
}
# Lemmas the lexicon files under another spelling (Attic γίγνομαι for Koine γίνομαι).
SPELLING = {"gi/nomai": "gi/gnomai", "ginw/skw": "gignw/skw"}

PUNCT = re.compile(r"[.,;:·!?—·]")


# --------------------------------------------------------------------------
# the parse, in plain English
# --------------------------------------------------------------------------

POS = {"N": "noun", "V": "verb", "A": "adjective", "RA": "article",
       "RP": "personal pronoun", "RD": "demonstrative pronoun", "RR": "relative pronoun",
       "RI": "interrogative pronoun", "C": "conjunction", "P": "preposition",
       "D": "adverb", "X": "particle", "I": "interjection", "M": "number"}
TENSE = {"P": "present", "I": "imperfect", "F": "future", "A": "aorist",
         "X": "perfect", "Y": "pluperfect"}
VOICE = {"A": "active", "M": "middle", "P": "passive", "E": "middle/passive"}
MOOD = {"I": "indicative", "S": "subjunctive", "O": "optative", "D": "imperative",
        "N": "infinitive", "P": "participle"}
PERSON = {"1": "1st person", "2": "2nd person", "3": "3rd person"}
CASE = {"N": "nominative", "G": "genitive", "D": "dative", "A": "accusative", "V": "vocative"}
NUMBER = {"S": "singular", "P": "plural", "D": "dual"}
GENDER = {"M": "masculine", "F": "feminine", "N": "neuter", "C": "masculine/feminine"}

# CLAUDE.md fixes the wording for aorist, imperfect and perfect; the other two follow it.
ASPECT = {
    "aorist": "one completed act seen whole, not a process observed in progress",
    "imperfect": "was, and kept on being: action going on in past time",
    "present": "going on, in progress",
    "perfect": "a standing resultant state, not a past event",
    "pluperfect": "a resultant state that stood in the past",
}
SHARED_VOICE = {"present", "imperfect", "perfect", "pluperfect"}


def describe(pos, tense="", voice="", mood="", person="", case="", number="", gender=""):
    t, v = TENSE.get(tense, ""), VOICE.get(voice, "")
    if v in ("middle", "passive") and t in SHARED_VOICE:
        v = "middle/passive"
    parts = [POS.get(pos, pos)] + [x for x in (
        t, v, MOOD.get(mood, ""), PERSON.get(person, ""),
        CASE.get(case, ""), NUMBER.get(number, ""), GENDER.get(gender, "")) if x]
    return " · ".join(parts), (ASPECT.get(t, "") if pos == "V" else "")


def morphgnt(pos, code):
    """MorphGNT: a two-letter part of speech and an eight-place parse —
    person, tense, voice, mood, case, number, gender, degree."""
    f = ["" if c == "-" else c for c in code.ljust(8, "-")]
    return describe(pos.rstrip("-"), tense=f[1], voice=f[2], mood=f[3], person=f[0],
                    case=f[4], number=f[5], gender=f[6])


# --------------------------------------------------------------------------
# the lexicon
# --------------------------------------------------------------------------

BETA_LETTERS = dict(zip("αβγδεζηθικλμνξοπρστυφχψως", "abgdezhqiklmncoprstufxyws"))
BETA_MARKS = {"̓": ")", "̔": "(", "́": "/", "̀": "\\", "͂": "=",
              "ͅ": "|", "̈": "+"}


def beta(word):
    """Unicode Greek -> the Beta Code the lexicon is keyed by (πνεῦμα -> pneu=ma)."""
    out = []
    for c in unicodedata.normalize("NFD", word.lower()):
        out.append(BETA_LETTERS.get(c) or BETA_MARKS.get(c, ""))
    return "".join(out)


def load_middle_liddell():
    """{Beta Code key: [translation, …]} from Perseus's Middle Liddell, in entry order.

    Only <tr> elements from the first <sense> on count: the headword line, principal
    parts and etymology stand before the senses and are not glosses. Of homographs
    (key1, key2 …) the first entry is kept.
    """
    xml = MIDDLE_LIDDELL.read_text(encoding="utf-8")
    entries = {}
    for m in re.finditer(r'<entry\b[^>]*\bkey="([^"]+)"[^>]*>(.*?)</entry>', xml, re.S):
        key = re.sub(r"\d+$", "", m.group(1))
        if key in entries:
            continue
        body = m.group(2)
        start = body.find("<sense")
        scope = body[start:] if start >= 0 else body
        glosses = (re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", t)).strip()
                   for t in re.findall(r"<tr\b[^>]*>(.*?)</tr>", scope, re.S))
        entries[key] = [g for g in glosses if g]
    return entries


def lexicon_senses(entries, lemma):
    key = SPELLING.get(beta(lemma), beta(lemma))
    if key not in entries:
        return None
    skip, seen, out = NOT_SENSES.get(key, set()), set(), []
    for sense in entries[key]:
        if sense not in skip and sense not in seen:
            seen.add(sense)
            out.append(sense)
    return out


# --------------------------------------------------------------------------
# the sources
# --------------------------------------------------------------------------

def read_morph(book, chapter):
    """The project's own analysis of an LXX chapter, as {verse: [(form, lemma, pos, code)]},
    or None if it has not been written yet."""
    path = render.DATA / book / ("%d.morph.txt" % chapter)
    if not path.exists():
        return None
    out = {}
    for n, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        cols = line.split()
        if len(cols) != 5 or ":" not in cols[0]:
            raise SystemExit("%s line %d: expected 'verse pos parse form lemma'" % (path.name, n))
        ref, pos, code, form, lemma = cols
        out.setdefault(int(ref.split(":")[1]), []).append((form, lemma, pos, code))
    return out


def lxx_tokens(book, chapter):
    morph = read_morph(book, chapter)
    if morph is None:
        return None
    return {verse: [(form, lemma, "", morphgnt(pos, code)) for form, lemma, pos, code in words]
            for verse, words in morph.items()}


def nt_tokens(book, chapter):
    filename, number = NT[book]
    path = MORPHGNT / filename
    if not path.exists():
        return None
    out = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        cols = line.split()
        if len(cols) < 7 or cols[0][:2] != number or int(cols[0][2:4]) != chapter:
            continue
        _, pos, code, _, word, _, lemma = cols[:7]
        out.setdefault(int(cols[0][4:6]), []).append((word, lemma, "", morphgnt(pos, code)))
    return out


# --------------------------------------------------------------------------

def nfc(s):
    return unicodedata.normalize("NFC", s)


def same(a, b):
    """The source's form against ours; the verse-initial capital is ours to print."""
    a, b = nfc(a), nfc(b)
    return a == b or (a[:1].lower() == b[:1].lower() and a[1:] == b[1:])


def build(book, chapter, entries):
    verses = json.loads((render.DATA / book / ("%d.json" % chapter)).read_text(encoding="utf-8"))
    if book in NT:
        tokens, kind = nt_tokens(book, chapter), "nt"
        if tokens is None:
            return None, "sources/morphgnt/%s not found — see sources/README.md" % NT[book][0]
    else:
        tokens, kind = lxx_tokens(book, chapter), "lxx"
        if tokens is None:
            return None, ("data/%s/%d.morph.txt not found — the LXX layer needs the "
                          "project's own analysis (see that file's header in GEN/1)" % (book, chapter))

    out = []
    for verse in verses:
        number = int(verse["ref"].rsplit(":", 1)[1])
        ours = PUNCT.sub("", verse["greek"]).split()
        theirs = tokens.get(number, [])
        if len(ours) != len(theirs) or not all(same(t[0], o) for t, o in zip(theirs, ours)):
            raise SystemExit("%s: the source's words do not match the verse's Greek\n  ours:   %s\n"
                             "  source: %s" % (verse["ref"], " ".join(ours),
                                               " ".join(t[0] for t in theirs)))
        names = {n["greek"]: n["gloss"] for n in verse.get("names", [])}
        words = []
        for form, (_, lemma, _, (parse, aspect)) in zip(ours, theirs):
            senses, lexicon = lexicon_senses(entries, lemma), "Middle Liddell"
            if senses is None and lemma in names:
                senses, lexicon = [names[lemma]], "name"
            elif senses is None and lemma in LSJ:
                senses, lexicon = LSJ[lemma], "LSJ"
            elif senses is None:
                print("  note: no lexicon senses for %s (%s) — add it to LSJ in words.py"
                      % (lemma, verse["ref"]))
                senses, lexicon = [], "none"
            words.append({"form": form, "lemma": lemma, "parse": parse, "aspect": aspect,
                          "senses": senses[:SHOWN], "more": max(0, len(senses) - SHOWN),
                          "lexicon": lexicon})
        out.append({"ref": verse["ref"], "words": words})
    return {"source": SOURCE_NOTE[kind], "verses": out}, None


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("chapters", nargs="*", metavar="BOOK/CHAPTER",
                    help="chapters to build (default: everything on the page)")
    args = ap.parse_args()
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")

    targets = [(b.upper(), int(c)) for b, _, c in (a.partition("/") for a in args.chapters)]
    entries = load_middle_liddell()
    for book, chapter in targets or render.PAGE:
        layer, why = build(book, chapter, entries)
        if layer is None:
            print("SKIP  %s %d: %s" % (book, chapter, why))
            continue
        path = render.DATA / book / ("%d.words.json" % chapter)
        path.write_text(json.dumps(layer, ensure_ascii=False, indent=2) + "\n",
                        encoding="utf-8", newline="\n")
        count = sum(len(v["words"]) for v in layer["verses"])
        print("wrote %s (%d verses, %d words)" % (path.relative_to(render.ROOT).as_posix(),
                                                   len(layer["verses"]), count))


if __name__ == "__main__":
    main()
