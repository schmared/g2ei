# Second-pass brief

Every Old Testament chapter's morphology is written twice. The first pass is
`data/<BOOK>/<chapter>.morph.txt`. The second is made by a separate agent that sees only the
Greek and the conventions below — never the first — and `build/morph_diff.py` lists every
place the two disagree.

The second pass shares no memory with the first, so it catches slips of attention: a shifted
slot, a gender agreeing with the wrong noun, a case left over from the previous word. It does
not catch what both passes would get wrong for the same reason. That is what the reference
data is for when a disagreement is settled.

## Running it

1. Print the chapter's Greek and its word counts. The session runs this, not the agent —
   the chapter's JSON holds the notes, which contain analysis.

   ```bash
   python -c "import json,sys; sys.path.insert(0,'build'); import validate as V; sys.stdout.reconfigure(encoding='utf-8'); v=json.load(open('data/GEN/3.json',encoding='utf-8')); print(', '.join('%s %d' % (x['ref'].split()[1], len(V.PUNCT.sub('', x['greek']).split())) for x in v)); print(); [print(x['ref'].split()[1], x['greek']) for x in v]"
   ```

2. Give a **fresh** agent the brief below, with its placeholders filled. It has to be a
   separate agent: a session that wrote the first pass cannot make the second without
   remembering it.

3. Compare:

   ```bash
   python build/morph_diff.py data/GEN/3.morph.txt <the second pass>
   ```

4. Settle every disagreement in `data/<BOOK>/<chapter>.morph.txt` — never by editing the second
   pass to make the diff go quiet.
   - Where the question is **a convention** — a part of speech for a small word, a lemma's
     spelling — count what MorphGNT does in `sources/morphgnt/` rather than trusting either
     pass's memory of it. Genesis 2's ἐάν and ὅτε were both settled that way, in opposite
     directions.
   - Where it is **grammar**, the side that can say why wins, and a reason that disagrees with
     the reference module goes on the line as `# module …`.

5. A disagreement that traces back to this brief is a defect in the brief. Correct it here,
   so the next chapter's second pass does not repeat it.

### What it found in Genesis 2

Twelve disagreements over 531 words. The second pass was right three times — ὅτε and τε are
conjunctions, and Τίγρις is masculine — and wrong once, tagging the ἐάν of `ὃ ἐάν` as a
conjunction where MorphGNT tags that construction as a particle. The other eight came from
this brief: it told the second pass to give δύο no features, before MorphGNT was checked and
found to code δύο like any adjective. The brief below is corrected.

### What it found in Genesis 3

Six disagreements over 581 words, with the conventions for the chapter's new small words — ἰδού,
μήποτε, adverbial καί, ἀνὰ μέσον — added to the brief beforehand from MorphGNT counts. The
second pass was right four times: τοῦ at 3:2 goes with masculine παραδείσου, and αὐτοῦ at 3:3
(twice) and 3:5 resumes the fronted ἀπὸ καρποῦ, the fruit, not the tree — the reference module
reads all three the same way. It was wrong twice, and both trace to this brief: it had no rule
for τί ὅτι, and its rule for contracted nouns sent συκῆς to συκέα, where Middle Liddell and
MorphGNT both file συκῆ. Both rules are corrected below.

### What it found in Genesis 4

Three disagreements over 531 words, and the second pass was right all three times. ἐργᾷ at
4:12 is the contracted future of ἐργάζομαι, not a present — the reference module agreed.
σφυροκόπος at 4:22 is a second noun beside χαλκεύς, as the Hebrew has two. And ἑπτά closing
4:24 is an adverbial accusative, *seventy times seven*, not a nominative. None traced to this
brief; its names rule, extended beforehand with MorphGNT's spellings of the personal names
the New Testament shares, drew no disagreement at all.

### What it found in Genesis 5

Nothing: the two passes agreed on all 482 words. The chapter is a genealogy, its frame repeated
nine times, and the conventions it needed were added beforehand — MorphGNT's spellings of
Μαλελεήλ, Νῶε and Σήμ, the rule for a name the New Testament spells with other letters, gender
`C` for τρεῖς, numerals printed as several words, and a rule filing ἐννακόσιοι under Middle
Liddell's ἐνακόσιοι, which Genesis 6 showed to be wrong. The reference module disagreed with
both in eighty places, all annotated: it gives the indeclinable numerals no case, reads the years
after ἐγένοντο αἱ ἡμέραι as accusative everywhere but 5:31, and codes τρία at 5:31 masculine.

### What it found in Genesis 6

Three disagreements over 505 words, with MorphGNT's tags for the chapter's new small words —
ἡνίκα, οὖν, ὡς ἄν, the indefinite τις, ἐναντίον, ὑποκάτω, ὅσος — and its middle lemmas for the
deponents added beforehand. The second pass was right once: ἐκείνοις at 6:21 are the animals
of 6:19–20, neuter. It was wrong twice, and both trace to this brief. It filed νοσσιάς under
νεοσσιά and κατάγαια under κατάγειος, following the rule added for Genesis 5 that a later
spelling goes under the one Middle Liddell heads. That rule contradicted every earlier filing —
γίνομαι, ἔχθρα, δειλινός, κατέναντι — and MorphGNT's νοσσιά at Luke 13:34. The rule below is
corrected, and so is Genesis 5's ἐννακόσιοι.

### What it found in Genesis 7

Six disagreements over 521 words, all one word. The second pass filed τεσσαράκοντα under
SBLGNT's spelling, τεσσεράκοντα, following the rule as Genesis 6 left it: a word the New
Testament uses takes MorphGNT's spelling. That wording went further than the filings it
summarised. In every one of them — γίνομαι, ἔχθρα, νοσσιά — MorphGNT only agreed with the
spelling the text prints, and the spelling the text prints was the rule. It is restated below as
what the filings do. Nothing else disagreed; the chapter's new small words — καθά, ἐπάνω and
ἔξωθεν with and without a genitive, ἡ ξηρά — were added beforehand.

### What it found in Genesis 8

Two disagreements over 522 words, with ὀπίσω, καθώς, εἰ meaning *whether*, and the article before
a prepositional phrase added beforehand. The second pass was right about Αραρατ at 8:4: τὰ ὄρη τὰ
Αραρατ is *the mountains, those of Ararat*, the name a genitive after the article, as the Hebrew
construct *hārê ʾărārāṭ* has it, and as the reference module reads it too. It filed ἐμνήσθη under
μιμνήσκω where MorphGNT has the middle; the list of middle lemmas below had not named it, and now
does.

### What it found in Genesis 9

Nothing that `morph_diff.py` reports: the two passes agreed on all 566 words, with the chapter's
new small words — πλήν, ὥστε, ἀντί, ἔξω, the καί of καὶ γάρ, ὑμέτερος — and MorphGNT's Χανάαν,
διατίθεμαι and νεώτερος under νέος added beforehand. The diff counts gender `C` as agreeing with
`M` or `F`, and there the second pass was the more exact: αἰωνίους and αἰώνιον, with feminine
nouns, keep the forms αἰώνιος shares between masculine and feminine, and are `C` under the rule
below, where the first pass had them `F`.

### What it found in Genesis 10

One disagreement over 456 words, in a chapter of ninety-one names. The conventions the Table of
Nations needed were added beforehand: MorphGNT's forms of every name the New Testament shares,
place names among them; declined place names keeping their gender; peoples' names as nouns;
ὅθεν by its sense; ἕως before a bare infinitive; the genitive after γῆ. The second pass was right
at 10:32, where τούτων takes up αἱ φυλαί and is feminine. And again it was the more exact where the
diff forgives: πρωτότοκον at 10:15 is two-termination, `C`, where the first pass had `M`.

