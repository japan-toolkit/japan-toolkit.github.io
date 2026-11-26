#!/bin/sh
# Every check before a deploy, in one command. Stops at the first failure (exit 1).
# usage: sh build/check_all.sh            (from the repo root, branch `source` or a daily/ branch)
# Optional: AXE=/path/to/axe.min.js sh build/check_all.sh   also runs the accessibility check (see build/check_a11y.js).
set -e
cd "$(dirname "$0")/.."
step() { printf '\n== %s\n' "$1"; }
step "build";                 python3 build/build.py
step "calculator tests";      for t in tools/*/test_*.js; do echo "$t"; node "$t" >/dev/null; done
step "Python tool tests";     for t in build/test_*.py; do echo "$t"; python3 -I "$t" >/dev/null; done
step "check script test";     node build/test_check_pages.js
step "term check";            python3 build/check_terms.py
step "official sources";      python3 build/check_sources.py
step "links / hreflang";      python3 build/check_links.py dist
step "pages at 390px";        node build/check_pages.js dist
if [ -n "$AXE" ]; then step "accessibility"; node build/check_a11y.js dist "$AXE"; else step "accessibility: skipped (set AXE=...)"; fi
printf '\nALL CHECKS PASSED\n'
