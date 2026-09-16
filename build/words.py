#!/usr/bin/env python3
"""sources/  ->  data/<BOOK>/<chapter>.words.json — the word-by-word layer.

For every word of every verse in data/<BOOK>/<chapter>.json this records:

    form     the word as the verse prints it
    lemma    its dictionary form — what a concordance or lexicon files it under
    parse    what the form itself says: part of speech, tense, voice, mood,
             person, number, case, gender
    aspect   for verbs, what the tense means where English cannot show it, in the
             project's fixed wording (CLAUDE.md)
    senses   the opening senses of the lemma's Middle Liddell entry, in the
             lexicon's own order and with no regard to context

A concordance stops at the lemma. This layer takes the step after it: the lemma's
whole range, *and* what this particular form adds to it.

Where the lemma and parse come from:

    LXX books   data/<BOOK>/<chapter>.morph.txt — the project's own analysis, written
                a chapter at a time alongside the transcription.
    NT books    sources/morphgnt/ — MorphGNT, CC BY-SA.

Senses come from Middle Liddell (1889) in the Perseus Digital Library's XML (CC BY-SA
3.0 US) — only the translations inside an entry's numbered senses, never its etymology;
for the few lemmas it lacks, from LSJ as published by PerseusDL (CC BY-SA 4.0).

sources/ is not committed (NOTICE.md), so this writes a file that is, and
build/render.py reads that file — the site builds without sources/.

    python build/words.py                  # every chapter on the page
    python build/words.py GEN/1            # named chapters only
"""
import argparse
import json
import pathlib
import re
import sys
import unicodedata

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import render  # noqa: E402  — for ROOT, DATA, PAGE, BOOKS

SOURCES = render.ROOT / "sources"
MIDDLE_LIDDELL = SOURCES / "middle-liddell/Perseus_text_1999.04.0058.xml"

# Lemmas Middle Liddell lacks — or has, but tags with nothing usable — with LSJ's
# senses in LSJ's order, from LSJ as published by PerseusDL/lexica, CC BY-SA 4.0.
# Add an entry when words.py reports a lemma with no senses. Perseus's own markup
# sometimes wraps citation fragments in <tr>; those are left out here by hand, and
# the entry records which file the senses came from.
LSJ = {
    "ἀκατασκεύαστος": ["not properly prepared", "unwrought, unformed", "chaos",
                        "unpolished, unartificial"],
    # LSJ gives ἁγιάζω no gloss of its own: the entry reads "= ἁγίζω, LXX Ge. 2.3",
    # so the senses are the ones the cross-reference points at, under ἁγίζω.
    "ἁγιάζω": ["hallow, make sacred"],
    # Middle Liddell has no πράσινος at all. LSJ prints "leek-green, light green" and
    # cites this very verse for the stone: "λίθος π., = πρασῖτις, LXX Ge. 2.12". Its
    # later sense, "the green faction", is the Circus faction, a substantive plural.
    "πράσινος": ["leek-green, light green"],
    # Middle Liddell *has* ὀστέον, but tags only "the" — sliced out of "the bleached
    # bones of the dead" — and never tags its actual gloss, which the entry gives as
    # the Latin os, ossis. LSJ (eng16) tags "bone" among citation debris (d)Fr., a
    # mangled ´sthi) that is not part of any sense.
    "ὀστέον": ["bone", "the bleached bones of the dead"],
    # Middle Liddell has no entry for the pronoun of the second person at all. LSJ
    # (eng21) opens it "thou", and everything after is paradigm, not sense.
    "σύ": ["thou"],
    # Middle Liddell has no φλόγινος. LSJ (eng24) gives "flaming, fiery" and cites this
    # very verse for the sword, "ῥομφαία LXX Ge. 3.24"; then "flame-coloured" of garments.
    "φλόγινος": ["flaming, fiery", "flame-coloured"],
    # Middle Liddell's only entry is ποιμάν, "doric for ποιμήν", which glosses nothing and
    # points at an entry the abridgement does not have. LSJ (eng17) cites GEN 4:2 for
    # "shepherd": "π. προβάτων LXX Ge. 4.2".
    "ποιμήν": ["herdsman", "shepherd", "captain, chief", "master, lord", "pastor, teacher"],
    # No Middle Liddell entry. LSJ (eng26) cites GEN 4:21.
    "ψαλτήριον": ["stringed instrument, psaltery, harp"],
    # No Middle Liddell entry. LSJ (eng13): the weal of Isaiah 53:5 as well as GEN 4:23.
    "μώλωψ": ["mark of a stripe, weal, bruise", "blood-clot"],
    # No Middle Liddell entry. LSJ (eng5) cites GEN 4:24 and Matthew 18:22, and nothing else.
    "ἑβδομηκοντάκις": ["seventy times"],
    # No Middle Liddell entry. LSJ (eng5) cites GEN 5:22 for the first sense; the second is
    # the impersonal of decrees; "well pleased, satisfied" is the passive's, and the active's
    # used intransitively. The passive's medical "get relief" is left out.
    "εὐαρεστέω": ["to be well pleasing", "it seemed good, it was resolved",
                  "to be well pleased, satisfied"],
    # Middle Liddell has only the middle, διαναπαύομαι, "to rest awhile". LSJ (eng4) has
    # the active, which GEN 5:29 διαναπαύσει ἡμᾶς is, and gives the middle's gloss after it.
    "διαναπαύω": ["allow to rest awhile", "interrupt", "relieve", "rest awhile"],
    # Middle Liddell has both numerals but tags no translation in either: "Lat. octo,
    # eight", "Lat. tres, tria, three". LSJ tags them — ὀκτώ in eng16; τρεῖς is filed in
    # eng22 under its neuter, τρία, whose entry opens "three".
    "ὀκτώ": ["eight"],
    "τρεῖς": ["three"],
    # No Middle Liddell entry. LSJ (eng1) gives one sense and cites GEN 6:14.
    "ἀσφαλτόω": ["smear with pitch"],
    # No Middle Liddell entry. LSJ (eng4) gives one sense and cites GEN 6:16.
    "διώροφος": ["with two roofs or stories"],
}

