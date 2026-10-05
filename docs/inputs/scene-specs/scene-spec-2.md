# The Gaps in the Weather Machine — scene spec

Copy and direction for every scene. Hand this to Claude Code, which should turn
each block into one entry in the `SCENES` array in `site-src/template.html`,
then run `python scripts/build_site.py`.

---

## On the register

The copy is written after Bratton's *Planetary Sapience*: long sentences with
subordinate clauses, abstract nouns as subjects, triads, and the defining
move — *it names*, *it is*, *what it reveals*. One concrete anchor per scene,
then a lift into what the anchor means.

Two deliberate modulations. The framing scenes carry the full register. The
data scenes carry one or two sentences and then the number, because a station
count does not need philosophy wrapped around it and thirty-two consecutive
paragraphs of theory would be unreadable on a scrolling page.

Bratton's own vocabulary is borrowed where it fits exactly and is attributed
where it is quoted: *epistemological accomplishment*, *distributed sensory
organ*, *epistemological technology*, *unrequested demystification*.

---

## How to read a block

```
CAMERA    center:[lon, lat]  zoom:N     real coordinates; the engine negates for d3
LAYERS    name:opacity                  names must match the LAYERS object
MODE      bare | quote | boxed
COPY                                    the text, as HTML
NOTE                                    anything the builder needs
```

**Layers available:** `stations`, `usable`, `years`, `argo`, `seals`, `sharks`,
`telemetry`, `st_decay`, `sats_shell`, `fl_deaths`, `fl_affected`, `fl_damage`,
`storms`, `michael`, `haiyan`, `xx_before`, `xx_water`, `xx_lost`, `fema`,
`aiextra`. **Wipes:** `us`, `mozambique`, `xaixai`.

Scenes 22, 23, 28 and 29 need data that does not exist yet. They are marked and
listed again at the end.

---

# ACT ONE — the organ grows

## 1. Before instruments

```
CAMERA  center:[-40, 12]  zoom:0.86
LAYERS  (none)
MODE    bare
```

> Consider the planet as it was for almost all of its four-and-a-half-billion
> year career: a body entirely capable of storms and entirely incapable of
> registering them. Weather happened, and nothing kept an account of it.
>
> Human societies lived inside that ignorance and built what they could to
> compensate. We read omens in the sky, consulted oracles, and made calendars
> to anticipate the flood, and the harvests and voyages and cities that
> depended on those guesses failed at the rate you would expect.

**NOTE** Dark earth, nothing drawn. Hold longer than the scenes that follow.

---

## 2. The telegraph

```
CAMERA  center:[10, 45]  zoom:1.05
LAYERS  stations:0.7
MODE    bare
```

> Weather travels at roughly the speed of a horse. Electricity travels at the
> speed of light. From the moment an observation could outrun the storm it
> described, a forecast became something other than a prophecy, and the
> instruments that had been accumulating in gardens and observatories for a
> century acquired a use they had never had in isolation.
>
> What followed was less an invention than a wiring together. Nations
> connected their observers to each other, and in 1873 formalised the
> arrangement as the International Meteorological Organization. Measurement
> became a shared undertaking, which is also to say it became a political one.

**NOTE** This fills the blank in your original scene 2. The telegraph rather
than "the industrial age", because synoptic meteorology is a communications
achievement and not an instrumental one. Stations should fade up over Europe
first, where the network began.

---

## 3. Satellites

```
CAMERA  center:[30, 12]  zoom:0.68
LAYERS  sats_shell:1, stations:0.25
MODE    bare
```

> On 1 April 1960, TIROS-1 returned the first television image of a cloud field
> from orbit, and within a decade the planet was being photographed
> continuously by machines it had itself, at several removes, produced.
>
> This is the layer that does most of the looking and none of the touching. A
> satellite measures radiance at the top of the atmosphere, from which the
> state of the air below is inferred rather than observed. It is an
> extraordinary instrument for the surface of things and a poor one for the
> two metres above the ground where crops grow and people live.

