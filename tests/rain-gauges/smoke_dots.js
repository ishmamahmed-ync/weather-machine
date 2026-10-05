// Copied from prototypes/rain-gauges/INTEGRATION.md section 9 (the author's acceptance test).
// Changes: Playwright is required from this repo's node_modules, not a path on another machine; and (5 Oct 2026) the
// expected values follow the design system: globe centred at 70% of the width, narration in the slide-text block.
// Smoke test for the rain-gauge DOTS MAP (section 1).   Usage:  node smoke_dots.js <url-or-file-url>
// Needs:  npm i playwright && npx playwright install chromium
// RG_SCROLL=1 scrolls the section into view first (use it on the combined page); RG_EMBEDDED=1 does that and also skips the "only d3 added" check (use it inside the main page).
// Every id is prefixed rgm-; if you rename anything while integrating, search for 'rgm-' below.
const { chromium } = require('playwright');
const URL = process.argv[2];
(async () => {
  const browser = await chromium.launch(); let failed = 0; const errors = [];
  const check = (name, ok, got) => { if (!ok) failed++; console.log((ok ? 'PASS  ' : 'FAIL  ') + name + (ok ? '' : `   (got: ${got})`)); };
  const open = async (w, h, touch) => { const ctx = await browser.newContext({ viewport: { width: w, height: h }, isMobile: !!touch, hasTouch: !!touch }); const p = await ctx.newPage(); p.on('pageerror', e => errors.push(e.message)); await p.route(/fonts\.(googleapis|gstatic)\.com/, r => r.abort()); await p.goto(URL); await p.waitForTimeout(process.env.RG_EMBEDDED ? 1800 : 900); if (process.env.RG_EMBEDDED || process.env.RG_SCROLL) { await p.evaluate(() => document.querySelector('#rgm-scene').scrollIntoView()); await p.waitForTimeout(900); } return p; };
  const page = await open(1440, 900);
  const D = await page.evaluate(() => JSON.parse(document.getElementById('rg-DATA').textContent));
  const fmtD = d => d >= 10 ? d.toFixed(1) : d >= 1 ? d.toFixed(2) : d >= 0.1 ? d.toFixed(2) : d.toFixed(3);
  const clsOf = i => { if (D.n[i] === 0) return 0; const d = D.n[i] / D.area[i] * 1000; const E = [0.1, 0.5, 1, 2, 5, 10]; for (let k = 0; k < 6; k++) if (d <= E[k]) return k + 1; return 7; };
  const colours = await page.evaluate(() => { const cs = getComputedStyle(document.getElementById('rgm-scene')); return [0, 1, 2, 3, 4, 5, 6, 7].map(k => { const h = cs.getPropertyValue('--c' + k).trim().replace('#', ''); return [parseInt(h.slice(0, 2), 16), parseInt(h.slice(2, 4), 16), parseInt(h.slice(4, 6), 16)]; }); });
  const GCX = 1440 * 0.70, GCY = 450, R = 0.42 * 900, RAD = Math.PI / 180;   // the design system's globe: 70% across
  const proj = (lon, lat, z = 1, lon0 = 15, lat0 = 22) => { const dl = (lon - lon0) * RAD, ph = lat * RAD, p0 = lat0 * RAD, cosc = Math.sin(p0) * Math.sin(ph) + Math.cos(p0) * Math.cos(ph) * Math.cos(dl); return { x: GCX + R * z * Math.cos(ph) * Math.sin(dl), y: GCY - R * z * (Math.cos(p0) * Math.sin(ph) - Math.sin(p0) * Math.cos(ph) * Math.cos(dl)), cosc }; };
  const N = D.n.length;

  /* 1. layout and legend */
  const L = await page.evaluate(() => { const s = document.getElementById('rgm-scene'), cv = document.getElementById('rgm-globe'), w = cv.parentElement, cs = getComputedStyle(w), c = cv.getBoundingClientRect(), sr = s.getBoundingClientRect(); return { sceneH: Math.round(sr.height), fills: Math.abs(c.width - sr.width) < 1 && Math.abs(c.height - sr.height) < 1, border: cs.borderTopWidth, radius: cs.borderTopLeftRadius, bg: cs.backgroundColor, rows: [...document.querySelectorAll('#rgm-list .rgm-k')].map(e => e.innerText.trim()), title: (document.querySelector('#rgm-scene .wm-display') || document.querySelector('.rgm-title')).innerText, label: /(flood|stream|river) gauge/i.test(document.getElementById('rgm-scene').innerText) }; });
  check('scene fits the viewport', Math.abs(L.sceneH - 900) <= 2, L.sceneH);
  check('the earth has no frame and fills the scene', L.fills && L.border === '0px' && L.radius === '0px' && /rgba\(0, 0, 0, 0\)|transparent/.test(L.bg), JSON.stringify(L));
  check('legend: 8 classes, densest first', JSON.stringify(L.rows) === JSON.stringify(['10 or more', '5 to 10', '2 to 5', '1 to 2', '0.5 to 1', '0.1 to 0.5', 'under 0.1', 'no gauge']), JSON.stringify(L.rows));
  check('labelled as rain gauges, never as flood, stream or river gauges', /rain gauge/i.test(L.title) && !L.label, L.title);

  /* 2. dots: zoomed to 1.96x the pixel at each dot's centre is exactly its class colour, and dot size follows the original's scale/210 */
  for (let k = 0; k < 2; k++) await page.click('#rgm-zin'); await page.waitForTimeout(200);
  const Z2 = Math.pow(1.4, 2), dotPos = (i, q, z) => proj(D.ix[i] + 0.25 + 0.5 * (q & 1), D.iy[i] - 0.25 + 0.5 * (q >> 1), z);
  const cand = []; for (let i = 0; i < N; i++) for (let q = 0; q < 4; q++) { const p = dotPos(i, q, Z2), lat = D.iy[i] - 0.25 + 0.5 * (q >> 1); if (p.cosc > 0.75 && Math.abs(lat) < 50 && p.x > 30 && p.x < 1410 && p.y > 30 && p.y < 870) cand.push([i, q, p]); }
  let seed = 5; const rnd = () => (seed = (seed * 1664525 + 1013904223) % 4294967296) / 4294967296; const sample = Array.from({ length: 200 }, () => cand[Math.floor(rnd() * cand.length)]);
  let okc = 0; const badc = [], seen = new Set();
  for (const [i, q, p] of sample) { const px = await page.evaluate(([x, y]) => { const c = document.getElementById('rgm-globe'), k = c.width / c.getBoundingClientRect().width, d = c.getContext('2d').getImageData(Math.floor(x * k), Math.floor(y * k), 1, 1).data; return [d[0], d[1], d[2]]; }, [p.x, p.y]);
    const w = colours[clsOf(i)]; seen.add(clsOf(i)); if (Math.abs(px[0] - w[0]) <= 2 && Math.abs(px[1] - w[1]) <= 2 && Math.abs(px[2] - w[2]) <= 2) okc++; else badc.push([i, q, px, w, Math.round(Math.hypot(px[0] - w[0], px[1] - w[1], px[2] - w[2]))]); }
  const nearest = px => colours.reduce((bi, c, k) => Math.hypot(px[0] - c[0], px[1] - c[1], px[2] - c[2]) < Math.hypot(px[0] - colours[bi][0], px[1] - colours[bi][1], px[2] - colours[bi][2]) ? k : bi, 0);
  const wrongc = badc.filter(b => nearest(b[2]) !== clsOf(b[0]));   // a mismatch is "wrong" only if the pixel is closer to a different class; otherwise it is a faint country-border line over the dot (borders sit on top once zoomed in)
  check(`the pixel at a dot's centre is its class colour (${okc}/200 exact, ${badc.length - wrongc.length} with a faint border line over them, ${wrongc.length} wrong; ${seen.size} of 8 classes sampled)`, okc >= 190 && wrongc.length === 0 && seen.size >= 6, JSON.stringify(wrongc.slice(0, 2)));
  for (let k = 0; k < 4; k++) await page.click('#rgm-zin'); await page.waitForTimeout(200);          // now 1.4^6 = 7.53x
  const Z6 = Math.pow(1.4, 6), expectSz = R * Z6 / 210;
  let bi = -1, bq = 0, bdist = 1e9; for (let i = 0; i < N; i++) for (let q = 0; q < 4; q++) { const p = dotPos(i, q, Z6); const d = Math.hypot(p.x - GCX, p.y - 450); if (d < bdist && D.n[i] > 0 && Math.abs(p.x - GCX) > 30) { bdist = d; bi = i; bq = q; } }
  const pp = dotPos(bi, bq, Z6), cl = colours[clsOf(bi)];
  const run = await page.evaluate(([x, y, col]) => { const c = document.getElementById('rgm-globe'), k = c.width / c.getBoundingClientRect().width, g = c.getContext('2d'), row = g.getImageData(0, Math.floor(y * k), c.width, 1).data; let n = 0, i = Math.floor(x * k); const m = j => Math.abs(row[j * 4] - col[0]) <= 3 && Math.abs(row[j * 4 + 1] - col[1]) <= 3 && Math.abs(row[j * 4 + 2] - col[2]) <= 3; if (!m(i)) return -1; let a = i, b = i; while (a > 0 && m(a - 1)) a--; while (b < c.width - 1 && m(b + 1)) b++; return (b - a + 1) / k; }, [pp.x, pp.y, cl]);
  check(`dot size follows the original's scale/210 (expected ${expectSz.toFixed(1)} px, measured ${run.toFixed(1)} px)`, run > 0 && Math.abs(run - expectSz) <= 1.6, run);
  // gaps: the junction of a block's four dots is background, not a filled cell (blocks away from the poles)
  let gapOk = 0, gapN = 0; const gap = [];
  for (let i = 0; i < N && gapN < 80; i++) { const lat = D.iy[i]; if (Math.abs(lat) > 40) continue; const p = proj(D.ix[i] + 0.5, lat, Z6); if (p.cosc < 0.5 || p.x < 20 || p.x > 1420 || p.y < 20 || p.y > 880) continue; gapN++;
    const px = await page.evaluate(([x, y]) => { const c = document.getElementById('rgm-globe'), k = c.width / c.getBoundingClientRect().width, d = c.getContext('2d').getImageData(Math.floor(x * k), Math.floor(y * k), 1, 1).data; return [d[0], d[1], d[2]]; }, [p.x, p.y]);
    const dist = (a, b) => Math.hypot(a[0] - b[0], a[1] - b[1], a[2] - b[2]), cc = colours[clsOf(i)], land = [22, 29, 38], ocean = [11, 18, 27]; if (dist(px, cc) > 12 && Math.min(dist(px, land), dist(px, ocean)) < 14) gapOk++; else gap.push([i, px, cc]); }
  check(`dots are separate, with background showing between them (${gapOk}/${gapN} block centres)`, gapN >= 20 && gapOk >= gapN - 2, JSON.stringify(gap.slice(0, 2)));
  await page.screenshot({ path: 'gd_zoom.png' });
  await page.click('#rgm-reset');
  { let last = '', same = 0; for (let t = 0; t < 80 && same < 5; t++) { await page.waitForTimeout(300); const h = await page.evaluate(() => { const c = document.getElementById('rgm-globe'), d = c.getContext('2d').getImageData(0, 0, c.width, c.height).data; let x = 0; for (let i = 0; i < d.length; i += 97) x = (x * 31 + d[i]) | 0; return x; }); same = h === last ? same + 1 : 0; last = h; } }   // wait until the fly-home has really finished

  /* 3. hover: tooltip equals the data for 150 random blocks */
  const visB = []; for (let i = 0; i < N; i++) { const q = proj(D.ix[i] + 0.5, D.iy[i]); if (q.cosc > 0.35 && Math.abs(D.iy[i]) < 60) visB.push(i); }
  const sampleB = Array.from({ length: 150 }, () => visB[Math.floor(rnd() * visB.length)]);
  let okh = 0; const badh = [];
  for (const i of sampleB) { const q = proj(D.ix[i] + 0.5, D.iy[i]); await page.mouse.move(q.x, q.y); await page.waitForTimeout(6);
    const t = (await page.locator('#rgm-tip').isVisible()) ? (await page.locator('#rgm-tip').innerText()).split('\n') : [''];
    const n = D.n[i], want1 = `${D.countries[D.ctry[i]]} · ${n ? fmtD(n / D.area[i] * 1000) + ' per 1,000 km²' : 'no gauge'}`, wantN = n ? `from a 1° cell with ${n.toLocaleString('en-US')} ${n === 1 ? 'gauge' : 'gauges'}` : 'from a 1° cell with no gauge';
    if (t[0] === want1 && (t[1] || '').endsWith(wantN)) okh++; else badh.push([t.join(' | ').slice(0, 90), want1]); }
  check(`hover tooltip matches the data (${okh}/150)`, okh === 150, JSON.stringify(badh.slice(0, 2)));
  await page.mouse.move(10, 880); await page.waitForTimeout(50); check('tooltip hidden over empty space', !(await page.locator('#rgm-tip').isVisible()), '');

  /* 4. zoomed in: each of a block's four dots reports its own lattice-aligned 0.5° bounds */
  for (let k = 0; k < 6; k++) await page.click('#rgm-zin'); await page.waitForTimeout(150);
  const Z = Math.pow(1.4, 6);
  let best = -1, bd = 1e9; for (let i = 0; i < N; i++) { const d = Math.hypot(D.ix[i] + 0.5 - 15, D.iy[i] - 22); if (d < bd) { bd = d; best = i; } }
  const ix = D.ix[best], iy = D.iy[best];
  const rng = (a, b, pos, neg) => a >= 0 && b >= 0 ? `${a.toFixed(1)}–${b.toFixed(1)}°${pos}` : a <= 0 && b <= 0 ? `${(-b).toFixed(1)}–${(-a).toFixed(1)}°${neg}` : `${(-a).toFixed(1)}°${neg}–${b.toFixed(1)}°${pos}`;
  const quarters = [['SW', 0, 0], ['SE', 0.5, 0], ['NW', 0, 0.5], ['NE', 0.5, 0.5]]; let okq = 0; const badq = [];
  for (const [nm, dx, dy] of quarters) { const q = proj(ix + dx + 0.25, iy - 0.5 + dy + 0.25, Z); await page.mouse.move(q.x, q.y); await page.waitForTimeout(40);
    const t = (await page.locator('#rgm-tip').isVisible()) ? (await page.locator('#rgm-tip').innerText()).split('\n')[1] || '' : '';
    const want = `0.5° cell ${rng(ix + dx, ix + dx + 0.5, 'E', 'W')} · ${rng(iy - 0.5 + dy, iy + dy, 'N', 'S')}`; if (t.startsWith(want)) okq++; else badq.push([nm, t.slice(0, 60), want]); }
  check(`all four 0.5° quarters of block (${ix}, ${iy}) report their own bounds`, okq === 4, JSON.stringify(badq));
  check('all quarter bounds sit on the 0.5° lattice', [ix, ix + .5, iy - .5, iy].every(v => Math.abs(v * 2 - Math.round(v * 2)) < 1e-9), '');

  /* 5. interaction */
  const hash = pg => pg.evaluate(() => { const c = document.getElementById('rgm-globe'), d = c.getContext('2d').getImageData(0, 0, c.width, c.height).data; let x = 0; for (let i = 0; i < d.length; i += 101) x = (x * 31 + d[i]) | 0; return x; });
  { const f = await open(1440, 900); const h0 = await hash(f); await f.mouse.move(GCX, 450); await f.mouse.down(); await f.mouse.move(GCX - 80, 470, { steps: 8 }); await f.mouse.up(); await f.waitForTimeout(150);
    check('drag turns the globe', (await hash(f)) !== h0, ''); check('a drag shows no tooltip', !(await f.locator('#rgm-tip').isVisible()), ''); await f.close(); }
  { const f = await open(1440, 900); const h1 = await hash(f); await f.mouse.move(GCX, 450);
    const y0 = await f.evaluate(() => scrollY), scrollable = await f.evaluate(() => document.documentElement.scrollHeight > innerHeight + 5);
    await f.mouse.wheel(0, 300); await f.waitForTimeout(300); const y1 = await f.evaluate(() => scrollY);
    check('a plain wheel does not zoom the globe (and scrolls the page when the page can scroll)', (await hash(f)) === h1 && (!scrollable || y1 > y0), JSON.stringify({ y0, y1, scrollable }));
    await f.mouse.move(GCX, 450); await f.keyboard.down('Control'); await f.mouse.wheel(0, -300); await f.keyboard.up('Control'); await f.waitForTimeout(250); check('Ctrl + wheel zooms', (await hash(f)) !== h1, ''); await f.close(); }
  const globals = await page.evaluate(() => { const f = document.createElement('iframe'); document.body.appendChild(f); const base = new Set(Object.getOwnPropertyNames(f.contentWindow)); f.remove(); return Object.getOwnPropertyNames(window).filter(k => !base.has(k)); });
  if (!process.env.RG_EMBEDDED) check('only one global added (d3)', globals.length === 1 && globals[0] === 'd3', JSON.stringify(globals));
  await page.close();

  /* 6. other sizes and touch */
  for (const [w, h] of [[1280, 720], [1920, 1080]]) { const p = await open(w, h); const m = await p.evaluate(() => ({ h: document.getElementById('rgm-scene').offsetHeight, over: document.documentElement.scrollWidth > innerWidth })); check(`${w}x${h}: fits, no sideways scroll`, Math.abs(m.h - h) <= 2 && !m.over, JSON.stringify(m)); await p.close(); }
  const ph = await open(390, 844, true);
  const pm = await ph.evaluate(() => { const g = document.getElementById('rgm-globewrap'), r = g.getBoundingClientRect(); return { pos: getComputedStyle(g).position, over: document.documentElement.scrollWidth > innerWidth, w: Math.round(r.width), h: Math.round(r.height), act: document.querySelector('.rgm-act').textContent }; });
  check('phone: stacked, square-ish earth, no sideways scroll', pm.pos === 'relative' && !pm.over && pm.h <= pm.w + 2, JSON.stringify(pm));
  const box = await ph.evaluate(() => { const r = document.getElementById('rgm-globe').getBoundingClientRect(); return { x: r.left, y: r.top, w: r.width, h: r.height }; });
  await ph.touchscreen.tap(box.x + box.w * 0.5, box.y + box.h * 0.55); await ph.waitForTimeout(150);
  check('phone: tapping a cell shows its value', await ph.locator('#rgm-tip').isVisible(), '');
  check('no JavaScript errors', errors.length === 0, errors.join(' | '));
  console.log(failed ? `\n${failed} check(s) FAILED` : '\nall checks passed'); await browser.close(); process.exit(failed ? 1 : 0);
})();
