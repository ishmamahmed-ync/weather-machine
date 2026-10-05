// Slide 17 "How about the place you were born?" (prototypes/country-profile/story-plugin.js) on the final page's shared globe.
//   node tests/profile.test.js http://localhost:8766/weather-machine.html
// Reduced motion, so every camera move lands at once. Expected figures were recomputed from the raw files
// (EM-DAT 2000-2025, IDMC 2008-2025) on 5 Oct 2026, independently of build_globe.py.
const { chromium } = require('playwright');
const URL = process.argv[2];
(async () => {
  const b = await chromium.launch(); let failed = 0; const errs = [];
  const check = (n, ok, g) => { if (!ok) failed++; console.log((ok ? 'PASS  ' : 'FAIL  ') + n + (ok ? '' : '   (got: ' + g + ')')); };
  for (const [w, h] of [[1440, 900], [1280, 720]]) {
    const ctx = await b.newContext({ viewport: { width: w, height: h }, reducedMotion: 'reduce' }), p = await ctx.newPage();
    p.on('pageerror', e => errs.push(e.message)); p.on('console', m => { if ((m.type() === 'warning' || m.type() === 'error') && !/GL Driver|willRead/.test(m.text())) errs.push(m.text()); });
    await p.goto(URL); await p.waitForTimeout(1200);
    const go = async n => { await p.evaluate(n => { const s = [...document.querySelectorAll('.step[data-slide="born"]')][n]; scrollTo(0, s.getBoundingClientRect().top + scrollY); }, n); await p.waitForTimeout(900); };
    const read = () => p.evaluate(() => {
      const bars = [...document.querySelectorAll('.cp-bars .wm-bar')];
      return {
        lead: document.querySelector('#slide .text .wm-lead').textContent,
        ks: bars.map(x => x.querySelector('.k').textContent), vs: bars.map(x => x.querySelector('.v').textContent),
        lefts: [...new Set(bars.map(x => Math.round(x.getBoundingClientRect().left)))],
        pairs: bars.map(x => [...x.querySelectorAll('.track .fill')].map(f => [Math.round(f.getBoundingClientRect().height), getComputedStyle(f).backgroundColor])),
        bottom: Math.round(document.getElementById('slide').getBoundingClientRect().bottom),
        view: WMSTORY.view(), scroll: scrollY };
    });

    await go(0);
    let r = await read();
    check(`${w}x${h} empty: the author's words, four bars with dashes`, /^Enter your country and birth year/.test(r.lead) && r.vs.length === 4 && r.vs.every(v => v === '–'), JSON.stringify(r));

    await p.selectOption('#cp-country', 'BGD'); await p.fill('#cp-born', '2000'); await p.selectOption('#cp-ref', 'DEU'); await p.locator('#cp-born').blur();
    await p.waitForTimeout(500); r = await read();
    check(`${w}x${h} Bangladesh, born 2000: the narration becomes the finding (3,581 killed, 114 million affected, 12 million displacements)`,
      r.lead === 'Since 2000, the year you were born, floods have killed 3,581 people in Bangladesh, affected 114 million, and forced people from their homes 12 million times.', r.lead);
    check(`${w}x${h}: the four bars, in order, Germany for comparison`,
      r.ks.join('|') === 'Deaths|Affected|At risk of a 1-in-100-year flood|Displacements' && /^3,581\s*vs 286/.test(r.vs[0]) && /^94\s*million\s*vs 14 million/.test(r.vs[2]), JSON.stringify([r.ks, r.vs]));
    check(`${w}x${h}: one bar per line (all start at the same left edge)`, r.lefts.length === 1, JSON.stringify(r.lefts));
    check(`${w}x${h}: the comparison bar is white and as thick as your country's`,
      r.pairs.every(([a, b]) => b && a[0] === b[0] && b[1] === 'rgb(236, 234, 229)'), JSON.stringify(r.pairs));
    check(`${w}x${h}: the globe turned to Bangladesh`, Math.abs(r.view.centre[0] - 90.2) < 2 && Math.abs(r.view.centre[1] - 23.9) < 2, JSON.stringify(r.view));
    check(`${w}x${h}: it fits on screen`, r.bottom <= h - 8, r.bottom);

    await p.fill('#cp-born', '1990'); await p.waitForTimeout(200); r = await read();
    check(`${w}x${h} born 1990: the records start in 2000, and the sentence says so`, /^Since 2000, when the records begin \(you were born in 1990\), floods have killed 3,581/.test(r.lead), r.lead);
    await p.fill('#cp-born', '2000');

    await p.click('.cp-panel .wm-btn[data-mode="all"]'); await p.waitForTimeout(300); r = await read();
    check(`${w}x${h} Others: all weather and climate disasters, with the flood share (63% of the affected)`,
      /weather and climate disasters have killed 11,691/.test(r.lead) && r.ks[1] === 'Affected · 63% floods', JSON.stringify([r.lead, r.ks]));
    check(`${w}x${h} Others fits on screen`, r.bottom <= h - 8, r.bottom);
    await p.click('.cp-panel .wm-btn[data-mode="flood"]');

    const y0 = await p.evaluate(() => scrollY);
    await p.fill('#cp-born', ''); for (const k of ['1', '9', '0', '0', ' ']) await p.locator('#cp-born').press(k);
    r = await read();
    check(`${w}x${h}: 1900 is refused (marked, the finding stays); Space in the field does not move the page`,
      await p.evaluate(() => document.getElementById('cp-born').classList.contains('is-bad')) && /^Since 2000, the year/.test(r.lead) && Math.abs(r.scroll - y0) < 2, JSON.stringify(r));
    await p.fill('#cp-born', '2000');

    check(`${w}x${h}: one step only (the rain-gauge half is dropped)`, await p.evaluate(() => document.querySelectorAll('.step[data-slide="born"]').length === 1 && !document.querySelector('.cp-gauge')), '');

    await p.evaluate(() => { const s = document.querySelector('.step[data-slide="frontline"]'); scrollTo(0, s.getBoundingClientRect().top + scrollY); }); await p.waitForTimeout(900);
    r = await p.evaluate(() => WMSTORY.view());
    check(`${w}x${h}: the next slide takes the globe away from Bangladesh`, Math.abs(r.centre[0] - 90.2) > 10, JSON.stringify(r));
    await go(0); r = await read();
    check(`${w}x${h}: coming back, the finding is still there`, /^Since 2000, the year you were born/.test(r.lead), r.lead);
    await ctx.close();
  }
  check('no JavaScript errors or warnings', errs.length === 0, errs.join(' | '));
  console.log(failed ? `\n${failed} check(s) FAILED` : '\nall checks passed'); await b.close(); process.exit(failed ? 1 : 0);
})();
