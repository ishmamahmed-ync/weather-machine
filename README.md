# The Gaps in the Weather Machine

A data visualisation about who can measure their own climate, and who cannot.

Harvard GSD, Master in Design Engineering — studio project.

**Live site:** https://ishmamahmed-ync.github.io/weather-machine/

---

## What this argues

The planet is covered in instruments, but not evenly. The United States holds
59% of the world's weather stations. Twenty-one countries have none with a
usable long-term record. Where measurement is thin, forecasts are worse,
adaptation is harder to design, and the same storm kills far more people.

The piece follows that gap from a global view down to a single river basin in
Mozambique, then to the places where the gap has been closed by accident —
by instrumented seals and sharks — and ends on the observation that the
shortfall is no longer mainly about instruments. It is about what countries
share, and what we choose to spend on.

---

## Repository layout

```
data/raw/          source downloads (not committed — see docs/SOURCES.md)
data/processed/    cleaned, joined outputs used by the site
scripts/           the Python that turns raw into processed
site/              the website (single self-contained HTML file)
drafts/            wireframe SVGs for layout work
docs/SOURCES.md    every dataset: origin, date, licence, row counts
docs/NOTES.md      data problems found and how they were handled
```

---

## Running the site

The site is one self-contained HTML file with no network dependencies. Open it
directly:

```
open index.html
```

`index.html` is **generated** — do not hand-edit it. Edit `site-src/template.html`
and rebuild:

```
python scripts/build_site.py
```

It has two views, switched from the top right:

- **Story** — a scroll-driven narrative, 29 scenes
- **Explore** — drag to rotate, scroll to zoom, toggle any of 24 data layers

Pressing `D` anywhere opens a live styling panel for tuning colours, dot sizes
and camera positions.

---

## Rebuilding the data

Requires Python 3.9 or later.

```
pip install -r requirements.txt
```

Download the raw sources into `data/raw/` (see `docs/SOURCES.md` for links),
then:

```
# weather stations: fixed-width NCEI file -> clean CSV and GeoJSON
python scripts/clean_ghcnd_stations.py data/raw/ghcnd-stations.txt data/processed

# add each station's period of record
python scripts/add_station_ages.py data/raw/ghcnd-inventory.txt \
       data/processed/ghcnd-stations-clean.csv data/processed

# tropical cyclone tracks, thinned to 12-hourly observed positions
python scripts/build_simple_tracks.py data/raw/ibtracs.ALL.list.v04r01.csv \
       data/processed --step 12 --since 2006 --min-peak-wind 34

# EM-DAT floods -> points, with geocoding provenance recorded per event
python scripts/build_flood_geojson.py data/raw/EM-DAT_Floods.xlsx \
       data/processed/emdat-floods.geojson --since 2016

# wireframe SVGs for layout work
python scripts/make_drafts.py
```

Each script prints what it kept and what it dropped, and why.

---

## A note on method

Several figures in the piece were checked against the source files rather than
taken from the literature, and a few corrections came out of that. Those are
recorded in `docs/NOTES.md`, including two cases where the published or
commonly quoted number was wrong, and one where a bug in my own processing
silently deleted an entire ocean basin.

The layers drawn over the United States in the flood-model comparison are
**illustrative** — sampled from a published density, not the underlying
county-level data. This is stated in `docs/SOURCES.md` and should be stated in
any caption that uses them.

---

## Licence

Code in `scripts/` and `site/`: MIT.

Data in `data/processed/` remains under the licence of its source. Several
sources are non-commercial or require attribution — see `docs/SOURCES.md`
before reusing anything here.
