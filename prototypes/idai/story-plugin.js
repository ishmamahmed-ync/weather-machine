/* ======== STORY PLUGIN: Idai, on the final page's shared globe ========
   Only in the final page (scripts/build_all.py), where the story defines window.WMSTORY. Draws this
   prototype's data (idai-data.json, from build_idai.py) on the story's one globe; the photos and the MODIS
   pair it registers are shown by the story (corner lens and side photo, and the before/after wipe).
   Maps are kept simple (the author, 5 Oct): one map per slide, only the labels the story needs.

   Layers (a slide's views switch them on; the story fades them):
     idai_base    flat land at map scale (the design system: the Idai story uses flat land), Mozambique a
                  shade lighter, coastlines, and a lat/lon grid that tightens with zoom, white like the globe's
     idai_tracks  the three IBTrACS tracks in calendar order, coloured by Saffir-Simpson category as recorded;
                  on the season slide they draw one after another, timed with the day counts in the words; on the
                  case-study slide (mode 'track') Idai alone draws itself in, a spinning mark at its head
     idai_flood   UNOSAT flood extent, 13 to 20 March 2019 (Sentinel-1 radar), drawn once the camera arrives
     idai_damage  a zoom callout: a small white rectangle over central Beira on the regional map, joined by two
                  lines to a big rectangle showing it magnified: Copernicus EMS EMSR348 building grades, with
                  Copernicus's water and coastline (Beira Center area only)
     idai_labels  the few labels each map needs, and on the flood map a schematic arrow (rain over Zimbabwe's
                  highlands, carried back by the rivers): labelled schematic, it is not a river line */
