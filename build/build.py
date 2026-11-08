"""Build the static multilingual site for https://japan-toolkit.github.io/ from the tool pages."""
import json, re, shutil, html, subprocess
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
ROOT = REPO / "tools"
OUT = REPO / "dist"
BASE = "https://japan-toolkit.github.io"
LANGS = ["vi", "ne", "id", "my", "en", "ja"]
LANG_NAMES = {"vi": "Tiếng Việt", "ne": "नेपाली", "id": "Bahasa Indonesia", "my": "မြန်မာ", "en": "English", "ja": "日本語"}
TOOLS = ["takehome", "nenkin-refund", "leaving-japan", "resident-tax", "payslip"]

# Google Search Console: the owner pastes the code from the "HTML tag" method into this file
# (just the content="..." value, or the whole <meta> tag). Empty or missing file = no tag.
GSC_FILE = REPO / "ops" / "google-site-verification.txt"

def gsc_meta():
    if not GSC_FILE.exists():
        return ""
    raw = "\n".join(l for l in GSC_FILE.read_text().splitlines() if not l.strip().startswith("#")).strip()
    if not raw:
        return ""
    m = re.search(r'content="([^"]+)"', raw)
    code = m.group(1) if m else raw
    assert re.fullmatch(r"[A-Za-z0-9_-]{20,100}", code), f"unexpected verification code in {GSC_FILE}: {code!r}"
    return f'<meta name="google-site-verification" content="{code}">'

SHORT = {
 "nenkin-refund": {"vi":"Tính tiền nenkin hoàn lại","ne":"नेन्किन फिर्ता क्याल्कुलेटर","id":"Kalkulator pengembalian nenkin","my":"နန်ကင်ပြန်အမ်းငွေ တွက်စက်","en":"Nenkin refund calculator","ja":"脱退一時金の計算機"},
 "leaving-japan": {"vi":"Việc cần làm trước khi về nước","ne":"जापान छोड्नुअघिको चेकलिस्ट","id":"Daftar periksa sebelum pulang","my":"မထွက်ခွာမီ စစ်ဆေးစာရင်း","en":"Leaving Japan checklist","ja":"帰国前チェックリスト"},
 "takehome": {"vi":"Tính lương thực nhận","ne":"हातमा आउने तलब क्याल्कुलेटर","id":"Kalkulator gaji bersih","my":"လက်ထဲရောက်လစာ တွက်စက်","en":"Take-home pay calculator","ja":"手取り計算機"},
 "resident-tax": {"vi":"Thuế cư trú khi về nước","ne":"जापान छोड्दा आवासीय कर","id":"Pajak penduduk saat pulang","my":"ပြန်ချိန် နေထိုင်သူအခွန်","en":"Resident tax when leaving","ja":"帰国時の住民税"},
 "payslip": {"vi":"Đọc phiếu lương","ne":"तलब विवरण बुझ्ने तरिका","id":"Baca slip gaji","my":"လစာစာရွက် ဖတ်နည်း","en":"Pay slip reader","ja":"給与明細の読み方"},
}
UI = {
 "tagline": {"vi":"Công cụ miễn phí cho người nước ngoài làm việc tại Nhật","ne":"जापानमा काम गर्ने विदेशीहरूका लागि निःशुल्क उपकरण","id":"Alat gratis untuk orang asing yang bekerja di Jepang","my":"ဂျပန်တွင် အလုပ်လုပ်သော နိုင်ငံခြားသားများအတွက် အခမဲ့ ကိရိယာများ","en":"Free tools for foreigners working in Japan","ja":"日本で働く外国人のための無料ツール"},
 "intro": {"vi":"Không cần đăng ký. Số liệu bạn nhập chỉ ở trên thiết bị của bạn.","ne":"दर्ता गर्नु पर्दैन। तपाईंले लेखेका अंकहरू तपाईंकै उपकरणमा मात्र रहन्छन्।","id":"Tanpa pendaftaran. Angka yang Anda masukkan hanya tersimpan di perangkat Anda.","my":"စာရင်းသွင်းရန် မလိုပါ။ သင်ထည့်သော ကိန်းဂဏန်းများသည် သင့်စက်ပေါ်တွင်သာ ရှိပါသည်။","en":"No sign-up. The numbers you type stay on your own device.","ja":"登録不要。入力した数字はあなたの端末の中だけで使われます。"},
 "more": {"vi":"Công cụ khác","ne":"अन्य उपकरण","id":"Alat lainnya","my":"အခြားကိရိယာများ","en":"More tools","ja":"ほかのツール"},
 "privacy": {"vi":"Chính sách bảo mật","ne":"गोपनीयता नीति","id":"Kebijakan privasi","my":"ကိုယ်ရေးအချက်အလက် မူဝါဒ","en":"Privacy policy","ja":"プライバシーポリシー"},
}

