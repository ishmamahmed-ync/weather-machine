#!/usr/bin/env python3
"""Put every gridded layer on one of two standard grids: one size for land, one for ocean.

    python scripts/regrid_layers.py                      # land 0.5, ocean 1 (the defaults)
    python scripts/regrid_layers.py --land 1 --ocean 2   # any other pair

Writes a SAMPLE, and leaves the live site alone:

    site-src/layers/globe-data-land<L>-ocean<O>.json   copy of globe-data.json, layers below replaced
    sample-land<L>-ocean<O>.html                       the full site built from that copy

To adopt it, copy the .json over globe-data.json and run build_site.py.

A grid can only be as fine as its source, and must nest into it (be a whole
multiple of it). The script refuses anything else rather than invent positions:
    land   >= 0.25, multiple of 0.25   (stations; MHEWS is redrawn from borders)
    ocean  >= 1,    multiple of 1      (Argo and OBIS sources are 1 degree)

Grid convention (same as the engine's decode()): cell size s, cells start at
-180 / -90, so 1-degree centres are at x.5, 0.5-degree centres at x.25 / x.75.

Land
    stations, usable, years   re-binned from the packed 0.25-degree grid by adding
                              counts. Exact, because the cells nest.
                              (years holds station-years per cell, so it adds too.)
    mhews_2022, mhews_2025    redrawn from Natural Earth borders: one dot per cell centre
                              inside a reporting country, the rule add_mhews_layers.py
                              uses; a country holding no centre gets one dot at the
                              Sendai Monitor's centroid.

Ocean
    argo        from data/processed/argo-density-1deg.geojson, profiles added.
                (The live packed layer is 1.5 degrees, which nests into nothing standard.)
    seals       re-binned from the packed 0.5-degree grid, profiles added. Exact.
    telemetry   from data/processed/obis-species-by-cell.csv: DISTINCT species per
                cell. Adding the 1-degree species counts would count a species once
                for every 1-degree cell it occupies.
    sharks      from data/processed/obis-sharks-by-cell.csv, distinct species per cell,
                kept where the cell centre is in the NW Atlantic box of trim_sharks_layer.py.
    turtles     from obis-species-by-cell.csv: one dot per cell holding leatherback
                or loggerhead.
    coldspots   from data/processed/argo_coldspots.geojson: one dot per cell centre
                inside a coldspot patch (the rule add_coldspots_layer.py used at 1 degree).

OBIS cell coordinates are whole degrees and are read as cell CENTRES (cells span
k-0.5..k+0.5). The previous telemetry and sharks packing read them as south-west
corners, which put those layers half a degree north-east. Evidence for centres:
0 and both -180 and 180 occur (impossible for floored corners), and fewer cells
land on land (9.1% vs 10.7% against Natural Earth 50m). A whole-degree centre
that sits exactly on a 2-degree boundary (even numbers) goes to the cell to its
north-east, which is what floor() does. So on any standard grid the OBIS layers
carry half a source cell (about 55 km) of position uncertainty; at 1 degree this
reproduces the live telemetry and sharks layers exactly.

Not gridded, on purpose: point layers at real locations (fema, aiextra, the
Limpopo xx_* close-ups, st_decay), tracks, bubbles and the satellite shell.
"""
import argparse
import csv
import json
import math
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LAYERS = ROOT / "site-src/layers"
SRC = LAYERS / "globe-data.json"
PROC = ROOT / "data/processed"
BOUNDS = ROOT / "data/raw/ne_50m_admin_0_countries.geojson"
SHARK_BOX = (-82, -60), (24, 46)          # lon, lat; matches trim_sharks_layer.py
TURTLES = {"Dermochelys coriacea", "Caretta caretta"}


# ---- grid helpers ---------------------------------------------------------

def decode(L):
    """Packed grid -> list of (lon, lat, n) at cell centres."""
    st = L["s"]; N = round(360 / st); la0 = round(90 / st); lo0 = round(180 / st)
    idx, out = 0, []
    for d, n in zip(L["d"], L["n"]):
        idx += d
        la = idx // N - la0
        lo = idx - (la + la0) * N - lo0
        out.append((lo * st + st / 2, la * st + st / 2, n))
    return out


def cell(lon, lat, st):
    """(lo, la) integer cell of a point. Longitude 180 wraps to -180."""
    if lon >= 180: lon -= 360
    return math.floor(lon / st), math.floor(lat / st)


def centre(c, st):
    return c[0] * st + st / 2, c[1] * st + st / 2


def encode(counts, st):
    """{(lo, la): n} -> packed {s, d, n}, sorted by cell index."""
    N = round(360 / st); la0 = round(90 / st); lo0 = round(180 / st)
    rows = sorted(((la + la0) * N + (lo + lo0), n) for (lo, la), n in counts.items())
    d, prev = [], 0
    for idx, _ in rows:
        d.append(idx - prev); prev = idx
    return {"s": st, "d": d, "n": [n for _, n in rows]}


