# Notes

Problems found in the data, and what was done about them. Included because the
findings are only as good as the handling, and because several of these changed
what the piece could claim.

---

## Errors found in published or widely quoted figures

**The GDIS codebook reports 11,801 disasters retrieved from EM-DAT. The correct
figure is 11,081.** The codebook's own arithmetic proves it: it states 1,157
disasters had no identifiable location, and 11,081 − 9,924 = 1,157, whereas
11,801 − 9,924 = 1,877. The paper uses 11,081, and 9,924/11,081 = 89.6% matches
its stated geocoding rate. A transposition, printed twice.

**"20% of Mozambique's GDP" for the 2000 floods is not supportable.** Damage was
around $500 million against a 2000 GDP near $4.2 billion. The sourced framing is
GFDRR's: GDP growth fell from a forecast 7% to 1.5%, and USAID records losses of
about $600 million, more than double annual export earnings. The piece uses the
growth and export figures.

**"Countries stopped sharing weather data after a 1970s golden age" is not
supported.** WMO's "end of the golden age" language (WMO-No. 1244) describes
policy and diplomacy — real pressure on free exchange from the mid-1980s, a near
"data war" by the early 1990s, and the Resolution 40 compromise of 1995. It does
not describe a measured decline in stations transmitting, and connecting the two
was an inference, not a finding. See the archival explanation below.

**"Damage is roughly equal everywhere" is false.** Tested on the EM-DAT file:
damage is *more* concentrated than deaths, Gini 0.870 against 0.836. What is
true, and stronger, is the inversion — Europe holds 20.2% of flood damage and
1.5% of flood deaths; Africa holds 2.9% and 27.0%.

**There is no "40% more counties" figure in the flood-model paper.** It reports
11.04 million additional people (69% above baseline) and 4.12 million buildings
(81%). The 40% in that paper refers to metropolitan areas inadequately mapped.

---

## Bugs in my own processing

**The North Atlantic silently vanished.** The IBTrACS basin code for it is `NA`,
which pandas treats as a missing value by default. 185 Atlantic storms — Melissa,
Dorian, Irma, Maria — were loaded with a blank basin and dropped from every
per-basin count. Caught only because they appeared in a longest-lived listing
with no basin. Fixed with `keep_default_na=False`.

**Binning inverted the central finding.** At 2° cells, the United States
occupied 383 cells and Africa 411 — making Africa look *denser* when the true
station ratio is 36:1 the other way. Fixed by moving to 0.25° cells and
switching to additive compositing, so density accumulates as brightness rather
than being squeezed into dot size. The rendered ratio is now about 27:1 against
a true 36:1: compressed, but no longer reversed.

**Extracted dots reproduced map labels as holes.** Pulling flood dots out of a
screenshot faithfully reproduced "New York" and "Washington" as negative space,
because the labels had covered the dots beneath. Fixed by blurring to a density
and sampling from that, which closes the holes — at the cost of the dots no
longer being individual locations. Recorded as illustrative in `SOURCES.md`.

**A join fanned out.** Two tag codes are duplicated in the MEOP tag file, which
inflated the profile join by 1,617 rows. Fixed by de-duplicating on the key.

---

## Datasets evaluated and rejected

**GDIS.** Rejected because GADM 3.6 has no geometry for Kiribati, the Maldives
or the Marshall Islands, so no disaster in those countries is geocoded at all.
Also absent: Nauru, Cook Islands, Niue, Saint Kitts and Nevis, Aruba, Anguilla,
Bermuda, Singapore. For an argument about small island states, the dataset omits
the evidence. Wildfire is excluded from GDIS entirely, and dry mass movement has
49 records worldwide across 58 years.

**`ish-history.csv`.** A 633-byte deprecation notice, not data. The live file is
`isd-history.csv` — one letter apart.

---

## Structural limits worth stating in captions

**EM-DAT records only events crossing a threshold**: 10+ killed, or 100+
affected, or a declared state of emergency, or an international appeal. Two of
those four are institutional acts, so the database records events that crossed
an administrative line, not events that happened.

