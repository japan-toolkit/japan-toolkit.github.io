# Translations waiting for a native-speaker check

## AI cross-review (no native reviewer available) — method, 2026-11-08
1. Extract the target-language strings only (no English) from `ops/review/<lang>.md`.
2. A fresh reviewer agent that never sees the English back-translates each string literally and lists native-reader
   problems (grammar, unnatural wording, wrong term, register, Unicode), with a corrected version.
3. A second fresh agent back-translates only the corrections. Claude compares both back-translations with the English
   source and accepts a correction only if the meaning still matches (hedges like "may" kept, numbers unchanged).
4. Apply with `build/apply_translation_fixes.py` — it replaces whole strings by key only. (A first version replaced
   substrings and changed unrelated text, e.g. a short Burmese word inside 'tax'; caught before deploy and redone.)
   Rerun all tests, rebuild review sheets, ship through the normal approval.
This catches meaning errors and obvious unnatural wording, but it is still machine judgement: real users' reports
(the "translation mistake?" link on every page → GitHub issue) stay the final check.

### Done
- 2026-11-08 my + ne: leaving-japan, resident-tax (all strings + FAQ) and all 120 kanji-work words. my: 41 flagged,
  37 corrections applied, 4 rejected (2 kept original wording, 2 replaced by better terms: 図面, 通勤手当); hedges fixed
  ("may not be approved"). ne: 34 flagged, 32 applied, 2 rejected (排泄, 転出届 kept). Consistent terms now:
  my 通勤手当 = အလုပ်သွားလာစရိတ် ထောက်ပံ့ငွေ, 差引支給額 = အသားတင် လက်ခံရငွေ; ne "पेन्सन (नेन्किन)".
- 2026-11-08 my + ne round 2: takehome, payslip, nenkin-refund, kanji-grade/kanji-work UI and FAQs. my: 53 flagged,
  46 applied (4 rejected: 'prefecture' rendered as 'district', a refund line that became 'part of', an eligibility line
  that became ambiguous, 1 style-only). ne: 31 flagged, 30 applied (1 rejected: bonus hint changed meaning).
  Many fixes hedge firm claims ("usually", "may") and fix terms (Burmese 子ども・子育て支援金 no longer reads as an allowance
  you receive; kun label no longer reads as 'tax').
- 2026-11-08 vi + id (all strings, ~390 each): vi 32 flagged / 32 applied, id 14 flagged / 14 applied (1 adjusted).
  Found two content issues that also affected en/ja/ne/my and were fixed in all six languages:
  (1) "giving or selling your phone or SIM is illegal" was too broad → now "a SIM card or phone line in your name";
  (2) "you can get most of this back" (payslip, pension) → "part of this back (up to a limit)" in en/ja/vi/id.
- 2026-11-09 takehome FAQ new Q (bonus income tax, 5th item): vi/ne/id/my cross-reviewed; 0 meaning errors, wording fixes
  applied in all four (vi 'được'/'tiền thuế là', id 'tabel tarif pajak bonus'/'dikalikan', my subject 'အခွန်ကို' + 'တွက်ချက်',
  ne 'बीमा शुल्क'); second back-translation matched the English.
- 2026-11-09 (2) bonus '10×' wording (bSpecial + FAQ, both amounts 'after insurance'): cross-reviewed, meaning OK in all 4;
  applied: my 'နုတ်ပြီးသော' (adjectival, key fix) + sentence split, ne comma, id 'yang juga sudah dipotong', vi 'vượt quá'/'thì'.
  Rejected: new insurance terms (my လူမှုဖူလုံရေး…, id iuran asuransi sosial) to keep site-wide terms; added 'because' clauses.
- 2026-11-09 (3) kanji-work 'fishing' set (12 words + topic name + lede): readings checked blind (all 12 match, single standard
  reading), glosses back-translated blind; applied ne topic grammar, ne 漁港 reorder, ne 船酔い calque removed, my 餌 = feed/bait,
  vi 'và'. Kept my topic ငါးလုပ်ငန်း (ရေလုပ်ငန်း is the official term; consider).
- 2026-11-09 (4) kanji-work 'car' (自動車整備) set: readings checked blind (all match; 輪止め わどめ / オイル漏れ noted in ja meaning);
  故障 replaced by 洗車 (overlapped with 油漏れ as a distractor). Applied my 車検 'ကာလအလိုက်', my 燃料 'လောင်စာဆီ', my bolt 'မူလီ',
  id 'Uji berkala kendaraan', ne 'दबाब', ne topic 'गाडी मर्मत सम्भार'; second back-translation clean.
- 2026-11-09 (5) kanji-work 'cleaning' (ビルクリーニング) set: readings checked blind (床 = ゆか on the job); 混ぜるな危険 clear in all 4.
  Fixed ne ladder (सिँढी 'stairs' → भर्याङ 'ladder'), ne detergent/vacuum/ventilation/sign wording, vi 'Đang làm vệ sinh',
  vi bleach 'thuốc tẩy trắng', my detergent (was readable as sanitizer), id topic 'Pembersihan gedung'; second back-translation clean.
