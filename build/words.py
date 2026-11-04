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
    # Middle Liddell has no μεθερμηνεύω. LSJ: "translate, LXX Si.Prol., …:—freq. in Pass." (JHN 1:38)
    "μεθερμηνεύω": ["translate"],
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
    # and not GEN 50:8's nominative: FORM_SENSES gives it to the dative alone. LSJ (eng21): συναναφέρω, the active's senses, "carry up
    # together", metaph. "bring up together with itself", "refer to … at the same time", "certify at
    # the same time", "report"; the passive's and the astronomers' are left out, as GEN 50:25's
    # συνανοίσετε is active.
    "ἐνταφιαστής": ["undertaker, embalmer"],
    "πανοικία": ["whole household", "with all the house"],
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
    # EXO 38. Not in Middle Liddell. LSJ (eng12): λαβίς, "«handle»", "«hilt»", "«holder», i.e. «forceps»",
    # "«clamp, clasp»", "«tongs» or «snuffers» to trim lamps", citing 38:17. LSJ (eng5) gives ἐπαρυστρίς no gloss of
    # its own, "= foreg.", ἐπαρυστήρ, so it reads ἐπαρυστήρ's, as at 25:38. LSJ (eng17): παράθεμα, "«appendage»",
    # citing 38:24; its "= ἐπίθεμα" is Hesychius's. LSJ (eng4): διωστήρ, "«instrument for pushing out» embedded
    # weapons", "«pole running through rings,» for carrying the ark", citing 38:10. LSJ (eng5): ἐνθέμιον, "«cabin on
    # the poop of a ship»", "«socket» of a lampstand", citing 38:16. LSJ (eng11), under καρυωτός: the masculine made a
    # noun, ὁ κ. (sc. φοῖνιξ), "«date»-palm", and the adjective, φιάλη καρυωτή, "«adorned with a nut-shaped boss»",
    # "also κ. λαμπάδια LXX Ex. 38.16": this text has the adjective.
    "λαβίς": ["handle", "hilt", "holder", "forceps", "clamp, clasp", "tongs", "snuffers"],
    "ἐπαρυστρίς": ["vessel for pouring oil into a lamp"],
    "παράθεμα": ["appendage"],
    "διωστήρ": ["instrument for pushing out embedded weapons", "pole running through rings for carrying the ark"],
    "ἐνθέμιον": ["cabin on the poop of a ship", "socket of a lampstand"],
    "καρυωτός": ["adorned with a nut-shaped boss"],
    # EXO 39. Not in Middle Liddell. LSJ (eng25) gives χώνευσις no gloss of its own, "= χωνεία", and LSJ's χωνεία
    # is "«melting and casting of metal»", so it reads that.
    "χώνευσις": ["melting and casting of metal"],
    # EXO 40. Not in Middle Liddell. LSJ (eng4): διεμβάλλω, "«put in through»". LSJ (eng1): ἀπαρτία, "= ἀποσκευή",
    # and then glosses of its own, "«household utensils, movables, chattels»", citing 40:36, "«spoil»", "«public
    # auction»"; Hesychius's list after them is his. LSJ (eng1) gives ἀναζυγή no gloss of its own, "= ἀνάζευξις",
    # citing 40:38, so it reads Middle Liddell's ἀνάζευξις, as πόρευσις reads πορεία's (GEN 33).
    "διεμβάλλω": ["put in through"],
    "ἀπαρτία": ["household utensils, movables, chattels", "spoil", "public auction"],
    "ἀναζυγή": ["a marching off, return home"],
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

# Homographs Middle Liddell lacks: it has the key, but under it a different word, so its entry is
# not the text's word at all. περισκελής is two words in LSJ — (A) from σκέλλω, "dry and hard all
# round", the one Middle Liddell has; (B) from σκέλος, "round the leg", whence τὰ περισκελῆ, drawers,
# citing EXO 28:42 — and the text's is (B). Each is named with the etymology that tells the two
# apart; build/validate.py accepts an LSJ reading of a word Middle Liddell has through this table
# only.
LSJ_HOMOGRAPHS = {
    "περισκελής": ("σκέλος", ["round the leg", "drawers"]),  # LSJ περισκελής (B) (eng10)
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
    "u(pere/xw": {"to hold", "over", "so as to protect", "hold above", "he had", "above", "the ground", "to overtop",
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
    "u(pa/rxw": {"to make a beginning of", "to begin", "a beginning", "had been made",  # pieces and repeats of sense I
                 "there is store", "quae cum ita sint", "he will be on", "side",  # a construction's; Latin; an example's pieces
                 "the fact is that . .", "it is allowed, it is possible", "was possible", "since it is allowed"},  # the
                 # impersonal construction's, ὑπάρχει c. acc. (or dat.) et inf. (Q12)
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
    "paragi/gnomai": {"near, attend upon"},       # cut, whole in MARKUP_LOST (Q15)
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
    # EXO 40
    "e)piskia/zw": {"keeping a hidden watch"},  # the passive participle's example, ὄμμ' ἐπεσκιασμένη
    # EXO 39
    "difqe/ra": {"(an undressed hide)"},       # the entry's contrast with δέρρις
    "katakosme/w": {"was fitting"},            # an example's, "«was fitting» it on the string"
    "pro/qesis": {"laid before, the shewbread"},  # an example's, οἱ ἄρτοι τῆς προθέσεως
    # EXO 38
    "stereo/s": {"solid gold", "a cubic"},     # examples', "all of «solid gold»", "«a cubic» number"
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
    "e)ci/sthmi": {"to drive", "out of", "to lose", "give", "up"},  # "to drive one out of", "to lose one's father, give him
                                                 # up", "to lose one's senses" cut, whole in MARKUP_LOST; an example's piece
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
    # The edit pass after Exodus (reference/open-questions.md, settled)
    "du/o": {"two and two"},                     # Q29: the doubled δύο δύο's, which only the doubled word makes
    "qeo/s": {"his will", "God's name", "more divine", "more used by the gods"},  # Q28: pieces of ὑπὲρ θεόν and
                                                 # the oath "in God's name"; the comparative θεώτερος's, and an example's
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
_UPARXW_NOUN = {"existing circumstances, present advantages", "what belongs to one, one's possessions, means"}
_UPARXW_PTCP = {"existing", "current", "own proper", "normal"}
_UPARXW_VERB = {"to begin, make a beginning", "to begin to be, come into being, arise, spring up",
                "to be in existence, to be there, to be ready", "to be", "to be laid down, to be taken for granted",
                "to belong to, fall to", "accrue", "to be devoted to", "to be begun"} | _UPARXW_PTCP
_EXISTHMI_CAUS = {"to put out of its place, to change", "alter utterly", "to drive one out of", "to derange"}
_EXANISTHMI_INTR = {
    "bid one", "rise", "to stand up from one's seat", "to arise and depart from, emigrate from",
    "to break up, depart", "to be driven out", "to be forced to emigrate", "to be depopulated"}
_EXANISTHMI_CAUS = {
    "to raise up: to make one rise", "bid one", "rise", "to order", "to rise", "to make",
    "emigrate, to remove", "expel", "to depopulate, destroy", "to rouse", "from their lair"}
_APOLLUMI_ACT = {"to destroy utterly, kill, slay", "to destroy, demolish, waste", "to talk", "bore", "to death",
                 "bore one to death", "to lose utterly"}
_APOLLUMI_MID = {"to perish utterly, die", "to be undone", "you are done for, lost, ruined",
                 "to be lost, slip away, vanish"}
# συνίστημι's B, "Pass. and intr. tenses of Act.": read by the passive, the perfect and the aor2
SUNISTHMI_INTRANSITIVE = {
    "to stand together", "to form in order of battle", "to meet", "in fight, be engaged with", "to be involved",
    "to form a league or union", "to be connected or allied", "to arise, become, take place",
    "to hold together, endure, continue", "to be compact, solid, firm", "to be contracted"}
FORM_SENSES = {
    # Q3: an LSJ word takes the same rules. πανοικία's "with all the house" is the dative's, "dat. as Adv."
    "panoiki/a": [("-", "-", {"with all the house"}, None, "^....[NGAV]")],
    # Q14: a pointer the entry gives the plural, read in the plural only
    "diplo/os": [("-", "-", NOT_SENSES["diplo/os"] | {"two"}, None, "^.....S")],
    # Q12: ὑπάρχω's passive alone is "to be begun"; its participle alone "existing", "current", "own proper",
    # "normal" (ἡ ὑπάρχουσα οὐσία, φύσις); its neuter plural participle, τὰ ὑπάρχοντα, is the noun, read in the
    # noun's senses only, as a word used as a noun is. Q11: ἀναγγέλλω's "was reported" is the passive's.
    "u(pa/rxw": [("PIFAXY", "AME", NOT_SENSES["u(pa/rxw"] | _UPARXW_VERB, None, "^...P.PN"),
                 ("PIFAXY", "AME", NOT_SENSES["u(pa/rxw"] | _UPARXW_NOUN | {"to be begun"}, None, "^...P"),
                 ("PIFAXY", "AME", NOT_SENSES["u(pa/rxw"] | _UPARXW_NOUN | _UPARXW_PTCP | {"to be begun"})],
    "a)nagge/llw": [("PIFAXY", "AM", {"was reported"})],
    "mhro/s": [("-", "-", {"slices cut from the thighs", "the thighs"}, None, "^.....S")],
    # The edit pass after Exodus. κύριος, two entries under one key (ENTRY): the noun's κυρία,
    # "mistress, lady of the house", is the feminine's; "sir", the vocative's ("later, κύριε was a
    # form of respectful address"); "the Lord" and "Jehovah", ὁ Κύριος's, the singular's. The
    # adjective's comparatives (κυριώτεροι, "better able", "of more authority"), its uses as a
    # noun (τὸ κύριον, τὰ κύρια) and the phrase κ. θέσθαι's "by authority" are not EXO 21:8's
    # predicate. Each entry's strings are its own, so one set serves both.
    "ku/rios": [("-", "-", {"a lord, master", "the head", "master", "sir", "the Lord", "Jehovah"}, None, "^......F"),
                ("-", "-", {"mistress", "lady of the house", "better able", "of more authority", "the ruling power",
                            "the authorities", "by authority", "the appointed"}, None, "^....VS"),
                ("-", "-", {"mistress", "lady of the house", "the Lord", "Jehovah"}, None, "^....VP"),
                ("-", "-", {"mistress", "lady of the house", "sir", "the Lord", "Jehovah"}, None, "^.....P"),
                ("-", "-", {"mistress", "lady of the house", "sir", "better able", "of more authority",
                            "the ruling power", "the authorities", "by authority", "the appointed"}, None, "^.....S")],
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
        "to set before oneself", "to put in front"}),
                   # EXO 40: the active leaves out the middle's and the passive's "was allowed"
                   ("PIFAXY", "A", NOT_SENSES["proti/qhmi"] | {
        "to have set before one", "to propose to oneself", "to put forth on one's own part, display, shew",
        "to set before oneself", "to put in front", "was allowed"})],
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
    # EXO 38. στερεός's adjective leaves out the adverb's "firmly, fast"; καταστασιάζω's active the passive's.
    "stereo/s": [("-", "-", NOT_SENSES["stereo/s"] | {"firmly, fast"}, None, "^....[NGDAV]")],
    "katastasia/zw": [("PIFAXY", "A", {"to be factiously opposed", "overpowered"})],
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
    # Q18: and "intr. in Pass. and Mid., with aor2, perf., and plup. act.", which leave out the causal senses;
    # "changed, sour" and "disfigured" translate the perfect participle in examples, and stay with it.
    "e)ci/sthmi": [("F", "A", NOT_SENSES["e)ci/sthmi"] | {
        "to stand aside from", "is displaced, disordered", "to shrink from, shun", "to retire from, give up possession of",
        "to cease from, abandon", "to lose one's father, give him up", "to lose one's senses",
        "to be out of one's wits, to be astonished, amazed", "to degenerate", "changed, sour", "disfigured",
        "to change one's position, one's opinion"}),
                   ("A", "A", NOT_SENSES["e)ci/sthmi"] | _EXISTHMI_CAUS | {"changed, sour", "disfigured"}, "εστη$"),
                   ("PIFAXY", "EMP", NOT_SENSES["e)ci/sthmi"] | _EXISTHMI_CAUS | {"changed, sour", "disfigured"}),
                   ("XY", "A", NOT_SENSES["e)ci/sthmi"] | _EXISTHMI_CAUS)],
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
        "a standing"}, "^(?!.*στησ)"),
                   # the transitive tenses, aor1 συνέστησεν (GEN 40:4) and the present and future, leave out
                   # the intransitive section, which the coverage pass had given the passive alone (Q33)
                   ("PIFA", "A", NOT_SENSES["suni/sthmi"] | SUNISTHMI_INTRANSITIVE)],
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
    "fw=s": "fa/os",                # φῶς, the contraction Middle Liddell prints inside φάος (JHN 1:4)
    "i)/de": "i)de/2",              # ἴδε, "imperat. aor. of εἶδον, lo, behold", the second ἰδέ (JHN 1:29)
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
    # Two words under one spelling, told apart by the part of speech the morphology gives: the
    # adjective, "having power or authority over", is the first entry; the noun, "a lord,
    # master", the second. EXO 21:8's οὐ κύριός ἐστιν πωλεῖν is the adjective, the
    # construction its entry names: κύριός εἰμι, c. inf., "I have authority to do".
    "ku/rios": {"noun": "ku/rios2", "adjective": "ku/rios1"},
    # μήν the particle, "now verily", is filed under its own key; SPELLING sends the noun's μήν,
    # month, to μείς, and the particle with it, so the part of speech sends it back
    "mei/s": {"noun": "mei/s", "particle": "mh/n"},
}


def entry_key(key, parse=""):
    """The entry a key reads, by ENTRY, for a form whose parse begins `parse`."""
    to = ENTRY.get(key, key)
    if isinstance(to, dict):
        pos = parse.split(" ·")[0]
        return to.get(pos, next(iter(to.values())))
    return to


def entry_keys(key):
    """Every entry ENTRY may send a key to."""
    to = ENTRY.get(key, key)
    return list(to.values()) if isinstance(to, dict) else [to]

# SBLGNT's critical signs — ⸀ ⸂…⸃ marking a variant, ⟦…⟧ the bracketed John 7:53–8:11 — stand
# beside a word and are not one
PUNCT = re.compile(r"[.,;:·!?—·()⸀⸁⸂⸃⸄⸅⟦⟧]")


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
    # The same fault in a later sense, which the first-sense check never reads; found by the
    # support check (Q32), where a chain carried the English and its card did not.
    "ai(=ma": [(4, "blood-relationship, kin")],    # III, "like Lat. sanguis, blood-relationship, kin"
    "e)calei/fw": [(5, "to wipe out, destroy utterly")],  # 2, "metaph., like Lat. delere, to wipe out, destroy utterly"
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
    # Q15. παραγίνομαι: "to be beside, to be by or «near, attend upon» one" — the first two cut off
    # outside the <tr>, so the head began at *near*.
    "paragi/gnomai": [(0, "to be beside, to be by or near, attend upon")],
    # μήν, the particle: "Lat. vero, verily, truly" — the English inside the Latin element
    "mh/n1": [(1, "verily, truly")],
    # ὑπερέχω: "«to hold» one thing «over» another"
    "u(pere/xw": [(0, "to hold over")],
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
    "e)ci/sthmi": [(2, "to drive one out of"),
                   # Q18: "ἐκστῆναι πατρός «to lose» one's father, «give» him «up»"; "φρενῶν ἐξεστάναι «to lose» one's senses"
                   (12, "to lose one's father, give him up"), (13, "to lose one's senses")],
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
    "me/nw": [(0, "to stay stand fast, abide")],  # "Lat. maneo, to stay stand fast, abide"; the comma after *stay*, lost, in MISPRINTS
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
    "stura/kinos": {"made of the wood of the tree": "made of the wood of the tree στύραξ"},  # "made of the wood of the tree στύραξ" (GEN 30:37)
}

# A sense that is only a pointer, "= X": πάγος ends "= παγετός, Soph.", and παγετός is *frost*.
# Where a whole entry is a pointer the corpus reads the entry pointed to; a sense that is one
# reads X's translations in its place (after the translation named, or first where none is), X's
# own NOT_SENSES applied. build/validate.py fails on a pointer among the corpus's words until it
# is settled here or in POINTERS_NOT_READ.
SENSE_POINTERS = {
    "bo/trus": ("bunch of grapes", "bo/struxos"),         # "a cluster or bunch of grapes, … = βόστρυχος, Anth."
    "gerousi/a": ("a Council of Elders, Senate", "presbei/a"),  # "a Council of Elders, Senate, Eur. = πρεσβεία"
    "diplo/os": ("mutual", "du/o"),                        # "in pl., = δύο" — the plural's (FORM_SENSES)
    "qa/natos": ("Death", "nekro/s"),                      # "Θάνατος Death, … = νεκρός, Anth."
    "kaqw/s": (None, "kaqa/"),                             # "= καθά, Hdt., NTest.", the entry's first sense
    "li/banos": ("the frankincense-tree", "libanwto/s"),   # "= λιβανωτός, in which sense it is fem."
    "mei/s": ("by the month", "mhni/skos"),                # "= μηνίσκος, Ar."
    "mhro/s": ("the thigh", "mhri/a"),                     # "in pl. = μηρία" — the plural's (FORM_SENSES)
    "pa/gos": ("the Areopagus", "pageto/s"),               # "= παγετός, Soph."
    "a)poskhno/w": ("to keep apart from", "a)poskhne/w"),  # "= ἀποσκηνέω, Plut."
    "o(/rmos": ("refuge", "e(/rma1"),                      # "= ἕρμα 1, Anth."
}
POINTERS_NOT_READ = {
    "peri/": "rarely = ἀμφί, as in περιδέξιος: a compound's sense, not the preposition's",
    "a)/maca": "= ἁμαξιτός, which Middle Liddell has no entry for",
    "dou=los": "the neuter τὸ δοῦλον's, a collective, = οἱ δοῦλοι and δουλεία: not δούλη's, which is filed here",
    "ei)": "a construction's: εἰ after verbs of wonder or indignation, = ὅτι",
    "o(/s": "early Greek's demonstrative use, = οὗτος: not the relative's",
}


def read_pointers(entries):
    """SENSE_POINTERS read into the entries they stand in, in place."""
    for key, (after, target) in SENSE_POINTERS.items():
        senses = entries[key]
        bare = re.sub(r"\d+$", "", target)
        add = []
        for g in entries[target]:
            g = g.rstrip(".")
            if g not in NOT_SENSES.get(bare, set()) and g not in senses and g not in add:
                add.append(g)
        # the translation named may have been joined to the one before it by "or"
        at = 0 if after is None else next(i for i, g in enumerate(senses)
                                          if g == after or after in g.split(" or ")) + 1
        senses[at:at] = add


# Translations a Greek word follows without finishing: the gloss is whole, and the Greek
# after it is an example's object.
GREEK_AFTER = {
    "krate/w",                                  # "to become master of, get possession of" τῆς ἀρχῆς
    "a)palla/ssw",                              # "to leave off or cease from" τῶν μακρῶν λόγων
    "a)/n",                                     # a paragraph on usage tagged as one translation,
                                                # its Greek the examples: nothing is cut
}

# Translations the tagging cuts where the printed entry runs on in plain English (Q32): διαθήκη's
# «an arrangement between» two parties, «covenant» — the <tr> stops at *between*, and *two parties*
# stands outside it, though it is the translation's own end. GREEK_LOST restores a translation a
# Greek word finishes; this one a translation its own English finishes. Each value is the entry's
# words, in order, with nothing added: the chains carried them already, written from the page,
# and the support check, which reads a chain against its card, found the card short of them.
TEXT_LOST = {
    "diaqh/kh": {"a disposition": "a disposition of property by will",      # «a disposition» of property by will
                 "an arrangement between": "an arrangement between two parties"},  # «an arrangement between» two parties
    "diati/qhmi": {"to dispose of one's": "to dispose of one's property",  # «to dispose of one's» property,
                   "devise": "devise it by will"},                       # «devise» it «by will»
    "glw=ssa": {"mouthpiece": "mouthpiece of a pipe"},                    # «the tongue» or «mouthpiece» of a pipe
    "kei/rw": {"to ravage": "to ravage a country",                        # «to ravage» a country,
               "by cutting down": "by cutting down the crops and fruit-trees"},  # «by cutting down» the crops and fruit-trees
    # «a number of» 10, 000: the numeral in words, since a comma parts a chain's senses
    "muria/s": {"a number of": "a number of ten thousand"},
    "pu/rgos": {"a movable tower for": "a movable tower for storming towns"},  # «a movable tower for» storming towns
    "sfa/zw": {"to slaughter": "to slaughter victims for sacrifice"},     # esp. «to slaughter» victims for sacrifice
    "suntele/w": {"to belong to": "to belong to a class, be counted in it"},  # «to belong to» a class, be counted in it
    "tetra/pous": {"four feet": "four feet in length"},                   # of things, «four feet» in length
    "e)rgasi/a": {"a working": "a working of a material"},                # «a working» of a material
    "e)gxw/rios": {"a dweller in": "a dweller in the land"},              # «a dweller in» the land, «inhabitant»
    "e)cariqme/w": {"to count out, pay in ready": "to count out, pay in ready money"},  # «to count out, pay in ready» money
    "e)pikale/w": {"to call in": "to call in as a helper or ally"},       # Mid. «to call in» as a helper or ally
    "kta/omai": {"get": "get for another"},                               # «to procure» or «get» for another
    "a)/ggos": {"a cinerary": "a cinerary urn"},                          # «a cinerary» urn
    "sunnefe/w": {"wearing a clouded": "wearing a clouded look"},         # «wearing a clouded» look
    "xroni/zw": {"long": "to remain long"},                               # to remain «long»
    "mai=a": {"a": "a true mother"},                                      # «a» true «mother»
    "a)pa/gw": {"to lead away": "to lead away from the subject"},         # «to lead away» from the subject
    "a)lla/ssw": {"to take": "to take one thing for another"},            # «to take» one thing «for» another
    "sugxai/rw": {"joy, congratulate": "wish one joy, congratulate"},    # «to wish» one «joy, congratulate»
    "a)po/llumi": {"bore": "bore one to death"},                         # «to talk» or «bore» one «to death»
    "e)chge/omai": {"to shew": "to shew one the way, go before, lead"},  # «to shew» one «the way, go before, lead»
    "i(ma/s": {"the traces by which horses were": "the traces by which horses were attached to the chariot"},
}

# A misprint in the encoded entry, corrected to the word the entry plainly means and nothing more:
# μένω's «to be lasting, remian, last, stand». GEN 24:55 printed it *remain* from its first draft
# (lexicon-notes, *Words new in GEN 24*); the Q24 rebuild read the card back, misprint and all, into
# every μένω unit, and John 1 gave it five more. The same entry opens «Lat. maneo, to stay stand
# fast, abide», a comma short: *stay stand fast* is no English, and read as one translation it put
# *stayed stand fast* in JHN 1:32 and 1:39. The comma is restored, so the run is three pieces, `stayed
# / stood fast / abided`, and the headword *stayed* (2026-11-04). A correction applies to the
# translations MARKUP_LOST restores as well as to the <tr>s.
MISPRINTS = {
    "me/nw": {"remian": "remain", "stay stand fast": "stay, stand fast"},
}


def corrected(key, gloss):
    """A translation with the entry's misprints put right (MISPRINTS)."""
    for bad, good in MISPRINTS.get(re.sub(r"\d+$", "", key), {}).items():
        gloss = re.sub(r"\b%s\b" % bad, good, gloss)
    return gloss


# A word Middle Liddell files as a section of another word's entry instead of under a key
# of its own. "πρότερος and πρῶτος, Comp. and Sup. formed from πρό": section A is the
# comparative, B the superlative. Within B, I is the adjective and II the neuter plural
# used as a noun; III and IV are the adverbs πρῶτον and πρώτως. -> (host, section, parts)
FILED_WITHIN = {
    "prw=tos": ("pro/teros", "B", ("I", "II")),
    # πλατεῖα, the street: "πλατεῖα (sc. ὁδός), a street; (sub. χείρ), the flat of the hand", πλατύς I.5. Read
    # through the whole adjective it took the adjective's senses, which the noun is not (Q32). A fourth
    # item is the level the section stands at, where the entry has no lettered sections above it.
    "platei=a": ("platu/s", "I", ("5",), 2),
}


def filed_within(body, section, parts, depth=1):
    """The translations of one lettered section of an entry, and only the parts named."""
    out, inside, part = [], False, None
    for s in re.finditer(r"<sense\b([^>]*)>(.*?)</sense>", body, re.S):
        level = re.search(r'level="(\d+)"', s.group(1))
        n = re.search(r'\bn="([^"]*)"', s.group(1))
        level = int(level.group(1)) if level else 0
        n = n.group(1) if n else ""
        if level <= depth:
            inside = n == section
            continue
        if not inside:
            continue
        if level == depth + 1:
            part = n
        if part in parts:
            out += [re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", g)).strip()
                    for g in re.findall(r"<tr\b[^>]*>(.*?)</tr>", s.group(2), re.S)]
    return [g for g in out if g]


# Latin the encoding put inside an English translation, Middle Liddell's gloss of its own gloss:
# δοκέω "videor mihi, to think", πνεῦμα "anima, breathed air, breath", πῆχυς "ulna, a cubit or ell",
# ἐπεί "after (postquam), since, when (quum)". The English is the sense; the Latin is cut.
LATIN_IN = ("videor mihi", "videor", "anima", "ulna", "agere", "pinus picea", "alius", "tamen, vero",
            "uti familiariter", "in rationes referre", "priusquam", "summum bonum", "placuit senatui")


def tidy_gloss(gloss):
    gloss = re.sub(r";\s*also$", "", gloss)                      # λαός "soldiers; also", the next sense's
    gloss = re.sub(r"\s*\((?:postquam|quum)\)", "", gloss)
    for latin in LATIN_IN:
        gloss = re.sub(r"(?:^|(?<=, ))%s(?:, |$)" % re.escape(latin), "", gloss)
    gloss = re.sub(r"(?<=[a-z]{2})\. (?=[a-z])", ", ", gloss)        # ὄνομα "a name. fame"
    return gloss.replace("theHoly", "the Holy").strip(" ,")


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
        # Two translations the entry joins with "or" — συναναβαίνω's "«to go up with» or «together»",
        # ἐφίστημι's "«to stand by» or «near»" — are one translation: the second is not always a
        # sense by itself (*together*, *near*), and dropped it is a sense lost (Q2). Each is kept
        # with the one before it, as the entry prints them.
        trs, last = [], None
        for t in re.finditer(r"<tr\b[^>]*>(.*?)</tr>", scope, re.S):
            text = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", t.group(1))).strip()
            between = re.sub(r"<[^>]+>", "", scope[last:t.start()]).strip() if last is not None else None
            trs.append((text, between == "or"))
            last = t.end()
        lost = dict(GREEK_LOST.get(re.sub(r"\d+$", "", key), {}))
        lost.update(TEXT_LOST.get(re.sub(r"\d+$", "", key), {}))
        cleaned = []
        for gloss, joined in trs:
            # One translation in the whole lexicon runs on into the voice label after it —
            # ἐξαποστέλλω's "to send quite away:—Pass." — so the label is cut off, not the gloss.
            gloss = re.sub(r":\s*—\s*(?:Pass|Mid|Act)\.$", "", gloss)
            # Nine run on into the sign of an equivalence after them — κύριος's "the Lord, = Hebr.
            # Jehovah" — so the sign is cut, and the translation it points to stays its own.
            gloss = re.sub(r",?\s*=$", "", gloss)
            # A preposition's entry opens with the case it governs inside the translation —
            # ἀπό's "from, away from. c. gen." — and the label is the entry's, not the gloss's.
            gloss = re.sub(r"\.?\s+c\. (?:gen|dat|acc)\.$", "", gloss)
            gloss = corrected(key, tidy_gloss(gloss))
            cleaned.append((lost.get(gloss, gloss), joined))
        for at, gloss in MARKUP_LOST.get(key, ()):
            cleaned.insert(at, (corrected(key, gloss), False))
        senses = []
        for gloss, joined in cleaned:
            if not gloss:
                continue
            if joined and senses:
                senses[-1] = senses[-1] + " or " + gloss
            else:
                senses.append(gloss)
        entries.setdefault(key, senses)
        entries.setdefault(re.sub(r"\d+$", "", key), senses)
        for word, (host, section, parts, *depth) in FILED_WITHIN.items():
            if key == host:
                entries[word] = filed_within(body, section, parts, *depth)
    read_pointers(entries)
    return entries


