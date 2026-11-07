# Backlog (top = next)

0. **Confirm the 5-year deadline** on leaving-japan (「引かれた税金を取り戻す…期限は5年以内」) on an nta.go.jp page, or soften the wording. Reason: only user-facing figure without an official source.
1. **Take-home pay calculator** — 令和9年分 税額表 is now published (basic deduction raised, 防衛特別所得税 added; URLs in FACTS.md). Build for 2027 pay from the start. Split into steps: (a) calc engine + tests against official 令和8年分 月額表 甲欄 / 電算機特例; (b) UI in six languages. Watch: 令和9年分 税額表 is being published (Nov).
   Original note: (手取り計算) in six languages — FY2026 rates from ops/FACTS.md; income tax via the monthly withholding table (源泉徴収税額表 甲欄). Verify against official examples before shipping.
2. **FAQ sections** — nenkin-refund live; payslip on `daily/2026-11-08` awaiting approval. Next: leaving-japan (3–5 questions each, original text, figures only from FACTS.md).
3. **Resident tax when leaving Japan** (出国時の住民税) explainer/estimator.
4. **Free JLPT / 特定技能 kanji quiz** — if KANJIDIC data is used it must stay CC BY-SA with credit on every page; keep paid materials separate and original.
5. **Paid material plan** — 特定技能 field vocabulary (介護, 外食, 建設…) in vi/id/ne; design only, no selling until the owner approves a platform.

6. **Search Console follow-up** — verified and sitemap.xml submitted by the owner on 2026-11-07. From ~2026-11-21, ask the owner weekly which queries bring visitors; use them to pick FAQ topics. Reason: data-driven priorities.
7. **Last official source** — 協会けんぽ全国平均 9.9% (18.3% now cited on nenkin.go.jp). Reason: still TODO in FACTS.md.

## Done
- 2026-11-08 (owner session): all FACTS.md sources re-read, no changes; 18.3% cited officially; NTA 令和9年分 table recorded; leaving-japan rules (住民税 1月1日, 在留カード返納, 納税管理人) sourced. payslip FAQ (4 Q&A × 6 languages) on `daily/2026-11-08`, 26 pages checked.
- 2026-11-08: nenkin-refund FAQ (4 Q&A × 6 languages, visible <details> + FAQPage structured data) via optional `faq.json` in build.py. All 26 pages checked with Playwright at 390px: no JS errors, no horizontal scroll, 4 FAQ items + valid JSON-LD on each nenkin-refund page. Branch `daily/2026-11-08`; owner approved, merged to `source` and deployed to main on 2026-11-08.
- 2026-11-07 (2nd run): FACTS.md now cites official pages (kyoukaikenpo r08, mhlw PDF, nenkin FAQ/leaflet) with page/check dates; old-year 国民年金保険料 derived from the official payout table. Merged to `source`.
- 2026-11-07: Search Console readiness — optional verification meta tag in build.py (root page only, validated), owner guide `ops/SEARCH_CONSOLE.md`. Verification code added and deployed to main on 2026-11-07 after owner approval.
- 2026-11-07: nenkin-refund, leaving-japan, payslip (6 languages), multilingual site, privacy page, sitemap.
8. **Sitemap lastmod per page** — build.py hard-codes 2026-11-07 for every URL; use the date each tool last changed. Reason: accurate lastmod helps recrawl after FAQ updates.
