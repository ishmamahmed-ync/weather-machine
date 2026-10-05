#!/usr/bin/env python3
"""Build idai.html: a scroll story of the 2019 cyclone season in Mozambique.

    cd prototypes/idai && python3 build_idai.py

Photos (photos/) and the two satellite images (maps/) are referenced by relative
path; everything else is packed into the page.

Inputs
  data/processed/storm_nodes.csv           IBTrACS tracks, 12-hourly: Desmond, Idai, Kenneth
  data/raw/ne_50m_admin_0_countries.geojson   country shapes for the globe and the track map
  data/raw/idai/unosat-TC20190312MOZ_SHP/  UNOSAT Sentinel-1 flood extent, 13-20 March 2019
                                           (HDX "UNOSAT Geospatial Data on Floods in Mozambique")
  data/raw/idai/cems-EMSR348_*_GRADING/    Copernicus EMS EMSR348 building damage grading,
                                           Pleiades 0.5 m, 26 March 2019, plus streets / water
  data/raw/idai/nasa-modis-aqua-721-*.jpg  NASA GIBS, MODIS Aqua bands 7-2-1, 24 Feb / 21 Mar 2019,
                                           EPSG:4326, bbox 33.9..35.2 E, 20.6..19.0 S
  site-src/template.html                   d3-array + d3-geo, inlined so the page works from file://

Prints what it kept, and the checks it ran, every time.
"""
import csv
import json
import math
import re
import shutil
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
RAW = ROOT / "data/raw/idai"
sys.path.insert(0, str(ROOT / "prototypes/country-profile"))
from build_globe import simplify, simplify_ring   # noqa: E402
from shp import read                              # noqa: E402

STORMS = {"2019018S24033": "desmond", "2019063S18038": "idai", "2019112S10053": "kenneth"}
SAT_BBOX = [33.9, -20.6, 35.2, -19.0]          # the GIBS request; flood map uses the same frame
FLOOD_BBOX = [32.4, -21.2, 35.9, -18.4]        # wider than the frame: the zoomed globe shows land beyond it, so no false edge
DMG_BBOX = [34.82, -19.862, 34.935, -19.772]   # Beira city, the four graded districts
FLOOD_FILES = ["ST1_20190313_WaterExtent_SofalaProvince", "ST1_20190314_WaterExtent_SofalaProvince",
               "ST1_20190319_WaterExtent_SofalaProvince", "ST1_20190319_WaterExtent_ManicaSofalaProvinces",
               "ST1_20190320_WaterExtent_SofalaProvince"]
# label positions: OpenStreetMap Nominatim, settlement points (queried 2026-10-04)
PLACES = {"Beira": [34.8358, -19.8340], "Dondo": [34.7435, -19.6164], "Buzi": [34.5969, -19.8838],
          "Nhamatanda": [34.2083, -19.2702], "Mafambisse": [34.6326, -19.5460], "Tica": [34.4350, -19.4025],
          "Guara-Guara": [34.4667, -19.8639], "Grudja": [33.9860, -19.8203]}


def enc(ring, scale):
    """[[x,y],...] -> flat ints, first point absolute then deltas (small JSON)."""
    out, px, py = [], 0, 0
    for x, y in ring:
        ix, iy = round(x * scale), round(y * scale)
        out += [ix - px, iy - py]; px, py = ix, iy
    return out


def inside(ring, b):
    xs = [p[0] for p in ring]; ys = [p[1] for p in ring]
    return not (max(xs) < b[0] or min(xs) > b[2] or max(ys) < b[1] or min(ys) > b[3])


def ring_area(r):
    R = 6371.0088; a = 0.0
    for (x1, y1), (x2, y2) in zip(r, r[1:]):
        a += math.radians(x2 - x1) * (2 + math.sin(math.radians(y1)) + math.sin(math.radians(y2)))
    return a * R * R / 2


