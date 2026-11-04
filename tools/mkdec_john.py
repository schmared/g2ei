# -*- coding: utf-8 -*-
"""The coverage verdicts for John's new words: python tools/mkdec_john.py -> decisions/dec9zz_john.jsonl.
A chapter's rows go under its heading; the file sorts after every earlier one, so a row here replaces
an earlier call on the same translation."""
import io
import json
import os
import sys

from _paths import ROOT, DECISIONS  # noqa: E402
sys.path.insert(0, ROOT + "/build")
import words as W  # noqa: E402

ROWS = [
    # ---------------------------------------------------------------- JHN 1
    ("ἐξηγέομαι", "the way, go before, lead", "NOT", "piece", "«to shew» one «the way, go before, lead»: restored whole in TEXT_LOST"),
    ("ὁμολογέω", "to have", "NOT", "phrase", "οὐδὲν ὁμ. τινι, to have naught to do with: οὐδέν carries 'naught'"),
    ("ὁμολογέω", "to do with", "NOT", "phrase", "οὐδὲν ὁμ. τινι, to have naught to do with"),
    ("ὁμολογέω", "I grant", "FORM", "first person active", "ὁμολογῶ σοι, I grant you"),
    ("ὁμολογέω", "to be agreed upon, allowed or granted by common consent", "FORM", "passive", "Pass."),
    ("ὁμολογέω", "to be allowed or confessed to be", "FORM", "passive", "Pass., c. inf."),
    ("ὁμολογέω", "it is granted, allowed", "FORM", "passive", "Pass., ὁμολογεῖται"),
    ("ὁμολογέω", "things granted", "FORM", "passive participle", "τὰ ὁμολογούμενα"),
    ("εὐθύνω", "straight", "NOT", "piece", "«to steer» the bark «straight», «to make» crooked judgments «straight»"),
    ("εὐθύνω", "to make", "NOT", "piece", "«to make» crooked judgments «straight»"),
    ("εὐθύνω", "call", "NOT", "piece", "«call» him «to account»: the next translation says it whole"),
    ("εὐθύνω", "to account", "NOT", "piece", "«call» him «to account»"),
    ("ἱμάς", "the traces by which horses were attached to the chariot", "FORM", "plural", "in pl."),
    ("ἱμάς", "the reins", "FORM", "plural", "in pl."),
    ("ἱμάς", "the straps", "FORM", "plural", "in pl., on which the body of the chariot was hung"),
    ("ἱμάς", "the lash", "FORM", "plural", "in pl., of a whip"),
    ("ἱμάς", "the caestus", "FORM", "plural", "in pl., of boxers"),
    ("ἱμάς", "straps put round the hand", "FORM", "plural", "in pl., the caestus"),
    ("ἱμάς", "girdle", "FORM", "singular", "in sg., the magic girdle of Aphrodite"),
    ("ἱμάς", "leash", "NOT", "repeat", "ἱμὰς κύνειος, a proverb's: 'a dog-leash' again"),
    # ὅπου is a relative adverb of place, which the entry says in prose; its first translation, «in some
    # places», is a phrase's, and the senses of the word itself are *where* and, of cause, *whereas* (JHN 1:28)
    ("ὅπου", "in some places", "NOT", "phrase", "ἔσθ' ὅπου, Lat. est ubi"),
    ("ὅπου", "somewhere or other", "NOT", "phrase", "ὅκου δή, with another particle, Lat. nescio ubi"),
    ("ὅπου", "wherever", "NOT", "phrase", "ὅπου ἄν, with the subjunctive: ἄν's"),
    ("ὅπου", "by which", "NOT", "piece", "οὐκ ἔσθ' ὅπου, there are no means «by which»"),
    ("ὅπου", "that", "NOT", "piece", "οὐκ ἔσθ' ὅπου, it is impossible «that»"),
    ("διδάσκαλος", "school", "NOT", "phrase", "εἰς διδασκάλου φοιτᾶν, to go to school"),
    ("διδάσκαλος", "taught the actors", "NOT", "label", "why a dramatic poet was called διδάσκαλος"),
    ("φωνέω", "making", "NOT", "piece", "ὄπα φωνήσασα, «making» the voice «sound»"),
    ("φωνέω", "sound", "NOT", "piece", "ὄπα φωνήσασα, «making» the voice «sound»"),
    ("φωνέω", "to have the", "NOT", "piece", "μέγιστα φωνέειν, «to have the» loudest «voice»"),
    ("φωνέω", "voice", "NOT", "piece", "μέγιστα φωνέειν, «to have the» loudest «voice»"),
    ("θεάομαι", "the spectators", "NOT", "construction", "οἱ θεώμενοι, the participle with the article"),
    ("πλήρωμα", "their fill", "NOT", "piece", "πλ. τυρῶν, their fill of cheese: the example's possessive"),
    ("πλήρωμα", "their complement", "NOT", "piece", "of single ships, their complement: the example's possessive"),
    ("βαπτίζω", "soaked in wine", "FORM", "passive", "Pass., βεβαπτισμένοι, metaph."),
    ("βαπτίζω", "over head and ears", "NOT", "phrase", "ὀφλήμασι βεβαπτισμένος, over head and ears in debt"),
    ("βαπτίζω", "to get oneself baptized", "FORM", "middle", "Mid."),
    ("φανερόω", "to become so", "FORM", "passive", "Pass., to become known or famous"),
    ("ἐξουσία", "the authorities", "FORM", "plural", "αἱ ἐξουσίαι"),
    ("φῶς", "eyes", "FORM", "plural", "φάος, metaph., in pl. the eyes", "fa/os"),
    ("Χριστός", "to be rubbed on", "FORM", "adjective", "the adjective's", "xristo/s"),
    ("Χριστός", "anointed", "FORM", "adjective", "the adjective's", "xristo/s"),
    ("Χριστός", "salves", "FORM", "neuter plural", "τὰ χριστά", "xristo/s"),
]


def key_of(lemma):
    return W.SPELLING.get(W.beta(lemma), W.beta(lemma))


with io.open(os.path.join(DECISIONS, "dec9zz_john.jsonl"), "w", encoding="utf-8") as f:
    for row in ROWS:
        lemma, sense, verdict, code, why = row[:5]
        key = row[5] if len(row) > 5 else W.entry_keys(key_of(lemma))[0]
        f.write(json.dumps({"lemma": lemma, "key": key, "sense": sense, "verdict": verdict, "code": code,
                            "why": why}, ensure_ascii=False) + "\n")
print(len(ROWS))