# New Testament books: MorphGNT file and its book number.
MORPHGNT = SOURCES / "morphgnt"
NT = {"JHN": ("64-Jn-morphgnt.txt", "04")}

SHOWN = 5  # senses shown per word; the rest are counted, not dropped silently

_SENSES_NOTE = ("Senses: Middle Liddell (1889; Perseus Digital Library, CC BY-SA 3.0 US), in "
                "the lexicon's own order, without regard to context; LSJ (PerseusDL, "
                "CC BY-SA 4.0) where Middle Liddell has no "
                "entry. Middle/passive marks a tense in which the two voices share one "
                "form; masculine/feminine, an adjective whose form does not distinguish them.")
SOURCE_NOTE = {
    "lxx": "Dictionary form and parse: this project's own analysis. " + _SENSES_NOTE,
    "nt": "Dictionary form and parse: MorphGNT's analysis of the SBLGNT. " + _SENSES_NOTE,
}

# Perseus marks a few Latin equivalents, scraps of longer glosses, and glosses for a
# single construction as translations too. They are skipped by name, so the rule stays
# mechanical everywhere else. (Etymology needs no entry: it stands outside the senses.)
# Skim a new chapter's cards and add to this; keep it short.
NOT_SENSES = {
    "a)/nqrwpos": {"vir", "homo", "homo histrio",  # Latin
                   "in the world", "all"},      # scraps of constructions
    "ei)mi/": {"is no more",                    # οὐκέτ᾽ ἐστί — one construction
               "Troja fuit)"},                  # Latin
    "o)/noma": {"by name"},                     # ὀνόματι — one construction
    "poie/w": {"of"},                           # a scrap
    "kai/": {"que"},                            # Latin
    "gh=": {"ubi terrarum, where in (in what quarter of) the world, where on earth"},  # ποῦ γῆς
    "sko/tos": {"nocte premere"},               # Latin
    "e)pa/nw": {"part", "upper"},               # scraps of "the upper part"
    "o(/ti": {"knowing, thinking", "saying",    # ὅτι with a participle — constructions
              "came that", "has", "had)",
              "that they would", "that I would", "not only"},
    # Perseus opens ἄρχω with "in pass. sense:— to be first", a gloss for the passive
    # alone; the entry's first numbered sense is "to begin, make a beginning", marked
    # "both in Act. and Mid.", which is the ἤρξατο of GEN 2:3. Skipped by name, because
    # that same opening position carries the principal sense in most entries — λόγος's
    # "the word" among them — and must not be skipped by rule.
    "a)/rxw": {"to be first"},
    # βρέχω the same way: every gloss Perseus tags in sense I stands inside that sense's
    # ":—Pass." clause, and its active gloss ("to wet", Lat. rigo) is never tagged at all.
    # GEN 2:5 ἔβρεξεν is active, and sense II — "to rain, send rain" — is the one it uses.
    "bre/xw": {"to be wetted, get wet", "to bathe", "soaked"},
    # Fragments of the phrase the entry uses to distinguish πηγή *from* κρουνός, which
    # is what "(the spring or well-head)" glosses — a different word.
    "phgh/": {"(the spring", "well-head)"},
    "pla/ssw": {"made clay", "is a-moulding"},   # pieces of quoted examples
    # πορεύω files the deponent πορεύομαι, and its sense I is marked "Act." where the
    # text's form is middle. Sense II is left whole — the entry marks it "Pass. and
    # Mid.", so its opening gloss, "to be driven or carried", is available to a middle
    # form and is not skipped. Only the actives go.
    "poreu/w": {"to make to go, carry, convey", "to carry", "ferry over",
                "to bring, furnish, bestow, find"},
    # ἐκπορεύω likewise: the active "to make to go out, fetch out" heads the entry, and
    # the middle glosses it tags after it — "to go out", "forth, march out" — are the
    # ἐκπορεύεται of GEN 2:10.
    "e)kporeu/w": {"to make to go out, fetch out"},
    "a)nh/r": {"homo", "vir gregis",            # Latin, and the entry says "not homo"
               "a woman", "wife, a husband"},   # from "a man, opp. to a woman"
    # οὐ's entry lists the quasi-compounds it forms — οὐ δίδωμι "to withhold", οὐκ ἐῶ
    # "to refuse" — and their Latin equivalents, which are not senses of the negative.
    "ou)": {"to withhold", "to refuse", "nolo", "nego.", "nondissolution", "of its not"},
    "proskolla/w": {"to"},                      # from "to glue on or to"
    "o)ste/on": {"the"},                        # from "the bleached bones of the dead"
    # αἰσχύνω's sense I and its subsenses are the active — "to make ugly, disfigure",
    # "to dishonour" — and GEN 2:25 ᾐσχύνοντο is middle/passive. Sense II, the first
    # numbered sense open to that voice, is "to be ashamed, feel shame".
    "ai)sxu/nw": {"to make ugly, disfigure, mar", "to dishonour, tarnish", "to dishonour"},
    # φοβέω heads its actives "A. Act." — to put to flight, to terrify — and its passive
    # and middle "B. Pass. and Mid."; GEN 3:10 ἐφοβήθην is passive, so the actives go.
    "fobe/w": {"to put to flight", "to strike with fear, to terrify, frighten, alarm",
               "alarm", "by terror"},
    # ἅπτω's sense I is the active, "to fasten, bind fast", with a transitive middle
    # beside it; sense II is marked "Mid." and "c. gen." — the construction of GEN 3:3
    # ἅψησθε αὐτοῦ — and its opening gloss, "to fasten oneself to", is that form's.
    "a(/ptw": {"to fasten, bind fast", "to fasten for oneself", "to join", "to fasten", "on"},
    # στρέφω's senses A.I–VI are the active; "B. Pass. and Mid." opens "to turn oneself,
    # to turn round", which is GEN 3:24 στρεφομένην.
    "stre/fw": {"to turn about", "aside, turn", "to turn", "guide", "to sway",
                "to overturn, upset", "to twist", "to twist, torture", "to twist, plait",
                "to spin", "over", "to turn from the right course, divert, embezzle"},
    # ἐνδύω's sense I, "to go into, put on", is the intransitive and the middle; the
    # entry marks sense II "Causal in pres. ἐνδύω, fut. -δύσω, aor1 -έδυσα", which is
    # GEN 3:21 ἐνέδυσεν, the aorist that clothes another.
    "e)ndu/w": {"to go into", "to put on", "to wear", "to put on, assume",
                "to enter, to press into", "to enter"},
    # One entry for two words: ὥς, accented, the demonstrative "so, thus", and ὡς, the
    # relative "as" — the entry's own words. Perseus's opening summary mixes the two.
    # GEN 3:5 and 3:22 print the relative, so the demonstrative's glosses go.
    "w(s": {"thus, as, so that, since", "so, thus", "even so, nevertheless",
            "not even so, in no wise", "so . . as . .", "thus, for instance"},
    "meta/": {"in the midst of, among with gen., dat., and acc."},  # Perseus's summary
    "a)resto/s": {"quite", "satisfaction"},     # from the adverb "quite to his satisfaction"
    "a)na/": {"motion upwards"},                # describes the accusative; glosses nothing
    "fwnh/": {"rumpere vocem"},                 # Latin
    # Scraps from the opening senses of GEN 3's new words: pieces of longer glosses,
    # descriptions of a construction, and an etymology tagged as a translation.
    "te/knon": {"bairn", "beran, to bear)"},    # "(cf. Scottish bairn, from Anglo-S. beran, to bear)"
    "a)kou/w": {"thing heard", "pers. from whom it is heard"},  # "c. acc. of thing heard, gen. of pers."
    "a)pe/rxomai": {"departure from one", "and arrival at"},     # describes εἰς after the verb
    "a)postre/fw": {"back", "back from"},       # from "to turn one back", "back from flight"
    "katoiki/zw": {"as colonists", "in"},       # from "establish there as colonists", "plant one in"
    "w(rai=os": {"hora)"},                      # etymology
    "kru/ptw": {"having cloaked his"},          # from "having cloaked his head"
    "e(/ws": {"future"},                        # from "in future time"
    "lu/ph": {"condition"},                     # from "distress, sad plight or condition"
    "mh/": {"thought", "statement", "that one thinks a thing is not", "that it is not."},  # the note on μή and οὐ
    "o)fqalmo/s": {"before", "to one's face"},  # from "before one's eyes", "to one's face"
    "r(a/ptw": {"to make oneself", "having got"},  # from quoted examples
    "plhqu/nw": {"I am led by general opinion"},   # a construction
    "fu/llon": {"of leaves"},                   # from "the generation of leaves"
    # ἀνίστημι heads its senses "A. Causal in pres., imperf." — to make to stand up — and
    # "B. Intr. … in aor2 ἀνέστην": GEN 4:8 ἀνέστη is that aorist, so the causals go.
    "a)ni/sthmi": {"to make to stand up, raise up", "by", "to raise from sleep, wake up",
                   "to raise from the dead", "to set up, build", "to set up", "to build oneself",
                   "to build up again, restore", "to put up for sale", "to rouse to action, stir up",
                   "to rouse to arms, raise", "to make", "rise, break up", "rise", "make",
                   "emigrate, transplant", "rise and leave sanctuary", "to put up", "spring"},
    "dia/": {"through c. gen. through, by means of c. acc."},   # Perseus's summary
    # ἕτερος: Perseus tags scraps of "one of the two gates" and "one depends upon the
    # other" ahead of the sense itself, the other of two.
    "e(/teros": {"one of the", "one of two parties", "one", "the one"},
    "prose/xw": {"near", "bring", "to port", "brought", "to land here?"},  # pieces of "bring a ship near a place, to port"
    "ei)": {"shall do)", "had done)"},           # pieces of worked examples
    "dw=ron": {"the gifts of", "given by"},
    "fe/rw": {"motion", "is fair"},
    "boa/w": {"men ready to shout", "it proclaims"},
    "de/xomai": {"at the hand of"},
    "ste/nw": {"for"},
    "me/gas": {"women"},                        # from "tall women"
    "ai)ti/a": {"of"},
    "e)ponoma/zw": {"after"},
    "genna/w": {"the child", "he grow, get"},
    "si/dhros": {"wrought with much toil"},
    "paralu/w": {"part from", "to dismiss from the", "to set", "free from . .", "one beside another"},
    "kta/omai": {"to get one's"},
    "diaire/w": {"open", "into"},
    "o)rqo/s": {"standing with their walls entire"},
    "xa/skw": {"may", "I was all agape", "gaping fools"},  # from "then may earth yawn for me"
    "kiqa/ra": {"guitar)"},                     # "(whence guitar)"
    "xalko/s": {"a blacksmith."},               # from a cross-reference to χαλκεύς
    "e)cani/sthmi": {"bid one", "rise"},        # from "bid one rise from suppliant posture"
    "h(suxa/zw": {"the dead"},                  # from "of the dead"
    # GEN 5
    "qh=lus": {"of", "by women"},              # from "of or belonging to women", "murder by women"
    "metati/qhmi": {"he would", "have caused", "among", "and call them", "to put", "in place",
                    "for oneself"},             # pieces of worked examples
    "katara/omai": {"they pray"},               # "they pray that he may perish" — one construction
    "pentako/sioi": {"the senate of"},          # from "the senate of five hundred"
    # GEN 6
    "xa/ris": {"Grace", "well", "ill favoured), grace, loveliness"},  # Perseus's heading, and pieces of "well or ill favoured"
    "o(/sos": {"quantus"},                      # Latin
    # ἐκλέγω's opening glosses, "to pick or single out", and its sense II, "to levy taxes",
    # are the active; GEN 6:2 ἐξελέξαντο is middle, "to pick out for oneself, choose out".
    "e)kle/gw": {"to pick", "single out", "to levy taxes", "tribute", "to levy", "on"},
    "ei)sporeu/w": {"to lead into"},            # the active; GEN 6:4 is the middle, "to go into, enter"
    "qumo/w": {"to make angry", "passion", "irasci in cornua"},  # the active, τὸ θυμούμενον, and Latin
    "e)nqume/omai": {"was not conscious"},      # a worked example
    "o)nomasto/s": {"not to be named", "mentioned", "abominable"},  # οὐκ ὀνομαστός, one construction
    "fqei/rw": {"may ye perish! ruin seize ye!", "plague take thee! away with thee!", "thou depart",
                "off from", "to run headlong"},  # curses and idioms of the passive
}
# The key the lexicon files a word under, where that is not the key the lemma itself
# gives: a different spelling (Attic γίγνομαι for Koine γίνομαι), the active a deponent
# is filed beneath (πορεύω for πορεύομαι), or the entry a bare cross-reference points at
# (κατέναντι reads "= κατεναντίον" and glosses nothing itself). Each is recorded in
# reference/lexicon-notes.md with the entry it resolves to.
SPELLING = {
    "gi/nomai": "gi/gnomai",
    "ginw/skw": "gignw/skw",
    "ei(=s": "ei(/s",               # Perseus keys the numeral with an acute
    "poreu/omai": "poreu/w",        # deponent, filed under the active
    "e)kporeu/omai": "e)kporeu/w",  # likewise
    "kate/nanti": "katenanti/on",   # cross-reference; the entry has no <tr> of its own
    "peteino/n": "peteino/s",       # the neuter noun, filed under the adjective
    "e(/neken": "e(/neka",          # the Koine form of the Attic preposition
    "e)nte/llomai": "e)nte/llw",    # deponent, filed under the active
    "fobe/omai": "fobe/w",          # MorphGNT's middle, filed under the active
    "e)/xqra": "e)/xqrh",           # the entry is headed with the Ionic spelling
    "deilino/s": "deielino/s",      # cross-reference; "contr. for δειελινός" glosses nothing
    "o)rqw=s": "o)rqo/s",           # the adverb, filed inside the adjective's entry
    "e)nnako/sioi": "e)nako/sioi",  # the later spelling; the entry is headed with the earlier
    "e)kle/gomai": "e)kle/gw",      # MorphGNT's middle, filed under the active
    "ei)sporeu/omai": "ei)sporeu/w",  # likewise
    "qumo/omai": "qumo/w",          # likewise
    "e)pimelw=s": "e)pimelh/s",     # the adverb, filed inside the adjective's entry
    "e)nanti/on": "e)nanti/os",     # cross-reference; "adverb v. ἐναντίος" glosses nothing
    "nossia/": "neossia/",          # the contracted spelling; the entry is headed with νεοσσιά
    "kata/gaios": "kata/geios",     # cross-reference; "ionic for κατάγειος" glosses nothing
}

