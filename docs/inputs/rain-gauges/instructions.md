# Integrating the rain-gauge sections into the main page

> **Audience: Claude Code.** Read this whole file before changing anything. Both sections are already built and have been tested together, on their own and inside a copy of the main page. Your job is to place them in the main page without breaking either one.

| | |
|---|---|
| **File to integrate** | `rain-gauge-sections.html`: two sections in one self-contained file (907 KB), no build step |
| **Main page** | the globe story `globe-editable-18.html` ("The Gaps in the Weather Machine"). Facts about it in this file were checked against that file; if it has changed, re-verify section 3.2 |
| **Network use** | none, apart from an optional Google Fonts `<link>` (IBM Plex Sans, Space Grotesk), the same families the main page already loads |
| **Data** | Su et al., *Nature* 652, 119–125 (2026), Fig. 2c, rebuilt from the authors' published data (attribution in section 11) |

---
## 0. What it is, and the decisions already made

Two full-viewport sections the visitor scrolls through, placed after the story's last step, **in this order**:

1. **The density map** (`#rgm-scene`). The earth and nothing else: one small square dot per 0.5° land cell, drawn the way the story page draws its own density layers, coloured by gauges per 1,000 km² in eight classes. Title top-left, legend bottom-left. This is the overview: where the gauges are.
2. **The explorer** (`#rg-scene`). A bordered chart panel on the left (terrain tabs, one square per 1° cell against the WMO minimum) and an unframed globe on the right, linked both ways. This is the detail: how that measures up, terrain by terrain.

Both show the same dataset, so they share one data block, one land layer and one copy of d3. Together that is **840 KB smaller** than shipping the two as separate files.

> **These are rain gauges (precipitation gauges) from the Su et al. paper. They are not flood or stream gauges. Keep the label "rain gauge" everywhere, and do not rename them "flood gauges".**

Defaults chosen, so you do not need to ask:

| Decision | Choice |
|---|---|
| Placement | One wrapper, `<div class="rg-sections" id="rg-sections">`, placed **after `<main id="story">`** as normal-flow sections. Not inside a story scene: the story pins one fixed canvas and builds its scenes from `SCENES`; these sections need their own canvases and their own scrolling layout |
| Globes | **Each section draws its own canvas** and covers the story's fixed canvas while it is on screen (section 3). Reusing the story's canvas is possible but costly (section 4) |
| Shared | `rg-DATA`, `rg-LAND`, `rg-BORD`, the d3 blocks, and the top-bar clearance variable `--rg-topbar` on the wrapper. Everything else belongs to one section |
| Theme | **Dark only** |
| Names | The map uses the prefix `rgm-` and the explorer uses `rg-` (ids, classes, CSS variables). Every CSS rule is scoped to its section, and neither JS block defines a global. Verified: **0** ids and **0** classes shared with the main page, and no duplicate ids |

**Removed from earlier versions on purpose:** the "highlight a country" feature, the page-level header and intro, the light theme, the bullet-point footnotes about the data, and size-coded chart markers. Do not restore them.

**They can still be split.** Each section is self-contained (its own CSS, markup and JS). If the human wants them apart, copy the shared blocks once, put each section where wanted, and add each to the observer in step 7.

---

## 1. Layout specs (so a resize does not regress)

### 1.1 Section 1: the density map

- `.rgm-scene`: `position:relative; isolation:isolate; z-index:3; min-height:100vh`, opaque `#05080E`.
- The globe is an absolutely positioned wrapper (`inset:0`) with a full-size `<canvas>`, so it fills the section with no frame. Globe centre is the middle of the section; radius is `0.42 * min(width, height)`, the story's own value.
- Bare text over the earth (all `pointer-events:none`, with a dark text-shadow for legibility): title and one sentence top-left (`left:4vw`, `max-width:min(27rem,34vw)`), the legend bottom-left, the hint and the source line bottom-right. The zoom buttons and Reset view sit top-right, below the top-bar clearance.
- **Dots:** one per 0.5° cell. Each is a square of `max(0.3, scale / 210)` px, where `scale` is the globe radius times the zoom. That is the story page's own formula (about 1.8 px at its default view), so dots grow with zoom and are the same size whatever the layer's cell size.
- **Stacked layout (760 px and below):** normal flow: heading, then the earth (`min(100vw, 62vh)` tall, radius `0.46 * min(w, h)`), then the legend as a wrapped row, then the source line.

### 1.2 Section 2: the explorer

**Desktop (viewport wider than 920 px)**
- `.rg-scene`: `min-height:100vh`, flex, vertically centred, `padding: calc(var(--rg-topbar) + 1.2rem) 0 1.2rem`.
- Panel: `margin-left:4vw`, `width:min(40rem, 46vw)`, `z-index:2`.
- Globe: an absolutely positioned wrapper (`inset:0`) with a full-size `<canvas>`; globe centre `x = 0.72 * width`, radius `R = min(0.42 * min(width, height), 0.28 * width - 8)`.
- Overlays on the globe (all bare text, `pointer-events:none` except the buttons): zoom buttons top-right, hint under them, selection caption bottom-right, status key under the caption.
- Chart plot height fills the room that is left: `clamp(240, viewportHeight - panelOverhead - scenePadding - 76, 520)`, where `panelOverhead` is measured as the panel's height minus the chart's. It re-fits on resize.
- **The detail card has a fixed height (140 px; 176 px at 640 px and below), scrolling inside if a note is long.** This is essential: see section 10.

**Stacked (920 px and below)**
- The globe wrapper becomes `position:sticky; top:var(--rg-topbar); height:clamp(210px,40vh,320px)` with an opaque background, so the panel scrolls beneath it. Globe centre is the middle of the wrapper, radius `0.44 * min(w, h)`.
- Panel is full width with 14 px margins; tab strip scrolls sideways; chart plot height is 380 px (320 px when narrower than 520 px).

**Column labels under the chart** switch density by column width: 82 px and up shows "1,086 cells / 561 no gauge"; 66 to 82 px shows "561 none"; below 66 px shows a continent code, a percentage and "none".

---

---
## 2. Anatomy of the built file

Banner comments mark the parts:

| Part | Banner / id | Size | Take it? |
|---|---|---|---|
| Fonts link and `html,body{margin:0;background:#05080E}` | `STANDALONE PREVIEW ONLY` | tiny | **No.** The main page has both |
| Wrapper variable | `<style id="rg-shared-css">`: `.rg-sections{--rg-topbar:0px}` | tiny | Yes |
| Map CSS | `<style id="rgm-css">`, every rule scoped to `.rgm-scene` | 4 KB | Yes |
| Explorer CSS | `<style id="rg-css">`, every rule scoped to `.rg-scene` | 8 KB | Yes |
| Markup | `<div class="rg-sections" id="rg-sections">` holding the two `<section>` elements (`rgm-scene`, then `rg-scene`) | 8 KB | Yes. It runs from that opening tag to its closing `</div>`, the last `</div>` before the data banner |
| Cell data | `<script id="rg-DATA" type="application/json">`, **shared** | 274 KB | Yes (schema in section 7) |
| Land | `<script id="rg-LAND" type="application/json">`, **shared** | 310 KB | Yes. GeoJSON MultiPolygon, 1,328 polygons, Natural Earth 50m simplified, plus the main page's own Antarctica outline, wound for d3 |
| Borders | `<script id="rg-BORD" type="application/json">`, **shared** | 210 KB | Yes. MultiLineString, drawn only when zoomed in |
| d3 | `<script id="rg-D3A">`, `<script id="rg-D3G">` | 52 KB | **No.** d3-array 3.2.4 and d3-geo 3.1.1, byte-identical to the main page's copies. Both sections need only `d3.geoOrthographic`, `d3.geoPath`, `d3.geoGraticule10` |
| Map code | `<script id="rgm-JS">`, one IIFE | 12 KB | Yes |
| Explorer code | `<script id="rg-JS">`, one IIFE | 31 KB | Yes. Both code blocks need `d3` and the three data blocks to exist when they run |