**NOTE** The shell is illustrative rather than orbital. Geostationary orbit sits
at 6.6 Earth radii and will not fit beside the planet at any honest scale; say
so in a footnote if there is room.

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
> The newest layer of the apparatus, not the oldest. Every ten days each float
> sinks to two kilometres, drifts with whatever current it finds, then rises
> measuring temperature and salinity and reports what it found by satellite
> before sinking again. The first profile in the global index is dated 28 July
> 1997, which makes the systematic measurement of the ocean interior younger
> than most of the people reading this.

**NOTE** Chronology: stations are 19th century, satellites 1960, floats 1999.
Your original sequence had floats before satellites. The reordering matters,
because the newest layer being the ocean is itself part of the argument.

---

# ACT TWO — the organ is uneven

## 5. An incomplete organ

```
CAMERA  center:[20, 10]  zoom:0.9
LAYERS  stations:1, argo:0.3
MODE    quote
```

> The knowledge that the planet is warming is not a discovery so much as an
> epistemological accomplishment, assembled out of instruments.
>
> Which means it can only be assembled where the instruments are.

**NOTE** The first line is a close paraphrase of Bratton: "The knowledge of
'climate change' is an epistemological accomplishment of planetary-scale
computation." Either attribute it or quote it directly.

---

## 6. A century of record

```
CAMERA  center:[-98, 39]  zoom:1.8
LAYERS  stations:1
MODE    boxed
```

> **76,708**
> stations across the contiguous United States
>
> At this density the instruments stop reading as points and resolve into a
> surface, which is what a distributed sensory organ looks like when it is
> actually distributed. One country holds 59% of every weather station on
> Earth.
>
> The density is also shallower than it appears. Some 53,167 of those stations
> are volunteer rain gauges installed since 1998, measuring precipitation only.

---

## 7. Sparse, old, and going quiet

```
CAMERA  center:[20, 2]  zoom:1.6
LAYERS  stations:1
MODE    boxed
```

> **2,166**
> stations across the whole of Africa
>
> One rotation east, the same layer, nothing switched off for the view.
>
> The surviving African stations are not young, which is the part that
> confounds expectation. Their median record runs to 68 years against 8 years
> in the United States. This is not an immature network but an old one that has
> been contracting, and the instruments that remain are largely inherited from
> the period in which they were installed by someone else.

---

## 8. Where the map is half drawn

```
CAMERA  center:[-96, 38]  zoom:2.45
WIPE    us
LAYERS  (none — the wipe carries it)
MODE    bare
```

> A model can finish a map that is already half drawn. FEMA has mapped roughly
> a third of America's river channels over sixty years, and a generative model
> trained on that third learned the relationship between terrain and floodplain
> well enough to extend it across the rest at thirty-metre resolution.
>
> Drag the handle. What the completion revealed was 11 million people and 4.1
> million buildings standing in flood zones that no official map had recorded,
> which is an unrequested demystification of the ordinary kind: the risk was
> always there, and the instrument that found it merely made it sayable.

**NOTE** Attribution is Wu, Zhang & Stouffs, *Nature Communications* 17:5983
(2026), not AlphaGeo, who built the website presenting it. The dots in this
wipe are sampled from a density and are illustrative.

---

## 9. Where it was never drawn

```
CAMERA  center:[35, -18]  zoom:2.45
WIPE    mozambique
LAYERS  stations:1
MODE    bare
```

> The handle does not move here, because there is no second map to reveal.
> Mozambique has no national flood hazard layer, so the model has nothing to
> learn the relationship from and nothing against which its answer could be
> checked. Its authors are explicit that the method transfers only where
> high-quality local data already exists.
>
> An intelligence trained on the well-measured world will improve fastest where
> measurement is already best. This is not a failure of the technique. It is
> the technique operating exactly as specified, and inheriting the geography of
> the archive it was trained on.

---

## 10. The consequence is asymmetric

```
CAMERA  center:[14, 8]  zoom:0.92
LAYERS  stations:0.35
MODE    quote
```

> What becomes of a place that has not been given the means to see itself?

---

## 11. Hurricane Michael