**GHCN-Daily counts stations whose data reaches NOAA.** Somalia's zero does not
mean Somalia owns no thermometers. The map measures participation in the
international observing commons, not national infrastructure. Belgium's 1
against ISD's 52 is the clearest demonstration.

**The apparent post-1970 decline is archival, and the reason is stronger than
"countries stopped sharing".** An earlier draft of this project claimed that
countries had retreated from a prior norm of sharing. That is wrong. Menne et
al. (2012), NOAA's own description of GHCN-Daily, states there has been no
formal mechanism or requirement to share daily data via the GTS, no central
repository for daily climate reports, that transmission has been treated as
optional, and that **most participating countries have provided historical daily
station records only once**. The archive is built from one-off donations that
age out — which is why nearly half of Brazil's stations have their last year in
either 1983 or 1997.

So the defensible claim is not that the commons was dismantled. It is that a
commons for daily climate data **was never built**. Sharing became obligatory
for the first time in 2021, when all 193 WMO members adopted GBON. Under its
compliance criteria, least-developed countries and small island states report 9%
of required surface stations and 13% of required upper-air stations.

One decline in *transmission* is separately documented and does hold: SOFF
reports that African radiosonde observations reaching global models fell by
roughly 50% between 2015 and early 2020, and further since.

**Damage and deaths have different coverage.** In the flood file, 1,243 events
carry deaths and only 406 carry damage. Comparing the two maps without saying so
would read a reporting gap as a finding.

---

## Sendai G-1 counts do not match the published MHEWS reports

The *Global Status of MHEWS* reports give 95 countries with MHEWS in 2022 and
119 in 2025. Rebuilding the lists from the Sendai Framework Monitor in September
2026 gives **85 as of 2022 and 105 as of 2025**. Counting any G-1 filing, even a
score of 0, gives 91 and 113, and adding countries that filed only G-2 to G-5
gives 112 and 131. None of these reproduces the published figures. The likely
causes are that the Monitor is revised as countries back-fill past years, and
that each report was a snapshot on its publication date. The reports' own
country lists could not be checked: the WMO library puts the PDF behind a
human-verification page. **Quote the report's number with the report's name,
and our number with "Sendai Framework Monitor, September 2026". Do not mix the two.**

Also worth knowing before captioning the map: the "as of" rule carries old
filings forward. The United States last filed G-1 for 2021 and Japan for 2020,
but both count in 2025. China, India, Germany and Spain have never filed G-1,
so they appear as having no MHEWS when in fact they have not reported.

---

## Checked while building scene spec 3 (28 September 2026)

**The AI-spending comparison was off by a factor of four.** The spec said $3.1 bn
is "less than two days" of AI spending, using $1.65 bn a day. $2.7 trillion over
365 days is **$7.4 bn a day**, so the five-year early warning plan is about
**10 hours** of 2026 AI spending. The scene now says "less than half a day". The
870-to-1 ratio stands, but it compares **one year** of AI spending with the
**whole five-year** plan, so the copy now says exactly that.

**Volunteer rain gauges: 51,229, not 53,167.** Counted from
`ghcnd-stations-with-age.csv`: GHCN network code `1` (CoCoRaHS), in the
contiguous US, all with a first year of 1998 or later. There are 51,468 across
all states. The 53,167 in the spec could not be reproduced from the processed
file, so the scene uses 51,229.

**Africa's 2,166 stations could not be reproduced from a country list.**
Filtering GHCN by African country names, French and British island
territories included, gives 2,119, with a median record of 69 years (the spec
has 68). The 2,166 has been in the piece since an earlier build and is kept, but
whoever wrote it should record how Africa was defined.