# Homographs where Perseus's *first* entry is a different word from the one the text
# uses, so the first sense of the first entry would be the first sense of the wrong
# word. This says which entry is the word; the lexicon still says what it means, and
# the reason for each is recorded in reference/lexicon-notes.md. Keep it short: a
# lemma belongs here only when the entries are genuinely different words.
ENTRY = {
    "xou=s": "xou=s2",   # xou=s1 is the Pitcher-feast, the liquid measure; GEN 2:7 is dust
    "o(/ti": "o(/ti2",   # o(/ti1 is ὅ τι, "for what"; the conjunction is the second entry
    "le/gw": "le/gw3",   # le/gw1 is "to lull to sleep", le/gw2 "to gather"; saying is the third
    "ou)": "ou)8",       # of eighteen entries, all but this one gloss an idiom (ou) ga/r,
                         # ou) mh/n …); ou)8 is the plain negative, "not", Lat. non
    "o(do/s": "o(do/s2",  # o(do/s1 is the attic ὀδός for οὐδός, "a threshold"; GEN 3:24 is the way
}

PUNCT = re.compile(r"[.,;:·!?—·]")


# --------------------------------------------------------------------------
# the parse, in plain English
# --------------------------------------------------------------------------

POS = {"N": "noun", "V": "verb", "A": "adjective", "RA": "article",
       "RP": "personal pronoun", "RD": "demonstrative pronoun", "RR": "relative pronoun",
       "RI": "interrogative pronoun", "C": "conjunction", "P": "preposition",
       "D": "adverb", "X": "particle", "I": "interjection", "M": "number"}
