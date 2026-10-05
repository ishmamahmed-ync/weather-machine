"""
Convert argo_coldspots.geojson (26 patch polygons) into point form.

Writes two files next to the input:

  argo_coldspots_points.geojson     one dot per 1-degree grid cell whose centre
                                    falls inside a coldspot patch. Same grid as
                                    argo-density-1deg.geojson (centres at x.5),
                                    so the dots line up with the density layer.
  argo_coldspots_centroids.geojson  one dot per patch, placed on the grid cell
                                    nearest the patch's spherical centroid (so
                                    it always lands inside the patch, even for
                                    C-shaped or antimeridian-spanning ones).

Standard library only. Usage:  python3 scripts/coldspots_to_points.py

Copied into the repo on 5 Oct 2026 from the author's Data/Argo/ folder. How the 26 patches in
argo_coldspots.geojson were drawn is not recorded anywhere on this machine.
"""
import json
import math
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent / "data/processed"   # repo copy: reads and writes data/processed
SRC = HERE / "argo_coldspots.geojson"


def in_ring(x, y, ring):
    """Ray-casting point-in-polygon test for one ring of [lon, lat] pairs."""
    inside = False
    for (x1, y1), (x2, y2) in zip(ring, ring[1:]):
        if (y1 > y) != (y2 > y):
            if x < x1 + (y - y1) * (x2 - x1) / (y2 - y1):
                inside = not inside
    return inside


def in_polygon(x, y, poly):
    """poly = [outer, hole, hole, ...]"""
    return in_ring(x, y, poly[0]) and not any(in_ring(x, y, h) for h in poly[1:])


def to_xyz(lon, lat):
    lo, la = math.radians(lon), math.radians(lat)
    return (math.cos(la) * math.cos(lo), math.cos(la) * math.sin(lo), math.sin(la))


def main():
    src = json.loads(SRC.read_text())
    cells, centroids = [], []

    for f in src["features"]:
        pid = f["properties"]["patch_id"]
        area = f["properties"]["area_km2"]
        g = f["geometry"]
        polys = g["coordinates"] if g["type"] == "MultiPolygon" else [g["coordinates"]]

        # bounding box, snapped to the half-degree grid
        xs = [c[0] for p in polys for c in p[0]]
        ys = [c[1] for p in polys for c in p[0]]
        pts = []
        lat = math.floor(min(ys)) + 0.5
        while lat < max(ys):
            lon = math.floor(min(xs)) + 0.5
            while lon < max(xs):
                if any(in_polygon(lon, lat, p) for p in polys):
                    pts.append((lon, lat))
                lon += 1
            lat += 1

        if not pts:
            raise SystemExit(f"patch {pid}: no grid centre inside, needs a finer grid")

        for lon, lat in pts:
            cells.append({"type": "Feature",
                          "geometry": {"type": "Point", "coordinates": [lon, lat]},
                          "properties": {"patch_id": pid, "patch_area_km2": area}})

        # spherical mean of the cells, then snap to the nearest cell inside the patch
        v = [sum(c) for c in zip(*(to_xyz(*p) for p in pts))]
        n = math.sqrt(sum(c * c for c in v))
        v = [c / n for c in v]
        best = max(pts, key=lambda p: sum(a * b for a, b in zip(to_xyz(*p), v)))
        centroids.append({"type": "Feature",
                          "geometry": {"type": "Point", "coordinates": list(best)},
                          "properties": {"patch_id": pid, "area_km2": area,
                                         "cells": len(pts)}})
        print(f"patch {pid:>2}: {area:>9,} km2 -> {len(pts):>4} dots")

    for name, feats in [("argo_coldspots_points.geojson", cells),
                        ("argo_coldspots_centroids.geojson", centroids)]:
        out = {"type": "FeatureCollection", "name": name[:-8], "features": feats}
        (HERE / name).write_text(json.dumps(out, separators=(",", ":")))
        print(f"wrote {name}: {len(feats)} points")


if __name__ == "__main__":
    main()
