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
    # Middle Liddell has no entry for the pronoun of the second person at all. LSJ
    # (eng21) opens it "thou", and everything after is paradigm, not sense.
    "σύ": ["thou"],
    # Middle Liddell has no φλόγινος. LSJ (eng24) gives "flaming, fiery" and cites this
    # very verse for the sword, "ῥομφαία LXX Ge. 3.24"; then "flame-coloured" of garments.
    "φλόγινος": ["flaming, fiery", "flame-coloured"],
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
    # A close form counts only where it covers the form the text uses, and the middle does
    # not say what the active means — so this one stays with LSJ.
    "διαναπαύω": ["allow to rest awhile", "interrupt", "relieve", "rest awhile"],
    # No Middle Liddell entry. LSJ (eng1) gives one sense and cites GEN 6:14.
    "ἀσφαλτόω": ["smear with pitch"],
    # No Middle Liddell entry. LSJ (eng4) gives one sense and cites GEN 6:16.
    "διώροφος": ["with two roofs or stories"],
    # No Middle Liddell entry. LSJ (eng5) gives one sense and cites GEN 7:11.
    "ἑξακοσιοστός": ["six hundredth"],
    # No Middle Liddell entry. LSJ (eng1): "height", of plants, animals and royal majesty,
    # then the senses below; GEN 7:23 renders the Hebrew yĕqûm, "living substance", with it.
    "ἀνάστημα": ["height", "protuberance, prominence", "high ground", "erection, building",
                 "eruption"],
    # No Middle Liddell entry. LSJ (eng5): "diminish", citing GEN 8:3 for the passive.
    "ἐλαττονόω": ["diminish"],
    # No Middle Liddell entry for either. LSJ (eng16) gives the adjective's senses and cites
    # GEN 9:23 for "looking backwards", of the face; the adverb, "backwards", is cited from the
    # same verse, πορεύεσθαι ὀπισθοφανῶς.
    "ὀπισθοφανής": ["seen from behind", "showing behind", "appearing behind or after",
                    "reversing the image", "looking backwards"],
    "ὀπισθοφανῶς": ["backwards"],
    # No Middle Liddell entry for these three. LSJ (eng5): ἐγγίζω, transitive first, then
    # "approach", and with an infinitive "to be on the point of", the sense of GEN 12:11;
    # ἐνισχύω; and ἐτασμός, which LSJ defines by the entry before it, ἔτασις, "trial, affliction".
    "ἐγγίζω": ["bring near, bring up to", "approach", "to be imminent", "approximate to",
               "to be next of kin", "to be on the point of"],
    "ἐνισχύω": ["strengthen, confirm", "prevail in, prevail among"],
    "ἐτασμός": ["trial, affliction"],
    # No Middle Liddell entry for these four. LSJ (eng1): ἁλυκός, "salt, brackish"; ἀποσκευή,
    # "removal, riddance", glossed "i.e. assassination", then "baggage", "household stuff" and
    # "ordure, filth". LSJ (eng21): σφαιρωτήρ, "thong, latchet", and "a ball" on a pillar,
    # "knop". LSJ (eng17): περάτης opens "= πορθμεύς", whose LSJ senses stand in its place,
    # "ferryman", "boatman, seaman", "conveyer", before its own "wanderer, emigrant", given as
    # the explanation of Ἑβραῖος, the word GEN 14:13 translates.
    "ἁλυκός": ["salt, brackish"],
    "ἀποσκευή": ["removal, riddance", "baggage", "household stuff", "ordure, filth"],
    "σφαιρωτήρ": ["thong, latchet", "a ball", "knop"],
    "περάτης": ["ferryman", "boatman, seaman", "conveyer", "wanderer, emigrant"],
    # No Middle Liddell entry for these three. LSJ (eng23): ὑπερασπίζω, "cover with a shield",
    # and with a genitive, "defend". LSJ (eng22): τριετίζω, "to be three years old". LSJ (eng4):
    # διχοτόμημα, "half of a thing cut in two", and "any portion of a thing cut up".
    "ὑπερασπίζω": ["cover with a shield", "defend"],
    "τριετίζω": ["to be three years old"],
    "διχοτόμημα": ["half of a thing cut in two", "any portion of a thing cut up"],
    # No Middle Liddell entry for these two. LSJ (eng11): κατάσχεσις, "holding back, restraining,
    # retention", "possession", "relation, attitude". LSJ (eng5): ἑκατονταέτης, one sense, "of a
    # hundred years", and "years old" after its citation of this verse, LXX Ge. 17.17.
    "κατάσχεσις": ["holding back, restraining, retention", "possession", "relation, attitude"],
    "ἑκατονταετής": ["of a hundred years, years old"],
    # No Middle Liddell entry for these two. LSJ (eng13): μοσχάριον, "little calf". LSJ (eng2):
    # βούτυρον, "butter", and "a plant".
    "μοσχάριον": ["little calf"],
    "βούτυρον": ["butter", "a plant"],
    # No Middle Liddell entry for these five. LSJ (eng17): προσοίγνυμι, "shut". LSJ (eng1):
    # ἀορασία, "inability to see, blindness", "failure to observe". LSJ (eng3): γελοιάζω, "jest".
    # LSJ (eng5): ἐπαύριον, "on the morrow"; εἰσσπάομαι, "draw into oneself".
    "προσοίγνυμι": ["shut"],
    "ἀορασία": ["inability to see, blindness", "failure to observe"],
    "γελοιάζω": ["jest"],
    "ἐπαύριον": ["on the morrow"],
    "εἰσσπάομαι": ["draw into oneself"],
    # Middle Liddell has no κἀγώ. LSJ (eng11): "crasis for καὶ ἐγώ", which glosses nothing;
    # the senses are καί's first and the pronoun's.
    "κἀγώ": ["and I"],
    # No Middle Liddell entry for these two. LSJ (eng1): ἀπογαλακτίζω, "wean from the
    # mother's milk"; ἀρχιστράτηγος, "commander-in-chief".
    "ἀπογαλακτίζω": ["wean from the mother's milk"],
    "ἀρχιστράτηγος": ["commander-in-chief"],
    # No Middle Liddell παρεπίδημος. LSJ (eng17): "sojourning in a strange place".
    "παρεπίδημος": ["sojourning in a strange place"],
    # No Middle Liddell entry for these four. LSJ (eng17): ποτιστήριον, "drinking-trough for
    # cattle", then the Latin "popina", which glosses nothing in English. LSJ (eng5): ἐνώτιον,
    # "ear-ring". LSJ (eng1): ἅβρα, "favourite slave"; ἀποσάττω, "unsaddle, unpack", "stop up,
    # caulk", "stuff with food", and in the middle "stuff oneself", left out of the active.
    "ποτιστήριον": ["drinking-trough for cattle"],
    "ἐνώτιον": ["ear-ring"],
    "ἅβρα": ["favourite slave"],
    "ἀποσάττω": ["unsaddle, unpack", "stop up, caulk", "stuff with food"],
    # Neither δόμα nor πυρράκης is in Middle Liddell. LSJ (eng4): δόμα, "gift", then
    # "payment". LSJ (eng17): πυρράκης, a masculine noun of the first declension, "red, ruddy".
    "δόμα": ["gift", "payment"],
    "πυρράκης": ["red, ruddy"],
    # No Middle Liddell entry for these two. LSJ (eng5): ἑκατοστεύω, "bear a hundredfold". LSJ
    # (eng3): γεώργιον, "field", then "orchard", "husbandry", "crop", and in the plural a "tax"
    # on land.
    "ἑκατοστεύω": ["bear a hundredfold"],
    "γεώργιον": ["field", "orchard", "husbandry", "crop", "tax"],
    # No Middle Liddell entry for these four. LSJ (eng17): πιότης, "fattiness", then "wealth,
    # prosperity"; πτερνίζω, "strike with the heel", "trip up, supplant", "heel an old shoe";
    # προσοχθίζω, "to be wroth with", and, of the phrase this verse has, "am weary" of. LSJ
    # (eng11): κατανύσσω, "stab, gouge", and in the passive "to be sorely pricked", "to be
    # bewildered, stunned".
    "πιότης": ["fattiness", "wealth, prosperity"],
    "πτερνίζω": ["strike with the heel", "trip up, supplant", "heel an old shoe"],
    "προσοχθίζω": ["to be wroth with", "am weary", "to be treated with contumely"],
    # Middle Liddell has ἐνύπνιον but not the verb. LSJ (eng5): ἐνυπνιάζω, "dream", with the
    # middle and passive used of the same thing; MorphGNT files the middle, ἐνυπνιάζομαι.
    "ἐνυπνιάζομαι": ["dream"],
    # The flock-breeding words of GEN 30, none of them in the abridgement.
    # LSJ (eng4) cites this very verse: "διάλευκος … LXX Ge. 30.32".
    "διάλευκος": ["quite white"],
    # LSJ (eng20) cites GEN 30:32 for the animals; the first sense is of sprinkling.
    "ῥαντός": ["sprinkled", "speckled or spotted"],
    # LSJ (eng12) has the active "in LXX Ge. 30.37"; the second sense is of metal plates.
    "λεπίζω": ["peel off the husk, skin or bark", "strip an object of its covering of metal plates"],
    # LSJ (eng12) cites GEN 30:37 and nothing else for the noun.
    "λέπισμα": ["peel"],
    # LSJ (eng11) files it καρύϊνος and cites the LXX ῥάβδος for the walnut-wood sense.
    "καρύινος": ["of nuts", "made of walnut-wood"],
    # LSJ (eng21) cites GEN 30:39 among the ash-coloured things.
    "σποδοειδής": ["ashy, ash-coloured"],
    # LSJ (eng5) has this verse alone: "ἐγκισσάω, have yearnings like one pregnant, LXX Ge. 30.38".
    "ἐγκισσάω": ["have yearnings like one pregnant"],
    # GEN 31, and LSJ cites this chapter for three of the four.
    # LSJ (eng11): "κατάβρωσις, eating up, devouring, LXX Ge. 31.15".
    "κατάβρωσις": ["eating up, devouring"],
    # LSJ (eng11): "κλοποφορέω, steal from, rob, τινα LXX Ge. 31.26".
    "κλοποφορέω": ["steal from, rob"],
    # LSJ (eng5): "ἐθισμός, accustoming, habituation … τὰ κατ' ἐθισμόν τινος LXX Ge. 31.35"; the
    # plural is "habits", "usages".
    "ἐθισμός": ["accustoming, habituation", "habits", "usages"],
    # LSJ (eng9) θηριάλωτος, cited from Leviticus 5:2, of the beast the wild beasts took.
    "θηριάλωτος": ["caught by wild beasts"],
    # GEN 32.
    # LSJ (eng5) cites this very verse: "ἐπισκάζω, limp upon, μηρῷ LXX Ge. 32.31(32)".
    "ἐπισκάζω": ["limp upon"],
    # GEN 33. LSJ (eng17) gives πόρευσις no gloss of its own: the entry reads "= πορεία … cf.
    # LXX Ge. 33.14", so the senses are Middle Liddell's πορεία.
    "πόρευσις": ["a walking, mode of walking", "a going, a journey, way, passage", "a march",
                 "a crossing of water, passage"],
    # GEN 34. No Middle Liddell entry. LSJ (eng22) gives τραυματίας two senses, "wounded man"
    # and "corpse of one slain".
    "τραυματίας": ["wounded man", "corpse of one slain"],
    # GEN 35. Middle Liddell has θλίβω but not the noun; LSJ (eng9) gives θλῖψις three senses
    # and cites this very verse for the third.
    "θλῖψις": ["pressure", "crushing, castration", "oppression, affliction"],
    # No Middle Liddell entry. LSJ (eng11) gives the comparative of κάτω three senses.
    "κατώτερος": ["lower", "more southerly", "later, younger"],
    # GEN 37. Middle Liddell has ἐνύπνιον but neither of these. LSJ (eng5) cites this very
    # verse: "ἐνυπνιαστής, dreamer, ib. 37.19". LSJ (eng20): ῥητίνη, "resin of the pine".
    "ἐνυπνιαστής": ["dreamer"],
    "ῥητίνη": ["resin of the pine"],
    # No Middle Liddell entry. LSJ (eng1) cites the next mention of this office, "LXX Ge.
    # 39.1": "chief cook", then, as a description and not a translation, "title of a great
    # officer in Oriental courts".
    "ἀρχιμάγειρος": ["chief cook"],
    # GEN 38. None of these four is in Middle Liddell. LSJ (eng3): γαμβρεύω, "form connexions
    # by marriage", in the middle "marry" (citing this verse's variant), in the passive "to be
    # connected by marriage". LSJ (eng25) gives χήρευσις no gloss of its own for its first
    # sense — "= χηρεία 1, LXX Ge. 38.14" — so that sense is Middle Liddell's χηρεία,
    # "widowhood"; the second is LSJ's own. LSJ (eng16): ὁρμίσκος, "small necklace", then
    # "signet-cord" citing this chapter, "collar". LSJ (eng17): προεκφέρω, "put out before",
    # citing 38:28, then "utter, pronounce before"; its passive is left with the actives.
    "γαμβρεύω": ["form connexions by marriage", "marry", "to be connected by marriage"],
    "χήρευσις": ["widowhood", "separation from a husband"],
    "ὁρμίσκος": ["small necklace", "signet-cord", "collar"],
    "προεκφέρω": ["put out before", "utter, pronounce before", "to be carried away headlong"],
    # GEN 39. No Middle Liddell entry. LSJ (eng1) cites this very verse: "ἀρχιδεσμοφύλαξ,
    # chief gaoler, LXX Ge. 39.21", and nothing more.
    "ἀρχιδεσμοφύλαξ": ["chief gaoler"],
    # GEN 40. None of these is in Middle Liddell. LSJ (eng1) cites this chapter for each of
    # the three titles: "ἀρχιοινοχόος, chief cup-bearer"; "ἀρχισιτοποιός, chief baker, LXX Ge.
    # 40.1"; "ἀρχιοινοχοεία, office of chief cup-bearer, LXX Ge. 40.13", the spelling LSJ
    # heads it with. ἀρχιδεσμώτης is filed inside ἀρχιδεσμοφύλαξ, "also ἀρχιδεσμώτης … LXX Ge.
    # 40.4", and so reads its "chief gaoler". LSJ (eng4): "διασάφησις, explanation,
    # interpretation, LXX Ge. 40.8". LSJ (eng25): "χονδρίτης, made of groats or coarse meal",
    # of bread, citing 40:16. LSJ (eng11) heads κανοῦν as κάνεον, "Att. contr. κανοῦν": "basket
    # of reed or cane, esp. bread-basket".
    "ἀρχιοινοχόος": ["chief cup-bearer"],
    "ἀρχισιτοποιός": ["chief baker"],
    "ἀρχιοινοχοΐα": ["office of chief cup-bearer"],
    "ἀρχιδεσμώτης": ["chief gaoler"],
    "διασάφησις": ["explanation, interpretation"],
    "χονδρίτης": ["made of groats or coarse meal"],
    "κανοῦν": ["basket of reed or cane", "bread-basket"],
    # GEN 41. None of these is in Middle Liddell, which has the verb εὐθηνέω and not the
    # noun, and γέννημα, the begotten thing, and not γένημα, the thing grown — LSJ keeps them
    # apart, "(cf. γέννημα)". LSJ (eng5): εὐθηνία, "prosperity, plenty", citing 41:29, then of
    # the body "good condition", "abundance", and "corn-supply"; its personified goddess,
    # "Abundance, Plenty", is a name and repeats the senses. LSJ (eng3): "γένημα, produce, of
    # the fruits of the earth". LSJ (eng4): δευτερόω, "do the second time: repeat", "change",
    # "give one a second blow", "slay", and "intr., occur twice", citing 41:32. LSJ (eng22):
    # "τοπάρχης, governor of a district, esp. in Egypt", citing 41:34. LSJ (eng1) heads ἄχει
    # as "ἄχει or ἄχι", "reed-grass", citing 41:2, "used for lamp-wick" — an Egyptian word;
    # ἀνεμόφθορος, keyed by Perseus without its nu (a)emo/fqoros), "blasted by the wind";
    # ἀποπεμπτόω, "give a fifth part of", citing 47:26, then "take a fifth part of", citing
    # 41:34. LSJ (eng21): "σιτοβολών, place for storing corn, granary", citing 41:56.
    "εὐθηνία": ["prosperity, plenty", "good condition", "abundance", "corn-supply"],
    "γένημα": ["produce"],
    "δευτερόω": ["do the second time: repeat", "change", "give one a second blow", "slay",
                 "occur twice"],
    "τοπάρχης": ["governor of a district"],
    "ἄχει": ["reed-grass", "lamp-wick"],
    "ἀνεμόφθορος": ["blasted by the wind"],
    "ἀποπεμπτόω": ["give a fifth part of", "take a fifth part of"],
    "σιτοβολών": ["place for storing corn, granary"],
    # GEN 42. None of these is in Middle Liddell. LSJ (eng11): "καταδέομαι, entreat earnestly",
    # citing 42:21. LSJ (eng21): σιτοδοσία, "gratuitous distribution of corn", then "allowance
    # of corn", citing 42:19. LSJ (eng1): ἀγορασμός, "purchasing", then "purchase", citing 42:19.
    # Three LSJ entries gloss nothing themselves and point elsewhere in LSJ, and, as with
    # ἁγιάζω, their senses are the ones the pointer reaches: "ἑρμηνευτής, = ἑρμηνεύς", citing
    # 42:23 (eng5); "κατασκοπεύω, = sq.", that is κατασκοπέω (eng11); "κατακενόω, strengthd.
    # for κενόω", citing 42:35 (eng11). κενόω's passive senses are left with the actives.
    "καταδέομαι": ["entreat earnestly"],
    "σιτοδοσία": ["gratuitous distribution of corn", "allowance of corn"],
    "ἀγορασμός": ["purchasing", "purchase"],
    "ἑρμηνευτής": ["interpreter", "dragoman", "court interpreter", "matrimonial agent, go-between",
                   "broker, commissionaire", "interpreter, expounder"],
    "κατασκοπεύω": ["view closely, spy out, reconnoitre", "reconnoitre", "keep a look-out", "inspect"],
    # GEN 43. LSJ (eng21): "συνεσθίω, eat together", citing 43:32. One translation.
    "συνεσθίω": ["eat together"],
    # LSJ (eng10) files ἵλεως under ἵλαος, "Att. and later ἵλεως", and Middle Liddell has
    # neither: "propitious, gracious", of things "propitious, blameless, atoned for", of men
    # "gracious, kindly". LSJ
    # (eng5): ἐγκρατεύομαι, "exercise self-control", citing 43:31, "force oneself", "starve
    # oneself", and "to be a member of the Encratite sect".
    "ἵλεως": ["propitious, gracious", "propitious, blameless, atoned for", "gracious, kindly"],
    "ἐγκρατεύομαι": ["exercise self-control", "force oneself", "starve oneself",
                     "to be a member of the Encratite sect"],
    # GEN 44. LSJ (eng9): "θηριόβρωτος, = θηρόβορος", a pointer, and θηρόβορος reads "eaten or
    # torn by wild beasts": one gloss, the "or" joining a half that is none by itself.
    "θηριόβρωτος": ["eaten or torn by wild beasts"],
    # LSJ (eng11): "κόνδυ, drinking-vessel", citing this chapter "as a measure"; one translation.
    # LSJ (eng16): "οἰωνισμός, = foreg.", citing 44:5, and the entry before it is οἴωνισμα,
    # "omen from the flight or cries of birds".
    "κόνδυ": ["drinking-vessel"],
    "οἰωνισμός": ["omen from the flight or cries of birds"],
    # GEN 45. None of these is in Middle Liddell. LSJ (eng1): ἀναγνωρίζω, "recognize", "Pass., LXX
    # Ge. 45.1", then "recognize or come to the knowledge of", "reveal oneself, make oneself known",
    # and causal "cause to recognize, reveal oneself to". LSJ (eng1): "ἀροτρίασις, = sq.", citing
    # 45:6, and the next entry is ἀροτριασμός, "ploughing, tillage". LSJ (eng10): "κατάλειμμα,
    # remnant", citing 45:7. LSJ (eng17): πορεῖον, "means of conveyance, carriage", and "load"; the
    # "trolleys" between them are an example's.
    "ἀναγνωρίζω": ["recognize", "recognize or come to the knowledge of", "reveal oneself, make oneself known",
                   "cause to recognize, reveal oneself to"],
    "ἀροτρίασις": ["ploughing, tillage"],
    "κατάλειμμα": ["remnant"],
    "πορεῖον": ["means of conveyance, carriage", "load"],
    # GEN 47. Middle Liddell has no σιτομετρέω. LSJ (eng21): "deal out portions of corn or
    # provisions", citing 47:12 for σ. σῖτον, one translation, "provisions" finishing what "corn"
    # began; "hold office of σιτομέτρης"; and transitive, "supply a force with provisions, victual
    # it". The passive's "have it served out as rations" is not a sense of the active ἐσιτομέτρει.
    "σιτομετρέω": ["deal out portions of corn or provisions", "hold office of sitometres (σιτομέτρης)",
                   "supply with provisions, victual"],
    # GEN 48. Middle Liddell has no βαρυωπέω. LSJ (eng2): "to be dim-sighted", citing 48:10, and
    # nothing more.
    "βαρυωπέω": ["to be dim-sighted"],
    # GEN 49. None of these is in Middle Liddell. LSJ (eng5): ἐρείδω, the active's senses only, as
    # GEN 49:6's ἐρείσαι is active: "cause to lean, prop", "fix firmly, plant", "prop up, support,
    # stay", "press hard, attack", "push, thrust", "infix, plant in" and an example's "inflict", "press
    # down, depress", "match, set against" (of wagers), and intransitive "press hard", "settle upon",
    # "exert pressure", "rest", "set to work, fall to", "become fixed". The pieces of examples
    # ("piling … against", "plant … firm", "fix … firmly", "hurled forth") and the middle's and
    # passive's senses (III, IV) are left out. LSJ (eng14, fetched for this word): νευροκοπέω,
    # "hamstring, hough", one translation. LSJ (eng23): ὑπερισχύω, "to be exceedingly strong", of
    # trees "to be too luxuriant", of persons "to be overbearing", c. gen. "to be stronger than,
    # prevail over".
    "ἐρείδω": ["cause to lean, prop", "fix firmly, plant", "prop up, support, stay", "press hard, attack",
               "push, thrust", "infix, plant in", "inflict", "press down, depress", "match, set against",
               "settle upon", "exert pressure", "rest", "set to work, fall to", "become fixed"],
    "νευροκοπέω": ["hamstring, hough"],
    # GEN 50. LSJ (eng5): ἐνταφιαστής, "undertaker, embalmer", one translation. LSJ (eng17): πανοικία,
    # "whole household", and its dative as an adverb, "with all the house", which is the dative's
    # and not GEN 50:8's nominative. LSJ (eng21): συναναφέρω, the active's senses, "carry up
    # together", metaph. "bring up together with itself", "refer to … at the same time", "certify at
    # the same time", "report"; the passive's and the astronomers' are left out, as GEN 50:25's
    # συνανοίσετε is active.
    "ἐνταφιαστής": ["undertaker, embalmer"],
    "πανοικία": ["whole household"],
    "συναναφέρω": ["carry up together", "bring up together with itself", "refer to at the same time",
                   "certify at the same time", "report"],
    # EXO 1. None of these is in Middle Liddell. LSJ (eng25): χυδαῖος, "poured out in streams,
    # abundant", citing Ex 1:7, then "common, ordinary" and "common, vulgar, coarse"; the adverb's
    # "pell-mell" is the adverb's. LSJ (eng11): κατοδυνάω, "afflict grievously", citing Ex 1:14, one
    # translation. LSJ (eng17): πλινθεία, "brickmaking", citing Ex 1:14, and "drawing up of an army
    # in square". LSJ (eng7): ζωογονέω, "propagate" or "engender living creatures", "breed",
    # "engender", "to be viviparous", "produce alive", "make alive, quicken", and "= ζωγρέω, preserve
    # alive", citing Ex 1:17; "producing" is a piece of the example of Zeus and Pallas.
    # EXO 13. Not in Middle Liddell, which has only πρωτόγονος. LSJ (eng17): πρωτογενής, "first-born,
    # primeval", "of persons, LXX Ex. 13.2"; "Fortuna Primigenia" is a cult title.
    "πρωτογενής": ["first-born, primeval"],
    # EXO 14. Neither is in Middle Liddell. LSJ (eng5): ἐνδοξάζομαι, "Pass., to be glorified", citing
    # Ex 14:4, one translation; the morphology files it under the active, ἐνδοξάζω, as the NT does. LSJ
    # (eng22): τριστάτης, "one who stands next to the king and queen, vizier", one translation, citing
    # 4 Ki 7:2.
    "ἐνδοξάζω": ["be glorified"],
    "τριστάτης": ["one who stands next to the king and queen, vizier"],
    # EXO 15. Neither is in Middle Liddell. LSJ (eng21): σκεπαστής, "shelterer, protector", citing Ex 15:2,
    # one translation. LSJ (eng1): ἁγίασμα, "= ἁγιαστήριον", a pointer to "holy place, sanctuary", which
    # Middle Liddell lacks too, then "holiness".
    "σκεπαστής": ["shelterer, protector"],
    "ἁγίασμα": ["holy place, sanctuary", "holiness"],
    # EXO 16. None of these is in Middle Liddell. LSJ (eng4): διατήρησις, "preservation", citing Ex 16:33.
    # LSJ (eng5): ἐγκρίς, "a cake made with oil and honey", citing Ex 16:31, one translation; "= ἀμανίτης,
    # Hsch." an explanation. LSJ (eng5): ἐλαττονέω, "receive less", citing Ex 16:18, "give less", "waste,
    # be consumed", "to be missing, defective", and the middle's "lack, want". LSJ (eng21): συσκήνιος, "=
    # sq.", read as σύσκηνος, "one who lives in the same tent, messmate, comrade", the entry it points to.
    "διατήρησις": ["preservation"],
    "ἐγκρίς": ["a cake made with oil and honey"],
    "ἐλαττονέω": ["receive less", "give less", "waste, be consumed", "to be missing, defective", "lack, want"],
    "συσκήνιος": ["one who lives in the same tent, messmate, comrade"],
    # EXO 17. Not in Middle Liddell. LSJ (eng11): καταλιθοβολέω, "throw stones at, stone", citing Ex 17:4.
    "καταλιθοβολέω": ["throw stones at, stone"],
    # EXO 18. None of these is in Middle Liddell. LSJ (eng1): ἀνυπομόνητος, "unbearable", and the active
    # "not enduring". LSJ (eng17): πρωΐθεν, "from morning", citing Ex 18:13, one translation. LSJ (eng21):
    # συναντιλαμβάνομαι, "help in gaining", "assist in supporting", "render assistance", and c. dat. "take
    # part with, help", citing Ex 18:22.
    "ἀνυπομόνητος": ["unbearable", "not enduring"],
    "πρωΐθεν": ["from morning"],
    "συναντιλαμβάνομαι": ["help in gaining", "assist in supporting", "render assistance", "take part with, help"],
    # EXO 19. Not in Middle Liddell. LSJ (eng3): γνοφώδης, "dark, gloomy", citing Ex 19:16, one translation.
    "γνοφώδης": ["dark, gloomy"],
    # EXO 20. Not in Middle Liddell. LSJ (eng13): μακροχρόνιος, "lasting a long time, lingering", "dwelling a
    # long time", citing Ex 20:12, "long-lived"; the neuter's "long duration" is the noun's. LSJ (eng1):
    # ἀναβαθμίς, "step, stair", citing Ex 20:26, one translation.
    "μακροχρόνιος": ["lasting a long time, lingering", "dwelling a long time", "long-lived"],
    "ἀναβαθμίς": ["step, stair"],
    # EXO 21. None of these is in Middle Liddell. LSJ (eng11): κατάκαυμα, "anything burnt", "fiery inflammation",
    # "burning", citing Ex 21:25, the plural's "burnt parts" and "burns" left to the plural; κερατίζω, "butt with
    # horns", and c. acc. "gore", citing Ex 21:28; κερατιστής, "one that butts", citing Ex 21:29, 36. LSJ (eng12):
    # λατομέω, "quarry", and "λ. λάκκον «hew» it «out»", citing Ex 21:33, whole. LSJ (eng17): προσαποθνήσκω, "die
    # besides" or "with", citing Ex 21:29, whole. LSJ (eng5): ἐξεικονίζω, "explain by a simile", Pass. "to be
    # fully shapen" or "formed", citing Ex 21:22, and "to be exactly like"; "formed in the image of" is a
    # participle's, in an example.
    "κατάκαυμα": ["anything burnt", "fiery inflammation", "burning"],
    "κερατίζω": ["butt with horns", "gore"],
    "κερατιστής": ["one that butts"],
    "λατομέω": ["quarry", "hew it out"],
    "προσαποθνήσκω": ["die besides or with"],
    "ἐξεικονίζω": ["explain by a simile", "to be fully shapen or formed", "to be exactly like"],
    # EXO 22. None of these is in Middle Liddell. LSJ (eng17): προσεμπίμπρημι, under προσεμπίπρημι, "set on fire
    # besides", citing Ex 22:6, the passive's "become still further inflamed" left to the passive. LSJ (eng24):
    # φερνίζω, "portion, endow", citing Ex 22:16. LSJ (eng1): ἀμνήστευτος, "unwooed; not sought in lawful
    # wedlock", the neuter plural's "without honourable wooing" left to the adverb; ἀνταποθνήσκω, "die" or "am
    # killed in requital", whole. LSJ (eng5): ἐκδανείζω, "lend out at interest", the middle's "borrow" left to the
    # middle; ἐνεχύρασμα, "pledge, thing pawned", citing Ex 22:26(25).
    "προσεμπίμπρημι": ["set on fire besides"],
    "φερνίζω": ["portion, endow"],
    "ἀμνήστευτος": ["unwooed; not sought in lawful wedlock"],
    "ἀνταποθνήσκω": ["die or am killed in requital"],
    "ἐκδανείζω": ["lend out at interest"],
    "ἐνεχύρασμα": ["pledge, thing pawned"],
    # EXO 23. Not in Middle Liddell. LSJ (eng9): θυσίασμα, "= θυσία II", a pointer to θυσία's "victim, offering",
    # which it reads. LSJ (eng17): πρωτογένημα, "firstfruits". LSJ (eng5): ἐχθρεύω, "to be at enmity with",
    # citing Ex 23:22.
    "θυσίασμα": ["victim, offering"],
    "πρωτογένημα": ["firstfruits"],
    "ἐχθρεύω": ["to be at enmity with"],
    # EXO 24. Not in Middle Liddell. LSJ (eng17): προσπορεύομαι, "go to, approach"; "apply" for a loan; "take up"
    # revenue cases; "make a start" or "get on with" the crops; "go in quest of" the office, "be candidate for" it;
    # "hunt for" paradoxes; "encroach on"; of a day, "draw near, approach".
    "προσπορεύομαι": ["go to, approach", "apply", "take up", "make a start or get on with", "go in quest of",
                      "be candidate for", "hunt for", "encroach on", "draw near, approach"],
    # EXO 25. Not in Middle Liddell. LSJ (eng3): γλυφή, "carving: carved work", "emblem, device", "the work" of one,
    # "hole cut" in a beam. LSJ (eng9): θυΐσκη, "censer". LSJ (eng11): καρυΐσκος, "Dim. of κάρυον", read as κάρυον's
    # "any kind of nut" and "walnuts" (its "filberts" is a phrase's, κ. πλατέα); κυμάτιον, "Dim. of κῦμα I.3", read
    # as κῦμα I.3's "waved moulding, cyma", and its own "volute", "groove". LSJ (eng12): λυχνία, "lampstand". LSJ
    # (eng21): σπονδεῖον, "cup from which the σπονδή was poured", "bowl", "pouring-cup". LSJ (eng1): ἀναφορεύς,
    # "bearer, bearing-pole"; ἄσηπτος, "not liable to decay or corruption", "undigested", its "of Acacia tortilis"
    # the phrase ξύλα ἄσηπτα's, citing this chapter. LSJ (eng5): ἐπίθεμα, "= ἐπίθημα, cover", "capital", "remedy for
    # external application", "addition", "higher bid", "shaft"; ἐπαρυστήρ, "vessel for pouring" oil into a lamp,
    # whole; ἐρυθροδανόω, "dye with madder, dye red". LSJ (eng23): ὑπόθεμα, "= ὑπόθημα, base", its "on the
    # security" a phrase's, ἐπὶ ὑποθέματι.
    "γλυφή": ["carving: carved work", "emblem, device", "the work", "hole cut"],
    "θυΐσκη": ["censer"],
    "καρυΐσκος": ["any kind of nut", "walnuts"],
    "κυμάτιον": ["waved moulding, cyma", "volute", "groove"],
    "λυχνία": ["lampstand"],
    "σπονδεῖον": ["cup from which the σπονδή was poured", "bowl", "pouring-cup"],
    "ἀναφορεύς": ["bearer, bearing-pole"],
    "ἄσηπτος": ["not liable to decay or corruption", "undigested"],
    "ἐπίθεμα": ["cover", "capital", "remedy for external application", "addition", "higher bid", "shaft"],
    "ἐπαρυστήρ": ["vessel for pouring oil into a lamp"],
    "ἐρυθροδανόω": ["dye with madder, dye red"],
    "ὑπόθεμα": ["base"],
    # EXO 26. Not in Middle Liddell. LSJ (eng1): αὐλαία, "curtain", "hunting-net", "in pl., screens" to protect a wall;
    # ἀγκωνίσκος, "= foreg.", ἀγκωνίσκιον, "Dim. of ἀγκών", read as Middle Liddell's ἀγκών, as κυμάτιον is read (Q20).
    # LSJ (eng11): κατακάλυμμα, "covering, veil", citing this chapter. LSJ (eng21): σύμβλησις, "union: a joint",
    # citing 26:24, "comparison", "reference to", "interpretation", "assistance". LSJ (eng5): ἐπίσπαστρον, "rope for
    # pulling", a fowler's "net", "= ἐπισπαστήρ 1", read as Middle Liddell's "the latch or handle by which a door is
    # pulled to", and "that which is drawn over, curtain, hanging", citing 26:36; ἐπιδιπλόω, "make double", citing
    # 26:9, "«fold» them «double»", "«multiply by» «two»"; ἐπικάλυμμα, "cover, veil", "covering" of an orifice, "of the
    # gills" and "of the opercula". ὑποκαλύπτω is in neither lexicon (26:12): plain text, with a note.
    "αὐλαία": ["curtain", "hunting-net", "screens"],
    "ἀγκωνίσκος": ["the bend of the arm, the elbow", "the arm", "any bend", "jutting angle", "the bend", "reach", "angle"],
    "κατακάλυμμα": ["covering, veil"],
    "σύμβλησις": ["union: a joint", "comparison", "reference to", "interpretation", "assistance"],
    "ἐπίσπαστρον": ["rope for pulling", "net", "the latch or handle by which a door is pulled to",
                    "that which is drawn over, curtain, hanging"],
    "ἐπιδιπλόω": ["make double", "fold double", "multiply by two"],
    "ἐπικάλυμμα": ["cover, veil", "covering", "gills", "opercula"],
    # EXO 27. Not in Middle Liddell. LSJ (eng4): δικτυωτός, "made in net-fashion", "latticed, trellised", and in θυρὶς
    # δ., "«lattice»-window", the adjective's own English; its neuter as a noun is left to its own use. LSJ (eng11):
    # καλυπτήρ, "covering, sheath", "cover", "lid", and "pl., tiles"; the metaphor 'pillars of society' is quoted,
    # not translated. LSJ (eng17): περιαργυρόω, "case, plate with silver", its passive citing 27:11; περιχαλκόω,
    # "«cover with brass» or «copper»", citing 27:6, one translation as LSJ prints it, the "or" kept as in κανοῦν.
    # LSJ (eng21): σανιδωτός, "planked, boarded over", citing 27:8. LSJ (eng1): ἄτρυγος, "without lees, clarified,
    # pure", citing 27:20. LSJ (eng20): ῥαφιδευτής, "stitcher, embroiderer", citing 27:16.
    "δικτυωτός": ["made in net-fashion", "latticed, trellised", "lattice"],
    "καλυπτήρ": ["covering, sheath", "cover", "lid", "tiles"],
    "περιαργυρόω": ["case, plate with silver"],
    "περιχαλκόω": ["cover with brass or copper"],
    "σανιδωτός": ["planked, boarded over"],
    "ἄτρυγος": ["without lees, clarified, pure"],
    "ῥαφιδευτής": ["stitcher, embroiderer"],
    # EXO 28. Not in Middle Liddell. LSJ (eng3): γλύμμα, "engraved figure, signet", "inscription". LSJ (eng4):
    # διανήθω, "spin out", its perfect passive participle citing 35:6. LSJ (eng11): κίδαρις, "Persian head-dress",
    # "turban of Jewish high priest", citing 28:4, "an Arcadian dance"; καθυφαίνω, "interweave, weave in", citing 28:17,
    # Pass. "to be inwoven"; κατάλιθος, "set with precious stones", citing 28:17; κοσυμβωτός, "tasselled, fringed";
    # κροσσωτός, "tasselled, fringed", and "stepped", of a wall; κροσσοί, "tassels, fringe", "lappets"; κόσυμβος,
    # "fringe", citing 28:35, "hair-net". LSJ (eng12): λιγύριον, "a precious stone (Dim. of λίγυρος)", citing 28:19,
    # with no translation marked, and λίγυρος "= λιγύριον": the description is all the English there is;
    # λιθουργικός, "«of» or «for a» λιθουργός", citing 28:11, the Greek word given a transliteration, as κάτοικος
    # is; the neuter's "sum spent on masonry", a noun, is left to the noun. LSJ (eng17): παρωμίς, "shoulderstrap",
    # citing 28:14; περικύκλῳ, "= πέριξ, round about", inside περίκυκλος; περιστήθιον, "breastband", citing 28:4;
    # περιστόμιον, inside περιστόμιος: "mouth of a vessel", "mouth-band", "region of the epiglottis", "collar" of a
    # garment, "edge". LSJ (eng22): τετράστιχος, "«in four rows» or «courses»", citing 28:17, one translation, as
    # περιχαλκόω. LSJ (eng25): χρυσόλιθος, "topaz", citing 28:20. LSJ (eng1): ἀσπιδίσκη, inside ἀσπιδίσκος, "boss,
    # disk", "small shield", "constellation"; ἀχάτης, "agate"; ἁλυσιδωτός, "wrought in chain fashion". LSJ (eng5):
    # ἐκτύπωμα, "figure in relief", "reflection". LSJ (eng16): ὀνύχιον, "small claw", pig's "trotters", "cloues"
    # (cloves) of garlic, "onyx", citing 28:20. LSJ (eng27): ᾤα, "sheepskin", "garment of this material", "drawers"
    # or "apron", and "= ὄα (B). 1, «border» or «fringe of a garment»", citing this chapter. LSJ (eng20): ῥοΐσκος
    # (A), "Dim. of ῥόα, «small pomegranate»: hence, «knob» or «tassel shaped like a pomegranate»", citing this
    # chapter. LSJ (eng2): βηρύλλιον, "Dim.", inside βήρυλλος, "gem of sea-green colour, beryl", read as κυμάτιον is
    # read (Q20).
    "γλύμμα": ["engraved figure, signet", "inscription"],
    "διανήθω": ["spin out"],
    "κίδαρις": ["Persian head-dress", "turban of Jewish high priest", "an Arcadian dance"],
    "καθυφαίνω": ["interweave, weave in", "to be inwoven"],
    "κατάλιθος": ["set with precious stones"],
    "κοσυμβωτός": ["tasselled, fringed"],
    "κροσσωτός": ["tasselled, fringed", "stepped"],
    "κροσσός": ["tassels, fringe", "lappets"],
    "κόσυμβος": ["fringe", "hair-net"],
    "λιγύριον": ["a precious stone"],
    "λιθουργικός": ["of or for a lithourgos (λιθουργός)"],
    "παρωμίς": ["shoulderstrap"],
    "περικύκλῳ": ["round about"],
    "περιστήθιον": ["breastband"],
    "περιστόμιον": ["mouth of a vessel", "mouth-band", "region of the epiglottis", "collar", "edge"],
    "τετράστιχος": ["in four rows or courses"],
    "χρυσόλιθος": ["topaz"],
    "ἀσπιδίσκη": ["boss, disk", "small shield", "constellation"],
    "ἀχάτης": ["agate"],
    "ἁλυσιδωτός": ["wrought in chain fashion"],
    "ἐκτύπωμα": ["figure in relief", "reflection"],
    "ὀνύχιον": ["small claw", "trotters", "cloves", "onyx"],
    "ᾤα": ["sheepskin", "garment of this material", "drawers", "apron", "border", "fringe of a garment"],
    "ῥοΐσκος": ["small pomegranate", "knob or tassel shaped like a pomegranate"],
    "βηρύλλιον": ["gem of sea-green colour, beryl"],
    # EXO 29. Not in Middle Liddell. LSJ (eng11): κάρπωμα, "fruit", "profit", "offering of fruits" (printed
    # "offering offruits"). LSJ (eng12): λάγανον, "a thin broad cake", its Latin "tracta" the Latin. LSJ (eng21):
    # στηθύνιον, "Dim. of στῆθος", citing 29:26, no translation of its own, read as Middle Liddell's στῆθος (Q20).
    # LSJ (eng25): χρῖσις, "smearing", "anointing", citing 29:21, "colouring, varnish, wash", "colour-washing". LSJ
    # (eng1): ἀφαίρεμα, "that which is taken away as the choice part", "tribute", "deduction", "«coarse grits made
    # from» ζέα", the Greek word given its English spelling, as βύσσος is; ἀφόρισμα, "that which is set apart: the
    # wave-offering", citing 29:24, one translation. LSJ (eng5): ἐνδελεχισμός, "= ἐνδελέχεια, «persistence»", and
    # "θυμίαμα -ισμοῦ «perpetual» incense", the genitive's English, citing 29:38. LSJ (eng16): ὁλοκαύτωσις,
    # "sacrifice of a burnt-offering" (printed "burntoffering"), citing 29:25.
    "κάρπωμα": ["fruit", "profit", "offering of fruits"],
    "λάγανον": ["a thin broad cake"],
    "στηθύνιον": ["the breast", "the breast as the seat of feeling, the heart"],
    "χρῖσις": ["smearing", "anointing", "colouring, varnish, wash", "colour-washing"],
    "ἀφαίρεμα": ["that which is taken away as the choice part", "tribute", "deduction",
                 "coarse grits made from zea (ζέα)"],
    "ἀφόρισμα": ["that which is set apart: the wave-offering"],
    "ἐνδελεχισμός": ["persistence", "perpetual"],
    "ὁλοκαύτωσις": ["sacrifice of a burnt-offering"],
    # EXO 30. Not in Middle Liddell. LSJ (eng12): λουτήρ, "«washing» or «bathing-tub»", citing 30:18, one
    # translation. LSJ (eng13): μυρεψικός, "«of» or «for unguents, aromatic»", citing 30:25; its "Balanites
    # aegyptiaca" is a plant's Latin name. LSJ (eng21): σίκλος, "= σίγλος", whose sense is "Hebr. «shekel», a weight",
    # citing 30:23. LSJ (eng25): χαλβάνη, "«the» resinous «juice of all-heal, Ferula galbaniflua»", citing 30:34, the
    # Latin name of the plant left to the Latin. LSJ (eng5): ἐξιλασμός, "= ἐξίλασις", whose senses are "propitiation,
    # atonement". κάτεργον and ἡδυσμός are in neither lexicon: plain text, with a note.
    "λουτήρ": ["washing or bathing-tub"],
    "μυρεψικός": ["of or for unguents, aromatic"],
    "σίκλος": ["shekel"],
    "χαλβάνη": ["the resinous juice of all-heal"],
    "ἐξιλασμός": ["propitiation, atonement"],
    # EXO 31. Not in Middle Liddell. LSJ (eng14): νηστός, "«spun»", citing 31:4, one translation. LSJ (eng4):
    # διασκευή, "«construction»", "«equipment»", "«furniture» or «vessels»", citing 31:7, "«rhetorical elaboration» of
    # a topic", "«set phrases»", "«new edition» or «recension» of a work", "«theatrical performance»"; its V, "=
    # ἀνασκευή", is a pointer and not a translation, and is left out.
    "νηστός": ["spun"],
    # EXO 32. Not in Middle Liddell. LSJ (eng25): χωνευτός, "«formed of cast metal, molten»", one translation.
    # LSJ (eng17): πολυπληθύνω, "«multiply»", citing 32:13, one translation.
    "χωνευτός": ["formed of cast metal, molten"],
    "πολυπληθύνω": ["multiply"],
    # EXO 33. LSJ (eng17): περιστολή, "«wrapping up»", "«laying out»" of a corpse, "«peristaltic action»", "«adornments»",
    # citing 33:6, "«restraint, decorum»"; its "ἐν π. «secretly»" a phrase's, left out. Middle Liddell has γνωστός, "later
    # form of γνωτός", and no adverb; LSJ (eng3), inside γνωστός: "Adv. -τῶς «clearly»", one translation.
    "περιστολή": ["wrapping up", "laying out", "peristaltic action", "adornments", "restraint, decorum"],
    "γνωστῶς": ["clearly"],
    # EXO 34. Not in Middle Liddell. LSJ (eng16): οἰκτίρμων, "«merciful»", citing 34:6; LSJ (eng17): πολυέλεος,
    # "«very merciful»", citing 34:6. One translation each.
    "οἰκτίρμων": ["merciful"],
    "πολυέλεος": ["very merciful"],
    # EXO 35. Not in Middle Liddell. LSJ (eng4), inside διατόναιον: "so διατόνιον, «curtain-hook» or «-ring», LXX Ex.
    # 35.11", one translation. LSJ (eng5): ἐμπλόκιον, "«a fashion of plaiting women's hair»", "«hair-clasp»", citing
    # 35:22. LSJ (eng17), inside περιδέξιος: "Subst. περιδέξιον, «armlet for the right arm»", citing 35:22; Middle
    # Liddell's περιδέξιος is the adjective alone, with no noun. LSJ (eng1): ἀρχιτεκτονία, "«architecture,
    # construction»", citing 35:32. LSJ (eng17): ποικιλτός, "«variegated, broidered»".
    "διατόνιον": ["curtain-hook or -ring"],
    "ἐμπλόκιον": ["a fashion of plaiting women's hair", "hair-clasp"],
    "περιδέξιον": ["armlet for the right arm"],
    "ἀρχιτεκτονία": ["architecture, construction"],
    "ποικιλτός": ["variegated, broidered"],
    # EXO 36. Not in Middle Liddell. LSJ (eng21): συμπορπάομαι, "Pass., «to be fastened together»", citing 36:13, the
    # voice the text uses. LSJ (eng17): περισιαλόομαι, "Pass., «to be broidered round the edge»", citing 36:13. LSJ (eng21):
    # συνυφή, "= συνύφασμα, «web»", metaph. "«construction»", "amorous «embrace»". ἐκκόλαμμα and συμπλεκτός are in
    # neither lexicon: plain text, from ἐκκολάπτω and συμπλέκω.
    "συμπορπάω": ["to be fastened together"],
    "περισιαλόω": ["to be broidered round the edge"],
    "συνυφή": ["web", "construction", "amorous embrace"],
    # EXO 37. Not in Middle Liddell. LSJ (eng20) gives ῥαφιδευτός no gloss of its own: "= ῥαπτός, ib. 37.21", so
    # the senses are Middle Liddell's ῥαπτός, its example's "a stitched" left out, as πόρευσις reads πορεία's
    # (GEN 33). LSJ (eng17): ποικιλτικός, "«skilful in embroidery»"; its ἡ -κή, "«embroidery»", is the feminine
    # made a noun, and this verse has the neuter, which LSJ gives only as "v.l. for ποικιλτά".
    "ῥαφιδευτός": ["stitched, patched", "strung together, continuous", "worked with the needle",
                   "an embroidered carpet"],
    "ποικιλτικός": ["skilful in embroidery"],
    "διασκευή": ["construction", "equipment", "furniture or vessels", "rhetorical elaboration", "set phrases",
                 "new edition or recension", "theatrical performance"],
    # EXO 12. None of these is in Middle Liddell. LSJ (eng3): γειώρας, "sojourner", "proselyte". LSJ
    # (eng4): δέσμη, "package, bundle", "a measure in Egypt", "in Medicine, handful"; Rahlfs prints the
    # accusative δεσμήν, the module δέσμην. LSJ (eng5): ἐνδόσθια, "= ἐντόσθια", a pointer to ἐντόσθιος,
    # "mostly, Subst. ἐντόσθια, τά, inwards, entrails", which names this verse's spelling; ἐπίμικτος,
    # LSJ's ἐπίμεικτος, "common to", "mixed", "combining the features of", "sociable, gregarious", the
    # adverb's "in combination" left to the adverb. LSJ (eng7): ζυμωτός, "fermented, leavened", citing
    # Ex 13:7. LSJ (eng12): λατρευτός, "= foreg.", a pointer to λατρευτικός, "servile", citing ἔργον
    # in this chapter. LSJ (eng17): πικρίς, "ox-tongue, Helminthia sepioides", "= κιχόριον", a pointer
    # to an entry LSJ does not have, and "sour soil".
    "γειώρας": ["sojourner", "proselyte"],
    "δέσμη": ["package, bundle", "measure", "handful"],
    "ἐνδόσθια": ["inwards, entrails"],
    "ἐπίμικτος": ["common to", "mixed", "combining the features", "sociable, gregarious"],
    "ζυμωτός": ["fermented, leavened"],
    "λατρευτός": ["servile"],
    "πικρίς": ["ox-tongue, Helminthia sepioides", "sour soil"],
    # EXO 10. None of these is in Middle Liddell. LSJ (eng21): σκῶλον, τό, "= σκῶλος", then its own
    # "stumblingblock, hindrance", citing Ex 10:7. Middle Liddell's σκῶλος, "a pointed stake", is the
    # masculine, and the text's σκῶλον is a predicate nominative, which no form of σκῶλος can be.
    # LSJ (eng26): ψηλαφητός, "that can be felt", citing the darkness of Ex 10:21.
    "σκῶλον": ["stumblingblock, hindrance"],
    "ψηλαφητός": ["that can be felt"],
    # EXO 9. None of these is in Middle Liddell. LSJ (eng5): ἐγκρατέω, "to be master of, exercise
    # control over", citing Ex 9:2 (Middle Liddell has the adjective ἐγκρατής, not the verb). LSJ
    # (eng11): καμιναία, "furnace", citing Ex 9:10. LSJ (eng24): φλυκτίς, "= φλύκταινα", a pointer,
    # then "boil", citing Ex 9:9; LSJ's φλύκταινα reads "blister" and "pustule". LSJ (eng21):
    # συνάντημα, "incident, occurrence", "visitation", citing Ex 9:14, "confirmation"; σπερματίζω,
    # "sow", and intransitive, of plants, "to be in seed", citing Ex 9:31 (the passive's "conceive,
    # become pregnant" is the passive's, and no active form's).
    "ἐγκρατέω": ["be master of, exercise control over"],
    "καμιναία": ["furnace"],
    "φλυκτίς": ["blister", "pustule", "boil"],
    "συνάντημα": ["incident, occurrence", "visitation", "confirmation"],
    "σπερματίζω": ["sow", "to be in seed"],
    # EXO 8. None of these is in Middle Liddell. LSJ (eng9): θημωνιά, which Rahlfs spells θιμωνιά,
    # "= foreg.", a pointer to θημών, "heap", citing Ex 8:10. LSJ (eng1): ἀνάψυξις, "cooling",
    # "exposure", "drying up", "relief, respite", citing Ex 8:11. LSJ (eng5): ἐπαποστέλλω, "send after",
    # "send to attack" ("send" is an example's piece). LSJ (eng17): παραδοξάζω, "make wonderful or
    # extraordinary", "will lay unheard-of inflictions upon" (De 28:59, the future's), "put a mark of
    # distinction between, separate" (Ex 9:4).
    "θιμωνιά": ["heap"],
    "ἀνάψυξις": ["cooling", "exposure", "drying up", "relief, respite"],
    "ἐπαποστέλλω": ["send after", "send to attack"],
    "παραδοξάζω": ["make wonderful or extraordinary", "lay unheard-of inflictions upon",
                   "put a mark of distinction between, separate"],
    # EXO 7. LSJ (eng5): ἐπόζω, "become stinking", citing Ex 7:18, one translation; not in Middle
    # Liddell.
    "ἐπόζω": ["become stinking"],
    # EXO 6. LSJ (eng11): καταδυναστεία, "oppression", citing Ex 6:7; Middle Liddell has the verb,
    # καταδυναστεύω, and not the noun. LSJ (eng16): ὀλιγοψυχία, "= λιποψυχία", a pointer, then
    # "faint-heartedness", citing Ex 6:9; λιποψυχία (eng12), not in Middle Liddell, reads "swooning".
    "καταδυναστεία": ["oppression"],
    "ὀλιγοψυχία": ["swooning", "faint-heartedness"],
    # EXO 5. LSJ (eng17): πολυπληθέω, "multiply", citing Ex 5:5, and "abound" in feet; πλινθουργία,
    # "v.l. for πλινθεία 1", a pointer to that sense, "brickmaking". Middle Liddell has only the
    # middle βδελύσσομαι, which does not say what the active of Ex 5:21 ἐβδελύξατε means; LSJ
    # (eng2) files it there, "later causal, in Act., cause to stink, make loathsome or abominable",
    # citing Ex 5:21, as διαναπαύω above.
    "πολυπληθέω": ["multiply", "abound"],
    "πλινθουργία": ["brickmaking"],
    "βδελύσσω": ["cause to stink, make loathsome or abominable"],
    # EXO 4. No Middle Liddell entry. LSJ (eng2): βραδύγλωσσος, "slow of tongue", citing Ex 4:10.
    "βραδύγλωσσος": ["slow of tongue"],
    # EXO 3. None of these is in Middle Liddell. LSJ (eng9): θλιμμός, "= θλῖψις", a pointer, citing
    # Ex 3:9, and θλῖψις is LSJ's too (GEN 35). LSJ (eng5): ἐργοδιώκτης, "taskmaster", citing Ex 3:7.
    # LSJ (eng11): κατεμβλέπω, "strengthd. for ἐμβλέπω", citing Ex 3:6, then "look down upon,
    # despise" from a later writer: the pointer is followed to LSJ's ἐμβλέπω, "look in the face, look
    # at", "consider", "look into", "look", and the entry's own sense kept after it.
    "θλιμμός": ["pressure", "crushing, castration", "oppression, affliction"],
    "ἐργοδιώκτης": ["taskmaster"],
    "κατεμβλέπω": ["look in the face, look at", "consider", "look into", "look", "look down upon, despise"],
    # EXO 2. None of these is in Middle Liddell. LSJ (eng9): θῖβις, "basket" plaited from papyrus,
    # citing Ex 2:3, 2:6; the Hebrew and Egyptian words after it are etymology, not senses. LSJ
    # (eng11): καταστενάζω, "sigh, mourn", citing Ex 2:23; καταχρίω, "anoint, smear, coat", citing
    # Ex 2:3. LSJ (eng22): τροφεύω, "serve as a wet-nurse, suckle", citing Ex 2:7. LSJ (eng1):
    # ἀσφαλτόπισσα, "= πισσάσφαλτος", a pointer, citing Ex 2:3, and πισσάσφαλτος (eng17) reads
    # "compound of asphalt and pitch".
    "θῖβις": ["basket"],
    "καταστενάζω": ["sigh, mourn"],
    "καταχρίω": ["anoint, smear, coat"],
    "τροφεύω": ["serve as a wet-nurse, suckle"],
    "ἀσφαλτόπισσα": ["compound of asphalt and pitch"],
    "χυδαῖος": ["poured out in streams, abundant", "common, ordinary", "common, vulgar, coarse"],
    "κατοδυνάω": ["afflict grievously"],
    "πλινθεία": ["brickmaking", "drawing up of an army in square"],
    "ζωογονέω": ["propagate", "engender living creatures", "breed", "engender", "to be viviparous",
                 "produce alive", "make alive, quicken", "preserve alive"],
    "ὑπερισχύω": ["to be exceedingly strong", "to be too luxuriant", "to be overbearing",
                  "to be stronger than, prevail over"],
    "κατακενόω": ["empty", "empty of", "to be emptied, made or left empty", "make empty by leaving, desert",
                  "empty by depletion", "carry off", "empty out, pour away", "make away with", "expend",
                  "waste away, shrivel", "make empty", "make void, of no effect"],
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
    "kai/": {"que", "ac", "aeque, perinde, simul"},  # Latin
    # κατὰ γῆν and γῆν πρὸ γῆς are idioms the entry quotes, not senses of the noun;
    # ποῦ γῆς likewise.
    # Middle Liddell splits one citation across two <tr>s — "to fill their ranks
    # full" — and the halves are not senses. A chain read them as "the numbers of
    # a body".
    "a)naplhro/w": {"to fill their", "full"},
    # Middle Liddell files a city's institutions under its numerals: the boards of
    # ten, thirty, forty and three hundred that governed Athens, the drachmae a
    # thousand stands for, the tenth-day naming rite, the second prize, the quart.
    # They are proper nouns of a constitution, as Uranus is of the sky, and a
    # numeral is left with the number it is.
    # δεύτερος αὐτός and τρίτος αὐτός, himself with one or two others: the
    # translations are fragments of the idiom, not senses of the ordinal.
    "tri/tos": {"with two others", "completing the tale"},
    "de/ka": {"the Ten"},
    "tria/konta": {"the council of thirty", "the Thirty", "the thirty tyrants"},
    "tessara/konta": {"the Forty"},
    "triako/sioi": {"the Three Hundred"},
    "xi/lioi": {"a thousand drachmae"},
    "de/katos": {"the tenth day after birth", "naming-day"},
    "deu/teros": {"the second prize", "place", "with another"},
    "te/tartos": {"a liquid measure", "quart)"},
    # GEN 36
    "h(gemoni/a": {"hegemony.", "imperium"},    # a repeat, and the Latin
    "ne/mw": {"due", "is freely bestowed", "portions", "is devoured"},
    "katoikodome/w": {"in"},                    # of "to build upon or in"
    "gh=": {"ubi terrarum, where in (in what quarter of) the world, where on earth",
            "on land, by land", "from land to land"},
    # πύλαι οὐρανοῦ and πρὸς οὐρανὸν βιβάζειν are quoted idioms, evehere ad Deos is
    # the Latin of the second, and Uranus is the god, not the sky.
    "ou)rano/s": {"Heavengate", "to exalt to heaven", "evehere ad Deos", "on high",
                  "Uranus"},
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
    "a(/ptw": {"engaged in", "on", "to fasten", "to fasten for oneself", "to fasten, bind fast", "to join", "to reach the mark",
               "touched on", "red-hot"},  # pieces of examples; examples' translations
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
    "w(rai=os": {"fruits gathered in due season", "hora)", "of the season", "yearling"},  # etymology; pieces of examples
    "kru/ptw": {"having cloaked his", "secret"},  # from "having cloaked his head"; a piece of the perfect participle
    "e(/ws": {"future"},                        # from "in future time"
    "lu/ph": {"condition"},                     # from "distress, sad plight or condition"
    # the note on μή and οὐ, then the labels of the constructions and their examples
    "mh/": {"thought", "statement", "that one thinks a thing is not", "that it is not.",
            "such things as",                   # from a relative clause's example
            "oratio obliqua.", "ut qui nihil sciam",              # Latin
            "fear", "apprehension",             # the verbs the construction follows
            "surely he is dead, is he not?", "surely he is not dead, is he?",
            "will you not be", "will you be", "how can a man help"},   # examples, rendered
    "o)fqalmo/s": {"before", "eyes", "sight", "the king's eye", "to one's face"},  # from "before one's eyes", "to one's face"; pieces of examples
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
    "ei)": {"if he is doing", "shall do)", "if he was doing", "if he did", "had done)",
            "if he were to do", "if he do", "if I had"},   # the paradigm, tense by tense
    "dw=ron": {"the gifts of", "given by"},
    "fe/rw": {"motion", "is fair"},
    "boa/w": {"men ready to shout", "it proclaims"},
    "de/xomai": {"at the hand of", "to accept", "to receive"},  # two bare repetitions
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
    # "yawn" is from "then may earth yawn for me"; the entry's own gloss, "to yawn,
    # gape", was inside the Latin element and is restored by MARKUP_LOST.
    "xa/skw": {"may", "I was all agape", "gaping fools", "yawn"},
    "kiqa/ra": {"guitar)"},                     # "(whence guitar)"
    "xalko/s": {"a blacksmith.",                # from a cross-reference to χαλκεύς
                "copper alloyed with tin)", "brass", "copper alloyed with zinc"},  # "bronze (i. e. copper alloyed with tin), not brass (i. e. copper alloyed with zinc …)": English defined, and a sense ruled out (EXO 27)
    "e)cani/sthmi": {"bid one", "rise"},        # from "bid one rise from suppliant posture"
    "h(suxa/zw": {"the dead", "finding rest", "by resting from war"},  # from "of the dead"; examples', a negated infinitive and a participle
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
    "qumo/w": {"angry", "irasci in cornua", "passion", "to make angry"},  # the active, τὸ θυμούμενον, and Latin; a piece of "to be wroth, angry"
    # GEN 7
    "a)noi/gnumi": {"and opened", "so as to open", "they tried to put back", "to tap", "took off"},  # pieces of Homeric examples; pieces of examples
    "chro/s": {"siccis oculis"},                # Latin
    "mei/s": {"in the course of", "monthly", "by the month", "the beginning", "the waning", "from the end of the month", "the three-and twentieth"},  # the Attic calendar
    "u(eto/s": {"a lasting", "a drizzling"},     # pieces of the distinction from ὄμβρος and ψακάς
    "katarra/kths": {"rushing down upon"},      # the reason the gull is named
    "e)calei/fw": {"to strike", "off"},         # from "to strike his name off the roll"
    # GEN 8
    # μιμνήσκω's active, "to remind", is another use; ἐμνήσθη is the middle, "to remind oneself of".
    "mimnh/skw": {"to remind, put", "in mind", "of", "to recall to memory, make famous"},
    "ko/rac": {'"pasce corvos," "go to the dogs," "go and be hanged,"'},  # an imprecation
    "u(postre/fw": {"bringing back"},          # a piece of an example
    "e)pe/xw": {"having put", "to his lips"},   # from "having put it to his lips"
    "e)/gkeimai": {"clothes"},                  # from "wrapped in clothes"
    "e)klei/pw": {"fails", "to appear"},        # from "fails not to appear"
    "pata/ssw": {"knocks"},                     # a form in an example
    "qe/ros": {"about"},                        # from "about summer"
    "e)nqume/omai": {"was not conscious"},      # a worked example
    "o)nomasto/s": {"not to be named", "mentioned", "abominable"},  # οὐκ ὀνομαστός, one construction
    "fqei/rw": {"may ye perish! ruin seize ye!", "plague take thee! away with thee!", "thou depart",
                "off from", "to run headlong"},  # curses and idioms of the passive
    # GEN 9
    # διατίθημι files MorphGNT's middle διατίθεμαι; its senses I–III are the active, and GEN 9:17
    # διεθέμην is the middle, "B. Mid. to arrange as one likes, to dispose of".
    "diati/qhmi": {"by will", "devise", "handled", "he was", "in their own places, dispose", "the devisor, testator", "to dispose", "to dispose of one's", "to manage", "to place separately, arrange", "to recite", "to treat", "treated", "with"},  # the last from "to settle a quarrel with one"; pieces of the middle
    "a)nti/": {"over against, opposite. c. gen.",  # Perseus's summary
               "as good as", "for",             # pieces of worked examples
               "over against, opposite", "against, in opposition to, as", "in return", "instead",
               "equal to, like", "counter"},    # "IN COMPOS.": the senses in compounds
    "plhro/w": {"animum explere", "having poured", "till it was full", "to be filled full of", "to fill full", "to fill full of"},  # Latin, and an example; pieces of sense I
    "fo/bos": {"to flight",                     # φόβονδε, another form
               "(the sensation of fear)"},      # glosses δέος, which the entry sets against φόβος
    "u(me/teros": {"you", "to your house", "raised by you"},  # pieces of examples; ὑμέτερόνδε
    "oi)=nos": {"beer"},                        # from "barley-wine, a kind of beer"
    "e)kxe/w": {"poured forth his", "forth"},   # pieces of "poured forth his arrows", "stream out or forth"
    "pi/nw": {"du vin)", "with", "drinking", "having finished drinking",  # pieces of examples
              "to be drunk"},                   # the perfect πέπωκα alone
    "mequ/skw": {"with"},                       # from "with nectar"
    "gumno/w": {"to strip", "he stript himself"},  # pieces of examples
    "to/con": {"spearmen)", "by guess"},        # an explanation, and τόξῳ, one construction
    "nw=ton": {"behind", "rear"},               # κατὰ νώτου, one construction
    "w(/ste": {"the result", "effect", "upon", "that one", "to"},  # descriptions and pieces of examples
    "pai=s": {"sons", "a boy-"},                # "sons of the Lydians", and "a boy-swineherd"
    "e)/cw": {"the heathen);"},                 # "(in NTest. the heathen)"
    # GEN 10
    "nh=sos": {"to swim", "floating land."},    # the etymology: "perhaps from νέω, to swim, as if floating land"
    "glw=ssa": {"of talking", "word of mouth", "mere hearsay", "tongue"},  # pieces of phrases in examples
    "xw/ra": {"there", "in the position", "esteem, nullo loco haberi", "its place", "order"},  # pieces of examples
    "e)/rxomai": {"over", "across", "come and", "je vais dire)"},  # pieces of examples, and French
    # GEN 11
    "xei=los": {"with the lips", "the lips", '"lip-service, "'},  # pieces of proverbs
    "pli/nqos": {"bricks", "to bake"},          # from "to make bricks", "to bake them"
    "o)pta/w": {"to roast", "cooking by means of fire", "dry heat",  # a piece of an example, and the
                "to boil in water"},            # note setting ὀπτᾶν against ἕψω
    "pu=r": {"things irresistible", "terrible", "fire and water", "raged furiously"},  # the entry's
                                                # description of a symbol, and pieces of examples
    "phlo/s": {"lutum", "coenum"},              # Latin
    "katabai/nw": {"came down", "she came down from", "is dismounted from", "come down from the loom?",
                   "in the course of speaking", "he ended", "begging"},  # pieces of examples
    "pu/rgos": {"a tower of defence from"},     # from "a tower of defence from deaths"
    "nu/mfh": {"spring-", "sea-", "tree-", "mountain-", "meadow-", "rapture", "caught by the Nymphs"},
    # GEN 12
    "oi)/xomai": {"abire)", "to have come", "to go", "come",  # the entry's contrasts with ἥκω and ἔρχομαι
                  "and gone", "he's", "away", "the absent"},  # pieces of examples
    "xra/omai": {"consulting", "using an oracle"},  # where the sense comes from, not the sense
    "peripoie/w": {"to make to remain over and above, to keep safe, preserve", "to save up, lay by",
                   "to put round", "upon, procure", "to get"},  # the active; MorphGNT files the middle
    # ἀφίστημι heads sense A "Causal in pres. and imperf., in fut. … aor1", and sense B "intr. …
    # in aor2 ἀπέστην"; GEN 12:8 ἀπέστη and 14:4 ἀπέστησαν are that aorist, so the causals go.
    "a)fi/sthmi": {"to put away, remove", "to hinder from", "to frustrate", "to depose", "removed",
                   "from your own", "to make to revolt, move to revolt", "to weigh out", "in full",
                   "to have", "weighed out to one", "to"},
    "lale/w": {"it shall be told"},             # the passive, in an example
    "peri/": {"around, round about with gen., dat., and acc."},  # Perseus's summary
    "h(mi/onos": {"a mule-", "mule-", "wild ass."},  # pieces of compounds, and a cross-reference
    "ka/mhlos": {"a camel-", "gamal."},          # a compound, and the Hebrew the word comes from
    "dei/knumi": {"will shew", "shewed that", "drank to", "he pledged"},  # pieces of examples
    # GEN 13
    "decio/s": {"side", "on the right", "unlucky", "on the left", "(sinister", "gauche)"},  # pieces of examples and Latin
    "xwre/w": {"gave way", "begone!", "he retired from", "along", "go", "have come",
              "take us into your hearts"},     # pieces of examples
    "pro/teros": {"prae.", "fore", "men of former times", "by the first", "a former marriage",
                  "on the day before", "superior to",   # pieces of examples
                  # the superlative's, πρῶτος, which Middle Liddell files under πρότερος
                  "first", "first, foremost", "at the front", "end", "outermost", "among the first",
                  "the first men", "the first prize", "the first part, beginning", "the first, highest",
                  "the extremities", "the chief", "first, at present, just now", "at first",
                  "first, in the first place", "before", "first, for the first time"},
    "a)rgu/rion": {'"silver"'},                 # a quotation mark from an example
    "xrusi/on": {"my golden one! my little treasure!"},  # an endearment in an example
    "sumporeu/omai": {"with"},                  # the case it takes
    "a(/ma": {"at"},                            # a piece of an example
    "du/namai": {"I possibly can", "avails", "bear", "having influence", "he could", "is worth", "it cannot be, is not to be", "men of power", "powerful, mighty", "they could", "to be able", "to mean"},  # pieces of examples
    "ma/xh": {"fights", "a battle", "battle", "battle with"},  # pieces of examples
    "katastre/fw": {"subdued and made", "am constrained to", "a close periodic"},  # pieces of examples
    "skhno/w": {"be"},                          # a piece of an example
    "a)nable/pw": {"in the face"},              # a piece of an example
    # GEN 14
    "basileu/s": {"king", "more of a king, more kingly", "most kingly", "the king's son, prince"},  # pieces of examples and other degrees
    "po/lemos": {"war", "a war;", "war, —"},     # pieces of examples
    "sumfwne/w": {"for", "it was agreed"},      # pieces of examples
    "triskaide/katos": {"the", "th day"},       # pieces of "the 13th day"
    "katako/ptw": {"cut in pieces", 'to cut in pieces, "cut up, "'},  # pieces of examples
    "i)sxuro/s": {"strength, vigour", "strongest points", "strongly, with all force", "exceedingly"},  # the neuter as a noun, the superlative, the adverb
    "fre/ar": {"a spring)"},                    # a piece of "(opp. a spring)"
    "feu/gw": {"to flee", "the endeavour to flee", "the attempt", "the accomplishment", "flee and",
               "can escape", "escaped from his hands", "the exiles", "the accused, defendant",
               "the accuser, prosecutor", "is accused of"},  # pieces of examples
    "e)mpi/ptw": {"upon", "into", "violently"},  # pieces of examples
    "i(/ppos": {"chariot-horses", "the chariot", "riding", "a thousand", "the hippopotamus",
                "anything large", "coarse", "horsechestnut, horselaugh"},  # the plural's, phrases and compounds
    "a)riqme/w": {"they got", "counted"},        # pieces of examples
    "i)/dios": {"private", "a private man", "private buildings", "private affairs, private interests",
                "one's own property", "one's own affairs", "oneself", "for my own part",
                "especially, peculiarly", "by oneself, privately, separately, on one's own account",
                "apart from"},                   # the noun's, the adverb's and pieces of examples
    "e)pipi/ptw": {"over"},                     # a piece of an example
    "diw/kw": {"to chase", "the prosecutor", "he who impeaches the words"},  # pieces of examples
    "lao/s": {"o people!", "oyez!", "men, people;"},  # a proclamation, and a repeat
    "e)kfe/rw": {"to declare one's"},           # a piece of an example
    "kti/zw": {"founded by emigrants from", "having invented"},  # pieces of examples
    "paradi/dwmi": {"transmission", "into another's hands", "to allow", "to", "permits"},  # pieces of examples
    "e)xqro/s": {"'tis hateful"},               # a piece of an example
    "so/s": {"for thee"},                       # a piece of an example
    # GEN 15
    "r(h=ma": {"word for word"},                 # a phrase
    "misqo/s": {"wages", "of our hired service", "pay", "the pay", "one obol", "three)", "the fee", "fee"},  # pieces of examples
    "a)polu/w": {"of being", "by payment of", "against one", "in defence", "from"},  # pieces of examples
    "klhronome/w": {"heir", "of"},              # pieces of "to be heir of"
    "eu)qu/s": {"straight", "straight to", "straight towards", "leading straight", "as soon as"},  # εὐθύ, of place, and ἐπεὶ εὐθέως
    "a)lla/": {"not only"},                     # οὐ μόνον … ἀλλά
    "pisteu/w": {"in", "believe", "believed", "he would be believed", "I am believed likely to", "he trusted",
                 "have", "committed", "I am entrusted with"},  # pieces of examples
    "sw=ma": {"life", "body", "soul", "bodily", "a body"},  # pieces of examples
    "h(/lios": {"East", "hot sunny days"},       # pieces of examples
    "skoteino/s": {"the darkness"},             # the neuter as a noun
    "pa/roikos": {"near", "with neighbours"},   # pieces of examples
    "kako/w": {"befouled"},                     # a piece of an example
    "kri/nw": {"picked out, chosen", "they decide the question", "contest", "judge", "to have",
               "decided, come to issue", "judging of", "judge that"},  # pieces of examples
    "w(=de": {"so . . , as . .", "so", "just as thou art, at once", "thus off"},  # pieces of examples
    "ei)rh/nh": {"peace", "a peace;", "it"},     # pieces of examples
    "qa/ptw": {"burning the body"},             # a piece of an example
    "a(marti/a": {"a fault committed by", "fault"},  # pieces of examples
    "e)pei/": {"began", "had"},                 # pieces of examples
    "flo/c": {"to put", "out", "the flame"},    # pieces of examples
    # GEN 16
    "sugklei/w": {"shut off and intercepted", "muffled", "shut the doors", "the part that was", "closed up"},  # pieces of examples
    "u(pakou/w": {"to listen", "to give ear to", "to comply"},  # repeats
    "gasth/r": {"bellies", "his belly", "it"},  # pieces of examples
    "a)tima/zw": {"thou speakest", "in dishonour of", "will not disdain", "deem", "unworthy"},  # pieces of examples
    "a)dike/w": {"wrong-doing", "righteous dealing", "to do", "in"},  # pieces of examples
    "ko/lpos": {"her robe so as to form a fold", "deep-folded", "their folded robes", "in her bosom"},  # pieces of examples
    "a)podidra/skw": {"by stealth"},            # a piece of an example
    "plh=qos": {"in force", "in great numbers", "upon the whole, in general", "usually, mostly"},  # adverbial phrases
    "e)pakou/w": {"to hear", "from"},           # pieces of examples
    # GEN 17
    "a)/memptos": {"in regard of", "less blameworthy", "so as to merit no blame, right well", "without censure"},  # an example's piece, the comparative, the adverbs
    "pi/ptw": {"to fall in", "to fall and lie", "the fallen", "to fall by", "fell", "cadunt austri)", "to fail", "to fall out of"},  # pieces of examples
    "perite/mnw": {"cutting off", 'for oneself, "lifting"'},  # pieces of an example
    "paidi/on": {"a little"},                   # half of "a little or young child"
    "oi)ki/a": {"establishments"},              # a piece of an example
    "a)llo/trios": {"of", "malis ridere alienis", "the help of another's", "as if it absolutely belonged to another", "unfavourably", "favourably"},  # pieces of examples, Latin, the adverbs
    "gela/w": {"a laugh being raised"},         # a piece of an example
    "nai/": {"yea by . ."},                     # an oath formula
    "e)niauto/s": {"times", "during", "every year"},  # pieces of examples
    # GEN 18
    "ka/qhmai": {"the judges, the court"},     # the participle as a noun
    "meshmbri/a": {"at noon"},                  # a piece of an example
    "proskune/w": {"to him as king"},           # a piece of an example
    "a(/ra": {"explanation", "in questions", "the anxiety", "who is there"},  # descriptions and pieces of examples
    "pare/rxomai": {"passed away", "the past", "now gone by", "in time past, of old", "past events"},  # participles and pieces of examples
    "ni/zw": {"feet", "from", "washed off", "off his", "washing part"},  # pieces of examples
    "de/ndron": {"fruit-trees", "timber)"},     # pieces of an example
    "e(/neka": {"as far as depends on", "as far as", "went"},  # pieces of examples
    "speu/dw": {"urge on", "to be urged on", "urge", "anxiously", "you urge, contend", "in haste, eagerly"},  # pieces of examples, the passive, the participle
    "fura/w": {"so as to make", "to make", "into a", "paste"},  # pieces of examples
    "me/tron": {"the length", "the prime"},     # pieces of examples
    "a(palo/s": {"gently"},                     # the adverb
    "parati/qhmi": {"meats set before one", "of one's own", "the serving-men", "to lay before", "to place upon"},  # pieces of examples
    "pari/sthmi": {"having brought", "into view", "near", "present circumstances", "opinion", "it occurs", "since it was in their power, since the opportunity offered"},  # pieces of examples
    "a)pokri/nw": {"answer", "be", "distinct", "let", "parted from the throng", "to be separated and brought", "to reply"},  # pieces of examples; a bare repetition of the sense before it
    "w(/ra": {"'tis time", "at", "at the right time", "hour", "in", "in due time, in good time", "in the day", "seasons", "spring", "summer", "the time for", "time", "winter", "year", "youth!"},  # pieces of examples; the three seasons Middle Liddell names in passing
    "o)/pisqen": {"those who are left behind", "shall", "rear ranks"},  # pieces of examples
    "pre/sbus": {"the wise", "of age", "nihil) antiquius habere", "more highly than . ."},  # pieces of examples, Latin, the adverb
    "probai/nw": {"are far gone", "is wearing fast", "went on", "advanced", "to be", "gone", "kept making advances", "kept extending", "he was set over", "ruled"},  # pieces of examples
    "gunaikei=os": {"of", "bona dea", "with women"},  # half of "of or belonging to", Latin, a piece of an example
    "ge": {"and not otherwise", "the least"},   # pieces of examples
    "ghra/skw": {"to be so", "grew old"},       # pieces of examples
    "a)rne/omai": {"to deny that"},             # a construction
    "sunapo/llumi": {"to destroy one's", "as well as oneself", "also", "with"},  # pieces of examples
    "a)po/llumi": {"to drive", "ruined", "oh destined to a miserable end!", "oh villain, scoundrel!"},  # pieces of examples
    "a)ni/hmi": {"loosed", "from", "baring her", "flaying", "are let range at large"},  # pieces of examples
    "spodo/s": {"the ashes", "of a bibulous"},  # pieces of examples
    "a(/pac": {"once"},                         # a repeat
    # GEN 19
    "pu/lh": {"(a house-door)", "house-door.", "the pass round the mountains", "the gates", "the pass"},  # pieces of examples
    "katalu/w": {"having been dismissed", "to take", "down", "is", "guest", "may I take my rest"},  # pieces of examples
    "o)rqreu/w": {"rising up early"},           # the middle participle
    "pe/ssw": {"to cook oneself", "to have", "to nurse", "to lead a sodden"},  # pieces of examples
    "koima/w": {"lay", "asleep"},               # pieces of an example
    "a(/pas": {"everything, unumquodque"},     # Latin
    "suggi/gnomai": {"comrades"},               # the participle as a noun
    "a)re/skw": {"will we make up among ourselves", "the resolution", "grateful, acceptable"},  # pieces of examples, the participle
    "mhdei/s": {"what is naught"},              # a piece of an example
    "ske/ph": {"under shelter from", "protection"},  # pieces of examples
    "suntri/bw": {"to rub", "together", "to stave", "in", "to have", "broken"},  # pieces of examples
    "a)poklei/w": {"to shut", "out", "to get", "debarred from"},  # pieces of examples
    "zhte/w": {"seeking", "what is sought for"},  # pieces of examples
    "e)ktri/bw": {"to produce", "by rubbing", "to bring", "to a wretched end"},  # pieces of examples
    "o)/rqros": {"at dawn", "dawn", "in the morning", "morning early"},
    "ui(o/s": {"A son"},                        # Perseus's sense-letter, not a gloss
    "o(ra/w": {"To see"},                       # likewise  # pieces of examples; a piece of an example
    "krate/w": {"the lady of the house", "the conquerors", "'tis better to"},  # pieces of examples
    "fei/domai": {"taking care", "refrain from", "sparingly", "shrink"},  # pieces of examples, the adverb
    "sw/zw": {"who save", "from", "what is likely to save", "to rescue"},  # pieces of examples
    "e)ggu/s": {"by a great deal, nothing like it", "very nearly"},  # pieces of examples
    "ka/minos": {"baking"},                     # a piece of an example
    "ou)dei/s": {"ne ullus"},                   # Latin
    "deu=ro": {"to (have come hither and) be here"},  # an explanation
    "e)/leos": {"pity for . ."},                # a construction
    # GEN 20
    # "auris, the ear" is the Latin with the English after it, and "the ear"
    # stands on its own as the next sense.
    "ou)=s": {"in the ear", "auris, the ear"},  # a piece of an example, and the Latin
    "e)nora/w": {"in", "he saw"},               # pieces of examples
    "a)gnoe/w": {"not recognising", "he perceived", "knew well", "learn all", "ignorantly, by mistake"},  # pieces of examples, the adverb
    "a)lhqeu/w": {"he was right about", "to prove"},  # pieces of examples
    "u(/pnos": {"in sleep", "Sleep"},           # a piece of an example, and Perseus's sense-letter
    "profh/ths": {"interpreter", "interpreters"},  # pieces of examples
    "sunoike/w": {"marriage", "he is associated", "being versed", "are associated"},  # pieces of examples
    # GEN 21
    "e)piskope/w": {"visited"},                 # a piece of an example
    "ge/lws": {"with laughing", "ridiculous"},  # pieces of examples
    "sugxai/rw": {"with", "to wish", "joy of"},  # pieces of examples
    "qhla/zw": {"sucking"},                     # a piece of an example
    "a)sko/s": {"the bag", "a bag made of the skin", "to flay"},  # pieces of examples
    "o(/rkos": {"an oath by", "oath", "the tender", "to bind", "to abide by"},  # pieces of examples
    "r(i/ptw": {"has been made"},               # a piece of an example
    "bolh/": {"stroke", "touch"},               # pieces of an example
    "a)naboa/w": {"a war-cry"},                 # a piece of an example
    "klai/w": {"weeping", "well beaten", "he shall weep", "he shall repent it"},  # pieces of examples
    "du/namis": {"strength", "as far as lies in one"},  # pieces of examples
    "o)/mnumi": {"swears"},                     # a piece of an example
    "e)le/gxw": {"to treat", "with contempt", "to put", "to shame"},  # pieces of examples
    "a)faire/w": {"having taken", "off", "to have", "taken from one"},  # pieces of examples; "to have it taken from one" cut in two, whole in MARKUP_LOST
    "a)mfo/teros": {"on both sides, utrinque", "both ways, in utramque partem"},  # adverbial phrases
    "martu/rion": {"evidence", "here is a proof, namely"},  # pieces of examples
    "o)ru/ssw": {"trench", "to have", "dug"},  # pieces of examples
    # GEN 22
    "peira/zw": {"let trial be made", "the tempter"},  # the passive's example, the participle
    "a)gaphto/s": {"one must be content"},     # a piece of an example
    "paralamba/nw": {"by inheritance", "undertakings"},  # pieces of examples
    "sxi/zw": {"divided", "into", "branches", "were divided"},  # pieces and translations of examples
    "au)tou=": {"exactly"},                     # a piece of an example
    "paida/rion": {"a child"},                  # a piece of an example
    "ke/ras": {"horns", "horn doors", "true", "in flank", "towards the wing", "in column"},  # pieces of examples
    "e)mo/s": {"possessive", "for me"},         # pieces of examples
    # GEN 23
    "ko/ptw": {"smote", "on",                   # pieces of an example
               "to lay", "waste"},              # "«to lay» it «waste»", cut, whole in MARKUP_LOST (EXO 27)
    "kth=sis": {"success in"},                  # a piece of an example
    "ta/fos": {"a funeral-feast"},              # a piece of an example
    "kwlu/w": {"to hinder", "prevent", "from"},  # pieces of examples
    "diplo/os": {"so as to be double", "bent double", "mutual"},  # pieces of examples
    "me/ros": {"considerations of rank", "his turn of duty"},  # pieces of examples
    "a)/cios": {"worth", "quantivis pretii"},   # pieces of examples, Latin
    "do/kimos": {"most approved", "really, truly"},  # a piece of an example, the adverb
    "e)/mporos": {"a trafficker"},              # a piece of an example
    "kuro/w": {"the end hath been fixed", "determined"},  # pieces of examples
    # GEN 24
    "bou/lomai": {"he willed", "would you have", "nobis volentibus est", "according to my wish",
                  "quid sibi vult haec res", "I had rather", "than"},  # pieces of examples, Latin
    "e)qe/lw": {"to wish that . .", "they cared not", "they were unable", "future", "will revert",
               "que veut-il dire"},             # pieces of examples, French
    "a)gaqo/s": {"it is good", "regular"},      # pieces of examples
    "koimi/zw": {"suffer", "to rest—", "straverunt aequora venti)", "to lay", "asleep"},  # pieces of examples, Latin
    "o)ye/": {"too late", "serum diei"},        # a piece of an example, Latin
    "e)pikli/nw": {"to", "closed", "to prick", "inclined at an angle to"},  # pieces of examples, the passive's
    "e(toima/zw": {"made his", "arrangements"},  # pieces of an example
    "o)/yis": {"in appearance", "sights", "from what they saw", "presence"},  # pieces of examples
    "e)pitre/xw": {"at", "in haste, eagerly", "runs over"},  # pieces of examples
    "kaqaire/w": {"we lowered", "to take", "down", "close", "swallow", "utterly", "prize"},  # pieces of examples
    "draxmh/": {"denarius", "franc"},           # Latin and French equivalents
    "o(lkh/": {"towards"},                      # a piece of "a drawing on or towards"
    "e)perwta/w": {"about"},                    # a piece of "to ask a thing or about a thing"
    "o(rki/zw": {"I adjure", "by"},             # pieces of an example
    "qera/pwn": {"free service;", "the companion", "esquire", "the charioteer", "devoted to the service of"},  # pieces of examples
    "e)rwta/w": {"of", "question", "the question", "to be asked"},  # pieces of examples; the passive, and a piece of sense II
    "fhmi/": {"shall we say", "what one says", "you would say, would think", "think", "they say, it is said",
              "on dit", "said", "said yes", "not", "say no", "say yes or no"},  # pieces of examples, French
    "periti/qhmi": {"to put", "round"},         # pieces of an example
    "a)ntile/gw": {"answer"},                   # a piece of "to declare in opposition or answer"
    "skeu=os": {"the vessel", "vessel"},        # pieces of examples
    "me/nw": {"wait ye for", "they waited for", "I wait", "long", "it remains"},  # pieces of examples, the impersonal
    "e)pibai/nw": {"to", "they bring", "bring to"},  # pieces of examples
    "a)nalamba/nw": {"back"},                   # a piece of "to call back"
    "periba/llw": {"having thrown", "to wreck", "on", "putting on their", "round", "having", "around",
                   "with", "to put", "\"to compass\""},  # pieces of examples
    "parakale/w": {"\"vocatus atque non vocatus, \"", "to attend one", "summoned"},  # pieces of examples, Latin
    "braxi/wn": {"the shoulder"},               # a piece of "βραχίων ὤμου, the shoulder"
    "e)kkeno/w": {"to pour out", "to shoot all"},  # pieces of examples
    "a)ntle/w": {"exhaurire labores"},          # Latin
    "parqe/nos": {"new"},                       # a piece of an example
    "dei/lh": {"early", "late", "in the course of the afternoon"},  # pieces of examples
    "a)lh/qeia": {"in very truth", "in truth and reality", "the character of the"},  # adverbial phrases, a piece
    # GEN 25
    "presbu/ths": {"elder, older", "eldest", "higher, more important", "greater than", "an ambassador",
                   "a chief, president", "an elder of the Jewish Council", "an elder of the Church, presbyter"},
                                                # πρεσβύτης is "= πρέσβυς I"; the rest of πρέσβυς is other senses
    "plh/rhs": {"polluted", "fill"},            # pieces of examples
    "me/llw": {"was just going", "thinkest", "did you", "think you might", "could", "were", "was destined",
               "we were able to", "a certainty", "it must be that", "I must have", "a probability", "be",
               "belike", "thou art like", "were like to", "I thought you would", "shouldn't I",
               "be sure I have", "are", "in futurity", "might", "be delayed", "delays are going on"},  # pieces of examples
    "punqa/nomai": {"by inquiry", "from", "I heard", "they had", "heard of", "learn that", "learn"},  # pieces of examples
    "u(pere/xw": {"over", "so as to protect", "hold above", "he had", "above", "the ground", "to overtop",
                  "be prominent", "the more powerful"},  # pieces of examples
    "e)la/sswn": {"in a thing", "less account", "at less distance", "less"},  # pieces of examples
    "o(/de": {"nearer", "more remote;", "deictic", "what can be pointed out.", "voici", "what is before one",
              "here is", "here", "of mine", "just", "before one", "these preparations which I see",
              "immediately to come", "in", "with these words"},  # pieces of examples, French
    "geu/w": {"let us try"},                    # a piece of an example
    "e)pilamba/nomai": {"from", "traverse", "corripere campum"},  # pieces of examples, Latin
    "e(/yw": {"we boiled some"},                # a piece of an example
    "dasu/s": {"with all the leaves", "the copses", "thick"},  # pieces of examples
    # GEN 26
    "xwri/s": {"by themselves", "apart", "in reserve", "without evidence", "to distinguish", "help",
               "will", "quality"},              # pieces of examples
    "xro/nos": {"with chronological accuracy", "by the dates", "for a while", "at once, once for all",
                "for", "long?", "in time, at last", "time, after a time", "of time", "in time, at length",
                "a certain time", "a while", "hereafter", "delays"},  # pieces of examples
    "spei/rw": {"to engender, beget them", "to be born", "spargere voces", "the arable part of",
                "of lost labour"},              # pieces of examples, Latin
    "zhlo/w": {"to be jealous", "to esteem", "for"},  # pieces of examples
    "dunato/s": {"able", "fit for service", "quantum fieri possit", "strongly, powerfully", "the ablest-bodied men", "the chief men of rank and influence"},  # pieces of examples, Latin, the adverb; a piece of an example
    "ma/xomai": {"against", "with the sanction, under the auspices", "will fight", "the force that had",
                 "come into action"},           # pieces of examples
    "fa/skw": {"alleging", "pretending", "he said", "alleged"},  # pieces of examples
    "ph/gnumi": {"crystallises", "fix in", "fix on", "fixed", "frozen", "hard", "having their", "impaled", "on", "pitch", "stiffen", "stuck fast", "to be irrevocably", "to build oneself", "to fix", "to pitch their", "to stick", "upon", "was"},  # pieces of examples; a piece of an example
    "tro/pos": {"wise", "way", "in no wise, by no means, on no account", "how?", "in a manner",
                "after the manner", "in its ways", "ways", "fitly, duly", "sort", "temper", "taste"},  # pieces of examples
    "swthri/a": {"a way", "means of safety", "guarantee for the safe keeping", "ways of preserving"},  # pieces of examples
    "e)ri/zw": {"with", "in"},                  # pieces of examples
    "mise/w": {"hated (would not suffer)", "grudging"},  # pieces of examples
    # GEN 28
    "proskale/w": {"I have called"},            # a piece of an example
    "sunagwgh/": {"a levying", "a gathering in of", "a forming", "in column"},  # pieces of examples; "a forming in column" cut, whole in MARKUP_LOST
    "a)panta/w": {"from", "anyone that meets you, any chance person"},  # pieces of examples
    "du/w": {"plunged into", "plunge into", "go in to", "he got himself unto", "got behind", "setting", "sank",
             "wilt", "put on", "to enter, come over", "upon", "filled"},  # pieces and translations of examples; "to enter, come over or upon", cut, whole in MARKUP_LOST
    "a)fikne/omai": {"from", "the person reached"},  # pieces of examples
    "u(poti/qhmi": {"beginning"},               # a piece of an example
    "e)pixe/w": {"shed over", "throw", "oneself"},  # pieces of examples
    "eu)/xomai": {"to pray that", "long"},      # pieces of examples
    "fobero/s": {"formidable", "terror"},       # pieces of examples
    "a)/kron": {"the highest", "furthest point"},  # pieces of "the highest or furthest point"
    # GEN 29
    "e)caei/rw": {"having bade", "rise", "excites"},  # pieces of examples
    "a)napau/w": {"hinder from", "to give", "rest", "relief"},  # pieces of senses I and I.1
    "suna/gw": {"to join", "begin", "to match", "one against the other"},  # pieces of the battle sense
    "po/qen": {"from what", "how can it be? impossible!"},  # a piece of an example, and one
    "u(giai/nw": {"in health", "soundness"},    # a piece of sense 1, and a usage note
    "kth=nos": {"an ox", "sheep"},              # pieces of "a single beast, as an ox or sheep"
    "prose/rxomai": {"go to"},                  # a piece of "to come or go to"
    "perilamba/nw": {"surround", "you get hold of"},  # a piece of sense I.2, and an example
    "a)sqenh/s": {"too weak", "the weaker sort", "the poor"},  # pieces of senses I.1 and I.2
    "ei)=dos": {"nature", "course"},            # pieces of senses II and II.2
    "belti/wn": {"to improve, advance"},        # the verb the entry cross-refers to
    "o)li/gos": {"too few to", "little"},       # a piece of sense I.2, and a bare repetition
    "ga/mos": {"marriage with"},                # a piece of "marriage with him"
    "paralogi/zomai": {"to be so misled"},      # the passive of the sense before it
    "e)rgasi/a": {"a working"},                 # a piece of "a working of a material"
    "e)rga/zomai": {"to do", "to"},             # pieces of sense II.2
    # GEN 30
    "stere/w": {"robbed of", "to have taken from one"},  # pieces of the passive
    "go/nu": {"the knees", "by [clasping] the knees", "on", "knees"},  # pieces of examples
    "tu/xh": {"by ill-luck"},                   # a piece of an example
    "maka/rios": {"my good sir, my dear sir", "happy you", "the rich and better educated"},  # pieces of examples
    "makari/zw": {"to deem", "while we bless"},  # a piece of "to bless, to deem or pronounce happy"
    "mh=lon": {"sweet", "round as apples."},    # pieces of examples
    "i(kano/s": {"sufficient", "with sufficient power", "sufficiently versed in", "very tolerable", "enough", "large enough", "security"},  # pieces of examples
    "misqo/w": {"to offer to let", "offers", "for pay", "to let out"},  # pieces of senses I and II
    "pe/mptos": {"the fifth day"},              # a piece of an example
    "dwre/w": {"to be given", "presented", "to be presented with"},  # the passive of sense I
    "o)/neidos": {"of reproach", "the reproach"},  # pieces of examples
    "ei)/sodos": {"entrance, a right"},         # a piece of "entrance, a right or privilege of entrance"
    "ou)qei/s": {"good for nothing", "nobodies"},  # pieces of examples
    "poimai/nw": {"has been traversed"},        # a piece of an example
    "kle/ptw": {"stole", "to let", "down secretly", "thievish"},  # pieces of examples
    "leuko/s": {"glassy", "bright, limpid"},    # pieces of sense I
    "r(a/bdos": {"the measure"},                # a piece of an example
    "poiki/los": {"in-wrought", "the Poecile"},  # a piece of sense II.2, and the great hall at Athens
    "lhno/s": {"trough;"},                      # the entry's first word, repeated whole below it
    "mi/gnumi": {"to mix", "with", "to join"},  # pieces of senses I and II
    "a)/shmos": {"sign", "with"},               # pieces of "without mark or sign"
    "e)pi/shmos": {"with", "inscription on them"},  # pieces of an example
    "ploute/w": {"to be rich"},                 # a bare repetition of the first sense
    "fai/nw": {"to shew", "to make", "clear", "to inform of", "as contraband", "shining"},  # pieces of examples; "to make it clear", "to inform of as contraband" cut, whole in MARKUP_LOST; examples' participles
    # GEN 31
    "do/ca": {"one expects", "expect"},          # pieces of an example
    "a)lla/ssw": {"to take", "for", "in turn", "in turns"},  # pieces of "to take one thing for another" and of examples
    "ge/nesis": {"by descent"},                  # a piece of an example
    "klhronomi/a": {"possession of . ."},        # a citation's debris
    "pipra/skw": {"I am bought and sold!", "betrayed, ruined, undone"},  # pieces of examples
    "plou=tos": {"Plutus"},                      # the god, not the word
    "a)pa/gw": {"to take away for", "with oneself", "brought to a point, tapering off"},  # pieces of the middle and passive
    "u(pa/rxw": {"to make a beginning of", "to begin", "to be begun", "a beginning"},  # pieces of sense I
    "kei/rw": {"to cut off one's", "have", "cut off"},  # pieces of the middle
    "ei)/dwlon": {"phantoms"},                   # a piece of an example
    "diabai/nw": {"stand with the legs apart", "planting himself firmly"},  # pieces of sense I
    "o(rma/w": {"push on, spur on, cheer on", "inspired", "was inflicted"},  # pieces of sense I
    "eu)frosu/nh": {"festivities"},              # a piece of an example
    "mousiko/s": {"of", "music"},                # pieces of "of or for music, musical"
    "tu/mpanon": {"tympana"},                    # the Latin plural, in a citation
    "a)cio/w": {"to think", "deem worthy of", "reward", "punishment"},  # pieces of sense I
    "pra/ssw": {"to accomplish", "to avail", "to cause"},  # a bare repetition, and two examples
    "i)sxu/w": {"to be strong", "influence"},    # a bare repetition, and a piece of sense 2
    "e)piqumi/a": {"by passion", "desire of", "for"},  # pieces of examples
    "e)piqume/w": {"to desire to", "eagerness"},  # pieces of examples
    "e)reuna/w": {"he seeks after", "finds", "to search"},  # pieces of examples
    "e)mba/llw": {"to throw", "to put", "into", "to give"},  # pieces of examples
    "e)pikaqi/zw": {"had", "set"},               # pieces of an example
    "o)rgi/zw": {"with"},                        # a piece of "to grow angry with"
    "kau=ma": {"in the sun-heat"},               # a piece of an example
    "keno/s": {"empty"},                         # a bare repetition of the first sense
    "ma/rtus": {"witnesses"},                    # the plural of the one sense
    "sulle/gw": {"to compile a list of", "to collect"},  # a piece of an example, and a repetition
    "marture/w": {"in favour of", "bears witness to", "testify"},  # pieces of examples
    "marturi/a": {"evidence"},                   # a bare repetition
    "e)fora/w": {"was in view"},                 # a piece of an example
    "kaki/a": {"(excellence)", "defects"},       # the word it is opposed to, and a plural
    "qu/w1": {"offering", "burning", "to slaughter for sacrifice)"},  # pieces of the parenthesis the entry opens with
    "qusi/a": {"mode of offering", "sacrifices"},  # a piece of sense I, and a repetition
    # GEN 32
    "paremba/llw": {"to put", "in line with"},   # pieces of "to put in line with"
    "xroni/zw": {"to delay", "long"},            # pieces of examples
    "a)pore/w": {"resource", "to be at a loss", "to be at a loss about"},  # a piece of sense I, and two repetitions
    "e)kko/ptw": {"he had", "knocked out", "to cut", "out of"},  # pieces of examples
    "sw/|zw": {"to keep", "preserve for oneself"},  # a repetition, and a piece of the middle
    "e)caire/w": {"to take out", "to discharge their"},  # a repetition, and a piece of an example
    "pw=los": {"colt", "filly"},                 # pieces of "a foal, young horse, colt, filly"
    "proporeu/omai": {"forward"},                # a piece of "to go before or forward"
    "poi/mnh": {"of sheep"},                     # a piece of "properly of sheep"
    "prosde/xomai": {"to admit"},                # a bare repetition
    "paraporeu/omai": {"alongside"},             # a piece of "to go beside or alongside"
    "e(/ndeka": {"the Eleven, the Police-commissioners"},  # the Athenian magistrates
    "dia/basis": {"a means"},                    # a piece of "a means or place of crossing"
    "palai/w": {"beaten"},                       # the passive participle of an example
    "pla/tos": {"in breadth"},                   # a piece of an example
    "a)nate/llw": {"mounting up"},               # a piece of the passive
    # GEN 33
    "e)/sxatos": {"the furthest", "extremities"},  # a repetition, and a piece of an example
    "proe/rxomai": {"far advanced", "to go on"},  # a piece of an example, and a repetition
    "prostre/xw": {"towards, come to"},          # a piece of "to run to or towards"
    "e)lee/w": {"mercy shewn one"},               # a piece of the passive
    "bia/zw": {"overpowered", "suffer violence", "forcibly made slaves", "to do", "violence",
               "[to be favourable]"},  # pieces of the passive; "to do them violence" cut, whole in MARKUP_LOST; an example's
    "loxeu/w": {"brought to birth"},             # a piece of an example
    "sxolh/": {"leisure", "quiet", "time", "a fit time"},  # pieces of examples
    "e)pikale/w": {"to invoke", "to watch over"},  # a repetition, and a piece of an example
    # GEN 34
    "e)gxw/rios": {"in"},                        # the first half of "in or of the country"
    "miai/nw": {"violaverit ostro si quis ebur)", "to incur such defilement"},  # Virgil, and the passive
    "luphro/s": {"painfully, so as to cause pain", "painful"},  # the adverb, and "it is painful"
    "proaire/w": {"sooner than", "to prefer"},   # half of "before or sooner than", and a repetition
    "platu/s": {"broad", "large", "widespread"},  # pieces of "broad herds, i. e. large or widespread"
    "o(moio/w": {"to make", "suitable"},          # pieces of "to make their feelings suitable"
    "po/nos": {"the toil", "battle"},             # pieces of the Homeric examples
    "a)sfalh/s": {"safe", "safety", "it is safe", "a convincing"},  # pieces of examples
    "a)riqmo/s": {"in", "sum", "among", "account", "a mere set", "a mere lot", "a muster"},  # pieces of examples
    "diarpa/zw": {"to seize", "plunder"},         # the two halves of "to seize as plunder"
    "ei)rhniko/s": {"of", "peaceably"},           # half of "of or for peace", and the adverb
    "o)ligosto/s": {"the smallest space"},        # from "the smallest space of Time"
    "tetra/pous": {"four feet"},                  # from "four feet in length"
    # GEN 35
    "ai)/rw": {"to step, walk", "to hoist", "to mount up, ascend", "to get", "under sail",
               "to get under way, start, set out", "to pluck up", "to raise by words",
               "to take up for oneself: to carry off, win, gain", "to receive, get", "wilt incur",
               "to take upon oneself, undergo, carry, bear", "to undertake, begin", "to raise up",
               "to raise, lift up"},           # pieces of examples, the passive, and the middle
    "kaqari/zw": {"to be", "become clean", "to be purged away"},  # the passive
    "spe/ndw": {"to pour a libation", "to make a drink-offering with",
                "I am offered (as a drink-offering", "to pour libations one with another",
                "to make a treaty, make peace", "to make peace with", "to give", "pledges",
                "having concluded", "peace", "to make up", "to make a truce",
                "to be concluded"},            # pieces of examples, and the middle
    "spondh/": {"solemn drink-offerings", "the truce", "the truce with", "a truce",
                "the solemn truce", "armistice"},  # pieces of examples
    "qarse/w": {"take courage! cheer up", "with good courage", "confidence", "take heart for",
                "to venture", "to have confidence in", "to believe confidently that",
                "to make bold", "venture"},    # pieces of examples
    "mai=a": {"a", "mother"},                   # the two halves of "also a true mother"
    "o)du/nh": {"grief for"},                   # from "grief for him"
    "o)sfu/s": {"one's loins", "of the loins"},  # pieces of "to gird up one's loins"
    "li/qinos": {"stony"},                      # from "stony death"
    "e)pe/keina": {"beyond", "on the far side"},  # a repetition, and a piece of an example
    # Opening the last of the words that print as plain text.
    # Middle Liddell writes "on the upper side or part" and "of three stories or
    # floors" as one sense each; splitting on the "or" makes a second sense out of
    # half a phrase. τριώροφος has no other, so it is a one-sense word and stays
    # plain text, which is what GEN 6:16's own note already says.
    "triw/rofos": {"floors"},
    # ὑπεναντίος: "opposite or contrary to" is one gloss of the dative construction,
    # split the same way. τὸ and τὰ ὑπεναντίον are the neuter substantive and -ίως
    # is the adverb, so neither is a sense οἱ ὑπεναντίοι can wear, as κατὰ μῆνα was
    # not a sense of μήν.
    "u(penanti/os": {"opposite", "the contrary", "on the contrary",
                     "in a manner contrary to"},
    # Entries reached by the Middle-Liddell-first rule. ἀρνός opens with its etymology,
    # "akin to ἔριον, wool"; πρῶτος's "end" is half of "at the front or end of the pole",
    # and cannot translate the adjective, while "among the first" and "at the front" are
    # the idioms ἐν πρώτοις and ἐν πρώτῳ,
    # which a merged unit already opens with ἐν's own English, as κατὰ μῆνα was not μήν.
    "a)rno/s": {"wool"},
    "prw=tos": {"end", "among the first", "at the front"},  # "at the front" is ἐν πρώτῳ
    "ou)=los": {"incessant"},                  # from "screaming incessant", in the example
    # πάλιν's "notion of contradiction" sliced by the tagging: "gain" is half of "gain say",
    # "against)" keeps the parenthesis it came out of, "contradiction" is the label; "back,
    # restore" glosses πάλιν δοῦναι and "unsay" μῦθον πάλιν λάζεσθαι, the phrases rather
    # than the adverb; "back from" is its genitive construction; the bare "back" repeats.
    "pa/lin": {"contradiction", "gain", "against)", "unsay", "back, restore", "back from",
               "back"},
    # "so called from its broad leaves" is why the tree has the name, not a sense.
    "pla/tanos": {"broad leaves."},
    # νῦν's entry turns aside — "besides the sense of Time, the enclit. νυν, νυ denotes
    # immediate sequence" — and everything after that belongs to the enclitic νυν, a
    # different word, as κατὰ μῆνα was not a sense of μήν.
    "nu=n": {"upon", "then, thereupon, thereafter", "then, therefore", "then!", "then?"},
    # The particles. Middle Liddell writes most of a particle's entry as prose about how
    # it works, and the scraper takes a <tr> wherever it finds one, so the labels of a
    # construction — "fear", "apprehension", "a question", "a wish" — and the sentences
    # that illustrate it come through beside the translations. Only the translations are
    # senses.
    # What the recovered translation displaces: the word the dictionary was describing
    # rather than translating, or an example's rendering that had stood in its place.
    "w)=mos": {"ulna", "the lower)", "it"},     # the parenthesis about ὠλένη, the forearm
    "dh/": {"exactness"},                       # "used to give greater exactness" is the description
    "tre/mw": {"to tremble"},                   # now inside "to tremble, quake, quiver"
    "ga/r": {"to introduce the reason", "to introduce the reason for",
             "the statement of which", "gives the reason may be omitted",
             "a question", "a wish", "O",       # the labels of the constructions
             "quid enim",                       # Latin
             "why"},                            # the second half of "why, what"
    "te": {"et."},                              # Latin
    # GEN 37
    "e)nu/pnion": {"in sleep"},                 # the adverbial use, "a vision in sleep came"
    "katafe/rw": {"will bring", "down",         # "grief will bring me down to the grave"
                  "I bring down"},              # "I bring down my foot"
    "e)kdu/w": {"they stripped", "of"},         # scraps of examples
    "peristre/fw": {"round", "behind"},         # halves of "to wheel it round", "to tie his hands behind"
    "o)rqo/w": {"is rightly sent"},             # a scrap of an example
    "selh/nh": {"the full-", "moon",            # "the full-moon", split across two tags
                "lunam deducere"},              # Latin
    "diarrh/gnumi": {'"split you!"'},           # an oath in comedy
    "a(rpa/zw": {"by"},                         # a scrap
    "e)nteu=qen": {"illinc",                    # Latin
                   "what remains"},             # τἀντεῦθεν, with the article
    "plana/w": {"having missed", "to do", "irregularly", "at random",  # pieces of examples
                "that have visited"},
    "qhri/on": {"beast!", "bete"},              # a term of reproach, and its French
    "kata/gw": {"into the nether world"},       # where Odysseus is led down, not a sense
    "a)nabiba/zw": {"up", "to have",            # halves of "to draw a ship up", "to have them
                    "put on board ship"},       # put on board ship"
    "xrh/simos": {"that will not pass",         # of coin, a scrap
                  "with advantage"},            # an adverbial phrase
    # GEN 38
    "periaire/w": {"taking off", "taking [the cover] off", "opening",   # glosses of examples
                   "to take off one's", "when", "has been taken away"},
    "pa/rodos": {"as", "passed by"},            # pieces of examples
    "katakalu/ptw": {"having covered his"},     # "having covered his head", an example
    "e)a/w": {"we will have done with"},        # an example
    "e)ntau=qa": {"here-", "in that department of"},  # scraps
    "katakai/w": {"alive", "had burnt down, burnt out"},  # "burn alive"; a pluperfect example
    "de/w": {"his", "he had", "bound"},         # an example; "to let, stop from" is a sense
    # GEN 39.
    # πῶς with another particle, or with verbs of selling: each of these translates the
    # phrase — πῶς ἄν, πῶς ἄρα, πῶς γάρ, πῶς δή, καὶ πῶς, πῶς οὐ, πῶς ποτε — not πῶς.
    "pw=s": {"how? at what price?", "how possibly . . ?", "O how", "would that",
             "how then . . ?", "[that cannot be], for how can . . ?", "how in the world?",
             "how can it be?", "how not so . . ; ?", "surely it is so . .", "how ever . . ?"},
    "ei)/sw": {"into the house", "even to the inside"},  # glosses of two Homeric examples
    "katalei/pw": {"being", "left behind",      # "being part of the army left behind"
                   "will leave", "yet remains to be fought"},  # examples
    "toiou=tos": {"such a wretch", "such a man",  # examples
                  "such a reason", "what goes before"},  # an example; a description
    "e)pispa/w": {"by", "having dragged"},       # "having dragged her by the hair"
    "eu)nou=xos": {"chamberlains"},             # what eunuchs were employed as, not the word
    # GEN 40.
    "fulakh/": {"to watch", "watch", "watches",  # glosses of examples: "keep watch and ward",
                "guarded", "occupied", "to preserve",  # "nothing visible to watch", "set watches"
                "to keep guard, be on the watch", "on"},
    "qa/llw": {"grew", "fresh", "copious", "rich", "sumptuous"},  # the examples' τεθαλυῖα
    "stafulh/": {"by the level"},               # "matched in height by the level", an example
    "kloph/": {"by stealth", "fraud"},          # κλοπῇ, "by stealth or fraud": the dative's idiom
    "krema/nnumi": {"will bring", "hang them up", "up by", "to hang up one's",  # examples
                    "thou wert hanging", "hangs over", "depending"},
    "oi)noxoe/w": {"she was pouring out", "for wine"},  # "she was pouring out nectar for wine"
    # GEN 41.
    "cure/w": {"it shaves",                     # ξυρεῖ ἐν χρῷ, a proverb: "it shaves close"
               "have their", "shaved"},          # "they have their whole body shaved"
    "lepto/s": {"a thin line",                  # ἐπὶ λεπτόν, an idiom
                "sheep and goats", "light breezes"},  # what two examples name
    "sofo/s": {"than all craft"},               # "better than all craft", an example
    "a)namimnh/skw": {"of"},                    # "to remind one of a thing"
    "sumbai/nw": {"has", "come in my way, has had", "to do with me"},  # one example's glosses
    "swth/rios": {"to preserve", "deliverance to"},  # an example; half of "bringing safety or
                                                     # deliverance to one"
    "oi(=os": {"reason"},                       # "introduces the reason", a description
    "a)nali/skw": {"upon"},                     # "to spend upon a thing"
    "kloio/s": {"a"},                           # "a sort of pillory"
    "pwle/w": {"at a high"},                    # "at a high price", an example
    # GEN 42.
    "pri/amai": {"to have", "sold to one, to buy, purchase"},  # one translation in two; MARKUP_LOST
    "badi/zw": {"were getting"},                # "were getting on", an example's verb
    "lu/w": {"undid her", "to unbind one's", "to unyoke one's", "to get", "loosed", "on payment of",
             "rotted", "made", "slack", "loose", "killed", "weak", "ties are broken", "in full",
             "it boots not"},                   # glosses of examples' forms and pieces of senses
    "e)pe/rxomai": {"it happened", "over", "on"},  # an impersonal example; pieces of "to go over"
    "diamarturi/a": {"evidence given to prevent"},  # the half the <tr> holds; MARKUP_LOST has it whole
    "e)kde/xomai": {"succeeded"},                # an example's verb
    "staqmo/s": {"in weight", "in", "by weight", "weights"},  # the dative's idioms and an example
    "ku/ptw": {"with the head down", "at full speed", "stooping", "greedily", "bent"},  # examples
    "sustre/fw": {"together", "in a body", "they were formed in a mass", "sharply", "briefly, curtly",
                  "pithy"},                     # pieces of senses, examples, and the participle's adverb
    "a)pe/xw": {"part", "to hold one's", "off", "were far from", "from", "it sufficeth, it is enough",
               "to be as far"},  # "to be as far as possible from", an example's piece
    "makra/n": {"far", "to a greater distance", "as far as possible"},  # a repetition, and the comparative's and superlative's
    "parame/nw": {"trusty"},                     # the slave's name Παρμένων, "trusty"; not a sense of the verb
    "loipo/s": {"quod superest"},                # Latin
    "e)ktre/fw": {"for oneself"},                # a piece of the middle's "to rear for oneself"
    "gemi/zw": {"charging", "with", "freighted"},  # pieces of examples
    "zeu/gnumi": {"to put to one's", "having", "fastened", "in the yoke of", "well-joined", "by bridges", "with ropes"},  # pieces of examples and of the middle's
    # τέλος: repetitions inside examples ("its issue", "the result", "the end" before "the end,
    # death", "full age", "a tax", "the magistrates"), pieces ("hood" of "man hood", "it"), the
    # phrases τέλος ἔχειν and λαβεῖν rendered whole, and Cicero's Latin
    "te/los": {"issue", "a finish", "accomplished", "the end, to be finished", "ready", "the result",
               "completed", "the end", "finis bonorum", "full age", "hood", "to be grown up", "duties",
               "squadrons", "troops", "due", "a tax", "it", "the magistrates",
               "as the consummation of life"},
    "e)calla/ssw": {"sees", "change take place", "other", "shall I take?"},  # pieces of examples
    "ble/pw": {"see too clearly", "face", "looked", "looking like", "thoughtful", "looking towards",
               "actually existing"},           # pieces of examples, and the participle's
    "xai/rw": {"I rejoice at", "thou wilt", "shalt not rejoice", "thou shalt", "accept the greeting",
               "taking leave", "parting", "have done with", "away with", "let", "be put aside", "may'st",
               "fare well", "with a benison", "welcome", "S. D."},  # pieces of examples and constructions
    "nomh/": {"to spread"},                      # νομὴν ἔχειν, of a sore, rendered whole
    "e)cai/retos": {"that can be taken out, removable"},  # ἐξαιρετός's, the entry's other word
    "klh=ros": {"the laity.", "by lot"},          # the contrast the clergy is drawn against; an example's phrase
    "r(u/omai": {"from"},                         # a piece of "deliver us from the pollution"
    # GEN 49: the renderings of examples and the pieces of constructions, each named by its entry.
    "a)qroi/zw": {"having rallied", "amounted collectively", "has gathered strength, arisen"},  # examples' renderings
    "e)cubri/zw": {"to come to", "pitch of insolence", "to commit", "violence"},  # pieces of examples
    "e)kze/w": {"boiled over"},                   # an example's rendering, "boiled over with worms"
    "koi/th": {"bed-", "to be pregnant"},         # "bed-time"; κοίτην ἔχειν rendered whole
    "strwmnh/": {"prepared;"},                    # the end of "a bed spread or prepared"
    "boulh/": {"counsels", "the Council of", "of the Council, a member of it"},  # a plural; pieces
    "su/stasis": {"knots"},                       # an example's plural, κατὰ συστάσεις
    "h(=par": {"pregnant"},                       # ὑφ' ἥπατος φέρειν, of pregnant women
    "a)po/keimai": {"store", "in reserve"},       # pieces of "great store of laughter in reserve"
    "plu/nw": {"to bathe", "to wash the hands", "feet)", '"to give', 'a dressing,"'},  # λούομαι's and νίζω's; slang in pieces
    "peribolh/": {"compass", "a circuit", "long and short"},  # examples' repeats; a phrase's
    "ploi=on": {"craft", "vessels", "ships"},     # examples' plurals
    "pi/wn": {"rich", "pingues segetes"},         # a piece of "rich fat"; Latin
    "pone/w": {"were busied", "was busy", "do with pains", "care", "to labour", "do", "labour"},  # examples; pieces
    "e)gka/qhmai": {"on"},                        # the end of "to sit in or on"
    "da/knw": {"prick"},                          # the end of "to sting or prick"
    "perime/nw": {"they do", "wait for"},         # pieces of an example
    "to/ceuma": {"an arrow", "bow-shot"},         # examples' repeats
    "kra/tos": {"with all one's might", "strength, by open force, by storm", "Strength, Might", "the meed"},  # κατὰ κράτος whole; the personified; an example's
    "masto/s": {"the breast", "mamelon)"},        # an example's; French
    "koru/fh": {"top of the head", "the highest point", "best of all", "excellence of"},  # examples; pieces
    "lu/kos": {"to be struck dumb", "Moerim lupi videre priores);"},  # a proverb; Virgil
    "diadi/dwmi": {"around"},                     # the end of "to cast one's eyes around"
    "trofh/": {"bread", "a way", "while in the nursery"},  # an example's; a piece; a phrase
    "e)pita/ssw": {"to", "they had", "placed next", "set as guards over"},  # pieces of examples
    "h(ge/omai": {"to be", "leader in", "commander of", "fit, deem", "necessary"},  # pieces of "to be leader in", "to think fit, deem necessary"
    "e(/lic": {"flashes of forked"},              # a piece of "flashes of forked lightning"
    # GEN 50
    "sunanabai/nw": {"together", "with"},         # the half of "to go up with or together", and τινί "with" one
    "patriko/s": {"of"},                          # half of "of or belonging to one's father"
    "mnhsikake/w": {"to bear", "malice, pass an act of amnesty", "a grudge for", "to remind", "of the ills"},  # pieces of examples
    "kommo/s": {"plango), a beating of the breast in lamentation", "lamentation"},  # the <tr> opened inside the Latin; MARKUP_LOST has it whole. An example's
    "pe/ran": {"done on the opposite side", "just over the border", "border-"},  # pieces of τὰ πέραν and ἡ πέραν γῆ
    "tafh/": {"the urn"},                        # one passage's, Sophocles' urn of Orestes
    # EXO 1
    "tosou=tos": {"so", "as large",               # pieces of examples, τοσοῦτος μέγαθος "so large"
                  "so small a distance", "so far", "so far, so far", "in the meantime",
                  "so far, so long"},             # the phrases with prepositions
    # EXO 2
    "a)stei=os": {"pretty"},                     # the irony of "a pretty piece of luck"
    "manqa/nw": {"by inquiry", "learners, pupils", "know that", "perfectly!", "having learnt",
                 "what new reason? wherefore"},  # a qualifier, the participle as a noun, idioms of examples
    "dikasth/s": {"judices", "presiding judge"},  # the Latin, and ὁ κριτής's gloss
    "e)mfanh/s": {"bodily", "visible", "actual", "in public", "light",  # pieces of examples
                  "visibly, openly", "openly", "not secretly", "treacherously", "really"},  # the adverb's
    "boh/": {"at the battle-cry", "of war", "as far as sound went, only in appearance"},  # pieces of examples
    "tu/ptw": {"to tread", "beating, lashing", "smote", "I get"},  # pieces of examples
    "lou/w": {"body", "hands and feet", "clothes)", "bathe", "let him bathe", "washed", "fresh from", "bath",
              "fresh-bathed, after bathing", "ire lavatum)", "to wash one's"},  # νίζω's and πλύνω's, examples, the Latin
    # EXO 3
    "kai/w": {"they lighted them", "penetrabile frigus adurit", "with fire", "cautery"},  # examples, Virgil, a piece
    "ka/kwsis": {"for ill-usage"},              # a piece of δίκη κακώσεως
    "r(e/w": {"runs with", "runs", "rained", "flow", "salso multoque fluenti)", "let", "run"},  # examples' pieces, Virgil
    "qli/bw": {"he will rub his", "a small, close", "narrow"},  # pieces of examples
    "ai)te/w": {"for", "to"},                    # pieces of "to ask for", "to ask a thing of"
    "gei/twn": {"vicus)", "from", "in the neighbourhood"},  # the Latin, pieces of examples
    "skuleu/w": {"having stript", "off"},       # an example's
    "eu)labe/omai": {"without reserve"},         # μὴ εὐλαβηθῆναι, an example's
    # EXO 4
    "kwfo/s": {"the blunt, dull", "dumb", "the dumb, senseless", "dull", "ringing", "noisy"},  # examples' pieces; "dumb, mute" stays
    "tuflo/s": {"back"},                         # τὰ τυφλὰ τοῦ σώματος, one's back, an example's
    "e)pilamba/nw": {"from", "traverse", "corripere campum", "to hold oneself", "by, lay hold of, catch"},  # pieces, Virgil; the cut sense whole in MARKUP_LOST
    "yh=fos": {"by arithmetic, to cipher", "to reckon exactly", "accurately", "one's vote", "by vote", "the vote",
               "question", "a decree", "judgment", "calculus Minervae", "acquittal", "lot;", "trials, the latter in",
               "elections."},                   # examples' translations, a proverb, the note on ballot and lot
    "e)pista/ths": {"the right-", "left-hand man", "the front-rank man)", "a", "master", "which stood over"},  # παραστάτης's and προστάτης's glosses; "a training-master" cut in two, whole in MARKUP_LOST; a piece
    "be/ltistos": {"my good friend"},             # ὦ βέλτιστε, the vocative's mode of address
    # EXO 14
    "metastre/fw": {"are changed", "contrariwise"},  # examples' translations: my fortunes are changed; the participle as an adverb
    "mnh=ma": {"a memorial"},                   # a repeat, of one dedicated to a god
    "pari/hmi": {"at the side, let fall", "hung down", "to slack away", "letting go one's hold of", "left it",
                 "have admitted", "their", "obtain", "consent", "I ask", "quarter", "we ask pardon"},  # "to let drop … at the side" cut, whole in MARKUP_LOST; examples' pieces and translations
    "krei/sswn": {"betters", "advantages", "a better right", "too great", "too bad for", "worse", "superior to"},  # nouns of the plural, examples' translations
    "poleme/w": {"with", "hostilities passed"},  # a piece; a passive example's
    "siga/w": {"still, to keep silence", "hush! be still!", "hushed", "secret", "was kept"},  # cut from "to be", whole in MARKUP_LOST; the imperative's; examples'
    "summi/gnumi": {"with", "having combined", "has not", "as an ingredient in his nature", "happened together",
                    "to make", "acquainted with"},  # pieces and examples' translations; "to make … acquainted with" whole in MARKUP_LOST
    "u(pa/gw": {"bring", "under", "to bring", "before the judgment-seat", "beneath", "so as to lead", "on",
                "on with you !"},  # examples' pieces; "to bring … before the judgment-seat" whole in MARKUP_LOST; what ὑπό refers to
    "bi/aios": {"violent", "of violence", "by force, perforce"},  # examples' translations; the adverb βιαίως
    "tei=xos": {"coats", "moenia sibi circumdare", "to breach", "paries, city-walls", "house-wall;"},  # examples' translations, the Latin, τεῖχος set against τοῖχος
    "e(wqino/s": {"early in the morning"},      # τὸ ἑωθινόν, the neuter as an adverb
    "suntara/ssw": {"confounded with"},         # a passive example's
    "sunde/w": {"drawn up", "gird up thy"},     # a passive and a middle example's
    "a)/cwn": {"the wooden tablets of", "laws, made to turn upon an axis"},  # οἱ ἄξονες, Solon's laws
    # EXO 15
    "e)/ndocos": {"held in esteem", "honour, of high repute"},  # "held in esteem or honour …", cut, whole in MARKUP_LOST
    "doca/zw": {"can I suppose", "is supposed", "to entertain"},  # examples' translations; δόξαν δοξάζειν, the phrase's
    "katadu/w": {"set", "having popped down", "we will go down", "to cut", "down to the water's edge, disable"},  # examples'; "to cut it … disable", cut, whole in MARKUP_LOST
    "ku=ma": {"pregnant"},                     # "as if pregnant", the gloss's own gloss
    "th/kw": {"to cause to waste", "pine away", "is consumed", "dead", "languishing"},  # "to cause to waste or pine away", cut, whole in MARKUP_LOST; examples'
    "me/geqos": {"greatness"},                 # "greatness, i. e. might, power": the i. e. explains it
    "e(toi=mos": {"ready", "in hand", "off-hand, forthwith", "what comes to hand", "ready to", "readiness", "readily"},  # examples', phrases', the neuter's, the adverb's
    "katerga/zomai": {"achieved", "is subdued, brought under cultivation", "be prevailed upon", "to make"},  # passive examples'; κ. μέλι, an example's
    "xoro/s": {"round", "a single actor"},     # pieces of the note on the Attic chorus
    "e)ca/rxw": {"to begin", "address"},       # an example's: to begin a hymn, address it
    "a)koh/": {"tidings"},                     # an example's repeat
    "foi=nic": {"bay", "red", "dark reds", "brighter shades"},  # examples'; the note on colours
    "no/sos": {"madness"},                     # θεία ν., the phrase's
    "sku=lon": {"arms taken as spoil"},        # an example's
    "dii/sthmi": {"to set", "at variance with", "to divide", "into fractions", "made way, opened", "chasms",
                  "to stand at certain distances", "intervals"},  # cut, whole in MARKUP_LOST; examples'
    "a)ei/dw": {"to sing in one's praise"},    # ἀείδειν ἀμφί τινος, the phrase's
    "w)di/s": {"birth"},                       # an example's, at a single birth
    # EXO 16
    "pa/gos": {"that which is fixed", "firmly set"},  # cut, whole in MARKUP_LOST
    "metre/w": {"by the eye", "to get", "measure"},  # examples' pieces
    "pleona/zw": {"to go beyond bounds, take", "claim too much"},  # cut, whole in MARKUP_LOST
    "pikrai/nw": {"to make sharp", "bitter"},   # cut, whole in MARKUP_LOST
    "a)poti/qhmi": {"to put aside", "disregard"},  # an example's, the law put aside
    "o)rtugomh/tra": {"the Ortygian mother"},  # Latona, the comic poet's joke
    "a)poqh/kh": {"store"},                    # an example's
    "*sa/bbaton": {"of the week"},             # μία τῶν σαββάτων, the phrase's
    "oi)ke/w": {"those who have been settled", "those who dwell", "to live", "with habits", "would", "governed"},  # examples' translations
    # EXO 17
    "di/ya": {"for"},                          # a piece of an example, thirst for drink
    "loidore/w": {"they use", "reproaches"},   # an example's
    "pe/tra": {"a rock, a ledge", "shelf of rock", "a rock", "a rocky peak", "ridge", "fixed rock", "a stone",
               "masses of live rock", "rock", "a cave in the rock"},  # cut, whole in MARKUP_LOST; the note on πέτρος; examples'
    "e)pile/gw": {"he chose him", "chosen men", "nihil curare"},  # examples'; the Latin
    "kaqi/hmi": {"we let down, lowered", "let down", "bring", "to the rest", "were carried down to the water", "has entered"},  # examples' pieces and translations
    "sthri/zw": {"he set", "fast", "rising up", "to be firmly set", "fixed, to stand fast", "steady", "to", "a firm footing",
                 "is lifted up", "thou art tarrying, art settled"},  # examples'; the passive's, cut, whole in MARKUP_LOST
    "katagra/fw": {"to fill", "with writing"}, # cut, whole in MARKUP_LOST
    # EXO 18
    "a)/fesis": {"a letting go", "having made", "one"},  # a repeat; an example's
    "a)spa/zomai": {"salute"},                 # an example's
    "mo/xqos": {"for", "hardship, distress;", "work", "poor man's lot)."},  # a piece; the note on μόχθος and πόνος
    "diakri/nw": {"making", "distinction", "distinction was made", "to get", "decided"},  # examples' pieces
    "sumbouleu/w": {"to advise", "the advice given", "an adviser", "ask", "advice"},  # a repeat; the participles'; pieces
    "shmai/nw": {"to give a sign", "signal to do", "without any order from", "to make signal", "signal is given",
                 "when signal was given", "signal was given", "tell", "to stamp with a sign", "mark, to seal", "to be", "sealed up"},  # cut, whole in MARKUP_LOST; examples'
    "u(perhfani/a": {"contempt towards", "for"},  # cut, whole in MARKUP_LOST
    "xili/arxos": {"tribunus militum", "the tribuni militares consulari potestate"},  # the Latin it translates
    "braxu/s": {"briefly", "scantily, seldom", "low", "little by little", "in few words", "briefly, in few words", "lightly"},  # phrases' and the adverb's
    "koufi/zw": {"to make a light", "of", "of their cargo", "from"},  # examples' pieces
    "e)lafro/s": {"lightly, buoyantly", "light, easy", "light", "active", "light troops"},  # the adverb's; examples'
    # EXO 19
    "pte/ruc": {"wings", "the wings", "anything that covers", "protects"},  # the plural of the first sense, and a repeat; cut, whole in MARKUP_LOST
    "h)xe/w": {"to let", "sound", "is made"},  # cut, whole in MARKUP_LOST; examples'
    "ptoe/w": {"he gapes like one distraught", "distraction"},  # an example's; the participle's as a noun
    "kapno/s": {"of smoke", "trifles"},       # a proverb's; an example's
    "qigga/nw": {"reach"},                    # an example's
    "a)palla/ssw": {"from"},                  # a piece of the construction
    "prosa/gw": {"to draw", "upon oneself", "will induce", "imports"},  # cut, whole in MARKUP_LOST; an example's; the participle's as a noun
    # EXO 20
    "a)/nw": {"the living", "the dead", "the gods above", "up and down, to and fro", "upside down, topsy-turvy",
              "higher", "further", "above, beyond", "highest", "inland)"},  # phrases' with the article and with κάτω; the comparative's and superlative's; "i. e. inland", what "up the country" means
    "ka/tw": {"lower, further, downwards", "lower than, below", "at the lowest part"},  # the comparative's and superlative's
    "zhlwth/s": {"qana, to glow, be zealous)"},  # the Hebrew word the NT's use translates
    "ma/taios": {"seriousness, gravity", "idly, without ground"},  # a phrase's, τὸ μὴ μάταιον; the adverb's
    "ou)/te": {"both not", "and"},            # the construction with τε, an example's
    "yeudh/s": {"lying", "a liar", "lying men", "lies);", "in falsehood", "falsehoods, lies", "falsely"},  # a repeat; the noun's; examples'; the neuter plural's; the adverb's
    "tima/w": {"penalty", "against", "condemned", "for", "he estimates", "at"},  # examples' pieces
    "e)gxeiri/dion": {"in the hand"},         # the adjective's; the noun is "as Subst." inside ἐγχειρίδιος
    # EXO 21
    "dou/lh": {"a born bondman", "slave", "one made a slave", "a bondman, slave", "slave to",
               "slavish, servile, subject"},  # the masculine's and the adjective's: δούλη is the feminine inside δοῦλος
    "e)leu/qeros": {"of freedom", "freedom", "to freedom"},  # examples', and the neuter's as a noun
    "suneise/rxomai": {"to enter along with", "together"},  # cut, whole in MARKUP_LOST
    "krith/rion": {"a means for judging", "trying, a criterion, standard, test"},  # cut, whole in MARKUP_LOST
    "trupa/w": {"having", "pierced for earrings", "which had a hole in it", "to force", "through"},  # the passive's examples; cut, whole in MARKUP_LOST
    "a)qete/w": {"refuse", "request"},          # cut, whole in MARKUP_LOST
    "o(mili/a": {"communion", "intercourse with", "intercourse", "mates"},  # repeats of the first sense; a piece of "ship-mates"
    "a)postere/w": {"from"},                   # a piece of the construction
    "pugmh/": {"diligently;", "often, with;", "the distance from the elbow to the knuckles, = 18"},  # the NT's interpretation by other words, πύκα and πυκνά; the measure's <tr> run on into "= 18 δάκτυλοι", whole in MARKUP_LOST
    "katakli/nw": {"having made", "recline"},  # an example's participle
    "di/kh": {"custom", "judgment", "trial", "make amends", "punishment", "vengeance", "penalty", "satisfaction",
              "to have their causes tried"},  # repeats; phrases' (δίκην διδόναι, λαμβάνειν, ὀφλεῖν, αἰτεῖν)
    "zhmio/w": {"will suffer", "losses", "to be fined", "amerced in"},  # cut, whole in MARKUP_LOST
    "e)pizh/mios": {"penalties"},              # the neuter plural's as a noun
    "lu/tron": {"as ransom", "ransom", "for"},  # examples' and a piece
    "gnwri/zw": {"to make known"},             # a repeat
    "a)ci/wma": {"honour"},                    # an example's, γάμων ἀξ., a repeat of the first sense
    # EXO 22
    "to/kos": {"compound interest"},          # a phrase's, τόκοι τόκων
    "a)porri/ptw": {"outcasts", "to shoot forth bold, keen"},  # the participle's as a noun; cut from its "words", whole in MARKUP_LOST
    "a)naneu/w": {"shaking the head)"},       # the gloss of a gesture: "which we express by shaking the head"
    "xh/ra": {"widow", "widower", "widow)", "widowed, bereaved", "torn from"},  # an example's, a repeat; χῆρος's, the masculine and the adjective formed from χήρα, and its example's piece
    "katabo/skw": {"to feed flocks upon", "in", "the shepherd"},  # cut, whole in MARKUP_LOST; an example's participle
    "e)gkale/w": {"to bring a charge", "against one"},  # a repeat of the sense before, cut by its object
    "a(li/skomai": {"were seized and taken", "to be caught", "detected"},  # an example's; cut, whole in MARKUP_LOST
    "de/on": {"things needful", "proper, advantages", "duties", "in good time", "for a needful purpose", "secret service"},  # τὰ δέοντα cut, whole in MARKUP_LOST; phrases'
    "o)fei/lw": {"debemur morti)", "it is", "destiny", "(ought", "owe)", "O that thou hadst", "O that I had",
                 "would thou hadst never", "would"},  # Horace; examples' translations; the note on "ought"
    "e)panastre/fw": {"to turn back upon"},    # "to turn back upon one", cut, whole in MARKUP_LOST
    "r(h/gnumi": {"to break, break asunder", "in pieces, rend, shiver, shatter", "force one's", "breaking into speech",
                  "rumpere vocem", "having let loose"},  # "to break … or in pieces", cut, whole in MARKUP_LOST; a piece, examples', Virgil
    # EXO 37
    "leitourgi/a": {"liturgies", "liturgy."},  # the ordinary liturgies' list; "hence our word liturgy"
    "e)ciso/w": {"acts"},                     # an example's, "acts in no way like a mother"
    # EXO 36
    "te/mnw": {"cutting", "to wound", "I made", "cut", "off", "had", "cut off", "to have", "wrought", "hewn",
               "by felling the trees", "cutting the corn"},  # examples' pieces
    "e)ggra/fw": {"having", "written on", "flores inscripti nomina."},  # an example's pieces; Virgil
    "gra/mma": {"to read", "kept school"},     # examples'
    "e)pi/keimai": {"off the coast", "having their", "covered", "under an assumed"},  # examples' pieces
    "xala/w": {"having unbent"},               # an example's participle
    # EXO 35
    "sunaqroi/zw": {"collected amounts", "has not joined"},  # examples', the passive's and a single person's
    "para/rruma": {"anything drawn along the side: a leathern", "hair curtain, stretched along"},  # cut, whole in MARKUP_LOST
    "suni/hmi": {"to the intelligent"},         # the participle's, an example's
    # EXO 34
    "a)lhqino/s": {"true"},                    # an example's, "to turn out a «true» man"
    "a)llo/fulos": {"with foreigners"},        # an example's, πόλεμος ἀλλ.
    "xrw=ma": {"the surface, skin: the colour of the"},  # "«the colour of the» skin", cut, whole in MARKUP_LOST
    # EXO 33
    "a)/peimi": {"return"},
    "skope/w": {"considering", "being considered"},  # an example's participles, σκοπῶν καὶ σκοπούμενος
    "oi)ktei/rw": {"to pity", "for", "because of"},  # "«to pity» one «for» or «because of» a thing", cut, whole in MARKUP_LOST
    "penqiko/s": {"mourning"},                  # the adverb's example, πενθικῶς ἔχειν                    # an example's, ἄπιτε ἐς ὑμέτερα, after "to return"
    "fi/los": {"pleases", "please", "his own", "friends", "fain", "in a manner dear", "pleasing", "kindly"},  # predicative and adverbial uses' examples
    # EXO 32
    "i(la/skomai": {"to make", "propitious to one, conciliate"},  # "«to make» him «propitious to one, conciliate» him", cut, whole in MARKUP_LOST
    "troph/": {"bruma", "appears to turn his course", "a change", "by figures", "tropes",  # Latin; an explanation's; cut, whole in MARKUP_LOST
               "the turning of the enemy, putting", "to flight, a rout", "flight", "in the rout"},  # cut, whole in MARKUP_LOST; examples'
    "a)naka/mptw": {"to bend one's steps"},    # "«to bend one's steps» back", cut, whole in MARKUP_LOST
    "ei)=mi": {"I shall go, shall come. to come", "go", "goes", "go and"},  # two translations run together, whole in MARKUP_LOST; examples' pieces
    "ta/xos": {"for speed"},                   # an example's, ὡς τάχεος εἶχεν
    "grafh/": {"in a picture"},                # an example's, ὅσον γραφῇ
    "o(/rmhma": {"for"},                       # the example's "«longings» … «for» Helen", a piece
    "sune/rxomai": {"engaged in, contested"},  # the battle's participle, an example's
    "parabai/nw": {"standing beside", "the transgressors", "though offences are committed"},  # participles' in examples
    # EXO 31
    "a)nakale/w": {"from"},                    # "esp. «from» exile", a piece of to recall
    "qei=os": {"by divine", "most marvellous", "distinction"},  # examples' pieces: θείᾳ μοίρᾳ, the superlative, a title's
    # EXO 30
    "*)=iris": {"Iris"},                       # the goddess's name, and the plant's, whole in MARKUP_LOST
    "o)/nuc": {"my fingers' ends", "on tiptoe", "de tenero ungui"},  # phrases', ἐξ ἄκρων ὀνύχων and the like; Horace
    # EXO 29
    "teleio/w": {"to make", "perfect, complete, accomplish", "to bring", "to perfection",  # cut, whole in MARKUP_LOST
                 "when", "had their wishes accomplished", "successful"},  # examples' pieces
    "proti/qhmi": {"let", "lie in state", "to set out", "for show", "sale", "was", "allowed",  # cut, whole in MARKUP_LOST
                   "first", "over", "proposed to themselves, observed", "appointed"},  # the or-alternatives' pieces; middle examples'
    "zw/nnumi": {"girded on his", "to gird on one's"},  # the middle's examples' pieces
    "me/los": {"limb by limb", "in tune", "out of tune"},  # phrases', κατὰ μέλεα, ἐν μέλει, παρὰ μέλος
    "a)mno/s": {"lambs"},                       # an example's, "lambs in temper"
    "kaqarmo/s": {"an atonement", "by purifying", "avert", "by purification", "a purifying"},  # examples' pieces
    # EXO 28
    "ai)/sqhsis": {"to have a perception of", "perceive", "to give a perception", "to become perceptible",
                   "visions"},                  # phrases', αἴσθησιν ἔχειν and of things; an example's, αἰσθήσεις θεῶν
    "zw/nh": {"upper-girdle", "under the breasts)", "girdle", "belt", "rest oneself", "for girdle-money", "pin-money)"},  # the στρόφιον's, set against it; examples' repeats; phrases'
    "poi/hsis": {"(action)"},                  # πρᾶξις's, set against it
    "te/xnh": {"wise", "means", "craft", "to practise", "professionally", "a trade"},  # phrases' and examples' repeats
    "logei=on": {"part", "speakers"},           # pieces of "the part of the stage occupied by the speakers"
    "r(uqmo/s": {"time", "in numerum", "kind"},  # an example's repeat; Virgil; an example's
    "spiqamh/": {"inches"},                    # "about 7 1/2 inches", the span measured in English
    "xrw/s": {"close to the skin", "close", "nearly", "home", "so as to shave", "graze", "near at hand, hard by"},  # phrases', ἐν χροΐ and ἐν χρῷ
    "mi/tra": {"beneath", "over"},             # the description's, beneath the cuirass and over it
    "me/twpon": {"line"},                      # a phrase's, ἐπὶ μετώπου
    "e)carta/w": {"having", "hung on one, be furnished with"},  # cut, whole in MARKUP_LOST
    "ple/kw": {"having twisted me"},           # the middle's example
    "perikalu/ptw": {"put", "as a cloak round"},  # pieces of an example
    "sumple/kw": {"joining", "we are entangled", "engaged with"},  # examples'
    "ei)/seimi": {"I will", "come before", "it came into their minds"},  # examples' and their pieces
    "sunufai/nw": {"web was woven"},           # an example's, "this web was woven"
    "leitourge/w": {"the services performed"},  # an example's, τὰ λελειτουργημένα
    "xri/w": {"poison) one's", "to smear their"},  # examples' pieces
    "e)pa/gw": {"against", "lay", "to it"},    # pieces of examples
    "sune/xw": {"to keep", "together, keep", "from falling to pieces", "together, make", "pull in time"},  # cut, whole in MARKUP_LOST
    # EXO 27
    "foreu/s": {"pack-"},                      # a piece of an example, "a pack- horse"
    "koi=los": {"when no one is in it", "a hollow", "hollow", "cava flumina)"},  # an example's paraphrase, of a bed; examples' repeats, a way and a voice; Virgil
    "i(sti/on": {"sail", "the sails"},          # examples' repeats, "to lower or furl sail", "to keep the sails close-reefed"
    "kataskeuh/": {"in preparing for"},        # a phrase's, ἐν κατασκευῇ τοῦ πολέμου
    "e)sxa/ra": {"the watch-fires"},           # a phrase's, πυρὸς ἐσχάραι
    "a)/rguros": {"white"},                    # the gloss of ἀργός, from which the word is derived
    "kaqaro/s": {"a clear, open", "clear", "clear and open", "cleared away", "citizens of pure blood", "a real, genuine",
                 "the sound portion", "clear, exactly balanced",  # examples', of a space, a way, a river, a hindrance, the marks, citizens, a saying, an army, accounts
                 "sceleris purus",              # Horace
                 "pure", "with clean hands, honestly", "clearly, plainly"},  # the adverb's
    "sunta/ssw": {"to draw up", "in line with", "in the", "order", "with", "having drawn up his", "the conspirators"},  # examples' and their pieces
    # EXO 26
    "suna/ptw": {"to bind", "fast", "with misery", "to connect", "with", "refer", "to", "involved", "engaged",
                 "in conflict"},               # cut, whole in MARKUP_LOST; examples' and their pieces
    "i)/sos": {'"measure', 'measure, "', "half and half", "tit for tat", "equally divided",
               "the equal division of all civic rights", "fair", "even as", "like", "equally", "like as, as if",
               "alike"},                        # phrases'; an example's repeat; the adverbs'
    "diori/zw": {"to determine", "to be"},   # "to determine one to be", cut, whole in MARKUP_LOST
    "moxlo/s": {"vectis"},                    # the Latin
    "o)pi/sqios": {"the hind-"},              # a piece of an example, "the hind- legs"
    "sumbolh/": {"encounter", "charges.", "de symbolis esse"},  # Aristophanes' play, repeated; Terence's Latin
    "xa/lkeos": {"a bronze", "for a shield of brass", "of brass", "ferreus somnus"},  # examples', of a statue, a prize, a heart; Virgil
    "ne/w": {"spun"},                          # an example's, the middle, of the Fates
    # EXO 25
    "i(lasth/rion": {"propitiatory"},        # the adjective's; the noun is "as Subst." inside ἱλαστήριος
    "u(a/kinqos": {"hyacinth", "dark blue", "dark", "black.", "jacinth"},  # the entry's prose on the flower's colour, a repeat; "not (prob.) our jacinth"
    "qri/c": {"the hair", "only a hair's breadth"},  # an example's repeat; a proverb's
    "ai)/geios": {"of a goat", "goats"},       # cut, whole in MARKUP_LOST
    "podh/rhs": {"that falls over the feet", "which covered the body quite down to the feet",
                 "the parts about the feet, the feet"},  # examples', of a frock and a shield; the neuter plural's as a noun
    "para/deigma": {"example"},               # a phrase's, ἐπὶ παραδείγματος
    "strepto/s": {"pliant", "a collar of twisted", "linked metal", "to be bent", "turned", "may be turned",
                  "a glib, pliant"},            # an example's repeat; cut, whole in MARKUP_LOST; an example's
    "tra/peza": {"four-legged a table", "table", "Siculae dapes", "the bank", "bankers"},  # τετράπεζα's gloss run into the first sense, restored in MARKUP_LOST; a repeat; Horace; a repeat; a phrase's
    "suskia/zw": {"to shade quite over, throw a shade over, shade closely", "thickly"},  # cut, whole in MARKUP_LOST
    "e)pa/nwqen": {"men of former time"},      # a phrase's, οἱ ἐπάνωθεν
    "kataxruso/w": {"splendid"},               # the gloss of "golden", "i. e. splendid"
    "a)ki/nhtos": {"immovable", "not to be stirred", "touched, inviolate"},  # the adverb's; cut, whole in MARKUP_LOST
    "lu/xnos": {"lamplighting time"},          # a phrase's, περὶ λύχνων ἁφάς
    "stefa/nh": {"coronal"},                   # an example's repeat
    "klw/qw": {"one's destiny"},               # a phrase's, τὰ κλωσθέντα
    "ta/lanton": {"l.", "coin"},              # pounds sterling; "no such coin as a talent"
    "tu/pos": {"the print", "marks", "the sound of", "tread", "anything wrought of metal", "stone",
               "in outline, in general"},       # a repeat; the plural's, letters; cut, whole in MARKUP_LOST; a phrase's
    "e)lau/nw": {"on", "drove on", "harass", "shall persecute", "they drove it", "he struck", "struck", "thrust",
                 "to beat with", "he made", "of beaten", "to draw a line of", "has its", "carried down", "plant",
                 "in line"},                    # pieces and examples'; cut, whole in MARKUP_LOST
    # EXO 24
    "gra/fw": {"having scratched", "to write", "name", "to write for oneself", "for one's own use, note down", "for",
               "the prosecutors", "the articles of the indictment", "the penalty named in the indictment"},  # an example's; cut, whole in MARKUP_LOST; a piece; the participles' as nouns
    "a)nagignw/skw": {"to know", "again", "students", "he had persuaded"},  # cut, whole in MARKUP_LOST; the participle's as a noun; an example's
    "prosxe/w": {"to pour to", "on"},          # cut, whole in MARKUP_LOST
    "diafwne/w": {"with"},                     # a piece, the dative's τινι
    "nomoqete/w": {"it hath been", "ordained by law"},  # cut by "so", whole in MARKUP_LOST
    "e)gxe/w": {"to fill the κλεψύδρα"},       # a phrase's, ἐγχεῖν ὕδωρ τινί
    "kataskeda/nnumi": {"pour upon", "over", "to spread", "against", "to pour", "sprinkle about"},  # cut, whole in MARKUP_LOST
    "krath/r": {"bowls of wine"},              # an example's, the plural of "a bowl of wine"
    "fle/gw": {"making", "blaze", "flash", "letting", "blaze up", "to make illustrious", "famous", "to be",
               "become so"},                    # cut, whole in MARKUP_LOST
    # EXO 23
    "pe/nhs": {"(beggar)"},                    # πτωχός's, in the distinction the entry draws
    "sugkatati/qhmi": {"to deposit together", "at the same time", "to deliver", "with"},  # cut, whole in MARKUP_LOST; a phrase's, σ. τινι τὴν αὐτὴν δόξαν
    "lumai/nomai": {"to inflict indignities", "outrages upon"},  # cut, whole in MARKUP_LOST
    "ptwxo/s": {"one who crouches", "cringes, a beggar", "a beggar-man", "poorly, scantily"},  # cut, whole in MARKUP_LOST; a phrase's, πτωχὸς ἀνήρ; the adverb's
    "a)nayu/xw": {"to let", "rest and get dry, relieve", "dry off", "to give", "relief from"},  # cut, whole in MARKUP_LOST
    "sunte/leia": {"defrayed by subscription"},  # a phrase's, εἰς σ. ἄγειν
    "u(poste/llw": {"made", "furl", "to shelter", "behind", "to cloak", "through fear, to prevaricate, dissemble",
                    "dissimulation"},  # cut, whole in MARKUP_LOST; a phrase's, μηδὲν ὑποστειλάμενος
    "a)nti/keimai": {"by way of opposition"},  # the adverb's, ἀντικειμένως
    "a)/dikos": {"towards", "wrong", "jure an injuria", "without reason"},  # a piece, ἐς τινα after "unjust in"; the neuter plural's as a noun, an example's; the adverb's
    "dikaio/w": {"to hold", "deem right, think fit, demand", "to do a man right", "justice, to judge",
                 "to refuse"},  # cut, whole in MARKUP_LOST; a phrase's, οὐ δ.
    "e)ci/sthmi": {"to drive", "out of"},       # "to drive one out of" cut, whole in MARKUP_LOST; an example's piece
    "e)rh=mos": {"in solitude", "in which one party does not appear", "by default", "judgment by default",
                 "in a case where there was no defence"},  # the neuter plural's as an adverb; ἐρήμη δίκη's, phrases'
    "a)/grios": {"a countryman", "to harsher measures", "more wild, stormy", "a malignant disease", "savagely"},  # a label, "of a countryman, as opp. to a citizen"; the comparative's; a phrase's, ἀγρ. νόσος; the adverb's
    # EXO 13
    "mnhmoneu/w": {"to call to", "mind, mention"},  # "to call to another's mind, mention", cut in two
    "metame/lei": {"I repent of", "since it repented", "they repented that",
                   "that which will cause regret, matter for future repentance"},  # examples' translations
    "o(dhge/w": {"upon his way"},                # an example's piece
    # EXO 12
    "a)rke/w": {"will suffice", "'tis enough", "am content", "there is", "help", "enough", "good"},  # examples'
    "e)niau/sios": {"for a year"},               # a repeat of "for a year, lasting a year"
    "w)mo/s": {"raw", "savagely", "rudely, coarsely", "a more coarse, more unmitigated"},  # a repeat; the adverbs'; the comparative's
    "perizw/nnumai": {"put", "on", "to have", "girded round them"},  # examples' pieces
    "spoudh/": {"speed", "pains", "much ado about", "with great attention to", "busily", "in earnest, seriously"},  # repeats; phrases'
    "pai/w": {"he smote his", "struck", "dashed", "strikes on"},  # examples' translations
    "e)nde/w": {"bound", "fast", "having packed", "up", "entangled", "in", "to have", "secured"},  # examples' pieces
    "pezo/s": {"by land", "beasts"},             # τὰ πεζά, a phrase's and the neuter's
    "no/mos": {"custom", "law", "by the law of force, in the fight", "scuffle", "in actual warfare", "to blows", "tunes"},  # repeats; phrases'
    "meso/w": {"mid-", "mid", "in the middle of"},  # examples' translations
    "ba/ptw": {"to dye", "by dipping", "having dipped", "so as to draw"},  # a repeat; examples' pieces
    "kaqikne/omai": {"hast touched", "came down upon"},  # examples' translations
    # EXO 11
    "plhgh/": {"a blow"},                        # a repeat of "a blow, stroke"
    "e)kbolh/": {"turning", "out of", "the time when", "comes into ear", "earth cast", "scraped up",
                 "children exposed", "wrecked"},  # examples' pieces and translations
    "ku/wn": {"a word of reproach"},             # the use's label, not a translation
    "a)fhge/omai": {"the van", "what has been told"},  # participles used as nouns, examples'
    # EXO 10
    "e(ch=s": {"the next"},                      # ἡ ἑξῆς ἡμέρα, the phrase's; "next" is a sense above it
    "a)/nemos": {"the wind", "to the winds"},     # a repeat with the article; ἀνέμοις, an example's dative
    "qu/ella": {"thunderstorms"},                # πυρὸς θύελλαι, the phrase's
    "e)ruqro/s": {"the Erythraean sea", "Red Sea", "Arabian Gulf", "Indian Ocean", "the Persian Gulf"},  # Ἐρυθρὴ θάλασσα, the phrase's
    "fa/os": {"day-light", "light", "the light", "light of my life"},  # repeats of "light, daylight"; γλυκερὸν φάος, an address
    "fu/w": {"made", "grow", "will bring to light", "birth", "is", "by nature", "to fall", "grew", "natural lot",
             "it is natural", "is natural", "by nature, be"},  # examples' pieces and translations
    # EXO 9
    "r(hto/s": {"stated", "on stated terms, on certain conditions", "expressly, distinctly"},  # a repeat; ἐπὶ ῥητοῖς, the phrase's; the adverb ῥητῶς
    "o(/ros": {"the boundary between", "as the limit", "cippi)"},  # pieces of examples, the Latin
    "e(/lkos": {"of plague-ulcers"},           # the use's label, not a translation of the word
    "u(/w": {"when it is raining", "as it was raining", "it did", "rain on", "was rained upon", "it rained"},  # examples'
    "pa/ssw": {"laying", "upon", "sprinkle some", "to work", "in embroidery"},  # examples' pieces
    "e)mpoie/w": {"introduced by", "poet's art"},  # a passive example's pieces
    "li/non": {"lint-"},                         # a piece of "lint-seed"
    "plh/ssw": {"struck", "on", "having driven", "having smitten his", "I have lost", "by this blow", "from", "moved"},  # examples' pieces and translations
    # EXO 8
    "kni/y": {"insect which gnaws"},              # cut from "a small … figs", whole in MARKUP_LOST
    "kalu/ptw": {"to be buried", "I will put", "over"},  # κ. χθονὶ γυῖα, a phrase's; pieces of an example
    "a)fani/zw": {"hypocritical", "to make away with"},  # a piece; "make away with" again, of property
    "o)/zw": {"smelling", "smelling of", "there is a", "smell from", "there will be an odour of", "from"},  # examples' pieces
    "e)capata/w": {"in"},                       # a piece of e)c. tina/ ti "in" a thing
    "da/ktulos": {"the fingers", "the thumb", "the toes"},  # phrases' translations: μέγας δ., δάκτυλοι ποδῶν
    # EXO 7
    "suni/sthmi": {"is joined", "were at issue"},  # examples' translations of finite forms
    "metaba/llw": {"to throw one's", "over", "to drink different", "to change", "give up",
                   "changing his course and turning", "to change one's", "to exchange", "for"},  # examples' pieces and translations
    "sofisth/s": {"an adept", "a professor of"},  # an example's repeat; a piece of "a professor of grammar, rhetoric …"
    "koitw/n": {"a chamberlain, praefectus cubiculi"},  # ὁ ἐπὶ τοῦ κοιτῶνος, the phrase's, with the Latin
    "w(sau/tws": {"in like manner"},             # ὡσαύτως καί, an example's repeat
    # EXO 7
    "no/os": {"heedfully", "senselessly", "wisely", "in mind", "sensible", "one's mind", "heart and soul",
              "intend", "to intend"},           # phrases' translations: νόῳ, παρὲκ νόον, σὺν νόῳ, ἐκ παντὸς νόου, ἐν νόῳ ἔχειν
    # EXO 6
    "su/n": {"help", "blessing", "as standing with", "on", "side, of", "party", "together", "besides, also, likewise",
             "with, along with, together", "to kill one person as well as another", "to join with another in killing.",
             "altogether, completely", "two together", "by twos, two and two"},  # pieces of examples ("with God's help or blessing", "on his side, of his party"); the adverb's and compounds' senses
    "a)/logos": {"a horse"},                     # "in modern Greek ἄλογον is a horse"
    # EXO 5
    "a)polei/pw": {"to leave", "in the lurch", "wanting", "of", "wanted", "without", "cognisance"},  # "to leave one in the lurch" cut in two, whole in MARKUP_LOST; examples' pieces
    "sxola/zw": {"respite from", "opportunity for"},  # cut from their verbs, whole in MARKUP_LOST
    "merimna/w": {"cares"},                      # the object of an example, πολλὰ μ.
    "kala/mh": {"straw", "slaughter", "-straw", "the stubble", "the residue)"},  # examples' repeats, what the metaphor means, a piece of wheat-straw
    "fo/nos": {"a slaughter", "murder, homicide", "for", "murder and manslaughter", "of blood"},  # an example's, the first sense repeated, pieces, an example pair's
    "ou)ke/ti": {"(not yet)"},                   # what οὔπω means, set against it
    "kaqh/kw": {"came", "is come", "[the time]", "comes", "duty it is"},  # examples' translations
    "e)rhmo/w": {"of", "without"},                # pieces of "to bereave one of", "to leave the oars without men"
    # ἄν: a paragraph on the particle's uses, tagged as one translation, opens the card.
    "a)/n": {'conditional Particle. In attic, it is not joined with pres. or perf. ind., nor with imperat. of any tense. Three uses of a)/n must be distinguished in practice: in combination with Conjunctions and Relatives. in Apodosis. in Iterative sentences. in combinations with Conjunctions and Relatives: such words are regularly foll. by the subj., viz. e)a/n (= ei) a)/n) h)/n, a)/n , e)ph/n; o(\\s a)/n quicunque'},
}

