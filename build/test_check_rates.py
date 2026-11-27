#!/usr/bin/env python3
"""Tests for build/check_rates.py on made-up page texts (no real page is stored in the repo)."""
import io, sys, tempfile, contextlib
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import check_rates as cr

JS = (Path(__file__).resolve().parent.parent / "tools" / "takehome" / "insurance.js").read_text(encoding="utf-8")
CUR = cr.read_current(JS)
fails = 0


def check(name, cond):
    global fails
    print(("ok   " if cond else "FAIL ") + name)
    fails += 0 if cond else 1


def suffix(p):
    return {"北海道": "", "東京": "都", "京都": "府", "大阪": "府"}.get(p, "県")


def run(text, *extra):
    with tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False, encoding="utf-8") as f:
        f.write(text)
    out = io.StringIO()
    with contextlib.redirect_stdout(out):
        code = cr.main(["check_rates.py", f.name, *extra])
    Path(f.name).unlink()
    return code, out.getvalue()


check("insurance.js table has 47 prefectures", len(CUR) == 47 and set(CUR) == set(cr.PREFS))

# 1. table layout with full names and %: identical → exit 0
table = "| 都道府県 | 健康保険料率 |\n|---|---|\n" + "\n".join(f"| {p}{suffix(p)} | {CUR[p]:.2f}% |" for p in cr.PREFS)
code, out = run(table)
check("identical table → exit 0", code == 0 and "All 47 rates identical" in out)

# 2. 支部 layout, full-width digits and ％, values on the next line
fw = str.maketrans("0123456789.", "０１２３４５６７８９．")
lines = "\n".join(f"{p}支部\n{format(CUR[p], '.2f').translate(fw)}％" for p in cr.PREFS)
code, out = run("令和9年3月分（4月納付分）からの保険料率\n" + lines)
check("支部 + full-width + line breaks → exit 0", code == 0)

# 3. 東京都 must not be read as 京都, 京都府 must not be lost
rates, probs = cr.parse_page("東京都 9.85% 京都府 9.89%")
check("東京都 / 京都府 read separately", rates == {"東京": 9.85, "京都": 9.89} and len(probs) == 45)
r2, _ = cr.parse_page(table.replace(f"| 京都府 | {CUR['京都']:.2f}% |", "| 京都府 | 9.99% |"))
check("東京 unchanged when 京都 changes", r2["東京"] == CUR["東京"] and r2["京都"] == 9.99)

# 4. one rate changed → exit 2 and named
code, out = run(table.replace(f"| 佐賀県 | {CUR['佐賀']:.2f}% |", "| 佐賀県 | 10.60% |"))
check("changed rate → exit 2", code == 2 and "CHANGED 佐賀: 10.55% -> 10.60%" in out)

# 5. a prefecture missing → exit 1, nothing guessed
code, out = run("\n".join(l for l in table.split("\n") if "沖縄" not in l))
check("missing prefecture → exit 1", code == 1 and "沖縄: not found" in out)

# 6. two different values for one prefecture → exit 1
code, out = run(table + "\n東京都 9.90%")
check("conflicting values → exit 1", code == 1 and "東京: two different rates" in out)

# 7. same value repeated is fine; care rate (1.62%) and years are ignored
code, out = run(table + f"\n東京支部 {CUR['東京']:.2f}%（介護保険 1.62%）\n東京 2027.04")
check("repeat + care rate + year ignored → exit 0", code == 0)

# 8. a number is never taken across another prefecture's name
rates, probs = cr.parse_page("北海道 東京 9.85%")
check("北海道 does not take 東京's rate", "北海道" not in rates and rates.get("東京") == 9.85)

# 9. --js prints a line that round-trips
code, out = run(table, "--js", "2027")
line = [l for l in out.splitlines() if l.startswith("const HEALTH_RATE_FY2027")]
check("--js line round-trips", code == 0 and len(line) == 1 and cr.read_current(line[0]) == CUR)

print("check_rates tests:", "ALL OK" if not fails else f"{fails} FAILED")
sys.exit(1 if fails else 0)
