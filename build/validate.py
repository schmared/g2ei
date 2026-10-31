#!/usr/bin/env python3
"""Mechanical checks over data/<BOOK>/<chapter>.json.

Run before committing a chapter. Exit status is 0 only if nothing failed.

    python build/validate.py                 # every chapter on the page
    python build/validate.py GEN/1 JHN/1     # named chapters only
    python build/validate.py -v              # list every passing check too

Eight checks — the ones CLAUDE.md asks for, one for the word-by-word layer, and two
that hold the project's own morphology to its own grammar and to itself:

  fields   every verse has ref / greek / notes / reading, non-empty; notes well-formed;
           flags drawn from the permitted vocabulary; every [[anchor|chain]] unit and
           [[name:…]] marker well-formed and resolvable; every Old Testament verse cites
           the printed page its Greek was transcribed from
  names    every proper name in the Greek is glossed on its first occurrence in the
           chapter and left bare after that — and so is a name its capital cannot show,
           a transliteration in lower case or a name opening a sentence, once its entry
           names it
  banned   no phrase from BANNED_PHRASES in either reading panel
  anchors  no headword stands bare: an anchor never appears as plain text outside its
           unit, so the unanchored panel never shows it on its own. (It may appear
           inside its own chain — the chain is the whole range, the headword its
           first sense.)
  words    the word-by-word file, where there is one, still matches the verse's Greek
  1 sense  a content word is a unit exactly when its entry says more than its headword
           does — both ways, so neither a range left shut nor a chain that only repeats
           its headword can happen by accident
  morph    the project's own Old Testament morphology is well-formed by the code's own
           grammar: an infinitive has a tense and no case, a participle has a case, a
           preposition has no features — so a shifted slot fails with no reference
  corpus   that morphology agrees with itself: a form keeps its dictionary form, a
           verb its parse and a noun its gender and number wherever they recur,
           unless the line says why with "# corpus ..."
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
import collections
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
EDITIONS = {"GEN": "lxx", "EXO": "lxx", "JHN": "sblgnt"}

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

UNIT = re.compile(r"\[\[(?!name:)([^|\]]+)\|([^|\]]+)\|([^|\]]+)\]\]")


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
    """The [[anchor|chain|lemma]] units in a reading, as (anchor, chain, lemma)."""
    return [(a.strip(), c.strip(), l.strip()) for a, c, l in render.UNIT.findall(text)]


def lemmas(field):
    """The Greek words a unit's lemma field names, the case each carries dropped.

    One unit may open more than one word: ἐν and ἀνά take no unit of their own before
    a noun, the noun's unit swallows them, and its chain opens both. The field lists
    them, `ἐν; γῆ`, and each item may still carry its own case, `ἀνά + accusative`.
    """
    return [item.split(" + ")[0].strip() for item in field.split(";") if item.strip()]


# The aspect formulas the project writes into a reading whole, the same words every
# time. They are the project's own phrasing, not a gloss of any one Greek word, so the
# bare-headword check reads past them: ὡς at GEN 27:23 is a unit, `as`, and the `as`
# inside "kept on being as a standing …" is not that headword loose in the text.
FORMULAS = (
    "was, and kept on being as a standing and continuing condition and not a momentary one,",
    "were, and kept on being as a standing and continuing condition and not a momentary one,",
    "was, and kept on being,",
    "were, and kept on being,",
    "one completed act seen whole, not a process observed in progress",
    # the same two, where the sentence ends on them (GEN 26:7)
    "was, and kept on being as a standing and continuing condition and not a momentary one.",
    "were, and kept on being as a standing and continuing condition and not a momentary one.",
    # and where a semicolon follows them (EXO 13:17)
    "was, and kept on being as a standing and continuing condition and not a momentary one;",
    "were, and kept on being as a standing and continuing condition and not a momentary one;",
)


def outside_units(text):
    """The reading with every unit, name marker and aspect formula taken out — the
    plain text that appears identically in both panels."""
    for formula in FORMULAS:
        text = text.replace(formula, " ¦ ")
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
        for field in ("speech", "printed"):
            words = verse.get(field, [])
            if not (isinstance(words, list) and all(isinstance(w, str) and w for w in words)):
                rep.fail("fields", ref, "`%s` must be a list of Greek words" % field)

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
                part = body.split("|")
                if len(part) != 3 or not all(f.strip() for f in part):
                    rep.fail("fields", ref,
                             "malformed unit [[%s]] — expected [[anchor|chain|lemma]]"
                             % body[:40])
                elif "—" in part[0] or "—" in part[1]:
                    rep.fail("fields", ref,
                             "unit %r contains an em dash; em dashes delimit chains in the "
                             "anchored panel, so use a comma inside a chain" % part[0])
        leftover = MARKER.sub("", text)
        if "[[" in leftover or "]]" in leftover:
            rep.fail("fields", ref, "unbalanced [[ ]] in reading")

        for n in verse.get("names", []):
            bare = n.get("bare", False)
            if not isinstance(bare, bool):
                rep.fail("fields", ref, "name %r: `bare` is %r; it must be true or false"
                         % (n.get("greek"), bare))
            fields = ("greek", "unanchored", "anchored")
            for field in fields if bare else fields + ("gloss",):
                if not str(n.get(field, "")).strip():
                    rep.fail("fields", ref, "name %r has no %s" % (n.get("greek"), field))
            if bare and str(n.get("gloss", "")).strip():
                rep.fail("fields", ref, "name %r is marked bare but carries a gloss; a name "
                                        "is glossed on its first occurrence only"
                         % n.get("greek"))

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
        # A capital with its iota written beside it (ᾌσωμεν, EXO 15:1) is titlecase, not upper case.
        if bare and (bare[0].isupper() or bare[0].istitle()) and not initial:
            out.append(bare)
        initial = bool(word) and word[-1] in SENTENCE_END
    return out


def matches(candidate, entry_greek):
    """Is `candidate` an inflected form of the name recorded as `entry_greek`?

    Compared accent-stripped, so oblique cases match the nominative the names entry
    records — Ἰωάννου against Ἰωάννης, Μωυσέως against Μωυσῆς: a shared stem of at
    least four letters, and what differs no longer than a case ending. A Semitic name is
    indeclinable and matches only itself, so two names that merely begin alike stay two
    names — Αδα is not Αδαμ (GEN 4:19), and Καιν is not Καιναν: where one form is the bare
    stem, the lengths must be within one of each other. Where both carry an ending, they
    may differ by more — Σοδομοις is Σοδομα (GEN 13:12). What differs must be a case ending on both sides, so a name and the
    name of its people stay two names — Αἰγύπτιοι is not Αἴγυπτον (GEN 12:14).
    """
    a, b = fold(candidate), fold(entry_greek)
    if not a or not b:
        return False
    if a == b:
        return True
    shared = 0
    for x, y in zip(a, b):
        if x != y:
            break
        shared += 1
    ends = a[shared:], b[shared:]
    return (shared >= 4 and (abs(len(a) - len(b)) <= 1 or all(ends))
            and ends[0] in CASE_ENDINGS and ends[1] in CASE_ENDINGS)


# What may differ between two forms of one name, accents folded away: the endings of the
# three declensions, as far as a stem the two forms share leaves them.
CASE_ENDINGS = {"", "α", "ας", "αν", "αι", "αις", "ων", "ης", "η", "ην", "ος", "ου", "ω", "ον",
                "οι", "ους", "οις", "ε", "ες", "ι", "ιν", "ις", "εως", "ει", "εις", "εσι", "εσιν",
                "υ", "υς", "υν", "ν", "ς", "σι", "σιν", "ως"}


def named_words(greek, entries):
    """Words this verse prints that one of its names entries names, wherever they stand.

    Capitals find most names, but not two kinds. An obvious transliteration carries its
    meaning as a proper name does (CLAUDE.md), yet the edition may print it in lower
    case — τὰ χερουβιμ, GEN 3:24. And a name that opens a sentence has a capital that
    proves nothing — Αδαμ δὲ ἔγνω, GEN 4:1. The entry names both, and they count.
    """
    words = PUNCT.sub(" ", greek).split()
    return [w for w in words if any(matches(w, e.get("greek", "")) for e in entries)]


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
        candidates += [w for w in named_words(verse["greek"], entries) if w not in candidates]
        found_any = found_any or bool(candidates)
        used = set()

        for candidate in candidates:
            # the entry for this very form first: a verse can print two cases of one name, each
            # with its own entry (Σαρα and Σαρας, GEN 16:2)
            entry = (next((e for e in entries if e["greek"] == candidate), None)
                     or next((e for e in entries if matches(candidate, e["greek"])), None))
            key = next((k for k in glossed if matches(candidate, k)), None)
            if key is not None and entry is not None and entry["anchored"] not in glossed[key]:
                # the same Greek form naming someone else, with another English name:
                # Σεννααρ the land at GEN 14:1 and the king at 14:2. It is glossed anew.
                key = None

            marker = "[[name:%s]]" % (entry["greek"] if entry else candidate)
            if key is None:
                if entry is None:
                    rep.fail("names", ref,
                             "%s is a proper name on first occurrence with no entry in names"
                             % candidate)
                    continue
                if entry.get("bare"):
                    rep.fail("names", ref,
                             "%s is marked bare here, but this is its first occurrence in "
                             "the chapter, where it carries its gloss" % candidate)
                used.add(entry["greek"])
                glossed.setdefault(entry["greek"], {})[entry["anchored"]] = ref
                if marker not in verse["reading"]:
                    rep.fail("names", ref, "%s is glossed here first but the reading "
                                           "carries no %s" % (candidate, marker))
            elif entry is not None:
                used.add(entry["greek"])
                first = glossed[key][entry["anchored"]]
                if first == ref and not entry.get("bare"):
                    # the same name again in the verse that glosses it: the renderer
                    # glosses the first marker only
                    continue
                if not entry.get("bare"):
                    rep.fail("names", ref,
                             "%s was already glossed at %s; a later occurrence takes an "
                             "entry marked bare" % (candidate, first))
                elif marker not in verse["reading"]:
                    rep.fail("names", ref, "%s has a bare entry here but the reading "
                                           "carries no %s" % (candidate, marker))

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

# Words a chain carries because of the form or the case it is in, not because the lexicon
# gave them: auxiliaries, articles, the prepositions a case-ending forces into English,
# and the pronouns that follow concord. Two chains that differ only in these are one word
# written twice, which is the chain following the form — the point of it, not drift.
GRAMMAR = {
    "the", "a", "an", "of", "to", "in", "into", "on", "at", "by", "for", "with", "from",
    "is", "are", "was", "were", "be", "been", "being", "am", "will", "would", "shall",
    "should", "may", "might", "can", "could", "must", "have", "has", "had", "having",
    "do", "does", "did", "let", "not", "and", "or", "that", "it", "its", "he", "him",
    "his", "she", "her", "they", "them", "their", "we", "us", "our", "i", "my", "me",
    "you", "your", "one", "ones", "oneself", "himself", "herself", "itself",
    "themselves", "myself", "yourself", "yourselves", "ourselves", "who", "whom", "what", "one's",
    "which", "this", "these", "those", "there", "so", "as", "own",
}

# English's irregular parts, so that a chain wearing the form the Greek calls for still
# reads as the lexicon's own word: the entry says `take`, the chain says `took`.
IRREGULAR = {
    "took": "take", "taken": "take", "gave": "give", "given": "give", "went": "go",
    "gone": "go", "came": "come", "made": "make", "brought": "bring", "stood": "stand",
    "strove": "strive", "striven": "strive", "broke": "break", "broken": "break",
    "sheaves": "sheaf",  # δράγμα, singular beside plural at GEN 37:7
    "stole": "steal", "stolen": "steal", "felt": "feel", "held": "hold", "kept": "keep",
    "left": "leave", "laid": "lay", "lain": "lie", "led": "lead", "said": "say",
    "saw": "see", "seen": "see", "sent": "send", "sat": "sit", "slept": "sleep",
    "spoke": "speak", "spoken": "speak", "paid": "pay", "ran": "run", "rose": "rise",
    "risen": "rise", "sold": "sell", "sought": "seek", "taught": "teach", "told": "tell",
    "thought": "think", "threw": "throw", "thrown": "throw", "understood": "understand",
    "wore": "wear", "worn": "wear", "won": "win", "wrote": "write", "written": "write",
    "knew": "know", "known": "know", "grew": "grow", "grown": "grow", "drew": "draw",
    "drawn": "draw", "fell": "fall", "fallen": "fall", "found": "find", "got": "get",
    "gotten": "get", "heard": "hear", "hid": "hide", "hidden": "hide", "bore": "bear",
    "borne": "bear", "born": "bear", "began": "begin", "begun": "begin", "bound": "bind",
    "bought": "buy", "built": "build", "caught": "catch", "chose": "choose",
    "chosen": "choose", "drove": "drive", "driven": "drive", "ate": "eat", "eaten": "eat",
    "forgot": "forget", "forgotten": "forget", "froze": "freeze", "hung": "hang",
    "meant": "mean", "met": "meet", "lost": "lose", "shook": "shake", "shaken": "shake",
    "shone": "shine", "shot": "shoot", "sang": "sing", "sank": "sink",
    "sprang": "spring", "struck": "strike", "swore": "swear", "sworn": "swear",
    "smote": "smite", "smitten": "smite", "stank": "stink", "smelt": "smell",
    "swept": "sweep", "tore": "tear", "torn": "tear", "woke": "wake",
    "children": "child", "men": "man", "women": "woman", "feet": "foot",
    "teeth": "tooth", "oxen": "ox", "geese": "goose", "mice": "mouse", "lives": "life",
    "wives": "wife", "knives": "knife", "leaves": "leaf", "calves": "calf",
    "halves": "half", "thieves": "thief", "loaves": "loaf", "selves": "self",
    "slew": "slay", "slain": "slay", "begot": "beget", "begotten": "beget", "sped": "speed",
    "died": "die", "dying": "die", "oversaw": "oversee", "overseen": "oversee", "lying": "lie",
}

# The project's own wording for verbal aspect (CLAUDE.md). It is grammar written into the
# text, not a sense the lexicon gave, so it is set aside like an auxiliary — a perfect
# participle and an aorist one may share an English headword, and then only this differs.
ASPECT = re.compile(r"\band (?:it )?(?:stands?|standing|remains?|remaining|continues?|"
                    r"continuing|holds?|holding)\b(?![^,]*\bwith\b)[^,]*")


def stem(token):
    """One English word cut back to a stem an entry and a chain both reach."""
    token = IRREGULAR.get(token, token)
    # A plural ending comes off and lets one more come off after it — `beings` to `being`
    # to `be`. A verb ending is the last: taking an `s` from what `-ed` left cut `deposed`
    # to `depo` where `depose` stays `depos`, and two forms of one word read as two words.
    for _ in range(2):
        if len(token) > 5 and token.endswith(("ies", "ied")):
            token = token[:-3] + "y"
            break
        elif len(token) > 4 and token.endswith("ing") and re.search(r"[aeiouy]", token[:-3]):
            # `bringing` to `bring`, but `bring` and `thing` are words of their own: what is
            # left without a vowel was never an `-ing` ending
            token = token[:-3]
            break
        elif len(token) > 4 and token.endswith("ed"):
            token = token[:-2]
            break
        elif len(token) > 4 and token.endswith("es"):
            token = token[:-2]
        elif len(token) > 3 and token.endswith("s") and not token.endswith("ss"):
            token = token[:-1]
        else:
            break
    if len(token) > 3 and token.endswith("e"):
        token = token[:-1]
    if len(token) > 3 and token[-1] == token[-2] and token[-1] not in "aeiou":
        token = token[:-1]
    return token


def senses(chain):
    """What a chain says, as a multiset, with what only the form put there set aside.

    A multiset and not a set: μερίς reads `a part, a portion, … a part and division and
    class`, and losing one of the two `part`s is a sense lost.
    """
    out = collections.Counter()
    prev = None
    text = ASPECT.sub("", chain).lower()
    for m in re.finditer(r"[a-zA-Z']+", text):
        token = m.group()
        # the article's noun follows its gender, `the one coming in second` beside `the
        # thing coming in second`: one is grammar already, and so is the other where words
        # follow it in the item (δεύτερος at GEN 32:9 and EXO 27:15). Where the item ends
        # on it, `the subject of speech and the thing`, the thing is a sense.
        carried = (prev == "the" and token in ("thing", "things")
                   and re.match(r" [a-z]", text[m.end():m.end() + 2]))
        prev = token
        if token in GRAMMAR or carried:
            continue
        token = stem(token)
        if token and token not in GRAMMAR:
            out[token] += 1
    return out


def content(text):
    """The stems a gloss or a chain item says, what only the form put there set aside."""
    return set(senses(text))


def leading_grammar(item):
    """The words an item opens with that only the form put there: `of the`, `we will`."""
    out = []
    for token in item.split(" "):
        # the article's noun goes with the article: `the things going into and entering`
        if token.lower() not in GRAMMAR and not (out and token in ("thing", "things")):
            break
        out.append(token)
    return out


def split_runs(chain, card):
    """Where a chain splits one translation of its card across items: [(first, last)].

    Middle Liddell gives a sense as a run of words in one translation — σταθμός *a
    dwelling, abode*, κιβωτός *a wooden box, chest, coffer* — and the run is one sense with
    several English words for it. The chain keeps it as one item, the words joined with
    *and*: `dwelling and abode`. Split into items of their own, `face, visage, countenance`,
    each word reads as a sense of its own, and the commas no longer tell the reader where
    the entry's senses part.

    A run is found where its words fall on consecutive items, in order, each item saying
    exactly the words of the run it holds and nothing else: a word the chain put somewhere
    else, or dropped, is not this check's to decide. Nor is an item another sense of the
    card says by itself — ἀκούω gives *to have hearing of* alone and *to hear of, hear tell
    of* as a run, and `had hearing of` is the first — or a stretch two runs both reach.
    """
    items = chain.split(", ")
    # the article's noun, `the things going into`, is the form's and not the entry's; but
    # `things which are eaten` is the entry's `that which is eaten`, so an item is read both
    # with the opening noun and without it
    said = [content(item) for item in items]
    bare = [content(re.sub(r"^(?:of |to )?(?:the )?(?:things?|ones?) ", "", item)) for item in items]
    alone = [content(sense) for sense in card if len(re.split(r",\s*", sense)) == 1]
    found = []
    for sense in card:
        pieces = [content(p) for p in re.split(r",\s*", sense)]
        pieces = [p for p in pieces if p]
        if len(pieces) < 2:
            continue
        for start in range(len(items)):
            at, acc, ok = start, set(), True
            for piece in pieces:
                if at >= len(items):
                    ok = False
                    break
                acc |= piece
                if acc in (said[at], bare[at]):
                    at, acc = at + 1, set()
                elif not (acc < said[at] or acc < bare[at]):
                    ok = False
                    break
            if (ok and not acc and at - 1 > start
                    and not any(said[i] in alone or bare[i] in alone for i in range(start, at))):
                found.append((start, at - 1))
                break
    found = set(found)
    return sorted(r for r in found if not any(o != r and o[0] <= r[1] and r[0] <= o[1]
                                              for o in found))


def join_runs(chain, card):
    """The chain with each split run joined into one item, its shared opening said once.

    The perfect's formula comes once, at the end of the joined item, where it stood on the
    item that carried it: `has talked and chatted and prattled and babbled and it stands
    so`. Anywhere inside, it would close the item early for every check that reads one.
    """
    for lead in MERGED_LEAD:
        if chain.startswith(lead):
            return lead + join_runs(chain[len(lead):], card)
    items = chain.split(", ")
    for first, last in reversed(split_runs(chain, card)):
        aspect = ASPECT.search(items[first])
        parts = [ASPECT.sub("", item).rstrip() for item in items[first:last + 1]]
        head = leading_grammar(parts[0])
        joined = parts[0]
        for item in parts[1:]:
            words = item.split(" ")
            n = 0
            while n < len(head) and n < len(words) - 1 and words[n] == head[n]:
                n += 1
            joined += " and " + " ".join(words[n:])
        if aspect:
            joined += " " + aspect.group(0).strip()
        items[first:last + 1] = [joined]
    return ", ".join(items)


def unit_cards(book, chapter, verses):
    """Each unit of a chapter with the full card of the word it opens.

    Yields (verse, head, chain, field, card); the card is None where it cannot be had — a
    preposition, read by its case's section; a formula word; a word the morphology does not
    hold where the unit says.
    """
    import words
    if not _ENTRIES:
        _ENTRIES.append(words.load_middle_liddell())
    tokens = words.nt_tokens(book, chapter) if book in words.NT else words.lxx_tokens(book, chapter)
    for verse in verses:
        number = words.verse_key(verse["ref"])
        theirs = (tokens or {}).get(number, [])
        nth = collections.Counter()
        for head, chain, field in units(verse["reading"]):
            word = lemmas(field)[-1]
            k, nth[word] = nth[word], nth[word] + 1
            card = None
            if " + " not in field.split(";")[-1] and word not in FORMULA_LEMMAS:
                places = [t for t in theirs if t[1] == word]
                if k < len(places):
                    form, lemma, code = places[k][:3]
                    card = words.lexicon_senses(_ENTRIES[0], lemma, code, form)
                    if card is None:
                        card = words.LSJ.get(lemma)
            yield verse, head, chain, field, card


def check_runs(book, chapter, verses, rep):
    """A run of words in one translation of the card is one item of the chain."""
    before = rep.failed
    count = 0
    for verse, head, chain, field, card in unit_cards(book, chapter, verses):
        if not card:
            continue
        count += 1
        for first, last in split_runs(chain, card):
            items = chain.split(", ")
            rep.fail("runs", verse["ref"], "%s `%s` splits one translation across `%s` — join "
                     "it with and" % (lemmas(field)[-1], head, ", ".join(items[first:last + 1])))
    rep.done("runs", "%d units, each translation one item" % count, before)


def chains_that_drifted(seen):
    """(lemma, headword[, card]) -> {chain: ref}  ->  the groups that lost a sense.

    One word in one form reads one way. A chain may still wear the form the Greek calls
    for — singular beside plural, imperative beside aorist — and that is not drift. What
    it may not do is say less than another chain of the same word says: everything the
    shorter one says the longer one says too, and the longer says more.

    Counting senses is not enough to see that. `took, received, took hold of and grasped
    and seized` and `took, received, took hold of and seized` carry three commas each,
    and the second has lost `grasped`.

    A third item in the key is the card: the senses the lexicon gives that form. Two forms
    the lexicon reads differently are not one form drifting — δίδωμι's present stem has
    *to be ready to give, to offer*, which its aorist has not, and διδόναι and δοῦναι are
    both `to give`.
    """
    out = []
    for key, chains in sorted(seen.items(), key=lambda kv: tuple(map(str, kv[0]))):
        lemma, head = key[:2]
        if len(chains) < 2:
            continue
        keyed = {c: senses(c) for c in chains}
        # one says less than the other; or each says something the other does not, which
        # is two chains each having lost what the other kept — πόθεν read `from what
        # country` in one verse and `how can it be` in another, and neither is the entry
        pairs = [(a, b) for a in chains for b in chains
                 if a != b and keyed[a] != keyed[b]
                 and (not (keyed[a] - keyed[b])
                      or (set(keyed[a]) - set(keyed[b]) and set(keyed[b]) - set(keyed[a])))]
        if pairs:
            out.append((lemma, head, sorted(chains.items(), key=lambda kv: kv[1])))
    return out


def check_chains(targets, rep):
    """One word in one form reads one way.

    Each unit names the Greek word it opens, so the comparison is per lemma, not per
    headword: `take` is both λαμβάνω and δέχομαι, and their chains share nothing after
    the first gloss. Within one lemma and one headword the chain must be the same
    wherever it stands, or the range the reader is given depends on which chapter they
    opened. Where the word-by-word layer shows the form's card, units are compared only
    with units the lexicon gives the same senses.
    """
    before = rep.failed
    seen = {}
    for book, chapter in targets:
        path = render.DATA / book / ("%d.json" % chapter)
        if not path.exists():
            continue
        layer = render.DATA / book / ("%d.words.json" % chapter)
        lay = ({v["ref"]: v["words"] for v in
                json.loads(layer.read_text(encoding="utf-8")).get("verses", [])}
               if layer.exists() else {})
        for verse in json.loads(path.read_text(encoding="utf-8")):
            words = lay.get(verse["ref"]) or []
            nth = collections.Counter()
            count = collections.Counter(lemmas(lemma)[-1] for _, _, lemma in units(verse["reading"]))
            for head, chain, lemma in units(verse["reading"]):
                word = lemmas(lemma)[-1]
                k, nth[word] = nth[word], nth[word] + 1
                places = [words[i] for i in unit_places(words, word, count[word])]
                card = tuple(places[k].get("senses") or ()) if k < len(places) else None
                seen.setdefault((lemma, head, card), {}).setdefault(chain, verse["ref"])
    for lemma, head, where in chains_that_drifted(seen):
        short, long_ = min(where, key=lambda kv: sum(senses(kv[0]).values())), \
            max(where, key=lambda kv: sum(senses(kv[0]).values()))
        lost = senses(long_[0]) - senses(short[0])
        rep.fail("chains", short[1],
                 "%s `%s` says less here than at %s — %s — one word, one range"
                 % (lemma, head, long_[1], ", ".join(sorted(lost))))
    rep.done("chains", "%d lemma-and-headword groups, no drift" % len(seen), before)


# The English a preposition that merges into its object's unit leads that unit with. It is
# the preposition's range, not the word's, and a chain is measured without it.
MERGED_LEAD = ("within, inside of, and by means of ", "up to, up along, and throughout ")

# θεός reads by the article's two formulas, fixed wordings of different length, and not by
# a range drawn from its entry; Ἐν ἀρχῇ, at GEN 1:1 and JHN 1:1, by the wording that keeps
# the quotation visible.
FORMULA_LEMMAS = {"θεός"}
FORMULA_CHAINS = ("within, inside of, and by means of the first moment",)


def range_of(chain):
    """How many senses a chain gives, a merged preposition's English set aside."""
    for lead in MERGED_LEAD:
        if chain.startswith(lead):
            chain = chain[len(lead):]
    return len(chain.split(", "))


