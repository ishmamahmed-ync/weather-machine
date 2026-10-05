// The slide navigator (design system .wm-nav) on the final page.
//   node tests/nav.test.js http://localhost:8766/weather-machine.html
const { chromium } = require('playwright');
const URL = process.argv[2];
(async () => {
  const b = await chromium.launch(); let failed = 0; const errs = [];
  const check = (n, ok, g) => { if (!ok) failed++; console.log((ok ? 'PASS  ' : 'FAIL  ') + n + (ok ? '' : '   (got: ' + g + ')')); };
  const p = await b.newPage({ viewport: { width: 1440, height: 900 } });
  p.on('pageerror', e => errs.push(e.message)); p.on('console', m => { if ((m.type() === 'warning' || m.type() === 'error') && !/GL Driver/.test(m.text())) errs.push(m.text()); });
  await p.goto(URL); await p.waitForTimeout(2000);
  const st = () => p.evaluate(() => {
    const nav = document.querySelector('.wm-nav'), cur = nav.querySelector('[aria-current]'), lines = [...nav.querySelectorAll('.ln')];
    const txt = el => { const r = document.createRange(); r.selectNodeContents(el); return r.getBoundingClientRect(); };
    return { n: SCENES.length, lines: lines.length, acts: nav.querySelectorAll('.act').length, cur: +cur.dataset.i, label: cur.getAttribute('aria-label'),
      lit: [...nav.querySelectorAll('.act.is-on .num')].map(n => n.textContent).join(''), past: nav.querySelectorAll('.ln.is-past').length,
      enabled: lines.filter(l => !l.disabled).length, names: nav.innerText.replace(/\s+/g, ' ').trim(),
      clear: Math.round(txt(document.querySelector('#slide [data-p="label"]')).left - Math.max(...lines.map(l => l.getBoundingClientRect().right))),
      numTop: +txt(nav.querySelector('.num')).top.toFixed(1), labTop: +txt(document.querySelector('#slide [data-p="label"]')).top.toFixed(1),
      brand: Math.round(txt(document.querySelector('#topbar .wm-label')).left), textLeft: Math.round(txt(document.querySelector('#slide [data-p="label"]')).left),
      curW: parseFloat(getComputedStyle(cur, '::before').width), restW: parseFloat(getComputedStyle(lines[lines.length - 1], '::before').width) }; });
  let s = await st();
  check(`one line per slide (${s.n}) in 6 sections, every one clickable`, s.lines === s.n && s.acts === 6 && s.enabled === s.n, JSON.stringify(s));
  check('slide 1 current, section I lit, its line the longest', s.cur === 0 && s.lit === 'I' && s.curW > s.restW, JSON.stringify(s));
  check('only numerals on screen', s.names === 'I II III IV V VI', s.names);
  check('numeral I level with the slide label', Math.abs(s.numTop - s.labTop) < 0.5, s.numTop + ' vs ' + s.labTop);
  check('the site title and the slide text share one left edge', s.brand === s.textLeft, s.brand + ' vs ' + s.textLeft);
  check('the text clears the longest line', s.clear >= 16, s.clear);
  const N = s.n; for (const i of [6, 12, N - 1]) {
    await p.click(`.wm-nav .ln[data-i="${i}"]`); await p.waitForTimeout(2200); s = await st();
    check(`clicking line ${i + 1} jumps there; ${i} lines visited`, s.cur === i && s.past === i, JSON.stringify([s.cur, s.past, s.lit]));
  }
  await p.evaluate(() => document.activeElement && document.activeElement.blur());
  let on = false; for (let k = 0; k < 14 && !on; k++) { await p.keyboard.press('Tab'); on = await p.evaluate(() => document.activeElement.classList.contains('ln')); }
  // Tab passes the page's own controls first (focusing the explorer's tabs scrolls to slide 8): the navigator's one
  // tab stop is whichever line is current when the focus arrives
  const f = await p.evaluate(() => ({ focused: +document.activeElement.dataset.i, cur: +document.querySelector('.wm-nav [aria-current]').dataset.i }));
  check('Tab reaches the current line (one stop for the whole navigator)', on && f.focused === f.cur, JSON.stringify(f));
  await p.keyboard.press('Home'); await p.keyboard.press('Enter'); await p.waitForTimeout(2500); s = await st();
  check('Home then Enter goes back to slide 1', s.cur === 0, s.cur);
  const m = await b.newPage({ viewport: { width: 390, height: 844 }, isMobile: true, hasTouch: true }); await m.goto(URL); await m.waitForTimeout(2000);
  const mm = await m.evaluate(() => ({ nav: getComputedStyle(document.querySelector('.wm-nav')).display, mini: document.querySelector('.wm-nav-mini').textContent }));
  check(`phone: collapses to "I · 1 / ${N}"`, mm.nav === 'none' && mm.mini === 'I · 1 / ' + N, JSON.stringify(mm));
  check('no JavaScript errors or warnings', errs.length === 0, errs.join(' | '));
  console.log(failed ? `\n${failed} check(s) FAILED` : '\nall checks passed'); await b.close(); process.exit(failed ? 1 : 0);
})();
