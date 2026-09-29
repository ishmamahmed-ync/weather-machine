#!/usr/bin/env python3
"""Pack the Sendai G-1 MHEWS countries into site-src/layers/globe-data.json,
as dots filling each country's boundary.

    python scripts/fetch_sendai_g1.py     # first, if the CSVs need refreshing
    python scripts/add_mhews_layers.py

Input   data/processed/sendai-g1-mhews-2022.csv
        data/processed/sendai-g1-mhews-2025.csv
        data/raw/ne_50m_admin_0_countries.geojson
            Natural Earth 1:50m admin-0 countries, public domain.
            https://github.com/nvkelso/natural-earth-vector (geojson/)
Output  DATA.mhews_2022, DATA.mhews_2025 = { type:'points', xy:[lon,lat, ...] }

Each reporting country gets one dot per 1-degree cell centre (x.5, the same grid
as the Argo layer) that falls inside its boundary. A country too small to hold
any cell centre gets a single dot at the Sendai Monitor's centroid, so no
reporting country disappears.

Countries are matched on ISO 3166 alpha-3 (Natural Earth ADM0_A3, then
ISO_A3_EH for the few, like France and Norway, whose ISO_A3 is -99). Admin-0 boundaries include overseas territories: France's shape
contains French Guiana and Reunion, the US includes Alaska and Hawaii.

Safe to re-run: it replaces those two entries and leaves every other layer alone.
"""
import csv
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "site-src/layers/globe-data.json"
BOUNDS = ROOT / "data/raw/ne_50m_admin_0_countries.geojson"


def in_ring(x, y, ring):
    inside = False
    for (x1, y1), (x2, y2) in zip(ring, ring[1:]):
        if (y1 > y) != (y2 > y) and x < x1 + (y - y1) * (x2 - x1) / (y2 - y1):
            inside = not inside
    return inside


def fill(geometry):
    """1-degree cell centres inside a Polygon or MultiPolygon."""
    polys = geometry["coordinates"] if geometry["type"] == "MultiPolygon" else [geometry["coordinates"]]
    pts = set()
    for poly in polys:
        outer, holes = poly[0], poly[1:]
        xs = [c[0] for c in outer]
        ys = [c[1] for c in outer]
        lat = math.floor(min(ys)) + 0.5
        while lat < max(ys):
            lon = math.floor(min(xs)) + 0.5
            while lon < max(xs):
                if in_ring(lon, lat, outer) and not any(in_ring(lon, lat, h) for h in holes):
                    pts.add((lon, lat))
                lon += 1
            lat += 1
    return sorted(pts)


def main():
    # ADM0_A3 first: ISO_A3_EH is shared by some territories (Ashmore and
    # Cartier Islands and the Indian Ocean Territories both carry AUS), and
    # whichever came first in the file would otherwise stand in for Australia.
    features = json.loads(BOUNDS.read_text())["features"]
    shapes = {}
    for key in ("ADM0_A3", "ISO_A3_EH", "ISO_A3"):
        for f in features:
            iso = f["properties"].get(key)
            if iso and iso != "-99":
                shapes.setdefault(iso, f["geometry"])

    cache = {}
    data = json.loads(OUT.read_text())
    for year in (2022, 2025):
        rows = list(csv.DictReader(open(ROOT / f"data/processed/sendai-g1-mhews-{year}.csv")))
        xy, small, missing = [], [], []
        for r in rows:
            iso = r["iso3"]
            if iso not in cache:
                cache[iso] = fill(shapes[iso]) if iso in shapes else []
                if iso not in shapes:
                    missing.append(iso)
            pts = cache[iso] or [(round(float(r["lon"]), 2), round(float(r["lat"]), 2))]
            if not cache[iso]:
                small.append(r["name"])
            for lon, lat in pts:
                xy += [lon, lat]
        data[f"mhews_{year}"] = {"type": "points", "xy": xy}
        print(f"mhews_{year}: {len(rows)} countries -> {len(xy)//2} dots")
        print(f"   single centroid dot (smaller than a grid cell): {len(small)}: {', '.join(small)}")
        if missing:
            print(f"   no boundary found, centroid used: {missing}")
    OUT.write_text(json.dumps(data, separators=(",", ":")))
    print(f"packed into {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