_ENTRIES = []


def opening(word, chain):
    """The sense of its entry a noun or adjective opens with, where that is not the first.

    A word used as a noun takes the first noun sense: τὸ καλόν is *beauty*, τὸ κακόν *evil*,
    τὰ πάντα *all things*, and each is a range of its own beside the adjective's.
    """
    import words
    if not _ENTRIES:
        _ENTRIES.append(words.load_middle_liddell())
    for lead in MERGED_LEAD:
        if chain.startswith(lead):
            chain = chain[len(lead):]
    first = re.sub(r"^(?:of |to )?(?:the |a |an )?", "", chain.split(", ")[0]).lower()
    for i, sense in enumerate(words.lexicon_senses(_ENTRIES[0], word["lemma"]) or []):
        core = re.sub(r"^(?:to |the |a |an )", "", re.split(r"[,;:]", sense)[0].strip()).lower()
        # a run joined into the first item: `the existing circumstances and present advantages`
        if first == core or first.startswith(core + " and "):
            return "" if i == 0 else core
    return ""


def range_key(word, chain=""):
    """What decides a word's range: its lemma, part of speech, voice or number, and the
    senses its entry gives that form, which the word-by-word card shows — and for a noun
    or adjective, the sense it opens with where it is used as a noun."""
    parse = word["parse"].split(" · ")
    voice = next((v for v in ("middle/passive", "passive", "middle", "active") if v in parse), "")
    number = "" if parse[0] == "verb" else next((n for n in ("singular", "plural") if n in parse), "")
    degree = next((d for d in ("comparative", "superlative") if d in parse), "")
    # a participle the article makes a noun of opens its own range as a noun does: τὰ
    # ὑπάρχοντα is `the existing circumstances`, and ὑπάρχει `begins`
    use = opening(word, chain) if parse[0] != "verb" or "participle" in parse else ""
    return (word["lemma"], parse[0], voice, number, degree, tuple(word.get("senses") or ()),
            word.get("more"), use)


