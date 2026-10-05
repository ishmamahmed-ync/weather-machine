#!/usr/bin/env python3
"""Generate docs/NARRATIVE.md: the story so far, in text.

    python3 scripts/build_narrative.py

Scene text (main site SCENES), Idai slides and the stories are copied from their
source files; the notes on each scene (sources, checks, open questions) are written
by hand in NOTE below. Rerunning OVERWRITES docs/NARRATIVE.md, so put your own
writing elsewhere, or edit the hand-written parts here.
"""
import re, html, json
from pathlib import Path
R = Path(__file__).resolve().parent.parent

def clean(h):
    h = re.sub(r'\s+', ' ', h)                      # source line wraps are not line breaks
    h = re.sub(r'<span style="[^"]*">(.*?)</span>', r'\1', h)   # coloured words stay inline
    h = re.sub(r'</b>\s*<span>', ' ', h)            # stat number then its label: "603 deaths"
    h = re.sub(r'</b>', ': ', h)                     # bold lead-in: "21 January 2019: Tropical Storm..."
    h = re.sub(r'</span>', '\n', h)                 # kickers and stat lines end a line
    h = re.sub(r'<br\s*/?>', '\n', h); h = re.sub(r'</p>|</div>|</h1>', '\n', h)
    h = re.sub(r'<small>', ' ', h); h = re.sub(r'<[^>]+>', '', h); h = html.unescape(h)
    lines = [re.sub(r'\s+', ' ', l).strip() for l in h.split('\n')]
    return [l for l in lines if l]

# ---------------- main site scenes ----------------
t = (R / "site-src/template.html").read_text()
a = t.index('const SCENES'); b = t.index('\n];', a)
objs = re.split(r'\n\s*(?://[^\n]*\n\s*)*\{\s*(?=center)', t[a:b])[1:]
LAYER = {"stations": "weather stations", "argo": "Argo floats", "seals": "seal profiles", "sharks": "shark sightings (NW Atlantic)",
         "telemetry": "tracked animals", "coldspots": "Argo coldspots", "turtles": "turtles", "mhews_2022": "early warning 2022",
         "mhews_2025": "early warning 2025", "fl_affected": "flood: people affected", "fl_deaths": "flood: deaths",
         "michael": "Hurricane Michael track", "haiyan": "Typhoon Haiyan track", "storms": "all storm tracks 2006–2026",
         "sats_shell": "satellite shell (illustrative)"}
def scene(o):
    c = re.search(r'center:\s*\[([^\]]*)\]', o).group(1)
    z = re.search(r'zoom:\s*([\d.]+)', o).group(1)
    L = re.search(r'layers:\{([^}]*)\}', o)
    lay = [(k, float(v)) for k, v in re.findall(r'(\w+):\s*([\d.]+)', L.group(1))] if L else []
    wipe = re.search(r"wipe:\s*'(\w+)'", o)
    kind = 'quote' if re.search(r'\bquote\s*:', o) else 'bare' if re.search(r'\bbare\s*:', o) else 'card'
    lon, lat = [float(x) for x in c.split(',')]
    return dict(lines=clean(re.search(r'html:`(.*?)`', o, re.S).group(1)), lon=lon, lat=lat, zoom=z, layers=lay,
                wipe=wipe.group(1) if wipe else None, kind=kind, photo=bool(re.search(r'\bphoto\s*:', o)))
S = [scene(o) for o in objs]

def place(lon, lat): return f"{abs(lon):g}°{'E' if lon >= 0 else 'W'}, {abs(lat):g}°{'N' if lat >= 0 else 'S'}"