Everything is readable, not minified. The map reads `rg-DATA`, `rg-LAND` and `rg-BORD` directly by id, so those ids must not change.

---

## 3. Integration recipe (default: drop-in sections, each with its own canvas)

### 3.1 Steps

1. **CSS.** Append the contents of the three style blocks (`rg-shared-css`, `rgm-css`, `rg-css`) to the main page's `<style>`.
2. **Markup.** Paste `<div class="rg-sections" id="rg-sections">...</div>` directly **after `<main id="story"></main>`** (before `#hintbar`).
3. **Data.** Paste the three `type="application/json"` scripts (`rg-DATA`, `rg-LAND`, `rg-BORD`) into the body. They are inert.
4. **JS.** Paste `<script id="rgm-JS">` and then `<script id="rg-JS">` at the **end of the body**, after the main page's d3 blocks and after the markup and data above, so that `d3` and the elements exist when they run.
5. **Top-bar clearance (one place for both sections).** The story's fixed `#topbar` is about 2.7 rem tall. Add to the main CSS:

   ```css
   .rg-sections { --rg-topbar: 2.8rem; }
   ```

   It pushes the map's title and controls and the explorer's panel clear of the bar, and sets where the explorer's globe pins on phones. It defaults to 0 for the standalone preview.
6. **Hide it in Explore mode (required).** The main page's Explore mode hides `#story` but not its siblings, so without this the sections would sit over the Explore view. One rule covers both sections:

   ```css
   body[data-mode="explore"] #rg-sections { display: none !important; }
   ```

7. **Hide the chrome that would sit over the sections.** `#hintbar` ("press D for controls") is fixed at `z-index:9`, bottom-left. The fixed story card `#cardhost` (`z-index:2`) is already covered by the sections (`z-index:3`) but is worth hiding too. Mirror the existing explore-mode pattern with a flag set while either section is on screen:

   ```css
   body[data-gauges] #hintbar, body[data-gauges] #cardhost { display: none !important; }
   ```

   ```js
   (() => { const on = new Set(), io = new IntersectionObserver(es => {
       es.forEach(e => e.isIntersecting && e.intersectionRatio > 0.5 ? on.add(e.target) : on.delete(e.target));
       document.body.toggleAttribute('data-gauges', on.size > 0); }, { threshold: [0, 0.5, 1] });
     ['rgm-scene', 'rg-scene'].forEach(id => io.observe(document.getElementById(id))); })();
   ```

8. Run both smoke tests (section 9).

### 3.2 What the main page does that matters here (verified)

| Item | Fact |
|---|---|
| Story canvas | `#stage{position:fixed; inset:0; z-index:0}` containing `#globe` |
| Story | `<main id="story">` is empty in the markup and filled by JS; `main{position:relative; z-index:1}`; each `.step` is `100vh` |
| Story card | `#cardhost{position:fixed; z-index:2; left:4vw; width:min(52ch,42vw)}` |
| Top bar | `#topbar` fixed, `z-index:6`, padding `.85rem 4vw`, gradient fading to transparent |
| Progress bar | `#progress` fixed, 1 px, `z-index:7`, width = `scrollY / (scrollHeight - innerHeight)`. Adding the two sections makes the page longer, so the bar now reaches 100% at the end of the explorer. That is acceptable; decide whether it should |
| Scene detection | An `IntersectionObserver` on `.step` elements only (`rootMargin -42% 0px -42% 0px`). The new sections are not `.step`s, so they are never treated as story scenes |
| Rendering | The main engine's `tick` runs every frame but renders only when `dirty` is set, so there is no continuous cost to pause while the scene is on screen |
| Keyboard | One `window` `keydown` listener toggles the control panel on `D`/`d` (it does not filter form controls). Neither section has a text input or a `<select>`, so nothing in them types letters. The explorer's Escape handler is on `document` and acts only while the explorer is on screen; the map's only keyboard handling is arrow keys and +/- on its focused canvas |
| Globals | `LAYERS`, `SATELLITES`, `WIPE`, `SCENES`, `LOOK`, `SETTINGS`, `START`, `DATA`, `PHOTO`, `IMG`. Neither section defines any; the only global they use is `d3` |
### 3.3 Why the sections cover the story's globe instead of reusing it

Each section is `position:relative; z-index:3` with an opaque `#05080E` background, so it simply covers the fixed story canvas and card as it scrolls in. Visually that is the same as a globe with no frame, because each section's own canvas is styled and positioned like the story's. What you lose is a continuous camera fly from the last story view into the map (it arrives as a section, not as a camera move). If that matters, see section 4.

---

## 4. Advanced and optional: reuse the story's globe instead of a second canvas per section

Only do this if the human asks for a seamless transition. It is a real port, not a drop-in.

