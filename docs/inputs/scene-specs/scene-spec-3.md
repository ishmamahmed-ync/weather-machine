# The Gaps in the Weather Machine — scene spec

Copy and direction for all 32 scenes. Hand to Claude Code. Each block becomes
one entry in the `SCENES` array in `site-src/template.html`. Then run
`python scripts/build_site.py`.

**Layers:** `stations`, `usable`, `years`, `argo`, `seals`, `sharks`,
`telemetry`, `st_decay`, `sats_shell`, `fl_deaths`, `fl_affected`, `fl_damage`,
`storms`, `michael`, `haiyan`, `xx_before`, `xx_water`, `xx_lost`, `fema`,
`aiextra`. **Wipes:** `us`, `mozambique`, `xaixai`.

**Modes:** `bare` (no box), `quote` (large text, no box), `boxed` (card with a
number).

Scenes 22, 23, 28 and 29 need data we don't have yet. Marked below.

---

## 1

	center:[-40, 12]  zoom:0.86   layers: none   mode: bare

Humans have tried to predict the weather since the beginning of civilisation.
Our crops, our voyages and our lives depended on it. We prayed to gods,
consulted oracles and made calendars to guess when the floods would come.

None of it worked.

---

## 2

	center:[10, 45]  zoom:1.05   layers: stations:0.7   mode: bare

Then we started to measure.

Weather moves at the speed of a horse. A telegram moves at the speed of light.
Once a warning could travel faster than the storm, forecasting became possible.
Countries wired their weather stations together, and in 1873 they formed the
International Meteorological Organization.

**NOTE** This fills your blank in scene 2. The telegraph, not the industrial
age. Stations should appear over Europe first.

---

## 3

	center:[30, 12]  zoom:0.68   layers: sats_shell:1, stations:0.25   mode: bare

In 1960 we started sending up satellites.

TIROS-1 sent back the first picture of clouds from orbit on 1 April. Within ten
years the whole planet was being photographed all day, every day.

But a satellite looks down from the top of the atmosphere. It cannot measure the
air two metres off the ground, where crops grow and people live.

**NOTE** The shell is illustrative, not real orbits. Geostationary satellites
are 6.6 Earth radii out and won't fit next to the planet at true scale.

---

## 4

	center:[-150, 0]  zoom:0.88   layers: argo:1, stations:0.2   mode: boxed

**3,375,214**
ocean profiles from 20,530 floats

In 1999 we started dropping floats into the ocean. Every ten days each one
sinks two kilometres, drifts, then rises measuring temperature and salinity, and
radios what it found.

This is the newest part of the network, not the oldest. We have only been
measuring the deep ocean properly for 25 years.

**NOTE** Your original order had floats before satellites. It's the other way
round: stations 1800s, satellites 1960, floats 1999.

---

## 5

	center:[20, 10]  zoom:0.9   layers: stations:1, argo:0.3   mode: quote

We built a machine to watch the weather.

But not all places have the same view of the storm.

---

## 6

	center:[-98, 39]  zoom:1.8   layers: stations:1   mode: boxed

**76,708**
weather stations in the continental United States

There are so many that they stop looking like dots and turn into a solid
surface. One country holds 59% of all the weather stations on Earth.

Most of them are new. 53,167 are volunteer rain gauges put up since 1998, and
they only measure rain.

---

## 7

	center:[20, 2]  zoom:1.6   layers: stations:1   mode: boxed

**2,166**
weather stations in all of Africa

Same layer, one turn of the globe east. Nothing has been switched off.

The African stations are not new. Their median record is 68 years, against 8
years in the US. The network is old and shrinking, not young and growing.

---

## 8

	center:[-96, 38]  zoom:2.45   wipe: us   layers: none   mode: bare

Where there is already a lot of data, AI can fill in the gaps.

FEMA has mapped about a third of America's rivers in sixty years. Researchers
trained a model on that third and used it to predict the rest at 30-metre
resolution.

Drag the handle. The model found 11 million people and 4.1 million buildings in
flood zones that no official map had recorded.

**NOTE** Wu, Zhang & Stouffs, *Nature Communications* 17:5983 (2026). Not
AlphaGeo, who built the website about it. The dots are illustrative.

---

## 9

	center:[35, -18]  zoom:2.45   wipe: mozambique   layers: stations:1   mode: bare

Where there isn't, it can't.

The handle doesn't move. Mozambique has no national flood map, so there is
nothing for a model to learn from and nothing to check its answer against. The
authors say so themselves: the method only works where good local data already
exists.

