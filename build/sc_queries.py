"""Weekly Search Console summary (in Japanese) from the owner's "Export -> CSV" download.

Usage: python3 -I build/sc_queries.py <export.zip | folder | Queries.csv ...> [--min-impr N]

Reads the CSVs that Search Console puts in its performance export (queries, pages, countries; English or Japanese
UI — the files are recognised by their header row, not by file name) and prints a short Japanese report:
  - totals, clicks/impressions per tool and per language (from the pages table)
  - top queries with a guessed language and the tool they belong to
  - queries that match no tool  -> ideas for new FAQ questions or tools
  - queries on page 1-2 with few clicks -> title / description to improve
Standard library only; nothing is sent anywhere.
PRIVACY: the export is the owner's account data. Never commit it to this public repo; read it from the session's
upload folder and keep only the conclusions (in ops/BACKLOG.md)."""
import csv, io, re, sys, unicodedata, zipfile
from pathlib import Path
from urllib.parse import urlparse

TOOLS = ["nenkin-refund", "leaving-japan", "resident-tax", "payslip", "takehome", "kanji-work", "kanji-grade"]
LANGS = ["vi", "ne", "id", "my", "en", "ja"]

# Lower-case keywords (any language) that tie a query to a tool. First match wins, in this order.
TOOL_WORDS = {
    "nenkin-refund": ["脱退一時金", "dattai", "nenkin", "年金", "pension", "lương hưu", "hoàn tiền", "lump-sum", "lump sum",
                      "पेन्सन", "pensiun", "ပင်စင်", "refund"],
    "resident-tax": ["住民税", "juminzei", "jumin", "resident tax", "thuế cư trú", "thuế thị dân", "आवासीय कर",
                     "pajak penduduk", "နေထိုင်သူအခွန်"],
    "leaving-japan": ["帰国", "出国", "leaving japan", "leave japan", "về nước", "在留カード", "residence card",
                      "thẻ cư trú", "pulang", "घर फर्क"],
    "takehome": ["手取り", "take-home", "take home", "tedori", "lương thực nhận", "gaji bersih", "源泉徴収", "所得税",
                 "income tax", "賞与", "bonus"],
    "payslip": ["給与明細", "payslip", "pay slip", "phiếu lương", "slip gaji", "तलब", "လစာ"],
    "kanji-work": ["特定技能", "tokutei", "kỹ năng đặc định", "介護", "kaigo", "vocabulary", "từ vựng"],
    "kanji-grade": ["漢字", "kanji", "hán tự", "hán việt"],
}
ID_WORDS = {"pajak", "gaji", "kerja", "cara", "berapa", "pensiun", "pulang", "jepang", "potongan", "untuk", "dan"}
VI_CHARS = set("ăâđêôơưàảãáạằẳẵắặầẩẫấậèẻẽéẹềểễếệìỉĩíịòỏõóọồổỗốộờởỡớợùủũúụừửữứựỳỷỹýỵ")

KINDS = {  # header of the first column -> table kind
    "top queries": "queries", "上位のクエリ": "queries", "クエリ": "queries",
    "top pages": "pages", "上位のページ": "pages", "ページ": "pages",
    "country": "countries", "国": "countries",
}
COLS = {"clicks": ["clicks", "クリック数"], "impr": ["impressions", "表示回数"], "ctr": ["ctr"],
        "pos": ["position", "掲載順位", "平均掲載順位"]}


def num(s):
    s = (s or "").strip().replace(",", "").rstrip("%")
    try:
        return float(s)
    except ValueError:
        return 0.0


def read_table(text):
    rows = list(csv.reader(io.StringIO(text.lstrip("﻿"))))
    if not rows:
        return None, []
    head = [h.strip().casefold() for h in rows[0]]
    kind = KINDS.get(head[0])
    if not kind:
        return None, []
    idx = {}
    for key, names in COLS.items():
        for i, h in enumerate(head):
            if h in names:
                idx[key] = i
    out = []
    for r in rows[1:]:
        if not r or not r[0].strip():
            continue
        out.append({"key": r[0].strip(), **{k: num(r[i]) if i < len(r) else 0.0 for k, i in idx.items()}})
    return kind, out


def load(paths):
    texts = []
    for p in map(Path, paths):
        if p.is_dir():
            texts += [f.read_text(encoding="utf-8-sig") for f in sorted(p.glob("*.csv"))]
        elif zipfile.is_zipfile(p):
            with zipfile.ZipFile(p) as z:
                texts += [z.read(n).decode("utf-8-sig") for n in z.namelist() if n.lower().endswith(".csv")]
        else:
            texts.append(p.read_text(encoding="utf-8-sig"))
    tables = {}
    for t in texts:
        kind, rows = read_table(t)
        if kind:
            tables.setdefault(kind, []).extend(rows)
    return tables


