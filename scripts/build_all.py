#!/usr/bin/env python3
"""Build the final page: the story plus every prototype section, in one self-contained file.

    python3 scripts/build_all.py

Reads final/sections.json (the order), final/story/template.html (the story: scenes,
globe engine, Explore mode) and each prototype folder, and writes the file named in
sections.json (weather-machine.html). That file is generated: never edit it by hand.
Edit the story template, a prototype's own files, or sections.json, then rebuild.

What goes in once, shared by every section: d3-array and d3-geo (from the story),
the design system (design-system/wm.css and wm.js), the story's layer data and images.

Each prototype is read by a small adapter below, which returns its styles, its markup
(one entry per part, so parts can sit in different places in the order), its data
blocks and its code. Adapters drop anything the page already has (a second d3, a
standalone page's fonts and body styles).

Checks before writing: every placeholder filled; no remote scripts; d3 present once;
no id used twice; each module's ids carry its prefix. The page must open from file://.
"""
import json, re, sys
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FINAL = ROOT / "final"
LAYERS = ROOT / "site-src/layers"
sys.path.insert(0, str(ROOT / "design-system"))
from inline import inline  # noqa: E402

# The story's own placeholders, the same files the live site uses (scripts/build_site.py)
STORY_SUBS = {
    "__DATA__": None,   # the grid-standard base data plus final/story/layers/extra.json: see story_data()
    "__XXB__": LAYERS / "limpopo-before.webp.b64",
    "__XXA__": LAYERS / "limpopo-after.webp.b64",
    "__SEAL__": LAYERS / "seal.webp.b64",
    "__RELIEF__": LAYERS / "relief.webp.b64",
}


def story_data():
    """The story's layers: the grid standard (land 0.5°, ocean 1°; scripts/regrid_layers.py),
    with the final page's extra layers (scripts/pack_final_layers.py) laid over it by name."""
    base = json.loads((LAYERS / "globe-data-land0.5-ocean1.json").read_text())
    extra_path = FINAL / "story/layers/extra.json"
    if not extra_path.exists(): fail("run scripts/pack_final_layers.py first")
    extra = json.loads(extra_path.read_text())
    unknown = [k for k in extra if k not in base]
    if unknown: print(f"  extra layers new to the base data: {unknown}")
    base.update(extra)
    return json.dumps(base, separators=(",", ":"))


def instrument_photos():
    """The instrument cards' photos (assets/instruments, register instruments.json), embedded as data URIs.
    Shown whether or not their credit is cleared (the author's decision, 5 Oct); the slides' source line says
    "Photos: credit to come" until it is."""
    import base64
    folder = ROOT / "assets/instruments"
    reg = json.loads((folder / "instruments.json").read_text())["instruments"]
    out = {}
    for k, it in reg.items():
        f = folder / it["file"]
        if not f.exists(): fail(f"instrument photo missing: {f}")
        out[k] = {"name": it["name"], "tint": it["tint"], "focus": it["focus"],
                  "src": "data:image/webp;base64," + base64.b64encode(f.read_bytes()).decode()}
    return json.dumps(out, separators=(",", ":"))


def block(html, tag, id_):
    """The inside of <tag id="id_" ...>...</tag>; exits if it is missing."""
    m = re.search(rf'<{tag}\b[^>]*\bid="{id_}"[^>]*>(.*?)</{tag}>', html, re.S)
    if not m:
        sys.exit(f"missing <{tag} id=\"{id_}\">")
    return m.group(1)


def element(html, id_):
    """The whole element with this id, nested tags of the same name balanced (for <div>s inside <div>s)."""
    m = re.search(rf'<(\w+)\b[^>]*\bid="{id_}"[^>]*>', html)
    if not m: sys.exit(f"missing element id=\"{id_}\"")
    tag, i, depth = m.group(1), m.end(), 1
    for x in re.finditer(rf'<(/?){tag}\b[^>]*>', html[i:]):
        depth += -1 if x.group(1) else 1
        if depth == 0: return html[m.start():i + x.end()]
    sys.exit(f"unbalanced <{tag}> for id {id_}")


def whole(html, tag, id_):
    """The whole element <tag id="id_" ...>...</tag>, tags included."""
    m = re.search(rf'<{tag}\b[^>]*\bid="{id_}"[^>]*>.*?</{tag}>', html, re.S)
    if not m:
        sys.exit(f"missing <{tag} id=\"{id_}\">")
    return m.group(0)


