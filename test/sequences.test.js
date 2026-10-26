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

    /* The timeline, as in MyGradMod: twenty years, the last ten shown at first. */
    const sl = () => d.evaluate('({ count: $("#sq-count").text(), labels: $("#sq-slider .sl-lab").map(function(){ return this.textContent + (this.classList.contains("sl-end") ? "*" : ""); }).get().join(), rows: $(".sq-table tbody tr").length, marked: $(".sq-table tr.sq-cmp th").map(function(){ return this.childNodes[0].textContent; }).get().join() })');
    const strip = () => d.evaluate('$(".sq-tile").map(function(){ return this.innerText.replace(/\\s+/g, " "); }).get()');
    const at = i => d.evaluate(`(() => { const s = document.getElementById("sq-slider"); s.scrollIntoView({ block: "center" }); const b = s.getBoundingClientRect(); return { x: b.left + b.width * ${i} / 19, y: b.top + 17 }; })()`);
    const mouse = (type, p, buttons) => d.send('Input.dispatchMouseEvent', { type, x: p.x, y: p.y, button: 'left', buttons, clickCount: 1 });
    const drag = async (i, j) => { const a = await at(i), b = await at(j); await mouse('mousePressed', a, 1); for (let k = 1; k <= 6; k++) await mouse('mouseMoved', { x: a.x + (b.x - a.x) * k / 6, y: a.y }, 1); await mouse('mouseReleased', b, 0); await sleep(300); };
    const settled = () => d.waitFor('$("#bg-progress").is(":hidden") && !/Loading…/.test($("#period-view").text())', 600);
    let w = await sl();
    check('the timeline: the last ten years shown of twenty, and the tiles’ two years marked', w.count === '10 years' && w.labels === '2026–27,2017–18,2007–08*' && w.rows === 10 && w.marked === '2025–26,2017–18', w);
    check('a year without Winter and Spring yet is gray, and says why', await d.evaluate('$("#sq-slider .sl-seg.hist").first().attr("title")') === '2026–27: Winter and Spring not published yet');
    await drag(9, 19);
    check('dragging the older end back: the earlier years are read', await d.evaluate('$("#bg-progress").is(":visible") && /^Reading earlier years from the Time Schedule: \\d+ of \\d+ pages$/.test($("#bg-status").text())'), await d.evaluate('$("#bg-status").text()'));
    await settled();
    await sleep(300);
    w = await sl();
    let t = await strip();
    const ch124t = Math.round((yearTotal(2025, ['124']) / yearTotal(2007, ['124']) - 1) * 100), ch207 = Math.round((yearTotal(2025, ['207']) / yearTotal(2007, ['307']) - 1) * 100);
    check('twenty years: every tile compares with 2007–08', w.count === '20 years' && w.rows === 20 && w.marked === '2025–26,2007–08' && t[1].includes((ch124t > 0 ? '+' : '') + ch124t + '% since 2007–08') && t[4].includes((ch207 > 0 ? '+' : '') + ch207 + '% since 2007–08'), { w, t1: t[1], t4: t[4], ch124t, ch207 });
    check('2007–08’s MATH 207 is MATH 307', /as MATH 307/.test(await d.evaluate('$(".sq-table tbody tr").last().find("td").eq(4).text()')));
    check('the window is kept in this browser', (await d.evaluate('localStorage.getItem("tsmod-seq-window")')) === '{"from":2007,"to":2026}');
    await d.evaluate('$("#sq-slider .sl-dot[data-end=a]")[0].focus()');
    for (let k = 0; k < 3; k++) await d.key('ArrowRight', 'ArrowRight', 39);
    w = await sl();
    t = await strip();
    check('arrow keys move a dot a year at a time: 2023–24 against 2007–08', w.count === '17 years' && w.marked === '2023–24,2007–08' && t[1].includes(fmt(yearTotal(2023, ['124'])) + ' students') && await d.evaluate('document.activeElement.getAttribute("data-end") === "a"'), { w, t1: t[1] });
    await drag(10, 8);
    w = await sl();
    check('dragging the stretch slides the window: 2025–26 to 2009–10', w.count === '17 years' && w.labels.startsWith('2025–26,2009–10') && w.marked === '2025–26,2009–10', w);
    await drag(0, 0);
    w = await sl();
    check('a click newer than both ends moves the newer end', w.count === '18 years' && w.labels.startsWith('2026–27,2009–10') && w.marked === '2025–26,2009–10', w);
    const p5 = await at(5);
    for (const type of ['mousePressed', 'mouseReleased', 'mousePressed', 'mouseReleased']) await mouse(type, p5, type === 'mousePressed' ? 1 : 0);
    await sleep(300);
    await settled();
    w = await sl();
    check('a double-click goes back to the last ten years', w.count === '10 years' && w.marked === '2025–26,2017–18' && (await d.evaluate('localStorage.getItem("tsmod-seq-window")')) === 'null', w);

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
    /* A snapshot keeps the window and the older years it shows. */
    await d.click('.sq-chip[data-seq$=":built-in:0"]');
    await d.evaluate('$("#sq-slider .sl-dot[data-end=b]")[0].focus()');
    for (let k = 0; k < 4; k++) await d.key('ArrowRight', 'ArrowRight', 39);
    await settled();
    const wide = await sl();
    await d.evaluate('window.showSaveFilePicker = undefined');
    await d.click('#snap-save');
    await d.evaluate('$("#snap-history").prop("checked", true).trigger("change")');
    await d.click('.snap-save');
    const file = await d.downloaded();
    await d.openFile(file);
    await d.waitFor('$("#sq-slider").length > 0', 100);
    await sleep(500);
    const reopened = await sl();
    check('a snapshot keeps the window, and the older years’ numbers', wide.count === '14 years' && JSON.stringify(reopened) === JSON.stringify(wide) && /students/.test(await d.evaluate('$(".sq-table tbody tr").last().find("td").eq(1).text()')), { wide, reopened });
    if (process.env.SHOT) {
      await d.click('.sq-chip[data-seq$=":built-in:0"]');
      await d.evaluate('window.scrollTo(0, 0)');
      const shot = await d.send('Page.captureScreenshot', { format: 'png', captureBeyondViewport: true, clip: { x: 0, y: 0, width: 1440, height: 1700, scale: 1 } });
      fs.writeFileSync(path.join(__dirname, 'tmp', 'sequences.png'), Buffer.from(shot.data, 'base64'));
    }
    check('no script errors', d.errors.length === 0, d.errors);
  } finally { d.kill(); }
};
