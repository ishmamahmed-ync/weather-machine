#!/usr/bin/env python3
"""Build data.json and index.html for the country-profile prototype.

    cd prototypes/country-profile && python3 build_data.py

One record per country (ISO 3166 alpha-3), from five sources:

  EM-DAT        data/raw/emdat-2026-10-03.xlsx
                weather and climate disasters only (hydrological, meteorological,
                climatological; the export has no geophysical events), start
                years 2006-2025: deaths, injured, total affected, event count
  CRI 2026      data/raw/germanwatch-cri-2026-full-report.pdf, annex table
                (transcribed to cri2026.csv by extract_cri.py): rank 1995-2024, rank 2024
  GHCN-Daily    data/processed/ghcnd-stations-with-age.csv: stations with a
                precipitation record reporting in 2025 or 2026, against the WMO
                minimum of one precipitation gauge per 575 km2 (WMO-No. 168,
                Table I.2.6, interior plains / hilly; coasts 900, mountains 250)
  Areas         data/raw/ne_50m_admin_0_countries.geojson, spherical area of
                the admin-0 polygon (includes overseas territories)
  IDMC GIDD     data/raw/idmc-gidd-displacements-2008-2025.xlsx: disaster
                internal displacements per country-year, summed 2008-2025
                data/raw/idmc-events/*.xlsx: event level, the flood share
                (Hazard type = Flood, Figure category = Internal Displacements)

Every join is on ISO3. GHCN and CRI only carry names; unmatched names are
printed so they can be added to the alias table below.
"""
import csv
import json
import math
import re
import unicodedata
from collections import defaultdict
from pathlib import Path

from xlsx import read_rows

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
RAW, PROC = ROOT / "data/raw", ROOT / "data/processed"
Y0, Y1 = 2006, 2025          # EM-DAT window: 20 full years
WMO_KM2 = 575                # km2 per precipitation gauge, interior plains

# names in GHCN or the CRI that don't match Natural Earth's
ALIASES = {
    "burma": "MMR", "congo (kinshasa)": "COD", "congo (brazzaville)": "COG",
    "democratic republic of congo": "COD", "republic of congo": "COG",
    "dr congo": "COD", "congo republic": "COG",
    "gambia, the": "GMB", "the gambia": "GMB", "bahamas, the": "BHS", "the bahamas": "BHS",
    "cote d'ivoire": "CIV", "cote d‘ivoire": "CIV", "ivory coast": "CIV",
    "korea, south": "KOR", "korea, republic of": "KOR", "korea, north": "PRK",
    "islamic republic of afghanistan": "AFG", "islamic republic of iran": "IRN",
    "lao people‘s democratic republic": "LAO", "lao people's democratic republic": "LAO",
    "kyrgyz republic": "KGZ", "slovak republic": "SVK", "czech republic": "CZE",
    "democratic republic of timor-leste": "TLS", "east timor": "TLS",
    "chinese taipei": "TWN", "russia": "RUS", "swaziland": "SWZ", "cape verde": "CPV",
    "st. kitts and nevis": "KNA", "st. lucia": "LCA", "st. vincent and the grenadines": "VCT",
    "micronesia": "FSM", "federated states of micronesia": "FSM", "turkey": "TUR",
    "united states of america": "USA", "united states": "USA", "macedonia": "MKD",
    "north macedonia": "MKD", "vietnam": "VNM", "bosnia and herzegovina": "BIH",
    "tanzania": "TZA", "moldova": "MDA", "syria": "SYR", "brunei": "BRN",
    "west bank": "PSE", "gaza strip": "PSE", "palestine": "PSE", "kosovo": "XKX",
    "south sudan": "SSD", "sao tome and principe": "STP", "eswatini": "SWZ",
    # territories whose gauges belong to the admin-0 shape that contains them
    "french guiana": "FRA", "reunion": "FRA", "mayotte": "FRA",
    "svalbard": "NOR", "jan mayen": "NOR", "falkland islands (islas malvinas)": "FLK",
    "gibraltar": "GIB", "macau s.a.r": "MAC", "midway islands": "UMI", "virgin islands": "VIR",
}


