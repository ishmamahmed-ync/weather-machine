#!/usr/bin/env python3
"""Build globe.html: the one-screen country comparison (globe + four circles).

    cd prototypes/country-profile && python3 build_globe.py

Per country (ISO3) it stores YEARLY series so the page can sum from the user's
birth year:
  em    EM-DAT 2000-2025 (the export starts in 2000): deaths and total affected,
        all weather/climate disasters and floods only (Flood + Glacial lake outburst flood)
  disp  IDMC GIDD 2008-2025: disaster internal displacements, all and floods only
  risk  Rentschler et al. 2022, people exposed to a 1-in-100-year flood (flood_exposure.csv)
  gauges, need, stations   GHCN-Daily active precipitation gauges, WMO minimum
        (one per 575 km2), active stations reporting temperature
Plus, for the globe: simplified Natural Earth country shapes and the active
gauge / station locations (deduplicated to 0.1 degree cells).

Reuses the name matching and area code in build_data.py.

Also writes profile-data.json, for the final page's plugin (story-plugin.js, slide 17 "Since you were
born"): the same yearly series, people at risk and shapes. su_by_country() (Su et al. 2026 gauges against
the WMO minimum for each cell's terrain) is kept but not used: the author dropped the gauge half, 5 Oct.
"""
import csv
import json
import math
import re
import sys
from collections import defaultdict

from build_data import ALIASES, HERE, PROC, RAW, ROOT, WMO_KM2, geom_area, norm, num
from xlsx import read_rows

EM0, EM1 = 2000, 2025
GI0, GI1 = 2008, 2025
FLOOD_EM = {"Flood", "Glacial lake outburst flood"}
sys.setrecursionlimit(100000)   # rdp recursion on long coastlines (Russia, Canada)


# ---------- geometry: Ramer-Douglas-Peucker on lon/lat ----------
def rdp(pts, eps):
    if len(pts) < 3:
        return pts
    (x1, y1), (x2, y2) = pts[0], pts[-1]
    dx, dy = x2 - x1, y2 - y1
    L = math.hypot(dx, dy) or 1e-12
    idx, dmax = 0, -1
    for i in range(1, len(pts) - 1):
        x, y = pts[i]
        d = abs(dy * x - dx * y + x2 * y1 - y2 * x1) / L
        if d > dmax:
            idx, dmax = i, d
    if dmax <= eps:
        return [pts[0], pts[-1]]
    return rdp(pts[:idx + 1], eps)[:-1] + rdp(pts[idx:], eps)


def simplify_ring(ring, eps):
    """RDP on a closed ring. Plain rdp() measures distance from the first-to-last
    chord, which for a closed ring is a single point, so every ring collapsed to
    two points. Split at the vertex farthest from the start and simplify each half."""
    if len(ring) < 4:
        return ring
    x0, y0 = ring[0]
    k = max(range(len(ring)), key=lambda i: (ring[i][0] - x0) ** 2 + (ring[i][1] - y0) ** 2)
    if k == 0:
        return ring
    return rdp(ring[:k + 1], eps)[:-1] + rdp(ring[k:], eps)


def simplify(geom, eps=0.06):
    polys = geom["coordinates"] if geom["type"] == "MultiPolygon" else [geom["coordinates"]]
    out = []
    for poly in polys:
        rings = []
        for ring in poly:
            r = simplify_ring(ring, eps)
            if len(r) >= 4:
                rings.append([[round(x * 100), round(y * 100)] for x, y in r])   # 0.01 degree ints
        if rings:
            out.append(rings)
    if not out:   # tiny island state: keep its largest ring, unsimplified
        big = max((p[0] for p in polys), key=len)
        out = [[[[round(x * 100), round(y * 100)] for x, y in big]]]
    return out


