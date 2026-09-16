#!/usr/bin/env python3
"""Mechanical checks over data/<BOOK>/<chapter>.json.

Run before committing a chapter. Exit status is 0 only if nothing failed.

    python build/validate.py                 # every chapter on the page
    python build/validate.py GEN/1 JHN/1     # named chapters only
    python build/validate.py -v              # list every passing check too

Six checks — the five CLAUDE.md asks for, and one for the word-by-word layer:

  fields   every verse has ref / greek / notes / reading, non-empty; notes well-formed;
           flags drawn from the permitted vocabulary; every [[anchor|chain]] unit and
           [[name:…]] marker well-formed and resolvable; every Old Testament verse cites
           the printed page its Greek was transcribed from
  names    every proper name in the Greek is glossed on its first occurrence in the
           chapter and left bare after that
  banned   no phrase from BANNED_PHRASES in either reading panel
  anchors  no headword stands bare: an anchor never appears as plain text outside its
           unit, so the unanchored panel never shows it on its own. (It may appear
           inside its own chain — the chain is the whole range, the headword its
           first sense.)
  words    the word-by-word file, where there is one, still matches the verse's Greek
  greek    the New Testament, character-for-character against the SBLGNT in sources/.
           The Old Testament is transcribed from the printed Rahlfs, so its word forms
           are cross-checked only where LXX_RAHLFS_DIR points at a local morphological
           module; otherwise that check, and the one on our own morphology, report SKIP

Both reading panels are derived from the one `reading` string (see build/render.py),
so they cannot disagree with each other. These checks are about what that string says.

BANNED_PHRASES and ANCHORS are maintained editorial lists. They grow as chapters are
written; see the comments on each.
"""
import argparse
import html
import json
import os
import pathlib
import re
import sqlite3
import sys
import unicodedata

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import render  # noqa: E402  — for DATA, PAGE, BOOKS, and the reading markup

ROOT = render.ROOT
SOURCES = ROOT / "sources"

FLAGS = {None, "divergence", "not in this text", "name", "variant"}

# Which edition each book is checked against. LXX books are read from the Rahlfs
# MyBible module; NT books from the SBLGNT plain-text files.
EDITIONS = {"GEN": "lxx", "JHN": "sblgnt"}

# The two Old Testament cross-checks are optional and off by default. They read a local
# Rahlfs morphological module, which is no part of this repository and never a source for
# it: the Greek in data/ is transcribed from the printed page each verse cites, and the
# morphology in data/*/*.morph.txt is the project's own. Point LXX_RAHLFS_DIR at a module
# to turn them on for a session; without it both report SKIP and everything else runs.
_RAHLFS_DIR = os.environ.get("LXX_RAHLFS_DIR")
LXX_RAHLFS = pathlib.Path(_RAHLFS_DIR) if _RAHLFS_DIR else None
LXX_DB = LXX_RAHLFS / "11_end-users_files/MyBible/Bibles/LXX1.SQLite3" if LXX_RAHLFS else None
SBLGNT_DIR = SOURCES / "sblgnt/text"


# --------------------------------------------------------------------------
# maintained editorial lists
# --------------------------------------------------------------------------

# Phrases familiar from other English versions that have no basis in the Greek.
# Add to this whenever the notes carry a `not in this text` flag. Checked against
# the reading panels only — the notes are where these phrases are supposed to be
# named and refused.
BANNED_PHRASES = [
    # GEN 1:2 — the LXX drops Hebrew *pānîm* at both points, reading only
    # ἐπάνω τῆς ἀβύσσου / ἐπάνω τοῦ ὕδατος.
    "face of the waters",
    "face of the deep",
]

