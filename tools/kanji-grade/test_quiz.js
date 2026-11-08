// Tests for the school-grade kanji quiz: data shape and that every question has exactly one right answer.
const { KANJI, KANJIDIC_VERSION } = require("./kanji.js");
const Q = require("./quiz.js"); Q.setKanji(KANJI);
let fails = 0; const f = m => { fails++; console.log("FAIL", m); };
// Data: 1,026 教育漢字 split 80/160/200/202/193/191 (学年別漢字配当表, 2020).
const byGrade = [1,2,3,4,5,6].map(g => KANJI.filter(r => r[1] === g).length);
if (KANJI.length !== 1026) f("expected 1026 kanji, got " + KANJI.length);
if (byGrade.join() !== "80,160,200,202,193,191") f("grade counts " + byGrade.join());
for (const r of KANJI) { if (!r[5].length) f(r[0] + " no meaning"); if (!r[3].length && !r[4].length) f(r[0] + " no reading"); }
if (!/^\d{4}-\d+$/.test(KANJIDIC_VERSION.database_version)) f("version");
// Display helpers.
if (Q.showReading("ひと.つ") !== "ひと(つ)") f("showReading okurigana");
if (Q.showReading("-ひと") !== "ひと") f("showReading dash");
if (Q.readingKey("ショウ") !== "しょう") f("readingKey");
// Every question, many seeds: 4 distinct options, exactly one is the answer, and no distractor is a valid reading/meaning.
let seed = 1; const rnd = () => (seed = (seed * 16807) % 2147483647) / 2147483647;
let built = 0;
for (const mode of ["reading", "meaning", "viet"]) for (let g = 1; g <= 6; g++) {
  const pool = KANJI.filter(r => r[1] === g);
  for (const row of pool) for (let k = 0; k < 3; k++) {
    const q = Q.makeQuestion(row, pool, mode, rnd); if (!q) { f(`no question ${mode} ${row[0]}`); continue; } built++;
    if (q.options.length !== 4 || new Set(q.options).size !== 4) f(`options ${mode} ${row[0]} ${q.options}`);
    if (q.options.filter(o => o === q.answer).length !== 1) f(`answer count ${mode} ${row[0]}`);
    if (mode === "reading") {
      const own = new Set([...row[3], ...row[4]].map(Q.readingKey));
      for (const o of q.options) if (o !== q.answer && own.has(Q.readingKey(o))) f(`distractor is a real reading: ${row[0]} ${o}`);
    }
  }
}
for (let g = 1; g <= 6; g++) for (const mode of ["reading", "meaning", "viet"]) {
  const r = Q.makeRound(g, mode, 10, rnd); if (r.length !== 10 || new Set(r.map(q => q.row[0])).size !== 10) f(`round ${g} ${mode}`);
}
console.log(fails ? `${fails} failures` : `all tests passed (${built} questions checked, data ${KANJIDIC_VERSION.database_version})`);
process.exit(fails ? 1 : 0);
