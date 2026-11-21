"""Source check: every official link the site shows must be a source listed in ops/FACTS.md,
so the daily facts check re-reads everything users are sent to.
Usage: python3 build/check_sources.py [--days N]      (exit 1 if a link is not in FACTS.md)
  1. Collects every URL in tools/**/(*.html, *.js, *.json) and build/build.py.
  2. Official = a host ending in .go.jp, or kyoukaikenpo.or.jp. Other hosts (fonts, GitHub, licences) are ignored.
  3. An official link passes if FACTS.md contains the full URL, or (for a PDF) its file name, or it is a bare
     home page (path '/' only — no figure is taken from a home page).
  4. Info only (never fails): FACTS.md rows whose 'Checked' date is more than N days old (default 14)."""
import argparse, datetime, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
URL_RE = re.compile(r"https?://[^\s\"'<>()`|\\]+")
OFFICIAL_HOSTS = (".go.jp", "kyoukaikenpo.or.jp")


def host_path(url):
    m = re.match(r"https?://([^/]+)(/.*)?$", url)
    return m.group(1).lower(), (m.group(2) or "/")


def is_official(url):
    host, _ = host_path(url)
    return any(host == h.lstrip(".") or host.endswith(h) for h in OFFICIAL_HOSTS)


def site_urls(root=ROOT):
    """{url: [file, ...]} for every URL in the tools and build.py."""
    files = [p for p in (root / "tools").rglob("*") if p.suffix in (".html", ".js", ".json")]
    files.append(root / "build" / "build.py")
    found = {}
    for p in sorted(files):
        if p.name.startswith("test_"):
            continue
        for u in URL_RE.findall(p.read_text(encoding="utf-8")):
            u = u.rstrip(".,;:")
            found.setdefault(u, []).append(str(p.relative_to(root)))
    return found


def listed(url, facts):
    if url in facts:
        return True
    _, path = host_path(url)
    if path == "/":
        return True
    name = path.rsplit("/", 1)[-1]
    if name.lower().endswith(".pdf") and re.search(r"(?<![\w.])" + re.escape(name[:-4]) + r"(?:\.pdf)?(?![\w])", facts):
        return True
    return False


def unlisted(found, facts):
    return sorted(u for u in found if is_official(u) and not listed(u, facts))


def stale_rows(facts, today, days):
    """[(figure, checked_date)] for table rows whose last column is a date older than `days`."""
    out = []
    for line in facts.splitlines():
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) < 6 or not re.fullmatch(r"\d{4}-\d{2}-\d{2}", cells[-1]):
            continue
        d = datetime.date.fromisoformat(cells[-1])
        if (today - d).days > days:
            out.append((cells[0], cells[-1]))
    return out


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--days", type=int, default=14)
    a = ap.parse_args(argv)
    facts = (ROOT / "ops" / "FACTS.md").read_text(encoding="utf-8")
    found = site_urls()
    bad = unlisted(found, facts)
    official = [u for u in found if is_official(u)]
    print(f"official links on the site: {len(official)}")
    for u in bad:
        print(f"NOT IN FACTS.md: {u}  ({', '.join(sorted(set(found[u])))})")
    today = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9))).date()
    old = stale_rows(facts, today, a.days)
    if old:
        print(f"info: {len(old)} FACTS.md rows last checked more than {a.days} days ago:")
        for fig, d in old:
            print(f"  {d}  {fig}")
    print(f"{len(bad)} problem(s)")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
