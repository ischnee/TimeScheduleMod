// Smaller behaviors: Tab in an empty note, and the % Full dots.
const { launch } = require('./harness.js');
module.exports = async (check, port) => {
  const d = await launch('details', port);
  try {
    await d.openWithPhil();
    check('the first card says Sections counted', (await d.evaluate('$(".stats-row .stat-card h3").first().text()')) === 'Sections counted');
    check('header says TimeScheduleMod', (await d.evaluate('$(".dashboard-header h1").text() + " | " + document.title')) === 'TimeScheduleMod | AUT2026 TimeScheduleMod');
    await d.click('#snap-save');
    const state = () => d.evaluate('({ focus: document.activeElement.id, note: $("#snap-note").val(), pick: $(".snap-picks button.on").text() })');
    await d.key('Tab', 'Tab', 9);
    const a = await state();
    check('Tab in the empty note fills "First day of classes" and stays', a.note === 'First day of classes' && a.focus === 'snap-note' && a.pick === 'First day of classes', a);
    await d.key('Tab', 'Tab', 9);
    check('a second Tab moves on', (await state()).focus !== 'snap-note');
    await d.evaluate('$("#snap-note").val("Census day").trigger("input").focus()');
    await d.key('Tab', 'Tab', 9);
    check('Tab after your own note moves on and keeps it', (await state()).note === 'Census day');
    await d.evaluate('$("#snap-dialog").remove(); $(document).off("keydown.snap"); $("#course-table").DataTable().order([[8, "desc"]]).page.len(10).draw()');
    const dots = await d.evaluate('$("#course-table tbody tr").slice(0, 2).map(function(){ const td = $(this).find("td"); return td.eq(1).text() + " " + td.eq(8).text() + " " + td.eq(8).find(".fill-dot").attr("class") + " " + td.eq(8).find(".fill-dot").attr("title"); }).get()');
    check('over capacity gets the dark green dot', dots[0] === 'PHIL 345 110.0% fill-dot over Over capacity', dots[0]);
    check('75–100% gets the green dot', /fill-dot full 75–100% full$/.test(dots[1]), dots[1]);
    check('no script errors', d.errors.length === 0, d.errors);
  } finally { d.kill(); }
};
