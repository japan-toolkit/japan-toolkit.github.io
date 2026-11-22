// Accessibility check of the built site with axe-core (light + dark, 390px). Exit 1 on any violation.
// axe-core is not vendored: install it outside the repo first, e.g.
//   npm i --prefix /tmp/axe axe-core@4.10.2
//   node build/check_a11y.js dist /tmp/axe/node_modules/axe-core/axe.min.js
const { chromium } = require('playwright');
const fs = require('fs'), path = require('path');
const [root, axePath] = process.argv.slice(2);
if (!root || !axePath) { console.error('usage: node build/check_a11y.js <dist> <axe.min.js>'); process.exit(2); }
const axe = fs.readFileSync(axePath, 'utf8');
const pages = [];
(function walk(d) { for (const f of fs.readdirSync(d)) { const p = path.join(d, f); if (fs.statSync(p).isDirectory()) walk(p); else if (f === 'index.html') pages.push(p); } })(path.resolve(root));
(async () => {
  const b = await chromium.launch(); let bad = 0;
  for (const cs of ['light', 'dark']) {
    const ctx = await b.newContext({ viewport: { width: 390, height: 844 }, colorScheme: cs });
    await ctx.route(/fonts\.(googleapis|gstatic)\.com/, r => r.abort());
    for (const f of pages) {
      const p = await ctx.newPage(); await p.goto('file://' + f); await p.addScriptTag({ content: axe });
      const v = await p.evaluate(async () => (await axe.run(document, { resultTypes: ['violations'] })).violations
        .map(v => `${v.id} (${v.impact}) ×${v.nodes.length}: ${v.nodes[0].target.join(' ')}`));
      for (const x of v) { bad++; console.log(`${cs} ${path.relative(root, f)}: ${x}`); }
      await p.close();
    }
    await ctx.close();
  }
  console.log(`${pages.length} pages × 2 colour schemes: ${bad} violation(s)`);
  await b.close(); process.exit(bad ? 1 : 0);
})();
