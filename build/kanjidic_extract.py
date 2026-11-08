"""Extract 教育漢字 (KANJIDIC2 grade 1-6) into a compact JS data file.
Usage: python3 -I build/kanjidic_extract.py <kanjidic2.xml.gz> tools/kanji-grade/kanji.js  (then: node tools/kanji-grade/test_quiz.js)
Keeps only: literal, grade, strokes, on/kun readings, English meanings, Vietnamese (Hán-Việt) readings.
No SKIP codes or other contributor fields (KANJIDIC licence section 8)."""
import sys, gzip, json, xml.etree.ElementTree as ET
src, out = sys.argv[1], sys.argv[2]
with gzip.open(src, "rb") as f:
    root = ET.parse(f).getroot()
h = root.find("header")
hdr = {k: h.findtext(k) for k in ("file_version", "database_version", "date_of_creation")}
rows = []
for c in root.iter("character"):
    g = c.findtext("misc/grade")
    if not g or not g.isdigit() or not 1 <= int(g) <= 6:
        continue
    rm = c.find("reading_meaning")
    on, kun, vi, en = [], [], [], []
    if rm is not None:
        for grp in rm.findall("rmgroup"):
            for r in grp.findall("reading"):
                t = r.get("r_type")
                if t == "ja_on": on.append(r.text)
                elif t == "ja_kun": kun.append(r.text)
                elif t == "vietnam": vi.append(r.text)
            for m in grp.findall("meaning"):
                if m.get("m_lang") is None: en.append(m.text)
    rows.append([c.findtext("literal"), int(g), int(c.findtext("misc/stroke_count")), on, kun, en, vi])
rows.sort(key=lambda r: (r[1], r[2], r[0]))
with open(out, "w", encoding="utf-8") as f:
    f.write("// Kanji data from KANJIDIC2 (Electronic Dictionary Research and Development Group, EDRDG),\n")
    f.write("// https://www.edrdg.org/wiki/index.php/KANJIDIC_Project — licensed CC BY-SA 4.0\n")
    f.write("// (https://creativecommons.org/licenses/by-sa/4.0/). This extract (grades 1-6 only; literal, grade,\n")
    f.write("// strokes, on/kun readings, English meanings, Vietnamese readings) is shared under the same licence.\n")
    f.write(f"// Source file: database_version {hdr['database_version']}, created {hdr['date_of_creation']}.\n")
    f.write("// Row: [kanji, grade, strokes, on[], kun[], meaningsEn[], vietnamese[]]\n")
    f.write("const KANJIDIC_VERSION = " + json.dumps(hdr, ensure_ascii=False) + ";\n")
    f.write("const KANJI = " + json.dumps(rows, ensure_ascii=False, separators=(",", ":")) + ";\n")
    f.write('if (typeof module !== "undefined") module.exports = { KANJI, KANJIDIC_VERSION };\n')
from collections import Counter
print(hdr, len(rows), Counter(r[1] for r in rows), "no-en:", sum(1 for r in rows if not r[5]), "no-vi:", sum(1 for r in rows if not r[6]), "no-reading:", sum(1 for r in rows if not r[3] and not r[4]))
