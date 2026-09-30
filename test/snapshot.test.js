// Saving a snapshot (download fallback, reload first, with history) and reopening the file.
const fs = require('fs'), path = require('path');
const { launch, fetchCount, snapshotIn, BASE } = require('./harness.js');
module.exports = async (check, port) => {
  const d = await launch('snapshot', port);
  const cards = () => d.evaluate(`({ sections: $("#stat-sec").text(), enrolled: $("#stat-enrl").text(), fullness: $("#stat-pct").text(), tas: $("#stat-ta").text(),
    genEds: $(".gened-filter:checked").map(function(){ return this.value; }).get().join(), level: $(".level-btn.active").text(), search: $("#course-table_filter input").val(),
    order: JSON.stringify($("#course-table").DataTable().order()), rows: $("#course-table tbody tr").slice(0, 4).map(function(){ return $(this).find("td").slice(1, 8).map(function(){ return $(this).text(); }).get().join("|"); }).get().join(" / ") })`);
  try {
    await d.openEmpty();
    check('Save disabled before any prefix', await d.evaluate('$("#snap-save").prop("disabled")'));
    await d.openWithPhil();
    check('data time shown', /^Data as of \d/.test(await d.evaluate('$("#snap-asof").text()')));
    await d.click('.gened-filter[value="NSc"]');
    await d.click('.level-btn[data-level="100"]');
    await d.click('#course-table thead th:nth-child(7)'); await d.click('#course-table thead th:nth-child(7)');
    await d.evaluate('$("#course-table_filter input").val("intro").trigger("keyup")');
    await d.evaluate('window.showSaveFilePicker = undefined');   // headless Chrome can't use the Save As dialog; test the download path
    const before = await fetchCount();
    await d.click('#snap-save');
    await d.click('.snap-picks button:first-child');
    await d.click('#snap-history');
    check('file name from quarter, prefix, time and note', /^Time Schedule AUT2026 PHIL \d{4}-\d\d-\d\d \d{4} First day of classes\.html$/.test(await d.evaluate('$("#snap-file").text()')));
    await d.click('.snap-save');
    const file = await d.downloaded();
    check('file saved', !!file, file);
    check('reloaded once before saving', (await fetchCount()) - before === 1);
    const live = await cards();
    const html = fs.readFileSync(path.join(d.downloads, file), 'utf8'), snap = snapshotIn(html);
    check('no TA names in the file', !/Assistant,/.test(html));
    check('quiz sections keep only a leader label', Object.keys(snap.quizData[0]).sort().join() === 'enrl,leader,lim,number,prefix,section,sln,src', Object.keys(snap.quizData[0]));
    const requests = [];
    await d.send('Network.enable'); d.on(m => { if (m.method === 'Network.requestWillBeSent') requests.push(m.params.request.url); });
    await d.openFile(file);
    const reopened = await cards();
    check('reopened file matches the live dashboard (numbers, filters, sort, search)', JSON.stringify(reopened) === JSON.stringify(live), { live, reopened });
    const view = await d.evaluate('({ banner: $(".snap-banner").text(), locked: !$("#prefix-input").is(":visible"), save: $("#snap-save").is(":visible"), x: $(".chip-remove:visible").length, title: document.title })');
    check('snapshot banner with the note', /^SNAPSHOTFirst day of classesAutumn 2026 · data as of /.test(view.banner), view.banner);
    check('prefixes locked, no Save, no chip ×', view.locked && !view.save && view.x === 0, view);
    check('tab title names the snapshot', view.title === 'Snapshot AUT2026 PHIL · First day of classes', view.title);
    await d.click('.switch .slider');
    await d.evaluate('$("#ts-course-select").val(["PHIL|100"]).trigger("change")');
    await d.waitFor('(document.getElementById("chart-timeseries").data || []).length > 0', 40);
    const quarters = await d.evaluate('(document.getElementById("chart-timeseries").data || [])[0].y.filter(v => v !== null).length');
    check('Time Series works from the saved history (5 quarters)', quarters === 5, quarters);
    check('the file never contacts the Time Schedule', requests.filter(u => u.startsWith(BASE)).length === 0, requests.filter(u => u.startsWith(BASE)));
    check('no script errors', d.errors.length === 0, d.errors);
  } finally { d.kill(); }
};
