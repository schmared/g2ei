# -*- coding: utf-8 -*-
"""`# module …` notes for GEN 50: the corpus's own note for the same form or lemma pair where
there is one, and these by form where there is not."""
import collections
import glob
import io
import os
import re
import subprocess
import sys

sys.stdout.reconfigure(encoding="utf-8")
from _paths import ROOT, WORK, DECISIONS  # noqa: E402
BOOK, CH = sys.argv[1], int(sys.argv[2])
HAND = {}
_hand = "%s/hand%s%d.py" % (WORK, BOOK, CH)
if os.path.exists(_hand):
    exec(io.open(_hand, encoding="utf-8").read())

from _paths import rahlfs_dir  # noqa: E402
env = dict(os.environ, LXX_RAHLFS_DIR=rahlfs_dir(),
           PYTHONIOENCODING="utf-8")
out = subprocess.run([sys.executable, ROOT + "/build/validate.py"], cwd=ROOT, env=env,
                     capture_output=True, text=True, encoding="utf-8").stdout
FAIL = re.compile(r"FAIL  words    %s %d:(\d+[a-z]?)\s+word (\d+) \((\S+)\): our (lemma|parse) (\S+), the module (\S+)" % (BOOK, CH))
fails = [m.groups() for m in FAIL.finditer(out)]

by_form = collections.defaultdict(collections.Counter)
by_pair = collections.defaultdict(collections.Counter)
for p in glob.glob(ROOT + "/data/*/*.morph.txt"):
    if p.replace("\\", "/").endswith("/%s/%d.morph.txt" % (BOOK, CH)):
        continue
    for line in io.open(p, encoding="utf-8"):
        if "# module" not in line or line.startswith("#"):
            continue
        body, note = line.split("# module", 1)
        parts = body.split()
        if len(parts) < 5:
            continue
        note = "module" + note.split("  #")[0].rstrip("\n")
        by_form[parts[3]][note] += 1
        m = re.match(r"module lemma (\S+)", note)
        if m:
            by_pair[(parts[4], m.group(1))][note] += 1

notes = {}
for verse, word, form, kind, ours, theirs in fails:
    note = HAND.get("%s:%s" % (verse, word)) or HAND.get(form)
    if not note:
        cand = by_form.get(form) or (by_pair.get((ours, theirs)) if kind == "lemma" else None)
        note = cand.most_common(1)[0][0] if cand else None
    notes[(verse, int(word))] = note
    print("%s:%s w%s %s -> %s" % (CH, verse, word, form, note))

if "--write" in sys.argv and all(notes.values()):
    path = "%s/data/%s/%d.morph.txt" % (ROOT, BOOK, CH)
    lines = io.open(path, encoding="utf-8").read().split("\n")
    count = collections.Counter()
    for n, line in enumerate(lines):
        if not line or line.startswith("#"):
            continue
        v = line.split()[0].split(":")[1]
        count[v] += 1
        note = notes.get((v, count[v]))
        if note:
            lines[n] = line.rstrip() + ("  # " if "#" not in line else "  # ") + note if "# module" not in line else line
    io.open(path, "w", encoding="utf-8", newline="\n").write("\n".join(lines))
    print("written")
elif "--write" in sys.argv:
    print("not written: a difference has no note")