TENSE = {"P": "present", "I": "imperfect", "F": "future", "A": "aorist",
         "X": "perfect", "Y": "pluperfect"}
VOICE = {"A": "active", "M": "middle", "P": "passive", "E": "middle/passive"}
MOOD = {"I": "indicative", "S": "subjunctive", "O": "optative", "D": "imperative",
        "N": "infinitive", "P": "participle"}
PERSON = {"1": "1st person", "2": "2nd person", "3": "3rd person"}
CASE = {"N": "nominative", "G": "genitive", "D": "dative", "A": "accusative", "V": "vocative"}
NUMBER = {"S": "singular", "P": "plural", "D": "dual"}
GENDER = {"M": "masculine", "F": "feminine", "N": "neuter", "C": "masculine/feminine"}

# CLAUDE.md fixes the wording for aorist, imperfect and perfect; the other two follow it.
ASPECT = {
    "aorist": "one completed act seen whole, not a process observed in progress",
    "imperfect": "was, and kept on being: action going on in past time",
    "present": "going on, in progress",
    "perfect": "a standing resultant state, not a past event",
    "pluperfect": "a resultant state that stood in the past",
}
SHARED_VOICE = {"present", "imperfect", "perfect", "pluperfect"}


def describe(pos, tense="", voice="", mood="", person="", case="", number="", gender=""):
    t, v = TENSE.get(tense, ""), VOICE.get(voice, "")
    if v in ("middle", "passive") and t in SHARED_VOICE:
        v = "middle/passive"
    parts = [POS.get(pos, pos)] + [x for x in (
        t, v, MOOD.get(mood, ""), PERSON.get(person, ""),
        CASE.get(case, ""), NUMBER.get(number, ""), GENDER.get(gender, "")) if x]
    return " · ".join(parts), (ASPECT.get(t, "") if pos == "V" else "")