**Turtle cell counts differ between files.** The spec quotes leatherbacks in
508 cells and loggerheads in 1,105. `obis-species-by-cell.csv` has 435 and 991,
or 1,323 distinct cells combined. The new `turtles` layer is built from that CSV
and the scene quotes no cell count. Verified from the same files: zero MEOP seal
cells in the Mozambique Channel (32–50°E, 27–10°S), and 28 loggerhead plus 5
leatherback cells inside it.

**Checked and confirmed:** 76,708 contiguous-US stations; 59.3% US share; US
median record 8 years; Mozambique 19 stations, 16 active, 14 active with 30+
years; Michael and Haiyan both 125 kt and 204 h in `storms.csv`; 545,596 MEOP
profiles ("half a million").

**Scene 22's copy changed.** The spec said "about half the world's countries
had an early warning system of any kind" in 2022. The Sendai data is 85 of 195
(44%), and G-1 measures *multi-hazard* systems, not systems of any kind. The copy
now says "fewer than half … covers more than one hazard".

---

## On-screen caveats removed (28 September 2026)

At the author's request, the scene cards no longer carry caveat or citation
lines. These include "dots are illustrative" (US flood dots, satellite shell),
"as recorded in IBTrACS", the EM-DAT 12% geocoding note, and "no dot means no
report" (Sendai G-1). The caveats still apply and are recorded in SOURCES.md and
above. This departs from the CLAUDE.md rule that captions using the US flood
dots say "illustrative". A `/data` or `/notes` page is the natural place to
restore them.

---

## Things that are approximate

- The 65° reach used for geostationary satellite footprints is a working
  convention, not a measurement. The geometric horizon is 81.31°. The polar gap
  holds at any value.
- Four of the eight geostationary longitudes are sourced; INSAT and FengYun
  should be checked against WMO OSCAR before publication.
- The Lower Limpopo georeference carries about 1 km of residual on a 110 km
  frame, from using label positions rather than the points they name.
- Mozambique's 2000 GDP is used as approximately $4.2 billion and should be
  confirmed against World Bank series if the percentage is quoted.

---

## Checked for the final page (5 October 2026)

`scripts/check_figures.py` holds every figure on the 24 slides of the author's narrative
(v3 short), recomputes what the repo's data can recompute, and writes `docs/FIGURES.md`.

**Africa's stations: 2,119, now with a recorded definition.** The 50 African country
names in GHCN-Daily (49 states plus Western Sahara; Comoros, Djibouti, Sao Tome and
Principe, Somalia and South Sudan have no stations in the file) give 2,110. Adding six
island territories (Reunion, Mayotte, Juan de Nova, Europa and Tromelin [France]; Saint
Helena [UK]) gives **2,119**, median record 69 years. The old 2,166 could not be
reproduced under any definition tried, including the Canaries and Madeira (14 more).
The author chose 2,119 on 5 Oct.

**"76,708 stations, 59% of all on Earth" mixes two areas.** 59% (59.3%) is the whole
United States, 78,567 stations including Alaska (1,053) and Hawaii (805). The contiguous
US alone, 76,708, is **57.9%**. The live site carries the same mismatch. Either "76,708 …
58%" or "78,567 … 59%".

**Su et al. figures: quote the paper.** Author's rule, 5 Oct: on screen, rain-gauge
totals are the paper's own (221,483 gauges, 13.4% of land meeting the WMO minimum,
Europe 2.4 and Africa 0.09 per 1,000 km²). The published Fig. 2c data inside the map gives
212,996 gauges, 13.5% of cells, Europe 1.99 and Africa 0.10, because some cells were
cleaned. Only 123 excluded cells (an eighth terrain class) are documented in
`prototypes/rain-gauges/INTEGRATION.md`; the rest of the cleaning is not yet recorded. Per-cell
values in the hover and the explorer come from the data, since the paper does not publish them.

**Mozambique Channel, "a third of the global average": the method.** Argo profiles per
unit ocean area (1° cells with at least one profile, each weighted by cos latitude) in
35–45°E, 26–11°S, against the same over the whole ocean: 0.35. A plain mean of profiles
per cell gives 0.44 instead, so the method has to travel with the number.

