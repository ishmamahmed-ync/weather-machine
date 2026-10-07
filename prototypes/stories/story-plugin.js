/* ======== STORY PLUGIN: the frontline stories, on the final page's shared globe ========
   Only in the final page (scripts/build_all.py), where the story defines window.WMSTORY. Since 5 Oct the stories
   are the third step of "We know what works" (a view with stories:true); the slide's other steps show the map.
   One white circle per story on the globe; under the slide's words, a card: a 16:9 photo framed in white
   with a link to the source in its bottom-right corner, then place, title, description and source (the design
   system's story card, .wm-card.is-tight).
   It opens on the first story of stories.json (Malawi's flood detectors). Next, a click on a circle, or
   ← → step through them, the globe turning to each place; Space goes on to the next slide.
   A story can carry layers (seals, sharks, tracked animals, Argo, coldspots): they fade in while it is open.
   Photos: each article's own image where one suits (stories.json photo_url; build_all.py embeds them), in the
   design system's duotone over the story's colour, with its credit; otherwise the colour block. */
(() => {
  'use strict';
  const H = window.WMSTORY; if (!H) return;
  const DATA = JSON.parse(document.getElementById('sto-DATA').textContent);
  const S = DATA.stories, STY = DATA.layerStyles || {};
  const css = n => getComputedStyle(document.documentElement).getPropertyValue(n).trim();
  const esc = s => String(s).replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
  const MONTHS = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'];
  const fmtDate = d => { const [y, m, day] = d.split('-').map(Number); return (day ? day + ' ' : '') + (m ? MONTHS[m - 1] + ' ' : '') + y; };

  let API = null, on = false, active = 0, proj = null, hoverI = -1;
  const ZOOM = 0.8;

  // ---------- the card under the slide's words ----------
  const panel = document.createElement('div'); panel.className = 'sto-panel';
  // the design system's story card (.wm-card.is-tight, as in the specimen): photo, place, title, description,
  // the story's layer key, then the source and Next
  panel.innerHTML =
    '<article class="wm-card is-tight sto-card">' +
      '<div class="wm-photo is-duotone sto-photo"><a class="wm-icon-btn sto-more" target="_blank" rel="noopener" aria-label="Read the full story">' +
        '<svg viewBox="0 0 13 13" fill="none" stroke="currentColor" stroke-width="1.4"><path d="M3 10L10 3M4.5 3H10v5.5"/></svg></a>' +
        '<span class="wm-credit sto-credit"></span></div>' +
      '<div class="sto-meta"><span class="wm-label sto-place"></span><span class="wm-note sto-count" aria-live="off"></span></div>' +
      '<h3 class="wm-title sto-title"></h3>' +
      '<p class="wm-body sto-desc"></p>' +
      '<div class="wm-legend is-stacked sto-key"></div>' +
      '<div class="sto-foot"><span class="wm-source sto-src"></span>' +
        '<button class="wm-btn sto-next" type="button" aria-label="Next story">Next ' +
          '<svg viewBox="0 0 12 12" fill="none" stroke="currentColor" stroke-width="1.4" width="11" height="11"><path d="M1.5 6h9M7 2.5L10.5 6 7 9.5"/></svg></button></div>' +
    '</article>';
  const $ = s => panel.querySelector(s);
  $('.sto-next').addEventListener('click', () => show((active + 1) % S.length));
  // Space on the Next button belongs to the page (the next slide), not to the button
  $('.sto-next').addEventListener('keydown', e => {
    if (e.key !== ' ') return;
    e.preventDefault(); e.stopPropagation(); e.currentTarget.blur();
    document.body.dispatchEvent(new KeyboardEvent('keydown', { key: ' ', shiftKey: e.shiftKey, bubbles: true }));
  });

  function card(i) {
    const s = S[i];
    // the photo in the design system's duotone, over the story's colour; without one, the colour alone
    const ph = $('.sto-photo'); ph.style.setProperty('--tint', s.color || '#2E3A4A');
    let img = ph.querySelector('img');
    if (s.photo) { if (!img) { img = document.createElement('img'); img.alt = ''; ph.prepend(img); } img.src = s.photo; }
    else if (img) img.remove();
    $('.sto-credit').textContent = s.photo ? 'Photo: ' + (s.photo_credit || s.source) : '';
    $('.sto-more').href = s.url;
    $('.sto-place').textContent = s.place;
    $('.sto-title').textContent = s.title;
    // the description, with one optional inline link (e.g. "elephant seals" -> the seal data)
    const L = s.link, at = L ? s.description.indexOf(L.text) : -1;
    $('.sto-desc').innerHTML = at < 0 ? esc(s.description)
      : esc(s.description.slice(0, at)) + '<a class="wm-link" href="' + esc(L.url) + '" target="_blank" rel="noopener"' + (L.note ? ' title="' + esc(L.note) + '"' : '') + '>' +
        esc(L.text) + '</a>' + esc(s.description.slice(at + L.text.length));
    $('.sto-key').innerHTML = (s.layers || []).filter(l => STY[l.key]).map(l =>
      '<span><i class="wm-swatch" style="background:' + STY[l.key].color + '"></i>' + esc(STY[l.key].label) + '</span>').join('');
    $('.sto-src').textContent = s.source + (s.date ? ', ' + fmtDate(s.date) : '');
    $('.sto-src').title = $('.sto-src').textContent;
    $('.sto-count').textContent = (i + 1) + ' of ' + S.length;
  }
  function show(i) {
    active = i; card(i);
    const s = S[i], layers = {};
    (s.layers || []).forEach(l => { layers[l.key] = l.alpha; });
    // the globe at its usual size, as on slides 2 to 4 (zoom 0.8: the author, 5 Oct)
    if (API && on) API.view({ lon: s.lon, lat: s.lat, z: ZOOM * (s.zoom || 1), layers });
    if (API) API.redraw();
  }
  addEventListener('keydown', e => {                       // ← → step through the stories while the slide is on
    if (!on || e.metaKey || e.ctrlKey || e.altKey || /^(input|textarea|select)$/i.test(e.target.tagName || '')) return;
    if (e.key === 'ArrowRight') { e.preventDefault(); show((active + 1) % S.length); }
    if (e.key === 'ArrowLeft') { e.preventDefault(); show((active - 1 + S.length) % S.length); }
  });
  card(0);

  // ---------- the circles ----------
  const visible = (p, s) => { const r = p.rotate(); return d3.geoDistance([-r[0], -r[1]], [s.lon, s.lat]) < Math.PI / 2 - 0.05; };
  function hit(x, y) {
    if (!proj) return -1;
    let best = -1, bd = 14 * 14;                            // a generous target for small circles
    S.forEach((s, i) => { if (!visible(proj, s)) return; const q = proj([s.lon, s.lat]), d = (q[0] - x) ** 2 + (q[1] - y) ** 2; if (d < bd) { bd = d; best = i; } });
    return best;
  }

  H.register('stories', {
    attach(api) { API = api; },
    mount(el) { el.appendChild(panel); },
    // the slide's view says whether the stories are on (stories:true): on "We know what works" they are its third step
    step(view) {
      on = !!(view && view.stories); panel.hidden = !on; document.body.toggleAttribute('data-stories', on);
      if (on) show(active); else { hoverI = -1; if (API) { API.canvas.style.cursor = ''; API.redraw(); } }
    },
    stop() { on = false; panel.hidden = true; document.body.removeAttribute('data-stories'); hoverI = -1; if (API) API.canvas.style.cursor = ''; },
    // drawn on top of the layers while the slide is on (an interactive plugin: drag turns the globe)
    draw(ctx, p) {
      proj = p; if (!on) return; const W = css('--wm-text');
      ctx.save();
      S.forEach((s, i) => {
        if (!visible(p, s)) return;
        const q = p([s.lon, s.lat]), a = i === active, h = i === hoverI;
        ctx.beginPath(); ctx.arc(q[0], q[1], a ? 6.5 : h ? 6 : 5, 0, 6.2832);
        ctx.fillStyle = a ? W : 'rgba(236,234,229,.16)'; ctx.fill();
        ctx.strokeStyle = W; ctx.lineWidth = 1.2; ctx.stroke();
        if (a) { ctx.beginPath(); ctx.arc(q[0], q[1], 11, 0, 6.2832); ctx.globalAlpha = .45; ctx.stroke(); ctx.globalAlpha = 1; }
      });
      ctx.restore();
    },
    click(x, y) { if (!on) return; const i = hit(x, y); if (i >= 0) show(i); },
    hover(e) {
      if (!on) return; const r = API.canvas.getBoundingClientRect(), i = hit(e.clientX - r.left, e.clientY - r.top);
      if (i !== hoverI) { hoverI = i; API.canvas.style.cursor = i >= 0 ? 'pointer' : ''; API.canvas.title = i >= 0 ? S[i].place : ''; API.redraw(); }
    },
    leave() { if (hoverI >= 0) { hoverI = -1; if (API) { API.canvas.style.cursor = ''; API.redraw(); } } }
  });
})();