def lexicon_senses(entries, lemma, code="", form="", parse=""):
    key = SPELLING.get(beta(lemma), beta(lemma))
    key = entry_key(key, parse)
    if key not in entries:
        return None
    return form_senses(entries[key], re.sub(r"\d+$", "", key), lemma, code, form, parse)


def lsj_senses(lemma, code="", form=""):
    """An LSJ word's senses, by the same NOT_SENSES and FORM_SENSES as Middle Liddell's: LSJ's
    πανοικία gives its dative as an adverb a sense of its own (EXO 1:1), which the nominative of
    GEN 50:8 does not have. A homograph Middle Liddell lacks (LSJ_HOMOGRAPHS) reads here too."""
    if lemma in LSJ_HOMOGRAPHS:
        senses = LSJ_HOMOGRAPHS[lemma][1]
    elif lemma in LSJ:
        senses = LSJ[lemma]
    else:
        return None
    return form_senses(senses, beta(lemma), lemma, code, form)


# BEGIN COVERAGE (generated from the Q24 pass: each card translation a chain left out, sorted into
# a sense, which the chain now carries, or one of these. The reason is the value.)
COVERAGE_NOT = {
    'a(/gios': {
        'the Holy of Holies': 'phrase: τὰ ἅγια τῶν ἁγίων: two words, one name',
    },
    'a(marta/nw': {
        'that I should lose': "piece: 'that I should lose my sight', ἁμαρτήσεσθαι ὀπωπῆς",
    },
    'a)/cios': {
        'duty': "piece: II.3, 'is her duty, to arrest the man'",
    },
    'a)/gw': {
        'took and placed': 'phrase: στῆσε δ᾽ ἄγων',
        'to sweep a country': 'phrase: ἄγειν καὶ φέρειν',
        'things': 'label: prose: φέρειν refers to things',
        'men and cattle)': 'label: prose: ἄγειν to men and cattle',
        'plundering': 'phrase: φέρων καὶ ἄγων',
        'to draw a line of wall': 'phrase: τεῖχος ἄγειν',
        'weighs or draws down: cf': 'label: prose on the accusative of weight',
        'for his son': 'piece: to bring home a wife for his son',
    },
    'a)/kanqa': {
        'thorny': "piece: metaph. ἄκανθαι 'thorny questions': the adjective renders the noun",
    },
    'a)/llos': {
        'one man': 'phrase: ἄλλος ἄλλο λέγει, repeated',
        'one thing, one another': 'phrase: ἄλλος ἄλλο λέγει, repeated',
        'different men say different things': "phrase: ἄλλος ἄλλο λέγει, the sentence's sense",
        'one or two': 'phrase: ἄλλος καὶ ἄλλος',
        'one thing after another': 'phrase: ἄλλο καὶ ἄλλο',
        'alia': 'latin: Lat. cetera, reliqua, not alia',
    },
    'a)/nwqen': {
        'the living': 'phrase: οἱ ἄνωθεν',
        'first principles': 'phrase: τὰ ἄνωθεν',
    },
    'a)/roura': {
        'jugerum': "latin: II, 'nearly = the Roman jugerum'",
        'as bearing children': "label: metaph. of a woman: the entry's description of a use",
    },
    'a)/rxw': {
        'even': 'phrase: ἀρξάμενοι ἀπὸ παιδίων, even from boyhood',
    },
    'a)cio/w': {
        'he deigns': "repeat: εἴ τις ἀξιοῖ μαθεῖν 'if he deigns': 'to deign'",
        'claimed': "repeat: νικᾶν ἠξίουν 'claimed': 'to claim'",
    },
    'a)delfo/s': {
        'gemellus': 'latin: Lat., beside geminus',
    },
    'a)faire/w': {
        'separate, set aside': "phrase: ἀφ. χωρίς: χωρίς carries 'separate'",
    },
    'a)fi/hmi': {
        'to give up to be': "phrase: III.2, ἀφ. τι δημόσιον εἶναι: εἶναι carries 'to be'",
        'she loosed her': "piece: B.2, δειρῆς ἀφίετο πήχεε: 'she' and 'her' are not the word's",
    },
    'a)fikne/omai': {
        'came up': "repeat: μνηστῆρας ἀφ. 'came up to them': the example's past of 'to come up to'",
    },
    'a)kou/w': {
        'to be ill spoken of by': 'phrase: κακῶς ἀκ. πρός τινος',
        'to have evil spoken of': 'phrase: ἀκ. κακά',
        'pers, from whom it is heard': 'label: the construction: gen. of the person',
        'from whom': 'label: the person from whom the thing is heard takes a prep.',
    },
    'a)lhqh/s': {
        'itane? indeed? really? in sooth?': "phrase: ἀληθές; in a question, the sentence's, Latin first",
    },
    'a)lla/ssw': {
        'for': 'piece: «to take» one thing «for» another: restored whole in TEXT_LOST',
    },
    'a)mfo/teros': {
        'from both sides, ex utraque parte': "phrase: ἀπ᾽ ἀμφοτέρων, as 'on both sides, utrinque' already is",
    },
    'a)nabai/nw': {
        'to embark': "repeat: repeats 'go on board, embark'",
    },
    'a)naxwre/w': {
        'to withdraw': "repeat: III, from the world: a piece of 'to retire or withdraw'",
    },
    'a)po/': {
        'without': 'phrase: οὐκ ἀπὸ τρόπου, not without reason',
        'after': "repeat: ἀπὸ δείπνου; repeats 'from, after'",
        'shot from': 'piece: by [arrow shot from] silver bow',
        'less direct': 'label: implying a less direct agency',
        'in earnest, eagerly': 'phrase: ἀπὸ σπουδῆς',
        'equally`': "phrase: cut at validate's 200-char limit; full: equally (ἀπὸ τοῦ ἴσου)",
        'equally': 'phrase: ἀπὸ τοῦ ἴσου, ἀπ᾽ ἴσης',
        'by word of mouth': 'phrase: ἀπὸ γλώσσης',
        'from, asunder': 'label: IN COMPOS.: the prefix, not the preposition',
        'away, off': 'label: IN COMPOS.: the prefix, not the preposition',
        'finishing off, completing': 'label: IN COMPOS.: the prefix, not the preposition',
        'ceasing from, leaving off': 'label: IN COMPOS.: the prefix, not the preposition',
        'back again': 'label: IN COMPOS.: the prefix, not the preposition',
        'in full': 'label: IN COMPOS.: the prefix, not the preposition',
        'by way of abuse': 'label: IN COMPOS.: the prefix, not the preposition',
        "what is one's own": 'label: IN COMPOS., as ἀπέχω: the prefix, not the preposition',
    },
    'a)po/llumi': {
        'to talk or bore': "phrase: λόγοις ἀπ. τινα, to talk or bore one to death: λόγοις says 'talk'",
        'to death': 'piece: «to talk» or «bore» one «to death»: restored whole in TEXT_LOST',
    },
    'a)pobai/nw': {
        '': 'scrap: empty string where the 200-char message cut; later items not listed',
    },
    'a)podi/dwmi': {
        'make atonement for': "phrase: ἀπ. τινι λώβην, 'give him back his insult, i. e. make atonement for it'",
        'to take': "piece: ἀπ. τι ἐς Ἑλλάδα 'to take to Greece and sell it there'",
        'and sell': "piece: ἀπ. τι ἐς Ἑλλάδα 'to take to Greece and sell it there'",
        'back': "repeat: piece of 'to give up or back' and of 'to give him back'",
        'to': "scrap: the validator's report cut this item off after 'to'",
        'to deliver': "repeat: I.5, ἀπ. ἐπιστολήν: repeats 'to deliver over, give up'",
        'to give an account of': "phrase: I.6, λόγον ἀπ.: λόγον carries 'an account'",
        'increase': "repeat: 'if the land increase in height': repeats 'to increase'",
        'decrease': "label: a piece of the entry's explanation",
    },
    'a)pokri/nomai': {
        'to separate, set apart': "deponent: the deponent ἀποκρίνομαι: the active's sense, set aside by name",
        'to mark by a distinctive form, distinguish': "deponent: the deponent ἀποκρίνομαι: the active's sense, set aside by name",
        'to choose out, choose': "deponent: the deponent ἀποκρίνομαι: the active's sense, set aside by name",
    },
    'a)pore/w': {
        'hesitation': 'phrase: οὐκ ἀπορήσας, without hesitation',
    },
    'a)postre/fw': {
        'to avert': "repeat: of 'to turn back, avert'; a danger",
        'bent back': 'piece: to have their beaks bent back',
        'twisted': "piece: to have one's feet twisted",
    },
    'a)riqmo/s': {
        'into my account': "phrase: οὐδ' εἰς ἀριθμὸν ἥκεις, you come not into my account",
        'quality, worth': "label: 'opp. to quality, worth': the contrasting term, not a sense",
        'nos numerus sumus': "latin: Horace's phrase",
    },
    'a)rxh/': {
        'from the beginning, from of old': 'phrase: ἐξ ἀρχῆς',
        'anew, afresh': 'phrase: ἐξ ἀρχῆς πάλιν',
        'in the beginning, at first': 'phrase: κατ᾽ ἀρχάς',
        'absolutely': 'phrase: ἀρχὴν οὐ, absolutely not',
        'at all': 'phrase: ἀρχὴν οὐ, not at all',
        'in all': 'phrase: ἀρχὴν with numerals',
    },
    'a)sfalh/s': {
        'without fail for ever': "phrase: ἔμπεδον ἀσφαλέως: ἔμπεδον says 'for ever'",
    },
    'a)sko/s': {
        'alive, maltreat wantonly': "phrase: proverb. ἀσκὸν δείρειν τινά 'to flay one alive, maltreat wantonly'",
    },
    'ai(=ma': {
        'akin': 'phrase: ἐν αἵματι, akin by blood',
    },
    'ai)ti/a': {
        'to be accused': 'phrase: αἰτίαν ἔχειν',
        'as their characteristic': "piece: a piece of an example's translation",
    },
    'ai)w/n': {
        'posterity': 'phrase: ὁ μέλλων αἰών',
        'of old, for ages': "phrase: ἀπ' αἰῶνος",
        'for ever': "phrase: τὸν δι' αἰῶνος χρόνον; εἰς τοὺς αἰῶνας",
    },
    'au)/rion': {
        'on the morrow or till morning': 'phrase: ἐς αὔριον',
    },
    'au)to/s': {
        'body': 'label: the opposed term: not the body',
        'others': 'label: the opposed term: opp. to others',
        'alo': "repeat: cut at validate's 200-char limit; full: alone, which repeats 'by oneself, alone'",
        'alone': "repeat: repeats 'by oneself, alone'",
        'among friends': 'phrase: αὐτοί ἐσμεν, we are by ourselves',
        'in hand': 'phrase: αὐτῇ σὺν φόρμιγγι, lyre in hand',
        'only in oblique cases': 'label: a grammatical label',
        'sameness': 'label: to denote sameness',
        'natural, native, not made': 'label: αὐτο- IN COMPOS.: the prefix',
        'of mere . . , of nothing but . .': 'label: αὐτο- IN COMPOS.: the prefix',
        'of oneself, self-': 'label: αὐτο- IN COMPOS.: the prefix',
        'independently': 'label: αὐτο- IN COMPOS.: the prefix',
        'just, exactly': 'label: αὐτο- IN COMPOS.: the prefix',
    },
    'bapti/zw': {
        'over head and ears': 'phrase: ὀφλήμασι βεβαπτισμένος, over head and ears in debt',
    },
    'bo/trus': {
        'a flash of lightning': 'phrase: βόστρυχος: πυρὸς β., of a flash of lightning: πυρός says the fire',
    },
    'cu/lon': {
        'the front bench': 'phrase: πρῶτον ξύλον',
    },
    'de/': {
        'adversative': 'label: with adversative force',
        'then': "repeat: after 'then, yet'",
        'si tu oblitus es, at Dii meminerint': 'latin: Latin parallel',
    },
    'de/xomai': {
        'expect': "repeat: μηδὲ συμφορὰν δέχου: repeats 'to expect'",
    },
    'dh/': {
        'many times and oft': "phrase: πολλάκις δή: πολλάκις carries 'many times'",
        'like me': "phrase: ἐμὲ δή «a» man «like me»: ἐμέ carries 'me'",
        'one or other': "phrase: δή τις some 'one or other', Lat. nescio quis: τις carries 'one'",
        'whatever it be': "phrase: δή τι: τι carries 'whatever'",
        'so then': "repeat: II.2, καὶ σὺ δή; repeats 'so then, so'",
        'a fortiori': "latin: II.4, γε δή to express what follows 'a fortiori'",
        'above all': 'phrase: γε δή, καὶ δή',
        'what is more': 'phrase: καὶ δή',
        'now suppose': 'phrase: καὶ δή in assumptions',
        'be they who they may': "phrase: οἵτινες δή: the phrase's",
    },
    'di/dwmi': {
        'having indulged': 'phrase: ὀργῇ χάριν δούς',
        'to deliberate': 'phrase: δ. λόγον ἑαυτῷ',
        'to wife': 'piece: to give their daughter to wife',
        'up': 'piece: to give oneself up',
    },
    'di/kaios': {
        'quite exactly': 'phrase: τῷ δικαιοτάτῳ τῶν λόγων',
        'use': "piece: of 'fit for another's use'",
        'are bound': 'construction: C, δίκαιός εἰμι with inf., δίκαιοί ἐστε ἰέναι',
        'have reason': 'construction: C, δίκαιός εἰμι with inf.',
        'dignus est qui pereat': 'latin: C, Latin of δ. ἐστιν ἀπολωλέναι',
        'have a right': 'construction: δίκαιός εἰμι c. inf.',
    },
    'dia/noia': {
        'regards the sense': 'phrase: τῇ διανοίᾳ as «regards the sense»: the dative as a phrase',
    },
    'diati/qhmi': {
        'by will': 'piece: «devise» it «by will»: restored whole in TEXT_LOST',
    },
    'dida/skalos': {
        'school': 'phrase: εἰς διδασκάλου φοιτᾶν, to go to school',
        'taught the actors': 'label: why a dramatic poet was called διδάσκαλος',
    },
    'die/rxomai': {
        'shot through': "repeat: of 'to shoot through'; a thought shot through me",
    },
    'do/ca': {
        'to imagine, suppose': 'phrase: I.3, δόξῃ ἐπίστασθαι',
    },
    'doke/w': {
        'videtur mihi, I seem to myself, methinks': "phrase: I.3 δοκῶ μοι: μοι carries 'to myself'; Lat. videtur mihi",
        'to seem, as opp, to reality': "label: II.2 absol.: 'as opp. to reality' is the entry's prose; «to seem» is on the card already",
        'it seems to me, meseems, methinks': 'construction: II.4 impers., δοκεῖ μοι',
        'placuit senatui`': 'latin: cut from «placuit senatui»: Latin of ἔδοξε τῇ βουλῇ',
        '': 'latin: Latin of ἔδοξε τῇ βουλῇ',
    },
    'dw=ron': {
        'receiving presents': 'phrase: δώρων ἑλεῖν, the genitive of the charge',
    },
    'dwre/w': {
        'to make': "piece: of 'to make presents': the run cut by its object",
    },
    'e(/teros': {
        'after to-morrow': 'phrase: ἡ ἑτέρα (sc. ἡμέρα), day after to-morrow',
        'malus': 'latin: Lat. sequior for malus',
        'with one hand': 'phrase: τῇ ἑτέρᾳ (sc. χειρί)',
        'with the left hand': 'phrase: τῇ ἑτέρᾳ (sc. χειρί)',
        'on the next day': 'phrase: sub. ἡμέρᾳ',
        '2n another or a different way': 'phrase: sub. ὁδῷ',
        'to or on': "phrase: cut by validate's cap: 'to or on the other side', ἐπὶ θάτερα",
        '2n another or a different way`': "phrase: = '2n another or a different way' with the cut's backtick; sub. ὁδῷ",
        'to or on the other side': 'phrase: IV.2.a, ἐπὶ θάτερα',
        'on the one or other side': 'phrase: IV.2.b, κατὰ θάτερα',
    },
    'e)/cwqen': {
        'foreigners': 'phrase: οἱ ἔξωθεν',
        'matters outside the house': 'phrase: τὰ ἔξωθεν',
    },
    'e)/mprosqen': {
        'forwards': 'phrase: I.1, εἰς τὸ ἔμπ.',
        'opposite': 'phrase: I.1, ἐκ τοῦ ἔμπρ.',
    },
    'e)/rgon': {
        'hominumque boumque labores)': 'latin: Virgil',
        'the tilled lands': "repeat: ἔργα Ἰθάκης; repeats 'tilled lands'",
        'fis': "phrase: cut at validate's 200-char limit; full: fishing (θαλάσσια ἔργα, the adjective carries the sea)",
        'fishing': 'phrase: θαλάσσια ἔργα, the adjective carries the sea',
        'there is need of, use of': 'construction: ἔργον ἐστί c. gen. rei',
        'it is hard work, difficult': 'construction: ἔργον ἐστί c. inf.',
        "of women's work, weaving": "label: the entry's label for a use",
        'his business, his proper work': 'construction: ἔργον ἐστί c. gen. pers.',
        'use': "construction: οὐκ ἔργον c. inf., 'tis no use",
    },
    'e)/rxomai': {
        'I go to': 'construction: c. part. fut., ἔρχομαι οἰσόμενος: the participle carries the purpose',
        'I am going to': 'construction: c. part. fut., ἔρχομαι λέξων',
        'I intend': 'construction: c. part. fut., ἔρχομαι λέξων',
        'to come within a little of, be near': 'phrase: παρὰ μικρὸν ἐλθεῖν',
    },
    'e)/sxatos': {
        'worst of possible': "phrase: ἔσχατ' ἐσχάτων κακά",
        'for the last time': 'phrase: τὸ ἔσχατον, adverbial',
    },
    'e)/ti': {
        'and besides, nay more': 'phrase: ἔτι δέ',
    },
    'e)/xw': {
        'the poor': 'phrase: οἱ οὐκ ἔχοντες: the negative carries it',
        'kept and made much of': 'phrase: ἔχων ἀτίταλλε, the participle with another verb',
        "tenes? d' ye understand": "phrase: ἔχεις τι; the question's rendering, with Latin tenes",
        'attend to this': "phrase: δεῦρο νοῦν ἔχε: νοῦν carries 'attend'",
        'I know not': "phrase: οὐκ ἔχω ὅπως: the negative carries 'not'",
        'to be well off for': "phrase: εὖ ἔχειν τινός: εὖ carries 'well'",
        'abound in': 'phrase: εὖ ἔχειν τινός',
        'I am in a state': 'construction: θαυμάσας ἔχω: ἔχω with aor. part. as periphrasis',
        'duration': "label: the part. ἔχων adds a notion of 'duration'",
        'he aimed': "piece: an example's translation",
        'he held his course': "piece: an example's translation",
        'he could not': "piece: an example's translation",
        'the case stands': 'phrase: πῶς ἔχει, how the case stands',
        'by': 'piece: to hold him by the hand',
        'will': 'piece: οὐ σχήσει, will not withhold',
        'I will hold fast': "repeat: ἕξω, an example of 'to hold oneself'",
        'you keep': 'piece: ληρεῖς ἔχων, you keep chattering',
        'the neighbouring people': 'construction: οἱ ἐχόμενοι, the participle with the article',
    },
    'e)a/n': {
        'whosoever': 'phrase: ὃς ἐάν',
    },
    'e)a/w': {
        'to forbid, hinder, prevent': 'phrase: οὐκ ἐᾶν: οὐκ says the negation',
    },
    'e)cani/sthmi': {
        'to order': "piece: of 'to order the men in ambush to rise' (cf. 'bid one … rise')",
        'from their lair': "piece: of 'to rouse them from their lair'",
    },
    'e)ce/rxomai': {
        'turn out': "repeat: of 'to turn out'",
    },
    'e)chge/omai': {
        'the way, go before, lead': 'piece: «to shew» one «the way, go before, lead»: restored whole in TEXT_LOST',
    },
    'e)k': {
        'with all': 'phrase: ἐκ θυμοῦ, with all my heart',
        'change from': 'label: to denote change from',
        'after)': "repeat: κακὸν ἐκ κακοῦ, from (or after); repeats 'after'",
        'from a number': 'label: to express distinction from a number',
        'with water from': 'piece: washed his body with water from the river',
        'to hang or fasten': 'label: with Verbs signifying to hang or fasten',
        'sitting or standing': 'label: with verbs of sitting or standing',
        'just finished': 'phrase: ἐκ θυσίας γενέσθαι',
        'built by': "piece: cut at validate's 200-char limit; full: built by them (walls built by them)",
        'built by them': "piece: walls built by them; 'built' supplied",
        'wherefore?': 'phrase: ἐκ τίνος; ἐκ τοῦ;',
    },
    'e)kba/llw': {
        'from the stage': "piece: of 'to drive an actor from the stage'; validate's cap cut the list after it",
    },
    'e)kei=nos': {
        'ille': 'latin: Latin',
        'hic': 'latin: Latin',
        'the nearer': 'label: describes οὗτος',
        'the latter.': 'label: describes οὗτος',
        'that time': 'phrase: ἐξ ἐκείνου, from that time',
        'th': "phrase: cut at validate's 200-char limit (GEN 2:12); full: that place, there (κατ᾽ ἐκεῖνα)",
        'that place, there': 'phrase: κατ᾽ ἐκεῖνα',
        'afterwards': 'phrase: μετ᾽ ἐκεῖνα',
    },
    'e)klei/pw': {
        'and go': "piece: elliptic phrase, «to abandon» the city «and go» to the heights: εἰς's",
        'the deceased': 'construction: οἱ ἐκλιπόντες, the participle with the article',
        'incomplete': "piece: an example's adjective",
    },
    'e)mo/s': {
        'for my part, as far as concerns me': 'phrase: τὸ ἐμόν, τοὐμόν, adverbial',
        'my country': "phrase: ἡ ἐμή, sc. γῆ, the ellipsis's",
    },
    'e)nanti/os': {
        'the very reverse': "phrase: τὰ ἐν. τούτων, an example's rendering",
        'exactly opposed': 'phrase: II.3, ἐναντίως ἔχειν, of the adverb ἐναντίως',
    },
    'e)piba/llw': {
        "it falls to one's very lot, it concerns one": 'construction: impers. c. acc. et inf.',
        'with their arrows on the string': 'phrase: ἐπιβεβλημένοι τοξόται',
    },
    'e)pife/rw': {
        'to the grave': 'piece: to bring offerings to the grave',
        'against': 'piece: to bring as a charge against',
    },
    'e)pikale/w': {
        'charge?': "piece: 'is this your charge?'",
        'he was charged with having': 'piece: a Pass. example, τὰ ἐπικαλεύμενα χρήματα',
    },
    'e)pimelh/s': {
        'business': 'phrase: ἐπιμελές μοι ἦν, it was my business',
    },
    'e)piskeua/zw': {
        'upon': "piece: ἐφ' ἁμαξῶν: ἐπί, not the verb",
    },
    'e)piti/qhmi': {
        'as a door': "piece: λίθον ἐπέθηκε θύρῃσιν, 'put a stone as a door to the cave'",
        'before': "piece: 'put it before the door'",
    },
    'ei(/s': {
        'nullus unus': 'latin: Latin',
        'single man': "piece: εἷς οὐδείς, no single man; 'man' supplied",
        'singly': 'phrase: καθ᾽ ἓν ἕκαστον',
        'alternately': 'phrase: παρ᾽ ἕνα',
        'one, as opp, to': "label: 'one' with the label 'as opp. to'",
        'another;': 'label: the opposed term',
        'faber unus': 'latin: Latin',
        'by himself': 'phrase: εἷς ἕκαστος, each by himself',
        'one by one': 'phrase: καθ᾽ ἕνα, καθ᾽ ἕν',
    },
    'ei)mi/': {
        'appearing to be': 'label: to be, opp. to appearing to be',
        'esse': 'latin: Latin',
        'videri': 'latin: Latin',
        'no one': 'construction: οὐκ ἔστιν ὅς',
        'some things': 'construction: ἔστιν ἅ',
        'somewhere': 'construction: ἔστιν ὅπη, ἔσθ᾽ ὅπου',
        'somehow': 'construction: ἔστιν ὅπη, ἔσθ᾽ ὅπου',
        'in some manner': 'construction: ἔστιν ὅπως',
        'sometimes': 'construction: ἔστιν ὅτε',
        'it is possible': 'construction: ἔστι impers. c. inf.',
        'quantum in illis esset': 'latin: Latin',
    },
    'ei)s': {
        'to come before': "piece: λόγους ποιεῖσθαι εἰς τὸ πλῆθος; the verb carries 'come'",
        'aedem);': 'latin: ad Castoris (sc. aedem)',
        'up to': "repeat: repeats 'to, up to, until'",
        'until': "repeat: repeats 'to, up to, until'",
    },
    'ei)sa/gw': {
        "into one's house, ducere uxorem": "piece: «to lead» a wife «into one's house», with Latin ducere uxorem: a piece of the example, γυναῖκα carrying 'wife'",
        'into court': 'piece: «to bring» a cause «into court»; the whole follows as «to bring into court, prosecute»',
    },
    'ei)se/rxomai': {
        "it comes into one's head": 'construction: impers., εἰσῆλθε αὐτόν, c. inf.',
    },
    'eu(ri/skw': {
        'make themselves': 'phrase: τὰ ἔργα τοὺς λόγους εὑρίσκεται',
        'having fetched': "repeat: repeats 'to fetch, earn'",
        'for what it will fetch': 'phrase: τοῦ εὑρόντος',
    },
    'eu)=': {
        'greatness, abundance, prosperity, easiness': 'label: IV in Compos., what εὖ- implies in compounds',
    },
    'eu)logi/a': {
        'of the alms collected': "label: the entry's label for a use",
    },
    'eu)qu/nw': {
        'straight': 'piece: «to steer» the bark «straight», «to make» crooked judgments «straight»',
        'to make': 'piece: «to make» crooked judgments «straight»',
        'call': 'piece: «call» him «to account»: the next translation says it whole',
        'to account': 'piece: «call» him «to account»',
    },
    'fai/nw': {
        '': "scrap: an empty item: the validator's report cut here",
        'a thing appears to be': "label: prose: 'φαίνεσθαι c. inf. indicates that a thing appears to be so and so'",
        'that it manifestly is': "label: prose: 'φαίνεσθαι c. part. states the fact that it manifestly is so and so'",
        'manifestly harms': "piece: φαίνεται ὁ νόμος βλάπτων: βλάπτων carries 'harms'",
        'appears likely to harm': "piece: φαίνεται … βλάψειν: βλάψειν carries 'likely to harm'",
        'nullo in loco haberi': 'latin: B.II.3, Latin of οὐδαμοῦ φανῆναι',
        'yes': "phrase: φαίνεται, the answer's",
        'does this appear': "piece: an example's question",
        'do I look like': 'phrase: τί φαίνομαι; what do I look like',
    },
    'fanero/s': {
        'openly': 'phrase: ἐκ τοῦ φανεροῦ, with a prep. in adverb sense',
    },
    'fe/rw': {
        'to work': "repeat: of 'to bring, produce, work, cause'",
        'due or owing': "piece: of 'to pay something due or owing'",
        "which one gets for one's own use": "label: prose: 'the Mid. being used of that which one gets for one's own use'",
        'ducit ad . .': 'latin: Lat. via fert or ducit ad',
        'spectare ad . .': 'latin: Lat. vergere or spectare ad',
        'inclined to': "repeat: ἡ γνώμη ἔφερε συμβάλλειν: repeats 'inclines'",
        'it tends': 'construction: VII.3.c, impers., much like συμφέρει',
        'is conducive': 'construction: VII.3.c, impers. φέρει',
        'take': 'phrase: βαρέως φέρειν, take ill: with adverbs',
        'to have': 'piece: ἔπος φέρεσθαι, to have word brought one',
        'brought one, receive': 'piece: ἔπος φέρεσθαι, to have word brought one',
        'to be': 'piece: εὖ φέρεσθαι, to be well spoken of',
        'what': 'piece: τὸ φέρον, what heaven bears to you',
        'bears to you, awards you': "piece: an example's rendering of τὸ φέρον",
    },
    'file/w': {
        'she kissed': "piece: 'the kiss wherewith she kissed him'",
        'is wont': "repeat: 'as is wont': 'to be wont'",
        'it is usual': 'construction: II.2, impers., ὡς δὴ φιλεῖ',
    },
    'fobe/w': {
        'to flee': "repeat: repeats 'to be put to flight, to flee affrighted, flee'",
    },
    'fobero/s': {
        'gave cause for fear': 'phrase: φοβεροὶ ἦσαν μή: ἦσαν carries the verb',
        'reason to dread': 'construction: I.2, φοβερόν [ἐστι] μή',
    },
    'fu/w': {
        'to get': "repeat: A 4, φρένας φύειν: a piece of 'to grow or get'",
        'not formed': "phrase: φύσει μὴ πεφυκότα: μή says 'not'",
        'is putting forth scions': "repeat: an example of 'to put forth shoots'",
    },
    'fula/ssw': {
        'I will take care': "piece: εἰσορῶν φυλάξομαι, an example's",
        'by one, bear': 'piece: to keep a thing by one, bear it in mind',
        'in mind': 'piece: to keep a thing by one, bear it in mind',
    },
    'futeu/w': {
        'with fruit-trees': 'piece: to plant ground with fruit-trees',
    },
    'fwne/w': {
        'making': 'piece: ὄπα φωνήσασα, «making» the voice «sound»',
        'sound': 'piece: ὄπα φωνήσασα, «making» the voice «sound»',
        'to have the': 'piece: μέγιστα φωνέειν, «to have the» loudest «voice»',
        'voice': 'piece: μέγιστα φωνέειν, «to have the» loudest «voice»',
    },
    'fwnh/': {
        'an articulate sound': "repeat: φωνὴν ῥηγνύναι; the same as 'any articulate sound'",
    },
    'ga/r': {
        'but': "phrase: ἀλλὰ γάρ: ἀλλά carries 'but'",
        'would that': 'phrase: πῶς γάρ, εἰ γάρ, in wishes',
    },
    'genea/': {
        'by birth-right': 'phrase: γενεῇ, the dative as a phrase',
        'by descent': 'phrase: γενεὴν Αἰτωλός, acc. of respect',
        'in kind': 'phrase: γενεήν, acc. of respect',
    },
    'gerousi/a': {
        'the ambassadors': "label: πρεσβεία's note, 'the ambassadors of early times were elders': prose, not a sense",
    },
    'gi/gnomai': {
        'born': "repeat: νέον γεγαώς; repeats 'to be born'",
        'turning': 'phrase: πάντα γιγνόμενος, turning every way',
        'am I to become': 'phrase: τί γένωμαι;',
        'it went': 'construction: impers. with adverbs, κακῶς ἐγένετό μοι',
        'it goes': 'construction: impers. with adverbs, εὖ γίγνεται',
    },
    'gignw/skw': {
        'was aware of': "repeat: repeats 'were aware of'",
        'thou mayst discern': "repeat: an example of 'to discern'",
        'I felt that I was': "piece: ἔγνων ἡττημένος, an example's rendering",
        'that he may learn how to': "piece: ἵνα γνῷ, the example's: ἵνα carries 'that'",
    },
    'h(/kw': {
        'to be gone': 'label: glosses οἴχομαι, set against ἥκω',
        'to come or go': 'label: glosses ἔρχομαι',
        'off for': 'phrase: εὖ ἥκειν τινός',
        'have plenty of': 'phrase: εὖ ἥκειν τινός',
        'off': 'phrase: εὖ ἥκειν, absol.',
    },
    'h(me/ra': {
        'in daytime': 'phrase: τὰς ἡμέρας',
        'sufficient for the day': 'phrase: ἐφ᾽ ἡμέραν',
        'day by day, daily': 'phrase: τοὐφ᾽ ἡμέραν, καθ᾽ ἡμέραν',
        'every day': 'phrase: τὸ καθ᾽ ἡμ.',
        'day-break': 'phrase: ἅμα ἡμέρᾳ and the phrases for day-break',
        'on': "piece: τῇδε τῇ ἡμέρᾳ, on this day: the dative's English, which its marker says",
        'within': "piece: ἡμερῶν ὀλίγων, within a few days: the genitive's English, which its marker says",
        'day by day': 'phrase: τοὐφ᾽ ἡμέραν',
    },
    'h)/': {
        'sooner than . .': "phrase: φθάνειν ἤ: φθάνω carries 'sooner'",
    },
    'i(/na': {
        'in which case he must be': 'phrase: ἵν᾽ ἦν τυφλός',
        'ne': 'latin: Lat. ut ne or ne',
        '[I tell thee this] that': 'phrase: elliptical; the bracket supplies the verb',
        'to what end?': 'phrase: ἵνα τί',
        'see that': 'phrase: elliptical, ὅρα or βλέπε understood',
    },
    'i(/sthmi': {
        'to stir up': 'repeat: φυλόπιδα στήσειν, repeats «to raise, rouse, stir up»',
        'against': "piece: «to weigh» one thing «against» another: πρός's",
        'two': "piece: the month divided into «two» parts: the entry's account of the calendar",
        'three': "piece: fell into «three» decads: the entry's account of the calendar",
    },
    'i(kano/s': {
        'far enough': 'phrase: III.2, ἱκ. ἔχειν',
    },
    'i(ma/s': {
        'leash': "repeat: ἱμὰς κύνειος, a proverb's: 'a dog-leash' again",
    },
    'i)sxu/s': {
        'perforce': "phrase: κατ' ἰσχύν",
    },
    'ka/kwsis': {
        'for ill-usage or neglect of parents': 'phrase: δίκη κακώσεως, an action for ill-usage',
    },
    'kai/': {
        'both': "piece: τε . . καί, both . . and: 'both' renders τε",
    },
    'kairo/s': {
        'measure, unduly': 'phrase: καιροῦ πέρα',
        'in season, at the right time, opportune': 'phrase: εἰς καιρόν',
        'prematurely': 'phrase: πρὸ καιροῦ',
    },
    'kako/s': {
        'a sorry': "repeat: κ. ἀλήτης, a sorry beggar: repeats 'sorry'",
        'already signi': 'label: cut from «already signifying something bad»: E in Compos.',
        'already signifying something bad': 'label: E in Compos., what κακο- does to a compound',
        'signifying something good': 'label: E in Compos., what κακο- does to a compound',
    },
    'kale/w': {
        'a supposititious': 'piece: καλεῖ με πλαστόν, calls me a supposititious son',
        'shall be given': 'piece: a name shall be given to thy tomb: the name the subject',
        'I am': 'piece: an example of κέκλημαι = εἰμί',
        'were to be': 'piece: an example of κέκλημαι = εἰμί',
        'is': 'piece: an example of κέκλημαι = εἰμί',
        'called': 'repeat: κέκληται, where is the hill called',
    },
    'kalo/s': {
        'in good time, in season': 'phrase: ἐν κ. (sub. χρόνῳ)',
        'noble': "repeat: καλὰ ἔργματα; repeats 'beautiful, noble'",
        'honestum': "latin: Cicero's",
        'turpe': "latin: Cicero's",
        'beautiful': "repeat: καλὸς δέμας 'beautiful of form'",
        'in a good': "phrase: ἐν καλῷ [τόπῳ] 'in a good place'",
        'h': "latin: cut at validate's 200-char limit (GEN 2:9); full: honestum",
        '': "scrap: an empty item: the validator's report cut here",
    },
    'kaqi/sthmi': {
        "to get one's": "piece: τὴν ζόην καταστήσασθαι, to get one's living",
        'middle': 'piece: ἡ καθεστηκυῖα ἡλικία, middle age',
        'presence': 'piece: to stand in his presence',
    },
    'kardi/a': {
        'freely': 'phrase: τἀπὸ καρδίας λέγειν, Lat. ex animo',
    },
    'katalamba/nw': {
        'it happens to': 'construction: II.3 impers., καταλαμβάνει τινά, c. inf.',
        'fortune': "construction: II.3 impers., «it is» one's «fortune» to do",
        'inquiries about': "piece: ὁ θάνατος καταλαμφθείς, «inquiries about» the death «being checked»: the sentence's",
        'forces': 'repeat: ἀναγκαίη μιν κ. φαίνειν; repeats «to force or compel»',
        'to get': 'piece: κ. τὸ πῦρ, to get it under',
        'under': 'piece: κ. τὸ πῦρ, to get it under',
    },
    'kate/xw': {
        'conquest': "piece: A.II.7, 'to occupy, in right of conquest'",
    },
    'kefalh/': {
        'head foremost, head downwards, headlong': 'phrase: ἐπὶ κεφαλήν',
    },
    'khru/ssw': {
        'he gives notice, proclamation is made': 'construction: impers., κηρύσσει (sc. ὁ κῆρυξ)',
    },
    'klai/w': {
        'I shall mourn': 'construction: II, impers. pass., μάτην ἐμοὶ κεκλαύσεται',
    },
    'kle/ptw': {
        "thief's": "piece: κλέπτον βλέπει 'he has a thief's look', as 'thievish' already is",
    },
    'kli=mac': {
        'leaning aslant)': "label: etymology: 'because of its leaning aslant'",
        'entanglement': "label: III, prose: 'to express the entanglement of the limbs of wrestlers'",
        'abiit, evasit, erupit.': "latin: IV, Cicero's example 'abiit, evasit, erupit'",
    },
    'ko/ptw': {
        'to': "scrap: the validator's report cut this item off after 'to'",
    },
    'ko/smos': {
        'order, duly': 'phrase: κόσμῳ, κατὰ κόσμον, in order, duly',
        '"the world,"': "label: as we use 'the world'",
    },
    'koi=los': {
        'the vale': 'phrase: κοίλη Λακεδαίμων, the vale of L.: the name makes the noun',
    },
    'komi/zw': {
        'to recover': "repeat: κομίζεσθαι χρήματα: repeats 'to get back for oneself, recover'",
    },
    'korufh/': {
        'best of all': "phrase: παντὸς ἔχει κορυφάν: παντός says 'of all'",
    },
    'ku/rios': {
        'I have authority': 'construction: κύριός εἰμι c. inf.',
        'am entitled': 'construction: κύριός εἰμι c. inf.',
    },
    'kwlu/w': {
        'hindrance': "piece: 3, Pass., μηδὲ δαπάνῃ κεκωλύσθω 'and let there be no hindrance'",
        'nothing hinders, be it so': 'phrase: 5, οὐδὲν κωλύει, absol., as a form of assent',
    },
    'lamba/nw': {
        'whole': 'piece: the whole in acc.',
        'part': 'piece: with gen. of part only',
        'to catch it': 'phrase: λ. δίκην, as we say',
        'added': 'piece: having battlements added',
        'seized': 'label: the part seized in gen.',
        'by': 'piece: caught her by the wing: the genitive of the part',
        'so and so': 'piece: to take a thing so and so',
        'suffer': 'phrase: λ. δίκην, to receive, i.e. suffer, punishment',
        '"to take': "repeat: 'to take a cold': a repeat, with the entry's quotation mark",
        'having': 'piece: having battlements added',
    },
    'le/gw': {
        'to say something': "phrase: λ. τι; τι carries 'something'",
        'to speak to the point or purpose': 'phrase: λ. τι',
        'am I right': 'phrase: λέγω τι;',
        'meaning': 'piece: οὐδὲν λέγει, has no meaning',
        'authority': 'piece: οὐδὲν λέγει, has no authority',
        'to say what is not, to lie': 'phrase: οὐδὲν λέγειν',
        'mean?': 'scrap: what does this mean?',
        'mean you': 'phrase: πῶς λέγεις; how mean you?',
        'as the saying goes': 'phrase: τὸ λεγόμενον',
        'has': 'piece: οὐδὲν λέγει, has no meaning',
        'does': 'piece: τί τοῦτο λέγει; what does this mean',
        'they are said': "repeat: λέγονται: 'to say' in the passive, which the passive chain says",
    },
    'li/an': {
        'aye truly, verily': 'phrase: strengthened καὶ λίην',
    },
    'lo/gos': {
        "talking's": "phrase: λόγου ἕνεκα, for talking's sake",
        'in word, in pretence': 'phrase: λόγῳ, the dative opp. to ἔργῳ',
        'ground?': "repeat: ἐκ τίνος λόγου; repeats 'a reason, ground, plea'",
        'it stands to reason that . .': 'phrase: B.4, ὁ λόγος αἱρεῖ c. acc. et inf.',
        'account': "repeat: λόγου οὐδενὸς γενέσθαι: repeats 'account, consideration, esteem, regard'",
        'account of': "repeat: λόγου ποιεῖσθαι 'to make account of': repeats 'account'",
        'to be reckoned': "phrase: ἐν ἀνδρὸς λόγῳ εἶναι: εἶναι carries 'to be'",
        'Thought': "label: prose: 'comprising both senses of Thought and Word', i. e. A and B",
    },
    'logi/zomai': {
        'set down': 'repeat: to spend 3 minae and «set down» 12; repeats «to set down»',
    },
    'lumai/nomai': {
        'used to murder': 'piece: ἐλυμαίνου, the speeches you used to murder',
    },
    'ma/la': {
        'more than': "phrase: παντὸς μᾶλλον: the genitive carries 'than'",
        'a fortiori`': 'latin: cut from «a fortiori»: τὸ μ. καὶ ἧττον, a form of argument, in Latin',
        'for the most part, mostly': 'phrase: ἐς τὰ μάλιστα',
        'especially, as much as any': 'phrase: ἐν τοῖς μάλιστα',
        'most certainly': 'phrase: καὶ μάλιστα, in answers',
        'a fortiori': 'latin: II.6, τὸ μ. καὶ ἧττον, a form of argument, in Latin',
    },
    'ma/xaira': {
        "with the rasor's": "piece: μιᾷ μαχαίρᾳ 'with the rasor's single blade'",
        'scissars': "phrase: διπλῆ μ. 'scissars': διπλῆ carries it",
    },
    'mai=a': {
        'mother': 'piece: «a» true «mother»: restored whole in TEXT_LOST',
    },
    'me/gas': {
        'to greatness': "piece: μέγας ηὐξήθη, 'rose to greatness'",
        'le grand monarque': 'latin: French, for βασιλεὺς ὁ μέγας',
        'of great importance': 'phrase: μέγα ποιεῖσθαί τι, to esteem of great importance',
        'by far': 'phrase: μέγα, μεγάλα as adverbs with a comparative',
        'far': "phrase: piece of 'by far', the adverbial neuter",
    },
    'me/n': {
        'begin': 'label: μενοῦνγε, to «begin» a sentence: usage prose',
    },
    'me/ros': {
        'proportion': "phrase: II, πρὸς μέρος 'in proportion'",
        'my or thy part': "phrase: III, τοὐμὸν μέρος, τὸ σὸν μ.: the possessives carry 'my', 'thy'",
        'I or me, thou or thee': "phrase: III, τοὐμὸν μέρος, 'i. e. simply I or me'",
        'in the class of . .': 'phrase: IV.2, ἐν μέρει τινὸς τιθέναι',
    },
    'me/sos': {
        'moderate or neutral': 'phrase: οἱ διὰ μέσου',
        'intervening': 'phrase: οἱ ἐν μ. λόγοι',
        'went between': 'phrase: τὰ ἐν μ.',
        'for all to contend for`': "phrase: cut at validate's 200-char limit; full: for all to contend for (ἐν μέσῳ)",
        'for all to contend for': 'phrase: ἐν μέσῳ',
        'before all': 'phrase: ἐς μέσον',
        'in public': 'phrase: ἐς τὸ μέσον',
        'in common to all': 'phrase: ἐς μέσον',
        'clear of': 'phrase: ἐκ τοῦ μέσου',
        'meanwhile': 'phrase: διὰ μέσου, of time',
        'by the middle, by the waist': 'phrase: μέσον ἔχειν, λαβεῖν',
    },
    'mei/s': {
        'nimbus or glory': "label: μηνίσκος: prose comparison, 'like the nimbus or glory of Christian Saints'",
    },
    'mei/s/mh/n': {
        'and see . . , here comes . . ;': 'phrase: καὶ μήν, marking an entrance on the stage',
        'quid vero?': 'latin: Latin of τί μήν;',
        'well, but how . . ?': "phrase: πῶς μήν; πῶς carries 'how'",
    },
    'metati/qhmi': {
        'to adopt a new': "piece: of 'to adopt a new opinion', Mid. τὴν γνώμην",
    },
    'mh/': {
        'fear or apprehension': 'label: after Verbs expressing fear or apprehension',
    },
    'mh/n': {
        'quid vero?': 'latin: Latin',
        'well, but how . . ?': "phrase: ἀλλὰ πῶς μήν, a phrase's",
        'and see . . , here comes . . ;': "phrase: καὶ μήν, the phrase's",
        'then?': "phrase: τί μήν; the question's",
    },
    'mh/pote': {
        'nescio an': "latin: Lat., beside 'perhaps'",
    },
    'mh/thr': {
        "mother's womb": 'phrase: ἀπὸ or ἐκ μητρός',
    },
    'mh=kos': {
        'long': "piece: μ. λόγου, 'a long speech'",
        'at length, in full': 'phrase: ἐς μῆκος, adverbial',
    },
    'mi/gnumi': {
        'upon': "piece: πότμον μῖξαί τινι 'to bring death upon him'",
        'win': "piece: a piece of an example's translation",
    },
    'mikro/s': {
        'shortly': 'phrase: ἐν σμικρῷ (sc. χρόνῳ)',
        'but a little': 'phrase: ἐπὶ σμικρόν',
        'into small pieces': 'phrase: κατὰ μικρόν',
        'within a little': 'phrase: παρὰ μικρόν',
        'within an ace': 'phrase: παρὰ μ. ἐλθεῖν, c. inf.',
        'but a lit': 'phrase: cut from «but a little»: ἐπὶ σμικρόν',
        'little by little': 'phrase: κατὰ μικρὸν ἀεί',
        'for a little, cheap': 'phrase: μικροῦ, the genitive of price',
    },
    'mimnh/skw': {
        'with good heed, let him remember': "phrase: ὧδέ τις μεμνημένος μαχέσθω, the sentence's free rendering",
        'aloud': 'piece: «to remember» a thing «aloud», i.e. to mention',
    },
    'mo/nos': {
        'without': "piece: μόνος c. gen., 'alone, without' — the genitive carries it",
    },
    'ne/os': {
        'a youth': 'phrase: ἐκ νέου from «a youth»',
        'youth upwards': 'phrase: ἐκ νέου from «youth upwards»',
        'anew, afresh': 'phrase: ἐκ νέας, Lat. denuo',
    },
    'ni/zw': {
        'bathing': 'label: usage note: λούομαι is used of «bathing»',
        'washing clothes': 'label: usage note: πλύνω of «washing clothes»',
        'he washed': "piece: an example's verb",
    },
    'no/mos': {
        'by custom, conventionally': 'phrase: νόμῳ, the dative as an adverb',
    },
    'nu/c': {
        'while it was': 'piece: νυκτὸς ἔτι «while it was» still «night»',
        'the livelong night': 'phrase: νύκτα, the accusative of time as a phrase («the night» long)',
        'midnight': 'phrase: μέσαι νύκτες, μέσος carries the mid',
        'towards': "piece: εἰς νύκτα «towards» night: the preposition's",
        'night-fall': 'phrase: ὑπὸ νύκτα, ἐκ νυκτός: the preposition makes it the fall of night',
    },
    'o(/moios': {
        'tit': "phrase: cut at validate's 200-char limit; full: tit for tat (τὸ ὁμοῖον ἀνταποδιδόναι)",
        'tit for tat': 'phrase: τὸ ὁμοῖον ἀνταποδιδόναι',
        'a like return': 'phrase: τὴν ὁμοίην (sc. χάριν) φέρεσθαι',
        'in like esteem': 'phrase: ἐν ὁμοίῳ ποιεῖσθαι',
        'with equal advantages, in fair fight': 'phrase: ἐκ τῶν ὁμοίων',
        'the person or thing to which one is like': 'label: Construction: in dat.',
        'in which each takes part': "piece: ὁμοία μάχη, an example's translation",
    },
    'o(/pou': {
        'in some places': "phrase: ἔσθ' ὅπου, Lat. est ubi",
        'somewhere or other': 'phrase: ὅκου δή, with another particle, Lat. nescio ubi',
        'wherever': "phrase: ὅπου ἄν, with the subjunctive: ἄν's",
        'by which': "piece: οὐκ ἔσθ' ὅπου, there are no means «by which»",
        'that': "piece: οὐκ ἔσθ' ὅπου, it is impossible «that»",
    },
    'o(/pws': {
        'how, as': 'repeat: heading of I; repeats «as, in such manner as» and «how, in what manner»',
        'in such manner as, as': 'repeat: repeats «as, in such manner as»',
        'in what manner, how': 'repeat: repeats «how, in what manner»',
        'fieri non potest quin': 'latin: Latin of οὐκ ἔστιν ὅπως οὐ',
        'as you are off for feet': 'phrase: ὅπως ποδῶν (sc. ἔχετε)',
        'not only not . . but . .': 'phrase: οὐχ ὅπως . . , ἀλλὰ . .',
        'not only': 'phrase: οὐχ ὅπως',
        'but': "phrase: ἀλλά's, in οὐχ ὅπως . . ἀλλά",
        'also . .': "phrase: καί's, in οὐχ ὅπως . . ἀλλὰ καί",
        'do not [think] that': 'phrase: μὴ ὅπως',
        'so far from being able': 'phrase: μὴ ὅπως, i.e.',
        'how or that in some way or other': 'phrase: ὅπως ἄν (κεν) with subj. makes the manner indefinite',
        'B.': "scrap: a speaker's letter in a quoted dialogue",
        'how?': "repeat: ὅπως; as the echo of πῶς; repeats 'how'",
    },
    'o(/s': {
        'such and such a person': 'phrase: ὃς καὶ ὅς, the demonstrative doubled',
        'by attraction': "label: takes the antecedent's case «by attraction»: grammar",
        'nuncium miserunt, qui nunciaret': 'latin: Latin of ἄγγελον ἧκαν, ὃς ἀγγείλειε',
        'to tell': 'piece: ὃς ἀγγείλειε, the relative with its verb rendered by an infinitive',
        'in some places': 'phrase: ἔστιν οὗ',
        'in what part': 'phrase: οὗ γῆς, with γῆς',
        'to the place where . .': 'phrase: pregnant οὗ for ἐκεῖσε οὗ',
        'from the time when': 'phrase: ἐξ οὗ (sub. χρόνου)',
    },
    'o(/sos': {
        'indefinite': 'label: with τις, to denote «indefinite» size or number',
        'amazingly': 'phrase: θαυμαστὸν ὅσον, θαυμαστόν carries it; Lat. mirum quantum',
        'enough to': 'repeat: ὅσον ἀποζῆν; repeats «so much as is enough»',
        'enough for': 'repeat: ὅσον δοκεῖν; repeats «so much as is enough»',
        'how great soever': "phrase: ὅσος ἄν with subj.: ἄν carries 'soever'",
        'how much': 'phrase: ὅσος δή',
        'of a certain amount': 'phrase: ἐπὶ μισθῷ ὅσῳ δή',
        'ever so small': 'phrase: ὁσοσοῦν, with οὖν',
        'immediately': 'phrase: ὅσον οὐκ ἤδη',
        'so far as not, save or except so far as': "phrase: ὅσον μή: μή carries 'not'",
        'so far as I can without': "phrase: ὅσον γε μὴ ποτιψαύων, the sentence's",
        'quanto melior, eo magis': 'latin: Latin of ὅσῳ … τοσούτῳ',
        'while': 'phrase: ἐν ὅσῳ',
    },
    'o(/ti': {
        'seeing or knowing, thinking or saying': 'label: after Verbs of seeing or knowing, thinking or saying',
        'although': 'phrase: οὐχ ὅτι, not followed by a second clause',
    },
    'o(do/s': {
        'further on the way, forwards': 'phrase: πρὸς ὁδοῦ',
        'methodically, systematically': 'phrase: ὁδῷ, the dative as a phrase (cf. ψήφῳ)',
        '': "scrap: empty: validate's cap cut here; the next card item is 'the Way'",
    },
    'o(mologe/w': {
        'to have': "phrase: οὐδὲν ὁμ. τινι, to have naught to do with: οὐδέν carries 'naught'",
        'to do with': 'phrase: οὐδὲν ὁμ. τινι, to have naught to do with',
    },
    'o(ra/w': {
        'he kept looking': "repeat: ὅρα, the imperfect of 'to see or look'",
        'shall have eyes': 'phrase: πάνθ᾽ ὁρῶντα λέξομεν',
        "see'st thou? d'ye see?": 'phrase: ὁρᾷς; ὁρᾶτε; parenthetically',
        'keeping': 'piece: always keeping it in sight',
        'in sight': 'piece: always keeping it in sight',
        'to behold': "repeat: δεινὸς ἰδεῖν; repeats 'behold'",
        'I see': "repeat: φωνῇ γὰρ ὁρῶ, I see by sound: 'to see' in the first person",
    },
    'o(rma/w': {
        'that had got': "piece: αἱ μάλιστα ὁρμήσασαι [νῆες] 'the ships that had got the greatest start'",
        'that they put': "piece: μὴ φεύγειν ὁρμήσωνται 'that they put not themselves in motion'",
        'going out from thence': "phrase: B.3, ἐνθεῦτεν ὁρμώμενοι: ἐνθεῦτεν carries 'from thence'",
        'goes': "repeat: ὁρμᾶται 'goes … forth', split by 'fearless': repeats 'to go forth'",
        'forth': "repeat: ὁρμᾶται 'goes … forth': repeats 'to go forth'",
    },
    'o)/noma': {
        'pretence': "repeat: ὀνόματι, ἐπ᾽ ὀνόματι; repeats 'a false name, pretence, pretext'",
        'verbum': 'latin: Latin',
    },
    'o)/nos': {
        "an ass's": 'repeat: περὶ ὄνου σκιᾶς: the genitive of «an ass»',
    },
    'o)li/gos': {
        'almost': 'phrase: IV.1, ὀλίγου δεῖν',
        'but little': "piece: IV.1, ὀλίγου ἐδέησε καταλαβεῖν 'wanted but little of overtaking'",
        'hard upon': 'phrase: IV.1, ὀλίγου ἐς χιλίους',
        'a short distance': 'phrase: IV.2, δι᾽ ὀλίγου (sc. χώρου)',
        'at short notice, suddenly': 'phrase: IV.2, δι᾽ ὀλίγου (sc. χρόνου)',
        'in few words': 'phrase: IV.2, δι᾽ ὀλίγων',
        'in a small space, within small compass': 'phrase: IV.3, ἐν ὀλίγῳ (sc. χώρῳ)',
        'in a sh': "phrase: IV.3, ἐν ὀλίγῳ (sc. χρόνῳ), 'in a short time, suddenly': the report cut it",
        'in a short time, suddenly': 'phrase: IV.3, ἐν ὀλίγῳ (sc. χρόνῳ)',
        'one among few': 'phrase: IV.4, ἐν ὀλίγοις',
        'exceedingly, remarkably': 'phrase: IV.4, ἐν ὀλίγοις, i. e.',
        'within a little': 'phrase: IV.6, ἐς ὀλίγον',
        'few at a time, in small parties': "phrase: IV.7, κατ' ὀλίγους",
        'shortly': "phrase: IV.8, μετ' ὀλίγον",
        'a little, almost': "phrase: IV.9, παρ' ὀλίγον",
    },
    'o)pi/sw': {
        'the past': "label: the entry's prose: the future is behind us, whereas «the past» is before our eyes",
        'before': 'label: the same prose: «before» our eyes',
    },
    'o)rqo/s': {
        'right': "repeat: of 'straight, right'; right opposite the sun",
        'straightway': 'phrase: ὀρθᾷ χερί, ὀρθῷ ποδί',
        'to put the foot out': 'phrase: ὀρθὸν πόδα τιθέναι',
        'to set up, restore': 'phrase: ὀρθὸν ἱστάναι τινά',
        'the state': "label: prose: 'the state being represented as a ship'",
        'a ship)': 'label: the same prose',
        'in straight course': "phrase: κατ' ὀρθόν",
        'strictly speaking, in very truth': "phrase: III.2, ὀρθῷ λόγῳ: λόγῳ carries 'speaking'",
    },
    'o)ru/ssw': {
        'a dig or heavy blow': "piece: πὺξ ὀρ., of a pugilist, 'to give a dig or heavy blow'",
    },
    'oi(=os': {
        'why, what': "phrase: οἷον δή: δή says 'why'",
        'the sort of person': 'phrase: οἷός τις: τις says the person',
        'like as when . .': "phrase: οἷος ὅτε: ὅτε says 'when'",
        'possible': 'construction: οἷόν τε ἐστί, it is possible',
        'it is possible': 'construction: οἷόν τε ἐστίν, without inf.',
        'cannot': 'construction: οὐχ οἷόν τε ἐστίν, it cannot be',
        'in what a state': 'phrase: οἵως ἔχεις: ἔχεις says the state',
    },
    'oi)/omai': {
        'thou art': 'piece: αἰεὶ ὀίεαι, thou art ever suspecting',
        'there comes a boding': 'construction: impers., ὀίεταί μοι ἀνὰ θυμόν',
        'think it': "phrase: cut of 'think it my duty', οἴομαι δεῖν: δεῖν says the duty; later items not listed",
        'think it my duty': 'phrase: IV, οἴομαι δεῖν: δεῖν says the duty',
        'je crois devoir': 'latin: French, for οἴομαι δεῖν',
        'I think I shall. .': "piece: an example's rendering",
        'I do': 'piece: I do not think, i.e. mean',
        'I think': "repeat: κιχήσεσθαί σε ὀίω: 'to think' in the first person",
    },
    'oi)=da': {
        'to acknowledge a debt to another, thank him': 'phrase: χάριν εἰδέναι',
    },
    'oi)=kos': {
        'home': "repeat: ἐπ' οἴκου, ἀπ' οἴκου; repeats «home, within»",
        'home, within': 'phrase: κατ᾽ οἴκους',
    },
    'ou(/tws': {
        'ut': 'latin: Lat. sic … ut',
        'sic te diva regat)': 'latin: Horace',
        'jacentes sic temere)': 'latin: Horace',
        'impune': 'latin: Lat., for οὐ … οὕτως ἄπει',
    },
    'ou(=tos': {
        'the more remote': 'label: describes ἐκεῖνος, opp. to οὗτος',
        'what precedes': 'label: usage: οὗτος refers to what precedes',
        'iste': 'latin: Latin',
        'so then, therefore': 'phrase: πρὸς ταῦτα',
        'on the one hand . . , on the other . . , partly . . , partly. .': 'phrase: τοῦτο μὲν . . τοῦτο δέ',
        'thereupon': 'phrase: ἐκ τούτου or τούτων',
        'herein, so far': 'phrase: ἐν τούτῳ',
        'in the meantime': 'phrase: ἐν τούτῳ',
        'besides': 'phrase: πρὸς τούτοις',
    },
    'ou)=n': {
        'whoever': 'label: glosses ὅστις before οὖν is added',
        'whosoever;': 'phrase: ὁστισοῦν',
        'how': 'label: glosses ὅπως',
        'howsoever;': 'phrase: ὁπωσοῦν',
        'be he who he may': "phrase: ὁστισοῦν, ὅστις οὖν: the phrase's",
    },
    'ou)de/': {
        'not even . . , nor yet . .': 'construction: οὐδέ repeated at the head of two clauses',
        'neither . . , nor . .': 'label: renders οὔτε . . οὔτε, the comparison',
    },
    'ou)dei/s': {
        'good for nothing': 'phrase: οὐδὲν εἶναι: εἶναι with the neuter',
    },
    'pa=s': {
        'between': 'label: is put between the Art. and Subst.',
        'totality': 'label: to denote totality',
        'as neut.': 'label: πᾶσι as neut.',
        'any': 'piece: πᾶν ποιῶν, by any means whatever',
        'whatever': 'piece: πᾶν ποιῶν, by any means whatever',
        'on the whole, in general, generally': 'phrase: ἐπὶ πᾶν',
        'above all, absolutely, necessarily': 'phrase: παντὸς μᾶλλον',
        'absolutely so': 'phrase: π. γε μᾶλλον, in answers',
        'to all extremity': 'phrase: ἐς πᾶν κακοῦ',
        'altogether': 'phrase: ἐς τὸ πᾶν; διὰ παντός',
        'in all extremity': 'phrase: ἐν παντί',
        'for ever, continually': 'phrase: διὰ παντός',
        'in all things, altogether': 'phrase: ἐν πᾶσι',
        'in all points, entirely, wholly': 'phrase: κατὰ πάντα, τὸ πᾶν',
        'in every way, by all means, altogether': 'phrase: πάντως, πάντα, adverbial',
        'on the whole, altogether': 'phrase: τὸ πᾶν, adverbial',
        'with or in the judgment of all': 'phrase: παρὰ πᾶσι',
        'all the': 'piece: a piece of an example',
        'all his': 'piece: a piece of an example',
        'in all': 'phrase: ἐν πᾶσι',
        'at all': 'phrase: with a negative',
    },
    'pai=s': {
        "a child's child, grandchild": "phrase: παῖς παιδός: the genitive carries 'child's'",
    },
    'path/r': {
        "by the father's side": 'phrase: τὰ πρὸς πατρός',
        'Zeus': 'label: prose: among the gods Zeus is called πατήρ',
        "from one's fathers": "phrase: ἐξ ἔτι πατρῶν, as an inheritance from one's fathers",
    },
    'pau/w': {
        'stopt [flowing]': "phrase: αἷμα ἐπαύσατο, 'flowing' supplied; the sense is «to leave off doing», already on the card",
    },
    'pe/mpw': {
        'speed': "phrase: the quoted line 'welcome the coming, speed the parting guest'",
    },
    'perisso/s': {
        'signal': "repeat: repeats 'signal' of I 2",
        'superfluous': "repeat: II.2, in bad sense: repeats 'more than sufficient, redundant, superfluous'",
        'over': "piece: περισσὰ δρᾶν 'to be over busy'",
        'superfluously, uselessly': 'phrase: B.II, ἐκ περιττοῦ as adv.',
    },
    'pezo/s': {
        'on land, going by land': 'phrase: πεζῇ, the dative as an adverb',
    },
    'pi/mplhmi': {
        'to get': "piece: Mid., πλ. νῆας, 'to get ships laden'",
        'laden': "piece: of 'to get ships laden'",
    },
    'pla/gios': {
        'right and left': 'phrase: εἰς τὰ πλ. παράγειν',
        'obliquely': 'phrase: εἰς πλάγιον',
    },
    'pla/ssw': {
        'from invention': 'phrase: πλάσας λέγειν, to speak from invention',
    },
    'platu/nw': {
        "to widen one's": "piece: a piece of an example, to widen one's phylacteries",
    },
    'plh/rwma': {
        'their fill': "piece: πλ. τυρῶν, their fill of cheese: the example's possessive",
        'their complement': "piece: of single ships, their complement: the example's possessive",
    },
    'po/lis': {
        'their dwellings': 'label: glosses ἄστυ, set against πόλις',
    },
    'po/nos': {
        'the fruits of': "piece: τοὺς ἡμετέρους π., the fruits of our labour: half of III's example",
    },
    'poie/w': {
        'to build them': 'piece: οἰκία ποιήσασθαι, to build them houses',
        'made, get': "piece: of 'to have a thing made, get it made' (Mid.)",
        'to cause or bring about': "repeat: c. acc. et inf.; repeats 'to bring to pass, bring about, cause'",
        'to cause': "repeat: πόλεμον ποιεῖν; repeats 'to bring to pass, bring about, cause'",
        'to bring about': "repeat: εἰρήνην π.; repeats 'to bring to pass, bring about, cause'",
        'fortunately': 'phrase: εὖ ποιοῦν',
        'to have': 'piece: Mid., to have a thing made: the run cut by its object',
        'made': "piece: of 'to have a thing made, get it made'",
        "one's": "piece: to make him one's son",
        "one's own": "piece: to make a thing one's own (Mid.)",
    },
    'poiki/los': {
        'the Poecile or great hall at Athens adorned with paintings': "phrase: II.3, ἡ στοὰ ἡ ποικίλη, as 'the Poecile' already is",
    },
    'polu/s': {
        'with full stream': 'phrase: πολλῇ ῥυῇ',
        'all': "piece: πολλὸς ἦν λισσόμενος, 'he was all intreaties'",
        'a high price': 'phrase: ἐπὶ πολλῷ',
        'quite': 'phrase: ἔτι πολλῆς νυκτός, while still quite night',
        'much harm': "phrase: II.4, πολλὰ ἔρξαι τινά: 'harm' is the phrase's, not the word's",
        'much too much': 'phrase: πολλοῦ πολύς, the doubled word',
        'at a great distance': 'phrase: IV.1, διὰ πολλοῦ',
        'from a great distance': 'phrase: IV.2, ἐκ πολλοῦ',
        'for a long time': 'phrase: IV.2, ἐκ πολλοῦ',
        'over a great space, far': 'phrase: IV.3.a, ἐπὶ πολύ',
        'for a long time, long': 'phrase: IV.3.b, ἐπὶ πολύ',
        'to a great extent': 'phrase: IV.3.c, ἐπὶ πολύ',
        'very generally': 'phrase: IV.3.c, ὡς ἐπὶ πολύ',
        'by far': 'phrase: πολλῷ with a comparative',
        'far': "phrase: piece of 'by far'",
        'for the most part': 'phrase: τὸ πολύ, ὡς ἐπὶ τὸ πολύ',
    },
    'ponhro/s': {
        'in bad case': "repeat: adv. πονηρῶς ἔχειν; repeats 'in bad case, …'",
        'rogue and son of rogues': 'phrase: πονηρὸς κἀκ πονηρῶν',
        "coward's": "repeat: π. χρώματα, the coward's hue; repeats 'cowardly'",
    },
    'pou/s': {
        'close at hand': 'phrase: πὰρ ποδί; ἐν ποσί',
        'off-hand, at once': 'phrase: παρὰ ποδός',
        'in a moment': 'phrase: παρὰ πόδα',
        'the way, far off': 'phrase: ἐκ ποδῶν, out of the way',
        'on the track': 'phrase: κατὰ πόδας',
        'at his heels': 'phrase: κατὰ πόδας τινός',
        'backwards, facing the enemy': 'phrase: ἐπὶ πόδα',
        'leisurely': 'phrase: ἐπὶ π. ἀναχωρεῖν',
        'round the foot': 'phrase: περὶ πόδα',
        'fitting exactly': 'phrase: περὶ πόδα, i.e.',
        'sheet': "repeat: ναῦς ἐνταθεῖσα ποδί; repeats 'the sheet'",
    },
    'pra/ssw': {
        'business': 'piece: τὰ ἑαυτοῦ, the object, not πράσσω',
        'to do o': "repeat: string cut by the 200-char message; card item 'to do or fare' (εὖ πράττειν) repeats IV; later items not listed",
        'to do or fare': "repeat: IV, εὖ or κακῶς πράττειν: repeats 'to be in a certain state or condition, to do or fare so and so'",
    },
    'pra=gma': {
        'work in life?': "phrase: τὸ σὸν τί ἐστι τὸ πρ.; the question's rendering; «work» follows by itself",
        'circumstances': 'repeat: τοῖς πράγμασιν, by «circumstances»; repeats «circumstances, affairs»',
        'innovatio': "phrase: cut from «innovations»: νεώτερα πρ., νεώτερα carries 'new'",
        'to have trouble about': 'phrase: πράγματα ἔχειν, c. part.',
        'trouble': "repeat: πρ. παρέχειν τινί; repeats 'troublesome business, trouble, annoyance'",
        'the trouble': "repeat: c. inf.; repeats 'troublesome business, trouble, annoyance'",
        'innovations': "phrase: νεώτερα πρ., Lat. res novae: νεώτερα carries 'new'",
    },
    'pri/n': {
        'comparative': "label: 'formed with a comparative force'",
    },
    'pro/': {
        'to come out in front of': "piece: χωρεῖν πρὸ δόμων; χωρεῖν carries 'come out'",
        'forwards, onward': 'phrase: πρὸ ὁδοῦ, further on the road',
        'position before or in front`': "label: cut at validate's 200-char limit; full: position before or in front, IN COMPOS. (the prefix, not the preposition)",
        'position before or in front': 'label: IN COMPOS.: the prefix, not the preposition',
        'priority of rank': 'label: IN COMPOS.: the prefix, not the preposition',
        'of order': 'label: IN COMPOS.: the prefix, not the preposition',
        'proximity, readiness': 'label: IN COMPOS.: the prefix, not the preposition',
        'forth from': 'label: IN COMPOS.: the prefix, not the preposition',
        'prematureness': 'label: IN COMPOS.: the prefix, not the preposition',
        'before, forwards': 'label: IN COMPOS.: the prefix, not the preposition',
        'before, in defence': 'label: IN COMPOS.: the prefix, not the preposition',
        'forth': 'label: IN COMPOS.: the prefix, not the preposition',
        'publicly': 'label: IN COMPOS.: the prefix, not the preposition',
        'away': 'label: IN COMPOS.: the prefix, not the preposition',
        'before, in preference': 'label: IN COMPOS.: the prefix, not the preposition',
    },
    'pro/swpon': {
        'before': 'phrase: ἐς πρόσωπόν τινος ἀφικέσθαι',
        'in front, facing': 'phrase: κατὰ πρόσωπον',
        'a tete-a-tete': 'phrase: ἡ κατὰ πρ. ἔντευξις',
        'vultus instantis tyranni': 'latin: Horace',
        'in bodily presence': 'phrase: κατὰ πρόσωπον',
    },
    'prosa/gw': {
        'closely': "piece: 'to apply the eye closely to the eyelet-holes'",
        'make': "piece: πρ. ὅρκον τινί 'make him take it'",
        'take': "piece: πρ. ὅρκον τινί 'make him take it'",
        'to': "scrap: the validator's report cut this item off after 'to'",
        'to draw all eyes upon oneself': "phrase: B, πάντων πρ. ὄμματα: ὄμματα carries 'eyes'",
    },
    'prosde/xomai': {
        'expectation': 'phrase: τῷ Νικίᾳ προσδεχομένῳ ἦν, according to his expectation',
    },
    'prosfe/rw': {
        'to bear': "piece: of 'to bring it to bear', πρ. τόλμαν",
        'to bring forward': "repeat: of 'to bring forward, quote, cite'; proposals",
        'near': "piece: of 'to bring one thing near another' (III)",
        'make': "piece: of 'make it like' (III)",
        'like': "piece: of 'make it like' (III)",
        'towards': "piece: of 'to deal with, behave oneself in a certain way towards one'",
    },
    'proskale/w': {
        'on a charge of': "piece: φόνου 'on a charge of murder': the genitive's",
    },
    'prospi/ptw': {
        'to circumstances': 'phrase: πρὸς τὰ προσπίπτοντα, according to circumstances',
    },
    'prosti/qhmi': {
        "to associate one's": "piece: of 'to associate one's opinion to another', Mid. τὴν γνώμην",
        'to be profited': 'phrase: πρ. πλέον: πλέον carries the profit',
        'made': "piece: προσεθήκαντο πόλεμον, made war: of 'to bring upon others'",
    },
    'qa/natos': {
        "for one's life": "phrase: θανάτου κρίνεσθαι, to be tried for one's life",
        'dead': 'label: νεκρός as adj., through III = νεκρός; θάνατος has no adjective',
    },
    'qauma/sios': {
        'marvellous': "repeat: θαυμάσιος τὸ κάλλος; repeats 'marvellous'",
    },
    'qauma/zw': {
        'I keep wondering that': 'construction: II Pass., θαυμάζεται μὴ παρών, i.e.',
    },
    'qe/ros': {
        'during the summer': 'phrase: τὸ θέρος, the accusative of time as a phrase',
    },
    'qea/omai': {
        'the spectators': 'construction: οἱ θεώμενοι, the participle with the article',
    },
    'qu/ra': {
        'to put to': "phrase: θύρην ἐπιτιθέναι: ἐπιτιθέναι's",
    },
    'qumo/s': {
        'to take away life': "phrase: θυμὸν ἀπαυρᾶν, ἀφελέσθαι, etc.: the verbs carry 'take away'",
        'in his heart or with all his heart': 'phrase: ἤθελε θυμῷ, the dative as a phrase',
        "with all one's heart": 'phrase: θυμῷ βουλόμενος, the dative as a phrase',
        'sorrow or joy': "label: 'as the seat of sorrow or joy': the tr marks the emotions, not the word",
        'as the seat of anger': "label: the entry's description of a use",
    },
    'r(a/ptw': {
        'made the shoe': 'phrase: τὸ ὑπόδημα ἔρραψας',
    },
    'r(h/gnumi': {
        'to let loose': 'repeat: ῥῆξαι φωνήν; repeats «to let break loose, let loose»',
        'to speak freely, speak out': 'phrase: ῥῆξαι φωνήν, φωνήν carrying the speech; like rumpere vocem',
    },
    'shmei=on': {
        'a proof': "repeat: of 'a sign or proof'",
    },
    'si=tos': {
        'ground': "piece: σ. ἀληλεσμένος 'ground corn': the participle's",
    },
    'ske/ptomai': {
        'only consider': "phrase: σκέψασθε δέ: δέ says 'only'",
    },
    'skeu=os': {
        'the vessel': "label: metaph., τὸ σκεῦος, the body, as the vessel of the soul: the entry's explanation",
    },
    'skhnh/': {
        'the stage': "label: prose: 'the stage (in our sense) was προσκήνιον'",
        'the actors, players': 'phrase: οἱ ἀπὸ σκηνῆς',
        'actually represented on the stage': 'phrase: τὸ ἐπὶ σκηνῆς μέρος',
        'odes sung on the stage': 'phrase: τὰ ἀπὸ τῆς σκηνῆς',
        'a stage, "': "repeat: of 'a wooden stage', in the quoted 'all the world's a stage'",
    },
    'sklhro/s': {
        'on a hard seat': 'phrase: σκληρῶς καθῆσθαι: καθῆσθαι says the seat',
    },
    'ste/gh': {
        'at home': 'phrase: κατὰ στέγας',
    },
    'sto/ma': {
        'by word of mouth': 'phrase: ἀπὸ στόματος',
        "in every one's mouth": 'phrase: διὰ στόμα',
        'talk': "phrase: πᾶσι διὰ στόματος, 'tis the common talk",
    },
    'stre/fw': {
        "d'ye shuffle": "piece: from 'why d'ye shuffle so?'",
    },
    'sugxai/rw': {
        'to wish': 'piece: «to wish» one «joy, congratulate»: restored whole in TEXT_LOST',
        'joy of': 'piece: «to wish» one «joy of» the events: the run before it again',
    },
    'sullamba/nw': {
        'to take part with': "repeat: V.2, 'to take part with one in a thing': repeats 'to take part with, assist'",
    },
    'sumpi/ptw': {
        'it happened, fell out, came to pass': 'construction: impers., συνέπεσε, c. inf.',
        'have come to exactly': "piece: 'have come to exactly the same point with me'",
        'having collapsed': "repeat: σῶμα συμπεσόν: repeats 'fall in, collapse'",
    },
    'suntele/w': {
        'contributions': 'label: prose: citizens classed acc. to the contributions',
    },
    'sxolh/': {
        'hardly': "repeat: σχολῇ in an a fortiori argument; repeats 'hardly' of B 2",
    },
    'ta/fos': {
        'dead and buried': "phrase: ὄντες ἐν τάφοις 'though dead and buried'",
    },
    'ta/ssw': {
        'over': "piece: τ. τινὰ ἐπί τινος, one over a thing: ἐπί's",
        'set': "piece: to act as one of a 'set'",
        'certain': "piece: of 'to appoint or fix a certain payment'",
        'to fix': "repeat: τάσσειν ἀργυρίου, to fix the price: repeats 'to appoint or fix'",
    },
    'taxu/s': {
        'in haste': 'phrase: B.2, διὰ ταχέων',
        'as soon as possible': 'phrase: C.II.2, ὅττι τάχιστα',
        'by the quickest way': 'phrase: C.II.3, τὴν ταχίστην (sc. ὁδόν)',
        'most quickly': 'phrase: C.II.3, τὴν ταχίστην (sc. ὁδόν)',
    },
    'te/leios': {
        'performed with all': "piece: of 'performed with all rites'",
        'the surest bird of augury': 'phrase: αἰετὸς τελειότατος πετεηνῶν',
        'which imported': "piece: 'a vision which imported nothing'",
        'tycta': 'label: the Persian word it renders',
    },
    'teleuta/w': {
        'at last': 'repeat: τελευτῶντες, repeats «at the end, at last»',
    },
    'teleuth/': {
        'at the end, at last': 'phrase: I.5, ἐς τελευτήν',
        'the extremities': "repeat: II, plural of 'the end, extremity', τελευταὶ Λιβύης",
    },
    'ti/qhmi': {
        'to pile': "phrase: cut at validate's 200-char limit; full: to pile arms (τίθεσθαι τὰ ὅπλα)",
        'to pile arms': 'phrase: τίθεσθαι τὰ ὅπλα',
        'to bivouac': 'phrase: τίθεσθαι τὰ ὅπλα',
        'to take up a position, draw up in order of battle': 'phrase: τίθεσθαι τὰ ὅπλα',
        "to lay down one's arms, surrender": 'phrase: τίθεσθαι τὰ ὅπλα',
        "to keep one's arms in good order": 'phrase: εὖ θέσθαι ὅπλα',
        'to kneel down': 'phrase: τιθέναι τὰ γόνατα',
        'ordain': "repeat: so may he ordain; repeats 'to ordain, command'",
        'has made': "repeat: ἔθηκε; repeats 'to make'",
        'thou didst make': "repeat: ἔθηκας; repeats 'to make'",
        'in what light': 'phrase: ποῦ χρὴ τίθεσθαι ταῦτα;',
        'nullo in numero habere': 'latin: Latin',
        'hold': "repeat: I hold not that he lives; repeats 'to hold'",
        'to lay down, assume': "repeat: repeats 'to lay down, assume, hold, reckon or regard as'",
        'left': "piece: an example's participle",
        "to give one's": "piece: τίθεσθαι τὴν γνώμην, to give one's opinion",
    },
    'timh/': {
        'to pay or make': "piece: τίνειν or ἀποτίνειν τιμήν 'to pay or make it': the verbs'",
    },
    'tis': {
        'a brute': "label: 'a man, opp. to a brute': the term opposed, κύων",
        'kind of`': "piece: 'kind of' with the cut's backtick, from 'a bold kind of fellow'",
        '': "scrap: empty: validate's cap cut here; the next card item is 'a brute'",
    },
    'to/te': {
        'at one time or other': "phrase: τότ' ἢ τότε",
    },
    'toiou=tos': {
        'just such': 'phrase: strengthd. τ. ἕτερος, just such another',
    },
    'tre/fw': {
        'left the nursery': "phrase: ἐξ ὅτου 'τράφην ἐγώ, the sentence's free rendering",
        'puts': 'piece: this is what «puts» fat «on» swine',
        'she constantly performs': "phrase: οἵας λατρείας τρέφει, the sentence's free rendering",
        'he keeps': "piece: an example's",
        'on': 'piece: this is what puts fat on swine',
    },
    'tro/pos': {
        'means': "piece: παντὶ τρόπῳ 'by all means', as 'way' and 'wise' already are",
    },
    'tu/xh': {
        '"in God\'s name, "': 'phrase: II.3, ἀγαθῇ τύχῃ, a formula',
        'what a piece of ill-luck': 'phrase: III, an exclamation: τῆς τύχης, τὸ ἐμὲ τυχεῖν',
    },
    'u(polei/pw': {
        'fails': "repeat: ὑπ. τινά ὁ λόγος 'fails him': 'to fail'",
        'against oneself': "piece: III, Mid., 'to leave cause for reproach against oneself'",
    },
    'w(/ra': {
        'twenty-four hours': "label: II.2, prose: 'divided into twenty-four hours by Hipparchus'",
        'twelve parts': "label: II.2, prose: 'the natural day into twelve parts'",
        'the Hours': "label: B, mythol., αἱ Ὧραι: a name of goddesses, as 'Uranus' is for οὐρανός",
    },
    'w(s': {
        'in very truth': 'phrase: ὡς ἀληθῶς',
        'quam facillime;': 'latin: Latin',
        'quam celerrime': 'latin: Latin',
        'so that I never should . .': 'phrase: ὡς ἔδειξα μήποτε . .',
        'while': "repeat: repeats 'so long as, while'",
        'quomodo': 'latin: Latin',
        'nowise can it be that': 'phrase: οὐκ ἔσθ᾽ ὡς',
        'quam': 'latin: Latin',
        'ut vidi, ut perii, ut me malus abstulit error).': 'latin: Virgil',
        'some': "repeat: παῖς ὡς ἑπταετής; repeats 'about, nearly'",
        'to what end?': 'phrase: ὡς τί',
    },
    'xa/ris': {
        'for or towards': 'piece: renders the genitive τινός',
        'a sense of favour, feel grateful': 'phrase: χάριν εἰδέναι τινί',
        'to please': 'phrase: χάριν φέρειν τινί',
        'to oblige': 'phrase: χάριν φέρειν τινί',
        'pleasure, for': "scrap: a tr cut across 'for his pleasure, for his sake' (acc. χάριν); 'pleasure or sake' gives the sense",
        'reason?': "phrase: τοῦ χάριν; 'for what reason?', the question's rendering",
        'for the sake': "phrase: πρὸς χάριν βορᾶς: πρός carries 'for'",
        'for the pleasure of devouring': "phrase: πρὸς χάριν βορᾶς: βορᾶς carries 'devouring'",
        'as a favour, freely': 'phrase: πρὸς χάριν alone',
        "heart's content": "phrase: πρὸς χάριν, to their heart's content",
        'on terms of friendship or mutual favour': 'phrase: διὰ χαρίτων εἶναι',
        'Aglaia, Euphrosyne, Thalia.': 'label: prose: the names of the three Graces',
        'as far as regards, as to': 'phrase: χάριν used as a preposition',
    },
    'xai/rw': {
        'go unpunished, shalt repent': 'phrase: οὐ χαιρήσεις: the negative makes the idiom',
        "to dismiss from one's mind, put away from one, renounce": 'phrase: ἐᾶν χαίρειν τινά: ἐᾶν makes the idiom',
    },
    'xei/r': {
        'one takes a person by the hand': "label: 'the gen. is used when …': prose on the case",
        'one takes the hand of a person': "label: 'the acc. is used when …': prose on the case",
        'off hand, roughly': 'phrase: ἀπὸ χειρὸς λογίζεσθαι',
        'between the hands': 'phrase: διὰ χερῶν λαβεῖν',
        'under control': 'phrase: διὰ χειρὸς ἔχειν',
        'blows or close quarters': 'phrase: ἐς χεῖρας ἐλθεῖν',
        'from near at hand, close': 'phrase: ἐκ χειρός',
        'in hand, be engage': "phrase: cut by validate's cap: 'in hand, be engaged in', ἐν χερσὶν ἔχειν",
        'in hand, be engaged in': "phrase: ἐν χερσὶν ἔχειν, as decided for the cut 'in hand, be engage'",
        'between': "phrase: μετὰ χερσὶν ἔχειν: μετά carries 'between'",
        'close before one': 'phrase: πρὸ χειρῶν',
        'given by hand': 'phrase: πρὸς χεῖρα, at a sign given by hand',
        "under one's power": 'phrase: ὑπὸ χεῖρα ποιεῖσθαι',
        'single-': "piece: μιᾷ χειρί 'single-handed': μιᾷ carries 'single-'",
        'grappling-': "piece: χ. σιδηρᾶ 'a grappling-iron': σιδηρᾶ carries 'iron'; 'grapnel' gives the sense whole",
        'on': 'piece: λαιᾶς χειρός, on the left hand: the genitive of place',
        'hand?': 'repeat: on which hand?',
        'in hand': 'phrase: διὰ χειρὸς ἔχειν, εἰς χεῖρας λαμβάνειν, μετὰ χεῖρας ἔχειν',
        'hand to hand': 'phrase: ἐν χερσί',
        'in, the hands': 'phrase: μετὰ χερσὶν ἔχειν',
        'handed': 'piece: μιᾷ χειρί, single-handed',
    },
    'xra/omai': {
        'to become a slave': "phrase: ζυγῷ χρ. δουλίῳ: the dative carries 'slave'",
        'custom': 'piece: such «is» their «custom»: a second rendering of the same sentence',
        'friends': "piece: a piece of 'χρῆσθαί τινι φίλῳ, to have as a friend'",
        'to make of': 'piece: τί χρήσομαι, what use shall I make of',
        'use shall I make': 'piece: τί χρήσομαι',
    },
    'yuxh/': {
        'heart': "repeat: ἐκ τῆς ψυχῆς; repeats 'the soul, heart'",
        'of things dear as life': "label: the entry's label for a use",
    },
    'za/w': {
        'of living men': "piece: ἐλέγχιστε ζωόντων; 'men' is supplied for the genitive participle",
    },
    'zugo/n': {
        'those on the upper bench': 'phrase: οἱ ἐπὶ ζυγῷ δορός',
        'a file': "label: VI, 'opp. to a file'",
    },
    'zwh/': {
        'living': "repeat: to get one's living; repeats 'a living'",
    },
}
COVERAGE_ONLY = {
    'a(/gios': {
        'the Temple': 'neuter',  # τὸ ἅγιον
    },
    'a(/ls': {
        'the sea': 'singular',  # as fem. sg., «the sea»
    },
    'a(/ptw': {
        'to fasten oneself to, cling to, hang on by, lay hold of, grasp, touch': 'middle',  # II, Mid., c. gen.
    },
    'a(marta/nw': {
        'a sin is committed': 'passive',  # Pass., ἁμαρτάνεταί τι (II.2)
    },
    'a)/bussos': {
        'with no bottom, bottomless, unfathomed': 'adjective',  # sense I is the adjective; the units are the noun ἡ ἄβυσσος (II)
    },
    'a)/cios': {
        'worthily of': 'adverb',  # III, adv. ἀξίως, c. gen.
    },
    'a)/gw': {
        'taking': 'active participle',  # ἄγων, in the sense of 'with'
        'being formed': 'passive participle',  # κόλπου ἀγομένου
        'to carry away for oneself, take with one': 'middle',  # Mid.
        'to marry': 'middle',  # Mid., ἄγεσθαι
        'to bring home': 'middle',  # Mid., of the father
        'to let pass': 'middle',  # Mid., διὰ στόμα ἄγεσθαι μῦθον
        'to take': 'middle',  # ἄγεσθαί τι ἐς χεῖρας
        'to undertake': 'middle',  # Mid., ἄγεσθαι ἐς χεῖρας
        'let us go': 'first person',  # ἄγωμεν
    },
    'a)/nqos': {
        'bright colours': 'plural',  # III, in pl.
    },
    'a)/nqrwpos': {
        'sirrah! you sir': 'vocative',  # in vocat., ἄνθρωπε
        'a woman': 'feminine',  # fem.
    },
    'a)/roura': {
        'corn-lands, fields': 'plural',  # I, in pl.
    },
    'a)/rxw': {
        'beginning the sacrifice with': 'middle',  # Mid. also in a religious sense
        'to lead, rule, govern': 'active',  # of Authority, only in Act.
        'to rule, be leader of . .': 'active',  # of Authority, only in Act.
        'to rule over': 'active',  # of Authority, only in Act.
        'to rule, govern': 'active',  # of Authority, only in Act.
        'to hold a subordinate': 'active',  # cut at validate's 200-char limit; full: to hold a subordinate office (only in Act.)
        'to hold a subordinate office': 'active',  # of Authority, only in Act.
        'to be archon': 'active',  # of Authority, only in Act.; at Athens
        'subjects': 'passive participle',  # Pass., οἱ ἀρχόμενοι
        'to be ruled, governed': 'passive',  # Pass.
    },
    'a)/rxwn': {
        'the chief magistrates at Athens': 'plural',  # Ἄρχοντες, οἱ, nine in number
    },
    'a)cio/w': {
        'deeming himself worthy': 'middle',  # III.2, as a real Mid., οὐκ ἀξιούμενος
        'state of opi': 'participle',  # V, ἐν τῷ τοιῷδε ἀξιοῦντι 'in such a state of opinion': the report cut it
        'state of opinion': 'participle',  # V, ἐν τῷ τοιῷδε ἀξιοῦντι 'in such a state of opinion'
    },
    'a)delfo/s': {
        'brother and sister': 'plural',  # ἀδελφοί, like Lat. fratres
        'brotherly or sisterly': 'adjective',  # II, adj. ἀδελφός, ή, όν
        'in pairs': 'adjective',  # II.2, of anything
        'twin': 'adjective',  # II.2
        'just like': 'adjective',  # II.2, c. gen. or dat., ἀδελφὰ τῶνδε
    },
    'a)faire/w': {
        'to be robbed or deprived': 'passive',  # III, Pass.
        'to prevent, hinder from': 'middle',  # II.2, Mid., foll. by μή c. inf.
    },
    'a)fi/hmi': {
        'let go hold of': 'middle',  # B.3, Mid. c. gen. only, τέκνων ἀφοῦ
        'to break up, march, sail': 'not passive',  # seemingly intr.
    },
    'a)fori/zw': {
        'to mark off for oneself, appropriate': 'middle',  # Mid.
    },
    'a)gapa/w': {
        'to be beloved': 'passive',  # I, Pass.
    },
    'a)gaphto/s': {
        'cheerfully, contentedly': 'adverb',  # III, adv. -τῶς
        'just enough to content one, only just, barely, scarcely': 'adverb',  # III.2, adv. -τῶς
    },
    'a)gaqo/s': {
        'good, gentle, noble': 'not neuter',  # I.1, of persons
        'good, brave': 'not neuter',  # I.2, of persons
        'good, serviceable': 'not neuter',  # II.1, of things
        'the good': 'neuter',  # τὸ ἀγαθόν, the good
        'the goods of fortune, wealth': 'neuter plural',  # II.2, in pl., ἀγαθά, τά
        'good qualities': 'neuter plural',  # II.2, in pl., of a horse
        'a good': 'neuter',  # τὸ ἀγαθόν, a good, used as a noun
    },
    'a)kou/w': {
        'to hear oneself called, be called': 'not passive',  # the active in a passive sense, with an adv.
    },
    'a)lhqh/s': {
        'unconcealed, true': 'not adverb',  # the adverb ἀληθῶς has its own II, «truly», «really, actually, in reality»
        'true': 'not adverb',  # I, opp. to ψευδής
        'the truth': 'neuter',  # τὸ ἀληθές, τὰ ἀληθῆ
        'truthful': 'not adverb',  # I.2 of persons
        'true, coming true': 'not adverb',  # I.3 of oracles
        'in very truth': 'superlative',  # III 2, τὸ ἀληθέστατον
        'truly': 'adverb',  # II adv. ἀληθῶς
        'really, actually, in reality': 'adverb',  # II 2
        'really and truly': 'neuter',  # III 2, τὸ ἀληθές
    },
    'a)lhqino/s': {
        'truly, really': 'adverb',  # adv. -νῶς
    },
    'a)lla/ssw': {
        'to buy': 'middle',  # III, Mid. ἀλλάσσεσθαι … hence 'to buy'
    },
    'a)mblu/nw': {
        'to become dull, lose its edge or force': 'passive',  # Pass.
    },
    'a)nabai/nw': {
        'to make to go up': 'aorist',  # aor1 ἀνέβησα used as aor. to ἀναβιβάζω
        'to put on sh': 'aorist',  # cut at validate's 200-char limit; full: to put on shipboard
        'to put on shipboard': 'aorist',  # aor1 ἀνέβησα used as aor. to ἀναβιβάζω
    },
    'a)nabiba/zw': {
        'to ascend': 'passive',  # Pass., ἀναβιβάζεσθαι εἰς τιμήν
    },
    'a)nafe/rw': {
        'to fetch up a deep-drawn breath, heave a deep sigh': 'middle',  # I.2 Mid., ἀνενείκασθαι, absol.
        'to': 'passive',  # cut from «to recover oneself, come to oneself»: II.6 Pass.
        'to recover oneself, come to oneself': 'passive',  # II.6, Pass.
    },
    'a)naire/w': {
        'to take upon oneself, undertake': 'middle',  # B II Mid.
        'to undertake, contract for the execution of': 'middle',  # B II Mid., ἀν. δημόσιον ἔργον
    },
    'a)nalamba/nw': {
        'to take upon oneself, undertake, engage in': 'middle',  # I.4, Mid.
    },
    'a)nali/skw': {
        'expended': 'passive',  # Pass. part., τἀνηλωμένα
    },
    'a)naplhro/w': {
        'to be restored to its former size': 'passive',  # Pass., of the sun after an eclipse
    },
    'a)nastre/fw': {
        'turned up': 'passive',  # I Pass., ὄρος ἀνεστραμμένον «turned up» by digging
        'to be or dwell in': 'passive',  # III Pass., Lat. versari
        'to go to': 'passive',  # III Pass., «to go to» a place «and dwell there»
        'and dwell there': 'passive',  # III Pass., the rest of «to go to» a place «and dwell there»
    },
    'a)ne/xw': {
        'to hold oneself up, bear up, hold out': 'middle',  # C II Mid.
    },
    'a)ni/hmi': {
        'to devote oneself, give oneself up': 'passive',  # III.6 Pass.
        'to be treated remissly': 'passive',  # III.7 Pass.
    },
    'a)ni/sthmi': {
        "to rise from one's seat": 'middle',  # B.1; the causal στησ- forms already skip B
        'to rise from bed': 'middle',  # B.1
        'to rise from the dead': 'middle',  # B.1
        'recover': 'middle',  # B.1, to rise from an illness
        'to be set up, to rise up, rear itself': 'middle',  # B.3, of buildings and statues
        'to rise to go, set out, go away': 'middle',  # B.II
        'to be compelled to migrate': 'middle',  # B.II.2
        'to be depop': 'middle',  # cut by validate's cap: 'to be depopulated' (B.II.2)
        'to be depopulated': 'middle',  # B.II.2, of a country, as decided for the cut 'to be depop'
        'subject to migration': 'middle',  # B.II.2, οὐκέτι ἀνισταμένη
        'to be put up': 'middle',  # B.II.4, of game
    },
    'a)noi/gnumi': {
        'to be open, stand open': 'passive',  # II Pass., of doors
        'to get into the open sea, get clear of land': 'not passive',  # absol., nautical
    },
    'a)ntile/gw': {
        'to be disputed': 'passive',  # 2, Pass.
        'to be counter-claimed': 'passive',  # 2, Pass., of a place
    },
    'a)pa/gw': {
        'to retire, withdraw, march away': 'not passive',  # intr.
    },
    'a)pata/w': {
        'to be deceived into thinking': 'passive',  # Pass., ἀπατᾶσθαι, ὡς . .
    },
    'a)po/': {
        'far away': 'adverb',  # AS ADVERB
    },
    'a)pobai/nw': {
        'to make to dismount, disembark, land': 'aorist',  # B, Causal in aor1 ἀπέβησα
        'things ended': 'neuter plural',  # τὰ ἀποβάντα
    },
    'a)podi/dwmi': {
        "to give away of one's own will, to sell": 'middle',  # III, Mid.
        'to sell for': 'middle',  # III, Mid., ἀπ. τοῦ εὑρίσκοντος
        'to farm out': 'middle',  # III, Mid., at Athens, of the public taxes
        'was allowed': 'passive',  # I.3, so in Pass., ὁ λόγος ἀπεδόθη αὐτοῖς
        'to yield fruit': 'not passive',  # intr., of land
    },
    'a)pokalu/ptw': {
        'to be disclosed, made known': 'passive',  # Pass.
    },
    'a)poste/llw': {
        'to go away, depart, set out': 'passive',  # Pass.: the passive's own English
        'to go back, retire': 'not passive',  # intr.
    },
    'a)postre/fw': {
        'hostile': 'perfect passive',  # ἀπεστραμμένοι λόγοι
        'to turn and flee': 'passive',  # B, Pass.
        'to fa': 'passive',  # cut by validate's 200-char cap: 'to fall off from' (B.II.3, ἀποστραφῆναί τινος)
        'to fall off from': 'passive',  # B, Pass.
        'desert': 'passive',  # B, Pass., ἀποστραφῆναί τινος
        'to turn oneself about, turn back': 'passive',  # B, Pass.
    },
    'a)poti/nw': {
        'to get paid one, to exact or require': 'middle',  # II Mid. ἀποτίνομαι, a penalty from a man
        'to avenge oneself on': 'middle',  # II 2 Mid. c. acc. pers.
        'punish': 'middle',  # II 2 Mid., ἀποτίσασθαί τινα
        'to take vengeance for': 'middle',  # II 3 Mid. c. acc. rei
        'to take vengeance': 'middle',  # II 3 Mid. absol.
    },
    'a)qroi/zw': {
        'to gather for oneself, collect round one': 'middle',  # Mid.
    },
    'a)re/skw': {
        'to appease, conciliate': 'middle',  # I.2 Mid.
    },
    'a)rxh/': {
        'to begin with, first': 'accusative',  # absol. in acc. ἀρχήν
        '"the authorities, "': 'plural',  # in pl., αἱ ἀρχαί
        'the magistrates': 'plural',  # in pl., αἱ ἀρχαί
    },
    'a)sfalh/s': {
        'fast, firm, steady': 'adverb',  # II, epic adv. ἀσφαλέως ἔχειν
        'without faltering': 'adverb',  # II, neut. ἀσφαλές as adv., ἀσφ. ἀγορεύει
    },
    'a)sqenh/s': {
        'feebly, slightly': 'adverb',  # II, adv. ἀσθενῶς
    },
    'ai(=ma': {
        'streams of blood': 'plural',  # in pl., Trag. (I)
    },
    'ai)sxro/s': {
        'dishonour, disgrace': 'neuter',  # τὸ αἰσχρόν, as Subst.
        'shamefully': 'adverb',  # adv.
    },
    'ai)sxu/nw': {
        'to feel shame before one': 'passive',  # B. Pass., c. acc. pers.
    },
    'au)ca/nw': {
        'grew taller': 'passive',  # Pass., ηὐξανόμην I grew taller
    },
    'au)lai/a': {
        'screens': 'plural',  # LSJ, in pl., screens against missiles
    },
    'au)to/s': {
        'the result': 'neuter',  # in neut., αὐτὸ δείξει
        'together with': 'dative',  # in dat. with Subst.
        'and all': 'dative',  # αὐτῇ σὺν πήληκι; αὐτοῖς ἀνδράσι
    },
    'bapti/zw': {
        'soaked in wine': 'passive',  # Pass., βεβαπτισμένοι, metaph.
        'to get oneself baptized': 'middle',  # Mid.
    },
    'baru/s': {
        'ill': 'adverb',  # adv., βαρέως φέρειν, to take a thing ill
        'with disgust': 'adverb',  # adv., βαρέως ἀκούειν, to hear with disgust
    },
    'basileu/w': {
        'to have become king': 'aorist',  # in aor.
        'to submit to the king': 'passive',  # under Pass.
    },
    'bdelu/ssomai': {
        'the abominable': 'participle',  # II, οἱ ἐβδελυγμένοι, NTest.
    },
    'be/ltistos': {
        'the aristocracy': 'plural',  # οἱ βέλτιστοι or τὸ βέλτιστον
    },
    'bia/zw': {
        'to use force, struggle': 'middle',  # II 3, Mid. βιάζομαι absol.
    },
    'bo/skw': {
        'to feed, graze': 'passive',  # II, Pass., of cattle
        'to be fed or nurtured': 'passive',  # II.2, Pass. metaph.
        'to run riot in': 'passive',  # II.2, β. τινί or περί τι
    },
    'de/w': {
        'save': 'active',  # I so in partic., ἑνὸς δέον εἰκοστόν the 20th year «save» one
        'to bind, tie, put on oneself': 'middle',  # II Mid.
    },
    'di/dwmi': {
        'to give oneself up, devote oneself': 'not passive',  # IV, seemingly intr.
    },
    'di/kaios': {
        'in due form, decently': 'adverb',  # adv., δικαίως μνᾶσθαι (A.I)
        'a right, a lawful claim': 'neuter',  # B.I.2
        'rightly, justly': 'adverb',  # adv. -ως (B.I.2)
        'really and truly': 'adverb',  # adv. -ως (B.II.2)
        'with reaso': 'adverb',  # cut by validate's cap: 'with reason', δικαίως (B.II.3)
        'observant of custom and social rule, well-ordered, civilised': 'not adverb',  # A.I
        'regular': 'not adverb',  # A.I, δικαίη ζόη 'a regular way of living'
        'observant of right, righteous': 'not adverb',  # A.2
        'in accordance with right, righteous': 'not adverb',  # A.2, of actions
        'even, well-balanced': 'not adverb',  # B.I, of things
        'regul': 'not adverb',  # B.I, 'regular, exact, rigid': the report cut it
        'with reason': 'adverb',  # B.II.3, δικαίως 'with reason'
    },
    'diaire/w': {
        'the breach': 'passive',  # τὸ διῃρημένον
        'to divide among themselves': 'middle',  # Mid. (II)
    },
    'diale/gw': {
        'to use a dialect or language': 'middle',  # B II, Dep. διαλέγομαι
    },
    'diameri/zw': {
        'to divide or part among themselves': 'middle',  # II Mid.
    },
    'diaste/llw': {
        'to give express orders': 'middle',  # 3, in Mid., NTest.
    },
    'diasw/zw': {
        'to retain': 'middle',  # II Mid.
        'to come safe through, arrive in safety': 'passive',  # I Pass.
        'to recover': 'passive',  # I Pass., «to recover» from illness
    },
    'diati/qhmi': {
        'to arrange mutually': 'middle',  # B 4 Mid.
        'to make a covenant with': 'middle',  # B 4 Mid., δ. διαθήκην τινί
        'to settle': 'middle',  # B 4 Mid., ἔριν δ. ἀλλήλοις
    },
    'diplo/os': {
        'two': 'plural',  # II, in pl. = δύο
    },
    'do/los': {
        'wiles': 'plural',  # 1, in pl.
    },
    'doca/zw': {
        'to hold an opinion': 'not passive',  # absol.
    },
    'doke/w': {
        'the decree': 'participle',  # II.4, τὸ δόξαν
        'when it was decreed or resolved': 'participle',  # II.4.b, acc. absol. δόξαν
        'men who are held': 'participle',  # II.5, οἱ δοκοῦντες εἶναί τι
        'of repute': 'participle',  # II.5, men 'of repute'
        'those who have been found guilty': 'passive',  # II.5, in Pass., οἱ δεδογμένοι ἀνδροφόνοι
    },
    'dwrea/': {
        'a gift, present': 'not adverb',  # I
        'a free gift, bounty': 'not adverb',  # I, esp.
    },
    'e(toima/zw': {
        'to cause to be prepared': 'middle',  # II, Mid.
    },
    'e)/cw': {
        'things outside': 'neuter plural',  # τὰ ἔξω «things outside» the walls
    },
    'e)/mprosqen': {
        'the front, fore-side': 'neuter',  # I.1, τὸ and τὰ ἔμπροσθεν
    },
    'e)/sxatos': {
        'the utmost': 'neuter',  # as Subst., τὸ ἔσχατον, τὰ ἔσχατα
        'extremest': 'superlative',  # so in Sup., τὰ πάντων ἐσχατώτατα
        'the end': 'neuter',  # ἐς τὸ ἔσχατον, to the end
        'to the uttermost, exceedingly': 'adverb',  # V adv. -τως
    },
    'e)/xw': {
        'a wealthy man': 'active participle',  # ὁ ἔχων
        'to be possessed by, belong to': 'passive',  # Pass. «to be possessed by, belong to», τινι
        'what concerns': 'neuter participle',  # τὸ ἐς Ἀργείους ἔχον
        'to hold on by, cling to': 'middle',  # Mid., c. gen.
        'to cleave or cling to': 'middle',  # Mid., metaph.
        'to lay claim to': 'middle',  # Mid.
        'to be zealous for': 'middle',  # Mid., μάχης
        'to come next to, follow closely': 'middle',  # Mid.
        'follows up': 'middle',  # Mid., τῆς πληγῆς ἔχεται
        'to be close, touch, border on': 'middle',  # Mid., of peoples or places
        'next': 'middle',  # of Time, τὸ ἐχόμενον ἔτος
        'to depend on': 'middle',  # Mid.
        'to pertain to': 'middle',  # Mid.
        "to maintain oneself, hold one's ground": 'middle',  # Mid.
        'to keep off from oneself, repel': 'middle',  # Mid., c. acc.
        'to stop oneself, stop': 'middle',  # Mid.
        'to keep oneself back, abstain or refrain from': 'middle',  # Mid.
        'to have charge of, keep': 'not passive',  # no passive
        'to have to wife': 'not passive',  # no passive
        "to have in one's house, to entertain": 'not passive',  # no passive
        'to have means or power': 'not passive',  # intransitive
        'with': 'participle',  # ἔχων with a verb: come with an army
        'to bear or hold for oneself': 'middle',  # Mid. II
        'extended': 'not passive',  # intr., of the view
        'to lead towards': 'not passive',  # intr.
        'to point towards, tend towards': 'not passive',  # intr.
        'to put in, land': 'not passive',  # intr.
        'to take part in, have to do with': 'not passive',  # intr.
    },
    'e)a/w': {
        'to be given up': 'passive',  # I Pass.
    },
    'e)ca/ptw': {
        'to hang on': 'middle',  # II Mid.
        'to hang': 'middle',  # II 2 Mid.: 'to hang a thing to oneself, carry it about one', one translation
        'to oneself, carry': 'middle',  # II 2 Mid., same translation
        'about': 'middle',  # II 2 Mid., same translation
        'wear': 'middle',  # II 2 Mid.
    },
    'e)caei/rw': {
        'to rise up, rise': 'passive',  # III, Pass.
        'to be excited, agitated': 'passive',  # III, Pass.
    },
    'e)caire/w': {
        'to be given as a special honour': 'passive',  # II Pass., τινι
        'dedicated': 'passive',  # Pass. part., ἐξαραιρημένος Ποσειδέωνι
        'taken out of their hands': 'passive',  # Pass., ἐξαιρεθέντες τὸν Δημοκήδεα
    },
    'e)calei/fw': {
        'to blot': 'middle',  # Mid., ἐξαλείψασθαι φρενός «to blot» it «out of one's» mind
    },
    'e)cani/sthmi': {
        'emigrate, to remove or expel': 'active',  # I.2, 'to make a tribe emigrate'
        'to depopulate, destroy': 'active',  # I.3, πόλιν
        'to arise and depart from, emigrate from': 'passive',  # II.2, c. gen.
    },
    'e)cegei/rw': {
        'to be awaked, wake up': 'passive',  # Pass.
    },
    'e)ci/sthmi': {
        'to shrink from, shun': 'perfect or passive',  # B.2, c. acc.
    },
    'e)cousi/a': {
        'the authorities': 'plural',  # αἱ ἐξουσίαι
    },
    'e)gei/rw': {
        'to awake': 'passive',  # II Pass., with perf. act. ἐγρήγορα
        'to keep watch or vigil': 'aorist',  # II, in aor2 also
        'to be awake': 'perfect',  # II, in perf.
        'to rouse or stir oneself, be excited': 'passive',  # II 2 under Pass.
    },
    'e)kba/llw': {
        'to put ashore': 'middle',  # Mid. (I)
    },
    'e)kdu/w': {
        'put off': 'middle',  # I 2 Mid. ἐκδύομαι
        "to put off one's clothes, strip": 'middle',  # I 2 Mid. absol.
        'to put off': 'middle',  # II 1, ἐκδύνω same sense as Mid.
        'to go or get out of': 'perfect',  # II 2, ἐξέδυν, ἐκδέδυκα, c. gen.
        'to emerge from': 'perfect',  # II 2, the sea
        'to escape': 'perfect',  # II 2 b, c. acc.
    },
    'e)kei=': {
        'the dead': 'never',  # οἱ ἐκεῖ, i.e. the dead
    },
    'e)kei=nos': {
        'in that way, in that case': 'adverb',  # adv. ἐκείνως
        'there, at that place, on that road': 'dative',  # dat. fem. ἐκείνῃ as adv. (sub. ὁδῷ)
        'in that manner': 'dative',  # dat. fem. ἐκείνῃ, of manner
    },
    'e)kei=qen': {
        'yon': 'never',  # c. gen., τοὐκεῖθεν ἄλσους
    },
    'e)klekto/s': {
        'the elect': 'plural',  # II, οἱ ἐκλεκτοί, NTest.
    },
    'e)klu/w': {
        'to get': 'middle',  # I, Mid., 'to get one set free', split by 'one'
        'likely to let loose': 'participle',  # II, ἐκλύσων στόμα
        'to be faint, fail, give way': 'passive',  # II.3, Pass.
    },
    'e)kpe/mpw': {
        'to go forth, depart': 'passive',  # I.2, Pass.
    },
    'e)ktei/nw': {
        'to be outstretched, lie at length': 'passive',  # Pass. (I)
        'to be on the rack': 'passive',  # metaph. in Pass. (III)
    },
    'e)kto/s': {
        'external things': 'neuter plural',  # II absol., τὰ ἐκτός
    },
    'e)kxe/w': {
        'to pour out, stream out or forth': 'passive',  # II Pass.
        'to be spread out': 'passive',  # II Pass., generally
        'to be poured out like water, forgotten': 'passive',  # II.2 Pass.
        'to give oneself up to joy, to be overjoyed': 'passive',  # Pass.
        'to burst out': 'passive',  # II.3 Pass., ἐκχ. γελῶν
        'to lie languidly': 'passive',  # II.4 Pass.
    },
    'e)lattone/w': {
        'lack, want': 'middle',  # LSJ 3, Med.
    },
    'e)le/gxw': {
        'to be convicted': 'passive',  # II, Pass.
    },
    'e)lee/w': {
        'to be pitied, have pity or mercy shewn one': 'passive',  # Pass.
    },
    'e)mba/llw': {
        'to lay': 'middle',  # III 2 Mid., ἐμβάλλεσθαί τι θυμῷ, to lay it to heart
        'fall upon': 'middle',  # III 3 Mid. c. gen., ἐμβάλεσθε τῶν λαγῴων
    },
    'e)mo/s': {
        'my property': 'neuter',  # 3, τὸ ἐμόν, τὰ ἐμά
        'my part, my affairs, my interest': 'neuter',  # 3, τὰ ἐμά or τὸ ἐμόν
    },
    'e)nanti/os': {
        'over against, opposite': 'adjective',  # I.1; the existing FORM_SENSES note reads the preposition from the neuter's senses
        'fronting, face to face': 'adjective',  # I.1
        'in opposite directions, meeting': 'adjective',  # I.1, with verbs of motion
        'opposing, facing': 'adjective',  # I.2, in fight
        "one's adversaries": 'plural',  # οἱ ἐν. (I.2)
        'opposed to': 'adjective',  # I.2, generally
        'the opposite, contrary, reverse': 'neuter',  # I.3, of qualities, τὰ ἐν.
        'contrariwise': 'neuter',  # II.1.c, neut. ἐναντίον without a case, and II.3 ἐναντίως
        'on the other hand': 'neuter',  # II.1.c, in attic τοὐναντίον
    },
    'e)ndu/w': {
        'to clothe in': 'active',  # II Causal, c. dupl. acc.
        'to clothe': 'active',  # II 2, τινά
        'to wear': 'perfect',  # I.1, perf. ἐνδέδυκα 'to wear'
    },
    'e)pa/gw': {
        'to procure or provide for oneself': 'middle',  # II. Mid. «to procure» or «provide for oneself»
        'to': 'middle',  # cut from «to devise, invent»: II Mid., metaph., Ἀΐδα φεῦξιν ἐπ.
        'bring in or introduce as allies': 'middle',  # II.2, Mid., of persons
        'to call in': 'middle',  # II.3, Mid., as witnesses
        'adduce': 'middle',  # II.3, Mid.
        'to bring over to oneself, win over': 'middle',  # II.6, Mid.
        'to devise, invent': 'middle',  # II, Mid., metaph., Ἀΐδα φεῦξιν ἐπ.
    },
    'e)pai/rw': {
        'to be led on, excited': 'passive',  # II Pass.
        'to be elated at': 'passive',  # II.2 Pass.
        'to be conceited or proud': 'passive',  # II.2 Pass., absol.
    },
    'e)paine/w': {
        'well done!': 'aorist',  # I.4 the aor. ἐπῄνεσα used in a pres. sense, and absol.
        'I thank you, I am much obliged': 'present',  # III κάλλιστ', ἐπαινῶ
    },
    'e)pe/xw': {
        'he lay outstretched': 'middle',  # V aor2 mid. ἐπέσχετο
    },
    'e)piba/llw': {
        'the portion that falls to one': 'neuter participle',  # τὸ ἐπιβάλλον (sc. μέρος)
        'to throw oneself upon, desire eagerly': 'middle',  # Mid., c. gen.
        'to put upon oneself': 'middle',  # Mid., c. acc.
        'to take possession of, take': 'middle',  # cut at validate's 200-char limit; full: to take possession of, take upon oneself (Mid., me
        'to take possession of, take upon oneself': 'middle',  # Mid., metaph.
        'to be put upon': 'passive',  # in Pass.
        'devote oneself to': 'not passive',  # intr.
        'to apply oneself to': 'not passive',  # intr.
        'to belong to, fall to': 'not passive',  # intr.
        'to fall upon or against': 'not passive',  # intr.
        'to follow, come next': 'not passive',  # intr.
        "to give one's attention to, think on": 'not passive',  # intr.
        'to throw oneself upon, go straight towards': 'not passive',  # intr.
    },
    'e)pibai/nw': {
        'to make one mount, set him upon': 'active',  # B, Causal in aor1 act.
    },
    'e)pife/rw': {
        'to bring with or upon oneself, bring as dowry': 'middle',  # Mid.
        'to rush upon or after, attack, assault': 'passive',  # III, Pass.
        'to come after or next, ensue': 'passive',  # III, Pass.
        'coming events': 'neuter plural',  # τὰ ἐπιφερόμενα
        'to be borne onwards': 'passive',  # Pass.
    },
    'e)pigignw/skw': {
        'to come to a decision, to resolve, decide': 'not passive',  # intr.
    },
    'e)pikale/w': {
        'to call before one, summon': 'middle',  # Mid. (I.4)
        'to challenge': 'middle',  # Mid. (I.5)
        'to be nicknamed': 'passive',  # Pass. (II)
        'to be called by surname': 'passive',  # Pass. (II)
    },
    'e)pikli/nw': {
        'to lie over against': 'passive',  # III, Pass.
        'to lie down at table': 'passive',  # IV, in Pass.
    },
    'e)pispa/w': {
        'being drawn tight': 'passive',  # ἐπισπασθέντος τοῦ βρόχου
        'returning with a rush': 'passive',  # I 5 Pass., of the sea
        'to become uncircumcised': 'middle',  # II in Mid.
    },
    'e)pistre/fw': {
        'constantly turning': 'middle or passive',  # II Mid. and Pass., ἐπιστρεφόμενος
        'turned to gaze on': 'middle or passive',  # II Mid. and Pass., θάλαμον ἐπεστράφη
        'turned about, changed': 'middle or passive',  # II Mid. and Pass., δόξα ἐπεστράφη
        'to go back-and for-wards, wander over': 'middle or passive',  # II.2 Mid. and Pass.
        'to': 'middle or passive',  # cut from «to turn the mind towards, to pay attention to»: II.3 Mid. and Pass.
        'to recover oneself, pay attention': 'middle or passive',  # II.3, absol.
        'to visit': 'middle or passive',  # II.4, c. acc.
        'earnest, vehement': 'passive',  # II.5, = ἐπιστρεφής
        'to turn the mind towards, to pay attention to': 'middle or passive',  # II.3, Mid. and Pass., c. gen.
    },
    'e)piti/qhmi': {
        'to set oneself to, apply oneself to, employ oneself on or in': 'middle',  # B.II, Mid., c. dat.
        'to make an attempt upon, attack': 'middle',  # B.II.2, Mid.
        'with assiduity': 'middle',  # B.II.3, Mid. absol., δικαιοσύνην ἐπιθέμενος ἤσκεε
        'to cause': 'middle',  # B.IV, Mid., 'to cause a penalty to be imposed', split by 'a penalty'
        'to lay commands on': 'middle',  # B.V, Mid., τί τινι
    },
    'e)pitima/w': {
        'to rise in price': 'passive',  # I 2 Pass.
    },
    'e)pitre/pw': {
        'inclined itself': 'middle',  # I, in aor2 mid., θυμὸς ἐπετράπετο
        "to entrust oneself, leave one's case to": 'middle',  # I 3, so in Mid.
    },
    'e)pitugxa/nw': {
        'the first person one meets, any one': 'participle',  # ὁ ἐπιτυχών, like ὁ τυχών
    },
    'e)pixe/w': {
        'to pour or throw': 'middle',  # B, Mid.
        'to have poured out for one to drink': 'middle',  # B.II, Mid.
        'to drink': 'middle',  # B.II, Mid., ἐπ. ἄκρατόν τινος
        'to stream to': 'passive',  # C, Pass., of a crowd
        'to come like a stream over': 'passive',  # C, Pass.
    },
    'e)rga/zomai': {
        'to be done': 'passive',  # perf. pass. in pass. sense; fut. ἐργασθήσομαι
    },
    'e)sqi/w': {
        'is eaten up': 'passive',  # Pass., οἶκος ἐσθίεται
    },
    'ei)/seimi': {
        'the new': 'participle',  # ὁ ἐσιών, the new king
        'what enters into one, food': 'neuter plural',  # IV, τὰ εἰσιόντα
    },
    'ei)mi/': {
        'true': 'participle',  # τὸν ἐόντα λόγον, the true story
    },
    'ei)sa/gw': {
        'to introduce new': 'not passive',  # its noun outside the translation
    },
    'ei)sfe/rw': {
        'to carry with one, sweep along': 'middle',  # II, Mid.
        'to bring in for oneself, to import': 'middle',  # II.2, Mid.
        'to bring in with one, introduce': 'middle',  # II.3, Mid.
        'to be brought in, introduced': 'passive',  # III, Pass.
        'to rush': 'passive',  # III.2, Pass., 'to rush in': the report cut 'in'
        'to rush in': 'passive',  # III.2, Pass., as decided for the cut 'to rush'
    },
    'eu(ri/skw': {
        'to get for oneself, bring on oneself': 'middle',  # Mid.
        'to find out for oneself': 'middle',  # so in Mid.
    },
    'eu)=': {
        'the right, the good cause': 'neuter',  # II as Subst., τὸ εὖ
    },
    'fa/os': {
        'eyes': 'plural',  # φάος, metaph., in pl. the eyes
    },
    'fai/nw': {
        "to exhibit as one's own": 'middle',  # A, Mid.
        'born': 'passive',  # B.2, Pass., φανεὶς δύστηνος 'born to misery'
        'shewn to': 'passive',  # B.2, Pass., δοῦλος φανείς 'shewn to be, having become': the card cuts the tr
        'shewn to be, having become': 'passive',  # B.2, Pass., δοῦλος φανείς
        'what has once come to light': 'passive participle',  # τὸ φανθέν
        'manifestly': 'passive',  # B, Pass., εὔνοος ἐφαίνετο ἐών
        'informed against': 'passive participle',  # A.4, Pass., τὰ φανθέντα, articles informed against
        'to shine brightly': 'passive',  # B, Pass., of fire
        'they were manifest': 'passive',  # B, Pass., Κᾶρες ἐφάνησαν
        'to give light': 'active',  # intr. in act., to give light, shine
        'make it ring clear': 'not passive',  # its object 'it'
        'to give information': 'not passive',  # absol.
        'to make it clear': 'not passive',  # its object 'it'
    },
    'fanero/s': {
        'openly, manifestly': 'adverb',  # I 5 adv. -ρῶς
    },
    'fanero/w': {
        'to become so': 'passive',  # Pass., to become known or famous
    },
    'fe/rw': {
        "for one's own use": 'middle',  # Mid., to bring with one or for one's own use (IV)
        'to carry off with one': 'middle',  # VI, Mid.
        'to win for oneself': 'middle',  # VI.3, so in Mid.
        'to win and hold': 'middle',  # VI.3, metaph., τὰ πρῶτα φέρεσθαι
        'to gain': 'middle',  # VI.3, πλέον φέρεσθαι, the advantage
        'to take home': 'middle',  # VI.3, of the Mid., 'esp. to take home'
        'spoken of': 'passive',  # VIII, Pass., εὖ, πονηρῶς φέρεσθαι
        'is carried about': 'passive',  # VIII, absol. φέρεται, Lat. fertur
        'it is said': 'passive',  # VIII, φέρεται, i. e. it is said
        'come, now, well': 'imperative',  # IX, imperat. φέρε used as adv.
        'well then': 'imperative',  # IX.2, φέρε before a question
        'fortune, fate': 'neuter participle',  # τὸ φέρον
        'to be swept away': 'passive',  # B.I, Pass.
        'flying': 'passive',  # B.I, ἧκε φέρεσθαι, sent him flying
        'go': 'passive',  # B.I, ἧκα πόδας … φέρεσθαι, I let go: ἧκα carries 'let'
        'swing free': 'passive',  # B.I, φέρεσθαι
        'with a rush': 'passive participle',  # B.I.2, φερόμενοι with another verb of motion
        'hurriedly, in haste': 'active participle',  # φέρων, intr.
        'to come': 'passive',  # B.II, of voluntary motion, ὁμόσε τινὶ φέρεσθαι
        'to turn out well or ill, succeed or fail': 'passive',  # B.III, εὖ, κακῶς φέρεσθαι
        'take their course': 'passive',  # B.III, ἐᾶν ταῦτα φέρεσθαι
        'inclines': 'not passive',  # intr.
        'to aim at a thing, hint or point at, refer to it': 'not passive',  # absol.
        'to lead to': 'not passive',  # absol., of roads
        'to lead to, be conducive to': 'not passive',  # absol.
        'to stretch, extend to or towards': 'not passive',  # absol., of country
    },
    'file/w': {
        'welcome shalt thou be': 'passive',  # I.2, Pass., φιλήσεαι
        'to kiss one another': 'middle',  # I.3, Mid.
    },
    'fobero/s': {
        'terror, danger': 'neuter',  # I.2, τὸ φ.
    },
    'fqei/rw': {
        'to have suffered loss from shipwreck': 'passive',  # Pass.: the passive's own English, as printed
        'to pine away in': 'passive',  # Pass.
    },
    'fro/nimos': {
        'presence of mind': 'neuter',  # τὸ φρ.
        'prudence': 'neuter',  # τὸ φρόνιμον
        'wisdom': 'neuter plural',  # in pl., φρόνιμα
    },
    'fu/lac': {
        'the garrison': 'plural',  # οἱ φ.
    },
    'fu/w': {
        'the begetter, father': 'active participle',  # ὁ φύσας
        'to be by nature disposed to do': 'perfect',  # B II 2 c. inf.
        'to be by nature prone': 'perfect',  # B II 3, φῦναι ἐπὶ δακρύοις
        'the things produced': 'participle',  # τῶν φύντων
        'to be': 'perfect',  # the perfect in a present sense
        'to put forth shoots': 'not passive',  # absol.
    },
    'fula/ssw': {
        'to be watched, kept under guard': 'passive',  # Pass.
        'to be fostered in or by . .': 'passive',  # Pass., φυλάττεσθαι παρά τινι
        'cautious, prudent': 'perfect passive',  # πεφυλαγμένος
        '': 'middle',  # cut at validate's 200-char limit (GEN 2:15); full: with caution (φυλασσομένους, Mid.)
        'cautious, prudent`': 'middle',  # cut at validate's 200-char limit; full: cautious, prudent (Mid.)
        'with caution': 'middle',  # φυλασσομένους πορεύεσθαι
        'to guard, keep safe': 'middle',  # C.I.3 Mid.
        'to take care': 'middle',  # Mid. c. inf.
        'to take care for': 'middle',  # Mid. c. gen.
        'be chary of': 'middle',  # Mid. c. gen.
        "to beware of, be on one's guard against, shun, avoid": 'middle',  # φυλάσσεσθαί τι or τινα
        'guard against': 'middle',  # Mid. c. inf., φ. μὴ ποιεῖν
        'to keep watch and ward, keep guard': 'not passive',  # absol.
    },
    'futeu/w': {
        'the father': 'participle',  # ὁ φυτεύσας alone
        'the parents': 'participle',  # οἱ φυτεύσαντες
        'to spring': 'passive',  # Pass., to spring from parents
    },
    'gemi/zw': {
        'to be laden or freighted': 'passive',  # Pass.
    },
    'gi/gnomai': {
        'the result or amount': 'participle',  # of sums, ὁ γεγονὼς ἀριθμός
        'the event, the fact': 'neuter participle',  # in neut. part., τὸ γενόμενον
        'the facts': 'neuter participle',  # τὰ γενόμενα
        'former events, the past': 'neuter participle',  # τὰ γεγενημένα
        'the f': 'neuter participle',  # cut at validate's 200-char limit; full: the future (τὸ γενησόμενον)
        'the future': 'neuter participle',  # τὸ γενησόμενον
    },
    'gignw/skw': {
        'to be pronounced': 'passive',  # Pass., of a sentence or judgment
        'I understand': 'first person active',  # ἔγνων, in dialogue: the active's
        'were aware of': 'not passive',  # c. gen., to be aware of: no passive
    },
    'gumno/s': {
        'the parts not covered by armour, the exposed parts': 'neuter plural',  # τὰ γυμνά
        'the right side': 'neuter plural',  # τὰ γυμνά, esp.
    },
    'gumno/w': {
        'to strip oneself naked or to be stript naked': 'passive',  # Pass.
    },
    'gunaikei=os': {
        "the women's apartments, harem": 'feminine',  # II as Subst. ἡ γυναικηίη = γυναικών
    },
    'h(me/ra': {
        'by day': 'genitive',  # ἡμέρας, by day
    },
    'h(suxa/zw': {
        'to make still, lay to rest': 'aorist',  # II, Causal in aor1
    },
    'i(/na': {
        'in that place, there': 'adverb',  # Adverb of place, demonstr.
        'in which place, where': 'adverb',  # relat., = ὅπου
        'in whatever part': 'adverb',  # c. gen., ἵνα γῆς
        'whither': 'adverb',  # with Verbs of motion
        'when, at which': 'adverb',  # of circumstance
    },
    'i(/ppos': {
        'horse, cavalry': 'singular',  # II, ἵππος, ἡ, always in sg.
    },
    'i(kano/s': {
        'sufficiently, adequately, enough': 'adverb',  # III, adv. -νῶς
    },
    'i(ma/s': {
        'the traces by which horses were attached to the chariot': 'plural',  # in pl.
        'the reins': 'plural',  # in pl.
        'the straps': 'plural',  # in pl., on which the body of the chariot was hung
        'the lash': 'plural',  # in pl., of a whip
        'the caestus': 'plural',  # in pl., of boxers
        'straps put round the hand': 'plural',  # in pl., the caestus
        'girdle': 'singular',  # in sg., the magic girdle of Aphrodite
    },
    'i)a/omai': {
        'to be healed, to recover': 'passive',  # II, aor1 ἰάθην is always pass.
    },
    'kai/': {
        'and above all': 'conjunction',  # A. copulative, θεοὶ καὶ Ζεύς; the units are adverbial καί
    },
    'kako/s': {
        'bad': 'not neuter',  # the first sense; B κακόν, κακά, as Subst. reads «evil, ill»
        'mean, ugly': 'not neuter',  # I.1 of persons
        'ill-born, mean, ignoble': 'not neuter',  # I.2 of persons
        'craven, cowardly, base': 'not neuter',  # I.3
        'worthless, sorry, poor': 'not neuter',  # I.4
        'bad, evil, wicked': 'not neuter',  # I.5 in moral sense
        'bad, evil, baneful': 'not neuter',  # II of death, disease
        'bad, unlucky': 'not neuter',  # II of omens
        'evil, abusive': 'not neuter',  # II of words
        'evil words, reproaches': 'neuter plural',  # B.2 κακά, τά, also «evil words, reproaches»
        'evil words, r': 'neuter plural',  # B 2, κακά, τά; string cut by the 200-char message, card item 'evil words, reproaches'; lat
    },
    'kale/w': {
        'I call down': 'middle',  # ἀρὰς καλοῦμαι
        'to be invoked': 'passive',  # in Pass., of the god
        'to sue': 'middle',  # of the plaintiff, in Mid.
        'to have received a name, to b': 'perfect passive',  # cut at validate's 200-char limit; full: to have received a name, to bear it (perf. pass. κ
        'is called on': 'passive',  # πρὶν … καλεῖσθαι, before it is called on
        'to have received a name, to bear it': 'perfect passive',  # κέκλημαι: the perfect passive's own English, as printed
        'to be': 'perfect passive',  # κέκλημαι, often = εἰμί
    },
    'kalo/s': {
        'beauty': 'neuter',  # I.2, τὸ καλόν
        'the decencies, proprieties, elegancies': 'neuter plural',  # I.2, τὰ καλά
        'moral beauty, virtue': 'neuter',  # τὸ καλόν
        'well, rightly': 'adverb',  # adv. καλῶς
        'well, happ': 'adverb',  # cut at validate's 200-char limit; full: well, happily (καλῶς)
        'well, happily': 'adverb',  # καλῶς
        'well': 'adverb',  # κ. πράσσειν, to fare well
        'right well': 'adverb',  # καλῶς = πάνυ
        'rightly, deservedly': 'adverb',  # κ. ποιῶν, as adv.
        'well said!': 'adverb',  # C.II.5, καλῶς in answers
        'thank you!': 'adverb',  # C.II.5, καλῶς, to decline an offer
        'finely': 'superlative',  # Sup. κάλλιστ᾽, ironically
        'beautiful, beauteous, fair': 'not adverb',  # I, first sense of the adjective
        'beautiful, fair, good': 'not adverb',  # II
        'good, auspicious': 'not adverb',  # II.2, of sacrifices
        'beautiful, noble': 'not adverb',  # III, moral sense
    },
    'kalu/ptw': {
        'to cover or veil oneself': 'middle',  # I Mid.
    },
    'kalupth/r': {
        'tiles': 'plural',  # LSJ 3, pl.
    },
    'kaqeu/dw': {
        'a sleeping state': 'participle',  # I, ἐκ τοῦ καθεύδοντος (part. neut.)
    },
    'kaqi/sthmi': {
        'steadied': 'middle',  # A, Mid. aor1, κατεστήσαντο the sails
        'be returned': 'passive',  # A 2 Pass., οὐκ ἂν χάρις καθίσταιτο
        'to appoint for oneself, establish, institute': 'middle',  # A II 2, in aor1 mid.
        'to be set, set oneself down, settle, arrive': 'passive',  # B 1
        'to come before': 'passive',  # B 1 b
        'stand in': 'passive',  # B 1 b: 'stand in his presence', one translation
        'to stand quiet, be c': 'passive',  # B 3; string cut by the 200-char message, card item 'to stand quiet, be calm'; later items 
        'abated': 'aorist',  # ὁ θόρυβος κατέστη
        'composedly': 'active participle',  # καταστάς
        'are ye?': 'perfect',  # B 4, τίνι τρόπῳ καθέστατε;
        'the present state of life': 'neuter plural',  # τὰ καθεστῶτα
        'existing laws, customs': 'neuter plural',  # τὰ κατεστεῶτα
        'to stand against, oppose': 'passive',  # [6] Pass.: the passive's own English
        'to stand quiet, be calm': 'passive',  # B.3, of water
        'to come into a certain state, to become': 'perfect',  # B.4, in perf.
        'to be established or instituted, to prevail, exist': 'passive',  # B.5
        'existing, established, prevailing': 'participle',  # B.5, in perf. part., οἱ καθεστῶτες νόμοι
    },
    'kaqufai/nw': {
        'to be inwoven': 'passive',  # LSJ Pass.
    },
    'kata/gw': {
        'to come to land, land': 'passive',  # I 3 Pass.
        'to turn in and lodge in': 'passive',  # I 3 b, κατάγεσθαι παρά τινι
        'to return': 'passive',  # II Pass.
    },
    'katadei/knumi': {
        'had been proved': 'passive',  # Pass., c. part., κατεδέδεκτο
    },
    'katadu/w': {
        'to slink away and lie hid': 'middle',  # I 3
    },
    'katafai/nw': {
        'to become visible, appear': 'passive',  # Pass.
    },
    'katafe/rw': {
        'to be weighed down': 'passive',  # I 4 Pass.
        'to return': 'passive',  # II Pass.
    },
    'katafrone/w': {
        'to be thought little of, despised': 'passive',  # I.2, Pass.
    },
    'katagela/w': {
        'to laugh scornfully': 'not passive',  # absol.
    },
    'katakeno/w': {
        'waste away, shrivel': 'passive',  # LSJ strengthd. for κενόω; κενόω I 6, in Pass.
    },
    'katalamba/nw': {
        'what happened, the circumstances': 'neuter plural',  # II.4 absol., τὰ καταλαβόντα = τὰ συμβάντα
        'being constrained': 'passive',  # III.3 Pass., καταλαμβανόμενος
    },
    'katalei/pw': {
        'to reserve for oneself': 'middle',  # Mid.
        'to leave behind one': 'middle',  # so in Mid., καταλείπεσθαι παῖδας
        'to leave': 'middle',  # I 3, in Mid., simply, to leave in a certain state
    },
    'katamanqa/nw': {
        'to have learnt, to be aware': 'perfect',  # 5, in perf.
    },
    'katapau/w': {
        'to leave off from, cease from': 'middle or passive',  # III, Pass. and Mid.
        'to leave off, cease': 'middle or passive',  # III, Pass. and Mid.
    },
    'katara/omai': {
        'accursed': 'passive',  # the perfect passive participle, κατηραμένος
    },
    'katarra/kths': {
        'down-rushing': 'adjective',  # I as adj.
        'downward': 'adjective',  # I as adj., τὸν καταρράκτην ὁδόν
    },
    'kataxe/w': {
        'lie in heaps': 'passive',  # I 3 Pass.
    },
    'katayu/xw': {
        'to be chilled, become cold': 'passive',  # I Pass., of persons
        'to be dried or parched up': 'passive',  # II Pass., of a country
    },
    'kate/xw': {
        'to be possessed, inspired': 'passive',  # A.II.9, in Pass., of persons
        'to be held down, to be bound, kept under': 'passive',  # A.2, Pass.
        'to be detained, to stay, stop, tarry': 'passive',  # A.3, Pass.
        'to keep back for oneself, embezzle': 'middle',  # C, Mid.
        'to hold, contain': 'middle',  # C.3, Mid.
        'subdued': 'middle',  # C.II, κατασχόμενος: the aor. mid. used like a Pass.
        'to be stopped, to stop': 'middle',  # C.II, the aor. mid. used like a Pass.
        'prevail, are frequent': 'not passive',  # intr.
        'prevails, is rife': 'not passive',  # intr.
        'to come from the high sea to shore, put in': 'not passive',  # intr.
        'to have the upper hand': 'not passive',  # intr.
        'to prevail': 'not passive',  # intr.
    },
    'katerga/zomai': {
        'to be overcome': 'perfect passive',  # I 2 b, perf. pass.
    },
    'katesqi/w': {
        'corroded': 'passive',  # 3, perf. pass. part. κατεδηδεσμένοι
    },
    'katoike/w': {
        'to be administered, governed': 'passive',  # II in Pass., of a state
        'to have been settled, to dwell': 'passive',  # I.2 so in perf. and plup. pass.
    },
    'katoiki/zw': {
        'to be placed or settled': 'passive',  # Pass., of persons (II.1)
        'to have colonies planted there, to be colonised': 'passive',  # Pass., of places
    },
    'kei/rw': {
        'shorn': 'passive',  # I, Pass., κεκάρθαι τὰς κεφαλάς
        'to be cut off': 'passive',  # I, Pass., of the hair
        'swept clean': 'middle',  # III, Mid., Ἄρης πλάκα κερσάμενος
    },
    'khru/ssw': {
        'the public orders': 'neuter plural',  # τὰ κηρυχθέντα
    },
    'kine/w': {
        'to be put in motion, to be moved, move, stir': 'passive',  # B Pass.
        'to move forward': 'passive',  # B.2 Pass., of soldiers
    },
    'klai/w': {
        'to your sorrow, at your peril': 'participle',  # I, κλάων
        'to bewail oneself, weep aloud': 'middle',  # III, Mid.
        'bathed in tears, all tears': 'passive',  # III, perf. part. pass. κεκλαυμένος
        'to bewail to oneself': 'middle',  # III.2, Mid., trans.
    },
    'kle/ptw': {
        'blindfold': 'passive',  # Pass., προβαίνει κλεπτόμενος
        'by fraud': 'active participle',  # κλέπτων ἢ βιαζόμενος
        'to whisper malicious': 'not passive',  # its noun outside the translation
    },
    'ko/ptw': {
        'to be shattered or disabled': 'passive',  # I.2, Pass., of ships
        'stricken': 'passive',  # I.2, metaph., φρενῶν κεκομμένος (perf. pass. part.)
        'to coin oneself': 'middle',  # I.3, Mid., money
        'order to be coined': 'middle',  # I.3, Mid.
        'to be stamped or coined': 'passive',  # I.3, Pass., of the money
    },
    'koi=los': {
        'the hold': 'feminine',  # κοίλη ναῦς, so ἡ κοίλη alone
        'the valley': 'feminine',  # ἡ Κοίλη, the valley of the Ilissus
        'a hollow, cavity, ravine': 'neuter',  # II as Subst. κοῖλον, τό
        'the cavities': 'neuter',  # II, τὰ κ., in the body
    },
    'koili/a': {
        'tripe and puddings': 'plural',  # in pl.
    },
    'koima/w': {
        'to fall asleep, go or lie abed': 'middle or passive',  # II, Mid. and Pass.
    },
    'komi/zw': {
        'to be conveyed, to journey, travel': 'passive',  # II.3, Pass.
        'have reaped': 'passive',  # II.4, perf. pass. in mid. sense, κεκόμισθε
        'to get back for oneself, recover': 'middle',  # II.6, Mid.
        'to come or go back, return': 'passive',  # II.6, Pass.
    },
    'krema/nnumi': {
        'to be hung up, suspended': 'passive',  # II Pass.
        'to be in suspense': 'passive',  # II 3 metaph.
    },
    'kri/nw': {
        'to be brought to trial': 'passive',  # IV.2, Pass.
    },
    'kru/ptw': {
        'to hide oneself, lie hidden': 'middle or passive',  # Mid. and Pass.
    },
    'kta/omai': {
        'to possess, have, hold': 'pluperfect',  # in perf. and plup. (II)
        'an owner, master': 'participle',  # ὁ κεκτημένος
        'lord and master': 'participle',  # ὁ κεκτημένος, of a woman's
    },
    'ku/klos': {
        'any circular body': 'not adverb',  # II
        'a wheel': 'not adverb',  # II.1
        'a place of assembly': 'not adverb',  # II.2
        'circle of people': 'not adverb',  # II.2, 'a ring or circle of people'
        'the vault': 'not adverb',  # II.3
        'the orb or disk': 'not adverb',  # II.4
        'the wall round': 'not adverb',  # II.5
        'a round shield': 'not adverb',  # II.6
        'the eye-balls, eyes': 'not adverb',  # II.7, in pl.
        'the eye': 'not adverb',  # II.7, rarely in sg.
        'any circular motion, an': 'not adverb',  # III, 'any circular motion, an orbit': the report cut 'orbit'
        'any circular motion, an orbit': 'not adverb',  # III, of the heavenly bodies
        'revolution': 'not adverb',  # III, of the seasons
        'cycle': 'not adverb',  # III, of events
        'a circular dance': 'not adverb',  # III.2
    },
    'ku/rios': {
        'a lord, master': 'masculine',  # I ὁ κύριος; κυρία, ἡ is I.2
        'the head': 'masculine',  # I «the head» of a family
        'master': 'masculine',  # I «master» of a house
        'the Lord': 'singular',  # II ὁ Κύριος
        'Jehovah': 'singular',  # II ὁ Κύριος, = Hebr. Jehovah
    },
    'kuklo/w': {
        'to go in a circle, go round': 'passive',  # Pass. or Mid.
    },
    'kuro/w': {
        "to accomplish one's end": 'middle',  # 1, Mid.
        'it has been accomplished': 'passive',  # Pass.
    },
    'kwlu/w': {
        'a hindrance': 'participle',  # 4, τὸ κωλῦον
    },
    'lamba/nw': {
        'to take hold of, lay hold on': 'middle',  # B. Mid., c. gen.
        'reach, gain': 'middle',  # Mid., λ. τῶν ὀρῶν
        'to have given one, to get, gain, win': 'not passive',  # no passive
        'took and': 'participle',  # λαβών, almost pleonastic
        'to take to': 'middle',  # B.2, Mid., λ. τῶν ὀρῶν
        'to admit of': 'not passive',  # no passive
    },
    'le/gw': {
        'I mean': 'first person active',  # λέγω, I mean, in parenthesis: the active's
        'say on': 'imperative',  # λέγε, say on
        'the so-called': 'passive participle',  # ὁ λεγόμενος
    },
    'li/qos': {
        'some special stone': 'feminine',  # the fem. was mostly used of some special stone
        'magnet': 'feminine',  # fem.
        'touchstone': 'feminine',  # fem.
        'a piece of crystal': 'feminine',  # ἡ διαφανὴς λ.
    },
    'lo/gos': {
        'histories, history': 'plural',  # A.IV.2, in pl.
        'one part of such a work': 'singular',  # A.IV.2, in sg.
    },
    'logi/zomai': {
        'to form calculations': 'not passive',  # intr.
    },
    'loxeu/w': {
        'to lie embedded': 'middle or passive',  # Pass.
    },
    'lupe/w': {
        'to grieve about': 'passive',  # Pass., c. acc. rei (II)
        'to feel pain': 'passive',  # Pass., absol. (II)
    },
    'ma/la': {
        'very, very much, exceedingly': 'comparative',  # I; μᾶλλον is II
        'very': 'comparative',  # I.1 μάλα πολλά
        'together, every one': 'comparative',  # I.1 μάλα πάντες all «together, every one»
        'all': 'comparative',  # I.1 μάλ' ἀσκηθής «all» unhurt
        'quite': 'comparative',  # I.1 with advs.
        'right': 'comparative',  # I.1 εὖ μάλα «right» well
        'greatly': 'comparative',  # I.1 with verbs
        'carefully': 'comparative',  # I.1 μάλ' ἡνιόχευεν
        'ever so much': 'comparative',  # I.2 strengthening an assertion
        'never so much': 'comparative',  # I.2 μάλα περ with a partic.
        'yes, certainly, exactly so': 'comparative',  # I.3 in answers
        'most, most of all': 'superlative',  # III, Sup. μάλιστα
        'first and above all': 'superlative',  # III, μάλιστα μέν . . , ἔπειτα δέ
        'precise': 'superlative',  # III, τί μάλιστα;
        'certainly': 'superlative',  # III, ὡς μ., in answers
        'about': 'superlative',  # III.4, with numbers
    },
    'me/gas': {
        'most important': 'superlative',  # τὸ μέγιστον
        'greatly, mightily, exceedingly': 'adverb',  # B, adv. μεγάλως
        'very much, exceedingly': 'neuter',  # B.II
        'aloud, loudly': 'neuter',  # B.II, with verbs of sound
        'greater': 'comparative',  # μείζων (C.1)
        'too': 'comparative',  # cut by validate's cap: 'too great, too much, more than enough', μείζων (C.1)
        'too great, too much, more than enough': 'comparative',  # C.1, μείζων
    },
    'me/llw': {
        'expectation': 'infinitive',  # II.2, τὸ μέλλειν ἀγαθά
        'the future': 'participle',  # II.3, ὁ μ. χρόνος
        'things to come, the event, issue, future': 'participle',  # II.3, τὸ μέλλον, τὰ μέλλοντα
    },
    'me/sos': {
        'the middle, the space between': 'neuter',  # as Subst. τὸ μέσον
        'the difference, average': 'neuter',  # τὸ μέσον
        'the middle state or mean': 'neuter',  # τὸ μέσον
        'moderately': 'adverb',  # μέσως
        'a little': 'adverb',  # καὶ μέσως
        'in a middle way': 'adverb',  # μέσως βεβιωκέναι
    },
    'megalu/nw': {
        'to gain great glory': 'passive',  # Pass.
        'to boast oneself': 'middle',  # II Mid.
    },
    'mei/s': {
        'a month': 'particle',  # the units are ἦ μήν 'now verily', mh/n1; the alias mh/n → mei/s sends them to the month
        'a crescent': 'particle',  # μείς 2 = μηνίσκος; the units are the particle μήν
    },
    'metati/qhmi': {
        "to get rid of, transfer one's": 'middle',  # Mid. (II.3.b), τὸν φόβον
    },
    'mh=lon': {
        "girl's breasts": 'plural',  # II, pl., metaph.
    },
    'mhro/s': {
        'slices cut from the thighs': 'plural',  # 2, in pl. = μηρία
    },
    'mi/gnumi': {
        'to be mixed up with, mingled among': 'passive',  # B, Pass.
        'to be bound': 'passive',  # B, Pass., μίσγεσθαι ξενίῃ
        'to mingle with, hold intercourse with': 'passive',  # B, Pass.: a report cut of 'to mingle with, hold intercourse with, live with'
        'to mingle with, hold intercourse with, live with': 'passive',  # B, Pass.
        'to hold intercourse': 'passive',  # B, Pass.
        'to be brought into contact with': 'passive',  # B.2, Pass.
        'was rolled': 'passive',  # B.2, Pass., κάρη κονίῃσιν ἐμίχθη
        'to rea': 'passive',  # B.2, Pass., 'to reach, get at': the report cut it
        'to reach, get at': 'passive',  # B, Pass.
        'to go to join': 'passive',  # B, Pass.
        'to come to': 'passive',  # B, Pass. absol.
        'to mix in fight': 'passive',  # B, Pass., in hostile sense
        'to have intercourse with, to be united to': 'passive',  # B.4, Pass., of men and women
    },
    'mikro/s': {
        'but little': 'adverb',  # III.1 regul. adv., σμικρῶς
        'within a little, almost': 'genitive',  # III.2 adverbial usages
        'by a little': 'dative',  # III.3 μικρῷ, with the comp.
        'a little': 'accusative',  # III.4
    },
    'misqo/w': {
        'to contract': 'middle',  # II, Mid.
        'to be let on contract': 'passive',  # III, Pass., of a house
    },
    'mnhmoneu/w': {
        'to be remembered, had in memory': 'passive',  # Pass.
    },
    'mo/nos': {
        'the one only person, one above all others': 'superlative',  # Sup. μονώτατος
    },
    'molu/nw': {
        'to become vile': 'passive',  # Pass.
        'to wallow in': 'passive',  # Pass., ἐν ἀμαθίᾳ μολύνεσθαι
    },
    'mousiko/s': {
        'more accomplished in': 'comparative',  # II.2, c. inf., μουσικώτεροι
        'harmoniously, suitably': 'adverb',  # III, adv. -κῶς
    },
    'muria/s': {
        'consisting of': 'adjective',  # II, adj. 'consisting of 10,000': the number is cut from the tr
    },
    'ne/mw': {
        'to distribute among themselves': 'middle',  # A II Mid.
        'to maintain itself, be constituted': 'passive',  # A III Pass., of a country
        'go to pasture, graze': 'middle',  # B 2 Mid., of cattle
        'to eat': 'middle',  # B 2 Mid., of men
        'to spread': 'middle',  # B 2 Mid., of sores, ἐνέμετο
    },
    'ne/os': {
        'youths': 'plural',  # or alone, νέοι «youths»
        'newly, lately, just, just now': 'neuter',  # III neut. νέον as adv. of Time
        'most recently': 'superlative',  # III Sup. νεώτατα
    },
    'nea=nis': {
        'youthful': 'adjective',  # II as adj.
        'new': 'adjective',  # II 2
    },
    'no/mimos': {
        'conformable to custom, usage': 'not neuter',  # I; the units are the neuter plural noun
        'law, customary, prescriptive, established, lawful, rightful': 'not neuter',  # I; the units are the neuter plural noun
    },
    'nu/c': {
        'the goddess of Night': 'never',  # III Νύξ as prop. n., daughter of Chaos (cf. οὐρανός's Uranus in NOT_SENSES)
    },
    'o(/moios': {
        'more like': 'comparative',  # comp. ὁμοιότερος
        'most like': 'superlative',  # Sup. -ότατος
        'the peers': 'plural',  # οἱ ὅμοιοι
        'in like manner with': 'adverb',  # adv. ὅμοιον, ὅμοια; ὁμοίως
        'alike, equally': 'adverb',  # adv. ὁμοίως
    },
    'o(/s': {
        'where': 'singular',  # absol. usages: gen. sg. οὗ, of Place, like ὅπου
        'that, how that': 'singular',  # acc. sg. neut. ὅ for δι' ὅ or ὅτι
        'be': 'singular',  # cut from «because»: ὅ for ὅτι, Lat. quod
        'wherefore': 'singular',  # acc. sg. neut. ὅ, also «wherefore», Lat. quapropter
    },
    'o(/sos': {
        'how far, how much': 'neuter',  # III.1b
        'how': 'neuter',  # III.1b with adjs., ὅσον μέγα
        'only so far as, only just': 'neuter',  # III.2
        'only': 'neuter',  # III.2 εἰ μὴ ὅσον γραφῇ
        'about, nearly': 'neuter',  # III.3 ὅσον τε, of distances
        'so far as, inasmuch as': 'neuter',  # III.4 with adjs.
        'by how much': 'dative',  # IV ὅσῳ, ὅσῳ περ
    },
    'o(moio/w': {
        'to make a like return': 'middle',  # 3, in Mid. also
    },
    'o(mologe/w': {
        'I grant': 'first person active',  # ὁμολογῶ σοι, I grant you
        'to be agreed upon, allowed or granted by common consent': 'passive',  # Pass.
        'to be allowed or confessed to be': 'passive',  # Pass., c. inf.
        'it is granted, allowed': 'passive',  # Pass., ὁμολογεῖται
        'things granted': 'passive participle',  # τὰ ὁμολογούμενα
    },
    'o(ra/w': {
        'to let on': 'passive',  # cut at validate's 200-char limit (GEN 2:19); full: to let oneself be seen, appear (Pass.)
        'to let oneself be seen, appear': 'passive',  # Pass., like φαίνομαι
        'all that is seen, things visible': 'neuter plural',  # τὰ ὁρώμενα
        'to have sight': 'not passive',  # intransitive
        'take heed, beware': 'not passive',  # absol.
    },
    'o(rma/w': {
        'think': 'middle or passive',  # B.1, c. inf.
        'he purposed': 'middle or passive',  # B.1, τὸν ὥρμητο λέγειν
        'eagerly': 'middle or passive',  # B.1, ὁρμηθέντε
        'to hasten after': 'middle or passive',  # B.2, c. gen.
        'to make a place his headquarters or base of operations': 'middle or passive',  # B.3, of a general
        'setting out, beginning': 'middle or passive',  # B.3, ὁρμώμενος
        'to h': 'middle or passive',  # B.4, 'to hasten, be eager': the report cut it
        'to hasten, be eager': 'middle or passive',  # B.4, Mid. and Pass.
        'to go forth': 'middle or passive',  # B.4, τὸ φέγγος ὁρμάσθω
        'incited': 'passive',  # B.5, in a really pass. sense, πρὸς θεῶν ὡρμημένος
    },
    'o)/mnumi': {
        'has been sworn by, adjured': 'passive',  # III, Pass., ὀμώμοσται Ζεύς
    },
    'o)/yis': {
        'the organs of sight, the eyes': 'plural',  # II, in pl.
    },
    'o)li/gos': {
        'little, a little, slightly': 'neuter',  # III, neut. ὀλίγον as adv.
        'all but, almost': 'genitive',  # IV.1, ὀλίγου alone
    },
    'o)rqo/s': {
        'really, truly': 'adverb',  # III.3, ὀρθῶς 'really, truly'
        'a right angle': 'feminine',  # IV.2, ἡ ὀρθή (sub. γωνία)
        'the nominative': 'feminine',  # IV.3, ἡ ὀρθή (sub. πτῶσις), Lat. casus rectus
    },
    'o)rqo/w': {
        'to succeed, prosper': 'passive',  # Pass.
        'success': 'neuter participle',  # τὸ ὀρθούμενον
        'to be upright, deal justly': 'passive',  # III 3, in Pass. also
        "to rise from one's seat, stand up": 'passive',  # Pass., simply
    },
    'o)ru/ssw': {
        'dug or quarried': 'middle',  # II, Mid., λίθους ὀρύξασθαι 'to have stones dug or quarried'
    },
    'oi)/omai': {
        'I ween': 'first person',  # III, ὀίω used parenthetically in first person
        'I believe you, of course, no doubt': 'first person',  # III 2
        "don't you think so? what think you": 'second person',  # οἴει; as a question
        'I think, I suppose, I believe': 'first person',  # οἶμαι, parenthetic
        'think you': 'second person',  # πῶς οἴει; parenthetic
    },
    'oi)=da': {
        'my witness': 'imperative',  # the Imperat. in protestations, ἴστω Ζεύς
    },
    'oi)=kos': {
        'homeward, home': 'accusative',  # acc. οἶκον, = οἴκονδε, οἴκαδε
        'a single house': 'plural',  # pl. οἶκοι for «a single house», Lat. aedes
    },
    'oi)ke/w': {
        'to be situate, to lie': 'passive',  # A.2, Pass., of cities
    },
    'oi)kodome/w': {
        'will be emboldened': 'passive',  # Pass., οἰκοδομηθήσεται
    },
    'ou(=tos': {
        'yes': 'neuter plural',  # neut. ταῦτα, ταῦτ᾽ ὦ δέσποτα
        'therefore': 'neuter plural',  # ταῦτα absol.; also διὰ ταῦτα
        'on this spot, here': 'dative',  # dat. fem. ταύτῃ
        'in this p': 'dative',  # cut at validate's 200-char limit; full: in this point, herein (ταύτῃ)
        'in this point, herein': 'dative',  # ταύτῃ
        'in this way, thus': 'dative',  # ταύτῃ
    },
    'ou)dei/s': {
        'nobodies': 'plural',  # II.3 in pl., οὐδένες
        'not at all, naught': 'neuter',  # III, neut. οὐδέν as adv.
    },
    'pa=s': {
        'all things': 'neuter plural',  # πάντα γίγνεσθαι
        'everything': 'neuter',  # εἰς πᾶν; πάντα εἶναί τινι
        'in all points': 'neuter plural',  # cut at validate's 200-char limit; full: in all points, entirely, wholly (πάντα as adv.)
        'in all points, en': 'neuter plural',  # cut at validate's 200-char limit; full: in all points, entirely, wholly (πάντα as adv.)
        'everything, anything': 'neuter singular',  # πᾶν
        'anything': 'neuter singular',  # πᾶν
        "the whole, one's all": 'neuter singular',  # τὸ πᾶν
    },
    'pai/zw': {
        'in jest, jestingly': 'participle',  # II, the part. παίζων used absol.
        'is jocularly told': 'passive',  # II, Pass., ὁ λόγος πέπαισται
    },
    'paida/rion': {
        'young children': 'plural',  # in pl.
    },
    'parakrou/w': {
        'to be led astray, go wrong': 'passive',  # I, Pass.; so also in Mid.
    },
    'paralu/w': {
        'to be parted from': 'passive',  # Pass., τινος (II)
        'to be exempt': 'passive',  # Pass., from service (II)
        'to be disabled at the side, to be paralysed': 'passive',  # in Pass. (IV)
        'to be exhausted, to flag': 'passive',  # IV, of camels
    },
    'parati/qhmi': {
        'to deposit what belongs to one': 'middle',  # B.2 Mid.
        'give in charge, commit': 'middle',  # B.2 Mid.
        'to venture, stake, hazard': 'middle',  # B.3 Mid., παρθέμενοι κεφαλάς
        'to employ': 'middle',  # B.4 Mid.
    },
    'pari/sthmi': {
        'to make to stand or to place beside': 'active',  # A Causal in pres., imperf., fut. and aor1
        'to set before the mind, present, offer, bring home to the mind': 'active',  # A.II causal
        'to give': 'active',  # A.II π. τινὶ θαρρεῖν «to give» one confidence
        'to make good, prove, shew': 'active',  # A.II.2 causal
        'to set side by side, compare': 'active',  # A.III causal
        'to bring forward, produ': 'middle',  # cut from «to bring forward, produce»: C some tenses of Mid., esp. fut. and aor1, causal
        "to bring to one's side": 'middle',  # C.II
        'to bring over by force, bring to terms': 'middle',  # C.II.1
        'to gain by kindness, win over': 'middle',  # C.II.2
        "to dispose for one's own views or purposes": 'middle',  # C.II.3
        'to bring forward, produce': 'middle',  # C.I, some tenses of Mid., esp. fut. and aor1, causal
    },
    'parqe/nos': {
        'maiden, virgin, chaste': 'adjective',  # II, as adj.
        'an unmarried man': 'masculine',  # III, as masc., NTest.
    },
    'path/r': {
        'forefathers': 'plural',  # in pl. fathers, i.e. forefathers
    },
    'pe/mpw': {
        'to be carried in procession': 'passive',  # III, in Pass.
        "to send for oneself, to send in one's own service or cause": 'middle',  # B.II, Mid.
    },
    'peina/w': {
        'a hungry man': 'participle',  # πεινᾶντι
    },
    'peira/zw': {
        'to be sorely tempted, to be tempted to sin': 'passive',  # II, Pass., NTest.
    },
    'periaire/w': {
        'to be stript of': 'passive',  # II Pass. c. acc. rei
    },
    'periba/llw': {
        'the space enclosed, enclosure': 'passive',  # III, Pass., τὸ περιβεβλημένον
        'to have come into possession of': 'perfect passive',  # IV, perf. pass.
    },
    'perisso/s': {
        'greater things': 'comparative',  # I 4, περισσότερα, greater things than
        'greater things than': 'comparative',  # I.4, περισσότερα, as decided for 'greater things'
        'greater than': 'comparative',  # I.4, περιττότερος προφήτου
        'extravagancies': 'neuter plural',  # II.3, περισσὰ μηχανᾶσθαι
        'extraordinarily, exceedingly': 'adverb',  # B, adv. περισσῶς
        'overmuch': 'adverb',  # B, περισσῶς, educated overmuch
        'in a peculiar manner, remarkably': 'adverb',  # B.2, adv. (also περισσά)
        'more sumptuously': 'comparative',  # B.2, περισσότερον τῶν ἄλλων θάψαι
        'in vain': 'neuter plural',  # B.4, τὰ περισσά
    },
    'peristre/fw': {
        'to be turned round, spin round': 'passive',  # 1 Pass.
    },
    'perite/mnw': {
        'to make incisions all round': 'middle',  # Mid.
        'they practise circumcision': 'middle',  # Mid., περιτάμνονται
        'to be curtailed of': 'passive',  # I.3 Pass., περιτάμνεσθαι γῆν
        'to be cut off, intercepted': 'passive',  # II Pass.
    },
    'periti/qhmi': {
        'to put round oneself, put on': 'middle',  # I, Mid.
    },
    'ph/gnumi': {
        'to become solid, stiff or hard': 'perfect or passive',  # intr. perf. and Pass.
        'to become congealed, freeze': 'perfect or passive',  # III, intr. perf. and Pass., of liquids
        'to be irrevocably fixed, established': 'perfect or passive',  # IV, intr. perf. and Pass.
    },
    'pi/mplhmi': {
        "to satiate one's": 'middle',  # Mid., θυμὸν πλήσασθαι (II)
        'to be filled, become or be full of': 'passive',  # Pass. (III)
        'to have enough of': 'passive',  # Pass. (III.2)
    },
    'pikro/s': {
        'bitterly, cruelly': 'adverb',  # C, adv. πικρῶς
    },
    'pisteu/w': {
        'to believe mutually': 'middle',  # I Mid.
        'to comply': 'not passive',  # absol.
        'to dare': 'not passive',  # c. inf.
    },
    'pla/gios': {
        'placed sideways, slanting, aslant': 'noun',  # I
        'not straightforward, crooked, treacherous': 'noun',  # II, metaph.
    },
    'pla/ssw': {
        'to be moulded, made': 'passive',  # Pass.
        'fictitious': 'passive',  # Pass., οὐ πεπλασμένος
    },
    'platu/nw': {
        'is opened, enlarged': 'passive',  # metaph., ἡ καρδία πεπλάτυνται, perf. pass.
        'to grow broad, widen out': 'passive',  # Pass. «to grow broad, widen out»
    },
    'platu/s': {
        'wide, broad': 'adjective',  # I, the adjective: not the noun
        'flat, level': 'adjective',  # II, the adjective
        'broad-shouldered': 'adjective',  # II, the adjective
        'flatly, merely': 'neuter',  # neut. as adv.
        'salt, brackish': 'adjective',  # of liquids, the adjective
        'a street': 'noun',  # III, as Subst., ἡ πλατεῖα
        'the flat of the hand': 'noun',  # III, as Subst., ἡ πλατεῖα
    },
    'plhqu/nw': {
        'to be in the majority, to prevail': 'passive',  # Pass.
    },
    'plhro/w': {
        'fully observed': 'passive',  # III.4 Pass., νόμοι πληρούμενοι
        'to crowd in': 'passive',  # Pass.
        'comes in full': 'not passive',  # intr.
    },
    'poie/w': {
        'to take': 'middle',  # Mid., ποιεῖσθαί τινα ἄλοχον
        'to adopt': 'middle',  # Mid., ποιεῖσθαί τινα υἱόν
        'to hold, deem, consider, reckon, esteem': 'middle',  # V. in Mid.
        'to deem': 'middle',  # V. in Mid., μέγα π.
        'those who are reputed . .': 'passive participle',  # οἱ ποιούμενοι
        'spend': 'middle',  # τὴν νύκτα ἐφ᾽ ὅπλοις ποιεῖσθαι
        'to put the case assume': 'imperative',  # ποίει, put the case, assume
        'to oneself': 'middle',  # to take her to oneself as wife
        'to act': 'not passive',  # intr.
        'to work, operate': 'not passive',  # absol., of medicine
    },
    'poiki/los': {
        'in double sense': 'adverb',  # III.3, adv. ποικίλως
        'd': 'adverb',  # III.4, ποικίλως ἔχειν 'to be different': the report cut it
        'different': 'adverb',  # III.4, ποικίλως ἔχειν 'to be different'
    },
    'polu/s': {
        'the greater number': 'plural',  # II.3
        'the people, the commonalty': 'plural',  # οἱ πολλοί, like τὸ πλῆθος
        'of the multitude': 'plural',  # εἷς τῶν πολλῶν
        'the most': 'neuter plural',  # II.3.c
        'ver': 'neuter plural',  # cut by validate's cap: 'very much, too much' (II.4)
        'very much, too much': 'neuter plural',  # II.4, the pl. πολλά with Verbs, as decided for the cut 'ver'
        'much, very': 'neuter',  # III.1.a, neut. πολύ, πολλά
        'many times, ofttimes, often, much': 'neuter',  # III.1.a, of repetition
        'far, very much': 'neuter',  # III.1.b, of Degree
        'very': 'genitive',  # III.1.b, absol. gen. πολλοῦ
        'a great way, far': 'neuter',  # III.1.c, of Space, οὐ πολλόν
        'much, far': 'neuter',  # III.2.a, with a comp., πολὺ κάλλιον
    },
    'ponhri/a': {
        'knavish tricks, rogueries': 'plural',  # in pl.
    },
    'ponhro/s': {
        'the evil one': 'masculine',  # ὁ π.
    },
    'poreu/w': {
        'to carry or ferry over': 'active',  # Act., c. dupl. acc.
    },
    'pou/s': {
        'the arms': 'plural',  # in pl., a bird's talons; «the arms» of a polypus
        'the lower corners of the sail or the ropes fastened thereto, the sheets': 'plural',  # II.2, in a ship, πόδες
    },
    'pra/ssw': {
        'those who were treating with': 'participle',  # οἱ πράσσοντες αὐτῷ, articular participle
        'the traitors': 'participle',  # οἱ πράσσοντες, articular participle
        'was a-practising': 'passive',  # Pass., of secret practices, ἐπράσσετο
        'called on to pay up': 'passive',  # V.2, Pass., πεπραγμένος τὸν φόρον
        'to exact for oneself': 'middle',  # V.2, Mid., πράξασθαί τινα ἀργύριον
        'I had exacted': 'passive',  # V.2, ἐπεπράγμην, plup. pass. in mid. sense
    },
    'pra=gma': {
        'circumstances, affairs': 'plural',  # III in pl., πράγματα
        'the business of life': 'plural',  # III.1 ἀπηλλάχθαι πραγμάτων
        'state-affairs': 'plural',  # III.2
        'power': 'plural',  # III.2 τὰ Περσικὰ πρ.
        'the government': 'plural',  # III.2 καταλαμβάνειν τὰ πρ.
        'power or office': 'plural',  # III.2 οἱ ἐν τοῖς πράγμασι
        'private affairs or circumstances': 'plural',  # III.3, in pl.
        'troublesome business, trouble, annoyance': 'plural',  # III.4, in pl., in bad sense
    },
    'pre/sbus': {
        'an old man': 'positive',  # I πρέσβυς, Lat. senex
        'chiefs, princes': 'plural',  # I, pl. πρέσβεις
        'eldest': 'superlative',  # Sup. πρεσβύτατος
        'an ambassador': 'plural',  # II like πρεσβευτής
        'a chief, president': 'positive',  # III; the comp. πρεσβύτερος is «an elder of the Jewish Council»
    },
    'pro/': {
        'before, in front, forth, forward': 'adverb',  # πρό absol. as adv., of place
        'before, beforehand': 'adverb',  # πρό absol. as adv., of time
        'before, earlier': 'adverb',  # πρό absol. as adv., of time
        'prematurely': 'adverb',  # πρό absol. as adv., of time
    },
    'pro/keimai': {
        'the corpse laid out': 'participle',  # ὁ προκείμενος
        'in hand': 'participle',  # τὸ προκείμενον πρῆγμα
        'initial': 'participle',  # γράμμα πρ., an initial letter
    },
    'proaire/w': {
        'to choose before or sooner than': 'middle',  # Mid.
    },
    'probai/nw': {
        'to put forward, advance': 'active',  # V Causal, in fut. act.
    },
    'proekfe/rw': {
        'to be carried away headlong': 'passive',  # LSJ II Pass.
    },
    'proora/w': {
        'foresight': 'infinitive',  # τὸ προορᾶν σευ, your foresight
        'to foresee': 'middle',  # II 2, in attic also in Mid.
    },
    'prosa/gw': {
        'to attach oneself to': 'passive',  # II, Pass.
        "to bring or draw to oneself, attach to oneself, bring over to one's side": 'middle',  # B, Mid., Lat. sibi conciliare
        'to draw to oneself, embrace': 'middle',  # B.2, Mid., absol.
        'to induce': 'middle',  # B.3, Mid., c. inf.
        'to take to oneself, to take up': 'middle',  # B.II, Mid., ὀστᾶ
        'to procure, import': 'middle',  # B.II, Mid.
    },
    'prose/xw': {
        'attentively': 'participle',  # absol., προσέχων ἀκουσάτω
        'to attach oneself to': 'middle',  # Mid. (I.5)
        'cleave to`': 'middle',  # cut by validate's cap: 'cleave to' (Mid., I.5)
        'cleave to': 'middle',  # I.5, Mid., c. dat.
        'to be held fast by': 'passive',  # I.6, Pass., ὑπό τινος
        'to be implicated in': 'passive',  # I.6, Pass., metaph., c. dat.
    },
    'prosfe/rw': {
        'to be borne towar': 'passive',  # cut by validate's cap: 'to be borne towards' (B, Pass.)
        'to be borne towards': 'passive',  # B, Pass., as decided for the cut 'to be borne towar'
        'to put in': 'passive',  # B, Pass., of ships
        'to go against, attack, assault': 'passive',  # B, Pass.
        'to rush on, make an onset': 'passive',  # B, Pass.
        'to engage': 'passive',  # B, Pass.
        'to go to or towards': 'passive',  # B.3, Pass.
        'sailing': 'passive',  # B, Pass., προσφερόμενοι
        'to deal with, behave oneself': 'middle only',  # Mid.
        'to answer': 'passive',  # B, Pass., προσφέρεσθαι πρὸς λόγον
        'to come near': 'passive',  # B, Pass.
        'be like': 'passive',  # B.5, προσφέρεσθαί τινι
        'to be put or imposed upon': 'passive',  # B.II, προσφέρεσθαί τινι
        'to take to oneself as meat or drink': 'middle',  # C, Mid.
        'meat or drink, food': 'passive participle',  # Pass., τὰ προσφερόμενα
        'to exhibit': 'middle',  # C.2, Mid., φιλοτιμίαν ὑμῖν
        'to apply or cause to be applied': 'middle',  # C.3, Mid.
        'make an offer': 'not passive',  # no passive
    },
    'proskale/w': {
        'to cite or summon into court': 'middle',  # II.2, under Mid., in attic of an accuser
        'to be summoned': 'passive',  # II.2, Pass.
        'the party summoned': 'passive participle',  # ὁ προσκληθείς
        'to cite as witness': 'middle',  # II.3, under Mid.
    },
    'prosti/qhmi': {
        'to associate oneself to': 'middle',  # B, Mid., absol.
        'to be well-inclined': 'middle',  # B, Mid., πρ. τῷ ἀστῷ
        'to come in, submit': 'middle',  # B, Mid., absol.
        "to give one's assent, agree to`": 'middle',  # cut by validate's cap: 'to give one's assent, agree to' (B.2, Mid.)
        "to give one's assent, agree to": 'middle',  # B.2, Mid., c. dat.
        'will deposit': 'middle',  # B.3, ψῆφον … προσθήσομαι
        'to associate with oneself': 'middle',  # B.II, Mid., c. acc. pers.
        'take to one as a friend or ally, win over': 'middle',  # B.II, Mid.
        'take': 'middle',  # B.II, ταύτην προσθοῦ δάμαρτα, take her to wife
        'to add to oneself, gain': 'middle',  # B.II.2, Mid., c. acc. rei
        'to bring upon oneself': 'middle',  # B.II.2, Mid., of evils
        'to bring upon': 'middle',  # B.II.2.b, Mid., others
        'to vent': 'middle',  # B.II.2.b, μῆνιν προσθέσθαι τινί
        'to make additions, to augment': 'not passive',  # absol.
    },
    'pw=los': {
        'a young man': 'masculine',  # more rarely masc., a young man
    },
    'qa/llw': {
        'luxuriant, exuberant': 'participle',  # part. perf. τεθηλώς, τεθαλυῖα, as adj.
    },
    'qa/natos': {
        'kinds of death': 'plural',  # pl. θάνατοι
        'the dead': 'plural',  # νεκρός in pl., through III = νεκρός
    },
    'qauma/sios': {
        'wonderfully': 'neuter',  # θαυμάσιον ὅσον
        'exceedingly': 'adverb',  # I 2 adv. -ίως, i.e. exceedingly
        'marvellously': 'adverb',  # I 2, θ. ὡς ἄθλιος
    },
    'qauma/zw': {
        'to receive': 'passive',  # II.2 Pass., τὰ εἰκότα θ. «to receive» proper «marks of respect»
        'marks of respect': 'passive',  # II.2 Pass., the rest of «to receive» proper «marks of respect»
    },
    'qei=os': {
        'the Divine Being, the Divinity, Deity': 'neuter',  # II, θεῖον, τό
        'divine things, the acts and attributes of the gods, the course of providence': 'neuter plural',  # II 2, θεῖα, τά
        'religious observances': 'neuter plural',  # II 2, θεῖα, τά
        'religion': 'neuter plural',  # II 2, ἔρρει τὰ θεῖα
        'by divine providence': 'adverb',  # III adv. θείως
        'by special provide': 'comparative',  # III, θειοτέρως; string cut by the 200-char message, card item 'by special providence'; lat
        'by special providence': 'comparative',  # III, θειοτέρως
    },
    'qu/ra': {
        'double or folding doors': 'plural',  # mostly in pl. (I)
    },
    'qu/w': {
        'the flesh of the victim': 'neuter plural',  # Pass., τὰ τεθυμένα
        'to cause to be offered, to have a victim slain': 'middle',  # II Mid.
        'to take the auspices': 'middle',  # II Mid., 'and so'
        'I consult the auspices': 'middle',  # II Mid., θύομαι ἰέναι
        'to tear in pieces': 'middle',  # metaph., within II Mid.
    },
    'qumia/w': {
        'to be burnt': 'passive',  # Pass.
    },
    'r(a/bdos': {
        'fasces': 'plural',  # 7, αἱ ῥάβδοι, of the Roman lictors
    },
    'r(a/ptw': {
        'sewed up': 'passive',  # Pass., ἐρράφθαι τὸ χεῖλος
    },
    'r(h/gnumi': {
        'to break for oneself, get broken': 'middle',  # Mid. «to break for oneself, get broken»
        'to break oneself a way through': 'middle',  # in Mid., ῥήξασθαι φάλαγγας
        "to break or force one's": 'middle',  # absol., ῥήξασθαι «to break» or «force one's» way
        'to beat the g': 'never',  # cut from «to beat the ground, dance»: II absol. in the form ῥήσσω
        'to beat the ground, dance': 'never',  # II, absol. in the form ῥήσσω
        'to be wrecked': 'passive',  # B.4, Pass., of ships
        'to break its bounds': 'perfect or passive',  # C, intr., like Pass.
    },
    'ske/ptomai': {
        'well-considered': 'passive',  # II 3, ἐσκεμμένα
    },
    'skeu=os': {
        'furniture, house-gear, utensils, chattels': 'plural',  # 1, pl. in collective sense
        'accoutrements, equipment': 'plural',  # 1, pl. collective, esp. military
        'baggage, luggage': 'plural',  # 1, pl. collective
    },
    'so/s': {
        'thy business': 'singular',  # σὸν ἔργον, c. inf.; so, σόν [ἐστι] alone
        'thy kinsfolk, people': 'plural',  # οἱ σοί
        'what concerns thee, thy interest, words, purpose': 'singular',  # τὸ σόν
        'thy property': 'neuter plural',  # τὰ σά «thy property»
        'thy interests': 'neuter plural',  # τὰ σά, «thy interests»
    },
    'sofo/s': {
        'cleverly, wisely': 'adverb',  # III adv. σοφῶς
    },
    'stre/fw': {
        'tossing': 'middle or passive',  # B, of one tossing in bed
        'to turn back, return': 'middle or passive',  # B.2
        'to twist about': 'middle or passive',  # B.II
        'to twist and turn, shuffle': 'middle or passive',  # B.II, in argument
        'to turn and change': 'middle or passive',  # B.II.2
        'to twist oneself up with': 'middle or passive',  # B.III
        'stick close': 'middle or passive',  # B.III
        'to be at large, go about': 'middle or passive',  # B.III.2
        'to turn': 'middle',  # cut by validate's cap: 'to turn about with oneself, take back' (C, strict Mid.)
        'to turn about with oneself, take back': 'middle',  # C, in strict Mid. sense
        'to wheel about': 'active',  # D, intr. in Act., of soldiers
    },
    'sugkalu/ptw': {
        'muffled up': 'passive',  # Pass., συγκεκαλυμμένη
        "to wrap oneself up, cover one's face": 'middle',  # Mid.
    },
    'sugxe/w': {
        'to be in confusion': 'passive',  # I Pass.
    },
    'sullamba/nw': {
        'quickly, in a hurry': 'participle',  # absol. in part., ξυλλαβών
        'quick': 'participle',  # cut by validate's cap: 'quickly, in a hurry', ξυλλαβών
        'they were arrested': 'passive',  # II.2, Pass., πρὶν ξυλληφθῆναι
    },
    'sulle/gw': {
        "to collect for oneself, for one's own use": 'middle',  # I Mid.
        'to come together, become customary': 'passive',  # I 3 Pass.
        'to come together, assemble': 'passive',  # II Pass., of persons
    },
    'sumbai/nw': {
        'to be agreed on': 'passive',  # II Pass., of the terms
        'a chance event, contingency': 'participle',  # τὸ συμβεβηκός
    },
    'sumbiba/zw': {
        'to be joined or knit together, framed': 'passive',  # I Pass.
    },
    'sumbolh/': {
        'contributions': 'plural',  # IV, in pl., συμβολαί
    },
    'sumpodi/zw': {
        'to be entangled in a net': 'passive',  # I, Pass.
    },
    'suna/gw': {
        'to engage': 'not passive',  # intr.
    },
    'sunapo/llumi': {
        'to perish together': 'passive',  # Pass. «to perish together»
    },
    'sunariqme/w': {
        'to be counted with others, to be taken into account': 'passive',  # Pass.
    },
    'sune/xw': {
        'to be constrained, oppressed, afflicted': 'passive',  # I.4 Pass.
        'to meet': 'not passive',  # intr.
    },
    'suneto/s': {
        'intelligently': 'adverb',  # III adv. -τῶς
        'intelligibly': 'adverb',  # III 2
    },
    'suni/sthmi': {
        'the conspirators': 'participle',  # τὸ ξυνιστάμενον, οἱ ξυνεστῶτες
        'to arise, bec': 'passive',  # string cut by the 200-char message; card item 'to arise, become, take place' (B IV 2); lat
        'a well-disciplined': 'participle',  # B.IV.3, ξυνεστὼς στρατός
        'a standing': 'participle',  # B.IV.3, στράτευμα συνεστηκός
    },
    'sunoike/w': {
        'to be thickly peopled': 'passive',  # II, Pass., of a country
    },
    'sunta/ssw': {
        'to be drawn up in line': 'passive',  # I Pass.
        'to form in line': 'middle',  # I, so in Mid.
        'to be collected, resolute, steady': 'passive',  # I 2, in Pass., of single persons
        'to be organised for paying contributions': 'passive',  # II 2 Pass.
        'to agree to such assessment': 'middle',  # II 2 Mid.
        'to agree together': 'middle',  # III Mid.
        'to take leave of': 'middle',  # IV Mid., σ. τινι
        'bi': 'middle',  # string cut by the 200-char message; card item 'bid' (IV Mid., 'bid him farewell', with 'fa
        'bid': 'middle',  # IV, Mid., σ. τινι, bid him farewell
        'farewell': 'middle',  # IV, Mid., rest of 'bid him farewell'
    },
    'suntele/w': {
        'to belong to a class, be counted in it': 'not passive',  # intr.
        'to pay towards common expenses, contribute': 'not passive',  # absol.
        'tributary or subject to': 'not passive',  # συντελεῖν εἰς, intr.
    },
    'sw/zw': {
        'to come safe, escape to': 'passive',  # II in Pass., a place
    },
    'swth/rios': {
        'more likely to bring safety': 'comparative',  # comp. -ιώτερος
    },
    'sxolh/': {
        'in a leisurely way, tardily': 'dative',  # B, σχολῇ as adv.
        'scarcely, hardly, not at all': 'dative',  # B 2, σχολῇ, at one's leisure i.e. scarcely
    },
    'ta/fos': {
        'a single grave': 'plural',  # II, in pl. of a single grave
    },
    'ta/ssw': {
        'in rank and file': 'passive',  # absol., τεταγμένοι
        'to fall in, form in order': 'middle',  # Mid., of battle (I)
        'to join': 'passive',  # Pass., πρὸς τὴν ξυμμαχίαν ταχθῆναι
        'agree to pay': 'middle',  # Mid., 'to take a payment on oneself' (III.3)
        'to agree upon, settle': 'middle',  # in Mid. (III.4)
        'to take a payment on oneself': 'middle',  # III.3, Mid., φόρον τάξασθαι
        'fixed, prescribed': 'passive',  # III.6, in perf. part. pass., ὁ τεταγμένος χρόνος
    },
    'tara/ssw': {
        'to cause confusion': 'not passive',  # absol.
    },
    'taxu/s': {
        'quick, swift, fleet': 'not adverb',  # I
        'quick, rapid, hasty': 'not adverb',  # II
        'speed, haste': 'neuter',  # II, τὸ ταχύ
        'quick, rapid, sudden': 'not adverb',  # II.2
        'fleeting': 'not adverb',  # II.2, τ. ἐλπίδες
        'sooner': 'comparative',  # C.I.2, neut. θᾶσσον as adv.
        'rather': 'comparative',  # C.I.2, neut. θᾶσσον as adv.
    },
    'te/knon': {
        'my son, my child': 'vocative',  # τέκνον, in address
    },
    'te/leios': {
        'a royal banquet': 'neuter',  # IV
        'at last': 'adverb',  # V
        'perfectly': 'adverb',  # cut by validate's cap: 'perfectly, absolutely, thoroughly' (V.2)
        'perfectly, absolutely, thoroughly': 'adverb',  # V.2, adv. τελέως
    },
    'teknopoie/w': {
        'to breed children': 'middle',  # in Mid. of both parents
    },
    'teleuta/w': {
        'to be fulfilled, to come to pass, happen': 'passive',  # Pass. «to be fulfilled, to come to pass, happen»
        'at the end, at last': 'participle',  # II.4 the part. τελευτῶν used as adv.
    },
    'tetra/gwnos': {
        'a body of men drawn up in square': 'neuter',  # τετράγωνον, ου
    },
    'thre/w': {
        'to be constantly guarded': 'passive',  # Pass.
    },
    'ti/ktw': {
        'the parents': 'active participle',  # οἱ τεκόντες
        'the father': 'active participle',  # ὁ τεκών
        'the mother': 'active participle',  # ἡ τεκοῦσα
        'to bear young, breed': 'not passive',  # intr.
        'to lay eggs': 'not passive',  # its object the eggs
    },
    'ti/qhmi': {
        'to vote': 'middle',  # τίθεσθαι absol.
        'to lay up': 'middle',  # Mid., θέσθαι θυμὸν ἐν στήθεσσι
        'to harbour': 'middle',  # Mid., θέσθαι τινὶ κότον
        'the deposits': 'passive participle',  # τὰ τεθέντα
        'to settle, end': 'middle',  # πόλεμον θέσθαι
        'the prizes': 'passive participle',  # τὰ τιθέμενα
        'to give': 'middle',  # Mid., ὄνομα θέσθαι
        'to give oneself': 'middle',  # Mid., of republican legislatures
        'make': 'middle',  # Mid., make a law
        'adopt': 'middle',  # υἱὸν τίθεσθαί τινα
        'to make for oneself': 'middle',  # in Mid.
        'to make oneself': 'middle',  # θέσθαι κέλευθον
        'to get': 'middle',  # μεγάλην ἐπιγουνίδα θέσθαι
        'to work oneself': 'middle',  # θέσθαι πόνον
    },
    'toiou=tos': {
        'such a proceeding': 'neuter',  # 3, τοιοῦτον or τὸ τ.
        'just so, even so': 'neuter plural',  # 4, τοιαῦτα affirms
        'and such-like': 'neuter plural',  # 5, τὰ πλοῖα, τὰ τοιαῦτα
        'in such wise': 'neuter plural',  # 6, τοιαῦτα as an adv.
    },
    'tre/fw': {
        'to become firm': 'passive',  # Pass., with intr. perf. act. τέτροφα
        'to bred, reared': 'passive',  # II.2 Pass. «to bred, reared» (sic, for to be bred)
        'to have within oneself, to contain, keep, have': 'not passive',  # no passive
    },
    'tri/bolos': {
        'a threshing-machine, boards with sharp stones fixed in the bottom': 'plural',  # τρίβολοι, οἱ (II)
    },
    'u(eto/s': {
        'rainiest': 'superlative',  # II as adj. in Sup. ὑετώτατοι
    },
    'u(polei/pw': {
        'to remain in force': 'passive',  # Pass., of things
        'to stay behind': 'passive',  # Pass.
        'to lag behind': 'passive',  # Pass.
        'to fall behind': 'passive',  # Pass.
        'to be inferior to': 'passive',  # II.5, Pass.
        'to fail, come to an end': 'not passive',  # intr., of things
        'to fail': 'not passive',  # intr., of things
    },
    'u(postre/fw': {
        'reversely': 'participle',  # II.4 part. ὑποστρέψας as adv.
    },
    'u(poti/qhmi': {
        'to be laid down, assumed': 'passive',  # I.2, Pass.
        'to lay down as a principle, take for granted, assume': 'middle',  # I.2, Mid.
        'to assume or suppose that . .': 'middle',  # I.2, Mid., c. acc. et inf.
        'to suggest, hint': 'middle',  # II, so in Mid., ὑποθέσθαι τινὶ βουλήν
        'advise or counsel': 'middle',  # II, Mid., ἔπος, ἔργον ὑποθέσθαι τινί
        'to advise, admonish': 'middle',  # II.2, ὑποθέσθαι τινί, c. dat. pers. only
        'to propose to oneself': 'middle',  # II.3, Mid.
        'to lend': 'middle',  # III, in Mid., of the mortgagee
    },
    'u(yhlo/s': {
        'loftily': 'neuter plural',  # ὑψηλὰ κομπεῖν to talk «loftily»
    },
    'w(rai=os': {
        'the summer season': 'feminine',  # ἡ ὡραία
    },
    'xa/ris': {
        'graces, charms': 'plural',  # of persons, pl. (I)
        'sake': 'accusative',  # VI.1, acc. sg. as adv., for his sake
        'pleasure or sake': 'accusative',  # VI.1, ἐμὴν χάριν, σὴν χάριν
        'Charis': 'never',  # B, as a mythological pr. n., wife of Hephaestus
        'the Charites or Graces': 'never',  # B.2, mostly in pl. Χάριτες
    },
    'xai/rw': {
        'hail, welcome': 'imperative',  # III 1, χαῖρε at meeting
        'fare-thee-well, farewell, good-bye': 'imperative',  # III 2, χαῖρε at parting
        'glad, joyful, delighted': 'participle',  # IV, part. χαίρων
        'safe, with impunity': 'participle',  # IV 2, χαίρων joined with another Verb
    },
    'xitw/n': {
        'the upper leather': 'plural',  # of a shoe, in pl. (III)
    },
    'xra/omai': {
        'he was endowed': 'pluperfect',  # φρεσὶ κέχρητ' ἀγαθῇσι; I.7 the perf. as strengthened pres.
        'to be in need or want of, to yearn after': 'perfect',  # I.6 perf. κέχρημαι
        'needy, in need, poor': 'participle',  # I.6 part. κεχρημένος used as an adj.
        'to be used': 'passive',  # I.8 aor1 pass. χρησθῆναι
    },
    'xrh/simos': {
        'advantage': 'neuter',  # τὸ αὐτίκα χρ., present advantage
    },
    'xristo/s': {
        'to be rubbed on': 'adjective',  # the adjective's
        'anointed': 'adjective',  # the adjective's
        'salves': 'neuter plural',  # τὰ χριστά
    },
    'xroni/zw': {
        'to be prolonged or protracted': 'passive',  # II Pass.
        'to grow up': 'passive',  # II 2 under Pass., χρονισθείς
    },
    'yu=xos': {
        'frosts, cold weather': 'plural',  # pl. ψύχεα, Lat. frigora
    },
    'za/w': {
        'alive': 'participle',  # ζῶν κατακαυθῆναι, to be burnt alive
    },
    'zhmio/w': {
        'wilt lose': 'passive',  # II Pass., τὴν ψυχὴν ζημιώσεαι
    },
}
# END COVERAGE


