#!/usr/bin/env python3
"""Tests for check_links.py on small made-up sites (temp dirs only). Run: python3 -I build/test_check_links.py"""
import os, sys, tempfile
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import check_links  # noqa: E402

S = check_links.SITE
fails = 0


def site(files):
    d = tempfile.mkdtemp()
    for rel, body in files.items():
        f = os.path.join(d, rel)
        os.makedirs(os.path.dirname(f), exist_ok=True)
        with open(f, "w", encoding="utf-8") as fh:
            fh.write(body)
    return d


def page(url, alts=(), body="", canonical=True):
    head = f'<link rel="canonical" href="{S}{url}">' if canonical else ""
    head += "".join(f'<link rel="alternate" hreflang="{l}" href="{S}{u}">' for l, u in alts)
    return f"<html><head>{head}<link rel=stylesheet href=\"https://fonts.googleapis.com/x\"></head><body>{body}</body></html>"


def smap(*urls):
    return "<urlset>" + "".join(f"<loc>{S}{u}</loc>" for u in urls) + "</urlset>"


ALTS = [("vi", "/vi/a/"), ("en", "/en/a/"), ("x-default", "/")]


def good():
    return {
        "index.html": page("/", body='<a href="vi/a/">vi</a><a href="/en/a/#faq">en</a>'),
        "vi/a/index.html": page("/vi/a/", ALTS, '<a href="../../">home</a><a href="#top" id="top">t</a><a href="mailto:x@y">m</a>'),
        "en/a/index.html": page("/en/a/", ALTS, '<h2 id="faq">FAQ</h2><a href="https://example.com/">ext</a>'),
        "404.html": "<html><body><a href=\"/\">home</a></body></html>",
        "sitemap.xml": smap("/", "/vi/a/", "/en/a/"),
    }


def expect(name, files, n_problems, needle=None):
    global fails
    probs, _, _ = check_links.check(site(files))
    ok = len(probs) == n_problems and (needle is None or any(needle in p for p in probs))
    print(("ok  " if ok else "FAIL"), name, "->", probs if not ok or probs else "0 problems")
    fails += not ok


expect("clean site", good(), 0)
f = good(); f["vi/a/index.html"] = f["vi/a/index.html"].replace('href="../../"', 'href="../b/"')
expect("missing relative target", f, 1, "missing vi/b/index.html")
f = good(); f["index.html"] = f["index.html"].replace("#faq", "#nope")
expect("missing fragment", f, 1, "no id 'nope'")
f = good(); f["en/a/index.html"] = page("/en/a/", [("en", "/en/a/")], '<h2 id="faq">F</h2>')
expect("hreflang not reciprocal", f, 1, "does not link back")
f = good(); f["vi/a/index.html"] = page("/vi/a/", ALTS + [("ja", "/ja/a/")])
expect("hreflang target missing", f, 1, "hreflang ja -> missing")
f = good(); f["en/a/index.html"] = page("/vi/a/", ALTS, '<h2 id="faq">F</h2>')
expect("canonical points elsewhere", f, 1, "is not this page")
f = good(); f["sitemap.xml"] = smap("/", "/vi/a/", "/en/a/", "/old/")
expect("sitemap loc missing", f, 1, "/old/ -> missing")
f = good(); f["sitemap.xml"] = smap("/", "/vi/a/")
expect("page not in sitemap", f, 1, "en/a/index.html has a canonical but is not listed")
f = good(); f["vi/a/index.html"] += '<img src="/img/x.png">'
expect("missing image (root-relative src)", f, 1, "missing img/x.png")
f = good(); f["vi/a/index.html"] += f'<a href="{S}/privacy/">p</a>'
expect("absolute own-site link missing", f, 1, "missing privacy/index.html")

print("test_check_links:", "OK" if not fails else f"{fails} FAILED")
sys.exit(1 if fails else 0)
