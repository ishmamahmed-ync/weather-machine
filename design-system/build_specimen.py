#!/usr/bin/env python3
"""Build specimen.html, the design system's visual reference.

    cd design-system && python3 build_specimen.py

The colour swatches are generated from wm.css itself (each token's value and its
comment), so the specimen cannot drift from the stylesheet. The globe sheet uses
real data on the proposed grid standard: the main site's land outline, weather
stations at 0.5 degrees, Argo profiles at 1 degree (scripts/regrid_layers.py helpers).

Writes specimen.html (a full page, opens from a file). With --fragment PATH it
also writes the same page without the <html>/<head>/<body> wrapper, for publishing.
"""
import html
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(ROOT / "scripts"))
from inline import inline                       # noqa: E402
from regrid_layers import rebin, encode          # noqa: E402

# wm.css comment headings -> specimen groups (only colour groups are shown as swatches)
GROUPS = ["Surfaces", "Text", "Lines", "Status", "Instruments", "Impacts"]


def swatches(css):
    root = css[css.index(":root{"):css.index("/* ---------- 2. Base")]
    out, group = {}, None
    for line in root.splitlines():
        h = re.match(r"\s*/\*\s*(\w+)", line)
        if h and h.group(1) in GROUPS and h.group(1) not in out:   # first heading only ("Text halo" is not a group)
            group = h.group(1); out[group] = []; continue
        if h and h.group(1)[0].isupper() and h.group(1) not in GROUPS and not line.strip().startswith("--"):
            group = None                               # a new capitalised heading ends the group; lowercase notes don't
        if group is None:
            continue
        for name, val, note in re.findall(r"(--wm-[\w-]+):\s*([^;]+);\s*(?:/\*\s*(.*?)\s*\*/)?", line):
            if val.startswith("blur") or re.match(r"--wm-gauge-\d$", name):
                continue                               # the density ramp is drawn as a ramp, like the storm scale
            out[group].append((name, val.strip(), (note or "").strip()))
    titles = {"Surfaces": "Surfaces", "Text": "Text, four steps", "Lines": "Lines",
              "Status": "Status, interface only", "Instruments": "Data: instruments, who is watching",
              "Impacts": "Data: impacts, what happens to people"}
    parts = []
    for g in GROUPS:
        tiles = "".join(
            f'<div class="sw"><div class="chip" style="background:var({n})"></div>'
            f'<span class="name">{html.escape(n)}</span><span class="val">{html.escape(v)}</span>'
            f'<span class="use">{html.escape(note)}</span></div>' for n, v, note in out.get(g, []))
        parts.append(f'<div class="group"><h3>{titles[g]}</h3><div class="swatches">{tiles}</div></div>')
    return "\n".join(parts), sum(len(v) for v in out.values())


def main():
    css = (HERE / "wm.css").read_text()
    sw, n = swatches(css)
    data = json.loads((ROOT / "site-src/layers/globe-data.json").read_text())
    # the proposed grid standard (scripts/regrid_layers.py): land 0.5 degrees, ocean 1 degree
    from collections import defaultdict
    from regrid_layers import cell
    argo = defaultdict(int)
    for f in json.loads((ROOT / "data/processed/argo-density-1deg.geojson").read_text())["features"]:
        argo[cell(*f["geometry"]["coordinates"], 1.0)] += f["properties"]["profiles"]
    spec = {"land": data["land"],
            "stations": encode(rebin(data["stations"], 0.5), 0.5),
            "argo": encode(argo, 1.0)}
    site = (ROOT / "site-src/template.html").read_text()
    d3 = "\n".join(re.search(rf'<script id="{k}">.*?</script>', site, re.S).group(0) for k in ("D3A", "D3G"))

    # instrument cards from assets/instruments: stations, Argo, satellites as rows, rain gauges newest (16:9)
    import base64
    reg = json.loads((ROOT / "assets/instruments/instruments.json").read_text())
    DESC = {"stations": "132,501 in the global archive", "argo": "3,375,214 profiles from 20,530 floats",
            "sats": "439 Earth-observing, in operation (2025). Placeholder photo: replace",
            "gauges": "A gauge in 8,303 of 15,263 land cells of 1°"}
    cards = []
    for i, key in enumerate(reg["order"]):
        it = reg["instruments"][key]
        b64 = base64.b64encode((ROOT / "assets/instruments" / it["file"]).read_bytes()).decode()
        row = " is-row" if i < len(reg["order"]) - 1 else ""
        cards.append(f'<div class="wm-instrument{row}" style="--tint:var({it["tint"]})"><div class="ph">'
                     f'<img src="data:image/webp;base64,{b64}" alt="{html.escape(it["shows"])}" style="object-position:{it["focus"]}"></div>'
                     f'<span class="name">{html.escape(it["name"])}</span><p class="desc">{html.escape(DESC[key])}</p></div>')
    instruments = '<div class="wm-instruments">' + "".join(cards) + "</div>"

    frag = (HERE / "specimen-template.html").read_text()
    frag = frag.replace("__INSTRUMENTS__", instruments)
    frag = inline(frag).replace("__SWATCHES__", sw).replace("__D3__", d3)
    frag = frag.replace("__SPEC__", json.dumps(spec, separators=(",", ":")))
    for t in ("__SWATCHES__", "__D3__", "__SPEC__", "__INSTRUMENTS__", "/*__WM_CSS__*/", "/*__WM_JS__*/"):
        assert t not in frag, f"unfilled {t}"
    assert 'src="http' not in frag, "the specimen must stay self-contained"

    head, body = frag.split("</style>", 1)
    page = ('<!DOCTYPE html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n'
            '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
            f'{head}</style>\n</head>\n<body>\n{body}\n</body>\n</html>\n')
    (HERE / "specimen.html").write_text(page)
    print(f"{n} colour tokens; wrote specimen.html  {len(page)/1e3:.0f} KB")
    if "--fragment" in sys.argv:
        dest = Path(sys.argv[sys.argv.index("--fragment") + 1])
        dest.write_text(frag)
        print(f"wrote fragment {dest}")


if __name__ == "__main__":
    main()