**The US flood-map wipe had its labels swapped (live site too).** The model's additions
are drawn left of the handle, but the left label read "Official FEMA flood map" and the
right "After the model fills the gaps". Fixed in the final page's story
(`final/story/template.html`, `WIPE.us`); the live `site-src/template.html` still has it.

**Argo on the instrument card: "3,375,214 profiles from 20,530 floats", reconciled with the raw index.**
The raw GDAC index on this machine (`data/raw/ar_index_global_prof.txt.gz`, "Date of update 20260923152414")
has 3,411,164 rows. The processed density file keeps the rows that have both a date and a valid position:
that rule gives **20,530 floats** exactly, and 3,375,215 profiles, one more than the 3,375,214 summed from
`data/processed/argo-density-1deg.geojson`. The rest are 18,926 rows with no date and 288 with fill-value
positions. The one-profile difference is not explained; the card quotes the processed total.
`scripts/check_figures.py` recomputes both from the files.

**Idai on the final page (5 Oct 2026): what was simplified, and what is approximate.**
- One readable map for the damage (the author's note): **central Beira only** (Copernicus EMS EMSR348,
  23BEIRACENTER), 8,705 graded buildings: 33 destroyed, 2,968 damaged, 5,704 possibly damaged. Copernicus's own
  table gives 33, 2,968 and 5,705. The prototype's four districts (16,333 buildings) are not stitched together.
- The **river names** on the flood map are placed by towns that stand on each river (Mafambisse on the Pungwe,
  Buzi town on the Buzi). They are approximate positions, not river geometry: the page has no river data.
- The **arrow** from Zimbabwe's highlands to the coast is schematic, and its key says so.
- At city scale the land is plain: the Natural Earth outlines, simplified for the wide maps, are about 1 km off
  there, so only Copernicus's own water and coastline are drawn.

**Country profile on the final page (slide 17, 5 Oct 2026).** *Update, same day: the author dropped the slide's
rain-gauge half, so the Su et al. part below is not on the page (the code is kept in `build_globe.py`,
`su_by_country()`, unused). The slide's narration now becomes the finding once a country and year are chosen;
for anyone born before 2000 it reads "Since 2000, when the records begin (you were born in 1990)", not "Since
1990", because EM-DAT here starts in 2000. The clause about rain gauges was cut from the slide's words, and
Su et al. from its source line.*
- The gauges are now Su et al.'s (2026) 1° cells, the rain-gauge explorer's own data, instead of GHCN-Daily
  stations active in 2025-26. Per country: the gauges in its cells, and the gauges its cells would hold at the
  WMO minimum **for each cell's terrain** (minimum density x cell area, summed), replacing the single 575 km²
  rule. Per-country values are computed from the data; the paper publishes none. All 174 of Su et al.'s country
  names match Natural Earth ("Svalbard and Jan Mayen" goes to Norway); the 49 cells the explorer notes are in
  South Sudan today (pre-2011 borders in the source) are counted for South Sudan, not Sudan.
- **The urban class makes rich, dense countries fall short.** Su et al. class every one of Germany's 44 cells
  (and Belgium's, the Netherlands') as *Urban*, whose WMO minimum is 66.7 gauges per 1,000 km². Germany's 7,685
  gauges are 34% of the 22,700 that implies, and none of its cells meets it. This is the paper's classification,
  as in the explorer's Urban tab; it is not corrected here, but a reader comparing with Germany should know.
- The comparison is a **share of the minimum**, both countries on one bar (Bangladesh 46 of 951, 5%; Germany
  34%), because raw counts would compare countries of very different size.
- **EM-DAT's export runs into 2026**; the totals stop at 2025 ("Records to 2025"). Recomputed from the raw
  files independently of `build_globe.py`: Bangladesh, born 2000, floods: 3,581 deaths and 113,527,462 affected
  (2000-2025; 2026 adds 59 and 1,280,039); 11,915,755 flood displacements (IDMC 2008-2025); 46 gauges in 10
  cells, 951 needed. `tests/profile.test.js` checks the page shows these.
