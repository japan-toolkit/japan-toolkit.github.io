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
- 48 words in 4 sets (safety signs, pay slip, shifts, documents) + 72 words in 6 特定技能-field sets (construction, care, food service, farming, factory, hotel) = 120 words. 2026-11-09: +12 fishing (漁業) = 132 words, 11 sets. +12 car maintenance (自動車整備) = 144 words, 12 sets. +12 building cleaning (ビルクリーニング) = 156 words, 13 sets. +12 aviation (航空) = 168 words, 14 sets. 2026-11-10: +12 shipbuilding (造船・舶用工業) = 180 words, 15 sets. +12 railways (鉄道) = 192 words, 16 sets. 2026-11-11: +12 forestry (林業) = 204 words, 17 sets. 2026-11-12: +12 wood products (木材産業) = 216 words, 18 sets.
- Each word: kanji, reading (hiragana), meaning in all six languages, one line on where you see it.
- Two modes: kanji → meaning (in your language), kanji → reading. 4 choices; wrong choices come from the same set.
- 10 questions per round, then a review of the ones you missed (with reading and meaning).
- Best score per set is kept on the device (localStorage, per-viewer convenience only; nothing sent anywhere).
- All text is written by us, so no licence conditions apply. Readings and meanings are checked twice.
- Safety words are the reason this exists: a wrong answer on 立入禁止 or 火気厳禁 matters more than on a JLPT word.

### Version 2: school-grade kanji from KANJIDIC2 (built 2026-11-08, tools/kanji-grade)
- 教育漢字 by grade 1–6 (1,026), readings quiz for every language; English meaning; Hán-Việt for Vietnamese.
- Footer credit on every quiz page; data file published as CC BY-SA; monthly data refresh in the daily run.
- Needs the official `kanjidic2.xml.gz` from edrdg.org. The fetch tool here cannot save binary files, so the
  owner should decide how we get it (e.g. allow a direct download in the build, or the owner downloads it once).

## Not doing
- No JLPT level claims. No paid content mixed into the free quiz. No tracking.

## Version 2 notes (2026-11-08)
- Data: owner-supplied `kanjidic2.xml.gz` (database_version 2026-311, created 2026-11-07, sha256 0ac6d0c0…ce7).
  `build/kanjidic_extract.py` keeps grades 1–6 only (1,026 = 80/160/200/202/193/191) and only literal, grade,
  strokes, on/kun readings, English meanings, Vietnamese readings. Output `tools/kanji-grade/kanji.js` (CC BY-SA 4.0 header).
- Modes: reading (all languages), English meaning (all), Hán-Việt (vi only). A distractor is never a real reading of
  the shown kanji, and meaning distractors never share a meaning word with the answer (`test_quiz.js`, 9,234 questions).
- Credit line with links to KANJIDIC project, EDRDG, licence and CC BY-SA 4.0 on every language page, plus the data version.
- Refresh: the licence asks web dictionary services to update at least monthly. www.edrdg.org is not reachable from
  this environment, so on the first run of each month ask the owner for a new file (or to allow the domain), re-run
  the extract script and the tests, and ship.

## Review-mistakes mode (2026-11-09)
- Results screen: 'practise the missed words' starts a round with only this round's mistakes.
- Start screen: 'review my mistakes (n)' appears when this device remembers missed words for the chosen set + mode
  (localStorage `kjw-miss`, kanji only). A word leaves the list when answered correctly in any round.
- Retry/review rounds do not change the best score (only full 10-question rounds count).
- Privacy page now mentions that missed quiz words are stored on the device.
- 2026-11-09: same mode added to kanji-grade (localStorage `kjg-miss`, per grade + mode; `makeRoundFrom` in quiz.js, tested).
