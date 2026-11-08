"""Key-based application of reviewed translation fixes. Replaces whole string literals only (never substrings)."""
import json, subprocess, sys, re
S = sys.argv[1]
def getT(tool, lang, key):
    r = subprocess.run(["node", "build/get_string.js", tool, lang, key], capture_output=True, text=True)
    return json.loads(r.stdout) if r.stdout.strip() else None
def lit(s): return json.dumps(s, ensure_ascii=False)
def keep_tags(cur, fix, lang):
    if cur.startswith("<strong>") and not fix.startswith("<strong>"):
        end = "။" if lang == "my" else "।"
        i = fix.find(end)
        if i > 0: return "<strong>" + fix[:i+1] + "</strong>" + fix[i+1:]
    return fix
plans = json.load(open(sys.argv[2]))  # [{lang, section, key, fix}]
report = []
for p in plans:
    lang, sec, key, fix = p["lang"], p["section"], p["key"], p["fix"]
    if sec == "words":
        f = "tools/kanji-work/words.js"; s = open(f).read()
        m = re.search(r'\["' + re.escape(key) + r'","[^"]*",\{[^}]*\}\]', s)
        if not m: report.append(("MISS", p)); continue
        entry = m.group(0)
        old = re.search(lang + r':("[^"]*")', entry).group(1)
        new_entry = entry.replace(lang + ":" + old, lang + ":" + lit(fix), 1)
        s = s.replace(entry, new_entry, 1); open(f, "w").write(s); report.append(("OK", key)); continue
    cur = getT(sec, lang, key)
    if cur is None: report.append(("NOKEY", p)); continue
    fix = keep_tags(cur, fix, lang)
    f = f"tools/{sec}/faq.json" if key.startswith("faq[") else f"tools/{sec}/index.html"
    s = open(f).read(); o = lit(cur); n = lit(fix)
    c = s.count(o)
    if c == 0: report.append(("MISS", p, o[:60])); continue
    s = s.replace(o, n); open(f, "w").write(s); report.append(("OK" if c == 1 else f"OKx{c}", sec, key))
print(json.dumps([r for r in report if r[0] != "OK"], ensure_ascii=False, indent=0)[:3000])
print("ok:", sum(1 for r in report if r[0].startswith("OK")), "of", len(report))
