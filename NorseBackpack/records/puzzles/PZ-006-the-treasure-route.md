---
id: PZ-006
title: The treasure route
type: puzzle
# idea | candidate | decided | built | parked
status: decided
# The structure beat this puzzle belongs to (one ID)
beat: ST-004
# Props the player needs, e.g. [PP-001]
props: [PP-013, PP-030, PP-031]
# Puzzles that must be solved first, e.g. [PZ-002]
needs: [PZ-004]
# cipher | physical | search | logic | wordplay | other
mechanic: search
# 1 (easy) to 3 (hard)
difficulty: 2
# Lock it opens: 3-digit | 4-digit | 4-letter | 3-digit-colour (blank if none)
lock: 3-digit
answer: 521
# Compartment this lock closes (shown on the Locks tab)
container: Front right pocket
reset_display: 000
# What players call this lock on the hint page, e.g. "The luggage tag" (spoiler-free)
hint_title: Lock 5
# Explicit opt-in for the PUBLIC hint page. Candidates are never published.
publish_hints: yes
# Independent of design/build status: untested | passed | changes-needed
test_status: untested
# physical | digital (a digital walkthrough does not verify a physical prop)
test_method:
# Optional stable Clue Library technique link
technique:
# Any related record IDs, e.g. [PZ-002, Q-004]
links: []
# Set to an ID when this record is replaced. It then moves to the Parked tab.
superseded_by:
tags: [old-PZ-17]
---

## How it works

One portrait map, symbols not to scale, carrying line/area/point symbols instead of isolated icons — the split-panel design below was shelved 17 Sept 2026 in favour of this. Players walk the drawn path network and count what the route crosses.

Lock 6 of 13 in the release order decided 7 Oct 2026 (Q-005). Difficulty 2 of 3 is Claude's estimate from the mechanism (number of props and steps), not playtest data.

**9 Oct 2026 (designer, Q-001):** now lock 5 of 13. Compartment: front right pocket.

## Player notices

Postcard A2 (Hvammur), Aud’s laminated journey map, and the Aud’s Treasure Museum ticket (six rows, one per leg, three tally columns: bridges, fords, gates).

## Player does

Walk the six legs on the real drawn network, from the northern chapel to the cave beyond the ruin at I9. At the merged leg 5, follow the road to the correct “village at a crossing” (H9, not the lookalike near H3/G3) — A2’s message gives the direction (south) and the forest detail needed to tell them apart. Tally bridges, fords and gates crossed across all six legs.

## Player obtains

Code **521**. Opening this lock releases PP-005, PP-010, PP-011.

## Story reason

Turns Aud’s own map from a final-route prop into a working treasure map without printing a second sheet, and makes the tally self-checking — a blue line or a gate is unmistakable, so counting is hard to get subtly wrong.

## Clue wording

A2’s message (rewritten 19 Sept 2026) plants both checks needed for the leg-5 ambiguity without naming either outright: the direction, and “the road that followed the forest.”

## Hints

1. The Island Settlement map and the Treasure Museum ticket go together: the ticket gives directions, and the Hvammur postcard says what to count on the way.
2. Start at the northernmost chapel on the map and follow the ticket’s six steps along the roads.
3. Keep three separate tallies as you go: bridges, fords and gates. On the fifth step, the postcard tells you which way to go and which road to follow.

## Solution

Six legs: chapel → chapel (1 bridge), → well (2 fords, 1 bridge), → landing (1 bridge), → standing stone (1 bridge), → village at the crossing, south along the forest road (1 gate, 1 bridge), → the cave beyond the ruin (nothing). Totals: 5 bridges, 2 fords, 1 gate: **521**.

## Solution notes

Design-side solution text, kept when the player-facing Solution above was written for the hint page (9 Oct 2026).

Six legs: chapel→chapel (1 bridge), →well (2 fords, 1 bridge), →landing (1 bridge), →standing stone (1 bridge), →village at the crossing H9 (1 gate, 1 bridge), →ruin/cave (nothing). Totals: **5 bridges, 2 fords, 1 gate → code 521**. Corrected 19 Sept 2026 from an earlier miscount (`531`) after the user spotted a leg with no ford on the printed sheet.

## Open risks

**None — verified 26 Sept 2026.** The user printed a test sheet and hand-walked all six legs by hand against the ticket; 521 is confirmed. `Props/AudTicket/build_aud_ticket_pdf.py` prints the correct `ANSWER 5 2 1`. **Superseded design, kept for reference:** the earlier Dalir split-panel sheet and its plot-number-sum mechanism (code `467`) — see `NorseBackpack/Drafts/2026-09-17_Aud_split_panel/README.md`.

## Releases (as worded on the old page)

**Superseded 9 Oct 2026** by the compartment map in Q-001; the current release list is under Player obtains.

**Since 7 Oct 2026 (Q-005):** lock 6; releases postcard R2, Rollo’s map and the Rouen museum ticket. ~~The mixed coin hoard in the cave at I9, plus postcards A1 (Dögurðarnes) and A3 (Esjuberg)~~ — these now come from lock 9 (counting).

Lock as recorded: Three-digit padlock (lock 6; on the coin cache until 7 Oct 2026). Old page status: Decided · 521 verified by hand-walk, 26 Sept 2026.

## Design notes (PZ-006: Verified · 521 confirmed by hand-walk, 26 Sept 2026)

**Aud’s treasure-map, coin-hoard and comb chain — now gates entry to Harald’s leg.**

**Ticket back simplified, 29 Sept 2026 (user).** The player copy of Aud’s Treasure Museum ticket no longer shows “COUNT WHAT YOU CROSS”, the bridge/ford/gate tally boxes, the worked leg 1 or the BRG/FRD/GTE legend — just the six directions. Card A2 now carries the counting: “It was fun to count how many bridges, fords and gates I crossed.” The answer copy (page 3) keeps the boxes and the 5 2 1 total. Built in `Props/AudTicket/build_aud_ticket_pdf.py`.

**Approved update, 22 September 2026:** coin values total 3705 and rotate to SOLE; HRAFN selects four flight digits, 2648, for a lock directly on the board pouch. The scale and cryptex are superseded. [Full specifications, visual and postcard changes]. Older options below retain their historical status.

**Replacement started, 17 Sept 2026 — one map, symbols not to scale, edited in the browser.** Aud’s treasure hunt moves onto the **existing single portrait map**, zoomed in, rather than a second panel or an invented landscape. The user’s constraint, in their words: *“I would prefer using one map and have my geo markers not to scale than having to create a new map.”*

**The scale conflict, and how it is resolved.** Aud’s three route stops span 34 km east–west and 110 km north–south — that spread *is* the digit **7** the answer key traces. Holding all four stops needs a frame about 143 km tall, which puts **1 pt at roughly 211 m**; a real 500 m hedge would be 2.4 pt long, a dash rather than a sinuous line. Rather than fake the geography, **symbols are simply drawn at whatever size reads well and are not to scale**. A hedge on this sheet is tens of kilometres long in real terms. That is accepted: the sheet is a puzzle prop, not a survey, and it keeps the real coastline, the real stop positions and the existing 7 intact.

**No elevation data exists in the repository** — only Natural Earth coastlines. Contour lines are therefore hand-drawn in the designer, not derived, and “every 50 m” is a labelling convention we choose rather than a measurement.

**The lock mechanic is reopened from scratch.** The plot-number sum is not carried forward; how the route yields a code is undecided again, alongside the map itself.

**Built this session:**

- `TravelMap/export_aud_base.py` — runs the real build at the zoomed frame and writes `aud_base.js`: coastline, stops, towns and area labels already converted to **PDF page points**. The projection is never reimplemented in JavaScript, so the designer and the printed sheet cannot drift apart.
- `TravelMap/Aud_Map_Designer.html` — the editor. Draws the map 1:1 with the PDF and places symbols on it. **Line symbols** (hedge, stone wall, paved road, track, footpath, river, stream, ditch, contour), **area symbols** (wood, marsh, lake, field, moor) and **point symbols** (farm, church, ruin, mill, cairn, stone, bridge, well, marker, label). Click to place or draw, drag vertices, optional curve smoothing for sinuous lines, per-feature width and label, grid-reference readout, display zoom, undo, browser autosave, and JSON export/import. Hedges, walls and ditches carry their own ornament along the line — blobs and ticks — which is exactly what an isolated icon could not do.

