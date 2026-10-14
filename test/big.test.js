// A department the size of MATH (fake-time-schedule.js's page.math): loads, every view opens, and the page never stops
// answering for long. Each step is timed by how long the page takes to answer a trivial question while it works.
const { launch, sleep } = require('./harness.js');
module.exports = async (check, port) => {
  const d = await launch('big', port);
  /* The longest the page's main thread went without answering, sampled every 100 ms for ms milliseconds. */
  const longestFreeze = async (ms) => {
    let worst = 0;
    for (const end = Date.now() + ms; Date.now() < end;) {
      const t = Date.now();
      await Promise.race([d.evaluate('1'), sleep(60000)]);
      worst = Math.max(worst, Date.now() - t);
      await sleep(100);
    }
    return worst;
  };
  const step = async (label, action, ready, limitMs) => {
    const t = Date.now();
    await action();
    const ok = await d.waitFor(ready, 480);
    const freeze = await longestFreeze(3000);
    console.log(`      ${label}: ${((Date.now() - t) / 1000).toFixed(1)} s, longest freeze after ${freeze} ms`);
    check(`${label}: done, and the page answers within ${limitMs} ms`, ok && freeze < limitMs, { ok, freeze });
  };
  try {
    await d.openEmpty();
    await step('MATH loads', () => d.evaluate('$("#prefix-input").val("MATH").trigger("change")'), '$("#course-table tbody tr td").length > 3', 1500);
    await step('background reading of the decade', async () => {}, '$("#bg-progress").is(":hidden")', 1500);
    for (const [view, sel] of [['Year', 'year'], ['Decade', 'decade'], ['AY time series', 'ayseries'], ['Summers', 'summers'], ['Summer time series', 'sumseries']]) {
      const exists = await d.evaluate(`!!document.querySelector(".view-seg [data-view=${sel}]")`);
      if (!exists) { check(view + ' button found', false, sel); continue; }
      await step(view, () => d.click(`.view-seg [data-view=${sel}]`), '!/Loading…/.test($("#period-view").text() + $("#ts-view, .ts-view").text())', 1500);
    }
    await step('back to Quarter', () => d.click('.view-seg [data-view=quarter]'), '$("#course-table tbody tr td").length > 3', 1500);
    check('no script errors', d.errors.length === 0, d.errors);
  } finally { d.kill(); }
};
