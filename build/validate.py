#!/usr/bin/env python3
"""Mechanical checks over data/<BOOK>/<chapter>.json.

Run before committing a chapter. Exit status is 0 only if nothing failed.

    python build/validate.py                 # every chapter on the page
    python build/validate.py GEN/1 JHN/1     # named chapters only
    python build/validate.py -v              # list every passing check too

Five checks, per CLAUDE.md:

  fields   every verse has ref / greek / notes / unanchored / anchored, non-empty,
           notes well-formed, flags drawn from the permitted vocabulary, and every
           [[name:…]] / [[flag]] marker resolvable
  names    every proper name in the Greek is glossed on its first occurrence in the
           chapter, in both reading texts, and left bare after that
  banned   no phrase from BANNED_PHRASES in either reading text
  anchors  no headword from ANCHORS in the unanchored text
  greek    the Greek matches the source edition in sources/ character-for-character

BANNED_PHRASES and ANCHORS are maintained editorial lists. They grow as chapters are
written; see the comments on each.
"""
import argparse
import json
import pathlib
import re
import sqlite3
import sys
import unicodedata

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import render  # noqa: E402  — for DATA, PAGE, BOOKS

ROOT = render.ROOT
SOURCES = ROOT / "sources"

FLAGS = {None, "divergence", "not in this text", "name", "variant"}

# Which edition each book is checked against. LXX books are read from the Rahlfs
# MyBible module; NT books from the SBLGNT plain-text files.
EDITIONS = {"GEN": "lxx", "JHN": "sblgnt"}

LXX_DB = SOURCES / "LXX-Rahlfs-1935/11_end-users_files/MyBible/Bibles/LXX1.SQLite3"
SBLGNT_DIR = SOURCES / "sblgnt/text"


# --------------------------------------------------------------------------
# maintained editorial lists
# --------------------------------------------------------------------------

# Phrases familiar from other English versions that have no basis in the Greek.
# Add to this whenever the notes carry a `not in this text` flag. Checked against
# the reading texts only — the notes are where these phrases are supposed to be
# named and refused.
BANNED_PHRASES = [
    # GEN 1:2 — the LXX drops Hebrew *pānîm* at both points, reading only
    # ἐπάνω τῆς ἀβύσσου / ἐπάνω τοῦ ὕδατος.
    "face of the waters",
    "face of the deep",
]