# Senses a word filed under another word's entry keeps, though that entry's NOT_SENSES sets
# them aside. νή is the particle of oaths, with the accusative of what is sworn by; ναί's own
# "yea by", which ναί's card sets aside as an oath formula, is the sense νή's parse calls for.
KEEP_SENSES = {"nh/": {"yea by . ."}}

# An entry that divides its senses by tense and voice, so that which of them belong to a
# form depends on the form's parse and not on its lemma alone. For a form whose tense and
# voice are among those listed, the set given here is skipped in place of NOT_SENSES.
_ISTHMI_INTR = {
    "to be set", "placed, to stand", "to be there", "to be in a", "state", "condition",
    "to lie, be situated", "to stand still, stop, halt", "to stand idle",
    "to stop, cease, be at rest", "to stand firm", "to stand up, rise up", "to arise, begin",
    "was beginning", "began", "begins", "two", "three", "to be appointed"}
_APHISTHMI_INTR = {
    "to stand away", "aloof from, keep far from", "to lose", "to withdraw from", "to revolt from",
    "to revolt", "to give up", "to make way", "give way", "to shrink from", "to stand aloof"}
_EPHISTHMI_CAUS = {
    "to set", "place upon", "to set over", "to set up, establish, institute", "to set by", "near to",
    "to stop, make halt", "attend", "to give attention", "to arrest the attention"}
