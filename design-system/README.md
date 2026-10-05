# Weather Machine design system

One visual language for *The Gaps in the Weather Machine* and every prototype
around it. **It is authoritative** (author's decision, 5 Oct 2026): every page follows
it, and where a page or a prototype's own notes disagree on anything visual, this wins.
The grid standard (land 0.5°, ocean 1°) applies to every page too. It was written from what the pages already do (an audit on
4 Oct 2026, below), so most of it is the main site's look made explicit, with
the drift between pages removed.

| File | What it is |
|---|---|
| `wm.css` | Tokens (colour, type, space, shape, motion) and `wm-*` components |
| `wm.js` | The same tokens for canvas drawing, plus the globe's rendering rules (`WM.*`) |
| `inline.py` | Puts both into a page at build time, so pages stay single self-contained files |
| `specimen.html` | The visual reference: every token and component, rendered (`build_specimen.py`) |

## Principles

1. **The night side of the planet.** Dark ground, light data. Colour belongs to
   the data; everything else (text, lines, controls) is warm grey.
2. **One hue, one meaning, everywhere.** Amber is always weather stations, blue is
   always Argo. A colour never stands for two things, even on different pages.
3. **Say what is shown, and what is not.** Every card names its source. Anything
   not real is labelled *illustrative* where it appears. Keys say what a layer is
   not when it could be mistaken (shark *sightings*, not the tagged sharks).
4. **Lines before boxes.** Cards over the globe are the only boxed elements.
   Fields are underlines, buttons are outlines, rules separate rows. No drop shadows.
5. **The globe is always there.** Words on the left, globe on the right. When a big
   image takes the stage, the globe minimises to the top-right corner; it never leaves.
   The camera moves only to show the reader where to look.
6. **Every image is framed.** A white frame round every photograph: 16:9 inside
   cards, 4:3 for big images beside the text.

## Colour

### Interface

| Token | Value | Use |
|---|---|---|
| `--wm-bg` | `#05080E` | Page and space |
| `--wm-raised` | `#080C13` | Side panels |
| `--wm-glass` | `rgba(5,8,14,.84)` + 14px blur | Cards over the globe |
| `--wm-ocean` / `--wm-land` / `--wm-coast` / `-2` | `#0B121B` / `#161D26` / `#242E3A` / `#4A5B6E` | Sphere; flat land; its coastline; coastlines and borders once zoomed in |
| `--wm-relief-lo` / `-hi` | `#14171B` / `#40454B` | Shaded relief |
| `--wm-text` | `#ECEAE5` | Headings, numbers, primary text |
| `--wm-text-2` | `#D9D6CF` | Running text in cards |
| `--wm-muted` | `#8B95A1` | Subtitles, notes, labels |
| `--wm-faint` | `#5C6773` | Sources, fine print |
| `--wm-line` / `-soft` | `#222C38` / `#1B2531` | Card borders; dividers |
| `--wm-outline` | `rgba(236,234,229,.55)` | Buttons and controls at rest |
| `--wm-track` | `rgba(236,234,229,.26)` | Slider tracks, empty checkboxes |
| `--wm-rim` / `--wm-grat` | `.35` / `.07` of text | Globe edge; graticule |
| `--wm-alert` / `--wm-ok` | `#E8433F` / `#3FB6A8` | Status in the interface only |

Four text greys, no more. Pure white (`#FFFFFF`) is not used; the lightest colour
is `--wm-text`.

### Data: instruments (who is watching)

| Token | Value | Meaning |
|---|---|---|
| `--wm-station` | `#FFB547` | Weather stations (GHCN-Daily) |
| `--wm-station-2` | `#FFD08A` | Stations by record length |
| `--wm-gauge` | `#3FD98A` | Rain gauges: the rain-gauge prototype's green (decided 5 Oct); was Argo blue in the country profile |
| `--wm-gauge-lo` / `-no` / `-wmo` | `#2A6B49` / `#76818D` / `#58C48A` | Below the WMO minimum / no gauge / the minimum line |
| `--wm-gauge-0` … `-7` | `#2E3745` → `#E3FFF0` | Gauge density, 8 classes per 1,000 km² (none, <0.1 … 10+); `WM.gaugeClass()` |
| `--wm-argo` | `#45B0CE` | Argo floats |
| `--wm-seal` | `#6FD8B4` | Seal-borne profiles |
| `--wm-shark` | `#F07A55` | Sharks |
| `--wm-tracked` | `#B98CE0` | Tracked animals without sensors |
| `--wm-turtle` | `#C6E377` | Turtles |
| `--wm-sat` | `#CBD6E2` | Satellites |
| `--wm-gap` | `#E4EEFF` | Coldspots, where nobody measures |

### Data: impacts (what happens to people)

| Token | Value | Meaning |
|---|---|---|
| `--wm-deaths` | `#E8433F` | Deaths |
| `--wm-affected` | `#F2C744` | People affected |
| `--wm-damage` | `#5BC8A8` | Damage. Close to seal teal: never on screen together |
| `--wm-flood` | `#7DB4D1` | Flood extent on maps; people at risk of a 1-in-100-year flood |
| `--wm-displaced` | `#B98CE0` | Displacements (movements, not people). Same value as `--wm-tracked`: never on screen together |
| `--wm-settle` / `-x` | `#E05CC8` / `#FF3D6E` | Settlements before / gone |
| `--wm-warn-22` / `-25` | `#F5D04A` / `#F08A3E` | Reported an early warning system, 2022 / added by 2025 |
| `--wm-dmg-3` / `-2` / `-1` | `#E8433F` / `#F29A3A` / `#5C6773` | Buildings destroyed / damaged / possibly damaged (Copernicus EMS grades). Destroyed shares the impact red with deaths: both are the worst outcome |
| `--wm-ts` … `--wm-c5` | `#F5E06A` → `#B81D2C` | Storm intensity, tropical storm to category 5 (Saffir-Simpson) |

Photo placeholders use `WM.PLACEHOLDER`: muted, darker than any data colour, so
an empty photo never reads as data.

## Type

Space Grotesk for display (titles, numbers), IBM Plex Sans for everything else.
Georgia italic only for water names on maps.

| Role | Class / token | Setting |
|---|---|---|
| Hero number (a year) | `.wm-hero` | 500, clamp(4–7.5rem), −.04em, tabular |
| Page title | `.wm-display` | 400, clamp(1.9–2.7rem), −.02em, balanced |
| Stat | `.wm-stat` | 500, clamp(1.7–2.6rem), −.02em, tabular |
| Card title | `.wm-title` | 500, 1.25rem, −.01em |
| Narration | `.wm-lead` | 1.125rem / 1.55, with halo |
| Body | `.wm-body` | .875rem / 1.55, `--wm-text-2`, max 62ch |
| Subtitle / note | `.wm-sub` / `.wm-note` | muted |
| Label (kicker, key, hint) | `.wm-label` | 600, ~10.5px, uppercase, +.1em |
| Source | `.wm-source` | .75rem, faint, journal in italics |
| Map: country / water / town | `.wm-place` / `.wm-water` / `.wm-town` | spaced caps / serif italic / sans |

**Slide text sits in one place (author's rule, 5 Oct).** On every slide of the story, and in
every prototype section placed in it, the narrative is the core: label (the act), title
(`.wm-display`), narration (`.wm-lead`), in the left column at `--wm-slide-top` (left edge
`--wm-slide-left`, past the slide navigator when the page has one), the same
top edge on every slide (`.wm-slide`). Everything else (interactive controls, legends,
bars, labels, hints) goes **below** the narration, under a rule, and the source line comes
last. The block never moves between slides; a slide's camera moves never re-draw it.
Pull quotes use `.wm-quote` inside it.

Root size is 16px on every page (the main site is 17px and the prototypes 15px
today). Uppercase is only for labels, hints, keys and country names on maps.

## Images

- **Every image sits in a white frame**: 1px `--wm-frame` (`#ECEAE5`, the system's
  white), 2px corners. No unframed, full-bleed or background photographs.
- **Three ratios, each with one job.** `.wm-photo`, 16:9, for photos inside cards (story
  cards, with the ↗ link in the bottom-right corner, and an instrument's first
  appearance). `.wm-figure.is-side`, **4:3**, for big images shown beside the text
  (Idai's devastation). **1:1** only for an instrument card once it has shrunk to a row.
- **Instrument photos are tinted to the instrument's map colour** (grayscale image,
  luminosity blend over the colour: the main site's duotone), so the photo, its dot and
  its layer on the globe read as one thing.
- A big side image fills most of the right side: up to 56vw wide, as tall as the screen
  allows. **The corner globe is centred on the image's top-right corner**: the image is inset
  by one globe radius from the right and from the top, so the corner point falls exactly on
  the globe's centre and the frame's two edges run out from under it. On phones the image
  drops into the flow, full width.
- Every image carries a credit line underneath (`.wm-credit`). Instrument cards are the
  one exception: their photos are credited together in the scene's source line, so the
  legend stays compact. No credit, no image: photos whose licence is not cleared stay
  placeholders.
- Instrument photos live in `assets/instruments/` with a register
  (`instruments.json`: tint, crop focus, credit, licence, status).
- Placeholders are the same frame filled with a `WM.PLACEHOLDER` colour.
- **Exception for the final page (author's decision, 5 Oct):** every photo is shown, cleared or
  not, with the credit line "Credit to come" until the author fixes attribution. Once embedded,
  the photos travel inside the built page, so clear them before the repo goes public.

## Space and shape

- Space in 4px steps: 4, 8, 12, 16, 24, 32, 48, 64 (`--wm-s1` … `--wm-s8`).
  Page edge `--wm-gutter` = max(16px, 4vw). Running text at most 62ch.
- Three radii only: **2px** controls and photos, **3px** cards and tooltips,
  **50%** dots and round buttons. No pills.
- 1px lines everywhere; 1.2px for globe markers; 1.5px focus outline.
- No shadows. Words set straight over the globe get the text halo (`--wm-halo`).

## Components

| Component | Class | Notes |
|---|---|---|
| Instrument card | `.wm-instruments` > `.wm-instrument` (`.is-row`) | First appearance: 16:9 tinted photo, dot + name + one line below. When the next instrument arrives the earlier ones become rows (64px square photo, name and its one line beside; 44px on screens under 820px tall, so a stack of four fits under a slide's words); the stack is the legend. `--tint` sets the colour. The line is the instrument's number of sensors (the final page, 5 Oct) |
| Side image | `.wm-figure.is-side` > `.wm-frame` + `.wm-credit` | 4:3, white frame, most of the right side; the corner globe is centred on its top-right corner |
| Inline link | `.wm-link` | A word in running text that leads to its data or source: underlined, in the text's own colour (e.g. "seals" in the seal story links to the seal data) |
| Slide text | `.wm-slide` > `.wm-label`, `.wm-display`, `.text` > `.wm-lead`, `.below`, `.wm-source` | One fixed place for every slide's narrative; everything else below it |
| Slide navigator | `nav.wm-nav` > `ol` > `li.act` (`.is-on`) > `.num` + `ol` > `li` > `button.ln` (`.is-past`, `aria-current`); `.wm-nav-mini` on phones; `.has-wm-nav` on the body | One short line per slide in the left margin, following the scroll; the section's numeral left of its first line, lit for the current section; current line longer, in `--wm-text`; visited `--wm-muted`; upcoming `--wm-faint`. No names on screen: each line's `aria-label` is its slide's title. Click or Enter jumps; ↑ ↓ move between lines. Tokens `--wm-nav-*`; the slide text moves past it (`--wm-slide-left`). Phones: "III · 7 / 24" |
| Pull quote | `.wm-quote` + `.wm-note` | A quoted line set large inside the slide text, attribution below |
| Bars | `.wm-bars` > `.wm-bar` (`.is-ref`) > `.k`, `.v`, `.track` > `.fill` | One shared scale, the largest value fills the track; solid = subject, outlined = comparison; `--c` from a data token |
| Bar pair | `.track.is-pair` > `.fill` + `.fill.is-ref`; `.v .ref` | Subject and comparison in one bar (country profile): the subject in its colour above, the comparison solid white below, same thickness, same scale; one bar per line, always horizontal. A faded fill with a solid `.part` shows a share (floods within all disasters) |
| Events | `.wm-events` > `.axis` > `.yr`, `.ev.is-up` / `.ev.is-down` (`--tier`) > `.lb` | A thin dated timeline (slide 21): one hairline, a year label per year, events on tiers above (one side, e.g. the US) and below (the rest), each with a hairline to its date |
| Events, vertical | `.wm-events.is-vertical` > `.key`, `ol` > `li.is-up` / `li.is-down` > `.when`, `.dot`, `.lb` | The dated timeline as a list (slide 23, the author's choice): one event a row in date order, evenly spaced, dots on one hairline; filled for one side, hollow for the other |
| Link cards | `.wm-links` > `a` > `.wm-label`, `.name` (+ arrow), `.what` | Where to go next (the last slide): a 2 × 2 grid of outlined cards; the whole card is the link, opening in a new tab. The outline turns white on hover and focus |
| Dial | `.wm-dial` > `svg` (`.track`, `.val`, `.val.lap`) + `.nums` | A thin-line ring for a quantity against a unit (slide 23); no clock face. A value past one unit laps on an inner ring in a second colour. Draws in over 1.6 s; none with reduced motion |
| Card | `.wm-card` (`.is-tight` for side cards) | Glass, 1px line, 3px. The only box |
| Bare narration | `.wm-bare` | No box; title, sub, stat get the halo |
| Card photo | `.wm-photo` (`.is-duotone`, `--tint`) | 16:9, white frame; link-out button in its bottom-right corner. `.is-duotone`: the photo in grayscale over its tint, as the instrument cards (the stories use each story's colour) |
| Button | `.wm-btn` (`.is-on`, `.is-primary`) | Outlined rectangle, 2px; filled when on |
| Segmented | `.wm-seg` | Story / Explore, Flood / Others |
| Icon button | `.wm-icon-btn` (`.is-small`) | Round 34px (26px): play, close, link out |
| Legend | `.wm-legend` (`.is-stacked`) + `.wm-swatch` (`.is-line`) | 8px dots, 14px line for tracks |
| Readout | `.wm-readout` | Swatch, big number, label; rule above |
| Hint | `.wm-hint` | "Space or scroll to continue" |
| Tooltip | `.wm-tip` | Title, then place in small caps |
| Slider / timeline | `.wm-range`, `.wm-timeline` | 1px track, 11px outlined thumb that fills on hover |
| Checkbox | `.wm-check` | 13px, fills with a dark tick |
| Field / select | `.wm-field` | Underline only; the placeholder is the label |

Card anatomy, top to bottom: photo, label (place or kicker), title, stat and note,
body, legend, then a footer with the source on the left and the action on the right.

## The globe

- **Always on screen, in one of two states:**
  - **Full**: d3 orthographic, radius 0.42 of the shorter side; on desktop centred
    at 70% of the width, behind the page, with the text column fading from `--wm-bg`.
  - **Corner**: while a big image is shown, the globe minimises to a round lens in the
    top-right corner, **centred on the image's top-right corner** (`--wm-z-mini`, above
    the image): radius clamp(80px, 8.7vw, 125px), 3vw from the right, below the top bar
    (`WM.miniView(W, H)`). It may show the whole sphere or zoom toward the
    story's place inside the lens (Idai uses 2.8–4.2×). It flies between the two
    states over about 0.9s, and back when the image goes.
- **The white lines are always visible**: lat/lon grid and the circular edge, in both
  states. Full: grid 15% white at 0.5px, edge 60% at 1px (raised from 7% / 35% on 5 Oct).
  Corner: grid 30% white at 0.5px, edge 75% at 1px, so the small lens still reads as a
  globe. Never dark lines.
- Shaded relief by default. The Idai story uses flat land on purpose, for speed.
- Graticule every 10°, 0.5px, `--wm-grat`. Rim 1px, `--wm-rim`.
- **Rotation**: store real `[lon, lat]`; `WM.rotateFor()` negates it for d3, once.
- **Density grids** (stations, Argo, seals): additive squares, density as
  brightness: `WM.gridSize(scale)`, `WM.gridAlpha(n, max)` (power .85, floor .13, gain 7).
- **Dot layers**: radius grows with the fourth root of zoom, `WM.dotRadius(scale, dot)`.
- **Markers** (stories, places): ring, hover fill, selected solid with a halo;
  `WM.drawMarker()`; hit radius 14px.
- **Grid sizes: land 0.5°, ocean 1°, on every page** (decided 5 Oct; `scripts/regrid_layers.py`).
  Not yet applied on the live site, the stories or the country profile (see the handover).
- **Motion**: camera moves ease in and out (`WM.ease`) along the great circle between the two
  centres, over 0.5 to 1.2s depending on distance and zoom; layers fade over 0.6s; idle drift
  4°/s until the first touch. Respect reduced motion (everything instant).
- **Slide changes** (5 Oct): a slide with a **new title** fades the whole text block out
  (0.25s), swaps every part at once, and fades it back in (0.35s) as the camera settles; a slide
  that keeps its title (a continuation) fades only the parts that change (0.18s), and the rest
  never moves. Tested by `tests/transitions.test.js`.

## Words

- **Numbers**: commas for thousands (132,501), tabular figures in readouts,
  "about" or "around" for rounded values, en dash for ranges (2018–2023),
  units written out once (km², °, US$).
- **Dates**: 16 Jul 2024; a year alone where that is all the source gives.
- **Sources**: one line, "Publisher, date"; papers as "Author et al., *Journal*
  vol:page (year)". Every card has one.
- **Illustrative**: say so in the label or key itself, every time.
- **Titles**: sentence case. Keys and labels say what a thing is, plainly.

## Audit: what each page changes to align (4 Oct 2026)

| Page | Change |
|---|---|
| All pages | Globe grid and edge → 15% / 60% white (every page draws them fainter or dark today). |
| Main site | **Seal photo is an unframed 132px square**, already tinted: it becomes an instrument card (`.wm-instrument`), framed. Stations, satellites and Argo get instrument cards the first time they appear (photos to come from the author). Panel surface `#0A0E15` → `--wm-raised`. Extra greys `#C3CBD4` `#7C8794` `#6B7684` `#9FB3C8` → the four text greys. Root 17px → 16px. Toggle outline .3 → `--wm-outline`. Floodwater `#2E6FA3` and model-added `#4FC3F7` → decide with `--wm-flood`. FEMA dots `#FFFFFF` → `--wm-text`. |
| Country profile | **Rain gauges use Argo blue `#45B0CE`** → `--wm-gauge` green. Root 15px → 16px. Labels 9.5/10/10.5px → `.wm-label`. |
| Idai | **Photos are full-bleed backgrounds** → framed 4:3 side images (`.wm-figure.is-side`) with credits. **Globe lines are dark** (grid `#1F2A37`, edge `#242E3A` outside the lens) → white per the globe rules; the corner lens (radius 125, top right) already matches. Warm greys `#C9C6BF` (×9) `#A9AFB7` `#56606C` → text greys. Orange `#F29A3A` → storm `--wm-c2`. Map labels already match. Flat globe stays. |
| History | Slider thumb filled white → `.wm-range` (outlined, fills on hover). Readouts already match `.wm-readout`. |
| Stories | Card photo has no frame → `.wm-photo` (white frame). Next is a pill (999px) → `.wm-btn`. Close button → `.wm-icon-btn.is-small`. Legend dots 7px → `.wm-swatch` 8px. |
| Rain gauges | Globe present, unframed and full-bleed ✓. Its greens are now the system's (`--wm-gauge-*`) ✓. Its graticule `#161F2A` → the new white grid. |

### Open colour conflicts

- Greens and teals: seals `#6FD8B4`, damage `#5BC8A8`, status ok `#3FB6A8`, and now rain
  gauges `#3FD98A` (5 Oct). Gauges are on land, seals at sea, and none of them share a
  screen today; keep it that way, or move damage and status ok off green.
- Three flood blues on the main site and Idai (`#2E6FA3`, `#4FC3F7`, `#7DB4D1`).
  The system picks `#7DB4D1` for flood extent; the main site's Limpopo layers are
  a decision for the author.

## Using it in a page

1. In the template: `<body class="wm">`, `<style>/*__WM_CSS__*/ …</style>`,
   `<script>/*__WM_JS__*/</script>` before the page's own script.
2. In the build script: `from inline import inline` (see `inline.py`), then
   `page = inline(page)`.
3. Style with tokens (`var(--wm-…)`) and `wm-*` classes; draw with `WM.*`.
   Add a colour only by adding a token here first, with its one meaning.
