"""Check every number on the final page's 24 slides.

    python3 scripts/check_figures.py        (from the repo root; standard library only)

Writes docs/FIGURES.md, a table of every figure with its source line and status, and
exits with an error if a figure that can be recomputed from the repo's data no longer
matches. The slide numbers and wording follow the author's narrative
(weather_machine_narrative_v3_short_1.txt, 5 Oct 2026); the sources follow the long
version (weather_machine_narrative_v3_LONG.txt) and the research dossier.

Status, one per figure:
  data       recomputed here from data/processed or the built pages; must match
  arithmetic the sum is redone here; the inputs come from the named source
  paper      quoted from the paper itself, by the author's rule (5 Oct 2026). The
             published data inside the map gives slightly different totals because
             some cells were cleaned; the report shows both, but the page quotes the paper
  cited      taken from the named source; not checkable from the repo
  unsourced  on the page, but no source is recorded yet
"""
import csv, json, math, re, statistics, sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PROC = ROOT / "data/processed"
R_EARTH = 6371.0088  # km, mean radius


# ---------- loaders (each read once) ----------
_cache = {}
def once(fn):
    def wrap():
        if fn.__name__ not in _cache: _cache[fn.__name__] = fn()
        return _cache[fn.__name__]
    return wrap

@once
def stations():
    return list(csv.DictReader(open(PROC / "ghcnd-stations-with-age.csv", encoding="utf-8")))

@once
def gauges():
    """The Su et al. Fig. 2c cells, as shipped inside the rain-gauge sections."""
    t = (ROOT / "prototypes/rain-gauges/rain-gauge-sections.html").read_text(encoding="utf-8")
    return json.loads(re.search(r'<script id="rg-DATA" type="application/json">(.*?)</script>', t, re.S).group(1))

@once
def floods():
    return [f["properties"] for f in json.load(open(PROC / "emdat-floods-2016-2026.geojson"))["features"]]

@once
def countries():
    return json.load(open(ROOT / "data/raw/ne_50m_admin_0_countries.geojson"))["features"]


# ---------- definitions the figures depend on ----------
# Africa = the African countries as GHCN names them (the five with no stations, Comoros,
# Djibouti, Sao Tome and Principe, Somalia and South Sudan, are absent from the file),
# plus Western Sahara and six French and British island territories off the coast.
AFRICA = ["Algeria", "Angola", "Benin", "Botswana", "Burkina Faso", "Burundi", "Cameroon", "Cape Verde",
          "Central African Republic", "Chad", "Congo (Brazzaville)", "Congo (Kinshasa)", "Cote D'Ivoire",
          "Egypt", "Equatorial Guinea", "Eritrea", "Ethiopia", "Gabon", "Gambia, The", "Ghana", "Guinea",
          "Guinea-Bissau", "Kenya", "Lesotho", "Liberia", "Libya", "Madagascar", "Malawi", "Mali",
          "Mauritania", "Mauritius", "Morocco", "Mozambique", "Namibia", "Niger", "Nigeria", "Rwanda",
          "Senegal", "Seychelles", "Sierra Leone", "South Africa", "Sudan", "Swaziland", "Tanzania", "Togo",
          "Tunisia", "Uganda", "Zambia", "Zimbabwe", "Western Sahara",
          "Reunion [France]", "Mayotte [France]", "Juan De Nova Island [France]", "Europa Island [France]",
          "Tromelin Island [France]", "Saint Helena [United Kingdom]"]
NOT_CONTIGUOUS = {"AK", "HI", "PR", "VI", "GU", "AS", "MP", "UM", ""}

def contiguous_us():
    return [s for s in stations() if s["country_name"] == "United States" and s["state"] not in NOT_CONTIGUOUS]

def africa_stations():
    names = set(AFRICA)
    return [s for s in stations() if s["country_name"] in names]


def ring_area(ring):
    """Area of a lon/lat ring on the sphere, km² (the same method as d3.geoArea, unsigned)."""
    s = 0.0
    for (x1, y1), (x2, y2) in zip(ring, ring[1:] + ring[:1]):
        s += math.radians(x2 - x1) * (2 + math.sin(math.radians(y1)) + math.sin(math.radians(y2)))
    return abs(s) * R_EARTH ** 2 / 2

def polys(f):
    g = f["geometry"]
    return [g["coordinates"]] if g["type"] == "Polygon" else g["coordinates"]

def land_area(features, keep=lambda ring: True):
    total = 0.0
    for f in features:
        for p in polys(f):
            if keep(p[0]): total += ring_area(p[0]) - sum(ring_area(h) for h in p[1:])
    return total


