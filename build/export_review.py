"""Export every user-facing string, side by side with English, for native-speaker review.
Usage: python3 build/export_review.py   -> ops/review/<lang>.md (vi, ne, id, my) and ops/review/ja.md
Reviewers edit the right-hand column or leave a comment; nothing here is served on the site."""
import json, re, subprocess
from pathlib import Path
REPO = Path(__file__).resolve().parent.parent
TOOLS = REPO / "tools"
OUT = REPO / "ops" / "review"
LANGS = ["vi", "ne", "id", "my", "ja"]
NAMES = {"vi": "Tiếng Việt", "ne": "नेपाली", "id": "Bahasa Indonesia", "my": "မြန်မာ", "ja": "日本語"}

def tool_T(tool):
    src = (TOOLS / tool / "index.html").read_text()
    js = src.split("<script>")[1].split("\nlet lang")[0]
    js = re.sub(r"/\*@include ([\w.-]+\.js)\*/", "", js)
    js += "\nconsole.log(JSON.stringify(T))"
    return json.loads(subprocess.run(["node", "-e", js], capture_output=True, text=True, check=True).stdout)

def flat(x, path=""):
    if isinstance(x, str):
        yield path, x
    elif isinstance(x, list):
        for i, v in enumerate(x):
            yield from flat(v, f"{path}[{i}]")
    elif isinstance(x, dict):
        for k, v in x.items():
            yield from flat(v, f"{path}.{k}" if path else k)

def cell(s):
    return re.sub(r"<[^>]+>", "", s).replace("|", "\\|").replace("\n", " ")

def main():
    OUT.mkdir(parents=True, exist_ok=True)
    tools = sorted(p.name for p in TOOLS.iterdir() if (p / "index.html").exists())
    words = json.loads(subprocess.run(["node", "-e", f"const {{WORDS}}=require({json.dumps(str(TOOLS/'kanji-work'/'words.js'))});console.log(JSON.stringify(WORDS))"],
                                      capture_output=True, text=True, check=True).stdout)
    for lang in LANGS:
        lines = [f"# Translation review: {NAMES[lang]} ({lang})", "",
                 "Please check that each sentence is correct, natural and easy to understand for a worker in Japan.",
                 "Write corrections in the last column (or open a GitHub issue). Japanese words in （） or 「」 should stay as they are.", ""]
        total = 0
        for tool in tools:
            T = tool_T(tool)
            en = dict(flat(T["en"])); tr = dict(flat(T[lang]))
            lines += [f"## {tool}", "", "| key | English | " + lang + " | correction |", "|---|---|---|---|"]
            for k, v in en.items():
                lines.append(f"| {k} | {cell(v)} | {cell(tr.get(k, '(missing)'))} | |"); total += 1
            faq = TOOLS / tool / "faq.json"
            if faq.exists():
                d = json.loads(faq.read_text())
                for i, it in enumerate(d["items"]):
                    for part in ("q", "a"):
                        lines.append(f"| faq[{i}].{part} | {cell(it['en'][part])} | {cell(it[lang][part])} | |"); total += 1
            lines.append("")
        lines += ["## kanji-work word list", "", "| word | reading | English | " + lang + " | correction |", "|---|---|---|---|---|"]
        for s, ws in words.items():
            for k, r, m in ws:
                lines.append(f"| {k} | {r} | {cell(m['en'])} | {cell(m[lang])} | |"); total += 1
        (OUT / f"{lang}.md").write_text("\n".join(lines) + "\n")
        print(lang, total, "strings")

if __name__ == "__main__":
    main()
