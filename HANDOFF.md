# Project Handoff

Last updated: 2026-09-09 by Codex

## Current Task

Build an interactive HTML map on the existing site to select and reorder the aunt’s visits among places associated with Leif Erikson, Rollo, Aud the Deep-Minded and Harald Hardrada.

## Status

Implemented and linked from the root homepage and Norse brainstorm. The map contains 57 researched person/place associations: Leif 7, Rollo 11, Aud 13 and Harald 26. Each stop explains its historical connection and distinguishes supported, saga, uncertain and contextual evidence. No surviving complete travel log exists; this is a broad working catalogue, not a claim of exhaustive verified stops.

Users can add places, repeat visits, reorder with arrows or position numbers, reverse or clear each trip, undo changes, fit a trip or all four people, search/filter stops and inspect four north-up route-shape previews. Plans save in this browser and can be exported/imported as JSON; shape previews export as SVG. The default coast map works offline, including direct file opening. Street detail is optional and online.

The existing repository is a local static site; README still says a live site is to be created. The user requested committing and pushing the completed Norse work to `origin/main`. This checkpoint includes the map, related Norse planning updates, site links and handoff; unrelated Aurora and AGENTS.md changes remain local. No website deployment is included. A preview server was started at http://127.0.0.1:8767/NorseBackpack/Travel_Map.html and the page was queued for opening in Codex.

## Files Changed This Session

- `NorseBackpack/Travel_Map.html` — new interactive workshop page.
- `NorseBackpack/TravelMap/stops.js` — catalogue and historical sources.
- `NorseBackpack/TravelMap/map.js` — map, ordered trips, persistence and exports.
- `NorseBackpack/TravelMap/map.css` — responsive Norse styling.
- `NorseBackpack/TravelMap/README.md` — maintenance, research limits and coordinate methodology.
- `NorseBackpack/TravelMap/vendor/` — local Leaflet 1.9.4, its license and Natural Earth public-domain land geometry.
- `index.html` — link to the map in the Norse design-guide card.
- `NorseBackpack/Norse_Brainstorm.html` — link to the route workshop above the header; previous planning edits preserved.
- `HANDOFF.md` — current session and next action.

## Decisions

- These routes belong to the fictional aunt. Selecting a place does not claim the historical person visited that precise coordinate.
- Stable stop IDs support portable plans. Repeated visits are allowed; each trip supports up to 100 visits.
- No final route, date sequence, digit answer or lock length is set. All routes start empty.
- Digit previews preserve geographic proportions and north-up orientation; the editor does not stretch geography into numbers.
- Historic claims and coordinate precision are separate. Regional pins are explicitly marked; uncertain origins are alternatives, not a historical sequence.
- Imported plans use the current trusted catalogue and reject unknown/wrong-person IDs. Corrected catalogue coordinates may change old plan shapes; this is documented.
- Reuse the existing static HTML site. No new hosted project or site architecture was introduced.

## Checks

- Read README, prior handoff, Git status/history and existing Norse final-puzzle text before editing.
- JavaScript syntax checks — pass.
- Catalogue integrity — pass: 57 unique IDs, valid person/source links and numeric coordinates.
- Browser workflow — pass: add, repeated visits, up/down and numbered reordering, reverse, undo, per-person isolation, reload persistence, search, evidence filter, map-popup add, overview, JSON export/import, invalid import preserving state, SVG export, clear/undo and direct file opening.
- Browser console/page errors after fixes — none in the main workflow.
- Desktop and 390px mobile layouts inspected; mobile has no horizontal overflow. Mobile route editing — pass.
- Homepage and brainstorm navigation links — pass; both affected layouts visually inspected.
- Optional OpenStreetMap detail — loaded and visually verified above the offline coast layer; switching back to offline mode — pass.
- Browser storage denied — editing remains usable and the export reminder is shown. SVG export rendered and visually inspected — pass.
- `git diff --check` — pass; existing Windows line-ending warnings remain.
- Sources checked against historical/heritage publications and saga texts. Icelandic anchors corrected using official heritage and geographic references; all coordinates remain described as approximate.
- Test scripts, exports and screenshots are outside the repository under the session visualization directory; they do not seed the user’s browser state.
- No final digit geometry, physical print legibility or player solve has been approved or tested.

## Prior Project Context Preserved

- Norse tone: playful mystery, mostly adults with teens supported; no prior Norse knowledge required.
- Props must reset cleanly. Candidate set: museum tickets, 3D-printed rune cryptex, hnefatafl board/pieces, maps and handwritten-note facsimiles.
- Rune cryptex answer and what it releases are undecided. The linked Koolehaoda L-Coffee backpack remains a candidate needing physical fit/hardware checks.
- Earlier final-puzzle prose in the brainstorm still describes the single-route prototype. The new four-person workshop explores the revised design; final puzzle instructions should be updated after route selection.
- Existing uncommitted Aurora map/converter/assets and AGENTS.md changes are unrelated and were preserved.

## Next Action

Use the workshop to select promising stops and visit orders, then export the plan for a digit-legibility review before fixing postcard dates and lock length.

## Blockers / Questions

- No implementation blocker. Three versus four final digits remains open.
- The Leif attachment mentioned in the earlier conversation was not visible; no claim was made to reproduce it.
- Exact historical voyages and some regional landfalls cannot be established from surviving evidence.