def check_ranges(targets, rep):
    """One word reads one range in every form it takes.

    The chain check compares units that share a headword, so ἐπιβάλλω could read five
    senses as `threw` and eleven as `you may throw`, and γυνή could drop *the mortal woman*
    from every articular form while the anarthrous kept it, and nothing saw either. Here
    each unit is paired with the word it opens, and units the lexicon gives the same senses
    — one lemma, one voice, one number, the same card — must give the reader as many of
    them, whatever tense, person or case they wear. Counting is not the whole of sameness,
    which the chain check holds within a headword; it is what can be held across headwords.
    """
    before = rep.failed
    groups = collections.defaultdict(list)
    for book, chapter in targets:
        path = render.DATA / book / ("%d.json" % chapter)
        layer = render.DATA / book / ("%d.words.json" % chapter)
        if not (path.exists() and layer.exists()):
            continue
        lay = {v["ref"]: v["words"] for v in
               json.loads(layer.read_text(encoding="utf-8")).get("verses", [])}
        for verse in json.loads(path.read_text(encoding="utf-8")):
            words = lay.get(verse["ref"]) or []
            nth = collections.Counter()
            count = collections.Counter(lemmas(field)[-1] for _, _, field in units(verse["reading"]))
            for head, chain, field in units(verse["reading"]):
                word = lemmas(field)[-1]
                k, nth[word] = nth[word], nth[word] + 1
                if (" + " in field.split(";")[-1] or word in FORMULA_LEMMAS
                        or chain.startswith(FORMULA_CHAINS)):
                    continue
                places = [words[i] for i in unit_places(words, word, count[word])]
                if k < len(places):
                    groups[range_key(places[k], chain)].append(
                        (range_of(chain), verse["ref"], head))
    for key, where in groups.items():
        top = max(where)
        told = set()
        for n, ref, head in where:
            if n < top[0] and (head, n) not in told:
                told.add((head, n))
                rep.fail("ranges", ref, "%s `%s` gives %d senses, `%s` at %s gives %d — one "
                         "word, one range in every form" % (key[0], head, n, top[2], top[1], top[0]))
    rep.done("ranges", "%d groups of one word's forms, each one range" % len(groups), before)


def check_prepositions(targets, rep):
    """A preposition does not inflect, so its chain cannot follow the form.

    The chain check lets two units of one word read differently when the headword
    differs, because the chain follows the form. A preposition has one form. Within one
    lemma and one case its chain is therefore the same everywhere or it is drift, and the
    case is what decides the sense: Middle Liddell gives each case its own section.
    """
    before = rep.failed
    seen = {}
    for book, chapter in targets:
        path = render.DATA / book / ("%d.json" % chapter)
        if not path.exists():
            continue
        for verse in json.loads(path.read_text(encoding="utf-8")):
            for head, chain, lemma in units(verse["reading"]):
                if " + " not in lemma:
                    continue
                seen.setdefault(lemma, {}).setdefault(chain, (head, verse["ref"]))
    for lemma, chains in sorted(seen.items()):
        if len(chains) < 2:
            continue
        where = sorted(chains.items(), key=lambda kv: kv[1][1])
        rep.fail("prepositions", where[0][1][1],
                 "%s reads `%s` here and `%s` at %s — a preposition has one form, so one "
                 "case is one chain" % (lemma, where[0][1][0], where[1][1][0], where[1][1][1]))
    rep.done("prepositions", "%d preposition-and-case groups, one chain each" % len(seen),
             before)


