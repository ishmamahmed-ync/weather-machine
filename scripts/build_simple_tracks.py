"""
Turn an IBTrACS CSV into a simple storm-animation dataset.

Works on any ibtracs.*.list.v04r01.csv (ACTIVE, ALL, since1980, or a basin file).

    python build_simple_tracks.py <ibtracs.csv> <outdir> [--step 12]

Outputs
  storms.csv       one row per storm: spawn point, target point, end point, peak intensity
  storm_nodes.csv  one row per node at the chosen step, with bearing + km to the next node
  storm_tracks.geojson  one LineString per storm, dateline-safe
"""

import os, sys, json, argparse
import numpy as np
import pandas as pd

KEEP = [
    "SID", "SEASON", "BASIN", "SUBBASIN", "NAME", "ISO_TIME", "NATURE",
    "LAT", "LON", "WMO_WIND", "WMO_PRES", "TRACK_TYPE", "DIST2LAND", "LANDFALL",
    "IFLAG", "USA_WIND", "USA_PRES", "USA_SSHS",
    "TOKYO_WIND", "TOKYO_PRES", "REUNION_WIND", "REUNION_PRES",
    "BOM_WIND", "BOM_PRES", "NADI_WIND", "NADI_PRES", "WELLINGTON_WIND",
]

# Saffir-Simpson-ish buckets from 1-min sustained wind in knots.
CAT_BINS = [-np.inf, 33, 63, 82, 95, 112, 136, np.inf]
CAT_LABELS = ["td", "ts", "cat1", "cat2", "cat3", "cat4", "cat5"]


def load(path, step_hours, basin=None, since=None, chunksize=250_000, verbose=True):
    """Stream the file in chunks, discarding rows we will never use.

    Thinning is row-wise (it depends only on ISO_TIME and IFLAG), so it is safe
    to apply per chunk. This drops roughly three quarters of the rows before
    anything is held in memory, which is what makes a 331 MB input cheap.
    """
    head = pd.read_csv(path, nrows=0).columns.tolist()
    cols = [c for c in KEEP if c in head]
    kept, seen = [], 0

    # keep_default_na=False is essential: basin code "NA" is the North Atlantic,
    # and pandas would otherwise read the entire Atlantic basin as null.
    reader = pd.read_csv(
        path, skiprows=[1], usecols=cols, keep_default_na=False,
        na_values=[" ", "", "  ", "   "], low_memory=False, chunksize=chunksize,
    )
    for chunk in reader:
        seen += len(chunk)
        chunk["ISO_TIME"] = pd.to_datetime(chunk["ISO_TIME"], errors="coerce")
        chunk = chunk.dropna(subset=["SID", "ISO_TIME", "LAT", "LON"])
        if basin:
            chunk = chunk[chunk["BASIN"].isin(basin)]
        if since:
            chunk = chunk[pd.to_numeric(chunk["SEASON"], errors="coerce") >= since]
        chunk = drop_spurs(chunk)
        chunk = thin(chunk, step_hours)
        if len(chunk):
            kept.append(chunk)
        if verbose:
            print(f"  read {seen:,} rows -> kept {sum(len(k) for k in kept):,}", end="\r")

    if verbose:
        print()
    if not kept:
        raise SystemExit("no rows survived filtering - check --basin / --since")

    d = pd.concat(kept, ignore_index=True)
    for c in d.columns:
        if c.endswith(("_WIND", "_PRES")) or c in ("DIST2LAND", "LANDFALL", "USA_SSHS"):
            d[c] = pd.to_numeric(d[c], errors="coerce")
    return d


def drop_spurs(d):
    """Keep only primary tracks so no storm is drawn twice."""
    if "TRACK_TYPE" not in d.columns:
        return d
    tt = d["TRACK_TYPE"].astype(str).str.lower()
    return d[~tt.str.contains("spur", na=False)].copy()


def coalesce_intensity(d):
    """WMO first, then USA, then whichever regional agency has it."""
    wind_order = [
        "WMO_WIND", "USA_WIND", "TOKYO_WIND", "REUNION_WIND",
        "BOM_WIND", "NADI_WIND", "WELLINGTON_WIND",
    ]
    pres_order = ["WMO_PRES", "USA_PRES", "TOKYO_PRES", "REUNION_PRES", "BOM_PRES", "NADI_PRES"]

    def pick(cols):
        cols = [c for c in cols if c in d.columns]
        out = pd.Series(np.nan, index=d.index, dtype="float64")
        src = pd.Series(pd.NA, index=d.index, dtype="object")
        for c in cols:
            fill = out.isna() & d[c].notna()
            out[fill] = d.loc[fill, c]
            src[fill] = c.replace("_WIND", "").replace("_PRES", "").lower()
        return out, src

    d["wind_kt"], d["wind_src"] = pick(wind_order)
    d["pres_mb"], _ = pick(pres_order)
    d["category"] = pd.cut(d["wind_kt"], bins=CAT_BINS, labels=CAT_LABELS).astype(object)
    d.loc[d["wind_kt"].isna(), "category"] = None
    return d


