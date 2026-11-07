// Employee social-insurance premiums for one month (FY2026), from the official
// 協会けんぽ 令和8年度 保険料額表 (東京支部: https://www.kyoukaikenpo.or.jp/assets/R8_13tokyo.pdf).
// Grade boundaries are national; only the health-insurance rate differs by prefecture.
// [standard monthly pay 標準報酬月額, lower bound of 報酬月額 (以上)] for 健康保険 grades 1-50.
const GRADES = [[58000,0],[68000,63000],[78000,73000],[88000,83000],[98000,93000],[104000,101000],[110000,107000],
 [118000,114000],[126000,122000],[134000,130000],[142000,138000],[150000,146000],[160000,155000],[170000,165000],
 [180000,175000],[190000,185000],[200000,195000],[220000,210000],[240000,230000],[260000,250000],[280000,270000],
 [300000,290000],[320000,310000],[340000,330000],[360000,350000],[380000,370000],[410000,395000],[440000,425000],
 [470000,455000],[500000,485000],[530000,515000],[560000,545000],[590000,575000],[620000,605000],[650000,635000],
 [680000,665000],[710000,695000],[750000,730000],[790000,770000],[830000,810000],[880000,855000],[930000,905000],
 [980000,955000],[1030000,1005000],[1090000,1055000],[1150000,1115000],[1210000,1175000],[1270000,1235000],
 [1330000,1295000],[1390000,1355000]];
// 協会けんぽ 令和8年度 健康保険料率 (%), from https://www.kyoukaikenpo.or.jp/about/business/insurance_rate/rate_prefectures/r08/
// transcribed 2026-11-08. second independent read 2026-11-08: all 47 identical.
const HEALTH_RATE_FY2026 = {"北海道":10.28, "青森":9.85, "岩手":9.51, "宮城":10.10, "秋田":10.01, "山形":9.75, "福島":9.50, "茨城":9.52, "栃木":9.82, "群馬":9.68, "埼玉":9.67, "千葉":9.73, "東京":9.85, "神奈川":9.92, "新潟":9.21, "富山":9.59, "石川":9.70, "福井":9.71, "山梨":9.55, "長野":9.63, "岐阜":9.80, "静岡":9.61, "愛知":9.93, "三重":9.77, "滋賀":9.88, "京都":9.89, "大阪":10.13, "兵庫":10.12, "奈良":9.91, "和歌山":10.06, "鳥取":9.86, "島根":9.94, "岡山":10.05, "広島":9.78, "山口":10.15, "徳島":10.24, "香川":10.02, "愛媛":9.98, "高知":10.05, "福岡":10.11, "佐賀":10.55, "長崎":10.06, "熊本":10.08, "大分":10.08, "宮崎":9.77, "鹿児島":10.13, "沖縄":9.44};
const RATES_FY2026 = { kaigo: 0.0162, kodomo: 0.0023, pension: 0.183, koyo: 0.005 };
// 健康保険 grade (1-50) for a monthly pay amount.
function healthGrade(pay) { let g = 0; while (g + 1 < GRADES.length && pay >= GRADES[g + 1][1]) g++; return g + 1; }
const healthStd = pay => GRADES[healthGrade(pay) - 1][0];
// 厚生年金 uses health grades 4 (88,000) to 35 (650,000) as its grades 1-32.
const pensionStd = pay => Math.min(650000, Math.max(88000, healthStd(pay)));
// Deducted from pay: 50銭以下は切り捨て、50銭を超える場合は切り上げ (footnote of the 保険料額表).
const roundDeduction = x => { const f = Math.floor(x); return x - f > 0.5 + 1e-9 ? f + 1 : f; };
// pay: monthly pay incl. commuting and overtime (for 標準報酬, normally the April-June average); healthRate: e.g. 0.0985 (東京).
function premiums(pay, { healthRate, age40to64 = false, koyo = true, rates = RATES_FY2026 } = {}) {
  const hs = healthStd(pay), ps = pensionStd(pay);
  const health = roundDeduction(hs * (healthRate + (age40to64 ? rates.kaigo : 0)) / 2);
  const kodomo = roundDeduction(hs * rates.kodomo / 2);
  const pension = roundDeduction(ps * rates.pension / 2);
  const koyoAmt = koyo ? roundDeduction(pay * rates.koyo) : 0;
  return { healthStd: hs, pensionStd: ps, health, kodomo, pension, koyo: koyoAmt, total: health + kodomo + pension + koyoAmt };
}
if (typeof module !== "undefined") module.exports = { HEALTH_RATE_FY2026, GRADES, healthGrade, healthStd, pensionStd, roundDeduction, premiums, RATES_FY2026 };