(() => {
  'use strict';
  const H = window.WMSTORY; if (!H) return;
  const DATA = JSON.parse(document.getElementById('idai-DATA').textContent);
  H.photos = Object.assign(H.photos || {}, JSON.parse(document.getElementById('idai-PHOTOS').textContent));
  const RAD = Math.PI / 180, reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;

  // ---------- data, decoded once ----------
  const dec = (a, sc) => { const out = []; let x = 0, y = 0; for (let i = 0; i < a.length; i += 2) { x += a[i]; y += a[i + 1]; out.push([x / sc, y / sc]); } return out; };
  const feat = polys => {
    const coords = polys.map(p => p.map(r => r.map(([x, y]) => [x / 100, y / 100])));
    coords.forEach(p => { if (d3.geoArea({ type: 'Polygon', coordinates: [p[0]] }) > 2 * Math.PI) p.forEach(r => r.reverse()); });
    return { type: 'Feature', geometry: { type: 'MultiPolygon', coordinates: coords } };
  };
  const region = Object.entries(DATA.region).map(([iso, p]) => Object.assign(feat(p), { id: iso }));
  const mozFine = region.find(f => f.id === 'MOZ');
  const flood = DATA.flood.map(r => dec(r, 1e4));
  const water = DATA.water.map(r => dec(r, 1e5)), coast = DATA.coast.map(r => dec(r, 1e5));
  const C = DATA.center, dmg = [];
  for (let i = 0; i < C.dmg.length; i += 3) dmg.push([C.dmg[i] / 1e5, C.dmg[i + 1] / 1e5, C.dmg[i + 2]]);

  // the storm ramp (design system --wm-ts .. --wm-c5) and the damage grades (--wm-dmg-*)
  const RAMP = WM.STORM, catIdx = c => c === 'ts' ? 0 : c && c.startsWith('cat') ? +c.slice(3) : -1;   // -1: depression
  const css = n => getComputedStyle(document.documentElement).getPropertyValue(n).trim();
  const GRADE = { 1: css('--wm-dmg-1'), 2: css('--wm-dmg-2'), 3: css('--wm-dmg-3') };
  const LOOK = WM.LOOK;

  let API = null, mode = null, t0 = 0, arrived = 0, wasMoving = true;
  const SEASON = [['desmond', 1000, 3000], ['idai', 3000, 5000], ['kenneth', 5000, 7000]];   // ms after the slide arrives; matches the beats in the words
  const TRACK = [1100, 5200];      // the case-study slide: Idai draws itself in, starting once the camera has arrived, over 5.2 s

  // the storm's head while its track draws in: a dot in the category's colour and two spinning arms (a cyclone
  // turns clockwise in the southern hemisphere)
  function cycloneMark(ctx, proj, f, ms) {
    const tr = DATA.tracks.idai, segs = tr.length - 1, u = f * segs, i = Math.min(segs - 1, Math.floor(u)), k = u - i;
    const a = tr[i], b = tr[i + 1], q = proj([a[0] + (b[0] - a[0]) * k, a[1] + (b[1] - a[1]) * k]); if (!q) return;
    const c = Math.max(catIdx(a[3]), catIdx(b[3])), col = c < 0 ? LOOK.muted : RAMP[c], r = 7 + Math.max(0, c) * 1.4, spin = ms / 1000 * 2.4;
    ctx.save(); ctx.translate(q[0], q[1]);
    ctx.beginPath(); ctx.arc(0, 0, 3.2, 0, 6.2832); ctx.fillStyle = col; ctx.fill();
    ctx.rotate(spin); ctx.strokeStyle = col; ctx.lineWidth = 1.6; ctx.lineCap = 'round';
    for (const s of [0, Math.PI]) { ctx.beginPath(); ctx.arc(0, 0, r, s, s + 1.9); ctx.stroke(); }
    ctx.restore();
  }

  // ---------- drawing helpers ----------
  const path = (ctx, proj) => d3.geoPath(proj, ctx);
  function catTrack(ctx, proj, n, frac, w) {
    const t = DATA.tracks[n], segs = t.length - 1, upto = frac * segs, P = path(ctx, proj);
    ctx.lineCap = 'round';
    for (let i = 0; i < segs && i < upto; i++) {
      const a = t[i], b = t[i + 1], f = Math.min(1, upto - i);
      const end = [a[0] + (b[0] - a[0]) * f, a[1] + (b[1] - a[1]) * f], k = Math.max(catIdx(a[3]), catIdx(b[3]));
      ctx.beginPath(); P({ type: 'LineString', coordinates: [[a[0], a[1]], end] });
      ctx.strokeStyle = k < 0 ? LOOK.muted : RAMP[k]; ctx.lineWidth = k < 0 ? w * .6 : w; ctx.setLineDash(k < 0 ? [3, 3] : []); ctx.stroke();
    }
    ctx.setLineDash([]);
  }
  const ring = (ctx, proj, pts) => { pts.forEach((q, i) => { const v = proj(q); if (v) i ? ctx.lineTo(v[0], v[1]) : ctx.moveTo(v[0], v[1]); }); };
  function grid(ctx, proj) {                                  // a lat/lon grid that tightens with zoom
    const s = proj.scale(), step = s < 900 ? 10 : s < 6000 ? 2 : s < 60000 ? 0.5 : s < 600000 ? 0.05 : 0.01;
    if (step === 10) return;                                  // the story already draws the 10° grid
    const r = proj.rotate(), c = [-r[0], -r[1]], half = Math.min(80, Math.hypot(innerWidth, innerHeight) / s / RAD);
    ctx.beginPath(); path(ctx, proj)(d3.geoGraticule().extent([[c[0] - half, Math.max(-89, c[1] - half)], [c[0] + half, Math.min(89, c[1] + half)]]).step([step, step]).precision(step / 2)());
    ctx.strokeStyle = WM.LOOK.grat; ctx.lineWidth = .5; ctx.stroke();
  }
  // map labels, set like the design system's .wm-place / .wm-water / .wm-town
  function label(ctx, proj, text, ll, kind, opt = {}) {
    const q = proj(ll); if (!q) return;
    const F = { place: ['500 12px "IBM Plex Sans", sans-serif', '#6F7884', '.32em'], big: ['500 15px "IBM Plex Sans", sans-serif', LOOK.muted, '.38em'],
                water: ['italic 14px Georgia, serif', '#5F8FA8', '0'], river: ['italic 15px Georgia, serif', LOOK.text, '0'], town: ['500 13px "IBM Plex Sans", sans-serif', LOOK.text2, '0'],
                note: ['500 11.5px "IBM Plex Sans", sans-serif', LOOK.muted, '0'], name: ['600 12px "IBM Plex Sans", sans-serif', LOOK.text, '0'] }[kind];
    ctx.save(); ctx.font = F[0]; ctx.fillStyle = F[1]; if ('letterSpacing' in ctx) ctx.letterSpacing = F[2] === '0' ? '0px' : F[2];
    ctx.textAlign = opt.align || 'center'; ctx.textBaseline = 'middle'; ctx.shadowColor = 'rgba(5,8,14,.95)'; ctx.shadowBlur = 6;
    const dx = opt.dx || 0, dy = opt.dy || 0;
    if (kind === 'town' && !opt.nodot) { ctx.beginPath(); ctx.arc(q[0], q[1], 2.6, 0, 6.2832); ctx.fillStyle = LOOK.text; ctx.fill(); ctx.fillStyle = F[1]; }
    String(text).split('\n').forEach((line, i) => ctx.fillText(line, q[0] + dx, q[1] + dy + i * 15));
    ctx.restore();
  }
  // a heavy layer (thousands of shapes) is drawn once into an offscreen canvas for the current view, and only
  // once the camera has arrived; then it fades in over 0.4 s
  const caches = {};
  function cached(key, ctx, proj, alpha, paint, fade = { from: 0, to: 1, ms: 400 }) {
    if (API && API.moving()) return;
    const cv = ctx.canvas, k = [proj.scale(), ...proj.translate(), ...proj.rotate(), cv.width, cv.height].map(v => v.toFixed(3)).join();
    let c = caches[key];
    if (!c || c.k !== k) {
      c = caches[key] = c || { cv: document.createElement('canvas') };
      c.cv.width = cv.width; c.cv.height = cv.height; const g = c.cv.getContext('2d');
      const dpr = cv.width / (cv.clientWidth || cv.width); g.setTransform(dpr, 0, 0, dpr, 0, 0); g.clearRect(0, 0, cv.width, cv.height);
      paint(g); c.k = k;
    }
    const f = reduce ? 1 : Math.min(1, (performance.now() - arrived) / fade.ms); if (f < 1 && API) API.animate(60);
    const o = fade.from + (fade.to - fade.from) * (reduce ? 1 : WM.ease(f));
    ctx.save(); ctx.setTransform(1, 0, 0, 1, 0, 0); ctx.globalAlpha = alpha * o; ctx.drawImage(c.cv, 0, 0); ctx.restore();
  }
  function track(ctx, proj) {                                   // note when the camera has just arrived
    const m = API ? API.moving() : false;
    if (wasMoving && !m) arrived = performance.now();
    wasMoving = m;
  }

  H.register('idai', {
    attach(api) { API = api; },
    step(view) {
      mode = view.idai || null; t0 = performance.now();
      if (mode === 'season' && API) API.animate(reduce ? 50 : 8500);
      if (mode === 'track' && API) API.animate(reduce ? 50 : TRACK[0] + TRACK[1] + 900);
    },
    stop() { mode = null; },
    layers: {
      idai_base(ctx, proj, a) {
        track(ctx, proj);
        const P = path(ctx, proj);
        ctx.save(); ctx.globalAlpha = a;
        if (proj.scale() > 300000) {                          // city scale: plain land; Copernicus's own water and coastline go on top
          ctx.beginPath(); P({ type: 'Sphere' }); ctx.fillStyle = LOOK.land; ctx.fill(); grid(ctx, proj); ctx.restore(); return;
        }
        ctx.beginPath(); P({ type: 'Sphere' }); ctx.fillStyle = LOOK.ocean; ctx.fill();
        ctx.fillStyle = LOOK.land; for (const f of region) { ctx.beginPath(); P(f); ctx.fill(); }
        ctx.beginPath(); P(mozFine); ctx.fillStyle = 'rgba(236,234,229,.06)'; ctx.fill();
        grid(ctx, proj);
        ctx.strokeStyle = LOOK.coast; ctx.lineWidth = .7; for (const f of region) { ctx.beginPath(); P(f); ctx.stroke(); }
        ctx.beginPath(); P(mozFine); ctx.strokeStyle = LOOK.muted; ctx.lineWidth = .9; ctx.stroke();
        ctx.restore();
      },
      idai_tracks(ctx, proj, a) {
        ctx.save(); ctx.globalAlpha = a;
        if (mode === 'season') {
          const ms = reduce ? 1e9 : performance.now() - t0;
          SEASON.forEach(([n, from, to]) => { const f = Math.max(0, Math.min(1, (ms - from) / (to - from))); if (f > 0) catTrack(ctx, proj, n, f, 2.6); });
        } else if (mode === 'track') {
          const ms = reduce ? 1e9 : performance.now() - t0, f = Math.max(0, Math.min(1, (ms - TRACK[0]) / TRACK[1]));
          if (f > 0) catTrack(ctx, proj, 'idai', f, 2.6);
          if (!reduce && f > 0 && f < 1) cycloneMark(ctx, proj, f, ms);
        } else catTrack(ctx, proj, 'idai', 1, 2.2);
        ctx.restore();
      },
      idai_flood(ctx, proj, a) {
        track(ctx, proj);
        cached('flood', ctx, proj, a, g => {
          g.beginPath(); for (const r of flood) { ring(g, proj, r); g.closePath(); }
          g.fillStyle = WM.COLOR.flood; g.fill('nonzero');   // passes overlap; nonzero keeps their union
        }, { from: 0.08, to: 0.9, ms: 3000 });   // the water rises: from very faint to 90% over 3 s once the camera arrives (the author, 5 Oct)
      },
      idai_damage(ctx, proj, a) {
        track(ctx, proj);
        cached('damage', ctx, proj, a, g => {
          const [w, s, e, n] = C.box, nw = proj([w, n]), se = proj([e, s]); if (!nw || !se) return;
          const small = [nw[0], nw[1], se[0], se[1]];                         // x0, y0, x1, y1 on screen
          // the big rectangle: same shape as the small one, 60% of the screen's height, beside it to the right
          const vw = g.canvas.clientWidth || innerWidth, vh = g.canvas.clientHeight || innerHeight;
          const bh = Math.min(vh * .6, 560), bw = bh * (small[2] - small[0]) / (small[3] - small[1]);
          const bx = Math.min(vw - Math.max(48, vw * .04) - bw, small[2] + Math.max(90, vw * .07)), by = (vh - bh) / 2;
          const big = [bx, by, bx + bw, by + bh];
          const corners = r => [[r[0], r[1]], [r[2], r[1]], [r[2], r[3]], [r[0], r[3]]];
          const cs = corners(small), cb = corners(big), all = cs.concat(cb);
          g.save(); g.strokeStyle = LOOK.text; g.lineCap = 'butt';
          // the two joining lines: corner to matching corner, keeping only the outer two (every corner on one side)
          g.globalAlpha = .55; g.lineWidth = 1;
          for (let i = 0; i < 4; i++) {
            const [p, q] = [cs[i], cb[i]], side = v => (q[0] - p[0]) * (v[1] - p[1]) - (q[1] - p[1]) * (v[0] - p[0]);
            const sd = all.map(side).filter(v => Math.abs(v) > 1e-6);
            if (sd.every(v => v > 0) || sd.every(v => v < 0)) { g.beginPath(); g.moveTo(p[0], p[1]); g.lineTo(q[0], q[1]); g.stroke(); }
          }
          g.globalAlpha = 1;
          // the magnified map, drawn with its own projection fitted to the big rectangle
          const P2 = d3.geoOrthographic().rotate([-(w + e) / 2, -(s + n) / 2]).clipAngle(90)
            .fitExtent([[big[0], big[1]], [big[2], big[3]]], { type: 'Polygon', coordinates: [[[w, s], [w, n], [e, n], [e, s], [w, s]]] });
          g.save(); g.beginPath(); g.rect(bx, by, bw, bh); g.clip();
          g.fillStyle = LOOK.land; g.fillRect(bx, by, bw, bh);
          for (const r of water) { g.beginPath(); ring(g, P2, r); g.closePath(); g.fillStyle = LOOK.ocean; g.fill(); }
          for (const r of coast) { g.beginPath(); ring(g, P2, r); g.strokeStyle = css('--wm-coast-2'); g.lineWidth = 1; g.stroke(); }
          const sz = { 1: 2.4, 2: 3, 3: 4 };
          for (const gr of [1, 2, 3]) { g.fillStyle = GRADE[gr]; for (const d of dmg) { if (d[2] !== gr) continue; const v = P2(d); if (v) g.fillRect(v[0] - sz[gr] / 2, v[1] - sz[gr] / 2, sz[gr], sz[gr]); } }
          g.restore();
          // the two frames, white like the design system's image frame
          g.strokeStyle = css('--wm-frame'); g.lineWidth = 1;
          g.strokeRect(small[0] + .5, small[1] + .5, small[2] - small[0], small[3] - small[1]);
          g.strokeRect(bx + .5, by + .5, bw - 1, bh - 1);
          g.restore();
          label(g, P2, 'Central Beira, 26 March 2019', [w, n], 'note', { align: 'left', dy: -14 });
        });
      },
      idai_labels(ctx, proj, a) {
        if (API && API.moving()) return;
        ctx.save(); ctx.globalAlpha = a * (reduce ? 1 : Math.min(1, (performance.now() - arrived) / 400));
        if (mode === 'season') {
          [['MOZAMBIQUE', [37.6, -15.9], 'big'], ['MALAWI', [34.0, -12.6], 'place'], ['ZIMBABWE', [30.0, -18.6], 'place'], ['MADAGASCAR', [46.0, -19.6], 'place'], ['SOUTH AFRICA', [30.0, -25.2], 'place']]
            .forEach(([t, ll, k]) => label(ctx, proj, t, ll, k));
          label(ctx, proj, 'Mozambique Channel', [41.2, -22.4], 'water');
          label(ctx, proj, 'Beira', DATA.places.Beira, 'town', { align: 'left', dx: 8 });
          const ms = reduce ? 1e9 : performance.now() - t0;
          [['Desmond\nJanuary 2019', 'desmond', 0, [-10, 0], 'right'], ['Idai\nMarch 2019', 'idai', 1, [10, -14], 'left'], ['Kenneth\nApril 2019', 'kenneth', 2, [10, 0], 'left']].forEach(([t, n, i, d, al]) => {
            if (ms < SEASON[i][1]) return;
            label(ctx, proj, t, DATA.tracks[n][0].slice(0, 2), 'name', { align: al, dx: d[0], dy: d[1] });
          });
        }
        if (mode === 'damage') {
          label(ctx, proj, 'Beira', [C.box[0], (C.box[1] + C.box[3]) / 2], 'town', { align: 'right', dx: -10, nodot: true });
          label(ctx, proj, 'MOZAMBIQUE', [34.55, -19.45], 'big');
          label(ctx, proj, 'Mozambique Channel', [34.82, -20.5], 'water');
        }
        if (mode === 'flood') {
          label(ctx, proj, 'MOZAMBIQUE', [34.9, -18.75], 'big'); label(ctx, proj, 'ZIMBABWE', [32.75, -19.15], 'place');
          // river names: placed by towns that stand on each river (Mafambisse on the Pungwe, Buzi on the Buzi);
          // approximate positions, not river geometry (no river data in the page)
          label(ctx, proj, 'Pungwe', [34.45, -19.42], 'river'); label(ctx, proj, 'Buzi', [34.3, -20.02], 'river');   // light, to read over the flood
          label(ctx, proj, 'Beira', DATA.places.Beira, 'town', { align: 'left', dx: 8 });
          label(ctx, proj, 'Mozambique Channel', [35.35, -20.55], 'water');
          // the schematic arrow: from Zimbabwe's eastern highlands, over the plain, to the coast
          const pts = [[32.95, -19.55], [33.5, -19.25], [34.15, -19.45], [34.68, -19.72]].map(q => proj(q)).filter(Boolean);
          if (pts.length === 4) {
            ctx.beginPath(); ctx.moveTo(pts[0][0], pts[0][1]); ctx.bezierCurveTo(pts[1][0], pts[1][1], pts[2][0], pts[2][1], pts[3][0], pts[3][1]);
            ctx.strokeStyle = LOOK.text; ctx.lineWidth = 1.2; ctx.setLineDash([]); ctx.stroke();
            const ang = Math.atan2(pts[3][1] - pts[2][1], pts[3][0] - pts[2][0]), L = 9;
            ctx.beginPath(); ctx.moveTo(pts[3][0], pts[3][1]);
            ctx.lineTo(pts[3][0] - L * Math.cos(ang - .45), pts[3][1] - L * Math.sin(ang - .45)); ctx.moveTo(pts[3][0], pts[3][1]);
            ctx.lineTo(pts[3][0] - L * Math.cos(ang + .45), pts[3][1] - L * Math.sin(ang + .45)); ctx.stroke();
          }
        }
        ctx.restore();
      }
    }
  });
})();
