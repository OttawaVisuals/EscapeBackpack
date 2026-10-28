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
lock: 4-digit
answer: 2134
envelope_marks: ᛚᚹᚲᛏ
# Compartment this lock closes (shown on the Locks tab)
container: Envelope 11
reset_display: 000
# What players call this lock on the hint page, e.g. "The luggage tag" (spoiler-free)
hint_title: Just opened ᛁᛉᚲᛇ
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

**11 Oct 2026 (designer, PR-007):** no locks or pockets any more. This code, set on the rune cypher wheel (PP-047), points to envelope 11, which holds what lock 11 used to close.


**11 Oct 2026 (playtest 1 feedback, built same day):** Oslo ticket front no longer shows a mini-board; it shows a capture diagram (PP-036).

## Player notices

The 11 × 11 board and pieces, the Hnefatafl Museum ticket with the rules, Harald’s Oslo map whose back carries the setup, and postcard H1 which sets the task.

## Player does

Recover the setup from Liv's papers (the back of Harald's map and the museum ticket), place the pieces, then play the sequence: a dark piece moves, then the king, four times. The first two dark moves are the numbered arrows on the map back, the third is Liv's riddle, the last is marked by the shield icon on Harald's map. The king must reach a corner in exactly four straight-line moves. Count how far he travels on each leg.

## Player obtains

Code **253**. Opening this lock releases PP-019, PP-020, PP-038.

## Story reason

The strongest physical centrepiece in the set, the only puzzle that can release something mechanically rather than through a dial, and the only one that gives a trail map a job before the endgame.

## Clue wording

“I’m spending a whole week in Oslo, so much to do! It’s Harald’s city and has so much Viking history. Found the quirkiest little museum near the harbour, all about hnefatafl, the chess-like old board game the Vikings loved and that we used to play with our own rules when you were younger. Grabbed you a little souvenir from the gift shop so you can try — can you get the king to escape in exactly 3 moves? Count how far he travels each time. Love, Aunt Liv.”

## Hints

1. The board is eleven columns wide. Count what you can actually see, and think about what the smudge hides.
2. Something was lying on the ink. It is still in the box, and it is the right shape.
3. Dark moves first, then the king, four times. The numbered arrows on the back of Harald's map are the first two dark moves; Liv's riddle gives the third.
4. The shield on the museum ticket is also printed on Harald's map. It marks where the last dark piece goes, and that move frees the way for the king.
5. The king does not have to run to the top of the column. Try stopping after one square.
6. F6 → H6 → H7 → K7 → K11, then measure each leg.

## Solution

Set out the starting position from Liv's note, with columns I to K taken from the museum ticket. Then play: dark E1 → E6, king F6 → H6; dark H2 → H5, king H6 → H7; dark H10 → H11 (the attacker on the second-highest row steps up to the top row), king H7 → K7; dark K10 → I10 (the shield on Harald's map is at I10, and moving the piece on K10 frees column K), king K7 → K11. The moves are **2**, **1**, **3** and **4** squares long: **2134**.

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
- `Props/Hnefatafl/build_board_setup_pdf.py` — the map-back panel: columns A–H plus the throne and two visible corners, attackers and defenders drawn as visually distinct tokens (dark filled vs. light outlined squares), with an irregular stain swallowing columns I–K (their squares are never drawn under the stain, not merely covered by it — the earlier 7×7 draft made that mistake and the tokens showed through). Liv's own margin note sits beside the stain (“Oops — ticket was still wet when I set it down here. Sorry, past me. — L”). Output: `NorseBackpack/Print/_pdf_source/Hnefatafl_Board_Setup_Insert.pdf` — a standalone insert, now composited onto Harald's trail map back (see the map gallery in this tab). **7 Oct 2026 (user):** the standalone insert (and its Word file `NorseBackpack/Print/Print_HnefataflBoardSetupInsert.docx`) now has no background colour, because a paper-tone block on a white page looked pasted on. Harald’s map back keeps the paper tone edge to edge, so it is unchanged. **Same day (user):** the grid lines under the stain read as untouched while the pieces were gone. Both the insert and Harald’s map back now erase the straight pen lines under the stain and draw smudged copies in their place: wavy, dragged downward, blurred and broken in places, so the grid is still roughly traceable for lining up the ticket (`_smudged_lines` in `build_board_setup_pdf.py`, fixed seed). ~~First pass: a page-colour wash fading the straight lines (`LINE_FADE` 0.88); the user found them still too straight.~~ The stain artwork itself is unchanged; its grey streaks are part of the generated image (Codex).

