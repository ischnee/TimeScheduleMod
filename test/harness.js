// Shared test helpers: the fake Time Schedule server, and a throwaway headless Chrome driven over the DevTools protocol.
// Needs Google Chrome and Node 20+ run with --experimental-websocket (run.js does that).
const { spawn } = require('child_process');
const fs = require('fs');
const path = require('path');
const http = require('http');
const page = require('./fake-time-schedule.js');

const DIR = __dirname, TMP = path.join(DIR, 'tmp'), PORT = 9556, BASE = `http://127.0.0.1:${PORT}`;
const CHROME = process.env.CHROME || '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';
const sleep = ms => new Promise(r => setTimeout(r, ms));

/* The fake Time Schedule. /dash serves the dashboard (captured from the build by run.js) with its Time Schedule
   addresses pointed here. Each fetch of the current quarter's page adds 1 to PHIL 100 A's enrollment, so a reload
   shows up in the numbers; /__signout makes that page a sign-in page with no sections. */
function startServer() {
  let fetches = 0, signedOut = false, clasDelay = 0;   // clasDelay: slows past CLAS pages, to see the background reading
  const past = { AUT2025: -3, WIN2026: -5, SPR2026: -7, AUT2024: -9 };
  const server = http.createServer((req, res) => {
    if (req.url === '/dash' || req.url === '/dash-phil') {
      const html = fs.readFileSync(path.join(TMP, req.url === '/dash' ? 'dashboard.html' : 'dashboard-phil.html'), 'utf8').split('https://www.washington.edu/students/timeschd/').join(BASE + '/students/timeschd/');
      res.writeHead(200, { 'content-type': 'text/html; charset=utf-8' }); return res.end(html);
    }
    // Pages for the wrong-page notices and the loader: somewhere else, the Time Schedule's front page, a quarter page, a page
    // that blocks scripts from other sites (as many sites do), and the built bookmarklet as jsDelivr would serve it.
    if (req.url === '/elsewhere' || req.url === '/students/timeschd/' || req.url === '/students/timeschd/AUT2026/') { res.writeHead(200, { 'content-type': 'text/html' }); return res.end('<html><body><h1>' + req.url + '</h1></body></html>'); }
    if (req.url === '/strict') { res.writeHead(200, { 'content-type': 'text/html', 'content-security-policy': "script-src 'self'" }); return res.end('<html><body><h1>Strict</h1></body></html>'); }
    if (req.url.startsWith('/cdn/bookmarklet-timeschedulemod.js')) { res.writeHead(200, { 'content-type': 'application/javascript' }); return res.end(fs.readFileSync(path.join(DIR, '..', 'bookmarklet-timeschedulemod.js'))); }
    if (req.url === '/__fetches') { res.writeHead(200); return res.end(String(fetches)); }
    if (req.url === '/__signout') { signedOut = !signedOut; res.writeHead(200); return res.end(String(signedOut)); }
    if (req.url.startsWith('/__clasdelay')) { clasDelay = +(req.url.split('=')[1] || 0); res.writeHead(200); return res.end(String(clasDelay)); }
    const c = req.url.match(/^\/students\/timeschd\/([A-Z]{3}\d{4})\/clas\.html$/);
    if (c && clasDelay && c[1] !== 'AUT2026') { const ms = clasDelay; return setTimeout(() => { const html = page.clas.page(c[1]); if (html) { res.writeHead(200, { 'content-type': 'text/html; charset=utf-8' }); res.end(html); } else { res.writeHead(404); res.end('not found'); } }, ms); }
    if (c) { const html = signedOut ? null : page.clas.page(c[1]); if (html) { res.writeHead(200, { 'content-type': 'text/html; charset=utf-8' }); return res.end(html); } res.writeHead(404); return res.end('not found'); }
    const m = req.url.match(/^\/students\/timeschd\/([A-Z]{3}\d{4})\/phil\.html$/);
    if (m && m[1] === 'AUT2026') {
      if (signedOut) { res.writeHead(200, { 'content-type': 'text/html' }); return res.end('<html><body><h1>Sign in</h1><form></form></body></html>'); }
      fetches++;
      const html = page('AUT2026', 0).replace(/(PHIL&nbsp;&nbsp; 100 [\s\S]*?Instructor,\w+\s+Open\s+)(\d+)(\/)/, (all, a, n, b) => a + String(+n + fetches - 1).padStart(3) + b);
      res.writeHead(200, { 'content-type': 'text/html; charset=utf-8' }); return res.end(html);
    }
    if (m && past[m[1]] !== undefined) { res.writeHead(200, { 'content-type': 'text/html; charset=utf-8' }); return res.end(page(m[1], past[m[1]])); }
    res.writeHead(404); res.end('not found');
  });
  return new Promise(r => server.listen(PORT, '127.0.0.1', () => r(server)));
}
const fetchCount = async () => +(await (await fetch(BASE + '/__fetches')).text());
const toggleSignedOut = () => fetch(BASE + '/__signout');

