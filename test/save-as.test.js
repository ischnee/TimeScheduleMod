// Chrome's Save As dialog, replaced by a stand-in that records how it's called (headless Chrome can't click a native dialog).
const { launch, fetchCount, toggleSignedOut } = require('./harness.js');
const FAKE = `window.__saved = null; window.__calls = []; window.__removed = false;
  window.showSaveFilePicker = async function(opts){
    window.__calls.push({ opts: opts, fetches: +(await (await fetch("/__fetches")).text()) });
    if (window.__cancel) throw new DOMException("The user aborted a request.", "AbortError");
    return { name: "Picked name.html", createWritable: async () => { const parts = []; return { write: async b => parts.push(await b.text()), close: async () => { window.__saved = parts.join(""); } }; },
      remove: async () => { window.__removed = true; } };
  };`;
module.exports = async (check, port) => {
  const d = await launch('saveas', port);
  try {
    await d.openWithPhil();
    check('this Chrome has the Save As dialog', (await d.evaluate('typeof window.showSaveFilePicker')) === 'function');
    await d.evaluate(FAKE + 'window.__cancel = true;');
    await d.click('#snap-save');
    check('button says "Save file…"', (await d.evaluate('$(".snap-save").text()')) === 'Save file…');
    let before = await fetchCount();
    await d.click('.snap-save');
    const c = await d.evaluate('({ open: $("#snap-dialog").length === 1, enabled: !$(".snap-save").prop("disabled"), saved: window.__saved })');
    check('cancelled Save As: back in the dialog, nothing saved or reloaded', c.open && c.enabled && c.saved === null && (await fetchCount()) === before, c);
    await d.evaluate('window.__cancel = false');
    before = await fetchCount();
    await d.click('.snap-save');
    await d.waitFor('!!window.__saved', 40);
    const s = await d.evaluate('({ call: window.__calls[window.__calls.length - 1], data: (window.__saved || "").includes("id=\\"tsv-snapshot\\""), toast: $(".snap-toast").text(), open: $("#snap-dialog").length === 1 })');
    check('Save As asked first, before the reload', s.call.fetches === before, s.call);
    check('Save As opens in the snapshots folder with the suggested name', s.call.opts.id === 'tsv-snapshots' && /^Time Schedule AUT2026 PHIL .*\.html$/.test(s.call.opts.suggestedName), s.call.opts);
    check('the snapshot is written there', s.data && !s.open && s.toast === 'Snapshot saved as “Picked name.html”', s);
    await toggleSignedOut();
    await d.evaluate('window.__saved = null');
    await d.click('#snap-save'); await d.click('.snap-save');
    await d.waitFor('$("#snap-status").hasClass("err")', 20);
    const f = await d.evaluate('({ saved: window.__saved, removed: window.__removed })');
    await toggleSignedOut();
    check('a failed reload after Save As removes the empty file', f.saved === null && f.removed, f);
    check('no script errors', d.errors.length === 0, d.errors);
  } finally { d.kill(); }
};
