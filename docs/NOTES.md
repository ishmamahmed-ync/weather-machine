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

**The apparent post-1970 decline is largely archival.** NOAA attributes it to
discontinued contributions from countries in the international collection, and
the "international collection" is a static archive ending in 2008. Nearly half
of Brazil's stations have their last year in either 1983 or 1997 — feeds ending,
not instruments failing. The defensible claim is that the shared record is
thinning, not that measurement stopped.

**Damage and deaths have different coverage.** In the flood file, 1,243 events
carry deaths and only 406 carry damage. Comparing the two maps without saying so
would read a reporting gap as a finding.

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
