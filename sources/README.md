# Source editions

The Greek editions this project reads from. **They are not committed** — everything in this
directory except this file is excluded by [`../.gitignore`](../.gitignore). See
[`../NOTICE.md`](../NOTICE.md) for why.

Fetch them here before running `python build/validate.py`. Without them the `greek` check
cannot run; it reports `SKIP` and the summary says so explicitly rather than passing
quietly. The other four checks work without any of this.

## New Testament — SBL Greek New Testament

CC BY 4.0. Free to redistribute with attribution.

```bash
git clone --depth 1 https://github.com/LogosBible/SBLGNT.git sources/sblgnt
```

`validate.py` reads `sources/sblgnt/text/<Book>.txt`, one verse per line as
`John 1:1<TAB><greek>`.

## Old Testament — Septuagint, Rahlfs 1935

CC BY-NC-SA 4.0, **and the upstream repository asks that you agree to send a CCAT user
declaration before downloading any of its data.** Read
<https://github.com/eliranwong/LXX-Rahlfs-1935> and the
[CCAT declaration](http://ccat.sas.upenn.edu/gopher/text/religion/biblical/lxxmorph/0-user-declaration.txt)
first, and do not download if you do not agree.

```bash
git clone --depth 1 https://github.com/eliranwong/LXX-Rahlfs-1935.git sources/LXX-Rahlfs-1935
```

`validate.py` reads the MyBible module at
`sources/LXX-Rahlfs-1935/11_end-users_files/MyBible/Bibles/LXX1.SQLite3`, table `verses`,
stripping the `<S>`/`<m>` tags to recover the word forms.

## What these can and cannot verify

| | word forms | accents | punctuation | capitalisation |
| --- | --- | --- | --- | --- |
| SBLGNT | yes | yes | yes | yes |
| Rahlfs (CCAT-derived) | yes | yes | **no** | **no** |

The Rahlfs data descends from the CCAT/CATSS `lxxmorph` database, a word-level
morphological analysis that carries no sentence punctuation. So Septuagint pointing in
`data/` has no source behind it, and `validate.py` prints a standing `note` saying so
instead of reporting a clean pass. The README's *Known limitation* section discusses the
options.