def main():
    # ---- countries ----
    ne = json.loads((RAW / "ne_50m_admin_0_countries.geojson").read_text())["features"]
    C, byname, shapes = {}, {norm(k): v for k, v in ALIASES.items()}, {}
    for key in ("ADM0_A3", "ISO_A3_EH", "ISO_A3"):
        for f in ne:
            p = f["properties"]; iso = p.get(key)
            if not iso or iso == "-99" or iso in C:
                continue
            C[iso] = {"iso": iso, "name": p.get("NAME_LONG") or p["NAME"], "area": round(geom_area(f["geometry"]))}   # full names, not "Bosnia and Herz."
            shapes[iso] = simplify(f["geometry"])
            for n in ("NAME", "NAME_LONG", "ADMIN", "FORMAL_EN", "NAME_SORT", "NAME_ALT", "BRK_NAME"):
                if p.get(n):
                    byname.setdefault(norm(p[n]), iso)
    iso_of = lambda name: byname.get(norm(name))

    # ---- EM-DAT yearly ----
    rows = read_rows(RAW / "emdat-2026-10-03.xlsx")
    h = next(rows); I = {k: i for i, k in enumerate(h)}
    g = lambda r, k: r[I[k]] if I[k] < len(r) else ""
    ny = EM1 - EM0 + 1
    em = defaultdict(lambda: [[0] * ny for _ in range(4)])   # deaths_all, aff_all, deaths_flood, aff_flood
    for r in rows:
        y = int(num(g(r, "Start Year")))
        if not (EM0 <= y <= EM1):
            continue
        s = em[g(r, "ISO")]; i = y - EM0
        d, a = int(num(g(r, "Total Deaths"))), int(num(g(r, "Total Affected")))
        s[0][i] += d; s[1][i] += a
        if g(r, "Disaster Type") in FLOOD_EM:
            s[2][i] += d; s[3][i] += a

    # ---- IDMC GIDD yearly, all and flood, from the event rows ----
    ng = GI1 - GI0 + 1
    disp = defaultdict(lambda: [[0] * ng for _ in range(2)])
    for f in sorted((RAW / "idmc-events").glob("*.xlsx")):
        rows = read_rows(f)
        h = next(rows); I = {k: i for i, k in enumerate(h)}
        for r in rows:
            if g(r, "Figure cause") != "Disaster" or g(r, "Figure category") != "Internal Displacements":
                continue
            y = int(num(g(r, "Year")))
            if not (GI0 <= y <= GI1):
                continue
            v = int(num(g(r, "Total figures")))
            s = disp[g(r, "ISO3")]
            s[0][y - GI0] += v
            if g(r, "Hazard type") == "Flood":
                s[1][y - GI0] += v

    # ---- flood exposure (Rentschler et al. 2022) ----
    risk, miss = {}, []
    for r in csv.DictReader(open(HERE / "flood_exposure.csv")):
        iso = iso_of(r["country"])
        if iso:
            risk[iso] = int(r["exposed_k"]) * 1000
        else:
            miss.append(r["country"])
    print(f"flood exposure: {len(risk)} countries matched" + (f"; UNMATCHED {miss}" if miss else ""))

    # ---- GHCN: active rain gauges and weather stations ----
    gauges, stations = defaultdict(int), defaultdict(int)
    gcell, scell = set(), set()
    for r in csv.DictReader(open(PROC / "ghcnd-stations-with-age.csv")):
        lon, lat = float(r["lon"]), float(r["lat"])
        iso = iso_of(r["country_name"])
        if r["has_precip"] == "1" and r["precip_last"] and int(r["precip_last"]) >= 2025:
            gauges[iso] += 1; gcell.add((round(lon * 10), round(lat * 10)))
        if r["has_temp"] == "1" and r["temp_last"] and int(r["temp_last"]) >= 2025:
            stations[iso] += 1; scell.add((round(lon * 10), round(lat * 10)))
    print(f"GHCN: {sum(gauges.values())} active rain gauges ({len(gcell)} cells), "
          f"{sum(stations.values())} active temperature stations ({len(scell)} cells)")

    # ---- assemble ----
    out = []
    for iso, c in C.items():
        rec = {"iso": iso, "name": c["name"], "area": c["area"]}
        if iso in em: rec["em"] = em[iso]
        if iso in disp: rec["disp"] = disp[iso]
        if iso in risk: rec["risk"] = risk[iso]
        rec["gauges"] = gauges.get(iso, 0)
        rec["stations"] = stations.get(iso, 0)
        rec["need"] = max(1, round(c["area"] / WMO_KM2))
        if "em" in rec or "disp" in rec or "risk" in rec:
            out.append(rec)
    out.sort(key=lambda r: r["name"])
    geo = {iso: s for iso, s in shapes.items()}   # all shapes, so the globe has no holes

    flat = lambda cells: [v for c in sorted(cells) for v in c]
    data = {"meta": {"em": [EM0, EM1], "disp": [GI0, GI1], "wmo_km2": WMO_KM2, "built": "2026-10-03"},
            "countries": out, "shapes": geo, "gaugeCells": flat(gcell), "stationCells": flat(scell)}
    write_plugin_data(data, iso_of)
    payload = json.dumps(data, separators=(",", ":"))
    print(f"{len(out)} countries with data, {len(geo)} shapes; payload {len(payload)/1e3:.0f} KB")

    # d3-array + d3-geo, inlined from the main site so the page works from file://
    site = (ROOT / "site-src/template.html").read_text()
    d3 = "\n".join(re.search(rf'<script id="{k}">.*?</script>', site, re.S).group(0) for k in ("D3A", "D3G"))

    # the main site's grey shaded-relief texture (scripts/make_relief.py), same globe look
    relief = (ROOT / "site-src/layers/relief.webp.b64").read_text().strip()

    page = (HERE / "globe-template.html").read_text()
    for token in ("__D3__", "__DATA__", "__RELIEF__"):
        assert token in page, f"globe-template.html has no {token}"
    page = page.replace("__D3__", d3).replace("__RELIEF__", relief).replace("__DATA__", payload)
    (HERE / "globe.html").write_text(page)
    print(f"wrote globe.html  {(HERE / 'globe.html').stat().st_size/1e6:.2f} MB")