The reference module could not be read for this chapter at first: its code for Μεσραιμ holds a
space (`lxx.N.N M`), and `validate.py` split the verse on spaces. It now finds each word by its tags.

### What it found in Genesis 11

Nothing: the two passes agreed on all 599 words, exactly, with the chapter's new small words —
δεῦτε, πλησίον after the article, ἐνώπιον, οὗ as *whose* — the MorphGNT forms of the names of Luke
3:34–36, and στεῖρα's filing added beforehand. Both read the two forms that are one spelling for two
tenses, συγχέωμεν and συνέχεεν, as aorists, where the reference module has a present and an
imperfect.

### What it found in Genesis 12

Three disagreements over 433 words, with καθάπερ, ὅπως, τότε, εὖ, ἕνεκεν, ἐμαυτοῦ, the middles
χράομαι, κτάομαι and περιποιέομαι, and Φαραώ, Συχέμ and Αἰγύπτιος added beforehand. The second pass
was right twice, about gender the form does not show: ὄνοι is masculine and ἡμίονοι feminine, as
δέκα ὄνους αἴροντας and δέκα ἡμιόνους αἰρούσας show at 45:23, a better witness than MorphGNT's
she-asses. It was wrong once, from memory: it tagged ἐν τῇ ἐρήμῳ `N-`, where MorphGNT has ἔρημος `A-`
all 23 times in that phrase. The rule below now names it.

### What it found in Genesis 13

One disagreement over 389 words, with ἴδε and ἰδέ, ἅμα, συμπορεύομαι and δύναμαι, ἡ περίχωρος and τὸ
πρότερον, and Ἰορδάνης, Φερεζαῖος and the gender of Σόδομα and Γόμορρα added beforehand. The second
pass was right: ποτιζομένη is `-PEPNSF-`, voice E, since middle and passive share the present's
form; the first pass had written P, from the sense.

### What it found in Genesis 14

Three disagreements over 517 words, with the parentheses among the punctuation, ἅμα with a dative,
and Δαμασκός, Μελχισέδεκ, Σαλήμ, Βαλάκ and Αμορραῖος added beforehand. Each pass was right once
and half. The first was right that ἀνασωθέντων files under ἀνασώζω, without the iota subscript,
as Middle Liddell heads it. The second was right that Μαμβρη at 14:13 is a man, `----GSM-`: ὁ
Αμορις beside it names him the Amorite. On δεκάτην they split: the first pass had MorphGNT's
`A-`, the second MorphGNT's dictionary form, δεκάτη, which Middle Liddell also heads, with a
cross-reference to δέκατος. The rule below now names it.

### What it found in Genesis 15

Three disagreements over 365 words. The second pass was right that Δαμασκός in οὗτος Δαμασκὸς
Ελιεζερ names the man and takes his gender, as the brief's Σιδῶνα does. The first pass was right
twice, on small words the brief did not name: εὐθύς, *immediately*, which MorphGNT codes as the
adjective all 51 times, and the τοῦ of ἕως τοῦ νῦν, which it codes masculine. The brief names both
now, and the reciprocal ἀλλήλων, which the second pass rightly put with the personal pronouns.

### What it found in Genesis 16

One disagreement over 355 words. At 16:14, Φρέαρ οὗ ἐνώπιον εἶδον, the second pass read οὗ as the
relative, *the well of him whom I saw*; the first read the adverb, *the well where I saw face to
face*, since the name repeats Hagar's ἐνώπιον εἶδον of 16:13, and that reading was kept.

### What it found in Genesis 17

Nothing: the two passes agreed on all 583 words, once the elision mark was written U+02BC in
both, as the brief asks.

### What it found in Genesis 18

Seven disagreements over 649 words. The second pass was right that the second Σαρρα at 18:11 is
the nominative subject of ἐξέλιπεν — Genesis marks her dative with the article, τῇ Σαρρα (18:14) —
and that πρεσβύτερος carries degree `C`; the lemma stays πρεσβύτερος, as MorphGNT files it. The
first pass's Μαμβρη at 18:1 stays the place, `GS--`, as at 13:18; μέν and ἆρα stay `C-`, as MorphGNT
mostly has them; and μή before συναπολέσῃς at 18:23 stays `D-`.

### What it found in Genesis 19

Twelve disagreements over 910 words. The second pass was right that τὰ κακά at 19:19 is the
nominative subject of καταλάβῃ, with με its object; that καί at 19:21, ἐθαύμασά σου τὸ πρόσωπον καὶ
ἐπὶ τῷ ῥήματι τούτῳ, is *also*, `D-`; and that ἀποθνήσκω keeps the spelling of the other chapters. The
first pass's πλατεῖα stays MorphGNT's lemma, not πλατύς; πρεσβύτερος stays filed under itself, as
settled at 18:11; adverbial μόνον stays `A- ----ASN- μόνος`, as MorphGNT has it at Matt 8:8; and μή at
19:9 stays `D-`. εἰσεσπάσαντο is filed under LSJ's εἰσσπάομαι, as neither pass had it.

### What it found in Genesis 20

One disagreement over 426 words. The second pass tagged Ἄρα at 20:11 a particle, `X-`; the first
kept it with the conjunctions, `C-`, as MorphGNT files ἄρα forty-six times in forty-nine.

### What it found in Genesis 21

Three disagreements over 662 words, with the plural ἀμφότεροι settled beforehand as ἀμφότερος, the
singular Middle Liddell heads. The first pass kept πρωΐ with the diaeresis Rahlfs prints, not πρωί;
Φαραν after τῇ ἐρήμῳ τῇ as the genitive `GS--`, the desert of Pharan, as at 14:6; and θεός in lower
case at 21:33, where Rahlfs capitalises the name called upon, as the brief's rule for speech has it.

### What it found in Genesis 22

Two disagreements over 543 words. The first pass kept πρωΐ with the diaeresis Rahlfs prints, and
filed ἐπέσαξεν under ἐπισάττω, the Attic spelling Middle Liddell heads, not ἐπισάσσω.

### What it found in Genesis 23

Seven disagreements over 427 words. The second pass filed ἀπεκρίθησαν, ἀποκριθείς and ἀπεκρίθη
under ἀποκρίνω, as Middle Liddell heads them; the first kept ἀποκρίνομαι, as MorphGNT files them and as
18:9 settled, and the brief's list of middle verbs now names it. The second filed διπλοῦν and διπλῷ
under the uncontracted διπλόος; the first kept MorphGNT's διπλοῦς. And the second coded κύκλῳ as the
dative of κύκλος; the first kept the adverb, `D- κύκλῳ`, as MorphGNT has it at Mark 3:34.

### What it found in Genesis 24

Nineteen disagreements over 1539 words. The second pass was right that ἔξω τῆς πόλεως at 24:11
governs a genitive, `P-`; that the speech-opening Καί at 24:19 is *also*, `D-`; that ὅσα at 24:36,
ὅσα ἦν αὐτῷ, is the nominative subject of ἦν, as settled at 12:20; and that ἀντειπεῖν goes under
ἀντιλέγω, as MorphGNT files it (Luke 21:15). The first pass kept πρεσβύτερος under itself, μήποτε with
the conjunctions, as MorphGNT has it 22 times in 25, and adverbial μόνον as `A- μόνος`, all as settled
before; ἀποκριθείς under ἀποκρίνομαι; χρυσοῦς and ἀργυροῦς, MorphGNT's contracted forms, as διπλοῦς
at 23:9, not Middle Liddell's χρύσεος and ἀργύρεος; and ὁ θεός in address at 24:12 and 24:42 in the
nominative its form has, as MorphGNT codes Ὁ θεός at Luke 18:13 and Heb 1:8. The brief now names each.

