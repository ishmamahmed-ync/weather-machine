/* ==========================================================================
   Weather Machine design system: wm.js
   The same tokens as wm.css, for canvas and WebGL drawing, plus the globe's
   rendering rules. Inlined into each page by design-system/inline.py; defines
   one global, WM. No dependencies; the globe helpers expect d3-geo.
   ========================================================================== */
const WM = (function(){

  // Surfaces and lines (match wm.css)
  const LOOK = {
    bg:'#05080E', ocean:'#0B121B', land:'#161D26', coast:'#242E3A',
    reliefLo:'#14171B', reliefHi:'#40454B', reliefEdge:0.55,
    text:'#ECEAE5', text2:'#D9D6CF', muted:'#8B95A1', faint:'#5C6773',
    line:'#222C38', rim:'rgba(236,234,229,.6)', grat:'rgba(236,234,229,.15)'
  };

  // One hue per meaning. Keys match DATA layer names on the main site where they exist.
  const COLOR = {
    // instruments: who is watching
    stations:'#FFB547', years:'#FFD08A', gauges:'#3FD98A', gaugesLow:'#2A6B49', gaugesNone:'#76818D', gaugesWMO:'#58C48A', argo:'#45B0CE', seals:'#6FD8B4',
    sharks:'#F07A55', telemetry:'#B98CE0', turtles:'#C6E377', sats:'#CBD6E2', coldspots:'#E4EEFF',
    // impacts: what happens to people
    deaths:'#E8433F', affected:'#F2C744', damage:'#5BC8A8', flood:'#7DB4D1',
    settlements:'#E05CC8', settlementsLost:'#FF3D6E', mhews2022:'#F5D04A', mhews2025:'#F08A3E',
    // status, interface only
    alert:'#E8433F', ok:'#3FB6A8'
  };

  // Rain-gauge density, gauges per 1,000 km2: index with WM.gaugeClass(d). Upper bounds inclusive.
  const GAUGE = ['#2E3745','#1E4D36','#266B48','#2F8C5C','#3DB074','#5FD394','#A2EBC2','#E3FFF0'];
  const GAUGE_EDGES = [0.1, 0.5, 1, 2, 5, 10];
  const gaugeClass = (n, d) => { if(!n) return 0; for(let k = 0; k < 6; k++) if(d <= GAUGE_EDGES[k]) return k + 1; return 7; };

  // Saffir-Simpson: tropical storm, categories 1 to 5. Index with WM.storm(category).
  const STORM = ['#F5E06A','#F6C243','#F09A3E','#E8703E','#DC4340','#B81D2C'];
  const storm = cat => STORM[Math.max(0, Math.min(5, cat | 0))];

  // Photo placeholders until images are cleared: muted, darker than any data colour
  const PLACEHOLDER = ['#2E4A5C','#3B4A2E','#4A3B2E','#2E3F4A','#2E4A44','#4A2E3B','#3F3A4A','#4A452E'];

  // ---- globe rules ----
  const GLOBE = {
    radius:0.42,        // globe radius as a share of the shorter window side
    centreX:0.70,       // desktop: centre of the right-hand part of the page
    gratStep:10,        // degrees
    gratWidth:0.5, rimWidth:1,
    backCull:1.5533,    // radians: skip points this far from the centre (just under 90°)
    // The globe is on every screen. While a big image is shown it minimises to the top-right
    // corner as a round lens CENTRED ON the image's top-right corner (drawn on top), and its white lines
    // (lat/lon grid, circular edge) stay visible.
    mini:{ rMin:80, rMax:125, rShare:0.087, top:0.04, topMin:54, right:0.03,
           grat:'rgba(236,234,229,.3)', gratWidth:0.5, rim:'rgba(236,234,229,.75)', rimWidth:1, fly:0.9 }
  };
  // Where the corner globe sits for a W x H window: centre and radius in CSS pixels
  function miniView(W, H){
    const m = GLOBE.mini, r = Math.max(m.rMin, Math.min(m.rMax, W * m.rShare));
    return { cx: W - W * m.right - r, cy: Math.max(H * m.top, m.topMin) + r, r };
  }

  // Density grid (stations, Argo, seals ...): additive squares, density as brightness.
  // The 0.85 power, 0.13 floor and gain 7 are the main site's defaults.
  const GRID = { power:0.85, floor:0.13, gain:7 };
  const gridSize = scale => Math.max(0.3, scale / 210);
  const gridAlpha = (n, max, g = GRID) =>
    g.floor + (1 - g.floor) * Math.min(1, Math.pow(n, g.power) / Math.pow(max, g.power) * g.gain);

  // Dot layers grow with the fourth root of zoom; linear growth turned close-ups to mush.
  const dotRadius = (scale, dot = 1.3) => Math.max(0.5, dot * Math.min(2.6, Math.max(0.6, Math.pow(scale / 520, 0.25))));

  // Clickable markers (stories, places): ring, then hover, then selected with a halo
  const MARKER = { r:5.5, stroke:1.2, fill:'rgba(236,234,229,.16)', hover:'rgba(236,234,229,.5)',
                   active:'#ECEAE5', halo:6, haloStroke:'rgba(236,234,229,.45)', hit:14 };
  function drawMarker(ctx, x, y, state, k = 1){
    const r = MARKER.r * Math.pow(k, 0.25);
    if(state === 'active'){ ctx.beginPath(); ctx.arc(x, y, r + MARKER.halo, 0, 6.2832);
      ctx.strokeStyle = MARKER.haloStroke; ctx.lineWidth = 1; ctx.stroke(); }
    ctx.beginPath(); ctx.arc(x, y, r, 0, 6.2832);
    ctx.fillStyle = state === 'active' ? MARKER.active : state === 'hover' ? MARKER.hover : MARKER.fill; ctx.fill();
    ctx.strokeStyle = LOOK.text; ctx.lineWidth = MARKER.stroke; ctx.stroke();
  }

  // Easing for globe moves: ease in and out (cubic)
  const ease = t => t < .5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2;

  // Rotation: store real [lon, lat]; d3's rotate() takes the negation. Do it here, once.
  const rotateFor = ([lon, lat]) => [-lon, -lat];

  // "#RRGGBB" -> "r,g,b" for building rgba() strings in loops
  const rgb = h => [1, 3, 5].map(i => parseInt(h.slice(i, i + 2), 16)).join(',');

  return { LOOK, COLOR, GAUGE, GAUGE_EDGES, gaugeClass, STORM, storm, PLACEHOLDER, GLOBE, miniView, GRID, gridSize, gridAlpha,
           dotRadius, MARKER, drawMarker, ease, rotateFor, rgb };
})();
