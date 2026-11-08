// Tests for bonus.js against the NTA 算出率の表 and the worked example in zeigakuhyo2027/data/19-22.pdf.
global.BONUS_TABLE = (new Function(require("fs").readFileSync(__dirname + "/bonus_table.js", "utf8") + ";return BONUS_TABLE"))();
Object.assign(global, require("./insurance.js"));
const { bonusRate, bonusDeductions } = require("./bonus.js");
let fails = 0; const eq = (l, g, e) => { if (g !== e) { fails++; console.log("FAIL", l, "expected", e, "got", g); } };
// Table shape: 21 rows, 8 columns, upper bounds strictly increasing down each column, last row open.
for (const y of ["2026", "2027"]) {
  const t = BONUS_TABLE[y]; eq(y + " rows", t.rates.length, 21);
  for (let d = 0; d < 8; d++) { for (let i = 1; i < 20; i++) if (!(t.upper[i][d] > t.upper[i - 1][d])) eq(`${y} col ${d} row ${i} increasing`, false, true); eq(`${y} last open ${d}`, t.upper[20][d], null); }
}
// Worked example (令和9年分, p.22): bonus 554,000, 社会保険料等 85,593, prior month 196,616, 2 people -> 2.042%, tax 9,564.
eq("example rate", bonusRate(196616, 2, 2027), 2.042);
eq("example tax", Math.floor((554000 - 85593) * 2.042 / 100 + 1e-9), 9564);
// Boundaries: 0人 2027: under 87,000 -> 0%, 87,000 -> 2.042%, 100,000 -> 4.084%; 7人以上 column for 9 people.
eq("86,999", bonusRate(86999, 0, 2027), 0); eq("87,000", bonusRate(87000, 0, 2027), 2.042); eq("100,000", bonusRate(100000, 0, 2027), 4.084);
eq("2026 82,000", bonusRate(82000, 0, 2026), 2.042); eq("9 people", bonusRate(320000, 9, 2027), 2.042);
eq("top", bonusRate(5000000, 0, 2027), 45.945);
// Insurance on a bonus: 300,500 yen in Tokyo, under 40 -> 標準賞与額 300,000.
const r = bonusDeductions(300500, { prevNet: 200000, deps: 0, year: 2027, healthRate: 0.0985 });
eq("std", r.std, 300000); eq("health", r.health, 14775); eq("kodomo", r.kodomo, 345); eq("pension", r.pension, 27450);
eq("koyo", r.koyo, 1502); // 300,500 × 0.5% = 1,502.5 -> 50銭以下切捨て
eq("rate", r.rate, 4.084); eq("tax", r.tax, Math.floor((300500 - r.ins) * 0.04084 + 1e-9));
// Caps: pension 1,500,000 per month, health 5,730,000 per fiscal year.
const big = bonusDeductions(2000000, { prevNet: 600000, deps: 0, year: 2027, healthRate: 0.0985 });
eq("pension cap", big.stdP, 1500000); eq("pension amt", big.pension, 137250);
const late = bonusDeductions(1000000, { prevNet: 600000, year: 2027, healthRate: 0.0985, healthBefore: 5000000 });
eq("health cap rest", late.stdH, 730000);
// Out of scope: no prior-month pay, or bonus after insurance > 10× prior month.
eq("no prior pay", bonusDeductions(300000, { prevNet: 0, year: 2027, healthRate: 0.0985 }).special, true);
eq("over 10x", bonusDeductions(3000000, { prevNet: 100000, year: 2027, healthRate: 0.0985 }).special, true);
console.log(fails ? `${fails} failures` : "all tests passed"); process.exit(fails ? 1 : 0);