### What it found in Genesis 25

Nine disagreements over 624 words. The second pass was right that ζῶντος at 25:6 is masculine, with
Abraham; that ὀνόματα at 25:13 and 25:16 and τὸ ὄνομα at 25:30 are nominative, the subjects of verbless
clauses and of ἐκλήθη; that ὡσεί at 25:25 is the conjunction; that πυρράκης is LSJ's masculine noun,
not an adjective; and that ἐπειλημμένη goes under ἐπιλαμβάνομαι, as MorphGNT files the middle. The
first pass kept διπλοῦς, as settled at 23:9. Two things neither pass had: ἐπειλημμένη is voice `E`,
the perfect having one form for middle and passive, and ἄγροικος takes gender `C`, being a
two-termination adjective, as ἄπλαστος beside it does. The second pass's file was written first and
read here only after the first was complete, except for its opening line, which was seen in passing:
Προσθέμενος, the aorist middle participle of προστίθημι, on which both passes agreed.

### What it found in Genesis 26

Twenty disagreements over 751 words, and four of them my own mis-numbering of a verse's words. The
second pass was right that πάντα τὰ φρέατα at 26:15 is the hanging nominative, resumed by αὐτά, where
the φρέατα of 26:18 is the object; that καί at 26:21 is *also*; that ἐκείνου and αὐτοῦ of the well
are neuter; and that the well-names Ἀδικία, Ἐχθρία, Εὐρυχωρία, Ὅρκος and Φρέαρ keep the capital
Rahlfs prints, as the brief's rule for a Greek word used as a name has it, and that Ευαῖος keeps the
breathing he leaves off. The first pass kept γέ, MorphGNT's accented enclitic, as settled at 18:13.
GEN 10:19's Γεραρα, coded as an indeclinable singular, was brought into line with the neuter plural
settled at 20:1.

### What it found in Genesis 27

Eight disagreements over 1039 words. The second pass was right that Τί τοῦτο at 27:20 and τὸ ὄνομα at
27:36 are nominative, the subjects of a verbless clause and of ἐκλήθη; that καί at 27:31 is *also*;
and that ποιήσω at 27:37 is the deliberative aorist subjunctive, as ἀποστρέψω at 24:5. The first pass
kept adverbial μόνον as `A- μόνος` and μέν with the conjunctions, both as settled before.

### What it found in Genesis 28

No disagreements at all over 527 words — the first Genesis chapter where the two passes matched at
every word. The second pass recorded ten decisions, all of them the first pass's: προσκαλέω and κοιμάω
filed under their actives; ἔδυ a root aorist under δύω, not δύνω; Χανααν without gender, as the land;
ἐστηριγμένη and ἐπεστήρικτο medio-passive perfect and pluperfect; exclamatory Ὡς as D-, since the C-
rule covers *as, like* only; ἄκρον the noun; ἐπέχεεν aorist, not imperfect; ἀποστρέψω and ἀποδεκατώσω
futures, not aorist subjunctives, as main-clause verbs; and βορρᾶν under the contracted βορρᾶς.

### What it found in Genesis 29

Eleven disagreements over 733 words. The second pass was right that φρέαρ at 29:2 is nominative after
ἰδού, that τὰ κτήνη at 29:7 is the accusative subject of συναχθῆναι, that Τί τοῦτο at 29:25 is accusative
as at 12:18, that δεύτερον at 29:33 is masculine with υἱόν, that καί at 29:27 and 29:33 is *also*, and
that δωρεάν is lemmatized as the adverb itself, the lexicon's filing being handled by `SPELLING`. The
first pass kept πρεσβύτερος, the comparative Middle Liddell heads, where the second pass had πρέσβυς.
Two were settled by neither: ἐργᾷ at 29:27 is the future middle, as the corpus already has it at 4:12
and the module agrees; and Ιουδα at 29:35 the module files as the indeclinable Ἰουδά, not the declined
Ἰούδας the second pass proposed.

### What it found in Genesis 30

Twenty-one disagreements over 915 words, and most of them the first pass's: Βαλλα is the nominative
feminine of Rachel's slave-girl, not a genitive masculine; Ρουβην at 30:14 is the subject; καί at 30:15
is *also*; καλόν at 30:20 agrees with the accusative δῶρον; ἕτερον at 30:24 with υἱόν; τὰ παιδία at
30:26 is the object of ἀπόδος; ἐάν after the relative at 30:33 is the particle, as at 28:15; τριῶν at
30:36 is common gender, as τρεῖς at 29:34; τῶν ῥάβδων at 30:38 is feminine; πᾶν at 30:40 is accusative;
and the four names Γάδ, Ἀσήρ, Ἰσσαχάρ and Ζαβουλών take the accents MorphGNT gives them, as Ῥαχήλ does.
The first pass kept θυμόω and δωρέω under the actives Middle Liddell heads, the deliberative ποιήσω of
27:37, καρύινος as Rahlfs spells it, and κάμηλος feminine, as the corpus has had it since GEN 24.

### What it found in Genesis 31

Seventeen disagreements over 1233 words. The second pass was right about ὄρος throughout — the article
before it is neuter, not masculine, at 31:23, 31:25 and 31:54 — and right that τὰ πρόβατα at 31:10 is the
subject of ἐνεκίσσων, that καί at 31:6 and 31:33 is *also*, that ἓξ ἔτη at 31:41 is the accusative of
duration, that Ιακωβ at 31:48 is the dative after εἶπεν, and that ἐάν at 31:52 is the conjunction, not the
particle after a relative. The first pass kept ἀποκρίνω, περιποιέω and διατίθημι under the actives Middle
Liddell heads, and Γαλααδ in the dative at 31:23, where the second article makes it agree with ὄρει.

### What it found in Genesis 32

Thirty disagreements over 715 words, and the second pass carried most of them: ποιεῖτε at 32:17 is the
imperative beside προπορεύεσθε, ἐρωτᾷ at 32:18 the subjunctive after ἐάν, Ιακωβ at 32:19, 32:26 and 32:33
the genitive after παιδός and μηροῦ, πᾶσι at 32:20 masculine with the servants, πρόσωπόν at 32:21 the
object of προσδέξεται, τὰ δῶρα at 32:22 the subject of παρεπορεύοντο, and τὸ πλάτος at 32:26, τὸ Εἶδος at
32:32 and ὅ at 32:33 the subjects of the intransitive ἐνάρκησεν and παρῆλθεν. The first pass kept the
nominative in address at 32:10, which the brief settles; φοβέομαι, ἅπτω, σῴζω and πρωΐ as the corpus and
Middle Liddell have them; βοῦς feminine; ἰδού as X-; and Εἶδος accusative in apposition to τὸ ὄνομα at
32:31, where the same word is the subject at 32:32.

### What it found in Genesis 33

Four disagreements over 413 words, and none of them changed the file: ἰδού stays X- as the corpus has
tagged it since GEN 1, βοῦς stays masculine as at 30:43, ἑαυτῷ stays RP, and Σικιμων takes the neuter
plural gender the second pass gave it, since the name is declined Greek and not an indeclinable. The
module's own reading settled seven places where the first pass had the wrong case: Ιωσηφ at 33:7, τὰς
εὐλογίας at 33:11, οἰκίας at 33:17, Συχεμ at 33:19, and Σηιρ and Σαλημ after εἰς.

### What it found in Genesis 34