def check_unit_words(book, chapter, verses, rep):
    """Every unit opens a word the verse actually holds.

    The lemma a unit names is checked against the chapter's own morphology, so a unit
    cannot claim a word that is not there. Without this the lemma would be an assertion
    nothing tests, and the chain check would be comparing whatever it was given.
    """
    before = rep.failed
    path = render.DATA / book / ("%d.words.json" % chapter)
    if not path.exists():
        rep.note("unit words", "no word-by-word layer for this chapter yet")
        return
    held = {v["ref"]: collections.Counter(w["lemma"] for w in v["words"])
            for v in json.loads(path.read_text(encoding="utf-8")).get("verses", [])}
    n = 0
    for verse in verses:
        there = held.get(verse["ref"])
        if there is None:
            continue
        own = units(verse["reading"])
        n += len(own)
        # a preposition's unit names the case it governs as well, because Middle
        # Liddell gives each case its own section and the sense comes from there
        claimed = collections.Counter(w for _, _, lemma in own for w in lemmas(lemma))
        for head, chain, lemma in own:
            for word in lemmas(lemma):
                if word not in there:
                    rep.fail("unit words", verse["ref"],
                             "`%s` says it opens %s, which is not a word of this verse"
                             % (head, word))
        # and no oftener than the verse holds it. Testing only that a word is there
        # let GEN 7:16 file εἰσπορεύομαι's unit under εἰσέρχομαι, which the verse also
        # holds, in a unit of its own — two units, one word, and nothing to see it.
        for word, over in (claimed - there).items():
            rep.fail("unit words", verse["ref"],
                     "%d unit%s open %s, which this verse holds %d time%s"
                     % (claimed[word], "" if claimed[word] == 1 else "s", word,
                        there[word], "" if there[word] == 1 else "s"))
    rep.done("unit words", "%d units name a word their verse holds" % n, before)


# Words that carry no sense of their own, so nothing about them is left shut: the
# article, and the copula the project renders by its own formula. ἐν was here too, as the
# preposition that merges into its object's unit; but where there is no unit to merge
# into — a name, a pronoun, a plain noun — it takes its own, and 43 had been left as a
# bare *in* under the exemption. It is opened like any preposition now, merged or alone.
FREE_WORDS = {"ὁ", "εἰμί"}

# The parts of speech the rule is about. A particle is in it too, opened by its parse
# as a preposition is opened by the case it governs: καί read as an adverb takes the
# adverbial senses, καί read as the connective is the conjunction and stays plain.
CONTENT_WORDS = ("noun", "verb", "adjective", "adverb", "preposition")


def opens_more(word):
    """Whether a word's entry says anything its headword would not already carry.

    The headword is the first translation of the entry's first sense, so what a chain
    adds is whatever else the entry says — a second sense, or simply more words in the
    first one. κιβωτός has one sense and still wants a unit, because that sense reads
    `a wooden box, chest, coffer` and the headword keeps only the box.

    `more` is how many senses the word-by-word layer left out; any of them is more.
    """
    got = word.get("senses") or []
    if not got:
        return False                       # no entry: there is nothing to open it with
    if word.get("more"):
        return True
    whole = set()
    for sense in got:
        whole |= set(senses(sense))
    return bool(whole - set(senses(re.split(r"[,;]", got[0])[0])))



def unit_places(words, word, count):
    """Which occurrences of `word` a verse's `count` units open, in order.

    Units are paired with their words in order, which holds while a verse has a unit
    for every occurrence. Where it has fewer, the units are the occurrences whose entry
    says more than its headword: δέρρις is one sense in the singular and two in the
    plural, and EXO 26:8 and 26:12 hold the singular, plain, before the plural, a unit.
    """
    places = [i for i, w in enumerate(words) if w["lemma"] == word]
    if count >= len(places):
        return places
    chosen = [i for i in places if opens_more(words[i])][:count]
    chosen += [i for i in places if i not in chosen][:count - len(chosen)]
    return sorted(chosen)

def check_one_sense(book, chapter, verses, rep):
    """A word is a unit exactly when its entry says more than its headword does.

    Both ways, because either way round is a word read wrong. A word whose entry says
    more and stands as plain text is a range the reader never sees — that was 1,038
    words of Genesis, and it was an accident, not a decision. A unit whose chain is
    word for word its headword prints `headword — headword —` and says nothing the
    plain text would not.

    Grammar is not in it: the article and εἰμί are rendered by the project's own
    formulas, and a particle's entry is a list of constructions rather than a range.

    Units are counted, not just seen: one unit for a word opens one occurrence of it.
    A set let one ἐν opened in a verse stand for every ἐν there (GEN 7:11 had two, and
    one unit).
    """
    before = rep.failed
    path = render.DATA / book / ("%d.words.json" % chapter)
    if not path.exists():
        rep.skip("one sense", "no word-by-word layer for this chapter yet")
        return
    layer = {v["ref"]: v["words"] for v in
             json.loads(path.read_text(encoding="utf-8")).get("verses", [])}
    shut = kept = 0
    for verse in verses:
        words = layer.get(verse["ref"])
        if words is None:
            continue
        own = units(verse["reading"])
        claimed = collections.Counter(w.split(" + ")[0] for _, _, lemma in own
                                      for w in lemmas(lemma))

        content = [w for w in words
                   if not (w.get("lexicon") == "name" or w["lemma"] in FREE_WORDS
                           or w["parse"].split(" ·")[0] not in CONTENT_WORDS)]
        # a unit opens the occurrence that needs one first: δέρρις is one sense in the
        # singular and two in the plural, and EXO 26:12 holds the plural after a singular
        opened = set()
        for i, word in enumerate(content):
            if claimed[word["lemma"]] > 0 and opens_more(word):
                claimed[word["lemma"]] -= 1
                opened.add(i)
        for i, word in enumerate(content):
            if i in opened:
                continue
            if claimed[word["lemma"]] > 0:
                claimed[word["lemma"]] -= 1
                continue
            if opens_more(word):
                shut += 1
                rep.fail("one sense", verse["ref"],
                         "%s (%s) is plain text, but its entry says more than "
                         "`%s` does — open it as a unit"
                         % (word["form"], word["lemma"], word["senses"][0]))

        heads = [anchor for anchor, _, _ in own]
        heads += [item["anchor"] for item in ANCHORS]
        for anchor, chain, lemma in own:
            if chain.strip() != anchor.strip():
                continue
            # Flattening a unit whose English holds another unit's headword would
            # write that headword as plain text — `made` inside `made swear`. The
            # unit is what tells the two apart, so it stays.
            if any(other != anchor
                   and re.search(r"\b%s\b" % re.escape(other), anchor, re.I)
                   for other in heads):
                kept += 1
                continue
            rep.fail("one sense", verse["ref"],
                     "`%s` (%s) is a unit whose chain is word for word its headword; "
                     "it adds nothing, so write it as plain text" % (anchor, lemma))
    rep.done("one sense", "%d verses; %d units kept for a headword they hold"
             % (len(layer), kept), before)


# Perseus's own markup, audited. Middle Liddell writes "Lat. <latin>, <English>", and
# the encoding wraps the whole run in one Latin element, English and all, so the loader
# never sees that translation. Nineteen words had lost one, five of them their own first
# sense. The reading does not show it — a chain written by somebody reading the entry's
# text is right, and only the senses the loader could see were wrong — so nothing in the
# data can catch it. This reads the lexicon instead, and every site must be settled:
# named in MARKUP_LOST, which restores the English, or in LATIN_ONLY, which says there
# is none to restore.
LATIN_RUN = re.compile(r'<foreign[^>]*lang="la"[^>]*>(.*?)</foreign>', re.S)


def check_markup(targets, rep):
    before = rep.failed
    try:
        import words as W
    except Exception as exc:                      # pragma: no cover
        rep.skip("markup", "build/words.py would not load: %s" % exc)
        return
    source = SOURCES / "middle-liddell/Perseus_text_1999.04.0058.xml"
    if not source.exists():
        rep.skip("markup", "sources/middle-liddell is not here")
        return
    xml = source.read_text(encoding="utf-8")
    bodies = {}
    for m in re.finditer(r'<entry\b[^>]*\bkey="([^"]+)"[^>]*>(.*?)</entry>', xml, re.S):
        bodies.setdefault(m.group(1), m.group(2))
        bodies.setdefault(re.sub(r"\d+$", "", m.group(1)), m.group(2))

    wanted = set()
    for book, chapter in targets:
        path = render.DATA / book / ("%d.words.json" % chapter)
        if not path.exists():
            continue
        for verse in json.loads(path.read_text(encoding="utf-8")).get("verses", []):
            for word in verse["words"]:
                if word["lexicon"] != "name":
                    wanted.add(word["lemma"])

    settled = set(W.LATIN_ONLY) | {re.sub(r"\d+$", "", k) for k in W.MARKUP_LOST}
    seen = 0
    for lemma in sorted(wanted):
        key = W.SPELLING.get(W.beta(lemma), W.beta(lemma))
        key = W.ENTRY.get(key, key)
        body = bodies.get(key)
        if not body:
            continue
        start = body.find("<sense")
        first = re.search(r"<sense\b[^>]*>(.*?)</sense>", body[start:], re.S) if start >= 0 else None
        if not first:
            continue
        for run in LATIN_RUN.finditer(first.group(1)):
            inner = re.sub(r"<[^>]+>", "", run.group(1)).strip()
            if "," not in inner:
                continue                          # one Latin word: no English to lose
            seen += 1
            if re.sub(r"\d+$", "", key) not in settled:
                rep.fail("markup", lemma,
                         "the entry's first sense reads `Lat. %s`, and the whole of it is "
                         "inside the Latin element — if any of that is English, name it in "
                         "MARKUP_LOST; if it is Latin throughout, name it in LATIN_ONLY"
                         % inner[:60])
    # Greek does the same where Middle Liddell names a thing by its Greek word: the <tr> ends
    # on "made of", "in the", "as a", and the word that finishes it is a Greek element after
    # it — or the element is inside the <tr> and reaches the card as Beta Code. Every site
    # among the corpus's words is settled in GREEK_LOST, which restores the sense, or in
    # GREEK_AFTER, which says the gloss was whole and the Greek is an example's.
    greek = set(W.GREEK_LOST) | set(W.GREEK_AFTER)
    cut = 0
    for lemma in sorted(wanted):
        key = W.SPELLING.get(W.beta(lemma), W.beta(lemma))
        key = W.ENTRY.get(key, key)
        body = bodies.get(key)
        if not body or body.find("<sense") < 0:
            continue
        for t in GREEK_CUT.finditer(body[body.find("<sense"):]):
            text = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", t.group(1))).strip()
            if not ('lang="greek"' in t.group(1) or (t.group(2) and ENDS_SHORT.search(text))):
                continue
            cut += 1
            if re.sub(r"\d+$", "", key) not in greek:
                rep.fail("markup", lemma,
                         "the translation `%s` stops at a Greek word, or holds one — if the "
                         "word finishes it, restore it in GREEK_LOST; if the gloss is whole, "
                         "name it in GREEK_AFTER" % text[:60])
    rep.done("markup", "%d first-sense Latin runs and %d translations a Greek word cuts, all "
             "settled" % (seen, cut), before)


GREEK_CUT = re.compile(r'<tr\b[^>]*>(.*?)</tr>\s*(<foreign[^>]*lang="greek")?', re.S)
ENDS_SHORT = re.compile(r"\b(?:of|the|a|an|in|to|for|with|by|at|on|from|into|as)$")


