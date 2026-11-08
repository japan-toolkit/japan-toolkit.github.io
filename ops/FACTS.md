# Official figures used by the tools (last checked 2026-11-08 JST, all sources re-read)

Every row should cite a primary (official) page. "Checked" = page re-read and figure confirmed on that date.

| Figure | Value | Used in | Source (official) | Page 更新日 | Checked |
|---|---|---|---|---|---|
| 脱退一時金ページ | — | nenkin-refund | https://www.nenkin.go.jp/service/jukyu/seido/sonota-kyufu/dattai-ichiji/20150406.html | 2026-04-01 | 2026-11-08 |
| 厚生年金 支給率表 (60月上限, 最終月2021年4月以降) | 0.5/1.1/1.6/2.2/2.7/3.3/3.8/4.4/4.9/5.5 | nenkin-refund | same page | 2026-04-01 | 2026-11-08 |
| 請求期限 | 日本に住所を有しなくなった日から2年以内 | nenkin-refund, leaving-japan | same page | 2026-04-01 | 2026-11-08 |
| 国民年金 脱退一時金 FY2026 | 6月=53,760円 … 60月以上=537,600円 (FY2025 60月=525,300 / FY2024 509,400 / FY2023 495,600) | nenkin-refund | https://www.nenkin.go.jp/service/jukyu/seido/sonota-kyufu/dattai-ichiji/20210401_01.html | 2026-04-01 | 2026-11-08 |
| 国民年金保険料 月額 FY2026 | 17,920円 | nenkin-refund | https://www.nenkin.go.jp/faq/kokunen/seido/hokenryo/seidosetsumei/20150331.html | 2026-04-01 | 2026-11-08 |
| 国民年金保険料 月額 FY2025 / FY2024 / FY2023 | 17,510 / 16,980 / 16,520円 | nenkin-refund | Derived from the payout table above ÷ 30 (60月 payout = 保険料 × 1/2 × 60), 20210401_01.html. The FAQ page shows the current year only. | 2026-04-01 | 2026-11-08 |
| 源泉徴収 (厚生年金の脱退一時金) | 20.42% (国民年金分は源泉徴収なし) | nenkin-refund | https://www.nenkin.go.jp/international/english/japanese-system/benefit/payment.files/B.pdf (nenkin.go.jp leaflet, marked 2026.9) | 2026-09 | 2026-11-08 |
| 協会けんぽ 健康保険料率 | 都道府県別 9.21% (新潟) 〜 10.55% (佐賀), 東京 9.85% (2026年3月分から). payslip band 4.0–6.0% of gross covers every half-rate. Sample 12,805 = 東京 grade 20 (260,000) 折半額 | payslip, takehome | https://www.kyoukaikenpo.or.jp/about/business/insurance_rate/rate_prefectures/r08/ ; R8_13tokyo.pdf | not shown | 2026-11-08 |
| 介護保険料率 (40〜64歳) | 1.62% (2026年3月分から) | payslip | same kyoukaikenpo r08 page | not shown | 2026-11-08 |
| 子ども・子育て支援金率 | 0.23% (2026年4月分=5月納付分から, 全国一律) | payslip | same kyoukaikenpo r08 page | not shown | 2026-11-08 |
| 雇用保険 労働者負担 (一般の事業) | 5/1,000 (事業主 8.5/1,000, 計 13.5/1,000; 2026-04-01〜2027-03-31; 前年 5.5/1,000) | payslip | https://www.mhlw.go.jp/content/001672589.pdf (linked from 栃木労働局 newpage_01657) | not shown | 2026-11-08 |
| 厚生年金保険料率 | 18.3% (本人 9.15%) | nenkin-refund, payslip | https://www.nenkin.go.jp/service/kounen/hokenryo/ryogaku/ryogakuhyo/index.html 「厚生年金保険料率は18.3％で固定されています」 | not shown | 2026-11-08 |
| 源泉徴収税額表 令和8年分 | 月額表 01-07.pdf, 電算機特例 18.pdf | (planned take-home calc) | https://www.nta.go.jp/publication/pamph/gensen/zeigakuhyo2026/01.htm | — | 2026-11-08 |
| 源泉徴収税額表 令和9年分 (2027年に支払う給与) | 公表済み。「令和８年度税制改正において、所得税の基礎控除の引上げ等が行われたことに伴い、税額が変更」。対象税目に防衛特別所得税が加わる。月額表 data/01-07.pdf, 告示 data/18.pdf | payslip FAQ, (planned take-home calc) | https://www.nta.go.jp/publication/pamph/gensen/zeigakuhyo2027/01.htm ; あらまし https://www.nta.go.jp/publication/pamph/gensen/2026kaisei.pdf | — | 2026-11-08 |
| 源泉徴収 電算機方式 (甲欄) 令和9年分 | 給与所得控除 ~169,444→57,500 / 30%+6,667 / 20%+36,667 / 10%+91,667 / 162,500; 基礎控除 51,667 (A≤2,120,833, 以降 40,000/26,667/13,334/0); 配偶者・扶養 31,667/人; 税率 5.105% … 45.945% (別表第四); 10円未満四捨五入. 令和8年分は 給与所得控除 最低 54,167 (≤158,333), 基礎控除 48,334 | takehome engine | https://www.nta.go.jp/publication/pamph/gensen/zeigakuhyo2027/data/18.pdf ; 2026: …/zeigakuhyo2026/data/18.pdf | 令和8年財務省告示第128号 | 2026-11-08 |
| 標準報酬月額 等級表 (健保1–50 / 厚年1–32) + 折半額 | 58,000〜1,390,000円; 厚年 88,000〜650,000円; 控除時は50銭以下切捨て・50銭超切上げ | takehome insurance.js | https://www.kyoukaikenpo.or.jp/assets/R8_13tokyo.pdf 「令和８年３月分（４月納付分）からの健康保険・厚生年金保険の保険料額表」(東京支部) | 令和8年3月分〜 | 2026-11-08 |
| 協会けんぽ 都道府県別 健康保険料率 (47) | 北海道 10.28 … 東京 9.85 … 佐賀 10.55 (最高) … 新潟 9.21 (最低), full list in tools/takehome/insurance.js | takehome | https://www.kyoukaikenpo.or.jp/about/business/insurance_rate/rate_prefectures/r08/ — second independent read 2026-11-08: all 47 identical | not shown | 2026-11-08 |
| 雇用保険料の端数処理 | 賃金から源泉控除する場合「50銭以下の場合は切り捨て、50銭1厘以上の場合は切り上げ」; 基準は賃金総額（総支給額） | takehome insurance.js | https://www.mhlw.go.jp/new-info/kobetu/roudou/gyousei/hoken/2020/dl/keizoku-20.pdf (p.20) | (2020 edition) | 2026-11-08 |
| 個人住民税の課税 | その年の1月1日時点で住所がある人に課税 | leaving-japan | https://www.soumu.go.jp/main_sosiki/jichi_zeisei/czaisei/czaisei_seido/150790_06.html 「個人住民税は、その年の1月1日時点で市町村（都道府県）に住所がある方に対して課税されます。」 | not shown | 2026-11-08 |
| 在留カードの返納 | 再入国許可によらない出国は出入国港で直ちに返納 (みなし再入国の扱いはこのページに記載なし) | leaving-japan | https://www.moj.go.jp/isa/applications/procedures/nyuukokukanri10_00020.html | not shown | 2026-11-08 |
| 納税管理人 (脱退一時金の税金還付) | 帰国前に最終住所地の税務署へ「納税管理人の届出書」。出さずに帰国した場合は申告時に併せて提出 | nenkin-refund, leaving-japan | B.pdf leaflet (above) | 2026-09 | 2026-11-08 |
| 還付申告の期限 | 還付申告書は「その年の翌年1月1日から5年間提出することができます」(一般規定。退職所得の選択課税の様式ページは未確認) | leaving-japan | https://www.nta.go.jp/taxes/shiraberu/taxanswer/shotoku/2030.htm | 令和8年4月1日現在法令等 | 2026-11-08 |

## Calendar
- New fiscal-year rates are usually announced Feb–Mar and apply from March/April. Watch closely in those months.
- November: NTA publishes next year's 源泉徴収税額表 (a `zeigakuhyo2027` folder for 令和9年分 already exists on nta.go.jp). This matters for the planned take-home calculator.
