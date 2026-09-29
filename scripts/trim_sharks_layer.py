#!/usr/bin/env python3
"""Trim the sharks grid layer in site-src/layers/globe-data.json to the
Northwest Atlantic, the region of McDonnell et al. (2026).

    python scripts/trim_sharks_layer.py

The layer is OBIS shark occurrence (16 species, location only), packed as a
1-degree grid: s = cell size, d = delta-encoded cell index, n = count per cell.
It keeps cells whose centre is between 82W and 60W and between 24N and 46N, and
re-encodes the deltas. Before trimming, 137 cells: 63 around North America's
east coast, Gulf and Caribbean, 56 Pacific, 6 NE Atlantic and Mediterranean,
12 elsewhere.

Safe to re-run: cells already outside the box are gone, so a second run changes nothing.
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "site-src/layers/globe-data.json"
LON, LAT = (-82, -60), (24, 46)

data = json.loads(OUT.read_text())
L = data["sharks"]
st = L["s"]; N = round(360 / st); la0 = round(90 / st); lo0 = round(180 / st)

idx, cells = 0, []
for d, n in zip(L["d"], L["n"]):
    idx += d
    la = idx // N - la0
    lo = idx - (la + la0) * N - lo0
    lon, lat = lo * st + st / 2, la * st + st / 2
    cells.append((idx, lon, lat, n))

keep = [c for c in cells if LON[0] <= c[1] <= LON[1] and LAT[0] <= c[2] <= LAT[1]]
d_out, prev = [], 0
for idx, *_ in keep:
    d_out.append(idx - prev); prev = idx
data["sharks"] = {"s": st, "d": d_out, "n": [c[3] for c in keep]}
OUT.write_text(json.dumps(data, separators=(",", ":")))
print(f"sharks: kept {len(keep)} of {len(cells)} cells, dropped {len(cells) - len(keep)}")
