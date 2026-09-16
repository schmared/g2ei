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
import morph_diff as D  # noqa: E402

GEN = json.loads((render.DATA / "GEN/1.json").read_text(encoding="utf-8"))
GEN3 = json.loads((render.DATA / "GEN/3.json").read_text(encoding="utf-8"))
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


def holds(expr, message):
    """A plain assertion in the (failed, skipped, lines) shape the runners expect."""
    return (0, 0, []) if expr else (1, 0, ["  FAIL  %s" % message])


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


def with_morph(edit, check="check_analysis", chapter=1):
    """A morphology check against a copy of data/ whose GEN 1 morphology is edited, run
    for `chapter` — a corpus difference is reported on the later of its two lines."""
    def go():
        tmp = pathlib.Path(tempfile.mkdtemp())
        try:
            shutil.copytree(render.DATA, tmp / "data")
            path = tmp / "data/GEN/1.morph.txt"
            path.write_text(edit(path.read_text(encoding="utf-8")),
                            encoding="utf-8", newline="\n")
            saved, render.DATA = render.DATA, tmp / "data"
            try:
                return run(getattr(V, check), "GEN", chapter)
            finally:
                render.DATA = saved
        finally:
            shutil.rmtree(tmp, ignore_errors=True)
    return go


GEN2_MORPH = render.DATA / "GEN/2.morph.txt"


def with_second_pass(edit, expect):
    """morph_diff between GEN 2's morphology and an edited copy standing in for a second
    pass; `expect` is how many disagreements it must find."""
    def go():
        tmp = pathlib.Path(tempfile.mkdtemp())
        try:
            second = tmp / "second.txt"
            second.write_text(edit(GEN2_MORPH.read_text(encoding="utf-8")),
                              encoding="utf-8", newline="\n")
            found = D.diff(GEN2_MORPH, second)
            return holds(len(found) == expect, "expected %d disagreement(s), found %d: %s"
                         % (expect, len(found), found[:3]))
        finally:
            shutil.rmtree(tmp, ignore_errors=True)
    return go


R11 = GEN[0]["reading"]

# The same name entry as John 1:6's, marked as a later occurrence: no gloss, and the
# panel-specific form kept.
BARE = {k: v for k, v in JHN[2]["names"][0].items() if k != "gloss"}
BARE["bare"] = True

# A transliteration the edition prints in lower case (GEN 3:24), in a verse of its own.
CHERUBIM = {"greek": "χερουβιμ", "unanchored": "cheroubim", "anchored": "cherubim",
            "gloss": "(χερουβιμ, from Hebrew kĕrûbîm)"}
