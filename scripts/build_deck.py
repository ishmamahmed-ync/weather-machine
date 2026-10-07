#!/usr/bin/env python3
"""Three presentation slides as SVG, for Figma (drag the files onto a Figma canvas: each opens as an editable frame).

    python3 scripts/build_deck.py      (standard library only)

Writes docs/deck/01-intro.svg, 02-about.svg, 03-tech-stack.svg (1920 x 1080). Colours, type and line weights are the
design system's (design-system/wm.css): the page black, Space Grotesk for titles, IBM Plex Sans for the rest, uppercase
tracked labels, thin outlined cards. The intro globe is drawn from the project's own data: GHCN-Daily weather
stations (one dot per 1° cell) and Argo profiles (one dot per 2° cell), seen from the site's weather-machine view
(20°W, 20°N); the satellite ring is illustrative, as on the site.
"""
import csv, json, math
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PROC = ROOT / "data/processed"
OUT = ROOT / "docs/deck"
W, H = 1920, 1080
C = dict(bg="#05080E", ocean="#0B121B", land="#161D26", text="#ECEAE5", text2="#D9D6CF", muted="#8B95A1", faint="#5C6773",
         line="#222C38", rim="rgba(236,234,229,.6)", grat="rgba(236,234,229,.15)", frame="#ECEAE5", glass="#080C13",
         station="#FFB547", argo="#45B0CE", sat="#CBD6E2", gauge="#3FD98A", flood="#7DB4D1")
DISP, SANS = "Space Grotesk, IBM Plex Sans, sans-serif", "IBM Plex Sans, sans-serif"
M = 140                                                       # the slide margin


def esc(s):
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def text(x, y, s, size, fill, font=SANS, weight=400, track=0, anchor="start", upper=False, style=""):
    return (f'<text x="{x}" y="{y}" font-family="{font}" font-size="{size}" font-weight="{weight}" fill="{fill}" '
            f'letter-spacing="{track}" text-anchor="{anchor}"{" font-style=\"" + style + "\"" if style else ""}>'
            f'{esc(s.upper() if upper else s)}</text>')


def label(x, y, s, fill=C["muted"], size=17, anchor="start"):
    return text(x, y, s, size, fill, weight=500, track=round(size * .1, 2), anchor=anchor, upper=True)


def frame(n, body):
    """The slide: the page black, the site's header line top left, the slide number bottom right."""
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">\n'
            f'<rect width="{W}" height="{H}" fill="{C["bg"]}"/>\n'
            + label(M, 84, "The Gaps in the Weather Machine", C["text"], 17)
            + text(W - M, H - 64, f"{n:02d}", 17, C["faint"], weight=500, anchor="end")
            + "\n" + body + "\n</svg>\n")


# ---------------------------------------------------------------- 1. intro: the title and the weather machine
def ortho(lon, lat, lon0, lat0, R, cx, cy):
    l, p, l0, p0 = map(math.radians, (lon, lat, lon0, lat0))
    cosc = math.sin(p0) * math.sin(p) + math.cos(p0) * math.cos(p) * math.cos(l - l0)
    if cosc <= 0: return None
    return (cx + R * math.cos(p) * math.sin(l - l0), cy - R * (math.cos(p0) * math.sin(p) - math.sin(p0) * math.cos(p) * math.cos(l - l0)))


def dots(pts, r):
    """Many dots as one path (one layer in Figma, not thousands)."""
    return "".join(f"M{x - r:.1f} {y:.1f}a{r} {r} 0 1 0 {2 * r} 0a{r} {r} 0 1 0 {-2 * r} 0" for x, y in pts)


