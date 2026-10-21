// The Enrollment Summary's denied requests and room sizes: Get them opens the summary in a tab, the bookmarklet clicked
// there reads it and the dashboard's other quarters and sends them back, and the Quarter card and the Decade cells show them.
const fs = require('fs'), path = require('path');
const { BASE, sleep, launch, connect } = require('./harness.js');
const page = require('./fake-time-schedule.js');
const CODE = fs.readFileSync(path.join(__dirname, '..', 'bookmarklet-timeschedulemod.js'), 'utf8').slice('javascript:'.length);
/* What the card should say for CLAS in a quarter: denied requests at lecture sections, not withdrawn. */
function expected(q) {
  const rows = page.summary.rows(page.clas.page(q)).filter(r => r.type !== 'QZ' && !r.withdrawn);
  return { denied: rows.reduce((n, r) => n + r.denied, 0), sections: rows.filter(r => r.denied > 0).length,
    quiz: page.summary.rows(page.clas.page(q)).filter(r => r.type === 'QZ' && !r.withdrawn).reduce((n, r) => n + r.denied, 0) };
}
module.exports = async (check, port) => {
  const d = await launch('summary', port);
  const list = async () => (await fetch(`http://127.0.0.1:${port}/json/list`)).json();
  try {
    await d.openEmpty();
    await d.evaluate('localStorage.removeItem("tsmod-enrollment-summary")');
    await d.evaluate('$("#prefix-input").val("CLAS").trigger("change")');
    await d.waitFor('$("#course-table tbody tr td").length > 3');
    await sleep(300);
    check('before: the card waits for the summary, with Get them', (await d.evaluate('$("#stat-denied").text() + " | " + $("#dn-get").text() + " | " + $("#stat-denied-sub").text()')) === '– | Get them | From the Enrollment Summary',
      await d.evaluate('$("#stat-denied").text() + " | " + $("#dn-get").text() + " | " + $("#stat-denied-sub").text()'));

    const before = new Set((await list()).map(t => t.id));
    await d.click('#dn-get');
    let tab; for (let i = 0; i < 40 && !tab; i++) { await sleep(150); tab = (await list()).find(t => t.type === 'page' && !before.has(t.id)); }
    check('Get them opens the Enrollment Summary in a tab', !!tab && /\/sdb\/timeschd\/uwnetid\/tsstat\.asp\?QTRYR=AUT\+2026&CURRIC=CLAS#tsmod=/.test(tab.url), tab && tab.url);
    const s = await connect(tab.webSocketDebuggerUrl);
    for (let i = 0; i < 40 && !(await s.evaluate('document.readyState === "complete" && !!document.querySelector("table")').catch(() => false)); i++) await sleep(150);
    await s.send('Runtime.evaluate', { expression: CODE, userGesture: true });
    let note = '';
    for (let i = 0; i < 160 && !/Sent/.test(note); i++) { await sleep(150); note = await s.evaluate('(document.querySelector("#tsmod-notice .msg") || {}).textContent || ""').catch(() => ''); }
    check('the bookmarklet on the summary tab reads the 40 quarters and sends them', /^Sent 40 pages of the Enrollment Summary to TimeScheduleMod/.test(note), note);
    s.ws.close();

    await d.waitFor('/^\\d/.test($("#stat-denied").text())', 40);
    const e26 = expected('AUT2026');
    const card = await d.evaluate('({ v: $("#stat-denied").text(), sub: $("#stat-denied-sub").text(), btn: $("#dn-get").text(), title: $("#denied-card").attr("title") })');
    check('the card: requests denied at the lecture sections counted', card.v === String(e26.denied), { card, e26 });
    check('…at how many sections, and the quiz sections’ denials', card.sub.startsWith('at ' + e26.sections + ' section') && (!e26.quiz || card.sub.includes('+ ' + e26.quiz + ' at quiz sections')), card.sub);
    check('…its hover lists the most-denied sections, with seats and room size', /Most denied:\nCLAS \d+ [A-Z]+: \d+ denied · \d+ of \d+ seats · room holds \d+/.test(card.title), card.title);
    check('…and Get them becomes Update', card.btn === 'Update', card.btn);
    check('kept in this browser: 40 quarters of CLAS', await d.evaluate('Object.keys(JSON.parse(localStorage.getItem("tsmod-enrollment-summary"))).filter(k => /_CLAS$/.test(k)).length') === 40);

    if (process.env.SHOT) { await d.evaluate('window.scrollTo(0, 0)'); const shot = await d.send('Page.captureScreenshot', { format: 'png', clip: { x: 0, y: 0, width: 1440, height: 520, scale: 1 } }); fs.writeFileSync(path.join(__dirname, 'tmp', 'summary-card.png'), Buffer.from(shot.data, 'base64')); }
    await d.click('.view-seg [data-view=decade]');
    await d.waitFor('$("#bg-progress").is(":hidden") && !/Loading…/.test($("#period-view").text())', 200);
    await sleep(300);
    if (process.env.SHOT) { const shot = await d.send('Page.captureScreenshot', { format: 'png', captureBeyondViewport: true, clip: { x: 0, y: 0, width: 1440, height: 1500, scale: 1 } }); fs.writeFileSync(path.join(__dirname, 'tmp', 'summary-decade.png'), Buffer.from(shot.data, 'base64')); }
    const e19 = expected('AUT2019');
    const cell = await d.evaluate('$(".pv-cell[data-q=AUT2019], [data-q=AUT2019].pv-cell").first().find(".pv-dn").text()');
    check('Decade: each quarter’s cell shows its denied requests', cell.startsWith(e19.denied + ' denied'), { cell, e19 });
    await d.click('.view-seg [data-view=quarter]');

    // Opened on its own (no dashboard to send to): it says how to use it.
    await d.send('Page.navigate', { url: BASE + '/sdb/timeschd/uwnetid/tsstat.asp?QTRYR=AUT+2026&CURRIC=CLAS' });
    await d.waitFor('document.readyState === "complete" && !!document.querySelector("table")');
    await d.send('Runtime.evaluate', { expression: CODE, userGesture: true });
    await sleep(400);
    check('on the summary by itself: explains Get them', /click Get them on the dashboard's Denied requests card/.test(await d.evaluate('(document.querySelector("#tsmod-notice .msg") || {}).textContent || ""')),
      await d.evaluate('(document.querySelector("#tsmod-notice .msg") || {}).textContent || ""'));
    check('no script errors', d.errors.length === 0, d.errors);
  } finally { d.kill(); }
};
