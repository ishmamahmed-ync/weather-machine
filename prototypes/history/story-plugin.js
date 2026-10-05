/* ======== STORY PLUGIN: a century of watching, on the final page's shared globe ========
   Only in the final page (scripts/build_all.py), where the story defines window.WMSTORY. Draws with
   history-layers.js, exactly as the standalone history.html does. The slide that names this plugin has one
   step per chapter: arriving on a step plays that chapter at 1.5 s per decade, then waits for Space.
   Under the slide's words: the year, the three counts, and the timeline (design system .wm-timeline). */
(() => {
  'use strict';
  const H = window.WMSTORY; if (!H) return;
  const DATA = JSON.parse(document.getElementById('hist-DATA').textContent);
  const LY = HistoryLayers(DATA);
  const CHAPTERS = [
    { title:'Weather stations', from:1900, to:1960 },
    { title:'Satellites',       from:1960, to:1990 },
    { title:'Argo floats',      from:1990, to:2025 }
  ];
  const Y0 = 1900, Y1 = 2025, RATE = 10 / 1.5;                 // 1.5 s per decade
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const fmt = n => Math.round(n).toLocaleString('en-US');
  let API = null, year = Y0, ch = 0, playing = false, on = false, clock = 0, last = 0, raf = 0;

  // ---------- the panel under the slide's words ----------
  const pct = y => ((y - Y0) / (Y1 - Y0) * 100) + '%';
  const panel = document.createElement('div'); panel.className = 'hist-panel';
  panel.innerHTML =
    '<span class="wm-stat hist-year" aria-live="off">1900</span>' +
    '<div class="wm-readout"><i class="wm-swatch" style="background:var(--wm-station)"></i><b class="hist-n" data-k="st">0</b><span class="hist-l" data-k="st"></span></div>' +
    '<div class="wm-readout"><i class="wm-swatch" style="background:var(--wm-sat)"></i><b class="hist-n" data-k="sat">–</b><span>Earth-observing satellites in operation</span></div>' +
    '<div class="wm-readout"><i class="wm-swatch" style="background:var(--wm-argo)"></i><b class="hist-n" data-k="ar">–</b><span class="hist-l" data-k="ar"></span></div>' +
    '<div class="hist-bar"><button class="wm-icon-btn hist-play" type="button" aria-label="Play"></button>' +
      '<div class="wm-timeline"><input class="wm-range hist-range" type="range" min="1900" max="2025" step="0.1" value="1900" aria-label="Year">' +
      '<div class="ticks">' + CHAPTERS.map(c => '<span class="c" style="left:' + pct((c.from + c.to) / 2) + '">' + c.title + '</span>').join('') +
        [...new Set(CHAPTERS.flatMap(c => [c.from, c.to]))].map(y => '<span class="t" style="left:' + pct(y) + '">' + y + '</span>').join('') +
      '</div></div></div>';
  const $ = s => panel.querySelector(s), range = $('.hist-range'), btn = $('.hist-play'), labels = [...panel.querySelectorAll('.c')];
  const ICON = { pause:'<svg viewBox="0 0 12 12" fill="currentColor"><rect x="2" y="1" width="3" height="10"/><rect x="7" y="1" width="3" height="10"/></svg>',
                 play:'<svg viewBox="0 0 12 12" fill="currentColor"><path d="M3 1l8 5-8 5z"/></svg>' };

  function readouts() {
    const n = LY.counts(year);
    $('.hist-year').textContent = Math.floor(year + 1e-6);
    $('.hist-n[data-k="st"]').textContent = fmt(n.stations);
    $('.hist-l[data-k="st"]').textContent = 'weather stations with data in the ' + n.decade + 's';
    $('.hist-n[data-k="sat"]').textContent = n.sats ? fmt(n.sats) : '–';
    $('.hist-n[data-k="ar"]').textContent = n.argo ? fmt(n.argo) : '–';
    $('.hist-l[data-k="ar"]').textContent = n.argo ? 'ocean squares (1°) with an Argo float' : 'Argo floats: none yet';
    range.value = year; range.style.setProperty('--p', pct(year));
    labels.forEach((l, i) => l.classList.toggle('is-on', i === ch));
  }
  function setPlaying(p) { playing = p; btn.innerHTML = ICON[p ? 'pause' : 'play']; btn.setAttribute('aria-label', p ? 'Pause' : 'Play'); }
  function loop(now) {
    raf = 0; if (!on) return;
    const dt = last ? Math.min(0.1, (now - last) / 1000) : 0; last = now; clock += dt;
    if (playing) { year = Math.min(CHAPTERS[ch].to, year + dt * RATE); if (year >= CHAPTERS[ch].to) setPlaying(false); }
    readouts(); if (API) API.redraw();
    raf = requestAnimationFrame(loop);                       // satellites drift while the slide is on screen
  }
  btn.addEventListener('click', () => {
    if (playing) return setPlaying(false);
    if (year >= CHAPTERS[ch].to - 1e-6) year = CHAPTERS[ch].from;   // a finished chapter plays again
    setPlaying(true);
  });
  range.addEventListener('input', () => {
    year = +range.value; ch = Math.max(0, CHAPTERS.findIndex(c => year < c.to)); if (year >= Y1) ch = CHAPTERS.length - 1;
    setPlaying(false); readouts(); if (API) API.redraw();
  });

  // follow mode: the story's era timeline (the weather-machine slides) sets the year; satellites drift while on
  let follow = false, raf2 = 0, last2 = 0;
  function drift(now) {
    raf2 = 0; if (!follow) return;
    const dt = last2 ? Math.min(0.1, (now - last2) / 1000) : 0; last2 = now; if (!reduce) clock += dt;
    if (API) API.redraw(); raf2 = requestAnimationFrame(drift);
  }

  H.register('history', {
    setYear(y) { year = y; if (API) API.redraw(); },
    run(on) { follow = on; if (on && !raf2) { last2 = 0; raf2 = requestAnimationFrame(drift); } },
    layers: {
      hist_stations(ctx, proj, a) { LY.stations(ctx, proj, year, a); },
      hist_argo(ctx, proj, a) { LY.argo(ctx, proj, year, a); },
      hist_sats(ctx, proj, a) { LY.sats(ctx, proj, year, clock, a); }
    },
    attach(api) { API = api; },
    mount(el) { el.appendChild(panel); readouts(); },
    // the story calls this when a step of the slide arrives: play that step's chapter from its start
    step(view) {
      ch = Math.max(0, Math.min(CHAPTERS.length - 1, view.chapter || 0)); year = CHAPTERS[ch].from;
      if (reduce) { year = CHAPTERS[ch].to; setPlaying(false); } else setPlaying(true);
      on = true; last = 0; readouts(); if (!raf) raf = requestAnimationFrame(loop);
    },
    stop() { on = false; setPlaying(false); if (raf) cancelAnimationFrame(raf); raf = 0; }
  });
})();
