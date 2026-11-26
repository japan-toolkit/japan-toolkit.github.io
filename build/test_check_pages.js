// Test for build/check_pages.js on a small made-up site: one clean page and one page per problem type.
// usage: node build/test_check_pages.js
const fs = require('fs'), path = require('path'), os = require('os');
const { execFileSync } = require('child_process');
const d = fs.mkdtempSync(path.join(os.tmpdir(), 'check-pages-'));
const page = (dir, body, head = '<title>T</title>') => {
  fs.mkdirSync(path.join(d, dir), { recursive: true });
  fs.writeFileSync(path.join(d, dir, 'index.html'),
    `<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">${head}</head><body>${body}</body></html>`);
};
page('', '<h1>Root</h1>');
page('ok', '<h1>OK</h1><p>fine</p><script>document.querySelector("p").textContent = "still fine"</script>');
page('jserror', '<h1>E</h1><script>undefinedFunction()</script>');
page('consoleerror', '<h1>C</h1><script>console.error("boom")</script>');
page('wide', '<h1>W</h1><div style="width:600px">too wide</div>');
page('missingjs', '<h1>M</h1><script src="/nope.js"></script>');
page('notitle', '<h1>N</h1>', '');
page('noh1', '<p>no heading</p>');
let out = '', code = 0;
try { out = execFileSync('node', [path.join(__dirname, 'check_pages.js'), d], { encoding: 'utf8' }); }
catch (e) { out = e.stdout; code = e.status; }
const expect = { '/jserror/': 'pageerror', '/consoleerror/': 'console: boom', '/wide/': 'horizontal scroll',
  '/missingjs/': 'HTTP 404', '/notitle/': 'empty <title>', '/noh1/': 'no <h1>' };
let fail = 0;
const check = (ok, msg) => { if (!ok) { fail++; console.log('FAIL ' + msg); } };
check(code === 1, 'exit code 1 expected, got ' + code);
for (const [u, s] of Object.entries(expect)) check(out.split('\n').some(l => l.startsWith(u + ':') && l.includes(s)), `${u} should report "${s}"`);
check(!out.split('\n').some(l => l.startsWith('/ok/:') || l.startsWith('/:')), 'clean pages must not be reported');
check(out.includes('8 pages at 390px: 6 with problems'), 'summary line');
fs.rmSync(d, { recursive: true, force: true });
if (fail) { console.log(out); process.exit(1); }
console.log('check_pages test OK (8 pages, 6 problem types caught, clean pages pass)');