def morphgnt(pos, code):
    """MorphGNT: a two-letter part of speech and an eight-place parse —
    person, tense, voice, mood, case, number, gender, degree."""
    f = ["" if c == "-" else c for c in code.ljust(8, "-")]
    return describe(pos.rstrip("-"), tense=f[1], voice=f[2], mood=f[3], person=f[0],
                    case=f[4], number=f[5], gender=f[6])


# --------------------------------------------------------------------------
# the lexicon
# --------------------------------------------------------------------------

BETA_LETTERS = dict(zip("αβγδεζηθικλμνξοπρστυφχψως", "abgdezhqiklmncoprstufxyws"))
BETA_MARKS = {"̓": ")", "̔": "(", "́": "/", "̀": "\\", "͂": "=",
              "ͅ": "|", "̈": "+"}


def beta(word):
    """Unicode Greek -> the Beta Code the lexicon is keyed by (πνεῦμα -> pneu=ma)."""
    out = []
    for c in unicodedata.normalize("NFD", word.lower()):
        out.append(BETA_LETTERS.get(c) or BETA_MARKS.get(c, ""))
    return "".join(out)


def load_middle_liddell():
    """{Beta Code key: [translation, …]} from Perseus's Middle Liddell, in entry order.

    Only <tr> elements from the first <sense> on count: the headword line, principal
    parts and etymology stand before the senses and are not glosses.

    Homographs are stored twice: under the key the lexicon prints (xou=s1, xou=s2 …)
    and, for the first of them, under the bare key as well. An uncurated lemma still
    resolves to the first entry, exactly as before; ENTRY names the few lemmas where
    that entry is the wrong word.
    """
    xml = MIDDLE_LIDDELL.read_text(encoding="utf-8")
    entries = {}
    for m in re.finditer(r'<entry\b[^>]*\bkey="([^"]+)"[^>]*>(.*?)</entry>', xml, re.S):
        key, body = m.group(1), m.group(2)
        start = body.find("<sense")
        scope = body[start:] if start >= 0 else body
        glosses = (re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", t)).strip()
                   for t in re.findall(r"<tr\b[^>]*>(.*?)</tr>", scope, re.S))
        # One translation in the whole lexicon runs on into the voice label after it —
        # ἐξαποστέλλω's "to send quite away:—Pass." — so the label is cut off, not the gloss.
        glosses = (re.sub(r":\s*—\s*(?:Pass|Mid|Act)\.$", "", g) for g in glosses)
        senses = [g for g in glosses if g]
        entries.setdefault(key, senses)
        entries.setdefault(re.sub(r"\d+$", "", key), senses)
    return entries