# Conventional headwords that must never be written as plain text in a reading —
# only ever as the anchor of an [[anchor|chain]] unit, so the unanchored panel
# drops them. Every verse's own anchors are checked this way automatically; this
# list exists to catch a headword written out as prose where the unit was forgotten,
# which the verse's own units cannot know about.
ANCHORS = [
    {"anchor": "in beginning", "lemma": "ἐν ἀρχῇ"},
    {"anchor": "in the beginning", "lemma": "ἐν ἀρχῇ"},
    {"anchor": "made", "lemma": "ποιέω"},
    {"anchor": "the heaven", "lemma": "οὐρανός"},
    {"anchor": "the earth", "lemma": "γῆ"},
    {"anchor": "unseen", "lemma": "ἀόρατος"},
    {"anchor": "not properly prepared", "lemma": "ἀκατασκεύαστος"},
    {"anchor": "darkness", "lemma": "σκότος"},
    {"anchor": "the great deep", "lemma": "ἄβυσσος"},
    {"anchor": "the word", "lemma": "λόγος"},
    {"anchor": "towards the God", "lemma": "πρὸς τὸν θεόν"},
]


# --------------------------------------------------------------------------
# reporting
# --------------------------------------------------------------------------

class Report:
    def __init__(self, verbose=False):
        self.verbose = verbose
        self.failed = 0
        self.skipped = 0

    def ok(self, check, detail):
        if self.verbose:
            print("  ok    %-8s %s" % (check, detail))

    def done(self, check, detail, before):
        """Report a clean pass only if nothing failed since `before`."""
        if self.failed == before:
            self.ok(check, detail)

    def fail(self, check, ref, message):
        self.failed += 1
        print("  FAIL  %-8s %-10s %s" % (check, ref, message))

    def skip(self, check, message):
        self.skipped += 1
        print("  SKIP  %-8s %s" % (check, message))

    def note(self, check, message):
        print("  note  %-8s %s" % (check, message))


# --------------------------------------------------------------------------
# helpers
# --------------------------------------------------------------------------

MARKER = re.compile(r"\[\[(.*?)\]\]")


def fold(word):
    """Accent- and case-insensitive key for a Greek word."""
    d = unicodedata.normalize("NFD", word)
    return "".join(c for c in d if unicodedata.category(c) != "Mn" and c.isalpha()).lower()


def spans(haystack, needle):
    """All case-insensitive occurrences of a literal string, as (start, end)."""
    out, low, target, i = [], haystack.lower(), needle.lower(), 0
    while True:
        i = low.find(target, i)
        if i < 0:
            return out
        out.append((i, i + len(target)))
        i += 1


def units(text):
    """The [[anchor|chain]] units in a reading, as (anchor, chain)."""
    return [(a.strip(), c.strip()) for a, c in render.UNIT.findall(text)]


def outside_units(text):
    """The reading with every unit and name marker taken out — the plain text that
    appears identically in both panels."""
    return render.NAME.sub(" ", render.UNIT.sub(" ¦ ", text))


def panels(verse):
    """Both derived panels as plain text."""
    names = verse.get("names", [])
    return {form: html.unescape(re.sub(r"<[^>]+>", "",
                                       render.reading(verse["reading"], names, form)))
            for form in ("unanchored", "anchored")}


def show_diff(a, b, label_a, label_b):
    """First differing character, with a little context on each side."""
    n = min(len(a), len(b))
    i = next((k for k in range(n) if a[k] != b[k]), n)
    if i == len(a) == len(b):
        return "differ, but not in any character (length %d)" % len(a)
    def at(s):
        if i >= len(s):
            return "end of string"
        c = s[i]
        return "%r (U+%04X %s)" % (c, ord(c), unicodedata.name(c, "?"))
    return "char %d: %s %s / %s %s   …%s…" % (
        i, label_a, at(a), label_b, at(b), a[max(0, i - 22):i + 8])


# --------------------------------------------------------------------------
# 1. fields
# --------------------------------------------------------------------------

