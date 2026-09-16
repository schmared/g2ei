#!/usr/bin/env python3
"""Check the checks: every check in build/validate.py, fired at broken data.

    python build/test_validate.py
    python build/test_validate.py -v     # show every case's own message

A validator that passes everything is indistinguishable from no validator at all.
Each NEGATIVE case takes the real data, breaks one thing, and requires the matching
check to report at least one failure. Each CONTROL requires the untouched data to
pass — including the cases that are deliberately allowed, like a headword repeating
inside its own chain. DERIVATION holds the invariant the two panels rest on: both
come from the one `reading` string, so every chain must appear in both, in order.

Without sources/, the checks that read them report SKIP; a negative case whose check
skipped is reported as skipped rather than counted as a miss, so this runs anywhere.
"""
import argparse
import contextlib
import copy
import io
import json
import pathlib
import re
import shutil
import sys
import tempfile

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import render  # noqa: E402
import validate as V  # noqa: E402

GEN = json.loads((render.DATA / "GEN/1.json").read_text(encoding="utf-8"))
JHN = json.loads((render.DATA / "JHN/1.json").read_text(encoding="utf-8"))


def mut(data, path, value):
    """A deep copy of `data` with one value replaced, addressed by a key path."""
    out = copy.deepcopy(data)
    target = out
    for key in path[:-1]:
        target = target[key]
    target[path[-1]] = value
    return out


def run(fn, *args):
    """One check against one dataset, its output captured. -> (failed, skipped, lines)"""
    rep, buf = V.Report(), io.StringIO()
    with contextlib.redirect_stdout(buf):
        fn(*args, rep)
    return rep.failed, rep.skipped, buf.getvalue().strip().splitlines()


def with_words(edit):
    """check_words against a copy of data/ whose GEN word-by-word layer is edited.

    The layer is a file rather than a field, so breaking it means breaking a copy;
    render.DATA is pointed at the copy for the duration.
    """
    def go():
        tmp = pathlib.Path(tempfile.mkdtemp())
        try:
            shutil.copytree(render.DATA, tmp / "data")
            path = tmp / "data/GEN/1.words.json"
            layer = json.loads(path.read_text(encoding="utf-8"))
            edit(layer)
            path.write_text(json.dumps(layer, ensure_ascii=False), encoding="utf-8",
                            newline="\n")
            saved, render.DATA = render.DATA, tmp / "data"
            try:
                return run(V.check_words, "GEN", 1, GEN)
            finally:
                render.DATA = saved
        finally:
            shutil.rmtree(tmp, ignore_errors=True)
    return go


R11 = GEN[0]["reading"]

# Each must report at least one failure.
NEGATIVE = [
    ("fields   empty reading",           lambda: run(V.check_fields, mut(GEN, [0, "reading"], "  "))),
    ("fields   legacy unanchored key",   lambda: run(V.check_fields, mut(GEN, [0, "unanchored"], "x"))),
    ("fields   flag not in vocabulary",  lambda: run(V.check_fields, mut(GEN, [0, "notes", 0, "flag"], "typo"))),
    ("fields   malformed unit (no |)",   lambda: run(V.check_fields, mut(GEN, [0, "reading"], "[[made]] x"))),
    ("fields   unit with empty chain",   lambda: run(V.check_fields, mut(GEN, [0, "reading"], "[[made| ]] x"))),
    ("fields   em dash inside a chain",  lambda: run(V.check_fields, mut(GEN, [0, "reading"], "[[made|a — b]] x"))),
    ("fields   unbalanced brackets",     lambda: run(V.check_fields, mut(GEN, [0, "reading"], "[[made|a x"))),
    ("fields   dangling [[name:…]]",     lambda: run(V.check_fields, mut(GEN, [0, "reading"], "x [[name:Ἀβραάμ]]"))),
    ("fields   [[flag]] in the reading", lambda: run(V.check_fields, mut(GEN, [0, "reading"], "x [[flag]]"))),
    ("fields   OT verse with no print",  lambda: run(V.check_fields, mut(GEN, [0, "print"], ""))),
    ("names    proper name unglossed",   lambda: run(V.check_names, mut(JHN, [2, "names"], []))),
    ("names    marker missing",          lambda: run(V.check_names, mut(JHN, [2, "reading"], "no marker"))),
    ("names    re-glossed in chapter",   lambda: run(V.check_names, JHN + [dict(JHN[2], ref="JHN 1:15")])),
    ("names    speech word not capital", lambda: run(V.check_names, mut(GEN, [0, "speech"], ["γῆν"]))),
    ("banned   in plain text",           lambda: run(V.check_banned, mut(GEN, [1, "reading"], "over the face of the waters"))),
    ("banned   inside a chain",          lambda: run(V.check_banned, mut(GEN, [1, "reading"], "[[x|upon the Face Of The Deep]]"))),
    ("anchors  listed headword as text", lambda: run(V.check_anchors, mut(GEN, [0, "reading"], "In the beginning, " + R11))),
    ("anchors  own headword as text",    lambda: run(V.check_anchors, mut(GEN, [1, "reading"], "[[wind|a, b]] and the wind"))),
    ("anchors  English name unanchored", lambda: run(V.check_anchors, mut(JHN, [2, "names", 0, "unanchored"], "John"))),
    ("words    Greek changed, now stale", lambda: run(V.check_words, "GEN", 1, mut(GEN, [0, "greek"], "Ἐν ἀρχῇ ἐποίησε ὁ θεὸς τὸν οὐρανὸν καὶ τὴν γῆν."))),
    ("words    verse missing from layer", with_words(lambda l: l["verses"].pop())),
    ("words    word with no lemma",      with_words(lambda l: l["verses"][0]["words"][2].update(lemma=""))),
    ("greek    OT word altered",         lambda: run(V.check_greek, "GEN", 1, mut(GEN, [0, "greek"], "Ἐν ἀρχῇ ἐποίησεν ὁ θεὸς τὸν οὐρανὸν καὶ τὴν γῆ."))),
    ("greek    NT verse altered",        lambda: run(V.check_greek, "JHN", 1, mut(JHN, [0, "greek"], "Ἐν ἀρχῇ ἦν ὁ λόγος."))),
]

