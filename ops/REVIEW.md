# Translations waiting for a native-speaker check

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
| ne (Nepali) | all 3 tools, portal | medium | not reviewed |
| my (Burmese) | all 3 tools, portal | medium-low | not reviewed — highest priority |
| vi (Vietnamese) | all 3 tools, portal | good | not reviewed |
| id (Indonesian) | all 3 tools, portal | good | not reviewed |
| all five | nenkin-refund FAQ (tools/nenkin-refund/faq.json, 4 Q&A, added 2026-11-08) | vi/id good, ne medium, my medium-low | not reviewed |
| all five | payslip FAQ (tools/payslip/faq.json, 4 Q&A, added 2026-11-08) | vi/id good, ne medium, my medium-low | not reviewed |
| all five | leaving-japan FAQ (tools/leaving-japan/faq.json, 4 Q&A, added 2026-11-08) | vi/id good, ne medium, my medium-low | not reviewed |
| all five | takehome calculator (tools/takehome/index.html, new tool, added 2026-11-08) | vi/id good, ne medium, my medium-low | not reviewed |
| all five | takehome FAQ (tools/takehome/faq.json, 4 Q&A, added 2026-11-08) | vi/id good, ne medium, my medium-low | not reviewed |
| all five | resident-tax guide (tools/resident-tax/index.html, new tool, added 2026-11-08) | vi/id good, ne medium, my medium-low | not reviewed |
| all five | resident-tax FAQ (tools/resident-tax/faq.json, 4 Q&A, added 2026-11-08) | vi/id good, ne medium, my medium-low | not reviewed |
| all five | kanji-work quiz (tools/kanji-work/words.js 120 words in 10 sets incl. construction/care/food/farm/factory/hotel, added 2026-11-08) — also check readings/meanings of every word | vi/id good, ne medium, my medium-low | not reviewed |
| all five | kanji-grade quiz UI strings (tools/kanji-grade/index.html, added 2026-11-08; data itself is KANJIDIC2) | vi/id good, ne medium, my medium-low | not reviewed |