def check_fields(verses, rep):
    before = rep.failed
    for verse in verses:
        ref = verse.get("ref", "<no ref>")

        for field in ("ref", "greek", "reading"):
            if not str(verse.get(field, "")).strip():
                rep.fail("fields", ref, "%s is missing or empty" % field)
        if not verse.get("notes"):
            rep.fail("fields", ref, "notes is missing or empty")
        for legacy in ("unanchored", "anchored"):
            if legacy in verse:
                rep.fail("fields", ref, "%r is the old schema; both panels now derive "
                                        "from `reading`" % legacy)
        if EDITIONS.get(ref.split(" ")[0]) == "lxx" and not str(verse.get("print", "")).strip():
            rep.fail("fields", ref, "no `print` citation — Old Testament Greek is transcribed "
                                    "from the printed Rahlfs, and each verse cites its page")
        speech = verse.get("speech", [])
        if not (isinstance(speech, list) and all(isinstance(w, str) and w for w in speech)):
            rep.fail("fields", ref, "`speech` must be a list of Greek words")

        for i, note in enumerate(verse.get("notes") or []):
            where = "note %d" % (i + 1)
            if not str(note.get("lemma", "")).strip():
                rep.fail("fields", ref, "%s has no lemma" % where)
            if not str(note.get("text", "")).strip():
                rep.fail("fields", ref, "%s (%s) has no text" % (where, note.get("lemma")))
            flag = note.get("flag")
            if flag not in FLAGS:
                rep.fail("fields", ref, "%s has flag %r; permitted: %s"
                         % (where, flag, ", ".join(sorted(str(f) for f in FLAGS))))
            if "[[flag]]" in note.get("text", "") and not flag:
                rep.fail("fields", ref, "%s uses [[flag]] but carries no flag" % where)

        text = str(verse.get("reading", ""))
        known = {n.get("greek") for n in verse.get("names", [])}
        for m in MARKER.finditer(text):
            body = m.group(1)
            if "[" in body or "]" in body:
                rep.fail("fields", ref, "nested markup in [[%s]]" % body[:40])
            elif body.startswith("name:"):
                if body[5:] not in known:
                    rep.fail("fields", ref, "[[%s]] has no entry in names" % body)
            elif body == "flag":
                rep.fail("fields", ref, "[[flag]] belongs in a note, not the reading")
            else:
                anchor, bar, chain = body.partition("|")
                if not bar or "|" in chain or not anchor.strip() or not chain.strip():
                    rep.fail("fields", ref,
                             "malformed unit [[%s]] — expected [[anchor|chain]]" % body[:40])
                elif "—" in anchor or "—" in chain:
                    rep.fail("fields", ref,
                             "unit %r contains an em dash; em dashes delimit chains in the "
                             "anchored panel, so use a comma inside a chain" % anchor)
        leftover = MARKER.sub("", text)
        if "[[" in leftover or "]]" in leftover:
            rep.fail("fields", ref, "unbalanced [[ ]] in reading")

        for n in verse.get("names", []):
            for field in ("greek", "unanchored", "anchored", "gloss"):
                if not str(n.get(field, "")).strip():
                    rep.fail("fields", ref, "name %r has no %s" % (n.get("greek"), field))

    rep.done("fields", "%d verses" % len(verses), before)


# --------------------------------------------------------------------------
# 2. names
# --------------------------------------------------------------------------

SENTENCE_END = ".;!?"


def proper_names(greek):
    """Capitalised words that are not sentence-initial.

    Both editions capitalise three things: the start of a sentence, a proper name,
    and the first word of direct speech (Rahlfs, Gen 1:3: εἶπεν ὁ θεός Γενηθήτω
    φῶς). Excluding the sentence-initial position leaves names and speech-openers;
    check_names skips the speech-openers a verse lists in its `speech` field.
    """
    words, out, initial = greek.split(), [], True
    for word in words:
        bare = word.strip("".join(set(",.;:·!?()[]«»—’")))
        if bare and bare[0].isupper() and not initial:
            out.append(bare)
        initial = bool(word) and word[-1] in SENTENCE_END
    return out


