"""Draft wireframe SVGs of four screens, sized for Figma (1440 x 900).

Text stays as <text> so it is editable after import; groups are named so the
layer tree is legible; no CSS variables or blend modes, which Figma ignores.
"""
import json, math, random
import numpy as np

W, H = 1440, 900
INK, MUTED, RULE = "#ECEAE5", "#8B95A1", "#2A3542"
VOID, OCEAN, LAND = "#05080E", "#0B121B", "#161D26"
GRID = "#18222E"
LAMP, FLOAT, SEAL, SHARK = "#FFB547", "#45B0CE", "#6FD8B4", "#F07A55"
MAGENTA, WATER = "#E05CC8", "#2E6FA3"

land_geom = json.load(open("ne110.geojson"))


def ortho(lon, lat, lon0, lat0, R, cx, cy):
    """Orthographic projection. Returns (x, y, visible)."""
    l, p = math.radians(lon - lon0), math.radians(lat)
    p0 = math.radians(lat0)
    cosc = math.sin(p0) * math.sin(p) + math.cos(p0) * math.cos(p) * math.cos(l)
    x = cx + R * math.cos(p) * math.sin(l)
    y = cy - R * (math.cos(p0) * math.sin(p) - math.sin(p0) * math.cos(p) * math.cos(l))
    return x, y, cosc >= 0


def rings(geom):
    t, c = geom["type"], geom["coordinates"]
    if t == "Polygon":
        return c
    out = []
    for poly in c:
        out += poly
    return out


def coast_paths(lon0, lat0, R, cx, cy, simplify=2):
    """Coastline as SVG paths, split wherever a line goes round the back."""
    out = []
    for f in land_geom["features"]:
        for ring in rings(f["geometry"]):
            d, pen = [], False
            for i, (lo, la) in enumerate(ring):
                if i % simplify:
                    continue
                x, y, vis = ortho(lo, la, lon0, lat0, R, cx, cy)
                if not vis:
                    pen = False
                    continue
                d.append(("M" if not pen else "L") + f"{x:.1f} {y:.1f}")
                pen = True
            if len(d) > 3:
                out.append("".join(d))
    return out


def graticule(lon0, lat0, R, cx, cy, step=30):
    out = []
    for lon in range(-180, 181, step):
        d, pen = [], False
        for lat in range(-90, 91, 3):
            x, y, vis = ortho(lon, lat, lon0, lat0, R, cx, cy)
            if not vis:
                pen = False
                continue
            d.append(("M" if not pen else "L") + f"{x:.1f} {y:.1f}")
            pen = True
        if d:
            out.append("".join(d))
    for lat in range(-60, 61, step):
        d, pen = [], False
        for lon in range(-180, 181, 3):
            x, y, vis = ortho(lon, lat, lon0, lat0, R, cx, cy)
            if not vis:
                pen = False
                continue
            d.append(("M" if not pen else "L") + f"{x:.1f} {y:.1f}")
            pen = True
        if d:
            out.append("".join(d))
    return out


def head(title):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
            f'viewBox="0 0 {W} {H}" font-family="Inter, Helvetica, Arial, sans-serif">'
            f'<title>{title}</title>'
            f'<g id="background"><rect width="{W}" height="{H}" fill="{VOID}"/></g>')


def globe(lon0, lat0, R, cx, cy, grat=True, coast=True, simplify=2):
    s = f'<g id="globe"><circle cx="{cx}" cy="{cy}" r="{R:.1f}" fill="{OCEAN}"/>'
    if grat:
        s += f'<g id="graticule" fill="none" stroke="{GRID}" stroke-width="0.8">'
        s += "".join(f'<path d="{d}"/>' for d in graticule(lon0, lat0, R, cx, cy))
        s += "</g>"
    if coast:
        s += f'<g id="coastline" fill="{LAND}" stroke="{RULE}" stroke-width="0.8">'
        s += "".join(f'<path d="{d}"/>' for d in coast_paths(lon0, lat0, R, cx, cy, simplify))
        s += "</g>"
    s += f'<circle cx="{cx}" cy="{cy}" r="{R:.1f}" fill="none" stroke="{RULE}" stroke-width="1.2"/></g>'
    return s


def dots(pts, lon0, lat0, R, cx, cy, colour, r=1.6, gid="dots", opacity=0.9):
    s = f'<g id="{gid}" fill="{colour}" opacity="{opacity}">'
    for lo, la in pts:
        x, y, vis = ortho(lo, la, lon0, lat0, R, cx, cy)
        if vis:
            s += f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}"/>'
    return s + "</g>"


