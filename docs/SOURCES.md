# Sources

Every dataset used in this project: where it came from, when it was downloaded,
what licence it carries, and what was done to it.

Raw downloads are **not committed** — several are 50–330 MB. Links below are the
exact sources used. Everything in `data/processed/` is reproducible from them
with the scripts in `scripts/`.

---

## Weather stations

### GHCN-Daily station list and inventory
NOAA National Centers for Environmental Information.
`https://www.ncei.noaa.gov/pub/data/ghcn/daily/`
Files: `ghcnd-stations.txt`, `ghcnd-inventory.txt`, `ghcnd-countries.txt`
**Downloaded 19 September 2026.** US Government work, not subject to copyright.

The station file is **fixed-width, not delimited**, despite often being named
`.csv`. Field positions follow NCEI `readme.txt` section IV.

→ `data/processed/ghcnd-stations-with-age.csv` — **132,501 stations**, with
country and network decoded, elevation sentinels nulled, and each station's
first year, last year, record length and active flag joined from the inventory.

→ `data/processed/ghcnd-stations-wmo.geojson` — **7,966 stations** carrying a
WMO identifier, i.e. the internationally exchanged subset.

Key figures drawn from this file: 59.3% of all stations are in the United
States; 36% of 1.5° land cells contain none; 14,295 stations have both a
30-year record and current data; 21 countries have none.

### ISD station history
NOAA Integrated Surface Database.
`https://www.ncei.noaa.gov/pub/data/noaa/isd-history.csv`
**Downloaded 19 September 2026.** Snapshot's latest END date is 2025-08-28.

→ `data/processed/isd-stations-clean.csv` — **28,095 stations**. 1,566 rows
dropped for null or `(0,0)` coordinates, including 379 zero-island sentinels.

Used for the comparison showing that GHCN and ISD disagree by an order of
magnitude in opposite directions: Belgium has 1 station in GHCN and 52 in ISD;
Sweden has 1,721 and 500.

---

## Ocean

### Argo global profile index
Argo Program, Coriolis GDAC.
`https://data-argo.ifremer.fr/ar_index_global_prof.txt.gz`
**Downloaded 23 September 2026.** Cite the GDAC DOI: `10.17882/42182`.
Argo data are freely available.

→ `data/processed/argo-density-1deg.geojson` — **36,674 cells**, binned from
3,375,214 profiles across 20,530 floats. 238 rows had 0–360 longitude and were
wrapped; 289 had `-99.999 / -999.999` fill values and were dropped.

### MEOP-CTD — seal-borne profiles
Marine Mammals Exploring the Oceans Pole to Pole.
`https://www.meop.net/database/meop-databases/meop-ctd-database.html`
Access via a short form. **Downloaded 23 September 2026.**
Non-commercial use; contact the PI before any commercial use.
Cite Roquet et al. 2014 and Treasure et al. 2017.

→ `data/processed/meop-density-1deg.geojson` — **7,021 cells** from 545,596
profiles.
→ `data/processed/meop-deployments.geojson` — **233 deployments**, with an
`in_my_download` flag marking the 125 absent from the copy used here.

**Known incompleteness.** The download covers 108 of 233 deployments — every
Australian, US and Brazilian one, and none from France, Canada, the UK, Norway,
Germany, South Africa, Sweden, China, Japan, Chile or Italy. That is 469,594 of
767,182 temperature profiles, or 61%. The deployments layer records this
explicitly rather than hiding it.

---

## Storms

### IBTrACS v04r01
NOAA NCEI International Best Track Archive for Climate Stewardship.
`https://www.ncei.noaa.gov/data/international-best-track-archive-for-climate-stewardship-ibtracs/v04r01/access/csv/ibtracs.ALL.list.v04r01.csv`
**Downloaded 23 September 2026.** NOAA data, not subject to copyright.
WMO-endorsed archive.

→ `data/processed/storms.csv` — **1,813 storms**, 2006–2026, filtered to those
reaching at least 34 kt, spur tracks excluded.
→ `data/processed/storm_nodes.csv` — **26,606 nodes** at 12-hourly spacing.

Row 2 of the source is a **units row**, not data. Filtering to 12-hourly keeps
only positions flagged `O` (observed) and discards the interpolated fills. The
basin code for the North Atlantic is `NA`, which pandas reads as null by
default — see `docs/NOTES.md`.

Caveat carried into the piece: IBTrACS documentation notes that changing
operational procedures and observing systems have introduced significant
heterogeneities in the record.