**Zoomed frame, panned 17 Sept 2026:** lon −22.9751..−20.5451, lat 64.08..65.37 — about 1.8× closer than the shipped sheet, and panned **east** so the content sits further left and far more land comes into play. Two constraints pin the pan and they nearly conflict: **stop 1 (Dögurðarnes) sits in grid column B** (x 140.2, column B spans 94.1..154.7), and **Bjarnarhöfn — decoy card AD’s own site — stays on the sheet**, 9 pt inside the west edge at A4. At exact column-B centre Bjarnarhöfn fell 7 pt off the page. Stops now read B2, E2 and E10. The build asserts every *visited* stop projects inside the map area, so panning further fails loudly; Bjarnarhöfn is a decoy card rather than a visit, so it is not covered by that assert and is checked by hand in the exporter. **Designer placements are stored as page points, not coordinates — re-panning the frame moves the coastline under them and they do not follow, so the frame should be settled before anything is drawn.Still open:** the decorative labels `ÍSLAND`, `DENMARK STRAIT`, `FAXAFLÓI` and now `Snæfellsnes` fall outside this frame and need repositioning before the zoomed sheet is printed; the designer’s export is not yet read by `build_trail_maps_pdf.py`; and the whole puzzle mechanic is undecided.

**First symbol layer, 17 Sept 2026 — 59 features, `TravelMap/aud_features.json`. Superseded the same day: being redrawn from scratch against the build brief below.** The first pass was drawn for looks rather than for a puzzle, and measuring it is what produced the brief. It is kept as the file of record until the rebuild lands, and it is not wrong — it reads as a surveyed valley rather than a scatter of icons, which was the point of replacing the shelved detail panel. What it lacked was structure a route can be written against: **not one of its 29 landmarks sat inside a wood, field, moor or marsh**, so with 6 ruins and 6 standing stones on the sheet no clue could point at one without naming it; it carried only 4 route crossings; and no route passed *through* an area, only around. Its path network was fine — 12 of 13 routes in one connected component, 11 junctions — which is why the brief below asks for almost no extra paths.

##### Build brief — what the sheet has to carry

Targets, not a wish list. These are what a traced-route puzzle needs in order to be writable at all; the numbers assume a seven-leg route. Counts are per sheet.

**A · The countable events.** Whatever the final mechanic, the code is built from things the route demonstrably crosses. These have to exist before any leg can be written.

| Want | Target | Why |
|---|---|---|
| Route crossing water (ford or bridge) | 5+ | The most legible crossing on any map — a blue line is unmistakable, so the tally is self-checking. |
| Route crossing a barrier (hedge, wall, ditch) | 3+ | A second, visually different class of event, so two tallies can be kept apart. |
| Each crossing in its own grid cell | all of them | Two crossings in one cell cannot be counted separately. A long line drawn across the grain of the tracks earns several at once — that is the cheap way to get them. |
| Fords *and* bridges, both present | both | Two ways to cross water means a leg can specify which, and a ford is the more Icelandic answer. |

**B · The navigable skeleton.** How a leg is described without using a single place name — which is what lets every feature stay unlabelled.

| Want | Target | Why |
|---|---|---|
| Landmark sitting *on* a route (within ~8 pt) | ~20 | *“Follow the path to the mill.”* A landmark the path does not reach cannot be a step. |
| Forks where three or more ways meet | 6+ | A bend is not a decision. Only a fork is. |
| Landmark *at* a fork | 3+ | Lets a fork be named — *“bear left at the cairn”* — instead of counted. |
| Route passing *through* an area | 3+ | *“Across the moor,” “through the wood.”* Skirting an area does not give a leg anything to say. |
| Route running alongside a wall, hedge or river | 2 | Describes a leg with no landmark at all — useful where the ground is otherwise empty. |
| Dead ends | 6+ | Somewhere for the treasure, and somewhere for a wrong turn to stop rather than wander. |

**C · The ambiguity engine.** The reason a wrong turn produces a wrong *code* rather than a stuck player, and where card A2’s in-person clue earns its place.

| Want | Target | Why |
|---|---|---|
| Landmark sitting inside an area | 8+ | **The single most important item on this page.** It is what lets a clue say *“the chapel in the wood”* with no name attached. A landmark in open ground can only be pointed at by naming it. |
| Confusable pairs with different context | 3+ pairs | Two of the same symbol, one in a wood and one on the shore. Repeated symbols are an asset, not clutter — but only once they can be told apart. |
| At least one pair split by water vs woodland | 1 | Card A2 already says the chapel is inland among birches, not the one by the water. That clue needs both churches to exist and to be distinguishable on the sheet. |
| Both branches of the ambiguous hop stay walkable | 1 hop | The wrong choice has to lead somewhere and produce a different tally. A dead stop teaches nothing. |
| Deliberately stranded landmarks | 5–7 | Scenery that is off the network entirely, so not every symbol on the sheet is in play. Real maps have these. |

**D · Composition and production rules.** Constraints the rebuild must not break. The first three are measured, not matters of taste.

- **Everything on land.** Checked by sampling every line every 2 pt and every area on a 30×30 grid against the coastline polygon. A vertex-only test is not enough — a road with both ends ashore can still span a fjord between two vertices — and it also gives false alarms, since Dögurðarnes and Bjarnarhöfn themselves fall a fraction outside the polygon at Natural Earth resolution.
- **19 pt minimum clearance** from every stop pin and town dot. Hvammur and Krosshólaborg sit only 8.5 pt apart, so nothing can thread between them — routes stop short of that cluster.
- **Nothing outside the map area** (x 33.6–578.4, y 78.24–758.4). A vertex past the edge bleeds into the grid band.
- **No two point symbols closer than 16 pt**, or the icons collide at print size.
- **Keep column E, rows 2–10 visually quiet.** That corridor is where the player draws the digit **7** in wet-erase for the final puzzle — the route from B2 across to E2 and then down to E10. New ink there competes with the endgame.
- **Do not add paths for the sake of it.** The first pass already had enough junctions; what it lacked were crossings and context. One new watercourse drawn across the grain buys more than six new footpaths, and a dense lane network reads as English enclosure country rather than settlement-era Dalir.
- **Page points, y up, 612×792**, and the export’s `frame` must match `export_aud_base.py`’s `ZOOM_FRAME`. Placements are stored as page points, not coordinates, so re-panning the frame slides the coastline out from under them.
- **Z-order when the export is wired into the build:** designer features draw *beneath* the stop pins, town dots and their labels. The clearances keep the sheet readable, but the base map’s own labels must win any remaining overlap, the same way they do on a real map.

**The brief is live in the designer, 17 Sept 2026.** `TravelMap/Aud_Map_Designer.html` now carries a **Build brief** panel that counts every target above against whatever is currently drawn, grouped in the same four sections and scored out of 18. It updates as you draw (debounced, since crossing detection is O(n²) on segments) and turns each row green when its target is met, so the brief is checkable at the moment of drawing rather than after an export. Targets where drawing *more* is harmless are written as minimums — `5+`, `3+` — and only the hard-zero rules and the stranded-scenery count are true ranges. The land test carries 2.5 pt of slack, because a wall or track that runs down to the shore legitimately touches the coastline.

**Base-map label collisions fixed in the designer at the same time.** Dögurðarnes and Hvammur are each *both* a stop and a town in the corpus, so the designer was drawing two labels on one point; Krosshólaborg then landed on top of Hvammur’s. The print build already solves this — a town that is also a stop is labelled once, by the stop, and a reserve/place pass moves or drops the rest — so the designer now mirrors that logic instead of drawing both lists naively. Stop labels are planned first so the more important label wins the good position, and any label that cannot be placed is named in the panel rather than silently lost. With the current layer, none are dropped.

**Five symbols added and crossings automated, 17 Sept 2026.** Drawing the first stretch of the rebuilt map turned up two gaps in the tool.

