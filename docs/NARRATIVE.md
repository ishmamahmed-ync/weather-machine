# The Gaps in the Weather Machine: narrative so far

*Snapshot of 5 October 2026. Everything built so far, in text: the argument, every scene of the main piece, the five prototypes, the datasets behind them, every number with its source, and what is still open. Scene text and story text are copied from the source files, not retyped.*

Legend for the notes: ✅ checked against data or a source · ⚠️ no source recorded yet · ❗ differs, flagged or needs a decision.

## Contents

1. The argument
2. The main piece, scene by scene
3. The prototypes (five)
4. Datasets
5. Corrections already made
6. Literature
7. Open questions

## 1. The argument

**Title:** The Gaps in the Weather Machine. **Subtitle:** Who can see the storm coming, and who can't.

**Thesis.** The planet's observing apparatus (weather stations, satellites, ocean floats) is unevenly distributed. The gap has consequences measurable in lives. The shortfall is now less about instruments than about what countries share and what we choose to spend on.

**The data-sharing argument, as it now stands.** Sharing daily climate data was never required. Most countries donated their history to the global archive once, and the archive decays as those donations age (Menne et al. 2012). GBON (2021) is the first actual obligation, and compliance sits at 9% of required surface stations in least developed countries and small island states. Africa's radiosonde reports to global models fell about 50% between 2015 and 2020, a genuine decline in transmission.

**What the piece must not say.** "We are not measuring less, we are sharing less" was written and withdrawn: it fitted the shape of the data but not the explanation (Notes). A gap in the archive is not a gap in instruments: Somalia's zero means no data reaches NOAA, not that Somalia owns no thermometers.

**Framing device discussed, not built:** the AMOC. The RAPID array has measured the Atlantic overturning since 2004; McCarthy et al. (*GRL* 2025) find the trend won't reach unfamiliar signal-to-noise until the 2040s. Use as opening frame and closing statistic only, and keep claims on detection, not collapse.

**Arc.** 1 The machine → 2 Rich and poor views → 3 The cost → 4 What works → 5 Creative responses → 6 Money and purpose.

## 2. The main piece, scene by scene

Live at https://ishmamahmed-ync.github.io/weather-machine/ · source `site-src/template.html` (`SCENES`). **29 scenes**. Story mode scrolls through them; Explore mode lets the reader drag, zoom and toggle 24 layers.

### Act 1 · The machine

*How humanity learned to watch the weather, and the three instruments the piece follows.*

#### Scene 0 · The Gaps in the Weather Machine

> Who can see the storm coming, and who can't
> For most of history we could only guess at the weather. We prayed, consulted oracles and made calendars. None of it worked.

*centred 40°W, 12°N, zoom 0.86 · narration, no card*


#### Scene 1 · Weather stations

> Since the 1800s
> Then we started to measure.

*Globe: weather stations · centred 10°E, 45°N, zoom 1.05 · narration, no card*

- ✅ Weather stations layer: GHCN-Daily, 132,501 stations (NOAA NCEI, downloaded 19 Sep 2026).

#### Scene 2 · Satellites

> Since 1960
> They watch from above, but cannot measure the air two metres off the ground, where crops grow and people live.

*Globe: satellite shell (illustrative), weather stations (faint) · centred 30°E, 12°N, zoom 0.68 · narration, no card*

- ⚠️ The satellite shell's dots are illustrative positions (caveat removed from screen 28 Sep; see NOTES.md).
- Real counts now exist: WMO OSCAR/Space, 2 weather satellites working in 1960, 26 in 1990, 47 in 2025; all Earth-observing 3 / 43 / 439 (history prototype).

#### Scene 3 · Argo floats

> 3,375,214
> ocean profiles from 20,530 floats, since 1999
> Floats drift through the oceans measuring temperature and salinity.

*Globe: Argo floats, weather stations (faint) · centred 150°W, 0°N, zoom 0.88 · card*

- ✅ 3,375,214 profiles, 20,530 floats: Argo GDAC index, downloaded 23 Sep 2026.
- ⚠️ "since 1999": the Argo programme began in 1999, but the index holds profiles from 1997.

#### Scene 4 · An uneven machine

> Coverage is not shared equally
> We built a machine to watch the weather.
> But not all places have the same view of the storm.

*Globe: weather stations, Argo floats (faint) · centred 20°E, 10°N, zoom 0.9 · large pull quote*


### Act 2 · Rich and poor views

*The same machine sees some places far better than others; AI widens the gap.*

#### Scene 5 · The United States

> 76,708
> weather stations, 59% of all on Earth
> So many they merge into a solid surface. Most are new: 51,229 are volunteer rain gauges put up since 1998.

*Globe: weather stations · centred 98°W, 39°N, zoom 1.8 · card*

- ✅ 76,708 contiguous-US stations; 59% (59.3%) of all; 51,229 CoCoRaHS volunteer gauges since 1998 (corrected from 53,167). Checked 28 Sep.
- ❗ "So many they merge into a solid surface" depends on the 0.25° grid. At the proposed 1° land grid this stops being true; at 0.5° it mostly holds.

#### Scene 6 · Africa

> 2,166
> weather stations across the continent
> Same layer, one turn east. Africa's stations are old, with a median record of 68 years against 8 in the US. The network is shrinking, not growing.

*Globe: weather stations · centred 20°E, 2°N, zoom 1.6 · card*

- ❗ 2,166 stations: not reproducible from a country list (2,119 with island territories). Median record 68 yr in the copy, 69 recomputed; US median 8 ✅. Record how "Africa" was defined.
- ✅ "The network is shrinking": defensible only as the archive (Menne et al. 2012). Stations stop *reporting to the archive*; see Notes.

#### Scene 7 · Where data is rich