# ---------------------------------------------------------------- adapters
def rain_gauges():
    """prototypes/rain-gauges: its template (blocks as in INTEGRATION.md section 2), on the
    design system since 5 Oct. Two parts, the density map and the explorer, each in its own
    .rg-sections wrapper so the shared top-bar clearance (--rg-topbar) reaches both wherever
    they are placed. Each carries a [data-slide-text] slot the story fills with its words."""
    src = (ROOT / "prototypes/rain-gauges/template.html").read_text(encoding="utf-8")
    css = "\n".join(block(src, "style", i) for i in ("rg-shared-css", "rgm-css", "rg-css"))
    parts = {
        "map": '<div class="rg-sections">\n' + whole(src, "section", "rgm-scene") + "\n</div>",
        "explorer": '<div class="rg-sections">\n' + whole(src, "section", "rg-scene") + "\n</div>",
    }
    data = "\n".join(whole(src, "script", i) for i in ("rg-DATA", "rg-LAND", "rg-BORD"))
    # each part's own code; the story plugin (gauge layers on the shared globe) always goes in
    part_js = {"map": whole(src, "script", "rgm-JS"), "explorer": whole(src, "script", "rg-JS")}
    js = whole(src, "script", "rgp-JS")
    # its d3 copies are skipped: verified byte-identical to the story's
    # on the shared globe (option A, 5 Oct): the explorer's panel only; the story mounts it under slide 8's words
    # and draws the cells on its own globe through the explorer code's hosted mode
    panel = ('<div class="rg-scene rg-in-story" id="rg-scene" hidden>\n<div id="rg-gtip" class="wm-tip rg-tip" hidden></div>\n'
             + element(src, "rg-panel") + "\n</div>")
    part_js["explorer-panel"] = part_js["explorer"]
    return {"css": css, "parts": parts, "part_js": part_js, "data": data, "js": js, "prefixes": ("rg-", "rgm-", "rgp-"),
            "panels": {"explorer-panel": panel},
            "d3": (block(src, "script", "rg-D3A"), block(src, "script", "rg-D3G"))}


def history():
    """prototypes/history: a century of watching, as a plugin of the shared globe. Its data (history-data.json,
    written by build_history.py), the drawing it shares with the standalone page (history-layers.js) and the
    plugin (story-plugin.js, story-plugin.css). No section and no globe of its own."""
    h = ROOT / "prototypes/history"
    data_file = h / "history-data.json"
    if not data_file.exists(): fail("run prototypes/history/build_history.py first (it writes history-data.json)")
    return {"css": (h / "story-plugin.css").read_text(), "parts": {}, "part_js": {},
            "data": '<script id="hist-DATA" type="application/json">' + data_file.read_text() + "</script>",
            "js": "<script id=\"hist-JS\">\n" + (h / "history-layers.js").read_text() + "\n" + (h / "story-plugin.js").read_text() + "\n</script>",
            "prefixes": ("hist-",)}


def idai():
    """prototypes/idai: Idai on the shared globe. Its data (idai-data.json, written by build_idai.py) without the
    parts the final page does not draw (the world outline, the four districts' streets and outlines), the plugin
    (story-plugin.js), and its three photos and the MODIS pair, embedded (shown whatever their credit status:
    the author's decision, 5 Oct; each says "credit to come")."""
    import base64
    h = ROOT / "prototypes/idai"
    data_file = h / "idai-data.json"
    if not data_file.exists(): fail("run prototypes/idai/build_idai.py first (it writes idai-data.json)")
    data = json.loads(data_file.read_text())
    for k in ("world", "moz", "roads", "aoi", "dmg"): data.pop(k, None)
    def uri(f, mime): return f"data:{mime};base64," + base64.b64encode(f.read_bytes()).decode()
    photos = {"idai-floodplain": uri(h / "photos/aerial-floodplain.jpg", "image/jpeg"),
              "idai-cow": uri(h / "photos/drowned-cow.jpg", "image/jpeg"),
              "idai-pylons": uri(h / "photos/pylons-floodwater.jpg", "image/jpeg"),
              "modis-before": uri(h / "maps/modis-721-2019-02-24.jpg", "image/jpeg"),
              "modis-after": uri(h / "maps/modis-721-2019-03-21.jpg", "image/jpeg")}
    return {"css": "", "parts": {}, "part_js": {},
            "data": ('<script id="idai-DATA" type="application/json">' + json.dumps(data, separators=(",", ":")) + "</script>\n"
                     '<script id="idai-PHOTOS" type="application/json">' + json.dumps(photos) + "</script>"),
            "js": "<script id=\"idai-JS\">\n" + (h / "story-plugin.js").read_text() + "\n</script>",
            "prefixes": ("idai-",)}


