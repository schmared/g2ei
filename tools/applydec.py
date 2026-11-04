# -*- coding: utf-8 -*-
"""Turn the gap verdicts (dec*.jsonl) into words.py's COVERAGE_NOT and COVERAGE_ONLY blocks.

python applydec.py            -> prints a summary and unmapped FORM codes, writes coverage_block.py
python applydec.py --write    -> replaces the block between the markers in build/words.py"""
import collections
import glob
import io
import json
import os
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")
SP = os.path.dirname(os.path.abspath(__file__))
from _paths import ROOT, WORK, DECISIONS  # noqa: E402
sys.path.insert(0, ROOT + "/build")
import words as W  # noqa: E402

MAP = [  # (pattern in the agent's FORM code, FORMS name), first match wins
    (r"not (?:the )?neuter|adjective, not τὰ", "not neuter"), (r"perfect and passive|perfect, pluperfect|perfect or passive", "perfect or passive"),
    (r"neuter pl", "neuter plural"), (r"not (?:the )?adverb|adjective'?s?\b.*not.*adverb|not as adverb", "not adverb"),
    (r"not (?:the )?participle", "not participle"), (r"not (?:the )?perfect", "not perfect"),
    (r"not (?:the )?passive", "not passive"), (r"not (?:the )?active|middle(?:/| or | and )passive", "middle or passive"),
    (r"\bplural\b|\bpl\b", "plural"), (r"\bsingular\b", "singular"), (r"\bdual\b", "dual"),
    (r"\bpassive\b", "passive"), (r"\bmiddle\b", "middle"), (r"\bactive\b", "active"),
    (r"participle", "participle"), (r"infinitive", "infinitive"), (r"imperative", "imperative"),
    (r"pluperfect", "pluperfect"), (r"perfect", "perfect"), (r"future", "future"), (r"aorist", "aorist"),
    (r"imperfect", "imperfect"), (r"present", "present"),
    (r"comparative", "comparative"), (r"superlative", "superlative"),
    (r"vocative", "vocative"), (r"dative", "dative"), (r"genitive", "genitive"), (r"accusative", "accusative"),
    (r"nominative", "nominative"),
    (r"feminine", "feminine"), (r"masculine", "masculine"), (r"neuter", "neuter"),
    (r"\badverb", "adverb"), (r"conjunction", "conjunction"), (r"particle", "particle"),
    (r"preposition", "preposition"), (r"\bnoun\b|substantive|as subst", "noun"), (r"adjective", "adjective"),
    (r"\bverb\b", "verb"),
]


MANUAL = {"middle only": "middle only", "second person": "second person", "first person": "first person", "positive (πρέσβυς)": "positive", "proper name Νύξ": "never", "proper name Χάρις": "never",
          "proper name Χάριτες": "never", "the form ῥήσσω": "never", "with the article (οἱ ἐκεῖ)": "never",
          "with the article (τοὐκεῖθεν)": "never", "first person, parenthetic": "first person",
          "first person οἶμαι, answering a question": "first person", "second person οἴει, as a question": "second person",
          "neuter singular": "neuter singular", "active participle": "active participle",
          "passive participle": "passive participle", "middle participle": "middle participle",
          "neuter participle": "neuter participle", "perfect passive": "perfect passive",
          "first person active": "first person active"}


def form_name(code):
    if code in MANUAL:
        return MANUAL[code]
    low = code.lower()
    for pat, name in MAP:
        if re.search(pat, low):
            return name
    return None


def main():
    rows = []
    for path in sorted(glob.glob(os.path.join(DECISIONS, "dec*.jsonl"))):
        for line in io.open(path, encoding="utf-8"):
            line = line.strip()
            if line:
                row = json.loads(line)
                # only the hand-made verdicts replace an earlier call; the agents' files are read as before
                row["_manual"] = "manual" in path or "q33" in path
                rows.append(row)
    notd = collections.defaultdict(dict)
    onlyd = collections.defaultdict(dict)
    unmapped = collections.Counter()
    verdicts = collections.Counter()
    for r in rows:
        verdicts[r["verdict"]] += 1
        key = re.sub(r"\d+$", "", r["key"].split("/")[0] if "/" in r["key"] and r["key"].count("/") > 1 and False else r["key"])
        key = re.sub(r"\d+$", "", r["key"])
        sense = W.tidy_gloss(r["sense"])
        why = ("%s: %s" % (r.get("code", ""), r.get("why", ""))).strip(": ")
        # a later verdict on the same translation replaces an earlier one, of either kind
        if r["verdict"] == "NOT":
            notd[key][sense] = why
            if r["_manual"]:
                onlyd[key].pop(sense, None)
        elif r["verdict"] == "FORM":
            name = form_name(r.get("code", ""))
            if name is None:
                unmapped[r.get("code", "")] += 1
                continue
            onlyd[key][sense] = (name, r.get("why", ""))
            if r["_manual"]:
                notd[key].pop(sense, None)
        elif r["verdict"] == "KEEP" and r["_manual"]:
            notd[key].pop(sense, None)
            onlyd[key].pop(sense, None)
    print(dict(verdicts), "rows", len(rows))
    print("unmapped FORM codes:", unmapped.most_common(40))
    out = ["# BEGIN COVERAGE (generated from the Q24 pass: each card translation a chain left out, sorted into",
           "# a sense, which the chain now carries, or one of these. The reason is the value.)",
           "COVERAGE_NOT = {"]
    for key in sorted(k for k in notd if notd[k]):
        out.append("    %r: {" % key)
        for sense, why in notd[key].items():
            out.append("        %r: %r," % (sense, why))
        out.append("    },")
    out.append("}")
    out.append("COVERAGE_ONLY = {")
    for key in sorted(k for k in onlyd if onlyd[k]):
        out.append("    %r: {" % key)
        for sense, (name, why) in onlyd[key].items():
            out.append("        %r: %r,  # %s" % (sense, name, why.replace("\n", " ")[:90]))
        out.append("    },")
    out.append("}")
    out.append("# END COVERAGE")
    block = "\n".join(out) + "\n"
    io.open(os.path.join(WORK, "coverage_block.py"), "w", encoding="utf-8").write(block)
    print(len(notd), "keys NOT,", len(onlyd), "keys FORM")
    if "--write" in sys.argv:
        p = ROOT + "/build/words.py"
        s = io.open(p, encoding="utf-8").read()
        if "# BEGIN COVERAGE" in s:
            s = re.sub(r"# BEGIN COVERAGE.*?# END COVERAGE\n", lambda m: block, s, flags=re.S)
        else:
            anchor = "# The forms a FORM_ONLY sense belongs to"
            s = s.replace(anchor, block + "\n\n" + anchor, 1)
        io.open(p, "w", encoding="utf-8", newline="\n").write(s)
        print("written")


if __name__ == "__main__":
    main()