def guess_lang(q):
    s = unicodedata.normalize("NFC", q.casefold())
    if re.search(r"[ऀ-ॿ]", s):
        return "ne"
    if re.search(r"[က-႟]", s):
        return "my"
    if re.search(r"[぀-ヿ一-鿿]", s) and not VI_CHARS & set(s):
        return "ja"
    if VI_CHARS & set(s):
        return "vi"
    if ID_WORDS & set(re.findall(r"[a-z]+", s)):
        return "id"
    return "en"


def guess_tool(q):
    s = unicodedata.normalize("NFC", q.casefold())
    for tool, words in TOOL_WORDS.items():
        if any(w in s for w in words):
            return tool
    return None


def page_tool(url):
    parts = [p for p in urlparse(url).path.split("/") if p and p != "index.html"]
    lang = parts.pop(0) if parts and parts[0] in LANGS else "-"
    if not parts:
        return lang, "(トップ)"
    return lang, parts[0] if parts[0] in TOOLS else "(その他)"


def report(tables, min_impr=10):
    L = []
    q = sorted(tables.get("queries", []), key=lambda r: (-r.get("impr", 0), -r.get("clicks", 0)))
    pages = tables.get("pages", [])
    if not q and not pages:
        return "Search Console の CSV（クエリ/ページ）が見つかりませんでした。エクスポートした ZIP をそのまま添付してください。"
    base = pages or q
    L.append(f"## 検索の概要\n- クリック合計 {sum(r.get('clicks', 0) for r in base):.0f} / 表示回数合計 "
             f"{sum(r.get('impr', 0) for r in base):.0f}（{'ページ' if pages else 'クエリ'}表から。上位1,000行までの集計）")
    if pages:
        by_tool, by_lang = {}, {}
        for r in pages:
            lang, tool = page_tool(r["key"])
            for d, k in ((by_tool, tool), (by_lang, lang)):
                c = d.setdefault(k, [0, 0])
                c[0] += r.get("clicks", 0)
                c[1] += r.get("impr", 0)
        L.append("\n## ツール別（クリック / 表示回数）")
        L += [f"- {k}: {v[0]:.0f} / {v[1]:.0f}" for k, v in sorted(by_tool.items(), key=lambda kv: -kv[1][1])]
        L.append("\n## 言語別（クリック / 表示回数）")
        L += [f"- {k if k != '-' else '(言語なし: トップ等)'}: {v[0]:.0f} / {v[1]:.0f}" for k, v in sorted(by_lang.items(), key=lambda kv: -kv[1][1])]
    if q:
        L.append("\n## よく表示された検索語（上位15）")
        for r in q[:15]:
            L.append(f"- {r['key']} — 表示 {r.get('impr', 0):.0f}, クリック {r.get('clicks', 0):.0f}, "
                     f"順位 {r.get('pos', 0):.1f} [{guess_lang(r['key'])}, {guess_tool(r['key']) or 'どのツールにも該当なし'}]")
        none = [r for r in q if guess_tool(r["key"]) is None and r.get("impr", 0) >= min_impr]
        L.append(f"\n## どのツールにも当てはまらない検索語（表示 {min_impr} 以上）→ 新しいFAQ・ツールの候補")
        L += [f"- {r['key']} — 表示 {r.get('impr', 0):.0f} [{guess_lang(r['key'])}]" for r in none[:15]] or ["- なし"]
        weak = [r for r in q if r.get("impr", 0) >= min_impr and 0 < r.get("pos", 0) <= 20 and r.get("ctr", 0) < 2]
        L.append(f"\n## 1〜2ページ目に出ているのにクリックが少ない（表示 {min_impr} 以上・CTR 2%未満）→ タイトル・説明文の改善候補")
        L += [f"- {r['key']} — 順位 {r.get('pos', 0):.1f}, CTR {r.get('ctr', 0):.1f}% [{guess_tool(r['key']) or '-'}]"
              for r in weak[:15]] or ["- なし"]
    if tables.get("countries"):
        top = sorted(tables["countries"], key=lambda r: -r.get("impr", 0))[:8]
        L.append("\n## 国別（表示回数 上位）")
        L += [f"- {r['key']}: 表示 {r.get('impr', 0):.0f}, クリック {r.get('clicks', 0):.0f}" for r in top]
    return "\n".join(L)


def main(argv):
    min_impr = 10
    if "--min-impr" in argv:
        i = argv.index("--min-impr")
        min_impr = int(argv[i + 1])
        argv = argv[:i] + argv[i + 2:]
    if not argv:
        print(__doc__)
        return 2
    print(report(load(argv), min_impr))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