**What to port** (explorer: all in `rg-JS`, section "GLOBE"; the map's drawing is simpler, `drawDots` plus `pick` in `rgm-JS`): `quad`, `visible`, `fillSet`, `drawCells`, `drawOverlay` (the selection ring, pulse and label), `pickCell` (inverse projection to a cell), `fit`, `cellZoom`. They depend on a projection `proj`, the view (`rot`, `z`), the canvas size and radius, and the theme colours. The story engine has its own `proj`, `cur`/`tgt` view with easing, and a `render()` that draws `LAYERS`, so the cell layer would be a new layer drawn with the story's `proj`.

**What would have to change in the main page:** pointer events on the story canvas (today only enabled in Explore mode) for drag, hover and double-click; a way for the scene to set the story camera (`tgt`) from chart clicks; hiding the layers that do not belong; and the story's `100vh` pinned structure. The chart panel then becomes a story card (`.card` styling) rather than a section.

**Do not attempt this unless asked.** The default in section 3 delivers the requested layout with far less risk.

---

---

## 5. Behaviour contract (must still work after integration)

### 5.1 Section 1: the map

- **Hover** (mouse) or **tap** (touch) a dot: a tooltip names the country and the value ("Germany · 11.4 per 1,000 km²" or "… · no gauge"), with a second line giving the 0.5° cell's lattice-aligned bounds and the 1° cell it came from ("0.5° cell 14.5–15.0°E · 22.0–22.5°N · from a 1° cell with 3 gauges"). Each of a block's four quarters reports its own bounds.
- **Drag turns the globe** (movement above 5 px). On touch a tap shows the tooltip and stays until the next tap or drag. There is no selection state.
- A **plain mouse wheel must still scroll the page**; zoom is Ctrl/Cmd + wheel, the + / - buttons, or +/- keys on the focused canvas. Arrow keys on the focused canvas turn it. Reset view flies home (lon 15, lat 22, zoom 1).
- Zoom is 0.8× to 30×. Borders and a stronger coastline fade in from zoom 1.2 to 3.
- Touch devices get "Tap" instead of "Hover" in the hint. Reduced motion removes the fly-home easing.

### 5.2 Section 2: the explorer

**Chart**
- Click a square: selects that cell (card, ring on the chart, the globe flies to it at about 18 px per cell, with a ring, pulse and label on the globe).
- Click a diamond **or** a continent name under a column: selects the continent (globe fits it, outline tinted pale blue, this terrain's cells shown in status colours, empty cells grey, column band highlighted).
- Hover a square or diamond: tooltip. Cells with no gauge are not squares; they are counted in the diamonds and in the "no gauge" line under each column.

**Globe**
- **Drag turns the globe** (movement above 5 px). A **single click does nothing**. **Double-click** (mouse) or **double-tap** (touch: two taps within 450 ms and 26 px) **selects the cell**, and the view does not move.
- Hover shows a tooltip with a "Double-click to select" hint. A **plain mouse wheel must still scroll the page**; zoom is Ctrl/Cmd + wheel, the + / - buttons, or +/- keys on the focused canvas. Arrow keys on the focused canvas turn it. Reset view returns to lon 15, lat 22, zoom 1.
- Selecting a grey cell (no gauge): the card says "No gauge in this cell" and estimates how many gauges it would need; the chart rings that continent's "no gauge" label and lights its column.
- Cells of other terrains are not drawn, so they cannot be selected.

**Tabs**: `role="tablist"` / `role="tab"`, arrow keys and Home/End. Switching clears the selection. **Esc** clears the selection while the scene is on screen.

**Touch devices** get "double-tap" wording (`matchMedia('(pointer: coarse)')`). Reduced motion removes the fly-to easing and the pulse.

---

## 6. Colours and theme

### 6.1 The map

The eight density classes, **in gauges per 1,000 km²** (they are the legend, and the dots use exactly these colours):

| Class | Range | Colour |
|---|---|---|
| 0 | no gauge | `--c0` |
| 1 | under 0.1 | `--c1` |
| 2 | 0.1 to 0.5 | `--c2` |
| 3 | 0.5 to 1 | `--c3` |
| 4 | 1 to 2 | `--c4` |
| 5 | 2 to 5 | `--c5` |
| 6 | 5 to 10 | `--c6` |
| 7 | 10 or more | `--c7` |

Upper bounds are inclusive (a cell at exactly 0.5 is class 2). Tokens on `.rgm-scene`:

```css
.rgm-scene {
  --bg:#05080E; --ocean:#0B121B; --land:#161D26; --coast:#242E3A; --coast2:#4A5B6E; --grat:#161F2A; --ink:#ECEAE5; --muted:#8F9AA6; --line:#25303D; --card:#0A1018;
  /* density classes, gauges per 1,000 km²: none, then six green steps and one for the densest */
  --c0:#2E3745; --c1:#1E4D36; --c2:#266B48; --c3:#2F8C5C; --c4:#3DB074; --c5:#5FD394; --c6:#A2EBC2; --c7:#E3FFF0;
}
```

### 6.2 The explorer

Everything is a CSS variable on the section's own element, read at draw time (the explorer's `readTheme()` and the map's equivalent read the section element, not `:root`). The first six values below match the main page's `LOOK`:

```css
.rg-scene {
  /* palette (dark only) */
  --bg:#05080E; --ocean:#0B121B; --land:#161D26; --coast:#242E3A; --grat:#161F2A; --ink:#ECEAE5;
  --muted:#8F9AA6; --line:#222C38; --panel:rgba(5,8,14,.84); --grid:#17202B; --card:#0A1018; --card-line:#25303D; --chip:#121B26;
  --coast2:#4A5B6E; --zone:rgba(79,190,130,.11); --wmo:#58C48A; --dia-out:#F2F5F7; --dia-in:#05080E; --sel:#ECEAE5;
  /* status colours: meets the WMO minimum / below it / no gauge */
  --g-hi:#3FD98A; --g-lo:#2A6B49; --g-no:#76818D; --lo-rim:rgba(63,217,138,.45); --tint:#6C8FE8;
}
```

Colour means **status**: green (`--g-hi`) meets the WMO minimum, faint green (`--g-lo`, with `--lo-rim` as its outline) falls short, grey (`--g-no`) has no gauge; `--tint` outlines a selected continent on the globe. To retheme, change these variables only.

---

---

## 7. Data

### 7.1 The `rg-DATA` block (columnar; one entry per land cell, 15,263 in all)

| Key | Meaning |
|---|---|
| `classes` | Terrain names in tab order: Plains, Hilly, Mountains, Coastal, Islands, Urban, Polar/Arid |
| `conts`, `contNames` | Continent codes and names in column order: AS, EU, AF, OC, NA, SA |
| `wmo` | WMO minimum per terrain, gauges per 1,000 km²: `[1.7391, 1.7391, 4, 1.1111, 40, 66.6667, 0.1]` |
| `groups` | 42 `[start, end)` index ranges into the arrays below. Group index `g = terrain*6 + continent` |
| `ix` | **West edge** longitude of the cell, integer degrees, -180..179. Cell longitude centre = `ix + 0.5` |
| `iy` | `floor(latitude centre)`. **Latitude centre = `iy + 0.163017`** for every cell (the source grid is offset from the integer lattice) |
| `n` | Number of gauges in the cell (0 means none) |
| `area` | Cell area in km², integer |
| `ctry` | Index into `countries` (174 names, sorted) |
| `noteMap` | Sparse map cell-index to index into `notes`; 620 cells carry a note |
| `countries`, `notes` | Name list and note strings (`notes[0]` is empty) |

### 7.2 Cell geometry (get this right or clicks land on the wrong cell)

- A cell spans longitude `[ix, ix+1]` and latitude `[iy - 0.336983, iy + 0.663017]`.
- Lookup from a point: `ix = floor(lon)`, `iy = floor(lat + 0.336983)`. Key: `(((ix+180)%360+360)%360)*1000 + (iy+90)`.
- **The explorer never snaps cells to a lattice**: the offset is part of the source data. (The map does snap, deliberately: see 7.6.)
- On the globe a cell is drawn as the four corners passed through the projection. It is visible if the dot product of its centre's unit vector with the view vector exceeds 0.03.

### 7.3 Derived values and the colour rule

- `d = n / area * 1000` (gauges per 1,000 km²).
- **Status:** `n === 0` gives *no gauge*; else `d >= wmo[terrain]` gives *meets*; else *below*. A continent diamond uses the same rule on its mean (over **all** cells in the group, zeros included).
- This matches the paper's own `density_delta < 0` rule on all 15,263 cells (0 disagreements).

### 7.4 Provenance and cleaning (kept here because the page no longer shows it)

- Source file: `Figure2/all_loc_gauge_density_1degree.csv` in `github.com/JJiaSu/Precipitation-Observing-Network-Gaps-Limit-Climate-Change-Impact-Assessment` (a supplement to Zenodo record 10.5281/zenodo.18364510, CC BY 4.0). The paper's plotting script draws Fig. 2c from this file.
- 123 cells in an eighth terrain class that the paper's script drops are excluded.
- **Country names were repaired**: the source labels India's 271 cells "Republic of Indonesia"; Algeria's and North Korea's labels are both truncated to "Democratic People"; the Chinese-name column disambiguates. 90 cells with no country were named from their location (Natural Earth). The source uses pre-2011 borders, so South Sudan's area is labelled Sudan, and the card carries a note. Names are tidied to common English names.
- `fig2c_gauge_density_by_cell.csv` (delivered separately) holds the full cleaned table.

### 7.5 Regenerating `rg-DATA`

Run this on `fig2c_gauge_density_by_cell.csv`. It reproduces the shipped block exactly (verified field by field). Replace the contents of `<script id="rg-DATA">` with its output.

```python
# Rebuild the DATA block of rain-gauge-globe.html from fig2c_gauge_density_by_cell.csv.
#   python regen_data.py fig2c_gauge_density_by_cell.csv > data.json
import sys, json, numpy as np, pandas as pd

CLASSES = ['Plains', 'Hilly', 'Mountains', 'Coastal', 'Islands', 'Urban', 'Polar/Arid']          # terrain order = tab order
CONTS = {'Asia': 'AS', 'Europe': 'EU', 'Africa': 'AF', 'Oceania': 'OC', 'North America': 'NA', 'South America': 'SA'}
NOTES = ['',
  'The source data has no country for this cell; it is named from the cell’s location.',
  'The source data uses pre-2011 borders, where this area is part of Sudan. Today it is in South Sudan.',
  'The source file’s English label for this cell reads “Republic of Indonesia”, but its Chinese name (印度) shows it is India.',
  'The source file’s English label is cut off (“Democratic People”); its Chinese name (阿尔及利亚) identifies Algeria.',
  'The source file’s English label is cut off (“Democratic People”); its Chinese name (朝鲜) identifies North Korea.']

c = pd.read_csv(sys.argv[1], encoding='utf-8-sig')
c = c[c.terrain_class.isin(CLASSES)].copy()                                    # drops the 123 cells in the eighth class the paper does not plot
c['cls'] = c.terrain_class.map({n: i for i, n in enumerate(CLASSES)})
c['cont'] = c.continent.map({n: i for i, n in enumerate(CONTS)})
countries = sorted(c.country.unique()); c['ctry'] = c.country.map({n: i for i, n in enumerate(countries)})
c['ix'] = (c.lon_centre - 0.5).round().astype(int)                              # west edge of the 1-degree cell
c['iy'] = np.floor(c.lat_centre).astype(int)                                    # latitude centre = iy + 0.163017 in every row
c['note'] = c.country_note.fillna('').map(lambda t: NOTES.index(t) if t in NOTES else 0)
c['area'] = c.cell_area_km2.round().astype(int)
c = c.sort_values(['cls', 'cont', 'iy', 'ix']).reset_index(drop=True)
groups = []
for k in range(7):
    for j in range(6):
        idx = c.index[(c.cls == k) & (c.cont == j)]; groups.append([int(idx.min()), int(idx.max()) + 1])
wmo = [round(float(c[c.cls == k].wmo_minimum_per_1000km2.iloc[0]), 4) for k in range(7)]
out = {'classes': CLASSES, 'conts': list(CONTS.values()), 'contNames': list(CONTS), 'wmo': wmo, 'countries': countries, 'notes': NOTES,
       'groups': groups, 'ix': c.ix.tolist(), 'iy': c.iy.tolist(), 'n': c.gauges_in_cell.astype(int).tolist(), 'area': c.area.tolist(),
       'ctry': c.ctry.tolist(), 'noteMap': {int(i): int(v) for i, v in c.note.items() if v}}
print(json.dumps(out, ensure_ascii=False, separators=(',', ':')))
```

---

### 7.6 How the map turns 1° cells into 0.5° dots

The source publishes counts only at 1°. The map shows them as 0.5° dots purely so it matches the page's other 0.5° layers. **That adds no information**, so never describe it as 0.5° measurements.

- **Snapping.** The source's 1° cell has longitude `[ix, ix+1]` and latitude centre `iy + 0.163017`. Each cell is moved onto the half-degree lattice as a block of longitude `[ix, ix+1]` and latitude `[iy - 0.5, iy + 0.5]`: a shift of exactly 0.163° (about 18 km) in latitude, nothing in longitude, no smoothing. Blocks tile without overlap because `(ix, iy)` is unique.
- **Four dots per block**, at the quarter centres: longitude `ix + 0.25` or `ix + 0.75`, latitude `iy - 0.25` or `iy + 0.25`. All four share the block's value, giving 15,263 × 4 = 61,052 dots.
- **Classes** use the explorer's cell density `d = n / area * 1000` with upper bounds 0.1, 0.5, 1, 2, 5 and 10. Counts of 1° cells per class (none to densest): `6,960 · 749 · 3,220 · 1,147 · 923 · 1,043 · 582 · 639`. They match the source CSV's own exact densities with **0** cells in a different class.
- **Picking.** Inverse-project the pointer to lon/lat; the block is `ix = floor(lon)`, `iy = floor(lat + 0.5)`; the quarter is east if `lon - ix >= 0.5` and north if `lat - (iy - 0.5) >= 0.5`. A near miss within a few pixels falls back to the nearest block, so tiny cells stay reachable.
- **Not on the map:** the 123 open-water cells (Caspian, Great Lakes, African lakes), and everything south of 56°S or north of 83°N, because the source has no cells there (so Antarctica is blank, and the page says so).

### 7.7 Why the map and the explorer use different resolutions

The explorer's chart and globe work per 1° cell (one square in the chart is one 1° cell). The map shows the same cells as 0.5° dots. This is known and was not harmonised. **Ask the human before changing either.**

---

## 8. Reference constants

| Item | Value |
|---|---|
| Chart markers | **one uniform square per cell**, 5.2 px a side (4.4 px when the chart is narrow); the size encodes nothing, because height already shows the density |
| Chart y scale | cube root, from 0.01 to `max(tab max density, WMO) * 1.1`, re-scaled per tab |
| Chart jitter | deterministic: fractional part of `sin((i+1)*12.9898)*43758.5453`, spread ±0.4 of a column |
| Globe | home lon 15, lat 22, zoom 1; fly easing 0.13 per frame; single-cell zoom `min(10, 18 / (R * pi/180))`; zoom limits 0.8 to 14 |
| Canvas sizing | measured from `canvas.getBoundingClientRect()` (not a wrapper), or clicks drift |
| Thresholds | drag starts after 5 px; double-tap 450 ms and 26 px (pick tolerance: touch 12 px, mouse 5 px) |
| Overlay alphas | none selected: green .92, faint .85, grey .5; a cell selected: .72 / .66 / .4; continent: .1 / .1 / .07; highlighted cells .97 |
| Coast and borders | contrast ramps in from zoom 1.2 to 3.0 |
| Breakpoints | 1180 px (tab padding), 920 px (stacked layout), 640 px (taller card), chart narrow mode under 520 px wide |
| Map dots | one square per 0.5° cell, side `max(0.3, R * zoom / 210)` px; drawn class by class (no gauge first, densest last); far side hidden beyond about 89° from the centre |
| Map globe | centre of the section, radius `0.42 * min(w, h)` (0.46 stacked); zoom 0.8 to 30; fly easing 0.13 per frame |
| Map pick tolerance | mouse 3 px, touch 12 px (plus 0.8 of a cell's screen size for near misses) |

---

## 9. Acceptance tests

Two Playwright scripts, one per section, embedded below. They passed against the shipped file: **21 checks for the map and 46 for the explorer on the combined file** (20 and 45 inside the main page, where the "only `d3` added" check does not apply).

**How to run** (needs `npm i playwright && npx playwright install chromium`):

- **Combined file on its own:** `RG_SCROLL=1 node smoke_dots.js <url>` and `RG_SCROLL=1 node smoke_scene.js <url>`. `RG_SCROLL` scrolls the section under test into view first, because each section sits at its own scroll position.
- **Inside the main page:** `RG_EMBEDDED=1 node smoke_dots.js <url>` and `RG_EMBEDDED=1 node smoke_scene.js <url>`. That also skips the "only `d3` added" check, and for the explorer it expects the phone globe to pin at the `--rg-topbar` offset and allows for the top-bar clearance in the "fits the screen" tolerance.
- If you rename ids, edit the `SEL` map at the top of `smoke_scene.js` and search for `rgm-` in `smoke_dots.js`.

**What the map test checks:** the section fits the viewport and the earth has no frame and fills it; the legend has eight classes, densest first; the title says "rain gauge" and the section never says "flood" or "stream"; **the pixel at a dot's centre is its class colour** (200 sampled dots; a few have a faint country-border line over them once zoomed in, which is expected); **dot size follows the story's `scale / 210`**; dots are separate with background between them (so they are not filled cells); the hover tooltip matches the data for 150 random cells; all four 0.5° quarters of a block report their own lattice-aligned bounds; a drag turns the globe; a plain wheel does not zoom it (and scrolls the page where the page can scroll) while Ctrl + wheel does; no globals except `d3`; other sizes; the phone layout and tap-to-read; no JavaScript errors.

**What the explorer test checks:** the layout (the scene fits the viewport, the panel is bordered, the globe has no border or box and fills the scene, the sphere is centred at 72%), every tab's square count (total 8,303), the one-line tab summary, the highest Plains square (a China cell, 35.8 per 1,000 km² at 31.2°N 118.5°E), the Africa diamond (0.086, faint) and North America diamond (green), the Urban cell at 122.1 that the paper's axis cuts off, that every marker is the same size and square, that a single click does nothing, that **100 of 100 double-clicks select exactly the cell clicked**, that selecting never resizes the scene, panel or globe, that a drag turns the globe without selecting, that no `<select>`, bullet list or "highlight" button exists, and the phone layout (sticky globe that stays pinned).

### smoke_dots.js

```js
// Smoke test for the rain-gauge DOTS MAP (section 1).   Usage:  node smoke_dots.js <url-or-file-url>
// Needs:  npm i playwright && npx playwright install chromium
// RG_SCROLL=1 scrolls the section into view first (use it on the combined page); RG_EMBEDDED=1 does that and also skips the "only d3 added" check (use it inside the main page).
// Every id is prefixed rgm-; if you rename anything while integrating, search for 'rgm-' below.
const { chromium } = require('/home/claude/.npm-global/lib/node_modules/playwright');
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
  const GCX = 720, GCY = 450, R = 0.42 * 900, RAD = Math.PI / 180;
  const proj = (lon, lat, z = 1, lon0 = 15, lat0 = 22) => { const dl = (lon - lon0) * RAD, ph = lat * RAD, p0 = lat0 * RAD, cosc = Math.sin(p0) * Math.sin(ph) + Math.cos(p0) * Math.cos(ph) * Math.cos(dl); return { x: GCX + R * z * Math.cos(ph) * Math.sin(dl), y: GCY - R * z * (Math.cos(p0) * Math.sin(ph) - Math.sin(p0) * Math.cos(ph) * Math.cos(dl)), cosc }; };
  const N = D.n.length;

  /* 1. layout and legend */
  const L = await page.evaluate(() => { const s = document.getElementById('rgm-scene'), cv = document.getElementById('rgm-globe'), w = cv.parentElement, cs = getComputedStyle(w), c = cv.getBoundingClientRect(), sr = s.getBoundingClientRect(); return { sceneH: Math.round(sr.height), fills: Math.abs(c.width - sr.width) < 1 && Math.abs(c.height - sr.height) < 1, border: cs.borderTopWidth, radius: cs.borderTopLeftRadius, bg: cs.backgroundColor, rows: [...document.querySelectorAll('#rgm-list .rgm-k')].map(e => e.innerText.trim()), title: document.querySelector('.rgm-title').innerText, label: /flood|stream/i.test(document.getElementById('rgm-scene').innerText) }; });
  check('scene fits the viewport', Math.abs(L.sceneH - 900) <= 2, L.sceneH);
  check('the earth has no frame and fills the scene', L.fills && L.border === '0px' && L.radius === '0px' && /rgba\(0, 0, 0, 0\)|transparent/.test(L.bg), JSON.stringify(L));
  check('legend: 8 classes, densest first', JSON.stringify(L.rows) === JSON.stringify(['10 or more', '5 to 10', '2 to 5', '1 to 2', '0.5 to 1', '0.1 to 0.5', 'under 0.1', 'no gauge']), JSON.stringify(L.rows));
  check('labelled as rain gauges, never as flood or stream gauges', /rain gauge/i.test(L.title) && !L.label, L.title);

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
  let bi = -1, bq = 0, bdist = 1e9; for (let i = 0; i < N; i++) for (let q = 0; q < 4; q++) { const p = dotPos(i, q, Z6); const d = Math.hypot(p.x - 720, p.y - 450); if (d < bdist && D.n[i] > 0 && Math.abs(p.x - 720) > 30) { bdist = d; bi = i; bq = q; } }
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
  { const f = await open(1440, 900); const h0 = await hash(f); await f.mouse.move(720, 450); await f.mouse.down(); await f.mouse.move(640, 470, { steps: 8 }); await f.mouse.up(); await f.waitForTimeout(150);
    check('drag turns the globe', (await hash(f)) !== h0, ''); check('a drag shows no tooltip', !(await f.locator('#rgm-tip').isVisible()), ''); await f.close(); }
  { const f = await open(1440, 900); const h1 = await hash(f); await f.mouse.move(720, 450);
    const y0 = await f.evaluate(() => scrollY), scrollable = await f.evaluate(() => document.documentElement.scrollHeight > innerHeight + 5);
    await f.mouse.wheel(0, 300); await f.waitForTimeout(300); const y1 = await f.evaluate(() => scrollY);
    check('a plain wheel does not zoom the globe (and scrolls the page when the page can scroll)', (await hash(f)) === h1 && (!scrollable || y1 > y0), JSON.stringify({ y0, y1, scrollable }));
    await f.mouse.move(720, 450); await f.keyboard.down('Control'); await f.mouse.wheel(0, -300); await f.keyboard.up('Control'); await f.waitForTimeout(250); check('Ctrl + wheel zooms', (await hash(f)) !== h1, ''); await f.close(); }
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
```

### smoke_scene.js

```js
// Smoke test for the rain-gauge SCENE.   Usage:  node smoke_scene.js <url-or-file-url>
// Needs:  npm i playwright && npx playwright install chromium
// RG_SCROLL=1 scrolls the section into view first (use it on the combined page).
// Inside the main page set RG_EMBEDDED=1: the scene is scrolled into view first, the "only d3" global check is skipped,
// and on phones the globe is expected to pin at the top-bar offset (--rg-topbar) instead of 0.
// Every id is prefixed rg-; if you rename anything while integrating, change the SEL map.
const { chromium } = require('playwright');
const SEL = { scene: '#rg-scene', panel: '#rg-panel', canvas: '#rg-globe', chart: '#rg-chart', squares: '#rg-chart .bub rect', diamonds: '#rg-chart path.dia', card: '#rg-card', tabinfo: '#rg-tabinfo', cap: '#rg-gcap', tip: '#rg-gtip', ring: '#rg-gSel rect.ring.sq', labelRing: '#rg-gSel rect.ring:not(.sq)' };
const EXPECT_SQUARES = { 'Plains': 2320, 'Hilly': 1516, 'Mountains': 2306, 'Coastal': 77, 'Islands': 282, 'Urban': 1088, 'Polar/Arid': 714 };   // total 8,303
(async () => {
  const browser = await chromium.launch(); let failed = 0;
  const check = (name, ok, got) => { if (!ok) failed++; console.log((ok ? 'PASS  ' : 'FAIL  ') + name + (ok ? '' : `   (got: ${got})`)); };
  const errors = [];
  const open = async (w, h, touch) => { const ctx = await browser.newContext({ viewport: { width: w, height: h }, isMobile: !!touch, hasTouch: !!touch }); const p = await ctx.newPage(); p.on('pageerror', e => errors.push(e.message)); await p.goto(process.argv[2]); await p.waitForTimeout(process.env.RG_EMBEDDED ? 1800 : 900); if (process.env.RG_EMBEDDED || process.env.RG_SCROLL) { await p.evaluate(() => document.querySelector('#rg-scene').scrollIntoView()); await p.waitForTimeout(900); } return p; };

  /* ---------- desktop 1440 x 900 ---------- */
  const page = await open(1440, 900);
  const card = async () => (await page.locator(SEL.card).innerText()).replace(/\s+/g, ' ');
  const clickTop = async () => { const pt = await page.evaluate(sel => { let best; document.querySelectorAll(sel).forEach(r => { const y = +r.getAttribute('y'); if (!best || y < best.y) best = { x: +r.getAttribute('x') + +r.getAttribute('width') / 2, y, h: +r.getAttribute('height') }; }); const b = document.querySelector('#rg-chart').getBoundingClientRect(); return { x: b.left + best.x, y: b.top + best.y + best.h / 2 }; }, SEL.squares); await page.mouse.click(pt.x, pt.y); await page.waitForTimeout(300); };
  const diamondClass = i => page.evaluate(([s, i]) => document.querySelectorAll(s)[i].getAttribute('class'), [SEL.diamonds, i]);
  const clickDiamond = async i => { const pt = await page.evaluate(([s, i]) => { const d = document.querySelectorAll(s)[i].getAttribute('d').match(/M([\d.]+) ([\d.]+)L/), b = document.querySelector('#rg-chart').getBoundingClientRect(); return { x: b.left + +d[1], y: b.top + +d[2] + 9.5 }; }, [SEL.diamonds, i]); await page.mouse.click(pt.x, pt.y); await page.waitForTimeout(300); };

  // 1. layout: bordered chart panel on the left, unframed globe on the right
  const L = await page.evaluate(([S, P, C]) => { const s = document.querySelector(S).getBoundingClientRect(), p = document.querySelector(P), pr = p.getBoundingClientRect(), cv = document.querySelector(C), cr = cv.getBoundingClientRect(), wrap = getComputedStyle(cv.parentElement);
    return { scene: [Math.round(s.width), Math.round(s.height)], panelLeft: pr.left < s.width / 2 && pr.right < s.width * 0.55, panelBorder: getComputedStyle(p).borderTopWidth, canvasBorder: getComputedStyle(cv).borderTopWidth, wrapBorder: wrap.borderTopWidth, wrapBg: wrap.backgroundColor, wrapRadius: wrap.borderTopLeftRadius, canvasCoversScene: Math.abs(cr.width - s.width) < 1 && Math.abs(cr.height - s.height) < 1, selects: document.querySelectorAll(S + ' select').length, bullets: document.querySelectorAll(S + ' ul, ' + S + ' li').length, highlightButtons: [...document.querySelectorAll(S + ' button')].filter(b => /highlight/i.test(b.textContent)).length }; }, [SEL.scene, SEL.panel, SEL.canvas]);
  check('scene fits the viewport (1440x900)', L.scene[0] === 1440 && Math.abs(L.scene[1] - 900) <= 2, L.scene);
  check('chart panel is on the left and has a 1px border', L.panelLeft && L.panelBorder === '1px', JSON.stringify([L.panelLeft, L.panelBorder]));
  check('globe has no border, no radius, no box background', L.canvasBorder === '0px' && L.wrapBorder === '0px' && L.wrapRadius === '0px' && /rgba\(0, 0, 0, 0\)|transparent/.test(L.wrapBg), JSON.stringify([L.canvasBorder, L.wrapBorder, L.wrapRadius, L.wrapBg]));
  check('globe canvas fills the whole scene (full bleed)', L.canvasCoversScene, '');
  check('no country menu, no "highlight" button, no bullet lists', L.selects === 0 && L.highlightButtons === 0 && L.bullets === 0, JSON.stringify([L.selects, L.highlightButtons, L.bullets]));
  // sphere centred at 72% of the width: opaque just inside the right edge, transparent just outside it
  const edge = await page.evaluate(sel => { const c = document.querySelector(sel), x = c.getContext('2d'), W = c.getBoundingClientRect().width, H = c.getBoundingClientRect().height, dpr = c.width / W, GCX = W * 0.72, R = Math.min(Math.min(W, H) * 0.42, W * 0.28 - 8); const a = px => x.getImageData(Math.round(px * dpr), Math.round(H / 2 * dpr), 1, 1).data[3]; return { inside: a(GCX + R - 4), outside: a(GCX + R + 6), centre: a(GCX) }; }, SEL.canvas);
  check('sphere is centred at 72% of the width (edge pixels)', edge.inside > 0 && edge.outside === 0 && edge.centre > 0, JSON.stringify(edge));

  // 2. chart data
  for (const [name, n] of Object.entries(EXPECT_SQUARES)) {
    await page.getByRole('tab', { name, exact: true }).click(); await page.waitForTimeout(250);
    const got = await page.locator(SEL.squares).count(); check(`${name}: ${n} squares`, got === n, got);
    check(`${name}: 6 diamonds`, (await page.locator(SEL.diamonds).count()) === 6, await page.locator(SEL.diamonds).count());
  }
  await page.getByRole('tab', { name: 'Plains', exact: true }).click(); await page.waitForTimeout(250);
  const info = (await page.locator(SEL.tabinfo).innerText()).replace(/\s+/g, ' ');
  check('Plains summary line (one line)', info === 'Plains · WMO minimum 1.74 per 1,000 km² · 2,320 of 4,130 cells have a gauge', info);
  check('summary stays on one line', (await page.locator(SEL.tabinfo).evaluate(e => e.getBoundingClientRect().height)) < 24, '');
  await clickTop(); let c = await card();
  check('Plains: the highest square is China, 35.8, 31.2°N 118.5°E', /China/.test(c) && /35\.8 gauges/.test(c) && /31\.2°N, 118\.5°E/.test(c), c.slice(0, 120));
  check('a square ring is drawn on the selected square', (await page.locator(SEL.ring).count()) === 1, '');
  check('globe caption names it', /China/.test(await page.locator(SEL.cap).innerText()), '');
  await clickDiamond(2); c = await card();
  check('Africa diamond: average 0.086, 405 cells with no gauge', /Africa average/.test(c) && /0\.086 gauges/.test(c) && /405 cells \(63%\)/.test(c), c.slice(0, 140));
  check('Africa diamond is "below", N. America diamond is "meets"', /\blo\b/.test(await diamondClass(2)) && /\bhi\b/.test(await diamondClass(4)), '');
  await page.keyboard.press('Escape'); check('Escape clears the selection', /Each square is one/.test(await card()), (await card()).slice(0, 60));
  await page.getByRole('tab', { name: 'Urban', exact: true }).click(); await page.waitForTimeout(250); await clickTop(); c = await card();
  check('Urban: the highest square is the US cell at 122.1', /United States/.test(c) && /122\.1 gauges/.test(c), c.slice(0, 120));
  await page.getByRole('tab', { name: 'Plains', exact: true }).click(); await page.waitForTimeout(250);

  // 2b. markers: every cell is the same size and square (height alone carries the density), and the legend swatches match
  { const m = await page.evaluate(() => { const rs = [...document.querySelectorAll('#rg-chart .bub rect')], w = new Set(rs.map(r => r.getAttribute('width'))), h = new Set(rs.map(r => r.getAttribute('height'))), sw = getComputedStyle(document.querySelector('.rg-legend .rg-sw')).borderTopLeftRadius;
      return { n: rs.length, widths: [...w], heights: [...h], circles: document.querySelectorAll('#rg-chart .bub circle').length, swatchRadius: sw }; });
    check('every Plains cell is the same size and square', m.n === 2320 && m.widths.length === 1 && m.heights.length === 1 && m.widths[0] === m.heights[0] && m.circles === 0, JSON.stringify(m));
    check('legend swatches are squares, not circles', parseFloat(m.swatchRadius) < 5, m.swatchRadius); }
  // 3. globe clicks: single click does nothing, double-click selects exactly that cell
  await page.keyboard.press('Escape'); await page.click('#rg-greset');   // chart clicks fly the globe; return to the home view the maths below assumes, and wait until it has stopped moving
  { let last = '', same = 0; for (let t = 0; t < 40 && same < 4; t++) { await page.waitForTimeout(250); const h = await page.evaluate(sel => { const c = document.querySelector(sel), d = c.getContext('2d').getImageData(0, 0, c.width, c.height).data; let x = 0; for (let i = 0; i < d.length; i += 97) x = (x * 31 + d[i]) | 0; return x; }, SEL.canvas); same = h === last ? same + 1 : 0; last = h; } }
  const D = await page.evaluate(() => JSON.parse(document.getElementById('rg-DATA').textContent));
  const fmtD = d => d >= 10 ? d.toFixed(1) : d >= 0.1 ? d.toFixed(2) : d.toFixed(3);
  const cells = []; for (let g = 0; g < 42; g++) { const [s, e] = D.groups[g]; for (let i = s; i < e; i++) cells.push({ cls: Math.floor(g / 6), lon: D.ix[i] + 0.5, lat: D.iy[i] + 0.163017, n: D.n[i], area: D.area[i], ctry: D.ctry[i] }); }
  const box = await page.evaluate(sel => { const r = document.querySelector(sel).getBoundingClientRect(); return { x: r.left, y: r.top, w: r.width, h: r.height }; }, SEL.canvas);
  const GCX = box.x + box.w * 0.72, GCY = box.y + box.h / 2, R = Math.min(Math.min(box.w, box.h) * 0.42, box.w * 0.28 - 8), RAD = Math.PI / 180;
  const proj = (lon, lat) => { const dl = (lon - 15) * RAD, ph = lat * RAD, p0 = 22 * RAD, cosc = Math.sin(p0) * Math.sin(ph) + Math.cos(p0) * Math.cos(ph) * Math.cos(dl); return { x: GCX + R * Math.cos(ph) * Math.sin(dl), y: GCY - R * (Math.cos(p0) * Math.sin(ph) - Math.sin(p0) * Math.cos(ph) * Math.cos(dl)), cosc }; };
  const wpx = c => Math.hypot(proj(c.lon - .5, c.lat).x - proj(c.lon + .5, c.lat).x, proj(c.lon - .5, c.lat).y - proj(c.lon + .5, c.lat).y);
  const vis = cells.filter(c => c.cls === 0 && proj(c.lon, c.lat).cosc > 0.3 && proj(c.lon, c.lat).x > 740 && wpx(c) >= 1.8);   // right of the panel, wide enough to hit
  const before = await card(), q0 = proj(vis.find(c => c.n > 0).lon, vis.find(c => c.n > 0).lat);
  await page.mouse.click(q0.x, q0.y); await page.waitForTimeout(250);
  check('single click on a cell selects nothing', (await card()) === before, (await card()).slice(0, 60));
  let seed = 11; const rnd = () => (seed = (seed * 1664525 + 1013904223) % 4294967296) / 4294967296; let ok = 0; const bad = [];
  for (let i = 0; i < 100; i++) { const c0 = vis[Math.floor(rnd() * vis.length)], q = proj(c0.lon, c0.lat); await page.mouse.dblclick(q.x, q.y); await page.waitForTimeout(16);
    const want = D.countries[c0.ctry] + (c0.n ? '  ' + fmtD(c0.n / c0.area * 1000) + ' per 1,000 km²' : '  no gauge'), got = (await page.locator(SEL.cap).innerText()).replace(/\s+/g, ' ');
    if (got.startsWith(want.replace(/\s+/g, ' '))) ok++; else bad.push([got.slice(0, 50), want]); }
  check(`double-click selects exactly the cell clicked (${ok}/100)`, ok === 100, JSON.stringify(bad.slice(0, 2)));
  const g1 = vis.find(c => c.n > 0), q1 = proj(g1.lon, g1.lat); await page.mouse.dblclick(q1.x, q1.y); await page.waitForTimeout(250);
  check('double-click on a gauged cell rings its square in the chart', (await page.locator(SEL.ring).count()) === 1, await page.locator(SEL.ring).count());
  const g0 = vis.find(c => c.n === 0), q2 = proj(g0.lon, g0.lat); await page.mouse.dblclick(q2.x, q2.y); await page.waitForTimeout(250);
  check('double-click on a grey cell: card says no gauge, label ringed, no square ring', /No gauge in this cell/.test(await card()) && (await page.locator(SEL.labelRing).count()) === 1 && (await page.locator(SEL.ring).count()) === 0, (await card()).slice(0, 70));
  // selecting must not resize anything (the card has a fixed height): check with a cell that carries a note and with a grey cell
  { const geo = () => page.evaluate(([S, C, P]) => [document.querySelector(S).offsetHeight, Math.round(document.querySelector(C).getBoundingClientRect().height), document.querySelector(P).offsetHeight], [SEL.scene, SEL.canvas, SEL.panel]);
    const g0b = await geo(); const india = cells.find(c => c.cls === 0 && D.noteMap && c.n > 0 && D.countries[c.ctry] === 'India' && proj(c.lon, c.lat).cosc > 0.3 && proj(c.lon, c.lat).x > 740);
    if (india) { const qi = proj(india.lon, india.lat); await page.mouse.dblclick(qi.x, qi.y); await page.waitForTimeout(300); }
    const g1b = await geo(); await page.mouse.dblclick(q2.x, q2.y); await page.waitForTimeout(300); const g2b = await geo();
    check('selecting a cell (with or without a note) does not change the scene, panel or globe size', JSON.stringify(g0b) === JSON.stringify(g1b) && JSON.stringify(g0b) === JSON.stringify(g2b), JSON.stringify([g0b, g1b, g2b])); }
  const sel0 = await card(); await page.mouse.move(GCX, GCY); await page.mouse.down(); await page.mouse.move(GCX - 90, GCY + 20, { steps: 8 }); await page.mouse.up(); await page.waitForTimeout(150);
  check('a drag turns the globe and selects nothing', (await card()) === sel0, '');
  await page.mouse.move(q1.x + 400, q1.y); // (moved away) hover on a known cell:
  await page.mouse.move(proj(g1.lon, g1.lat).x, proj(g1.lon, g1.lat).y); await page.waitForTimeout(100);
  // (after the drag the view changed, so just check the tooltip element exists and is hidden over empty space)
  await page.mouse.move(box.x + 6, box.y + box.h - 6); await page.waitForTimeout(80);
  check('globe tooltip hidden over empty space', !(await page.locator(SEL.tip).isVisible()), '');
  const globals = await page.evaluate(() => { const f = document.createElement('iframe'); document.body.appendChild(f); const base = new Set(Object.getOwnPropertyNames(f.contentWindow)); f.remove(); return Object.getOwnPropertyNames(window).filter(k => !base.has(k)); });
  if (!process.env.RG_EMBEDDED) check('only one global added (d3)', globals.length === 1 && globals[0] === 'd3', JSON.stringify(globals));
  await page.close();

  /* ---------- other sizes ---------- */
  for (const [w, h] of [[1280, 720], [1920, 1080], [1024, 768]]) { const p = await open(w, h); const m = await p.evaluate(sel => ({ h: Math.round(document.querySelector(sel).getBoundingClientRect().height), over: document.documentElement.scrollWidth > innerWidth, ph: Math.round(document.querySelector('#rg-panel').getBoundingClientRect().height) }), SEL.scene);
    const tol = (w < 1100 ? 45 : 12) + (process.env.RG_EMBEDDED ? 45 : 0);   // a narrow window wraps the tab strip; inside the main page the top-bar clearance (--rg-topbar, ~45px) adds to it
    check(`${w}x${h}: scene fits within ${h + tol}px, no sideways scroll`, m.h <= h + tol && !m.over, JSON.stringify(m)); await p.close(); }

  /* ---------- phone 390 x 844 ---------- */
  const ph = await open(390, 844, true);
  const pm = await ph.evaluate(sel => { const w = getComputedStyle(document.querySelector('#rg-globe').parentElement); return { pos: w.position, over: document.documentElement.scrollWidth > innerWidth, tabsScroll: document.querySelector('#rg-tabs').scrollWidth > document.querySelector('#rg-tabs').clientWidth }; }, SEL.scene);
  check('phone: stacked layout, globe is sticky, no sideways scroll', pm.pos === 'sticky' && !pm.over, JSON.stringify(pm));
  const sceneTop = await ph.evaluate(() => window.scrollY + document.querySelector('#rg-scene').getBoundingClientRect().top);
  await ph.evaluate(y => window.scrollTo(0, y + 700), sceneTop); await ph.waitForTimeout(300);
  const top = await ph.evaluate(() => Math.round(document.querySelector('#rg-globe').parentElement.getBoundingClientRect().top)), want = await ph.evaluate(() => Math.round(parseFloat(getComputedStyle(document.querySelector('#rg-globe').parentElement).top) || 0));
  check('phone: globe stays pinned at the top (at the top-bar offset) while the panel scrolls', Math.abs(top - want) <= 1, JSON.stringify({ top, want }));
  const R2 = await ph.evaluate(() => { const c = document.querySelector('#rg-globe').getBoundingClientRect(); return [Math.round(c.width), Math.round(c.height)]; }); check('phone: globe canvas is wider than tall and under 340px', R2[1] <= 340, JSON.stringify(R2));
  await ph.close();

  check('no JavaScript errors', errors.length === 0, errors.join(' | '));
  console.log(failed ? `\n${failed} check(s) FAILED` : '\nall checks passed'); await browser.close(); process.exit(failed ? 1 : 0);
})();
```

**Manual checks** the scripts do not cover:
1. Scroll from the last story step into the map, then on into the explorer: each arrives opaque, the story's globe and card are hidden behind them, and nothing from the story shows through.
2. Press the main page's Explore button: **neither section is visible** (step 6). Press Story: they return below the steps.
3. The top edge of each section clears the fixed top bar; the explorer's zoom buttons and the map's are not under it.
4. Plain mouse wheel over either globe scrolls the page; Ctrl/Cmd + wheel zooms the globe under the pointer.
5. Press `D` while a section is on screen: the main page's control panel opens as it always does, and nothing in the sections triggers it.
6. Resize through 1180, 920, 760, 640 and 520 px: no horizontal scroll; the explorer's globe stays pinned when stacked.
7. Phone or touch emulation: tapping a dot shows its value; in the explorer a double-tap selects, a single tap does nothing, and a finger-drag turns the globe without scrolling the page.

---

## 10. Deliberate decisions: do not "fix" these

- **The detail card has a fixed height.** Selecting a cell used to grow the panel, which grew the scene, which resized the globe's canvas and shifted the sphere by a few pixels, so the next double-click landed on the wrong cell. Never let selection change the height of the panel.
- **No `overflow:hidden` on `.rg-scene`.** It turns the scene into a scroll container, and the phone layout's sticky globe stops sticking. The canvas is exactly scene-sized, so nothing needs clipping.
- **`box-sizing:border-box` applies to the scene element itself**, not just its children, or `min-height:100vh` plus padding overshoots the viewport.
- **The globe is unframed and full-bleed; the panel is bordered.** Do not add a border, rounded corners or a background to the globe wrapper.
- **Cube-root y-axis, rescaled per tab.** The paper uses one shared axis capped at 85, which hides one US cell (122.1). Here it is drawn.
- **Chart markers are uniform squares.** Size used to scale with density, which only repeated what the height already shows, and square markers match the square cells on the globe. Do not reintroduce a size encoding, and keep the legend swatches, the grey "no gauge" markers under the columns and the selection ring square.
- **Zero-gauge cells are not squares.** They are counted in the diamonds and shown grey on the globe.
- **Colour = status, not continent.**
- **The data is 1°.** The explorer works per 1° cell. The map splits each cell into four 0.5° dots with the same value, after snapping to the lattice (section 7.6), only to match the page's other layers. Do not smooth, interpolate or otherwise manufacture finer data, and never present it as 0.5° measurements.
- **Corrected country labels** (section 7.4). Do not revert to the raw label column.
- **The scene ships its own land layer** (Natural Earth 50m, simplified). The main page's land has only 127 polygons, so on the Islands and Coastal tabs cells would float over blank sea.
- **A double-click on the globe does not move the view**; only chart clicks fly the globe. The globe never captures the plain mouse wheel.
- No `localStorage`, cookies or network calls.

---
- **Map: the dots are the story page's dots.** Same shape (a square), same size formula (`scale / 210`), drawn at cell centres, one per cell. Do not turn them into filled cells and do not scale them by density.
- **Map: class colours, not a brightness ramp.** The story page shows density as brightness of one hue; the map uses the eight discrete colours of its legend, and the legend was approved as it is. Keep dots and legend in step.
- **Map: no-gauge cells are drawn as grey dots**, because "no gauge" is a legend row.
- **Map: the hover shows 0.5° bounds and the parent 1° cell's gauge count**, so nobody mistakes a dot for a 0.5° measurement.
- **Map: keep the order** (map first, explorer second) and the label "Rain gauge density".

---

## 11. Attribution to keep in the page

The scene's source line must stay visible:

- Su, J. *et al.* "Precipitation observing network gaps limit climate change impact assessment". *Nature* 652, 119–125 (2026), Fig. 2c. Data: Zenodo record 10.5281/zenodo.18364510, **CC BY 4.0**.
- The scene is built from that published **data**; it does not reproduce the article's figure (the article itself is CC BY-NC-ND).
- Country names tidied using Natural Earth (public domain). Land and borders: Natural Earth 50m, simplified.
- d3-array and d3-geo (Mike Bostock; d3-geo also Charles Karney): keep the licence header comments at the top of the d3 blocks (the main page's copies already have them).
- Fonts: IBM Plex Sans and Space Grotesk (SIL Open Font License).

Both sections carry their own one-line source credit; keep both.

---

## 12. Known limitations (not bugs to chase)

- **Touch on wide screens.** The canvas fills the scene with `touch-action:none`, so on a tablet in landscape, a vertical swipe that starts on the globe turns the globe instead of scrolling the page. Scrolling from the panel or the left margin still works. The phone layout (920 px and below) has a short pinned globe, so this does not apply there.
- Squares are not keyboard-focusable; tabs and the canvas keys are the keyboard route.
- Cells under about 1 px on screen (high latitudes at the overview zoom) cannot be targeted until you zoom in; that is geometry, not a picking bug.
- Coastal cells can overlap the sea: each cell is a 1° square around one centre point.
- One instance per page (one IIFE, one set of state).
- At about 1000 px wide or narrower in desktop layout, the tab strip wraps and the scene can be up to about 45 px taller than the screen.
- **The map's globe takes vertical swipes on a phone.** The canvas has `touch-action:none`, so a swipe that starts on the earth turns it instead of scrolling the page. The heading above it and the legend below it scroll normally. If that proves annoying, `touch-action:pan-y` on the stacked layout lets vertical swipes scroll (and limits turning by touch to horizontal drags).
- Dots near the globe's edge keep their screen size while their spacing foreshortens, so they overlap there. The story page's own dots do the same.
- The map draws 61,052 dots by hand each frame (the projection is computed inline, not through d3). That is fast in a real browser; headless software rendering is much slower, so do not judge frame rate from a headless run.

