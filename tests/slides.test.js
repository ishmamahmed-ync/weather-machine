// Every slide of the story, checked against the design system's slide-text rule.
//   node tests/slides.test.js http://localhost:8766/weather-machine.html [screenshot-folder]
// The narrative text sits in one fixed place on every slide (.wm-slide): same top edge,
// same left edge, same type sizes; it fits on screen and stays clear of the globe.
// Runs with reduced motion, so each slide settles at once.
const { chromium } = require('playwright');
const URL = process.argv[2], SHOTS = process.argv[3];
(async () => {
  const browser = await chromium.launch(); let failed = 0;
  const check = (name, ok, got) => { if (!ok) failed++; console.log((ok ? 'PASS  ' : 'FAIL  ') + name + (ok ? '' : `   (got: ${got})`)); };
  for (const [w, h] of [[1440, 900], [1280, 720]]) {
    const ctx = await browser.newContext({ viewport: { width: w, height: h }, reducedMotion: 'reduce' });
    const page = await ctx.newPage(); const errors = [];
    page.on('pageerror', e => errors.push(e.message));
    page.on('console', m => { if ((m.type() === 'error' || m.type() === 'warning') && !/GL Driver Message/.test(m.text())) errors.push(m.text()); });
    await page.goto(URL); await page.waitForTimeout(1200);
    const ids = await page.evaluate(() => [...new Set([...document.querySelectorAll('.step')].map(s => s.dataset.slide))]);
    const rows = [];
    // prototype sections that carry a slide's words: scrolled to their top, their narration must land where the story's does
    const mods = await page.evaluate(() => [...document.querySelectorAll('.mod [data-slide-text]')].map(s => s.dataset.slideText));
    const modRows = [];
    for (const id of mods) {
      await page.evaluate(id => { const s = document.querySelector('[data-slide-text="' + id + '"]').closest('section'); scrollTo(0, s.getBoundingClientRect().top + scrollY); }, id);
      await page.waitForTimeout(400);
      modRows.push(await page.evaluate(id => {
        const slot = document.querySelector('[data-slide-text="' + id + '"]'), blk = slot.closest('.wm-slide');
        const fs = sel => { const n = slot.querySelector(sel); return n ? getComputedStyle(n).fontSize : null; };
        return { id, top: Math.round(slot.querySelector('.wm-label').getBoundingClientRect().top), left: Math.round(slot.getBoundingClientRect().left),
                 title: fs('.wm-display'), lead: fs('.wm-lead'), label: fs('.wm-label'), source: !!blk.querySelector('.wm-source'),
                 shown: slot.textContent.includes(SCENES.find(s => s.id === id).title) };
      }, id));
      if (SHOTS && w === 1440) await page.screenshot({ path: `${SHOTS}/section-${id}.png` });
    }
    for (const id of ids) {
      await page.evaluate(id => { const s = document.querySelector('.step[data-slide="' + id + '"]'); scrollTo(0, s.getBoundingClientRect().top + scrollY); }, id);
      await page.waitForTimeout(350);
      rows.push(await page.evaluate(id => {
        // a flow slide carries its own text block in its step; every other slide uses the fixed one
        const step = document.querySelector('.step[data-slide="' + id + '"]'), flow = step.classList.contains('is-flow');
        const el = flow ? step.querySelector('.wm-slide') : document.getElementById('slide'), r = el.getBoundingClientRect(), lab = el.querySelector('.wm-label').getBoundingClientRect();
        const fs = sel => { const n = el.querySelector(sel); return n ? getComputedStyle(n).fontSize : null; };
        const R = Math.min(innerWidth, innerHeight) * WM.GLOBE.radius, cx = innerWidth * WM.GLOBE.centreX;
        const nar = flow ? Math.max(...[...el.children].filter(c => !c.classList.contains('below') && !c.classList.contains('wm-source')).map(c => c.getBoundingClientRect().right)) : r.right;
        return { id, flow, top: Math.round(lab.top), left: Math.round(r.left), right: Math.round(nar), bottom: flow ? 0 : Math.round(r.bottom),
                 title: fs('.wm-display'), lead: fs('.wm-lead'), label: fs('.wm-label'), source: !!el.querySelector('.wm-source'),
                 globeLeft: Math.round(cx - R), shown: el.textContent.includes(SCENES.find(s => s.id === id).title) };
      }, id));
      if (SHOTS && w === 1440) await page.screenshot({ path: `${SHOTS}/slide-${String(rows.length).padStart(2, '0')}-${id}.png` });
    }
    const one = k => [...new Set(rows.map(r => r[k]).filter(v => v !== null))];   // a title-only slide (e.g. 'question') has no narration
    check(`${w}x${h}: ${rows.length} slides, each showing its own title`, rows.every(r => r.shown), rows.filter(r => !r.shown).map(r => r.id).join(' '));
    check(`${w}x${h}: the text starts at the same top edge on every slide`, one('top').length === 1, JSON.stringify(one('top')));
    check(`${w}x${h}: and the same left edge`, one('left').length === 1, JSON.stringify(one('left')));
    check(`${w}x${h}: one title size, one narration size, one label size`, one('title').length === 1 && one('lead').length === 1 && one('label').length === 1,
      JSON.stringify([one('title'), one('lead'), one('label')]));
    check(`${w}x${h}: narration is 18px (.wm-lead, 1.125rem) and labels .66rem`, one('lead')[0] === '18px' && one('label')[0] === '10.56px', JSON.stringify([one('lead'), one('label')]));
    // a slide that shows nothing to cite (no layers, no narration: 'question', the empty globe) needs no source
    const bareIds = await page.evaluate(() => SCENES.filter(s => !(s.text || []).length && (s.views || []).every(v => !Object.values(v.layers || {}).some(a => a > 0))).map(s => s.id));
    const bare = id => bareIds.includes(id);
    check(`${w}x${h}: every slide has a source line`, rows.every(r => r.source || bare(r.id)), rows.filter(r => !r.source && !bare(r.id)).map(r => r.id).join(' '));
    const over = rows.filter(r => r.bottom > h - 8);
    check(`${w}x${h}: every slide's text fits on screen`, over.length === 0, over.map(r => `${r.id} ends at ${r.bottom}px`).join(', '));
    const hit = rows.filter(r => r.right > r.globeLeft + 4);
    check(`${w}x${h}: the text column stays clear of the globe`, hit.length === 0, hit.map(r => `${r.id} ${r.right} > ${r.globeLeft}`).join(', '));
    check(`${w}x${h}: no JavaScript errors or warnings`, errors.length === 0, errors.join(' | '));
    const st = rows[0];
    check(`${w}x${h}: ${modRows.length} prototype sections and ${rows.filter(r => r.flow).length} flow slides carry their slide's words`, modRows.every(r => r.shown && r.source), JSON.stringify(modRows.map(r => r.id)));
    check(`${w}x${h}: in each section the words start exactly where the story's do`, modRows.every(r => r.top === st.top && r.left === st.left), JSON.stringify(modRows.map(r => [r.id, r.top, r.left])) + ' vs ' + st.top + ',' + st.left);
    check(`${w}x${h}: and in the same sizes`, modRows.every(r => r.title === st.title && r.lead === st.lead && r.label === st.label), JSON.stringify(modRows));
    if (w === 1440) console.log('      title size ' + one('title') + ', text top ' + one('top') + 'px, tallest slide ends at ' + Math.max(...rows.map(r => r.bottom)) + 'px');
    await ctx.close();
  }
  console.log(failed ? `\n${failed} check(s) FAILED` : '\nall checks passed'); await browser.close(); process.exit(failed ? 1 : 0);
})();
