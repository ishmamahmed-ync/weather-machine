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