STRANDED = re.compile(r"(?<![\w\-])the\s+\[\[(?!name:)([^|\]]+)\|[^|\]]+\|([^|\]]+)\]\]")
ARTICLE_NOUN = re.compile(r"^(?:of |to |with )?the (ones|one|things|thing)(?: |$)")
# A plain case marker before a unit or an article's noun that carries the same marker:
# `to [[to the house|…]]`, `of of the ones`. Inside one unit it is the gloss's own word —
# ἀλλογενής is *of another race*, and its genitive *of of another race* — and stays.
DOUBLED = re.compile(r"(?<![\w\-|\[])(of|to) (?:\[\[(?!name:))?\1 (?=the |\w)")
# A preposition read as plain text, its one translation ending in the word a case marker
# uses: ἔναντι is *in the presence of*, and the genitive after it opens with its own *of*,
# as ἐναντίον's unit, *in the presence of*, stands before *of lord*. That *of* is the gloss's.
# ἐνωτίζομαι is *to hearken to*, one translation, and the dative after it opens with its own *to*
# (EXO 15:26).
PLAIN_LEADS = ("in the presence ", "hearken ")
# A gloss that opens with the word a case marker uses: εὐώνυμος is *of good name* and *of good
# omen*, and its genitive marks the case before the gloss's own *of* — `of of good name` (EXO 14:22);
# πένης, as an adjective, is *of a poor man*, and its genitive reads `of of a poor man` (EXO 23:6);
# λιθουργικός is *of or for a λιθουργός*, and its genitive `of of or for a lithourgos` (EXO 28:11).
# εἰκοσαετής is *of twenty years*, and its genitive `of of twenty years` (EXO 30:14). πενθικός is *of or for
# mourning*, and ἐν merged into it ends on its own *by means of*: `… and by means of of or for mourning` (EXO 33:4).
# ἑβδομάς is *of seven years, a septenary*, and its genitive `of of seven years and septenaries` (EXO 34:22).
GLOSS_LEADS = ("of of good name", "of of good omen", "of of a poor man", "of of or for a lithourgos",
               "of of twenty years", "of of or for mourning", "of of seven years")
# What stands in a reading, in order: a unit (its anchor), a name, or plain text.
PIECES = re.compile(r"\[\[name:[^\]]+\]\]|\[\[(?!name:)([^|\]]+)\|[^|\]]+\|[^|\]]+\]\]|[^\[]+")
THE_LEADS = re.compile(r"^(?:of |to )?the ")


def printed_before(pieces, n):
    """Whether the article has printed already just before piece `n`: in the unit before it
    (`[[of the mine]]`), in plain text over one word (`the two`), or before a name (`the
    [[name:Ροωβωθ]]`)."""
    back = [p for p in pieces[:n] if p.group(0).strip()]
    if not back:
        return False
    prev = back[-1]
    if prev.group(1) is not None:
        return bool(THE_LEADS.match(prev.group(1).strip()))
    if prev.group(0).startswith("[[name:"):
        return len(back) >= 2 and back[-2].group(1) is None and \
            re.search(r"(?<![\w\-])the\s*$", back[-2].group(0)) is not None
    return re.search(r"(?<![\w\-])the [\w\-]+\s*$", prev.group(0)) is not None


def shared_article(words, i):
    """Whether the noun at `i` stands under an article two words back, past a possessive, a
    numeral or a name in the same case and number: τοῦ ἐμοῦ λαοῦ, οἱ δύο ἄγγελοι, τὴν Ροωβωθ
    πόλιν."""
    if i < 2 or words[i]["parse"].split(" · ")[0] != "noun" or own_article_of(words, i):
        return False
    art, between = words[i - 2]["parse"].split(" · "), words[i - 1]["parse"].split(" · ")
    parse = words[i]["parse"].split(" · ")
    if art[0] != "article" or between[0] not in ("adjective", "noun"):
        return False
    return all([t for t in art if t in kind] == [t for t in parse if t in kind]
               for kind in (("nominative", "genitive", "dative", "accusative", "vocative"),
                            ("singular", "plural")))


def article_noun(parse):
    """The English noun an article over a participle carries, by gender and number."""
    p = parse.split(" · ")
    if "neuter" in p:
        return "things" if "plural" in p else "thing"
    return "ones" if "plural" in p else "one"


CASE_MARK = {"genitive": "of", "dative": "to"}
PIECE = re.compile(r"\[\[[^\]]*\]\]|[^\s\[]+")


def name_words(verse, words):
    """Each name marker in the reading with its word in the word-by-word layer: the next
    word of the same form not yet taken. None if a marker has no such word."""
    out, used = [], set()
    for m in render.NAME.finditer(verse["reading"]):
        i = next((k for k, w in enumerate(words)
                  if k not in used and w["form"] == m.group(1)), None)
        if i is None:
            return None
        used.add(i)
        out.append((m, i))
    return out


def own_article(words, i):
    """Whether the name at words[i] has an article of its own: the nearest word before it,
    past a particle (ὁ δὲ Ιακωβ), is an article in the name's case. An article in another
    case is not the name's — τὰ ὄρη τὰ Αραρατ, *the things of Ararat* — and the marker
    then goes after it."""
    case = lambda w: next((c for c in ("nominative", "genitive", "dative", "accusative",
                                        "vocative") if c in w["parse"].split(" · ")), None)
    # nor one in another gender: τῆς Κορε συναγωγῆς (EXO 38:22) is συναγωγῆς's article, with
    # the masculine name between them
    gender = lambda w: next((g for g in ("masculine", "feminine", "neuter")
                             if g in w["parse"].split(" · ")), None)
    k = i - 1
    while k >= 0 and words[k]["parse"].split(" · ")[0] in ("conjunction", "particle"):
        k -= 1
    if k < 0 or not words[k]["parse"].startswith("article") or case(words[k]) != case(words[i]):
        return False
    return None in (gender(words[k]), gender(words[i])) or gender(words[k]) == gender(words[i])


def marker_before(text, at, article=False):
    """The case marker printed before a name at `at` — past its `the`, where the name has
    an article of its own: `of`, `to`, or whatever plain word or unit stands there instead."""
    pieces = [p.rstrip(",;:") for p in PIECE.findall(text[:at])]
    if article and pieces and pieces[-1] == "the":
        pieces.pop()
    return pieces[-1] if pieces else ""


def check_name_cases(book, chapter, verses, rep):
    """A name marks its case as any noun does: the genitive *of*, the dative *to*. And its
    article prints, as every article does: τῷ Ιακωβ is *to the Jacob*. GEN 10 had set the
    article before a name unprinted, as English would, and some 334 places followed it;
    that was an exception made for English's sake, and is gone.

    A name prints only its own form, so the marker stands as plain text before it, and
    before the name's article where it has one — *the sons of Ησαυ*, *out of of Χαρραν*, *in
    to Εδωμ*, as GEN 2:7 reads *from of the earth*. An indeclinable name shows no case in
    its spelling; the case is the one the chapter's morphology gives it, which two passes
    have settled. Before this check names went both ways, 135 genitives marked and some 380
    not, because the pass that marked every noun's case read units and not names.
    """
    before = rep.failed
    path = render.DATA / book / ("%d.words.json" % chapter)
    if not path.exists():
        return
    lay = {v["ref"]: v["words"] for v in
           json.loads(path.read_text(encoding="utf-8")).get("verses", [])}
    seen = 0
    for verse in verses:
        words = lay.get(verse["ref"])
        if not words or not verse["reading"]:
            continue
        pairs = name_words(verse, words)
        if pairs is None:
            rep.fail("names", verse["ref"], "a name marker with no word of its form in the "
                     "word-by-word layer")
            continue
        for m, i in pairs:
            art = own_article(words, i)
            last = marker_before(verse["reading"], m.start())
            if art and last != "the":
                rep.fail("names", verse["ref"], "%s has its own article in the Greek, and "
                         "the article prints: `the %s`" % (m.group(1), m.group(1)))
            elif not art and last == "the":
                rep.fail("names", verse["ref"], "a `the` before %s, which has no article of "
                         "its own; an article in another case makes a noun of it, `the one "
                         "of %s`" % (m.group(1), m.group(1)))
            case = next((c for c in CASE_MARK if c in words[i]["parse"].split(" · ")), None)
            if not case:
                continue
            seen += 1
            got = marker_before(verse["reading"], m.start(), art)
            if got != CASE_MARK[case]:
                rep.fail("names", verse["ref"], "%s is %s; it reads `%s %s`, not `%s`"
                         % (m.group(1), case, CASE_MARK[case], m.group(1),
                            (got + " " if got else "") + m.group(1)))
    rep.done("names", "%d genitive and dative names, each marked, and every name's article "
             "printed" % seen, before)


# The particles that stand second in their clause and so may come between an article and
# its word: ὁ δὲ θεός, τὸ γὰρ ὕδωρ.
POSTPOSITIVE = {"δέ", "γάρ", "μέν", "οὖν", "τε", "γε"}


def own_article_of(words, i):
    """Whether the noun or adjective at `i` has an article of its own: one standing directly
    before it, past a postpositive particle, in its own case, number and gender.

    English gets an article where the Greek has one, and the unit carries it — τὸ σπέρμα σου
    is *the that which is sown of you*, as τὰ σά is *the thy property*. 66 units had let a
    gloss that opens with *that which* or *anything* stand in for the article, and the Greek
    article was lost.
    """
    parse = words[i]["parse"].split(" · ")
    if parse[0] not in ("noun", "adjective"):
        return False
    j = i - 1
    while j >= 0 and words[j]["lemma"] in POSTPOSITIVE:
        j -= 1
    if j < 0:
        return False
    art = words[j]["parse"].split(" · ")
    if art[0] != "article":
        return False
    # case and number the same; gender the same, or among the two an adjective of two
    # terminations shares (`masculine/feminine`)
    for kind in (("nominative", "genitive", "dative", "accusative", "vocative"),
                 ("singular", "plural")):
        if [t for t in art if t in kind] != [t for t in parse if t in kind]:
            return False
    genders = {g for t in parse[1:] for g in t.split("/")} & {"masculine", "feminine", "neuter"}
    return not genders or any(t in genders for t in art)