_EPHISTHMI_INTR = {
    "to stand upon", "to be imposed upon", "to stand on the top", "surface", "to be set over",
    "to be in authority", "to stand by", "near", "to appear to", "to stand against, oppose",
    "to come upon by surprise", "to impend, be at hand", "to halt, stop",
    "to fix one's mind on, give one's attention to"}
_EPHISTHMI_MID = {"to set up", "to set, post"}
_EPHISTHMI_SCRAPS = {"having halted", "to fix one's", "cream"}  # an example's, a piece, i.e.
_ANAIREO_ACT = {
    "to take up, raise", "to take up and carry off, bear away", "to take up", "to make away with, to destroy, kill",
    "to abolish, annul", "to destroy", "confute", "to appoint, order", "to answer, give a response"}
_ANAIREO_MID = {
    "to take up for oneself, take up", "to gain, win, get, achieve", "to exact", "to take up and carry off, snatch away",
    "to take up in one's arms", "to conceive in the womb", "to take upon oneself, undertake",
    "to undertake, contract for the execution of", "to accept as one's own", "to take back to oneself, cancel"}
_ANAIREO_SCRAPS = {"for burial", "own", "against", "to entertain"}  # pieces of examples
_EXANISTHMI_INTR = {
    "bid one", "rise", "to stand up from one's seat", "to arise and depart from, emigrate from",
    "to break up, depart", "to be driven out", "to be forced to emigrate", "to be depopulated"}