def matches(candidate, entry_greek):
    """Is `candidate` an inflected form of the name recorded as `entry_greek`?

    Compared on a shared accent-stripped prefix, so oblique cases match the
    nominative the names entry records — Ἰωάννου against Ἰωάννης, Μωυσέως
    against Μωυσῆς.
    """
    a, b = fold(candidate), fold(entry_greek)
    if not a or not b:
        return False
    shared = 0
    for x, y in zip(a, b):
        if x != y:
            break
        shared += 1
    return shared >= min(4, len(a), len(b))


def check_names(verses, rep):
    before = rep.failed
    glossed, found_any = {}, False

    for verse in verses:
        ref = verse["ref"]
        entries = verse.get("names", [])
        capitals, speech = proper_names(verse["greek"]), verse.get("speech", [])
        for word in speech:
            if word not in capitals:
                rep.fail("names", ref, "`speech` lists %s, which is not a capitalised word "
                                       "inside this verse's Greek" % word)
        candidates = [c for c in capitals if c not in speech]
        found_any = found_any or bool(candidates)
        used = set()

        for candidate in candidates:
            entry = next((e for e in entries if matches(candidate, e["greek"])), None)
            key = next((k for k in glossed if matches(candidate, k)), None)

            if key is None:
                if entry is None:
                    rep.fail("names", ref,
                             "%s is a proper name on first occurrence with no entry in names"
                             % candidate)
                    continue
                used.add(entry["greek"])
                glossed[entry["greek"]] = ref
                marker = "[[name:%s]]" % entry["greek"]
                if marker not in verse["reading"]:
                    rep.fail("names", ref, "%s is glossed here first but the reading "
                                           "carries no %s" % (candidate, marker))
            else:
                if entry is not None:
                    used.add(entry["greek"])
                    rep.fail("names", ref,
                             "%s was already glossed at %s; later occurrences are bare"
                             % (candidate, glossed[key]))

        for entry in entries:
            if entry["greek"] not in used:
                rep.fail("names", ref,
                         "names carries %s, which is not a proper name in this verse's Greek"
                         % entry["greek"])

    if not found_any:
        rep.done("names", "no proper names in this chapter", before)
    else:
        rep.done("names", "%d glossed: %s" % (len(glossed), ", ".join(glossed)), before)


# --------------------------------------------------------------------------
# 3. banned phrases
# --------------------------------------------------------------------------

def check_banned(verses, rep):
    before = rep.failed
    for verse in verses:
        for panel, text in panels(verse).items():
            for phrase in BANNED_PHRASES:
                if spans(text, phrase):
                    rep.fail("banned", verse["ref"],
                             "%s contains %r, which has no basis in this Greek text"
                             % (panel, phrase))
    rep.done("banned", "%d phrases checked" % len(BANNED_PHRASES), before)


# --------------------------------------------------------------------------
# 4. anchors
# --------------------------------------------------------------------------

def check_anchors(verses, rep):
    """No headword stands bare in the reading.

    The unanchored panel is built from the chains, so the only way a headword can
    reach it on its own is as plain text written outside any unit. That is caught
    here, for this verse's own headwords and for the listed ones. A headword inside
    its own chain is allowed: the chain is the whole lexical range, and the headword
    is simply its first sense.
    """
    before, total = rep.failed, 0
    for verse in verses:
        ref, text = verse["ref"], verse["reading"]
        bare = outside_units(text)
        own = units(text)
        total += len(own)

        unanchored = panels(verse)["unanchored"]
        for name in verse.get("names", []):
            if re.search(r"\b%s\b" % re.escape(name["anchored"]), unanchored):
                rep.fail("anchors", ref,
                         "unanchored uses the conventional form %r for %s; it takes the "
                         "transliteration %r" % (name["anchored"], name["greek"],
                                                 name["unanchored"]))

        watch = {}
        for anchor, _ in own:
            watch.setdefault(anchor.lower(), "a unit in this verse")
        for item in ANCHORS:
            watch.setdefault(item["anchor"].lower(), item["lemma"])
        for anchor, why in watch.items():
            if re.search(r"\b%s\b" % re.escape(anchor), bare, re.I):
                rep.fail("anchors", ref,
                         "%r (%s) is written as plain text; make it a unit, "
                         "[[%s|…]], so the unanchored panel drops it" % (anchor, why, anchor))

    rep.done("anchors", "%d units, %d listed headwords" % (total, len(ANCHORS)), before)


