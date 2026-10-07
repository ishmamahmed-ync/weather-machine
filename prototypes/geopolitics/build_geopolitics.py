#!/usr/bin/env python3
"""Slide 23, "Some regions withhold data because of geopolitical tensions": the map data for its two stops.

    python3 prototypes/geopolitics/build_geopolitics.py      (standard library only)

Writes prototypes/geopolitics/geopolitics-data.json, which scripts/build_all.py puts in the page for the plugin
(story-plugin.js). Inputs, in data/raw (not committed; docs/SOURCES.md):

  geopolitics/flood2025/FL20250818PAK_SHP/VIIRS_20250826_20250907_FloodWaterExtent_PAK
      UNOSAT, satellite-detected flood water over Pakistan, 26 Aug to 7 Sep 2025 (VIIRS, NOAA), CC BY-SA,
      via HDX. One multipolygon, "New Water / Water Increase", "Not yet field validated". Simplified here.
  geopolitics/rivers/ne_10m_rivers_lake_centerlines
      Natural Earth 10m rivers (public domain): the six rivers of the Indus Waters Treaty only.
  ne_50m_admin_0_countries.geojson
      Natural Earth 50m countries: the seven Arctic Council states other than Russia, tinted on the Arctic stop.

No borders are drawn between India and Pakistan or between Russia and Ukraine (Kashmir and Crimea are disputed);
those countries are named by labels only.
"""
import json, math, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
RAW = ROOT / "data/raw"
sys.path.insert(0, str(ROOT / "prototypes/idai")); sys.path.insert(0, str(ROOT / "prototypes/country-profile"))
from shp import read                                   # noqa: E402
from build_globe import rdp, simplify_ring, simplify   # noqa: E402

TREATY = ("Indus", "Jhelum", "Chenab", "Ravi", "Beas", "Sutlej")      # western three to Pakistan, eastern three to India
ARCTIC = ("USA", "CAN", "GRL", "DNK", "ISL", "NOR", "SWE", "FIN")    # Greenland is part of the Kingdom of Denmark


def ring_area(r):
    return abs(sum(x1 * y2 - x2 * y1 for (x1, y1), (x2, y2) in zip(r, r[1:] + r[:1]))) / 2


def flood():
    g, p = next(iter(read(str(RAW / "geopolitics/flood2025/FL20250818PAK_SHP/VIIRS_20250826_20250907_FloodWaterExtent_PAK"))))
    assert p["Water_Stat"].startswith("New Water"), p["Water_Stat"]
    rings, n0, dropped = [], 0, 0
    for part in g["parts"]:
        n0 += len(part)
        if ring_area(part) < 3e-5: dropped += 1; continue           # under ~0.3 km2: specks; the rest is 94% of the area
        r = simplify_ring(part, 0.005)
        if len(r) < 4: dropped += 1; continue
        rings.append([v for x, y in r for v in (round(x * 1000), round(y * 1000))])
    print(f"flood: {len(g['parts'])} rings, {n0:,} points -> {len(rings)} rings, {sum(len(r) for r in rings)//2:,} points "
          f"({dropped} small rings dropped); UNOSAT area {p['Area_m2']/1e6:,.0f} km2")
    return rings


def rivers():
    out = {}
    for g, p in read(str(RAW / "geopolitics/rivers/ne_10m_rivers_lake_centerlines")):
        name = (p.get("name") or "").strip("\x00 ")
        if name not in TREATY: continue
        xs = [x for part in g["parts"] for x, y in part]
        if not 60 < min(xs) < 82: continue                          # another river of the same name elsewhere
        for part in g["parts"]:
            out.setdefault(name, []).append([v for x, y in rdp(part, 0.01) for v in (round(x, 3), round(y, 3))])
    assert sorted(out) == sorted(TREATY), sorted(out)
    print("rivers: " + ", ".join(f"{k} {sum(len(l) for l in v)//2}" for k, v in out.items()))
    return out


def arctic():
    feats = json.loads((RAW / "ne_50m_admin_0_countries.geojson").read_text())["features"]
    out = {f["properties"]["ADM0_A3"]: simplify(f["geometry"], 0.08) for f in feats if f["properties"]["ADM0_A3"] in ARCTIC}
    assert sorted(out) == sorted(ARCTIC), sorted(out)
    print("arctic council states: " + ", ".join(out))
    return out


def main():
    data = {"flood": flood(), "rivers": rivers(), "arctic": arctic()}
    f = Path(__file__).parent / "geopolitics-data.json"
    f.write_text(json.dumps(data, separators=(",", ":")))
    print(f"wrote {f.relative_to(ROOT)}  {f.stat().st_size/1e3:.0f} KB")


if __name__ == "__main__":
    main()