_EXANISTHMI_CAUS = {
    "to raise up: to make one rise", "bid one", "rise", "to order", "to rise", "to make",
    "emigrate, to remove", "expel", "to depopulate, destroy", "to rouse", "from their lair"}
_APOLLUMI_ACT = {"to destroy utterly, kill, slay", "to destroy, demolish, waste", "to talk", "bore", "to death",
                 "to lose utterly"}
_APOLLUMI_MID = {"to perish utterly, die", "to be undone", "you are done for, lost, ruined",
                 "to be lost, slip away, vanish"}
FORM_SENSES = {
    # EXO 29. τελειόω's and ζώννυμι's active leave out the middle's and the passive's; προτίθημι's middle-passive and
    # passive the middle's; τάσσω's middle the active's and the passive's.
    "ta/ssw": [("PIFAXY", "M", {
        "to arrange, put in order", "to draw up in order of battle, to form, array, marshal", "to be drawn up",
        "in rank and file", "to post, station", "to appoint", "over", "to be appointed to", "to appoint one to do",
        "to be appointed", "to order", "to assign to", "set", "to join", "to place in a certain order",
        "to appoint, ordain, order, prescribe", "fix", "certain", "to fix", "fixed, prescribed"})],
    "teleio/w": [("PIFAXY", "A", NOT_SENSES["teleio/w"] | {
        "to be accomplished", "to be fulfilled", "to attain perfection, come to the end of one's labours",
        "to reach maturity"})],
    "zw/nnumi": [("PIFAXY", "A", NOT_SENSES["zw/nnumi"] | {
        "to gird oneself, gird up one's loins", "to gird up one's loins, prepare for battle"})],
    "proti/qhmi": [("PIFAXY", "EP", NOT_SENSES["proti/qhmi"] | {
        "to have set before one", "to propose to oneself", "to put forth on one's own part, display, shew",
        "to set before oneself", "to put in front"})],
    # EXO 28. αἴσθησις's and τέχνη's singular leave out the plural's; ἐπάγω's middle the active's; χρίω's active the
    # middle's and the passive's.
    "ai)/sqhsis": [("-", "-", NOT_SENSES["ai)/sqhsis"] | {"the senses"}, None, "^.....S")],
    "te/xnh": [("-", "-", NOT_SENSES["te/xnh"] | {"arts, wiles, cunning devices"}, None, "^.....S")],
    "e)pa/gw": [("PIFAXY", "M", NOT_SENSES["e)pa/gw"] | {
        "to bring on", "to bring upon", "to set on, urge on", "to lead on", "to lead on by persuasion, influence",
        "to induce", "to bring in, invite", "to bring to", "bring in", "to bring in, supply", "to lay on", "apply",
        "to bring forward, propose", "to bring in over and above, to add", "to intercalate"})],
    "xri/w": [("PIFAXY", "A", NOT_SENSES["xri/w"] | {"to anoint oneself", "to anoint", "to be coloured"})],
    # EXO 27. παραδείκνυμι's active and passive leave out the middle's; ποικιλία's and λύχνος's singular the plural's;
    # καίω's and συντάσσω's active the middle's and the passive's; κόπτω's middle-passive and passive the middle's.
    "paradei/knumi": [("PIFAXY", "AP", {"to exhibit, bring forward"})],
    "poikili/a": [("-", "-", {"pieces of broidery"}, None, "^.....S")],
    "lu/xnos": [("-", "-", NOT_SENSES["lu/xnos"] | {"the lamp-market"}, None, "^.....S")],
    "kai/w": [("PIFAXY", "A", NOT_SENSES["kai/w"] | {"to be lighted, to burn", "to be burnt", "parched up"})],
    "sunta/ssw": [("PIFAXY", "A", NOT_SENSES["sunta/ssw"] | {
        "to be drawn up in line", "to form in line", "to be collected, resolute, steady", "to be organised",
        "to be organised for paying contributions", "to agree to such assessment", "to be prescribed",
        "to agree together", "to take leave of", "bid", "farewell"})],
    "ko/ptw": [("PIFAXY", "EP", NOT_SENSES["ko/ptw"] | {"to coin oneself", "order to be coined", "to beat one's breast",
                                                        "to mourn for"})],
    # EXO 26. συνάπτω's active leaves out the middle's and the passive's; ἴσος's masculine and feminine the neuter's
    # as a noun; δέρρις's and συμβολή's singular the plural's; κατακαλύπτω's active the middle's.
    "suna/ptw": [("PIFAXY", "A", NOT_SENSES["suna/ptw"] | {"to have intercourse with", "to get one's daughter",
                                                           "to be next to, connected with", "to take part with",
                                                           "to assist", "to bring upon oneself"})],
    "i)/sos": [("-", "-", NOT_SENSES["i)/sos"] | {"an equal share, fair measure", "equal rights, equality"}, None,
                "^......[MFC]")],
    "de/rris": [("-", "-", {"screens of hide"}, None, "^.....S")],
    "katakalu/ptw": [("PIFAXY", "A", {"having veiled oneself"})],
    "sumbolh/": [("-", "-", NOT_SENSES["sumbolh/"] | {"contributions"}, None, "^.....S")],
    # EXO 25. στρεπτός's neuter and feminine leave out the masculine noun's, "a collar of twisted or linked metal",
    # "a twist" or "roll"; τάλαντον's and τύπος's singular the plural's; χρυσόω's and ἐλαύνω's active the
    # passive's; φαίνω's active the middle's, the passive's and the passive's examples.
    "strepto/s": [("-", "-", NOT_SENSES["strepto/s"] | {"a collar of twisted or linked metal", "a twist", "roll"},
                   None, "^......[NF]")],
    "ta/lanton": [("-", "-", NOT_SENSES["ta/lanton"] | {"a pair of scales"}, None, "^.....S")],
    "tu/pos": [("-", "-", NOT_SENSES["tu/pos"] | {"figures worked in relief"}, None, "^.....S")],
    "xruso/w": [("PIFAXY", "A", {"to be gilded"})],
    "fai/nw": [("PIFA", "A", NOT_SENSES["fai/nw"] | {
        "to exhibit as one's own", "informed against", "appeared", "to come to light, be seen, appear", "to shine brightly",
        "to come into being", "born", "shewn to be, having become", "what has once come to light", "to appear to be",
        "a thing appears to be", "that it manifestly is", "appear", "manifestly", "manifestly harms",
        "appears likely to harm", "they were manifest", "do I look like", "does this appear", "yes",
        "nullo in loco haberi"})],
    "e)lau/nw": [("PIFAXY", "A", NOT_SENSES["e)lau/nw"] | {"to go through"})],
    # EXO 24. γράφω's, νομοθετέω's, ἐγχέω's, κατασκεδάννυμι's and φλέγω's active leave out the middle's and the
    # passive's; ἀνέγνω, the second aorist, leaves out the Ionic first aorist's "to persuade" or "induce" and its
    # passive; ἡσυχάζω is "causal in aor1", and its other tenses leave out "to make still, lay to rest".
    "gra/fw": [("PIFAXY", "A", NOT_SENSES["gra/fw"] | {"to write for oneself or for one's own use, note down", "to indict",
                                                       "denounce", "to be indicted"}),
               # EXO 31. The perfect passive reads the active's senses in the passive and the passive's own, less the
               # middle's and "to move that", whose clause the passive cannot hold (Q21).
               ("PIFAXY", "EP", NOT_SENSES["gra/fw"] | {"to write for oneself or for one's own use, note down",
                                                        "to indict", "denounce", "to move that"})],
    "a)nagignw/skw": [("A", "A", NOT_SENSES["a)nagignw/skw"] | {"to persuade", "induce", "to be persuaded"},
                       "γνω(ν|ς|μεν|τε|σαν)?$")],
    "nomoqete/w": [("PIFAXY", "A", NOT_SENSES["nomoqete/w"] | {"to make laws for oneself, frame laws",
                                                               "it hath been ordained by law"})],
    "e)gxe/w": [("PIFAXY", "A", NOT_SENSES["e)gxe/w"] | {"to fill one's cup"})],
    "kataskeda/nnumi": [("PIFAXY", "A", NOT_SENSES["kataskeda/nnumi"] | {"to pour or sprinkle about"})],
    "h(suxa/zw": [("PIFXY", "A", NOT_SENSES["h(suxa/zw"] | {"to make still, lay to rest"})],
    "fle/gw": [("PIFAXY", "A", NOT_SENSES["fle/gw"] | {"to take fire, blaze up", "to blaze up, be a-light",
                                                       "to be or become so"})],
    # EXO 23. συγκατατίθημι's middle and ὑποστέλλω's read the middle's senses; συνεγείρω's active and ἀναψύχω's
    # leave out the passive's; πτωχός's masculine and neuter leave out the feminine's "a beggar-woman", πτωχή.
    "sugkatati/qhmi": [("PIFAXY", "ME", NOT_SENSES["sugkatati/qhmi"] | {"to deposit together or at the same time"})],
    "sunegei/rw": [("PIFAXY", "A", {"to rise together"})],
    "a)nayu/xw": [("PIFAXY", "A", NOT_SENSES["a)nayu/xw"] | {"to be revived, refreshed"})],
    "u(poste/llw": [("PIFAXY", "ME", NOT_SENSES["u(poste/llw"] | {"to draw in", "made him furl", "to draw back for shelter",
                                                                  "to shelter oneself behind", "to withdraw"})],
    "ptwxo/s": [("-", "-", NOT_SENSES["ptwxo/s"] | {"a beggar-woman"}, None, "^......[MN]")],
    # EXO 31. ἀνακαλέω's middle reads the senses Middle Liddell gives "so in Mid." and "Mid.", less the active's "to
    # summon, cite", "to call" by a name and "to call on"; τεκτονικός's neuter leaves out the masculine's and the
    # feminine's as nouns, "a good carpenter or builder" and "joiners' work, carpentry".
    "a)nakale/w": [("PIFAXY", "ME", NOT_SENSES["a)nakale/w"] | {"to summon, cite", "to call", "to call on"}),
                   # EXO 35. The active leaves out the middle's own: "Mid. to call to oneself, send for, summon",
                   # "Mid. … to cheer on".
                   ("PIFAXY", "A", NOT_SENSES["a)nakale/w"] | {"to call to oneself, send for, summon", "to cheer on"})],
    "tektoniko/s": [("-", "-", {"a good carpenter", "builder", "joiners' work, carpentry"}, None, "^......N")],
    # οἰκέτης's singular leaves out "οἱ οἰκέται … one's household, the women and children", the plural's (EXO 32).
    "oi)ke/ths": [("-", "-", {"one's household, the women and children"}, None, "^.....S")],
    # EXO 33. ἄπειμι's "be gone" is the imperative's, οὐκ ἄπει; = ἄπιθι. φίλος's masculine leaves out the feminine's,
    # the neuter's and the superlative's as nouns.
    "a)/peimi": [("PIFAXY", "A", NOT_SENSES["a)/peimi"] | {"be gone"}, None, "^...[^D]")],
    "e)mfani/zw": [("PIFAXY", "A", {"to become visible"})],
    # EXO 34. νέμω's middle and passive read the first sense in the passive, the senses Middle Liddell marks "Mid."
    # and "Pass.", and leave out the active's own, as GEN 41:3's ἐνέμοντο has them. χρῶμα's singular leaves out
    # "metaph. in pl. ornaments, embellishments".
    "ne/mw": [("PIFAXY", "ME", NOT_SENSES["ne/mw"] | {
        "to pay", "to hold, possess", "to hold sway, manage", "to manage", "to support", "to use",
        "to hold, consider as", "to take", "to pasture", "graze", "drive to pasture, tend", "to graze", "to give"})],
    "xrw=ma": [("-", "-", NOT_SENSES["xrw=ma"] | {"ornaments, embellishments", "embellishments in music"}, None,
                "^.....S")],
    # EXO 36. τέμνω's, κωλύω's and χαλάω's passive leave out the senses that have no passive: the absolute, the
    # intransitive, the middle's, and κωλύω's participle and impersonal third person. γράμμα's plural leaves out the
    # senses Middle Liddell marks "in sg."; ἑκουσίως, the adverb, the neuter's "voluntary acts".
    "te/mnw": [("PIFAXY", "P", NOT_SENSES["te/mnw"] | {
        "to use the knife", "to sacrifice", "to take solemn oaths", "to fell oneself", "to make", "advance"})],
    "kwlu/w": [("PIFAXY", "P", NOT_SENSES["kwlu/w"] | {
        "let there be", "hindrance", "one to hinder", "a hindrance", "there is", "nothing hinders, be it so"})],
    "xala/w": [("PIFAXY", "EP", NOT_SENSES["xala/w"] | {
        "to let go, slacken one's hold", "to become slack", "loose", "stand open", "to have a remission of",
        "to yield to", "to be indulgent to", "to remit, to grow slack"})],
    "gra/mma": [("-", "-", NOT_SENSES["gra/mma"] | {"a drawing, picture", "a bill, account"}, None, "^.....P")],
    "e(kou/sios": [("-", "-", {"voluntary acts"}, None, "^--------")],
    # EXO 35. συνίημι's and ὑφαίνω's active leave out the middle's.
    "suni/hmi": [("PIFAXY", "A", NOT_SENSES["suni/hmi"] | {"to come together, come to an agreement"})],
    "u(fai/nw": [("PIFAXY", "A", {"to weave oneself"})],
    "fi/los": [("-", "-", NOT_SENSES["fi/los"] | {"a dear one, friend", "an object of love", "one's nearest and dearest"},
                None, "^......M")],
    # EXO 32. συνίστημι's second aorist active, συνέστη, is intransitive, as the perfect is: its causal senses and the
    # perfect participle's "a well-disciplined" army and "a standing" one left out. παραβαίνω's and διασκεδάννυμι's
    # active leave out the passive's. τροπή's singular leaves out the plural's tropics and solstices. εἶμι's
    # imperative keeps ἴτω's own "let it pass, well then" and leaves out the indicative's future use; its other
    # forms the reverse.
    "parabai/nw": [("PIFAXY", "A", NOT_SENSES["parabai/nw"] | {"to be transgressed"})],
    "diaskeda/nnumi": [("PIFAXY", "A", {"to be dispersed"})],
    "troph/": [("-", "-", NOT_SENSES["troph/"] | {"the tropics", "solstices", "midsummer", "midwinter",
                                                  "the winter solstice"}, None, "^.....S")],
    "ei)=mi": [("PIFAXY", "A", NOT_SENSES["ei)=mi"] | {"I shall go, shall come"}, None, "^...D"),
               ("PIFAXY", "A", NOT_SENSES["ei)=mi"] | {"let it pass, well then"})],
    # δικαιόω's active leaves out the passive's "proved, tested", and the passive the active's constructions with
    # an infinitive, "to consent" to do and "to desire" one to do, as GEN 38:26 and 44:16 read it. ἀναπαύω's middle
    # reads the Mid. and Pass. section, as GEN 29:2 and 49:14 do. ἐξίστημι is "causal in pres., imperf., fut.,
    # aor1": its future active leaves out the intransitive senses.
    "dikaio/w": [("PIFAXY", "A", NOT_SENSES["dikaio/w"] | {"proved, tested"}),
                 ("PIFAXY", "PE", NOT_SENSES["dikaio/w"] | {"to consent", "to desire"})],
    "a)napau/w": [("PIFAXY", "ME", NOT_SENSES["a)napau/w"] | {"to make to cease, to stop", "to stop, put an end to",
                                                               "to rest, halt", "to take rest"})],
    "e)ci/sthmi": [("F", "A", NOT_SENSES["e)ci/sthmi"] | {
        "to stand aside from", "is displaced, disordered", "to shrink from, shun", "to retire from, give up possession of",
        "to cease from, abandon", "to lose", "give", "up", "to be out of one's wits, to be astonished, amazed",
        "to degenerate", "changed, sour", "disfigured", "to change one's position, one's opinion"})],
    # EXO 22. ἐνεχυράζω's active leaves out the passive's and the middle's; πιπράσκω's passive its own "to be
    # sold", which is the first sense in the passive.
    "pipra/skw": [("PIFAXY", "P", NOT_SENSES["pipra/skw"] | {"to be sold"})],
    "e)nexura/zw": [("PIFAXY", "A", {"to have one's", "seized for debt", "to have security given one, take it for oneself"})],
    # EXO 21. ἀποστερέω's active leaves out the passive's; δίκη's other cases the accusative's "δίκην as adv.,
    # after the manner of".
    "a)postere/w": [("PIFAXY", "A", NOT_SENSES["a)postere/w"] | {"to be robbed", "deprived of"})],
    "di/kh": [("-", "-", NOT_SENSES["di/kh"] | {"after the manner of"}, None, "^....[NGDV]")],
    # EXO 20. τιμάω's active leaves out the passive's and the middle's; φονεύω's the passive's.
    "tima/w": [("PIFAXY", "A", NOT_SENSES["tima/w"] | {"to be honoured, held in honour", "to be held worthy",
                                                       "to estimate"})],
    "foneu/w": [("PIFAXY", "A", {"to be slain"})],
    # EXO 19. βιάζω's middle and middle/passive read the middle's senses, as GEN 33:11 reads them;
    # ἅπτω's middle the middle's, and its future middle the passive's too, "Pass., with fut. mid. to be set
    # on fire"; ἀπαλλάσσω's active leaves out the passive's and middle's; προσάγω's middle the active's
    # and passive's; ἀφορίζω's active the middle's "to mark off for oneself", and its middle the active's.
    "bia/zw": [("PIFAXY", "ME", NOT_SENSES["bia/zw"] | {"to constrain", "to be hard pressed", "forced from one"})],
    "a(/ptw": [("F", "M", NOT_SENSES["a(/ptw"] | {"to kindle, set on fire", "to light"}),
               ("PIFAXY", "ME", NOT_SENSES["a(/ptw"] | {"to kindle, set on fire", "to light", "to be set on fire, catch fire"})],
    "a)palla/ssw": [("PIFAXY", "A", NOT_SENSES["a)palla/ssw"] | {
        "to be set free", "released from", "get rid of", "to get off", "to be acquitted", "to remove, depart from",
        "to depart", "to depart, die", "to be divorced", "to leave", "inferior to", "to leave off", "cease from",
        "to have done, give over, cease", "and be done with it", "to depart from enmity", "to be reconciled"})],
    "prosa/gw": [("PIFAXY", "M", NOT_SENSES["prosa/gw"] | {
        "to bring to", "upon", "to furnish, supply", "to put to, add", "to put to, bring to, move towards, apply",
        "to apply", "closely", "to set before", "to put", "to", "make", "take", "to bring up", "move on towards",
        "put forth", "to bring in", "before", "to introduce", "to attach oneself to", "to draw near, approach",
        "to bring to, come to land"})],
    "a)fori/zw": [("PIFAXY", "A", {"to mark off for oneself, appropriate"}),
                 ("PIFAXY", "M", {"to mark off by boundaries"})],
    # EXO 18. μόχθος's singular leaves out the plural's; the actives of διακρίνω, συμβουλεύω, σημαίνω and κουφίζω
    # leave out the middle's and passive's.
    "mo/xqos": [("-", "-", NOT_SENSES["mo/xqos"] | {"toils, troubles, hardships"}, None, "^.....S")],
    "diakri/nw": [("PIFAXY", "A", NOT_SENSES["diakri/nw"] | {"to be parted", "to part and join different",
                                                             "to be dissolved into elemental parts", "to come to a decision",
                                                             "to contend", "to doubt, hesitate"})],
    "sumbouleu/w": [("PIFAXY", "A", NOT_SENSES["sumbouleu/w"] | {"to consult with", "to consult, deliberate"})],
    "shmai/nw": [("PIFAXY", "A", NOT_SENSES["shmai/nw"] | {"to give oneself a token", "conclude from signs, conjecture",
                                                           "to mark for oneself"})],
    "koufi/zw": [("PIFAXY", "A", NOT_SENSES["koufi/zw"] | {"to be lifted up, soar", "to be relieved",
                                                           "to feel one's burthens lightened"})],
    # EXO 17. ἐπιλέγω's active leaves out the middle's; καθίημι's active
    # the passive's; στηρίζω's active the middle's and passive's, and its passive the middle's. τρέπω: "in
    # aor1 mid., to put an enemy to flight", and that alone (15:13's ἐτρέψατο).
    "e)pile/gw": [("PIFAXY", "A", NOT_SENSES["e)pile/gw"] | {"to think upon, think over", "to deem", "expect that",
                                                            "to con over, read"})],
    "kaqi/hmi": [("PIFAXY", "A", NOT_SENSES["kaqi/hmi"] | {"to come down", "to be put in motion"})],
    "sthri/zw": [("PIFAXY", "A", NOT_SENSES["sthri/zw"] | {"to fix for oneself", "to be firmly set or fixed, to stand fast or steady"}),
                 ("PIFAXY", "MEP", NOT_SENSES["sthri/zw"] | {"to fix for oneself"})],
    "tre/pw": [("A", "M", {"to turn", "direct", "to shew", "to turn one's steps, turn in a certain direction", "to roam",
                           "to take", "betake oneself", "to be turned", "look", "turn about", "bent back", "to divert",
                           "to turn another way, to alter, change", "to be changed, change", "undergoing",
                           "put to flight, rout, defeat", "to be put to flight, turn and flee", "to turn away, keep off, hinder",
                           "to overturn", "to turn, apply", "have you made of"}, "ψ")],
    # EXO 16. The particle ὄφελον is ὀφείλω's "aor2 … used to express a wish … would that", and reads that
    # alone; the actives of μετρέω, πλεονάζω, διαθερμαίνω and ἀποτίθημι leave out the middle's and the
    # passive's senses, and ἀποτίθημι's middle the active's.
    # δέον: "neut. part. of the impers. δεῖ, made into a Noun, that which is binding, needful, right, proper …
    # τὰ δέοντα things needful or proper, advantages or duties": the plural of 16:22 reads the plural's, and
    # the singular the singular's.
    "de/on": [("-PIFAXY", "-AMEP", NOT_SENSES["de/on"] | {"that which is binding, needful, right, proper"}, None, "^.....P"),
              ("-PIFAXY", "-AMEP", NOT_SENSES["de/on"] | {"things needful or proper, advantages or duties"})],
    "o)fei/lw": [("-", "-", NOT_SENSES["o)fei/lw"] | {"to owe, have to pay", "account for", "to be debtor", "to be in debt",
                                                     "to be owed, to be due", "to be liable to", "to be bound, to be obliged",
                                                     "ought to have"})],
    "metre/w": [("PIFAXY", "A", NOT_SENSES["metre/w"] | {"to be measured", "to have measured out to one"})],
    # οἰκέω's passive (γῆν οἰκουμένην, 16:35) leaves out the active's intransitive "to dwell, live, be settled"
    # and "to conduct oneself".
    "oi)ke/w": [("PIFAXY", "PE", NOT_SENSES["oi)ke/w"] | {"to dwell, live, be settled", "to conduct oneself"})],
    "pleona/zw": [("PIFAXY", "A", NOT_SENSES["pleona/zw"] | {"to be exaggerated"})],
    "diaqermai/nw": [("PIFAXY", "A", {"to be heated"})],
    "a)poti/qhmi": [("PIFAXY", "A", NOT_SENSES["a)poti/qhmi"] | {"to put away from oneself, lay aside", "to avoid, escape",
                                                              "to put by for oneself, stow away", "to put off, defer"}),
                   ("PIFAXY", "M", NOT_SENSES["a)poti/qhmi"] | {"to put away, stow away"})],
    # EXO 15. δοξάζω's passive leaves out the intransitive "to hold an opinion"; καταδύω's second aorist,
    # intransitive, the causal "to make to sink … mostly in aor1" (κατέδυσαν, 15:5, is either aorist's third
    # plural, and sinks); ᾠδή's singular the plural's "lyric poetry"; σκῦλον's plural the singular's
    # "booty, spoil, prey"; ἀκοή's other cases the dative's "by hearsay". The actives of μερίζω, θραύω and
    # ἀείδω leave out the middle's and the passive's senses, and the middle of κατεργάζομαι the passive's.
    "doca/zw": [("PIFAXY", "P", NOT_SENSES["doca/zw"] | {"to hold an opinion"})],
    "katadu/w": [("A", "A", NOT_SENSES["katadu/w"] | {"to make to sink", "to cut down to the water's edge, disable"},
                  "δυ(ν|ς|μεν|τε|σαν)$")],
    # δύω: "Causal in fut. and aor1, to strip off"; the second aorist, ἔδυ, ἔδυσαν, is not causal (GEN 28:11,
    # EXO 15:10), and leaves it out.
    "du/w": [("A", "A", NOT_SENSES["du/w"] | {"to strip off"}, "δυ(ν|ς|μεν|τε|σαν)?$")],
    "w)|dh/": [("-", "-", {"lyric poetry"}, None, "^.....S")],
    # ὠδίς: "mostly in pl. the pangs or throes of labour … in sg. travail-pain, anguish … in sg., also, the
    # fruit of travail or labour, a birth, child … also in pl., of love, pangs": the plural of 15:14 leaves
    # out the singular's, and the singular the plural's.
    "w)di/s": [("-", "-", NOT_SENSES["w)di/s"] | {"travail-pain, anguish", "the fruit of travail", "labour, a birth, child"},
                None, "^.....P"),
               ("-", "-", NOT_SENSES["w)di/s"] | {"the pangs", "throes of labour, travail-pains", "pangs"})],
    "sku=lon": [("-", "-", NOT_SENSES["sku=lon"] | {"booty, spoil, prey"}, None, "^.....P")],
    "a)koh/": [("-", "-", NOT_SENSES["a)koh/"] | {"by hearsay"}, None, "^....[^D]")],
    "meri/zw": [("PIFAXY", "A", {"to divide among themselves", "to take part in", "to be divided", "to be reckoned as part"})],
    "qrau/w": [("PIFAXY", "A", {"to fly into pieces"})],
    "a)ei/dw": [("PIFAXY", "A", NOT_SENSES["a)ei/dw"] | {"to be sung"})],
    "katerga/zomai": [("PIFAXY", "M", NOT_SENSES["katerga/zomai"] | {"to be effected", "to be overcome"})],
    # διΐστημι: "Mid. and Pass., with aor2, perf., and plup. act., to stand apart, to be divided"; the
    # second aorist διέστη (15:8) is intransitive and leaves out the transitive senses and "aor1 mid. is
    # trans. to separate".
    "dii/sthmi": [("A", "A", NOT_SENSES["dii/sthmi"] | {"to set apart, to place separately, separate",
                                                        "to set one at variance with", "to divide it into fractions",
                                                        "to separate"}, "στη(?!σ)")],
    # EXO 14. ἐναντίος: "in adv. usages: neut. ἐναντίον, opposite, face to face … as prep. c. gen. in the
    # presence of, before … against … contrariwise … on the other hand", and the adverb ἐναντίως, are
    # the neuter's, which the preposition ἐναντίον reads from this card; οἱ ἐν., "one's adversaries",
    # is the masculine plural's, and "the very reverse" and "exactly opposed" examples'. The declined
    # adjective of 14:2 and 14:9, ἐξ ἐναντίας, leaves them out; "over against, opposite", which the
    # entry gives ἐξ ἐναντίας, is its second sense already.
    "e)nanti/os": [("-", "-", {"one's adversaries", "the very reverse", "opposite, face to face",
                               "in the presence of, before", "against", "contrariwise", "on the other hand",
                               "exactly opposed"}, None, "^....[NGDAV]")],
    # The active of EXO 14 takes none of the passive's or the middle's senses.
    "metastre/fw": [("PIFAXY", "P", NOT_SENSES["metastre/fw"] | {"to turn another way, change one's ways",
                                                                  "to care for, regard"})],
    "sunapa/gw": [("PIFAXY", "A", {"to be led away likewise", "to accommodate oneself to"})],
    "pari/hmi": [("PIFAXY", "A", NOT_SENSES["pari/hmi"] | {"to be relaxed, weakened, exhausted", "to obtain leave from",
                                                            "to beg to be let off", "to beg a favour"})],
    "poleme/w": [("PIFAXY", "A", NOT_SENSES["poleme/w"] | {"to have war made upon", "to be treated as enemies"})],
    "siga/w": [("PIFAXY", "A", NOT_SENSES["siga/w"] | {"to be kept silent", "to be kept secret"})],
    "summi/gnumi": [("PIFAXY", "A", NOT_SENSES["summi/gnumi"] | {"to be mingled with", "to join forces",
                                                                  "to have intercourse with"})],
    "u(pa/gw": [("PIFAXY", "A", NOT_SENSES["u(pa/gw"] | {"to bring under one's own power, reduce", "to suggest"})],
    "suntara/ssw": [("PIFAXY", "A", NOT_SENSES["suntara/ssw"] | {"to be thrown into confusion",
                                                                  "to be confounded, greatly troubled, much distressed"})],
    # τεῖχος: "pl. of a single fort, fortifications" is the plural's; the singular of 14:22 and 14:29
    # leaves it out.
    "tei=xos": [("-", "-", NOT_SENSES["tei=xos"] | {"a single fort, fortifications"}, None, "^.....S")],
    # ῥήγνυμι: the active of 14:16 leaves out "Mid. to break for oneself … to break oneself a way through"
    # and "Pass. … to break, burst … to break asunder, be rent … to burst forth … to be wrecked"; "intr.,
    # like Pass., to break forth … to break its bounds" is the active's.
    "r(h/gnumi": [("PIFAXY", "A", NOT_SENSES["r(h/gnumi"] | {"to break for oneself, get broken", "to break oneself a way through",
                                                              "to break, burst", "to break asunder, be rent", "to burst forth",
                                                              "to be wrecked"})],
    # μεταμέλει: "impers. it repents me, rues me … Mid. μεταμέλομαι, to feel repentance, to rue, regret
    # … to change one's purpose or line of conduct". EXO 13:17's μεταμελήσῃ is the impersonal active.
    "metame/lei": [("PIFAXY", "A", {"I repent of", "since it repented", "they repented that",
                                     "that which will cause regret, matter for future repentance",
                                     "to feel repentance, to rue, regret", "to change one's purpose",
                                     "line of conduct"})],
    # ὅρκος: "on oath" is the dative's, ὅρκῳ; EXO 13:19 reads it after the noun's senses.
    "o(/rkos": [("-", "-", NOT_SENSES["o(/rkos"], None, "^....D"),
                ("-", "-", NOT_SENSES["o(/rkos"] | {"on oath"})],
    # σπουδή: "σπουδῇ, as adv., in haste, hastily … with great exertion … earnestly, seriously" are the
    # dative's, and "in pl. zealous exertions … also party feelings, rivalries" the plural's: EXO 12:11's
    # μετὰ σπουδῆς reads the singular's senses, 12:33's σπουδῇ those and the dative's.
    "spoudh/": [("-", "-", {"speed", "pains", "much ado about", "with great attention to", "busily",
                            "in earnest, seriously", "zealous exertions", "party feelings, rivalries"}, None, "^....DS"),
                ("-", "-", {"speed", "pains", "much ado about", "with great attention to", "busily",
                            "in earnest, seriously", "in haste, hastily",
                            "with great exertion, with difficulty, hardly, scarcely", "earnestly, seriously, urgently"},
                 None, "^....[NGA]P"),
                ("-", "-", {"speed", "pains", "much ado about", "with great attention to", "busily",
                            "in earnest, seriously", "zealous exertions", "party feelings, rivalries", "in haste, hastily",
                            "with great exertion, with difficulty, hardly, scarcely", "earnestly, seriously, urgently"})],
    # νόμος: "dat. νόμῳ by custom, conventionally" is the dative's; EXO 12's nominatives leave it out.
    "no/mos": [("-", "-", {"custom", "law", "by the law of force, in the fight", "scuffle", "in actual warfare",
                           "to blows", "tunes"}, None, "^....D"),
               ("-", "-", {"custom", "law", "by the law of force, in the fight", "scuffle", "in actual warfare",
                           "to blows", "tunes", "by custom, conventionally"})],
    # ἀπόλλυμι: "to destroy utterly … Mid. ἀπόλλυμαι … perf. -όλωλα … to perish utterly, die". The
    # second perfect is active in form and the middle's in sense, as EXO 10:7's ἀπόλωλεν Αἴγυπτος;
    # the active's other tenses take the active's senses, and the middle's the middle's.
    "a)po/llumi": [("XY", "A", _APOLLUMI_ACT | NOT_SENSES["a)po/llumi"]),
                   ("PIFAXY", "A", _APOLLUMI_MID | NOT_SENSES["a)po/llumi"]),
                   ("PIFAXY", "MEP", _APOLLUMI_ACT | NOT_SENSES["a)po/llumi"])],
    # ἀνέχω: "trans. to hold up … intr. to rise up … Mid. to hold up what is one's own … to hold
    # oneself up, bear up, hold out … to bear up against … to suffer". GEN 45:1's ἀνέχεσθαι, to
    # bear with them all, is the middle and takes only its senses; "be of good courage" is the
    # aorist imperative's and "with patience" the participle's.
    "a)ne/xw": [("PIFAXY", "ME", {
        "to hold up", "in fight", "to lift up", "in prayer", "make ready, go on", "to lift up, exalt",
        "to uphold, maintain", "remaining constant to", "to put forth", "to hold back", "to keep",
        "to rise up, rise, emerge", "to arise, happen", "to appear, shew oneself", "to project",
        "to jut out", "to hold on, keep doing", "is constant", "to aver constantly that . .",
        "to hold up, cease", "to wait, delay", "to cease from", "get rest from", "be of good courage",
        "with patience", "I will", "suffer"})],
    # χαίρω: the imperative's greetings, the participle's "glad" and "safe, with impunity", the
    # future's "go unpunished", and the infinitive's "to dismiss from one's mind" (χαίρειν λέγειν)
    # are not senses of GEN 45:16's aorist ἐχάρη.
    "xai/rw": [("A", "P", {
        "I rejoice at", "thou wilt", "shalt not rejoice", "thou shalt", "accept the greeting",
        "taking leave", "parting", "have done with", "away with", "let", "be put aside", "may'st",
        "fare well", "with a benison", "welcome", "S. D.", "go unpunished, shalt repent",
        "hail, welcome", "fare-thee-well, farewell, good-bye", "glad, joyful, delighted",
        "safe, with impunity", "to dismiss from one's mind, put away from one, renounce"})],
    # ζεύγνυμι: "in Mid., of the husband, to wed … Pass. to be married". GEN 46:29's active
    # ζεύξας, he yoked his chariots, takes neither.
    "zeu/gnumi": [("PIFAXY", "A", {"to put to one's", "having", "fastened", "in the yoke of", "well-joined", "by bridges", "with ropes", "to wed", "to be married"})],
    # διαβοάω: "Mid. to contend in shouting" is not a sense of the passive διεβοήθη, GEN 45:16.
    "diaboa/w": [("PIFAXY", "P", {"to contend in shouting"})],
    # ἀπέχω: "Mid. … to hold oneself off a thing, abstain or desist from it". GEN 43:23's
    # active ἀπέχω, I have your money, takes none of the middle's.
    "a)pe/xw": [("PIFAXY", "A", {"part", "to hold one's", "off", "were far from", "from",
                                 "it sufficeth, it is enough", "to be as far",
                                 "to hold oneself off", "abstain", "desist from", "to abstain from"})],
    # ἐμπίπλημι: "to fill quite full … Mid. to fill for oneself … Pass. to be filled full of".
    # GEN 42:25's ἐμπλῆσαι is the active.
    "e)mpi/plhmi": [("PIFAXY", "A", {"to fill for oneself", "to be filled full of", "to take my fill of",
                                     "to sate myself with", "to be satiated", "to be filled with . .",
                                     "to eat one's fill",
                                     "what is one's own", "he filled his", "with"})],  # and examples' pieces
    # ξυρέω: "to shave … Mid. and Pass. to shave oneself or have oneself shaved". GEN 41:14's
    # active ἐξύρησαν, they shaved him, has only the first.
    "cure/w": [("PIFAXY", "A", {"to shave oneself", "have oneself shaved"})],
    # ἀναμιμνήσκω: "to remind … in Pass. to remember". The active of GEN 41:9 reminds.
    "a)namimnh/skw": [("PIFAXY", "A", {"to remember"})],
    # ἐγείρω: "Pass. … to awake … in aor2 also to keep watch or vigil … in perf. to be
    # awake". GEN 41:4's ἠγέρθη is the first aorist passive: neither the second aorist's
    # watching nor the perfect's being awake.
    "e)gei/rw": [("A", "P", {"to keep watch", "vigil", "to be awake"})],
    # ἵστημι: "Causal Tenses, to make to stand … Pass. and intr. tenses of Act. to be set or
    # placed, to stand". The causal tenses are the present, imperfect, future and first
    # aorist active, the first aorist built on στησ- as ἀνίστημι's below; the intransitive,
    # the second aorist, perfect and pluperfect. "to stand" is the headline's summary of
    # the intransitive, and section B opens with "to be set". GEN 18:2's εἱστήκεισαν had
    # read twelve senses and 12:8's ἔστησεν seven, off one card. ἔστησαν is both aorists'
    # third plural, as ἀπέστησαν is below; at GEN 43:15 it has no object and is they stood,
    # so the causal pattern leaves the third plural to the intransitive.
    "i(/sthmi": [("PIF", "A", _ISTHMI_INTR | {"to stand"}),
                 ("A", "A", _ISTHMI_INTR | {"to stand"}, "στησ(?!αν)"),
                 ("AXY", "A", {"to make to stand", "to stand", "to make to stand, set", "to set",
                               "in array, post", "to make to stand, stop, stay, check",
                               "to halt", "to fix", "to set up", "to raise", "up",
                               "to raise, rouse, stir up", "to stir up", "to set up, appoint",
                               "to establish, institute", "to place in the balance, weigh",
                               "to weigh", "against"}),
                 # EXO 33. The middle and passive are intransitive too, "Pass. and intr. tenses of Act. to be set
                 # or placed, to stand": ἵστατο, στήσῃ.
                 ("PIFAXY", "MEP", {"to make to stand", "to stand", "to make to stand, set", "to set",
                                    "in array, post", "to make to stand, stop, stay, check",
                                    "to halt", "to fix", "to set up", "to raise", "up",
                                    "to raise, rouse, stir up", "to stir up", "to set up, appoint",
                                    "to establish, institute", "to place in the balance, weigh",
                                    "to weigh", "against"})],
    # ἀφίστημι: "Causal in pres. and imperf., in fut. ἀποστήσω, aor1 ἀπέστησα", and NOT_SENSES
    # keeps the intransitive. ἀπέστησαν is both aorists' third plural; at GEN 14:4 it is
    # they revolted, so the causal pattern leaves the third plural to the intransitive.
    "a)fi/sthmi": [("PIF", "A", _APHISTHMI_INTR | {"removed", "from your own", "weighed out to one",
                                                   "to", "to have", "in full"}),
                   ("A", "A", _APHISTHMI_INTR | {"removed", "from your own", "weighed out to one",
                                                 "to", "to have", "in full"}, "στησ(?!αν)")],
    # ἐξανίστημι: "Causal in pres., imperf., fut. and aor 1 … intr. in Pass., with aor2, perf.
    # and plup. act." NOT_SENSES drops two scraps; the intransitive forms drop the causal.
    "e)cani/sthmi": [("PIF", "A", _EXANISTHMI_INTR),
                     ("A", "A", _EXANISTHMI_INTR, "στησ"),
                     ("AXY", "A", _EXANISTHMI_CAUS)],
    # γηράσκω: "Causal in aor1 ἐγήρασα, to bring to old age"; the other tenses grow old.
    "ghra/skw": [("PIFXY", "A", {"to bring to old age"})],
    # δίδωμι: "in pres. and imperf., to be ready to give, to offer" — a sense of those two
    # tenses only.
    "di/dwmi": [("AFXY", "AMPE", {"to be ready to give, to offer"})],
    # ζάω: "ζῶν, living, alive", and "of living men" — the participle's. The finite verb and
    # the infinitive leave them out.
    # ζῶσιν, the third plural, is finite: the participle's ζωσ- is the feminine (ζῶσα, ζώσης).
    "za/w": [("PIFAXY", "A", {"of living men", "living", "alive"}, "^(?!ζ[ωω](ν|σ(?!ιν?$)))")],
    # ἀνίστημι heads sense A "Causal in pres., imperf." and sense B "Intr. in pres. and
    # imperf. ἀνίσταμαι, -μην, … in aor2 ἀνέστην". NOT_SENSES keeps B, for GEN 4:8 ἀνέστη;
    # the present and imperfect active — GEN 9:9 ἀνίστημι — keep A, less its "by" (from
    # "by his hand") and the aorist middle "to build oneself".
    # The first aorist and future active are causal too, "in pres., imperf., fut., and aor1",
    # but the parse code does not tell ἀνάστησον (aor1, GEN 38:8) from ἀνέστη (aor2, 37:7),
    # so the form decides: the causal tenses are built on στησ-. ἀνέστησαν is both aorists' third plural, as ἔστησαν
    # is ἵστημι's; at EXO 32:6 it has no object and is they stood up, so the third plural is left to the intransitive.
    "a)ni/sthmi": [("PI", "A", {
        "by", "to build oneself",
        "to stand up, rise", "to rise from one's seat", "to rise from bed", "to rise from the dead",
        "to rise from", "recover", "to rise", "to stand up", "to be set up, to rise up, rear itself",
        "to rise to go, set out, go away", "to be compelled to migrate", "to be depopulated",
        "subject to migration", "to be put up"}),
                   ("AF", "A", {
        "by", "to build oneself",
        "to stand up, rise", "to rise from one's seat", "to rise from bed", "to rise from the dead",
        "to rise from", "recover", "to rise", "to stand up", "to be set up, to rise up, rear itself",
        "to rise to go, set out, go away", "to be compelled to migrate", "to be depopulated",
        "subject to migration", "to be put up"}, "στησ(?!αν)")],
    # ἐπιτίθημι heads its actives "A. Act." and its middles "B. Mid."; a middle form — GEN 9:23
    # ἐπέθεντο — takes B, whose first sense is "to put on oneself". "to give" is left out with
    # the actives: the middle's own "to give" a name would otherwise be listed in the active's
    # place, ahead of the middle's first sense.
    "e)piti/qhmi": [("PIFAXY", "M", {
        "to lay, put", "place upon", "laid on", "on", "to apply", "to set", "up", "to put on", "put",
        "as a door", "before", "to put", "to, shut", "to put to, grant", "give besides",
        "to add, bring on", "to", "to impose", "inflict", "to dispatch", "to give",
        "in", "with assiduity"})],
    # παύω opens "Causal, to make to cease", and marks its middle and passive senses "Pass. and
    # Mid.": to take one's rest, to leave off from. GEN 11:8 ἐπαύσαντο is the middle.
    # παρατάσσω's active is "to place side by side, draw up in battle-order"; its middle, "Mid.
    # to draw up one's men in battle-order", then "Mid. and Pass." senses. GEN 14:8
    # παρετάξαντο is the aorist middle.
    "parata/ssw": [("A", "M", {"to place side by side, draw up in battle-order", "in order of battle"})],
    # ἀνασῴζω's middle senses — "to recover" one from fear, "for oneself", "to preserve in mind,
    # remember" — are skipped for the aorist passive of GEN 14:13, which keeps the first sense
    # and its own "Pass. to return safe".
    "a)nasw/zw": [("A", "P", {"to recover", "for oneself", "to preserve in mind, remember"})],
    # ἐπίσταμαι: the participle "is often also used as an adj., knowing, understanding, skilful",
    # and "c. gen. skilled or versed"; the adverb is "skilfully, expertly". None is a sense of the
    # finite verb, GEN 47:5's ἐπίστῃ.
    "e)pi/stamai": [("PIFAXY", "AMPE", {"knowing, understanding, skilful", "skilled", "versed",
                                         "skilfully, expertly"}, "^(?!επισταμεν)")],
    # κτάομαι: "Dep. in pres., imperf., fut. and aor1 … in perf. and plup. … to have acquired, i. e.
    # to possess, have, hold". GEN 47:23's perfect κέκτημαι takes the perfect's senses only; the
    # participle's "an owner, master" and the aorist passive's "to be gotten" are neither.
    "kta/omai": [("XY", "AMPE", {"to procure for oneself, to get, gain, acquire", "to win",
                                 "to bring upon oneself, incur", "to make", "to procure", "get",
                                 "an owner, master", "lord and master", "to be gotten", "to get one's"})],
    # καταδουλόω: "Mid. to make a slave to oneself, to enslave". GEN 47:21's aorist middle
    # κατεδουλώσατο takes the middle's senses, not the active "to reduce to slavery, enslave".
    "katadoulo/w": [("PIFAXY", "M", {"to reduce to slavery, enslave"})],
    # προστάσσω: GEN 47:11's active προσέταξεν takes none of the passive's senses ("orders had been
    # given" … "to receive orders"); "to" is a piece of "to assign them to his command".
    "prosta/ssw": [("PIFAXY", "A", {"to", "orders had been given", "orders given", "orders that will be given",
                                    "the order having been given", "to be ordered", "to receive orders"})],
    # ἔκγονος: "as Subst. a child, whether son or daughter; and in pl. ἔκγονοι, descendants;
    # neut., ἔκγονα, one's offspring". GEN 48:6's τὰ ἔκγονα is the neuter, and the masculine's
    # child, son, daughter and descendants are not its senses.
    "e)/kgonos": [("-", "-", {"a child", "son", "daughter", "descendants"}, "^εκγονα$")],
    # βαρύς: the adverb βαρέως is filed inside the entry, and "to take a thing ill", "to hear with
    # disgust" are its; GEN 48:17's βαρύ is the adjective. Homer's "notion of strength and force"
    # is described, not translated, and "suffering" is the end of "heavy with age or suffering";
    # both are set aside for the adjective only, since GEN 31:35's βαρέως reads "with strength and
    # force".
    "baru/s": [("-", "-", {"ill", "with disgust", "strength and force", "suffering"}, "^(?!βαρεως)")],
    # ἀντιλαμβάνω: "to receive instead of … to receive in turn or as a return", then "Mid. … to lay
    # hold of". GEN 48:17's aorist middle ἀντελάβετο takes the middle's senses only.
    "a)ntilamba/nw": [("PIFAXY", "M", {"to receive instead of", "to receive in turn", "as a return"})],
    # GEN 49: an active form takes none of the passive's senses, and a middle none of the active's.
    "paratei/nw": [("PIFAXY", "A", {"to draw a long", "to be stretched along", "to be stretched at length, laid low",
                                    "to be half-dead, worn out", "to strain themselves", "hold out"})],
    "pone/w": [("PIFAXY", "A", {"were busied", "was busy", "do with pains", "care", "to labour", "do", "labour",
                                "to be worn out, spoilt", "to be worn out, to suffer greatly", "to be trained", "educated",
                                "to be won", "achieved by toil"})],
    "da/knw": [("PIFAXY", "A", {"prick", "I was stung, vexed"})],
    "e)pidi/dwmi": [("PIFAXY", "A", {"to take as witness", "let us look to"})],
    "loidore/w": [("PIFAXY", "A", NOT_SENSES["loidore/w"] | {"to rail at one another", "to rail at"}),
                  ("PIFAXY", "MEP", NOT_SENSES["loidore/w"] | {"to abuse, revile", "to rebuke"})],  # EXO 17: the middle reads the middle's
    "e)ne/xw": [("PIFAXY", "A", {"to be held, caught, entangled in", "was seized with", "to be obnoxious, liable", "subject to"})],
    "diadi/dwmi": [("PIFAXY", "A", {"around", "to be spread abroad"})],
    "e)pita/ssw": [("PIFAXY", "A", {"to", "they had", "placed next", "set as guards over", "to accept orders, submit to commands",
                                    "to be ordered", "orders given"})],
    # ἡγέομαι: "the rulers, leading men" is the participle used as a noun (οἱ ἡγούμενοι), not the
    # finite verb's; GEN 49:26's ἡγήσατο is finite.
    "h(ge/omai": [("PIFAXY", "MEP", {"to be", "leader in", "commander of", "fit, deem", "necessary", "the rulers", "leading men"},
                   "^(?!ηγουμεν)")],
    # GEN 50. θνήσκω: "to die, be dying, in aor2 and perf. to be dead": the perfect τέθνηκεν of 50:15
    # takes "to be dead" and not the present's "to die, be dying"; the rest are an example's pieces
    # and translation. The metaphorical "to die, perish", of things, is given no tense, and stays.
    "qnh/skw": [("XY", "A", {"to die, be dying", "to fall by", "hand, be slain by", "are in mortal fear of"})],
    # EXO 1. ἐφίστημι: "Causal in pres., imperf., fut., and aor1", "intr. in Mid. and Pass., …
    # with perf., plup. and aor2 act.", and "the aor1 mid. is used in causal sense, to set up, to
    # set, post". The first aorist is built on στησ-, as ἵστημι's is; ἐπέστησαν is both aorists'.
    "e)fi/sthmi": [("PIF", "A", _EPHISTHMI_INTR | _EPHISTHMI_MID | _EPHISTHMI_SCRAPS),
                   ("A", "A", _EPHISTHMI_INTR | _EPHISTHMI_MID | _EPHISTHMI_SCRAPS, "στησ(?!αν)"),
                   ("AXY", "A", _EPHISTHMI_CAUS | _EPHISTHMI_MID | _EPHISTHMI_SCRAPS)],
    # κατασοφίζομαι, "Dep. to conquer by sophisms or fallacies, to outwit … also as Pass. to be
    # outwitted": a middle form leaves out the passive.
    "katasofi/zomai": [("PIFAXY", "M", {"to be outwitted"})],
    # EXO 3. ῥέω: "Causal, in aor1 act., to let flow, pour": the present leaves it out. θλίβω's and
    # αἰτέω's actives leave out their passives' and middles' senses.
    "r(e/w": [("PIXY", "A", NOT_SENSES["r(e/w"] | {"to let flow, pour"})],
    "qli/bw": [("PIFAXY", "A", NOT_SENSES["qli/bw"] | {"to be compressed"})],
    # EXO 5. ἀπολείπω's active leaves out the middle "to leave behind one" and the passive's
    # senses; διαστρέφω's the passive's. ἀφαιρέω's passive leaves out the middle's; the present
    # ἀφαιρεῖται of Ex 5:11, which takes οὐθέν for its subject, is passive.
    "a)polei/pw": [("PIFAXY", "A", NOT_SENSES["a)polei/pw"] | {
        "to leave behind one", "to be left behind, stay behind", "to be distanced by, inferior to",
        "to be parted from, be absent", "far from", "to be deprived of", "to be wanting in, fall short of",
        "to be bereft of"})],
    "diastre/fw": [("PIFAXY", "A", {"to be distorted", "to have one's eyes distorted, to get a squint"})],
    # EXO 6. δηλόω's active leaves out the passive "to be or become manifest"; διαλέγω's deponent
    # leaves out the active "to pick out"; λυτρόω's middle, the future λυτρώσομαι, the passive.
    # ἄλογος's "brutes, animals" is τὰ ἄλογα, the neuter plural as a noun, and no other form's.
    "dhlo/w": [("PIFAXY", "A", {"to be", "become manifest"})],
    # EXO 8. καλύπτω's and ἀφανίζω's active leave out the middle and passive senses.
    "kalu/ptw": [("PIFAXY", "A", NOT_SENSES["kalu/ptw"] | {"veil oneself", "concealed in"})],
    # περιαιρέω's active leaves out the middle's and the passive's senses, the passive the active's
    # and the middle's; βαρύνω's active leaves out the passive's.
    "periaire/w": [("PIFAXY", "A", NOT_SENSES.get("periaire/w", set()) | {
                       "to take off from oneself", "to strip off, take away", "to be taken off", "to be stript of"}),
                   ("PIFAXY", "P", NOT_SENSES.get("periaire/w", set()) | {
                       "to take off something that surrounds, take off an outer coat, take away, strip off",
                       "to take off from oneself", "to strip off, take away"})],
    "baru/nw": [("PIFAXY", "A", {"he is heavy", "weary", "disabled", "to be oppressed, distressed"})],
    # EXO 9. Number: ὅρος's and χάλαζα's singular leave out the plural's senses; ῥητός's "rational
    # quantities" is τὰ ῥητά's. Voice: ὕω's, φλογίζω's and ἐκπετάννυμι's active leave out the
    # passive's; διαγγέλλω's passive the middle's; πλήσσω's passive the active's and the middle's.
    "o(/ros": [("-", "-", NOT_SENSES["o(/ros"] | {"bounds, boundaries", "marking-stones", "stone tablets", "the terms"},
                None, "^.....S")],
    "xa/laza": [("-", "-", {"a hailshower, hailstorm", "hailstones"}, None, "^.....S")],
    "r(hto/s": [("-", "-", NOT_SENSES["r(hto/s"] | {"rational quantities"}, None, "^.....(?!PN)")],
    "u(/w": [("PIFAXY", "A", NOT_SENSES["u(/w"] | {"to be rained on", "it rains"}, None, "^[12]"),
             ("PIFAXY", "A", NOT_SENSES["u(/w"] | {"to be rained on"})],
    "flogi/zw": [("PIFAXY", "A", {"to be set on fire, to blaze, flame"})],
    "e)kpeta/nnumi": [("PIFAXY", "A", {"wholly given up to"})],
    "diagge/llw": [("PIFAXY", "P", {"to pass", "from man to man, inform one another"})],
    "plh/ssw": [("PIFAXY", "P", NOT_SENSES["plh/ssw"] | {"to strike, smite", "to whip", "to strike", "amaze, confound"})],
    "a)fani/zw": [("PIFAXY", "A", NOT_SENSES["a)fani/zw"] | {"to be concealed", "suppressed",
                                                         "to become unseen, to disappear"})],
    # EXO 7. μεταβάλλω's active, but the participle, leaves out the middle's senses and the
    # participle's adverbial "instead, in turn".
    # συνίστημι's perfect active is intransitive: the transitive senses, and the participle-noun "the
    # conspirators", are left out (Ex 7:19 συνεστηκὸς ὕδωρ, water standing together). ἐπιστρέφω's
    # middle and passive take the entry's Mid. and Pass. senses, less the present participle's
    # "constantly turning" and the perfect participle's "earnest, vehement".
    "suni/sthmi": [("XY", "A", NOT_SENSES["suni/sthmi"] | {
        "to set together, combine, associate, unite, band together", "to bring", "into union with", "to win, acquire",
        "to put together, organise, frame", "to contrive", "to settle", "to bring together as friends, introduce",
        "recommend one to another", "to offer", "as a guarantee", "the conspirators"}),
                   ("A", "A", NOT_SENSES["suni/sthmi"] | {
        "to set together, combine, associate, unite, band together", "to bring", "into union with", "to win, acquire",
        "to put together, organise, frame", "to contrive", "to settle", "to bring together as friends, introduce",
        "recommend one to another", "to offer", "as a guarantee", "the conspirators", "a well-disciplined",
        "a standing"}, "^(?!.*στησ)")],
    "e)pistre/fw": [("PIFAXY", "MEP", {
        "to turn about, turn round", "to make a sudden tack", "to put", "to flight", "to return", "to turn towards",
        "to press", "to turn", "to correct, make to repent", "to repent", "to curve, twist, torment",
        "constantly turning", "earnest, vehement"})],
    "metaba/llw": [("PIFAXY", "A", NOT_SENSES["metaba/llw"] | {
        "instead, in turn", "to change what is one's own", "to change one with another, exchange",
        "to barter, traffic", "to turn oneself, turn about", "to change one's purpose, change sides", "to turn",
        "wheel about"}, None, "^...[^P]")],
    "diale/gw": [("PIFAXY", "MEP", {"to pick out one from another, to pick out"})],
    "lutro/w": [("PIFAXY", "AM", {"to be ransomed"})],
    "a)/logos": [("-", "-", NOT_SENSES["a)/logos"] | {"brutes, animals"}, None, "^.....(?!PN)")],
    # καθήκω's "in part." senses, and the attributive participle's "the regular, proper", are the
    # participle's: a finite form leaves them out (GEN 19:31 καθήκει, EXO 5:13 τὰ καθήκοντα).
    "kaqh/kw": [("PIFAXY", "A", NOT_SENSES["kaqh/kw"] | {"the regular, proper", "that which is meet, fit",
                                                       "proper, one's due", "duty",
                                                       "the present state of things, circumstances"},
                 None, "^...[^P]")],
    "a)faire/w": [("PIFAXY", "PE", NOT_SENSES["a)faire/w"] | {"to take away for oneself, take away",
                                                         "to prevent, hinder from"})],
    "ai)te/w": [("PIFAXY", "A", NOT_SENSES["ai)te/w"] | {"to ask for oneself, to claim", "to have a thing begged of",
                                                         "to be asked"})],
    # EXO 4. ἐπιλαμβάνω: "Mid., with perf. pass., to hold oneself on by, lay hold of, catch … to
    # attack … to object to": the middles of 4:4 take those, not the active's. προχειρίζω "as Dep.
    # προχειρίζομαι … to take into one's hand, prepare for oneself, to choose, elect, to determine":
    # the middle of 4:13 leaves out the active's and the passive participle's. ψῆφος: "in pl.
    # accounts", which the singular of 4:25 leaves out.
    "e)pilamba/nw": [("PIFAXY", "ME", NOT_SENSES["e)pilamba/nw"] | {
        "to lay hold of, seize, attack", "to overtake, surprise, interrupt", "to attain to, reach", "to live over",
        "to seize, stop", "to stop", "to get over"})],
    "proxeiri/zw": [("PIFAXY", "M", {"to put into the hand, have ready at hand", "taken in hand, undertaken"})],
    "yh=fos": [("-", "-", NOT_SENSES["yh=fos"] | {"accounts"}, None, "^.....S")],
    # EXO 3. προΐημι: "Mid. to send forward from oneself … to utter … to give up, let go …": the
    # future middle of 3:19 leaves out the active's and the passive's senses, and the pieces of
    # the middle's examples ("gave … up as lost", "did not lose themselves").
    "proi/hmi": [("PIFAXY", "M", {"to send before, send on", "forward", "to send", "to", "to send away, dismiss, let go",
                                  "let", "go", "to let loose, let fall", "let drop", "he let", "slip",
                                  "to send forth, shoot", "dart forth", "it pours", "to allow",
                                  "to give up, deliver over, betray", "to be given", "thrown away", "to give up",
                                  "devote", "gave", "up as lost", "did", "lose"})],
    # EXO 2. ἀναιρέω: the active "to take up, raise … to make away with, destroy, kill, … abolish",
    # and the "Mid. to take up for oneself … to gain, win … to take up in one's arms": a middle
    # (2:5, 2:10) takes the middle's, an active (2:14, 2:15) the active's; "for burial" is a piece
    # of "to take up and carry off, snatch away, esp. for burial".
    "a)naire/w": [("PIFAXY", "M", _ANAIREO_ACT | _ANAIREO_SCRAPS),
                  ("PIFAXY", "A", _ANAIREO_MID | _ANAIREO_SCRAPS)],
    # EXO 2. λούω: "Mid. and Pass. to bathe", "in strict pass. sense … to be washed": the middle
    # of 2:5 takes "to bathe" only.
    "lou/w": [("PIFAXY", "M", NOT_SENSES["lou/w"] | {"to wash", "to be washed"})],
    # τύπτω: the active's "to beat, strike, smite"; "Mid. … to mourn for", "Pass. to be beaten,
    # struck or wounded, to be stung … to receive blows".
    "tu/ptw": [("PIFAXY", "A", NOT_SENSES["tu/ptw"] | {"to mourn for", "to be beaten, struck", "wounded",
                                                       "to be stung", "to receive"})],
    # ἐκδίδωμι: "ἐκδ. θυγατέρα to give one's daughter in marriage … so in Mid.": the middle of 2:21
    # takes that sense alone.
    "e)kdi/dwmi": [("PIFAXY", "M", {"to give up, surrender", "to give up", "to give out for money, let out for hire",
                                    "to lend out money", "to empty themselves"})],
    # βία: "βίαι τινός against one's will, in spite of him", "βίαι alone as an adv., perforce" —
    # the dative's. Its periphrasis "the strength of Hercules" is an example's.
    "bi/a": [("-", "-", {"the strength", "against", "will, in spite of"}, None, "^....D"),
             ("-", "-", {"the strength", "against", "will, in spite of", "against one's will, in spite of",
                         "perforce"})],
    # τοσοῦτος: "in pl. so many" — the singular's τοσούτῳ, EXO 1:12, leaves it out.
    "tosou=tos": [("-", "-", NOT_SENSES["tosou=tos"] | {"so many"}, None, "^.....S")],
    # ταφή: "in pl. also, a burial-place": the singular of GEN 50:3 leaves it out.
    "tafh/": [("-", "-", {"the urn", "a burial-place"}, "^ταφ(η|ης|ην)$")],
    # ἐνδείκνυμι: the middle of 50:15 and 50:17 reads the Mid. senses, and "to inform against", which
    # the entry gives "so in Mid."; not the active's "to mark, point out" or the passive's participle.
    # "what is one's own" is the half of "to shew forth oneself or what is one's own", and "I will
    # declare myself" an example's.
    "e)ndei/knumi": [("PIFAXY", "M", {"to mark, point out", "being informed against for", "what is one's own",
                                      "I will declare myself"})],
    # βουλεύω: the middle of 50:20 reads sense I, "to take counsel, deliberate", which "in Prose
    # belongs chiefly to the Mid.", and the Mid. senses; not the active's "to deliberate on, plan,
    # devise" with its object, the passive's, sense II "to give counsel, advise", or the Council.
    "bouleu/w": [("PIFAXY", "M", {"in council", "we shall agree", "to deliberate on, plan, devise", "to be determined",
                                  "resolved on", "to give counsel", "to advise", "to be a member of Council",
                                  "of the Council of"})],
    "pau/w": [("PIFAXY", "MEP", {
        "to make to cease", "to bring to an end, check, make an end of", "to make an end of, stop, abate",
        "to let", "rest", "to annul", "to put", "down", "to make to rest, stop, hinder, keep back from",
        "to depose", "from", "would make an end of", "to stop", "doing", "being", "from being",
        "cease, leave off"})],
}
# The key the lexicon files a word under, where that is not the key the lemma itself
# gives: a different spelling (Attic γίγνομαι for Koine γίνομαι), the active a deponent
# is filed beneath (πορεύω for πορεύομαι), or the entry a bare cross-reference points at
# (κατέναντι reads "= κατεναντίον" and glosses nothing itself). Each is recorded in
# reference/lexicon-notes.md with the entry it resolves to.
SPELLING = {
    "e(kousi/ws": "e(kou/sios",       # the adverb, "adv. -ίως", inside the adjective's entry (EXO 36:2)
    "skopeu/w": "skope/w",           # σκοπεύω, "later form for σκοπέω" (EXO 33:8)
    "oi)kti/rw": "oi)ktei/rw",       # οἰκτίρω, "late form of οἰκτείρω" (EXO 33:19)
    "linou=s": "li/neos",            # the contracted adjective, filed under the uncontracted, as χαλκοῦς (EXO 28:42)
    "a)/nqinos": "a)nqino/s",         # the entry accented ἀνθινός (EXO 28:34)
    "topa/zion": "to/pazos",         # τοπάζιον, which LSJ files under τόπαζος, "also … τοπάζιον, LXX Ex. 28.17" (EXO 28:17)
    "e(kato/ntarxos": "e(katonta/rxhs",  # ἑκατόνταρχος, Middle Liddell's ἑκατοντάρχης, "leader of a hundred" (EXO 18:21)
    "kri/ma": "kri=ma",               # κρίμα, the entry headed with the circumflex (EXO 18:22)
    "e)gxeiri/dion": "e)gxeiri/dios",  # "as Subst., ἐγχειρίδιον … a hand-knife, dagger", inside the adjective (EXO 20:25)
    "dou/lh": "dou=los",              # "Hom. has only the fem. δούλη, a bondwoman", inside δοῦλος (EXO 21:7)
    "kakw=s": "kako/s",               # the adverb, filed inside the adjective's entry, as καλῶς (EXO 22:27)
    "sfhki/a": "sfhkia/",          # σφηκία, the entry accented σφηκιά, whose LSJ cites Ex 23:28 (EXO 23:28)
    "a)naginw/skw": "a)nagignw/skw", # the entry is headed with the Attic spelling, ἀναγιγνώσκω (EXO 24:7)
    "i(lasth/rion": "i(lasth/rios",   # "as Subst., ἱλαστήριον, the mercy-seat", inside the adjective (EXO 25:17)
    "palaisth/s": "palasth/",        # LSJ's παλαιστής (B), "v. παλαστή"; Middle Liddell's παλαιστής is a wrestler (EXO 25:25)
    "xalkou=s": "xa/lkeos",          # the contracted adjective, filed under the uncontracted, as χρυσοῦς (EXO 26:11)
    "di/yos": "di/ya",                # δίψος, "= δίψα", and nothing more (EXO 17:3)
    "ko/rion": "kori/annon",          # LSJ's κόριον (B), "shortd. for κορίαννον"; Middle Liddell's κόριον is the diminutive of κόρη (EXO 16:14)
    "sa/bbaton": "*sa/bbaton",        # σάββατον, keyed with the capital (EXO 16:23)
    "sabbati/zw": "*sabbati/zw",      # σαββατίζω, keyed with the capital (EXO 16:30)
    "o)/felon": "o)fei/lw",           # the particle ὄφελον, ὀφείλω's "aor2 ὤφελον, ὄφελον … to express a wish" (EXO 16:3)
    "profh=tis": "profh/ths",         # προφῆτις, "fem. of προφήτης", and nothing more (EXO 15:20)
    "dii+/sthmi": "dii/sthmi",        # διΐστημι, keyed without the diaeresis (EXO 15:8)
    "a)/|dw": "a)ei/dw",               # ᾄδω, the Attic contraction of ἀείδω (EXO 15:1)
    "e(/toimos": "e(toi=mos",          # ἕτοιμος, the entry headed with the circumflex (EXO 15:17)
    "e)ndo/cws": "e)/ndocos",          # the adverb, named inside the adjective's entry, "adv. -ως" (EXO 15:1)
    "a)poliqo/w": "a)poliqo/omai",     # the passive the text uses, "Pass. to become stone" (EXO 15:16)
    "stratia/": "strati/a",            # στρατιά, Middle Liddell's στρατία, "= στρατός, an army" (EXO 14:4)
    "perizw/nnumi": "perizw/nnumai",   # the middle, "with perf. pass. -έζωσμαι", the voice the text uses (EXO 12:11)
    "o)leqreu/w": "o)loqreu/w",        # ὀλεθρεύω, Middle Liddell's ὀλοθρεύω (EXO 12:23)
    "gno/fos": "dno/fos",              # γνόφος, Middle Liddell's "= δνόφος" (EXO 10:22)
    "katagi/nomai": "katagi/gnomai",   # the Attic spelling, as γίνομαι (EXO 10:23)
    "o)lu/ra": "o)/lura",               # ὀλύρα, Middle Liddell's ὄλυρα (EXO 9:32)
    "kuno/muia": "kuna/muia",          # κυνόμυια, Middle Liddell's "= κυνάμυια" (EXO 8:17)
    "skni/y": "kni/y",                  # σκνίψ, Middle Liddell's κνίψ, "like σκνίψ" (EXO 8:12)
    "e)paoido/s": "e)pw|do/s",          # ἐπαοιδός, the uncontracted ἐπῳδός, LSJ's "= ἐπῳδός" (EXO 7:11)
    # Close forms of the same word, under which Middle Liddell files it. A close form
    # counts only where it covers the form the text uses — not a compound under its
    # simplex, nor a verb under its noun, which would be composing rather than reading.
    "poimh/n": "poimh/",            # the entry is ποιμήν; Perseus truncates its key
    "katanu/ssw": "katanu/ssomai",  # the passive the text uses, filed as κατανύσσομαι
    "xei/marros": "xeima/rrous",    # the contracted χείμαρρους of the same adjective
    "di/draxmon": "di/draxmos",     # "as Subst. δίδραχμον, a double-drachm"
    "o(/los": "ou)=los1",           # "ionic form of ὅλος, whole, entire"; no ὅλος of its own
    "krufh=|": "kru/bdhn",          # κρυφῆ reads "= κρύβδην" and glosses nothing itself
    "ai)xmalwti/s": "ai)xma/lwtos",  # "fem. of αἰχμάλωτος", and nothing more
    "a)rh/n": "a)rno/s",            # the lamb, filed under its genitive ἀρνός
    "e)/kgonon": "e)/kgonos",       # "neut., ἔκγονα, one's offspring", of the same adjective
    "nw=tos": "nw=ton",             # the back: νῶτος, MorphGNT's form, is νῶτον in the masculine
    "prwino/s": "prw/ios",          # "later form of πρώιος", and nothing more
    "e)cai/retos": "e)caireto/s",   # "ἐξαίρετος, ον, taken out", printed inside ἐξαιρετός's entry
    "katalimpa/nw": "katalei/pw",   # "= καταλείπω", and nothing more
    "xro/a": "xroia/",              # χρόα, LSJ's "v. χροιά": Middle Liddell spells it χροιά
    "proi+/hmi": "proi/hmi",            # προΐημι, keyed without the diaeresis
    "a(/lwn": "a(/lws",             # "= ἅλως found in the obl. cases", and nothing more
    "kopeto/s": "kommo/s",          # "= κομμός", and nothing more
    "e)/sw": "ei)/sw",              # "older form of εἴσω"; its one translation is of the
                                    # comparative ἐσωτέρω, "to the interior" of Greece
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
    "e)coleqreu/w": "e)coloqreu/w",  # the spelling the text prints; Middle Liddell heads the other
    "a)rseniko/s": "a)rreniko/s",    # the less Attic form, as LSJ calls it
    "e)/xqra": "e)/xqrh",           # the entry is headed with the Ionic spelling
    "deilino/s": "deielino/s",      # cross-reference; "contr. for δειελινός" glosses nothing
    "o)rqw=s": "o)rqo/s",           # the adverb, filed inside the adjective's entry
    "e)nnako/sioi": "e)nako/sioi",  # the later spelling; the entry is headed with the earlier
    "e)kle/gomai": "e)kle/gw",      # MorphGNT's middle, filed under the active
    "ei)sporeu/omai": "ei)sporeu/w",  # likewise
    "qumo/omai": "qumo/w",          # likewise
    "e)pispa/omai": "e)pispa/w",    # likewise (1 Cor 7:18)
    "e)pimelw=s": "e)pimelh/s",     # the adverb, filed inside the adjective's entry
    "a)sfalw=s": "a)sfalh/s",       # likewise, and the entry glosses it "in all senses of the adj."
    "sklhrw=s": "sklhro/s",         # the adverb, filed inside the adjective's entry
    "e)nanti/on": "e)nanti/os",     # cross-reference; "adverb v. ἐναντίος" glosses nothing
    "nossia/": "neossia/",          # the contracted spelling; the entry is headed with νεοσσιά
    "kata/gaios": "kata/geios",     # cross-reference; "ionic for κατάγειος" glosses nothing
    # The month. Middle Liddell's μήν is the particle, "verily"; it files the month under the
    # nominative μείς. When the particle appears it will need its own way in.
    "mh/n": "mei/s",
    "a)noi/gw": "a)noi/gnumi",     # the -νυμι form heads the entry
    "sfodrw=s": "sfodro/s",        # the adverb, filed inside the adjective's entry
    "mimnh/skomai": "mimnh/skw",    # MorphGNT's middle, filed under the active
    "cura/w": "cure/w",             # the -άω spelling of the same verb; the entry is ξυρέω
    "ma/rsippos": "ma/rsipos",      # the spelling Rahlfs prints; Middle Liddell heads μάρσιπος
    "pentaplasi/ws": "pentapla/sios",  # the adverb; LSJ files it inside the adjective, "Adv.
                                        # -ως LXX Ge. 43.34", and Middle Liddell has the adjective
    "a)ggei=on": "a)/ggos",          # cross-reference; the entry reads "ἄγγος" and glosses nothing
    "nh/": "nai/",                  # "Particle of strong affirmation, like epic ναί": no translation
                                    # of its own, and the Attic form of the particle it names
    "diati/qemai": "diati/qhmi",    # likewise
    "kunhgo/s": "kunago/s",         # the entry is headed with the Doric and Attic κυναγός
    "plhsi/on": "plhsi/os",         # the adverb, filed inside the adjective's entry
    "e)nw/pion": "e)nw/pios",       # likewise
    "kaqa/per": "kaqa/",            # filed inside the entry for καθά
    "e)/rhmos": "e)rh=mos",         # the entry is headed with the Attic accent, ἐρῆμος
    "peripoie/omai": "peripoie/w",  # MorphGNT's middle, filed under the active
    "e)neuloge/w": "e)neuloge/omai",  # the entry is headed with the passive
    "borra=s": "*bore/as",          # the contracted Attic form, filed under Βορέας
    "tere/minqos": "te/rminqos",    # the spelling Rahlfs prints; the entry is headed τέρμινθος
    "paragi/nomai": "paragi/gnomai",  # the Attic spelling
    "deka/th": "de/katos",          # cross-reference; "v. δέκατος II." glosses nothing
    "e)peidh/": "e)pei/",            # not in Middle Liddell; LSJ's ἐπειδή reads "v. ἐπεί"
    "kli/banos": "kri/banos",       # the entry is headed with the Attic κρίβανος
    "kuri/a": "ku/rios2",           # cross-reference; "fem. of κύριος signf. B. 1. 2." — the noun's κυρία, mistress
    "a)/ra": "a(/ra",               # Perseus keys ἄρα with a rough breathing
    "a)=ra": "a(/ra",               # "in accent and sense a stronger form of ἄρα"; the entry glosses nothing
    "a)lhqw=s": "a)lhqh/s",         # the adverb, filed inside the adjective's entry
    "ou)xi/": "ou)",                # the strengthened οὐ, filed in its entry
    "mhdamw=s": "mhdamh=",          # cross-reference; "adverb of μηδαμός = μηδαμῇ"
    "ei(/neka": "e(/neka",          # the Ionic and poetic form, filed under ἕνεκα
    "ni/ptw": "ni/zw",              # the late present, filed under νίζω
    "a)pokri/nomai": "a)pokri/nw",  # MorphGNT's middle, filed under the active
    "presbu/teros": "pre/sbus",     # the comparative, filed inside the positive's entry
    "e)kkre/mamai": "e)kkrema/nnumi",  # the passive, filed at the end of the active's entry
    "a(/maca": "a)/maca",            # Perseus keys ἅμαξα with the smooth breathing
    "o)rqri/zw": "o)rqreu/w",       # cross-reference; "= ὀρθρεύω"
    "platei=a": "platu/s",          # the feminine used as a noun, filed inside the adjective's entry
    "suggi/nomai": "suggi/gnomai",  # the Attic spelling
    "sw/|zw": "sw/zw",              # the entry is headed without the iota subscript
    "diasw/|zw": "diasw/zw",        # likewise
    "de/omai": "de/w2",             # the deponent, filed under δέω, to lack; de/w1 is to bind
    "prwi+/": "prwi/",              # the entry is headed without the diaeresis
    "ma=llon": "ma/la",             # the comparative, filed inside the positive's entry
    "a)tmi/s": "a)tmo/s",           # cross-reference; "= ἀτμός"
    "e)xqe/s": "xqe/s",             # cross-reference; "v. χθές"
    "e)piske/ptomai": "e)piskope/w",  # "a pres., which furnishes its tenses to ἐπισκοπέω"
    "pallakh/": "pallaki/s",        # cross-reference; "= παλλακίς"
    "diplou=s": "diplo/os",         # the contracted form, filed under the uncontracted
    "ku/klw|": "ku/klos",           # the adverbial dative, filed inside κύκλος
    "qe/lw": "e)qe/lw",             # the later form, filed under ἐθέλω
    "xrusou=s": "xru/seos",         # the contracted form, filed under the uncontracted
    "a)rgurou=s": "a)rgu/reos",     # likewise
    "qe/ristron": "qeri/strion",    # "so θέριστρον", inside θερίστριον
    "e)pilamba/nomai": "e)pilamba/nw",  # MorphGNT's middle, filed under the active
    "presbu/ths": "pre/sbus",       # cross-reference; "= πρέσβυς I"
    "e(/yema": "e(/yhma",           # LSJ: "late form of ἕψημα"
    "kalw=s": "kalo/s",             # the adverb, filed inside the adjective's entry
    "e)xqri/a": "e)/xqrh",          # LSJ: "late form of ἔχθρα", whose entry is headed ἔχθρη
    "taxu/": "taxu/s",              # the adverb, filed inside the adjective's entry
    "dikai/ws": "di/kaios",         # likewise
    "e)ndelexw=s": "e)ndelexh/s",    # the adverb, "adv. -χῶς", inside the adjective's entry (EXO 29:38)
    "kaqarismo/s": "kaqarmo/s",     # "later form for καθαρμός" (EXO 29:36)
    "i)=ris": "*)=iris",             # the appellative ἶρις, "as Appellat. ἶρις", inside the goddess's entry (EXO 30:24)
    "e)piginw/skw": "e)pigignw/skw",  # the Attic spelling of a Koine form, as γινώσκω
    "zugo/s": "zugo/n",             # the entry is headed with the neuter
    "kli/mac": "kli=mac",           # the entry is headed with the circumflex
    "e)cai/rw": "e)caei/rw",       # the entry is headed with the Epic ἐξαείρω
    "dwrea/n": "dwrea/",           # the adverb, filed inside the noun's entry
    "ou)qei/s": "ou)dei/s",        # the later spelling, filed under οὐδείς
    "bare/ws": "baru/s",           # the adverb, filed inside the adjective's entry
    "a)fro/nws": "a)/frwn",        # the adverb, which the entry glosses "senselessly"
    "e)comologe/w": "e)comologe/omai",  # the entry is headed with the deponent middle
    "a(/|dhs": "*(/a|dhs",          # one entry, keyed with the god's capital; "as appellative,
                                    # Hades, the world below", the use εἰς ᾅδου is
}

