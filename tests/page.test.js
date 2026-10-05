// Whole-page test for the final page (weather-machine.html), built by scripts/build_all.py.
//   node tests/page.test.js http://localhost:8766/weather-machine.html
// Serve the repo first:  python3 -m http.server 8766
// Checks how the story and the module sections fit together; each module has its own tests
// (tests/rain-gauges/). Covers INTEGRATION.md section 9's manual checks 1, 2, 3, 5 and 6.
const { chromium } = require('playwright');
const URL = process.argv[2];
(async () => {
  const browser = await chromium.launch(); let failed = 0;
  const check = (name, ok, got) => { if (!ok) failed++; console.log((ok ? 'PASS  ' : 'FAIL  ') + name + (ok ? '' : `   (got: ${got})`)); };
  const errors = [], requests = [];
  const ctx = await browser.newContext({ viewport: { width: 1440, height: 900 } });
  const page = await ctx.newPage();
  page.on('pageerror', e => errors.push(e.message));
  // the headless browser's own GPU notices ('GL Driver Message … GPU stall') are not page errors
  page.on('console', m => { if ((m.type() === 'error' || m.type() === 'warning') && !/GL Driver Message/.test(m.text())) errors.push(m.type() + ': ' + m.text()); });
  page.on('request', r => requests.push(r.url()));
  await page.goto(URL); await page.waitForTimeout(1500);

  // 1. the story is built into its slots, modules after it, in sections.json order
  const order = await page.evaluate(() => [...document.querySelectorAll('#story > .step, #story > .mod')]
    .map(e => e.classList.contains('mod') ? e.dataset.module + ':' + e.dataset.part : 'step'));
  const steps = order.filter(x => x === 'step').length;
  // slides whose words a prototype section carries (and that have no story step of their own) are not steps
  check('every view of every slide became a step', steps === await page.evaluate(() => SCENES.filter(s => document.querySelector('.step[data-slide="' + s.id + '"]') || !document.querySelector('.mod [data-slide-text="' + s.id + '"]')).reduce((n, s) => n + (s.views || [1]).length, 0)), steps);
  const slideOrder = await page.evaluate(() => [...document.querySelectorAll('#story > .step, #story > .mod')].map(e => e.dataset.slide || e.dataset.part).filter((x, i, a) => x !== a[i - 1]));
  const cfg = await (await page.request.get(URL.replace('weather-machine.html', 'final/sections.json'))).json();
  const want = cfg.order.flatMap(o => o.story ? o.story : o.part ? [o.part] : []);   // plugin entries place nothing
  check('order follows final/sections.json', JSON.stringify(slideOrder) === JSON.stringify(want), slideOrder.join(' '));

  // 2. the story still drives its card at the top of the page
  check('slide text shows on the first slide', await page.evaluate(() => /Gaps in the Weather Machine/.test(document.getElementById('slide').textContent)), '');

  // 3. scroll into each module: it covers the globe, and the story's card, hint and wipe handle hide
  const SECTIONS = await page.evaluate(() => [...document.querySelectorAll('#story > .mod section')].map(s => s.id));
  for (const id of SECTIONS) {
    await page.evaluate(id => document.getElementById(id).scrollIntoView(), id); await page.waitForTimeout(700);
    const s = await page.evaluate(id => {
      const sec = document.getElementById(id), r = sec.getBoundingClientRect(), bar = document.getElementById('topbar').getBoundingClientRect();
      const top = document.elementFromPoint(innerWidth * 0.7, innerHeight * 0.5);
      const firstText = sec.querySelector('h2, .rgm-title, .rg-tabs, [role=tablist]');
      return { flag: document.body.hasAttribute('data-mod'), card: getComputedStyle(document.getElementById('slide')).display,
               hint: getComputedStyle(document.getElementById('hintbar')).display, cmp: getComputedStyle(document.getElementById('cmp')).display,
               covers: sec.contains(top), bg: getComputedStyle(sec).backgroundColor, clear: firstText ? firstText.getBoundingClientRect().top >= bar.bottom - 6 : null };
    }, id);
    check(`${id}: the section covers the story's globe (opaque, on top)`, s.covers && s.bg !== 'rgba(0, 0, 0, 0)', JSON.stringify(s));
    check(`${id}: story text, hint and wipe handle are hidden`, s.flag && s.card === 'none' && s.hint === 'none' && s.cmp === 'none', JSON.stringify(s));
    check(`${id}: its first line of text clears the top bar`, s.clear === true, JSON.stringify(s));
  }
  // 4. back to the story: the flag clears
  await page.evaluate(() => window.scrollTo(0, 0)); await page.waitForTimeout(700);
  check('back at the top, the story text returns', await page.evaluate(() => !document.body.hasAttribute('data-mod') && getComputedStyle(document.getElementById('slide')).display !== 'none'), '');

  // 5. Explore hides the modules; Story brings them back
  await page.click('#navExplore'); await page.waitForTimeout(300);
  const exp = await page.evaluate(ids => ids.map(id => document.getElementById(id).getClientRects().length), SECTIONS);
  check('Explore mode: no section is on the page', exp.every(n => n === 0), JSON.stringify(exp));
  await page.click('#navStory'); await page.waitForTimeout(300);
  const back = await page.evaluate(ids => ids.map(id => document.getElementById(id).getClientRects().length), SECTIONS);
  check('Story mode: the sections return', back.every(n => n > 0), JSON.stringify(back));

  // 6. the D panel is gone (author, 5 Oct)
  await page.keyboard.press('d'); await page.waitForTimeout(200);
  check('pressing D opens nothing', await page.evaluate(() => !document.querySelector('#panel.open')), '');
  // Space moves one stop: the next slide step or section; Shift+Space comes back
  await page.evaluate(() => { window.scrollTo(0, 0); document.activeElement && document.activeElement.blur(); }); await page.waitForTimeout(400);
  await page.keyboard.press('Space'); await page.waitForTimeout(1200);
  const y1 = await page.evaluate(() => scrollY), h1 = await page.evaluate(() => innerHeight);
  check('Space moves to the next slide', Math.abs(y1 - h1) < 4, y1);
  await page.keyboard.press('Shift+Space'); await page.waitForTimeout(1200);
  check('Shift+Space comes back', (await page.evaluate(() => scrollY)) < 4, await page.evaluate(() => scrollY));

  // 7. self-contained: the only requests are the page itself and Google Fonts
  const foreign = requests.filter(u => !u.startsWith(URL.split('/weather-machine')[0]) && !/fonts\.(googleapis|gstatic)\.com/.test(u) && !u.startsWith('data:'));
  check('no network requests except the page and Google Fonts', foreign.length === 0, foreign.join(' '));

  // 8. widths: no sideways scroll anywhere on the page
  for (const [w, h] of [[1280, 720], [1024, 768], [390, 844]]) {
    await page.setViewportSize({ width: w, height: h }); await page.waitForTimeout(300);
    const over = await page.evaluate(() => document.documentElement.scrollWidth > innerWidth + 1);
    check(`${w}x${h}: no sideways scroll`, !over, '');
  }

  check('no JavaScript errors or warnings', errors.length === 0, errors.join(' | '));
  console.log(failed ? `\n${failed} check(s) FAILED` : '\nall checks passed'); await browser.close(); process.exit(failed ? 1 : 0);
})();
