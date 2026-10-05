# Stories of Resilience (draft)

**In the final page (slide 18):** `story-plugin.js` and `story-plugin.css` bring the stories onto the shared
globe as a plugin (`scripts/build_all.py`, adapter `stories`; it reads `stories.json` directly). The card sits
under the slide's words: the 16:9 photo (white frame, link to the article in its corner) beside place and title,
Revised 5 Oct: the design system's story card (`.wm-card.is-tight`): photo, place and count, title, description
(three lines at most), the layer key, source and Next. Photos: `photos/web/<id>.webp` (git-ignored; made from
each story's `photo_url`, see docs/NOTES.md), shown in duotone with their credit. Test: `tests/stories.test.js`.


One scene. Title and subtitle on the left; on the right, the globe with one circle
per story. It opens on the first story, **Malawi's flood detectors** (a sensors-and-flooding
story; order set 5 Oct: Malawi, Bangladesh's volunteers, then the other flood early-warning stories, then the seals, sharks and
March et al., then the hope stories). **Next** at the card's bottom right steps through them
in the order of `stories.json`, and clicking a circle (or
← →) jumps to one. The card: a 16:9 photo placeholder with an arrow to the original
article in its bottom-right corner, then place, title, description, source and date. Esc or × closes it. Drag to turn the globe, scroll to zoom; it
drifts slowly until the first interaction.

```
python3 build_stories.py    # stories.json + template.html -> stories.html
```

Edit words in `stories.json`, never in `stories.html`. A story can carry one inline
`link` (`text`, `url`, `note`): that phrase in its description is underlined and links out
(the design system's `.wm-link`). The seal story links "elephant seals" to the MEOP-CTD
seal database. A story can also carry `zoom`
and `layers` (map layers that fade in while its card is open); the layer data is
packed from the main site's `site-src/layers/globe-data.json`, and `layerStyles`
sets each layer's colour and the label shown in the card's key.

## Where the stories came from

Two lists from the author, 4 Oct 2026:

- `list: "flood"`: 7 flood early-warning stories (spreadsheet
  *flood_sensing_stories_of_hope.xlsx*: headline, country, link).
- `list: "hope"`: 11 stories of hope (*Hope_txt.rtf*: headline, link).

Titles are the author's headlines. **Descriptions are written here from each
source article** (read on 4 Oct 2026), in our own words, at most 42 words, using
only figures stated in the article. Locations are the most specific place the
article names; coordinates are approximate (town, district or region centre).

| Story | Source, date | Place used | How it was read |
|---|---|---|---|
| Malawi flood detectors | UNICEF Malawi, 16 Jul 2024 | Karonga District | fetched |
| Bangladesh Cyclone Preparedness Programme (added 5 Oct) | American Red Cross, 29 May 2020 | Coastal Bangladesh | browser (403 to fetch); PMC article on the programme is behind a CAPTCHA |
| Nepal–India border | ICIMOD, 27 Feb 2023 | Ratu River | fetched |
| Cambodia | UNICEF Innovation, 6 Jul 2017 | Cambodia (country) | fetched |
| Nepal, resilience | UNICEF Nepal, 25 Feb 2020 | Saptari District | fetched |
| Kenya, Tana IoT | UNESCO, 14 Apr 2026 | Tana River Basin | fetched |
| Ghana, TAHMO | GSMA, 3 Dec 2025 | Aboabo | browser (403 to fetch) |
| India, community FEWS | UNFCCC; ICIMOD | Lakhimpur and Dhemaji, Assam | UNFCCC page is behind a CAPTCHA; details from ICIMOD via search |
| South Australia | Govt of South Australia, 2026 | state centre | browser (403 to fetch) |
| EU wind and solar | Ember, 22 Jan 2026 | EU centre | fetched |
| Right whales | NOAA Fisheries, 30 Apr 2026 | SE US calving grounds | fetched |
| Mangroves | Tulane University, 4 Jun 2026 | New Orleans (global study) | fetched |
| Dorset puffins | National Trust, 22 Jul 2026 | Dancing Ledge, Purbeck | fetched |
| Yangtze | Live Science, 12 Feb 2026 | Wuhan (middle Yangtze) | browser |
| Kenya fly farming | Global Center on Adaptation, 30 Mar 2025 | Mukuru, Nairobi | fetched |
| Guyana | CVF-V20, 28 May 2026 | Guyana | fetched |
| Panama | Adaptation Fund, 16 Jul 2026 | Santa María watershed | fetched |
| Central Asia | Climate Home News, 24 Mar 2026 | Central Asia (Kyrgyzstan) | fetched |
| Vanuatu | UNDP, 12 Jun 2025 | Espiritu Santo | fetched |

## Animal-borne sensing (3 stories with map layers)

Written from the main site's own scenes and data, re-checked on 4 Oct 2026:

| Story | Layers shown | Checks |
|---|---|---|
| Elephant seals, Southern Ocean | seals, Argo (faint) | South of 65°S: 151,967 seal profiles vs 48,821 Argo, **75.7%** seals (the main site says 74%). The seal download is only 61% of MEOP's profiles (`docs/SOURCES.md`), so the true share is likely higher; the card says "about three-quarters". |
| Sharks, NW Atlantic | sharks, Argo (faint) | McDonnell et al. 2026, *npj Clim Atmos Sci* 9:147: 29 sharks, >8,200 profiles, up to 40% lower surface temperature error in a proof-of-concept. **The shark layer is OBIS sightings in the study box, not the tagged sharks' tracks**; the key says so. |
| Tagged animals could fill Argo's gaps | Argo coldspots, tracked species | March, Boehme, Tintoré, Vélez-Belchi & Godley 2020, *Global Change Biology* 26(2):586–596, doi 10.1111/gcb.14902 (read in full on PMC): >1.5 million Argo profiles; coldspots 69.76 million km², 18.6% of the ocean; 183 species in 8 groups, tracking from >3,000 animals. **The coldspot layer is this project's own calculation** (26 patches, 48.1 million km²), not the paper's map; the key says so. The dot sits in the Caribbean, one of the gaps the paper names. |

The Mozambique turtle story was the project's own proposal, not a published finding,
and was replaced by March et al. 2020, which makes the argument in print.

## Open items for the author

1. **Fit with the title.** The title is about those *least responsible* coping, and
   the brief about responding to *missing data*. The 7 flood stories fit both. Several
   "hope" stories do not: South Australia, the EU, US right whales, Dorset puffins and
   the Tulane mangrove study are in wealthy, high-emitting places and are about
   recovery, not data. All 18 are in; the `list` field lets you filter.
2. **Yangtze headline** says "four-year fishing ban". The source describes a
   **10-year** ban from 2021; the study used data from 2018 to 2023. Consider
   "…after China's fishing ban".
3. **"Puffing" → "puffling"** fixed in the Dorset headline (a young puffin).
4. **Central Asia** article also covers Pakistan (the larger programme, ~435,000
   people); the description says so.
5. **Ghana**: the source says only "Aboabo, an urban suburb"; the dot is placed at
   Kumasi, where Aboabo is, which is our inference.
6. **Photos**: placeholders only. `photo_ref` and `photo_credit` record each
   article's own image where one was found; licences are not cleared.
7. **Subtitle** ends "are …", as given.
8. The three animal stories are about wealthy-country science programmes.
9. Two pairs of stories sit close together at full-globe size (Ratu River and
   Saptari, ~1° apart; the two Kenya stories). Scroll to zoom, or use ← →.
