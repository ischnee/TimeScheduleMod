// The Sequences view on the made-up MATH department: MATH's built-in pathways (from Andy Loveless's material), renumbered
// courses joined (207 was 307 before Autumn 2019 in the fake data), sequences found from course titles, section-size growth,
// your own sequences, and the numbers in the grid and the executive strip.
const fs = require('fs'), path = require('path');
const { sleep, launch } = require('./harness.js');
const page = require('./fake-time-schedule.js');
const QN = { WIN: 0, SPR: 1, SUM: 2, AUT: 3 };
const quarters = ay => ['AUT' + ay, 'WIN' + (ay + 1), 'SPR' + (ay + 1)];
const lectures = (q, nums) => (page.math.sections(q) || []).filter(s => nums.includes(s.number));
const yearTotal = (ay, nums) => quarters(ay).reduce((n, q) => n + lectures(q, nums).reduce((m, s) => m + s.enrl, 0), 0);
const fmt = n => n.toLocaleString('en-US');
module.exports = async (check, port) => {
  const d = await launch('sequences', port);
  try {
    await d.openEmpty();
    await d.evaluate('localStorage.removeItem("tsmod-sequences")');
    await d.evaluate('$("#prefix-input").val("MATH").trigger("change")');
    await d.waitFor('$("#course-table tbody tr td").length > 3', 120);
    await d.click('.view-seg [data-view=sequences]');
    await d.waitFor('$("#bg-progress").is(":hidden") && !/Loading…/.test($("#period-view").text())', 480);
    await sleep(500);
    const chips = await d.evaluate('$(".sq-chips .sq-chip").map(function(){ return $(this).text(); }).get()');
    check('MATH’s built-in sequences, then ones found from titles, then + Add', ['Calculus', 'Non-calculus', 'Remediation', 'High demand', 'Upper division'].every((n, i) => chips[i] === n)
      && chips.includes('Discrete Mathematical Modeling') && chips.includes('Section-size growth') && chips[chips.length - 1] === '+ Add a sequence', chips);
    const heads = await d.evaluate('$(".sq-table thead th").map(function(){ return this.childNodes[0].textContent; }).get()');
    check('Calculus: 120 → 124 → 125 → 126 → 207 → 208, then the sequence total', heads.join('|') === "Academic year|MATH 120|MATH 124|MATH 125|MATH 126|MATH 207|MATH 208|Sequence", heads);
    const cellText = (ay, col) => d.evaluate(`$(".sq-table tbody tr").filter(function(){ return $(this).find("th").text().indexOf("${ay}–${String(ay + 1).slice(2)}") === 0; }).find("td").eq(${col}).text()`);
    const c124 = await cellText(2024, 1);
    check('a year’s cell: the course’s students over Autumn, Winter and Spring', c124.startsWith(fmt(yearTotal(2024, ['124'])) + ' students'), { c124, expected: yearTotal(2024, ['124']) });
    const c207old = await cellText(2017, 4);
    check('renumbered: 2017–18’s MATH 207 counts MATH 307, and says so', c207old.startsWith(fmt(yearTotal(2017, ['307'])) + ' students') && /as MATH 307/.test(c207old), { c207old, expected: yearTotal(2017, ['307']) });
    const seqSum = await cellText(2022, 6);
    check('the Sequence column adds up the courses', seqSum.startsWith(fmt(yearTotal(2022, ['120', '124', '125', '126', '207', '208'])) + ' students'), seqSum);
    const tiles = await d.evaluate('$(".sq-tile").map(function(){ return this.innerText.replace(/\\s+/g, " "); }).get()');
    check('the strip: a tile per course, in order, and one for all six', tiles.length === 7 && tiles[0].startsWith('MATH 120') && tiles[6].startsWith('All 6 courses'), tiles.map(t => t.slice(0, 20)));
    const ch124 = Math.round((yearTotal(2025, ['124']) / yearTotal(2017, ['124']) - 1) * 100);
    check('MATH 124’s tile: 2025–26’s students, and the change since 2017–18', tiles[1].includes(fmt(yearTotal(2025, ['124'])) + ' students') && tiles[1].includes((ch124 > 0 ? '+' : '') + ch124 + '% since 2017–18'), { tile: tiles[1], ch124 });
    const big208now = Math.max(...quarters(2025).flatMap(q => lectures(q, ['208']).map(s => s.lim))), big208then = Math.max(...quarters(2017).flatMap(q => lectures(q, ['308']).map(s => s.lim)));
    check('MATH 208’s largest section, now and then (as 308)', tiles[5].includes('Largest section ' + big208now + ' (was ' + big208then + ')'), { tile: tiles[5], big208now, big208then });
    check('flow arrows between the courses', await d.evaluate('$(".sq-arrow").length') === 5);

    await d.click('.sq-chip[data-seq*="Discrete Mathematical Modeling"]');
    check('found from titles: DISCRETE MATHEMATICAL MODELING I and II', (await d.evaluate('$(".sq-table thead th").map(function(){ return this.childNodes[0].textContent; }).get().join("|")')) === 'Academic year|MATH 381|MATH 382|Sequence');
    await d.click('.sq-chip[data-seq*="Section-size growth"]');
    const grew = await d.evaluate('$(".sq-table thead th").map(function(){ return this.childNodes[0].textContent; }).get()');
    check('section-size growth lists the courses whose largest section grew most', ['MATH 124', 'MATH 207', 'MATH 208', 'MATH 224'].every(c => grew.includes(c)) && !grew.includes('MATH 381'), grew);

    await d.click('.sq-add');
    await d.evaluate('$("#sq-name").val("Probability path"); $("#sq-courses").val("MATH 300, 394")');
    await d.click('.sq-form button[type=submit]');
    check('your own sequence: saved, shown and kept in this browser', (await d.evaluate('$(".sq-chips .sq-chip.on").text() + " | " + $(".sq-table thead th").map(function(){ return this.childNodes[0].textContent; }).get().join("|") + " | " + localStorage.getItem("tsmod-sequences")'))
      === 'Probability path | Academic year|MATH 300|MATH 394|Sequence | {"MATH":[{"name":"Probability path","courses":["300","394"]}]}');
    await d.click('.sq-del');
    check('× removes it', !(await d.evaluate(`$(".sq-chips .sq-chip").text()`)).includes('Probability path') && (await d.evaluate('localStorage.getItem("tsmod-sequences")')) === '{"MATH":[]}');
    if (process.env.SHOT) {
      await d.click('.sq-chip[data-seq$=":built-in:0"]');
      await d.evaluate('window.scrollTo(0, 0)');
      const shot = await d.send('Page.captureScreenshot', { format: 'png', captureBeyondViewport: true, clip: { x: 0, y: 0, width: 1440, height: 1700, scale: 1 } });
      fs.writeFileSync(path.join(__dirname, 'tmp', 'sequences.png'), Buffer.from(shot.data, 'base64'));
    }
    check('no script errors', d.errors.length === 0, d.errors);
  } finally { d.kill(); }
};