![Hnefatafl board-setup insert, standalone](Props/_Renders/Hnefatafl_Board_Setup_Insert_Insert.png)Standalone insert

- `Props/Hnefatafl/build_ticket_pdf.py` — the ticket's back panel: the same three columns, reversed and matched to the same 0.4in cell pitch, so the grid lines genuinely continue when the two sheets are butted together. The ticket grew from 2.4 × 5.6in to 2.6 × 6.6in to fit the taller three-column, eleven-row panel.

Settled: the grid lines cross the join so registration is self-verifying; the stain leaves the gap visible rather than implied; both marks are printed rather than real ink so the prop resets. **New candidate · recorded 2026-09-15:** 3D-print the attacker and defender pieces with controlled, concealed weights and a letter or rune on each base. Weigh and order the attackers light-to-heavy to read one sentence/word; weigh and order the defenders separately to read a second. A dark attacker and light defender may share a weight, so players must understand and group the two sides before ordering. The 16 attackers can carry the longer instruction; the 6 defenders suit a short word. Keep this separate from the board-reconstruction/king-escape solve: it is a later Oslo branch using the same pieces, not another condition of setting up the board. **Open:** which exact two texts the sides yield; target masses, ballast method and base-letter treatment; and whether the attacker/defender weights remain stable through repeated 3D-printing. Harald's actual trail map sheet is now built; the insert panel still needs compositing onto its back. Which specific board to buy is still open (PP-035), though the board size itself (11×11) and the A–H/I–K split are now settled regardless of which listing is chosen. **Updated, 25 Sept 2026:** Harald’s map sheet exists and `build_trail_maps_pdf.py` composites the board setup onto its back. What remains is the stock and read-through test in PP-036, and the board purchase in PP-035.

## Playtest evidence

**Playtest 1** (feedback relayed by the designer 11 Oct 2026; playtest date, team and hint use not recorded). The simplified board drawing on the Oslo ticket was confusing (read as a setup). Replaced (PP-036); retest needed.

**16 Oct 2026 (designer, envelope 10):** changes asked for: (1) H1 text clearer that the puzzle starts from a set-up board (done, PP-016); (2) the ticket back (mirrored I–K strip, PP-036) to look more smudged, like a wet-ink transfer (Codex job, brief not written yet); (3) **black-piece moves** so exactly one escape remains, with the black pieces' moves defined for players. Not designed yet: the choice is scripted replies on the ticket (my pick) or per-piece move rules; I would write a solver to prove a single 3-move escape. The current solution F6 → H6 → H11 → K11 (253) holds until the designer decides.

