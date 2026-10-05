#!/usr/bin/env python3
"""Layers the final page needs that the live site's packed data does not have.

    python3 scripts/pack_final_layers.py      (standard library only)

Writes final/story/layers/extra.json. scripts/build_all.py lays it over the story's base
data (site-src/layers/globe-data-land0.5-ocean1.json, the grid standard: land 0.5°,
ocean 1°), key by key, so a layer here replaces the base layer of the same name.

storms   The same 1,813 IBTrACS tracks (2006–2026, every 12-hourly observed fix) as the
         base layer, re-read from data/processed/storm_nodes.csv with each storm's
         season added (yr), and ordered by season, so slide 1 can draw them year by year.
         Checked here: every point and every peak category equals the base layer's.
af_decay Slide 19: Africa's weather stations on 0.5-degree land cells (GHCN-Daily, data/processed/
         ghcnd-stations-with-age.csv; "Africa" as in scripts/check_figures.py, the 2,119 stations). Per cell
         the first year any of its stations reports and the last year any does (y0, y); the slide lights a
         cell between the two as a year counter runs 1970 to 2025. A cell going dark means its records stop
         reaching the global archive, not necessarily that its stations closed (docs/NOTES.md, Menne 2012).
st_flicker  "Yet the world is pulling back": the 0.5-degree cells with a weather station reporting in 2024 or later
         in the countries the slide names (the United States, Russia, Ukraine, and Finland, Sweden and Denmark,
         the EU members of the Arctic Council). The slide makes them flicker: illustrative, not real outages.
st_low, st_arctic  Slide 21: the base weather-station grid (0.5 degrees) split at the Arctic Circle
         (66.56 N), so the Arctic stations can fade on their own. Together they are the base layer exactly.
"""
import collections, csv, json, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PROC = ROOT / "data/processed"
BASE = ROOT / "site-src/layers/globe-data-land0.5-ocean1.json"
OUT = ROOT / "final/story/layers/extra.json"
CAT = {"ts": 0, "cat1": 1, "cat2": 2, "cat3": 3, "cat4": 4, "cat5": 5}   # index into the Saffir-Simpson ramp


def wrap(lon):
    return round(((float(lon) + 180) % 360) - 180, 1)    # storm_nodes.csv runs past 180°E for some Pacific tracks


def storms():
    meta = {r["sid"]: r for r in csv.DictReader(open(PROC / "storms.csv", encoding="utf-8"))}
    tracks = collections.OrderedDict()
    for r in csv.DictReader(open(PROC / "storm_nodes.csv", encoding="utf-8")):
        tracks.setdefault(r["sid"], []).append(r)
    order = sorted(tracks, key=lambda s: (int(meta[s]["season"]), meta[s]["spawn_time"]))
    xy, ln, cat, yr = [], [], [], []
    for s in order:
        for r in tracks[s]:
            xy += [wrap(r["lon"]), round(float(r["lat"]), 1)]
        ln.append(len(tracks[s])); cat.append(CAT[meta[s]["peak_category"]]); yr.append(int(meta[s]["season"]))
    out = {"type": "tracks", "xy": xy, "len": ln, "cat": cat, "yr": yr}

    # the same tracks as the base layer, point for point
    base = json.load(open(BASE))["storms"]
    def bag(d):
        b, p = collections.Counter(), 0
        for n, c in zip(d["len"], d["cat"]):
            b[(c, tuple(d["xy"][2 * p:2 * (p + n)]))] += 1; p += n
        return b
    if bag(base) != bag(out):
        sys.exit("storms: the repacked tracks differ from the base layer; not writing")
    print(f"storms   {len(ln):,} tracks, {len(xy)//2:,} points, seasons {min(yr)}–{max(yr)}; identical to the base layer")
    return out


def af_decay():
    sys.path.insert(0, str(ROOT / "scripts"))
    from check_figures import AFRICA
    names, cells, n = set(AFRICA), {}, 0
    for r in csv.DictReader(open(PROC / "ghcnd-stations-with-age.csv")):
        if r["country_name"] not in names: continue
        lon, lat = float(r["lon"]), float(r["lat"]); n += 1
        k = (int((lon + 180) // 0.5), int((lat + 90) // 0.5))
        c = cells.setdefault(k, [9999, 0])
        c[0] = min(c[0], int(r["first_year"])); c[1] = max(c[1], int(r["last_year"]))
    keys = sorted(cells)
    xy = [v for (i, j) in keys for v in (round(i * 0.5 - 180 + 0.25, 2), round(j * 0.5 - 90 + 0.25, 2))]
    act = lambda y: sum(1 for k in keys if cells[k][0] <= y <= cells[k][1])
    print(f"af_decay: {n} African stations in {len(keys)} cells of 0.5 degrees; reporting cells "
          f"1970 {act(1970)}, 1980 {act(1980)}, 2000 {act(2000)}, 2025 {act(2025)}")
    return {"type": "timeline", "xy": xy, "y0": [cells[k][0] for k in keys], "y": [cells[k][1] for k in keys],
            "from": 1970, "to": 2025}


FLICKER = ("United States", "Russia", "Ukraine", "Finland", "Sweden", "Denmark")


def st_flicker():
    cells, n = set(), {}
    for r in csv.DictReader(open(PROC / "ghcnd-stations-with-age.csv")):
        c = r["country_name"]
        if c not in FLICKER or int(r["last_year"] or 0) < 2024: continue
        cells.add((int((float(r["lon"]) + 180) // 0.5), int((float(r["lat"]) + 90) // 0.5))); n[c] = n.get(c, 0) + 1
    keys = sorted(cells)
    print(f"st_flicker: {len(keys)} cells of 0.5 degrees, stations reporting 2024+: " + ", ".join(f"{k} {v}" for k, v in n.items()))
    return {"type": "points", "xy": [v for (i, j) in keys for v in (round(i * 0.5 - 180 + 0.25, 2), round(j * 0.5 - 90 + 0.25, 2))]}


def stations_split():
    sys.path.insert(0, str(ROOT / "scripts"))
    from regrid_layers import decode, encode, cell
    base = json.loads(BASE.read_text())["stations"]
    st = base["s"]; low, arc = {}, {}
    for lon, lat, n in decode(base):
        (arc if lat > 66.56 else low)[cell(lon, lat, st)] = n
    tot = sum(base["n"])
    assert sum(low.values()) + sum(arc.values()) == tot
    print(f"stations split at 66.56 N: {sum(arc.values())} of {tot} station counts north of the Arctic Circle "
          f"({len(arc)} cells)")
    return encode(low, st), encode(arc, st)


def main():
    OUT.parent.mkdir(parents=True, exist_ok=True)
    low, arc = stations_split()
    extra = {"storms": storms(), "af_decay": af_decay(), "st_low": low, "st_arctic": arc, "st_flicker": st_flicker()}
    OUT.write_text(json.dumps(extra, separators=(",", ":")))
    print(f"wrote {OUT.relative_to(ROOT)}  {OUT.stat().st_size/1e6:.2f} MB")


if __name__ == "__main__":
    main()
