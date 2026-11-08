// Bonus (賞与) deductions: social insurance on the 標準賞与額 and income tax by the 算出率の表 (甲欄).
// Needs bonus_table.js and insurance.js (roundDeduction, RATES_FY2026).
// Sources: nenkin.go.jp 20141203 (標準賞与額 = 1,000円未満切捨て; 厚生年金 上限 150万円/月; 健康保険 年度累計 573万円),
// NTA zeigakuhyo 15-16.pdf (table) and 19-22.pdf (残額 × 率, 1円未満切捨て; 月額表 method if no prior-month pay or bonus > 10×).
const BONUS_PENSION_CAP = 1500000, BONUS_HEALTH_CAP = 5730000;
function bonusRate(prevNet, deps, year) {
  const t = BONUS_TABLE[String(year)]; if (!t) throw new Error("no bonus table for " + year);
  const d = Math.min(7, Math.max(0, deps));
  for (let i = 0; i < t.rates.length; i++) { const up = t.upper[i][d]; if (up === null || prevNet < up) return t.rates[i]; }
  return t.rates[t.rates.length - 1];
}
// bonus: gross bonus (yen). prevNet: last month's pay after social insurance, excluding non-taxable commuting allowance.
// healthBefore: 標準賞与額 already counted for health insurance this fiscal year (default 0).
function bonusDeductions(bonus, { prevNet, deps = 0, year, healthRate, age40to64 = false, koyo = true, healthBefore = 0, rates = RATES_FY2026 }) {
  bonus = Math.max(0, Math.floor(bonus));
  const std = Math.floor(bonus / 1000) * 1000;
  const stdH = Math.max(0, Math.min(std, BONUS_HEALTH_CAP - healthBefore)), stdP = Math.min(std, BONUS_PENSION_CAP);
  const health = roundDeduction(stdH * (healthRate + (age40to64 ? rates.kaigo : 0)) / 2);
  const kodomo = roundDeduction(stdH * rates.kodomo / 2);
  const pension = roundDeduction(stdP * rates.pension / 2);
  const koyoAmt = koyo ? roundDeduction(bonus * rates.koyo) : 0;
  const ins = health + kodomo + pension + koyoAmt, base = bonus - ins;
  // Outside the table's scope the company uses the 月額表 method; we do not estimate that case.
  const special = !(prevNet > 0) || base > 10 * prevNet;
  const rate = special ? null : bonusRate(prevNet, deps, year);
  const tax = special ? null : Math.floor(base * rate / 100 + 1e-9);
  return { std, stdH, stdP, health, kodomo, pension, koyo: koyoAmt, ins, rate, tax, special, net: special ? null : bonus - ins - tax };
}
if (typeof module !== "undefined") module.exports = { bonusRate, bonusDeductions, BONUS_PENSION_CAP, BONUS_HEALTH_CAP };
