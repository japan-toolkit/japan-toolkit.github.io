// Monthly income-tax withholding, 甲欄, by the official computer method
// (電子計算機等を使用して源泉徴収税額を計算する方法, NTA zeigakuhyo2026/2027 data/18.pdf).
// A = pay after social insurance for the month (円); deps = spouse + dependants counted (源泉控除対象).
const TAX_YEARS = {
  2026: { kyuyoMin: 54167, kyuyoMinTo: 158333, kiso0: 48334 },
  2027: { kyuyoMin: 57500, kyuyoMinTo: 169444, kiso0: 51667 },
};
function kyuyoKojo(A, y) {
  const c = TAX_YEARS[y];
  if (A <= c.kyuyoMinTo) return c.kyuyoMin;
  if (A <= 299999) return Math.ceil(A * 0.3 + 6667);
  if (A <= 549999) return Math.ceil(A * 0.2 + 36667);
  if (A <= 708330) return Math.ceil(A * 0.1 + 91667);
  return 162500;
}
function kisoKojo(A, y) {
  if (A <= 2120833) return TAX_YEARS[y].kiso0;
  if (A <= 2162499) return 40000;
  if (A <= 2204166) return 26667;
  if (A <= 2245833) return 13334;
  return 0;
}
const RATE = [[162500, 0.05105, 0], [275000, 0.10210, 8296], [579166, 0.20420, 36374], [750000, 0.23483, 54113],
  [1500000, 0.33693, 130688], [3333333, 0.40840, 237893], [Infinity, 0.45945, 408061]];
function withholdingKou(A, deps, y) {
  if (!TAX_YEARS[y]) throw new Error("unsupported year " + y);
  A = Math.floor(A);
  const B = A - kyuyoKojo(A, y) - 31667 * deps - kisoKojo(A, y);
  if (B <= 0) return 0;
  const [, r, d] = RATE.find(([max]) => B <= max);
  const tax = B * r - d;
  return tax <= 0 ? 0 : Math.round(tax / 10) * 10;   // 10円未満四捨五入
}
if (typeof module !== "undefined") module.exports = { withholdingKou, kyuyoKojo, kisoKojo, TAX_YEARS };
