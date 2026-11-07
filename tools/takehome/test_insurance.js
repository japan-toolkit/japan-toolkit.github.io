// Checks insurance.js against the official 協会けんぽ 令和8年度 保険料額表 (東京支部, R8_13tokyo.pdf), transcribed 2026-11-08.
const { GRADES, healthGrade, healthStd, pensionStd, roundDeduction, premiums } = require("./insurance.js");
let fails = 0; const eq = (l, g, e) => { if (Math.abs(g - e) > 1e-6) { fails++; console.log("FAIL", l, "expected", e, "got", g); } };
// [grade, std, 介護なし折半, 介護あり折半, 子育て支援金折半, 厚年折半 or null]
const T = [[1,58000,2856.5,3326.3,66.7,null],[4,88000,4334.0,5046.8,101.2,8052],[12,150000,7387.5,8602.5,172.5,13725],
 [17,200000,9850,11470,230,18300],[20,260000,12805,14911,299,23790],[27,410000,20192.5,23513.5,471.5,37515],
 [35,650000,32012.5,37277.5,747.5,59475],[38,750000,36937.5,43012.5,862.5,null],[50,1390000,68457.5,79716.5,1598.5,null]];
for (const [g, std, h, hk, k, p] of T) {
  eq(`grade ${g} std`, GRADES[g - 1][0], std);
  eq(`grade ${g} health`, Math.round(std * 0.0985 / 2 * 10) / 10, h);
  eq(`grade ${g} health+kaigo`, Math.round(std * (0.0985 + 0.0162) / 2 * 10) / 10, hk);
  eq(`grade ${g} kodomo`, Math.round(std * 0.0023 / 2 * 10) / 10, k);
  if (p) eq(`grade ${g} pension`, std * 0.183 / 2, p);
}
// Boundaries: 報酬月額 A～B means A以上B未満.
eq("62,999 -> g1", healthGrade(62999), 1); eq("63,000 -> g2", healthGrade(63000), 2);
eq("394,999 -> g26", healthGrade(394999), 26); eq("395,000 -> g27", healthGrade(395000), 27);
eq("1,355,000 -> g50", healthGrade(1355000), 50); eq("5,000,000 -> g50", healthGrade(5000000), 50);
eq("pension floor", pensionStd(50000), 88000); eq("pension cap", pensionStd(900000), 650000);
eq("std 260k", healthStd(255000), 260000);
// Rounding: 50銭以下切り捨て、超えたら切り上げ.
eq("2856.5", roundDeduction(2856.5), 2856); eq("3326.3", roundDeduction(3326.3), 3326); eq("66.7", roundDeduction(66.7), 67);
// Whole example: pay 255,000 in Tokyo, under 40.
const r = premiums(255000, { healthRate: 0.0985 });
eq("ex health", r.health, 12805); eq("ex kodomo", r.kodomo, 299); eq("ex pension", r.pension, 23790); eq("ex koyo", r.koyo, 1275);
const { HEALTH_RATE_FY2026: HR } = require("./insurance.js");
eq("47 prefectures", Object.keys(HR).length, 47); eq("Tokyo rate", HR["東京"], 9.85);
for (const v of Object.values(HR)) if (!(v > 9 && v < 11)) { fails++; console.log("FAIL rate out of range", v); }
console.log(fails ? `${fails} failures` : "all tests passed"); process.exit(fails ? 1 : 0);
