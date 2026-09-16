#!/usr/bin/env python3
"""Compare two independent analyses of one chapter's morphology.

    python build/morph_diff.py data/GEN/3.morph.txt second-pass.txt

The second pass is made without the first in view — from the Greek and the conventions
alone — and every disagreement is then settled in data/<BOOK>/<chapter>.morph.txt by
correcting whichever side was wrong. Two passes seldom make the same slip in the same
place, so what survives both is far less likely to be a slip at all.

Words are compared in order within each verse: part of speech, dictionary form and
parse, with E agreeing with M or P and C with M or F, as in validate.py. Annotations
are ignored. Both files are first checked for well-formedness, since a malformed code on
either side would otherwise surface as a run of spurious disagreements.

Exit status is 0 only when the two analyses agree.
"""
import argparse
import pathlib
import sys
import unicodedata

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import validate  # noqa: E402
import words  # noqa: E402


def nfc(s):
    return unicodedata.normalize("NFC", s)


def diff(first, second):
    """Every disagreement between two morph files, as a line of text; [] when they agree."""
    a = words.parse_morph(pathlib.Path(first))
    b = words.parse_morph(pathlib.Path(second))
    out = []
    for label, morph in (("first", a), ("second", b)):
        for verse, lines in sorted(morph.items()):
            for i, (form, lemma, pos, code, _) in enumerate(lines, 1):
                for problem in validate.shape_problems(pos, code, lemma):
                    out.append("verse %d word %d (%s), %s file: %s"
                               % (verse, i, form, label, problem))
    for verse in sorted(set(a) | set(b)):
        x, y = a.get(verse, []), b.get(verse, [])
        if len(x) != len(y):
            out.append("verse %d: %d words in the first, %d in the second"
                       % (verse, len(x), len(y)))
            continue
        for i, (p, q) in enumerate(zip(x, y), 1):
            if validate.corpus_key(p[0]) != validate.corpus_key(q[0]):
                out.append("verse %d word %d: the files disagree on the word itself, %s / %s"
                           % (verse, i, p[0], q[0]))
                continue
            what = []
            if p[2] != q[2]:
                what.append("part of speech %s / %s" % (p[2], q[2]))
            if nfc(p[1]) != nfc(q[1]):
                what.append("lemma %s / %s" % (p[1], q[1]))
            if not validate.codes_agree(p[3], q[3]):
                what.append("parse %s / %s" % (p[3], q[3]))
            if what:
                out.append("verse %d word %d (%s): %s" % (verse, i, p[0], "; ".join(what)))
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("first", help="the analysis on record, e.g. data/GEN/3.morph.txt")
    ap.add_argument("second", help="the independent second pass")
    args = ap.parse_args()
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    found = diff(args.first, args.second)
    for line in found:
        print("  " + line)
    words_compared = sum(len(v) for v in words.parse_morph(pathlib.Path(args.first)).values())
    print()
    print("%d words compared: %s" % (
        words_compared, "the two analyses agree" if not found else
        "%d disagreement%s to settle" % (len(found), "" if len(found) == 1 else "s")))
    return 1 if found else 0


if __name__ == "__main__":
    sys.exit(main())
