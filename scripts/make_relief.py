#!/usr/bin/env python3
"""Shrink the Natural Earth grey shaded relief into the globe texture.

    python scripts/make_relief.py

Input   data/raw/GRAY_50M_SR_W/GRAY_50M_SR_W.tif
            Natural Earth "Gray Earth with Shaded Relief and Water", 1:50m,
            10800 x 5400, 8-bit grey, equirectangular, public domain.
            https://naciscdn.org/naturalearth/50m/raster/GRAY_50M_SR_W.zip
Output  site-src/layers/relief.webp.b64   4096 x 2048 WebP, base64

Water in the source is a single flat value (106 of 255, two thirds of all
pixels); land runs about 132-211. The engine's shader relies on that gap to
tell water from land, so don't re-colour the image here: tone it in LOOK.

Uses macOS `sips` to resize and `cwebp` (brew install webp) to encode.
"""
import base64
import subprocess
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "data/raw/GRAY_50M_SR_W/GRAY_50M_SR_W.tif"
OUT = ROOT / "site-src/layers/relief.webp.b64"
W, H, Q = 4096, 2048, 72

with tempfile.TemporaryDirectory() as tmp:
    png, webp = Path(tmp) / "r.png", Path(tmp) / "r.webp"
    subprocess.run(["sips", "-z", str(H), str(W), "-s", "format", "png", str(SRC), "--out", str(png)],
                   check=True, capture_output=True)
    subprocess.run(["cwebp", "-quiet", "-q", str(Q), "-metadata", "none", str(png), "-o", str(webp)], check=True)
    OUT.write_text(base64.b64encode(webp.read_bytes()).decode())
print(f"wrote {OUT.relative_to(ROOT)}  {OUT.stat().st_size/1e3:.0f} KB (base64)")
