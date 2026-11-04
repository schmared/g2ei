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
GEN7 = json.loads((render.DATA / "GEN/7.json").read_text(encoding="utf-8"))
GEN36 = json.loads((render.DATA / "GEN/36.json").read_text(encoding="utf-8"))
GEN24 = json.loads((render.DATA / "GEN/24.json").read_text(encoding="utf-8"))
GEN19 = json.loads((render.DATA / "GEN/19.json").read_text(encoding="utf-8"))
GEN50 = json.loads((render.DATA / "GEN/50.json").read_text(encoding="utf-8"))
GEN9 = json.loads((render.DATA / "GEN/9.json").read_text(encoding="utf-8"))
EXO26 = json.loads((render.DATA / "EXO/26.json").read_text(encoding="utf-8"))
EXO8 = json.loads((render.DATA / "EXO/8.json").read_text(encoding="utf-8"))
EXO15 = json.loads((render.DATA / "EXO/15.json").read_text(encoding="utf-8"))
JHN = json.loads((render.DATA / "JHN/1.json").read_text(encoding="utf-8"))


def mut(data, path, value):
    """A deep copy of `data` with one value replaced, addressed by a key path."""
    out = copy.deepcopy(data)
    target = out
    for key in path[:-1]:
        target = target[key]
    target[path[-1]] = value
    return out


def shut(verses, index, lemma):
    """One unit written out as plain text — the accident the one-sense rule is about."""
    out = copy.deepcopy(verses)
    out[index]["reading"] = V.UNIT.sub(
        lambda m: m.group(1) if m.group(3) == lemma else m.group(0),
        out[index]["reading"])
    return out


def with_lsj(extra):
    """The lexicon check, with words added to the LSJ table for the length of one run."""
    import words as W
    saved = dict(W.LSJ)
    W.LSJ.update(extra)
    try:
        return run(V.check_lexicon)
    finally:
        W.LSJ.clear()
        W.LSJ.update(saved)


def with_homograph(extra):
    """The lexicon check, with a word added to LSJ_HOMOGRAPHS for the length of one run."""
    import words as W
    saved = dict(W.LSJ_HOMOGRAPHS)
    W.LSJ_HOMOGRAPHS.update(extra)
    try:
        return run(V.check_lexicon)
    finally:
        W.LSJ_HOMOGRAPHS.clear()
        W.LSJ_HOMOGRAPHS.update(saved)


def anchors_in(book, chapter):
    """check_anchors with the chapter named, so it reads the word-by-word layer."""
    return lambda verses, rep: V.check_anchors(verses, rep, book, chapter)


def with_pointer_dropped(drop):
    """The markup check with one entry taken out of SENSE_POINTERS for the length of one run."""
    import words as W
    saved = W.SENSE_POINTERS.pop(drop)
    try:
        return run(V.check_markup, [("EXO", 16)])
    finally:
        W.SENSE_POINTERS[drop] = saved


def with_greek_lost(drop):
    """The markup check with one entry taken out of GREEK_LOST for the length of one run."""
    import words as W
    saved = W.GREEK_LOST.pop(drop)
    try:
        return run(V.check_markup, [("GEN", 41)])
    finally:
        W.GREEK_LOST[drop] = saved


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


def with_data(path, edit, check):
    """A corpus-wide check against a copy of data/ with one chapter's file edited, for the
    checks that read the files themselves rather than the verses they are handed."""
    def go():
        tmp = pathlib.Path(tempfile.mkdtemp())
        try:
            shutil.copytree(render.DATA, tmp / "data")
            target = tmp / "data" / path
            target.write_text(edit(target.read_text(encoding="utf-8")), encoding="utf-8",
                              newline="\n")
            saved, render.DATA = render.DATA, tmp / "data"
            try:
                return check()
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


# ---- chains -------------------------------------------------------------------
# One word in one form reads one way. A chain may follow the form — singular beside
# plural, imperative beside aorist — but it may not gain or lose a sense.
FULL = "was made large, was increased, was augmented, was promoted to honour"
CUT = "was made large, was increased, was augmented"
PLURAL = "were made large, were increased, were augmented, were promoted to honour"
PAST = "made large, increased, augmented, promoted to honour"
# A sense dropped inside an and-joined gloss leaves the commas where they were, so
# counting senses cannot see it: λαμβάνω carried both of these for years.
JOINED = "was made large, was increased, was augmented and promoted to honour"
LOST_CONJUNCT = "was made large, was increased, was augmented"
# The project writes verbal aspect into the text, so a perfect participle and an aorist
# one may share a headword and differ only in that. It is grammar, not a sense.
PERFECT = "was made large and it stands so, was increased, was augmented, was promoted to honour"


