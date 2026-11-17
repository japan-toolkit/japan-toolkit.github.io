"""Site-wide term check: the same official term must be translated the same way everywhere.
Usage: python3 build/check_terms.py      (exit 1 if a problem is found)
Reads every user-facing string (tool T tables, faq.json, kanji-work words, build.py UI) and the glossary
build/terms.json. Two checks per language:
  1. 'avoid'   — a drifted or old form appears anywhere.
  2. 'missing' — the English string mentions a concept (glossary 'en' regex) but the translation of the same
                 string does not contain the glossary term. Keys in terms.json 'skip' are exempt (with a reason)."""
import json, re, subprocess, sys, unicodedata
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import export_review as er  # noqa: E402  (tool_T, flat)
import build as b  # noqa: E402  (UI table; build() only runs under __main__)

LANGS = ["vi", "ne", "id", "my", "ja"]


def norm(s):
    s = re.sub(r"<[^>]+>", "", s)
    return unicodedata.normalize("NFC", s).casefold()


def all_strings():
    """{lang: {key: text}} for every user-facing string; en included as the reference."""
    out = {}
    tools = sorted(p.name for p in er.TOOLS.iterdir() if (p / "index.html").exists())
    for tool in tools:
        T = er.tool_T(tool)
        for lang, tab in T.items():
            for k, v in er.flat(tab):
                out.setdefault(lang, {})[f"{tool}:{k}"] = v
        faq = er.TOOLS / tool / "faq.json"
        if faq.exists():
            for i, it in enumerate(json.loads(faq.read_text())["items"]):
                for lang, qa in it.items():
                    for part in ("q", "a"):
                        out.setdefault(lang, {})[f"{tool}:faq[{i}].{part}"] = qa[part]
    words = json.loads(subprocess.run(
        ["node", "-e", f"const {{WORDS}}=require({json.dumps(str(er.TOOLS / 'kanji-work' / 'words.js'))});"
                       "console.log(JSON.stringify(WORDS))"],
        capture_output=True, text=True, check=True).stdout)
    for _set, ws in words.items():
        for kanji, _reading, m in ws:
            for lang, v in m.items():
                out.setdefault(lang, {})[f"words:{kanji}"] = v
    for key, d in b.UI.items():
        if isinstance(d, dict):
            for lang, v in d.items():
                if isinstance(v, str):
                    out.setdefault(lang, {})[f"ui:{key}"] = v
    return out


def check(strings, glossary):
    problems, uses = [], {}
    skip = glossary.get("skip", {})
    en = strings["en"]
    for concept, g in glossary["concepts"].items():
        trig = re.compile(g["en"], re.I)
        for lang in LANGS:
            terms = g[lang] if isinstance(g[lang], list) else [g[lang]]
            terms_n = [norm(t) for t in terms]
            for bad in g.get("avoid", {}).get(lang, []):
                for k, v in strings[lang].items():
                    if norm(bad) in norm(v):
                        problems.append(f"[{lang}] avoid  {concept}: '{bad}' in {k}")
            for k, v in en.items():
                if not trig.search(re.sub(r"<[^>]+>", "", v)) or k not in strings[lang]:
                    continue
                if lang == "ja" and k.startswith("words:"):
                    continue  # the Japanese gloss explains the word itself
                uses[(concept, lang)] = uses.get((concept, lang), 0) + 1
                if any(t in norm(strings[lang][k]) for t in terms_n):
                    continue
                if f"{lang}:{k}:{concept}" in skip or f"*:{k}:{concept}" in skip:
                    continue
                problems.append(f"[{lang}] missing {concept} ('{terms[0]}') in {k}: {re.sub(r'<[^>]+>', '', strings[lang][k])[:90]}")
    return problems, uses


def main():
    glossary = json.loads((Path(__file__).resolve().parent / "terms.json").read_text())
    strings = all_strings()
    problems, uses = check(strings, glossary)
    for concept in glossary["concepts"]:
        print(f"{concept}: {uses.get((concept, 'vi'), 0)} strings")
    for p in problems:
        print(p)
    print(f"{len(problems)} problem(s)")
    sys.exit(1 if problems else 0)


if __name__ == "__main__":
    main()
