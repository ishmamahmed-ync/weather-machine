/* ======== STORY PLUGIN: "Since you were born", on the final page's shared globe ========
   Only in the final page (scripts/build_all.py), where the story defines window.WMSTORY. Narrative slide 17.
   The reader picks their country, year of birth and a country to compare with. The slide's narration then
   becomes the finding ("Since 2005, the year you were born, floods have killed ..."); under it, four bars
   (deaths, affected, at risk, displacements) on one scale, your country in colour, the comparison in white;
   the globe turns to the country and outlines it. (The rain-gauge half was dropped by the author, 5 Oct.)

   Data: profile-data.json (build_globe.py): EM-DAT and IDMC yearly series, Rentschler et al. (2022) people at
   risk, Natural Earth outlines.
   Layer (the slide's view switches it on; the story fades it):
     cp_outline   the chosen country's outline, white */
(() => {
  'use strict';
  const H = window.WMSTORY; if (!H) return;
  const DATA = JSON.parse(document.getElementById('cp-DATA').textContent);
  const M = DATA.meta, by = {};
  DATA.countries.forEach(c => by[c.iso] = c);
  const thisYear = new Date().getFullYear(), DEFAULT_REF = 'USA';
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;

  const css = n => getComputedStyle(document.documentElement).getPropertyValue(n).trim();
  // ---------- outlines ----------
  const shapeOf = {};
  function shape(iso) {
    if (shapeOf[iso] !== undefined) return shapeOf[iso];
    const polys = DATA.shapes[iso]; if (!polys) return (shapeOf[iso] = null);
    const coords = polys.map(p => p.map(r => r.map(([x, y]) => [x / 100, y / 100])));
    coords.forEach(p => { if (d3.geoArea({ type: 'Polygon', coordinates: [p[0]] }) > 2 * Math.PI) p.forEach(r => r.reverse()); });
    return (shapeOf[iso] = { type: 'Feature', geometry: { type: 'MultiPolygon', coordinates: coords } });
  }
  // where to look: the largest part of the country (so France is framed on France, not French Guiana)
  function home(iso) {
    const f = shape(iso); if (!f) return null;
    const parts = f.geometry.coordinates.map(p => ({ type: 'Polygon', coordinates: p }));
    const big = parts.reduce((a, b) => d3.geoArea(b) > d3.geoArea(a) ? b : a);
    const c = d3.geoCentroid(big);
    const r = Math.max(0.004, ...big.coordinates[0].map(v => d3.geoDistance(c, v)));
    const z = Math.max(1, Math.min(24, 0.62 / Math.sin(Math.min(1.3, r))));
    return { lon: c[0], lat: c[1], z: Math.max(1, z * 0.45) };   // the country in its region
  }

  // ---------- state (kept in this browser only, so a return visit shows the same country) ----------
  const state = { iso: null, ref: null, born: null, mode: 'flood' };
  try { Object.assign(state, JSON.parse(localStorage.getItem('wm-born') || '{}')); } catch (e) {}
  if (!by[state.iso]) state.iso = null;
  if (!by[state.ref]) state.ref = null;
  const refIso = () => state.ref || DEFAULT_REF;
  const save = () => { try { localStorage.setItem('wm-born', JSON.stringify(state)); } catch (e) {} };

  // ---------- the panel under the slide's words ----------
  const panel = document.createElement('div'); panel.className = 'cp-panel';
  const opts = DATA.countries.map(c => '<option value="' + c.iso + '">' + c.name + '</option>').join('');
  panel.innerHTML =
    '<div class="cp-fields">' +
      '<select class="wm-field" id="cp-country" required aria-label="Your country"><option value="" disabled hidden>Your country</option>' + opts + '</select>' +
      '<input class="wm-field" id="cp-born" type="text" inputmode="numeric" maxlength="4" placeholder="Year of birth" aria-label="Year of birth" autocomplete="off">' +
      '<select class="wm-field" id="cp-ref" required aria-label="Country to compare with"><option value="" disabled hidden>Compare with</option>' + opts + '</select>' +
    '</div>' +
    '<div class="cp-head"><div class="wm-legend cp-key"></div>' +
      '<div class="wm-seg" role="group" aria-label="Disasters counted"><button class="wm-btn is-on" type="button" data-mode="flood">Flood</button><button class="wm-btn" type="button" data-mode="all">Others</button></div></div>' +
    '<div class="wm-bars cp-bars"></div>' +
    '<p class="wm-note cp-scale"></p>';
  const $ = s => panel.querySelector(s);
  const selC = $('#cp-country'), selR = $('#cp-ref'), yob = $('#cp-born');
  selC.value = state.iso || ''; selR.value = state.ref || ''; if (state.born) yob.value = state.born;

  yob.addEventListener('focus', () => yob.placeholder = 'YYYY');
  yob.addEventListener('blur', () => yob.placeholder = 'Year of birth');
  yob.addEventListener('input', () => {                    // four digits, 1920 to this year; a plain text field
    const d = yob.value.replace(/\D/g, '').slice(0, 4);
    yob.value = d; yob.classList.remove('is-bad');
    if (d.length < 4) return;
    if (+d < 1920 || +d > thisYear) { yob.classList.add('is-bad'); return; }
    state.born = +d; update(false);
  });
  selC.addEventListener('change', () => { state.iso = selC.value; update(true); });
  selR.addEventListener('change', () => { state.ref = selR.value; update(false); });
  panel.querySelectorAll('.wm-seg .wm-btn').forEach(b => b.addEventListener('click', () => { state.mode = b.dataset.mode; update(false); }));

  // ---------- numbers ----------
  const fmt = n => Math.round(n).toLocaleString('en-US');
  const compact = n => n >= 1e9 ? (n / 1e9).toFixed(n >= 1e10 ? 0 : 1) + ' billion'
                    : n >= 1e6 ? (n / 1e6).toFixed(n >= 1e7 ? 0 : 1) + ' million' : fmt(n);
  const big = n => compact(n).replace(/ (million|billion)$/, '<small>$1</small>');
  const esc = s => String(s).replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
  const sum = (s, y0, from) => { if (!s) return 0; let t = 0; for (let i = Math.max(0, from - y0); i < s.length; i++) t += s[i]; return t; };
  // totals from the birth year (or the first year of records), by whole calendar years
  function stats(c, born) {
    const fe = Math.max(born, M.em[0]), fd = Math.max(born, M.disp[0]), em = c.em, dp = c.disp, fl = state.mode === 'flood';
    return {
      deaths: sum(em && em[fl ? 2 : 0], M.em[0], fe), affected: sum(em && em[fl ? 3 : 1], M.em[0], fe),
      disp: sum(dp && dp[fl ? 1 : 0], M.disp[0], fd), risk: c.risk || 0,
      fDeaths: sum(em && em[2], M.em[0], fe), fAffected: sum(em && em[3], M.em[0], fe), fDisp: sum(dp && dp[1], M.disp[0], fd)
    };
  }
  const MEASURES = [['deaths', 'Deaths', '--wm-deaths'], ['affected', 'Affected', '--wm-affected'],
                    ['risk', 'At risk of a 1-in-100-year flood', '--wm-flood'], ['disp', 'Displacements', '--wm-displaced']];
  const w = (v, m) => v > 0 ? 'width:max(2px, ' + (v / m * 100).toFixed(3) + '%)' : 'width:0; min-width:0';   // above zero stays visible

  // four bars on ONE scale: the largest of the eight values (four measures, two countries) fills the track
  function bars(s, t, all, cName, rName) {
    const m = Math.max(1, ...MEASURES.flatMap(([k]) => [s[k], t[k]]));
    $('.cp-bars').innerHTML = MEASURES.map(([k, title, tok]) => {
      const v = s[k], f = all && k !== 'risk' ? s['f' + k[0].toUpperCase() + k.slice(1)] : null;
      const share = f != null && v > 0 ? ' · ' + Math.round(f / v * 100) + '% floods' : '';   // in the name, so the number line stays one line
      const fill = f != null
        ? '<span class="fill" style="' + w(v, m) + '; background:color-mix(in srgb, var(--c) 40%, transparent)"><span class="part" style="width:' + (v > 0 ? (f / v * 100).toFixed(2) : 0) + '%"></span></span>'
        : '<span class="fill" style="' + w(v, m) + '"></span>';
      return '<div class="wm-bar" style="--c:var(' + tok + ')"><span class="k">' + title + share + '</span>' +
        '<span class="v" style="color:var(--c)">' + big(v) + '<span class="ref">vs ' + compact(t[k]) + '<span class="in"> in ' + esc(rName) + '</span></span></span>' +
        '<div class="track is-pair">' + fill + '<span class="fill is-ref" style="' + w(t[k], m) + '"></span></div></div>';
    }).join('');
    return 'One scale for all four bars: the longest fills the width.';
  }

  // the slide's narration: the author's words until a country and year are chosen, then the finding
  let leadEl = null, leadOrig = '';
  function narration(html) {
    const p = panel.closest('.wm-slide') && panel.closest('.wm-slide').querySelector('.text .wm-lead');
    if (!p) return;
    if (p !== leadEl) { leadEl = p; leadOrig = p.innerHTML; }   // the story rebuilds the words each time the slide arrives
    p.innerHTML = html || leadOrig; p.classList.toggle('cp-finding', !!html);
  }
  function empty() {
    narration(null);
    $('.cp-bars').innerHTML = MEASURES.map(([k, title, tok]) =>
      '<div class="wm-bar" style="--c:var(' + tok + ')"><span class="k">' + title + '</span><span class="v">–</span><div class="track is-pair"></div></div>').join('');
    $('.cp-scale').textContent = '';
  }

  function update(move) {
    panel.querySelectorAll('.wm-seg .wm-btn').forEach(x => x.classList.toggle('is-on', x.dataset.mode === state.mode));
    save();
    const c = by[state.iso], r = by[refIso()];
    if (move && c && API && on) { const h = home(state.iso); if (h) API.flyTo(h.lon, h.lat, h.z); }
    if (API) API.redraw();
    $('.cp-key').innerHTML = c ? '<span><i class="wm-swatch cp-me"></i>' + esc(c.name) + '</span>' +
      '<span><i class="wm-swatch cp-ref-sw"></i>' + esc(r.name) + '</span>' : '';
    if (!c || !state.born) return empty();
    const born = state.born, all = state.mode === 'all';
    const s = stats(c, born), t = stats(r, born);
    const kind = all ? 'weather and climate disasters' : 'floods';
    // the records start in 2000: for anyone born earlier the sentence says so rather than claim their whole life
    const lead = born < M.em[0] ? 'Since ' + M.em[0] + ', when the records begin (you were born in ' + born + '),'
                                : 'Since ' + born + ', the year you were born,';
    narration(lead + ' ' + kind + ' have killed <b>' + compact(s.deaths) + '</b> people in ' + esc(c.name) +
      ', affected <b>' + compact(s.affected) + '</b>, and forced people from their homes <b>' + compact(s.disp) + '</b> times.');
    const scale = bars(s, t, all, c.name, r.name);

    $('.cp-scale').textContent = scale + ' Displacements are movements, not people' +
      (born < M.disp[0] ? ' (records from ' + M.disp[0] + ')' : '') + '. Records to ' + M.em[1] + '.';
  }

  // ---------- the globe ----------
  let API = null, on = false;
  H.register('country-profile', {
    attach(api) { API = api; },
    mount(el) { el.appendChild(panel); update(false); },
    step() { on = true; const h = state.iso && home(state.iso); if (h && API) API.flyTo(h.lon, h.lat, h.z); },
    stop() { on = false; },
    layers: {
      cp_outline(ctx, proj, a) {
        const f = state.iso && shape(state.iso); if (!f) return;
        ctx.save(); ctx.globalAlpha = a; ctx.beginPath(); d3.geoPath(proj, ctx)(f);
        ctx.strokeStyle = css('--wm-text'); ctx.lineWidth = 1.2; ctx.stroke(); ctx.restore();
      }
    }
  });
})();
