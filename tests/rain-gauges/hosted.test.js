// The rain-gauge explorer on the final page's shared globe (option A, 5 Oct 2026).
//   node tests/rain-gauges/hosted.test.js http://localhost:8766/weather-machine.html
// The same behaviour as the author's smoke_scene.js, but the cells are drawn by the story's globe: the explorer's
// panel sits under slide 8's words ("Cell by cell"), and the globe takes drag, double-click and Ctrl/⌘ + scroll.
const { chromium } = require('playwright');
const URL = process.argv[2];
const EXPECT_SQUARES = { 'Plains': 2320, 'Hilly': 1516, 'Mountains': 2306, 'Coastal': 77, 'Islands': 282, 'Urban': 1088, 'Polar/Arid': 714 };
(async () => {
  const browser = await chromium.launch(); let failed = 0; const errors = [];
  const check = (name, ok, got) => { if (!ok) failed++; console.log((ok ? 'PASS  ' : 'FAIL  ') + name + (ok ? '' : `   (got: ${got})`)); };
  const page = await browser.newPage({ viewport: { width: 1440, height: 900 } });
  page.on('pageerror', e => errors.push(e.message));
  page.on('console', m => { if ((m.type() === 'error' || m.type() === 'warning') && !/GL Driver|willReadFrequently/.test(m.text())) errors.push(m.text()); });
  await page.goto(URL); await page.waitForTimeout(1500);
  await page.evaluate(() => { const s = document.querySelector('.step[data-slide="cells"]'); scrollTo(0, s.getBoundingClientRect().top + scrollY); });
  const settle = async () => { let last = '', same = 0; for (let t = 0; t < 60 && same < 4; t++) { await page.waitForTimeout(150); const h = await page.evaluate(() => { const c = document.getElementById('globe'), d = c.getContext('2d', { willReadFrequently: true }).getImageData(0, 0, c.width, c.height).data; let x = 0; for (let i = 0; i < d.length; i += 997) x = (x * 31 + d[i]) | 0; return x; }); same = h === last ? same + 1 : 0; last = h; } };
  await settle();
  const card = async () => (await page.locator('#rg-card').innerText()).replace(/\s+/g, ' ');

  // 1. one globe: no section of its own, the panel under the slide's words, the globe interactive
  const L = await page.evaluate(() => ({ ownGlobe: !!document.getElementById('rg-globe'), sections: document.querySelectorAll('#story > .mod').length,
    inSlide: !!document.querySelector('.step[data-slide="cells"] .below #rg-panel'), interactive: document.body.hasAttribute('data-interactive'),
    title: document.querySelector('.step[data-slide="cells"] .wm-display').textContent, tools: getComputedStyle(document.getElementById('gtools')).display, toolsBottom: Math.round(innerHeight - document.getElementById('gtools').getBoundingClientRect().bottom), zoomButtons: !!document.getElementById('gzin') }));
  check('one globe: the explorer brings no globe or section of its own', !L.ownGlobe && L.sections === 0, JSON.stringify(L));
  check('its panel sits under the "Cell by cell" words', L.inSlide && /Cell by cell/.test(L.title), JSON.stringify(L));
  check('while the slide is on screen the story globe is interactive, with Reset view at the bottom right', L.interactive && L.tools === 'flex' && L.toolsBottom < 40 && !L.zoomButtons, JSON.stringify(L));

  // 2. the chart, as in smoke_scene.js
  for (const [name, n] of Object.entries(EXPECT_SQUARES)) {
    await page.getByRole('tab', { name, exact: true }).click(); await page.waitForTimeout(150);
    check(`${name}: ${n} squares`, (await page.locator('#rg-chart .bub rect').count()) === n, await page.locator('#rg-chart .bub rect').count());
  }
  await page.getByRole('tab', { name: 'Plains', exact: true }).click(); await page.waitForTimeout(200);
  check('Plains summary line', (await page.locator('#rg-tabinfo').innerText()).replace(/\s+/g, ' ') === 'Plains · WMO minimum 1.74 per 1,000 km² · 2,320 of 4,130 cells have a gauge', await page.locator('#rg-tabinfo').innerText());
  const clickTop = async () => { const pt = await page.evaluate(() => { let best; document.querySelectorAll('#rg-chart .bub rect').forEach(r => { const y = +r.getAttribute('y'); if (!best || y < best.y) best = { x: +r.getAttribute('x') + +r.getAttribute('width') / 2, y, h: +r.getAttribute('height') }; }); const b = document.querySelector('#rg-chart').getBoundingClientRect(); return { x: b.left + best.x, y: b.top + best.y + best.h / 2 }; }); await page.mouse.click(pt.x, pt.y); await page.waitForTimeout(300); };
  const rot0 = await page.evaluate(() => getComputedStyle(document.body).cursor);
  await clickTop(); let c = await card();
  check('Plains: the highest square is China, 35.8, 31.2°N 118.5°E', /China/.test(c) && /35\.8 gauges/.test(c) && /31\.2°N, 118\.5°E/.test(c), c.slice(0, 120));
  await settle();
  const centre = await page.evaluate(() => { const c = document.getElementById('globe'), x = c.getContext('2d', { willReadFrequently: true }), k = c.width / c.clientWidth, d = x.getImageData(Math.round(innerWidth * 0.7 * k), Math.round(innerHeight / 2 * k), 1, 1).data; return [d[0], d[1], d[2]]; });
  check('a chart click flies the shared globe to the cell (the selected cell is now at the globe\'s centre)', centre[1] > 150 && centre[1] > centre[0], JSON.stringify(centre));
  const clickDiamond = async i => { const pt = await page.evaluate(i => { const d = document.querySelectorAll('#rg-chart path.dia')[i].getAttribute('d').match(/M([\d.]+) ([\d.]+)L/), b = document.querySelector('#rg-chart').getBoundingClientRect(); return { x: b.left + +d[1], y: b.top + +d[2] + 9.5 }; }, i); await page.mouse.click(pt.x, pt.y); await page.waitForTimeout(300); };
  await clickDiamond(2); c = await card();
  check('Africa diamond: average 0.086, 405 cells with no gauge', /Africa average/.test(c) && /0\.086 gauges/.test(c) && /405 cells \(63%\)/.test(c), c.slice(0, 140));
  await page.keyboard.press('Escape'); check('Escape clears the selection', /Each square is one/.test(await card()), (await card()).slice(0, 60));
  await page.getByRole('tab', { name: 'Urban', exact: true }).click(); await page.waitForTimeout(200); await clickTop(); c = await card();
  check('Urban: the highest square is the US cell at 122.1', /United States/.test(c) && /122\.1 gauges/.test(c), c.slice(0, 120));
  await page.getByRole('tab', { name: 'Plains', exact: true }).click(); await page.waitForTimeout(200);

  // 3. the shared globe: Reset view returns to the slide's view (lon 15, lat 22, zoom 1); then pick cells by double-click
  await page.click('#greset'); await settle();
  const D = await page.evaluate(() => JSON.parse(document.getElementById('rg-DATA').textContent));
  const fmtD = d => d >= 10 ? d.toFixed(1) : d >= 0.1 ? d.toFixed(2) : d.toFixed(3);
  const cells = []; for (let g = 0; g < 42; g++) { const [s, e] = D.groups[g]; for (let i = s; i < e; i++) cells.push({ cls: Math.floor(g / 6), lon: D.ix[i] + 0.5, lat: D.iy[i] + 0.163017, n: D.n[i], area: D.area[i], ctry: D.ctry[i] }); }
  const W = 1440, Hh = 900, GCX = W * 0.70, GCY = Hh / 2, R = Math.min(W, Hh) * 0.42, RAD = Math.PI / 180;
  const proj = (lon, lat) => { const dl = (lon - 15) * RAD, ph = lat * RAD, p0 = 22 * RAD, cosc = Math.sin(p0) * Math.sin(ph) + Math.cos(p0) * Math.cos(ph) * Math.cos(dl); return { x: GCX + R * Math.cos(ph) * Math.sin(dl), y: GCY - R * (Math.cos(p0) * Math.sin(ph) - Math.sin(p0) * Math.cos(ph) * Math.cos(dl)), cosc }; };
  const wpx = c => Math.hypot(proj(c.lon - .5, c.lat).x - proj(c.lon + .5, c.lat).x, proj(c.lon - .5, c.lat).y - proj(c.lon + .5, c.lat).y);
  const panelRight = await page.evaluate(() => document.getElementById('rg-panel').getBoundingClientRect().right);
  const vis = cells.filter(c => c.cls === 0 && proj(c.lon, c.lat).cosc > 0.3 && proj(c.lon, c.lat).x > panelRight + 20 && proj(c.lon, c.lat).y > 120 && wpx(c) >= 1.8);
  const before = await card(), q0 = proj(vis.find(c => c.n > 0).lon, vis.find(c => c.n > 0).lat);
  await page.mouse.click(q0.x, q0.y); await page.waitForTimeout(250);
  check('single click on a cell selects nothing', (await card()) === before, (await card()).slice(0, 60));
  let seed = 11; const rnd = () => (seed = (seed * 1664525 + 1013904223) % 4294967296) / 4294967296; let ok = 0; const bad = [];
  for (let i = 0; i < 100; i++) { const c0 = vis[Math.floor(rnd() * vis.length)], q = proj(c0.lon, c0.lat); await page.mouse.dblclick(q.x, q.y); await page.waitForTimeout(16);
    const got = (await card()).slice(0, 80), want = D.countries[c0.ctry];
    const wantD = c0.n ? fmtD(c0.n / c0.area * 1000) + ' gauges' : 'No gauge';
    if (got.startsWith(want) && got.includes(wantD)) ok++; else bad.push([got.slice(0, 50), want, wantD]); }
  check(`double-click on the shared globe selects exactly the cell clicked (${ok}/100)`, ok === 100, JSON.stringify(bad.slice(0, 2)));
  const geo = () => page.evaluate(() => [Math.round(document.getElementById('rg-panel').getBoundingClientRect().height), Math.round(document.querySelector('.step[data-slide="cells"]').getBoundingClientRect().height)]);
  const g0 = await geo(); const g1c = vis.find(c => c.n === 0), q2 = proj(g1c.lon, g1c.lat); await page.mouse.dblclick(q2.x, q2.y); await page.waitForTimeout(250);
  check('a grey cell: the card says no gauge', /No gauge in this cell/.test(await card()), (await card()).slice(0, 70));
  check('selecting never resizes the panel or the slide', JSON.stringify(g0) === JSON.stringify(await geo()), JSON.stringify([g0, await geo()]));
  const sel0 = await card(); await page.mouse.move(GCX, GCY); await page.mouse.down(); await page.mouse.move(GCX - 90, GCY + 20, { steps: 8 }); await page.mouse.up(); await page.waitForTimeout(150);
  const turned = await page.evaluate(() => document.body.hasAttribute('data-interactive'));
  check('a drag turns the shared globe and selects nothing', (await card()) === sel0 && turned, '');

  // 4. leaving the slide hands the globe back to the story
  await page.evaluate(() => { const s = document.querySelector('.step[data-slide="cant-see"]'); scrollTo(0, s.getBoundingClientRect().top + scrollY); }); await page.waitForTimeout(800);
  check('the next slide: the globe is the story\'s again (not interactive, no Reset view)', await page.evaluate(() => !document.body.hasAttribute('data-interactive') && getComputedStyle(document.getElementById('gtools')).display === 'none'), '');
  check('no JavaScript errors or warnings', errors.length === 0, errors.join(' | '));
  console.log(failed ? `\n${failed} check(s) FAILED` : '\nall checks passed'); await browser.close(); process.exit(failed ? 1 : 0);
})();