def rebin(L, st):
    out = defaultdict(int)
    for lon, lat, n in decode(L):
        out[cell(lon, lat, st)] += n
    return out


def species_cells(path, st, keep=lambda r: True):
    sp = defaultdict(set)
    for r in csv.DictReader(open(path)):
        if keep(r):
            sp[cell(float(r["lon"]), float(r["lat"]), st)].add(r["species"])
    return sp


def in_ring(x, y, r):
    c, j = False, len(r) - 1
    for i in range(len(r)):
        xi, yi = r[i]; xj, yj = r[j]
        if (yi > y) != (yj > y) and x < (xj - xi) * (y - yi) / (yj - yi) + xi:
            c = not c
        j = i
    return c


def centres_inside(geom, st):
    polys = geom["coordinates"] if geom["type"] == "MultiPolygon" else [geom["coordinates"]]
    hits = set()
    for p in polys:
        xs = [a for a, b in p[0]]; ys = [b for a, b in p[0]]
        for lo in range(math.floor(min(xs) / st), math.floor(max(xs) / st) + 1):
            for la in range(math.floor(min(ys) / st), math.floor(max(ys) / st) + 1):
                x, y = centre((lo, la), st)
                if in_ring(x, y, p[0]) and not any(in_ring(x, y, h) for h in p[1:]):
                    hits.add((lo, la))
    return hits


def nests(st, src):
    """True if cells of size st are whole multiples of source cells of size src."""
    k = st / src
    return st >= src and abs(k - round(k)) < 1e-9


def fmt(st):
    return f"{st:g}"


def mhews_points(rows, shapes, st, cache):
    """One dot per cell centre inside each reporting country, as add_mhews_layers.py."""
    xy, small = [], []
    for r in rows:
        iso = r["iso3"]
        if iso not in cache:
            cache[iso] = sorted(set().union(*[centres_inside(g, st) for g in shapes.get(iso, [])]))
        pts = [centre(c, st) for c in cache[iso]]
        if not pts:
            pts = [(round(float(r["lon"]), 2), round(float(r["lat"]), 2))]
            small.append(r["name"])
        for lon, lat in pts:
            xy += [lon, lat]
    return xy, small


# ---- build ----------------------------------------------------------------