# hand-written notes per scene: numbers, sources, verification status
V, U, F = "✅", "⚠️", "❗"      # verified / no source recorded / differs or flagged
NOTE = {
 0: [],
 1: [f"{V} Weather stations layer: GHCN-Daily, 132,501 stations (NOAA NCEI, downloaded 19 Sep 2026)."],
 2: [f"{U} The satellite shell's dots are illustrative positions (caveat removed from screen 28 Sep; see NOTES.md).",
     "Real counts now exist: WMO OSCAR/Space, 2 weather satellites working in 1960, 26 in 1990, 47 in 2025; all Earth-observing 3 / 43 / 439 (history prototype)."],
 3: [f"{V} 3,375,214 profiles, 20,530 floats: Argo GDAC index, downloaded 23 Sep 2026.",
     f"{U} \"since 1999\": the Argo programme began in 1999, but the index holds profiles from 1997."],
 4: [],
 5: [f"{V} 76,708 contiguous-US stations; 59% (59.3%) of all; 51,229 CoCoRaHS volunteer gauges since 1998 (corrected from 53,167). Checked 28 Sep.",
     f"{F} \"So many they merge into a solid surface\" depends on the 0.25° grid. At the proposed 1° land grid this stops being true; at 0.5° it mostly holds."],
 6: [f"{F} 2,166 stations: not reproducible from a country list (2,119 with island territories). Median record 68 yr in the copy, 69 recomputed; US median 8 ✅. Record how \"Africa\" was defined.",
     f"{V} \"The network is shrinking\": defensible only as the archive (Menne et al. 2012). Stations stop *reporting to the archive*; see Notes."],
 7: [f"{V} 11 million people (11.04 M, +69%) and 4.1 million buildings (4.12 M, +81%): Wu, Zhang & Stouffs 2026, *Nature Communications* 17:5983.",
     f"{F} The US flood dots are sampled from a blurred density of AlphaGeo screenshots: **illustrative**. CLAUDE.md requires the word on screen; it was removed 28 Sep."],
 8: [f"{U} \"Mozambique has no national flood map\": no source recorded."],
 9: [],
 10: [f"{V} 125 knots, both storms: IBTrACS `storms.csv`.", f"{U} 74 deaths: no source recorded (NHC's report splits US direct and indirect deaths; 74 likely includes Central America)."],
 11: [f"{U} 6,352 deaths, 1,071 missing; US$25.5 bn (Michael) vs US$2.98 bn (Haiyan): no source recorded."],
 12: [f"{V} 636 radars (US and EU, 1.1 bn people) vs 37 (Africa, 1.2 bn): Otto 2023, *Yale Environment 360*.",
      f"{U} \"24 hours of warning cuts disaster damage by about 30%\": no source recorded (usually Global Commission on Adaptation 2019)."],
 13: [f"{V} 19 stations (16 active, 14 with 30+ years): GHCN-Daily, checked 28 Sep.", f"{U} 34 million people: no source recorded.",
      f"{V} \"A third of the global average\" Argo density: rechecked 4 Oct, 0.35× (35–45°E, 26–11°S).", f"{U} Upstream Limpopo gauges \"Mozambique doesn't own\": no source recorded."],
 14: [f"{U} \"55% of the built-up area in this frame ends up underwater\": method not recorded. Imagery georeferenced to ~1 km (Notes)."],
 15: [f"{V} Africa 27.0% of flood deaths, Europe 1.5%: EM-DAT floods 2016–2026, 1,680 events. Damage inverts it (Europe 20.2%, Africa 2.9%).",
      "Only 12% of events have EM-DAT's own coordinates; 46% are placed at country centroids (caveat removed from screen)."],
 16: [f"{V} −50% African radiosonde reports 2015–2020: SOFF. 9% surface / 13% upper-air of required stations in LDCs and SIDS: WMO GBON Baseline 2023."],
 17: [f"{V} Guterres, remarks to the Early Warnings for All high-level event, 22 Oct 2025."],
 18: [f"{V} 85 countries: Sendai Framework Monitor, Target G-1, fetched 28 Sep 2026 (\"as of\" rule).",
      f"{F} The *Global Status of MHEWS* report says 95 for 2022. Quote each number with its own source; never mix (Notes)."],
 19: [f"{V} 105 countries (report says 119). Same rule as above. China, India, Germany and Spain have never filed G-1, so they show as having none."],
 20: [f"{V} GBON (2021) is the first actual obligation to share; all 193 WMO members adopted it."],
 21: [f"{F} 74% of profiles south of 65°S: recomputed 4 Oct as 75.7% (151,967 seal vs 48,821 Argo). The seal download is 61% of MEOP, so the true share is likely higher.",
      "MEOP-CTD, downloaded 23 Sep 2026; cite Roquet et al. 2014, Treasure et al. 2017."],
 22: [f"{V} McDonnell, Kirtman, Braun & Hammerschlag 2026, *npj Clim Atmos Sci* 9:147. The map shows OBIS shark **sightings**, not the 29 tagged sharks."],
 23: [f"{V} 315 species, 12,735 cells of 1°: OBIS-SEAMAP, downloaded 23 Sep 2026. Location only, no environmental data."],
 24: [f"{F} This is the project's own proposal. Published support now found: March et al. 2020, *Global Change Biology* 26:586–596 (Argo coldspots 18.6% of the ocean; 183 species could fill them). Consider citing it here.",
      f"{V} Zero seal cells in the Channel; 28 loggerhead and 5 leatherback cells inside it (Notes)."],
 25: [],
 26: [f"{V} US$2.7 trillion: Gartner, Sep 2026. US$3.1 bn over five years: the UN Early Warnings for All plan. \"Less than half a day\": corrected from \"two days\" (Notes)."],
 27: [f"{V} Bratton, *Planetary Sapience*, Noema."],
 28: [],
}
ACTS = [(0, "Act 1 · The machine", "How humanity learned to watch the weather, and the three instruments the piece follows."),
        (5, "Act 2 · Rich and poor views", "The same machine sees some places far better than others; AI widens the gap."),
        (9, "Act 3 · The cost", "What happens to a place that can't see the weather coming."),
        (17, "Act 4 · What works", "Early warning saves lives, and coverage is slowly growing."),
        (21, "Act 5 · Creative responses", "Scientists already measure the ocean with animals; the limits of clever fixes."),
        (26, "Act 6 · Money and purpose", "The cost of the fix against what we spend on computation; what we need.")]

