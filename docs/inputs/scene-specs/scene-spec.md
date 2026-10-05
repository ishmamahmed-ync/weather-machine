# The Gaps in the Weather Machine — scene spec

Copy and direction for every scene. Written to be handed to Claude Code, which
should translate each block into one entry in the `SCENES` array in
`site-src/template.html`, then run `python scripts/build_site.py`.

---

## How to read a block

```
CAMERA    center:[lon, lat]  zoom:N        real coordinates; the engine negates for d3
LAYERS    name:opacity                     names must match the LAYERS object
MODE      bare | quote | boxed             bare = no box, quote = large pull quote
COPY                                       the text, as HTML
NOTE                                       anything the builder needs to know
```

**Layers available now:** `stations`, `usable`, `years`, `argo`, `seals`,
`sharks`, `telemetry`, `st_decay`, `sats_shell`, `fl_deaths`, `fl_affected`,
`fl_damage`, `storms`, `michael`, `haiyan`, `xx_before`, `xx_water`, `xx_lost`,
`fema`, `aiextra`.

**Wipes available:** `us`, `mozambique`, `xaixai`.

Four scenes need data that does not exist yet. They are marked
**NEEDS DATA** and listed again at the end.

---

# ACT ONE — the machine gets built

## 1. Before instruments

```
CAMERA  center:[-40, 12]  zoom:0.86
LAYERS  (none)
MODE    bare
```

> For as long as there have been people, there have been storms that no one
> could see coming.
>
> Harvests, voyages, cities: all of it staked on a sky that gave no notice. We
> read omens, prayed, consulted oracles, and built calendars to guess at the
> flood.

**NOTE** Dark earth, nothing on it. Hold this one longer than the rest.

---

## 2. The telegraph makes weather knowable

```
CAMERA  center:[10, 45]  zoom:1.05
LAYERS  stations:0.7
MODE    bare
```

> Then we began to measure — and, more importantly, to tell each other.
>
> Weather moves at roughly the speed of a horse. The telegraph moves at the
> speed of light. Once an observation could outrun the storm it described,
> forecasting became possible for the first time, and nations began wiring
> their observers together. The International Meteorological Organization was
> founded in 1873.

**NOTE** This fills your blank in scene 2. The telegraph is the right answer
rather than "the industrial age" — synoptic meteorology is a communications
invention, not an instrument one. Stations fade up over Europe first, since
that is where the network began.

---

## 3. Satellites

```
CAMERA  center:[30, 12]  zoom:0.68
LAYERS  sats_shell:1, stations:0.25
MODE    bare
```

> On 1 April 1960, TIROS-1 returned the first television picture of a cloud
> field from orbit. Within a decade the planet was being photographed
> continuously.
>
> A satellite sees everything and touches nothing. It measures radiance at the
> top of the atmosphere, not the temperature of the air where people live.

**NOTE** The shell is illustrative, not orbital — geostationary orbit is 6.6
Earth radii out and will not fit beside the planet at any honest scale. Say so
in a footnote if there is room.

---

## 4. Floats

```
CAMERA  center:[-150, 0]  zoom:0.88
LAYERS  argo:1, stations:0.2
MODE    boxed
```

> **3,375,214**
> ocean profiles from 20,530 drifting floats
>
> The newest layer, not the oldest. The Argo array began deploying in 1999; the
> first profile in the global index is dated 28 July 1997. Every ten days each
> float sinks to two kilometres, drifts, then rises measuring temperature and
> salinity, and reports by satellite when it surfaces.

**NOTE** Chronology matters here. Your sequence had floats before satellites;
it is the other way round. Stations 1800s, satellites 1960, floats 2000.

---

# ACT TWO — the machine is uneven

## 5. The machine is incomplete

```
CAMERA  center:[20, 10]  zoom:0.9
LAYERS  stations:1, argo:0.3
MODE    quote
```

> Three centuries of instruments, and the planet still cannot see itself
> evenly.

---

## 6. A century of data

```
CAMERA  center:[-98, 39]  zoom:1.8
LAYERS  stations:1
MODE    boxed
```

> **76,708**
> stations across the contiguous United States
>
> Here the instruments crowd so densely that the continent stops reading as
> points and becomes a lit surface. One country holds 59% of every weather
> station on Earth.

**NOTE** One honest qualification, worth including: 53,167 of those are
volunteer rain gauges installed since 1998, precipitation only. The US network
is wide and shallow.

---

## 7. Sparse, young, falling apart

