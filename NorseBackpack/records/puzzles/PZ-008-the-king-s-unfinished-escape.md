---
id: PZ-008
title: The king’s unfinished escape
type: puzzle
# idea | candidate | decided | built | parked
status: decided
# The structure beat this puzzle belongs to (one ID)
beat: ST-005
# Props the player needs, e.g. [PP-001]
props: [PP-016, PP-035, PP-036, PP-034]
# Puzzles that must be solved first, e.g. [PZ-002]
needs: [PZ-011]
# cipher | physical | search | logic | wordplay | other
mechanic: logic
# 1 (easy) to 3 (hard)
difficulty: 3
# Lock it opens: 3-digit | 4-digit | 4-letter | 3-digit-colour (blank if none)
lock: 3-digit
answer: 253
# Compartment this lock closes (shown on the Locks tab)
container: Small pouch, in the main compartment
# What players call this lock on the hint page, e.g. "The luggage tag" (spoiler-free)
hint_title: Lock 11
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
tags: [old-PZ-01, old-PZ-07]
---

## How it works

Rebuild the board your aunt sketched on the back of a map, then finish the game she left set up.

Lock 8 of 13 in the release order decided 7 Oct 2026 (Q-005). Difficulty 3 of 3 is Claude's estimate from the mechanism (number of props and steps), not playtest data.

**9 Oct 2026 (designer, Q-001):** now lock 11 of 13. Compartment: small pouch, in the main compartment.

## Player notices

The 11 × 11 board and pieces, the Hnefatafl Museum ticket with the rules, Harald’s Oslo map whose back carries the setup, and postcard H1 which sets the task.

## Player does

Recover the setup from two papers, place the fixed pieces, then take the king from the throne to any corner in exactly three straight-line moves. Count how far he travels on each leg.

## Player obtains

Code **253**. Opening this lock releases PP-019, PP-020, PP-038.

## Story reason

The strongest physical centrepiece in the set, the only puzzle that can release something mechanically rather than through a dial, and the only one that gives a trail map a job before the endgame.

## Clue wording

“I’m spending a whole week in Oslo, so much to do! It’s Harald’s city and has so much Viking history. Found the quirkiest little museum near the harbour, all about hnefatafl, the chess-like old board game the Vikings loved and that we used to play with our own rules when you were younger. Grabbed you a little souvenir from the gift shop so you can try — can you get the king to escape in exactly 3 moves? Count how far he travels each time. Love, Aunt Liv.”

## Hints

1. The board is eleven columns wide. Count what you can actually see.
2. Something was lying on the ink. It is still in the bag, and it is the right shape.
3. Work backward from a corner that is still reachable.
4. F6 → H6 → H11 → K11 — then measure each leg.

## Solution

Set out the starting position from Liv’s note, with columns I to K taken from the museum ticket. The king starts on the centre square F6 and escapes in exactly three moves: F6 → H6 → H11 → K11. The moves are **2**, **5** and **3** squares long: **253**.

## Solution notes

Design-side solution text, kept when the player-facing Solution above was written for the hint page (9 Oct 2026).

11 × 11, 16 attackers, 6 defenders, king on the true centre throne at F6. Exhaustive search over that exact layout gives exactly one three-move solution: **F6 → H6 → H11 → K11**. Its legs measure **2, 5 and 3** squares → **253**. Nothing is printed on the board. Columns A–H stay visible on the map back; I–K are lost to the stain and recovered from the ticket’s mirrored offset — assuming those three columns empty still leaves 31 candidate routes, so a guess fails to resolve rather than resolving wrongly.

## Open risks

**Composited, 19 Sept 2026.** Harald’s map sheet (`Trail_Map_4_Harald_{Print,ANSWER}.pdf`) is now two pages, one physical object: page 1 the rune-cipher front, page 2 the board-setup panel (stain, pieces, Liv’s margin note) reusing `build_board_setup_pdf.py`’s own drawing code and the shared paper/ink palette, centred on the same letter page and background tone as the front. Print both sides and laminate — no separate insert to align by hand. The old 7 × 7 solution (`231`) is fully superseded — not a fallback. A bought board in another size means rebuilding both the layout and its uniqueness proof (PP-035). **Still untested:** whether the offset reads through the ticket stock while the smear still hides the original (PP-036), and whether the front’s printed reference grid or this back page’s own ink ghosts through the laminate at real stock weight. This is also the third “line two papers up” gesture in the bag.

## Releases (as worded on the old page)

**Superseded 9 Oct 2026** by the compartment map in Q-001; the current release list is under Player obtains.

**Since 7 Oct 2026 (Q-005):** lock 8; releases postcards R1, R6 and RD.

Lock as recorded: Three-digit lock, or the throne compartment if the board is built rather than bought. Old page status: Code decided · lock 8 since 7 Oct 2026.

## Design notes (PZ-008: Decided at 11×11)

**Hnefatafl: exactly three moves, and the code is the leg lengths.**

