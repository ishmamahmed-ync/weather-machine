# Handover: The Gaps in the Weather Machine

*Written 5 October 2026, at the end of a long working session. For whoever picks this
up next: a person, or Claude Code. Read this first, then `CLAUDE.md` (project rules),
`design-system/README.md` (the look) and `docs/NARRATIVE.md` (the story so far).*

Harvard GSD, Master in Design Engineering, Studio I, Project II. Author: Ishmam Ahmed.
Live site: https://ishmamahmed-ync.github.io/weather-machine/

---

## 0. Latest: the final page, end of session 2 (5 Oct 2026, late)

**Read this section first.** It supersedes older notes below where they disagree.

**What exists.** `weather-machine.html` (9.46 MB, generated, never hand-edit): the author's narrative v3
(short; the long version is only for sources: `~/Library/Mobile Documents/.../Project II/Narrative/
weather_machine_narrative_v3_short_1.txt` and `..._LONG.txt`; dossier `~/Downloads/weather_machine_research_dossier.txt`).
Build: `sh scripts/rebuild_all.sh` (or `python3 scripts/pack_final_layers.py && python3 scripts/build_all.py`).
Order: `final/sections.json`. Words and views: `SCENES` in `final/story/template.html`. How it works:
`final/README.md`. Live site (`index.html`) is untouched until the author switches.

**Architecture (decided: option A).** One shared globe for the whole page. Prototypes come in as plugins
(`WMSTORY.register`): layers drawn on the story's globe, a panel under their slide's words, step/stop hooks,
photos (`WMSTORY.photos`). Done: rain gauges (slide 5 layer, slide 8 explorer as a flow slide), history
(fills the weather-machine slides 2–5 with the era timeline), Idai (slides 10–15). Still story slides with words
only: none; every slide is built.

**Author's decisions this session** (all applied):
- Design system authoritative; slide text in one fixed place (`.wm-slide`), everything else below it; titles
  `.wm-display`; slide navigator (`.wm-nav`, 24 lines, numerals, phone "III · 7 / 24") on the main page.
- Slides 2–5 all "The weather machine", same words; instrument cards (16:9 first, then 64px rows: name + number
  of sensors); era timeline pinned at the bottom (stations 1900–60, satellites 1960–90, Argo 1990–today, gauges
  Today); the globe fills in year by year (history data); gauges reveal; globe still, turning 8°/s, centre 20°N.
- Slides 6–7 titled "The Gaps"; slide 8 keeps "Cell by cell". Radar and balloon bars both solid.
- Africa 2,119 stations; "The United States has 78,567 weather stations, 59%"; "more than three times the land".
- Su et al. figures always quoted from the paper (data differs: cleaned cells).
- Transitions: a new title fades the whole text block (0.25 s out, 0.35 s in, staggered with the camera);
  same title fades only changed parts; camera eases in-out along the great circle, 0.5–1.2 s; layers 0.6 s.
- Every photo shown (instrument photos, Idai) with "Credit to come"; author fixes attribution later.
  **They are embedded in weather-machine.html and design-system/specimen.html: clear credits before the repo
  is public.** `.gitignore` covers the photo folders and `node_modules/`.
- Maps simple and readable: one map per slide, few labels (the Beira map is central Beira only).
- Explore mode kept; D panel removed; Space = next slide (Shift+Space back).

**Revised order (the author, 5 Oct, late: `Narrative/website-text_v2.txt`).** 24 slides, six acts (I Setup ...
VI Closing the gaps). Removed: "The rich get better maps" (the AI flood-map study is now a hope story card).
After slide 17 (clarified by the author): 18 "The frontlines are responding" (the stories), 19 "What can we do to
support them?" (the line alone, empty globe), 20 works (warning map, two steps), then not-enough, money, fraying,
end, with the author's new titles.

**Next, in order.**
1. ~~Slide 14 (Idai in numbers)~~ **done:** regional map (zoom 45) with a zoom callout: small white rectangle on
   central Beira, two joining lines, big rectangle with the 8,705 graded buildings (`idai_damage`). Awaiting the
   author's look.
2. Optional, offered: smooth the switch into slide 8 (the fixed text block disappears abruptly).
3. ~~Slide 17, country profile~~ **done** (plugin `country-profile`; revised 5 Oct on the author's notes: one
   step, no rain gauges; the narration becomes the finding; bars one per line, comparison solid white, same
   thickness). The unused Su et al. gauge code and its Urban-class caveat are in docs/NOTES.md.