# ---------- the checks ----------
def c_archive():
    return len(stations())

def c_sats_2025():
    rows = list(csv.DictReader(open(ROOT / "prototypes/history/satellites_per_year.csv")))
    return int(next(r for r in rows if r["year"] == "2025")["all_in_operation"])

def c_argo_profiles():
    return sum(f["properties"]["profiles"] for f in json.load(open(PROC / "argo-density-1deg.geojson"))["features"])

def c_argo_floats():
    """Floats in the raw index, counting rows with a date and a valid position (the processed file's rule)."""
    import gzip
    floats = set()
    with gzip.open(ROOT / "data/raw/ar_index_global_prof.txt.gz", "rt") as f:
        for line in f:
            if line.startswith("#") or line.startswith("file,"): continue
            c = line.rstrip("\n").split(",")
            try: la, lo = float(c[2]), float(c[3])
            except ValueError: continue
            if c[1] and -90 <= la <= 90 and lo > -999: floats.add(c[0].split("/")[1])
    return len(floats)

def c_beira_center():
    d = json.load(open(ROOT / "prototypes/idai/idai-data.json"))["center"]
    return len(d["dmg"]) // 3

def c_us():
    return len(contiguous_us())

def all_us():
    return [s for s in stations() if s["country_name"] == "United States"]

def c_us_all():
    return len(all_us())

def c_us_share():
    return round(100 * len(all_us()) / len(stations()))

