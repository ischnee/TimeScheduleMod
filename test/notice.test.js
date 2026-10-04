// Clicked in the wrong place: TSMod's own notice with the steps; and the README's loader says so when a site blocks it.
const fs = require('fs'), path = require('path');
const { BASE, sleep, launch } = require('./harness.js');
const CODE = fs.readFileSync(path.join(__dirname, '..', 'bookmarklet-timeschedulemod.js'), 'utf8').slice('javascript:'.length);
const README = fs.readFileSync(path.join(__dirname, '..', 'README.md'), 'utf8');
const LOADER = README.match(/```\njavascript:(\(function\(\)\{[\s\S]*?\}\)\(\);)\n```/)[1];
module.exports = async (check, port) => {
  const d = await launch('notice', port);
  const go = async url => { await d.send('Page.navigate', { url }); await d.waitFor(`document.readyState === "complete" && location.href === ${JSON.stringify(url)}`); };
  const notice = () => d.evaluate('(() => { const n = document.getElementById("tsmod-notice"); if (!n) return null; const a = n.querySelector("a.go"); return { head: n.querySelector("#tsmod-notice-head").textContent, msg: n.querySelector(".msg").textContent, link: a.style.display === "none" ? null : a.textContent + " " + a.getAttribute("href") }; })()');
  const run = (code, gesture) => d.send('Runtime.evaluate', { expression: code, userGesture: gesture !== false });
  try {
    await go(BASE + '/elsewhere');
    await run(CODE);
    let n = await notice();
    check('somewhere else: says it’s installed, with the steps', n && n.head === 'TimeScheduleMod successfully installed' && n.msg === 'Open the UW Time Schedule: sign in with your UW NetID, pick any quarter (for example Autumn 2026), then click TimeScheduleMod again.', n);
    check('…and a button to the Time Schedule', n && n.link === 'Open the Time Schedule https://www.washington.edu/students/timeschd/', n);
    await d.key('Escape', 'Escape', 27);
    check('Escape closes it', !(await notice()));
    await go(BASE + '/students/timeschd/');
    await run(CODE);
    n = await notice();
    check('on the Time Schedule’s front page: pick a quarter', n && n.msg === 'Pick a quarter on this page, then click TimeScheduleMod again.' && !n.link, n);
    await go(BASE + '/students/timeschd/AUT2026/');
    await run(CODE, false);
    n = await notice();
    check('pop-up blocked: says to allow pop-ups', n && n.msg === 'Pop-up blocked! Allow pop-ups for this site, then click TimeScheduleMod again.', n);

    const otherOrigin = 'http://localhost:' + new URL(BASE).port + '/cdn/bookmarklet-timeschedulemod.js';
    const loader = LOADER.replace('https://cdn.jsdelivr.net/gh/ischnee/TimeScheduleMod@main/bookmarklet-timeschedulemod.js', otherOrigin);
    await go(BASE + '/elsewhere');
    await run(loader);
    await d.waitFor('!!document.getElementById("tsmod-notice")', 20);
    check('the README’s loader, somewhere else: the same notice', /successfully installed/.test(((await notice()) || {}).head || ''));
    const dialogs = [];
    d.on(m => { if (m.method === 'Page.javascriptDialogOpening') { dialogs.push(m.params.message); d.send('Page.handleJavaScriptDialog', { accept: true }); } });
    await go(BASE + '/strict');
    await run(loader);
    for (let i = 0; i < 20 && !dialogs.length; i++) await sleep(150);
    check('a site that blocks outside scripts: the loader says it couldn’t load', dialogs[0] === "TimeScheduleMod couldn't load on this page. Open the UW Time Schedule, pick a quarter, then click it again.", dialogs);
    check('no script errors', d.errors.length === 0, d.errors);
  } finally { d.kill(); }
};