**Board size changed to 11×11** (from 7×7, for realism) and the user designed the final layout themselves in [the board designer](../Props/Hnefatafl/board_designer.html) — 16 attackers, 6 defenders, king on the true centre throne (F6). Exhaustive search over that exact layout confirms **exactly three moves has one solution**: **F6 → H6 → H11 → K11**. The legs measure **2, 5 and 3** squares, giving code `253`. (Four moves has 18 solutions, same non-uniqueness pattern as the old 7×7 layout, so three stays the right move count.) The old 7×7 solution (`231`) is fully superseded — not a fallback, not a parallel option.
**The hidden-strip mechanism scales cleanly.** Columns A–H stay visible on the map back; columns I–K (3 columns, holding 3 attackers plus corners K1/K11) are lost to the stain and recovered on the ticket. Verified by search: assuming those three columns are empty still finds **31** candidate three-move routes, so the puzzle still refuses to resolve rather than resolving wrongly — the same self-checking property the 7×7 version had at 18 candidates.
**Rebuilt:** `Props/Hnefatafl/board_layout.py` (new 11×11 geometry, attackers/defenders now tracked separately), `build_board_setup_pdf.py` and `build_ticket_pdf.py` (both draw attacker vs. defender as visually distinct tokens now that the layout has both), and the interactive prototype in the [Prototype tab] (board, blockers, reset/hint routes all updated to match).
Setup still arrives via the map back and the museum ticket (PZ-008), still on **Harald's trail** (the Oslo postcard, stop 1) — blocked on Harald's map sheet, which does not exist yet. Liv's task line on the Oslo postcard (Q-019) still reads “exactly three moves,” which is now correct again since the new layout's unique solution also happens to be three moves.

## Design notes (PZ-008: Rebuilt at 11×11 · on Harald’s map)

**The board setup, split across the map back and the museum ticket.**

**Reassigned from Leif to Harald.** Superseding the earlier “it is Leif's map” decision below: the user moved this to **Harald's trail**, arriving with the Oslo postcard (stop 1, Q-019). Liv wrote the 22 fixed-piece positions (16 attackers, 6 defenders) on the back of the Oslo trail map; the wet ticket was set down on the drawing and lifted the right-hand strip (columns I–K), leaving an illegible stain on the map and a *mirrored* copy (columns read **K J I** left to right — reversed from the map's own I, J, K order) on the ticket's blank back panel. Hold the ticket to the light, align on the grid lines, the board completes.
**Rebuilt at 11×11 (PZ-008), both panels, sharing one geometry source so they can't drift apart:**

- `Props/Hnefatafl/board_layout.py` — the 22 attacker/defender squares, throne and corners, one place, matching the interactive prototype in this page and the user's own [board designer](../Props/Hnefatafl/board_designer.html) export exactly.
- `Props/Hnefatafl/build_board_setup_pdf.py` — the map-back panel: columns A–H plus the throne and two visible corners, attackers and defenders drawn as visually distinct tokens (dark filled vs. light outlined squares), with an irregular stain swallowing columns I–K (their squares are never drawn under the stain, not merely covered by it — the earlier 7×7 draft made that mistake and the tokens showed through). Liv's own margin note sits beside the stain (“Oops — ticket was still wet when I set it down here. Sorry, past me. — L”). Output: `output/pdf/Hnefatafl_Board_Setup_Insert.pdf` — a standalone insert, now composited onto Harald's trail map back (see the map gallery in this tab). **7 Oct 2026 (user):** the standalone insert (and its Word file `output/docx/Print_HnefataflBoardSetupInsert.docx`) now has no background colour, because a paper-tone block on a white page looked pasted on. Harald’s map back keeps the paper tone edge to edge, so it is unchanged. **Same day (user):** the grid lines under the stain read as untouched while the pieces were gone. Both the insert and Harald’s map back now erase the straight pen lines under the stain and draw smudged copies in their place: wavy, dragged downward, blurred and broken in places, so the grid is still roughly traceable for lining up the ticket (`_smudged_lines` in `build_board_setup_pdf.py`, fixed seed). ~~First pass: a page-colour wash fading the straight lines (`LINE_FADE` 0.88); the user found them still too straight.~~ The stain artwork itself is unchanged; its grey streaks are part of the generated image (Codex).

![Hnefatafl board-setup insert, standalone](Props/_Renders/Hnefatafl_Board_Setup_Insert_Insert.png)Standalone insert

- `Props/Hnefatafl/build_ticket_pdf.py` — the ticket's back panel: the same three columns, reversed and matched to the same 0.4in cell pitch, so the grid lines genuinely continue when the two sheets are butted together. The ticket grew from 2.4 × 5.6in to 2.6 × 6.6in to fit the taller three-column, eleven-row panel.

Settled: the grid lines cross the join so registration is self-verifying; the stain leaves the gap visible rather than implied; both marks are printed rather than real ink so the prop resets. **New candidate · recorded 2026-09-15:** 3D-print the attacker and defender pieces with controlled, concealed weights and a letter or rune on each base. Weigh and order the attackers light-to-heavy to read one sentence/word; weigh and order the defenders separately to read a second. A dark attacker and light defender may share a weight, so players must understand and group the two sides before ordering. The 16 attackers can carry the longer instruction; the 6 defenders suit a short word. Keep this separate from the board-reconstruction/king-escape solve: it is a later Oslo branch using the same pieces, not another condition of setting up the board. **Open:** which exact two texts the sides yield; target masses, ballast method and base-letter treatment; and whether the attacker/defender weights remain stable through repeated 3D-printing. Harald's actual trail map sheet is now built; the insert panel still needs compositing onto its back. Which specific board to buy is still open (PP-035), though the board size itself (11×11) and the A–H/I–K split are now settled regardless of which listing is chosen. **Updated, 25 Sept 2026:** Harald’s map sheet exists and `build_trail_maps_pdf.py` composites the board setup onto its back. What remains is the stock and read-through test in PP-036, and the board purchase in PP-035.