# The forms a FORM_ONLY sense belongs to, by the parse code (person, tense, voice, mood, case,
# number, gender, degree) and the part of speech.
FORMS = {
    "plural": lambda c, p: c[5] == "P", "singular": lambda c, p: c[5] in "S-",
    "dual": lambda c, p: c[5] == "D",
    "active": lambda c, p: c[2] == "A", "middle": lambda c, p: c[2] in "ME", "passive": lambda c, p: c[2] in "PE",
    "middle or passive": lambda c, p: c[2] in "MPE", "not active": lambda c, p: c[2] in "MPE",
    "not passive": lambda c, p: c[2] in "AM", "not middle": lambda c, p: c[2] in "AP",
    "participle": lambda c, p: c[3] == "P", "not participle": lambda c, p: c[3] != "P",
    "infinitive": lambda c, p: c[3] == "N", "imperative": lambda c, p: c[3] == "D",
    "present": lambda c, p: c[1] in "PI", "imperfect": lambda c, p: c[1] == "I", "future": lambda c, p: c[1] == "F",
    "aorist": lambda c, p: c[1] == "A", "perfect": lambda c, p: c[1] in "XY", "pluperfect": lambda c, p: c[1] == "Y",
    "not perfect": lambda c, p: c[1] not in "XY", "perfect or passive": lambda c, p: c[1] in "XY" or c[2] in "PE",
    "nominative": lambda c, p: c[4] == "N", "genitive": lambda c, p: c[4] == "G", "dative": lambda c, p: c[4] == "D",
    "accusative": lambda c, p: c[4] == "A", "vocative": lambda c, p: c[4] == "V",
    "masculine": lambda c, p: c[6] in "MC", "feminine": lambda c, p: c[6] in "FC", "neuter": lambda c, p: c[6] == "N",
    "not neuter": lambda c, p: c[6] != "N",
    "comparative": lambda c, p: c[7] == "C", "superlative": lambda c, p: c[7] == "S",
    "positive": lambda c, p: c[7] == "-",
    "neuter plural": lambda c, p: c[6] == "N" and c[5] == "P",
    "noun": lambda c, p: p.startswith("noun"), "adjective": lambda c, p: p.startswith("adjective"),
    "adverb": lambda c, p: p.startswith("adverb"), "not adverb": lambda c, p: not p.startswith("adverb"),
    "conjunction": lambda c, p: p.startswith("conjunction"), "particle": lambda c, p: p.startswith("particle"),
    "preposition": lambda c, p: p.startswith("preposition"), "verb": lambda c, p: p.startswith("verb"),
    "first person": lambda c, p: c[0] == "1", "second person": lambda c, p: c[0] == "2",
    "middle only": lambda c, p: c[2] == "M",
    # Q33: the parse read more finely where a sense belongs to one form of a form — πᾶν, not πᾶς;
    # ὁ τεκών, not the passive participle; τὸ φέρον, not every neuter
    "neuter singular": lambda c, p: c[6] == "N" and c[5] in "S-",
    "active participle": lambda c, p: c[3] == "P" and c[2] == "A",
    "passive participle": lambda c, p: c[3] == "P" and c[2] in "PE",
    "middle participle": lambda c, p: c[3] == "P" and c[2] in "ME",
    "neuter participle": lambda c, p: c[3] == "P" and c[6] == "N",
    "perfect passive": lambda c, p: c[1] in "XY" and c[2] in "PE",
    "first person active": lambda c, p: c[0] == "1" and c[2] == "A",
    "never": lambda c, p: False,
}

