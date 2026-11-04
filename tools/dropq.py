# -*- coding: utf-8 -*-
"""Delete settled questions from reference/open-questions.md: python dropq.py 6 8 9"""
import io, re, sys
from _paths import ROOT, WORK, DECISIONS  # noqa: E402
p = ROOT + "/reference/open-questions.md"
s = io.open(p, encoding="utf-8").read()
for n in sys.argv[1:]:
    m = re.search(r"^## Q%s\. .*?(?=^## Q\d+\. |\Z)" % n, s, re.S | re.M)
    assert m, n
    s = s[:m.start()] + s[m.end():]
io.open(p, "w", encoding="utf-8", newline="\n").write(s.rstrip("\n") + "\n")
print(re.findall(r"^## (Q\d+)\.", s, re.M))
