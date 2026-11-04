#!/usr/bin/env python3
"""The SBLGNT's apparatus, read from sources/sblgntapp, and what a variant note says of it.

    python build/apparatus.py JHN/1      # each verse's statements, to write into its notes

The SBLGNT marks a variation unit in its text — ⸀ or ⸁ before one word, ⸂…⸃ or ⸄…⸅ around
several — and its apparatus says, unit by unit and in the text's order, which printed editions
read what. It compares editions, not manuscripts: Westcott–Hort, Tregelles, the Greek behind
the NIV, Robinson–Pierpont and, since the 2022 update, Nestle–Aland 28 (Holmes's introduction,
"Symbols Used in the Notes"; sblgnt.com, "Updates to the SBLGNT Apparatus").

A variant note carries the unit's statement word for word, as `statement` gives it, so what a
note says an edition reads is checked against the apparatus and nothing else. The notes were
first written from memory, and the apparatus found three of them wrong in John 1 alone: a
second reading at 1:18 it does not have, a third unit at 1:27 and Westcott–Hort's omission
there, and Robinson–Pierpont's τόν at 1:45 set before Ἰησοῦν where it follows it.

Notation (the introduction's): `]` parts the text's reading from the others, `;` one other
from the next, `+` adds words after the marked one, `–` lacks it, and `…` stands for words
every reading shares.
"""
import pathlib
import re
import sys
import unicodedata

ROOT = pathlib.Path(__file__).resolve().parent.parent
APP_DIR = ROOT / "sources/sblgntapp/text"

# The sigla, in the words a note says them in. Holmes is the SBLGNT's editor: the siglum stands
# on a reading he prints against all four editions.
SIGLA = {
    "WH": "Westcott–Hort",
    "WHmarg": "Westcott–Hort's margin",
    "WHapp": "Westcott–Hort's appendix",
    "Treg": "Tregelles",
    "Tregmarg": "Tregelles's margin",
    "NIV": "the NIV's Greek",
    "NA28": "Nestle–Aland 28",
    "NA27": "Nestle–Aland 27",
    "RP": "Robinson–Pierpont",
    "TR": "the Textus Receptus",
    "Greeven": "Greeven",
    "Holmes": "SBLGNT's editor",
    "⟦WH⟧": "Westcott–Hort, in double brackets",
}

# the signs in the text, and what a note calls each
OPEN = {"⸀": "⸀", "⸁": "⸁", "⸂": "⸂…⸃", "⸄": "⸄…⸅"}
CLOSE = {"⸂": "⸃", "⸄": "⸅"}
SIGNS = "⸀⸁⸂⸃⸄⸅"
EDGE = ".,;:·!?()[]—⟦⟧" + SIGNS
# a third unit on one word and after it, ⸀1, ⸀2 (1 Cor 12:10)
NUMBERED = re.compile(r"[⸀⸁]\d*")


def nfc(s):
    return unicodedata.normalize("NFC", s)


def bare(text):
    """A reading without the signs and the punctuation at its edges, for comparing with the text."""
    words = [w.strip(EDGE) for w in NUMBERED.sub(" ", nfc(text)).split()]
    return " ".join(w for w in words if w)


def _split_support(text):
    """A reading followed by its sigla → (reading, [sigla])."""
    words = text.split()
    sigla = []
    while words and words[-1].rstrip(".;") in SIGLA:
        sigla.insert(0, words.pop().rstrip(".;"))
    return " ".join(words), sigla


def parse_entry(text):
    """One unit of the apparatus → (lemma, support, [(reading, support), …]), or None where the
    line does not have the shape (`]` missing, or a reading with no sigla)."""
    if "]" not in text:
        return None
    left, _, right = text.partition("]")
    lemma, support = _split_support(left.strip())
    if not support:
        return None
    others, words, seen_siglum = [], [], False
    for word in right.split():
        if word.rstrip(".;") in SIGLA:
            words.append(word)
            seen_siglum = True
            if word.endswith(";"):
                others.append(_split_support(" ".join(words)))
                words, seen_siglum = [], False
            continue
        if seen_siglum:
            others.append(_split_support(" ".join(words)))
            words, seen_siglum = [], False
        words.append(word)
    if words:
        others.append(_split_support(" ".join(words)))
    if not others or any(not s for _, s in others):
        return None
    return lemma, support, others


