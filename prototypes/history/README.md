# A Century of Watching (draft)

One scene in three chapters: weather stations 1900–1960, satellites
1960–1990, Argo floats 1990–2025. Each chapter plays at 1.5 s per decade, then
waits for space or scroll. Every layer stays at full strength throughout.

```
python3 extract_satellites.py     # OSCAR export -> satellites.csv, satellites_per_year.csv
python3 build_history.py          # -> history.html
```

Settings (chapter years, copy, `SECONDS_PER_DECADE`) are at the top of the
script in `template.html`.

## In the final page (5 Oct 2026)

No slide of its own (the author's call): the history fills in the **weather-machine slides** (2 to 5) on the
story's one shared globe. Each press of Space adds an instrument's card, and the era timeline pinned under the
cards plays that instrument's era: stations 1900–1960, satellites 1960–1990, Argo 1990–today (at 1.5 s per
decade), while the globe fills in year by year with this prototype's data. The fourth slide (rain gauges)
holds at Today; the gauge cells fill in as a reveal only (that data has no dates).

| File | What it is |
|---|---|
| `history-layers.js` | The drawing, year by year: stations, Argo, satellites. **Shared** by `history.html` (inlined by `build_history.py`) and the final page, so both draw exactly the same |
| `story-plugin.js` | The final page's plugin: the three layers, and `setYear()` / `run()`, which the story's era timeline drives. (Its own panel and chapter playback are kept for a standalone slide, unused now.) |
| `history-data.json` | Written by `build_history.py`; `scripts/build_all.py` embeds it. Rebuild history first |

Test: `node tests/history.test.js http://localhost:8766/weather-machine.html` (each slide's era, its cards,
the timeline never moving, the text clear of it).

## Sources

| Layer | Source | Notes |
|---|---|---|
| Weather stations | `data/processed/ghcnd-stations-with-age.csv` (GHCN-Daily) | 132,437 of 132,501 stations (64 have no dates). 0.5° cells; per decade, stations whose record overlaps it. Record spans in the archive, not installation dates. |
| Satellites | WMO OSCAR/Space, https://space.oscar.wmo.int/satellites, full export downloaded 4 Oct 2026 → `data/raw/oscar-space-satellites-2026-10-04.xlsx` (1,052 rows) | **Number is real, positions are random.** All meteorological and Earth-observation satellites that flew: 871, launch to end of life. |
| Argo floats | `data/processed/argo-density-1deg.geojson` | 1° cells lit from first to last profile year. |

### Which satellites are counted

All of OSCAR (meteorological and Earth observation together), minus what never
operated. `extract_satellites.py`:

- 1,052 rows → 858 satellites that flew → **871 spacecraft**, because four rows stand
  for several (CYGNSS 8, RapidEye 5, TWINS 2, Van Allen Probes 2).
- Dropped: 164 planned, concept or not yet launched (incl. Metop-SG-B1, Nov 2026);
  20 lost at launch.
- 10 rows are one spacecraft moved to a new post ("Meteosat-7 (IODC)", "GOES-10
  (S-America)") and are folded into that satellite, so it isn't counted twice.
- Presumably inactive / Unclear (35) with an open end date ("≥2019") end in that
  year: OSCAR confirms them only that far. Back-up and Stand-by count as operating.
- OSCAR's scope includes a few space-weather and solar missions (ACE, SOHO, Parker
  Solar Probe); they are counted, as OSCAR lists them.

In operation, all: 1960 **3**, 1970 21, 1980 29, 1990 **43**, 2000 88, 2010 153,
2020 322, 2025 **439**; 457 today.

A `weather` column keeps the narrower definition (41 weather programmes: GOES,
Meteosat, NOAA/POES, Metop, Himawari, FengYun, Meteor, INSAT …; list in the script):
1960 2, 1990 26, 2025 47.

### Checks

- TIROS-1 launch 1 Apr 1960, end 17 Jun 1960 in OSCAR; GOES-16 launch 19 Nov 2016;
  Meteosat-1 23 Nov 1977; Metop-A 2006–2021; NOAA-18 and NOAA-19 ended Jun and Aug 2025.
- Weather subset, independent: CelesTrak's "weather" group (satellites in orbit, 4 Oct 2026) lists
  76; removing what this definition excludes (8 CYGNSS, ~20 Tianmu radio-occultation,
  2 Sentinel-3) leaves ~46, against 45 here. Membership differs at the edges:
  CelesTrak still lists some FengYun-3 and Meteor satellites OSCAR marks inactive.

## Open items

- The satellite chapter is still sparse: 43 satellites by 1990 even counting all of
  OSCAR. The growth is after 2000 (88 → 439), which falls in the Argo chapter.
- Present is 2025; 2026 is a partial year in the Argo data.
- Panel copy for chapters 2 and 3 is placeholder.
