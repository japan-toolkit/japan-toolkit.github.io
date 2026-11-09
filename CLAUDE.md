# Japan Practical Toolkit — operating manual

Free, multilingual web tools for foreigners working in Japan.
Live site: https://japan-toolkit.github.io/ (GitHub Pages, served from branch `main`).
This branch (`source`) holds the sources and the operations notes. It is never served.

## Owner and constraints
- The owner checks in **once a day, about 30 minutes**, reading in Japanese. Write every report in Japanese.
- The owner stays **anonymous**. Never add a real name, photo, address or personal email anywhere.
- No paid services unless the owner approves. Outside companies only through the monetization rules below.
- Nothing illegal; never encourage gambling, account/SIM selling or other abuse.
- Languages, in this order: vi, ne, id, my, en, ja. English stays.
- Commit as `Claude <noreply@anthropic.com>` (`git config user.name Claude && git config user.email noreply@anthropic.com`).

## Monetization (owner goal, decided 2026-11-09)
The site exists to earn money; "official release" = the start of earning. Three ways, in this order:
1. **Donation links** (e.g. Ko-fi / GitHub Sponsors). A small link only; never pressure users.
2. **Paid study material** (e.g. 特定技能 field vocabulary books), sold on an external platform that the owner chooses.
   - GitHub Pages must not host a shop ("not allowed ... to run your online business, e-commerce site"): the site only links out.
   - Original content only: no KANJIDIC2 or other CC BY-SA data, no text copied from other sites.
   - A native-speaker check is required before anything is sold.
   - The free tools stay free and complete. Paid material is extra; never put existing free content behind a paywall.
3. **Ads**, only after the owner has chosen and signed up for an ad service.
   - Update the privacy page first (cookies, third-party ad provider, 外部送信 notice).
   - Block ad categories that target this audience: loans / consumer credit, gambling, SIM or bank-account trading,
     visa or job brokers, MLM, dating. Ads must not look like tool content and never sit inside a result area.
- The owner signs up for every service and handles payouts and seller-information duties. Claude never creates accounts,
  never enters payment details, and asks the owner before adding any third-party script.
- Every monetization change goes through the normal `daily/` branch and owner approval.

## Layout
- `tools/<tool>/index.html` — one self-contained page per tool, with a `T` translation table for all six languages.
- `build/build.py` — turns the tools into the site (per-language URLs, portals, sitemap, privacy page) in `dist/`.
- `ops/FACTS.md` — official figures the tools rely on, with sources. Check these for changes.
- `ops/BACKLOG.md` — next work, in priority order.
- `ops/REVIEW.md` — translations waiting for a native-speaker check.

## How to build and deploy
1. `python3 build/build.py` (needs node).
2. Check every page renders: serve `dist/` locally and open each `/<lang>/<tool>/` with Playwright; no JS errors, no horizontal scroll at 390px.
3. Deploy only after the owner approves: clone `main`, replace its contents with `dist/` (keep `.git`), commit, push.
   Until approval, push work to a branch named `daily/YYYY-MM-DD` instead.

## Daily routine (scheduled run)
1. Clone the repo; work on branch `source`.
2. **Facts check**: re-read each source in `ops/FACTS.md`. If any figure or page "更新日" changed, note it at the top of the report and prepare the fix on a `daily/` branch.
3. **One piece of work** from the top of `ops/BACKLOG.md` that can be finished and verified in one run. Push it to `daily/YYYY-MM-DD` on both `source` changes and a built preview. Do not merge to `main`.
4. Update `ops/BACKLOG.md` (move done items, add ideas with a one-line reason), commit to `source`.
   **Monthly (first run of each month, JST):** the KANJIDIC2 licence asks for regular data updates. www.edrdg.org is not reachable from this environment, so put a request at the top of the report: ask the owner to download https://www.edrdg.org/kanjidic/kanjidic2.xml.gz and attach it in the session. When it arrives: `python3 -I build/kanjidic_extract.py <file> tools/kanji-grade/kanji.js`, `node tools/kanji-grade/test_quiz.js`, build, check, push to `daily/`, and ask for approval. If the owner allows www.edrdg.org later, download it directly instead.
5. Report to the owner in Japanese, short:
   - 今日の要確認（法改正・数値変更があれば最優先。毎月最初の実行では漢字データ更新のお願いも）
   - 今日やったこと（branch名、変更点、確認結果）
   - 承認してほしいこと（「反映してOK」と返信すれば main に反映）
   - 明日やる予定

## Quality rules
- Every number shown to users must trace to an official source listed in `ops/FACTS.md`.
- Test calculation logic against the official tables before shipping.
- Keep tools offline-only: no data leaves the browser. No cookies or tracking unless the owner approves and the privacy page is updated first.
- Avoid copying other sites' text. Write original explanations.
