// Copied from prototypes/rain-gauges/INTEGRATION.md section 9 (the author's acceptance test).
// Changes: Playwright is required from this repo's node_modules, not a path on another machine; and (5 Oct 2026) the
// expected values follow the design system: globe at 70% of the width (radius min(0.42 of the shorter side, 0.30 of the
// width less 8)), pinned to the screen while the narration and panel scroll; round legend swatches.
// Smoke test for the rain-gauge SCENE.   Usage:  node smoke_scene.js <url-or-file-url>
// Needs:  npm i playwright && npx playwright install chromium
// RG_SCROLL=1 scrolls the section into view first (use it on the combined page).
// Inside the main page set RG_EMBEDDED=1: the scene is scrolled into view first, the "only d3" global check is skipped,
// and on phones the globe is expected to pin at the top-bar offset (--rg-topbar) instead of 0.
// Every id is prefixed rg-; if you rename anything while integrating, change the SEL map.
const { chromium } = require('playwright');
const SEL = { scene: '#rg-scene', panel: '#rg-panel', canvas: '#rg-globe', chart: '#rg-chart', squares: '#rg-chart .bub rect', diamonds: '#rg-chart path.dia', card: '#rg-card', tabinfo: '#rg-tabinfo', cap: '#rg-gcap', tip: '#rg-gtip', ring: '#rg-gSel rect.ring.sq', labelRing: '#rg-gSel rect.ring:not(.sq)' };
const EXPECT_SQUARES = { 'Plains': 2320, 'Hilly': 1516, 'Mountains': 2306, 'Coastal': 77, 'Islands': 282, 'Urban': 1088, 'Polar/Arid': 714 };   // total 8,303
(async () => {
  const browser = await chromium.launch(); let failed = 0;
  const check = (name, ok, got) => { if (!ok) failed++; console.log((ok ? 'PASS  ' : 'FAIL  ') + name + (ok ? '' : `   (got: ${got})`)); };
  const errors = [];
  const open = async (w, h, touch) => { const ctx = await browser.newContext({ viewport: { width: w, height: h }, isMobile: !!touch, hasTouch: !!touch }); const p = await ctx.newPage(); p.on('pageerror', e => errors.push(e.message)); await p.goto(process.argv[2]); await p.waitForTimeout(process.env.RG_EMBEDDED ? 1800 : 900); if (process.env.RG_EMBEDDED || process.env.RG_SCROLL) { await p.evaluate(() => document.querySelector('#rg-scene').scrollIntoView()); await p.waitForTimeout(900); } return p; };

  /* ---------- desktop 1440 x 900 ---------- */
  const page = await open(1440, 900);
  const card = async () => (await page.locator(SEL.card).innerText()).replace(/\s+/g, ' ');
  const clickTop = async () => { const pt = await page.evaluate(sel => { let best; document.querySelectorAll(sel).forEach(r => { const y = +r.getAttribute('y'); if (!best || y < best.y) best = { x: +r.getAttribute('x') + +r.getAttribute('width') / 2, y, h: +r.getAttribute('height') }; }); const b = document.querySelector('#rg-chart').getBoundingClientRect(); return { x: b.left + best.x, y: b.top + best.y + best.h / 2 }; }, SEL.squares); await page.mouse.click(pt.x, pt.y); await page.waitForTimeout(300); };
  const diamondClass = i => page.evaluate(([s, i]) => document.querySelectorAll(s)[i].getAttribute('class'), [SEL.diamonds, i]);
  const clickDiamond = async i => { const pt = await page.evaluate(([s, i]) => { const d = document.querySelectorAll(s)[i].getAttribute('d').match(/M([\d.]+) ([\d.]+)L/), b = document.querySelector('#rg-chart').getBoundingClientRect(); return { x: b.left + +d[1], y: b.top + +d[2] + 9.5 }; }, [SEL.diamonds, i]); await page.mouse.click(pt.x, pt.y); await page.waitForTimeout(300); };

  // 1. layout: bordered chart panel on the left, unframed globe on the right
  const L = await page.evaluate(([S, P, C]) => { const s = document.querySelector(S).getBoundingClientRect(), p = document.querySelector(P), pr = p.getBoundingClientRect(), cv = document.querySelector(C), cr = cv.getBoundingClientRect(), wrap = getComputedStyle(cv.parentElement);
    return { scene: [Math.round(s.width), Math.round(s.height)], panelLeft: pr.left < s.width / 2 && pr.right < s.width * 0.55, panelBorder: getComputedStyle(p).borderTopWidth, canvasBorder: getComputedStyle(cv).borderTopWidth, wrapBorder: wrap.borderTopWidth, wrapBg: wrap.backgroundColor, wrapRadius: wrap.borderTopLeftRadius, canvasCoversScene: Math.abs(cr.width - s.width) < 1 && Math.abs(cr.height - innerHeight) < 1, pinned: wrap.position === 'sticky', selects: document.querySelectorAll(S + ' select').length, bullets: document.querySelectorAll(S + ' ul, ' + S + ' li').length, highlightButtons: [...document.querySelectorAll(S + ' button')].filter(b => /highlight/i.test(b.textContent)).length }; }, [SEL.scene, SEL.panel, SEL.canvas]);
  check('scene is the full width, at least the screen tall, with the globe pinned to the screen', L.scene[0] === 1440 && L.scene[1] >= 898 && L.pinned, JSON.stringify([L.scene, L.pinned]));
  check('chart panel is on the left and has a 1px border', L.panelLeft && L.panelBorder === '1px', JSON.stringify([L.panelLeft, L.panelBorder]));
  check('globe has no border, no radius, no box background', L.canvasBorder === '0px' && L.wrapBorder === '0px' && L.wrapRadius === '0px' && /rgba\(0, 0, 0, 0\)|transparent/.test(L.wrapBg), JSON.stringify([L.canvasBorder, L.wrapBorder, L.wrapRadius, L.wrapBg]));
  check('globe canvas fills the screen (full bleed)', L.canvasCoversScene, '');
  check('no country menu, no "highlight" button, no bullet lists', L.selects === 0 && L.highlightButtons === 0 && L.bullets === 0, JSON.stringify([L.selects, L.highlightButtons, L.bullets]));
  // sphere centred at 70% of the width: opaque just inside the right edge, transparent just outside it
  const edge = await page.evaluate(sel => { const c = document.querySelector(sel), x = c.getContext('2d'), W = c.getBoundingClientRect().width, H = c.getBoundingClientRect().height, dpr = c.width / W, GCX = W * 0.70, R = Math.min(Math.min(W, H) * 0.42, W * 0.30 - 8); const a = px => x.getImageData(Math.round(px * dpr), Math.round(H / 2 * dpr), 1, 1).data[3]; return { inside: a(GCX + R - 4), outside: a(GCX + R + 6), centre: a(GCX) }; }, SEL.canvas);
  check('sphere is centred at 70% of the width (edge pixels)', edge.inside > 0 && edge.outside === 0 && edge.centre > 0, JSON.stringify(edge));

  // 2. chart data
  for (const [name, n] of Object.entries(EXPECT_SQUARES)) {
    await page.getByRole('tab', { name, exact: true }).click(); await page.waitForTimeout(250);
    const got = await page.locator(SEL.squares).count(); check(`${name}: ${n} squares`, got === n, got);
    check(`${name}: 6 diamonds`, (await page.locator(SEL.diamonds).count()) === 6, await page.locator(SEL.diamonds).count());
  }
  await page.getByRole('tab', { name: 'Plains', exact: true }).click(); await page.waitForTimeout(250);
  const info = (await page.locator(SEL.tabinfo).innerText()).replace(/\s+/g, ' ');
  check('Plains summary line (one line)', info === 'Plains · WMO minimum 1.74 per 1,000 km² · 2,320 of 4,130 cells have a gauge', info);
  check('summary stays on one line', (await page.locator(SEL.tabinfo).evaluate(e => e.getBoundingClientRect().height)) < 24, '');
  await clickTop(); let c = await card();
  check('Plains: the highest square is China, 35.8, 31.2°N 118.5°E', /China/.test(c) && /35\.8 gauges/.test(c) && /31\.2°N, 118\.5°E/.test(c), c.slice(0, 120));
  check('a square ring is drawn on the selected square', (await page.locator(SEL.ring).count()) === 1, '');
  check('globe caption names it', /China/.test(await page.locator(SEL.cap).innerText()), '');
  await clickDiamond(2); c = await card();
  check('Africa diamond: average 0.086, 405 cells with no gauge', /Africa average/.test(c) && /0\.086 gauges/.test(c) && /405 cells \(63%\)/.test(c), c.slice(0, 140));
  check('Africa diamond is "below", N. America diamond is "meets"', /\blo\b/.test(await diamondClass(2)) && /\bhi\b/.test(await diamondClass(4)), '');
  await page.keyboard.press('Escape'); check('Escape clears the selection', /Each square is one/.test(await card()), (await card()).slice(0, 60));
  await page.getByRole('tab', { name: 'Urban', exact: true }).click(); await page.waitForTimeout(250); await clickTop(); c = await card();
  check('Urban: the highest square is the US cell at 122.1', /United States/.test(c) && /122\.1 gauges/.test(c), c.slice(0, 120));
  await page.getByRole('tab', { name: 'Plains', exact: true }).click(); await page.waitForTimeout(250);

  // 2b. markers: every cell is the same size and square (height alone carries the density), and the legend swatches match
  { const m = await page.evaluate(() => { const rs = [...document.querySelectorAll('#rg-chart .bub rect')], w = new Set(rs.map(r => r.getAttribute('width'))), h = new Set(rs.map(r => r.getAttribute('height'))), sw = getComputedStyle(document.querySelector('.rg-legend .rg-sw')).borderTopLeftRadius;
      return { n: rs.length, widths: [...w], heights: [...h], circles: document.querySelectorAll('#rg-chart .bub circle').length, swatchRadius: sw }; });
    check('every Plains cell is the same size and square', m.n === 2320 && m.widths.length === 1 && m.heights.length === 1 && m.widths[0] === m.heights[0] && m.circles === 0, JSON.stringify(m));
    check('legend swatches are the design system\'s round dots', /50%|^[4-9]/.test(m.swatchRadius), m.swatchRadius); }
  // 3. globe clicks: single click does nothing, double-click selects exactly that cell
  await page.keyboard.press('Escape'); await page.click('#rg-greset');   // chart clicks fly the globe; return to the home view the maths below assumes, and wait until it has stopped moving
  { let last = '', same = 0; for (let t = 0; t < 40 && same < 4; t++) { await page.waitForTimeout(250); const h = await page.evaluate(sel => { const c = document.querySelector(sel), d = c.getContext('2d').getImageData(0, 0, c.width, c.height).data; let x = 0; for (let i = 0; i < d.length; i += 97) x = (x * 31 + d[i]) | 0; return x; }, SEL.canvas); same = h === last ? same + 1 : 0; last = h; } }
  const D = await page.evaluate(() => JSON.parse(document.getElementById('rg-DATA').textContent));
  const fmtD = d => d >= 10 ? d.toFixed(1) : d >= 0.1 ? d.toFixed(2) : d.toFixed(3);
  const cells = []; for (let g = 0; g < 42; g++) { const [s, e] = D.groups[g]; for (let i = s; i < e; i++) cells.push({ cls: Math.floor(g / 6), lon: D.ix[i] + 0.5, lat: D.iy[i] + 0.163017, n: D.n[i], area: D.area[i], ctry: D.ctry[i] }); }
  const box = await page.evaluate(sel => { const r = document.querySelector(sel).getBoundingClientRect(); return { x: r.left, y: r.top, w: r.width, h: r.height }; }, SEL.canvas);
  const GCX = box.x + box.w * 0.70, GCY = box.y + box.h / 2, R = Math.min(Math.min(box.w, box.h) * 0.42, box.w * 0.30 - 8), RAD = Math.PI / 180;
  const proj = (lon, lat) => { const dl = (lon - 15) * RAD, ph = lat * RAD, p0 = 22 * RAD, cosc = Math.sin(p0) * Math.sin(ph) + Math.cos(p0) * Math.cos(ph) * Math.cos(dl); return { x: GCX + R * Math.cos(ph) * Math.sin(dl), y: GCY - R * (Math.cos(p0) * Math.sin(ph) - Math.sin(p0) * Math.cos(ph) * Math.cos(dl)), cosc }; };
  const wpx = c => Math.hypot(proj(c.lon - .5, c.lat).x - proj(c.lon + .5, c.lat).x, proj(c.lon - .5, c.lat).y - proj(c.lon + .5, c.lat).y);
  const vis = cells.filter(c => c.cls === 0 && proj(c.lon, c.lat).cosc > 0.3 && proj(c.lon, c.lat).x > 740 && wpx(c) >= 1.8);   // right of the panel, wide enough to hit
  const before = await card(), q0 = proj(vis.find(c => c.n > 0).lon, vis.find(c => c.n > 0).lat);
  await page.mouse.click(q0.x, q0.y); await page.waitForTimeout(250);
  check('single click on a cell selects nothing', (await card()) === before, (await card()).slice(0, 60));
  let seed = 11; const rnd = () => (seed = (seed * 1664525 + 1013904223) % 4294967296) / 4294967296; let ok = 0; const bad = [];
  for (let i = 0; i < 100; i++) { const c0 = vis[Math.floor(rnd() * vis.length)], q = proj(c0.lon, c0.lat); await page.mouse.dblclick(q.x, q.y); await page.waitForTimeout(16);
    const want = D.countries[c0.ctry] + (c0.n ? '  ' + fmtD(c0.n / c0.area * 1000) + ' per 1,000 km²' : '  no gauge'), got = (await page.locator(SEL.cap).innerText()).replace(/\s+/g, ' ');
    if (got.startsWith(want.replace(/\s+/g, ' '))) ok++; else bad.push([got.slice(0, 50), want]); }
  check(`double-click selects exactly the cell clicked (${ok}/100)`, ok === 100, JSON.stringify(bad.slice(0, 2)));
  const g1 = vis.find(c => c.n > 0), q1 = proj(g1.lon, g1.lat); await page.mouse.dblclick(q1.x, q1.y); await page.waitForTimeout(250);
  check('double-click on a gauged cell rings its square in the chart', (await page.locator(SEL.ring).count()) === 1, await page.locator(SEL.ring).count());
  const g0 = vis.find(c => c.n === 0), q2 = proj(g0.lon, g0.lat); await page.mouse.dblclick(q2.x, q2.y); await page.waitForTimeout(250);
  check('double-click on a grey cell: card says no gauge, label ringed, no square ring', /No gauge in this cell/.test(await card()) && (await page.locator(SEL.labelRing).count()) === 1 && (await page.locator(SEL.ring).count()) === 0, (await card()).slice(0, 70));
  // selecting must not resize anything (the card has a fixed height): check with a cell that carries a note and with a grey cell
  { const geo = () => page.evaluate(([S, C, P]) => [document.querySelector(S).offsetHeight, Math.round(document.querySelector(C).getBoundingClientRect().height), document.querySelector(P).offsetHeight], [SEL.scene, SEL.canvas, SEL.panel]);
    const g0b = await geo(); const india = cells.find(c => c.cls === 0 && D.noteMap && c.n > 0 && D.countries[c.ctry] === 'India' && proj(c.lon, c.lat).cosc > 0.3 && proj(c.lon, c.lat).x > 740);
    if (india) { const qi = proj(india.lon, india.lat); await page.mouse.dblclick(qi.x, qi.y); await page.waitForTimeout(300); }
    const g1b = await geo(); await page.mouse.dblclick(q2.x, q2.y); await page.waitForTimeout(300); const g2b = await geo();
    check('selecting a cell (with or without a note) does not change the scene, panel or globe size', JSON.stringify(g0b) === JSON.stringify(g1b) && JSON.stringify(g0b) === JSON.stringify(g2b), JSON.stringify([g0b, g1b, g2b])); }
  const sel0 = await card(); await page.mouse.move(GCX, GCY); await page.mouse.down(); await page.mouse.move(GCX - 90, GCY + 20, { steps: 8 }); await page.mouse.up(); await page.waitForTimeout(150);
  check('a drag turns the globe and selects nothing', (await card()) === sel0, '');
  await page.mouse.move(q1.x + 400, q1.y); // (moved away) hover on a known cell:
  await page.mouse.move(proj(g1.lon, g1.lat).x, proj(g1.lon, g1.lat).y); await page.waitForTimeout(100);
  // (after the drag the view changed, so just check the tooltip element exists and is hidden over empty space)
  await page.mouse.move(box.x + 6, box.y + box.h - 6); await page.waitForTimeout(80);
  check('globe tooltip hidden over empty space', !(await page.locator(SEL.tip).isVisible()), '');
  const globals = await page.evaluate(() => { const f = document.createElement('iframe'); document.body.appendChild(f); const base = new Set(Object.getOwnPropertyNames(f.contentWindow)); f.remove(); return Object.getOwnPropertyNames(window).filter(k => !base.has(k)); });
  if (!process.env.RG_EMBEDDED) check('only one global added (d3)', globals.length === 1 && globals[0] === 'd3', JSON.stringify(globals));
  await page.close();

  /* ---------- other sizes ---------- */
  for (const [w, h] of [[1280, 720], [1920, 1080], [1024, 768]]) { const p = await open(w, h); const m = await p.evaluate(sel => { const c = document.querySelector('#rg-globe').getBoundingClientRect(); return { over: document.documentElement.scrollWidth > innerWidth, globe: Math.round(c.height), screen: innerHeight, pinned: getComputedStyle(document.querySelector('#rg-globe').parentElement).position === 'sticky' }; }, SEL.scene);
    // a short screen makes the scene taller than the window: the narration and panel scroll beneath the pinned globe
    check(`${w}x${h}: globe pinned and the screen's height, no sideways scroll`, m.pinned && Math.abs(m.globe - m.screen) <= 1 && !m.over, JSON.stringify(m)); await p.close(); }

  /* ---------- phone 390 x 844 ---------- */
  const ph = await open(390, 844, true);
  const pm = await ph.evaluate(sel => { const w = getComputedStyle(document.querySelector('#rg-globe').parentElement); return { pos: w.position, over: document.documentElement.scrollWidth > innerWidth, tabsScroll: document.querySelector('#rg-tabs').scrollWidth > document.querySelector('#rg-tabs').clientWidth }; }, SEL.scene);
  check('phone: stacked layout, globe is sticky, no sideways scroll', pm.pos === 'sticky' && !pm.over, JSON.stringify(pm));
  const sceneTop = await ph.evaluate(() => window.scrollY + document.querySelector('#rg-scene').getBoundingClientRect().top);
  await ph.evaluate(y => window.scrollTo(0, y + 700), sceneTop); await ph.waitForTimeout(300);
  const top = await ph.evaluate(() => Math.round(document.querySelector('#rg-globe').parentElement.getBoundingClientRect().top)), want = await ph.evaluate(() => Math.round(parseFloat(getComputedStyle(document.querySelector('#rg-globe').parentElement).top) || 0));
  check('phone: globe stays pinned at the top (at the top-bar offset) while the panel scrolls', Math.abs(top - want) <= 1, JSON.stringify({ top, want }));
  const R2 = await ph.evaluate(() => { const c = document.querySelector('#rg-globe').getBoundingClientRect(); return [Math.round(c.width), Math.round(c.height)]; }); check('phone: globe canvas is wider than tall and under 340px', R2[1] <= 340, JSON.stringify(R2));
  await ph.close();

  check('no JavaScript errors', errors.length === 0, errors.join(' | '));
  console.log(failed ? `\n${failed} check(s) FAILED` : '\nall checks passed'); await browser.close(); process.exit(failed ? 1 : 0);
})();
