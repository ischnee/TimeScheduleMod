// The TA card and its By course breakdown, against numbers worked out by hand (see fake-time-schedule.js).
const { launch } = require('./harness.js');
module.exports = async (check, port) => {
  const d = await launch('ta', port);
  try {
    await d.openEmpty();
    check('By course button hidden before data', !(await d.evaluate('$("#ta-open").is(":visible")')));
    await d.openWithPhil();
    const card = await d.evaluate('({ value: $("#stat-ta").text(), sub: $("#stat-ta-sub").text() })');
    check('all courses: ≈20 TAs', card.value === '≈20', card);
    check('all courses: 12 named + ≈8 more, 16 without a TA, 3 empty', card.sub === '12 named + ≈8 more16 sections without a TA · 3 empty', card.sub);
    await d.evaluate('$(".level-btn[data-level=100]").click()');
    const c100 = await d.evaluate('$("#stat-ta").text() + " | " + $("#stat-ta-sub").text()');
    check('100-level only: ≈17 (10 named + ≈7)', c100 === '≈17 | 10 named + ≈7 more14 sections without a TA', c100);
    await d.evaluate('$(".level-btn[data-level=all]").click()');
    await d.click('#ta-open');
    const m = await d.evaluate(`({
      rows: $(".ta-table tbody tr").map(function(){ const td = $(this).children("td"); return td.eq(0).text() + " | " + td.eq(2).text() + " | " + td.eq(3).text() + " | " + td.eq(5).text(); }).get(),
      total: $(".ta-table tfoot td").last().text(), kinds: [$(".qz.ta").length, $(".qz.need").length, $(".qz.empty").length],
      first: $(".qz").first().text(), shared: $(".qz:has(i)").length, href: $(".qz").first().attr("href"), loads: $(".ta-loads").text() })`);
    check('one row per course with quiz sections', m.rows.length === 7, m.rows);
    check('course sums as worked out', JSON.stringify(m.rows) === JSON.stringify(['PHIL 100 | 4 | 2 | 4 ÷ 2 = +2', 'PHIL 102 | 2 | 3 | 0', 'PHIL 114 | 0 | 2 | 5 ÷ 2 = +3',
      'PHIL 115 | 2 | 2 | 1 to TA8; 1 ÷ 2 = +1', 'PHIL 120 | 2 | 3 | 3 ÷ 3 = +1', 'PHIL 240 | 1 | 2 | 0', 'PHIL 242 | 2 | 2 | 2 ÷ 2 = +1']), m.rows);
    check('total matches the card', m.total === '+8 → ≈20 TAs', m.total);
    check('47 chips: 28 TA, 16 need a TA, 3 empty', m.kinds.join() === '28,16,3', m.kinds);
    check('TA1 is the first TA in PHIL 100', m.first === 'AATA124', m.first);
    check('TA7 marked as shared in both of its courses', m.shared === 2, m.shared);
    check('chips open the section on the Time Schedule', /sdb\.admin\.uw\.edu\/timeschd\/uwnetid\/sln\.asp\?QTRYR=AUT\+2026&SLN=\d+$/.test(m.href), m.href);
    check('usual load line', m.loads.startsWith('Usual load 2 quiz sections per TA ·2 each: TA1 TA2 TA3 TA4 TA7 TA11 TA12'), m.loads);
    check('no TA name anywhere on the page', (await d.evaluate('(document.documentElement.outerHTML.match(/Assistant,/g) || []).length')) === 0);
    await d.key('Escape', 'Escape', 27);
    check('Escape closes it', await d.evaluate('$("#ta-dialog").length === 0'));
    check('no script errors', d.errors.length === 0, d.errors);
  } finally { d.kill(); }
};