> AI fills the gaps
> Drag the handle. Trained on FEMA's flood maps, a model found 11 million people and 4.1 million buildings in flood zones no official map had recorded.

*before/after wipe (US flood maps) · centred 96°W, 38°N, zoom 2.0 · narration, no card*

- ✅ 11 million people (11.04 M, +69%) and 4.1 million buildings (4.12 M, +81%): Wu, Zhang & Stouffs 2026, *Nature Communications* 17:5983.
- ❗ The US flood dots are sampled from a blurred density of AlphaGeo screenshots: **illustrative**. CLAUDE.md requires the word on screen; it was removed 28 Sep.

#### Scene 8 · Where data is poor

> It can't
> Mozambique has no national flood map, so the handle doesn't move. AI makes the best-measured places better measured.

*Globe: weather stations · before/after wipe · centred 35°E, 18°S, zoom 2.45 · narration, no card*

- ⚠️ "Mozambique has no national flood map": no source recorded.

### Act 3 · The cost

*What happens to a place that can't see the weather coming.*

#### Scene 9 · The cost

> Two storms, two outcomes
> So what happens to a place that can't see the weather coming?

*Globe: weather stations (faint) · centred 14°E, 8°N, zoom 0.92 · large pull quote*


#### Scene 10 · Hurricane Michael

> Florida, 2018 · 125 knots
> Tracked for days, warned, evacuated. 74 people died.

*Globe: Hurricane Michael track, all storm tracks 2006–2026 (faint), weather stations · centred 86°W, 29°N, zoom 3.0 · narration, no card*