# Senses whose English object is the passive's own subject (Q35). In the passive the object
# becomes the subject, so a passive form reads the sense without it, as English says the passive:
# δικαιόω's *to do a man right or justice, to judge* is, of the man, *to be done right or justice,
# to be judged*. A gloss whose object stays an object — κόπτω's *to cut down the trees in it* — is
# said in English's own passive in the chain itself, `having had the trees in it cut down` (Q21).
PASSIVE_OF = {
    "dikaio/w": {"to do a man right or justice, to judge": "to be done right or justice, to be judged"},
    "diako/ptw": {"to break through the line": "to be broken through"},
    "kate/xw": {"to bring a ship to land, bring it in or to": "to be brought to land, brought in or to"},
    "poti/zw": {"to water cattle": "to be watered"},
    "xala/w": {"to loosen or undo things drawn tightly together": "to be loosened or undone"},
    "a)nasw/zw": {"to recover what is lost, rescue": "to be recovered, rescued"},
    "te/mnw": {"plough the sea": "be ploughed"},
    "katapau/w": {"to make one stop from": "to be made to stop from"},
}

# Senses the entry gives only some forms of a word: {key: {sense: form}}, form a FORMS name — a
# sense "in pl.", "Pass.", "part.", of the comparative, of the vocative. A form outside it leaves
# the sense out, as FORM_SENSES would; this says it one sense at a time.
FORM_ONLY = {
    # ἐνδύω: "ἐνδύω and -δύνω with Mid. … «to go into», of clothes, «to put on»"; "Causal in pres., fut.,
    # aor1 … «to clothe in», «to clothe»". The corpus's active forms are the causal tenses.
    "e)ndu/w": {"to go into": "middle", "to put on": "middle", "to wear": "middle", "to put on, assume": "middle",
               "to enter, to press into": "middle", "to enter": "middle", "to clothe in": "active",
               "to clothe": "active"},
    # ἵνα: "Adverb, of Place … «in that place, there»", then "Final Conjunction … «that, in order that»"
    "i(/na": {"in that place, there": "adverb", "in which place, where": "adverb", "in whatever part": "adverb",
              "in what": "adverb", "whither": "adverb", "when, at which": "adverb",
              "that, in order that": "conjunction", "that he might": "conjunction",
              "in which case he must be": "conjunction", "that not": "conjunction"},
}


