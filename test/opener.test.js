// The real path: TSMod clicked on a department's page opens its own tab, and takes that page's prefix from the page itself,
// with no second download of it (the startup lag the user saw), timed when the page loaded.
const fs = require('fs'), path = require('path');
const { launch, BASE, sleep, fetchCount, connect } = require('./harness.js');
const CODE = fs.readFileSync(path.join(__dirname, '..', 'bookmarklet-timeschedulemod.js'), 'utf8').slice('javascript:'.length)
  .split('https://www.washington.edu/students/timeschd/').join(BASE + '/students/timeschd/');
module.exports = async (check, port) => {
  const d = await launch('opener', port);
  const list = async () => (await fetch(`http://127.0.0.1:${port}/json/list`)).json();
  try {
    await d.send('Page.navigate', { url: BASE + '/students/timeschd/AUT2026/phil.html' });
    await d.waitFor('document.readyState === "complete" && /phil\\.html$/.test(location.href)');
    const before = await fetchCount(), ids = new Set((await list()).map(t => t.id));
    await d.send('Runtime.evaluate', { expression: CODE, userGesture: true });
    let target; for (let i = 0; i < 50 && !target; i++) { target = (await list()).find(t => t.type === 'page' && !ids.has(t.id)); if (!target) await sleep(100); }
    const w = await connect(target.webSocketDebuggerUrl);
    await w.send('Runtime.enable');
    let ok = false; for (let i = 0; i < 80 && !ok; i++) { ok = await w.evaluate('!!window.jQuery && $("#course-table tbody tr td").length > 3 && $(".prefix-chip").length === 1').catch(() => false); if (!ok) await sleep(150); }
    await sleep(300);
    const s = await w.evaluate('({ chips: $(".prefix-chip").text(), asof: $("#snap-asof").text(), sections: $("#stat-sec").text() })');
    check('opened from the PHIL page: PHIL is loaded', ok && /^PHIL/.test(s.chips) && +s.sections > 0, s);
    check('…from the page itself, with no second download of it', (await fetchCount()) === before, { before, after: await fetchCount() });
    check('…and its time is when that page loaded', / · as of \d/.test(s.asof), s.asof);
    await fetch(`http://127.0.0.1:${port}/json/close/${target.id}`);
  } finally { d.kill(); }
};
