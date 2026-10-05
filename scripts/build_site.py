#!/usr/bin/env python3
"""Assemble site/index.html from the template and the packed layer data.

    python scripts/build_site.py

The published site is one self-contained HTML file: no network requests, no
build tooling in the browser, opens from a file path. That portability is
deliberate — it cannot break in a crit — but it means the data has to be
injected at build time rather than fetched at run time. This does that.

Inputs   site-src/template.html          markup, styles, engine, with placeholders
         site-src/layers/*.json|.b64     packed layer data and embedded images
Output   index.html                      what GitHub Pages serves

Placeholders in the template, each replaced once:

    __DATA__   the whole layer payload (see scripts/pack_layers.py)
    __XXB__    Lower Limpopo, before image, base64 WebP
    __XXA__    Lower Limpopo, after image, base64 WebP
    __SEAL__   instrumented seal photograph, base64 WebP
    __RELIEF__ grey shaded-relief globe texture, base64 WebP (scripts/make_relief.py)
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "site-src"
LAYERS = SRC / "layers"
OUT = ROOT / "index.html"

SUBS = {
    "__DATA__": LAYERS / "globe-data.json",
    "__XXB__": LAYERS / "limpopo-before.webp.b64",
    "__XXA__": LAYERS / "limpopo-after.webp.b64",
    "__SEAL__": LAYERS / "seal.webp.b64",
    "__RELIEF__": LAYERS / "relief.webp.b64",
}


def main():
    template = SRC / "template.html"
    if not template.exists():
        sys.exit(f"missing template: {template}")

    html = template.read_text()

    for token, path in SUBS.items():
        if not path.exists():
            sys.exit(f"missing layer file: {path}")
        if token not in html:
            sys.exit(f"template has no {token} placeholder — did it get built already?")
        html = html.replace(token, path.read_text().strip())

    leftover = [t for t in SUBS if t in html]
    if leftover:
        sys.exit(f"placeholders still unfilled: {leftover}")

    if 'src="http' in html:
        sys.exit("template loads a remote script — the site must stay self-contained")

    OUT.write_text(html)
    print(f"wrote {OUT.relative_to(ROOT)}  {OUT.stat().st_size/1e6:.2f} MB")
    print("open it directly, or commit and push to deploy")


if __name__ == "__main__":
    main()