def drifted(pairs):
    """pairs: [(chain, ref)] for one lemma and one headword -> how many groups drift."""
    return len(V.chains_that_drifted({("αὐξάνω", "was made large"): dict(pairs)}))


def drifted_by_card(cards):
    """cards: [(chain, ref, card)] for δίδωμι `to give` -> how many groups drift."""
    seen = {}
    for chain, ref, card in cards:
        seen.setdefault(("δίδωμι", "to give", card), {})[chain] = ref
    return len(V.chains_that_drifted(seen))


PRESENT_GIVE = "to give, to be ready to give and offer, to grant"
AORIST_GIVE = "to give, to grant"


def every_marked_name_is_a_name():
    """A word a verse marks as a name is a name in the layer, whatever the lexicon holds.

    Βάλανος, Υἱός and Εἶδος are Greek words Rahlfs prints capitalised as names. Lower-casing
    their Beta Code lands on the common noun they are made from, and the layer used to show
    that noun's senses in place of the name.
    """
    bad = []
    for book, chapter in render.PAGE:
        layer = render.DATA / book / ("%d.words.json" % chapter)
        if not layer.exists():
            continue
        verses = {v["ref"]: v for v in json.loads(
            (render.DATA / book / ("%d.json" % chapter)).read_text(encoding="utf-8"))}
        for v in json.loads(layer.read_text(encoding="utf-8"))["verses"]:
            marked = {n["greek"] for n in verses[v["ref"]].get("names", [])}
            for w in v["words"]:
                if w["form"] in marked and w["lexicon"] != "name":
                    bad.append("%s %s is a name in the verse but %s in the layer"
                               % (v["ref"], w["form"], w["lexicon"]))
    return holds(not bad, "; ".join(bad[:3]))


def no_sense_letter_as_a_gloss():
    """Perseus prints a sense's letter inside the sense; it is not a gloss.

    υἱός carried "A son" beside "a son" in every chapter from GEN 4 on.
    """
    bad = []
    for book, chapter in render.PAGE:
        layer = render.DATA / book / ("%d.words.json" % chapter)
        if not layer.exists():
            continue
        for v in json.loads(layer.read_text(encoding="utf-8"))["verses"]:
            for w in v["words"]:
                for s in w["senses"]:
                    # "A son" beside "a son": Perseus prints the sense's letter inside
                    # the sense, and it was read as a gloss of its own. Compared against
                    # the other senses, never against this one's own lower-casing.
                    others = {x[:1].lower() + x[1:] for x in w["senses"] if x != s}
                    if s[:1].isupper() and s[:1].lower() + s[1:] in others:
                        bad.append("%s %s: %r" % (v["ref"], w["form"], s))
    return holds(not bad, "; ".join(bad[:3]))


