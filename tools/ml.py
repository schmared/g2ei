# -*- coding: utf-8 -*-
"""Print Middle Liddell entries by Beta Code key, tags stripped, translations in «»."""
import io
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")
from _paths import ROOT, WORK, DECISIONS  # noqa: E402
s = io.open(ROOT + "/sources/middle-liddell/"
            "Perseus_text_1999.04.0058.xml", encoding="utf-8").read()
for key in sys.argv[1:]:
    pat = r'<entry\b[^>]*\bkey="%s\d?"[^>]*>(.*?)</entry>' % re.escape(key)
    for m in re.finditer(pat, s, re.S):
        body = re.sub(r"<tr\b[^>]*>(.*?)</tr>", r"«\1»", m.group(1), flags=re.S)
        body = re.sub(r"<[^>]+>", "", body)
        print("==", key, re.sub(r"\s+", " ", body)[:int(__import__("os").environ.get("MLN","1800"))])
        print()