def form_senses(senses, bare, lemma, code="", form="", parse=""):
    """The senses of an entry a form reads, NOT_SENSES and FORM_SENSES applied."""
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
    # the coverage pass's verdicts (Q24): translations that are not senses, and senses of some forms only
    skip = set(skip) | set(COVERAGE_NOT.get(bare, ())) | set(COVERAGE_NOT.get(beta(lemma), ()))
    only = dict(COVERAGE_ONLY.get(bare, {}))
    only.update(FORM_ONLY.get(bare, {}))
    if only:
        skip |= {sense for sense, where in only.items() if not FORMS[where](code, parse)}
    seen, out = set(), []
    restored = {g for k in (bare, bare + "1", bare + "2") for _, g in MARKUP_LOST.get(k, ())}
    passive = PASSIVE_OF.get(bare, {}) if code[2] in "PE" else {}
    for sense in senses:
        if sense in passive and sense not in skip:
            sense = passive[sense]
        # two translations joined by "or" are set aside together or not at all: one of them
        # set aside alone is a piece of the translation dropped (Q2). Pieces set aside because
        # MARKUP_LOST restores the whole are not the whole set aside.
        if sense in skip or (" or " in sense and sense not in restored
                             and all(p in skip for p in sense.split(" or "))):
            continue
        if sense not in seen:
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
    # Verses SBLGNT prints and MorphGNT does not analyse — John 7:53–8:11, which SBLGNT gives in
    # double brackets — take the project's own morphology, written as an LXX chapter's is, in
    # data/<book>/<chapter>.morph.txt. It holds those verses only; MorphGNT's stand for the rest.
    own = read_morph(book, chapter)
    for verse, words in (own or {}).items():
        if verse not in out:
            out[verse] = [(form, lemma, code, morphgnt(pos, code)) for form, lemma, pos, code, _ in words]
    return out