def load(name):
    """{"1:26": [entry text, …]} for one book, or None if the file is not there. Keyed by chapter
    and verse alone: the apparatus spells the book out (Matthew), the text abbreviates it (Matt)."""
    path = APP_DIR / ("%s.txt" % name)
    if not path.exists():
        return None
    out, key = {}, None
    for line in path.read_text(encoding="utf-8-sig").splitlines():
        line = nfc(line.replace(" ", " ").strip())
        if re.match(r"^.+ \d+:\d+$", line):
            key = line.rsplit(" ", 1)[1]
            out[key] = []
            continue
        if not line or key is None:
            continue
        line = re.sub(r"^•\s*", "", line)
        line = re.sub(r"^\d+(:\d+)?(–\d+)?\s+", "", line) if not out[key] else line
        out[key].append(line.strip())
    return out


def units(greek):
    """The text's variation units, in order: [(sign, the words it marks)]."""
    greek = nfc(greek)
    out = []
    for i, ch in enumerate(greek):
        if ch in "⸀⸁":
            m = re.match(r"(\d*)(\S*)", greek[i + 1:])
            out.append((OPEN[ch] + m.group(1), bare(m.group(2))))
        elif ch in CLOSE:
            end = greek.find(CLOSE[ch], i + 1)
            out.append((OPEN[ch], bare(greek[i + 1:end if end >= 0 else None])))
    return out


def names(sigla):
    said = [SIGLA[s] for s in sigla]
    return said[0] if len(said) == 1 else ", ".join(said[:-1]) + " and " + said[-1]


def printed(lemma):
    """The text's reading as the apparatus prints it, less a sign it carries to tell two units
    on one word apart (Mark 16:8 ⸁γάρ, 1 Cor 12:10 ⸀1 ἄλλῳ)."""
    return NUMBERED.sub("", lemma).strip()


def reading(lemma, text):
    """One other reading, said in full: `+ X` is the marked words with X after them."""
    if text == "–":
        return "omitted"
    if text.startswith("+ "):
        return "%s %s" % (printed(lemma), text[2:].strip())
    return text


def statement(sign, entry):
    """What a variant note says of one unit, word for word."""
    lemma, support, others = entry
    parts = ["%s, %s" % (printed(lemma), names(support))]
    parts += ["%s, %s" % (reading(lemma, r), names(s)) for r, s in others]
    return "SBLGNT's %s: %s." % (sign, "; ".join(parts))


def verse_statements(ref_tail, greek, app):
    """For one verse, by its chapter and verse: ([statement, …], problem or None). A problem is
    the text and the apparatus failing to line up — a fault in the parse, not in the data."""
    lines = app.get(ref_tail, [])
    marks = units(greek)
    if len(lines) != len(marks):
        return [], "the text marks %d variation unit(s), the apparatus has %d" % (len(marks), len(lines))
    out = []
    for (sign, marked), line in zip(marks, lines):
        entry = parse_entry(line)
        if entry is None:
            return [], "cannot read the apparatus line %r" % line
        if bare(entry[0]).lower().split()[:1] != marked.lower().split()[:1]:
            return [], "the apparatus's %r does not stand at the text's %s%s" % (entry[0], sign, marked)
        out.append(statement(sign, entry))
    return out, None


def main():
    sys.path.insert(0, str(ROOT / "build"))
    import json
    import render
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    for item in sys.argv[1:]:
        book, _, chapter = item.partition("/")
        name = render.BOOKS[book.upper()]["name"]
        app = load(name)
        if app is None:
            sys.exit("sources/sblgntapp/text/%s.txt not found; see sources/README.md" % name)
        verses = json.loads((render.DATA / book.upper() / ("%s.json" % chapter)).read_text(encoding="utf-8"))
        for verse in verses:
            said, problem = verse_statements(verse["ref"].split(" ", 1)[1], verse["greek"], app)
            for line in ([problem] if problem else said):
                print("%-10s %s" % (verse["ref"], line))


if __name__ == "__main__":
    main()