def check_unit_cases(book, chapter, verses, rep):
    """Every declined word marks its own case: a genitive or dative unit opens with `of` or
    `to`, whatever the word is — noun, adjective, demonstrative, participle.

    Agreement puts the same ending on every word of a phrase, and each ending stays visible:
    τῇ ἡμέρᾳ ταύτῃ is *to the day to this*, as ἀπὸ τῆς γῆς is *from of the earth*. The corpus
    had marked agreeing words 215 times and left them bare 71, mostly in the dative, and read
    a few datives by their use, *with big*. Units are paired with their words by lemma, in
    order; a unit that opens a preposition as well (`ἐν; γῆ`, `διά + genitive`) keeps the
    preposition's English in the lead and is not asked for a marker.
    """
    before = rep.failed
    path = render.DATA / book / ("%d.words.json" % chapter)
    if not path.exists():
        return
    lay = {v["ref"]: v["words"] for v in
           json.loads(path.read_text(encoding="utf-8")).get("verses", [])}
    seen = articled = 0
    for verse in verses:
        words = lay.get(verse["ref"])
        if not words:
            continue
        nth = collections.Counter()
        count = collections.Counter(lemmas(f)[-1].split(" + ")[0] for _, _, f in units(verse["reading"]))
        for head, chain, field in units(verse["reading"]):
            items = lemmas(field)
            word = items[-1].split(" + ")[0]
            k, nth[word] = nth[word], nth[word] + 1
            places = unit_places(words, word, count[word])
            if " + " not in items[-1] and k < len(places) and own_article_of(words, places[k]) \
                    and not re.search(r"\bthe\b", head):
                articled += 1
                rep.fail("cases", verse["ref"], "`%s` (%s) has its own article; the unit "
                         "carries it, `the`" % (head, words[places[k]]["form"]))
            if len(items) > 1 or " + " in items[-1]:
                continue
            if k >= len(places):
                continue
            parse = words[places[k]]["parse"].split(" · ")
            if "infinitive" in parse:
                # an infinitive with an article of its own reads as a gerund, the article
                # and its case inside the unit: πρὸ τοῦ γενέσθαι, *before of the coming
                # into being*. GEN 5 had set the article unprinted, `before to come into
                # being`, and 82 followed it.
                j = places[k] - 1
                while j >= 0 and words[j]["parse"].split(" · ")[0] in (
                        "adverb", "particle", "personal pronoun", "conjunction"):
                    j -= 1
                art = words[j]["parse"].split(" · ") if j >= 0 else []
                if (art[:1] == ["article"] and "neuter" in art and "singular" in art
                        and not re.search(r"\bthe \w+ing\b", head)):
                    rep.fail("cases", verse["ref"], "`%s` (%s) has its own article; it reads "
                             "as a gerund, `the …ing`" % (head, words[places[k]]["form"]))
                continue
            case = next((c for c in CASE_MARK if c in parse), None)
            if not case:
                continue
            seen += 1
            if not head.startswith(CASE_MARK[case] + " "):
                rep.fail("cases", verse["ref"], "`%s` is %s (%s); it opens `%s %s`"
                         % (head, case, words[places[k]]["form"], CASE_MARK[case], head))
    rep.done("cases", "%d genitive and dative units, each marked; every article carried"
             % seen, before)


# εἰμί's imperfect in the reading: the state formula, its short form, its negative (GEN 2:5),
# and the Johannine pre-existence forms.
BE_FORMULA = re.compile(r"kept on (?:not )?being|already in unbroken existence|"
                        r"was and remained|was — continuously")


def check_imperfect_be(book, chapter, verses, rep):
    """ἦν is never flattened to *was*: every imperfect of εἰμί carries its formula.

    The one settled exception is possession, ἦν with the dative of the owner — ὅσα ἦν αὐτῷ,
    *as great as was to him* (12:20, 16:1, 24:29) — found here by a dative within three
    words that no preposition governs. Five had read a bare *was* with no such reason
    (7:19, 7:22, 7:23, 8:1, 8:9), and nothing saw it.
    """
    before = rep.failed
    path = render.DATA / book / ("%d.words.json" % chapter)
    if not path.exists():
        return
    lay = {v["ref"]: v["words"] for v in
           json.loads(path.read_text(encoding="utf-8")).get("verses", [])}
    n = 0
    for verse in verses:
        words = lay.get(verse["ref"]) or []
        need = 0
        for i, w in enumerate(words):
            parse = w["parse"].split(" · ")
            if w["lemma"] != "εἰμί" or "imperfect" not in parse or "indicative" not in parse:
                continue
            n += 1
            owner = any("dative" in words[j]["parse"]
                        and not (j and words[j - 1]["parse"].startswith("preposition"))
                        for j in range(max(0, i - 3), min(len(words), i + 4)) if j != i)
            need += not owner
        got = len(BE_FORMULA.findall(verse["reading"]))
        if got < need:
            rep.fail("anchors", verse["ref"], "%d imperfect%s of εἰμί, %d with a formula — ἦν is "
                     "never a bare *was*" % (need, "" if need == 1 else "s", got))
    rep.done("anchors", "%d imperfects of εἰμί, none flattened" % n, before)


def check_articles(book, chapter, verses, rep):
    """The article goes where its word is, and carries that word's gender.

    A plain `the` in front of a unit printed `the to house`, `the the man`, `the upon of
    the earth`: the article belonged inside the unit, or was a second copy of one already
    there, or was making a noun of a phrase and needed its noun — `the things upon of the
    earth`. ὁ δέ is no exception: where the article stands as a pronoun it carries its
    noun too, `the one, but, … said`, and a plain `the` before δέ had more often been an
    article cut off from its own noun — ὁ δὲ θεός read with the anarthrous formula. And
    over a participle the article's noun follows the participle's gender:
    masculine and feminine `one`, neuter `thing`, as a Greek reader hears the difference
    between persons and things.
    """
    before = rep.failed
    path = render.DATA / book / ("%d.words.json" % chapter)
    lay = {}
    if path.exists():
        lay = {v["ref"]: v["words"] for v in
               json.loads(path.read_text(encoding="utf-8")).get("verses", [])}
    for verse in verses:
        ref, text = verse["ref"], verse["reading"]
        for m in STRANDED.finditer(text):
            rep.fail("articles", ref,
                     "a plain `the` stands before `%s`; put it inside the unit, drop it if "
                     "the unit carries it already, or give it its noun if it makes a noun "
                     "of a phrase" % m.group(1))
        plain = render.NAME.sub("¦", render.UNIT.sub("¦", text))
        if re.search(r"(?<![\w\-])the the(?![\w\-])", plain):
            rep.fail("articles", ref, "`the the` in the plain text: one article, written twice")
        for m in DOUBLED.finditer(text):
            if text[:m.start()].endswith(PLAIN_LEADS) or text.startswith(GLOSS_LEADS, m.start()):
                continue
            rep.fail("articles", ref,
                     "`%s %s`: the case is marked twice, once outside the unit or the article's "
                     "noun and once inside it" % (m.group(1), m.group(1)))
        words = lay.get(ref)
        if not words:
            continue
        # One article, printed once. Over a possessive, a numeral or a name and its noun it
        # prints with the first word — `of the mine` `of sound`, `the two` `messengers` —
        # and the noun's unit printing it again read `the two the messengers`.
        pieces = list(PIECES.finditer(text))
        count = collections.Counter(lemmas(f)[-1] for _, _, f in units(text))
        seen = collections.Counter()
        for n, piece in enumerate(pieces):
            if piece.group(1) is None:
                continue
            unit = render.UNIT.match(piece.group(0))
            word = lemmas(unit.group(3))[-1]
            nth, seen[word] = seen[word], seen[word] + 1
            places = unit_places(words, word, count[word])
            if (nth < len(places) and THE_LEADS.match(unit.group(1).strip())
                    and shared_article(words, places[nth]) and printed_before(pieces, n)):
                rep.fail("articles", ref,
                         "`%s` prints the article a second time: it stands before %s %s and "
                         "has printed there" % (unit.group(1).strip(), words[places[nth] - 1]["form"],
                                                words[places[nth]]["form"]))
        seen = collections.Counter()
        for head, chain, field in units(text):
            word = lemmas(field)[-1]
            nth, seen[word] = seen[word], seen[word] + 1
            m = ARTICLE_NOUN.match(head)
            places = unit_places(words, word, count[word])
            if not m or nth >= len(places) or "participle" not in words[places[nth]]["parse"]:
                continue
            want = article_noun(words[places[nth]]["parse"])
            if m.group(1) != want:
                rep.fail("articles", ref,
                         "`%s` is %s; the article's noun follows its gender: `%s`"
                         % (head, words[places[nth]]["parse"].split(" · ")[-1], want))
    rep.done("articles", "%d verses" % len(verses), before)


def check_lexicon(rep):
    """Middle Liddell is the lexicon; LSJ answers only where it has nothing.

    The LSJ table used to win outright, so a word Middle Liddell did have could be read
    from LSJ instead — ὦμος, μνημεῖον, and ποιμήν, whose entry hides under a truncated
    key. A close form counts as having the word (SPELLING, ENTRY, FILED_WITHIN), and so
    does an entry whose translation the markup hides, which MARKUP_LOST recovers. What is
    left in the table must be a word Middle Liddell lacks under every one of those.
    """
    before = rep.failed
    try:
        import words as W
        entries = W.load_middle_liddell()
    except Exception as exc:                      # pragma: no cover
        rep.skip("lexicon", "Middle Liddell would not load: %s" % exc)
        return
    for lemma in W.LSJ:
        if W.lexicon_senses(entries, lemma) is not None:
            rep.fail("lexicon", lemma,
                     "Middle Liddell has this word, so LSJ may not stand in for it — take "
                     "the LSJ entry out, and recover anything the markup hides with "
                     "MARKUP_LOST")
    rep.done("lexicon", "%d words from LSJ, none of them in Middle Liddell" % len(W.LSJ),
             before)


AORIST_FORMULA = "one completed act seen whole, not a process observed in progress"

# A hint is a short note on what happens in the verse or what matters in it, never a
# translation of it: a fluent rendering picks one English word for each Greek one, which is
# what the reading exists not to do, and it brought a familiar Bible's phrasing onto the
# page. Some 500 hints in Genesis 8-37 had become translations, most of 24-35 verse after
# verse. What gives a translation away is mechanical enough to hold: a speech rendered in
# the first or second person, a sentence carried on from the verse before, length.
HINT_MAX = 140
HINT_PERSON = re.compile(r"\b(I|me|my|mine|myself|you|your|yours|yourself|yourselves|"
                         r"we|us|our|ours|ourselves)\b")
HINT_QUOTED = re.compile(r"(?<!\w)'[^']*'(?!\w)|‘[^’]*’|\"[^\"]*\"")
HINT_CONNECTIVE = re.compile(r"^(And|But|Then|For|Now|So)\b")


def hint_faults(hint):
    """What makes a hint read as a translation, if anything."""
    out = []
    if len(hint) > HINT_MAX:
        out.append("longer than %d characters" % HINT_MAX)
    if re.match(r"^[a-z]", hint):
        out.append("opens in lower case, carrying on the verse before")
    if HINT_CONNECTIVE.match(hint):
        out.append("opens with a connective, carrying on the verse before")
    m = HINT_PERSON.search(HINT_QUOTED.sub("", hint))
    if m:
        out.append("speaks in the first or second person (`%s`) — a speech rendered, not "
                   "reported; quote a phrase in single quotes only to discuss its wording"
                   % m.group(1))
    return out


def check_banned(verses, rep):
    before = rep.failed
    for verse in verses:
        # The aorist reads as the plain English past, every other past tense being marked;
        # the formula stood on 59 of Genesis 1-11's aorists and none after, and is gone.
        if AORIST_FORMULA in verse["reading"]:
            rep.fail("banned", verse["ref"], "the aorist formula is in the reading; the "
                     "aorist reads as the plain past, and the formula is the word-by-word "
                     "layer's line")
        for fault in hint_faults(verse.get("hint", "")):
            rep.fail("banned", verse["ref"], "the hint %s; a hint is a short note on what "
                     "happens or matters, never a translation" % fault)
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