4. ~~Slide 18, stories~~ **done** (plugin `stories`: 22 stories from stories.json, circles on the globe, Next, ← →,
   click a circle; Space goes on to slide 19. 12 stories have their article's photo, in duotone with its
   credit (downloaded 5 Oct, licences NOT cleared; `photos/` is git-ignored, so a fresh clone needs them
   re-made: docs/NOTES.md); the rest keep the colour block).
5. ~~Slides 19-24~~ **done** (5 Oct, late): 19 Africa's stations on 0.5° cells lit first to last year, counter
   1970-2025 (878 → 1,003 in 1980 → 399); 20 locked Mozambique wipe, labels fixed; 21 the timeline (US above,
   the wider world below; it runs **2022-2026**, not 2024-26, because the world's events are from 2022-23),
   Argo then Arctic stations fade; 22 unchanged; 23 the dial and the faint gauge-gap cells; 24 every layer, gap
   cells breathing, a slow pull-out from Africa, the end card.
6. Left: the optional smoothing into slide 8; clearing the photo licences (Idai, instruments, stories); the author's look.

**Tests** (serve the repo: `python3 -m http.server 8766`, then `node tests/<name>.test.js
http://localhost:8766/weather-machine.html`): `page`, `slides`, `nav`, `history`, `idai`, `profile`, `stories`, `ending`, `transitions`,
`rain-gauges/hosted`; standalone rain gauges: `RG_SCROLL=1 node tests/rain-gauges/smoke_dots.js|smoke_scene.js
http://localhost:8766/prototypes/rain-gauges/rain-gauge-sections.html`; figures: `python3 scripts/check_figures.py`
(56 figures, 0 failed; 7 unsourced, listed in docs/FIGURES.md). All passed at the end of this session.
The app's browser pane throttles to ~2 fps: judge motion in a real browser or with Playwright.

**Nothing is committed yet** (history to 29 Sep). See section 9 before committing.

---

## 1. Start here

- **The real repository is `~/Documents/MDE Websites/weather-machine`** (GitHub Desktop).
  The copy in iCloud (`…/Harvard/Y1S1/Studio I/Project II/files/weather-machine`) is
  old and is **not** the repo; edits there never reach GitHub.
- **Nothing from 4–5 October is committed yet.** See section 9 before committing: two
  folders hold photos whose licences are not cleared.
- The author is new to web development and git. Explain what a change does and why,
  in plain language. The author commits and pushes in GitHub Desktop (two steps).
- The author works visually: screenshots and short notes. Take the intent, show the
  result, and report what was checked.

**The thesis.** The planet's observing apparatus is unevenly distributed; the gap
costs lives; the shortfall is now less about instruments than about what countries
share and what we choose to spend. Daily climate data sharing was never required
(Menne et al. 2012); GBON (2021) is the first obligation. Do not write "we are sharing
less": that was written, checked and withdrawn.

---

## 1b. If you were handed the zip

`weather-machine-handover-2026-10-05.zip` (182 MB; 478 MB, 731 files unpacked) is the whole
repository as of 5 Oct 2026, uncommitted work included, plus the raw data the builds need.

1. Unzip it. Everything is in `weather-machine/`.
2. Run `sh scripts/rebuild_all.sh` from that folder (Python 3.9+, standard library only,
   about 20 s). **Verified on 5 Oct**: unpacked into an empty folder, every build ran and all
   11 outputs (`index.html`, the grid sample, the coldspot dots, the five prototype pages,
   `satellites.csv`, the specimen, `NARRATIVE.md`) came out byte-identical to the originals.
3. Read this file, then `CLAUDE.md`, `design-system/README.md`, `docs/NARRATIVE.md`.
4. Then follow **the author's new narrative document and instructions**, given separately.
   They decide section order and copy; this file and the design system decide the rest.

**What is in it**

| | |
|---|---|
| The repository | All source, built pages, `docs/`, `design-system/`, `assets/`, and **`.git`** (history to 29 Sep; everything since is uncommitted in the working tree) |
| `data/processed/` (36 MB) | Every processed dataset the builds read |
| `data/raw/` (gitignored) | The raw files the builds read: EM-DAT export, IDMC GIDD and events, Rentschler SI, Germanwatch CRI, Natural Earth countries, WMO OSCAR export, the Idai shapefiles and imagery (UNOSAT, Copernicus EMS, NASA MODIS), the relief source `GRAY_50M_SR_W/`, and the raw **Argo index** `ar_index_global_prof.txt.gz` (added 5 Oct) |
| `docs/inputs/` | The author's original inputs: the stories spreadsheet and text file, the rain-gauge `instructions.md`, and the main site's three scene specs (Sep 2026) |
| `scripts/rebuild_all.sh` | Rebuilds everything in order |
| `scripts/coldspots_to_points.py` | Added 5 Oct from the author's `Data/Argo/`; reproduces the 10,054 coldspot dots byte-for-byte |

**What is not in it**

- The raw downloads behind `data/processed/` (GHCN-Daily station list and inventory, ISD
  history, IBTrACS, the EM-DAT flood export, MEOP lists, OBIS-SEAMAP CSVs) were not on this
  machine. The processed files are included, so every page builds; re-running the
  `scripts/clean_*` / `add_*` steps from raw would need those downloads (links in
  `docs/SOURCES.md`).
- How the 26 Argo coldspot patches (`argo_coldspots.geojson`) were drawn is not recorded.
- The author's new narrative document (supplied separately), and the Idai source text
  `Idai_text.rtf` (its words are in `prototypes/idai/template.html`).
- `data/raw/GRAY_50M_SR_W.zip` (the unzipped folder is included).

**Handle with care**: the zip holds the EM-DAT raw export (CRED terms: do not republish), MEOP
data (non-commercial), and photos whose licences are not cleared. It is for the author's
own use; do not publish it or push its photos to a public repo (section 9). On this
machine, work in the real repo (`~/Documents/MDE Websites/weather-machine`); a copy unzipped
elsewhere is a second clone of the same GitHub repo.

---

## 2. What exists

| Piece | Where | Open | Rebuild | Size | State |
|---|---|---|---|---|---|
| **Main site** | `site-src/template.html` → `index.html` | `index.html` | `python3 scripts/build_site.py` | 2.70 MB | Live. 29 scenes, Explore mode, 20 layers |
| Country profile | `prototypes/country-profile/` | `globe.html` | `python3 build_globe.py` | 1.15 MB | Year of birth (changed 5 Oct); four horizontal bars on one scale (changed 5 Oct) |
| Idai | `prototypes/idai/` | `idai.html` | `python3 build_idai.py` | 2.83 MB + 2.3 MB of `photos/` and `maps/` beside it | 8 slides standalone. In the final page since 5 Oct as a plugin of the shared globe (slides 10–15) |
| History | `prototypes/history/` | `history.html` | `python3 extract_satellites.py && python3 build_history.py` | 1.95 MB | Three chapters: stations 1900–60, satellites 1960–90, Argo 1990–2025. In the final page since 5 Oct, as a plugin of the shared globe (slide 6) |
| Stories | `prototypes/stories/` | `stories.html` | `python3 build_stories.py` | 0.71 MB | 22 stories; opens on Malawi's flood detectors, then Bangladesh's cyclone volunteers and the other flood stories, then the seals ("elephant seals" links to the seal data); Next button; animal stories show map layers |
| Rain gauges | `prototypes/rain-gauges/` | `rain-gauge-sections.html` | `python3 build_rain_gauges.py` (edit `template.html`) | 0.95 MB | On the design system and in the final page (slides 5 and 8), 5 Oct; see the note at the top of `INTEGRATION.md` |
| **Final page** | `final/` (+ `scripts/build_all.py`) | `weather-machine.html` | `python3 scripts/pack_final_layers.py && python3 scripts/build_all.py` | 4.24 MB | The narrative's 24 slides on the design system, one shared globe; rain gauges built in as a plugin (slides 5 and 8); history, Idai, country profile and stories still to come (steps 5–8). Tests in `tests/` |
| Design system | `design-system/` | `specimen.html` | `python3 build_specimen.py` | 0.36 MB | Tokens, components, globe rules, audit. Published privately: https://claude.ai/artifact/Rt68Uk889R8u4A4KJeNy6G |
| Regrid sample | `sample-land0.5-ocean1.html` | itself | `python3 scripts/regrid_layers.py` | 3.33 MB | Main site with land 0.5°, ocean 1°. A sample; **not adopted** |
| Instrument photos | `assets/instruments/` | – | – | 0.34 MB | 4 photos + `instruments.json` register (tint, crop, credit, status) |
| Narrative | `docs/NARRATIVE.md` | – | `python3 scripts/build_narrative.py` | 42 KB | Every scene and prototype in text, with sources and open questions |

**Rebuild everything**: `sh scripts/rebuild_all.sh`. **Original inputs** from the author:
`docs/inputs/`.

Each prototype folder has a `README.md`: what it shows, its sources, the checks its
build runs, and its open items. `prototypes/README.md` is the index.

Every build is standard-library Python (3.9+), run from inside its folder. Pages must
work from `file://`: no CDN scripts (d3-array and d3-geo are inlined from
`site-src/template.html`); Google Fonts is the only network request.

---

## 3. The final build: one long page, still editable piece by piece

The plan is one long page with the main story and every prototype as sections. It
stays editable per prototype **only if the combined file is generated, never edited**,
the way `index.html` is generated from `site-src/template.html` today.

**Recommended structure (not built yet):**

1. **Each prototype stays a module in its own folder**: template, data, build
   script. That folder is the only place it is edited.
2. **Each module keeps its standalone build**, so it can be opened and tested alone.
3. **A section build** (`scripts/build_site.py`, extended, or a new
   `scripts/build_all.py`) reads an ordered list of sections, takes each module's
   CSS, markup, data and script, puts shared pieces in once (d3, relief texture,
   land, `wm.css`, `wm.js`), and writes the one page.
4. **Every module namespaces everything**: CSS classes, ids, CSS variables, JS
   globals. The rain-gauge sections already do this (`rg-`, `rgm-`, zero shared ids,
   no globals but `d3`); use `prototypes/rain-gauges/INTEGRATION.md` as the model.
   The other prototypes do **not** yet. A real collision already happened on 5 Oct:
   the country profile's new bars reused the class `.track`, which the gauge meter on
   the same page also uses, and the bars came out 10px wide.
5. ~~Each section covers the story's fixed globe with its own canvas~~ **Decided 5 Oct (the author,
   option A): one shared globe.** Sliding sections over the globe broke continuity. Each prototype
   comes in as a plugin of the story's globe (layers, a panel under its slide's words, drawing and
   pointer while its slide is on screen); see `final/README.md`. Rain gauges done; history, Idai,
   the country profile and stories follow the same pattern.
