/* ==========================================================================
   The history layers, drawn year by year. Shared by the standalone page (history.html, through
   build_history.py) and the final page's shared globe (story-plugin.js), so both draw exactly the same.
   Needs d3-geo. DATA is what build_history.py packs (history-data.json).

   stations  0.5° land cells; for each decade, the stations whose record in the global archive overlaps
             it (record spans, not installation dates). Additive squares, density as brightness, the
             main site's 0.85 / 0.13 / 7. Between two decades the counts are blended.
   argo      1° ocean cells, each lit from the year of its first profile to the year of its last.
   sats      every meteorological and Earth-observation satellite in WMO OSCAR/Space, from launch to end
             of life. The number is real; positions are seeded random and drift (illustrative).
   ========================================================================== */
function HistoryLayers(DATA){
  const POWER = 0.85, FLOOR = 0.13, GAIN = 7, RAD = Math.PI / 180;
  const DEC = DATA.decades, ND = DEC.length, Y0 = DEC[0];
  const stXY = Float32Array.from(DATA.st.xy), stN = Int32Array.from(DATA.st.n);
  const arXY = Float32Array.from(DATA.argo.xy), arY = Int16Array.from(DATA.argo.y), arN = Float32Array.from(DATA.argo.n);
  let stMax = 0; for(const v of stN) if(v > stMax) stMax = v;
  let arMax = 0; for(const v of arN) if(v > arMax) arMax = v;
  const stNorm = Math.pow(stMax, POWER), arNorm = Math.pow(arMax, POWER);
  const bright = (n, norm) => FLOOR + (1 - FLOOR) * Math.min(1, Math.pow(n, POWER) / norm * GAIN);

  // satellites: real launch and end-of-life years; seeded random positions, so every load looks the same
  let seed = 7;
  const rnd = () => { seed = (seed + 0x6D2B79F5) | 0; let t = Math.imul(seed ^ seed >>> 15, 1 | seed);
    t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; };
  const SAT = [];
  for(let i = 0; i < DATA.sats.length; i += 2){
    SAT.push({ lon: rnd() * 360 - 180, lat: Math.asin(2 * rnd() - 1) / RAD,
               from: DATA.sats[i], to: DATA.sats[i + 1] + 1,              // in operation through its last year
               speed: (rnd() < .5 ? -1 : 1) * (2 + rnd() * 5),            // degrees of longitude per second
               alt: 1.05 + rnd() * 0.07 });
  }

  // Each cell's position on the sphere, worked out once; per frame only the view changes. The projection is the
  // orthographic maths d3 uses (same positions), done inline because tens of thousands of cells are drawn a frame.
  const trig = xy => { const n = xy.length / 2, o = { sl: new Float32Array(n), cl: new Float32Array(n), sp: new Float32Array(n), cp: new Float32Array(n) };
    for(let i = 0; i < n; i++){ const lo = xy[2 * i] * RAD, la = xy[2 * i + 1] * RAD; o.sl[i] = Math.sin(lo); o.cl[i] = Math.cos(lo); o.sp[i] = Math.sin(la); o.cp[i] = Math.cos(la); }
    return o; };
  const stT = trig(stXY), arT = trig(arXY);
  const arB = Float32Array.from(arN, n => bright(n, arNorm));          // each Argo cell's brightness, worked out once
  function view(proj){
    const s = proj.scale(), t = proj.translate(), r = proj.rotate(), l0 = -r[0] * RAD, p0 = -r[1] * RAD;
    return { s, tx: t[0], ty: t[1], sl0: Math.sin(l0), cl0: Math.cos(l0), sp0: Math.sin(p0), cp0: Math.cos(p0) };
  }
  // screen position of cell i, or false on the far side (beyond about 89 degrees from the centre)
  const at = (V, T, i, out) => {
    const sd = T.sl[i] * V.cl0 - T.cl[i] * V.sl0, cd = T.cl[i] * V.cl0 + T.sl[i] * V.sl0;     // sin and cos of (lon - lon0)
    if(V.sp0 * T.sp[i] + V.cp0 * T.cp[i] * cd < 0.017) return false;
    out[0] = V.tx + V.s * T.cp[i] * sd; out[1] = V.ty - V.s * (V.cp0 * T.sp[i] - V.sp0 * T.cp[i] * cd); return true;
  };
  const Q = [0, 0];

  const decadeAt = year => { const f = (year - Y0) / 10, i = Math.max(0, Math.min(ND - 2, Math.floor(f))); return [i, Math.max(0, Math.min(1, f - i))]; };
  const centre = proj => { const r = proj.rotate(); return [-r[0], -r[1]]; };

  function stations(ctx, proj, year, alpha = 1){
    const [i, t] = decadeAt(year), V = view(proj), sz = Math.max(0.3, V.s / 210), h = sz / 2;
    ctx.globalCompositeOperation = 'lighter'; ctx.fillStyle = 'rgb(255,181,71)';   // one colour; each cell's brightness is its opacity
    for(let c = 0; c < stT.sl.length; c++){
      const n = stN[c * ND + i] * (1 - t) + stN[c * ND + i + 1] * t;
      if(n <= 0.02 || !at(V, stT, c, Q)) continue;
      ctx.globalAlpha = (n >= 1 ? bright(n, stNorm) : bright(1, stNorm) * n) * alpha;   // fade in from nothing
      ctx.fillRect(Q[0] - h, Q[1] - h, sz, sz);
    }
    ctx.globalAlpha = 1; ctx.globalCompositeOperation = 'source-over';
  }
  const litness = (c, year) => Math.min(1, Math.max(0, year - arY[2 * c] + 1)) * Math.min(1, Math.max(0, arY[2 * c + 1] + 1 - year));
  function argo(ctx, proj, year, alpha = 1){
    const V = view(proj), sz = Math.max(0.3, V.s / 210), h = sz / 2;
    ctx.globalCompositeOperation = 'lighter'; ctx.fillStyle = 'rgb(69,176,206)';
    for(let c = 0; c < arN.length; c++){
      const a = litness(c, year); if(a <= 0.01 || !at(V, arT, c, Q)) continue;
      ctx.globalAlpha = arB[c] * a * alpha;
      ctx.fillRect(Q[0] - h, Q[1] - h, sz, sz);
    }
    ctx.globalAlpha = 1; ctx.globalCompositeOperation = 'source-over';
  }
  function sats(ctx, proj, year, clock, alpha = 1){
    const ctr = centre(proj), tr = proj.translate();
    const r = Math.max(0.6, 1.3 * Math.min(2.2, Math.max(0.6, Math.pow(proj.scale() / 520, 0.25))));
    ctx.fillStyle = '#CBD6E2';
    for(const s of SAT){
      const a = Math.min(1, (year - s.from) / 0.4, (s.to - year) / 0.4);      // fade in at launch, out at end of life
      if(a <= 0) continue;
      const lon = ((s.lon + s.speed * clock + 540) % 360) - 180, p = [lon, s.lat];
      if(d3.geoDistance(p, ctr) > 1.5708) continue;                           // hide anything round the back
      const q = proj(p); if(!q) continue;
      ctx.globalAlpha = 0.85 * a * alpha;
      ctx.beginPath(); ctx.arc(tr[0] + (q[0] - tr[0]) * s.alt, tr[1] + (q[1] - tr[1]) * s.alt, r, 0, 6.2832); ctx.fill();
    }
    ctx.globalAlpha = 1;
  }
  // the numbers on screen: stations with data in the decade (blended between decades), satellites in
  // operation that year (the per-year table), 1° ocean cells with an Argo float that year
  let litY = NaN, litN = 0;
  function counts(year){
    const [i, t] = decadeAt(year);
    if(year !== litY){ litY = year; litN = 0; for(let c = 0; c < arN.length; c++) if(litness(c, year) > 0.01) litN++; }   // only when the year moves
    const lit = litN;
    return { stations: DATA.perDecade[i] * (1 - t) + DATA.perDecade[i + 1] * t,
             sats: year >= 1960 ? DATA.satsPerYear[Math.floor(year + 1e-6)] || 0 : 0, argo: lit,
             decade: Math.min(DEC[ND - 1], Math.floor(Math.floor(year + 1e-6) / 10) * 10) };
  }
  return { stations, argo, sats, counts };
}
