# Design: free kanji quiz (2026-11-08)

## Who and why
Foreign workers (技能実習・特定技能・留学生のアルバイト) who need to *read* kanji at work and in city paperwork,
more than pass an exam. Most quiz sites teach by JLPT level; few teach the words on a factory wall or a pay slip.

## Findings that shape the design
- **No official JLPT kanji lists since 2010.** KANJIDIC2's `jlpt` field is the old 4-level test (pre-2010).
  Labelling a quiz "N5 kanji" would rest on unofficial lists, so we do not use JLPT labels.
- **KANJIDIC2** (EDRDG): CC BY-SA 4.0, free, commercial use allowed; credit + link on every page that shows it;
  derived data stays CC BY-SA; keep it current; SKIP codes are CC BY-NC-SA (do not use).
  Meanings are English (plus fr/es/pt); there is a Vietnamese Hán-Việt reading (`r_type="vietnam"`), but
  **no Nepali, Indonesian or Burmese meanings**. `grade` 1–6 = 教育漢字 (1,026 kanji, MEXT), 8 = rest of 常用.
- Our site language order is vi, ne, id, my, en, ja, so a KANJIDIC-only quiz would serve en/vi well and the others poorly.

## Plan
### Version 1: "Kanji you see at work" (original content, no external data)
- About 48 words in 4 sets: safety signs, pay slip, shifts and attendance, documents and city office.
- Each word: kanji, reading (hiragana), meaning in all six languages, one line on where you see it.
- Two modes: kanji → meaning (in your language), kanji → reading. 4 choices; wrong choices come from the same set.
- 10 questions per round, then a review of the ones you missed (with reading and meaning).
- Best score per set is kept on the device (localStorage, per-viewer convenience only; nothing sent anywhere).
- All text is written by us, so no licence conditions apply. Readings and meanings are checked twice.
- Safety words are the reason this exists: a wrong answer on 立入禁止 or 火気厳禁 matters more than on a JLPT word.

### Version 2 (later, needs owner OK): school-grade kanji from KANJIDIC2
- 教育漢字 by grade 1–6 (1,026), readings quiz for every language; English meaning; Hán-Việt for Vietnamese.
- Footer credit on every quiz page; data file published as CC BY-SA; monthly data refresh in the daily run.
- Needs the official `kanjidic2.xml.gz` from edrdg.org. The fetch tool here cannot save binary files, so the
  owner should decide how we get it (e.g. allow a direct download in the build, or the owner downloads it once).

## Not doing
- No JLPT level claims. No paid content mixed into the free quiz. No tracking.
