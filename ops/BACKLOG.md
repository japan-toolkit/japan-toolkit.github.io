# Backlog (top = next)

1. **Translation quality (AI cross-review, see ops/REVIEW.md)** — my/ne safety + leaving/resident-tax done on `daily/2026-11-08` (awaiting approval). Next: my/ne remaining tools, then vi, id. Also: 'translation mistake?' link on every page lets real users report.
2. **Search Console follow-up** — from ~2026-11-21, ask the owner weekly which queries bring visitors; use them to pick new FAQ questions and tools. Reason: data-driven priorities.
3. **Take-home calculator: bonus (賞与)** — live on main 2026-11-08 (NTA bonus rate table 2026/2027 transcribed twice; official worked example passes). Later: add a bonus FAQ question.
4. **Kanji quizzes** — monthly KANJIDIC2 refresh (CLAUDE.md). Ideas: more field sets (漁業, 自動車整備, 航空, ビルクリーニング), a "review my mistakes" mode. Words must be checked twice.
5. **Paid material plan** — 特定技能 field vocabulary in vi/id/ne; design only, no selling until the owner approves a platform. Keep separate from the free quizzes (KANJIDIC data is CC BY-SA; paid material must not use it).
6. **Last-year resident tax estimate** — only if an official, nationwide formula can be cited; otherwise keep the guide as is.

## Status of shipped tools (all live on main, 2026-11-08)
- takehome (income tax 2026/2027 甲欄 + FY2026 insurance, 47 prefectures, FAQ) · nenkin-refund (+FAQ) · leaving-japan (+FAQ, links) ·
  resident-tax (+FAQ) · payslip (+FAQ, official rate range) · kanji-work (120 words, 10 sets) · kanji-grade (1,026 kanji, KANJIDIC2 2026-311).
- Sitemap lastmod per tool. Privacy page mentions quiz scores.

## Done
- 2026-11-08: kanji-grade quiz (1,026 kanji, reading/meaning/Hán-Việt), 50 pages checked, 9,234 generated questions tested.
- 2026-11-08: kanji-work quiz v1 (new tool), privacy page updated for quiz scores, 44 pages checked, full play-through test in 6 languages × 4 sets × 2 modes.
- 2026-11-08: resident-tax guide (new tool, 6 languages), 38 pages checked.
- 2026-11-08: payslip no longer relies on the unofficial 9.9% national average: note cites the official prefecture range 9.21–10.55%, sample health amount = official Tokyo table (12,805). Live on main 2026-11-08.
- 2026-11-08: take-home calculator page (6 languages) on `daily/2026-11-08`; 47 prefecture rates double-checked.
- 2026-11-08: take-home step (b) social-insurance module + tests.
- 2026-11-08: take-home step (a) income-tax engine + tests (not user-facing yet).
- 2026-11-08: 5-year tax refund period confirmed (nta taxanswer 2030, general rule). leaving-japan FAQ (4 Q&A × 6 languages) on `daily/2026-11-08`.
- 2026-11-08 (owner session): all FACTS.md sources re-read, no changes; 18.3% cited officially; NTA 令和9年分 table recorded; leaving-japan rules (住民税 1月1日, 在留カード返納, 納税管理人) sourced. payslip FAQ (4 Q&A × 6 languages) on `daily/2026-11-08`, 26 pages checked.
- 2026-11-08: nenkin-refund FAQ (4 Q&A × 6 languages, visible <details> + FAQPage structured data) via optional `faq.json` in build.py. All 26 pages checked with Playwright at 390px: no JS errors, no horizontal scroll, 4 FAQ items + valid JSON-LD on each nenkin-refund page. Branch `daily/2026-11-08`; owner approved, merged to `source` and deployed to main on 2026-11-08.
- 2026-11-07 (2nd run): FACTS.md now cites official pages (kyoukaikenpo r08, mhlw PDF, nenkin FAQ/leaflet) with page/check dates; old-year 国民年金保険料 derived from the official payout table. Merged to `source`.
- 2026-11-07: Search Console readiness — optional verification meta tag in build.py (root page only, validated), owner guide `ops/SEARCH_CONSOLE.md`. Verification code added and deployed to main on 2026-11-07 after owner approval.
- 2026-11-07: nenkin-refund, leaving-japan, payslip (6 languages), multilingual site, privacy page, sitemap.
8. **Sitemap lastmod per page** — done, live on main 2026-11-08 (git date of each tool, JST).