def norm(s):
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode()
    s = re.sub(r"\s*\[.*?\]", "", s)              # "Reunion [France]" -> "Reunion"
    return re.sub(r"\s+", " ", s.strip().lower())


def ring_area_km2(ring):
    R = 6371.0088
    a = 0.0
    for (x1, y1), (x2, y2) in zip(ring, ring[1:]):
        a += math.radians(x2 - x1) * (2 + math.sin(math.radians(y1)) + math.sin(math.radians(y2)))
    return abs(a * R * R / 2)


def geom_area(g):
    polys = g["coordinates"] if g["type"] == "MultiPolygon" else [g["coordinates"]]
    return sum(ring_area_km2(p[0]) - sum(ring_area_km2(h) for h in p[1:]) for p in polys)


def num(x):
    try:
        return float(x) if x not in ("", None) else 0.0
    except ValueError:
        return 0.0


def main():
    # ---- countries, names, areas (Natural Earth) ----
    ne = json.loads((RAW / "ne_50m_admin_0_countries.geojson").read_text())["features"]
    C, byname = {}, {norm(k): v for k, v in ALIASES.items()}   # aliases go through the same normalising
    for key in ("ADM0_A3", "ISO_A3_EH", "ISO_A3"):
        for f in ne:
            p = f["properties"]
            iso = p.get(key)
            if not iso or iso == "-99" or iso in C:
                continue
            C[iso] = {"iso": iso, "name": p["NAME"], "area_km2": round(geom_area(f["geometry"]))}
            for n in ("NAME", "NAME_LONG", "ADMIN", "FORMAL_EN", "NAME_SORT", "NAME_ALT", "BRK_NAME"):
                if p.get(n):
                    byname.setdefault(norm(p[n]), iso)

    def iso_of(name):
        return byname.get(norm(name))

    # ---- EM-DAT ----
    rows = read_rows(RAW / "emdat-2026-10-03.xlsx")
    h = next(rows); I = {k: i for i, k in enumerate(h)}
    g = lambda r, k: r[I[k]] if I[k] < len(r) else ""
    em, kept, skipped = defaultdict(lambda: defaultdict(float)), 0, 0
    for r in rows:
        y = int(num(g(r, "Start Year")))
        if not (Y0 <= y <= Y1):
            skipped += 1
            continue
        e = em[g(r, "ISO")]
        e["deaths"] += num(g(r, "Total Deaths"))
        e["injured"] += num(g(r, "No. Injured"))
        e["affected"] += num(g(r, "Total Affected"))
        e["events"] += 1
        kept += 1
    print(f"EM-DAT: {kept} events {Y0}-{Y1} across {len(em)} countries; {skipped} outside the window")

    # ---- CRI 2026 ----
    cri, miss = {}, []
    for r in csv.DictReader(open(HERE / "cri2026.csv")):
        iso = iso_of(r["country"])
        if not iso:
            miss.append(r["country"]); continue
        cri[iso] = {"rank_1995_2024": int(r["rank_1995_2024"]), "rank_2024": int(r["rank_2024"])}
    n_cri = len(cri)
    print(f"CRI 2026: {n_cri} countries matched" + (f"; UNMATCHED {miss}" if miss else ""))

    # ---- GHCN precipitation gauges ----
    gauges, miss = defaultdict(int), set()
    for r in csv.DictReader(open(PROC / "ghcnd-stations-with-age.csv")):
        if r["has_precip"] != "1" or not r["precip_last"] or int(r["precip_last"]) < 2025:
            continue
        iso = iso_of(r["country_name"])
        if iso:
            gauges[iso] += 1
        else:
            miss.add(r["country_name"])
    print(f"GHCN: {sum(gauges.values())} active precipitation gauges in {len(gauges)} countries"
          + (f"; unmatched (territories, mostly): {sorted(miss)}" if miss else ""))

    # ---- IDMC GIDD: totals ----
    rows = read_rows(RAW / "idmc-gidd-displacements-2008-2025.xlsx")
    h = next(rows); I = {k: i for i, k in enumerate(h)}
    disp, disp_years = defaultdict(float), defaultdict(float)
    for r in rows:
        v = g(r, "Disaster Internal Displacements (Raw)")
        if v:
            disp[g(r, "ISO3")] += num(v)
            disp_years[(g(r, "ISO3"), g(r, "Year"))] += num(v)

    # ---- IDMC GIDD: event level, flood share, and a check against the totals ----
    flood, ev_years = defaultdict(float), defaultdict(float)
    for f in sorted((RAW / "idmc-events").glob("*.xlsx")):
        rows = read_rows(f)
        h = next(rows); I = {k: i for i, k in enumerate(h)}
        for r in rows:
            if g(r, "Figure cause") != "Disaster" or g(r, "Figure category") != "Internal Displacements":
                continue
            v = num(g(r, "Total figures"))
            ev_years[(g(r, "ISO3"), g(r, "Year"))] += v
            if g(r, "Hazard type") == "Flood":
                flood[g(r, "ISO3")] += v
    match = sum(1 for k, v in disp_years.items() if abs(ev_years.get(k, 0) - v) <= max(1, 0.001 * v))
    print(f"GIDD: event rows reproduce {match} of {len(disp_years)} published country-year totals")
    worst = sorted(((abs(ev_years.get(k, 0) - v), k, v, ev_years.get(k, 0)) for k, v in disp_years.items()), reverse=True)[:5]
    for d, k, v, e in worst:
        if d > 1:
            print(f"   mismatch {k}: published {v:,.0f}, events sum {e:,.0f}")

    # ---- assemble ----
    out = []
    for iso, c in C.items():
        e = em.get(iso)
        rec = dict(c)
        rec["emdat"] = {k: int(e[k]) for k in ("deaths", "injured", "affected", "events")} if e else None
        rec["cri"] = cri.get(iso)
        n = gauges.get(iso, 0)
        rec["gauges"] = {"active": n, "km2_per_gauge": round(c["area_km2"] / n) if n else None,
                         "wmo_needed": max(1, round(c["area_km2"] / WMO_KM2))}
        rec["gidd"] = {"disaster": int(disp[iso]), "flood": int(flood[iso])} if iso in disp or iso in flood else None
        if rec["emdat"] or rec["cri"] or n or rec["gidd"]:
            out.append(rec)

    # ranks among countries with data (1 = most)
    def rank(key, getter):
        vals = sorted(((getter(r), r["iso"]) for r in out if getter(r) is not None), reverse=True)
        for i, (_, iso) in enumerate(vals):
            next(r for r in out if r["iso"] == iso).setdefault("ranks", {})[key] = [i + 1, len(vals)]
    rank("deaths", lambda r: r["emdat"]["deaths"] if r["emdat"] else None)
    rank("affected", lambda r: r["emdat"]["affected"] if r["emdat"] else None)
    rank("disaster_disp", lambda r: r["gidd"]["disaster"] if r["gidd"] else None)
    rank("flood_disp", lambda r: r["gidd"]["flood"] if r["gidd"] else None)

    out.sort(key=lambda r: r["name"])
    meta = {"emdat_window": [Y0, Y1], "gidd_window": [2008, 2025], "wmo_km2": WMO_KM2, "cri_ranked": n_cri,
            "built": "2026-10-03"}
    payload = json.dumps({"meta": meta, "countries": out}, separators=(",", ":"))
    (HERE / "data.json").write_text(payload)
    print(f"wrote data.json: {len(out)} countries")

    # single self-contained page, like the main site: opens from a file, no server
    page = (HERE / "template.html").read_text()
    assert "__DATA__" in page, "template has no __DATA__ placeholder"
    (HERE / "index.html").write_text(page.replace("__DATA__", payload))
    print(f"wrote index.html  {(HERE / 'index.html').stat().st_size/1e3:.0f} KB")


if __name__ == "__main__":
    main()