def country_profile():
    """prototypes/country-profile: slide 17 "Since you were born", as a plugin of the shared globe. Its data
    (profile-data.json, written by build_globe.py: yearly EM-DAT and IDMC totals per country, people at risk,
    outlines, Su et al. gauge totals) and the plugin (story-plugin.js, story-plugin.css). The rain-gauge
    squares come from the rain-gauge plugin's rg-DATA, so that plugin must be in the page too."""
    h = ROOT / "prototypes/country-profile"
    data_file = h / "profile-data.json"
    if not data_file.exists(): fail("run prototypes/country-profile/build_globe.py first (it writes profile-data.json)")
    return {"css": (h / "story-plugin.css").read_text(), "parts": {}, "part_js": {},
            "data": '<script id="cp-DATA" type="application/json">' + data_file.read_text() + "</script>",
            "js": "<script id=\"cp-JS\">\n" + (h / "story-plugin.js").read_text() + "\n</script>",
            "prefixes": ("cp-",)}


def stories():
    """prototypes/stories: slide 18, the frontline stories, as a plugin of the shared globe. Its words
    (stories.json: every story's place, title, description, source, link and layers) and the plugin
    (story-plugin.js, story-plugin.css). The layers a story shows (seals, sharks, ...) are the story's own."""
    h = ROOT / "prototypes/stories"
    data = json.loads((h / "stories.json").read_text())
    keep = ("id", "list", "title", "description", "place", "lon", "lat", "source", "date", "url", "color", "link", "layers", "zoom", "photo_credit")
    out = {"stories": [{k: s[k] for k in keep if k in s} for s in data["stories"]], "layerStyles": data.get("layerStyles", {})}
    # the article photos (photo_url in stories.json), cropped to 16:9 at 640 x 360 in photos/web (git-ignored;
    # licences not cleared, shown with their credit: the author's decision, 5 Oct); the seals use the project's
    # own seal photo. A story without one keeps its colour block.
    import base64
    web, n = h / "photos/web", 0
    for s, src in zip(out["stories"], data["stories"]):
        f = web / (s["id"] + ".webp")
        if src.get("photo_url"):
            if not f.exists(): fail(f"story photo missing: {f} (see prototypes/stories/README.md)")
            s["photo"] = "data:image/webp;base64," + base64.b64encode(f.read_bytes()).decode(); n += 1
        elif s["id"] == "seals":
            s["photo"] = "data:image/webp;base64," + (LAYERS / "seal.webp.b64").read_text().strip(); n += 1
    print(f"  stories: {n} photos of {len(out['stories'])}")
    return {"css": (h / "story-plugin.css").read_text(), "parts": {}, "part_js": {},
            "data": '<script id="sto-DATA" type="application/json">' + json.dumps(out, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/") + "</script>",
            "js": "<script id=\"sto-JS\">\n" + (h / "story-plugin.js").read_text() + "\n</script>",
            "prefixes": ("sto-",)}


def geopolitics():
    """prototypes/geopolitics: slide 23's two maps (the Indus rivers and Pakistan's 2025 flood water; the Arctic Council
    states and the Arctic Circle), as a plugin of the shared globe. Its data (geopolitics-data.json, written by
    build_geopolitics.py) and the plugin (story-plugin.js)."""
    h = ROOT / "prototypes/geopolitics"
    data_file = h / "geopolitics-data.json"
    if not data_file.exists(): fail("run prototypes/geopolitics/build_geopolitics.py first (it writes geopolitics-data.json)")
    return {"css": "", "parts": {}, "part_js": {},
            "data": '<script id="geo-DATA" type="application/json">' + data_file.read_text() + "</script>",
            "js": "<script id=\"geo-JS\">\n" + (h / "story-plugin.js").read_text() + "\n</script>",
            "prefixes": ("geo-",)}


ADAPTERS = {"rain-gauges": rain_gauges, "history": history, "idai": idai, "country-profile": country_profile, "stories": stories,
            "geopolitics": geopolitics}


# ---------------------------------------------------------------- checks
class Ids(HTMLParser):
    """Collects id attributes from the markup (not from inside scripts or styles)."""
    def __init__(self):
        super().__init__(); self.ids = []
    def handle_starttag(self, tag, attrs):
        for k, v in attrs:
            if k == "id" and v: self.ids.append(v)


def fail(msg):
    sys.exit("build_all: " + msg)


def main():
    # the sections file: final/sections.json, or another one given on the command line (a mock, a test build)
    cfg_path = Path(sys.argv[1]) if len(sys.argv) > 1 else FINAL / "sections.json"
    cfg = json.loads(cfg_path.read_text())
    page = (FINAL / "story/template.html").read_text(encoding="utf-8")

    page = page.replace("__INSTRUMENT_PHOTOS__", instrument_photos())
    for token, path in STORY_SUBS.items():
        if token not in page: fail(f"story template has no {token}")
        page = page.replace(token, story_data() if path is None else path.read_text().strip())

    modules, order_html, sizes, holding = {}, [], [], []
    for item in cfg["order"]:
        if "story" in item:
            scenes = item["story"] if isinstance(item["story"], str) else ",".join(item["story"])
            order_html.append(f'<div class="story-slot" data-scenes="{scenes}"></div>')
        elif "module" in item:
            name, part = item["module"], item["part"]
            if name not in ADAPTERS: fail(f"no adapter for module {name!r}")
            mod = modules.setdefault(name, ADAPTERS[name]())
            mod.setdefault("placed", []).append(part)
            if part not in mod["parts"]: fail(f"module {name!r} has no part {part!r}")
            order_html.append(f'<div class="mod" data-module="{name}" data-part="{part}">\n'
                              + mod["parts"][part] + "\n</div>")
        elif "plugin" in item:
            name = item["plugin"]
            if name not in ADAPTERS: fail(f"no adapter for module {name!r}")
            mod = modules.setdefault(name, ADAPTERS[name]()); mod.setdefault("placed", [])
            for pn in item.get("panels", []):                       # panels the story mounts inside its own slides
                if pn not in mod.get("panels", {}): fail(f"module {name!r} has no panel {pn!r}")
                mod["placed"].append(pn); holding.append(mod["panels"][pn])
        else:
            fail(f"sections.json entry is neither story, module nor plugin: {item}")

    # shared d3: a module's copy is dropped only if it is the same bytes as the story's
    story_d3 = (block(page, "script", "D3A"), block(page, "script", "D3G"))
    for name, mod in modules.items():
        if "d3" in mod and mod["d3"] != story_d3:
            fail(f"module {name!r} ships a different d3 from the story's; reconcile before sharing")

    if holding:
        order_html.append('<div id="plugin-panels" hidden>\n' + "\n".join(holding) + "\n</div>")
    page = page.replace("__PAGE__", json.dumps({"nav": bool(cfg.get("nav")), "partial": bool(cfg.get("partial"))}))
    page = page.replace("__ORDER__", "\n".join(order_html))
    page = page.replace("__MODULE_CSS__", "\n".join(m["css"] for m in modules.values()))
    page = page.replace("__MODULE_DATA__", "\n".join(m["data"] for m in modules.values()))
    page = page.replace("__MODULE_JS__", "\n".join(m["js"] + "\n" + "\n".join(m.get("part_js", {}).get(p, "") for p in m["placed"]) for m in modules.values()))
    page = inline(page)

    # ---- checks
    left = sorted(set(re.findall(r"__[A-Z][A-Z_]+__", page)) | set(re.findall(r"/\*__WM_[A-Z]+__\*/", page)))
    if left: fail(f"placeholders still unfilled: {left}")
    if re.search(r'<script[^>]+src=["\']?https?:', page): fail("a remote script crept in; the page must stay self-contained")
    if page.count("https://d3js.org/d3-geo/") != 1: fail("d3-geo should appear exactly once")
    p = Ids(); p.feed(page)
    dup = [k for k, n in Counter(p.ids).items() if n > 1]
    if dup: fail(f"ids used more than once: {dup}")
    for name, mod in modules.items():
        markup = "\n".join(mod["parts"].values()) + "\n".join(mod.get("panels", {}).values()) + mod["data"]
        q = Ids(); q.feed(markup)
        bad = [i for i in q.ids if not i.startswith(mod["prefixes"])]
        if bad: fail(f"module {name!r} has ids without its prefix {mod['prefixes']}: {bad[:5]}")

    out = ROOT / cfg["output"]
    out.write_text(page, encoding="utf-8")
    print(f"wrote {out.relative_to(ROOT)}  {out.stat().st_size/1e6:.2f} MB")
    for name, mod in modules.items():
        n = sum(len(mod[k].encode()) for k in ("css", "data", "js")) + sum(len(v.encode()) for v in mod["parts"].values())
        print(f"  module {name:<12} {n/1e6:.2f} MB  parts: {', '.join(mod['parts'])}")
    def label(i):
        if "story" in i: return "story: " + (i["story"] if isinstance(i["story"], str) else ", ".join(i["story"]))
        if "plugin" in i: return f"plugin {i['plugin']}"
        return f"{i['module']}:{i['part']}"
    print("  order: " + " → ".join(label(i) for i in cfg["order"]))


if __name__ == "__main__":
    main()
