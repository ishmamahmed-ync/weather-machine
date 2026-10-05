#!/usr/bin/env python3
"""Satellites in operation, year by year, from WMO OSCAR/Space: all of them, and weather only.

    cd prototypes/history && python3 extract_satellites.py

Input   data/raw/oscar-space-satellites-2026-10-04.xlsx
        WMO OSCAR/Space satellite list, https://space.oscar.wmo.int/satellites,
        exported 4 Oct 2026 (the file is stamped 2026-10-05, server time), all
        1,052 satellites, no filter. OSCAR covers meteorological AND Earth-observation
        satellites and has no field separating the two, so weather is defined below
        by programme.
Output  satellites.csv   one row per satellite that flew: acronym, programme, orbit, status,
                         launch year, last year of operation (blank = still operating),
                         weather (1 if it meets the definition below)
        satellites_per_year.csv   year, all in operation, weather in operation

The page uses ALL of them (meteorological and Earth observation, as OSCAR lists them).
The weather flag is kept for reference.

Weather definition: programmes whose purpose is routine weather imaging or sounding from
geostationary or polar orbit, run by weather agencies or the military, plus the
experimental forerunners of those series (TIROS, Nimbus). Excluded on purpose:
single-parameter research missions (TRMM, GPM, CloudSat, Aeolus, TROPICS,
Megha-Tropiques), radio-occultation (COSMIC, Spire, PlanetiQ), commercial
constellations (Tomorrow.io), multi-purpose technology demonstrators (ATS),
ocean and land programmes. EXCLUDED_BORDERLINE lists the near misses.

A satellite counts in year Y if it launched in or before Y and its end of life is
in or after Y. Dropped from everything: "Lost at launch", and "Planned" or not yet
launched (they never operated). Rows for a satellite moved to a new post
("Meteosat-7 (IODC)") are folded into the satellite; rows standing for several
("CYGNSS (8 sats)") count that many. Presumably inactive / Unclear with an open EOL
("≥2019") end in that year. Not weather: satellites with no payload listed (INSAT
communications satellites) and NOT_WEATHER. Anything not
Inactive whose EOL is open ("≥2032") or in the future counts as operating now;
that includes satellites marked Back-up or Stand-by, which are in orbit and
working but not the primary satellite at their post. An Inactive satellite with
an open EOL ("≥2014") is taken to have ended that year.
"""
import csv
import re
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
sys.path.insert(0, str(ROOT / "prototypes/country-profile"))
from xlsx import read_rows  # noqa: E402

SRC = ROOT / "data/raw/oscar-space-satellites-2026-10-04.xlsx"
NOW = 2026

WEATHER = [
    # US
    "Television and Infra-Red Observation Satellite",
    "Nimbus",
    "TIROS Operational System",
    "NOAA 3rd generation / Improved TIROS Operational System",
    "National Oceanic and Atmospheric Administration - 4th generation",
    "NOAA 4th generation / Polar Operational Environmental Satellites",
    "NOAA 5th generation / Polar Operational Environmental Satellites",
    "Joint Polar Satellite System",
    "Synchronous Meteorological Satellite",
    "Geostationary Operational Environmental Satellite - 1st generation",
    "Geostationary Operational Environmental Satellite - 2nd generation",
    "Geostationary Operational Environmental Satellite - 3rd generation",
    "Defense Meteorological Satellite Program - Block 5D-1",
    "Defense Meteorological Satellite Program - Block 5D-2",
    "Defense Meteorological Satellite Program - Block 5D-3",
    "Electro-optical Infrared Weather System-Geostationary mission",
    "Weather System Follow-on",
    # Europe
    "Meteosat First Generation",
    "Meteosat Second Generation (MSG)",
    "Meteosat Third Generation (MTG) - “I” imaging, “S” sounding",
    "EUMETSAT Polar System",
    "EPS Second Generation",
    "Arctic Weather Satellite",
    # Russia / USSR
    "Meteor-1", "Meteor-2", "Meteor-3", "Meteor-3M",
    "Electro",
    "Arctica in Molniya orbit",
    # Japan, China, India, Korea
    "Himawari 1st generation (Geostationary Meteorological Satellite)",
    "Himawari 2nd generation (Multifunction Transport Satellite)",
    "Himawari 3rd generation",
    "Feng-Yun - 1", "Feng-Yun - 2", "Feng-Yun - 3", "Feng-Yun - 4",
    "Indian National Satellite - 1", "Indian National Satellite - 2", "Indian National Satellite - 3",
    "Kalpana",
    "Communication, Oceanography and Meteorology Satellite",
]
EXCLUDED_BORDERLINE = [
    "Application Technology Satellite", "Tropical Rainfall Measuring Mission",
    "Global Precipitation Measurement mission", "Megha-Tropiques",
    "Time-Resolved Observations of Precipitation structure and storm Intensity with a Constellation of Smallsats",
    "Constellation Observing System for Meteorology, Ionosphere & Climate", "Tomorrow.io constellation",
    "Meteor-Priroda", "Sentinel-3", "Deep Space Climate Observatory",
]
# satellites inside a kept programme that carry no weather instrument
NOT_WEATHER = {
    "GEO-KOMPSAT-2B": "air quality (GEMS) and ocean colour (GOCI-II); the weather imager is on 2A",
}