out = []
w = out.append
w("# The Gaps in the Weather Machine: narrative so far\n")
w("*Snapshot of 5 October 2026. Everything built so far, in text: the argument, every scene of the main piece, the five prototypes, the datasets behind them, every number with its source, and what is still open. Scene text and story text are copied from the source files, not retyped.*\n")
w("Legend for the notes: ✅ checked against data or a source · ⚠️ no source recorded yet · ❗ differs, flagged or needs a decision.\n")
w("## Contents\n\n1. The argument\n2. The main piece, scene by scene\n3. The prototypes (five)\n4. Datasets\n5. Corrections already made\n6. Literature\n7. Open questions\n")

w("## 1. The argument\n")
w("**Title:** The Gaps in the Weather Machine. **Subtitle:** Who can see the storm coming, and who can't.\n")
w("**Thesis.** The planet's observing apparatus (weather stations, satellites, ocean floats) is unevenly distributed. The gap has consequences measurable in lives. The shortfall is now less about instruments than about what countries share and what we choose to spend on.\n")
w("**The data-sharing argument, as it now stands.** Sharing daily climate data was never required. Most countries donated their history to the global archive once, and the archive decays as those donations age (Menne et al. 2012). GBON (2021) is the first actual obligation, and compliance sits at 9% of required surface stations in least developed countries and small island states. Africa's radiosonde reports to global models fell about 50% between 2015 and 2020, a genuine decline in transmission.\n")
w("**What the piece must not say.** \"We are not measuring less, we are sharing less\" was written and withdrawn: it fitted the shape of the data but not the explanation (Notes). A gap in the archive is not a gap in instruments: Somalia's zero means no data reaches NOAA, not that Somalia owns no thermometers.\n")
w("**Framing device discussed, not built:** the AMOC. The RAPID array has measured the Atlantic overturning since 2004; McCarthy et al. (*GRL* 2025) find the trend won't reach unfamiliar signal-to-noise until the 2040s. Use as opening frame and closing statistic only, and keep claims on detection, not collapse.\n")
w("**Arc.** 1 The machine → 2 Rich and poor views → 3 The cost → 4 What works → 5 Creative responses → 6 Money and purpose.\n")