```
CAMERA  center:[-86, 29]  zoom:3.0
LAYERS  michael:1, storms:0.18, stations:0.5
MODE    bare
```

> Hurricane Michael came ashore on the Florida Panhandle on 10 October 2018 at
> 125 knots, having been tracked for days across the densest observing network
> on the planet. Warnings preceded it, evacuation orders moved people inland,
> and the apparatus did what it had been built over a century to do.
>
> **74 people died.**

---

## 12. Typhoon Haiyan

```
CAMERA  center:[125, 11]  zoom:3.0
LAYERS  haiyan:1, storms:0.18
MODE    bare
```

> Typhoon Haiyan crossed the Philippines on 8 November 2013 at 125 knots,
> having lasted, from first fix to last, the same 204 hours as Michael. By the
> two measures the archive records — intensity and duration — these are the
> same storm occurring in two different worlds.
>
> **6,352 people died**, and a further 1,071 were never found.
>
> Michael cost $25.5 billion and Haiyan cost $2.98 billion, so a ledger kept in
> dollars ranks Michael as the catastrophe and Haiyan as the smaller event.

**NOTE** Both are 125 kt and 204 h in IBTrACS, which is what makes the pairing
work. Say "as recorded in IBTrACS"; other agencies rate Haiyan considerably
higher.

---

## 13. The cost of not being told

```
CAMERA  center:[24, 4]  zoom:1.05
LAYERS  stations:0.9
MODE    boxed
```

> **636 against 37**
> weather radars in the US and EU, against Africa
>
> The United States and the European Union share 636 weather radars between 1.1
> billion people. Africa, with 1.2 billion, has 37.
>
> Twenty-four hours of notice reduces the damage a hazard does by about a
> third, which is the most favourable ratio available anywhere in adaptation.
> The notice requires an instrument.

**NOTE** Friederike Otto, "Without Warning: A Lack of Weather Stations Is
Costing African Lives", *Yale Environment 360*, 31 October 2023. The 30% figure
is the Global Commission on Adaptation via WMO.

---

## 14. The thinning runs offshore

```
CAMERA  center:[25, -5]  zoom:1.5
LAYERS  stations:1, argo:0.8
MODE    bare
```

> Argo distributes itself more evenly than any land network, because a float
> goes where the ocean takes it and the ocean is indifferent to borders and to
> budgets. Even so the distribution is not uniform. Coverage in the Mozambique
> Channel runs at 2,108 profiles per million square kilometres against a global
> average of 5,936, and against 10,033 in the Gulf Stream.
>
> Some of that is physical, since a float needs two kilometres of water beneath
> it and avoids shelves. The remainder is the ordinary consequence of who
> deploys the instruments.

**NOTE** Verified from the Argo index. State it as relative; the Channel holds
7,115 profiles, not zero.

---

## 15. Mozambique

```
CAMERA  center:[35, -18]  zoom:2.6
LAYERS  stations:1, argo:0.5
MODE    boxed
```

> **19**
> weather stations in Mozambique, of which 14 hold both a long record and
> current data
>
> Eight hundred thousand square kilometres, 34 million people, and 2,700
> kilometres of coast facing a cyclone basin, observed by nineteen instruments.
>
> Nine of its major river basins begin somewhere else. Less than a tenth of the
> water that floods the Limpopo valley is generated inside the country; the
> rest arrives from South Africa, Botswana and Zimbabwe, past gauges Mozambique
> neither owns nor is entitled to read. Its exposure is transboundary and its
> instruments are national, and no quantity of domestic investment closes that
> gap.

**NOTE** Verified: 19 stations, 16 active, 14 with a 30-year record and current
data. The transboundary figure is FAO's Limpopo assessment.

---

## 16. The lower Limpopo

```
CAMERA  center:[33.44, -24.87]  zoom:52
WIPE    xaixai
LAYERS  (none)
MODE    bare
```

> What the record does hold is the aftermath. This is the lower Limpopo around
> Xai-Xai, before and after. Magenta is built ground and blue is where the
> water stands on the later date.
>
> **55% of the built area in this frame is underwater.**

---

# ACT THREE — the pattern, and the direction of travel