def lexicon_senses(entries, lemma):
    key = SPELLING.get(beta(lemma), beta(lemma))
    key = ENTRY.get(key, key)
    if key not in entries:
        return None
    skip = NOT_SENSES.get(re.sub(r"\d+$", "", key), set())
    seen, out = set(), []
    for sense in entries[key]:
        if sense not in skip and sense not in seen:
            seen.add(sense)
            out.append(sense)
    return out


# --------------------------------------------------------------------------
# the sources
# --------------------------------------------------------------------------

# The kinds of trailing annotation a morph line may carry: a deliberate difference from
# the reference module, or from this project's own analysis of the same form elsewhere.
ANNOTATIONS = ("module", "corpus")


def parse_morph(path):
    """A morphology file as {verse: [(form, lemma, pos, code, notes)]}.

    `notes` maps each trailing annotation's kind to its text — "# module …" or
    "# corpus …", and a line may carry both. validate.py reports an annotated difference
    as a note rather than a failure, and fails if the difference it names is not there.
    An annotation of any other kind is kept under "?", so that it can be refused.
    """
    out = {}
    for n, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        body, *annotations = line.split("#")
        cols = body.split()
        if len(cols) != 5 or ":" not in cols[0]:
            raise SystemExit("%s line %d: expected 'verse pos parse form lemma'" % (path.name, n))
        notes = {}
        for text in (a.strip() for a in annotations):
            kind = text.split(None, 1)[0] if text else ""
            notes[kind if kind in ANNOTATIONS else "?"] = text
        ref, pos, code, form, lemma = cols
        out.setdefault(int(ref.split(":")[1]), []).append((form, lemma, pos, code, notes))
    return out