Twenty-one disagreements over 704 words. The second pass was right about seven of them and they
were taken: ὑπάρχοντα is nominative, not accusative; ἀρσενικόν is accusative at 34:15, 34:22 and
34:25, where 17:10 had it nominative; and ὅσα is the subject of ἦν four times over, at 34:28 and
34:29. The rest went to the corpus — καί stays C- where the second pass read it adverbially, μόνον
stays the neuter adjective as MorphGNT files it, ὅτε stays C-, βόας stays feminine as at 18:7, and
κατανύσσω keeps the active form LSJ heads. The module's own reading then settled twelve more: the
imperatives at 34:9 and 34:10, τὴν παῖδα feminine at 34:12, ἐν τούτῳ neuter three times, and τῶν
ἐγχωρίων masculine at 34:1.

### What it found in Genesis 35

Seventeen disagreements over 592 words, and the second pass was right about thirteen. It caught
five names left accusative from an earlier chapter where this one has them nominative — Ισσαχαρ and
Ζαβουλων at 35:23, Νεφθαλι at 35:25, Γαδ and Ασηρ at 35:26 — and ἔτη ἑκατὸν ὀγδοήκοντα at 35:28,
which is the predicate of ἐγένοντο, as 25:7 and 25:17 already had it. It was right too that Βαιθηλ
is accusative after the active ἐκάλεσεν at 35:7 and 35:15, where the corpus has the nominative only
after the passive (11:9, 17:15), and accusative with τὸν τόπον at 35:1, as Συχεμ is genitive with
τοῦ τόπου at 12:6; and that αὐτῶν at 35:5 is masculine, of the men and not the cities. Three of its
lemma corrections came from the brief's own list of names the New Testament accents: Βενιαμίν,
Βηθλέεμ and Ἰούδας. The four that went the other way were διασῴζω, which keeps the iota subscript
the text prints, and the three Βαιθηλ readings the module then settled.

### What it found in Genesis 36

Forty-nine disagreements over 677 words, which came to five questions (the GEN 36 commit has
them in full). The second pass was right about the largest: `ἡγεμὼν Θαιμαν` is apposition, not
a genitive, and thirty words turned on it. Κόρε, Ζάρα, Σαούλ and Χαρράν took MorphGNT's accented
forms. The first pass kept the masculine of Ισραηλ, Μαδιαμ and Εδωμ as a people, which GEN 14:7
had settled.

### What it found in Genesis 37

Five disagreements over 769 words, and the second pass was right four times. Μή opening the
brothers' question at 37:8 is `X-`, as this brief says and GEN 18:17 and 30:2 have it. στακτῆς
is the adjective στακτός used as a noun, the only way either lexicon files it. Two went past the
chapter. ὀσφύς is the lemma at 37:34 and at 35:11, whose note had claimed the circumflex was
MorphGNT's; MorphGNT gives ὀσφύς all eight times, as Middle Liddell does. And γε follows this
brief's rule for enclitics at 18:13 and 26:9 too, where the corpus had taken MorphGNT's γέ over
the lexicon's key. It was wrong once: the interrogative ἆρα, which the brief did not cover, is
`C-` as GEN 18:13 and MorphGNT have it, and the brief now says so.

### What it found in Genesis 38

Two disagreements over 671 words, and both came from rules the brief had recorded only among
its findings and never among its instructions: μέν is `C-`, as settled at GEN 18 and as MorphGNT
codes it 156 times of 178, and χήρα is `A-`, as MorphGNT codes it all 26 times. Both are in the
instructions now. The first pass also took two points from the corpus that the brief does not
state: πρωτότοκος is two-termination, gender `C`, and τῇδε at 38:27 is ὅδε, `RD ----DSF-`.

### What it found in Genesis 39

One disagreement over 567 words, and it is the Greek's own: λαβὼν ὁ κύριος Ιωσηφ ἐνέβαλεν
αὐτόν at 39:20. The second pass read the indeclinable name as genitive, *the lord of Joseph*,
the way an anarthrous name after an articular noun reads nearly everywhere in Genesis; the
first pass and the module read it as the object of λαβών, which has no other. Both are Greek.
The accusative stands, because the participle wants an object and ὁ κύριος is complete without
one (39:16 has it bare), and the verse's notes give both readings. Not a rule, so nothing in
the instructions changes.

The module then found two things both passes had missed alike, so the diff could not. ἐπεσπάσατο
goes under ἐπισπάομαι, as MorphGNT files its middle, and that is now in the instructions. And
ὑπεξῄρηται at 39:9 is read as middle — *to put aside, except*, which Middle Liddell gives only in
the middle — so οὐδέν after it is its object, `----ASN-`, not its subject.

### What it found in Genesis 40

Four disagreements over 478 words, all one word: κανᾶ, κανῷ, κανοῦ, which the second pass filed
under κάνεον, the headword LSJ gives them, and the first under κανοῦν, the contracted form the
text prints. The dictionary form keeps the text's spelling, and the instructions now name it.

### What it found in Genesis 41

Twelve disagreements over 1,140 words, and the second pass had eleven of them right. The first
had taken κοιλίας twice for the genitive singular where τὰς shows the accusative plural, read μή
opening a question as `D-` and ἕως before a finite verb as `P-`, filed ἄχει under LSJ's other
spelling, ἄχι, and Ἡλίου under the common noun of 15:12, where the brief files a Greek word the
text capitalises as printed. At 41:32 it took Φαραω for the genitive of 41:25, Pharaoh's dream,
where the Hebrew's ʾel-parʿōh makes it the dative; at 41:51 it took πάντων τῶν for neuter beside
the masculine πόνων. The one it kept is ξυράω, which the second pass filed as ξυρέω, LSJ's
headword: ἐξύρησαν is both, and MorphGNT files the verb ξυράω. The instructions now name it, and
ἕως before a finite verb.

### What it found in Genesis 42

Seven disagreements over 802 words. The second pass had three right: ἥκατε, twice, is the perfect
ἧκα, as MorphGNT codes ἥκασιν at Mark 8:3, and not the present the brief's ἥκω rule meant; and
ἐμπορεύεσθε at 42:34, after the futures ἀποδώσω and γνώσομαι, is the indicative. The first had the
other four. πρίασθαι and πρίασθε go under πρίαμαι, the key Middle Liddell gives them. The αὐτοῦ
of τὸ αἷμα αὐτοῦ, after τὸ παιδάριον, is masculine: MorphGNT codes αὐτοῦ after τὸ παιδίον as `GSM`
at Matt 2:11 and 2:13, the passage the second pass cited for the neuter. The instructions now
name all three.

### What it found in Genesis 43

Three disagreements over 795 words. The second pass had στακτήν right: it is the adjective
στακτός used as a noun, `A-`, as at 37:25, where the first had made a noun of it. The first had
the other two. μήποτε at 43:12, μήποτε ἀγνόημά ἐστιν, is *perhaps*, not *lest*, and MorphGNT tags
that μήποτε `X-` all three times it has it (Luke 3:15, John 7:26, 2 Tim 2:25), where the second
pass had `D-`. πρεσβύτερος stays filed under itself, the fourth time the second pass has put it
under πρέσβυς. The instructions now name both.

### What it found in Genesis 44

Four disagreements over 761 words, and the second pass had three of them right. τὸ πρωὶ διέφαυσεν
makes a noun of the adverb as the subject of the verb, the morning dawned, so τό is nominative, where
the first pass had carried over the accusative of ὤρθρισεν … τὸ πρωί; τί in Τί ὅτι is the accusative
the brief already names; and ἐθυμώθη's subjunctive θυμωθῇς goes under θυμόομαι, as the brief has it.
The first kept ἐκκρέμαται under ἐκκρέμαμαι, as MorphGNT files ἐξεκρέματο (Luke 19:48), where the
second had the active ἐκκρεμάννυμι; Middle Liddell prints ἐκκρέμαμαι inside that entry. One more
the comparison passed over: the second pass gave θηριόβρωτος, a two-termination adjective, the
masculine/feminine gender `C`, and the first had `M`. `morph_diff.py` does not count `C` against
`M` or `F`, so read gender `C` by hand. The instructions now name the article before an adverb and
ἐκκρέμαμαι.