## 17. The same shape everywhere

```
CAMERA  center:[30, 14]  zoom:0.86
LAYERS  fl_affected:1, fl_deaths:1
MODE    boxed
```

> Every flood in the record since 2016, with yellow for people affected and red
> for people killed. Africa carries 27% of the deaths and Europe carries 1.5%.
>
> People in Africa, South Asia, Central and South America and small island
> states are fifteen times more likely to die in a climate disaster than people
> elsewhere, and the distribution of instruments is one of the reasons why.

**NOTE** The 15× figure is WMO/SOFF. Footnote that EM-DAT supplied coordinates
for only 12% of these events, so most points are province or country centroids.

---

## 18. And the direction is downward

```
CAMERA  center:[22, 0]  zoom:1.2
LAYERS  stations:0.8
MODE    boxed
```

> **−50%**
> African radiosonde reports reaching global forecast models, 2015 to 2020
>
> A weather balloon is how the atmosphere above a place gets measured, and
> every global forecast model depends on a supply of them. Africa's
> contribution halved across five years and has fallen further since.
>
> Against the WMO's minimum standard, the least-developed countries and small
> island states currently report 9% of the required surface stations and 13% of
> the required upper-air stations. The apparatus is not merely uneven. In the
> places that need it most it is contracting.

**NOTE** SOFF, un-soff.org/operations, and the WMO GBON Baseline 2023. Be
precise: the 50% is African radiosondes reaching global models, not early
warning systems in general.

---

## 19. From the era of the mean to the era of deviation

```
CAMERA  center:[-40, 14]  zoom:0.84
LAYERS  storms:0.9
MODE    quote
```

> "We are leaving the era of the mean and entering the era of the standard
> deviation."
>
> *— Olivier Hamant*

Smaller, beneath:

> The average stops describing the conditions that have to be survived, and
> damage migrates into the tails of the distribution. This raises the value of
> a forecast at precisely the moment a forecast becomes harder to produce,
> because reading a tail requires a long local record and a record is the one
> input that cannot be acquired quickly at any price.

**NOTE** Attribute the framing to Hamant rather than asserting rising variance
as settled. A shifted mean and a widened distribution both move damage into the
tail, so the argument survives either way.

---

## 20. Warning

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
> to place every person on Earth under a warning system, 2023 to 2027
>
> Fifty cents per person per year, across 329 projects in 127 countries.
>
> More than half of all national investment in early warning goes to five
> countries: China, Bangladesh, India, Pakistan and Indonesia. The financing
> for the gap reproduces the shape of the gap.

---

## 22. Coverage, 2023

```
CAMERA  center:[14, 10]  zoom:0.9
LAYERS  NEEDS DATA
MODE    boxed
```

> In 2023, about half the world's countries reported holding a multi-hazard
> early warning system of any kind.

**NEEDS DATA** — no early-warning-coverage layer exists. WMO publishes MHEWS
coverage by country in its *Global Status of Multi-Hazard Early Warning
Systems* reports. Download the country table and build a choropleth. Until
then, either cut 22 and 23, or let scene 18 carry the trend on figures we have.

---

## 23. Coverage, 2025

```
CAMERA  center:[14, 10]  zoom:0.9
LAYERS  NEEDS DATA
MODE    boxed
```

> By 2025 the share had risen. The map is filling in, unevenly, and from a very
> low base in the places where the consequences of not being warned are worst.

**NEEDS DATA** — same source as 22. Both years must come from the same series
or the comparison means nothing.

---

# ACT FOUR — an artificial response

## 24. The obligation to share

```
CAMERA  center:[20, -5]  zoom:1.3
LAYERS  stations:0.7
MODE    bare
```

> The countries that contributed least to the problem are the ones now
> installing the instruments, and in 2021 all 193 members of the World
> Meteorological Organization adopted the Global Basic Observing Network.
>
> For the first time in a century and a half of international meteorology, the
> exchange of basic observations became an obligation rather than a courtesy.
> The commons had not been dismantled at some earlier point. It had never been
> constructed.