def read_morph(book, chapter):
    """The project's own analysis of an LXX chapter (see parse_morph), or None if it has
    not been written yet."""
    path = render.DATA / book / ("%d.morph.txt" % chapter)
    return parse_morph(path) if path.exists() else None


def lxx_tokens(book, chapter):
    morph = read_morph(book, chapter)
    if morph is None:
        return None
    return {verse: [(form, lemma, "", morphgnt(pos, code))
                    for form, lemma, pos, code, _ in words]
            for verse, words in morph.items()}


def nt_tokens(book, chapter):
    filename, number = NT[book]
    path = MORPHGNT / filename
    if not path.exists():
        return None
    out = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        cols = line.split()
        if len(cols) < 7 or cols[0][:2] != number or int(cols[0][2:4]) != chapter:
            continue
        _, pos, code, _, word, _, lemma = cols[:7]
        out.setdefault(int(cols[0][4:6]), []).append((word, lemma, "", morphgnt(pos, code)))
    return out


# --------------------------------------------------------------------------

def nfc(s):
    return unicodedata.normalize("NFC", s)


def same(a, b):
    """The source's form against ours; the verse-initial capital is ours to print."""
    a, b = nfc(a), nfc(b)
    return a == b or (a[:1].lower() == b[:1].lower() and a[1:] == b[1:])