def year(s):
    m = re.search(r"(19\d\d|20\d\d)", s or "")
    return int(m.group(1)) if m else None


def end_year(r):
    """Last year in operation; None = still operating; False = drop (with reason)."""
    status, eol_raw = r["Sat status"], r["(expected) EOL"]
    eol = year(eol_raw)
    if status in ("Inactive", "Presumably inactive", "Unclear"):
        # "≥2019" on a satellite not known to be working: OSCAR confirms it up to 2019, so it ends there
        return eol if eol is not None else False
    if "≥" in eol_raw or eol is None or eol >= NOW:
        return None                                         # still operating (incl. back-up, stand-by)
    return eol


def count(acronym):
    """Rows like 'CYGNSS (8 sats)' stand for several satellites."""
    m = re.search(r"\((\d+) sats?\)", acronym)
    return int(m.group(1)) if m else 1


def main():
    rows = list(read_rows(SRC))
    R = [dict(zip(rows[0], r)) for r in rows[1:]]
    progs = {r["Satellite Programme"] for r in R}
    missing = [p for p in WEATHER + EXCLUDED_BORDERLINE if p not in progs]
    assert not missing, f"programme names not in the export: {missing}"

    sats, dropped = [], Counter()
    for r in R:
        launch = year(r["Launch"])
        if r["Sat status"] == "Lost at launch":
            dropped["lost at launch"] += 1; continue
        if r["Sat status"] == "Planned" or launch is None or launch > NOW or "≥" in r["Launch"]:
            dropped["not launched (planned, concept, TBD)"] += 1; continue
        eol = end_year(r)
        if eol is False:
            dropped["inactive, no end date"] += 1; continue
        weather = (r["Satellite Programme"] in WEATHER and r["Acronym"] not in NOT_WEATHER
                   and bool(r["Payload"].strip()))
        sats.append({"acronym": r["Acronym"], "programme": r["Satellite Programme"], "orbit": r["Orbit"],
                     "status": r["Sat status"], "launch": launch, "eol": "" if eol is None else eol,
                     "weather": int(weather), "count": count(r["Acronym"])})

    # The same spacecraft moved to a new post gets its own row: "Meteosat-7 (IODC)",
    # "GOES-10 (S-America)". Fold those into the original: first launch to last end.
    by = {s["acronym"]: s for s in sats}
    merged = []
    for s in sats:
        m = re.match(r"^(.*?)\s*\(([^)]*)\)$", s["acronym"])
        if m and m.group(1) in by and not re.match(r"\d+ sats?$", m.group(2)):
            base = by[m.group(1)]
            base["eol"] = "" if "" in (base["eol"], s["eol"]) else max(base["eol"], s["eol"])
            merged.append(s["acronym"])
    sats = [s for s in sats if s["acronym"] not in merged]

    sats.sort(key=lambda s: (s["launch"], s["acronym"]))
    with open(HERE / "satellites.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(sats[0])); w.writeheader(); w.writerows(sats)

    def alive(s, y): return s["launch"] <= y and (s["eol"] == "" or s["eol"] >= y)
    per = [(y, sum(s["count"] for s in sats if alive(s, y)), sum(s["count"] for s in sats if alive(s, y) and s["weather"]))
           for y in range(1959, NOW + 1)]
    with open(HERE / "satellites_per_year.csv", "w", newline="") as f:
        w = csv.writer(f); w.writerow(["year", "all_in_operation", "weather_in_operation"]); w.writerows(per)

    print(f"{len(R):,} rows in OSCAR; {len(sats):,} satellites flew and are kept "
          f"({sum(s['count'] for s in sats):,} counting multi-satellite rows); dropped: {dict(dropped)}")
    print(f"  relocation rows folded into their satellite: {len(merged)}: {', '.join(merged)}")
    print(f"  of which weather: {sum(s['weather'] for s in sats)}; still operating: "
          f"{sum(s['count'] for s in sats if s['eol'] == '')} ({sum(1 for s in sats if s['eol'] == '' and s['weather'])} weather)")
    print("  in operation, all / weather:")
    print("  " + "  ".join(f"{y}:{a}/{w}" for y, a, w in per if y % 5 == 0))


if __name__ == "__main__":
    main()
