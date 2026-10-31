# Source editions

The Greek editions this project reads from. **They are not committed** — everything in this
directory except this file is excluded by [`../.gitignore`](../.gitignore). See
[`../NOTICE.md`](../NOTICE.md) for why.

Fetch them here before running `python build/words.py` or `python build/validate.py`.
Without the SBLGNT the `greek` check cannot run: it reports `SKIP` and the summary says so
explicitly rather than passing quietly. Every other check works without any of this.

## New Testament — SBL Greek New Testament

CC BY 4.0. Free to redistribute with attribution.

```bash
git clone --depth 1 https://github.com/LogosBible/SBLGNT.git sources/sblgnt
```

`validate.py` reads `sources/sblgnt/text/<Book>.txt`, one verse per line as
`John 1:1<TAB><greek>`.

## New Testament morphology — MorphGNT

CC BY-SA 3.0 for the parsing and lemmatization, which may be adapted under CC BY-SA 4.0.
Only the file for each book on the page is needed — for John, about 1 MB:

```bash
curl -sL --create-dirs -o sources/morphgnt/64-Jn-morphgnt.txt https://raw.githubusercontent.com/morphgnt/sblgnt/master/64-Jn-morphgnt.txt
```

`build/words.py` reads it for the word-by-word layer. Until it is present, John's Greek lines
render without that layer.

The second morphology pass settles questions of convention — what part of speech a small word
is, which spelling a lemma takes — by counting what MorphGNT does across the whole New
Testament (see `reference/second-pass-brief.md`), so it is worth fetching every book, about
9 MB in all:

```bash
for f in 61-Mt 62-Mk 63-Lk 64-Jn 65-Ac 66-Ro 67-1Co 68-2Co 69-Ga 70-Eph 71-Php 72-Col 73-1Th 74-2Th 75-1Ti 76-2Ti 77-Tit 78-Phm 79-Heb 80-Jas 81-1Pe 82-2Pe 83-1Jn 84-2Jn 85-3Jn 86-Jud 87-Re; do curl -sL -o sources/morphgnt/$f-morphgnt.txt https://raw.githubusercontent.com/morphgnt/sblgnt/master/$f-morphgnt.txt; done
```

## Lexicon — Middle Liddell, Perseus XML

Liddell and Scott's *Intermediate Greek-English Lexicon* (1889) as the Perseus Digital
Library encoded it — CC BY-SA 3.0 US, adaptable under CC BY-SA 4.0. `build/words.py` reads
each word's senses from it, and the headword rule takes each headword from it.

```bash
curl -sL --create-dirs -o sources/middle-liddell/Perseus_text_1999.04.0058.xml https://raw.githubusercontent.com/blinskey/middle-liddell/master/Perseus_text_1999.04.0058.xml
```

## Lexicon — LSJ, where Middle Liddell has no entry

