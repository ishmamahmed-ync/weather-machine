#!/bin/sh
# Rebuild every page in the project from its sources, in dependency order.
#
#     sh scripts/rebuild_all.sh          (from the repository root)
#
# Python 3.9+, standard library only. Stops at the first failure. Each build prints
# its own checks; read them. The raw downloads it needs are in data/raw/ (gitignored).
set -e
cd "$(dirname "$0")/.."
ROOT=$(pwd)
step(){ printf '\n=== %s\n' "$1"; }

step "main site: site-src/template.html -> index.html"
python3 scripts/build_site.py

step "grid-standard sample: land 0.5, ocean 1 (sample-land0.5-ocean1.html)"
python3 scripts/regrid_layers.py --land 0.5 --ocean 1

step "Argo coldspot dots (data/processed)"
python3 scripts/coldspots_to_points.py | tail -2

step "country profile -> prototypes/country-profile/globe.html"
cd "$ROOT/prototypes/country-profile" && python3 build_globe.py

step "Idai -> prototypes/idai/idai.html (+ photos/, maps/)"
cd "$ROOT/prototypes/idai" && python3 build_idai.py

step "history -> prototypes/history/history.html"
cd "$ROOT/prototypes/history" && python3 extract_satellites.py && python3 build_history.py

step "stories -> prototypes/stories/stories.html"
cd "$ROOT/prototypes/stories" && python3 build_stories.py

step "rain gauges -> prototypes/rain-gauges/rain-gauge-sections.html"
cd "$ROOT/prototypes/rain-gauges" && python3 build_rain_gauges.py

step "final page's extra layers -> final/story/layers/extra.json"
cd "$ROOT" && python3 scripts/pack_final_layers.py

step "design system -> design-system/specimen.html"
cd "$ROOT/design-system" && python3 build_specimen.py

step "narrative -> docs/NARRATIVE.md"
cd "$ROOT" && python3 scripts/build_narrative.py

step "final page -> weather-machine.html (after every prototype it reads)"
cd "$ROOT" && python3 scripts/build_all.py

step "figures -> docs/FIGURES.md"
cd "$ROOT" && python3 scripts/check_figures.py > /dev/null || echo "a figure no longer matches: see docs/FIGURES.md"

printf '\nAll builds finished.\n'
