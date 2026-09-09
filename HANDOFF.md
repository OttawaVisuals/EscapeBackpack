# Project Handoff

Last updated: 2026-09-09 by Codex

## Current Task and Status

Expanded the Rollo trip into a Rollo → William the Conqueror → Richard the Lionheart family-history route. Implemented and tested; user requested commit and push to origin/main. No website deployment is included.

The map now contains 72 researched person/place associations across four trips: Leif 7, family 26 (Rollo 11, William 7, Richard 8), Aud 13 and Harald 26. This is a working catalogue, not an exhaustive verified travel log. Evidence and approximate coordinate precision remain labelled.

The family trip supports mixing all three men's stops in any aunt-visit order. A person filter narrows the catalogue; selected visits and map pins remain available. Family labels identify each stop, and expandable context explains the intervening generations and Norman/Angevin legacy.

## Files Changed

- NorseBackpack/Travel_Map.html — family context, person filter and trip wording.
- NorseBackpack/TravelMap/stops.js — 15 William/Richard associations, sources and figure labels.
- NorseBackpack/TravelMap/map.js — family labels/filter, search and export compatibility.
- NorseBackpack/TravelMap/map.css — family information and label styling.
- NorseBackpack/TravelMap/README.md — catalogue counts, limitations and compatibility notes.
- HANDOFF.md — current handover.

## Decisions

- Preserve the rollo route key, all 57 original entries and IDs, and version-1 saved-plan format. Existing saved routes and imports remain usable.
- Other three trips remain intact. The aunt can mix and repeat stops freely; no historical sequence is imposed.
- No final route, dates, digit answer or lock length is set.
- Geographic previews retain north-up orientation and proportions.
- Richard's Limassol wedding-site association is explicitly uncertain. Regional and historic-site pins are approximate anchors.
- Reuse the existing static site; preview: http://127.0.0.1:8767/NorseBackpack/Travel_Map.html.
- Preserve unrelated local AGENTS.md and Aurora map/converter/asset changes outside this commit.

## Checks

- JavaScript syntax and git diff whitespace checks — pass.
- Catalogue — 72 unique entries; every original entry's existing fields preserved.
- Browser checks — legacy storage/import, mixed-family route additions and reordering, person filters, name search, popup attribution, reload persistence, JSON metadata/roundtrip, undo import, other-trip isolation and SVG family heading all pass.
- Desktop and 390px mobile screenshots visually inspected; no horizontal overflow. Mobile addition works.
- Browser errors — none in the tested workflow.
- Historical claims checked against Royal Household, English Heritage, Historic England, Normandy/Caen tourism, Cyprus tourism and Danube heritage sources linked in the catalogue.
- Test scripts, screenshots and exports live outside the repository in the session visualization directory. Tests used isolated browser storage.
- Final digit geometry, printed legibility and player solving remain untested until routes are selected.

## Prior Project Context

- Norse tone: playful mystery for adults with teens supported; no prior Norse knowledge required.
- Props must reset cleanly. Candidates include museum tickets, rune cryptex, hnefatafl pieces, maps and note facsimiles.
- Cryptex answer/release remain undecided; candidate backpack needs physical fit/hardware checks.
- Older brainstorm final-puzzle prose still describes the single-route prototype; update after route selection.
- Previous map checkpoint: d8baee9.

## Next Action and Open Questions

Select promising stops and aunt-visit orders, then export the plan for digit-legibility review before setting dates and lock length.

No implementation blocker. Three versus four final digits remains open. The earlier Leif attachment was not visible, and exact voyages/landfalls cannot always be established from surviving evidence.