def thin(d, step_hours):
    """Keep observed synoptic nodes at the requested spacing."""
    d = d.sort_values(["SID", "ISO_TIME"]).copy()
    hours = d["ISO_TIME"].dt.hour
    if step_hours % 6 == 0:
        d = d[hours % step_hours == 0]
    else:
        d = d[hours % 3 == 0]
    # IFLAG first char 'O' marks an observation rather than an interpolated fill.
    if "IFLAG" in d.columns and len(d):
        obs = d["IFLAG"].astype(str).str[0].eq("O")
        if obs.mean() > 0.2:       # only trust the flag if it is actually populated
            d = d[obs]
    return d


def unwrap_lon(lon):
    """Remove antimeridian jumps so a track is one continuous line."""
    lon = np.asarray(lon, dtype="float64")
    if len(lon) < 2:
        return lon
    out = lon.copy()
    shift = 0.0
    for i in range(1, len(lon)):
        step = lon[i] - lon[i - 1]
        if step > 180:
            shift -= 360
        elif step < -180:
            shift += 360
        out[i] = lon[i] + shift
    return out


def bearing_km(lat1, lon1, lat2, lon2):
    R = 6371.0088
    p1, p2 = np.radians(lat1), np.radians(lat2)
    dl = np.radians(lon2 - lon1)
    dp = p2 - p1
    a = np.sin(dp / 2) ** 2 + np.cos(p1) * np.cos(p2) * np.sin(dl / 2) ** 2
    km = 2 * R * np.arcsin(np.sqrt(np.clip(a, 0, 1)))
    y = np.sin(dl) * np.cos(p2)
    x = np.cos(p1) * np.sin(p2) - np.sin(p1) * np.cos(p2) * np.cos(dl)
    brg = (np.degrees(np.arctan2(y, x)) + 360) % 360
    return brg, km


def build_nodes(d, step_hours):
    frames = []
    for sid, s in d.groupby("SID", sort=False):
        s = s.sort_values("ISO_TIME").reset_index(drop=True)
        if len(s) < 2:
            continue
        s["step"] = np.arange(len(s))
        s["lon_unwrapped"] = unwrap_lon(s["LON"].values)
        brg, km = bearing_km(
            s["LAT"].values[:-1], s["lon_unwrapped"].values[:-1],
            s["LAT"].values[1:], s["lon_unwrapped"].values[1:],
        )
        s["bearing_to_next"] = np.append(brg, np.nan).round(1)
        s["km_to_next"] = np.append(km, np.nan).round(1)
        s["speed_kmh"] = (s["km_to_next"] / step_hours).round(1)
        s["km_cum"] = np.append(0, np.cumsum(km)).round(1)
        total = s["km_cum"].iloc[-1]
        s["t"] = (s["km_cum"] / total).round(4) if total > 0 else 0.0
        s["hours_from_spawn"] = (
            (s["ISO_TIME"] - s["ISO_TIME"].iloc[0]).dt.total_seconds() / 3600
        ).astype(int)
        frames.append(s)
    return pd.concat(frames, ignore_index=True)


def build_storms(nodes):
    rows = []
    for sid, s in nodes.groupby("SID", sort=False):
        s = s.sort_values("step")
        first, last = s.iloc[0], s.iloc[-1]
        landfalls = s[s["DIST2LAND"] == 0] if "DIST2LAND" in s else s.iloc[0:0]
        if len(landfalls):
            tgt, kind = landfalls.iloc[0], "landfall"
        elif "DIST2LAND" in s and s["DIST2LAND"].notna().any():
            tgt, kind = s.loc[s["DIST2LAND"].idxmin()], "closest_approach"
        else:
            tgt, kind = last, "track_end"
        peak = s.loc[s["wind_kt"].idxmax()] if s["wind_kt"].notna().any() else last
        rows.append({
            "sid": sid,
            "name": (first["NAME"] if pd.notna(first["NAME"]) else "UNNAMED"),
            "season": int(first["SEASON"]),
            "basin": first["BASIN"],
            "nodes": len(s),
            "spawn_time": first["ISO_TIME"],
            "spawn_lat": round(float(first["LAT"]), 3),
            "spawn_lon": round(float(first["LON"]), 3),
            "target_kind": kind,
            "target_time": tgt["ISO_TIME"],
            "target_lat": round(float(tgt["LAT"]), 3),
            "target_lon": round(float(tgt["LON"]), 3),
            "target_step": int(tgt["step"]),
            "end_lat": round(float(last["LAT"]), 3),
            "end_lon": round(float(last["LON"]), 3),
            "duration_h": int(last["hours_from_spawn"]),
            "track_km": float(last["km_cum"]),
            "peak_wind_kt": (None if pd.isna(peak["wind_kt"]) else int(peak["wind_kt"])),
            "peak_category": peak["category"],
            "peak_step": int(peak["step"]),
            "crosses_dateline": bool(
                (s["lon_unwrapped"].max() > 180) or (s["lon_unwrapped"].min() < -180)
            ),
        })
    return pd.DataFrame(rows)


