# Project Handoff

Last updated: 2026-09-14 by Claude Code

> Session continuity only. Open design questions are **not** tracked here — they live in the
> Open questions tab of `NorseBackpack/Norse_Brainstorm.html`, each with a stable ID.
> See "Where Design State Lives" in `AGENTS.md`.

## Session Close — 2026-09-14 (continued) — Harald's trail map sheet unblocked and built

**Task, same session continued:** start Harald's trail map sheet, which `build_trail_maps_pdf.py`
had listed in `BLOCKED` since stops 5–6 ("Sicily", "Asia Minor") were regions, not named points.

**Researched real, verifiable places for both** (WebSearch, not memory):
- **Sicily → Syracuse.** Confirmed by multiple sources: during the 1038–1040 Byzantine campaign
  under George Maniakes, Harald's forces took part in capturing Messina and Syracuse — a specific,
  well-documented site.
- **Asia Minor → no single city resolves.** Every source describes a broad sweep (~80 strongholds
  captured, advancing to the Euphrates), no named city tied to Harald specifically. Reported this
  honestly to the user rather than inventing one; they chose **"pick a representative city, clearly
  flagged as illustrative."** Chose **Melitene** (modern Malatya) — a real, well-documented
  Byzantine-Arab frontier fortress directly on the Euphrates, explicitly marked as a placement
  choice, not a sourced fact about Harald.