def build(book, chapter, entries):
    verses = json.loads((render.DATA / book / ("%d.json" % chapter)).read_text(encoding="utf-8"))
    if book in NT:
        tokens, kind = nt_tokens(book, chapter), "nt"
        if tokens is None:
            return None, "sources/morphgnt/%s not found — see sources/README.md" % NT[book][0]
    else:
        tokens, kind = lxx_tokens(book, chapter), "lxx"
        if tokens is None:
            return None, ("data/%s/%d.morph.txt not found — the LXX layer needs the "
                          "project's own analysis (see that file's header in GEN/1)" % (book, chapter))

    # A name is glossed once per chapter in the reading text, but every card wants its
    # sense, so the map is built across the chapter; an entry marked bare carries no
    # gloss and contributes nothing to it.
    names = {n["greek"]: n["gloss"] for verse in verses
             for n in verse.get("names", []) if n.get("gloss")}

    out = []
    for verse in verses:
        number = int(verse["ref"].rsplit(":", 1)[1])
        ours = PUNCT.sub("", verse["greek"]).split()
        theirs = tokens.get(number, [])
        if len(ours) != len(theirs) or not all(same(t[0], o) for t, o in zip(theirs, ours)):
            raise SystemExit("%s: the source's words do not match the verse's Greek\n  ours:   %s\n"
                             "  source: %s" % (verse["ref"], " ".join(ours),
                                               " ".join(t[0] for t in theirs)))
        words = []
        for form, (_, lemma, _, (parse, aspect)) in zip(ours, theirs):
            if lemma in LSJ:
                # An explicit LSJ entry wins: the table holds the words Middle Liddell
                # lacks *and* the ones whose entry it tags with nothing usable, like
                # ὀστέον, where taking what Perseus tagged would give "bones of the dead"
                # for a single bone.
                senses, lexicon = LSJ[lemma], "LSJ"
                words.append({"form": form, "lemma": lemma, "parse": parse, "aspect": aspect,
                              "senses": senses[:SHOWN], "more": max(0, len(senses) - SHOWN),
                              "lexicon": lexicon})
                continue
            senses, lexicon = lexicon_senses(entries, lemma), "Middle Liddell"
            if senses is None and (lemma in names or form in names):
                # A name entry is keyed by the form the verse prints (Ἀσσυρίων), which
                # is not always the dictionary form the morphology gives (Ἀσσύριος).
                senses, lexicon = [names.get(lemma) or names[form]], "name"
            elif senses is None and lemma in LSJ:
                senses, lexicon = LSJ[lemma], "LSJ"
            elif senses is None:
                print("  note: no lexicon senses for %s (%s) — add it to LSJ in words.py"
                      % (lemma, verse["ref"]))
                senses, lexicon = [], "none"
            words.append({"form": form, "lemma": lemma, "parse": parse, "aspect": aspect,
                          "senses": senses[:SHOWN], "more": max(0, len(senses) - SHOWN),
                          "lexicon": lexicon})
        out.append({"ref": verse["ref"], "words": words})
    return {"source": SOURCE_NOTE[kind], "verses": out}, None


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("chapters", nargs="*", metavar="BOOK/CHAPTER",
                    help="chapters to build (default: everything on the page)")
    args = ap.parse_args()
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")

    targets = [(b.upper(), int(c)) for b, _, c in (a.partition("/") for a in args.chapters)]
    entries = load_middle_liddell()
    for book, chapter in targets or render.PAGE:
        layer, why = build(book, chapter, entries)
        if layer is None:
            print("SKIP  %s %d: %s" % (book, chapter, why))
            continue
        path = render.DATA / book / ("%d.words.json" % chapter)
        path.write_text(json.dumps(layer, ensure_ascii=False, indent=2) + "\n",
                        encoding="utf-8", newline="\n")
        count = sum(len(v["words"]) for v in layer["verses"])
        print("wrote %s (%d verses, %d words)" % (path.relative_to(render.ROOT).as_posix(),
                                                   len(layer["verses"]), count))


if __name__ == "__main__":
    main()
