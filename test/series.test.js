// Background reading of the other quarters, and the AY and summer time series, against the made-up CLAS pages.
const { launch, BASE, sleep } = require('./harness.js');
const page = require('./fake-time-schedule.js');
module.exports = async (check, port) => {
  const d = await launch('series', port);
  const options = () => d.evaluate('$("#ts-course-select option").map(function(){ return $(this).text(); }).get()');
  const series = () => d.evaluate('(() => { const t = (document.getElementById("chart-timeseries").data || [])[0]; return t ? { x: t.x, y: t.y, name: t.name } : null; })()');
  try {
    await fetch(BASE + '/__clasdelay?ms=120');
    await d.openEmpty();
    await d.evaluate('$("#prefix-input").val("CLAS").trigger("change")');
    await d.waitFor('$("#course-table tbody tr td").length > 3');
    await d.click('#excl-bar .excl-yes');
    await d.click('.view-seg [data-view=decade]');
    await sleep(300);
    check('a view that needs pages not read yet shows the progress bar', await d.evaluate('$("#bg-progress").is(":visible") && /^Reading the last ten years from the Time Schedule: \\d+ of \\d+ pages$/.test($("#bg-status").text())'), await d.evaluate('$("#bg-status").text()'));
    await d.click('.view-seg [data-view=quarter]');
    check('the Quarter view never shows it', await d.evaluate('$("#bg-progress").is(":hidden")'));
    await fetch(BASE + '/__clasdelay?ms=0');
    await d.waitFor('/ of (\\d+) pages$/.test($("#bg-status").text()) && false', 1);   // nothing to wait on in Quarter: reading goes on behind it
    await sleep(6000);
    await d.click('.view-seg [data-view=summers]');
    await sleep(150);
    check('read in the background meanwhile: Summers opens with no progress bar', await d.evaluate('$("#bg-progress").is(":hidden") && $(".pv-stable tbody tr").length === 10 && !/Loading/.test($("#period-view").text())'));

    await d.click('.view-seg [data-view=ayseries]');
    await d.waitFor('!$("#ts-course-select").prop("disabled") && $("#ts-course-select option").length > 0');
    const ay = await options();
    check('AY time series lists whole courses from the whole decade, with when an old one was last taught', JSON.stringify(ay) === JSON.stringify(['CLAS 101 - LATIN AND GREEK IN CURRENT USE', 'CLAS 210 - GREEK AND ROMAN MYTHOLOGY', 'CLAS 320 - GREEK PHILOSOPHY', 'CLAS 330 - GREEK TRAGEDY · last taught Spr 2019']), ay);
    check('excluded courses aren’t offered', !ay.some(o => /484/.test(o)));
    await d.evaluate('$("#ts-course-select").val(["CLAS|101"]).trigger("change")');
    await d.waitFor('(document.getElementById("chart-timeseries").data || []).length > 0');
    let s = await series();
    const aut19 = page.clas.sections('AUT2019')[0].enrl;
    check('AY time series: 30 quarters, no summers', s.x.length === 30 && !s.x.some(x => /^SUM/.test(x)) && s.x[0] === 'WIN 2017' && s.x[29] === 'AUT 2026', s.x);
    check('the course’s enrollment per quarter', s.y[s.x.indexOf('AUT 2019')] === aut19 && s.name === 'CLAS 101 - Enrl', { y: s.y[s.x.indexOf('AUT 2019')], want: aut19, name: s.name });
    await d.click('#ts-inst-none');
    s = await series();
    check('Clear unchecks every instructor', s.y.every(v => v === null));
    await d.click('#ts-inst-all');

    await d.click('.view-seg [data-view=sumseries]');
    await d.waitFor('!$("#ts-course-select").prop("disabled") && $("#ts-course-select option").length > 0');
    const sum = await options();
    check('Summer time series lists summer courses only', JSON.stringify(sum) === JSON.stringify(['CLAS 101 - LATIN AND GREEK IN CURRENT USE']), sum);
    await d.evaluate('$("#ts-course-select").val(["CLAS|101"]).trigger("change")');
    await d.waitFor('(document.getElementById("chart-timeseries").data || []).length > 0 && document.getElementById("chart-timeseries").data[0].x.length === 10');
    s = await series();
    check('Summer time series: the ten summers only', s.x.length === 10 && s.x.every(x => /^SUM/.test(x)) && s.y[s.x.indexOf('SUM 2019')] === page.clas.sections('SUM2019')[0].enrl, s);
    check('no script errors', d.errors.length === 0, d.errors);
  } finally { d.kill(); await fetch(BASE + '/__clasdelay?ms=0').catch(() => {}); }
};