6. **Explore mode must hide the sections**, and the story's hint bar and card must hide
   while a section is on screen (INTEGRATION.md §3.1 steps 6–7 apply to every section).

**Size, and one file or split.** The pieces total about 10 MB, plus Idai's 2.3 MB of
external photos and maps, which are not inlined today. Shared pieces counted once save
perhaps 1 MB (six copies of d3 at 52 KB, three of the relief texture at 256 KB).

| | Combined: one file, ~10–12 MB | Split: a small page + data and image files |
|---|---|---|
| Opening | Double-click works, offline, from a USB stick; nothing can go missing | Needs a web server (GitHub Pages is fine); a local double-click won't load the data |
| First screen | Waits for everything: ~1–3 s on fast Wi-Fi, 10–30 s+ on a phone | First scene after ~1 MB; later sections load as the reader scrolls |
| Images | Embedded as text, a third larger | Ordinary image files, cached |
| Git | Every change rewrites one 10 MB file; the repo grows fast | Only the changed file changes |

**Decided 5 Oct: combined, one file (about 10–12 MB).** So the section build must inline
everything, including Idai's photos and maps (today they sit beside `idai.html` as files),
share d3, the relief texture, land, `wm.css` and `wm.js` once, and keep the total in view.
The costs above are accepted.

