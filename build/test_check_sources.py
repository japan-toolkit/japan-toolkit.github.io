"""Tests for build/check_sources.py (made-up facts text; no network)."""
import datetime, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import check_sources as cs  # noqa: E402

n = 0


def ok(cond, msg):
    global n
    n += 1
    if not cond:
        print("FAIL:", msg)
        sys.exit(1)


FACTS = """| a | 1 | t | https://www.nenkin.go.jp/x/page.html | — | 2026-11-17 |
| b | 2 | t | leaflets ja 000679117 / en 000679118 .pdf | — | 2026-10-01 |
| c | 3 | t | https://www.mhlw.go.jp/content/001672589.pdf | — | 2026-11-20 |
"""
ok(cs.is_official("https://www.nta.go.jp/a.htm"), "nta official")
ok(cs.is_official("https://www.kyoukaikenpo.or.jp/"), "kyoukaikenpo official")
ok(not cs.is_official("https://fonts.googleapis.com/css2"), "fonts not official")
ok(not cs.is_official("https://evil.go.jp.example.com/"), "lookalike host not official")
ok(not cs.is_official("https://github.com/x"), "github not official")
ok(cs.listed("https://www.nenkin.go.jp/x/page.html", FACTS), "exact URL listed")
ok(not cs.listed("https://www.nenkin.go.jp/x/other.html", FACTS), "other page not listed")
ok(cs.listed("https://www.soumu.go.jp/main_content/000679118.pdf", FACTS), "pdf by file name")
ok(not cs.listed("https://www.soumu.go.jp/main_content/000679119.pdf", FACTS), "different pdf number")
ok(not cs.listed("https://www.soumu.go.jp/main_content/00067911.pdf", FACTS), "prefix of a number is not a match")
ok(cs.listed("https://www.mhlw.go.jp/", FACTS), "home page passes")
ok(not cs.listed("https://www.mhlw.go.jp/new/page.html", FACTS), "non-home page on same host fails")
found = {"https://www.nta.go.jp/new.htm": ["tools/x/index.html"], "https://fonts.googleapis.com/a": ["t"],
         "https://www.nenkin.go.jp/x/page.html": ["t"]}
ok(cs.unlisted(found, FACTS) == ["https://www.nta.go.jp/new.htm"], "unlisted finds only the new official link")
old = cs.stale_rows(FACTS, datetime.date(2026, 11, 22), 14)
ok(old == [("b", "2026-10-01")], f"stale rows: {old}")
# Real site: every official link is in FACTS.md
real = cs.unlisted(cs.site_urls(), (cs.ROOT / "ops" / "FACTS.md").read_text(encoding="utf-8"))
ok(real == [], f"real site unlisted: {real}")
print(f"check_sources test OK ({n} checks)")