# Reset the artifact host used to provide, so standalone pages render the same.
RESET = """<style>:root{padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}body{margin:0;font-size:14px;font-family:system-ui,sans-serif}img{max-width:100%}[hidden]{display:none!important}
.site-nav{max-width:760px;margin:0 auto;padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px));padding-block:0 40px;display:flex;flex-direction:column;gap:10px;font-size:14px}
.site-nav h2{font-size:15px;margin:0}.site-nav ul{list-style:none;margin:0;padding:0;display:flex;flex-wrap:wrap;gap:8px}
.site-nav a{color:inherit}.site-nav li a{display:inline-block;border:1px solid currentColor;border-radius:999px;padding:5px 12px;text-decoration:none;opacity:.8}
.site-nav .legal{font-size:12px;opacity:.7}
.site-faq{max-width:760px;margin:0 auto;padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px));padding-block:0 28px;display:flex;flex-direction:column;gap:8px}
.site-faq h2{font-size:20px;margin:0 0 4px}.site-faq details{border:1px solid currentColor;border-color:color-mix(in srgb,currentColor 25%,transparent);border-radius:12px;padding:12px 14px}
.site-faq summary{cursor:pointer;font-weight:600}.site-faq p{margin:8px 0 0;opacity:.85}</style>"""

def meta_for(tool):
    """Read each language's title and lede straight from the tool's translation table."""
    src = (ROOT / tool / "index.html").read_text()
    js = src.split("<script>")[1].split("let lang")[0]
    js += "console.log(JSON.stringify(Object.fromEntries(Object.entries(T).map(([k,v])=>[k,{title:v.title,lede:v.lede}]))))"
    return json.loads(subprocess.run(["node", "-e", js], capture_output=True, text=True, check=True).stdout)

def head(lang, title, desc, path, extra=""):
    alts = "".join(f'<link rel="alternate" hreflang="{l}" href="{BASE}/{l}/{path}">' for l in LANGS)
    alts += f'<link rel="alternate" hreflang="x-default" href="{BASE}/">'
    return (f'<!doctype html><html lang="{lang}"><head><meta charset="utf-8">'
            f'<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">'
            f'<title>{html.escape(title)}</title><meta name="description" content="{html.escape(desc)}">'
            f'<link rel="canonical" href="{BASE}/{lang}/{path}">{alts}'
            f'<meta property="og:title" content="{html.escape(title)}"><meta property="og:description" content="{html.escape(desc)}">'
            f'{RESET}{extra}</head>')

def nav(lang, current):
    items = "".join(f'<li><a href="../{t}/">{SHORT[t][lang]}</a></li>' for t in TOOLS if t != current)
    return (f'<nav class="site-nav"><h2>{UI["more"][lang]}</h2><ul>{items}</ul>'
            f'<a class="legal" href="/privacy/">{UI["privacy"][lang]}</a></nav>')

def faq_html(tool, lang):
    """Optional tools/<tool>/faq.json -> visible FAQ (<details>) + FAQPage JSON-LD. Plain text only."""
    f = ROOT / tool / "faq.json"
    if not f.exists():
        return ""
    data = json.loads(f.read_text())
    items = [it[lang] for it in data["items"]]
    assert all(it["q"].strip() and it["a"].strip() for it in items), (tool, lang)
    ld = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": it["q"], "acceptedAnswer": {"@type": "Answer", "text": it["a"]}} for it in items]}
    rows = "".join(f'<details><summary>{html.escape(it["q"])}</summary><p>{html.escape(it["a"])}</p></details>' for it in items)
    return (f'<section class="site-faq" id="faq"><h2>{html.escape(data["heading"][lang])}</h2>{rows}</section>'
            f'<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False).replace("</", "<\\/")}</script>')