```
CAMERA  center:[20, 2]  zoom:1.6
LAYERS  stations:1
MODE    boxed
```

> **2,166**
> stations across the whole of Africa
>
> One rotation east, the same layer. Nothing was switched off for this view.
>
> And the surviving African stations are not young — their median record is 68
> years, against 8 in the United States. The network is old, small, and mostly
> no longer reporting.

**NOTE** The record-length inversion is counterintuitive and worth keeping. It
stops the scene reading as "poor countries have new, bad equipment".

---

## 8. Where there is enough data, AI can fill in

```
CAMERA  center:[-96, 38]  zoom:2.45
WIPE    us
LAYERS  (none — the wipe carries it)
MODE    bare
```

> Where a map is already half drawn, a model can finish it.
>
> FEMA has mapped about a third of America's river channels in sixty years. A
> generative model learned the relationship between terrain and floodplain from
> that third and extended it across the rest, at 30-metre resolution.
>
> Drag the handle. It found **11 million people** and **4.1 million buildings**
> standing in flood zones that no official map recorded.

**NOTE** Attribution: Wu, Zhang & Stouffs, *Nature Communications* 17:5983
(2026). Not AlphaGeo, who built the website presenting it. The dots in this
wipe are illustrative — sampled from a density, not real locations.

---

## 9. Where there is not, the gap widens

```
CAMERA  center:[35, -18]  zoom:2.45
WIPE    mozambique
LAYERS  stations:1
MODE    bare
```

> And where the map was never drawn, there is nothing to learn from.
>
> The handle does not move. Mozambique has no national flood hazard map, so the
> model has nothing to train on and nothing to be checked against. The method
> transfers, in its authors' own words, only *where high-quality local data
> exists*.
>
> A model trained on the well-measured world improves fastest where measurement
> is already best. This is not the method failing. It is the method working
> exactly as described.

---

## 10. Asymmetric consequences

```
CAMERA  center:[14, 8]  zoom:0.92
LAYERS  stations:0.35
MODE    quote
```

> What happens to a place that cannot see itself?

---

## 11. Hurricane Michael

```
CAMERA  center:[-86, 29]  zoom:3.0
LAYERS  michael:1, storms:0.18, stations:0.5
MODE    bare
```

> **Hurricane Michael**, 10 October 2018. 125 knots at landfall on the Florida
> Panhandle.
>
> The storm was tracked for days across the densest observing network on Earth.
> Warnings ran ahead of it. Evacuation orders moved people inland.
>
> **74 people died.**

---

## 12. Typhoon Haiyan

```
CAMERA  center:[125, 11]  zoom:3.0
LAYERS  haiyan:1, storms:0.18
MODE    bare
```

> **Typhoon Haiyan**, 8 November 2013. Also 125 knots. Also 204 hours from
> first fix to last.
>
> **6,352 people died.** A further 1,071 were never found.
>
> Michael cost $25.5 billion. Haiyan cost $2.98 billion. Sort the century's
> storms by dollars and Michael is a catastrophe. Sort them by lives and it
> barely appears.

**NOTE** Both storms are 125 kt and 204 h in IBTrACS, which is what makes the
pairing work. Say "as recorded in IBTrACS" — other agencies rate Haiyan far
higher.

---

## 13. It is costing lives

```
CAMERA  center:[24, 4]  zoom:1.05
LAYERS  stations:0.9
MODE    boxed
```

> **636 vs 37**
> weather radars, US and EU against Africa
>
> The US and EU share 636 weather radars for 1.1 billion people. Africa, with
> 1.2 billion, has 37.
>
> Twenty-four hours' notice of a hazard reduces the damage it does by about a
> third. Without stations, there is no notice.

**NOTE** Friederike Otto, "Without Warning: A Lack of Weather Stations Is
Costing African Lives", *Yale Environment 360*, 31 October 2023. The 30% figure
is the Global Commission on Adaptation, via WMO.

---

## 14. Africa, land and sea

```
CAMERA  center:[25, -5]  zoom:1.5
LAYERS  stations:1, argo:0.8
MODE    bare
```

> The thinning runs offshore as well. Argo covers the world ocean more evenly
> than any land network — but coverage in the Mozambique Channel runs at
> **2,108 profiles per million square kilometres**, against a global average of
> **5,936**, and **10,033** in the Gulf Stream.

**NOTE** Verified from the Argo index. State it as relative, not as absence —
the Channel has 7,115 profiles, not zero. Part of the sparseness is physical:
Argo floats need about two kilometres of water and avoid shelves.

---

## 15. Mozambique