def c_af_cells(year):
    """Slide 19's counter: Africa's 0.5-degree cells with a station reporting in `year` (first <= year <= last)."""
    def f():
        names, cells = set(AFRICA), {}
        for r in csv.DictReader(open(PROC / "ghcnd-stations-with-age.csv")):
            if r["country_name"] not in names: continue
            k = (int((float(r["lon"]) + 180) // 0.5), int((float(r["lat"]) + 90) // 0.5))
            c = cells.setdefault(k, [9999, 0]); c[0] = min(c[0], int(r["first_year"])); c[1] = max(c[1], int(r["last_year"]))
        return sum(1 for a, b in cells.values() if a <= year <= b)
    return f


def c_africa():
    return len(africa_stations())

def c_land_ratio():
    af = land_area([f for f in countries() if f["properties"]["CONTINENT"] == "Africa"])
    us = land_area([f for f in countries() if f["properties"]["ADM0_A3"] == "USA"])
    return round(af / us, 2)

def c_moz():
    return sum(1 for s in stations() if s["country_name"] == "Mozambique")

def c_channel():
    """Argo profiles per unit ocean area in 35–45°E, 26–11°S against the whole ocean
    (cells with at least one profile, each weighted by its area, cos latitude)."""
    cells = [(f["geometry"]["coordinates"], f["properties"]["profiles"])
             for f in json.load(open(PROC / "argo-density-1deg.geojson"))["features"]]
    box = [(y, p) for (x, y), p in cells if 35 <= x <= 45 and -26 <= y <= -11]
    dens = lambda cs: sum(p for _, p in cs) / sum(math.cos(math.radians(y)) for y, _ in cs)
    return round(dens(box) / dens([(y, p) for (x, y), p in cells]), 2)

def c_per_cell():
    return round(max(gauges()["area"]) / 575, 1)

def c_map_gauges():
    return sum(gauges()["n"])

def c_map_meets():
    D = gauges(); cls = [0] * len(D["n"])
    for g, (s, e) in enumerate(D["groups"]):
        for i in range(s, e): cls[i] = g // 6
    ok = sum(1 for i, n in enumerate(D["n"]) if n and n / D["area"][i] * 1000 >= D["wmo"][cls[i]])
    return round(100 * ok / len(D["n"]), 1)

def c_map_cont(code):
    def f():
        D = gauges(); j = D["conts"].index(code); idx = []
        for g, (s, e) in enumerate(D["groups"]):
            if g % 6 == j: idx += range(s, e)
        return round(sum(D["n"][i] for i in idx) / sum(D["area"][i] for i in idx) * 1000, 2)
    return f

def c_flood_share(region, field):
    def f():
        rows = [r for r in floods() if r.get(field) not in (None, "")]
        tot = sum(float(r[field]) for r in rows)
        return round(100 * sum(float(r[field]) for r in rows if r["region"] == region) / tot, 1)
    return f

def c_mhews(year):
    return lambda: sum(1 for _ in csv.DictReader(open(PROC / f"sendai-g1-mhews-{year}.csv")))

def c_not_reported():
    total = sum(1 for _ in csv.DictReader(open(PROC / "sendai-g1-mhews.csv")))
    return total - c_mhews(2025)()


# Each figure: slide, what the page says, the value, status, the one-line source, and a
# check for 'data' (returns the recomputed value) or 'arithmetic' (returns the result).
# 'map' is what the published data inside the map gives, shown for 'paper' figures.
FIGURES = [
    # I · Setup
    (1, "recorded disasters rose nearly fivefold in fifty years", "×5", "cited",
     "WMO and UNDRR, Atlas of Mortality and Economic Losses, 1970–2019 (2021)", None),
    (1, "deaths fell almost threefold", "÷3", "cited",
     "WMO and UNDRR, Atlas of Mortality and Economic Losses, 1970–2019 (2021)", None),
    # II · The weather machine
    (5, "the US takes in three times the data it sends out", 3, "arithmetic",
     "NOAA NWS International Affairs: about 15.9 GB a day in, 5.4 GB out [E-06]", lambda: round(15.9 / 5.4)),
    (2, "card: 132,501 weather stations in the global archive", 132501, "data",
     "NOAA NCEI, GHCN-Daily, downloaded 19 Sep 2026", c_archive),
    (3, "card: 439 Earth-observing satellites in operation (2025)", 439, "data",
     "WMO OSCAR/Space, export 4 Oct 2026 (prototypes/history/satellites_per_year.csv)", c_sats_2025),
    (4, "card: 3,375,214 Argo profiles", 3375214, "data", "Argo GDAC index, 23 Sep 2026 (data/processed)", c_argo_profiles),
    (4, "card: from 20,530 floats", 20530, "data", "Argo GDAC index, 23 Sep 2026 (raw index, rows with a date and position)", c_argo_floats),
    (5, "card: 221,483 rain gauges sharing their records", 221483, "paper",
     "Su et al., Nature 652:119 (2026)", c_map_gauges),
    # III · The gaps
    (6, "the United States has 78,567 weather stations (Alaska and Hawaii included)", 78567, "data",
     "GHCN-Daily, checked 5 Oct 2026", c_us_all),
    (6, "59% of all on Earth", 59, "data", "GHCN-Daily", c_us_share),
    (6, "Africa, with more than three times the land", 3.18, "data",
     "Natural Earth 1:50m land areas (Africa against the whole US, Alaska and Hawaii included)", c_land_ratio),
    (6, "Africa has 2,119 stations", 2119, "data",
     "GHCN-Daily; Africa = African countries plus Western Sahara and six island territories", c_africa),
    (6, "636 radars for 1.1 bn (US and EU); 37 for 1.2 bn (Africa)", "636 / 37", "cited",
     "WMO figures cited by F. Otto, Yale Environment 360, 31 Oct 2023", None),
    (7, "the Channel gets a third of the global average density of Argo profiles", 0.35, "data",
     "Argo GDAC index, downloaded 23 Sep 2026 (profiles per unit area, 35–45°E, 26–11°S)", c_channel),
    (8, "WMO: about one rain gauge per 575 km² on open plains", 575, "cited", "WMO-No. 168, Table I.2.6", None),
    (8, "up to about 21 in every one-degree square", 21, "arithmetic",
     "largest 1° land cell in the Su et al. data, divided by 575 km²", lambda: int(c_per_cell())),
    (8, "only 13.4% of the world's land meets the standard", 13.4, "paper",
     "Su et al., Nature 652:119 (2026)", c_map_meets),
    (8, "Europe has 2.4 gauges per 1,000 km²", 2.4, "paper", "Su et al., Nature 652:119 (2026)", c_map_cont("EU")),
    (8, "Africa has 0.09", 0.09, "paper", "Su et al., Nature 652:119 (2026)", c_map_cont("AF")),
    # IV · Idai
    (10, "over 60% of its people live in low-lying coastal areas", "60%", "unsourced", "", None),
    (10, "just 19 of its weather stations reach the global archive", 19, "data", "GHCN-Daily", c_moz),
    (10, "much of the water that floods its rivers falls in its neighbours' highlands", "-", "cited",
     "ISET-International, Learning from Cyclones Idai and Kenneth (ReliefWeb) [W-4]", None),
    (11, "Desmond 21 Jan 2019; Idai 52 days later", 52, "arithmetic",
     "IBTrACS v04r01; landfall dates ISET [W-4]", lambda: (date(2019, 3, 14) - date(2019, 1, 21)).days),
    (11, "Kenneth 42 days after that", 42, "arithmetic",
     "IBTrACS v04r01; landfall dates ISET [W-4]", lambda: (date(2019, 4, 25) - date(2019, 3, 14)).days),
    (11, "never hit by so many cyclones in one season", "-", "unsourced", "", None),
    (12, "forecasters saw Idai coming five days ahead", 5, "cited", "ECMWF, 2019 [W-2]", None),
    (14, "1.85 million people affected", 1850000, "unsourced", "likely Government of Mozambique PDNA (2019)", None),
    (14, "603 deaths in Mozambique", 603, "unsourced", "likely Government of Mozambique PDNA (2019)", None),
    (14, "more than 1,000 across three countries", 1000, "cited", "Otto 2023 [I-17]; ECMWF [W-2]", None),
    (14, "map: central Beira, 8,705 buildings graded", 8705, "data",
     "Copernicus EMS EMSR348, Beira Center (33 destroyed, 2,968 damaged, 5,704 possibly; Copernicus's table: 33, 2,968, 5,705)", c_beira_center),
    (14, "122,700 destroyed, 111,200 damaged, 77 health facilities, 400,000 in shelters", "-", "unsourced",
     "likely Government of Mozambique PDNA (2019)", None),
    (15, "over 140,000 animals killed", 143422, "arithmetic",
     "124,498 birds + 10,305 sheep and goats + 5,428 cows + 3,191 pigs (author's Idai text; likely PDNA)",
     lambda: 124498 + 10305 + 5428 + 3191),
    (15, "124,498 birds, 10,305 sheep and goats, 5,428 cows, 3,191 pigs; US$3.1 million", "-", "unsourced",
     "likely Government of Mozambique PDNA (2019)", None),
    (16, "1,345 km of transmission lines, 10,216 km of distribution lines, 3,990 transformers, 30 substations", "-", "unsourced",
     "likely Government of Mozambique PDNA (2019)", None),
    # V · Who pays
    (17, "Africa has 27% of recorded flood deaths", 27.0, "data",
     "EM-DAT (CRED, UCLouvain), floods 2016–2026, export 18 Sep 2026", c_flood_share("Africa", "deaths")),
    (17, "Europe 1.5%", 1.5, "data", "EM-DAT floods 2016–2026", c_flood_share("Europe", "deaths")),
    (17, "damage: Europe 20.2%", 20.2, "data", "EM-DAT floods 2016–2026", c_flood_share("Europe", "damage_kusd")),
    (17, "damage: Africa 2.9%", 2.9, "data", "EM-DAT floods 2016–2026", c_flood_share("Africa", "damage_kusd")),
    # VI · Closing the gaps (the author's order, 5 Oct 2026)
    (19, "story card: river sensors give up to 72 hours' warning in Karonga, Malawi", 72, "cited", "UNICEF Malawi, 16 Jul 2024", None),
    (19, "story card: more than 70,000 Cyclone Preparedness Programme volunteers; Bhola (1970) killed at least 300,000", 70000, "cited",
     "American Red Cross, 29 May 2020", None),
    (19, "story card: an AI model found 11 million more people in flood zones, 69% above the official count", 11040000, "cited",
     "Wu, Zhang & Stouffs, Nature Communications 17:5983 (2026)", None),
    (21, "mortality at least six times lower with good early warning (Guterres)", 6, "cited",
     "A. Guterres, Early Warnings for All high-level event, 22 Oct 2025", None),
    (21, "about 90 countries still haven't reported a multi-hazard warning system", 90, "data",
     "Sendai Framework Monitor, Target G-1, fetched 28 Sep 2026 (195 countries less 105)", c_not_reported),
    (21, "map: 85 countries in 2022", 85, "data", "Sendai Framework Monitor, Target G-1", c_mhews(2022)),
    (21, "map: 105 countries in 2025", 105, "data", "Sendai Framework Monitor, Target G-1", c_mhews(2025)),
    (22, "LDCs and SIDS deliver 9% of the surface data WMO requires", 9, "cited",
     "WMO GBON Baseline 2023, SOFF Sixth Steering Committee", None),
    (22, "African weather-balloon reports fell by half, 2015 to 2020", 50, "cited", "WMO 2021 [I-05]; SOFF", None),
    (22, "map counter: 878 African 0.5° cells with a station reporting in 1970", 878, "data", "GHCN-Daily stations (pack_final_layers.py af_decay)", c_af_cells(1970)),
    (22, "map counter: 399 in 2025", 399, "data", "GHCN-Daily stations (pack_final_layers.py af_decay)", c_af_cells(2025)),
    (23, "the UN fund for their missing weather data is seeking US$400 million", 400e6, "cited",
     "SOFF Action Report 2025 [E-41][E-42]", None),
    (23, "the world spends that on its militaries in just over an hour", 1.2, "arithmetic",
     "SIPRI: US$2,887 billion in 2025 [E-72]", lambda: round(400e6 / (2887e9 / (365 * 24)), 1)),
    (23, "dial: one hour of world military spending is about US$330 million", 330, "arithmetic",
     "SIPRI: US$2,887 billion in 2025, over 8,760 hours", lambda: round(2887e3 / 8760 / 10) * 10),
    (23, "every dollar invested returns more than 25", 25, "cited", "World Bank, via WMO 2021 [I-05]", None),
    (24, "US: fewer balloons, FEWS NET suspended, exit from 66 bodies, NOAA cut by a quarter proposed", "-",
     "cited", "[E-13][E-14] balloons; [E-12] FEWS NET; [E-01]–[E-03] withdrawals; [I-16][E-17][E-18][E-20] budgets", None),
    (24, "war has destroyed or cut off a quarter of Ukraine's observing network", "25%", "cited",
     "Proceedings, 15th Int. Conf. 'Monitoring', EAGE 2023 [W-6] (losses since 2014)", None),
    (24, "EUMETSAT and the Arctic Council suspended cooperation with Russia", "-", "cited",
     "Reuters, 22 Mar 2022 [W-5]; Scientific American / E&E News [W-7]", None),
    (25, "'an existential problem of planetary proportions' (ICJ)", "-", "cited",
     "ICJ advisory opinion, 23 Jul 2025 [E-63][E-64] (quote via [E-65]; check the opinion's own text)", None),
    (26, "TAHMO: more than 600 stations in over 20 African countries, aiming for 20,000", 600, "cited",
     "TU Delft; METER Group case study", None),
    (26, "HOT volunteers mapped over 200,000 buildings after Idai", 200000, "cited",
     "HOT, 'Maps in action: how maps help the aid response for Cyclone Idai'; OSM wiki, Cyclone Idai", None),
]


def close(a, b):
    if isinstance(b, float) or isinstance(a, float):
        return abs(a - b) <= max(0.05, 0.01 * abs(b))
    return a == b

def fmt(v):
    if isinstance(v, float) and v.is_integer() and v > 1000: v = int(v)
    return f"{v:,}" if isinstance(v, int) else str(v)


def main():
    rows, failed = [], 0
    for slide, says, value, status, source, check in FIGURES:
        got, note = "", ""
        if check:
            got = check()
            if status in ("data", "arithmetic"):
                ok = close(got, value)
                if not ok: failed += 1
                note = "✅" if ok else f"❗ recomputed {fmt(got)}"
            elif status == "paper":
                note = f"map data gives {fmt(got)} (cleaned cells); the page quotes the paper"
        elif status == "unsourced":
            note = "⚠️ needs a source"
        rows.append((slide, says, fmt(value), status, source or "–", note))
        print(f"{slide:>2}  {status:<10} {fmt(value):>12}  {note or '-'}  · {says}")

    counts = {s: sum(1 for r in rows if r[3] == s) for s in ("data", "arithmetic", "paper", "cited", "unsourced")}
    md = ["# Figures on the final page",
          "",
          "*Generated by `scripts/check_figures.py`; do not edit by hand. Slides follow the author's",
          "narrative (v3 short, 5 Oct 2026); sources follow the long version and the research dossier.*",
          "",
          "Status: **data** recomputed from the repo and must match · **arithmetic** redone here ·",
          "**paper** quoted from the paper (the author's rule; the map's cleaned data differs slightly) ·",
          "**cited** from the named source, not checkable here · **unsourced** needs a source.",
          "",
          "Totals: " + " · ".join(f"{k} {v}" for k, v in counts.items()) + f" · **failed {failed}**",
          "",
          "| Slide | On the page | Value | Status | Source | Check |",
          "|---|---|---|---|---|---|"]
    md += [f"| {s} | {t} | {v} | {st} | {src} | {n} |" for s, t, v, st, src, n in rows]
    (ROOT / "docs/FIGURES.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    print(f"\n{len(rows)} figures: " + ", ".join(f"{v} {k}" for k, v in counts.items()) + f"; {failed} failed")
    print("wrote docs/FIGURES.md")
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