w("## 2. The main piece, scene by scene\n")
w(f"Live at https://ishmamahmed-ync.github.io/weather-machine/ · source `site-src/template.html` (`SCENES`). **{len(S)} scenes**. Story mode scrolls through them; Explore mode lets the reader drag, zoom and toggle 24 layers.\n")
acts = {i: (t, d) for i, t, d in ACTS}
for i, s in enumerate(S):
    if i in acts:
        w(f"### {acts[i][0]}\n\n*{acts[i][1]}*\n")
    L = s["lines"]; title = L[0]; rest = L[1:]
    w(f"#### Scene {i} · {title}\n")
    if rest:
        w("\n".join(f"> {l}" for l in rest) + "\n")
    bits = []
    if s["layers"]: bits.append("Globe: " + ", ".join(f"{LAYER.get(k, k)}" + ("" if v >= 0.5 else " (faint)") for k, v in s["layers"]))
    if s["wipe"]: bits.append("before/after wipe" + (" (US flood maps)" if s["wipe"] == "us" else " (Lower Limpopo imagery)" if s["zoom"] == "52" else ""))
    if s["photo"]: bits.append("photo: instrumented seal")
    bits.append(f"centred {place(s['lon'], s['lat'])}, zoom {s['zoom']}")
    bits.append({"quote": "large pull quote", "bare": "narration, no card", "card": "card"}[s["kind"]])
    w("*" + " · ".join(bits) + "*\n")
    for n in NOTE.get(i, []):
        w(f"- {n}")
    w("")

# ---------------- prototypes ----------------
w("## 3. The prototypes\n")
w("All in `prototypes/`, styled like the main site, each one self-contained.\n")

w("### 3.1 Country profile: \"Pick your country and year of birth\" (`country-profile/globe.html`)\n")
w("The reader picks their country, year of birth and a reference country. The page totals what weather and climate disasters have cost their country in their lifetime, compares it with the reference, and shows their country on the globe with its rain-gauge coverage.\n")
w("> In the N years since you were born, floods have killed X people in C, affected Y and forced people from their homes Z times.\n")
w("- Four horizontal bars on one shared scale (the largest of the eight values fills the width): deaths, affected, at risk of a 1-in-100-year flood, displacements. Yours solid, reference outlined. Flood / Others toggle.\n- Globe: rain gauges and weather stations reporting in 2025–26; bar: gauges shared vs the WMO threshold (one per 575 km²).\n- Data: EM-DAT 2000–2025 (deaths, affected); IDMC GIDD 2008–2025 (displacements, which are movements, not people); Rentschler et al. 2022 *Nat Commun* 13:3527 (people exposed to a 1-in-100-year flood, 1.81 bn total, matches the paper); GHCN-Daily (gauges shared with the archive, not all gauges operated: Belgium shows 0); WMO-No. 168 (threshold, a simplification).\n- ✅ IDMC rows reproduce 2,301 of 2,302 published country-year totals.\n- Open: a GBON threshold for stations; EM-DAT from 1960 for whole lifetimes; per-capita rates. Rain gauges currently share Argo's blue; they move to the system's gauge green, and the dots to 0.5° cells (decided 5 Oct).\n")

w("### 3.2 Idai: a scroll story of Mozambique's 2019 cyclone season (`idai/idai.html`)\n")
w("Eight full-screen slides; one globe that flies from the corner into Mozambique's maps and back. Text is the author's (`Idai_text.rtf`).\n")
it = (R / "prototypes/idai/template.html").read_text()
sa = it.index('const SLIDES'); sb = it.index('\n];', sa)
for j, m in enumerate(re.finditer(r'html:`(.*?)`', it[sa:sb], re.S), 1):
    L = [l for l in clean(m.group(1)) if l != "Scroll or press space"]
    w(f"**Slide {j}.** " + " / ".join(L) + "\n")