### What it found in Genesis 45

Six disagreements over 614 words. The second pass was right that εἴπατε at 45:9, καὶ εἴπατε αὐτῷ,
is the imperative after ἀνάβητε. The first had the other five: τοῦτο γὰρ δεύτερον ἔτος at 45:6 and
πέντε ἔτη at 45:11 are accusatives of time, as MorphGNT codes τοῦτο τρίτον (John 21:14, 2 Cor 13:1)
and ἔτη of duration, where the second pass had made verbless clauses of both. Both passes read the
λοιπὰ πέντε ἔτη of 45:6 as nominative. The instructions now name the accusative of time.

### What it found in Genesis 46

No disagreements over 668 words, most of them names. One difference the comparison passes over,
and the second pass had it right: πλείονι, the comparative of πολύς, takes gender `C`, `----DSCC`,
as the corpus codes μείζων and ἐλάσσων, where the first pass had `M`.

### What it found in Genesis 47

Seven disagreements over 852 words. Two went to the second pass: σπείρωμεν at 47:19, which is
present and aorist subjunctive alike, is the aorist, one sowing of the seed asked for, as σπείρατε
at 47:23; and the first Φαραω of 47:22 is the subject of ἔδωκεν, nominative, as in ἣν ἔδωκεν αὐτοῖς
Φαραω after it, where the first pass had read *the priests of Pharaoh*. The rest went to the
corpus: adverbial μόνον stays `A- μόνος`, where the second pass has had it `D-` before, and ἄκρον
is the noun, as at 28:18 and in MorphGNT's own ἀπʼ ἄκρων … ἕως τῶν ἄκρων (Matt 24:31). Both are
now in the brief.

### What it found in Genesis 48

Ten disagreements over 564 words. Six went to the second pass:
- ἐάν after a relative, `ἃ ἐὰν γεννήσῃς`, is `X-`, as the corpus has it eight times in nine;
- τοῦ before γήρους and before προσώπου is neuter, with its noun;
- καί is the adverb, *also*, three times: καὶ τὸ σπέρμα σου at 48:11, and both καὶ οὗτος at 48:19,
  for the Hebrew gam;
- Εφραθα after τοῦ ἐλθεῖν is the accusative of destination.

The first pass kept ἔκγονα under ἔκγονον, as MorphGNT files it at 1 Tim 5:4; Βαιθλεεμ under
Βηθλέεμ, as at 35:19; and Σικιμα at 48:22 as a singular, `----AS--`, since ἐξαίρετον and ἥν with it
are singular, where the second pass had the neuter plural the name takes elsewhere.

### What it found in Genesis 49

Five disagreements over 569 words, and the second pass was right on all five: Ιουδα at 49:9 is the
vocative, since the declined name's nominative is Ιουδας and the verse goes on in the second person;
ἕως before ἄν is the conjunction, `C-`, as the corpus has it; and the three articles of ἐν τῷ σπηλαίῳ
τῷ διπλῷ τῷ ἀπέναντι are neuter. One more the comparison passes over: πίων takes gender `C`,
Middle Liddell's *ὁ, ἡ*, at 49:20 as at 49:15.

### What it found in Genesis 50

Two disagreements over 560 words, and the second pass was right on both: the second Πένθος of 50:11
is accusative after the active ἐκάλεσεν τὸ ὄνομα, as Φρέαρ at 21:31, where the corpus had taken the
nominative of 35:8's Βάλανος for the pattern (Βάλανος shows its case; a neuter does not); and θνήσκω
takes no iota subscript, since Perseus keys it `qnh/skw`, as the brief already says of ἀποθνήσκω.

### What it found in Exodus 1

Ten disagreements over 373 words; the second pass was right on nine. ἅμα with a dative is a
preposition, `P-`, as at GEN 14:5; τῶν Εβραίων at 1:15 is masculine, the people, beside τῶν
Αἰγυπτίων; Φουα is a woman; μαιοῦσθε after ὅταν is the subjunctive, Koine spelling the -όω
subjunctive with ου; Τί ὅτι takes τί as accusative, as GEN 18:13; ἐάν after a relative is the
particle, `X-`; and πᾶν θῆλυ at 1:22, taken up by αὐτό, is a hanging nominative. The first pass's
περιποιέω stands against the second's περιποιέομαι: the verb has an active in use, and is not on the
brief's list of middle-only verbs.

### What it found in Exodus 2

Nine disagreements over 561 words, and the second pass was right on all nine: τὸ ἀποβησόμενον is the
subject of the verbless question at 2:4, nominative; τοῦ παιδίου and τοῦ ὕδατος take neuter
articles; μή opening a question that expects no is `X-`, as MorphGNT tags it 57 times; and αὐτῶν at
2:16–18, of the seven daughters, is feminine.

### What it found in Exodus 3

No disagreements over 595 words. The second pass reached the same readings of λῦσαι (aorist middle
imperative, not the infinitive), ὅσα (nominative, the subject in its own clause), γείτονος
(feminine, a woman's neighbour) and προσκέκληται (προσκαλέω, Middle Liddell's headword, with voice
`E` in the perfect).

### What it found in Exodus 4

Two disagreements over 746 words, both of lemma, and the first pass stands on both: προχειρίζω
and θυμόω are Middle Liddell's headwords, with the deponent or passive inside the entry, and neither
is on the brief's list of verbs filed under the middle. MorphGNT files προχειρίζομαι and θυμόομαι;
the module too.

### What it found in Exodus 5

Three disagreements over 472 words. Two went to the second pass: τὸν Ισραηλ at 5:2 is accusative,
the object of ἐξαποστέλλω, where the first pass had the genitive; and καί in καθάπερ καὶ ὅτε at 5:13
is the adverb, *also*, as at GEN 41:21. The first pass stands on προσκαλέω, the corpus's lemma at
EXO 3:18 and GEN 28:1, where the second filed the middle προσκαλέομαι as MorphGNT does.

### What it found in Exodus 6

Two disagreements over 565 words, most of them names, and the second pass was right on both: καί in
ἐν ᾗ καὶ παρῴκησαν (6:4) is the adverb, *also*; and Αβιουδ takes MorphGNT's Ἀβιούδ (Matt 1:13),
the same letters, as the brief's rule for names has it. Both passes filed διαλεγόμενοι under
Middle Liddell's διαλέγω, read συγγενείας after κατά as the accusative plural, and gave the
numerals of a verbless lifespan the nominative.

### What it found in Exodus 7

Six disagreements over 697 words, and the second pass was right on four: ἐπαοιδοί is an adjective
used as a noun, `A-`, under the brief's rule; νοῦν goes under νόος, the uncontracted headword, as
ὀστέον does; οὐδέ in οὐδὲ ἐπὶ τούτῳ is *not even*, `D-`; and κύκλῳ with a genitive after it is the
preposition, `P-`, as MorphGNT codes it in Revelation — GEN 35:5 and 41:48 were corrected with it,
and the rule above now names both uses. The first pass stands on τριῶν, gender `C` as the brief has
τρεῖς, though its noun here is neuter.

### What it found in Exodus 8

One disagreement over 730 words, and the first pass stands: ἐπαοιδοί, which the second pass tagged
`N-`, is an adjective used as a noun and stays `A-`, as the brief's rule has it and as Exodus 7
settled. Both passes read ἐμοῦ and σοῦ between the article and its noun as the possessives.

### What it found in Exodus 9

