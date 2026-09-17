#!/usr/bin/env python3
"""data/<BOOK>/<chapter>.json  ->  site/index.html

Block structure lives in templates/. This file owns two things only: the
inline-markup expansion the JSON strings use, and the book metadata table.
Nothing here should hand-write per-chapter markup.

Inline markup permitted inside JSON strings:

    *emphasis*        -> <em>emphasis</em>
    [[flag]]          -> (notes) the note's flag badge, at that position
                         (a note with a flag and no [[flag]] gets it prepended)
    [[anchor|chain]]  -> (reading) the chain alone in the unanchored panel; in the
                         anchored panel the anchor, then the chain set off in em
                         dashes and shaded — see reading()
    [[name:Ἰωάννης]]  -> (reading) the name span plus its parenthetical gloss, drawn
                         from the verse's "names" list; the form used is the
                         Greek transliteration in the unanchored panel and the
                         conventional English one in the anchored panel. An entry
                         marked "bare" prints the form alone: a name is glossed on
                         its first occurrence in the chapter and bare thereafter,
                         and both panels still print their own form of it.

Both reading panels are derived from the verse's single `reading` string, so the
anchored text is always exactly the unanchored text with the headwords added.

Where data/<BOOK>/<chapter>.words.json exists (written by build/words.py), each
Greek line gets the word-by-word layer: form, lemma, parse, and lexicon senses.

Usage:
    python build/render.py                 # write site/index.html
    python build/render.py --check FILE    # render and diff against FILE
"""
import argparse
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
TEMPLATES = ROOT / "templates"
SITE = ROOT / "site"

# Chapters on the page, in order.
PAGE = [("GEN", 1), ("GEN", 2), ("GEN", 3), ("GEN", 4), ("GEN", 5), ("GEN", 6), ("GEN", 7), ("GEN", 8), ("GEN", 9), ("GEN", 10), ("JHN", 1)]

BOOKS = {
    "GEN": {
        "name": "Genesis",
        "src": "Septuagint · Rahlfs",
        "notes_sub": "Lexical range, aspect, and where the Greek parts from the Hebrew",
    },
    "JHN": {
        "name": "John",
        "src": "Nestle-Aland",
        "notes_sub": "Lexical range, aspect, and the grammar English cannot reproduce",
    },
}

GREEK = re.compile(r"[Ͱ-Ͽἀ-῿]")


# --------------------------------------------------------------------------
# inline markup
# --------------------------------------------------------------------------

def esc(s):
    """Escape only the three characters that would change the markup.

    Quotes and apostrophes are left as themselves — they appear in the reading
    texts as real punctuation and entity-escaping them is noise.
    """
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def emphasis(html):
    return re.sub(r"\*(.+?)\*", r"<em>\1</em>", html, flags=re.S)


def inline(text, flag=None):
    """Notes and hints: *emphasis* and the positional [[flag]] badge."""
    out = emphasis(esc(text))

    if flag:
        badge = '<span class="flag">%s</span>' % esc(flag)
        if "[[flag]]" in out:
            out = out.replace("[[flag]]", badge)
        else:
            out = badge + " " + out
    elif "[[flag]]" in out:
        raise ValueError("[[flag]] used in a note with no flag: %r" % text)
    return out


UNIT = re.compile(r"\[\[(?!name:)([^|\[\]]+)\|([^\[\]]+)\]\]")
NAME = re.compile(r"\[\[name:([^\]]+)\]\]")
SENTENCE_START = re.compile(r"(?:^|[.!?]\s+)$")


def capitalise(s):
    for i, c in enumerate(s):
        if c.isalpha():
            return s[:i] + c.upper() + s[i + 1:]
    return s


def reading(text, names, form):
    """Derive one panel ("unanchored" or "anchored") from a verse's `reading`.

    A unit [[anchor|chain]] becomes the chain alone in the unanchored panel, and in
    the anchored panel the anchor followed by the chain in em dashes, shaded:

        anchor <span class="chain">— chain —</span>

    Nothing else differs between the panels. The rest is typography, not wording:
    a comma or em dash straight after a unit is absorbed into its closing dash, no
    closing dash is added before . ; : ! ? or the end, and a unit at the head of a
    sentence is capitalised — the chain in the unanchored panel, the anchor in the
    anchored one.
    """
    src = esc(text)
    out, pos = [], 0
    for m in UNIT.finditer(src):
        out.append(src[pos:m.start()])
        anchor, chain = m.group(1).strip(), m.group(2).strip()
        initial = bool(SENTENCE_START.search(src[:m.start()]))
        pos = m.end()
        if form == "unanchored":
            out.append(capitalise(chain) if initial else chain)
            continue
        rest = src[pos:]
        absorbed = re.match(r"\s*[,—]\s*", rest)
        if absorbed:
            close, gap = " —", " "
            pos += absorbed.end()
        elif re.match(r"\s*(?:[.;:!?)]|$)", rest):
            close, gap = "", ""
        else:
            close, gap = " —", ""
        out.append('%s <span class="chain">— %s%s</span>%s'
                   % (capitalise(anchor) if initial else anchor, chain, close, gap))
    out.append(src[pos:])

    by_greek = {n["greek"]: n for n in names}
    glossed = set()

    def name(m):
        n = by_greek[m.group(1)]
        span = '<span class="name">%s</span>' % esc(n[form])
        if n.get("bare") or n["greek"] in glossed:
            # Glossed on its first occurrence in the chapter, bare after that — which
            # includes a second occurrence in the verse that carries the gloss (Αβελ
            # twice in GEN 4:2) — but still panel-specific: Iōannēs unanchored, John
            # anchored.
            return span
        glossed.add(n["greek"])
        return '%s <span class="paren">%s</span>' % (span, esc(n["gloss"]))

    return emphasis(NAME.sub(name, "".join(out)))


