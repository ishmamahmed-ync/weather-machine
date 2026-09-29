# CLAUDE.md

Context for Claude Code working on this repository.

---

## What this is

**The Gaps in the Weather Machine** — a data visualisation for a Harvard GSD
Master in Design Engineering studio project. It argues that the planet's
observing apparatus is unevenly distributed, that the gap has consequences
measurable in lives, and that the shortfall is now less about instruments than
about what countries share and what we choose to spend on.

Live at `https://ishmamahmed-ync.github.io/weather-machine/`

The author is new to web development and version control. Explain what a change
does and why, not just that it is done. Prefer small verifiable steps over large
refactors.

---

## Current state

Working and deployed. A single self-contained HTML file, 2.1 MB, no network
dependencies, 29 scenes, two views.

- **Story** — scroll-driven narrative, camera and layers driven by scroll position
- **Explore** — drag to rotate, scroll to zoom, 24 toggleable layers
- Press `D` anywhere for a live styling panel

Rendering is d3-geo orthographic projection onto a 2D canvas. **d3-array and
d3-geo are inlined** in the template, not loaded from a CDN, because the file
must work from `file://`. This was a real bug: the first version fetched d3 from
cdnjs, which works over https and silently fails from a local file, producing a
blank page with no error.

---

## Architecture

```
site-src/template.html        markup, styles, engine, with __DATA__ placeholders
site-src/layers/*.json|.b64   packed layer data and base64 images
scripts/build_site.py         injects the layers into the template
index.html                    the built artefact GitHub Pages serves
```

`index.html` is **generated**. Do not hand-edit it. Edit `site-src/template.html`
and run `python scripts/build_site.py`. The script verifies every placeholder is
filled and that no remote script sneaked in.

### Inside the template

Four blocks, in order:

1. `<script id="IMG">` — base64 image constants
2. `<script id="CONFIG">` — **the only part the author edits.** `LAYERS`,
   `SATELLITES`, `WIPE`, `SCENES`, `LOOK`, `SETTINGS`. Heavily commented.
3. `<script id="D3A">` / `<script id="D3G">` — inlined d3
4. `<script id="ENGINE">` — rendering, scroll observers, explore mode, panels
5. `<script id="DATA">` — `const DATA = __DATA__;`

The engine starts on `DOMContentLoaded` (the data block parses last) and is
wrapped in try/catch that paints the error to the page. A blank screen means the
catch itself failed — check the browser console.

### A scene

```js
{ center:[-98, 39],        // real lon/lat. Engine negates it for d3's rotate().
  zoom:1.8,                // 1 = normal, 52 = the Limpopo close-up
  layers:{ stations:1 },   // name -> opacity 0..1; omitted means off
  sats:0,                  // geostationary footprints
  wipe:'us',               // key into WIPE
  quote:true,              // large bare pull quote, width auto-banded by length
  bare:true,               // no box, normal size, for narration
  photo:{src, tint},       // square duotone image above the card
  legend:false,            // legends are automatic from visible layers
  html:`<p>…</p>` }
```

**Rotation sign is the classic trap.** `d3.geoOrthographic().rotate()` takes the
negated centre. Scenes store a real `[lon, lat]` and the engine negates once.
Every scene was wrong at one point because I stored the negated value directly.

### Layer types

| `DATA[k].type` | shape | renderer |
|---|---|---|
| (packed grid) | delta-encoded cell indices + counts | additive blending, density as brightness |
| `points` | flat `[lon,lat,…]` | fixed-radius circles, one batched path |
| `tracks` | `xy`, `len[]`, `cat[]` | polylines, colour by category, travelling pulse |
| `bubbles` | `xy`, `v[]` | area-proportional circles |
| `shell` | `xy`, `alt` | dots projected above the sphere |
| `timeline` | `xy`, `y[]`, `from`, `to` | stations disappear as a year cursor advances |

Grid layers take `power`, `size`, `floor`, `gain`. Point layers take `dot` and
`alpha`. The `D` panel greys out whichever don't apply.

**Dot radius must not scale linearly with zoom.** It uses a fourth root. Linear
scaling gave 9 px radii at zoom 9.5 and the map turned to mush.

---

## Data pipeline

Raw downloads are not committed (50–330 MB). `docs/SOURCES.md` has every link,
download date, licence and row count. `data/processed/` holds the cleaned
outputs. Scripts in `scripts/` go from one to the other; each prints what it kept
and dropped.

**Gap to close:** there is no script that turns `data/processed/` into
`site-src/layers/globe-data.json`. That packing was done ad hoc. Writing
`scripts/pack_layers.py` — binning, delta-encoding, sampling — is the single
most useful piece of engineering outstanding, because right now adding a dataset
requires reconstructing that work.