Liddell–Scott–Jones as [PerseusDL](https://github.com/PerseusDL/lexica) publishes it,
CC BY-SA 4.0. Middle Liddell is an abridgement and drops words the Septuagint uses —
ἀκατασκεύαστος (Gen 1:2), ἁγιάζω (Gen 2:3) — so those senses come from LSJ.

The lexicon is split into 27 files of about 270 MB in total, alphabetically. Fetch only the
files a chapter needs:

```bash
curl -sL --create-dirs -o sources/lsj/grc.lsj.perseus-eng1.xml https://raw.githubusercontent.com/PerseusDL/lexica/master/CTS_XML_TEI/perseus/pdllex/grc/lsj/grc.lsj.perseus-eng1.xml
```

| file | covers | fetched for |
| --- | --- | --- |
| `eng1` | the whole of alpha, `*a` to `ἄωτος` (42 MB) | ἀκατασκεύαστος (Gen 1:2), ἁγιάζω (Gen 2:3), ἀσφαλτόω (Gen 6:14), ἀνάστημα (Gen 7:23), ἁλυκός, ἀποσκευή (Gen 14), ἀορασία (Gen 19:11), ἀπογαλακτίζω, ἀρχιστράτηγος (Gen 21), ἀποσάττω, ἅβρα (Gen 24), ἀρήν (Gen 30:32), αἰχμαλωτίς (Gen 31:26), ἀσφαλτόπισσα (Exod 2:3), ἀνάψυξις (Exod 8:11), ἁγίασμα (Exod 15:17), ἀνυπομόνητος (Exod 18:18), ἀναβαθμίς (Exod 20:26), ἀμνήστευτος (Exod 22:15), ἀνταποθνήσκω (Exod 22:2), ἀναφορεύς (Exod 25:13), ἄσηπτος (Exod 25:5), αὐλαία (Exod 26:1), ἀγκωνίσκος (Exod 26:17), ἄτρυγος (Exod 27:20), ἀσπιδίσκη (Exod 28:13), ἀχάτης (Exod 28:19), ἁλυσιδωτός (Exod 28:22), ἀφαίρεμα (Exod 29:27), ἀφόρισμα (Exod 29:24) |
| `eng2` | beta (5 MB) | βούτυρον (Gen 18:8), βραδύγλωσσος (Exod 4:10), βδελύσσομαι, whose active Exod 5:21 is, βηρύλλιον (Exod 28:20) |
| `eng3` | gamma (4 MB) | γελοιάζω (Gen 19:14), γεώργιον (Gen 26:14), γειώρας (Exod 12:19), γνοφώδης (Exod 19:16), γλυφή (Exod 25:7), γλύμμα (Exod 28:11) |
| `eng4` | delta (15 MB) | διαναπαύω (Gen 5:29), διώροφος (Gen 6:16), διχοτόμημα (Gen 15:11), δίδραχμον (Gen 20:14), δόμα (Gen 25:6), διάλευκος (Gen 30:32), δέσμη (Exod 12:22), διατήρησις (Exod 16:33), δικτυωτός (Exod 27:4), διανήθω (Exod 28:8) |
| `eng12` | lambda (7 MB) | λεπίζω, λέπισμα (Gen 30:37), λιποψυχία, which ὀλιγοψυχία points to (Exod 6:9), λατρευτός and λατρευτικός, which it points to (Exod 12:16), λατομέω (Exod 21:33), λυχνία (Exod 25:31), λιγύριον (Exod 28:19), λιθουργικός (Exod 28:11), λάγανον (Exod 29:2), λουτήρ (Exod 30:18) |
| `eng20` | rho (2 MB) | ῥαντός (Gen 30:32), ῥαφιδευτής (Exod 27:16), ῥοΐσκος (Exod 28:33) |
| `eng5` | epsilon (40 MB) | ἑβδομηκοντάκις (Gen 4:24), εὐαρεστέω (Gen 5:22), ἑξακοσιοστός (Gen 7:11), ἐλαττονόω (Gen 8:3), ἐνισχύω, ἐγγίζω, ἐτασμός (Gen 12), ἑκατονταέτης (Gen 17:17), ἐπαύριον, εἰσσπάομαι (Gen 19), ἐνώτιον (Gen 24:22), ἑκατοστεύω (Gen 26:12), ἐνυπνιάζομαι (Gen 28:12), ἐγκισσάω (Gen 30:38), ἐθισμός (Gen 31:35), ἐπισκάζω (Gen 32:32), ἐρείδω (Gen 49:6), ἐργοδιώκτης, ἐμβλέπω (Exod 3), ἐπόζω (Exod 7:18), ἐπαοιδός, which points to ἐπῳδός (Exod 7:11), ἐπαποστέλλω (Exod 8:17), ἐγκρατέω (Exod 9:2), ἐνδόσθια and ἐντόσθιος, which it points to (Exod 12:9), ἐπίμικτος, filed as ἐπίμεικτος (Exod 12:38), ἐνδοξάζομαι (Exod 14:4), ἐγκρίς, ἐλαττονέω (Exod 16), ἐξεικονίζω (Exod 21:22), ἐκδανείζω (Exod 22:24), ἐνεχύρασμα (Exod 22:25), ἐχθρεύω (Exod 23:22), ἐπίθεμα (Exod 25:17), ἐπαρυστήρ (Exod 25:38), ἐρυθροδανόω (Exod 25:5), ἐπίσπαστρον (Exod 26:36), ἐπιδιπλόω (Exod 26:9), ἐπικάλυμμα (Exod 26:14), ἐκτύπωμα (Exod 28:36), ἐνδελεχισμός (Exod 29:38), ἐξιλασμός (Exod 30:10) |
| `eng7` | zeta (1 MB) | ζωογονέω (Exod 1:17), ζυμωτός (Exod 12:19) |
| `eng25` | chi (3 MB) | χείμαρρος (Gen 32:24), χυδαῖος (Exod 1:7), χρυσόλιθος (Exod 28:20), χρῖσις (Exod 29:21), χαλβάνη (Exod 30:34) |
| `eng11` | kappa (23 MB) | κατάσχεσις (Gen 17:8), κἀγώ (Gen 20:6), κατανύσσω (Gen 27:38), καρύινος (Gen 30:37), κρυφῇ, κατάβρωσις, κλοποφορέω (Gen 31), κατοδυνάω (Exod 1:14), καταστενάζω, καταχρίω (Exod 2), κατεμβλέπω (Exod 3:6), καταδυναστεία (Exod 6:7), καμιναία (Exod 9:10), καταλιθοβολέω (Exod 17:4), κατάκαυμα (Exod 21:25), κερατίζω (Exod 21:28), κερατιστής (Exod 21:29), καρυΐσκος (Exod 25:33), κυμάτιον (Exod 25:11), κατακάλυμμα (Exod 26:14), καλυπτήρ (Exod 27:3), κίδαρις (Exod 28:4), καθυφαίνω, κατάλιθος (Exod 28:17), κοσυμβωτός (Exod 28:4), κροσσωτός (Exod 28:14), κροσσοί (Exod 28:22), κόσυμβος (Exod 28:39), κάρπωμα (Exod 29:25) |
| `eng9` | iota and theta (5 MB) | θηριάλωτος (Gen 31:39), θῖβις (Exod 2:3), θλιμμός (Exod 3:9), θημωνιά, which Rahlfs spells θιμωνιά (Exod 8:10), θυσίασμα (Exod 23:18), θυΐσκη (Exod 25:29) |
| `eng13` | mu (12 MB) | μώλωψ (Gen 4:23), μοσχάριον (Gen 18:7), μήτρα (Gen 20:18), μνημεῖον (Gen 23:6), μακροχρόνιος (Exod 20:12), μυρεψικός (Exod 30:25) |
| `eng14` | nu (4 MB) | νευροκοπέω (Gen 49:6) |
| `eng16` | omicron (12 MB) | ὀστέον (Gen 2:23), ὀκτώ (Gen 5:28), ὀπισθοφανής and ὀπισθοφανῶς (Gen 9:23), ὅλος (Gen 25:25), ὀλιγοψυχία (Exod 6:9), ὀνύχιον (Exod 28:20), ὁλοκαύτωσις (Exod 29:25) |
| `eng17` | pi, `p` to `πώϋξ` (38 MB) | πράσινος (Gen 2:12), ποιμήν (Gen 4:2), πρῶτος (Gen 8:5), filed under πρότερος, περάτης and πορθμεύς (Gen 14:13), προσοίγνυμι (Gen 19:6), παρεπίδημος (Gen 23:4), ποτιστήριον (Gen 24:20), πυρράκης (Gen 25:25), πιότης, πτερνίζω, προσοχθίζω (Gen 27), πλινθεία (Exod 1:14), πισσάσφαλτος (Exod 2:3), πολυπληθέω, πλινθουργία (Exod 5), παραδοξάζω (Exod 8:18), πικρίς (Exod 12:8), πρωτογενής (Exod 13:2), πρωΐθεν (Exod 18:13), προσαποθνήσκω (Exod 21:29), προσεμπίμπρημι (Exod 22:5), πρωτογένημα (Exod 23:16), προσπορεύομαι (Exod 24:14), περιαργυρόω (Exod 27:11), περιχαλκόω (Exod 27:6), παρωμίς (Exod 28:14), περικύκλῳ (Exod 28:33), περιστήθιον (Exod 28:4), περιστόμιον (Exod 28:32) |
| `eng21` | sigma (23 MB) | σύ (Gen 3), which Middle Liddell omits, σφαιρωτήρ (Gen 14:23), συνάντημα (Exod 9:14), σπερματίζω (Exod 9:31), σκῶλον (Exod 10:7), σκεπαστής (Exod 15:2), συσκήνιος (Exod 16:16), συναντιλαμβάνομαι (Exod 18:22), σπονδεῖον (Exod 25:29), σύμβλησις (Exod 26:24), σανιδωτός (Exod 27:8), στηθύνιον (Exod 29:26), σίκλος (Exod 30:23) |
| `eng22` | tau (12 MB) | τρεῖς (Gen 5:32), filed under τρία, τριετίζω (Gen 15:9), τροφεύω (Exod 2:7), τριστάτης (Exod 14:7), τετράστιχος (Exod 28:17) |
| `eng23` | upsilon (9 MB) | ὑπερασπίζω (Gen 15:1), ὑπερισχύω (Gen 49:26), ὑπόθεμα (Exod 25:38) |
| `eng24` | phi (8 MB) | φλόγινος (Gen 3:24), φλυκτίς and φλύκταινα (Exod 9:9), φερνίζω (Exod 22:15) |
| `eng26` | psi (2 MB) | ψαλτήριον (Gen 4:21), ψηλαφητός (Exod 10:21) |
| `eng27` | omega (2 MB) | ὦμος (Gen 21:14), ᾤα (Exod 28:32) |

To find which file holds a letter without downloading any of them, read the head of a few
and look at the first entry's key:

```bash
curl -sL -r 0-199999 https://raw.githubusercontent.com/PerseusDL/lexica/master/CTS_XML_TEI/perseus/pdllex/grc/lsj/grc.lsj.perseus-eng17.xml | grep -o 'key="[^"]*"' | head -1
```

`eng2` opens at beta, `eng3` gamma, `eng4` delta, `eng5` epsilon, `eng7` zeta, `eng11` kappa, `eng13` mu, `eng14` nu, `eng16` omicron, `eng20` rho,
`eng12` lambda, `eng20` rho, `eng21` sigma, `eng22` tau.

Entries are `<entryFree key="…">` in Beta Code, with `<tr>` for each translation, as in
Middle Liddell. Some entries define a word only by cross-reference (`ἁγιάζω` reads
`= ἁγίζω`), in which case the senses are the ones the reference points at. `build/words.py`
carries the handful found so far in its `LSJ` table, each with the entry it came from.

## The printed Rahlfs — where the Old Testament Greek comes from

The Greek in `data/` is transcribed by hand from Rahlfs's printed edition, not copied from
anything in this directory. The 1935 first printing is lending-only at the Internet Archive;
the 1950 printing, a reprint of the same text, is open:

<https://archive.org/details/septuaginta-id-est-vetus-testamentum-graece-iuxta-lxx-interpretes-edidit-by-alfred-rahlfs-1935>

The scan is of two-page spreads, and the archive's own page-number map is wrong, so go by
leaf: in volume I, leaf 26 is the title page and **leaf 27's right-hand page is Genesis,
p. 1**. A single leaf is at `https://archive.org/download/<item>/page/n27.jpg`. Cite the
printed page in each verse's `print` field. Don't commit the images.

## What these can and cannot verify

| | word forms | accents | punctuation | capitalisation |
| --- | --- | --- | --- | --- |
| SBLGNT | yes | yes | yes | yes |
| Rahlfs, printed (the scan above) | yes | yes | yes | yes |

The New Testament is checked mechanically, character for character. The Old Testament has no
digital edition behind it at all: its Greek — words, accents and pointing alike — comes from
the printed page each verse cites in `print`, and its morphology is the project's own
analysis.

`validate.py` can cross-check those two against a local Rahlfs morphological module if the
environment variable `LXX_RAHLFS_DIR` points at one. Nothing in the repository needs it, no
such module is distributed with it, and without it both checks report `SKIP`.