# Each must report at least one failure.
NEGATIVE = [
    ("fields   empty reading",           lambda: run(V.check_fields, mut(GEN, [0, "reading"], "  "))),
    ("fields   legacy unanchored key",   lambda: run(V.check_fields, mut(GEN, [0, "unanchored"], "x"))),
    ("fields   flag not in vocabulary",  lambda: run(V.check_fields, mut(GEN, [0, "notes", 0, "flag"], "typo"))),
    ("fields   malformed unit (no |)",   lambda: run(V.check_fields, mut(GEN, [0, "reading"], "[[made]] x"))),
    ("fields   unit with empty chain",   lambda: run(V.check_fields, mut(GEN, [0, "reading"], "[[made| ]] x"))),
    ("fields   unit with no lemma",     lambda: run(V.check_fields, mut(GEN, [0, "reading"], "[[made|a, b]] x"))),
    ("articles a plain `the` before the unit it belongs in",
                                         lambda: run(V.check_articles, "GEN", 1,
                                                     mut(GEN, [0, "reading"], "the [[house|a, b|οἶκος]] x"))),
    # GEN 31:5 had read `the [[but]] [[God|everything that God is by nature…]]`: ὁ δὲ θεός,
    # its article cut off by δέ, and the anarthrous formula on an articular θεός
    ("articles a bare `the` in front of a particle",
                                         lambda: run(V.check_articles, "GEN", 1,
                                                     mut(GEN, [0, "reading"],
                                                         "the [[but|but, however|δέ]] x"))),
    ("articles one article written twice",
                                         lambda: run(V.check_articles, "GEN", 1,
                                                     mut(GEN, [0, "reading"], "x the the house"))),
    # GEN 35:2 read `to [[to the house|…]]` and `to to the ones`: the dative marked twice
    ("articles a case marked outside the unit and in it",
                                         lambda: run(V.check_articles, "GEN", 1,
                                                     mut(GEN, [0, "reading"],
                                                         "x to [[to the house|to the house, to the abode|οἶκος]]"))),
    ("articles a case marked twice before the article's noun",
                                         lambda: run(V.check_articles, "GEN", 1,
                                                     mut(GEN, [0, "reading"], "x of of the ones y"))),
    # GEN 36:10 had read `the sons of Ησαυ; Ελιφας son Αδας`: a genitive name unmarked
    ("names  a genitive name with no `of`",
                                         lambda: run(V.check_name_cases, "GEN", 36, [
                                             dict(v, reading=v["reading"].replace(
                                                 "son of [[name:Αδας]]", "son [[name:Αδας]]"))
                                             for v in GEN36])),
    # GEN 14:13 τῇ δρυὶ τῇ Μαμβρη: the second article is not the name's, so a `the` before
    # the name does not stand in for its marker
    ("names  an article in another case taken for the name's own",
                                         lambda: run(V.check_name_cases, "GEN", 36, [
                                             dict(v, reading=v["reading"].replace(
                                                 "of the sons of [[name:Ησαυ]]", "of the sons the [[name:Ησαυ]]"))
                                             for v in GEN36])),
    # GEN 24:24 τοῦ Μελχας: a masculine article before a woman's name is not hers, and a `the`
    # before the name stands for nothing (the check had compared case alone)
    ("names  an article in another gender taken for the name's own",
                                         lambda: run(V.check_name_cases, "GEN", 24, [
                                             dict(v, reading=v["reading"].replace(
                                                 "of the one of [[name:Μελχας]]", "of the one of the [[name:Μελχας]]"))
                                             for v in GEN24])),
    # GEN 12:17 ἐτασμοῖς μεγάλοις had read `to trials with big`: a dative read by its use
    ("cases  a dative adjective read as an instrumental",
                                         lambda: run(V.check_unit_cases, "GEN", 12, [
                                             dict(v, reading=v["reading"].replace("[[to big|to big", "[[with big|with big"))
                                             for v in json.loads((render.DATA / "GEN/12.json").read_text(encoding="utf-8"))])),
    # GEN 7:11 τῇ ἡμέρᾳ ταύτῃ had read `to the day this`
    ("cases  an agreeing demonstrative left unmarked",
                                         lambda: run(V.check_unit_cases, "GEN", 7, [
                                             dict(v, reading=v["reading"].replace("[[to this|to this", "[[this|this"))
                                             for v in GEN7])),
    # GEN 7:11 had two ἐν and one unit, and read `in the six hundredth year`: one unit
    # for a word had stood for every occurrence of it in the verse
    ("one sense  a second ἐν left as a bare `in`",
                                         lambda: run(V.check_one_sense, "GEN", 7, [
                                             dict(v, reading=v["reading"].replace(
                                                 "[[in|within, inside of, and by means of|ἐν]] to the six hundredth",
                                                 "in to the six hundredth"))
                                             for v in GEN7])),
    # GEN 8:12 οὐ προσέθετο τοῦ ἐπιστρέψαι had read `not put to, to turn about`
    ("cases  an articular infinitive read as a bare infinitive",
                                         lambda: run(V.check_unit_cases, "GEN", 8, [
                                             dict(v, reading=re.sub(r"\[\[of the turning about\|[^\]]*\]\]",
                                                                    "[[to turn about|to turn about|ἐπιστρέφω]]", v["reading"]))
                                             for v in json.loads((render.DATA / "GEN/8.json").read_text(encoding="utf-8"))])),
    # GEN 33:4 had read `And Esau ran to meet him and embraced him and kissed him and fell
    # on his neck, and they both wept.` — the verse translated
    ("banned a hint that carries on the verse before",
                                         lambda: run(V.check_banned, mut(GEN, [0, "hint"], "and Esau ran to meet him."))),
    ("banned a hint that renders a speech",
                                         lambda: run(V.check_banned, mut(GEN, [0, "hint"], "Take your wife and go."))),
    ("banned the aorist formula in a reading",
                                         lambda: run(V.check_banned, mut(GEN, [0, "reading"],
                                             "x — one completed act seen whole, not a process observed in progress — y"))),
    # GEN 7:16 τὰ εἰσπορευόμενα is neuter: the article's noun is `things`, not `ones`
    ("articles a neuter participle given `the ones`",
                                         lambda: run(V.check_articles, "GEN", 7, [
                                             dict(v, reading=v["reading"].replace(
                                                 "[[the things going into|the things going into / entering|",
                                                 "[[the ones going into|the ones going into / entering|"))
                                             for v in GEN7])),
    # GEN 19:1 οἱ δύο ἄγγελοι: one article, printed with the numeral — `the two the messengers`
    ("articles the article printed again past a numeral",
                                         lambda: run(V.check_articles, "GEN", 19, [
                                             dict(v, reading=v["reading"].replace(
                                                 "[[messengers|messengers /", "[[the messengers|the messengers /"))
                                             for v in GEN19])),
    # EXO 8:19 τοῦ ἐμοῦ λαοῦ: printed with the possessive — `of the mine of the people`
    ("articles the article printed again past a possessive",
                                         lambda: run(V.check_articles, "EXO", 8, [
                                             dict(v, reading=v["reading"].replace(
                                                 "[[of people|of people,", "[[of the people|of the people,"))
                                             for v in EXO8])),
    # κιβωτός reads *a wooden box, chest, coffer*, one translation: split across items, each
    # word reads as a sense of its own
    # Q24: a chain that stops short of its card — κιβωτός without its chest and coffer
    ("coverage a chain short of its card",
                                         lambda: run(V.check_coverage, "GEN", 7, [
                                             dict(v, reading=v["reading"].replace(
                                                 "[[the wooden box|the wooden box / chest / coffer|",
                                                 "[[the wooden box|the wooden box / chest|"))
                                             for v in GEN7])),
    # Q2: a run's pieces joined with *and*, a word the Greek does not have
    ("delimiter a run joined with and",
                                         lambda: run(V.check_delimiter, "GEN", 7, [
                                             dict(v, reading=v["reading"].replace(
                                                 "the wooden box / chest / coffer", "the wooden box and chest and coffer"))
                                             for v in GEN7])),
    # Q17: the perfect's formula on some items and not all
    ("perfects the formula missing from an item",
                                         lambda: run(V.check_perfects, "GEN", 9, [
                                             dict(v, reading=v["reading"].replace(
                                                 "I have remitted and it stands so", "I have remitted"))
                                             for v in GEN9])),
    # Q32: an item no translation on the card gives — δέ's *however*, which stood beside all 1,255 of its units
    ("support  an item no card translation gives",
                                         lambda: run(V.check_support, "GEN", 7, [
                                             dict(v, reading=v["reading"].replace(
                                                 "[[but|but, while / whereas", "[[but|but, however, while / whereas"))
                                             for v in GEN7])),
    # Q35: an example's own person rendered as if it were the word's — `will I mean`, `be shall be given`
    ("english  an example's person in the word's form",
                                         lambda: run(V.check_english, "GEN", 7, [
                                             dict(v, reading=v["reading"].replace(
                                                 "I say / now / so then|δέ]]", "I say / now / so then, will I mean|δέ]]"))
                                             for v in GEN7])),
    ("english  a function word given a verb's ending",
                                         lambda: run(V.check_english, "GEN", 7, [
                                             dict(v, reading=v["reading"].replace(
                                                 "I say / now / so then|δέ]]", "I say / now / so then, whatted concerns|δέ]]"))
                                             for v in GEN7])),
    ("runs     one translation split across items",
                                         lambda: run(V.check_runs, "GEN", 7, [
                                             dict(v, reading=v["reading"].replace(
                                                 "[[the wooden box|the wooden box / chest / coffer|",
                                                 "[[the wooden box|the wooden box, the chest, the coffer|"))
                                             for v in GEN7])),
    ("lexicon  LSJ standing in for a word Middle Liddell has",
                                         lambda: with_lsj({"λόγος": ["word"]})),
    # ποιμήν is in Middle Liddell only under a truncated key, `poimh/`, which SPELLING
    # names; once named, it is a word Middle Liddell has, and LSJ may not answer for it
    ("lexicon  ...and a word it has only under a close form",
                                         lambda: with_lsj({"ποιμήν": ["shepherd"]})),
    # a homograph is a word Middle Liddell has under its key, but as another word; one it
    # lacks altogether belongs in the LSJ table
    ("lexicon  a homograph Middle Liddell has no key for",
                                         lambda: with_homograph({"γειώρας": ("γῆ", ["sojourner"])})),
    # GEN 50:7: συναναβαίνω's plain *went up with* holds ἀνέβη's headword, and passes; a bare
    # *went up* beside it is the headword loose
    ("anchors  a headword loose beside a word's own run",
                                         lambda: run(anchors_in("GEN", 50), [dict(v, reading=v["reading"].replace(
                                             "[[went up|", "went up [[went up|", 1)) if v["ref"] == "GEN 50:7" else v
                                             for v in GEN50])),
    # πάγος ends "= παγετός", a sense with no translation of its own: the card stopped short of
    # frost, and nothing failed
    ("markup   a sense that is only a pointer",
                                         lambda: with_pointer_dropped("pa/gos")),
    # βύσσινος reads "made of βύσσος", and the <tr> stopped at "made of": the card had shown
    # half a translation, and nothing failed
    ("markup   a translation a Greek word cuts off",
                                         lambda: with_greek_lost("bu/ssinos")),
    ("unit wds one word, claimed by two units",
                                         lambda: run(V.check_unit_words, "GEN", 1,
                                                     mut(GEN, [0, "reading"],
                                                         "[[made|a, b|ποιέω]] [[made|a, b|ποιέω]]"))),
    ("unit wds a merged unit whose second word the verse lacks",
                                         lambda: run(V.check_unit_words, "GEN", 1,
                                                     mut(GEN, [0, "reading"],
                                                         "[[in a hare|a, b|ἐν; λαγώς]] x"))),
    ("1 sense  a word whose entry says more, left as plain text",
                                         lambda: run(V.check_one_sense, "GEN", 1,
                                                     shut(GEN, 0, "γῆ"))),
    ("1 sense  a chain that only repeats its headword",
                                         lambda: run(V.check_one_sense, "GEN", 1,
                                                     mut(GEN, [0, "reading"],
                                                         "[[made|made|ποιέω]] x"))),
    ("unit wds unit claims a word the verse lacks",
                                         lambda: run(V.check_unit_words, "GEN", 1,
                                                     mut(GEN, [0, "reading"], "[[made|a, b|λαγώς]] x"))),
    ("fields   printed not a list",      lambda: run(V.check_fields, mut(GEN, [0, "printed"], "τοῦτου"))),
    ("fields   em dash inside a chain",  lambda: run(V.check_fields, mut(GEN, [0, "reading"], "[[made|a — b|ποιέω]] x"))),
    ("fields   unbalanced brackets",     lambda: run(V.check_fields, mut(GEN, [0, "reading"], "[[made|a x"))),
    ("fields   dangling [[name:…]]",     lambda: run(V.check_fields, mut(GEN, [0, "reading"], "x [[name:Ἀβραάμ]]"))),
    ("fields   [[flag]] in the reading", lambda: run(V.check_fields, mut(GEN, [0, "reading"], "x [[flag]]"))),
    ("fields   OT verse with no print",  lambda: run(V.check_fields, mut(GEN, [0, "print"], ""))),
    ("names    proper name unglossed",   lambda: run(V.check_names, mut(JHN, [2, "names"], []))),
    ("names    marker missing",          lambda: run(V.check_names, mut(JHN, [2, "reading"], "no marker"))),
    ("names    re-glossed in chapter",   lambda: run(V.check_names, JHN + [dict(JHN[2], ref="JHN 1:15")])),
    ("names    speech word not capital", lambda: run(V.check_names, mut(GEN, [0, "speech"], ["γῆν"]))),
    ("banned   in plain text",           lambda: run(V.check_banned, mut(GEN, [1, "reading"], "over the face of the waters"))),
    ("banned   inside a chain",          lambda: run(V.check_banned, mut(GEN, [1, "reading"], "[[x|upon the Face Of The Deep|γῆ]]"))),
    ("anchors  listed headword as text", lambda: run(V.check_anchors, mut(GEN, [0, "reading"], "In the beginning, " + R11))),
    ("anchors  own headword as text",    lambda: run(V.check_anchors, mut(GEN, [1, "reading"], "[[wind|a, b|πνεῦμα]] and the wind"))),
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
    # GEN 13:16 τὸ σπέρμα σου had read `that which is sown of you`: a gloss that opens with
    # *that which* had stood in for the article, and the Greek article was lost
    ("cases  an articular noun whose unit lost its `the`",
                                         lambda: run(V.check_unit_cases, "GEN", 13, [
                                             dict(v, reading=v["reading"].replace(
                                                 "[[the that which is sown|the that which is sown",
                                                 "[[that which is sown|that which is sown"))
                                             for v in json.loads((render.DATA / "GEN/13.json").read_text(encoding="utf-8"))])),
    # GEN 7:19 ἃ ἦν ὑποκάτω τοῦ οὐρανοῦ had read `which was below`
    ("anchors  ἦν flattened to a bare `was`",
                                         lambda: run(V.check_imperfect_be, "GEN", 7, [
                                             dict(v, reading=v["reading"].replace(
                                                 "which was, and kept on being as a standing and continuing condition and not a momentary one, [[below",
                                                 "which was [[below"))
                                             for v in GEN7])),
    # GEN 2:21 ἐπέβαλεν had read five senses as `threw`, where 22:12's ἐπιβάλῃς reads eleven
    ("ranges   one word, a short range in another form",
                                         with_data("GEN/2.json",
                                                   lambda t: re.sub(r"\[\[threw\|[^|\]]*\|ἐπιβάλλω\]\]",
                                                                    "[[threw|threw, cast upon, laid on, affixed, added|ἐπιβάλλω]]", t),
                                                   lambda: run(V.check_ranges, [("GEN", 2), ("GEN", 22)]))),
]

