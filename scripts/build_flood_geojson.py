"""
Turn an EM-DAT flood export into a single ArcGIS-ready GeoJSON of points.

    python build_flood_geojson.py <emdat.xlsx> <out.geojson> [--since YEAR]

EM-DAT populates Latitude/Longitude for only a minority of flood records, so
location is resolved in three tiers and the tier is recorded on every feature
as `geo_precision`:

    reported  - EM-DAT's own Latitude/Longitude
    admin1    - mean centroid of the admin units EM-DAT lists, matched by name
                against Natural Earth 10m admin-1 provinces
    country   - country centroid, a last resort

Every feature carries every property, using null where a value is absent.
This matters: some readers infer the field schema from the first feature only,
so an omitted property can silently become a missing column.
"""

import sys, json, re, argparse, unicodedata
import pandas as pd
import numpy as np
from shapely.geometry import shape

NUM = {
    "deaths": "Total Deaths",
    "injured": "No. Injured",
    "affected": "No. Affected",
    "total_affected": "Total Affected",
    "homeless": "No. Homeless",
    "damage_kusd": "Total Damage ('000 US$)",
}


def norm(s):
    if s is None or (isinstance(s, float) and np.isnan(s)):
        return ""
    s = unicodedata.normalize("NFKD", str(s)).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]", "", s.lower())


def load_geo(adm1_path, country_path):
    adm1 = {}
    for f in json.load(open(adm1_path))["features"]:
        p = f["properties"]
        iso = p.get("adm0_a3")
        pt = shape(f["geometry"]).representative_point()
        for key in ("name", "name_en", "gn_name", "woe_name", "name_alt"):
            v = p.get(key)
            if not v:
                continue
            for part in str(v).split("|"):
                k = (iso, norm(part))
                if k[1]:
                    adm1.setdefault(k, (pt.y, pt.x))

    ctry = {}
    for f in json.load(open(country_path))["features"]:
        p = f["properties"]
        pt = shape(f["geometry"]).representative_point()
        for key in ("ISO_A3", "ADM0_A3", "SOV_A3"):
            v = p.get(key)
            if v and v != "-99":
                ctry.setdefault(v, (pt.y, pt.x))
    return adm1, ctry


def resolve(row, adm1, ctry):
    lat, lon = row.get("Latitude"), row.get("Longitude")
    if pd.notna(lat) and pd.notna(lon) and -90 <= lat <= 90 and -180 <= lon <= 180:
        return float(lat), float(lon), "reported", None

    iso = row.get("ISO")
    au = row.get("Admin Units")
    if pd.notna(au):
        try:
            units = json.loads(au)
        except Exception:
            units = []
        names, pts = [], []
        for u in units:
            for k in ("adm1_name", "adm2_name"):
                n = u.get(k)
                if not n:
                    continue
                names.append(n)
                hit = adm1.get((iso, norm(n)))
                if hit:
                    pts.append(hit)
                break
        if pts:
            return (float(np.mean([p[0] for p in pts])),
                    float(np.mean([p[1] for p in pts])),
                    "admin1", len(pts))

    hit = ctry.get(iso)
    if hit:
        return float(hit[0]), float(hit[1]), "country", None
    return None, None, None, None


def iso_date(row, prefix):
    y = row.get(f"{prefix} Year")
    if pd.isna(y):
        return None
    m = row.get(f"{prefix} Month")
    d = row.get(f"{prefix} Day")
    m = int(m) if pd.notna(m) else 1
    d = int(d) if pd.notna(d) else 1
    try:
        return f"{int(y):04d}-{m:02d}-{d:02d}"
    except Exception:
        return None


def val(row, col):
    if col not in row:
        return None
    v = pd.to_numeric(row[col], errors="coerce")
    return None if pd.isna(v) else int(v)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("src")
    ap.add_argument("out")
    ap.add_argument("--since", type=int)
    ap.add_argument("--adm1", default="ne_adm1.geojson")
    ap.add_argument("--countries", default="ne_countries.geojson")
    a = ap.parse_args()

    d = pd.read_excel(a.src, sheet_name="EM-DAT Data")
    if a.since:
        d = d[d["Start Year"] >= a.since]
    adm1, ctry = load_geo(a.adm1, a.countries)

    feats, tally, dropped = [], {"reported": 0, "admin1": 0, "country": 0}, 0
    for _, row in d.iterrows():
        lat, lon, prec, nunits = resolve(row, adm1, ctry)
        if lat is None:
            dropped += 1
            continue
        tally[prec] += 1

        props = {
            "disno": row.get("DisNo."),
            "event_name": None if pd.isna(row.get("Event Name")) else str(row["Event Name"]),
            "country": row.get("Country"),
            "iso": row.get("ISO"),
            "region": row.get("Region"),
            "subregion": row.get("Subregion"),
            "subtype": row.get("Disaster Subtype"),
            "location": None if pd.isna(row.get("Location")) else str(row["Location"])[:250],
            "start_date": iso_date(row, "Start"),
            "end_date": iso_date(row, "End"),
            "year": int(row["Start Year"]) if pd.notna(row.get("Start Year")) else None,
            "geo_precision": prec,
            "admin_units_matched": nunits,
        }
        for k, col in NUM.items():
            props[k] = val(row, col)

        # log helpers: these distributions span seven orders of magnitude, so a
        # linear proportional-symbol ramp collapses everything but the top few.
        for k in ("deaths", "injured", "affected", "total_affected"):
            v = props[k]
            props[f"{k}_log"] = None if v is None else round(float(np.log10(v + 1)), 3)

        feats.append({
            "type": "Feature",
            "geometry": {"type": "Point", "coordinates": [round(lon, 4), round(lat, 4)]},
            "properties": props,
        })

    with open(a.out, "w", encoding="utf-8") as f:
        json.dump({"type": "FeatureCollection", "features": feats}, f, ensure_ascii=False)

    print(f"features written {len(feats):,}   dropped (no location) {dropped}")
    for k, v in tally.items():
        print(f"  {k:<9} {v:>5}  ({100*v/len(feats):4.1f}%)")


if __name__ == "__main__":
    main()