```
CAMERA  center:[35, -18]  zoom:2.6
LAYERS  stations:1, argo:0.5
MODE    boxed
```

> **19**
> weather stations in Mozambique. 14 have both a long record and current data.
>
> 800,000 square kilometres, 34 million people, 2,700 kilometres of coast
> facing a cyclone basin. Nineteen stations.
>
> And nine of its major river basins begin in other countries. Less than a
> tenth of the water that floods the Limpopo valley is generated inside
> Mozambique — the rest arrives from South Africa, Botswana and Zimbabwe, past
> gauges Mozambique does not own and cannot read.

**NOTE** Verified: 19 stations, 16 active, 14 with a 30-year record and current
data. The transboundary figure is FAO's Limpopo assessment.

---

## 16. The Limpopo

```
CAMERA  center:[33.44, -24.87]  zoom:52
WIPE    xaixai
LAYERS  (none)
MODE    bare
```

> The lower Limpopo, around Xai-Xai. Drag the handle.
>
> Magenta is built ground. Blue is where the water stands on the later date.
> **55% of the built area in this frame is under water.**

---

# ACT THREE — the pattern, and the trend

## 17. A pattern, worldwide

```
CAMERA  center:[30, 14]  zoom:0.86
LAYERS  fl_affected:1, fl_deaths:1
MODE    boxed
```

> Every flood recorded since 2016. **Yellow** is people affected. **Red** is
> people killed.
>
> Africa carries 27% of the deaths. Europe carries 1.5%.
>
> People in Africa, South Asia, Central and South America and small island
> states are **fifteen times more likely** to die in a climate disaster.

**NOTE** The 15× figure is WMO/SOFF. Flag in a footnote that EM-DAT supplied
coordinates for only 12% of these events, so most points are province or
country centroids.

---

## 18. And it is getting worse

```
CAMERA  center:[22, 0]  zoom:1.2
LAYERS  stations:0.8
MODE    boxed
```

> **−50%**
> African radiosonde reports reaching global forecast models, 2015 to 2020
>
> Weather balloons are how the atmosphere above a place gets measured, and
> global forecast models depend on them. Africa's contribution halved in five
> years, and has fallen further since.
>
> Under the WMO's minimum standard, least-developed countries and small island
> states currently report **9%** of the required surface stations and **13%** of
> the required upper-air stations.

**NOTE** Source: SOFF, un-soff.org/operations and the WMO GBON Baseline 2023.
Be precise: the 50% is African radiosondes reaching global models, not "early
warning systems" as a whole.

---

## 19. From the era of the mean to the era of deviation

```
CAMERA  center:[-40, 14]  zoom:0.84
LAYERS  storms:0.9
MODE    quote
```

> We are leaving the era of the mean and entering the era of standard
> deviation.
>
> *— Olivier Hamant*

Then, in the smaller line beneath:

> The average stops describing the conditions you have to survive. Damage moves
> into the tails. Which raises the value of a forecast at exactly the moment a
> forecast becomes harder to make — because reading a tail requires a long local
> record, and that is the one input no budget can buy quickly.

**NOTE** Attribute the framing to Hamant rather than asserting rising variance
as settled. A shifted mean and a widened distribution both move damage into the
tail, so the argument holds either way.

---

## 20. Which is why warning matters

```
CAMERA  center:[14, 12]  zoom:0.88
LAYERS  stations:0.25
MODE    quote
```

> "Early warnings are not an abstraction. They give farmers the power to
> protect their crops and livestock. Enable families to evacuate safely. And
> protect entire communities from devastation. We know that disaster-related
> mortality is at least six times lower in countries with good early-warning
> systems in place."
>
> *— António Guterres, UN Secretary-General, 22 October 2025*

---

## 21. Early Warnings for All

```
CAMERA  center:[14, 12]  zoom:0.88
LAYERS  stations:0.5
MODE    boxed
```

> **$3.1 billion**
> to put every person on Earth under a warning system, 2023 to 2027
>
> Fifty cents per person per year. 329 projects are tracked across 127
> countries.
>
> More than half of all national investment goes to just five of them: China,
> Bangladesh, India, Pakistan and Indonesia.

**NOTE** Even the funding for the gap is unevenly distributed. That detail is
from the WMO/SOFF Global Observatory.

---

## 22. Warning coverage, 2023

```
CAMERA  center:[14, 10]  zoom:0.9
LAYERS  NEEDS DATA
MODE    boxed
```

> In 2023, roughly half the world's countries reported having a multi-hazard
> early warning system.