Seven disagreements over 823 words, and the second pass was right on five: βουσίν is masculine,
MorphGNT's usual gender for βοῦς; καμιναίας is the noun καμιναία, *furnace*, which LSJ cites from
9:10, and not the adjective; τοιαύτη is `RD`, as MorphGNT tags τοιοῦτος and as the corpus already
had it; ἔθνος in ἀφʼ οὗ γεγένηται ἐπʼ αὐτῆς ἔθνος is the subject; and πυρός, *wheat*, which the
first pass's seed had read as πῦρ.

### What it found in Exodus 10

Four disagreements over 730 words. The second pass was right on three: τίνος in ἕως τίνος, at
10:3 and 10:7, is masculine, χρόνου understood, as MorphGNT reads οὗ in ἕως οὗ; and τὸ πρωί at 10:13 is the subject
of ἐγενήθη, nominative. φῶς stays under φάος, the uncontracted form Middle Liddell heads, as νοῦς
under νόος.

### What it found in Exodus 11

One disagreement over 262 words, and the second pass was right: Φαραω at 11:9 is the subject of
εἰσακούσεται, nominative. Both passes read οὗ σὺ ἀφηγῇ as the relative with ἀφηγέομαι's genitive,
not the adverb, and πρωτοτόκου as neuter with πᾶν πρωτότοκον.

### What it found in Exodus 12

Thirteen disagreements over 1,103 words, and the second pass was right on nine: five αὐτοῦ in 12:43–48
and τοῦ πασχα are neuter, for the πασχα; Ααρων after πρός at 12:43 is accusative; πλήν at 12:16 has no
genitive after it and is the conjunction; and ἐναρχομένου at 12:18 takes the month for its subject,
masculine. The first pass kept ὀσφύς as the corpus has it, μόνον agreeing with τοῦτο, δέσμη as LSJ
heads it, and μισθωτός as an adjective used as a noun.

### What it found in Exodus 13

Three disagreements over 502 words. The second pass was right that μεταμελήσῃ files under μεταμέλει,
Middle Liddell's impersonal headword. ὄνου stays feminine, the she-ass whose womb opens, and
πρωτοτόκων at 13:15 neuter, as πρωτοτόκων κτηνῶν beside it and as at 11:5 and 12:29.

### What it found in Exodus 14

Two disagreements over 786 words, and the second pass was right on both: Μαγδώλου is feminine, a town
in -ος as Αἴγυπτος is, and 14:19's ἐξῆρεν δὲ καί is the adverb, *also*, as GEN 19:35 ἐπότισαν δὲ καί.

## The brief

Copy everything below the rule into a new agent. Replace `<BOOK NAME>`, `<CHAPTER>`,
`<OUTPUT PATH>`, `<WORD COUNTS>`, `<TOTAL>` and `<THE TEXT>`.

---

You are doing an independent morphological analysis of Septuagint <BOOK NAME> <CHAPTER>
(Rahlfs 1935) — every word: its part of speech, parse, and dictionary form. Another analysis
of the same text already exists; yours will be diffed against it to find errors in either.
Your value comes entirely from being independent, so the rules about what not to open matter.

## Do not open or read

- anything under `data/`, `reference/`, `site/` or `sources/`
- anything the environment variable `LXX_RAHLFS_DIR` points at
- do not run anything in `build/`, and do not search the web for a parsed Septuagint

Work from your own knowledge of Greek grammar and the conventions below. The format examples
here are all you need.

## Output

Write the analysis to `<OUTPUT PATH>`, UTF-8, LF line endings. One line per word, in text
order, five space-separated columns:

    verse pos parse form lemma

e.g. `2:1 V- 3API-P-- συνετελέσθησαν συντελέω`. No header, no comments, no blank lines. Copy
each form exactly as the text prints it with punctuation (`. , · ; : — ( )`) removed; keep accents
as printed (a grave stays grave), keep capitals, and keep the elision mark ʼ (U+02BC).

Words per verse: <WORD COUNTS>. There must be <TOTAL> lines. Check your counts before
finishing.

## Part of speech (column 2)

N- noun · V- verb · A- adjective (numerals included) · RA article · RP personal pronoun
(αὐτός, the reflexives ἑαυτοῦ, σεαυτοῦ, ἐμαυτοῦ, and the reciprocal ἀλλήλων included) · RD demonstrative · RR relative pronoun
(ὅσος included) · RI interrogative (the indefinite τις included) · P- preposition · C- conjunction · D- adverb · X- particle · I- interjection

Small words are tagged as MorphGNT tags them:

- **C-** καί, δέ, γάρ, ὅτι, τε, ἵνα, οὖν, ἡνίκα, καθά, καθώς, καθάπερ, ὥστε, ὅπως (with ἄν `X-`); εἰ, *if* or *whether*; πλήν
  with no genitive after it, *only, except*; ἐάν meaning *if*; ὅτε introducing a clause, including
  after a noun that is not a time (`ἡ μαρτυρία … ὅτε`, John 1:19); οὐδέ meaning *nor*; μήποτε
  meaning *lest*; ὡς meaning *as, like*, and the ὡς of `ὡς ἄν` (Rom 15:24), with ἄν `X-`; ὅθεν
  meaning *wherefore* (Heb 2:17); ἕως before an infinitive with no article (`ἕως ἐλθεῖν`), which
  has no genitive to govern, and ἕως opening a clause with a finite verb (`ἕως οὐκ ἠδύναντο`)
- **X-** also ἴδε, *behold*, as MorphGNT tags it. But ἰδέ, accented on the last syllable as Rahlfs
  prints it at `ἰδὲ ἀπὸ τοῦ τόπου`, is the aorist imperative of ὁράω, `V- 2AAD-S--`
- **X-** ἄν; ἐάν where it stands for ἄν after a relative (`ὃ ἐὰν θέλητε`, John 15:7); ἰδού;
  μή opening a question that expects *no*; μήποτε meaning *perhaps* (`μήποτε ἀληθῶς ἔγνωσαν`,
  John 7:26)
- **A-** εὐθύς meaning *immediately*, `A- ----NSM-`, as MorphGNT codes it all 51 times; χήρα, *widow*, `A-` under χήρα, as MorphGNT codes it all 26 times
- **D-** αὐτοῦ meaning *here*, under the lemma αὐτοῦ, as MorphGNT has it (Matt 26:36); κύκλῳ, *round
  about*, under κύκλῳ (Mark 3:34), but `P-` with a genitive after it, as MorphGNT codes κύκλῳ τοῦ
  θρόνου (Rev 4:6); πρωΐ, filed as
  πρωΐ
- **C-** ἄρα, *then, perhaps*, as MorphGNT codes it 46 times of 49; and the interrogative ἆρα,
  as MorphGNT codes it twice of three (Acts 8:30, Gal 2:17); and μέν, as MorphGNT codes it 156 times of 178
- **D-** οὐ, μή, νῦν, τότε, εὖ, ἅμα with no dative after it, ἔτι, ἐκεῖ, ἐκεῖθεν, ποῦ, δεῦτε; καί meaning *also, even*, and the καί of
  `καὶ γάρ` (all 38 times in MorphGNT); ὅθεν meaning *from where* (Matt 12:44); οὐδέ meaning *not
  even*; ὅτε after a noun of time (`ἔρχεται ὥρα ὅτε`, John 4:21); οὗ meaning *where* (οὗ meaning
  *whose, of which* is the relative, `RR`); ἐπάνω, ἔξωθεν and ἔξω with no genitive after them
  (1 Cor 15:6); πλησίον, *near*, even after the article, *the neighbour* (`τὸν πλησίον`, Matt
  19:19), where the article takes the case and gender of the person meant
