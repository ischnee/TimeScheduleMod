// Opened from a department's page (…/AUT2026/phil.html), the dashboard starts with that prefix loaded; a snapshot saved
// from it reopens without fetching.
const { launch, BASE, sleep } = require('./harness.js');
module.exports = async (check, port) => {
  const d = await launch('preload', port);
  try {
    await d.send('Page.navigate', { url: BASE + '/dash-phil' });
    const loaded = await d.waitFor('!!window.jQuery && $("#course-table tbody tr td").length > 3 && $(".prefix-chip").length === 1');
    await sleep(300);
    const s = await d.evaluate('({ chips: $(".prefix-chip").text(), hint: $("#prefix-hint").text(), input: $("#prefix-input").val(), enrolled: $("#stat-enrl").text() })');
    check('PHIL is loaded without typing', loaded && /^PHIL/.test(s.chips) && s.hint === '1 active prefix' && s.input === '', s);
    await d.openEmpty();
    await sleep(500);
    check('opened from the quarter’s main page: nothing preloaded', (await d.evaluate('$(".prefix-chip").length')) === 0);
    await d.send('Page.navigate', { url: BASE + '/dash-phil' });
    await d.waitFor('!!window.jQuery && $("#course-table tbody tr td").length > 3');
    await sleep(300);
    await d.evaluate('window.showSaveFilePicker = undefined');
    await d.click('#snap-save');
    await d.click('#snap-reload');
    await d.click('.snap-save');
    const file = await d.downloaded();
    const requests = [];
    await d.send('Network.enable'); d.on(m => { if (m.method === 'Network.requestWillBeSent') requests.push(m.params.request.url); });
    await d.openFile(file);
    await sleep(500);
    check('its snapshot reopens with PHIL and never fetches', (await d.evaluate('$(".prefix-chip").length')) === 1 && requests.filter(u => u.startsWith(BASE)).length === 0, requests.filter(u => u.startsWith(BASE)));
    check('no script errors', d.errors.length === 0, d.errors);
  } finally { d.kill(); }
};