- Small states with no 1° land cell in Su et al. (49 of the 219 countries offered, e.g. Malta, Mauritius,
  Luxembourg) get a line saying so instead of a gauge bar.

**Slides 18 to 24 on the final page (5 Oct 2026, late): choices and checks.**
- **Slide 19, Africa's stations go dark.** 2,119 African stations (the slide 6 definition) on 1,100 cells of 0.5°;
  a cell is lit from the first year any of its stations reports to the last. Cells reporting: 878 in 1970,
  1,003 in 1980 (the peak), 519 in 2000, 399 in 2025 (`check_figures.py` recomputes 1970 and 2025). A cell going
  dark means its records stop reaching the global archive (GHCN-Daily), not necessarily that its stations closed:
  the Menne et al. (2012) finding above. Lighting cells from their first year (not only switching them off) shows
  stations being installed too, so the map does not overstate the fall.
- **Slide 21, the timeline runs 2022 to 2026**, not 2024 to 2026 as the narrative's visual note says: the world's
  events are from 2022 and 2023 (EUMETSAT suspended Russia's licences in March 2022; the Arctic Council paused on
  3 March 2022; Ukraine's hydromet service reported losing a quarter of its observing network by 2023, counting
  since 2014, and the label says so). US dates from the research dossier's chronology: FEWS NET suspended early
  2025, balloon cuts March 2025, the plan to cut NOAA by a quarter April 2025 (NYT), the 66 withdrawals
  7 January 2026. The second NOAA proposal (April 2026) was left off for space; the narration's "proposals" covers it.
- **Slide 21's Arctic fade** uses the base station grid split at 66.56 N (731 of the 132,501 station counts, in
  478 cells); the two parts add back to the base layer exactly and are drawn at its brightness. Still illustrative.
- **Slide 23's dial**: one ring = one hour of world military spending, US$2,887 billion / 8,760 h = US$329.6
  million ("about US$330 million"); US$400 million is 1.21 rings, 1 hour 13 minutes.
- **Slide 18's photos are placeholders** in each story's colour. The article images are listed in stories.json
  (`photo_ref`, `photo_credit`); their licences are not cleared and nothing has been downloaded.

**Slide 18's photos (5 Oct 2026, the author's go-ahead).** Each story's own article image, read from the
article's og:image, downloaded to `prototypes/stories/photos/raw/` (git-ignored, about 28 MB), centre-cropped to
16:9 (Bangladesh from the top, to keep the faces), and saved at 640 x 360 WebP in `photos/web/` (about 30 KB
each); the page shows them in the design system's duotone over each story's colour, with the credit from
`stories.json`. Source URLs are kept there as `photo_url`. 12 of 22 have a photo (11 articles plus the
project's own seal photo). Not used, with the reason in `photo_note`: Ratu River (Alamy), Yangtze (Getty
Images), Guyana (Shutterstock), all stock photos licensed separately; Vanuatu (a posed group photo, too busy);
sharks (the only image is a chart); EU wind and solar (a logo); Ghana, Assam, March et al., South Australia
(no image found). **None of the licences is cleared**: clear them before the repository is public, as for the
Idai photos. The page grew from 10.0 to 10.5 MB. The card follows the design system's story card; the slide's
narration was shortened to one line by the author, and the descriptions are cut to three lines on the card.

**The author's revised order (5 Oct 2026, late; `website-text_v2.txt`).**
- Six acts. Removed: "The rich get better maps". The closing order is now question, works, not-enough, money,
  fraying, end; four titles and two passages are the author's rewordings (slides 2-5's "from around the world";
  the end's "No country can see the storm coming alone").
