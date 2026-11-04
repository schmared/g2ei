# -*- coding: utf-8 -*-
"""Print LSJ entries by Beta Code key, tags stripped, translations in «»."""
import glob
import io
import re
import sys

from _paths import ROOT  # noqa: E402

sys.stdout.reconfigure(encoding="utf-8")
S = "".join(io.open(p, encoding="utf-8").read() for p in
            glob.glob(ROOT + "/sources/lsj/*.xml"))
for key in sys.argv[1:]:
    pat = r'<entryFree\b[^>]*\bkey="%s\d?"[^>]*>(.*?)</entryFree>' % re.escape(key)
    for m in re.finditer(pat, S, re.S):
        body = re.sub(r"<tr\b[^>]*>(.*?)</tr>", r"«\1»", m.group(1), flags=re.S)
        body = re.sub(r"<[^>]+>", "", body)
        print("==", key, re.sub(r"\s+", " ", body)[:900])
        print()