# the perfect participle's *having* among them: διυφαίνω is plain *having been filled up by
# weaving*, and that *having* is not ἔχω's beside it (EXO 36:30)
AUXILIARIES = {"has", "have", "had", "having", "was", "were", "will", "shall", "be", "been", "being",
               "may", "might", "let"}


# What an article over a phrase or an adverb prints as its noun: *the one*, *the things*.
ARTICLE_NOUNS = ("the one", "the ones", "the thing", "the things")


def entitled_to(book, chapter, verses):
    """{ref: {English a word of this verse may print as plain text}}.

    Two Greek words can head with the same English: μή and οὐ both give `not`, τε and
    καί both `and`. When one of them is a unit and the other is rightly plain text, the
    plain one is no headword left loose — it is its own word, printing its own first
    sense. Without this the bare-headword check reads every `not` in a verse holding μή
    as μή's, and every `and` in a verse holding τε as τε's.
    """
    path = render.DATA / book / ("%d.words.json" % chapter) if book else None
    if path is None or not path.exists():
        return {}
    layer = {v["ref"]: v["words"] for v in
             json.loads(path.read_text(encoding="utf-8")).get("verses", [])}
    out = {}
    for verse in verses:
        words = layer.get(verse["ref"])
        if words is None:
            continue
        claimed = {w for _, _, lemma in units(verse["reading"]) for w in lemmas(lemma)}
        here = set()
        for i, word in enumerate(words):
            # an article over a phrase or an adverb carries its own noun as plain text,
            # `of the one` before ἀνὰ μέσον (EXO 26:10), and is no εἷς left loose
            if (word["lemma"] == "ὁ" and i + 1 < len(words)
                    and words[i + 1]["parse"].startswith(("preposition", "adverb"))):
                for mark in ("", "of ", "to "):
                    here.update(mark + noun for noun in ARTICLE_NOUNS)
            got = word.get("senses") or []
            if got and word["lemma"] not in claimed:
                first = re.split(r"[,;]", got[0])[0].strip().lower()
                here.add(first)
                # and each word of it: ἐνευλογέω is plain *will be blessed in*, and its
                # *in* is its own, not a loose headword of the ἐν beside it (GEN 12:3)
                here.update(first.split())
                # in the number the form wears: λάγανον is plain *a thin broad cake*, and the
                # plural's *cakes* is its own, not ἄρτος's headword loose beside it (EXO 29:2)
                here.update(w + "s" for w in first.split())
                # and a plain verb prints the auxiliaries its tense needs: ἐκπορνεύω is
                # plain *has committed fornication*, and that *has* is not ἔχω's (GEN 38:24)
                if word["parse"].startswith("verb"):
                    here.update(AUXILIARIES)
        out[verse["ref"]] = here
    return out


def check_anchors(verses, rep, book=None, chapter=None):
    """No headword stands bare in the reading.

    The unanchored panel is built from the chains, so the only way a headword can
    reach it on its own is as plain text written outside any unit. That is caught
    here, for this verse's own headwords and for the listed ones. A headword inside
    its own chain is allowed: the chain is the whole lexical range, and the headword
    is simply its first sense.
    """
    before, total = rep.failed, 0
    entitled = entitled_to(book, chapter, verses)
    for verse in verses:
        ref, text = verse["ref"], verse["reading"]
        bare = outside_units(text)
        own = units(text)
        total += len(own)

        for entry in verse.get("names", []):
            # Plain text only. A name written as prose would print the same form in
            # both panels, which is the failure worth catching; a name inside a unit's
            # chain or inside its own gloss is not. Middle Liddell's second sense for
            # παράδεισος is "the garden of Eden", and a gloss may name the conventional
            # form in passing — neither reaches the reader as the name itself.
            if re.search(r"\b%s\b" % re.escape(entry["anchored"]), bare):
                rep.fail("anchors", ref,
                         "%r is written as plain text; a proper name is always a "
                         "[[name:%s]] marker, so each panel prints its own form of it"
                         % (entry["anchored"], entry["greek"]))

        watch = {}
        for anchor, _, _ in own:
            watch.setdefault(anchor.lower(), "a unit in this verse")
        for item in ANCHORS:
            watch.setdefault(item["anchor"].lower(), item["lemma"])
        for anchor, why in watch.items():
            # another word of this verse may be entitled to print exactly this English
            if anchor in entitled.get(ref, ()):
                continue
            # a hyphenated word is one word: the plain *drinking-troughs* of GEN 30:38 does
            # not hold the gerund *the drinking* beside it
            if re.search(r"(?<![\w-])%s(?![\w-])" % re.escape(anchor), bare, re.I):
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


MODULE_WORD = re.compile(r"(\S+?)<S>(\d+)</S>\S*?<m>([^<]+)</m>")


def lettered(rows):
    """{verse: text} with a verse Rahlfs numbers with a letter given its own key.

    The module prints Exod 28:29a inside 28:29, after `<br/><i>[a]</i>`; the page prints it
    as a verse of its own, and the data keeps it so, as `29a`.
    """
    out = {}
    for verse, text in rows.items():
        parts = re.split(r"<br/>\s*<i>\[([a-z])\]</i>", text)
        out[verse] = parts[0]
        for letter, part in zip(parts[1::2], parts[2::2]):
            out["%d%s" % (verse, letter)] = part
    return out


def module_words(text):
    """One verse of the module as [(form, lexeme, parse code)].

    Words are found by their tags, not by splitting on spaces: the module's parse code can
    itself hold a space (Μεσραιμ at GEN 10:6 and 10:13 is `lxx.N.N M`), and splitting there
    cut one word in two.
    """
    return [m.groups() for m in MODULE_WORD.finditer(text)]


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
        rows = lettered(dict(con.execute("select verse, text from verses where book_number = ? "
                                         "and chapter = ?", (number, chapter)).fetchall()))
    finally:
        con.close()
    nfc = lambda s: unicodedata.normalize("NFC", s)
    for verse, ours in sorted(morph.items(), key=lambda kv: words.verse_order(kv[0])):
        ref = "%s %d:%s" % (book, chapter, verse)
        theirs = module_words(rows.get(verse, ""))
        if len(ours) != len(theirs):
            rep.fail("words", ref, "%d words analysed, %d in the module"
                     % (len(ours), len(theirs)))
            continue
        for i, ((form, lemma, _, code, notes), (_, lexeme, mcode)) in enumerate(
                zip(ours, theirs), 1):
            reason = notes.get("module", "")
            theirs_lemma = lemmas.get(lexeme, "?")
            lemma_differs = nfc(lemma) != nfc(lemmas.get(lexeme, ""))
            parse_differs = not agrees(morph_features(code), module_features(mcode))
            if reason:
                # The analysis is the project's own; where it knowingly departs from the
                # module, the morph file says so and why, and the difference is reported
                # rather than passed over. A reason that names a difference no longer
                # there is itself a failure, so the annotations cannot go stale.
                if lemma_differs or parse_differs:
                    rep.note("words", "%s word %d (%s): ours %s, module %s — %s"
                             % (ref, i, form,
                                lemma if lemma_differs else code,
                                theirs_lemma if lemma_differs else mcode, reason))
                else:
                    rep.fail("words", ref, "word %d (%s) records a difference from the "
                             "module that is not there; delete the note" % (i, form))
            elif lemma_differs:
                rep.fail("words", ref, "word %d (%s): our lemma %s, the module %s — check "
                         "which is right" % (i, form, lemma, theirs_lemma))
            elif parse_differs:
                rep.fail("words", ref, "word %d (%s): our parse %s, the module %s — check "
                         "which is right" % (i, form, code, mcode))


# --------------------------------------------------------------------------
# 5b. the project's own morphology: well-formed, and consistent with itself
# --------------------------------------------------------------------------

POSITIONS = ("person", "tense", "voice", "mood", "case", "number", "gender", "degree")
ALPHABET = dict(zip(POSITIONS, ("123", "PIFAXY", "AMPE", "ISODNP", "NGDAV", "SPD", "MFNC",
                                "CS")))
PARTS = {"N-": "a noun", "V-": "a verb", "A-": "an adjective", "RA": "an article",
         "RP": "a personal pronoun", "RD": "a demonstrative", "RR": "a relative",
         "RI": "an interrogative", "P-": "a preposition", "C-": "a conjunction",
         "D-": "an adverb", "X-": "a particle", "I-": "an interjection"}


def shape_problems(pos, code, lemma):
    """What is wrong with a line's part of speech and parse, judged by the code's own
    grammar alone — no reference needed. An empty list means well-formed.

    Most slips in a hand-written parse are not wrong analysis but a character in the
    wrong place: ποιῆσαι written --AAN--- leaves the tense empty and puts the mood in
    the voice slot. Each slot has its own alphabet, so a shifted slot usually shows as
    a letter that cannot stand there; the shape each part of speech takes catches the
    rest. A noun's gender stays optional, because an indeclinable foreign place name
    has none to record.
    """
    if pos not in PARTS:
        return ["part of speech %r is not one of %s" % (pos, " ".join(PARTS))]
    if len(code) != 8:
        return ["parse %r has %d places; it takes 8" % (code, len(code))]
    f = dict(zip(POSITIONS, code))
    wrong = ["%r cannot stand in the %s slot" % (v, k) for k, v in f.items()
             if v != "-" and v not in ALPHABET[k]]
    if wrong:
        return wrong
    label = PARTS[pos]
    if pos == "V-":
        label = {"N": "an infinitive", "P": "a participle"}.get(f["mood"], "a finite verb")
    need = lambda *keys: ["%s needs a %s" % (label, k) for k in keys if f[k] == "-"]
    none = lambda *keys: ["%s takes no %s" % (label, k) for k in keys if f[k] != "-"]

    if pos in ("P-", "C-", "D-", "X-", "I-"):
        return none(*POSITIONS)
    if pos == "V-" and f["mood"] == "N":
        return need("tense", "voice") + none("person", "case", "number", "gender", "degree")
    if pos == "V-" and f["mood"] == "P":
        return need("tense", "voice", "case", "number", "gender") + none("person", "degree")
    if pos == "V-":
        return (need("person", "tense", "voice", "mood", "number")
                + none("case", "gender", "degree"))
    out = none("person", "tense", "voice", "mood") + need("case", "number")
    if pos != "A-":
        out += none("degree")
    if pos in ("A-", "RA", "RD", "RR"):
        out += need("gender")
    if pos == "RA" and unicodedata.normalize("NFC", lemma) != "ὁ":
        out.append("an article's dictionary form is ὁ, not %s" % lemma)
    return out


