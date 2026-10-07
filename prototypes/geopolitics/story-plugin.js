/* ======== STORY PLUGIN: slide 23's two maps, on the final page's shared globe ========
   Only in the final page (scripts/build_all.py), where the story defines window.WMSTORY. Data: geopolitics-data.json
   (build_geopolitics.py). Labels are set like the Idai maps' (the design system's .wm-place / .wm-water).

   Layers (the slide's two views switch them on; the story fades them):
     geo_indus   the six rivers of the Indus Waters Treaty, UNOSAT's satellite-detected flood water over Pakistan
                 (26 Aug to 7 Sep 2025, the same blue as Idai's flood), and the labels: India, Pakistan, the rivers
     geo_arctic  the seven Arctic Council states other than Russia, tinted; the Arctic Circle, dashed; the labels:
                 those states, Russia and Ukraine
   No borders between India and Pakistan or Russia and Ukraine (Kashmir and Crimea are disputed): labels only. */
(() => {
  'use strict';
  const H = window.WMSTORY; if (!H) return;
  const DATA = JSON.parse(document.getElementById('geo-DATA').textContent);
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const LOOK = WM.LOOK, FLOOD = WM.COLOR.flood, RIVER = 'rgba(236,234,229,.8)';   // rivers light grey, so the flood is the only blue

  // ---------- data, decoded once ----------
  const flood = DATA.flood.map(r => { const o = []; for (let i = 0; i < r.length; i += 2) o.push([r[i] / 1000, r[i + 1] / 1000]); return o; });
  const rivers = Object.entries(DATA.rivers).map(([name, lines]) => ({ name,
    geo: { type: 'MultiLineString', coordinates: lines.map(l => { const o = []; for (let i = 0; i < l.length; i += 2) o.push([l[i], l[i + 1]]); return o; }) } }));
  const arctic = { type: 'FeatureCollection', features: Object.values(DATA.arctic).map(polys => {
    const coords = polys.map(p => p.map(r => r.map(([x, y]) => [x / 100, y / 100])));
    coords.forEach(p => { if (d3.geoArea({ type: 'Polygon', coordinates: [p[0]] }) > 2 * Math.PI) p.forEach(r => r.reverse()); });
    return { type: 'Feature', geometry: { type: 'MultiPolygon', coordinates: coords } }; }) };
  const circle = { type: 'LineString', coordinates: d3.range(-180, 181, 2).map(x => [x, 66.56]) };

  let API = null, arrived = 0, wasMoving = true;
  function track() { const m = API ? API.moving() : false; if (wasMoving && !m) arrived = performance.now(); wasMoving = m; }
  const fadeIn = ms => { const f = reduce ? 1 : Math.min(1, (performance.now() - arrived) / ms); if (f < 1 && API) API.animate(60); return WM.ease(f); };
  // a label only where it faces us (the Arctic view sees round the pole)
  function label(ctx, proj, text, ll, kind, opt = {}) {
    const r = proj.rotate(); if (d3.geoDistance(ll, [-r[0], -r[1]]) > 1.45) return;
    const q = proj(ll); if (!q) return;
    const F = { place: ['500 12px "IBM Plex Sans", sans-serif', '#8C96A3', '.32em'], big: ['500 15px "IBM Plex Sans", sans-serif', LOOK.text2, '.38em'],
                river: ['italic 14px Georgia, serif', RIVER, '0'], line: ['italic 12.5px Georgia, serif', LOOK.muted, '0'] }[kind];
    ctx.save(); ctx.font = F[0]; ctx.fillStyle = F[1]; if ('letterSpacing' in ctx) ctx.letterSpacing = F[2] === '0' ? '0px' : F[2];
    ctx.textAlign = opt.align || 'center'; ctx.textBaseline = 'middle'; ctx.shadowColor = 'rgba(5,8,14,.95)'; ctx.shadowBlur = 6;
    ctx.fillText(text, q[0] + (opt.dx || 0), q[1] + (opt.dy || 0)); ctx.restore();
  }
  // the flood (thousands of rings) is drawn once per view into an offscreen canvas, once the camera has arrived
  const cache = { cv: document.createElement('canvas'), k: '' };
  function floodLayer(ctx, proj, alpha) {
    if (API && API.moving()) return;
    const cv = ctx.canvas, k = [proj.scale(), ...proj.translate(), ...proj.rotate(), cv.width, cv.height].map(v => v.toFixed(3)).join();
    if (cache.k !== k) {
      cache.cv.width = cv.width; cache.cv.height = cv.height; const g = cache.cv.getContext('2d');
      const dpr = cv.width / (cv.clientWidth || cv.width); g.setTransform(dpr, 0, 0, dpr, 0, 0);
      g.beginPath(); for (const r of flood) { r.forEach((p, i) => { const v = proj(p); if (v) i ? g.lineTo(v[0], v[1]) : g.moveTo(v[0], v[1]); }); g.closePath(); }
      g.fillStyle = FLOOD; g.fill('nonzero');
      g.strokeStyle = FLOOD; g.lineWidth = .6; g.lineJoin = 'round'; g.stroke();   // a hairline edge so the small patches read (VIIRS, 375 m)
      cache.k = k;
    }
    ctx.save(); ctx.setTransform(1, 0, 0, 1, 0, 0); ctx.globalAlpha = alpha * 0.9 * fadeIn(900); ctx.drawImage(cache.cv, 0, 0); ctx.restore();
  }

  // label positions: placed by hand, beside each river where it runs alone (approximate, read off the river lines)
  const RIVER_LABELS = [['Indus', [69.6, 27.6], { align: 'right', dx: -10 }], ['Jhelum', [72.9, 33.1], { align: 'right', dx: -10 }],
    ['Chenab', [73.3, 31.6], { align: 'right', dx: -8 }], ['Ravi', [73.9, 31.0], { align: 'left', dx: 8 }],
    ['Beas', [75.5, 31.7], { align: 'left', dx: 10 }], ['Sutlej', [73.7, 29.9], { align: 'left', dx: 10 }]];

  H.register('geopolitics', {
    attach(api) { API = api; },
    layers: {
      geo_indus(ctx, proj, a) {
        track();
        floodLayer(ctx, proj, a);
        const P = d3.geoPath(proj, ctx);
        ctx.save(); ctx.globalAlpha = a; ctx.strokeStyle = RIVER; ctx.lineWidth = 1.1; ctx.lineJoin = 'round'; ctx.lineCap = 'round';
        for (const r of rivers) { ctx.beginPath(); P(r.geo); ctx.stroke(); }
        ctx.restore();
        if (API && API.moving()) return;
        ctx.save(); ctx.globalAlpha = a * fadeIn(500);
        label(ctx, proj, 'INDIA', [76.6, 27.2], 'big'); label(ctx, proj, 'PAKISTAN', [66.6, 29.6], 'big');
        RIVER_LABELS.forEach(([t, ll, o]) => label(ctx, proj, t, ll, 'river', o));
        ctx.restore();
      },
      geo_arctic(ctx, proj, a) {
        track();
        const P = d3.geoPath(proj, ctx);
        ctx.save(); ctx.globalAlpha = a;
        ctx.beginPath(); P(arctic); ctx.fillStyle = 'rgba(236,234,229,.13)'; ctx.fill(); ctx.strokeStyle = 'rgba(236,234,229,.45)'; ctx.lineWidth = .7; ctx.stroke();
        ctx.beginPath(); P(circle); ctx.setLineDash([4, 4]); ctx.strokeStyle = 'rgba(236,234,229,.55)'; ctx.lineWidth = 1; ctx.stroke(); ctx.setLineDash([]);
        ctx.restore();
        if (API && API.moving()) return;
        ctx.save(); ctx.globalAlpha = a * fadeIn(500);
        label(ctx, proj, 'RUSSIA', [98, 62], 'big'); label(ctx, proj, 'UKRAINE', [31.5, 49], 'place');
        [['UNITED STATES', [-152, 64.5]], ['CANADA', [-105, 62]], ['GREENLAND (DENMARK)', [-41, 73]], ['ICELAND', [-18.7, 64.9]],
         ].forEach(([t, ll]) => label(ctx, proj, t, ll, 'place'));
        // the Nordic states are close together at this scale: Norway to the west of its coast, Finland to the east
        label(ctx, proj, 'NORWAY', [6.5, 61.8], 'place', { align: 'right' }); label(ctx, proj, 'SWEDEN', [15.5, 62.6], 'place', { dy: 6 });
        label(ctx, proj, 'FINLAND', [29.5, 64.2], 'place', { align: 'left' });
        label(ctx, proj, 'Arctic Circle', [130, 66.56], 'line', { dy: -9 });
        ctx.restore();
      }
    }
  });
})();
