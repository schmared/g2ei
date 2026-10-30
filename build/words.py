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
    "a(/ptw": {"engaged in", "on", "to fasten", "to fasten for oneself", "to fasten, bind fast", "to join", "to reach the mark"},  # pieces of examples
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
    "o(/rkos": {"an oath by", "oath", "the tender"},  # pieces of examples
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
    "sxi/zw": {"divided", "into", "branches"},  # pieces of examples
    "au)tou=": {"exactly"},                     # a piece of an example
    "paida/rion": {"a child"},                  # a piece of an example
    "ke/ras": {"horns", "horn doors", "true", "in flank", "towards the wing", "in column"},  # pieces of examples
    "e)mo/s": {"possessive", "for me"},         # pieces of examples
    # GEN 23
    "ko/ptw": {"smote", "on"},                  # pieces of an example
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
    "sunagwgh/": {"a levying", "a gathering in of"},  # pieces of examples
    "a)panta/w": {"from", "anyone that meets you, any chance person"},  # pieces of examples
    "du/w": {"plunged into", "plunge into", "go in to"},  # pieces of examples
    "a)fikne/omai": {"from", "the person reached"},  # pieces of examples
    "u(poti/qhmi": {"beginning"},               # a piece of an example
    "e)pixe/w": {"shed over", "throw", "oneself"},  # pieces of examples
    "eu)/xomai": {"to pray that", "long"},      # pieces of examples
    "fobero/s": {"formidable", "terror"},       # pieces of examples
    "a)/kron": {"the highest", "furthest point"},  # pieces of "the highest or furthest point"
    # GEN 29
    "e)caei/rw": {"having bade", "rise"},       # pieces of an example
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
    "fai/nw": {"to shew", "to make"},           # pieces of examples
    # GEN 31
    "do/ca": {"one expects", "expect"},          # pieces of an example
    "a)lla/ssw": {"to take"},                    # a piece of "to take one thing for another"
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
    "bia/zw": {"overpowered", "suffer violence", "forcibly made slaves"},  # pieces of the passive
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
    # so the form decides: the causal tenses are built on στησ-.
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
        "subject to migration", "to be put up"}, "στησ")],
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
    "loidore/w": [("PIFAXY", "A", {"to rail at one another", "to rail at", "they use", "reproaches"})],
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
        "recommend one to another", "to offer", "as a guarantee", "the conspirators"})],
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
}

# The same loss with Greek in place of Latin. Middle Liddell names a thing by its Greek word
# inside a translation — βύσσινος "made of βύσσος" — and Perseus tags the word as Greek, so
# the <tr> stops before it ("made of") or, where the tag sits inside the <tr>, the loader
# printed its Beta Code ("to be in the a)gora/"). Each sense is restored as the printed entry
# gives it, quoted beside it. build/validate.py fails on a new site until it is settled here
# or in GREEK_AFTER.
GREEK_LOST = {
    "bu/ssinos": {"made of": "made of βύσσος"},  # "made of βύσσος, σινδὼν β. a fine linen bandage"
    "a)gora/zw": {"to be in the a)gora/": "to be in the ἀγορά",  # "to be in the ἀγορά, frequent it"
                  "to lounge in the": "to lounge in the ἀγορά"},  # "to lounge in the ἀγορά"
    "a)fi/hmi": {"to let go as an": "to let go as an ἄφετος"},  # "to let go as an ἄφετος, consecrate"
    "katoike/w": {"to dwell in as a": "to dwell in as a κάτοικος"},  # "to dwell in as a κάτοικος, to settle in"
    "r(a/bdos": {"the wand borne by the": "the wand borne by the ῥαψῳδός"},  # "the wand borne by the ῥαψῳδός"
    "e)piskoph/": {"the office of": "the office of ἐπίσκοπος"},  # "the office of ἐπίσκοπος, NTest."
    "eu)labe/omai": {"to behave like the": "to behave like the εὐλαβής"},
    "a)/logos": {"without": "without λόγος"},  # "«without» λόγος, i. e., without speech, speechless"  # "to behave like the εὐλαβής, have a care"
}

# Translations a Greek word follows without finishing: the gloss is whole, and the Greek
# after it is an example's object.
GREEK_AFTER = {
    "krate/w",                                  # "to become master of, get possession of" τῆς ἀρχῆς
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
        number = int(verse["ref"].rsplit(":", 1)[1])
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