**16 Oct 2026 (designer, direction, not built):** the black-piece moves (scripted replies, option A) are to be given by a **riddle on a postcard**. **HD (Constantinople) is retired from envelope 3 and redone completely as an Oslo-leg card for this puzzle** (envelope 10, with H1). The **FERMENTED rebus (sugar + yeast → flask) moves to H2 or H3**, and the other of the two gets a drawing of a tipsy person (PZ-004 and PP-017/018/022 need updating when this is built; the DRINK acrostic and HONEY riddle stay). The riddle must decode to the black moves in order, e.g. “first move F1 to F4, second move G2 to H2, third …” (the squares here are the designer's example, not the real ones). Before building: design the riddle and prove with a solver that exactly one 3-move escape remains after black's replies.

**16 Oct 2026 (designer, supersedes the HD direction above):** the black-piece moves use **“sequence continuation” with chess notation** (Clue library): the first moves are written in notation and the rest follow a pattern players infer. It is carried by the **Oslo postcard (H1), the back of Harald's map and the ticket**. **HD stays as it is in envelope 3** (FERMENTED rebus kept; no tipsy-person drawing, no changes to H2/H3). The spot-the-difference and board-picture ideas were rejected: showing the final board would skip the moves. Not designed yet: a solver must prove a single 3-move escape.

**16 Oct 2026 (Claude, solver work for the black moves):** `Props/Hnefatafl/hnefatafl_solver.py` (rook-like sliding, custodial capture, king to a corner, black moves first: B K B K B K). It reproduces the current single escape F6 H6 H11 K11 (253). Findings: (1) a single guard marching H5→H7→H9→H11 leaves one escape (F6 H6 H1 K1) but the legs are again 2, 5, 3 = **253**, so a player who ignores black still gets the right code; (2) designs where three guards slide the same vector give different codes (e.g. A4→C4, A8→C8, F11→H11: king F6 F7 A7 A11, code **154**; A4→B4, G8→H8, A5→B5: F6 F7 A7 A1, code **156**), but the third guard is not pinned down by the pattern; (3) no design found where both from-squares and to-squares are arithmetic progressions, the third move matters and the code differs from 253. Not decided: the pattern for the postcard, the code (it would change from 253, which also changes envelope 11's runes).

**16 Oct 2026 (Claude, tool):** `Props/Hnefatafl/board_designer.html` now starts on the real puzzle layout and has a **Puzzle run** panel for trying the black and king moves by hand: click a piece then a square, or type a move (`A8-D8`). Sequences: black, king, black, king, black, king; black, king, black, king, king; or king only. It enforces who moves, slides like a rook, captures by sandwich, and reports the king's legs and the code when he reaches a corner (and says if it takes more or fewer than 3 king moves). Undo, Restart, and a switch to cover columns I to K like the stain. The old file is kept as `board_designer.2026-10-16_before_play_mode.html`. Tested against the solver on two lines: A8-D8 / F6-F7 / H5-H7 / F7-A7 / A7-A11 gives code 154, and the plain F6-H6-H11-K11 gives 253. Captures follow the designer's old rules (corner and throne count as hostile), the solver's do not treat the throne as hostile; no difference showed up in these lines.

**16 Oct 2026 (designer, direction, not built):** the puzzle is to change from "escape in exactly 3 moves" to **exactly 4 king moves**, with black moves added (the number of black moves and their puzzle are still open). The board tool (`Props/Hnefatafl/board_designer.html`) now lets the designer choose 3 or 4 king moves and 0 to 4 black moves (black plays before the king's move of the same number), and reports the legs and a code of that many digits. If adopted: the answer becomes a 4-character code (the cypher wheel's four dials can take it), H1's “exactly 3 moves”, the ticket, hints and the digital game all change, and envelope 11's runes change with the new code. The solver (`hnefatafl_solver.py`) takes the king-move count as a parameter (`nk`). With 4 king moves and no black moves, today's route F6 H6 H11 K11 is no longer an escape in exactly 4.

**16 Oct 2026 (designer):** king capture rule fixed on the ticket (PP-036): four sides hostile, the edge counts; two enemies do not capture him. Tool and solver agree.

**17 Oct 2026 (designer, adopted; not yet built):** the puzzle becomes **4 king moves with 4 black moves** (black plays before each king move), answer **2233**. Start layout (16 dark + I7 and I9 = **18 dark**, 6 light, king F6): dark A4 A5 A8 B1 D11 D7 E1 E11 F1 F11 F9 G1 H2 H10 I6 I7 I9 K4; light C5 E8 F5 F8 G5 G7. Compared with today's layout: D6→D7, H5→H2, G8→H10, K8 removed, E1 added, I7 and I9 added (all three of I6, I7, I9 and K4 sit in the hidden columns I to K, so the ticket strip must show them). Black moves in order: **E1-E6, H2-H5, H10-J10, J10-J11**. King: F6-H6 (2), H6-H8 (2), H8-K8 (3), K8-K11 (3) = **2233**. Solver check (`hnefatafl_solver.py`, ticket rules incl. the king-capture line): this is the only escape in 4 king moves, none in 3 or fewer; every black move matters (skipping any one changes the result); without I7 and I9 there were 3 escapes (2134, 2233, 2332), with only one of them 2. Picture: `Props/Hnefatafl/black_moves_solution_2233_preview.png`. **Still to design (puzzle, per the designer):** the two arrows on the back of Harald's map (two of the black moves), a cryptic note giving their order, and a puzzle that gives the last black position (option B, a place on Harald's map whose grid reference is a board square: e.g. J10 and J11 are not on the map's lettering, so the designer must pick which two moves are the arrows and how the others are given). Ripple when built: `board_layout.py` (layout, solution path), map-back setup and note ("13 dark, 6 light"), ticket strip, H1 text (“exactly 3 moves” → 4), the code in the PZ-008 `answer`, envelope 11's runes (rebuild the wheel), the hint page, `Digital/leif-data.js` and tests, PP-035 (the pieces: 18 dark instead of 16), PP-036.

**17 Oct 2026 (Claude, solver; proposal to the designer, not decided):** the adopted moves 3 and 4 (H10-J10, J10-J11) end in column J, which does not exist on Harald's map (columns A, C, E, I, K, N, R, T, V), so the “last position from a place on the map” puzzle cannot name them. With the adopted layout, many replacements keep the answer 2233 and the unique escape; the ones where **both** replaced moves are needed (skipping either changes the result) are: **H10-E10 (or H10-C10, H10-A10) then I9-I11**. Other both-needed pairs give different codes (2237 or 2332). The first two black moves (E1-E6, H2-H5) are the ones that decide the route; most pairs of moves 3 and 4 do not change the answer.

**17 Oct 2026 (designer, decided; not yet built):** black moves 3 and 4 are **H10-E10 and I9-I11** (replacing H10-J10 and J10-J11, which end in a column Harald's map does not have). Full line: black E1-E6, king F6-H6 (2), black H2-H5, king H6-H8 (2), black H10-E10, king H8-K8 (3), black I9-I11, king K8-K11 (3) = **2233**. Solver check on the 18-dark layout: exactly one escape in 4 king moves, none in 3 or fewer. Which black moves matter: skipping move 1 leaves 44 escapes, skipping move 2 leaves 4, skipping move 4 leaves 5; **skipping move 3 (H10-E10) still gives the same single escape**, so move 3 is there for the count and the story, not for the route (it was a “both needed” result only when moves 3 and 4 were played before king moves 3 and 4 in the other order I tested; treat move 3 as decorative). If only the destination square is told, the piece is ambiguous: E10 can be reached by H10 or E11 at that moment, I11 by I9 or F11, so the puzzle must also name the piece (its start square). Build list approved for listing (17 Oct): see the dated note below once the designer signs it off.

**17 Oct 2026 (designer):** the layout stays at **18 dark** (no extra blocker on H9). The king can stop on H7, H8 or H9 when sliding up column H, but only H8 gives an escape: east of H7 and H9 sit the hidden pieces I7 and I9 (ticket strip). The designer likes that the natural idea is to go all the way to the top, which fails, so it adds difficulty. The board tool has a button “Adopted layout (18 dark, code 2233)” that loads this layout (tested: the 8-move line gives code 2233; H6-H9 does not lead to an escape).

**17 Oct 2026 (designer, decided; supersedes the 2233 design above; not yet built):** answer **2134**, **4 king moves, 4 black moves** (black plays before each king move). **Start layout, 18 dark and 6 light, king F6:** dark A4 A5 A8 B1 D11 D7 E1 E11 F1 F11 F9 G1 H2 H10 I6 I8 I9 K4; light C5 E8 F5 F8 G5 G7. Against today's layout: D6→D7, H5→H2, G8→H10, K8 removed, E1 added, I8 and I9 added (hidden columns I to K hold I6, I8, I9, K4). **Black:** E1-E6, H2-H5, **H10-E10**, **I9-I11**. **King:** F6-H6 (2), H6-H7 (1), H7-K7 (3), K7-K11 (4) = **2134**. Solver check: exactly one escape in 4 king moves, none in 3 or fewer. **The last black move is needed:** without I9-I11 there are five escapes (2134, 1153, 2143, 2233, 2323, all through H11 and row 11); the designer's earlier last move J10-J7 changed nothing, and J-column moves cannot be named on Harald's map anyway. The black piece moves 3 (H10-E10, also H10-C10 or H10-A10 work) and 4 (I9-I11) end on E10 and I11, columns that exist on Harald's map. The king stops on **H7** after one square, because I8 and I9 block rows 8 and 9: going to the top (H8, H9, H11) fails. Still to design: the two arrows on the back of Harald's map (E1-E6 and H2-H5 are the decisive ones), the cryptic order note, and the puzzle that gives moves 3 and 4 (the piece as well as the square: E10 can be reached by H10 or E11, I11 by I9 or F11). Build list (not approved yet): `board_layout.py`, map back, ticket strip + smudge, ticket rules line, H1 (“exactly 4 moves”), answer 2134 with the wheel and envelope 11's runes, hint page, `Digital/leif-data.js` and tests, PP-035 (18 dark), PP-036. Picture: `Props/Hnefatafl/black_moves_solution_2134_preview.png`.

**17 Oct 2026:** animated solution for the 2134 design, for hints and the solution page: `Props/Hnefatafl/black_moves_solution_2134.gif` (10 frames: start, the eight moves with the black move arrowed, then the escape and code; loops). Not yet linked from the hint page; regenerate it if the layout or moves change (script was a scratch file, the layout and moves are in the note above).

**17 Oct 2026:** the solution GIF `Props/Hnefatafl/black_moves_solution_2134.gif` was rebuilt smoother: 98 frames, about 18 s, 287 KB, loops. Each move slides across the board with easing (dark pieces get a small shadow and blue outline and leave a blue trail; the king leaves his path as he goes), and eight progress dots at the bottom fill in black and king order. The first, simpler version is replaced (kept outside the project). Same note as before: shows every piece, so it belongs on the solution page or the last hint.

**17 Oct 2026 (designer, delivery of the four black moves, not built):** (1) **moves 1 and 2** (E1-E6, H2-H5): Codex draws them as **pencil arrows with the numbers 1 and 2** on the board on the back of Harald's map (this also gives the order, so no separate cryptic order note is needed); (2) **move 3** (H10-E10): given as a **riddle in the H1 postcard text**; (3) **move 4** (I9-I11): an **icon for the Viking chess game** printed on Harald's map at the matching grid cell (I11; the map's columns are A, C, E, I, K, N, R, T, V and its rows count from the top, so players read the label) and also shown on the museum ticket, where it says what the icon means. Solver check (Claude): giving only the destination squares is enough. Moves 3 and 4 may be played by either piece that can reach the square (H10 or E11 to E10; I9 or F11 to I11) and all four combinations give the same unique escape 2134. At the start H10 is the only dark piece on row 10. I11 on Harald's map does not clash with the five branch-rune cells of PZ-012 (G6, A10, I9, C3, F2 in that record's wording); the icon must not disturb that puzzle.

**17 Oct 2026 (designer, the smudge as the in-story reason; not built):** Liv's note on the back of Harald's map becomes: “Silly sausage me, I smudge[d] part of the board with my wet museum ticket. Not to worry, for the 3rd attacker move solve this riddle: [riddle]. For the last attacker move, you might have to look somewhere else for it.” The first two moves are shown as numbered arrows on the board. The riddle is still to be chosen (options for E10 were offered; option 3, “Row ten, same column as the first arrow ends.”, is only a stand-in in the preview). The designer typed “smudge”; “smudged” is used in the preview (to be confirmed). Preview with the adopted 2134 layout, placeholder arrows and the longer note: `Props/Hnefatafl/mapback_note_preview_2134.png`; it needs about 66 pt more space under the board (bottom margin 62 to 128 pt, so the insert gets taller) and Codex would redraw the arrows as pencil. Replaces the old “Oops - ticket was still wet … Sorry, past me” lines.

**17 Oct 2026 (designer, decided; not built):** the **third black move** riddle is “The attacker on the second-highest row flees the king and goes to safety between his colleagues.” It means **H10 → F10**: at that moment H10 is the only dark piece on row 10, the king stands on H7 in its column, and F10 is the only square H10 can reach that sits between two dark pieces (F11 above, F9 below). Solver: H10-F10 followed by I9-I11 (or F11-I11) leaves the same unique escape F6 H6 H7 K7 K11 = 2134. So the line is now **E1-E6, H2-H5, H10-F10, I9-I11** (E10 is replaced by F10; E10, G10 and A10 would also leave 2134, so the third move is a soft clue). The map-back note reads: “Silly sausage me, I smudged part of the board with my wet museum ticket. Not to worry, for the 3rd attacker move solve this riddle: [the riddle]. For the last attacker move, you might have to look somewhere else for it.” **Icon for the fourth move:** Codex generated `C:\EscapeBackpack\output\imagegen\hnefatafl-shield.png` (1254 x 1254, transparent, one dark colour: a round shield with a crowned king piece and four discs), to sit at I11 on Harald's map and on the museum ticket. Not yet placed.

**17 Oct 2026 (designer, built part):** the hand-drawn shield icon (Codex, `hnefatafl-shield-hand-drawn.png`, copied to `Props/Hnefatafl/Hnefatafl_Shield_Icon_HandDrawn_v1.png`, prompt beside it) replaces the flat first version. **Done:** icon on the Hnefatafl Museum ticket front (PP-036) and on Harald's map at I11 (PP-034). **Liv's text stays vague** about the icon (the map-back note only says to look somewhere else for the last attacker move). Not done yet: the rest of the build list (board_layout, map back with arrows and the note, ticket strip and smudge, H1, code 2134 and the wheel, hints, digital game, PP-035).

**17 Oct 2026 (designer, decided; supersedes the F10 riddle and the 18-dark layout above; not yet built):** **K10 version.** Layout **19 dark, 6 light**, king F6: dark A4 A5 A8 B1 D11 D7 E1 E11 F1 F11 F9 G1 H2 H10 I6 I8 I9 K4 **K10**; light C5 E8 F5 F8 G5 G7. Hidden columns I to K hold I6, I8, I9, K4, K10 (five pieces on the ticket strip). **Black: E1-E6, H2-H5, H10-H11, K10-I10. King: F6-H6 (2), H6-H7 (1), H7-K7 (3), K7-K11 (4) = 2134.** The idea (designer): **the last black move opens the escape.** The dark piece on K10 blocks column K above the king, so K7-K11 only works after K10 leaves. Solver (`hnefatafl_solver.py`): exactly one escape in 4 king moves, none in 3 or fewer; **without the last black move there is no escape at all**; skipping move 1 leaves 44 escapes, skipping move 2 leaves 4; move 3 is soft (skipping it still gives the same unique 2134; about 116 other third moves also keep it, but H10 sliding sideways does not, so H10-F10 and H10-E10 no longer work). K10 may go to I10 or any square west on row 10 and the answer stays 2134. Two leaks in the designer's first K10 attempt were closed: K4 must stay (without it K7-K1 also escapes, 2136) and H10 must stay on column H (moved to H11 at the start it let the king escape through row 10, 2471). **Move 3 riddle:** “The attacker on the second-highest row steps up to the top row” = **H10-H11** (H10 is the only dark piece on row 10; it steps straight up to row 11). **Move 4:** the hand-drawn shield icon, now to sit at **I10** on Harald's map (not I11 as built so far), and on the ticket; I10 is a column Harald's map has (I). The other pieces that can reach I10 at that moment (H10's old square, I8, I11) would not open the column, so players must also work out that K10 is the piece to move. Map-back note: arrows 1 and 2 numbered, then the smudge note with the move-3 riddle. Still to build: the whole list (board_layout.py, map back, ticket strip and smudge with K10 included, H1 “exactly 4 moves”, code 2134 with the wheel and envelope 11's runes, hints, digital game, PP-035 for 19 dark, PP-036), **and move the map icon from I11 to I10.**

**17 Oct 2026:** the solution GIF `Props/Hnefatafl/black_moves_solution_2134.gif` and the picture `black_moves_solution_2134_k10_preview.png` now show the K10 version (19 dark; black E1-E6, H2-H5, H10-H11, K10-I10; king F6-H6-H7-K7-K11 = 2134). The board tool's “Adopted layout (19 dark, code 2134)” button loads it (tested: the 8-move line reports 2134, and K7-K11 before K10 has left is refused). The shield icon on Harald's map moved from I11 to **I10** (PP-034 note below).

**17 Oct 2026 (built):** 2134 design built. `board_layout.py` (19 dark, BLACK_MOVES, solution path; the old layout kept as `board_layout.2026-10-17_before_2134.py`); map back and Harald's page 2 (`build_board_setup_pdf.py`, old kept as `...2026-10-17_before_2134.py`: arrows 1 and 2, Liv's note with the riddle); ticket strip and rules line; H1 “exactly 4 moves”; `answer: 2134`, `lock: 4-digit`; hints and solution rewritten; cypher wheel rebuilt (envelope 11 = 2134, runes ᛚᚹᚲᛏ; PR-007 row 11 and PZ-012's hint title updated); `Digital/leif-data.js` and `leif.test.cjs` (40 of 40 pass); icon at I10. `hnefatafl_solver.py` run against `board_layout.py` confirms one escape in 4 king moves, none in fewer, none without the last dark move. **Still open:** Codex to redraw the arrows if wanted and to redo the smudged ticket strip with the new pieces; PP-035 physical set needs 19 dark pieces; the hint page text beyond this record; nothing printed or paper-tested; the digital game is a hint entry only (no board).

**17 Oct 2026:** the smudged ticket strip for the 2134 layout is done and in use (see PP-036): five squares at K10, K4, I9, I8, I6. Only the physical read-through and print tests are open for the ticket; Codex may still redraw the pencil arrows on the map back (placeholder arrows are drawn in code).

**17 Oct 2026 (designer, Q-063): turn order added to H1.** After “exactly 4 moves?” the message now reads “Each round, a dark piece moves first, as my notes show, then the king.” (wording by Claude, chosen by the designer from options; the message is one line longer). Not added: “the other pieces stay where they are” (the solver assumes it; offered, not chosen). Print PDFs, page images and web copies rebuilt.