TRANSLIT = dict(GEN[0], greek="καὶ ἔταξεν τὰ χερουβιμ.", reading="and [[name:χερουβιμ]].",
                names=[CHERUBIM])

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
    ("anchors  name written as plain text",
                                         lambda: run(V.check_anchors, mut(JHN, [2, "reading"], "there came to be John, [[name:Ἰωάννης]]"))),
    ("words    a recorded difference that is not there",
                                         with_morph(lambda t: t.replace(
                                             "1:1 V- 3AAI-S-- ἐποίησεν ποιέω",
                                             "1:1 V- 3AAI-S-- ἐποίησεν ποιέω  # module 3AAI-P-- — stale"))),
    ("words    Greek changed, now stale", lambda: run(V.check_words, "GEN", 1, mut(GEN, [0, "greek"], "Ἐν ἀρχῇ ἐποίησε ὁ θεὸς τὸν οὐρανὸν καὶ τὴν γῆν."))),
    ("words    verse missing from layer", with_words(lambda l: l["verses"].pop())),
    ("words    word with no lemma",      with_words(lambda l: l["verses"][0]["words"][2].update(lemma=""))),
    ("greek    OT word altered",         lambda: run(V.check_greek, "GEN", 1, mut(GEN, [0, "greek"], "Ἐν ἀρχῇ ἐποίησεν ὁ θεὸς τὸν οὐρανὸν καὶ τὴν γῆ."))),
    ("greek    NT verse altered",        lambda: run(V.check_greek, "JHN", 1, mut(JHN, [0, "greek"], "Ἐν ἀρχῇ ἦν ὁ λόγος."))),
    ("greek    capital with no reason for it",
                                         lambda: run(V.check_greek, "GEN", 1, mut(GEN, [0, "greek"], "Ἐν ἀρχῇ ἐποίησεν ὁ Θεὸς τὸν οὐρανὸν καὶ τὴν γῆν."))),
    ("names    bare entry on a first occurrence",
                                         lambda: run(V.check_names, mut(JHN, [2, "names"], [BARE]))),
    ("names    lower-case transliteration with no marker",
                                         lambda: run(V.check_names, [dict(TRANSLIT, reading="and cherubim.")])),
    ("names    a name opening the verse, glossed but not marked",
                                         lambda: run(V.check_names, [dict(JHN[2], greek="Ἰωάννης ἦν.", reading="John was.")])),
    ("names    transliteration entry for a word not printed",
                                         lambda: run(V.check_names, [dict(TRANSLIT, greek="καὶ ἔταξεν αὐτούς.")])),
    ("fields   bare entry still carrying a gloss",
                                         lambda: run(V.check_fields, [dict(JHN[2], names=[dict(JHN[2]["names"][0], bare=True)])])),
    # the project's own morphology, judged by its code's own grammar
    ("morph    infinitive with its slots shifted",
                                         with_morph(lambda t: t.replace("1:1 V- 3AAI-S-- ἐποίησεν", "1:1 V- --AAN--- ἐποίησεν"), "check_morph_shape")),
    ("morph    participle missing its case",
                                         with_morph(lambda t: t.replace("1:1 V- 3AAI-S-- ἐποίησεν", "1:1 V- -PAP-ASF ἐποίησεν"), "check_morph_shape")),
    ("morph    finite verb carrying a case",
                                         with_morph(lambda t: t.replace("1:1 V- 3AAI-S-- ἐποίησεν", "1:1 V- 3AAIAS-- ἐποίησεν"), "check_morph_shape")),
    ("morph    noun with no number",     with_morph(lambda t: t.replace("1:1 N- ----DSF- ἀρχῇ", "1:1 N- ----D-F- ἀρχῇ"), "check_morph_shape")),
    ("morph    preposition with a case", with_morph(lambda t: t.replace("1:1 P- -------- Ἐν", "1:1 P- ----D--- Ἐν"), "check_morph_shape")),
    ("morph    parse the wrong length",  with_morph(lambda t: t.replace("1:1 V- 3AAI-S-- ἐποίησεν", "1:1 V- 3AAI-S- ἐποίησεν"), "check_morph_shape")),
    ("morph    article not filed under ὁ",
                                         with_morph(lambda t: t.replace("1:1 RA ----NSM- ὁ ὁ", "1:1 RA ----NSM- ὁ ὅς"), "check_morph_shape")),
    ("morph    annotation of no known kind",
                                         with_morph(lambda t: t.replace("1:1 N- ----DSF- ἀρχῇ ἀρχή", "1:1 N- ----DSF- ἀρχῇ ἀρχή  # someone said so"), "check_morph_shape")),
    # the project's own morphology, held to itself across chapters
    ("corpus   verb form parsed two ways",
                                         with_morph(lambda t: t.replace("1:1 V- 3AAI-S-- ἐποίησεν", "1:1 V- 3AAI-P-- ἐποίησεν"), "check_corpus", 2)),
    ("corpus   form under two dictionary forms",
                                         with_morph(lambda t: t.replace("1:1 N- ----NSM- θεὸς θεός", "1:1 N- ----NSM- θεὸς Θεός"), "check_corpus", 2)),
    ("corpus   noun changing its gender",
                                         with_morph(lambda t: t.replace("1:1 N- ----NSM- θεὸς θεός", "1:1 N- ----NSF- θεὸς θεός"), "check_corpus", 2)),
    ("corpus   lemma bare, then accented",
                                         with_morph(lambda t: t + "1:2 N- ----DSM- Αδαμ Αδαμ\n", "check_corpus", 2)),
    ("corpus   lemma with, then without, iota subscript",
                                         with_morph(lambda t: t + "1:2 V- 2FMI-P-- ἀποθανεῖσθε ἀποθνῄσκω\n", "check_corpus", 2)),
    ("corpus   note with no difference to explain",
                                         with_morph(lambda t: t.replace("1:1 C- -------- καὶ καί", "1:1 C- -------- καὶ καί  # corpus — stale"), "check_corpus", 1)),
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
    # The module's own spelling conventions are not discrepancies; anything else is.
    ("greek    the module's elision mark compares equal",
                                         lambda: holds(V.same_form("ἀπ᾿", "ἀπʼ"),
                                                       "U+1FBF and U+02BC must compare equal")),
    ("greek    a verse-initial capital is allowed",
                                         lambda: holds(V.same_form("καὶ", "Καὶ", initial=True),
                                                       "the head of a verse may be capitalised")),
    ("greek    a capital listed in speech is allowed",
                                         lambda: holds(V.same_form("ἀπὸ", "Ἀπὸ", speech={"Ἀπὸ"}),
                                                       "a word opening direct speech may be capitalised")),
    ("greek    a capital not listed in speech is refused",
                                         lambda: holds(not V.same_form("θεὸς", "Θεὸς"),
                                                       "a capital with no reason must be a discrepancy")),
    # A name glossed once per chapter, bare after that, and still panel-specific.
    ("fields   a bare name needs no gloss",
                                         lambda: run(V.check_fields, [dict(JHN[2], names=[BARE])])),
    ("names    a later occurrence takes a bare entry",
                                         lambda: run(V.check_names, JHN + [dict(JHN[2], ref="JHN 1:15", names=[BARE])])),
    ("names    a lower-case transliteration is glossed like a name",
                                         lambda: run(V.check_names, [TRANSLIT])),
    ("names    a name twice in the verse that glosses it",
                                         lambda: run(V.check_names, [dict(JHN[2], greek="ἦν Ἰωάννης, καὶ Ἰωάννης ἦν.",
                                                                          reading="was [[name:Ἰωάννης]], and [[name:Ἰωάννης]] was.")])),
    ("names    ...is glossed the first time only",
                                         lambda: holds(render.reading("[[name:Ἰωάννης]] and [[name:Ἰωάννης]]", JHN[2]["names"], "anchored")
                                                       .count('class="paren"') == 1,
                                                       "a repeated name prints its gloss once")),
    ("names    a name opening the verse is still a name",
                                         lambda: run(V.check_names, [dict(JHN[2], greek="Ἰωάννης ἦν.", reading="[[name:Ἰωάννης]] was.")])),
    ("names    clean GEN 3, with lower-case χερουβιμ",
                                         lambda: run(V.check_names, GEN3)),
    ("names    an inflected name matches its nominative",
                                         lambda: holds(V.matches("Ἰωάννου", "Ἰωάννης") and V.matches("Μωυσέως", "Μωυσῆς")
                                                       and V.matches("Ἀσσυρίων", "Ἀσσύριος"),
                                                       "oblique cases must find the entry")),
    ("names    names that only begin alike stay apart",
                                         lambda: holds(not V.matches("Αδα", "Αδαμ") and not V.matches("Καιναν", "Καιν")
                                                       and not V.matches("Ενως", "Ενωχ"),
                                                       "Adah is not Adam, Kainan is not Cain")),
    ("words    a documented difference is a note, not a failure",
                                         lambda: run(V.check_analysis, "GEN", 2)),
    ("anchors  a chain may contain the conventional form",
                                         lambda: run(V.check_anchors, mut(JHN, [2, "reading"], "[[a park|a park, the garden of John, paradise]] [[name:Ἰωάννης]]"))),
    ("names    a bare name prints its form with no parenthetical",
                                         lambda: holds(
                                             'class="paren"' not in render.reading(JHN[2]["reading"], [BARE], "anchored")
                                             and "John" in render.reading(JHN[2]["reading"], [BARE], "anchored")
                                             and "Iōannēs" in render.reading(JHN[2]["reading"], [BARE], "unanchored"),
                                             "a bare name keeps its panel form and drops the gloss")),
    # the morphology: well-formed, consistent with itself, and comparable across passes
    ("morph    clean GEN 1",             lambda: run(V.check_morph_shape, "GEN", 1)),
    ("morph    clean GEN 2",             lambda: run(V.check_morph_shape, "GEN", 2)),
    ("corpus   clean GEN 1",             lambda: run(V.check_corpus, "GEN", 1)),
    ("corpus   clean GEN 2, with its noted homograph ὅ",
                                         lambda: run(V.check_corpus, "GEN", 2)),
    ("morph    clean GEN 3",             lambda: run(V.check_morph_shape, "GEN", 3)),
    ("corpus   clean GEN 3, with its noted ἔφαγον and φάγῃ",
                                         lambda: run(V.check_corpus, "GEN", 3)),
    ("corpus   grave and acute are one form",
                                         lambda: holds(V.corpus_key("καλὸν") == V.corpus_key("καλόν"),
                                                       "a grave is the acute before another word")),
    ("corpus   a capital is the same form",
                                         lambda: holds(V.corpus_key("Καὶ") == V.corpus_key("καὶ"),
                                                       "a capital marks position only")),
    ("corpus   εἰς and εἷς stay two words",
                                         lambda: holds(not V.spelled_twice("εἰς", "εἷς") and not V.spelled_twice("οὐ", "οὗ"),
                                                       "differently marked words are different words")),
    ("corpus   one word spelled two ways is caught",
                                         lambda: holds(V.spelled_twice("ἀποθνῄσκω", "ἀποθνήσκω") and V.spelled_twice("Αδαμ", "Ἀδάμ"),
                                                       "iota subscript, and bare against accented")),
    ("diff     E agrees with M; M never with P",
                                         lambda: holds(V.codes_agree("3PEI-S--", "3PMI-S--") and not V.codes_agree("3AMI-S--", "3API-S--"),
                                                       "voice compatibility")),
    ("diff     an analysis agrees with itself",
                                         lambda: holds(D.diff(GEN2_MORPH, GEN2_MORPH) == [], "identical files must not differ")),
    ("diff     one changed parse is one disagreement",
                                         with_second_pass(lambda t: t.replace("2:1 V- 3API-P-- συνετελέσθησαν", "2:1 V- 3AAI-P-- συνετελέσθησαν"), 1)),
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
    page = [v for book, chapter in render.PAGE
            for v in json.loads((render.DATA / book / ("%d.json" % chapter)).read_text(encoding="utf-8"))]
    for verse in page:
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