---

## Editorial rules

This project is *about* data integrity, so it is held to a higher standard than
usual. `docs/NOTES.md` records every problem found, including three bugs of my
own. Maintain it.

- **Verify before asserting.** This bit me hardest on the data-sharing story: I
  connected WMO's "end of the golden age" policy language to the post-1970
  decline in station counts and wrote "we are not measuring less, we are sharing
  less" into the narrative. Menne et al. (2012) shows the real cause — daily data
  sharing was never obligatory, and most countries contributed their history once.
  The scene was rewritten. A clean story that fits the shape of the data is not
  the same as the explanation.
- Several published figures also turned out wrong: the
  GDIS codebook's 11,801 (should be 11,081), "20% of Mozambique's GDP" (closer
  to 12%, and the sourced framing is growth falling from 7% to 1.5%), and a
  claim that flood damage is evenly distributed (it is more concentrated than
  deaths, Gini 0.870 vs 0.836).
- **Attribute correctly.** The flood-completion model is Wu, Zhang & Stouffs
  (Tsinghua / NUS / Singapore-ETH), *Nature Communications* 17:5983. AlphaGeo
  built a website presenting it. This was misattributed three times.
- **Never fabricate data to illustrate a point.** The US flood dots are sampled
  from a blurred density, not real locations, and that is stated in
  `SOURCES.md`. Any caption using them must say "illustrative".
- **Test before claiming a fix.** Use jsdom to actually execute the page; it
  catches what reading the code does not. jsdom does not resolve CSS variables
  in `getComputedStyle`, so verify those by inspecting rules instead.

---

## Open decisions

**Hover tooltips.** Wanted, not built. Attributes were stripped to keep the file
small. Restoring them costs ~110 KB for storms and ~170 KB for floods, but
~11 MB for all 132,501 stations — so restrict stations to the 991 GSN reference
sites. Hit-testing via `projection.invert()` plus a k-d tree, or a hidden
picking canvas for the track polylines.

**Renderer.** Canvas 2D gives total aesthetic control and is at its ceiling
(~65,000 stroke ops per frame on the storm scene). deck.gl's `GlobeView` would
give picking for free and handle far more data, at the cost of rebuilding the
visual language — additive blending, sub-pixel dots, the travelling pulse — as
custom layers. Decide by target: polished narrative piece, or explorable atlas.

**Splitting data out of the HTML.** Would let the page open instantly and make
layers independently downloadable, at the cost of needing a local server and
losing single-file portability. Keep a single-file export either way.

**The data-sharing argument, as now stated.** Sharing daily climate data was
never required; most countries donated their history once; the archive decays as
those donations age. GBON (2021) is the first actual obligation, and compliance
sits at 9% of required surface stations in LDCs and SIDS. Africa's radiosonde
reports to global models fell ~50% between 2015 and 2020 — that one is a genuine
decline in transmission. Sources: Menne et al. 2012 (JTECH 29:897), Applequist
et al. 2024 (Sci Data 11:633), SOFF GBON Baseline 2023, un-soff.org/operations.

**AMOC as a framing device.** Discussed, not built. The argument: the RAPID
array has measured the Atlantic overturning since 2004, and McCarthy et al.
(*GRL* 2025) find current trends will not reach "unfamiliar" signal-to-noise
until the **2040s** — 21 years of record against a 70-year natural cycle. That
is the project's thesis at planetary scale, and it universalises the ignorance
rather than framing it as poor-country deficit. Use as opening frame and closing
statistic only; it should not become the spine, and claims should stay on
*detection*, not collapse.

---

## Suggested next steps, in order

1. **`/data` page on the site.** `SOURCES.md` rendered as a designed page inside
   the piece. Highest value for the crit — it reads as part of the work rather
   than an appendix.
2. **`scripts/pack_layers.py`.** Closes the reproducibility gap above.
3. **Hover on storms and floods.** The interaction the author misses from CARTO.
4. **`/notes` page.** `NOTES.md` as a page. The audit work is content, and it
   demonstrates judgement.

---

## Workflow

```
# edit site-src/template.html, then
python scripts/build_site.py
open index.html
```

Then commit and push in GitHub Desktop. Commit and push are separate steps —
this has caught the author more than once. GitHub Pages redeploys in 2–3 minutes.

## Housekeeping outstanding

- The repository is **private**; it needs to be public for instructors to
  inspect the data. Settings → General → Danger Zone → Change visibility.
- `README.md` still says `open site/index.html`; the file is now at the root.
- `README.md` still has a placeholder where the live URL should go.