# Homographs where Perseus's *first* entry is a different word from the one the text
# uses, so the first sense of the first entry would be the first sense of the wrong
# word. This says which entry is the word; the lexicon still says what it means, and
# the reason for each is recorded in reference/lexicon-notes.md. Keep it short: a
# lemma belongs here only when the entries are genuinely different words.
ENTRY = {
    "ne/w": "ne/w2",     # ne/w1 is "to swim", ne/w3 "to heap"; EXO 26:31's νενησμένης is spun (ne/w2)
    "xou=s": "xou=s2",   # xou=s1 is the Pitcher-feast, the liquid measure; GEN 2:7 is dust
    "o(/ti": "o(/ti2",   # o(/ti1 is ὅ τι, "for what"; the conjunction is the second entry
    "le/gw": "le/gw3",   # le/gw1 is "to lull to sleep", le/gw2 "to gather"; saying is the third
    "eu)qu/s": "eu)qu/s2",  # eu)qu/s1 is the adjective, "straight"; the adverb, "straightway", is the second
    "ou)": "ou)8",       # of eighteen entries, all but this one gloss an idiom (ou) ga/r,
                         # ou) mh/n …); ou)8 is the plain negative, "not", Lat. non
    "o(do/s": "o(do/s2",  # o(do/s1 is the attic ὀδός for οὐδός, "a threshold"; GEN 3:24 is the way
    "stei=ra": "stei=ra2",  # stei=ra1 is a ship's keel; the barren woman of GEN 11:30 is the second
    "mo/sxos": "mo/sxos2",  # mo/sxos1 is a young shoot; the calf of GEN 12:16 is the second
    "mh=lon": "mh=lon2",  # mh=lon1 is a sheep or goat; the mandrake fruit of GEN 30:14 is the apple
    "nu=n": "nu=n1",     # nu=n2 is νῦν δή, "just now"; νῦν itself is the first entry
    "e(/lic": "e(/lic2",  # e(/lic1 is the adjective, "twisted"; the vine's tendril of GEN 49:11 is the noun
    "pw=s": "pw=s2",     # pw=s1 is Aristotle's unaccented-sense πῶς, "in a certain way"; the
                         # interrogative, "how?", is the second
    "a)/nw": "a)/nw2",
    "a)/peimi": "a)/peimi2",  # a)/peimi1 is "to be away"; EXO 33:8's ἀπιόντος, of εἶμι, is "to go away"   # a)/nw1 is the verb, "to accomplish"; the adverb of EXO 20:4, "up", is the second
}