def build_tool(tool):
    src = (ROOT / tool / "index.html").read_text()
    # /*@include file.js*/ pulls a tested module (same folder) into the page, so tests and page share one copy.
    src = re.sub(r"/\*@include ([\w.-]+\.js)\*/", lambda m: (ROOT / tool / m.group(1)).read_text(), src)
    meta = meta_for(tool)
    top, rest = src.split('<div class="wrap">', 1)
    top = re.sub(r"<title>.*?</title>\s*", "", top)
    top = re.sub(r'<meta name="claude:viewport-fit-sides"[^>]*>\s*', "", top)
    body = '<div class="wrap">' + rest
    # Per-language URL: language comes from the page, and switching navigates to the sibling URL.
    body, n1 = re.subn(r'try\{\s*const s=localStorage\.getItem\("\w+-lang"\); if\(T\[s\]\) lang=s;\s*\}catch\(e\)\{\}', "lang=window.__LANG;", body)
    body, n2 = re.subn(r'\$\("lang"\)\.addEventListener\("change",e=>\{', f'$("lang").addEventListener("change",e=>{{location.href="../../"+e.target.value+"/{tool}/";return;', body)
    body, n3 = re.subn(r'<div class="brand">Japan Practical Toolkit</div>', '<a class="brand" href="../" style="text-decoration:none">Japan Practical Toolkit</a>', body)
    assert (n1, n2, n3) == (1, 1, 1), (tool, n1, n2, n3)
    for lang in LANGS:
        m = meta[lang]
        page = (head(lang, f'{m["title"]} | Japan Practical Toolkit', m["lede"], f"{tool}/", top)
                + f'<body><script>window.__LANG="{lang}";</script>' + body + faq_html(tool, lang) + nav(lang, tool) + "</body></html>")
        d = OUT / lang / tool
        d.mkdir(parents=True, exist_ok=True)
        (d / "index.html").write_text(page)

PORTAL_CSS = """<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,600;12..96,800&family=Be+Vietnam+Pro:wght@400;500;600&family=Noto+Sans+Devanagari:wght@400;600&family=Noto+Sans+Myanmar:wght@400;600&family=Noto+Sans+JP:wght@400;600&display=swap">
<style>
:root{--bg:#f3f5f4;--surface:#fff;--ink:#14231f;--muted:#5a6b66;--line:#d7dfdc;--accent:#0f6b5c;--accent-soft:#dcefea;
--display:"Bricolage Grotesque","Be Vietnam Pro","Noto Sans Devanagari","Noto Sans Myanmar","Noto Sans JP",system-ui,sans-serif;
--body:"Be Vietnam Pro","Noto Sans Devanagari","Noto Sans Myanmar","Noto Sans JP",system-ui,sans-serif}
@media (prefers-color-scheme:dark){:root{--bg:#0f1715;--surface:#16211e;--ink:#e4ece9;--muted:#9aaba6;--line:#2a3a36;--accent:#5cc4ae;--accent-soft:#1d3631;color-scheme:dark}}
body{background:var(--bg);color:var(--ink);font-family:var(--body);font-size:15px;line-height:1.65}
html:lang(my) body{line-height:1.95}
.wrap{max-width:760px;margin:0 auto;padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px));padding-block:32px 40px;display:flex;flex-direction:column;gap:22px}
.brand{font-family:"Bricolage Grotesque",sans-serif;font-weight:600;letter-spacing:.04em;text-transform:uppercase;font-size:12px;color:var(--muted)}
h1{font-family:var(--display);font-weight:800;font-size:clamp(26px,5vw,40px);line-height:1.2;margin:0;text-wrap:balance}
p{margin:0;color:var(--muted)}
.cards{display:flex;flex-direction:column;gap:12px}
.card{display:block;background:var(--surface);border:1px solid var(--line);border-radius:14px;padding:18px;text-decoration:none;color:inherit}
.card:hover,.card:focus-visible{border-color:var(--accent);outline:none}
.card b{display:block;font-size:17px;color:var(--accent)}
.card span{color:var(--muted);font-size:14px}
.langs{display:flex;flex-wrap:wrap;gap:8px}
.langs a{border:1px solid var(--line);background:var(--surface);border-radius:999px;padding:6px 14px;color:var(--ink);text-decoration:none;font-size:14px}
.langs a[aria-current]{background:var(--accent);border-color:var(--accent);color:var(--surface)}
footer{font-size:12.5px;color:var(--muted)} footer a{color:var(--accent)}
</style>"""

def lang_links(cur, prefix):
    return '<div class="langs">' + "".join(
        f'<a href="{prefix}{l}/" lang="{l}"{" aria-current=\"page\"" if l == cur else ""}>{LANG_NAMES[l]}</a>' for l in LANGS) + "</div>"