w("- Sources: storm tracks IBTrACS v04 ✅ (categories match Saffir-Simpson for each wind); flood extent UNOSAT Sentinel-1, 13–20 Mar 2019 ✅ (area within 0.4%); before/after NASA MODIS via GIBS ✅ (public domain); Beira damage Copernicus EMS EMSR348 ✅ (16,333 graded buildings, checked against Copernicus's table).")
w(f"- ⚠️ Impact figures (1.85 million, 603, houses, clinics, 400,000, livestock, energy): the author's text, not independently verified; likely the Government of Mozambique PDNA. Cite before publishing.")
w(f"- ❗ \"Category 4\" for Idai and Kenneth: IBTrACS (10-min winds) peaks at Category 3; Category 4 is JTWC's 1-minute rating. The track colours show Cat 3. Pick one convention.")
w(f"- ❗ \"51 days later\": 21 Jan to 14 Mar is 52 days. 603 deaths is Mozambique only (1,000+ across Mozambique, Zimbabwe, Malawi).")
w(f"- ❗ Photo credits are blank; the photos look like agency images. Clear licences before the repo is public.\n")

w("### 3.3 A century of watching (`history/history.html`)\n")
w("One scene in three chapters. Each plays at 1.5 seconds per decade, then waits for space or scroll. All layers stay at full strength.\n")
w("| Chapter | Years | What appears |\n|---|---|---|\n| 1 · On the ground: Weather stations | 1900–1960 | Stations whose daily records reached the global archive, decade by decade (0.5° cells) |\n| 2 · From orbit: Satellites | 1960–1990 | Every weather and Earth-observation satellite in WMO OSCAR, real counts; positions random |\n| 3 · In the ocean: Argo floats | 1990–2025 | 1° ocean cells lit from first to last profile |\n")
w("| Year | Stations with data in the decade | Satellites working (all OSCAR / weather only) | Argo 1° cells lit |\n|---|---|---|---|")
for y, st, sa_, sw_, ar in [(1900, "13,635", "–", "–", "–"), (1960, "43,722", "3", "2", "–"), (1970, "45,462", "21", "15", "–"),
                            (1990, "40,792", "43", "26", "–"), (2000, "51,450", "88", "28", "1,270"), (2010, "65,288", "153", "33", "31,626"),
                            (2020, "56,928 (2020s)", "322", "39", "33,417"), (2025, "56,928 (2020s)", "439", "47", "29,403")]:
    w(f"| {y} | {st} | {sa_} / {sw_} | {ar} |")
w("")
w("- ❗ The dip from the 1970s (45,462) to the 1990s (40,792) is the archive, not stations closing (Menne et al. 2012). The on-screen fine print says so; keep it.\n- Ocean measurements before Argo (ships, buoys, XBTs) are not shown, and the page says so.\n- Satellites: OSCAR export 4 Oct 2026, 1,052 rows → 858 that flew (871 spacecraft). Weather-only subset cross-checked against CelesTrak (~46 vs 45 working today).\n- Panel copy for chapters 2 and 3 is placeholder.\n")

w("### 3.4 Stories of resilience (`stories/stories.html`)\n")
st = json.loads((R / "prototypes/stories/stories.json").read_text())
w(f"**Title:** {st['title']}  \n**Subtitle:** {st['subtitle']}\n")
w("One scene: the globe on the right with a circle per story; the page opens on the first story and **Next** steps through them. Animal stories fade in their map layers. Descriptions were written from each source article on 4 Oct 2026.\n")
names = {"animals": "Sensing with animals", "flood": "Flood and cyclone early warning (the spreadsheet, plus Bangladesh added 5 Oct)", "hope": "Stories of hope (from the text file)"}
for grp in ("animals", "flood", "hope"):
    w(f"**{names[grp]}**\n")
    for s in [x for x in st["stories"] if x["list"] == grp]:
        lay = ""
        if s.get("layers"): lay = " Map: " + ", ".join(st["layerStyles"][l["key"]]["label"] for l in s["layers"]) + "."
        w(f"- **{s['title']}** ({s['place']}). {s['description']} *{s['source']}, {s['date']}.*{lay} <{s['url']}>")
    w("")
