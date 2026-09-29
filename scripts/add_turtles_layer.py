#!/usr/bin/env python3
"""Pack leatherback and loggerhead turtle cells into site-src/layers/globe-data.json.

    python scripts/add_turtles_layer.py

Input   data/processed/obis-species-by-cell.csv
        rows are (species, lon, lat) for each 1-degree cell a species occupies;
        lon/lat are cell centres rounded to whole degrees (range -180..180)
Output  DATA.turtles = { type:'points', xy:[lon,lat, ...] }
        one dot per cell holding either species; a cell holding both is drawn once

Safe to re-run: it replaces the turtles entry and leaves every other layer alone.
"""
import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "data/processed/obis-species-by-cell.csv"
OUT = ROOT / "site-src/layers/globe-data.json"
SPECIES = {"Dermochelys coriacea": "leatherback", "Caretta caretta": "loggerhead"}

cells, per = set(), {s: 0 for s in SPECIES}
for r in csv.DictReader(open(SRC)):
    if r["species"] in SPECIES:
        per[r["species"]] += 1
        cells.add((float(r["lon"]), float(r["lat"])))
for s, n in per.items():
    print(f"{SPECIES[s]:>11} ({s}): {n} cells")

xy = [v for c in sorted(cells) for v in c]
data = json.loads(OUT.read_text())
data["turtles"] = {"type": "points", "xy": xy}
OUT.write_text(json.dumps(data, separators=(",", ":")))
print(f"turtles: {len(cells)} distinct cells packed into {OUT.relative_to(ROOT)}")
