"""Test for build/sc_queries.py with made-up Search Console exports (no real data in the repo).
Run: python3 -I build/test_sc_queries.py"""
import sys, tempfile, zipfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import sc_queries as s  # noqa: E402

EN_Q = ("﻿Top queries,Clicks,Impressions,CTR,Position\n"
        "nenkin refund calculator,12,300,4%,6.2\n"
        "thuế cư trú khi về nước,1,120,0.83%,9.5\n"
        "cara hitung pajak penduduk jepang,0,40,0%,14\n"
        "जापान पेन्सन फिर्ता,3,50,6%,4.1\n"
        "ဂျပန် လစာ အခွန်,0,15,0%,22\n"
        "手取り 計算 外国人,2,90,2.2%,11\n"
        "japan driver license exchange,0,60,0%,18\n"
        "visa renewal documents,0,5,0%,30\n")
EN_P = ("Top pages,Clicks,Impressions,CTR,Position\n"
        "https://japan-toolkit.github.io/vi/resident-tax/,1,120,0.83%,9.5\n"
        "https://japan-toolkit.github.io/en/nenkin-refund/,12,300,4%,6.2\n"
        "https://japan-toolkit.github.io/,0,20,0%,30\n"
        "https://japan-toolkit.github.io/vi/,0,10,0%,40\n"
        "https://japan-toolkit.github.io/privacy/,0,3,0%,50\n")
JA_Q = ("上位のクエリ,クリック数,表示回数,CTR,掲載順位\n"
        "脱退一時金 計算,5,200,2.5%,5\n"
        "外国人 運転免許 切り替え,0,30,0%,12\n")
JA_C = "国,クリック数,表示回数,CTR,掲載順位\nベトナム,3,400,0.75%,8\n日本,10,300,3.3%,7\n"

fails = 0


def ok(cond, msg):
    global fails
    if not cond:
        fails += 1
        print("FAIL:", msg)


# language and tool guesses
for q, lang, tool in [("nenkin refund calculator", "en", "nenkin-refund"),
                      ("thuế cư trú khi về nước", "vi", "resident-tax"),
                      ("thuế thị dân", "vi", "resident-tax"),
                      ("cara hitung pajak penduduk jepang", "id", "resident-tax"),
                      ("जापान पेन्सन फिर्ता", "ne", "nenkin-refund"),
                      ("ဂျပန် လစာ အခွန်", "my", "payslip"),
                      ("手取り 計算 外国人", "ja", "takehome"),
                      ("thẻ cư trú 在留カード", "vi", "leaving-japan"),
                      ("japan driver license exchange", "en", None)]:
    ok(s.guess_lang(q) == lang, f"lang {q!r} -> {s.guess_lang(q)} (want {lang})")
    ok(s.guess_tool(q) == tool, f"tool {q!r} -> {s.guess_tool(q)} (want {tool})")

ok(s.page_tool("https://japan-toolkit.github.io/vi/resident-tax/") == ("vi", "resident-tax"), "page vi")
ok(s.page_tool("https://japan-toolkit.github.io/") == ("-", "(トップ)"), "page root")
ok(s.page_tool("https://japan-toolkit.github.io/vi/") == ("vi", "(トップ)"), "page vi portal")
ok(s.page_tool("https://japan-toolkit.github.io/privacy/") == ("-", "(その他)"), "page privacy")

with tempfile.TemporaryDirectory() as d:
    d = Path(d)
    # English UI export as a ZIP (file names do not matter: tables are found by header)
    z = d / "export.zip"
    with zipfile.ZipFile(z, "w") as zf:
        zf.writestr("Queries.csv", EN_Q)
        zf.writestr("Pages.csv", EN_P)
        zf.writestr("Devices.csv", "Device,Clicks,Impressions,CTR,Position\nMOBILE,10,400,2.5%,9\n")
    t = s.load([z])
    ok(len(t["queries"]) == 8 and len(t["pages"]) == 5 and "countries" not in t, f"zip tables {[(k, len(v)) for k, v in t.items()]}")
    ok(t["queries"][1]["ctr"] == 0.83 and t["queries"][0]["impr"] == 300, "numbers parsed")
    r = s.report(t)
    print(r, "\n" + "-" * 40)
    ok("クリック合計 13 / 表示回数合計 453" in r, "totals from pages table")
    ok("- nenkin-refund: 12 / 300" in r and "- (トップ): 0 / 30" in r and "- (その他): 0 / 3" in r, "per tool")
    ok("- vi: 1 / 130" in r, "per language")
    none_part = r.split("新しいFAQ")[1].split("##")[0]
    ok("driver license" in none_part and "visa renewal" not in none_part, "no-tool list respects min impressions")
    weak = r.split("改善候補")[1]
    ok("thuế cư trú khi về nước" in weak and "nenkin refund" not in weak and "ဂျပန်" not in weak, "weak list (pos<=20, ctr<2)")
    # Japanese UI export as a folder of CSVs
    (d / "f").mkdir()
    (d / "f" / "クエリ.csv").write_text(JA_Q, encoding="utf-8")
    (d / "f" / "国.csv").write_text(JA_C, encoding="utf-8")
    t2 = s.load([d / "f"])
    r2 = s.report(t2, min_impr=20)
    print(r2, "\n" + "-" * 40)
    ok("クエリ表から" in r2 and "表示回数合計 230" in r2, "ja totals from queries when no pages table")
    ok("外国人 運転免許 切り替え — 表示 30 [ja]" in r2, "ja no-tool query")
    ok("- ベトナム: 表示 400, クリック 3" in r2, "countries")
    ok("見つかりませんでした" in s.report({}), "empty export message")

print("FAILED" if fails else "OK: all sc_queries tests passed", fails)
sys.exit(1 if fails else 0)