# --------------------------------------------------------------------------
# 5. word by word
# --------------------------------------------------------------------------

def check_words(book, chapter, verses, rep):
    """The word-by-word file, where there is one, still matches the verse's Greek.

    build/words.py writes it from sources/; if a verse's Greek changes afterwards,
    the layer is stale, and this says so rather than letting it render wrong.
    """
    before = rep.failed
    path = render.DATA / book / ("%d.words.json" % chapter)
    if not path.exists():
        rep.note("words", "no word-by-word layer for this chapter yet "
                          "(python build/words.py %s/%d)" % (book, chapter))
        return
    by_ref = {v["ref"]: v["words"]
              for v in json.loads(path.read_text(encoding="utf-8")).get("verses", [])}
    nfc = lambda s: unicodedata.normalize("NFC", s)
    if EDITIONS.get(book) == "lxx":
        check_analysis(book, chapter, rep)
    for verse in verses:
        ref = verse["ref"]
        if ref not in by_ref:
            rep.fail("words", ref, "missing from %s — re-run build/words.py" % path.name)
            continue
        forms = [nfc(w.get("form", "")) for w in by_ref[ref]]
        if forms != [nfc(w) for w in PUNCT.sub("", verse["greek"]).split()]:
            rep.fail("words", ref, "the word-by-word forms no longer match the Greek — "
                                   "re-run build/words.py")
        for i, w in enumerate(by_ref[ref]):
            for field in ("lemma", "parse"):
                if not str(w.get(field, "")).strip():
                    rep.fail("words", ref, "word %d (%s) has no %s" % (i + 1, w.get("form"), field))
    rep.done("words", "%d verses match the Greek" % len(verses), before)


LXX_LEXEMES = LXX_RAHLFS / "09a_LXX_lexicon/01-04.csv" if LXX_RAHLFS else None
FEATURES = ("person", "tense", "voice", "mood", "case", "number", "gender")


def module_features(code):
    """lxx.V.AAI3S -> {tense: A, voice: A, mood: I, person: 3, number: S}"""
    code = code[4:] if code.startswith("lxx.") else code
    pos, _, f = code.partition(".")
    if pos == "V":
        out = dict(tense=f[0:1], voice=f[1:2], mood=f[2:3])
        rest = f[3:]
        if out["mood"] == "P":
            out.update(case=rest[0:1], number=rest[1:2], gender=rest[2:3])
        elif out["mood"] != "N":
            out.update(person=rest[0:1], number=rest[1:2])
        return out
    return dict(case=f[0:1], number=f[1:2], gender=f[2:3])


def morph_features(code):
    return {k: v for k, v in zip(FEATURES, code) if v != "-"}


def agrees(ours, theirs):
    """Our analysis against the module's. Part of speech is not compared — the two
    schemes label δέ, for instance, differently. Our E (middle/passive) and C
    (masculine/feminine) agree with either of the pair they stand for."""
    either = {("voice", "E"): {"M", "P", "E"}, ("gender", "C"): {"M", "F", "C"}}
    for k in FEATURES:
        a, b = ours.get(k, ""), theirs.get(k, "")
        if a != b and b not in either.get((k, a), set()):
            return False
    return True


