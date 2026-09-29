#!/usr/bin/env python3
"""Pack the Argo coldspot dots into site-src/layers/globe-data.json.

    python scripts/add_coldspots_layer.py

Input   data/processed/argo_coldspots_points.geojson
        one point per 1-degree cell whose centre falls inside a coldspot patch
        (made from argo_coldspots.geojson by Data/Argo/coldspots_to_points.py)
Output  DATA.coldspots = { type:'points', xy:[lon,lat, lon,lat, ...] }

Safe to re-run: it replaces the coldspots entry and leaves every other layer alone.
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "data/processed/argo_coldspots_points.geojson"
OUT = ROOT / "site-src/layers/globe-data.json"

feats = json.loads(SRC.read_text())["features"]
xy = []
for f in feats:
    lon, lat = f["geometry"]["coordinates"]
    xy += [round(lon, 2), round(lat, 2)]

data = json.loads(OUT.read_text())
data["coldspots"] = {"type": "points", "xy": xy}
OUT.write_text(json.dumps(data, separators=(",", ":")))
print(f"coldspots: {len(feats)} points packed into {OUT.relative_to(ROOT)}")