- ✅ 125 knots, both storms: IBTrACS `storms.csv`.
- ⚠️ 74 deaths: no source recorded (NHC's report splits US direct and indirect deaths; 74 likely includes Central America).

#### Scene 11 · Typhoon Haiyan

> Philippines, 2013 · 125 knots
> 6,352 people died. Another 1,071 were never found.
> Measured in money, Michael was the bigger disaster: $25.5 billion against $2.98 billion.

*Globe: Typhoon Haiyan track, all storm tracks 2006–2026 (faint) · centred 125°E, 11°N, zoom 3.0 · narration, no card*

- ⚠️ 6,352 deaths, 1,071 missing; US$25.5 bn (Michael) vs US$2.98 bn (Haiyan): no source recorded.

#### Scene 12 · The warning gap

> 636 vs 37
> weather radars: US and EU vs Africa
> Roughly the same population. 24 hours of warning cuts disaster damage by about 30%, but you need instruments to give it.

*Globe: weather stations · centred 24°E, 4°N, zoom 1.05 · card*

- ✅ 636 radars (US and EU, 1.1 bn people) vs 37 (Africa, 1.2 bn): Otto 2023, *Yale Environment 360*.
- ⚠️ "24 hours of warning cuts disaster damage by about 30%": no source recorded (usually Global Commission on Adaptation 2019).

#### Scene 13 · Mozambique

> 19
> weather stations for 34 million people
> Offshore, the Mozambique Channel gets a third of the global average of Argo profiles. Upstream, most of the water that floods the Limpopo flows past gauges Mozambique doesn't own.

*Globe: weather stations, Argo floats, Argo coldspots · centred 35°E, 18°S, zoom 2.6 · card*

- ✅ 19 stations (16 active, 14 with 30+ years): GHCN-Daily, checked 28 Sep.
- ⚠️ 34 million people: no source recorded.
- ✅ "A third of the global average" Argo density: rechecked 4 Oct, 0.35× (35–45°E, 26–11°S).
- ⚠️ Upstream Limpopo gauges "Mozambique doesn't own": no source recorded.

#### Scene 14 · Xai-Xai

> The lower Limpopo, before and after
> Drag the handle. 55% of the built-up area in this frame ends up underwater.

*before/after wipe (Lower Limpopo imagery) · centred 33.44°E, 24.87°S, zoom 52 · narration, no card*

- ⚠️ "55% of the built-up area in this frame ends up underwater": method not recorded. Imagery georeferenced to ~1 km (Notes).

#### Scene 15 · Who dies

> Every flood recorded since 2016
> Yellow is people affected, red people killed. Africa has 27% of the deaths. Europe has 1.5%.

*Globe: flood: people affected, flood: deaths · centred 30°E, 14°N, zoom 0.86 · card*

- ✅ Africa 27.0% of flood deaths, Europe 1.5%: EM-DAT floods 2016–2026, 1,680 events. Damage inverts it (Europe 20.2%, Africa 2.9%).
- Only 12% of events have EM-DAT's own coordinates; 46% are placed at country centroids (caveat removed from screen).

#### Scene 16 · Getting worse

> −50%
> African weather balloon reports, 2015 to 2020
> The poorest countries and small island states have 9% of the surface stations the WMO says they need, and 13% of the upper-air ones.

*Globe: weather stations · centred 22°E, 0°N, zoom 1.2 · card*

- ✅ −50% African radiosonde reports 2015–2020: SOFF. 9% surface / 13% upper-air of required stations in LDCs and SIDS: WMO GBON Baseline 2023.

### Act 4 · What works

*Early warning saves lives, and coverage is slowly growing.*

#### Scene 17 · Early warning works

> António Guterres, UN Secretary-General, 2025
> “Disaster-related mortality is at least six times lower in countries with good early-warning systems in place.”

*Globe: weather stations (faint) · centred 14°E, 12°N, zoom 0.88 · large pull quote*

- ✅ Guterres, remarks to the Early Warnings for All high-level event, 22 Oct 2025.

#### Scene 18 · Early warning, 2022

> 85
> countries with a multi-hazard system
> Fewer than half the world's countries.

*Globe: early warning 2022 · centred 14°E, 10°N, zoom 0.9 · card*

- ✅ 85 countries: Sendai Framework Monitor, Target G-1, fetched 28 Sep 2026 ("as of" rule).
- ❗ The *Global Status of MHEWS* report says 95 for 2022. Quote each number with its own source; never mix (Notes).

#### Scene 19 · Early warning, 2025

> 105
> countries, orange added since 2022
> The map is filling in, but slowly.

*Globe: early warning 2025, early warning 2022 · centred 14°E, 10°N, zoom 0.9 · card*

- ✅ 105 countries (report says 119). Same rule as above. China, India, Germany and Spain have never filed G-1, so they show as having none.

#### Scene 20 · Sharing

> Required since 2021
> All 193 WMO members must now share basic weather observations. And scientists are finding cheaper ways to collect the data.

*Globe: weather stations · centred 20°E, 5°S, zoom 1.3 · narration, no card*

- ✅ GBON (2021) is the first actual obligation to share; all 193 WMO members adopted it.

### Act 5 · Creative responses

*Scientists already measure the ocean with animals; the limits of clever fixes.*

#### Scene 21 · Seals

> 74%
> of ocean profiles south of 65°S
> Floats get trapped under sea ice. Elephant seals carrying sensors dive under it anyway. Nobody planned this network.

*Globe: seal profiles, Argo floats (faint) · photo: instrumented seal · centred 30°E, 70°S, zoom 1.0 · card*

- ❗ 74% of profiles south of 65°S: recomputed 4 Oct as 75.7% (151,967 seal vs 48,821 Argo). The seal download is 61% of MEOP, so the true share is likely higher.
- MEOP-CTD, downloaded 23 Sep 2026; cite Roquet et al. 2014, Treasure et al. 2017.

#### Scene 22 · Sharks

> 40%
> lower surface temperature forecast error, at best
> 29 sharks carrying depth and temperature tags logged more than 8,200 ocean profiles in the Northwest Atlantic. Fed into an operational forecast model in a proof-of-concept test, they cut surface temperature error by up to 40%. The gains were largest over the continental shelf and slope, water that conventional instruments under-sample.
> McDonnell, Kirtman, Braun & Hammerschlag, “Improved seasonal climate forecasting using shark-borne sensor data in a dynamic ocean”, npj Climate and Atmospheric Science 9:147 (2026).

*Globe: shark sightings (NW Atlantic), Argo floats (faint), seal profiles (faint) · centred 68°W, 34°N, zoom 1.3 · card*

- ✅ McDonnell, Kirtman, Braun & Hammerschlag 2026, *npj Clim Atmos Sci* 9:147. The map shows OBIS shark **sightings**, not the 29 tagged sharks.

#### Scene 23 · We already track animals

> 315
> marine species tracked around the world, none carrying sensors
> Whales, turtles, seabirds and sharks, followed for conservation. The tags report where the animal is, and nothing about the water around it.

*Globe: tracked animals, seal profiles (faint), shark sightings (NW Atlantic), Argo floats (faint) · centred 0°E, 6°N, zoom 0.86 · card*

- ✅ 315 species, 12,735 cells of 1°: OBIS-SEAMAP, downloaded 23 Sep 2026. Location only, no environmental data.

#### Scene 24 · Can we do the same for Mozambique?

> The Mozambique Channel is an Argo coldspot
> Floats sample it at a third of the global average, and no seal has been tagged there. But leatherback and loggerhead turtles already migrate through it. Add a sensor and the same tag closes an ocean data gap.

*Globe: Argo coldspots, turtles, Argo floats (faint), weather stations (faint) · centred 32°E, 14°S, zoom 1.35 · card*

- ❗ This is the project's own proposal. Published support now found: March et al. 2020, *Global Change Biology* 26:586–596 (Argo coldspots 18.6% of the ocean; 183 species could fill them). Consider citing it here.
- ✅ Zero seal cells in the Channel; 28 loggerhead and 5 leatherback cells inside it (Notes).

#### Scene 25 · The limits

> Clever fixes are cheap
> But animals can't measure rainfall over Chókwè, or give a district 30 years of records to size a drain. The boring things still have to be paid for.

*Globe: weather stations · centred 20°E, 5°N, zoom 1.1 · narration, no card*


### Act 6 · Money and purpose

*The cost of the fix against what we spend on computation; what we need.*

#### Scene 26 · The money exists

> $2.7 trillion
> worldwide spending on AI in 2026
> The UN's plan to put every person on Earth under an early warning system costs $3.1 billion over five years: less than half a day of AI spending.

*Globe: weather stations (faint) · centred 10°E, 16°N, zoom 0.84 · card*

- ✅ US$2.7 trillion: Gartner, Sep 2026. US$3.1 bn over five years: the UN Early Warnings for All plan. "Less than half a day": corrected from "two days" (Notes).

#### Scene 27 · What computation is for

> Benjamin Bratton, Planetary Sapience
> “In its current commercial form, the primary purpose of planetary-scale computation is to measure and model individual people in order to predict their next impulse. But a more aspirational goal would be to contribute to the comprehension, composition and enforcement of a shared future that is more rich, diverse and viable.”

*Globe: weather stations (faint), Argo floats (faint), seal profiles (faint), shark sightings (NW Atlantic) (faint), tracked animals · centred 6°E, 14°N, zoom 0.82 · large pull quote*

- ✅ Bratton, *Planetary Sapience*, Noema.

#### Scene 28 · What we need

> Essential infrastructure
> Dams.
> Weather stations.
> Radiosondes.
> Seawalls.

*Globe: weather stations, Argo floats (faint), seal profiles (faint), shark sightings (NW Atlantic) (faint), turtles (faint) · centred 6°E, 14°N, zoom 0.82 · large pull quote*


## 3. The prototypes

All in `prototypes/`, styled like the main site, each one self-contained.

### 3.1 Country profile: "Pick your country and year of birth" (`country-profile/globe.html`)

The reader picks their country, year of birth and a reference country. The page totals what weather and climate disasters have cost their country in their lifetime, compares it with the reference, and shows their country on the globe with its rain-gauge coverage.

> In the N years since you were born, floods have killed X people in C, affected Y and forced people from their homes Z times.

- Four horizontal bars on one shared scale (the largest of the eight values fills the width): deaths, affected, at risk of a 1-in-100-year flood, displacements. Yours solid, reference outlined. Flood / Others toggle.
- Globe: rain gauges and weather stations reporting in 2025–26; bar: gauges shared vs the WMO threshold (one per 575 km²).
- Data: EM-DAT 2000–2025 (deaths, affected); IDMC GIDD 2008–2025 (displacements, which are movements, not people); Rentschler et al. 2022 *Nat Commun* 13:3527 (people exposed to a 1-in-100-year flood, 1.81 bn total, matches the paper); GHCN-Daily (gauges shared with the archive, not all gauges operated: Belgium shows 0); WMO-No. 168 (threshold, a simplification).
- ✅ IDMC rows reproduce 2,301 of 2,302 published country-year totals.
- Open: a GBON threshold for stations; EM-DAT from 1960 for whole lifetimes; per-capita rates. Rain gauges currently share Argo's blue; they move to the system's gauge green, and the dots to 0.5° cells (decided 5 Oct).

### 3.2 Idai: a scroll story of Mozambique's 2019 cyclone season (`idai/idai.html`)

Eight full-screen slides; one globe that flies from the corner into Mozambique's maps and back. Text is the author's (`Idai_text.rtf`).

**Slide 1.** Mozambique, 2019 / Idai / Mozambique is one of the least developed countries in the world, and one of the most exposed to climate change.

**Slide 2.** More than 60% of its people live in low-lying coastal areas.

**Slide 3.** One season, three storms / 21 January 2019: Tropical Storm Desmond makes landfall, causing severe flooding. / 51 days later: Idai, a Category 4 cyclone. / 42 days after that: Cyclone Kenneth, also Category 4. / Mozambique had never been hit by so many tropical cyclones in a single season. Climate change was no longer intangible.

**Slide 4.** 14 March 2019 / Cyclone Idai made landfall near the port city of Beira. It was the deadliest natural disaster in southern Africa in nearly two decades. / Blue: land that flooded between 13 and 20 March, seen by radar. The plain between the Pungwe and Buzi rivers became an inland sea.

**Slide 5.** Before and after / Drag the handle: the same plain on 24 February and on 21 March. / False colour: water is dark blue, vegetation green, cloud cyan. Each pixel is 250 m.

**Slide 6.** Idai in numbers / 1.85 million people affected / 603 deaths, the official toll / 122,700 houses destroyed / 111,200 houses partially destroyed / 77 health facilities severely damaged / 400,000 displaced people in shelters, most with poor access to basic services / Map: in Beira alone, satellite analysts graded 16,333 damaged buildings.

**Slide 7.** Beyond people / 124,498 birds / 10,305 sheep and goats / 5,428 cows / 3,191 pigs / were killed: about US$3.1 million in losses.

**Slide 8.** In the energy sector / 1,345 km of transmission lines / 10,216 km of distribution lines / 3,990 transformers / 30 substations / were damaged.

- Sources: storm tracks IBTrACS v04 ✅ (categories match Saffir-Simpson for each wind); flood extent UNOSAT Sentinel-1, 13–20 Mar 2019 ✅ (area within 0.4%); before/after NASA MODIS via GIBS ✅ (public domain); Beira damage Copernicus EMS EMSR348 ✅ (16,333 graded buildings, checked against Copernicus's table).
- ⚠️ Impact figures (1.85 million, 603, houses, clinics, 400,000, livestock, energy): the author's text, not independently verified; likely the Government of Mozambique PDNA. Cite before publishing.
- ❗ "Category 4" for Idai and Kenneth: IBTrACS (10-min winds) peaks at Category 3; Category 4 is JTWC's 1-minute rating. The track colours show Cat 3. Pick one convention.
- ❗ "51 days later": 21 Jan to 14 Mar is 52 days. 603 deaths is Mozambique only (1,000+ across Mozambique, Zimbabwe, Malawi).
- ❗ Photo credits are blank; the photos look like agency images. Clear licences before the repo is public.

### 3.3 A century of watching (`history/history.html`)

One scene in three chapters. Each plays at 1.5 seconds per decade, then waits for space or scroll. All layers stay at full strength.

| Chapter | Years | What appears |
|---|---|---|
| 1 · On the ground: Weather stations | 1900–1960 | Stations whose daily records reached the global archive, decade by decade (0.5° cells) |
| 2 · From orbit: Satellites | 1960–1990 | Every weather and Earth-observation satellite in WMO OSCAR, real counts; positions random |
| 3 · In the ocean: Argo floats | 1990–2025 | 1° ocean cells lit from first to last profile |

| Year | Stations with data in the decade | Satellites working (all OSCAR / weather only) | Argo 1° cells lit |
|---|---|---|---|
| 1900 | 13,635 | – / – | – |
| 1960 | 43,722 | 3 / 2 | – |
| 1970 | 45,462 | 21 / 15 | – |
| 1990 | 40,792 | 43 / 26 | – |
| 2000 | 51,450 | 88 / 28 | 1,270 |
| 2010 | 65,288 | 153 / 33 | 31,626 |
| 2020 | 56,928 (2020s) | 322 / 39 | 33,417 |
| 2025 | 56,928 (2020s) | 439 / 47 | 29,403 |

- ❗ The dip from the 1970s (45,462) to the 1990s (40,792) is the archive, not stations closing (Menne et al. 2012). The on-screen fine print says so; keep it.
- Ocean measurements before Argo (ships, buoys, XBTs) are not shown, and the page says so.
- Satellites: OSCAR export 4 Oct 2026, 1,052 rows → 858 that flew (871 spacecraft). Weather-only subset cross-checked against CelesTrak (~46 vs 45 working today).
- Panel copy for chapters 2 and 3 is placeholder.

### 3.4 Stories of resilience (`stories/stories.html`)

**Title:** Those least responsible for climate change are coping, and showing resilience  
**Subtitle:** Stories about how citizen scientists, researchers, and people on the frontline, are …

One scene: the globe on the right with a circle per story; the page opens on the first story and **Next** steps through them. Animal stories fade in their map layers. Descriptions were written from each source article on 4 Oct 2026.

**Sensing with animals**

- **Elephant seals measure the ocean where floats can't go** (Southern Ocean). Argo floats can't surface through sea ice to report, but elephant seals carrying sensor tags dive beneath it. In the data used here, about three-quarters of ocean temperature profiles south of 65°S come from seals: a network nobody planned. *MEOP-CTD database; Argo, 2026-09-23.* Map: Seal-borne ocean profiles (MEOP), Argo float profiles. <https://www.meop.net/database/meop-databases/meop-ctd-database.html>
- **Sharks carrying sensors sharpen ocean forecasts** (Northwest Atlantic, Gulf Stream). 29 blue and shortfin mako sharks tagged with depth and temperature sensors logged more than 8,200 ocean profiles in the Northwest Atlantic. Fed into a forecast model, they cut surface temperature error by up to 40%, most over the continental shelf and slope. *McDonnell et al., npj Climate and Atmospheric Science 9:147, 2026.* Map: Shark sightings in the study region (OBIS), not the tagged sharks, Argo float profiles. <https://doi.org/10.1038/s41612-026-01394-9>
- **Tagged animals could carry sensors into the gaps Argo misses** (Global study; the Caribbean is one of the gaps it names). Mapping over 1.5 million Argo profiles, a study found gaps covering 18.6% of the ocean: polar seas, shallow shelves, marginal seas and upwelling zones. Set against 183 marine species and more than 3,000 tracked animals, it argues seals, turtles and sharks could fill them. *March et al., Global Change Biology 26:586, 2020.* Map: Argo coldspots, as calculated for this project (the paper's own map differs), Tracked marine animals, 315 species (OBIS-SEAMAP). <https://doi.org/10.1111/gcb.14902>

**Flood and cyclone early warning (the spreadsheet, plus Bangladesh added 5 Oct)**

- **Improved flood detectors save lives and property** (Karonga District, Malawi). River sensors and an automated alert system on the North Rukuru River now warn families in Karonga District up to 72 hours before a flood, up from less than six hours. The district has had 21 major floods in five decades. *UNICEF Malawi, 2024-07-16.* <https://www.unicef.org/malawi/stories/improved-flood-detectors-save-lives-and-property>
- **Cyclone Amphan: In Bangladesh, Preparedness Paid Off** (Coastal Bangladesh). As Cyclone Amphan approached in May 2020, more than 70,000 Cyclone Preparedness Programme volunteers spread warnings by megaphone, flag and door to door, and over two million people reached shelters. In 1970, the Bhola cyclone killed at least 300,000. *American Red Cross, 2020-05-29.* <https://www.redcross.org/about-us/news-and-events/news/2020/cyclone-amphan-in-bangladesh-preparedness-paid-off.html>
- **Community cooperation across Nepal-India border saves lives during flood** (Ratu River, Nepal–India border). Volunteers on both sides of the border watch a low-cost sensor on the Ratu River and phone warnings downstream when the water rises. The system cost about US$3,500 and gives around 64,000 people one to three hours' warning each year. *ICIMOD, 2023-02-27.* <https://www.icimod.org/article/community-cooperation-across-nepal-india-border-saves-lives-during-flood/>
- **Protecting lives in flood-prone Cambodia** (Cambodia). People in Need built an early warning system that sends flood alerts straight to mobile phones, triggered automatically by a river sensor called Tepmachcha. It covers more than 200,000 households, after floods in 2013 affected 1.7 million people. *UNICEF Office of Innovation, 2017-07-06.* <https://www.unicef.org/innovation/stories/protecting-lives-flood-prone-cambodia>
- **Putting resilience at the centre of development** (Saptari District, Nepal). In Saptari, river early warning systems and community emergency centres, backed by UNICEF, let families prepare and move before floods arrive, as part of a programme that puts children at the centre of disaster planning. *UNICEF Nepal, 2020-02-25.* <https://www.unicef.org/nepal/stories/putting-resilience-centre-development>
- **Bridging the monitoring gap: UNESCO and WRA launch IoT to enhance flood early warnings** (Tana River Basin, Kenya). In March 2026, UNESCO and Kenya's Water Resources Authority installed internet-connected sensors in the Tana River Basin that report river levels, rainfall and soil moisture in real time, giving downstream communities earlier notice of floods. *UNESCO, 2026-04-14.* <https://www.unesco.org/en/articles/bridging-monitoring-gap-unesco-and-wra-launch-iot-enhance-flood-early-warnings>
- **TAHMO: Leveraging commercial microwave link data to develop flood early warning systems** (Aboabo, Ghana). In Aboabo, TAHMO measures rainfall from the way it weakens the signal between mobile-phone masts, adds low-cost river sensors and residents' smartphone videos of the river, and sends flood alerts by SMS, voice call and WhatsApp. *GSMA, 2025-12-03.* <https://www.gsma.com/solutions-and-impact/connectivity-for-good/mobile-for-development/gsma_resources/tahmo-leveraging-commercial-microwave-link-data-to-develop-flood-early-warning-systems/>
- **Community-Based Flood Early Warning System — India** (Lakhimpur and Dhemaji, Assam, India). In Assam's Lakhimpur and Dhemaji districts, a riverbank sensor radios a signal when the water reaches a critical level, and the warning is passed by mobile phone to 45 vulnerable communities downstream. It won a UNFCCC Momentum for Change award in 2014. *UNFCCC; ICIMOD, 2014-12-10.* <https://unfccc.int/climate-action/un-global-climate-action-awards/winning-projects/activity-database/community-based-flood-early-warning-system-india>

**Stories of hope (from the text file)**

- **Deep learning completes US flood hazard maps** (United States). Trained on America's official flood maps, a deep-learning model filled in the areas they leave unmapped and found 11 million more people living in flood zones, 69% above the official count. It can only learn where a national map exists. *Wu, Zhang & Stouffs, Nature Communications 17:5983, 2026.* Map: FEMA flood zones (illustrative dots), Added by the model (illustrative dots). <https://doi.org/10.1038/s41467-026-74336-x>
- **South Australia increases its net electricity generation from renewables from 1% in 2007 to over 75% in 2025** (South Australia). Wind and solar are now the state's main sources of electricity: wind supplied around 45% and solar over 32% in 2024/25, with about half of homes carrying rooftop panels. The state aims for 100% net renewable electricity by 2027. *Government of South Australia, 2026.* <https://www.energymining.sa.gov.au/industry/hydrogen-and-renewable-energy/leading-the-green-economy>
- **Wind and solar overtake fossil power in the EU for the first time in 2025** (European Union). In 2025, wind and solar generated 30% of the EU's electricity, ahead of fossil fuels at 29%, for the first time. Solar alone reached a record 13%, and coal fell to a historic low of 9.2%. *Ember, 2026-01-22.* <https://ember-energy.org/latest-updates/wind-and-solar-generated-more-power-than-fossil-fuels-in-the-eu-for-the-first-time-in-2025/>
- **Endangered North Atlantic right whales had their most calves in nearly two decades** (Calving grounds, southeastern United States). Aerial surveys off the southeastern United States counted 23 right whale calves in the 2026 calving season, the most since 2009, and sighted 129 individual whales across more than 1,400 flight hours. *NOAA Fisheries, 2026-04-30.* <https://www.fisheries.noaa.gov/feature-story/numbers-2026-north-atlantic-right-whale-calving-season>
- **Global mangrove forests rebound, offering signs for climate and coastal resilience** (Global study, Tulane University, New Orleans). A four-decade satellite study led by Tulane University found that mangrove gains have outpaced losses for the past 16 years, leaving a net decline of only about 1% since the 1980s. *Tulane University, 2026-06-04.* <https://news.tulane.edu/pr/global-mangrove-forests-rebound-offering-hopeful-sign-climate-and-coastal-resilience>
- **First puffling sighting in three decades gives hope for Dorset's dwindling puffin colony** (Dancing Ledge, Dorset, UK). Volunteers monitoring Dancing Ledge on the Purbeck coast saw a young puffin leave its cliff crevice, the first in about 30 years, at a colony now down to around three breeding pairs. *National Trust, 2026-07-22.* <https://www.nationaltrust.org.uk/services/media/2026/july/first-puffling-sighting-in-three-decades-gives-hope-for-dorsets-dwindling-puffin-colony>
- **China's Yangtze River shows dramatic recovery after four-year fishing ban** (Yangtze River, China). After China banned commercial fishing across the Yangtze basin in 2021, a study in Science found the mass of fish in survey samples more than doubled between 2018 and 2023, and finless porpoises rose from 445 in 2017 to 595 in 2022. *Live Science, 2026-02-12.* <https://www.livescience.com/planet-earth/rivers-oceans/china-banned-fishing-in-its-biggest-river-and-species-are-starting-to-recover>
- **From waste to wealth: How fly farming is building climate resilience and creating jobs** (Mukuru, Nairobi, Kenya). In Mukuru, an informal settlement in Nairobi, black soldier fly larvae turn food waste into animal feed and fertiliser, creating jobs, cutting feed costs by about 30% and, by clearing waste, reducing flooding. *Global Center on Adaptation, 2025-03-30.* <https://gca.org/from-waste-to-wealth-how-fly-farming-is-building-climate-resilience-and-creating-jobs/>
- **Guyana's forests drive a new era of low-carbon development** (Guyana). Guyana has kept more than 99% of its forest, about 18 million hectares, and turned it into income through carbon markets, earning 33.47 million carbon credits for 2022 under its low-carbon development strategy. *CVF-V20, 2026-05-28.* <https://cvfv20.org/guyanas-forests-drive-a-new-era-of-low-carbon-development/>
- **Adapting to climate change in Panama** (Santa María watershed, Panama). Farming communities, including in the Santa María watershed, are adopting better water management, agroforestry and ecosystem restoration to cope with heat, shifting rainfall and water scarcity. The project supports more than 114,000 people and has restored 600 hectares. *Adaptation Fund, 2026-07-16.* <https://www.adaptation-fund.org/stories-of-resilience-adapting-to-climate-change-in-panama/>
- **Early warning systems are saving lives in Central Asia** (Central Asia). Early warning systems that pair local knowledge with remote sensors are being installed to warn mountain communities of glacial lake outburst floods. A UNESCO project in Central Asia aims to protect about 100,000 people, alongside a larger programme in Pakistan. *Climate Home News, 2026-03-24.* <https://www.climatechangenews.com/2026/03/24/early-warning-systems-are-saving-lives-in-central-asia/>
- **How climate adaptation in Vanuatu is protecting forests, oceans and communities** (Espiritu Santo, Vanuatu). On Espiritu Santo, the Indigenous-led Santo Sunset Environment Network trained 89 climate rangers and set up community conservation areas across 42 villages to restore forests, secure food and prepare for cyclones. *UNDP, 2025-06-12.* <https://www.adaptation-undp.org/how-climate-adaptation-vanuatu-protecting-forests-oceans-and-communities>

- ❗ Fit with the title: the flood stories fit "least responsible … coping" and the lack-of-data brief; several hope stories (South Australia, the EU, US right whales, Dorset puffins, the Tulane mangrove study) and the three animal stories are about wealthy places or programmes.
- ❗ Yangtze headline says "four-year fishing ban"; the source describes a 10-year ban from 2021.
- The subtitle is unfinished ("are …"). Photos are placeholders; licences not cleared.

### 3.5 Rain gauge density: map and explorer (`rain-gauges/rain-gauge-sections.html`)

Two scenes meant to follow the story's last scene. Kept for the final build; integration instructions in `INTEGRATION.md`. **Rain (precipitation) gauges, not flood or stream gauges.**

1. **Rain gauge density.** The earth alone: one dot per 0.5° land cell, coloured by gauges per 1,000 km² in eight classes (no gauge, under 0.1, up to 10 or more). Each 1° source cell is drawn as four dots with the same value, so this adds no information beyond 1°.
2. **Rain gauge density against the WMO minimum.** Terrain tabs (Plains, Hilly, Mountains, Coastal, Islands, Urban, Polar/Arid); one square per 1° cell, plotted by continent against that terrain's WMO minimum, linked to the globe. Green meets the minimum, faint green falls short, grey has no gauge.

- ✅ Su et al. 2026, *Nature* 652:119–125, Fig. 2c, rebuilt from the published data (Zenodo 10.5281/zenodo.18364510, CC BY 4.0). 15,263 land cells; 8,303 with a gauge. Plains: 2,320 of 4,130 cells have a gauge; WMO minimum 1.74 per 1,000 km². Africa's Plains average 0.086, below the minimum, with 63% of cells empty.
- Decided 5 Oct: the design system adopts this page's greens (`--wm-gauge`).

## 4. Datasets

Full detail, links and licences in `docs/SOURCES.md`; problems in `docs/NOTES.md`.

| Dataset | Who | Downloaded | Size used | What it shows | Used in |
|---|---|---|---|---|---|
| GHCN-Daily station list + inventory | NOAA NCEI | 19 Sep 2026 | 132,501 stations; 7,966 with a WMO id | Stations whose data reached the archive, with first/last year | Main (most scenes), country profile, history |
| ISD station history | NOAA | 19 Sep 2026 | 28,095 stations | Second station archive; disagrees with GHCN (Belgium 1 vs 52) | Comparison only |
| Argo global profile index | Argo GDAC (Coriolis) | 23 Sep 2026 | 3,375,214 profiles, 20,530 floats, 36,674 1° cells | Ocean temperature/salinity profiles | Main, history, stories |
| Argo coldspots | this project | – | 26 patches, 48.1 million km² | Under-sampled ocean (script not in repo) | Main scene 13 and 24, stories |
| MEOP-CTD | MEOP consortium | 23 Sep 2026 | 545,596 profiles; 108 of 233 deployments (61%) | Seal-borne ocean profiles | Main scene 21, stories |
| OBIS-SEAMAP | Duke MGEL | 23 Sep 2026 | 315 species, 12,735 1° cells; 16 shark species | Where tracked animals go (location only) | Main scenes 22–24, stories |
| Shark ocean-sensing programmes | hand-compiled from 3 papers | – | 3 features | Where sharks have carried ocean sensors | Reference |
| IBTrACS v04r01 | NOAA NCEI | 23 Sep 2026 | 1,813 storms 2006–2026, 26,606 nodes | Storm tracks and intensity | Main scenes 10–11, Idai |
| EM-DAT floods | CRED, UCLouvain | 18 Sep 2026 | 1,680 events 2016–2026 | Flood deaths, affected, damage | Main scene 15 |
| EM-DAT weather/climate disasters | CRED | 3 Oct 2026 | 2000–2025 | Lifetime disaster totals | Country profile |
| IDMC GIDD events | IDMC | Oct 2026 | 2008–2025, one file per year | Internal displacements | Country profile |
| Rentschler et al. 2022 SI | Nat Commun 13:3527 | Oct 2026 | 188 countries, 1.81 bn people | Exposure to 1-in-100-year floods | Country profile |
| Sendai Framework Monitor, Target G-1 | UNDRR | 28 Sep 2026 | 195 countries; 85 (2022), 105 (2025) | Countries reporting a multi-hazard early warning system | Main scenes 18–19 |
| WMO OSCAR/Space | WMO | 4 Oct 2026 | 1,052 rows → 871 spacecraft | Earth-observing satellites, launch to end of life | History |
| UNOSAT flood extent | UNOSAT via HDX | Oct 2026 | Sentinel-1, 13–20 Mar 2019 | Idai flood extent | Idai |
| Copernicus EMS EMSR348 | European Union | Oct 2026 | 16,333 graded buildings | Beira building damage | Idai |
| NASA MODIS (GIBS) | NASA | Oct 2026 | 24 Feb and 21 Mar 2019 | Before/after imagery | Idai |
| Wu, Zhang & Stouffs 2026 flood layer | via AlphaGeo screenshots | – | illustrative dots | AI-completed US flood maps | Main scene 7 |
| Lower Limpopo before/after | satellite composites | – | georeferenced to ~1 km | Xai-Xai flooding | Main scene 14 |
| Su et al. 2026, Fig. 2c data | Nature 652:119; Zenodo, CC BY 4.0 | Oct 2026 | 15,263 1° land cells, 8,303 gauged | Rain gauges per 1,000 km² against the WMO minimum by terrain | Rain gauge prototype |
| Natural Earth | public domain | 28 Sep 2026 | 1:50m and 1:110m | Land and country shapes | All |

**Evaluated and rejected:** GDIS (no geometry for Kiribati, the Maldives or the Marshall Islands, exactly the states the argument concerns); `ish-history.csv` (a deprecation notice, not data).

**Structural limits to state somewhere:** EM-DAT records only events that cross an administrative threshold. GHCN-Daily counts stations whose data reaches NOAA, not national infrastructure. Flood deaths and damage have different coverage (1,243 vs 406 events). The MEOP download is 61% of all seal profiles.

## 5. Corrections already made

- "We are not measuring less, we are sharing less": withdrawn. Daily data sharing was never obligatory (Menne et al. 2012).
- GDIS codebook's 11,801 disasters is a transposition of 11,081.
- "20% of Mozambique's GDP" for the 2000 floods: unsupportable; use growth falling from 7% to 1.5% and losses of about $600 million.
- "Damage is roughly equal everywhere": false. Damage is more concentrated than deaths (Gini 0.870 vs 0.836); Europe 20.2% of damage and 1.5% of deaths, Africa 2.9% and 27.0%.
- No "40% more counties" in the flood-model paper: it is 11.04 M people (+69%) and 4.12 M buildings (+81%).
- AI-spending comparison: "less than two days" → "less than half a day" (US$7.4 bn a day).
- Volunteer gauges 53,167 → 51,229. Early warning "of any kind" → multi-hazard (G-1).
- Flood-model attribution: Wu, Zhang & Stouffs (Tsinghua / NUS / Singapore-ETH), not AlphaGeo, which built a website presenting it.
- Processing bugs fixed: the North Atlantic dropped as `NA`; 2° binning inverted the US–Africa finding; extracted dots reproduced map labels as holes; a MEOP join fanned out; telemetry cells at 180° drawn 1° too far north (found 4 Oct, fixed in the regrid sample).
- On-screen caveats removed 28 Sep at the author's request (illustrative dots, IBTrACS, EM-DAT geocoding, G-1 "no report"). They still apply; a /data or /notes page is the place to restore them.

## 6. Literature

- Menne, M.J. et al. (2012). An Overview of the GHCN-Daily Database. *J. Atmos. Oceanic Technol.* 29, 897–910. **The key source on sharing.**
- Applequist, S., Durre, I. & Vose, R. (2024). GHCN Monthly Precipitation v4. *Scientific Data* 11, 633.
- Lawrimore, J.H. et al. (2011). GHCN monthly mean temperature v3. *JGR Atmospheres* 116, D19121.
- WMO GBON Baseline 2023, SOFF Sixth Steering Committee; SOFF, un-soff.org/operations.
- Wu, A.N., Zhang, Y. & Stouffs, R. (2026). Deep learning completes US flood hazard maps. *Nature Communications* 17, 5983.
- McDonnell, Kirtman, Braun & Hammerschlag (2026). Improved seasonal climate forecasting using shark-borne sensor data in a dynamic ocean. *npj Clim Atmos Sci* 9:147.
- March, D., Boehme, L., Tintoré, J., Vélez-Belchi, P.J. & Godley, B.J. (2020). Towards the integration of animal-borne instruments into global ocean observing systems. *Global Change Biology* 26(2), 586–596. **Found 4 Oct; supports scenes 23–24.**
- Pagniello et al. 2024, *Sci Rep* 14:13837; Holland et al. 2022, *Anim Biotelem* 10:34 (shark-borne sensing).
- Rentschler, J., Salhab, M. & Jafino, B. (2022). *Nature Communications* 13, 3527 (flood exposure).
- Otto, F. (2023). Without Warning. *Yale Environment 360*, 31 Oct (radars).
- McCarthy, G.D. et al. (2025). Signal and Noise in the AMOC at 26°N. *GRL* (framing device, not built).
- Jaffrés 2019, *Computers & Geosciences* 122; WMO-No. 1244 (Resolution 40); Viscusi & Masterman (VSL); Gartner Sep 2026 (AI spending); Guterres, 22 Oct 2025; Bratton, *Planetary Sapience*; Patzek 2026 (preprint, not peer reviewed).

## 7. Open questions

**Sources to add (on screen now, no source recorded):** Michael 74 deaths; Haiyan 6,352 dead and 1,071 missing; damage US$25.5 bn vs US$2.98 bn; "24 hours of warning cuts damage by about 30%"; Mozambique 34 million people; "no national flood map"; upstream Limpopo gauges; Xai-Xai 55% of built-up area; the Idai impact figures.

**Numbers that differ from a recheck:** seals 74% vs 75.7%; Africa 2,166 stations vs 2,119 (define Africa); Africa median record 68 vs 69 years; Sendai 85/105 vs the reports' 95/119 (quote each with its source).

**Decisions:**
- Restore caveats (illustrative dots, "as recorded in IBTrACS", geocoding, G-1) on a /data or /notes page, or on screen.
- Scene 24 (Mozambique turtles) is the project's own proposal: cite March et al. 2020, or reframe as a proposal.
- Satellite scene 2: switch the illustrative shell to the real OSCAR counts?
- Grid standard: decided 5 Oct, land 0.5° and ocean 1° on every page (re-check the US scene's "solid surface" at 0.5°).
- AMOC as opening frame and closing statistic.
- Idai: Category 3 or 4; 51 or 52 days; Mozambique-only deaths; photo licences.
- Stories: which of the 21 fit the title; Yangtze headline; finish the subtitle.
- Decided 5 Oct: the design system is authoritative; the final page is one combined file. Next steps: HANDOVER.md section 8.
