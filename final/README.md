# The final page

One self-contained file, `weather-machine.html` at the repo root, holding the story and
every prototype as sections. **Generated: never edit it by hand.**

```
python3 scripts/build_all.py      # writes weather-machine.html
```

| File | What it is | Edit it? |
|---|---|---|
| `sections.json` | The order of the page: runs of story scenes, and prototype sections between them | Yes, to reorder |
| `story/template.html` | The story: the 24 slides of the author's narrative (`SCENES`, words only, no HTML), layers, the globe engine, Explore mode. Started 5 Oct 2026 as a copy of `site-src/template.html` | Yes: words and views in `SCENES` |
| `story/layers/extra.json` | Layers the live site's data lacks (storm tracks with their season), laid over the grid-standard base data by name. Built by `scripts/pack_final_layers.py` | No: rebuild it |
| `scripts/build_all.py` | Reads both, takes each prototype from its own folder, shares d3 and the design system once, checks, writes the page | Only to add a prototype |

The live site (`index.html`, built from `site-src/template.html`) is untouched by this
build. Switching the live site to the final page is the author's decision, at the end.

## One shared globe (option A, decided 5 Oct 2026)

The whole page has **one globe**: the story's. A prototype never brings its own globe into the
final page; it comes in as a **plugin** of that globe, so the camera always moves on from where it
was and nothing slides over the globe like a new page. A plugin, registered with
`WMSTORY.register(name, {...})` from the prototype's own code, can give:

| Part | What the story does with it |
|---|---|
| `layers: { key(ctx, proj, alpha) }` | draws it like any layer; a slide's `views` fade it in and out (`LAYERS.key.plugin = name`) |
| a panel (in `sections.json`, `"panels"`) | mounts it under the words of the slide that names the plugin (`plugin:` in `SCENES`) |
| `draw(ctx, proj)` | calls it every frame while that slide is on screen |
| `hover`, `dblclick`, `doubletap`, `leave`, `home` | while that slide is on screen the globe takes drag, Ctrl/⌘ + scroll and the zoom buttons, and passes these on |
| `attach(api)` | hands it `api.flyTo(lon, lat, zoom)`, `api.redraw()`, `api.animate(ms)`, `api.R()`, `api.canvas` |

The same prototype code still draws its own globe in its standalone page (it checks for
`window.WMSTORY`). Rain gauges were the first: slide 5's map is the `gauges` layer; the explorer is a flow slide
(`flow:true`, its text scrolls with the page) carrying the explorer's panel. History is the second: its
three layers fill in the weather-machine slides year by year, following the era timeline pinned under the
instrument cards (`ERAS` and each slide's `era:` in `SCENES`); the story sets the plugin's year and runs it
while its layers are on. (A plugin can also own a slide with steps: `step(view)` as each step arrives,
`stop()` when the slide is left.) Idai is the third: its layers draw the maps of slides 10 to 15, and a view
with `photo:` (a photo a plugin registered in `WMSTORY.photos`) shows the design system's side image and puts
the globe in the corner lens. The country profile is the fourth: slide 17 "Since you were born"; its panel (fields, bars)
mounts under the words, the plugin replaces the slide's narration with the finding once a country and year are
chosen, and flies the camera to the country (`api.flyTo`). The stories are the fifth: slide 18, one step; the plugin draws the circles
(an interactive plugin: `draw`, `click`, `hover`), fills the card under the words and moves the camera and the
story's layers together (`api.view({lon, lat, z, layers})`). Space always goes on to the next slide.

Slides 19 to 24 use the story's own parts: `below.events` (a dated timeline, design system `.wm-events`),
`below.dial` (`.wm-dial`), a timeline layer with first and last years (`af_decay`, with a live counter), layers that
borrow another layer's brightness (`maxOf`), and on a view `zoomFrom` + `slow` (arrive close, pull slowly out) and
`pulse` (those layers breathe, none with reduced motion).

## How a prototype gets in

Each prototype stays in its own folder and keeps its own standalone page. `build_all.py`
has one small adapter per prototype that returns its styles, its markup (one entry per
part, so the parts can go in different places), its data and its code. Every id and
class in a prototype carries its prefix (`rg-` and `rgm-` for the rain gauges), and the
build refuses a page with a repeated id.

In the page, a prototype section covers the story's fixed globe with its own canvas.
While one is on screen the story's card, hint and wipe handle hide (`body[data-mod]`),
and Explore mode hides them all.

## How a slide is drawn

Every slide's words sit in one fixed place, the design system's `.wm-slide`: label (the
act), title, narration, then below a rule everything else (legend, bars, stats, notes),
then the source line. The block is built once, one element per part; moving to the next
slide redraws only the parts that change, so a shared title (the four "The weather
machine" slides, the two "The Gaps" slides) never flickers. A slide with several `views`
keeps its words while the camera moves. Space, Page Down or Down goes to the next slide or
section; Shift+Space goes back.

- **Instrument cards** (`cards:` in `SCENES`): the design system's rows, a square photo with
  the instrument's name, photos from `assets/instruments/`. The stack grows one card per
  slide and is the legend.
- **The slide navigator** (`"nav": true` in `sections.json`): the design system's `.wm-nav`,
  one line per slide in the left margin; `tests/nav.test.js`. `final/mock-navigator.json`
  builds the two-slide mock it was approved on.

## Tests

Serve the repo (`python3 -m http.server 8766`), then from the repo root:

```
node tests/page.test.js http://localhost:8766/weather-machine.html
node tests/slides.test.js http://localhost:8766/weather-machine.html
node tests/nav.test.js http://localhost:8766/weather-machine.html
node tests/history.test.js http://localhost:8766/weather-machine.html
node tests/idai.test.js http://localhost:8766/weather-machine.html
node tests/transitions.test.js http://localhost:8766/weather-machine.html
node tests/rain-gauges/hosted.test.js http://localhost:8766/weather-machine.html      # the explorer on the shared globe
RG_SCROLL=1 node tests/rain-gauges/smoke_dots.js http://localhost:8766/prototypes/rain-gauges/rain-gauge-sections.html
RG_SCROLL=1 node tests/rain-gauges/smoke_scene.js http://localhost:8766/prototypes/rain-gauges/rain-gauge-sections.html
python3 scripts/check_figures.py
```

The two `smoke_` tests are the author's acceptance tests from `INTEGRATION.md`, now run on the standalone page; `hosted.test.js` runs the explorer's checks on the shared globe.