def check_morph_shape(book, chapter, rep):
    """Every line of the project's own morphology well-formed, and every annotation of a
    kind this file knows. Needs nothing outside the repository."""
    import words
    morph = words.read_morph(book, chapter)
    if morph is None:
        return
    before, total = rep.failed, 0
    for verse, lines in sorted(morph.items(), key=lambda kv: words.verse_order(kv[0])):
        ref = "%s %d:%s" % (book, chapter, verse)
        for i, (form, lemma, pos, code, notes) in enumerate(lines, 1):
            total += 1
            for problem in shape_problems(pos, code, lemma):
                rep.fail("morph", ref, "word %d (%s) %s %s: %s" % (i, form, pos, code, problem))
            if "?" in notes:
                rep.fail("morph", ref, "word %d (%s) carries an annotation of no known kind, "
                         "%r; an annotation begins 'module' or 'corpus'" % (i, form, notes["?"]))
    rep.done("morph", "%d words well-formed" % total, before)


COMPATIBLE = {("voice", "E"): {"M", "P"}, ("gender", "C"): {"M", "F"}}


def codes_agree(a, b):
    """Two parse codes in the project's own scheme, place by place. E (middle/passive)
    agrees with M or P, and C (masculine/feminine) with M or F, in either direction;
    M and P never agree with each other."""
    if len(a) != len(b):
        return False
    for k, x, y in zip(POSITIONS, a, b):
        if x != y and y not in COMPATIBLE.get((k, x), ()) and x not in COMPATIBLE.get((k, y), ()):
            return False
    return True


def corpus_key(form):
    """A form as the corpus compares it: a grave written as the acute it stands for, and
    lower case, since a capital marks only a position in the sentence."""
    d = unicodedata.normalize("NFD", form).replace("̀", "́")
    return unicodedata.normalize("NFC", d).lower()


def spelled_twice(a, b):
    """Are two different spellings of a dictionary form the same word written two ways?

    Two slips count, both made in Genesis 2: a lemma with and without its iota subscript
    (ἀποθνῄσκω / ἀποθνήσκω), and one written bare and accented (Αδαμ / Ἀδάμ). Words that
    differ in breathing or accent while both are marked — εἰς and εἷς, οὐ and οὗ — are
    different words, and never match.
    """
    if a == b:
        return False
    nfd = lambda s: unicodedata.normalize("NFD", s)
    if nfd(a).replace("ͅ", "") == nfd(b).replace("ͅ", ""):
        return True
    marked = lambda s: any(unicodedata.category(c) == "Mn" for c in nfd(s))
    return fold(a) == fold(b) and marked(a) != marked(b)


def corpus():
    """Every word of the project's own morphology, in corpus order — books as the page
    orders them, chapters by number, words as written — as
    ((book, chapter), ref, index, form, lemma, pos, code, notes)."""
    import words
    out = []
    for book in render.BOOKS:
        paths = sorted((render.DATA / book).glob("*.morph.txt"),
                       key=lambda p: int(p.name.split(".")[0]))
        for path in paths:
            chapter = int(path.name.split(".")[0])
            for verse, lines in sorted(words.parse_morph(path).items(),
                                       key=lambda kv: words.verse_order(kv[0])):
                ref = "%s %d:%s" % (book, chapter, verse)
                for i, line in enumerate(lines, 1):
                    out.append(((book, chapter), ref, i) + tuple(line))
    return out


def check_corpus(book, chapter, rep):
    """The repository is its own reference: a form analysed one way anywhere in the
    corpus is analysed that way wherever it recurs, unless the line says why.

    Each word is held against everything before it, in corpus order:
      lemma     a form keeps its dictionary form
      spelling  a dictionary form keeps one spelling (see spelled_twice)
      verb      a finite verb or infinitive keeps its whole parse; a participle its
                tense, voice and mood, since its case follows the syntax
      noun      a noun keeps its gender and number, since its case follows the syntax
    A reading new to the corpus is reported once, on the line that introduces it, in
    that line's chapter. "# corpus ..." on the line makes it a note, and a "# corpus ..."
    note on a line that introduces nothing fails — so a genuine homograph is recorded
    where it first divides, and the record cannot outlive its reason.
    """
    before, checked = rep.failed, 0
    lemmas, spellings, verbs, nouns = {}, {}, {}, {}

    def introduces(table, key, value, ref, agree):
        """Record `value` under `key`; if no reading already there agrees with it, return
        the first reading there as (value, ref), else None."""
        seen = table.setdefault(key, {})
        first = next(iter(seen.items()), None)
        new = bool(seen) and not any(agree(value, s) for s in seen)
        seen.setdefault(value, ref)
        return first if new else None

    same = lambda a, b: a == b
    for place, ref, i, form, lemma, pos, code, notes in corpus():
        key, lemma = corpus_key(form), unicodedata.normalize("NFC", lemma)
        found = []
        hit = introduces(lemmas, key, lemma, ref, same)
        if hit:
            found.append("dictionary form %s, where %s has %s" % (lemma, hit[1], hit[0]))
        group = spellings.setdefault(fold(lemma), {})
        if lemma not in group:
            twin = next((s for s in group if spelled_twice(s, lemma)), None)
            if twin:
                found.append("dictionary form spelled %s, where %s spells it %s"
                             % (lemma, group[twin], twin))
            group[lemma] = ref
        if len(code) == 8 and pos == "V-":
            shape = "-" + code[1:4] + "----" if code[3] == "P" else code
            hit = introduces(verbs, (key, lemma), shape, ref, codes_agree)
            if hit:
                found.append("parse %s, where %s has %s" % (code, hit[1], hit[0]))
        elif len(code) == 8 and pos == "N-":
            hit = introduces(nouns, (key, lemma), "-----" + code[5:7] + "-", ref, codes_agree)
            if hit:
                found.append("number and gender %s, where %s has %s"
                             % (code[5:7], hit[1], hit[0][5:7]))

        if place != (book, chapter):
            continue
        checked += 1
        note = notes.get("corpus")
        if found and note:
            for what in found:
                rep.note("corpus", "%s word %d (%s): %s — %s" % (ref, i, form, what, note))
        elif found:
            for what in found:
                rep.fail("corpus", ref, "word %d (%s): %s — correct one, or say why on "
                         "this line with '# corpus ...'" % (i, form, what))
        elif note:
            rep.fail("corpus", ref, "word %d (%s) records a difference from the corpus that "
                     "is not there; delete the note" % (i, form))
    rep.done("corpus", "%d words consistent with the corpus" % checked, before)


# --------------------------------------------------------------------------
# 6. Greek against the source edition
# --------------------------------------------------------------------------

PUNCT = re.compile(r"[.,;:·!?—·()]")

# A local module carries bare word forms: no capitals, and its own choice of elision
# mark. Neither is evidence about what the printed page has, so neither counts as a
# discrepancy. The data's own mark is U+02BC, as in the SBLGNT, so one convention
# covers both testaments.
ELISION = dict.fromkeys(map(ord, "’᾿᾽ʼ'"), "ʼ")


def sentence_starts(greek):
    """For each word of a verse, whether it opens a sentence — by the rule proper_names
    uses, so the two checks agree on which capitals need no reason. Punctuation standing
    alone (Rahlfs's section dash) is not a word."""
    out, initial = [], True
    for word in greek.split():
        if not PUNCT.sub("", word):
            continue
        out.append(initial)
        initial = word[-1] in SENTENCE_END
    return out


def same_form(module, data, initial=False, speech=(), printed=()):
    """One word of the module against the same word of the transcription.

    A capital the printed page has a reason for is not a discrepancy: the head of a
    sentence — the verse's own, or one inside it, as where Rahlfs opens a paragraph with
    no verse number of its own (GEN 11:13) — or a word opening direct speech, which the
    verse lists in `speech`, the same field check_names reads. Nor is a form the verse
    lists in `printed`: the page's own misprint, which the module corrects (GEN 24:58
    τοῦτου) and the transcription keeps. Any other difference is real and fails.
    """
    a, b = module.translate(ELISION), data.translate(ELISION)
    if a == b:
        return True
    if data in printed:
        return True
    # the capital of a letter with iota subscript is its titlecase, ᾗ to ᾟ (EXO 6:28, which
    # Rahlfs prints with the iota beside it); upper() would make it two letters, ἯΙ
    return (initial or data in speech) and a[:1].title() + a[1:] == b


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
        rows = lettered(dict(con.execute(
            "select verse, text from verses where book_number = ? and chapter = ?",
            (row[0], chapter)).fetchall()))
        out = {verse: re.sub(r"<S>.*?</S>|<m>.*?</m>", "", text).split()
               for verse, text in rows.items()}
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
    import words
    for verse in verses:
        number = words.verse_key(verse["ref"])
        if number not in src:
            rep.fail("greek", verse["ref"], "not in the Rahlfs module")
            continue
        want = [nfc(w) for w in src[number]]
        got = [nfc(w) for w in PUNCT.sub("", verse["greek"]).split()]
        if len(want) != len(got):
            rep.fail("greek", verse["ref"],
                     "%d words in the data, %d in Rahlfs" % (len(got), len(want)))
            continue
        speech = {nfc(w) for w in verse.get("speech", [])}
        printed = {nfc(w) for w in verse.get("printed", [])}
        starts = sentence_starts(verse["greek"])
        used = set()
        for i, (a, b) in enumerate(zip(want, got)):
            if not same_form(a, b, initial=starts[i], speech=speech):
                if same_form(a, b, printed=printed):
                    used.add(b)
                    continue
                rep.fail("greek", verse["ref"],
                         "word %d: Rahlfs %r / data %r" % (i + 1, a, b))
        for word in sorted(printed - used):
            rep.fail("greek", verse["ref"],
                     "`printed` lists %s, which does not differ from the module here" % word)
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
    before = rep.failed
    check_fields(verses, rep)
    if rep.failed > before:
        # the remaining checks read `reading`; on a malformed file they would only
        # repeat the same fault in other words. Counted from this chapter's own start:
        # rep.failed is the whole run's tally, so testing it outright made one bad
        # chapter skip every check of every chapter after it.
        return
    check_names(verses, rep)
    check_banned(verses, rep)
    check_anchors(verses, rep, book, chapter)
    check_articles(book, chapter, verses, rep)
    check_name_cases(book, chapter, verses, rep)
    check_unit_cases(book, chapter, verses, rep)
    check_imperfect_be(book, chapter, verses, rep)
    if EDITIONS.get(book) == "lxx":
        check_morph_shape(book, chapter, rep)
        check_corpus(book, chapter, rep)
    check_words(book, chapter, verses, rep)
    check_unit_words(book, chapter, verses, rep)
    check_one_sense(book, chapter, verses, rep)
    check_runs(book, chapter, verses, rep)
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

    print("")
    print("chains")
    check_chains(targets, rep)

    print("ranges")
    check_ranges(targets, rep)

    print("prepositions")
    check_prepositions(targets, rep)

    print("markup")
    check_markup(targets, rep)

    print("lexicon")
    check_lexicon(rep)

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