- **Clarified the same evening:** slide 18 is the stories, retitled "The frontlines are responding"; slide 19 is a
  new pause, "What can we do to support them?", the line alone over an empty globe (it replaces "What can we do to
  stop this needless loss of life?"); then "We know what works". 24 slides.
- **The AI flood-map study is a hope story** (Wu, Zhang & Stouffs 2026, doi 10.1038/s41467-026-74336-x), with the
  illustrative FEMA and model dots on the US. Its description quotes only the paper's figures (11.04 million more
  people, 69% above baseline); the old slide's "it couldn't be done for Mozambique" was unsourced and is gone.
- Figures no longer on the page and removed from `check_figures.py`: Sub-Saharan Africa's <1% of CO2, "about
  thirty" deaths in 2020, "Mozambique has no national flood map". 56 figures now, 0 failed.
- On slide 22 the two March 2022 events share one line ("EUMETSAT and the Arctic Council suspend work with Russia"),
  as in the narration, so the slide fits a 720 px screen under its longer title.

**Further edits from the author (5 Oct 2026, late).**
- Titles: slide 8 "The Gaps: Cell by cell"; slide 9 "What happens when we can't predict what's coming" with
  the subtitle "A case study of Cyclone Idai in Mozambique" (Idai's track alone, drawn in over 5 s); slide 12 "The
  storm was expected. The flood was not." (its flood layer now rises from faint to 90% over 3 s); slide 16 "Who
  lives and who dies" (the line "Counted in money, disasters look like a rich-world problem" removed); slide 17
  "How about the place you were born?"; the last slide "There can be no gaps in the weather machine", its end
  card ending "Collective Planetary Stewardship." instead of "Radar."
- "Beyond people" is two slides, both numbered like "Idai in numbers": the animals (124,498 birds, 10,305 sheep and
  goats, 5,428 cows, 3,191 pigs; US$3.1 million) and the power grid (1,345 km of transmission lines, 10,216 km of
  distribution lines, 3,990 transformers, 30 substations), from the author's long narrative, likely the 2019
  PDNA: still "source to come". The transformers were in the long narrative but not the short text.
- Slide 21's year and live cell count are drawn on the map, top right of Africa.
- Slide 24's timeline is vertical: one event a row in date order, a filled dot for the US, hollow for the wider
  world. On screens under 820 px tall the layer legend steps aside and the illustrative note moves into the
  timeline's key ("Globe: illustrative fade").
- **Bug found and fixed:** two CSS comments added on 5 Oct were never closed (`/* ...` with no `*/`), so the
  browser skipped the rules after them up to the next comment's end (the end card's short-screen rule, the
  timeline legend rule, the stats layout). All style blocks were scanned; none is left open.


**More edits (5 Oct 2026, late).** The rain-gauge gap layer is off "We can afford to fix it" and the end slide (the
author: too heavy). "Yet the world is pulling back": the narration ends at "...suspended cooperation with Russia";
the globe is tilted towards the pole so the US, Europe and Russia show together; the station lights of the countries
it names flicker (`st_flicker`: 4,437 cells of 0.5° with a GHCN-Daily station reporting in 2024 or later in the US,
Russia, Ukraine, and Finland, Sweden and Denmark, the EU members of the Arctic Council). The flicker is illustrative
and the slide's note says so. "Beyond people": animal counts in red, grid figures in orange; the closing line is now
"The damage cascades: lost herds and a broken grid keep costing families long after the water goes down."

**Flicker revised (5 Oct 2026, late):** all the lights switch on and off together, abruptly, in an irregular Morse-like rhythm (a failing bulb); off leaves a faint ghost. The faint layer of all other stations was removed from that slide so the flicker reads, including over the dense US.

**End slide transition (5 Oct 2026, late):** no zoom any more (zoomFrom/slow removed: it lagged). From the arctic view the globe turns back to the slides 2-5 view (equator from slightly above) at the same distance (0.84) and rotates; the stations, satellites and Argo floats fill in year by year as on slides 2-5, at 1 s a decade instead of 1.5 (a hidden `era` sweep, 1900 to 2025). No rain gauges, no pulsing cold spots.
