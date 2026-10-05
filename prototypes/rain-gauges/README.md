# Rain gauge density: map and explorer

Two full-screen scenes. **Edit `template.html`**; `python3 build_rain_gauges.py` writes the
standalone preview `rain-gauge-sections.html` (0.95 MB, opens from a file) with the design
system inlined. **In the final page** (`scripts/build_all.py`) the map carries slide 5 and the
explorer slide 8 of the narrative: each opens with that slide's words in the design system's
fixed slide-text block, everything else below them. See the dated note at the top of
`INTEGRATION.md` for what changed on 5 Oct 2026.

1. **Rain gauge density** (`#rgm-scene`): the earth alone, one dot per 0.5° land
   cell, coloured by gauges per 1,000 km² in eight classes.
2. **Rain gauge density against the WMO minimum** (`#rg-scene`): a chart panel
   with terrain tabs (Plains, Hilly, Mountains, Coastal, Islands, Urban,
   Polar/Arid), one square per 1° cell against the WMO minimum for that terrain,
   linked both ways to a globe. Green meets the minimum, faint green falls
   short, grey has no gauge.

**These are rain (precipitation) gauges, not flood or stream gauges.** Keep that
label everywhere; the page's own tests check it.

`INTEGRATION.md` is the author's `instructions.md`, unchanged: how to place the
two sections in the main page, the behaviour they must keep, the data schema,
two Playwright test scripts, and the decisions not to undo. Read all of it before
integrating.

## Data

Su, J. *et al.* (2026), "Precipitation observing network gaps limit climate change
impact assessment", *Nature* 652, 119–125, Fig. 2c, rebuilt from the authors'
published data: `Figure2/all_loc_gauge_density_1degree.csv` (GitHub
JJiaSu/Precipitation-Observing-Network-Gaps-Limit-Climate-Change-Impact-Assessment;
Zenodo 10.5281/zenodo.18364510, **CC BY 4.0**). The article itself is CC BY-NC-ND, so
the page rebuilds the figure from the data rather than reproducing it.

- 15,263 land cells of 1°; 8,303 with at least one gauge. 123 cells in an eighth
  terrain class the paper does not plot are excluded.
- WMO minimum per terrain, gauges per 1,000 km²: Plains 1.74, Hilly 1.74,
  Mountains 4, Coastal 1.11, Islands 40, Urban 66.7, Polar/Arid 0.1.
- Status rule matches the paper's `density_delta < 0` on all 15,263 cells.
- Country labels repaired (India was labelled "Republic of Indonesia"; Algeria and
  North Korea truncated to "Democratic People"); source uses pre-2011 borders.
- The 0.5° dots on the map add no information: each 1° cell is shown as four dots
  with the same value, so the map matches the other layers' 0.5° look.

## Checked on 5 Oct 2026, from the repo copy

Opened from `prototypes/rain-gauges/`: both scenes render; 15,263 cells, 8,303
gauged; the Plains line reads "2,320 of 4,130 cells have a gauge", as the
instructions state; no remote scripts (only the Google Fonts link).

## Open, for the final build

- **Done 5 Oct:** on the design system (tokens, white grid and rim, globes at 70%,
  narration in the fixed place); the explorer's globe drawn at 0.5° like the map (the chart
  stays one square per 1° cell). Tests updated and passing (`tests/rain-gauges/`).
- The older `rain-gauge-density-0p5deg-dots.html` (same Prototypes folder in iCloud)
  was not copied; this file supersedes it.

## Figures on screen: quote the paper (author's rule, 5 Oct 2026)

Totals on screen are the paper's own numbers, cited to Su et al. 2026: 221,483 gauges,
13.4% of land meeting the WMO minimum, Europe 2.4 and Africa 0.09 gauges per 1,000 km².
Do not "correct" them to the data: the published Fig. 2c cells give 212,996 gauges, 13.5%,
1.99 and 0.10 because some cells were cleaned (`docs/NOTES.md`). Per-cell values in the
hover, the cards and the chart come from the data, because the paper does not publish them.