# Conventional headwords the anchored panel keeps and the unanchored panel must
# do without.
#
# This is a curated list, not every anchor. A word belongs here only if the
# unanchored text is meant to drop it — δέ keeps "but", ὕδωρ keeps "the water",
# and ἄνθρωπος keeps "a man", because those carry no gloss-chain that replaces them.
#
# `allow` lists contexts in which the same string is a legitimate link in a
# gloss-chain rather than a headword standing on its own. Prefer writing the
# anchor as the full phrase ("the Word", not "Word") — that alone resolves most
# apparent collisions.
ANCHORS = [
    {"anchor": "in the beginning", "lemma": "ἐν ἀρχῇ"},
    {"anchor": "made", "lemma": "ποιέω"},
    {"anchor": "the heaven", "lemma": "οὐρανός"},
    {"anchor": "the earth", "lemma": "γῆ"},
    {"anchor": "invisible", "lemma": "ἀόρατος"},
    {"anchor": "unfurnished", "lemma": "ἀκατασκεύαστος",
     # the chain itself runs "un-built-out, unfurnished, unequipped, …"; the
     # anchored panel lifts the word out to serve as the anchor
     "allow": ["un-built-out, unfurnished"]},
    {"anchor": "darkness", "lemma": "σκότος"},
    {"anchor": "the abyss", "lemma": "ἄβυσσος"},
    {"anchor": "the Word", "lemma": "λόγος"},
    {"anchor": "with God", "lemma": "πρὸς τὸν θεόν"},
    {"anchor": "this one", "lemma": "οὗτος"},
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

        for field in ("ref", "greek", "unanchored", "anchored"):
            if not str(verse.get(field, "")).strip():
                rep.fail("fields", ref, "%s is missing or empty" % field)
        if not verse.get("notes"):
            rep.fail("fields", ref, "notes is missing or empty")

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

        known = {n.get("greek") for n in verse.get("names", [])}
        for panel in ("unanchored", "anchored"):
            for marker in re.findall(r"\[\[name:([^\]]+)\]\]", verse.get(panel, "")):
                if marker not in known:
                    rep.fail("fields", ref,
                             "%s references [[name:%s]] with no entry in names"
                             % (panel, marker))
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

    In both source editions a capital marks either the start of a sentence or a
    proper name, so excluding the sentence-initial position leaves the names. A
    false positive is corrected by glossing the word; a word that should not be
    glossed has no business being capitalised mid-sentence.
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
        candidates = proper_names(verse["greek"])
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
                for panel in ("unanchored", "anchored"):
                    if marker not in verse[panel]:
                        rep.fail("names", ref,
                                 "%s is glossed here first but %s carries no %s"
                                 % (candidate, panel, marker))
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
        for panel in ("unanchored", "anchored"):
            for phrase in BANNED_PHRASES:
                if spans(verse[panel], phrase):
                    rep.fail("banned", verse["ref"],
                             "%s contains %r, which has no basis in this Greek text"
                             % (panel, phrase))
    rep.done("banned", "%d phrases checked" % len(BANNED_PHRASES), before)


# --------------------------------------------------------------------------
# 4. anchors
# --------------------------------------------------------------------------

def check_anchors(verses, rep):
    before = rep.failed
    for verse in verses:
        text = verse["unanchored"]

        for name in verse.get("names", []):
            for hit in re.finditer(r"\b%s\b" % re.escape(name["anchored"]), text):
                rep.fail("anchors", verse["ref"],
                         "unanchored uses the conventional form %r for %s; it takes the "
                         "transliteration %r" % (name["anchored"], name["greek"],
                                                 name["unanchored"]))
                break

        for item in ANCHORS:
            allowed = [s for a in item.get("allow", []) for s in spans(text, a)]
            for hit in re.finditer(r"\b%s\b" % re.escape(item["anchor"]), text, re.I):
                if any(lo <= hit.start() and hit.end() <= hi for lo, hi in allowed):
                    continue
                rep.fail("anchors", verse["ref"],
                         "unanchored contains the anchor %r (%s) — the chain replaces it"
                         % (item["anchor"], item["lemma"]))
                break

    rep.done("anchors", "%d headwords checked" % len(ANCHORS), before)


# --------------------------------------------------------------------------
# 5. Greek against the source edition
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
    if not LXX_DB.exists():
        return None, "%s not found" % LXX_DB.relative_to(ROOT).as_posix()
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
    rep.done("greek", "%d verses against LXX-Rahlfs-1935" % len(verses), before)
    rep.note("greek", "word forms only — the Rahlfs module carries no punctuation, "
                      "so the pointing in the data is unverified")


# --------------------------------------------------------------------------

def validate(book, chapter, rep):
    path = render.DATA / book / ("%d.json" % chapter)
    print("\n%s %d  %s" % (book, chapter, path.relative_to(ROOT).as_posix()))
    if not path.exists():
        rep.fail("data", "%s %d" % (book, chapter), "file not found")
        return
    verses = json.loads(path.read_text(encoding="utf-8"))
    check_fields(verses, rep)
    check_names(verses, rep)
    check_banned(verses, rep)
    check_anchors(verses, rep)
    check_greek(book, chapter, verses, rep)


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("chapters", nargs="*", metavar="BOOK/CHAPTER",
                    help="chapters to check (default: everything on the page)")
    ap.add_argument("-v", "--verbose", action="store_true",
                    help="print passing checks as well as failures")
    args = ap.parse_args()

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
