#!/usr/bin/env python3
"""Compare 協会けんぽ prefecture health-insurance rates in a saved page text with tools/takehome/insurance.js.

Why: new rates are announced every Feb–Mar and the official pages can only be read while the owner is present.
Save the text of the official rate page (e.g. .../rate_prefectures/r09/) to a file, then:

    python3 -I build/check_rates.py <page.txt>            # compare with HEALTH_RATE_FY2026 in insurance.js
    python3 -I build/check_rates.py <page.txt> --js 2027  # also print a ready HEALTH_RATE_FY2027 line

The text may be in any layout ("東京支部 9.85%", a table, full-width digits...). Each of the 47 prefectures must
appear with one rate (the same value repeated is fine). Exit 0 = all 47 found and identical, 2 = all found but some
differ, 1 = a prefecture is missing or has two different values (read the page again; nothing is guessed).
Standard library only; reads the files, sends nothing.
"""
import json, re, sys, unicodedata
from pathlib import Path

PREFS = ["北海道", "青森", "岩手", "宮城", "秋田", "山形", "福島", "茨城", "栃木", "群馬", "埼玉", "千葉", "東京",
         "神奈川", "新潟", "富山", "石川", "福井", "山梨", "長野", "岐阜", "静岡", "愛知", "三重", "滋賀", "京都",
         "大阪", "兵庫", "奈良", "和歌山", "鳥取", "島根", "岡山", "広島", "山口", "徳島", "香川", "愛媛", "高知",
         "福岡", "佐賀", "長崎", "熊本", "大分", "宮崎", "鹿児島", "沖縄"]
# Leftmost match wins, so "東京都" is read as 東京 (never as 京都). Between the name and the rate only a suffix,
# spaces or line breaks, separators or a short label may stand (no digits, no other prefecture), so a number is never taken
# from the next row.
NAME = "|".join(sorted(PREFS, key=len, reverse=True))
PAIR = re.compile(r"(" + NAME + r")(?:都|府|県|支部)*(?:(?!" + NAME + r")[^\d]){0,12}?(\d{1,2}\.\d{1,3})\s*[%％]?")


def read_current(js_text):
    m = re.search(r"const HEALTH_RATE_FY\d{4}\s*=\s*(\{[^}]*\})", js_text)
    if not m:
        raise SystemExit("insurance.js: HEALTH_RATE_FY#### table not found")
    return {k: float(v) for k, v in json.loads(m.group(1)).items()}


def parse_page(text):
    """Return ({pref: rate}, [problems])."""
    text = unicodedata.normalize("NFKC", text)
    found, problems = {}, []
    for m in PAIR.finditer(text):
        name = m.group(1)
        rate = float(m.group(2))
        if not 5.0 <= rate <= 15.0:
            continue  # not a health-insurance rate (e.g. a year or a care-insurance rate)
        found.setdefault(name, set()).add(rate)
    rates = {}
    for p in PREFS:
        vals = found.get(p)
        if not vals:
            problems.append(f"{p}: not found in the page text")
        elif len(vals) > 1:
            problems.append(f"{p}: two different rates {sorted(vals)}")
        else:
            rates[p] = next(iter(vals))
    return rates, problems


def compare(current, new):
    return [(p, current.get(p), new[p]) for p in PREFS if p in new and current.get(p) != new[p]]


def js_line(rates, year):
    body = ", ".join(f'"{p}":{rates[p]:.2f}' for p in PREFS)
    return f"const HEALTH_RATE_FY{year} = {{{body}}};"


def main(argv):
    if len(argv) < 2:
        print(__doc__)
        return 1
    page = Path(argv[1]).read_text(encoding="utf-8", errors="replace")
    js = Path(__file__).resolve().parent.parent / "tools" / "takehome" / "insurance.js"
    current = read_current(js.read_text(encoding="utf-8"))
    new, problems = parse_page(page)
    print(f"check_rates: {len(new)}/47 prefectures read from {argv[1]}")
    for p in problems:
        print("  PROBLEM", p)
    diffs = compare(current, new)
    for p, old, rate in diffs:
        print(f"  CHANGED {p}: {old:.2f}% -> {rate:.2f}%")
    if problems:
        print("Not all 47 rates could be read. Nothing is guessed: read the official page again.")
        return 1
    hi = max(new, key=new.get); lo = min(new, key=new.get)
    print(f"  range: {lo} {new[lo]:.2f}% (lowest) – {hi} {new[hi]:.2f}% (highest); 東京 {new['東京']:.2f}%")
    if "--js" in argv:
        print(js_line(new, argv[argv.index("--js") + 1]))
    if diffs:
        print(f"{len(diffs)} prefecture(s) differ from insurance.js. Update insurance.js, FACTS.md and the payslip range.")
        return 2
    print("All 47 rates identical to insurance.js.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
