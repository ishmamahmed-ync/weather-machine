// The closing slides (22 to 27 since 7 Oct): the Africa decay map, the geopolitics stops, the US timeline, the dial, the ending.   node tests/ending.test.js http://localhost:8766/weather-machine.html
const { chromium } = require('playwright');
const URL = process.argv[2];
(async () => {
  const b = await chromium.launch(); let failed = 0; const errs = [];
  const check = (n, ok, g) => { if (!ok) failed++; console.log((ok ? 'PASS  ' : 'FAIL  ') + n + (ok ? '' : '   (got: ' + g + ')')); };
  const watch = p => { p.on('pageerror', e => errs.push(e.message)); p.on('console', m => { if ((m.type() === 'warning' || m.type() === 'error') && !/GL Driver|willRead/.test(m.text())) errs.push(m.text()); }); };
  const go = (p, id, n = 0) => p.evaluate(([id, n]) => { const s = [...document.querySelectorAll('.step[data-slide="' + id + '"]')][n]; scrollTo(0, s.getBoundingClientRect().top + scrollY); }, [id, n]);

  for (const [w, h] of [[1440, 900], [1280, 720]]) {
    const ctx = await b.newContext({ viewport: { width: w, height: h }, reducedMotion: 'reduce' }), p = await ctx.newPage(); watch(p);
    await p.goto(URL); await p.waitForTimeout(1200);
    const bottom = () => p.evaluate(() => Math.round(document.getElementById('slide').getBoundingClientRect().bottom));

    await go(p, 'not-enough'); await p.waitForTimeout(900);
    let r = await p.evaluate(() => ({ yr: document.querySelector('#slide [data-year="sweep"]').textContent, n: document.querySelector('#slide [data-count="sweep"]').textContent }));
    check(`${w}x${h} not enough: the counter ends in 2025 with 399 African cells reporting`, r.yr === '2025' && /^399 cells/.test(r.n), JSON.stringify(r));

    // slide 23 (7 Oct): two stops, the Indus then the Russian Arctic; each shows its own pair of year cards
    const stops = [['1960,2025', 'st_flk_indus', 72], ['2022,2024', 'st_flk_ru', 45]];
    for (const n of [0, 1]) {
      await go(p, 'geopolitics', n); await p.waitForTimeout(1200);
      r = await p.evaluate(() => ({ years: [...document.querySelectorAll('#slide .wm-yearset')].filter(x => getComputedStyle(x).display !== 'none')
        .flatMap(x => [...x.querySelectorAll('.wm-stat')].map(y => y.textContent)).join(), lon: Math.round(WMSTORY.view().centre[0]) }));
      check(`${w}x${h} geopolitics, stop ${n + 1}: only its two year cards (${stops[n][0]}), the globe on lon ${stops[n][2]}`,
        r.years === stops[n][0] && Math.abs(r.lon - stops[n][2]) < 2, JSON.stringify(r));
      check(`${w}x${h} geopolitics, stop ${n + 1} fits on screen`, await bottom() <= h - 8, await bottom());
    }
    await go(p, 'fraying'); await p.waitForTimeout(900);
    const a = await p.evaluate(() => [...document.querySelectorAll('#slide .wm-events li')].length);
    check(`${w}x${h} decline in cooperation: the timeline has the 4 US events`, a === 4, a);
    // the vertical timeline: in date order, every row on its own line (no two rows overlap), inside the column
    r = await p.evaluate(() => { const li = [...document.querySelectorAll('#slide .wm-events li')], rs = li.map(x => x.getBoundingClientRect()), box = document.querySelector('#slide .below').getBoundingClientRect();
      const months = { Jan:1, Feb:2, Mar:3, Apr:4, Early:1, By:12 }, when = li.map(x => x.querySelector('.when').textContent);
      const key = s => { const [m, y] = s.split(' '); return +y * 12 + (months[m] || 6); };
      let hit = 0; for (let i = 1; i < rs.length; i++) if (rs[i].top < rs[i - 1].bottom - 1) hit++;
      return { when: when.join(', '), sorted: when.every((s, i) => !i || key(when[i - 1]) <= key(s)), hit, inside: rs.every(x => x.right <= box.right + 1) }; });
    check(`${w}x${h} pulling back: vertical, in date order, one event a row, inside the column`, r.sorted && r.hit === 0 && r.inside, JSON.stringify(r));
    check(`${w}x${h} pulling back fits on screen`, await bottom() <= h - 8, await bottom());

    await go(p, 'money'); await p.waitForTimeout(900);
    r = await p.evaluate(() => ({ rings: document.querySelectorAll('#slide .wm-dial circle.val').length, stats: [...document.querySelectorAll('#slide .wm-dial .wm-stat')].map(x => x.textContent).join(' | '),
      cap: (document.querySelector('#slide .wm-dial .cap') || {}).textContent }));
    check(`${w}x${h} money: the dial (one lap and more) with its two numbers`, r.rings === 2 && r.stats === 'US$400 million | 1 hour 13 minutes' && /about US\$330 million/.test(r.cap), JSON.stringify(r));

    await go(p, 'end'); await p.waitForTimeout(900);
    r = await p.evaluate(() => ({ end: [...document.querySelectorAll('#slide .end .wm-quote')].map(x => x.textContent).join(' '), view: WMSTORY.view() }));
    check(`${w}x${h} the end: the end card, the whole globe`, r.end === 'Weather stations. Rain gauges. River gauges. Radiosondes. Collective Planetary Stewardship.' && Math.abs(r.view.zoom - 0.84) < 0.01, JSON.stringify(r));
    check(`${w}x${h} the end fits on screen`, await bottom() <= h - 8, await bottom());

    // the last slide: four link cards, each opening in a new tab
    await go(p, 'resources'); await p.waitForTimeout(900);
    r = await p.evaluate(() => [...document.querySelectorAll('#slide .wm-links a')].map(a => [a.querySelector('.wm-label').textContent, a.href, a.target]));
    check(`${w}x${h} help close the gaps: Learn, Build, Donate, Volunteer, each a link out in a new tab`,
      r.map(x => x[0]).join() === 'Learn,Build,Donate,Volunteer' && r.every(x => /^https:\/\//.test(x[1]) && x[2] === '_blank'), JSON.stringify(r));
    check(`${w}x${h} help close the gaps fits on screen`, await bottom() <= h - 8, await bottom());
    await ctx.close();
  }

  // with motion: the counter runs, and the last slide pulls out slowly
  const p = await (await b.newContext({ viewport: { width: 1440, height: 900 } })).newPage(); watch(p);
  await p.goto(URL); await p.waitForTimeout(1200);
  await go(p, 'not-enough'); await p.waitForTimeout(700);
  const y1 = +(await p.evaluate(() => document.querySelector('#slide [data-year="sweep"]').textContent));
  await p.waitForTimeout(3000);
  const y2 = +(await p.evaluate(() => document.querySelector('#slide [data-year="sweep"]').textContent));
  check('slide 19 with motion: the year counter advances', y1 < 1980 && y2 > y1 + 10, y1 + ' → ' + y2);
  // the end (since 5 Oct): no zooming; the globe turns back to the equator view at the same distance, rotates, and
  // the sensors fill in year by year (1 s a decade)
  await go(p, 'money'); await p.waitForTimeout(1500);   // the slide before the end since 7 Oct
  const z0 = await p.evaluate(() => WMSTORY.view().zoom);
  await go(p, 'end'); await p.waitForTimeout(1200);
  const v1 = await p.evaluate(() => WMSTORY.view()); await p.waitForTimeout(2500);
  const v2 = await p.evaluate(() => WMSTORY.view());
  check('the end with motion: no zoom in or out from the slide before, back to the equator view, turning',
    Math.abs(v1.zoom - z0) < 0.01 && Math.abs(v2.zoom - z0) < 0.01 && Math.abs(v1.centre[1] - 20) < 3 && Math.abs(v2.centre[0] - v1.centre[0]) > 5, JSON.stringify([z0, v1, v2]));

  check('no JavaScript errors or warnings', errs.length === 0, errs.join(' | '));
  console.log(failed ? `\n${failed} check(s) FAILED` : '\nall checks passed'); await b.close(); process.exit(failed ? 1 : 0);
})();
