# Country profile: "Pick your country and year of birth"

A one-screen companion to *The Gaps in the Weather Machine*, kept separate from
the main site. The reader picks their country, year of birth and a reference
country. The page totals what weather and climate disasters have cost their
country in their lifetime, compares it with the reference, and puts their
country on the globe next to its rain-gauge coverage.

Open `globe.html` directly; it is one self-contained file (~1.15 MB) that works
from `file://`. `globe.html#BGD,DEU` opens Bangladesh against Germany.

## What is on the screen

Laid out from the author's Figma frame, styled like the main site (dark,
minimal, thin white lines).

| Area | Content |
|---|---|
| Left, top | Title "Pick your country and year of birth"; a sentence: *"In the N years since you were born, floods have killed X people in C, affected Y and forced people from their homes Z times."* |
| Left, under the sentence | Four horizontal bars, left-aligned with the title: **Deaths** (red), **Affected** (yellow), **At risk of a 1-in-100-year flood** (blue), **Displacements** (violet). Solid bar = your country, white-outlined bar = reference. **One scale for all eight bars**: the largest value (any measure, either country) fills the width, stated under the bars. Anything above zero is at least 2px. (Circles until 5 Oct 2026.) |
| Right, top | Three underlined fields (no boxes): *Your country*, *Year of birth* (four digits, 1920 to this year), *Reference country*. The placeholder is the label. |
| Right | **Flood / Others** toggle (styled like the main site's Story/Explore buttons). |
| Right | The main site's shaded-relief globe, rotated to centre the chosen country (white outline). Blue dots = active rain gauges, amber = active weather stations. |
| Far right | Vertical bar: rain gauges **shared** vs the **WMO threshold**, amber below / teal above. |

**Others mode** ("all disasters") shows the flood part of your bar solid and the
other disasters faded, with the flood share as a percentage.

**Empty state:** fields show only placeholders; the four bars show dashes; the bars and the
gauge meter appear once a country and year are chosen. The reference silently defaults to the
US until the reader picks one (the key under the bars names it).

## Data, per country (ISO 3166 alpha-3)

| Measure | Source | Window | Notes |
|---|---|---|---|
| Deaths, total affected | EM-DAT public export (`data/raw/emdat-2026-10-03.xlsx`) | 2000-2025, yearly | Export holds **weather/climate disasters only** (no earthquakes/volcanoes). "Floods" = types *Flood* + *Glacial lake outburst flood*. |
| Displaced | IDMC GIDD event export, one file per year (`data/raw/idmc-events/2008..2025.xlsx`) | 2008-2025, yearly | Internal displacements = **movements, not people**. Flood = hazard type *Flood*. |
| At risk | Rentschler, Salhab & Jafino 2022, *Nat Commun* 13:3527, Suppl. Table 1 → `flood_exposure.csv` | 2020 | People exposed to a 1-in-100-year flood (>15 cm). Not age- or toggle-dependent. |
| Rain gauges | GHCN-Daily (`data/processed/ghcnd-stations-with-age.csv`) | reporting in 2025-26 | **Shared with the global archive**, not every gauge operated (Belgium shows 0). |
| WMO threshold | WMO-No. 168, Table I.2.6 | — | One gauge per **575 km²** (interior plains). Mountains 250, coasts 900: a simplification. |
| Area / shapes | Natural Earth 1:50m admin-0 | — | Matched on `ADM0_A3` first (ISO_A3_EH is shared by two Australian territories). |

Lifetime totals start at `max(birth year, first year of data)`. For anyone born
before 2000 the sentence reads *"Since 2000, the first year on record in your
N-year life…"*; displacement before 2008 is noted in the fine print.

## Checks the builds run (and what they found)

- Bars checked in the browser (Bangladesh vs Germany, born 1990, Others mode): affected 182 million = 100%; at risk 94 million = 52%; displacements 26 million = 14%; flood part of affected 62.6% (= 63% floods). The bar track is `.btrack`: `.track` is the gauge meter's class, and reusing it squeezed the bars to 10px.

- IDMC event rows reproduce **2,301 of 2,302** published country-year totals (Ghana 2025 off by 57).
- CRI 2026: 174 countries, ranks 1-174, no gaps (used only in the older `index.html`).
- Flood exposure: 188 countries, total **1.81 billion**, matching the paper.
- Every unmatched country name is printed.
- Year of birth (changed from date of birth on 5 Oct 2026): letters are stripped; years before 1920 or after this year are rejected. Age is this year minus the birth year, so before their birthday a reader is counted one year older; the totals were already by whole calendar years. A full date saved by the earlier version is read as its year.

## Files

```
build_data.py            data.json + index.html (older 4-card version); helpers reused below
build_globe.py           globe.html (the current one-screen version)
globe-template.html      markup / styles / engine for globe.html  ← edit this
template.html            the older card version's template
xlsx.py                  stdlib .xlsx reader (no openpyxl on this machine)
extract_cri.py           CRI 2026 PDF annex -> cri2026.csv   (needs pypdf + cryptography)
extract_flood_exposure.py  Rentschler SI PDF -> flood_exposure.csv (needs pypdf)
cri2026.csv, flood_exposure.csv   committed transcriptions, so builds don't need pypdf
```

Rebuild: `python3 build_globe.py` (from this folder; ~20 s, standard library only).

`build_globe.py` also exports `simplify()` / `simplify_ring()`, the Ramer-Douglas-Peucker
line simplifier used by the Idai prototype. **Bug fixed on 2026-10-04:** plain RDP on a
closed ring collapses it (first point = last point), which had silently kept only each
country's largest outline. `simplify_ring()` splits the ring at its farthest vertex first.

## In the final page (slide 17)

`story-plugin.js` and `story-plugin.css` bring this onto the final page's shared globe as a plugin
(`scripts/build_all.py`, adapter `country_profile`); `build_globe.py` also writes `profile-data.json` for it (the
yearly series, people at risk, outlines). One step: the fields, then the slide's narration becomes the finding
("Since 2005, the year you were born, floods have killed ..."; for anyone born before 2000, "Since 2000, when
the records begin"), and four horizontal bars, one per line, on one scale: your country in its colours, the
comparison solid white at the same thickness; Flood / Others. The globe turns to the country and outlines it.
The rain-gauge half was dropped (the author, 5 Oct); `su_by_country()` is kept, unused. The standalone
`globe.html` is unchanged. Test: `tests/profile.test.js`.

## Open items

- **Decided 5 Oct**: "at risk" stays on the shared scale. The page follows the design system (authoritative) and the grid standard: the gauge and station dots move from 0.1° locations to 0.5° cells, and their legend then says "cells with a gauge".

- Weather stations have no WMO threshold of their own here; GBON's surface target (one per 200 km) could be added.
- A longer EM-DAT export (from 1960) would let the sentence cover any adult's whole life.
- Per-capita rates would make small and large countries comparable (needs population data).
- `index.html` (four cards) is the superseded first version, kept for comparison.