w("- ❗ Fit with the title: the flood stories fit \"least responsible … coping\" and the lack-of-data brief; several hope stories (South Australia, the EU, US right whales, Dorset puffins, the Tulane mangrove study) and the three animal stories are about wealthy places or programmes.\n- ❗ Yangtze headline says \"four-year fishing ban\"; the source describes a 10-year ban from 2021.\n- The subtitle is unfinished (\"are …\"). Photos are placeholders; licences not cleared.\n")

w("### 3.5 Rain gauge density: map and explorer (`rain-gauges/rain-gauge-sections.html`)\n")
w("Two scenes meant to follow the story's last scene. Kept for the final build; integration instructions in `INTEGRATION.md`. **Rain (precipitation) gauges, not flood or stream gauges.**\n")
w("1. **Rain gauge density.** The earth alone: one dot per 0.5° land cell, coloured by gauges per 1,000 km² in eight classes (no gauge, under 0.1, up to 10 or more). Each 1° source cell is drawn as four dots with the same value, so this adds no information beyond 1°.\n2. **Rain gauge density against the WMO minimum.** Terrain tabs (Plains, Hilly, Mountains, Coastal, Islands, Urban, Polar/Arid); one square per 1° cell, plotted by continent against that terrain's WMO minimum, linked to the globe. Green meets the minimum, faint green falls short, grey has no gauge.\n")
w("- ✅ Su et al. 2026, *Nature* 652:119–125, Fig. 2c, rebuilt from the published data (Zenodo 10.5281/zenodo.18364510, CC BY 4.0). 15,263 land cells; 8,303 with a gauge. Plains: 2,320 of 4,130 cells have a gauge; WMO minimum 1.74 per 1,000 km². Africa's Plains average 0.086, below the minimum, with 63% of cells empty.\n- Decided 5 Oct: the design system adopts this page's greens (`--wm-gauge`).\n")

