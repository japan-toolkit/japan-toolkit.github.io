# Official figures used by the tools (last checked 2026-11-07 18:40 JST)

Every row should cite a primary (official) page. "Checked" = page re-read and figure confirmed on that date.

| Figure | Value | Used in | Source (official) | Page 更新日 | Checked |
|---|---|---|---|---|---|
| 脱退一時金ページ | — | nenkin-refund | https://www.nenkin.go.jp/service/jukyu/seido/sonota-kyufu/dattai-ichiji/20150406.html | 2026-04-01 | 2026-11-07 |
| 厚生年金 支給率表 (60月上限, 最終月2021年4月以降) | 0.5/1.1/1.6/2.2/2.7/3.3/3.8/4.4/4.9/5.5 | nenkin-refund | same page | 2026-04-01 | 2026-11-07 |
| 請求期限 | 日本に住所を有しなくなった日から2年以内 | nenkin-refund, leaving-japan | same page | 2026-04-01 | 2026-11-07 |
| 国民年金 脱退一時金 FY2026 | 6月=53,760円 … 60月以上=537,600円 (FY2025 60月=525,300 / FY2024 509,400 / FY2023 495,600) | nenkin-refund | https://www.nenkin.go.jp/service/jukyu/seido/sonota-kyufu/dattai-ichiji/20210401_01.html | 2026-04-01 | 2026-11-07 |
| 国民年金保険料 月額 FY2026 | 17,920円 | nenkin-refund | https://www.nenkin.go.jp/faq/kokunen/seido/hokenryo/seidosetsumei/20150331.html | 2026-04-01 | 2026-11-07 |
| 国民年金保険料 月額 FY2025 / FY2024 / FY2023 | 17,510 / 16,980 / 16,520円 | nenkin-refund | Derived from the payout table above ÷ 30 (60月 payout = 保険料 × 1/2 × 60), 20210401_01.html. The FAQ page shows the current year only. | 2026-04-01 | 2026-11-07 |
| 源泉徴収 (厚生年金の脱退一時金) | 20.42% (国民年金分は源泉徴収なし) | nenkin-refund | https://www.nenkin.go.jp/international/english/japanese-system/benefit/payment.files/B.pdf (nenkin.go.jp leaflet, marked 2026.9) | 2026-09 | 2026-11-07 |
| 協会けんぽ 健康保険料率 | 都道府県別 (例 東京 9.85%); 全国平均 9.9% | payslip | https://www.kyoukaikenpo.or.jp/about/business/insurance_rate/rate_prefectures/r08/ (3月分=4月納付分から). 全国平均 9.9% is NOT stated on that page — still from 報道 (rodo.co.jp/news/211243). TODO: official statement. | not shown | 2026-11-07 |
| 介護保険料率 (40〜64歳) | 1.62% (2026年3月分から) | payslip | same kyoukaikenpo r08 page | not shown | 2026-11-07 |
| 子ども・子育て支援金率 | 0.23% (2026年4月分=5月納付分から, 全国一律) | payslip | same kyoukaikenpo r08 page | not shown | 2026-11-07 |
| 雇用保険 労働者負担 (一般の事業) | 5/1,000 (事業主 8.5/1,000, 計 13.5/1,000; 2026-04-01〜2027-03-31; 前年 5.5/1,000) | payslip | https://www.mhlw.go.jp/content/001672589.pdf (linked from 栃木労働局 newpage_01657) | not shown | 2026-11-07 |
| 厚生年金保険料率 | 18.3% (本人 9.15%) | nenkin-refund, payslip | NOT confirmed on an official page yet (the 脱退一時金 page gives only the rule). TODO: nenkin.go.jp 保険料額表 page. | — | — |

## Calendar
- New fiscal-year rates are usually announced Feb–Mar and apply from March/April. Watch closely in those months.
- November: NTA publishes next year's 源泉徴収税額表 (a `zeigakuhyo2027` folder for 令和9年分 already exists on nta.go.jp). This matters for the planned take-home calculator.
