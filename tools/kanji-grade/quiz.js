// Question builder for the school-grade kanji quiz. Pure functions, tested by test_quiz.js.
// Uses KANJI rows: [kanji, grade, strokes, on[], kun[], meaningsEn[], vietnamese[]]
const kataToHira = s => s.replace(/[ァ-ヶ]/g, c => String.fromCharCode(c.charCodeAt(0) - 0x60));
// "ひと.つ" -> "ひと(つ)", "-ひと" -> "ひと"; on'yomi stay in katakana.
function showReading(r) { const s = r.replace(/^-|-$/g, ""); const i = s.indexOf("."); return i < 0 ? s : s.slice(0, i) + "(" + s.slice(i + 1) + ")"; }
const readingKey = r => kataToHira(r.replace(/[-.()]/g, ""));
function readingSet(row) { return new Set([...row[3], ...row[4]].map(readingKey)); }
// Meanings without radical notes, at most 3.
function showMeaning(row) { const m = row[5].filter(x => !/radical/i.test(x)); return (m.length ? m : row[5]).slice(0, 3).join(", "); }
const showViet = row => row[6].join(" / ");

function shuffle(a, rnd = Math.random) { a = a.slice(); for (let i = a.length - 1; i > 0; i--) { const j = Math.floor(rnd() * (i + 1)); [a[i], a[j]] = [a[j], a[i]]; } return a; }

// Returns {row, answer, options[4]} or null when 3 safe distractors cannot be found.
function makeQuestion(row, pool, mode, rnd = Math.random) {
  let answer, cands;
  if (mode === "reading") {
    const all = [...row[3], ...row[4]]; if (!all.length) return null;
    const r = all[Math.floor(rnd() * all.length)], isOn = row[3].includes(r);
    answer = showReading(r);
    const own = readingSet(row);
    cands = pool.filter(x => x !== row).flatMap(x => isOn ? x[3] : x[4])
      .filter(x => !own.has(readingKey(x))).map(showReading);
  } else if (mode === "meaning") {
    answer = showMeaning(row);
    const ownWords = new Set(row[5].map(x => x.toLowerCase()));
    cands = pool.filter(x => x !== row && !x[5].some(m => ownWords.has(m.toLowerCase()))).map(showMeaning);
  } else if (mode === "viet") {
    if (!row[6].length) return null;
    answer = showViet(row);
    const own = new Set(row[6].map(x => x.toLowerCase()));
    cands = pool.filter(x => x !== row && x[6].length && !x[6].some(v => own.has(v.toLowerCase()))).map(showViet);
  } else return null;
  const uniq = [...new Set(cands)].filter(x => x !== answer);
  if (uniq.length < 3) return null;
  return { row, answer, options: shuffle([answer, ...shuffle(uniq, rnd).slice(0, 3)], rnd) };
}
function makeRound(grade, mode, n = 10, rnd = Math.random) {
  const pool = KANJI.filter(r => r[1] === grade), qs = [];
  for (const row of shuffle(pool, rnd)) { const q = makeQuestion(row, pool, mode, rnd); if (q) qs.push(q); if (qs.length === n) break; }
  return qs;
}
if (typeof module !== "undefined") module.exports = { kataToHira, showReading, readingKey, showMeaning, showViet, makeQuestion, makeRound, setKanji: k => { global.KANJI = k; } };
