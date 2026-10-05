#!/usr/bin/env python3
"""Build history.html: one scene, 1900 to the present, in three chapters with a decade slider.

    cd prototypes/history && python3 build_history.py

Standard library only. Writes history.html next to this file; open it directly.

Weather stations   data/processed/ghcnd-stations-with-age.csv (GHCN-Daily, 132,501 stations)
                   Binned to the 0.5-degree land grid. For each decade 1900s..2020s, the
                   number of stations whose record overlaps that decade:
                   first_year <= decade + 9 and last_year >= decade.
                   These are record spans in the global archive, NOT installation dates
                   (see scripts/add_station_ages.py and docs/NOTES.md, Menne et al. 2012).

Argo floats        data/processed/argo-density-1deg.geojson, 1-degree ocean cells.
                   A cell is lit from its first_year to its last_year.

Satellites         satellites.csv, made by extract_satellites.py from WMO OSCAR/Space: every
                   meteorological and Earth-observation satellite that flew. Real launch and
                   end-of-life years, so the number on screen is real; each satellite's
                   position on the globe is random (illustrative).
"""
import csv
import json
import math
import re
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
DECADES = list(range(1900, 2030, 10))          # 1900 .. 2020, 13 keyframes
LAND = 0.5


def main():
    # ---- stations: per 0.5-degree cell, stations per decade ----
    cells = defaultdict(lambda: [0] * len(DECADES))
    used = skipped = 0
    for r in csv.DictReader(open(ROOT / "data/processed/ghcnd-stations-with-age.csv")):
        if not r["first_year"] or not r["last_year"]:
            skipped += 1
            continue
        f, l = int(r["first_year"]), int(r["last_year"])
        lon, lat = float(r["lon"]), float(r["lat"])
        if lon >= 180: lon -= 360
        c = (math.floor(lon / LAND), math.floor(lat / LAND))
        for i, d in enumerate(DECADES):
            if f <= d + 9 and l >= d:
                cells[c][i] += 1
        used += 1
    per_decade = [sum(v[i] for v in cells.values()) for i in range(len(DECADES))]
    st_xy, st_n = [], []
    for (lo, la), v in sorted(cells.items()):
        if any(v):
            st_xy += [lo * LAND + LAND / 2, la * LAND + LAND / 2]
            st_n += v
    print(f"stations: {used:,} used, {skipped} without dates skipped, {len(st_xy)//2:,} cells")
    for d, n in zip(DECADES, per_decade):
        print(f"   {d}s  {n:>7,} stations with data in the decade")

    # ---- argo: 1-degree cells with first/last year ----
    ar_xy, ar_y, ar_n = [], [], []
    for feat in json.loads((ROOT / "data/processed/argo-density-1deg.geojson").read_text())["features"]:
        lon, lat = feat["geometry"]["coordinates"]
        if lon >= 180: lon -= 360
        p = feat["properties"]
        ar_xy += [lon, lat]; ar_y += [p["first_year"], p["last_year"]]; ar_n.append(p["profiles"])
    total = sum(ar_n)
    print(f"argo: {len(ar_n):,} cells, {total:,} profiles, first year {min(ar_y[0::2])}")
    for y in (2000, 2005, 2010, 2020):
        print(f"   {y}: {sum(1 for i in range(len(ar_n)) if ar_y[2*i] <= y <= ar_y[2*i+1]):,} cells lit")

    # ---- satellites: launch and end-of-life years (blank end = still operating), one per spacecraft ----
    sats = [(int(r["launch"]), int(r["eol"]) if r["eol"] else 9999)
            for r in csv.DictReader(open(HERE / "satellites.csv")) for _ in range(int(r["count"]))]
    per_year = {int(r["year"]): int(r["all_in_operation"])
                for r in csv.DictReader(open(HERE / "satellites_per_year.csv"))}
    print(f"satellites: {len(sats)}; in operation 1960 {per_year[1960]}, 1990 {per_year[1990]}, 2025 {per_year[2025]}")

    data = {"decades": DECADES, "perDecade": per_decade,
            "sats": [v for s in sats for v in s], "satsPerYear": per_year,
            "st": {"s": LAND, "xy": st_xy, "n": st_n},
            "argo": {"xy": ar_xy, "y": ar_y, "n": ar_n}}
    payload = json.dumps(data, separators=(",", ":"))

    # d3-array + d3-geo, inlined from the main site so the page works from file://
    site = (ROOT / "site-src/template.html").read_text()
    d3 = "\n".join(re.search(rf'<script id="{k}">.*?</script>', site, re.S).group(0) for k in ("D3A", "D3G"))
    # the main site's grey shaded-relief texture (scripts/make_relief.py)
    relief = (ROOT / "site-src/layers/relief.webp.b64").read_text().strip()

    page = (HERE / "template.html").read_text()
    for token in ("__D3__", "__DATA__", "__RELIEF__", "__LAYERS_JS__"):
        assert token in page, f"template.html has no {token}"
    page = (page.replace("__D3__", d3).replace("__RELIEF__", relief).replace("__DATA__", payload)
                .replace("__LAYERS_JS__", (HERE / "history-layers.js").read_text()))
    # the same data for the final page's shared globe (scripts/build_all.py reads it)
    (HERE / "history-data.json").write_text(payload)
    assert 'src="http' not in page, "page loads a remote script; it must stay self-contained"
    (HERE / "history.html").write_text(page)
    print(f"wrote history.html  {(HERE / 'history.html').stat().st_size/1e6:.2f} MB "
          f"(data {len(payload)/1e3:.0f} KB)")


if __name__ == "__main__":
    main()