AI makes the best-measured places better measured. That is not a bug. It is how
it works.

---

## 10

	center:[14, 8]  zoom:0.92   layers: stations:0.35   mode: quote

So what happens to a place that can't see the weather coming?

---

## 11

	center:[-86, 29]  zoom:3.0   layers: michael:1, storms:0.18, stations:0.5   mode: bare

Hurricane Michael hit the Florida Panhandle on 10 October 2018 at 125 knots.

It was tracked for days. Warnings went out ahead of it. People were evacuated.

**74 people died.**

---

## 12

	center:[125, 11]  zoom:3.0   layers: haiyan:1, storms:0.18   mode: bare

Typhoon Haiyan hit the Philippines on 8 November 2013, also at 125 knots. It
lasted 204 hours, exactly as long as Michael.

**6,352 people died.** Another 1,071 were never found.

Michael cost $25.5 billion. Haiyan cost $2.98 billion. Measured in money,
Michael was the bigger disaster.

**NOTE** Both are 125 kt and 204 h in IBTrACS, which is what makes the pair
work. Say "as recorded in IBTrACS" — other agencies rate Haiyan higher.

---

## 13

	center:[24, 4]  zoom:1.05   layers: stations:0.9   mode: boxed

**636 vs 37**
weather radars in the US and EU, vs Africa

The US and EU have 636 radars for 1.1 billion people. Africa has 37 for 1.2
billion.

24 hours of warning cuts the damage from a disaster by about 30%. But you need
instruments to give the warning.

**NOTE** Friederike Otto, "Without Warning: A Lack of Weather Stations Is
Costing African Lives", *Yale Environment 360*, 31 October 2023.

---

## 14

	center:[25, -5]  zoom:1.5   layers: stations:1, argo:0.8   mode: bare

The gap continues out to sea.

Argo floats spread out more evenly than any land network, because they drift
wherever the ocean takes them. But the Mozambique Channel gets 2,108 profiles
per million square kilometres. The global average is 5,936. The Gulf Stream
gets 10,033.

**NOTE** Verified from the Argo index. Say it as a comparison, not as absence —
the Channel has 7,115 profiles. Some of the gap is physical: floats need 2 km
of water and avoid shallow areas.

---

## 15

	center:[35, -18]  zoom:2.6   layers: stations:1, argo:0.5   mode: boxed

**19**
weather stations in Mozambique. 14 have both a long record and current data.

800,000 square kilometres. 34 million people. 2,700 kilometres of coast facing
a cyclone basin. Nineteen stations.

And nine of its main rivers start in other countries. Less than a tenth of the
water that floods the Limpopo comes from inside Mozambique. The rest comes down
from South Africa, Botswana and Zimbabwe, past gauges Mozambique doesn't own.

**NOTE** Verified: 19 stations, 16 active, 14 with a 30-year record and current
data. Transboundary figure is FAO's Limpopo assessment.

---

## 16

	center:[33.44, -24.87]  zoom:52   wipe: xaixai   layers: none   mode: bare

Here is what happened in the lower Limpopo, around Xai-Xai.

Drag the handle. Magenta is built-up ground. Blue is where the water sits
afterwards.

**55% of the built-up area in this frame is underwater.**

---

## 17

	center:[30, 14]  zoom:0.86   layers: fl_affected:1, fl_deaths:1   mode: boxed

Every flood recorded since 2016. Yellow is people affected. Red is people
killed.

Africa has 27% of the deaths. Europe has 1.5%.

People in Africa, South Asia, Latin America and small island states are 15
times more likely to die in a climate disaster.

**NOTE** The 15× figure is WMO/SOFF. Footnote that EM-DAT gave coordinates for
only 12% of these events, so most points are province or country centroids.

---

## 18

	center:[22, 0]  zoom:1.2   layers: stations:0.8   mode: boxed

**−50%**
African weather balloon reports reaching global forecast models, 2015 to 2020

Weather balloons measure the atmosphere above a place. Every global forecast
model needs them. Africa's reports halved in five years, and have dropped
further since.

Against the WMO's minimum standard, the poorest countries and small island
states have 9% of the surface stations they need and 13% of the upper-air ones.

It isn't just uneven. It's getting worse.

**NOTE** SOFF, un-soff.org/operations, and WMO GBON Baseline 2023. Be precise:
the 50% is African radiosondes reaching global models, not early warning
systems generally.

---

## 19

	center:[-40, 14]  zoom:0.84   layers: storms:0.9   mode: quote

