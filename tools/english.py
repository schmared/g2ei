# -*- coding: utf-8 -*-
"""English inflection for the rebuild: verb forms and noun plurals, British spelling as Middle Liddell has it."""
import re

IRREGULAR = {
    # base: (past, past participle)
    "arise": ("arose", "arisen"), "awake": ("awoke", "awoken"), "be": ("was", "been"), "bear": ("bore", "borne"),
    "beat": ("beat", "beaten"), "become": ("became", "become"), "befall": ("befell", "befallen"),
    "beget": ("begot", "begotten"), "begin": ("began", "begun"), "behold": ("beheld", "beheld"),
    "bend": ("bent", "bent"), "bereave": ("bereaved", "bereft"), "beseech": ("besought", "besought"),
    "bet": ("bet", "bet"), "bid": ("bade", "bidden"), "bind": ("bound", "bound"), "bite": ("bit", "bitten"),
    "bleed": ("bled", "bled"), "blow": ("blew", "blown"), "break": ("broke", "broken"), "breed": ("bred", "bred"),
    "bring": ("brought", "brought"), "build": ("built", "built"), "burn": ("burned", "burned"),
    "burst": ("burst", "burst"), "buy": ("bought", "bought"), "cast": ("cast", "cast"),
    "catch": ("caught", "caught"), "chide": ("chid", "chidden"), "choose": ("chose", "chosen"),
    "cleave": ("clove", "cloven"), "cling": ("clung", "clung"), "come": ("came", "come"), "cost": ("cost", "cost"),
    "creep": ("crept", "crept"), "cut": ("cut", "cut"), "deal": ("dealt", "dealt"), "dig": ("dug", "dug"),
    "do": ("did", "done"), "draw": ("drew", "drawn"), "dream": ("dreamt", "dreamt"), "drink": ("drank", "drunk"),
    "drive": ("drove", "driven"), "dwell": ("dwelt", "dwelt"), "eat": ("ate", "eaten"), "fall": ("fell", "fallen"),
    "feed": ("fed", "fed"), "feel": ("felt", "felt"), "fight": ("fought", "fought"), "find": ("found", "found"),
    "flee": ("fled", "fled"), "fling": ("flung", "flung"), "fly": ("flew", "flown"), "forbear": ("forbore", "forborne"),
    "forbid": ("forbade", "forbidden"), "forget": ("forgot", "forgotten"), "forgive": ("forgave", "forgiven"),
    "forsake": ("forsook", "forsaken"), "freeze": ("froze", "frozen"), "get": ("got", "got"), "give": ("gave", "given"),
    "go": ("went", "gone"), "grind": ("ground", "ground"), "grow": ("grew", "grown"), "hang": ("hung", "hung"),
    "have": ("had", "had"), "hear": ("heard", "heard"), "heave": ("heaved", "heaved"), "hew": ("hewed", "hewn"),
    "hide": ("hid", "hidden"), "hit": ("hit", "hit"), "hold": ("held", "held"), "hurt": ("hurt", "hurt"),
    "keep": ("kept", "kept"), "kneel": ("knelt", "knelt"), "know": ("knew", "known"), "lade": ("laded", "laden"),
    "lay": ("laid", "laid"), "lead": ("led", "led"), "lean": ("leant", "leant"), "leap": ("leapt", "leapt"),
    "learn": ("learned", "learned"), "leave": ("left", "left"), "lend": ("lent", "lent"), "let": ("let", "let"),
    "lie": ("lay", "lain"), "light": ("lit", "lit"), "lose": ("lost", "lost"), "make": ("made", "made"),
    "mean": ("meant", "meant"), "meet": ("met", "met"), "mow": ("mowed", "mown"), "pay": ("paid", "paid"),
    "put": ("put", "put"), "quit": ("quitted", "quitted"), "read": ("read", "read"), "rend": ("rent", "rent"),
    "rid": ("rid", "rid"), "ride": ("rode", "ridden"), "ring": ("rang", "rung"), "rise": ("rose", "risen"),
    "run": ("ran", "run"), "say": ("said", "said"), "see": ("saw", "seen"), "seek": ("sought", "sought"),
    "sell": ("sold", "sold"), "send": ("sent", "sent"), "set": ("set", "set"), "sew": ("sewed", "sewn"),
    "shake": ("shook", "shaken"), "shear": ("sheared", "shorn"), "shed": ("shed", "shed"), "shine": ("shone", "shone"),
    "shoot": ("shot", "shot"), "show": ("showed", "shown"), "shew": ("shewed", "shewn"), "shrink": ("shrank", "shrunk"),
    "shut": ("shut", "shut"), "sing": ("sang", "sung"), "sink": ("sank", "sunk"), "sit": ("sat", "sat"),
    "slay": ("slew", "slain"), "sleep": ("slept", "slept"), "slide": ("slid", "slid"), "sling": ("slung", "slung"),
    "slit": ("slit", "slit"), "smell": ("smelt", "smelt"), "smite": ("smote", "smitten"), "sow": ("sowed", "sown"),
    "speak": ("spoke", "spoken"), "speed": ("sped", "sped"), "spell": ("spelt", "spelt"), "spend": ("spent", "spent"),
    "spill": ("spilt", "spilt"), "spin": ("spun", "spun"), "spit": ("spat", "spat"), "split": ("split", "split"),
    "spoil": ("spoilt", "spoilt"), "spread": ("spread", "spread"), "spring": ("sprang", "sprung"),
    "stand": ("stood", "stood"), "steal": ("stole", "stolen"), "stick": ("stuck", "stuck"), "sting": ("stung", "stung"),
    "stink": ("stank", "stunk"), "strew": ("strewed", "strewn"), "stride": ("strode", "stridden"),
    "strike": ("struck", "struck"), "string": ("strung", "strung"), "strive": ("strove", "striven"),
    "swear": ("swore", "sworn"), "sweep": ("swept", "swept"), "swell": ("swelled", "swollen"), "swim": ("swam", "swum"),
    "swing": ("swung", "swung"), "take": ("took", "taken"), "teach": ("taught", "taught"), "tear": ("tore", "torn"),
    "tell": ("told", "told"), "think": ("thought", "thought"), "thrive": ("throve", "thriven"),
    "throw": ("threw", "thrown"), "thrust": ("thrust", "thrust"), "tread": ("trod", "trodden"),
    "wake": ("woke", "woken"), "wear": ("wore", "worn"), "weave": ("wove", "woven"), "weep": ("wept", "wept"),
    "wet": ("wet", "wet"), "win": ("won", "won"), "wind": ("wound", "wound"), "wring": ("wrung", "wrung"),
    "write": ("wrote", "written"), "abide": ("abode", "abode"), "gird": ("girded", "girded"), "seethe": ("seethed", "seethed"),
    "shoe": ("shod", "shod"), "bless": ("blessed", "blessed"), "can": ("could", "could"), "will": ("willed", "willed"),
}
PREFIXES = ("over", "under", "out", "fore", "with", "up", "mis", "re", "un", "be", "for")
DOUBLE = {"admit", "commit", "permit", "omit", "submit", "transmit", "remit", "emit", "refer", "prefer", "defer",
          "infer", "confer", "occur", "recur", "incur", "compel", "expel", "propel", "repel", "rebel", "regret",
          "control", "patrol", "equip", "acquit", "begin", "forget", "abhor", "deter", "inter", "aver", "allot",
          "befit", "outwit", "upset", "beset", "unpin", "outstrip", "outrun", "embed"}


