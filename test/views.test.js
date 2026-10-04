// Year, Decade and Summers, the view buttons, and courses excluded everywhere, against the made-up CLAS pages
// (fake-time-schedule.js), whose sections the expected numbers are added up from.
const { launch, sleep } = require('./harness.js');
const page = require('./fake-time-schedule.js');
const QN = { WIN: 0, SPR: 1, SUM: 2, AUT: 3 };
/* What a quarter should show with these courses left out, and optionally one level only. */
function expect(q, out, level) {
  const secs = page.clas.sections(q).filter(s => !out.includes(s.number) && (!level || s.number[0] === level[0]));
  const enrl = secs.reduce((n, s) => n + s.enrl, 0), lim = secs.reduce((n, s) => n + s.lim, 0), tas = secs.some(s => s.quizzes) ? 2 : 0;
  return { sections: secs.length, enrl, lim, pct: (enrl / lim * 100).toFixed(1) + '%', tas };
}
const cell = e => `${e.enrl} enrolled | of ${e.lim} seats · ${e.pct} full | ${e.sections} ${e.sections === 1 ? 'section' : 'sections'} · ${e.tas} ${e.tas === 1 ? 'TA' : 'TAs'}`;
module.exports = async (check, port) => {
  const d = await launch('views', port);
  const settle = async () => { await d.waitFor('$("#bg-progress").is(":hidden") && !/Loading…/.test($("#period-view").text())', 120); await sleep(300); };
  const cells = () => d.evaluate('$(".pv-table tbody tr").map(function(){ return [[$(this).find("th").text()].concat($(this).find("td").map(function(){ return this.innerText.trim().replace(/\\n+/g, " | "); }).get())]; }).get()');
  const cards = sel => d.evaluate(`$(${JSON.stringify(sel)} + " .pv-card .pv-v").map(function(){ return $(this).text(); }).get().join(" / ")`);
  try {
    await d.openEmpty();
    await d.evaluate('$("#prefix-input").val("CLAS").trigger("change")');
    await d.waitFor('$("#course-table tbody tr td").length > 3');
    await sleep(300);
    const head = await d.evaluate('({ links: $(".dashboard-links").length, text: $(".dashboard-header").text(), views: $(".view-seg button").map(function(){ return $(this).text(); }).get().join(","), asofInButton: $("#snap-save #snap-asof").length === 1 && / · as of /.test($("#snap-asof").text()) })');
    check('the All Departments and CAS links are gone', head.links === 0 && !/All Departments|CAS Curriculum/.test(head.text), head);
    check('view buttons: Quarter, Year, Decade, AY time series, Summers, Summer time series', head.views === 'Quarter,Year,Decade,AY time series,Summers,Summer time series', head.views);
    check('the data time sits inside Save snapshot', head.asofInButton, head);

    check('CLAS 484 suggested as independent study', /Look like independent study: CLAS 484/.test(await d.evaluate('$("#excl-bar").text()')), await d.evaluate('$("#excl-bar").text()'));
    await d.click('#excl-bar .excl-yes');
    check('excluded everywhere after one click', (await d.evaluate('$("#excl-bar").text()')).startsWith('Excluded everywhere:CLAS 484×'), await d.evaluate('$("#excl-bar").text()'));
    const aut26 = expect('AUT2026', ['484']);
    check('and left out of this quarter’s cards', (await d.evaluate('$("#stat-enrl").text() + " " + $("#stat-sec").text()')) === aut26.enrl + ' ' + aut26.sections, await d.evaluate('$("#stat-enrl").text() + " " + $("#stat-sec").text()'));

    await d.click('.view-seg [data-view=year]');
    await settle();
    const y26 = await d.evaluate('({ head: $(".pv-year h2").text(), cols: $(".pv-col h2").map(function(){ return $(this).text(); }).get(), na: $(".pv-col .pv-na").map(function(){ return $(this).text(); }).get() })');
    check('Year opens on 2026–27, with only Autumn published', /^2026–27 1 of 3 quarters$/.test(y26.head) && y26.cols[0] === 'Autumn 2026 this quarter' && y26.na.join() === 'Not published yet,Not published yet', y26);
    check('the quarter view’s numbers carry into Year', (await cards('.pv-col[data-q=AUT2026]')) === [aut26.sections, aut26.enrl, aut26.lim, aut26.pct, aut26.tas].join(' / '), await cards('.pv-col[data-q=AUT2026]'));
    check('the Year button shows the year, with a caret', (await d.evaluate('$(".view-seg [data-view=year]").text()')) === '2026–27▾', await d.evaluate('$(".view-seg [data-view=year]").text()'));
    await d.click('.view-seg [data-view=year]');
    check('clicked again, it opens the ten years', (await d.evaluate('$("#pv-yearmenu button").map(function(){ return $(this).text(); }).get().join(",")')) === '2026–27,2025–26,2024–25,2023–24,2022–23,2021–22,2020–21,2019–20,2018–19,2017–18');
    await d.click('#pv-yearmenu [data-year="2019"]');
    check('picking one switches the year and closes the menu', (await d.evaluate('$(".view-seg [data-view=year]").text() + " " + $("#pv-yearmenu").length')) === '2019–20▾ 0');
    await settle();
    const q19 = ['AUT2019', 'WIN2020', 'SPR2020'].map(q => expect(q, ['484']));
    const yr = { sections: q19.reduce((n, e) => n + e.sections, 0), enrl: q19.reduce((n, e) => n + e.enrl, 0), lim: q19.reduce((n, e) => n + e.lim, 0), tas: 6 };
    check('2019–20 totals: three quarters added up, TAs as TA-quarters', (await cards('.pv-year')) === [yr.sections, yr.enrl, yr.lim, (yr.enrl / yr.lim * 100).toFixed(1) + '%', yr.tas].join(' / '), { got: await cards('.pv-year'), yr });
    check('2019–20 columns: each quarter’s own numbers', (await cards('.pv-col[data-q=WIN2020]')) === [q19[1].sections, q19[1].enrl, q19[1].lim, q19[1].pct, 2].join(' / '), await cards('.pv-col[data-q=WIN2020]'));
    check('each column has its Enrolled vs Capacity chart', (await d.evaluate('$(".pv-col .pv-chart").filter(function(){ return (this.data || []).length > 0; }).length')) === 3);

    await d.click('.view-seg [data-view=decade]');
    await settle();
    let rows = await cells();
    check('Decade: ten academic years, newest first', rows.length === 10 && rows[0][0].startsWith('2026–27') && rows[9][0].startsWith('2017–18'), rows.map(r => r[0]));
    check('Decade: an unpublished quarter says so', rows[0][2] === 'Not published yet' && rows[0][3] === 'Not published yet', rows[0]);
    const r19 = rows.find(r => r[0].startsWith('2019–20'));
    check('Decade: each quarter with every number', JSON.stringify(r19.slice(1, 4)) === JSON.stringify(q19.map(cell)), { got: r19.slice(1, 4), want: q19.map(cell) });
    check('Decade: the year column adds them up, in TA-quarters', r19[4] === `${yr.enrl} enrolled | of ${yr.lim} seats · ${(yr.enrl / yr.lim * 100).toFixed(1)}% full | ${yr.sections} sections · 6 TA-quarters`, r19[4]);
    await d.click('.pv-table td[data-q=WIN2020]');
    await settle();
    check('clicking a quarter opens its year, with that quarter marked', (await d.evaluate('$(".view-seg .on").text() + " " + $(".pv-col.pv-focus").attr("data-q")')) === '2019–20▾ WIN2020', await d.evaluate('$(".view-seg .on").text() + " " + $(".pv-col.pv-focus").attr("data-q")'));

    await d.click('.view-seg [data-view=summers]');
    await settle();
    rows = await cells();
    const s26 = expect('SUM2026', ['484']), s19 = expect('SUM2019', ['484']);
    check('Summers: ten summers, newest first', rows.length === 10 && rows[0][0] === '2026' && rows[9][0] === '2017', rows.map(r => r[0]));
    check('Summers: every number per summer', rows[0][1] === cell(s26), { got: rows[0][1], want: cell(s26) });
    check('Summers: the newest opens beside the list', (await d.evaluate('$(".pv-sdetail h2").text()')) === 'Summer 2026' && (await cards('.pv-sdetail')) === [s26.sections, s26.enrl, s26.lim, s26.pct, 0].join(' / '), await cards('.pv-sdetail'));
    await d.click('.pv-stable th[data-summer="2019"]');
    check('clicking a summer shows it', (await d.evaluate('$(".pv-sdetail h2").text()')) === 'Summer 2019' && (await cards('.pv-sdetail')).startsWith(s19.sections + ' / ' + s19.enrl + ' / '), await cards('.pv-sdetail'));

    await d.click('.view-seg [data-view=quarter]');
    await d.evaluate('$("#course-table").DataTable().search("CLAS 320").draw()');
    await d.click('#course-table tbody tr:first-child .sec-toggle');
    check('unchecking a course’s only section excludes it everywhere', /CLAS 320×/.test(await d.evaluate('$("#excl-bar").text()')), await d.evaluate('$("#excl-bar").text()'));
    await d.evaluate('$("#course-table").DataTable().search("").draw()');
    await d.click('.view-seg [data-view=decade]');
    await settle();
    rows = await cells();
    check('…and from every quarter in Decade', rows.find(r => r[0].startsWith('2019–20'))[1] === cell(expect('AUT2019', ['484', '320'])), rows.find(r => r[0].startsWith('2019–20'))[1]);
    await d.click('#excl-bar [data-course="CLAS 320"]');
    rows = await cells();
    check('× brings it back everywhere', rows.find(r => r[0].startsWith('2019–20'))[1] === cell(q19[0]) && !/CLAS 320/.test(await d.evaluate('$("#excl-bar").text()')), rows.find(r => r[0].startsWith('2019–20'))[1]);
    await d.click('.view-seg [data-view=quarter]');
    await d.click('.level-btn[data-level="100"]');
    await d.click('.view-seg [data-view=decade]');
    await settle();
    rows = await cells();
    check('"Count only: 100-level" carries into every quarter', rows.find(r => r[0].startsWith('2019–20'))[1] === cell(expect('AUT2019', ['484'], '100')), rows.find(r => r[0].startsWith('2019–20'))[1]);
    await d.click('.view-seg [data-view=quarter]');
    await d.click('.level-btn[data-level="all"]');

    await d.click('.view-seg [data-view=ayseries]');
    check('AY time series opens from its button', await d.evaluate('$("#time-series-view").is(":visible") && !$("#current-quarter-view").is(":visible")'));
    await d.click('.view-seg [data-view=quarter]');
    check('and Quarter comes back', await d.evaluate('$("#current-quarter-view").is(":visible") && $(".stats-row").is(":visible") && !$("#period-view").is(":visible")'));

    await d.openEmpty();
    await d.evaluate('$("#prefix-input").val("CLAS").trigger("change")');
    await d.waitFor('$("#course-table tbody tr td").length > 3');
    await sleep(300);
    check('reopened: CLAS 484 is still excluded', (await d.evaluate('$("#excl-bar").text()')).startsWith('Excluded everywhere:CLAS 484×') && (await d.evaluate('$("#stat-enrl").text()')) === String(aut26.enrl), await d.evaluate('$("#excl-bar").text()'));
    check('no script errors', d.errors.length === 0, d.errors);
  } finally { d.kill(); }
};
