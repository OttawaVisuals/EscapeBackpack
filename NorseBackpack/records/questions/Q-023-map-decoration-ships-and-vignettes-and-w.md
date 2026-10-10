---
id: Q-023
title: Map decoration: ships and vignettes, and where they may go.
type: question
# open | answered | parked
status: open
# Records this question is about, e.g. [PZ-003]
about: [PP-029]
# Leave empty while open
answer:
# Any related record IDs, e.g. [PZ-002, Q-004]
links: []
# Set to an ID when this record is replaced. It then moves to the Parked tab.
superseded_by:
tags: [old-PR-11]
---

Status on the old page: **Built · test print**

The maps read as competent but restrained; the wanted feel is closer to an adventure map. Decoration is **Codex’s lane**; the base map stays with the build script.
**Art may not go just anywhere.** Two hard constraints: players draw the trail legs in wet-erase over the sheet, so anything printed under that line competes with the answer; and they locate stops by reading names, so anything over a label hides a clue. `NorseBackpack/TravelMap/build_art_placement_guide.py` computes the legal area and renders it — green is sea clear of the route corridor, every label box and the title furniture; red is the route plus a 26pt halo where nothing prints.
**Slots are cut landscape, not largest-area.** Maximising area gave tall narrow columns — one was 1.62 × 4.25 in — which is the worst possible frame for a ship under sail, the main subject. The guide now constrains aspect to roughly 1.4:1–2.0:1, which costs some area and buys usable art. Slot figures re-cut a second time after PP-029’s frame pan; the numbers above this line are superseded twice over — read the build script’s `LEIF_ART` comments for the current ones.
**Built.** Six of Codex’s first-pass assets went on the sheet: longship, whale, iceberg, polar bear, wolf, small settlement cluster. Two defects were fixed on the pixels themselves rather than by asking for a re-render — `fill_art_alpha_holes.py` fills every fully-enclosed transparent hole (a sail, a hull, an iceberg face) with a pale paper tone, so the reference grid can no longer print through a ship that was effectively made of glass; the whale and the settlement came back untouched, since both are genuinely open line art with no enclosed body, not filled silhouettes. The longship was also shrunk, from a first pass at 2.36 × 1.61 in down to 1.70 × 0.85 in — it was crowding the Labrador Sea.
**Land pieces placed by search, not by eye.** Each candidate spot was required to maximise clearance from the printed coastline, then to miss every reserved label box from a clean build — not a distance-from-named-place heuristic, which first missed a real collision between the wolf and the word “MARKLAND”. Final clearances: polar bear 5.8°, wolf 1.9°, settlement 4.1° from the nearest coastline, all three also clear of the drawn route by the usual 26pt halo.
**Land-only restriction relaxed** for the three small pieces (bear, wolf, settlement) — see above for where they actually landed. Their boxes are reserved before town-label placement, so a name moves rather than printing through the art, and none was placed on top of a real settlement's dot. No new settlement name or map point is invented.
**Style:** flat screen-print, no gradients, two or three inks from the existing palette (`#B56A2A`, `#59635D`, `#283B34`), and reduced opacity so the art recedes behind the map information. Nothing crosses a sea-slot boundary.
**Rollo sheet built.** Seven rust-only vignettes now decorate the second map: crossbow bolt, treaty scroll, ducal coronet, needle and thread, royal crown, longship and boar. Each visible mark is `#A2562D`. After the first proof showed the place-to-icon associations were too loose, every placement box was reduced from 58 pt to 38 pt and pulled into a tight ring beside its associated stop; visible artwork is now at most about 0.43 in wide. The three pieces around Saint-Clair-sur-Epte, Rouen and Roumare use different sides of that compact cluster so they remain distinct. Labels, town dots and the route stroke stay clear.
**Re-run the guide after any route change** — the corridor moves with the stops, and art placed against an old corridor can end up under the drawn line. Exact generating prompts are recorded in the Design guide tab.