def text_block(x, y, lines, size=19, fill=INK, lead=1.55, weight="400", gid="copy"):
    s = f'<g id="{gid}">'
    for i, ln in enumerate(lines):
        s += (f'<text x="{x}" y="{y + i*size*lead:.0f}" font-size="{size}" '
              f'fill="{fill}" font-weight="{weight}">{ln}</text>')
    return s + "</g>"


def legend(x, y, items, gid="legend"):
    s = f'<g id="{gid}">'
    ox = x
    for colour, label in items:
        s += f'<circle cx="{ox+4}" cy="{y-4}" r="4.5" fill="{colour}"/>'
        s += f'<text x="{ox+16}" y="{y}" font-size="13" fill="{MUTED}">{label}</text>'
        ox += 20 + len(label) * 7.2
    return s + "</g>"


def sample_stations(n, bbox=None):
    import pandas as pd
    d = pd.read_csv("/mnt/user-data/outputs/ghcnd-stations-clean.csv", low_memory=False)
    if bbox:
        w, s_, e, nn = bbox
        d = d[(d.lon.between(w, e)) & (d.lat.between(s_, nn))]
    d = d.sample(min(n, len(d)), random_state=4)
    return list(zip(d.lon, d.lat))


# ---------------------------------------------------------------- screen 1
def screen1():
    cx, cy, R = 980, 450, 340
    s = head("01 narration over an empty globe")
    s += globe(-40, 12, R, cx, cy)
    s += text_block(58, 380, [
        "For as long as there have been people, there has",
        "been weather arriving that no one could see coming.",
    ], size=21)
    s += text_block(58, 470, [
        "Harvests, voyages, cities: all of it staked on a sky",
        "that gave no notice.",
    ], size=21, fill=MUTED)
    s += f'<text x="58" y="840" font-size="12" fill="{MUTED}" letter-spacing="1">SCROLL</text>'
    s += f'<g id="notes"><text x="58" y="70" font-size="11" fill="{MUTED}" letter-spacing="1.4">01 &#183; NARRATION &#183; NO BOX</text></g>'
    return s + "</svg>"


# ---------------------------------------------------------------- screen 2
def screen2():
    cx, cy, R = 980, 450, 340
    pts = sample_stations(1400)
    s = head("02 data card over a dotted globe")
    s += globe(-30, 18, R, cx, cy)
    s += dots(pts, -30, 18, R, cx, cy, LAMP, r=1.5, gid="dots-stations", opacity=0.85)
    s += ('<g id="card">'
          f'<rect x="58" y="300" width="470" height="300" rx="3" fill="#05080E" '
          f'fill-opacity="0.84" stroke="{RULE}"/>')
    s += f'<text x="90" y="372" font-size="46" fill="{LAMP}" font-weight="500">132,501</text>'
    s += f'<text x="90" y="398" font-size="14" fill="{MUTED}">weather stations in the global daily archive</text>'
    s += ('<text x="90" y="442" font-size="17" fill="#ECEAE5">Over three centuries the planet has been</text>'
          '<text x="90" y="468" font-size="17" fill="#ECEAE5">studded with an apparatus for sensing itself.</text>'
          '<text x="90" y="506" font-size="17" fill="#ECEAE5">A thin artificial nervous system laid across</text>'
          '<text x="90" y="532" font-size="17" fill="#ECEAE5">a natural one.</text>')
    s += legend(90, 572, [(LAMP, "Weather stations"), (FLOAT, "Argo floats")], gid="legend")
    s += "</g>"
    s += f'<g id="notes"><text x="58" y="70" font-size="11" fill="{MUTED}" letter-spacing="1.4">02 &#183; DATA CARD &#183; STAT + LEGEND</text></g>'
    return s + "</svg>"