**NOTE** GBON adoption is the strongest verified example available for this
scene. If you want a named national programme it needs sourcing; the copy does
not name one because I could not verify one.

---

## 25. Borrowing a network

```
CAMERA  center:[-30, 14]  zoom:0.84
LAYERS  argo:0.9, stations:0.2
MODE    quote
```

> If a network cannot be afforded, it can sometimes be borrowed from something
> already in motion.

---

## 26. Seals

```
CAMERA  center:[30, -70]  zoom:1.0
LAYERS  seals:1, argo:0.45
PHOTO   seal, tinted #6FD8B4
MODE    boxed
```

> **74%**
> of ocean profiles south of 65°S are collected by seals
>
> Argo floats become trapped beneath sea ice and stop reporting, which leaves
> the Southern Ocean in winter unobservable by the instrument designed to
> observe oceans. Southern elephant seals carrying conductivity and temperature
> sensors dive beneath that ice regardless and surface to transmit.
>
> Half a million profiles from water no machine reaches in winter. No agency
> designed this network, and it functions because the animals were going there
> in any case.

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
> Twenty-eight blue sharks and one mako, carrying depth and temperature tags,
> swam through the continental shelf water that Argo samples thinly because
> floats avoid shallow ground. Their 8,200 profiles more than doubled the
> record that existed for that water, and assimilating them cut surface
> temperature forecast error by up to forty percent.
>
> Twenty-nine animals, no new satellites, and no new budget line.

**NOTE** McDonnell, Kirtman, Braun & Hammerschlag, *npj Climate and Atmospheric
Science* 9:147 (2026).

---

## 28. The platforms already in the gap

```
CAMERA  center:[42, -18]  zoom:2.0
LAYERS  telemetry:1, argo:0.4, stations:0.6
MODE    boxed
```

> **315**
> marine species already tracked, none of them carrying sensors
>
> Leatherback and loggerhead turtles migrate through the Mozambique Channel,
> which is the same water Argo samples at a third of the global rate and in
> which not a single seal profile has ever been taken. They are tracked already,
> for conservation, and what they return is position and nothing else.
>
> An instrumented turtle would close an observing gap and fund the monitoring
> that protects it, from the same tag. The infrastructure is swimming.

**NOTE, PART NEEDS DATA** — the `telemetry` layer contains turtles (leatherback
across 508 cells, loggerhead across 1,105) but is not broken out by species or
filtered to the Channel. Filter `obis-species-by-cell.csv` to *Dermochelys
coriacea* and *Caretta caretta* and build a new layer. Verified: zero MEOP seal
cells in the Mozambique Channel.

---

## 29. The unglamorous half

```
CAMERA  center:[20, 5]  zoom:1.1
LAYERS  NEEDS DATA (radiosondes), stations:0.6
MODE    bare
```

> No animal measures rainfall over Chókwè, and no tag gives a district the
> thirty-year record it needs to size a culvert or price a crop. The borrowed
> network extends the apparatus into places machines cannot go; it does not
> substitute for the apparatus.
>
> What remains to be paid for is the part nobody photographs. Radiosonde
> stations, streamflow gauges upstream of the border, dams with telemetry
> attached, housing that survives the water, and a standing agreement that the
> readings cross the border when the water does.

**NEEDS DATA** — no radiosonde layer. WMO OSCAR/Surface
(oscar.wmo.int/surface) lists upper-air stations with an API and bulk export.
Without it, run the scene on `stations` alone; the copy still holds.

---

## 30. What we spend instead

```
CAMERA  center:[10, 16]  zoom:0.84
LAYERS  stations:0.15
MODE    boxed
```

> **$2.7 trillion**
> worldwide spending on artificial intelligence in 2026, an increase of 49.5%
> in a single year
>
> Gartner's own analyst describes the data-centre buildout as the largest
> infrastructure project humanity has ever undertaken, and on the numbers he is
> correct. Set against $3.1 billion over five years for a global warning
> system, the ratio is roughly 870 to 1, and the entire five-year programme
> costs less than two days of it.
>
> Planetary-scale computation is not virtual. It is being built, at enormous
> physical expense, and what it is being built to do is a choice.