# Each must report no failure. The last three are the allowances, which a check
# written too strictly would break.
CONTROL = [
    ("fields   clean GEN + JHN",         lambda: run(V.check_fields, GEN + JHN)),
    ("names    clean JHN",               lambda: run(V.check_names, JHN)),
    ("banned   clean GEN",               lambda: run(V.check_banned, GEN)),
    ("anchors  clean GEN + JHN",         lambda: run(V.check_anchors, GEN + JHN)),
    ("words    clean GEN",               lambda: run(V.check_words, "GEN", 1, GEN)),
    ("greek    clean GEN",               lambda: run(V.check_greek, "GEN", 1, GEN)),
    ("greek    clean JHN",               lambda: run(V.check_greek, "JHN", 1, JHN)),
    ("anchors  headword repeats in its own chain",
                                         lambda: run(V.check_anchors, mut(GEN, [1, "reading"], "[[wind|breath, wind, spirit]] x"))),
    ("names    sentence-initial capital is not a name",
                                         lambda: run(V.check_names, mut(GEN, [0, "names"], []))),
    ("words    a chapter with no layer is a note, not a failure",
                                         lambda: run(V.check_words, "JHN", 2, JHN)),
]

SHADED = re.compile(r'<span class="chain">(.*?)</span>')


def derivation(verse):
    """Both panels from one string: every chain, in order, in each of them."""
    names = verse.get("names", [])
    anchored = render.reading(verse["reading"], names, "anchored")
    unanchored = render.reading(verse["reading"], names, "unanchored")
    shaded = [re.sub(r"^— | —$", "", s) for s in SHADED.findall(anchored)]
    chains = [c.strip() for _, c in render.UNIT.findall(verse["reading"])]
    ok = (len(shaded) == len(chains)
          and all(s.lower() == c.lower() for s, c in zip(shaded, chains))
          and all(c.lower() in unanchored.lower() for c in chains))
    return ok, len(chains)


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("-v", "--verbose", action="store_true",
                    help="show each case's own message, not just its verdict")
    args = ap.parse_args()
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")

    bad = skipped = 0

    print("NEGATIVE — the check must fire")
    for label, case in NEGATIVE:
        failed, skips, lines = case()
        if failed:
            verdict = "ok  "
        elif skips:
            verdict, skipped = "skip", skipped + 1
        else:
            verdict, bad = "MISS", bad + 1
        message = next((l for l in lines if "FAIL" in l or "SKIP" in l), "")
        print("  %s %-36s %s" % (verdict, label,
                                 message[14:].strip()[:84] if args.verbose or verdict != "ok  " else ""))

    print("\nCONTROL — the check must not fire")
    for label, case in CONTROL:
        failed, _, lines = case()
        if failed:
            bad += 1
        print("  %s %-52s %d failure(s)" % ("ok  " if not failed else "BAD ", label, failed))
        if failed and args.verbose:
            for line in lines:
                print("       %s" % line.strip())

    print("\nDERIVATION — every chain appears in both panels, in order")
    for verse in GEN + JHN:
        ok, n = derivation(verse)
        if not ok:
            bad += 1
        print("  %s %-10s %d chains" % ("ok  " if ok else "BAD ", verse["ref"], n))

    print()
    print("%d case%s wrong" % (bad, "" if bad == 1 else "s") if bad else "all cases as expected")
    if skipped:
        print("%d negative case%s skipped — the check needs a source this repository does "
              "not carry; see sources/README.md" % (skipped, "" if skipped == 1 else "s"))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