- **P-** ἀντί; ἅμα with a dative (`ἅμα αὐτοῖς`, Matt 13:29); a word governing a genitive as a preposition does — ἐπάνω, ἀπέναντι, ἀνά, ἐναντίον,
  ἐνώπιον, ὑποκάτω, ὀπίσω, ἕνεκεν (filed under ἕνεκα), and ἔξωθεν with a genitive (Mark 7:15) — and ἕως
  governing a genitive, an articular infinitive included

## Parse (column 3) — exactly 8 characters

Positions: person, tense, voice, mood, case, number, gender, degree. Use `-` where a position
does not apply.

- person `1 2 3` · tense `P` present `I` imperfect `F` future `A` aorist `X` perfect `Y`
  pluperfect · voice `A` active `M` middle `P` passive `E` middle/passive · mood `I`
  indicative `S` subjunctive `O` optative `D` imperative `N` infinitive `P` participle · case
  `N G D A V` · number `S P D` · gender `M F N C` · degree `C` comparative `S` superlative

Shape by type:

- finite verb: person, tense, voice, mood, number — no case, no gender. `3AAI-S--`
- infinitive: tense, voice, mood N — nothing else. `-AAN----`
- participle: tense, voice, mood P, **and** case, number, gender. `-PAPNSM-`
- noun: case and number, and gender (see indeclinables). `----NSF-`
- article, adjective, demonstrative, relative: case, number, gender. `----DSM-`
- personal pronoun, interrogative: case and number, and gender where the form has one
  (μου has none: `----GS--`)
- preposition, conjunction, adverb, particle: `--------`

Conventions:

- **Voice E** only in the tenses where middle and passive share one form — present,
  imperfect, perfect, pluperfect — deponents included. Aorist and future distinguish the two,
  so use M or P there, by the form: a deponent's aorist in -θη- is `P` (ἐνεθυμήθη `3API-S--`,
  as MorphGNT codes ἐνθυμηθέντος).
- **Gender C** for an adjective whose form does not distinguish masculine from feminine:
  two-termination adjectives (ἀόρατος, πράσινος) and numerals like τέσσαρας and τρεῖς.
- **Indeclinables** take case and number from the syntax, as MorphGNT does, and gender where
  there is one to take: a personal name, from the person (Αδαμ `----DSM-`, a woman's name
  `F`), or a numeral agreeing with its noun (οἱ δύο `----NPM-`, as MorphGNT codes δύο at
  John 1:35). An indeclinable place name has none (Εδεμ `----DS--`). A declinable name keeps
  its gender like any noun — rivers are masculine (Τίγρις, Εὐφράτης), Βαβυλών, Σιδών and Γάζα
  feminine, Σόδομα neuter plural — except where it names a person, who gives it his own: τὸν
  Σιδῶνα, Canaan's first-born, is `----ASM-`.
- A people's name declined in Greek (Χετταῖος, Ἀράδιος, Κίτιοι, οἱ Αἰγύπτιοι) is a noun, `N-`, as
  MorphGNT codes Ἀσσύριος and Κύπριος, though it tags Αἰγύπτιος and Χαναναῖος as adjectives, filed in the nominative singular masculine. A people's name in the Hebrew plural -ιιμ or -ιν (τοὺς Λουδιιμ, Φυλιστιιμ, τοὺς Ραφαϊν)
  is indeclinable, filed as printed, and plural and masculine
  from the people.
- A place name after γῆ with no article of its own (`ἐν τῇ γῇ Σεννααρ`) is genitive, as MorphGNT
  codes `ἐν γῇ Χανάαν` at Acts 13:19.
- An indeclinable common noun takes its gender from the article or adjective beside it.
- An article before an indeclinable name still carries full case, number and gender.
- A name after a repeated article — `τὴν δρῦν τὴν Μαμβρη`, `ἐν τῇ ἐρήμῳ τῇ Φαραν` — is genitive:
  *the oak, the one of Mambre*.
- An adjective used as a noun stays `A-`: ἡ ξηρά, *the dry land*, is `A- ----NSF- ξηρός`, as
  MorphGNT codes it, and so is ἡ ἔρημος, *the desert*, `A- ----DSF- ἔρημος` all 23 times in
  MorphGNT; so are ἡ περίχωρος, *the country round about*, and τὸ πρότερον, *before*,
  `A- ----ASNC πρότερος`, and εἰς ἀριστερά, εἰς δεξιά, neuter plural. δεκάτη, *a tenth*, is `A- ----ASF- δεκάτη`, as MorphGNT codes and files it. στεῖρα, *barren*, is `A-` under its own dictionary form, στεῖρα, as MorphGNT and
  Middle Liddell both file it.
- A demonstrative with an ordinal and no verb of its own, `τοῦτο δεύτερον ἔτος`, is an accusative
  of time, `----ASN-`, as MorphGNT codes τοῦτο τρίτον at John 21:14; so is a span, `πέντε ἔτη`,
  `----APN-`, as MorphGNT codes ἔτη of duration.
- An article before an adverb makes a noun of it and takes the case of its place in the clause:
  `τὸ πρωὶ διέφαυσεν`, *the morning dawned*, τό `RA ----NSN-`; `ὤρθρισεν … τὸ πρωί`, `----ASN-`.
- ἐκκρέμαμαι, *to hang from*, is filed under itself, as MorphGNT files ἐξεκρέματο (Luke 19:48).
- Adverbial μόνον, *only*, is the neuter of the adjective, `A- ----ASN- μόνος`, as MorphGNT files
  ἀλλὰ μόνον εἰπέ (Matt 8:8).
- ἄκρον, *the furthest point, the end*, is the noun, `N- ἄκρον`, also where it stands before
  another genitive: `ἀπʼ ἄκρων ὁρίων … ἕως τῶν ἄκρων`, as MorphGNT codes ἀπʼ ἄκρων οὐρανῶν ἕως
  τῶν ἄκρων αὐτῶν (Matt 24:31).
- πρεσβύτερος, *elder*, is filed under itself with degree `C` (`A- ----NSMC πρεσβύτερος`), as
  MorphGNT files it, and not under πρέσβυς.
- μέσος with a genitive after it — `ἐν μέσῳ τοῦ …`, `ἀνὰ μέσον τοῦ …` — is the neuter
  adjective used as a noun: `A- ----DSN-`, `A- ----ASN-`.
- A word of address is vocative, case `V` — but a declined nominative form used in address stays
  nominative: `Κύριε ὁ θεός`, ὁ and θεός `----NSM-`, as MorphGNT codes Ὁ θεός at Luke 18:13 and Heb 1:8.
- A pronoun standing for a neuter noun that names a person takes the person's gender: αὐτοῦ
  after τὸ παιδίον is `GSM`, as MorphGNT codes it at Matt 2:11 and 2:13.
- A relative takes its case from its own clause: in `ἔδωκεν αὐτῷ ὅσα ἦν αὐτῷ`, ὅσα is the
  nominative subject of ἦν.
- τί in `τί ὅτι`, *why is it that*, is accusative, `RI ----ASN-`, as MorphGNT codes it all
  three times (Luke 2:49; Acts 5:4, 5:9).
- `ἵνα τί`, *why*, printed as two words, is the ellipsis ἵνα τί γένηται: ἵνα `C-`, τί
  `RI ----NSN-`. (MorphGNT prints the pair as one word, ἱνατί, and so cannot guide it.)