- **`port`** (anchor), **`village`** (three gables, so it reads apart from the single-house `farm`) and **`cave`** (a solid arch in a hillside) — all three requested while drawing. A cave is also the obvious home for the treasure terminus when the route is finally written.
- **`ford`** (stones between two bank ticks) and **`gate`** (two posts, two bars) — added because a crossing needs a symbol that says *which kind* of crossing it is. You bridge a river, wade a stream, and go through a gate in a hedge or a wall.

**“Place crossings” button.** Draw the route straight over the obstacle and the designer puts the right symbol exactly on the intersection: `river → bridge`, `stream → ford`, `ditch → bridge`, `hedge/wall → gate`. It skips any crossing that already has a symbol within 10 pt, so it is safe to re-run, and it is undoable. **This exists because placing them by hand does not work:** the first stretch of the rebuild had a bridge sitting in a 12.5 pt gap between two paths that each stopped short of the ditch — it looked like a crossing, but nothing crossed anything, so it scored zero and left the network broken. A new scorecard row, **Crossings with no symbol** (target 0), catches the reverse case.

**Crossing markers no longer count as landmarks.** `bridge`, `ford` and `gate` are excluded from “landmarks on a route”, “inside an area”, “stranded” and the confusable-pair test. A bridge is trivially on a route, so counting it flattered the score — the first layer’s 5 landmarks-on-a-route were really 2 plus three bridges.

**Clearance from settlements: the rule is about labels, not roads.** A road that serves a village is correct cartography, and the 19 pt rule exists only because the base map’s stop pins and town labels are drawn on top and the build’s label placer cannot see designer geometry. Until the export feeds `build_trail_maps_pdf.py`, keep routes 19 pt clear and let them *end at the outskirts*, which reads as serving the settlement. Once the export is wired in, the placer should reserve designer features too and the rule can relax — except at Hvammur and Krosshólaborg, which sit 8.5 pt apart and can never be threaded.

**Stop 1 was plotted in the sea, and is now ashore — 18 Sept 2026.** The user spotted it on the sheet. Measured, Dögurðarnes sat **12.1 pt from the coastline, about 2.6 km** — roughly 4 mm off the shore at print size, far too much to be a rounding artifact. An earlier note in this session blamed “Natural Earth resolution” for both this and Bjarnarhöfn; that was right for Bjarnarhöfn (0.7 km) and wrong for this stop.

**The cause is the vendored coastline, not the coordinate.** `TravelMap/vendor/land.js` is Natural Earth **50m** — 1:50 million, generalised to a few kilometres. That is fine on the other three sheets; Aud’s is zoomed to about 211 m per point, where it is not. Dögurðarnes is a headland in Breiðafjörður, and at 1:50m the peninsula it sits on simply does not exist. `stops.js` already flags the coordinate `uncertain`, noting it “represents the peninsula, not an exact landing”.

**Decided: nudge the plotted position; keep the real coordinate.** Re-vendoring `ne_10m_land` for one dot was the alternative and was declined. A new `PLOT_NUDGE` table in `build_trail_maps_pdf.py` shifts only the drawing, and `stops.js` is untouched. Because the stop has to move 2.6 km to reach *any* land, the shift is necessarily large: **3.5 km north-east, landing 900 m inshore**, about 16 pt on the zoomed sheet.

**Effect on the digit 7, measured before committing to it:** the top bar goes from 150.8 pt to 138.9 pt (8% shorter) and flattens from **+9.3° to +4.9°**. That is an improvement — a flatter top stroke reads more like a 7 — and the descender is untouched. **The grid references do not change: stops still read B2, E2 and E10.A check was added so this cannot happen quietly again.** The build already asserted that every stop projects inside the map *area*, which a stop floating in the water passes happily — that is why this survived. Stops are now tested against the coastline and reported **in points as well as kilometres**, because 8 km is two points on Leif’s 500 km sheet and invisible, but twelve on Aud’s and glaring. It immediately found two more: **Battle Harbour** (8.2 km, **2.0 pt**) and **Patara** (1.8 km, **0.4 pt**). Both are far too small to see at those sheets’ scales and were left alone.

**One more trap closed:** `export_aud_base.py` reads the plan directly rather than through the build, so the printed sheet was fixed while the designer went on drawing the stop at sea. Both now share `plot_nudge()`. All four sheets were rebuilt in passing — which finally replaces the Aud PDFs that had been stuck as the rejected landscape two-panel version since the file was locked by an open viewer.

