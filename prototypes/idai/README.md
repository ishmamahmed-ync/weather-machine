# Idai: a scroll story of Mozambique's 2019 cyclone season

An NYT-style visual article, separate from the main site and styled like it.
Eight full-screen slides; text on the left, a photo or a map behind every slide
(no blank or dark slides; the author's rule). Scroll, or press space / arrow
keys; Home/End jump. Open `idai.html`; it needs `photos/` and `maps/` beside it.

## In the final page (5 Oct 2026)

Slides 10 to 15 of the final page, on the story's **one shared globe** (no globe of its own), following the
narrative's brackets: the photo slides put the globe in the corner lens, centred on the photo's top-right
corner (the story's corner lens, `WM.miniView`); the map slides fly it in and draw this prototype's layers once
it arrives. Maps kept simple (the author): one map per slide, only the labels the story needs; the damage map
is central Beira only.

| File | What it is |
|---|---|
| `story-plugin.js` | The final page's plugin: `idai_base` (flat land at map scale), `idai_tracks` (calendar order, timed with the day counts), `idai_flood`, `idai_damage`, `idai_labels` (and the schematic arrow) |
| `idai-data.json` | Written by `build_idai.py` (now with `center`, Beira Center's buildings); `scripts/build_all.py` embeds it, minus what the page does not draw, with the photos and the MODIS pair |

Test: `node tests/idai.test.js http://localhost:8766/weather-machine.html`.

## The one-globe idea

There is **one globe** for the whole piece, an orthographic d3 projection drawn
on a single canvas. Each slide is a *view* `{tx, ty, scale, center, clip}`:

- **Photo slides:** the globe is a round lens in the top-right corner (or large on the opening slide).
- **Map slides:** the globe flies to the middle and **zooms in**: Mozambique Channel, then the Pungwe-Buzi plain, then Beira's streets. Only after it arrives does it fade in that slide's layers and labels.
- **Going back to a photo:** it zooms out to the corner.

Flights tween screen position and lens radius linearly, scale geometrically,
and the centre along the great circle. Labels are HTML, placed from the same
projection, hidden while flying.

**Look:** the main site's **flat** globe (the author asked to drop the relief so it
loads faster): ocean `#0B121B`, land `#161D26`, coastline `#242E3A`, Mozambique a
shade lighter, a lat/lon grid that tightens with zoom (10°, 2°, 0.5°, 0.02°),
text cards like the main site's (`rgba(5,8,14,.84)`, 1px `#222C38`, 3px radius).
**No drop shadows.**

## The slides (edit them in `SLIDES` at the top of `template.html`)

| # | Text (from the author's `Idai_text.rtf`) | Behind it |
|---|---|---|
| 1 | Title; least developed, exposed to climate change | large globe over the flooded-house photo (dimmed) |
| 2 | More than 60% live in low-lying coastal areas | flooded-house photo, globe in the corner |
| 3 | Desmond 21 Jan, Idai 51 days later, Kenneth 42 days after; never so many | **map**: the three tracks animate in turn (Desmond, Kenneth, Idai, ~6 s) in Saffir-Simpson colours |
| 4 | Landfall near Beira, 14 March; deadliest in two decades | **map**: UNOSAT flood extent + Idai's path |
| 5 | Before / after | **map**: NASA MODIS pair with a drag slider, pinned to its corners on the globe |
| 6 | Idai in numbers (1.85 M affected, 603 deaths, houses, clinics, shelters) | **map**: Beira building damage |
| 7 | Beyond people: livestock | drowned-cow photo |
| 8 | Energy sector damage | pylons-in-floodwater photo |

Track colours are the main site's storm ramp (`LAYERS.storms.ramp`):
TS `#F5E06A`, Cat 1 `#F6C243`, 2 `#F09A3E`, 3 `#E8703E`, 4 `#DC4340`, 5 `#B81D2C`;
depression = grey dashed. Categories in the data were checked against wind speed.

## Data and how each was verified

| Layer | Source | Verification |
|---|---|---|
| Storm tracks | IBTrACS v04 via `data/processed/storm_nodes.csv` (12-hourly) | Desmond 6, Idai 23, Kenneth 11 fixes. Every category matches Saffir-Simpson for its wind (90 kt = Cat 2, 105 kt = Cat 3). Idai peak 105 kt; last fix 32.2°E is in Zimbabwe (west of Mutare). Landfall time 23:30 UTC 14 March from Copernicus EMS. |
| Flood extent | UNOSAT, Sentinel-1, 13/14/19/20 March 2019 (HDX `TC20190312MOZ_SHP.zip`) | Geometry area matches the file's `Area_m2` within 0.4% (19 Mar Sofala 2,853 vs 2,844 km²). All features "New Water / Water Increase" (no permanent water). Confidence "To Be Evaluated": rapid mapping, said on the map. Packed for 32.4-35.9°E, 21.2-18.4°S, wider than the frame, so no false edge when zoomed; 99.7% of area kept after simplification. |
| Before / after | NASA GIBS `MODIS_Aqua_CorrectedReflectance_Bands721`, 24 Feb & 21 Mar 2019, EPSG:4326, bbox 33.9-35.2°E, 20.6-19.0°S | Same pair NASA Earth Observatory used. Beira's coordinates fall on the city. Public domain. Cloud shows cyan. 250 m pixels. |
| Building damage | Copernicus EMS EMSR348 grading, Beira NW/West/Center/East; Pléiades 0.5 m (26 Mar 2019) vs WorldView (Sep 2018) | 16,333 graded: 613 destroyed, 7,698 damaged, 8,022 possibly damaged. Beira Center checked against Copernicus's own PDF table: 33 = 33, 2,968 = 2,968, 5,704 vs 5,705. Only damaged buildings exist in the data. Streets, water and coastline from the same packages. |
| Town labels | OpenStreetMap Nominatim, **settlement** points (queried 2026-10-04) | Dondo and Nhamatanda re-queried: the first answers were district centroids. |
| Impact figures | the author's text | **Not independently verified**; add the citation (likely the Government of Mozambique PDNA). |

## Build

```
python3 build_idai.py      # from this folder; ~15 s, standard library only
```

Prints each layer's counts and the area check. It imports `simplify`/`simplify_ring`
from `../country-profile/build_globe.py` and reads `shp.py` (a stdlib shapefile reader).
d3-array + d3-geo are copied from the main site's `site-src/template.html`.
Raw inputs live in `data/raw/idai/` (gitignored).

Performance: each map's layers are drawn once into an offscreen canvas on arrival
and faded as an image (the flood layer is ~24,000 polygons); a full redraw ~12 ms.
Page ~2.7 MB, mostly flood polygons.

## Open before publishing

1. **"Category 4"** in slide 3's text contradicts the track colours: IBTrACS (regional
   centre, 10-min winds) peaks at Cat 3 for both Idai and Kenneth; Cat 4 is JTWC's 1-min
   rating. Pick one convention; the main site already says "as recorded in IBTrACS".
2. **"51 days later"**: 21 Jan → 14 Mar is 52 days.
3. **Photo credits**: `credit:""` per slide; these look like agency photos. Clear the licence
   before the repo goes public (the photos are in `photos/` and would be committed).
4. **603 deaths** is Mozambique only; Idai killed 1,000+ across Mozambique, Zimbabwe, Malawi.
5. Animation order is Desmond → Kenneth → Idai (author's choice); calendar order is D → I → K.