def globe(cx, cy, R, lon0=-20, lat0=20):
    P = lambda lo, la: ortho(lo, la, lon0, lat0, R, cx, cy)
    out = [f'<circle cx="{cx}" cy="{cy}" r="{R}" fill="{C["ocean"]}"/>']
    # the graticule, every 15°, only the near side
    segs = []
    lines = [[(lo, la) for la in range(-90, 91, 2)] for lo in range(-180, 180, 15)] + \
            [[(lo, la) for lo in range(-180, 181, 2)] for la in range(-75, 76, 15)]
    for ln in lines:
        cur = []
        for q in (P(*ll) for ll in ln):
            if q: cur.append(q)
            elif cur: segs.append(cur); cur = []
        if cur: segs.append(cur)
    out.append(f'<path d="{"".join("M" + "L".join(f"{x:.1f} {y:.1f}" for x, y in s) for s in segs if len(s) > 1)}" '
               f'fill="none" stroke="{C["grat"]}" stroke-width="1"/>')
    # Argo: one dot per 2° cell with profiles
    argo = {(math.floor(f["geometry"]["coordinates"][0] / 2), math.floor(f["geometry"]["coordinates"][1] / 2))
            for f in json.load(open(PROC / "argo-density-1deg.geojson"))["features"]}
    pa = [q for q in (P(i * 2 + 1, j * 2 + 1) for i, j in argo) if q]
    out.append(f'<path d="{dots(pa, 1.2)}" fill="{C["argo"]}" fill-opacity=".4"/>')
    # weather stations: one dot per 1° cell with a station
    st = {(math.floor(float(r["lon"])), math.floor(float(r["lat"]))) for r in csv.DictReader(open(PROC / "ghcnd-stations-with-age.csv"))}
    ps = [q for q in (P(i + .5, j + .5) for i, j in st) if q]
    out.append(f'<path d="{dots(ps, 1.7)}" fill="{C["station"]}" fill-opacity=".9"/>')
    out.append(f'<circle cx="{cx}" cy="{cy}" r="{R}" fill="none" stroke="{C["rim"]}" stroke-width="1.5"/>')
    # satellites: an illustrative tilted orbit round the globe, a dot every 30°
    rx, ry, tilt = R * 1.22, R * .34, -14
    out.append(f'<g transform="rotate({tilt} {cx} {cy})"><ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="none" '
               f'stroke="{C["sat"]}" stroke-opacity=".35" stroke-width="1" stroke-dasharray="3 6"/>')
    sd = []
    for k in range(12):
        a = math.radians(k * 30 + 8); x, y = cx + rx * math.cos(a), cy + ry * math.sin(a)
        if math.sin(a) < 0 and math.hypot(x - cx, (y - cy)) < R: continue      # behind the globe
        sd.append((x, y))
    out.append(f'<path d="{dots(sd, 3.2)}" fill="{C["sat"]}"/></g>')
    print(f"globe: {len(ps):,} station cells and {len(pa):,} Argo cells on the near side")
    return "\n".join(out)


def intro():
    b = [label(M, 380, "Studio I · Project II"),
         text(M, 480, "The Gaps in the", 92, C["text"], DISP, 400, -2),
         text(M, 584, "Weather Machine", 92, C["text"], DISP, 400, -2),
         f'<line x1="{M}" y1="660" x2="{M + 560}" y2="660" stroke="{C["line"]}" stroke-width="1"/>']
    for i, ln in enumerate(["How a planetary constellation of sensors helps us stay ahead",
                            "of natural disasters, and what the cracks in its design reveal",
                            "about the state of a world in polycrisis."]):
        b.append(text(M, 712 + i * 34, ln, 22, C["muted"]))
    b.append(globe(1430, 540, 360))
    # the key, under the globe
    kx, ky = 1100, 960
    for i, (col, name) in enumerate([(C["station"], "Weather stations"), (C["argo"], "Argo floats"), (C["sat"], "Satellites (illustrative)")]):
        x = kx + i * 230
        b.append(f'<circle cx="{x}" cy="{ky - 6}" r="5" fill="{col}"/>' + text(x + 14, ky, name, 16, C["muted"]))
    return frame(1, "\n".join(b))


# ---------------------------------------------------------------- 2. about: two photo spaces
def about():
    b = [label(M, 200, "Studio I · Project II"), text(M, 280, "About", 64, C["text"], DISP, 400, -1)]
    gap, top = 64, 330
    pw, ph = (W - 2 * M - gap) / 2, 640
    for i in range(2):
        x = M + i * (pw + gap)
        b.append(f'<g><rect x="{x}" y="{top}" width="{pw}" height="{ph}" fill="{C["land"]}" stroke="{C["frame"]}" stroke-width="2"/>'
                 + text(x + pw / 2, top + ph / 2, "Greyscale photo", 18, C["faint"], weight=500, anchor="middle")
                 + "</g>")
    return frame(2, "\n".join(b))


# ---------------------------------------------------------------- 3. tech stack: datasets -> CARTO -> Claude <- Figma
DATASETS = [  # (name, what, colour from the design system)
    ("GHCN-Daily", "Weather stations · NOAA", C["station"]),
    ("ISD", "Station history · NOAA", C["station"]),
    ("WMO OSCAR/Space", "Satellites", C["sat"]),
    ("Argo GDAC", "Ocean floats", C["argo"]),
    ("MEOP-CTD", "Seal-borne sensors", "#6FD8B4"),
    ("OBIS-SEAMAP", "Animal tracking", "#B98CE0"),
    ("Su et al. 2026", "Rain gauges", C["gauge"]),
    ("IBTrACS", "Storm tracks · NOAA", "#F2C744"),
    ("EM-DAT", "Disaster impacts · CRED", "#E8433F"),
    ("IDMC GIDD", "Displacement", "#B98CE0"),
    ("UNOSAT", "Flood extents", C["flood"]),
    ("Copernicus EMS", "Building damage", "#F29A3A"),
    ("NASA MODIS", "Satellite imagery", C["muted"]),
    ("Sendai Monitor", "Early warning systems", "#F5D04A"),
    ("Natural Earth", "Borders and rivers", C["muted"]),
]


