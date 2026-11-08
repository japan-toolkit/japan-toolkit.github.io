// Data checks for words.js: complete translations, unique answers per set (so every question has one right choice).
const { WORDS } = require("./words.js");
const LANGS = ["vi","ne","id","my","en","ja"]; let fails = 0;
const f = m => { fails++; console.log("FAIL", m); };
const all = new Set();
for (const [set, list] of Object.entries(WORDS)) {
  if (list.length < 8) f(`${set}: needs at least 8 words`);
  const readings = new Set();
  for (const [k, r, m] of list) {
    if (all.has(k)) f(`duplicate word ${k}`); all.add(k);
    if (!/^[ぁ-ゖー]+$/.test(r.replace("カード",""))) f(`${k}: reading not kana: ${r}`);
    if (readings.has(r)) f(`${set}: duplicate reading ${r}`); readings.add(r);
    for (const l of LANGS) if (!m[l] || !m[l].trim()) f(`${k}: missing ${l}`);
  }
  for (const l of LANGS) { const ms = list.map(w => w[2][l]); if (new Set(ms).size !== ms.length) f(`${set}/${l}: duplicate meanings`); }
}
console.log(fails ? `${fails} failures` : `all tests passed (${all.size} words)`); process.exit(fails ? 1 : 0);