"We are leaving the era of the mean and entering the era of the standard
deviation."

*— Olivier Hamant*

Smaller, underneath:

The average stops telling you what to prepare for. The damage moves into the
extremes. That makes forecasting more valuable and harder at the same time,
because you need decades of local records to know what an extreme even is.

**NOTE** Attribute the framing to Hamant. Don't assert rising variance as
settled — a shifted average and a wider spread both push damage into the tails,
so the point holds either way.

---

## 20

	center:[14, 12]  zoom:0.88   layers: stations:0.25   mode: quote

"Early warnings are not an abstraction. They give farmers the power to protect
their crops and livestock. Enable families to evacuate safely. And protect
entire communities from devastation. We know that disaster-related mortality is
at least six times lower in countries with good early-warning systems in place."

*— António Guterres, UN Secretary-General, 22 October 2025*

---

## 21

	center:[14, 12]  zoom:0.88   layers: stations:0.5   mode: boxed

**$3.1 billion**
to put every person on Earth under an early warning system, 2023 to 2027

That's 50 cents per person per year. 329 projects across 127 countries.

More than half of the national spending goes to five countries: China,
Bangladesh, India, Pakistan and Indonesia. Even the funding is uneven.

---

## 22

	center:[14, 10]  zoom:0.9   layers: NEEDS DATA   mode: boxed

But things are starting to look a little better. 

In 2022, about half the world's countries had an early warning system of any
kind.

**NEEDS DATA** — Use the Sendai Monitor Data, Show 2022 first 

---

## 23

	center:[14, 10]  zoom:0.9   layers: NEEDS DATA   mode: boxed

By 2025 more countries had one. The map is filling in, but slowly, and from a
very low starting point in the places that need it most.

**NEEDS DATA** — same source as 22. Both years must come from the same report
series or the comparison is meaningless.

---

## 24

	center:[20, -5]  zoom:1.3   layers: stations:0.7   mode: bare

The countries that caused the least of this are the ones now building the
instruments.

In 2021 all 193 WMO member countries signed up to the Global Basic Observing
Network. For the first time, sharing basic weather observations became a
requirement rather than a favour.

**NOTE** GBON is the strongest verified example for this scene. If you want a
named national programme, it needs sourcing — I couldn't verify one.

---

## 25

	center:[-30, 14]  zoom:0.84   layers: argo:0.9, stations:0.2   mode: quote

Scientists are also finding cheaper ways to collect the data.

---