PUNCT = re.compile(r"[.,;:·!?—·()]")


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
DEGREE = {"C": "comparative", "S": "superlative"}

# CLAUDE.md fixes the wording for aorist, imperfect and perfect; the other two follow it.
ASPECT = {
    "aorist": "one completed act seen whole, not a process observed in progress",
    "imperfect": "was, and kept on being: action going on in past time",
    "present": "going on, in progress",
    "perfect": "a standing resultant state, not a past event",
    "pluperfect": "a resultant state that stood in the past",
}
SHARED_VOICE = {"present", "imperfect", "perfect", "pluperfect"}


def describe(pos, tense="", voice="", mood="", person="", case="", number="", gender="",
             degree=""):
    t, v = TENSE.get(tense, ""), VOICE.get(voice, "")
    if v in ("middle", "passive") and t in SHARED_VOICE:
        v = "middle/passive"
    parts = [POS.get(pos, pos)] + [x for x in (
        t, v, MOOD.get(mood, ""), PERSON.get(person, ""),
        CASE.get(case, ""), NUMBER.get(number, ""), GENDER.get(gender, ""),
        DEGREE.get(degree, "")) if x]
    return " · ".join(parts), (ASPECT.get(t, "") if pos == "V" else "")


def morphgnt(pos, code):
    """MorphGNT: a two-letter part of speech and an eight-place parse —
    person, tense, voice, mood, case, number, gender, degree."""
    f = ["" if c == "-" else c for c in code.ljust(8, "-")]
    return describe(pos.rstrip("-"), tense=f[1], voice=f[2], mood=f[3], person=f[0],
                    case=f[4], number=f[5], gender=f[6], degree=f[7])