def main():
    data = {"places": PLACES, "satBox": SAT_BBOX, "dmgBox": DMG_BBOX}

    # ---- storm tracks ----
    tracks = {n: [] for n in STORMS.values()}
    for r in csv.DictReader(open(ROOT / "data/processed/storm_nodes.csv")):
        if r["sid"] in STORMS:
            tracks[STORMS[r["sid"]]].append([round(float(r["lon"]), 2), round(float(r["lat"]), 2), r["time"][:13], r["category"], float(r["wind_kt"] or 0)])
    data["tracks"] = tracks
    for k, v in tracks.items():
        print(f"track {k}: {len(v)} points, {v[0][2]} to {v[-1][2]}")

    # ---- countries: whole world for the globe, finer for the track map ----
    ne = json.loads((ROOT / "data/raw/ne_50m_admin_0_countries.geojson").read_text())["features"]
    world, region = {}, {}
    for f in ne:
        iso = f["properties"].get("ADM0_A3")
        world[iso] = simplify(f["geometry"], eps=0.12)
        if iso in ("MOZ", "MWI", "ZWE", "ZMB", "ZAF", "MDG", "TZA", "SWZ", "BWA", "COM", "MYT"):
            region[iso] = simplify(f["geometry"], eps=0.01)
    data["world"], data["region"] = world, region
    data["moz"] = simplify(next(f for f in ne if f["properties"].get("ADM0_A3") == "MOZ")["geometry"], eps=0.03)

    # ---- UNOSAT flood extent, clipped to the satellite frame ----
    rings, kept_area, src_area, dropped = [], 0.0, 0.0, 0
    for name in FLOOD_FILES:
        for g, p in read(RAW / "unosat-TC20190312MOZ_SHP" / name):
            assert p["Water_Stat"].startswith("New Water"), p["Water_Stat"]   # flood only, no permanent water
            for r in g["parts"]:
                if not inside(r, FLOOD_BBOX):
                    continue
                a = ring_area(r); src_area += a
                s = simplify_ring(r, 0.0008)
                if len(s) < 4:
                    dropped += 1; continue
                kept_area += ring_area(s)
                rings.append(enc(s, 1e4))
    data["flood"] = rings
    print(f"flood: {len(rings)} rings kept, {dropped} slivers dropped; signed area kept "
          f"{abs(kept_area):,.0f} of {abs(src_area):,.0f} km2 summed over 5 overlapping passes "
          f"({abs(kept_area) / abs(src_area) * 100:.1f}%)")

    # ---- Copernicus EMSR348 building damage, Beira ----
    pts, grades = [], Counter()
    G = {"Destroyed": 3, "Damaged": 2, "Possibly damaged": 1}
    for d in ("21BEIRANW", "22BEIRAWEST", "23BEIRACENTER", "24BEIRAEAST"):
        for g, p in read(RAW / f"cems-EMSR348_{d}_GRADING" / f"EMSR348_{d}_GRA_v2_built_up_p"):
            x, y = g["parts"][0][0]
            pts += [round(x * 1e5), round(y * 1e5), G[p["damage_gra"]]]; grades[p["damage_gra"]] += 1
    data["dmg"] = pts
    print(f"damage points: {sum(grades.values())} {dict(grades)}")

    # one readable map for the final page (the author, 5 Oct): Beira Center only, not the four districts stitched
    c_pts, c_grades = [], Counter()
    for g, p in read(RAW / "cems-EMSR348_23BEIRACENTER_GRADING" / "EMSR348_23BEIRACENTER_GRA_v2_built_up_p"):
        x, y = g["parts"][0][0]
        c_pts += [round(x * 1e5), round(y * 1e5), G[p["damage_gra"]]]; c_grades[p["damage_gra"]] += 1
    xs, ys = c_pts[0::3], c_pts[1::3]
    center_box = [min(xs) / 1e5, min(ys) / 1e5, max(xs) / 1e5, max(ys) / 1e5]
    center = {"dmg": c_pts, "box": center_box, "grades": dict(c_grades)}
    print(f"Beira Center: {sum(c_grades.values())} graded {dict(c_grades)}, box {center_box}")

    roads, water, coast, aoi = [], [], [], []
    for d in ("03BEIRA", "21BEIRANW", "22BEIRAWEST", "23BEIRACENTER", "24BEIRAEAST"):
        base = RAW / f"cems-EMSR348_{d}_GRADING"
        for g, p in read(base / f"EMSR348_{d}_GRA_v2_transportation_l"):
            for part in g["parts"]:
                if inside(part, DMG_BBOX):
                    roads.append([1 if p["obj_type"].startswith("212") else 0] + enc(part, 1e5))
        for g, p in read(base / f"EMSR348_{d}_GRA_v2_area_of_interest_a"):
            if d != "03BEIRA":
                aoi.append(enc(g["parts"][0], 1e5))
        if (base / f"EMSR348_{d}_GRA_v2_hydrography_a.shp").exists():
            for g, p in read(base / f"EMSR348_{d}_GRA_v2_hydrography_a"):
                if p["obj_type"].split("-")[0] in ("BA040", "BH140", "BH080"):
                    for part in g["parts"]:
                        if inside(part, DMG_BBOX):
                            water.append(enc(part, 1e5))
        if (base / f"EMSR348_{d}_GRA_v2_hydrography_l.shp").exists():
            for g, p in read(base / f"EMSR348_{d}_GRA_v2_hydrography_l"):
                if p["obj_type"].startswith("BA010"):
                    for part in g["parts"]:
                        coast.append(enc(part, 1e5))
    data.update(roads=roads, water=water, coast=coast, aoi=aoi)
    data["center"] = center
    print(f"Beira base: {len(roads)} road/rail lines, {len(water)} water areas, {len(coast)} coastline lines, {len(aoi)} district outlines")

    # ---- satellite pair ----
    (HERE / "maps").mkdir(exist_ok=True)
    for day in ("2019-02-24", "2019-03-21"):
        shutil.copy(RAW / f"nasa-modis-aqua-721-{day}.jpg", HERE / "maps" / f"modis-721-{day}.jpg")

    site = (ROOT / "site-src/template.html").read_text()
    d3 = "\n".join(re.search(rf'<script id="{k}">.*?</script>', site, re.S).group(0) for k in ("D3A", "D3G"))
    page = (HERE / "template.html").read_text()
    for token in ("__D3__", "__DATA__"):
        assert token in page, f"template.html has no {token}"
    payload = json.dumps(data, separators=(",", ":"))
    page = page.replace("__D3__", d3).replace("__DATA__", payload)
    missing = [p for p in re.findall(r'(?:photo|img):\s*"([^"]+)"', page) if not (HERE / p).exists()]
    assert not missing, f"files referenced but missing: {missing}"
    (HERE / "idai.html").write_text(page)
    # the same data for the final page's shared globe (scripts/build_all.py reads it)
    (HERE / "idai-data.json").write_text(payload)
    print(f"wrote idai.html  {(HERE / 'idai.html').stat().st_size/1e6:.2f} MB (data {len(payload)/1e6:.2f} MB) + photos/ + maps/")


if __name__ == "__main__":
    main()
