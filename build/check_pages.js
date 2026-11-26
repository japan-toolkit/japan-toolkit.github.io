// Render check of the built site: serves <dist> over local HTTP and opens every page at 390px with Playwright.
// Fails (exit 1) on: HTTP status != 200, a JS error (pageerror or console.error), horizontal scroll,
// an empty <title> or <h1>. Requests to Google Fonts are blocked (the sandbox cannot reach them; not a page error).
// usage: node build/check_pages.js dist
const { chromium } = require('playwright');
const http = require('http'), fs = require('fs'), path = require('path');
const root = process.argv[2];
if (!root) { console.error('usage: node build/check_pages.js <dist>'); process.exit(2); }
const base = path.resolve(root);
const TYPES = { '.html': 'text/html; charset=utf-8', '.js': 'text/javascript', '.css': 'text/css', '.json': 'application/json',
  '.xml': 'application/xml', '.txt': 'text/plain', '.svg': 'image/svg+xml', '.png': 'image/png', '.ico': 'image/x-icon' };
const pages = [];
(function walk(d) {
  for (const f of fs.readdirSync(d).sort()) {
    const p = path.join(d, f);
    if (fs.statSync(p).isDirectory()) { if (f !== '.git') walk(p); }
    else if (f === 'index.html') pages.push('/' + path.relative(base, d).split(path.sep).filter(Boolean).map(s => s + '/').join(''));
  }
})(base);

const server = http.createServer((req, res) => {
  let u = decodeURIComponent(req.url.split('?')[0].split('#')[0]);
  let f = path.join(base, u);
  if (!f.startsWith(base)) { res.writeHead(403); return res.end(); }
  if (fs.existsSync(f) && fs.statSync(f).isDirectory()) f = path.join(f, 'index.html');
  if (!fs.existsSync(f)) { res.writeHead(404); return res.end('not found'); }
  res.writeHead(200, { 'content-type': TYPES[path.extname(f)] || 'application/octet-stream' });
  fs.createReadStream(f).pipe(res);
});

server.listen(0, '127.0.0.1', async () => {
  const origin = `http://127.0.0.1:${server.address().port}`;
  const b = await chromium.launch();
  const ctx = await b.newContext({ viewport: { width: 390, height: 844 } });
  await ctx.route(/fonts\.(googleapis|gstatic)\.com/, r => r.abort());
  let bad = 0;
  for (const u of pages) {
    const p = await ctx.newPage(), errs = [];
    p.on('pageerror', e => errs.push('pageerror: ' + e.message));
    p.on('console', m => { if (m.type() === 'error' && !/fonts\.(googleapis|gstatic)|ERR_FAILED/.test(m.text() + (m.location().url || ''))) errs.push('console: ' + m.text()); });
    p.on('requestfailed', r => { if (!/fonts\.(googleapis|gstatic)\.com/.test(r.url())) errs.push('request failed: ' + r.url()); });
    p.on('response', r => { if (r.url().startsWith(origin) && r.status() >= 400) errs.push(`HTTP ${r.status()}: ${r.url().slice(origin.length)}`); });
    const r = await p.goto(origin + u, { waitUntil: 'load' });
    if (!r || r.status() !== 200) errs.push('status ' + (r && r.status()));
    await p.waitForTimeout(150);
    const info = await p.evaluate(() => ({
      sw: document.documentElement.scrollWidth, cw: document.documentElement.clientWidth,
      title: document.title.trim(), h1: (document.querySelector('h1') || {}).textContent || '' }));
    if (info.sw > info.cw) errs.push(`horizontal scroll: scrollWidth ${info.sw} > ${info.cw}`);
    if (!info.title) errs.push('empty <title>');
    if (!info.h1.trim()) errs.push('no <h1> text');
    for (const e of errs) console.log(`${u}: ${e}`);
    if (errs.length) bad++;
    await p.close();
  }
  console.log(`${pages.length} pages at 390px: ${bad} with problems`);
  await b.close(); server.close(); process.exit(bad || !pages.length ? 1 : 0);
});