# --------------------------------------------------------------------------
# the lexicon
# --------------------------------------------------------------------------

BETA_LETTERS = dict(zip("αβγδεζηθικλμνξοπρστυφχψως", "abgdezhqiklmncoprstufxyws"))
BETA_MARKS = {"̓": ")", "̔": "(", "́": "/", "̀": "\\", "͂": "=",
              "ͅ": "|", "̈": "+"}


def _no_repeated_keys():
    """A dict literal keeps only the last of a repeated key, so a second entry for a lemma
    silently kills the first and its scraps come back into every chapter built afterwards.
    That went unseen across seventeen NOT_SENSES lemmas, because the chapters already built
    were never rebuilt. Read this file's own source and refuse to load with a repeat in it."""
    import ast
    tree = ast.parse(pathlib.Path(__file__).read_text(encoding="utf-8"))
    for node in tree.body:
        if not isinstance(node, ast.Assign) or not isinstance(node.value, ast.Dict):
            continue
        name = getattr(node.targets[0], "id", "?")
        seen = {}
        for k in node.value.keys:
            if not isinstance(k, ast.Constant) or not isinstance(k.value, str):
                continue
            if k.value in seen:
                raise AssertionError(
                    "%s repeats %r at lines %d and %d — merge them into one entry, or the "
                    "earlier one does nothing" % (name, k.value, seen[k.value], k.lineno))
            seen[k.value] = k.lineno


