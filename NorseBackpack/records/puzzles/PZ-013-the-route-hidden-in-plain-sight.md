---
id: PZ-013
title: The route hidden in plain sight
type: puzzle
# idea | candidate | decided | built | parked
status: decided
# The structure beat this puzzle belongs to (one ID)
beat: ST-006
# Props the player needs, e.g. [PP-001]
props: [PP-001, PP-002, PP-003, PP-004, PP-005, PP-006, PP-007, PP-008, PP-009, PP-010, PP-011, PP-012, PP-013, PP-014, PP-015, PP-016, PP-017, PP-018, PP-019, PP-020, PP-021, PP-022, PP-029, PP-032, PP-030, PP-034, PP-039, PP-024, PP-031, PP-033, PP-036]
# Puzzles that must be solved first, e.g. [PZ-002]
needs: [PZ-001, PZ-002, PZ-003, PZ-004, PZ-005, PZ-006, PZ-007, PZ-008, PZ-009, PZ-010, PZ-011, PZ-012]
# cipher | physical | search | logic | wordplay | other
mechanic: logic
# 1 (easy) to 3 (hard)
difficulty: 2
# Lock it opens: 3-digit | 4-digit | 4-letter | 3-digit-colour (blank if none)
lock: 4-digit
answer: 1972
envelope_marks: ᛈᛚᚹᛉ
# Compartment this lock closes (shown on the Locks tab)
container: Envelope 13
reset_display: 0000
# What players call this lock on the hint page, e.g. "The luggage tag" (spoiler-free)
hint_title: Just opened ᚲᛟᛉᛏ
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
tags: [old-PZ-18, old-PZ-06, old-PZ-08]
---

## How it works

Twenty-two cards, four of them decoys. Filter, sort, trace, and read the four shapes as four digits.

Lock 13 of 13 in the release order decided 7 Oct 2026 (Q-005). Difficulty 3 of 3 is Claude's estimate from the mechanism (number of props and steps), not playtest data.

**9 Oct 2026 (designer, Q-001):** now lock 13 of 13. Compartment: inside lockable pocket 2.

**11 Oct 2026 (designer, PR-007):** no locks or pockets any more. This code, set on the rune cypher wheel (PP-047), points to envelope 13, which holds what lock 13 used to close.


**12 Oct 2026 (designer, Q-054, after playtest 1):** **the finale no longer sends players back to the card text.** Playtest 1 found reconstructing the order from postcard sentences and ticket dates too complicated. Now:
- **Decoys carry no mark** (they had a horned helmet or a double axe).
- **The marks give the order.** On each trail the n-th stop carries the n-th element in the journal page's caption order (`Postcards/postcard_marks.py`). The page now says so: “To retrace my steps, follow only the places that carry one of our family's marks. / On each journey I met them in the order written under each drawing.”
- **The marks are crops of the page's own drawings** (`Art/FinalPuzzle/build_iconography_marks.py`), so a card matches the page at a glance.
- **Each map shows its journey's stamp** in the title band (`TravelMap/build_trail_maps_pdf.py`, `TRAIL_STAMPS`).

The code stays **1972**: the trail order and the stops are unchanged, only how players find the order. The order-reconstruction clue set (ticket dates, card statements, `Tools/final_riddle_solver.py`) is no longer needed to solve. Q-055 (decided the same day): the journal's Travel highlights are cut; the transition tickets stay as story. Difficulty is now about 2 (Claude's estimate), not 3.

**17 Oct 2026 (designer, Q-062): the order comes from tickets again, the filter from one raven.** Stop order within a journey now comes from the hop tickets (decoys included, PP-039); journey order from the three flight bookings. A raven mark on the real cards (none on decoys) filters the decoys, with Liv's note "retrace only the steps relevant to our family history". The crest and the six-element order no longer apply; the hint and solution text below about the journal's caption order are superseded once the new props are built. The code stays 1972. Retest needed.

