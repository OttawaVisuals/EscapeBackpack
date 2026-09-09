# Norse route workshop

Open `../Travel_Map.html` directly or through the root site index. No build step is needed.

## Editable sources

- `stops.js`: 72 person/place associations — Leif 7, Rollo & descendants 26 (Rollo 11, William 7, Richard 8), Aud 13, Harald 26. Each has a named historical figure, evidence category, coordinate precision note, explanation and historical source.
- `map.js`: route selection, repeated visits, reordering, undo, storage, JSON import/export and SVG shape export.
- `map.css`: layout and existing Norse visual style.

IDs are stable references in saved plans. Preserve them when correcting descriptions or anchors. Imported plans accept only known stop IDs belonging to the specified person, with at most 100 visits per trip. Repeat visits are allowed. Import restores all four routes; Undo restores the previous plan during the current page session.

The family trip retains the internal `rollo` key and every original stop ID/coordinate. Existing version-1 saves and imports remain compatible. Its `figure` field distinguishes Rollo, William the Conqueror and Richard the Lionheart; users can mix all three in a single route. The family-member filter narrows the catalogue without hiding selected route points. Exported visits include the figure; old exports need no migration. The family note uses ellipses explicitly for intervening generations. This is Viking history and its later legacy, not a claim that William or Richard were Viking-Age explorers.

Plans use browser storage key `escape-backpack-norse-routes-v1`. Storage belongs to the browser/device/site address and is not shared. Exports contain route IDs plus readable visit information and source URLs. Imports use current catalogue coordinates, not exported coordinates; a future catalogue correction may therefore change an old plan's shape. No plan is preselected or seeded into the user's storage.

## Candidate 1972 plan

`Norse_Aunt_Route_Plan.json` is the current candidate final itinerary. In the workshop's left-to-right trip order, its north-up route previews are intended to read:

- Leif Erikson: **1** — Helluland → Markland → L’Anse aux Meadows.
- Rollo & descendants: **9** — Châlus → Rouen → Bayeux → Winchester → Battle → Roumare forest.
- Aud the Deep-Minded: **7** — Dögurðarnes → Hvammur → Esjuberg.
- Harald Hardrada: **2** — Oslo → Staraya Ladoga → Kyiv → Hedeby → Sicily → Anatolia.

The projected workshop previews were visually checked and read as **1972**. This sets a four-digit candidate code, not dates or a proven historical chronology. Recheck the shapes at the final printed map size; the family **9** has the most complex geometry.

## Research and geography

This is a working catalogue of identifiable life, journey and research associations, not an exhaustive historical itinerary. The surviving narratives contain disputed identifications and unnamed or unlocatable places. Do not turn regional anchors into precise historical landfalls or invent extra stops to fill gaps. The candidate route sets the intended four-digit code **1972**; historical chronology and aunt travel dates remain unassigned.

The main historical citations are embedded in `stops.js` and visible beside every stop. Aud's Icelandic localities required additional map checks:

- Hvammur: coordinates from [Visit West Iceland](https://www.west.is/en/experiences/culture-heritage/history-and-culture/hvammur), rounded to a settlement anchor.
- Krosshólaborg: coordinates and prayer-site tradition from [Visit West Iceland](https://www.west.is/is/stadir/krossholaborg).
- Dagverðarnes: modern locality at approximately 65.17, -22.52, checked against [Mapcarta / OpenStreetMap](https://mapcarta.com/de/19181316); not an exact saga landing.
- Kambsnes: modern Dalabyggð locality at approximately 65.081, -21.803, checked against [Mapcarta / GeoNames](https://mapcarta.com/19176764). Do not confuse it with the namesake in the Westfjords.

Other coordinates are approximate modern city, settlement, island or regional anchors. The deliberately broad England, Sweden, Denmark, Helluland, Markland and campaign-region pins do not assert precise historical positions. Before producing a local-scale physical puzzle, verify the chosen anchors at that scale.

The map and previews both use north-up Web Mercator. Each preview scales uniformly to its own bounds, preserving aspect ratio. Straight segments represent the aunt's puzzle connections, not navigable roads, sea routes or proven historical voyages. No digit recognition or solver claim is made.

## Bundled dependencies

- Leaflet 1.9.4: `vendor/leaflet.js`, `vendor/leaflet.css`; [official download](https://leafletjs.com/download.html). BSD license is retained in `vendor/LEAFLET-LICENSE.txt`.
- Natural Earth 1:50m land: `vendor/land.js`, downloaded from [natural-earth-vector](https://github.com/nvkelso/natural-earth-vector/blob/master/geojson/ne_50m_land.geojson), wrapped in a JavaScript assignment to support `file:` opening without fetch restrictions. [Public-domain terms](https://www.naturalearthdata.com/about/terms-of-use/). Preserve as generated map data.
- Optional online street layer: OpenStreetMap standard tiles with visible attribution. No tile caching or bulk downloading. Offline mode is the default and does not request street tiles.

Historical source checks and browser validation were performed on 2026-09-09. See the root `HANDOFF.md` for session checks and remaining design decisions.