# --------------------------------------------------------------------------
# template engine — the mustache subset the templates actually use
# --------------------------------------------------------------------------

TAG = re.compile(r"\{\{(?P<kind>[{#^/]?)\s*(?P<key>[\w.]+)\s*\}?\}\}")
STANDALONE = re.compile(r"^[ \t]*(\{\{[#^/][\w.]+\}\})[ \t]*\r?\n", re.M)


def _close(tpl, start, key):
    """Return (inner, index-after-close) for the section opened before `start`."""
    depth, pos = 1, start
    while True:
        m = TAG.search(tpl, pos)
        if m is None:
            raise ValueError("unclosed section {{#%s}}" % key)
        if m.group("kind") in ("#", "^"):
            depth += 1
        elif m.group("kind") == "/":
            depth -= 1
            if depth == 0:
                return tpl[start:m.start()], m.end()
        pos = m.end()


def _lookup(stack, key):
    for frame in reversed(stack):
        if isinstance(frame, dict) and key in frame:
            return frame[key]
    return None


def render(tpl, stack):
    out, pos = [], 0
    while True:
        m = TAG.search(tpl, pos)
        if m is None:
            out.append(tpl[pos:])
            return "".join(out)
        out.append(tpl[pos:m.start()])
        kind, key = m.group("kind"), m.group("key")
        value = _lookup(stack, key)

        if kind in ("#", "^"):
            inner, pos = _close(tpl, m.end(), key)
            truthy = bool(value)
            if kind == "^":
                if not truthy:
                    out.append(render(inner, stack))
            elif isinstance(value, list):
                for item in value:
                    out.append(render(inner, stack + [item]))
            elif truthy:
                out.append(render(inner, stack + [value if isinstance(value, dict) else {}]))
        elif kind == "{":
            out.append("" if value is None else str(value))
            pos = m.end()
        else:
            out.append("" if value is None else esc(str(value)))
            pos = m.end()


def load_template(name):
    tpl = (TEMPLATES / name).read_text(encoding="utf-8")
    return STANDALONE.sub(r"\1", tpl)


# --------------------------------------------------------------------------
# verse -> template context
# --------------------------------------------------------------------------

def context(verse, words=None, words_src=""):
    book, chapter_verse = verse["ref"].split(" ")
    chapter, number = chapter_verse.split(":")
    meta = BOOKS[book]
    names = verse.get("names", [])
    demo = verse.get("demo")

    notes = []
    for i, note in enumerate(verse["notes"]):
        notes.append({
            "first": i == 0,
            "latin": not GREEK.search(note["lemma"]),
            "lemma": inline(note["lemma"]),
            "text": inline(note["text"], flag=note.get("flag")),
        })

    return {
        "banner": verse.get("banner", "%s %s:%s" % (meta["name"].upper(), chapter, number)),
        "section_class": "demo" if demo else "verse",
        "demo": demo,
        "num": "%s %s : %s" % (meta["name"], chapter, number),
        "src": meta["src"],
        "greek": verse["greek"],
        "hint": inline(verse["hint"]),
        "notes_sub": verse.get("notes_sub", meta["notes_sub"]),
        "notes": notes,
        "unanchored": reading(verse["reading"], names, "unanchored"),
        "anchored": reading(verse["reading"], names, "anchored"),
        "has_words": bool(words),
        "words": [dict(w, senses=" · ".join(w["senses"])) for w in (words or [])],
        "words_src": words_src,
    }


def load_words(book, chapter):
    """The word-by-word layer for a chapter, as {ref: words}, and its source note."""
    path = DATA / book / ("%d.words.json" % chapter)
    if not path.exists():
        return {}, ""
    layer = json.loads(path.read_text(encoding="utf-8"))
    return {v["ref"]: v["words"] for v in layer["verses"]}, layer.get("source", "")


def build():
    verse_tpl = load_template("verse.html")
    page_tpl = load_template("page.html")

    sections = []
    for book, chapter in PAGE:
        verses = json.loads((DATA / book / ("%d.json" % chapter)).read_text(encoding="utf-8"))
        words, words_src = load_words(book, chapter)
        for verse in verses:
            ctx = context(verse, words.get(verse["ref"]), words_src)
            sections.append(render(verse_tpl, [ctx]).rstrip("\n"))

    return render(page_tpl, [{"sections": "\n\n".join(sections)}])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", metavar="FILE",
                    help="compare the render against FILE instead of writing site/")
    args = ap.parse_args()
    # a --check diff carries Greek; don't let a cp1252 pipe on Windows crash on it
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")

    html = build()

    if args.check:
        # newline="" so the comparison sees line endings as they really are
        want = pathlib.Path(args.check).read_text(encoding="utf-8", newline="")
        if html == want:
            print("identical to %s (%d bytes)" % (args.check, len(html)))
            return 0
        import difflib
        sys.stdout.writelines(difflib.unified_diff(
            want.splitlines(True), html.splitlines(True),
            fromfile=args.check, tofile="render.py", n=1))
        return 1

    SITE.mkdir(exist_ok=True)
    out = SITE / "index.html"
    # newline="\n" — the generated file must not pick up CRLF on Windows
    out.write_text(html, encoding="utf-8", newline="\n")
    print("wrote %s (%d bytes)" % (out.relative_to(ROOT), len(html)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
