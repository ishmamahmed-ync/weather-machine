# Prototypes

Experiments alongside *The Gaps in the Weather Machine*, kept off the live site.
All are dark, minimal and styled to match the main site; all are built by a
Python script (standard library only) from a template plus data, and all open
straight from a file.

| Folder | What | Open | Rebuild |
|---|---|---|---|
| `country-profile/` | "Pick your country and year of birth": lifetime disaster toll vs a reference country, four horizontal bars on one scale, globe + WMO rain-gauge bar | `globe.html` | `python3 build_globe.py` |
| `idai/` | Scroll story of Cyclone Idai (2019): one globe that zooms from the corner into Mozambique maps (tracks, floods, before/after, Beira damage) and back | `idai.html` | `python3 build_idai.py` |
| `history/` | One scene, 1900 to the present in three chapters (stations 1900–60, satellites 1960–90, Argo 1990–2025); each plays at 1.5 s per decade, then waits for space or scroll | `history.html` | `python3 build_history.py` |
| `stories/` | One scene: stories of resilience as clickable circles on the globe; a card with photo placeholder, title, description and link opens under the title | `stories.html` | `python3 build_stories.py` |
| `rain-gauges/` | Two scenes for the end of the story: rain gauge density on the globe (0.5° dots), then an explorer of 1° cells against the WMO minimum by terrain. Kept for the final build, not yet integrated; see `INTEGRATION.md` | `rain-gauge-sections.html` | none (self-contained) |

Run each build **from inside its folder**. Scripts find the repo root as
`Path(__file__).parent.parent.parent`, and expect:

```
site-src/template.html               d3-array + d3-geo, copied into each page
site-src/layers/relief.webp.b64      relief texture (country-profile globe only)
data/processed/ghcnd-stations-with-age.csv, storm_nodes.csv
data/raw/ne_50m_admin_0_countries.geojson
data/raw/emdat-2026-10-03.xlsx, idmc-gidd-displacements-2008-2025.xlsx, idmc-events/
data/raw/idai/                       UNOSAT, Copernicus EMS, NASA images
```

Shared code: `country-profile/build_globe.py` provides `simplify()` and
`simplify_ring()`; `idai/build_idai.py` imports them. `country-profile/xlsx.py`
and `idai/shp.py` are standard-library readers for .xlsx and shapefiles (this
machine has no pandas, openpyxl, GDAL or shapely).

Each folder's README lists its sources, the checks the build runs, and the open
editorial items.