---

## Disaster impacts

### EM-DAT — floods
Centre for Research on the Epidemiology of Disasters, UCLouvain.
`https://public.emdat.be/` — free for non-commercial and academic use,
registration required. **Export dated 18 September 2026.**

→ `data/processed/emdat-floods-2016-2026.geojson` — **1,680 events**, 2016–2026.

**Geocoding provenance is recorded on every feature** as `geo_precision`,
because EM-DAT supplied coordinates for only 12% of these records:

| tier | count | what it is |
|---|---|---|
| `reported` | 195 | EM-DAT's own latitude and longitude |
| `admin1` | 710 | mean centroid of the provinces EM-DAT lists, matched to Natural Earth |
| `country` | 775 | country centroid, last resort |

Any map implying a location should filter to `geo_precision <> 'country'`.

Coverage varies by field: deaths on 1,243 events, total affected on 1,528,
damage on only 406. `total_affected` excludes deaths — verified as exactly
`injured + affected + homeless` on all 1,111 rows carrying both.

### GDIS — geocoded disaster locations (evaluated, not used in the final piece)
Rosvold & Buhaug 2021, NASA SEDAC. `https://doi.org/10.7927/zz3b-8y61`
Rejected because GADM 3.6 contains no geometry for Kiribati, the Maldives or
the Marshall Islands, so those countries are absent entirely — precisely the
states the argument concerns. Recorded in `docs/NOTES.md`.

---

## Marine animal tracking

### OBIS-SEAMAP
Duke University Marine Geospatial Ecology Lab. Halpin et al. 2009.
`https://seamap.env.duke.edu/` — **Downloaded 23 September 2026.**
Licence varies by contributing dataset; permission-required datasets are
excluded from the criteria-based download route.

→ `data/processed/obis-species-by-cell.csv` — **27,291 species-cell rows**,
315 species, from 1,427,856 records in 12,735 cells of 1°.
→ `site-src/layers/globe-data.json` `turtles` — leatherback (*Dermochelys coriacea*, 435
cells) and loggerhead (*Caretta caretta*, 991 cells) filtered from
`obis-species-by-cell.csv`: 1,323 distinct cells, built by `scripts/add_turtles_layer.py`.
→ `data/processed/obis-sharks-by-cell.csv` — **311 rows**, 16 shark species.

On the globe the `sharks` layer is trimmed to the NW Atlantic (82–60°W, 24–46°N): 61 of 137 cells, by `scripts/trim_sharks_layer.py`. These are OBIS sightings in the study region, **not** the tracks of the 29 tagged sharks.

**Location only — no environmental measurements.** The `species` field in the
source is a semicolon-delimited list per cell, so record counts belong to the
cell, not to any one species.

### Shark-borne ocean sensing
`data/processed/shark-ocean-sensing-programmes.geojson` — **3 features**,
compiled by hand from the papers, not downloaded. Coordinates are approximate
region centroids.

- Pagniello et al. 2024, *Sci Rep* 14:13837 — salmon shark, Gulf of Alaska, 56 CTD profiles. `10.1038/s41598-024-63543-5`
- Holland et al. 2022, *Anim Biotelem* 10:34 — tiger shark, Oahu, 500+ temperature-depth profiles
- McDonnell, Kirtman, Braun & Hammerschlag 2026, "Improved seasonal climate forecasting using shark-borne sensor data in a dynamic ocean", *npj Clim Atmos Sci* 9:147 — 29 sharks, Northwest Atlantic, >8,200 depth–temperature profiles; retrospective forecasts up to 40% lower surface temperature error in a proof-of-concept experiment, strongest over shelf and slope. `10.1038/s41612-026-01394-9`

---

## Basemap

Natural Earth 1:110m and 1:50m land and country polygons.
`https://github.com/nvkelso/natural-earth-vector` — public domain.

---

## Imagery and figures

**Lower Limpopo before/after** — two false-colour satellite composites of the
Xai-Xai area. Georeferenced in this project by locating the Chokwe, Chibuto,
Macia and Xai-Xai labels and fitting to their known coordinates; the horizontal
and vertical scales agreed to 0.48%, confirming a north-up Web Mercator frame.
Derived bounds: 32.936°E–33.951°E, 25.352°S–24.380°S.