- 2026-11-09 (6) kanji-work review mode UI (retry / review / footer note): cross-reviewed; fixed 'wrong words' → 'words you
  answered wrongly' in ne/id, shorter my button labels; second back-translation clean.
- 2026-11-09 (7) kanji-work 'aviation' (航空) set: readings checked blind (all match; staff often say ゲート/エプロン/FOD/ディレイ).
  Sharpened 手荷物 vs 貨物 and 駐機場 vs 立入制限区域 glosses in all languages (could both look right); vi 遅延 no longer reads
  as 'missed my flight'; ne 制限区域 'प्रतिबन्धित', ne nouns instead of verbs; my 誘導/整備士/駐機場 fixed; second back-translation clean.
- 2026-11-09 (8) kanji-grade review mode UI: vi/ne/id fine; my 'မှားသော/မှားခဲ့သော' read as 'incorrect kanji' → 'မှားဖြေခဲ့သော'
  (answered wrongly), same fix applied to the kanji-work strings; back-translation clean.
- 2026-11-10 kanji-work 'shipbuilding' (造船・舶用工業) set: readings checked blind — caught 玉掛け = たまがけ (draft had たまかけ),
  fixed before shipping. Fixed: ne machining no longer says 'cut' (overlapped with 切断; 'खिएर' rejected as ungrammatical → 'ताछेर'),
  vi/id topic names now say marine *equipment* (舶用) not shipping in general, vi 'oxy' spelling, id/vi slinging = tie *and hang*
  on the crane hook, ja 玉掛け explanation; second back-translation clean.
- Status: all four languages AI-cross-reviewed once. Next: re-run after each text change; watch GitHub issues.

## How to get a free review (plan, 2026-11-08)
- Review sheets: `ops/review/<lang>.md` (vi, ne, id, my, ja). Each lists every string next to the English, with a
  "correction" column. Regenerate after any text change: `python3 build/export_review.py`.
- Share the GitHub link of one sheet with a native speaker you know (friend, coworker, language-exchange partner).
  They can reply with corrections in any form; Claude applies them, rebuilds and asks for approval as usual.
- Priority order: 1) kanji-work safety words and leaving-japan/resident-tax steps (wrong = real harm),
  2) calculators' labels and notes, 3) FAQ, 4) everything else. Burmese (my) first, then Nepali (ne).
- No paid services or companies. Credit reviewers only if they want it (first name or handle), never the owner.

Machine-written; confidence noted. The owner decides when to order a review.

| Language | Pages | Confidence | Status |
|---|---|---|---|
| ne (Nepali) | all tools | medium → AI cross-reviewed 2026-11-08 | no native review |
| my (Burmese) | all tools | medium-low → AI cross-reviewed 2026-11-08 | no native review — highest priority |
| vi (Vietnamese) | all tools | good → AI cross-reviewed 2026-11-08 | no native review |
| id (Indonesian) | all tools | good → AI cross-reviewed 2026-11-08 | no native review |
| all five | nenkin-refund FAQ (tools/nenkin-refund/faq.json, 4 Q&A, added 2026-11-08) | vi/id good, ne medium, my medium-low | not reviewed |
| all five | payslip FAQ (tools/payslip/faq.json, 4 Q&A, added 2026-11-08) | vi/id good, ne medium, my medium-low | not reviewed |
| all five | leaving-japan FAQ (tools/leaving-japan/faq.json, 4 Q&A, added 2026-11-08) | vi/id good, ne medium, my medium-low | not reviewed |
| all five | takehome calculator (tools/takehome/index.html, new tool, added 2026-11-08) | vi/id good, ne medium, my medium-low | not reviewed |
| all five | takehome FAQ (tools/takehome/faq.json, 5 Q&A, added 2026-11-08; bonus Q added 2026-11-09) | vi/id good, ne medium, my medium-low | not reviewed |
| all five | resident-tax guide (tools/resident-tax/index.html, new tool, added 2026-11-08) | vi/id good, ne medium, my medium-low | not reviewed |
| all five | resident-tax FAQ (tools/resident-tax/faq.json, 4 Q&A, added 2026-11-08) | vi/id good, ne medium, my medium-low | not reviewed |
| all five | kanji-work quiz (tools/kanji-work/words.js 180 words in 15 sets incl. construction/care/food/farm/factory/hotel/fishing/car/cleaning/aviation/shipbuilding, added 2026-11-08) — also check readings/meanings of every word | vi/id good, ne medium, my medium-low | not reviewed |
| all five | kanji-grade quiz UI strings (tools/kanji-grade/index.html, added 2026-11-08; data itself is KANJIDIC2) | vi/id good, ne medium, my medium-low | not reviewed |
