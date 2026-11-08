# Backlog (top = next)

1. **Take-home pay calculator** — (a) DONE on `daily/2026-11-08`: `tools/takehome/engine.js` (income tax 甲欄, official computer method, 2026 and 2027) + `test_engine.js` (matches the 令和9年分 月額表 within 10 yen at band midpoints up to 602,000円). (b) DONE on `daily/2026-11-08`: `insurance.js` (grades 1–50, pension 88k–650k cap, 50銭 rounding, 47 prefecture rates) + `test_insurance.js` vs the official 東京 保険料額表. Before UI: second check of the 47 rates; confirm 雇用保険 rounding. (c) UI DONE on `daily/2026-11-08` (32 pages checked; page totals = tested modules for 4 cases × 6 languages). Live on main 2026-11-08. Remaining: 雇用保険 rounding source; FAQ for takehome; bonus (賞与) mode later. Also get a few 令和8年分 月額表 rows to test the 2026 mode.
2. **FAQ sections** — nenkin-refund live; payslip live (2026-11-08); leaving-japan live (2026-11-08). Next: more questions from Search Console queries (3–5 questions each, original text, figures only from FACTS.md).
3. **Resident tax when leaving Japan** (出国時の住民税) explainer/estimator.
4. **Free JLPT / 特定技能 kanji quiz** — if KANJIDIC data is used it must stay CC BY-SA with credit on every page; keep paid materials separate and original.
5. **Paid material plan** — 特定技能 field vocabulary (介護, 外食, 建設…) in vi/id/ne; design only, no selling until the owner approves a platform.

6. **Search Console follow-up** — verified and sitemap.xml submitted by the owner on 2026-11-07. From ~2026-11-21, ask the owner weekly which queries bring visitors; use them to pick FAQ topics. Reason: data-driven priorities.
7. **Last official source** — 協会けんぽ全国平均 9.9% (18.3% now cited on nenkin.go.jp). Reason: still TODO in FACTS.md.

## Done
- 2026-11-08: take-home calculator page (6 languages) on `daily/2026-11-08`; 47 prefecture rates double-checked.
- 2026-11-08: take-home step (b) social-insurance module + tests.
- 2026-11-08: take-home step (a) income-tax engine + tests (not user-facing yet).
- 2026-11-08: 5-year tax refund period confirmed (nta taxanswer 2030, general rule). leaving-japan FAQ (4 Q&A × 6 languages) on `daily/2026-11-08`.
- 2026-11-08 (owner session): all FACTS.md sources re-read, no changes; 18.3% cited officially; NTA 令和9年分 table recorded; leaving-japan rules (住民税 1月1日, 在留カード返納, 納税管理人) sourced. payslip FAQ (4 Q&A × 6 languages) on `daily/2026-11-08`, 26 pages checked.
- 2026-11-08: nenkin-refund FAQ (4 Q&A × 6 languages, visible <details> + FAQPage structured data) via optional `faq.json` in build.py. All 26 pages checked with Playwright at 390px: no JS errors, no horizontal scroll, 4 FAQ items + valid JSON-LD on each nenkin-refund page. Branch `daily/2026-11-08`; owner approved, merged to `source` and deployed to main on 2026-11-08.
- 2026-11-07 (2nd run): FACTS.md now cites official pages (kyoukaikenpo r08, mhlw PDF, nenkin FAQ/leaflet) with page/check dates; old-year 国民年金保険料 derived from the official payout table. Merged to `source`.
- 2026-11-07: Search Console readiness — optional verification meta tag in build.py (root page only, validated), owner guide `ops/SEARCH_CONSOLE.md`. Verification code added and deployed to main on 2026-11-07 after owner approval.
- 2026-11-07: nenkin-refund, leaving-japan, payslip (6 languages), multilingual site, privacy page, sitemap.
8. **Sitemap lastmod per page** — build.py hard-codes 2026-11-07 for every URL; use the date each tool last changed. Reason: accurate lastmod helps recrawl after FAQ updates.
