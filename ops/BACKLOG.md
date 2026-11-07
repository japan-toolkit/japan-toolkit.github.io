# Backlog (top = next)

1. **Take-home pay calculator** (手取り計算) in six languages — FY2026 rates from ops/FACTS.md; income tax via the monthly withholding table (源泉徴収税額表 甲欄). Verify against official examples before shipping.
2. **FAQ sections** under each tool (3–5 real questions each, original text) to help search and answer common worries.
3. **Resident tax when leaving Japan** (出国時の住民税) explainer/estimator.
4. **Free JLPT / 特定技能 kanji quiz** — if KANJIDIC data is used it must stay CC BY-SA with credit on every page; keep paid materials separate and original.
5. **Paid material plan** — 特定技能 field vocabulary (介護, 外食, 建設…) in vi/id/ne; design only, no selling until the owner approves a platform.

6. **Waiting on owner: Search Console code** — once the owner sends the HTML-tag code, put it in `ops/google-site-verification.txt`, rebuild, verify, deploy after 「反映してOK」. (Code ready on `daily/2026-11-07`.)
7. **FACTS.md source fix** — the 国民年金保険料 monthly amounts are not on 20210401_01.html (it only lists payouts); find the official 保険料 page on nenkin.go.jp and cite it. Reason: every number must trace to an official source.
8. **Primary sources for payslip rates** — replace kaiketsu-j / all-senmonka citations with kyoukaikenpo.or.jp and mhlw.go.jp pages. Reason: same rule.

## Done
- 2026-11-07: Search Console readiness — optional verification meta tag in build.py (root page only, validated), owner guide `ops/SEARCH_CONSOLE.md`. Branch `daily/2026-11-07` (not merged to `source` yet; merge when deploying).
- 2026-11-07: nenkin-refund, leaving-japan, payslip (6 languages), multilingual site, privacy page, sitemap.
