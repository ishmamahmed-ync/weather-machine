// The weather-machine slides (2 to 5): the instruments fill in year by year with the era timeline under the cards.
//   node tests/history.test.js http://localhost:8766/weather-machine.html
// Runs with reduced motion, so each slide lands at once on the end of its era.
const { chromium } = require('playwright');
const URL = process.argv[2];
(async () => {
  const b = await chromium.launch(); let failed = 0; const errs = [];
  const check = (n, ok, g) => { if (!ok) failed++; console.log((ok ? 'PASS  ' : 'FAIL  ') + n + (ok ? '' : '   (got: ' + g + ')')); };
  for (const [w, h] of [[1440, 900], [1280, 720]]) {
    const ctx = await b.newContext({ viewport: { width: w, height: h }, reducedMotion: 'reduce' }), p = await ctx.newPage();
    p.on('pageerror', e => errs.push(e.message)); p.on('console', m => { if ((m.type() === 'warning' || m.type() === 'error') && !/GL Driver/.test(m.text())) errs.push(m.text()); });
    await p.goto(URL); await p.waitForTimeout(1200);
    const want = [['stations', 1960, 'Weather stations', 1], ['satellites', 1990, 'Satellites', 2], ['argo', 2025, 'Argo floats', 3], ['machine', 2025, '', 4]];
    const tops = [];
    for (const [id, year, lit, cards] of want) {
      await p.evaluate(id => { const s = document.querySelector('.step[data-slide="' + id + '"]'); scrollTo(0, s.getBoundingClientRect().top + scrollY); }, id);
      await p.waitForTimeout(500);
      const r = await p.evaluate(() => { const e = document.querySelector('#slide .era');
        return { year: +e.querySelector('input').value, lit: (e.querySelector('.c.is-on') || {}).textContent || '', top: Math.round(e.getBoundingClientRect().top),
                 cards: document.querySelectorAll('#slide .wm-instrument').length, text: Math.round(document.querySelector('#slide .wm-source').getBoundingClientRect().bottom) }; });
      tops.push(r.top);
      check(`${w}x${h} ${id}: timeline at ${year}${lit ? ', ' + lit + ' lit' : ''}; ${cards} card(s)`, r.year === year && r.lit === lit && r.cards === cards, JSON.stringify(r));
      check(`${w}x${h} ${id}: the text ends above the timeline`, r.text < r.top, JSON.stringify(r));
    }
    check(`${w}x${h}: the timeline never moves`, new Set(tops).size === 1, tops.join(','));
    await ctx.close();
  }
  check('no JavaScript errors or warnings', errs.length === 0, errs.join(' | '));
  console.log(failed ? `\n${failed} check(s) FAILED` : '\nall checks passed'); await b.close(); process.exit(failed ? 1 : 0);
})();
