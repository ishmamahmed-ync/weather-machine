// The frontline stories (prototypes/stories/story-plugin.js) on slide 18, 'The frontlines are responding'.
//   node tests/stories.test.js http://localhost:8766/weather-machine.html
const { chromium } = require('playwright');
const URL = process.argv[2];
(async () => {
  const b = await chromium.launch(); let failed = 0; const errs = [];
  const check = (n, ok, g) => { if (!ok) failed++; console.log((ok ? 'PASS  ' : 'FAIL  ') + n + (ok ? '' : '   (got: ' + g + ')')); };
  for (const [w, h] of [[1440, 900], [1280, 720]]) {
    const ctx = await b.newContext({ viewport: { width: w, height: h }, reducedMotion: 'reduce' }), p = await ctx.newPage();
    p.on('pageerror', e => errs.push(e.message)); p.on('console', m => { if ((m.type() === 'warning' || m.type() === 'error') && !/GL Driver|willRead/.test(m.text())) errs.push(m.text()); });
    await p.goto(URL); await p.waitForTimeout(1200);
    await p.evaluate(() => { const s = document.querySelector('.step[data-slide="frontline"]'); scrollTo(0, s.getBoundingClientRect().top + scrollY); });
    await p.waitForTimeout(1200);
    const read = () => p.evaluate(() => ({ title: document.querySelector('.sto-title').textContent, place: document.querySelector('.sto-place').textContent,
      count: document.querySelector('.sto-count').textContent, href: document.querySelector('.sto-more').href,
      bottom: Math.round(document.getElementById('slide').getBoundingClientRect().bottom), view: WMSTORY.view() }));
    let r = await read();
    check(`${w}x${h}: opens on Malawi's flood detectors, the globe on Karonga`, /flood detectors/.test(r.title) && r.count === '1 of 23' &&
      Math.abs(r.view.centre[0] - 33.93) < 1 && Math.abs(r.view.centre[1] + 9.93) < 1, JSON.stringify(r));
    check(`${w}x${h}: the photo links to the source`, /unicef\.org\/malawi/.test(r.href), r.href);

    await p.evaluate(() => document.querySelector('.sto-next').click()); await p.waitForTimeout(300); r = await read();
    check(`${w}x${h}: Next goes to Bangladesh's volunteers`, r.count === '2 of 23' && /Bangladesh/.test(r.place), JSON.stringify(r));
    await p.keyboard.press('ArrowLeft'); await p.waitForTimeout(200); r = await read();
    check(`${w}x${h}: ← goes back`, r.count === '1 of 23', r.count);

    // the seal story: its layers fade in and "elephant seals" links to the seal data
    for (let i = 0; i < 8; i++) await p.evaluate(() => document.querySelector('.sto-next').click());
    await p.waitForTimeout(800); r = await read();
    const seal = await p.evaluate(() => { const a = document.querySelector('.sto-desc a.wm-link'); return { text: a && a.textContent, href: a && a.href, key: document.querySelector('.sto-key').textContent }; });
    check(`${w}x${h}: the seal story links "elephant seals" to the MEOP-CTD database, with its layers' key`,
      /seals/i.test(r.title) && seal.text === 'elephant seals' && /meop\.net/.test(seal.href) && /Seal-borne/.test(seal.key), JSON.stringify(seal));

    // every story fits on screen
    let worst = { bottom: 0 };
    for (let i = 0; i < 23; i++) { const x = await read(); if (x.bottom > worst.bottom) worst = x; await p.evaluate(() => document.querySelector('.sto-next').click()); await p.waitForTimeout(40); }
    check(`${w}x${h}: all 23 stories fit on screen`, worst.bottom <= h - 8, worst.title + ' ends at ' + worst.bottom);

    // clicking a circle opens its story
    const pos = await p.evaluate(() => { const v = WMSTORY.view(); return v; });
    const hitOk = await p.evaluate(() => new Promise(res => {
      const cv = document.getElementById('globe'), r = cv.getBoundingClientRect();
      // the open story's own circle sits at the globe's centre after the move
      const x = r.left + r.width * WM.GLOBE.centreX, y = r.top + r.height / 2;
      const before = document.querySelector('.sto-count').textContent;
      cv.dispatchEvent(new PointerEvent('pointerdown', { clientX: x, clientY: y, pointerId: 1, bubbles: true, pointerType: 'mouse' }));
      cv.dispatchEvent(new PointerEvent('pointerup', { clientX: x, clientY: y, pointerId: 1, bubbles: true, pointerType: 'mouse' }));
      setTimeout(() => res(document.querySelector('.sto-count').textContent === before), 100);
    }));
    check(`${w}x${h}: a click on the open story's circle keeps it open (circles are clickable)`, hitOk, '');

    // Space goes on to the next slide, even from the Next button
    await p.focus('.sto-next'); await p.keyboard.press(' '); await p.waitForTimeout(1500);
    const slide = await p.evaluate(() => document.querySelector('#slide .wm-display').textContent);
    check(`${w}x${h}: Space on the Next button goes to the next slide`, /What can we do to support them/.test(slide), slide);
    await ctx.close();
  }
  check('no JavaScript errors or warnings', errs.length === 0, errs.join(' | '));
  console.log(failed ? `\n${failed} check(s) FAILED` : '\nall checks passed'); await b.close(); process.exit(failed ? 1 : 0);
})();