def _split(v):
    if v in IRREGULAR:
        return "", v
    for p in PREFIXES:
        if v.startswith(p) and v[len(p):] in IRREGULAR and len(v) > len(p) + 1:
            return p, v[len(p):]
    return None, v


def _cvc(v):
    one_syllable = len(re.findall(r"[aeiouy]+", v)) == 1
    return (one_syllable and re.search(r"[^aeiou][aeiou][bdfgklmnprstvz]$", v) is not None) or v in DOUBLE


def past(v):
    p, root = _split(v)
    if p is not None:
        return p + IRREGULAR[root][0]
    return _ed(v)


def pp(v):
    p, root = _split(v)
    if p is not None:
        return p + IRREGULAR[root][1]
    return _ed(v)


def _ed(v):
    if v.endswith("e"):
        return v + "d"
    if re.search(r"[^aeiou]y$", v):
        return v[:-1] + "ied"
    if re.search(r"[^aeiou][aeiou]l$", v):
        return v + "led"                      # British: travelled, quarrelled
    if _cvc(v):
        return v + v[-1] + "ed"
    if v.endswith("c"):
        return v + "ked"
    return v + "ed"


def ing(v):
    if v == "be":
        return "being"
    if v.endswith("ie"):
        return v[:-2] + "ying"
    if v.endswith("e") and not v.endswith(("ee", "ye", "oe")) and v not in ("singe", "dye"):
        return v[:-1] + "ing"
    if re.search(r"[^aeiou][aeiou]l$", v):
        return v + "ling"
    if _cvc(v):
        return v + v[-1] + "ing"
    if v.endswith("c"):
        return v + "king"
    return v + "ing"