**Updated the sourced data in two places** (both needed — they're separate copies): `stops.js`
(the 72-entry research corpus, plus two new source entries) and `Norse_Aunt_Route_Plan.json`'s
embedded `visits.harald` copies for `h-sicily`/`h-anatolia`. New evidence category `illustrative`
added for the Melitene entry, distinct from `supported`/`saga`/`uncertain`, so it can't be mistaken
for sourced fact later.

**Added `harald` to `TRAILS` and built the sheet** — first attempt succeeded cleanly (no dropped
labels, no collisions): all six stops findable by name. Title `THE VARANGIAN ROAD` is a draft pick,
not yet confirmed with the user. Frame is necessarily much more zoomed out than the other three
sheets (continent-spanning: Norway to Sicily to eastern Anatolia) — a coarser km-per-square is an
accepted consequence, not an oversight.

**Real problem caught: the traced route doesn't read as a digit `2`.** Plotted in visit order, the
path crosses west↔east twice — a zigzag, not a clean 2. Flagged to the user before going further
(this is the core final-puzzle mechanic — traced shapes read as the code). They chose **accept as-is**
over reordering (which would also require re-checking `PZ-08`'s postmark-order constraint and
`PZ-11`'s held-back-card choice).

**Second, independent instance of the same problem found and partially fixed:** the "Travel routes"
tab already had a hardcoded, hand-drawn SVG polyline captioned "Harald route shaped like the digit
2" — an idealized target shape drawn before the real map existed, not derived from any projection,
plus a full duplicate copy of the old Sicily/Anatolia stop text (name, note, source link) that
`stops.js` alone doesn't drive. Updated that duplicate text to Syracuse/Melitene and re-captioned the
SVG as an idealized target that the real map doesn't achieve, rather than leaving the page
contradicting its own answer key.

### Files changed

- `NorseBackpack/TravelMap/stops.js` — `h-sicily`→Syracuse, `h-anatolia`→Melitene (new coordinates,
  evidence/precision/note/source), two new `NORSE_SOURCES` entries.
- `NorseBackpack/TravelMap/Norse_Aunt_Route_Plan.json` — same two stops' embedded copies updated to
  match.
- `NorseBackpack/TravelMap/build_trail_maps_pdf.py` — `BLOCKED` emptied; new `harald` entry in
  `TRAILS` (frame, parallels, title, band colour, minimal/empty regions-areas-waters-extra_towns).
- `output/pdf/Trail_Map_4_Harald_Print.pdf`, `Trail_Map_4_Harald_ANSWER.pdf` — new.
- `NorseBackpack/Norse_Brainstorm.html` — `PZ-09` (Harald's sheet now built, shape risk noted),
  `PZ-11` (Aldeigjuborg hold-back flagged stale, needs re-test against the real projection), `PZ-06`
  (the "loosest of the four" note updated to reflect the real zigzag), the postcard-gallery Harald
  caption, the prop-kit list's "three of four sheets built" line, and the Travel routes tab's
  hardcoded Harald route-card (stale stop text + misleadingly confident SVG shape).

### Checks run

- Ran `build_trail_maps_pdf.py harald`: clean build, no `STOPS NOT LABELLED` line, no label
  collisions reported.
- Rendered both the print and ANSWER PDFs at 200dpi and inspected visually: all six stops labelled
  and findable, coastlines/grid/scale bar/compass all correct, no overlap or dropped content.
- Verified the shape problem by reading the actual projected stop order off the rendered answer
  key, not by assumption.
- Live-checked (served over local HTTP) that both the Travel routes tab's Leaflet mini-map and the
  separate `Travel_Map.html` workshop page pick up the new Syracuse/Melitene data automatically
  (both read `stops.js` at runtime) — no console errors on either page.
- HTML tag balance after all edits: 897 `div`, 12 `section`, 64 `figure`, 23 `details`, 23 `article`,
  13 `ul`, 108 `li`, 80 `a`, 5 `svg`, 7 `ol` — all paired.
- Validated `Norse_Aunt_Route_Plan.json` still parses after editing.
- Deleted temporary preview PNGs after inspection.

### Next action

Re-test `PZ-11`'s Harald hold-back choice (Aldeigjuborg/Staraya Ladoga) against the real built map's
projection — it was chosen on an approximate projection before this sheet existed, and the "one-card-
removed" shape test needs redoing now that six real points exist.

### Blockers / open items

- `PZ-11`'s Harald hold-back card is stale (see Next action).
- Title `THE VARANGIAN ROAD` is an unconfirmed draft pick.
- Harald's sheet has no decorative regions/areas/waters/extra-town labels yet (the other three
  sheets each have 8–25) — currently only the six real stops are labelled.
- The hnefatafl board-setup panel (`Props/Hnefatafl/build_board_setup_pdf.py`) still needs
  compositing onto this sheet's back now that it exists.
- The coin puzzle's three mint-city locations (`PZ-09`) are still unplaced on this sheet.
- `PR-11`-style decorative vignettes (present on Leif's and Rollo's sheets) don't exist for Harald.

## Session Close — 2026-09-14 — Incomplete hand-drawn hnefatafl setup sketch

**Task:** create a square, high-resolution PNG of the final 11×11 board setup as Liv's practical
pen sketch on the blank white back of a document, with columns I–K made unreadable by wet ink
transferred and dragged when another sheet was lifted away.

**Built, then revised:** `Hnefatafl_Incomplete_Board_Sketch_v3.png` is the selected 1254×1254
PNG. It keeps the exact dark-green hand-ruled setup on plain white document paper. Columns I–K
now show restrained lifted ink: mostly white paper with broken grid fragments, offset ghosts and
small dragged marks. The information is missing rather than hidden under a dark mass. The visible
A–H positions were checked cell-by-cell against the user's coordinate list. The heavier v1 and
v2 treatments are retained beside it as superseded directions.

**Companion paper built:** `Hnefatafl_Transferred_Ink_Paper_v1.png` (1254×1254 PNG). It carries
only the transferred 3×11 strip, horizontally mirrored as K–J–I: attackers at K8, K4 and I6,
with rust diamonds at K11 and K1. The grid and marks are readable but retain slight feathering,
missing flecks and offset ghosts so they look transferred rather than freshly redrawn.

**Project-page record:** added both rendered images and their exact built-in ImageGen prompts to
the Hnefatafl setup section in `NorseBackpack/Norse_Brainstorm.html`.

**Checks:** confirmed PNG format and 1254×1254 dimensions for v3; inspected the full render; checked the
11×11 cell count, visible token coordinates, lack of text/labels, and fragmented I–K area. HTML
tag balance and live browser rendering were checked after the edit.

**Next action:** decide whether v3 becomes the actual Harald map-back artwork or remains a
visual direction alongside the existing deterministic PDF panel. No PDF was rebuilt in this
session.

## Session Close — 2026-09-14 (continued) — Board size changed to 11×11; user's final layout solved and all props rebuilt

**Task, same session continued:** the user asked to make the board "more realistic" — first proposed
10×10, then corrected to 11×11 after I flagged that 10×10 has no true centre square (even-sized
board). Built an interactive sandbox so they could design the final layout themselves; they used it
and handed back a finished 22-piece layout (16 attackers, 6 defenders) in the tool's own export
format.

**Built:** `NorseBackpack/Props/Hnefatafl/board_designer.html` — standalone, self-contained 11×11
sandbox with true centre throne (F6), an adapted starting layout (8 defenders in a ring inspired by
Tablut's pattern, 20 attackers in edge rows — not claimed as verified history for this size), slide
movement with custodian captures, a free-form Place/Edit mode, and a live coordinate export.

**Solved the user's final layout by exhaustive search** (not eyeballed): 1 and 2 moves have zero
solutions, **3 moves has exactly one** — `F6 → H6 → H11 → K11`, legs 2/5/3, code `253` — and 4 moves
already has 18. Also verified the hidden-strip property still holds at this size: assuming the three
hidden columns (I–K) are empty finds 31 false candidate routes, so the puzzle still "refuses to
resolve instead of resolving wrongly."

**Rebuilt all three Hnefatafl props at 11×11**, sharing one updated geometry module:
- `board_layout.py` — full rewrite: `ATTACKERS`/`DEFENDERS` tracked as separate sets (not just one
  undifferentiated `BLOCKS`), 11×11 `SIZE`, new throne/corners/solution path, new A–H visible /
  I–K hidden column split (up from A–E/F–G at 7×7).
- `build_board_setup_pdf.py` — map-back panel now draws attackers (dark) and defenders (light,
  outlined) as visually distinct tokens; stain enlarged to 3 columns; caption switched from a full
  coordinate list to counts (19 pieces don't fit legibly on one line the way 10 did).
- `build_ticket_pdf.py` — mirrored offset panel now 3 columns (K, J, I reversed) instead of 2,
  also with distinct attacker/defender tokens; ticket page grew from 2.4×5.6in to 2.6×6.6in to fit.
- The **interactive prototype in the main page itself** (previously left stale at 7×7 in the prior
  entry below) was also updated: 11×11 grid, real attacker/defender sets, corrected corner test,
  reset/hint routes rewritten to the new solution. This was not explicitly requested but leaving the
  page's own demo showing a superseded 7×7 board while every other section described 11×11 would
  have been a real inconsistency.

**`PZ-01` moved from "in progress" back to Decided** (at 11×11) — the 7×7 solution stays visible only
where explicitly marked as a superseded illustration (`PZ-07`'s old SVG diagram caption), not
anywhere it could be mistaken for current.

### Files changed

- `NorseBackpack/Props/Hnefatafl/board_designer.html` — new (from the "in progress" half of this
  session).
- `NorseBackpack/Props/Hnefatafl/board_layout.py` — full rewrite for 11×11.
- `NorseBackpack/Props/Hnefatafl/build_board_setup_pdf.py` — rebuilt for 11×11, attacker/defender
  token distinction.
- `NorseBackpack/Props/Hnefatafl/build_ticket_pdf.py` — rebuilt for 11×11, same token distinction.
- `output/pdf/Hnefatafl_Board_Setup_Insert.pdf`, `Hnefatafl_Ticket_Print.pdf`,
  `Hnefatafl_Ticket_Letter_Print.pdf` — rebuilt in place.
- `NorseBackpack/Norse_Brainstorm.html` — `PZ-01` (finalized 11×11 solution/code, pill back to
  Decided), `PZ-07` (rebuilt-panel details, 3-column split), `PR-08` (11×11 target, piece-count
  note), the codes-reference table row, "What the board feeds" card, the interactive prototype's
  CSS (`.board` grid now 11 columns, new `.cell.defenderblock` style, resized king/token glyphs)
  and JS (`attackers`/`defenders`/`blocks` sets, 121-cell render loop, corrected corner test, new
  reset/hint routes), and its surrounding panel text.

### Checks run

- Ran the uniqueness search in a throwaway script (not committed) over the user's exact layout:
  confirmed 0/0/1/18 solutions at 1/2/3/4 moves, and 31 false candidates assuming I–K empty.
- Rebuilt both PDF props and rendered every page (map insert, ticket front, ticket back) at
  250–300dpi; cross-checked the map panel's visible tokens and the ticket's mirrored panel token-
  by-token against the layout data — all 19 visible + 3 hidden (via the ticket) pieces landed on the
  exact expected squares.
- Loaded the main page's Prototype tab live in the browser, clicked "Show route": rendered
  "Solution: F6 → H6 → H11 → K11. Legs: 2, 5, 3 → code 253." exactly matching the search result, on
  an 11×11 grid with the corners in all four visual corners. No console errors.
- HTML tag balance after all edits: 897 `div`, 12 `section`, 63 `figure`, 22 `details`, 23 `article`,
  13 `ul`, 108 `li`, 80 `a` — all paired.
- Deleted temporary preview PNGs and the scratch solver script after inspection.

### Next action

Decide whether Codex should start Oslo's front artwork now, or wait for Harald's trail map sheet to
exist first — same open call as before, unaffected by the board-size work.

### Blockers / open items

- Harald's trail map sheet still doesn't exist — the real blocker for finishing this puzzle's
  physical props (unchanged from earlier this session).
- `PR-08` (which specific 11×11 board/piece set to buy) is still unchecked against real listings.
- The Oslo postcard's front artwork and print PDF are still unbuilt.
- `PR-09`'s physical print test (does the offset read through the ticket, does the stain hide the
  original) has not been run — the props are sized correctly now but untested on paper.

## Session Close — 2026-09-14 — King's escape (hnefatafl): compartment dropped, moved to Harald, ticket + map-back panel built

**Task:** continue the king's escape puzzle. In chat, the user dropped the throne-compartment
idea entirely (board is now a straightforward bought prop, no cavity), then asked to build the
Oslo museum ticket, the Oslo postcard text, and the map-back setup panel + its mirrored offset —
for **Harald's trail**, not Leif's (reassigning `PZ-07`/`PZ-09`).

**Decided in chat, written into the page:**
- Throne compartment dropped (`PZ-01` candidate summary, `PR-08`, the puzzle-detail card, the
  "Needs work" note, the "build" tab's prop-kit bullet, the 3D-printer inventory line).
- The prop renamed pamphlet → **ticket** throughout (it's flat, not folded — confirmed with the
  user this is the same object, not a second prop).
- Ticket content simplified to the *real* historical rules (light defenders at centre, dark
  attackers, sandwich-capture, king escapes to a corner) — general museum-visitor copy, not this
  puzzle's own house rules (fixed non-moving blockers). Liv's actual task line ("get him to a
  corner in exactly three moves") moved to the **Oslo postcard** instead, in her voice: "We like
  to play our own rules though: can you get the king to escape to a corner in exactly three
  moves?"
- Whole mechanism reassigned from Leif's map to **Harald's Oslo map** (`PZ-07`, `PZ-09`) — Oslo is
  a real, verified stop (`h-oslo`, order 1, Harald's trail opener). Harald's trail map sheet does
  **not exist yet** (`build_trail_maps_pdf.py` has no entry for him, and two of his six stops are
  still regions, not named places) — flagged to the user before drafting, who chose to draft text
  now and let the art wait.
- Oslo postcard message and Fun Fact drafted and written into `PZ-05` (not yet built as a PDF —
  blocked on front art, which is Codex's job, and on Harald's map for context).

**Built — two new Python props, sharing one geometry module so they can't drift apart:**
- `NorseBackpack/Props/Hnefatafl/board_layout.py` — the 14 fixed blocker squares, throne and
  corners, pulled from the exact `blocks` set in this page's own interactive prototype (not
  re-derived by eye). Also the map/ticket split: columns A–E visible, F–G hidden.
- `NorseBackpack/Props/Hnefatafl/build_board_setup_pdf.py` → `output/pdf/Hnefatafl_Board_Setup_Insert.pdf`
  — the map-back panel: grid, throne, corners and the 10 visible blockers, with an irregular stain
  over columns F–G and Liv's margin apology beside it. **Real bug caught and fixed**: the first
  version painted the stain as a translucent overlay, so the hidden blockers showed through as
  darker patches — visually defeating the "hidden" strip entirely. Fixed by never drawing tokens
  in the hidden columns at all, so the stain covers blank paper, not a disguised token.
- `NorseBackpack/Props/Hnefatafl/build_ticket_pdf.py` → `output/pdf/Hnefatafl_Ticket_Print.pdf`
  (+ `_Letter_Print.pdf`) — front: museum branding, a decorative (non-puzzle) mini board icon, and
  the real-rules text. Back: the reconstruction-caveat line plus the mirrored two-column offset
  panel (columns printed G, F — reversed from the map's own F, G order — at the same 0.5in cell
  pitch as the map panel, so the grid lines actually continue when butted together). **Real bug
  caught and fixed**: the first rules draft said "no captures" one line above "the attackers win
  by surrounding him" — a direct self-contradiction, since surrounding *is* a capture in real
  hnefatafl. Rewrote to describe the actual sandwich-capture rule.

### Files changed

- `NorseBackpack/Props/Hnefatafl/board_layout.py` — new.
- `NorseBackpack/Props/Hnefatafl/build_board_setup_pdf.py` — new.
- `NorseBackpack/Props/Hnefatafl/build_ticket_pdf.py` — new.
- `output/pdf/Hnefatafl_Board_Setup_Insert.pdf`, `Hnefatafl_Ticket_Print.pdf`,
  `Hnefatafl_Ticket_Letter_Print.pdf` — new.
- `NorseBackpack/Norse_Brainstorm.html` — `PZ-01`, `PZ-05` (Oslo message + Fun Fact), `PZ-07`
  (reassigned to Harald, both panels marked built), `PZ-09` (hnefatafl job moved off Leif's map
  onto Harald's), `PR-08`, `PR-09`, the codes-reference table row, the puzzle-candidate summary,
  the interactive prototype's caption, the "build" tab's prop-kit list, and the 3D-printer
  inventory line — all updated for the compartment drop, the pamphlet→ticket rename, and the
  Leif→Harald reassignment.

### Checks run

- Ran both build scripts; inspected all three PDF pages (map insert, ticket front, ticket back) at
  300dpi. Caught and fixed the two real bugs above before calling either script done.
- Verified the ticket's mirrored panel against the shared blocker data by hand: G-column blockers
  (G2, G4, G5) land in the left slot, F-column blocker (F2) in the right slot, matching the
  reversed G-then-F column order; corners G1/G7 render as open diamonds in the correct rows.
- HTML tag balance after all edits: 897 `div`, 12 `section`, 63 `figure`, 22 `details`, 23
  `article`, 13 `ul`, 108 `li` — all paired.
- Served over local HTTP (another session's `static-preview` on port 8734, joined directly since
  it serves the same repo checkout) and inspected the Puzzle details tab: heading, rules text and
  prototype caption all show the updated ticket/Harald wording; no console errors.
- Deleted temporary preview PNGs from `output/pdf/` after inspection; the three new production
  PDFs are left in place.

### Next action

Decide whether Codex should start Oslo's front artwork now (independent of the map, like Rouen's
front was built before its map/lock context existed) or wait — either way, Harald's trail map
sheet (`build_trail_maps_pdf.py`) is the real blocker for finishing this puzzle's physical props.

### Blockers / open items

- Harald's trail map sheet does not exist yet — two of his six stops (Sicily, Anatolia) are still
  regional anchors, not named places, which blocks the sheet itself, not just this puzzle.
- `PR-08` (which physical board to buy, 7×7 vs. 9×9/11×11) is still unchecked against real
  listings — now simpler since the compartment requirement is gone, but still unresolved.
- The Oslo postcard's front artwork and print PDF are both unbuilt — this session only wrote the
  message and Fun Fact into `PZ-05`.
- `PR-09`'s print test (does the offset read through the ticket, does the stain hide the original)
  is now buildable/testable since both scripts exist, but no physical print test has been run.

## Session Close — 2026-09-14 — Oslo postcard front

**Task:** create Postcard 13's Oslo front from the user-selected Wikimedia photograph of
Akershus Fortress viewed from the water, matching the approved postcard series.

**Done:** verified Balou46's source and CC BY-SA 4.0 licence, generated a screen-print nighttime
waterfront illustration, normalized it to 1500 × 1050 at 300 dpi, and added the shared
`OSLO / NORWAY` title treatment. The exact prompt, attribution and front-only status are recorded
in the Postcards tab and source register. The back and print PDF were not part of this session.

### Files changed

- `NorseBackpack/Postcards/Postcard_13_Oslo_Front.png` — finished front.
- `NorseBackpack/Postcards/Postcard_13_Oslo_Illustration_v1.png` — print-sized illustration.
- `NorseBackpack/Postcards/References/Postcard_13_Oslo_ImageGen_Source.png` — untouched ImageGen result.
- `NorseBackpack/Postcards/References/Oslo_Akershus_Balou46_Source.jpg` — Wikimedia source.
- `NorseBackpack/Postcards/build_postcard_front_images.py` — Oslo registered in the shared front builder.
- `NorseBackpack/Postcards/References/README.md` — attribution and adaptation notes.
- `NorseBackpack/Norse_Brainstorm.html` — gallery, overview, exact prompt and source summary.

### Checks run

- Inspected the Wikimedia source, generated illustration and titled front at full size.
- Confirmed the final front is 1500 × 1050 at 300 dpi.
- Served the design page over local HTTP and inspected the Oslo overview tile and gallery card in
  the in-app browser. The image loaded at its natural 1500 × 1050 size, the Postcards view was
  active, and the browser console had no warnings or errors. HTML tag counts remain balanced.

### Next action

Decide Postcard 13's message and Fun Fact before building its back and print PDF.

### Blockers / open items

- No front-art blocker remains. The back content and PDF are still unbuilt.

## Session Close — 2026-09-14 — Châlus postcard front

**Task:** create Postcard 04's Châlus front from the user-selected Wikimedia photograph of
Château de Châlus-Chabrol, matching the approved postcard series.

**Done:** verified Fonquebure's source and CC BY-SA 3.0 licence, generated a screen-print castle
illustration, normalized it to 1500 × 1050 at 300 dpi, and added the shared
`CHÂLUS / HAUTE-VIENNE` title treatment. The source photograph's white caption strip was excluded.
The exact prompt, attribution and front-only status are recorded in the Postcards tab and source
register. The back and print PDF were not part of this session.

### Files changed

- `NorseBackpack/Postcards/Postcard_04_Chalus_Front.png` — finished front.
- `NorseBackpack/Postcards/Postcard_04_Chalus_Illustration_v1.png` — print-sized illustration.
- `NorseBackpack/Postcards/References/Postcard_04_Chalus_ImageGen_Source.png` — untouched ImageGen result.
- `NorseBackpack/Postcards/References/Chateau_Chalus_Chabrol_Fonquebure_Source.jpg` — Wikimedia source.
- `NorseBackpack/Postcards/build_postcard_front_images.py` — Châlus registered in the shared front builder.
- `NorseBackpack/Postcards/References/README.md` — attribution and adaptation notes.
- `NorseBackpack/Norse_Brainstorm.html` — gallery, overview, exact prompt and source summary.

### Checks run

- Inspected the Wikimedia source, generated illustration and titled front at full size.
- Confirmed the final front is 1500 × 1050 at 300 dpi.
- Served the design page over local HTTP and inspected the Châlus overview tile and gallery card
  in the in-app browser. The image loaded at its natural 1500 × 1050 size, the Postcards view was
  active, and the browser console had no warnings or errors. HTML tag counts remain balanced.

### Next action

Decide Postcard 04's message and Fun Fact before building its back and print PDF.

### Blockers / open items

- No front-art blocker remains. The back content and PDF are still unbuilt.

## Session Close — 2026-09-14 — Rouen postcard front

**Task:** create Postcard 05's Rouen front from the user-specified Wikimedia Commons photograph
`Rouen Place du Vieux-Marché 05`, matching the approved postcard series.

**Done:** verified Zairon's source photograph and CC BY-SA 4.0 licence, generated a
screen-print-style Old Market Square illustration, normalized it to 1500 × 1050 at 300 dpi, and
added the shared `ROUEN / NORMANDY` title treatment. The prompt, source credit and front-only
status are recorded in the Postcards tab and source register. The back and print PDF are not part
of this session.

### Files changed

- `NorseBackpack/Postcards/Postcard_05_Rouen_Front.png` — finished front.
- `NorseBackpack/Postcards/Postcard_05_Rouen_Illustration_v1.png` — print-sized illustration.
- `NorseBackpack/Postcards/References/Postcard_05_Rouen_ImageGen_Source.png` — untouched ImageGen result.
- `NorseBackpack/Postcards/References/Rouen_Place_du_Vieux_Marche_Source.{jpg,png}` — Wikimedia source and compatibility copy.
- `NorseBackpack/Postcards/build_postcard_front_images.py` — Rouen registered in the shared front builder.
- `NorseBackpack/Postcards/References/README.md` — attribution and adaptation notes.
- `NorseBackpack/Norse_Brainstorm.html` — gallery, overview, exact prompt and source summary.

### Checks run

- Inspected the Wikimedia source, generated illustration and titled front at full size.
- Confirmed the final front is 1500 × 1050 at 300 dpi.
- Served the design page over local HTTP and inspected the Rouen overview tile and gallery card in
  the in-app browser. The image loaded at its natural 1500 × 1050 size, the Postcards view was
  active, and the browser console had no warnings or errors. HTML tag counts remain balanced.

### Next action

Build `build_postcard_05_pdf.py` from the already-decided Rouen message, Fun Fact and word-lock
order clue, then render the back and print PDF.

### Blockers / open items

- No front-art blocker remains. The back, postmark treatment and PDF still need building.

## Session Close — 2026-09-14 — Château de Robert le Diable line icon

**Task:** create a simple black architectural line icon from the user-specified Wikimedia Commons
photograph `2014-Chateau-Robert-LeDiable.jpg`, with a transparent background.

**Done:** downloaded W. Mechelke's 3008 × 2000 original (CC BY-SA 3.0), verified the attribution
and licence on Commons, and used it as the sole structural reference. The accepted drawing keeps
the left round crenellated tower, broken central wall, receding curtain wall, major openings and
the source photograph's cropped right tower while omitting foliage, ground, railings and stone
texture. The first generation baked in a checkerboard; a second ImageGen background-extraction
pass produced genuine alpha. A reproducible cleanup normalizes the final 1536 × 1024, 300 dpi PNG
to exact black over transparency. The icon is not yet placed on Map 2.

### Files changed

- `NorseBackpack/TravelMap/Art/Rollo_Chateau_Robert_Le_Diable_Line_v1.png` — production icon.
- `NorseBackpack/TravelMap/Art/Sources/Chateau_Robert_Le_Diable_WMechelke_Source.jpg` — original
  Wikimedia photograph.
- `NorseBackpack/TravelMap/Art/Sources/Rollo_Chateau_Robert_Le_Diable_Line_v1_ImageGen_Source.png`
  — accepted transparent ImageGen render.
- `NorseBackpack/TravelMap/prepare_chateau_line_icon.py` — reproducible alpha/RGB/canvas cleanup.
- `NorseBackpack/Norse_Brainstorm.html` — gallery, source attribution, CC BY-SA note and exact
  two-stage ImageGen prompts added to the Design guide.

### Checks run

- Inspected the source photo, accepted render and normalized icon.
- Verified production output is 1536 × 1024 RGBA at 300 dpi, alpha extrema 0–255, with only
  `(0, 0, 0)` in visible RGB pixels.
- Served the design page over local HTTP and inspected the icon, caption and source/licence block
  in the in-app browser. The image loaded at its natural 1536 × 1024 size and the browser console
  has no warnings or errors. HTML tag counts remain balanced.

### Next action

User reviews the icon. If approved, decide its exact Map 2 size and location before editing the
map builder; placement must avoid labels and the final drawn-route corridor.

### Blockers / open items

- No technical blocker. Map placement was not requested and remains open.

## Session Close — 2026-09-14 — Six additional Map 2 word icons

**Task:** generate one Rollo/Map 2 icon for each paired English-word concept: Combat/Fight,
Beef/Cow, Forest/Woodland, Poultry/Hen, People/Folk and Tavern/Inn. The pairs are synonyms from
different origins, so the deliverable is six icons, not twelve.

**Done:** generated crossed sword/axe, cow, three-tree woodland, hen, three ordinary townspeople
and timber inn/tankard-sign subjects using the existing Rollo map art as style references. Forest,
folk and inn initially contained baked transparency checkerboards; corrected those with a second
ImageGen background-extraction pass. Ran all six through the existing normalization script so
each production asset is a 1024 × 1024 transparent PNG at 300 dpi with every visible RGB pixel
exactly `#A2562D`. Icons are built but not placed on Map 2.

### Files changed

- `NorseBackpack/TravelMap/Art/Rollo_{Combat,Cow,Forest,Hen,Folk,Inn}_v1.png` — six production
  icons.
- `NorseBackpack/TravelMap/Art/Sources/Rollo_{Combat,Cow,Forest,Hen,Folk,Inn}_v1_ImageGen_Source.png`
  — accepted raw or transparency-corrected renders.
- `NorseBackpack/TravelMap/normalize_rollo_vignettes.py` — six new assets added to the reproducible
  normalization list.
- `NorseBackpack/Norse_Brainstorm.html` — six-icon gallery, status and exact generation/correction
  prompts added to the Design guide.

### Checks run

- Inspected all six source renders and all six normalized assets.
- Verified every production file is 1024 × 1024 RGBA with alpha extrema 0–255 and only
  `(162, 86, 45)` in visible RGB pixels.
- Rendered the set at approximately 0.43 in / 300 dpi on the map's cream colour; all six concepts
  remain recognizable.
- Served the design page over local HTTP and inspected the six-icon gallery in the in-app browser;
  all six images loaded at their natural 1024 × 1024 size, the 3 × 2 layout is clean, and the
  browser console has no warnings or errors. HTML tag counts remain balanced.

### Next action

User reviews the six icons. If approved, decide their actual Map 2 locations before changing the
map builder; placement must respect stop labels and the final drawn-route corridor.

### Blockers / open items

- No technical blocker. Map placement was not requested and remains open.

## Session Close — 2026-09-14 — Battle postcard front artwork

**Task:** continue the postcard image set with the Battle/Hastings stop, using the user-specified
Wikimedia Commons photograph of the wooden archer sculpture at the battlefield and the same
screen-print travel-poster style as the approved fronts.

**Done:** downloaded Richard Cooke's exact Commons source and verified its CC BY-SA 2.0 licence.
Used it as the scene reference alongside four finished postcard illustrations as style/layout
references. The first ImageGen render was accepted: it keeps the carved kneeling archer clearly
wooden, the drawn longbow, open field, tree line, distant Battle Abbey and broad summer sky, with
no reenactment or invented figures. Normalized the 1499 × 1049 render to the exact PC-13 1500 ×
1050 size at 300 dpi, then used the shared builder to add `BATTLE / EAST SUSSEX`. Card 08 is
front-only; its message, Fun Fact, assigned tree/teacup rebus, back and print PDF remain unwritten.

### Files changed

- `NorseBackpack/Postcards/Postcard_08_Battle_Illustration_v1.png` — print-sized illustration.
- `NorseBackpack/Postcards/Postcard_08_Battle_Front.png` — titled postcard front.
- `NorseBackpack/Postcards/References/Battle_Hastings_Sculpture_Source.jpg` — exact source.
- `NorseBackpack/Postcards/References/Postcard_08_Battle_ImageGen_Source.png` — raw render.
- `NorseBackpack/Postcards/References/README.md` — source, licence and adaptation notes.
- `NorseBackpack/Postcards/build_postcard_front_images.py` — Battle added to the shared list.
- `NorseBackpack/Norse_Brainstorm.html` — Rollo overview thumbnail, front-only gallery entry,
  source note and exact production prompt.

### Checks run

- Inspected the photograph, normalized illustration and titled front at full size.
- Confirmed both production PNGs are 1500 × 1050; the illustration records 300 dpi.
- HTML tag balance: 827 `div`, 11 `section`, 47 `figure`, 17 `details` and 19 `article` elements,
  all paired.
- Served over local HTTP and checked the Postcards tab: overview thumbnail and gallery image load
  at natural size 1500 × 1050; the new front lays out cleanly; no browser warnings or errors.

### Next action

Create the next user-selected front. Build Battle's back only after its message and Fun Fact are
approved; the tree/teacup rebus placement is already assigned by `PZ-14`.

### Blockers / open items

- No technical blocker. Battle is not fully built, so the Rollo count remains 1 of 6 and the
  overview correctly shows its artwork without a completion checkmark.

## Session Close — 2026-09-14 — Winchester postcard front artwork

**Task:** continue the postcard image set with Winchester, using the user-specified Wikimedia
Commons photograph of Winchester Cathedral and the same screen-print travel-poster style as the
approved fronts.

**Done:** downloaded Graham Horn's exact Commons source and verified its CC BY-SA 2.0 licence.
Used it as the scene reference alongside cards 01–03 and Bayeux as style/layout references. The
first ImageGen render was accepted: it retains the elevated winter view, long cathedral nave,
square central tower, west front, layered roofs and snow-dusted ridge in the set's flat,
lightly-distressed palette. Normalized the 1499 × 1049 render to the exact PC-13 1500 × 1050 size
at 300 dpi, then used the shared front builder to add `WINCHESTER / ENGLAND`. Card 07 is front-only;
its message, Fun Fact, assigned cross/bow/lightning rebus, back and print PDF remain unwritten.

### Files changed

- `NorseBackpack/Postcards/Postcard_07_Winchester_Illustration_v1.png` — print-sized illustration.
- `NorseBackpack/Postcards/Postcard_07_Winchester_Front.png` — titled postcard front.
- `NorseBackpack/Postcards/References/Winchester_Cathedral_Graham_Horn_Source.jpg` — exact source.
- `NorseBackpack/Postcards/References/Postcard_07_Winchester_ImageGen_Source.png` — raw render.
- `NorseBackpack/Postcards/References/README.md` — source, licence and adaptation notes.
- `NorseBackpack/Postcards/build_postcard_front_images.py` — Winchester added to the shared list.
- `NorseBackpack/Norse_Brainstorm.html` — Rollo overview thumbnail, front-only gallery entry,
  source note and exact production prompt.

### Checks run

- Inspected the photograph, normalized illustration and titled front at full size.
- Confirmed both production PNGs are 1500 × 1050; the illustration records 300 dpi.
- HTML tag balance: 824 `div`, 11 `section`, 46 `figure`, 16 `details` and 18 `article` elements,
  all paired.
- Served over local HTTP and checked the Postcards tab: the overview thumbnail and gallery image
  load at natural size 1500 × 1050; the new front lays out cleanly; no browser warnings or errors.

### Next action

Create the next user-selected front. Build Winchester's back only after its message and Fun Fact
are approved; the cross/bow/lightning rebus placement is already assigned by `PZ-14`.

### Blockers / open items

- No technical blocker. Winchester is not a fully built card, so the Rollo count remains 1 of 6
  and the overview correctly shows its artwork without a completion checkmark.

## Session Close — 2026-09-14 — Bayeux postcard front artwork

**Task:** continue the postcard image set with Bayeux, using the user-specified Wikimedia Commons
photograph of Bayeux Tapestry Scene 57 and the same screen-print travel-poster style as cards
01–03.

**Done:** downloaded the exact Commons source, verified its CC0/public-domain status, and used it
as the scene reference alongside the three finished postcard illustrations as style/layout
references. The first ImageGen render was accepted without a second generation: it preserves the
standing soldier, arrow-struck shield bearer, mounted figure, fallen warrior, inscription and
animal borders in a limited-palette screen-print treatment. Normalized the 1499 × 1049 render to
the exact PC-13 1500 × 1050 size at 300 dpi, then used the shared postcard-front builder to add
`BAYEUX / NORMANDY` in the established title band. Card 06 is front-only; its message, Fun Fact,
imprint, back and print PDF remain unwritten. The generated Latin inscription is decorative and
close to the source, but is not a letter-perfect scholarly transcription.

### Files changed

- `NorseBackpack/Postcards/Postcard_06_Bayeux_Illustration_v1.png` — print-sized illustration.
- `NorseBackpack/Postcards/Postcard_06_Bayeux_Front.png` — titled postcard front.
- `NorseBackpack/Postcards/References/Bayeux_Tapestry_scene57_Harold_death_Source.jpg` — exact
  user-specified source image.
- `NorseBackpack/Postcards/References/Postcard_06_Bayeux_ImageGen_Source.png` — untouched render.
- `NorseBackpack/Postcards/References/README.md` — source, licence and adaptation notes.
- `NorseBackpack/Postcards/build_postcard_front_images.py` — Bayeux added to the shared front list.
- `NorseBackpack/Norse_Brainstorm.html` — Rollo overview thumbnail, front-only gallery entry,
  source note and exact production prompt.

### Checks run

- Inspected the source, normalized illustration and titled front at full size.
- Confirmed both production PNGs are 1500 × 1050; the illustration records 300 dpi.
- Confirmed Bayeux uses the same shared typography routine as cards 01–03 and the title sits fully
  inside the blank navy band.
- HTML tag balance remained valid: 821 `div`, 11 `section`, 44 `figure`, 15 `details` and 17
  `article` elements, all paired. Served over local HTTP and checked the Postcards tab: the Bayeux
  overview thumbnail and full gallery image both load at natural size 1500 × 1050, the new entry
  lays out cleanly, the correct view is active, and the browser console has no warnings or errors.

### Next action

Create the next user-selected postcard front. Bayeux's back should wait until its message and Fun
Fact are approved (`PZ-05`), since this session was image-only.

### Blockers / open items

- No technical blocker. Bayeux is not a complete card yet, so it remains excluded from the
  “fully built” count and has no checkmark in the overview.

## Session Close — 2026-09-14 — Norse hint page copied into the live escape-backpack-games repo

**Task:** follow-up to the prior session's `NorseBackpack/norse-hints.html` (built in this repo,
matching the Hiking Backpack's live hint-companion format). The user asked to copy it into the
actual `escape-backpack-games` repo so it goes live at the real URL.

**Done:** that repo (`OttawaVisuals/escape-backpack-games`, public, flat file structure —
`index.html`, `styles.css`, `assets/`, `hiking-hints.html`, etc. at root) wasn't cloned anywhere on
this machine, so this session cloned it fresh to `C:\EscapeBackpack\escape-backpack-games` (a
sibling of this repo, outside it — not tracked here). Confirmed the repo's own `styles.css` and
`assets/logo.png` are the canonical originals (this repo's copies in `NorseBackpack/` were just a
local preview copy, byte-for-byte the same content), so only `norse-hints.html` itself was copied
in — no need to touch the shared assets. Asked and confirmed two scope questions before pushing:
(1) don't add Norse to `index.html`'s backpack grid or any other page's nav dropdown yet — only 5 of
9 planned puzzle stations are real, so site-wide discoverability is a separate decision for later;
(2) commit and push now rather than leaving it staged. Committed and pushed straight to `main`
(`4fc3519`); GitHub Pages rebuilt within about a minute.

**Live now:** https://ottawavisuals.github.io/escape-backpack-games/norse-hints.html — verified with
no console errors, using the repo's real `styles.css`/logo (not the local preview copies).

### Files changed

- `C:\EscapeBackpack\escape-backpack-games\norse-hints.html` — new, pushed to `main`. **This path is
  outside this repo** — nothing here tracks it; future sessions working on the public hint page need
  to go to that clone (or re-clone it) rather than editing `NorseBackpack/norse-hints.html` and
  expecting it to be the live copy anymore. Keep both in sync by hand until/unless a better workflow
  is set up.
- No changes in this repo this session beyond this handoff entry.

### Checks run

- Diffed the local `NorseBackpack/styles.css`/`assets/logo.png` against the escape-backpack-games
  repo's own copies — content-identical (one added comment line in the CSS, negligible size
  difference in the PNG from a base64 round-trip); used the repo's canonical files rather than
  overwriting them.
- Served the copied file locally against the repo's real assets (temporary `python -m http.server
  8735` in the clone) before pushing: loaded clean, no console errors.
- After pushing, polled the live GitHub Pages URL until it returned 200, then loaded it in the
  browser: correct title, no console errors, matches the pre-push local check.

### Next action

Decide whether/when to make Norse discoverable site-wide (homepage card + nav dropdown on every
other page) — deliberately not done this session. Also decide how the two copies of
`norse-hints.html` (this repo's `NorseBackpack/` original and the pushed one in the separate clone)
should be kept in sync going forward, since they are two different files on disk now.

### Blockers / open items

- `C:\EscapeBackpack\escape-backpack-games` is a separate git repo/clone, not a submodule or
  otherwise linked from this repo — a future session needs to know it exists and where, since
  nothing in this repo's structure points to it.
- Same 4 illustrative-only Norse puzzles (rune relic, family connection, king's escape, saga in
  pieces) and station 3's unwritten in-fiction hint text remain open from the prior session.

## Session Close — 2026-09-14 — Postcards tab: new "All 18, by trail" overview

**Task:** the user asked for a visual overview on the Postcards tab: all four trails with their
colours, one small box per postcard showing the front art (where built), a checkmark on completed
cards, and a highlight on specific postcards. The highlight criterion went through two rounds —
first proposed as "the last stop of each trail" (guessed, per the user's phrasing "to stay out"),
then corrected once the user clarified they meant the cards decided in `PZ-11` to be held back
until the final container, so the map/deck doesn't leak a digit early. Searched
`Norse_Brainstorm.html` for that decision rather than relying on memory, since `PZ-11` isn't
something recorded in Claude Code's cross-session memory.

**Built:** a new "All 18, by trail" block in the Postcards tab, above the existing card gallery.
Four `trail-group`s (Leif `#216580`, Rollo `#a2562d`, Aud `#6d528b`, Harald `#467444`, matching the
stamp-series colours already decided), each showing its real route stops from
`TravelMap/Norse_Aunt_Route_Plan.json`'s `visits` block in order (3+6+3+6 = 18, confirmed against
that file). Built cards (01, 02, 03 — all Leif's) show their real front art with a checkmark badge;
unbuilt stops show a dashed, trail-tinted placeholder box with just the stop name. A rust "Held
back" banner marks the three `PZ-11` cards: **Rollo — Roumare forest** (stop 6), **Aud — Hvammur**
(stop 2), **Harald — Staraya Ladoga** (stop 2, labelled "Held back?" since `PZ-11` itself calls that
one provisional pending Harald's map sheet). Leif's trail carries no held-back badge — `PZ-11`
explicitly excludes it as the deliberate "teaching trail." A legend at the bottom of the block spells
out all three states and links back to `PZ-11`.

### Files changed

- `NorseBackpack/Norse_Brainstorm.html` — new `.trail-overview`/`.pc-box`/`.pc-held` CSS block; new
  "All 18, by trail" markup in the `#postcards` section, with a full pass correcting it from a
  first (wrong) "final leg of trail" framing to the actual `PZ-11` held-back set.

### Checks run

- Served over local HTTP (`static-preview`, port 8734): no console errors. Verified via a
  cache-busted reload (`?cb=2`, same known caching quirk as prior sessions — the shared server
  returns a stale response on a plain re-navigate to an already-visited URL) that all three
  "Held back" badges landed on the correct boxes (Roumare forest, Hvammur, Staraya Ladoga) and that
  Leif's cards carry only the checkmark, no held-back badge.
- Cross-checked the 18-stop count and per-trail split (3/6/3/6) against
  `TravelMap/Norse_Aunt_Route_Plan.json` directly rather than assuming.

### Next action

Nothing queued specifically from this session. If continuing on postcards, cards 04–18 (Rollo, Aud,
Harald) are still entirely unwritten — same backlog as before (`PC-07`/`PZ-05`).

### Blockers / open items

- Harald's held-back card (Staraya Ladoga) is provisional per `PZ-11` itself — re-test once Harald's
  real map sheet exists (`build_trail_maps_pdf.py` currently has no Harald sheet; two of his stops
  are still regions, not named places).
- All the pre-existing blockers below (postmark dates, Hnefatafl placement, 15 unbuilt cards, etc.)
  are unchanged by this session.

## Session Close — 2026-09-14 — Five Bayeux-style postcard margin symbols

**Task:** create a Roman numeral I, an arrow/2 hybrid, a face-on die showing five, a separate plain
right-pointing arrow meaning “to,” and a fish-scale patch meaning “scale,” matching Aunt Liv's
existing multicolour Bayeux-style postcard drawings.

**Done:** generated all five with the built-in ImageGen workflow using
`Postcards/RebusIcons/Sources/Bayeux_Reference_Crop.png` as a style/palette reference. The first
three source renders baked a fake transparency checkerboard into RGB; the plain arrow arrived with
genuine alpha, as did the fish-scale patch. `prepare_bayeux_margin_symbols.py` handles both source types, removes isolated grid
fragments where needed, recentres the artwork and writes genuine 1024 × 1024 RGBA PNGs at 300 dpi.
Updated `PC-15` from five to ten unassigned margin drawings and added the new gallery and exact
prompts to the Design guide. No postcard builder or card-to-symbol assignment was changed.

### Files changed

- `NorseBackpack/Postcards/RebusIcons/Rebus_{Roman_I,Arrow_2,Die_5,Arrow_To,Fish_Scales}_Bayeux_v1.png` — production
  assets.
- `NorseBackpack/Postcards/RebusIcons/Sources/Rebus_{Roman_I,Arrow_2,Die_5,Arrow_To,Fish_Scales}_Bayeux_v1_ImageGen_Source.png`
  — untouched ImageGen renders.
- `NorseBackpack/Postcards/RebusIcons/prepare_bayeux_margin_symbols.py` — reproducible alpha cleanup.
- `NorseBackpack/Postcards/RebusIcons/Bayeux_Margin_Symbols_v1_PrintScale_Preview.png` — 0.45 in
  proof at 300 dpi on the project cream ground.
- `NorseBackpack/Norse_Brainstorm.html` — `PC-15`, gallery, production notes and exact prompts.

### Checks run

- Full-size visual inspection: exactly one I, one right-pointing arrow/2 hybrid, one flat die with
  exactly five pips, one separate straight right-pointing arrow and one seven-scale patch; no extra
  objects or competing meanings of “scale.”
- Pixel checks: each production asset is 1024 × 1024 RGBA at 300 dpi, alpha spans 0–255, has one
  connected visible component and does not touch the canvas edge.
- 0.45 in / 135 px proof inspected: all five remain distinct and readable.
- Served the HTML over local HTTP and inspected the Design guide: all eight gallery images render,
  the new row fits cleanly, and the prompt disclosure is present. HTML tag counts remain balanced.

### Next action

Decide the card-to-symbol mapping and reading order for `PC-15`, then place the selected symbols in
the relevant postcard builders at 0.4–0.5 in and rebuild those PDFs.

### Blockers / open items

- `PC-15` remains open by design; no target postcards were specified.

## Session Close — 2026-09-13 (later still) — Norse public hint-companion page, v1 (5 real stations)

**Task:** start a public player-facing hint page for the Norse Backpack, matching the format of the
live Hiking Backpack hint companion the user pointed to
(`https://ottawavisuals.github.io/escape-backpack-games/hiking-hints.html`). That site is a
**separate GitHub repo** (`ottawavisuals.github.io/escape-backpack-games`), not this one — this
session read its rendered structure and the shared `styles.css`/`assets/logo.png` from the live
site (plus a local reference copy of its full HTML the user provided at
`NorseBackpack/Source_Info/hiking-hints.html`) to reproduce the format here, but did not get push
access to that other repo.

**Format reproduced exactly:** single self-contained HTML file, team-name entry → timer →
station grid → progressive per-station hint modal (Hint #1/#2/#3/Solution, expand-one-at-a-time) →
completion screen, with localStorage session persistence and an optional fire-and-forget Google
Apps Script logger (same shared nav/palette as the live site: forest green + brass + rust, Young
Serif/Inter Tight/JetBrains Mono).

**Content scope — asked and answered before writing anything:** the user chose "5 real stations
only" over including all of Norse's puzzle set. Cross-checked every entry in `Norse_Brainstorm.html`'s
`puzzles` array first and found four of them (`the rune-labelled relic`, `the family connection`,
`the king's unfinished escape`, `the saga in pieces`) explicitly carry **illustrative, not-real**
codes (the array literally says "Values illustrative" against 582/427/2468/231) — publishing those
as if they were real answers would hand players a wrong solution, so they are deliberately left off
this page entirely rather than shown as placeholders. The 5 stations that do appear use only
puzzle-array content that is real:

1. The Opening Puzzle → `1021`
2. The Beasts on the Chart → `3212` (BEAR)
3. The Joined Top Edge → `1576` (real code; the source array's hint text is literally
   `['Not written yet.']` for this one, so hint #1 here states plainly that no in-fiction nudge
   exists yet and just gives the decided physical mechanism instead of inventing flavour text)
4. The Route Hidden in Plain Sight (final) → `1972`
5. See You in Norway (ending, no code)

No invented time estimates or benchmark numbers: the Hiking page's completion screen compares your
time to a benchmark best/average, but Norse has never been playtested, so those numbers would be
fabricated. The Norse completion screen instead shows only your own time plus a note that no
benchmark exists yet. `LOGGER_URL` is left empty (not a fake endpoint) — the existing `logAsync()`
guard already no-ops safely when it's blank, exactly like the Hiking page's own guard against
placeholder URLs.

### Files changed

- `NorseBackpack/norse-hints.html` — new. The public hint-companion page.
- `NorseBackpack/styles.css` — new. Copy of the live site's shared stylesheet, so the page renders
  correctly both here and if later dropped into the `escape-backpack-games` repo.
- `NorseBackpack/assets/logo.png` — new. Copy of the live site's nav brand-mark image.

### Checks run

- Served over local HTTP (`static-preview`, port 8734): no console errors on
  `NorseBackpack/norse-hints.html`.
- Walked the flow live: entered a team name, started the timer, opened hint panels for stations 3
  (2 hint levels) and 5 (1 hint level) and confirmed only the real number of levels renders (no
  phantom "Solution" label when fewer than 4 entries exist) — the hint-count logic scales correctly
  per station.
- Confirmed the nav "Hints" dropdown lists both Hiking and Norse as Live with correct relative
  links, matching the live site's pattern.
- Did not fully exercise the Done→complete-screen confirm flow interactively (a click-coordinate
  mismatch after a viewport resize got in the way, not a code issue) — that logic is unmodified from
  the Hiking page's already-proven implementation, so it was not re-verified line-by-line.

### Next action

Decide whether/how to port this file into the actual `escape-backpack-games` repo (this session has
no access to it) — or keep developing it here until Norse's remaining puzzle stations are decided,
then add them as real stations rather than placeholders.

### Blockers / open items

- No access to the `escape-backpack-games` repo, so this page cannot go live at the same URL as the
  Hiking page without a manual copy-over by the user (or granting access in a future session).
- The 4 illustrative-only puzzles (rune relic, family connection, king's escape, saga in pieces)
  still need real decided answers before they can be added to this page.
- Station 3's hint ladder still has no real in-fiction hint text (`PZ-05` backlog) — only the
  mechanism and solution are written.

## Session Close — 2026-09-13 (later) — Fixed a real stop dropped from Rollo's map; brainstormed the Châlus/Saint-Clair-sur-Epte rebus lock

**Task:** review Codex's newly-built Rollo map icons (previous session below), then design the next
lock mechanism (2+ cards, per the user's request for locks needing more than one card) around a
Bayeux-Tapestry-style rebus.

**Rebus lock designed (not yet written into `Norse_Brainstorm.html` as a `PZ-` entry):** two
postcard rebuses — cross+bow+lightning → CROSSBOW BOLT (Châlus) and tree+teacup → TREATY
(Saint-Clair-sur-Epte) — point players to the matching full icon on Rollo's map; the distance
between those two icons, read with the architect's scale ruler already on hand, is the lock input.
5 postcard rebus icons (cross, bow, lightning, tree, teacup) were generated by Codex in tapestry
style (`NorseBackpack/Postcards/RebusIcons/`, v2/Bayeux palette kept, v1 flat-icon version rejected
as not tapestry-like enough) and a scratch placement mockup was rendered to check legibility on an
actual card back (scratchpad only, not committed — placeholder message text, Rollo's real card copy
is still unwritten per `PZ-05`).

**Real bug found and fixed while inspecting Codex's Rollo map build:** `Trail_Map_2_Rollo_Print.pdf`
was silently dropping the label for **Roumare forest** — one of the six real route stops needed to
draw Rollo's final digit-9 shape — to a label-collision with the newly-added icon boxes. This was
already present in Codex's build before this session touched anything (confirmed by reverting the
file and reproducing it); the console output has always reported dropped labels via a
`STOPS NOT LABELLED ON SHEET` line, but nobody had checked it since the icons were added. Also
opportunistically confirmed neither `Saint-Clair-sur-Epte` nor `Roumare forest` printed on the map
before the fix (contradicts `PZ-09`'s claim that Saint-Clair-sur-Epte is "already labelled" — that
claim is stale and should be corrected next time `PZ-09` is touched).

**Fix:** nudged the treaty-scroll and ducal-coronet icon boxes in `ROLLO_ART`
(`build_trail_maps_pdf.py`) by a small offset found via a brute-force search over nearby positions,
checking the script's own `missing + collided` return value after each try rather than guessing.
The result is zero real stops dropped (only decorative corpus towns — Caen, Hastings, Lewes, etc. —
are dropped, same as before the icons existed). The coronet still isn't perfectly centred on the
Rouen dot — every tighter position tried reopened the Roumare collision — so it reads as "near
Rouen" rather than sitting exactly on it. A cleaner fix would need Codex to re-flow more of the
cluster (Rouen, Roumare, Saint-Clair-sur-Epte, Bayeux icons all sit within ~50pt of each other), not
just a two-box nudge.

### Files changed

- `NorseBackpack/TravelMap/build_trail_maps_pdf.py` — `ROLLO_ART` treaty-scroll and ducal-coronet
  box positions.
- `output/pdf/Trail_Map_2_Rollo_{Print,ANSWER}.pdf` — rebuilt with the fix.
- `NorseBackpack/Postcards/RebusIcons/` (Codex, this session) — 5 rebus icons, v1 and v2, plus
  ImageGen source renders.
- `NorseBackpack/TravelMap/Art/Rollo_*_v1.png` (Codex, this session) — 7 map icons; see Codex's
  session entry below for the generation details.

### Checks run

- Reproduced the pre-existing label-collision bug by reverting the file and rebuilding; confirmed
  it predates this session's edits.
- Ran `build_trail_maps_pdf.py rollo` after the fix: console reports zero real stops in
  `STOPS NOT LABELLED ON SHEET` (that line no longer appears at all).
- Visually inspected the fixed region at 600 dpi: Rouen, Roumare forest and Saint-Clair-sur-Epte all
  print clearly; crossbow bolt (Châlus) and needle-and-thread (Bayeux) were already correctly
  anchored and untouched.
- Rendered the 5 rebus icons (v1 and v2) at print scale; v2 (Bayeux palette) confirmed legible and
  kept, v1 rejected.
- Did not re-run the full HTML QA pass (no `Norse_Brainstorm.html` changes yet — the rebus lock is
  not written up as a `PZ-` entry, see below).

### Next action

Write the crossbow-bolt/treaty rebus lock up as a new `PZ-` entry in `Norse_Brainstorm.html` (design
is agreed in chat but not yet recorded on the page, per `AGENTS.md`'s "Where Design State Lives"
rule), and correct `PZ-09`'s stale claim that Saint-Clair-sur-Epte was already labelled.

### Blockers / open items

- Rollo's card message content is still unwritten (`PZ-05`) — the placement mockup used placeholder
  text only.
- The coronet-vs-Rouen-dot centring is a minor cosmetic gap, not a functional one; leaving it unless
  Codex does a fuller layout pass.
- The user separately raised a possible third rebus (fish = "scale," combined with a ratio number
  from the architect's ruler's marked scales) as a further clue layer on the same lock — still being
  brainstormed, not designed.

## Session Close — 2026-09-13 — Rollo map vignettes

**Task:** add the supplied seven rust-brown story icons to the second printable Norse trail map,
matching the decorative treatment already used on Leif's first map.

**Done:** generated a crossbow bolt, treaty scroll, ducal coronet, needle and thread, royal crown,
longship and boar with the built-in ImageGen tool. The untouched source renders are retained. A
reproducible normalization pass removes ImageGen's low-alpha glow, fits each subject to a consistent
1024 px square canvas, adds 300 dpi metadata and sets every visible pixel to exact `#A2562D` while
preserving transparency. Added all seven to Rollo's print and answer maps at 0.55–0.7 in visible
size, beneath labels and outside the solved route's 26 pt keep-clear corridor. The crown stays on
England and the longship at sea. Exact prompts and the full icon gallery are recorded in the Design
guide; the Travel routes gallery now describes the illustrated Rollo sheet.

### Files changed

- `NorseBackpack/TravelMap/Art/Rollo_*_v1.png` — seven normalized production icons.
- `NorseBackpack/TravelMap/Art/Sources/Rollo_*_v1_ImageGen_Source.png` — seven untouched renders.
- `NorseBackpack/TravelMap/normalize_rollo_vignettes.py` — reproducible cleanup step.
- `NorseBackpack/TravelMap/build_trail_maps_pdf.py` — Rollo placement table and compositing.
- `output/pdf/Trail_Map_2_Rollo_{Print,ANSWER}.pdf` — rebuilt map and designer answer key.
- `NorseBackpack/Norse_Brainstorm.html` — PR-11 state, gallery and exact prompts.
- `HANDOFF.md` — this session record.

### Checks run

- Visually inspected all seven normalized icons together; each subject is recognizable and the
  coronet/closed crown remain distinct.
- Verified all seven production PNGs are 1024 × 1024, 300 dpi, RGBA, alpha 0–255, and use only
  RGB `(162, 86, 45)` / `#A2562D` in visible pixels.
- Rebuilt and visually inspected both one-page US Letter PDFs. Labels remain readable, the longship
  is at sea, the crown is on England, and the answer route does not cross any vignette.
- Served `Norse_Brainstorm.html` over local HTTP. The Travel routes and Design guide entries render,
  all nine Rollo image references load at 1024 × 1024, and the browser reports no console errors.
- Python compile checks and targeted `git diff --check` passed.

### Next action

Print Rollo's map at true size and confirm all seven icons remain recognizable through the intended
lamination and reduced-opacity treatment.

### Blockers / open items

- No implementation blocker. The true-size physical print check remains outstanding.

## Session Close — 2026-09-13 — Aunt Liv's multicolour Bayeux rebus drawings

**Task:** revise the five postcard rebus icons so they read as drawings by Aunt Liv and use the
style and colours of the supplied Bayeux Tapestry reference, rather than the earlier single rust
colour.

**Done:** created a v2 set for cross, horizontal recurve bow, lightning bolt, flattened tree and
teacup. The new drawings use irregular blue-black outlines and restrained terracotta, ochre and
sage-blue fills sampled visually from the reference. They remain compact transparent assets rather
than photographed embroidery. The original one-colour files are retained as v1. Added `PC-15`
because the repo still does not say which postcard carries which symbol or what the rebus order is;
no postcard builder was changed without that mapping.

### Files changed

- `NorseBackpack/Postcards/RebusIcons/Rebus_*_Bayeux_v2.png` — five revised 1024 px assets.
- `NorseBackpack/Postcards/RebusIcons/Rebus_Icons_Bayeux_v2_{Preview,PrintScale_Preview}.png` —
  full-size and true 0.5 in review sheets.
- `NorseBackpack/Postcards/RebusIcons/Sources/*_Bayeux_v2_ImageGen_Source.png` — raw renders.
- `NorseBackpack/Postcards/RebusIcons/Sources/Bayeux_Reference_Crop.png` — lightweight reference crop.
- `NorseBackpack/Norse_Brainstorm.html` — v2 gallery, exact prompts, attribution and `PC-15`.
- `HANDOFF.md` — this session record.

### Checks run

- Visually inspected both five-up previews on the project cream ground; the set reads consistently
  and all five silhouettes remain clear at 0.5 in / 150 px at 300 dpi.
- Verified all five production PNGs are 1024 × 1024, 300 dpi, RGBA, with alpha spanning 0–255.
- Served the design page over local HTTP: the five v2 images render in the gallery, `PC-15` appears
  in Open questions, and the page reports no browser console errors.

### Next action

Decide the card-to-symbol mapping and reading order for `PC-15`, then place the drawings at a true
0.4–0.5 in print size in the relevant postcard builders and rebuild those PDFs.

### Blockers / open items

- `PC-15`: target postcards and rebus order are not recorded.

## Session Close — 2026-09-13 — Bayeux-style postcard rebus icons

**Task:** generate five tiny transparent rebus icons for a printable postcard: cross, bow,
lightning bolt, tree and teacup.

**Done:** created five 1024 × 1024 transparent PNGs at 300 dpi. Each uses only exact rust-brown
`#A2562D` in visible pixels. The silhouettes are intentionally simple at 0.4–0.5 in print size:
plain Latin cross, horizontal strung recurve bow, single jagged bolt, flattened medieval tree and
plain handled teacup on a saucer. ImageGen repeatedly introduced literal yarn texture or tonal glow,
so the accepted flat alpha masks were normalized mechanically to one ink colour on consistent square
canvases. The accepted source renders and exact production prompts are retained.

### Files changed

- `NorseBackpack/Postcards/RebusIcons/Rebus_{Cross,Bow,Lightning,Tree,Teacup}.png` — final icons.
- `NorseBackpack/Postcards/RebusIcons/Rebus_Icons_Preview.png` — cream-background review sheet.
- `NorseBackpack/Postcards/RebusIcons/Sources/*_ImageGen_Source.png` — accepted source renders.
- `NorseBackpack/Norse_Brainstorm.html` — preview gallery, production notes and exact prompts.
- `HANDOFF.md` — this session record.

### Checks run

- Inspected the five-icon montage on the project cream background: all silhouettes read clearly.
- Verified every final file is 1024 × 1024, carries 300 dpi metadata, has alpha from 0–255, and
  every visible pixel is exactly RGB `(162, 86, 45)` / `#A2562D`.
- Served the design page over local HTTP: all five gallery images load at their natural 1024 ×
  1024 dimensions and the page reports no console errors.

### Next action

Place the five icons at their intended 0.4–0.5 in size on the target postcard layout and run a
true-size print test.

### Blockers / open items

- The target postcard and exact rebus arrangement were not provided in this session, so the icons
  are not yet placed into a card build.

## Session Close — 2026-09-13 (actually final for today) — Card 03 built; card 01's imprint bug caught and fixed; all three of Leif's cards complete

**Task:** draft and build card 03's message (Helluland/Baffin Island). User wanted a sky/scenery beat,
specifically the aurora borealis — confirmed message option A with a "Love, Aunt Liv" sign-off, and
the safer (no-date) Fun Fact option paralleling card 02's saga-identification approach.

**Real bug found before it shipped:** while building card 03 with a flavour-only imprint (per
`PZ-10`, only the live pointer card gets a real grid reference), checked card 01's imprint and found
it still read `Vinland Editions · Series F, No. 1` — the actual beasts-chain answer — left over from
before last session moved that pointer to card 02 (`PZ-13`). Two cards were both claiming to be the
real answer. Fixed card 01's imprint to a flavour value (`Series A, No. 1`), rebuilt its PDF and
regenerated its gallery back PNG.

**Card 03 built** the same way as card 02: new `build_postcard_03_pdf.py`, cloned from the proven
card 01/02 pattern (same fonts, same `PC-13` layout table, Leif's stamp reused, postmark place-only
with no invented date). Imprint is flavour (`Series C, No. 3`, no referent).

**Collection builder fully reconciled.** `build_postcard_collection.py`'s `CARDS` list is now empty
— all three of Leif's cards have their own dedicated scripts, so the shared placeholder path has
nothing left to silently overwrite. Its `main()` now assembles the full collection PDF from all
three dedicated scripts' outputs. Rebuilt `Norse_Postcards_Full_Print.pdf` (6 pages, verified: 3
cards × front+back) and regenerated both cards' gallery back PNGs from the real builds.

### Files changed

- `NorseBackpack/Postcards/build_postcard_03_pdf.py` — new.
- `NorseBackpack/Postcards/build_postcard_01_pdf.py` — imprint fixed from the real pointer to a
  flavour value.
- `NorseBackpack/Postcards/build_postcard_collection.py` — `CARDS` emptied (all three cards now have
  dedicated scripts); `main()` updated to assemble from all three.
- `NorseBackpack/Postcards/Postcard_01_LAnse_Back.png`, `Postcard_03_Baffin_Island_Back.png` —
  regenerated from the real builds.
- `output/pdf/Postcard_01_LAnse_{Print,Letter_Print}.pdf` — rebuilt with the corrected imprint.
- `output/pdf/Postcard_03_Baffin_Island_{Print,Letter_Print}.pdf` — new.
- `output/pdf/Norse_Postcards_Full_Print.pdf` — rebuilt, 6 pages.
- `NorseBackpack/Norse_Brainstorm.html` — `PZ-05` (card 03 content, card 01 bug note), `PC-07`
  (3 of 18), Postcards gallery toolbar note and card 03's caption/alt text.

### Checks run

- `build_postcard_03_pdf.py` ran clean (front-size guard passed).
- Rendered both pages via PyMuPDF at 300 dpi and visually inspected: front unstretched, message
  correct, Fun Fact box fits with no overflow, imprint reads `Series C, No. 3`.
- Verified `Norse_Postcards_Full_Print.pdf` is exactly 6 pages after rebuild.
- Served over local HTTP: no console errors; confirmed via `find` (cache-busted query string needed
  — the shared server this session is attached to cached an earlier response once) that both `PZ-05`
  and the gallery captions show the new text.
- Deleted temporary preview PNGs from `output/pdf/` after inspection.

### Next action

Cards 04–18 are all still unwritten (`PC-07`, `PZ-05`) — Leif's trail (the first three) is the only
one fully built. Rollo, Aud and Harald's cards are next whenever the user wants to continue.

### Blockers / open items

- Postmark dates remain unassigned for every card (`PC-03`/`PC-04`).
- Where Hnefatafl (`PZ-01`) sits in the sequence — still open.
- Museum ticket physical print test — still outstanding.

## Session Close — 2026-09-13 (final for today) — Card 02 fully built (front + real back); postcard-voice standard moved into the project HTML

**Task:** two follow-ups from the same thread. First, the user pointed out that a tone/voice
decision had been saved only to Claude Code's personal memory and should live in the project itself
— moved it into `Norse_Brainstorm.html`'s Design guide → Tone & voice section, and strengthened
`AGENTS.md`'s "Where Design State Lives" to say the HTML page is the project's main repository, not
just a status board. Second, the user finalized card 02's message text (two typos fixed:
"exaggerating.," → "exaggerating," and "It sound like" → "It sounded like") and asked for a Fun Fact,
then said to generate the actual postcard.

**Fun Fact:** offered two options — a timber-trade one needing a date I couldn't verify, and a safer
saga-citation one. User picked the safe option (no date to source-check).

**Card 02 built end to end.** New `NorseBackpack/Postcards/build_postcard_02_pdf.py`, cloned from
card 01's proven reportlab pattern (same fonts, same `PC-13` standard layout table) rather than the
simplified placeholder path in `build_postcard_collection.py`. Reuses Leif's longship stamp (one
stamp per traveller, not per card) and the existing Battle Harbour front art (already 1500×1050, no
guard failures). Postmark shows the place only — **no date drawn**, since the eighteen postmark
dates are still unassigned (`PC-03`/`PC-04`) and `PZ-08` needs those checked against a trail-order
constraint before any go on a card; inventing one would violate "do not invent dates" and could
conflict later. The imprint line now reads the real pointer, `Vinland Editions · Series F, No. 1`,
since `PZ-13` moved that from card 03 to card 02 last session.

**Found and fixed a collision before it caused damage:** `build_postcard_collection.py` still had
card 02 in its `CARDS` list with placeholder text. Running it would have silently overwritten the
new hand-built PDF. Removed card 02 from that list, added a comment explaining why, and pointed the
collection assembler at the new dedicated script's output instead.

Regenerated `Postcard_02_Battle_Harbour_Back.png` from the real PDF (was the stale placeholder image)
and updated the Postcards gallery tab's caption and alt text to match.

### Files changed

- `NorseBackpack/Postcards/build_postcard_02_pdf.py` — new.
- `NorseBackpack/Postcards/build_postcard_collection.py` — card 02 removed from `CARDS`; assembler
  now references the dedicated script's PDF output.
- `NorseBackpack/Postcards/Postcard_02_Battle_Harbour_Back.png` — regenerated from the real build.
- `output/pdf/Postcard_02_Battle_Harbour_Print.pdf`, `Postcard_02_Battle_Harbour_Letter_Print.pdf` —
  new.
- `NorseBackpack/Norse_Brainstorm.html` — `PZ-05` (final message + Fun Fact + build status), `PC-07`
  (2 of 18), Design guide's Tone & voice section (new "Liv's postcard voice" card), Postcards gallery
  caption/alt text for card 02.
- `AGENTS.md` — "Where Design State Lives" strengthened per the user's correction.
- `~/.claude/projects/.../memory/` — removed the postcard-voice content memory; added a process-only
  memory about where durable project content belongs (repo, not personal memory).

### Checks run

- `build_postcard_02_pdf.py` ran clean (front-size guard passed, no stretching).
- Rendered both pages of the single-card PDF and the two-up letter PDF via PyMuPDF at 300/150 dpi
  and visually inspected: front unstretched, message/typos correct, stamp and postmark legible,
  address and Fun Fact box fit with no overflow, imprint reads correctly, crop marks outside trim on
  the letter sheet.
- Served over local HTTP (port 8734): no console errors; confirmed via `find` + screenshot (not
  `get_page_text`, which locks onto the journey article regardless of hash) that the Postcards
  gallery caption and back image updated correctly.
- Deleted temporary preview PNGs from `output/pdf/` after inspection; real outputs left in place.

### Next action

Draft card 03's message (scenery/sky angle, per the earlier lock-sequence discussion) in the same
confirmed voice, then decide its Fun Fact and build it the same way.

### Blockers / open items

- 16 of 18 cards still have no message text; card 03 has none yet.
- Postmark dates remain unassigned for every card (`PC-03`/`PC-04`) — card 02's postmark will need
  a date added once that's resolved.
- Where Hnefatafl (`PZ-01`) sits in the sequence — still open.
- Museum ticket physical print test — still outstanding.

## Session Close — 2026-09-13 (later still, once more) — Card 02's message decided; postcard voice standard set

**Task:** draft card 02's (Markland) message. Offered four short options in chat, varying how directly
each buried its animal mention. The user picked option B and said its tone — enthusiastic, warm, fun,
friendly — should be the standard for all 18 cards, not just this one.

**Written into `PZ-05`:** the voice standard, and card 02's decided message text (*"Second stop:
Markland, 'Forest Land' to the old sagas, and they weren't exaggerating. Trees for miles, and
something with claws walked past my tent last night — I didn't sleep a wink! Still, you'd love it
here."*). Its Fun Fact trivia and its build script/PDF are still outstanding — this only fixes the
message text.

**Corrected mid-session:** the voice standard was first saved only to Claude Code's personal
cross-session memory. The user pointed out durable design content belongs in the project itself, not
somewhere invisible to the repo. Moved it into the Design guide tab's existing "Tone & voice" section
(a new "Liv's postcard voice" card, alongside the game-wide tone cards already there) and deleted the
memory file. Kept a process note in memory instead — *how to decide where content goes*, not the
content itself.

### Files changed

- `NorseBackpack/Norse_Brainstorm.html` — `PZ-05` updated: voice standard, card 02 message text,
  status pill. Design guide tab's "Tone & voice" section gained a "Liv's postcard voice" card (the
  durable version of the standard).

### Checks run

- Served over local HTTP (port 8734, shared server): no console errors, card 02's message text
  renders correctly under `PZ-05`.

### Next action

Draft card 03's message next (scenery/sky, per the earlier lock-sequence discussion), in the same
confirmed voice. Then card 02's Fun Fact trivia (real Markland/Labrador-coast fact, `PC-07`).

### Blockers / open items

- 16 of 18 cards still have no message text at all; card 03 has none yet either.
- Where Hnefatafl (`PZ-01`) sits in the sequence — still open from the prior entry.
- Museum ticket physical print test — still outstanding.

## Session Close — 2026-09-13 (later still again) — Leif's opening lock sequence decided (`PZ-13`); `PZ-10` superseded to card 02

**Task:** the user asked for Leif's route/props state, flagged cards 02/03 as unwritten, then sketched
an actual lock sequence: card 01 opens lock 1, releasing card 02 + map + ticket together; solving the
beasts chain opens lock 2, releasing card 03. That structure directly contradicts the placement this
session's earlier entry had just decided (card 03) — worked out before this sequencing existed.

**Discussed and confirmed in chat first**, then written in:

- **`PZ-13` (new, decided).** Records the two-lock sequence itself: card 01 → lock 1 → (card 02 + map +
  ticket) → beasts chain solved → lock 2 → card 03. Card 02's animal mention is flavour/immersion only,
  kept separate from the disguised "You know me" nudge line, which stays in the imprint. Hnefatafl
  (`PZ-01`) is moved out of this early chain entirely — timing left undecided, consistent with
  `ST-01`/`ST-02` staying unfrozen.
- **`PZ-10` superseded.** Pointer card moved from card 03 to **card 02** — under the new sequence, card
  02 is what's actually in hand alongside the map and ticket when the chain runs, not card 03.
- **Puzzle array (`puzzles` JS, journey view) updated to match:** opening-puzzle entry's `reward` now
  names what lock 1 releases; beasts-on-the-chart entry's `input`/`clue`/`reward`/`status` updated to
  name card 02 as the pointer and lock 2 as what it opens.

**Still unwritten:** the actual text of cards 02 and 03 (`PC-07`/`PZ-05`) — this session only fixed
the mechanism and which card does what, not the message content itself.

### Files changed

- `NorseBackpack/Norse_Brainstorm.html` — new `PZ-13`; `PZ-10` placement text rewritten; `puzzles`
  array entries for "The opening puzzle" and "The beasts on the chart" updated (`reward`, `input`,
  `clue`, `status` fields).

### Checks run

- Served over local HTTP (`static-preview`, port 8734, shared with another already-running session —
  navigated directly rather than restarting it): no console errors, `PZ-13` renders and its
  cross-references resolve.

### Next action

Write card 02 and card 03's actual messages. Working ideas from this session: card 02 mentions the
animals in passing (pure flavour); card 03 mentions scenery or sky (no puzzle mechanism required of
it). Both still need real text — part of the `PC-07`/`PZ-05` backlog.

### Blockers / open items

- Where Hnefatafl (`PZ-01`) actually sits in the sequence — deliberately left open this session.
- `PZ-05` (full letter/message content) remains the largest unwritten piece overall.
- Museum ticket physical print test (from an earlier session) is still outstanding.

## Session Close — 2026-09-13 (later still) — `PZ-10` pointer card placement decided

**Task:** pick up the "beasts-chain sequencing" open item from the prior session. That item had two
parts — which of the 18 cards is live when the chain runs, and the rule-line wording. The wording was
already decided (*"You know me — every little detail counts."*); only placement was open.

**Decided in chat first, then written in:** card 03 (Helluland) carries the rule line, not card 01
(already full) and not card 02. Reasoning: card 03 is the last of Leif's three stops, so by then his
full trail set and his map (with the beast chart already on it, `PZ-09`) are both in hand — the line
reads as a "now go use what you've got" beat. Card 02 was the only other real candidate and was set
aside on pacing alone, not ruled out by any hard constraint. Full sequencing (`PZ-05`, the aunt's
letters) is still unwritten, so this only fixes *which* card, not the exact wording in context — card
03's message is still placeholder text (`PC-07`).

### Files changed

- `NorseBackpack/Norse_Brainstorm.html` — `PZ-10` pill changed from "one piece unwritten" to "card
  text unwritten"; placement paragraph rewritten from open to decided.

### Checks run

- Served over local HTTP (`static-preview`, port 8734 — shared with another session already running
  it, so `preview_start` was skipped and the existing server used directly): no console errors,
  Open questions tab renders `PZ-10`'s new text correctly. Screenshot came back blank (the known
  preview-pane painting artifact noted in earlier sessions, not a page fault) — verified via
  `get_page_text` instead.

### Next action

Write card 03's actual message (part of the still-unwritten `PC-07`/`PZ-05` backlog) so the rule
line has real surrounding context, once the user wants to tackle postcard message-writing generally.

### Blockers / open items

- `PZ-05` (the aunt's letters/card messages) remains the largest unwritten piece and still blocks
  full puzzle sequencing beyond this one placement decision.
- Physical print test for the museum ticket (from the prior session) is still outstanding —
  unchanged by this session.

## Session Close — 2026-09-13 (later same day) — Museum ticket back built; Codex's v2 front verified; `PZ-10` decided

**Task:** design and build the museum ticket prop end to end, then settle `PZ-10`'s one remaining
open question (imprint on all 18 postcards, or only the pointer card).

**Museum ticket, front to back.** Discussed and settled the ticket concept in chat first, per
"Propose before editing": a fictional **Viking Museum of L'Anse aux Meadows** (avoids naming a real
institution), front carries the museum name and a flavour-only numbered site map, back carries the
A–Z visitor index the beasts-chain puzzle needs. Wrote the full 26-letter exhibit list, the user
supplied the digit for each, and this session computed and recorded all seven resulting beast codes
in a new `PZ-12` — BEAR (the currently live pointer, per `PZ-10`) resolves to **3212**. Wrote Codex's
art brief for the front (2 × 5.5 in, clean-map style, 9 flavour-only markers, explicit "no meaningful
pattern" constraint) — Codex had already built it by the time it was reviewed.

Built the back myself (text/data layout is Claude Code's lane, not Codex's, per the Agent Roles
split): `NorseBackpack/Props/MuseumTicket/build_museum_ticket_pdf.py` combines Codex's front PNG with
a drawn A–Z index into one print-ready card, following the project's established reportlab
conventions (same palette, crop-mark helper, front-size guard pattern as `build_postcard_01_pdf.py`).
Single alphabetical column, not two — a 2 in-wide ticket doesn't fit two legible columns at a real
font size once the front art pinned the physical dimensions the earlier chat guess hadn't accounted
for. Zebra-striped for scanning. Rendered and visually confirmed before handing off.

**Codex's v2 front fix, reviewed rather than taken on faith.** The user flagged that Codex's revised
front (remapping its 9 markers to match the back's digit groupings thematically — e.g. marker 3 now
sits on the quay/boat shed, matching Boat Shed/Compass Room/Keel Yard/Navigation Room/Quay all
resolving to digit 3) needed checking. Verified all nine marker-to-group assignments by hand against
the `PZ-12` letter table — all nine are correct. Rebuilt the ticket PDF against the new front (size
guard passed, no stretching) and regenerated the back-page preview PNG to match the front's updated
ticket number (`No. 0847` → `No. 084726`, now consistent on both faces). Found and removed one stray
duplicate back-image file this session had generated under the wrong version suffix before Codex's
fix landed.

**`PZ-10` decided.** The one open sub-question — does every postcard carry the publisher's imprint,
or only the pointer card — is settled: **all 18 get the imprint line.** Reasoning discussed in chat
first: the imprint only hides by reading as routine production metadata, and that only works if
every card has one — a single card being the only one with a publisher's line would itself be the
tell. Seventeen of the eighteen imprints are pure flavour with no real referent (no other trail map
currently has a lettered grid); only the live pointer card's Series letter means anything. Recorded
the consequence for the shared card builder: `build_postcard_collection.py` must reserve the
credit-strip imprint line for every future card back, not just Card 01's custom script — costs
nothing now since 15 cards are unbuilt and 02/03 are still placeholders.

### Files changed

- `NorseBackpack/Norse_Brainstorm.html` — new `PZ-12` (full A–Z index, all seven beast codes); beasts-
  chain puzzle entry updated from "illustrative" to decided `BEAR = 3212`; props list updated;
  `PZ-10` updated to decided on the all-18-imprint question.
- `NorseBackpack/Props/MuseumTicket/build_museum_ticket_pdf.py` — new. Builds the combined front+back
  print PDF and a letter-sheet version with crop marks.
- `NorseBackpack/Props/MuseumTicket/Museum_Ticket_Back_300dpi_v2.png` — regenerated to match the v2
  front's ticket number after Codex's fix.
- `output/pdf/Museum_Ticket_Print.pdf`, `Museum_Ticket_Letter_Print.pdf` — rebuilt against the v2
  front.

### Checks run

- Ran `build_museum_ticket_pdf.py` clean against both the v1 and v2 fronts (the front-size guard
  raises loudly on a mismatched image instead of stretching).
- Rendered both PDF pages at high resolution (PyMuPDF) and visually inspected: front markers
  unstretched, back index legible with all 26 rows fitting comfortably, both faces share the same
  ticket number.
- Hand-verified all nine v2 marker-to-digit-group assignments against the `PZ-12` letter table —
  correct.
- Verified all seven beast codes (BEAR 3212, WOLF 4865, SEAL 4216, ORCA 8231, LOON 6883, HARE 5122,
  DEER 4222) against every other code already in the game (`1021`, `1972`, `231`, `582`, `427`,
  `2468`) — no collisions. Noted, not fixed: DEER lands on three repeated digits, and no letter in
  the table maps to `0`, so no code drawn from this index can ever contain a `0` — both invisible to
  players.
- Served the page over local HTTP (`static-preview`, port 8734): no console errors, both ticket
  images load, `PZ-12` and the updated `PZ-10` text render correctly in the Open questions tab.
- Checked `AGENTS.md` for stale museum-ticket references — none found; this session's decisions
  correctly live only in `Norse_Brainstorm.html` per "Where Design State Lives," since neither rises
  to the level of the file's two hard invariants.

### Next action

Physical print test: print the letter-sheet PDF at 100% and confirm the A–Z index is comfortable to
read at true size, and that Codex's v2 front holds up on paper (not just screen).

### Blockers / open items

- Still open on the beasts-chain: which of the 18 cards is actually live when the chain runs, and
  the exact wording of the pointer rule line — both blocked on `PZ-05`/`PZ-09` sequencing, unchanged
  by this session.

## Session Close — 2026-09-13 — Museum ticket front, revised map

**Task:** build the fictional Viking Museum of L'Anse aux Meadows ticket front, then revise its
numbered site features so they agree with the A–Z visitor index already decided in `PZ-12`.

**Done:** version 2 keeps the clean-map style and established palette but remaps all nine visible
zones: entrance/visitor centre 1, excavation 2, quay/boat work 3, crafts 4, forge 5, longhouse 6,
Jarl's quarters 7, great hall/ocean gallery 8, and an outlying palisaded building 9. The markers
remain equal-weight scenery: no route, ordering cue or visual code. The ticket number was lengthened
from `No. 0847` to `No. 084726` on both sides. Production front and back PNGs are exactly 600 ×
1650 px at 300 dpi (2 × 5.5 in). Version 1 is retained for comparison. Both exact ImageGen prompts
are recorded in the Design guide tab.

### Files changed

- `NorseBackpack/Props/MuseumTicket/Museum_Ticket_Front_300dpi_v2.png` — revised production front.
- `NorseBackpack/Props/MuseumTicket/Museum_Ticket_Front_Source_v2.png` — revised original render.
- `NorseBackpack/Props/MuseumTicket/Museum_Ticket_Back_300dpi_v2.png` — refreshed back preview.
- `NorseBackpack/Props/MuseumTicket/build_museum_ticket_pdf.py` — now uses the version-2 front and
  prints `No. 084726` on the back.
- `output/pdf/Museum_Ticket_Print.pdf` and `Museum_Ticket_Letter_Print.pdf` — rebuilt.
- `NorseBackpack/Norse_Brainstorm.html` — current previews, feature mapping and revision prompt.
- `HANDOFF.md` — this session record.

### Checks run

- Inspected the revised front at full size: text is correct; digits 1–9 each appear once with
  consistent styling; all nine visible features agree with their room-number groups.
- Read front and back image metadata: both are 600 × 1650 px at 300 dpi.
- Rendered and visually inspected both pages of the direct ticket PDF and letter-sheet PDF. Front
  and back are sharp, within trim marks, and both display `No. 084726`.
- Served the design page over local HTTP: both version-2 previews load at 600 × 1650 px and the
  page reports no console errors.

### Next action

Print the letter-sheet PDF at 100% and confirm that the small A–Z index remains comfortable to read
at physical size.

### Blockers / open items

- No design blocker. Physical print legibility has not yet been tested.

## Session Close — 2026-09-12 (later same day) — HTML readability fix + stale-status sync

**Task:** the user asked me to confirm details of the beasts-chain puzzle (clue 2: F1/BEAR/numbers).
I initially reported it as unwritten/undecided — wrong. Root cause: `grep`'s content mode silently
truncates very long lines to `[Omitted long matching line]`, and this file had single lines up to
23,148 characters (the whole `puzzles` JS array was one line; several `qrow` entries were 3,000–8,000
chars). I was skipping those omitted results instead of reading the underlying lines, so I missed
real content (`PZ-10`'s decided rule line, the `F1`/`BEAR` grid reference) that was there all along.

**Fix 1 — file made actually readable.** Extracted the six large inline `<svg>` diagrams (40KB) to
`Art/Diagrams/*.svg`, referenced via `<img>` (added `.fig img` alongside the existing `.fig svg` CSS
rules so sizing is unaffected). Reformatted all remaining long lines by replacing runs of whitespace
with newlines *only in text between tags* (never inside a tag/attribute, verified by asserting the
whitespace-collapsed content is byte-identical before/after) and split the `puzzles` array onto one
line per object. File dropped from 260,971 → 227,867 bytes and is now under Read's 256KB/25k-token
limits, so it can be read directly instead of grepped.

**This broke, then was fixed: the JS was briefly invalid.** The line-wrap pass assumed `<script>`
always starts a line — it doesn't here (it follows a huge preceding line) — so raw newlines landed
inside single-quoted JS string literals, which is a syntax error in classic JS. Caught by
`node --check`, not by eye. Fixed surgically: a small string-aware scanner walked the script block
and converted only the newlines that were *inside* a quote back to a space (exactly reversing that
specific damage), leaving the safe inter-object newlines alone. Re-verified with `node --check` →
clean, and confirmed in a real browser that puzzle 1 and puzzle 2 still render with identical text.

**Fix 2 — local browser QA now actually works.** Every prior handoff in this file claims the in-app
browser "blocks local `file://` pages" so JS/console checks could not run. That claim is false: a
`file://` URL renders as a static, non-interactive snapshot (0×0 viewport, no JS execution) in this
tool, but a real HTTP origin works fully. Added `.claude/launch.json` (repo root) with a
`static-preview` config (`python -m http.server 8734`) — use `preview_start` with
`name: "static-preview"`, then navigate to `http://localhost:8734/NorseBackpack/Norse_Brainstorm.html`.
This gives real DOM/JS/console/network access for every future HTML check in this repo. Update
`AGENTS.md`'s Validation section if this should become the standard method.

**Fix 3 — stale content sync, now that the file could be read properly.** Cross-referenced the
`puzzles` array against what's actually on disk (via a background audit agent) and found three
entries stale against finished work:
- **Beasts on the chart** (`clue 2`): status was `'candidate · chain agreed'`, clue said "not
  written", risk implied the artwork wasn't final. Reality: all seven beasts are finished and placed
  (`TravelMap/build_trail_maps_pdf.py:163-169`, comment shows a PR-11→PR-13 revision already done),
  bear is at grid square F1, and `PZ-10`'s generic rule line *is* already decided
  ("You know me — every little detail counts"). Updated status to
  `'candidate · art finished, placement open'` and rewrote `clue`/`solve`/`risk` to say what's
  actually still open: which of the 18 cards carries the pointer, and a true-size bear-vs-wolf
  legibility check.
- **The opening puzzle** (`clue 1`, decided): risk said the luggage tags were "not yet purchased or
  physically test-printed" — but `output/pdf/Luggage_Tag_Inserts_Print.pdf` already exists. Updated.
- **The route hidden in plain sight** (final puzzle): status was `'decided · shape only'` and risk
  said card-mounting method was still open — but `PZ-06` (same file) already decided laminated
  wet-erase sheets, and print-ready PDFs exist for 3 of 4 trails (`output/pdf/Trail_Map_{1,2,3}_*`;
  Harald's sheet doesn't exist yet). Updated status to `'decided · 3 of 4 maps built'` and rewrote
  risk to drop the resolved parts.

**Fix 4 — added a "Travel routes" tab gallery** for the print-ready trail map PDFs and Leif's beast
art (bear/orca thumbnails), so this specific gap — finished assets with no gallery entry — can't
recur silently. Links: `output/pdf/Trail_Map_{1_Leif,2_Rollo,3_Aud}_Print.pdf`; Harald shows an
explicit "not built yet" pill instead of a dead link.

### Files changed

- `NorseBackpack/Norse_Brainstorm.html` — SVG extraction, CSS `.fig img` rules, full-file line
  rewrap, `puzzles` array reformatted + 3 stale entries corrected, new Travel-routes maps gallery.
- `NorseBackpack/Art/Diagrams/*.svg` — new, 6 files extracted from inline `<svg>`.
- `.claude/launch.json` — new, `static-preview` server config for local HTML QA.

### Checks run

- `node --check` on the extracted `<script>` block: clean.
- Whitespace-collapse equality asserted programmatically before/after the line-wrap pass (proves no
  visible text changed).
- Served over `http://localhost:8734` (not `file://`): zero console errors; puzzle list renders all
  8 entries with correct text (spot-checked puzzles 1 and 2 word-for-word against pre-edit content);
  all 23 `<img>` elements on the page resolve to real files (checked via `Image()` + `naturalWidth`,
  and via network-request log for the new diagrams); new Travel-routes gallery renders, links point
  to real PDFs, thumbnails load. Screenshotted both the Postcard-system tab and the Design-spec tab
  (confirms the two large re-hosted diagrams — board-setup-transfer, hnefatafl board — render).

### Next action

Nothing queued from this session specifically. The three corrected puzzle entries still have real
open items recorded in their `clue`/`risk` text (see `PZ-05`/`PZ-10` for the beasts pointer;
Harald's trail map doesn't exist yet). If continuing on the beasts puzzle, start there.

### Blockers / notes for future sessions

- **Read this file with `Read`, not `Grep` content mode, if it grows past ~256KB again** — grep
  truncates long lines silently and that caused this session's original error. If a line exceeds
  ~2-3k chars again, prefer `awk`/Python line-length checks over trusting grep output completeness.
- The `.claude/launch.json` static server is generic (serves the whole repo root); reuse it for any
  future HTML in this project rather than re-discovering the `file://` limitation.

## Session Close — 2026-09-12

**Today, in order:** postcard card-back layout redesigned and set as the standard (Fun Fact block
nearly doubled, address moved into dead space); the `F1` publisher's-imprint puzzle designed, built,
then relocated to sit opposite the image credit (`PZ-10`); image-credit file paths dropped from all
three cards, with `Image_Credits.html` extended to cover 02/03 first so nothing was left undocumented
(`PC-09`, `PC-14`); card size fixed at 5 × 3.5 in for all eighteen cards (`PC-13`); the resulting 5%
front-art stretch found and fixed **twice** — once in `build_postcard_01_pdf.py` (Codex reframed the
art), once in `build_postcard_collection.py` (found by this session while closing out, same bug, no
guard existed) — `PC-11` is now fully closed with matching guards in both builders; and the beasts-
chain rule line was picked (*"You know me — every little detail counts"*), deliberately generic
after two more specific drafts were rejected as too easy.

**Everything postcard-related that was open this session is now closed or has a clear next step.**
No known distortion or size-mismatch bugs remain in the three build scripts.

### Files changed today (all sessions)

- `NorseBackpack/Postcards/build_postcard_01_pdf.py` — layout redesign, imprint placement, credit
  trim, size guard.
- `NorseBackpack/Postcards/build_postcard_collection.py` — credit trim, then `SIZE`/`PAGE` fix,
  proportional back layout, size guard (this session).
- `NorseBackpack/Postcards/build_postcard_front_images.py` — 1500×1050 guard, proportional title
  position (Claude Code); illustration art itself reframed by Codex.
- `NorseBackpack/Postcards/Image_Credits.html` — entries for all three postcards.
- `NorseBackpack/Postcards/build_topedge_test_sheet.py` — new DPI/size constants (Codex).
- `NorseBackpack/Norse_Brainstorm.html` — `PC-09`, `PC-11`, `PC-13`, `PC-14`, `PZ-10`, `PZ-11` and
  the Design spec's new card-back standard section.
- `output/pdf/Postcard_0{1,2,3}_*`, `Norse_Postcards_Full_Print.pdf` — rebuilt, final state.

### Next action

Pick one:
1. **Place the beasts-chain rule line** — blocked on `PZ-05`/`PZ-09` deciding which card is live
   when that puzzle runs.
2. **Write real back content for cards 02/03** — currently placeholder text ("Message and travel
   date to be finalized").
3. Something new — no other blockers on the board right now.

## Earlier Session — PC-13 Front-Art Reframe

**Session scope:** reframe the three existing postcard illustrations from 1536 × 1024 (3:2) to
1500 × 1050 (10:7) without stretching, preserve the Card 02/03 `1576` edge join, and exercise the
existing size guards.

Done:

- Reframed all three illustration sources with the same exact-ratio transform: crop 38 px from
  each side and 2 px from the bottom (1460 × 1022, exactly 10:7), preserve the top pixel row, then
  uniformly scale to 1500 × 1050. A generative Card 01 trial was rejected because it changed the
  artwork; it was not used in the project.
- Applied the identical centred horizontal crop and scale to Cards 02 and 03. Rebuilt their fronts,
  rotated Card 02 against Card 03, and confirmed the cloud fragments still join as `1576`.
- Rebuilt `Postcard_02_03_Aligned_Preview.jpg` and the 4× alignment proof from the new fronts.
- Updated `build_topedge_test_sheet.py` from the obsolete 256 dpi / 6 × 4 in assumptions to
  300 dpi / 5 × 3.5 in, added a 1500 × 1050 guard, and regenerated its PDF.
- Updated `Norse_Brainstorm.html` (`PC-11`, `PC-13`, Postcards preview text and Design spec) and
  `Postcards/References/README.md` to record what is now done and what remains.

Files changed this session:

- `NorseBackpack/Postcards/Postcard_0{1,2,3}_*_Illustration_*.png` — reframed in place.
- `NorseBackpack/Postcards/Postcard_0{1,2,3}_*_Front.png` — rebuilt.
- `NorseBackpack/Postcards/Postcard_02_03_Aligned_Preview.jpg` and
  `Postcard_02_03_1576_Alignment_Proof.png` — rebuilt at the new aspect/scale.
- `NorseBackpack/Postcards/build_topedge_test_sheet.py` and
  `output/pdf/Postcard_02_03_TopEdge_Test.pdf` — updated/rebuilt.
- `output/pdf/Postcard_01_LAnse_Print.pdf` and `Postcard_01_LAnse_Letter_Print.pdf` — rebuilt by
  the guarded Card 01 builder.
- `NorseBackpack/Norse_Brainstorm.html`, `NorseBackpack/Postcards/References/README.md`.

Checks:

- All three illustration sources and all three generated fronts are exactly 1500 × 1050.
- `build_postcard_front_images.py` and `build_postcard_01_pdf.py` both completed without guard
  errors.
- Full-size visual inspection: no subject or title clipping; Cards 02/03 remain full bleed.
- New 4× seam proof visually reads `1576` after Card 02 is rotated 180°.
- Rendered and inspected every page of the rebuilt Card 01 single-card PDF, two-up PDF, and
  top-edge test PDF; no layout defects found. Poppler emitted missing-display-font warnings for
  Symbol/ArialUnicode, but the rendered pages themselves are correct.
- The in-app browser security policy blocked the local `file://` Norse page, so the HTML could not
  be visually checked there. Source-level tag/link checks passed; the refreshed preview images were
  inspected directly at full size.

**Update, same day, Claude Code session:** this next action was the bug. `build_postcard_collection.py`
still had `SIZE=(1536,1024)` / `PAGE=6×4in` while its own front images were already 1500×1050 —
confirmed by rendering `Postcard_02_Battle_Harbour_Print.pdf` and finding the front stretched 5%
onto a 6×4in page, plus the card itself was still the wrong physical size against `PC-13`. No guard
existed to catch it. Fixed: `SIZE=(1500,1050)`, `PAGE=landscape(3.5×72, 5×72)` (matches
`build_postcard_01_pdf.py` exactly), `build_back()`'s placeholder layout moved from fixed pixels to
fractions of the canvas so it survives the next size change, and `build_pdf()` now raises if either
image isn't exactly `SIZE` instead of silently stretching it — same pattern as the other two
builders. Rebuilt and verified: page is exactly 5.0 × 3.5 in, front ratio matches page ratio exactly
(1.4286 both), placeholder back renders with no clipping. `PC-11` is now fully closed.

## Latest Session — Leif Map Review; Per-Trail Band Colour

**Session scope:** review Codex's seven-animal Leif map, then add per-trail colour to the map
generator. No change to any animal placement.

**Review result: placements are correct.** All seven animals verified programmatically in single
cells — BEAR F1, SEAL D1, HARE A3, DEER G2, LOON B5, WOLF A6, ORCA G7 — each clear of the route
corridor and every label box. Rendered at 600 dpi and inspected at true print size: all seven are
identifiable, and the artwork style is consistent across the set.

Findings raised, and their outcomes:

- **Whale/orca collision — user overruled, deliberately.** Both are on the sheet in row 7, two
  cells apart, and `WHALE` is five letters so it is a dead end for a four-dial lock. The user keeps
  the whale on the grounds that it is much larger and drawn in a different ornamental style, which
  signals it as an anomaly and gives players the contrast to name the orca correctly. Accepted.
  Consequence: the middle hint rung must ask "which animal is that, exactly?" rather than point at
  the ticket.
- **LOON could be read as DUCK** — also four letters, so a misread is a confident wrong answer, not
  a soft failure. Risk judged moderate (the drawing has the dagger bill, collar and checkered back)
  but it is a second reason the hint ladder should name the bird family.
- **Stale stable filename** — resolved. `Trail_Map_1_Leif_Print.pdf` was still the pre-animal map
  because PDFgear held it open; the user closed it and this session's rebuild wrote the real file.
- **PDF weight** — 18 MB. The five new vignettes are 1536 × 1024 PNGs printed inside a 48 × 44 pt
  box (0.67 × 0.61 in, ~400 px at 600 dpi), so they are roughly 4× over-resolution. Not fixed;
  downsampling to ~600 px would cut the file with nothing visible changing at print size.

**Cardstock question answered: do not print the maps on coloured stock.** The sheet is a
full-coverage two-tone illustration (sea `#DCE7E4`, land `#EFE3C4`) and printers cannot lay down
white, so coloured stock shifts both fills toward the paper and compresses a contrast that is
already narrow — and that contrast is what identifies the unlabelled animals. The Apricot Crush
stock is better spent on the paper props, where ink coverage is light.

**Per-trail band colour built instead.** Each sheet's grid band now carries its trail colour with
the grid references reversed to white: Leif `#216580`, Rollo `#A2562D`, Aud `#6D528B`. Harald falls
back to a neutral until that trail is defined — it should get `#467444`.

### Files Changed

- `NorseBackpack/TravelMap/build_trail_maps_pdf.py` — `band` key per trail; band drawn as four
  strips before the neat line; grid references reversed to white.
- `NorseBackpack/Postcards/build_postcard_01_pdf.py` — publisher's imprint added, then the whole
  right column reflowed and the type scaled up (see below);
  `output/pdf/Postcard_01_LAnse_Print.pdf`, `Postcard_01_LAnse_Letter_Print.pdf` and
  `Norse_Postcards_Full_Print.pdf` rebuilt (cards 02/03 regenerated mechanically from unchanged
  inputs by the collection builder).
- `NorseBackpack/Norse_Brainstorm.html` — `PZ-06` extended with the band decision, the
  white/natural cardstock rule and its reasoning, and the 5 mil pouch note.
- `output/pdf/Trail_Map_{1_Leif,2_Rollo,3_Aud}_{Print,ANSWER}.pdf` — rebuilt.

### Checks

- All three trails rebuild with no error; Leif, Rollo and Aud rendered and compared side by side —
  the three band colours are distinguishable at thumbnail size, which is the whole point.
- Leif rendered at 150 dpi: white grid references legible on the blue band, title band still cream,
  map content and all eleven vignettes unchanged.
- Collision guard still reports only its prior dropped non-stop labels (Makkovik, Red Bay, Rigolet).
- `Norse_Brainstorm.html` opened in the in-app browser: 8 puzzles render, 48 question rows, the new
  `PZ-06` text present, no console errors and no `undefined` in the output.

**Early-digit leak closed — `PZ-11` added.** The user spotted that giving a trail's full card set
and its map at the start lets players draw that digit immediately. Analysis and decision:

- Removing the postmark dates does **not** fix it. Leif's three stops project to roughly (218, 235),
  (218, 254) and (163, 680) — every ordering reads as a vertical stroke, so a dateless deck hides
  nothing on a three-stop trail. It would also cost `PZ-08`, which takes the digit order from
  postmarks.
- **Leif is now the deliberate teaching trail.** His cards 01–03 are all committed early and his map
  must be present for the beasts chain, so his `1` is derivable mid-game. Accepted: a group that
  finds it has discovered the mechanism themselves and holds one digit of four.
- **One card held back from each other trail**, chosen by drawing every one-card-removed variant:
  Rollo → **Roumare forest** (the loop-closer; the 9 opens into something closer to a 5),
  Aud → **Hvammur** (forced by the exclusions; any removal leaves two points and no shape),
  Harald → **Aldeigjuborg / Staraya Ladoga** — **provisional**, since Harald has no `TRAILS` entry
  so the test used an approximate projection. Re-test when his sheet exists.
- Two cards per trail were unavailable: the trail's earliest card (`PZ-08`'s sort) and its
  continuation-set card (Markland, Bayeux, Esjuberg, Sicily).
- Verified the scheme actually bites: the route line and numbered stop markers are drawn only on the
  ANSWER sheet, so on the player map stops are ordinary town dots among ~24 labels. The cards are
  what identify the points.
- Consequence for `ST-01`: the final container must release three postcards as well as the reward.

**`PZ-10` settled and printed — the publisher's imprint.** Postcard 01 now carries
`Vinland Editions · Series F, No. 1` right-aligned on the last line of the Fun Fact caption, at
4.2 pt in the same muted grey as the image credit beneath it. Series F, No. 1 is square F1 of
Leif's sheet, where the polar bear is drawn. English only — the French *Édition / Série* form was
mocked up and dropped.

It needed no layout change: the caption's last line ends 9 pt short, so the imprint sits
right-aligned on that same baseline inside the Fun Fact border, which is where a real publisher's
code goes. Verified at 600 dpi and at true card size — it disappears into the production-metadata
strip exactly as intended.

**Two pieces still open on that chain**, both recorded in `PZ-10`:

- **The rule that unlocks it is unwritten.** The card carries the data; nothing yet carries the
  instruction to read it. Working line: *"Never mind the picture. The publishers put more useful
  things on these than the photographers ever did."* Card 01's message is already full at five
  paragraphs plus sign-off, so this either displaces something there or moves to whichever card is
  live when the beasts chain runs. Belongs with `PZ-05`.
- **Whether all eighteen cards carry an imprint**, with only the pointers getting a Series letter.

**Card 01 back reflowed and type scaled up.** The imprint first went inside the Fun Fact border,
then moved to the credit strip, right-aligned opposite the attribution, at the user's request. The
attribution stays: it is legally required (public repo, CC BY-SA 3.0 adaptation) and it is also the
imprint's camouflage — remove it and the imprint becomes the only small grey text on the card.

The right column had a 60 × 72 pt dead strip left of the stamp, and the address panel was 150 pt
wide for a longest line of 78 pt. The address block moved up into that strip, the stamp now overlaps
its unused top-right corner as it would on a real card, and the ruled lines stop at x=278 instead of
running under the stamp. That freed 44 pt of height for the Fun Fact block, which grew from 48 to
89 pt. Sizes now: Fun Fact body 5 → **7.4** (leading 5.8 → 8.8), Fun Fact header 6 → 7.5, imprint
4.2 → **5**, image credit 3.2 → **4**, address 8 → 8.6, TO label 5.2 → 5.8. The Fun Fact text was
re-measured so the box fits its seven wrapped lines with even padding rather than being oversized.

**Layout recorded as the standard; cards 02/03 NOT updated — blocked.** The new card-back layout
and type scale are written into the Design spec tab as the standard for all eighteen cards, with a
full element/size/position table and the rule that the Fun Fact box is sized to its wrapped text
rather than the other way round.

Updating 02 and 03 turned out to be a resize, not a restyle, so it was not attempted. Two conflicts
surfaced and are recorded rather than silently resolved:

- **`PC-13` (new, blocks the deck).** Card 01 is 5 × 3.5 in (10:7, reportlab). Cards 02 and 03 are
  6 × 4 in (3:2, PIL, from 1536 × 1024 art). The Design spec calls for ~5 × 3.5 in and card 01 is
  the one that matches. Resizing 02/03 changes their aspect ratio, so both fronts need reframing,
  and it breaks production work: the hold-to-light top-edge join is built on "1536×1024 px over a
  6 × 4 in card = 256 dpi", and the 1576 alignment proof is measured at that scale. `PC-11` already
  wants the fronts re-rendered at true size, so the two should be answered together. **The choice —
  resize 02/03, or adopt 6 × 4 and re-cut card 01 — should be made before card 04 is built**, since
  fifteen cards are unbuilt.
- **`PC-09` — resolved and actioned on card 01.** That entry wanted the image credit moved off the
  card entirely (a file path on a gift-shop prop). The attribution stays, since it also camouflages
  the imprint, but the narrower immersion point was right: the anachronism was the file path, not
  the credit. The `Source and full attribution: Postcards/Image_Credits.html` line is now dropped.
  One credit line remains and still satisfies CC BY-SA 3.0 on its own — modification notice, title,
  author, licence. `PC-09` marked decided.
- **`PC-14` (found, then fixed).** `Image_Credits.html` documented **only card 01**; cards 02 and 03
  carried their attribution *only* on the cards themselves, as four printed lines each including two
  full URLs. Stripping those would have deleted the project's only record of them, so the credits
  page was extended first: matching entries for **Postcard 02** ("Battle Harbour - MacGillivray",
  Matt MacGillivray, CC BY 2.0) and **Postcard 03** ("Grinnell Glacier Bergie Bits, Baffin Island",
  Gregory "Slobirdr" Smith, CC BY-SA 2.0), each with original work, photographer, source file page,
  licence, changes and adaptation licence, taken from `References/README.md`. Only then were the
  printed credits reduced to one line each in card 01's form. **No URL is now printed on any card
  back.** `PC-14` marked decided.

  Worth knowing: the printed line names the *source's* licence, not the adaptation's, and carries no
  licence URI. For the two ShareAlike sources (01 and 03) that notice now lives only on the credits
  page, which ships in the repo alongside the PDFs. Reasonable for the medium, but it is a judgement
  call rather than a technicality. Card 02's source is CC BY 2.0 and carries no ShareAlike condition.

- `NorseBackpack/Postcards/Image_Credits.html` — entries added for Postcards 02 and 03.
- `NorseBackpack/Postcards/build_postcard_collection.py` — cards 02/03 printed credits reduced to
  one line each; `output/pdf/Postcard_02_*`, `Postcard_03_*` and `Norse_Postcards_Full_Print.pdf`
  rebuilt.

**`PC-13` decided: 5 × 3.5 in** (360 × 252 pt, 10:7) is the standard for all eighteen cards. Cards
02 and 03 must be rebuilt to it — their backs are placeholders, so little is lost there.

**Checking that decision turned up a live defect.** Every front is 1536 × 1024 (3:2) while the card
is 10:7, and `build_postcard_01_pdf.py` draws the front with `preserveAspectRatio=False` — so card
01's printed front is **stretched vertically by exactly 5%** (1.5 ÷ 1.4286). It is shipping in
`Postcard_01_LAnse_Print.pdf` and the collection PDF right now, and shows most in the title
lettering. Card 01's *back* is already correct at 1500 × 1050.

`PC-11` already prescribed the right fix — re-render at 1500 × 1050 from the source photographs in
`References/`, do **not** rescale or crop the existing art — so it was updated rather than replaced,
and promoted from tidy-up to defect fix. `build_postcard_front_images.py` also has to change: it
currently *raises* on anything that is not 1536 × 1024.

Two constraints recorded for when 02/03 are reframed: the crop must be symmetric and identical on
both, or the `1576` top-edge cloud flecks fall out of register when 02 is rotated 180° against 03;
and the join must be re-proofed, since the dpi changes with the card size.

**Code-side half of `PC-11` done; art half blocked on Codex.** Fixed what a Claude Code session can
fix: `build_postcard_front_images.py` now requires 1500 × 1050 (was 1536 × 1024) and scales title
position by height fraction instead of fixed pixels; `build_postcard_01_pdf.py` now raises loudly if
`Postcard_01_LAnse_Front.png` isn't exactly 1500 × 1050, instead of silently stretching it onto the
page as before. Verified: running `build_postcard_front_images.py` against the current (still
1536 × 1024) illustration raises the expected error rather than proceeding.

**Not done — cannot be done by this agent: the three illustration source files still need
reframing/regeneration to 1500 × 1050.** That's image generation, Codex's lane per the role split
in `AGENTS.md`. Nothing was rebuilt this session (front images, card 01 PDF, or the collection),
since the guards correctly refuse to run until the art is the right size.

**Superseded closure claim — corrected by the latest session.** Codex reframed all three
illustrations to 1500 × 1050 and updated `build_topedge_test_sheet.py`'s `DPI` constant to 300.
The earlier note incorrectly claimed the collection builder had also been converted; repository
state shows it still uses 1536 × 1024 on a 6 × 4 in page. Verified work from that pass:

- `build_postcard_front_images.py` — no size-guard errors, all 3 fronts rebuilt
- `build_postcard_01_pdf.py` — rebuilt clean, no distortion errors
- `Postcard_02_03_1576_Alignment_Proof.png` — all four digits (1-5-7-6) still legible at the new size
- `Postcard_02_03_Aligned_Preview.jpg` — card 02 rotated 180° meets card 03 with no visible seam

The remaining postcard-pipeline step is the `build_postcard_collection.py` size/page conversion
recorded in the latest session above.

**Beasts-chain rule line decided.** Two drafts naming the mechanism directly (one referencing "the
publishers," one contrasting "drew" vs "printed") were rejected as too easy — finding the unlabelled
F1 and then noticing the map has a lettered grid is already the puzzle. Settled on a deliberately
generic line instead: *"You know me — every little detail counts."* Reusable across other puzzles
rather than spent here. Recorded in `PZ-10`.

Placement still open: goes on whichever card is live when the beasts chain runs, not card 01 (its
message is full). Depends on `PZ-05`/`PZ-09` settling the sequence.

### Next Action

None queued. Open items on the board: place the beasts-chain rule line once sequencing is decided (`PZ-10` / `PZ-05`) and decide where it goes, since card
01's message has no room as it stands. Then re-test Harald's held-back card once his trail is
defined in `TRAILS` — that entry also needs `band="#467444"` to complete the band set.

## Earlier Session — Leif Map: Seven Animal Grid Placements

**Session scope:** update only Leif's seven animal vignettes to the supplied page boxes. The
longship, whale, settlement and iceberg remain unchanged.

Bear and wolf were moved. New seal, hare, deer/caribou, loon and orca vignettes were generated in
the existing dark-green screen-print style, cleaned to real transparency after ImageGen baked in a
checkerboard, and added to the map. The seven cells are F1, D1, A3, G2, B5, A6 and G7 respectively.
The animal list in the design page now uses LOON instead of the earlier CROW candidate.

### Files Changed

- `NorseBackpack/TravelMap/build_trail_maps_pdf.py` — seven exact animal boxes and opacity values.
- `NorseBackpack/TravelMap/Art/Leif_{Seal,Hare,Deer,Loon,Orca}_v1.png` and matching
  `Art/processed/` derivatives — new transparent animal assets.
- `NorseBackpack/Norse_Brainstorm.html` — placement state, LOON substitution and exact generation
  prompt structure recorded.
- `output/pdf/Trail_Map_1_Leif_ANSWER.pdf` — rebuilt answer key.
- `output/pdf/Trail_Map_1_Leif_Print_UPDATED.pdf` — rebuilt player map. The normal stable print
  filename could not be replaced because PID 25340 (`PDFgear`) has it open.

### Checks

- All five new source PNGs are RGBA with alpha extrema 0–255 after deterministic cleanup.
- Rebuilt player and answer PDFs are single-page US Letter files and rendered successfully.
- Visually inspected both pages at 180 dpi: all seven animals occupy the requested cells; the four
  unchanged decorations remain fixed; no animal is clipped and the answer route remains readable.
- Existing collision guard reports only its prior dropped non-stop labels: Makkovik, Red Bay and
  Rigolet. No route stop is missing.
- Live local HTML QA could not run because the in-app browser security policy blocked the
  `file://` page. Source structure and references were checked directly instead.

### Next Action

Close `Trail_Map_1_Leif_Print.pdf` in PDFgear, then replace that stable file with the verified
`Trail_Map_1_Leif_Print_UPDATED.pdf`.

## Latest Session — Card 01 Front Reframed to Full Bleed

**Session scope:** give Card 01's artwork side the same edge-to-edge treatment already approved
for Cards 02 and 03. The back was not redesigned.

Card 01's cream outer rim was removed with a uniform 20 px crop, then the artwork was restored to
1536 × 1024. The finished native-size front is now the PDF source, so its title placement matches
the web preview instead of being rebuilt separately. No hidden edge code was added.

### Files Changed

- `NorseBackpack/Postcards/Postcard_01_LAnse_Illustration_v3.png` — new full-bleed source.
- `NorseBackpack/Postcards/Postcard_01_LAnse_Front.png` — rebuilt at 1536 × 1024.
- `NorseBackpack/Postcards/build_postcard_01_pdf.py` — uses the finished front directly.
- `NorseBackpack/Postcards/build_postcard_front_images.py` — Card 01 added to the shared front builder.
- `NorseBackpack/Postcards/Postcard_01_LAnse.html`, `Postcard_01_LAnse_Style_Study.html`,
  `Image_Credits.html`, `References/README.md`, and `NorseBackpack/Norse_Brainstorm.html` —
  full-bleed source/status and adaptation notes recorded.
- `output/pdf/Postcard_01_LAnse_Print.pdf`, `Postcard_01_LAnse_Letter_Print.pdf`, and
  `Norse_Postcards_Full_Print.pdf` — rebuilt. Cards 02 and 03's individual PDFs were mechanically
  regenerated from unchanged inputs by the collection builder.

### Checks

- Inspected the native 1536 × 1024 front and both pages of the individual print PDF.
- Inspected the two-up letter front sheet and confirmed the crop marks remain outside the cards.
- Confirmed the full collection's first two rendered pages are identical to the individual PDF.
- Confirmed the back remains visually unchanged and readable.
- HTML structure remains balanced: 715 `div`, 11 `section`, 22 `figure`, and 9 `details` pairs.
- Local HTML browser QA could not run because the in-app browser security policy blocked the
  `file://` page. The changed HTML source and referenced image assets were checked directly.

### Next Action

Review or print Card 01's new full-bleed front. If approved, continue with the next postcard task.

## Latest Session — Second 40-SVG Norse Icon Batch

**Session scope:** extend the reusable icon library using the same five approved style treatments.
No icon was placed on a finished map or prop.

Built eight new subjects in clean-map, carved-woodcut, historic-manuscript,
antique-cartography and hand-drawn styles: bone/antler comb, hnefatafl game piece, silver coin,
carved rune stick, drinking horn, palisade fort, trading port and early wooden church. This adds
40 transparent SVGs. The rune stick's first render looked like repeated modern “K” letters; it was
corrected to neutral tally-notches before recording the set. `PR-16` is **Built · review**.

### Files Changed

- `NorseBackpack/Icons/Options_02/` — five style folders with eight SVGs each.
- `NorseBackpack/Icons/Norse_Icon_Style_Options_Batch_2.svg` and `.png` — comparison artifacts.
- `NorseBackpack/Icons/build_style_options.js` — second batch added to the editable generator.
- `NorseBackpack/Norse_Brainstorm.html` — second-batch preview and `PR-16` added.
- `HANDOFF.md` — this handover entry.

### Checks

- All 40 second-batch files parse as XML, use the 64 × 64 viewBox and render with transparency.
- Comparison sheet rendered at 2622 × 1600 and was visually inspected at 64 px and 20 px.
- HTML structural counts remain balanced and the new preview reference resolves.

### Next Action

Review `PR-16`'s comparison sheet and approve or target any subject that needs redrawing before use.

## Latest Session — Norse Constraints Loosened; Cross-Project Clue Library Built

**Session scope:** brainstorming the Norse opening/lock structure, then two concrete outputs the
user asked for — relax the recorded Norse constraints, and build a reusable clue repository.

Discussion covered the lock count (8–10 wanted), how the four trail maps can each carry two or more
jobs before the finale so players do not read them as the endgame device, and clue-hiding techniques
generally. Most of that stayed in chat per propose-before-editing; the one design decision the user
approved for writing was Leif's front-of-sheet job, recorded below as item 3.

Three things were written:

1. **`AGENTS.md` design invariants rewritten.** The user said the work is still over-constrained by
   earlier decisions. Only two constraints remain recorded: eighteen postcards, and a final puzzle
   that reads as shapes drawn on maps (and even that is open if something better appears). The
   opening luggage-tag puzzle, the codes `1021`/`1972`, the six puzzle families, container structure,
   lock hardware and postcard order are now explicitly soft. Anything marked "Decided" in
   `Norse_Brainstorm.html` before 2026-09-12 is a strong candidate, not a constraint.
2. **`clues.html` created** — a cross-project repository of 167 clue and puzzle techniques across
   eight categories (text 30, symbols 24, maps 22, props 26, materials 19, logic 13, combining 21,
   structure 12), each with a plain description, a worked example written for one of our own games, a
   build cost, a 1–5 difficulty rating, optional pitfall note, and a source link. Plus a principles
   page and a sources page citing Nicholson's escape-room papers, The Codex, the Wiemker taxonomy
   paper and MIT Mystery Hunt construction guides.

   The **Combining clues** category was added after a follow-up discussion about composition rather
   than concealment. Its organising idea: locks gate access, pointers gate understanding, so the
   number of puzzles need not equal the number of locks. It covers pointer chains (the lockless
   "the answer names the next prop" pattern, plus the *inert until named* fix for its shortcut
   weakness), rule/data splits, instruments, selection-and-order splits, transformation chains,
   accumulators, convergence and the *burst structure* (a lock releases props, a hardware-free chain
   plays out among them, the last step yields the next code). Seven entries specifically cover
   getting several props to feed one lock — searchable with "several props".
3. **Leif's map given a front-of-sheet job — the "Beasts on the chart" chain**, written into
   `Norse_Brainstorm.html`. Seven unlabelled animal vignettes on the North Atlantic sea chart
   (BEAR, WOLF, SEAL, ORCA, CROW, HARE, DEER), each drawn in a setting only that animal occupies.
   A postcard points to one; identifying it gives a four-letter key; the key is looked up letter by
   letter on an A–Z visitor index printed on the back of the L'Anse aux Meadows museum ticket,
   giving four digits. A transformation chain, not a pointer — neither prop is any use alone.
   This answers the gap `PZ-09` flagged, since Leif's only other job is on the back of the sheet.

   User decisions recorded: beasts are **unlabelled** (context does the identifying, not captions),
   the lookup is a **keyed index on the ticket back**, and there is **no validator** — the lock is
   the check. That last one is deliberate and means a misidentification is only caught by the
   padlock, so the middle hint rung pushes on identification rather than on the lookup.

   `BOAR` was requested and excluded on the native-species test: wild boar are not native to North
   America. It moves to Rollo's map, where it is both correct and apt (Roumare was a hunting
   forest). `DEER` was kept, drawn as a caribou, which is genuinely native to all three Leif stops.

### Files Changed

- `AGENTS.md` — "Norse Backpack — current design invariants" section rewritten and dated.
- `clues.html` — new, cross-project clue/puzzle library with tabbed nav and a live search.
- `index.html` — added a Clue Library card under "Design guides & brainstorming".
- `NorseBackpack/Norse_Brainstorm.html` — new "Beasts on the chart" puzzle entry; `PZ-09` updated
  (Leif now has two decided jobs, boar noted against Rollo); new `PZ-10` for the pointing clue.
  Also fixed three hardcoded puzzle counts in the script (`i===6`, `/ 7`) that would have broken
  the journey and detail nav as soon as an eighth puzzle was added.
- `HANDOFF.md` — this handover entry.

### Checks

- Opened `clues.html` in the in-app browser. JavaScript runs, all 10 nav tabs switch correctly,
  category counts render, and all 167 cards have a source, a worked example, a build cost and a
  valid category.
- Search verified as spanning every category rather than only the open tab ("lamp" returns 6 across
  four categories); empty-state message verified.
- Deep links (`clues.html#view-map`) verified. Fixed a bug found during testing: an unknown hash
  such as `#view-typo` threw a TypeError in `render()`; `navigate()` now falls back to the intro page.
- All PDF links confirmed `target="_blank" rel="noopener"` with no `download` attribute, per the
  house rule. No relative or broken links.
- Card layout verified through the DOM (three-column grid, cards 377 × 392). Screenshots of the
  scrolled grid came back blank — a preview-pane painting artifact, not a page fault, confirmed by
  `elementFromPoint` returning the expected card content at those coordinates.
- Opened `Norse_Brainstorm.html` in the in-app browser. All 8 puzzles render without error, the
  journey grid shows 8 steps with the ending card last, and prev/next disable correctly at both
  ends — verifying the hardcoded-count fix. `PZ-09` and the new `PZ-10` render in Open questions;
  no console errors and no `undefined` in the output.

### Next Action

Settle `PZ-10` — how the postcard points to one square of Leif's chart. The leading candidate is the
typed publisher's imprint every card already carries (*Édition Vinland Nº 14* → *Série F · Nº 1*),
which hides the grid reference in plain sight and keeps the card carrying the rule rather than the
data. Also open in the same question: whether the chart carries a lettered grid or a latitude and
longitude graticule — the graticule is what a sea chart would really have and reads as navigation
rather than as a lookup device.

Codex is picking up the chart artwork (the seven animal vignettes). The constraint to hand over:
all seven must be identifiable at true print size from setting as much as silhouette, and bear
versus wolf is the risky pair — both read as "quadruped" at 8 mm. A test sheet of all seven at size
should come before final artwork.

## Earlier Session — Knotwork Raven Chosen; Matching Profile Icon Built

**Session scope:** choose the adventure's main raven image and derive its matching frame-free icon.

The user chose `Raven_Profile_Knotwork_Frame_v1.png` as the current main image and possible family
symbol. The spread-wing study remains secondary. A new profile icon preserves the same raven's
pose, engraved detail and palette while removing the whole knotwork frame. ImageGen twice returned
a checkerboard baked into RGB instead of real transparency; `remove_checkerboard_background.js`
therefore removes the repeated neutral checker colours deterministically. A cream-background proof
caught and removed an enclosed checker patch between the legs. `PR-15` is now **Main image chosen**.

### Files Changed

- `NorseBackpack/Art/Raven/Raven_Profile_Icon_v1.png` — new, transparent frame-free icon.
- `NorseBackpack/Art/Raven/remove_checkerboard_background.js` — reproducible alpha cleanup.
- `NorseBackpack/Norse_Brainstorm.html` — main image decision, icon preview, edit prompt and alpha
  correction recorded.
- `HANDOFF.md` — this handover entry.

### Checks

- Final icon is 1254 × 1254 RGBA with alpha extrema 0–255.
- Rendered on cream and inspected: frame and checkerboard are fully absent, including between the
  legs; raven silhouette and pale engraved feather detail remain intact.
- Screen-size proof inspected at 64, 128 and 256 px; the profile remains identifiable at 64 px.
- HTML structure remains balanced after the new three-image identity card.

### Next Action

Test the frame-free profile at its intended printed size. It is still intricate hero-derived art;
if a true 20 px map glyph is needed, simplify from this silhouette rather than scaling it blindly.

## Latest Session — Two Intricate Hero Raven Studies

**Session scope:** create the two approved compositions for the adventure's central raven artwork.
No small raven icon derived and no artwork placed into a finished prop.

Generated two transparent 1254 × 1254 PNG studies in the established dark forest-green and muted
rust palette: a symmetrical spread-wing heraldic raven with interlace built into the feathers, and
a profile raven inside a complete circular Norse knotwork frame. Both use adult-raven anatomy cues
(heavy beak, shaggy throat, wedge tail) and avoid the chick-like proportions of the rejected icons.
`PR-15` is now **Built · review**; exact ImageGen prompts and both previews are recorded in the
Design guide.

### Files Changed

- `NorseBackpack/Art/Raven/Raven_Spread_Wing_Emblem_v1.png` — new.
- `NorseBackpack/Art/Raven/Raven_Profile_Knotwork_Frame_v1.png` — new.
- `NorseBackpack/Norse_Brainstorm.html` — `PR-15` updated and hero-study card added with prompts.
- `HANDOFF.md` — this handover entry.

### Checks

- Both files are 1254 × 1254 RGBA PNGs with genuine transparent and opaque pixels.
- Both generated compositions were visually inspected at full size; no text, scenery or extra full
  bird is present, and both read clearly as ravens.

### Next Action

Choose the lead hero composition and request any single targeted refinement before deriving a
simplified small raven icon from it.

## Latest Session — Seven Icon Subjects Approved; Raven Split Out

**Session scope:** record the review of the five icon sets and begin a separate direction for the
adventure's central raven artwork. No new raven artwork generated yet; composition comes first.

The user approved all five style treatments for seven subjects: longship, settlement, longhouse,
runestone, burial mound, round shield and Dane axe. No single global style was chosen; consistency
is required within each finished piece. All five small raven studies are rejected because they
read as chicks. `PR-14` now records the seven-subject approval, while new `PR-15` treats the raven
as intricate hero artwork for *The Raven Inheritance*, with a small derived map icon deferred.

### Files Changed

- `NorseBackpack/Norse_Brainstorm.html` — Design guide approval/rejection recorded; `PR-14`
  rewritten and `PR-15` opened.
- `HANDOFF.md` — this handover entry.

### Checks

- HTML structural counts remain balanced after the two register updates.

### Next Action

Choose the hero raven's composition, then generate a first intricate transparent artwork study and
record its exact prompt under `PR-15`.

## Latest Session — Five Complete Norse Icon Style Options

**Session scope:** rebuild the reusable eight-icon family as five coherent style choices after the
first-pass raven and Dane axe were judged unclear. No icon has been placed on a map or prop.

Built 40 transparent SVGs: the same eight subjects in clean-map, carved-woodcut,
historic-manuscript, antique-cartography and hand-drawn treatments. The raven now uses a dark,
heavier beak and wedge tail instead of the first pass's orange, duck-like beak. The Dane axe now
has one broad crescent blade visibly joined to its long haft. A single comparison sheet shows all
five sets at 64 px and 20 px. The old root-level set remains only as a superseded reference.

### Files Changed

- `NorseBackpack/Icons/Options/` — five folders containing eight SVGs each.
- `NorseBackpack/Icons/build_style_options.js` — editable data-driven source for all 40 SVGs and
  the comparison sheet.
- `NorseBackpack/Icons/Norse_Icon_Style_Options.svg` and `.png` — comparison artifacts.
- `NorseBackpack/Norse_Brainstorm.html` — Design guide preview updated; `PR-14` opened for the
  style choice.
- `HANDOFF.md` — this handover entry.

### Checks

- All generated SVG files parsed as XML and share the intended 64 × 64 viewBox.
- The comparison sheet rendered locally and was visually inspected at both displayed sizes.
- All 40 individual files rendered successfully at 20 px with transparent backgrounds intact.
- No browser check: the in-app browser continues to block local `file://` SVG URLs by policy.

### Next Action

Choose a whole style in `PR-14`, or name any deliberate hybrid choices, before replacing the
superseded root-level set or placing icons on maps.

## Latest Session — Reusable Norse SVG Icon Set

**Session scope:** a small reusable icon family for text and maps. No map placement or puzzle
content changed.

Built eight individual transparent 64 × 64 SVGs: longship, settlement, longhouse, runestone,
burial mound, round shield, Dane axe and raven. They use the existing map-art palette
(`#283B34` with restrained `#B56A2A`) but are deliberately simpler than the large `PR-11` PNG
vignettes so they remain readable at roughly 20–24 px. Added an SVG preview sheet and a rendered
PNG preview. Recorded the set and its construction rules in the Design guide tab.

### Files Changed

- `NorseBackpack/Icons/` — eight individual SVGs plus `Norse_Icon_Set_Preview.svg` and `.png`.
- `NorseBackpack/Norse_Brainstorm.html` — reusable icon-family card added to Design guide.
- `HANDOFF.md` — this handover entry.

### Checks

- All nine SVG files parsed as valid XML.
- Every individual icon rendered to 256 × 256 PNG with real transparent pixels and opaque art.
- The combined preview rendered at 1440 × 780 and was visually inspected; all eight are distinct
  at map size, and the compact text-size row remains legible.
- The in-app browser refused the local `file://` SVG URL under its browser security policy, so a
  live browser check of the standalone SVG was not possible. The local SVG renderer succeeded.

### Next Action

Review the preview, then choose whether a second batch should extend map locations (fort, harbour,
church, trading place) or object/ornament symbols (comb, coin, game piece, drinking horn).

## Latest Session — Leif's Map: Frame Pan, Guard Fix, Art Placed Correctly

**Session scope:** Leif's trail map only, continuing directly from Codex's decoration pass below.
Two connected pieces: panning the frame east per the user's request, and fixing three real defects
in how the six vignettes from that pass were actually sitting on the sheet.

### `PR-13` decided — frame panned one grid column east, same scale

User asked to pan the map one `PR-12` grid column right (map moves left) to trim the empty
Nunavik/Ungava Bay/Québec mass and bring Greenland fully into view. An Iceland-inclusive frame was
tried first and rejected in chat (Qikiqtarjuaq's label collided at that zoom, and two of Aud's
stops leaked onto Leif's sheet by name) before the user asked for the plain one-column pan instead.

**A real bug surfaced by actually building the literal request.** The stop-in-frame guard checks a
stop's raw longitude against the frame's nominal box; Qikiqtarjuaq (67.6°N) reads as just outside
that box after the shift and the guard correctly refused to build — but was wrong to refuse. A
conic projection's meridians converge toward the pole, so the point's real *projected* position
lands 1.83 in inside the printed map. Verified by projecting it, not by trusting either the
assertion or a relaxed copy of it. **Both frame guards (stops, region labels) were rewritten** to
check the projected page position against the printed map area instead of the raw coordinate
against the frame's lon/lat box — the real question was always where the point lands on paper.

The pan itself still cost one region label a real collision, unrelated to the guard question:
HELLULAND's label had to move (68.2,−68.6 → 68.5,−70.0) because its old spot now collided with
Qikiqtarjuaq's own label — caught by the stop-collision guard added in the grid session, exactly
the case it exists for. Bonus: Brattahlíð/Qassiarsuk — Erik the Red's estate, where Leif
historically sailed from — now falls inside the frame and labels for free from the existing corpus.

### Three defects fixed in the art Codex placed

1. **The ship (and iceberg, and polar bear) were made of glass.** Their sails/hull/rock faces had
   fully transparent interiors, so the `PR-12` reference grid printed straight through them. Fixed
   on the pixels, not by re-rendering: new `fill_art_alpha_holes.py` closes tiny linework gaps then
   fills every fully-enclosed transparent hole with a pale paper tone. The whale and settlement came
   back untouched — both are genuinely open line art with no enclosed body, not filled silhouettes
   with a bug. Source assets in `Art/` are untouched; the build now draws from `Art/processed/`.
2. **The longship was too large**, per direct user feedback — shrunk from 2.36 × 1.61 in to
   1.70 × 0.85 in.
3. **The wolf collided with the word "MARKLAND", and the settlement collided with "GRŒNLAND"/Nuuk.**
   The original placement checked distance from named *points* only; it never checked the actual
   footprint of a region label, which is wide (letter-spaced small caps). Re-placed both by a proper
   search: maximise clearance from the printed coastline, then require the candidate box to miss
   every reserved label box from a clean (art-free) build. Final clearances: bear 5.8°, wolf 1.9°,
   settlement 4.1° from the nearest coastline; all three also clear the drawn route by the usual
   26pt halo, and no two vignettes overlap each other.

All six re-verified after the frame pan: inside the printed map area, clear of the route corridor,
clear of every label, clear of each other. Stop-collision guard clean; the three collisions in the
build log (Makkovik, Red Bay, Rigolet) are decoys, checked by name against the route plan.

## Files Changed

- `NorseBackpack/TravelMap/build_trail_maps_pdf.py` — `TRAILS["leif"]` frame/lon0/regions/areas/
  waters/extra_towns updated for `PR-13`; both frame-validity asserts rewritten to check projected
  page position instead of raw lon/lat; `ART_DIR` repointed at `Art/processed/`; `LEIF_ART` boxes
  replaced (smaller ship, bear/wolf/settlement re-placed).
- `NorseBackpack/TravelMap/fill_art_alpha_holes.py` — new. Fills enclosed alpha holes in the six
  vignettes; `Art/processed/` is its output, regenerate after any new or replaced asset.
- `NorseBackpack/Norse_Brainstorm.html` — `PR-13` added as Decided; `PR-11` updated with what was
  actually built and the placement-search method; stale "Chosen for Leif" line (old Baffin/Nuuk
  positions) corrected to match.
- `output/pdf/Trail_Map_1_Leif_{Print,ANSWER,ART_GUIDE}.pdf` — rebuilt. Rollo and Aud rebuilt too,
  as a regression check on the shared guard code; both unchanged (still digits 9 and 7).

## Checks

- Guard clean on all three unblocked trails after the assert rewrite — confirms the fix didn't
  loosen anything for Rollo/Aud, only correct the projection-vs-raw-coordinate mismatch for Leif.
- Every one of the six vignette boxes checked programmatically post-placement: inside the printed
  map area, ≥26pt from the drawn route, zero overlap with any of the ~55 reserved label boxes from
  a clean build, zero overlap with each other.
- Before/after crops of the three alpha-filled assets (longship, iceberg, polar bear) rendered over
  a grid-line backdrop and inspected: interiors read as solid fabric/rock, hatching preserved as ink
  on top of the fill, no artifacts.
- Leif Print and ANSWER rendered at 180 dpi and inspected in full; ANSWER still reads as digit 1.
- Page opened in the in-app browser, Open questions tab clicked, `PR-13` and the rewritten `PR-11`
  read on screen; tag balance 693 `div` / 11 `section` / 19 `figure` / 8 `details` / 8 `table` /
  11 `svg` / 92 `li` / 158 `strong` / 138 `code` / 20 `em` / 84 `b`, all paired.
- Not run: true-size physical print of the new frame or the filled art; no test of whether the pale
  fill tone reads correctly once actually printed and laminated (extends `PR-09`'s open print test).

## Next Action

Print the current Leif sheet true-size and confirm the filled sail/hull/iceberg read as solid on
paper, not just on screen. Aud and Rollo still have no decoration pass — `PR-11` covers Leif only.

## Blockers and Open Items

- The Iceland-edge framing (lon −65.5..−23.0) was built and verified working but not adopted; kept
  only as a rejected option in this session's chat, not written to any file. Revisit only if the
  user asks for Iceland again.
- `fill_art_alpha_holes.py` is a manual re-run step, not wired into `build_trail_maps_pdf.py`'s own
  pipeline — if a new asset lands in `Art/` and the fill script isn't re-run, the build will happily
  draw the old `Art/processed/` copy or fail to find the new file. Worth wiring together later.
- Everything else carried over unchanged from the previous session below (Harald blocked, `PR-10`
  coordinate sourcing, Rollo's decoy thinning, `PZ-09` second jobs).

---

## Previous Session — Leif's Map: Balanced Treasure-Map Decoration

**Session scope:** Leif's trail map only. The user chose the balanced decoration option; no other
map or puzzle was changed.

### `PR-11` built — six restrained vignettes

Leif's sheet now carries a westbound longship in safe sea slot A, a breaching whale in B, and an
iceberg with floes in D. Three smaller land ornaments add the requested treasure-map character: a
polar bear on Baffin Island, a wolf in Labrador / Québec, and a three-building Norse-style cluster
beside Nuuk. The sea pieces remain inside the placement-guide boxes. The land pieces are drawn
under labels and reserve their own boxes before town-label placement, so a label moves rather than
printing through the art. No new settlement name or map point was invented.

All art is transparent PNG, placed at reduced opacity, and uses the existing dark green, grey and
muted rust palette. The exact final ImageGen prompts are recorded in the Design guide tab. A first,
more detailed whale generation was rejected; only the simplified final prompt and asset are part
of the project.

## Files Changed

- `NorseBackpack/TravelMap/Art/` — six new transparent vignette assets.
- `NorseBackpack/TravelMap/build_trail_maps_pdf.py` — Leif-only decoration placement, proportional
  image fitting, opacity and label-box reservation.
- `NorseBackpack/Norse_Brainstorm.html` — `PR-11` marked built / test print; chosen composition,
  placement rule and exact prompts recorded.
- `output/pdf/Trail_Map_1_Leif_Print.pdf` and `Trail_Map_1_Leif_ANSWER.pdf` — rebuilt with decoration.

## Checks

- Leif print and answer PDFs rebuilt; all 22 labels retained and no stop-label guard fired.
- Both one-page PDFs rendered at 180 dpi and visually inspected in full: artwork is transparent,
  the route corridor remains clear, labels remain readable, and the answer stroke stays dominant.
- Source script compiles; both PDFs reopen as one-page letter PDFs.
- HTML structural counts remain balanced: 688 `div`, 11 `section`, 19 `figure`, 8 `details`,
  8 `table`, 11 `svg`, and 1 `pre`.
- Not run: the in-app browser refused the local `file://` URL under its security policy, so the new
  Design guide card was not visually browser-checked and console errors could not be checked.
- Not run: true-size physical print. `PR-11` stays at **Built · test print** until icon detail and
  opacity are judged on paper.

## Next Action

Review the decorated Leif print PDF, then print one true-size copy. Check that the longship does not
dominate, the small bear/wolf/settlement remain recognizable, and the laminated wet-erase route is
still visually strongest.

---

## Previous Session — Leif's Map: the Reference Grid

**Session scope:** Leif's trail map only. The grid, the knock-on re-cut of the art slots, and the
Codex icon brief. No card file, no other puzzle touched.

### `PR-12` closed — a 9 × 11 lettered grid on every sheet

A–I across, 1–11 down, labels repeated on all four sides in a new 12 pt border band. Cells come out
0.84 × 0.86 in — visually square, and the division is **exact**, so there are no runt half-cells.

Four treatments were rendered on Leif's sheet and shown side by side before anything was written:
sea-only lattice, lattice over everything, band-only, and sea-only with a chart-style alternating
border. **User chose the lattice over everything.** Applied with one refinement: the grid is drawn
*over the land* (so a settlement can be given a square reference, which is the point of choosing
this variant) but *under every label*, so no printed line can sit on a clue. Verified at 300 dpi on
the densest cluster — Rigolet has a grid line behind it and still reads clean.

The grid belongs to the **sheet, not the geography** — all four maps carry the identical 9 × 11
whatever frame they use, so a square reference means the same place on the page every time. The
accepted cost is that a square is ~190 km on Leif's sheet and ~55 km on Aud's.

The old 5° degree graticule is **removed**; the grid replaces it. Recoverable from git if wanted.

### It re-framed every sheet, and that had consequences

The band takes 12 pt per side, so the projection rescales on all four maps. Two knock-ons:

1. **Every slot size in `PR-11` went stale.** Measured, not assumed: A 1.88 × 4.50 → 1.62 × 4.25,
   B 1.12 × 2.00 → 1.38 × 1.50, and so on. This is why the grid had to land before Codex was
   briefed, not after.
2. **Two more decoy labels now collide** — Caen and Falaise on Rollo, Krosshólaborg on Aud. Checked
   against the route plan: none is a stop.

That second point exposed a **real defect in the existing build guard**. It only caught stops
*missing from the corpus*; a stop whose label was dropped for collision would have passed silently
and been unfindable on the sheet. With the frame now tighter that is reachable, so the guard was
extended to cross-check `lab.skipped` against the stop names. Clean on all six sheets.

### `PR-11` — slots recut landscape

The greedy largest-rectangle search was maximising area and producing tall columns; against the new
frame the biggest was 1.62 × 4.25 in, which is the worst possible frame for a ship under sail. The
guide now constrains aspect to roughly 1.4:1–2.0:1 via a prefix-sum sweep over candidate sizes.
Result: five usable slots, A 2.50 × 1.75 in down to E 1.25 × 0.88 in. **A, B and C are contiguous**
in the Labrador Sea — filling all three would read as one block, so the brief says take two.

### Two collisions recorded rather than solved

- **Leif's sheet now carries two grids** — this one on the front, the hnefatafl setup on the back
  (`PZ-07`), whose registration instruction is literally "align on the grid lines". `PR-09` was
  extended: its print test now has to read *both* faces, since a front grid ghosting backwards would
  add noise to exactly the lines the offset registers against.
- **`ST-05`'s dig-site plan is gridded too.** Family resemblance or false lead — left open.

## Files Changed

- `NorseBackpack/TravelMap/build_trail_maps_pdf.py` — `BAND`, `GRID_COLS`/`GRID_ROWS`, map area
  inset; graticule block removed; grid drawn between the land fill and the labels; frame/corner-tick
  block replaced by the band and its references; stop-collision guard added.
- `NorseBackpack/TravelMap/build_art_placement_guide.py` — `largest_rects` replaced by
  `landscape_rects` (prefix-sum, aspect-constrained); docstring and legend updated.
- `NorseBackpack/Norse_Brainstorm.html` — `PR-12` added as Decided; `PR-11` slot figures replaced
  and the aspect change recorded; `PR-09` extended with the reverse ghosting direction.
- `output/pdf/` — all six trail-map PDFs rebuilt (`Trail_Map_{1,2,3}_*_{Print,ANSWER}.pdf`) and
  `Trail_Map_1_Leif_ART_GUIDE.pdf` regenerated.

## Checks

- All six sheets rebuilt; stop-label guard clean on every one.
- Dropped decoy labels cross-checked by name against `Norse_Aunt_Route_Plan.json`: Caen, Falaise,
  Hastings, Lewes, Salisbury, Southampton, Krosshólaborg are none of them stops.
- Leif, Rollo, Aud print sheets and Leif's answer key rendered and visually inspected. Leif also
  inspected at 300 dpi over the densest label cluster to confirm no grid line crosses a name.
- New slot figures taken from the guide's own printed output, not estimated.
- `Norse_Brainstorm.html` tag balance after the edits: 687 `div`, 11 `section`, 19 `figure`,
  7 `details`, 8 `table`, 11 `svg`, 92 `li`, 151 `strong`, 135 `code`, 20 `em`, 76 `b` — all paired;
  `br` void.
- Page opened in the in-app browser, Open questions tab clicked, `PR-11` and `PR-12` read on screen
  and confirmed rendering correctly. No console errors.
- Not run: no print test of the grid at true size; no test of whether the front grid ghosts through
  to the back of Leif's sheet (`PR-09`); the four grid variants were judged on screen, not in print.

## Next Action

Write the Codex icon brief into the Design guide tab and generate the art. Proposed set, **not yet
agreed**: longship under sail (two poses), a sea beast for the open Labrador Sea, ice floes for
Davis Strait, an ornate compass rose replacing the script-drawn one, and a title cartouche. Flat
screen-print, *not* the engraved cross-hatched style of the stamps — the map's own line work is
flat. Transparent PNG at 600 dpi minimum; anything with a baked background shows as a box on the
sea tint.

## Blockers and Open Items

- Harald's map still cannot build — "Sicily" and "Asia Minor" are regions with no endpoint.
- `PR-10`: every `APPROX` map coordinate still needs source-checking before a sheet is printed.
- Rollo's south-coast English cluster now drops six decoy labels, one more than before. No stop
  affected, but the list still wants thinning down there.
- The red acetate filter and the UV pen/blacklight remain on the decided tool list with no puzzle
  feeding them.
- `PZ-09`: Aud, Rollo and Harald still need their second job chosen.

---

## Previous Session — Props: Hnefatafl, the Four Maps, the Dig Site

**Session scope:** the prop side, while Codex worked the cards in parallel. No card file was
touched. Four connected pieces: the hnefatafl puzzle, the final map mechanic, the printable maps
themselves, and the dig site.

### 1. `PZ-01` closed — hnefatafl at three moves

A commercial set forces three changes: board size (built for 7 × 7 Brandubh; 9 × 9 and 11 × 11 are
commoner), piece count (a stock 7 × 7 gives 12 non-king pieces against this layout's 14 blockers),
and the readout — nothing can be printed on a bought board. The real cost is the throne
compartment, which no commercial set can have (`PR-08`).

Decided: **three moves**, and the code is **how far the king travels on each leg**. D4 → F4 → F7
→ G7 measures 2, 3 and 1 → `231`. Works bought or built, and retires the objection that digits on
a game board announce it as a puzzle prop.

### 2. `PZ-07` opened — the board setup split across two papers

Liv wrote the piece positions on the back of a trail map; the museum pamphlet was pressed onto wet
ink and lifted the right-hand strip, leaving an illegible smear on the map and a **mirrored** copy
on the pamphlet's blank end panel. The pamphlet is an invented **Hnefatafl Museum, Oslo** leaflet
that also carries the simplified rules, so rules arrive as printed matter and Liv's handwriting
keeps its single job. Verified rather than assumed: the full board has exactly one three-move
escape, but assuming the hidden strip empty yields **18** candidate routes — the puzzle refuses to
resolve instead of resolving wrongly. A three-panel sketch is embedded in the Design spec tab.
**Later in the session the map was chosen: Leif's** (see 6).

### 3. `PZ-06` closed — four laminated letter sheets, wet-erase marker

Printed and laminated at home, gloss pouches, cards laid beside each map in date order, legs drawn
onto the laminate. No pins, cord or overlay.

**Pinned cards was eliminated on geometry, not preference** — the finding worth keeping. Rouen and
Roumare are 10 km apart on a 624 km trail, so they fall 0.13 in apart on letter and still only
0.38 in apart on a 24 × 36 poster. No printable size separates them enough for two postcards.

### 4. The printable maps — built

`NorseBackpack/TravelMap/build_trail_maps_pdf.py` builds all four sheets plus answer keys from one
script, so a key cannot drift from the sheet it answers. Natural Earth 50m coastlines from the
vendored `land.js`, Lambert conformal conic, explicit per-trail frames, postcard palette.
Settlement labels come from `stops.js`, the 72-entry sourced research corpus, so the decoys are
other places from Liv's own research.

Built: **Leif, Rollo, Aud** — print sheets and answer keys. **Harald is blocked** and the script
refuses it: stops 5 and 6 are "Sicily" and "Asia Minor", regions with no endpoint to draw to.

Answer keys confirm the shapes. **Aud's 7 is clean. Rollo's 9 works well** — the Rouen/Roumare
10 km gap turns out to be what closes the loop. **Leif's 1 is confirmed weak**: a single straight
stroke with a stub where L'Anse and Battle Harbour nearly coincide. It survives on the two
backstops only (one lock left, `1972` parses as a year). Worth a play-test early.

### 5. Leif's stops fixed — regional anchors replaced

The route plan had "Markland candidate" and "Helluland candidate" as *regional anchors*, while
postcard 02 is Battle Harbour. With stops unmarked, players locate each stop by name, and a saga
region the size of Spain has no endpoint. Now `l-meadows → l-battle → l-qikiqtarjuaq`.
Qikiqtarjuaq was chosen from four Baffin candidates: most upright long leg (16° off vertical) and
the east-coast approach a ship following the coast would make.

`stops.js` was **left alone** — it is the historical corpus, and Markland/Helluland remain valid
research entries there. Only Liv's itinerary moved. This created a trap that was caught and fixed:
the page's mini-maps resolve IDs against that corpus with `.filter(Boolean)`, so the two new IDs
would have **silently vanished** — three pins quietly becoming one. A supplement now merges
itinerary-only stops into the lookup.

### 6. Map presentation decisions

- Title block **stripped to the title alone**. Cut: the trail name and "Map n of four" (they
  pre-sorted the deck and handed over the digit order), the find-them-by-name instruction
  (designer's voice, not Liv's), the `stops unmarked by design` note, and finally the
  projection/coastline credit. Natural Earth is public domain and asks for no attribution;
  provenance stays in the script and `TravelMap/README.md`.
- `PZ-08` **decided**: the digit order is the postmark dates — sort the deck, the order each trail
  first appears is its digit's order. Composes with the interleaving decision instead of fighting
  it. **Constrains the unwritten dates**: earliest card per trail must fall Leif → Rollo → Aud →
  Harald or the code is not `1972`. Wants a script once the 18 dates exist.
- `PZ-09` **new principle**: every map earns at least one job besides the endgame. Leif decided
  (board setup on the back, which also settles `PZ-07`'s map question). Aud, Rollo, Harald are
  candidates — Aud's is nearly free, since `Kambsnes` is already labelled and `PZ-03` proposes
  `KAMBR` for the five-letter lock.
- `PR-11` **new**: map decoration is Codex's lane.
  `NorseBackpack/TravelMap/build_art_placement_guide.py` computes where art may legally go — sea
  clear of the route corridor, every label box and the title furniture. Leif's four slots: A 1.88
  × 4.50 in, B 1.12 × 2.00 in, C 1.38 × 1.62 in, D 0.75 × 1.75 in. **Re-run the guide after any
  route change**; the corridor moves with the stops.

### 7. `ST-05` opened — the dig site

The ticket and closing letter already say Norway, so Aud's Iceland map cannot locate it. Proposed:
a fifth letter sheet, Liv's gridded **excavation site plan**, in the last container with the
ticket. Real digs use lettered/numbered grids, it keeps the four trail maps clean, and it has
metres-per-square resolution where a grid on Harald's 2,800 km map would be ~200 km per square.
Its job is explicitly **not** a puzzle — pure payoff plus one optional, ungated noticing-reward,
the only thing in the bag that would make the closing line a payoff rather than a compliment.

## Files Changed

- `NorseBackpack/Norse_Brainstorm.html` — `PZ-01`, `PZ-06`, `PZ-08` closed as Decided; `PZ-07`,
  `PZ-09`, `PR-08`, `PR-09`, `PR-10`, `PR-11`, `ST-05` added or extended; Design spec hnefatafl
  section rewritten with an embedded sketch; both affected `puzzles` JS entries rewritten;
  Prototype board's printed digits removed and its messages switched to leg lengths; Options tab
  candidates unblocked or struck through; Props & choices updated; `routeMapPlans` and the static
  route list updated for Leif's new stops.
- `NorseBackpack/TravelMap/build_trail_maps_pdf.py` — new. All four maps plus answer keys.
- `NorseBackpack/TravelMap/build_art_placement_guide.py` — new. Legal art areas for Codex.
- `NorseBackpack/TravelMap/Norse_Aunt_Route_Plan.json` — Leif's stops 2 and 3 replaced.
- `NorseBackpack/TravelMap/README.md` — Leif's route line rewritten with the reasoning.
- `output/pdf/` — `Trail_Map_1_Leif_{Print,ANSWER,ART_GUIDE}.pdf`,
  `Trail_Map_2_Rollo_{Print,ANSWER}.pdf`, `Trail_Map_3_Aud_{Print,ANSWER}.pdf`.
- Deleted `NorseBackpack/TravelMap/build_trail_map_leif_pdf.py`, folded into the general builder.

## Checks

- Tag balance after every edit round; final 682 `div`, 92 `li`, 151 `strong`, 129 `code`, all
  paired; `br` correctly void.
- Exhaustive board search run twice (full layout 1 solution; hidden strip assumed empty 18). The
  `231` legs were read off the verified route.
- Great-circle distances and sheet-area arithmetic computed from the route JSON, not estimated.
- Every PDF rendered and visually inspected. Leif's print sheet re-checked by text extraction
  after the credit removal: no "Lambert"/"Natural Earth" string remains, title intact.
- Build-time guards added and **they caught real defects**: four stops would have been unlabelled
  and therefore unfindable; `ÍSLAND` was placed outside its own frame and silently never drew.
- Simulated `byId` stop resolution against the real 72-entry corpus: all four trails resolve.
- Defects found and fixed mid-session: `height="auto"` invalid on `<svg>` collapsed the page below
  the sketch; auto-framing zoomed Leif out to 33° of mostly empty ocean and was reverted to
  explicit frames; `ENGLAND / England` printed the same word twice.
- **Two invented place names reached a rendered sheet.** "Reyðhol" and "Hvammsýla" are not real
  Icelandic places — faulty recall, caught only on visual inspection. Removed; Reykholt was the
  real place being garbled. This is why `PR-10` exists: every `APPROX` label needs source-checking.

Not run: no check of what hnefatafl sets are actually for sale (`PR-08` figures are general,
listings unverified). No print test of the offset, the smear, the laminated maps, or the
back-of-map grid show-through (`PR-09`). The pamphlet's historical text is unchecked (`HI-05`).
No play-test that the drawn shapes read as `1972`. The Leaflet mini-maps could not be seen
rendering — the preview pane serves the page as a `data:` URL so the vendor scripts do not load
and `initRouteMaps` guards out; resolution logic was verified against the real data instead.

## Next Action

Settle `PR-08` — bought board versus built — since the hnefatafl layout, the map/pamphlet split
and whether the throne compartment exists at all are downstream of it. Checking real listings for
a 7 × 7 Brandubh set is the concrete first step.

## Blockers and Open Items

- **Harald's map cannot build** until "Sicily" and "Asia Minor" become named settlements. Same
  treatment Leif just had.
- `PR-10`: every `APPROX` map coordinate needs source-checking before a sheet is printed for play.
- Rollo's south-coast English cluster drops five decoy labels to collision; no stops affected, but
  the list wants thinning down there.
- The red acetate filter and the UV pen/blacklight are still on the decided tool list with **no
  puzzle feeding them**. Flagged at the start of this session and still true; `ST-05`'s optional
  find is one candidate job for the UV pen.
- `PZ-09`: Aud, Rollo and Harald still need their second job chosen.

---

## Previous Session — Physical Registration Test

The previous session (Codex, below) left one open unknown: whether ordinary printer scaling
and hand-trimming were accurate enough for the 12-px-wide `1576` half-digits to actually
register when Card 02 is rotated and butted against Card 03.

Reviewed Codex's work first: inspected both fronts at normal size (digits genuinely invisible),
zoomed into the four digit positions on `Postcard_02_Battle_Harbour_Front.png` (found the marks
sit right at the top pixel rows, essentially zero safety margin before trim — a real risk worth
flagging, though Codex's own handoff already named this as the next unknown), and confirmed the
alignment preview images render correctly with no HTML regressions.

Built `NorseBackpack/Postcards/build_topedge_test_sheet.py` — a standalone script (not touching
the real card builds) that crops just the top ~1.2 in of each front at the same 256 dpi the
final cards use, lays them on one small PDF sized for a 100%-scale print, with a "cut here = true
top edge" line on each strip and a 6.00 in reference ruler to catch silent printer rescaling.
Output: `output/pdf/Postcard_02_03_TopEdge_Test.pdf`. Sent to the user to print and test by hand.

**User printed it and confirmed: it works.** The zero-margin risk did not materialize in
practice. This closes the open question from Codex's "Next action" below — no further print
testing needed before finalizing these two fronts.

Files changed this session: `NorseBackpack/Postcards/build_topedge_test_sheet.py` (new),
`output/pdf/Postcard_02_03_TopEdge_Test.pdf` (new, test artifact). Also removed four stray
`_qa_*.png` scratch crops from `NorseBackpack/Postcards/` left over from the review.

Next action: the front-art mechanic is now physically validated. Move on to writing and
building cards 02 and 03's backs (Fun Fact + handwritten message, same structure as card 01's
rebuilt layout) — drafts exist in this session's chat log but were not yet written to any file.

---

## Previous Session — Codex, Front Art

**Session scope (Codex):** make the current Card 02 Battle Harbour and Card 03 Baffin Island fronts
full bleed, then hide a split `1576` along their top edges so rotating Card 02 by 180 degrees
and butting the two top edges together reveals the code.

Done:

1. Reframed both 1536×1024 illustration sources with a uniform ~3% crop so the existing
   screen-print artwork reaches every edge without inventing new scenery or changing the palette.
2. Added four 12-pixel-wide complementary half-digits at fixed centres (x = 384, 640, 896,
   1152). Card 02 uses mirrored source positions and pre-inverted marks; after rotation they
   register with Card 03 as `1576`. Pale, distressed ink makes them read as cloud flecks.
3. Regenerated both titled front PNGs and the two individual print PDFs plus the full postcard
   PDF. Updated the source register's existing `Change:` lines and recorded the decided mechanic
   in the Postcards tab.
4. Added an expanded alignment preview to the Postcards tab: the complete cards in their play
   position plus a 4× seam detail. Both preview images are stored with the postcard assets.
5. User then increased the digit width from 6 to 12 pixels. Regenerated both fronts, the
   alignment images and all three affected PDFs without changing the fixed centres. User
   reviewed the updated HTML preview and confirmed the result is good; this session is complete.

Files changed by this session:

- `NorseBackpack/Postcards/Postcard_02_Battle_Harbour_Illustration_v1.png`
- `NorseBackpack/Postcards/Postcard_03_Baffin_Island_Illustration_v1.png`
- `NorseBackpack/Postcards/Postcard_02_Battle_Harbour_Front.png`
- `NorseBackpack/Postcards/Postcard_03_Baffin_Island_Front.png`
- `NorseBackpack/Postcards/Postcard_02_03_Aligned_Preview.jpg`
- `NorseBackpack/Postcards/Postcard_02_03_1576_Alignment_Proof.png`
- `NorseBackpack/Postcards/References/README.md`
- `NorseBackpack/Norse_Brainstorm.html`
- `output/pdf/Postcard_02_Battle_Harbour_Print.pdf`
- `output/pdf/Postcard_03_Baffin_Island_Print.pdf`
- `output/pdf/Norse_Postcards_Full_Print.pdf`

Checks:

- Inspected both full-size illustration sources and titled fronts: full bleed, composition and
  title hierarchy preserved; half-digits are effectively invisible at normal size.
- Built a 4× nearest-neighbour seam proof from rotated Card 02 plus upright Card 03. It reads
  `1576`, and the four centres align exactly.
- Rendered the affected PDF fronts at 150 dpi and inspected them. Full-set pages 3 and 5 are
  byte-identical to the corresponding individual rendered fronts.
- HTML tag balance remains valid after the preview addition: 639 paired `div`s, 11 paired
  `section`s, 18 paired `figure`s and 7 paired `details` elements.
- Browser visual check of the Postcards tab could not run: this session's in-app browser policy
  blocked the local `file://` URL. Source structure and the displayed image assets were checked.

Next action: print the two fronts at final size, trim consistently, and physically test the
top-edge registration. The code is 12 pixels wide per digit, so printer scaling and trim
tolerance are the remaining unknowns.

## Previous Session (retained because its changes are still uncommitted)

**Session scope:** rework the postcard back-of-card structure (from the new mockup slide in
`Norse_Ideas.pptx`), close the resulting open question, write and build card 01 as the template
card, then flip Leif's trail order so L'Anse aux Meadows is genuinely first. Four connected
pieces of one continuous session, not a whole-game review.

Done, part 1 — structure rework:

1. Read the new "Postcard design" slide in `Norse_Ideas.pptx` (via its raw slide XML — no
   LibreOffice in this environment) and proposed the change in chat first: the mockup's "Fun
   fact" box is a rename/relocation of the existing printed-caption zone, not a new one; its
   voice was initially left to vary per card (typed or handwritten).
2. Reworked the "Four zones" schematic in the Postcard system tab to match: handwritten note
   full-height on one side; stamp, shrunk address, and a titled "FUN FACT" block stacked on the
   other. Renamed "printed caption" &rarr; "Fun Fact" everywhere it refers to this zone. Widened
   the diagram's viewBox 840&rarr;920 to stop legend text clipping (pre-existing issue, fixed
   while the figure was already being redrawn).
3. Logged `PC-12`: letting Fun Fact's voice vary per card meant her handwriting could carry two
   different jobs (trivia and task) on one card with no visual tell between them.

Done, part 2 — closing PC-12 and building card 01:

4. User decided PC-12 always-typed. Updated the voices panel, diagram legend/figcaption, and
   verb D; closed `PC-12` as **Decided**.
5. Settled Fun Fact content for card 01 (L'Anse aux Meadows): the butternut-wood find (real,
   verifiable, ties naturally to the sagas' "Vinland"), per the user's steer away from
   number-bearing trivia.
6. User kept the existing handwritten letter on card 01 exactly as written, including "the first
   stop on my journey." This originally led me to close `PC-08` on a reinterpretation (see part 3
   below for why that reinterpretation was superseded).
7. Rebuilt `NorseBackpack/Postcards/build_postcard_01_pdf.py`'s back-of-card layout: address
   block shrunk into a bordered box, a new bordered, titled "FUN FACT" block added underneath it
   with the butternut-wood text (typeset). Front card and handwritten message untouched.
8. Regenerated `output/pdf/Postcard_01_LAnse_Print.pdf`, `output/pdf/Postcard_01_LAnse_Letter_
   Print.pdf`, and `NorseBackpack/Postcards/Postcard_01_LAnse_Back.png` (1500×1050) from the
   rebuilt script. First render had the "Canada" address line overflowing into the Fun Fact
   title — found and fixed by resizing both boxes, re-rendered clean.
9. Updated the Postcard system tab's "first-card layout prototype" note, job 2's card text, and
   the Next steps list to reflect card 01 as done.

Done, part 3 — flipping Leif's trail order:

10. User decided L'Anse aux Meadows should genuinely be first on Leif's trail, superseding my
    earlier PC-08 reinterpretation ("first stop" = first postcard sent). Flipped the trail
    instead of the sentence.
11. Edited `TravelMap/Norse_Aunt_Route_Plan.json`: `routes.leif` and `visits.leif` reordered and
    renumbered to L'Anse aux Meadows (1) &rarr; Markland (2) &rarr; Helluland (3). Markland stays
    in the middle position, so only the two ends actually moved.
12. Swept every other place this order appears: `TravelMap/README.md`'s candidate-plan summary;
    the Postcard system tab's coverage-matrix column labels *and* the per-column "jobs besides
    the maps" digit row (the doubled-job "2" had to move with the L'Anse column — caught this by
    checking the actual x-coordinates, not just the header labels); the Travel routes tab's
    route summary line and its static `<ol class="route-stops">` list; and the page's embedded
    `routeMapPlans` JS object that drives the live Leaflet mini-maps. Rewrote `PC-08` to record
    the actual fix (route flipped, not the sentence reinterpreted).
13. Did **not** change the decorative static SVG route-shape polylines (digit "1" shape, card 01
    hold-to-light figure, etc.) — connecting the same three points in reverse order draws an
    identical line, so nothing to fix there.

## Files Changed

- `NorseBackpack/Norse_Brainstorm.html` — Postcard system tab (diagram, terminology, PC-08 and
  PC-12 register entries, next steps, job-2 card text, coverage-matrix labels and digit row) and
  Travel routes tab (route summary text, ordered stop list, embedded `routeMapPlans`).
- `NorseBackpack/Postcards/build_postcard_01_pdf.py` — back-card layout: address box shrunk,
  Fun Fact block added with the butternut-wood text; new `FUNFACT` colour constant.
- `NorseBackpack/Postcards/Postcard_01_LAnse_Back.png` — regenerated.
- `output/pdf/Postcard_01_LAnse_Print.pdf`, `output/pdf/Postcard_01_LAnse_Letter_Print.pdf` —
  regenerated.
- `TravelMap/Norse_Aunt_Route_Plan.json` — Leif's trail order flipped.
- `TravelMap/README.md` — candidate-plan summary updated to match.
- `NorseBackpack/Norse_Ideas.pptx` — read only (slide 5 XML), not edited. Was already showing as
  modified in git status at session start (the user's own edit adding that slide); still modified.

Not touched: `Postcard_01_LAnse_Front.png`, the other postcards, `TravelMap/stops.js` (a flat
lookup table, not order-dependent), `TravelMap/map.js`, the stamp artwork, and anything on the
uncommitted Aurora side.

## Checks

- Element balance in `Norse_Brainstorm.html` after all edits: 638 `<div>`/`</div>`, 11
  `<section>`/`</section>`, 16 `<figure>`, 10 `<svg>`, 8 `<table>` — all paired.
- `Norse_Aunt_Route_Plan.json` validated as parseable JSON after the reorder.
- Visual check in-browser: Postcard system, Travel routes and Open questions tabs render
  correctly, no console errors. Confirmed the coverage-matrix column swap and the digit-row fix
  by reading the actual on-screen numbers, not just trusting the label swap. Confirmed the
  Travel routes tab's static ordered list reads L'Anse &rarr; Markland &rarr; Helluland via
  `get_page_text` (the in-app browser's `find` missed it over a smart-apostrophe mismatch — not
  a real issue, just a tool quirk).
- The Travel routes tab's *live* Leaflet mini-maps did not render in this browser tool (blank
  grey boxes, no console error) — the page loads via a `data:` URL in this preview tool, which
  has no base URI, so the relative `<script src="TravelMap/vendor/...">` tags can't resolve.
  Same limitation seen earlier this session with the postcard preview HTML's relative `<img>`
  tags. Not a real defect — verified correctness at the source level instead (the embedded
  `routeMapPlans` array and the underlying JSON are both updated and consistent). If a future
  session needs to see the live map actually render, open it from a real `file://` path or a
  local server rather than this tool's snapshot preview.
- Visual check of the rebuilt card: rendered both PDF pages and the two-up letter sheet to PNG
  with PyMuPDF (`fitz`) at print resolution and inspected them directly.
- **Not run:** LibreOffice (`soffice`) is not installed in this environment, so the pptx skill's
  normal slide-image QA path is unavailable — the mockup slide was read from its raw XML instead.
- Not run: a source check of the butternut-wood fact, or a print test of the rebuilt card.

## Next Action

Write the remaining 17 Fun Facts (`PC-07`, 1 of 18 done) and postmark dates (`PC-03`/`PC-04`)
using card 01 as the template. Card 01's postmark should date **first** on Leif's trail now, not
last — worth double-checking when dates are assigned. After that: build the continuation set on
paper, then solve family D (`PC-05`).

## Blockers and Notes

- Nothing is blocked on a purchase.
- Working tree is not clean: `NorseBackpack/Norse_Ideas.pptx` was already modified before this
  session started (the user's own edit) and remains modified. This session's changes to
  `Norse_Brainstorm.html`, `build_postcard_01_pdf.py`, the regenerated PDFs/PNG,
  `Norse_Aunt_Route_Plan.json`, and `TravelMap/README.md` are also uncommitted. Not committed or
  pushed — user has not asked for that yet.
- If a future session needs to visually QA a `.pptx`, install LibreOffice first, or read the
  slide XML directly as done here. If it needs to see the live Travel Map render, don't rely on
  this tool's `data:`-URL snapshot preview for pages with relative script/image references.
