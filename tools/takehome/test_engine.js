// Tests the income-tax engine against the official 令和9年分 月額表 甲欄 (NTA zeigakuhyo2027/data/01-07.pdf),
// rows transcribed 2026-11-08. Run: node tools/takehome/test_engine.js
const { withholdingKou } = require("./engine.js");
let fails = 0;
const check = (label, got, exp, tol) => { if (Math.abs(got - exp) > tol) { fails++; console.log("FAIL", label, "expected", exp, "got", got); } };

// 1) Bands up to 602,000: the table is built at the band's midpoint, so the computer method must match within 10 yen.
const BANDS = [
  [149000, 151000, [2080, 470, 0, 0]],
  [179000, 181000, [3450, 1840, 220, 0]],
  [199000, 201000, [4170, 2550, 940, 0]],
  [248000, 251000, [5940, 4320, 2710, 1090]],
  [299000, 302000, [7760, 6150, 4530, 2910]],
  [368000, 371000, [12860, 9630, 7350, 5730]],
  [449000, 452000, [19480, 16240, 13020, 9780]],
  [599000, 602000, [44720, 38250, 31780, 25320]],
];
for (const [lo, hi, exp] of BANDS) exp.forEach((e, d) => check(`${lo}-${hi} deps=${d}`, withholdingKou((lo + hi) / 2, d, 2027), e, 10));

// 2) Table rows at 740,000 (all columns) and, with no dependants, 960,000 and 3,500,000: within 150 yen.
//    Above 740,000 the table adds dependants at a flat step (about 6,460 yen each), while the computer method
//    deducts 31,667 yen per person at the marginal rate, so with dependants the two legally differ. Not tested.
[71000, 64540, 58060, 51600].forEach((e, d) => check(`740000 deps=${d}`, withholdingKou(740000, d, 2027), e, 150));
check("960000 deps=0", withholdingKou(960000, 0, 2027), 121130, 150);
check("3500000 deps=0", withholdingKou(3500000, 0, 2027), 1125240, 150);

// 3) Under 111,000 yen the table gives 0; the computer method gives at most about 100 yen here (legal difference).
for (const A of [88000, 105000, 110000]) for (let d = 0; d < 4; d++) check(`${A} deps=${d}`, withholdingKou(A, d, 2027), 0, 100);

// 4) 2026 vs 2027: the 2027 deductions are larger, so tax never goes up.
for (let A = 50000; A <= 3000000; A += 7000) for (let d = 0; d < 4; d++)
  if (withholdingKou(A, d, 2027) > withholdingKou(A, d, 2026)) { fails++; console.log("FAIL 2027>2026 at", A, d); }

console.log(fails ? `${fails} failures` : "all tests passed");
process.exit(fails ? 1 : 0);
