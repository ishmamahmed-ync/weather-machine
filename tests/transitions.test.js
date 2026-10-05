// How the page moves from one slide to the next (design system, Motion).
//   node tests/transitions.test.js http://localhost:8766/weather-machine.html
const { chromium } = require('playwright');
const URL = process.argv[2];
(async () => {
  const b = await chromium.launch(); let failed = 0; const errs = [];
  const check = (n, ok, g) => { if (!ok) failed++; console.log((ok ? 'PASS  ' : 'FAIL  ') + n + (ok ? '' : '   (got: ' + g + ')')); };
  const p = await b.newPage({ viewport: { width: 1440, height: 900 } });
  p.on('pageerror', e => errs.push(e.message));
  await p.goto(URL); await p.waitForTimeout(2000);
  const sample = () => p.evaluate(() => { window.__s = []; const t0 = performance.now(), slide = document.getElementById('slide');
    (function s() { const v = WMSTORY.view(); window.__s.push({ t: performance.now() - t0, op: +getComputedStyle(slide).opacity, c: v.centre, m: v.moving,
      title: slide.querySelector('[data-p="title"]').textContent, label: slide.querySelector('[data-p="label"]').textContent });
      if (performance.now() - t0 < 1800) requestAnimationFrame(s); })(); });
  const R = Math.PI / 180, dist = (a, c) => Math.acos(Math.min(1, Math.sin(a[1] * R) * Math.sin(c[1] * R) + Math.cos(a[1] * R) * Math.cos(c[1] * R) * Math.cos((a[0] - c[0]) * R))) / R;
  // 1 -> 2: a new title
  await sample(); await p.keyboard.press('Space'); await p.waitForTimeout(2000);
  let s = await p.evaluate(() => window.__s);
  check('slide 1 to 2: the text block fades out completely before the new words appear', Math.min(...s.map(x => x.op)) === 0, Math.min(...s.map(x => x.op)));
  check('no frame shows old and new parts together', s.filter(x => x.label.startsWith('II') !== x.title.startsWith('The weather')).length === 0, '');
  check('the new words are fully back within 1.3 s', s.filter(x => x.t > 1300).every(x => x.op === 1), '');
  const a = s.findIndex(x => x.m), z = s.findIndex((x, i) => i > a && !x.m), total = dist(s[a].c, s[z].c), dur = s[z].t - s[a].t;
  const at = f => { const i = s.findIndex(x => x.t - s[a].t >= dur * f); return dist(s[a].c, s[i].c) / total; };
  check(`the camera eases in (under 10% of the way after 15% of the time; got ${(at(0.15) * 100).toFixed(0)}%)`, at(0.15) < 0.10, at(0.15));
  check(`and eases out (over 90% after 80% of the time; got ${(at(0.8) * 100).toFixed(0)}%)`, at(0.8) > 0.90, at(0.8));
  check(`the move takes 0.5 to 1.2 s (got ${Math.round(dur)} ms for ${total.toFixed(0)}°)`, dur >= 450 && dur <= 1300, dur);
  // 2 -> 3: the same title: only the changed parts fade, the block never does
  await p.evaluate(() => { window.__swaps = 0; new MutationObserver(() => window.__swaps++).observe(document.querySelector('#slide [data-p="title"]'), { childList: true, subtree: true, characterData: true }); });
  await sample(); await p.keyboard.press('Space'); await p.waitForTimeout(2000);
  s = await p.evaluate(() => window.__s);
  check('slide 2 to 3 (same title): the block stays at full opacity', s.every(x => x.op === 1), Math.min(...s.map(x => x.op)));
  check('and the title is never redrawn', (await p.evaluate(() => window.__swaps)) === 0, await p.evaluate(() => window.__swaps));
  check('no JavaScript errors', errs.length === 0, errs.join(' | '));
  console.log(failed ? `\n${failed} check(s) FAILED` : '\nall checks passed'); await b.close(); process.exit(failed ? 1 : 0);
})();