**NEEDS DATA** — there is no early-warning-coverage layer in the project. WMO
publishes MHEWS coverage by country in its *Global Status of Multi-Hazard Early
Warning Systems* reports. Someone needs to download the country table and build
a choropleth layer. Until then, either cut scenes 22 and 23 or replace them with
the GBON compliance figures from scene 18, which we do have.

---

## 23. Warning coverage, 2025

```
CAMERA  center:[14, 10]  zoom:0.9
LAYERS  NEEDS DATA
MODE    boxed
```

> By 2025 that share had risen. The map is filling in — unevenly, and from a
> very low base in the places that need it most.

**NEEDS DATA** — same source as scene 22. Both years must come from the same
WMO series, or the comparison is meaningless.

---

# ACT FOUR — what is being done

## 24. The frontlines are stepping up

```
CAMERA  center:[20, -5]  zoom:1.3
LAYERS  stations:0.7
MODE    bare
```

> The countries least responsible for the problem are the ones building the
> instruments.
>
> In 2021 all 193 members of the WMO adopted the Global Basic Observing Network
> — the first time in a century and a half of international meteorology that
> sharing basic observations became an obligation rather than a favour.

**NOTE** This scene needs a concrete example to earn its claim. GBON adoption
is the strongest thing we have verified, so I have used it. If you want a named
national programme, that needs sourcing — the current copy does not name one
because I cannot verify one.

---

## 25. Scientists are finding other ways

```
CAMERA  center:[-30, 14]  zoom:0.84
LAYERS  argo:0.9, stations:0.2
MODE    quote
```

> If you cannot afford to build a network, borrow one that is already moving.

---

## 26. Seals

```
CAMERA  center:[30, -70]  zoom:1.0
LAYERS  seals:1, argo:0.45
PHOTO   seal, tinted #6FD8B4
MODE    boxed
```

> **74%**
> of ocean profiles south of 65°S come from seals
>
> Argo floats become trapped under sea ice and stop. Southern elephant seals
> carrying conductivity and temperature sensors dive beneath it anyway, and
> surface to transmit.
>
> Half a million profiles from water no machine reaches in winter. No agency
> designed this network. It works because the animals were already going there.

---

## 27. Sharks

```
CAMERA  center:[-68, 34]  zoom:1.3
LAYERS  sharks:1, argo:0.35, seals:0.3
MODE    boxed
```

> **40%**
> reduction in Gulf Stream surface temperature forecast error
>
> Twenty-eight blue sharks and one mako, tagged with depth and temperature
> sensors, swam through continental shelf water that Argo samples thinly. Their
> 8,200 profiles more than doubled the record that existed there.
>
> Twenty-nine animals. No new satellites, no new budget line.

**NOTE** McDonnell, Kirtman, Braun & Hammerschlag, *npj Climate and Atmospheric
Science* 9:147 (2026).

---

## 28. And the animals already in the gap

```
CAMERA  center:[42, -18]  zoom:2.0
LAYERS  telemetry:1, argo:0.4, stations:0.6
MODE    boxed
```

> **315**
> marine species already tracked, carrying no sensors
>
> Leatherback and loggerhead turtles migrate through the Mozambique Channel —
> the same water Argo samples at a third of the global rate, and where not one
> seal profile has ever been taken.
>
> They are tracked for conservation. They carry positions, not measurements.
> Instrumenting them would close an observing gap and fund the monitoring that
> protects them, with the same tag.

**NOTE, PART NEEDS DATA** — the `telemetry` layer exists and contains turtles
(leatherback across 508 cells, loggerhead across 1,105), but it is not broken
out by species or filtered to the Mozambique Channel. To show turtles
specifically, filter `obis-species-by-cell.csv` to *Dermochelys coriacea* and
*Caretta caretta* and build a new layer. Verified: zero MEOP seal cells in the
Mozambique Channel.

---

## 29. But instruments still have to be paid for

```
CAMERA  center:[20, 5]  zoom:1.1
LAYERS  NEEDS DATA (radiosonde stations), stations:0.6
MODE    bare
```

> Animals cannot measure rainfall over Chókwè, and no tag gives a district a
> thirty-year record.
>
> The unglamorous things still have to be built: radiosonde stations,
> streamflow gauges upstream of the border, dams with telemetry, housing that
> stands, and an agreement to keep the readings flowing across borders.

**NEEDS DATA** — there is no radiosonde layer. WMO OSCAR/Surface
(oscar.wmo.int/surface) lists upper-air stations and can be filtered and
downloaded. Without it, run the scene on `stations` alone; the copy still works.