## 26

	center:[30, -70]  zoom:1.0   layers: seals:1, argo:0.45   photo: seal (#6FD8B4)   mode: boxed

**74%**
of ocean profiles south of 65°S are collected by seals

Argo floats get trapped under sea ice and stop working. So scientists put
temperature and salinity sensors on southern elephant seals, which dive under
the ice anyway and come up to transmit.

Half a million profiles from water no machine can reach in winter. Nobody
planned this network. It works because the seals were already going there.

---

## 27

	center:[-68, 34]  zoom:1.3   layers: sharks:1, argo:0.35, seals:0.3   mode: boxed

**40%**
lower forecast error for sea surface temperature in the Gulf Stream

In 2026 researchers tagged 28 blue sharks and one mako with depth and
temperature sensors. The sharks swam through shelf water that Argo floats
avoid because it's too shallow.

Their 8,200 profiles more than doubled the record for that water. Feeding them
into the forecast cut surface temperature errors by up to 40%.

29 animals. No new satellites. No new budget.

**NOTE** McDonnell, Kirtman, Braun & Hammerschlag, \*npj Climate and Atmospheric
Science\* 9:147 (2026).

---

## 28

	center:[42, -18]  zoom:2.0   layers: telemetry:1, argo:0.4, stations:0.6   mode: boxed

**315**
marine species already being tracked, none carrying sensors

Leatherback and loggerhead turtles migrate through the Mozambique Channel. That
is the same water Argo samples at a third of the global rate, and where no seal
has ever been tagged.

They are already tracked for conservation. The tags send back position and
nothing else.

Put a sensor on one and you close an ocean data gap and fund the monitoring
that protects it, with the same device.

**NOTE, PART NEEDS DATA** — the `telemetry` layer has turtles in it (leatherback
in 508 cells, loggerhead in 1,105) but isn't split by species. Filter
`obis-species-by-cell.csv` to *Dermochelys coriacea* and *Caretta caretta* and
build a new layer. Verified: zero seal cells in the Mozambique Channel.

---

## 29

	center:[20, 5]  zoom:1.1   layers: NEEDS DATA (radiosondes), stations:0.6   mode: bare

But animals can't measure rainfall over Chókwè. And no tag gives a district the
30 years of records it needs to size a drain or price a crop.

The boring things still have to be paid for. Weather balloon stations. River
gauges upstream, across the border. Dams with sensors on them. Houses that
survive the water. And an agreement that the readings get shared when the flood
is coming.

**NEEDS DATA** — no radiosonde layer. WMO OSCAR/Surface
(oscar.wmo.int/surface) lists upper-air stations and has bulk export. Without
it, run the scene on `stations` alone; the copy still works.

---

## 30

	center:[10, 16]  zoom:0.84   layers: stations:0.15   mode: boxed

**$2.7 trillion**
worldwide spending on AI in 2026, up 49.5% in one year

Gartner's own analyst calls the data centre buildout the largest infrastructure
project humanity has ever undertaken.

The early warning plan costs $3.1 billion over five years. That's a ratio of
about 870 to 1. The whole five-year programme costs less than two days of AI
spending.

**NOTE** Gartner, September 2026. $1.65 billion a day, so $3.1 bn is 1.9 days.

---

## 31

	center:[6, 14]  zoom:0.82   layers: stations:0.2, argo:0.2, seals:0.3, sharks:0.4, telemetry:0.5   mode: quote

"In its current commercial form, the primary purpose of planetary-scale
computation is to measure and model individual people in order to predict their
next impulse. But a more aspirational goal would be to contribute to the
comprehension, composition and enforcement of a shared future that is more
rich, diverse and viable."

*— Benjamin Bratton, Planetary Sapience*

---

---

# Needs data

| scene  | missing                                          | source                                                                                         |
| ------ | ------------------------------------------------ | ---------------------------------------------------------------------------------------------- |
| 22, 23 | Early warning coverage by country, 2023 and 2025 | WMO *Global Status of Multi-Hazard Early Warning Systems*. Same series for both years.         |
| 28     | Turtle telemetry in the Mozambique Channel       | Already in `obis-species-by-cell.csv`. Filter to *Dermochelys coriacea* and *Caretta caretta*. |
| 29     | Radiosonde station locations                     | WMO OSCAR/Surface, `oscar.wmo.int/surface`.                                                    |

Only 22 and 23 can't run at all. Cut them if time is short.

---

# Figures and sources

| figure                                               | source                                    |
| ---------------------------------------------------- | ----------------------------------------- |
| 3,375,214 Argo profiles, 20,530 floats               | Argo GDAC index, downloaded 2026-09-23    |
| 76,708 US stations; 2,166 African; 59% share         | GHCN-Daily, downloaded 2026-09-15         |
| median record 8 yr US, 68 yr Africa                  | GHCN-Daily inventory join                 |
| 19 Mozambique stations, 14 usable                    | GHCN-Daily                                |
| 2,108 / 5,936 / 10,033 Argo profiles per million km² | computed from the Argo index              |
| zero seal cells in the Mozambique Channel            | computed from MEOP                        |
| Michael 125 kt, 204 h, 74 deaths, $25.5 bn           | IBTrACS and NHC                           |
| Haiyan 125 kt, 204 h, 6,352 deaths, $2.98 bn         | IBTrACS and NDRRMC                        |
| Africa 27% of flood deaths, Europe 1.5%              | EM-DAT, computed                          |
| 15× more likely to die                               | WMO / SOFF                                |
| 636 radars vs 37                                     | Otto, *Yale Environment 360*, 31 Oct 2023 |
| 24 hours' warning cuts damage \~30%                  | Global Commission on Adaptation via WMO   |
| −50% African radiosondes 2015–2020                   | SOFF, un-soff.org/operations              |
| 9% surface, 13% upper-air in poorest countries       | WMO GBON Baseline 2023                    |
| mortality 6× lower with warning systems              | Guterres, 22 Oct 2025                     |
| $3.1 bn, 50c per person, 329 projects, 127 countries | UN / WMO EW4All                           |
| 74% of profiles south of 65°S from seals             | MEOP and Argo, computed                   |
| 29 sharks, 8,200 profiles, 40% error reduction       | McDonnell et al. 2026                     |
| 11 m people, 4.1 m buildings, 69% / 81%              | Wu, Zhang & Stouffs 2026                  |
| $2.7 trillion AI spend 2026, +49.5%                  | Gartner, September 2026                   |
| 55% of built area flooded at Xai-Xai                 | computed from the two satellite scenes    |