def box(x, y, w, h, title, sub=None, big=False):
    s = [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="3" fill="{C["glass"]}" stroke="{C["text"] if big else C["line"]}" stroke-width="{1.5 if big else 1}"/>']
    if sub is None:
        s.append(text(x + 16, y + h / 2 + 6, title, 17, C["text"], weight=500))
    else:
        s.append(text(x + 24, y + h / 2 - 6, title, 30 if big else 17, C["text"], DISP if big else SANS, 500, -.3 if big else 0))
        s.append(text(x + 24, y + h / 2 + 26, sub, 16, C["muted"]))
    return "".join(s)


def curve(x1, y1, x2, y2, col=C["muted"], op=.55, w=1.2, arrow=False):
    mx = (x1 + x2) / 2
    s = f'<path d="M{x1} {y1:.1f}C{mx} {y1:.1f} {mx} {y2:.1f} {x2 - (8 if arrow else 0)} {y2:.1f}" fill="none" stroke="{col}" stroke-opacity="{op}" stroke-width="{w}"/>'
    if arrow:
        s += f'<path d="M{x2 - 10} {y2 - 6:.1f}L{x2} {y2:.1f}L{x2 - 10} {y2 + 6:.1f}" fill="none" stroke="{col}" stroke-width="{w + .3}"/>'
    return s


def tech():
    b = [label(M, 200, "Tech stack"), text(M, 280, "From data and design to one page", 64, C["text"], DISP, 400, -1)]
    # column 1: the datasets, small boxes
    x0, y0, bw, bh, gap = M, 352, 330, 34, 7
    cy_ds = []
    b.append(label(x0, y0 - 22, "Geospatial datasets", C["faint"], 15))
    for i, (name, what, col) in enumerate(DATASETS):
        y = y0 + i * (bh + gap); cy_ds.append(y + bh / 2)
        b.append(f'<rect x="{x0}" y="{y}" width="{bw}" height="{bh}" rx="3" fill="{C["glass"]}" stroke="{C["line"]}"/>'
                 f'<circle cx="{x0 + 18}" cy="{y + bh / 2}" r="4.5" fill="{col}"/>'
                 + text(x0 + 34, y + bh / 2 + 6, name, 16, C["text"], weight=500)
                 + text(x0 + bw - 14, y + bh / 2 + 6, what, 13.5, C["muted"], anchor="end"))
    # column 2: CARTO (processing), and below it the Figma design system
    cx, cw, chh = 820, 380, 110
    carto_y = (cy_ds[0] + cy_ds[-1]) / 2 - chh / 2 - 60
    fig_y = cy_ds[-1] - chh + 10
    b.append(label(cx, carto_y - 22, "Processing", C["faint"], 15))
    b.append(label(cx, fig_y - 22, "Design", C["faint"], 15))
    # column 3: Claude, where the two converge
    kx, kw, kh = 1440, 340, 150
    ky = (carto_y + chh / 2 + fig_y + chh / 2) / 2 - kh / 2
    b.append(label(kx, ky - 22, "Build", C["faint"], 15))
    # the flows, under the boxes
    for y in cy_ds: b.append(curve(x0 + bw, y, cx, carto_y + chh / 2, op=.4, w=1))
    b.append(curve(cx + cw, carto_y + chh / 2, kx, ky + kh / 2 - 22, C["text"], .8, 1.5, True))
    b.append(curve(cx + cw, fig_y + chh / 2, kx, ky + kh / 2 + 22, C["text"], .8, 1.5, True))
    b.append(box(cx, carto_y, cw, chh, "CARTO", "Processing and mapping", True))
    b.append(box(cx, fig_y, cw, chh, "Figma", "The design system", True))
    b.append(box(kx, ky, kw, kh, "Claude", "Where data and design converge", True))
    return frame(3, "\n".join(b))


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for name, svg in [("01-intro", intro()), ("02-about", about()), ("03-tech-stack", tech())]:
        f = OUT / f"{name}.svg"; f.write_text(svg); print(f"wrote {f.relative_to(ROOT)}  {f.stat().st_size / 1e3:.0f} KB")


if __name__ == "__main__":
    main()