# Each must report no failure. The last three are the allowances, which a check
# written too strictly would break.
CONTROL = [
    # τὸ καλόν is *beauty*, the adjective *beautiful*: a word used as a noun opens a range
    # of its own, and the two are not one range cut short
    ("ranges   a word used as a noun beside its adjective",
                                         lambda: run(V.check_ranges, [("GEN", 2), ("GEN", 3), ("GEN", 12)])),
    ("chains   a sense dropped from one occurrence is drift",
                                         lambda: holds(drifted([(FULL, "GEN 21:8"), (CUT, "GEN 30:30")]) == 1,
                                                       "a chain that lost a sense must be reported")),
    ("chains   a sense dropped inside an and-joined gloss",
                                         lambda: holds(drifted([(JOINED, "GEN 21:8"), (LOST_CONJUNCT, "GEN 30:30")]) == 1,
                                                       "the commas still number the same; the sense is gone")),
    # πόθεν read `from what country` in one verse and `how can it be` in another: neither is
    # a subset of the other, and each has lost what the other kept
    ("chains   each chain saying what the other does not",
                                         lambda: holds(drifted([("was made large, was increased", "GEN 21:8"),
                                                                ("was made large, was augmented", "GEN 30:30")]) == 1,
                                                       "two chains apart both ways have both drifted")),
    ("chains   one form of one word is not two words",
                                         lambda: holds(V.stem("deposed") == V.stem("depose")
                                                       and V.stem("strove") == V.stem("strive"),
                                                       "a verb ending is the last to come off")),
    ("chains   the chain following the form is not drift",
                                         lambda: holds(drifted([(FULL, "GEN 21:8"), (PLURAL, "GEN 30:30")]) == 0,
                                                       "singular beside plural is the form, not drift")),
    ("chains   a tense the form calls for is not drift",
                                         lambda: holds(drifted([(FULL, "GEN 21:8"), (PAST, "GEN 30:30")]) == 0,
                                                       "imperative beside aorist is the form, not drift")),
    ("chains   the aspect formula is not a sense",
                                         lambda: holds(drifted([(FULL, "GEN 21:8"), (PERFECT, "GEN 30:30")]) == 0,
                                                       "a perfect and an aorist may share a headword")),
    ("chains   two forms the lexicon reads apart are not drift",
                                         lambda: holds(drifted_by_card([(PRESENT_GIVE, "EXO 5:7", ("present",)),
                                                                        (AORIST_GIVE, "EXO 5:21", ("aorist",))]) == 0,
                                                       "διδόναι and δοῦναι have different cards")),
    ("chains   one card read two ways is drift",
                                         lambda: holds(drifted_by_card([(PRESENT_GIVE, "EXO 5:7", ("card",)),
                                                                        (AORIST_GIVE, "EXO 5:21", ("card",))]) == 1,
                                                       "the same card, a sense lost")),
    ("chains   the corpus carries no drift",
                                         lambda: run(V.check_chains, render.PAGE)),
    ("words    a name the verse marks is a name in the layer",
                                         every_marked_name_is_a_name),
    ("words    no sense-letter stands as a gloss",
                                         no_sense_letter_as_a_gloss),
    ("fields   clean GEN + JHN",         lambda: run(V.check_fields, GEN + JHN)),
    ("names    clean JHN",               lambda: run(V.check_names, JHN)),
    ("banned   clean GEN",               lambda: run(V.check_banned, GEN)),
    ("anchors  clean GEN + JHN",         lambda: run(V.check_anchors, GEN + JHN)),
    ("coverage clean GEN 7",              lambda: run(V.check_coverage, "GEN", 7, GEN7)),
    ("delimiter clean GEN 7",             lambda: run(V.check_delimiter, "GEN", 7, GEN7)),
    ("perfects clean GEN 9",              lambda: run(V.check_perfects, "GEN", 9, GEN9)),
    ("support  clean GEN 7",              lambda: run(V.check_support, "GEN", 7, GEN7)),
    ("english  clean GEN 7",              lambda: run(V.check_english, "GEN", 7, GEN7)),
    # a unit on a word's third occurrence, after two in another case: δέρρις at EXO 26:8 opens δέρρεσι,
    # and its chain is read against that form's card, not the first occurrence's
    ("support  clean EXO 26, a unit on a later occurrence",
                                         lambda: run(V.check_support, "EXO", 26, EXO26)),
    ("coverage clean EXO 26, a unit on a later occurrence",
                                         lambda: run(V.check_coverage, "EXO", 26, EXO26)),
    ("anchors  a word's one translation holds another's headword",
                                         lambda: run(anchors_in("GEN", 50), GEN50)),
    ("words    clean GEN",               lambda: run(V.check_words, "GEN", 1, GEN)),
    ("greek    clean GEN",               lambda: run(V.check_greek, "GEN", 1, GEN)),
    ("greek    clean JHN",               lambda: run(V.check_greek, "JHN", 1, JHN)),
    ("anchors  headword repeats in its own chain",
                                         lambda: run(V.check_anchors, mut(GEN, [1, "reading"], "[[wind|breath, wind, spirit|πνεῦμα]] x"))),
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
    ("greek    a capital with iota subscript is its titlecase",
                                         lambda: holds(V.same_form("ᾗ", "ᾟ", initial=True),
                                                       "ᾗ's capital is ᾟ, not ἯΙ")),
    ("greek    a capital opening a sentence inside the verse is allowed",
                                         lambda: holds(V.sentence_starts("καὶ ἀπέθανεν. Καὶ ἔζησεν Καιναν —") == [True, False, True, False, False],
                                                       "GEN 11:13: Rahlfs opens Cainan's paragraph with a capital, inside the verse")),
    ("greek    a capital listed in speech is allowed",
                                         lambda: holds(V.same_form("ἀπὸ", "Ἀπὸ", speech={"Ἀπὸ"}),
                                                       "a word opening direct speech may be capitalised")),
    ("greek    a misprint listed in printed is allowed",
                                         lambda: holds(V.same_form("τούτου", "τοῦτου", printed={"τοῦτου"}),
                                                       "GEN 24:58: the page's own accent, kept as printed")),
    ("greek    a misprint not listed in printed is refused",
                                         lambda: holds(not V.same_form("τούτου", "τοῦτου"),
                                                       "an unlisted difference in pointing must be a discrepancy")),
    ("greek    a capital not listed in speech is refused",
                                         lambda: holds(not V.same_form("θεὸς", "Θεὸς"),
                                                       "a capital with no reason must be a discrepancy")),
    # A name glossed once per chapter, bare after that, and still panel-specific.
    ("fields   a bare name needs no gloss",
                                         lambda: run(V.check_fields, [dict(JHN[2], names=[BARE])])),
    ("names    a later occurrence takes a bare entry",
                                         lambda: run(V.check_names, JHN + [dict(JHN[2], ref="JHN 1:15", names=[BARE])])),
    ("names    two cases of one name in one verse, each with its entry",
                                         lambda: run(V.check_names, json.loads((render.DATA / "GEN/16.json").read_text(encoding="utf-8"))[:2])),
    ("names    one form naming two bearers is glossed for each",
                                         lambda: run(V.check_names, JHN + [dict(JHN[2], ref="JHN 1:15",
                                                     names=[dict(JHN[2]["names"][0], anchored="Jonah")])])),
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
    ("unit wds a merged unit names both its words",
                                         lambda: holds(V.lemmas("ἀνά + accusative; μέσος") == ["ἀνά", "μέσος"]
                                                       and V.lemmas("μετά + accusative") == ["μετά"],
                                                       "the lemma field lists every word a unit opens")),
    # ὁ δέ: the article as pronoun carries its noun like any other, `the one, but, … said`
    ("articles ὁ δέ's article carrying its noun",
                                         lambda: run(V.check_articles, "GEN", 1,
                                                     mut(GEN, [0, "reading"],
                                                         "the one [[but|but, however|δέ]] x"))),
    # EXO 6:12 ἔναντι κυρίου: the preposition's one translation is plain text and ends in *of*
    ("articles ἔναντι's own *of* before a genitive",
                                         lambda: run(V.check_articles, "GEN", 1,
                                                     mut(GEN, [0, "reading"],
                                                         "x in the presence of [[of lord|of lord, of master|κύριος]] y"))),
    # EXO 14:22 ἐξ εὐωνύμων: εὐώνυμος is *of good name*, and its genitive marks the case before it
    # EXO 15:26 ἐνωτίσῃ ταῖς ἐντολαῖς: the verb's one translation ends in *to*
    ("articles ἐνωτίζομαι's own *to* before a dative",
                                         lambda: run(V.check_articles, "GEN", 1,
                                                     mut(GEN, [0, "reading"],
                                                         "x you may hearken to [[to the injunctions|to the injunctions and orders|ἐντολή]] y"))),
    # EXO 15:1 ᾌσωμεν: a capital with its iota beside it is titlecase, not upper case
    ("names    clean EXO 15, a titlecase capital opening speech",
                                         lambda: run(V.check_names, EXO15)),
    ("articles εὐώνυμος's own *of* inside its genitive",
                                         lambda: run(V.check_articles, "GEN", 1,
                                                     mut(GEN, [0, "reading"],
                                                         "x [[of of good name|of of good name and honoured, of of good omen|εὐώνυμος]] y"))),
    ("articles clean GEN 7, with its neuter participle",
                                         lambda: run(V.check_articles, "GEN", 7, GEN7)),
    ("articles clean GEN 19 and EXO 8, an article over a numeral and a possessive",
                                         lambda: tuple(map(sum, zip(run(V.check_articles, "GEN", 19, GEN19)[:2],
                                                                    run(V.check_articles, "EXO", 8, EXO8)[:2]))) + ([],)),
    ("lexicon  clean: every LSJ word is one Middle Liddell lacks",
                                         lambda: run(V.check_lexicon)),
    # διαναπαύω stays with LSJ: Middle Liddell has only the middle, which does not say
    # what the active of GEN 5:29 means, and a close form must cover the form in the text
    ("lexicon  a close form that does not cover the text's form is no entry",
                                         lambda: holds("διαναπαύω" in __import__("words").LSJ,
                                                       "διαναπαύω reads LSJ's active")),
    ("1 sense  clean GEN 1",             lambda: run(V.check_one_sense, "GEN", 1, GEN)),
    # κιβωτός has one numbered sense and still wants a unit, because that sense reads
    # `a wooden box, chest, coffer`; ὁρκίζω keeps its repeating chain because `made
    # swear` holds ποιέω's headword, and flattening it would write that as plain text.
    ("1 sense  clean GEN 24, with its kept unit",
                                         lambda: run(V.check_one_sense, "GEN", 24,
                                                     json.loads((render.DATA / "GEN/24.json").read_text(encoding="utf-8")))),
    ("names    clean GEN 3, with lower-case χερουβιμ",
                                         lambda: run(V.check_names, GEN3)),
    ("names    an inflected name matches its nominative",
                                         lambda: holds(V.matches("Ἰωάννου", "Ἰωάννης") and V.matches("Μωυσέως", "Μωυσῆς")
                                                       and V.matches("Ἀσσυρίων", "Ἀσσύριος"),
                                                       "oblique cases must find the entry")),
    ("names    a people's name is not its land's",
                                         lambda: holds(not V.matches("Αἰγύπτιοι", "Αἴγυπτον") and V.matches("Χαναναῖοι", "Χαναναίων")
                                                       and V.matches("Σαρας", "Σαραν") and V.matches("Σιδῶνος", "Σιδῶνα"),
                                                       "the Egyptians are not Egypt; Σαρας is Σαραν")),
    ("names    two endings may differ in length",
                                         lambda: holds(V.matches("Σοδομοις", "Σοδομα") and V.matches("Σοδομα", "Σοδομοις"),
                                                       "Σοδομοις is Σοδομα (GEN 13:12)")),
    ("names    names that only begin alike stay apart",
                                         lambda: holds(not V.matches("Αδα", "Αδαμ") and not V.matches("Καιναν", "Καιν")
                                                       and not V.matches("Ενως", "Ενωχ"),
                                                       "Adah is not Adam, Kainan is not Cain")),
    ("words    a space inside the module's parse code does not split the word",
                                         lambda: holds(V.module_words("Μεσραιμ<S>708772</S><m>lxx.N.N M</m> καὶ<S>2532</S><m>lxx.C</m>")
                                                       == [("Μεσραιμ", "708772", "lxx.N.N M"), ("καὶ", "2532", "lxx.C")],
                                                       "GEN 10:6 has `lxx.N.N M`; the words are found by their tags")),
    ("words    a documented difference is a note, not a failure",
                                         lambda: run(V.check_analysis, "GEN", 2)),
    ("anchors  a chain may contain the conventional form",
                                         lambda: run(V.check_anchors, mut(JHN, [2, "reading"], "[[a park|a park, the garden of John, paradise|παράδεισος]] [[name:Ἰωάννης]]"))),
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
    chains = [c.strip() for _, c, _ in render.UNIT.findall(verse["reading"])]
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