**US flood exposure dots** — extracted from two screenshots of AlphaGeo's
FloodMapper interface, which presents Wu, Zhang & Stouffs (2026). The dots in
the final site are **sampled from a blurred density**, not the underlying
locations, because the originals contained label-shaped holes where map
type occluded the data. **Illustrative only.** The underlying AI-generated
flood layer is published openly at `10.6084/m9.figshare.29163797` and should be
used instead if precision matters.

---

## Early warning systems

### Sendai Framework Monitor, Target G-1
UNDRR, Sendai Framework Monitor public analytics API.
`https://sendaimonitor.undrr.org/analytics/global-target/16/7`
**Fetched 28 September 2026** by `scripts/fetch_sendai_g1.py`. UNDRR terms of use; cite
the Sendai Framework Monitor.

G-1 is a 0–1 composite score of MHEWS capability, one value per country per
reporting year. Countries report irregularly: 54 filed for 2022 and 44 for 2025.
A country counts as **reported having MHEWS as of year Y** if its most recent
G-1 value for any year up to and including Y is above 0.

→ `data/processed/sendai-g1-mhews.csv` — 195 countries, G-1 score by year 2005–2026.
→ `data/processed/sendai-g1-mhews-2022.csv` — **85 countries** (6 more reported a score of 0).
→ `data/processed/sendai-g1-mhews-2025.csv` — **105 countries** (8 more reported 0).
On the globe, each country is filled with dots on the 1° grid (x.5 centres)
inside its Natural Earth boundary; countries too small to hold a grid centre
(10 in 2022, 16 in 2025, mostly small island states) get one dot at the
Monitor's centroid. 2022: 8,993 dots; 2025: 10,681. Built by `scripts/add_mhews_layers.py`.

### Natural Earth admin-0 countries, 1:50m
`https://github.com/nvkelso/natural-earth-vector` → `geojson/ne_50m_admin_0_countries.geojson`
**Downloaded 28 September 2026**, 3.1 MB, 242 features. Public domain. Kept in
`data/raw/`. Matched on `ADM0_A3`, since `ISO_A3_EH` is shared by two Australian
territories. Admin-0 shapes include overseas territories (France includes
French Guiana and Réunion).
**These counts are lower than the published reports' figures** (see NOTES.md).

---

## Literature cited in the piece

- Wu, A.N., Zhang, Y. & Stouffs, R. (2026). Deep learning completes US flood hazard maps. *Nature Communications* **17**, 5983. `10.1038/s41467-026-74336-x`
- Applequist, S., Durre, I. & Vose, R. (2024). GHCN Monthly Precipitation v4. *Scientific Data* **11**, 633. `10.1038/s41597-024-03457-z` — the post-1970 decline is discontinued contributions, not station closures.
- Menne, M.J. et al. (2012). An Overview of the GHCN-Daily Database. *J. Atmos. Oceanic Technol.* **29**, 897–910. — **the key source on sharing**: no formal mechanism or requirement to share daily data via the GTS, no central repository, transmission optional, and most countries provided historical records only once.
- Lawrimore, J.H. et al. (2011). GHCN monthly mean temperature v3. *JGR Atmospheres* **116**, D19121. — station counts peak near 6,000 in the 1960s–70s.
- WMO GBON Baseline 2023, SOFF Sixth Steering Committee — LDCs and SIDS at 9% of required surface stations, 13% of upper-air.
- SOFF, `un-soff.org/operations` — African radiosonde observations to global models down ~50% between 2015 and early 2020.
- Jaffrés, J.B.D. (2019). GHCN-Daily: a treasure trove awaiting discovery. *Computers & Geosciences* **122**, 35–44.
- WMO (2019). *Origin, Impact and Aftermath of WMO Resolution 40*. WMO-No. 1244.
- McCarthy, G.D. et al. (2025). Signal and Noise in the AMOC at 26°N. *Geophysical Research Letters*. `10.1029/2025GL115055`
- Viscusi, W.K. & Masterman, C. — value of a statistical life by income band.
- Otto, F. (2023). Without Warning. *Yale Environment 360*, 31 October — 636 radars in the US and EU for 1.1 bn people, 37 in Africa for 1.2 bn.
- Gartner (September 2026) — worldwide AI spending to reach $2.7 trillion in 2026, up 49.5%.
- Guterres, A. (22 October 2025), remarks to the Early Warnings for All high-level event.
- Bratton, B. *Planetary Sapience*, Noema.
- Patzek, T.W. (2026). *Thermal Power and Climate Change*, preprint — not peer reviewed.
