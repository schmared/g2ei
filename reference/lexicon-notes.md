# Lexicon notes — headwords and gloss-chains

Seeded from GEN 1:1–2, JHN 1:1–2 and JHN 1:6.

**These strings are copied verbatim into new chapters.** ἀρχή must read the same way in
Gen 1:1 and John 1:1 — that consistency is what makes the quotation visible on the page.
If a chain or headword has to change, change it here first and re-render every chapter that
uses it.

## How an entry is used

Each entry gives a **headword** and a **chain**. In a verse's `reading` they are one unit:

    [[headword|chain|lemma]]

The unanchored panel shows the chain alone; the anchored panel shows `headword — chain —`,
shaded. There is one chain per entry, not one per panel.

### The headword rule

The headword is **the lexicon's first sense, in the form the text uses**. No translation is
consulted.

1. **Lexicon.** Middle Liddell (1889), as the Perseus Digital Library encodes it, in
   `sources/middle-liddell/`. Where it has no entry, LSJ as published by PerseusDL
   (CC BY-SA 4.0).
2. **Sense.** The first translation in the entry's first numbered sense. The headword line,
   principal parts and etymology stand before the senses and are never taken. For a
   preposition, the first sense for the case it governs. For a word used as a noun, the
   first noun sense.

   Where Perseus's opening gloss belongs to one voice only — ἄρχω's *in pass. sense:— to be
   first*, against its numbered I, *to begin, make a beginning* ("both in Act. and Mid.") —
   it is skipped **by name** in `NOT_SENSES`. Not by rule: the same opening position carries
   the principal sense in most entries, λόγος's *the word* among them, and a rule that
   skipped it would rewrite the prologue's headword to *spoken*.

   The same holds for a sense restricted to a *form* rather than a voice. ἐνδύω's sense I,
   *to go into, put on*, is dressing oneself; the entry marks sense II "Causal … aor1
   -έδυσα", and GEN 3:21 ἐνέδυσεν is that aorist, so sense I is skipped by name. And one
   entry can hold two words: ὡς's opens with the accented demonstrative ὥς, *so, thus*,
   before the relative ὡς, *as*, which is the word Rahlfs prints.

   A word used as a conjunction takes the first conjunction sense, as a word used as a noun
   takes the first noun sense: ἵνα is an adverb of place in its first sense and *that, in
   order that* in its second; μήποτε is *never* as an adverb and *that at no time, lest
   ever* as a conjunction.

   A sense the entry restricts to one *tense* is skipped the same way: ἀνίστημι heads its
   causal senses "in pres., imperf." and its intransitive ones "in aor2 ἀνέστην", so GEN 4:8
   ἀνέστη is *stood up* and GEN 9:9 ἀνίστημι *I make to stand up*. Where one lemma is used both
   ways, the word-by-word layer cannot skip by lemma alone: `FORM_SENSES` in `build/words.py`
   names the senses to skip for a given tense and voice, in place of `NOT_SENSES`. ἐπιτίθημι's
   middle, *B. Mid. to put on oneself*, is filed there the same way for GEN 9:23 ἐπέθεντο, and
   παύω's, *to take one's rest*, for GEN 11:8 ἐπαύσαντο. A sense restricted only by *subject* or *construction* is not: the
   rule reads the lexicon, not the verse. So συλλαμβάνω is *having collected* at GEN 4:1,
   though its fourth sense, "of females, to conceive", is what the verse means; ἄρχω with the
   genitive is *will begin* at 4:7, though *to rule* is its second sense; and πρόβατον is
   *anything that walks forward*, which Middle Liddell gives as the word's proper sense before
   *cattle, flocks* and, in Attic, *sheep*. The chain carries the rest, and the notes say
   where the verse's meaning stands in the entry.

   A passive or middle form takes the first sense in its own voice: κρύπτω, *to hide*, is *were
   hidden* at GEN 3:8, and φθείρω, *to ruin*, *was ruined* at 6:11. Where the entry also gives the
   passive a translation of its own — κρύπτω's *to hide oneself, lie hidden*, φθείρω's *to go to
   ruin*, πληθύνω's *to prevail* — that translation is the lexicon adding a reading, and it goes
   in the chain, not the headword. GEN 6 and 7 first took it for the headword (*went to ruin*,
   *to become firm*, *were open*); they were put back when GEN 8 found the two rules side by side.
   A verb filed under its middle (ἐκπορεύομαι, πορεύομαι, φοβέομαι) is different: its active
   glosses belong to another word's use and are skipped by name, as above.
3. **Form.** Tense, voice, mood, person and number come from the Greek form.
4. **Article.** English gets *the* where the Greek has the article, and nothing where it
   does not. The *a* in a lexicon's gloss (*a beginning*) is its citation form, not the text's.
5. **Capitals.** None the Greek does not mark. Proper names and *God* are capitalised, as
   the lexicon prints them; nothing is capitalised to make it a title, and no pronoun
   standing for God takes a reverential capital.

### Homographs

Where the lexicon prints two entries under one spelling, the first is not always the word
the text uses, and "the first sense of the first entry" would then be the first sense of the
wrong word. `ENTRY` in `build/words.py` names which entry is meant; it decides nothing about
what the word means, only which entry is the word, and every case is listed here:

| lemma | entry taken | why not the first |
| --- | --- | --- |
| χοῦς (GEN 2:7) | `xou=s2` — *earth thrown down, heaped up, dust* | `xou=s1` is the Pitcher-feast, the liquid measure |
| ὅτι (GEN 2:3) | `o(/ti2` — *that* | `o(/ti1` is ὅ τι, *for what, wherefore* |
| λέγω (GEN 2:16) | `le/gw3` — *to say, speak* | `le/gw1` is *to lull to sleep*, `le/gw2` *to gather* |
| οὐ (GEN 2:5) | `ou)8` — *not* | the other seventeen gloss idioms, οὐ γάρ, οὐ μήν … |
| ὁδός (GEN 3:24) | `o(do/s2` — *a way, path* | `o(do/s1` is the Attic ὀδός for οὐδός, *a threshold* |
| στεῖρα (GEN 11:30) | `stei=ra2` — *a cow that has not calved*; *barren* | `stei=ra1` is *a ship's keel* |
| μόσχος (GEN 12:16) | `mo/sxos2` — *a calf* | `mo/sxos1` is *a young shoot* |
| εὐθύς (GEN 15:4) | `eu)qu/s2` — the adverb, *straightway* | `eu)qu/s1` is the adjective, *straight, direct* |
| μῆλον (GEN 30:14) | `mh=lon2` — *tree-fruit* | `mh=lon1` is *a sheep or goat* |
<!-- homograph rows above -->

A lemma belongs there only where the entries are genuinely different words. A word with one
entry and several senses is not a homograph: its first numbered sense stands, however far
from the expected meaning it reads.

### Where the lexicon files a word elsewhere

`SPELLING` in `build/words.py` redirects a lemma to the key its entry actually sits under.
Three reasons, and all of them are the lexicon's filing rather than a decision about sense:

| lemma | filed under | why |
| --- | --- | --- |
| γίνομαι, γινώσκω | γίγνομαι, γιγνώσκω | the Attic spelling of a Koine form |
| εἷς (GEN 2:11) | `ei(/s` | Perseus keys the numeral with an acute, not a circumflex |
| πορεύομαι (GEN 2:14) | πορεύω | a deponent, filed under its active |
| ἐκπορεύομαι (GEN 2:10) | ἐκπορεύω | likewise |
| κατέναντι (GEN 2:14) | κατεναντίον | the entry is a bare cross-reference, `= κατεναντίον`, and glosses nothing itself |
| φοβέομαι (GEN 3:10) | φοβέω | MorphGNT's middle, filed under the active |
| ἔχθρα (GEN 3:15) | ἔχθρη | the entry is headed with the Ionic spelling |
| δειλινός (GEN 3:8) | δειελινός | a cross-reference, *contr. for δειελινός* |
| ὀρθῶς (GEN 4:7) | ὀρθός | the adverb, filed inside the adjective's entry |
| ἐννακόσιοι (GEN 5:5) | ἐνακόσιοι | the later spelling; the entry is headed with the earlier |
| ἐκλέγομαι, εἰσπορεύομαι, θυμόομαι (GEN 6) | ἐκλέγω, εἰσπορεύω, θυμόω | MorphGNT's middles, filed under the active |
| ἐπιμελῶς (GEN 6:5) | ἐπιμελής | the adverb, filed inside the adjective's entry |
| ἐναντίον (GEN 6:8) | ἐναντίος | the entry is a bare cross-reference, *adverb v. ἐναντίος* |
| νοσσιά (GEN 6:14) | νεοσσιά | the contracted spelling; the entry is headed with the full one |
| κατάγαιος (GEN 6:16) | κατάγειος | a cross-reference, *ionic for κατάγειος* |
| μήν, the month (GEN 7:11) | μείς | Middle Liddell's μήν is the particle, *verily*; the month is filed under its nominative μείς |
| ἀνοίγω (GEN 7:11) | ἀνοίγνυμι | the -νυμι form heads the entry |
| σφοδρῶς (GEN 7:19) | σφοδρός | the adverb, filed inside the adjective's entry |
| μιμνήσκομαι (GEN 8:1) | μιμνήσκω | MorphGNT's middle, filed under the active |
| διατίθεμαι (GEN 9:17) | διατίθημι | likewise |
| κυνηγός (GEN 10:9) | κυναγός | the entry is headed with the Doric and Attic spelling |
| πλησίον, ἐνώπιον (GEN 11:3, 11:28) | πλησίος, ἐνώπιος | the adverb, filed inside the adjective's entry |
| καθάπερ (GEN 12:4) | καθά | filed inside the entry for καθά |
| ἔρημος (GEN 12:9) | ἐρῆμος | the entry is headed with the Attic accent |
| περιποιέομαι (GEN 12:12) | περιποιέω | MorphGNT's middle, filed under the active |
| ἐνευλογέω (GEN 12:3) | ἐνευλογέομαι | the entry is headed with the passive |
| βορρᾶς (GEN 13:14) | Βορέας | the contracted Attic form, filed under the uncontracted |
| τερέμινθος (GEN 14:6) | τέρμινθος | the spelling Rahlfs prints; the entry is headed τέρμινθος |
| παραγίνομαι (GEN 14:13) | παραγίγνομαι | the Attic spelling |
| δεκάτη (GEN 14:20) | δέκατος | cross-reference; "v. δέκατος II." glosses nothing |
| ἐπειδή (GEN 15:3) | ἐπεί | not in Middle Liddell; LSJ's entry reads "v. ἐπεί" |
| κλίβανος (GEN 15:17) | κρίβανος | the entry is headed with the Attic κρίβανος |
| κυρία (GEN 16:4) | κύριος (the second entry) | cross-reference; "fem. of κύριος signf. B. 1. 2." |
| ἐξολεθρεύω (GEN 17:14) | ἐξολοθρεύω | the spelling the text prints, as MorphGNT files ἐξολεθρευθήσεται (Acts 3:23) |
| ἀρσενικός (GEN 17:10) | ἀρρενικός | LSJ: "less Att. form ἀρσενικός" |
| ἄρα (GEN 18:3) | `a(/ra` | Perseus keys the entry with a rough breathing |
| ἆρα (GEN 18:13) | ἄρα | "in accent and sense a stronger form of ἄρα"; the entry glosses nothing |
| ἀληθῶς (GEN 18:13) | ἀληθής | the adverb, filed inside the adjective's entry |
| οὐχί (GEN 18:15) | οὐ | the strengthened form, filed in its entry |
| μηδαμῶς (GEN 18:25) | μηδαμῇ | cross-reference; "adverb of μηδαμός = μηδαμῇ" |
| εἵνεκα (GEN 18:5) | ἕνεκα | the Ionic and poetic form |
| νίπτω (GEN 18:4) | νίζω | the late present, filed under νίζω |
| ἀποκρίνομαι (GEN 18:9) | ἀποκρίνω | MorphGNT's middle, filed under the active |
| πρεσβύτερος (GEN 18:11) | πρέσβυς | the comparative, filed inside the positive's entry |
| ὀρθρίζω (GEN 19:2) | ὀρθρεύω | cross-reference; "= ὀρθρεύω" |
| πλατεῖα (GEN 19:2) | πλατύς | the feminine used as a noun, filed inside the adjective's entry |
| συγγίνομαι (GEN 19:5) | συγγίγνομαι | the Attic spelling |
| σῴζω, διασῴζω (GEN 19:17, 19:19) | σώζω, διασώζω | the entries are headed without the iota subscript |
| δέομαι (GEN 19:18) | δέω (the second entry) | the deponent, filed under δέω, to lack; the first δέω is to bind |
| πρωΐ (GEN 19:27) | πρωί | the entry is headed without the diaeresis |
| μᾶλλον (GEN 19:9) | μάλα | the comparative, filed inside the positive's entry |
| ἀτμίς (GEN 19:28) | ἀτμός | cross-reference; "= ἀτμός" |
| ἐχθές (GEN 19:34) | χθές | cross-reference; "v. χθές" |
| ἐπισκέπτομαι (GEN 21:1) | ἐπισκοπέω | "a pres., which furnishes its tenses to ἐπισκοπέω" |
| παλλακή (GEN 22:24) | παλλακίς | cross-reference; "= παλλακίς" |
| διπλοῦς (GEN 23:9) | διπλόος | the contracted form, filed under the uncontracted |
| κύκλῳ (GEN 23:17) | κύκλος | the adverbial dative, filed inside κύκλος |
| θέλω (GEN 24:8) | ἐθέλω | the later form, filed under ἐθέλω |
| χρυσοῦς (GEN 24:22) | χρύσεος | the contracted form, filed under the uncontracted |
| ἀργυροῦς (GEN 24:53) | ἀργύρεος | likewise |
| θέριστρον (GEN 24:65) | θερίστριον | "so θέριστρον", inside θερίστριον |
| ἐπιλαμβάνομαι (GEN 25:26) | ἐπιλαμβάνω | MorphGNT's middle, filed under the active |
| πρεσβύτης (GEN 25:8) | πρέσβυς | cross-reference; "= πρέσβυς I" |
| ἕψεμα (GEN 25:29) | ἕψημα | LSJ: "late form of ἕψημα" |
| καλῶς (GEN 26:29) | καλός | the adverb, filed inside the adjective's entry |
| ἐχθρία (GEN 26:21) | ἔχθρη | LSJ: "late form of ἔχθρα", whose entry is headed with the Ionic ἔχθρη |
| ταχύ (GEN 27:20) | ταχύς | the adverb, filed inside the adjective's entry |
| δικαίως (GEN 27:36) | δίκαιος | likewise |
| ἐπιγινώσκω (GEN 27:23) | ἐπιγιγνώσκω | the Attic spelling of a Koine form, as γινώσκω |
| ζυγός (GEN 27:40) | ζυγόν | the entry is headed with the neuter |
| κλίμαξ (GEN 28:12) | κλῖμαξ | Middle Liddell heads the entry with the circumflex |
| βορρᾶς (GEN 28:14) | βορρᾶς | the contracted form, which the entry carries beside βορέας |
| ἐξαίρω (GEN 29:1) | ἐξαείρω | the entry is headed with the Epic form |
| δωρεάν (GEN 29:15) | δωρεά | the adverb, filed inside the noun's entry |
| ἐξομολογέω (GEN 29:35) | ἐξομολογέομαι | the entry is headed with the deponent middle |
| οὐθείς (GEN 30:31) | οὐδείς | the later spelling |
| βαρέως (GEN 31:35) | βαρύς | the adverb, filed inside the adjective's entry |
| ἀφρόνως (GEN 31:28) | ἄφρων | the adverb, which the entry glosses *senselessly* |
| πρῶτος (GEN 32:18) | πρότερος | the superlative filed under the comparative, as at 8:5 |
| ἀσφαλῶς | ἀσφαλής | the adverb, filed inside the adjective's entry |
| σκληρῶς | σκληρός | the adverb, filed inside the adjective's entry |
<!-- spelling rows above -->

The dictionary form itself does not follow the lexicon's filing: it keeps the spelling the text
prints — γίνομαι, ἔχθρα, νοσσιά, δειλινός, κατέναντι, ἐννακόσιοι, κατάγαιος, τεσσαράκοντα — and
this table finds its entry. Only the form is the dictionary's: ὀστοῦν goes under ὀστέον. GEN 5
first filed ἐννακόσιοι under ἐνακόσιοι itself; the second pass of GEN 6 showed that at odds with
every filing before it. The brief's rule was then worded as *a word the New Testament uses takes
MorphGNT's spelling*, and GEN 7's second pass, applying it, filed τεσσαράκοντα under SBLGNT's
τεσσεράκοντα: MorphGNT had only ever agreed with the text's spelling, never decided it.

Where Middle Liddell has no entry a word can be found under, LSJ supplies the senses (`LSJ` in
`build/words.py`): σύ, φλόγινος (GEN 3); ποιμήν — Middle Liddell has only the Doric ποιμάν,
*doric for ποιμήν*, pointing at an entry it lacks — ψαλτήριον, μώλωψ and ἑβδομηκοντάκις
(GEN 4). One word is in neither: σφυροκόπος (GEN 4:22), for which LSJ has only the verb
σφυροκοπέω. With no lexicon sense to head it, it stands as plain text, *a hammer-beater*, and
the note says why.

GEN 5 adds εὐαρεστέω, which Middle Liddell lacks, and the active διαναπαύω: Middle Liddell has
only the middle, διαναπαύομαι, *to rest awhile*, and 5:29 διαναπαύσει ἡμᾶς is transitive. It
also adds two numerals whose Middle Liddell entries, like ὀστέον's, tag no translation at all —
*Lat. octo, eight*; *Lat. tres, tria, three* — so ὀκτώ and τρεῖς take LSJ's, which files τρεῖς
under its neuter, τρία.

The last is the same shape as ἁγιάζω in LSJ (`= ἁγίζω`): an entry that exists, carries no
translation, and names the entry that does. Following it is not interpretation — the lexicon
is saying where the word is defined.

GEN 6 adds ἀσφαλτόω and διώροφος from LSJ, each with one sense and each citing the verse.
GEN 9 adds ὀπισθοφανής, *seen from behind*, and its adverb ὀπισθοφανῶς, *backwards*, both citing
9:23. GEN 12 adds ἐγγίζω, ἐνισχύω, and ἐτασμός, which LSJ defines only by the entry before it,
ἔτασις, *trial, affliction*. GEN 14 adds ἁλυκός, *salt, brackish*; ἀποσκευή, whose *removal,
riddance* comes before *baggage*; σφαιρωτήρ, *thong, latchet*; and περάτης, which opens "= πορθμεύς",
so that πορθμεύς's LSJ senses, *ferryman*, *boatman, seaman*, *conveyer*, stand before its own
*wanderer, emigrant*, as ἁγίζω's stand for ἁγιάζω. GEN 15 adds ὑπερασπίζω, *cover with a shield*, from the upsilon file; τριετίζω, *to be three years old*; and διχοτόμημα, *half of a thing cut in two*. GEN 17 adds κατάσχεσις, *holding back, restraining, retention*, then *possession*, from the kappa file; and ἑκατονταέτης, *of a hundred years*, *years old*, citing 17:17. GEN 18 adds μοσχάριον, *little calf*, and, from the beta file, βούτυρον, *butter*, then *a plant*. GEN 19 adds προσοίγνυμι, *shut*; ἀορασία, *inability to see, blindness*; γελοιάζω, *jest*, from the gamma file; ἐπαύριον, *on the morrow*; and εἰσσπάομαι, *draw into oneself*. GEN 20 adds μήτρα, *womb*, whose Middle Liddell entry tags only Latin; δίδραχμον, *coin of two drachms*, under δίδραχμος; and κἀγώ, *crasis for καὶ ἐγώ*. GEN 21 adds ἀπογαλακτίζω, *wean from the mother's milk*; ἀρχιστράτηγος, *commander-in-chief*; and, from the omega file, ὦμος, *the shoulder with the upper arm*. GEN 23 adds παρεπίδημος, *sojourning in a strange place*, and μνημεῖον, *memorial, remembrance, record*, whose Middle Liddell entry tags its first sense only in Latin. GEN 24 adds ποτιστήριον, *drinking-trough for cattle*; ἐνώτιον, *ear-ring*; ἅβρα, *favourite slave*; and ἀποσάττω, *unsaddle, unpack*, *stop up, caulk*, *stuff with food*. GEN 25 adds three more: ὅλος, which Middle Liddell lacks altogether, *whole, entire, complete in all its parts*; δόμα, *gift*, then *payment*; and πυρράκης, *red, ruddy*, which LSJ files as a masculine noun. GEN 26 adds ἑκατοστεύω, *bear a hundredfold*, and γεώργιον, *field*, then *orchard*, *husbandry*, *crop* and, in the plural, a *tax* on land. GEN 27 adds four more: πιότης, *fattiness*, then *wealth, prosperity*; πτερνίζω, *strike with the heel*, *trip up, supplant*; προσοχθίζω, *to be wroth with*, and of this chapter's phrase *am weary* of; and κατανύσσω, *stab, gouge*, and in the passive *to be sorely pricked*. GEN 28 adds one more: ἐνυπνιάζομαι, *dream*, which Middle Liddell does not have at all. GEN 30 adds eight, the whole vocabulary of Jacob's flocks: ἀρήν, *lamb*; διάλευκος, *quite white*; ῥαντός, *sprinkled*, then *speckled or spotted*; σποδοειδής, *ashy, ash-coloured*; ἐγκισσάω, *have yearnings like one pregnant*; λεπίζω, *peel off the husk, skin or bark*; λέπισμα, *peel*; and καρύινος, *of nuts*, *made of walnut-wood*. LSJ cites this chapter for six of the eight. GEN 31 adds six: κρυφῇ, *secretly, in secret*, which Middle Liddell has only as the Doric κρύφα; κατάβρωσις, *eating up, devouring*; κλοποφορέω, *steal from, rob*; ἐθισμός, *accustoming, habituation*; θηριάλωτος, *caught by wild beasts*; and αἰχμαλωτίς, *captive*, which Middle Liddell has as an entry with no translation tagged in it. LSJ cites this chapter for four of the six. GEN 32 adds two: χείμαρρος, which LSJ heads χειμάρροος, *winter-flowing*, and as a noun *torrent*, *river*, *valley, watercourse*; and ἐπισκάζω, *limp upon*, cited from this chapter. GEN 33 adds πόρευσις, which LSJ defines only by cross-reference, "= πορεία", citing this verse. GEN 34 adds τραυματίας, which Middle Liddell lacks and LSJ (eng22) glosses "wounded man" and "corpse of one slain". GEN 35 adds θλῖψις, which Middle Liddell lacks and LSJ (eng9) glosses "pressure", "crushing, castration" and "oppression, affliction", citing this verse; and κατώτερος, which LSJ (eng11) heads as the comparative of κάτω.
<!-- LSJ sentences above -->

GEN 9 also files ἐμεθύσθη under μεθύσκω, *to make drunk*, where Middle Liddell gives its aorist
passive, though MorphGNT files the same form under μεθύω, *to be drunk*.

Where a deponent is filed under its active, the entry's opening gloss is usually the active
one and the form in the text is not. That is the ἄρχω and βρέχω situation again, and it is
settled the same way: by name, per lemma, with the entry's own voice labels quoted.

Each entry below records the lexicon sense its headword came from.

### The chain rules

- **A chain is the whole range.** Lexical range, plus aspect where the aspect belongs to the
  word itself. The headword may repeat inside it — it is the chain's first sense.
- **No filler and no commentary.** A point *about* the text — that John is quoting Genesis,
  that ἐγένετο is the verb withheld from the Logos — goes in the notes.
- **The headword never stands bare** in the unanchored panel, as plain text outside its unit.
- **No em dashes inside a chain.** Em dashes delimit chains in the anchored panel.
- **Words with no chain are plain text**, identical in both panels: ὕδωρ (*the water*), a
  supplied copula, ἦν's aspect expansion, ἐπάνω.
- **short** marks the reduced form used when a word is restated rather than introduced.
  John 1:2 restates John 1:1 and takes the short forms.
- **No reverential capitals.** A pronoun standing for God is lowercase — *he who is God
  definitively, the one the article marks out*, *facing him*. The manuscripts have no lower
  case, so the capital is always the editor's. *God* itself keeps its capital, as the lexicon
  prints it.

### How an entry's translations are read

Settled in the edit pass after Exodus (the open questions named after each).

- **A pointer is followed.** A whole entry that is a pointer — *= X*, *strengthd. for X* — reads
  X's entry: κατέναντι, ἁγίασμα, κατεμβλέπω (*strengthd. for ἐμβλέπω*, EXO 3:6), the entry's own
  translation kept after it (Q5). A pointer that is one sense of an entry, πάγος's *= παγετός*,
  reads X's translations in its place, by `SENSE_POINTERS` in `build/words.py` (Q14). LSJ's *Dim.
  of X* reads X's senses (κυμάτιον, καρυΐσκος), and the note says *Dim.*: the reading cannot say
  *little* without adding a word the entry does not print (Q20).
- **An example's translation:** a translation of the word, in that use, is kept (σύνταξις's
  *contingent*); a translation of the whole phrase, or a repeat of a sense above it, goes in
  `NOT_SENSES` (ψῆφος's *by vote*; φόνος's *murder and manslaughter*, where the adjectives carry the
  difference; καλάμη's *the residue*, which says what a metaphor means) (Q7). Where the phrase
  itself is in the text, its translations are the word's there: ἐρυθρός keeps *the Erythraean sea*
  and its extent at Ἐρυθρὴ θάλασσα (Q8).
- **An adverb its entry names and never glosses** reads its adjective's senses, made adverbs where
  English has the adverb and left as the entry's phrase where it has none: ἐνδόξως, `held in esteem
  and honour and of high repute, notably` (Q13).
- **A passive whose English object sits inside a phrase** is said in English's own passive, the
  object the subject: κόπτω's *to cut down the trees in it* is `having had the trees in it cut down`
  (EXO 27:20), περικαλύπτω's *to throw a veil* `having had a veil thrown over them` (28:20), γράφω's
  *to write a person's name* `having had a person's name written` (31:18), and the note says so (Q21).
- **An entry that marks no translation** gives its description as the English: λιγύριον, *a precious
  stone* (EXO 28:19), as σμάραγδος's *a precious stone of a green colour* is kept from inside its
  Latin (Q25).
- **A first translation that is only a preposition or a particle**, which an *or* completes, is read
  with the *or* as the printed entry gives it: θεῖον, `of or from the gods` (EXO 31:3); μυρεψικός *of
  or for unguents* (Q26). Alone, *of* says nothing, and in the anchored panel it reads as a case-marker.
- **A gloss given in the plural:** one whose plural is only its example's is inflected to the form
  (ὅρμημα's *longings*, `the longing`, in a singular); a sense the entry gives the plural — "in pl.",
  or the plural named as a sense's headword (τάλαντον's *scales*, οἰκέτης's *household*) — the
  singular leaves out, by `FORM_SENSES` (Q27).
- **An adjective used as a noun whose entry has one noun sense:** the noun sense heads, the
  adjective's senses after it, so the unit is not a headword alone: `the embroidered carpets — the
  embroidered carpets, the stitched and patched, … —` (ῥαφιδευτά, EXO 37:21) (Q30).
- **A deponent whose entry gives no passive** reads the middle's senses, even where the context asks
  for a passive, and the note says what the context asks: ἐπεσκεμμένων, EXO 39:2 (Q31).

---

## Prepositions and particles

### ἐν (with ἀρχή)

Not its own unit so far: ἐν ἀρχῇ is one unit, and ἐν's chain opens the ἀρχή chain (see
ἀρχή). Middle Liddell's first sense: *in, among* (with the dative) → *in*.

- **link:** `within, inside of, and by means of`
- **used:** GEN 1:1, JHN 1:1, JHN 1:2

Locative, instrumental, and sphere-of-operation senses are all live and none is chosen.
Fixed; it does not reduce in restatement.

### πρός + accusative

- **headword:** `towards the God` — Middle Liddell's accusative block opens at its 53rd sense
  group, *towards, to*; the static *with* first appears at the 66th. τὸν θεόν is articular.
- **chain (full):** `toward the God, facing him, oriented to him, in living motion and address toward him, held face to face in a nearness that never collapses into sameness`
- **short:** `facing, oriented toward, and in living address toward the God`
- **used:** JHN 1:1 (full), JHN 1:2 (short)

Directional, never static. Note in the apparatus wherever παρά / μετά / σύν were available
and not used. The lexicon rule removes *with* from the headword as well as the chain.

### παρά + genitive

- **headword:** `from the side of God` — Middle Liddell, first sense with the genitive: *from
  the side of*. θεοῦ is anarthrous.
- **chain:** `from alongside and from the side of God`
- **used:** JHN 1:6

### δέ

- **headword:** `but` — Middle Liddell, first sense.
- **chain:** `but, however, whereas, on the other hand`
- **used:** GEN 1:2

Soft adversative. Never rendered with the force of ἀλλά.

### ἐπάνω — plain text

`upon, over, and atop` (full) / `over and atop` (short). No unit. GEN 1:2, twice: full at the
abyss, short at the water.

### ἀπό + genitive

- **headword:** `from` — Middle Liddell, first sense with the genitive: *from, away from*.
- **chain:** `from, away from, far from, apart from`
- **used:** GEN 2:2, GEN 2:3

Separation, not source. Resting ἀπὸ τῶν ἔργων is a standing apart *from* the works.

### ὅτι

- **headword:** `that` — the conjunction; the lexicon prints two entries under this
  spelling and this is the second (see *Homographs* above). First sense *that*.
- **chain:** `that, seeing that, although, for that, because, inasmuch as`
- **used:** GEN 2:3

Both the *that* of reported speech and the *because* the sense wants; neither is chosen.

### ὅτε

- **headword:** `when` — Middle Liddell, first sense.
- **chain:** `when, sometimes`
- **used:** GEN 2:4

### Ordinals — plain text

`the sixth`, `the seventh`. No unit: Middle Liddell gives ἕκτος one sense, *sixth*, and
ἕβδομος *seventh*, so there is no range to open and a unit would only repeat the headword.
GEN 2:2, GEN 2:3.

### πρό + genitive

- **headword:** `before` — Middle Liddell, first sense *before*.
- **chain:** `before, in front of, further on, sooner, rather than`
- **used:** GEN 2:5, twice, both with the articular infinitive (πρὸ τοῦ γενέσθαι, πρὸ τοῦ
  ἀνατεῖλαι)

### ἐπί

- **headword:** `upon` — Middle Liddell, first sense *on, upon*.
- **chain:** `upon, on, in, at, near`
- **used:** GEN 2:5, twice — with the genitive (ἐπὶ τῆς γῆς) and with the accusative
  (ἐπὶ τὴν γῆν)

The entry opens with one heading for all three cases, and its tagged translations do not
separate them, so the case cannot be read off the lexicon the way it can for πρός and παρά.
One chain serves both, and the case is recorded here rather than guessed at in the text.

### ἐκ + genitive

- **headword:** `out of` — Middle Liddell, first sense *out of, from*.
- **chain:** `out of, forth from, from`
- **used:** GEN 2:6

### εἰς + accusative

- **headword:** `into` — Middle Liddell, first sense *into, to*.
- **chain:** `into, to, in, rest in`
- **used:** GEN 2:7, twice — of place (εἰς τὸ πρόσωπον) and of result (εἰς ψυχὴν ζῶσαν);
  GEN 2:9, twice; GEN 2:10

### ἐν — joined to its object

ἐν is never a unit by itself. It joins its object, as in ἐν ἀρχῇ:

- **ἐν μέσῳ** (GEN 2:9) — **headword** `in middle`; **chain** `within, inside of, and by
  means of the middle, in the middle, the centre, mid, between two`.
- **ἐν Εδεμ** (GEN 2:8) — the object is a proper name, which carries its own marker, so
  ἐν stands as plain text `in` and opens no chain.

A one-word anchor `in` is unusable in any case: `validate.py` would find it inside the fixed
aorist formula, *not a process observed in progress*, and refuse it as a bare headword.

### κατά

- **headword:** `down` — Middle Liddell, first sense *down, downwards*.
- **chain:** `down, downwards, down from, down upon, over, upon`
- **used:** GEN 2:8, GEN 2:18, GEN 5:1, GEN 5:3 (twice)

Like ἐπί, the entry heads all its cases together and its tagged translations do not separate
them. κατὰ ἀνατολάς is the idiom *eastward*, which the first sense does not give; the note
records the idiom and the reading prints the lexicon. κατʼ εἰκόνα at GEN 5:1 and κατὰ τὴν
ἰδέαν at 5:3 are *according to*, and are settled the same way.

### Adverbs of place — ἐκεῖ, ἐκεῖθεν

- ἐκεῖ — **headword** `there`; **chain** `there, in that place`. GEN 2:8, 2:11, 2:12.
- ἐκεῖθεν — **headword** `from that place`; **chain** `from that place, thence, thereafter,
  next`. GEN 2:10.

### ἔτι

- **headword:** `yet` — Middle Liddell, first sense *yet, as yet, still*.
- **chain:** `yet, as yet, still, further, besides, moreover`
- **used:** GEN 2:9

### κατέναντι

- **headword:** `over against` — the entry carries no translation of its own, reading
  `κατέναντι = κατεναντίον`; the senses are that entry's, *over against, opposite, before*.
- **chain:** `over against and opposite and before`
- **used:** GEN 2:14

### Ordinals, continued — plain text

`the second`, `the third`, `the fourth` (GEN 2:13, 2:14) and `four` (τέσσαρες, GEN 2:10), on
the same ground as `the sixth` and `the seventh`: one sense each, so no range to open.

### ἵνα

- **headword:** `that` — used as a conjunction, so the first conjunction sense, *that, in
  order that*; the entry's first sense is the adverb of place, *there, where*.
- **chain:** `that, in order that`
- **used:** GEN 3:3 (ἵνα μή, with `not` as plain text)

### οὐδέ

- **headword:** `but not` — Middle Liddell, first sense, *but not*, answering to μέν.
- **chain:** `but not, and not, nor, not even, not at all`
- **used:** GEN 3:3

### μήποτε

- **headword:** `that at no time` — used as a conjunction, so sense II, *that at no time,
  lest ever*; sense I is the adverb, *never, on no account*.
- **chain:** `that at no time and lest ever, never and on no account, perhaps`
- **used:** GEN 3:22

### ὡς

- **headword:** `as` — the relative, sense A.II. The entry opens with the accented
  demonstrative ὥς, *so, thus*, a different word, and those glosses are skipped by name.
- **chain:** `as, according as, considering, like`
- **used:** GEN 3:5, GEN 3:22

### ἕως + genitive

- **headword:** `until` — Middle Liddell, first sense *until, till*. The entry itself cites
  ἕως with the articular infinitive, ἕως τοῦ ἀποτῖσαι, the construction of GEN 3:19.
- **chain:** `until, till, while and so long as`
- **used:** GEN 3:19

### ἀνά — joined to its object

- **ἀνὰ μέσον** (GEN 3:15, four times) — **headword** `up to middle`; **chain** `up to, up
  along, and throughout the middle, in the middle, the centre, mid, between two`. ἀνά with
  the accusative: the entry describes that case as *motion upwards*, which glosses nothing and
  is skipped by name, and its first translation is *up to, up along*. The pair is the idiom
  *between*, recorded in the verse's note, as κατὰ ἀνατολάς was.

### μετά + genitive

- **headword:** `in the midst of` — Middle Liddell, first sense with the genitive, *in the
  midst of, among*; *along with* is the second and *with* the third. Perseus's opening
  summary, *in the midst of, among with gen., dat., and acc.*, is skipped by name.
- **chain:** `in the midst of, among, in common, along with, with, by means of`
- **used:** GEN 3:6, GEN 3:12, with the pronoun as plain text

### ἀπέναντι

- **headword:** `opposite` — Middle Liddell, one sense, *opposite, against*, c. gen.
- **chain:** `opposite and against`
- **used:** GEN 3:24

### ποῦ

- **headword:** `where` — *where?* first; *how? by what right?* second.
- **chain:** `where, at what point, how, by what right`
- **used:** GEN 3:9

### ἰδού

- **headword:** `lo` — Middle Liddell, first sense *lo! behold! see there!*
- **chain:** `lo, behold, see there`
- **used:** GEN 3:22

### Plain text — small words and single senses

- μή — `not`, like οὐ; οὐ μή — `no, not` (GEN 3:1).
- τί in τί ὅτι and τί τοῦτο — `why` (GEN 3:1, 3:13).
- καί as *also* — `also` (GEN 3:6).
- ἑαυτοῖς — `for themselves` (GEN 3:7).
- ἐπικατάρατος — `yet more accursed`: Middle Liddell's one sense (GEN 3:14, 3:17, 4:11).
- τὸ δειλινόν — `at evening`: filed under δειελινός, one sense (GEN 3:8).
- One sense each in GEN 4, so plain text: πρωτότοκος `the first-born` (4:4), περίλυπος `deeply
  grieved` (4:6), σήμερον `to-day` (4:14), ἑπτά `seven` and ἑπτάκις `seven times` (4:15, 4:24),
  ἑβδομηκοντάκις `seventy times` (4:24, LSJ), ἀδελφή `sister` (4:22), νεανίσκος `a youth` and
  ἐνωτίζομαι `hearken to` (4:23), υἱός `son` (4:17, 4:25, 4:26 — Middle Liddell's *A son* and *a
  son* are one sense).
- σφυροκόπος — `a hammer-beater`: in no lexicon here (4:22).
- εἰ, ἐάν — `if`; τί in ἵνα τί — `what` (4:6); ἐν τῷ εἶναι — `in the being of` (4:8). *(ἐάν corrected at Genesis 37: its entry's first translation is* if haply*, and it is a unit; see "ἐάν reads its entry".)*
- εἰμί with a participle (ἦν ἐργαζόμενος, 4:2; ἦν οἰκοδομῶν, 4:17) — `was, and kept on being,`
  before the participle's unit, the imperfect formula of 2:5 in short.
- One sense each in GEN 5, so plain text: every numeral — `two hundred`, `thirty`, `a hundred`,
  `nine hundred` and the rest (*the Thirty*, *the Forty*, *the Three Hundred* name bodies of men,
  not further senses of the number) — with ὀκτώ `eight` and τρεῖς `three` from LSJ; ἔτος `years`,
  `of years`; υἱός `sons`, `a son`; θυγάτηρ `daughters`. δέκα πέντε (5:10), printed as two words,
  is `fifteen`, and the note says so. *(Corrected before Genesis 38: two words, two numerals, `ten five`,
  as 17:25 and 37:2 read.)*
- εἰμί of age (ἦν Νωε ἐτῶν πεντακοσίων, 5:32) — the state formula of GEN 1:2 in full.
- τὸ before an infinitive (μετὰ τὸ γεννῆσαι, 5:4 and after) — not printed, as with τοῦ at 2:5. *(Retired before Genesis 37: the infinitive reads as a gerund with its article; see "The articular infinitive".)*
- GEN 6: ἄν and ἐάν after a relative or ὡς — `ever` (6:4, 6:17), as ἄν was at 2:17; the
  reflexives — `for themselves` (6:2, 6:4), `for yourself`, `yourself` (6:14, 6:19, 6:21);
  εἰμί — `are` (6:2), `being` (6:9), `is` and `may be` (6:17), `will be` (6:3, 6:19), `it will
  be` (6:21), and ἦσαν `were, and kept on being,` (6:4), the short formula, since the full one's
  *as* would stand beside ὡς's headword; δύο δύο — `two two` (6:19, 6:20).
- One sense each in GEN 6, so plain text: ἀσφαλτόω `you will smear with pitch` (6:14, LSJ);
  διώροφος `with two roofs or stories` (LSJ) and τριώροφος `of three stories or floors` (6:16);
  εἴκοσι `twenty`; θυγάτηρ `daughters`; υἱός `sons`.
- One sense each in GEN 7, so plain text: διατρέφω `to sustain continually` (7:3); ἑξακοσιοστός
  `six hundredth` (7:11, LSJ); μείς `month`; εἰκάς `twentieth`, *the twentieth day of the month*
  (7:11); ἡ ξηρά `the dry land` (7:22), the noun sense of ξηρός; ἐπάνω without a genitive —
  `upon, over, and atop` (7:20), and with one `over and atop` (7:18), the forms of GEN 1:2; ὕδωρ,
  `the water`, `of water` (7:6–24); ἐν τῷ ἑξακοσιοστῷ ἔτει — `in the six hundredth year` (7:11),
  ἐν joined to plain words as at 2:8.
- One sense each in GEN 8, so plain text: ἐλαττονόω `was being diminished` (8:3, 8:5, LSJ);
  θυρίς `the window` (8:6); θυσιαστήριον `an altar`, `the altar` (8:20); εὐωδία `of a sweet smell`
  (8:21). Ordinals stay plain as at 2:13 and 4:19, though δέκατος and πρῶτος have further senses,
  *a tithe*, *foremost*: `the tenth`, `the eleventh`, `the first` (8:5, 8:13), and `month`.
- ὁλοκάρπωσις — `whole burnt-offerings` (8:20): in neither Middle Liddell nor LSJ, which has only
  the verb ὁλοκαρπόομαι, *to be offered as a whole burnt-offering*. Plain text, as σφυροκόπος.
- εἷς as a numeral: ἐν τῷ ἑνὶ καὶ ἑξακοσιοστῷ ἔτει — `in the [[one]] and six
  hundredth year` (8:13); μιᾷ τοῦ μηνός — `[[one]] of the month`, the chain of GEN 2:21.
- One sense each in GEN 9, so plain text: κατακυριεύω `gain dominion over` (9:1); ἀμπελών `a
  vineyard` (9:20); οἶνος `of the wine` (9:21, 9:24), once *beer*, Middle Liddell's piece of
  *barley-wine, a kind of beer*, is left out; εὐλογητός `blessed` (9:26); ἐπικατάρατος `yet more accursed`, as
  at 3:14 (9:25); ὀπισθοφανῶς `backwards` (9:23, LSJ); numerals and `years` (9:28, 9:29).
- καὶ γάρ — `also for` (9:5): καί as *also*, γάρ plain as at 2:5.
- τὸ ὑμέτερον αἷμα — `the [[your]] [[blood]]` (9:5): the article plain before the adjective's
  unit, as before τὸ πρὸς ἑσπέραν at 8:11.
- ἦν of a standing relation (Χαμ ἦν πατὴρ Χανααν, 9:18) — the state formula of 1:2 in full; ἦσαν
  opening the verse — `were, and kept on being,` as at 6:4.

### διά + genitive

- **headword:** `through` — Middle Liddell, with the genitive, *in a line, through, right
  through*; Perseus's opening summary is skipped by name.
- **chain:** `through, right through, by means of, by the agency of`
- **used:** GEN 4:1 (διὰ τοῦ θεοῦ)

### μετά + accusative

- **headword:** `into the middle of` — the first translation for the accusative; *after*, of
  time, comes later.
- **chain:** `into the middle of, coming among, in pursuit and quest of, after`
- **used:** GEN 4:3 (μεθʼ ἡμέρας)

### ὀρθῶς, οὕτως, λίαν

- ὀρθῶς — **headword** `straight`; **chain** `straight, uprightly, rightly, truly and
  correctly, justly`. The adverb of ὀρθός, whose first sense is *straight*. GEN 4:7.
- οὕτως — **headword** `in this way`; **chain** `in this way, in this manner, so, thus, even so,
  so much`. GEN 4:15.
- λίαν — **headword** `very`; **chain** `very and exceedingly, very much, overmuch`. GEN 4:5.

### Small words new in GEN 6

- ἡνίκα — **headword** `at which time`; **chain** `at which time and when, since, whenever`. 6:1.
- διά + accusative — **headword** `through`, the entry's first translation for that case;
  **chain** `through, throughout and over, during, by aid of and by means of, by reason of,
  because of, for the sake of`. 6:3, with the articular infinitive.
- ἐναντίον + genitive — **headword** `in the presence of`, the neuter used as a preposition inside
  the entry for ἐναντίος; **chain** `in the presence of, before, opposite and face to face,
  against`. 6:8, 6:11, 6:13.
- ὑποκάτω — **headword** `below`; **chain** `below and under`. 6:17.
- ὅσος — **headword** `as great as`, after Perseus's Latin *quantus*, left out; **chain** `as great
  as, as much as, as far as, as long as, as many as`. 6:17, 6:22.
- οὖν — **headword** `really`; **chain** `really, at all events, surely, so, then and therefore`.
  6:14.
- τις — **headword** `any one`; **chain** `any one, some one, many a one, each one, every man`. 6:5.
- ἐπιμελῶς — **headword** `carefully`, the adverb of ἐπιμελής, *careful*; **chain** `carefully,
  anxiously, attentively`. 6:5.
- ἔσωθεν, ἔξωθεν, ἄνωθεν — `from within` / `from within, within`; `from without` / `from without,
  outside, without and free from`; `from above` / `from above, from on high, from the upper
  country, above and on high, from the beginning, by descent, over again and anew`. 6:14, 6:16.
- ἐκεῖνος — `those`, `that`, `to those` / `those, the ones there, the more remote`, in the form:
  the chain of GEN 2:12. 6:4, 6:21.
- καθά — **headword** `according as`; **chain** `according as and just as, like as if and exactly as`.
  7:9, 7:16.
- ἔτι — **headword** `yet`, the chain of GEN 2:9. 7:4.
- σφόδρα, σφοδρῶς — `very` / `very and very much and exceedingly and violently, far, most certainly`;
  `vehemently` / `vehemently, violently, excessively, impetuously, strongly and robustly`, the
  adverb of σφοδρός, *vehement*. 7:18, 7:19.
- ἔξωθεν with a genitive — `from without`, the chain of GEN 6:14. 7:16.

### Small words new in GEN 9

- πλήν without a genitive — **headword** `but`, the entry's first sense as an adverb; *more than,
  except, save* are the preposition's, with the genitive, and stand last; **chain** `but, than,
  much like, only not, except that, save that, except, save so far as, more than, save, short of`.
  9:4.
- ὥστε with the infinitive — **headword** `so as to`, the first conjunction sense; **chain** `so as
  to, as to, on the condition that, and so and therefore and consequently, as and as being, since
  it was`. 9:15.
- ἀντί + genitive — **headword** `over against`, sense 0, *over against, opposite*; Perseus's
  summary and the senses *IN COMPOS.* are skipped by name; **chain** `over against, opposite,
  instead and in the place of, as good as and equal to, at the price of and for, for the sake of,
  set against and compared with`. 9:6, and 2:21 and 4:25, whose chain first stopped at *as good
  as*, the fifth of the senses a word card shows.
- ὑπό + accusative — **headword** `towards and under`, the entry's first translation for that case;
  **chain** `towards and under, under and into, under and before, under, in subjection, towards,
  about, about the time, to a certain degree and in some measure`. 9:2, ὑπὸ χεῖρας.
- ἔξω without a genitive — **headword** `out`; **chain** `out, out of, outside, without, foreign,
  clear of, beyond and over, but and except`. 9:22.
- ὑμέτερος — **headword** `your`; **chain** `your, yours, your part and your business, your
  character`. 9:5.
- ἐν with an articular infinitive — ἐν τῷ συννεφεῖν με — `in the collecting clouds` / `within,
  inside of, and by means of the collecting clouds, the being cloudy, the wearing a clouded look`,
  then `of me` (9:14): joined, as ἐν always is, with the infinitive's subject in the genitive's
  English, as at 4:8.
- τοῦ with an infinitive (τοῦ καταφθεῖραι 9:11, τοῦ μνησθῆναι 9:16) — not printed, as at 2:5.

### Small words new in GEN 10

- ὅθεν — **headword** `from whom` (`whence` since EXO 30, which reads the gloss MARKUP_LOST recovers): Perseus leaves the entry's first gloss, *whence, from which*,
  untagged, and the first it tags is *from whom*; **chain** `from whom, from whatever source and in
  what manner soever, where, whence and wherefore`. 10:14.
- ἕως before an infinitive with no article (ἕως ἐλθεῖν, 10:19, 10:30) — `until`, the chain of GEN
  3:19; ἕως Λασα (10:19) the same.
- ἕκαστος — **headword** `every`; **chain** `every, every one, each, each one, all and each one,
  singly and by itself, each by himself`. 10:5.
- καί as *also* (καὶ αὐτῷ, 10:21) — `also`, plain, as at 3:6.
- One sense each in GEN 10, so plain text: νῆσος `islands` (10:5, 10:32), once the etymology *to
  swim, floating land* is left out; πρωτότοκος `first-born` (10:15), as at 4:4; κατοίκησις `the
  settling in` (10:30); δύο `two`; υἱός `sons`.
- The article before a people's name (τοὺς Λουδιιμ, τὸν Χετταῖον, τῶν Χαναναίων) is not printed,
  as before a person's name. *(Retired before Genesis 37: an exception made for English's sake.
  Every name's own article prints now, `the Λουδιιμ`, `to the Jacob`; see "Every declined word".)*

### Words new in GEN 35

- The chapter has no verse 21: Rahlfs's apparatus notes at that number `21 𝔐: uide 𝔊 16`, the Hebrew's
  verse standing in the Greek at 35:16. The transcription runs 35:1-20 and then 35:22-29.
- χαβραθα — the Hebrew kibrat carried into Greek untranslated, a stretch of ground of unknown length.
  The printed page has it in lower case where the digital module capitalises it, so it is filed in
  `printed`, and it is a name with no capital in either panel, as τὰ χερουβιμ is at 3:24. 35:16.
- αἴρω — Ἄρατε is active, so the chain is the Act. section only; the Mid. senses (*to take up for
  oneself, carry off, win*) are filed in NOT_SENSES. 35:2.
- σπένδω — likewise active here: *to pour a drink-offering*. The Mid. is *to make a treaty*, since
  treaties were sealed by pouring, and that sense is not this form's. 35:14.
- ἐπιφαίνω — ἐπεφάνη is passive, so the active senses passivized lead and the intransitive *shewed
  light, shone upon* follows. 35:7.
- θλῖψις — Middle Liddell has θλίβω but not the noun. LSJ gives three senses and cites this very
  verse for the third, *oppression, affliction*. 35:3.
- κατώτερος — no Middle Liddell entry; LSJ heads the comparative of κάτω on its own. Here it stands
  as an adverb with the genitive, below Bethel. 35:8.
- ὀσφύς — filed as Middle Liddell keys it and MorphGNT files it, all eight times. (This line once
  read ὀσφῦς, "the circumflex MorphGNT gives it"; MorphGNT gives none. Corrected at Genesis 37.) 35:11.
- σκληρῶς — the adverb, filed inside σκληρός, and taking the adjective's senses, as βαρέως does at
  31:35. Its chain is the one σκληρός already has from 21:11. 35:17.
- Βάλανος and Υἱός — two Greek words Rahlfs prints capitalised as names, and so names here with a
  `# corpus` note apiece: Βάλανος πένθους is the oak of weeping, Υἱὸς ὀδύνης μου is Ben-ʾÔnî. The
  common nouns βάλανος and υἱός stand in the same chapter. 35:8, 35:18.
- `covered over` now heads two entries: κατακρύπτω here and ἐπικαλύπτω at 7:19, as `the men` heads
  both ἄνθρωπος and ἀνήρ. A later chapter must name the verse it means. 35:4.
- One sense each in GEN 35, and so kept as units with a one-word chain: δυστοκέω `was in sore
  travail`; τοκετός `birth`; τροφός `the feeder`; and the numerals stand plain.

| lemma | headword | chain | used |
| --- | --- | --- | --- |
| αἴρω | `take up` | `take up and raise and lift up, bear and sustain, raise up and exalt, excite, extol and exaggerate, lift and take away and remove, take off and kill` | 35:2 |
| αὐξάνω | `be increased` | `be increased, be made to grow, be exalted and magnified, be advanced and promoted` | 35:11 |
| βάλανος | `the acorn` | `the acorn, the similar fruit and date, the iron peg and bolt-pin` | 35:8 |
| διασῴζω | `saved through` | `saved through, brought safe through, kept safe, preserved` | 35:3 |
| δυστοκέω | `was in sore travail` | `was in sore travail` | 35:16 |
| θάπτω | `buried` | `buried, honoured with funeral rites` | 35:29 |
| θάπτω | `was buried` | `was buried, was honoured with funeral rites` | 35:19 |
| θαρσέω | `be of good courage` | `be of good courage and take courage, be over-bold and audacious, have confidence in, venture` | 35:17 |
| θεός | `the gods` | `the gods, the deities` | 35:2, 35:4 |
| θλῖψις | `of pressure` | `of pressure, of crushing and castration, of oppression and affliction` | 35:3 |
| καθαρίζω | `make yourselves clean` | `make yourselves clean and cleanse yourselves` | 35:2 |
| καταδιώκω | `pursued closely` | `pursued closely` | 35:5 |
| κατακρύπτω | `covered over` | `covered over and hid away and concealed, used concealment and concealed himself` | 35:4 |
| κατώτερος | `lower` | `lower, more southerly, later and younger` | 35:8 |
| λίθινος | `of stone`, plain text: one translation; EXO 11 took out what the entry does not give (*stony* is an example's, in `NOT_SENSES`) | | 35:14 |
| μαῖα | `the good mother` | `the good mother and dame, the fostermother and nurse, the true mother, the midwife` | 35:17 |
| μνημεῖον | `of the memorial` | `of the memorial, of the remembrance, of the record, of the monument` | 35:20 |
| πένθος | `of mourning` | `of mourning, of grief and sadness, of a mourning garb, of a misfortune and calamity` | 35:8 |
| παιδίσκη | `of a young girl` | `of a young girl and maiden, of a young slave and courtesan` | 35:25, 35:26 |
| παλλακή | `of the concubine` | `of the concubine and mistress` | 35:22 |
| παραγίνομαι | `came to be beside` | `came to be beside, came near and arrived, was present and stood by, came to help` | 35:9 |
| πλήρης | `full` | `full, filled, complete, satisfied, whole and entire` | 35:29 |
| πορεύομαι | `I was driven` | `I was driven, I was carried, I went, I walked, I marched, I went across and passed` | 35:3 |
| πρωτότοκος | `first-born`, plain text | one translation, as at 4:4; *first-fruits* is in no entry, and EXO 11 took it out of nine units | 35:23 |
| πύργος | `of the tower` | `of the tower, of the city walls with towers, of the movable tower for storming, of the tower of defence, of the highest part of any building, of the troops drawn up in close order and the column` | 35:16 |
| σπένδω | `poured a drink-offering` | `poured a drink-offering, made a drink-offering, poured` | 35:14 |
| σπονδή | `a drink-offering` | `a drink-offering, a solemn treaty, a truce, the treaty itself` | 35:14 |
| στολή | `the equipments` | `the equipments and armaments, the equipment and raiment and apparel, the pieces of dress and garments and robes` | 35:2 |
| συναγωγή | `bringings together` | `bringings together and unitings, places of assembly and synagogues, drawings together and contractings, formings in column, pursings up, wrinklings, collections, conclusions and inferences` | 35:11 |
| τερέμινθος | `the terebinth` | `the terebinth, the turpentine tree` | 35:4 |
| τοκετός | `in birth` | `within, inside of, and by means of birth, delivery` | 35:16 |
| τροφός | `the feeder` | `the feeder and rearer and nurse` | 35:8 |
| φόβος | `fear` | `fear, flight, panic, awe and reverence, the object of fear and terror` | 35:5 |
| ἀλλάσσω | `change` | `change, alter, exchange, give in exchange and barter, take one in exchange for another` | 35:2 |
| ἀναβαίνω | `go up` | `go up, mount, ascend, go up to, rise, come up, come to and arrive at, go up country, go aboard` | 35:1 |
| ἀναβαίνω | `let us go up` | `let us go up, let us mount, let us ascend, let us go up to, let us rise, let us come up, let us come to and arrive at, let us go up country, let us go aboard` | 35:3 |
| ἀποδιδράσκω | `to run away` | `to run away, to run off and escape, to run away from` | 35:1, 35:7 |
| ἀποθνήσκω | `was dying off` | `was dying off and dying, was being put to death and slain` | 35:18 |
| ἀπόλλυμι | `destroyed utterly` | `destroyed utterly and killed and slew, destroyed and demolished and wasted, talked and bored to death, lost utterly` | 35:4 |
| ἀφίημι | `to send forth` | `to send forth, to discharge, to let go and loose and set free, to let alone and leave, to give up and hand over, to permit and allow` | 35:18 |
| ἐν, with οὖς | `in the ears` | `within, inside of, and by means of the ears` | 35:4 |
| ἐνώτιον | `the earrings` | `the earrings` | 35:4 |
| ἐξαίρω | `lifted out` | `lifted out, took out and removed, lifted up and raised, stirred up and excited, carried off and carried away, made an end of and destroyed, set out and departed` | 35:5 |
| ἐπέκεινα | `on yonder side` | `on yonder side and beyond, the part beyond and the far side` | 35:16 |
| ἐπακούω | `to the one having hearkened` | `to the one having hearkened, to the one having listened, to the one having given ear` | 35:3 |
| ἐπιφαίνω | `was shewn forth` | `was shewn forth, was displayed, was shewn off, came into light and came suddenly into view, presented himself and shewed himself and appeared, shewed light and shone upon` | 35:7 |
| ἐπιχέω | `poured upon` | `poured upon, poured over, poured out over` | 35:14 |
| ὀδύνη | `of pain of body` | `of pain of body, of pain of mind and grief and distress` | 35:18 |
| ὀσφύς | `of the loin` | `of the loin, of the loins, of the lower part of the back` | 35:11 |

### Words new in GEN 34

- ἐγχώριος — *in* or *of the country*, and as a noun *a dweller in the land, inhabitant*. The noun
  sense heads it, as with ἡ περίχωρος at 13:10, since it stands here as a noun. 34:1.
- μιαίνω — *to stain, dye* first, of ivory dyed with purple; the defilement is the second sense.
  The Greek of this chapter says staining, never violence. 34:5, 34:13, 34:27.
- ἀσχήμων — *misshapen, unseemly*, the neuter as a noun: the deed is named by its shape. 34:7.
- κατανύσσω — *to stab, gouge*, in the passive of the mind, as at 27:38. 34:7.
- προαιρέω — προείλατο is the middle, so the chain is Middle Liddell's Mid. section: *to take away
  first for oneself*, then *to choose before, prefer*. 34:8.
- ἐπιγαμβρεύω and ἐγκτάομαι — one sense each, and both narrow: *to marry as the next of kin*, and
  *to acquire possessions in a foreign country*. 34:9, 34:10.
- πλατύς — *wide, broad*; *large* and *widespread* belong to an example (*broad herds*) and are filed
  in NOT_SENSES. The separate entry πλατεῖα, the street, is what 19:2 takes. 34:10, 34:21.
- φερνή — *that which is brought by the wife*, a dowry; in this verse the bridegroom offers it, as the
  Hebrew mōhar is offered. 34:12.
- ὁμοιόω — passive here, so the active senses passivized lead and the passive-only ones follow:
  *be made like, be likened and compared*, then *become like, be like*. 34:15, 34:22, 34:23.
- ἀσφαλῶς — the adverb, filed inside ἀσφαλής, whose entry glosses it *in all senses of the adj., in
  safety, with certainty*: that gloss heads it and the adjective's senses follow, as with ἀφρόνως at
  31:28. The epic adverb ἀσφαλέως has its own glosses, which are not this word's. 34:25.
- πόνος — *work, hard work, toil* first, and *the consequence of toil, pain* only at II: the Greek
  names the labour, not the soreness. 34:25.
- τραυματίας — Middle Liddell has nothing; LSJ gives *wounded man* and *corpse of one slain*. 34:27.
- ὀλιγοστός — *one out of a few*, the superlative form of ὀλίγος. 34:30.
- βοῦς — a noun of common gender: LSJ heads it `βοῦς ... ὁ and ἡ`, and Middle Liddell names no gender
  at all. So the lemma has no gender of its own and each occurrence takes what the text marks — the
  article first (τὰς βόας 18:7 feminine, τοὺς βόας 32:8 and 34:28 masculine, αἱ βόες 33:13 feminine),
  then a contrast beside it (βόας τεσσαράκοντα against ταύρους δέκα at 32:16, so cows against bulls).
  Where nothing marks it (13:5, 26:14, 30:43, 32:6) the corpus keeps the masculine. The gender never
  reaches the reading text: the headword is `cow` either way, since it is the entry's first English
  translation — *a bullock, bull, ox* stands inside the Latin, which is skipped.
- One sense each in GEN 34, and so plain text: ἀδελφή `sister`; ἀρσενικός `male`; παρασιωπάω
  `passed over in silence`; αἰχμαλωτεύω `took prisoner`; and the numerals.

| lemma | headword | chain | used |
| --- | --- | --- | --- |
| αἰχμαλωτεύω | `took prisoner` | `took prisoner` | 34:29 |
| γίνομαι | `you may come to be` | `you may come to be, you may arise, you may be brought into existence` | 34:15 |
| δίδωμι | `we will give` | `we will give, we will grant, we will provide, we will give over and deliver up` | 34:11, 34:16, 34:21 |
| διαρπάζω | `tore in pieces` | `tore in pieces, effaced, spoiled and plundered, seized as plunder` | 34:27, 34:29 |
| εἰρηνικός | `of peace` | `of peace, for peace and peaceful` | 34:21 |
| εἰσακούω | `you may hearken` | `you may hearken and give ear to, you may hear, you may hearken to and give heed to` | 34:17 |
| εὑρίσκω | `may I find` | `may I find, may I find out, may I discover, may I get and gain` | 34:11 |
| καταμανθάνω | `to observe well` | `to observe well and examine closely, to learn thoroughly, to perceive and understand, to discover and find, to consider` | 34:1 |
| κατανύσσω | `were stabbed` | `were stabbed and gouged, were sorely pricked, were bewildered and stunned` | 34:7 |
| κατοικέω | `to those inhabiting` | `to those inhabiting, to those occupying, to those dwelling and living, to those settled` | 34:30 |
| κατοικέω | `we will dwell in` | `we will dwell in, we will settle in, we will colonise, we will inhabit, we will settle and dwell, we will lie and be situate` | 34:15 |
| κοιμάω | `having been lulled` | `having been lulled, having been hushed to sleep and put to sleep, having been lulled to rest and stilled and calmed, having fallen asleep, having gone abed and lain abed, having slept, having fallen asleep and died, having kept watch at night` | 34:7 |
| λαμβάνω | `we will take` | `we will take, we will receive, we will take hold of and grasp and seize` | 34:16, 34:21 |
| λυπηρός | `painful` | `painful and distressing, causing sorrow, causing pain and troublesome and vexatious and offensive` | 34:7 |
| μάχαιρα | `of a large knife` | `of a large knife and dirk, of a knife for cutting up, of a short sword and dagger, of a sabre and bent sword, of a rasor` | 34:26 |
| μιαίνω | `stained` | `stained, dyed, defiled and sullied, tainted and defiled` | 34:5, 34:13, 34:27 |
| μιαίνω | `stained` | `stained, dyed, defiled and sullied, tainted and defiled` | 34:5, 34:13, 34:27 |
| μισητός | `hateful` | `hateful` | 34:30 |
| νεανίσκος | `the youth` | `the youth` | 34:19 |
| οἰκέω | `let them inhabit` | `let them inhabit, let them occupy, let them dwell and live, let them be settled` | 34:21 |
| οἰκέω | `they will inhabit` | `they will inhabit, they will occupy, they will dwell and live, they will be settled` | 34:23 |
| οἰκέω | `we will inhabit` | `we will inhabit, we will occupy, we will dwell and live, we will be settled` | 34:16 |
| οἰκία | `in the buildings` | `within, inside of, and by means of the buildings, the houses, the dwellings, the households and domestic establishments, the households and inmates of the house, the houses and families from which one is descended` | 34:29 |
| παρασιωπάω | `passed over in silence` | `passed over in silence` | 34:5 |
| παρθένος | `of the maid` | `of the maid and maiden and virgin and girl` | 34:3 |
| περιτέμνω | `cut themselves` | `cut themselves, clipped themselves round about, pruned themselves, cut themselves off, cut themselves off and hemmed themselves in all round, curtailed themselves of, cut themselves off and intercepted` | 34:24 |
| περιτέμνω | `they have been cut` | `they have been cut and it stands so, they have been clipped round about, they have been pruned, they have been cut off, they have been cut off and hemmed in all round, they have been curtailed of, they have been cut off and intercepted` | 34:22 |
| περιτέμνω | `to be cut` | `to be cut, to be clipped round about, to be pruned, to be cut off, to be cut off and hemmed in all round, to be curtailed of, to be cut off and intercepted` | 34:15, 34:17, 34:22 |
| περιτέμνω | `to be cut` | `to be cut, to be clipped round about, to be pruned, to be cut off, to be cut off and hemmed in all round, to be curtailed of, to be cut off and intercepted` | 34:15, 34:17, 34:22 |
| πλατύς | `wide` | `wide and broad, flat and level, broad-shouldered, flat, a street, the flat of the hand, salt and brackish` | 34:10, 34:21 |
| πληθύνω | `make full` | `make full and increase and multiply` | 34:12 |
| ποιέω | `you have made` | `you have made and it stands made, you have done and it stands done, you have produced and it stands produced, you have created and it stands created` | 34:30 |
| προαιρέω | `took away first for himself` | `took away first for himself, removed out of his way, chose before and preferred, preferred to do, purposed and proposed to do` | 34:8 |
| πόνος | `in work` | `within, inside of, and by means of work, hard work and toil, toil and labour, bodily exertion and exercise, a work and task and business, implements for labour and stock in trade, the consequence of toil and distress and trouble and suffering and pain, anything produced by work` | 34:25 |
| πόρνη | `to a harlot` | `to a harlot and prostitute` | 34:31 |
| πύλη | `the one wing of a pair of double gates` | `the one wing of a pair of double gates, the gates of a town, the house-door, the nether world and hell, the entrance, the orifice, the entrance into a country through mountains and the mountain-pass, the narrow straits` | 34:20, 34:24 |
| στόμα | `in mouth` | `within, inside of, and by means of mouth, the mouth as the organ of speech, the mouthpiece, the face, the chasm and cleft` | 34:26 |
| συγκόπτω | `they will break up` | `they will break up and cut up, they will thrash soundly and pound well` | 34:30 |
| συνάγω | `having been brought together` | `having been brought together, having been gathered together, having been collected, having been convened, having been joined in one and united, having been received into a house, having been drawn together and narrowed and contracted, having been concluded and inferred` | 34:30 |
| ταπεινόω | `lowered` | `lowered, lessened, disparaged, humbled and abased, made lowly and humbled` | 34:2 |
| τετράπους | `the four-footed` | `the four-footed, the quadrupeds, the four feet in length` | 34:23 |
| τραυματίας | `the wounded men` | `the wounded men, the corpses of ones slain` | 34:27 |
| φερνή | `that which is brought by the wife` | `that which is brought by the wife, the dowry and portion, the dower, the bridal gifts` | 34:12 |
| χράομαι | `they should use` | `they should use, they should have and use, they should indulge, they should experience and suffer and be subject to, they should come to, they should live under, they should make use of, they should treat, they should be intimate with, they should be in need and yearn after, they should have in use and possess` | 34:31 |
| χρονίζω | `spent time` | `spent time, took time and tarried and lingered and delayed and was slow, remained long` | 34:19 |
| ἀκροβυστία | `foreskin` | `foreskin, circumcision, uncircumcision, the uncircumcised` | 34:14 |
| ἀπέρχομαι | `we will go away` | `we will go away, we will depart from, we will depart, we will depart from life` | 34:17 |
| ἀρέσκω | `made good` | `made good and made up, made amends, pleased and satisfied and flattered` | 34:18 |
| ἀριθμός | `in number` | `within, inside of, and by means of number, amount and sum and extent, mere number and quantity, a numbering and counting, the science of numbers and numeration and arithmetic` | 34:30 |
| ἀσφαλῶς | `in safety` | `in safety and with certainty, not liable to fall, immoveably, steadfastly, firmly, unfailingly, trustily, surely, certainly, safely and securely` | 34:25 |
| ἀσχήμων | `misshapen` | `misshapen and unseemly and shameful, indecorous` | 34:7 |
| ἄνθρωπος | `to a man` | `to a man, to a human being, to mankind` | 34:14 |
| ἄρχων | `the ruler` | `the ruler and commander and chief and captain, the chief magistrate` | 34:2 |
| ἐγκτάομαι | `acquire possessions in` | `acquire possessions in` | 34:10 |
| ἐγχώριος | `of the dwellers in the land` | `of the dwellers in the land, of the inhabitants, of the ones in and of the country, of the ones according to the custom of the country` | 34:1 |
| ἐκπορεύομαι | `the ones going out` | `the ones going out, the ones going forth, the ones marching out` | 34:24 |
| ἐκτρίβω | `I will be rubbed out` | `I will be rubbed out, I will be rubbed hard, I will be destroyed root and branch, I will be rubbed constantly and worn out` | 34:30 |
| ἐμπορεύομαι | `let them travel` | `let them travel, let them travel for traffic and be merchants and trade and traffic, let them import, let them make gain of and overreach` | 34:21 |
| ἐμπορεύομαι | `travel` | `travel, travel for traffic and be merchants and trade and traffic, import, make gain of and overreach` | 34:10 |
| ἐν, with αὐτός | `in her` | `within, inside of, and by means of her` | 34:10 |
| ἐν, with σύ | `in you` | `within, inside of, and by means of you` | 34:15 |
| ἐν, with ἡμεῖς | `in us` | `within, inside of, and by means of us` | 34:10 |
| ἐπιγαμβρεύω | `marry as the next of kin` | `marry as the next of kin` | 34:9 |
| ἔγκειμαι | `was lying in` | `was lying in and wrapped in, was involved in, was pressing upon, was urgent and insisting, was devoted to` | 34:19 |
| ἔνδοξος | `most held in esteem` | `most held in esteem and honour and of the highest repute, most notable` | 34:19 |
| ὀλιγοστός | `one out of a few`, plain text: one translation; EXO 11 took out what the entry does not give (*the smallest space* is an example's, in `NOT_SENSES`) | | 34:30 |
| ὁμοιόω | `let us be made like` | `let us be made like, let us be likened and compared, let us become like, let us be like` | 34:23 |
| ὁμοιόω | `they will be made like` | `they will be made like, they will be likened and compared, they will become like, they will be like` | 34:22 |
| ὁμοιόω | `we will be made like` | `we will be made like, we will be likened and compared, we will become like, we will be like` | 34:15 |
| ὄνειδος | `reproach` | `reproach and censure and blame, disgrace, matter of reproach` | 34:14 |
| ὄνος | `the asses` | `the asses, the beasts of burden, the windlasses and pulleys, the upper millstones, the beakers and wine-cups` | 34:28 |

### Words new in GEN 33

- ἐπιδιαιρέω — *to divide anew*, of the ranking of the wives and children before Esau. 33:1.
- ἔσχατος — *outermost* first, and *the last* third: Rachel and Joseph are put outermost. 33:2.
- προσεγγίζω — one sense, *to approach*, three times over as each household comes near. 33:6, 33:7.
- βιάζω — the middle, *to overpower by force, press hard*: Jacob presses the gift on Esau. 33:11.
- λοχεύω — *to bring forth, bear*, in the passive of the flocks in labour. 33:13.
- σχολή — *spare time, leisure*: κατὰ σχολήν, at the pace the road allows, and κατὰ πόδα at the
  children's step. 33:14.
- πόρευσις — Middle Liddell has nothing; LSJ gives it no gloss of its own but reads "= πορεία", and
  cites this verse, so the senses are πορεία's. 33:14.
- Σκηναί and Παρεμβολαί — two place-names the Greek translates and Rahlfs prints with a capital, and in
  33:17 the common noun σκηνάς stands in the same verse as the name Σκηναί. 32:3, 33:17.
- Σαλημ — the Hebrew is *šālēm ʿîr šĕkem*, *safe to the city of Shechem*; the Greek reads Salem as a
  place, as at 14:18. 33:18.
- εὐθεῖαν — the feminine of εὐθύς, of the straight way. The lexicon prints two entries under the one
  spelling and the project files the adverb's, so the chain here reads `straightway`. 33:12.
- ἑκατὸν ἀμνῶν — a hundred lambs, where the Hebrew has a hundred *qĕśîṭâ*, a weight the Greek does not
  name. 33:19.
- One sense each in GEN 33, and so plain text: ἑπτάκις `seven times`; θυσιαστήριον `an altar`, kept as a
  unit; τίς `what`; and the numerals.

| lemma | headword | chain | used |
| --- | --- | --- | --- |
| βιάζω | `overpowered by force` | `overpowered by force and pressed hard, did them violence, laid violent hands on, forced, used force and struggled, forced one's way, increased in violence` | 33:11 |
| γινώσκω | `learns to know` | `learns to know, perceives, marks, learns, discerns and distinguishes` | 33:13 |
| δέχομαι | `take` | `take, accept, receive, receive in exchange for, take rather and choose` | 33:10 |
| εὐδοκέω | `you will be well pleased` | `you will be well pleased, you will consent, you will be glad` | 33:10 |
| εὑρίσκω | `I have found` | `I have found and it stands so, I have found out, I have discovered, I have gotten and gained` | 33:10 |
| θυσιαστήριον | `an altar` | `an altar` | 33:20 |
| καταδιώκω | `I may pursue closely` | `I may pursue closely` | 33:13 |
| καταλείπω | `I will leave behind` | `I will leave behind, I will leave as an heritage, I will forsake and abandon and leave in the lurch, I will leave remaining, I will leave alone` | 33:15 |
| κλαίω | `they wept` | `they wept, they lamented, they wailed, they wept for` | 33:4 |
| λοχεύω | `are brought forth` | `are brought forth and borne, are brought to the birth and attended in childbirth and delivered, are delivered and bear children, are born` | 33:13 |
| οἰκία | `buildings` | `buildings, houses, dwellings, households and domestic establishments, households and inmates of the house, houses and families from which one is descended` | 33:17 |
| παιδάριον | `of the young little boys` | `of the young little boys, of the young slaves` | 33:14 |
| παρεμβάλλω | `put in beside` | `put in beside and inserted and interpolated and interposed, insinuated, put in line with, fell into line and encamped` | 33:18 |
| πορεύομαι | `we will be driven` | `we will be driven, we will be carried, we will go, we will walk, we will march, we will go across and pass` | 33:12 |
| πούς | `foot` | `foot, talon, the foot of a hill` | 33:14 |
| προέρχομαι | `let him go forward` | `let him go forward, let him go on, let him advance, let him go before` | 33:14 |
| προέρχομαι | `went forward` | `went forward, went on, advanced, went before` | 33:3 |
| προσεγγίζω | `approached`, plain text: one translation; EXO 11 took out what the entry does not give, the entry's *to approach* (*came near* was not its first sense) | | 33:6, 33:7 |
| προσεγγίζω | `approached`, plain text: one translation; EXO 11 took out what the entry does not give, the entry's *to approach* (*came near* was not its first sense) | | 33:6, 33:7 |
| προσπίπτω | `fell upon` | `fell upon, struck against, fell against, attacked and assaulted, ran to, embraced, fell in with and lighted upon and met with` | 33:4 |
| πρῶτος, with ἐν | `in first` | `within, inside of, and by means of first, first and foremost, outermost, first men, first prize, first part and beginning, first and highest, extremities, chief` | 33:2 |
| πόλις | `city` | `city, citadel, country, body of citizens, state` | 33:18 |
| πόρευσις | `of the walking` | `of the walking and mode of walking, of the going and journey and way and passage, of the march, of the crossing of water` | 33:14 |
| σχολή | `spare time` | `spare time, leisure, rest, ease, rest from, idleness, the learned discussion and lecture` | 33:14 |
| τράχηλος | `the neck` | `the neck and throat` | 33:4 |
| φέρω | `I brought` | `I brought, I bore, I carried, I endured` | 33:11 |
| ἀδελφός | `son of the same mother` | `son of the same mother, brother, near kinsman` | 33:9 |
| ἀμνός | `of lambs` | `of lambs` | 33:19 |
| ἀπαίρω | `having lifted off` | `having lifted off and carried off and taken away and removed from, having led away, having sailed and marched away and departed, having departed from, having set out on` | 33:12 |
| ἀπαίρω | `lifts off` | `lifts off and carries off and takes away and removes from, leads away, sails and marches away and departs, departs from, sets out on` | 33:17 |
| ἀπαντάω | `I have moved from` | `I have moved from and it stands so, I have met, I have met and encountered, I have come` | 33:8 |
| ἀποθνήσκω | `they will die off` | `they will die off and die, they will be put to death and slain` | 33:13 |
| ἁπαλός | `softer to the touch` | `softer to the touch, more tender, fresher, softer and gentler, more soft and delicate` | 33:13 |
| ἐγγίζω | `to bring near` | `to bring near, to bring up to, to draw near and approach` | 33:3 |
| ἐλεέω | `had pity on` | `had pity on and shewed mercy upon, felt pity` | 33:5, 33:11 |
| ἐνισχύω | `I will strengthen` | `I will strengthen and confirm, I will prevail in and prevail among` | 33:14 |
| ἐπιδιαιρέω | `divided anew` | `divided anew, distributed among themselves` | 33:1 |
| ἐπικαλέω | `called upon for himself` | `called upon for himself, invoked and appealed to, invited, called in as a helper or ally, called before him and summoned, challenged` | 33:20 |
| ἔσχατος | `outermost` | `outermost, furthest and uttermost and extreme, last, uppermost, lowest and deepest, innermost` | 33:2 |

### Words new in GEN 32

- The chapter is Rahlfs's, not the Hebrew's: what the Hebrew numbers 31:55 the Greek has as 32:1, and
  the Greek runs one verse ahead of the Hebrew to the end of the chapter.
- παρεμβολή — *insertion, interpolation* first, and *an encampment, fortress* second; the Hebrew is
  *maḥăneh*, the camp, and the place-name Παρεμβολαί, Rahlfs's capital and all, is Mahanaim. 32:2–32:22.
- παρεμβάλλω — the perfect participle παρεμβεβληκυῖαν, the standing state: the camp stands encamped. 32:2.
- συναντάω — *to meet face to face*, of the angels at 32:2 and of Esau at 32:18.
- ἱκανόω — *to make sufficient, qualify*; the Hebrew is *qāṭōntî*, *I am too small for all the mercies*,
  and the Greek turns it about: the mercies are made sufficient. 32:11.
- ἐξαιρέω — the middle imperative ἐξελοῦ takes the Mid., *to take out for oneself*, then *to choose for
  oneself, carry off as booty*. 32:12.
- ἅπτω — ἥψατο is the middle, whose first sense is *to fasten oneself to, cling to, hang on by, lay hold
  of, grasp, touch*. 32:26, 32:33.
- ναρκάω — *to grow stiff, numb*, of the thigh; πλάτος, *breadth, width*, of its broad part. 32:26, 32:33.
- ἐνισχύω — no Middle Liddell entry; LSJ gives *strengthen, confirm*, then *prevail in, prevail among*,
  which is the striving with God the name Ισραηλ is heard in. 32:29.
- ἐπισκάζω — no Middle Liddell entry either; LSJ has *limp upon* and cites this very verse. 32:32.
- χείμαρρος — Middle Liddell has nothing; LSJ heads the adjective χειμάρροος, *winter-flowing, swollen by
  rain and melted snow*, and as a noun *torrent*, and in the Septuagint *river* and *valley, watercourse*.
  Rahlfs prints the shortened χείμαρρος. 32:24.
- Εἶδος θεοῦ — the Greek of Peniel, and the Greek says *form of God* where the Hebrew says *face*; the
  face is kept in πρόσωπον πρὸς πρόσωπον in the same verse. 32:31, 32:32.
- κύριε ὁ εἴπας — the nominative article and participle in address beside the vocative κύριε, as the
  brief's rule has it: the nominative in address keeps its case. 32:10.
- εὖ and καλῶς stand side by side at 32:13, and both head as `well`: two Greek words, one English word,
  and only the Greek line tells them apart.
- πρῶτος — filed under πρότερος, as at 8:5, so `to the before` heads the first servant's rank. 32:18, 32:20.
- One sense each in GEN 32, and so plain text: ταῦρος `bulls`; διάστημα `an interval`; ἱκανόω; ποίμνιον
  `flock`, as at 29:2; τίς `what`, `of what`; τρίτος `to the third`; and the numerals.

| lemma | headword | chain | used |
| --- | --- | --- | --- |
| αἴξ | `goats` | `goats, wild goats and ibexes, waves` | 32:15 |
| γίνομαι | `I have come to be` | `I have come to be and it stands so, I have arisen, I have been brought into existence` | 32:11 |
| γίνομαι | `came to be` | `came to be, arose, were brought into existence` | 32:6 |
| δεύτερος | `the second` | `the second, the one coming in second, the next best, the next, the one after, the secondly and next and afterwards and a second time, the second time, the secondary, the second of two` | 32:9 |
| δεύτερος | `to the second` | `to the second, to the one coming in second, to the next best, to the next, to the one after, to the secondly and next and afterwards and a second time, to the second time, to the secondary, to the second of two` | 32:20 |
| διάβασις | `the crossing over` | `the crossing over and passage, the means and place of crossing, the ford, the bridge` | 32:23 |
| διάστημα | `an interval` | `an interval` | 32:17 |
| διαβαίνω | `I made a stride` | `I made a stride, I walked and stood with the legs apart, I stepped across and passed over, I crossed over` | 32:11 |
| διαβιβάζω | `carried over` | `carried over, carried across, transported` | 32:24 |
| δικαιοσύνη | `of righteousness` | `of righteousness and justice` | 32:11 |
| δυνατός | `strong` | `strong and mighty and able, powerful, possible, practicable` | 32:29 |
| δύναμαι | `is able` | `is able and capable and strong enough, is powerful and mighty, has influence, dares and bears, passes for, is worth, is equivalent to, signifies and means, avails` | 32:26 |
| δῶρον, with ἐν | `in the gifts` | `within, inside of, and by means of the gifts, the presents, the votive gifts, the blessings` | 32:21 |
| εὐλογέω | `you may speak well of` | `you may speak well of, you may praise, you may honour, you may bless` | 32:27 |
| εὑρίσκω | `may find` | `may find, may find out, may discover, may get and gain` | 32:6 |
| εὑρίσκω, with ἐν | `in the finding` | `within, inside of, and by means of the finding, the finding out, the discovering, the getting and gaining` | 32:20 |
| θηλάζω | `suckling` | `suckling, giving suck` | 32:16 |
| καταφιλέω | `kissed tenderly` | `kissed tenderly and caressed` | 32:1 |
| λέγω | `you will say` | `you will say, you will speak, you will declare, you will call by name, you will tell` | 32:5, 32:19, 32:21 |
| λέγω | `you will say` | `you will say, you will speak, you will declare, you will call by name, you will tell` | 32:5, 32:19, 32:21 |
| μηρός | `to the thigh` | `to the thigh, to the leg-bones` | 32:32 |
| ναρκάω | `grew stiff` | `grew stiff, grew numb` | 32:26, 32:33 |
| νεῦρον | `of the sinew` | `of the sinew and tendon, of the tendons of the feet, of the sinews and vigour, of the gut and cord made of sinew, of the cord of a sling` | 32:33 |
| νεῦρον | `the sinew` | `the sinew and tendon, the tendons of the feet, the sinews and vigour, the gut and cord made of sinew, the cord of a sling` | 32:33 |
| παλαίω | `was wrestling` | `was wrestling, was wrestling with` | 32:25 |
| παλαίω, with ἐν | `in the wrestling` | `within, inside of, and by means of the wrestling, the wrestling with` | 32:26 |
| παρέρχομαι | `went by` | `went by, went beside, went past, passed by, passed, outstripped, outwitted and escaped and eluded, arrived at, passed in, went into, passed without heeding, passed over and disregarded and slighted, overstepped and transgressed, passed unnoticed and escaped the notice of, came forward` | 32:32 |
| παραγίνομαι | `comes to be beside` | `comes to be beside, is present, arrives, comes to help` | 32:21 |
| παραπορεύομαι | `were going beside` | `were going beside, were going alongside, were going past, were passing` | 32:22 |
| παρεμβάλλω | `having put in beside` | `having put in beside and inserted and interpolated and interposed and it stands so, having insinuated, having put in line with, having fallen into line and encamped` | 32:2 |
| παρεμβολή | `an insertion` | `an insertion and interpolation, an encampment and fortress` | 32:2, 32:3, 32:9 |
| παρεμβολή | `insertions` | `insertions and interpolations, encampments and fortresses` | 32:8, 32:11 |
| παρεμβολή | `the insertion` | `the insertion and interpolation, the encampment and fortress` | 32:9 |
| παρεμβολή, with ἐν | `in the insertion` | `within, inside of, and by means of the insertion and interpolation, the encampment and fortress` | 32:22 |
| παροικέω | `I dwelt beside` | `I dwelt beside, I dwelt along the coast of, I lived near, I dwelt among, I lay near, I lived in and sojourned` | 32:5 |
| πατάσσω | `may beat` | `may beat, may knock, may strike and smite, may knock at` | 32:12 |
| πλάτος | `of the breadth` | `of the breadth and width` | 32:26, 32:33 |
| ποίμνη | `of a flock`, plain text: one translation; EXO 11 took out what the entry does not give (*of sheep* is a piece, in `NOT_SENSES`) | | 32:17 |
| προπορεύομαι | `go before` | `go before, go forward, come forward, be promoted and advance` | 32:17 |
| προπορεύομαι | `the ones going before` | `the ones going before, the ones going forward, the ones coming forward, the ones being promoted and advancing` | 32:18 |
| προπορεύομαι | `to the ones going before` | `to the ones going before, to the ones going forward, to the ones coming forward, to the ones being promoted and advancing` | 32:20, 32:21 |
| προπορεύομαι | `to the ones going before` | `to the ones going before, to the ones going forward, to the ones coming forward, to the ones being promoted and advancing` | 32:20, 32:21 |
| προσδέχομαι | `will receive favourably` | `will receive favourably and accept, will receive hospitably, will admit into, will admit to citizenship, will admit, will wait for and expect, will wait patiently` | 32:21 |
| πρῶτος | `to the before` | `to the before, to the in front and forward, to the former and sooner, to the elder, to the above and superior, to the earlier` | 32:18, 32:20 |
| πῶλος | `foals` | `foals, young horses, colts, fillies, young animals and puppies, young girls and maidens` | 32:16 |
| συναντάω | `may meet face to face` | `may meet face to face, may meet together and assemble, may meet with, may come in contact with, may befall` | 32:18 |
| συναντάω | `met face to face` | `met face to face, met together and assembled, met with, came in contact with, befell` | 32:2 |
| σῴζω | `to be saved` | `to be saved, to be kept, to be saved from death and kept alive and preserved, to be kept safe, to be kept and observed and maintained, to be kept in mind and remembered, to be brought safe to, to come safe and escape to` | 32:9 |
| σῴζω | `was saved` | `was saved and kept, was saved from death and kept alive and preserved, was kept safe, was kept and observed and maintained, was kept in mind and remembered, was brought safe to, was carried off safe and rescued from, came safe and escaped to` | 32:31 |
| τέκνον | `to the things borne` | `to the things borne, to the born, to children, to the young` | 32:12 |
| ταῦρος | `bulls` | `bulls` | 32:16 |
| φέρω | `was bringing` | `was bringing, was bearing, was carrying, was enduring` | 32:14 |
| φοβέω | `I am put to flight` | `I am put to flight, I flee affrighted, I flee, I am seized with fear, I am affrighted, I fear` | 32:12 |
| χείμαρρος | `the winter-flowing` | `the winter-flowing, the swollen by rain and melted snow, the torrent, the river, the drain and gutter, the valley and watercourse` | 32:24 |
| χρονίζω | `I spent time` | `I spent time, I took time and tarried and lingered and delayed and was slow, I remained long` | 32:5 |
| χώρα | `space in which a thing is` | `space in which a thing is, place, position and post, place in life and station, land and country, piece of land and estate and farm, country` | 32:4 |
| ἀναστρέφω | `turned upside down` | `turned upside down, upset, turned back and brought back, rallied, turned back and returned and retired, dwelt, conducted themselves, revolved, faced about` | 32:7 |
| ἀνατέλλω | `made to rise up` | `made to rise up, made to grow up, gave birth to and brought to light, rose, took its rise, grew` | 32:32 |
| ἀπορέω | `was without means` | `was without means, was without resource, was at a loss and in doubt and puzzled, was left wanting and unprovided for` | 32:8 |
| ἀποστέλλω | `I may send off` | `I may send off, I may send away and banish, I may despatch, I may go away and depart` | 32:27 |
| ἀποστέλλω | `I sent off` | `I sent off, I sent away and banished, I despatched, I went away and departed` | 32:6 |
| ἀποστέλλω | `has sent off` | `has sent off and it stands so, has sent away and banished, has despatched, has gone away and departed` | 32:19 |
| ἀποστρέφω | `having been turned` | `having been turned, having been turned back, having been turned away, having been brought back, having turned himself about` | 32:1 |
| ἄγγελος | `messengers` | `messengers and envoys, ones that announce, divine messengers and angels` | 32:4 |
| ἄνθρωπος | `man` | `a man, a human being, mankind` | 32:25 |
| ἄνθρωπος | `of men` | `of men, of human beings, of mankind` | 32:29 |
| ἅπτω | `fastened himself to` | `fastened himself to and clung to and hung on by and laid hold of and grasped and touched, engaged in and took part in, laid hold of and disputed, set upon and attacked and assailed, touched and affected, grasped with the senses and apprehended and perceived, came up to and reached and gained` | 32:26, 32:33 |
| ἐκκόπτω | `may cut out` | `may cut out and knock out, may fell and cut down all the trees, may cut off and make an end of, may beat off and repulse` | 32:9 |
| ἐνισχύω | `you strengthened` | `you strengthened and confirmed, you prevailed in and prevailed among` | 32:29 |
| ἐξαιρέω | `take out for yourself` | `take out for yourself, choose for yourself and carry off as booty, bereave of, take away from one, set free and deliver` | 32:12 |
| ἐξιλάσκομαι | `I will propitiate` | `I will propitiate` | 32:21 |
| ἐπισκάζω | `was limping upon` | `was limping upon` | 32:32 |
| ἐρωτάω | `asked` | `asked, asked about, enquired of and questioned, begged and solicited` | 32:30 |
| ἐρωτάω | `asks` | `asks, asks about, enquires of and questions, begs and solicits` | 32:18 |
| ἐρωτάω | `you ask` | `you ask, you ask about, you enquire of and question, you beg and solicit` | 32:30 |
| ἐσθίω | `may eat` | `may eat, may eat of` | 32:33 |
| ἔρχομαι | `comes` | `comes, goes, goes back and returns, is going to and intends, comes within a little of and is near` | 32:7 |
| ἔρχομαι | `we came` | `we came, we went, we went back and returned, we were going to and intended, we came within a little of and were near` | 32:7 |
| ἱκανόω | `is made sufficient` | `is made sufficient and qualified` | 32:11 |
| ἴσως | `equally` | `equally and in like manner, fairly and equitably, probably and perhaps, about` | 32:21 |
| ὄρθρος | `the day-break` | `the day-break and dawn and cock-crow` | 32:27 |
| ὑπολείπω | `was left behind` | `was left behind, was left remaining, was left in reserve` | 32:25 |
| ῥάβδος | `to the rod` | `to the rod, to the wand, to the stick, to the switch, to the magic wand, to the fishing-rod, to the limed twig, to the spear-staff and shaft, to the staff of office, to the rod for chastisement, to the stripe and strip` | 32:11 |

### Words new in GEN 31

- Rahlfs prints no verse 51: the numbering runs 50, 52, and what the Hebrew has as 51 the Greek has
  already given at 31:48. The chapter therefore has 53 verses, not 54.
- At 31:49 the printed page capitalises the article that opens the name, Ἡ ὅρασις, where the digital
  module has lower-case ἡ. The transcription follows the page, and the verse lists Ἡ in `printed`.
- δόξα — *a notion* first, and *glory, splendour* last: what Laban's sons say Jacob has made of their
  father's goods. 31:1, 31:16.
- παρακρούω — the middle takes the Mid., *to strike away from oneself, parry*, where the sense in the
  verse is the cheating of the wage. 31:7.
- ἀλλάσσω — *to make other than it is, to change, alter*. 31:7.
- ἀποκρίνω — the answering of 31:14 and the rest is the Mid.; the entry's first sense is *to separate,
  set apart*, and the form is the aorist passive, so the chain opens `having been separated`.
- εἴδωλον — *an image, a phantom*, and *an idol* last: Laban's teraphim. 31:19, 31:34, 31:35.
- κρυφῇ, ἐθισμός, κλοποφορέω, κατάβρωσις — four LSJ words, three of them cited from this chapter alone,
  and the fourth, θηριάλωτος, from Leviticus. 31:15, 31:26, 31:35, 31:39.
- αἰχμαλωτίς — Middle Liddell has the entry and tags no translation in it; LSJ gives *captive* and cites
  this verse. 31:26.
- βαρέως and ἀφρόνως — two adverbs, filed inside βαρύς and ἄφρων, whose entry glosses ἀφρόνως itself as
  *senselessly*. 31:28, 31:35.
- ὑπάρχω — *to begin, make a beginning*; the possessions of 31:18 are τὰ ὑπάρχοντα, the things beginning.
- ὁρμάω — *to set in motion, urge*, and the rushing off is its intransitive. 31:21.
- Βουνὸς τῆς μαρτυρίας and Βουνὸς μάρτυς — Laban's name and Jacob's, and where the Hebrew has one in
  Aramaic and one in Hebrew, the Greek gives both in Greek and the two languages go. Ἡ ὅρασις is Mizpah,
  the Hebrew's watch-post, translated as well. 31:47–31:49.
- ἐφοράω — Ἐπίδοι is its aorist optative, *may he oversee*; the module reads ἐπιδίδωμι, which would give
  ἐπιδοίη. 31:49.
- Three cognate constructions in the chapter: κατέφαγεν καταβρώσει, ἐπιθυμίᾳ ἐπεθύμησας, διαθώμεθα
  διαθήκην, and ἔθυσεν θυσίαν a fourth. 31:15, 31:30, 31:44, 31:54.
- ἐν πάσῃ τῇ ἰσχύι — ἐν takes the word next to it, πάσῃ, into the unit: `in all`, and then the article
  and the noun. 31:6.
- One sense each in GEN 31, and so plain text: θυγάτηρ `daughters`; υἱός `sons`; ἔτος `years`; ὀφθαλμός
  `of eyes`; ἐχθές `yesterday`; τρίτος `third`; διάλευκος `quite white`, as at 30:32.

| lemma | headword | chain | used |
| --- | --- | --- | --- |
| αἰχμαλωτίς | `captives` | `captives` | 31:26 |
| βαρέως | `heavily` | `heavily, with strength and force, grievously and oppressively` | 31:35 |
| βουνός | `a hill` | `a hill and mound` | 31:46 |
| βουνός | `of the hill` | `of the hill and mound` | 31:46 |
| βουνός | `the hill` | `the hill and mound` | 31:46, 31:48, 31:52 |
| γένεσις | `of the origin` | `of the origin and source and productive cause, of the beginning, of the manner of birth, of the race and descent, of the production and generation, of the creation and created things, of the kind and family, of the generation and age` | 31:13 |
| γίνομαι | `I was coming into being` | `I was coming to be, I was arising, I was being brought into existence` | 31:40 |
| γυνή | `of women` | `of women, of mistresses and ladies, of wives and spouses, of mortal women` | 31:35 |
| διαβαίνω | `I may make a stride` | `I may make a stride, I may walk and stand with the legs apart, I may step across and pass over, I may cross over` | 31:52 |
| διαβαίνω | `made a stride` | `made a stride, walked and stood with the legs apart, stepped across and passed over, crossed over` | 31:21 |
| διαβαίνω | `you may make a stride` | `you may make a stride, you may walk and stand with the legs apart, you may step across and pass over, you may cross over` | 31:52 |
| διατίθημι | `let us arrange as we like` | `let us arrange as we like and dispose of, let us dispose of our property and devise it by will, let us set out for sale and dispose of` | 31:44 |
| δόξα | `the notion` | `the notion, the expectation, the opinion and judgment, the mere opinion and conjecture, the fancy and vision and dream, the opinion which others have of one and the estimation and reputation and credit and honour and glory, the estimate popularly formed of a thing, the glory and splendour and effulgence` | 31:1, 31:16 |
| δύναμαι | `I am able` | `I am able and capable and strong enough, I am powerful and mighty, I have influence, I dare and bear, I pass for, I am worth, I am equivalent to, I signify and mean, I avail` | 31:35 |
| εἴδωλον | `the images` | `the images and phantoms, the unsubstantial forms, the images in the mind and ideas, the fancies, the likenesses, the idols` | 31:19, 31:34, 31:35 |
| εὐφροσύνη | `of mirth` | `of mirth and merriment, of good cheer and festivity, of glad thoughts` | 31:27 |
| εὑρίσκω | `you may find` | `you may find, you may find out, you may discover, you may get and gain` | 31:32 |
| εὔχομαι | `you prayed` | `you prayed, you offered prayers, you paid your vows, you made a vow, you prayed for` | 31:13 |
| θηριάλωτος | `caught by wild beasts` | `caught by wild beasts` | 31:39 |
| θύω | `offered` | `offered, burned, sacrificed, slaughtered and slew, offered sacrifices, celebrated with offerings` | 31:54 |
| κακία | `to badness` | `to badness in quality, to the defects, to cowardice and sloth, to moral badness and wickedness and vice, to ill-repute, to evil suffered` | 31:52 |
| κακοποιέω | `to do ill` | `to do ill and play the knave, to manage one's affairs ill, to do mischief to and maltreat` | 31:7, 31:29 |
| κατάβρωσις | `to an eating up` | `to an eating up and devouring` | 31:15 |
| καταδιώκω | `you pursued closely` | `you pursued closely` | 31:36 |
| καταφιλέω | `to kiss tenderly` | `to kiss tenderly and caress` | 31:28 |
| κατεσθίω | `I ate up` | `I ate up, I devoured` | 31:38 |
| κατεσθίω | `ate up` | `ate up, devoured` | 31:15 |
| καῦμα | `to the burning heat` | `to the burning heat, to the sun-heat, to the fever-heat` | 31:40 |
| κείρω | `to cut short` | `to cut short, to shear, to clip, to cut out and hew out, to ravage a country by cutting down the crops and fruit-trees, to destroy, to tear and eat greedily, to consume and waste` | 31:19 |
| κενός | `empty` | `empty and vain, to no purpose and in vain, void and destitute and bereft, empty-handed, empty of wit and empty-headed` | 31:42 |
| κιθάρα | `of a lyre` | `of a lyre, of a lute` | 31:27 |
| κλέμμα | `thefts` | `thefts, stratagems in war, frauds` | 31:39 |
| κλέπτω | `stole` | `stole and filched and purloined, cozened and cheated and deceived and beguiled, concealed and kept secret and disguised, did secretly and treacherously, seized and occupied secretly` | 31:19, 31:32 |
| κλέπτω | `you stole` | `you stole and filched and purloined, you cozened and cheated and deceived and beguiled, you concealed and kept secret and disguised, you did secretly and treacherously, you seized and occupied secretly` | 31:30 |
| κληρονομία | `an inheritance`, plain text: one translation; EXO 11 took out what the entry does not give (*possession of . .* is a citation's, in `NOT_SENSES`) | | 31:14 |
| κλοποφορέω | `you stole from` | `you stole from and robbed` | 31:26 |
| κρίνω | `will separate` | `will separate and part and put asunder and distinguish, will pick out and choose, will pick out for himself and choose, will decide, will judge, will adjudge, will judge of and estimate, will expound and interpret, will determine, will question, will bring to trial and accuse, will pass sentence upon and condemn` | 31:53 |
| κριός | `rams` | `rams, battering-rams` | 31:38 |
| κριός | `the rams` | `the rams, the battering-rams` | 31:10, 31:12 |
| κρυφῇ | `secretly` | `secretly, in secret` | 31:26 |
| κρύπτω | `hid` | `hid and covered and cloaked, covered in the earth and buried, concealed and kept secret` | 31:20 |
| κόπος | `the striking` | `the striking and beating, the toil and trouble and suffering, the weariness and fatigue` | 31:42 |
| λέγω | `has said` | `has said and it stands so, has spoken, has declared, has called by name, has told` | 31:16 |
| λίθος | `stones` | `stones, precious stones, marbles` | 31:46 |
| λαλέω | `you may talk` | `you may talk, you may chat, you may prattle, you may babble, you may say, you may talk of, you may speak, you may chatter, you may chirp` | 31:24, 31:29 |
| λευκός | `the light` | `the light, the bright, the brilliant, the glassy, the limpid, the clear and plain and distinct, the white, the fair` | 31:8 |
| λογίζομαι | `we have been reckoned` | `we have been reckoned and it stands so, we have been counted and calculated, we have been considered and pondered, we have been reckoned upon and expected` | 31:15 |
| μάρτυς | `a witness` | `a witness` | 31:44, 31:47 |
| μάχαιρα | `to a large knife` | `to a large knife and dirk, to a knife for cutting up, to a short sword and dagger, to a sabre and bent sword, to a rasor` | 31:26 |
| μαρτυρέω | `bears witness` | `bears witness, is a witness, gives evidence, bears testimony, bears witness to and in favour of, testifies` | 31:46, 31:48 |
| μαρτυρία | `of the witness` | `of the witness and testimony and evidence` | 31:47 |
| μερίς | `a part` | `a part and portion and share and parcel, a contribution, a part and division and class` | 31:14 |
| μηδέ | `but not` | `but not, and not, nor, not even` | 31:52 |
| μουσικός | `of musical` | `of musical and for music, of the skilled in music, of votaries of the Muses and men of letters and accomplishment and scholars` | 31:27 |
| νύξ | `of night-season` | `of night-season, of night, of the watches of the night, of the dark of night, of the night of death` | 31:39 |
| νύξ | `of the night-season` | `of the night-season, of the night, of the watches of the night, of the dark of night, of the night of death` | 31:40 |
| οἰκία, with ἐν | `in the building` | `within, inside of, and by means of the building, the house, the dwelling, the household and domestic establishment, the household and inmates of the house, the house and family from which one is descended` | 31:41 |
| οἶδα | `you know` | `you know, you are assured, you are versed in` | 31:6 |
| οὗτος | `to these` | `to these, to the nearer, to what follows` | 31:43 |
| παγετός | `to frost` | `to frost` | 31:40 |
| παιδίσκη | `of the young girls` | `of the young girls, of the young women, of the maidservants and handmaids, of the courtesans` | 31:33 |
| παρακρούω | `struck away from himself` | `struck away from himself and parried` | 31:7 |
| παραλαμβάνω | `having received from` | `having received from, having inherited, having taken upon himself and undertaken, having taken in pledge, having taken by force and treachery and got possession of, having received by hearsay and report and ascertained, having taken up and caught up, having taken to himself and associated with himself, having invited, having waited for and intercepted, having taken prisoner` | 31:23 |
| περιποιέω | `kept for himself` | `kept for himself, saved for himself, compassed and acquired and obtained, made gain` | 31:18 |
| πιπράσκω | `has sold` | `has sold and it stands so` | 31:15 |
| πλοῦτος | `the wealth` | `the wealth and riches, the treasure` | 31:16 |
| ποιέω | `has made` | `has made and it stands made, has done and it stands done, has produced and it stands produced, has created and it stands created` | 31:1 |
| ποιέω | `makes` | `makes, does, produces, creates` | 31:12 |
| ποικίλος | `the many-coloured` | `the many-coloured and spotted and mottled and pied and dappled, the wrought in various colours and broidered, the in-wrought, the intricate, the changeful and various and diversified and manifold, the complex, the subtle and wily` | 31:8 |
| πορεύομαι | `you have been driven` | `you have been driven and it stands so, you have been carried, you have gone, you have walked, you have marched, you have gone across and passed` | 31:30 |
| πράσσω | `you passed over` | `you passed over, you accomplished, you achieved and brought about and effected, you availed, you caused, you effected an object and were successful, you had to do and were busy with, you managed state-affairs, you transacted and negotiated and managed` | 31:28 |
| πρόβατον, with ἐν | `in the things that walk forward` | `within, inside of, and by means of the things that walk forward, the cattle, the flocks and herds, the horses, the small cattle, the sheep` | 31:41 |
| σάγμα | `the coverings` | `the coverings, the coverings of a shield, the large cloaks, the pack-saddles, the piles` | 31:34 |
| σκεῦος | `of the vessels` | `of the vessels, of the implements of any kind, of the furniture and house-gear and utensils and chattels, of the accoutrements and equipment, of the baggage and luggage, of the tackling, of the gear, of the inanimate objects and things, of the bodies and vessels` | 31:37 |
| συγκαίω | `being set on fire with` | `being set on fire with, being burned up at once` | 31:40 |
| συλλέγω | `collect` | `collect, gather, compile and scrape together, call together, get together` | 31:46 |
| συλλέγω | `collected` | `collected, gathered, compiled and scraped together, called together, got together` | 31:46 |
| σός | `of thy` | `of thy, of thine` | 31:32 |
| ταπεινόω | `you will lower` | `you will lower, you will lessen, you will disparage, you will humble and abase, you will make lowly and humble` | 31:50 |
| τόπος, with ἐν | `in place` | `within, inside of, and by means of place, local circumstances, position, passage in a book, topic, common-place, occasion and opportunity` | 31:13 |
| τύμπανον | `of kettledrums` | `of kettledrums, of drum-sticks, of staffs and cudgels, of wheels of solid wood` | 31:27 |
| φυλάσσω | `keep watch and ward for yourself` | `keep watch and ward for yourself and keep guard, watch and guard and keep and defend, watch for and lie in wait for, keep and maintain and cherish, observe` | 31:24, 31:29 |
| φόβος | `of the flight` | `of the flight, of the panic fear, of the fear and terror, of the outward show of fear, of the object of terror` | 31:53 |
| ἀδίκημα | `the wrong done` | `the wrong done and wrong, the wrong done to one, that which is got by wrong and the ill-gotten goods` | 31:36 |
| ἀλείφω | `you anointed with oil` | `you anointed with oil and oiled, you prepared as if for gymnastics and stimulated, you plastered, you stopped up` | 31:13 |
| ἀλλάσσω | `made other than it is` | `made other than it is and changed and altered, gave in exchange for and bartered, repaid and requited, gave up and left and quit, took one thing for another and assumed, interchanged and alternated` | 31:7 |
| ἀλλότριος | `the belonging to another` | `the belonging to another, the another man's, the unlike one's own, the forced and unnatural, the foreign and strange, the hostile` | 31:15 |
| ἀμνάς | `to ewe lambs` | `to ewe lambs` | 31:41 |
| ἀναβαίνω | `going up` | `going up, mounting, ascending, going up to, rising, coming up, coming to and arriving at, going up country, going aboard` | 31:10, 31:12 |
| ἀναγγέλλω | `to carry back tidings of` | `to carry back tidings of, to report` | 31:20 |
| ἀναγγέλλω | `you carried back tidings of` | `you carried back tidings of, you reported` | 31:27 |
| ἀναφέρω | `I have brought up` | `I have brought up and it stands so, I have carried up, I have carried up the country, I have taken with me, I have poured forth, I have heaved and uttered, I have upheld and taken upon myself, I have offered and contributed, I have led up, I have carried back and recovered, I have brought back and reported, I have traced up` | 31:39 |
| ἀξιόω | `I was thought worthy` | `I was thought worthy, I was esteemed and honoured, I was thought worthy to do, I was thought fit and expected and required and demanded, I was required` | 31:28 |
| ἀπάγω | `led away` | `led away, carried off, brought back and brought home, returned what he owed and rendered and paid, arrested and carried off, brought before a magistrate and accused, carried off to prison, led away from the subject` | 31:18 |
| ἀπάγω | `you led away` | `you led away, you carried off, you brought back and brought home, you returned what you owed and rendered and paid, you arrested and carried off, you brought before a magistrate and accused, you carried off to prison, you led away from the subject` | 31:26 |
| ἀπέρχομαι | `to go away` | `to go away, to depart from, to depart, to depart from life` | 31:18, 31:30 |
| ἀποδιδράσκω | `runs away` | `runs away and off and escapes, flees from, deserts, flees and shuns` | 31:20 |
| ἀποδιδράσκω | `you ran away` | `you ran away and off and escaped, you fled from, you deserted, you fled and shunned` | 31:26 |
| ἀποκρίνω | `having been separated` | `having been separated and set apart, having been marked by a distinctive form and distinguished, having been chosen out, having given answer to and replied, having answered charges and defended herself` | 31:14 |
| ἀποκρίνω | `having been separated` | `having been separated and set apart, having been marked by a distinctive form and distinguished, having been chosen out, having given answer to and replied, having answered charges and defended herself` | 31:31, 31:36, 31:43 |
| ἀποτίνω | `I was paying back` | `I was paying back and repaying and returning, I was paying for, I was making atonement, I was paying in full` | 31:39 |
| ἀτεκνόω | `were made childless` | `were made childless, were deprived of children` | 31:38 |
| ἀφίστημι | `was standing away` | `was standing away, was keeping aloof, was departing and withdrawing, was revolting` | 31:40 |
| ἀφίστημι | `we will stand away` | `we will stand away, we will keep aloof, we will depart and withdraw, we will revolt` | 31:49 |
| ἀφαιρέω | `took away for himself` | `took away for himself and took away, prevented and hindered from` | 31:9, 31:16 |
| ἀφαιρέω | `you may take from` | `you may take from, you may take away from, you may take off, you may remove, you may separate and set aside` | 31:31 |
| ἀφρόνως | `senselessly` | `senselessly, without sense, crazed and frantic, silly and foolish` | 31:28 |
| ἁμάρτημα | `the failure` | `the failure and fault and sin, the bodily defect and malady` | 31:36 |
| ἐγκισσάω | `were having yearnings like one pregnant` | `were having yearnings like one pregnant` | 31:10 |
| ἐθισμός | `accustoming` | `accustoming and habituation, habits, usages` | 31:35 |
| ἐλέγχω | `let them disgrace` | `let them disgrace and put to shame, let them cross-examine and question, let them censure and accuse, let them bring to the proof and disprove and confute, let them bring convincing proof, let them prove` | 31:37 |
| ἐμβάλλω | `threw in` | `threw in, put in, threw at and upon and against, inflicted, applied, made an inroad and invasion, broke and burst and rushed in, struck a ship with the ram and charged it` | 31:34 |
| ἐμός | `mine` | `mine, to me and relating to me and against me, by me` | 31:31, 31:43 |
| ἐν | `in` | `within, inside of, and by means of` | 31:18 |
| ἐξαποστέλλω | `I sent quite away` | `I sent quite away, I dispatched` | 31:27 |
| ἐπιγινώσκω | `look upon` | `look upon and witness and observe, recognise and know again, acknowledge and approve, find out and discover and detect, come to a decision and resolve and decide` | 31:32 |
| ἐπιγινώσκω | `looked upon` | `looked upon and witnessed and observed, recognised and knew again, acknowledged and approved, found out and discovered and detected, came to a decision and resolved and decided` | 31:32 |
| ἐπιθυμέω | `you set your heart upon` | `you set your heart upon, you lusted after and longed for and coveted and desired` | 31:30 |
| ἐπιθυμία | `to desire` | `to desire and yearning and longing` | 31:30 |
| ἐπικαθίζω | `set upon` | `set upon, sat upon and lighted upon` | 31:34 |
| ἐρευνάω | `sought` | `sought, searched for and searched after and tracked` | 31:33, 31:35 |
| ἐρευνάω | `you sought` | `you sought, you searched for and searched after and tracked` | 31:37 |
| ἐφοράω | `may he oversee` | `may he oversee and observe and survey, may he watch over and take notice of, may he look upon and behold` | 31:49 |
| ἕτερος | `of other` | `of other, of the other of two, of another, of second, of other than usual and different` | 31:49 |
| ἰσχύω | `is strong` | `is strong and mighty and powerful and prevails, has power and influence` | 31:29 |
| ὀργίζω | `was made angry` | `was made angry and provoked to anger and irritated, grew angry and was wroth` | 31:36 |
| ὁράω | `I have seen` | `I have seen and it stands so, I have perceived, I have beheld, I have looked at` | 31:12 |
| ὁράω | `I see` | `I see, I perceive, I behold, I look at` | 31:5 |
| ὁρμάω | `set in motion` | `set in motion, urged and pushed on and spurred on and cheered on, stirred up, made a start and hastened on, rushed headlong at, started and began` | 31:21 |
| ὅλος, with ἐν | `in whole` | `within, inside of, and by means of whole and entire, continuous and incessant` | 31:35 |
| ὑπάρχω | `the things beginning` | `the things beginning and making a beginning, the things beginning to be and coming into being and arising and springing up, the things being in existence` | 31:18 |
| ὕπνος, with ἐν | `in the sleep` | `within, inside of, and by means of the sleep, the slumber, the sleep of death, the Sleep` | 31:10 |

### Words new in GEN 30

- The naming verses carry the Hebrew wordplay in the Greek where the Greek keeps it: Δαν with ἔκρινεν,
  Νεφθαλι with συνανεστράφην, Γαδ with ἐν τύχῃ, Ασηρ with μακαρία, Ισσαχαρ with μισθός — glossed in the
  text itself, ὅ ἐστιν Μισθός — Ζαβουλων with αἱρετιεῖ, and Ιωσηφ with προσθέτω. 30:6–30:24.
- μῆλον — two entries under one spelling: μῆλον1 *a sheep or goat*, μῆλον2 the fruit. The mandrakes of
  30:14 are the second. Perseus's markup puts *an apple* inside the Latin tag it opens with, so the
  entry's first English translation is *tree-fruit*, and that is the headword. 30:14.
- θυμόω, δωρέω — filed under the actives Middle Liddell heads, as προσκαλέω at 28:1, though the forms
  here are passive and perfect middle. 30:2, 30:20.
- στερέω — *to deprive, bereave, rob of*; στερεόω, which the module has, is *to make firm*. 30:2.
- συλλαμβάνω — the middle Συνελάβετό with the dative at 30:8: Middle Liddell's Mid. is *to lay hold of*,
  and its sense V, *to take part with, assist*, is what the dative asks. The active, *to collect*, is the
  conceiving of 30:5 and the rest.
- τύχη — the first sense is *the good which man obtains*, and *fortune, chance* the third; ἐν τύχῃ takes
  the ἐν unit. 30:11.
- ἱκανός — *becoming, befitting, sufficing* first, and *sufficient, adequate, enough* second. 30:15.
- μισθόω — the perfect middle μεμίσθωμαι takes the Mid. section, *to have let to one, to hire*. 30:16.
- κοιλία — *belly*, and its chain runs through *the paunch* to *the womb*: καρπὸν κοιλίας, the fruit of
  the belly. 30:2.
- ἀφίστημι — the causal aorist ἀπέστησεν, *put away, removed*, where the corpus's ἀπέστη at 12:8 is the
  intransitive. 30:36.
- The flock-breeding words, none of them in the abridgement, all from LSJ, and all four cited from this
  chapter: ἀρήν *lamb*, διάλευκος *quite white*, ῥαντός *sprinkled*, then *speckled or spotted*,
  σποδοειδής *ashy, ash-coloured*, ἐγκισσάω *have yearnings like one pregnant*, λεπίζω *peel off the
  husk, skin or bark*, λέπισμα *peel*, καρύινος *of nuts*, *made of walnut-wood*. 30:32–30:41.
- ἀρήν and ἀμνός — two Greek words for the lamb, and one English word between them: the chains read the
  same, and only the Greek line tells them apart. 30:32, 30:40.
- στυράκινος — Middle Liddell glosses it *made of the wood of the tree στύραξ*, and `GREEK_LOST`
  restores the name the markup cuts: plain `made of the wood of the tree storax (στύραξ)`. 30:37.
- κλέπτω and πληρόω — two perfect passives, κεκλεμμένον and πεπλήρωνται, each a standing state. 29:21, 30:33.
- οὐθείς — the later spelling of οὐδείς, which the lexicon files it under. 30:31.
- ἐνώπιον — the preposition, as at 11:28, and plain text there: `face to face of`. 30:33, 30:38.
- One sense each in GEN 30, so plain text: υἱός `of the son`; ἀδελφή `the sister`; γόνυ `of the knees`;
  πυρός `of wheat`; μανδραγόρας `the mandrakes`; τεκνοποιέω `I will bear children`; σήμερον `to-day`;
  ἐμαυτοῦ `for myself`; ἑαυτοῦ `for himself`; ποτιστήριον `drinking-troughs for cattle`, as at 24:20.

| lemma | headword | chain | used |
| --- | --- | --- | --- |
| αἱρετίζω | `will choose` | `will choose and select` | 30:20 |
| αἴξ | `the goats` | `the goats, the wild goats and the ibexes, the waves` | 30:35 |
| αἴξ, with ἐν | `in the goats` | `within, inside of, and by means of the goats, the wild goats and the ibexes, the waves` | 30:32, 30:33 |
| αὐξάνω | `was made large` | `was made large and increased and augmented, was increased in power and strengthened and exalted and aggrandised, was promoted to honour and glorified and magnified, grew and waxed and increased, grew up` | 30:30 |
| αὔριον | `to-morrow` | `to-morrow, on the morrow` | 30:33 |
| δίδωμι | `I gave` | `I gave, I granted, I provided, I gave over and delivered up` | 30:18 |
| διαστέλλω | `set apart` | `set apart, drew asunder and tore apart, distinguished and determined, ordered and commanded` | 30:28, 30:35, 30:40 |
| διαχωρίζω | `separate`, plain text: one translation; EXO 11 took out what the entry does not give, as at GEN 13 (*part asunder, set apart* were LSJ's) | | 30:32, 30:40 |
| δικαιοσύνη | `the righteousness` | `the righteousness and justice` | 30:33 |
| δουλεία | `the servitude` | `the servitude and slavery and bondage, the slaves and the slave-class` | 30:26 |
| δουλεύω | `I have been a slave` | `I have been a slave and stand so, I have served and been subject to` | 30:26, 30:29 |
| δωρέω | `has given` | `has given and it stands so, has presented and stands so` | 30:20 |
| δύναμαι | `I was able` | `I was able and capable and strong enough, I dared and bore, I passed for, I was worth, I was equivalent to, I signified and meant` | 30:8 |
| δῶρον | `gift` | `gift, present, votive gift, blessing` | 30:20 |
| εἴσοδος | `to the way in` | `to the way in and entrance, to the place of entrance and entry, to the right and privilege of entrance` | 30:27 |
| ζηλόω | `was jealous of` | `was jealous of, envied, vied with and emulated and rivalled, was zealous after and strove after` | 30:1 |
| θερισμός | `of reaping-time` | `of reaping-time, of harvest, of the crop` | 30:14 |
| θυμόομαι | `was wroth` | `was wroth, was angry, was wild and restive, vented fury, was angry with, was angry at` | 30:2 |
| καρύινος | `of nuts` | `of nuts, made of walnut-wood` | 30:37 |
| κλέπτω | `having been stolen` | `having been stolen and filched and purloined and standing so, having been cozened and cheated and deceived and beguiled, having been concealed and kept secret and disguised, having been done secretly and treacherously, having been seized and occupied secretly` | 30:33 |
| κοιλία | `of belly` | `of belly, of the paunch, of the paunch stuffed with mince-meat and black-pudding and sausage, of the womb` | 30:2 |
| κοιμάω | `let him be lulled` | `let him be lulled, let him be hushed to sleep and put to sleep, let him be lulled to rest and stilled and calmed, let him fall asleep, let him go abed and lie abed, let him sleep, let him fall asleep and die, let him keep watch at night` | 30:15 |
| κρίνω | `separated` | `separated and parted and put asunder and distinguished, picked out and chose, picked out for himself and chose, decided, judged, adjudged, judged of and estimated, expounded and interpreted, determined, questioned, brought to trial and accused, passed sentence upon and condemned` | 30:6 |
| κριός | `a ram` | `a ram, a battering-ram` | 30:40 |
| λαμβάνω | `taking` | `taking, receiving, taking hold of and grasping and seizing` | 30:41 |
| λεπίζω | `peeled off the husk` | `peeled off the husk, peeled off the skin and bark, stripped an object of its covering of metal plates` | 30:37, 30:38 |
| λευκός | `light` | `light, bright, brilliant, glassy, limpid, clear and plain and distinct, white, fair` | 30:35, 30:37 |
| ληνός, with ἐν | `in the troughs` | `within, inside of, and by means of the troughs, the wine-vats` | 30:38, 30:41 |
| μίγνυμι | `mixed` | `mixed, mixed up, mingled, joined and brought together` | 30:40 |
| μακάριος | `blessed` | `blessed and happy` | 30:13 |
| μακαρίζω | `they bless` | `they bless, they deem happy, they pronounce happy` | 30:13 |
| μισθός | `wages` | `wages and pay and hire, recompense and reward, payment and requital` | 30:32 |
| μισθόω | `I have had let to me` | `I have had let to me and it stands so, I have hired and it stands so, I have engaged for pay` | 30:16 |
| μῆλον | `tree-fruits` | `tree-fruits, girls' breasts, the cheeks` | 30:14 |
| οἰωνίζομαι | `I took omens from the flight and cries of birds` | `I took omens from the flight and cries of birds, I divined from omens and augured` | 30:27 |
| οὐθείς | `and not one` | `and not one, no one and none, naught and good for naught` | 30:31 |
| πέμπτος | `fifth` | `fifth, one with four others, a fifth part` | 30:17 |
| πίνω | `to drink` | `to drink, to drink of, to drink up` | 30:38 |
| παρέρχομαι | `let it go by` | `let it go by, let it go beside, let it go past, let it pass by, let it pass, let it outstrip, let it outwit and escape and elude, let it arrive at, let it pass in, let it go into, let it pass without heeding, let it pass over and disregard and slight, let it overstep and transgress, let it pass unnoticed and escape the notice of, let it come forward` | 30:32 |
| παρατίθημι | `set beside` | `set beside, placed before, gave in charge and entrusted, deposited` | 30:38 |
| περισύρω | `dragging about` | `dragging about, tearing away from` | 30:37 |
| πλάτανος | `of the oriental plane` | `of the oriental plane` | 30:37 |
| πλουτέω | `was rich` | `was rich, was wealthy, was rich in` | 30:43 |
| ποικίλος | `many-coloured` | `many-coloured and spotted and mottled and pied and dappled, wrought in various colours and broidered, in-wrought, intricate, changeful and various and diversified and manifold, complex, subtle and wily` | 30:37, 30:39, 30:40 |
| ποιμαίνω | `I will be shepherd` | `I will be shepherd, I will tend, I will roam the pastures, I will tend and cherish and mind` | 30:31 |
| ποιμαίνω | `was shepherd` | `was shepherd, was tending, was roaming the pastures, was tending and cherishing and minding` | 30:36 |
| προστίθημι | `let him put to` | `let him put to, let him hand over and deliver, let him give and bestow, let him impose further, let him attribute, let him add` | 30:24 |
| πότε | `when` | `when, at what time` | 30:30 |
| σποδοειδής | `ashy` | `ashy and ash-coloured` | 30:39 |
| στερέω | `deprived` | `deprived, bereaved, robbed of, took away` | 30:2 |
| στυράκινος | plain | `made of the wood of the tree storax (στύραξ)` | 30:37 |
| συλλαμβάνω | `laid hold of for himself` | `laid hold of for himself, seized for himself, took part with and assisted` | 30:8 |
| συναναστρέφω | `was turned back together` | `was turned back together, lived along with` | 30:8 |
| τίθημι | `was setting` | `was setting, was putting, was placing, was planting, was laying` | 30:42 |
| τίκτω | `were bringing into the world` | `were bringing into the world, were bearing, were bringing forth, were begetting, were producing and yielding` | 30:39 |
| τίκτω | `will bring into the world` | `will bring into the world, will bear, will bring forth, will beget, will produce and yield` | 30:3 |
| τελευτάω | `I will finish` | `I will finish, I will accomplish, I will end my life and die, I will end and come to an end` | 30:1 |
| τράγος | plain | `the he-goats` | 30:35 |
| τύχη, with ἐν | `in the good which man obtains` | `within, inside of, and by means of the good which man obtains, the favour of the gods and good fortune and luck and success, fortune and chance, ill fortune` | 30:11 |
| φαίνω | `was being brought to light` | `was being brought to light and made to appear, was showing itself, was appearing, was coming to light and being seen, was shining` | 30:37 |
| φαιός | `dusky` | `dusky and dun and gray` | 30:32, 30:33, 30:35 |
| φυλάσσω | `I will keep watch and ward` | `I will keep watch and ward and keep guard, I will watch and guard and keep and defend, I will watch for and lie in wait for, I will keep and maintain and cherish, I will observe` | 30:31 |
| ἀμνός | `the lambs` | `the lambs` | 30:40 |
| ἀμνός, with ἐν | `in the lambs` | `within, inside of, and by means of the lambs` | 30:32, 30:33, 30:35, 30:40 |
| ἀποστέλλω | `send off` | `send off, send away and banish, despatch, go away and depart` | 30:25 |
| ἀρήν, with ἐν | `in the lambs` | `within, inside of, and by means of the lambs, the sheep, the rams, the ewes` | 30:32, 30:33, 30:35, 30:40 |
| ἀφίστημι | `put away` | `put away and removed, hindered from, frustrated, deposed, made to revolt and moved to revolt, weighed out` | 30:36 |
| ἀφαιρέω | `took from` | `took from, took away from, took off, removed, separated and set aside` | 30:23 |
| ἄνθρωπος | `the man` | `the man, the human being, mankind` | 30:43 |
| ἄσημος | `the without mark` | `the without mark, the uncoined, the without device, the giving no sign and unintelligible` | 30:42 |
| ἐγκισσάω | `had yearnings like one pregnant` | `had yearnings like one pregnant` | 30:41 |
| ἐγκισσάω | `may have yearnings like one pregnant` | `may have yearnings like one pregnant` | 30:39 |
| ἐγκισσάω | `to have yearnings like one pregnant` | `to have yearnings like one pregnant` | 30:41 |
| ἐπίσημος | `the having a mark on` | `the having a mark on, the stamped and coined, the notable and remarkable` | 30:42 |
| ἐπακούω | `will listen` | `will listen, will hearken to and hear, will give ear and hearken, will obey` | 30:33 |
| ἔρχομαι | `may come` | `may come, may go, may go back and return, may be going to and intend, may come within a little of and be near` | 30:38 |
| ἕκτος | `sixth` | `sixth` | 30:19 |
| ἡμέρα, with ἐν | `in days` | `within, inside of, and by means of days, day-breaks, times` | 30:14 |
| ἱκανός | `becoming` | `becoming and befitting and sufficing, sufficient and competent, sufficient and adequate and enough, large enough, considerable and long, satisfactory` | 30:15 |
| ὁδός | `way` | `way, path, track, road, highway, course, journey, manner and method` | 30:36 |
| ὄνειδος | `the reproach` | `the reproach and censure and blame, the disgrace, the matter of reproach` | 30:23 |
| ὑπολείπω | `the ones having been left behind` | `the ones having been left behind, the ones having been left remaining, the ones having been left in reserve` | 30:36 |
| ῥάβδος | `a rod` | `a rod, a wand, a stick, a switch, a magic wand, a fishing-rod, a limed twig, a spear-staff and shaft, a staff of office, a rod for chastisement, a stripe and strip` | 30:37, 30:38, 30:39, 30:41 |
| ῥαντός | `sprinkled` | `sprinkled, speckled or spotted` | 30:32, 30:33, 30:35, 30:39 |

### Words new in GEN 29

- ἐξαίρω — Middle Liddell heads the entry with the Epic ἐξαείρω, *to lift up, lift off the earth*: the
  Hebrew idiom *he lifted his feet* carried over word for word. 29:1.
- ποίμνιον — one sense, *a flock*; Middle Liddell's second, of disciples, glosses nothing. 29:2, 29:3.
- ἀναπαύω — the middle participle takes the Mid. and Pass. section: *desisting from, taking one's rest
  and sleeping, regaining strength*. 29:2.
- συνάγω — first *to bring together, gather together, collect, convene*; the senses of joining battle
  and matching two warriors are of the active in one idiom only, and are left out. 29:3, 29:7, 29:8, 29:22.
- πόθεν — *whence?*, the interrogative adverb. 29:4.
- ὑγιαίνω — *to be sound, healthy*, for the Hebrew's *is there peace to him*. 29:6.
- ὥρα — the entry opens with *period*, whether of the year, month or day, and *a part of the year, a
  season* is its first numbered sense; so the headword is `period`, where the sense here is the hour. 29:7.
- κτῆνος — the plural is *flocks and herds*; *a single beast* is the singular's sense, and stays out of
  a plural's chain. 29:7.
- δύναμαι — *to be able, capable, strong enough*, and then *to pass for, be worth, be equivalent to,
  signify and mean*. 29:8.
- περί with the genitive — the first sense for that case, *round about, around*, though the sense here
  is *for*, the price of the service. 29:18, 29:20, 29:25.
- δωρεάν — no entry of its own: the accusative of δωρεά used as an adverb, *as a free gift, freely*, and
  so filed inside the noun, as ταχύ inside ταχύς at 27:20. 29:15.
- μείζων, νεώτερος, πρεσβύτερος — three comparatives: Middle Liddell heads the first two under μέγας and
  νέος, and πρεσβύτερος has an entry of its own, as at 27:1. 29:16–29:26.
- ἀσθενής — the Hebrew is *rakkôt*, *tender*; the Greek is *without strength, weak, feeble*. 29:17.
- ὡραῖος — *produced at the right season, seasonable, timely*; *beautiful* is the last sense of the
  last, where καλή before it is the adjective's first. 29:17.
- βελτίων — the irregular comparative of ἀγαθός, with its own entry, which translates it *better* and
  then cross-refers to a verb. 29:19.
- πληρόω — the perfect passive πεπλήρωνται, the standing state: the days stand full. 29:21.
- ἐργάζομαι — ἐργᾷ is the future middle, as at 4:12, not the present. 29:27.
- μισέω — one sense, *to hate*, with the passive *to be hated*: both forms of it here are passive. 29:31, 29:33.
- ἐξομολογέω — Middle Liddell heads the deponent ἐξομολογέομαι, *to confess in full*, then *to make full
  acknowledgments, give thanks*, which is what the name Ιουδα is heard in. 29:35.
- ἵστημι — ἔστη τοῦ τίκτειν takes 23:17's intransitive chain, `was set`, with the articular infinitive. 29:35.
- Ρουβην, Συμεων, Λευι, Ιουδα — each name is glossed with the Hebrew wordplay the Greek keeps: εἶδεν …
  τὴν ταπείνωσιν, ἤκουσεν, and ἐξομολογήσομαι. Λευι's *he will be joined* the Greek does not carry. 29:32–29:35.
- One sense each in GEN 29, and so plain text: υἱός `the son`; θυγάτηρ `the daughter`; ἀδελφή `of the
  sister`; ὀφθαλμός `eyes`; συνάντησις `a meeting`; ἔτος `years`; μήν `month`; and the numerals δύο, ἑπτά,
  τρεῖς. ἀποκυλίω `rolled away` and προσδίδωμι `gave besides` have one sense each and stay units.

| lemma | headword | chain | used |
| --- | --- | --- | --- |
| βελτίων | `better` | `better` | 29:19 |
| βοάω | `having cried aloud` | `having cried aloud, having shouted, having sounded and resounded and roared and howled, having called to one and called on, having called for and shouted out for, having noised abroad, having commanded in a loud voice` | 29:11 |
| βόσκω | `feed` | `feed, tend, nourish and support, maintain, feed up` | 29:7 |
| βόσκω | `was feeding` | `was feeding, was tending, was nourishing and supporting, was maintaining, was feeding up` | 29:9 |
| γάμος | `a wedding` | `a wedding and wedding-feast, marriage and wedlock, marriage with` | 29:22 |
| γινώσκω | `we learn to know` | `we learn to know, we perceive, we mark, we learn, we discern and distinguish` | 29:5 |
| γινώσκω | `you learn to know` | `you learn to know, you perceive, you mark, you learn, you discern and distinguish` | 29:5 |
| δουλεύω | `I was a slave` | `I was a slave, I served and was subject to` | 29:25 |
| δουλεύω | `I will be a slave` | `I will be a slave, I will serve and be subject to` | 29:18 |
| δουλεύω | `was a slave` | `was a slave, served and was subject to` | 29:20, 29:30 |
| δωρεά | `as a free gift` | `as a free gift and freely, to no purpose and in vain` | 29:15 |
| δύναμαι | `we will be able` | `we will be able and capable and strong enough, we will be powerful and mighty, we will have influence, we will dare and bear, we will pass for, we will be worth, we will be equivalent to, we will signify and mean, we will avail` | 29:8 |
| εἰσέρχομαι | `I may go in` | `I may go in, I may go into and enter, I may come into, I may come in, I may come upon` | 29:21 |
| εἶδος | `to that which is seen` | `to that which is seen, to the form, to the shape, to the figure, to the sort and particular kind and nature, to the particular state and course, to the class and kind and sort` | 29:17 |
| κτῆνος | `the flocks and herds` | `the flocks and herds, the single beasts, the beasts for riding` | 29:7 |
| μέγας | `to the bigger` | `to the bigger, to the greater, to the taller, to the vaster, to the stronger and mightier, to the weightier and more important` | 29:16 |
| μήτρα | `the womb` | `the womb, the cervix including the orifice of the womb, the matrix, the source and origin, the core and heart-wood, the diseased condition, the queen-wasp` | 29:31 |
| μισέω | `I am hated` | `I am hated` | 29:33 |
| μισέω | `is hated` | `is hated` | 29:31 |
| νέος | `of the younger` | `of the younger, of the more youthful, of the newer and fresher, of the stranger` | 29:18 |
| νέος | `to the younger` | `to the younger, to the more youthful, to the newer and fresher, to the stranger` | 29:16 |
| οἰκέω | `inhabit` | `inhabit, occupy, dwell and live, be settled` | 29:19 |
| παραλογίζομαι | `you misreckoned` | `you misreckoned and miscalculated, you cheated out, you defrauded of, you misled by fallacious reasoning` | 29:25 |
| περί | `round about` | `round about, around, about and near, about and for and on account of, about and concerning, about and as to` | 29:18, 29:20, 29:25 |
| περιλαμβάνω | `having seized around` | `having seized around and embraced, having encompassed and surrounded, having intercepted, having got hold of and caught, having comprehended and included` | 29:13 |
| πληρόω | `have been made full` | `have been made full and stand so, have been filled full, have been gorged and satiated, have been manned, have been made complete, have been fulfilled and paid in full and made up` | 29:21 |
| ποιμήν | `the herdsmen` | `the herdsmen, the shepherds, the captains and chiefs` | 29:8 |
| ποτίζω | `having given to drink` | `having given to drink, having watered, having watered the cattle` | 29:7 |
| ποτίζω | `we will give to drink` | `we will give to drink, we will water, we will water the cattle` | 29:8 |
| ποτίζω | `were giving to drink` | `were giving to drink, were watering, were watering the cattle` | 29:2, 29:3 |
| πρεσβύτερος | `the elder` | `the elder, the older, the higher and more important, the greater than, the elder of the Jewish Council, the elder of the Church and presbyter` | 29:26 |
| προσέρχομαι | `having come to` | `having come to, having gone to, having visited, having approached and drawn nigh and been nigh at hand, having come in and surrendered and capitulated, having come forward to speak, having associated with, having come in` | 29:10 |
| προσδίδωμι | `gave besides` | `gave besides` | 29:33 |
| πρόβατον | `of the things that walk forward` | `of the things that walk forward, of the cattle, of the flocks and herds, of the horses, of the small cattle, of the sheep` | 29:6, 29:9 |
| πόθεν | `whence` | `whence, from what source, whence and wherefore` | 29:4 |
| συνάγω | `brought together` | `brought together, gathered together, collected, convened, joined in one and united, received into his house, drew together and narrowed and contracted, concluded and inferred` | 29:22 |
| συνάγω | `to be brought together` | `to be brought together, to be gathered together, to be collected, to be convened, to be joined in one and united, to be received into a house, to be drawn together and narrowed and contracted, to be concluded and inferred` | 29:7, 29:8 |
| συνάγω | `were being brought together` | `were being brought together, were being gathered together, were being collected, were being convened, were being joined in one and united, were being received into a house, were being drawn together and narrowed and contracted, were being concluded and inferred` | 29:3 |
| συντελέω | `bring quite to an end` | `bring quite to an end and complete and accomplish, make up the whole and the number, pay towards common expenses and contribute, belong to a class and be counted in it` | 29:27 |
| ταπείνωσις | `the humiliation` | `the humiliation and abasement and defeat, the low estate and low condition` | 29:32 |
| φωνή | `to the sound` | `to the sound and tone, to the sound of the voice, to the cry, to the faculty of speech and discourse, to the language, to the saying` | 29:11 |
| ἀγαπάω | `to treat with affection` | `to treat with affection, to caress, to love, to be fond of, to regard with brotherly love, to be well pleased and contented with, to be content` | 29:20 |
| ἀγαπάω | `will treat with affection` | `will treat with affection and caress and love and be fond of, will regard with brotherly love, will be well pleased and contented with, will be content` | 29:32 |
| ἀναπαύω | `desisting from` | `desisting from, taking their rest and sleeping, halting and resting, regaining strength` | 29:2 |
| ἀναπληρόω | `filled up` | `filled up, made up and supplied, filled, paid in full` | 29:28 |
| ἀνοίγω | `opened` | `opened, undid and opened, laid open and unfolded and disclosed, got into the open sea and got clear of land` | 29:31 |
| ἀπαγγέλλω | `bring tidings` | `bring tidings, report, announce, carry a report, relate and narrate` | 29:15 |
| ἀπαγγέλλω | `brought tidings` | `brought tidings, reported, announced, carried a report, related and narrated` | 29:12 |
| ἀποκαθίστημι | `were re-establishing` | `were re-establishing and restoring and reinstating` | 29:3 |
| ἀποκυλίω | `may roll away` | `may roll away` | 29:8 |
| ἀποκυλίω | `rolled away` | `rolled away` | 29:10 |
| ἀποκυλίω | `were rolling away` | `were rolling away` | 29:3 |
| ἀσθενής | `without strength` | `without strength and weak and feeble and weakly, weak and poor, insignificant, petty and small` | 29:17 |
| ἐξαίρω | `having lifted up` | `having lifted up and lifted off the earth, having raised in dignity and exalted, having raised and aroused and stirred up, having carried off for himself and earned and won and gained, having taken on himself` | 29:1 |
| ἐξομολογέω | `I will confess in full` | `I will confess in full, I will make full acknowledgments and give thanks, I will agree and promise` | 29:35 |
| ἐργάζομαι | `you will work` | `you will work, you will labour, you will work at and make and build, you will do and perform and accomplish, you will work the land, you will earn by working` | 29:27 |
| ἐργασία | `of the work` | `of the work and daily labour and business, of a working at and making and building, of a working of a material, of the trade and commerce, of the practising and exercising, of the work of art and production` | 29:27 |
| ἔρχομαι | `was coming` | `was coming, was going, was going back and returning, was going to and intending, was coming within a little of and being near` | 29:6, 29:9 |
| ἕβδομος | `the sevenths` | `the sevenths, the seventh days` | 29:27, 29:28 |
| ὀλίγος | `few` | `few, little, scanty, small, too few, little and small` | 29:20 |
| ὀστέον | `of the bones` | `of the bones, of the bones of the dead` | 29:14 |
| ὁράω | `sees` | `sees, perceives, beholds, looks at` | 29:2 |
| ὑγιαίνω | `is sound` | `is sound and healthy, is in health, is sound of mind` | 29:6 |
| ὡραῖος | `produced at the right season` | `produced at the right season, seasonable, timely, happening in season and done in due season, due and proper, ripe, in the bloom of youth and blooming, beautiful` | 29:17 |
| ὥρα | `period` | `period, a part of the year and a season, the seasons, the prime of the year and springtime, the year, the quarters of the heavens, a part of the day, the times of day` | 29:7 |

### Words new in GEN 28

- προσκαλέω — the middle προσκαλεσάμενος takes the Mid. section: *to call to oneself, call to one, call
  to one's aid*, and *to cite* before a court. 28:1.
- συναγωγή — first *a bringing together, uniting*; *a place of assembly, a synagogue* is the third sense,
  so the nations Jacob is to become are `bringings together`. 28:3.
- παροίκησις — one sense, *a neighbourhood*: the land lived beside rather than owned. 28:4.
- ἀπαντάω — Middle Liddell opens with *to move from*, and *to meet* follows; with the dative here. 28:11.
- δύω — the entry is *causal in fut. and aor1, to strip off*; the second aorist ἔδυ is not, and leaves it out (`FORM_SENSES`, settled at EXO 15:10): *entered* heads. 28:11.
- κεφαλή — πρὸς κεφαλῆς, with no article in the Greek, so `of head` without one. 28:11, 28:18.
- ἐνυπνιάζομαι — no Middle Liddell entry; LSJ gives *dream*, and that one sense is the whole chain. 28:12.
- κλίμαξ — Middle Liddell heads the entry κλῖμαξ; Rahlfs's spelling is kept. 28:12.
- στηρίζω and ἐπιστηρίζω — the perfect participle ἐστηριγμένη and the pluperfect ἐπεστήρικτο, each the
  standing state: `having been made fast and standing so`, `had been made to lean on and stood so`. 28:12, 28:13.
- ἄκρον — the noun, *the mountain-top*, as MorphGNT codes τὸ ἄκρον, not the adjective ἄκρος. 28:18.
- βορρᾶς — the contracted form the text prints, not βορέας; two senses, *north wind* and *the north*. 28:14.
- φυλή — the tribes of 10:18, where 22:18 has ἔθνη, τὰ ἔθνη. 28:14.
- ὡς — exclamatory here, *how fearful*; the unit is `as`, the adverb's first translation, since Middle
  Liddell gives the exclamation no separate gloss. 28:17.
- θεοῦ without the article keeps 1:2's `of everything that God is by nature, of deity in full and undiminished kind`, and θεόν 17:7's qualitative
  chain; Οἶκος θεοῦ, the Greek of Bêt-ʾĒl, is printed as a name with Rahlfs's capital. 28:17, 28:19, 28:21, 28:22.
- πύλη — the chain of 19:1, `the one wing of a pair of double gates`. 28:17.
- Two cognate accusatives: ηὔξατο εὐχήν, εὔχομαι with εὐχή, and δεκάτην ἀποδεκατώσω, as at 14:20. Each is
  kept word for word. 28:20, 28:22.
- One sense each, and so a chain of one word, as κατάρα at 27:12: παροίκησις, ἐνυπνιάζομαι, ἔλαιον,
  δεκάτη. υἱός stays plain text, `the son`, as before. 28:5, 28:9.

| lemma | headword | chain | used |
| --- | --- | --- | --- |
| αὐξάνω | `may he make large` | `may he make large and increase and augment, may he increase in power and strengthen and exalt and aggrandise, may he promote to honour and glorify and magnify, may he grow and wax and increase, may he grow up` | 28:3 |
| βορρᾶς | `north wind` | `north wind, the north, northward` | 28:14 |
| δίδωμι | `may give` | `may give, may grant, may provide, may give over and deliver up` | 28:20 |
| δίδωμι | `you may give` | `you may give, you may grant, you may provide, you may give over and deliver up` | 28:22 |
| δεκάτη | `a tenth` | `a tenth, a tenth part and tithe, a tenth day` | 28:22 |
| διαφυλάσσω | `may watch closely` | `may watch closely and guard carefully, may observe closely, may observe and maintain, may guard against` | 28:20 |
| διαφυλάσσω | `watching closely` | `watching closely and guarding carefully, observing closely, observing and maintaining, guarding against` | 28:15 |
| δύω | `entered` | `entered and made one's way into, sank into, set, got into and put on, entered and came over and upon` | 28:11 |
| εἰμί | `may be` | `may be` | 28:20 |
| εὐλογέω | `may he speak well of` | `may he speak well of, may he praise, may he honour, may he bless` | 28:3 |
| εὐλογέω, with ἐν τῷ | `in the speaking well of` | `within, inside of, and by means of the speaking well of, the praising, the honouring, the blessing` | 28:6 |
| εὐχή | `prayer` | `prayer, vow, a mere wish and an aspiration, a prayer for evil, an imprecation` | 28:20 |
| εὔχομαι | `prayed` | `prayed, offered prayers, paid his vows, made a vow, prayed for` | 28:20 |
| καθεύδω | `you lie down to sleep` | `you lie down to sleep and sleep, you lie asleep and lie idle, you sleep and lie still and are at rest` | 28:13 |
| καταβαίνω | `were stepping down` | `were stepping down, were going and coming down, were going down from, were dismounting, were coming down stairs, were going down from the inland parts to the sea, were coming to land and getting safe ashore, were going down into the arena, were coming down from the tribune, were coming to, were ending` | 28:12 |
| κεφαλή | `of head` | `of head, of the life, of the top, of the brim, of the coping, of the source, of the crown and completion` | 28:11, 28:18 |
| κλίμαξ | `ladder` | `ladder, stairs, scaling-ladder` | 28:12 |
| λίθος | `of the stones` | `of the stones, of the precious stones, of the marbles` | 28:11 |
| λαλέω | `I talked` | `I talked, I chatted, I prattled, I babbled, I said, I talked of, I spoke, I chattered, I chirped` | 28:15 |
| παροίκησις | `of the neighbourhood` | `of the neighbourhood` | 28:4 |
| περιβάλλω | `to throw round oneself` | `to throw round oneself, to put on, to throw round oneself for defence, to build round, to surround and enclose for oneself, to bring into one's power and aim at, to cloke and veil` | 28:20 |
| πλατύνω | `will be made broad` | `will be made broad, will be widened, will be enlarged` | 28:14 |
| πληθύνω | `may he make full` | `may he make full and increase and multiply` | 28:3 |
| πορεύομαι | `you may be driven` | `you may be driven, you may be carried, you may go, you may walk, you may march, you may go across and pass` | 28:15 |
| προσκαλέω | `having called to himself` | `having called to himself, having called to one, having called to his aid, having cited` | 28:1 |
| στήλη | `block of stone` | `block of stone, prop and buttress to a wall, slab, gravestone, record and contract and agreement, turning-post` | 28:18, 28:22 |
| στηρίζω | `having been made fast` | `having been made fast and propped and fixed and set and standing so, having been confirmed and established and standing so, having been fixed and settled and determined and standing so, having been firmly set and fixed and standing fast and steady and standing so` | 28:12 |
| συναγωγή | `bringings together` | `bringings together and unitings, places of assembly and synagogues, drawings together and contractings, formings in column, pursings up, wrinklings, collections, conclusions and inferences` | 28:3 |
| φοβερός | `fearful` | `fearful, causing fear and dreadful and terrible, matter for fear and regarded with fear` | 28:17 |
| ἀναβαίνω | `were going up` | `were going up, were mounting, were ascending, were going up to, were rising, were coming up, were coming to and arriving at, were going up country, were going aboard` | 28:12 |
| ἀπαντάω | `moved from` | `moved from, met, met and encountered, came` | 28:11 |
| ἀποίχομαι | `was gone away` | `was gone away, was absent and away, had departed` | 28:6 |
| ἀποδεκατόω | `I will tithe` | `I will tithe and pay tithes of, I will take tithe` | 28:22 |
| ἀποστρέφω | `I will turn` | `I will turn, I will turn back, I will turn away, I will turn myself about, I will bring back` | 28:15 |
| ἀποστρέφω | `may turn` | `may turn, may turn back, may turn away, may turn himself about, may bring back` | 28:21 |
| ἀφικνέομαι | `was coming to` | `was coming to, was arriving at and reaching, was arriving` | 28:12 |
| ἄκρον | `the mountain-top` | `the mountain-top and peak, the headland and foreland and cape, the end and extremity, the highest pitch and height, the exceedingly, the highest place, the prize, the oldest rulers` | 28:18 |
| ἐγκαταλείπω | `I may leave behind` | `I may leave behind, I may leave in the lurch, I may leave out and omit` | 28:15 |
| ἐνυπνιάζομαι | `dreamed` | `dreamed` | 28:12 |
| ἐξεγείρω | `was awakened` | `was awakened, was awaked and woke up, was raised from the dead, was aroused and brought on` | 28:16 |
| ἐπιστηρίζω | `had been made to lean on` | `had been made to lean on and stood so, had leaned upon` | 28:13 |
| ἐπιχέω | `poured water over` | `poured water over, poured` | 28:18 |
| ἔλαιον | `olive-oil` | `olive-oil` | 28:18 |
| ἱμάτιον | `outer garment` | `outer garment, cloak and mantle, Roman toga, clothes, cloth` | 28:20 |
| ἵστημι | `I made to stand` | `I made to stand, I set, I stopped and stayed and checked, I set up and raised, I established and instituted, I appointed, I weighed` | 28:22 |
| ὑποτίθημι | `placed under` | `placed under, placed under one's feet, placed under as a foundation, suggested and advised, set before, pledged and mortgaged` | 28:18 |
| ὕπνος | `of the sleep` | `of the sleep, of the slumber, of the sleep of death, of the Sleep` | 28:16 |

### Words new in GEN 27

- φιλέω — one verb for both the loving of food and the kiss: *to love, regard with affection*, and so
  `love` where the Hebrew has *kiss*. 27:4, 27:9, 27:14, 27:26, 27:27.
- εὐλογία — first *good language*, then *fine language*, *a fair speech*, *eulogy*, and *blessing*
  last: the blessing of the chapter is the lexicon's fifth sense. 27:12–41.
- κατάρα — one sense, *a curse*, against εὐλογία's five. 27:12, 27:13.
- ἔδεσμα — *meat*, in the plural throughout. 27:4–31.
- τε — `both`, as at 2:25, where the enclitic pairs two nouns. 27:3, 27:36.
- ἐξέστη … ἔκστασιν μεγάλην and ἀνεβόησεν φωνὴν μεγάλην — cognate accusatives, each kept word for
  word: ἐξίστημι with ἔκστασις, ἀναβοάω with φωνή. 27:33, 27:34, 27:38.
- πτερνίζω — no Middle Liddell entry; LSJ's *strike with the heel*, *trip up, supplant*, which is the
  heel of 25:26 heard again in the name. 27:36.
- κατανύσσω — no Middle Liddell entry either; LSJ's *stab, gouge*, and in the passive *to be sorely
  pricked*. 27:38.
- προσοχθίζω — LSJ gives the phrase of this verse, προσώχθικα τῇ ζωῇ μου, under *am weary of*; its
  first sense is *to be wroth with*. 27:46.
- πιότης — LSJ, *fattiness*, then *wealth, prosperity*: the blessing of 27:28 and the word of 27:39.
- ἐπιγινώσκω — filed under the Attic ἐπιγιγνώσκω, as γινώσκω under γιγνώσκω. 27:23.
- ταχύ and δικαίως — adverbs, filed inside their adjectives' entries, as ὀρθῶς at 4:7. 27:20, 27:36.
- ζυγός — Middle Liddell heads the neuter ζυγόν; Rahlfs prints the masculine article, so the lemma
  keeps the masculine the text has. 27:40.
- The aspect formulas are now read past by the bare-headword check in `build/validate.py`: at 27:23
  ὡς is a unit, `as`, and the *as* inside *kept on being as a standing …* is the project's own
  phrasing, not that headword loose in the text.
- One sense each in GEN 27, so plain text: υἱός `son`; βραχίων `the arms`; ἐπικατάρατος `yet more
  accursed`, as at 3:14; οἶνος `wine`; θυγάτηρ `the daughters`.

| lemma | headword | chain | used |
| --- | --- | --- | --- |
| γυμνός | `the naked parts` | `the naked parts and unclad, the unarmed, the uncovered, the stripped of` | 27:16 |
| δέρμα | `the skins` | `the skins, the hides, the skins prepared for bags and bottles` | 27:16 |
| δίδωμι | `may he give` | `may he give, may he grant, may he provide, may he give over and deliver up` | 27:28 |
| δεύτερος | `second` | `second, coming in second, next best, next, after, secondly and next and afterwards and a second time, a second time, secondary, second of two` | 27:36 |
| δικαίως | `observantly of custom and social rule` | `observantly of custom and social rule, well-orderedly and civilly, observantly of right and righteously, evenly and well-balancedly, regularly and exactly, rightly and lawfully and justly, really and genuinely and truly, fairly and moderately` | 27:36 |
| δουλεύω | `let them be slaves` | `let them be slaves, let them serve and be subject to` | 27:29 |
| δουλεύω | `you will be a slave` | `you will be a slave, you will serve and be subject to` | 27:40 |
| δρόσος | `of the dew` | `of the dew, of pure water, of anything tender, of the young of animals` | 27:28, 27:39 |
| δόλος | `of a bait` | `of a bait, of any cunning contrivance for deceiving and catching, of any trick, of a stratagem, of craft and cunning and treachery` | 27:35 |
| εἰμί | `let be` | `let be` | 27:33 |
| εἰσφέρω | `carried into` | `carried into, brought in and contributed, paid the property-tax, brought` | 27:18, 27:25 |
| εἰσφέρω | `you will carry into` | `you will carry into, you will bring in and contribute, you will pay the property-tax, you will bring` | 27:10 |
| εὐλογέω | `having been spoken well of` | `having been spoken well of and standing so, having been praised, having been honoured, having been blessed` | 27:29, 27:33 |
| εὐλογέω | `may speak well of` | `may speak well of, may praise, may honour, may bless` | 27:4, 27:10, 27:19, 27:25, 27:31 |
| εὐλογέω | `speak well of` | `speak well of, praise, honour, bless` | 27:34, 27:38 |
| εὐλογέω | `the one speaking well of` | `the one speaking well of, praising, honouring, blessing` | 27:29 |
| εὐλογία | `good language` | `good language, fine language, a fair speech and specious talk, eulogy and panegyric, blessing` | 27:12, 27:36, 27:38 |
| εὐλογία | `good language` | `good language, fine language, a fair speech and specious talk, eulogy and panegyric, blessing` | 27:12, 27:36, 27:38 |
| εὐλογία | `of the good language` | `of the good language, of the fine language, of the fair speech and specious talk, of the eulogy and panegyric, of the blessing` | 27:41 |
| εὐλογία | `the good language` | `the good language, the fine language, the fair speech and specious talk, the eulogy and panegyric, the blessing` | 27:35, 27:36 |
| εὑρίσκω | `you found` | `you found, you found out, you discovered, you got and gained` | 27:20 |
| ζυγός | `the yoke` | `the yoke, the cross-bar, the pair and team, the balance and scales, the rowing-bench` | 27:40 |
| ζωή | `to the life` | `to the life, to the means of life and substance, to existence, to a way of life` | 27:46 |
| θήρα | `hunting of wild beasts` | `hunting of wild beasts and the chase, eager pursuit, the beast taken and spoil and booty and prey and game` | 27:3, 27:5, 27:7, 27:33 |
| θήρα | `of the hunting of wild beasts` | `of the hunting of wild beasts and chase, of the eager pursuit, of the beast taken and the spoil and booty and prey and game` | 27:19, 27:25, 27:30, 27:31 |
| θηρεύω | `having hunted` | `having hunted, having gone hunting, having hunted after and chased and caught, having hunted down, having laid wait for` | 27:33 |
| θηρεύω | `hunt` | `hunt, go hunting, hunt after and chase and catch, hunt down, lay wait for` | 27:3 |
| θηρεύω | `to hunt` | `to hunt, to go hunting, to hunt after and chase and catch, to hunt down, to lay wait for` | 27:5 |
| θυμός | `the soul` | `the soul, the spirit and heart, the anger and wrath, the mind and temper, the will and desire, the courage and spirit` | 27:44 |
| καθαιρέω | `you may take down` | `you may take down, you may put down and close, you may bring down, you may put down by force and destroy and kill and slay, you may put down and reduce and depose and dethrone and remove, you may rase to the ground and pull down, you may cancel and rescind, you may condemn, you may reduce, you may overpower and seize and catch, you may fetch down as a reward and achieve and take and carry off` | 27:40 |
| κατάρα | `curse` | `curse` | 27:12 |
| κατάρα | `the curse` | `the curse` | 27:13 |
| κατανύσσω | `having been stabbed` | `having been stabbed and gouged, having been sorely pricked, having been bewildered and stunned` | 27:38 |
| καταράομαι | `the one calling down curses upon` | `the one calling down curses upon and imprecating upon, cursing and execrating, uttering imprecations` | 27:29 |
| καταφρονέω | `thinking down upon` | `thinking down upon, looking down upon and thinking slightly of, regarding slightly and despising` | 27:12 |
| κατοίκησις | `the settling in`, plain text: one translation; EXO 11 took out what the entry does not give, as at GEN 10 (*the dwelling, the habitation* were LSJ's) | | 27:39 |
| κἀγώ | `and me` | `and me` | 27:34, 27:38 |
| λαλέω | `of talking` | `of talking, of chatting, of prattling, of babbling, of saying, of talking of, of speaking, of chattering, of chirping` | 27:5, 27:6 |
| λαμβάνω | `has taken` | `has taken and it stands so, has received and it stands so, has taken hold of and grasped and seized and it stands so` | 27:36 |
| λαμβάνω | `will take` | `will take, will receive, will take hold of and grasp and seize` | 27:46 |
| λεῖος | `smooth` | `smooth, plain and not embroidered, smooth and level and flat, smooth-skinned and beardless` | 27:11 |
| μάχαιρα | `to the large knife` | `to the large knife and dirk, to the knife for cutting up, to the short sword and dagger, to the sabre and bent sword, to the rasor` | 27:40 |
| μέν | `on the one hand` | `on the one hand and other hand, as well as and while, whereas, indeed, for my part, surely, accordingly and so, at all events and at any rate, so then, nay rather, nay, yea rather, yet and but however and nevertheless, of course and certainly, only` | 27:22 |
| μεταπέμπω | `I will send after` | `I will send after, I will send for and summon` | 27:45 |
| νέος | `younger` | `younger, newer, fresher, unexpected and strange` | 27:15, 27:42 |
| οἰκέτης | `house-slaves` | `house-slaves and menials, one's household and the women and children`, brought to its card in EXO 32 | 27:37 |
| οἰκέω | `inhabit` | `inhabit, occupy, dwell and live, be settled` | 27:44 |
| οἶνος | `with wine` | `with wine` | 27:37 |
| πέμπω | `having sent` | `having sent and despatched, having conveyed and carried, having conducted, having sent forth` | 27:42 |
| πένθος | `of the grief` | `of the grief and sadness and sorrow, of the mourning for, of the public mourning, of the misfortune` | 27:41 |
| παραδίδωμι | `handed over to another` | `handed over to another and transmitted, transmitted and imparted, delivered up and surrendered, betrayed, committed, gave up, handed down, granted and bestowed, offered and allowed` | 27:20 |
| παύω | `to take one's rest` | `to take one's rest, to rest and cease and have done, to leave off from and rest and cease from, to be at rest, to leave off doing` | 27:30 |
| περιτίθημι | `placed round` | `placed round, bestowed and conferred upon` | 27:16 |
| πικρός | `pointed` | `pointed, sharp, keen, pungent and bitter, piercing and shrill, cruel and relentless, embittered and angry` | 27:34 |
| πιότης | `of the fattiness` | `of the fattiness, of wealth and prosperity` | 27:28, 27:39 |
| πλήρης | `of filled` | `of filled, of infected by, of satiated with, of filled with, of full, of full of people, of full and complete` | 27:27 |
| πλῆθος | `a great number` | `a great number and throng and crowd and multitude, the greater number and greater part and mass and main body, the majority and people, the populace and mob, quantity, number, magnitude and size, extent, amount, length` | 27:28 |
| ποιέω | `I may make` | `I may make, I may do, I may produce, I may create` | 27:37 |
| πρίν | `before` | `before, before that time and sooner, aforetime and formerly and once and erst, of old` | 27:4 |
| πρεσβύτερος | `of the elder` | `of the elder, of the older, of the higher and more important, of the greater than, of an elder of the Jewish Council, of an elder of the Church and presbyter` | 27:15, 27:42 |
| προσάγω | `bring to` | `bring to, furnish and supply, put to and add, move towards and apply` | 27:25 |
| προσάγω | `brought to` | `brought to, furnished and supplied, put to and added, moved towards and applied` | 27:25, 27:31 |
| προσκυνέω | `they will make obeisance` | `they will make obeisance, they will fall down and worship and worship and adore, they will do reverence to, they will make the salam, they will prostrate themselves before` | 27:29 |
| προσοχθίζω | `I am wroth with` | `I am wroth with and it stands so, I am weary of and it stands so, I am treated with contumely and it stands so` | 27:46 |
| πρόβατον | `the things that walk forward` | `the things that walk forward, the cattle, the flocks and herds, the horses, the small cattle, the sheep` | 27:9 |
| πτερνίζω | `has struck with the heel` | `has struck with the heel and it stands so, has tripped up and supplanted and it stands so, has heeled an old shoe and it stands so` | 27:36 |
| σκεῦος | `the vessel` | `the vessel, the implement of any kind, the inanimate object and thing, the body and the vessel of the soul` | 27:3 |
| στηρίζω | `I made fast` | `I made fast and propped and fixed and set, I confirmed and established, I fixed and settled and determined` | 27:37 |
| στολή | `the equipment` | `the equipment and armament, the equipment and raiment and apparel, the piece of dress and garment and robe` | 27:15 |
| σῖτος | `of corn` | `of corn and grain, of food made from grain and bread, of meat, of drink` | 27:28 |
| σῖτος | `with corn` | `with corn, with grain, with food made from grain and bread, with meat, with drink` | 27:37 |
| ταχύ | `quickly` | `quickly, swiftly, fleetly` | 27:20 |
| τελευτή | `of the finishing` | `of the finishing and completion and accomplishment, of the termination and end, of the end and event and issue` | 27:2 |
| τις | `some` | `some, any, a certain one` | 27:44 |
| τράχηλος | `of the neck` | `of the neck and throat` | 27:16, 27:40 |
| φέρω | `bring` | `bring, bear, carry, endure` | 27:4, 27:7, 27:13 |
| φέρω | `brought` | `brought, bore, carried, endured` | 27:14 |
| φαρέτρα | `quiver` | `quiver` | 27:3 |
| φιλέω | `I love` | `I love, I regard with affection, I feel affection, I love and cherish, I treat affectionately and kindly and welcome` | 27:4 |
| φιλέω | `love` | `love, regard with affection, feel affection, love and cherish, treat affectionately and kindly and welcome` | 27:26 |
| φιλέω | `loved` | `loved, regarded with affection, felt affection, loved and cherished, treated affectionately and kindly and welcomed` | 27:27 |
| φιλέω | `loves` | `loves, regards with affection, feels affection, loves and cherishes, treats affectionately and kindly and welcomes` | 27:9 |
| φιλέω | `was loving` | `was loving, was regarding with affection, was feeling affection, was loving and cherishing, was treating affectionately and kindly and welcoming` | 27:14 |
| ψηλαφάω | `I will feel` | `I will feel and grope about, I will feel about for and search after, I will feel and touch and stroke` | 27:21 |
| ψηλαφάω | `felt` | `felt and groped about, felt about for and searched after, felt and touched and stroked` | 27:22 |
| ψηλαφάω | `may feel` | `may feel and grope about, may feel about for and search after, may feel and touch and stroke` | 27:12 |
| ἀμβλύνω | `were blunted` | `were blunted and had the edge taken off, were made dull, became dull and lost their edge` | 27:1 |
| ἀνίστημι | `let stand up` | `let stand up, let rise, let rise to fight against, let rise to go and set out` | 27:31 |
| ἀναβοάω | `cried aloud` | `cried aloud, shouted aloud, called out, cried out` | 27:34, 27:38 |
| ἀπαγγέλλω | `was brought tidings of` | `was brought tidings of, was reported, was announced, was carried a report of, was related and narrated` | 27:42 |
| ἀπειλέω | `forces back` | `forces back` | 27:42 |
| ἀποδιδράσκω | `run away` | `run away and off and escape, flee from, desert, flee and shun` | 27:43 |
| ἀποκτείνω | `I may kill` | `I may kill and slay, I may condemn to death` | 27:41 |
| ἀποκτείνω | `to kill` | `to kill, to slay` | 27:42 |
| ἀποστέλλω | `having sent off` | `having sent off, having sent away and banished, having despatched, having gone away and departed` | 27:45 |
| ἀτεκνόω | `I may be made childless` | `I may be made childless, I may be deprived of children` | 27:45 |
| ἁπαλός | `soft to the touch` | `soft to the touch, tender, fresh, soft and gentle, soft and delicate` | 27:9 |
| ἄνωθεν | `from above` | `from above and on high, from the upper country, above and on high, from the beginning, by descent, over again and anew` | 27:39 |
| ἄρτος | `the cakes` | `the cakes, the loaves of wheat-bread, the breads` | 27:17 |
| ἐγγίζω | `bring near` | `bring near and bring up to, approach, be imminent, approximate to, be next of kin, be on the point of` | 27:21, 27:26 |
| ἐγγίζω | `let bring near` | `let bring near and bring up to, let approach, let be imminent, let approximate to, let be next of kin, let be on the point of` | 27:41 |
| ἐγκοτέω | `was indignant at` | `was indignant at` | 27:41 |
| ἐκλύω | `you will loose` | `you will loose and release and set free, you will unloose and unstring, you will relax and enfeeble, you will bring to an end` | 27:40 |
| ἐλάσσων | `smaller` | `smaller, less, worse and worse off, worse than and inferior to, subservient to, fewer, the smaller number` | 27:6 |
| ἐνδύω | `clothed` | `clothed, put on, made to go into` | 27:15 |
| ἐντέλλομαι | `I enjoin` | `I enjoin, I command` | 27:8 |
| ἐξίστημι | `stood aside from` | `stood aside from, was displaced / disordered, …, changed one's position / one's opinion`, the intransitive section (Q18) | 27:33 |
| ἐπάγω | `I will bring upon` | `I will bring upon, I will bring on and forward, I will lead on and bring on, I will bring in, I will lay on` | 27:12 |
| ἐπιγινώσκω | `looked upon` | `looked upon and witnessed and observed, recognised and knew again, acknowledged and approved, found out and discovered and detected, came to a decision and resolved and decided` | 27:23 |
| ἐπιλανθάνομαι | `may forget` | `may forget` | 27:45 |
| ἐσθίω | `I will eat` | `I will eat, I will eat of` | 27:25 |
| ἐσθίω | `eat` | `eat, eat of` | 27:19 |
| ἐσθίω | `having eaten` | `having eaten, having eaten of` | 27:7 |
| ἐσθίω | `let eat` | `let eat, let eat of` | 27:31 |
| ἐσθίω | `will eat` | `will eat, will eat of` | 27:10 |
| ἔδεσμα | `meats` | `meats` | 27:4, 27:7, 27:9, 27:14, 27:31 |
| ἔδεσμα | `the meats` | `the meats` | 27:17 |
| ἔκστασις | `displacement` | `displacement, distraction of mind, astonishment and amazement, trance` | 27:33 |
| ἔριφος | `of the young goats` | `of the young goats and kids` | 27:16 |
| ἔριφος | `young goats` | `young goats and kids` | 27:9 |
| ἡμέρα, with ἐν | `in day` | `within, inside of, and by means of day, day-break, time` | 27:45 |
| ἤδη | `by this time` | `by this time, before this, already, now and presently and forthwith, directly` | 27:36 |
| ἱμάτιον | `of the outer garments` | `of the outer garments and cloaks, of the mantles, of the clothes` | 27:27 |
| ὀργή | `the natural impulse` | `the natural impulse, the temper and temperament and disposition and nature, the passion and anger and wrath` | 27:45 |
| ὀσμή | `smell` | `smell and scent and odour` | 27:27 |
| ὀσμή | `the smell` | `the smell and scent and odour` | 27:27 |
| ὅπως | `in order that` | `in order that, so that` | 27:4, 27:10, 27:19, 27:31 |
| ὑπακούω | `listen to` | `listen to and hearken to and hear, give ear and hearken, obey` | 27:13 |
| ὑπολείπω | `you left remaining for yourself` | `you left remaining for yourself, you left behind for yourself, you reserved for yourself` | 27:36 |
| ὦ | `O` | `O, oh` | 27:20 |

### Words new in GEN 26

- νόμιμος — τὰ νόμιμα is the adjective used as a noun, so it takes the entry's noun sense, *usages,
  customs*, and then *funeral rites*. 26:5.
- πρόσταγμα, ἐντολή, δικαίωμα, νόμιμος — four words in a row for the Hebrew's *mišmartî miṣwōtay
  ḥuqqôtay wĕtôrōtāy*, each with its own chain. 26:5.
- ὅρκος and its names — the well of 26:33 is named Ὅρκος, and the city Φρέαρ ὅρκου: Greek words
  Rahlfs prints as names, so they keep their capitals in the lemma and carry a name's gloss, as
  Ἀδικία, Ἐχθρία and Εὐρυχωρία do at 26:20–22.
- ἁπτόμενος — the middle of ἅπτω, *to fasten oneself to, touch*, as at 3:3. 26:11.
- ἐκρίνοντο — κρίνω in the middle: *were being separated*, of a dispute. 26:21.
- ὑπὸ κυρίου — ὑπό with the genitive, whose first sense is *from under*; *by*, of the agent, is
  inside that sense. 26:29.
- μικροῦ — the adverbial genitive, *within a little*: `of small`. 26:10.
- ποιήσειν — the future infinitive, with the present infinitive's chain, as ἀδικήσειν at 21:23. 26:29.
- ἕως οὗ — ἕως with the relative in the genitive, *until which*. 26:13; and at 26:32 the relative is
  drawn into the genitive after φρέατος.
- Names: Αβιμελεχ and Φικολ and Οχοζαθ again, as at 21:22; Γεραρα, which declines as a neuter plural
  (Γεραροις, Γεραρων), as at 20:1 — GEN 10:19's Γεραρα was brought into line with it; Ιουδιν, Βεηρ,
  Βασεμμαθ, Αιλων, and Ευαῖος the Hivite, whose breathing Rahlfs leaves off. 26:1–34.
- One sense each in GEN 26, so plain text: ἐνευλογέω `will be blessed in` (26:4), as at 22:18;
  ἑκατοστεύω `bearing a hundredfold` (26:12, LSJ); ἐμφράσσω `blocked up` (26:15, 26:18); καθότι
  `in what manner` (26:29); ὕδωρ `water`; θυσιαστήριον `an altar` (26:25).

| lemma | headword | chain | used |
| --- | --- | --- | --- |
| αὐξάνω | `made large` | `made large and increased and augmented, increased in power and strengthened and exalted and aggrandised, promoted to honour and glorified and magnified, grew and waxed and increased, grew up` | 26:22 |
| βασιλεύς | `the king` | `the king and chief, the hereditary king, the lord and master and householder, the second of the nine archons, the king of Persia` | 26:8 |
| βδελύσσομαι | `we felt nausea` | `we felt nausea and were sick, we felt a loathing at and loathed` | 26:29 |
| βοῦς | `of oxen` | `of oxen, of cows, of ox-hide shields` | 26:14 |
| γε | `at least` | `at least, at any rate, even, that is to say, really, namely and that is, yes and, well then` | 26:9 |
| γεώργιον | `fields` | `fields, orchards, husbandries, crops, taxes` | 26:14 |
| διατίθεμαι | `we will dispose` | `we will dispose, we will make a will, we will arrange, we will covenant` | 26:28 |
| δικαίωμα | `the acts by which wrong is set right` | `the acts by which wrong is set right, the judgments and punishments and penalties, the pleas of right, the justifications, the ordinances and decrees` | 26:5 |
| διότι | `for the reason that` | `for the reason that and since, wherefore and for what reason, that` | 26:22 |
| δοχή | `a receiving` | `a receiving, a reception, an entertainment, a feast` | 26:30 |
| δυνατός | `stronger` | `stronger, mightier, abler, more powerful, more possible, more practicable` | 26:16 |
| εὐλογέω | `I have spoken well of` | `I have spoken well of and it stands so, I have praised and it stands so, I have honoured and it stands so, I have blessed and it stands so` | 26:24 |
| εὑρίσκω | `we found` | `we found, we found out, we discovered, we got and gained` | 26:32 |
| ζηλόω | `rivalled` | `rivalled, vied with, emulated, were jealous of and envied, pronounced happy and admired and praised, desired emulously and strove after, were impelled by zeal` | 26:14 |
| θάνατος | `of death` | `of death, of the death threatened, of the sentence of death` | 26:11 |
| θυρίς | `of the window`, plain text: one translation; EXO 11 took out what the entry does not give, as at GEN 8:6 (*little door* was the etymology's *Dim. of θύρα*) | | 26:8 |
| καθότι | `in what manner` | `in what manner` | 26:29 |
| κακός | `bad` | `bad, mean and ugly, ill-born and mean and ignoble, craven and cowardly and base, worthless and sorry and poor, evil and wicked, baneful and unlucky and abusive` | 26:29 |
| καλῶς | `well` | `well, rightly, well and happily, right well, rightly and deservedly` | 26:29 |
| καταβαίνω | `you may step down` | `you may step down, you may go and come down, you may go down from, you may dismount, you may come down stairs, you may go down from the inland parts to the sea, you may come to land and get safe ashore, you may go down into the arena, you may come down from the tribune, you may come to, you may end` | 26:2 |
| καταλύω | `put down` | `put down and destroyed, dissolved and broke up, deposed, dismissed and disbanded, neglected, ended and brought to an end, broke, made peace with, unloosed and unyoked, took down, took up his quarters and lodged, went and lodged, took his rest` | 26:17 |
| κρίνω | `were being separated` | `were being separated and parted and put asunder and distinguished, were being picked out and chosen, were being decided, were being judged, were being adjudged, were being judged of and estimated, were being expounded and interpreted` | 26:21 |
| κριθή | `barley-corns` | `barley-corns and barley, beer` | 26:12 |
| κτῆνος | `flocks and herds` | `flocks and herds, single beasts, beasts for riding` | 26:14 |
| λέγω | `we said` | `we said, we spoke, we declared, we called by name, we told` | 26:28 |
| λιμός | `of the hunger` | `of the hunger and famine` | 26:1 |
| μάχομαι | `fought` | `fought, fought with, quarrelled and wrangled and disputed, opposed and gainsaid, contended for the mastery` | 26:20, 26:22 |
| μισέω | `you hated` | `you hated` | 26:27 |
| νόμιμος | `the usages` | `the usages and customs, the funeral rites` | 26:5 |
| πάλιν | `back` | `back and backwards, contrariwise, opposite, the change, again and once more and anew, again in turn` | 26:18 |
| πήγνυμι | `made fast` | `made fast, fixed in the earth and planted, fastened together and constructed and built, made solid and stiff and hard, froze, became solid and stiff, became congealed and froze` | 26:25 |
| παραγίνομαι | `having been beside` | `having been beside / been by / near / attended upon, having been present at, …, having been fully grown`, the eight senses of every form (EXO 36; Q15) | 26:32 |
| παρακύπτω | `having stooped sideways` | `having stooped sideways, having stooped for the purpose of looking at, having looked sideways at and cast a careless glance on, having peeped out of, having peeped in and looked in` | 26:8 |
| παροικέω | `dwell beside` | `dwell beside, dwell along the coast of, live near, dwell among, lie near, live in and sojourn` | 26:3 |
| πλατύνω | `made broad` | `made broad, widened, enlarged` | 26:22 |
| ποιμήν | `of the herdsmen` | `of the herdsmen, of the shepherds, of the captains and chiefs` | 26:20 |
| ποιμήν | `the herdsmen` | `the herdsmen, the shepherds, the captains and chiefs` | 26:20 |
| πολυχρόνιος | `long-existing` | `long-existing and of olden time and ancient, lasting for long` | 26:8 |
| προβαίνω | `stepping on` | `stepping on, stepping forward, advancing, proceeding, going before, being before and superior to, overstepping` | 26:13 |
| πρόβατον | `of things that walk forward` | `of things that walk forward, of cattle, of flocks and herds, of horses, of small cattle, of sheep` | 26:14 |
| πρόσταγμα | `the ordinances` | `the ordinances and commands` | 26:5 |
| πρότερος | `before` | `before and in front and forward, former and sooner, elder, above and superior, earlier` | 26:1 |
| πόλις | `to the city` | `to the city, to the citadel, to the country, to the body of citizens, to the state` | 26:33 |
| σπείρω | `sowed` | `sowed, scattered like seed and strewed and threw about, spread abroad, was scattered and dispersed` | 26:12 |
| συντάσσω | `drew up together` | `drew up together, arranged in order, appointed, enjoined, ordered` | 26:11 |
| σωτηρία | `of a saving` | `of a saving and deliverance and preservation and safety, of a safe return, of a keeping safe, of security and a guarantee for safety` | 26:31 |
| τρόπος | `turn` | `turn, direction, course, way, manner and fashion, way of life and habit and custom, character and temper, manner and style, tropes and figures` | 26:29 |
| φάραγξ, with ἐν | `in the ravine` | `within, inside of, and by means of the ravine, the chasm, the gully, the mountain-stream` | 26:17, 26:19 |
| φάσκω | `saying` | `saying and affirming and asserting, thinking and deeming and expecting, promising` | 26:20 |
| φρέαρ | `of the well` | `of the well, of the tank and cistern and reservoir, of the oil jar` | 26:20, 26:32 |
| φρέαρ | `the wells` | `the wells, the tanks and cisterns and reservoirs, the oil jars` | 26:15, 26:18 |
| φυλάσσω | `kept watch and ward` | `kept watch and ward and kept guard, watched and guarded and kept and defended, watched for and lay in wait for, kept and maintained and cherished, observed` | 26:5 |
| χράομαι | `we used` | `we used, we had and used, we indulged, we experienced and suffered and were subject to, we came to, we lived under, we made use of, we treated, we were intimate with, we were in need and yearned after, we had in use and possessed` | 26:29 |
| χρόνος, with ἐν | `in the time` | `within, inside of, and by means of the time, the definite time and while and period and season, the periods of time, the lifetime and an age, the season and portion of the year, the delay and loss of time` | 26:1, 26:15 |
| χωρίς | `separately` | `separately and asunder and apart, by oneself, separately and besides, separately and one by one, except, of different nature and kind, without, separate from and apart, aloof from and far from, independent of and without reckoning and not to mention and besides, differently from and otherwise than` | 26:1 |
| ἀδικέω | `did wrong` | `did wrong, did one wrong and wronged and injured, spoiled and damaged` | 26:20 |
| ἀπέρχομαι | `go away` | `go away, depart from, depart, depart from life` | 26:16 |
| ἀπαίρω | `having lifted off` | `having lifted off and carried off and taken away and removed from, having led away, having sailed and marched away and departed, having departed from, having set out on` | 26:21, 26:22 |
| ἀποίχομαι | `were gone away` | `were gone away, were absent and away, had departed` | 26:31 |
| ἀποκτείνω | `they may kill` | `they may kill and slay, they may condemn to death` | 26:7 |
| ἀποστέλλω | `you sent off` | `you sent off, you sent away and banished, you despatched, you went away and departed` | 26:27 |
| ἀρά | `prayer` | `prayer, prayer for evil and curse and imprecation, effect of the curse and bane and ruin` | 26:28 |
| ἄγνοια | `want of perception` | `want of perception and ignorance, a mistake` | 26:10 |
| ἅπτω | `the one fastening himself to` | `the one fastening himself to and clinging to and hanging on by and laying hold of and grasping and touching, engaging in and taking part in, laying hold of and disputing, setting upon and attacking and assailing, touching and affecting, grasping with the senses and apprehending and perceiving, coming up to and reaching and gaining` | 26:11 |
| ἐμφράσσω | `blocked up` | `blocked up` | 26:15, 26:18 |
| ἐνιαυτός, with ἐν | `in the year` | `within, inside of, and by means of the year, the long period of time, the cycle of the year` | 26:12 |
| ἐντολή | `the injunctions` | `the injunctions and orders and commands and behests` | 26:5 |
| ἐξαποστέλλω | `we sent quite away` | `we sent quite away, we dispatched` | 26:29 |
| ἐπάγω | `you brought upon` | `you brought upon, you brought on and forward, you led on and brought on, you brought in, you laid on, you brought upon oneself` | 26:10 |
| ἐρίζω | `striving` | `striving and wrangling and quarrelling, rivalling and vying with and being a match for, contending with, engaging in a contest and keeping the contest up` | 26:35 |
| ἑκατοστεύω | `bearing a hundredfold` | `bearing a hundredfold` | 26:12 |
| ἔνοχος | `held in` | `held in, liable to and subject to, liable to the penalty` | 26:11 |
| ἕτερος | `other` | `other, one of two, the other of two, another, second, different, other than, worse` | 26:21, 26:22 |
| ὀρύσσω | `dug` | `dug, dug up, dug through and made a canal through, buried` | 26:15, 26:18, 26:19, 26:21, 26:22, 26:25, 26:32 |
| ὀρύσσω | `dug` | `dug, dug up, dug through and made a canal through, buried` | 26:15, 26:18, 26:19, 26:21, 26:22, 26:25, 26:32 |
| ὁράω | `we have seen` | `we have seen and it stands so, we have perceived and it stands so, we have beheld and it stands so, we have looked at and it stands so` | 26:28 |
| ὄνομα | `the names` | `the names, the fames, the mere names, the phrases and expressions` | 26:18 |
| ὅρκος | `the object by which one swears` | `the object by which one swears and witness of an oath, the oath` | 26:3 |
| ὑπακούω | `listened to` | `listened to and hearkened to and heard, gave ear and hearkened, obeyed` | 26:5 |
| ὑπό + genitive | `from under` | `from under, under and beneath, by, under the protection of` | 26:29 |

### Words new in GEN 25

- πρεσβύτης — Middle Liddell's entry is the cross-reference *= πρέσβυς I*, so the senses are that
  sense's alone, *an old man* and *the elder*; πρέσβυς II and III, the ambassador and the chief, and
  the comparative filed inside it, are another sense's. 25:8.
- πλήρης — Middle Liddell's first sense, *c. gen. full of a thing*, is untranslated; the first English
  is *filled*. 25:8.
- γένεσις and γενεά — the plural αἱ γενέσεις is the chain of GEN 2:4, as at 6:9; γενεά, a different
  word, is first *race, stock, family*. 25:12, 25:13, 25:19.
- δέομαι — Middle Liddell files the deponent under δέω, *to lack*: `was lacking`, where the verse has
  Isaac praying. 25:21.
- ἔλαβεν ἐν γαστρί — the idiom for conceiving, kept word for word; γαστήρ is first *the paunch, belly*,
  and *the womb* is its second sense. 25:21.
- ἀποδίδωμι in the middle — *to give away of one's own will, to sell*, the middle's own sense, where
  the active is *to give up, give back*. 25:31, 25:33.
- τελευτάω — first *to complete, finish, accomplish*; *to end life, to die*, the verse's sense, stands
  inside that first sense. 25:32.
- γεύω in the active — one sense, *to give a taste of*: plain text. Its *to taste of* is the middle's.
  25:30.
- ἐπιλαμβάνομαι — MorphGNT's middle, filed under the active ἐπιλαμβάνω; the perfect participle takes
  the middle's senses, *to hold oneself by, lay hold of, catch*, with the perfect's standing state.
  25:26.
- ὅδε — τῇδε, the dative feminine used of the place: `to this`. 25:24.
- Names: this chapter glosses thirty, Keturah's sons and Ishmael's among them. Ναβδεηλ stands for two
  different Hebrew names — ʿAbdĕʾēl at 25:13, and at 25:3 a name the Hebrew does not have at all.
  Σύρος, the Syrian, is a people's name declined in Greek, as Χετταῖος is, and the article before it
  is not printed. 25:2–20.
- One sense each in GEN 25, so plain text: πρωτότοκος `first-born` (25:13, 25:25), as at 10:15;
  νεανίσκος `the youths` (25:27); πυρράκης `ruddy` (25:25, LSJ), a masculine noun in LSJ, not an
  adjective; φαυλίζω `held cheap` (25:34); κυνηγέω `to hunt` (25:27), two glosses of one sense.

| lemma | headword | chain | used |
| --- | --- | --- | --- |
| αὐξάνω | `were made large` | `were made large and increased and augmented, were increased in power and strengthened and exalted and aggrandised, were promoted to honour and glorified and magnified, grew and waxed and increased, grew up` | 25:27 |
| γένος | `the race` | `the race, the stock and family, the offspring and posterity, the clan and house, the tribe and caste, the breed, the age and generation, the sex and gender, the class and sort and kind, the genus` | 25:17 |
| γαστήρ, with ἐν | `in belly` | `within, inside of, and by means of belly, paunch, the paunch stuffed with mince-meat and black-pudding and sausage, the womb` | 25:21 |
| γαστήρ, with ἐν | `in the belly` | `within, inside of, and by means of the belly, the paunch, the paunch stuffed with mince-meat and black-pudding and sausage, the womb` | 25:23 |
| γενεά | `of the races` | `of the races and stocks and families, of the breeds, of the tribes and nations, of the races and generations, of the offspring, of the birth-places, of the ages and times of life, of the times of birth` | 25:13 |
| γῆρας, with ἐν | `in old age` | `within, inside of, and by means of old age, the latter part of life` | 25:8 |
| δέομαι | `was lacking` | `was lacking, was missing, was standing in need of, was in want and need, was asking for and begging` | 25:21 |
| δίδυμος | `double` | `double and twofold and twain, twin, twins` | 25:24 |
| δασύς | `thick with hair` | `thick with hair and hairy and shaggy and rough, downy, thick with leaves, thick with bushes and wood, bushy country` | 25:25 |
| διαστέλλω | `will be put asunder` | `will be put asunder and torn open, will be distinguished and defined, will be determined, will be given express orders` | 25:23 |
| δορά | `skin` | `skin and hide` | 25:25 |
| δουλεύω | `will be a slave` | `will be a slave, will serve and be subject to` | 25:23 |
| δόμα | `gifts` | `gifts, payments` | 25:6 |
| ζάω | `living` | `living, alive, in full life and strength and fresh and strong` | 25:6 |
| θήρα | `the hunting of wild beasts` | `the hunting of wild beasts and chase, the eager pursuit, the beast taken and the spoil and booty and prey and game` | 25:28 |
| κοιλία | `of the large cavity of the body` | `of the large cavity of the body and belly, of the intestines and bowels` | 25:23 |
| κοιλία, with ἐν | `in the large cavity of the body` | `within, inside of, and by means of the large cavity of the body and belly, the intestines and bowels` | 25:24 |
| κτάομαι | `procured for himself` | `procured for himself, got, gained, acquired, brought upon himself and incurred, procured for another` | 25:10 |
| κυνηγέω | `to hunt` | `to hunt and chase` | 25:27 |
| λαός | `peoples` | `peoples, men, soldiers, land-armies, common men, folk, Jews, Christians` | 25:23 |
| μέγας | `the bigger` | `the bigger, the greater, the taller, the vaster, the stronger and mightier, the weightier and more important` | 25:23 |
| μέλλω | `thinks of doing` | `thinks of doing, intends to do, is about to do, is destined to do, is like to do, delays and puts off and hesitates and scruples` | 25:22 |
| νεανίσκος | `the youths` | `the youths` | 25:27 |
| οἶδα | `knowing` | `knowing, being assured, being versed in` | 25:27 |
| παιδίον | `the young children` | `the young children, the young slave-lads` | 25:22 |
| παλλακή | `of the concubines` | `of the concubines and mistresses` | 25:6 |
| πεδίον | `of the plain` | `of the plain, of the flat, of the plain flat open country` | 25:29 |
| πλήρης | `filled` | `filled, infected by, satiated with, filled with, full, full of people, full and complete` | 25:8 |
| πληρόω | `were made full` | `were made full, were filled full of, were gorged and satiated, were filled with, were manned, were made full and complete, were fulfilled and paid in full and made up` | 25:24 |
| πρεσβύτης | `old man` | `old man, elder` | 25:8 |
| προστίθημι | `having put to` | `having put to, having handed over and delivered, having given and bestowed, having imposed further, having attributed, having added` | 25:1 |
| προστίθημι | `was put to` | `was put to, was handed over and delivered, was given and bestowed, was imposed further, was attributed, was added` | 25:8, 25:17 |
| πρωτοτόκια | `the rights of the first-born` | `the rights of the first-born and birthright` | 25:31, 25:32, 25:33, 25:34 |
| πτέρνα | `of the heel` | `of the heel, of the under part of the heel, of the ham` | 25:26 |
| πυνθάνομαι | `to learn by hearsay` | `to learn by hearsay, to learn, to hear, to hear of and hear tell of and hear news of, to inquire about` | 25:22 |
| πυρρός | `of flame-coloured` | `of flame-coloured, of yellowish-red, of red-haired, of red and tawny, of red with blushes` | 25:30 |
| σκηνή, with ἐν | `in the covered places` | `within, inside of, and by means of the covered places and tents, the camps, the dwelling-places, the temples` | 25:16 |
| σκιρτάω | `were springing` | `were springing, were leaping, were bounding` | 25:22 |
| τελευτάω | `to complete` | `to complete, to finish, to accomplish, to fulfil, to bring about, to bring to an end, to make an end of, to end life and die, to come to an end` | 25:32 |
| υἱός | `sons` | `sons` | 25:3, 25:4 |
| υἱός | `to the sons` | `to the sons` | 25:6 |
| φακός | `of lentil` | `of lentil, of its fruit` | 25:34 |
| φαυλίζω | `held cheap` | `held cheap and depreciated and disparaged` | 25:34 |
| ἀγαπάω | `was treating with affection` | `was treating with affection and caressing and loving and fond of, was regarding with brotherly love, was well pleased and contented with, was content` | 25:28 |
| ἀποδίδωμι | `gave away of his own will` | `gave away of his own will, sold` | 25:33 |
| ἀποδίδωμι | `give away of your own will` | `give away of your own will, sell` | 25:31 |
| ἀποθνήσκω | `to die off` | `to die off and die, to be put to death and slain` | 25:11 |
| ἄγροικος | `of the country` | `of the country, in the country, dwelling in the country and a countryman and rustic, clownish and boorish and rude, rough and uncultivated` | 25:27 |
| ἄπλαστος | `not moulded` | `not moulded, in its natural state and natural and unaffected` | 25:27 |
| ἄρτος | `cake` | `cake, loaf of wheat-bread, bread` | 25:34 |
| ἐκλείπω | `I leave out` | `I leave out and omit and pass over, I forsake and desert and abandon, I suffer an eclipse, I die, I leave off and cease and stop, I fail and am wanting` | 25:30 |
| ἐκλείπω | `having left out` | `having left out and omitted and passed over, having forsaken and deserted and abandoned, having suffered an eclipse, having died, having left off and ceased and stopped, having failed and been wanting` | 25:8, 25:17 |
| ἐκλείπω | `leaving out` | `leaving out and omitting and passing over, forsaking and deserting and abandoning, suffering an eclipse, dying, leaving off and ceasing and stopping, failing and being wanting` | 25:29 |
| ἐλάσσων | `to the smaller` | `to the smaller and less, to the worse and worse off, to worse than and inferior to, to subservient to, to fewer, to the smaller number` | 25:23 |
| ἐπιλαμβάνομαι | `having held herself by` | `having held herself by and standing so, having laid hold of and caught, having attacked, having made a seizure of, having got and obtained, having gained and reached, having attempted, having taken up and interrupted in speaking, having objected to` | 25:26 |
| ἔπαυλις, with ἐν | `in the folds` | `within, inside of, and by means of the folds` | 25:16 |
| ἕψεμα | `anything boiled` | `anything boiled, vegetables for kitchen use` | 25:29, 25:34 |
| ἕψεμα | `of anything boiled` | `of anything boiled, of vegetables for kitchen use` | 25:30 |
| ἕψω | `boiled` | `boiled, seethed, smelted and refined, cherished` | 25:29 |
| ὅδε | `to this` | `to this, to the immediate present, here and on the spot, thus, hither and to this spot, therefore and on this account` | 25:24 |
| ὅλος | `whole` | `whole and entire, continuous and incessant` | 25:25 |
| ὑπερέχω | `will hold over` | `will hold over, will have and hold above, will be above and rise above the horizon, will be above water, will rise above and overlook, will outflank, will overtop and exceed and outdo, will prevail, will get over and cross` | 25:23 |

### Words new in GEN 24

- ὅθεν — Middle Liddell's first sense is the Latin *unde*; the first English is *from whom*, and the
  chain goes on *from whatever source, where, whence and wherefore*. 24:5.
- μένω — the first sense is Latin only; the first English is *to stay at home, stay where one is,
  not stir*: `let stay at home`. Middle Liddell's misprint *remian* is printed *remain*. 24:55.
- ἐπικλίνω — first *to put* a door *to*: `put to`, with *to bend towards* and the intransitive's *to
  incline towards*; the passive's senses are left out. 24:14.
- ἀντλέω — first *to bale out bilge-water, bale the ship*; *to draw water* is its second sense. 24:13, 24:20.
- ὁλκή — *a drawing, dragging, tugging*; Middle Liddell has no *weight*, the sense of the verse. 24:22.
- κακὸν καλῷ — both neuters used as nouns, so each takes its first noun sense: κακός *evil, ill*, as τὰ
  κακά at 19:19; καλός *beauty*, then *moral beauty, virtue*. GEN 2:9, 2:17, 3:5 and 3:22 had read
  καλοῦ and καλόν with the adjective's senses, and were brought into line. 24:50.
- γηρᾶσαι — the first aorist of γηράσκω, to which Middle Liddell gives the causal *to bring to old
  age*; the chain keeps it. 24:36.
- ἐφέστηκα, ἕστηκα, ἕστηκας, ἑστηκότος — the intransitive perfects: `I have stood upon`, `I have
  been set and stand so`, as εἱστήκεισαν at 18:2. 24:13, 24:30, 24:31, 24:43.
- ἐγενήθην — the aorist passive of γίνομαι takes the middle's chain, as ἐγενήθη at 11:28. 24:7.
- περιεβάλετο, ὑδρεύομαι, νίψασθαι — middles, which take the entry's middle senses: *to throw round
  oneself, put on*; *to draw water for oneself*; *to wash one's hands*. 24:11–65.
- παρθένος — *an unmarried man* is the masculine's sense, and ἡ παρθένος leaves it out. 24:14.
- ἔφη — the imperfect, as MorphGNT codes it: `was declaring`. 24:47.
- εὐοδόω and ὁρκίζω — one sense each in the active, *to help on the way* and *to make one swear*, but
  written as units whose chain is the headword alone wherever plain text would put another unit's
  headword outside it (*the way*, *made*), as εἰσεσπάσαντο at 19:10. 24:12–56.
- τῷ ἑαυτοῦ θεράποντι — the article, the reflexive, the noun: `to the of himself` and θεράπων with no
  article of its own, as τὴν σεαυτοῦ ψυχήν at 19:17. 24:44.
- τοῦτου (24:58) — Rahlfs's own misprint for τούτου, kept as printed; the verse lists it in the new
  `printed` field, which `build/validate.py` reads as it reads `speech`.
- Names: Λαβαν `(Λαβαν, from Hebrew Lābān, "white")`; Μεσοποταμία `(Μεσοποταμία, Greek, "the land
  between the rivers", for Hebrew ʾĂram Nahărayim, "Aram of the two rivers")`. The article before the
  name of the land is not printed, as before a person's. 24:10, 24:29.
- One sense each in GEN 24, so plain text: ἐξορκίζω `I will adjure` (24:3); κοιμίζω `put to sleep`
  (24:11); παρασιωπάω `was passing over in silence` (24:21); ἐνώτιον `ear-rings` (24:22, LSJ);
  ποτιστήριον `the drinking-trough for cattle` (24:20, LSJ); βραχίων `the arm` (24:18), once *the
  shoulder*, a piece of βραχίων ὤμου, is left out; εὐλογητός `blessed` (24:27, 24:31); ὁρκισμός `the
  administration of an oath` (24:41); ἅβρα `the favourite slaves` (24:61, LSJ); καταπηδάω `leaped down`
  (24:64); θέριστρον `the light summer garment` (24:65), filed inside θερίστριον.

| lemma | headword | chain | used |
| --- | --- | --- | --- |
| βούλομαι | `wills` | `wills, wishes and is willing, means, professes and pretends and would fain, prefers` | 24:5 |
| γίνομαι | `I came into being` | `I came to be, I arose, I was brought into existence` | 24:4, 24:7 |
| γηράσκω | `to grow old` | `to grow old, to become old, to bring to old age` | 24:36 |
| δίδωμι | `they may give` | `they may give, they may grant, they may provide, they may give over and deliver up` | 24:41 |
| δείλη | `of afternoon` | `of afternoon, of the late afternoon and evening` | 24:63 |
| διηγέομαι | `set out in detail` | `set out in detail and described in full` | 24:66 |
| δραχμή | `handful` | `handful, drachm, drachma` | 24:22 |
| δύναμαι | `we will be able` | `we will be able and capable and strong enough, we will be powerful and mighty, we will have influence, we will dare and bear, we will pass for, we will be worth, we will be equivalent to, we will signify and mean, we will avail` | 24:50 |
| δῶρον | `gifts` | `gifts, presents, votive gifts, blessings` | 24:53 |
| εὐαρεστέω | `I was well pleasing` | `I was well pleasing, I seemed good and was resolved, I was well pleased and satisfied` | 24:40 |
| εὐδοκέω | `having been well pleased` | `having been well pleased, having consented, having been glad` | 24:26, 24:48 |
| εὐοδόω | `has helped on the way` | `has helped on the way and it stands helped on the way, has had a prosperous journey, has prospered and been successful` | 24:21, 24:27 |
| εὐοδόω | `help on the way` | `help on the way, have a prosperous journey, prosper and be successful` | 24:12 |
| εὐοδόω | `helped on the way` | `helped on the way, had a prosperous journey, prospered and was successful` | 24:48, 24:56 |
| εὐοδόω | `will help on the way` | `will help on the way, will have a prosperous journey, will prosper and be successful` | 24:40 |
| εὐοδόω | `you help on the way` | `you help on the way, you have a prosperous journey, you prosper and are successful` | 24:42 |
| θέλω | `may will` | `may will, may wish, may purpose, may be wont and accustomed, may mean and purport` | 24:8 |
| θεράπων | `waiting-man` | `waiting-man, attendant, companion in arms, servant` | 24:44 |
| κάμηλος | `of the camel` | `of the camel, of the camel in an army, of the camelry and camel-brigade` | 24:64 |
| κάμηλος | `of the camels` | `of the camels, of the camels in an army, of the camelry and camel-brigade` | 24:10, 24:30 |
| κάμηλος | `the camels` | `the camels, the camels in an army, the camelry and camel-brigade` | 24:11, 24:14, 24:22, 24:32, 24:46, 24:61 |
| κάμηλος | `to the camels` | `to the camels, to the camels in an army, to the camelry and camel-brigade` | 24:19, 24:20, 24:31, 24:32, 24:44 |
| καθαιρέω | `took down` | `took down, put down and closed, brought down, put down by force and destroyed and killed and slew, put down and reduced and deposed and dethroned and removed, rased to the ground and pulled down, cancelled and rescinded, condemned, reduced, overpowered and seized and caught, fetched down as a reward and achieved and took and carried off` | 24:18, 24:46 |
| καθαρός | `clear of dirt` | `clear of dirt and clean and spotless and unsoiled, clear and open and free, clear from shame and pollution and pure, clear of guilt and defilement and clean and pure, purified, clear of and from, clear of admixture and clear and pure, pure and genuine, without blemish, clear and exact` | 24:8 |
| κακός | `evil` | `evil, ill, evil word and reproach` | 24:50 |
| καλέω | `let us call` | `let us call, let us summon, let us call to ourselves, let us invite` | 24:57 |
| καλός | `to beauty` | `to beauty, to moral beauty and virtue` | 24:50 |
| κατέχω | `hold fast` | `hold fast, hold back and withhold, check and restrain and control and bridle, detain, possess and occupy, fill, occupy and be spread over and cover, confine and cover, hold down and overpower and oppress and afflict` | 24:56 |
| καταλύω | `to put down` | `to put down and destroy, to dissolve and break up, to depose, to dismiss and disband, to neglect, to end and bring to an end, to break, to make peace with, to unloose and unyoke, to take down, to take up one's quarters and lodge, to go and lodge, to take one's rest` | 24:23, 24:25 |
| καταμανθάνω | `was observing well` | `was observing well and examining closely, was learning thoroughly, was perceiving and understanding, was discovering and finding, was considering` | 24:21 |
| κληρονομέω | `let receive a share of an inheritance` | `let receive a share of an inheritance and inherit a portion, let inherit, let be an inheritor, let succeed` | 24:60 |
| κύριος | `of the lord` | `of the lord / master, of the head, of the master, of the Lord, of the Jehovah` | 24:9, 24:10, 24:12, 24:27, 24:36, 24:42, 24:48, 24:51 |
| λέγω | `of saying` | `of saying, of speaking, of declaring, of calling by name, of telling` | 24:30 |
| λαλέω | `has talked` | `has talked and it stands so, has chatted, has prattled, has babbled, has said, has talked of, has spoken, has chattered, has chirped` | 24:30 |
| λαμβάνω | `you may take` | `you may take, you may receive, you may take hold of and grasp and seize` | 24:3 |
| μένω | `let stay at home` | `let stay at home, let stay where one is, let not stir, let stay away from, let stay and tarry, let be lasting and remain and last and stand, let remain as one was and hold good and remain contented, let abide by, let await and expect and wait for` | 24:55 |
| μήτηρ | `of the mother` | `of the mother, of the dam, of the source` | 24:28, 24:67 |
| μήτηρ | `to the mother` | `to the mother, to the dam, to the source` | 24:53 |
| μηρός | `the thigh` | `the thigh, the leg-bones` | 24:2, 24:9 |
| μυριάς | `of numbers of ten thousand` | `of numbers of ten thousand, of myriads, of countless numbers` | 24:60 |
| νίπτω | `to wash one's hands` | `to wash one's hands, to purge and cleanse, to wash off` | 24:32 |
| οἰκέω | `I inhabit` | `I inhabit, I occupy, I dwell and live, I am settled` | 24:3 |
| οἰκέω | `of the ones dwelling in` | `of the ones dwelling in, settling in, colonising, inhabiting, settling and dwelling, lying and situate` | 24:13 |
| οἶκος | `house` | `house and abode and dwelling, room and chamber, house of a god and temple, household goods and substance, household and family` | 24:27 |
| οὗτος, with ἐν | `in this` | `within, inside of, and by means of this, the nearer, what follows` | 24:14, 24:44 |
| πίνω | `I drank` | `I drank, I drank of, I drank up` | 24:46 |
| πίνω | `I may drink` | `I may drink, I may drink of, I may drink up` | 24:14 |
| πίνω | `drink` | `drink, drink of, drink up` | 24:14, 24:18, 24:44, 24:46 |
| πίνω | `drinking` | `drinking, drinking of, drinking up` | 24:14, 24:19, 24:22 |
| πίνω | `drinking` | `drinking, drinking of, drinking up` | 24:14, 24:19, 24:22 |
| πίνω | `they drank` | `they drank, they drank of, they drank up` | 24:54 |
| πίνω | `they may drink` | `they may drink, they may drink of, they may drink up` | 24:19 |
| παρακαλέω | `was called to` | `was called to, was called to aid and called in and sent for and called on and invoked, was summoned, was invited, was called to and exhorted and cheered and encouraged, was excited and fomented, was exhorted, was demanded and required, was comforted and consoled` | 24:67 |
| παρθένος | `maid` | `maid and maiden and virgin and girl` | 24:16 |
| παρθένος | `the maid` | `the maid and maiden and virgin and girl` | 24:14, 24:16, 24:43, 24:55 |
| παροικέω | `I dwell beside` | `I dwell beside, I dwell along the coast of, I live near, I dwell among, I lie near, I live in and sojourn` | 24:37 |
| πατήρ | `to the father` | `to the father, to the grandfather` | 24:23 |
| παύω | `they may take their rest` | `they may take their rest and rest and cease and have done, they may leave off from and rest and cease from, they may be at rest, they may leave off doing` | 24:14 |
| παῖς | `child` | `child, son, daughter, grandchild, boy and youth and lad, girl and maiden, slave and servant and man and maid` | 24:34 |
| περιβάλλω | `threw round herself` | `threw round herself, put on, threw round herself for defence, built round, surrounded and enclosed for herself, brought into her power and aimed at, cloked and veiled` | 24:65 |
| περιτίθημι | `I placed round` | `I placed round, I bestowed and conferred upon` | 24:47 |
| πορεύομαι | `I am driven` | `I am driven, I am carried, I go, I walk, I march, I go across and pass` | 24:42 |
| πορεύομαι | `I will be driven` | `I will be driven, I will be carried, I will go, I will walk, I will march, I will go across and pass` | 24:58 |
| πορεύομαι | `was being driven` | `was being driven, was being carried, was going, was walking, was marching, was going across and passing` | 24:62 |
| πορεύομαι | `will be driven` | `will be driven, will be carried, will go, will walk, will march, will go across and pass` | 24:39 |
| πορεύομαι | `you will be driven` | `you will be driven, you will be carried, you will go, you will walk, you will march, you will go across and pass` | 24:4, 24:38, 24:58 |
| ποτίζω | `I will give to drink` | `I will give to drink, I will water, I will water the cattle` | 24:14, 24:46 |
| ποτίζω | `give to drink` | `give to drink, water, water the cattle` | 24:17, 24:43, 24:45 |
| προσέχω | `hold to` | `hold to and offer, bring to, turn to, turn the mind to, give heed to` | 24:6 |
| προσκυνέω | `I made obeisance` | `I made obeisance, I fell down and worshipped and worshipped and adored, I did reverence to, I made the salam, I prostrated myself before` | 24:48 |
| πρόσταγμα | `the ordinance` | `the ordinance and command` | 24:50 |
| σκεῦος | `vessels` | `vessels, implements of any kind, furniture and house-gear and utensils and chattels, accoutrements and equipment, baggage and luggage, tackling, gear, inanimate objects and things, bodies and vessels` | 24:53 |
| σπεύδω | `having set a-going` | `having set a-going and urged on and hastened and quickened, having sought eagerly and striven after, having promoted zealously and pressed, having pressed on and hastened and exerted herself and striven eagerly, having been eager to do, having been anxious that` | 24:46 |
| σπεύδω | `set a-going` | `set a-going and urged on and hastened and quickened, sought eagerly and strove after, promoted zealously and pressed, pressed on and hastened and exerted herself and strove eagerly, was eager to do, was anxious that` | 24:18, 24:20 |
| συντελέω | `to bring quite to an end` | `to bring quite to an end, to complete, to accomplish, to make up into the whole and into the number` | 24:15, 24:45 |
| τίθημι | `set` | `set, put, place, plant, lay` | 24:2 |
| τίκτω | `the one having been brought into the world` | `the one having been brought into the world, having been brought forth, having been borne and produced` | 24:15 |
| τρέχω | `having run` | `having run, having moved quickly, having run over, having run the risk` | 24:28 |
| φημί | `was declaring` | `was declaring and making known, was saying and affirming and asserting, was thinking and deeming and supposing, was saying yes and affirming, was saying no and denying and refusing` | 24:47 |
| φυλή | `of the race` | `of the race, of the tribe, of the body united by ties of blood and descent, of the clan, of the tribe by local habitation, of the hundred and county, of the contingent furnished by a tribe, of the brigade` | 24:40 |
| φυλή | `race` | `race, tribe, body united by ties of blood and descent, clan, tribe by local habitation, hundred and county, contingent furnished by a tribe, brigade` | 24:41 |
| φυλή | `the race` | `the race, the tribe, the body united by ties of blood and descent, the clan, the tribe by local habitation, the hundred and county, the contingent furnished by a tribe, the brigade` | 24:4, 24:38 |
| χιλιάς | `numbers one thousand` | `numbers one thousand and thousands, very large numbers` | 24:60 |
| χρυσίον | `piece of gold` | `piece of gold, gold, gold coin and money` | 24:35 |
| χρυσοῦς | `golden` | `golden, of gold, decked and inlaid with gold, gilded and gilt, gold-coloured and golden-yellow` | 24:22, 24:53 |
| χρυσοῦς | `of golden` | `of golden, of gold, of decked and inlaid with gold, of gilded and gilt, of gold-coloured and golden-yellow` | 24:22 |
| χόρτασμα | `fodders` | `fodders, forages, foods for men` | 24:25, 24:32 |
| ψέλιον | `armlets` | `armlets, anklets` | 24:22 |
| ψέλιον | `the armlets` | `the armlets, the anklets` | 24:30, 24:47 |
| ἀγαθός | `of the goods` | `of the goods, of the goods of fortune and wealth, of good qualities` | 24:10 |
| ἀγαπάω | `treated with affection` | `treated with affection and caressed and loved and was fond of, regarded with brotherly love, was well pleased and contented with, was content` | 24:67 |
| ἀδελφός | `the sons of the same mother` | `the sons of the same mother, the brothers, the near kinsmen` | 24:55 |
| ἀδολεσχέω | `to talk idly` | `to talk idly and prate` | 24:63 |
| ἀθῷος | `unpunished` | `unpunished, scot-free, free from, unharmed by, not deserving punishment and without fault` | 24:41 |
| ἀκούω, with ἐν τῷ | `in the hearing` | `within, inside of, and by means of the hearing, the having hearing of, the hearing tell of, the knowing by hearsay, the hearkening and giving ear, the listening to and obeying` | 24:52 |
| ἀλήθεια | `of truth` | `of truth, of truth and reality, of truthfulness and sincerity and frankness and candour` | 24:48 |
| ἀλήθεια | `the truth` | `the truth, the truth and reality, the truthfulness and sincerity and frankness and candour` | 24:27 |
| ἀνά + accusative | `up to` | `up to, up along, throughout and in course of and by, at the rate of and apiece, up to and in proportion` | 24:22 |
| ἀναγγέλλω | `carry back tidings of` | `carry back tidings of, report` | 24:23 |
| ἀναλαμβάνω | `having taken up` | `having taken up, having taken into one's hands, having taken on board ship, having taken with one, having taken upon oneself and assumed, having learned by rote, having got back and regained and recovered, having retrieved and made good, having restored and repaired and regained strength and revived, having taken up again and resumed and recollected, having pulled short up and checked and called back, having gained quite over and won over` | 24:61 |
| ἀντιλέγω | `to speak against` | `to speak against, to gainsay, to contradict, to declare in opposition, to answer, to reply, to allege in answer, to speak one against the other and speak in opposition` | 24:50 |
| ἀντλέω | `to bale out bilge-water` | `to bale out bilge-water and bale the ship, to draw water, to exhaust and come to the end of, to squander` | 24:13, 24:20 |
| ἀπέρχομαι | `I may go away` | `I may go away, I may depart from, I may depart, I may depart from life` | 24:54, 24:56 |
| ἀπέρχομαι | `will go away` | `will go away, will depart from, will depart, will depart from life` | 24:55 |
| ἀπαγγέλλω | `bring tidings` | `bring tidings, report, announce, carry a report, relate and narrate` | 24:49 |
| ἀποσάττω | `unsaddled` | `unsaddled and unpacked, stopped up and caulked, stuffed with food` | 24:32 |
| ἀποστέλλω | `will send off` | `will send off, will send away and banish, will despatch, will go away and depart` | 24:7, 24:40 |
| ἀποστρέφω | `I may turn` | `I may turn, I may turn back, I may turn away, I may turn myself about, I may bring back` | 24:5 |
| ἀποστρέφω | `you may turn` | `you may turn, you may turn back, you may turn away, you may turn yourself about, you may bring back` | 24:6, 24:8 |
| ἀρά | `of the prayer` | `of the prayer, of the prayer for evil and curse and imprecation, of the effect of the curse and bane and ruin` | 24:41 |
| ἀργυροῦς | `silver` | `silver and of silver` | 24:53 |
| ἀργύριον | `piece of silver` | `piece of silver and silver coin, money and sum of money and cash, silver` | 24:35 |
| ἄρχων | `to the ruler` | `to the ruler and commander and chief and captain, to the chief magistrate` | 24:2 |
| ἄχυρον | `husks` | `husks and chaff and bran` | 24:25, 24:32 |
| ἐγκαταλείπω | `left behind` | `left behind, left in the lurch, left out and omitted` | 24:27 |
| ἐκκενόω | `emptied out` | `emptied out, left desolate` | 24:20 |
| ἐκπέμπω | `send out` | `send out, send forth from, bring out by calling and call and fetch out, send forth and dispatch, send away and cast out and divorce, send out and send abroad, send forth and give out` | 24:54, 24:56 |
| ἐκπέμπω | `sent out` | `sent out, sent forth from, brought out by calling and called and fetched out, sent forth and dispatched, sent away and cast out and divorced, sent out and sent abroad, sent forth and gave out` | 24:59 |
| ἐκπορεύομαι | `go out` | `go out, go forth, march out` | 24:11, 24:13 |
| ἐκπορεύομαι | `was going out` | `was going out, was going forth, was marching out` | 24:15, 24:45 |
| ἐκφέρω | `having carried out of` | `having carried out of, having carried out, having carried off, having carried out of the sea and thrown ashore, having brought forth, having brought forth and produced, having brought about and accomplished, having brought out and published, having delivered, having brought forward, having disclosed and told and betrayed, having put forth and exerted, having borne the marks of, having carried to a certain point, having shot forth, having run away, having come to fulfilment and come to an end, having come to land and been cast ashore, having been carried beyond bounds and carried away` | 24:53 |
| ἐμός | `the mine` | `the mine, the to me and relating to me and against me, the by me` | 24:41 |
| ἐξέρχομαι | `you went out of` | `you went out of, you came out, you went away and marched off, you went forth` | 24:5 |
| ἐπερωτάω | `inquired of` | `inquired of and questioned and consulted, asked and asked about and put the question` | 24:23 |
| ἐπιβαίνω | `went upon` | `went upon, set foot on and trod and walked upon, got upon and mounted on, arrived at, indulged in and observed, mounted upon and got upon, set upon and attacked and assaulted, lit upon and went on to and entered, attacked, mounted, got a footing, stepped onwards and advanced` | 24:61 |
| ἐπικλίνω | `put to` | `put to, bend towards, incline towards` | 24:14 |
| ἐπιστρέφω | `I may turn about` | `I may turn about and turn round, I may return, I may turn towards, I may correct and make to repent` | 24:49 |
| ἐπιτρέχω | `ran upon` | `ran upon, made an assault upon, ran after, ran over and grazed the surface, was spread over, overran, ran over and treated lightly of, ran close after` | 24:17 |
| ἐρωτάω | `I asked` | `I asked, I asked about, I enquired of and questioned, I begged and solicited` | 24:47 |
| ἐρωτάω | `let us ask` | `let us ask, let us ask about, let us enquire of and question, let us beg and solicit` | 24:57 |
| ἐσθίω | `I may eat` | `I may eat, I may eat of` | 24:33 |
| ἐφίστημι | `I have stood upon` | `I have stood upon and stand so, I have been imposed upon, I have stood on the top and surface, I have been set over and been in authority, I have stood by and near and appeared to, I have stood against and opposed, I have come upon by surprise and impended and been at hand, I have halted and stopped, I have fixed my mind on and given my attention to` | 24:43 |
| ἑτοιμάζω | `I have made ready` | `I have made ready and it stands made ready, I have got ready and it stands got ready, I have prepared and it stands prepared, I have provided and it stands provided` | 24:31 |
| ἑτοιμάζω | `made ready` | `made ready, got ready, prepared, provided` | 24:44 |
| ἑτοιμάζω | `you made ready` | `you made ready, you got ready, you prepared, you provided` | 24:14 |
| ἔμπροσθεν | `before` | `before and in front of` | 24:7 |
| ἔρημος | `of the desert part` | `of the desert part, of the desolate and lone and lonely and lonesome and solitary, of the desolate and helpless, of the reft of and void, of the destitute of, of the wanting and without, of the undefended` | 24:62 |
| ἔρχομαι | `you may come` | `you may come, you may go, you may go back and return, you may be going to and intend, you may come within a little of and be near` | 24:41 |
| ἔχω | `having` | `having, holding, possessing, keeping, dwelling in and inhabiting, holding fast, bearing up against and supporting` | 24:15, 24:45 |
| ἱματισμός | `clothing` | `clothing and apparel` | 24:53 |
| ἵστημι | `I have been set` | `I have been set and stand so, I have been placed and stood, I have been there, I have been in a state and condition, I have lain and been situated, I have stood still and stopped and halted, I have stood idle, I have stopped and ceased and been at rest, I have stood firm, I have stood up and risen up, I have arisen and begun` | 24:13 |
| ἵστημι | `of having been set` | `of having been set and standing so, of having been placed and stood, of having been there, of having been in a state and condition, of having lain and been situated, of having stood still and stopped and halted, of having stood idle, of having stopped and ceased and been at rest, of having stood firm, of having stood up and risen up, of having arisen and begun` | 24:30 |
| ἵστημι | `you have been set` | `you have been set and stand so, you have been placed and stood, you have been there, you have been in a state and condition, you have lain and been situated, you have stood still and stopped and halted, you have stood idle, you have stopped and ceased and been at rest, you have stood firm, you have stood up and risen up, you have arisen and begun` | 24:31 |
| ὀψέ | `after a long time` | `after a long time, late, late in the day and at even` | 24:11 |
| ὁδός, with ἐν | `in way` | `within, inside of, and by means of way, path, track, road, highway, course, journey, manner and method` | 24:48 |
| ὁλκή | `drawing` | `drawing, dragging, tugging, drawing on and towards, attraction and force of attraction` | 24:22 |
| ὁλκή | `of drawing` | `of drawing, of dragging, of tugging, of drawing on and towards, of attraction and force of attraction` | 24:22 |
| ὁρκίζω | `made swear` | `made swear` | 24:37 |
| ὄψις | `with the look` | `with the look, with the appearance, with the aspect, with the sight, with the vision and apparition, with the eyesight and vision, with the view and sight` | 24:16 |
| ὅρασις | `of the seeing` | `of the seeing and act of sight, of the vision` | 24:62 |
| ὑδρία | `of the water-pot` | `of the water-pot and pitcher and urn, of the vessel and the pot of money, of the balloting urn, of the cinerary urn` | 24:17, 24:43 |
| ὑδρία | `the water-pot` | `the water-pot and pitcher and urn, the vessel and the pot of money, the balloting urn, the cinerary urn` | 24:14, 24:15, 24:16, 24:18, 24:20, 24:45, 24:46 |
| ὑδρεύω | `I will draw water for myself` | `I will draw water for myself and fetch water` | 24:19, 24:44 |
| ὑδρεύω | `drew water for herself` | `drew water for herself and fetched water` | 24:20, 24:45 |
| ὑδρεύω | `the ones drawing water for themselves` | `the ones drawing water for themselves and fetching water` | 24:11 |
| ὑδρεύω | `to draw water for oneself` | `to draw water for oneself and fetch water` | 24:43 |
| ὦμος | `of the shoulders with the upper arm` | `of the shoulders with the upper arm, of the shoulders` | 24:15, 24:45 |
| ῥῆμα | `of that which is said` | `of that which is said and spoken, of the word, of the saying, of the phrase, of the subject of speech and the thing, of the verb` | 24:9 |
| ῥῆμα | `of the things which are said` | `of the things which are said and spoken, of the words, of the sayings, of the phrases, of the subjects of speech and things, of the verbs` | 24:52 |

### Words new in GEN 23

- μνημεῖον — Middle Liddell's first sense carries its English only inside the Latin, *monimentum,
  any memorial, remembrance, record*, and tags only the second, *a monument*; LSJ's senses stand,
  *memorial, remembrance, record*, then *tomb, monument*. 23:6, 23:9.
- θάπτω — Middle Liddell's one sense is *to pay the last dues to a corpse, to honour with funeral
  rites*, and then *to bury, inter*: `I will pay the last dues to a corpse`. 23:4–19.
- τῷ τοῦ Σααρ — the article used as a noun with the genitive, *the one of Saar*: `to the of`, one
  English article for each Greek one. 23:8.
- Genitive absolute, ἀκουόντων τῶν υἱῶν Χετ — `of hearing`, as καθημένου at 18:1. 23:10.
- κύκλῳ — the adverbial dative, filed inside κύκλος: *in a circle* or *ring, round about*. 23:17.
- A verse that opens with direct speech prints its capital as the first word of the verse, so it is
  not listed in `speech`: Πάροικος (23:4), Μή (23:6), Παρʼ (23:11), Οὐχί (23:15).
- Names: Αρβοκ `(Αρβοκ, for Hebrew Qiryat ʾarbaʿ, "city of Arba" or "city of four")`; Χεβρων; Χετ,
  whose sons are the Hittites; Εφρων, son of Σααρ; Χετταῖος `(Χετταῖος, the man of Χετ, Heth;
  Hebrew Ḥittî)`. 23:2–10.
- One sense each in GEN 23, so plain text: παρεπίδημος `sojourning in a strange place` (23:4, LSJ);
  δένδρον `tree` (23:17).

| lemma | headword | chain | used |
| --- | --- | --- | --- |
| δίδραχμον | `of coins of two drachms` | `of coins of two drachms, of half-shekels` | 23:15 |
| δίδωμι | `let give` | `let give, let grant, let provide, let give over and deliver up` | 23:9 |
| διπλοῦς | `twofold` | `twofold and double, double-minded and treacherous` | 23:9, 23:19 |
| διπλοῦς, with ἐν | `in the twofold` | `within, inside of, and by means of the twofold and double, the double-minded and treacherous` | 23:17 |
| δόκιμος | `of assayed` | `of assayed and examined and tested, of approved and esteemed and notable, of excellent and notable and considerable` | 23:16 |
| εἰσπορεύομαι | `of the ones going into` | `of the ones going into and entering` | 23:10, 23:18 |
| ζωή | `the life` | `the life, the means of life and substance, the existence, the way of life` | 23:1 |
| θάπτω | `I will pay the last dues to a corpse` | `I will pay the last dues to a corpse and honour with funeral rites, I will bury and inter` | 23:4, 23:13 |
| θάπτω | `paid the last dues to a corpse` | `paid the last dues to a corpse and honoured with funeral rites, buried and interred` | 23:19 |
| θάπτω | `pay the last dues to a corpse` | `pay the last dues to a corpse and honour with funeral rites, bury and inter` | 23:6, 23:11, 23:15 |
| θάπτω | `to pay the last dues to a corpse` | `to pay the last dues to a corpse and honour with funeral rites, to bury and inter` | 23:6, 23:8 |
| κοίλωμα, with ἐν | `in the hollow` | `within, inside of, and by means of the hollow and cavity` | 23:2 |
| κτῆσις | `acquisition` | `acquisition, possession, possessions and property` | 23:4, 23:9, 23:18, 23:20 |
| κυρόω | `was made valid` | `was made valid, was confirmed, was ratified, was determined, was decided` | 23:20 |
| κωλύω | `will let` | `will let, will hinder, will check, will prevent, will impede` | 23:6 |
| κόπτω | `to beat one's breast` | `to beat one's breast, to mourn for` | 23:2 |
| κύκλῳ | `in a circle` | `in a circle, in a ring and round about` | 23:17 |
| λαλέω | `talk` | `talk, chat, prattle, babble, say, talk of, speak, chatter, chirp` | 23:8 |
| λαός | `of the people` | `of the people, of the men, of the soldiers, of the land-army, of the common men, of the folk, of the Jews, of the Christians` | 23:12, 23:13 |
| λαός | `to the people` | `to the people, to the men, to the soldiers, to the land-army, to the common men, to the folk, to the Jews, to the Christians` | 23:7 |
| μέρος, with ἐν | `in part` | `within, inside of, and by means of part, share, one's portion and heritage and lot, one's turn, the part one takes in and the part assigned, division` | 23:9 |
| μνημεῖον | `memorials` | `memorials, remembrances, records, tombs and monuments` | 23:6 |
| μνημεῖον | `of memorial` | `of memorial, of remembrance, of record, of monument` | 23:9 |
| μνημεῖον | `the memorial` | `the memorial, the remembrance, the record, the monument` | 23:6 |
| νεκρός | `of the dead body` | `of the dead body and corpse, of the dead` | 23:3 |
| νεκρός | `the dead body` | `the dead body and corpse, the dead` | 23:4, 23:6, 23:8, 23:11, 23:13, 23:15 |
| πενθέω | `to bewail` | `to bewail, to lament, to mourn for` | 23:2 |
| πολίτης | `of the members of a city` | `of the members of a city and state, of the citizens and freemen` | 23:11 |
| πρός + genitive | `from` | `from, from forth, on the side and quarter of, before and in presence of and in the eyes of, before and by, from and on the side of, proceeding from, from and at the hand of, by means and agency of, dependent on, under the protection of, at the beck of, on the side of and in favour of, fitting and suitable, befitting, like, agreeable to` | 23:13 |
| σπήλαιον | `grotto` | `grotto, cave, cavern` | 23:17 |
| σπήλαιον | `the grotto` | `the grotto and cave and cavern` | 23:9, 23:11, 23:17, 23:20 |
| τάφος | `of a burial` | `of a burial and funeral, of the act of burying, of the grave and tomb` | 23:4, 23:20 |
| ψυχή | `to the breath` | `to the breath, to the life, to the spirit, to life and death, to the ghost, to the departed soul` | 23:8 |
| ἀγρός | `the field` | `the field, the lands, the farm, the country` | 23:11, 23:17, 23:20 |
| ἀγρός, with ἐν | `in the field` | `within, inside of, and by means of the field, the lands, the farm, the country` | 23:17 |
| ἀκούω | `I have heard` | `I have heard and it stands so, I have had hearing of and it stands so, I have heard tell of and it stands so, I have known by hearsay and it stands so, I have hearkened and given ear and it stands so, I have listened to and obeyed and it stands so` | 23:15 |
| ἀκούω | `of hearing` | `of hearing, of having hearing of, of hearing tell of, of knowing by hearsay, of hearkening and giving ear, of listening to and obeying` | 23:10 |
| ἀποκαθίστημι | `re-established` | `re-established and restored and reinstated` | 23:16 |
| ἀποκρίνομαι | `gave answer to` | `gave answer to and replied, answered, answered charges and defended himself` | 23:14 |
| ἀποκρίνομαι | `gave answer to` | `gave answer to and replied, answered, answered charges and defended themselves` | 23:5 |
| ἀργύριον | `of a piece of silver` | `of a piece of silver and silver coin, of money and a sum of money and cash, of silver` | 23:9, 23:15, 23:16 |
| ἀργύριον | `the piece of silver` | `the piece of silver and silver coin, the money and sum of money and cash, the silver` | 23:13, 23:16 |
| ἄξιος | `weighing as much` | `weighing as much, of like value, worth as much as, worthy and goodly, of a proper value and cheap, deserved and meet and due, sufficient for, worthy of and deserving and meet for` | 23:9 |
| ἐκλεκτός, with ἐν | `in the picked out` | `within, inside of, and by means of the picked out and select` | 23:6 |
| ἔμπορος | `to ones who go on shipboard as passengers` | `to ones who go on shipboard as passengers, to any on a journey and travellers and wanderers, to merchants and traders` | 23:16 |
| ἵστημι | `was set` | `was set, was placed and stood, was there, was in a state and condition, lay and was situated, stood still and stopped and halted, stood idle, stopped and ceased and was at rest, stood firm, stood up and rose up, arose and began` | 23:17 |
| ὅριον, with ἐν | `in the boundaries` | `within, inside of, and by means of the boundaries and limits, the borders, the frontier` | 23:17 |

### Words new in GEN 22

- ὁ δὲ εἶπεν — the article as a pronoun, `he`, as at 4:9. 22:1, 22:7, 22:11.
- ἀγαπητός — first *beloved*, of an *only* son, the entry says; the Hebrew *yĕḥîd*, *only one*,
  stands behind it. 22:2, 22:12, 22:16.
- τέκνον in the vocative takes the entry's *my son, my child*, which belongs to address. 22:7, 22:8.
- σαβεκ — a transliteration of Hebrew *sĕbak*, *thicket*, printed in lower case: a name here, as
  τὰ χερουβιμ at 3:24. 22:13.
- κατέχω in the passive — the active's *to hold fast* first, the passive's *to be held down, to be
  bound, kept under* and *to be detained* last. 22:13.
- ἦ μήν — ἦ, *in truth, truly, verily*; μήν, whose opening *a Particle used to strengthen
  asseverations* is a description, takes its first tag, *now verily, full surely*, from καὶ μήν.
  22:17.
- ὑπεναντίος as a noun, οἱ ὑπεναντίοι — the entry's *the enemy*, one translation, plain. 22:17.
- τῆς ἐμῆς φωνῆς — ἐμός, first *mine*, with the article, and φωνή after it, each with the case's
  `of`. 22:18.
- πρόβατον singular — `the thing that walks forward`, the chain of GEN 12:16 in the singular. 22:7.
- One sense each in GEN 22, so plain text: ὁλοκάρπωσις `whole burnt-offering` (22:2–13), as at 8:20;
  τρίτος `the third` (22:4); θυσιαστήριον `an altar`, `the altar` (22:9); δεύτερος `second` (22:15);
  ἐμαυτοῦ `of myself` (22:16); ἐνευλογέομαι `will be blessed in` (22:18); πρωτότοκος `first-born`
  (22:21); ὀκτώ `eight` (22:23).

| lemma | headword | chain | used |
| --- | --- | --- | --- |
| αὐτοῦ | `at the very place` | `at the very place and just here and just there` | 22:5 |
| διέρχομαι | `we will go through` | `we will go through and pass through, we will go through in detail` | 22:5 |
| εὐλογέω | `speaking well of` | `speaking well of, praising, honouring, blessing` | 22:17 |
| κέρας | `of the horns of an animal` | `of the horns of an animal, of the horn, of the things made of horn, of the bows, of the horns for blowing, of the flutes, of the drinking-horns, of the horn guards and pipes, of the horn points, of the arms and branches of a river, of the wings of an army and fleet, of the any projections, of the mountain-peaks` | 22:13 |
| καθίζω | `make to sit down` | `make to sit down and seat, set and place, encamp, set up, sit down and be seated and take your seat, settle and sink in` | 22:5 |
| κατέχω | `being held fast` | `being held fast, being held back and withheld, being checked and restrained and controlled and bridled, being detained, being possessed and occupied, being filled, being occupied and spread over and covered, being confined and covered, being held down and overpowered and oppressed and afflicted, being held down and bound and kept under, being detained and staying and stopping and tarrying` | 22:13 |
| κριός | `the ram` | `the ram, the battering-ram` | 22:13 |
| λέγω | `I may say` | `I may say, I may speak, I may declare, I may call by name, I may tell` | 22:2 |
| λέγω | `having said` | `having said, having spoken, having declared, having called by name, having told` | 22:7 |
| λέγω | `they may say` | `they may say, they may speak, they may declare, they may call by name, they may tell` | 22:14 |
| λαμβάνω | `to take` | `to take, to receive, to take hold of and grasp and seize` | 22:10 |
| μάχαιρα | `the large knife` | `the large knife and dirk, the knife for cutting up, the short sword and dagger, the sabre and bent sword, the rasor` | 22:6, 22:10 |
| μήν | `now verily` | `now verily, full surely, truly, of a truth, then, of course and naturally so, well` | 22:17 |
| ξύλον | `of the woods` | `of the woods, of the firewood, of the timbers, of the pieces of wood and posts, of the sticks` | 22:9 |
| ξύλον | `the woods` | `the woods, the firewood, the timbers, the pieces of wood and posts, the sticks` | 22:6, 22:7, 22:9 |
| ξύλον | `woods` | `woods, firewood, timbers, pieces of wood and posts, sticks` | 22:3 |
| παιδάριον | `the young little boy` | `the young little boy, the young slave` | 22:5, 22:12 |
| παλλακή | `the concubine` | `the concubine and mistress` | 22:24 |
| παραλαμβάνω | `received from` | `received from, inherited, took upon himself and undertook, took in pledge, took by force and treachery and got possession of, received by hearsay and report and ascertained, took up and caught up, took to himself and associated with himself, invited, waited for and intercepted, took prisoner` | 22:3 |
| παῖς | `to the children` | `to the children, to the sons, to the daughters, to the grandchildren, to the boys and youths and lads, to the girls and maidens, to the slaves and servants and men and maids` | 22:5 |
| πειράζω | `was making proof` | `was making proof and trial of, was attempting, was trying and tempting, was putting to the test` | 22:1 |
| πορεύομαι | `be driven` | `be driven, be carried, go, walk, march, go across and pass` | 22:2 |
| προσκυνέω | `having made obeisance` | `having made obeisance, having fallen down and worshipped and worshipped and adored, having done reverence to, having made the salam, having prostrated themselves before` | 22:5 |
| πρόβατον | `the thing that walks forward` | `the thing that walks forward, the cattle, the flocks and herds, the horses, the small cattle, the sheep` | 22:7 |
| πρόβατον | `thing that walks forward` | `thing that walks forward, cattle, flocks and herds, horses, small cattle, sheep` | 22:8 |
| πῦρ | `the fire` | `the fire, the funeral-fire, the fire of the hearth` | 22:6, 22:7 |
| σπέρμα, with ἐν | `in the that which is sown` | `within, inside of, and by means of the that which is sown, the seed, the germ and origin and element, the offspring and issue, the race and descent` | 22:18 |
| συμποδίζω | `having tied the feet together` | `having tied the feet together, having bound hand and foot, having entangled` | 22:9 |
| σφάζω | `to slay` | `to slay, to slaughter, to slaughter by cutting the throat, to slaughter victims for sacrifice, to kill` | 22:10 |
| σχίζω | `having split` | `having split and cleaved, having parted and separated` | 22:3 |
| τέκνον | `that which is borne` | `that which is borne, the born, a child, my son and my child, the young` | 22:7, 22:8 |
| τίκτω | `has brought into the world` | `has brought into the world and it stands so, has brought forth and it stands so, has borne and it stands so, has begotten and it stands so, has produced and yielded and it stands so` | 22:20 |
| φείδομαι | `you spared` | `you spared, you did not destroy, you were merciful, you refrained from using and used sparingly, you were sparing and were thrifty and lived thriftily, you drew back from, you ceased, you forbore` | 22:12, 22:16 |
| φοβέομαι | `you are put to flight` | `you are put to flight, you flee affrighted, you flee, you are seized with fear, you are affrighted, you fear` | 22:12 |
| φυτόν, with ἐν | `in that which has grown` | `within, inside of, and by means of that which has grown and a plant and a tree, a creature, a descendant and child` | 22:13 |
| φωνή | `of sound` | `of sound and tone, of sound of the voice, of cry, of faculty of speech and discourse, of language, of saying` | 22:18 |
| χείρ | `hand` | `hand, hand and arm, arm` | 22:6 |
| χεῖλος | `the lip` | `the lip, the bill and beak, the edge and brink and brim and rim` | 22:17 |
| ἀγαπάω | `you treated with affection` | `you treated with affection and caressed and loved and were fond of, you regarded with brotherly love, you were well pleased and contented with, you were content` | 22:2 |
| ἀγαπητός | `beloved` | `beloved, only, worthy of love and loveable and dear, to be acquiesced in` | 22:2, 22:12, 22:16 |
| ἀναγγέλλω | `was carried back tidings of` | `was carried back tidings of, was reported` | 22:20 |
| ἀναστρέφω | `we may turn upside down` | `we may turn upside down, we may upset, we may turn back and bring back, we may rally, we may turn back and return and retire, we may dwell, we may conduct ourselves, we may revolve, we may face about` | 22:5 |
| ἀναφέρω | `bring up` | `bring up, carry up, carry up the country, take with you, pour forth, heave and utter, uphold and take upon yourself, offer and contribute, lead up, carry back and recover, bring back and report, trace up` | 22:2 |
| ἀποστρέφω | `was turned` | `was turned, was turned back, was turned away, was brought back, turned himself about` | 22:19 |
| ἐκτείνω | `stretched out` | `stretched out, spread out, put forth` | 22:10 |
| ἐμός | `of the mine` | `of the mine, of the to me and relating to me and against me, of the by me` | 22:18 |
| ἐπιβάλλω | `you may throw` | `you may throw and cast upon, you may lay on, you may affix, you may add, you may mention, you may throw yourself upon and go straight towards, you may fall upon and against, you may apply yourself to and devote yourself to, you may give your attention to and think on, you may follow and come next, you may belong to and fall to` | 22:12 |
| ἐπισάττω | `piled a load upon` | `piled a load upon, saddled` | 22:3 |
| ἦ | `in truth` | `in truth and truly and verily and of a surety, can it be` | 22:17 |
| ὁράω | `will see` | `will see, will perceive, will behold, will look at` | 22:8 |
| ὄμνυμι | `I swore` | `I swore, I swore to and affirmed and confirmed by oath, I swore that I would, I swore by` | 22:16 |
| ὄνος | `of the ass` | `of the ass, of the beast of burden, of the windlass and pulley, of the upper millstone, of the beaker and wine-cup` | 22:5 |
| ὄνος | `the ass` | `the ass, the beast of burden, the windlass and pulley, the upper millstone, the beaker and wine-cup` | 22:3 |
| ὑπακούω | `you listened` | `you listened and hearkened and gave ear, you made answer when called, you hearkened to and gave ear to and attended to, you answered, you answered to a charge, you submitted to, you yielded to and complied with, you gave way and submitted and complied, you answered one's expectations and succeeded, you were subject` | 22:18 |

### Words new in GEN 21

- ἐπισκέπτομαι — Middle Liddell's entry reads *a pres., which furnishes its tenses to ἐπισκοπέω*;
  that entry's senses, first *to look upon* or *at, inspect, observe*, then *to visit*. 21:1.
- φαίνω in the passive — the active's *to bring to light, make to appear* first, and the entry's
  *Pass. to come to light, be seen, appear* last: `was brought to light`. 21:11.
- πλανάω in the passive — likewise, the active's *to make to wander* first, the passive's *to
  wander, roam about, stray* last. 21:14.
- ὦμος — tagged in Middle Liddell only in Latin; LSJ, from the omega file, *the shoulder with the
  upper arm*. 21:14.
- Φρέαρ ὁρκισμοῦ — the second name the verse gives a well, glossed as a name as at 16:14:
  `(Φρέαρ, "a well", the first word of the name the verse gives the place, for Hebrew Bĕʾēr
  šebaʿ)`; ὁρκισμός after it plain. 21:31.
- Θεὸς αἰώνιος — the capital Rahlfs prints for the name called upon, listed in `speech`; θεός
  anarthrous, qualitative, as at 17:7. 21:33.
- The perfect ἐπακήκοεν, `has listened and it stands so` (21:17).
- One sense each in GEN 21, so plain text: γῆρας `the old age` (21:2, 21:7); ἀπογαλακτίζω `was weaned
  from the mother's milk` (21:8, LSJ); νυμφαγωγός `the leader of the bride`, ἀρχιστράτηγος `the
  commander-in-chief` (21:22, 21:32); ἀμνάς `lambs` (21:28–30); ὁρκισμός `of administration of an
  oath` (21:31).

| lemma | headword | chain | used |
| --- | --- | --- | --- |
| αὐξάνω | `was made large` | `was made large and increased and augmented, was increased in power and strengthened and exalted and aggrandised, was promoted to honour and glorified and magnified, grew and waxed and increased, grew up` | 21:8, 21:20 |
| βολή | `a throw` | `a throw, the stroke and wound, a glance` | 21:16 |
| γέλως | `laughter` | `laughter, occasion of laughter and matter for laughter` | 21:6 |
| γίνομαι | `having come into being` | `having come to be, having arisen, having been brought into existence` | 21:3 |
| διατίθεμαι | `arranged as they liked` | `arranged as they liked and disposed of, disposed of their property and devised it by will, set out for sale and disposed of, arranged mutually, made a covenant with, settled with` | 21:27, 21:32 |
| δοχή | `a receptacle` | `a receptacle, a reception and entertainment` | 21:8 |
| δύναμις | `of the power` | `of the power, of the might, of the strength, of the ability, of the authority, of the force for war and forces, of the quantity, of the faculty and capacity, of the force and meaning, of the worth and value` | 21:22, 21:32 |
| εἰσακούω | `hearkened` | `hearkened and gave ear to, heard, hearkened to and gave heed to` | 21:17 |
| εἷς | `of one` | `of one, of a single one and one alone` | 21:15 |
| θάνατος | `the death` | `the death, the death threatened, the sentence of death` | 21:16 |
| θηλάζω | `suckles` | `suckles, sucks` | 21:7 |
| καθίζω | `made to sit down` | `made to sit down and seated, set and placed, encamped, set up, sat down and was seated and took her seat, settled and sank in` | 21:16 |
| κλαίω | `wept` | `wept, lamented, wailed, wept for` | 21:16 |
| κρατέω | `be strong` | `be strong and mighty and powerful, rule and hold sway and be sovereign, rule among, be lord and master of and ruler over, conquer and prevail and get the upper hand, prevail and become current, prevail over, surpass and go beyond, conquer and master and outdo and surpass, become master of and get possession of, lay hold of, seize and hold fast, control and command` | 21:18 |
| λέγω | `may say` | `may say, may speak, may declare, may call by name, may tell` | 21:12 |
| μακρόθεν | `from afar` | `from afar, from long since` | 21:16 |
| μαρτύριον | `a testimony` | `a testimony and proof` | 21:30 |
| πίμπλημι | `filled full of` | `filled full of, filled with, filled up, filled, filled and discharged` | 21:19 |
| παίζω | `playing like a child` | `playing like a child, sporting, playing, dancing, sporting and jesting and joking, making sport of and mocking, playing with` | 21:9 |
| παιδίον | `of the young child` | `of the young child, of the slave-lad` | 21:12, 21:16, 21:17, 21:20 |
| παιδίον | `the young child` | `the young child, the slave-lad` | 21:8, 21:14, 21:15, 21:16, 21:18, 21:19 |
| παιδίσκη | `of the young girl` | `of the young girl and maiden, of the young slave and courtesan` | 21:10, 21:12, 21:13 |
| παροικέω | `you dwelt beside` | `you dwelt beside, you dwelt along the coast of, you lived near, you dwelt among, you lay near, you lived in and sojourned` | 21:23 |
| πλανάω | `was being made to wander` | `was being made to wander and led wandering about, was being led from the subject, was being led astray and misled and deceived, was wandering and roaming about and straying, was wandering over, was wandering abroad, was wandering and digressing, was wandering in mind and at a loss` | 21:14 |
| πρᾶγμα | `that which has been done` | `that which has been done and a deed and an act, anything necessary and expedient, a thing of consequence and importance, an action and affair, the thing and the business` | 21:26 |
| σκληρός | `hard` | `hard, harsh and crashing, stiff and unyielding, stiff and sturdy, austere and severe` | 21:11, 21:12 |
| συγχαίρω | `will rejoice with` | `will rejoice with and take part in joy, will wish joy and congratulate` | 21:6 |
| σός | `thy` | `thy and thine` | 21:13 |
| τίκτω | `I brought into the world` | `I brought into the world, I brought forth, I bore, I begot, I produced and yielded` | 21:7 |
| τοξότης | `a bowman` | `a bowman and archer, the Archer and Sagittarius, the city-guard` | 21:20 |
| τόξον | `of bow` | `of bow, of bow and arrows, of rays` | 21:16 |
| φαίνω | `was brought to light` | `was brought to light and made to appear, was shown forth and made known and revealed and disclosed and shown, was made clear and explained and expounded, was informed against and indicted and impeached, was proclaimed, came to light and was seen and appeared, shone brightly, came into being, appeared to be, was manifest` | 21:11 |
| φρέαρ | `a well` | `a well, a tank and cistern and reservoir, an oil jar` | 21:19 |
| φρέαρ | `of the wells` | `of the wells, of the tanks and cisterns and reservoirs, of the oil jars` | 21:25 |
| φρέαρ | `to the well` | `to the well, to the tank and cistern and reservoir, to the oil jar` | 21:33 |
| φρέαρ, with ἐν | `in the well` | `within, inside of, and by means of the well, the tank and cistern and reservoir, the oil jar` | 21:32 |
| χείρ | `with the hand` | `with the hand, with the hand and arm, with the arm` | 21:18 |
| ἀδικέω | `to do wrong` | `to do wrong, to do one wrong and wrong and injure, to spoil and damage` | 21:23 |
| ἀκούω | `may hear` | `may hear, may have hearing of, may hear tell of, may know by hearsay, may hearken and give ear, may listen to and obey` | 21:6 |
| ἀμφότερος | `each` | `each, both of two` | 21:27, 21:31 |
| ἀναβοάω | `having shouted aloud` | `having shouted aloud and uttered a loud cry, having called out, having cried out, having wailed aloud over, having called on` | 21:16 |
| ἀναγγέλλω | `will carry back tidings of` | `will carry back tidings of, will report` | 21:7 |
| ἀπέρχομαι | `having gone away` | `having gone away, having departed from, having departed, having departed from life` | 21:14, 21:16 |
| ἀσκός | `a leathern-bag` | `a leathern-bag and wine-skin, a bladder` | 21:14 |
| ἀσκός | `of the leathern-bag` | `of the leathern-bag and wine-skin, of the bladder` | 21:15 |
| ἀσκός | `the leathern-bag` | `the leathern-bag and wine-skin, the bladder` | 21:19 |
| ἀφαιρέω | `took away for themselves` | `took away for themselves and took away, prevented and hindered from` | 21:25 |
| ἄρουρα | `tilled land` | `tilled land, arable land and seed-land and cornland, land and earth, a woman as bearing children, a measure of land` | 21:33 |
| ἐκβάλλω | `throw` | `throw, cast out of, throw out, cast out and banish, depose, throw away and reject` | 21:10 |
| ἐλάτη | `of silver fir` | `of silver fir, of an oar, of a ship and boat` | 21:15 |
| ἐλέγχω | `disgraced` | `disgraced and put to shame, cross-examined and questioned, censured and accused, brought to the proof and disproved and confuted, brought convincing proof, proved` | 21:25 |
| ἐπακούω | `has listened` | `has listened and it stands so, has hearkened to and heard and it stands so, has given ear and hearkened and it stands so, has obeyed and it stands so` | 21:17 |
| ἐπισκέπτομαι | `looked upon` | `looked upon, looked at, inspected and observed and examined and regarded, watched over, visited, inspected and reviewed, considered and reflected, examined with himself and meditated` | 21:1 |
| ἐπιστρέφω | `turned about` | `turned about and turned round, returned, turned towards, corrected and made to repent` | 21:32 |
| ἐπιτίθημι | `laid` | `laid, put, placed upon, applied, set up, put on, put to and shut, put to and granted and gave besides, added and brought on, imposed and inflicted, dispatched, gave` | 21:14 |
| ἡμέρα | `to day` | `to day, to day-break, to time` | 21:8 |
| ἵστημι | `you made to stand` | `you made to stand, you set, you stopped and stayed and checked, you set up and raised, you established and instituted, you appointed, you weighed` | 21:29 |
| ὀρύσσω | `I dug` | `I dug, I dug up, I dug through and made a canal through, I buried` | 21:30 |
| ὁράω | `I may see` | `I may see, I may perceive, I may behold, I may look at` | 21:16 |
| ὄμνυμι | `I will swear` | `I will swear, I will swear to and affirm and confirm by oath, I will swear that one will, I will swear by` | 21:24 |
| ὄμνυμι | `swear` | `swear, swear to and affirm and confirm by oath, swear that one will, swear by` | 21:23 |
| ὄμνυμι | `swore` | `swore, swore to and affirmed and confirmed by oath, swore that one would, swore by` | 21:31 |
| ὅρκος | `of the object by which one swears` | `of the object by which one swears and witness of an oath, of the oath` | 21:14, 21:32, 21:33 |
| ὦμος | `the shoulder with the upper arm` | `the shoulder with the upper arm, the shoulder` | 21:14 |
| ῥίπτω | `threw` | `threw, cast, hurled, threw and tossed about, cast out, threw off and away, threw away and wasted, cast lots, threw and cast herself down, flung herself` | 21:15 |

### Words new in GEN 20

- κἀγώ — LSJ gives the crasis no gloss, only *crasis for καὶ ἐγώ*; the two words' senses stand,
  `and I`, plain. 20:6.
- μήτρα — Middle Liddell tags nothing but the Latin *matrix*, so LSJ's senses stand, first *womb*.
  20:18.
- δίδραχμον — no Middle Liddell entry; LSJ files it under δίδραχμος, *coin of two drachms*,
  *half-shekel*. 20:14, 20:16.
- προφήτης — its first appearance in the Greek Bible; Middle Liddell is first *one who speaks for a
  God and interprets his will to man, a prophet*, with the New Testament's *an inspired preacher and
  teacher*, *the revealer of God's counsel for the future* last. 20:7.
- The perfect participle with the formula — συνῳκηκυῖα `having dwelt together and standing so`
  (20:3); the perfect πεποίηκας `you have made and it stands made` (20:9).
- ἐν καθαρᾷ καρδίᾳ — ἐν joined to the adjective, καθαρός, the chain of GEN 7:2; καρδία anarthrous
  drops the lexicon's *the*, as γαστήρ at 16:4. 20:5, 20:6.
- τὰ σά — the chain of GEN 14:23, `the thy property`, with the article. 20:7.
- One sense each in GEN 20, so plain text: λίψ `south-west wind` (20:1); ἀδελφή `sister` (20:2,
  20:5, 20:12); χίλιοι `a thousand` (20:14, 20:16); ἀληθεύω `speak truth` (20:16).

| lemma | headword | chain | used |
| --- | --- | --- | --- |
| βασιλεία | `the kingdom` | `the kingdom and dominion, the hereditary monarchy` | 20:9 |
| γινώσκω | `I learned to know` | `I learned to know, I perceived, I marked, I learned, I discerned and distinguished` | 20:6 |
| γινώσκω | `learn to know` | `learn to know, perceive, mark, learn, discern and distinguish` | 20:7 |
| δίδραχμον | `coins of two drachms` | `coins of two drachms, half-shekels` | 20:14, 20:16 |
| δικαιοσύνη, with ἐν | `in righteousness` | `within, inside of, and by means of righteousness and justice` | 20:5 |
| εἰσέρχομαι | `we may go in` | `we may go in, we may go into and enter, we may come into, we may come in, we may come upon` | 20:13 |
| ζάω | `you will live` | `you will live, you will be in full life and strength and fresh and strong` | 20:7 |
| θεοσέβεια | `the service of God` | `the service of God, the fear of God and religiousness` | 20:11 |
| καθαρός, with ἐν | `in clear of dirt` | `within, inside of, and by means of clear of dirt and clean and spotless and unsoiled, clear and open and free, clear from shame and pollution and pure, clear of guilt and defilement and clean and pure, purified, clear of and from, clear of admixture and clear and pure, pure and genuine, without blemish, clear and exact` | 20:5, 20:6 |
| καρδία | `heart` | `heart, stomach` | 20:5, 20:6 |
| κατοικέω | `dwell in` | `dwell in, settle in, colonise, inhabit, settle and dwell, lie and be situate` | 20:15 |
| κινέω | `set in motion` | `set in motion, moved, removed, meddled with, applied, changed and innovated, roused and disturbed, stirred up and aroused and urged on, set agoing and caused and called` | 20:1 |
| λέγω | `I said` | `I said, I spoke, I declared, I called by name, I told` | 20:11, 20:13 |
| λέγω | `to say` | `to say, to speak, to declare, to call by name, to tell` | 20:2 |
| λαμβάνω | `you took` | `you took, you received, you took hold of and grasped and seized` | 20:3 |
| μήτηρ | `of mother` | `of mother, of dam, of source` | 20:12 |
| μήτρα | `womb` | `womb, the cervix including the orifice of the womb, matrix, source and origin, core and heart-wood, diseased condition, queen-wasp` | 20:18 |
| οὖς | `the ears` | `the ears, the handles` | 20:8 |
| παιδίσκη | `the young girls` | `the young girls and maidens, the young slaves and courtesans` | 20:17 |
| παροικέω | `dwelt beside` | `dwelt beside, dwelt along the coast of, lived near, dwelt among, lay near, lived in and sojourned` | 20:1 |
| πατήρ | `of father` | `of father, of grandfather` | 20:12 |
| ποιέω | `will make` | `will make, will do, will produce, will create` | 20:9 |
| ποιέω | `you have made` | `you have made and it stands made, you have done and it stands done, you have produced and it stands produced, you have created and it stands created` | 20:9 |
| προσεύχομαι | `offered prayers` | `offered prayers and vows, addressed in prayer, offered prayers and worshipped, prayed for` | 20:17 |
| προσεύχομαι | `will offer prayers` | `will offer prayers and vows, will address in prayer, will offer prayers and worship, will pray for` | 20:7 |
| προφήτης | `one who speaks for a God and interprets his will` | `one who speaks for a God and interprets his will, a prophet, an interpreter and declarer, an inspired preacher and teacher, the revealer of God's counsel for the future, a predicter of future events` | 20:7 |
| συγκλείω | `shutting` | `shutting and cooping up and hemming in and enclosing, setting together to fight as in the lists, shutting close and closing, locking, closing up, being well linked` | 20:18 |
| συνοικέω | `having dwelt together` | `having dwelt together and standing so, having lived with and standing so, having lived together and cohabited and standing so, having clung closely and standing so, having colonised jointly with and standing so` | 20:3 |
| σός | `the thy property` | `the thy property, the thy interests, the thy and thine and of thee` | 20:7 |
| τιμή | `that which is paid in token of worth` | `that which is paid in token of worth and value, worship and esteem and honour, honour and dignity and lordship, the prerogative, a dignity and office and magistracy, an authority and magistracy, a present of honour and offering, a reward and present, worth and value and price, payment, an estimate, compensation, the penalty, a valuation` | 20:16 |
| τόπος | `place` | `place, local circumstances, position, passage in a book, topic, common-place, occasion and opportunity` | 20:13 |
| τόπος, with ἐν | `in the place` | `within, inside of, and by means of the place, the local circumstances, the position, the passage in a book, the topic, the common-place, the occasion and opportunity` | 20:11 |
| φείδομαι | `I spared` | `I spared, I did not destroy, I was merciful, I refrained from using and used sparingly, I was sparing and was thrifty and lived thriftily, I drew back from, I ceased, I forbore` | 20:6 |
| φοβέομαι | `were put to flight` | `were put to flight, fled affrighted, fled, were seized with fear, were affrighted, feared` | 20:8 |
| χείρ | `of hands` | `of hands, of hands and arms, of arms` | 20:5 |
| ἀγνοέω | `not perceiving` | `not perceiving, not knowing, being ignorant of, going wrong and making a false step` | 20:4 |
| ἀδελφός | `son of the same mother` | `a son of the same mother, a brother, a near kinsman` | 20:5, 20:13 |
| ἀνήρ | `to a man` | `to a man, to a man in the prime of life` | 20:3 |
| ἀποδίδωμι | `gave up` | `gave up, gave back, restored, returned, rendered what is due and paid, returned and rendered and yielded, suffered and allowed, rendered, delivered over and gave up, delivered, rendered and gave in, gave an account of, increased` | 20:14 |
| ἀποδίδωμι | `give up` | `give up, give back, restore, return, render what is due and pay, return and render and yield, suffer and allow, render, deliver over and give up, deliver, render and give in, give an account of, increase` | 20:7 |
| ἀποδίδωμι | `you give up` | `you give up, you give back, you restore, you return, you render what is due and pay, you return and render and yield, you suffer and allow, you render, you deliver over and give up, you deliver, you render and give in, you give an account of, you increase` | 20:7 |
| ἀποθνήσκω | `you die off` | `you die off and die, you are put to death and slain` | 20:3 |
| ἀποκτείνω | `they may kill` | `they may kill and slay, they may condemn to death` | 20:2 |
| ἀφίημι | `I sent forth` | `I sent forth, I discharged, I let go and loose and set free, I let alone and left, I gave up and handed over, I permitted and allowed` | 20:6 |
| ἁμαρτάνω | `to miss the mark` | `to miss the mark, to fail of one's purpose, to go wrong, to err, to sin` | 20:6 |
| ἁμαρτάνω | `we missed the mark` | `we missed the mark, we failed of our purpose, we went wrong, we erred, we sinned` | 20:9 |
| ἁμαρτία | `a failure` | `a failure and fault and sin, guilt and sin` | 20:9 |
| ἄνθρωπος | `to the man` | `to the man, to the human being, to mankind` | 20:7 |
| ἅπτω | `fastened himself to` | `fastened himself to and clung to and hung on by and laid hold of and grasped and touched, engaged in and took part in, laid hold of and disputed, set upon and attacked and assailed, touched and affected, grasped with the senses and apprehended and perceived, came up to and reached and gained` | 20:4 |
| ἅπτω | `to fasten oneself to` | `to fasten oneself to and cling to and hang on by and lay hold of and grasp and touch, to engage in and take part in, to lay hold of and dispute, to set upon and attack and assail, to touch and affect, to grasp with the senses and apprehend and perceive, to come up to and reach and gain` | 20:6 |
| ἐνοράω | `having seen` | `having seen and remarked and observed, having looked at and upon` | 20:10 |
| ἐπάγω | `you brought on` | `you brought on, you brought upon, you set on and urged on, you led on, you brought in and invited, you brought to, you laid on and applied, you brought forward, you added` | 20:9 |
| ἔργον | `work` | `work, business, deeds, action, works of industry and tilled lands` | 20:9 |
| ἰάομαι | `healed` | `healed and cured` | 20:17 |
| ὕπνος | `sleep` | `sleep, slumber, the sleep of death, Sleep` | 20:6 |
| ὕπνος, with ἐν | `in sleep` | `within, inside of, and by means of sleep, slumber, the sleep of death, Sleep` | 20:3 |

### Words new in GEN 19

- ἐν τῷ with the infinitive — `in the sparing` (19:16), `in the rubbing out` and `in the turning
  down` (19:29), `in the falling asleep` (19:33, 19:35): the article inside the ἐν unit and the
  infinitive as a noun in *-ing*, as ἐν τῷ κινῆσαι is `in the setting in motion` at 11:2; the
  infinitive's subject follows, `lord`, `her`.
- σῴζω — filed under σώζω, first *to save, keep*. The passive takes the entry's passive *to come
  safe, escape to* last; the middle imperative σῴζου takes the middle, *to keep* or *preserve for
  oneself*. 19:17, 19:20, 19:22.
- δέομαι — filed under the second δέω, *to lack*; the deponent's senses stand, *to be in want* or
  *need*, *to ask for*, *to beg*. 19:18.
- μᾶλλον — the comparative, filed inside μάλα: *more*, then *more and more, still more*, *much
  more*, *rather*. ἤ — first *or*; its comparative *than, as* follows. 19:9.
- τὰ κακά — κακός as a noun, the entry's substantive *evil, ill*, with *evil words, reproaches*.
  19:19.
- περίοικος, τὴν περίοικον — the singular takes the adjective's *dwelling round*; *neighbours* is the
  plural's. περίχωρος as an adjective after the repeated article, `the round about a place`
  (19:28); as a noun, ἡ περίχωρος, the chain of GEN 13:10 (19:17). 19:25, 19:29.
- γαμβρός — first *any one connected by marriage*; in the plural, `ones connected by marriage`, the
  lexicon's *any* dropped as *a* is. 19:12, 19:14.
- ἀπό + μικρός, ἕως + μέγας — the adjectives as the entry gives them, in the genitive. 19:11.
- The instrumental dative takes `with` — ἀορασίᾳ `with inability to see` (19:11), as θανάτῳ is
  `with death` at 3:4 and τοῖς ὀφθαλμοῖς `with the eyes` at 13:14 and 18:2.
- εἰσσπάομαι — LSJ's one translation, *draw into oneself*, plain text: its *into* is its own,
  not the verse's εἰς left loose (Q19). 19:10.
- Names: Σοδομῖται `(Σοδομῖται, the men of Σόδομα, Sodom)`; Μωαβ, and Μωαβιτῶν `(Μωαβῖται, the
  people of Μωαβ, Moab)`; Αμμαν `(Αμμαν, for Hebrew Ben-ʿammî, "son of my people")`, anchored
  Ammon, the people's name the Greek form matches, and Αμμανιτῶν. The article before a people's
  name is not printed. 19:4, 19:37, 19:38.
- One sense each in GEN 19, so plain text: καταβιάζομαι `was constraining` (19:3); ἄζυμος
  `unleavened` (19:3); νεανίσκος `of a youth` (19:4); προσοίγνυμι `shut` (19:6, LSJ); παραβιάζομαι
  `were using violence to` (19:9); γελοιάζω `to jest` (19:14, LSJ); ἐπισπουδάζω `were making haste
  in`, συναπόλλυμι's middle `you may perish together`, ἀνομία `to the lawlessnesses` (19:15); θεῖον
  `brimstone` (19:24); ἐπαύριον `on the morrow` (19:34, LSJ); χθές `yesterday` (19:34); σήμερον
  `to-day` (19:37, 19:38).

| lemma | headword | chain | used |
| --- | --- | --- | --- |
| γαμβρός | `of the ones connected by marriage` | `of the ones connected by marriage, of the sons-in-law, of the brothers-in-law and sisters' husbands, of the wives' brothers, of the fathers-in-law, of the bridegrooms and wooers and suitors` | 19:14 |
| γαμβρός | `ones connected by marriage` | `ones connected by marriage, sons-in-law, brothers-in-law and sisters' husbands, wives' brothers, fathers-in-law, bridegrooms and wooers and suitors` | 19:12 |
| γαμβρός | `the ones connected by marriage` | `the ones connected by marriage, the sons-in-law, the brothers-in-law and sisters' husbands, the wives' brothers, the fathers-in-law, the bridegrooms and wooers and suitors` | 19:14 |
| γῆ | `to the earth` | `to the earth, to the land, to the ground` | 19:31 |
| δέομαι | `I am in want` | `I am in want and need, I stand in need of, I ask for and from, I beg` | 19:18 |
| δεῦρο | `hither` | `hither, here and on and come on, up to this point, until now and up to this time and hitherto` | 19:32 |
| διασῴζω | `to be preserved through` | `to be preserved through, to be preserved and maintained, to be kept in mind, to come safe through and arrive in safety, to recover` | 19:19 |
| δικαιοσύνη | `the righteousness` | `the righteousness and justice` | 19:19 |
| δοκέω | `thought` | `thought, supposed, imagined, expected, had and formed an opinion, was determined and resolved, seemed and pretended, seemed, seemed good` | 19:14 |
| δοκός | `of the bearing-beams` | `of the bearing-beams, of the balks and beams, of the bars` | 19:8 |
| δύναμαι | `I will be able` | `I will be able and capable and strong enough, I will be powerful and mighty, I will have influence, I will dare and bear, I will pass for, I will be worth, I will be equivalent to, I will signify and mean, I will avail` | 19:19, 19:22 |
| εἰσέρχομαι | `having gone in` | `having gone in, having gone into and entered, having come into, having come in, having come upon` | 19:5, 19:33, 19:34, 19:35 |
| ζάω | `to live` | `to live, to be in full life and strength and fresh and strong` | 19:19 |
| ζητέω | `seeking` | `seeking, seeking for, enquiring for and asking about, searching after and searching out, searching and inquiring into and investigating, requiring and demanding, seeking after and desiring, seeking to, having to seek and feeling the want of` | 19:11 |
| θαυμάζω | `I wondered` | `I wondered, I marvelled, I was astonied, I looked on with wonder and amazement and wondered at and marvelled at, I honoured and admired and worshipped` | 19:21 |
| κάθημαι | `was being seated` | `was being seated, was being seated in court, was sitting still and sitting quiet, was sitting and lying idle, was sitting down and lying, was leading a sedentary life, was being settled` | 19:1, 19:30 |
| κάμινος | `of an oven` | `of an oven and a furnace and a kiln` | 19:28 |
| καθήκω | `has come` | `has come and gone down, comes down to and comes and reaches to, has come to, is meet and fit and proper, belongs to, beseems` | 19:31 |
| κακός | `the evils` | `the evils, the ills, the evil words and reproaches` | 19:19 |
| κακόω | `we will treat ill` | `we will treat ill and maltreat and afflict and distress, we will spoil and ruin, we will suffer ill and be in ill plight and be distressed` | 19:9 |
| καταλαμβάνω | `may seize upon` | `may seize upon and lay hold of, may seize and overpower, may seize with the mind and apprehend and comprehend, may catch and overtake and come up with, may overtake and befall, may surprise and catch and find, may repress and arrest and check, may put an end to, may bind, may force and compel to do` | 19:19 |
| καταλύω | `put down` | `put down and destroy, dissolve and break up, depose, dismiss and disband, neglect, end and bring to an end, break, make peace with, unloose and unyoke, take down, take up your quarters and lodge, go and lodge, take your rest` | 19:2 |
| καταλύω | `we will put down` | `we will put down and destroy, we will dissolve and break up, we will depose, we will dismiss and disband, we will neglect, we will end and bring to an end, we will break, we will make peace with, we will unloose and unyoke, we will take down, we will take up our quarters and lodge, we will go and lodge, we will take our rest` | 19:2 |
| καταστρέφω | `to turn down` | `to turn down and trample on, to turn the soil, to upset and overturn, to subject to oneself and subdue, to turn back and bring back, to turn round and bring to an end, to come to an end and die, to twist up` | 19:21 |
| καταστρέφω | `turned down` | `turned down and trampled on, turned the soil, upset and overturned, subjected to himself and subdued, turned back and brought back, turned round and brought to an end, came to an end and died, twisted up` | 19:25 |
| καταστρέφω, with ἐν τῷ | `in the turning down` | `within, inside of, and by means of the turning down and trampling on, the turning the soil, the upsetting and overturning, the subjecting to oneself and subduing, the turning back and bringing back, the turning round and bringing to an end, the coming to an end and dying, the twisting up` | 19:29 |
| καταστροφή | `of the overturning` | `of the overturning, of the subduing and subjugation and reduction, of the sudden turn and end, of the close and conclusion, of the catastrophe` | 19:29 |
| καταφεύγω | `to flee for refuge` | `to flee for refuge, to flee and take refuge, to flee for protection, to escape, to have recourse to, to fall back upon and appeal to` | 19:20 |
| κοιμάω | `I was lulled` | `I was lulled, I was hushed to sleep and put to sleep, I was lulled to rest and stilled and calmed, I fell asleep, I went abed and lay abed, I slept, I fell asleep and died, I kept watch at night` | 19:34 |
| κοιμάω | `be lulled` | `be lulled, be hushed to sleep and put to sleep, be lulled to rest and stilled and calmed, fall asleep, go abed and lie abed, sleep, fall asleep and die, keep watch at night` | 19:34 |
| κοιμάω | `was lulled` | `was lulled, was hushed to sleep and put to sleep, was lulled to rest and stilled and calmed, fell asleep, went abed and lay abed, slept, fell asleep and died, kept watch at night` | 19:33, 19:35 |
| κοιμάω | `let us be lulled` | `let us be lulled, let us be hushed to sleep and put to sleep, let us be lulled to rest and stilled and calmed, let us fall asleep, let us go abed and lie abed, let us sleep, let us fall asleep and die, let us keep watch at night` | 19:32 |
| κοιμάω | `of the being lulled` | `of the being lulled, of the being hushed to sleep and put to sleep, of the being lulled to rest and stilled and calmed, of the falling asleep, of the going abed and lying abed, of the sleeping, of the falling asleep and dying, of the keeping watch at night` | 19:4 |
| κοιμάω, with ἐν τῷ | `in the being lulled` | `within, inside of, and by means of the being lulled, the being hushed to sleep and put to sleep, the being lulled to rest and stilled and calmed, the falling asleep, the going abed and lying abed, the sleeping, the falling asleep and dying, the keeping watch at night` | 19:33, 19:35 |
| κρίνω | `to pick out` | `to pick out and choose, to pick out for oneself and choose, to decide, to judge, to adjudge, to judge of and estimate, to expound and interpret, to determine, to question, to bring to trial and accuse, to pass sentence upon and condemn` | 19:9 |
| κρατέω | `were strong` | `were strong and mighty and powerful, ruled and held sway and were sovereign, ruled among, were lords and masters of and rulers over, conquered and prevailed and got the upper hand, prevailed and became current, prevailed over, surpassed and went beyond, conquered and mastered and outdid and surpassed, became masters of and got possession of, laid hold of, seized and held fast, controlled and commanded` | 19:16 |
| κύριος | `lords` | `lords / masters, the heads, masters, sirs` (the vocative) | 19:2 |
| λέγω | `were saying` | `were saying, were speaking, were declaring, were calling by name, were telling` | 19:5 |
| λαλέω | `you talked` | `you talked, you chatted, you prattled, you babbled, you said, you talked of, you spoke, you chattered, you chirped` | 19:21 |
| λαμβάνω | `having taken` | `having taken, having received, having taken hold of and grasped and seized` | 19:14 |
| μέγας | `of big` | `of big, of great, of tall, of full-grown, of vast and high, of spacious and wide, of strong and mighty, of violent, of loud, of prevailing, of weighty and important` | 19:11 |
| μέσος | `of middle` | `of middle, of in the middle, of the centre, of mid, of between two` | 19:29 |
| μήποτε | `that at no time` | `that at no time and lest ever, never and on no account, perhaps` | 19:17 |
| μεγαλύνω | `you made great` | `you made great and powerful, you exalted and strengthened, you made great by word and extolled and magnified, you aggravated` | 19:19 |
| μηδείς | `and not one` | `and not one, not even one, nobody and naught and good for naught, naught and nothing, a good for naught, not at all and by no means` | 19:8 |
| μικρός | `of small` | `of small, of little, of petty and trivial and slight, of short` | 19:11 |
| μικρός | `small` | `small, little, petty and trivial and slight, short` | 19:20 |
| μόνος | `alone` | `alone, left alone and forsaken and solitary, only` | 19:8 |
| μᾶλλον | `more` | `more, more and more and still more, much more, rather` | 19:9 |
| νίπτω | `wash the hands` | `wash the hands, purge and cleanse, wash off` | 19:2 |
| νύξ, with ἐν | `in the night-season` | `within, inside of, and by means of the night-season, the night, the watches of the night, the dark of night, the night of death` | 19:33, 19:35 |
| οἰκία | `the building` | `the building, the house, the dwelling, the household and domestic establishment, the household and inmates of the house, the house and family from which one is descended` | 19:3, 19:4 |
| οὐδείς | `and not one` | `and not one, no one and none, naught and good for naught` | 19:31 |
| πέσσω | `softened` | `softened, ripened, changed, cooked and dressed and baked, digested, cherished and nursed, enjoyed` | 19:3 |
| παρά + genitive | `from the side of` | `from the side of, from beside, from, near` | 19:24 |
| παραλύω | `were loosed from the side` | `were loosed from the side and taken off and detached, were undone and put an end to, were unyoked and parted from, were set free, were loosed beside, were parted from, were exempt, were disabled at the side and paralysed, were exhausted and flagged` | 19:11 |
| περίχωρος | `round about a place` | `round about a place, the people about, the country round about` | 19:28 |
| περιβλέπω | `you may look round about` | `you may look round about and gaze around, you may look round at, you may seek after and look about for, you may gaze on and admire and respect, you may be jealous of and suspect, you may covet` | 19:17 |
| περικυκλόω | `encircled` | `encircled and encompassed, went round` | 19:4 |
| πλατεῖα, with ἐν | `in the street` | `within, inside of, and by means of the street, the flat of the hand` | 19:2 |
| ποιέω | `you make` | `you make, you do, you produce, you create` | 19:19 |
| ποιέω | `you may make` | `you may make, you may do, you may produce, you may create` | 19:8 |
| πονηρεύομαι | `you may be evil` | `you may be evil and act wickedly and play the rogue` | 19:7 |
| ποτίζω | `gave to drink` | `gave to drink, watered, watered the cattle` | 19:33, 19:35 |
| ποτίζω | `let us give to drink` | `let us give to drink, let us water, let us water the cattle` | 19:32, 19:34 |
| πρεσβύτερος | `of elder` | `of elder, of older, of higher and more important, of greater than, of an elder of the Jewish Council, of an elder of the Church and presbyter` | 19:4 |
| πρεσβύτερος | `the elder` | `the elder, the older, the higher and more important, the greater than, the elder of the Jewish Council, the elder of the Church and presbyter` | 19:31, 19:33, 19:34, 19:37 |
| πρωΐ | `early in the day` | `early in the day, early, at morn, betimes, in good time, too soon and too early` | 19:27 |
| πρόθυρον | `the front-door` | `the front-door, the space before a door, the porch and verandah` | 19:6 |
| πρᾶγμα | `that which has been done` | `that which has been done and a deed and an act, anything necessary and expedient, a thing of consequence and importance, an action and affair, the thing and the business` | 19:22 |
| πόλις | `of the city` | `of the city, of the citadel, of the country, of the body of citizens, of the state` | 19:4, 19:15, 19:22 |
| πόλις | `the cities` | `the cities, the citadels, the countries, the bodies of citizens, the states` | 19:25, 19:29 |
| πόλις, with ἐν | `in the cities` | `within, inside of, and by means of the cities, the citadels, the countries, the bodies of citizens, the states` | 19:25 |
| πότος | `drinking` | `drinking and a drinking-bout and carousal` | 19:3 |
| πύλη | `the one wing of a pair of double gates` | `the one wing of a pair of double gates, the gates of a town, the house-door, the nether world and hell, the entrance, the orifice, the entrance into a country through mountains and the mountain-pass, the narrow straits` | 19:1 |
| πῦρ | `fire` | `fire, the funeral-fire, the fire of the hearth` | 19:24 |
| σκέπη | `the covering` | `the covering and shelter and protection` | 19:8 |
| σπήλαιον, with ἐν | `in the grotto` | `within, inside of, and by means of the grotto and cave and cavern` | 19:30 |
| στήλη | `a block of stone` | `a block of stone, a prop and buttress to a wall, a slab, a gravestone, the record and a contract and agreement, the turning-post` | 19:26 |
| συγγίνομαι | `we may be with` | `we may be with, we may hold converse and communication with, we may associate and keep company with, we may consult, we may come to assist, we may come together and meet` | 19:5 |
| συμπαραλαμβάνω | `you may be taken along with` | `you may be taken along with, you may be taken in as an adjunct` | 19:17 |
| συντρίβω | `to rub together` | `to rub together, to shiver to atoms, to beat to a jelly and crush` | 19:9 |
| σῴζω | `I will be saved` | `I will be saved and kept, I will be saved from death and kept alive and preserved, I will be kept safe, I will be kept and observed and maintained, I will be kept in mind and remembered, I will be brought safe to, I will be carried off safe and rescued from, I will come safe and escape to` | 19:20 |
| σῴζω | `keep for yourself` | `keep for yourself and preserve for yourself, keep in mind and remember` | 19:17 |
| σῴζω | `save` | `save and keep, save from death and keep alive and preserve, keep safe, keep and observe and maintain, keep in mind and remember, bring safe to, carry off safe and rescue from` | 19:17 |
| σῴζω | `saving` | `saving and keeping, saving from death and keeping alive and preserving, keeping safe, keeping and observing and maintaining, keeping in mind and remembering, bringing safe to, carrying off safe and rescuing from` | 19:17 |
| σῴζω | `to be saved` | `to be saved, to be kept, to be saved from death and kept alive and preserved, to be kept safe, to be kept and observed and maintained, to be kept in mind and remembered, to be brought safe to, to be carried off safe and rescued from, to come safe and escape to` | 19:22 |
| ταράσσω | `were stirred` | `were stirred, were stirred up, were troubled, were confounded and agitated and disturbed and disquieted, were thrown into disorder, were agitated and distracted, were raised by stirring up, were in disorder, were in a state of disorder and anarchy, were shaken in their seat` | 19:16 |
| φείδομαι, with ἐν τῷ | `in the sparing` | `within, inside of, and by means of the sparing, the not destroying, the being merciful, the refraining from using and using sparingly, the being sparing and being thrifty and living thriftily, the drawing back from, the ceasing, the forbearing` | 19:16 |
| ἀνήρ | `a man` | `a man, a man in the prime of life` | 19:8 |
| ἀνίστημι | `stand up` | `stand up, rise, rise to fight against, rise to go and set out` | 19:14 |
| ἀνίστημι | `to stand up` | `to stand up, to rise, to rise to fight against, to rise to go and set out` | 19:33, 19:35 |
| ἀνατέλλω | `the ones making to rise up` | `the ones making to rise up, growing up, giving birth to and bringing to light, rising, taking their rise, growing` | 19:25 |
| ἀορασία | `with inability to see` | `with inability to see, with blindness, with failure to observe` | 19:11 |
| ἀποθνήσκω | `I may die off` | `I may die off and die, I may be put to death and slain` | 19:19 |
| ἀποκλείω | `shut off from` | `shut off from and out of, debarred, shut out and excluded from, shut up and barred and closed, shut up, shut out and intercepted and barred` | 19:10 |
| ἀπόλλυμι | `we destroy utterly` | `we destroy utterly and kill and slay, we destroy and demolish and waste, we talk and bore to death, we lose utterly` | 19:13 |
| ἀρέσκω | `may make good` | `may make good and make up, may make amends, may please and satisfy and flatter` | 19:8 |
| ἀτμίς | `steam` | `steam and vapour` | 19:28 |
| ἀφίστημι | `stand away` | `stand away, stand aloof from and keep far from, lose, withdraw from, revolt from, revolt, give up, make way and give way, shrink from, stand aloof` | 19:9 |
| ἄγγελος | `the messengers` | `the messengers and envoys, the ones that announce, the divine messengers and the angels` | 19:1, 19:15, 19:16 |
| ἄδικος | `wrong-doing` | `wrong-doing and unrighteous and unjust, unjust in, so unjust as to, obstinate and unmanageable, wrongly done and wrong and unjust` | 19:8 |
| ἄλλος | `another` | `another, one besides, any other and some other, the other, all the others and the rest, yet and still, of other sort and different, other than, else` | 19:12 |
| ἅλς | `of a lump of salt` | `of a lump of salt, of salt` | 19:26 |
| ἅπας | `quite all` | `quite all and the whole, all together, all, everyone` | 19:4 |
| ἐγγίζω | `brought near` | `brought near and brought up to, approached, were imminent, approximated to, were next of kin, were on the point of` | 19:9 |
| ἐγγύς | `hard by` | `hard by and near to, near and nigh and at hand, nigh at hand, nearly, akin to` | 19:20 |
| ἐκκαλέω | `were calling out to themselves` | `were calling out to themselves, were calling forth and eliciting, were calling on to` | 19:5 |
| ἐκκλίνω | `bend out of the regular line` | `bend out of the regular line, turn away and give ground and retire, avoid and shun, turn aside towards` | 19:2 |
| ἐκκλίνω | `bent out of the regular line` | `bent out of the regular line, turned away and gave ground and retired, avoided and shunned, turned aside towards` | 19:3 |
| ἐκτρίβω | `rubs out` | `rubs out, rubs hard, destroys root and branch, rubs constantly and wears out` | 19:14 |
| ἐκτρίβω | `to rub out` | `to rub out, to rub hard, to destroy root and branch, to rub constantly and wear out` | 19:13 |
| ἐκτρίβω, with ἐν τῷ | `in the rubbing out` | `within, inside of, and by means of the rubbing out, the rubbing hard, the destroying root and branch, the rubbing constantly and wearing out` | 19:29 |
| ἐξάγω | `I will lead out` | `I will lead out, I will lead and carry out from, I will bring forth into the world, I will march out, I will eject, I will carry out and export, I will draw off, I will call forth and excite, I will lead on and tempt` | 19:8 |
| ἐξανίστημι | `let us raise up` | `let us raise up, let us make to rise, let us remove and expel, let us rouse` | 19:32, 19:34 |
| ἐξανίστημι | `stood up from one's seat` | `stood up from one's seat, rose, arose and departed from and emigrated from, broke up and departed, was driven out, was forced to emigrate, was depopulated` | 19:1 |
| ἐπιβλέπω | `looked upon` | `looked upon and looked attentively, looked well at and observed, eyed with envy` | 19:26, 19:28 |
| ἑσπέρα | `of evening` | `of evening, of eventide, of eve, of nightfall, of the west` | 19:1 |
| ἔλεος | `pity` | `pity and mercy and compassion, an object of compassion and a piteous thing` | 19:19 |
| ἔρχομαι | `you came` | `you came, you went, you went back and returned, you were going to and intended, you came within a little of and were near` | 19:9 |
| ἡμέρα | `of day` | `of day, of day-break, of time` | 19:37, 19:38 |
| ἤ | `or` | `or, either or, whether or, than and as, rather` | 19:9, 19:12 |
| ἵστημι | `you may be set` | `you may be set, you may be placed and stand, you may be there, you may be in a state and condition, you may lie and be situated, you may stand still and stop and halt, you may stand idle, you may stop and cease and be at rest, you may stand firm, you may stand up and rise up, you may arise and begin` | 19:17 |
| ὀπίσω | `backwards` | `backwards, back and back again, again, hereafter, behind, following` | 19:17, 19:26 |
| ὀρθρίζω | `having risen early` | `having risen early and been awake early` | 19:2 |
| ὀρθρίζω | `rose early` | `rose early and was awake early` | 19:27 |
| ὄρθρος | `day-break` | `day-break and dawn and cock-crow` | 19:15 |
| ὄρος, with ἐν | `in the mountain` | `within, inside of, and by means of the mountain and hill` | 19:30 |
| ὡσεί | `just as if` | `just as if and as though, about` | 19:28 |
| ῥῆμα | `to that which is said` | `to that which is said and spoken, to the word, to the saying, to the phrase, to the subject of speech and the thing, to the verb` | 19:21 |

### Words new in GEN 18

- ἆρα — Middle Liddell gives it no gloss, only *in accent and sense a stronger form of ἄρα*, so the
  chain is ἄρα's, as ἐπειδή's is ἐπεί's (15:3). Perseus keys ἄρα itself with a rough breathing,
  `a(/ra`; its first sense is *then, straightway, at once*. 18:3, 18:13.
- πρεσβύτερος — filed inside πρέσβυς, whose comparative is *elder, older*, and in the New
  Testament *an elder of the Jewish Council*, *an elder of the Church, presbyter*. The comparative's
  own senses stand, as the adverb's do for an adverb filed inside its adjective; πρέσβυς's
  *an old man* is not the comparative's. 18:11, 18:12.
- τὰ γυναικεῖα — γυναικεῖος's noun sense, *the women's apartments, harem*, belongs to the singular
  τὸ γυναικεῖον, so the plural takes the article and the adjective's senses, `the belonging to
  women`, as ὁ οἰκογενής is `the born in the house` (15:3). 18:11.
- ἵστημι and παρίστημι in the perfect and pluperfect take the intransitive senses the entries
  give those tenses: εἱστήκεισαν `had been set and stood so` (18:2), παρειστήκει `had stood by`
  (18:8), ἑστηκώς `having been set and standing so` (18:22). ἐξανίστημι's second aorist likewise,
  `having stood up from one's seat` (18:16).
- ἀποκρίνομαι — filed under ἀποκρίνω, whose middle is *to give answer to, reply*; its aorist
  passive is, in the entry's words, *= ἀπεκρίνατο*: `having given answer to`. 18:9, 18:27.
- The genitive absolute, καθημένου αὐτοῦ — the case's `of` before each gloss, `of being seated`.
  18:1.
- Two tags split by *or* where the first is no gloss by itself: νίπτω's *to wash the hands* or
  *feet* (*feet* left out), as παιδίον's *a little* at 17:12. 18:4.
- ὥρα plural — each sense in the plural, *Hours* capitalised as the lexicon prints the goddesses.
  18:10, 18:14.
- ἄρτος anarthrous — `a cake, a loaf of wheat-bread, bread`, the chain of GEN 3:19 with the
  lexicon's own articles. 18:5.
- μηδαμῶς — *adverb of μηδαμός = μηδαμῇ*; μηδαμῇ's one sense, *in no wise, not at all*. 18:25.
- One sense each in GEN 18, so plain text: συνάντησις `a meeting` (18:2); δένδρον `the tree`
  (18:4, 18:8), not δρῦς; σεμίδαλις `of the finest wheaten flour`, ἐγκρυφίας `baked in the ashes`
  (18:6); μοσχάριον `little calf` (18:7, 18:8, LSJ); γάλα `milk` (18:8); καταβλέπω `looked down
  at`, συμπροπέμπω `joining in escorting` (18:16); ἐνευλογέομαι `will be blessed in` (18:18), as at
  12:3; ἐλαττονόω `may be diminished` (18:28); οὐχί `not` (18:15).

| lemma | headword | chain | used |
| --- | --- | --- | --- |
| βούτυρον | `butter` | `butter, a plant` | 18:8 |
| βοῦς | `the cows` | `the cows, the oxen, the kine and cattle, the ox-hide shields` | 18:7 |
| γε | `at least` | `at least, at any rate, even, that is to say, really, namely and that is, yes and, well then` | 18:13 |
| γίνομαι | `coming into being` | `coming to be, arising, being brought into existence` | 18:18 |
| γελάω | `I laughed` | `I laughed, I laughed at, I derided` | 18:15 |
| γελάω | `you laughed` | `you laughed, you laughed at, you derided` | 18:15 |
| γηράσκω | `I have grown old` | `I have grown old and stand so, I have become old and remain so` | 18:13 |
| γινώσκω | `I may learn to know` | `I may learn to know, I may perceive, I may mark, I may learn, I may discern and distinguish` | 18:21 |
| γυναικεῖος | `the belonging to women` | `the belonging to women and like women and befitting them and feminine, the womanish and effeminate` | 18:11 |
| δίκαιος | `of observant of custom and social rule` | `of observant of custom and social rule and well-ordered and civilised, of observant of right and righteous, of even and well-balanced, of regular and exact, of right and lawful and just, of real and genuine and true, of fair and moderate` | 18:24 |
| δίκαιος | `the observant of custom and social rule` | `the observant of custom and social rule and well-ordered and civilised, the observant of right and righteous, the even and well-balanced, the regular and exact, the right and lawful and just, the real and genuine and true, the fair and moderate` | 18:23, 18:25 |
| εὑρίσκω | `I found` | `I found, I found out, I discovered, I got and gained` | 18:3 |
| εὑρίσκω | `I may find` | `I may find, I may find out, I may discover, I may get and gain` | 18:26, 18:28, 18:30 |
| εὑρίσκω | `may be found` | `may be found, may be found out, may be discovered` | 18:29, 18:30, 18:31, 18:32 |
| θύρα | `of the door` | `of the door, of the folding doors, of the gate, of the court, of the trap-door, of the frame of planks and raft, of the entrance` | 18:1, 18:2 |
| θύρα | `to the door` | `to the door, to the folding doors, to the gate, to the court, to the trap-door, to the frame of planks and raft, to the entrance` | 18:10 |
| κάθημαι | `of being seated` | `of being seated, of being seated in court, of sitting still and sitting quiet, of sitting and lying idle, of sitting down and lying, of leading a sedentary life, of being settled` | 18:1 |
| καταψύχω | `cool` | `cool and chill` | 18:4 |
| κρίνω | `the one picking out` | `the one picking out and choosing, the one picking out for oneself and choosing, the one deciding, the one judging, the one adjudging, the one judging of and estimating, the one expounding and interpreting, the one determining, the one questioning, the one bringing to trial and accusing, the one passing sentence upon and condemning` | 18:25 |
| κρίσις | `a separating` | `a separating and power of distinguishing, choice and selection, a decision and judgment, means of judging, a trial, the result of a trial and condemnation, a dispute, the event and issue` | 18:19, 18:25 |
| κραυγή | `a crying` | `a crying and screaming and shrieking and shouting` | 18:20 |
| κραυγή | `the crying` | `the crying and screaming and shrieking and shouting` | 18:21 |
| κρύπτω | `I may hide` | `I may hide and cover and cloak, I may cover in the earth and bury, I may conceal and keep secret` | 18:17 |
| λέγω | `you have said` | `you have said and it stands said, you have spoken and it stands spoken, you have declared and it stands declared, you have called by name and it stands so, you have told and it stands told` | 18:5 |
| λαλέω | `I may talk` | `I may talk, I may chat, I may prattle, I may babble, I may say, I may talk of, I may speak, I may chatter, I may chirp` | 18:30, 18:32 |
| λαλέω | `to talk` | `to talk, to chat, to prattle, to babble, to say, to talk of, to speak, to chatter, to chirp` | 18:27, 18:29, 18:31 |
| λαμβάνω | `let be taken` | `let be taken, let be received, let be taken hold of and grasped and seized` | 18:4 |
| μέν | `on the one hand` | `on the one hand and other hand, as well as and while, whereas, indeed, for my part, surely, accordingly and so, at all events and at any rate, so then, nay rather, nay, yea rather, yet and but however and nevertheless, of course and certainly, only` | 18:12 |
| μέτρον | `things by which anything is measured` | `things by which anything is measured, measures, rules, measures of content, measures and lengths and sizes, full measures, due measures, limits and proportions, metres, verses` | 18:6 |
| μεσημβρία | `of mid-day` | `of mid-day, of noon, of the parts towards noon and the South` | 18:1 |
| μηδαμῶς | `in no wise` | `in no wise and not at all` | 18:25 |
| νίπτω | `let wash the hands` | `let wash the hands, let purge and cleanse, let wash off` | 18:4 |
| οἶδα | `I knew` | `I knew, I was assured, I was versed in` | 18:19 |
| οἶκος | `to the house` | `to the house and abode and dwelling, to the room and chamber, to the house of a god and temple, to the household goods and substance, to the household and family` | 18:19 |
| παρά + dative | `beside` | `beside, alongside of, by, at, before, with` | 18:14 |
| παρέρχομαι | `you may go by` | `you may go by, you may go beside, you may go past, you may pass by, you may pass, you may outstrip, you may outwit and escape and elude, you may arrive at, you may pass in, you may go into, you may pass without heeding, you may pass over and disregard and slight, you may overstep and transgress, you may pass unnoticed and escape the notice of, you may come forward` | 18:3 |
| παρέρχομαι | `you will go by` | `you will go by, you will go beside, you will go past, you will pass by, you will pass, you will outstrip, you will outwit and escape and elude, you will arrive at, you will pass in, you will go into, you will pass without heeding, you will pass over and disregard and slight, you will overstep and transgress, you will pass unnoticed and escape the notice of, you will come forward` | 18:5 |
| παρίστημι | `had stood by` | `had stood by and beside and near, had helped and defended, had come and been at hand and been present, had been near and at hand, had come to the side of and come over to, had come to terms and surrendered and submitted, had happened, had come into his head and occurred to` | 18:8 |
| παρατίθημι | `placed beside` | `placed beside, set before and served up, offered and provided, placed upon, laid before and explained, compared` | 18:8 |
| παύω | `took his rest` | `took his rest and rested and ceased and had done, left off from and rested and ceased from, was at rest, left off doing` | 18:33 |
| παῖς | `of the child` | `of the child, of the son, of the daughter, of the grandchild, of the boy and youth and lad, of the girl and maiden, of the slave and servant and man and maid` | 18:17 |
| παῖς | `the child` | `the child, the son, the daughter, the grandchild, the boy and youth and lad, the girl and maiden, the slave and servant and man and maid` | 18:3, 18:5 |
| παῖς | `to the child` | `to the child, to the son, to the daughter, to the grandchild, to the boy and youth and lad, to the girl and maiden, to the slave and servant and man and maid` | 18:7 |
| πληθύνω | `has been made full` | `has been made full and increased and multiplied and stands so, has been in the majority and prevailed and remains so` | 18:20 |
| ποιέω | `I make` | `I make, I do, I produce, I create` | 18:17 |
| πολύς | `much` | `much and mighty and great, many, deep, loud, strong, large and wide, far, long, often` | 18:18 |
| πούς | `the feet` | `the feet, the talons, the feet of a hill` | 18:4 |
| πρεσβύτερος | `elder` | `elder, older, higher and more important, greater than, an elder of the Jewish Council, an elder of the Church and presbyter` | 18:12 |
| πρεσβύτερος | `elder` | `elder, older, higher and more important, greater than, elders of the Jewish Council, elders of the Church and presbyters` | 18:11 |
| προβαίνω | `having stepped on` | `having stepped on and standing so, having stepped forward and standing so, having advanced and standing so, having proceeded and standing so, having gone before and standing so, having been before and superior to and remaining so, having overstepped and standing so` | 18:11 |
| προσκυνέω | `made obeisance` | `made obeisance, fell down and worshipped and worshipped and adored, did reverence to, made the salam, prostrated himself before` | 18:2 |
| προστρέχω | `ran to` | `ran to, ran towards and came to, ran up, ran at and made a sally` | 18:2 |
| πόλις, with ἐν | `in the city` | `within, inside of, and by means of the city, the citadel, the country, the body of citizens, the state` | 18:24, 18:26 |
| σκηνή | `of the covered place` | `of the covered place and tent, of the camp, of the dwelling-place, of the temple` | 18:1, 18:2, 18:10 |
| σκηνή, with ἐν | `in the covered place` | `within, inside of, and by means of the covered place and tent, the camp, the dwelling-place, the temple` | 18:9 |
| σπεύδω | `set a-going` | `set a-going and urge on and hasten and quicken, seek eagerly and strive after, promote zealously and press, press on and hasten and exert yourself and strive eagerly, be eager to do, be anxious that` | 18:6 |
| σπεύδω | `set a-going` | `set a-going and urged on and hastened and quickened, sought eagerly and strove after, promoted zealously and pressed, pressed on and hastened and exerted himself and strove eagerly, was eager to do, was anxious that` | 18:6 |
| σποδός | `wood-ashes` | `wood-ashes and embers, ashes, dust` | 18:27 |
| συμπορεύομαι | `was going` | `was going, was journeying together, was coming together` | 18:16 |
| συναπόλλυμι | `you may destroy together` | `you may destroy together, you may lose` | 18:23 |
| συντάσσω | `will put in order together` | `will put in order together, will draw up and put in array, will arrange and organise, will concoct, will fix and assess, will ordain and prescribe` | 18:19 |
| συντελέω | `are being brought quite to an end` | `are being brought quite to an end and completed and accomplished, are being made up into the whole and into the number` | 18:21 |
| τίκτω | `I will bring into the world` | `I will bring into the world, I will bring forth, I will bear, I will beget, I will produce and yield` | 18:13 |
| ταχύνω | `made quickly` | `made quickly, was quick and made haste and sped and hurried` | 18:7 |
| τρέχω | `ran` | `ran, moved quickly, ran over, ran the risk` | 18:7 |
| φοβέομαι | `was put to flight` | `was put to flight, fled affrighted, fled, was seized with fear, was affrighted, feared` | 18:15 |
| φυλάσσω | `they will keep watch and ward` | `they will keep watch and ward and keep guard, they will watch and guard and keep and defend, they will watch for and lie in wait for, they will keep and maintain and cherish, they will observe` | 18:19 |
| φυράω | `mix` | `mix, knead, make up` | 18:6 |
| ἀδυνατέω | `wants strength` | `wants strength, is unable, is impossible` | 18:14 |
| ἀληθῶς | `truly` | `truly, really and actually and in reality` | 18:13 |
| ἀνήρ | `men` | `men, men in the prime of life` | 18:2 |
| ἀνίημι | `you will send up` | `you will send up and forth, you will make spring up, you will produce, you will send back and put back and open, you will let go and leave, you will let go unpunished, you will let loose at, you will set on and urge, you will let go for, you will set free from, you will let and allow, you will let go free and leave untilled, you will slacken and relax and let down and unstring, you will remit and neglect and give up, you will slacken and abate, you will give way, you will give up and cease, you will cease from` | 18:24 |
| ἀναστρέφω | `I will turn upside down` | `I will turn upside down, I will upset, I will turn back and bring back, I will rally, I will turn back and return and retire, I will dwell, I will conduct myself, I will revolve, I will face about` | 18:14 |
| ἀπέρχομαι | `went away` | `went away, departed from, departed, departed from life` | 18:33 |
| ἀποκρίνομαι | `having given answer to` | `having given answer to and replied, having answered, having answered charges and defended himself` | 18:27 |
| ἀποκτείνω | `to kill` | `to kill, to slay, to condemn to death` | 18:25 |
| ἀποστρέφω | `having turned` | `having turned, having turned back, having turned away, having turned oneself about, having brought back` | 18:22 |
| ἀποστρέφω | `turned` | `turned, turned back, turned away, turned himself about, brought back` | 18:33 |
| ἀπόλλυμι | `I may destroy utterly` | `I may destroy utterly and kill and slay, I may destroy and demolish and waste, I may talk and bore to death, I may lose utterly` | 18:28, 18:29, 18:30, 18:31, 18:32 |
| ἀπόλλυμι | `you will destroy utterly` | `you will destroy utterly and kill and slay, you will destroy and demolish and waste, you will talk and bore to death, you will lose utterly` | 18:24, 18:28 |
| ἀρνέομαι | `denied` | `denied and disowned, declined to give and refused, said no and declined and refused` | 18:15 |
| ἀσεβής | `of ungodly` | `of ungodly and godless and unholy and profane` | 18:23, 18:25 |
| ἀσεβής | `the ungodly` | `the ungodly and godless and unholy and profane` | 18:23, 18:25 |
| ἀφίημι | `I will send forth` | `I will send forth, I will discharge, I will let go and loose and set free, I will let alone and leave, I will give up and hand over, I will permit and allow` | 18:26 |
| ἁπαλός | `soft to the touch` | `soft to the touch, tender, fresh, soft and gentle, soft and delicate` | 18:7 |
| ἄρα, ἆρα | `then` | `then, straightway, at once, next in order, mark ye, for, just and very, then and therefore, so then` | 18:3, 18:13 |
| ἄρτος | `a cake` | `a cake, a loaf of wheat-bread, bread` | 18:5 |
| ἄρχω | `I began` | `I began, I made a beginning, I made a beginning of, I began from` | 18:27 |
| ἅπαξ | `once` | `once and once only and once for all` | 18:32 |
| ἐγγίζω | `having brought near` | `having brought near and brought up to, having approached, having been imminent, having approximated to, having been next of kin, having been on the point of` | 18:23 |
| ἐκκλίνω | `you bent out of the regular line` | `you bent out of the regular line, you turned away and gave ground and retired, you avoided and shunned, you turned aside towards` | 18:5 |
| ἐξανίστημι | `having stood up from one's seat` | `having stood up from one's seat, having risen, having arisen and departed from and emigrated from, having broken up and departed, having been driven out, having been forced to emigrate, having been depopulated` | 18:16 |
| ἐπάγω | `may bring on` | `may bring on, may bring upon, may set on and urge on, may lead on, may bring in and invite, may bring to, may lay on and apply, may bring forward, may add` | 18:19 |
| ἐπαναστρέφω | `turning back upon one` | `turning back upon one, wheeling round, returning to the charge` | 18:10 |
| ἔρχομαι | `coming` | `coming, going, going back and returning, going to and intending, coming within a little of and being near` | 18:21 |
| ἔχω | `I have` | `I have, I hold, I possess, I keep, I dwell in and inhabit, I hold fast, I bear up against and support` | 18:31 |
| ἔχω | `will have` | `will have, will hold, will possess, will keep, will dwell in and inhabit, will hold fast, will bear up against and support` | 18:10 |
| ἥκω | `I will have come` | `I will have come, I will be present, I will be here, I will have returned, I will have reached a point` | 18:10 |
| ἵστημι | `had been set` | `had been set and stood so, had been placed and stood, had been there, had been in a state and condition, had lain and been situated, had stood still and stopped and halted, had stood idle, had stopped and ceased and been at rest, had stood firm, had stood up and risen up, had arisen and begun` | 18:2 |
| ἵστημι | `having been set` | `having been set and standing so, having been placed and stood, having been there, having been in a state and condition, having lain and been situated, having stood still and stopped and halted, having stood idle, having stopped and ceased and been at rest, having stood firm, having stood up and risen up, having arisen and begun` | 18:22 |
| ὁδός | `the ways` | `the ways, the paths, the tracks, the roads, the highways, the courses, the journeys, the manners and methods` | 18:19 |
| ὄπισθεν | `behind` | `behind, at the back, the rear and back, back and backwards, in future and hereafter, following` | 18:10 |
| ὥρα | `periods` | `periods, parts of the year and seasons, springs, summers, winters, primes of the year and springtimes, parts of the year available for war and summer-seasons, years, quarters of the heavens, parts of the day, times of day, twenty-four hours, twelve parts, times and seasons, primes of life and youths and early manhoods, fruits of the year, Hours` | 18:10, 18:14 |
| ῥῆμα | `that which is said` | `that which is said and spoken, a word, a saying, a phrase, the subject of speech and a thing, a verb` | 18:25 |

### Words new in GEN 17

- περιτέμνω — Middle Liddell's *to cut* or *clip round about*, tagged in two pieces; *to cut* is a
  gloss by itself and heads, as *to go* heads συμπορεύομαι's *to go or journey together* (13:5).
  A passive form takes the active senses, *to be pruned*, *to be cut off*, *to be cut off and hemmed
  in all round*, and the passive's own, *to be curtailed of*, *to be cut off, intercepted*, last.
  *To make incisions all round* and *they practise circumcision* are translations of the middle
  alone, and neither passive nor active takes them. 17:10–14, 17:23–27.
- παιδίον — Middle Liddell's *a little* or *young child*: *a little* is no gloss by itself, so it
  goes in NOT_SENSES and *young child* heads. ἀλλότριος — *of* or *belonging to another*: *of*
  likewise, and *belonging to another* heads. 17:12.
- ἐνιαυτός — first *any long period of time, a cycle, period*; with the article, *the* stands where
  the lexicon has *any*, as it does for *a*: `in the long period of time`. 17:21.
- ἑκατονταέτης — articular, with no noun: `to the of a hundred years`, the article and the lexicon's
  gloss, as ὁ οἰκογενής is `the born in the house` (15:3). 17:17.
- ἀλλογενής — the gloss *of another race* in the genitive plural: the case's `of` stands before the
  lexicon's own, `of of another race`. 17:27.
- θεός anarthrous, not fronted — εἶναί σου θεός (17:7), ἔσομαι αὐτοῖς θεός (17:8): `God` /
  `everything that God is by nature, deity in full and undiminished kind`.
- Αβραμ and Αβρααμ, Σαρα and Σαρρα — two names each, each glossed on its first occurrence in the
  chapter; the anchored forms are Abram, Abraham, Sarai, Sarah. 17:5, 17:15.
- One sense each in GEN 17, so plain text: ἀρσενικός `male` (17:10, 17:12), under ἀρρενικός;
  ἀργυρώνητος `bought with silver` (17:12, 17:13, 17:23, 17:27); περιτομή `to circumcision`
  (17:13); ἀπερίτμητος `uncircumcised` and ὄγδοος `eighth` (17:14); ἐξολεθρεύω `will be destroyed
  utterly` (17:14), under ἐξολοθρεύω; δώδεκα `twelve` (17:20).

| lemma | headword | chain | used |
| --- | --- | --- | --- |
| αὐξάνω | `I will make large` | `I will make large and increase and augment, I will increase in power and strengthen and exalt and aggrandise, I will promote to honour and glorify and magnify, I will grow and wax and increase, I will grow up` | 17:6, 17:20 |
| γένος | `of the race` | `of the race, of the stock and family, of the offspring and posterity, of the clan and house, of the tribe and caste, of the breed, of the age and generation, of the sex and gender, of the class and sort and kind, of the genus` | 17:14 |
| γίνομαι | `come into being` | `come to be, arise, be brought into existence` | 17:1 |
| γίνομαι | `will come into being` | `will come to be, will arise, will be brought into existence` | 17:17 |
| γελάω | `laughed` | `laughed, laughed at, derided` | 17:17 |
| γενεά | `the races` | `the races and stocks and families, the breeds, the tribes and nations, the races and generations, the offspring, the birth-places, the ages and times of life, the times of birth` | 17:9, 17:10, 17:12 |
| γεννάω | `will beget` | `will beget and engender, will bring forth, will produce` | 17:20 |
| διάνοια, with ἐν | `in the thought` | `within, inside of, and by means of the thought, the intention and purpose, the notion and opinion, the intelligence and understanding, the meaning` | 17:17 |
| διασκεδάννυμι | `scattered abroad` | `scattered abroad and scattered to the winds and dispersed, disbanded` | 17:14 |
| διατηρέω | `you will watch closely` | `you will watch closely and observe, you will keep faithfully and maintain, you will keep` | 17:9, 17:10 |
| εὐαρεστέω | `be well pleasing` | `be well pleasing, seem good and be resolved, be well pleased and satisfied` | 17:1 |
| εὐλογέω | `I spoke well of` | `I spoke well of, I praised, I honoured, I blessed` | 17:20 |
| ζάω | `let live` | `let live, let be in full life and strength and fresh and strong` | 17:18 |
| θεός | `God` | `everything that God is by nature, deity in full and undiminished kind` | 17:7, 17:8 |
| καιρός | `the due measure` | `the due measure and proportion and fitness, the vital part, the right point of time, the proper time and season, the exact and critical time, the time, the advantage and profit and fruit` | 17:21 |
| καιρός, with ἐν | `in the due measure` | `within, inside of, and by means of the due measure and proportion and fitness, the vital part, the right point of time, the proper time and season, the exact and critical time, the time, the advantage and profit and fruit` | 17:23, 17:26 |
| καλέω | `will be called` | `will be called, will be summoned, will be invited` | 17:5, 17:15 |
| κατάσχεσις | `holding back` | `holding back and restraining and retention, possession, relation and attitude` | 17:8 |
| λαλέω | `talking` | `talking, chatting, prattling, babbling, saying, talking of, speaking, chattering, chirping` | 17:22 |
| ναί | `yea` | `yea and verily, aye and yes` | 17:19 |
| οἰκία | `of the building` | `of the building, of the house, of the dwelling, of the household and domestic establishment, of the household and inmates of the house, of the house and family from which one is descended` | 17:12, 17:13 |
| πίπτω | `fell` | `fell, fell down, fell violently upon and attacked, threw himself down and fell down, fell and was ruined, fell and sank, fell short and failed, fell and turned out, was lucky, fell under and belonged to` | 17:3, 17:17 |
| παιδίον | `young child` | `young child, a slave-lad` | 17:12 |
| παροικέω | `you dwell beside` | `you dwell beside, you dwell along the coast of, you live near, you dwell among, you lie near, you live in and sojourn` | 17:8 |
| περιτέμνω | `cut` | `cut, clipped round about, pruned, cut off, cut off and hemmed in all round` | 17:23, 17:24, 17:27 |
| περιτέμνω | `was cut` | `was cut, was clipped round about, was pruned, was cut off, was cut off and hemmed in all round, was curtailed of, was cut off and intercepted` | 17:25, 17:26 |
| περιτέμνω | `will be cut` | `will be cut, will be clipped round about, will be pruned, will be cut off, will be cut off and hemmed in all round, will be curtailed of, will be cut off and intercepted` | 17:10, 17:12, 17:13, 17:14 |
| περιτέμνω | `you will be cut` | `you will be cut, you will be clipped round about, you will be pruned, you will be cut off, you will be cut off and hemmed in all round, you will be curtailed of, you will be cut off and intercepted` | 17:11 |
| πλῆθος | `of a great number` | `of a great number and throng and crowd and multitude, of the greater number and greater part and mass and main body, of the majority and people, of the populace and mob, of quantity, of number, of magnitude and size, of extent, of amount, of length` | 17:4 |
| πολύς | `of many` | `of many, often, of much and mighty and great, of deep, of loud, of strong, of large and wide, of far, of long` | 17:5 |
| σάρξ | `of the flesh` | `of the flesh, of the muscles, of the body, of man's nature generally` | 17:13 |
| σάρξ | `the flesh` | `the flesh, the muscles, the body, man's nature generally` | 17:11, 17:14, 17:24, 17:25 |
| σημεῖον, with ἐν | `in sign` | `within, inside of, and by means of sign, mark and token, sign from the gods and omen, signal, standard and ensign, boundary` | 17:11 |
| τέκνον | `that which is borne` | `that which is borne, the born, a child, my son and my child, the young` | 17:16 |
| τίθημι | `I have set` | `I have set and it stands set, I have put and it stands put, I have placed and it stands placed, I have planted and it stands planted, I have laid and it stands laid` | 17:5 |
| τίκτω | `will bring into the world` | `will bring into the world, will bear, will bring forth, will beget, will produce and yield` | 17:17, 17:19, 17:21 |
| ἀκροβυστία | `of the foreskin` | `of the foreskin, of the circumcision, of the uncircumcision, of the uncircumcised` | 17:11, 17:14, 17:24, 17:25 |
| ἀκροβυστία | `the foreskins` | `the foreskins, the circumcisions, the uncircumcisions, the uncircumcised` | 17:23 |
| ἀλλογενής | `of of another race` | `of of another race and strangers` | 17:27 |
| ἀλλότριος | `of belonging to another` | `of belonging to another, of another man's, of unlike one's own, of a forced and unnatural, of foreign and strange, of hostile` | 17:12 |
| ἄμεμπτος | `not to be blamed` | `not to be blamed and blameless, perfect in its kind, without blame, not blaming and content` | 17:1 |
| ἐνιαυτός, with ἐν | `in the long period of time` | `within, inside of, and by means of the long period of time and cycle and period, the year` | 17:21 |
| ἐπακούω | `I listened` | `I listened, I hearkened to and heard, I gave ear and hearkened, I obeyed` | 17:20 |
| ἑκατονταετής | `to the of a hundred years` | `to the of a hundred years and years old` | 17:17 |
| ἡμέρα | `of the day` | `of the day, of the day-break, of the time` | 17:23, 17:26 |
| ἡμέρα | `to the day` | `to the day, to the day-break, to the time` | 17:14 |

### Words new in GEN 16

- ἀδικέω — its first sense, *to do wrong*, has no object a passive could make its subject, so *to
  do one wrong, to wrong*, heads the passive `I am done wrong`, and the first follows in its own
  voice, as καπνίζω at 15:17. 16:5.
- γαστήρ — ἐν γαστρὶ ἔχειν, *to be with child*, stands in Middle Liddell under the last sense, *the
  womb*; the headword is the first, *paunch*. 16:4, 16:5, 16:11.
- κυρία — filed under κύριος, whose noun sense gives ἡ κυρία, *mistress* or *lady of the house*.
  16:4, 16:8, 16:9.
- Φρέαρ — capitalised as the first word of the well's name, glossed as a name; φρέαρ before it is
  the common noun. οὗ after it is the adverb, *where*, plain. 16:14.
- Αἰγυπτία — glossed `(Αἰγυπτία, the woman of Αἴγυπτος, Egypt)`, the feminine of 12:12's gloss. 16:1.
- One sense each in GEN 16, so plain text: τεκνοποιέω `you may bear children` (16:2), as at 11:30;
  ὕδωρ `of the water` (16:7); ἐνώπιον `face to face` (16:13, 16:14), as at 11:28; ἕξ `six` (16:16).

| lemma | headword | chain | used |
| --- | --- | --- | --- |
| γαστήρ, with ἐν | `in paunch` | `within, inside of, and by means of paunch and belly, hollow, greed and gluttony, paunch stuffed with mince-meat and black-pudding and sausage, womb` | 16:4, 16:5, 16:11 |
| κακόω | `treated ill` | `treated ill and maltreated and afflicted and distressed, spoiled and ruined, suffered ill and was in ill plight and was distressed` | 16:6 |
| καλέω | `you will call` | `you will call, you will summon, you will call to yourself, you will invite` | 16:11 |
| κατοικέω | `will dwell in` | `will dwell in, will settle in, will colonise, will inhabit, will settle and dwell, will lie and be situate` | 16:12 |
| κρίνω | `may pick out` | `may pick out and choose, may pick out for oneself and choose, may decide, may judge, may adjudge, may judge of and estimate, may expound and interpret, may determine, may question, may bring to trial and accuse, may pass sentence upon and condemn, may be chosen, may be brought to trial` | 16:5 |
| κυρία | `of the mistress` | `of the mistress, of the lady of the house` | 16:8 |
| κυρία | `the mistress` | `the mistress, the lady of the house` | 16:4, 16:9 |
| κόλπος | `the bosom` | `the bosom, the womb, the fold formed by a loose garment, the pocket, any hollow, the deep hollow between waves, the bay and gulf, the vale` | 16:5 |
| λαλέω | `of the one talking` | `of the one talking, chatting, prattling, babbling, saying, talking of, speaking, chattering, chirping` | 16:13 |
| οἰκέω | `to inhabit` | `to inhabit, to occupy, to dwell and live, to be settled` | 16:3 |
| παιδίσκη | `a young girl` | `a young girl and maiden, a young slave and courtesan` | 16:1 |
| παιδίσκη | `the young girl` | `the young girl and maiden, the young slave and courtesan` | 16:2, 16:5, 16:6 |
| παιδίσκη | `young girl` | `young girl and maiden, young slave and courtesan` | 16:3, 16:8 |
| πηγή | `of the running waters` | `of the running waters, of the streams, of the fount, of the source, of the origin` | 16:7 |
| πλῆθος | `of the great number` | `of the great number and throng and crowd and multitude, of the greater number and greater part and mass and main body, of the majority and people, of the populace and mob, of the quantity, of the number, of the magnitude and size, of the extent, of the amount, of the length` | 16:10 |
| πορεύομαι | `you are driven` | `you are driven, you are carried, you go, you walk, you march, you go across and pass` | 16:8 |
| πόθεν | `whence` | `whence, from what source, whence and wherefore` | 16:8 |
| συγκλείω | `shut` | `shut and cooped up and hemmed in and enclosed, set together to fight as in the lists, shut close and closed, locked, closed up, was well linked` | 16:2 |
| συλλαμβάνω | `collected` | `collected and gathered together, took up, laid hold of and seized, comprehended, conceived` | 16:4 |
| τίκτω | `was bringing into the world` | `was bringing into the world, was bringing forth, was bearing, was begetting, was producing and yielding` | 16:1 |
| ταπείνωσις | `to the humiliation` | `to the humiliation and abasement and defeat, to the low estate and low condition` | 16:11 |
| ταπεινόω | `be lowered` | `be lowered, be lessened, be disparaged, be humbled and abased, be made lowly and humbled, humble oneself` | 16:9 |
| φρέαρ | `the well` | `the well, the tank and cistern and reservoir, the oil jar` | 16:14 |
| χείρ | `the hands` | `the hands, the hands and arms, the arms` | 16:9, 16:12 |
| χείρ, with ἐν | `in the hands` | `within, inside of, and by means of the hands, the hands and arms, the arms` | 16:6 |
| χράομαι | `use` | `use, have and use, indulge, experience and suffer and be subject to, come to, live under, make use of, treat, be intimate with, be in need and yearn after, have in use and possess` | 16:6 |
| ἀδελφός | `of the sons of the same mother` | `of the sons of the same mother, of the brothers, of the near kinsmen` | 16:12 |
| ἀδικέω | `I am done wrong` | `I am done wrong and wronged and injured, I am spoiled and damaged, I do wrong, I am wronged` | 16:5 |
| ἀποδιδράσκω | `I run away` | `I run away and off and escape, I flee from, I desert, I flee and shun` | 16:8 |
| ἀποδιδράσκω | `ran away` | `ran away and off and escaped, fled from, deserted, fled and shunned` | 16:6 |
| ἀποστρέφω | `be turned` | `be turned, be turned back, be turned away, be brought back, turn oneself about` | 16:9 |
| ἀριθμέω | `will be numbered` | `will be numbered, will be counted and reckoned up, will be counted out and paid, will be reckoned and counted as, will be reckoned, will be counted` | 16:10 |
| ἀτιμάζω | `I was held in no honour` | `I was held in no honour and esteemed lightly and dishonoured and slighted, I was treated as unworthy of and deemed unworthy, I was deprived of civil rights, I suffered dishonour` | 16:5 |
| ἀτιμάζω | `was held in no honour` | `was held in no honour and esteemed lightly and dishonoured and slighted, was treated as unworthy of and deemed unworthy, was deprived of civil rights, suffered dishonour` | 16:4 |
| ἄγγελος | `a messenger` | `a messenger and envoy, one that announces, a divine messenger and an angel` | 16:7 |
| ἄγγελος | `the messenger` | `the messenger and envoy, the one that announces, the divine messenger and the angel` | 16:8, 16:9, 16:10, 16:11 |
| ἄγροικος | `of or in the country` | `of or in the country, dwelling in the country and a countryman and rustic, clownish and boorish and rude, rough and uncultivated` | 16:12 |
| ἐπακούω | `listened` | `listened, hearkened to and heard, gave ear and hearkened, obeyed` | 16:11 |
| ἐφοράω | `the one having overseen` | `the one having overseen and having observed and having surveyed, having watched over and taken notice of, having looked upon and beheld` | 16:13 |
| ἔρχομαι | `you come` | `you come, you go, you go back and return, you are going to and intend, you come within a little of and are near` | 16:8 |
| ἔχω | `has` | `has, holds, possesses, keeps, dwells in and inhabits, holds fast, bears up against and supports` | 16:4, 16:5 |
| ἔχω | `you have` | `you have, you hold, you possess, you keep, you dwell in and inhabit, you hold fast, you bear up against and support` | 16:11 |
| ὁδός, with ἐν | `in the way` | `within, inside of, and by means of the way, the path, the track, the road, the highway, the course, the journey, the manner and method` | 16:7 |
| ὁράω | `having been seen` | `having been seen, having been looked at, having been beheld and perceived and observed, having been looked out for` | 16:13 |
| ὑπακούω | `listened` | `listened and hearkened and gave ear, made answer when called, hearkened to and gave ear to and attended to, answered, answered to a charge, submitted to, yielded to and complied with, gave way and submitted and complied, answered one's expectations and succeeded, was subject` | 16:2 |

### Words new in GEN 15

- δή — Perseus tags the entry's opening only as *exactness*, from "Particle used to give greater
  exactness", a description, and its other tags are pieces of examples (*all* alone, *quite* the
  greatest). The chain is the entry's own gloss, *now, in truth, indeed, surely, really*. 15:5.
- εὐθύς of time — Middle Liddell's second entry, the adverb, whose εὐθύ is *straight* of place and
  εὐθύς *straightway, forthwith, at once* of time; the place senses are skipped by name. 15:4.
- ἐπειδή — not in Middle Liddell; LSJ reads "v. ἐπεί", so the chain is ἐπεί's. 15:3, 15:17.
- καπνίζω — its first sense, *to make smoke, i. e. to make a fire*, has no object a passive could
  make its subject, so the second, *to smoke, blacken with smoke*, heads the passive participle, and
  the first follows in its own voice. 15:17.
- λογίζομαι — the aorist passive takes each sense in the passive; *to form calculations*, which has
  no passive, is left out. 15:6.
- θάπτω — *to pay the last dues to a corpse* in the passive: `having had the last dues paid to a
  corpse`. 15:15.
- τοῦ ποταμοῦ τοῦ μεγάλου — the second article is plain `the` and the adjective takes no `of`, as
  τοῦ θεοῦ τοῦ ὑψίστου at 14:18. 15:18.
- One sense each in GEN 15, so plain text: τριετίζω `being three years old` (15:9, LSJ); τρυγών
  `turtle-dove` (15:9); ἀλλήλων `to one another` (15:10), whose one sense is its case forms; γῆρας
  `old age` (15:15); τέταρτος `fourth` (15:16); τετρακόσιοι `four hundred` (15:13).

| lemma | headword | chain | used |
| --- | --- | --- | --- |
| αἴξ | `a goat` | `a goat, the wild goat and the ibex, waves` | 15:9 |
| γίνομαι | `was coming into being` | `was coming to be, was arising, was being brought into existence` | 15:17 |
| γενεά | `race` | `race and stock and family, breed, tribe and nation, race and generation, offspring, birth-place, age and time of life, time of birth` | 15:16 |
| γινώσκω | `I will learn to know` | `I will learn to know, I will perceive, I will mark, I will learn, I will discern and distinguish` | 15:8 |
| γινώσκω | `you will learn to know` | `you will learn to know, you will perceive, you will mark, you will learn, you will discern and distinguish` | 15:13 |
| δάμαλις | `a heifer` | `a heifer, a girl` | 15:9 |
| δή | `now` | `now, in truth, indeed, surely, really` | 15:5 |
| δίδωμι | `you will give` | `you will give, you will grant, you will provide, you will give over and deliver up` | 15:2 |
| δεσπότης | `master` | `master and lord and master of the house, despot and absolute ruler, owner and master and lord` | 15:2, 15:8 |
| διέρχομαι | `went through` | `went through and passed through, went through in detail` | 15:17 |
| διαιρέω | `took one from another` | `took one from another and cleaved in twain and divided into parts, divided, distinguished, determined` | 15:10 |
| διατίθεμαι | `arranged as he liked` | `arranged as he liked and disposed of, disposed of his property and devised it by will, set out for sale and disposed of, arranged mutually, made a covenant with, settled with` | 15:18 |
| δικαιοσύνη | `righteousness` | `righteousness and justice` | 15:6 |
| διχοτόμημα | `of the halves of a thing cut in two` | `of the halves of a thing cut in two, of the portions of a thing cut up` | 15:17 |
| διχοτόμημα | `the halves of a thing cut in two` | `the halves of a thing cut in two, the portions of a thing cut up` | 15:11 |
| δουλεύω | `they may be slaves` | `they may be slaves, they may serve and be subject to` | 15:14 |
| δουλόω | `they will make a slave of` | `they will make a slave of and enslave, they will make one's slave and make subject to oneself and enslave, they will be enslaved` | 15:13 |
| δυσμή | `settings` | `settings, quarters of sunset and wests` | 15:12 |
| δυσμή | `to settings` | `to settings, to quarters of sunset and wests` | 15:17 |
| δύναμαι | `you will be able` | `you will be able and capable and strong enough, you will be powerful and mighty, you will have influence, you will dare and bear, you will pass for, you will be worth, you will be equivalent to, you will signify and mean, you will avail` | 15:5 |
| εἰρήνη | `of peace` | `of peace and time of peace` | 15:15 |
| εὐθύς | `straightway` | `straightway and forthwith and at once, just, directly and simply` | 15:4 |
| θάπτω | `having had the last dues paid` | `having had the last dues paid to a corpse and been honoured with funeral rites, having been buried and interred` | 15:15 |
| κακόω | `they will treat ill` | `they will treat ill and maltreat and afflict and distress, they will spoil and ruin, they will suffer ill and be in ill plight and be distressed` | 15:13 |
| καπνίζω | `being smoked` | `being smoked and blackened with smoke, making smoke and making a fire, being black with smoke` | 15:17 |
| κλίβανος | `an earthen vessel` | `an earthen vessel and a pan` | 15:17 |
| κληρονομέω | `I will receive a share of an inheritance` | `I will receive a share of an inheritance and inherit a portion, I will inherit, I will be an inheritor, I will succeed` | 15:8 |
| κληρονομέω | `to receive a share of an inheritance` | `to receive a share of an inheritance and inherit a portion, to inherit, to be an inheritor, to succeed` | 15:7 |
| κληρονομέω | `will receive a share of an inheritance` | `will receive a share of an inheritance and inherit a portion, will inherit, will be an inheritor, will succeed` | 15:3, 15:4 |
| κρίνω | `I will pick out` | `I will pick out and choose, I will pick out for oneself and choose, I will decide, I will judge, I will adjudge, I will judge of and estimate, I will expound and interpret, I will determine, I will question, I will bring to trial and accuse, I will pass sentence upon and condemn, I will be chosen, I will be brought to trial` | 15:14 |
| κριός | `a ram` | `a ram, a battering-ram` | 15:9 |
| λέγω | `says` | `says, speaks, declares, calls by name, tells` | 15:2 |
| λέγω | `was said` | `was said, was spoken, was declared, was called by name, was told` | 15:13 |
| λαμπάς | `torches` | `torches, beacon-lights, oil-lamps, lights, torch-races, races` | 15:17 |
| λογίζομαι | `was counted` | `was counted, was reckoned and calculated and computed, was set down, was set down to one's account and charged, was deducted, was taken into account and calculated and considered, was counted and deemed and considered, was reckoned upon and expected, was counted upon, was concluded by reasoning and inferred, was counted and calculated` | 15:6 |
| μέσος | `middle` | `middle, in the middle, the centre, mid, between two` | 15:10 |
| μισθός | `the wages` | `the wages and pay and hire, the recompense and reward, the payment and requital` | 15:1 |
| οἰκογενής | `of the born in the house` | `of the born in the house and homebred` | 15:2 |
| οἰκογενής | `the born in the house` | `the born in the house and homebred` | 15:3 |
| οὐρανός | `the heaven` | `the heaven, the vault, the firmament and the sky` | 15:5 |
| οὔπω | `not yet` | `not yet, no longer and no more, not and not at all` | 15:16 |
| πάροικος | `dwelling beside` | `dwelling beside, a neighbour, a sojourner and alien` | 15:13 |
| πατήρ | `the fathers` | `the fathers, the grandfathers` | 15:15 |
| περί + accusative | `round about` | `round about, round, near, somewhere near, off, who are about one, about which one is occupied and concerned, about and in, about and in the case of, about and in respect of and in regard to` | 15:12 |
| περιστερά | `common pigeon` | `common pigeon, dove` | 15:9 |
| πιστεύω | `trusted` | `trusted, trusted to and in, put faith in, relied on, believed in, believed, believed on, believed mutually, complied, believed that and felt sure and confident that, dared, believed and had faith, entrusted, was trusted and believed, was entrusted with` | 15:6 |
| πολύς | `of much` | `of much and mighty and great, of many, of deep, of loud, of strong, of large and wide, of far, of long, often` | 15:14 |
| ποταμός | `of river` | `of river and stream, of river-god` | 15:18 |
| ποταμός | `of the river` | `of the river and stream, of the river-god` | 15:18 |
| πῦρ | `of fire` | `of fire, of the funeral-fire, of the fire of the hearth` | 15:17 |
| σκοτεινός | `dark` | `dark, darkling and blind, dark and obscure` | 15:12 |
| συγκαθίζω | `made to sit together` | `made to sit together, sat in conclave and met for deliberation, sat with` | 15:11 |
| σῶμα | `the bodies` | `the bodies, the dead bodies and corpses and carcases, the living bodies, the bodies and any material substances, the whole bodies and masses` | 15:11 |
| ταπεινόω | `they will lower` | `they will lower, they will lessen, they will disparage, they will humble and abase, they will make lowly and humble` | 15:13 |
| φλόξ | `a flame` | `a flame, a flash, the fiery strength` | 15:17 |
| φοβέομαι | `be put to flight` | `be put to flight, flee affrighted, flee, be seized with fear, be affrighted, fear` | 15:1 |
| φόβος | `flight` | `flight, panic fear, fear and terror, outward show of fear, object of terror` | 15:12 |
| χώρα | `of space in which a thing is` | `of space in which a thing is, of place, of position and post, of place in life and station, of land and country, of piece of land and estate and farm, of country` | 15:7 |
| ἀλλά | `otherwise` | `otherwise, but, except, yet, but then and however, but really and certainly` | 15:4 |
| ἀναβλέπω | `look up` | `look up, look, look up at, cast up, recover one's sight` | 15:5 |
| ἀναπληρόω | `have been filled up` | `have been filled up and stand filled up, have been made up and supplied and stand so, have been filled and stand filled, have been paid in full and stand so` | 15:16 |
| ἀντιπρόσωπος | `with the face towards` | `with the face towards and facing, face to face` | 15:10 |
| ἀπολύω | `I am loosed from` | `I am loosed from, I am undone, I am set free from and released, I am relieved from, I am acquitted, I am let go free on receipt of ransom and held to ransom, I am ransomed and redeemed, I am discharged and disbanded, I am dismissed, I am divorced, I am redeemed, I am done away with, I depart, I am set free from, I am released and let off, I am freed from, I am acquitted and discharged, I am separated and part` | 15:2 |
| ἀποσκευή | `of removal` | `of removal and riddance, of baggage, of household stuff, of ordure and filth` | 15:14 |
| ἀποστρέφω | `they will be turned` | `they will be turned, they will be turned back, they will be turned away, they will be brought back, they will turn themselves about` | 15:16 |
| ἀριθμέω | `number` | `number, count and reckon up, count out and pay, reckon and count as, be reckoned, be counted` | 15:5 |
| ἀστήρ | `the stars` | `the stars, the flames and lights and fires` | 15:5 |
| ἁμαρτία | `the failures` | `the failures and faults and sins, the guilts and sins` | 15:16 |
| ἄτεκνος | `without children` | `without children and childless, destroying children` | 15:2 |
| ἐξάγω | `the one having led out` | `the one having led out, having led and carried out from, having brought forth into the world, having marched out, having ejected, having carried out and exported, having drawn off, having called forth and excited, having led on and tempted` | 15:7 |
| ἐξέρχομαι | `they will go out of` | `they will go out of, they will come out, they will go away and march off, they will go forth` | 15:14 |
| ἐξέρχομαι | `will go out of` | `will go out of, will come out, will go away and march off, will go forth` | 15:4 |
| ἐπειδή, ἐπεί | `after that` | `after that, after, since, when, from the time when and ever since, whenever, as soon as, seeing that, for, although, else and otherwise` | 15:3, 15:17 |
| ἐπιπίπτω | `falls upon` | `falls upon, attacks and assails` | 15:12 |
| ἔθνος | `the number of people accustomed to live together` | `the number of people accustomed to live together and company and body of men, the host, the swarms and flocks, the nation and people, the nations and gentiles, the special class, the caste and tribe, the sex` | 15:14 |
| ἥλιος | `of sun` | `of sun, of day and a day, of Helios the sun-god` | 15:12 |
| ἥλιος | `the sun` | `the sun, the day and a day, Helios the sun-god` | 15:17 |
| ὄρνεον | `birds` | `birds, bird-market` | 15:11 |
| ὅραμα, with ἐν | `in that which is seen` | `within, inside of, and by means of that which is seen and a sight and spectacle` | 15:1 |
| ὑπερασπίζω | `I cover with a shield` | `I cover with a shield, I defend` | 15:1 |
| ὧδε | `in this wise` | `in this wise and so and thus, so very and so exceedingly, thus and as follows, hither and here` | 15:14, 15:16 |
| ῥῆμα | `that which is said` | `that which is said and spoken, a word, a saying, a phrase, the subject of speech and a thing, a verb` | 15:1 |
| ῥῆμα | `the things which are said` | `the things which are said and spoken, the words, the sayings, the phrases, the subjects of speech and things, the verbs` | 15:1 |

### Small words new in GEN 14

- πρός + dative — **headword** `hard by`, the entry's first sense for that case; **chain** `hard by,
  near, at, on, in, among, close to, before and in the presence of, upon and against, employed in,
  in addition to and besides`. 14:13.
- πλήν with a genitive — **headword** `more than`, the preposition's first sense; **chain** `more
  than, except, save, short of, save in respect, but, than, much like, only not, except that, save
  that, save so far as`, the adverb's senses after. 14:24.
- ἅμα with a dative — **headword** `at the same time with`, the preposition's sense; **chain** `at
  the same time with, together with, at once, at the same time`. 14:5.
- ὕψιστος — **headword** `highest`; **chain** `highest, loftiest`, one sense of two glosses, after a
  plain `the` for the article. 14:18–22.
- ἐν ἀριστερᾷ — **headword** `in left`, the chain of 13:9 after ἐν. 14:15.
- τὸ before an infinitive (μετὰ τὸ ἀναστρέψαι) — not printed, as at 5:4. 14:17. *(Retired before Genesis 37: the infinitive reads as a gerund with its article; see "The articular infinitive".)*
- A dative after a preposition other than ἐν keeps its `to`, as at 12:8: `hard by to the tree`
  (14:13). A name in the dative with no article of its own takes `to` as a pronoun does: `to
  Abram` (14:13).
- ἔφυγον, ἔλαβον, ἀπῆλθον, ἔφαγον — first singular or third plural by form; the headword says
  `they`, as at 3:6. 14:10, 14:11, 14:12, 14:24.
- σεαυτῷ — `for yourself`, as at 6:14. 14:21.
- One sense each in GEN 14, so plain text: the numerals `twelve`, `thirteenth`, `fourteenth`, `three
  hundred`, `ten`, `eight`, `four`, `five`, with ἔτος `years`, `year`; αἰχμαλωτεύω `has been taken
  prisoner and stands taken prisoner`, the perfect's standing state (14:14); καταδιώκω `pursued
  closely` (14:14); συνάντησις `a meeting` (14:17); οἶνος `wine` (14:18); εὐλογητός `blessed` (14:20);
  σπαρτίον `of a small cord` (14:23); νεανίσκος `the youths` (14:24).

### Small words new in GEN 13

- ὅθεν — `from whom`, the chain of 10:14. 13:3.
- οὗ, *where* — `where`, plain, as at 2:11. 13:3, 13:4, 13:14.
- τὸ πρότερον — **headword** `the before`, the entry's first sense, with the article Rahlfs prints;
  **chain** `the before, the in front and forward, the former and sooner, the elder, the above and
  superior, the earlier` — *before, sooner, earlier* is the neuter as an adverb, the verse's use.
  Middle Liddell files the superlative πρῶτος inside the entry, and its senses are left out. 13:3.
- ἅμα with no dative — **headword** `at once`; **chain** `at once, at the same time, at the same time
  with and together with`. 13:6.
- ἀνὰ μέσον ἐμοῦ καὶ σοῦ — `up to middle` and then `of me and of you`, as at 9:12. 13:8.
- ἑαυτῷ after the middle ἐξελέξατο — `for himself`, plain, after the middle's own *for himself*,
  so the reading has it twice. 13:11.
- παρά + accusative — **headword** `to the side of`, the entry's first sense for that case;
  **chain** `to the side of, motion alongside of, to, beside and near and by, passing by, beyond,
  contrary to and against, beside and except, on account of and because of and by means of, along
  the whole course of and during`. 13:18.
- εἰμί — ἦν with a dative of possession, `was`, plain, as at 11:3 and 12:20 (13:5); ἦν of place or
  state, the formula of GEN 1:2 in full (13:3, 13:6, 13:18); ἦν with a participle, `was, and kept on
  being,` (13:10), where ὡς is a headword as well; ἔστω `let be`, ἐσμεν `we are` (13:8); ἐστιν `is`
  (13:9); εἶ `are` (13:14).
- One sense each in GEN 13, so plain text: διαχωρίζω `be separated`, `were separated`, `to be
  separated` (13:9, 13:11, 13:14); λίψ `south-west wind`, Middle Liddell's *the SW. wind* with the
  abbreviation written out (13:14); διοδεύω `travel through` (13:17), as at 12:6; ἀποσκηνόω `having
  kept apart from` (13:18), whose second sense is only *= ἀποσκηνέω*, with no translation;
  θυσιαστήριον `of the altar`, `an altar` (13:4, 13:18).

### Small words new in GEN 12

- καθάπερ — `according as`, the chain of καθά at 7:9, inside whose entry it is filed. 12:4.
- τότε — **headword** `at that time`; **chain** `at that time, then, in those times and formerly, at
  one time`. 12:6.
- ὅπως with ἄν — **headword** `that`, the first conjunction sense; **chain** `that, in order that, as
  and in such manner as, how and in what manner`. 12:13.
- εὖ — **headword** `well`; **chain** `well, luckily, happily, well off`. 12:13, 12:16.
- ἕνεκεν — `on account of`, the chain of 2:24; περί + genitive — **headword** `round about`, the
  entry's first sense for that case; **chain** `round about, around, about and near, about and for
  and on account of, about and concerning, for very`. 12:13, 12:17, 12:20.
- τί τοῦτο — `why this`, as at 3:13; ἵνα τί — `that what`, as at 4:6. 12:18, 12:19.
- ἐμαυτῷ — `for myself`, plain, as the reflexives are. 12:19.
- One sense each in GEN 12, so plain text: εὐλογητός `blessed` (12:2); ἐνευλογέομαι `will be blessed
  in` (12:3), followed by the Greek's own ἐν σοί, *in you*; διοδεύω `travelled through` (12:6);
  συμπροπέμπω `to join in escorting` (12:20); θυσιαστήριον `an altar` (12:7, 12:8); ἀδελφή
  `sister` (12:13, 12:19).

### Small words new in GEN 11

- δεῦτε — **headword** `hither`; **chain** `hither, come on, come here`: one sense holding three
  glosses, a unit as ἐμφυσάω's was. 11:3, 11:4, 11:7.
- πλησίον with the article, *the neighbour* — **headword** `to the neighbour` · `of the neighbour`,
  the first noun sense inside πλησίος; **chain** `to the neighbour, to the one near and close to and
  neighbouring, to the one nigh and hard by, to one's neighbour`, in the case. 11:3, 11:7.
- ἐνώπιον — `face to face`, plain: the one translation ἐνώπιος is given; the preposition, *like
  Lat. coram*, has none. 11:28.
- νῦν — **headword** `now`; **chain** `now, even now, just now`, as at 2:23. 11:6.
- ἵνα — `that`, the chain of 3:3; ὅτε — `when`, the chain of 2:4. 11:7, 11:10.
- οὗ, *whose* (11:4) — `of which`, plain, as other relatives.
- ᾗ with no preposition (11:28) — `in which`, plain, as at 5:1.
- One sense each in GEN 11, so plain text: πλίνθος `bricks`, `the brick` (11:3); τεκνοποιέω `was
  bearing children`, the active's one sense (11:30); ἐνώπιον `face to face` (11:28); θυγάτηρ
  `daughter`; the numerals and `years`; δεύτερος `second` (11:10), with no article, as the Greek
  has none.
- The short imperfect, `was, and kept on being,`, at 11:1, where the full formula's *one* would
  stand beside εἷς's headword.

---

## Divine designations

### ὁ θεός — articular

- **headword:** `the God` — Middle Liddell, first sense *God*; articular, so *the*.
- **chain:** `he who is God definitively, the one the article marks out, the known and the only`
- **used:** GEN 1:1

Lowercase pronouns; the notes say why (GEN 1:1, *Capitals*).

### θεός — anarthrous, qualitative predicate

- **headword:** `the word was God` — the whole clause θεὸς ἦν ὁ λόγος: λόγος *the word*
  (articular), εἰμί *was* (imperfect), θεός *God* (anarthrous); English subject first.
- **chain:** `everything that God is by nature, deity in full and undiminished kind, was what that utterance was`
- **used:** JHN 1:1

The fronted anarthrous predicate restructures the clause, so the unit is the clause. The
chain must say what the subject is *by nature* without asserting identity of person and
without indefiniteness. Flag the fronting in the notes every time it occurs.

### θεοῦ — anarthrous genitive

- **headword:** `of God` — genitive; Middle Liddell *God*; anarthrous.
- **chain:** `of everything that God is by nature, of deity in full and undiminished kind`
- **used:** GEN 1:2 (πνεῦμα θεοῦ — its own unit, after πνεῦμα)

### τὸν θεόν — accusative under πρός

Rendered `the God` in the πρός headword and chain. The article is carried into English
against normal usage, because John 1:1c turns on articular τὸν θεόν against anarthrous θεός.

### κυρίου τοῦ θεοῦ — genitive

- `of lord` / `of lord / master, of the head, of master, of the Lord, of Jehovah`
- `of the God` / `of him who is God definitively, of the one the article marks out, of the known and the only`
- **used:** GEN 3:8, twice

The nominative chains, in the genitive.

### θεοί — plural, anarthrous

- **headword:** `gods` — Middle Liddell's first sense is *God*; its second, *a god*, is the
  one a plural can take, lower case as the lexicon prints it.
- **chain:** `gods, the gods, goddesses`
- **used:** GEN 3:5 (ὡς θεοί)

### θεός — singular, of another god

- **headword:** `to God` — the first sense, as the lexicon prints it; anarthrous, so no article.
- **chain:** `to God, to a god, to the god, to a goddess` — Middle Liddell's range, the oath πρὸς
  θεῶν's *the gods* in the singular. The formulas say what the God of the text is; of another
  god the text denies that, so the word is read literally, as the plural is (Q28). `NOT_SENSES`
  sets aside *his will* and *God's name* (pieces of ὑπὲρ θεόν and an oath) and the comparative
  θεώτερος's *more divine*.
- **used:** EXO 34:14 (θεῷ ἑτέρῳ)

---

## Verbs

### εἰμί — imperfect ἦν — plain text

No unit: the expansion *is* "was", expanded. It reads identically in both panels. Two settled
forms, not interchangeable:

- **state of a creature** (GEN 1:2): `was, and kept on being as a standing and continuing condition and not a momentary one`
- **pre-existence, against ἐγένετο** (JHN 1:1a): `there was, and was continuously, and was already in unbroken existence without any point of having come to be`
  - JHN 1:1b, before πρός: `was and remained`
  - **short** (JHN 1:2): `was — continuously, and without any point of having come to be —`

The second form is required anywhere the ἦν / ἐγένετο contrast is in play. Never flatten
either to *was*.

### γίνομαι — aorist ἐγένετο

- **headword:** `came into being` — Middle Liddell (filed under Attic γίγνομαι), sense I:
  *Radical sense, to come into being*; aorist middle, 3rd singular. No *there*: the Greek has
  none.
- **chain:** `there came to be, there arose, there was brought into existence`
- **used:** JHN 1:6

The verb withheld from the Logos in JHN 1:1–2. Wherever it stands against ἦν in the same
context, say so in the notes.

### ποιέω — aorist

- **headword:** `made` — Middle Liddell, first sense *to make*; aorist active, 3rd singular.
- **chain:** `made, did, produced, created`
- **used:** GEN 1:1

  Middle Liddell's first three senses: *to make*, *to do*, *to make, produce, create*.
  The chain read `fashioned, wrought, manufactured, produced, performed, and brought to a
  finished and accomplished state` from the first draft until 2026-09-18. Not one of
  *fashioned*, *wrought*, *manufactured* or *performed* is in the entry, and CLAUDE.md's
  own worked example gives ποιέω *to make* → ἐποίησεν *made*. The rest of the corpus had
  already derived it: every form but the aorist read `make, do, produce, create`.

Followed by the aorist formula as **plain text**: `— one completed act seen whole, not a
process observed in progress —`. The formula is grammar, not definition, so it sits outside
the chain.

### ἐπιφέρω — imperfect middle/passive

- **headword:** `was being brought upon` — Middle Liddell's first sense is *to bring, put, or
  lay upon*, which Perseus's markup splits into separate translations (*to bring, put* ·
  *lay upon*). Imperfect middle/passive, 3rd singular — one form in this tense — read passive, as
  the note reads it (*to be borne upon*).
- **chain:** `was being brought and put, was being laid upon, was being attacked and assailed, was being imputed, was being conferred and imposed upon, was being added to and increased, was being brought with, was being borne onwards`
- **used:** GEN 1:2

### ἀποστέλλω — perfect passive participle

- **headword:** `sent off` — Middle Liddell, first sense *to send off*; perfect passive participle.
- **chain:** `one sent off, dispatched, and commissioned on another's authority`
- **used:** JHN 1:6

Perfect — a standing status, not a past errand.

### συντελέω — aorist

- **headword:** `were brought quite to an end` (aorist passive, 3rd plural, GEN 2:1) /
  `brought quite to an end` (aorist active, 3rd singular, GEN 2:2) — Middle Liddell, first
  sense *to bring quite to an end, complete, accomplish*.
- **chain (passive):** `were brought quite to an end and completed and accomplished, were made up into the whole and into the number`
- **chain (active):** `brought quite to an end, completed, accomplished, made up into the whole and into the number`
- **used:** GEN 2:1, GEN 2:2

The *make up the whole* / *make up the number* senses are the lexicon's second and third and
stay in the chain: finishing here is also completing a count.

### καταπαύω — aorist

- **headword:** `laid to rest` — Middle Liddell, first sense *to lay to rest, put an end to*;
  aorist active, 3rd singular.
- **chain (full):** `laid to rest, put an end to, made to cease, stopped and kept in check, put down`
- **short:** `laid to rest, put an end to, made to cease`
- **used:** GEN 2:2 (full), GEN 2:3 (short)

Transitive in the lexicon's first sense, where English *rested* is intransitive. The range
runs as far as *kill*, which the chain does not carry; the note says so instead.

### εὐλογέω — aorist

- **headword:** `spoke well of` — Middle Liddell, first sense *to speak well of, praise,
  honour*; aorist active, 3rd singular. Rahlfs prints the augment ηὐ-.
- **chain:** `spoke well of, praised, honoured, blessed`
- **used:** GEN 2:3

*Blessed* is the entry's fourth gloss and comes last in the chain for that reason.

### ἁγιάζω — aorist

- **headword:** `hallowed` — no Middle Liddell entry; LSJ gives the word no gloss of its own
  either, reading `= ἁγίζω` and citing this verse, so the sense is ἁγίζω's, *hallow, make
  sacred*. Aorist active, 3rd singular.
- **chain:** `hallowed and made sacred`
- **used:** GEN 2:3

### ἄρχω — aorist middle

- **headword:** `began` — Middle Liddell's first *numbered* sense, *to begin, make a
  beginning*, marked "both in Act. and Mid."; aorist middle, 3rd singular. Perseus's opening
  gloss *in pass. sense:— to be first* belongs to the passive alone and is skipped by name in
  `NOT_SENSES` (see the headword rule above).
- **chain:** `began, made a beginning, made a beginning of, began from`
- **used:** GEN 2:3

### ποιέω — aorist infinitive

- **headword:** `to make` — the same entry as the indicative above, in the infinitive.
- **chain:** `to make, to do, to produce, to create`
- **used:** GEN 2:3 (ποιῆσαι, after ἤρξατο)

### γίνομαι — aorist infinitive

- **headword:** `to come into being` — the same entry as the indicative, in the infinitive.
- **chain:** `to come to be, to arise, to be brought into existence`
- **used:** GEN 2:5 (γενέσθαι, under πρὸ τοῦ)

### ἀνατέλλω — aorist infinitive

- **headword:** `to make to rise up` — Middle Liddell, first sense *to make to rise up*.
- **chain:** `to make to rise up, to grow up, to give birth to and bring to light, to rise, to take its rise, to grow`
- **used:** GEN 2:5 (ἀνατεῖλαι, under πρὸ τοῦ)

Transitive first, intransitive later, and the LXX uses it intransitively of the plant.

### βρέχω — aorist

- **headword:** `rained` — Middle Liddell's second sense, *to rain, send rain*, which the
  entry marks as New Testament usage. Every translation Perseus tags in the first sense
  stands inside that sense's `:—Pass.` clause, and its active gloss (*to wet*, Lat. *rigo*)
  is never tagged at all, so the passive glosses are skipped by name in `NOT_SENSES` — the
  same treatment as ἄρχω, for the same reason. Aorist active, 3rd singular.
- **chain:** `rained, sent rain`
- **used:** GEN 2:5

### ἐργάζομαι — present infinitive

- **headword:** `to work` — Middle Liddell, first sense *to work, labour*.
- **chain:** `to work, to labour, to work at and make and build, to do and perform and accomplish, to work the land, to earn by working`
- **used:** GEN 2:5

### ἀναβαίνω — imperfect

- **headword:** `was going up` — Middle Liddell, first sense *to go up, mount*; imperfect
  active, 3rd singular.
- **chain:** `was going up, was mounting, was going up to, was embarking`
- **used:** GEN 2:6

### ποτίζω — imperfect

- **headword:** `was giving to drink` — Middle Liddell, first sense *to give to drink*;
  imperfect active, 3rd singular.
- **chain:** `was giving to drink, was watering, was watering the cattle`
- **used:** GEN 2:6

### πλάσσω — aorist

- **headword:** `formed` — Middle Liddell, first sense *to form, mould, shape*; aorist
  active, 3rd singular.
- **chain:** `formed, moulded, shaped, moulded and formed by training, formed in the mind, put into a certain form`
- **used:** GEN 2:7

The potter's verb, Latin *fingere*. Not the ἐποίησεν of chapter 1.

### ἐμφυσάω — aorist

- **headword:** `blew in` — Middle Liddell gives the entry one sense and one translation,
  *to blow in: to play the flute*, where the colon marks a special application rather than a
  second sense. Aorist active, 3rd singular.
- **chain:** `blew in, played the flute`
- **used:** GEN 2:7

The chain carries the flute because the lexicon does. The note explains the colon.

### ζάω — present participle

- **headword:** `living` — Middle Liddell, first sense *to live*; present active participle,
  accusative singular feminine, agreeing with ψυχήν.
- **chain:** `living, alive, in full life and strength and fresh and strong`
- **used:** GEN 2:7

### φυτεύω — aorist

- **headword:** `planted` — Middle Liddell, first sense *to plant*; aorist active, 3rd singular.
- **chain:** `planted, planted for himself, begot, produced and brought about and caused`
- **used:** GEN 2:8

### τίθημι — aorist middle

- **headword:** `set` — Middle Liddell, first sense *to set, put, place*; aorist middle,
  3rd singular.
- **chain:** `set, put, placed, planted, laid`
- **used:** GEN 2:8

### ἐξανατέλλω — plain text

`sprang up from`. No unit: Middle Liddell gives the entry a single sense, *to spring up
from*, so there is no range to open. The LXX uses it transitively — God made the trees spring
up — where the lexicon has it intransitive; the verse's note records that. GEN 2:9.

### οἶδα — perfect infinitive

- **headword:** `to know` — Middle Liddell, first sense *to know*; perfect active infinitive,
  articular (τοῦ εἰδέναι).
- **chain:** `to know, to be assured, to be versed in`
- **used:** GEN 2:9

### ἐκπορεύομαι — present

- **headword:** `goes out` — filed under the active ἐκπορεύω, whose opening gloss, *to make
  to go out, fetch out*, is the active alone and is skipped by name; the middle glosses the
  entry tags next, *to go out* and *forth, march out*, are this form. Present middle,
  3rd singular.
- **chain:** `goes out, goes forth, marches out`
- **used:** GEN 2:10

### ἀφορίζω — present middle/passive

- **headword:** `is marked off by boundaries` — Middle Liddell, first sense *to mark off by
  boundaries*; present, 3rd singular, one form for middle and passive.
- **chain:** `is marked off by boundaries, is distinguished and determined and defined, is banished, is set apart and separated, is cast out and excommunicated, is set apart, is appointed and ordained`
- **used:** GEN 2:10

### κυκλόω — present participle

- **headword:** `the one encircling` — Middle Liddell, first sense *to encircle, surround*;
  present active participle, articular.
- **chain:** `the one encircling and surrounding, moving in a circle and whirling round, forming into a
  circle` — the active's three senses, each run whole. It had read `the one encircling, surrounding,
  moving in a circle, going round`, a run split and the middle's *to go round* taken in; EXO 13 set it
  right beside the aorist `encircled`.
- **used:** GEN 2:11, GEN 2:13

### πορεύομαι — present participle

- **headword:** `the one being driven` — filed under the active πορεύω. Sense I is marked
  *Act.* and is skipped by name; sense II is marked *Pass. and Mid.* and is kept whole, so
  its first translation, *to be driven or carried*, stands — the middle has a claim on it.
  *To go, walk, march* follows in the same sense group. Present middle participle, articular.
- **chain:** `the one being driven, being carried, going, walking, marching, going across and passing`
- **used:** GEN 2:14

### λαμβάνω — aorist

- **headword:** `took` — Middle Liddell, first sense *to take*; aorist active, 3rd singular.
- **chain:** `took, received, took hold of and grasped and seized`
- **used:** GEN 2:15

### φυλάσσω — present infinitive

- **headword:** `to keep watch and ward` — Middle Liddell, first sense *to keep watch and
  ward, keep guard*.
- **chain:** `to keep watch and ward, to keep guard, to watch and guard and keep and defend`
- **used:** GEN 2:15

A sentry's word before it is a gardener's. The garden is given a guard, not only a keeper.

### ἐντέλλομαι — aorist middle

- **headword:** `enjoined` — filed under the active ἐντέλλω, whose single sense, *to enjoin,
  command*, is not restricted to a voice, so nothing is skipped. Aorist middle, 3rd singular.
- **chain:** `enjoined, commanded`
- **used:** GEN 2:16

### λέγω

- **headword:** `saying` (present active participle, GEN 2:16) / `said` (aorist, GEN 2:18).
  The lexicon prints three entries under this spelling: λέγω¹ *to lull to sleep*, λέγω²
  *to gather, pick up*, λέγω³ *to say, speak*. The third is the word (see *Homographs*).
- **chain:** `saying, speaking, declaring, calling by name, telling`
- **used:** GEN 2:16, GEN 2:18

### ἐσθίω — future and aorist subjunctive

- **headword:** `you will eat` (future middle, 2nd singular GEN 2:16, plural GEN 2:17) /
  `you may eat` (aorist subjunctive, GEN 2:17) — Middle Liddell, first sense *to eat*.
- **chain:** `you will eat, you will eat of` / `you may eat, you may eat of`
- **used:** GEN 2:16, GEN 2:17

### γινώσκω — present infinitive

- **headword:** `to learn to know` — Middle Liddell, first sense *to learn to know, to
  perceive, mark, learn*. Filed under the Attic γιγνώσκω.
- **chain:** `to learn to know, to perceive, to mark, to learn, to discern and distinguish`
- **used:** GEN 2:17

Not οἶδα. The tree is τοῦ εἰδέναι at 2:9 and τοῦ γινώσκειν at 2:17 — knowledge one has,
against knowledge one comes by — and the two headwords keep the two verbs apart.

### ἀποθνῄσκω — future middle

- **headword:** `you will die off` — Middle Liddell, first sense *to die off, die*; future
  middle, 2nd plural. Perseus keys it without the iota subscript, `a)poqnh/skw`.
- **chain:** `you will die off and die, you will be put to death and slain`
- **used:** GEN 2:17

### ἄγω — aorist

- **headword:** `led` — Middle Liddell, first sense *to lead*; aorist active, 3rd singular.
- **chain:** `led, carried, conveyed, brought, marched`
- **used:** GEN 2:19

### ὁράω — aorist infinitive

- **headword:** `to see` — Middle Liddell, first sense *to see*; aorist infinitive (ἰδεῖν).
- **chain:** `to see, to perceive, to behold, to look at`
- **used:** GEN 2:19

### καλέω

- **headword:** `he will call` (future, GEN 2:19) / `called` (aorist, GEN 2:19, 2:20) —
  Middle Liddell, first sense *to call, summon*.
- **chain:** `called, summoned, called to himself, invited`
- **used:** GEN 2:19, GEN 2:20

### εὑρίσκω — aorist passive

- **headword:** `was found` — Middle Liddell, first sense *to find*; aorist passive,
  3rd singular.
- **chain:** `was found, was found out, was discovered`
- **used:** GEN 2:20

A search that came to nothing, not a simple absence.

### ἐπιβάλλω — aorist

- **headword:** `threw` — Middle Liddell, first sense *to throw*; aorist active, 3rd singular.
- **chain:** `threw, cast upon, laid on, affixed, added`
- **used:** GEN 2:21

### ὑπνόω — aorist

- **headword:** `put to sleep` — Middle Liddell, first sense *to put to sleep*, transitive and
  causative; *to fall asleep, sleep* is its second. Aorist active, 3rd singular.
- **chain:** `put to sleep, fell asleep and slept`
- **used:** GEN 2:21

The Septuagint uses the active intransitively — *and he slept*. The headword keeps the
lexicon's order and the verse's note carries the usage.

### ἀναπληρόω — aorist

- **headword:** `filled up` — Middle Liddell, first sense *to fill up*; aorist active,
  3rd singular.
- **chain:** `filled up, made up and supplied, filled, paid in full`
- **used:** GEN 2:21

Making good a deficiency — a gap in a line of troops, a debt paid in full.

### οἰκοδομέω — aorist

- **headword:** `built a house` — Middle Liddell, first sense *to build a house*, before the
  general *to build*. Aorist active, 3rd singular.
- **chain:** `built a house, built, built for himself`
- **used:** GEN 2:22

### λαμβάνω — aorist passive

- **headword:** `was taken` — the same entry as the active `took`; aorist passive,
  3rd singular.
- **chain:** `was taken, was received, was taken hold of and seized`
- **used:** GEN 2:23

### καλέω — future passive

- **headword:** `she will be called` — the same entry as `called`; future passive,
  3rd singular.
- **chain:** `she will be called, she will be summoned, she will be invited`
- **used:** GEN 2:23

### καταλείπω — future

- **headword:** `will leave behind` — Middle Liddell, first sense *to leave behind*; future
  active, 3rd singular.
- **chain:** `will leave behind, will leave as an heritage, will forsake and abandon and leave in
  the lurch, will leave remaining, will leave alone` *(corrected at Genesis 39: the chain had
  the middle's* behind him *and* inheritance *for the entry's* heritage*)*
- **used:** GEN 2:24

### προσκολλάω — future passive

- **headword:** `will be glued on` — Middle Liddell, first sense *to glue on*; future
  passive, 3rd singular. `NOT_SENSES` drops the scrap *to*, sliced from "to glue on or to".
- **chain:** `will be glued on, will stick, will cleave to`
- **used:** GEN 2:24

Passive in form where English makes it active. κόλλα is glue; *collagen* is its relative.

### αἰσχύνω — imperfect middle/passive

- **headword:** `were being ashamed` — sense I and its subsenses are the active (*to make
  ugly, disfigure, mar*; *to dishonour*) and are skipped by name; the first numbered sense
  open to this voice is II, *to be ashamed, feel shame*. Imperfect, 3rd plural, one form for
  middle and passive.
- **chain:** `were being ashamed, were feeling shame, were being dishonoured`
- **used:** GEN 2:25

### Verbs new in GEN 3

Each headword is Middle Liddell's first sense, in the form the text uses, unless a note says
otherwise.

| lemma | form | headword | chain | used |
| --- | --- | --- | --- | --- |
| ἐσθίω | aor. 3 sg / 3 pl / 1 sg / 2 sg | `ate` · `they ate` · `I ate` · `you ate` | `ate, ate of` (with the person) | 3:6, 3:11, 3:12, 3:13, 3:17 |
| ἐσθίω | fut. 1 pl | `we will eat` | `we will eat, we will eat of` | 3:2 |
| ἐσθίω | aor. inf. / aor. subj. 3 sg | `to eat` · `he may eat` | `to eat, to eat of` · `he may eat, he may eat of` | 3:11, 3:17, 3:22 |
| ἀποθνήσκω | aor. subj. 2 pl | `you may die off` | `you may die off and die, you may be put to death and slain` | 3:3 |
| ἅπτω | aor. mid. subj. 2 pl | `you may fasten yourselves to` | `you may fasten yourselves to and cling to and hang on by and lay hold of and grasp and touch, you may engage in and take part in, you may lay hold of and dispute, you may set upon and attack and assail, you may touch and affect, you may grasp with the senses and apprehend and perceive, you may come up to and reach and gain` | 3:3 |
| οἶδα | pluperf. 3 sg | `knew` | `knew, was assured, was versed in` | 3:5 |
| διανοίγω | fut. / aor. pass. 3 pl | `will be opened` · `were opened` | `will be opened, will be opened and explained` · `were opened, were opened and explained` | 3:5, 3:7 |
| γινώσκω | pres. ptcp. / aor. 3 pl | `learning to know` · `learned to know` | `learning to know, perceiving, marking, learning, discerning and distinguishing` · the same in the aorist | 3:5, 3:7 |
| ὁράω | aor. 3 sg | `saw` | `saw, perceived, beheld, looked at` | 3:6 |
| κατανοέω | aor. inf. | `to observe well` | `to observe well and understand, to perceive, to learn, to consider` | 3:6 |
| λαμβάνω | aor. ptcp. / aor. subj. / aor. pass. 2 sg | `having taken` · `he may take` · `you were taken` | `having taken, having received, having taken hold of and grasped and seized` · likewise | 3:6, 3:19, 3:22 |
| δίδωμι | aor. 3 sg / 2 sg | `gave` · `you gave` | `gave, granted, provided, gave over and delivered up` | 3:6, 3:12 |
| ῥάπτω | aor. 3 pl | `sewed` | `sewed, stitched together, devised and contrived and plotted` | 3:7 |
| ἀκούω | aor. 3 pl / 1 sg / 2 sg | `heard` · `I heard` · `you heard` | `heard, had hearing of, heard tell of, hearkened and gave ear, listened to and obeyed` | 3:8, 3:10, 3:17 |
| περιπατέω | pres. ptcp. | `walking up and down` | `walking up and down, walking about, walking, living` | 3:8, 3:10 |
| κρύπτω | aor. pass. 3 pl / 1 sg | `were hidden` · `I was hidden` | `were hidden and covered and cloaked, hid themselves and lay hidden, were concealed and kept secret` | 3:8, 3:10 |
| φοβέομαι | aor. pass. 1 sg | `I was put to flight` | `I was put to flight, I fled affrighted, I fled, I was seized with fear, I was affrighted, I feared` | 3:10 |
| ἀναγγέλλω | aor. 3 sg | `carried back tidings of` | `carried back tidings of, reported` | 3:11 |
| ἐντέλλομαι | aor. 1 sg | `I enjoined` | `I enjoined, I commanded` | 3:11, 3:17 |
| ποιέω | aor. 2 sg | `you made` | `you fashioned, you wrought, you produced, you performed, you did` | 3:13, 3:14 |
| ἀπατάω | aor. 3 sg | `cheated` | `cheated and tricked and outwitted and beguiled, deceived` | 3:13 |
| πορεύομαι | fut. 2 sg | `you will be driven` | `you will be driven, you will be carried, you will go, you will walk, you will march` | 3:14 |
| τίθημι | fut. 1 sg | `I will set` | `I will set, I will put, I will place, I will plant, I will lay` | 3:15 |
| τηρέω | fut. 3 sg / 2 sg | `will watch over` | `will watch over and protect and guard, will give heed to and watch narrowly, will watch for, will keep` | 3:15 |
| πληθύνω | pres. ptcp. / fut. 1 sg | `making full` · `I will make full` | `making full and increasing and multiplying` · likewise | 3:16 |
| τίκτω | fut. mid. 2 sg | `you will bring into the world` | `you will bring into the world, you will bring forth, you will bear, you will produce` | 3:16 |
| κυριεύω | fut. 3 sg | `will be lord` | `will be lord, will be master of, will have legal power` | 3:16 |
| ἀνατέλλω | fut. 3 sg | `will make to rise up` | the chain of GEN 2:5, in the future | 3:18 |
| ἀποστρέφω | aor. inf. | `to turn` | `to turn, to turn back, to turn away, to turn oneself about, to bring back` | 3:19 |
| ἀπέρχομαι | fut. 2 sg | `you will go away` | `you will go away, you will depart from, you will depart, you will depart from life` | 3:19 |
| ζάω | pres. ptcp. gen. pl. / fut. 3 sg | `of the living` · `he will live` | `of the living, of the alive, of those in full life and strength, of the fresh and strong` · `he will live, he will be in full life and strength and fresh and strong` | 3:20, 3:22 |
| ἐνδύω | aor. 3 sg | `clothed in` | `clothed in, clothed` — sense II, the causal aorist | 3:21 |
| γίνομαι | perf. 3 sg | `has come into being` | `has come to be and stands so, has arisen and remains arisen, has been brought into existence and continues so` — a standing resultant state | 3:22 |
| ἐκτείνω | aor. subj. 3 sg | `he may stretch out` | `he may stretch out, he may spread out, he may put forth` | 3:22 |
| ἐξαποστέλλω | aor. 3 sg | `sent quite away` | `sent quite away, dispatched` | 3:23 |
| ἐκβάλλω | aor. 3 sg | `threw` | `threw, cast out of, threw out, cast out and banished, deposed, threw away and rejected` | 3:24 |
| κατοικίζω | aor. 3 sg | `removed to` | `removed to, planted, settled, established as a colonist, restored to one's country` | 3:24 |
| τάσσω | aor. 3 sg | `arranged` | `arranged and put in order, drew up in order of battle, posted and stationed, appointed` | 3:24 |
| στρέφω | pres. mid./pass. ptcp. | `the one turning itself` | `the one turning itself, turning round, turning about, turning to and fro, turning back, revolving` — the entry's actives skipped by name | 3:24 |

### Verbs new in GEN 4

| lemma | form | headword | chain | used |
| --- | --- | --- | --- | --- |
| γινώσκω | aor. 3 sg / pres. 1 sg | `learned to know` · `I learn to know` | the chain of GEN 3:7, in the form | 4:1, 4:9, 4:17, 4:25 |
| συλλαμβάνω | aor. ptcp. fem. | `having collected` | `having collected and gathered together, having taken up, having laid hold of and seized, having comprehended, having conceived` | 4:1, 4:17, 4:25 |
| τίκτω | aor. 3 sg / aor. inf. | `brought into the world` · `to bring into the world` | `brought into the world, brought forth, bore, produced` | 4:1, 4:2, 4:17, 4:20, 4:22, 4:25 |
| κτάομαι | aor. mid. 1 sg | `I procured for myself` | `I procured for myself, I got, I gained, I acquired` | 4:1 |
| προστίθημι | aor. / fut. 3 sg | `put to` · `will put to` | `put to, handed over and delivered, gave and bestowed, imposed further, attributed, added` | 4:2, 4:12 |
| γίνομαι | aor. 3 sg (mid. and pass.) / aor. 2 sg | `came into being` · `you came into being` | the chain of JHN 1:6, in the form | 4:2, 4:3, 4:6, 4:8, 4:18, 4:26 |
| ἐργάζομαι | pres. ptcp. / fut. 2 sg (ἐργᾷ) | `working` · `you will work` | the chain of GEN 2:5, in the form | 4:2, 4:12 |
| φέρω | aor. 3 sg | `bore` | `bore, carried, bore along, brought and fetched, brought and offered and presented` | 4:3, 4:4 |
| ἐφοράω | aor. 3 sg (ἐπεῖδεν) | `oversaw` | `oversaw and observed and surveyed, watched over and took notice of, looked upon and beheld` | 4:4 |
| προσέχω | aor. 3 sg | `held to` | `held to and offered, brought to, turned to, turned the mind to, gave heed to` | 4:5 |
| λυπέω | aor. 3 sg | `gave pain to` | `gave pain to, pained, distressed, grieved, vexed, annoyed` | 4:5 |
| συμπίπτω | aor. 3 sg | `fell together` | `fell together, met in battle and came to blows, fell in with and met, fell upon and happened, concurred` | 4:5, 4:6 |
| προσφέρω | aor. subj. 2 sg | `you may bring to` | `you may bring to, you may apply, you may lay upon, you may offer, you may present and give, you may set before` | 4:7 |
| διαιρέω | aor. subj. 2 sg | `you may take one from another` | `you may take one from another and cleave in twain and divide into parts, you may divide, you may distinguish, you may determine` | 4:7 |
| ἁμαρτάνω | aor. 2 sg | `you missed the mark` | `you missed the mark, you failed of your purpose, you went wrong, you erred, you sinned` | 4:7 |
| ἡσυχάζω | aor. impv. 2 sg | `be still` | `be still and keep quiet and at rest` | 4:7 |
| ἄρχω | fut. 2 sg, c. gen. | `will begin` | `will begin, will make a beginning of, will lead the way, will lead and rule and govern, will rule over` | 4:7 |
| διέρχομαι | aor. subj. 1 pl | `let us go through` | `let us go through and pass through, let us go through in detail` | 4:8 |
| ἀνίστημι | aor2 3 sg | `stood up` | `stood up, rose, rose to fight against, rose to go and set out` | 4:8 |
| ἀποκτείνω | aor. / fut. / aor. ptcp. / aor. 1 sg | `killed` · `will kill` · `the one having killed` · `I killed` | `killed and slew, condemned to death`, in the form | 4:8, 4:14, 4:15, 4:23, 4:25 |
| βοάω | pres. 3 sg | `cries aloud` | `cries aloud, shouts, sounds and resounds and roars, calls on, calls for` | 4:10 |
| χάσκω | aor. 3 sg (ἔχανεν) | `yawned` | `yawned, gaped, uttered with open mouth` | 4:11 |
| δέχομαι | aor. inf. | `to take` | `to take, to accept, to receive, to receive in exchange, to give ear to` | 4:11 |
| δίδωμι | aor. inf. | `to give` | `to give, to grant, to provide, to give over and deliver up` | 4:12 |
| στένω, τρέμω | pres. ptcp. | `moaning` · `trembling` | `moaning, sighing, groaning, bewailing and lamenting` · `trembling, fearing, trembling at` | 4:12, 4:14 |
| ἀφίημι | aor. pass. inf. | `to be sent forth` | `to be sent forth, to be discharged, to be sent away and let go, to be set free, to be released` | 4:13 |
| ἐκβάλλω | pres. 2 sg | `you throw` | the chain of GEN 3:24, in the form | 4:14 |
| κρύπτω | fut. pass. 1 sg | `I will be hidden` | the chain of GEN 3:10, in the form | 4:14 |
| εὑρίσκω | pres. ptcp. | `the one finding` | `the one finding, the one finding out, the one discovering` | 4:14, 4:15 |
| ἐκδικέω | pres. ptcp. pass. pl. / perf. 3 sg | `things being avenged` · `has been avenged` | `things being avenged and punished, things on which vengeance is exacted, things being avenged, things being avenged one on another` · `has been avenged and punished and stands so, has had vengeance exacted for it and stands so, has been avenged and stands so, has been avenged one on another and stands so` | 4:15, 4:24 |
| παραλύω | fut. 3 sg | `will loose from the side` | `will loose from the side and take off and detach, will undo and put an end to, will set free, will loose beside` | 4:15 |
| ἀναιρέω | aor. inf. | `to take up` | `to take up, to raise, to take up and carry off, to make away with and destroy and kill, to abolish` | 4:15 |
| ἐξέρχομαι | aor. 3 sg | `went out of` | `went out of, came out, went away and marched off, went forth` | 4:16 |
| οἰκέω | aor. 3 sg / pres. ptcp. | `inhabited` · `of those inhabiting` | `inhabited, occupied, dwelt and lived, was settled`, in the form | 4:16, 4:20 |
| οἰκοδομέω | pres. ptcp. | `building a house` | the chain of GEN 2:22, in the form | 4:17 |
| ἐπονομάζω | aor. 3 sg | `gave a surname` | `gave a surname, named, called, pronounced` | 4:17, 4:25, 4:26 |
| γεννάω | aor. 3 sg | `begot` | `begot and engendered, brought forth, produced` | 4:18 |
| καταδείκνυμι | aor. ptcp. | `the one having discovered and made known` | `the one having discovered and made known, the one having invented and taught and introduced, the one having shown how` | 4:21 |
| ἀκούω | aor. impv. 2 pl | `hear` | the chain of GEN 3:8, in the form | 4:23 |
| ἐξανίστημι | aor1 3 sg | `raised up` | `raised up, made to rise, removed and expelled, roused` | 4:25 |
| ἐλπίζω | aor. 3 sg | `hoped for` | `hoped for, looked for, expected, hoped, thought and supposed, hoped in` | 4:26 |
| ἐπικαλέω | pres. mid. inf. | `to call upon` | `to call upon, to invoke and appeal to, to invite, to call in as a helper, to be called by surname` | 4:26 |

Where the lexicon restricts a sense to one voice, the entry's own labels decide, as for ἄρχω:
φοβέω's *A. Act.*, ἅπτω's active sense I against *II. Mid. … c. gen.*, στρέφω's *B. Pass.
and Mid.* A headword that takes a person from the form says it — `they ate` and `I ate` are
one Greek form, ἔφαγον, at 3:6 and 3:12.

### Verbs new in GEN 5

| lemma | form | headword | chain | used |
| --- | --- | --- | --- | --- |
| ποιέω | aor. 3 sg | `made` | the chains of GEN 1:1 (full) and 2:2 (short) | 5:1, 5:2 |
| εὐλογέω | aor. 3 sg | `spoke well of` | the chain of GEN 2:3; Rahlfs prints εὐλόγησεν here without the augment | 5:2 |
| ἐπονομάζω | aor. 3 sg | `gave a surname` | the chain of GEN 4:17 | 5:2, 5:3, 5:29 |
| ζάω | aor. 3 sg | `lived` | `lived, was in full life and strength and fresh and strong` — the chain of GEN 3:22, in the aorist | 5:3–30 |
| γεννάω | aor. 3 sg / aor. inf. | `begot` · `to beget` | the chain of GEN 4:18, in the form | 5:3–32 |
| γίνομαι | aor. 3 pl | `came into being` | `came to be, arose, were brought into existence` — no *there*, the subject standing in the clause | 5:4–31 |
| ἀποθνήσκω | aor. 3 sg | `died off` | `died off and died, was put to death and slain` | 5:5–31 |
| εὐαρεστέω | aor. 3 sg | `was well pleasing` | `was well pleasing, seemed good and was resolved, was well pleased and satisfied` — **no Middle Liddell entry**; LSJ, citing 5:22. The passive's own senses are left out; *well pleased* is also the active's, used intransitively | 5:22, 5:24 |
| εὑρίσκω | impf. pass. 3 sg | `was being found` | `was being found, was being found out, was being discovered` | 5:24 |
| μετατίθημι | aor. 3 sg | `placed among` | `placed among, placed differently, transposed, changed and altered, put in the place of another and substituted` — the entry's *Mid.* and *Pass.* senses left out | 5:24 |
| λέγω | pres. ptcp. | `saying` | the chain of GEN 2:16 | 5:29 |
| διαναπαύω | fut. 3 sg | `will allow to rest awhile` | `will allow to rest awhile, will interrupt, will relieve, will rest awhile` — LSJ's active; Middle Liddell has only the middle | 5:29 |
| καταράομαι | aor. mid. 3 sg | `called down curses upon` | `called down curses upon and imprecated upon, cursed and execrated, uttered imprecations` — *accursed*, the entry's sense for the perfect passive participle alone, left out | 5:29 |

Every verb of the genealogy's frame is aorist. The aorist formula stands after the first
aorist of 5:1 and 5:3 and after εὐηρέστησεν and μετέθηκεν (5:22, 5:24), not after each of the
chapter's sixty-seven aorist indicatives, as GEN 4:18 set it once in a run of ἐγέννησεν.

### Verbs new in GEN 6

| lemma | form | headword | chain | used |
| --- | --- | --- | --- | --- |
| γίνομαι | pres. inf. | `to come into being` | the chain of GEN 2:5 | 6:1 |
| ἄρχω | aor. mid. 3 pl | `began` | the chain of GEN 2:3 | 6:1 |
| ὁράω | aor. ptcp. / aor. 3 sg | `having seen` · `saw` | `having seen, having perceived, having beheld, having looked at`; the chain of GEN 3:6 | 6:2, 6:5, 6:12 |
| λαμβάνω | aor. 3 pl / fut. 2 sg | `they took` · `you will take` | the chain of GEN 2:15, in the form | 6:2, 6:21 |
| ἐκλέγομαι | aor. 3 pl | `they picked out for themselves` | `they picked out for themselves and chose out, they pulled out` — the entry's *Mid.*; its actives, *to pick, single out* and *to levy taxes*, left out | 6:2 |
| καταμένω | aor. subj. 3 sg | `may stay behind` | `may stay behind and stay, may remain fixed and continue` | 6:3 |
| εἰμί | pres. inf. | `to be` | the chain of GEN 2:18 | 6:3 |
| εἰσπορεύομαι | impf. 3 pl | `were going into` | `were going into and entering` — the entry's passive gloss; *to lead into*, the active, left out | 6:4 |
| γεννάω | impf. 3 pl | `were begetting` | `were begetting and engendering, were bringing forth, were producing` | 6:4 |
| πληθύνω | aor. pass. 3 pl | `were made full` | `were made full and increased and multiplied, were in the majority and prevailed` — the passive's own gloss last | 6:5 |
| διανοέομαι | pres. / aor. 3 sg | `is minded` · `was minded` | `is minded, intends, purposes, thinks over, thinks of, thinks and supposes, is disposed`, in the form | 6:5, 6:6 |
| ἐνθυμέομαι | aor. 3 sg | `laid to heart` | `laid to heart and considered well and reflected on and pondered, thought much and deeply of, took to heart, was hurt and angry at, thought out a thing and formed a plan, inferred and concluded` | 6:6 |
| ἀπαλείφω | fut. 1 sg | `I will wipe off` | `I will wipe off and expunge, I will cancel` | 6:7 |
| ποιέω | aor. 1 sg / impv. / fut. 2 sg | `I made` · `make` · `you will make` | `I fashioned, I wrought, I produced, I performed, I did`, the chain of GEN 3:13 · `make, do, produce, create` · `you will make, you will do, you will produce, you will create` | 6:7, 6:14–16 |
| θυμόομαι | aor. pass. 1 sg | `I was wroth` | `I was wroth, I was angry, I was wild and restive, I vented fury, I was angry with, I was angry at` — *to make angry*, the active, left out | 6:7 |
| εὑρίσκω | aor. 3 sg | `found` | `found, found out, discovered` | 6:8 |
| φθείρω | aor. pass. 3 sg | `was ruined` | `was ruined and wasted and spoiled and destroyed, went to ruin and perished` — the passive's own gloss last | 6:11 |
| πίμπλημι | aor. pass. 3 sg | `was filled full of` | `was filled full of, was filled with, was filled up and filled, became full of and was full of, had enough of` — sense III, *Pass.*, last | 6:11, 6:13 |
| καταφθείρω | perf. pass. ptcp. / aor. 3 sg / pres. 1 sg / aor. inf. | `having been destroyed` · `destroyed` · `I destroy` · `to destroy` | `destroyed, spoiled utterly and brought to naught`, in the form; the perfect, `having been destroyed and standing destroyed, having been spoiled utterly and brought to naught and remaining so` | 6:12, 6:13, 6:17 |
| ἥκω | pres. 3 sg | `has come` | `has come, is present, is here, has returned, has reached a point` — the entry's own perfect sense | 6:13 |
| συντελέω | fut. 2 sg | `you will bring quite to an end` | the active chain of GEN 2:2, in the future | 6:16 |
| ἐπισυνάγω | pres. ptcp. | `collecting and bringing to` | `collecting and bringing to, gathering together` | 6:16 |
| ἐπάγω | pres. 1 sg | `I bring on` | `I bring on, I bring upon, I set on and urge on, I lead on, I bring in and invite, I bring to, I lay on and apply, I bring forward, I add` | 6:17 |
| τελευτάω | fut. 3 sg | `will complete` | `will complete, will finish, will accomplish, will fulfil, will bring about, will bring to an end, will make an end of, will end life and die, will come to an end` — the entry's passives left out | 6:17 |
| ἵστημι | fut. 1 sg | `I will make to stand` | `I will make to stand, I will set, I will stop and stay and check, I will set up and raise, I will establish and institute, I will appoint, I will weigh` — the causal tenses | 6:18 |
| εἰσέρχομαι | fut. 2 sg / 3 pl | `you will go in` · `will go in` | `you will go in, you will go into and enter, you will come into, you will come in, you will come upon`, in the form | 6:18, 6:20 |
| εἰσάγω | fut. 2 sg | `you will lead in` | `you will lead in, you will lead into and introduce, you will admit, you will import, you will call in, you will bring in and bring forward` | 6:19 |
| τρέφω | pres. subj. 2 sg / pres. inf. mid.-pass. | `you may thicken` · `to be thickened` | `you may thicken, you may congeal, you may curdle, you may make to grow and increase, you may bring up and breed and rear, you may rear and keep, you may let grow and cherish and foster, you may produce and teem with, you may contain and have, you may maintain and support` · `to be thickened, to be congealed, to be curdled, to become firm, to be made to grow and increase, to be brought up and bred and reared, to rear for oneself, to be kept, to be let grow and cherished and fostered, to be maintained and supported` | 6:19, 6:20 |
| ἕρπω | pres. ptcp. gen. pl., articular | `of the creeping` | `of the creeping and crawling, of the moving slowly and walking, of the going and coming, of the stealing on and spreading` | 6:20 |
| ἐσθίω | fut. 2 pl / aor. inf. | `you will eat` · `to eat` | the chains of GEN 2:16 and 3:11 | 6:21 |
| συνάγω | fut. 2 sg | `you will bring together` | `you will bring together, you will gather together, you will collect, you will convene, you will join in one and unite, you will receive into your house, you will draw together and narrow and contract, you will conclude and infer` | 6:21 |
| ἐντέλλομαι | aor. 3 sg | `enjoined` | the chain of GEN 2:16 | 6:22 |

τρέφω is this chapter's σπέρμα: the verb for keeping the animals alive reads, in the lexicon's
order, *thicken* and *congeal* before *rear*, *keep* and *maintain*.

### Verbs new in GEN 7

| lemma | form | headword | chain | used |
| --- | --- | --- | --- | --- |
| εἰσέρχομαι | aor. impv. / aor. 3 sg and 3 pl | `go in` · `went in` | the chain of GEN 6:18, in the form | 7:1–16 |
| εἰσπορεύομαι | pres. ptcp. n. pl., articular | `the ones going into` | `the ones going into, the ones entering` | 7:16 |
| ὁράω | aor. 1 sg | `I saw` | `I saw, I perceived, I beheld, I looked at` | 7:1 |
| εἰσάγω | aor. impv. | `lead in` | the chain of GEN 6:19, in the imperative | 7:2 |
| ἐπάγω | pres. 1 sg | `I bring on` | the chain of GEN 6:17 | 7:4 |
| ἐξαλείφω | fut. 1 sg / aor. 3 sg / aor. pass. 3 pl | `I will plaster` · `plastered` · `were plastered` | `I will plaster, I will wash over, I will wipe out and obliterate, I will strike off, I will destroy utterly`, in the form — *to plaster* or *wash over* is sense I, *to wipe out* sense II | 7:4, 7:23 |
| ῥήγνυμι | aor. pass. 3 pl | `were broken` | `were broken and broken asunder and in pieces and rent and shivered and shattered, burst, burst forth` — the entry's *Pass.* last | 7:11 |
| ἀνοίγω | aor. pass. 3 pl | `were opened` | `were opened, were undone, were laid open and unfolded and disclosed, were open and stood open` — the passive's own gloss last | 7:11 |
| κινέω | pres. mid.-pass. ptcp. | `being set in motion` | `being set in motion, being moved, being removed, being roused and stirred up, being put in motion and moving and stirring, moving forward` — the entry's *Pass.* after the first senses | 7:14, 7:21 |
| κλείω | aor. 3 sg | `shut` | `shut, closed, barred, shut up and blocked, confined` | 7:16 |
| πληθύνω | aor. pass. / impf. mid.-pass. 3 sg | `was made full` · `was being made full` | the chain of GEN 6:5, in the form | 7:17, 7:18 |
| ἐπαίρω | aor. 3 sg | `lifted up and set on` | `lifted up and set on, lifted and raised, exalted and magnified, stirred up and excited, induced and persuaded` | 7:17 |
| ὑψόω | aor. pass. 3 sg | `was lifted high` | `was lifted high and raised up, was elevated and exalted` | 7:17, 7:20, 7:24 |
| ἐπικρατέω | impf. 3 sg | `was ruling over` | `was ruling over, was holding power, was prevailing and conquering, was getting the mastery, was superior` | 7:18, 7:19 |
| ἐπιφέρω | impf. mid.-pass. 3 sg | `was being brought upon` | the chain of GEN 1:2, word for word, in the same phrase | 7:18 |
| ἐπικαλύπτω | aor. 3 sg | `covered over` | `covered over and covered up and shrouded, put as a covering over` | 7:19, 7:20 |
| ἔχω | pres. 3 sg | `has` | `has, holds, possesses, keeps, dwells in and inhabits, holds fast, bears up against and supports` | 7:22 |
| καταλείπω | aor. pass. 3 sg | `was left behind` | the chain of GEN 2:24, in the passive | 7:23 |
| ἀποθνήσκω | aor. 3 sg | `died off` | the chain of GEN 5:5 | 7:21, 7:22 |

ἐπεφέρετο ἡ κιβωτὸς ἐπάνω τοῦ ὕδατος at 7:18 repeats 1:2's πνεῦμα θεοῦ ἐπεφέρετο ἐπάνω τοῦ ὕδατος,
where the Hebrew has *face of* at both; the chain of 1:2 is reused verbatim, and *face of the
waters* is refused by `validate.py` here as there.

### Verbs new in GEN 8

| lemma | form | headword | chain | used |
| --- | --- | --- | --- | --- |
| μιμνήσκομαι | aor. pass. 3 sg | `reminded himself of` | `reminded himself of, called to mind, remembered, bethought himself of, was minded, bore in mind and did not forget` — the entry's *Mid. and Pass.*; *to remind*, the active, left out | 8:1 |
| ἐπάγω | aor. 3 sg | `brought on` | the chain of GEN 6:17, in the aorist | 8:1 |
| κοπάζω | aor. / perf. 3 sg | `grew weary` · `has grown weary` | `grew weary, abated` · `has grown weary and stands so, has abated and remains abated` | 8:1, 8:7, 8:8, 8:11 |
| ἐπικαλύπτω | aor. pass. 3 pl | `were covered over` | the chain of GEN 7:19, in the passive | 8:2 |
| συνέχω | aor. pass. 3 sg | `was held together` | `was held together, was kept together, was enclosed and encompassed and embraced, was kept from dispersing, was constrained and forced, was compressed and oppressed, was afflicted` | 8:2 |
| ἐνδίδωμι | impf. 3 sg | `was giving in` | `was giving in, was giving into hands and giving up to, was lending, was giving, was causing and exciting, was showing and exhibiting, was allowing and granting and conceding, was giving way, was yielding` | 8:3 |
| πορεύομαι | pres. ptcp. | `being driven` | the chain of GEN 2:14 | 8:3, 8:5 |
| καθίζω | aor. 3 sg | `made to sit down` | `made to sit down and seated, set and placed, encamped, set up, sat down and was seated and took its seat, settled and sank in` — the causal first, as ὑπνόω at 2:21 | 8:4 |
| ὁράω | aor. pass. 3 pl / aor. inf. / aor. 3 sg | `were seen` · `to see` · `saw` | `were seen, were looked at, were beheld and perceived and observed, were looked out for`; the chains of GEN 2:19 and 3:6 | 8:5, 8:7, 8:8, 8:13 |
| ἀνοίγω | aor. 3 sg | `opened` | `opened, undid, laid open and unfolded and disclosed, got into the open sea` | 8:6 |
| ἀποστέλλω | aor. 3 sg | `sent off` | `sent off, sent away and banished, despatched, went away and departed` | 8:7, 8:8 |
| ἐξέρχομαι | aor. ptcp. / aor. 3 sg and 3 pl / aor. impv. | `having gone out of` · `went out of` · `go out of` | the chain of GEN 4:16, in the form | 8:7, 8:16, 8:18, 8:19 |
| ὑποστρέφω | aor. 3 sg | `turned round about` | `turned round about and turned back, turned about and turned short round, returned, turned away and eluded` | 8:7, 8:9 |
| ξηραίνω | aor. pass. inf. / aor. pass. 3 sg | `to be parched up` · `was parched up` | `to be parched up, to be dried up, to become dry and be parched, to be laid dry`, in the form | 8:7, 8:14 |
| εὑρίσκω | aor. ptcp. fem. | `having found` | `having found, having found out, having discovered, having gotten and gained` | 8:9 |
| ἐκτείνω | aor. ptcp. | `having stretched out` | the chain of GEN 3:22, in the participle | 8:9 |
| λαμβάνω, εἰσάγω | aor. 3 sg | `took` · `led in` | the chains of GEN 2:15 and 6:19, in the aorist | 8:9, 8:20 |
| ἐπέχω | aor. ptcp. | `having held upon` | `having held upon, having held out and presented and offered, having directed towards and aimed at, having intended and purposed, having faced, having kept in and held back and checked, having stayed and stopped and waited and paused, having reached and extended over` | 8:10, 8:12 |
| ἐξαποστέλλω | aor. 3 sg | `sent quite away` | the chain of GEN 3:23 | 8:10, 8:12 |
| ἀναστρέφω | aor. 3 sg | `turned upside down` | `turned upside down, upset, turned back and brought back, rallied, turned back and returned and retired, dwelt, conducted herself, revolved, faced about` | 8:11 |
| ἔχω | impf. 3 sg | `was having` | the chain of GEN 7:22, in the imperfect | 8:11 |
| γινώσκω | aor. 3 sg | `learned to know` | the chain of GEN 4:1 | 8:11 |
| προστίθημι | aor. mid. 3 sg / fut. 1 sg | `put to` · `I will put to` | the chain of GEN 4:2, in the form | 8:12, 8:21 |
| ἐπιστρέφω | aor. inf. | `to turn about` | `to turn about, to turn round, to return, to turn towards, to correct and make to repent` | 8:12 |
| ἐκλείπω | aor. 3 sg | `left out` | `left out and omitted and passed over, forsook and deserted and abandoned, suffered an eclipse, died, left off and ceased and stopped, failed and was wanting` | 8:13 |
| ἀποκαλύπτω | aor. 3 sg | `uncovered` | `uncovered, disclosed and revealed, revealed his whole mind` | 8:13 |
| ἐξάγω | aor. impv. | `lead out` | `lead out, lead and carry out from, bring forth into the world, march out, eject, carry out and export, draw off, call forth and excite, lead on and tempt` | 8:17 |
| αὐξάνω | pres. impv. pass. 2 pl | `be made large` | `be made large, be increased and augmented, be increased in power and strengthened and exalted, be promoted to honour and glorified and magnified, grow and wax and increase, grow up` — the passive's own *to grow* last | 8:17 |
| πληθύνω | pres. impv. pass. 2 pl | `be made full` | `be made full and increased and multiplied, be in the majority and prevail` | 8:17 |
| οἰκοδομέω | aor. 3 sg | `built a house` | the chain of GEN 2:22 | 8:20 |
| ἀναφέρω | aor. 3 sg | `brought up` | `brought up, carried up, carried up the country, took with him, poured forth, heaved and uttered, upheld and took upon himself, offered and contributed, led up, carried back and recovered, brought back and reported, traced up` | 8:20 |
| ὀσφραίνομαι | aor. 3 sg | `caught scent of` | `caught scent of and smelled and scented and tracked` | 8:21 |
| διανοέομαι | aor. ptcp. | `having been minded` | the chain of GEN 6:6, in the participle | 8:21 |
| καταράομαι | aor. inf. | `to call down curses upon` | the chain of GEN 5:29, in the infinitive | 8:21 |
| ἔγκειμαι | pres. 3 sg | `lies in` | `lies in and is wrapped in, is involved in, presses upon, is urgent and insists, is devoted to` | 8:21 |
| πατάσσω | aor. inf. | `to beat` | `to beat, to knock, to strike and smite, to knock at` | 8:21 |
| καταπαύω | fut. 3 pl | `will lay to rest` | the chain of GEN 2:2, in the future | 8:22 |

### Verbs new in GEN 9

| lemma | form | headword | chain | used |
| --- | --- | --- | --- | --- |
| εὐλογέω | aor. 3 sg | `spoke well of` | the chain of GEN 2:3 | 9:1 |
| αὐξάνω, πληθύνω | pres. impv. pass. 2 pl | `be made large` · `be made full` | the chains of GEN 8:17 | 9:1, 9:7 |
| πληρόω | aor. impv. 2 pl | `make full` | `make full, fill full of, fill full, gorge and satiate, glut, fill with, man, make complete, fill, fulfil and pay in full and make up, come in full` — the entry's passives and middles left out | 9:1, 9:7 |
| κινέω | pres. mid.-pass. ptcp. n. pl., articular | `the ones being set in motion` | the chain of GEN 7:14, with the article | 9:2 |
| δίδωμι | perf. 1 sg / pres. 1 sg | `I have given` · `I give` | `I have given and it stands given, I have granted and it stands granted, I have provided and it stands provided, I have given over and delivered up and it stands so` · `I give, I am ready to give and offer, I grant, I provide, I give over and deliver up` — *to be ready to give* is the entry's present | 9:2, 9:3, 9:12 |
| ἐσθίω | fut. 2 pl | `you will eat` | the chain of GEN 2:17 | 9:4 |
| ἐκζητέω | fut. 1 sg | `I will seek out` | `I will seek out and enquire, I will demand an account of` | 9:5 |
| ἐκχέω | pres. ptcp., articular / fut. pass. 3 sg | `the one pouring out` · `will be poured out` | `the one pouring out, the one pouring out like water and squandering and wasting` · `will be poured out, will be poured out like water and squandered and wasted, will stream out and forth, will be spread out, will be forgotten, will be overjoyed, will burst out, will lie languidly` — the passive's own senses last | 9:6 |
| ποιέω | aor. 1 sg / aor. 3 sg | `I made` · `made` | the chain of GEN 6:7 · `fashioned, wrought, produced, performed, did`, the same in the third person | 9:6, 9:24 |
| λέγω | aor. 3 sg / pres. ptcp. | `said` · `saying` | the chains of GEN 2:16–18 | 9:1–26 |
| ἀνίστημι | pres. 1 sg | `I make to stand up` | `I make to stand up and raise up, I raise from sleep and wake up, I raise from the dead, I set up and build, I build up again and restore, I put up for sale, I rouse to action and stir up, I rouse to arms and raise, I make rise and break up, I make rise and emigrate and transplant, I make rise and leave sanctuary, I put up and spring` — sense A, *Causal in pres., imperf.* | 9:9 |
| ἐξέρχομαι | aor. ptcp. pl., articular | `the ones having gone out of` · `of the ones …` | the chain of GEN 4:16, in the form | 9:10, 9:18, 9:22 |
| ἵστημι | fut. 1 sg | `I will make to stand` | the chain of GEN 6:18 | 9:11 |
| ἀποθνήσκω | fut. 3 sg / aor. 3 sg | `will die off` · `died off` | the chains of GEN 2:17 and 5:5, in the form | 9:11, 9:29 |
| καταφθείρω | aor. inf. | `to destroy` | the chain of GEN 6:17 | 9:11 |
| τίθημι | pres. 1 sg | `I set` | `I set, I put, I place, I plant, I lay` | 9:13 |
| συννεφέω | pres. inf., articular with ἐν | `in the collecting clouds` | `within, inside of, and by means of the collecting clouds, the being cloudy, the wearing a clouded look` | 9:14 |
| ὁράω | fut. pass. 3 sg / fut. mid. 1 sg / aor. 3 sg and 3 pl | `will be seen` · `I will see` · `saw` | the chains of GEN 8:5, 7:1 and 3:6, in the form | 9:14, 9:16, 9:22, 9:23 |
| μιμνήσκομαι | fut. pass. 1 sg / aor. pass. inf. | `I will remind myself of` · `to remind oneself of` | the chain of GEN 8:1, in the form | 9:15, 9:16 |
| ἐξαλείφω | aor. inf. | `to plaster` | the chain of GEN 7:4, in the infinitive | 9:15 |
| διατίθεμαι | aor. mid. 1 sg | `I arranged as I liked` | `I arranged as I liked and disposed of, I disposed of my property and devised it by will, I set out for sale and disposed of, I arranged mutually, I made a covenant with, I settled with` — the entry's *B. Mid.*; its actives left out | 9:17 |
| διασπείρω | aor. pass. 3 pl | `were scattered abroad` | `were scattered abroad, were thrown about, were squandered` | 9:19 |
| ἄρχω | aor. mid. 3 sg | `began` | the chain of GEN 2:3 | 9:20 |
| φυτεύω | aor. 3 sg | `planted` | the chain of GEN 2:8 | 9:20 |
| πίνω | aor. 3 sg | `drank` | `drank, drank of, drank up` — *to be drunk*, the perfect's, left out | 9:21 |
| μεθύσκω | aor. pass. 3 sg | `was made drunk` | `was made drunk and intoxicated and inebriated, was given to drink and watered and moistened, drank freely, got drunk, was drunk` — the passive's own senses last | 9:21 |
| γυμνόω | aor. pass. 3 sg | `was stripped naked` | `was stripped naked, was stripped, was left naked and exposed, was left bare and defenceless, stripped himself naked` | 9:21 |
| ἀναγγέλλω | aor. 3 sg | `carried back tidings of` | the chain of GEN 3:11 | 9:22 |
| λαμβάνω | aor. ptcp. pl. | `having taken` | the chain of GEN 3:6 | 9:23 |
| ἐπιτίθημι | aor. mid. 3 pl | `put on themselves` | `put on themselves, put on for themselves, set themselves to and applied themselves to and employed themselves on, made an attempt upon and attacked, brought on themselves, caused to be imposed, laid commands on, gave` — the entry's *B. Mid.* | 9:23 |
| πορεύομαι | aor. pass. 3 pl | `were driven` | the chain of GEN 2:14, in the aorist | 9:23 |
| συγκαλύπτω | aor. 3 pl | `covered` | `covered, veiled completely` — the passive's *muffled up* and the middle's *to wrap oneself up* left out | 9:23 |
| ἐκνήφω | aor. 3 sg | `slept off a drunken fit` | `slept off a drunken fit, became sober again` — one sense holding two glosses, a unit as ἐμφυσάω's was at 2:7 | 9:24 |
| γινώσκω | aor. 3 sg | `learned to know` | the chain of GEN 4:1 | 9:24 |
| πλατύνω | aor. opt. 3 sg | `may widen` | `may widen, may make wide` — the middle's and passive's senses left out | 9:27 |
| κατοικέω | aor. impv. 3 sg | `let dwell in` | `let dwell in, let settle in, let colonise, let inhabit, let settle and dwell, let lie and be situate` — the first translation reads *to dwell in as a* κάτοικος; the headword stops before the Greek | 9:27 |
| γίνομαι | aor. pass. impv. 3 sg / aor. 3 pl | `let come into being` · `came into being` | `let come to be, let arise, let be brought into existence`; the chain of GEN 5:5 | 9:27, 9:29 |
| ζάω | aor. 3 sg / pres. ptcp. | `lived` · `living` | the chains of GEN 5:3 and 2:7, in the form | 9:3, 9:10, 9:12, 9:28 |

### Verbs new in GEN 14

| lemma | form | headword | chain | used |
| --- | --- | --- | --- | --- |
| γίνομαι | aor. 3 sg | `came into being` | the chain of GEN 12:10 | 14:1 |
| ποιέω | aor. 3 pl | `made` | the chain of GEN 9:24 | 14:2 |
| συμφωνέω | aor. 3 pl | `agreed in sound` | `agreed in sound, were in harmony, agreed with and held the same opinions with, made an agreement and bargained with, agreed, conspired` | 14:3 |
| δουλεύω | impf. 3 pl | `were being slaves` | `were being slaves, were serving and being subject to` | 14:4 |
| ἀφίστημι | aor2 3 pl | `stood away` | the chain of GEN 12:8 | 14:4 |
| ἔρχομαι | aor. 3 sg · aor. 3 pl | `came` | the chain of GEN 10:19, in the form | 14:5, 14:7 |
| κατακόπτω | aor. 3 pl | `cut down` | `cut down and cut in pieces and cut up, killed and slew, broke in pieces and destroyed, coined into money` | 14:5, 14:7 |
| ἀναστρέφω | aor. ptcp. · aor. inf. | `having turned upside down` · `to turn upside down` | the chain of GEN 8:11, in the form, with the lexicon's *oneself* for 8:11's *herself* | 14:7, 14:17 |
| κατοικέω | pres. ptcp., articular · pres. ptcp. · impf. 3 sg | `the ones dwelling in` · `dwelling in` · `was dwelling in` | the chain of GEN 9:27, in the form | 14:7, 14:12, 14:13 |
| ἐξέρχομαι | aor. 3 sg | `went out of` | the chain of GEN 4:16 | 14:8, 14:17 |
| παρατάσσω | aor. mid. 3 pl | `drew up one's men in battle-order` | `drew up one's men in battle-order, were drawn up along, stood prepared` — the middle, its active *to place side by side* left out | 14:8 |
| φεύγω | aor. 3 sg · aor. 3 pl | `fled` · `they fled` | `fled and took flight and ran away, had recourse and took refuge, was shy of doing and shrank from doing, shrank back, fled from and shunned and avoided, fled the consequences of, fled one's country, was banished, went into exile and was an exile, was accused and prosecuted, was put on one's trial for, was charged with`, in the form | 14:10 |
| ἐμπίπτω | aor. 3 pl | `fell in` | `fell in, fell upon and attacked, lit and chanced upon, fell in with, broke in and burst in` | 14:10 |
| καταλείπω | aor. pass. ptcp., articular | `the ones having been left behind` | the chain of GEN 7:23, in the participle | 14:10 |
| λαμβάνω | aor. 3 pl · aor. impv. · fut. 1 sg and 3 pl | `they took` · `take` · `I will take` · `they will take` | the chain of GEN 2:15, in the form | 14:11, 14:12, 14:21, 14:23, 14:24 |
| ἀπέρχομαι | aor. 3 pl | `they went away` | the chain of GEN 3:19, in the aorist | 14:11 |
| ἀποίχομαι | impf. 3 pl | `were being gone away` | `were being gone away and far from, were being gone and had departed and were being absent, were being gone and had perished, were being dead and gone` | 14:12 |
| παραγίνομαι | aor. ptcp. | `having been beside` | `having been beside / been by / near / attended upon, having been present at, having come to one's side and come to aid and stood by and seconded and supported, …, having been fully grown` — Perseus tags *near, attend upon* inside *to be beside, to be by or near*, and `MARKUP_LOST` restores the whole run, so every form heads with *beside* (Q15) | 14:13 |
| ἀνασώζω | aor. pass. ptcp., articular gen. | `of the ones having been recovered` | `of the ones having been recovered and rescued, of the ones having returned safe` — the first sense in the passive, the entry's *Pass.* after it, its middles left out | 14:13 |
| ἀπαγγέλλω | aor. 3 sg | `brought tidings` | the chain of GEN 12:18, in the third person | 14:13 |
| ἀκούω | aor. ptcp. | `having heard` | the chain of GEN 3:8, in the participle | 14:14 |
| ἀριθμέω | aor. 3 sg | `numbered` | `numbered, counted and reckoned up, counted out and paid, reckoned and counted as, was reckoned, was counted` | 14:14 |
| ἐπιπίπτω | aor. 3 sg | `fell upon` | `fell upon, attacked and assailed` | 14:15 |
| πατάσσω | aor. 3 sg | `beat` | the chain of GEN 8:21, in the aorist | 14:15 |
| διώκω | aor. 3 sg | `pursued` | `pursued, chased and hunted, was a follower of and attached oneself and sought after, followed and waited for, drove and chased away and banished, impelled and sped on her way, urged on, drove and drove on, galloped and sped and ran, prosecuted and brought an action against, accused of and prosecuted for, avenged` | 14:15 |
| ἀποστρέφω | aor. 3 sg | `turned` | the chain of GEN 3:19, in the aorist | 14:16 |
| ὑπάρχω | pres. ptcp. n. pl., as a noun | `the existing circumstances` | the chain of GEN 12:5 | 14:16 |
| ἐκφέρω | aor. 3 sg | `carried out of` | `carried out of, carried out, carried off, carried out of the sea and threw ashore, brought forth, brought forth and produced, brought about and accomplished, brought out and published, delivered, brought forward, disclosed and told and betrayed, put forth and exerted, bore the marks of, carried to a certain point, shot forth, ran away, came to fulfilment and came to an end, came to land and was cast ashore, was carried beyond bounds and carried away` — the passives last | 14:18 |
| εὐλογέω | aor. 3 sg · perf. pass. ptcp. | `spoke well of` · `having been spoken well of` | the chain of GEN 2:3 · `having been spoken well of and remaining so, having been praised and standing praised, having been honoured and standing honoured, having been blessed and standing blessed` | 14:19 |
| κτίζω | aor. 3 sg | `peopled` | `peopled, built houses and cities, colonised, founded and planted and built, planted, set up, established, created and brought into being and brought about, made, perpetrated, was founded` — *to create* is its sixth sense | 14:19, 14:22 |
| παραδίδωμι | aor. 3 sg | `gave` | `gave, handed over to another and transmitted, transmitted and imparted, delivered up and surrendered, betrayed, committed, gave up, handed down, granted and bestowed, offered and allowed` | 14:20 |
| δίδωμι | aor. 3 sg · aor. impv. | `gave` · `give` | the chain of GEN 3:6, in the form | 14:20, 14:21 |
| ἐκτείνω | fut. 1 sg | `I will stretch out` | the chain of GEN 3:22, in the future | 14:22 |
| λέγω | aor. subj. 2 sg | `you may say` | the chain of GEN 2:16, in the subjunctive | 14:23 |
| πλουτίζω | aor. 1 sg | `I made wealthy` | `I made wealthy and enriched, I gained one's wealth` — the middle's sense last | 14:23 |
| ἐσθίω | aor. 3 pl | `they ate` | the chain of GEN 3:6 | 14:24 |
| συμπορεύομαι | aor. ptcp., articular gen. | `of the ones having gone` | the chain of GEN 13:5, in the form | 14:24 |

### Verbs new in GEN 13

| lemma | form | headword | chain | used |
| --- | --- | --- | --- | --- |
| ἀναβαίνω | aor. 3 sg | `went up` | `went up, mounted, went up to, embarked` — the chain of GEN 2:6, in the aorist | 13:1 |
| πορεύομαι | aor. pass. 3 sg | `was driven` | the chain of GEN 12:4 | 13:3 |
| ἔρχομαι | aor. 3 sg · aor. inf. · aor. ptcp. | `came` · `to come` · `having come` | the chains of GEN 10:19, in the form | 13:3, 13:10, 13:18 |
| ποιέω | aor. 3 sg · fut. 1 sg | `made` · `I will make` | the chains of GEN 9:24 and 12:2 | 13:4, 13:16 |
| ἐπικαλέω | aor. mid. 3 sg | `called upon` | the chain of GEN 12:8 | 13:4 |
| συμπορεύομαι | pres. ptcp., articular dat. | `to the one going` | `to the one going, to the one journeying together, to the one coming together` — Middle Liddell's *to go or journey together*, tagged in two pieces; its *with* is the case it takes | 13:5 |
| χωρέω | impf. 3 sg | `was making room for another` | `was making room for another and giving way and drawing back and retiring and withdrawing, was putting back and retiring, was giving way to, was retiring before, was going forward and moving on, was going and coming, was going on one's journey and travelling, was coming to, was coming on and beginning, was passing and near an end, was going on and advancing, was coming to an issue and turning out, was going on well and succeeding, was spreading abroad, was spreading, was having room for, was holding and containing` — *to hold, contain*, the verse's sense, is the entry's last | 13:6 |
| κατοικέω | pres. inf. · impf. 3 pl · aor. 3 sg | `to dwell in` · `were dwelling in` · `dwelt in` | the chain of GEN 9:27, in the form | 13:6, 13:7, 13:12, 13:18 |
| δύναμαι | impf. 3 pl · pres. 3 sg | `were being able` · `is able` | `were being able and capable and strong enough, were powerful and mighty, were having influence, were daring and bearing, were passing for, were worth, were equivalent to, were signifying and meaning, were availing`, in the form | 13:6, 13:16 |
| γίνομαι | aor. 3 sg | `came into being` | the chain of GEN 12:10 | 13:7 |
| ἐπαίρω | aor. ptcp. | `having lifted up and set on` | the chain of GEN 7:17, in the participle | 13:10 |
| ὁράω | aor. 3 sg · aor. impv. (ἰδέ) · pres. 2 sg | `saw` · `see` · `you see` | the chain of GEN 3:6, in the form | 13:10, 13:14, 13:15 |
| ποτίζω | pres. pass. ptcp. | `being given to drink` | `being given to drink, being watered` — the chain of GEN 2:6 in the passive, where *to water* and *to water cattle* come to the same | 13:10 |
| καταστρέφω | aor. inf. | `to turn down` | `to turn down and trample on, to turn the soil, to upset and overturn, to subject to oneself and subdue, to turn back and bring back, to turn round and bring to an end, to come to an end and die, to twist up, to be subdued` — the passive's *to be subdued* at the end | 13:10 |
| ἐκλέγομαι | aor. mid. 3 sg | `picked out for himself` | the chain of GEN 6:2, in the singular | 13:11 |
| ἀπαίρω | aor. 3 sg | `lifted off` | the chain of GEN 12:9 | 13:11 |
| σκηνόω | aor. 3 sg | `pitched tents` | `pitched tents and encamped, dwelt in a tent, settled and took up one's abode, lived, occupied with tents` — the verb of John 1:14 | 13:12 |
| ἀναβλέπω | aor. ptcp. | `having looked up` | `having looked up, having looked, having looked up at, having cast up, having recovered one's sight` | 13:14 |
| δίδωμι | fut. 1 sg | `I will give` | the chain of GEN 12:7 | 13:15, 13:17 |
| ἐξαριθμέω | aor. inf. · fut. pass. 3 sg | `to count throughout` · `will be counted throughout` | `to count throughout and number, to count out and pay in ready money`, in the form | 13:16 |
| ἀνίστημι | aor2 ptcp. | `having stood up` | the chain of GEN 4:8, in the participle | 13:17 |
| οἰκοδομέω | aor. 3 sg | `built a house` | the chain of GEN 8:20 | 13:18 |

### Verbs new in GEN 12

| lemma | form | headword | chain | used |
| --- | --- | --- | --- | --- |
| ἐξέρχομαι | aor. impv. · aor. 3 sg and 3 pl | `go out of` · `went out of` | the chain of GEN 8:16 and 4:16 | 12:1, 12:4, 12:5 |
| δείκνυμι | aor. subj. 1 sg | `I may bring to light` | `I may bring to light and display and exhibit, I may set before one, I may show and point out, I may tell and explain and teach, I may show and prove, I may inform against, I may offer and proffer, I may cause, I may welcome and greet and pledge` | 12:1 |
| ποιέω, εὐλογέω | fut. 1 sg | `I will make` · `I will speak well of` | the chains of GEN 6:14 and 2:3, in the future | 12:2, 12:3 |
| μεγαλύνω | fut. 1 sg | `I will make great` | `I will make great and powerful, I will exalt and strengthen, I will make great by word and extol and magnify, I will aggravate` — the middle's *to boast oneself* left out | 12:2 |
| εὐλογέω, καταράομαι | pres. ptcp. pl., articular · fut. 1 sg | `the ones speaking well of` · `the ones calling down curses upon` · `I will call down curses upon` | the chains of GEN 2:3 and 5:29, in the form | 12:3 |
| λαλέω | aor. 3 sg | `talked` | `talked, chatted, prattled, babbled, said, talked of, spoke, chattered, chirped` — *to speak*, like λέγω, is the entry's New Testament sense | 12:4 |
| οἴχομαι | impf. 3 sg | `had gone` | `had gone and been gone, had escaped from, had gone hence, was departed and dead, was absent and away, was undone and ruined, was rushing and sweeping along` — the entry gives the imperfect a pluperfect sense | 12:4 |
| ὑπάρχω | pres. ptcp. n. pl., as a noun | `the existing circumstances` | `the existing circumstances and present advantages, what belongs to one and the possessions and means` — the entry's first sense for τὰ ὑπάρχοντα | 12:5 |
| κτάομαι | aor. 3 pl | `they procured for themselves` | the chain of GEN 4:1, in the third plural | 12:5 |
| κατοικέω | impf. 3 pl | `were dwelling in` | the chain of GEN 11:2, in the imperfect | 12:6 |
| ὁράω | aor. pass. 3 sg and ptcp. · aor. subj. 3 pl · aor. ptcp. pl. · aor. 3 pl | `was seen` · `to the one having been seen` · `may see` · `having seen` · `saw` | the chains of GEN 8:5, 2:19 and 3:6, in the form | 12:7, 12:12, 12:14, 12:15 |
| ἀφίστημι | aor2 3 sg | `stood away` | `stood away, stood aloof from and kept far from, lost, withdrew from, revolted from, revolted, gave up, made way and gave way, shrank from, stood aloof` — sense B, the intransitive of the second aorist, as ἀνίστημι at 4:8 | 12:8 |
| ἵστημι | aor1 3 sg | `made to stand` | the chain of GEN 6:18, in the aorist | 12:8 |
| ἐπικαλέω | aor. mid. 3 sg | `called upon` | the chain of GEN 4:26, in the aorist; Middle Liddell gives sense I *so in Mid.* | 12:8 |
| ἀπαίρω | aor. 3 sg | `lifted off` | `lifted off and carried off and took away and removed from, led away, sailed and marched away and departed, departed from, set out on` — *to depart* is the entry's intransitive use | 12:9 |
| στρατοπεδεύω | aor. 3 sg | `encamped` | `encamped and bivouacked and took up a position, was in camp, was stationed` | 12:9 |
| παροικέω | aor. inf. | `to dwell beside` | `to dwell beside, to dwell along the coast of, to live near, to dwell among, to lie near, to live in and sojourn` | 12:10 |
| ἐνισχύω | aor. 3 sg | `strengthened` | `strengthened, confirmed, prevailed in and among` — LSJ | 12:10 |
| ἐγγίζω | aor. 3 sg | `brought near` | `brought near and brought up to, approached, was imminent, approximated to, was next of kin, was on the point of` — LSJ | 12:11 |
| εἰσέρχομαι | aor. inf. · aor. 3 sg | `to go in` · `went in` | the chain of GEN 6:18, in the form | 12:11, 12:14 |
| γινώσκω | pres. 1 sg | `I learn to know` | the chain of GEN 4:9 | 12:11 |
| ἀποκτείνω | fut. 3 pl | `they will kill` | the chain of GEN 4:8, in the future | 12:12 |
| περιποιέομαι | fut. 3 pl | `they will keep for themselves` | `they will keep for themselves, they will save for themselves, they will compass and acquire and obtain, they will make gain` — the middle; the actives left out | 12:12 |
| λέγω | aor. impv. (εἰπόν) · aor. 2 sg | `say` · `you said` | the chain of GEN 2:16, in the form | 12:13, 12:19 |
| γίνομαι | aor. subj. 3 sg | `may come into being` | the chain of GEN 5:5, in the subjunctive | 12:13 |
| ζάω | fut. 3 sg | `will live` | the chain of GEN 3:22 | 12:13 |
| ἐπαινέω | aor. 3 pl | `approved` | `approved, applauded, commended, complimented publicly and panegyrized, recommended and exhorted and advised, thanked, declined` | 12:15 |
| εἰσάγω | aor. 3 pl | `led in` | the chain of GEN 8:9 | 12:15 |
| χράομαι | aor. 3 pl | `used` | `used, had and used, indulged, experienced and suffered and were subject to, came to, lived under, made use of, treated, were intimate with, were in need and yearned after, had in use and possessed` — Perseus's *consulting*, *using an oracle*, which say where the sense comes from, left out | 12:16 |
| ἐτάζω | aor. 3 sg | `examined` | `examined and tested` | 12:17 |
| καλέω | aor. ptcp. | `having called` | the chain of GEN 2:19, in the participle | 12:18 |
| ἀπαγγέλλω | aor. 2 sg | `you brought tidings` | `you brought tidings, you reported, you announced, you carried a report, you related and narrated` | 12:18 |
| λαμβάνω | aor. 1 sg · aor. ptcp. | `I took` · `having taken` | the chain of GEN 2:15, in the form | 12:19 |
| ἀποτρέχω | pres. impv. | `run off` | `run off, run away, run hard` | 12:19 |
| ἐντέλλομαι | aor. 3 sg | `enjoined` | the chain of GEN 2:16 | 12:20 |

### Verbs new in GEN 11

| lemma | form | headword | chain | used |
| --- | --- | --- | --- | --- |
| κινέω | aor. inf., articular with ἐν | `in the setting in motion` | `within, inside of, and by means of the setting in motion, the moving, the removing, the meddling with, the applying, the changing and innovating, the rousing and disturbing, the stirring up and arousing and urging on, the setting agoing and causing and calling forth` — the actives | 11:2 |
| εὑρίσκω | aor. 3 pl | `found` | the chain of GEN 6:8 | 11:2 |
| κατοικέω | aor. 3 pl and 3 sg | `dwelt in` | `dwelt in, settled in, colonised, inhabited, settled and dwelt, lay and were situate`, in the number — the chain of GEN 9:27 | 11:2, 11:31 |
| πλινθεύω | aor. subj. 1 pl | `let us make into bricks` | `let us make into bricks, let us make bricks, let us build of brick, let us make in the form of a plinth or brick` | 11:3 |
| ὀπτάω | aor. subj. 1 pl | `let us roast` | `let us roast and broil, let us bake, let us bake and burn, let us bake and harden` | 11:3 |
| οἰκοδομέω | aor. subj. 1 pl · aor. 3 pl · pres. ptcp. pl. | `let us build a house` · `built a house` · `building a house` | the chain of GEN 2:22, in the form | 11:4, 11:5, 11:8 |
| ποιέω | aor. subj. 1 pl · aor. and pres. inf. | `let us make` · `to make` | `let us make, let us do, let us produce, let us create`; the chain of GEN 2:3 | 11:4, 11:6 |
| διασπείρω | aor. pass. inf. · aor. 3 sg | `to be scattered abroad` · `scattered abroad` | the chain of GEN 9:19, in the form | 11:4, 11:8, 11:9 |
| καταβαίνω | aor. 3 sg · aor. ptcp. pl. | `stepped down` · `having stepped down` | `stepped down, went and came down, went down from, dismounted, came down stairs, went down from the inland parts to the sea, came to land and got safe ashore, went down into the arena, came down from the tribune, came to, ended`, in the form | 11:5, 11:7 |
| ἐκλείπω | fut. 3 sg | `will leave out` | the chain of GEN 8:13, in the future | 11:6 |
| ἐπιτίθημι | aor. mid. subj. 3 pl | `they may put on themselves` | the chain of GEN 9:23, in the subjunctive | 11:6 |
| συγχέω | aor. subj. 1 pl · aor. 3 sg | `let us pour together` · `poured together` | `let us pour together and commingle and confound, let us make ruinous and destroy and obliterate and demolish, let us confound and trouble, let us confound and make of none effect and frustrate`, in the form — the passive's *to be in confusion* left out | 11:7, 11:9 |
| ἀκούω | aor. subj. 3 pl | `they may hear` | `they may hear, they may have hearing of, they may hear tell of, they may know by hearsay, they may hearken and give ear, they may listen to and obey` | 11:7 |
| παύω | aor. mid. 3 pl | `took their rest` | `took their rest and rested and ceased and had done, left off from and rested and ceased from, were at rest, left off doing` — the entry's *Pass. and Mid.*; the causal actives left out | 11:8 |
| καλέω | aor. pass. 3 sg | `was called` | `was called, was summoned, was invited` — the chain of GEN 2:23, in the aorist | 11:9 |
| γίνομαι | aor. 3 sg, no subject · aor. 3 sg and 3 pl · aor. pass. 3 sg | `came into being` | the chains of JHN 1:6 and GEN 5:5, in the form | 11:2, 11:3, 11:28, 11:32 |
| ζάω, γεννάω, ἀποθνήσκω | the frame of GEN 5 | `lived` · `begot` · `to beget` · `died off` | the chains of GEN 5 | 11:11–32 |
| λαμβάνω | aor. 3 pl and 3 sg | `took` | the chain of GEN 2:15 | 11:29, 11:31 |
| ἐξάγω | aor. 3 sg | `led out` | the chain of GEN 8:17, in the aorist | 11:31 |
| πορεύομαι | aor. pass. inf. | `to be driven` | the chain of GEN 2:14, in the infinitive | 11:31 |
| ἔρχομαι | aor. 3 sg | `came` | `came, went, went back and returned, was going to and intended, came within a little of and was near` — the chain of GEN 10:19 | 11:31 |

### Verbs new in GEN 10

| lemma | form | headword | chain | used |
| --- | --- | --- | --- | --- |
| γίνομαι | aor. pass. 3 pl · aor. mid. 3 sg and 3 pl · aor. pass. 3 sg, no subject | `came into being` | the chains of GEN 5:5, 4:2 and JHN 1:6, in the form | 10:1, 10:10, 10:19, 10:21, 10:25, 10:30 |
| ἀφορίζω | aor. pass. 3 pl | `were marked off by boundaries` | `were marked off by boundaries, were distinguished and determined and defined, were banished, were set apart and separated, were cast out and excommunicated, were set apart, were appointed and ordained` — the chain of GEN 2:10, in the aorist | 10:5 |
| γεννάω | aor. 3 sg | `begot` | the chain of GEN 4:18 | 10:8–26 |
| ἄρχω | aor. mid. 3 sg | `began` | the chain of GEN 2:3 | 10:8 |
| λέγω | fut. 3 pl | `they will say` | `they will say, they will speak, they will declare, they will call by name, they will tell` | 10:9 |
| ἐξέρχομαι | aor. 3 sg | `went out of` | the chain of GEN 4:16 | 10:11, 10:14 |
| οἰκοδομέω | aor. 3 sg | `built a house` | the chain of GEN 2:22 | 10:11 |
| διασπείρω | aor. pass. 3 pl | `were scattered abroad` | the chain of GEN 9:19 | 10:18, 10:32 |
| ἔρχομαι | aor. inf. | `to come` | `to come, to go, to go back and return, to be going to and intend, to come within a little of and be near` | 10:19, 10:30 |
| διαμερίζω | aor. pass. 3 sg | `was distributed` | `was distributed, was divided` — the middle's *to part among themselves* left out | 10:25 |

A third-person imperative takes *let* and no pronoun (κατοικησάτω *let dwell in*, γενηθήτω *let
come into being*), as a finite verb takes none; an optative takes *may* (πλατύναι *may widen*).

---

## Nouns

### ἀρχή (with ἐν)

- **headword:** `in beginning` — ἐν *in*; ἀρχή, Middle Liddell's first sense *a beginning*;
  ἀρχῇ is anarthrous, so no article. (Middle Liddell also lists *in the beginning, at first*
  among its later senses, for a phrase this extraction does not show; it is not used.)
- **chain:** `within, inside of, and by means of the first moment, the origin-point, the source, the first principle from which a thing proceeds, and simultaneously the headship, the rule, and the governing precedence over all that follows`
- **short:** `within, inside of, and by means of the first moment, the origin-point, the source, the first principle`
- **used:** GEN 1:1, JHN 1:1 (full, identical — the quotation), JHN 1:2 (short)

Both halves — temporal origin and ruling precedence — are obligatory in the full form. The
short form drops the precedence half only because JHN 1:2 restates JHN 1:1.

### λόγος

- **headword:** `the word` — Middle Liddell, first sense *the word*; articular. Lowercase: no
  title capital.
- **chain:** `the word, that by which the inward thought is expressed, the inward thought itself, language and talk, a word and a saying and a statement, an oracle, a saying and a maxim and a proverb, speech and discourse and conversation, report and repute, a tale and a story, a speech and an oration, that which is stated and a proposition and a principle, reason, account and consideration and esteem and regard, due relation and proportion and analogy`
- **short:** `the utterance, the account`
- **used:** JHN 1:1

Lowercase throughout; the notes say why (JHN 1:1, *Capitals*). *Logos* appears in neither
panel.

### οὐρανός

- **headword:** `the heaven` — Middle Liddell, first sense *heaven*; articular.
- **chain:** `the heaven, the vault, the firmament and the sky`
- **used:** GEN 1:1

  Senses I, I.1 and I.1's second translation. The entry's other translations are quoted
  idioms — πύλαι οὐρανοῦ *Heavengate*, πρὸς οὐρανὸν βιβάζειν *to exalt to heaven* with its
  Latin *evehere ad Deos* — and Uranus, the god. They are in `NOT_SENSES`. The chain read
  `the vaulted arch, the sky-expanse, the region above and over` until 2026-09-18; none of
  those three phrases is in the entry, and the 23 genitives already read the derived way.

Singular in the LXX against Hebrew dual/plural *šāmayim*. Flag `divergence`.

### γῆ

- **headword:** `the earth` — Middle Liddell, first sense *earth*; articular.
- **chain:** `the earth, the land, the ground`
- **used:** GEN 1:1

  Senses I (*earth*, *land*) and III (*ground*). κατὰ γῆν *on land, by land* and γῆν πρὸ
  γῆς *from land to land* are idioms the entry quotes, not senses, and are in
  `NOT_SENSES`. Anarthrous γῆ reads `earth, land, ground`: the articles follow the Greek,
  not the lexicon's phrasing of its own glosses.

  The chain read `the land, the dry ground, the terrestrial realm` — and in GEN 1:1 a
  longer `…the soil, the territory, the terrestrial realm as the counterpart-below` —
  until 2026-09-18. *Dry*, *terrestrial realm*, *soil*, *territory* and *counterpart-below*
  are none of them in the entry, and the headword `the earth` did not stand at the head of
  its own chain. 178 units across every chapter carried it.

### σκότος

- **headword:** `darkness` — Middle Liddell, first sense *darkness, gloom*; anarthrous.
- **chain:** `darkness, gloom, the darkness of death`
- **used:** GEN 1:2

### ἄβυσσος

- **headword:** `the great deep` — used as a noun (τῆς ἀβύσσου), so the first noun sense:
  Middle Liddell's third group, *the great deep, the abyss, bottomless pit*. The first two
  are the adjective (*with no bottom, bottomless*). Articular.
- **chain:** `the great deep, the abyss, the bottomless pit, the bottomless and unfathomed, the unfathomable and enormous`
- **used:** GEN 1:2

### πνεῦμα

- **headword:** `blowing` — Middle Liddell, sense I, whose first translation is *a blowing*
  (it goes on: *a wind, blast*); anarthrous, so no article.
- **chain:** `blowing, a wind and blast, a breeze, influence, breathed air and breath, the ghost, that which is breathed forth and odour and scent, spirit, inspiration`
- **used:** GEN 1:2 (followed by θεοῦ as its own unit)

Lowercase *spirit*; the notes say why (GEN 1:2, *Capitals*). In the full lexicon *spirit*
comes after *wind* and *breath*; the two-meaning quick gloss that puts it first is a summary,
not the lexicon's order. The one place where Greek and Hebrew line up exactly — πνεῦμα and
*rûaḥ* share the same triple range. Say so in the notes rather than choosing.

### ὕδωρ — plain text

`the water`. No chain — the word is not doing lexical work here. Singular against Hebrew
plural *mayim*; flag `divergence`. **The Hebrew's *face of* is absent from the LXX at both
points in this verse and must not appear in either reading text.**

### ἄνθρωπος

- **headword:** `man` — Middle Liddell, sense I *man* (the etymology *manfaced* stands before
  the senses); anarthrous, so no article.
- **chain:** `a man, a human being`
- **used:** JHN 1:6

### οὗτος

- **headword:** `this` — Middle Liddell, first sense.
- **chain:** `this same one, this very one and no other`
- **used:** JHN 1:2

`and no other` carries the near demonstrative's work of pinning the referent.

### Adjectives at GEN 1:2

- **ἀόρατος** — headword `unseen` (Middle Liddell, first sense *unseen, not to be seen,
  invisible*); chain `unseen and not to be seen and invisible, without sight` (was `unseeable, un-viewable, not presenting itself to the eye,
  imperceptible to sight`
- **ἀκατασκεύαστος** — headword `not properly prepared` (no Middle Liddell entry; LSJ's first
  sense, which LSJ follows with *unwrought, unformed*, citing this verse); chain `not properly prepared, unwrought and unformed, chaos, unpolished and unartificial` (was `un-built-out, unfurnished, unequipped, unprovisioned, not fitted out with its
  appointments, lacking the constructed arrangement that a full outfitting would supply`

Both stand under one `divergence` flag against Hebrew *tōhû wā-bōhû*. *Formless* is too
abstract for ἀκατασκεύαστος and is not used.

### κόσμος

- **headword:** `the order` — Middle Liddell, first sense *order*; articular.
- **chain:** `the order, the good order and decency, the form and fashion, the government, the ornament and adornment`
- **used:** GEN 2:1

*World* is a late sense and is not the lexicon's first. Flag `divergence` against Hebrew
*ṣābāʾ*, *host*: the Greek keeps the ranked arrangement and loses the army.

### ἡμέρα

- **headword:** `the day` — Middle Liddell, first sense *day*; articular where the Greek has
  the article (GEN 2:2, 2:3), anarthrous in ᾗ ἡμέρᾳ (GEN 2:4), which takes `day`.
- **chain:** `the day, the day-break, the time`
- **with ἐν:** `in the day` / `within, inside of, and by means of the day, the day-break, the time`
- **used:** GEN 2:2, GEN 2:3, GEN 2:4

### ἔργον

- **headword:** `the works` — Middle Liddell, first sense *work*; articular, plural.
- **chain (full):** `the works, the business, the deeds, the action, the works of industry and the tilled lands`
- **short:** `the works, the business, the deeds`
- **used:** GEN 2:2 (full, then short), GEN 2:3 (short)

### βίβλος

- **headword:** `the inner bark of the papyrus` — Middle Liddell, first sense; articular.
  *A book* is the entry's third sense and is not taken.
- **chain:** `the inner bark of the papyrus, the bark, the book`
- **used:** GEN 2:4

The plainest case so far of the rule against the expected word. The material stands where
the reader expects the object; the note carries the explanation.

### γένεσις

- **headword:** `of origin` — Middle Liddell, first sense *an origin, source, productive
  cause*; genitive, anarthrous.
- **chain:** `of origin, of source, of productive cause, of beginning, of manner of birth, of race and descent, of production and generation, of creation and the created things`
- **used:** GEN 2:4

The word the book is named from. It holds the origin of a thing and the account of that
origin together, where English splits *genesis* from *generations*.

### πᾶς

- **headword:** `all` — Middle Liddell, first sense *all, the whole*.
- **chain:** `all, the whole, every, every single`
- **used:** GEN 2:1, GEN 2:2, GEN 2:3

The whole taken together, not merely each part.

### οὐρανός and γῆ — anarthrous genitive

GEN 2:4 has them without the article, so no *the*:

- `of heaven` / `of heaven, of the vault, of the firmament and the sky`
- `of earth` / `of earth, of land, of the ground`

The articular forms are unchanged above.

### χλωρός

- **headword:** `greenish-yellow` — Middle Liddell, first sense; a colour, anarthrous.
- **chain:** `greenish-yellow, pale-green and light-green and green and grassy, yellow, pale and bleached, fresh and living`
- **used:** GEN 2:5

The colour comes first and the plant is named from it, which is the lexicon's order.

### χόρτος

- **headword:** `an inclosed place` — Middle Liddell, first sense *an inclosed place, a
  feeding-place*; anarthrous, accusative.
- **chain:** `an inclosed place and a feeding-place, any feeding-ground, food and fodder and provender, grass, hay`
- **used:** GEN 2:5

*Grass* is the entry's fourth sense. The enclosure stands where the reader expects the crop.

### ἀγρός — genitive

- **headword:** `of field` — Middle Liddell, first sense *fields, lands*; genitive singular,
  anarthrous, so the singular against the lexicon's plural citation form.
- **chain:** `of field, of lands, of a farm, of the country`
- **used:** GEN 2:5, twice

### πηγή

- **headword:** `running waters` — Middle Liddell, first sense *running waters, streams*,
  which the entry marks *mostly in pl.* while the text has the singular. The lexicon's
  first translation stands; the number is recorded in the verse's notes.
- **chain:** `running waters, streams, a fount, a source, an origin`
- **used:** GEN 2:6

`NOT_SENSES` drops *(the spring* and *well-head)* — fragments of the phrase by which the
entry distinguishes πηγή *from* κρουνός, and so glosses of a different word.

### πρόσωπον

- **headword:** `the face` — Middle Liddell, first sense *the face, visage, countenance*;
  articular. Genitive articular τῆς γῆς beside it takes `of the earth`.
- **chain:** `the face and visage and countenance, the look, the mask, the outward appearance`
- **used:** GEN 2:6, GEN 2:7

The LXX renders Hebrew *pānîm* here, having dropped it twice in 1:2. That difference is the
reason `face of the waters` is a banned phrase and `the face of the earth` is not.

### χοῦς

- **headword:** `earth thrown down` — the second of the two entries under this spelling (see
  *Homographs* above); accusative, anarthrous.
- **chain:** `earth thrown down, heaped up, dust`
- **used:** GEN 2:7

### πνοή

- **headword:** `a blowing` — Middle Liddell, first sense *a blowing, blast, breeze*;
  accusative, anarthrous.
- **chain:** `a blowing, a blast, a breeze, a breathing hard, breath, flame`
- **used:** GEN 2:7

The same opening gloss the lexicon gives πνεῦμα at 1:2. Two different words for moving air,
and *spirit* is first in neither.

### ζωή — genitive

- **headword:** `of a living` — Middle Liddell, first sense *a living*; genitive, anarthrous.
- **chain:** `of a living, of the means of life and substance, of life and existence, of a way of life`
- **used:** GEN 2:7

*A living* in the sense of a livelihood stands before *life*, and the chain keeps the order.

### ψυχή

- **headword:** `breath` — Middle Liddell, first sense; accusative, anarthrous.
- **chain:** `breath, the life, the spirit, life and death, the ghost, the departed soul`
- **used:** GEN 2:7

*Soul* is not the first sense and is not the headword. With πνοήν in the same verse the
phrase runs breath into breath.

### ἄνθρωπος — articular

- **headword:** `the man` — the same entry as the anarthrous `man` (JHN 1:6, GEN 2:5), with
  the article the Greek prints.
- **chain:** `the man, the human being, mankind`
- **used:** GEN 2:7, twice

### κύριος

- **headword:** `lord` — Middle Liddell files two words under κύριος: the adjective, *having
  power or authority over*, and the noun, *a lord, master*. `ENTRY` sends the noun to the second
  entry and the adjective to the first, by the part of speech the morphology gives (Q16).
  Anarthrous, so *lord* without the lexicon's *a*.
- **chain:** `lord / master, the head, master, the Lord, Jehovah` — the noun's entry whole: *the
  head* (of a family), *master* (of a house), and ὁ Κύριος, *the Lord, = Hebr. Jehovah*, the LXX's
  rendering of the divine name. The vocative adds *sir*, "later, κύριε was a form of respectful
  address" (`lord / master, the head, master, sir, the Lord, Jehovah`); the plural leaves out the
  singular ὁ Κύριος's two (`lords / masters, the heads, masters`, `sirs` in the vocative); κυρία's
  *mistress, lady of the house* is the feminine's. Articular, every item takes the article, as τὸ
  σπέρμα is *the that which is sown*, save where the gloss has it already: `the lord / master, the
  head, the master, the Lord, the Jehovah`.
- **the adjective:** EXO 21:8, οὐ κύριός ἐστιν πωλεῖν, the construction the first entry names,
  κύριός εἰμι c. inf., *I have authority to do, am entitled to do*: `having power / authority over /
  lord / master of, having authority, entitled, having authority / authoritative / supreme, …`, its
  comparatives and its uses as a noun left out by `FORM_SENSES`.
- **used:** GEN 2:8

Renders the Hebrew divine name, which the Greek replaces with a title rather than
transliterating. Say so in the notes wherever it first appears in a chapter.

### παράδεισος

- **headword:** `a park` — Middle Liddell, first sense *a park*; anarthrous at GEN 2:8,
  articular after (`the park`).
- **chain:** `a park, the garden of Eden and paradise`
- **used:** GEN 2:8, 2:9, 2:10

A Persian loanword for a walled enclosure. The lexicon's second sense names this very
garden, which is where the English word comes from.

### ἀνατολή

- **headword:** `risings` — Middle Liddell, first sense *a rising, rise*; accusative plural,
  anarthrous.
- **chain:** `risings and rises, the quarter of sunrise and east`
- **used:** GEN 2:8

### ξύλον

- **headword:** `wood` — Middle Liddell, first sense *wood*; `the wood` where articular.
- **chain:** `wood, firewood, timber, a piece of wood and post, a stick`
- **short:** `the wood, the timber, the piece of wood`
- **used:** GEN 2:9, three times

Cut material, not the living δένδρον. The same word carries the cross in Acts and Galatians.

### ὅρασις, βρῶσις

- ὅρασις — **headword** `seeing`; **chain** `seeing and the act of sight, a vision`. GEN 2:9.
- βρῶσις — **headword** `meat`; **chain** `meat, eating, corrosion and rust`. GEN 2:9.
  *Meat* stands first and *eating* second; the third sense is the rust of Matthew 6:19.

### ὡραῖος

- **headword:** `produced at the right season` — Middle Liddell, first sense.
- **chain:** `produced at the right season, seasonable, timely, of the season, gathered in due season`
- **used:** GEN 2:9

### μέσος

- **headword:** `middle` — Middle Liddell, first sense *middle, in the middle*.
- **chain:** `middle, in the middle, the centre, mid, between two`
- **used:** GEN 2:9

### καλός and πονηρός

- καλός, as an adjective — **headword** `beautiful`; **chain** `beautiful, beauteous, fair,
  good`. GEN 2:12, 2:18, 3:6, 6:2, 12:14, 15:15, 18:7.
- καλός, used as a noun — **headword** `beauty` (`of beauty` in the genitive, `to beauty` in
  the dative); **chain** `beauty, moral beauty and virtue`, the entry's first noun sense,
  τὸ καλόν, and then τὸ καλόν again in the moral sense. τὰ καλά, *the decencies, proprieties,
  elegancies*, is the plural's own and is left out of a singular. GEN 2:9, 2:17, 3:5, 3:22, 24:50.
- πονηρός — **headword** `of toilsome`; **chain** `of toilsome, of painful, of grievous, of
  good-for-nothing, of bad and worthless, of wicked`. GEN 2:9.

πονηρός begins as the word for hard labour and arrives at wickedness only later in the
entry. The pair καλοῦ καὶ πονηροῦ is therefore not *good and evil* in the lexicon's order.
It is not the pair it looks like in another way either: καλοῦ is a noun in the lexicon's
own entry and πονηροῦ is not, since Middle Liddell gives πονηρός's neuter no noun sense —
ὁ πονηρός, *the evil one*, is the masculine's. So one of the two takes noun senses and the
other keeps the adjective's, and the asymmetry is the lexicon's.

### γνωστός

- **headword:** `known` — Middle Liddell, first sense *known, to be known*.
- **chain:** `known and to be known`
- **used:** GEN 2:9 — a word the Hebrew of this phrase does not have; flag `divergence`.

### ποταμός

- **headword:** `a river` — Middle Liddell, first sense *a river, stream*; `the river` where
  articular, `to the river` in the dative.
- **chain:** `a river and stream, a river-god`
- **used:** GEN 2:10, 2:13, 2:14

### ἀρχή — plural, of rivers

- **headword:** `beginnings` — the same entry as ἐν ἀρχῇ; accusative plural, anarthrous.
- **chain:** `beginnings, origins, first causes, headships and rules and governing precedences`
- **used:** GEN 2:10

The word that opens Genesis and John, here of the heads of four rivers. The full range is
kept precisely so the connection stays on the page.

### ὄνομα, εἷς

- ὄνομα — **headword** `a name`; **chain** `a name, fame, a mere name, a phrase and
  expression`. GEN 2:11, 2:13.
- εἷς — **headword** `to the one` (dative); **chain** `to the one, to a single one, to one
  alone`. GEN 2:11. Perseus keys the numeral `ei(/s`, with an acute.

### χρυσίον, ἄνθραξ, λίθος, πράσινος

- χρυσίον — **headword** `the piece of gold`; **chain** `the piece of gold, the gold, the gold
  coin and money`, the article on every item as on every noun's (EXO 36). The diminutive names a nugget before the metal. GEN 2:11, 2:12.
- ἄνθραξ — **headword** `the charcoal`; **chain** `the charcoal and coal`. One sense only;
  the gem is named from the burning coal, as Latin *carbunculus* is. GEN 2:12.
- λίθος — **headword** `the stone`; **chain** `the stone, the precious stone, the marble`.
  GEN 2:12.
- πράσινος — **headword** `the leek-green`; **chain** `the leek-green and light green`.
  **No Middle Liddell entry**; LSJ gives *leek-green, light green* and cites this verse for
  the stone (λίθος π. = πρασῖτις). Its *green faction* sense is the Circus and is not in
  play. GEN 2:12.

### ἐκεῖνος

- **headword:** `of that` — Middle Liddell, first sense *the person there, that person*;
  genitive, agreeing with γῆς.
- **chain:** `of that, of the one there, of the more remote`
- **used:** GEN 2:12

### θάνατος

- **headword:** `with death` — Middle Liddell, first sense *death*; dative, anarthrous.
- **chain:** `with death, with the death threatened, with the sentence of death`
- **used:** GEN 2:17 — θανάτῳ ἀποθανεῖσθε, the Hebrew infinitive absolute imitated

### μόνος

- **headword:** `alone` — Middle Liddell, first sense *alone, left alone, forsaken solitary*.
- **chain:** `alone, left alone and forsaken and solitary, only`
- **used:** GEN 2:18

### βοηθός

- **headword:** `an assistant` — the entry opens as an adjective, *assisting, auxiliary*;
  the first **noun** sense is *an assistant*, and the rule takes it.
- **chain:** `an assistant, one assisting and auxiliary`
- **used:** GEN 2:18, GEN 2:20

The Septuagint uses the word of God himself as Israel's helper, so nothing in it implies
lesser rank. Say so in the notes rather than choosing a word that decides it.

### θηρίον, κτῆνος, πετεινόν

- θηρίον — **headword** `the wild animals`; **chain** `the wild animals, the beasts, the
  savage beasts, the game`. GEN 2:19, 2:20.
- κτῆνος — **headword** `to the flocks and herds` (dative plural); **chain** `to the flocks
  and herds, to the single beast, to the ox, to the sheep, to the beast for riding`. From
  κτάομαι, to acquire: the domestic animals are named by their belonging. GEN 2:20.
- πετεινόν — **headword** `the winged fowl`; **chain** `the winged fowl, the birds, the able
  to fly and full fledged`. The neuter noun is filed under the adjective πετεινός, whose
  first **noun** sense is *winged fowl*. GEN 2:19, 2:20.

### ὅμοιος

- **headword:** `like` — Middle Liddell, first sense *like, resembling*.
- **chain:** `like, resembling, the same, all one, shared alike by both`
- **used:** GEN 2:20

ὅμοιος αὐτῷ here against κατʼ αὐτόν at 2:18 — two Greek phrases for one Hebrew *kĕnegdô*,
and both are kept.

### ἔκστασις

- **headword:** `any displacement` — Middle Liddell gives one sense, *any displacement:
  entrancement, astonishment*, where the colon marks the application, as with ἐμφυσάω;
  *a trance* follows. Accusative, anarthrous.
- **chain:** `any displacement, entrancement, astonishment, a trance`
- **used:** GEN 2:21

A standing outside oneself, not sleep. The word of Acts 10:10 and Mark 16:8.

### πλευρά

- **headword:** `of ribs` (genitive plural, GEN 2:21) / `the rib` (accusative articular,
  GEN 2:22) — Middle Liddell, first sense *a rib*.
- **chain:** `of ribs, of the ribs and the side, of one side, of the page`
- **used:** GEN 2:21, GEN 2:22

*A rib* and *the side* are one word; Greek does not choose between them and neither does
the chain.

### σάρξ

- **headword:** `flesh` — Middle Liddell, first sense; anarthrous.
- **chain:** `flesh, the flesh, muscles, the body, man's nature generally`
- **used:** GEN 2:21, GEN 2:23, GEN 2:24

### ὀστέον

- **headword:** `bone` (GEN 2:23, the Attic contraction ὀστοῦν) / `of the bones` (genitive
  plural) — **Middle Liddell has the entry but tags no usable translation in it**: only
  *the*, sliced out of "the bleached bones of the dead". The sense is LSJ's, *bone*, and
  `LSJ` in `build/words.py` overrides the entry for that reason.
- **chain:** `bone, the bones of the dead`
- **used:** GEN 2:23

The first case of an entry that exists and glosses nothing usable — distinct from ἁγιάζω,
which exists and glosses nothing at all.

### γυνή and ἀνήρ

- γυνή — **headword** `a woman` (anarthrous) / `the woman` (articular); **chain** `a woman,
  a mistress and lady, a wife and spouse, a mortal woman`. GEN 2:22, 2:23, 2:24, 2:25.
- ἀνήρ — **headword** `of the man`; **chain** `of the man, of the man in the prime of life`.
  `NOT_SENSES` drops the Latin *homo* and *vir gregis*, and the scrap *a woman* from "opp.
  to a woman". GEN 2:23.

Two unrelated Greek words where the Hebrew has a pun — *ʾiššâ* from *ʾîš*. The reason clause
of 2:23 loses its hinge in Greek, and the note says so. ἀνήρ is also the first word in the
chapter that means the male as against ἄνθρωπος, the human being.

### πατήρ, μήτηρ

- πατήρ — **headword** `the father`; **chain** `the father, the grandfather`. GEN 2:24.
- μήτηρ — **headword** `the mother`; **chain** `the mother, the dam, the source`. GEN 2:24.

### γυμνός

- **headword:** `naked` — Middle Liddell, first sense *naked, unclad*.
- **chain:** `naked and unclad, unarmed, uncovered, stripped of`
- **used:** GEN 2:25

*Unarmed* is the entry's second sense, and chapter 3 turns on it.

### νῦν, εἷς, δύο

- νῦν — **headword** `now`; **chain** `now, even now, just now`. GEN 2:23.
- εἷς — **headword** `one`; **chain** `one, a single one and one alone`. GEN 2:21 (μίαν, of the
  rib), GEN 2:24 (μίαν, of the flesh).
- δύο — plain text `the two`. One sense, so no range to open. GEN 2:24, 2:25.

`οἱ δύο` at 2:24 is not in the Hebrew at all, and every New Testament quotation of the verse
quotes the Greek with it. Flag `divergence` there.

### ἀγρός and οὐρανός — articular genitive

τοῦ ἀγροῦ and τοῦ οὐρανοῦ take the article in English, as the rule requires:

- `of the field` / `of the field, of the lands, of the farm, of the country`
- `of the heaven` / `of the heaven, of the vault, of the firmament and the sky`
- **used:** GEN 2:19, GEN 2:20, GEN 3:18

GEN 2:19 and 2:20 first carried the anarthrous chains of 2:4–5, *of field* and *of heaven*,
though both have the article; they were corrected when GEN 3:18 reused them.

### Nouns and adjectives new in GEN 3

| lemma | headword | chain | used |
| --- | --- | --- | --- |
| ὄφις | `the serpent` | `the serpent and snake` | 3:1, 3:4, 3:13 |
| φρόνιμος (superl.) | `most in one's right mind` | `most in one's right mind, most in one's senses, most staid and unmoved and discreet, wisest, most sensible, most prudent` | 3:1 |
| θηρίον (gen. pl.) | `of the wild animals` | `of the wild animals, of the beasts, of the savage beasts, of the game` | 3:1, 3:14 |
| κτῆνος (gen. pl.) | `of the flocks and herds` | `of the flocks and herds, of the single beasts, of the beasts for riding` | 3:14 |
| καρπός | `fruit` · `of the fruit` | `fruit, produce, returns, profits, result` | 3:2, 3:3, 3:6 |
| ὀφθαλμός (pl.) | `the eyes` · `to the eyes` | `the eyes, the dearest and best, the comfort, the buds` | 3:5, 3:6, 3:7 |
| ἀρεστός | `acceptable` | `acceptable and pleasing` | 3:6 |
| φύλλον (pl.) | `leaves` | `leaves, foliage, petals, herbs` | 3:7 |
| συκῆ | `of fig-tree` | `of fig-tree, of fig` | 3:7 |
| περίζωμα (pl.) | `girdles round the loins` | `girdles round the loins and aprons` | 3:7 |
| φωνή | `the sound` · `of the sound` | `the sound and tone, the sound of the voice, the cry, the faculty of speech and discourse, the language, the saying` | 3:8, 3:10, 3:17 |
| πρόσωπον (anarthrous) | `face` · `of the face` | `face, visage, countenance, look, outward appearance` | 3:8, 3:19 |
| στῆθος | `the breast` | `the breast, the breast as the seat of feeling, the heart` | 3:14 |
| κοιλία | `the large cavity of the body` | `the large cavity of the body, the belly, the intestines, the bowels` | 3:14 |
| γῆ (anarthrous acc., nom.) | `earth` | `earth, land, the ground` | 3:14, 3:19 |
| ἡμέρα (pl.) | `the days` | `the days, the day-breaks, the times` | 3:14, 3:17 |
| ἔχθρα | `hatred` | `hatred and enmity, hatred for and enmity to, feud, hostility` | 3:15 |
| σπέρμα | `of that which is sown` | `of that which is sown, of the seed, of the germ and origin and element, of the offspring and issue, of the race and descent` | 3:15 |
| κεφαλή | `head` | `head, the life, the top, the brim, the coping, the source, the crown and completion` | 3:15 |
| πτέρνα | `heel` | `heel, the under part of the heel, the ham` | 3:15 |
| λύπη (pl.) | `the pains of body` · `in pains of body` | `the pains of body, the distresses and sad plights, the pains of mind and griefs` | 3:16, 3:17 |
| στεναγμός | `the sighing` | `the sighing and groaning and moaning` | 3:16 |
| τέκνον (pl.) | `things borne` | `things borne, the born, children, the young` | 3:16 |
| ἀνήρ (acc., dat.) | `the man` · `to the man` | `the man, the man in the prime of life` | 3:6, 3:16 |
| ἀποστροφή | `the turning back` | `the turning back, the turning away from and escape from, the resort and resource` | 3:16 |
| ἔργον, with ἐν | `in the works` | `within, inside of, and by means of the works, the business, the deeds` | 3:17 |
| ἄκανθα (pl.) | `thorns` | `thorns and prickles, prickly plants and thistles, thistledown, spines` | 3:18 |
| τρίβολος (pl.) | `caltrops` | `caltrops, three-spiked implements, prickly plants and burrs and thistles, threshing-boards` | 3:18 |
| χόρτος (articular) | `the inclosed place` | `the inclosed place and feeding-place, the feeding-ground, the food and fodder and provender, the grass, the hay` | 3:18 |
| ἱδρώς, with ἐν | `in sweat` | `within, inside of, and by means of sweat, exudation, gum` | 3:19 |
| ἄρτος | `the cake` | `the cake, the loaf of wheat-bread, the bread` | 3:19 |
| ὄνομα (articular) | `the name` | `the name, the fame, the mere name, the phrase and expression` | 3:20 |
| μήτηρ (anarthrous) | `mother` | `mother, dam, source` | 3:20 |
| χιτών (pl.) | `garments worn next the skin` | `garments worn next the skin and frocks, coats of mail, coverings, skins` | 3:21 |
| δερμάτινος | `of skin` | `of skin and leathern` | 3:21 |
| χείρ | `the hand` | `the hand, the hand and arm, the arm` | 3:22 |
| αἰών | `the period of existence` | `the period of existence, the life-time and life, the age and generation, the long space of time, the era and epoch, the world` | 3:22 |
| τρυφή | `of the softness` | `of the softness and delicacy and daintiness, of the luxuries, of the luxuriousness and wantonness` | 3:23, 3:24 |
| φλόγινος | `the flaming` | `the flaming and fiery, the flame-coloured` — **no Middle Liddell entry**; LSJ, citing this verse | 3:24 |
| ῥομφαία | `large sword` | `large sword and scymitar` — the article stands on φλογίνην before it | 3:24 |
| ὁδός | `the way` | `the way, the path, the track, the road, the highway, the course, the journey, the manner and method` | 3:24 |

### Nouns and adjectives new in GEN 4

| lemma | headword | chain | used |
| --- | --- | --- | --- |
| ἀδελφός | `the son of the same mother` · `of …` · `to …` | `the son of the same mother, the brother, the near kinsman` | 4:2, 4:8–11, 4:21 |
| ποιμήν | `herdsman` | `herdsman, shepherd, captain and chief, master and lord, pastor and teacher` — LSJ | 4:2 |
| πρόβατον (gen. pl.) | `of anything that walks forward` | `of anything that walks forward, of cattle, of flocks and herds, of horses, of small cattle, of sheep` | 4:2, 4:4 |
| ἡμέρα (anarthrous pl.) | `days` | `days, day-breaks, times` | 4:3 |
| καρπός (gen. pl.) | `of the fruits` | `of the fruits, of the produce, of the returns and profits, of the results` | 4:3 |
| θυσία | `an offering` · `the offerings` | `an offering, a mode of offering, offerings and sacrifices and sacred rites, a festival, the victim` | 4:3, 4:5 |
| κύριος (articular) | `to the lord` · `the lord` | the chain of `lord`, with the article | 4:3, 4:13 |
| στέαρ | `of the stiff fats` | `of the stiff fats and tallow and suet` | 4:4 |
| δῶρον | `the gifts` | `the gifts, the presents, the votive gifts, the blessings` | 4:4 |
| πεδίον | `the plain` · `in the plain` | `the plain, the flat, the plain flat open country` | 4:8 |
| φύλαξ | `a watcher` | `a watcher, a guard, a sentinel, a guardian and keeper and protector, an observer` | 4:9 |
| φωνή (anarthrous) | `sound` | `sound and tone, sound of the voice, cry, faculty of speech and discourse, language, saying` | 4:10 |
| αἷμα | `of blood` · `the blood` | `of blood, of bloodshed and murder, of race and kinship` | 4:10, 4:11 |
| στόμα | `the mouth` | `the mouth, the mouth as the organ of speech, the mouthpiece, the face, the chasm and cleft` | 4:11 |
| χείρ (gen.) | `of the hand` | `of the hand, of the hand and arm, of the arm` | 4:11 |
| ἰσχύς | `the strength` | `the strength, the might and power and force` | 4:12 |
| μέγας (comp.) | `bigger` | `bigger, greater, taller, vaster, stronger and mightier, weightier and more important` | 4:13 |
| αἰτία | `the charge` | `the charge, the accusation, the guilt, the fault, the cause` | 4:13 |
| σημεῖον | `a sign` | `a sign, a mark and token, a sign from the gods and an omen, a signal, a standard and ensign, a boundary` | 4:15 |
| γῆ, with ἐν, anarthrous | `in earth` | `within, inside of, and by means of earth, land, ground` | 4:16 |
| πόλις | `a city` · `the city` | `a city, a citadel, a country, a body of citizens, a state` | 4:17 |
| γυνή (pl.) | `women` · `to the women` | `women, mistresses and ladies, wives and spouses, mortal women` | 4:19, 4:23 |
| εἷς (dat.) | `to the one` | the chain of GEN 2:11 | 4:19 |
| πατήρ | `the father` | the chain of GEN 2:24 | 4:20 |
| σκηνή, with ἐν | `in covered places` | `within, inside of, and by means of covered places and tents, camps, dwelling-places, temples` | 4:20 |
| κτηνοτρόφος | `of those keeping cattle` | `of those keeping cattle and the pastoral` | 4:20 |
| ψαλτήριον | `stringed instrument` | `stringed instrument and psaltery and harp` — LSJ | 4:21 |
| κιθάρα | `lyre` | `lyre, lute` | 4:21 |
| χαλκεύς | `a worker in copper` | `a worker in copper and smith, a joiner, a worker in metal` | 4:22 |
| χαλκός, σίδηρος | `of copper` · `of iron` | `of copper, of metal, of bronze, of anything made of brass and metal, of a copper and caldron and urn, of a brasen mirror, of a copper coin` · `of iron, of a weapon and sword, of a knife and axe-head` | 4:22 |
| λόγος (pl.) | `the words` | `the words, the language and talk, the sayings and statements, the speech and discourse` | 4:23 |
| ἀνήρ (anarthrous) | `man` | `man, man in the prime of life` | 4:23 |
| τραῦμα | `a wound` | `a wound, a hurt and damage, a blow and defeat` | 4:23 |
| μώλωψ | `mark of a stripe` | `mark of a stripe and weal and bruise, blood-clot` — LSJ | 4:23 |
| σπέρμα (acc.) | `that which is sown` | the chain of GEN 3:15, in the accusative | 4:25 |
| ἕτερος | `other` | `other, one of two, the other of two, another, second, different, other than, worse` | 4:25 |

λόγος in the plural, Lamech's words, takes a chain of its own, from the entry's senses for
*words, a saying, speech*; the prologue's chain for ὁ λόγος is not borrowed for it.

Three headwords read furthest from the expected word, and all three are the lexicon's order:
σπέρμα is *that which is sown* before it is offspring; τέκνον is *that which is borne* before
it is a child; τρίβολος is a spiked iron for laming horses before it is a thistle.

### Nouns and adjectives new in GEN 5

| lemma | headword | chain | used |
| --- | --- | --- | --- |
| βίβλος, γένεσις | `the inner bark of the papyrus` · `of origin` | the chains of GEN 2:4 | 5:1 |
| ἄνθρωπος (anarthrous gen. pl.) | `of men` | `of men, of human beings` | 5:1 |
| ἡμέρα | `day` · `the days` | the chains of GEN 2:4 and 3:14 | 5:1–31 |
| θεός (anarthrous gen.) | `of God` | the chain of GEN 1:2 | 5:1 |
| θεός (articular dat.) | `to the God` | `to him who is God definitively, to the one the article marks out, to the known and the only` | 5:22, 5:24 |
| εἰκών | `a likeness` · `the likeness` | `a likeness and an image and portrait, an image in a mirror, a semblance and phantom, an image in the mind, a similitude and simile` | 5:1, 5:3 |
| ἄρσην | `male` | `male, the male sex, masculine and strong, mighty` | 5:2 |
| θῆλυς | `female` | `female, the female sex and womankind, belonging to women, feminine, fresh and refreshing, tender and delicate and gentle, soft and yielding and weak` | 5:2 |
| ὄνομα (articular) | `the name` | the chain of GEN 3:20 | 5:2, 5:3, 5:29 |
| ἰδέα | `the form` | `the form, the look, the outward appearance, the kind and sort and nature, the mode and fashion, the class and species` — sense I reads *= εἶδος, form* | 5:3 |
| ἔργον (gen. pl.) | `of the works` | the short chain of GEN 2:2, in the genitive | 5:29 |
| λύπη (gen. pl.) | `of the pains of body` | the chain of GEN 3:17, in the genitive | 5:29 |
| χείρ (gen. pl.) | `of the hands` | `of the hands, of the hands and arms, of the arms` | 5:29 |

ἰδέα and εἰκών at 5:3 render one Hebrew pair, *dĕmût* and *ṣelem*, that 1:26 rendered with
εἰκών and ὁμοίωσις; each Greek word keeps its own chain, so the reader sees the change of word.

### Nouns and adjectives new in GEN 6

| lemma | headword | chain | used |
| --- | --- | --- | --- |
| ἄνθρωπος (articular pl.) | `the men` · `of the men` · `in the men` | `the men, the human beings, mankind`, in the form | 6:1–5 |
| ἄνθρωπος (anarthrous gen.) | `of man` | `of a man, of a human being` | 6:7, 6:13 |
| πολύς | `many` | `many, often, much and mighty and great, deep, loud, strong, large and wide, far, long` | 6:1 |
| καλός (pl.) | `beautiful` | the chain of GEN 2:9 | 6:2 |
| γυνή | `women` · `the woman` · `the women` | the chains of GEN 2:22 and 4:19, in the form | 6:2, 6:18 |
| πνεῦμα | `the blowing` · `blowing` | the chain of GEN 1:2, with the article at 6:3 | 6:3, 6:17 |
| σάρξ | `fleshes` · `flesh` · `of flesh` | the chain of GEN 2:21, in the form; the plural `fleshes, the flesh, muscles, bodies, man's nature generally` | 6:3, 6:12, 6:17, 6:19 |
| αἰών | `the period of existence` · `of period of existence` | the chain of GEN 3:22, in the form | 6:3, 6:4 |
| γίγας | `the giants` | `the giants, the sons of Gaia, the mighty` — Middle Liddell's *the Giants*, lower case as the Greek is | 6:4 |
| ἡμέρα with ἐν | `in the days` | `within, inside of, and by means of the days, the day-breaks, the times` | 6:4 |
| ὀνομαστός | `named` | `named, to be named, of name and note, notable, famous` | 6:4 |
| κακία (pl.) | `the badnesses` | `the badnesses, the defects, the cowardices and sloths, the moral badnesses and wickednesses and vices, the ill-reputes, the evils` | 6:5 |
| καρδία with ἐν | `in the heart` | `within, inside of, and by means of the heart, the stomach` | 6:5 |
| πονηρός (articular n. pl.) | `the toilsome` | the chain of GEN 2:9, with the article | 6:5 |
| πρόσωπον (anarthrous) | `face` | the chain of GEN 4:14, in the same phrase | 6:7 |
| κτῆνος | `of flocks and herds` · `of the flocks and herds` | `of flocks and herds, of a single beast, of an ox, of a sheep, of a beast for riding`; the articular plural of GEN 3:14 | 6:7, 6:19, 6:20 |
| ἑρπετόν | `of walking animals` · `of the walking animals` | `of walking animals and quadrupeds, of creeping things and reptiles` — *a walking animal* is the first sense, *a creeping thing* the second | 6:7, 6:19, 6:20 |
| πετεινόν, οὐρανός | `of the winged fowl` · `of the heaven` | the chains of GEN 2:19–20, in the genitive | 6:7, 6:17, 6:20 |
| χάρις | `outward grace` | `outward grace, favour, loveliness, graciousness and kindness and goodwill, thankfulness and thanks and gratitude, a favour and kindness and boon, a gratification and delight` — the numbered senses; Perseus's heading, *Grace*, left out | 6:8 |
| γένεσις (pl.) | `the origins` | the chain of GEN 2:4, in the nominative plural | 6:9 |
| δίκαιος | `observant of custom and social rule` | `observant of custom and social rule and well-ordered and civilised, observant of right and righteous, even and well-balanced, regular and exact, right and lawful and just, real and genuine and true, fair and moderate` | 6:9 |
| τέλειος | `having reached its end` | `having reached its end and finished and complete, perfect and without spot or blemish, fullgrown, absolute and accomplished and perfect in his kind, fulfilled` | 6:9 |
| γενεά with ἐν | `in the race` | `within, inside of, and by means of the race, the stock and family, the breed, the tribe and nation, the generation, the offspring, the birth-place, the age and time of life` | 6:9 |
| ἀδικία | `of wrong-doing` | `of wrong-doing and injustice, of a wrong and an injury` | 6:11, 6:13 |
| ὁδός | `the way` | the chain of GEN 3:24 | 6:12 |
| καιρός | `due measure` | `due measure and proportion and fitness, a vital part, the right point of time, the proper time and season, the exact and critical time, the time, advantage and profit and fruit` | 6:13 |
| κιβωτός | `a wooden box` · `the wooden box` · `of the wooden box` | `a wooden box and chest and coffer`, in the form | 6:14–16, 6:18, 6:19 |
| ξύλον (gen. pl.) | `of woods` | `of woods, of firewood, of timbers, of pieces of wood and posts, of sticks` | 6:14 |
| τετράγωνος | `of with four equal angles` | `of with four equal angles and rectangular, of square, of squared, of perfect` — an adjective in the genitive takes *of*, as at 2:9 | 6:14 |
| νοσσιά | `nests of young birds` | `nests of young birds and nests` — under νεοσσιά | 6:14 |
| ἄσφαλτος | `with the asphalt` | `with the asphalt, with the bitumen` | 6:14 |
| πῆχυς | `of fore-arms` · `fore-arm` | `of fore-arms, of arms, of centrepieces of the bow, of horns and sides of the lyre, of cubits and ells, of cubit-rules`, in the form — the measure is sense IV | 6:15, 6:16 |
| μῆκος, πλάτος, ὕψος | `the length` · `the breadth` · `the height` | `the length, the distances, the height and tallness and stature` · `the breadth and width` · `the height, the top and summit and crown` | 6:15 |
| θύρα | `the door` | `the door, the folding doors, the gate, the court, the trap-door, the frame of planks and raft, the entrance` | 6:16 |
| πλάγιος (n. pl. as noun) | `of sides` | `of sides, of flanks` — the first noun sense | 6:16 |
| κατάγαιος | `in the earth` | `in the earth, under the earth and underground and subterranean` — under κατάγειος | 6:16 |
| κατακλυσμός | `the deluge` | `the deluge and inundation` | 6:17 |
| ζωή (anarthrous gen.) | `of a living` | the chain of GEN 2:7 | 6:17 |
| διαθήκη | `the disposition` | `the disposition of property by will, the will and testament, the arrangement between two parties, the covenant` | 6:18 |
| θηρίον (gen. pl.) | `of the wild animals` | the chain of GEN 3:1 | 6:19 |
| ὄρνεον | `of the birds` | `of the birds, of the bird-market` | 6:20 |
| γένος | `race` | `race, stock and family, offspring and posterity, a clan and house, a tribe and caste, a breed, an age and generation, sex and gender, a class and sort and kind, genus` | 6:20 |
| βρῶμα | `of the things which are eaten` | `of the things which are eaten and foods and meats` | 6:21 |

### Nouns and adjectives new in GEN 7

| lemma | headword | chain | used |
| --- | --- | --- | --- |
| οἶκος | `the house` | `the house and abode and dwelling, the room and chamber, the house of a god and temple, the household goods and substance, the household and family` | 7:1 |
| καθαρός (articular gen. pl.) | `of the clear of dirt` | `of the clear of dirt and clean and spotless and unsoiled, of the clear and open and free, of the clear from shame and pollution and pure, of the clear of guilt and defilement and clean and pure, of the purified, of the clear of and from, of the clear of admixture and clear and pure, of the pure and genuine, of the without blemish, of the clear and exact`; μή before it as plain `not` | 7:2, 7:3, 7:8 |
| ἡμέρα (anarthrous gen. pl.) | `of days` | `of days, of day-breaks, of times` | 7:4 |
| ὑετός | `rain` · `the rain` | `rain, a heavy shower` | 7:4, 7:12 |
| νύξ (pl.) | `night-seasons` | `night-seasons, nights, watches of the night, darknesses of night, nights of death` — the first tagged translation is *the night-season* | 7:4, 7:12, 7:17 |
| ἐξανάστασις | `the rising up from` | `the rising up from and resurrection` | 7:4 |
| ἀνάστημα | `the height` | `the height, the majesty, the protuberance and prominence, the high ground, the erection and building and structure, the eruption` — LSJ | 7:23 |
| ζωή with ἐν | `in the life` | `within, inside of, and by means of the life, the means of life and substance, existence, a way of life` — the articular chain of GEN 3:17 | 7:11 |
| πηγή (pl., articular) | `the running waters` | `the running waters, the streams, the founts, the sources, the origins` — the chain of GEN 2:6 | 7:11 |
| ἄβυσσος (gen.) | `of the great deep` | the chain of GEN 1:2, in the genitive | 7:11 |
| καταρράκτης (pl.) | `the broken waters` | `the broken waters and waterfalls, the portcullises, the gulls` — the first noun sense; *down-rushing* is the adjective | 7:11 |
| θηρίον, κτῆνος, ἑρπετόν, πετεινόν (nom.) | `the wild animals` · `the flocks and herds` · `walking animal` · `winged fowl` | the chains of GEN 6, in the nominative | 7:14 |
| ὄρος (pl.) | `the mountains` | `the mountains and hills` | 7:19, 7:20 |
| ὑψηλός (articular pl.) | `the high` | `the high and lofty and high-raised, the highland, the stately` | 7:19, 7:20 |
| πῆχυς (acc. pl.) | `fore-arms` | the chain of GEN 6:15, in the accusative | 7:20 |
| πνοή | `a blowing` | the chain of GEN 2:7 | 7:22 |
| κιβωτός with ἐν | `in the wooden box` | `within, inside of, and by means of the wooden box and chest and coffer` | 7:23 |

### Nouns and adjectives new in GEN 8

| lemma | headword | chain | used |
| --- | --- | --- | --- |
| κεφαλή (pl.) | `the heads` | `the heads, the lives, the tops, the brims, the copings, the sources, the crowns and completions` — the chain of GEN 3:15 in the plural | 8:5 |
| ὄρος (gen. pl.) | `of the mountains` | `of the mountains and hills` | 8:5 |
| κόραξ | `the carrion-crow` | `the carrion-crow, the raven, the engine like a raven's beak for grappling ships, the hooked handle of a door, the instrument of torture` | 8:7 |
| περιστερά | `the common pigeon` | `the common pigeon, the dove` | 8:8–12 |
| ὀπίσω + genitive | `after` | `after, backwards, back and back again, again, hereafter, behind` — the entry's sense with the genitive | 8:8 |
| ἀνάπαυσις | `repose` | `repose, rest, relaxation and recreation, rest from` | 8:9 |
| πούς (dat. pl.) | `to the feet` | `to the feet, to the talons, to the feet of a hill` | 8:9 |
| ἕτερος (pl.) | `other` | the chain of GEN 4:25 | 8:10, 8:12 |
| πάλιν | `back` | `back and backwards, contrariwise, opposite, the change, again and once more and anew, again in turn` | 8:10, 8:12 |
| ἑσπέρα | `evening` | `evening, eventide, eve, nightfall, the west` | 8:11 |
| φύλλον (sg.) | `leaf` | `leaf, foliage, petal, herb` — the chain of GEN 3:7 in the singular | 8:11 |
| ἐλαία | `of olive-tree` | `of olive-tree, of olives, of the fruit of the olive-tree and olive` | 8:11 |
| κάρφος | `a dry stalk` | `a dry stalk, dry sticks, dry twigs and chips and straws and bits of wool` | 8:11 |
| στόμα with ἐν | `in the mouth` | `within, inside of, and by means of the mouth, the mouth as the organ of speech, the mouthpiece, the face, the chasm and cleft` — the chain of GEN 4:11 | 8:11 |
| στέγη | `the roof` | `the roof, the roofed place and chamber and room, the tent` | 8:13 |
| πετεινόν, κτῆνος (anarthrous gen. pl.) | `of winged fowl` · `of flocks and herds` | the chains of GEN 6, without the article | 8:17 |
| ὀσμή | `a smell` | `a smell and scent and an odour` | 8:21 |
| διάνοια | `the thought` | `the thought, the intention and purpose, the notion and opinion, the intelligence and understanding, the meaning` | 8:21 |
| νεότης | `youth` | `youth, youthful spirit and impetuosity, rashness and petulance, a body of youth` | 8:21 |
| ζάω (pres. ptcp.) | `living` | the chain of GEN 2:7 | 8:21 |
| καθώς | `according as` | `according as, just as, like as if, exactly as, how` — the entry opens *= καθά* | 8:21 |
| θερισμός, ψῦχος, καῦμα, θέρος, ἔαρ | `reaping-time` · `cold` · `burning heat` · `summer` · `spring` | `reaping-time, harvest, the crop` · `cold, winter-time, coolness` · `burning heat, sun-heat, fever-heat` · `summer, summertime, summer-fruits and harvest and crop` · `spring, prime and flower` | 8:22 |
| ἡμέρα, νύξ (anarthrous acc. sg.) | `day` · `night-season` | `day, day-break, time` · `night-season, night, the watches of the night, the dark of night, the night of death` | 8:22 |

### Nouns and adjectives new in GEN 9

| lemma | headword | chain | used |
| --- | --- | --- | --- |
| τρόμος | `the trembling` | `the trembling and quaking and quivering` | 9:2 |
| φόβος | `the flight` | `the flight, the panic fear, the fear and terror, the outward show of fear, the object of terror` — *flight*, the only sense in Homer, is sense I | 9:2 |
| πᾶς (dat. pl.) | `to all` | the chain of GEN 2:20 | 9:2, 9:10 |
| θηρίον (dat. pl.) | `to the wild animals` | the chain of GEN 2:20 | 9:2, 9:10 |
| ὄρνεον (pl.) | `the birds` · `of birds` | `the birds, the bird-market`, the chain of GEN 6:20 in the form | 9:2, 9:10 |
| ἰχθύς (pl.) | `the fishes` | `the fishes, the fish-market` | 9:2 |
| θάλασσα | `of the sea` | `of the sea, of the Mediterranean, of a well of salt water` | 9:2 |
| χείρ (acc. pl., anarthrous) · (gen. sg., anarthrous) | `hands` · `of hand` | `hands, hands and arms, arms` · `of hand, of hand and arm, of arm` | 9:2, 9:5 |
| ἑρπετόν | `walking animal` | the chain of GEN 7:14 | 9:3 |
| βρῶσις | `meat` | the chain of GEN 2:9 | 9:3 |
| λάχανον (pl.) | `garden-herbs` | `garden-herbs and potherbs and vegetables and greens, the vegetable-market and green-market` | 9:3 |
| χόρτος (anarthrous gen.) | `of an inclosed place` | the chain of GEN 2:5, in the genitive | 9:3 |
| πᾶς (τὰ πάντα, as a noun) | `the all things` | `the all things, the everything, the whole` — the entry's neuter used as a noun, *all things* | 9:3 |
| κρέας | `flesh` | `flesh and meat and a piece of meat, dressed meat, a body and person` — not σάρξ, whose headword is also *flesh*; the note says which | 9:4 |
| αἷμα | `in blood` · `blood` · `of the blood` | the chain of GEN 4:10, in the form | 9:4, 9:5, 9:6 |
| ψυχή | `of breath` · `of the breaths` · `the breath` · `to breath` | the chain of GEN 2:7, in the form | 9:4, 9:5, 9:10, 9:12, 9:15, 9:16 |
| ἄνθρωπος | `of man` · `of the man` · `the man` · `man` | the chains of GEN 6:7, 8:21, 2:7 and JHN 1:6 | 9:5, 9:6, 9:20 |
| ἀδελφός | `of son of the same mother` · `to sons of the same mother` · `to the sons of the same mother` | the chain of GEN 4:2, in the form | 9:5, 9:22, 9:25 |
| εἰκών with ἐν | `in a likeness` | `within, inside of, and by means of a likeness, …` — the chain of GEN 5:1 | 9:6 |
| σπέρμα (dat.) | `to that which is sown` | the chain of GEN 4:25, in the dative | 9:9 |
| διαθήκη | `the disposition` · `of the disposition` · `of a disposition` · `a disposition` | the chain of GEN 6:18, in the form | 9:9–17 |
| κτῆνος (anarthrous gen. pl.) | `of flocks and herds` | the chain of GEN 8:17 | 9:10 |
| κατακλυσμός | `of the deluge` · `a deluge` · `the deluge` | the chain of GEN 6:17, in the form | 9:11, 9:15, 9:28 |
| σημεῖον | `the sign` · `a sign` | the chain of GEN 4:15, in the form | 9:12, 9:13, 9:17 |
| γενεά (pl.) | `races` | `races, stocks and families, breeds, tribes and nations, generations, offspring, birth-places, ages and times of life` — the chain of GEN 6:9 in the plural | 9:12 |
| αἰώνιος | `lasting for an age` | `lasting for an age, ever-lasting and eternal` | 9:12, 9:16 |
| ζάω (pres. ptcp., attributive) | `of living` · `to the living` | the chain of GEN 2:7 and 3:22, in the form | 9:10, 9:12, 9:15, 9:16 |
| τόξον | `the bow` | `the bow, the bow and arrows, the rays` — τόξῳ, *by guess*, one construction, left out | 9:13, 9:14, 9:16 |
| νεφέλη with ἐν · (pl.) | `in the cloud` · `clouds` | `within, inside of, and by means of the cloud, the bird-net` · `clouds, bird-nets` | 9:13, 9:14, 9:16 |
| πατήρ (anarthrous) | `father` | `father, grandfather` — as μήτηρ at 3:20 | 9:18 |
| οὗτος (pl.) | `these` · `of these` | the chain of GEN 6:9, in the form | 9:19 |
| γεωργός | `a husbandman` | `a husbandman, one tilling the ground` — the first noun sense, then the adjective, as βοηθός at 2:18 | 9:20 |
| γῆ (anarthrous gen.) | `of earth` | the chain of GEN 2:4 | 9:20 |
| οἶκος with ἐν · (pl.) | `in the house` · `in the houses` | the chain of GEN 7:1, in the form | 9:21, 9:27 |
| γύμνωσις | `the stripping` | `the stripping, the nakedness, the defenceless side` | 9:22, 9:23 |
| πατήρ | `the father` · `of the father` | the chain of GEN 2:24, in the form | 9:22, 9:23 |
| ἱμάτιον | `the outer garment` | `the outer garment, the cloak and mantle, the Roman toga, the clothes, the cloth` | 9:23 |
| νῶτον (pl.) | `backs` | `backs, wide surfaces, plains, ridges` — κατὰ νώτου, *from behind*, one construction, left out | 9:23 |
| πρόσωπον | `the face` | the chain of GEN 2:6 | 9:23 |
| ὀπισθοφανής | `seen from behind` | `seen from behind, showing behind, appearing behind or after, reversing the image, looking backwards` — **no Middle Liddell entry**; LSJ, citing 9:23 | 9:23 |
| νέος (comp.) | `the younger` | `the younger, the more youthful, the newer and fresher, the stranger` | 9:24 |
| παῖς | `a child` | `a child, a son, a daughter, a grandchild, a boy and youth and lad, a girl and maiden, a slave and servant and man and maid` — *a slave, servant* is sense III, *in relation to condition* | 9:25, 9:26, 9:27 |
| οἰκέτης | `a house-slave` | `a house-slave and menial` | 9:25 |

### Nouns and adjectives new in GEN 14

| lemma | headword | chain | used |
| --- | --- | --- | --- |
| βασιλεία, with ἐν | `in the kingdom` | the chain of GEN 10:10, after ἐν | 14:1 |
| βασιλεύς | `a king` · `of a king` · `the kings` · `kings` · `of the kings` | `a king and chief, an hereditary king, a lord and master and householder, the second of the nine archons, the king of Persia`, in the form — lower case for *Archons*; the comparative *more kingly* and the example *the king's son, prince* left out | 14:1–22 |
| ἔθνος (gen. and acc. pl.) | `of numbers of people accustomed to live together` · `numbers of …` | the chain of GEN 10:5, anarthrous | 14:1, 14:5, 14:9 |
| πόλεμος | `battle` | `battle and fight and war`, one sense of three glosses | 14:2, 14:8 |
| φάραγξ | `the cleft` | `the cleft and chasm, the ravine and gully` | 14:3 |
| ἁλυκός | `salt` | `salt, brackish` — LSJ, after a plain `the` | 14:3, 14:8, 14:10 |
| θάλασσα | `the sea` | the chain of GEN 12:8, with the article | 14:3 |
| ἅλς | `of the salt` | `of the salt, of the lumps of salt` — the plural's *salt* heads the plural; *the sea*, ἡ ἅλς, is the feminine's | 14:3 |
| γίγας | `the giants` | the chain of GEN 6:4 | 14:5 |
| ἰσχυρός | `strong` | `strong and mighty, hard, obstinate and stiff and stubborn and inveterate and excessive and severe` — the neuter as a noun, the superlative and the adverb left out | 14:5 |
| πόλις | `the city` | the chain of GEN 4:17, with the article, after a name under ἐν | 14:5 |
| ὄρος, with ἐν | `in the mountains` | the chain of GEN 7:19, after ἐν | 14:6 |
| τερέμινθος | `of the terebinth` | `of the terebinth, of the turpentine tree` — under τέρμινθος | 14:6 |
| ἔρημος, with ἐν | `in the desert part` | the chain of GEN 12:9 | 14:6 |
| πηγή | `the running waters` | the chain of GEN 2:6, with the article | 14:7 |
| κρίσις | `of the separating` | `of the separating and power of distinguishing, of the choice and selection, of the decision and judgment, of the means of judging, of the trial, of the result of a trial and condemnation, of the dispute, of the event and issue` | 14:7 |
| ἄρχων | `the rulers` | the chain of GEN 12:15 | 14:7 |
| κοιλάς | `the hollow` · `in the hollow` | `the hollow and deep valley`, and after ἐν | 14:8, 14:10, 14:17 |
| φρέαρ | `wells` | `wells, tanks and cisterns and reservoirs, oil jars` — *(opp. a spring)* left out | 14:10 |
| ἄσφαλτος | `of asphalt` | the chain of GEN 11:3, in the genitive | 14:10 |
| ὀρεινός, used as a noun | `the mountainous` | `the mountainous and hilly, the dwelling on the mountains` | 14:10 |
| ἵππος | `the horse` | `the horse and mare, the horse and cavalry` — ἡ ἵππος; the plural's *chariot-horses* and the compounds' *anything large* left out | 14:11, 14:16, 14:21 |
| βρῶμα | `the things which are eaten` | the chain of GEN 6:21, in the accusative | 14:11 |
| ἀποσκευή | `the removal` | `the removal and riddance, the baggage, the household stuff, the ordure and filth` — LSJ | 14:12 |
| τις | `any one` | the chain of GEN 6:5 | 14:13 |
| περάτης | `to the ferryman` | `to the ferryman, to the boatman and seaman, to the conveyer, to the wanderer and emigrant` — LSJ, through πορθμεύς | 14:13 |
| δρῦς | `to the tree` | the chain of GEN 12:6, in the dative | 14:13 |
| ἀδελφός | `of the son of the same mother` · `of son of the same mother` · `the son of the same mother` | the chains of GEN 4:9, 9:5 and 4:2 | 14:12–16 |
| συνωμότης | `fellow-conspirators` | `fellow-conspirators and confederates` | 14:13 |
| ἴδιος | `one's own` | `one's own, pertaining to oneself, private and personal, peculiar and separate and distinct, peculiar and different, strange and unaccustomed`, after a plain `the` — the noun's and adverb's senses left out | 14:14 |
| οἰκογενής | `born in the house` | `born in the house and homebred` | 14:14 |
| νύξ | `the night-season` | the chain of GEN 8:22, with the article | 14:15 |
| παῖς | `the children` | the chain of GEN 12:16, with the article | 14:15 |
| γυνή | `the women` | the chain of GEN 4:19, with the article | 14:16 |
| λαός | `the people` | `the people, the men, the soldiers, the land-army, the common men, the folk, the Jews, the Christians` | 14:16 |
| κοπή | `of the cutting in pieces` | `of the cutting in pieces and slaughter` — the word of Hebrews 7:1 | 14:17 |
| πεδίον | `the plain` | the chain of GEN 4:8 | 14:17 |
| ἄρτος | `cakes` | `cakes, loaves of wheat-bread, breads` — the chain of GEN 3:19, in the plural | 14:18 |
| ἱερεύς | `a priest` | `a priest and sacrificer, a minister` | 14:18 |
| οὐρανός, γῆ | `the heaven` · `the earth` | the chains of GEN 1:1, *as the counterpart-below* included, since γῆ is paired with οὐρανός | 14:19, 14:22 |
| ἐχθρός, used as a noun | `the one's enemies` | `the one's enemies, the hated and hateful, the hostile and at enmity with` — the noun sense, *one's enemy*, first | 14:20 |
| ὑποχείριος | `under the hand` | `under the hand and in hand, under any one's hand and under command and subject, into one's power` | 14:20 |
| δεκάτη | `tenth part` | `tenth part, tithe, tenth day, tenth day after birth, naming-day, tenth` — under δέκατος, whose noun sense heads it; the adjective's *tenth* last | 14:20 |
| ἀνήρ (pl.) | `the men` · `of the men` | the chain of GEN 3:6, in the plural | 14:21, 14:24 |
| χείρ | `the hand` | the chain of GEN 3:22 | 14:22 |
| σφαιρωτήρ | `of thong` | `of thong and latchet, of a ball, of knop` — LSJ | 14:23 |
| ὑπόδημα | `of a sole bound under the foot with straps` | `of a sole bound under the foot with straps and sandal, of a half-boot` | 14:23 |
| σός, used as a noun | `of the thy property` | `of the thy property, of the thy interests, of the thy and thine and of thee` — τὰ σά's senses, with the article the Greek prints; the masculine's *thy kinsfolk* and the singular's *thy business* left out | 14:23 |
| μερίς | `of the part` · `a part` | `of the part and portion and share and parcel, of the contribution, of the part and division and class`, in the form | 14:24 |

### Nouns and adjectives new in GEN 13

| lemma | headword | chain | used |
| --- | --- | --- | --- |
| ἔρημος, used as a noun | `the desert part` | the chain of GEN 12:9, without ἐν | 13:1, 13:3 |
| πλούσιος | `rich` | `rich, wealthy, opulent, rich in, richly furnished and ample and abundant` | 13:2 |
| κτῆνος (dat. and gen. pl.) | `with flocks and herds` · `of the flocks and herds` | the chain of GEN 2:20, in the form; the dative with *with*, as at 12:17 | 13:2, 13:7 |
| ἀργύριον | `with a piece of silver` | `with a piece of silver, with a silver coin, with money and a sum of money and cash, with silver` | 13:2 |
| χρυσίον | `with a piece of gold` | the chain of GEN 2:11, anarthrous, in the dative | 13:2 |
| σκηνή | `the covered place` · `covered places` | the chain of GEN 12:8 · of GEN 4:20 | 13:3, 13:5 |
| τόπος | `of the place` · `the place` | the chain of GEN 12:6, in the form | 13:3, 13:4, 13:14 |
| ἀρχή | `the beginning` | `the beginning, the origin, the first cause, the headship and rule and governing precedence` — the chain of GEN 2:10 in the singular, with the article | 13:4 |
| βοῦς | `cows` | `cows, oxen, kine and cattle, ox-hide shields` | 13:5 |
| πρόβατον | `things that walk forward` | the chain of GEN 12:16 | 13:5 |
| πολύς | `many` | the chain of GEN 6:1 | 13:6 |
| μάχη | `battle` | `battle and fight and combat, quarrels and strifes and wranglings, a contest, a struggle, a mode of fighting and way of battle, a field of battle` | 13:7, 13:8 |
| ποιμήν | `of the herdsmen` | the chain of GEN 4:2, in the genitive plural | 13:7, 13:8 |
| ἄνθρωπος (pl.) | `men` · `the men` | `men, human beings` · `the men, the human beings, mankind` — the chains of JHN 1:6 and GEN 2:7, in the plural | 13:8, 13:13 |
| ἀδελφός | `sons of the same mother` · `of the son of the same mother` | the chain of GEN 4:2, in the form | 13:8, 13:11 |
| ἀριστερός, used as a noun | `left` | `left and on the left, the left hand, boding ill and ominous` — εἰς ἀριστερά, anarthrous | 13:9 |
| δεξιός, used as a noun | `right` | `right, on the right hand, fortunate and boding good and lucky, dexterous and ready, sharp and shrewd and clever` — εἰς δεξιά: the first noun sense, *the right*, without the article the Greek does not print; the entry's first sense is *on the right hand* | 13:9 |
| περίχωρος | `the country round about` · `of the countries round about` | `the country round about, the round about a place, the people about`, in the form — the entry's sense for ἡ περίχωρος, ahead of the adjective's *round about a place* and οἱ περίχωροι, *the people about* | 13:10, 13:11, 13:12 |
| παράδεισος | `the park` | the chain of GEN 2:8, with the article | 13:10 |
| γῆ | `the earth` · `in earth` · `of the earth` | the chains of GEN 12 | 13:6–17 |
| πόλις, with ἐν | `in city` | `within, inside of, and by means of city, citadel, country, body of citizens, state` — the chain of GEN 4:17, anarthrous, after ἐν | 13:12 |
| πονηρός | `toilsome` | the chain of GEN 2:9, in the nominative | 13:13 |
| ἁμαρτωλός | `sinful` | `sinful, sinners` — the adjective, and as a noun *a sinner* | 13:13 |
| ὀφθαλμός | `the eyes` · `with the eyes` | the chain of GEN 3:5, in the form | 13:10, 13:14 |
| βορρᾶς | `north wind` | `north wind, the north, northward` — under Βορέας, whose *North* is set in lower case, as the Greek has it | 13:14 |
| ἀνατολή | `of risings` · `risings` | the chain of GEN 2:8, in the form | 13:11, 13:14 |
| θάλασσα | `sea` | the chain of GEN 12:8 | 13:14 |
| σπέρμα | `to that which is sown` · `that which is sown` | the chain of GEN 3:15, in the form | 13:15, 13:16 |
| αἰών | `of the period of existence` | the chain of GEN 3:22, in the genitive | 13:15 |
| ἄμμος | `the sand` | `the sand, the sandy ground and race-course` | 13:16 |
| τις | `any one` | the chain of GEN 6:5 | 13:16 |
| μῆκος, πλάτος | `the length` · `the breadth` | the chains of GEN 6:15 | 13:17 |
| δρῦς | `the tree` | the chain of GEN 12:6 | 13:18 |

### Nouns and adjectives new in GEN 12

| lemma | headword | chain | used |
| --- | --- | --- | --- |
| συγγένεια | `of the sameness of descent` | `of the sameness of descent, of the family and relationship and kin, of the ties of kindred and family connexion and influence, of the kinsfolk and kinsmen, of the families` | 12:1 |
| οἶκος (gen.) | `of the house` | the chain of GEN 7:1, in the genitive | 12:1 |
| ἔθνος (sg.) | `a number of people accustomed to live together` | the chain of GEN 10:5, in the singular | 12:2 |
| μέγας | `big` · `with big` | the chain of GEN 10:12, in the form | 12:2, 12:17 |
| τόπος | `of the place` | `of the place, of the local circumstances, of the position, of the passage in a book, of the topic, of the common-place, of the occasion and opportunity` | 12:6 |
| μῆκος | `the length` | the chain of GEN 6:15 | 12:6 |
| δρῦς | `the tree` | `the tree, the oak, the wood, the worn-out old man` — *originally a tree, commonly the oak* | 12:6 |
| ὑψηλός | `high` | the chain of GEN 7:19, after a plain *the* | 12:6 |
| ὄρος | `the mountain` | `the mountain and hill` | 12:8 |
| σκηνή | `the covered place` | `the covered place and tent, the camp, the dwelling-place, the temple` — the chain of GEN 4:20, in the singular | 12:8 |
| θάλασσα (anarthrous) | `sea` | `sea, the Mediterranean, a well of salt water` | 12:8 |
| ὄνομα with ἐπί | `to the name` | the chain of GEN 3:20, in the dative | 12:8 |
| ἔρημος, used as a noun | `in the desert part` | `within, inside of, and by means of the desert part, the desolate and lone and lonely and lonesome and solitary, the desolate and helpless, the reft of and void, the destitute of, the wanting and without, the undefended` — *desert parts*, τὰ ἐρῆμα, is the entry's first noun sense; ἡ ἐρῆμος is given no translation of its own | 12:9 |
| λιμός | `hunger` · `the hunger` | `hunger and famine` | 12:10 |
| εὐπρόσωπος | `fair of face` | `fair of face, with glad countenance, fair in outward show and specious` | 12:11 |
| γυνή | `woman` · `to the woman` · `a woman` · `the woman` | the chains of GEN 2:22 and 8:16, in the form | 12:5, 12:11–20 |
| ψυχή | `breath` · `the breath` | the chain of GEN 2:7 | 12:5, 12:13 |
| καλός | `beautiful` | the chain of GEN 2:9 | 12:14 |
| ἄρχων | `the rulers` | `the rulers and commanders and chiefs and captains, the chief magistrates` | 12:15 |
| πρόβατον | `things that walk forward` | the chain of GEN 4:2, in the nominative | 12:16 |
| μόσχος | `calves` | `calves, young bulls, heifers and young cows, boys and girls and maids, young animals` — under μόσχος² | 12:16 |
| ὄνος | `asses` | `asses, beasts of burden, windlasses and pulleys, upper millstones, beakers and wine-cups` | 12:16 |
| παῖς | `children` | the chain of GEN 9:25, in the plural | 12:16 |
| παιδίσκη | `young girls` | `young girls and maidens, young slaves and courtesans` | 12:16 |
| ἡμίονος | `half-asses` | `half-asses, mules, wild asses` | 12:16 |
| κάμηλος | `camels` | `camels, the camels in an army, the camelry and camel-brigade` | 12:16 |
| ἐτασμός | `with trials` | `with trials, with afflictions` — LSJ, through ἔτασις | 12:17 |
| πονηρός | `with toilsome` | the chain of GEN 2:9, in the dative | 12:17 |
| ἀνήρ | `to men` | the chain of GEN 4:23, in the dative plural | 12:20 |

### Nouns and adjectives new in GEN 11

| lemma | headword | chain | used |
| --- | --- | --- | --- |
| χεῖλος | `lip` · `the lips` | `lip, bill and beak, edge and brink and brim and rim`, in the number — *lip-service* and *with the lips*, pieces of proverbs, left out | 11:1, 11:6, 11:9 |
| εἷς (n.) | `one` | the chain of GEN 2:21 | 11:1, 11:6 |
| φωνή | `sound` · `the sound` | the chain of GEN 4:10, with and without the article | 11:1, 11:7 |
| πεδίον | `a plain` | the chain of GEN 4:8, without the article | 11:2 |
| πῦρ | `with fire` | `with fire, with the funeral-fire, with the fire of the hearth` — the entry's *symbol of things irresistible or terrible* left out | 11:3 |
| λίθος | `a stone` | `a stone, a precious stone, marble` | 11:3 |
| ἄσφαλτος | `asphalt` | `asphalt and bitumen` — the chain of GEN 6:14 | 11:3 |
| πηλός | `the clay` | `the clay and earth, the mud and mire` | 11:3 |
| πόλις | `a city` · `the city` | the chain of GEN 4:17 | 11:4, 11:5, 11:8 |
| πύργος | `a tower` · `the tower` | `a tower, the city walls with towers, a movable tower for storming, a tower of defence, the highest part of any building, troops drawn up in close order and a column`, with and without the article | 11:4, 11:5, 11:8 |
| κεφαλή | `the head` | the chain of GEN 3:15, with the article | 11:4 |
| πρόσωπον | `of face` · `face` | the chain of GEN 3:8, anarthrous | 11:4, 11:8, 11:9 |
| γένος | `race` | the chain of GEN 6:20 | 11:6 |
| γλῶσσα | `the tongue` | the chain of GEN 10:5, with the article | 11:7 |
| ὄνομα | `the name` · `a name` | the chains of GEN 3:20 and 2:11 | 11:4, 11:9, 11:29 |
| χώρα | `in the space in which a thing is` · `of the space …` | the chain of GEN 10:20, in the singular | 11:28, 11:31 |
| γυνή | `women` · `to the woman` · `a woman` | the chains of GEN 4:19 and 2:22, in the form | 11:29, 11:31 |
| πατήρ | `of the father` · `father` | the chains of GEN 9:22 and 9:18 | 11:28, 11:29 |
| στεῖρα | `a cow that has not calved` | `a cow that has not calved, barren` — *barren*, of a woman, is the entry's second translation, citing the New Testament | 11:30 |
| νύμφη | `the young wife` | `the young wife and bride, the married woman, the marriageable maiden, the nymph, the chrysalis and pupa` — *daughter-in-law*, the verse's sense, is sense 4, untagged | 11:31 |

### Nouns and adjectives new in GEN 10

| lemma | headword | chain | used |
| --- | --- | --- | --- |
| γένεσις (pl.) | `the origins` · `origins` | the chain of GEN 6:9, with and without the article | 10:1, 10:32 |
| ἔθνος (pl.) | `of the numbers of people accustomed to live together` · `in the …` · `the …` | `of the numbers of people accustomed to live together and companies and bodies of men, of the hosts, of the swarms and flocks, of the nations and peoples, of the nations and gentiles, of the special classes, of the castes and tribes, of the sexes`, in the form — *a nation* is sense 2; *Gentiles* lower case | 10:5, 10:20, 10:31, 10:32 |
| γῆ with ἐν | `in the earth` | `within, inside of, and by means of the earth, the land, the ground` | 10:5, 10:10 |
| γλῶσσα | `tongue` · `tongues` | `tongue, tongue as the organ of speech, tongue and language, mouthpiece of a pipe`, in the number | 10:5, 10:20, 10:31 |
| φυλή (pl.) | `in the races` · `the races` | `within, inside of, and by means of the races, the tribes, the bodies united by ties of blood and descent, the clans, the tribes by local habitation, the hundreds and counties, the contingents furnished by a tribe, the brigades` | 10:5, 10:18, 10:20, 10:31, 10:32 |
| γίγας (sg.) | `giant` | `giant, son of Gaia, mighty` — the chain of GEN 6:4 in the singular | 10:8, 10:9 |
| κυνηγός | `hound-leader` | `hound-leader, huntsman` — under κυναγός | 10:9 |
| κύριος, θεός (gen.) | `of lord` · `of the God` | the chains of GEN 3:8 | 10:9 |
| ἀρχή | `beginning` | `beginning, origin, first cause, headship and rule and governing precedence` — the chain of GEN 2:10 in the singular | 10:10 |
| βασιλεία | `of the kingdom` | `of the kingdom and dominion, of the hereditary monarchy` | 10:10 |
| ἐκεῖνος (gen.) | `of that` | the chain of GEN 2:12 | 10:11 |
| πόλις | `the city` | the chain of GEN 4:17, with the article | 10:11, 10:12 |
| μέγας | `big` · `of the bigger` | `big, great, tall, full-grown, vast and high, spacious and wide, strong and mighty, violent, loud, prevailing, weighty and important`; the comparative, the chain of GEN 4:13 in the genitive | 10:12, 10:21 |
| ὅριον (pl.) | `the boundaries` | `the boundaries and limits, the borders, the frontier` | 10:19 |
| χώρα (pl.) with ἐν | `in the spaces in which a thing is` | `within, inside of, and by means of the spaces in which a thing is, the places, the positions and posts, the places in life and stations, the lands and countries, the pieces of land and estates and farms, the countries` | 10:20, 10:31 |
| πατήρ (dat.) | `to father` | `to father, to grandfather` | 10:21 |
| ἀδελφός (dat.) | `to son of the same mother` · `to the son of the same mother` | the chain of GEN 4:2, in the form | 10:21, 10:25 |
| ὄνομα, εἷς | `a name` · `to the one` | the chains of GEN 2:11 | 10:25 |
| ὄρος (sg.) | `a mountain` | `a mountain and hill` | 10:30 |
| ἀνατολή (gen. pl.) | `of risings` | the chain of GEN 2:8, in the genitive | 10:30 |

Nearly every other word of the chapter is a name. A people's name declined in Greek — Κίτιοι,
Ῥόδιοι, Χετταῖος, Ἀράδιος, Χαναναῖος — is glossed like a person's, with its English form in the
anchored panel (*Citians*, *Hittite*, *Canaanites*); where the Greek names a different people from
the Hebrew (Ῥόδιοι for *Dōdānîm*), it is the Greek's that is anchored, and the note gives the Hebrew.
A name glossed in one case is bare in another (Σιδῶνα at 10:15, Σιδῶνος at 10:19).

---

## Aspect formulas

Fixed wording. These go in the reading text, never in a footnote. The word-by-word layer
uses the same wording.

| aspect | formula | where it sits |
| --- | --- | --- |
| aorist | the plain English past — *(retired before Genesis 38: the formula `one completed act seen whole, not a process observed in progress` stood after 59 of Genesis 1–11's aorists and none after; it is the word-by-word layer's line now)* | — |
| imperfect (state) | `and kept on being as a standing and continuing condition` | inside ἦν's plain text |
| imperfect (εἰμί, pre-existence) | `was already in unbroken existence without any point of having come to be` | inside ἦν's plain text |
| imperfect (other verbs) | `was being …` | inside the verb's chain and headword (ἐπιφέρω) |
| perfect | a standing resultant state, not a past event — worded to the verb | inside the verb's chain |

---

## Names

Gloss on first occurrence per chapter, bare thereafter.

| Greek | unanchored form | anchored form | gloss |
| --- | --- | --- | --- |
| Ἰωάννης | Iōannēs | John | `(Ἰωάννης, from Hebrew Yôḥānān, "Yah has shown favour")` |
| Εδεμ | Edem | Eden | `(Εδεμ, from Hebrew ʿĒden, "delight, luxury")` |
| Φισων | Phisōn | Pishon | `(Φισων, from Hebrew Pîšôn, perhaps from pûš, "to leap, spring")` |
| Ευιλατ | Euilat | Havilah | `(Ευιλατ, from Hebrew Ḥăwîlâ, usually connected with ḥôl, "sand")` |
| Γηων | Gēōn | Gihon | `(Γηων, from Hebrew Gîḥôn, from gîaḥ, "to burst forth")` |
| Αἰθιοπίας | Aithiopia | Ethiopia | `(Αἰθιοπίας, from αἴθω, "to burn", and ὤψ, "face"; Hebrew Kûš)` |
| Τίγρις | Tigris | Tigris | `(Τίγρις, from Old Persian tigrā, "arrow", for its swiftness; Hebrew Ḥiddeqel)` |
| Ἀσσυρίων | Assyriōn | Assyrians | `(Ἀσσυρίων, the Assyrians, from Aššur — their god, their city, and their land)` |
| Εὐφράτης | Euphratēs | Euphrates | `(Εὐφράτης, from Old Persian Ufrātu; Hebrew Pĕrāt)` |
| Αδαμ | Adam | Adam | `(Αδαμ, from Hebrew ʾādām, "man", from ʾădāmâ, "ground")` |
| Ζωή | Zōē | Zoe | `(Ζωή, "life"; Hebrew Ḥawwâ, from ḥāyâ, "to live")` |
| χερουβιμ | cheroubim | cherubim | `(χερουβιμ, the Hebrew plural kĕrûbîm, of kĕrûb, a word of uncertain derivation)` |
| Ευαν | Euan | Eve | `(Ευαν, from Hebrew Ḥawwâ, which 3:20 translated Ζωή, "life")` |
| Καιν | Kain | Cain | `(Καιν, from Hebrew Qayin, which the verse ties to qānâ, "to get, acquire")` |
| Αβελ | Abel | Abel | `(Αβελ, from Hebrew Hebel, "breath, vapour")` |
| Ναιδ | Naid | Nod | `(Ναιδ, from Hebrew Nôd, "wandering")` |
| Ενωχ | Enōch | Enoch | `(Ενωχ, from Hebrew Ḥănôk, usually connected with ḥānak, "to dedicate")` |
| Γαιδαδ | Gaidad | Irad | `(Γαιδαδ, from Hebrew ʿÎrād, of uncertain meaning)` |
| Μαιηλ | Maiēl | Mehujael | `(Μαιηλ, from Hebrew Mĕḥûyāʾēl, of uncertain meaning, ending in ʾēl, "God")` |
| Μαθουσαλα | Mathousala | Methuselah | `(Μαθουσαλα, the Greek form of Hebrew Mĕtûšelaḥ at 5:21, given here for Mĕtûšāʾēl, usually explained as "man of God")` |
| Λαμεχ | Lamech | Lamech | `(Λαμεχ, from Hebrew Lemek, of uncertain meaning)` |
| Αδα | Ada | Adah | `(Αδα, from Hebrew ʿĀdâ, usually connected with ʿădî, "ornament")` |
| Σελλα | Sella | Zillah | `(Σελλα, from Hebrew Ṣillâ, usually connected with ṣēl, "shade")` |
| Ιωβελ | Iōbel | Jabal | `(Ιωβελ, from Hebrew Yābāl, usually connected with yābal, "to lead, bring")` |
| Ιουβαλ | Ioubal | Jubal | `(Ιουβαλ, from Hebrew Yûbal, usually connected with yābal, "to lead, bring")` |
| Θοβελ | Thobel | Tubal | `(Θοβελ, from Hebrew Tûbal-qayin, without its second part)` |
| Νοεμα | Noema | Naamah | `(Νοεμα, from Hebrew Naʿămâ, "pleasant")` |
| Σηθ | Sēth | Seth | `(Σηθ, from Hebrew Šēt, which the verse ties to šît, "to set, appoint")` |
| Ενως | Enōs | Enosh | `(Ενως, from Hebrew ʾĕnôš, "man, mankind")` |
| Σηθ (GEN 5) | Sēth | Seth | `(Σηθ, from Hebrew Šēt, which 4:25 ties to šît, "to set, appoint")` |
| Καιναν | Kainan | Kenan | `(Καιναν, from Hebrew Qênān, usually connected with Qayin, the name of Cain)` |
| Μαλελεηλ | Maleleēl | Mahalalel | `(Μαλελεηλ, from Hebrew Mahălalʾēl, "praise of God")` |
| Ιαρεδ | Iared | Jared | `(Ιαρεδ, from Hebrew Yered, usually connected with yārad, "to go down")` |
| Μαθουσαλα (GEN 5) | Mathousala | Methuselah | `(Μαθουσαλα, from Hebrew Mĕtûšelaḥ, usually explained as "man of the javelin")` |
| Νωε | Nōe | Noah | `(Νωε, from Hebrew Nōaḥ, usually connected with nûaḥ, "to rest")` |
| Σημ | Sēm | Shem | `(Σημ, from Hebrew Šēm, "name")` |
| Χαμ | Cham | Ham | `(Χαμ, from Hebrew Ḥām, usually connected with ḥam, "hot")` |
| Ιαφεθ | Iapheth | Japheth | `(Ιαφεθ, from Hebrew Yepet, which 9:27 ties to pātâ, "to make wide")` |
| Χανααν | Chanaan | Canaan | `(Χανααν, from Hebrew Kĕnaʿan, of uncertain meaning)` |
| GEN 10 | | | ninety-one names, their glosses in `data/GEN/10.json`; the anchored forms are the English Bible's, and Κίτιοι, Ῥόδιοι are *Citians*, *Rhodians* |
| Σύγχυσις | Synchysis | Confusion | `(Σύγχυσις, "a commixture, confusion", for Hebrew Bābel, which the verse ties to bālal, "to confuse")` |
| Ραγαυ | Ragau | Reu | `(Ραγαυ, from Hebrew Rĕʿû, usually connected with rēaʿ, "friend")` |
| Σερουχ | Serouch | Serug | `(Σερουχ, from Hebrew Śĕrûg, of uncertain meaning)` |
| Ναχωρ | Nachōr | Nahor | `(Ναχωρ, from Hebrew Nāḥôr, of uncertain meaning)` |
| Θαρα | Thara | Terah | `(Θαρα, from Hebrew Teraḥ, of uncertain meaning)` |
| Αβραμ | Abram | Abram | `(Αβραμ, from Hebrew ʾAbrām, "the father is exalted")` |
| Αρραν | Arran | Haran | `(Αρραν, from Hebrew Hārān, of uncertain meaning)` |
| Λωτ | Lōt | Lot | `(Λωτ, from Hebrew Lôṭ, of uncertain meaning)` |
| Χαλδαίων | Chaldaiōn | Chaldeans | `(Χαλδαῖος, the Greek name of Hebrew Kaśdîm)` |
| Σαρα, Σαραν | Sara, Saran | Sarai | `(Σαρα, from Hebrew Śāray, usually connected with śārâ, "princess")` — bare in the accusative |
| Μελχα | Melcha | Milcah | `(Μελχα, from Hebrew Milkâ, usually connected with malkâ, "queen")` |
| Ιεσχα | Iescha | Iscah | `(Ιεσχα, from Hebrew Yiskâ, of uncertain meaning)` |
| Χαρραν | Charran | Haran | `(Χαρραν, from Hebrew Ḥārān, the city Harran)` |

| Αἴγυπτον | Aigypton | Egypt | `(Αἴγυπτος, the Greek name of the land; Hebrew Miṣrayim)` |
| Αἰγύπτιοι | Aigyptioi | Egyptians | `(Αἰγύπτιος, the man of Αἴγυπτος, Egypt)` |
| Φαραω | Pharaō | Pharaoh | `(Φαραω, from Hebrew Parʿōh, from the Egyptian for "great house")` |
| Συχεμ | Sychem | Shechem | `(Συχεμ, from Hebrew Šĕkem, "shoulder")` |
| Βαιθηλ | Baithēl | Bethel | `(Βαιθηλ, from Hebrew Bêt-ʾēl, "house of God")` |
| Αγγαι | Angai | Ai | `(Αγγαι, from Hebrew hāʿAy, "the ruin")` |
| Χαναναῖοι | Chananaioi | Canaanites | `(Χαναναῖος, from Hebrew Kĕnaʿănî, "of Canaan")` |

Αἰγύπτιοι and Αἴγυπτον stand in one verse at 12:14, and `validate.py` took the people for a case of
the land's name; names now match only where what differs is a case ending on both sides.

| Φερεζαῖοι | Pherezaioi | Perizzites | `(Φερεζαῖος, from Hebrew Pĕrizzî, usually connected with pĕrāzî, "a villager")` |
| Ιορδάνου | Iordanou | Jordan | `(Ἰορδάνης, from Hebrew Yardēn, usually connected with yārad, "to go down")` |
| Σοδομα, Σοδομοις | Sodoma, Sodomois | Sodom | `(Σόδομα, from Hebrew Sĕdōm, of uncertain meaning)` — the gloss of GEN 10:19; bare in the dative |
| Γομορρα | Gomorra | Gomorrah | `(Γόμορρα, from Hebrew ʿĂmōrâ, of uncertain meaning)` — the gloss of GEN 10:19 |
| Ζογορα | Zogora | Zoar | `(Ζογορα, from Hebrew Ṣōʿar, "small")` |
| Μαμβρη | Mambrē | Mamre | `(Μαμβρη, from Hebrew Mamrēʾ, of uncertain meaning)` |
| Χεβρων | Chebrōn | Hebron | `(Χεβρων, from Hebrew Ḥebrôn, usually connected with ḥeber, "association")` |

Σοδομοις at 13:12 is two letters longer than Σοδομα at 13:10, and `validate.py` matched two forms of
a name only within one letter of each other's length, which keeps Καιν apart from Καιναν. It now
allows more where both forms carry a case ending, with a test.

| Αμαρφαλ | Amarphal | Amraphel | `(Αμαρφαλ, from Hebrew ʾAmrāpel, of uncertain meaning)` |
| Αριωχ | Ariōch | Arioch | `(Αριωχ, from Hebrew ʾAryôk, of uncertain meaning)` |
| Ελλασαρ | Ellasar | Ellasar | `(Ελλασαρ, from Hebrew ʾEllāsār, of uncertain meaning)` |
| Χοδολλογομορ | Chodollogomor | Chedorlaomer | `(Χοδολλογομορ, from Hebrew Kĕdorlāʿōmer, usually connected with the Elamite for "servant of Lagamar")` |
| Θαργαλ | Thargal | Tidal | `(Θαργαλ, from Hebrew Tidʿāl, of uncertain meaning)` |
| Βαλλα | Balla | Bera | `(Βαλλα, from Hebrew Beraʿ, of uncertain meaning)` |
| Βαρσα | Barsa | Birsha | `(Βαρσα, from Hebrew Biršaʿ, of uncertain meaning)` |
| Σεννααρ (the king) | Sennaar | Shinab | `(Σεννααρ, for Hebrew Šinʾāb, of uncertain meaning)` |
| Συμοβορ | Symobor | Shemeber | `(Συμοβορ, from Hebrew Šemʾēber, of uncertain meaning)` |
| Βαλακ | Balak | Bela | `(Βαλακ, from Hebrew Belaʿ, usually connected with bālaʿ, "to swallow")` |
| Σηγωρ | Sēgōr | Zoar | `(Σηγωρ, from Hebrew Ṣōʿar, "small")` |
| Ασταρωθ, Καρναιν | Astarōth, Karnain | Ashteroth, Karnaim | `(Ασταρωθ, from Hebrew ʿAštĕrōt, the goddess Astarte, in the plural)`, `(Καρναιν, from Hebrew Qarnayim, "two horns")` |
| Ομμαίους | Ommaious | Emim | `(Ομμαῖος, from Hebrew ʾÊmîm, usually connected with ʾêmâ, "terror")` |
| Σαυη | Sauē | Shaveh | `(Σαυη, from Hebrew Šāwēh, "level plain")` |
| Χορραίους | Chorraious | Horites | `(Χορραῖος, from Hebrew Ḥōrî, usually connected with ḥōr, "cave")` |
| Σηιρ | Sēir | Seir | `(Σηιρ, from Hebrew Śēʿîr, "hairy")` |
| Φαραν | Pharan | Paran | `(Φαραν, from Hebrew Pāʾrān, of uncertain meaning)` |
| Καδης | Kadēs | Kadesh | `(Καδης, from Hebrew Qādēš, "holy")` |
| Αμαληκ | Amalēk | Amalek | `(Αμαληκ, from Hebrew ʿĂmālēq, of uncertain meaning)` |
| Ασασανθαμαρ | Asasanthamar | Hazazon-tamar | `(Ασασανθαμαρ, from Hebrew Ḥaṣăṣōn Tāmār, the second word "palm tree")` |
| Αμορις | Amoris | Amorite | `(Αμορις, from Hebrew hāʾĔmōrî, "the Amorite")` |
| Εσχωλ | Eschōl | Eshcol | `(Εσχωλ, from Hebrew ʾEškōl, "cluster")` |
| Αυναν | Aunan | Aner | `(Αυναν, from Hebrew ʿĀnēr, of uncertain meaning)` |
| Δαν | Dan | Dan | `(Δαν, from Hebrew Dān, "judge")` |
| Χωβα | Chōba | Hobah | `(Χωβα, from Hebrew Ḥôbâ, of uncertain meaning)` |
| Δαμασκοῦ | Damaskou | Damascus | `(Δαμασκός, from Hebrew Dammeśeq, of uncertain meaning)` |
| Μελχισεδεκ | Melchisedek | Melchizedek | `(Μελχισεδεκ, from Hebrew Malkî-ṣedeq, "king of righteousness")` |
| Σαλημ | Salēm | Salem | `(Σαλημ, from Hebrew Šālēm, usually connected with šālôm, "peace")` |

GEN 14 prints Σεννααρ twice for two bearers: the land, Shinar, at 14:1 and 14:9, and Shinab, king
of Adama, at 14:2. Each is glossed on its first occurrence. `validate.py` counted a name as glossed
by its Greek form alone, and would have called the king's gloss a second gloss of the land; it now
tells bearers apart by their English names, with a test, and `words.py` gives each card its own
bearer's gloss. Σηγωρ is the Ζογορα of 13:10, spelt another way.

| Μασεκ | Masek | Mesek | `(Μασεκ, from Hebrew mešeq, which the Hebrew does not use as a name, of uncertain meaning)` |
| Ελιεζερ | Eliezer | Eliezer | `(Ελιεζερ, from Hebrew ʾĔlîʿezer, "my God is help")` |
| Αμορραίων | Amorraiōn | Amorites | `(Αμορραῖος, from Hebrew ʾĔmōrî, of uncertain meaning)` |
| Καιναίους | Kainaious | Kenites | `(Καιναῖος, from Hebrew Qênî, usually connected with qayin, "smith")` |
| Κενεζαίους | Kenezaious | Kenizzites | `(Κενεζαῖος, from Hebrew Qĕnizzî, of uncertain meaning)` |
| Κεδμωναίους | Kedmōnaious | Kadmonites | `(Κεδμωναῖος, from Hebrew Qadmōnî, "eastern")` |
| Χετταίους | Chettaious | Hittites | `(Χετταῖος, from Hebrew Ḥittî, "of Ḥēt")` |
| Ραφαϊν | Raphain | Rephaim | `(Ραφαϊν, from Hebrew Rĕpāʾîm, of uncertain meaning)` |
| Ευαίους | Euaious | Hivites | `(Ευαῖος, from Hebrew Ḥiwwî, of uncertain meaning)` |
| Γεργεσαίους | Gergesaious | Girgashites | `(Γεργεσαῖος, from Hebrew Girgāšî, of uncertain meaning)` |
| Ιεβουσαίους | Iebousaious | Jebusites | `(Ιεβουσαῖος, from Hebrew Yĕbûsî, "of Jebus")` |

GEN 15:2's Μασεκ is the Hebrew *mešeq*, which occurs nowhere else and is not a name there; the
Greek makes it a woman's, the mother of Eliezer, whom it calls Δαμασκὸς Ελιεζερ.

| Αἰγυπτία | Aigyptia | Egyptian | `(Αἰγυπτία, the woman of Αἴγυπτος, Egypt)` |
| Αγαρ | Agar | Hagar | `(Αγαρ, from Hebrew Hāgār, of uncertain meaning)` |
| Σουρ | Sour | Shur | `(Σουρ, from Hebrew Šûr, "wall")` |
| Ισμαηλ | Ismaēl | Ishmael | `(Ισμαηλ, from Hebrew Yišmāʿēʾl, "God hears")` |
| Φρέαρ | Phrear | Well | `(Φρέαρ, "a well", the first word of the name the verse gives the well, for Hebrew Bĕʾēr laḥay rōʾî)` |
| Βαραδ | Barad | Bered | `(Βαραδ, from Hebrew Bered, "hail")` |

| Αβρααμ | Abraam | Abraham | `(Αβρααμ, from Hebrew ʾAbrāhām, which the Hebrew of 17:5 hears in ʾab hămôn gôyim, "father of a multitude of nations")` |
| Σαρρα | Sarra | Sarah | `(Σαρρα, from Hebrew Śārâ, "princess")` |
| Ισαακ | Isaak | Isaac | `(Ισαακ, from Hebrew Yiṣḥāq, "he laughs")` |

| Σοδομῖται | Sodomitai | Sodomites | `(Σοδομῖται, the men of Σόδομα, Sodom)` |
| Μωαβ | Mōab | Moab | `(Μωαβ, from Hebrew Môʾāb, of uncertain meaning)` |
| Μωαβιτῶν | Mōabitōn | Moabites | `(Μωαβῖται, the people of Μωαβ, Moab)` |
| Αμμαν | Amman | Ammon | `(Αμμαν, for Hebrew Ben-ʿammî, "son of my people")` |
| Αμμανιτῶν | Ammanitōn | Ammonites | `(Αμμανῖται, the people of Αμμαν, for Hebrew bĕnê-ʿammôn, the sons of Ammon)` |

| Γεραροις | Gerarois | Gerar | `(Γεραρα, from Hebrew Gĕrār, of uncertain meaning)` |
| Αβιμελεχ | Abimelech | Abimelech | `(Αβιμελεχ, from Hebrew ʾĂbîmelek, "my father is king")` |

| Οχοζαθ | Ochozath | Ahuzzath | `(Οχοζαθ, from Hebrew ʾĂḥuzzat, "possession")` |
| Φικολ | Phikol | Phicol | `(Φικολ, from Hebrew Pîkōl, of uncertain meaning)` |
| Φυλιστιιμ | Phylistiim | Philistines | `(Φυλιστιιμ, from Hebrew Pĕlištîm, the people of Pĕlešet)` |

| σαβεκ | sabek | sabek | `(σαβεκ, for Hebrew sĕbak, "a thicket")` |
| Ωξ | Ōx | Uz | `(Ωξ, from Hebrew ʿÛṣ, of uncertain meaning)` |
| Βαυξ | Baux | Buz | `(Βαυξ, from Hebrew Bûz, of uncertain meaning)` |
| Καμουηλ | Kamouēl | Kemuel | `(Καμουηλ, from Hebrew Qĕmûʾēl, of uncertain meaning)` |
| Σύρων | Syrōn | Syrians | `(Σύρος, the man of Συρία, Syria, for Hebrew ʾĂrām)` |
| Χασαδ | Chasad | Chesed | `(Χασαδ, from Hebrew Keśed, of uncertain meaning)` |
| Αζαυ | Azau | Hazo | `(Αζαυ, from Hebrew Ḥăzô, of uncertain meaning)` |
| Φαλδας | Phaldas | Pildash | `(Φαλδας, from Hebrew Pildāš, of uncertain meaning)` |
| Ιεδλαφ | Iedlaph | Jidlaph | `(Ιεδλαφ, from Hebrew Yidlāp, of uncertain meaning)` |
| Βαθουηλ | Bathouēl | Bethuel | `(Βαθουηλ, from Hebrew Bĕtûʾēl, of uncertain meaning)` |
| Ρεβεκκαν | Rebekkan | Rebekah | `(Ρεβεκκα, from Hebrew Ribqâ, of uncertain meaning)` |
| Ρεημα | Reēma | Reumah | `(Ρεημα, from Hebrew Rĕʾûmâ, of uncertain meaning)` |
| Ταβεκ | Tabek | Tebah | `(Ταβεκ, from Hebrew Ṭebaḥ, of uncertain meaning)` |
| Γααμ | Gaam | Gaham | `(Γααμ, from Hebrew Gaḥam, of uncertain meaning)` |
| Τοχος | Tochos | Tahash | `(Τοχος, from Hebrew Taḥaš, of uncertain meaning)` |
| Μωχα | Mōcha | Maacah | `(Μωχα, from Hebrew Maʿăkâ, of uncertain meaning)` |

| Αρβοκ | Arbok | Arba | `(Αρβοκ, for Hebrew Qiryat ʾarbaʿ, "city of Arba" or "city of four")` |
| Χετ | Chet | Heth | `(Χετ, from Hebrew Ḥēt, of uncertain meaning)` |
| Εφρων | Ephrōn | Ephron | `(Εφρων, from Hebrew ʿEprôn, of uncertain meaning)` |
| Σααρ | Saar | Zohar | `(Σααρ, from Hebrew Ṣōḥar, of uncertain meaning)` |
| Χετταῖος | Chettaios | Hittite | `(Χετταῖος, the man of Χετ, Heth; Hebrew Ḥittî)` |

| Μεσοποταμίαν | Mesopotamian | Mesopotamia | `(Μεσοποταμία, Greek, "the land between the rivers", for Hebrew ʾĂram Nahărayim, "Aram of the two rivers")` |
| Λαβαν | Laban | Laban | `(Λαβαν, from Hebrew Lābān, "white")` |

| Χεττουρα | Chettoura | Keturah | `(Χεττουρα, from Hebrew Qĕṭûrâ, usually connected with qĕṭōret, "incense")` |
| Ζεμραν | Zemran | Zimran | `(Ζεμραν, from Hebrew Zimrān, of uncertain meaning)` |
| Ιεξαν | Iexan | Jokshan | `(Ιεξαν, from Hebrew Yoqšān, of uncertain meaning)` |
| Μαδαν | Madan | Medan | `(Μαδαν, from Hebrew Mĕdān, of uncertain meaning)` |
| Μαδιαμ | Madiam | Midian | `(Μαδιαμ, from Hebrew Midyān, of uncertain meaning)` |
| Ιεσβοκ | Iesbok | Ishbak | `(Ιεσβοκ, from Hebrew Yišbāq, of uncertain meaning)` |
| Σωυε | Sōue | Shuah | `(Σωυε, from Hebrew Šûaḥ, usually connected with šûaḥ, "to sink down")` |
| Σαβα | Saba | Sheba | `(Σαβα, from Hebrew Šĕbāʾ, of uncertain meaning)` |
| Θαιμαν | Thaiman | Teman | `(Θαιμαν, from Hebrew Têmān, "south" or "the south country")` |
| Δαιδαν | Daidan | Dedan | `(Δαιδαν, from Hebrew Dĕdān, of uncertain meaning)` |
| Ραγουηλ | Ragouēl | Reuel | `(Ραγουηλ, from Hebrew Rĕʿûʾēl, "friend of God")` |
| Ναβδεηλ | Nabdeēl | Nabdeel | `(Ναβδεηλ, for Hebrew ʿAbdĕʾēl, "servant of God", as at 25:13)` |
| Ασσουριιμ | Assouriim | Asshurim | `(Ασσουριιμ, from Hebrew ʾAššûrim, a people of the Hebrew plural in -îm)` |
| Λατουσιιμ | Latousiim | Letushim | `(Λατουσιιμ, from Hebrew Lĕṭûšim, a people of the Hebrew plural in -îm)` |
| Λοωμιμ | Loōmim | Leummim | `(Λοωμιμ, from Hebrew Lĕʾummim, a people of the Hebrew plural in -îm, connected with lĕʾōm, "people")` |
| Γαιφα | Gaipha | Ephah | `(Γαιφα, for Hebrew ʿÊpâ, of uncertain meaning)` |
| Αφερ | Apher | Epher | `(Αφερ, from Hebrew ʿĒper, usually connected with ʿōper, "fawn")` |
| Αβιρα | Abira | Abida | `(Αβιρα, for Hebrew ʾĂbîdāʿ, "my father knows")` |
| Ελραγα | Elraga | Eldaah | `(Ελραγα, for Hebrew ʾEldāʿâ, of uncertain meaning)` |
| Ναβαιωθ | Nabaiōth | Nebaioth | `(Ναβαιωθ, from Hebrew Nĕbāyôt, of uncertain meaning)` |
| Κηδαρ | Kēdar | Kedar | `(Κηδαρ, from Hebrew Qēdār, usually connected with qādar, "to be dark")` |
| Μασσαμ | Massam | Mibsam | `(Μασσαμ, for Hebrew Mibśām, usually connected with bōśem, "balsam, spice")` |
| Μασμα | Masma | Mishma | `(Μασμα, from Hebrew Mišmāʿ, usually connected with šāmaʿ, "to hear")` |
| Ιδουμα | Idouma | Dumah | `(Ιδουμα, for Hebrew Dûmâ, usually connected with dāmam, "to be silent")` |
| Μασση | Massē | Massa | `(Μασση, from Hebrew Maśśāʾ, usually connected with nāśāʾ, "to lift, bear")` |
| Χοδδαδ | Choddad | Hadad | `(Χοδδαδ, for Hebrew Ḥădad, the name of a storm-god)` |
| Ιετουρ | Ietour | Jetur | `(Ιετουρ, from Hebrew Yĕṭûr, of uncertain meaning)` |
| Ναφες | Naphes | Naphish | `(Ναφες, from Hebrew Nāpîš, usually connected with nepeš, "breath, soul")` |
| Κεδμα | Kedma | Kedemah | `(Κεδμα, from Hebrew Qēdĕmâ, usually connected with qedem, "east")` |
| Ἀσσυρίους | Assyrious | Assyrians | `(Ἀσσύριος, the Assyrian, from Aššur — their god, their city, and their land)` |
| Σύρου | Syrou | Syrian | `(Σύρος, the man of Συρία, Syria; the Hebrew has ʾărammî, the Aramean)` |
| Μεσοποταμίας | Mesopotamias | Mesopotamia | `(Μεσοποταμία, Greek, "the land between the rivers", for Hebrew Paddan-ʾĂrām)` |
| Ησαυ | Ēsau | Esau | `(Ησαυ, from Hebrew ʿĒśāw, usually connected with śēʿār, "hair", the hairiness of 25:25)` |
| Ιακωβ | Iakōb | Jacob | `(Ιακωβ, from Hebrew Yaʿăqōb, which the Hebrew of 25:26 hears in ʿāqēb, "heel")` |
| Εδωμ | Edōm | Edom | `(Εδωμ, from Hebrew ʾĔdôm, which the Hebrew of 25:30 hears in ʾādōm, "red")` |

| Ἀδικία | Adikia | Injustice | `(Ἀδικία, the Greek word ἀδικία, "wrong-doing, injustice", printed as the well's name; the Hebrew is ʿĒśeq, "contention")` |
| Ἐχθρία | Echthria | Enmity | `(Ἐχθρία, the Greek word ἐχθρία, "hatred, enmity", printed as the well's name; the Hebrew is Śiṭnâ, "accusation")` |
| Εὐρυχωρία | Eurychōria | Room | `(Εὐρυχωρία, the Greek word εὐρυχωρία, "open space, free room", printed as the well's name; the Hebrew is Rĕḥōbôt, "broad places")` |
| Ὅρκος | Horkos | Oath | `(Ὅρκος, the Greek word ὅρκος, "the object by which one swears, oath", printed as the well's name; the Hebrew is Šibʿâ, "seven" or "oath")` |
| Ιουδιν | Ioudin | Judith | `(Ιουδιν, for Hebrew Yĕhûdît, "Jewess" or "woman of Judah")` |
| Βεηρ | Beēr | Beeri | `(Βεηρ, for Hebrew Bĕʾērî, usually connected with bĕʾēr, "well")` |
| Βασεμμαθ | Basemmath | Basemath | `(Βασεμμαθ, from Hebrew Bāśĕmat, usually connected with bōśem, "balsam, spice")` |
| Αιλων | Ailōn | Elon | `(Αιλων, from Hebrew ʾÊlōn, usually connected with ʾēlôn, "oak, terebinth")` |
| Ευαίου | Euaiou | Hivite | `(Ευαῖος, the man of the people the Hebrew calls Ḥiwwî, the Hivite)` |

| Συρίας | Syrias | Syria | `(Συρία, the Greek name of the land; the Hebrew here is Paddan-ʾĂrām)` |
| Μαελεθ | Maeleth | Mahalath | `(Μαελεθ, from Hebrew Māḥălat, of uncertain meaning)` |
| Οἶκος | Oikos | House | `(Οἶκος θεοῦ, "house of God", the Greek of Hebrew Bêt-ʾĒl, Bethel)` |
| Ουλαμλους | Oulamlous | Ulamlous | `(Ουλαμλους, for Hebrew Lûz, Luz, with ʾûlām, "but", read into the name)` |

| Ραχηλ | Rachēl | Rachel | `(Ραχηλ, from Hebrew Rāḥēl, "ewe")` |
| Λεια | Leia | Leah | `(Λεια, from Hebrew Lēʾâ, of uncertain meaning, perhaps "wild cow")` |
| Ζελφαν | Zelphan | Zilpah | `(Ζελφα, from Hebrew Zilpâ, of uncertain meaning)` |
| Βαλλαν | Ballan | Bilhah | `(Βαλλα, from Hebrew Bilhâ, of uncertain meaning)` |
| Ρουβην | Roubēn | Reuben | `(Ρουβην, from Hebrew Rĕʾûbēn, which the Hebrew of this verse hears in rāʾâ bĕʿonyî, "he has seen my affliction")` |
| Συμεων | Symeōn | Simeon | `(Συμεων, from Hebrew Šimʿôn, which the Hebrew of this verse hears in šāmaʿ, "he has heard")` |
| Λευι | Leui | Levi | `(Λευι, from Hebrew Lēwî, which the Hebrew of this verse hears in lāwâ, "he will be joined")` |
| Ιουδα | Iouda | Judah | `(Ιουδα, from Hebrew Yĕhûdâ, which the Hebrew of this verse hears in yādâ, "praise")` |

| Νεφθαλι | Nephthali | Naphtali | `(Νεφθαλι, from Hebrew Naptālî, which the Hebrew of this verse hears in niptaltî, "I have wrestled")` |
| Γαδ | Gad | Gad | `(Γαδ, from Hebrew Gād, "fortune", which the Greek keeps in ἐν τύχῃ)` |
| Ασηρ | Asēr | Asher | `(Ασηρ, from Hebrew ʾĀšēr, "happy", which the Greek keeps in μακαρία)` |
| Ισσαχαρ | Issachar | Issachar | `(Ισσαχαρ, from Hebrew Yiśśāḵār, which the Hebrew of this verse hears in śāḵār, "wage")` |
| Μισθός | Misthos | Wage | `(Μισθός, the Greek word for wage, which Rahlfs prints with a capital as the name's meaning)` |
| Ζαβουλων | Zaboulōn | Zebulun | `(Ζαβουλων, from Hebrew Zĕbûlûn, which the Hebrew of this verse hears in zābal, "honour, dwell with")` |
| Δινα | Dina | Dinah | `(Δινα, from Hebrew Dînâ, of uncertain meaning, from the root dîn, "judge")` |
| Ιωσηφ | Iōsēph | Joseph | `(Ιωσηφ, from Hebrew Yôsēp̄, which the Hebrew of this verse hears in yōsēp̄, "may he add", and in ʾāsap̄, "he has taken away")` |

| Γαλααδ | Galaad | Gilead | `(Γαλααδ, from Hebrew Gilʿād, which the Hebrew of 31:47 hears in gal ʿēd, "heap of witness")` |
| Σύρῳ | Syrō | Syrian | `(Σύρος again, in the dative)` |
| Βουνὸς | Bounos | Hill | `(Βουνός, "hill", the Greek of Hebrew Galʿēd and Yĕgar-śāhădûtā, the heap of witness of 31:47)` |
| Ἡ | Hē | The | `(Ἡ ὅρασις, "the vision", the Greek of Hebrew Miṣpâ, Mizpah, which the Hebrew hears in ṣāpâ, "he watched")` |

| Παρεμβολαί | Parembolai | Encampments | `(Παρεμβολαί, "encampments", the Greek of Hebrew Maḥănayim, the two camps)` |
| Ιορδάνην | Iordanēn | Jordan | `(Ἰορδάνης, from Hebrew Yardēn, which the Hebrew connects with yārad, "go down")` |
| Ιαβοκ | Iabok | Jabbok | `(Ιαβοκ, from Hebrew Yabbōq, which the Hebrew of this verse hears in the wrestling, yēʾābēq)` |
| Ισραηλ | Israēl | Israel | `(Ισραηλ, from Hebrew Yiśrāʾēl, which the Hebrew of this verse hears in śārâ ʿim ʾĕlōhîm, "he strove with God")` |
| Εἶδος | Eidos | Form | `(Εἶδος θεοῦ, "form of God", the Greek of Hebrew Pĕnîʾēl, Peniel, the face of God)` |

| Σκηνάς | Skēnas | Tents | `(Σκηναί, "tents", the Greek of Hebrew Sukkôt, Succoth, the booths)` |
| Σικιμων | Sikimōn | Shechem | `(Σικιμα, from Hebrew Šĕkem, "shoulder")` |
| Εμμωρ | Emmōr | Hamor | `(Εμμωρ, from Hebrew Ḥămôr, "ass")` |

| Χορραῖος | Chorraios | Horite | `(Χορραῖος, from Hebrew Ḥōrî, usually connected with ḥōr, "hole, cave")` |
| Χαναναίοις | Chananaiois | Canaanites | `(Χαναναῖος, from Hebrew Kĕnaʿănî, the people of Kĕnaʿan, Canaan)` |
| Φερεζαίοις | Pherezaiois | Perizzites | `(Φερεζαῖος, from Hebrew Pĕrizzî, usually connected with pĕrāzî, "villager, dweller in open country")` |

| Λουζα | Louza | Luz | `(Λουζα, from Hebrew Lûz, usually connected with lûz, "almond tree")` |
| Δεββωρα | Debbōra | Deborah | `(Δεββωρα, from Hebrew Dĕbôrâ, "bee")` |
| Βάλανος | Balanos | Acorn | `(Βάλανος πένθους, "acorn of mourning", the Greek of Hebrew ʾAllôn-bākût, the oak of weeping)` |
| Γαδερ | Gader | Eder | `(Γαδερ, from Hebrew ʿĒder, "flock")` |
| χαβραθα | chabratha | chabratha | `(χαβραθα, the Hebrew kibrat left untranslated, a stretch of ground of unknown length)` |
| Εφραθα | Ephratha | Ephrath | `(Εφραθα, from Hebrew ʾEprātâ, usually connected with pārâ, "to be fruitful")` |
| Υἱὸς | Hyios | Son | `(Υἱὸς ὀδύνης μου, "son of my pain", the Greek of Hebrew Ben-ʾÔnî)` |
| Βενιαμιν | Beniamin | Benjamin | `(Βενιαμιν, from Hebrew Binyāmîn, "son of the right hand" or "son of the south")` |
| Βηθλεεμ | Bēthleem | Bethlehem | `(Βηθλεεμ, from Hebrew Bêt-Leḥem, "house of bread")` |
| Βαλλας | Ballas | Bilhah | `(Βαλλα, from Hebrew Bilhâ, usually connected with bāhal, "to be troubled")` |
| Ιουδας | Ioudas | Judah | `(Ιουδας, from Hebrew Yĕhûdâ, which the Hebrew of 29:35 hears in yādâ, "to praise")` |
<!-- name rows above -->

Σύγχυσις translates the name where 10:10 gave the city its Greek name, Βαβυλών; as with Ζωή at
3:20, the anchored form is the English of the name the Greek prints, *Confusion*. Αρραν the man
(*Hārān*) and Χαρραν the city (*Ḥārān*) are both *Haran* in English, and two names in Greek.

A name glossed again in a later chapter keeps its gloss, unless the gloss spoke of the verse it
stood in: Σηθ's *which the verse ties* becomes *which 4:25 ties*. Μαθουσαλα at GEN 5 is glossed
for Mĕtûšelaḥ himself, where 4:18 gave the Greek name to Mĕtûšāʾēl.

Where the Greek and the English Bible name the same person with one name, differently spelled,
the anchored form is the English Bible's: Ενως is *Enosh*, Καιναν *Kenan*. Luke 3:36–38 spells
Καιναν and Ιαρεδ Καϊνάμ and Ἰάρετ; for that reason their dictionary forms are the forms Rahlfs
prints, not MorphGNT's (see the second-pass brief).

The anchored form is the English form of the name the *Greek* prints, which is not always the
English Bible's name for the person. Μαθουσαλα at GEN 4:18 is *Methuselah*, though the Hebrew
there names Cain's descendant Methushael; Θοβελ at 4:22 is *Tubal*, though the Hebrew has
Tubal-cain. The gloss records the Hebrew, and the note flags the difference.

A name that appears twice in the verse that glosses it (Αβελ at GEN 4:2) prints its gloss the
first time only.

Ζωή at GEN 3:20 translates the Hebrew name instead of transliterating it, and Rahlfs
capitalises it as a name; so the anchored form is the English form of *that* name, *Zoe*, not
*Eve*, which comes from the Hebrew. χερουβιμ is printed in lower case, and
stays lower case in both panels; its `names` entry is what makes it a name to the checks.

Rahlfs prints the Semitic names bare — Εδεμ, Φισων, Ευιλατ, Γηων — with no accent or
breathing, and the Greek-formed ones accented: Αἰθιοπίας, Ἀσσυρίων, Εὐφράτης, Τίγρις. The
transcription keeps that distinction, and it is itself evidence of which names the
translators felt to be Greek words.

Written `[[name:Ἰωάννης]]` in `reading`; the renderer picks the form by panel.

Every occurrence is written that way, including the ones after the first. The first carries
the entry above; each later one carries the same entry with `"bare": true` and no `gloss`,
so the form prints alone. Genesis 2 needs this from the start — Εδεμ stands in 2:8 and again
in 2:10, and Αδαμ runs through 2:16–23.

---

## What `build/validate.py` enforces from this file

- a headword never stands bare, as plain text outside its unit
- no em dash inside a chain
- `BANNED_PHRASES` — seeded with `face of the waters` and `face of the deep` (GEN 1:2)

- every unit names a Greek word its own verse holds — checked against the chapter's
  morphology, so a unit cannot claim a word that is not there
- one word in one form reads one way: of two units sharing a lemma and a headword, neither
  says less than the other. What the form put there — auxiliaries, the case prepositions,
  the concord pronouns, and the project's own wording for verbal aspect — is set aside
  before they are compared, so a perfect participle and an aorist one may share a headword
- one case is one chain: a preposition has one form, so its chain cannot follow the
  form. Within one lemma and one case it reads the same everywhere.

It does not yet check that a headword matches its recorded lexicon sense, or that a recurring
chain matches its entry here. Both are still enforced by reading this file first.

---

## The lemma in the data

Each unit carries the Greek word it opens, as a third field. It is never printed.

Before it was recorded, the chain check had to work out which word a unit rendered by
looking the unit up in the table above — so it saw 3,480 of the corpus's 9,972 units and
was blind to the rest. That is the wrong two-thirds: a chain that has drifted is by
definition a chain this file does not declare. With the lemma recorded the check reads
every unit, and the first full pass found 16 drifted groups and 103 units naming a word
their verse does not hold.

Most of those 103 named a near neighbour of the right word and only the lemma was wrong —
καθά for καθάπερ, ἕνεκα for εἵνεκα, ἄρα for ἆρα, ἀποκρίνω for ἀποκρίνομαι. The rest
carried another word's chain outright, and the reading said what the Greek does not:

| ref | read | the word there | now reads |
| --- | --- | --- | --- |
| GEN 31:23, 31:25 | `took down` | κατέλαβεν, καταλαμβάνω | `seized upon` |
| GEN 27:33 | `having carried out of` | εἰσήνεγκεν, εἰσφέρω | `having carried into` |
| GEN 34:3 | `loved` (φιλέω) | ἠγάπησεν, ἀγαπάω | `treated with affection` |
| GEN 34:12 | `the maid` (παρθένος) | τὴν παῖδα, παῖς | `the child` |
| GEN 30:11 | `named` (ὀνομαστός) | ἐπωνόμασεν, ἐπονομάζω | `gave a surname and named` |
| GEN 26:12 and 10 more | `that` (ἵνα) | ἐκείνῃ, ἐκεῖνος | `that, the one there, the more remote` |
| GEN 27:11 and 6 more | `man` (ἄνθρωπος) | ἀνήρ | `a man, a man in the prime of life` |
| GEN 28:19 / 29:26 / 32:4 | `before` (πρό) | πρότερος / πρίν / ἔμπροσθεν | each its own |

### Prepositions carry their case

Middle Liddell gives each case its own section, and CLAUDE.md takes a preposition's sense
from the case it governs, so μετά with a genitive and μετά with an accusative are two
entries and not one chain that drifted. The unit names the case: `μετά + genitive`.
Recording it found four διά units and one περί unit carrying the other case's chain.
GEN 24:11 is the one place with no case to read: τὸ πρὸς ὀψέ, *toward evening*, governs an
adverb, and the neuter article makes it the accusative section's time expression.


### Words new in GEN 36

- The chapter is a genealogy, and the genealogies read as GEN 10 and GEN 25 read: the frame of
  the list — *sons of*, *daughters of*, *sister*, *father* — stands as plain text, and only the
  words that are not kinship terms are opened. υἱός, θυγάτηρ, ἀδελφή and the numerals are
  unopened across the whole corpus; whether they should be is an open question, not a decision
  taken here.
- ἡγεμών — the chapter's own word, thirty-two times in the singular and nine in the plural. It
  renders the Hebrew ʾallûp, the head of a clan. Middle Liddell's first sense is *one who
  leads*, so that heads it; *commanders*, a repeat, and *Emperor* are left out.
- `ἡγεμὼν Θαιμαν` is apposition, not a genitive: the names of 15-18 are the sons named in
  11-14, so each is *chief Teman*, the man in his office. Where the plural ἡγεμόνες governs a
  name it is a genitive, and 18's Ελιβεμας shows the ending. The two independent passes at the
  morphology disagreed here, and the text settled it.
- νέμω — one occurrence, and the widest entry in the chapter: thirty-one translations running
  from dealing out a portion to pasturing a flock. Four are citation fragments and are filed in
  NOT_SENSES.
- βασιλεύω — the king-list of 31-39 uses it eight times as an aorist, once as a participle and
  once as an infinitive. Middle Liddell's first sense is *to be king*, so the aorist reads *was
  king*; the entry's own *to have become king* is the ingressive the aorist usually carries,
  and it stands inside the chain.
- κατοικοδομέω — found nowhere else in Genesis. Its second translation is the bare preposition
  *in*, a fragment of *to build upon or in*, and is filed in NOT_SENSES.
- ἡγεμονία — likewise, *hegemony.* repeats the sense above it and *imperium* is the Latin; both
  are filed.
- Αδας and Ωνας — two names the chapter declines, where the names check reads an inflected form
  as the same name only when the stem is long enough. Αδα is three letters and Ωναν ends
  otherwise, so each declined form carries its own gloss, and the gloss says whose it is.
- Θαμνα stands three ways: Eliphaz's concubine at 12, Lotan's sister at 22, and a clan at 40.
  The morphology reads the clan as masculine, with ἡγεμών, and the woman as feminine.
- Χαρραν at 26 is Hebrew Kĕrān, not the Ḥārān this same Greek form renders from 11:31; Βαραδ at
  35 is Bĕdad, not the Bered of 16:14; Αραμ at 28 is ʾĂrān, not the ʾĂrām of 10:22. Three Greek
  forms doing double duty, each recorded on its morphology line.
- Ezer's sons are four in the Greek where the Hebrew has three; Ιωυκαμ answers to nothing in
  the Hebrew line. Flagged `divergence` at 27.

| lemma | headword | chain | used |
| --- | --- | --- | --- |
| βασιλεύω | `the ones having been king` | `the ones having been king, the ones having ruled, the ones having reigned, the ones having been queen, the ones having been king of, the ones having been governed by a king, the ones having been master of` | 36:31 |
| βασιλεύω | `to be king` | `to be king, to rule, to reign, to be queen, to be king of, to be governed by a king, to be master of` | 36:31 |
| βασιλεύω | `was king` | `was king, ruled, reigned, was queen, was king of, was governed by a king, was master of` | 36:32 |
| γυνή | `of woman` | `of woman, of mistress and lady, of wife and spouse, of mortal woman` | 36:10 |
| δύναμαι | `was being able` | `was being able and capable and strong enough, was powerful and mighty, was having influence, was daring and bearing, was passing for, was worth, was equivalent to, was signifying and meaning, was availing` | 36:7 |
| κατοικέω | `of the one dwelling in` | `of the one dwelling in, of the one settling in, of the one colonising, of the one inhabiting, of the one settling and dwelling, of the one lying and situate` | 36:20 |
| κατοικοδομέω | `in the ones having been built upon` | `within, inside of, and by means of the ones having been built upon and standing so, the ones having been built away, the ones having been squandered in building` | 36:43 |
| κτῆσις | `of the acquisition` | `of the acquisition, of the possession, of the possessions and property` | 36:43 |
| νέμω | `was dealing out` | `was dealing out and distributing and dispensing, was having as his portion and possessing and enjoying, was dwelling in and inhabiting, was spending and passing, was holding and possessing, was holding sway and managing, was supporting, was using, was holding and considering as, was pasturing, was driving to pasture and tending, was feeding, was consuming and devouring, was giving` | 36:24 |
| παλλακή | `a concubine` | `a concubine and mistress` | 36:12 |
| περιποιέομαι | `kept for himself` | `kept for himself, saved for himself, compassed and acquired and obtained, made gain` | 36:6 |
| φέρω | `to bring` | `to bring, to bear, to carry, to endure` | 36:7 |
| ἐκκόπτω | `the one having cut out` | `the one having cut out and knocked out, the one having felled and cut down all the trees, the one having cut off and made an end of, the one having beaten off and repulsed` | 36:35 |
| ἡγεμονία | `in the leadings of the way` | `within, inside of, and by means of the leadings of the way and goings first, the chief commands, the authorities, the hegemonies, the sovereignties of one state over a number of subordinates, the divisions of the army and commands` | 36:30 |
| ἡγεμών | `ones who lead` | `ones who lead, guides, ones who are an authority, leaders and commanders and chiefs, chiefs and sovereigns, provincial governors` | 36:15 |
| ἡγεμών | `one who leads` | `one who leads, a guide, one who is an authority, a leader and commander and chief, a chief and sovereign, a provincial governor` | 36:15 |
| ἡγεμών | `of the ones who lead` | `of the ones who lead, of the guides, of the ones who are an authority, of the leaders and commanders and chiefs, of the chiefs and sovereigns, of the provincial governors` | 36:40 |
| ὑπάρχω | `of the existing circumstances` | `of the existing circumstances and present advantages, of what belongs to one and the possessions and means` | 36:7 |
| ὑποζύγιον | `the beasts for the yoke` | `the beasts for the yoke and beasts of burden` | 36:24 |


## The one-sense rule, and the last words it left shut

A word is a unit exactly when its entry says more than its headword does — both ways, so
that neither half can happen by accident. 1,038 content words of Genesis had been standing
as plain text; 933 of them turned out to be right, because their entry says no more than the
headword already carries, and the rest are opened here. `build/validate.py` holds both halves
now, against the chapter's own word-by-word layer.

More is not the same as a second numbered sense. κιβωτός has one sense and still wants a
unit, because that sense reads *a wooden box, chest, coffer* and the headword keeps only the
box. Going the other way, 85 units whose chain was word for word their headword became plain
text, πρωτότοκος among them — its entry is *first-born* and nothing else, so the unit printed
`of the first-born — of the first-born —`. Four kept their units although their chains repeat:
`made swear`, `made of the wood of the tree`, `drew into themselves` and `the he-goats` each
hold another unit's headword inside them, and the unit is what tells the two apart.

A rule could not finish the last of them. Each turned on something only the verse shows — so
these were settled one at a time, against the verse.

- **The case a unit wears is the one the prose around it already wears**, because the unit
  replaces that prose and nothing else. Where a preposition governs the word, the preposition
  carries the relation and the noun does not repeat it: GEN 1:2 already reads ἐπάνω τῆς
  ἀβύσσου as *above the great deep*, so ἐπάνω τοῦ ὕδατος reads *above the water*.
- **An ordinal takes the shape of the noun it agrees with, in its own verse.** ἡμέρα is
  rendered six ways across the corpus — *day*, *the day*, *to the day*, *in the day*, *of
  day*, *in day* — and an ordinal built from its own case instead produced *the day the to
  the third*. Until ἡμέρα is settled, concord is what keeps a phrase readable.
- **ἐπάνω** had never been opened at all: six tokens reading *upon, over, and atop* or
  *over and atop*, which is composed English, not Middle Liddell's.
- **GEN 7:16** carried a unit whose chain is εἰσπορεύομαι's entry but whose lemma said
  εἰσέρχομαι — which the verse also holds, in its own unit, so the check that a unit names a
  word its verse holds could not see it. That check does not count.
- **GEN 31:40** read *from the of eyes of me*; **GEN 29:17** had the article stranded before
  a postpositive δέ, where it could not join its noun; **GEN 33:2** had πρότερος's English
  filed under πρῶτος, the same fault as GEN 32:18.

Curated out of the lexicon, for reasons already established elsewhere in this file:

- τριώροφος *of three stories or floors* and ἐπάνω's *on the upper side or part* are one
  gloss each; splitting on the *or* makes a second sense out of half a phrase. τριώροφος has
  no other sense, so it is a one-sense word and stays plain text — which is what GEN 6:16's
  own note already said.
- ὑπεναντίος: *opposite or contrary to* split the same way; τὸ and τὰ ὑπεναντίον are the
  neuter substantive and -ίως is the adverb, so none of the three is a sense οἱ ὑπεναντίοι
  can wear — as κατὰ μῆνα was not a sense of μήν.
- οὖς's *auris, the ear* is the Latin with the English after it, and *the ear* stands on its
  own as the next sense. πλάτανος's *broad leaves* is why the tree has the name.

| γεύω | `give a taste of` | `give a taste of, taste of, taste and feel, taste the sweets of, have experience of` | 25:30 |
| γόνυ | `of the knees` | `of the knees, of the laps, of the joints` | 30:3 |
| δεκάτη | `a tenth` | `a tenth, a tenth part and tithe, a tenth day` | 28:22 |
| δεκάτη | `tenth part` | `tenth part and tithe, tenth day, tenth` | 14:20 |
| εἰσπορεύομαι | `of the ones going into` | `of the ones going into and entering` | 23:10 |
| εἰσπορεύομαι | `the ones going into` | `the ones going into, the ones entering` | 7:16 |
| εἰσπορεύομαι | `were going into` | `were going into and entering` | 6:4 |
| εὐοδόω | `has helped on the way` | `has helped on the way and it stands helped on the way, has had a prosperous journey, has prospered and been successful` | 24:21 |
| εὐοδόω | `help on the way` | `help on the way, have a prosperous journey, prosper and be successful` | 24:12 |
| εὐοδόω | `helped on the way` | `helped on the way, had a prosperous journey, prospered and was successful` | 24:48 |
| εὐοδόω | `will help on the way` | `will help on the way, will have a prosperous journey, will prosper and be successful` | 24:40 |
| εὐοδόω | `you help on the way` | `you help on the way, you have a prosperous journey, you prosper and are successful` | 24:42 |
| καταβιάζομαι | `was constraining` | `was constraining, was being forced` | 19:3 |
| λαός | `a people` | `a people, men, soldiers, a land-army, the common men, folk, Jews, Christians` | 25:23 |
| λαός | `of a people` | `of a people, of men, of soldiers, of a land-army, of the common men, of folk, of Jews, of Christians` | 25:23 |
| λαός | `of the people` | `of the people, of the men, of the soldiers, of the land-army, of the common men, of the folk, of the Jews, of the Christians` | 23:12 |
| λαός | `peoples` | `peoples, men, soldiers, land-armies, common men, folk, Jews, Christians` | 25:23 |
| λαός | `the people` | `the people, the men, the soldiers, the land-army, the common men, the folk, the Jews, the Christians` | 14:16 |
| λαός | `to the people` | `to the people, to the men, to the soldiers, to the land-army, to the common men, to the folk, to the Jews, to the Christians` | 23:7 |
| μηρός | `the thigh` | `the thigh, the leg-bones` | 24:2 |
| μηρός | `to the thigh` | `to the thigh, to the leg-bones` | 32:32 |
| ξηρός | `of the dry` | `of the dry, of the withered and lean and haggard, of the dry land, of the aground` | 7:22 |
| οὖς | `in the ears` | `within, inside of, and by means of the ears, the handles` | 35:4 |
| οὖς | `the ears` | `the ears, the handles` | 20:8 |
| περίοικος | `of the dwelling round` | `of the dwelling round, of the neighbours, of the free inhabitants` | 19:29 |
| περίοικος | `the dwelling round` | `the dwelling round, the neighbours, the free inhabitants` | 19:25 |
| πρῶτος | `in foremost` | `within, inside of, and by means of foremost, first` | 33:2 |
| πρῶτος | `of the foremost` | `of the foremost, of the first` | 8:13 |
| πρῶτος | `to the foremost` | `to the foremost, to the first` | 8:5 |
| πυρράκης | `red` | `red and ruddy` | 25:25 |
| συναπόλλυμι | `you may be destroyed together` | `you may be destroyed together, you may be lost, you may perish together` | 19:15 |
| συναπόλλυμι | `you may destroy together` | `you may destroy together, you may lose` | 18:23 |
| τέκνον | `that which is borne` | `that which is borne, the born, a child, my son and my child, the young` | 17:16 |
| τέκνον | `things borne` | `things borne, the born, children, the young` | 3:16 |
| τέκνον | `to the things borne` | `to the things borne, to the born, to children, to the young` | 31:16 |
| τεκνοποιέω | `I will bear children` | `I will bear children, I will beget them, I will breed children` | 30:3 |
| τεκνοποιέω | `was bearing children` | `was bearing children, was begetting them, was breeding children` | 11:30 |
| τεκνοποιέω | `you may bear children` | `you may bear children, you may beget them, you may breed children` | 16:2 |
| τερέμινθος | `of the terebinth` | `of the terebinth, of the turpentine tree` | 14:6 |
| τερέμινθος | `the terebinth` | `the terebinth, the turpentine tree` | 35:4 |
| τρίτος | `the third` | `the third, the third and finishing, the day after to-morrow, the day before, the thirdly, the sacrifice to the dead offered the third day after the funeral, the third part` | 2:14 |
| τρίτος | `third` | `third, third and finishing, day after to-morrow, day before, thirdly, a sacrifice to the dead offered the third day after the funeral, a third part` | 31:2 |
| τρίτος | `to the third` | `to the third, to the third and finishing, to the day after to-morrow, to the day before, to the thirdly, to the sacrifice to the dead offered the third day after the funeral, to the third part` | 22:4 |
| φρέαρ | `a well` | `a well, a tank and cistern and reservoir, an oil jar` | 21:19 |
| φρέαρ | `in the well` | `within, inside of, and by means of the well, the tank and cistern and reservoir, the oil jar` | 21:32 |
| φρέαρ | `of the well` | `of the well, of the tank and cistern and reservoir, of the oil jar` | 26:20 |
| φρέαρ | `of the wells` | `of the wells, of the tanks and cisterns and reservoirs, of the oil jars` | 21:25 |
| φρέαρ | `the well` | `the well, the tank and cistern and reservoir, the oil jar` | 16:14 |
| φρέαρ | `the wells` | `the wells, the tanks and cisterns and reservoirs, the oil jars` | 26:15 |
| φρέαρ | `to the well` | `to the well, to the tank and cistern and reservoir, to the oil jar` | 21:33 |
| φρέαρ | `wells` | `wells, tanks and cisterns and reservoirs, oil jars` | 14:10 |
| ἀδελφός | `of son of the same mother` | `of a son of the same mother, of a brother, of a near kinsman` | 9:5 |
| ἀδελφός | `of the son of the same mother` | `of the son of the same mother, of the brother, of the near kinsman` | 4:9 |
| ἀδελφός | `of the sons of the same mother` | `of the sons of the same mother, of the brothers, of the near kinsmen` | 16:12 |
| ἀδελφός | `son of the same mother` | `a son of the same mother, a brother, a near kinsman` | 20:5 |
| ἀδελφός | `son of the same mother` | `son of the same mother, brother, near kinsman` | 33:9 |
| ἀδελφός | `sons of the same mother` | `sons of the same mother, brothers, near kinsmen` | 13:8 |
| ἀδελφός | `the son of the same mother` | `the son of the same mother, the brother, the near kinsman` | 4:2 |
| ἀδελφός | `the sons of the same mother` | `the sons of the same mother, the brothers, the near kinsmen` | 24:55 |
| ἀδελφός | `to son of the same mother` | `to a son of the same mother, to a brother, to a near kinsman` | 10:21 |
| ἀδελφός | `to sons of the same mother` | `to sons of the same mother, to brothers, to near kinsmen` | 9:22 |
| ἀδελφός | `to the son of the same mother` | `to the son of the same mother, to the brother, to the near kinsman` | 4:21 |
| ἀδελφός | `to the sons of the same mother` | `to the sons of the same mother, to the brothers, to the near kinsmen` | 9:25 |
| ἀληθεύω | `speak truth` | `speak truth, come true` | 20:16 |
| ἄζυμος | `unleavened` | `unleavened, the feast of unleavened bread` | 19:3 |
| ἐξαποστέλλω | `I sent quite away` | `I sent quite away, I dispatched` | 31:27 |
| ἐξαποστέλλω | `sent quite away` | `sent quite away, dispatched` | 3:23 |
| ἐξαποστέλλω | `we sent quite away` | `we sent quite away, we dispatched` | 26:29 |
| ἐξαποστέλλω | `you sent quite away` | `you sent quite away, you dispatched` | 31:42 |
| ἐπάνω | `above` | `above and atop and on the upper side, above, above and more than` | 1:2 |
| ἐπιδιαιρέω | `divided anew` | `divided anew, distributed among themselves` | 33:1 |
| ἕβδομος | `seventh` | `seventh, a seventh day` | 7:11 |
| ἕβδομος | `the seventh` | `the seventh, the seventh day` | 2:2 |
| ἕβδομος | `the sevenths` | `the sevenths, the seventh days` | 29:27 |
| ὀφθαλμός | `of the eyes` | `of the eyes, of the dearest and best, of the comfort, of the buds` | 31:40 |
| ὀφθαλμός | `the eyes` | `the eyes, the dearest and best, the comfort, the buds` | 3:5 |
| ὀφθαλμός | `to the eyes` | `to the eyes, to the dearest and best, to the comfort, to the buds` | 3:6 |
| ὀφθαλμός | `with the eyes` | `with the eyes, with the dearest and best, with the comfort, with the buds` | 13:14 |
| ὑπεναντίος | `of the ones set over against and meeting` | `of the ones set over against and meeting, of the ones set against and opposite, of the enemies, of the ones opposed and opposite, of the ones contrary to` | 22:17 |
| ὕδωρ | `of the water` | `of the water, of the waters, of the rain-water and rain, of the water of the water-clock` | 9:11 |
| ὕδωρ | `of water` | `of water, of waters, of rain-water and rain, of water of a water-clock` | 7:6 |
| ὕδωρ | `the water` | `the water, the waters, the rain-water and rain, the water of the water-clock` | 1:2 |
| ὕδωρ | `water` | `water, waters, rain-water and rain, water of a water-clock` | 6:17 |


## The particles, opened by their parse

The project already picks a sense by part of speech — the first sense for the case a
preposition governs, the first noun sense for a word used as a noun. A particle follows the
same line. καί parsed as an adverb takes the adverbial senses and becomes a unit; καί parsed
as the connective is the conjunction and stays plain text. μή, γάρ, εἰ and τε are opened
outright. οὐ is not: its entry gives one sense, *not*, so by the one-sense rule it is plain
text, and 125 tokens were already right.

Middle Liddell writes most of a particle's entry as prose about how the word works, and the
scraper takes a `<tr>` wherever it finds one. So the labels of a construction come through
beside the translations — μή's *fear* and *apprehension* are the verbs it follows, γάρ's
*a question* and *a wish* are the constructions it stands in — and so do the sentences
illustrating them, rendered: *surely he is dead, is he not?*, *if he was doing*. Only the
translations are senses; the rest is in `NOT_SENSES` with its reason.

Two headwords collide, and that is a fact about English, not a fault. μή and οὐ both give
*not*; τε and καί both give *and*. So a plain `not` in a verse whose μή is a unit is not a
headword left loose — it is οὐ, printing its own first sense. `check_anchors` reads the
chapter's word-by-word layer and lets a word print the English it is entitled to.

**εἰ, and a translation the markup loses.** Perseus encodes the entry as *a Conditional
Conjunction, Lat.* `<foreign lang="la">si, if</foreign>` *; and in indirect questions,*
`<tr>whether.</tr>` — so the English *if* sits inside the Latin element and never reaches a
translation. Left as encoded, εἰ heads as *whether* and the conditional, which is what εἰ is
in every one of its Genesis occurrences, is nowhere in the chain. `MARKUP_LOST` in
`build/words.py` restores it at the front, quoting the entry and naming the element that took
it. It adds nothing Middle Liddell does not say.

**νῦν read νῦν δή's entry.** The lexicon files eighteen entries under `nu=n`, and the bare
key takes whichever stands first in the file: `nu=n2`, νῦν δή, *just now*. Thirty-four units
carried *now, even now, just now* — νῦν δή's range, not νῦν's. `ENTRY` now names `nu=n1`, and
everything after *besides the sense of Time, the enclit. νυν, νυ denotes immediate sequence*
is the enclitic νυν, a different word, curated out as κατὰ μῆνα was from μήν.

Counting units against words found two more of the same kind: GEN 24:14's second *that* was
filed under ἵνα where the verse's second conjunction is ὅτι, and GEN 32:29's second *but*
under δέ where it is ἀλλά. Each named a word the verse does hold, in a unit of its own, so
asking only whether a word is there could see nothing.

| γάρ | `for` | `for, since and as, for otherwise and else, now, but, why and what, would that` | 2:5 |
| εἰ | `if` | `if, whether, come on` | 4:14 |
| καί | `also` | `also and even, but, nay, and yet, as, likewise` | 3:6 |
| μή | `not` | `not, that not, perhaps, surely not and you don't mean to say that` | 3:1 |
| νῦν | `now at this very time` | `now at this very time, now, of the present, the present time, just now and but now, as it is and as the case now stands, in this case` | 2:23 |
| τε | `and` | `and, both and, and also` | 2:25 |
| ἀλλά | `otherwise` | `otherwise, but, except, yet, but then and however, but really and certainly` | 15:4 |
| ὅτι | `that` | `that, seeing that, although, for that, because, inasmuch as` | 2:3 |


## A noun marks its own case

The genitive reads `of`, the dative `to`, everywhere and whatever governs the word. The
corpus had done it both ways: γῆ under a preposition read `of the earth` twenty-eight times
and `the earth` six, and ὀφθαλμός's dative read `with the eyes` where the dative is
instrumental beside `to the eyes` where it is not — which is the *use* deciding the English,
and the use is context. One marker for one case is the only rule a check can hold without
deciding what governs what. 731 units already had it; 71 did not, and have it now.

Where a preposition merges into its object's unit the preposition keeps the lead, because
`within, inside of, and by means of the well` is ἐν's own English and not a case-marker.
Everywhere else the preposition carries its own sense and the noun still shows its form, so
GEN 1:2 reads `above — above and atop and on the upper side … — of the water`, and GEN 2:7
`from of the earth`. Awkward, and the form is visible, which is the trade this project makes
everywhere else.

`to day` for a bare dative ἡμέρᾳ is the one reading worth flagging: it is a hair from
`to-day`, which is how σήμερον reads. The hyphen is the only thing between them.

**Still open.** 150 units have their article written as plain text beside them rather than
inside them — `the` standing loose before `[[to house|…]]`, where τῷ οἴκῳ has the article
and the unit should carry it. Thirteen of those are ὁ δέ, where the article is a pronoun and
the prose is right; the rest are not. Three that this pass made conspicuous, by putting a
marker next to the loose article, are folded in here. The other ~134 want a pass of their own.
## Translations Perseus's markup swallows

Middle Liddell gives its Latin equivalent and its English together — *Lat. bos (bov-is), a
bullock, bull, ox, or a cow* — and Perseus wraps the whole run, English and all, in one
`<foreign lang="la">`. The loader reads translations from `<tr>` elements, so none of that
run reaches the senses. The printed page says it; the encoding hides it.

εἰ showed it first: *a Conditional Conjunction, Lat.* `si, if` *; and in indirect questions,*
`<tr>whether.</tr>`. Looking for the same shape — a comma inside a first-sense Latin element —
found **54 sites**, of which **24 words had lost a translation** and **seven had lost their
own first sense**, so the headword had been coming from somewhere further down the entry:

| word | the entry reads | the headword had been |
| --- | --- | --- |
| βοῦς | `Lat. bos (bov-is), a bullock, bull, ox, or a cow` | `cow` |
| κρίνω | `Lat. cerno, to separate, part, put asunder, distinguish` | `to pick out, choose` |
| ὦμος | `Lat. humerus, the shoulder with the upper arm` | `ulna` — the Latin for the forearm |
| δή | `Lat. jam) now, in truth, indeed, surely, really` | `exactness`, from "used to give greater exactness" |
| μήτρα | `Lat. matrix, the womb` | nothing: the entry resolved empty |
| τρεῖς | `Lat. tres, tria, three` | nothing |
| ὀκτώ | `Lat. octo, eight` | nothing |

`MARKUP_LOST` in `build/words.py` restores each one at the position the entry gives it,
quoting the entry and naming the element that took it. That adds nothing Middle Liddell does
not say. `LATIN_ONLY` records the sites where the run is Latin throughout, or where the
English beside it is a `<tr>` of its own and already in the senses.

**The reading was in better shape than the machinery.** Of 97 units on the affected words,
**73 already carried the sense** — whoever wrote them read the entry's text, where the
English is plainly there, and only the senses the loader could see were wrong. μνημεῖον's
chain had read `memorials, remembrances, records, tombs and monuments` for a long time
against an entry that resolved to `a monument` alone. 24 units had taken the sense below the
one they wanted, and are re-read here.

No check in the data could have caught it: a chain that is right is right. So
`check_markup` reads the lexicon instead, and every site must be settled in one table or the
other — a new chapter bringing a new word with the same shape fails the run until somebody
looks. It found nine of the fifty-four on its own, all of them words that print as plain text,
where only the card was wrong and no chain existed to be right.

**Two the recovery takes something from, left as they are for now.** μήτρα's entry resolved
empty, so `words.py` fell through to LSJ, and its chain is LSJ's fuller range — *the womb, the
cervix including the orifice of the womb, the matrix, the source and origin*. Middle Liddell
now gives one sense, `the womb`, and the rule is that LSJ serves only where Middle Liddell has
no entry, which would make μήτρα a one-sense word printing as plain text. ὦμος is the same
shape: its chain's second gloss, `the shoulder`, has no basis in the entry now that the first
reads in full. Both are rule-interaction questions rather than facts, and neither is changed
here.
## The article inside its word's unit

150 units had their article written as a plain `the` standing in front of them. The panel
then shows a word bare that belongs in a chain, and the unit's own chain reads as though the
Greek were anarthrous — `the [[to house|to house, …|οἶκος]]` prints *the to house*, where
τῷ οἴκῳ has one article and the unit should carry it. Marking the cases had made three of
them conspicuous; these are the rest.

**140 folded in.** A noun or an adjective takes `the X`, and a possessive gloss keeps it:
τὸ σόν is *the thy*, as every Greek article keeps its *the*. A participle takes it the way the
corpus already writes one — `the one coming`, `the ones having gone in`, and `of the one
having come into being` where the article is genitive. An articular infinitive becomes a
gerund, which is how ἐν τῷ ἐκτρῖψαι already read *in the rubbing out*: τῷ ἀποδιδράσκειν is
*the running away*, τὸ σῴζεσθαι *the being saved*.

Which occurrence of a word a unit opens is read off its position: the reading follows the
Greek word for word, so the nth unit naming a word answers to the nth one in the Greek. That
settled 39 that a count alone could not, GEN 31:13's `the [[God|…]]` among them, where θεός
stands twice and only the first is articular.

**45 left as they are, and rightly.** Where the article governs a phrase instead of a word
there is no one unit to put it in: τὰ ἐπὶ τῆς γῆς, τὰ ὀπίσω, τὰ νῦν, and ὁ δέ, where ὁ is the
pronoun subject and the prose reads *the, but, … he said*. 27 are that last kind.

**Still open.** 18 of those 45 are the article substantivizing a preposition's phrase or an
adverb, and they read *the upon of the earth*, *into the backwards*. English wants *the ones
upon the earth*, *into the things behind* — and `one` is already how the article's English is
written in front of a participle, so the same word would serve. Whether the substantivizing
article may print `the ones` or `the things` as plain text is a convention to settle, not a
fact, and nothing here assumes it.
## Middle Liddell first

Middle Liddell is the lexicon. LSJ answers only where Middle Liddell has no entry for the
word under its own key or a close form of it — and where Middle Liddell gives less than LSJ,
Middle Liddell is still the reading. Both are CC BY-SA, so licensing draws no line between
them.

The LSJ table had been winning outright: a word in it was read from LSJ even where Middle
Liddell had it. Of its 83 words, **15 now read Middle Liddell** and 68 stay.

**Six Middle Liddell had under their own key**, with the translation hidden by the markup and
now recovered by `MARKUP_LOST`: τρεῖς, ὀκτώ, μνημεῖον, ὀστέον, μήτρα, ὦμος.

**Nine it files under a close form**, now named in `SPELLING` or `FILED_WITHIN`:

| word | where Middle Liddell has it | what it gives |
| --- | --- | --- |
| ποιμήν | `poimh/` — the key truncated | a herdsman, shepherd, a captain, chief |
| κατανύσσω | κατανύσσομαι, the passive the text uses | to be sorely pricked, to be stupefied, to slumber |
| χείμαρρος | χειμάρρους, the contracted adjective | winter-flowing, swollen by rain and melted snow; as Subst. a torrent; a conduit |
| δίδραχμον | δίδραχμος, "as Subst. δίδραχμον" | worth two drachms; a double-drachm, half-shekel |
| ὅλος | οὖλος, "ionic form of ὅλος" | whole, entire; continuous, incessant |
| κρυφῇ | κρυφῆ, "= κρύβδην" | secretly |
| αἰχμαλωτίς | "fem. of αἰχμάλωτος" | taken by the spear, captive to one's spear, taken prisoner; prisoner; booty |
| ἀρήν | ἀρνός, its genitive used as the headword | a lamb, a sheep, ram, ewe |
| πρῶτος | πρότερος B, the superlative's section | **first**, first, foremost, outermost, the first men, the first prize … |

The old comments had called ποιμήν, δίδραχμον, χείμαρρος, κρυφῇ and ἀρήν absent from Middle
Liddell; each is there, under a key nobody had looked for.

A close form counts only where it covers the form in the text. διαναπαύω stays with LSJ:
Middle Liddell has only the middle, διαναπαύομαι, "to rest awhile", which does not say what
the active of GEN 5:29, *will give rest*, means. Nor does a compound count under its simplex,
or a verb under its noun — ἐνισχύω is not ἰσχύω, ἀσφαλτόω is not ἄσφαλτος — because reading
the one off the other would be composing.

**What the readings gain and lose.** πρῶτος heads as *first*, Middle Liddell's, where it had
been LSJ's *foremost*; ποιμήν loses LSJ's later *master, lord, pastor, teacher*; κατανύσσω
loses *stabbed and gouged*; χείμαρρος, a noun, heads with its first noun sense, *the torrent*;
δίδραχμα are *double-drachms* rather than *coins of two drachms*; μνημεῖον loses LSJ's
*tomb*. μήτρα, ὦμος and κρυφῇ now give one sense each and print as plain text: *the womb*,
*the shoulder with the upper arm*, *secretly*. αἰχμαλωτίς went the other way — the entry it
points to says more than the plain *captives* did, so it is a unit now, heading *prisoners*.

LSJ's fuller ranges for those words are not carried into the verse notes. The notes record
facts about the text; that a larger dictionary says more is a fact about dictionaries, and
LSJ says more for nearly every word. This file is where the change is recorded.

`check_lexicon` fails on an LSJ entry for any word Middle Liddell has, under any close form
`words.py` knows.
## The article's noun, by gender

Where the Greek article makes a noun of something that is not one — a participle, a
preposition's phrase, an adverb, a genitive — it is not *the* alone. Its gender and number
say what kind of noun, and a Greek reader hears the difference: οἱ μετ' αὐτοῦ are people,
τὰ ὀπίσω are things. So the article carries its English noun, chosen from its gender:

| gender | singular | plural |
| --- | --- | --- |
| masculine, feminine | the one | the ones |
| neuter | the thing | the things |

and its case is marked, as a noun's is: τῶν ἐπὶ τῆς γῆς is *of the things upon of the earth*.

Over a participle the noun sits inside the unit, where the corpus already put it — 46 of 48
read *the one* or *the ones*, whatever the gender. Seven neuter participles now read *the
things*: τὰ εἰσπορευόμενα of GEN 7:16 are *the things going into*, τὰ προπορευόμενα of GEN
32:18 *the things going before*. Neuter is grammatical gender — those are animals and flocks —
and the Greek says neuter of them.

Over a phrase or an adverb there is no one unit to hold the article, so it stands as plain
text with its noun: 44 of them. GEN 3:1 *of the things upon of the earth*, GEN 7:23 *the
ones in the midst of him*, GEN 19:17 *into the things backwards*, GEN 2:16 *of the thing in
the park*, where τοῦ ἐν τῷ παραδείσῳ has two articles and the first makes a noun of the
phrase. τὰ αὐτοῦ is *the things of him*; τοῦ Σααρ, said of a man, *of the one of Saar*. The
neuter singular is the awkward one — τὸ πρωί is *the thing early in the day* — and it is the
gender, not the sense, that chose it.

**Every plain `the` in front of a unit, classified from the Greek.** The pass that folded
articles in had skipped any headword with *the* inside it — *son of the same mother*, *in the
midst of*, *early in the day* — which hid every μετά and every ἀδελφός. Read off the Greek
instead, the plain `the`s before a unit were:

- **48 a second copy** of an article the unit already carried — *the the man*, GEN 29:32,
  and *the the he-goats*, three times, once its unit had been flattened to plain text.
  Dropped. They predate this session.
- **8 an article that belonged inside the unit** — all ἀδελφός, *the sons of the same mother*.
- **44 an article making a noun of a phrase**, given its noun as above.
- **28 ὁ δέ**, the pronoun, which stays.

And by hand: the article before a possessive belongs to the noun after it — τὴν ἑαυτῆς
παιδίσκην is *of herself the young girl*, GEN 16:3 — and the articular infinitive of GEN 35:17,
ἐν τῷ σκληρῶς αὐτὴν τίκτειν, took its τῷ off the adverb in front of it: *in hard her the
bringing into the world*. Two case markers written twice, *of the of daughters* and *of the of
flocks*, lost the second.

`check_articles` holds all of it: no plain `the` before a unit but ὁ δέ's, no `the the`, and
over a participle the article's noun follows its gender.
## Loose ends before Genesis 37

**ὁ δὲ θεός had the anarthrous formula.** At GEN 31:5 and 31:29 the article stood in front of
δέ — `the [[but]] [[God|everything that God is by nature, deity in full and undiminished
kind]]` — so the unit read as though the Greek had no article. Every θεός in the corpus was
checked against its Greek; those two were the only ones, and they read *but, the God* now,
with the articular formula.

**An article cut off from its noun by a particle.** The same shape fifteen more times: Ἡ μὲν
φωνή read *the <on the one hand> <sound>*, ὁ δὲ πατήρ *the <but>, <father>*. The particle goes
first and the article inside the noun's unit after it, as GEN 8:5 already had *<but>, <the
water>*. Where the next unit already carried the article — ὁ δὲ εὐλογῶν, *the one speaking
well of* — the stray `the` was a second copy and went. GEN 31:20's τοῦ μὴ ἀναγγεῖλαι is an
articular infinitive with μή between: *not, of the carrying back tidings of*.

**The article as pronoun carries its noun.** ὁ δὲ εἶπεν, "and he said", ten times: *the one,
but, said*; οἱ δὲ εἶπαν, *the ones*. It had been the one exception to the article's noun, and
on that rule's own logic it is the plainest case of all — the article is the noun there. No
plain `the` now stands in front of any unit, and `check_articles` holds it without an
exception.

**ἕως τοῦ νῦν read two ways.** *Until of the one now* at GEN 15:16 and 18:12, *until of the
thing now* at 32:5. The two masculine lines carried a note — "module GSN — masculine, as
MorphGNT codes ἕως τοῦ νῦν (Matt 24:21)" — following the New Testament parallel over the
Rahlfs module; 32:5 had never been brought into line. An adverb made into a noun takes the
neuter article, which is the module's own coding, so all three are neuter now and read *of the
thing now at this very time*.

**Chains that drifted both ways.** The chain check caught one chain saying less than another
of the same form, and nothing else. πόθεν read *from what country* in one verse and *how can it
be and impossible* in another — neither a subset of the other, and neither the entry, which
gives *whence, from what source, whence and wherefore*. Four words were like it; all now read
their entry. πάλιν took its full range, the *notion of contradiction* among it — *contrariwise,
opposite, the change* — which neither chain had carried, with the tagging's fragments curated
out: *gain* is half of *gainsay*. The check now fails on chains apart in either direction. It
needed its stemmer fixed first: `deposed` had been cut to `depo` where `depose` stays
`depos`, because an `s` came off what `-ed` left, and *strove* and *broke* were missing from
the irregulars.

**A case marked twice.** The article passes left eighteen places where a noun's case printed
once outside its unit and again inside it — `to [[to the house]]` at GEN 35:2, `of [[of the
hands]]` at 31:42 — or twice before the article's noun, *of of the ones* at 34:19. Each
was the marker the old plain *the* had carried, left behind when the article moved into the
unit. All eighteen print the marker once now, and `check_articles` fails on a marker written
twice. A unit whose own gloss opens with the marker keeps it: ἀλλογενής is *of another race*,
and its genitive at GEN 17:27 is *of of another race*, as the article stays before *thy*.

## Every declined word, and every name's article

Settled before Genesis 37, each with side-by-side examples. Applied across Genesis 1–36:

**A name marks its case.** Names had never come under the rule that gives a noun *of* or
*to*, which had read units only: 135 genitive names had their *of* and some 380 did not. A
name is a noun, and every genitive and dative name now carries its marker by the case the
morphology gives it, indeclinable names included: *the sons of Esau*, *out of of Charran*,
*in to Edom*. 433 markers. Eleven articles in another case than their name had stood as a
plain *the*; each makes a noun of the name, *the oak, the one of Mambre*.

**A name's article prints.** The GEN 10 note above kept it off, as English does before a
person's name, and some 334 places followed it while 27 printed it. One *the* per Greek
article holds for names too: τῷ Ιακωβ is *to the Jacob*, τοῦ Ιωσηφ *of the Joseph*. 331
added.

**Every declined word marks its case, not only the noun.** Agreement puts one ending on each
word of a phrase, and each shows it — *to the day to this*, *from of all of the works*. The
corpus had marked agreeing words 215 times and left them bare 71, mostly datives: *to the day
that*, *to the day the seventh*, and a few read by their use, `with big` at 12:17. All 92 units
are marked now, and the dates' plain ordinals and nouns with them (*in to the six hundredth to
year*). Indeclinable numerals are marked as indeclinable names are, by the morphology's case,
in the Greek's order: ἐτῶν ἐνενήκοντα ἐννέα is *of years of ninety of nine*, and 5:32 and 7:6,
which had read *of five hundred years*, now read *of years of five hundred*.

**ἐν takes its own unit where it has nothing to merge into.** It was exempt from the
one-sense check as the preposition that merges, and the check counted a word as opened if
any unit in the verse named it. Between them, 43 ἐν had printed as a bare *in* before a name,
a pronoun or a plain noun. Each is `[[in|within, inside of, and by means of|ἐν]]` now, its
object marked after it: *in to Χαρραν*, *in to you*, *in to which*. The check counts units
per occurrence and no longer exempts ἐν. ἐνευλογέω's plain *will be blessed in* beside the
new unit (12:3, 18:18, 28:14) needed the bare-headword check to let a plain word print each
word of its first sense, not only the whole of it.

**Smaller slips found on the way.** ῥάβδος read singular for its six plural forms at
30:37–41, and *a rod* for ταῖς ῥάβδοις; they read *the rods*. τῇ τρίτῃ ἡμέρᾳ at 31:22 had its
article moved onto the noun and the noun put first; it follows the Greek, *to the third to
day*. 14:5's τοὺς ἐν Ασταρωθ read *the in*, an article with no noun: *the ones in*. 23:11's τὸ
ἐν αὐτῷ, *the thing in to it*. 4:8 read the infinitive's accusative subject *of them*; it is
*them*, as at 32:20. 36:15's πρωτοτόκου has no article and lost its *the*; 31:33's τῶν δύο
παιδισκῶν had printed its one article twice and now prints it once.

## ἐάν reads its entry

ἐάν had read `if` as plain text since GEN 4, εἰ's English. Middle Liddell's entry begins "if
haply, if, followed by subj. (whereas εἰ is foll. by ind. or opt.)": the first translation is
*if haply* — the ἄν in εἰ + ἄν, which a Greek reader hears in the word — and the plain *if*
after it is the printed entry's own, left untagged by Perseus. `MARKUP_LOST` restores it, and
every conjunction ἐάν is `[[if haply|if haply, if|ἐάν]]`: 25 in Genesis 1–36. ἐάν after a
relative, the particle (`ὃ ἐάν`), keeps reading `ever` with ἄν; the entry's *whosoever* is that
construction's, not the conjunction's.

## The articular infinitive

CLAUDE.md has said since the article pass that an articular infinitive becomes a gerund, and
the merged ἐν τῷ form did — *in the rubbing out* — but every other one followed the GEN 5
note that left the article unprinted: πρὸ τοῦ γενέσθαι read *before to come into being*, οὐ
προσέθετο τοῦ ἐπιστρέψαι *not put to, to turn about*. 82 of them, against 17 gerunds. An
article left off for English's sake is the exception the project does not make, so each now
reads as a gerund with its article and the article's case: *before of the coming into being*,
*of the turning about*, *into the middle of the begetting* (μετὰ τὸ γεννῆσαι), *into the
drinking* (εἰς τὸ πιεῖν). The chains turn whole, a second verb joined by *and* with them —
*of the going back and returning* — and what is not a verb stays: *of the being concluded and
inferred*. ζῆν at 19:19 keeps its entry's *alive* as *of the being alive*, as the participle at
3:20 has *of the alive*. `check_unit_cases` fails on an infinitive with its own article that
does not read as a gerund. The bare-headword check now takes a hyphenated word as one word, so
the plain *drinking-troughs* of 30:38 does not hold the gerund *the drinking*.

### Words new in GEN 37

From Middle Liddell unless marked; the headword is the entry's first translation in the form the
text uses.

- ἐνύπνιον — **headword** `a thing seen in sleep`; **chain** `a thing seen in sleep, a dream`. The
  entry's *in sleep* glosses the adverbial use and is in `NOT_SENSES`. Articular `the thing seen
  in sleep`, plural `the things seen in sleep, the dreams`. 37:5–10, 37:20.
- ἐνυπνιάζομαι — LSJ, one sense, *dream*, for middle and passive alike: plain `dreamed`,
  `having dreamed`, as at 28:12. 37:5–10.
- ἐνυπνιαστής — LSJ, one sense, *dreamer*, citing this verse: plain `the dreamer`. 37:19.
- καταφέρω — **headword** `brought down`; **chain** `brought down, drove ships, paid down, carried
  home`; the passives and the scraps of examples left out. 37:2.
- ψόγος — **headword** `a blamable fault`; **chain** `a blamable fault, a blemish, a flaw, blame,
  censure`. 37:2.
- ποιμαίνω — `being shepherd` (participle), `are shepherd` (present plural), the chain of 30:36 in
  the form. 37:2, 37:13.
- νέος (positive) — **headword** `young`; **chain** `young, youthful, new and fresh, new and
  strange`, as the comparative's chain reads. 37:2.
- χιτών (singular) — `garment worn next the skin and frock, coat of mail, covering, skin`, the chain of
  3:21 in the singular, with no article where the Greek has none. 37:3–33.
- δεσμεύω — **headword** `to fetter`; **chain** `to fetter and put in chains, to tie together`. 37:7.
- δράγμα — **headword** `as much as one can grasp`; **chain** `as much as one can grasp, handfuls,
  trusses, sheaves, uncut corn`, singular `handful, truss, sheaf`. The stemmer now takes *sheaves*
  for *sheaf*. 37:7.
- ὀρθόω (aorist passive) — **headword** `was set straight`; the passive of the active senses with
  the passive-only ones, *rose from one's seat and stood up*, *went straight*. 37:7.
- περιστρέφω (aorist passive participle) — **headword** `having been whirled round`; **chain**
  `having been whirled round, having been wheeled round, having been turned round and spun round,
  having come round to, having been tied behind`. 37:7.
- κυριεύω — `being lord`, `you will be lord`, the chain of 3:16. βασιλεύω — `being king`, `you
  will be king`. 37:8.
- ὥσπερ — **headword** `just as if`; **chain** `just as if and even as`. Its first Latin run, *quasi,
  tanquam*, is Latin throughout and in `LATIN_ONLY`. 37:9.
- σελήνη — **headword** `the moon`; **chain** `the moon, the moonlight, Selene the goddess of the
  moon`, as ἥλιος reads. 37:9.
- ἀστήρ (anarthrous) — `stars, flames and lights and fires`. 37:9.
- ἐπιτιμάω — **headword** `laid a value upon`; **chain** `laid a value upon, shewed honour to,
  raised in price, laid a penalty on, censured`, the entry's spelling kept. 37:10.
- διατηρέω — `watched closely`, the chain of the future at 17:9 in the aorist. 37:11.
- βόσκω — `to feed`, `feed`, the chain of 29:7. 37:12, 37:16.
- ὑγιαίνω — `are sound`, the chain of 29:6 in the plural. 37:14.
- πλανάω (present participle) — `being made to wander`, the chain of 21:14 in the participle. 37:15.
- ζητέω — `you seek`, `I seek`, the chain of 19:11. 37:15–16.
- ἀπαίρω (perfect) — `they have lifted off`, each sense with the perfect's *and it stands so*.
  37:17.
- ἐντεῦθεν — **headword** `hence`; **chain** `hence, thence, henceforth, thenceforth, thereupon,
  from that source`. 37:17.
- κατόπισθεν, with the genitive — **headword** `behind`; **chain** `behind and after and in the rear`; the
  temporal senses are the adverb's. 37:17.
- προοράω — **headword** `saw before one`; the entry's *one* kept, as ἀναβλέπω keeps *one's sight*.
  37:18.
- πονηρεύομαι — **headword** `were being evil`; **chain** `were being evil, were acting wickedly,
  were playing the rogue`. 37:18.
- λάκκος — **headword** `the pond`; **chain** `the pond, the pit and reservoir`. 37:20–29.
- θηρίον (singular) — `a wild animal, a beast, a savage beast, game`, the chain of 2:19 in the
  singular. 37:20, 37:33.
- ἐξαιρέω (middle) — `took out for himself`, `may take out for himself`, with every middle sense:
  *choose for oneself and carry off as booty, bereave of, take away from one, set free and
  deliver*. 32:12's middle had stopped at the second and is brought into line; it is the verse
  where the sense is *deliver*. 37:21–22.
- ἐκχέω (aorist subjunctive) — `you may pour out`. ἐμβάλλω — `throw in`. ἐπιφέρω — `you may bring`.
  37:22.
- ἐκδύω — **headword** `took off`; **chain** `took off and stripped off, stripped`. 37:23.
- κενός — `empty`, the chain of 31:42. 37:24.
- ὁδοιπόρος — **headword** `wayfarers`; **chain** `wayfarers, travellers, fellow-travellers,
  guides`. 37:25.
- γέμω — **headword** `were being full`; **chain** `were being full, were being full of`. 37:25.
- θυμίαμα — **headword** `of things which are burnt as incense`; **chain** `… of fragrant stuffs, of
  stuffs for embalming`, the plural of *that which is burnt as incense*, as ῥῆμα's *that which is
  said* becomes *the things which are said*. 37:25.
- ῥητίνη — LSJ, one sense, *resin of the pine*: plain `of resin of the pine`. 37:25.
- στακτός, as a noun — **headword** `of oozing out in drops`; **chain** `of oozing out in drops, of
  trickling, of dropping, of distilling`. Neither lexicon has στακτή on its own. 37:25.
- κατάγω — **headword** `to lead down`, `led down`; the active senses in order. 37:25, 37:28.
- χρήσιμος — **headword** `useful`; **chain** `useful, serviceable, good for use, good, apt, fit,
  useful for, much-used`. 37:26.
- κρύπτω — `we may hide`, with *cover in the earth and bury* as 4:14 has it. 37:26.
- ἔμπορος (articular) — `the ones who go on shipboard as passengers`, the chain of 23:16. 37:28.
- ἐξέλκω — **headword** `drew`; **chain** `drew, dragged out, dragged out from, dragged along`.
  ἀναβιβάζω — **headword** `made go up`; **chain** `made go up, caused to mount, mounted, drew up,
  brought up`. 37:28.
- διαρρήγνυμι — **headword** `broke through`; **chain** `broke through and cleaved asunder, burst`.
  37:29, 37:34.
- σφάζω — `slew`, the chain of 22:10 in the aorist. ἔριφος — `a young goat and kid`. μολύνω —
  **headword** `stained`; **chain** `stained, sullied, defiled, made a beast of`. 37:31.
- ἁρπάζω — **headword** `snatched away`; **chain** `snatched away, carried off, stole and was a
  thief, seized hastily and snatched up, seized and overpowered, plundered`. 37:33.
- σάκκος — **headword** `a coarse hair-cloth`; **chain** `a coarse hair-cloth, sackcloth, anything
  made of this cloth, a sack, a bag, a coarse beard`. 37:34.
- πενθέω — `was bewailing`, `bewailing`. 37:34–35.
- θέλω — `was willing`, the chain of 24:8 in the imperfect. 37:35.
- ᾅδης — **headword** `of Hades`; **chain** `of Hades, of Pluto, of the world below, of the grave,
  of death`. Middle Liddell keys the word with the god's capital, `*(/a|dhs`, and the spelling
  table points the lower-case lemma there; the capitals are the lexicon's. 37:35.
- σπάδων — one sense, *an eunuch*: plain `the eunuch`. ἀρχιμάγειρος — LSJ, one sense, *chief cook*,
  its *title of a great officer in Oriental courts* a description and not a translation: plain
  `to chief cook`. 37:36.
- Names new to the chapter: Δωθαϊμ, Ισμαηλίτης, Μαδιηναῖος, Πετεφρης. Πετεφρη at 37:36 is the dative of
  Πετεφρης, the nominative Rahlfs prints at 39:1. (First written here as an indeclinable Πετεφρη, against
  the module; 39:1 shows the module was right.)

## Loose ends before Genesis 38

**Two words, two numerals.** δέκα πέντε read *fifteen* at 5:10 and 7:20, one English word for two
Greek ones, while 17:25, 31:41 and 37:2 read each word for itself — *ten three*, *ten four*, *ten
seven*. Composing them is the composition the reading does not do; both now read *ten five*.

**γῆρας has one sense.** Middle Liddell gives *old age* and nothing more, so it is plain text, as
at 15:15, 21:2, 21:7 and 37:3. 25:8 had a merged unit whose chain added *the latter part of life*,
which no lexicon here gives; ἐν stands alone there now, `in to old age`, as at 15:15.

**The article over an adverb, with its case.** ἕως τῆς σήμερον ἡμέρας had read *until the to-day of
day* five times (19:37, 19:38, 26:33, 35:4, 35:20): the article stands with σήμερον, between it and
its noun, as τῇ τρίτῃ ἡμέρᾳ's stands with *third* at 31:22, but without its genitive. It reads
*until of the to-day of day*. 19:34's τῇ ἐπαύριον, the article making a noun of the adverb, read
*the on the morrow*; it carries its noun and its dative, *to the one on the morrow*, as 30:33's
τῇ αὔριον already did.

## The aorist reads as the plain past

The aspect table put *one completed act seen whole, not a process observed in progress* after an
aorist, and GEN 5 set it once at the head of a run rather than after each. Genesis 1–11 carried it
59 times; from Genesis 12 it stopped, across some 1,500 aorist indicatives. Every other past tense
is marked — the imperfect `was …ing`, the perfect `and it stands so` — so the plain English past
already says aorist, as the aorist is the Greek narrative's plain tense; on every aorist the
formula would have added an emphasis the Greek does not carry, and on some it was a judgment no
check could hold. The 59 are gone, CLAUDE.md says so, and `check_banned` fails on the formula in a
reading. The word-by-word layer keeps it as the aorist's line.

## A hint is a note, not a translation

The `hint` field was in no rule. Genesis 1–7 and 36–37 used it for a short note on what happens in
the verse or what matters in it; from Genesis 8 the hints for speeches began to render the speech
(*Count the stars, if you can: so will your seed be*), and through Genesis 24–35 nearly every hint
was a fluent translation of its verse, often carrying on the verse before (*and make me meats, the
kind I love, and bring them to me*). A translation picks one English word for each Greek one, which
is what the reading exists not to do, and it carried a familiar Bible's phrasing onto the page —
*fell on his neck* at 33:4. 653 hints in Genesis 8–35, and 37:20, are now notes, reporting speech
rather than rendering it: *Esau runs to meet Jacob, embraces and kisses him, and they both weep*.
CLAUDE.md states the rule, and `check_banned` holds it: no hint over 140 characters, none carrying
on the verse before, none in the first or second person outside a phrase quoted to discuss its
wording.

### Words new in GEN 38

From Middle Liddell unless marked; the headword is the entry's first translation in the form the
text uses.

- γαμβρεύω — LSJ, which Middle Liddell lacks: *form connexions by marriage*, in the middle *marry*,
  citing this verse, in the passive *to be connected by marriage*. The middle imperative γάμβρευσαι
  heads with the middle's sense: **headword** `marry`; **chain** `marry, form connexions by
  marriage, be connected by marriage`. 38:8.
- ἀνίστημι (first aorist active) — causal, as Middle Liddell says of the present, imperfect, future
  and first aorist: `make to stand up`, the chain of 9:9 in the imperative. The word-by-word layer
  had shown ἀνάστησον the intransitive senses, because the parse code cannot tell a first aorist
  from a second; `FORM_SENSES` now takes a pattern on the form, and the causal tenses are the ones
  built on στησ-. 38:8.
- ὅταν — **headword** `whenever`; **chain** `whenever, until`. 38:9.
- θανατόω — **headword** `put to death`; **chain** `put to death, mortified, put to death by
  sentence`. 38:10.
- χήρα (A-, as MorphGNT codes it) — **headword** `bereft of a husband`; **chain** `bereft of a husband and a
  widow`. 38:11.
- πενθερός — **headword** `the father-in-law`; **chain** `the father-in-law, the parents-in-law, the
  connexion by marriage, the brother-in-law`. 38:13, 38:25.
- περιαιρέω (middle) — **headword** `took off from herself`; the middle's senses, *took off her own,
  stripped off and took away*. 38:14, 38:19.
- χήρευσις — LSJ glosses it only as χηρεία, which Middle Liddell gives as *widowhood*; its second
  sense is LSJ's own: `of the widowhood, of the separation from a husband`. 38:14, 38:19.
- θέριστρον — one sense, *a light summer garment*: plain text. 38:14, 38:19.
- καλλωπίζω (middle) — **headword** `adorned herself`; the middle section, from *made herself fine
  and smart* to *affected*. 38:14.
- πάροδος — **headword** `in by-way`, merged with ἐν; the entry's scraps *as* and *passed by* are
  left out. 38:14.
- κατακαλύπτω (middle) — **headword** `covered up for herself`; **chain** `covered up for herself,
  covered her own, veiled herself`. 38:15.
- ἐάω — **headword** `let`; **chain** `let, suffer, allow, permit, let alone and let be`. 38:16.
- ἀρραβών — **headword** `earnest-money`; **chain** `earnest-money and caution-money`. Its Latin run,
  *arrhabo, arrha*, is in `LATIN_ONLY`. 38:17–20.
- δακτύλιος — **headword** `the ring`; **chain** `the ring and seal-ring`. 38:18, 38:25.
- ὁρμίσκος — LSJ: **headword** `the small necklace`; **chain** `the small necklace, the signet-cord,
  the collar`, LSJ citing this chapter for the second. 38:18, 38:25.
- ἐνδύω (middle) — **headword** `went into`, the entry's first translation, *to go into*; **chain**
  `went into, put on, put on and assumed, entered and pressed into, entered`. 38:19.
- κομίζω (middle) — **headword** `to get for oneself`; **chain** `to get for oneself, to receive in
  full, to acquire, to gain, to receive hospitably and entertain`. 38:20.
- ἐνταῦθα — **headword** `here`; **chain** `here, there, hither, thither, at the very time and then,
  herein, in this state of things and in this position`. Its Latin run, *hic, illic*, is in
  `LATIN_ONLY`. 38:21.
- καταγελάω (aorist passive) — **headword** `we may be laughed at`; the passive of the active senses
  with the entry's *to be derided*. 38:23.
- τρίμηνος, as a noun — **headword** `a period of three months`; **chain** `a period of three
  months, of three months`. 38:24.
- ἐκπορνεύω — one sense, *to commit fornication*: plain `has committed fornication`. The
  bare-headword check now lets a plain verb print the auxiliaries its tense needs, so that *has*
  is not taken for ἔχω's headword. 38:24.
- πορνεία — **headword** `of fornication`; **chain** `of fornication and prostitution`. 38:24.
- κατακαίω (aorist passive imperative) — **headword** `let her be burnt down`. 38:24.
- δικαιόω (perfect passive) — **headword** `has been set right`; each passive sense with the
  perfect's *and it stands so*. 38:26.
- προεκφέρω — LSJ: **headword** `put out before`; **chain** `put out before, uttered and pronounced
  before`. 38:28.
- δέω — **headword** `bound`; **chain** `bound, tied, fettered, put in bonds, enchained`. 38:28.
- κόκκινος — one sense, *scarlet*: plain text. πρότερος — `before`, the chain of τὸ πρότερον without
  the article. 38:28, 38:30.
- διακόπτω (aorist passive) — **headword** `was cut in two`; **chain** `was cut in two, was cut
  through, was broken through`. 38:29.
- φραγμός — **headword** `a fencing in`; **chain** `a fencing in, a blocking up, a fence, a paling,
  a palisade, a place fenced off, an enclosure, a partition`. 38:29.
- Chains taken from earlier chapters: νύμφη (11:31), πύλη (19:1), δοκέω (19:14), ἐπερωτάω (24:23),
  ὅδε and δίδυμος (25:24), ἀφικνέομαι (28:12, in the aorist), κείρω (31:19), πόρνη (34:31), μαῖα
  (35:17), ἐπισυνάγω (6:16, in the aorist).
- ἄνθρωπος — `of man` had read *of a man, of a human being* at 6:7 and 7:23, where the base chain
  carries *mankind* as well; all three now do.
- Names new to the chapter: Οδολλαμίτης, Ιρας, Σαυα, Ηρ, Αυναν, Σηλωμ, Χασβι, Θαμαρ, Θαμνα (the
  place, without the gender 36:12's woman has), Αιναν, Φαρες, Ζαρα.

## Loose ends before Genesis 39

**A plain perfect keeps its standing state.** 14:14's plain ᾐχμαλώτευται reads *has been taken
prisoner and stands taken prisoner*; 38:24's plain ἐκπεπόρνευκεν had read *has committed
fornication* alone, and now carries *and it stands so*, as every perfect unit's chain does.

**γίνομαι's perfect reads one way.** Three perfects had *has come into being — has come to be and
stands so, has arisen and remains arisen, has been brought into existence and continues so*; 32:11's
γέγονα had *I have come to be*, with the standing state on its first sense only. It reads *I have
come into being — I have come to be and stand so, I have arisen and remain arisen, I have been
brought into existence and continue so*.

**Genesis 38's cards.** The scraps of examples in seven new entries — περιαιρέω's *when* and *has
been taken away*, πάροδος's *as* and *passed by*, κατακαίω's *alive* and the rest — are in
`NOT_SENSES`. δέω's *to let*, *stop* and *from* stay: they are one sense, *to let or stop from*,
which the markup splits.

### Words new in GEN 39

From Middle Liddell unless marked; the headword is the entry's first translation in the form the
text uses.

- κατάγω (aorist passive) — **headword** `was led down`; the active chain of 37:28 in the passive,
  with the passive's own *came to land and landed*, *turned in and lodged in* and *returned*. 39:1.
- εὐνοῦχος — one sense, *a eunuch*: plain text. *chamberlains*, which the entry says eunuchs were
  employed as, is in `NOT_SENSES`. 39:1.
- ἀρχιμάγειρος — LSJ, *chief cook*, one sense: plain text. 39:1.
- ἀνήρ (anarthrous) — **headword** `man`; **chain** `a man, a man in the prime of life`. 39:1, 39:2.
- ἐπιτυγχάνω — **headword** `hitting the mark`; **chain** `hitting the mark, lighting and falling
  upon and meeting with, attaining to and reaching and gaining, succeeding in, being successful in,
  succeeding and being successful, reading`. *the first person one meets* is ὁ ἐπιτυχών, with the
  article, and is left out. 39:2.
- καθίστημι (first aorist active, causal) — **headword** `set down`; **chain** `set down and
  placed, stopped and brought to land, stationed, brought down, restored, brought before, set in
  order and set, ordained and appointed, settled and established, brought into a certain state,
  presented, made and rendered so and so, made and continued`. The aorist passive infinitive,
  articular, heads with `the being set down` and adds the intransitive senses Middle Liddell gives
  every passive tense. 39:4, 39:5.
- εὐαρεστέω (imperfect) — **headword** `was being well pleasing`, the chain of 5:22 in the
  imperfect. 39:4.
- ἐπιτρέπω — **headword** `turned towards`; **chain** `turned towards, turned over to and committed
  and entrusted to, trusted to and relied upon, referred the matter to, gave up and yielded,
  permitted and suffered, yielded and gave way, commanded`. 39:6.
- θέλω (imperfect) — **headword** `was willing`; **chain** `was willing, was wishing, was purposing,
  was being wont and accustomed, was meaning and purporting`. 39:8.
- ὑπερέχω (present) — **headword** `holds over`, the chain of the future in the present. 39:9.
- ὑπεξαιρέω (perfect middle) — **headword** `has taken out privily for himself`; **chain** `has
  taken out privily for himself and it stands so, has stolen away, has put aside and excepted and
  excluded`, the middle's senses. Read as middle, with οὐδέν the object (`A- ----ASN-`), as the
  module has it; both passes had read it as passive. 39:9.
- πῶς — `ENTRY` sends it to `pw=s2`: the bare key had resolved to `pw=s1`, Aristotle's *in a
  certain way*. **headword** `how`; **chain** `how, in what way, in what manner`. The entry's
  translations of πῶς with another particle — πῶς ἄν, πῶς γάρ, πῶς δή, καὶ πῶς and the rest — are
  in `NOT_SENSES`. 39:9.
- τοιοῦτος — **headword** `such as this`; **chain** `such as this, so great and so noble and so bad,
  such a`, the last being Middle Liddell's gloss of τοιοῦτός τις, the phrase of this verse. 39:11.
- ἔσω — `SPELLING` sends it to εἴσω: Middle Liddell's ἔσω is "older form of εἴσω", and its one
  translation, *to the interior*, is of the comparative ἐσωτέρω. **headword** `to within`;
  **chain** `to within, into, inside, within`. 39:11.
- ἐπισπάομαι — lemma as MorphGNT files it (1 Cor 7:18), and as the module has it; `SPELLING`
  sends it to ἐπισπάω. **headword** `drew`; **chain** `drew and dragged after her, attracted and
  gained and won, drew on and allured and persuaded, induced, became uncircumcised`, the senses
  the entry gives the middle. 39:12.
- κοιμάω (passive) — **headword** `be lulled`, `I will be lulled`; see the corrections below.
  39:7, 39:12, 39:14, 39:17.
- καταλείπω — **headword** `left behind`, `having left behind`; **chain** `left behind, left as an
  heritage, forsook and abandoned and left in the lurch, left remaining, left alone`. 39:12–18.
- καταλιμπάνω — `SPELLING` sends it to καταλείπω: the entry reads "= καταλείπω" and glosses
  nothing. **headword** `leaves behind`, καταλείπω's chain in the present. 39:16.
- ἐμπαίζω — **headword** `to mock at`; **chain** `to mock at and mock, to sport in and on`. 39:14,
  39:17.
- βοάω (aorist, first person) — **headword** `I cried aloud`, the chain of the participle. 39:14,
  39:15, 39:18.
- ὑψόω (aorist active) — **headword** `I lifted high`; **chain** `I lifted high, I raised up, I
  elevated and exalted`; the middle's *to raise for oneself* is left out. 39:15, 39:18.
- θυμόομαι — **headword** `was wroth`, the chain of 6:7 in the third person. 39:19.
- ὀργή (anarthrous dative) — **headword** `to natural impulse`. 39:19.
- ὀχύρωμα — **headword** `the stronghold`; **chain** `the stronghold and fortress`: one sense,
  but two words in it. 39:20.
- δεσμώτης — **headword** `the prisoners`; **chain** `the prisoners, the captives, in chains and
  fettered`, the last the entry's gloss of the word as an adjective. 39:20.
- κατέχω (present passive) — **headword** `are held fast`, the chain of the participle at its
  first use in the indicative. 39:20.
- καταχέω (aorist) — **headword** `poured down upon`; **chain** `poured down upon and poured over,
  poured and showered down, threw and cast down, let fall upon, melted down`. 39:21.
- ἀρχιδεσμοφύλαξ — LSJ, *chief gaoler*, one sense and citing this chapter: plain text. 39:21–23.
- δεσμωτήριον — one sense, *a prison*: plain text. ἐν before it takes its own unit, `in`. 39:22,
  39:23.
- ἀπάγω (perfect passive participle) — **headword** `the ones having been led away`, the active
  chain in the passive, with the passive's *brought to a point, tapering off*. 39:22.

## Corrections found in Genesis 39

**κοιμάω's passives read the passive of its first sense.** Fourteen units from 19:4 to 35:22 had
headed the passive with *fell asleep*, a translation Middle Liddell gives the middle and passive
alone, where the passive-headword rule wants the first sense in the passive. 30:15 alone had it,
as *let him be lulled to sleep*. Each now heads with *lulled* — `was lulled`, `were lulled`, `I was
lulled`, `be lulled`, `let us be lulled`, `let him be lulled`, `having been lulled`, `of the being
lulled`, `in the being lulled` — and the chain runs *lulled, hushed to sleep and put to sleep,
lulled to rest and stilled and calmed*, then the passive's own *fell asleep, went abed and lay
abed, slept, fell asleep and died, kept watch at night*.

**καταλείπω reads its own entry.** 2:24, 7:23 and 14:10 had *leave behind him*, the middle's
gloss, and *inheritance* for the entry's *heritage*; 33:15 had *leave in the lurch, leave out and
omit*, the chain of ἐγκαταλείπω. All four now carry the active's five senses, *left behind, left
as an heritage, forsook and abandoned and left in the lurch, left remaining, left alone*, in their
own tense and voice.

**ἐθυμώθη is θυμόομαι.** 6:7 filed ἐθυμώθην under θυμόομαι, as MorphGNT files ἐθυμώθη at Matt 2:16;
30:2 had filed the same verb under θυμόω, with the active's *was made angry* at its head. The
corpus check found the two when 39:19 used the form again. 30:2 reads `was wroth` now, the chain
of 6:7.

**Two notes caught up.** 19:4's note still said the article before an infinitive is not printed,
which the articular-infinitive rule retired; 24:54's said κοιμάω is *to fall asleep*, which is its
passive.

## Loose ends before Genesis 40

**The article goes into its word's unit, every time.** 62 units had let a gloss that opens
with *that which* or *anything* stand in for the Greek article: τὸ σπέρμα σου read *that which
is sown of you*, τὸ ῥῆμα *that which is said*, τῶν προβάτων *of anything that walks forward*.
By the rule of *the thy property*, each carries its *the*: `the that which is sown`, `the that
which is said`, `of the things that walk forward`, and on every sense of the chain. 38:9's
second σπέρμα is anarthrous and keeps its bare form. `check_unit_cases` now fails an articular
noun or adjective whose unit has no *the*.

**ἦν is never a bare *was*.** Five imperfects of εἰμί had read *was* with no possession to
explain it (7:19, 7:22, 7:23, 8:1, 8:9); each has the state formula now. JHN 1:1c, θεὸς ἦν ὁ
λόγος, had lost the *was* that the clause's old unit carried, and reads the short pre-existence
form of 1:2, `was — continuously, and without any point of having come to be —`. The new
`check_imperfect_be` counts the formulas against the imperfects, possession excepted.

**One word, one range in every form.** The chain check held one range within a headword;
`check_ranges` holds it across them, pairing each unit with the word it opens and grouping by
lemma, voice, number, degree, the senses the card gives the form, and — for a word used as a
noun — the sense it opens with (τὸ καλόν *beauty*, τὸ κακόν *evil*). It found 259 short chains.
Some were the lexicon's own splits, which the card had not shown and now does:
- `FORM_SENSES`: ἵστημι, ἀφίστημι and ἐξανίστημι are causal in their present, imperfect, future
  and first aorist and intransitive in the rest (ἀπέστησαν, both aorists' third plural, is the
  intransitive *revolted* at 14:4); δίδωμι's *to be ready to give, to offer* is the present's;
  ζάω's *living, alive* the participle's; γηράσκω's *to bring to old age* the first aorist's.
- The word layer's parse now carries the degree, so μείζων is a comparative with its own range.

The rest were losses, and about 560 units were brought up to the fullest chain their group had,
in their own form: γυνή's articular forms regain *the mortal woman*; τίκτω *begot, produced and
yielded*; ἀκούω *knew by hearsay*; εὑρίσκω *got and gained*; ἔχω *dwelt in and inhabited*;
πρόσωπον *mask*; ἐπιβάλλω's aorist its eleven senses. Where a chain had read another word's
entry, it reads its own: παιδίον is `young children, young slave-lads`, not παῖς's chain;
οἰκέω and κατοικέω no longer trade chains (24:13, 25:27, 34:30); ἀποκρίνομαι at 31:31 is
answering, not ἀποκρίνω's separating; the active ἀπόδος (29:21, 30:26) no longer reads the
middle's *sell*, and 25:31's middle ἀπόδου keeps it. Where the headword was not the entry's
first sense, it is now: φέρω `bore`, not *brought*; γαστήρ `paunch`; πένθος `grief`; φόβος
`flight` at 35:5; ἐξαίρω `lifted up` at 35:5, with LSJ's intransitive *start* in the note;
παραγίνομαι `was near`; συντάσσω `put in order together`; ἀλλάσσω `make other than it is`;
ἀναβοάω `shouted aloud`; ἐπάγω `brought on`; ἐπακούω and ὑπακούω `listened`; ἐπικαλέω's
middle `called upon for himself`, without the passive's *was called by surname*; δοχή `a
receptacle`; ὅπως, final, `that, in order that`. Senses the entry does not give came out:
κτῆνος's *oxen, sheep*, στήλη's *monument, pillar*, δικαιοσύνη's *observance of custom*, κρίνω's
passive *be chosen* in the active, ταπεινόω's middle *humble oneself*. 19:17's σῴζου reads as
passive, *be saved … come safe and escape to*, the mountain, and its note gives the middle.

**Two chains caught up.** ἐν merged with οἰκία had dropped *from which one is descended*; τὰ
ὑπάρχοντα's genitive had *property and substance* for the entry's *means*. Three ἐν units at
34:10 and 34:15 had swallowed their pronoun, *in us*; ἐν stands alone and the pronoun marks its
case, `in to us`.

**The tables above.** 173 rows whose lemma and headword the corpus still uses now show the
chain it uses; a row whose headword the corpus has since given up is the history of that word.

### Words new in GEN 40

From Middle Liddell unless marked; the headword is the entry's first translation in the form the
text uses.

- ἀρχιοινοχόος, ἀρχισιτοποιός, ἀρχιοινοχοΐα, ἀρχιδεσμώτης — LSJ, one sense each, so plain text:
  `chief cup-bearer`, `chief baker`, `office of chief cup-bearer` (LSJ spells it ἀρχιοινοχοεία),
  and `chief gaoler`, the gloss of ἀρχιδεσμοφύλαξ, inside whose entry LSJ files ἀρχιδεσμώτης. 40:1–23.
- δεσμοφύλαξ — one sense, *a gaoler*: plain text. 40:3.
- φυλακή — **headword** `in watching`, merged with ἐν; **chain** `watching and guarding, watch and
  guard and ward, guard and garrison, station and post, place for keeping, ward and prison,
  keeping and preserving, guardianship, safe-guard and precaution`. The glosses of the entry's
  examples are in `NOT_SENSES`. 40:3, 40:4, 40:7.
- ἀπάγω (pluperfect passive) — **headword** `had been led away`, the passive chain of 39:22. 40:3.
- συνίστημι (first aorist, causal) — **headword** `set together`; the causal senses, from *set
  together and combined …* to *offered as a guarantee*. 40:4.
- παρίστημι (second aorist) — **headword** `stood by`, the pluperfect chain of 37 in the aorist. 40:4.
- ἑκάτερος — **headword** `each of two`; **chain** `each of two and either and each singly`. 40:5.
- ταράσσω (perfect passive participle) — **headword** `having been stirred`, the aorist passive's
  chain. 40:6.
- ἐρωτάω (imperfect) — **headword** `was asking`. 40:7.
- σκυθρωπός — **headword** `angry-looking`; **chain** `angry-looking, of sad countenance, sullen,
  gloomy and sad and melancholy`. 40:7.
- συγκρίνω — **headword** `compounded`, `the one compounding`; **chain** *compounded, compared,
  measured and estimated*. Middle Liddell has no sense of interpreting; LSJ's *interpret dreams*,
  citing 40:8, is in the note. σύγκρισις likewise: `the compounding, the comparing and
  comparison`, with LSJ's *interpretation of a dream*, citing 40:12, in the note. 40:8–22.
- διασάφησις — LSJ: **headword** `the explanation`; **chain** `the explanation and interpretation`. 40:8.
- πυθμήν — **headword** `hollow bottoms`; **chain** `hollow bottoms and stands of a cup, bottoms and
  depths, bottoms and foundations, anvil-stands, bottoms and stocks and roots of a tree, stems
  and stocks`. 40:10, 40:12.
- θάλλω — **headword** `blooming`; **chain** `blooming, abounding, being luxuriant, flourishing,
  being active`; the examples' τεθαλυῖα glosses are in `NOT_SENSES`. 40:10.
- ἀναφέρω (perfect participle) — **headword** `having brought up`, the chain of 22:2 with *and
  standing so*. 40:10.
- βλαστός `sprouts`; πέπειρος `ripe, softened`; βότρυς `the clusters, the bunches of grapes`;
  σταφυλή `of a bunch of grapes, of the plummet of a level`. 40:10, 40:11.
- ποτήριον — **headword** `the drinking-cup`; **chain** `the drinking-cup and wine-cup`. 40:11–21.
- ἐκθλίβω — **headword** `I squeezed much`; **chain** `I squeezed much, I distressed greatly`. 40:11.
- μιμνήσκομαι — the entry's last sense, *to mention, make mention of*, is in every chain now:
  40:14 has μνησθήσῃ περὶ ἐμοῦ Φαραω, *make mention of me to Pharaoh*, and the five earlier
  units took the sense on.
- ἀρχή — the entry's power, sovereignty, magistracy, office and term of office join the chain:
  `beginning, origin, first cause, headship and rule and governing precedence, end and corner,
  first place, power and sovereignty and dominion and command, sovereignty and empire and realm,
  magistracy and office, term of office`. 40:13 and 40:20–21 are the cup-bearer's office; 2:10,
  10:10 and 13:4 took the same range. Ἐν ἀρχῇ keeps its formula.
- οἰνοχοέω — one sense once the example's pieces are out, *to pour out wine for drinking*: plain
  text. 40:13.
- κλοπή — **headword** `to theft`; **chain** `to theft, to a secret act and fraud, to the surprise`.
  Middle Liddell's *by stealth* is the dative κλοπῇ as an idiom, and the case marker reads the
  dative as every dative; the note gives it. 40:15.
- κλέπτω (aorist passive) — **headword** `I was stolen`, the chain of 30:33 in the aorist. 40:15.
- κανοῦν — LSJ's κάνεον, contracted: **headword** `baskets of reed or cane`; **chain** `baskets of
  reed or cane, bread-baskets`. 40:16–18.
- χονδρίτης — LSJ, one translation, *made of groats or coarse meal*: plain text. 40:16.
- σιτοποιός — used as a noun, so its first noun sense heads: `of one that ground the corn in the
  handmill`, then the adjective's *of grinding and baking* and *of a baking-woman*. 40:17.
- κατεσθίω (imperfect) — `was eating up, was devouring`. 40:17.
- ἀφαιρέω (future) — **headword** `will take from`, the active chain of the aorist. 40:19.
- κρεμάννυμι — **headword** `will hang`, `hung`; **chain** *hang, hang up*. 40:19, 40:22.
- σάρξ (plural, articular) — `the fleshes`, the plural chain of 6:3 with the article. 40:19.
- ἐπιλανθάνομαι — one sense, *to forget*: plain text. 40:23.

### Words new in GEN 41

From Middle Liddell unless marked; the headword is the entry's first translation in the form the
text uses.

- εὐθηνία — LSJ, Middle Liddell having only the verb εὐθηνέω: **headword** `prosperity`; **chain**
  `prosperity and plenty, good condition, abundance, corn-supply`. LSJ's personified *Abundance,
  Plenty* is a goddess's name and repeats the senses. 41:29–53.
- γένημα — LSJ, one translation, *produce*: plain text, `the produces`. LSJ keeps it apart from
  γέννημα, the begotten, and so does the dictionary form. 41:34.
- δευτερόω — LSJ: **headword** `of the doing the second time`; **chain** *doing the second time,
  repeating, changing, giving one a second blow, slaying, occurring twice*. LSJ cites 41:32 for the
  last. 41:32.
- τοπάρχης — LSJ, one translation: plain text, `governors of a district`. 41:34.
- ἄχει — LSJ's "ἄχει or ἄχι", filed as printed: **headword** `in the reed-grass`, merged with ἐν;
  **chain** `the reed-grass, the lamp-wick`. 41:2, 41:18.
- ἀνεμόφθορος — LSJ, one translation, *blasted by the wind*: plain text. Perseus keys the entry
  without its nu, a)emo/fqoros. 41:6–27.
- ἀποπεμπτόω — LSJ: **headword** `let them give a fifth part of`; **chain** adds *take a fifth part
  of*, which LSJ cites for 41:34. 41:34.
- σιτοβολών — LSJ: **headword** `the places for storing corn`; **chain** `…, the granaries`. 41:56.
- ξυράω — the Koine spelling of ξυρέω, which Middle Liddell heads (`SPELLING`). The active has one
  sense once the middle's *shave oneself* is set aside by the form (`FORM_SENSES`) and the
  proverb's *it shaves* by `NOT_SENSES`: plain text, `shaved`. 41:14.
- ἐγείρω (first aorist passive) — **headword** `was awakened`; **chain** the active's senses in the
  passive, then the passive's own *awoke* and *roused and stirred himself and was excited*. The
  second aorist's *keep watch* and the perfect's *be awake* are set aside by the form. 41:4, 41:7.
- στάχυς — **headword** `ears of corn`; **chain** `ears of corn, scions and children and progeny`.
- ἐκλεκτός (adjective) — `picked out and select`, the chain of 23:6 without ἐν; the noun's *the elect*
  is not the adjective's. 41:2–20.
- αἰσχρός — **headword** `causing shame`; **chain** `causing shame and abusive, ugly and
  ill-favoured, shameful and disgraceful and base and infamous, awkward`; the comparative puts
  *more* before each. 41:3–27.
- λεπτός — **headword** `peeled`; **chain** `peeled and husked and threshed out, fine and small,
  thin and fine and delicate, thin and lean and meagre, slender and taper, strait and narrow,
  small and weak and impotent, faint, light and slight, fine and subtle and refined`. The examples'
  *a thin line*, *sheep and goats* and *light breezes* are in `NOT_SENSES`. 41:3–27.
- βόσκω (imperfect middle/passive) — **headword** `were being fed`, the first sense in the
  passive, then the passive's own *feeding and grazing*, *feeding on*, *nurtured*, *running riot
  in*. 41:2.
- νέμω (imperfect middle/passive) — **headword** `were being dealt out`; the middle's *distributing
  among themselves … possessing … dwelling in … dwelling*, and of cattle *feeding, going to pasture and
  grazing, feeding on, eating, consuming and devouring*. 41:3, 41:18.
- ἀναφύω (imperfect middle/passive) — **headword** `were being produced again`; **chain** adds
  *let grow*, *growing up*, *growing again*. 41:6, 41:23.
- καταπίνω — **headword** `gulped`; **chain** `gulped and swallowed down, drank in and imbibed,
  swallowed up and consumed, spent in tippling`. 41:7, 41:24.
- ἐξηγητής — **headword** `the ones who lead on`; **chain** `…, the advisers, the expounders and
  interpreters`. 41:8, 41:24.
- σοφός (as a noun, with no noun sense of its own) — **headword** `the ones skilled in any
  handicraft`, the article carrying its noun, then the entry's range. 41:8.
- ἀναμιμνήσκω — **headword** `I remind`; **chain** `I remind, I remind one of, I recall to memory
  and make mention of`. The passive's *remember* is set aside by the form. 41:9.
- συμβαίνω — **headword** `stood with the feet together`; **chain** to *came to pass and happened,
  turned out, resulted and followed*. One example's *has come in my way* is in `NOT_SENSES`. 41:13.
- σωτήριος (as a noun) — the first noun sense heads: `the deliverance`; **chain** `the deliverance,
  the safety, the thankoffering for deliverance`. 41:16.
- ἀποκρίνομαι (future passive) — `will give answer to`, the deponent chain of the aorist. 41:16.
- ἄνευ — **headword** `without`; **chain** `without, away from and far from, except and besides`.
  41:16, 41:44.
- ἵστημι (perfect infinitive) — `to have been set and to stand so`, the pluperfect's chain of 18:2
  in the infinitive. 41:1, 41:17.
- οἷος — **headword** `such as`; **chain** `such as, what sort, what manner of nature and kind and
  temper, how, like as and like and just as, because of what`. 41:19.
- ἔχω (present middle/passive participle) — **headword** `being had`, then the middle's *holding on
  by and clinging to … coming next to and following closely, being close and touching and
  bordering on*. 41:23.
- ἀληθής — **headword** `unconcealed`; **chain** `unconcealed, true, truthful, coming true`. 41:32.
- σκέπτομαι — **headword** `look about`; **chain** to *think of beforehand and premeditate*. 41:33.
- φρόνιμος and συνετός (positive and comparative) — `in one's right mind, …, prudent`, the
  superlative chain of 3:1 in its degree; `intelligent and sagacious and wise, intelligent in,
  intelligible`, its run one item since EXO 31. 41:33, 41:39.
- φυλάσσω (aorist and perfect passive) — **headword** `let it be watched`, `having been watched`,
  the first passivisable sense heading, *keep watch and ward* being intransitive. 41:35, 41:36.
- θρόνος — **headword** `the seat`; **chain** `the seat and chair, the throne and chair of state,
  the throne and the king's estate and dignity, the oracular seat, the chair of a teacher`. 41:40.
- βύσσινος — Middle Liddell's *made of βύσσος* names the stuff by its Greek word; the reading gives
  its English spelling with the Greek after it: **headword** `made of byssus (βύσσος)`; **chain**
  `made of byssus (βύσσος), fine linen`. 41:42.
- κλοιός — **headword** `a dog-collar`; **chain** `a dog-collar, a large wooden collar, a pillory, a
  collar`. 41:42.
- ἅρμα — **headword** `the chariot`; **chain** `the chariot, the war-chariot, the chariot and horses
  and yoked chariot, the team and horses`. 41:43.
- κηρύσσω — **headword** `was a herald`; **chain** to *commanded publicly*. κῆρυξ, `a herald, a
  pursuivant, a marshal, a public messenger, a crier`. 41:43.
- πεινάω `was hungry`; κράζω `croaked`, *screamed and shrieked and cried aloud*; πωλέω `was
  exchanging`, *selling and offering for sale*; ἀγοράζω `to be in the agora (ἀγορά)`, the entry's
  Greek word in its English spelling and then itself, then *buy in the market and buy and
  purchase*. 41:55–57.
- ἑαυτοῦ — Rahlfs prints αὑτοῦ at 41:11, the contracted reflexive: `of himself`.
- νεανίσκος, σήμερον, θυγάτηρ, υἱός, τριάκοντα, διάδηλος, ἐπιλανθάνομαι, ἐνυπνιάζομαι — one sense
  each: plain text.

**A breathing.** The module cross-check caught 41:11's αὑτοῦ, transcribed with the smooth
breathing; the scan shows the rough. The reflexive is now in the text, the morphology and the
reading.

## Loose ends before Genesis 42

**A Greek word inside a translation.** Middle Liddell names a thing by its Greek word in five
translations the corpus's words reach — βύσσινος *made of βύσσος*, ἀγοράζω *to be in the ἀγορά*
and *to lounge in the ἀγορά*, ἀφίημι *to let go as an ἄφετος*, κατοικέω *to dwell in as a
κάτοικος*, ῥάβδος *the wand borne by the ῥαψῳδός* — and Perseus tags the word as Greek, so the
`<tr>` stopped before it, or, inside it, reached the card as Beta Code. `GREEK_LOST` restores each
as the entry prints it; `GREEK_AFTER` names κρατέω, whose *get possession of* is whole and whose
Greek is an example's object, and ἄν, whose usage paragraph is tagged as one translation.
`validate.py` reads the lexicon for a new site, as it does for the Latin runs. The reading gives
such a word its English spelling with the Greek after it: `made of byssus (βύσσος)`, `to be in
the agora (ἀγορά)`. The 36 κατοικέω cards across the corpus now open with the whole first
translation.

### Words new in GEN 42

From Middle Liddell unless marked; the headword is the entry's first translation in the form the
text uses.

- πρᾶσις — **headword** `a selling`; **chain** `a selling, a sale`. 42:1.
- ῥᾳθυμέω — **headword** `you leave off work`; **chain** `…, you are remiss`. 42:1.
- πρίαμαι — Middle Liddell writes "to have *a thing* sold to one, to buy, purchase", and the italic
  object cuts the translation into two `<tr>`s; `MARKUP_LOST` restores it whole and `NOT_SENSES`
  sets the halves aside. **Headword** `have sold to yourselves`, `to have sold to themselves`, `to
  have sold to ourselves`; **chain** adds *buy, purchase, buy with, purchase by, buy at, farm*. 42:2,
  42:3, 42:10.
- μαλακία — **headword** `softness`; **chain** `softness and delicacy and effeminacy, want of
  patience and weakness, calmness of the sea`. μαλακίζομαι, `to be softened`, *made effeminate
  and show weakness and cowardice*, *appeased*. 42:4, 42:38.
- ἀλλοτριόω (imperfect passive) — **headword** `was being estranged from`. 42:7.
- ἥκω (perfect ἧκα) — `you have come and it stands so`, the chain of 6:13's present with the
  perfect's formula. 42:7, 42:9.
- κατάσκοπος — **headword** `ones who keep a look out`; **chain** `…, scouts and spies, persons sent
  to examine and report and inspectors`. 42:9–34.
- ἴχνος — **headword** `the tracks`; **chain** `the tracks and footsteps, the tracks and traces and
  clues, the feet, the legs`. 42:9, 42:12.
- ὑγίεια — **headword** `the health`; **chain** `the health and soundness, the healthy states and
  conditions`. 42:15, 42:16.
- νή — Middle Liddell gives no translation: "Particle of strong affirmation, like epic ναί". As a
  pointer to ναί it reads ναί's range, `yea and verily, aye and yes`, the chain of 17:19. 42:15, 42:16.
- φανερός — **headword** `open to sight`; **chain** `open to sight and visible and manifest and
  evident, known, open, real, known and acknowledged, conspicuous`. 42:16.
- ἀληθεύω `you speak truth, you come true`; ἀπάγω's aorist passive `be led away`, the passive
  chain of 40:3 in the imperative; φαίνω's future middle `you will be brought to light`. 42:15–16.
- βαδίζω — **headword** `go slowly`; **chain** `go slowly and walk, go and march, go by land, enter,
  proceed`. 42:19.
- ἀγορασμός — LSJ: `the purchasing, the purchase`. σιτοδοσία — LSJ: `of the gratuitous distribution
  of corn, of the allowance of corn`. Both cite 42:19. 42:19, 42:33.
- κατέχω (aorist passive imperative) — `let him be held fast`, the passive chain of 39:20. 42:19.
- πιστεύω (future passive) — `will be trusted`, the senses that take a passive. 42:20.
- ὑπεροράω — **headword** `we looked over`; **chain** `we looked over and looked down upon, we
  overlooked and slighted and despised, we showed contempt for`. 42:21.
- καταδέομαι — LSJ, one translation, *entreat earnestly*: plain text. 42:21.
- ἐπέρχομαι — **headword** `came upon`; **chain** to *went through and executed*. An impersonal
  example and the pieces of *to go over* are in `NOT_SENSES`. 42:21.
- ἑρμηνευτής — LSJ, "= ἑρμηνεύς": **headword** `the interpreter`; **chain** `the interpreter and
  dragoman, the court interpreter, the matrimonial agent and go-between, the broker and
  commissionaire, the interpreter and expounder`. 42:23.
- ἐμπίπλημι — the active `to fill quite full, to fill full of`; the middle and passive are set aside
  by the form. 42:25.
- ἀγγεῖον — Middle Liddell's entry reads only "ἄγγος", so it reads ἄγγος (`SPELLING`): `the vessels,
  the jars, the vats, the vases and pitchers and pails, the coffers and arks, the chests, the
  cinerary urns, the cells`. 42:25.
- ἐπισιτισμός — **headword** `a furnishing oneself with provisions`; **chain** `… and foraging, a
  stock and store of provisions`. 42:25.
- λύω — **headword** `having loosed`; **chain** the active range, from *loosened and unbound* to
  *profited and availed*. The examples' forms are in `NOT_SENSES`. 42:27.
- μάρσιππος — the spelling Rahlfs prints of Middle Liddell's μάρσιπος (`SPELLING`): `the bag, the
  pouch`. 42:27, 42:28.
- δεσμός — **headword** `the anything for binding`, as πόνος's `the anything produced by work`;
  plural `the things for binding`. 42:27, 42:35.
- κατασκοπεύω — LSJ, "= κατασκοπέω": `viewing closely and spying out and reconnoitring,
  reconnoitring, keeping a look-out, inspecting`. 42:30.
- κατακενόω — LSJ, "strengthd. for κενόω": the active senses of κενόω, `in the emptying`, merged
  with ἐν. 42:35.
- ἀτεκνόω (active) — `you made childless, you deprived of children`. 42:36.
- ἀνάγω — **headword** `I will lead up`; **chain** to *make ready and prepare myself*. 42:37.
- καταλείπω (perfect passive) — `has been left behind and stands so`. 42:38.
- λύπη (singular) — `of pain of body, of distress and sad plight, of pain of mind and grief`. 42:38.
- δέκα, δώδεκα, τρεῖς, σήμερον, υἱός, γῆρας, ἀλλήλων, κἀγώ, οὐχί, οὗ (where) — plain text.

## Loose ends before Genesis 43

**Three restored senses in the reading.** The senses `GREEK_LOST` gave back to the cards now stand
in the chains, the word given its English spelling and its Greek after it, or, where English has
none, a transliteration:

- κατοικέω — the first translation is *to dwell in as a κάτοικος*, and the headword was its first
  three words. Every unit now heads `dwelt in as a katoikos (κάτοικος)`, in its own form — `were
  dwelling in as a katoikos (κάτοικος)`, `to the ones dwelling in as a katoikos (κάτοικος)` — the
  noun kept singular, as the entry's generic *a κάτοικος* has it. 36 units, 9:27 to 36:20.
- ἀφίημι — *to let go as an ἄφετος, consecrate* joins the active chains after *let go and loose and
  set free*: `let go as an aphetos (ἄφετος) and consecrate`. The passive of 4:13 reads the entry's
  passive senses and is unchanged.
- ῥάβδος — *the wand borne by the ῥαψῳδός* joins after *a staff of office*: `a wand borne by the
  rhapsode (ῥαψῳδός)`, in each unit's number and case.

**νή opened by its oath.** νή reads ναί's entry, and with the accusative of what is sworn by it
takes the entry's oath, *yea by . .*: `yea by, yea, verily, aye and yes`. ναί itself still sets
the formula aside; a word filed under another's entry may now carry its own `NOT_SENSES`. 42:15,
42:16.

**ἄν's card.** A paragraph on the particle's uses, tagged as one translation, no longer opens it;
the card begins *perchance*.

### Words new in GEN 43

From Middle Liddell unless marked; the headword is the entry's first translation in the form the
text uses.

- διαμαρτυρία — Middle Liddell writes the Attic law-term in one translation, *evidence given to
  prevent a case from coming to trial* (`MARKUP_LOST`): plain text, the dative's `to` before it.
  43:3.
- διαμαρτύρομαι (perfect) — **headword** `has protested solemnly`; **chain** `has protested
  solemnly and it stands so, has protested, has protested and asseverated, has begged earnestly
  and conjured`. 43:3.
- ἐπερώτησις — `the questioning and consulting`. 43:7.
- ἐκδέχομαι — **headword** `I take`; **chain** `I take or receive from, I take up, I take up the
  argument, I wait for and expect, I await, I come next`. The lexicon's *or* stands where the
  *from another* that follows belongs to both verbs. 43:9.
- βραδύνω — **headword** `we made slow`; **chain** `we made slow and delayed, we were delayed, we
  were long and loitered and delayed`. 43:10.
- κάρυον — `nuts, walnuts, chestnuts`. 43:11.
- ῥητίνη and μέλι — one translation each, *the resin of the pine* and *honey* (`MARKUP_LOST`,
  "Lat. mel, honey"): plain text. 43:11.
- δισσός — `two-fold and double, two, double and divided and doubtful`. 43:12.
- ἀγνόημα — `a fault of ignorance and an error`. 43:12.
- μήποτε meaning *perhaps*, with the indicative — the corpus chain of 3:22, `that at no time,
  lest ever, never, on no account, perhaps`. 43:12.
- θῦμα — **headword** `things which are slain`; **chain** `things which are slain or offered,
  victims, sacrifices, offerings`, the lexicon's *or* kept where *offered* is no gloss by itself.
  43:16.
- ὁμομήτριος — one translation, *born of the same mother*: plain text, `the born of the same
  mother` after its article. 43:16, 43:29.
- συκοφαντέω (articular infinitive) — `of the accusing falsely`; **chain** to *of the giving false
  counsel*, without the passive's *to be falsely accused*. 43:18.
- πυλών — `in the gateway, the gate-house`, merged with ἐν. 43:19.
- σταθμός — Middle Liddell writes "a standing place for animals, Lat. stabulum, a stable, fold",
  and the Latin element took the English; `MARKUP_LOST` restores *a stable, fold* as the second
  sense. `in standing place, stable and fold, stye, dwelling and abode, quarters and lodgings,
  station, day's journey and day's march, upright post and bearing pillar, door-post, balance,
  weight`, merged with ἐν. *By weight* is the dative's idiom, in `NOT_SENSES`. 43:21.
- ἵλεως — LSJ, which files the Attic ἵλεως under the epic ἵλαος; Middle Liddell has neither:
  `propitious and gracious, propitious and blameless and atoned for, gracious and kindly`. 43:23.
- θησαυρός — `stores laid up and treasures, store-houses and treasure-houses and magazines,
  treasuries of a temple, receptacles, chests and caskets`. 43:23.
- εὐδοκιμέω — `being of good repute and held in esteem and honoured and famous and popular, being
  distinguished, having influence`. 43:23.
- ἀπέχω (active) — **headword** `I keep off`; **chain** `I keep off or away from, I keep apart and
  part, I am away or far from, I am distant, I am far from, I have or receive in full`. The
  middle's *to hold oneself off, abstain, desist from* is set aside by the form (`FORM_SENSES`),
  and *to be as far*, a piece of the example *to be as far as possible from*, by `NOT_SENSES`.
  43:23.
- ἀριστάω — `to take breakfast or luncheon`, one gloss. 43:25.
- κύπτω — `having bent forward and stooped down, having hung the head from shame, having bowed
  down under a burden`. 43:28.
- συστρέφω (imperfect, middle or passive) — **headword** `was being twisted up into a ball`; the
  active's transitive senses in the passive, *rally* and the passive's own *unite, club together,
  conspire* as they stand: `…, was being collected, was rallying, was being wheeled, was being
  turned, …, was being compressed`. 43:30.
- ἔντερον — `the intestines and pieces of gut, the guts, the guts and bowels`. 43:30.
- ταμιεῖον — `the treasury, the magazine`. 43:30.
- νίπτω (aorist middle participle) — `having washed one's hands`, the middle chain of 24:32. 43:31.
- ἐγκρατεύομαι — LSJ, citing this verse: `exercised self-control, forced himself, starved himself,
  was a member of the Encratite sect`. 43:31.
- συνδειπνέω (articular participle) — `to the ones dining or supping with, to the ones dining or
  supping with others, to the members of a picnic party`. 43:32.
- συνεσθίω — LSJ, one translation, *eat together*: plain text. 43:32.
- βδέλυγμα — `an abomination, an idol`. 43:32.
- πρεσβεῖον — `the gifts of honour, the privileges of age, the privileges, the rights of the
  eldest and his shares of the inheritance`. 43:33.
- πενταπλασίως — filed under πενταπλάσιος (`SPELLING`): `five-fold, five times as large as`. 43:34.
- ἵστημι — ἔστησαν is both aorists' third plural; at 43:15 it has no object, and the causal
  pattern now leaves the third plural to the intransitive, as ἀφίστημι's does: `were set`, the
  chain of 23:17 in the plural. στήσω at 43:9 is the aorist subjunctive, `I may make to stand`.

## Loose ends before Genesis 44

**Exclusions accumulate.** A word filed under another word's entry reads that entry's
`NOT_SENSES` and its own together. The loose ends before Genesis 43 had let a word's own set
replace its entry's, for νή, and that undid three others: οὐθείς, filed under οὐδείς, showed
οὐδείς's Latin *ne ullus* again (30, 31, 39, 41), πρεσβύτης showed πρέσβυς's scrap *the wise* (25),
and σῴζω, filed under the unsubscripted σώζω, lost that entry's exclusions. νή's oath sense, which
ναί's card sets aside, now stands in `KEEP_SENSES`, a table of what a word keeps from its entry's
exclusions. Before either change, a word's own set had never applied at all, so πρεσβύτης had
shown the comparative's *elder, older* and σῴζω the middle's *preserve for oneself*; the readings
already left both out.

**The εἴδω note on ὁράω.** Eleven aorists of ὁράω, 18:2 to 28:6, carried the note written for
οἶδα's pluperfect, *Middle Liddell files this under οἶδα*. They now read as the other twenty do:
*Middle Liddell files the aorist under ὁράω*.

### Words new in GEN 44

From Middle Liddell unless marked; the headword is the entry's first translation in the form the
text uses.

- πίμπλημι (aorist imperative) — `fill full of`, the active chain of 21:19. 44:1.
- κόνδυ — LSJ, one translation, *drinking-vessel*: plain text, `the drinking-vessel`. LSJ cites the
  chapter for the word as a measure. 44:2–17.
- ἀργυροῦς with its own article after the noun — `the silver`, chain `the silver and of silver`, as
  τὸ σπέρμα reads *the that which is sown*. 44:2, 44:5.
- τιμή (articular) — `the that which is paid in token of worth`, the chain of 20:16 with the
  article on every sense. 44:2.
- διαφαύσκω — one translation with a comma, *to shew light through, to dawn*: `shewed light through
  and dawned`. 44:3.
- τὸ πρωί as a subject — `the thing early in the day`, the neuter's noun before the adverb's unit,
  as 19:27 has it in the accusative. 44:3.
- ἀποστέλλω (aorist passive) — `were sent off`, `were sent away and banished`, `were sent off and
  despatched`: the transitive senses, without the intransitive *go away, depart*. 44:3.
- ἀπέχω (aorist, intransitive in use) — `kept off`, the chain of 43:23 in the third plural. 44:4.
- μακράν — **headword** `a long way`; **chain** `a long way and far and far away, far from, at
  length, long`. `NOT_SENSES` drops the repeated *far* of an example and the comparative's and
  superlative's *to a greater distance* and *as far as possible*. 44:4.
- ἐπιδιώκω — one translation, *to pursue after*: plain text. 44:4.
- καταλαμβάνω (future middle) — `you will seize upon`, the chain of 31:23. 44:4.
- ἀνταποδίδωμι — **headword** `you gave back`; **chain** `you gave back and repaid and tendered in
  repayment or requital, you made a return, you made correspondent, you answered to and
  corresponded with, you gave back words and answered, you delivered in turn`. *requital* is the
  other half of an *or*; the last *to give back*, of a sound, repeats the first. 44:4.
- οἰωνισμός — LSJ "= foreg.", pointing to οἴωνισμα, *omen from the flight or cries of birds*: one
  translation, plain text, `to omen from the flight or cries of birds`. 44:5, 44:15.
- οἰωνίζομαι — **headword** `takes omens from the flight and cries of birds`; **chain** adds
  *divines from omens and augurs*; the future, `will take omens …`. 44:5, 44:15.
- συντελέω (perfect, middle or passive, with an object) — `you have brought quite to an end and it
  stands so`, the four senses 18:21 gives the voice. 44:5.
- θηριόβρωτος — LSJ "= θηρόβορος", *eaten or torn by wild beasts*: one gloss, plain text. 44:28.
- ἐκκρέμαμαι — Middle Liddell prints the passive at the end of ἐκκρεμάννυμι (`SPELLING`).
  **Headword** `is hung from`, the first sense in the passive; **chain** `is hung from or upon,
  hangs on by and clings to, is devoted to, hangs from and depends upon`, the passive's own senses
  after it. 44:30.
- ἐπιμελέομαι — **headword** `I take care of`; **chain** `I take care of and have charge of and have
  the management of, I take care that, I give heed and attend, I am curator of`. 44:21.
- δύο — plain `two`; *two and two* is the doubled δύο δύο's, set aside in `NOT_SENSES` (Q29). 44:27.
- παραμένω — **headword** `I will stay beside`; **chain** `I will stay beside or near and stand by,
  I will remain faithful, I will stand my ground and stand fast, I will remain with, I will stay,
  I will stay behind or at home, I will survive and remain alive, I will endure and last`. *trusty*
  glosses the slave's name Παρμένων and is in `NOT_SENSES`. 44:33.
- οἰκέτης (singular) — `house-slave and menial`, the senses of 9:25 without the article. 44:33.
- ἐν τῷ ἰδεῖν — `in the seeing`, merged with ἐν, as 11:2's ἐν τῷ κινῆσαι. 44:31.
- γυνή and τίκτω — the corpus chains, `the woman … the mortal woman` and `brought into the world …
  begot, produced and yielded`; the drafts' shorter keys were stale. 44:27.
- γῆρας, ἐπιδιώκω, κόνδυ, οἰωνισμός, θηριόβρωτος — one translation each: plain text.

### Words new in GEN 45

From Middle Liddell unless marked; the headword is the entry's first translation in the form the
text uses.

- ἀνέχω (present middle) — **headword** `to hold up what is one's own`; **chain** `to hold up what is
  one's own, to hold oneself up and bear up and hold out, to bear up against, to suffer`. The
  middle takes only the entry's middle senses (`FORM_SENSES`): the active's holding up and rising,
  the aorist imperative's *be of good courage* and the participle's *with patience* are not its. 45:1.
- παρίστημι (perfect participle) — `of the ones having stood by`, the chain of 18:8 with the
  perfect's *and standing so*. 45:1.
- ἀναγνωρίζω — LSJ, citing 45:1 for the passive: **headword** `was being recognized`; **chain**
  `was being recognized, was recognizing or coming to the knowledge of, was revealing himself and
  making himself known, was causing to recognize and revealing himself to`. 45:1.
- κλαυθμός — one translation, *a weeping*: plain text, `of weeping`. 45:2.
- ἀκουστός — `heard`, `heard and audible, that should be heard`. 45:2.
- λυπέω (present imperative, middle or passive) — `be given pain`, the active's senses in the
  passive and the passive's own *grieve about, feel pain* after them. 45:5.
- φαίνω (aorist passive imperative) — `let be brought to light`, the chain of 21:11. 45:5.
- λοιπός — `remaining and the rest, it remains, what remains, the future, for the future,
  henceforward and hereafter, the rest, further and besides`; *quod superest* is Latin and in
  `NOT_SENSES`. 45:6.
- ἀροτρίασις — LSJ "= sq.", ἀροτριασμός, *ploughing, tillage*: `ploughing and tillage`. 45:6.
- ἄμητος — `reaping and harvesting, slaughter, harvest and harvest time, crop, harvest reaped`. 45:6.
- κατάλειμμα — LSJ, one translation, *remnant*; κατάλειψις, one translation, *a leaving behind*:
  plain text, without the article. 45:7.
- ἐκτρέφω — `to bring up from childhood and rear up`; *for oneself*, the middle's piece, is in
  `NOT_SENSES`. 45:7, 45:11.
- ἄρχων (anarthrous) — `ruler and commander and chief and captain, chief magistrate`, the chain of 42:6. 45:8.
- ἐγγύς — `hard by`, the chain of 19:20. 45:10.
- βοῦς with a feminine article — `the bullocks`, the word's chain; the note gives *cows*. 45:10.
- ἐκτρίβω (aorist passive) — `you may be rubbed out`, the active's senses in the passive. 45:11.
- βλέπω — `see and have the power of sight, look, look longingly and expect eagerly, look to, beware
  of, see that, see and behold, see the light of day and live, are alive and live`; the examples'
  pieces are in `NOT_SENSES`. 45:12.
- λαλέω (articular participle, neuter) — `the thing talking`. 45:12.
- διαβοάω (aorist passive) — `was shouted out and proclaimed and published, was the common talk,
  cried out`; the middle's *to contend in shouting* is set aside by the form. 45:16.
- χαίρω (aorist passive) — `rejoiced and was glad and was delighted, rejoiced at and was delighted
  with and took delight in, was wont`. The imperative's greetings, the participle's *glad* and
  *safe*, the future's *go unpunished* and the infinitive's *to dismiss from one's mind* are set
  aside by the form; the examples' pieces are in `NOT_SENSES`. 45:16.
- θεραπεία — `the waiting on and service, …, the body of attendants and suite and retinue`. 45:16.
- γεμίζω — `fill full of and load, freight with`; examples' pieces in `NOT_SENSES`. 45:17.
- πορεῖον — LSJ: `the means of conveyance and carriages, the loads`. 45:17.
- μυελός — `the marrow, the brain, the strengthening food, the inmost part`. 45:18.
- ἅμαξα — Perseus keys Middle Liddell's entry with the smooth breathing (`SPELLING`): `wagons and
  wains, wagon-loads of, carriages of the plough, Charles' wains, Great Bears`. 45:19, 45:21, 45:27.
- παραγίνομαι (present imperative) — `be near and attend upon, be present at, …, be fully grown`, the
  eight senses of every form; it read four, `come to be beside`, until EXO 36. 45:19.
- πᾶς with its own article, τὰ πάντα ἀγαθά — `the all`, the unit carrying the article. 45:20.
- χρυσοῦς as a noun, *gold pieces* — the adjective's chain of 24:22. 45:22.
- ἐξαλλάσσω (participle) — `changing utterly, withdrawing from, removing from, changing and turning
  another way and moving back and forward, unusual`; *unusual* is the participle's own gloss. 45:22.
- ἀναζωπυρέω — `rekindled, gained fresh life and courage`. 45:27.
- κλαυθμός, ἔτος, πέντε, δέκα, τριακόσιοι, υἱός, κατάλειμμα, κατάλειψις — one translation each:
  plain text. Names new: Γεσεμ (Goshen) and Ἀραβία.

## Loose ends before Genesis 46

**One translation is one item.** Middle Liddell gives many senses as a run of words in one
translation — σταθμός *a dwelling, abode*, κιβωτός *a wooden box, chest, coffer*, πρόσωπον *the
face, visage, countenance*. The corpus had written such runs two ways, joined (`dwelling and
abode`, `race, stock and family`) and split into items of their own (`face, visage,
countenance`, `a wooden box, a chest, a coffer`). Every chain now joins the run with *and*, the
form's opening said once and the perfect's formula after the whole item: `of the face and visage
and countenance`, `the wooden box and chest and coffer`, `has talked and chatted and prattled and
babbled and it stands so`. 2,431 units in 942 chains changed, by script against each word's card;
the chains quoted in this file were brought along where they matched a changed chain exactly.

The script, `split_runs` in `build/validate.py`, joins only what it can place: the run's words on
consecutive items, in order, each item saying exactly its share of the run. It leaves alone an
item the card also gives as a sense by itself — ἀκούω's *to have hearing of*, beside *to hear of,
hear tell of*; πᾶς's *all*, beside *all, the whole*; λέγω's *say on*, beside *to say, speak* — and
two runs that reach the same item. The new check `runs` holds the rest.

Four chains were settled by hand. GEN 6:21's συνάγω had drifted from the corpus's chain (`gather in
stores`, `join` apart from `in one`) and now reads it; GEN 31:33's παιδίσκη had drifted from its
card and now reads 12:16's `young girls and maidens, young slaves and courtesans`; γυμνός at
27:16 keeps its headword `the naked parts` and joins as 2:25 does; and παύω's *one's rest*,
written `their rest` and `his rest`, is now read past by the check.

The ranges check now gives an articular participle the range of its own a word used as a noun
has: τὰ ὑπάρχοντα, `the existing circumstances`, had shared a count with ὑπάρχει, `begins`, by
coincidence, and the join parted them.

### Words new in GEN 46

From Middle Liddell unless marked; the headword is the entry's first translation in the form the
text uses. Chains already in the corpus were read from it, in their joined form.

- τέλος (anarthrous, in εἰς τέλος) — **headword** `fulfilment`; **chain** `fulfilment or
  completion, consummation and issue and result and end, end and death, point or term, at last,
  throughout and for ever and completely, …, offerings, sacred rites`, the lexicon's articles
  dropped where the Greek has none. Repetitions inside examples, the pieces *hood* and *it*, the
  phrases τέλος ἔχειν and λαβεῖν, and Cicero's *finis bonorum* are in `NOT_SENSES`. 46:4.
- ἀναβιβάζω (future) — `I will make go up`, the chain of the aorist. 46:4.
- ἐπιβάλλω (future) — `will throw`, the chain of the aorist. 46:4.
- κτῆσις (articular) — `the acquisition, the possession, the possessions and property`. 46:6.
- ψυχή (plural) — `the breaths, the lives, the spirits, life and death, the ghosts, the departed
  souls`; anarthrous, `breaths, …`. It counts persons. 46:15–27.
- ζεύγνυμι — **headword** `having yoked`; **chain** `having yoked and put to, having harnessed and
  saddled and bridled, having put to and got ready, having bound and bound fast, having joined
  together, having joined in wedlock, having joined, having formed, having undergirded`. The
  middle's *to wed* and the passive's *to be married* are set aside for the active by the form;
  the examples' pieces are in `NOT_SENSES`. 46:29.
- ἅρμα (plural) — `the chariots, the war-chariots, the chariots and horses and yoked chariots,
  the teams and horses`. 46:29.
- πολύς (comparative, πλείων) — `to more and mightier and greater, to deeper, to louder, to
  stronger, to larger and wider, to farther, to longer, to oftener`, the positive's senses in the
  comparative. 46:29.
- συναντάω (infinitive) — `to meet face to face`, the chain of the aorist. 46:28.
- κτηνοτρόφος — one translation with a comma, *keeping cattle, pastoral*: `keeping cattle and
  pastoral`. 46:32, 46:34.
- ἄγω (perfect, ἀγειόχασιν) — `have led and it stands so, have carried, have conveyed, have
  brought, have marched`. 46:32.
- θυγάτηρ, ἀδελφή, συνάντησις, κλαυθμός, γῆρας and the numerals — one translation each: plain
  text.
- Names: about fifty new, most from the lists of 46:9–24. Where the Greek gives a name the Hebrew
  spells otherwise the gloss says *for* the Hebrew form (Ζαμβραμ, for Šimrôn); where it gives Perez's
  son the name of Simeon's (Ιεμουηλ for Ḥāmûl, 46:12), the second bearer has its own entry and
  English name. Ἡρώων πόλις is glossed as Ἡλίου πόλις was, the first word a capitalised Greek noun.

## Loose ends before Genesis 47

**ἄκρον.** GEN 28:18's `the mountain-top` carried three of the eight senses Middle Liddell gives
the noun — *a mountain-top, peak*, *a headland, foreland, cape*, *an end, extremity* — and none of
*the highest pitch, height*, *exceedingly* (εἰς ἄκρον), *the highest place*, *the prize*, *the
oldest rulers*. No note set them aside, and GEN 47:31's τὸ ἄκρον τῆς ῥάβδου reads the whole card,
so 28:18 now does too: `the mountain-top and peak, the headland and foreland and cape, the end and
extremity, the highest pitch and height, the exceedingly, the highest place, the prize, the oldest
rulers`. *The exceedingly* is the article over a gloss that opens otherwise, as δεύτερος reads *the
secondly and next and afterwards*.

**σπέρμα without its article.** Eight anarthrous units (4:25, 7:3, 8:22, 15:3, 19:32, 19:34, 21:12,
21:13) read `that which is sown, the seed, the germ …`, the articles of the articular chain left in
where the Greek has none; 38:8 and the rest read `that which is sown, seed, germ and origin and
element, offspring and issue, race and descent`, and now all do. The table's row for ἐν with
σπέρμα named the head `in that which is sown`; 22:18 is ἐν τῷ σπέρματί σου, and the unit reads `in
the that which is sown`.

### Words new in GEN 47

From Middle Liddell unless marked; the headword is the entry's first translation in the form the
text uses. Chains already in the corpus were read from it.

- νομή — **headword** `a pasture`; **chain** `a pasture and pasturage, fodder and food, a feeding and
  grazing, a spreading, division and distribution`. *To spread* renders νομὴν ἔχειν, of a sore,
  whole, and is in `NOT_SENSES`. 47:4.
- ἐπίσταμαι — **headword** `you know`; **chain** `you know, you are able, you are capable, you are
  assured, you believe that, you understand, you know and are versed in, you are acquainted with,
  you know for certain and know well, you know that`. The participle's adjectival *knowing,
  understanding, skilful*, *skilled*, *versed*, and the adverb's *skilfully, expertly*, are set
  aside for the finite verb in `FORM_SENSES`. 47:5.
- βέλτιστος, with ἐν — **headword** `in the best`; **chain** `within, inside of, and by means of
  the best, the what is best, the aristocracy`. *My good friend*, ὦ βέλτιστε, the vocative's mode of
  address, is in `NOT_SENSES`. The adjective has the article; γῇ after it reads `to earth`. 47:6,
  47:11.
- προστάσσω — **headword** `placed`; **chain** `placed, posted at, attached to and assigned to,
  assigned, appointed, gave as a command and prescribed and enjoined, commanded and ordered`. The
  passive's senses are set aside for the active in `FORM_SENSES`, with *to*, a piece of *to assign
  them to his command*. 47:11.
- σιτομετρέω (LSJ; not in Middle Liddell) — **headword** `was dealing out portions of corn or
  provisions`; **chain** `was dealing out portions of corn or provisions, was holding office of
  sitometres (σιτομέτρης), was supplying with provisions and victualling`. *Corn or provisions* is one
  translation, the *or* finishing what *corn* began. The passive's *have it served out as rations*
  is not the active's. 47:12, 47:14.
- ἐρημόω (aorist and future passive) — **headword** `may be stripped bare`, `will be stripped
  bare`; **chain** `may be stripped bare and desolated and laid waste, may be bereaved, may be left,
  may be bereft of, may be set free, may be delivered from, may be abandoned and deserted, may be
  evacuated, may be kept in solitude and isolated, may be isolated from`. *Of* and *without*,
  pieces of *to bereave one of* and *to leave the oars without men*, are in `NOT_SENSES`. 47:19.
- καταδουλόω (aorist middle) — **headword** `made a slave to himself`; **chain** `made a slave to
  himself and enslaved, enslaved in mind`. The active's *to reduce to slavery, enslave* is set aside
  for the middle in `FORM_SENSES`. 47:21.
- κτάομαι (perfect) — **headword** `I have acquired`; **chain** `I have acquired and it stands so, I
  possess and have and hold`, the perfect's own senses; the present and aorist's are set aside for
  it in `FORM_SENSES`. 47:23.
- δόσις — `in a giving` with ἐν, `within, inside of, and by means of a giving, a gift`; articular,
  `the giving, the gift`. 47:22.
- ἐπιζάω — one translation, *to overlive, survive*: `overlived and survived`. 47:28.
- ἐλεημοσύνη — one translation, *pity, mercy: a charity, alms*: `pity and mercy and a charity and
  alms`. 47:29.
- ἄκρον (plural) — `of mountain-tops and peaks, of headlands and forelands and capes, of ends and
  extremities, of highest pitches and heights, of exceedingly, of highest places, of prizes, of
  oldest rulers`; articular, `of the mountain-tops …`. 47:21.
- Forms new here, each the chain of a form already in the corpus: ἥκω `we have come`; καθίστημι
  `set down` (imperative, 41:33's); ἄρχων `rulers`; κατοικίζω `remove to`; γίνομαι `have come into
  being`; εὐλογέω `having spoken well of`; σῶμα `body`, `the body`; εὑρίσκω `the thing having been
  found`; ἀγοράζω `were being in the agora (ἀγορά)`; ἀποθνήσκω `we die off`; ἐκλείπω `has left out`;
  ἵππος `of the horses`; βοῦς `of the bullocks`; ὄνος `of the asses`; ἐκτρέφω `brought up from
  childhood`; ἄρτος `in cakes`; ἐκτρίβω `we may be rubbed out`; ὑπολείπω `is left behind`; κτάομαι
  `procure for yourself`; σπείρω `we may sow`, `sow`; ὅριον `of boundaries`; ἱερεύς `of the priests`,
  `to the priests`; δόμα `gift`; ἐσθίω `were eating`; πέμπτος `the fifth`; μέρος `part`, `parts`
  (23:9's selection); σῴζω `you have saved`; πρόσταγμα `an ordinance`; ἀποπεμπτόω `to give a fifth
  part of`; κληρονομέω `received a share of an inheritance`; ἐνιαυτός `of long periods of time`;
  ὑποτίθημι `place under` (28:18's selection); ἀλήθεια `truth`; θάπτω `you will pay the last dues to
  a corpse`; αἴρω `you will take up`; τάφος `in the burial` (23:4's selection); ῥάβδος `of the rod`.
- ἔτος, υἱός, σήμερον, γένημα and the numerals — one translation each: plain text. γενήματα reads
  `the produces`, as at 41:34.

### Words new in GEN 48

From Middle Liddell unless marked; the headword is the entry's first translation in the form the
text uses. Chains already in the corpus were read from it.

- ἐνοχλέω (present, middle or passive) — **headword** `is troubled`; **chain** `is troubled and
  disquieted and annoyed, gives trouble or annoyance to, is a nuisance`: the active passivized
  first, the intransitive senses in their own voice after, as ἐπιφαίνω at 35:7. The passive's own
  *to be troubled or annoyed* says nothing the first item does not. 48:1.
- κλίνη — **headword** `the that on which one lies`; **chain** `the that on which one lies and couch,
  the bed, the bier`, the article over a gloss that opens otherwise, as `the that which is sown`. 48:2.
- ἔκγονον (MorphGNT's dictionary form; Middle Liddell files it under ἔκγονος) — **headword** `the
  offspring`; **chain** `the offspring, the born of and sprung from`. The entry gives the neuter its
  own sense, *neut. ἔκγονα, one's offspring*, and the masculine's *a child, son, daughter* and
  *descendants* are set aside for it in `FORM_SENSES`. 48:6.
- κλῆρος, with ἐν — **headword** `in the lots`; **chain** `within, inside of, and by means of the
  lots, the casting lots and drawing lots, the allotments, the pieces of land and portions and
  farms, the clergy`. *The laity*, the contrast the entry draws with the clergy, and *by lot*, the
  example's phrase, are in `NOT_SENSES`. ἐν τοῖς ἐκείνων κλήροις reads `in the lots of those`. 48:6.
- ἱππόδρομος — `the chariot-road, the race-course`; genitive, `of the chariot-road, of the
  race-course`. 48:7.
- κατορύσσω — `I buried in the earth, I buried`. 48:7.
- βαρυωπέω (LSJ; not in Middle Liddell) — *to be dim-sighted*, one translation: plain text,
  `were dim-sighted`. 48:10.
- στερέω (aorist passive) — `I was deprived, I was bereaved, I was robbed of, I was taken away`,
  split as 30:2's active is. 48:11.
- δεξιός and ἀριστερός, used as nouns — with ἐν, `in the right` and `in the left`; anarthrous
  genitive after ἐκ, `of right`, `of left`; articular, `the right`, `the left`, each over 13:9's
  range. 48:13–18.
- ἐναλλάξ — `crosswise, alternately`. 48:14.
- τρέφω (participle) — `the one thickening, …, the one maintaining and supporting`, 6:19's range;
  the first sense heads, as the rule has it, however the context reads. 48:15.
- ῥύομαι (participle) — **headword** `the one drawing to himself`; **chain** `the one drawing to
  himself, the one drawing out of danger and rescuing and saving and delivering, the one saving, …,
  the one keeping off`. *From*, a piece of *deliver us from the pollution*, is in `NOT_SENSES`. 48:16.
- βαρύς — **headword** `heavy`; **chain** `heavy, heavy with age or suffering, heavy to bear and
  grievous, heavily, burdensome and grievous and oppressive, violent, …, strong and offensive`. The
  adverb βαρέως, filed inside the entry, keeps its *ill* and *with disgust* to itself
  (`FORM_SENSES`); Homer's *notion of strength and force* is a description, and *suffering* a
  piece, set aside for the adjective's forms in the same rule, since 31:35's βαρέως reads *with
  strength and force*. 48:17.
- καταφαίνω (aorist passive) — `was declared and made known, became visible and appeared, was quite
  clear or plain`: the active passivized, then the passive's own. 48:17.
- ἀντιλαμβάνω (aorist middle) — **headword** `laid hold of`; **chain** the middle's senses, `laid
  hold of, gained or reached, helped and took part with and assisted, …, held against and held
  back`; the active's *to receive instead of* and *in turn* are set aside in `FORM_SENSES`. 48:17.
- ἐξαίρετος — Middle Liddell prints it inside the entry for ἐξαιρετός, *that can be taken out*:
  `taken out and picked out and chosen, excepted, special and remarkable`, the other word's sense
  in `NOT_SENSES`. 48:22.
- ὑπέρ + accusative — **headword** `over`; **chain** the accusative section's translations, `over
  and beyond, over and above and exceeding and beyond, beyond and contrary to, above and upwards of,
  more than, beyond, before and earlier than`. *That over and beyond which* is the section's
  description, not a translation. 48:22.
- Forms new here, each the chain of a form already in the corpus: ἐνισχύω `having strengthened`;
  καθίζω `made to sit down` (masculine, *took his seat*); γεννάω `you may beget`; ἔρχομαι `I was
  coming`; ἐγγίζω `of bringing near` (participle); εὐλογέω `I may speak well of`, `will be spoken well
  of`; βλέπω `to see`; περιλαμβάνω `seized around`; εὐαρεστέω `were well pleasing`; κακός `of the
  evils`; ἐπικαλέω `will be called upon`; πληθύνω `may they be made full`; ἀφαιρέω `to take from`;
  ἐπιτίθημι `lay`; θέλω `willed`; οἶδα `I know`; ὑψόω `will be lifted high`; ποιέω `may he make`;
  ἀποθνήσκω `I die off`; ἀποστρέφω `will turn`; μάχαιρα `in a large knife`; τόξον `to bow`; καί,
  adverbial, `also` (48:11, 48:19).
- υἱός, γῆρας, τίς and the numerals — one translation each: plain text. Βαιθλεεμ is Rahlfs's own
  spelling here, filed under Βηθλέεμ as at 35:19.

### Words new in GEN 49

From Middle Liddell unless marked; the headword is the entry's first translation in the form the
text uses. Chains already in the corpus were read from it. Jacob's blessing is poetry, and dense
with rare words; most of what is new here came with a lexicon scrap to settle.

- **From LSJ** (not in Middle Liddell): ἐρείδω, the active's senses only, `may it cause to lean and
  prop, …, may it become fixed`; νευροκοπέω, *hamstring, hough*, one translation, `hamstrung and
  houghed`, from the nu file fetched for it; ὑπερισχύω, `was exceedingly strong, was too luxuriant,
  was overbearing, was stronger than and prevailed over`. 49:6, 49:26.
- **Close forms and cross-references:** νῶτος, MorphGNT's form, is filed as νῶτον, `of back, of any
  wide surface, of plains, of back or ridge`; πρωινός reads only *later form of πρώιος*, and takes
  that entry, `the early, the early in the day and at early morn, the early in the year`; ἕλιξ, the
  vine's tendril, is Middle Liddell's second entry, the noun (`ENTRY`), not the adjective
  *twisted*. 49:8, 49:27, 49:11.
- **Lost to Latin:** ὀδούς, λέων and λύκος print their first sense inside the Latin element (*Lat.
  dens, dentis, a tooth*; *Lat. leo, a lion*; *Lat. lupus, a wolf*), restored in `MARKUP_LOST`.
  ὀδούς and λύκος then have one sense each and are plain text; λέων adds *a lion's skin*. 49:9,
  49:12, 49:27.
- **Pieces and examples set aside** (`NOT_SENSES`): ἀθροίζω, κοίτη, στρωμνή, βουλή, σύστασις, ἧπαρ
  (*pregnant*, ὑφ' ἥπατος φέρειν, leaving *the liver* alone, plain text), ἀπόκειμαι, πλύνω (λούομαι's
  *to bathe* and νίζω's *to wash the hands or feet*, glossed in the entry by contrast), περιβολή,
  πλοῖον, πίων, ἐγκάθημαι, δάκνω, περιμένω, τόξευμα, κράτος (κατὰ κράτος, rendered whole, and the
  personified *Strength, Might*), μαστός, κορυφή, λύκος, διαδίδωμι, τροφή, ἐπιτάσσω, ἡγέομαι, ἕλιξ.
- **Voice** (`FORM_SENSES`): the active forms of παρατείνω, πονέω, δάκνω, ἐπιδίδωμι, λοιδορέω, ἐνέχω,
  διαδίδωμι and ἐπιτάσσω take none of their passive's or middle's senses; ἡγέομαι's *the rulers,
  leading men* is the participle's, and the finite ἡγήσατο leaves it out.
- New chains, each the card in the form the text uses: συνάγω `be brought together`; ἀθροίζω `be
  gathered together`; ἀναγγέλλω `I may carry back tidings of`; ἀπαντάω `will move from`; ἔσχατος `of
  outermost`; ἰσχύς `strength`; τέκνον `of things borne`; φέρω `to be borne`; αὐθάδης `self-willed`;
  ἐξυβρίζω `you broke out into insolence`; ἐκζέω `you may boil out`; κοίτη `the marriage-bed`;
  στρωμνή `the bed spread`; ἀδικία `wrong-doing`; αἵρεσις `of a taking`; βουλή `will`; σύστασις `to
  the putting together`; θυμός and ἐπιθυμία with ἐν; μῆνις `the wrath`; διαμερίζω, διασπείρω (future);
  αἰνέω `may they tell or speak of`; ἐχθρός `of the one's enemies`; σκύμνος `a cub`; λέων; βλαστός `of
  sprout`; ἀναπίπτω `having fallen back`; κοιμάω `you were lulled`; ἐγείρω `will awaken`; ἡγέομαι
  `going before`, `went before`; ἀπόκειμαι `the things being laid away`; προσδοκία `a looking for`;
  δεσμεύω `fettering`; πῶλος `the foal`; ἕλιξ `to the anything which assumes a spiral shape`; πλύνω
  `will wash`; περιβολή `the anything which is thrown round`; χαροπός `glad-eyed`; παράλιος `by the
  sea`; ὅρμος `a cord`; πλοῖον `of floating vessels`; παρατείνω `will stretch out along`; ἐπιθυμέω
  `set his heart upon`; ἀναπαύω `desisting from`; κλῆρος `of the lots`; ἀνάπαυσις `the repose`; πίων
  `fat`; πονέω `the working hard`; ὄφις `serpent`; ὁδός `of way`; ἐγκάθημαι `sitting in or on`; τρίβος
  `of a worn or beaten track`; δάκνω `biting`; ἵππος `of horse`; πίπτω `will fall`; ἱππεύς `the
  horseman`; σωτηρία `the saving`; περιμένω `I wait for`; πειρατήριον `ordeal`; πούς `feet`; δίδωμι
  `will give`; τρυφή `softness`; ἄρχων `to rulers`; στέλεχος `crown of the root`; ἀνίημι `having been
  sent up` (the perfect participle passive, *and standing so*, then the intransitive senses in
  their own voice); ἐπιδίδωμι `giving besides`; κάλλος `beauty`; αὐξάνω `having been made large`;
  ζηλωτός `to be emulated`; νέος `youngest`, the superlative over 44:20's comparative range;
  ἀναστρέφω `turn upside down`; διαβουλεύομαι `discussing pro and con`; λοιδορέω `were abusing`;
  ἐνέχω `were holding within`; τόξευμα `of things which are shot`; συντρίβω `was rubbed together`;
  κράτος `of strength`; τόξον `the bows`; ἐκλύω `was loosed`; νεῦρον `the sinews`; δυνάστης `of a
  lord`; κατισχύω `the one having had power over`; βοηθέω `came to aid`; ἐμός `the mine`; ἔχω `of
  having`; εὐλογία `of good language`, `to good languages`; μαστός `of ones of the breasts`; ὄρος
  `of mountains`; μόνιμος `of staying in one's place`; θίς `of heaps`; ἀέναος `of ever-flowing`;
  κορυφή `of head`; ἅρπαξ `rapacious`; διαδίδωμι `will give from hand to hand`; τροφή `nourishment`;
  προστίθημι `I am put to`; κτῆσις with ἐν; σπήλαιον `of the grotto`; εἰμί `of the thing being`;
  θάπτω `I paid the last dues to a corpse`; ἐπιτάσσω `putting upon as a duty`.
- One translation each, plain text: υἱός, ἧπαρ, ταῦρος, ἐπικατάρατος (*yet more accursed*),
  σκληρύνω, ἄμπελος, οἶνος, ὀδούς, γάλα, ὦμος, πειρατεύω, γένημα, βραχίων, μήτρα, λύκος, δώδεκα.

### Words new in GEN 50

From Middle Liddell unless marked; the headword is the entry's first translation in the form the
text uses. Chains already in the corpus were read from it.

- **From LSJ** (not in Middle Liddell): ἐνταφιαστής, *undertaker, embalmer*, one translation,
  `the undertakers and embalmers`; πανοικία, *whole household*, plain text in the nominative; its
  dative's *with all the house* is the dative's, by `FORM_SENSES`, which LSJ words now take (Q3); συναναφέρω, the active's senses, `you will carry up together, you
  will bring up together with yourselves, …, you will report`. 50:2, 50:8, 50:25.
- **Cross-references:** ἅλων reads only *= ἅλως found in the obl. cases*, and takes that entry, `a
  threshing-floor, disk`; κοπετός reads only *= κομμός*, `a striking, a beating of the breast in
  lamentation, a wild lament`. 50:10, 50:11.
- **Lost to Latin:** κομμός, "like Lat. planctus (from plango), a beating of the breast in
  lamentation": the `<tr>` opens inside the Latin parenthesis and carries *plango),* with it.
  `MARKUP_LOST` restores the English whole, under the entry's key `kommo/s1`, and `NOT_SENSES` sets
  the broken piece aside.
- **Lost to Greek:** ἐπισκοπή's *the office of ἐπίσκοπος* (`GREEK_LOST`), `to the office of
  episkopos (ἐπίσκοπος)`. 50:24, 50:25.
- **Voice and tense** (`FORM_SENSES`): θνήσκω's perfect takes *to be dead*, the entry's sense *in
  aor2 and perf.*, not the present's *to die, be dying*; the metaphorical *to die, perish* has no
  tense given and stays, `is dead, has died and perished and it stands so`. ἐνδείκνυμι's middle
  takes the Mid. senses and *to inform against*, given *so in Mid.*, `we informed against, we
  shewed forth ourselves, …, we courted`. βουλεύω's middle takes sense I, which *in Prose belongs
  chiefly to the Mid.*, and the Mid. senses, `you took counsel and deliberated and concerted
  measures, you had considered, …, you determined with yourselves and resolved on`.
- **Number:** ταφή's *a burial-place* is given *in pl.*, and the singular of 50:3 leaves it out,
  `of the burial, of the mode of burial, of the payment for burial and burial-fee`.
- **Pieces set aside** (`NOT_SENSES`): συναναβαίνω (*or together*, and τινί *with* one), which
  leaves one translation, *to go up with*; πατρικός (*of*, half of *of or belonging to*);
  μνησικακέω (the examples' *to bear … malice*, *a grudge for*, *to remind … of the ills*); πέραν
  (τὰ πέραν's *done on the opposite side*, ἡ πέραν γῆ's *just over the border*, *border-*); ταφή
  (Sophocles' urn).
- New chains, each the card in the form the text uses: πληρόω `made full`; καταριθμέω `are counted`,
  with the middle's `recount and enumerate` in its own voice; πενθέω `bewailed`; πένθος `the grief`,
  `grief`; δυνάστης `the lords`; μνημεῖον with ἐν; ἐπανέρχομαι `I will go back`, keeping *to go up*
  beside *to go up, ascend* and *pass*, a verb of its own in *to go up or pass from one place to
  another*; πρεσβύτερος `the elders`; οἰκία `the building`, `the buildings`; πατρικός `the derived
  from one's fathers`; συγγένεια `the sameness of descent`; ὑπολείπω `they left remaining for
  themselves`; ἅρμα `chariots`; ἱππεύς `horsemen`; παραγίνομαι `were near`; κόπτω `beat their
  breasts`; πέραν `on the other side`; μνησικακέω `may remember wrongs done one`; ἀνταπόδομα
  `repayment`; ἀνταποδίδωμι `may give back`; τελευτάω `of the completing`, `completed`; θεράπων `of
  the waiting-men`; παρακαλέω `called to`; τρίτος `of third`; γενεά `of race and stock and family`;
  τίκτω `were brought into the world`; μηρός `of thighs`; ἐπισκέπτομαι `will look upon`; ἀνάγω `will
  lead up`; πατήρ `to the fathers`; ὀστέον `the bones`; σορός with ἐν, `in the vessel for holding`.
- One translation each, plain text: ἐνταφιάζω (*to prepare for burial*), κάτοικος (*a settler*),
  διατρέφω (*to sustain continually*), πανοικία, συναναβαίνω — plain at 50:7 too, where ἀνέβη's unit
  heads with *went up*: a plain run that is a word's one translation is its own English (Q19).
- Names: Αταδ (from Hebrew ʾĀṭād, *bramble, thornbush*), and Πένθος, the name of 50:11, *Πένθος
  Αἰγύπτου*, `Mourning`, the Greek of ʾĀbēl Miṣrayim; the first Πένθος of the verse is the common
  noun, capitalised as the start of speech.

## Exodus

### Words new in EXO 1

From Middle Liddell unless marked; the headword is the entry's first translation in the form the
text uses. Chains already in the corpus (Genesis) were read from it and re-inflected.

- **From LSJ** (not in Middle Liddell): χυδαῖος `poured out in streams and abundant, common and
  ordinary, common and vulgar and coarse` (1:7); κατοδυνάω, *afflict grievously*, one translation,
  plain text (1:14); πλινθεία `to the brickmaking, to the drawing up of an army in square` (1:14);
  ζωογονέω `were propagating, …, were preserving alive`, *= ζωγρέω, preserve alive* last (1:17, 1:18,
  1:22), from the zeta file, `eng7`, fetched for it.
- **Tense, voice, number and case** (`FORM_SENSES`): ἐφίστημι is causal in the present, imperfect,
  future and first aorist, intransitive in the perfect, pluperfect and second aorist, as ἵστημι —
  ἐπέστησεν `set and placed upon, set over, …, arrested the attention`; the perfect's card now
  matches GEN 24's chain, which had kept only the intransitive. κατασοφίζομαι's middle leaves out
  the passive *to be outwitted*. τοσοῦτος in the singular leaves out *in pl. so many*. βία's
  *against one's will, in spite of* and *perforce* are the dative's, βίᾳ — the form cannot show the
  case once the iota subscript is stripped, so a `FORM_SENSES` rule now takes a fifth item, a
  pattern the parse code must show (`^....D`).
- **Cut translations restored** (`MARKUP_LOST`): ἐπιστάτης's *a training-master* (the `<tr>`s stop
  either side of *training-*), βία's *against one's will, in spite of* (*one's* between two
  `<tr>`s).
- **Pieces set aside** (`NOT_SENSES`): ἐπιστάτης (παραστάτης's and προστάτης's glosses, *the right-
  or left-hand man*, *the front-rank man*); τοσοῦτος (the phrases with prepositions, *so far*, *in
  the meantime*, and the examples' *so*, *as large*).
- **Joined *or*-pieces**, as the corpus joins them in ἐφίστημι's perfect (*stood by and near*):
  κατασοφίζομαι `let us conquer by sophisms and fallacies and outwit`; ἐπιστάτης `ones who stand
  near and by and suppliants`; ἐφίστημι `set and placed upon`, `set by and near to`. See
  open-questions.md, Q2.
- New chains: εἰσπορεύομαι `of the ones having gone into` (perfect); κατισχύω `were having power
  over`; πληθύνω `was making full`, `may be made full`; ἔθνος `to the number of people accustomed to
  live together`; προστίθημι `will be put to`; ὑπεναντίος `the ones set over against and meeting`;
  ἐκπολεμέω `having excited to war`; κακόω `may treat ill`; πόλις `cities`; ὀχυρός `firm`; ταπεινόω
  `were lowering`; τοσοῦτος `to so large`; πολύς `more` (the comparative); γίνομαι `were coming into
  being`; ἰσχύω `were being strong`, `was being strong`; βδελύσσομαι `were feeling nausea`; βία `to
  bodily strength`, `of bodily strength`; σκληρός `to the hard`; πηλός `to the clay`; ἔργον `to the
  works`; πεδίον with ἐν, plural; καταδουλόω `were being reduced to slavery` (imperfect
  middle/passive: the passive, then the middle's own); μαῖα `the good mothers`, `to the good
  mothers`; τίκτω `to the bringing into the world`, `bring into the world`, `were bringing into the
  world`, `may be brought into the world`; περιποιέω `keep` (the middle); ἄρσην `the male`;
  φοβέομαι `were being put to flight`; ῥίπτω `throw`.
- πανοικίᾳ, the dative, a unit: `to whole household, with all the house`, the dative's own English
  unmarked (Q3, Q4).
- One translation each, plain text: πέντε, καθότι (*in what manner*), καταδυναστεύω (*to exercise power over*), κατοδυνάω, μαιόομαι
  (*to deliver*).
- Names new to the corpus: Πιθωμ, Ων, Σεπφωρα (Shiphrah), Φουα (Puah, the midwife — GEN 46:13's
  Φουα is Issachar's son, and the morphology says so).

### Words new in EXO 2

- **From LSJ** (not in Middle Liddell): θῖβις, *basket* plaited from papyrus, one translation, plain
  text; καταστενάζω `sighed and mourned`; καταχρίω `anointed and smeared and coated`; τροφεύω
  `serving as a wet-nurse and suckling`; ἀσφαλτόπισσα, LSJ's pointer *= πισσάσφαλτος*, followed to
  *compound of asphalt and pitch*, one translation, plain text — as θηριόβρωτος at GEN 44. All cite
  this chapter.
- **Voice** (`FORM_SENSES`): ἀναιρέω's active and middle, each without the other's — the middle
  `took up for herself and took up, …, took back to herself and cancelled` (2:5, 2:10), the active
  `to take up and raise, …, to answer and give a response` (2:14, 2:15); GEN 4's card loses the
  middle's senses, which its chain never had. λούω's middle, *to bathe*, plain text. τύπτω's active,
  `beating and striking and smiting`. ἐκδίδωμι's middle, *to give one's daughter in marriage … so in
  Mid.*, `gave in marriage`.
- **Lost to Latin** (`MARKUP_LOST`): ἀστεῖος, *like Lat. urbanus, town-bred, polite, courteous*, the
  English inside the Latin element: `of the town, town-bred and polite and courteous, refined and
  elegant and pretty and witty and clever`.
- **Pieces set aside** (`NOT_SENSES`): ἀστεῖος (the ironic *a pretty piece of luck*), μανθάνω (*by
  inquiry*, *learners, pupils*, the idioms of examples), δικαστής (*judices*, and ὁ κριτής's *presiding
  judge*), ἐμφανής (examples' pieces, and the adverb's senses), βοή (examples' pieces), τύπτω, λούω
  (νίζω's and πλύνω's glosses, examples, the Latin).
- **The participle as a noun:** τὸ ἀποβησόμενον (2:4) reads the entry's noun senses for ἀποβαίνω's
  participle, `the issue and event, the results, the probable results`, as τὰ ὑπάρχοντα at GEN 12:5.
- **παραγίνομαι** in the articular infinitive takes the eight senses of `were near` (GEN 50:16), not
  the four of `come to be beside`: one range in every form.
- New chains, re-inflected from the corpus: ἔχω `had`; κρύπτω `to hide`; κατασκοπεύω `was viewing
  closely`; μανθάνω `to learn`; ἀνοίγω `having opened`; κλαίω `weeping`; φείδομαι `spared`; θέλω `you
  will`; καλέω `I may call`, `call`; θηλάζω `will suckle`, `suckle`, `was suckling`; νεᾶνις `the young
  woman`; διατηρέω `watch closely`; ἁδρύνω `of having been made ripe`; πολύς `to the many`, `the
  many`; γίνομαι `having come into being`; κατανοέω `having observed well`; πόνος `the work`;
  περιβλέπω `having looked round about`; πατάσσω `having beaten`; ἄμμος with ἐν; διαπληκτίζομαι
  `sparring with`; ἀδικέω `to the one doing wrong`; πλησίον `the neighbour`; δικαστής `a judge`;
  ἐμφανής `shewing in`; ἀναχωρέω `went back`; ἱερεύς `to the priest`; ἀντλέω `were baling out
  bilge-water`, `baled out bilge-water`; δεξαμενή `the reservoirs`; ῥύομαι `drew to himself`; ταχύνω
  `you made quickly`; καταλείπω `you have left behind`; κατοικίζω `was removed to`; ἀλλότριος `to
  belonging to another`; βοή `the loud cry`; γινώσκω `was learned to know` (the passive, with the
  passive's own *to be pronounced*); ἕλος `the low ground by rivers`, with ἐν.
- One translation each, plain text: θυγάτηρ, ἀδελφή, τρεῖς, ἅβρα
  (*favourite slave*), ἐχθές, σήμερον, θῖβις, ἀσφαλτόπισσα, λούω's middle.
- Names new to the corpus: Μωυσῆς (from Hebrew Mōšeh, which 2:10 hears in māšâ, *to draw out*; the
  Greek gives *from the water* and loses the play), Ιοθορ (Jethro, which the Greek adds at 2:16),
  Σεπφωρα the wife (Zipporah — the midwife of 1:15 has the same Greek), Γηρσαμ. Εβραῖον, the singular,
  is glossed apart from Εβραίων: the panels print *Hebrew* and *Hebrews*.
- **GEN 4:15 widened:** its ἀναιρέω, `of the taking up`, had five of the active's nine senses, two of
  them cut from one translation (*to take up, raise*); it now carries the whole active range, as
  `to take up` at 2:14 does — one word, one range in every form.
- **The page's own misprint:** ἐξήλθεν at 2:11, with the acute, for ἐξῆλθεν; kept, and the module
  has it too.

### Words new in EXO 3

- **From LSJ** (not in Middle Liddell): θλιμμός, LSJ's *= θλῖψις*, followed to θλῖψις (LSJ, GEN 35),
  `the pressure, the crushing and castration, the oppression and affliction`; ἐργοδιώκτης,
  *taskmaster*, plain text; κατεμβλέπω, *strengthd. for ἐμβλέπω*, followed to LSJ's ἐμβλέπω, with
  the entry's own *look down upon, despise* after it (open-questions.md, Q5).
- **Close form:** προΐημι is Middle Liddell's `proi/hmi`, without the diaeresis (`SPELLING`).
- **Voice** (`FORM_SENSES`): προΐημι's middle, *to send forward from oneself … to utter … to give up,
  let go*, `will send forward from himself, …, will neglect all advice and be reckless`; θλίβω's
  and αἰτέω's actives; ῥέω's present, without the causal aorist's *to let flow, pour*.
- **Lost to Greek** (`GREEK_LOST`): εὐλαβέομαι, *to behave like the εὐλαβής*, `was behaving like
  the eulabes (εὐλαβής)`.
- **Pieces set aside** (`NOT_SENSES`): καίω, κάκωσις, ῥέω, θλίβω, αἰτέω, γείτων, σκυλεύω, εὐλαβέομαι —
  examples' pieces, Latin, Virgil. ὑπόδημα's *half-boot* is not one: *a shoe or half-boot* is a
  sense, and GEN 14:23's chain, which had *half-boot* without *a shoe*, now reads `of a shoe and
  half-boot`.
- **The article over the participle of εἰμί:** ὁ ὤν, 3:14, `the one being, the one existing`, as
  εἰμί's own formula; the εἰμί unit stands outside the unit rule.
- New chains, re-inflected from the corpus: γαμβρός `of the one connected by marriage`; ἱερεύς `of
  the priest`; φλόξ with ἐν; βάτος `the bramble-bush`; καίω `is lighted`; κατακαίω `was being burned
  down`, `is burned down`; παρέρχομαι `having gone by`; ὅραμα `the that which is seen`; προσάγω
  `brings to` (the corpus's four senses, without the intransitive *to draw near* — Q1); ἐγγίζω `you
  may bring near`; λύω `loose` (the whole card, as GEN's `having loosed`); ὑπόδημα; πούς `of the
  feet`; ἵστημι `you have been set`; ἅγιος `devoted to the gods`; κάκωσις `the ill-treatment`, `of
  the ill-treatment`; κραυγή `of the crying`, `a crying`; ἀκούω `I have heard`; ὀδύνη `the pain of
  body`; καταβαίνω `I stepped down`; ἐξαιρέω `to take out for oneself`; ἐξάγω `to lead out`, `you
  will lead out`, with ἐν; εἰσάγω `to lead in`; ἀγαθός `good` (the adjective's senses); πολύς `much
  and mighty and great`; ῥέω `flowing`; θλίβω `press`; πορεύομαι `I will be driven`, `let us be
  driven`; ἐξαποστέλλω `I send quite away`, `will send quite away`; λατρεύω `you will work for hire`;
  ἔρχομαι `I will come`; ἀποστέλλω `has sent off`; ἐρωτάω `they will ask`; μνημόσυνον `a
  remembrance`; γενεά, plural; συνάγω `bring together`; γερουσία `the Council of Elders`, the
  lexicon's capitals; ὁράω `has been seen`; ἐπισκέπτομαι `I have looked upon`; συμβαίνω `has stood
  with the feet together`; εἰσακούω `they will hearken`; εἰσέρχομαι `you will go in`; προσκαλέω `has
  called to himself`; ὁδός `way`; θύω `we may offer`; κραταιός `of strong`; πατάσσω `I will beat`;
  θαυμάσιος `to the wonders` (the noun's senses, with the article); ἀποτρέχω `you may run off`;
  ἀπέρχομαι `you will go away`; αἰτέω `will ask`; γείτων `of one of the same land`; σύσκηνος `of one
  who lives in the same tent`; σκεῦος `vessels`; ἐπιτίθημι `you will lay`; σκυλεύω `you will strip`.
- One translation each, plain text: ἐνώπιον (*face to face*), γάλα, μέλι, ἐργοδιώκτης.
- Names new to the corpus: Χωρηβ (Horeb); the vocative Μωυσῆ.

### Words new in EXO 4

- **From LSJ** (not in Middle Liddell): βραδύγλωσσος, *slow of tongue*, plain text (4:10).
- **Close form:** χρόα, LSJ's *v. χροιά*, is Middle Liddell's χροιά (`SPELLING`): `the surface of a
  body and the skin and the body, the superficial appearance, the colour, the colour of the skin and
  the complexion`.
- **Cut translation restored** (`MARKUP_LOST`): ἐπιλαμβάνω's middle, *to hold oneself on by, lay hold
  of, catch*, with *on* between two `<tr>`s. GEN 25:26's ἐπειλημμένη, whose chain had split the two
  halves, now reads `having held herself on by and laid hold of and caught and standing so, …`.
  The verb is filed under ἐπιλαμβάνομαι, as GEN 25:26 files it.
- **Voice and number** (`FORM_SENSES`): ἐπιλαμβάνομαι's middle and middle/passive take the middle's
  senses only; προχειρίζω's middle, *as Dep. … to take into one's hand, prepare for oneself, to
  choose, elect, to determine*; ψῆφος's singular leaves out *in pl. accounts*. ζάω's rule now tells
  the third plural ζῶσιν from the participle's feminine ζῶσα, which share ζωσ-: the finite form
  had been reading the participle's *living, alive*.
- **Latin throughout** (`LATIN_ONLY`): τέρας, *Lat. portentum, prodigium*, after its English.
- **Pieces set aside** (`NOT_SENSES`): κωφός (examples' pieces; *dumb, mute* stays), τυφλός (*back*,
  an example's), ψῆφος (examples' translations, the proverb *calculus Minervae*, the note on ballot
  and lot), ἐπιλαμβάνω (pieces, Virgil).
- New chains, re-inflected from the corpus: πιστεύω `may trust`, `will trust`; εἰσακούω `may
  hearken`; ῥίπτω `throw`, `threw`; ἐκτείνω `stretch out`; ἐπιλαμβάνομαι `hold yourself on by`,
  `held himself on by`; εἰσφέρω `carry into`; κόλπος `of the bosom`; χιών `snow`; ἀποκαθίστημι `was
  re-established` (the intransitive second aorist); χρόα; σημεῖον `of the sign`, `to the signs`,
  `the signs`; ἔσχατος `of the outermost`; λαμβάνω `you will take`, `you may take`; ἐκχέω `you will
  pour out`; ξηρός `the dry`; τρίτος `of the third`; ἄρχω `you began`; ἰσχνόφωνος `checked in one's
  voice`; στόμα `mouth`; κωφός `blunt`; βλέπω `seeing and having the power of sight`; τυφλός
  `blind`; ἀνοίγω `I will open`; συμβιβάζω `I will bring together` (the active, without the
  passive's *to be joined*); μέλλω `you think of doing`; προχειρίζω `take into your hand`; δύναμαι
  `being able`; ἀποστέλλω `you will send off`; θυμόω `having been wroth`; ἐπίσταμαι `I know`; λαλέω
  `will talk`; χαίρω `will rejoice`; προσλαλέω `will talk to` (*to talk to or with*, joined);
  ῥάβδος `the rod`; στρέφω `the one having turned itself`; γαμβρός `the one connected by marriage`;
  ζάω `live`; ὑγιαίνω `being sound`; θνήσκω `are dead`; ζητέω `the ones seeking`; πορεύομαι `of
  being driven`; ἀποστρέφω `of turning`; τέρας `the signs`; ἐξαποστέλλω `may send quite away`, `to
  send quite away`; λατρεύω `may work for hire`; βούλομαι `you will`; ἀποκτείνω `I will kill`, `to
  kill`; κατάλυμα with ἐν; ψῆφος `a small stone`; ἀκροβυστία `the foreskin`; πούς `the feet`;
  ἵστημι `was set` (the intransitive second aorist ἔστη).
- One translation each, plain text: κέρκος (*the tail*), δύσκωφος (*stone-deaf*), βραδύγλωσσος,
  συνάντησις (*a meeting*), σκληρύνω (*to harden*), περιτομή (*circumcision*), ἀλλήλων.
- Names new to the corpus: Ααρων (Aaron), Λευίτης (the Levite).

### Words new in EXO 5

- **From LSJ** (not in Middle Liddell): πολυπληθέω, `multiplies, abounds` (5:5); πλινθουργία, LSJ's
  pointer to πλινθεία 1, *brickmaking*, plain text (5:7); βδελύσσω, the active of 5:21, which
  Middle Liddell's middle βδελύσσομαι does not cover: LSJ's causal *cause to stink, make loathsome
  or abominable*, `you caused to stink and made loathsome and abominable`, as διαναπαύω reads LSJ.
- **Cut translations restored** (`MARKUP_LOST`): ἀπολείπω, *to leave one in the lurch*; σχολάζω,
  *to have rest or respite from*, *to have leisure or opportunity for*; ἀφαιρέω, *to have it taken
  from one*. Each had a word outside the `<tr>` between or before its pieces.
- **Voice** (`FORM_SENSES`): ἀπολείπω's active leaves out the middle and the passive; διαστρέφω's
  active the passive; ἀφαιρέω's passive the middle, and the present ἀφαιρεῖται of 5:11, with οὐθέν
  its subject, is read as passive: `is taken from and taken away from, is removed, is separated and
  set aside, is robbed and deprived, has it taken from one`.
- **Pieces set aside** (`NOT_SENSES`): φόνος (an example's, a repeat, pieces, the pair *murder and
  manslaughter*), καλάμη (examples' repeats, what the metaphor means, a piece of *wheat-straw*),
  μεριμνάω (*cares*, an example's object), οὐκέτι (*(not yet)*, οὔπω's), καθήκω (examples'
  translations: *came*, *is come*, *comes*, *duty it is*).
- **The participle of καθήκω** opens the entry's participle senses as well as the verb's: τὰ καθήκοντα
  `the things having come and gone down, …, the regular and proper, …, the things which are meet and
  fit and proper and one's due and duty, the present state of things and circumstances`; τὸ καθῆκον
  the same in the singular. A finite form leaves the participle's senses out (`FORM_SENSES`),
  as GEN 19:31 καθήκει's chain already did; cleaning the card had put the two in one group.
- **The chain check** now compares two units of one lemma and headword only where the lexicon gives
  their forms the same card. δίδωμι's present stem has *to be ready to give, to offer* and its aorist
  has not, so διδόναι (5:7) and δοῦναι (5:21) are both `to give` and read different ranges; the
  ranges check already grouped by card.
- New chains: ἑορτάζω `may keep festival and holiday, may celebrate as and by a festival`;
  εἰσακούω `I will hearken`; θάνατος `death`; φόνος `murder and homicide and slaughter, blood shed in
  murder and gore, a corpse, a death`; διαστρέφω `you turn different ways and twist about and
  distort, you distort and pervert`; καταπαύω `let us lay to rest`; γραμματεύς `the secretaries and
  clerks`; οὐκέτι `no more and no longer and no further`; δίδωμι `to give` (present), `is given`,
  `was being given`, `will be given`; ἄχυρον `husk`, `the husk` (the singular); σύνταξις `the putting
  together and arranging and arrangement and organisation and order, the rule, the systematic
  treatise, the narrative, the grammatical construction and syntax, the body of troops, the
  contingent, the covenant and contract, the assigned impost and contribution, the payment and
  allowance and pension`, and its plural; σχολάζω `they have leisure`, `you have leisure` (twelve
  senses); κράζω `have croaked … and it stands so`; βαρύνω `let be weighed down`; μεριμνάω `let them
  care for`; κατασπεύδω `were pressing and urging and hastening on`; καλάμη `stalk and straw of corn,
  stalk without the ear and stubble, remains`; μαστιγόω `were whipped and flogged`, `have been
  whipped and flogged and it stands so`; καθίστημι `the ones having been set down`; ἐπιστάτης `of the
  ones standing near`; καταβοάω `cried down and cried out against, bawled down and outcried`;
  σχολαστής `ones who live at ease, leisurely and idle`; ἀπολείπω `you will leave over` (sixteen
  senses); ἔρχομαι `to coming`; ἐκπορεύομαι `of going out`; ῥύομαι `you drew to yourself`; πορεύομαι
  `let them be driven`, `I have been driven`; ὁράω `were seeing`; κακός with ἐν, `in evils`; λόγος
  with ἐν, `in words`; κενός `to empty`.
- One translation each, plain text: ἐργοδιώκτης (*taskmaster*, LSJ), πλίνθος (*a brick*), ἐχθές,
  σήμερον, συνάντησις, υἱός, τρεῖς.
- καί as the adverb, `also`, at 5:13 καθάπερ καὶ ὅτε.

### Words new in EXO 6

- **From LSJ** (not in Middle Liddell): καταδυναστεία, *oppression*, plain text (6:7) — Middle Liddell
  has the verb καταδυναστεύω and not the noun; ὀλιγοψυχία, LSJ's pointer *= λιποψυχία*, followed to
  LSJ's *swooning*, then *faint-heartedness*: `of the swooning, of the faint-heartedness` (6:9).
- **Greek cut from a translation** (`GREEK_LOST`): ἄλογος, *«without» λόγος, i. e. without speech*:
  `without logos (λόγος), unutterable, without reason and irrational, not reckoned upon and
  unexpected`. *a horse*, the modern Greek word's, is set aside; *brutes, animals* is τὰ ἄλογα and
  belongs to the neuter plural only (`FORM_SENSES` by parse).
- **σύν**, new to the corpus: the dative's senses, `along with and in company with and together
  with, with, endued with, to, attended with, in accordance with, with and by means of`; the pieces
  of *with God's help or blessing* and *on his side, of his party*, and the adverb's and compounds'
  senses, are set aside.
- **Voice** (`FORM_SENSES`): δηλόω's active leaves out the passive *to be or become manifest*;
  διαλέγω's deponent leaves out the active *to pick out*; λυτρόω's middle future λυτρώσομαι
  leaves out the passive *to be ransomed* and reads `I will release on receipt of ransom and hold
  to ransom`, Middle Liddell having no middle sense of its own.
- **A run joined**: GEN 9:27 and GEN 47 read οἶκος's plural `the houses, the abodes and dwellings`,
  one translation split in two; both now read `the houses and abodes and dwellings`, as every
  singular does.
- **Two checks fixed.** `same_form` capitalised a verse-initial word with `upper()`, which turns ᾗ
  into two letters, ἯΙ; the capital of a letter with iota subscript is its titlecase, ᾟ, which is
  how 6:28's Ἧι is written. And the doubled-marker check read ἔναντι's own *of*, its one
  translation *in the presence of* as plain text, as a case marker before κυρίου's *of*.
- New chains: ποιέω `I will make`; κραταιός `to strong`; ὑψηλός `to high`; ἐκβάλλω `will throw`;
  ὁράω `I was seen`, `you will see` (ὄψει, the future, not ὄψις); δηλόω `I made visible`;
  παροικέω `have dwelt beside … and it stands so`; εἰσακούω `I hearkened`, `will hearken`;
  καταδουλόω `are being reduced to slavery`; μιμνήσκομαι `I reminded myself of`; δυναστεία `of
  the power`; ῥύομαι `I will draw to myself`; λυτρόω `I will release on receipt of ransom`; κρίσις
  `to a separating`; εἰσάγω `I will lead in`; ἐκτείνω `I stretched out`; κλῆρος with ἐν, `in a lot`;
  σκληρός `of the hard`; ἀρχηγός, as a noun, `founders, princes and chiefs, first causes and
  originators, beginning and originating`; οἶκος `houses`, `of houses`; πατριά `of lineage`, `of
  lineages`, `the lineages`; πρωτότοκος `of firstborn`; συγγένεια `samenesses of descent`; ἀρχή `the
  beginnings`; δύναμις `to power`; διαλέγω `the ones conversing with`; λέγω `I say`.
- One translation each, plain text: βραχίων (*the arm*, ἐν taking a unit of its own before it),
  ἔναντι (*in the presence of*), θυγάτηρ, ἀδελφή, υἱός, ἔτος, the numerals.
- Names new to the corpus: Γεδσων (Gershon, where Genesis 46:11 has Γηρσων), Λοβενι, Σεμεϊ, Αμβραμ,
  Οζιηλ, Μοολι, Ομουσι, Ιωχαβεδ, Μαριαμ, Ναφεκ, Ζεχρι, Ελισαφαν, Σετρι, Ελισαβεθ, Αμιναδαβ,
  Ναασσων, Ναδαβ, Αβιουδ, Ελεαζαρ, Ιθαμαρ, Ασιρ, Ελκανα, Αβιασαφ, Φουτιηλ, Φινεες, Φοίνισσα (the
  Phoenician woman, where Genesis 46:10 has Χανανῖτις). Ισσααρ is Izhar here, Jezer at GEN 46:24.

### Words new in EXO 7

- **From LSJ** (not in Middle Liddell): ἐπόζω, *become stinking*, plain text (7:18, 7:21).
- **Close form**: ἐπαοιδός is ἐπῳδός uncontracted, LSJ's *= ἐπῳδός*, and reads Middle Liddell's
  ἐπῳδός (`SPELLING`); as an adjective used as a noun it opens with *an enchanter*: `the enchanters,
  the singing to and over, the acting as a charm for and against, the sung and said after, the
  called after, the verses and passages returning, the choruses and burdens and refrains`. νοῦς is
  filed under νόος, Middle Liddell's uncontracted headword, as the brief's rule for contracted forms
  has it; the translations of phrases (νόῳ *heedfully*, σὺν νόῳ *wisely*, ἐκ παντὸς νόου *heart and
  soul*, ἐν νόῳ ἔχειν *to intend*) are set aside: `the mind and perception, the sense, the mind and
  heart, the mind and purpose, the sense and meaning`.
- **Voice and form** (`FORM_SENSES`): μεταβάλλω's active, but the participle, leaves out the
  middle's senses and the participle's *instead, in turn*; συνίστημι's perfect active is
  intransitive, and 7:19's συνεστηκὸς ὕδωρ reads the intransitive senses, the participle's *a
  well-disciplined*, *a standing* among them; ἐπιστρέφω's middle and passive take the entry's own
  Mid. and Pass. senses (ἐπιστραφείς, 7:23).
- **Pieces set aside** (`NOT_SENSES`): μεταβάλλω (examples' pieces and translations), σοφιστής (*an
  adept* repeated, *a professor of*), κοιτών (*a chamberlain*, the phrase ὁ ἐπὶ τοῦ κοιτῶνος's),
  ὡσαύτως (*in like manner* repeated), συνίστημι (*is joined*, *were at issue*).
- **κύκλῳ with a genitive** is the preposition, `P-`, as MorphGNT codes κύκλῳ τοῦ θρόνου (Rev 4:6),
  and the adverb only where it stands alone (Mark 3:34). GEN 35:5 and 41:48, both with a genitive,
  are now `P-` too, and the brief says so.
- New chains: λαλέω `you will talk`, `may talk`; τέρας `a sign` (the singular); ἐπιβάλλω `I will throw
  and cast upon`; γινώσκω `will learn to know`; ἐκτείνω `stretching out`; δράκων `a dragon`,
  `dragons`; συγκαλέω `called to council`; σοφιστής `the masters of one's craft`; φαρμακός `the
  poisoners`; φαρμακεία `to the uses of drugs`; ὡσαύτως `in like manner and just so`; κατισχύω
  `had power over`; βαρέω `has been weighed down … and it stands so`; ἐξαποστέλλω `of the sending
  quite away`; ἵστημι `you will be set` (the intransitive future middle); συναντάω `meeting face to
  face`; τύπτω `I beat`; ποταμός with ἐν, `in the river`, and `the rivers`; μεταβάλλω `will throw
  into a different position`, `threw into a different position`; δύναμαι `will be able`; διῶρυξ `the
  trenches`; ἕλος `the low grounds by rivers`; συνίστημι `having stood together`; ξύλον and λίθος with
  ἐν; ἐπιστρέφω `having turned himself round`; ἀναπληρόω `were filled up`; πατάσσω `the beating`;
  ἀναβαίνω `having gone up`, `will go up`; οἶκος `the houses`; ταμιεῖον `the treasuries`; κλίνη `of
  the things on which one lies`; φύραμα and κλίβανος with ἐν; θεράπων `the waiting-men`.
- One translation each, plain text: σκληρύνω, ἐκδίκησις (*an avenging*), βάτραχος (*a frog*),
  ἐξερεύγομαι (*to empty themselves*, of rivers), κοιτών, ὀγδοήκοντα, ἑπτά.
- καί as the adverb, `also`, at 7:11 and 7:22, ἐποίησαν καὶ οἱ ἐπαοιδοί; οὐδέ as the adverb, *not
  even*, at 7:23, `D-`, as MorphGNT codes it where it does not mean *nor*.

### Words new in EXO 8

- **From LSJ** (not in Middle Liddell): θιμωνιά, LSJ's θημωνιά, *= foreg.*, pointing to θημών,
  *heap*, plain text, `heaps heaps` (8:10); ἀνάψυξις, `cooling, exposure, drying up, relief and
  respite` (8:11); ἐπαποστέλλω, `I send after, I send to attack` (8:17); παραδοξάζω, `I will make
  wonderful and extraordinary, I will lay unheard-of inflictions upon, I will put a mark of
  distinction between and separate` (8:18).
- **Close forms** (`SPELLING`): σκνίψ is Middle Liddell's κνίψ, *like σκνίψ*, whose one translation
  a word outside the `<tr>` cuts — *a small «insect which gnaws» figs*, whole in `MARKUP_LOST` —
  and reads as plain text, `the small insects which gnaw figs`; κυνόμυια is Middle Liddell's pointer
  to κυνάμυια, `dog-fly, shameless fly`.
- **Voice** (`FORM_SENSES`): καλύπτω's and ἀφανίζω's active leave out the middle and the passive;
  περιαιρέω's active leaves out the middle and the passive, and the passive the active and the
  middle (`will be taken off, will be stript of`); βαρύνω's active leaves out the passive's
  *heavy, weary, disabled* (ἐβάρυνεν, 8:28).
- **Pieces set aside** (`NOT_SENSES`): καλύπτω (a phrase's *to be buried*, an example's pieces),
  ἀφανίζω (*hypocritical*, *make away with* repeated), ὄζω (examples' pieces), ἐξαπατάω (*in*),
  δάκτυλος (*the fingers*, *the thumb*, *the toes*, phrases').
- **The possessive**: ἐμοῦ and σοῦ between the article and its noun (τοῦ ἐμοῦ λαοῦ) are ἐμός and
  σός, not the pronouns: `of the mine`, `of the thy and thine`.
- **παραγίνομαι's aorist** reads `was near`, as GEN 35:9 has it; the present's `comes to be beside`
  is the present's.
- **The stemmer** now reads *smote*, *smitten*, *stank* and *smelt* as forms of *smite*, *stink* and
  *smell*: πατάσσω's imperative `beat, … strike and smite` and its aorist `beat, … struck and smote`
  had read as two ranges.
- New chains: ἀνάγω `lead up`, `led up`; ἀναβιβάζω `was made to go up`; καλύπτω `covered with`;
  εὔχομαι `pray`, `I may pray`, `I will pray`; περιαιρέω `let him take off something that
  surrounds`, `took off something that surrounds`; ἐξαποστέλλω `I will send quite away`; τάσσω
  `fall in` (the middle imperative; `arrange` until EXO 29 read it with the middle's own senses); οἰκία `of the buildings`, `the buildings`; ἀφανίζω `to make
  unseen`; ὑπολείπω `will be left behind`; οἶδα `you may know`; βοάω `cried aloud`; ὁρισμός `of
  the marking out by boundaries`; ἀγρός `of the fields`; ὄζω `smelt`; βαρύνω `was weighed down`,
  `weighed down`; πατάσσω `beat` (the imperative); χῶμα `the earth thrown up`, `to earth thrown up`;
  τετράπους with ἐν; δάκτυλος `a finger`; ὀρθρίζω `rise early`; ἵστημι `be set` (the intransitive
  imperative); βούλομαι `you may will`; πίμπλημι `will be filled full of`; ἔπειμι `is upon`;
  διαστολή `a notch`; θύω `offer`, `we will offer`, `to offer`, `may offer`; βδέλυγμα `the
  abominations`; λιθοβολέω `we will be pelted with stones`; ἀποστέλλω `I send off`; ἀποτείνω `you
  will stretch out`; ὅδε `this`; ἐξέρχομαι `I will go out of`; προστίθημι `you may put to`;
  ἐξαπατάω `to deceive`; καιρός `of the due measure`.
- One translation each, plain text: βάτραχος, ἔπαυλις (*a fold*), ἐξολεθρεύω (*to destroy
  utterly*), θιμωνιά, σκνίψ.
- καί as the adverb at 8:3, 8:14 (ἐποίησαν καὶ οἱ ἐπαοιδοί) and 8:28 (καὶ ἐπὶ τοῦ καιροῦ τούτου);
  πλήν with no genitive is the conjunction, `C-`, at 8:5 and 8:7.

### Words new in EXO 9

- **From LSJ** (not in Middle Liddell): ἐγκρατέω, `you are master of and exercise control over`
  (9:2; Middle Liddell has the adjective ἐγκρατής); καμιναία, *furnace*, plain text (9:8, 9:10);
  φλυκτίς, LSJ's pointer to φλύκταινα, then *boil*: `blisters, pustules, boils` (9:9);
  συνάντημα, `the incidents and occurrences, the visitations, the confirmations` (9:14);
  σπερματίζω, `sowing, being in seed` (9:31).
- **Close form**: ὀλύρα is Middle Liddell's ὄλυρα, `the kind of grain and spelt and rye`.
- **Cut translation restored** (`MARKUP_LOST`): ὕω's *Lat. pluit, it rains*, the English inside
  the Latin element; the impersonal *it rains* is the third person's, and a first or second person
  leaves it out.
- **Number and voice** (`FORM_SENSES`): ὅρος's and χάλαζα's singular leave out the plural's
  senses; ῥητός's *rational quantities* is τὰ ῥητά's; ὕω's, φλογίζω's and ἐκπετάννυμι's active
  leave out the passive; διαγγέλλω's passive the middle; πλήσσω's passive the active and the
  middle, `was struck and stricken and smitten, received a heavy blow and was beaten, was stricken`.
- **Pieces set aside** (`NOT_SENSES`): ῥητός (a repeat, ἐπὶ ῥητοῖς, the adverb ῥητῶς), ὅρος
  (examples' pieces, the Latin), ἕλκος (*of plague-ulcers*, the use's label), ὕω (examples'), πάσσω
  (examples' pieces), ἐμποιέω (a passive example's pieces), λίνον (*lint-*), πλήσσω (examples').
- **βρέχω** heads as `wetted`, the entry's first sense, as GEN 2:5 has it.
- New chains: ἔπειμι `will be upon`; κτῆνος with ἐν, and `of flock and herd`; ἵππος and
  ὑποζύγιον with ἐν; βοῦς `to bullocks`; πρόβατον `to things that walk forward`; ῥητός `stated`;
  ὅρος `a boundary`; πάσσω `let him sprinkle`, `sprinkled`; γίνομαι `let come into being`;
  κονιορτός `dust stirred up`; ἕλκος `wounds`, `the wounds`; ἀναζέω `boiling up`; φαρμακός `the
  poisoners`, and with ἐν; ἵστημι `to be set`; ἐκτρίβω `you will be rubbed out`; διατηρέω `you were
  watched closely`; ἐνδείκνυμι `I may inform against`; διαγγέλλω `may be given notice by a
  messenger`; ἐμποιέω `you make in`; ὕω `I send rain`; ὥρα `the period`; χάλαζα `hail`, `the
  hail`, and with ἐν; κτίζω `has been peopled … and stands so`; κατασπεύδω `press`; εἰσέρχομαι
  `may go in`; πίπτω `may fall`; φοβέομαι `the one being put to flight`, `you have been put to
  flight … and stand so`; διάνοια `to the thought`; βοτάνη `grass`; φωνή `sounds`, `the sounds`;
  διατρέχω `was running across`; φλογίζω `setting on fire`; συντρίβω `rubbed together`; ἁμαρτάνω `I
  have missed the mark … and it stands so`; ἀσεβής `ungodly`; παύω `let take its rest`, `will take
  their rest`, `has taken its rest … and stands so`; προστίθημι `you will put to`; μένω `to stay
  stand fast`; ἐξέρχομαι `I may go out of`; γινώσκω `you may learn to know`; θεράπων `the
  waiting-men`; οὐδέπω `and not yet`; λίνον `the anything made of flax`; κριθή `the barley-corns`;
  παρίστημι `having stood by … and standing so`; ὄψιμος `late`; ἐκτός `outside`; στάζω `dropped`.
- One translation each, plain text: σκληρύνω, ἐπαύριον, αἰθάλη (*soot*), καμιναία, ἐκπετάννυμι's
  active, πυρός (*wheat*), οὗ (*where*).

### Words new in EXO 10

- **From LSJ** (not in Middle Liddell): σκῶλον, `stumblingblock and hindrance` (10:7), LSJ's
  neuter, citing this verse. Middle Liddell has only the masculine σκῶλος, *a pointed stake*, and
  the text's σκῶλον is the predicate nominative after ἔσται, which no form of σκῶλος can be.
  ψηλαφητός, *that can be felt*, one translation, plain text (10:21).
- **Close forms**: γνόφος is Middle Liddell's "= δνόφος", `darkness and dusk and gloom` (10:22);
  καταγίνομαι the Attic καταγίγνομαι, `were abiding and dwelling` (10:23); φῶς is filed under φάος,
  the uncontracted headword, as νοῦς under νόος: `light and daylight, a light, eyes` (10:23).
- **Latin throughout** (`LATIN_ONLY`): οὐδέποτε's *Lat. ne unquam quidem, nunquam*.
- **Voice** (`FORM_SENSES`): ἀπόλλυμι's second perfect ἀπόλωλα is active in form and the middle's
  in sense, *to perish utterly, die*, and its card now shows the middle's senses; the active's
  other tenses show the active's, and the middle's the middle's. `has perished utterly and died and
  it stands so, has been undone and it stands so, is done for and lost and ruined and it stands so,
  has been lost and slipped away and vanished and it stands so` (10:7).
- **Pieces set aside** (`NOT_SENSES`): ἑξῆς (*the next*, ἡ ἑξῆς ἡμέρα's), ἄνεμος (*the wind*, a
  repeat; *to the winds*, an example's dative), θύελλα (*thunderstorms*, πυρὸς θύελλαι's), φάος (repeats of *light,
  daylight*; an address), φύω (examples' pieces and translations).
- **Used as a noun**: τὸ περισσόν takes the entry's noun senses, `the surplus, the surplus and
  residue` (10:5).
- **The passive participle of φύω** heads with the first sense in the passive, the article's noun
  neuter: `the thing being brought forth and produced and put forth, being begotten and engendered
  and generated, growing and waxing and springing up and arising, being begotten and born, being
  born and descended from` (10:5).
- **The passive infinitive of ἐντρέπω** the same way: `to be turned about, to be altered, to turn
  about and linger and hesitate, to turn towards and give heed to and pay regard to and respect and
  reverence, to take care that, to feel shame and fear` (10:3).
- **One article over two words** prints once. τὴν ἐρυθρὰν θάλασσαν is `the red` `sea`, the
  adjective plain text; as GEN 22:18 has `of the mine` `of sound`, the noun after a possessive, a
  numeral or a name carries no second *the*. Ten units had printed it twice — GEN 10:11, 19:1,
  26:5, 30:27, 49:29; EXO 4:9, 5:15, 5:23, 8:4, 8:19 — and now read `city`, `messengers`, `of
  sound`, `to way in`, `people`, `to signs`, `to house-slaves`, `to name`, `of people`.
  `build/validate.py` fails on a new one.
- **EXO 8's ἀνάγω** had kept the present in its aorist chain, `led up` over `lead up, … take up,
  bring up`, and the imperative's reflexive in the third person: now `led up, … took up, brought
  up, …, made ready and prepared himself` (8:2), `themselves` (8:3), and the imperative's
  `yourself` (8:1).
- New chains: ἑξῆς `one after another`; ἐπέρχομαι `may come upon`; διηγέομαι `you may set out in
  detail`; ἐμπαίζω `I have mocked at … and it stands so`; ἐντρέπω `to be turned about`; θέλω `you
  may will`; καλύπτω `will cover with`; ὄψις `the look`; καθοράω `to look down`; κατεσθίω `will eat
  up`; περισσός `the surplus`; καταλείπω `the thing having been left behind`; φύω `the thing being
  brought forth`; οὐδέποτε `and not ever`; ὁράω `have seen … and it stands so`, `you may be seen`,
  `I will be seen`; γίνομαι `have come into being`; ἐκκλίνω `having bent out of the regular line`;
  οἶδα `to know`; ἀπόλλυμι `has perished utterly`; ἀποστρέφω `turned` with `themselves`; λατρεύω
  `work for hire`, `to work for hire`, `we may work for hire`; πορεύομαι `the ones being driven`;
  πρεσβύτερος `to elders`; ἑορτή `a feast`; πονηρία `a bad state`; πρόκειμαι `is set before one`;
  καρπός `the fruit`; ὑπολείπω `left remaining for herself`, `leave remaining for yourselves`, `we
  will leave remaining for ourselves`; ἄνεμος `wind`, `the wind`; νότος `south`, `the south`;
  ἀναλαμβάνω `took up` with `himself`; ἀνάγω `led up`; χάλαζα `of the hail`; βοτάνη `to grass`;
  κατασπεύδω `was pressing`; καλέω `to call`; προσδέχομαι `receive favourably`; προσεύχομαι `offer
  prayers`; θάλασσα `of sea`; σφοδρός `vehement`; γνόφος `darkness`; θύελλα `a furious storm`; κοίτη
  `of the marriage-bed`; φάος `light`; καταγίνομαι `were abiding`; ἀποτρέχω `let run off`;
  ὁλοκαύτωμα `whole burnt-offerings`; θυσία `offerings`; ὁπλή `a hoof`; βούλομαι `willed`;
  προστίθημι `to put to`; ποιέω `we will make`; ἀναβαίνω `let go up`; τέκνον `of the things borne`.
- One translation each, plain text: σκληρύνω, ἀκρίς (*a locust*), πρόπαππος (*a great-grandfather*),
  νεανίσκος (*a youth*), καθότι (*in what manner*), ψηλαφητός. ἐρυθρός is a unit: `the red, the
  Erythraean sea, the Red Sea / Arabian Gulf, the Indian Ocean, the Persian Gulf`, the phrase's names kept, since the
  phrase Ἐρυθρὴ θάλασσα is in the text, and their extent in the note (Q8; 10:19, 13:18, 15:4, 15:22, 23:31).

### Words new in EXO 11

- **Greek cut** (`GREEK_LOST`): γρύζω, *to say γρῦ, to grunt, grumble, mutter*; the encoding stops
  the first translation at *to say*. `will say gry (γρῦ), will grunt and grumble and mutter`
  (11:7), the interjection transliterated with the Greek after it.
- **Pieces set aside** (`NOT_SENSES`): πληγή (*a blow*, a repeat), ἐκβολή (examples' pieces and
  translations: *turning … out of*, *the time when … comes into ear*, *earth cast … scraped up*,
  *children exposed*, *wrecked*), κύων (*a word of reproach*, the use's label), ἀφηγέομαι (*the
  van*, *what has been told*, participles used as nouns).
- **A misprint the module shares**: 11:8 προκυνήσουσίν, for προσκυνήσουσίν. The transcription
  keeps it and a note says so; `printed` lists nothing, since the module prints the same.
- **πρωτότοκος** has one translation, *first-born*, and is plain text, as GEN 4, 10 and 25 had it.
  Nine units since GEN 35 had read `firstborn, first-fruits`, and *first-fruits* is in no entry the
  project reads: GEN 35:23, 41:51, 43:33, 46:8, 48:18, 49:3; EXO 4:22, 4:23, 6:14 are plain text now.
- **Chains that said more than their entry**, plain text now, each one translation: θυρίς `of the
  window` (GEN 26:8; *little door* was the etymology's *Dim. of θύρα*); κατοίκησις `the settling
  in` (27:39) and διαχωρίζω `separate` (30:32, 30:40), whose added senses were LSJ's though Middle
  Liddell has both words; κληρονομία `an inheritance` (31:14), ποίμνη `of a flock` (32:17),
  ὀλιγοστός `one out of a few` (34:30) and λίθινος `of stone` (35:14), whose added senses are the
  ones `NOT_SENSES` sets aside; προσεγγίζω `approached` (33:6, 33:7), the entry's *to approach*,
  where `came near` had headed it.
- New chains: πληγή `a blow`; ἐκβολή `to a throwing out`; αἰτέω `let ask`; χάρις `the outward
  grace`; εἰσπορεύομαι `I go into`; κάθημαι `is seated`; θρόνος `of the seat`; θεράπαινα `of the
  waiting maid`; γρύζω `will say gry (γρῦ)`; κύων `a dog`; γλῶσσα `to the tongue`; παραδοξάζω
  `will make wonderful`; ἀφηγέομαι `you lead from`; θυμός `of soul`; πληθύνω `I may make full`.
- One translation each, plain text: κρυφῇ (*secretly*), κίχρημι (*lent*), μύλος (*the millstone*),
  πρωτότοκος (*first-born*).

### Words new in EXO 12

- **From LSJ** (not in Middle Liddell): δέσμη, `package and bundle, measure, handful` (12:22; Rahlfs prints δεσμήν, the module δέσμην, and
  `printed` lists it); ἐνδόσθια, LSJ's "= ἐντόσθια", whose substantive is *inwards, entrails*: `to
  the inwards and entrails` (12:9); ἐπίμικτος, LSJ's ἐπίμεικτος, `common to, mixed, combining the
  features, sociable and gregarious` (12:38); ζυμωτός, `fermented and leavened` (12:19, 12:20);
  λατρευτός, "= foreg.", λατρευτικός, *servile*, plain text (12:16); πικρίς, `of ox-tongues and
  Helminthia sepioides, of sour soils` (12:8), its "= κιχόριον" pointing at an entry LSJ lacks.
- **Close forms**: περιζώννυμι under the middle περιζώννυμαι, "with perf. pass. -έζωσμαι", `having
  girded round themselves and girded themselves with and standing so` (12:11); ὀλεθρεύω under
  ὀλοθρεύω, *to destroy utterly*, plain text (12:23).
- **Cut translations restored** (`MARKUP_LOST`): αὐτόχθων's *aborigines, natives* and προσήλυτος's *one
  who has come over to Judaism, a convert, proselyte*, both inside the Latin element. αὐτόχθων used as
  a noun opens with them: `to aborigines and natives, to sprung from the land itself, to indigenous`
  (12:19), `the aborigine and native, …` (12:48).
- **Case and number** (`FORM_SENSES`): σπουδή's dative keeps the adverbial *in haste, hastily … earnestly,
  seriously, urgently*, unmarked after the noun's senses, as βίᾳ (12:33); its other cases leave them out,
  and the singular the plural's *zealous exertions, party feelings*. νόμος's *by custom, conventionally*
  is the dative's.
- **Pieces set aside** (`NOT_SENSES`): ἀρκέω, ἐνιαύσιος, ὠμός, περιζώννυμαι, σπουδή, παίω, ἐνδέω, πεζός,
  νόμος, μεσόω, βάπτω, καθικνέομαι — examples' pieces and translations, repeats, and an adverb's or a
  comparative's.
- **Used as a noun**: τὸ ἀρκοῦν, `the thing warding off, …, sufficient and enough` (12:4); πεζῶν, `of
  fighters on foot, …` (12:37); μισθωτός, `an hireling and hired servant, mercenaries` (12:45); νόμιμον,
  `usage and custom, funeral rites` (12:14, 12:17, 12:24).
- **A name**: πασχα, the Aramaic pasḥāʾ in Greek letters, indeclinable and printed lower case, is a
  name, as χερουβιμ: `pascha` / `passover`, glossed at its first occurrence (12:11).
  γειώρας, the Aramaic gîyôrāʾ, is one too, though it declines (Q10): `in to the geiōrais` /
  `in to the sojourners`, glossed with LSJ's *sojourner, proselyte* (12:19).
- New chains, among them: ἐνιαυτός `of the long period of time`; δέκατος `to the tenth`; λαμβάνω `let them
  take`; συλλαμβάνω `will lay hold of for himself`; γείτων `the one of the same land`; συναριθμέω `will
  reckon in`; ἐνιαύσιος `of a year`; ἀρήν `of the lambs`; διατηρέω `having been watched closely … and
  standing so`; σφάζω `will slay`; πλῆθος `the great number`; τίθημι `they will set`; σταθμός `of
  standing places`, `of the standing places`; φλιά `the doorpost`; κρέας `the flesh`; ὀπτός `roasted`;
  ὠμός `raw`; ἕψω `having been boiled … and standing so`; κατακαίω `you will burn down`; ὀσφύς `the
  loins`; ὑπόδημα `the soles bound under the feet with straps`; βακτηρία `the staffs`; σπουδή `of haste`,
  `to haste`; διέρχομαι `I will go through`; σκεπάζω `I will cover`; ἐκτρίβω `of the being rubbed out`;
  παίω `I may strike`; ἑορτάζω `you will keep festival`; ἀφανίζω `you will make unseen`; ζύμη `leaven`;
  κλητός `called`; φυλάσσω `you will keep watch and ward for yourselves`; ἐντολή `the injunction`;
  δύναμις `the power`; γερουσία `Council of Elders`; ὕσσωπος `of hyssop`; βάπτω `having dipped in water`;
  καθικνέομαι `you will come down to`; παρέρχομαι `will go by`; ἀφίημι `will send forth`; λατρεία `the
  state of a hired workman`; μεσόω `of forming the middle`; κάθημαι `of the one being seated`;
  αἰχμαλωτίς `of the prisoner`; θνήσκω `being dead`; καταβιάζομαι `were constraining`; φύραμα `the things
  which are mixed`; ἐνδέω `having been bound in`; αἰτέω `asked`; σκυλεύω `stripped`; ἐπιμένω `to stay on`;
  δύναμαι `were able`; προφυλακή `a guard in front`; νόμος `the anything assigned`, `anything assigned`;
  ἀλλογενής `of another race`; περιτέμνω `you will cut`; βιβρώσκω `will be eaten`; ἐκφέρω `you will
  carry out of`; προσέρχομαι `may come to`, `will come to`, `to the one having come to`; ἐγχώριος `to the
  dweller in the land`.
- One translation each, plain text: μήν (Middle Liddell's μείς, *a month*), τεσσαρεσκαιδέκατος,
  ὀλιγοστός, ἐκδίκησις, ἐξολεθρεύω, ἑπτά, ἐνάρχομαι, εἰκάς, σταῖς, ζυμόω, ὦμος, ἐγκρυφίας,
  κατοίκησις, ἔτος, τετρακόσιοι, τριάκοντα, ἑξακόσιοι, ἀργυρώνητος, ἀρσενικός, ἀπερίτμητος, κίχρημι,
  συναναβαίνω, λατρευτός, ὀλεθρεύω.

### Words new in EXO 13

- **From LSJ** (not in Middle Liddell, which has πρωτόγονος): πρωτογενής, `first-born and primeval`
  (13:2), beside πρωτότοκος's plain *first-born*.
- **The impersonal**: μεταμελήσῃ is filed under μεταμέλει, Middle Liddell's headword, which the second
  pass named and the first had as μεταμέλω. `FORM_SENSES` leaves the impersonal active the middle's
  *to feel repentance … to change one's purpose*: `it may repent and rue, may repent, may cause
  repentance and sorrow` (13:17).
- **Case** (`FORM_SENSES`): ὅρκος's *on oath* is the dative's, read after the noun's senses: `to object
  by which one swears and witness of an oath, to oath, on oath` (13:19).
- **Pieces set aside** (`NOT_SENSES`): μνημονεύω (*to call to* … *mind, mention*, cut in two around
  *another's*), μεταμέλει (examples' translations), ἀλλάσσω (*for*, *in turn*, *in turns*), ὁδηγέω (*upon
  his way*), ὅρκος (*to bind*, *to abide by*), ἐξαείρω (*excites*).
- **κυκλόω's active** takes the active's three senses: `encircled and surrounded, moved in a circle and
  whirled round, formed into a circle` (13:18). GEN 2:11 and 2:13 had read `the one encircling,
  surrounding, moving in a circle, going round`, a run split and the middle's *going round* taken in;
  they now read the same three in the participle.
- **ἀλλάσσω's active** leaves out *to buy*, the middle's, as GEN 31:7 and 35:2 have it: `you will make
  other than it is and change and alter, …, you will take one thing for another and assume, …` (13:13).
- **ὥρα's plural** carries the plural's seventeen senses, as GEN 18:14: `of periods, …, of Hours` (13:10).
- **The formula** for ἦν ending in a semicolon (13:17) is read past by the bare-headword check, as its
  comma and full-stop forms were.
- New chains: ἁγιάζω `hallow`, `you will hallow`; διανοίγω `opening`; μνημονεύω `call to mind`; δουλεία
  `of servitude`; ἐκπορεύομαι `you go out`, `I was going out`; νέος `of the young`; εἰσάγω `may lead in`;
  δίδωμι `to give`; ἕβδομος `to the seventh`; ὅριον `to the boundaries`; ἀναγγέλλω `you will carry back
  tidings of`; ὀφθαλμός `of eyes`; καιρός `due measures`; βουκόλιον `of the herds of cattle`; ὄνος `of
  ass`; πρόβατον `to thing that walks forward`; λυτρόω `you will release on receipt of ransom`; ἐρωτάω
  `may ask`; θύω `I offer`; ἀσάλευτος `not agitated`; ὁδηγέω `led`; μεταμέλει `it may repent`; ὁράω `to
  having seen`; κυκλόω `encircled`; ὅρκος `to object by which one swears`; συναναφέρω `you will carry up
  together`; ἐξαίρω `having lifted up` with `themselves`; στρατοπεδεύω `encamped`; ἡγέομαι `was going
  before`; στῦλος `in a pillar`, `the pillar`; νεφέλη `of a cloud`, `of the cloud`; δείκνυμι `to bring to
  light`; πῦρ `of the fire`.
- One translation each, plain text: μήτρα (*the womb*), σήμερον (*to-day*), γάλα (*milk*), μέλι (*honey*),
  ἕξ (*six*), ἀρσενικός (*male*).

### Words new in EXO 14

- **From LSJ** (not in Middle Liddell): ἐνδοξάζομαι, LSJ's passive headword, *to be glorified*, citing
  14:4, one translation, plain text (14:4, 14:17, 14:18); τριστάτης, `ones who stand next to the king and
  queen` — `ones who stand next to the king and queen and viziers`, one translation (14:7).
- **Spelling** (`SPELLING`): στρατιά, Middle Liddell's στρατία, *= στρατός, an army*: `to the army, to the
  land force, to the host and company and band, to the expedition` (14:4).
- **Cut translations restored** (`MARKUP_LOST`): παρίημι, *to let drop at the side, let fall*; σιγάω, *to
  be still, to keep silence*, *to be kept secret*; συμμίγνυμι, *to make acquainted with*; ὑπάγω, *to bring
  before the judgment-seat*; ἐπαναστρέφω, *to turn back upon one*, which GEN 18:10's participle now reads;
  ῥήγνυμι, *to break, break asunder or in pieces, rend, shiver, shatter*, one translation, which GEN 7:11's
  `were broken and broken asunder and in pieces and rent and shivered and shattered` now keeps as one item.
- **Form** (`FORM_SENSES`): ἐναντίος's declined adjective leaves out the neuter's adverb and preposition
  senses, which ἐναντίον reads from the same card, the masculine plural's *one's adversaries* and two
  examples': ἐξ ἐναντίας, `of opposite, of over against and opposite, …` (14:2, 14:9). τεῖχος's singular
  leaves out the plural's *a single fort, fortifications*. The actives of συναπάγω, παρίημι, πολεμέω,
  σιγάω, συμμίγνυμι, ὑπάγω, συνταράσσω and ῥήγνυμι leave out the passive's and the middle's senses, and
  μεταστρέφω's passive leaves out the active's intransitive and its sense with the genitive.
- **Pieces set aside** (`NOT_SENSES`): μεταστρέφω, μνῆμα (a repeat), παρίημι, κρείσσων (the plural's nouns,
  examples'), πολεμέω, σιγάω (the imperative's *hush!*), συμμίγνυμι, ὑπάγω, βίαιος (the adverb's), τεῖχος
  (τοῖχος set against it), ἑωθινός (the neuter adverb's), συνταράσσω, συνδέω, ἄξων (Solon's tablets),
  σχίζω (*were divided*, an example's), ῥήγνυμι.
- **Runs joined**: φεύγω's *to flee, take flight, run away* and στρατοπεδεύω's *to encamp, bivouac, take up a
  position* had been split in every unit, the past tense hiding it from the runs check: `fled and took
  flight and ran away`, `encamped and bivouacked and took up a position` (GEN 12, 14, 39; EXO 4, 13).
- **The case marked inside a gloss**: εὐώνυμος is *of good name*, and its genitive reads `of of good name
  and honoured, of of good omen and prosperous and fortunate, of left and on the left hand, of on the left`
  (14:22, 14:29). `validate.py` reads the doubled *of* there as the gloss's (`GLOSS_LEADS`).
- New chains: στρατοπεδεύω `let them encamp`, `you will encamp`; πλανάω `are made to wander`; συγκλείω `has
  shut`; φεύγω `has fled`, `let us flee`, `fled` (plural); μεταστρέφω `was turned about`; ποιέω `we made`;
  δουλεύω `of the being a slave`, `we may be slaves`, `to be a slave`; ζεύγνυμι `yoked`; ἅρμα `in the
  chariots`, `of the chariots`; ἵππος `to horses`; ἐκπορεύομαι `were going out`; ἱππεύς `the horsemen`;
  προσάγω `was bringing to`; ὑπάρχω `the beginning`; μνῆμα `memorials`; ἐξάγω `you led out`, `having led
  out`; θανατόω `to put to death`; λαλέω `we talked`; παρίημι `let drop beside`; κρείσσων `stronger`; ὁράω
  `you have seen`; προστίθημι `you will put to`; χρόνος `time`; πολεμέω `will be at war`, `is at war`; σιγάω
  `you will be silent`; βοάω `you cry aloud`; ἀναζεύγνυμι `let them yoke again`; ἐπαίρω `lift up and set
  on`; ῥήγνυμι `break`; εἰσέρχομαι `let go in`; ξηρός `of dry`, `dry`; προπορεύομαι `the one going before`;
  παρεμβολή `of the insertion`; συμμίγνυμι `mixed together`; ὑπάγω `led`; ἄνεμος `in wind`; νότος `to
  south`; βίαιος `to forcible`; σχίζω `was split`; τεῖχος `a wall`; εὐώνυμος `of of good name`; ἀναβάτης
  `the ones mounted`; ἑωθινός `to the in the morning`; συνταράσσω `threw all together into confusion`;
  συνδέω `bound`; ἀποκαθίστημι `let be re-established`; ἐπικαλύπτω `let cover over`; ἐκτινάσσω `shook out`;
  ἐπαναστρέφω `having turned back upon one`; εἰσπορεύομαι `the ones having gone into`; πιστεύω `trusted`
  (plural).
- One translation each, plain text: ἔπαυλις (*a fold*), ἐνώπιον (*face to face*), σκληρύνω, καταδιώκω (*to
  pursue closely*), συναπάγω's active (*to lead away with*), ἑξακόσιοι, ἄξων (*an axle*).

### Words new in EXO 15

- **From LSJ** (not in Middle Liddell): σκεπαστής, `shelterer and protector`, citing 15:2; ἁγίασμα, LSJ's
  *= ἁγιαστήριον*, a pointer to *holy place, sanctuary*, then *holiness*: `holy place and sanctuary,
  holiness` (15:17).
- **Spelling and close forms** (`SPELLING`): ᾄδω under ἀείδω, the uncontracted headword; διΐστημι under
  the key without its diaeresis; ἕτοιμος under ἑτοῖμος; ἀπολιθόω under the passive Middle Liddell heads,
  ἀπολιθόομαι, *to become stone*, the voice 15:16 uses; προφῆτις under προφήτης, *fem. of προφήτης*, and
  nothing more, read as GEN 20:7 reads it; ἐνδόξως under ἔνδοξος, which names the adverb and glosses it
  nowhere (open question Q13). ὠδῖνες is filed under ὠδίς, Middle Liddell's nominative, as the second pass had
  it.
- **Cut translations restored** (`MARKUP_LOST`): ἔνδοξος, *held in esteem or honour, of high repute*, which
  GEN 34:19's superlative now reads as one item; καταδύω, *to cut down to the water's edge, disable*; τήκω,
  *to cause to waste or pine away*; διΐστημι, *to set one at variance with*, *to divide it into fractions*,
  *to stand at certain distances or intervals*; δύω, *to enter, come over or upon*.
- **Form** (`FORM_SENSES`): the intransitive second aorists leave out the causal senses — καταδύω's
  κατέδυσαν, διΐστημι's διέστη, and δύω's ἔδυσαν, whose entry is *causal in fut. and aor1*. GEN 28:11's ἔδυ,
  the sun setting, had been headed `stripped off`; it now reads `entered and made one's way into, sank into,
  set, got into and put on, entered and came over and upon`. δοξάζω's passive leaves out the intransitive
  *to hold an opinion*; ᾠδή's singular the plural's *lyric poetry*; ὠδίς's plural the singular's, and the
  singular the plural's; σκῦλον's plural the singular's *booty, spoil, prey*; ἀκοή's other cases the dative's
  *by hearsay*, which 15:26's ἀκοῇ reads. The actives of μερίζω, θραύω and ἀείδω leave out the middle's and
  passive's, the middle of κατεργάζομαι the passive's.
- **Pieces set aside** (`NOT_SENSES`): δοξάζω, καταδύω, κῦμα (*pregnant*, the gloss's own gloss), τήκω,
  μέγεθος (*greatness*, i. e. *might, power*), ἕτοιμος, κατεργάζομαι, χορός (the note on the Attic chorus),
  ἐξάρχω, ἀκοή, φοῖνιξ (the note on colours), νόσος, σκῦλον, διΐστημι, ἀείδω, ὠδίς, δύω.
- **First senses that ignore the context**, as the rule has them: δοξάζω heads `has been thought`, its *to
  magnify, extol* last; φοῖνιξ heads `of purple-reds`, the palm its third sense.
- **Validator**: a capital with its iota written beside it (ᾌσωμεν) is titlecase, and the names check reads it
  as a capital; ἐνωτίζομαι's plain *hearken to* may stand before a dative's *to* (`PLAIN_LEADS`).
- New chains: ᾄδω `sang`, `let us sing`; ᾠδή `the song`; ἐνδόξως `held in esteem`; δοξάζω `has been thought`,
  `I will think`, `having been thought`; ἵππος `a horse`; ἀναβάτης `one mounted`, `ones mounted`, `to ones
  mounted`; θάλασσα `to sea`; σκεπαστής `shelterer`; σωτηρία `a saving`; ὑψόω `I will lift high`; συντρίβω
  `rubbing together`, `you rubbed together`; πόλεμος `battles`; ἅρμα `to chariots`; ἐπίλεκτος `chosen`;
  καταποντίζω `threw into the sea`; πόντος `to sea`; καταδύω `went down`; βυθός `depth`; θραύω `broke in
  pieces`; ἐχθρός `one's enemies`, `the one's enemy`; πλῆθος `to the great number`; δόξα `of the notion`, `in
  notions`; πνεῦμα `of blowing`; θυμός `of the soul`; διΐστημι `stood apart`; πήγνυμι `was made fast`; κῦμα
  `the anything swollen`; διώκω `having pursued`; καταλαμβάνω `I will seize upon`; μερίζω `I will divide`;
  σκῦλον `arms stript off a slain enemy`; ἐμπίπλημι `I will fill quite full`; ἀναιρέω `I will take up`; δύω
  `entered`; σφοδρός `to vehement`; θεός `in gods`; ἅγιος `in devoted to the gods`; θαυμαστός `wondrous`;
  ποιέω `making`; τέρας `signs`; ἐκτείνω `you stretched out`; ὁδηγέω `you led`; δικαιοσύνη `to the
  righteousness`; λυτρόω `you released on receipt of ransom`; παρακαλέω `you called to`; κατάλυμα `inn`;
  ὀργίζω `were made angry`; ὠδίς `pangs`; σπεύδω `set a-going` (plural); τρόμος `trembling`; τήκω `were
  melted`; ἐπιπίπτω `may fall upon`; μέγεθος `to greatness`; παρέρχομαι `may go by`; κτάομαι `you procured for
  yourself`; εἰσάγω `having led in`; ἕτοιμος `at hand`; κατοικητήριον `a dwelling-place`; κατεργάζομαι `you
  effected by labour`; ἁγίασμα `holy place`; αἰών `period of existence`; προφῆτις `the one who speaks for a
  God and interprets his will`; τύμπανον `the kettledrum`; χορός `of round dances`; ἐξάρχω `was beginning
  with`; εὑρίσκω `were finding`; ἐπονομάζω `was given a surname`; πίνω `we will drink`; γλυκαίνω `was
  sweetened`; δικαίωμα `acts by which wrong is set right`; κρίσις `separatings`; πειράζω `made proof`; ἀκοή `to
  a hearing`; ἀκούω `you may hear`; ἀρεστός `the acceptable`; ἐντολή `to the injunctions`; φυλάσσω `you may keep
  watch and ward`; νόσος `sickness`; ἐπάγω `I brought on`; ἰάομαι `the one healing`; στέλεχος `crowns of the
  root`; φοῖνιξ `of purple-reds`.
- One translation each, plain text: μόλιβος (*lead*), βραχίων (*the arm*), κληρονομία (*an
  inheritance*), καταφυτεύω (*to plant*), ἀπολιθόω, ἀδελφή (*a sister*), διαγογγύζω (*to murmur among
  themselves*), ἐνωτίζομαι (*to hearken to*), and the numerals.

### Words new in EXO 16

- **From LSJ** (not in Middle Liddell): διατήρησις, *preservation*, plain text (16:33, 16:34); ἐγκρίς, *a
  cake made with oil and honey*, one translation, plain text (16:31); ἐλαττονέω, `received less, gave less,
  wasted and was consumed, was missing and defective`, the middle's *lack, want* left out (16:18);
  συσκήνιος, LSJ's *= sq.*, read as σύσκηνος, `to the ones who live in the same tent and messmates and
  comrades` (16:16).
- **Spelling and close forms** (`SPELLING`): σάββατον and σαββατίζω, keyed with the capital; κόριον under
  κορίαννον, *coriander*, as LSJ's κόριον (B), *shortd. for κορίαννον* — Middle Liddell's κόριον is the
  diminutive of κόρη; the particle ὄφελον under ὀφείλω, whose *aor2 … ὄφελον … to express a wish* is
  *would that* (`FORM_SENSES` reads that alone).
- **A participle made a noun**: τὰ δέοντα (16:22) is filed under δέον, which Middle Liddell heads as *neut.
  part. of the impers. δεῖ, made into a Noun*; its plural reads the plural's *things needful or proper,
  advantages or duties*, restored whole: `the things needful and proper and advantages and duties`.
- **Cut translations restored** (`MARKUP_LOST`): πάγος, *that which is fixed or firmly set*; πλεονάζω, *to go
  beyond bounds, take or claim too much*; πικραίνω, *to make sharp or bitter*; δέον, as above.
- **Form** (`FORM_SENSES`): the actives of μετρέω, πλεονάζω, διαθερμαίνω and ἀποτίθημι leave out the
  middle's and passive's, ἀποτίθημι's middle the active's, and οἰκέω's passive (γῆν οἰκουμένην) the active's
  intransitive senses.
- **Pieces set aside** (`NOT_SENSES`): πάγος, μετρέω, πλεονάζω, πικραίνω, ἀποτίθημι (an example's *to put aside,
  disregard*), ὀρτυγομήτρα (*the Ortygian mother*, Latona), ἀποθήκη, σάββατον (*of the week*), ὀφείλω, δέον,
  οἰκέω (examples' translations).
- **Morphology**: the pronouns for the manna are neuter, after αὐτό at 16:15 and 16:21; πᾶν τὸ πλεονάζον
  (16:23) is a hanging nominative, which αὐτό takes up; γομορ and μαν are names, printed in lower case and
  indeclinable, the plural of γομορ taken from δύο.
- New chains: συναγωγή `to bringing together`, `the bringing together`, `of the bringing together`; ἐξέρχομαι
  `of having gone out of`; ἀποθνήσκω `we died off`; πλήσσω `having been struck`; καθίζω `we made to sit
  down`; λέβης `of the kettles`; ἐσθίω `we were eating`, `you ate`; πλησμονή `filling`; λιμός `in hunger`;
  συλλέγω `will collect`, `you will collect`, `to collect`; πειράζω `I may make proof`; νόμος `to the anything
  assigned`; ἑτοιμάζω `will make ready`; εἰσφέρω `may carry into`; συνάγω `may bring together`; εἰσακούω `in
  the hearkening`, `the hearkening`, `has hearkened and given ear to`, `I have hearkened and given ear to`, `to
  hearken and give ear to`; δίδωμι `in the giving`; προσέρχομαι `come to`; ἐπιστρέφω `turned themselves
  round`; νεφέλη `in a cloud`; πίμπλημι `you will be filled full of`; ὀρτυγομήτρα `a bird which migrates
  with the quails`; καταπαύω `of being laid to rest`; πάγος `that which is fixed`; καθήκω `the ones having
  come`; συσκήνιος `to the ones who live in the same tent`; πολύς `the much`; μετρέω `having measured in any
  way`; πλεονάζω `was more`, `the thing being more`; ἐλαττονέω `received less`; καταλείπω `let leave behind`,
  `leave behind`; ἐκζέω `boiled out or over`; σκώληξ `worms`, `a worm`; πικραίνω `was made sharp`; τήκω `was
  being melted`; δέον `the things needful`; δύο `of two`; σάββατον `sabbaths`, `the sabbaths`; πέσσω `you may
  soften`, `soften`; ἕψω `you may boil`, `boil`; ἀποθήκη `any place wherein to lay up`; κάθημαι `you will be
  seated`; ἐκπορεύομαι `let go out`; γεῦμα `the taste`; ἀποτίθημι `you will put away`, `put away from himself`;
  μαρτύριον `of the testimony`; οἰκέω `being inhabited and occupied`; δέκατος `the tenth`; μέτρον `of things by
  which anything is measured`.
- One translation each, plain text: γογγυσμός (*a murmuring*), διαγογγύζω, πεντεκαιδέκατος, ἕκτος, κόριον
  (*coriander*), ἐπόζω (*become stinking*), διαθερμαίνω's active (*to warm through*), στάμνος (*an earthen jar
  for racking off wine*), σαββατίζω (*to keep the Sabbath*), μέλι, ἔτος, διατήρησις, ἐγκρίς, ὄφελον.

### Words new in EXO 17

- **From LSJ** (not in Middle Liddell): καταλιθοβολέω, `will throw stones at and stone`, one translation,
  citing 17:4.
- **Spelling** (`SPELLING`): δίψος under δίψα, Middle Liddell's *= δίψα*, *thirst*, plain text (17:3).
- **Cut translations restored** (`MARKUP_LOST`): πέτρα, *a rock, a ledge or shelf of rock*, *a rocky peak or
  ridge*; στηρίζω, *to be firmly set or fixed, to stand fast or steady*; καταγράφω, *to fill with writing*.
- **Form** (`FORM_SENSES`): λοιδορέω's middle reads the middle's *to rail at one another* and the deponent's
  *to rail at*, as its active reads the active's; ἐπιλέγω's, καθίημι's and στηρίζω's actives leave out the
  middle's and passive's; τρέπω's first aorist middle reads *to put an enemy to flight* alone, as the entry
  gives it (17:13, plain text).
- **Runs joined**: στηρίζω's *to make fast, prop, fix, set* had been split at GEN 27:37 and 28:12; both now
  read it as one item and carry *to fix, settle, determine*, and the participle the passive's *to be firmly
  set or fixed*, as 17:12 does.
- **Pieces set aside** (`NOT_SENSES`): δίψα, λοιδορέω, πέτρα (the note on πέτρος, examples'), ἐπιλέγω, καθίημι,
  στηρίζω, καταγράφω.
- **Names**: Πειρασμός and Λοιδόρησις, Greek words Rahlfs prints as the place's name, as GEN 26's wells:
  *Trial* and *Railing*, for the Hebrew Massâ and Mĕrîbâ. The altar's name, Κύριός μου καταφυγή, opens with a
  capital and is read as words, listed in `speech`.
- **Morphology**: τί ποιήσω (17:4) is deliberative, the aorist subjunctive, as the second pass had it, and
  reads `I may make`; πρεσβυτέρων is comparative, as the corpus mostly codes it.
- New chains: ῥῆμα `of that which is said`; ὕδωρ `to water`; λοιδορέω `was railing at one another`, `you rail at
  one another`; πίνω `we may drink`, `will drink`; πειράζω `you make proof`, `the making proof`; διψάω
  `thirsted`; γογγύζω `was muttering`; ἀναβιβάζω `you made go up`; καταλιθοβολέω `will throw stones at`;
  πρεσβύτερος `of the elders`; πατάσσω `you beat`, `you will beat`; πορεύομαι `you will be driven`; πέτρα `of the
  rock`, `the rock`; λοιδορία `the railing`; πολεμέω `was being at war`; ἐπιλέγω `choose`; δυνατός `strong`;
  παρατάσσω `draw up one's men in battle-order`, `drew up …` (singular); κορυφή `of the head`, `the head`; βουνός
  `of the hill`; κατισχύω `was having power over`; καθίημι `sent down`; βαρύς `heavy`; στηρίζω `were making fast`,
  `having been made fast`; δυσμή `of settings`; φόνος `in murder`; καταγράφω `scratch away`; μνημόσυνον `the
  remembrance`; βιβλίον `in a paper`; ἀλοιφή `to anything used for anointing`; καταφυγή `a refuge`; κρυφαῖος `to
  hidden`.
- One translation each, plain text: τρέπω's first aorist middle, δίψος, θυσιαστήριον (*an altar*).

### Words new in EXO 18

- **From LSJ** (not in Middle Liddell): ἀνυπομόνητος, `to unbearable, to not enduring` (18:18); πρωΐθεν, *from
  morning*, plain text (18:13, 18:14); συναντιλαμβάνομαι, `will help in gaining, will assist in supporting,
  will render assistance, will take part with and help`, citing 18:22.
- **Spelling** (`SPELLING`): κρίμα under κρῖμα; ἑκατόνταρχος under ἑκατοντάρχης, *leader of a hundred*, plain
  text.
- **A first sense outside the markup** (`MARKUP_LOST`): ἐλαφρός, "= Lat. lev-is light in weight", whose
  first sense stands outside every `<tr>`, the card opening with the adverb's *lightly*: `light in weight,
  light to bear and not burdensome and easy, light in moving and nimble, lightminded and thoughtless` (18:26).
  Also σημαίνω's *to give a sign or signal to do* and *to stamp with a sign or mark, to seal*, and
  ὑπερηφανία's *contempt towards or for*.
- **Form** (`FORM_SENSES`): μόχθος's singular leaves out the plural's; the actives of διακρίνω, συμβουλεύω,
  σημαίνω and κουφίζω the middle's and passive's.
- **Pieces set aside** (`NOT_SENSES`): ἄφεσις, ἀσπάζομαι, μόχθος (the note on μόχθος and πόνος), διακρίνω,
  συμβουλεύω, σημαίνω, ὑπερηφανία, χιλίαρχος (the Latin it translates), βραχύς, κουφίζω, ἐλαφρός.
- **The reflexive inside an article's phrase**: τῷ ἑαυτοῦ λαῷ, τὸν ἑαυτοῦ τόπον, τὸν ἑαυτοῦ γαμβρόν read the
  noun's unit with its article and *of himself* after it, so no *the* stands bare.
- New chains: γαμβρός `to the one connected by marriage`; ἱερεύς `the priest`; ἄφεσις `the letting go`; δύο `the
  two`; ἀσπάζομαι `welcomed kindly`; μόχθος `the toil`; ἀγαθός `to the goods`; εὐλογητός `blessed`; γινώσκω `I
  learned to know`; συνεσθίω `to eat together`; κρίνω `will separate` (plural), `were separating`; παρίστημι `has
  stood by`, `to stand by`; κάθημαι `you are seated`; ἐκζητέω `to seek out`; ἀντιλογία `contradiction`; διακρίνω
  `I separate one from another`; συμβιβάζω `I bring together`; φθορά `to destruction`; καταφθείρω `you will be
  destroyed`; συμβουλεύω `I will advise`; ἀναφέρω `you will bring up`, `will bring up`, `were bringing up`;
  διαμαρτύρομαι `you will protest solemnly`; σημαίνω `you will shew by a sign`; θεοσεβής `fearing God`;
  ὑπερηφανία `arrogance`; καθίστημι `you will set down and place`; χιλίαρχος `commanders of a thousand men`;
  ὑπέρογκος `the of excessive bulk`, `of excessive bulk`; βραχύς `the short`; κρίμα `of the decisions`; κουφίζω
  `will be light`; κατισχύω `will have power over`; ἐπιλέγω `chose`; ἐλαφρός `light in weight`.
- One translation each, plain text: συνάντησις (*a meeting*), μισέω's active (*hating*), πεντηκόνταρχος (*the
  commander of fifty men*), δεκάδαρχος (*a commander of ten*), ἑκατόνταρχος, πρωΐθεν.

### Words new in EXO 19

- **From LSJ** (not in Middle Liddell): γνοφώδης, `dark and gloomy`, one translation, citing 19:16.
- **Voice** (`FORM_SENSES`): βιάζω's middle and middle/passive read the middle's senses, as GEN 33:11 reads them:
  `let overpower by force and press hard, let do them violence, let lay violent hands on, let force, let use
  force and struggle, let force one's way, let increase in violence` (19:24). ἅπτω's middle reads the middle's,
  and its future middle the passive's *to be set on fire, catch fire* too, which the entry gives "with fut.
  mid.": `will fasten itself to and cling to and hang on by and lay hold of and grasp and touch, …, will be set
  on fire and catch fire` (19:13). ἀπαλλάσσω's active leaves out the passive's and middle's; προσάγω's middle
  the active's and passive's; ἀφορίζω's active the middle's *to mark off for oneself*, and its middle the
  active's *to mark off by boundaries*.
- **Runs joined, senses restored**: ἅπτω's middle had split *to fasten oneself to, cling to, hang on by, lay
  hold of, grasp, touch* into six items at GEN 3:3, 20:4, 20:6, 26:11, 32:26 and 32:33, and stopped before
  *to set upon, attack, assail*, *to touch, affect*, *to grasp with the senses, apprehend, perceive* and *to
  come up to, reach, gain*; all six now read the run whole and the four senses after it. GEN 26:11 had read
  *meddling with*, which the entry does not give. βιάζω at GEN 33:11 had split *to overpower by force, press
  hard* and stopped at *forced*; it now reads `overpowered by force and pressed hard, did them violence, laid
  violent hands on, forced, used force and struggled, forced one's way, increased in violence`.
- **Cut translations restored** (`MARKUP_LOST`), each the word's own English in that use with its object
  between, by open question Q7's test: βιάζω's *to do them violence*, προσάγω's *to draw all eyes upon
  oneself*; and πτέρυξ's *anything that covers or protects*, ἠχέω's *to let it sound*.
- **Pieces set aside** (`NOT_SENSES`): πτέρυξ (*wings*, the first sense's plural; *the wings*, a repeat),
  ἠχέω (examples'), πτοέω (an example's; the participle's as a noun), καπνός (a proverb's, an example's),
  θιγγάνω (*reach*, an example's), ἀπαλλάσσω (*from*), προσάγω (an example's; the participle's), ἅπτω
  (*touched on*, *red-hot*, examples'). `GREEK_AFTER`: ἀπαλλάσσω's *to leave off or cease from* τῶν μακρῶν
  λόγων is whole.
- **A middle with no middle sense**: ἁγίασαι (19:23) is the aorist middle imperative, by its accent; Middle
  Liddell gives ἁγιάζω no middle, so it reads `hallow`, as the active, with no *for yourself*. Ἀφόρισαι
  reads the middle's own `mark off for yourself`.
- **Names**: τὸ ὄρος τὸ Σινα reads the name in apposition, in the mountain's case (`the mountain the Sinai`), as
  τῷ ὄρει τῷ Γαλααδ at GEN 31:23; τοῦ Σινα (19:1, 19:2) is neuter, the mountain's.
- New chains: ἔξοδος `of the going out`; ἐξαίρω `lifted up` (plural); ποιέω `I have made`; ἀναλαμβάνω `I took
  up`; πτέρυξ `of wings`; ἀετός `of eagles`; προσάγω `I brought`; ἀκούω `we will hear`; περιούσιος `having more
  than enough`; βασίλειος `of the king`; παραγίνομαι `I am near`, the eight senses since EXO 36; διαμαρτύρομαι `protest solemnly`,
  `you have protested solemnly`; ἁγνίζω `cleanse away`; πλύνω `let wash`, `washed`; ἀφορίζω `you will mark off
  by boundaries`, `mark off for yourself`; θιγγάνω `to touch`; ἅπτω `the one having fastened himself to`, `will
  fasten itself to`; λιθοβολέω `will be pelted with stones`; βολίς `to a javelin`; κατατοξεύω `will be struck
  down with arrows`; κτῆνος `flock and herd`; σάλπιγξ `the war-trumpets`, `of the war-trumpet`; νεφέλη `the
  cloud`, `a cloud`; ἀπέρχομαι `may go away`; ἁγιάζω `let be hallowed`; γυνή `to a woman`; γίνομαι `of having
  come into being`; ἀστραπή `flashes of lightning`; γνοφώδης `dark`; ἠχέω `was sounding`; πτοέω `was
  terrified`; παρίστημι `stood by` (plural); καπνίζω `was being smoked`; καταβαίνω `the having stepped down`;
  ἰσχυρός `more strong`; ἐγγίζω `may bring near`, `the ones bringing near`; ἱερεύς `the priests`; ἀπαλλάσσω
  `may set free`; προσαναβαίνω `to go up`; βιάζω `let overpower by force`; ἀπόλλυμι `may destroy utterly`;
  ἀναβαίνω `to go up`, `of the going up`; λίθος `in stones`.
- One translation each, plain text: ἱεράτευμα (*a priesthood*), ὁμοθυμαδόν (*with one
  accord*), σήμερον (*to-day*), συνάντησις (*a meeting*), τρεῖς (*three*), καπνός (*smoke*).

### Words new in EXO 20

- **From LSJ** (not in Middle Liddell): μακροχρόνιος, `lasting a long time and lingering, dwelling a long time,
  long-lived`, citing 20:12, the neuter's *long duration* left to the noun; ἀναβαθμίς, `in steps and stairs`
  (with ἐν), one translation, citing 20:26.
- **A noun filed inside its adjective** (`SPELLING`): ἐγχειρίδιον under ἐγχειρίδιος, "as Subst., ἐγχειρίδιον …
  a hand-knife, dagger"; the adjective's *in the hand* is set aside for the noun (`NOT_SENSES` by the noun's
  key): `the hand-knife and dagger` (20:25).
- **The wrong homograph** (`ENTRY`): ἄνω read Middle Liddell's first entry, the verb *to accomplish*; the
  adverb is the second. Its card leaves out the phrases' (*the living*, *the dead*, *the gods above*, *up and
  down*, *upside down*), the comparative's and superlative's, and the *i. e. inland* that glosses *up the
  country*: `up and upwards, up the country, up and aloft and on high, on earth, in heaven, in the upper
  quarter, on the north and northward, inward from the coast, formerly and of old, above`.
- **Form** (`FORM_SENSES`): τιμάω's active leaves out the passive's and the middle's (`pay honour to and hold in
  honour and honour and revere and reverence, …, condemn, fix`, 20:12); φονεύω's the passive's *to be slain*.
- **Pieces set aside** (`NOT_SENSES`): κάτω (the comparative's and superlative's), ζηλωτής (the Hebrew *qana*
  of the NT's note), μάταιος (τὸ μὴ μάταιον's, the adverb's), οὔτε (the construction with τε), ψευδής (a repeat;
  the noun's, examples', the neuter plural's, the adverb's), τιμάω (examples' pieces).
- **οὔτε** is opened by its parse, the conjunction: `and not, neither nor, nor`, as τε reads `and, both and,
  and also`.
- **The neuter adjective as a noun, without an article**: ἐπὶ ματαίῳ reads `upon to vain and empty and idle
  and trifling and frivolous, …`, no noun added (20:7).
- **ἐν before a numeral**: ἐν ἓξ ἡμέραις (20:11), where ἕξ is plain text between ἐν and its noun, gives ἐν a
  unit of its own: `in for, to six to days`.
- **Morphology**: μεμίανται (20:25) is the perfect's third singular, as the module codes it; both passes had
  read it plural. ἐάν after a relative (οὗ ἐάν, 20:24) is the particle, plain *ever*, as at 16:5.
- New chains: ἐξάγω `I led out`; εἴδωλον `an image`; ὁμοίωμα `a likeness`; οὐρανός `in the heaven`; κάτω
  `down`; ὕδωρ `in the water`; προσκυνέω `you will make obeisance`; λατρεύω `you may work for hire`; ζηλωτής
  `an emulator`; ἀποδίδωμι `giving up`; ἁμαρτία `failures`; πατήρ `of fathers`; τέταρτος `of fourth`; ἀγαπάω
  `to the ones treating with affection`; φυλάσσω `to the ones keeping watch and ward`; μάταιος `to vain`;
  καθαρίζω `may make clean`; λαμβάνω `the one taking`; σάββατον `of the sabbaths`; ἁγιάζω `to hallow`; βοῦς `the
  bullock`, `of the bullock`; ὑποζύγιον `the beast for the yoke`, `of the beast for the yoke`; προσήλυτος `the one
  that has arrived at`; παροικέω `the one dwelling beside`; ἡμέρα `to days`; τιμάω `pay honour to`; γίνομαι `you
  may come into being`; ἀγαθός `of the good`; δίδωμι `gives`, the present's five; μοιχεύω `you will commit
  adultery with`; κλέπτω `you will steal`; φονεύω `you will murder`; ψευδομαρτυρέω `you will be a false
  witness`; μαρτυρία `witness`; ψευδής `lying`; ἐπιθυμέω `you will set your heart upon`; οὔτε `and not`; ὁράω `was
  seeing`; λαμπάς `the torches`; καπνίζω `the thing making smoke`, the active; φοβέομαι `having been put to
  flight`; λαλέω `let talk`, `I have talked`; πειράζω `of the making proof`; ἁμαρτάνω `you may miss the mark`;
  γνόφος `the darkness`; θύω `you will offer`; ὁλοκαύτωμα `the whole burnt-offerings`; σωτήριος `the
  deliverances`; μόσχος `the calves`; ἐπονομάζω `I may give a surname`; λίθος `of stones`; οἰκοδομέω `you will
  build a house`; τμητός `cut`; ἐπιβάλλω `you have thrown`; μιαίνω `has been stained`; ἀναβαίνω `you will go up`;
  ἀποκαλύπτω `you may uncover`; ἀσχημοσύνη `the want of form`.
- One translation each, plain text: ἕξ (*six*), υἱός, θυγάτηρ, μισέω's active (*the ones hating*),
  θυσιαστήριον (*an altar*). The relative ὅστις is plain *who*, as ἥτις reads *which* at 9:18.

### Words new in EXO 21

- **From LSJ** (not in Middle Liddell): κατάκαυμα, `anything burnt, fiery inflammation, burning`, the plural's
  *burnt parts* and *burns* left to the plural; κερατίζω, `may butt with horns, may gore`; κερατιστής, *one that
  butts*, plain text; λατομέω, `may quarry, may hew it out`; προσαποθνήσκω, `will die besides and with`, *die
  besides or with* whole; ἐξεικονίζω, `having been explained by a simile and standing so, having been fully
  shapen and formed, having been exactly like` (21:22, 21:23).
- **In neither lexicon**: ὀπήτιον (21:6), plain text, *to the awl*, as σφυροκόπος at GEN 4:22.
- **Filed inside another word** (`SPELLING`): δούλη under δοῦλος, "Hom. has only the fem. δούλη, a
  bondwoman", the masculine's and the adjective's senses set aside by δούλη's own key: *the bondwomen*, plain
  text (21:7).
- **Cut translations restored** (`MARKUP_LOST`): συνεισέρχομαι, *to enter along with or together*; κριτήριον, *a
  means for judging or trying, a criterion, standard, test*; τρυπάω, *to force the point through*; ἀθετέω,
  *refuse his request*; ζημιόω, *will suffer great losses* and *to be fined or amerced in*; πυγμή's measure, *the
  distance from the elbow to the knuckles*, the `<tr>` having run on into "= 18 δάκτυλοι".
- **Form** (`FORM_SENSES`): ἀποστερέω's active leaves out the passive's; δίκη's other cases the accusative's
  *after the manner of*.
- **Pieces set aside** (`NOT_SENSES`): ἐλεύθερος, συνεισέρχομαι, κριτήριον, τρυπάω, ἀθετέω, ὁμιλία (repeats of
  the first sense), ἀποστερέω, πυγμή (the NT's interpretation by πύκα and πυκνά), κατακλίνω (an example's
  participle), δίκη (repeats; the phrases δίκην διδόναι, λαμβάνειν, ὀφλεῖν, αἰτεῖν), ζημιόω, ἐπιζήμιος, λύτρον,
  γνωρίζω, ἀξίωμα.
- **The dative's own English**: πυγμῇ's *with the fist, in boxing* and δίκῃ's *duly, rightly* carry no *to*, as
  βίᾳ (open question Q4).
- **Runs joined**: ἐκδικέω at GEN 4:15 and 4:24 had split *to avenge, punish* and stopped short of *to avenge*
  and *to avenge one on another*; both now read the card's four, as 21:20 and 21:21 do.
- **Morphology**: the second pass was right on six: the heading's ταῦτα τὰ δικαιώματα (21:1), τὰ παιδία (21:4)
  and τὰ κρέα (21:28) are nominative; καί at 21:3 is *also*, twice; πλήν at 21:19 is the conjunction, *only*,
  τῆς ἀργίας the genitive ἀποτίνω governs. αὑτῷ at 21:8 is the reflexive, a misreading of the scan corrected.
- New chains: δικαίωμα `the act by which wrong is set right`; παρατίθημι `you will place beside`; κτάομαι `you may
  procure for yourself`; ἐλεύθερος `free`; συνεισέρχομαι `may enter along with`; τίκτω `may bring into the world`;
  ἀγαπάω `I have treated with affection`; ἀποτρέχω `I run off`; προσάγω `will bring to`; κριτήριον `the means for
  judging`; σταθμός `the standing place`; τρυπάω `will bore`; οὖς `the ear`; ἀποδίδωμι `may give away of his own
  will`, `will give away of their own will`; εὐαρεστέω `may be well pleasing`; καθομολογέω `confessed`, `may
  confess`; πωλέω `to exchange`; ἀθετέω `set aside`; λαμβάνω `may take`; ἱματισμός `the clothing`; ὁμιλία `the
  being together`; ἀποστερέω `will rob`; θανατόω `let be put to death`; ἑκών `willing`; φεύγω `will flee`; φονεύω
  `the one having murdered`; ἐπιτίθημι `may put on himself`; δόλος `to a bait`; καταφεύγω `may flee for refuge`;
  τύπτω `beats`; κακολογέω `the one speaking ill of`; τελευτάω `may complete`, `let complete`, `the thing having
  completed`, `the one having completed`; κλέπτω `may steal`; λοιδορέω `may rail at one another`; λίθος `to a
  stone`, `to stones`; πυγμή `to a fist`; κατακλίνω `may be laid down`; περιπατέω `may walk up and down`; ῥάβδος
  `of a rod`, `in a rod`; ἀργία `of the idleness`; ἀποτίνω `will pay back`; δίκη `to custom`; ἐκδικέω `let be
  avenged`, `will be avenged`; διαβιόω `may live through`; μάχομαι `may fight`; ἐπιζήμιος `bringing loss upon`;
  ζημιόω `will be caused loss`; ἐπιβάλλω `may throw`, `may be thrown`; ἀξίωμα `of that of which one is thought
  worthy`; ὀφθαλμός `eye`, `of eye`, `the eye`, `of the eye`; πούς `of foot`; τραῦμα `of a wound`; μώλωψ `of mark of
  a stripe`; οἰκέτης `of the house-slave`; κερατίζω `may butt with horns`; διαμαρτύρομαι `may protest solemnly`,
  `having protested solemnly`; ἀφανίζω `may make unseen`; ἀναιρέω `may take up and raise`; λύτρον `prices paid`;
  ἀνοίγω `may open`; λάκκος `a pond`; καλύπτω `may cover with`; ἐμπίπτω `may fall in`; μόσχος `a calf`, `of the
  calf`; ὄνος `an ass`; ζάω `the one living`; διαιρέω `will take one from another`, the middle's with it; θνήσκω
  `the one being dead`; γνωρίζω `may be made known`; σφάζω `may slay`; πρόβατον `of the thing that walks forward`.
- One translation each, plain text: ἔτος (*a year*), ἀπολυτρόω (*will release on payment of ransom*), οἰκέτις
  (*mistress of the house*), καταδυναστεύω (*having exercised power over*), ἰατρεῖον (*the surgeries*), ἐκτυφλόω
  (*may make quite blind*), ὀδούς (*a tooth*), ταῦρος (*a bull*), καθότι (*in what manner*), ἐχθές, τρεῖς,
  τριάκοντα, πέντε, τέσσαρες.

### Words new in EXO 22

- **From LSJ** (not in Middle Liddell): προσεμπίμπρημι, under προσεμπίπρημι, *set on fire besides*, plain text;
  φερνίζω, `will portion and endow`; ἀμνήστευτος, `unwooed and not sought in lawful wedlock`; ἀνταποθνήσκω, `will
  die and be killed in requital`, *die or am killed in requital* whole; ἐκδανείζω, *lend out at interest*, plain
  text; ἐνεχύρασμα, `pledge and thing pawned`.
- **Filed inside another word** (`SPELLING`): κακῶς under κακός, as καλῶς under καλός: `ill, evil`, the adverb's
  own translations (22:27).
- **A first sense inside the Latin** (`MARKUP_LOST`): ὀρφανός, "Lat. orbus, orphan, without parents, fatherless".
  Also καταβόσκω's *to feed flocks upon or in*, ἀπορρίπτω's *to shoot forth bold, keen words*, ἁλίσκομαι's *to be
  caught or detected*.
- **Form** (`FORM_SENSES`): ἐνεχυράζω's active leaves out the passive's and the middle's; πιπράσκω's passive its
  own *to be sold*, which is the first sense in the passive, so πραθήτω is plain text, *let be sold*.
- **Pieces set aside** (`NOT_SENSES`): τόκος (*compound interest*, a phrase's), ἀπορρίπτω, ἀνανεύω (the gloss of a
  gesture), χήρα (χῆρος's senses, the masculine and the adjective formed from χήρα, and an example's), καταβόσκω,
  ἐγκαλέω (a repeat cut by its object), ἁλίσκομαι.
- **Runs joined**: χήρα at GEN 38:11 had split *bereft of a husband, a widow* and taken in χῆρος's *widowed,
  bereaved* and a piece, *torn from*; it reads `bereft of a husband and a widow`. παρθένος at GEN 24 and 34 had
  split *a maid, maiden, virgin, girl*; ἀδίκημα at GEN 31:36 *a wrong done, a wrong*.
- **Morphology**: the second pass was right on six: ὄνου is masculine, any ass in a list (22:3); ζῶντα is
  nominative, with τὸ κλέμμα; αὐτοῦ at 22:10, 13 and 14 is neuter, the animal; πλήν before a dative is the
  conjunction (22:19); χήρα is A-, as at GEN 38:11. ὅσον after κατά stays accusative.
- New chains: διόρυγμα `in the through-cut`; κλέπτης `the thief`; ἀνατέλλω `may make to rise up`; ὑπάρχω `may
  begin`; κλέμμα `of the theft`, `the theft`; καταλαμβάνω `may be seized upon`; πρόβατον `of thing that walks
  forward`; καταβόσκω `may feed flocks upon`, `to feed flocks upon`; ἀγρός `field`; ἀφίημι `may send forth`; κτῆνος
  `the flock and herd`; βέλτιστος `the best`; ἅλων `of a threshing-floor`; ἐκκαίω `the one having burned out`;
  κλέπτω `may be stolen`, `the one having stolen`; ὄμνυμι `will swear`; πονηρεύομαι `to have been evil`; ἀδίκημα `a
  wrong done`; μόσχος `of a calf`, `the calf`; ὑποζύγιον `of a beast for the yoke`, `a beast for the yoke`; ἱμάτιον
  `of outer garment`; ἐγκαλέω `of the one being called in`; ἔρχομαι `will come`; κρίσις `the separating`; ἁλίσκομαι
  `the one having been taken`; συντρίβω `may be rubbed together`; αἰχμάλωτος `taken by the spear`; γινώσκω `may
  learn to know`; ὅρκος `object by which one swears`; ἄγω `will lead`; αἰτέω `may ask`; μισθός `of the wages`;
  ἀπατάω `may cheat`; παρθένος `a maid`, `of the maids`; κοιμάω `may be lulled`, `will be lulled`, `being lulled`;
  φερνή `to that which is brought by the wife`, `the that which is brought by the wife`; ἀνανεύω `throwing the head
  back`, `may throw the head back`; βούλομαι `may will`; φαρμακός `poisoners`; περιποιέω `you will keep`;
  ἀποκτείνω `you will kill`; θεός `to gods`; προσήλυτος `ones that have arrived at`; κακόω `you will treat ill`,
  `you may treat ill`; θλίβω `you may press`; χήρα `bereft of a husband` (plural); ὀρφανός `an orphan`, `orphan`;
  κράζω `having croaked`; καταβοάω `may cry down`; εἰσακούω `I will hearken`; ὀργίζω `I will be made angry`; θυμός
  `to soul`; πενιχρός `to the poor`; κατεπείγω `pressing down`; τόκος `a bringing forth`; ἐνεχυράζω `you may take a
  pledge from`; περιβόλαιον `that which is thrown round`; ἀσχημοσύνη `of want of form`; ἐλεήμων `pitiful`;
  κακολογέω `you will speak ill of`; κακῶς `ill`; ἀπαρχή `beginnings of a sacrifice`; ληνός `of a tub`; καθυστερέω
  `you will come far behind`; κύων `to the dog`; ἀπορρίπτω `throw away`.
- One translation each, plain text: ἀμπελών, γένημα, παρακαταθήκη, ἀπώλεια, θηριάλωτος, θυσιάζω, ὀλεθρεύω,
  πρωτότοκος, ὄγδοος, ἑπτά.

### Words new in EXO 23

- **From LSJ** (not in Middle Liddell): θυσίασμα, "= θυσία II", read as θυσία's `victim and offering`; πρωτογένημα,
  *firstfruits*, plain text; ἐχθρεύω, *to be at enmity with*, citing this chapter, plain text. ἐμπλατύνω is in
  neither lexicon: plain text, *I may widen*, from πλατύνω, as σφυροκόπος at GEN 4:22 (23:18).
- **Filed inside another word** (`SPELLING`): σφηκία under σφηκιά, *a wasps' nest*, plain text. πλείων is filed under
  πολύς, as at 1:12, and reads the positive's senses in the comparative: `of more and mightier and greater, …` (23:2).
- **Inside the Latin** (`MARKUP_LOST`): ἐλαιών, "«an olive-yard», Lat. olivetum: the Mount of Olives, Olivet" —
  `the olive-yard, the Mount of Olives and Olivet`. φυγάς's "Lat. exul, profugus" is Latin throughout (`LATIN_ONLY`).
- **Cut translations restored** (`MARKUP_LOST`): συγκατατίθημι *to deposit together or at the same time*;
  λυμαίνομαι *to inflict indignities or outrages upon*; πτωχός *one who crouches or cringes, a beggar*; ἀναψύχω
  *to let rest and get dry, relieve*, *to let it dry off*, *to give him relief from*; ὑποστέλλω *made him furl*,
  *to shelter oneself behind*, *to cloak through fear, to prevaricate, dissemble*; δικαιόω *to hold or deem right,
  think fit, demand*, *to do a man right or justice, to judge*; ἐξίστημι *to drive one out of*; συναγωγή *a forming
  in column*. An example's object noun is left out, as ὑπάγω's "a person" is (the ships, a thing, an army); a
  pronoun between the pieces stays, as ἠχέω's "it".
- **Form** (`FORM_SENSES`): συγκατατίθημι's middle and ὑποστέλλω's read the middle's senses; συνεγείρω's active
  leaves out the passive's (*to help in raising*, plain text); ἀναψύχω's active leaves out the passive's; πτωχός's
  masculine and neuter leave out the feminine's *a beggar-woman*; δικαιόω's active leaves out the passive's
  *proved, tested*, and its passive the active's constructions with an infinitive, *to consent*, *to desire*;
  ἀναπαύω's middle reads the Mid. and Pass. section, *to halt, rest* included; ἐξίστημι's future active is causal
  and leaves out the intransitive senses.
- **Pieces set aside** (`NOT_SENSES`): πένης (πτωχός's *(beggar)*), συντέλεια (a phrase's), ἀντίκειμαι (the
  adverb's), ἄγριος (a label, the comparative's, a phrase's, the adverb's), ἄδικος (a piece, the neuter's as a noun,
  the adverb's), ἐρῆμος (the neuter plural's as an adverb, ἐρήμη δίκη's phrases), δικαιόω (a phrase's, οὐ δ.).
- **Old chains re-read**:
  - ἄδικος, GEN 19:8: *wrong-doing, unrighteous, unjust* is one translation, and *unjust in*, *so unjust as to* had
    been dropped: `wrong-doing and unrighteous and unjust, unjust in, so unjust as to, obstinate and unmanageable,
    wrongly done and wrong and unjust`.
  - ἐνιαυτός: *any long period of time, a cycle, period* is one translation: `of the long period of time and cycle
    and period, of the year`, `of long periods of time and cycles and periods, of years`, and with ἐν.
  - συναγωγή: *a forming in column*, *a pursing up*, *wrinkling*, *a collection*, *a conclusion, inference* had been
    dropped from every chain; GEN 35:11 read `gatherings, assemblies`, which the card never gave, and reads
    `bringings together …` with the rest.
  - ἐρῆμος: *desolate, helpless* is one translation; *reft of, void* or *destitute of* two; *wanting, without* had
    been dropped: `the desert part, the desolate and lone and lonely and lonesome and solitary, the desolate and
    helpless, the reft of and void, the destitute of, the wanting and without, the undefended`.
  - δικαιόω, GEN 38:26 and 44:16: `has been held and deemed right and thought fit and demanded and it stands so,
    has been done right and justice and judged and it stands so`.
  - ἀναπαύω, GEN 29:2 and 49:14: the middle's `halting and resting`.
  - ὑπολείπω, EXO 10:12, `reserved for herself`; ἀποστρέφω, GEN 15:16, `they will turn themselves about`.
- **Morphology**: the second pass was right on six: πλειόνων is filed under πολύς, GPCC; τὰ ὑπολειπόμενα is the
  object, accusative (23:11); ἐάν after ὧν is X- (23:16); ἕως ἄν is the conjunction (23:30). σπείρῃς stays aorist,
  as GEN 47:19's σπείρωμεν.
- New chains: παραδέχομαι `you will receive from`; ἀκοή `a hearing`; μάταιος `vain`; συγκατατίθημι `you will agree
  with`; ἄδικος `of the wrong-doing`, `of wrong-doing`; πολύς (comparative) `of more`; προστίθημι `you will be put
  to`; ἐκκλίνω `to bend out of the regular line`; πένης `one who works for his daily bread`, `of one who works for
  his daily bread`; ἐλεέω `you will have pity on`; κρίσις `in a separating`; συναντάω `you may meet face to face`;
  βοῦς `to the bullock`; ἐχθρός `of the one's enemy`, `to the one's enemies`; ὑποζύγιον `to the beast for the
  yoke`; πλανάω `to being made to wander`; ὁράω `you may see`, `you will be seen`; πίπτω `having fallen`; γόμος `the
  ship's freight`; διαστρέφω `you will turn different ways`; κρίμα `a decision`; ἀφίστημι `you will stand away`;
  δικαιόω `you will set right`; δῶρον `of gifts`; ὀφθαλμός `eyes`; βλέπω `of seeing and having the power of sight`;
  λυμαίνομαι `treats with indignity`; ῥῆμα `things which are said`; θλίβω `you will press`; προσήλυτος `of the one
  that has arrived at`; σπείρω `you will sow`, `you may sow`; συνάγω `you will bring together`; ἄφεσις `a letting
  go`; πτωχός `the ones who crouch`; ἔθνος `of the number of people accustomed to live together`; ὑπολείπω `the
  things being left behind`; ἄγριος `the living in the fields`; θηρίον `wild animals`; ἐλαιών `the olive-yard`;
  ἀναπαύω `may desist from`; ἀναψύχω `may cool`; λέγω `I have said`; φυλάσσω `keep watch and ward for
  yourselves`, `may keep watch and ward`; θεός `of gods`; ἕτερος `of other`; ἀναμιμνήσκω `you will be reminded`;
  ἀκούω `may be heard`, the passive's first; ἑορτάζω `keep festival`; ἑορτή `the feast`, `of the feast`; ἄζυμος
  `of the unleavened`; συντέλεια `of a joint payment`; ἔξοδος `of a going out`; συναγωγή `in the bringing
  together`; ἐκβάλλω `I may throw`, `I will throw`; ζύμη `to leaven`; θυσίασμα `of victim`; στέαρ `stiff fat`;
  ἀπαρχή `the beginnings of a sacrifice`; ἕψω `you will boil`; ἀρήν `a lamb`; ἑτοιμάζω `I made ready`; εἰσακούω
  `hearken and give ear to`; ἀπειθέω `be disobedient`; ὑποστέλλω `may cloak through fear`; ἐντέλλομαι `I may
  enjoin`; ἀντίκειμαι `I will be set over against`, `to the ones being set over against`; εἰσάγω `will lead in`;
  ἐκτρίβω `I will rub out`; καθαίρεσις `to a pulling down`; καθαιρέω `you will take down`; στήλη `the blocks of
  stone`; ἄγονος `unborn`; ἀριθμός `the number`; ἀναπληρόω `I will fill up`; ἐξίστημι `I will put out of its
  place`; εἰσπορεύομαι `you go into`; φυγάς `ones who flee`; ἐνιαυτός `in any long period of time`; ἐρῆμος
  `desolate`; αὐξάνω `you may be made large`; κληρονομέω `you may receive a share of an inheritance`; παραδίδωμι
  `I will give`; ἐγκάθημαι `the ones sitting in or on`, `they will sit in or on`; ἁμαρτάνω `to miss the mark`;
  δουλεύω `you may be a slave`; ποιέω `they may make`; πρόσκομμα `a stumble`.
- One translation each, plain text: μάρτυς, συνεγείρω (the active), ἐκτυφλόω, γένημα, ἀμπελών, ἀρσενικός, γάλα,
  οἶνος, σφηκία, πρωτογένημα, ἐχθρεύω.

### Words new in EXO 24

- **From LSJ** (not in Middle Liddell): προσπορεύομαι, `let them go to and approach, let them apply, let them take
  up, let them make a start and get on with, let them go in quest of, let them be candidate for, let them hunt for,
  let them encroach on, let them draw near and approach` (24:14).
- **Filed under another spelling** (`SPELLING`): ἀναγινώσκω under ἀναγιγνώσκω. ἀνέγνω, the second aorist, reads
  `knew well and knew certainly, knew again and recognised and acknowledged and owned, knew them again, read`; the
  Ionic first aorist's *to persuade* or *induce* and its passive are left to those forms (`FORM_SENSES`, by form).
- **γράφω**, its first here: `scratched and scraped and grazed, represented by lines drawn and delineated and drew
  and painted, expressed by written characters and wrote, wrote a person's name, inscribed, wrote down, set him
  down, registered and enrolled, proposed and moved, moved that`; the middle's and the passive's senses (*to write
  for oneself*, *to indict*, *denounce*, *to be indicted*) left to those voices.
- **Cut translations restored** (`MARKUP_LOST`): γράφω *to write a person's name*, *to write for oneself or for
  one's own use, note down*; ἀναγιγνώσκω *to know them again*; προσχέω *to pour to or on*; νομοθετέω *it hath been
  ordained by law*; κατασκεδάννυμι *pour upon or over*, *to spread against*, *to pour or sprinkle about*; φλέγω
  *making it blaze or flash*, *letting blaze up*, *to make illustrious or famous*, *to be or become so*.
  ἐγχέω's "to fill the κλεψύδρα" is restored (`GREEK_LOST`) and set aside as a phrase's.
- **Form** (`FORM_SENSES`): the actives of νομοθετέω, ἐγχέω, κατασκεδάννυμι and φλέγω leave out the middle's and
  the passive's; ἡσυχάζω is "causal in aor1", and its other tenses leave out *to make still, lay to rest*.
- **Pieces set aside** (`NOT_SENSES`): διαφωνέω's *with*; κρατήρ's *bowls of wine*, an example's plural; ἡσυχάζω's
  *finding rest* and *by resting from war*, examples', as the corpus's `be still and keep quiet and at rest`
  already read it.
- **Morphology**: the second pass was right on three: τὸ αἷμα after ἰδού is nominative (24:8), and οὐδὲ εἷς is the
  adverb, as at 14:28. Σινα stays appositional after τὸ ὄρος τό, as at 19:20.
- **Names**: the check that a name is glossed once keys by the anchored form, so Μωυσῇ, Μωυσῆς and Μωυσῆν, all
  *Moses*, share one key, while EXO 23's Αμορραῖον and Αμορραίους, *Amorite* and *Amorites*, take two.
- New chains: ἐγγίζω `will bring near`, `they will bring near`; φωνή `to sound`; γράφω `scratched`, `I scratched`;
  ὀρθρίζω `having risen early`; φυλή `races`; ἀναφέρω `brought up` (plural); σωτήριος `of deliverance`; ἥμισυς `the
  half`; ἐγχέω `poured in`; κρατήρ `mixing vessels`; προσχέω `poured to`; βιβλίον `the paper`; ἀναγινώσκω `knew
  well`; λέγω `they said`; κατασκεδάννυμι `scattered`; λόγος `of the words`; γερουσία `of the Council of Elders`;
  ὁράω `they saw`, `were seen`; σάπφειρος `of sapphire`; εἶδος `that which is seen`, `the that which is seen`;
  στερέωμα `of a solid body`; καθαριότης `to the cleanliness`; ἐπίλεκτος `of the chosen`; διαφωνέω `was
  dissonant`; νομοθετέω `to make law`; παρίστημι `the one having stood by`; πρεσβύτερος `to the elders`; τις `to any
  one`; προσπορεύομαι `let them go to`; φλέγω `burning`; μέσος `the middle`.
- One translation each, plain text: συναναβαίνω, θυσιαστήριον, νεανίσκος, μοσχάριον, πλίνθος, πυξίον, λίθινος, and
  the numerals.

### Words new in EXO 25

- **From LSJ** (not in Middle Liddell): γλυφή `the carving and carved work, the emblem and device, the work, the hole
  cut`; θυΐσκη *censer*, plain text; καρυΐσκος, "Dim. of κάρυον", read as κάρυον's `any kinds of nut, walnuts`;
  κυμάτιον, "Dim. of κῦμα I.3", read as that sense, `waved mouldings and cymas, volutes, grooves`; λυχνία
  *lampstand*, plain text; σπονδεῖον `the cups from which the spondē (σπονδή) was poured, the bowls, the
  pouring-cups`; ἀναφορεύς `bearers and bearing-poles`; ἄσηπτος `not liable to decay and corruption, undigested`,
  its *of Acacia tortilis* the phrase ξύλα ἄσηπτα's; ἐπίθεμα `cover, capital, remedy for external application,
  addition, higher bid, shaft`; ἐπαρυστήρ *vessel for pouring oil into a lamp*, plain text; ἐρυθροδανόω `having
  been dyed with madder and dyed red and standing so`; ὑπόθεμα *base*, plain text.
- **Filed inside another word** (`SPELLING`): ἱλαστήριον inside ἱλαστήριος, "as Subst., the mercy-seat", the
  adjective's *propitiatory* set aside: `the mercy-seat, the propitiation`. παλαιστής under παλαστή, as LSJ's
  second entry points, since Middle Liddell's παλαιστής is a wrestler: `of palm of the hand, of a palm and four
  fingers' breadth`.
- **Inside the entry** (`MARKUP_LOST`): τράπεζα's first <tr> took in τετράπεζα's gloss, *four-legged a table*; *a
  table* is restored. Cuts restored: αἴγειος *of a goat or goats*; στρεπτός *a collar of twisted or linked metal*,
  *to be bent or turned*, *glib, pliant*; συσκιάζω *… shade closely or thickly*; ἀκίνητος *not to be stirred or
  touched, inviolate*; τύπος *the sound of their tread*, *anything wrought of metal or stone*; φαίνω *to make it
  clear*, *to inform of as contraband*; ἐλαύνω *to drive to extremities*, *to drive or thrust through*, *to beat
  with a hammer*, *to draw a line of wall or a trench*, *plant them in line*.
- **Form** (`FORM_SENSES`): στρεπτός's neuter and feminine leave out the masculine noun's; τάλαντον's and τύπος's
  singular the plural's (*a pair of scales*, *figures worked in relief*); χρυσόω's, ἐλαύνω's and φαίνω's active
  the passive's — φαίνω's the middle's and the passive's examples too, so its future reads `they will bring to
  light and make to appear, …, they will give light`.
- **Pieces set aside** (`NOT_SENSES`): ὑάκινθος (the entry's prose on the flower's colours, and "not (prob.) our
  jacinth"), θρίξ, ποδήρης (the examples' frock and shield; the neuter plural's), παράδειγμα, τράπεζα (Horace's
  *Siculae dapes*; *bankers*, a phrase's), ἐπάνωθεν, καταχρυσόω (*splendid*, the gloss of *golden*), λύχνος,
  στεφάνη, κλώθω, τάλαντον (*l.*, and "no such coin"), ἐλαύνω's examples.
- **σπένδω** keeps GEN 35:14's three: `you will pour a drink-offering, you will make a drink-offering, you will pour`.
- **Morphology**: Rahlfs prints no verse 6. The second pass was right on ten: ἡμίσους masculine, with the cubit
  understood (six times); ἄνωθεν before a genitive a preposition (25:22), as ἐπάνω is; τρύβλιον as Middle Liddell
  accents it; οἷς and αὐτοῖς at 25:29 neuter, with the vessels. ὑάκινθος feminine (Q22), διὰ παντός neuter,
  καρυΐσκος with LSJ's diaeresis. χερουβιμ is neuter at 25:18 and masculine at 25:19–22, as its words show.
- New chains: the forms of the furnishings above; ἐλαύνω `you will drive`; δοκέω `may think`; ἀπαρχή `the beginning
  of a sacrifice`; χαλκός `copper`; πορφύρα `purple-fish`; βύσσος `a fine flax`; κλώθω `having been twisted by
  spinning`; θρίξ `hairs of the head`; αἴγειος `of a goat`; δέρμα `skins`; κριός `of rams`; σάρδιον `of Sardian
  stone`; ἐπωμίς `the point of the shoulder`; ποδήρης `the reaching to the feet`; δείκνυμι `I bring to light`, `the
  one having been brought to light`; παράδειγμα `the pattern`; μαρτύριον `of a testimony`, `the testimonies`;
  ἥμισυς `of half`; πῆχυς `of fore-arm`; καταχρυσόω `you will cover with gold-leaf`; χρυσόω `you will make golden`;
  καθαρός `to clear of dirt`, `of clear of dirt`; δακτύλιος `rings`, `the rings`; ἐμβάλλω `you will throw in`;
  δίδωμι `I may give`; τορευτός `worked in relief`; ποιέω `they will be made`; πτέρυξ `the wings`, `to the wings`;
  ἐπάνωθεν `from above`; συσκιάζω `shading quite over`; γινώσκω `I will be learned to know`; λαλέω `I will talk`;
  εἰμί `of the ones being`; τράπεζα `a table`, `the table`; εὖρος `the breadth`; στεφάνη `anything that encircles`
  and its articular forms; θήκη `cases to put anything in`; αἴρω `will be taken up`; τρύβλιον `the cups`; κύαθος
  `the cups`; σπένδω `you will pour a drink-offering`; καυλός `the shaft`; κρατήρ `the mixing vessels`; σφαιρωτήρ
  `thong`, `the thong`, `the thongs`; ἐκπορεύομαι `going out`, `to the ones going out`; εἷς `of the one`, `in the
  one`; ἐκτυπόω `having been modelled`; λύχνος `the portable lights`; φαίνω `they will bring to light`; τάλαντον `a
  balance`; τύπος `the blow`.
- One translation each, plain text: κόκκινος, ὑακίνθινος, κλίτος (*= κλίμα II, a clime*), καλαμίσκος, κρίνον,
  ἐνώπιος, ἀλλήλων, and the numerals.

### Words new in EXO 26

- **From LSJ** (not in Middle Liddell): αὐλαία `curtains, hunting-nets, screens`, the singular without the plural's
  *screens*; ἀγκωνίσκος, "= foreg.", ἀγκωνίσκιον, "Dim. of ἀγκών", read as Middle Liddell's ἀγκών (Q20): `bends of
  the arm and elbows, arms, any bends, jutting angles, bends, reaches, angles`; κατακάλυμμα `covering and veil`;
  σύμβλησις `union: a joint, comparison, reference to, interpretation, assistance`; ἐπίσπαστρον `rope for pulling,
  net, the latch or handle by which a door is pulled to, that which is drawn over and curtain and hanging`, its
  "= ἐπισπαστήρ 1" read as that entry; ἐπιδιπλόω `you will make double, you will fold double, you will multiply by
  two`; ἐπικάλυμμα `covers and veils, coverings, gills, opercula`. ὑποκαλύπτω is in neither lexicon: plain text,
  *you will cover under*, with a note.
- **Filed under another word**: χαλκοῦς under χάλκεος (`SPELLING`), as χρυσοῦς under χρύσεος, its "Lat. aeneus,
  aheneus" Latin throughout (`LATIN_ONLY`); νέω's second entry, *to spin* (`ENTRY`), not the first, *to swim*;
  ἐσώτερος, *interior*, for the neuter ἐσώτερον with a genitive.
- **Inside the Latin** (`MARKUP_LOST`): ἔνθεν, "of Place, Lat. inde, thence", and "Lat. unde, whence, from which" —
  `thence, on the one side, on this side, on that, …`. χωνεύω's *to cast into a mould (χόανος)* is restored
  (`GREEK_LOST`): plain text, one translation.
- **Cut translations restored**: συνάπτω *to bind it fast*, *to connect it with*, *refer it to*; διορίζω *to determine
  one to be*.
- **Form** (`FORM_SENSES`): συνάπτω's active leaves out the middle's and the passive's; ἴσος's masculine and
  feminine the neuter's as a noun; δέρρις's and συμβολή's singular the plural's (δέρρις is one sense in the
  singular, plain text, and a unit in the plural); κατακαλύπτω's active the middle's, so plain *you will cover up*.
- **Pieces set aside** (`NOT_SENSES`): συνάπτω's examples; ἴσος's phrases and adverbs; μοχλός's Latin *vectis*;
  ὀπίσθιος's *the hind-*; συμβολή's Aristophanic repeats and Terence's Latin; χάλκεος's examples and Virgil; νέω's
  *spun*.
- **Morphology**: the second pass was right on six: τῷ ὀπισθίῳ with στύλῳ, masculine (26:27); ἐσώτερον the
  comparative ἐσώτερος, as MorphGNT codes Heb 6:19; τὸ καταπέτασμα the subject of διοριεῖ (26:33); ἔξωθεν with a
  genitive the preposition. ὑάκινθος feminine, as the dye is wherever the text shows a gender (Q22); μῆκος and εὖρος at 26:2 nominative, a verbless
  clause; τὸ πλάτος at 26:16 accusative, as at 25:10.
- **validate.py**: units are paired with their Greek words in order, and where a verse has fewer units than
  occurrences of a word the pairing now prefers the occurrences whose entry says more than its headword (one helper,
  `unit_places`, used by the chains, ranges, cases and articles checks, and the one-sense check likewise): δέρρις's
  singular, plain, stands before its plural, a unit, at 26:8 and 26:12. And an article over a phrase or an adverb
  now entitles its own noun as plain text, `of the one` before ἀνὰ μέσον (26:10), which the bare-headword check had
  read as εἷς's headword loose.
- New chains: the furnishings above; συνάπτω `you will tie`, `of the one tying`; ἴσος `of equal to`, `equal to`;
  ἔνθεν `thence`; διορίζω `will draw a boundary through`; βάσις `steppings and steps`, `the steppings and steps`;
  μοχλός `bars`, `the bar`, `the bars`; στῦλος `pillars`, `the pillars`, `of the pillar`, `to the pillar`, `to
  pillar`, `of pillars`, `to pillars`, `to the pillars`; ἀγκύλη `loops`, `of the loops`; κρίκος `rings`, `the rings`,
  `to the rings`; συμβολή `the coming together`, `a coming together`; κεφαλίς `the parts of a shoe`; γωνία `of the
  corners`, `to corners`; ὀπίσθιος `of the hinder`, `to the hinder`; κάτωθεν `from below`; ὑφαντός `woven`;
  διικνέομαι `let go through`; ἀντιπίπτω `falling against`; ἐξώτερος `of the outer`; σκέπη `a covering`;
  καταπέτασμα `a curtain`, `the curtain`, `of the curtain`, `to the curtain`; χαλκοῦς `of copper`; ὑποτίθημι `you
  will place under`; ὑπερέχω `of the thing holding over`; συγκαλύπτω `covering`; πλάγιος `the sides`; συνέχω `being
  held together`; ἐργασία `to work`; μέτρον `that by which anything is measured`; ἀνίστημι `you will make to stand
  up`; τίθημι `you will set`; διορίζω `will draw a boundary through`; ἅγιος `of the devoted to the gods`, `in the
  devoted to the gods`.
- One translation each, plain text: ὑφάντης, ποικιλτής, τρίχινος, ἕκτος, χωνεύω, ἐσώτερος, νέω (to spin),
  ὑποκαλύπτω, κατακαλύπτω (the active), the numerals.

### Words new in EXO 27

- **From LSJ** (not in Middle Liddell): δικτυωτός `to made in net-fashion, to latticed and trellised, to lattice`, the
  last from θυρὶς δ., "lattice-window"; καλυπτήρ `the covering and sheath, the cover, the lid`, the singular without
  the plural's *tiles*; περιαργυρόω `having been cased and plated with silver and standing so`; περιχαλκόω *you will
  cover with brass or copper*, one translation, plain text, the "or" kept as in κανοῦν; σανιδωτός `planked and
  boarded over`; ἄτρυγος `without lees and clarified and pure`; ῥαφιδευτής `of the stitcher and embroiderer`.
- **Legacy chains brought to their cards**: καθαρός had dropped *clear of guilt or defilement, clean, pure*,
  *purified*, *clear of or from*, *without blemish*, *clear, exact*, and the tails of *clear of admixture, clear,
  pure* and *pure, genuine*: now `clear of dirt and clean and spotless and unsoiled, clear and open and free, clear
  from shame and pollution and pure, clear of guilt and defilement and clean and pure, purified, clear of and from,
  clear of admixture and clear and pure, pure and genuine, without blemish, clear and exact` (GEN 7, 8, 20, 24, 44,
  EXO 25, 27). χαλκός carried *brass*, which Middle Liddell rules out ("bronze …, not brass"), and dropped four
  senses: now `copper, metal, bronze, anything made of brass and metal, a copper and caldron and urn, a brasen
  mirror, a copper coin` (GEN 4:22, EXO 25:3, 27:2, 27:6). κέρας had dropped *any projection, e.g. a mountain-peak*
  and joined *a horn for blowing* to *a flute*, two senses: now `… the horns for blowing, the flutes, … the any
  projections, the mountain-peaks` (GEN 22:13, EXO 27:2).
- **Pieces set aside** (`NOT_SENSES`): φορεύς's *pack-*; κοῖλος's paraphrase of an empty bed, its examples' repeats
  and Virgil; ἱστίον's *sail* and *the sails*, examples' repeats; κατασκευή's *in preparing for*; ἐσχάρα's *the
  watch-fires*, πυρὸς ἐσχάραι; ἄργυρος's *white*, the gloss of ἀργός; καθαρός's examples, Horace and the adverb's;
  συντάσσω's examples; χαλκός's definitions of *bronze* and *brass*; κόπτω's *to lay … waste*, cut, whole in
  `MARKUP_LOST`.
- **Form** (`FORM_SENSES`): παραδείκνυμι's active and passive leave out the middle's *to exhibit, bring forward*;
  ποικιλία's and λύχνος's singular the plural's; καίω's and συντάσσω's active the middle's and the passive's;
  κόπτω's middle-passive and passive the middle's.
- **An adjective's chain is the adjective's**: κοῖλον at 27:8 is predicate, *you will make it hollow*, and its chain
  leaves to the noun *the hold*, *the vale*, *the valley*, *a hollow, cavity, ravine*, *the cavities*: `hollow and
  hollowed, lying in a hollow, forming a hollow, lying between high cliffs, embayed, nearly empty`.
- **The article's noun follows its gender over a phrase**: τὸ πρὸς λίβα, τὸ κατὰ θάλασσαν, τοῦ ἐπὶ τῆς διαθήκης,
  neuter, *the thing*, *of the thing*; and EXO 26:18, 20, 22, 27, 35, which had read the neuter *the one*, are
  brought to it. δεύτερος's neuter with the article reads `the second, the thing coming in second, …, the thing
  after, …`, and validate.py's chains check now takes *thing* after *the*, with words after it, for the article's
  noun, as it already took *one*.
- **Morphology**: the second pass was right on two: αὐτῶν after ἱστία is neuter, the hangings (seven times); ἐλαίων
  is ἔλαιον's genitive plural by its accent (ἐλαία's is ἐλαιῶν), *olive-oil out of of olive-oils*. The measures at
  27:1 stay accusative, as at 25:10; ὑάκινθος feminine (Q22); φῶς under φάος, as at 10:23; διὰ παντός neuter,
  as at 25:30.
- New chains: θυσιαστήριον *altar*, plain; στεφάνη's anarthrous `anything that encircles, brim, a diadem and coronal,
  edge, brow of a hill and edge of a cliff`; φιάλη `the broad and flat vessels and bowls, the cinerary urns, the
  broad and flat bowls`; ἐσχάρα `hearth and fire-place, a pan of coals and brasier, an altar for burnt-offerings`, and
  with the article and its cases; ἔργον `to work, to business, to deeds, to action, to works of industry and tilled
  lands`; γωνία `of corners`; φορεύς `bearers and carriers`; πλευρόν `the ribs, the ribs and the sides, the sides,
  the flanks`; αἴρω with ἐν, `in the taking up`; παραδείκνυμι `the thing having been exhibited side by side, the thing
  having been represented, the thing having been exhibited and handed over`; αὐλή `court-yard, wall of the court-yard,
  court, quadrangle, any court, hall`, `of the court-yard, …, of the any court, of the hall`; ἱστίον `any webs and
  sails`, `of the any webs and sails`; ψαλίς `the pairs of scissors, the buildings with a pointed stone roof and
  vaults`; ἀπηλιώτης `wind that comes from the rising sun and east wind`; ἄργυρος `to white metal, to silver, to
  silver-money and money`; στῦλος `of the pillars`; κάλυμμα `a head-covering, a hood, veil, a covering, a grave`;
  ποικιλία `to the marking with various colours and embroidering and embroidery, to the varied aspect and diversity,
  to the versatility and subtlety and craft`; καταργυρόω `having been covered with silver and standing so, having been
  silvered, having been bought, having been bribed with silver`; κατασκευή `the preparation, the equipment, the any
  kind of furniture that is fixed, the building and fixture, the any furniture, the state and condition and
  constitution, the device and trick`; ἐργαλεῖον `the tools and instruments`; πάσσαλος `the pegs, the gags`;
  συντάσσω's imperative `put in order together, …`; κόπτω `having been struck and smitten and knocked down and
  standing so, …` (Q21); καίω `to light and kindle, …`, `will light`, `may be lighted and kindled, may be lighted and
  burn, …`; λύχνος `a portable light and lamp`; ὕψος `height, top and summit and crown`.
- One translation each, plain text: θυσιαστήριον, κρεάγρα, πυρεῖον (*the piece of wood*, its plural's gloss in the
  singular), κλίτος (*clime*, as at 26:18), λίψ (*SW. wind*), ἔλαιον, κόκκινος, περιχαλκόω, the numerals.

### Words new in EXO 28

- **A lettered verse**: Rahlfs prints 28:29a after 28:29, for what the Hebrew's 23–28 give at length; the module keeps
  it inside 29, after `<br/><i>[a]</i>`. It is a verse of its own here, `EXO 28:29a`: words.py's `verse_key` reads
  `29a` beside the integers, `verse_order` sorts 29, 29a, 30, and validate.py's `lettered` splits the module's verse
  at the marker.
- **From LSJ** (not in Middle Liddell): γλύμμα `engraved figure and signet, inscription`; διανήθω *spin out*, plain;
  κίδαρις `Persian head-dress, turban of Jewish high priest, an Arcadian dance`; καθυφαίνω `you will interweave and
  weave in`, the passive's *to be inwoven* left out; κατάλιθος *set with precious stones* and τετράστιχος *in four
  rows or courses*, plain; κοσυμβωτός `tasselled and fringed`; κροσσωτός `tasselled and fringed, stepped`; κροσσοί
  `tassels and fringes, lappets`; κόσυμβος `the fringes, the hair-nets`; λιγύριον *a precious stone*, LSJ's
  description, which marks no translation (Q25); λιθουργικός *of or for a lithourgos (λιθουργός)*, plain, its
  genitive `of of or for a lithourgos` in validate.py's GLOSS_LEADS; παρωμίς *shoulderstrap*, περιστήθιον
  *breastband*, χρυσόλιθος *topaz*, ἀχάτης *agate*, ἁλυσιδωτός *wrought in chain fashion*, περικύκλῳ *round about*,
  plain; περιστόμιον `the mouth of a vessel, the mouth-band, the region of the epiglottis, the collar, the edge`;
  ἀσπιδίσκη `bosses and disks, small shields, constellations`; ἐκτύπωμα `figure in relief, reflection`; ὀνύχιον
  `small claw, trotters, cloves, onyx`; ᾤα `sheepskin, garment of this material, drawers, apron, border, fringe of a
  garment`; ῥοΐσκος `small pomegranates, knobs or tassels shaped like a pomegranate`; βηρύλλιον, "Dim." inside
  βήρυλλος, `gem of sea-green colour and beryl` (Q20).
- **Filed under another word** (`SPELLING`): λινοῦς under λίνεος, `of flax and flaxen and linen`; ἄνθινος under
  ἀνθινός, `like flowers and blooming and fresh, bright-coloured`; τοπάζιον under τόπαζος, which LSJ files it under,
  *topaz*, plain.
- **Inside the Latin** (`MARKUP_LOST`): σμάραγδος, "Lat. smaragdus, a precious stone of a green colour", the English
  in the Latin element as εἰ's *if* is: `a precious stone of a green colour, emerald, malachite`.
- **Cut translations restored**: ἐξαρτάω *having a thing hung on one, be furnished with*; συνέχω *to keep together,
  keep from falling to pieces* and *to keep together, make pull in time*.
- **Form** (`FORM_SENSES`): αἴσθησις's and τέχνη's singular leave out the plural's; ἐπάγω's middle the active's;
  χρίω's active the middle's and the passive's.
- **Pieces set aside** (`NOT_SENSES`): αἴσθησις's phrases; ζώνη's στρόφιον, examples' repeats and girdle-money;
  ποίησις's *(action)*, πρᾶξις's; τέχνη's phrases; λογεῖον's *part* and *speakers*, the description's, so that it
  is one translation, *a speaking-place*, plain; ῥυθμός's Virgil; σπιθαμή's *inches*; χρώς's phrases with ἐν; μίτρα's
  *beneath* and *over*; μέτωπον's *line*; πλέκω's, περικαλύπτω's, συμπλέκω's, εἴσειμι's, συνυφαίνω's,
  λειτουργέω's, χρίω's and ἐπάγω's examples and their pieces.
- **Legacy chains brought to their cards**: γένεσις's plural had split the run *origin, source, productive cause*
  and dropped *kind and family* and *generation and age*, which the singular keeps (GEN 6, 10, 11, 25, 36, 37,
  EXO 6); στολή's plural had dropped *equipment* and *pieces of dress and garments* (GEN 35:2, 45:22);
  σοφός had cut the run *cleverly devised, wise* (GEN 41:8).
- **Morphology**: the second pass was right on four: αὐτοῦ at 28:8 neuter, the woven work; μέσον at 28:32 nominative,
  the predicate of ἔσται; κύκλῳ with a genitive the preposition; ἄνθινον neuter, a noun. ὑάκινθος is feminine at 28:5
  and 28:37, by its article and its participle, and so feminine throughout Exodus, as the dye (Q22). περισκελής reads
  LSJ's second entry, from σκέλος, by `LSJ_HOMOGRAPHS`: Middle Liddell's one entry is the word from σκέλλω.
  Used as a noun, `drawers, round the leg`; `the drawers, the round the leg` at 36:35 (Q23).
- New chains: προσάγω's middle imperative `bring, draw to yourself and attach to yourself and bring over to your
  side, …`; στολή `an equipment` and its plural; ἅγιος `devoted to the gods and sacred and holy, holy and pure`, with
  the article; δόξα's anarthrous `notion, …`; σοφός's dative plural; ἐμπίπλημι `I filled quite full`; αἴσθησις `of
  perception by the senses, …`; χιτών; ζώνη `a belt and girdle, …`, `belts and girdles, …`; συνέχω's active
  participle; ἐξαρτάω's perfect passive participle; ὕφασμα `woven robe and web`; ποίησις `the making and fabrication
  and creation and production, …`; γλύφω `you will carve and cut out with a knife, …`; τέχνη `of art and skill and
  craft in work and cunning of hand, …`; σφραγίς `of a seal and signet and seal-ring, …`; ἀναλαμβάνω's future; ἄνθος
  with ἐν; πλοκή; πλέκω's perfect participle with the article; ἐμπρόσθιος `of the fore and front`; κρίσις's plural;
  ῥυθμός `the measured motion and time and rhythm, …`; σπιθαμή; στίχος `the row and file, the line, the verse`;
  σάρδιον, ἄνθραξ, σάπφειρος, ἀμέθυστος (the noun's range); περικαλύπτω, συνδέω, συμπλέκω, συνυφαίνω perfect
  participles; εἴσειμι and ἔξειμι datives; δήλωσις; φέρω's future; ἔχω; ῥήγνυμι's aorist passive subjunctive; ἐξανθέω;
  ῥόα; κώδων; λειτουργέω with ἐν and alone; πέταλον; ἐκτυπόω; ἁγίασμα `holy place and sanctuary, holiness`; μίτρα;
  μέτωπον; ἁμάρτημα's plural; ἁγιάζω's subjunctive; δόμα; κόσυμβος; κίδαρις's plural; ἐνδύω; χρίω; περισκελής;
  καλύπτω's infinitive; ἀσχημοσύνη's anarthrous; χρώς; ὀσφύς's anarthrous; προσπορεύομαι's subjunctive; ἐπάγω's
  middle `will procure, …, will bring upon themselves, …`.
- One translation each, plain text: ἱερατεύω, διαγλύφω, ἔναντι, ὑποδύτης, ὑακίνθινος, λῶμα, δεκτός, ἴασπις, λογεῖον,
  ὦμος (*the shoulder with the upper arm*, as at its earlier occurrences), κόκκινος, ποικιλτής, ὑφάντης, and those from
  LSJ above.

### Words new in EXO 29

- **From LSJ** (not in Middle Liddell): κάρπωμα `fruit, profit, offering of fruits`; λάγανον *a thin broad cake*,
  plain; στηθύνιον, "Dim. of στῆθος", no translation of its own, read as Middle Liddell's στῆθος, `the breast, the
  breast as the seat of feeling and heart` (Q20); χρῖσις `of the smearing, of the anointing, of the colouring and
  varnish and wash, of the colour-washing`; ἀφαίρεμα `that which is taken away as the choice part, tribute,
  deduction, coarse grits made from zea (ζέα)`; ἀφόρισμα `that which is set apart and the wave-offering`, one
  translation run; ἐνδελεχισμός `of persistence, of perpetual`, the second LSJ's English for this genitive;
  ὁλοκαύτωσις *the sacrifice of a burnt-offering*, plain.
- **Filed under another word** (`SPELLING`): ἐνδελεχῶς inside ἐνδελεχής, `continuously and perpetually`, as δικαίως is
  read inside δίκαιος; καθαρισμός, "later form for καθαρμός", `of the cleansing and purification, of the means of
  purification and purifying sacrifice and atonement and expiation, of the rites of initiation`.
- **A name in lower case**: ιν, the hin, `of the [[name:ιν]]`, *in* / *hin*, as χερουβιμ is a name.
- **Cut translations restored** (`MARKUP_LOST`): τελειόω *to make it perfect, complete, accomplish*, *to bring one to
  perfection*; προτίθημι *let it lie in state*, *to set out for show or sale*, *was allowed*.
- **Form** (`FORM_SENSES`): τελειόω's and ζώννυμι's active leave out the middle's and the passive's; προτίθημι's
  middle-passive and passive the middle's; τάσσω's middle the active's and the passive's — so τάξομαι reads `I will
  fall in and form in order, I will take a payment on myself, I will agree to pay, I will agree upon and settle, I
  will impose`, and EXO 8:5 Τάξαι and 8:8 ἐτάξατο, middles that had been given the active's range, are brought to
  it: `fall in, …`, `fell in, …`.
- **Pieces set aside** (`NOT_SENSES`): τελειόω's and προτίθημι's examples; ζώννυμι's middle examples; μέλος's
  phrases *limb by limb*, *in tune*, *out of tune*; ἀμνός's *lambs*, an example's, so that ἀμνός is one translation,
  *lamb*, plain; καθαρμός's examples.
- **Legacy chains brought to their cards**: ἀφορίζω's passive had dropped *banish*, *cast out, excommunicate*, *set
  apart*, *appoint, ordain* and carried the middle's *marked off for itself* (GEN 2:10, 10:5). GEN 3:8's τὸ δειλινόν,
  plain *at evening*, had dropped its article: *the at evening*, as 29:39 and 29:41.
- **validate.py**: a plain word's own English counts in the number its form wears: λάγανα, plain *thin broad cakes*,
  holds its own *cakes*, not ἄρτος's headword loose beside it.
- **Morphology**: the second pass was right on two: ἔξω with a genitive the preposition; τὸ θυσιαστήριον at 29:37
  nominative, the subject of ἔσται.
- New chains: ἄμωμος `without blame and blameless`; φυράω's perfect passive participle `having been mixed and standing
  so, having been kneaded, having been made up`; χρίω's `having been touched on the surface …`; κανοῦν's singular;
  προσφέρω `you will bring to, …`; θύρα's plural; λούω `you will wash, you will bathe`; μίτρα and πέταλον with the
  article; ἁγίασμα `the holy place`; χρῖσμα `of the anything smeared on, …`; ἐπιχέω `you will pour water over, you
  will pour`; ζώννυμι `you will gird, you will gird round the loins`; ζώνη's dative plural; περιτίθημι; κίδαρις with
  the article; ἱερατεία `priest's office and priesthood`; τελειόω `you will make perfect and complete, …`; ἐπιτίθημι's
  third persons; σφάζω `you will slay, …`; δάκτυλος; βάσις's singular; στέαρ's singular; λοβός `the lobe of the ear,
  the lobe of the liver, the liver`; κοιλία with the article; δέρμα's singular; κόπρος; κατακαίω's future; διχοτομέω;
  μέλος `limbs, …`; πλύνω's future; ἐνδόσθια `the inwards and entrails`; ὁλοκαύτωμα's singular; θυσίασμα `victim and
  offering`; οὖς; δεξιός with the article and the genitive; ἄκρον's plural with the article; ῥαίνω; τελείωσις
  `accomplishment and fulfilment`; προτίθημι's perfect passive participle; ἀφορίζω's and ἀφαιρέω's perfects; θῦμα and
  σωτήριος with the article; χρίω's aorist passive infinitive; ἐνδύω's future middle; ἱερεύς with the article; κρέας;
  ἄρτος's plural with the article; καταλείπω's aorist passive subjunctive; θυσία with the article; πρωινός; σπονδή with
  the article; δέκατος; ἐπικαλέω's first person and infinitive; δόξα with ἐν.
- One translation each, plain text: μοσχάριον, λάγανον, σεμίδαλις, πυρός, ἧπαρ, νεφρός, βραχίων, εὐωδία, ἔλαιον, οἶνος,
  δειλινός, ἀμνός, κατακαλύπτω's active, ὁλοκαύτωσις, ἱερατεύω, λογεῖον.

### Words new in EXO 30

- **From LSJ** (not in Middle Liddell): λουτήρ *a washing or bathing-tub*, one translation, plain; μυρεψικός `of or for
  unguents and aromatic`; σίκλος, "= σίγλος", *shekel*, plain; χαλβάνη *the resinous juice of all-heal*, plain, its
  plant's Latin name left out; ἐξιλασμός, "= ἐξίλασις", `of the propitiation and atonement`.
- **In neither lexicon**: κάτεργον, plain *a thing effected by labour*, from κατεργάζομαι; ἡδυσμός, plain *of
  seasoning*, from ἡδύνω — as σφυροκόπος (GEN 4:22) and ὑποκαλύπτω (EXO 26:12).
- **Filed under another word**: ἶρις, the appellative inside Middle Liddell's Ἶρις, `of rainbow and iris, of
  bright-coloured circle, of plant Iris`, the goddess's name set aside and the plant's restored (`MARKUP_LOST`).
- **Pieces set aside** (`NOT_SENSES`): ὄνυξ's phrases and Horace's Latin, `talon, a nail, a hoof, a veined gem and
  onyx`.
- **Legacy chains brought to their cards**: ὅθεν's first sense, *whence, from which*, which MARKUP_LOST recovers from
  inside its Latin, had never reached its units: `whence, whence and from which, from whom, …` (GEN 10:14, 13:3,
  24:5, EXO 5:11).
- **validate.py**: GLOSS_LEADS takes `of of twenty years`, εἰκοσαετής's genitive.
- **Morphology**: the second pass was right on three: ἐπάνω after ἀπὸ εἰκοσαετοῦς an adverb; αὐτοῦ at 30:33 neuter,
  the oil; θυμίαμα at 30:8 accusative in apposition, as κάρπωμα at 29:38. εὐώδης keeps the two-termination C.
- New chains: θυμίαμα with the article and the genitive; τοῖχος `the walls of a house and court, the sides of a ship`;
  στρεπτός with the article; πλευρόν's dative plural; σκυτάλη `staffs and cudgels and clubs, staffs, batons, Spartan
  dispatches, messages`; μαρτύριον's plural; θυμιάω `will burn so as to produce smoke and burn`; σύνθετος; ἐπισκευάζω
  `may get ready and equip and fit out, may make afresh and repair`, the middle's left out; ἐξάπτω `may fasten from and
  to, may let fall from, may place upon` — the lighting of the lamps is not among Middle Liddell's senses; ἁμαρτία's
  plural; συλλογισμός; πτῶσις; παραπορεύομαι; ἐπίσκεψις; δίδραχμον's singular; εἰσφορά; πλουτέω's and πένομαι's
  participles; ἐλαττονέω's future; προστίθημι's third person; δίδωμι's present with ἐν, `in the giving, … the being
  ready to give and offer, …`; νίπτω's future middle; ἀναφέρω's infinitive; ἥδυσμα's plural; ἄνθος with the article;
  ἐκλεκτός's and εὐώδης's genitives; κάλαμος `of a reed, …`; χρῖσμα; μύρον; μυρεψός `of one who prepares unguents and a
  perfumer`; τέχνη's dative; ἄλειμμα; σύνθεσις; ἀλλογενής's dative; ὄνυξ; διαφανής; ἴσος's neuter and its dative;
  μίγνυμι's perfect passive participle; συγκόπτω's second person; ἀπόλλυμι's future middle; ὀσφραίνομαι's infinitive.
- One translation each, plain text: ἐξιλάσκομαι *will propitiate*, *to propitiate*; ὀβολός; σμύρνα; κιννάμωμον;
  λίβανος; ἐξολεθρεύω; λυχνία; εἰκοσαετής; πεντακόσιοι, διακόσιοι; κάτεργον; ἡδυσμός.

### Words new in EXO 31

- **From LSJ** (not in Middle Liddell): νηστός *spun*, one translation, plain; διασκευή `the construction, the
  equipment, the furniture or vessels, the rhetorical elaboration, the set phrases, the new edition or recension, the
  theatrical performance`, its = ἀνασκευή a pointer and left out.
- **Middle senses** (`FORM_SENSES`): ἀνακαλέω's perfect middle, `I have called up the dead and it stands so, I have
  called again and again, I have invoked and appealed to, I have called to myself and sent for and summoned, I have
  cheered on, I have called back and recalled`, the active's *to summon, cite*, *to call* by a name and *to call on*
  left out.
- **Passive senses** (`FORM_SENSES`): γράφω's perfect passive participle, `having been scratched and scraped and
  grazed and standing so, …, having had a person's name written, …, having been indicted`, the middle's left out, and
  *to move that*, whose clause the passive cannot hold (Q21).
- **By gender** (`FORM_SENSES`): τεκτονικός's neuter, `the practised or skilled in building`, the masculine's and the
  feminine's as nouns left out.
- **A first translation that is a preposition**: θεῖος, «of» or «from the gods, sent by the gods, issuing from them,
  divine»: the headword `of or from the gods`, as μυρεψικός's at EXO 30:25 (Q26); the chain `of or from the gods and
  sent by the gods and issuing from them and divine, appointed of God, belonging or sacred to a god and in honour of a
  god and holy, under divine protection, more than human and wondrous, divinely strong and great and beautiful,
  excellent, marvellous`, the neuter's and the plural's as nouns and the adverb's left out. Its examples' pieces go in
  `NOT_SENSES`.
- New chains: σοφία `of skill, of knowledge of and acquaintance with, of sound judgment and intelligence and practical
  wisdom, of cunning and shrewdness and craft, of wisdom and philosophy`; σύνεσις `a coming together and union, quick
  comprehension and mother-wit and intelligence and sagacity, intelligence in, sagacity in respect to, conscience, a
  branch of art or science`, its = συνείδησις a pointer after *conscience*; ἐπιστήμη `of acquaintance with, of skill
  and experience, of knowledge, of scientific knowledge and science`; ἀρχιτεκτονέω `to be the architect, to construct
  and contrive`; διανοέομαι's infinitive; χαλκός with the article; κλώθω's participle with the article, `the one
  having been twisted by spinning and spun and standing so`; ὄνομα's and φυλή's anarthrous genitives; συνετός's
  dative; συντάσσω's first person; θυμίαμα and καθαρός with the article; σύνθεσις's genitive; ἁγιάζω's participle,
  `the one hallowing and making sacred`; θανατόω's future passive; ἔργον's anarthrous plural; πλάξ `flat surfaces and
  flat lands and plains, plains, the flat tops of a hill and table-lands, flat stones and tablets`.
- One translation each, plain text: νηστός; θυσιαστήριον; λειτουργικός *ministering*; ἱερατεύω *to be a priest*;
  βεβηλόω *the one profaning*; λίθινος *of stone*; λιθουργικός with the article, `the of or for a lithourgos
  (λιθουργός)`.
- **Legacy chain brought to its rule**: συνετός's run *intelligent, sagacious, wise* is one translation, and is now
  one item: `intelligent and sagacious and wise, intelligent in, intelligible`, and the comparative `more intelligent
  and sagacious and wise, …` (GEN 41:33, 41:39). The runs check had let it pass, since *intelligent in* says
  *intelligent* once its *in* is set aside.
- **Morphology**: the second pass was right twice: Ωρ after τὸν genitive, the one of Hur, as Μαμβρη at GEN 13:18; ἓξ
  at 31:17 dative, ἐν ἓξ ἡμέραις. Σινα after τῷ ὄρει keeps the case of its article, as the corpus codes it.

### Words new in EXO 32

- **No 32:9**: Rahlfs prints none, and the verse numbers run from 8 to 10; the module agrees. The note on 32:10 says
  the Hebrew's verse is not in this text.
- **From LSJ** (not in Middle Liddell): χωνευτός `formed of cast metal and molten`; πολυπληθύνω *multiply*, plain.
- **Restored whole** (`MARKUP_LOST`): ἱλάσκομαι *to make him propitious to one, conciliate him*, its aorist passive
  `was appeased, was made propitious to one and conciliated, was expiated, was gracious`; τροπή *a change by figures or
  tropes* and *the turning of the enemy, putting him to flight, a rout*; ἀνακάμπτω *to bend one's steps back*, `bend
  back, bend your steps back, return`; εἶμι's *I shall go, shall come* and *to come or go*, which Perseus runs together.
- **By form** (`FORM_SENSES`): συνίστημι's second aorist συνέστη intransitive, `stood together, formed in order of
  battle, met in fight and was engaged with, …, was contracted`; παραβαίνω's and διασκεδάννυμι's active without the
  passive's; τροπή's singular without the plural's tropics and solstices; εἶμι's imperative `let him go, let him come
  or go, let him go across, let him go through, let him fly, let him live, let it pass and well then`, ἴτω's own idiom
  kept and the indicative's future use left out, its other forms the reverse; οἰκέτης's singular without the plural's
  household.
- **ἀνίστημι**: ἀνέστησαν, both aorists' third plural, is left to the intransitive, as ἵστημι's ἔστησαν is: `stood up,
  rose, rose to fight against, rose to go and set out` (32:6).
- New chains: γραφίς `the stile for writing, the needle for embroidering, the embroidery`; τάχος `the swiftness and
  speed and fleetness and velocity, the quickness, the hastiness`; παραβαίνω `went by the side of, passed beside or
  beyond and overstepped and transgressed, passed over and omitted, escaped, came forward, stepped forward`;
  ἐξαναλίσκω `to spend entirely, to exhaust, to destroy utterly`; γραφή `representation by means of lines, drawing or
  delineation, painting, a drawing and painting and picture, writing and the art of writing, a writing, a letter, a
  statement, an indictment, a criminal prosecution`, with the article and without; κολάπτω `having been pecked at and
  standing so, having been struck, having been carved or chiselled`; τροπή `of a turn and turning, of a turn and
  change, of a change by figures or tropes, of the turning of the enemy and putting him to flight and a rout`; ὅρμημα
  `the stir and impulse, the longing, the struggle` (Q27); ἐπίχαρμα `an object of malignant joy, malignant joy`;
  συνέρχομαι `went together or in company, came together and assembled, had dealings or intercourse with, …`; νυνί
  `now and at this moment`; χρυσίον's plural `pieces of gold, gold, gold coin and money`; ἐγγύς's superlative ἔγγιστα,
  `most hard by and near to, …`, as φρόνιμος's at GEN 3:1; and the forms of χρονίζω, περιαιρέω's middle, δέχομαι,
  προσκυνέω's and θύω's perfects, δέομαι's aorist, θυμόω's present, παύω's imperative, μιμνήσκομαι's participle,
  ὄμνυμι, κατέχω's future, καταγράφω's perfect passive, κράζω's and ἐξάρχω's participles, ἐγγίζω's imperfect, ὀργίζω's
  participle, κατακαίω's aorist, διασκεδάννυμι's perfect passive, τίθημι's middle imperative, διέρχομαι's imperative,
  πληρόω's second person, δίδωμι's aorist passive infinitive, ἁμαρτάνω's perfects, ἀφίημι's present, ἐξαλείφω's
  imperative, γράφω's second person, ἐπισκέπτομαι's subjunctive, προπορεύομαι's future and present.
- One translation each, plain text: ἐνώτιον *ear-ring*; θυγάτηρ; ἐπαύριον; ἀνομέω *acted lawlessly*; ἔναντι;
  βραχίων *the arm*; ἄστρον *the stars*; οἶνος; καταλέω *ground down*; τρισχίλιοι; σήμερον; ἐξιλάσκομαι; ἐνώπιον *face
  to face*.
- **Legacy chains brought to their cards**: διασκεδάννυμι's run *to scatter abroad, scatter to the winds, disperse*
  is one item, `scattered abroad and scattered to the winds and dispersed, disbanded` (GEN 17:14); οἰκέτης's plural
  had read `house-slaves, household servants, menials`, a word the lexicon does not give and its run split, and now
  reads `house-slaves and menials, one's household and the women and children` (GEN 27:37, GEN 44, GEN 50:18, EXO 5).
- **Morphology**: two disagreements over 809 words, both θυμόω's lemma, which keeps Middle Liddell's spelling. ἐπὶ
  Ααρων at 32:1 is accusative, against the module's dative.

### Words new in EXO 33

- **From LSJ** (not in Middle Liddell): περιστολή `the wrapping up, the laying out, the peristaltic action, the
  adornment, the restraint and decorum`, LSJ's *adornments* at this verse read in the singular (Q27), its *secretly* a
  phrase's; γνωστῶς *clearly*, the adverb inside LSJ's γνωστός, which Middle Liddell does not give.
- **Filed under another form** (`SPELLING`): σκοπεύω, "later form for σκοπέω", `looking at or after, beholding and
  contemplating, looking out and watching, looking to and considering and examining, looking out for`; οἰκτίρω, "late
  form of οἰκτείρω", `I will pity and feel pity for and have pity upon, I will pity one for or because of a thing, I
  will be sorry`, the second sense restored whole (`MARKUP_LOST`).
- **The second entry** (`ENTRY`): ἄπειμι, of εἶμι, `of going away and departing, of returning, of receding, of
  going`; the imperative's *be gone* left out of the other forms. The mapping is the lemma's, so ἄπειμι *to be away*,
  of εἰμί, will need a lemma of its own when the text has it.
- **A word used as a noun**: φίλος, `the friend, the loved and beloved and dear, the dear, the dear and pleasant and
  welcome, the one's own, the loving and friendly, the friendly`, its first noun sense heading, as ἐχθρός's at EXO
  23:4; the masculine leaves out the feminine's, the neuter's and the superlative's nouns, and the predicative and
  adverbial examples go in `NOT_SENSES`. Its *Lat. amicus, carus* is Latin throughout (`LATIN_ONLY`).
- **ἵστημι's middle and passive** are intransitive, as the entry says, "Pass. and intr. tenses of Act.": `FORM_SENSES`
  leaves the causal senses out of them, so ἵστατο reads `was being set, was being placed and standing, …` and στήσῃ the
  chain of `you will be set`.
- **A first translation split by «or»** (Q26): πενθικός, «of» or «for mourning, mournful», `of or for mourning and
  mournful`, with ἐν merged into it; validate.py's GLOSS_LEADS takes `of of or for mourning`, ἐν's own *by means of*
  running into the gloss's *of*. ἐμφανίζω `make manifest and exhibit, represent, make clear or plain`, the passive's
  *to become visible* left out.
- New chains: καταπενθέω `mourned for and bewailed`; ὀπή `an opening and hole, a hole in the roof`; δόξα's genitive
  plural; σκηνή's anarthrous nominative `a covered place and tent, a camp, a dwelling-place, a temple`; ζητέω's
  participle with the article; εἰσπορεύομαι's and κατανοέω's imperfects; ἀπολύω's imperfect; θεράπων with the
  article; δηλόω's second person; εὑρίσκω's perfects; προπορεύομαι's and καταπαύω's first person; πορεύομαι's second
  person; συμπορεύομαι's participle; λέγω's perfect second person; δείκνυμι's future and imperative; παρέρχομαι's;
  καλέω's and ἐλεέω's first person; ἀφαιρέω's; ἐξαναλίσκω's subjunctive and future.
- One translation each, plain text: συναποστέλλω *will despatch together with*; γάλα; μέλι; συναναβαίνω *may go up
  with*; σκληροτράχηλος *stiff-necked*; ἐνδοξάζω *will be glorified*; ἐνώπιος *face to face*, its dative `to face to
  face`; γνωστῶς.
- **Morphology**: the second pass was right on all eight: ἔξω and ὀπίσω before a genitive are prepositions, as the
  corpus codes ἔξω τῆς παρεμβολῆς at EXO 29:14; ὅσα and τὸ πρόσωπον nominative subjects; καί at 33:17 the adverb,
  also. ἕως τοῦ εἰσελθεῖν takes the preposition.
- **words.py**: three SPELLING comments an earlier edit had moved onto χαλκοῦς's line are back beside σφηκία,
  ἀναγινώσκω and παλαιστής.

### Words new in EXO 34

- **The page's own misprint**: 34:28 prints ἄρτον οὖκ ἔφαγεν, with the circumflex; the transcription keeps it, the
  module prints it too, and the note says so.
- **From LSJ** (not in Middle Liddell): οἰκτίρμων *merciful* and πολυέλεος *very merciful*, plain, citing 34:6.
- **νέμω's middle and passive** (`FORM_SENSES`): the first sense in the passive, then the senses Middle Liddell marks
  "Mid." and "Pass.", the active's own left out, as GEN 41:3's ἐνέμοντο read them: `let them be dealt out and
  distributed and dispensed, let them distribute among themselves, …, let them spread`. GEN 41:3 and 41:18 had
  dropped *dwelling*, the absolute *to dwell*, and now carry it.
- **Restored whole** (`MARKUP_LOST`): χρῶμα's *the surface, skin: the colour of the skin*, `of the surface and skin
  and the colour of the skin, of the complexion, of the colour`; the plural's embellishments left out of the singular.
- **Set aside** (`NOT_SENSES`): ἀληθινός's example's *true*, `agreeable to truth, truthful and trusty, true and real`;
  ἀλλόφυλος's example's *with foreigners*, `of another tribe and foreign`.
- **validate.py**: GLOSS_LEADS takes `of of seven years`, ἑβδομάς's genitive, `of the numbers seven or numbers of
  seven, of periods of seven days and weeks, of of seven years and septenaries`.
- **πλησίον before a genitive** is a preposition, as ἔξω and ὀπίσω are (EXO 33): `near and close to, near and
  neighbouring, near and nigh and hard by`, its noun senses left to ὁ πλησίον.
- **θεῷ ἑτέρῳ** at 34:14 reads with the anarthrous formula (Q28).
- New chains: μακρόθυμος `longsuffering and patient`; διατηρέω's participle; ἀφαιρέω's participle; ἀδικία's plural;
  ἔνοχος with the article; ἐπάγω's participle; συμπορεύομαι's imperative; ἔνδοξος's positive; ἐκβάλλω's first person;
  τίθημι's subjunctive and perfect middle, `I have set for myself and it stands so, …`; ἐγκάθημαι's dative; βωμός
  `the any raised platforms and stands, the bases and pedestals, the raised places for sacrificing and altars, the
  tombs and cairns`; ἄλσος `the glades or groves, the groves`; ἐκκόπτω's future; θεός's articular plural genitive and
  dative; προσκυνέω's subjunctive; θύω's and καλέω's third plural subjunctive; φυλάσσω's future middle singular;
  ἐντέλλομαι's perfect; πρόβατον's dative; λυτρόω's subjunctive; καταπαύω's second person; σπόρος `to the sowing, to
  the seed-time, to the seed, to the produce and fruit and harvest and crop`; ἄμητος with the article; πλατύνω's,
  ἀναβαίνω's subjunctive; ἐπιθυμέω's future; ὁράω's aorist passive infinitive; γράφω's imperative and future;
  λόγος's anarthrous plural; καταβαίνω's imperfect and participle; ἐγγίζω's infinitive; κάλυμμα with the article;
  περιαιρέω's imperfect middle; ἐκπορεύομαι's articular infinitive; λαλέω's with ἐν; συλλαλέω `to talk or converse
  with`; σπεύδω's participle in the masculine; ὄρος's dative.
- One translation each, plain text: λαξεύω *hew in stone*; καθότι *in what manner*; ἀνομία *lawlessness*; γλυπτός
  *carved*; ἐκπορνεύω *commit fornication*; μήτρα *womb*; ἀρσενικός *male*; πρωτότοκος *first-born*; πυρός *wheat*;
  πρωτογένημα *firstfruits*; οἰκτίρμων; πολυέλεος.
- **Morphology**: the second pass was right on eleven of fourteen: καί at 34:1 and 34:4 the adverb, also; ἅ at 34:1
  and 34:10, τὰ πρόβατα, θύματα nominative subjects; πλησίον before a genitive a preposition; ἑπτά with ἡμέρας
  feminine; λυτρώσῃ after ἐάν the subjunctive; ἕως ἄν the conjunction. Σινα keeps the case of its article.

### Words new in EXO 35

- **Verses Rahlfs does not print**: 35:8, 35:15, 35:17 and 35:18; the module agrees, and a note on the verse after
  each gap says so. **35:12a**, after 12, is lettered, as 28:29a.
- **From LSJ** (not in Middle Liddell): διατόνιον *curtain-hook or -ring*, inside LSJ's διατόναιον, plain;
  ἐμπλόκιον `fashions of plaiting women's hair, hair-clasps`; περιδέξιον *armlet for the right arm*, the noun inside
  LSJ's περιδέξιος, Middle Liddell's περιδέξιος being the adjective alone, plain; ἀρχιτεκτονία `of architecture and
  construction`; ποικιλτός `variegated and broidered`. κάτεργον is in neither lexicon: plain, as at 30:16.
- **Restored whole** (`MARKUP_LOST`): παράρρυμα *anything drawn along the side: a leathern or hair curtain, stretched
  along the sides of ships*, `the anything drawn along the side and the leathern or hair curtains stretched along the
  sides of ships`.
- **By voice** (`FORM_SENSES`): ἀνακαλέω's active, `has called up the dead and it stands so, …, has summoned and cited,
  has called, has called on, has called back and recalled`, the middle's left out, as the middle at 31:2 leaves out the
  active's; συνίημι's active `to bring or set together, to perceive and hear, to understand`; ὑφαίνω's active `to
  weave, to weave and ply the loom, to contrive and plan and invent, to create and construct`.
- **Set aside** (`NOT_SENSES`): συναθροίζω's examples, *collected amounts*, *has not joined*, `gathered together and
  assembled`; συνίημι's participle's *to the intelligent*.
- New chains: κατάπαυσις `a putting to rest and a putting down and deposing, a cessation and calm`; κατοικία `to a
  settlement and colony and the foundation of a colony`; καταδέχομαι's participle; λιθουργέω `to turn into stone and
  petrify`, Middle Liddell's one sense; προβιβάζω `to make step forward and lead forward and lead on, to lead on and
  induce, to push forward and advance and exalt, to teach beforehand`; πλήρωσις `of the filling up and filling, of the
  satiety, of the completion of a number`; σφραγίς's accusative plural; κάλυμμα's plural; ἱστίον, φάος, σμάραγδος,
  χιτών, θρίξ, αἴγειος, ἱερατεία, σύνθεσις, κατασκευή, ἀφαίρεμα, σοφία, διάνοια, ποικιλία with or without the article
  in the forms the chapter has; σοφός in the singular; καίω's, φέρω's, λειτουργέω's futures; ἐργάζομαι's imperative;
  κατεργάζομαι's infinitive.
- One translation each, plain text: ὑακίνθινος *hyacinthine*; διανήθω *having been spun out*; νήθω *to spin*; νέω
  *spun*, *having been spun and standing so*; λογεῖον *the speaking-place*.
- **Morphology**: the second pass was right twice: αὐτοῦ at 35:16 neuter, the altar's; αὐτῶν at 35:26 feminine, the
  women's. φάος, νέω and Ουριας keep the corpus's lemmas.

### Words new in EXO 36

- **The page's own misprint**: 36:13 prints παὶ for καί; the transcription keeps it, the verse's `printed` field
  lists it, the module reads καί, and it reads *and*.
- **The order**: 36:8–38 gives the priests' garments, which the Hebrew gives at 39:1–31, before the tent's
  curtains; a `divergence` note at 36:8.
- **From LSJ** (not in Middle Liddell): συμπορπάω, which LSJ files as the passive συμπορπάομαι, *to be fastened
  together*; περισιαλόω, filed as περισιαλόομαι, *to be broidered round the edge*: plain, in the perfect's state.
  συνυφή `of the web, of the construction, of the amorous embrace`. ἐκκόλαμμα and συμπλεκτός are in neither
  lexicon: plain *a thing scraped out*, from ἐκκολάπτω, and *twined or plaited together*, from συμπλέκω.
- **The passive** (`FORM_SENSES`), each sense in the passive and the senses with no passive left out — the absolute,
  the intransitive, the middle's: τέμνω's aorist `was cut and hewn, …, was brought to a decision, was operated
  upon`; κωλύω's aorist `was let and hindered and checked and prevented, was let or hindered, was hindered and
  prevented and impeded, was hindered`, its participle's and impersonal senses left out; χαλάω's subjunctive `may be
  slackened and loosened, may be unstrung, may be let down and let sink and fall or droop, …, may be loosened or
  undone`. δίδωμι's aorist passive `was given, was granted, was provided, was given over and delivered up`, the
  present's *is ready to be given and offered* left to the present.
- **By number**: γράμμα's plural `things which are drawn, the lines of a drawing or picture, …, letters and
  learning`, the singular's senses in the plural and the senses marked "in sg." left out.
- **The adverb**: ἑκουσίως, inside ἑκούσιος (`SPELLING`), `voluntarily, willingly and acting of free will`, as
  δικαίως at GEN 27:36; the neuter's *voluntary acts* left out.
- **Set aside** (`NOT_SENSES`): the examples' pieces of τέμνω, ἐγγράφω (and Virgil's Latin), γράμμα (*to read*,
  *kept school*), ἐπίκειμαι and χαλάω (*having unbent*).
- **One translation, one item**: μηκέτι `no more and no longer and no further`; ἐκκολάπτω `having been scraped out
  and obliterated and standing so`; ἀδιάλυτος `undissolved and indissoluble`.
- **The article apart from its word**: τὰ ἅγια καθήκοντα, the article in ἅγια's unit and καθήκοντα `things having
  come`, as τὴν ἐρυθρὰν θάλασσαν at 13:18; τοὺς ἑκουσίως βουλομένους, `the ones` plain before the adverb; τὸ αὐτοῦ
  ἔργον, `the work` of him, as 18:23; τὸ δὲ περιστόμιον, the particle first.
- New chains: σοφία and ἐπιστήμη in the nominative; ἔχω's articular plural participle; βούλομαι's participle;
  προσπορεύομαι's and συντελέω's infinitives; φέρω's present and genitive participle; the imperfects of προσδέχομαι
  `were receiving favourably`, παραγίνομαι `were being near` and ἐργάζομαι `were working`; προσφέρω's infinitive and
  passive participle; προσκαταλείπω `left besides as a legacy, lost besides`; ἐν with ἐργάζομαι's participle;
  χρυσίον's articular genitive; the datives of ὑάκινθος, πορφύρα and κλώθω; συνυφαίνω's aorist infinitive and
  passive; πέταλον's plural; γλύφω's perfect participle; ὄνομα's articular genitive singular; ποικιλία without the
  article; περικυκλόω's perfect passive, *to surround* among its senses; ἐγγράφω's perfect passive `having been marked
  in or on and painted on and standing so, …, having been entered on the judge's list and indicted`; ἐμπλόκιον's
  genitive singular and articular plural; δακτύλιος's genitive plural; συμβολή's plural; πτερύγιον `wings, turrets
  or pinnacles`; ῥοΐσκος's articular genitive plural; κώδων's articular plural; λειτουργέω's articular infinitive;
  περισκελής and ζώνη with the article; ἐπίκειμαι `to be laid upon, to be put to or closed, …, to be imposed`;
  ἐν τῷ μέσῳ `in the middle`.
- One translation each, plain text: ὦμος, λογεῖον, λῶμα (*border of a robe* without the article), ὑποδύτης,
  τοπάζιον *topaz*, ἴασπις, λιγύριον, ἀχάτης, χρυσόλιθος *topaz*, κατάλιθος, τετράστιχος, δώδεκα *twelve*, συσφίγγω
  *condensed*, διυφαίνω, ποικιλτής, ἀλλήλων *one another*. δύο plain, as at 28:9 (Q29).
- **Corpus fixes**: χρυσίον's articular chain `the piece of gold, the gold, the gold coin and money`, the article on
  every item as on every noun's (GEN 2:11, 2:12; EXO 28:5, 31:4, 35:32); EXO 35:25's plain νενησμένα `having been
  spun and standing so`, the perfect's state; παραγίνομαι's present forms (GEN 32:21, 45:19; EXO 18:6, 18:15, 19:9)
  take the card's eight senses, `is near and attends upon, …, is fully grown`, where they had four not on the card,
  `come to be beside, be present, arrive, come to help`.
- **validate.py**: `AUXILIARIES` takes *having*, the plain perfect participle's: διυφαίνω's *having been filled up
  by weaving* is not ἔχω's headword loose beside it.
- **Morphology**: the second pass was right on three: κάτωθεν and ἄνωθεν before a genitive are prepositions, as
  ἄνωθεν at 25:22; αὐτοῦ at 36:37 neuter, the plate's. Anarthrous ὑακίνθου keeps the masculine (Q22), διανήθω
  the corpus's lemma, ὅλον ὑακίνθινον at 36:29 the neuter of ἔργον ὑφαντόν beside it.

### Words new in EXO 37

- **The order**: the Greek gives the curtains, the veil and the screen, then the court, which the Hebrew gives at
  38:9–20; the goats'-hair covering, the skins and the boards of the Hebrew's 36:14–34 are not here. A `divergence`
  note at 37:1.
- **From LSJ** (not in Middle Liddell): ῥαφιδευτός, which LSJ glosses only "= ῥαπτός", reads Middle Liddell's
  ῥαπτός, as πόρευσις reads πορεία's (GEN 33:14); used as a noun at 37:21 it is headed by the entry's noun sense,
  `the embroidered carpets, the stitched and patched, the strung together and continuous, the worked with the
  needle` (Q30). ποικιλτικός, *skilful in embroidery*, plain; LSJ's *embroidery* is the feminine's, ἡ ποικιλτική.
- **Set aside** (`NOT_SENSES`): λειτουργία's list of the Athenian liturgies and its *hence our word liturgy*;
  ἐξισόω's example's *acts*.
- New chains: καταχρυσόω's perfect passive `having been covered with gold-leaf and gilded and standing so, having
  been made golden` and aorist `covered with gold-leaf and gilded, made golden`; αὐλή with the article; ἱστίον's
  dative with the article; νῶτος's genitive with the article; ἀγκύλη with the article; ἐξισόω's present
  middle-passive participle `being made equal or even brought to a level with, being put on a level, making itself
  equal, being or becoming equal, being a match for and rivalling, being equal or like`; συντάσσω's aorist passive
  `was put in order together, …, was ordained and prescribed`; λειτουργία `the liturgy, the public duty, the any
  service or ministration and help, the public service, the service or ministry`; ἀρχιτεκτονέω's aorist `was the
  architect, constructed and contrived`.
- One translation each, plain text: κλίτος *the clime*; λίψ *SW. wind*, without the article, as at 27:9; ὑφάντης
  *of a weaver*; the numerals.
- **The article apart from its word**: τὰ πρὸς λίβα ἱστία, `the any webs` and the phrase after, as at 36:4.
- **Morphology**: the second pass was right on seventeen: the measures and τὸ αὐτό in the verbless clauses of 37:2
  and 37:16 nominative; the αὐτῶν that are the hangings' or the curtains' neuter or feminine. Anarthrous ὑακίνθου
  keeps the masculine (Q22), νῶτος the masculine of GEN 49:8, Ουριας the corpus's lemma.

### Words new in EXO 38

- **The order**: the ark, the mercy-seat, the table and the lampstand, which the Hebrew gives at 37:1–24, without the
  Hebrew's altar of incense; then the pillars, rings and pegs, the bronze altar, the oil and incense, and the laver.
  `divergence` notes at 38:1 and at 38:26, where the Hebrew's women who served, ṣōbĕʾōt, are the Greek's women who
  fasted.
- **From LSJ** (not in Middle Liddell): λαβίς `the handles, the hilts, the holders, the forceps, the clamps and
  clasps, the tongs or snuffers`, LSJ citing 38:17 for the last; ἐπαρυστρίς, "= foreg.", reading ἐπαρυστήρ's *vessel
  for pouring oil into a lamp*, plain, as at 25:38; παράθεμα *appendage*, plain; διωστήρ `instruments for pushing out
  embedded weapons, poles running through rings for carrying the ark`; ἐνθέμιον `cabin on the poop of a ship, socket
  of a lampstand`; καρυωτός, the adjective LSJ cites from 38:16, *adorned with a nut-shaped boss*, plain, its
  *date-palm* being the masculine made a noun.
- **Set aside** (`NOT_SENSES`): στερεός's examples' *solid gold* and *a cubic*; its adjective leaves out the adverb's
  *firmly, fast* (`FORM_SENSES`). καταστασιάζω's active leaves out the passive's senses, and is plain, *to form a
  counter-party in the state*.
- New chains: εὐρύς `wide and broad, far-reaching and far-spread`; σκιάζω's participle `overshadowing and shading,
  overshadowing and covering, shading in painting`; πρόκειμαι's articular participle; φωτίζω `enlightens and
  illuminates and instructs and teaches, brings to light and publishes, enlightens spiritually, baptizes`; στερεός
  `stiff and stark and firm and solid, stiff and stubborn and harsh`; βλαστός with the article; ἐξέχω's participle
  `standing out, projecting from, standing out and appearing`; λαμπάδιον `the small torches, the bandages`; λύχνος
  without the article; περιαργυρόω's aorist `cased and plated with silver`; χρυσόω's aorist `made golden and gilded`;
  ἐκτείνω's articular infinitive; κατακάλυμμα with the article; χαλκοῦς with the article, `the of copper`; ἀνήρ's
  articular dative plural; δικτυωτός without the dative; κάτοπτρον `of the mirrors, of the mere reflexions`; νίπτω's
  middle subjunctive and imperfect, `may wash one's hands`, `were washing one's hands`; εἰσπορεύομαι's anarthrous
  genitive participle; μέρος without the article; δεύτερος's neuter genitive.
- One translation each, plain text: χωνεύω *cast into a mould (χόανος)*; θυΐσκη *censer*; λυχνία *lampstand*;
  καλαμίσκος *a bit of reed*; πυρεῖον *pieces of wood*, read in the number the form wears; κρεάγρα *a flesh-hook*;
  ἔλαιον *olive-oil*; λουτήρ *washing or bathing-tub*; νηστεύω *fasted*; θυσιαστήριον *altar*; the numerals.
- **Names**: τῆς Κορε συναγωγῆς, the article συναγωγῆς's and the name after its unit, as at 36:4.
- **validate.py**: `own_article` compares gender as well as case, so an article in another gender is not taken for a
  name's own. It found two places the case-only check had passed: GEN 24:24 τοῦ Μελχας, now `of the one of Μελχας`,
  and EXO 23:31 τῆς Φυλιστιιμ, now `of the one of Φυλιστιιμ`. `test_validate.py` has a case for it.
- **Morphology**: the second pass was right on three: σκιάζοντα masculine singular with χερουβ ἕνα, αὐτῶν after it
  masculine, and τεσσάρων with the neuter μερῶν neuter. τρύβλιον and θυΐσκη keep the corpus's lemmas.

### Words new in EXO 39

- **The order**: the tallies of the metals, which the Hebrew gives at 38:24–31, come here after the furnishings;
  a `divergence` note at 39:1.
- **From LSJ** (not in Middle Liddell): χώνευσις, "= χωνεία", reading LSJ's χωνεία, *melting and casting of metal*,
  plain.
- **Set aside** (`NOT_SENSES`): διφθέρα's *(an undressed hide)*, its contrast with δέρρις; κατακοσμέω's example's
  *was fitting*; πρόθεσις's example's *laid before, the shewbread*, from οἱ ἄρτοι τῆς προθέσεως itself.
- **A deponent's perfect participle**: τῶν ἐπεσκεμμένων ἀνδρῶν at 39:2 reads ἐπισκέπτομαι's middle senses, `of the
  ones having looked upon and standing so, …, having examined with themselves and meditated`, as ἐπέσκεμμαι at 3:16;
  the entry gives no passive sense, and a passive reading had dropped one of the eight (Q31).
- New chains: κατεργάζομαι's aorist passive `was effected by labour and achieved and accomplished, …, was effected,
  was overcome`, the intransitive *to be successful* left out; ἐργασία with the article; τάλαντον's plural `balances,
  a pair of scales, anything weighed, definite weights and talents, weights, sums of money`, the plural's own *pair of
  scales* given as the entry gives it; ἀπαρχή's genitive; ἀνήρ's anarthrous genitive plural; μυριάς's anarthrous
  plural; κεφαλίς without the article and in the dative singular; κατακοσμέω `set in order and arranged, fitted out
  completely and adorned, reduced to order`; καταλείπω's feminine articular aorist passive participle; καῦσις
  `of the burning, of the cautery`; πρόθεσις `of the placing in public, of the laying out, of the public notice, of
  the statement, of the purpose and end proposed, of the supposition and calculation`; πρόκειμαι's articular plural;
  ἱερατεία with the article; διφθέρα `the prepared hides and tanned skins and pieces of leather, the leathern
  garments, the wallets and bags, the skins used as tents`; λοιπός's articular genitive plural; ἐπικάλυμμα with the
  article; ποιέω's perfect participle `having made and standing so, having done, having produced, having created`.
- One translation each, plain text: σίκλος *shekel*; λειτουργικός *ministering*; ἔναντι *in the presence of*; the
  numerals, the article printing with them, `the a hundred`.
- **Morphology**: the second pass was right on αὐτοῦ at 39:15, neuter, the altar's. φάος keeps the corpus's lemma;
  Ααρων at 39:18 keeps the dative of 36:8.

### Words new in EXO 40

- **Verses Rahlfs does not print**: 40:7, 40:11, 40:28 and 40:30–32; the module agrees, and a note on the verse after
  each gap says so.
- **The date**: 40:17 adds ἐκπορευομένων αὐτῶν ἐξ Αἰγύπτου to the Hebrew's month and year; a `divergence` note.
- **From LSJ** (not in Middle Liddell): διεμβάλλω *put in through*, plain; ἀπαρτία `to the household utensils and
  movables and chattels, to the spoil, to the public auction`, LSJ's own glosses after its "= ἀποσκευή"; ἀναζυγή, "=
  ἀνάζευξις", reading Middle Liddell's ἀνάζευξις, `to the marchings off and returns home`.
- **By voice** (`FORM_SENSES`): προτίθημι's active leaves out the middle's senses and the passive's *was allowed*:
  `you will place or set before and set out, you will throw, …, you will prefer`; the aorist the same.
- **Set aside** (`NOT_SENSES`): ἐπισκιάζω's passive participle's example, *keeping a hidden watch*.
- New chains: νουμηνία `to new moon and first of the month, to true new moon`, without the article; ἵστημι's future;
  σκεπάζω's future; πρόθεσις's accusative with the article; θυμιάω's articular infinitive and aorist; κάρπωμα's
  articular genitive plural; καταπέτασμα's anarthrous genitive; ἀλείφω's future `you will anoint with oil and oil,
  …, you will stop up`; ἱερατεία's anarthrous genitive; δεύτερος's neuter dative; δόξα's anarthrous genitive;
  δύναμαι's aorist passive singular; ἐπισκιάζω's imperfect `was throwing a shade upon and overshadowing`;
  ἀναζεύγνυμι's imperfect `were yoking again, were moving off, were breaking up, were moving, were breaking up and
  shifting one's quarters`.
- One translation each, plain text: ἔτος *year*; ἱερατεύω *to be a priest*.
- **Morphology**: the second pass was right on τὸ θυσιαστήριον at 40:10, the nominative subject of ἔσται; κύκλῳ before
  a genitive at 40:33 and ἔξωθεν at 40:22 are prepositions.

### The edit pass after Exodus

Chains the settled open questions changed, corpus-wide.

- **Pointers read** (`SENSE_POINTERS`, Q14): πάγος adds *frost* (παγετός); μήν, filed under μείς, adds
  μηνίσκος's *a crescent, nimbus, glory*, and is a unit now: `month, a crescent, nimbus, glory`, `of the
  month, of the crescent, of the nimbus, of the glory`, ἐν merged where it stands before it; λίβανος
  adds λιβανωτός's *frankincense, the gum of the tree, a censer* (EXO 30:34, a unit); ἀποσκηνόω adds
  ἀποσκηνέω's *to encamp apart from* (GEN 13:18, a unit); καθώς reads καθά's two runs first, `according
  as / just as, like as if / exactly as, how`. διπλοῦς's *= δύο* and μηρός's *= μηρία* are the plural's;
  θάνατος, βότρυς, γερουσία and ὅρμος add their pointers' translations. Not read (`POINTERS_NOT_READ`):
  περί's *= ἀμφί* (a compound's), ἅμαξα's *= ἁμαξιτός* (no entry), δοῦλος's (the neuter τὸ δοῦλον's),
  εἰ's (a construction's), ὅς's (early Greek's demonstrative).
- **παραγίνομαι** (Q15): `MARKUP_LOST` restores the first translation whole, *to be beside, to be by or near,
  attend upon*, which Perseus cut to *near, attend upon*; every form heads with *beside* and reads the card's
  eight senses: `was beside / was by / near / attended upon, was present at, …, was fully grown`, `is beside
  …`, `I am beside / am by / near / attend upon …`.
- **ἐξίστημι** (Q18): the intransitive forms — second aorist, perfect and pluperfect active, and the middle
  and passive — read Middle Liddell's intransitive section, by `FORM_SENSES`, and `MARKUP_LOST` restores *to
  lose one's father, give him up* and *to lose one's senses*: `stood aside from, was displaced / disordered,
  shrank from / shunned, retired from / gave up possession of, ceased from / abandoned, lost one's father / gave
  him up, lost one's senses, was out of one's wits / was astonished / amazed, degenerated, changed one's position
  / one's opinion` (GEN 27:33, 42:28, 45:26; EXO 18:9, 19:18), `were standing aside from, …` (GEN 43:33). The
  chain it replaced, `stood out of, changed and altered utterly, …`, came from no card.
- **ὑπάρχω** (Q12): the card settled. `NOT_SENSES` files sense I's repeats and pieces, the c. gen.
  construction's *there is store*, the Latin, an example's *he will be on … side*, and the impersonal
  construction's *the fact is that*, *it is allowed, it is possible*; `FORM_SENSES` gives the passive *to be
  begun*, the participle *existing, current, own proper, normal*, and τὰ ὑπάρχοντα, the neuter plural
  participle, the noun's senses alone. The verb: `begins / makes a beginning, begins to be / comes into being /
  arises / springs up, is in existence / is there / is ready, is, is laid down / is taken for granted, belongs to
  / falls to, accrues, is devoted to`; the noun: `the existing circumstances / present advantages, the what
  belongs to one / one's possessions / means`, which GEN 31:18 and 34:23, read before as `the things beginning`,
  now take too.
- **ἀναγγέλλω** (Q11): the run is one item, `carried back tidings of / reported`; *was reported* is the
  passive's, by `FORM_SENSES`, and the passive's run says it: `was carried back tidings of / reported`.
- **Every chain carries its card** (Q1, Q24). `validate.py`'s coverage check reads each unit against the
  translations its entry gives its form, after `NOT_SENSES` and `FORM_SENSES`; the coverage pass sorted every
  translation a chain left out into a sense, now in the chain, or a non-sense, set aside in `COVERAGE_NOT`
  (`words.py`, the reason the value: a label, Latin, an example's piece, a phrase's translation, a repeat), or a
  sense of some forms only, in `COVERAGE_ONLY` (by a `FORMS` name: plural, passive, participle, neuter …).
  φιλέω now says *kissed*; προσάγω's intransitive *draws near* is in EXO 3:4's chain. The pronouns and the
  formula words — θεός, ἐν, γίνομαι, ἀρχή at GEN 1:1 — are outside the check.
- **The delimiter** (Q2). A run of one translation is one item, its pieces joined with ` / `: `the wooden box /
  chest / coffer`, `carried back tidings of / reported`. Two translations the entry joins with *or* are one
  translation on the card (the loader joins them) and one item in the chain, `went up with / together`; where the
  first piece is a bare preposition or a word only the second completes, the *or* stays as printed: `of or from
  the gods`, `washing or bathing-tub`, `little or young child` (Q26). *and* stays only where the entry's own
  translation has it, `murder and manslaughter`.
- **The perfect's formula after every item** (Q17): `has given and it stands so, has granted and it stands so, …`.

### Q32–Q35: the cards read back, and the voice of each sense

- **A chain says only its card** (Q32). `validate.py`'s support check is the coverage check turned round: every
  item renders a translation the entry gives the form. 314 items no card gave were dropped or settled. Dropped:
  δέ's *however* (all 1,255 units); ὅτι's *although* and γάρ's *but* (the phrases οὐχ ὅτι and ἀλλὰ γάρ);
  ἄνθρωπος's *the human being* (the entry gives *man, mankind*; its *homo, not vir* is Latin, which the notes
  say); ἕτερος's *worse*; παῖς's *the grandchildren* (παῖς παιδός's); ἀρχή's *the headship and rule and governing
  precedence* outside GEN 1:1's formula; and the older *X and Y* items one of whose words no card has (τίκτω's
  *produced and yielded*, θυμός's *will and desire*, κόσμος's *ornament and adornment*, …), each sense still said
  by the card's own item.
- **Settled, not dropped**: translations the tagging cuts where the printed entry runs on in plain English,
  restored in `TEXT_LOST` (`words.py`), each value the entry's words in order — διαθήκη `the disposition of
  property by will`, `the arrangement between two parties`; διατίθημι `to dispose of one's property`, `devise it
  by will`; γλῶσσα `the tongue / mouthpiece of a pipe`; κείρω `to ravage a country`, `by cutting down the crops
  and fruit-trees`; μυριάς `a number of ten thousand` (the entry's *10, 000*, in words, since a comma parts a
  chain); πύργος, σφάζω, συντελέω, τετράπους, ἐργασία, ἐγχώριος, ἐξαριθμέω, ἐπικαλέω, κτάομαι, ἀγγεῖον, συννεφέω,
  χρονίζω, μαῖα (`the true mother`, its *mother* a piece), ἀπάγω (`to lead away from the subject`), ἀλλάσσω,
  συγχαίρω (`wish one joy / congratulate`), ἀπόλλυμι (`talk / bore one to death`). Two later-sense Latin runs, which
  the first-sense check never reads, go in `MARKUP_LOST`: αἷμα's *blood-relationship, kin*, ἐξαλείφω's *to wipe
  out, destroy utterly*. σκεῦος's «the vessel» stands inside the entry's account of a metaphor (*the body, as the
  vessel of the soul*) and is a label.
- **πλατεῖα** (`FILED_WITHIN`): *the street* is πλατύς I.5, read now as that section alone, `a street, the flat
  of the hand` (GEN 19:2); πλατύς's adjective senses are the adjective's, its noun senses the noun's (Q33).
- **The coverage calls, read word by word** (Q33), for the fifty commonest words and ἔχω, φέρω, γινώσκω, ἀκούω,
  οἴομαι, φύω, φιλέω, εὑρίσκω, προστίθημι: 99 calls moved, now in `COVERAGE_NOT` and `COVERAGE_ONLY`. Example sentences kept as senses are pieces now: γινώσκω's *I felt that I was*, *thou mayst
  discern*; καλέω's *shall be given*, *I am*, *is*; ἀκούω's *pers. from whom it is heard*; ἔρχομαι's *I go to*,
  *I intend*; λέγω's *has*, *does*; ἔχω's *by*, *will*, *you keep*. Phrases with a preposition are phrases: χείρ's
  *in hand*, *hand to hand*; οἶκος's *home, within* (κατ᾽ οἴκους); εἷς's *one by one*; ἡμέρα's *day-break*, *day by
  day*; and a case's own English is its marker's: ἡμέρα's *within*, *on*, χείρ's *on*. Finer forms, by new `FORMS`
  names: πᾶς's *everything, anything* the neuter singular's; τίκτω's *the father, the mother, the parents* and
  ἔχω's *a wealthy man* the active participle's; λέγω's *the so-called* and τίθημι's *the deposits* the passive
  participle's; φέρω's *fortune, fate* and ὀρθόω's *success* the neuter participle's; καλέω's *to have received a
  name, to bear it* and *to be* the perfect passive's; γινώσκω's *I understand* and λέγω's *I mean* the first
  person active's. συνίστημι's intransitive section, given the passive alone, is read again by the perfect and
  the aor2 (EXO 7:19, 32:1); its transitive tenses leave it out by `FORM_SENSES`. ἀποκρίνω's *to separate, set
  apart* is its passive's too (GEN 31:14), and the deponent ἀποκρίνομαι sets it aside by name.
- **Each sense in its own voice** (Q35). A passive form reads the entry's Pass. senses as printed, in the form's
  tense and person: κοιμάω `fell asleep / went / lay abed` (GEN 19:33, never `was fallen asleep`); ἐπιφέρω at
  GEN 1:2 `was rushing upon or after / attacking / assaulting, …, was coming after / next / ensuing`; ἀποστέλλω at
  JHN 1:6 `having gone away / departed / set out and standing so`, its Pass. sense, while the intransitive *to go
  back, retire* is left out; ὁράω `let oneself be seen / appeared`; καθίστημι's [6] Pass. *to stand against,
  oppose*; φθείρω's *to have suffered loss from shipwreck* (`had suffered loss from shipwreck`, GEN 6:11) and
  *to pine away in*. 48 Pass. and Mid. senses read in every voice before are the passive's or the middle's now
  (`COVERAGE_ONLY`). A sense with no passive is left out of passive forms (*not passive*): ἐπιβάλλω's
  intransitives, κατέχω's *to prevail*, ἔχω's *to lead towards*, φέρω's *to lead to*: sixty in all. A form
  parsed middle-or-passive reads the Mid. senses in the middle's English: ἄγω at GEN 38:25 `being led, …,
  marrying, bringing home`. Where the object is the passive's subject, `PASSIVE_OF` gives the passive the entry's
  gloss makes: δικαιόω `has been done right / justice / judged` (GEN 38:26), διακόπτω, κατέχω, ποτίζω, χαλάω,
  ἀνασώζω (`of the ones having been recovered / rescued`, the reading before the coverage pass), τέμνω, καταπαύω.
  An example's person or tense is the verb's, worn in the form: οἴομαι at GEN 37:7 `I was having a presage, …, I
  was holding`; γινώσκω `will be aware of`.
- **The checks behind it**: the support check above; the English check (no auxiliary before a subject or a second
  auxiliary, no function word with a verb's ending), which found the 70 units of example sentences rendered as the
  word's; and the cards' alignment: a word a verse says more often than it opens takes, in order, the occurrence
  whose card its chain fits (δέρρις at EXO 26:8 opens its third occurrence).

### Words new in JHN 1

- **The text**: SBLGNT's line, verbatim, its signs kept (⸀, ⸂…⸃); MorphGNT's morphology. Every verse carrying a
  sign has a note flagged `variant`, and validate now checks it (1:28's ⸀ before ὁ had none).
- **εἰμί**: where the Logos, the life or the light is the subject, the prologue's formula, `was, and was
  continuously, and was already in unbroken existence without any point of having come to be` (1:1, 1:2, 1:4, 1:9,
  1:10, and 1:15 and 1:30 of the one coming after John, who was first). Elsewhere the creature's, `was, and kept on
  being as a standing and continuing condition and not a momentary one`: John at 1:8, the ones sent at 1:24, the
  place and the hour at 1:28 and 1:39, Andrew at 1:40, Philip at 1:44. The infinitive at 1:46 `to be, to exist, to
  last`.
- **γίνομαι**: `came into being` heading `came to be, arose, was brought into existence` (1:3, 1:10, 1:14, 1:17,
  1:28); the perfect `has come into being` heading `has come to be and stands so, has arisen and remains arisen, has
  been brought into existence and continues so` (1:3, 1:15, 1:30); 1:6 keeps its `there came to be`.
- **χριστός**: capitalised at 1:17, Ἰησοῦ Χριστοῦ, it is a name, `Christ (Χριστός, the Greek for "anointed", …)`. In
  lower case at 1:20, 1:25 and 1:41 it is the noun, `the anointed one / the christ, the messiah`, Middle Liddell's «the
  Anointed One, the Christ», «Messiah», with no capital, since the Greek marks none.
- **Names**: Ῥαββί, Μεσσίας and ἀμήν are transliterations, and names. A later occurrence in another case, or without
  the capital that opened a speech, takes a bare entry: Σίμων at 1:42 after Σίμωνος at 1:40, ἀμὴν after Ἀμὴν at
  1:51. The names check had read the first pair as two names (a bare stem is matched only to a form one letter
  longer, which keeps Καιν from Καιναν) and the second as two because of the capital; both had been glossed twice.
- **Lexicon keys**: φῶς reads φάος, the contraction Middle Liddell prints inside it (`SPELLING`), and φάος's *eyes*,
  "in pl.", is the plural's alone, out of EXO 10:23, 27:20, 35:14 and 39:16's singulars. ἴδε reads the second ἰδέ,
  «lo, behold». μεθερμηνεύω is not in Middle Liddell: LSJ, *translate*, plain.
- **Restored** (`TEXT_LOST`): ἐξηγέομαι's «to shew» one «the way, go before, lead»; ἱμάς's «the traces by which horses
  were» attached to the chariot.
- **A misprint** (`MISPRINTS`, new): μένω's «to be lasting, remian, last, stand». GEN 24 had printed *remain*; the
  Q24 rebuild read the card back, misprint and all, into every μένω unit. The card says *remain* now, and the nine
  units do.
- **ὅπου**: a relative adverb of place, which the entry says in prose. Its first translation, «in some places», is
  the phrase ἔσθ' ὅπου's, and «somewhere or other» and «wherever» are ὅκου δή's and ὅπου ἄν's; with the pieces of
  οὐκ ἔσθ' ὅπου they are set aside. It heads with *where*: `where, whereas` (1:28).
- **By form** (`dec9zz_john.jsonl`): ὁμολογέω's Pass. senses, *things granted* the passive participle's, *I grant*
  the first person's; ἱμάς's plural senses (*the reins*, *the lash*, *the caestus*) and the singular's *girdle*;
  βαπτίζω's *soaked in wine* (Pass.) and *to get oneself baptized* (Mid.); ἐξουσία's *the authorities* (pl.);
  φανερόω's *to become so* (Pass.).
- **Set aside** (`NOT_SENSES`): εὐθύνω's pieces (*straight*, *to make*, *call*, *to account*); ὁμολογέω's οὐδὲν ὁμ.
  τινι; διδάσκαλος's *school* and the label *taught the actors*; φωνέω's pieces; θεάομαι's οἱ θεώμενοι; βαπτίζω's
  *over head and ears*; πλήρωμα's possessives (*their fill*, *their complement*); ἐξηγέομαι's piece of «to shew».
- **πᾶς**: Q33 gave *the whole / one's all* to the neuter singular, τὸ πᾶν. 564 chains in Genesis and Exodus
  carried it in other forms; they do not now.
- **Corrections beside it**: στρέφω at GEN 3:24, EXO 4:17 and 7:15 reads `turning to and fro` again. The delimiter
  check had taken that *and* for the pieces of «to turn to» or «from», since the first item holding *turn* was the
  one it read, and a mechanical pass cut it to `to / fro`; the check now reads the item that says the run and least
  else. `to turn to or from` is in all four chains (`the one turning to / from`), and `revolving` carries the
  article's noun as the rest of the chain does. JHN 1:38's aorist passive had been passivized again (`having been
  tossed`), which Q35 rules out: `having turned himself / having turned round / having turned about / having turned
  to and fro, having tossed, …`, as EXO 4:17. ὑπόδημα's «a shoe or half-boot» is two translations joined with *or*:
  `the shoe / half-boot` (GEN 14:23, EXO 3:5, 12:11, JHN 1:27). πλήρης at GEN 35:29, EXO 9:8 and 16:33 gains
  `filled with`, as its siblings carry it. The stemmer read *relying* as *re-* and *lying*; it does not now.
- New chains: φῶς `the light / daylight`; σκοτία `within, inside of, and by means of the darkness / gloom`; ἐξουσία
  `power / authority, power over / licence in, an office / magistracy, abundance of means / resources, pomp`; θεάομαι
  `we looked on / gazed at / viewed / beheld, we reconnoitred, we viewed as spectators, we reviewed`; μονογενής
  `only-begotten / single, one and the same`; πλήρωμα `of the full measure, of the satiety, of the full number, …`;
  ἐξηγέομαι `was leader of, led / directed / governed, went first / led the way, …`; ὁμολογέω `spoke together, spoke
  one language, …`; ἀπόκρισις `a separating, an answer`; εὐθύνω `guide straight / direct, steer, …`; βαπτίζω `you
  dip in / under water, you baptize`; ἱμάς `the leathern strap / thong, the girdle, the chin-strap, the latchet /
  thong, the dog-leash`; ἴδε `lo / behold`; φανερόω `may be made manifest, may be made known / famous, may become
  so`; μαθητής `of the learners / pupils`; ἐμβλέπω `having looked in the face / looked at`; ἀκολουθέω `followed /
  obeyed, went after or with, followed the thread, followed upon / were consequent upon`; διδάσκαλος `teacher /
  master, a dramatic poet`; ἑρμηνεύω `is interpreted / put into words / given utterance to, is explained`; φωνέω's
  articular infinitive `of the producing a sound / tone, …, of the having a voice / being significant, …`; τίς `who
  / which`; σκηνόω `pitched tents / encamped, dwelt in a tent, …`, the verb of GEN 13:12.
- One translation each, plain text: ἀμνός *a lamb*; ἀγαθός at 1:46, whose noun senses are the same word.
- συκῆ: `the fig-tree, the fig` (1:48), `of the fig-tree, of the fig` (1:50), as GEN 3:7. Drafted plain, it passed:
  the unit check read *fig-tree* as *fig* and *tree*, so *a fig* said nothing more. It keeps a hyphenated word
  whole now, and no other word in the corpus moved.
- **Tools**: `siblings.py` rebuilds a new chapter's units from their fullest corpus sibling, so the range check has
  nothing to report; `repair.py`'s seed rule expands a chain that is its headword alone.