def s3(v):
    if v == "be":
        return "is"
    if v == "have":
        return "has"
    if v in ("do", "go"):
        return v + "es"
    if v.endswith("do") or v.endswith("go"):
        return v + "es"
    if re.search(r"(s|x|z|ch|sh)$", v):
        return v + "es"
    if re.search(r"[^aeiou]y$", v):
        return v[:-1] + "ies"
    return v + "s"


IRREGULAR_PLURAL = {"man": "men", "woman": "women", "child": "children", "foot": "feet", "tooth": "teeth",
                    "goose": "geese", "mouse": "mice", "ox": "oxen", "louse": "lice", "die": "dice",
                    "leaf": "leaves", "life": "lives", "wife": "wives", "knife": "knives", "half": "halves",
                    "calf": "calves", "wolf": "wolves", "loaf": "loaves", "sheaf": "sheaves", "thief": "thieves",
                    "shelf": "shelves", "self": "selves", "staff": "staves", "hoof": "hoofs", "roof": "roofs",
                    "sheep": "sheep", "deer": "deer", "swine": "swine", "fish": "fish", "cattle": "cattle",
                    "kine": "kine", "people": "people", "folk": "folk", "offspring": "offspring", "series": "series",
                    "species": "species", "means": "means", "news": "news", "goods": "goods", "riches": "riches",
                    "wages": "wages", "entrails": "entrails", "bowels": "bowels", "clothes": "clothes",
                    "brethren": "brethren", "alms": "alms", "thanks": "thanks", "spoils": "spoils"}
UNCOUNTABLE_UNUSED = {"wheat", "barley", "gold", "silver", "brass", "bronze", "copper", "iron", "lead", "tin", "water",
               "wine", "oil", "milk", "honey", "flesh", "blood", "dust", "earth", "flax", "linen", "wool", "hair",
               "fire", "smoke", "light", "darkness", "evening", "night", "grass", "fodder", "meat", "bread",
               "flour", "salt", "stone", "wood", "timber", "incense", "frankincense", "myrrh", "spice", "purple",
               "scarlet", "fat", "dung", "mud", "clay", "pitch", "asphalt", "brimstone", "rain", "snow", "hail",
               "frost", "dew", "money", "wealth", "property", "substance", "glory", "honour", "shame", "anger",
               "wrath", "strength", "might", "power", "justice", "righteousness", "mercy", "pity", "peace",
               "safety", "health", "life", "death", "food", "drink", "sustenance", "pasture", "seed", "fruit",
               "produce", "corn", "straw", "stubble", "chaff", "leaven"}


AFTER_HEAD = {"of", "for", "with", "in", "on", "at", "from", "by", "to", "worn", "made", "used", "given", "which",
              "that", "who", "whose", "where", "under", "over", "upon", "into", "like", "against", "round", "about",
              "set", "borne", "put", "laid", "cut", "taken", "shaped", "wrought", "carried", "built", "sent", "or",
              "together", "out", "up", "down", "back", "forth", "away", "off", "apart", "asunder", "abroad"}


AGREE = {"is": "are", "was": "were", "has": "have", "goes": "go", "does": "do"}
PARTICIPLE = re.compile(r"^(?:\w+ed|seen|done|made|borne|born|given|taken|known|shown|sown|grown|thrown|drawn|"
                        r"worn|torn|sworn|written|spoken|broken|chosen|frozen|stolen|hidden|eaten|beaten|fallen|"
                        r"bound|found|ground|wound|held|kept|left|lost|sent|spent|built|bent|cut|put|set|laid|paid|"
                        r"said|sold|told|brought|bought|caught|taught|thought|sought|fought|struck|hung|spun)$")


def singular(noun):
    """The singular of a noun phrase a lexicon gives in the plural, for a singular form (Q27)."""
    words = noun.split(" ")
    at = len(words) - 1
    for i, w in enumerate(words[1:], 1):
        if w in AFTER_HEAD or PARTICIPLE.match(w):
            at = i - 1
            break
    w = words[at]
    back = {v: k for k, v in IRREGULAR_PLURAL.items() if k != v}
    if w in back:
        words[at] = back[w]
    elif w.endswith("ies") and len(w) > 4:
        words[at] = w[:-3] + "y"
    elif re.search(r"(?:ss|x|z|ch|sh)es$", w):
        words[at] = w[:-2]
    elif w.endswith("s") and not w.endswith(("ss", "us", "is")) and len(w) > 3:
        words[at] = w[:-1]
    return " ".join(words)


