// Runs the TimeScheduleMod tests against a fake Time Schedule: node --experimental-websocket test/run.js
// Captures the dashboard page the bookmarklet would open, serves it with made-up PHIL pages, and drives headless Chrome.
const fs = require('fs'), path = require('path');
const { TMP, startServer } = require('./harness.js');
const TESTS = ['ta', 'snapshot', 'save-problems', 'save-as', 'details', 'views', 'preload', 'series', 'notice', 'opener'];

(async () => {
  fs.mkdirSync(TMP, { recursive: true });
  // The page the bookmarklet writes into its new tab, captured by standing in for window.open.
  let html;
  global.window = { location: { href: 'https://www.washington.edu/students/timeschd/AUT2026/', pathname: '/students/timeschd/AUT2026/' }, open: () => ({ document: { write: h => (html = h), close() {} } }) };
  global.alert = m => { throw new Error('alert: ' + m); };
  eval(fs.readFileSync(path.join(__dirname, '..', 'bookmarklet-timeschedulemod.js'), 'utf8').slice('javascript:'.length));
  new Function([...html.matchAll(/<script>([\s\S]*?)<\/script>/g)].map(m => m[1]).join('\n'));   // the dashboard's script parses
  fs.writeFileSync(path.join(TMP, 'dashboard.html'), html);
  // The same, opened from a department's own page, which the dashboard loads by itself.
  global.window.location = { href: 'https://www.washington.edu/students/timeschd/AUT2026/phil.html', pathname: '/students/timeschd/AUT2026/phil.html' };
  eval(fs.readFileSync(path.join(__dirname, '..', 'bookmarklet-timeschedulemod.js'), 'utf8').slice('javascript:'.length));
  fs.writeFileSync(path.join(TMP, 'dashboard-phil.html'), html);
  const server = await startServer();
  let failed = 0, port = 9340;
  for (const name of TESTS) {
    const results = [];
    const check = (label, ok, detail) => results.push({ label, ok: !!ok, detail });
    try { await require(`./${name}.test.js`)(check, port++); }
    catch (e) { check('ran without error', false, e.message); }
    console.log(`\n${name}`);
    results.forEach(r => { if (!r.ok) failed++; console.log(`  ${r.ok ? 'PASS' : 'FAIL'}  ${r.label}${r.ok || r.detail === undefined ? '' : '  → ' + JSON.stringify(r.detail)}`); });
  }
  server.close();
  console.log(failed ? `\n${failed} failed` : '\nall passed');
  process.exit(failed ? 1 : 0);
})();