async function connect(url) {
  const ws = new WebSocket(url);
  await new Promise(r => (ws.onopen = r));
  let id = 0; const pending = {}, listeners = [];
  ws.onmessage = m => { const d = JSON.parse(m.data); if (pending[d.id]) { pending[d.id](d.result || { error: d.error }); delete pending[d.id]; } else if (d.method) listeners.forEach(f => f(d)); };
  const send = (method, params = {}) => new Promise(r => { pending[++id] = r; ws.send(JSON.stringify({ id, method, params })); });
  const evaluate = async expr => { const r = await send('Runtime.evaluate', { expression: expr, returnByValue: true, awaitPromise: true }); if (r.exceptionDetails) throw new Error(JSON.stringify(r.exceptionDetails).slice(0, 400)); return r.result ? r.result.value : r; };
  return { ws, send, evaluate, on: f => listeners.push(f) };
}

/* A fresh headless Chrome at 1440×900 with downloads going to tmp/downloads-<name>. Returns the page and helpers. */
async function launch(name, port) {
  const profile = path.join(TMP, 'profile-' + name), downloads = path.join(TMP, 'downloads-' + name);
  fs.rmSync(profile, { recursive: true, force: true }); fs.rmSync(downloads, { recursive: true, force: true }); fs.mkdirSync(downloads, { recursive: true });
  const chrome = spawn(CHROME, ['--headless=new', '--disable-gpu', `--user-data-dir=${profile}`, `--remote-debugging-port=${port}`, '--window-size=1440,900', 'about:blank'], { stdio: 'ignore' });
  const json = async p => (await fetch(`http://127.0.0.1:${port}${p}`)).json();
  for (let i = 0; i < 60; i++) { try { await json('/json/version'); break; } catch { await sleep(200); } }
  const browser = await connect((await json('/json/version')).webSocketDebuggerUrl);
  await browser.send('Browser.setDownloadBehavior', { behavior: 'allow', downloadPath: downloads, eventsEnabled: true });
  const d = await connect((await json('/json/list')).find(t => t.type === 'page').webSocketDebuggerUrl);
  await d.send('Page.enable'); await d.send('Runtime.enable');
  d.errors = [];
  d.on(m => { if (m.method === 'Runtime.exceptionThrown') d.errors.push((m.params.exceptionDetails.exception || {}).description || m.params.exceptionDetails.text); });
  await d.send('Emulation.setDeviceMetricsOverride', { width: 1440, height: 900, deviceScaleFactor: 1, mobile: false });
  d.downloads = downloads;
  d.kill = () => chrome.kill();
  /* A real mouse click in the middle of the element. */
  d.click = async sel => {
    const p = await d.evaluate(`(() => { const e = document.querySelector(${JSON.stringify(sel)}); if (!e) return null; e.scrollIntoView({ block: "center" }); const b = e.getBoundingClientRect(); return { x: b.left + b.width / 2, y: b.top + b.height / 2 }; })()`);
    if (!p) throw new Error('no element ' + sel);
    for (const type of ['mousePressed', 'mouseReleased']) await d.send('Input.dispatchMouseEvent', { type, x: p.x, y: p.y, button: 'left', clickCount: 1 });
    await sleep(250);
  };
  d.key = async (key, code, keyCode, modifiers = 0) => { for (const type of ['keyDown', 'keyUp']) await d.send('Input.dispatchKeyEvent', { type, key, code, windowsVirtualKeyCode: keyCode, modifiers }); await sleep(150); };
  d.waitFor = async (expr, tries = 60) => { for (let i = 0; i < tries; i++) { if (await d.evaluate(expr).catch(() => false)) return true; await sleep(250); } return false; };
  /* The dashboard before any prefix is loaded, then with PHIL loaded. */
  d.openEmpty = async () => {
    await d.send('Page.navigate', { url: BASE + '/dash' });
    await d.waitFor('!!window.jQuery && $("#dashboard").is(":visible")');
  };
  d.openWithPhil = async () => {
    if (!(await d.evaluate('!!window.jQuery && location.pathname === "/dash"').catch(() => false))) await d.openEmpty();
    await d.evaluate('$("#prefix-input").val("PHIL").trigger("change")');
    await d.waitFor('$("#course-table tbody tr td").length > 3');
    await sleep(300);
  };
  d.openFile = async file => {
    await d.send('Page.navigate', { url: 'file://' + path.join(downloads, file).split('/').map(encodeURIComponent).join('/') });
    await d.waitFor('!!window.jQuery && $("#course-table tbody tr td").length > 3');
    await sleep(500);
  };
  d.downloaded = async () => { for (let i = 0; i < 80; i++) { const f = fs.readdirSync(downloads).find(x => x.endsWith('.html')); if (f) return f; await sleep(250); } return null; };
  return d;
}

/* The snapshot data inside a saved file. */
function snapshotIn(html) { return JSON.parse(html.match(/<script id="tsv-snapshot" type="application\/json">([\s\S]*?)<\/script>/)[1]); }

module.exports = { DIR, TMP, BASE, sleep, startServer, fetchCount, toggleSignedOut, launch, snapshotIn };