---

## 30. A fraction of what we spend on AI

```
CAMERA  center:[10, 16]  zoom:0.84
LAYERS  stations:0.15
MODE    boxed
```

> **$2.7 trillion**
> worldwide spending on artificial intelligence in 2026, up 49.5% in a year
>
> Gartner's own analyst calls the data-centre buildout *the largest
> infrastructure project humanity has ever undertaken*.
>
> Set against $3.1 billion over five years for a global warning system, that is
> about **870 to 1**. The entire five-year programme costs less than two days of
> it.

**NOTE** Gartner, September 2026. The daily figure is $1.65 billion; $3.1 bn is
1.9 days.

---

## 31. Bratton

```
CAMERA  center:[6, 14]  zoom:0.82
LAYERS  stations:0.2, argo:0.2, seals:0.3, sharks:0.4, telemetry:0.5
MODE    quote
```

> "In its current commercial form, the primary purpose of planetary-scale
> computation is to measure and model individual people in order to predict
> their next impulse. But a more aspirational goal would be to contribute to the
> comprehension, composition and enforcement of a shared future that is more
> rich, diverse and viable."
>
> *— Benjamin Bratton, Planetary Sapience*

---

## 32. Close

```
CAMERA  center:[6, 14]  zoom:0.82
LAYERS  stations:0.55, argo:0.3, seals:0.4, sharks:0.5, telemetry:0.5
MODE    quote
```

> We built an artificial sense organ for a natural world, and then declined to
> pay for the half of it that watches the poor.
>
> More instruments, in the places that have none.
> Seawalls. Dams. Housing that stands.
> And an agreement to keep the readings flowing.

---

# Needs data before it can be built

| scene | what is missing | where to get it |
|---|---|---|
| 22, 23 | Early warning system coverage by country, 2023 and 2025 | WMO *Global Status of Multi-Hazard Early Warning Systems*. Both years must come from the same series. |
| 28 | Turtle telemetry, filtered to the Mozambique Channel | Already inside `obis-species-by-cell.csv`. Filter to *Dermochelys coriacea* and *Caretta caretta*, build a new layer. |
| 29 | Radiosonde / upper-air station locations | WMO OSCAR/Surface, `oscar.wmo.int/surface`. Has an API and bulk export. |

Scenes 22 and 23 are the only two that cannot run at all without new data. If
the deadline is tight, cut them and let scene 18 carry the trend — it has the
verified figures.

---

# Numbers used, and where each comes from

| figure | source |
|---|---|
| 3,375,214 Argo profiles, 20,530 floats | Argo GDAC index, downloaded 2026-09-23 |
| 76,708 US stations; 2,166 African; 59% share | GHCN-Daily, downloaded 2026-09-15 |
| median record 8 yr US, 68 yr Africa | GHCN-Daily inventory join |
| 19 Mozambique stations, 14 usable | GHCN-Daily |
| 2,108 / 5,936 / 10,033 Argo profiles per M km² | computed from the Argo index |
| zero MEOP seal cells in the Mozambique Channel | computed from MEOP |
| Michael 125 kt, 204 h, 74 deaths, $25.5 bn | IBTrACS and NHC |
| Haiyan 125 kt, 204 h, 6,352 deaths, $2.98 bn | IBTrACS and NDRRMC |
| Africa 27% of flood deaths, Europe 1.5% | EM-DAT, computed |
| 15× more likely to die | WMO / SOFF |
| 636 radars vs 37 | Otto, Yale Environment 360, 31 Oct 2023 |
| 24 h notice cuts damage ~30% | Global Commission on Adaptation, via WMO |
| −50% African radiosondes 2015–2020 | SOFF, un-soff.org/operations |
| 9% surface, 13% upper-air in LDCs and SIDS | WMO GBON Baseline 2023 |
| mortality 6× lower with warning systems | Guterres, 22 Oct 2025 |
| $3.1 bn, 50c per person, 329 projects, 127 countries | UN / WMO EW4All |
| 74% of profiles south of 65°S from seals | MEOP and Argo, computed |
| 29 sharks, 8,200 profiles, 40% error reduction | McDonnell et al. 2026 |
| 11 m people, 4.1 m buildings, 69% / 81% | Wu, Zhang & Stouffs 2026 |
| $2.7 trillion AI spend 2026, +49.5% | Gartner, September 2026 |
| 55% of built area flooded at Xai-Xai | computed from the two satellite scenes |
