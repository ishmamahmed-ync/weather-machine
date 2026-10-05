#!/usr/bin/env python3
"""Build stories.html: stories of resilience as clickable circles on the globe.

    cd prototypes/stories && python3 build_stories.py

Standard library only. Writes stories.html next to this file; open it directly.

Edit the words in stories.json, not in the page: title, subtitle, and one entry
per story (title, description, place, lon/lat, source, date, url, placeholder
colour, and optionally zoom and the map layers to show when it is open). Map layers
come from the main site's packed data, site-src/layers/globe-data.json, unchanged.
Descriptions were written from each source article on 4 Oct 2026; see
README.md. photo_ref / photo_credit record the article's own image for later;
nothing is downloaded and the card shows a coloured 16:9 block for now.
"""
import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
NEEDED = ("id", "title", "description", "place", "lon", "lat", "source", "url")


def main():
    data = json.loads((HERE / "stories.json").read_text())
    S = data["stories"]
    ids = [s["id"] for s in S]
    assert len(ids) == len(set(ids)), "duplicate story id"
    for s in S:
        missing = [k for k in NEEDED if s.get(k) in (None, "")]
        assert not missing, f"{s.get('id')}: missing {missing}"
        assert -180 <= s["lon"] <= 180 and -90 <= s["lat"] <= 90, f"{s['id']}: lon/lat out of range"
        assert s["url"].startswith("https://"), f"{s['id']}: url must be https"
    # map layers: pack only the ones a story uses, straight from the main site's data
    main = json.loads((ROOT / "site-src/layers/globe-data.json").read_text())
    styles = data.get("layerStyles", {})
    used = sorted({l["key"] for s in S for l in s.get("layers", [])})
    for key in used:
        assert key in main, f"layer {key} is not in globe-data.json"
        assert key in styles, f"layer {key} has no entry in layerStyles"
    data["layerData"] = {k: main[k] for k in used}
    for k in used:
        L = main[k]
        n = len(L["xy"]) // 2 if L.get("type") == "points" else len(L["n"])
        print(f"   layer {k:10} {L.get('type', 'grid'):6} {n:>7,} {'dots' if L.get('type') == 'points' else 'cells'}")
    words = max(len(s["description"].split()) for s in S)
    print(f"{len(S)} stories ({sum(s.get('list') == 'flood' for s in S)} flood sensing, "
          f"{sum(s.get('list') == 'hope' for s in S)} hope, {sum(s.get('list') == 'animals' for s in S)} animals); "
          f"longest description {words} words")

    site = (ROOT / "site-src/template.html").read_text()
    d3 = "\n".join(re.search(rf'<script id="{k}">.*?</script>', site, re.S).group(0) for k in ("D3A", "D3G"))
    relief = (ROOT / "site-src/layers/relief.webp.b64").read_text().strip()

    page = (HERE / "template.html").read_text()
    for token in ("__D3__", "__DATA__", "__RELIEF__"):
        assert token in page, f"template.html has no {token}"
    # keep the payload safe inside <script>: no "</" can close the tag early
    payload = json.dumps(data, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    page = page.replace("__D3__", d3).replace("__RELIEF__", relief).replace("__DATA__", payload)
    assert 'src="http' not in page, "page loads a remote script; it must stay self-contained"
    (HERE / "stories.html").write_text(page)
    print(f"wrote stories.html  {(HERE / 'stories.html').stat().st_size/1e6:.2f} MB")


if __name__ == "__main__":
    main()
