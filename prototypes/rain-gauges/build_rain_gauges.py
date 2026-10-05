#!/usr/bin/env python3
"""Build the standalone rain-gauge page: template.html + the design system -> rain-gauge-sections.html.

    python3 build_rain_gauges.py      (from this folder; standard library only)

Edit template.html, never rain-gauge-sections.html. The template's styles use the design
system's tokens (var(--wm-...)), so the standalone preview needs wm.css inlined; the final
page (scripts/build_all.py) reads the template's blocks directly and shares one wm.css.
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
sys.path.insert(0, str(ROOT / "design-system"))
from inline import inline  # noqa: E402

page = inline((HERE / "template.html").read_text(encoding="utf-8"))
if "/*__WM_CSS__*/" in page: sys.exit("wm.css was not inlined")
if 'src="http' in page: sys.exit("a remote script crept in")
out = HERE / "rain-gauge-sections.html"
out.write_text(page, encoding="utf-8")
print(f"wrote {out.name}  {out.stat().st_size/1e6:.2f} MB")
