#!/usr/bin/env python3
"""data/<BOOK>/<chapter>.json  ->  site/index.html

Block structure lives in templates/. This file owns two things only: the
inline-markup expansion the JSON strings use, and the book metadata table.
Nothing here should hand-write per-chapter markup.

Inline markup permitted inside JSON strings:

    *emphasis*        -> <em>emphasis</em>
    [[flag]]          -> the note's flag badge, at that position
                         (a note with a flag and no [[flag]] gets it prepended)
    [[name:Ἰωάννης]]  -> the name span plus its parenthetical gloss, drawn
                         from the verse's "names" list; the form used is the
                         Greek transliteration in the unanchored panel and the
                         conventional English one in the anchored panel

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
PAGE = [("GEN", 1), ("JHN", 1)]

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


def inline(text, flag=None, names=(), form=None):
    out = esc(text)
    out = re.sub(r"\*(.+?)\*", r"<em>\1</em>", out, flags=re.S)

    if flag:
        badge = '<span class="flag">%s</span>' % esc(flag)
        if "[[flag]]" in out:
            out = out.replace("[[flag]]", badge)
        else:
            out = badge + " " + out
    elif "[[flag]]" in out:
        raise ValueError("[[flag]] used in a note with no flag: %r" % text)

    by_greek = {n["greek"]: n for n in names}

    def name(m):
        n = by_greek[m.group(1)]
        return '<span class="name">%s</span> <span class="paren">%s</span>' % (
            esc(n[form]), esc(n["gloss"]))

    return re.sub(r"\[\[name:([^\]]+)\]\]", name, out)


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

def context(verse):
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
        "unanchored": inline(verse["unanchored"], names=names, form="unanchored"),
        "anchored": inline(verse["anchored"], names=names, form="anchored"),
    }


def build():
    verse_tpl = load_template("verse.html")
    page_tpl = load_template("page.html")

    sections = []
    for book, chapter in PAGE:
        verses = json.loads((DATA / book / ("%d.json" % chapter)).read_text(encoding="utf-8"))
        for verse in verses:
            sections.append(render(verse_tpl, [context(verse)]).rstrip("\n"))

    return render(page_tpl, [{"sections": "\n\n".join(sections)}])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", metavar="FILE",
                    help="compare the render against FILE instead of writing site/")
    args = ap.parse_args()

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
