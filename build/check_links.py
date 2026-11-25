#!/usr/bin/env python3
"""Offline link check for the built site (dist/). Stdlib only.

Checks, for every HTML page in dist/:
  1. every internal href/src (relative, root-relative or https://japan-toolkit.github.io/...) points to a file in dist/
     (a path ending in / needs index.html; #fragments must exist as id= on the target page);
  2. rel=canonical exists, is absolute and points to the page itself;
  3. hreflang alternates: each target exists, the set is reciprocal (A lists B -> B lists A), and each page lists itself;
  4. sitemap.xml: every <loc> exists in dist/, and every indexable page (has a canonical) is in the sitemap.
External links are not fetched (no network); they are only counted.

Usage: python3 build/check_links.py [dist]    exit 0 = no problems, 1 = problems found
"""
import os, re, sys
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote

SITE = "https://japan-toolkit.github.io"


class Page(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.links, self.ids, self.canonical, self.alts = [], set(), None, {}

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if a.get("id"):
            self.ids.add(a["id"])
        if tag == "a" and a.get("name"):
            self.ids.add(a["name"])
        if tag == "link":
            rel = (a.get("rel") or "").lower().split()
            if "canonical" in rel:
                self.canonical = a.get("href")
                return
            if "alternate" in rel and a.get("hreflang"):
                self.alts[a["hreflang"]] = a.get("href")
                return
        for k in ("href", "src"):
            v = a.get(k)
            if v is not None:
                self.links.append((tag, v))


def url_of(rel_file):
    """dist-relative file path -> site URL path ('vi/payslip/index.html' -> '/vi/payslip/')."""
    p = "/" + rel_file.replace(os.sep, "/")
    return p[: -len("index.html")] if p.endswith("/index.html") or p == "/index.html" else p


def resolve(dist, page_url, href):
    """Return (dist file path or None if external/skip, fragment)."""
    s = urlsplit(href)
    if s.scheme in ("mailto", "tel", "javascript", "data"):
        return None, None
    if s.scheme or s.netloc:
        if f"{s.scheme}://{s.netloc}" != SITE:
            return None, None
        path = s.path or "/"
    elif not s.path:
        path = page_url  # '#frag' only
    elif s.path.startswith("/"):
        path = s.path
    else:
        base = page_url if page_url.endswith("/") else page_url.rsplit("/", 1)[0] + "/"
        path = os.path.normpath(base + s.path).replace(os.sep, "/")
        if s.path.endswith("/") and not path.endswith("/"):
            path += "/"
    path = unquote(path)
    f = os.path.join(dist, path.lstrip("/"))
    if path.endswith("/"):
        f = os.path.join(f, "index.html")
    return f, s.fragment


def check(dist):
    problems, pages, external = [], {}, 0
    for root, _, files in os.walk(dist):
        if ".git" in root.split(os.sep):
            continue
        for fn in files:
            if fn.endswith(".html"):
                full = os.path.join(root, fn)
                p = Page()
                with open(full, encoding="utf-8") as fh:
                    p.feed(fh.read())
                pages[os.path.normpath(full)] = p
    if not pages:
        return ["no HTML pages found in " + dist], 0, 0

    for full, p in sorted(pages.items()):
        rel = os.path.relpath(full, dist)
        me = url_of(rel)
        for tag, href in p.links:
            f, frag = resolve(dist, me, href)
            if f is None:
                if urlsplit(href).scheme in ("http", "https"):
                    external += 1
                continue
            f = os.path.normpath(f)
            if not os.path.isfile(f):
                problems.append(f"{rel}: <{tag}> {href} -> missing {os.path.relpath(f, dist)}")
            elif frag and f.endswith(".html") and f in pages and frag not in pages[f].ids:
                problems.append(f"{rel}: <{tag}> {href} -> no id '{frag}' on target")
        if os.path.basename(full) == "404.html":
            continue  # 404 page is served for any path; no canonical needed
        if p.canonical:
            if not p.canonical.startswith(SITE + "/"):
                problems.append(f"{rel}: canonical not absolute on site: {p.canonical}")
            elif urlsplit(p.canonical).path != me:
                problems.append(f"{rel}: canonical {p.canonical} is not this page ({me})")
        for lang, href in p.alts.items():
            f, _ = resolve(dist, me, href)
            if f is None or not os.path.isfile(os.path.normpath(f)):
                problems.append(f"{rel}: hreflang {lang} -> missing {href}")
                continue
            other = pages.get(os.path.normpath(f))
            # x-default = the language picker; Google does not require it to link back
            if lang != "x-default" and other is not None and me not in {urlsplit(h).path for h in other.alts.values()}:
                problems.append(f"{rel}: hreflang {lang} -> {href} does not link back")
        if p.alts and me not in {urlsplit(h).path for h in p.alts.values()}:
            problems.append(f"{rel}: hreflang set does not include the page itself")

    sm = os.path.join(dist, "sitemap.xml")
    if os.path.isfile(sm):
        with open(sm, encoding="utf-8") as fh:
            locs = re.findall(r"<loc>([^<]+)</loc>", fh.read())
        in_map = set()
        for loc in locs:
            f, _ = resolve(dist, "/", loc.strip())
            if f is None or not os.path.isfile(os.path.normpath(f)):
                problems.append(f"sitemap.xml: {loc} -> missing")
            else:
                in_map.add(os.path.normpath(f))
        for full, p in pages.items():
            if p.canonical and full not in in_map:
                problems.append(f"sitemap.xml: {os.path.relpath(full, dist)} has a canonical but is not listed")
    else:
        problems.append("sitemap.xml missing")
    return problems, len(pages), external


def main():
    dist = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(__file__), "..", "dist")
    problems, n, ext = check(os.path.normpath(dist))
    for pr in problems:
        print("PROBLEM", pr)
    print(f"check_links: {n} pages, {ext} external links (not fetched), {len(problems)} problems")
    sys.exit(1 if problems else 0)


if __name__ == "__main__":
    main()