# --------------------------------------------------------------------------

def nfc(s):
    return unicodedata.normalize("NFC", s)


# Elision is written four ways: SBLGNT's ʼ (U+02BC), MorphGNT's ’ (U+2019), the koronis-like ᾿ and ᾽.
ELIDED = dict.fromkeys(map(ord, "’᾿᾽ʼ'"), "ʼ")


def same(a, b):
    """The source's form against ours; the verse-initial capital is ours to print."""
    a, b = nfc(a).translate(ELIDED), nfc(b).translate(ELIDED)
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
            senses, lexicon = lexicon_senses(entries, lemma, code, form, parse), "Middle Liddell"
            if lemma in LSJ_HOMOGRAPHS:
                senses, lexicon = lsj_senses(lemma, code, form), "LSJ"
            if not senses and (lemma in names or form in names or lemma in by_lemma):
                # A name entry is keyed by the form the verse prints (Ἀσσυρίων), which
                # is not always the dictionary form the morphology gives (Ἀσσύριος). It
                # also stands in for an entry that tags nothing: Middle Liddell's γάζα,
                # "treasure", is another word, and glosses nothing for Γάζα at GEN 10:19.
                own = next((bearers.get((n["greek"], n["anchored"])) for n in verse.get("names", [])
                            if n["greek"] == form), None)
                senses, lexicon = [own or names.get(lemma) or names.get(form) or by_lemma[lemma]], "name"
            elif senses is None and lemma in LSJ:
                senses, lexicon = lsj_senses(lemma, code, form), "LSJ"
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