_no_repeated_keys()


def beta(word):
    """Unicode Greek -> the Beta Code the lexicon is keyed by (πνεῦμα -> pneu=ma)."""
    out = []
    for c in unicodedata.normalize("NFD", word.lower()):
        out.append(BETA_LETTERS.get(c) or BETA_MARKS.get(c, ""))
    return "".join(out)


# Translations the markup loses. Perseus tags each translation <tr>, and the loader
# reads those; where a translation is swallowed by the element beside it, it never
# reaches the senses at all, though it stands in the printed entry. Each line quotes
# the entry and says which element took it, and is recorded in lexicon-notes.md.
# This adds nothing the lexicon does not say — it recovers what the encoding dropped.
MARKUP_LOST = {
    # εἰ reads "a Conditional Conjunction, Lat. si, if; and in indirect questions,
    # whether." <foreign lang="la"> holds "si, if", so the English "if" is inside the
    # Latin and only "whether." is a <tr>. Without this εἰ heads as `whether` and the
    # conditional, which is what εἰ is in every one of its Genesis occurrences, is
    # nowhere in the chain.
    "ei)1": [(0, "if")],
    # The same fault, found by looking for a comma inside a <foreign lang="la">: Middle
    # Liddell writes "Lat. <latin>, <English>" and Perseus wraps the whole run, English
    # and all, in the Latin element. Each line quotes the entry. Nineteen of these lost
    # a translation the printed page gives, and five of them lost the word's own first
    # sense, so the headword had come from somewhere further down the entry.
    "bou=s": [(0, "a bullock, bull, ox")],       # "Lat. bos (bov-is), a bullock, bull, ox, or a cow"
    "o)dou/s": [(0, "a tooth")],                 # "Lat. dens, dentis, a tooth"
    "le/wn": [(0, "a lion")],                   # "Lat. leo, a lion"
    "lu/kos": [(0, "a wolf")],                  # "Lat. lupus, a wolf"
    # "like Lat. planctus (from plango), a beating of the breast in lamentation": the <tr> opens
    # inside the Latin parenthesis and carries "plango)," with it.
    "kommo/s1": [(1, "a beating of the breast in lamentation")],
    # "of the town: hence, like Lat. urbanus, town-bred, polite, courteous": the Latin element holds
    # the English after it.
    "a)stei=os": [(1, "town-bred, polite, courteous")],
    # "a training- master": the <tr>s stop either side of "training-", and "a" and "master" reach
    # the card apart.
    "e)pista/ths": [(10, "a training-master")],
    # "Mid. … to hold oneself on by, lay hold of, catch": "on" stands between two <tr>s.
    "e)pilamba/nw": [(10, "to hold oneself on by, lay hold of, catch")],
    # EXO 5. Translations a word outside the <tr> cuts: "«to leave» one «in the lurch»", "to have
    # rest or «respite from» a thing", "to have leisure or «opportunity for» a thing", "«to have»
    # it «taken from one»". The pieces are in NOT_SENSES.
    # EXO 8. κνίψ: "a small «insect which gnaws» figs".
    "kni/y": [(0, "a small insect which gnaws figs")],
    # EXO 14. παρίημι: "to let drop beside or «at the side, let fall»"; σιγάω: "to be silent or «still, to keep
    # silence»", and "Pass. to be kept silent or «secret»"; συμμίγνυμι: "«to make» him «acquainted with»
    # fortune"; ὑπάγω: "«to bring» a person «before the judgment-seat»"; ἐπαναστρέφω: "«to turn back upon»
    # one". The verb, or its object, stands outside the <tr>.
    "pari/hmi": [(1, "to let drop at the side, let fall")],
    "siga/w": [(1, "to be still, to keep silence"), (7, "to be kept secret")],
    "summi/gnumi": [(11, "to make acquainted with")],
    "u(pa/gw": [(6, "to bring before the judgment-seat")],
    "e)panastre/fw": [(0, "to turn back upon one")],
    "e)/ndocos": [(0, "held in esteem or honour, of high repute")],  # «held in esteem» or «honour, of high repute» (EXO 15:1)
    # EXO 15. καταδύω: "«to cut» it «down to the water's edge, disable» it"; τήκω: "«to cause to waste» or
    # «pine away»"; διΐστημι: "«to set» one «at variance with» another", "«to divide» it «into fractions»",
    # "«to stand at certain distances» or «intervals»".
    "katadu/w": [(11, "to cut down to the water's edge, disable")],
    "du/w2": [(14, "to enter, come over or upon")],  # «to enter, come over» or «upon»
    # EXO 16. πάγος: "«that which is fixed» or «firmly set»"; πλεονάζω: "«to go beyond bounds, take» or «claim
    # too much»"; πικραίνω: "«to make sharp» or «bitter» to the taste".
    "pa/gos": [(0, "that which is fixed or firmly set")],
    # EXO 17. πέτρα: "«a rock, a ledge» or «shelf of rock» … «a rocky peak» or
    # «ridge»"; στηρίζω: "«to be firmly set» or «fixed, to stand fast» or «steady»"; καταγράφω: "«to fill» tablets
    # «with writing»".
    "pe/tra": [(0, "a rock, a ledge or shelf of rock"), (4, "a rocky peak or ridge")],
    "sthri/zw": [(7, "to be firmly set or fixed, to stand fast or steady")],
    "katagra/fw": [(3, "to fill with writing")],
    # EXO 18. σημαίνω: "«to give a sign» or «signal to do» a thing", "«to stamp with a sign» or «mark, to seal»";
    # ὑπερηφανία: "«contempt towards» or «for» another"; ἐλαφρός: "= Lat. lev-is light in weight", the first
    # sense, outside any <tr>.
    "shmai/nw": [(2, "to give a sign or signal to do"), (16, "to stamp with a sign or mark, to seal")],
    "u(perhfani/a": [(1, "contempt towards or for")],
    "e)lafro/s": [(0, "light in weight")],
    # EXO 19. βιάζω: "βιάζεσθαι νόμους «to do» them «violence»"; προσάγω: "πάντων πρ. ὄμματα «to draw» all eyes
    # «upon oneself»"; πτέρυξ: "«anything that covers» or «protects» like wings"; ἠχέω: "ἀχεῖν ὕμνον «to let» it
    # «sound»". Each the word's own English in that use, with its object between (open question Q7's test).
    "bia/zw": [(7, "to do them violence")],
    "prosa/gw": [(25, "to draw all eyes upon oneself")],
    "pte/ruc": [(6, "anything that covers or protects")],
    "h)xe/w": [(2, "to let it sound")],
    # EXO 21. συνεισέρχομαι: "«to enter along with» or «together»"; κριτήριον: "«a means for judging» or «trying,
    # a criterion, standard, test»"; τρυπάω: "«to force» the point «through» the foot"; ἀθετέω: "«refuse» his
    # «request»"; ζημιόω: "μεγάλα ζημιώσεται «will suffer» great «losses»", "«to be fined» or «amerced in»".
    "suneise/rxomai": [(0, "to enter along with or together")],
    "krith/rion": [(0, "a means for judging or trying, a criterion, standard, test")],
    "trupa/w": [(4, "to force the point through")],
    "a)qete/w": [(2, "refuse his request")],
    "zhmio/w": [(2, "will suffer great losses"), (6, "to be fined or amerced in")],
    "pugmh/": [(4, "the distance from the elbow to the knuckles")],  # the <tr> runs on into the equation "= 18 δάκτυλοι"
    # EXO 22. ἀπορρίπτω: "of words, «to shoot forth bold, keen» words"; καταβόσκω: "«to feed flocks upon» or «in» a
    # place"; ἁλίσκομαι: "«to be caught» or «detected» doing a thing".
    "a)porri/ptw": [(5, "to shoot forth bold, keen words")],
    "katabo/skw": [(0, "to feed flocks upon or in")],
    "a(li/skomai": [(6, "to be caught or detected")],
    # ὀρφανός: "Lat. orbus, orphan, without parents, fatherless" — the first sense, all inside the Latin element.
    "o)rfano/s": [(0, "orphan, without parents, fatherless")],
    # EXO 23. συγκατατίθημι: "«to deposit together» or «at the same time»"; λυμαίνομαι: "«to inflict indignities» or
    # «outrages upon»"; πτωχός: "«one who crouches» or «cringes, a beggar»"; ἀναψύχω: "ναῦς ἀν. «to let» the ships «rest
    # and get dry, relieve» them", "«to let» it «dry off»", "«to give» him «relief from» toil"; ὑποστέλλω: "«made» him
    # «furl» his sail", "«to shelter» oneself «behind»", "«to cloak» a thing «through fear, to prevaricate, dissemble»".
    # The ships and the thing are the examples' objects, left out as ὑπάγω's "a person" is; the pronouns stay.
    "sugkatati/qhmi": [(0, "to deposit together or at the same time")],
    "lumai/nomai": [(3, "to inflict indignities or outrages upon")],
    "ptwxo/s": [(0, "one who crouches or cringes, a beggar")],
    "a)nayu/xw": [(2, "to let rest and get dry, relieve"), (5, "to let it dry off"), (8, "to give him relief from")],
    "u(poste/llw": [(1, "made him furl"), (5, "to shelter oneself behind"), (9, "to cloak through fear, to prevaricate, dissemble")],
    # δικαιόω: "«to hold» or «deem right, think fit, demand»", "«to do a man right» or «justice, to judge»";
    # ἐξίστημι: "ἐξιστάναι τινὰ φρενῶν «to drive» one «out of» his senses"; συναγωγή: "σ. στρατιᾶς «a forming» an
    # army «in column»", the army the example's object, left out as ὑπάγω's "a person" is.
    "dikaio/w": [(2, "to hold or deem right, think fit, demand"), (8, "to do a man right or justice, to judge")],
    "e)ci/sthmi": [(2, "to drive one out of")],
    "sunagwgh/": [(5, "a forming in column")],
    # ἐλαιών: "«an olive-yard», Lat. olivetum: the Mount of Olives, Olivet, NTest." — the English after the colon inside
    # the Latin element.
    "e)laiw/n": [(1, "the Mount of Olives, Olivet")],
    # EXO 24. γράφω: "γρ. τινά «to write» a person's «name»", "Mid. «to write for oneself» or «for one's own use, note
    # down»"; ἀναγιγνώσκω: "«to know» them «again»"; προσχέω: "«to pour to» or «on»"; νομοθετέω: "«it hath been» so
    # «ordained by law»", the so left out; κατασκεδάννυμι: "«to scatter», or «pour upon» or «over»", "«to spread» a
    # report «against» one", the report the example's object, "Mid. «to pour» or «sprinkle about»"; φλέγω: "«making» it
    # «blaze» or «flash»", "«letting» the flame of mischief «blaze up»", the flame the example's object, "«to make
    # illustrious» or «famous»", "Pass. «to be» or «become so»".
    "gra/fw": [(4, "to write a person's name"), (14, "to write for oneself or for one's own use, note down")],
    "a)nagignw/skw": [(2, "to know them again")],
    "prosxe/w": [(0, "to pour to or on")],
    "nomoqete/w": [(3, "it hath been ordained by law")],
    "kataskeda/nnumi": [(1, "pour upon or over"), (4, "to spread against"), (7, "to pour or sprinkle about")],
    "fle/gw": [(4, "making it blaze or flash"), (8, "letting blaze up"), (12, "to make illustrious or famous"),
               (15, "to be or become so")],
    # EXO 25. αἴγειος: "«of a goat» or «goats»"; στρεπτός: "«a collar of twisted» or «linked metal»", "«to be bent» or
    # «turned»", "«a glib, pliant» tongue", the a the tongue's; τράπεζα: "prob. for τετράπεζα «four-legged a table»",
    # where the <tr> took in τετράπεζα's gloss; συσκιάζω: "«to shade quite over, throw a shade over, shade closely» or
    # «thickly»"; ἀκίνητος: "«not to be stirred» or «touched, inviolate»"; τύπος: "«the sound of» their «tread»",
    # "«anything wrought of metal» or «stone»"; ἐλαύνω: "«to drive» to extremities", "«to drive» or «thrust» through",
    # "«to beat with» a hammer", "«to draw a line of» wall or a trench", "«plant» them «in line»".
    "ai)/geios": [(0, "of a goat or goats")],
    "fai/nw": [(4, "to make it clear"), (11, "to inform of as contraband")],
    # EXO 26. ἔνθεν: "of Place, Lat. inde, thence", "Lat. unde, whence, from which", the English inside the Latin
    # element; συνάπτω: "«to bind» it «fast»", "«to connect» it «with» him, «refer» it «to» him"; διορίζω: "«to
    # determine» one «to be» so and so".
    "e)/nqen": [(0, "thence"), (7, "whence, from which")],
    "suna/ptw": [(2, "to bind it fast"), (14, "to connect it with"), (17, "refer it to")],
    "diori/zw": [(3, "to determine one to be")],  # "«to make» it «clear» to the ear"; "«to inform of» a thing «as contraband»"
    "strepto/s": [(4, "a collar of twisted or linked metal"), (9, "to be bent or turned"), (13, "glib, pliant")],
    "tra/peza": [(0, "a table")],
    # EXO 30. ἶρις: "the plant «Iris»", the appellative's last sense, its tr the bare name.
    "*)=iris": [(3, "the plant Iris")],
    # EXO 29. τελειόω: "of things, «to make» it «perfect, complete, accomplish»", "«to bring» one «to perfection»";
    # προτίθημι: "«to lay out» a dead body, «let» it «lie in state»", "«to set out» wares «for show» or «sale»",
    # "speech «was» not «allowed» them".
    "teleio/w": [(1, "to make it perfect, complete, accomplish"), (8, "to bring one to perfection")],
    "proti/qhmi": [(15, "let it lie in state"), (18, "to set out for show or sale"), (27, "was allowed")],
    # EXO 28. ἐξαρτάω: "perf. pass. part., c. acc. rei, «having» a thing «hung on one, be furnished with»".
    "e)carta/w": [(6, "having a thing hung on one, be furnished with")],
    # σμάραγδος: "Lat. smaragdus, a precious stone of a green colour", the English inside the Latin element, as
    # εἰ's "Lat. si, if".
    "sma/ragdos": [(0, "a precious stone of a green colour")],
    # συνέχω: "s. πόλιν «to keep» the state «together, keep» it «from falling to pieces»", "«to keep» the rowers
    # «together, make» them «pull in time»".
    "sune/xw": [(4, "to keep together, keep from falling to pieces"), (8, "to keep together, make pull in time")],
    # EXO 27. κόπτω: "k. τὴν χώραν «to cut down the trees in» it, «to lay» it «waste»".
    "ko/ptw": [(6, "to lay it waste")],
    # EXO 32. ἱλάσκομαι: "«to make» him «propitious to one, conciliate» him". τροπή: "«a change» of speech «by
    # figures» or «tropes»", the "of speech" the example's λέξεως; "«the turning of the enemy, putting» him «to
    # flight, a rout»". ἀνακάμπτω: "«to bend one's steps» back". εἶμι: "«I shall go, shall come. to come» or «go»",
    # the future use and the second sense run together in one element.
    "i(la/skomai": [(3, "to make him propitious to one, conciliate him")],
    "troph/": [(9, "a change by figures or tropes"), (13, "the turning of the enemy, putting him to flight, a rout")],
    "a)naka/mptw": [(2, "to bend one's steps back")],
    "ei)=mi": [(2, "I shall go, shall come"), (3, "to come or go")],
    # EXO 33. οἰκτείρω: "«to pity» one «for» or «because of» a thing".
    "oi)ktei/rw": [(1, "to pity one for or because of a thing")],
    # EXO 34. χρῶμα: "«the surface, skin: the colour of the» skin".
    "xrw=ma": [(1, "the surface, skin: the colour of the skin")],
    # EXO 35. παράρρυμα: "«anything drawn along the side: a leathern» or «hair curtain, stretched along» the sides of
    # ships".
    "para/rruma": [(0, "anything drawn along the side: a leathern or hair curtain, stretched along the sides of ships")],
    "suskia/zw": [(0, "to shade quite over, throw a shade over, shade closely or thickly")],
    "a)ki/nhtos": [(5, "not to be stirred or touched, inviolate")],
    "tu/pos": [(5, "the sound of their tread"), (8, "anything wrought of metal or stone")],
    "e)lau/nw": [(15, "to drive to extremities"), (26, "to drive or thrust through"), (30, "to beat with a hammer"),
                 (34, "to draw a line of wall or a trench"), (40, "plant them in line")],
    "de/on": [(1, "things needful or proper, advantages or duties")],  # τὰ δέοντα «things needful» or «proper, advantages» or «duties»
    "pleona/zw": [(2, "to go beyond bounds, take or claim too much")],
    "pikrai/nw": [(0, "to make sharp or bitter")],
    "th/kw": [(2, "to cause to waste or pine away")],
    "dii/sthmi": [(1, "to set one at variance with"), (4, "to divide it into fractions"),
                  (13, "to stand at certain distances or intervals")],
    "r(h/gnumi": [(0, "to break, break asunder or in pieces, rend, shiver, shatter")],  # «to break, break asunder» or «in pieces, rend, shiver, shatter»
    # EXO 12. αὐτόχθων: "αὐτόχθονες, οἱ, like Lat. Indigenae, aborigines, natives"; προσήλυτος: "a
    # sojourner, Lat. advena: one who has come over to Judaism, a convert, proselyte". The English
    # inside the Latin element, the Latin the capitalised Indigenae and advena.
    "au)to/xqwn": [(1, "aborigines, natives")],
    "prosh/lutos": [(2, "one who has come over to Judaism, a convert, proselyte")],
    # EXO 9. ὕω: "ὕει used impers., Lat. pluit, it rains" — the English inside the Latin element.
    # It is the third person's; a first or second person leaves it out (FORM_SENSES).
    "u(/w": [(1, "it rains")],
    "a)polei/pw": [(8, "to leave one in the lurch")],
    "sxola/zw": [(5, "to have rest or respite from"), (8, "to have leisure or opportunity for")],
    "a)faire/w": [(9, "to have it taken from one")],
    # "βίαι τινός against one's will, in spite of him": "one's" stands between two <tr>s.
    "bi/a": [(4, "against one's will, in spite of")],
    "kri/nw": [(0, "to separate, part, put asunder, distinguish")],  # "Lat. cerno, to separate, part, …"
    "mh/tra1": [(0, "the womb")],                # "Lat. matrix, the womb" — the whole entry
    "w)=mos": [(0, "the shoulder with the upper arm")],  # "Lat. humerus, the shoulder with the upper arm"
    "dh/": [(0, "now, in truth, indeed, surely, really")],  # "Lat. jam) now, in truth, indeed, surely, really"
    "ko/rac": [(0, "a raven")],                  # "Lat. corvus, a raven or carrion-crow"
    "lhno/s": [(0, "a tub")],                    # "like Lat. lacus, alveus, a tub or trough"
    "o(/qen": [(0, "whence, from which")],       # "Lat. unde, whence, from which … also from whom"
    "o)ste/on": [(0, "a bone")],                 # "Lat. os, ossis, a bone"
    "bre/xw": [(0, "to wet")],                   # "Lat. rigo, to wet"
    "nu/c": [(0, "night")],                      # "Lat. nox, night, i. e. either the night-season or a night"
    "a)gro/s": [(0, "a field")],                 # "Lat. ager, a field, in pl. fields, lands"
    "me/nw": [(0, "to stay stand fast, abide")],  # "Lat. maneo, to stay stand fast, abide" — the page's own comma
    "mh=lon2": [(0, "an apple")],                # "Lat. malum, an apple or (generally) any tree-fruit"
    "tre/mw": [(0, "to tremble, quake, quiver")],  # "Lat. tremo, to tremble, quake, quiver"
    "xa/skw": [(0, "to yawn, gape")],            # "Lat. hio, to yawn, gape"
    # these four keep the first sense they had; the lost English is a later one
    "ka/rfos": [(1, "a chip of wood")],          # "a dry stalk, Lat. palea, stipula, a chip of wood"
    "yu=xos": [(1, "frosts, cold weather")],     # the plural ψύχεα, "Lat. frigora frosts, cold weather"
    "oi)ke/ths": [(1, "one's household, the women and children")],  # οἱ οἰκέται, "Lat. familia, …"
    "e(/teros": [(1, "one of two")],             # "Lat. alter, the other, one of two"
    # Four more that the check found once it was looking at every word in the chapter
    # and not only the ones with units: a word written as plain text still gets a card,
    # and the card was showing an entry with its first translation missing.
    "mnhmei=on": [(0, "any memorial, remembrance, record")],  # "Lat. monimentum, any memorial, …"
    "trei=s": [(0, "three")],                    # "Lat. tres, tria, three" — the whole entry
    "o)ktw/": [(0, "eight")],                    # "Lat. octo, eight" — the whole entry
    "e(autou=": [(0, "of himself, herself, itself")],  # "Lat. sui, sibi, se, of himself, …"
    "u(po/dhma": [(1, "a shoe")],                # "Lat. calceus, a shoe"
    "staqmo/s": [(1, "a stable, fold")],         # "a standing place for animals, Lat. stabulum, a stable, fold"
    # Not Latin, but the same loss: ἐάν reads "if haply, if, followed by subj. (whereas εἰ is
    # foll. by ind. or opt.)", and only "if haply" is a <tr>. The plain "if" after it is the
    # printed entry's own translation, left untagged; the corpus had read ἐάν as that "if"
    # alone, εἰ's English, from GEN 4 on, with no unit and no "haply".
    "e)a/n": [(1, "if")],
    "me/li": [(0, "honey")],                     # "Lat. mel, honey" — the whole entry, all in the Latin
    # διαμαρτυρία reads "evidence given to prevent a case from coming to trial", and the <tr> stops
    # at "prevent": the rest of the translation is outside it.
    "diamarturi/a": [(0, "evidence given to prevent a case from coming to trial")],
    # Not Latin either: πρίαμαι reads "to have a thing sold to one, to buy, purchase", and the
    # italic object between "to have" and "sold to one" cuts one translation into two <tr>s.
    # The object is the word's own, supplied by the text.
    "pri/amai": [(0, "to have sold to one, to buy, purchase")],
}

# The first-sense Latin elements that hold Latin and nothing else, or whose English the
# entry already gives outside them, read and settled. Together with MARKUP_LOST this
# accounts for every one of them, so build/validate.py can fail on a new one and make
# somebody look rather than let a translation go quietly missing again.
LATIN_ONLY = {
    "pa=s", "o)/noma", "e(/ws", "e)k", "o(/te", "pou/s", "ai)/c", "o(/pws", "so/s",
    "u(yhlo/s", "pro/teros", "i(/ppos", "o)/yis", "despo/ths", "ge", "ei)=dos",
    "e(/rpw", "e)lai/a", "ste/ar", "lei=os", "e)/ar", "e)kba/llw", "e)pife/rw",
    # these five lose nothing: the run is Latin throughout, or the English beside it
    # is a <tr> of its own and already in the senses
    "ti/s", "e)/laion", "oi)=nos", "doke/w", "a)/zumos",
    "a)rno/s",                                  # "a lamb, Lat. agnus, agna": the lamb is a <tr>
    "w(/sper",                                  # "Lat. quasi, tanquam": Latin throughout; "just as if, even as" are <tr>s
    "a)rrabw/n",                                # "Lat. arrhabo, arrha", after "earnest-money, caution-money"
    "e)ntau=qa",                                # "Lat. hic, illic", after "here, there"
    "te/ras",                                   # "Lat. portentum, prodigium", after "a sign, wonder, marvel"
    "ou)de/pote",                               # "Lat. ne unquam quidem, nunquam", after "and not ever" or "nor ever, …, never"
    "fuga/s",                                   # "Lat. exul, profugus", after "a runaway, fugitive, a banished man, exile, refugee" (EXO 23:27)
    "xa/lkeos",                                 # "Lat. aeneus, aheneus", after "of copper" or "bronze, brasen" (EXO 26:11)
    "fi/los",                                   # "Lat. amicus, carus", after "loved, beloved, dear" (EXO 33:11)
}

# The same loss with Greek in place of Latin. Middle Liddell names a thing by its Greek word
# inside a translation — βύσσινος "made of βύσσος" — and Perseus tags the word as Greek, so
# the <tr> stops before it ("made of") or, where the tag sits inside the <tr>, the loader
# printed its Beta Code ("to be in the a)gora/"). Each sense is restored as the printed entry
# gives it, quoted beside it. build/validate.py fails on a new site until it is settled here
# or in GREEK_AFTER.
GREEK_LOST = {
    "xwneu/w": {"to cast into a mould (": "to cast into a mould (χόανος)"},  # "to cast into a mould (χόανος)" (EXO 26:37)
    "e)gxe/w": {"to fill the": "to fill the κλεψύδρα"},  # "ἐγχεῖν ὕδωρ τινί, i. e. to fill the κλεψύδρα (q. v.)" (EXO 24:6)
    "bu/ssinos": {"made of": "made of βύσσος"},  # "made of βύσσος, σινδὼν β. a fine linen bandage"
    "a)gora/zw": {"to be in the a)gora/": "to be in the ἀγορά",  # "to be in the ἀγορά, frequent it"
                  "to lounge in the": "to lounge in the ἀγορά"},  # "to lounge in the ἀγορά"
    "a)fi/hmi": {"to let go as an": "to let go as an ἄφετος"},  # "to let go as an ἄφετος, consecrate"
    "katoike/w": {"to dwell in as a": "to dwell in as a κάτοικος"},  # "to dwell in as a κάτοικος, to settle in"
    "r(a/bdos": {"the wand borne by the": "the wand borne by the ῥαψῳδός"},  # "the wand borne by the ῥαψῳδός"
    "e)piskoph/": {"the office of": "the office of ἐπίσκοπος"},  # "the office of ἐπίσκοπος, NTest."
    "eu)labe/omai": {"to behave like the": "to behave like the εὐλαβής"},  # "to behave like the εὐλαβής, have a care"
    "a)/logos": {"without": "without λόγος"},  # "«without» λόγος, i. e., without speech, speechless"
    "gru/zw": {"to say": "to say γρῦ"},  # "to say γρῦ, to grunt, grumble, mutter"
}

# Translations a Greek word follows without finishing: the gloss is whole, and the Greek
# after it is an example's object.
GREEK_AFTER = {
    "krate/w",                                  # "to become master of, get possession of" τῆς ἀρχῆς
    "a)palla/ssw",                              # "to leave off or cease from" τῶν μακρῶν λόγων
    "a)/n",                                     # a paragraph on usage tagged as one translation,
                                                # its Greek the examples: nothing is cut
}


# A word Middle Liddell files as a section of another word's entry instead of under a key
# of its own. "πρότερος and πρῶτος, Comp. and Sup. formed from πρό": section A is the
# comparative, B the superlative. Within B, I is the adjective and II the neuter plural
# used as a noun; III and IV are the adverbs πρῶτον and πρώτως. -> (host, section, parts)
FILED_WITHIN = {
    "prw=tos": ("pro/teros", "B", ("I", "II")),
}


def filed_within(body, section, parts):
    """The translations of one lettered section of an entry, and only the parts named."""
    out, inside, part = [], False, None
    for s in re.finditer(r"<sense\b([^>]*)>(.*?)</sense>", body, re.S):
        level = re.search(r'level="(\d+)"', s.group(1))
        n = re.search(r'\bn="([^"]*)"', s.group(1))
        level = int(level.group(1)) if level else 0
        n = n.group(1) if n else ""
        if level <= 1:
            inside = n == section
            continue
        if not inside:
            continue
        if level == 2:
            part = n
        if part in parts:
            out += [re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", g)).strip()
                    for g in re.findall(r"<tr\b[^>]*>(.*?)</tr>", s.group(2), re.S)]
    return [g for g in out if g]


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
        for at, gloss in MARKUP_LOST.get(key, ()):
            senses.insert(at, gloss)
        lost = GREEK_LOST.get(re.sub(r"\d+$", "", key), {})
        senses = [lost.get(g, g) for g in senses]
        entries.setdefault(key, senses)
        entries.setdefault(re.sub(r"\d+$", "", key), senses)
        for word, (host, section, parts) in FILED_WITHIN.items():
            if key == host:
                entries[word] = filed_within(body, section, parts)
    return entries


def lexicon_senses(entries, lemma, code="", form=""):
    key = SPELLING.get(beta(lemma), beta(lemma))
    key = ENTRY.get(key, key)
    if key not in entries:
        return None
    bare = re.sub(r"\d+$", "", key)
    # A word filed under another word's entry reads that entry's exclusions and its own, less
    # any it keeps: νή is filed under ναί, and the oath formula ναί sets aside is what νή is.
    skip = ((NOT_SENSES.get(bare, set()) | NOT_SENSES.get(beta(lemma), set()))
            - KEEP_SENSES.get(beta(lemma), set()))
    code = code.ljust(8, "-")
    plain = "".join(c for c in unicodedata.normalize("NFD", form)
                    if not unicodedata.combining(c)).lower()
    for rule in FORM_SENSES.get(bare, []):
        tenses, voices, instead = rule[:3]
        # a fourth item is a pattern the form itself must show, where the parse code
        # cannot tell two forms apart (a first aorist from a second); a fifth, a pattern the
        # parse must show, where the form cannot (βίᾳ and βία, without the iota, by case)
        if (code[1] in tenses and code[2] in voices
                and (len(rule) < 4 or not rule[3] or re.search(rule[3], plain))
                and (len(rule) < 5 or re.search(rule[4], code))):
            skip = instead
            break
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


def verse_key(ref):
    """A verse's number from `28:29` or `EXO 28:29`, as an int — or, for a verse Rahlfs
    prints with a letter after its number (Exod 28:29a, after 28:29), the number and the
    letter, `29a`."""
    number = ref.rsplit(":", 1)[1]
    return int(number) if number.isdigit() else number


def verse_order(key):
    """Sorts verse keys as the page does: 29, 29a, 30."""
    number = str(key)
    digits = number.rstrip("abcdefghijklmnopqrstuvwxyz")
    return int(digits), number[len(digits):]


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
        out.setdefault(verse_key(ref), []).append((form, lemma, pos, code, notes))
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
    return {verse: [(form, lemma, code, morphgnt(pos, code))
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
        out.setdefault(int(cols[0][4:6]), []).append((word, lemma, code, morphgnt(pos, code)))
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
    # One form can name two bearers in a chapter (Σεννααρ, the land at GEN 14:1 and the king
    # at 14:2), told apart by their English names; a card takes its own bearer's gloss.
    bearers = {(n["greek"], n["anchored"]): n["gloss"] for verse in verses
               for n in verse.get("names", []) if n.get("gloss")}
    # A name glossed in one case and bare in another (Σιδῶνα, then Σιδῶνος, GEN 10) shares
    # its dictionary form, and the card for the bare one takes the gloss through it.
    by_lemma = {lemma: names[form] for words in tokens.values()
                for form, lemma, *_ in words if form in names}

    out = []
    for verse in verses:
        number = verse_key(verse["ref"])
        ours = PUNCT.sub("", verse["greek"]).split()
        theirs = tokens.get(number, [])
        if len(ours) != len(theirs) or not all(same(t[0], o) for t, o in zip(theirs, ours)):
            raise SystemExit("%s: the source's words do not match the verse's Greek\n  ours:   %s\n"
                             "  source: %s" % (verse["ref"], " ".join(ours),
                                               " ".join(t[0] for t in theirs)))
        words = []
        for form, (_, lemma, code, (parse, aspect)) in zip(ours, theirs):
            # A word the verse marks as a name is a name. Σκηναί and Λουζα reach this
            # already, because no lexicon entry answers to them; Βάλανος, Υἱός and Εἶδος
            # did not, because lower-casing their Beta Code lands on the common noun they
            # are made from, and the noun's senses were shown in place of the name.
            marked = next((n for n in verse.get("names", []) if n["greek"] == form), None)
            if marked:
                own = bearers.get((marked["greek"], marked["anchored"]))
                gloss = own or marked.get("gloss") or names.get(form) or names.get(lemma)                     or by_lemma.get(lemma)
                if gloss:
                    words.append({"form": form, "lemma": lemma, "parse": parse,
                                  "aspect": aspect, "senses": [gloss], "more": 0,
                                  "lexicon": "name"})
                    continue
            # Middle Liddell first. LSJ answers only where Middle Liddell has no entry for
            # the word under its own key or a close form of it (SPELLING, ENTRY,
            # FILED_WITHIN). An entry whose translation the markup hides is recovered from
            # Middle Liddell itself (MARKUP_LOST), not replaced by LSJ.
            senses, lexicon = lexicon_senses(entries, lemma, code, form), "Middle Liddell"
            if not senses and (lemma in names or form in names or lemma in by_lemma):
                # A name entry is keyed by the form the verse prints (Ἀσσυρίων), which
                # is not always the dictionary form the morphology gives (Ἀσσύριος). It
                # also stands in for an entry that tags nothing: Middle Liddell's γάζα,
                # "treasure", is another word, and glosses nothing for Γάζα at GEN 10:19.
                own = next((bearers.get((n["greek"], n["anchored"])) for n in verse.get("names", [])
                            if n["greek"] == form), None)
                senses, lexicon = [own or names.get(lemma) or names.get(form) or by_lemma[lemma]], "name"
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