---

## 4. Design system (decided; see `design-system/README.md`)

Built from an audit of all pages on 4 Oct, then extended with the author's rules on
5 Oct. Pages stay single files: build scripts inline `wm.css` and `wm.js` with
`design-system/inline.py` (`/*__WM_CSS__*/`, `/*__WM_JS__*/`).

- **Six principles**: dark ground, light data; one hue, one meaning; say what is shown
  and what is not; lines before boxes; the globe is always there; every image is framed.
- **Colour**: four text greys; one colour per instrument (stations `#FFB547`, Argo
  `#45B0CE`, seals `#6FD8B4`, sharks `#F07A55`, tracked animals `#B98CE0`, satellites
  `#CBD6E2`, coldspots `#E4EEFF`, turtles `#C6E377`, rain gauges `#3FD98A`: the
  rain-gauge prototype's green, with its 8-class density ramp and its below-minimum /
  no-gauge colours, decided 5 Oct) and per impact; Saffir-Simpson storm ramp.
- **Type**: Space Grotesk display, IBM Plex Sans text, Georgia italic for water names;
  nine roles; 16px root everywhere.
- **Shape**: radii 2px (controls, photos), 3px (cards), 50% (dots). No shadows.
- **Images (5 Oct)**: every image in a 1px white frame. 16:9 inside cards; **4:3** for big
  images beside the text, filling most of the right side (up to 56vw); 1:1 only for an
  instrument card shrunk to a row. Every image has a credit (instrument photos are
  credited in the scene's source line).
- **The globe (5 Oct)**: always on screen. Full size, or minimised to a round lens in the
  top-right corner while a big image is shown, **centred exactly on the image's top-right
  corner** (`WM.miniView()`; the image is inset one globe radius). The white lat/lon grid
  and circular edge are always visible: full 15% / 60% white (raised on 5 Oct at the
  author's request), corner 30% / 75%.
- **Instrument cards (5 Oct)**: the first time an instrument appears, a 16:9 photo tinted
  to its map colour with dot, name and one line below; when the next arrives, earlier
  ones shrink to rows (square photo, label beside). The stack is the legend. Four 16:9
  cards measure 1,056 px tall in a 360 px column; four rows, 292 px.

**Not applied yet.** No page uses `wm.css` yet. The audit table in
`design-system/README.md` lists what each page changes: e.g. Idai's photos become
framed 4:3 side images and its dark globe lines turn white; the country profile's rain
gauges stop using Argo blue; the stories card photo gets its frame; the main site's
square seal photo becomes an instrument card.

---

## 5. Data and how the author works

- **Always verify.** Cross-check every dataset against its own metadata and an independent
  figure; report what was checked and what could not be; flag mismatches, never smooth
  them over. The project is *about* data integrity; `docs/NOTES.md` is its log.
- **Ask before downloading** any file: name, source, size. Browsing and searching are fine.
- **Attribute correctly**; never fabricate; anything not real says "illustrative" where it
  appears; keys say what a layer is not (shark *sightings*, not the tagged sharks).
- Sources: `docs/SOURCES.md` (every dataset, link, date, licence, counts). Raw downloads
  (340 MB) live in `data/raw/`, gitignored. EM-DAT's raw file must not be republished.
- **New this session** (all in SOURCES.md or the prototype READMEs): WMO OSCAR/Space
  satellite export (1,052 rows, 4 Oct); Su et al. 2026 *Nature* 652 rain-gauge data
  (CC BY 4.0); March et al. 2020 *Global Change Biology* 26:586 (animal telemetry for Argo
  gaps); 18 story articles read 4 Oct; the author's four instrument photos.

**Verification tips.** Serve the repo (`python3 -m http.server 8766 -d <repo>`) and check
at 1440×900. The desktop app's browser pane is often hidden, which stops
`requestAnimationFrame`: load the page into an iframe with a stand-in clock you advance by
hand (used for the history and stories tests). Reload with `?v=N` after a rebuild; the
pane caches. Console errors can be stale from another page. jsdom does not resolve CSS
variables in `getComputedStyle`.

---

## 6. Decisions made this session (4–5 Oct)

| Decision | Where |
|---|---|
| Grid standard proposed: land 0.5°, ocean 1° (sample only; land 1° compressed US:Africa contrast from ~13:1 to 5.7:1; 0.5° keeps ~8.9:1) | `scripts/regrid_layers.py` |
| OBIS cell coordinates are cell centres, not corners; the live telemetry layer has a 1° northward error at 180° and a half-degree NE offset | `regrid_layers.py` docstring |
| History: three chapters, all layers at full strength (dimming removed); satellites = **all** OSCAR satellites that flew (871 spacecraft; 3 / 43 / 439 working in 1960 / 1990 / 2025), positions random | `prototypes/history/` |
| Stories: Next button; link arrow on the photo; Mozambique turtle story removed as the project's own idea, replaced by March et al. 2020. Later on 5 Oct: open on a sensors-and-flooding story (Malawi), flood stories first, then the seals, with "elephant seals" as an inline link (`.wm-link`) to the MEOP seal data | `prototypes/stories/` |
| Country profile: year of birth; horizontal bars on one shared scale (the largest of eight values = 100%), "at risk" included | `prototypes/country-profile/` |
| Rain-gauge prototype kept as the author delivered it, for the final build | `prototypes/rain-gauges/` |
| Design system rules above, plus (5 Oct) rain gauges take the prototype's greens and the full-size globe's lines are stronger | `design-system/` |
| **The design system is authoritative**; every page follows it and the grid standard (land 0.5°, ocean 1°) | `CLAUDE.md`, `design-system/README.md` |
| **The final page is one combined file** (~10–12 MB) | `CLAUDE.md` open decisions |
| Country profile keeps "at risk" on the shared scale | `prototypes/country-profile/` |

---

## 7. Open: decisions only the author can make

Roughly in order of how much they block the final build.

1. ~~One file or split?~~ **Decided 5 Oct: combined, one self-contained file** (section 3).
2. **Section order of the final page**: the author will settle this in a new session, from a
   **new narrative document** written for that session. Follow that document.
3. ~~Rain-gauge colour~~ **Decided 5 Oct: the rain-gauge prototype's greens**, now in the
   design system (`--wm-gauge` `#3FD98A`, `--wm-gauge-0…7`).
4. **Photos and licences**: the author will clear credits, replace the "satellite" photo (a
   SpaceX Dragon cargo capsule, not an Earth-observation satellite) and confirm the bridge
   photo shows a rain gauge, **before the final commit**. Until then see section 9: git keeps
   every committed file in its history.
5. **Unsourced figures on the live site**: Michael 74 deaths; Haiyan 6,352 dead and 1,071
   missing; US$25.5 bn vs US$2.98 bn; "24 hours of warning cuts damage by about 30%";
   Mozambique 34 million people; "no national flood map"; upstream Limpopo gauges;
   Xai-Xai 55% of built-up area. And the Idai impact figures (likely the Government of
   Mozambique PDNA).
6. **Figures that differ from a recheck**: seals 74% (recomputed 75.7%); Africa 2,166
   stations (2,119 by country list: define "Africa"); Africa median record 68 vs 69 years.
7. **Idai**: "Category 4" vs IBTrACS Category 3; "51 days" is 52; 603 deaths is Mozambique
   only; animation order.
8. **Stories**: which of the 21 fit "those least responsible … coping" (several hope and
   animal stories are about wealthy places); Yangtze headline says "four-year" ban, the
   source says ten-year; finish the subtitle ("are …").
9. **Main-site scene 24** (Mozambique turtles) is the same proposal removed from the
   stories: cite March et al. 2020 or reframe it as a proposal.
10. **Caveats** removed from screen on 28 Sep (illustrative dots, "as recorded in IBTrACS",
    geocoding, G-1): restore on screen or on a `/data` page.
11. ~~Grid standard~~ **Decided 5 Oct: land 0.5°, ocean 1° on every page, the main site
    included.** Still to do (section 8): the main site (re-check the US scene's "merge into a
    solid surface" at 0.5°: it mostly holds, contrast ~8.9:1), the stories' ocean layers, and
    the country profile's gauge and station dots, which move from 0.1° locations to 0.5°
    cells (their legend must then say "cells with a gauge"). Per page, checked 5 Oct:

    | Page | Land | Ocean |
    |---|---|---|
    | History | 0.5° ✓ | Argo 1° ✓ |
    | Stories | – | Argo 1.5°, seals 0.5°, sharks / tracked animals / coldspots 1° (copied from the live site's layers, so tracked animals still carry the 180° bug). Fix: pack at 1° with `regrid_layers.py`, as history does |
    | Country profile | rain gauges and stations as 0.1° dots (they mark gauge locations, not counts per cell, so 0.5° would change their meaning) | – |
    | Rain gauges | Drawn at 0.5° like every land sensor (ruled 5 Oct). The data exists only at 1° (Su et al. publish counts per 1° cell; no gauge locations), so each 0.5° dot carries its 1° cell's value and the hover says so. The explorer's **chart** stays one square per 1° cell, because it counts cells against the WMO minimum; its **globe** is drawn at 0.5° | – |
    | Main site | stations 0.25° | Argo 1.5°, seals 0.5° |
    | Design system demo | 0.5° ✓ | 1° ✓ |
12. **History**: end at 2025 or 2020 (Argo coverage dips after 2020 because cells go quiet);
    chapter 2–3 panel copy is placeholder.
13. **Flood blues** on the main site (`#2E6FA3`, `#4FC3F7`) vs the system's `#7DB4D1`.
14. **Answered 5 Oct**: full-size globe lines stronger (done: 15% / 60%); the white border
    stays round the instrument card's photo only; **"at risk" stays** on the country
    profile's shared scale.

---

## 8. Open: work that needs no decision

1. **Build the section architecture** (section 3): namespace each prototype, then write
   the combined build, **one self-contained file**. Start with the rain-gauge sections,
   which are ready.
2. **Move every page onto the design system, which is authoritative** (audit table in
   `design-system/README.md`). Prototypes first; the live main site last.
3. **Put every page on the grid standard**, land 0.5° / ocean 1° (decision 11): main site,
   stories, country profile.
   - **Country profile: switch its rain gauges to the Su et al. data** (decided 5 Oct), the same
     cells as the rain-gauge explorer, drawn as 0.5° dots carrying their 1° cell's value, with
     the explorer's status colours; its gauge bar compares against the Su et al. WMO minimum
     for the country's terrain instead of the single 575 km² rule. (Narrative slide 17.)
   - **Narrative slide 21**: no new datasets; fade out the existing layers (Argo, then
     stations north of the Arctic Circle).
4. **`scripts/pack_layers.py`**: the processed-data → `globe-data.json` packing is still
   ad hoc (CLAUDE.md).
5. **`/data` and `/notes` pages** from `SOURCES.md` and `NOTES.md`; hover on storms and floods.
6. **Housekeeping**: README's repository layout still lists a `site/` folder (the site is
   `index.html` at the root); the repo must become public for the instructors.
7. **`docs/NARRATIVE.md`** is generated by `scripts/build_narrative.py` (scene text, Idai
   slides and stories copied from source; the per-scene notes are hand-written in the
   script). Rerunning overwrites the file: edit the script, or write elsewhere.
8. **Coldspot patches**: `scripts/coldspots_to_points.py` (found and added 5 Oct) turns the 26
   patches into dots and reproduces them exactly, but how the patches themselves
   (`argo_coldspots.geojson`, 48.1 million km²) were drawn is still not recorded.

---

## 9. Before the next commit

`git status` on 5 Oct: modified `CLAUDE.md`, `docs/SOURCES.md`, `index.html`,
`scripts/build_site.py`, `site-src/template.html`; new `assets/`, `design-system/`,
`docs/NARRATIVE.md`, `prototypes/`, `scripts/make_relief.py`, `scripts/regrid_layers.py`,
`site-src/layers/relief.webp.b64`, and the regrid sample files.

- **Do not commit unlicensed photos to a repo that will be public**:
  `prototypes/idai/photos/` (8 agency-looking photos, credits blank) and
  `assets/instruments/` (4 photos, credits unconfirmed). The author will clear the credits
  before the final commit, but **anything committed earlier stays in git's history** even
  after it is deleted, and would be visible once the repo is public. So leave both folders
  unticked in GitHub Desktop (or add them to `.gitignore`) until their licences are cleared.
- **Leave the regrid sample unticked** (`sample-land0.5-ocean1.html`,
  `site-src/layers/globe-data-land0.5-ocean1.json`) unless it is adopted.
- New this session: `scripts/build_narrative.py`, `HANDOVER.md`.
- `index.html` and `site-src/template.html` were already modified before this session
  (the relief globe work). Verified 5 Oct: `build_site.py` on the current template produces
  the current `index.html` byte-for-byte. Check the live page after pushing.
- New on 5 Oct for the zip: `scripts/rebuild_all.sh`, `scripts/coldspots_to_points.py`,
  `docs/inputs/`, `data/processed/argo_coldspots_centroids.geojson`, and the raw Argo index in
  `data/raw/` (gitignored).
- Commit, then push: two separate steps in GitHub Desktop. Pages redeploys in 2–3 minutes.