# ---------------- datasets ----------------
w("## 4. Datasets\n")
w("Full detail, links and licences in `docs/SOURCES.md`; problems in `docs/NOTES.md`.\n")
w("| Dataset | Who | Downloaded | Size used | What it shows | Used in |\n|---|---|---|---|---|---|")
rows = [
 ("GHCN-Daily station list + inventory", "NOAA NCEI", "19 Sep 2026", "132,501 stations; 7,966 with a WMO id", "Stations whose data reached the archive, with first/last year", "Main (most scenes), country profile, history"),
 ("ISD station history", "NOAA", "19 Sep 2026", "28,095 stations", "Second station archive; disagrees with GHCN (Belgium 1 vs 52)", "Comparison only"),
 ("Argo global profile index", "Argo GDAC (Coriolis)", "23 Sep 2026", "3,375,214 profiles, 20,530 floats, 36,674 1° cells", "Ocean temperature/salinity profiles", "Main, history, stories"),
 ("Argo coldspots", "this project", "–", "26 patches, 48.1 million km²", "Under-sampled ocean (script not in repo)", "Main scene 13 and 24, stories"),
 ("MEOP-CTD", "MEOP consortium", "23 Sep 2026", "545,596 profiles; 108 of 233 deployments (61%)", "Seal-borne ocean profiles", "Main scene 21, stories"),
 ("OBIS-SEAMAP", "Duke MGEL", "23 Sep 2026", "315 species, 12,735 1° cells; 16 shark species", "Where tracked animals go (location only)", "Main scenes 22–24, stories"),
 ("Shark ocean-sensing programmes", "hand-compiled from 3 papers", "–", "3 features", "Where sharks have carried ocean sensors", "Reference"),
 ("IBTrACS v04r01", "NOAA NCEI", "23 Sep 2026", "1,813 storms 2006–2026, 26,606 nodes", "Storm tracks and intensity", "Main scenes 10–11, Idai"),
 ("EM-DAT floods", "CRED, UCLouvain", "18 Sep 2026", "1,680 events 2016–2026", "Flood deaths, affected, damage", "Main scene 15"),
 ("EM-DAT weather/climate disasters", "CRED", "3 Oct 2026", "2000–2025", "Lifetime disaster totals", "Country profile"),
 ("IDMC GIDD events", "IDMC", "Oct 2026", "2008–2025, one file per year", "Internal displacements", "Country profile"),
 ("Rentschler et al. 2022 SI", "Nat Commun 13:3527", "Oct 2026", "188 countries, 1.81 bn people", "Exposure to 1-in-100-year floods", "Country profile"),
 ("Sendai Framework Monitor, Target G-1", "UNDRR", "28 Sep 2026", "195 countries; 85 (2022), 105 (2025)", "Countries reporting a multi-hazard early warning system", "Main scenes 18–19"),
 ("WMO OSCAR/Space", "WMO", "4 Oct 2026", "1,052 rows → 871 spacecraft", "Earth-observing satellites, launch to end of life", "History"),
 ("UNOSAT flood extent", "UNOSAT via HDX", "Oct 2026", "Sentinel-1, 13–20 Mar 2019", "Idai flood extent", "Idai"),
 ("Copernicus EMS EMSR348", "European Union", "Oct 2026", "16,333 graded buildings", "Beira building damage", "Idai"),
 ("NASA MODIS (GIBS)", "NASA", "Oct 2026", "24 Feb and 21 Mar 2019", "Before/after imagery", "Idai"),
 ("Wu, Zhang & Stouffs 2026 flood layer", "via AlphaGeo screenshots", "–", "illustrative dots", "AI-completed US flood maps", "Main scene 7"),
 ("Lower Limpopo before/after", "satellite composites", "–", "georeferenced to ~1 km", "Xai-Xai flooding", "Main scene 14"),
 ("Su et al. 2026, Fig. 2c data", "Nature 652:119; Zenodo, CC BY 4.0", "Oct 2026", "15,263 1° land cells, 8,303 gauged", "Rain gauges per 1,000 km² against the WMO minimum by terrain", "Rain gauge prototype"),
 ("Natural Earth", "public domain", "28 Sep 2026", "1:50m and 1:110m", "Land and country shapes", "All"),
]
for r in rows: w("| " + " | ".join(r) + " |")
w("\n**Evaluated and rejected:** GDIS (no geometry for Kiribati, the Maldives or the Marshall Islands, exactly the states the argument concerns); `ish-history.csv` (a deprecation notice, not data).\n")
w("**Structural limits to state somewhere:** EM-DAT records only events that cross an administrative threshold. GHCN-Daily counts stations whose data reaches NOAA, not national infrastructure. Flood deaths and damage have different coverage (1,243 vs 406 events). The MEOP download is 61% of all seal profiles.\n")

w("## 5. Corrections already made\n")
for c in [
 "\"We are not measuring less, we are sharing less\": withdrawn. Daily data sharing was never obligatory (Menne et al. 2012).",
 "GDIS codebook's 11,801 disasters is a transposition of 11,081.",
 "\"20% of Mozambique's GDP\" for the 2000 floods: unsupportable; use growth falling from 7% to 1.5% and losses of about $600 million.",
 "\"Damage is roughly equal everywhere\": false. Damage is more concentrated than deaths (Gini 0.870 vs 0.836); Europe 20.2% of damage and 1.5% of deaths, Africa 2.9% and 27.0%.",
 "No \"40% more counties\" in the flood-model paper: it is 11.04 M people (+69%) and 4.12 M buildings (+81%).",
 "AI-spending comparison: \"less than two days\" → \"less than half a day\" (US$7.4 bn a day).",
 "Volunteer gauges 53,167 → 51,229. Early warning \"of any kind\" → multi-hazard (G-1).",
 "Flood-model attribution: Wu, Zhang & Stouffs (Tsinghua / NUS / Singapore-ETH), not AlphaGeo, which built a website presenting it.",
 "Processing bugs fixed: the North Atlantic dropped as `NA`; 2° binning inverted the US–Africa finding; extracted dots reproduced map labels as holes; a MEOP join fanned out; telemetry cells at 180° drawn 1° too far north (found 4 Oct, fixed in the regrid sample).",
 "On-screen caveats removed 28 Sep at the author's request (illustrative dots, IBTrACS, EM-DAT geocoding, G-1 \"no report\"). They still apply; a /data or /notes page is the place to restore them.",
]:
    w(f"- {c}")