- `ὁ δέ`, *and he*, is still the article: `RA ----NSM-`, as MorphGNT codes it. So is an article
  standing before a prepositional phrase, in the case the phrase has in the sentence:
  `τὸ πρὸς ἑσπέραν`, *toward evening*, `RA ----ASN-`. The τοῦ of `ἕως τοῦ νῦν` is `RA ----GSN-`:
  an adverb made a noun takes the neuter article (MorphGNT's `GSM` at Matt 24:21 is not followed).
- Numerals take case, number and gender like any adjective — ἑπτά `A- ----APN-` beside a
  neuter plural — and a multiplicative adverb (ἑπτάκις) is `D-`. A number printed as several
  words (ἑκατὸν καὶ ἑξήκοντα πέντε, δέκα πέντε) is several words: each numeral agrees with the
  noun.
- Comparatives in -ων (μείζων) have one form for masculine and feminine: gender `C`, degree `C`.
  A comparative in -τερος has three: ὁ νεώτερος is `A- ----NSMC`, filed under its positive, νέος,
  as MorphGNT files it. A possessive adjective (ὑμέτερος) is `A-`.
- οἶδα's past forms (ᾔδει) are pluperfect, `Y`, as MorphGNT codes them. ἥκω is present, `P`,
  though it means *have come*; but a form with the perfect's -κα- (ἥκατε, ἥκασιν) is the perfect
  ἧκα, `X`, as MorphGNT codes ἥκασιν at Mark 8:3.
- A repeated distributive numeral (`δύο δύο`, Mark 6:7) is two words, each agreeing with its
  noun.
- Where the form is ambiguous, case, number and gender come from the syntax: neuters in the
  nominative and accusative, verbless clauses, agreement with a noun, a hanging nominative.

## Lemma (column 5)

The dictionary form as Middle Liddell (Perseus) files it:

- Koine spellings: γίνομαι, γινώσκω, and ξυράω, as MorphGNT files ξυρᾶσθαι (1 Cor 11:6), for the
  forms it shares with ξυρέω. No iota subscript where Perseus has none: ἀποθνήσκω.
  Enclitics unaccented, as Middle Liddell keys them: τε, γε (MorphGNT accents γέ; the lexicon
  does not).
- Verbs with no active in use under their middle form, as MorphGNT files them: ἐργάζομαι,
  πορεύομαι, ἐκπορεύομαι, εἰσπορεύομαι, εἰσέρχομαι, ἐντέλλομαι, φοβέομαι, ἀπέρχομαι,
  καταράομαι, ἐκλέγομαι, ἐνθυμέομαι, θυμόομαι (for ἐθυμώθη, as MorphGNT has it at Matt 2:16),
  διανοέομαι, μιμνήσκομαι, διατίθεμαι, χράομαι, κτάομαι, περιποιέομαι, συμπορεύομαι, δύναμαι,
  ἐπισπάομαι (for ἐπεσπάσατο, as MorphGNT has ἐπισπάσθω at 1 Cor 7:18),
  ἀποκρίνομαι (ἀπεκρίθη, ἀποκριθείς, voice `P`). But ἐπεκαλέσατο, the middle,
  goes under the active ἐπικαλέω, as MorphGNT files it.
- πρίασθαι, πρίασθε → πρίαμαι, the key Middle Liddell gives the aorist.
- εἰδέναι → οἶδα · εἶπεν → λέγω · ἀντειπεῖν → ἀντιλέγω · ἰδεῖν → ὁράω · φαγ- forms → ἐσθίω · μου → ἐγώ ·
  every article → ὁ.
- The dictionary form keeps the spelling the text prints — γίνομαι, ἔχθρα, νοσσιά, δειλινός, κανοῦν,
  ἐννακόσιοι, κατάγαιος, τεσσαράκοντα — even where Middle Liddell or MorphGNT spells the word
  otherwise (γίγνομαι, ἔχθρη, νεοσσιά, ἐνακόσιοι, κατάγειος, τεσσεράκοντα). What goes to the
  dictionary is the form, not the spelling: a contracted form goes under the form Middle Liddell
  cites, the uncontracted ὀστέον for ὀστοῦν but the contracted συκῆ, διπλοῦς, χρυσοῦς and ἀργυροῦς; ἕνεκεν → ἕνεκα, εἵνεκεν → εἵνεκα;
  ἀμφότεροι → ἀμφότερος, the singular Middle Liddell heads, not MorphGNT's plural. A neuter
  noun filed as such: πετεινόν.
- Proper names: a name the New Testament also uses, of a person or a place, takes MorphGNT's
  dictionary form, accented though Rahlfs prints it bare, even where the New Testament uses it of
  another bearer (Χανάαν the land, Acts 7:11; Μαγώγ a people, Rev 20:8). So far: Ἀδάμ, Εὕα, Κάϊν,
  Ἅβελ, Σήθ, Ἐνώς, Ἑνώχ, Μαθουσαλά, Λάμεχ, Μαλελεήλ, Νῶε, Σήμ, Χανάαν, Μαγώγ, Ἀρφαξάδ, Σαλά, Ἔβερ,
  Φάλεκ, Ἀράμ, Ῥαγαύ, Σερούχ, Ναχώρ, Θάρα, Λώτ, Χαρράν, Φαραώ, Συχέμ, Μελχισέδεκ, Σαλήμ, Βαλάκ,
  Ἐλιέζερ, Ἁγάρ, Ἀβραάμ, Σάρρα, Ἰσαάκ, Ἰακώβ, Ἠσαῦ, Ἰσραήλ, Ῥαχήλ, Λευί, Ῥουβήν, Συμεών, Ἰσσαχάρ,
  Ζαβουλών, Γάδ, Ἀσήρ, Ἰωσήφ, Βενιαμίν, Ἐφραίμ, Βηθλέεμ, Ἑμμώρ, Μαδιάμ, Κόρε, Ζάρα, Φαρές, Ἤρ, Θαμάρ, Σαούλ, Ἀράμ, and the declined Σιδών, Γάζα, Βαβυλών, Σόδομα, Γόμορρα, Αἴγυπτος, Αἰγύπτιος,
  Χαλδαῖος, Ἰορδάνης, Φερεζαῖος, Δαμασκός, Ῥεβέκκα, Ἰούδας, Μανασσῆς (τὸν Μανασση, as Matt 1:10 τὸν Μανασσῆ), Μεσοποταμία, Συρία, Ἀραβία, Ἑβραῖος and Ἰδουμαία.
  Νεφθαλι is not Νεφθαλίμ, nor Βαλααν Βαλαάμ. Where the New Testament spells the name with other
  letters (Luke 3:36–37 Καϊνάμ, Ἰάρετ), it is not the same dictionary form; a breathing or accent is
  not a letter, so Αβραμ and Σαρα are not Ἀβραάμ and Σάρρα, but Αβρααμ and Σαρρα are.
- Every other Semitic name, of a person or a place, exactly as printed, unaccented (Εδεμ, Φισων,
  Ναιδ), and in the nominative where it is declined. Greek names in the nominative singular
  (Αἰθιοπία, Τίγρις, Ἀσσύριος, Εὐφράτης, Χετταῖος, Ῥόδιος, Σύρος), with the breathing Rahlfs prints or
  leaves off (Αμορραῖος, Ομμαῖος). A Greek word the text prints capitalised as a name keeps its
  capital in the lemma.
- Σόδομα is neuter plural (ἐν Σοδομοις); Γόμορρα is declined either way, and the form decides:
  Γομορρας is the feminine singular, Γομορρα beside Σοδομα in the accusative the neuter plural.
- Any other Semitic word printed unaccented: exactly as printed, like the place names.

## The text

<THE TEXT>

## When you finish

Verify the line count and the per-verse counts. Write at most ten words you found genuinely
ambiguous, with how you decided each, to a file beside your output named as it is with
`.notes.txt` in place of `.txt`. Then reply with the line count only: the other analysis is
written without seeing your notes, and your reply is read before it is. Do not compare your
work against anything.