def check_analysis(book, chapter, rep):
    """The project's own LXX morphology against a local module, where one is configured.

    A reference, never a source: nothing from it is written into data/, and the check is
    optional — see the note on LXX_RAHLFS above.
    """
    import words
    morph = words.read_morph(book, chapter)
    if morph is None:
        rep.fail("words", "%s %d" % (book, chapter), "no data/%s/%d.morph.txt" % (book, chapter))
        return
    if not (LXX_DB and LXX_DB.exists() and LXX_LEXEMES.exists()):
        rep.skip("words", "our morphology not cross-checked — no local module "
                          "(set LXX_RAHLFS_DIR)")
        return
    lemmas = {}
    for line in LXX_LEXEMES.read_text(encoding="utf-8").splitlines():
        m = re.match(r"(\d+)\t.*?<font color='3'>([^<]+)</font>", line)
        if m:
            lemmas.setdefault(m.group(1), m.group(2))
    con = sqlite3.connect(LXX_DB)
    try:
        (number,) = con.execute("select book_number from books where long_name = ?",
                                (render.BOOKS[book]["name"],)).fetchone()
        rows = dict(con.execute("select verse, text from verses where book_number = ? "
                                "and chapter = ?", (number, chapter)).fetchall())
    finally:
        con.close()
    nfc = lambda s: unicodedata.normalize("NFC", s)
    for verse, ours in sorted(morph.items()):
        ref = "%s %d:%d" % (book, chapter, verse)
        theirs = [re.match(r"(.+?)<S>(\d+)</S>.*?<m>([^<]+)</m>", t).groups()
                  for t in rows.get(verse, "").split()]
        if len(ours) != len(theirs):
            rep.fail("words", ref, "%d words analysed, %d in the module"
                     % (len(ours), len(theirs)))
            continue
        for i, ((form, lemma, _, code), (_, lexeme, mcode)) in enumerate(zip(ours, theirs), 1):
            if nfc(lemma) != nfc(lemmas.get(lexeme, "")):
                rep.fail("words", ref, "word %d (%s): our lemma %s, the module %s — check "
                         "which is right" % (i, form, lemma, lemmas.get(lexeme, "?")))
            elif not agrees(morph_features(code), module_features(mcode)):
                rep.fail("words", ref, "word %d (%s): our parse %s, the module %s — check "
                         "which is right" % (i, form, code, mcode))


# --------------------------------------------------------------------------
# 6. Greek against the source edition
# --------------------------------------------------------------------------

PUNCT = re.compile(r"[.,;:·!?—·]")


def sblgnt_source(name):
    path = SBLGNT_DIR / ("%s.txt" % name)
    if not path.exists():
        return None, "sources/sblgnt/text/%s.txt not found" % name
    out = {}
    for line in path.read_text(encoding="utf-8-sig").splitlines():
        if "\t" in line:
            key, text = line.split("\t", 1)
            out[key.strip()] = text.strip()
    return out, None


def lxx_source(name, chapter):
    if not (LXX_DB and LXX_DB.exists()):
        return None, ("Old Testament word forms not cross-checked — no local module "
                      "(set LXX_RAHLFS_DIR); the Greek is transcribed from the printed "
                      "page each verse cites")
    con = sqlite3.connect(LXX_DB)
    try:
        row = con.execute(
            "select book_number from books where long_name = ?", (name,)).fetchone()
        if row is None:
            return None, "%s is not in the Rahlfs module" % name
        out = {}
        for verse, text in con.execute(
                "select verse, text from verses where book_number = ? and chapter = ?",
                (row[0], chapter)):
            out[verse] = re.sub(r"<S>.*?</S>|<m>.*?</m>", "", text).split()
        return out, None
    finally:
        con.close()