w("")

w("## 6. Literature\n")
for c in [
 "Menne, M.J. et al. (2012). An Overview of the GHCN-Daily Database. *J. Atmos. Oceanic Technol.* 29, 897–910. **The key source on sharing.**",
 "Applequist, S., Durre, I. & Vose, R. (2024). GHCN Monthly Precipitation v4. *Scientific Data* 11, 633.",
 "Lawrimore, J.H. et al. (2011). GHCN monthly mean temperature v3. *JGR Atmospheres* 116, D19121.",
 "WMO GBON Baseline 2023, SOFF Sixth Steering Committee; SOFF, un-soff.org/operations.",
 "Wu, A.N., Zhang, Y. & Stouffs, R. (2026). Deep learning completes US flood hazard maps. *Nature Communications* 17, 5983.",
 "McDonnell, Kirtman, Braun & Hammerschlag (2026). Improved seasonal climate forecasting using shark-borne sensor data in a dynamic ocean. *npj Clim Atmos Sci* 9:147.",
 "March, D., Boehme, L., Tintoré, J., Vélez-Belchi, P.J. & Godley, B.J. (2020). Towards the integration of animal-borne instruments into global ocean observing systems. *Global Change Biology* 26(2), 586–596. **Found 4 Oct; supports scenes 23–24.**",
 "Pagniello et al. 2024, *Sci Rep* 14:13837; Holland et al. 2022, *Anim Biotelem* 10:34 (shark-borne sensing).",
 "Rentschler, J., Salhab, M. & Jafino, B. (2022). *Nature Communications* 13, 3527 (flood exposure).",
 "Otto, F. (2023). Without Warning. *Yale Environment 360*, 31 Oct (radars).",
 "McCarthy, G.D. et al. (2025). Signal and Noise in the AMOC at 26°N. *GRL* (framing device, not built).",
 "Jaffrés 2019, *Computers & Geosciences* 122; WMO-No. 1244 (Resolution 40); Viscusi & Masterman (VSL); Gartner Sep 2026 (AI spending); Guterres, 22 Oct 2025; Bratton, *Planetary Sapience*; Patzek 2026 (preprint, not peer reviewed).",
]:
    w(f"- {c}")
w("")

w("## 7. Open questions\n")
w("**Sources to add (on screen now, no source recorded):** Michael 74 deaths; Haiyan 6,352 dead and 1,071 missing; damage US$25.5 bn vs US$2.98 bn; \"24 hours of warning cuts damage by about 30%\"; Mozambique 34 million people; \"no national flood map\"; upstream Limpopo gauges; Xai-Xai 55% of built-up area; the Idai impact figures.\n")
w("**Numbers that differ from a recheck:** seals 74% vs 75.7%; Africa 2,166 stations vs 2,119 (define Africa); Africa median record 68 vs 69 years; Sendai 85/105 vs the reports' 95/119 (quote each with its source).\n")
w("**Decisions:**")
for c in [
 "Restore caveats (illustrative dots, \"as recorded in IBTrACS\", geocoding, G-1) on a /data or /notes page, or on screen.",
 "Scene 24 (Mozambique turtles) is the project's own proposal: cite March et al. 2020, or reframe as a proposal.",
 "Satellite scene 2: switch the illustrative shell to the real OSCAR counts?",
 "Grid standard: decided 5 Oct, land 0.5° and ocean 1° on every page (re-check the US scene's \"solid surface\" at 0.5°).",
 "AMOC as opening frame and closing statistic.",
 "Idai: Category 3 or 4; 51 or 52 days; Mozambique-only deaths; photo licences.",
 "Stories: which of the 21 fit the title; Yangtze headline; finish the subtitle.",
 "Decided 5 Oct: the design system is authoritative; the final page is one combined file. Next steps: HANDOVER.md section 8.",
]:
    w(f"- {c}")
w("")
(R / "docs/NARRATIVE.md").write_text("\n".join(out))
print("wrote docs/NARRATIVE.md", sum(len(x) for x in out) // 1000, "KB,", len(S), "scenes")