# ---------- Su et al. (2026) rain gauges per country, for the final page ----------
def su_by_country(iso_of):
    """The rain-gauge explorer's cells (prototypes/rain-gauges/template.html, block rg-DATA: Su et al. 2026,
    Fig. 2c data, 1-degree land cells), grouped by country.
    Per country: n = gauges in its cells; need = the gauges its cells would hold at the WMO minimum for each
    cell's terrain (sum of minimum density x cell area); meet / below / none = cells meeting the minimum,
    below it, with no gauge (the explorer's status rule). A cell belongs to the country Su et al. label it
    with (one country per cell). Cells labelled Sudan that the explorer notes are in South Sudan today
    (pre-2011 borders in the source) go to South Sudan.
    Returns (totals by ISO, ISO for each Su country index, cell indices moved to South Sudan)."""
    t = (ROOT / "prototypes/rain-gauges/template.html").read_text()
    D = json.loads(re.search(r'<script id="rg-DATA"[^>]*>(.*?)</script>', t, re.S).group(1))
    alias = {"svalbard and jan mayen": "NOR"}
    su_iso = []
    for c in D["countries"]:
        iso = alias.get(norm(c)) or iso_of(c)
        if not iso: sys.exit(f"Su et al. country not matched: {c}")
        su_iso.append(iso)
    ssd_note = next(i for i, s in enumerate(D["notes"]) if "South Sudan" in s)
    moved = sorted(int(k) for k, v in D["noteMap"].items() if v == ssd_note)
    terr = [0] * len(D["n"])
    for g, (a, b) in enumerate(D["groups"]):
        for i in range(a, b): terr[i] = g // 6
    tot = defaultdict(lambda: {"n": 0, "need": 0.0, "meet": 0, "below": 0, "none": 0})
    moved_set = set(moved)
    for i, n in enumerate(D["n"]):
        iso = "SSD" if i in moved_set else su_iso[D["ctry"][i]]
        r = tot[iso]; w = D["wmo"][terr[i]]
        r["n"] += n; r["need"] += w * D["area"][i] / 1000
        r["meet" if n and n / D["area"][i] * 1000 >= w else "below" if n else "none"] += 1
    for r in tot.values(): r["need"] = round(r["need"])
    print(f"Su et al.: {len(D['n'])} cells, {sum(r['n'] for r in tot.values())} gauges, {len(tot)} countries; "
          f"{len(moved)} cells moved from Sudan to South Sudan")
    return tot, su_iso, moved


def write_plugin_data(data, iso_of, gauges=False):
    """profile-data.json for the final page. The author dropped the slide's rain-gauge half (5 Oct 2026), so
    the Su et al. totals are left out unless gauges=True (kept for a return to it)."""
    tot, su_iso, moved = su_by_country(iso_of) if gauges else ({}, None, None)
    keep = []
    for rec in data["countries"]:
        r = {k: rec[k] for k in ("iso", "name", "em", "disp", "risk") if k in rec}
        if rec["iso"] in tot: r["su"] = tot[rec["iso"]]
        keep.append(r)
    shapes = {r["iso"]: data["shapes"][r["iso"]] for r in keep if r["iso"] in data["shapes"]}
    out = {"meta": data["meta"], "countries": keep, "shapes": shapes}
    if gauges: out.update(suIso=su_iso, suToSSD=moved)
    s = json.dumps(out, separators=(",", ":"))
    (HERE / "profile-data.json").write_text(s)
    print(f"wrote profile-data.json  {len(s)/1e3:.0f} KB, {len(keep)} countries")


if __name__ == "__main__":
    main()