def build_portals():
    metas = {t: meta_for(t) for t in TOOLS}
    for lang in LANGS:
        cards = "".join(f'<a class="card" href="{t}/"><b>{SHORT[t][lang]}</b><span>{metas[t][lang]["lede"]}</span></a>' for t in TOOLS)
        page = (head(lang, f'{UI["tagline"][lang]} | Japan Practical Toolkit', UI["intro"][lang], "", PORTAL_CSS)
                + f'<body><div class="wrap"><div class="brand">Japan Practical Toolkit</div>{lang_links(lang, "../")}'
                + f'<div><h1>{UI["tagline"][lang]}</h1><p style="margin-top:8px">{UI["intro"][lang]}</p></div>'
                + f'<div class="cards">{cards}</div><footer><a href="/privacy/">{UI["privacy"][lang]}</a></footer></div></body></html>')
        (OUT / lang).mkdir(parents=True, exist_ok=True)
        (OUT / lang / "index.html").write_text(page)
    # Root: language chooser with the tagline in every language (no auto-redirect).
    rows = "".join(f'<a class="card" href="{l}/" lang="{l}"><b>{LANG_NAMES[l]}</b><span>{UI["tagline"][l]}</span></a>' for l in LANGS)
    root = (head("en", "Japan Practical Toolkit", "Free tools in Vietnamese, Nepali, Indonesian, Burmese, English and Japanese for foreigners working in Japan.", "", gsc_meta() + PORTAL_CSS).replace(f'<link rel="canonical" href="{BASE}/en/">', f'<link rel="canonical" href="{BASE}/">')
            + f'<body><div class="wrap"><div class="brand">Japan Practical Toolkit</div><h1>Japan Practical Toolkit</h1><div class="cards">{rows}</div>'
            + '<footer><a href="/privacy/">Privacy policy / プライバシーポリシー</a></footer></div></body></html>')
    (OUT / "index.html").write_text(root)

PRIVACY = """<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Privacy policy | Japan Practical Toolkit</title><link rel="canonical" href="https://japan-toolkit.github.io/privacy/">""" + PORTAL_CSS + """
<style>h2{font-family:var(--display);font-size:19px;margin:8px 0 0}ul{margin:0;padding-left:20px;color:var(--muted)}</style></head><body><div class="wrap">
<a class="brand" href="/" style="text-decoration:none">Japan Practical Toolkit</a>
<h1>Privacy policy</h1>
<p>Last updated: November 2026</p>
<ul>
<li>The tools run entirely in your browser. The numbers you type are not sent to or stored on any server.</li>
<li>Your browser may remember your language choice and checklist progress on your own device (local storage). You can clear this at any time in your browser settings.</li>
<li>We do not use cookies, accounts or tracking at this time. If we add analytics or advertising in the future, we will update this page first.</li>
<li>The tools give estimates and general information, not legal, tax or financial advice. Please confirm with the official office concerned.</li>
<li>Contact: open an issue at <a href="https://github.com/japan-toolkit/japan-toolkit.github.io/issues">GitHub</a>.</li>
</ul>
<h2 lang="ja">プライバシーポリシー（日本語）</h2>
<ul lang="ja">
<li>各ツールはブラウザの中だけで動作します。入力した数字がサーバーに送信・保存されることはありません。</li>
<li>言語の選択やチェックリストの進み具合は、あなたの端末のブラウザ（ローカルストレージ）に保存されることがあります。ブラウザの設定からいつでも削除できます。</li>
<li>現在、Cookie・アカウント・アクセス解析は使用していません。今後アクセス解析や広告を導入する場合は、事前に本ページを更新します。</li>
<li>本サイトの情報は目安・一般情報であり、法律・税務・金融の助言ではありません。最終的には各公的機関でご確認ください。</li>
<li>お問い合わせ：<a href="https://github.com/japan-toolkit/japan-toolkit.github.io/issues">GitHub</a> の Issue からご連絡ください。</li>
</ul></div></body></html>"""

def build_misc():
    (OUT / "privacy").mkdir(parents=True, exist_ok=True)
    (OUT / "privacy" / "index.html").write_text(PRIVACY)
    urls = [f"{BASE}/", f"{BASE}/privacy/"] + [f"{BASE}/{l}/" for l in LANGS] + [f"{BASE}/{l}/{t}/" for l in LANGS for t in TOOLS]
    (OUT / "sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + "".join(f"  <url><loc>{u}</loc><lastmod>2026-11-07</lastmod></url>\n" for u in urls) + "</urlset>\n")
    (OUT / "robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {BASE}/sitemap.xml\n")
    (OUT / "404.html").write_text('<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Page not found | Japan Practical Toolkit</title><meta http-equiv="refresh" content="0; url=/"></head><body><a href="/">Japan Practical Toolkit</a></body></html>')
    (OUT / ".nojekyll").write_text("")
    return len(urls)

if __name__ == "__main__":
    shutil.rmtree(OUT, ignore_errors=True)
    OUT.mkdir(parents=True)
    for t in TOOLS:
        build_tool(t)
    build_portals()
    n = build_misc()
    print("pages in sitemap:", n)