**The designer works on a phone, 17 Sept 2026, and is published at [claude.ai/artifact/26d6YkdDjuSkN2WS5Uc2fL](https://claude.ai/artifact/26d6YkdDjuSkN2WS5Uc2fL)** (private to the account). It was mouse-only: touch could tap but not drag, and the sheet rendered 734 px wide on a 375 px screen.

- **Pointer events** in place of mouse events, so one set of handlers serves mouse, pen and touch. The map carries `touch-action:none` so a drag belongs to the app rather than becoming a page scroll, and a **Pan** toggle hands the gesture back when the map itself needs moving.
- **Vertex handles gain an invisible 9 pt hit disc.** The visible 2.2 pt dot is a fine mouse target and a hopeless finger one, and enlarging it would clutter the sheet.
- **An action bar** carries what the keyboard does on desktop — Finish line, Undo, Delete, Fit, Pan. It sits in the Tool card on a big screen and pins to the bottom of the viewport on a phone, where the palette is a long scroll away from the map.
- **Fit-to-width zoom**, applied automatically below 780 px. The zoom floor dropped from 60% to 30%, because 612 pt cannot fit a phone at 60%.

**Two bugs surfaced while testing, both older than this change.** Every `font: 11px/1 inherit` shorthand in the stylesheet was **invalid** — `inherit` is a CSS-wide keyword, legal only as a whole value and never as one component of a shorthand — so Chrome dropped all nine declarations and fell back to its own defaults: the header rendered at 26 px instead of 14 px, buttons at 13.3 px instead of 11. It looked plausible on a desktop, which is why it survived. Separately, the new mobile media query was written next to the layout rules it belonged with, but **a media query carries no extra specificity**, so the component rules further down won every tie and almost none of it applied. It now sits last in the sheet.

**Pinch-zoom fix, same day.** The first mobile pass let Pan mode set `touch-action:auto`, which allowed the browser to zoom the whole page. Page zoom shrinks the visual viewport *inside* the layout viewport, and `position:fixed` is pinned to the layout viewport — so the action bar and every control on it slid off screen. The lesson is general: **a bottom-pinned bar and browser page zoom cannot coexist**.

- Pan mode now uses `touch-action:pan-x pan-y` — scrolling still works, browser zoom cannot happen at all.
- **Pinch drives the designer’s own zoom control instead**, so the sheet scales while the interface stays where it is. Two-finger drag pans in the same gesture, so a zoomed-in map no longer needs a trip to Pan mode.
- On a phone the map pane is now the scroll container rather than overflowing the document, so a pan scrolls a known element. It shrinks to fit the sheet and only scrolls once past 58dvh.
- **Touch taps commit on release, not on touch-down.** The first finger of a pinch was landing a symbol before the second finger arrived. A mouse has no such ambiguity and still acts immediately.

**Note on the published copy:** it is a snapshot and keeps its own browser storage, entirely separate from the local file. Work drawn in one does not appear in the other — move it across with **Copy JSON** and **Load JSON**, and republish after any change to the local designer.

##### The treasure hunt — decided 18 Sept 2026

**The mechanic is A1: count what the route crosses.** Four options were put up (A count the crossings, B grid columns as digits, C a legend cipher, D scale-bar measurement) and A was chosen. The reading is the refined form: the three digits are **bridges, fords and gates** — three visually distinct symbols the player counts on the sheet, rather than abstract categories. You do not have to know that a ditch is a barrier or that blue means water; you count pictures. Keyspace is a real ~1000, against the 35 of the leg-number variant (A2), which a patient player could brute-force in ten minutes.

**The route was found by walking the drawn network, not invented.** The layer was turned into a graph — nodes are junctions, dead ends and landmarks that sit on a track; edges are the stretches between them, carrying whatever they cross — and every seven-leg walk ending at a cave was enumerated. Two survive from the chapel; this is the stronger.

| Leg | From → to | Crosses |
|---|---|---|
| 1 | the northern **chapel** (C2) → the second **chapel** (E3), road 218 pt | 1 bridge |
| 2 | → the **well** (B5), road 328 pt | 2 fords, 1 bridge |
| 3 | → the **landing** (C6), road 88 pt | 1 bridge |
| 4 | → the **standing stone** (H5), road 408 pt | 1 bridge |
| 5 | → **the village at the crossing** (H9) — merged with the old leg 6, 19 Sept 2026; the standing stone at H7 is passed but no longer named, road 122+123 pt | 1 gate, 1 bridge |
| 6 | → the **ruin** (I9), road 106 pt; the cave lies 23 pt on, inside the wood | nothing |

**The code is `521`** — 5 bridges, 2 fords, 1 gate. Verified by the user on the printed map, 25 Sept 2026, with the reworded ticket legs (start at the northernmost chapel, C2). The treasure is the **cave in the wood beyond the ruin** at I9, which is why `cave` was added to the symbol set.

**Code corrected 19 Sept 2026, from `531` to `521`.** The user found leg 4 (landing → standing stone) has only 1 bridge, no ford, checking the printed sheet by eye. Re-walked against `aud_features.json` and the rendered PDF confirmed it: leg 4 is bridge-only, and leg 3 (well → landing) is also bridge-only — the ford this table used to credit to leg 4 is not on either leg’s road. Total across all six legs (seven at the time of this note; legs 5/6 were later merged) is **5 bridges, 2 fords, 1 gate**, not 3 fords. The extra ford in the old count most likely came from a stray ford symbol near the landing that sits on an unused branch, not from either leg’s actual road — not confirmed, just the likeliest explanation. ~~Not yet fixed: the wrong-branch score at leg 5 was never rechecked against this correction, and `Props/AudTicket/build_aud_ticket_pdf.py` still prints the old `ANSWER 5 3 1` — the built ticket PDFs are now wrong and need a rebuild once the wrong-branch figure is settled.~~ **Fixed:** `build_aud_ticket_pdf.py` already carries `ANSWER = (5, 2, 1)`, with an assert tying it to the per-leg tally — checked 26 Sept 2026, the built ticket PDFs are already correct, this note was just stale.

**The road was extended to reach the chapel.** Its head sat 31 pt short, which left the northernmost church unreachable as a route step and forced a weaker route scoring `301` — a zero digit, and two legs that stumbled through junctions in the same grid square. Extending the road rather than adding a connector keeps the feature count down and turns the chapel into a fork where the road meets the footpath already starting there. The new head is at **(172.25, 672.35)**: 12 pt from the chapel and 26.3 pt from the Dögurðarnes pin. Drawn straight at the chapel it would have passed 13.9 pt from that pin, inside the 19 pt rule, so it approaches from the south-east instead.

**Leg-5 mechanic replaced, 19 Sept 2026 — the H5 fork is no longer the puzzle.** Everything below describing the standing stone at H5 as a four-way junction, with A2 resolving which branch to take (open ground vs. the trees, wrong branch scoring `432`), is superseded. It is kept as the record of the first version of the mechanic.

**The deliberate ambiguity is now leg 5, moved and rebuilt.** Legs 5 and 6 were merged into one ticket row: from the standing stone at H5, the direction is *“Follow the road to the village at the crossing”*, crossing the H5 gate and the H7–H9 bridge together (`1 gate, 1 bridge`). The standing stone at H7 is still physically on the road but is no longer named as a stop. **The village at the crossing is H9** — the cairn/church/village cluster at the real crossroads. A second village-at-a-crossing symbol sits near H3/G3, well back up the road toward the start of the route, and reads the same on the sheet. A player who loses track of position could walk to the wrong one. Card **A2** resolves it: the correct village lies **south** of H5, and the road running there passes alongside the wood at H5/H6/I5/I6 — the decoy near H3/G3 sits inside a different wood, back near the start. Both the direction and the forest detail have to agree for a player to be sure.

**Card A2’s chapel line is superseded.** Its drafted message pointed at a chapel “inland among birches, not the one by the water”. The wood chapel is at E4 and sits 14.5 pt off the network, so it can never be a route step. **A2 has front art only — no back, no print PDF — so nothing is printed and the line was free to change,** and it has changed twice since: first to resolve the H5 fork, now to resolve the village-at-the-crossing choice below.

**The ticket carries the legs, not the crossings.** Aud’s Treasure Museum ticket does not exist yet — the built `Museum_Ticket` is L’Anse’s — so its form is free. It gives **directions only**; if it listed the crossings there would be nothing to solve. **Six rows, one per leg** (seven until the leg 5/6 merge), with three tally columns — bridges, fords, gates — and row 1 pre-filled as the worked example (*leg 1: 1 bridge*). The old seven-row plot-number form is superseded, though the row count survived by coincidence even before this merge.

**A2’s full message, rewritten 19 Sept 2026:** *“Hvammur today.
Such a lovely place and a great museum dedicated to Aud.
They even had a treasure hunt to find artifacts from Aud’s time.
I was able to solve it and had a lovely time discovering the countryside. I particularly enjoyed the road that followed the forest.
I might just have to remember how many ~~rivers~~ bridges, fords and gates I crossed. (“rivers” changed to “bridges”, 25 Sept 2026, to match the ticket’s columns)
With love,
Aunt Liv”* Two checks are load-bearing here, not one: the **direction** (south, away from the start) and **the forest along the road** (the wood at H5/H6/I5/I6). Neither is named outright — the letter only says she enjoyed the road, and a player has to match that against the sheet.

**The ticket is built, 18 Sept 2026 — `Props/AudTicket/build_aud_ticket_pdf.py`.Resized 25 Sept 2026:** now 3×4 in (see the hoard prop). Same 2×5.5 in stock, palette, header band and outer rule as the museum ticket (L’Anse at the time; Brattahlíð since 28 Sept 2026), so the two read as tickets from the same world. Unlike L’Anse’s it has **no ImageGen art** — both faces are vector, so there is nothing to re-render if the wording changes. [Open PDF](../Web/pdf/Aud_Ticket_Print.pdf) · [Letter sheet](../Web/pdf/Aud_Ticket_Letter_Print.pdf)

![Aud Treasure Museum ticket, front](Props/_Renders/Aud_Ticket_Front.png)Front

![Aud Treasure Museum ticket, back, with tally boxes per leg](Props/_Renders/Aud_Ticket_Back.png)Back

**Front:** *AUÐAR SAFN · Treasure Museum · Hvammur, Dalir*, admit-one, “admission incl. treasure hunt”, and a rust roundel standing in for a crest the museum does not have an asset for yet. **Back:** the legs, one per row, with three tally boxes each and the totals left blank — six rows since the 19 Sept 2026 leg 5/6 merge, seven before it. Row 1 is pre-filled in purple as the worked example; the footer spells out `BRG`/`FRD`/`GTE`. **Page 3 of the single-card PDF is an answer copy** — every box filled and `ANSWER 5 3 1` at the foot — for checking, not for the bag.

**Two things the build guards.** The leg text is measured and wrapped before drawing, so a longer direction raises rather than silently overflowing the card. And an `assert` ties the per-leg answers to the printed total, so the two cannot drift apart.

**Caught in the first render:** the stub number read `No. 531-A` — the answer, printed on the front of the ticket. ~~Now `No. 209418`, deliberately unrelated.~~ **Removed entirely, 27 Sept 2026:** stub numbers taken off every museum ticket (Aud, L’Anse, Rouen) so players never mistake one for a code.

**The layer reaches paper, 18 Sept 2026.** `TravelMap/aud_layer.py` draws `aud_features.json` onto the printed sheet, and `build_trail_maps_pdf.py` calls it over the coastline but **under the grid, the stop pins and every label** — the base map’s own labels win any overlap, as on a real map — clipped to the map area so a wood running off the edge stops at the neat line. Appearance is ported from the designer; the two have no shared source (one is SVG in a browser, the other ReportLab), so **a symbol changed in one must be changed in the other**.

**Aud’s frame is now the zoomed one** — lon −22.9751..−20.5451, lat 64.08..65.37. It had to be: the export stores **page points, not coordinates**, so it only lines up with the coastline at the frame it was drawn against. `assert_frame()` compares the two on every build and fails loudly rather than quietly printing a sheet whose coastline has slid out from under its symbols.

**Decorative labels re-set for the zoom.** `Breiðafjörður` ran off the west edge and now sits out in the bay at 65.34, −22.33. `Snæfellsnes` and `DENMARK STRAIT` are **dropped**: both project well off this sheet — the peninsula and the strait are simply not on it. They remain correct for the old wide frame if it is ever restored.

**Two toolchain gaps the first printed sheet exposed.** The exporter was feeding the designer only the research corpus, not the sheet’s own `extra_towns` — so the designer knew about **6 town dots when the sheet prints 13**, and its 19 pt clearance check never covered Búðardalur, Akranes or Stykkishólmur. Symbols were drawn straight over them. The exporter also never mentioned the two boxes the sheet keeps for the **scale bar and compass rose**, so symbols were being placed underneath both. Both are now exported, the designer draws the reserved boxes faintly, and a new scorecard row **In a reserved box** counts them. The layer was re-cleared against the fuller list: four point symbols moved, the largest by 16.5 pt, and the crossing markers rebuilt. **Brief now scores 19 of 20 with section D clean.**

##### Sheet legibility pass — 18 Sept 2026

The first printed sheet read as busy and under-styled. Six fixes, all measured rather than eyeballed:

- **Converging roads now merge.** Each road drew its own dark casing and then its pale carriageway, so the next road’s casing sliced across the previous one’s fill — four roads meeting printed as a braid of parallel dark lines. Roads are now drawn in **two passes**, every casing then every fill, which is what makes a network read as a network.
- **Bridges, fords and gates are oriented.** They were drawn at a fixed angle whatever they crossed. A bridge or ford now lies along the route it carries, a gate sits in the line of its wall, and angles are normalised so nothing prints upside down.
- **The grid steps back** on this sheet only — `#D9CDB2` at 0.3 pt against `TAN` at 0.45. The other three sheets have no drawn layer to compete with and keep the original weight.
- **A legend**, in the clear water bottom-left at `(40, 95)`, 160×200 pt, listing **only the symbols actually on the sheet**. Its box is reserved, so town labels route around it. `FAXAFLÓI` moved to 64.242, −22.108 because it printed across the key.
- **Two self-intersecting polygons repaired** — a wood at I10 and a moor at H11, the “broken forest” in the bottom-right corner. Untangled by 2-opt reversal, so the vertices are unchanged and only their order is rewritten. **The moor’s outline moved up to 95 pt in the process** and is meaningfully a different shape than drawn — worth a look before print.
- **Stykkishólmur plotted 16 pt (3.4 km) out to sea**, the same coarse-coastline problem as Dögurðarnes and on a peninsula 1:50m does not resolve. Added to `PLOT_NUDGE` at `(−0.0324, −0.0480)`, measured not guessed; the nudge now applies to town dots as well as stops. The compass reservation also gained 14 pt of headroom, because a village was printing over its **N**.

**Density, measured:** 89 point symbols, mean 1.8 per occupied grid cell, only **two** cells with four or more. The count is defensible; what made it read as busy is that all 89 are the same purple at the same weight, so nothing recedes. That is a **tone** problem, not a deletion problem — a real survey lets settlements assert and field boundaries whisper.

**Left for a styling pass (Codex):** the area fills — marsh, wood and moor are flat tints where they want texture — and the visual hierarchy above. Also the `bridge` glyph: now that it rotates correctly it reads awkwardly side-on when a road crosses a river north–south, and would be better as two abutment strokes than an arch. **The symbol vocabulary lives in two places with no shared source** — `Aud_Map_Designer.html` (SVG) and `aud_layer.py` (ReportLab) — so any restyle must change both or the designer and the print will disagree. That constraint belongs in the brief.

##### Where Aud’s leg stands — 18 Sept 2026

| Piece | State | Where |
|---|---|---|
| The map | **Drawn, verified, printing.** 140 features, brief scores 19/20 with section D clean. | `TravelMap/aud_features.json` · [Open PDF](../Web/pdf/Trail_Map_3_Aud_Print.pdf) · [answer copy](../Web/pdf/Trail_Map_3_Aud_ANSWER.pdf) |
| The route | **Six legs** (legs 5/6 merged 19 Sept 2026), walked on the real drawn network. | leg table above |
| The code | **`521`** — 5 bridges, 2 fords, 1 gate. | — |
| Card A2 | **Built**, front and back, 19 Sept 2026. Message rewritten to resolve the merged leg 5 (village at the crossing). | [Open PDF](../Web/pdf/Postcard_A2_Hvammur_Print.pdf) |
| The ticket | **Built**, three pages including an answer copy. | [Open PDF](../Web/pdf/Aud_Ticket_Print.pdf) · [Letter sheet](../Web/pdf/Aud_Ticket_Letter_Print.pdf) |
| The designer | Live, mobile-capable, scorecard against this brief. | `TravelMap/Aud_Map_Designer.html` · [published copy](https://claude.ai/artifact/26d6YkdDjuSkN2WS5Uc2fL) |

**The shipped PDFs carry the legibility pass.** An open viewer had them locked for a while, so an earlier pass was verified against a temp build; they have since been rebuilt and checked on the real files — 612×792, legend present, Stykkishólmur ashore, answer copy still reading as the digit **7**.

**Two loose ends on the sheet, both cosmetic and both known:**

- **The moor at H11 is not the shape it was drawn.** Untangling its self-intersection moved its outline by up to 95 pt. It is clean and it is on land, but it should be eyeballed against what was intended before print.
- **The cave at I9 is half-clipped by the map edge.** Cosmetic, one nudge inboard to fix, and very likely the “broken ford” spotted in the bottom-right corner.

**Verified by the user, 26 Sept 2026:** printed a test sheet and hand-walked all six legs against the ticket. `521` — 5 bridges, 2 fords, 1 gate — is confirmed correct. ~~The one verification still outstanding: print a test sheet and walk the six legs by hand against the ticket. Nothing else should be built on top of 521 until it passes.~~

**Downstream, unchanged:** `521` opens the hoard in the cave → coins sorted and their values tallied to `3705` (PZ-010) → `SOLE` → the comb laid over card AD → Harald’s leg unlocks. **Still open:** which coin pile the cache mark names, and A2’s replacement wording.

**Still deliberately absent: labels and the route itself.** Every feature carries an empty label, and that stays true through the rebuild. With repeated symbols doing the ambiguity work, naming them would undo the mechanic — and until the lock mechanic is settled there is nothing for a name to say. Labels, the traced route and the lock are one task, not three.

**Whole approach shelved, 17 Sept 2026 — concept rejected, not a failure.** Everything in this entry describing a **two-panel landscape sheet** with a zoomed Dalir/Hvammur survey panel is parked under `NorseBackpack/Drafts/2026-09-17_Aud_split_panel/` (see its `README.md`). Aud’s sheet is a single portrait map again, the split has been removed from `build_trail_maps_pdf.py`, all four trail maps build portrait, and Aud’s route still traces the digit **7**.

**Why.** One map was wanted, not two at two scales, and portrait rather than landscape. The deciding objection is the symbol vocabulary: a treasure hunt wants clues like *“follow the river upstream to the farmer’s hedge”*, and a hedge is a long sinuous **line** symbol — as are a paved road, a wall, a field boundary. A set of isolated 34 pt object stamps cannot express the clues the hunt actually needs. The drawn terrain lines also read poorly, and the panel lacked the furniture that makes a map feel real, contours above all.

**Completed but never delivered:** the ten v2 vignettes (ford, mill, falls, fold, chapel, cairn, stone, naust, farm, birch) were generated from the prompt set below and wired into the build script immediately before the shelving. They are intact in the drafts folder and are reusable if the replacement design still wants point symbols.

**Carried forward, because they are properties of any sum-based route rather than of this layout:** the two invariants (every stop a different landmark type, since a sum is order-independent; and the numbering verified against every same-type substitution, with nothing wrong landing within 15); the ticket-as-record-card prop; and the clue-chain rules (never name a grid reference, describe by position not appearance).

**Replacing it:** one portrait map, zoomed in, carrying the hunt itself — with line and area symbols (hedge, paved road, wall, field boundary, wood, marsh) and contour lines, rather than isolated icons. Design not settled; see the Open line at the end of this entry.

**Route mechanic redesigned, 17 Sept 2026 — supersedes digits-baked-into-the-artwork.** Everything below this note describing hidden digits worked into the landmark illustrations (`4` paddles, `8` carvings, `1` gate gap, `6` broken stones) and the resulting four-digit code `4816` is superseded. It is kept in place as the record of why the change was made.

**What was wrong with it.** Because the digit lived in the drawing, the same drawing always yielded the same digit. Placing a chapel twice meant both chapels carried `6`, so picking the wrong one cost nothing and the decoy was decorative. Making decoys bite would have meant a separate render per digit variant — roughly eighteen icons instead of nine — and it forced every clue to describe a landmark’s *appearance* rather than its position.

**The replacement.** Every cell of the detail panel carries its own small two-digit **survey plot number** printed quietly in one corner. Repeats across the grid are fine and expected — the numbers are a lookup table, not a signal. Players follow a clue chain from landmark to landmark, write down the plot number of each stop, and **the lock code is the sum of the stops’ plot numbers**. This decouples the artwork from the puzzle entirely: icons can now repeat freely, and Codex draws a landscape rather than digit-bearing icons.

**Lock is now three digits, not four.** Seven stops with two-digit plot numbers sum to the mid-hundreds. A four-digit result is arithmetically unreachable this way (it would need a route of well over a hundred cells), so the treasure lock drops to three dials. The code is derived from whatever the final numbering is rather than chosen up front — see the working value below.

**Two rules this mechanic forces, both learned the hard way.**

- **Every stop must be a different landmark type.** Addition is order-independent, so two stops sharing a type can be swapped for free and still total correctly. A first pass with sheepfolds at both stop 4 and stop 6 produced three wrong routes summing to exactly the right answer. Seven stops therefore use seven distinct types.
- **The numbering must be verified, not assumed.** Every near-miss route — each stop substituted for each same-type decoy on the map — is enumerated and checked. Nothing wrong may land within `15` of the answer. The same first pass had a wrong route two away from the target, indistinguishable from an arithmetic slip.

The upside of order-independence: players **cannot fail by walking the route in the wrong order**. Only misidentifying a landmark hurts. One whole failure mode is gone.

**Superseded, 18 Sept 2026 — this route and its plot-number code are dead.** Both belonged to the shelved split-panel landscape and to the plot-number mechanic retired with it. The live route is the six legs recorded above (legs 5 and 6 merged 19 Sept 2026), walked on the real drawn network, with the code `521` counted from bridges, fords and gates. The table below is kept only so the reasoning behind the two rules above survives — its landmark names, cells and plot numbers refer to a sheet that no longer exists.

**Working route and code, 17 Sept 2026 — provisional, tied to the current numbering:**

| Stop | Type | Cell | Plot | Same-type decoys on the map |
|---|---|---|---|---|
| 1 | The old ford | `c7` | `59` | none — given on the ticket |
| 2 | Watermill | `d7` | `79` | 1 (mill on the north branch) |
| 3 | Falls | `e4` | `45` | none — the one free hop |
| 4 | Sheepfold | `d3` | `71` | 2 |
| 5 | Ruined chapel | `b4` | `49` | 1 — **the deliberate ambiguity** |
| 6 | Cairn | `c9` | `86` | 3 |
| 7 | Standing stone | `f8` | `78` | 1 |

**Sum: `467`.** Verified against all **95** wrong-but-plausible routes; the closest lands **20** away. The numbering, the landmark placements, the route and the check all live together in `TravelMap/aud_detail_panel.py`, and `build_trail_maps_pdf.py` now imports them rather than holding its own copy — **built and rendering as of 17 Sept 2026**. Run `python aud_detail_panel.py` after changing *any* plot number or placement; it exits non-zero if an invariant breaks. It enforces four things: seven distinct stop types, no wrong route within `15` of the answer, no stop carrying a plot number under `20` (which would put “omit one stop” inside the margin), and no two features sharing a cell. All four guards were confirmed to fire by deliberately reintroducing the bugs they exist to catch.

**The clue chain — six clues, since stop 1 is given.** Each clue moves players from one stop to the next. Two standing constraints on the copy: **never name a grid reference** (that hands over the plot number), and **describe by position, not appearance** (all three sheepfolds are the same drawing; “the fold below the saddle” works, “the round fold” does not). One hop is deliberately free of decoys as a breather; one hop — the chapel — is deliberately ambiguous and is resolved only by A2’s in-person observation. **No clue copy is written yet**, and it is drafted against the finished map, not before, or it will describe terrain that does not exist.

**Prop consolidation, 17 Sept 2026 — the ticket *is* the record card.** A separate tally sheet was sketched, then merged into the museum ticket: **front** is the ticket face (masthead, stamped admission data, and a boxed panel giving the starting point), **reverse** is a seven-row `STOP / SITE / PLOT No.` form with a ruled `TOTAL` box. **Row 1 is pre-filled in handwriting** — *the old ford — 59* — which does four jobs at once: gives the start point where it will be used, teaches the recording format by example, confirms the route is seven stops without saying so, and hands players one verifiable lookup so their first grid read succeeds before any clue-solving begins.

The **SITE** column matters as much as the number box: writing down which landmark they believe they found makes a misidentification visible when players compare notes, instead of silently poisoning the sum. Rejected alternative: ten blank unnumbered rows, which hides the route length but removes the self-check — the sum already has no partial credit and no feedback, so difficulty belongs in the clue chain, not in concealing how many stops there are.

**Risk accepted:** one prop now carries the start point, the working record and the total, and must survive being written on and handled all game. Mitigation to decide: larger number boxes for pencil, or a blank spare record card in the envelope.

**Clue distribution, decided 17 Sept 2026:** the museum ticket gives the **starting point only**. **Postcard 1** carries the six-hop chain, written as continuous prose rather than a numbered list so that parsing it is part of the work. **Postcard 2** carries the single in-person detail that resolves the ambiguous hop. **Rewritten 18 Sept 2026:** it no longer points at a chapel in a birch hollow — that chapel is 14.5 pt off the network and can never be a route step. It now resolves **leg 5**, the fork at the standing stone; see Q-019.

**Revised and extended, 16–17 Sept 2026.** Gives Aud a museum ticket (previously the one trail without one), moves the weighing instruction from Hvammur to Dögurðarnes so Hvammur's old job doesn't leave it without one (PZ-010), and gives decoy card AD a lock job it lacked (the standing “every card gates a lock” rule, PZ-013) by having it end the chain together with the comb, which moves back from Harald’s trail to Aud’s.

**Step 1 is stale, 18 Sept 2026.** The Dalir split-panel map it describes was built and then shelved the same day — see `NorseBackpack/Drafts/2026-09-17_Aud_split_panel/README.md`. Aud’s sheet is a plain portrait map again and the treasure hunt is being redesigned to live on it; A2’s route-directing text can’t be written until that redesign lands. Steps 2–5 (the hoard, the comb, BOOK) are unaffected in concept, and A1/A3 are already built against them.

**Decided player flow, in order:**

1. Stale Players have postcard A2 (Hvammur), Aud’s laminated journey map, and a new fictional ticket, **Aud’s Treasure Museum** (tied to Hvammur; no historical accuracy needed, unlike the other trails’ tickets). Together these direct a four-step treasure route on the map. The map gains a grid, contour lines, river, paths and named local features; each unambiguous destination square hides one digit. **This describes the shelved Dalir panel design, not the current map — see the note above.**
2. The three-digit route code `521` releases the loose coin hoard (three currencies mixed) and the treasure tally, **together with postcards A1 (Dögurðarnes) and A3 (Esjuberg)** (step 7 of old page PC-18). **Superseded, 25 Sept 2026:** this step read “The four digits open a lock” and said a physical scale was handed out earlier. There is no scale any more.
3. The final treasure square also bears the cache mark for one coin type. Players sort the whole hoard, select that matching pile, add the selected coins’ values with the merchant’s key to `3705`, record it on the treasure tally (**Dögurðarnes**), then turn the whole tally upside down (**Esjuberg**) to reach `SOLE` (PZ-010). **Superseded, 22 Sept 2026:** replaces the weighing instruction and scale-display clue.
4. `SOLE` opens a lock releasing **decoy card AD (Bjarnarhöfn) and the comb** together. AD’s message, decided 18 Sept 2026, has Liv say Aud’s own comb — found alongside the coins, kept with the museum’s permission — is “the real treasure”; see [the comb prop] for the full text.
5. The comb, laid across AD’s message, exposes certain letters through its broken teeth, spelling candidate code `BOOK` (**decided 25 Sept 2026**: an upright comb, one tooth per line, reads B-O-O-K from lines 1, 3, 8 and 9; see the comb prop). The exposed code opens a lock that **gates entry to Harald’s leg** — Aud’s whole chain must be finished before Harald’s can start.

**Map detail built, 17 Sept 2026.** The single Aud sheet is now two panels: the unchanged full-region frame/projection/labels are uniformly reduced into the right panel; a new Dalir/Hvammur detail with a visually distinct 2×4 lowercase-letter/number grid sits left. It carries five placements in distinct cells: mill, Auðarsteinn, sheepfold, Bjarnarhöfn chapel (decoy) and inland chapel (target). Exact grid references and all ticket/A2 wording remain open.
**Superseded later the same day, and now built — portrait sheet, 2×4 grid and five placements are all replaced.** The sheet turns **landscape** (792×612 pt), which makes both panels larger rather than trading one against the other: the main map goes from 381×502 pt at scale `0.67` to **432×569 pt at scale `0.760`**, because its native 569×749 pt footprint drops almost exactly into landscape’s usable height. The detail panel goes from 156 pt wide to **307×569 pt**, carrying a **6×10 grid** of 46×50 pt cells with icons at 34 pt (about 74% of a cell). An inset cartouche inside the main map’s ocean was considered and rejected — cartographically the more authentic move, but it caps out around 220×300 pt, too small for a 6×10 hunt grid.
**Superseded, 18 Sept 2026 — everything from here to the end of this vignette spec describes the shelved split-panel sheet.** There is no detail panel: the hunt is drawn on the single portrait map, and the live route and code are recorded above. In particular the birch icon is **no longer load-bearing** — the two lookalike chapels are not the ambiguous hop any more, the fork at the standing stone is, and the detail that resolves it is which road runs into the trees. The ten v2 vignettes are shelved with the rest under `Drafts/2026-09-17_Aud_split_panel/` and have never appeared on a delivered sheet.
The panel is now drawn as a **naturalistic surveyed valley, not a puzzle board**: fjord shore, a river with a confluence, a ford and falls, hachured hills with a saddle, two tracks, and roughly **28 features across the 60 cells** — farmsteads with home-fields, naust, birch woods, marsh, cairns, sheepfolds, mills, chapels and standing stones. Landmarks sit on the terrain feature that explains them (the mill on the river, the fold on a slope, the chapels one coastal and one in a birch hollow), so the clues can lean on position instead of appearance. The ten reusable v2 landmark icons are now placed from production PNGs; the placements, route and plot numbers remain fixed when artwork is refreshed. Each icon gets a small deterministic per-cell nudge so they never all sit cell-centred (six centred icons read as a grid overlay rather than scenery), bounded so that no glyph can cross a cell line — a landmark straddling a boundary would let players read the wrong plot number.

Exact ImageGen prompts — landscape icon vocabulary, v2 (current)

Ten vignettes, one render per kind, written 17 Sept 2026 against the built panel. The kind strings match `aud_detail_panel.py`’s `FEATURES` exactly, so placement needs no translation table. **Marsh is deliberately not on this list** — it stays a vector tuft texture in the build script, since a diffuse wetland reads better as drawn texture than as an isolated object. The farmstead’s home-field enclosure is also drawn by the script, so that icon is the building only.

```
SHARED BLOCK (prepend to every icon below)

Use case: illustration-story
Asset type: tiny transparent decorative vignette for a printable Viking-era land-survey map
Style/medium: very simple flat hand-pulled screen-print map icon; elegant antique pictorial-map
ornament; minimal internal detail; lightly weathered ink edges
Composition/framing: one isolated object, compact roughly square silhouette, centered, generous
transparent margin
Viewpoint: simple side elevation seen slightly from above, consistent across the whole set
(the sheepfold is the one deliberate exception -- see its entry)
Color palette: purple #6D528B only
Constraints: genuinely transparent background with alpha; must stay legible at 34 pt (about
0.47 inches) wide; thin-to-medium outline; no text, no numerals, no border, no shadow, no
ground shadow, no paper texture, no gradient, no cross-hatching, no watermark, no extra objects

TWO RULES THAT OVERRIDE ANY INSTINCT TO ADD DETAIL

1. NO HIDDEN COUNTS. Do not work any countable detail into these icons. The previous version of
this set hid digits in the artwork -- four wheel paddles, eight carved marks -- and it was
dropped. The puzzle's digits now live in the plot numbers printed in the map's grid cells.
A conspicuous countable set of marks in an icon is therefore an active red herring now.
Where an element repeats (stones, planks, trees), keep the number irregular and unobtrusive.

2. EACH ICON IS REUSED AS-IS. Several appear more than once on the same sheet: up to five
farmsteads, four cairns, three sheepfolds, two mills, two chapels, two standing stones, two
naust, four birch clumps. One render per kind, placed repeatedly by the build script. Do not
produce variants -- the decoys are supposed to be visually identical to the real one, and the
clue text tells them apart by position. Design each icon so it still reads well when the same
image appears several times on one sheet.

THE TEN ICONS

ford
A line of four or five flat stepping stones crossing a shallow watercourse, seen from slightly
above. Leave the left and right edges open: this mark is placed on top of a drawn river line
and has to read as continuing into it.
Must read as: a crossing place, not a row of loose rocks.

mill
A small gabled wheel-house with a large overshot waterwheel mounted on one side. The wheel's
circular silhouette is the whole identity of this icon and must stay unmistakable at 34 pt.
Must read as: a watermill, distinct from the farmstead, at a glance.

falls
A stepped drop in a watercourse: a short rock lip with water breaking over it in two or three
ledges. Like the ford, leave left and right edges open to meet a drawn river line.
Must read as: falling water, not a bridge or a dam.

fold
A small drystone sheep pen (rett) seen in PLAN, from directly overhead -- the one viewpoint
exception in this set, because a pen reads as a ring only from above. An irregular oval ring
wall of dry-laid stone with a single narrow gate gap.
Must read as: a stock pen, not a building foundation or a well.

chapel
A small roofless rectangular stone chapel. One gable end still stands with a simple cross at
its apex; the opposite wall is broken down to a jagged stub, and there is no roof between them.
Must read as: a ruin, immediately, not an intact church.

cairn
A conical heap of many loose stones, broad at the base and tapering to a rough point, with
individual stones visible as irregular courses.
Must read as: a heap of many stones. See the warning under "stone".

stone
One single tall upright monolith -- a narrow worked slab roughly two and a half times taller
than it is wide, planted upright in the ground with a short ground line at its foot.
Must read as: ONE standing stone.
WARNING, the most important constraint in this set: the cairn and the standing stone are stops
6 and 7 of the treasure route, and confusing them breaks the puzzle. Make the silhouettes
opposite: the cairn is WIDE, low and made of MANY stones; the standing stone is NARROW, tall
and a SINGLE stone. If both were reduced to solid black shapes they must still be instantly
tellable apart.

naust
A low boat shed with a turf roof, its gable end facing the viewer, with an open dark doorway
wide enough to run a boat's prow through.
Must read as: a shed open at one end, distinct from the farmstead's closed longhouse.

farm
A small turf-walled longhouse with an intact pitched roof and a smoke louvre at the ridge,
standing alone. NO enclosure, fence or field boundary -- the build script draws the home-field
rectangle around this icon, and a second boundary in the artwork would collide with it.
Must read as: an inhabited farmhouse, intact, distinct from the roofless chapel.

birch
A compact clump of three or four slender birch trees with rounded crowns and pale slim trunks,
touching but not merged.
Must read as: a small stand of trees. This one is load-bearing: the birch hollow is the terrain
detail that tells the two lookalike chapels apart, so it has to be unmistakable at small size.

ASSET HANDLING

Retain each source render at TravelMap/Art/Sources/Aud_<kind>_v2_ImageGen_Source.png, then run
normalize_aud_vignettes.py, which thresholds alpha, fills enclosed alpha holes and makes every
visible production pixel exactly #6D528B. Production files land at TravelMap/Art/Aud_<kind>_v2.png.

<kind> must be exactly one of: ford, mill, falls, fold, chapel, cairn, stone, naust, farm, birch
-- the same strings aud_detail_panel.py uses in FEATURES.

Wiring: replace the placeholder vector bodies in build_trail_maps_pdf.py's _aud_glyph() with
image draws. Placements, route and plot numbers do not move. Keep each drawn image inside a
34 x 34 pt box: _aud_offset()'s docstring records the clearance budget that stops a glyph from
crossing a cell line, and a larger glyph would break it.
```

**Built, 17 Sept 2026.** All ten v2 production icons now live in `TravelMap/Art/Aud_<kind>_v2.png`, with untouched ImageGen source renders in `TravelMap/Art/Sources/`. `build_trail_maps_pdf.py` uses those reusable files in the 34 pt clearance boxes; only marsh remains vector terrain by design. The retired digit-bearing `Aud_*_v1.png` set is not used by the panel.

**Exact ImageGen prompts & asset handling — SUPERSEDED 17 Sept 2026 (digits no longer live in the art)**

Kept for the shared style block, which is still correct, and as the record of the rejected approach. Every “work the hidden digit N into the illustration” instruction is void: plot numbers on the grid now carry the digits, so icons may repeat freely and a new prompt set is needed for a full landscape vocabulary rather than four digit-bearing icons. The rendered `Aud_*_v1.png` files were rejected on their own terms too — the watermill read as a full scene rather than an isolated vignette, Auðarsteinn’s eight marks read as a dice face in an obvious 2×4 dot grid, and the sheepfold and chapel carried no visible digit at all.

```
Shared block (all four):
Use case: illustration-story
Asset type: tiny transparent decorative vignette for a printable Viking treasure map
Style/medium: very simple flat hand-pulled screen-print map icon; elegant antique adventure-map ornament; minimal internal detail and lightly weathered ink edges
Composition/framing: one isolated object, compact silhouette, centered, generous transparent margin
Color palette: purple #6D528B only
Constraints: genuinely transparent background with alpha; simple enough to read at roughly 0.55-0.7 inches wide; thin-to-medium outline; no text, no border, no shadow, no paper texture, no gradient, no cross-hatching, no watermark, no extra objects

Watermill: A small overshot waterwheel against a plain wheel-house wall, clean side profile. Work the hidden digit 4 naturally into the illustration as exactly four clearly countable wheel paddles, without showing a printed numeral.
Auðarsteinn: One single upright roughly tapered monument stone/boulder, straight-on, clearly a standing stone rather than scenery. Work the hidden digit 8 naturally into the illustration as eight tiny, simple weathered carving marks or pockmarks, without showing a printed numeral.
Sheepfold (rétt): A small circular or spiral drystone enclosure wall from a high angled/top-down view, clearly a stock pen rather than a building foundation. Work the hidden digit 1 naturally into the illustration as one distinct narrow entrance gap in the enclosure wall, without showing a printed numeral.
Ruined chapel: A small roofless stone chapel with a simple gable outline, three-quarter view, visibly a ruin by its broken wall line rather than an intact building. Work a hidden digit 6 naturally into the illustration as six small, countable missing or broken stones along the wall line, without showing a printed numeral. This exact same icon will be placed twice on the map.

Files: source renders are retained in `TravelMap/Art/Sources/Aud_*_ImageGen_Source.png`; `normalize_aud_vignettes.py` thresholds alpha, fills enclosed alpha holes and makes every visible production pixel exact `#6D528B`.
```

**Four-step route decided, 16 Sept 2026.** The wrinkle raised earlier — the museum ticket's written clues alone shouldn't be enough to find the treasure's final spot — is now designed. Card A2 (Hvammur)'s message is drafted with a placeholder line acknowledging a "treasure hunt at the Aud museum" and still withholds the actual observation text until it's written, but the mechanism producing it is fixed — see Q-019.

**The four landmarks, all near Hvammur/Dalir, digits and code decided 16 Sept 2026.Superseded 17 Sept 2026** — the per-landmark digits and the code `4816` are void; the route is now seven stops of seven distinct types summing their plot numbers. What survives from this list: Auðarsteinn as a real, sourced place; the lookalike-chapel ambiguity and its coastal-vs-birch-hollow resolution, which is still the one deliberately ambiguous hop.

- **The old watermill — digit 4.** A small ruined mill on a stream. Plain, findable from the ticket's description alone.
- **Auðarsteinn ("Aud's Stone") — digit 8.** Real, not invented: Laxdæla saga ties a stone near Hvammsfjörður to Aud's own death account. Findable from the ticket alone.
- **A sheepfold (rétt) — digit 1.** Findable from the ticket alone.
- **A lookalike chapel pair — digit 6, the actual wrinkle, and the final square carrying the coin-cache mark.** The ticket's description must fit two near-identical ruined chapels equally well. One sits at **Bjarnarhöfn**, the decoy card AD's own real location — a plausible wrong answer since that site is already "in play" as a card, and shown coastal on its own postcard front. The real target sits inland among birches instead. The distinguishing observation belongs in A2’s message, but **its wording is not written yet**. No new icon variant is used: the two chapel placements differ only by their map context (coastal vs. inland), not by their art.

**Resulting code, in the decided route order (mill → Auðarsteinn → sheepfold → chapel): `4816`. Superseded 17 Sept 2026** — replaced by the three-digit plot sum `467`, which was re-checked against every other code in the page (`1021`, `1576`, `1972`, `231`, `253`, `427`, `582`, `562`, `2468`) — no collision. It does repeat a digit, which `4816` deliberately avoided; that constraint is dropped, since the sum is computed rather than read off and cannot be made digit-unique by choice.

![Aud's map sheet split into two side-by-side panels: a new zoomed detail of Dalir/Hvammur on the left with its own small grid holding the four treasure landmarks, and the existing full-region map shifted right, unchanged.](Art/Diagrams/Diagram_Aud_Map_Split.svg)**Scale problem, and the fix.** At the main map's real scale (~23 km per grid cell), all four landmarks near Hvammur would collide into about one cell — the same problem Rollo's Rouen/Roumare pair hit. Fix: split the one physical sheet into two side-by-side panels. The right panel keeps the existing full-region map exactly as built, still carrying Aud's four real postcard stops for the final digit-shape trace. The left panel is a new zoomed-in detail of just Dalir/Hvammur with its own small grid, giving the four landmarks room to land in genuinely distinct cells. **Diagram outdated, 17 Sept 2026:** the split-panel principle it shows still holds, but the sheet is now landscape rather than portrait, the detail grid is 6×10 rather than 2×4, and the panel carries about 28 terrain features and seven stops rather than five bare icons. It needs redrawing.

**Open:** the six clue hops’ copy, split across two postcards (nothing written yet — drafted against the finished map, not before); the fjord still reads as a plain diagonal coastline rather than an inlet with a head, and the north river branch competes with it at similar line weight; whether the ticket gets larger pencil boxes or a spare blank record card; the three coin types and cache mark; coin quantity/design and fictional values (PP-037); a physical check that the selected coins total `3705` and the rotated tally reads `SOLE` (PP-026) without interfering with the map’s final route-tracing job; AD’s exact message text; and which words the comb needs to expose on it, and the resulting code.