def comparative(adj, degree):
    """big -> bigger, great -> greater, youthful -> more youthful; most/-est for the superlative."""
    w = adj
    more, er = ("more", "er") if degree == "C" else ("most", "est")
    irregular = {"good": ("better", "best"), "well": ("better", "best"), "bad": ("worse", "worst"),
                 "ill": ("worse", "worst"), "little": ("less", "least"), "much": ("more", "most"),
                 "many": ("more", "most"), "far": ("farther", "farthest"), "old": ("elder", "eldest")}
    if w in irregular:
        return irregular[w][0 if degree == "C" else 1]
    if " " in w or "-" in w or len(re.findall(r"[aeiouy]+", w)) > 2 or w.endswith(("ful", "ous", "ive", "ing", "ed", "ic", "al", "less", "ish")):
        return "%s %s" % (more, w)
    if len(re.findall(r"[aeiouy]+", w)) == 2 and not w.endswith(("y", "le", "er", "ow")):
        return "%s %s" % (more, w)
    if w.endswith("e"):
        return w + er[1:]
    if re.search(r"[^aeiou]y$", w):
        return w[:-1] + "i" + er
    if len(re.findall(r"[aeiouy]+", w)) == 1 and re.search(r"[^aeiou][aeiou][bdgmnpt]$", w):
        return w + w[-1] + er
    return w + er


def plural(noun):
    """The plural of an English noun phrase: the head noun is the last word, or the word before `of`."""
    words = noun.split(" ")
    # a clause, `that by which the thought is expressed`, and a participle or adjective standing alone,
    # `spoken`, have no plural of their own
    if noun.startswith("that which is "):
        return "things which are " + noun[len("that which is "):]
    if noun.startswith("that which "):
        return "things which " + noun[len("that which "):]
    if words[0] in ("that", "which", "what", "whatever", "who", "whoever", "those", "these", "such"):
        return noun
    if len(words) == 1 and re.search(r"(?:en|ed|ful|ous|less|ish|able|ible)$", words[0]) and words[0] not in ("garden", "linen", "oven", "token", "burden", "maiden", "heaven", "haven", "seed", "bed", "creed", "need", "deed", "reed", "weed", "steed", "sled", "shed"):
        return noun
    m = re.match(r"^(anything|something|any one|anyone|one) (that|which|who) (\w+)\b(.*)$", noun)
    if m:
        v = m.group(3)
        verb = AGREE.get(v) or (v[:-2] if re.search(r"(?:ss|x|z|ch|sh)es$", v) else
                                v[:-3] + "y" if v.endswith("ies") else
                                v[:-1] if v.endswith("s") and not v.endswith("ss") else v)
        return "%s %s %s%s" % ("things" if m.group(1) in ("anything", "something") else "ones",
                               m.group(2), verb, m.group(4))
    m = re.match(r"^(?:anything|something) (.*)$", noun)
    if m:
        return "things " + m.group(1)
    m = re.match(r"^(?:any one|anyone|one) (\w+ed|\w+en|\w+n)\b(.*)$", noun)
    if m:
        return "ones %s%s" % (m.group(1), m.group(2))
    if noun in ("this", "that"):
        return {"this": "these", "that": "those"}[noun]
    if noun.startswith("that which is "):
        return "things " + noun[len("that which is "):]
    if noun.startswith("that which "):
        return "things which " + noun[len("that which "):]
    at = len(words) - 1
    for i, w in enumerate(words[1:], 1):
        if (w in AFTER_HEAD or PARTICIPLE.match(w)) and i > 0:
            at = i - 1
            break
    w = words[at]
    low = w.lower()
    if low in IRREGULAR_PLURAL.values() and low not in IRREGULAR_PLURAL:
        new = w                                      # already plural: children, men
    elif low in IRREGULAR_PLURAL:
        new = IRREGULAR_PLURAL[low]
    elif "-" in w and w.rsplit("-", 1)[1] in IRREGULAR_PLURAL:
        a, b = w.rsplit("-", 1)
        new = a + "-" + IRREGULAR_PLURAL[b]
    elif low.endswith("man") and len(low) > 4:
        new = w[:-3] + "men"
    elif not re.search(r"[a-z]$", low):
        new = w
    elif re.search(r"(s|x|z|ch|sh)$", low):
        new = w if low.endswith(("ss", "ics", "ness")) and False else (w if low.endswith("s") and not low.endswith("ss") else w + "es")
    elif re.search(r"[^aeiou]y$", low):
        new = w[:-1] + "ies"
    elif re.search(r"[^aeiou]o$", low) and low not in ("piano", "photo"):
        new = w + "es"
    else:
        new = w + "s"
    words[at] = new
    return " ".join(words)