def check_greek(book, chapter, verses, rep):
    before = rep.failed
    nfc = lambda s: unicodedata.normalize("NFC", s)
    name = render.BOOKS[book]["name"]
    edition = EDITIONS.get(book)

    if edition is None:
        rep.skip("greek", "%s has no source edition configured in EDITIONS" % book)
        return

    if edition == "sblgnt":
        src, err = sblgnt_source(name)
        if err:
            rep.skip("greek", err)
            return
        for verse in verses:
            key = "%s %s" % (name, verse["ref"].split(" ", 1)[1])
            if key not in src:
                rep.fail("greek", verse["ref"], "%s is not in the SBLGNT text file" % key)
                continue
            want, got = nfc(src[key]), nfc(verse["greek"])
            if want != got:
                rep.fail("greek", verse["ref"],
                         show_diff(want, got, "SBLGNT", "data"))
        rep.done("greek", "%d verses character-for-character against SBLGNT" % len(verses), before)
        return

    src, err = lxx_source(name, chapter)
    if err:
        rep.skip("greek", err)
        return
    for verse in verses:
        number = int(verse["ref"].rsplit(":", 1)[1])
        if number not in src:
            rep.fail("greek", verse["ref"], "not in the Rahlfs module")
            continue
        want = [nfc(w) for w in src[number]]
        got = [nfc(w) for w in PUNCT.sub("", verse["greek"]).split()]
        if len(want) != len(got):
            rep.fail("greek", verse["ref"],
                     "%d words in the data, %d in Rahlfs" % (len(got), len(want)))
            continue
        for i, (a, b) in enumerate(zip(want, got)):
            # Rahlfs prints a capital at the head of a sentence; the module carries
            # bare word forms, so the verse-initial capital is not a discrepancy.
            if i == 0 and a[:1].upper() + a[1:] == b:
                continue
            if a != b:
                rep.fail("greek", verse["ref"],
                         "word %d: Rahlfs %r / data %r" % (i + 1, a, b))
    rep.done("greek", "%d verses against the local module" % len(verses), before)
    rep.note("greek", "word forms only; the pointing is Rahlfs's own, transcribed from "
                      "the printed page each verse cites")


# --------------------------------------------------------------------------

def validate(book, chapter, rep):
    path = render.DATA / book / ("%d.json" % chapter)
    print("\n%s %d  %s" % (book, chapter, path.relative_to(ROOT).as_posix()))
    if not path.exists():
        rep.fail("data", "%s %d" % (book, chapter), "file not found")
        return
    verses = json.loads(path.read_text(encoding="utf-8"))
    check_fields(verses, rep)
    if rep.failed:
        # the remaining checks read `reading`; on a malformed file they would only
        # repeat the same fault in other words
        return
    check_names(verses, rep)
    check_banned(verses, rep)
    check_anchors(verses, rep)
    check_words(book, chapter, verses, rep)
    check_greek(book, chapter, verses, rep)


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("chapters", nargs="*", metavar="BOOK/CHAPTER",
                    help="chapters to check (default: everything on the page)")
    ap.add_argument("-v", "--verbose", action="store_true",
                    help="print passing checks as well as failures")
    args = ap.parse_args()
    # reports carry Greek; don't let a cp1252 pipe on Windows crash on it
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")

    targets = []
    for item in args.chapters:
        book, _, chapter = item.partition("/")
        if not chapter.isdigit():
            ap.error("expected BOOK/CHAPTER, got %r" % item)
        targets.append((book.upper(), int(chapter)))
    targets = targets or render.PAGE

    rep = Report(args.verbose)
    for book, chapter in targets:
        validate(book, chapter, rep)

    print()
    if rep.failed:
        print("%d check%s failed" % (rep.failed, "" if rep.failed == 1 else "s"))
    else:
        print("all checks passed")
    if rep.skipped:
        print("%d check%s skipped — a skipped check is not a passing check"
              % (rep.skipped, "" if rep.skipped == 1 else "s"))
    return 1 if rep.failed else 0


if __name__ == "__main__":
    sys.exit(main())
