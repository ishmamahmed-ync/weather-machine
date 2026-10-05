// Idai (prototypes/idai) on the final page's shared globe.
//   node tests/idai.test.js http://localhost:8766/weather-machine.html
// Reduced motion, so every move and every beat lands at once.
const { chromium } = require('playwright');
const URL = process.argv[2];
(async () => {
  const b = await chromium.launch(); let failed = 0; const errs = [];
  const check = (n, ok, g) => { if (!ok) failed++; console.log((ok ? 'PASS  ' : 'FAIL  ') + n + (ok ? '' : '   (got: ' + g + ')')); };
  for (const [w, h] of [[1440, 900], [1280, 720]]) {
    const ctx = await b.newContext({ viewport: { width: w, height: h }, reducedMotion: 'reduce' }), p = await ctx.newPage();
    p.on('pageerror', e => errs.push(e.message)); p.on('console', m => { if ((m.type() === 'warning' || m.type() === 'error') && !/GL Driver|willRead/.test(m.text())) errs.push(m.text()); });
    await p.goto(URL); await p.waitForTimeout(1200);
    const go = async (id, n = 0) => { await p.evaluate(([id, n]) => { const s = [...document.querySelectorAll('.step[data-slide="' + id + '"]')][n]; scrollTo(0, s.getBoundingClientRect().top + scrollY); }, [id, n]); await p.waitForTimeout(700); };
    for (const [id, n, photo] of [['mozambique', 0, 'idai-floodplain'], ['beyond', 0, 'idai-cow'], ['beyond-grid', 0, 'idai-pylons']]) {
      await go(id, n);
      const r = await p.evaluate(ph => { const f = document.querySelector('#photo .wm-frame').getBoundingClientRect(), mv = WM.miniView(innerWidth, innerHeight),
        txt = Math.max(...[...document.querySelectorAll('#slide > *')].map(e => e.getBoundingClientRect().right)), img = document.querySelector('#photo img').src;
        return { cornerX: Math.round(f.right - mv.cx), cornerY: Math.round(f.top - mv.cy), gap: Math.round(f.left - txt), shown: document.body.hasAttribute('data-photo'),
                 right: img === (WMSTORY.photos || {})[ph], fits: f.bottom <= innerHeight }; }, photo);
      check(`${w}x${h} ${id} ${n + 1}: the photo shows, framed, the right one`, r.shown && r.right, JSON.stringify(r));
      check(`${w}x${h} ${id} ${n + 1}: the corner lens is centred on the photo's top-right corner`, Math.abs(r.cornerX) <= 1 && Math.abs(r.cornerY) <= 1, JSON.stringify(r));
      check(`${w}x${h} ${id} ${n + 1}: the photo clears the words and fits the screen`, r.gap >= 16 && r.fits, JSON.stringify(r));
    }
    await go('three-storms');
    const beats = await p.evaluate(() => [...document.querySelectorAll('#slide .beat .wm-stat')].map(x => x.textContent));
    check(`${w}x${h} three storms: the day counts 52 and 42 are set large`, beats.join() === '52,42', beats.join());
    await go('numbers');
    const nums = await p.evaluate(() => [...document.querySelectorAll('#slide .beat .wm-stat')].map(x => x.textContent));
    check(`${w}x${h} numbers: five figures, one by one`, nums.join('|') === '1.85 million|603|122,700|77|400,000', nums.join('|'));
    await go('who-pays');
    check(`${w}x${h}: after Idai the globe is full size again, no photo`, await p.evaluate(() => !document.body.hasAttribute('data-photo') && !document.querySelector('#photo').classList.contains('on')), '');
    await ctx.close();
  }
  check('no JavaScript errors or warnings', errs.length === 0, errs.join(' | '));
  console.log(failed ? `\n${failed} check(s) FAILED` : '\nall checks passed'); await b.close(); process.exit(failed ? 1 : 0);
})();