## Player notices
**17 Oct 2026 (designer, Q-062):** the 22 postcards (18 carry Liv's small raven, the 4 decoys none), the four maps (each with its stamp), the 18 hop tickets (one page per journey, stops chain from one to the next, decoys included), ~~the three flight tickets between journeys~~ (dropped 20 Oct 2026; every hop ticket is dated), and H6's note about the family icon.

**Superseded 17 Oct 2026:** the journal page with the family iconography (symbol, crest, caption order) as the way to order the stops.

**12 Oct 2026 (Q-054):** the 22 postcards (18 carry a family mark, the 4 decoys carry none), the four maps (each now shows its journey's stamp), and Liv's journal page with the family iconography.

**Superseded 12 Oct 2026:** All 22 postcards (18 real stops plus one decoy per trail), four laminated letter maps, a wet-erase marker, and the note in the final bundle carrying the family logo and crest. (8 Oct 2026: no wet-erase marker for now, PP-042 parked; players imagine the routes or trace them with their fingers on the maps.)

**19 Oct 2026 (designer):** every hop ticket and booking now carries a departure date (PP-039, 8 Sep to 12 Dec 2025). The stop order still comes from chaining the routes; the dates also confirm it. Code stays 1972. Retest needed.

## Player does
**17 Oct 2026 (designer, Q-062):** set aside the four cards with no raven. Put each remaining card beside the map with the same stamp. Chain the journey's travel tickets (decoys included) to get the stop order, then join the raven stops in that order on the map. Each map traces one digit; ~~the flight tickets give the order of the four journeys~~ the ticket dates give the order of the four journeys (20 Oct 2026).

**Superseded 17 Oct 2026:** order by the marks on Liv's journal page (the crest and symbol caption order).

**12 Oct 2026 (Q-054):** set aside the four cards with no mark. Put each remaining card beside the map that shows the same stamp. On each map, order the cards by their marks, in the order Liv's journal page lists them under each drawing (symbol: raven, longship, sun-wheel; crest: bearded axe, round shield, wolf, anchor, drinking horn, valknut), and join the stops in that order. Each trail traces one digit. Nobody needs to reread a card's text.

**Superseded 12 Oct 2026:** Use the crest/logo filter to drop the four decoys. Sort the rest by stamp series to find which trail each belongs to, lay each trail’s cards beside its map in reconstructed order, then draw the legs straight onto the laminated map.

## Player obtains

Code **1972**. Opening this lock releases PP-043, PP-044.

## Story reason

The cards work first as story and individual clues, then return as the final meta-puzzle. Every place name gains a second meaning.

## Clue wording

“I crossed an ocean to find where we began. Every stop mattered. Now you have the whole journey.”

## Hints
1. Liv wrote to retrace only the steps that matter to your family's history. Only the postcards with her small raven count. Four cards have no raven: set them aside.
2. Each map shows the stamp of its journey. Put each postcard beside the map with the same stamp. The travel tickets show how Liv got from each stop to the next, so use them to put each journey's stops in order.
3. On each map, join the raven stops in that order, skipping any stop without a raven. Each map draws one digit. The dates on the travel tickets give the order to read the four maps.

## Solution
Set aside the four postcards with no raven. Match the rest to the maps by their stamps. Chain each journey's travel tickets (each goes from one stop to the next) to put its stops in order; the decoy stops appear on the tickets too, so skip any whose postcard has no raven. On each map, join the raven stops in that order: Leif's map draws **1**, Rollo's **9**, Aud's **7** and Harald's **2**. The ticket dates put the journeys in order: Leif (September), Rollo (late September to mid October), Aud (late October), Harald (November to December): **1972**.

## Solution notes

Design-side solution text, kept when the player-facing Solution above was written for the hint page (9 Oct 2026).

Leif draws **1**, Rollo’s family line **9**, Aud **7** and Harald **2** — candidate code **1972**, in trail-first-appearance order. Order is reconstructed from ticket dates, postcard statements and the final bundle — never from anything printed on a card, since postmarks carry no date at all. **Superseded 19 Oct 2026:** tickets now carry dates (PP-039); order is still solved by chaining the routes.

## Open risks

**Shapes not proofed at true print size** — the family **9** is the riskiest. A traced shape reads the same forwards and backwards, and 3-stop trails barely constrain the drawing. `1972` reads as a year, which self-checks but invites year-guessing. Harald’s **2** currently reads as a zigzag, which weakens the self-check.

## Releases (as worded on the old page)

**Superseded 9 Oct 2026** by the compartment map in Q-001; the current release list is under Player obtains.

The last container — plane ticket and closing line

Lock as recorded: Four-digit padlock on the last container. Old page status: Decided in principle · 4 of 4 maps built.

The full itinerary, evidence model and solver notes are still on the archived page: [Final riddle tab](../Norse_Brainstorm.html#view-final-riddle).

## Design notes (PZ-013: Mechanism, itinerary and clue set decided, 17 Sept 2026)

**Final riddle v2: decoy postcards, crest/logo filter and order reconstruction — see the [Final riddle tab] for the full mechanism.**

Replaces old page PZ-11’s held-back cards and the plain postmark-date sort referenced in PZ-013/Q-013.
**Closed, 17 Sept 2026:**
• ~~Dated vs. undated decoys (22 vs. 18 calendar slots).~~ **Moot** — the slot grid is retired. All 22 cards sit in one sequence; decoys occupy positions like any other card.
• ~~The three symbol elements, six crest elements, and the two fake elements.~~ **Revised, 19 Sept 2026:** the real elements are unchanged; the fake Mjölnir and crown are superseded by a horned helmet (Leif/Aud) and double-sided axe (Rollo/Harald). All eleven hand-drawn marks are built under PP-041.
• ~~A decoy city per trail.~~ **Decided, 15 Sept 2026:** Leif = Brattahlíð/Qassiarsuk, Rollo = Walcheren, Aud = Bjarnarhöfn, Harald = Constantinople.
• ~~Aud has no museum ticket to anchor a calendar date.~~ **Resolved** — Aud’s Treasure Museum ticket (PZ-006) is dated 13 Apr, and it carries the one relation the four tickets still prove: Aud first-appears before Harald.
• ~~The constraint-grid solver — not started.~~ **Built and run**, 17 Sept 2026: `NorseBackpack/Tools/final_riddle_solver.py` plus `final_riddle_clues.py`. Tests 1, 2 and 4 pass. Re-run it after any change to a clue, a card’s text or the itinerary.
• ~~The 22 dates.~~ **Decided** — a 2 Feb to 15 Dec travel year with variable stay lengths, in the Final riddle tab. Supersedes the 3-day slot grid and the 1 March–3 May window, which could not survive variable stays: re-run under the weaker semantics the old clue set gave 18+ answers. **Superseded 19 Oct 2026 (designer):** one calendar, 8 Sep to 12 Dec 2025, stops of 1 day to 1 week, in PP-039 and `Props/Tickets/ticket_dates.py`.
• ~~The five one-clause edits to already-built cards.~~ **Applied and rebuilt, 17 Sept 2026** (R1, R2, R6, H1, H4) — wording in Q-019. The solver was re-run afterwards and the answer is still unique.
**Still open:**
• Which specific element sits on which real stop’s card — 18 real-card assignments, and the only thing still blocking the endgame. The four decoy assignments are fixed by the two shared fake pairs.
• The element mark’s physical form (wax seal? picture-border mark?) and its legibility test at card size under table lighting. Deliberately not UV.
• Validation test 3 — no decoy-inclusive answer draws a plausible digit. Geometric, needs each decoy plotted on its trail’s real map projection; the solver cannot answer it. Note the tension with “Guessing risks”, which wants each decoy to draw a *plausible* wrong digit so the shape cannot be eyeballed off the map. One of the two has to give.
• The four decoy cards’ text (LD and RD are built; AD and HD are not).

## Design notes (PZ-013: Decided)

**The final map mechanic: laminated letter prints, drawn on with wet-erase marker.**

**Four letter sheets, printed and laminated at home.** Players sort the deck by stamp, lay each trail’s cards out beside its map in date order, and draw the legs straight onto the laminate. No pins, no cord, no overlay. Wipe to reset.
**Pinned cards is eliminated on geometry, not preference.** Rouen and Roumare are 10 km apart on a trail spanning 624 km, so they land 0.13 in apart on a letter sheet — and still only 0.38 in apart on a 24 × 36 poster. Two 5-inch postcards cannot occupy that gap at any printable size. Separately, six cards need 105 in² against a letter sheet’s 84 in² of printable area.
**Footprint is fine:** four letter sheets laid 2 × 2 come to about 17 × 22 in, roughly 1.4 × 1.8 ft, leaving a normal table clear for the cards and props. Larger shop-printed and laminated maps (tabloid at about 1.8 × 2.8 ft for the set) stay available if the drawing ever feels cramped, but they end free same-day reprints.
**Specs:** gloss pouches, since matte takes marker unevenly, and **wet-erase** rather than dry-erase — dry-erase smears under a palm resting on a sheet being drawn across, and ghosts if left for days. A laminating pouch also covers both faces at once, which is what PZ-008 needs for the map whose back carries the board setup. 5 mil pouches over 3 mil for a sheet that is drawn on and wiped repeatedly.
**Per-trail colour, on the grid band only.** Each sheet's border band carries its trail's colour — Leif `#216580`, Rollo `#A2562D`, Aud `#6D528B`, and `#467444` for Harald once that sheet exists — with the grid references reversed to white. Four laminated sheets are hard to tell apart on a crowded table, and the band is the only element visible from any edge that carries no map content. Built into `build_trail_maps_pdf.py` as a `band` key per trail.
**Print on white or natural cardstock, not coloured.** The sheet is a full-coverage two-tone illustration (sea `#DCE7E4`, land `#EFE3C4`) and printers cannot lay down white, so coloured stock would shift both fills toward the paper and compress a contrast that is already narrow. That contrast is load-bearing rather than decorative: it is what identifies the unlabelled animals on Leif's chart, so it cannot be spent on route identity. Coloured stock is better spent on the paper props — her letters, the museum tickets and their indexes, the luggage tags — where ink coverage is light and the paper colour becomes the design instead of fighting it.
Still untested: that the drawn shapes read as `1972` in a real play-test. Harald’s 2 is the loosest of the four — now that his real sheet is built (Q-020), the traced route reads more as a zigzag than a digit at all. Accepted anyway: by then one lock remains and the code parses as a year, which self-checks.

## Design notes (PZ-013: Decided and verified, 17 Sept 2026)

**The digit order is each trail’s first appearance — read from the reconstructed travel order, not from postmark dates.**

The order in which each trail **first appears** is the order its digit is read. That part still holds.
**What changed (PZ-013):** the source of that order is no longer a straight sort of postmark dates. Postmarks now carry place only. Order comes instead from reconstructing Liv's calendar — ticket dates, postcard statements and the final bundle — described in the [Final riddle tab].
**Constraint this places on the still-open calendar.** The earliest real (non-decoy) card of each trail must fall in the order **Leif → Rollo → Aud → Harald**, or the code is not `1972`. Postcard L1 (L’Anse aux Meadows) is still the first card of the game, so Leif leading is already true. **Decided, 16 Sept 2026:** postmarks carry no date at all (Q-006/old page PC-03/old page PC-04, removed) — L1's own place in the calendar comes from the reconstructed evidence in the Final riddle tab, not from anything printed on the card.
**Checked, 17 Sept 2026.** The clue set resolves this uniquely. First appearances land at positions 1, 4, 6 and 8 — Leif, Rollo, Aud, Harald — giving `1972`. Verified by `NorseBackpack/Tools/final_riddle_clues.py`; the ordering is now carried by the postcards’ own text rather than by date arithmetic, since variable stay lengths mean a date is no longer a position.

## Playtest evidence

**Playtest 1** (feedback relayed by the designer 12 Oct 2026; playtest date, team and hint use not recorded). Going back to the postcards for travel clues was too complicated. Playtesters suggested: using the postcards only for the family mark; making the card marks look like the iconography; more tickets or a fuller journal; clearer decoys (possibly no mark); stamps on the maps. Changes above (Q-054). Retest needed.

**17 Oct 2026 (designer, map cleanup review):** the existing Harald route shape is accepted as the final digit **2**. Leave the route and geography unchanged during the map cleanup. Earlier zigzag/readability concerns are not a requested redesign.

**20 Oct 2026 (designer): the three itinerary receipts (flight bookings between journeys) are dropped.** Every hop ticket carries a date (19 Oct) and each journey's dates form their own block (Leif 8–17 Sep, Rollo 28 Sep – 16 Oct, Aud 24 Oct – 1 Nov, Harald 14 Nov – 12 Dec), so the hop tickets alone give both the stop order and the journey order (1-9-7-2). Fewer pieces and less reading in the finale. Hint 3 and the Solution were reworded the same day to point at the ticket dates instead of the flight tickets (Claude; wording open to the designer).
