// A reload that meets a signed-out Time Schedule saves nothing; a snapshot without history says so in Time Series.
const fs = require('fs');
const { launch, fetchCount, toggleSignedOut, BASE } = require('./harness.js');
module.exports = async (check, port) => {
  const d = await launch('problems', port);
  try {
    await d.openWithPhil();
    await d.evaluate('window.showSaveFilePicker = undefined');
    const enrolled = await d.evaluate('$("#stat-enrl").text()');
    await toggleSignedOut();
    await d.click('#snap-save');
    await d.evaluate('$("#snap-note").val("10th day").trigger("input")');
    await d.click('.snap-save');
    await d.waitFor('$("#snap-status").hasClass("err")', 20);
    const s = await d.evaluate('({ status: $("#snap-status").text(), open: $("#snap-dialog").length === 1, enabled: !$(".snap-save").prop("disabled") })');
    await toggleSignedOut();
    check('signed out: says so and saves nothing', s.status === 'The Time Schedule sent no sections for PHIL. You may need to sign in again. Nothing was saved.' && fs.readdirSync(d.downloads).length === 0, s);
    check('signed out: dialog stays open to try again', s.open && s.enabled, s);
    check('signed out: the live numbers are kept', (await d.evaluate('$("#stat-enrl").text()')) === enrolled);
    await d.click('#snap-reload');
    const before = await fetchCount();
    await d.click('.snap-save');
    const file = await d.downloaded();
    check('without reload: nothing is fetched', (await fetchCount()) === before);
    const requests = [];
    await d.send('Network.enable'); d.on(m => { if (m.method === 'Network.requestWillBeSent') requests.push(m.params.request.url); });
    await d.openFile(file);
    await d.click('.view-seg [data-view=series]');
    await d.evaluate('$("#ts-course-select").val(["PHIL|100"]).trigger("change")');
    await d.waitFor('(document.getElementById("chart-timeseries").data || []).length > 0', 40);
    const t = await d.evaluate('({ note: $(".snap-nohist").text(), quarters: (document.getElementById("chart-timeseries").data || [])[0].y.filter(v => v !== null).length })');
    check('without history: Time Series explains it has this quarter only', t.note === 'This snapshot didn’t save the 10-year history, so Time Series shows Autumn 2026 only.' && t.quarters === 1, t);
    check('without history: no requests to the Time Schedule', requests.filter(u => u.startsWith(BASE)).length === 0);
    check('no script errors', d.errors.length === 0, d.errors);
  } finally { d.kill(); }
};
