# -*- coding: utf-8 -*-
"""My own verdicts on what the review of the additions turned up: python mkdec9.py -> dec9_manual.jsonl.
They sort last, so they override the agents' where both decided a translation."""
import io
import json
import os
import sys

from _paths import ROOT, WORK, DECISIONS  # noqa: E402
sys.path.insert(0, ROOT + "/build")
import words as W  # noqa: E402

SP = os.path.dirname(os.path.abspath(__file__))
ROWS = [
    # (lemma, sense, verdict, code, why)
    ("κάκωσις", "for ill-usage or neglect of parents", "NOT", "phrase", "δίκη κακώσεως, an action for ill-usage"),
    ("μέγας", "by far", "NOT", "phrase", "μέγα, μεγάλα as adverbs with a comparative"),
    ("μέγας", "far", "NOT", "phrase", "piece of 'by far', the adverbial neuter"),
    ("μικρός", "for a little, cheap", "NOT", "phrase", "μικροῦ, the genitive of price"),
    ("μόνος", "without", "NOT", "piece", "μόνος c. gen., 'alone, without' — the genitive carries it"),
    ("μῆκος", "at length, in full", "NOT", "phrase", "ἐς μῆκος, adverbial"),
    ("νόμος", "by custom, conventionally", "NOT", "phrase", "νόμῳ, the dative as an adverb"),
    ("πεζός", "on land, going by land", "NOT", "phrase", "πεζῇ, the dative as an adverb"),
    ("πολύς", "by far", "NOT", "phrase", "πολλῷ with a comparative"),
    ("πολύς", "far", "NOT", "phrase", "piece of 'by far'"),
    ("πολύς", "for the most part", "NOT", "phrase", "τὸ πολύ, ὡς ἐπὶ τὸ πολύ"),
    ("πρόσωπον", "in bodily presence", "NOT", "phrase", "κατὰ πρόσωπον"),
    ("πᾶς", "in all things, altogether", "NOT", "phrase", "ἐν πᾶσι"),
    ("πᾶς", "in all points, entirely, wholly", "NOT", "phrase", "κατὰ πάντα, τὸ πᾶν"),
    ("πᾶς", "in every way, by all means, altogether", "NOT", "phrase", "πάντως, πάντα, adverbial"),
    ("πᾶς", "on the whole, altogether", "NOT", "phrase", "τὸ πᾶν, adverbial"),
    ("πᾶς", "with or in the judgment of all", "NOT", "phrase", "παρὰ πᾶσι"),
    ("ἐμός", "for my part, as far as concerns me", "NOT", "phrase", "τὸ ἐμόν, τοὐμόν, adverbial"),
    ("ἔσχατος", "for the last time", "NOT", "phrase", "τὸ ἔσχατον, adverbial"),
    ("αἰτία", "as their characteristic", "NOT", "piece", "a piece of an example's translation"),
    ("θυμός", "as the seat of anger", "NOT", "label", "the entry's description of a use"),
    ("μέσος", "by the middle, by the waist", "NOT", "phrase", "μέσον ἔχειν, λαβεῖν"),
    ("χάρις", "as far as regards, as to", "NOT", "phrase", "χάριν used as a preposition"),
    ("ἀρχή", "in all", "NOT", "phrase", "ἀρχὴν with numerals"),
    ("ὅμοιος", "in which each takes part", "NOT", "piece", "ὁμοία μάχη, an example's translation"),
    ("μήν", "quid vero?", "NOT", "latin", "Latin"),
    ("μήν", "well, but how . . ?", "NOT", "phrase", "ἀλλὰ πῶς μήν, a phrase's"),
    ("οἴομαι", "don't you think so? what think you", "FORM", "second person", "οἴει; as a question"),
    ("φαίνω", "yes", "NOT", "phrase", "φαίνεται, the answer's"),
    ("χράομαι", "friends", "NOT", "piece", "a piece of 'χρῆσθαί τινι φίλῳ, to have as a friend'"),
    ("μίγνυμι", "win", "NOT", "piece", "a piece of an example's translation"),
    ("ἐκλείπω", "the deceased", "NOT", "construction", "οἱ ἐκλιπόντες, the participle with the article"),
    ("ἐκλείπω", "incomplete", "NOT", "piece", "an example's adjective"),
    ("τίθημι", "left", "NOT", "piece", "an example's participle"),
    ("καταράομαι", "accursed", "FORM", "passive", "the perfect passive participle, κατηραμένος"),
    ("ἀληθής", "itane? indeed? really? in sooth?", "NOT", "phrase", "ἀληθές; in a question, the sentence's, Latin first"),
    ("ἐπέχω", "hinder", "KEEP", "", "a sense"),
    ("λέγω", "I mean", "FORM", "first person", "λέγω, I mean, in parenthesis"),
    ("ποιέω", "to put the case assume", "FORM", "imperative", "ποίει, put the case, assume"),
    ("ἔχω", "he aimed", "NOT", "piece", "an example's translation"),
    ("ἔχω", "he held his course", "NOT", "piece", "an example's translation"),
    ("ἔχω", "he could not", "NOT", "piece", "an example's translation"),
    ("ἔχω", "the case stands", "NOT", "phrase", "πῶς ἔχει, how the case stands"),
    ("τέκνον", "my son, my child", "FORM", "vocative", "τέκνον, in address"),
    ("δικαίως", "have a right", "NOT", "construction", "δίκαιός εἰμι c. inf."),
    ("πλατύνω", "to widen one's", "NOT", "piece", "a piece of an example, to widen one's phylacteries"),
    ("ἀποβαίνω", "things ended", "FORM", "neuter plural", "τὰ ἀποβάντα"),
    ("προσφέρω", "to deal with, behave oneself", "FORM", "middle only", "Mid."),
    ("ἐμός", "my country", "NOT", "phrase", "ἡ ἐμή, sc. γῆ, the ellipsis's"),
    ("μήν", "and see . . , here comes . . ;", "NOT", "phrase", "καὶ μήν, the phrase's"),
    ("μήν", "then?", "NOT", "phrase", "τί μήν; the question's"),
    ("πᾶς", "all the", "NOT", "piece", "a piece of an example"),
    ("πᾶς", "all his", "NOT", "piece", "a piece of an example"),
    ("πᾶς", "in all", "NOT", "phrase", "ἐν πᾶσι"),
    ("πᾶς", "at all", "NOT", "phrase", "with a negative"),
    ("χράομαι", "to make of", "NOT", "piece", "τί χρήσομαι, what use shall I make of"),
    ("χράομαι", "use shall I make", "NOT", "piece", "τί χρήσομαι"),
    ("νίπτω", "he washed", "NOT", "piece", "an example's verb"),
    ("φαίνω", "does this appear", "NOT", "piece", "an example's question"),
    ("φαίνω", "to give light", "FORM", "active", "intr. in act., to give light, shine"),
    ("ἀγαθός", "a good", "FORM", "neuter", "τὸ ἀγαθόν, a good, used as a noun"),
    ("ἀγαθός", "the good", "FORM", "neuter", "τὸ ἀγαθόν, the good"),
    # senses that have no passive (CLAUDE.md, the passive rule): a passive form leaves them out
    ("ὁράω", "to have sight", "FORM", "not passive", "intransitive"),
    ("καλέω", "to have received a name, to bear it", "NOT", "construction", "κέκλημαι, the perfect passive said as English's active: the passive chains say was called"),
    ("ἔχω", "to have charge of, keep", "FORM", "not passive", "no passive"),
    ("ἔχω", "to have to wife", "FORM", "not passive", "no passive"),
    ("ἔχω", "to have in one's house, to entertain", "FORM", "not passive", "no passive"),
    ("ἔχω", "to have means or power", "FORM", "not passive", "intransitive"),
    ("φθείρω", "to have suffered loss from shipwreck", "FORM", "not passive", "the passive's own English, already passive"),
    ("λαμβάνω", "to have given one, to get, gain, win", "FORM", "not passive", "no passive"),
    ("τρέφω", "to have within oneself, to contain, keep, have", "FORM", "not passive", "no passive"),
    ("ἔργον", "of women's work, weaving", "NOT", "label", "the entry's label for a use"),
    ("ψυχή", "of things dear as life", "NOT", "label", "the entry's label for a use"),
    ("εὐλογία", "of the alms collected", "NOT", "label", "the entry's label for a use"),
]


def key_of(lemma):
    return W.SPELLING.get(W.beta(lemma), W.beta(lemma))


with io.open(os.path.join(DECISIONS, "dec9_manual.jsonl"), "w", encoding="utf-8") as f:
    for lemma, sense, verdict, code, why in ROWS:
        keys = W.entry_keys(key_of(lemma))
        key = "mh/n" if lemma == "μήν" else keys[0]
        f.write(json.dumps({"lemma": lemma, "key": key, "sense": sense, "verdict": verdict, "code": code,
                            "why": why}, ensure_ascii=False) + "\n")
print(len(ROWS))
