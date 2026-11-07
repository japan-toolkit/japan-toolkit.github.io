# Backlog (top = next)

1. **Take-home pay calculator** — split into steps: (a) calc engine + tests against official 令和8年分 月額表 甲欄 / 電算機特例; (b) UI in six languages. Watch: 令和9年分 税額表 is being published (Nov).
   Original note: (手取り計算) in six languages — FY2026 rates from ops/FACTS.md; income tax via the monthly withholding table (源泉徴収税額表 甲欄). Verify against official examples before shipping.
2. **FAQ sections** under each tool (3–5 real questions each, original text) to help search and answer common worries.
3. **Resident tax when leaving Japan** (出国時の住民税) explainer/estimator.
4. **Free JLPT / 特定技能 kanji quiz** — if KANJIDIC data is used it must stay CC BY-SA with credit on every page; keep paid materials separate and original.
5. **Paid material plan** — 特定技能 field vocabulary (介護, 外食, 建設…) in vi/id/ne; design only, no selling until the owner approves a platform.

6. **Search Console follow-up** — verified and sitemap.xml submitted by the owner on 2026-11-07. From ~2026-11-21, ask the owner weekly which queries bring visitors; use them to pick FAQ topics. Reason: data-driven priorities.
7. **Last two official sources** — find official pages for 協会けんぽ全国平均 9.9% and 厚生年金 18.3% (nenkin.go.jp 保険料額表). Reason: still marked TODO in FACTS.md.

## Done
- 2026-11-07 (2nd run): FACTS.md now cites official pages (kyoukaikenpo r08, mhlw PDF, nenkin FAQ/leaflet) with page/check dates; old-year 国民年金保険料 derived from the official payout table. Merged to `source`.
- 2026-11-07: Search Console readiness — optional verification meta tag in build.py (root page only, validated), owner guide `ops/SEARCH_CONSOLE.md`. Verification code added and deployed to main on 2026-11-07 after owner approval.
- 2026-11-07: nenkin-refund, leaving-japan, payslip (6 languages), multilingual site, privacy page, sitemap.