**NOTE** Gartner, September 2026. Daily figure is $1.65 billion; $3.1 bn is 1.9
days. The closing sentence echoes Bratton's "Planetary-scale computation is not
virtual. It is a kind of terraforming of its host planet."

---

## 31. Bratton

```
CAMERA  center:[6, 14]  zoom:0.82
LAYERS  stations:0.2, argo:0.2, seals:0.3, sharks:0.4, telemetry:0.5
MODE    quote
```

> "In its current commercial form, the primary purpose of planetary-scale
> computation is to measure and model individual people in order to predict
> their next impulse. But a more aspirational goal would be to contribute to
> the comprehension, composition and enforcement of a shared future that is
> more rich, diverse and viable."
>
> *— Benjamin Bratton, Planetary Sapience*

---

## 32. Close

```
CAMERA  center:[6, 14]  zoom:0.82
LAYERS  stations:0.55, argo:0.3, seals:0.4, sharks:0.5, telemetry:0.5
MODE    quote
```

> The planet grew a sensory organ over three centuries, and the organ is
> unevenly innervated. Where it can feel, it can prepare; where it cannot, the
> same storm arrives as a surprise and leaves a different number of people
> alive.
>
> This is not a natural condition and it was not arrived at accidentally. It
> was built, which means it can be built differently.

---

# Needs data before it can be built

| scene | what is missing | where to get it |
|---|---|---|
| 22, 23 | Early warning coverage by country, 2023 and 2025 | WMO *Global Status of Multi-Hazard Early Warning Systems*. Both years from the same series. |
| 28 | Turtle telemetry filtered to the Mozambique Channel | Already inside `obis-species-by-cell.csv`. Filter to *Dermochelys coriacea* and *Caretta caretta*. |
| 29 | Radiosonde and upper-air station locations | WMO OSCAR/Surface, `oscar.wmo.int/surface`. |

Only 22 and 23 cannot run at all. If the deadline is tight, cut them and let
scene 18 carry the trend, since its figures are verified.

---

# Figures used, and where each comes from

| figure | source |
|---|---|
| 3,375,214 Argo profiles from 20,530 floats | Argo GDAC index, downloaded 2026-09-23 |
| 76,708 US stations; 2,166 African; 59% share | GHCN-Daily, downloaded 2026-09-15 |
| median record 8 yr US, 68 yr Africa | GHCN-Daily inventory join |
| 19 Mozambique stations, 14 usable | GHCN-Daily |
| 2,108 / 5,936 / 10,033 Argo profiles per million km² | computed from the Argo index |
| zero MEOP seal cells in the Mozambique Channel | computed from MEOP |
| Michael 125 kt, 204 h, 74 deaths, $25.5 bn | IBTrACS and NHC |
| Haiyan 125 kt, 204 h, 6,352 deaths, $2.98 bn | IBTrACS and NDRRMC |
| Africa 27% of flood deaths, Europe 1.5% | EM-DAT, computed |
| fifteen times more likely to die | WMO / SOFF |
| 636 radars against 37 | Otto, *Yale Environment 360*, 31 Oct 2023 |
| 24 hours' notice cuts damage by about a third | Global Commission on Adaptation via WMO |
| −50% African radiosondes 2015–2020 | SOFF, un-soff.org/operations |
| 9% surface and 13% upper-air in LDCs and SIDS | WMO GBON Baseline 2023 |
| mortality at least six times lower with warning | Guterres, 22 Oct 2025 |
| $3.1 bn, 50c per person, 329 projects, 127 countries | UN / WMO EW4All |
| 74% of profiles south of 65°S from seals | MEOP and Argo, computed |
| 29 sharks, 8,200 profiles, 40% error reduction | McDonnell et al. 2026 |
| 11 m people and 4.1 m buildings, 69% / 81% | Wu, Zhang & Stouffs 2026 |
| $2.7 trillion AI spend in 2026, +49.5% | Gartner, September 2026 |
| 55% of built area flooded at Xai-Xai | computed from the two satellite scenes |