def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--land", type=float, default=0.5, help="land cell size in degrees (default 0.5)")
    ap.add_argument("--ocean", type=float, default=1.0, help="ocean cell size in degrees (default 1)")
    a = ap.parse_args()
    LAND, OCEAN = a.land, a.ocean
    if not nests(LAND, 0.25):
        sys.exit(f"--land {fmt(LAND)}: stations are packed at 0.25 degrees; use 0.25, 0.5, 1, 2 ...")
    if not nests(OCEAN, 1.0):
        sys.exit(f"--ocean {fmt(OCEAN)}: Argo and OBIS sources are 1 degree; use 1, 2, 3 ... "
                 "(finer needs the raw downloads, see docs/SOURCES.md)")
    tag = f"land{fmt(LAND)}-ocean{fmt(OCEAN)}"
    OUT_JSON = LAYERS / f"globe-data-{tag}.json"
    OUT_HTML = ROOT / f"sample-{tag}.html"
    L, O = f"{fmt(LAND)} deg", f"{fmt(OCEAN)} deg"

    data = json.loads(SRC.read_text())
    report = []

    def note(key, before, after, extra=""):
        report.append(f"{key:10} {before:>24}  ->  {after:<24} {extra}")

    # land: stations, usable, years
    for k in ("stations", "usable", "years"):
        old = data[k]
        new = rebin(old, LAND)
        assert sum(new.values()) == sum(old["n"]), k
        data[k] = encode(new, LAND)
        note(k, f"{fmt(old['s'])} deg, {len(old['n']):,} cells", f"{L}, {len(new):,} cells",
             f"total {sum(old['n']):,} kept")

    # land points: MHEWS countries, redrawn from borders
    features = json.loads(BOUNDS.read_text())["features"]
    shapes = {}
    for key in ("ADM0_A3", "ISO_A3_EH", "ISO_A3"):      # same precedence as add_mhews_layers.py
        for f in features:
            iso = f["properties"].get(key)
            if iso and iso != "-99":
                shapes.setdefault(iso, [f["geometry"]])
    cache, check = {}, {}
    for year in (2022, 2025):
        rows = list(csv.DictReader(open(PROC / f"sendai-g1-mhews-{year}.csv")))
        old_n = len(data[f"mhews_{year}"]["xy"]) // 2
        xy1, _ = mhews_points(rows, shapes, 1.0, check)
        xy, small = mhews_points(rows, shapes, LAND, cache)
        data[f"mhews_{year}"] = {"type": "points", "xy": xy}
        note(f"mhews_{year}", f"1 deg, {old_n:,} dots", f"{L}, {len(xy)//2:,} dots",
             f"{len(rows)} countries, {len(small)} as one centroid dot "
             f"(method check: 1 deg gives {len(xy1)//2:,})")

    # ocean: argo from the 1-degree processed file
    old = data["argo"]
    new = defaultdict(int)
    for f in json.loads((PROC / "argo-density-1deg.geojson").read_text())["features"]:
        lon, lat = f["geometry"]["coordinates"]
        new[cell(lon, lat, OCEAN)] += f["properties"]["profiles"]
    assert sum(new.values()) == sum(old["n"]), "argo total changed"
    data["argo"] = encode(new, OCEAN)
    note("argo", f"{fmt(old['s'])} deg, {len(old['n']):,} cells", f"{O}, {len(new):,} cells",
         f"total {sum(old['n']):,} profiles kept")

    # ocean: seals from the packed 0.5-degree grid
    old = data["seals"]
    new = rebin(old, OCEAN)
    assert sum(new.values()) == sum(old["n"]), "seals"
    data["seals"] = encode(new, OCEAN)
    note("seals", f"{fmt(old['s'])} deg, {len(old['n']):,} cells", f"{O}, {len(new):,} cells",
         f"total {sum(old['n']):,} profiles kept")

    # ocean: telemetry, distinct species per cell
    old = data["telemetry"]
    sp = species_cells(PROC / "obis-species-by-cell.csv", OCEAN)
    data["telemetry"] = encode({c: len(s) for c, s in sp.items()}, OCEAN)
    allsp = set().union(*sp.values())
    note("telemetry", f"{fmt(old['s'])} deg, {len(old['n']):,} cells", f"{O}, {len(sp):,} cells",
         f"{len(allsp)} species, max {max(map(len, sp.values()))} per cell")

    # ocean: sharks, NW Atlantic only (box tested on the cell centre, as trim_sharks_layer.py)
    old = data["sharks"]
    (x0, x1), (y0, y1) = SHARK_BOX
    sp = species_cells(PROC / "obis-sharks-by-cell.csv", OCEAN)
    sp = {c: s for c, s in sp.items()
          if x0 <= centre(c, OCEAN)[0] <= x1 and y0 <= centre(c, OCEAN)[1] <= y1}
    data["sharks"] = encode({c: len(s) for c, s in sp.items()}, OCEAN)
    note("sharks", f"{fmt(old['s'])} deg, {len(old['n']):,} cells", f"{O}, {len(sp):,} cells",
         f"{len(set().union(*sp.values()))} species in the box")

    # ocean points: turtles
    old_n = len(data["turtles"]["xy"]) // 2
    cells = set(species_cells(PROC / "obis-species-by-cell.csv", OCEAN,
                              lambda r: r["species"] in TURTLES))
    data["turtles"] = {"type": "points",
                       "xy": [v for c in sorted(cells) for v in centre(c, OCEAN)]}
    note("turtles", f"1 deg, {old_n:,} dots", f"{O}, {len(cells):,} dots")

    # ocean points: coldspots, centre-in-patch
    old_n = len(data["coldspots"]["xy"]) // 2
    feats = json.loads((PROC / "argo_coldspots.geojson").read_text())["features"]
    check = set().union(*(centres_inside(f["geometry"], 1.0) for f in feats))
    per = [centres_inside(f["geometry"], OCEAN) for f in feats]
    cells = set().union(*per)
    empty = [f["properties"].get("patch_id") for f, p in zip(feats, per) if not p]
    data["coldspots"] = {"type": "points",
                         "xy": [v for c in sorted(cells) for v in centre(c, OCEAN)]}
    note("coldspots", f"1 deg, {old_n:,} dots", f"{O}, {len(cells):,} dots",
         f"(method check: 1 deg gives {len(check):,})"
         + (f"; patches with no cell centre: {empty}" if empty else ""))

    OUT_JSON.write_text(json.dumps(data, separators=(",", ":")))
    print("\n".join(report))
    print(f"\nwrote {OUT_JSON.relative_to(ROOT)}  {OUT_JSON.stat().st_size/1e6:.2f} MB "
          f"(was {SRC.stat().st_size/1e6:.2f} MB)")

    # build the sample page with the normal builder, pointed at the regridded data
    sys.path.insert(0, str(ROOT / "scripts"))
    import build_site
    build_site.SUBS["__DATA__"] = OUT_JSON
    build_site.OUT = OUT_HTML
    build_site.main()


if __name__ == "__main__":
    main()