# ---------------------------------------------------------------- screen 3
def screen3():
    cx, cy, R = 980, 450, 620          # zoomed in: globe overflows the frame
    pts = sample_stations(2200, bbox=(-126, 24, -66, 50))
    s = head("03 focus on the United States")
    s += globe(-98, 39, R, cx, cy, simplify=1)
    s += dots(pts, -98, 39, R, cx, cy, LAMP, r=1.7, gid="dots-us", opacity=0.9)
    s += text_block(58, 372, [
        "Here the instruments crowd so densely that the",
        "continent stops reading as points and becomes",
        "a lit surface.",
    ], size=21)
    s += ('<g id="stat-inline">'
          f'<text x="58" y="486" font-size="52" fill="{LAMP}" font-weight="500">76,708</text>'
          f'<text x="58" y="514" font-size="14" fill="{MUTED}">stations across the contiguous United States</text></g>')
    s += legend(58, 560, [(LAMP, "Weather stations")], gid="legend")
    s += f'<g id="notes"><text x="58" y="70" font-size="11" fill="{MUTED}" letter-spacing="1.4">03 &#183; REGION FOCUS &#183; UNITED STATES</text></g>'
    return s + "</svg>"


# ---------------------------------------------------------------- screen 4
def screen4():
    # at this zoom the sphere is far bigger than the frame, so it reads as flat
    cx, cy, R = 720, 460, 7600
    lon0, lat0 = 33.44, -24.87
    s = head("04 Limpopo before / after wipe")
    s += f'<g id="ground"><rect width="{W}" height="{H}" fill="{OCEAN}"/>'
    s += f'<g id="graticule" fill="none" stroke="{GRID}" stroke-width="0.8">'
    s += "".join(f'<path d="{d}"/>' for d in graticule(lon0, lat0, R, cx, cy, step=1))
    s += "</g></g>"

    # the framed panel
    bx, by, bw, bh = 560, 250, 420, 400
    rnd = random.Random(8)
    s += '<g id="wipe-panel">'
    s += f'<rect x="{bx}" y="{by}" width="{bw}" height="{bh}" fill="#0E141C"/>'
    s += '<g id="settlements-before" fill="' + MAGENTA + '" opacity="0.85">'
    for _ in range(320):
        x = bx + rnd.random() * bw * 0.5
        y = by + rnd.random() * bh
        s += f'<circle cx="{x:.0f}" cy="{y:.0f}" r="1.8"/>'
    s += "</g>"
    s += '<g id="floodwater-after" fill="' + WATER + '" opacity="0.85">'
    for _ in range(380):
        x = bx + bw * 0.5 + rnd.random() * bw * 0.5
        y = by + rnd.random() * bh
        s += f'<circle cx="{x:.0f}" cy="{y:.0f}" r="1.8"/>'
    s += "</g>"
    s += f'<rect x="{bx}" y="{by}" width="{bw}" height="{bh}" fill="none" stroke="{INK}" stroke-opacity="0.7"/>'
    s += f'<line x1="{bx+bw/2}" y1="{by}" x2="{bx+bw/2}" y2="{by+bh}" stroke="{INK}" stroke-width="2"/>'
    s += f'<circle cx="{bx+bw/2}" cy="{by+bh/2}" r="13" fill="{INK}"/>'
    s += f'<text x="{bx+bw/2}" y="{by+bh/2+4}" font-size="12" fill="#05080E" text-anchor="middle">&#8596;</text>'
    s += f'<text x="{bx}" y="{by+bh+20}" font-size="12" fill="{INK}">Before</text>'
    s += f'<text x="{bx+bw}" y="{by+bh+20}" font-size="12" fill="{INK}" text-anchor="end">After the flood</text>'
    s += "</g>"

    s += text_block(58, 372, [
        "What we can see is the aftermath.",
        "The lower Limpopo, around Xai-Xai.",
    ], size=21)
    s += text_block(58, 452, [
        "Drag the handle. Magenta is built ground.",
        "Blue is where the water stands on the later date.",
    ], size=18, fill=MUTED)
    s += legend(58, 530, [(MAGENTA, "Settlements"), (WATER, "Floodwater")], gid="legend")
    s += f'<g id="notes"><text x="58" y="70" font-size="11" fill="{MUTED}" letter-spacing="1.4">04 &#183; CLOSE FOCUS &#183; LIMPOPO WIPE</text></g>'
    return s + "</svg>"


for name, fn in [("01-narration-empty-globe", screen1),
                 ("02-data-card-dotted-globe", screen2),
                 ("03-focus-united-states", screen3),
                 ("04-focus-limpopo-wipe", screen4)]:
    out = f"/mnt/user-data/outputs/draft-{name}.svg"
    open(out, "w").write(fn())
    import os
    print(f"{name:32} {os.path.getsize(out)//1024:4d} KB")
