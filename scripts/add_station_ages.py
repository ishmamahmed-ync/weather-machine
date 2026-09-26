"""
Join GHCN-Daily record-of-period data onto the cleaned station file.

    python add_station_ages.py <ghcnd-inventory.txt> <stations-clean.csv> <outdir>

ghcnd-inventory.txt is fixed width (NCEI readme section VII), one row per
station per element:

    ID 1-11, LATITUDE 13-20, LONGITUDE 22-30, ELEMENT 32-35,
    FIRSTYEAR 37-40, LASTYEAR 42-45

FIRSTYEAR is the first year of *unflagged data*, not an installation date. A
station may predate its record, or have been relocated while keeping its ID.
Treat these as record spans, not station ages.
"""

import sys, json, argparse
import numpy as np
import pandas as pd

SPEC = [("station_id", 0, 11), ("element", 31, 35), ("first", 36, 40), ("last", 41, 45)]

TEMP = ("TMAX", "TMIN", "TAVG")
PRECIP = ("PRCP",)

# A station counts as active if it reported in the current or previous year.
ACTIVE_FROM = 2025


def read_inventory(path):
    rows = []
    with open(path, encoding="utf-8", errors="replace") as fh:
        for line in fh:
            if not line.strip():
                continue
            rows.append([line[a:b].strip() for _, a, b in SPEC])
    inv = pd.DataFrame(rows, columns=[k for k, _, _ in SPEC])
    inv["first"] = pd.to_numeric(inv["first"], errors="coerce")
    inv["last"] = pd.to_numeric(inv["last"], errors="coerce")
    return inv.dropna(subset=["first", "last"])


def summarise(inv):
    g = inv.groupby("station_id")
    out = pd.DataFrame({
        "first_year": g["first"].min().astype(int),
        "last_year": g["last"].max().astype(int),
        "n_elements": g["element"].nunique(),
    })

    def span(sub, label):
        if sub.empty:
            return
        s = sub.groupby("station_id")
        out[f"{label}_first"] = s["first"].min()
        out[f"{label}_last"] = s["last"].max()

    span(inv[inv["element"].isin(TEMP)], "temp")
    span(inv[inv["element"].isin(PRECIP)], "precip")

    out["record_years"] = out["last_year"] - out["first_year"] + 1
    out["active"] = (out["last_year"] >= ACTIVE_FROM).astype(int)
    out["has_temp"] = out.get("temp_first", pd.Series(np.nan, index=out.index)).notna().astype(int)
    out["has_precip"] = out.get("precip_first", pd.Series(np.nan, index=out.index)).notna().astype(int)
    out["temp_record_years"] = (out.get("temp_last") - out.get("temp_first") + 1)
    return out.reset_index()


def write_geojson(d, path, props):
    with open(path, "w", encoding="utf-8") as fh:
        fh.write('{"type":"FeatureCollection","features":[\n')
        for i, r in enumerate(d.itertuples(index=False)):
            rec = dict(zip(d.columns, r))
            p = {}
            for k in props:
                v = rec.get(k)
                if v is None or v is pd.NA or (isinstance(v, float) and np.isnan(v)):
                    v = None            # pandas nullable Int64 yields pd.NA
                elif isinstance(v, np.integer):
                    v = int(v)
                elif isinstance(v, np.floating):
                    v = float(v)
                p[k] = v
            feat = {"type": "Feature",
                    "geometry": {"type": "Point", "coordinates": [rec["lon"], rec["lat"]]},
                    "properties": p}
            fh.write(("," if i else "") + json.dumps(feat, ensure_ascii=False, separators=(",", ":")) + "\n")
        fh.write("]}\n")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("inventory")
    ap.add_argument("stations")
    ap.add_argument("outdir")
    a = ap.parse_args()

    inv = read_inventory(a.inventory)
    summary = summarise(inv)
    st = pd.read_csv(a.stations)
    d = st.merge(summary, on="station_id", how="left")

    for c in ("first_year", "last_year", "record_years", "n_elements",
              "active", "has_temp", "has_precip", "temp_first", "temp_last",
              "precip_first", "precip_last", "temp_record_years"):
        if c in d.columns:
            d[c] = d[c].astype("Int64")

    d.to_csv(f"{a.outdir}/ghcnd-stations-with-age.csv", index=False)
    write_geojson(d, f"{a.outdir}/ghcnd-stations-with-age.geojson",
                  ["station_id", "name", "country_name", "network_name", "gsn_flag",
                   "first_year", "last_year", "record_years", "active",
                   "has_temp", "has_precip", "temp_record_years"])

    missing = int(d["first_year"].isna().sum())
    print(f"stations                 {len(d):,}")
    print(f"matched to inventory     {len(d)-missing:,}")
    print(f"no inventory record      {missing:,}")
    print(f"active (>= {ACTIVE_FROM})         {int((d['active']==1).sum()):,}")
    print(f"median record years      {d['record_years'].median()}")


if __name__ == "__main__":
    main()