def build_geojson(nodes, storms):
    meta = storms.set_index("sid").to_dict("index")
    feats = []
    for sid, s in nodes.groupby("SID", sort=False):
        s = s.sort_values("step")
        m = meta[sid]
        feats.append({
            "type": "Feature",
            "geometry": {
                "type": "LineString",
                "coordinates": [
                    [round(float(x), 3), round(float(y), 3)]
                    for x, y in zip(s["lon_unwrapped"], s["LAT"])
                ],
            },
            "properties": {
                "sid": sid, "name": m["name"], "season": m["season"],
                "basin": m["basin"], "peak_wind_kt": m["peak_wind_kt"],
                "peak_category": m["peak_category"], "duration_h": m["duration_h"],
            },
        })
    return {"type": "FeatureCollection", "features": feats}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("src")
    ap.add_argument("outdir")
    ap.add_argument("--step", type=int, default=12,
                    help="hours between nodes (default 12)")
    ap.add_argument("--basin", nargs="+", metavar="B",
                    help="limit to basins: NA EP WP NI SI SP SA")
    ap.add_argument("--since", type=int, metavar="YEAR",
                    help="only seasons from this year onward")
    ap.add_argument("--min-peak-wind", type=float, metavar="KT",
                    help="keep only systems whose lifetime peak wind reaches "
                         "this many knots (34 = tropical storm, 64 = hurricane)")
    ap.add_argument("--shuffle", action="store_true",
                    help="randomise storm order so a truncated import loses a "
                         "random sample rather than the most recent decades")
    ap.add_argument("--no-geojson", action="store_true")
    a = ap.parse_args()
    os.makedirs(a.outdir, exist_ok=True)

    print(f"reading {a.src}")
    d = coalesce_intensity(load(a.src, a.step, a.basin, a.since))
    nodes = build_nodes(d, a.step)
    storms = build_storms(nodes)

    if a.min_peak_wind is not None:
        before = len(storms)
        keep = storms["peak_wind_kt"].notna() & (storms["peak_wind_kt"] >= a.min_peak_wind)
        storms = storms[keep].reset_index(drop=True)
        nodes = nodes[nodes["SID"].isin(set(storms["sid"]))].reset_index(drop=True)
        print(f"peak-wind filter >= {a.min_peak_wind:g} kt: {before:,} -> {len(storms):,} storms")

    if a.shuffle:
        order = storms.sample(frac=1, random_state=7)["sid"].tolist()
        rank = {s: i for i, s in enumerate(order)}
        storms = storms.set_index("sid").loc[order].reset_index()
        nodes = nodes.assign(_r=nodes["SID"].map(rank)).sort_values(
            ["_r", "step"]).drop(columns="_r").reset_index(drop=True)

    out = nodes[[
        "SID", "step", "ISO_TIME", "hours_from_spawn", "LAT", "LON", "lon_unwrapped",
        "wind_kt", "pres_mb", "category", "wind_src", "NATURE", "DIST2LAND",
        "bearing_to_next", "km_to_next", "speed_kmh", "km_cum", "t",
    ]].rename(columns={
        "SID": "sid", "ISO_TIME": "time", "LAT": "lat", "LON": "lon",
        "NATURE": "nature", "DIST2LAND": "dist2land_km",
    })

    out.to_csv(f"{a.outdir}/storm_nodes.csv", index=False)
    storms.to_csv(f"{a.outdir}/storms.csv", index=False)
    if not a.no_geojson:
        with open(f"{a.outdir}/storm_tracks.geojson", "w") as f:
            json.dump(build_geojson(nodes, storms), f)

    print(f"storms      {len(storms):,}")
    print(f"nodes       {len(out):,}  (step {a.step}h)")
    print(f"seasons     {int(storms.season.min())} to {int(storms.season.max())}")
    print(f"dateline    {int(storms.crosses_dateline.sum()):,} storms unwrapped")
    for f in ("storm_nodes.csv", "storms.csv", "storm_tracks.geojson"):
        p = f"{a.outdir}/{f}"
        if os.path.exists(p):
            print(f"  {f:<22}{os.path.getsize(p)/1e6:7.1f} MB")


if __name__ == "__main__":
    main()
