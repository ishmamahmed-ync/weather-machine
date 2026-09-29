#!/usr/bin/env python3
"""Sendai Framework Target G-1: which countries report having a multi-hazard
early warning system (MHEWS), as of 2022 and as of 2025.

    python scripts/fetch_sendai_g1.py

Source   Sendai Framework Monitor (UNDRR), public analytics API
         https://sendaimonitor.undrr.org/analytics/global-target/16/7
         /api/public/countries                              names, centroids
         /api/public/analytics/indicator/compare/{cycle}?indicatorId=33
                                                            G-1 score per country
         cycle id = reporting year - 2004 (18 = 2022, 21 = 2025)

G-1 is a composite score, 0 to 1, built from G-2..G-5. A country that files a
G-1 value > 0 is reporting that an MHEWS exists; 0 means it reported, but no
system.

"Reported having MHEWS as of year Y" here means: the country's most recent G-1
value filed for any year up to and including Y is greater than 0. Countries
report irregularly, so a single year's cycle undercounts badly (only 44 filed
for 2025 itself).

These counts do NOT match the published Global Status of MHEWS reports exactly
(95 in 2022, 119 in 2025). The Monitor is revised as countries back-fill, and
the reports were snapshots on their publication dates. See docs/NOTES.md.

Output   data/processed/sendai-g1-mhews.csv        every country, G-1 by year
         data/processed/sendai-g1-mhews-2022.csv   countries with MHEWS as of 2022
         data/processed/sendai-g1-mhews-2025.csv   countries with MHEWS as of 2025
"""
import csv
import json
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "data/processed"
API = "https://sendaimonitor.undrr.org/api/public"
YEARS = range(2005, 2027)
SNAPSHOTS = (2022, 2025)


def get(path):
    req = urllib.request.Request(f"{API}/{path}", headers={"User-Agent": "weather-machine"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.load(r)


def as_of(scores, year):
    """Most recent G-1 value filed for any year <= `year`, or None."""
    filed = [(y, v) for y, v in scores.items() if y <= year and v is not None]
    return max(filed)[1] if filed else None


def main():
    countries = get("countries")
    g1 = {}
    for y in YEARS:
        rows = get(f"analytics/indicator/compare/{y - 2004}?indicatorId=33").get("countries") or {}
        for iso, rec in rows.items():
            v = rec.get("selectedYear")
            g1.setdefault(iso, {})[y] = None if v is None else float(v)
        print(f"{y}: {len(rows):>3} countries filed G-1")

    known = {c["cca3"] for c in countries}
    unknown = sorted(set(g1) - known)
    if unknown:
        print(f"dropped, no country record: {unknown}")

    table = []
    for c in sorted(countries, key=lambda c: c["officialName"] or c["name"]):
        iso = c["cca3"]
        row = {"iso3": iso, "name": c["officialName"] or c["name"],
               "region": (c.get("unisdrRegion") or {}).get("name", ""),
               "lat": c["latitude"], "lon": c["longitude"]}
        for y in YEARS:
            v = g1.get(iso, {}).get(y)
            row[f"g1_{y}"] = "" if v is None else v
        table.append(row)

    with open(OUT / "sendai-g1-mhews.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(table[0]))
        w.writeheader()
        w.writerows(table)
    print(f"wrote sendai-g1-mhews.csv: {len(table)} countries")

    for year in SNAPSHOTS:
        keep, zero, never = [], 0, 0
        for row, c in zip(table, sorted(countries, key=lambda c: c["officialName"] or c["name"])):
            v = as_of(g1.get(c["cca3"], {}), year)
            if v is None:
                never += 1
            elif v == 0:
                zero += 1
            else:
                keep.append({k: row[k] for k in ("iso3", "name", "region", "lat", "lon")} | {"g1_latest": v})
        with open(OUT / f"sendai-g1-mhews-{year}.csv", "w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=list(keep[0]))
            w.writeheader()
            w.writerows(keep)
        print(f"as of {year}: {len(keep)} report MHEWS, {zero} reported a score of 0, "
              f"{never} never filed G-1  -> sendai-g1-mhews-{year}.csv")


if __name__ == "__main__":
    main()
