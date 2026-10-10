---
id: PZ-012
title: Branch runes and the raven’s flights
type: puzzle
# idea | candidate | decided | built | parked
status: decided
# The structure beat this puzzle belongs to (one ID)
beat: ST-005
# Props the player needs, e.g. [PP-001]
props: [PP-019, PP-020, PP-034, PP-038, PP-027]
# Puzzles that must be solved first, e.g. [PZ-002]
needs: [PZ-008]
# cipher | physical | search | logic | wordplay | other
mechanic: cipher
# 1 (easy) to 3 (hard)
difficulty: 3
# Lock it opens: 3-digit | 4-digit | 4-letter | 3-digit-colour (blank if none)
lock: 4-digit
answer: 2648
# Compartment this lock closes (shown on the Locks tab)
container: Large pouch, in the main compartment
# What players call this lock on the hint page, e.g. "The luggage tag" (spoiler-free)
hint_title: Lock 12
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
tags: [old-PZ-02]
---

## How it works

Decode five letters, then use them as five perches to read four flight digits.

Lock 12 of 13 in the release order decided 7 Oct 2026 (Q-005). Difficulty 3 of 3 is Claude's estimate from the mechanism (number of props and steps), not playtest data.

**9 Oct 2026 (designer, Q-001):** now lock 12 of 13. Compartment: large pouch, in the main compartment.

## Player notices

H4/H5 and the player-only perch card (from lock 11) and the corrected Harald map (from lock 7, with the board kit), since 7 Oct 2026. ~~All available before the board lock.~~

## Player does

Use RAVEN to select map columns; H4 decodes HRAFN. Follow the direct connections H→R→A→F→N and read one digit per flight in that order.

## Player obtains

Code **2648**. Opening this lock releases PP-021, PP-039, PP-040, PP-041.

## Story reason

Keeps the existing cipher and replaces the cryptex with one printable card and a normal lock.

## Clue wording

Keep H4’s key and H5’s underlined raven (capitals since 29 Sept 2026). Perch card: “Follow the five letters you uncovered. Read the number on each flight, in order.”

## Hints

1. The underlined word on the Sicily postcard matters to the map’s unusual column labels.
2. Read the columns R, A, V, E, N in that order. On Hedeby’s key, each stem’s left branches select the row; its right branches select the letter.
3. Use the five decoded letters as perches on the raven’s flights card. Move directly from each letter to the next and read one digit from each flight. Do not add them.

## Solution

R6 → H, A10 → R, V9 → A, E3 → F, N2 → N: HRAFN. Then H → R = 2, R → A = 6, A → F = 4, F → N = 8: **2648**.

## Solution notes

Design-side solution text, kept when the player-facing Solution above was written for the hint page (9 Oct 2026).

R6→H, A10→R, V9→A, E3→F, N2→N. Then H→R = 2, R→A = 6, A→F = 4, F→N = 8. Code **2648**. No translation of HRAFN is required.

## Open risks

Use the corrected map: the original E7 decoy creates a second answer (fixed in the production map 29 Sept 2026: decoy now at I7). H4/H5 remain unchanged. Perch artwork needs player-only print-size proof; comparison image contains the solution and must not be packed. Former cryptex and key are superseded.

## Releases (as worded on the old page)

**Superseded 9 Oct 2026** by the compartment map in Q-001; the current release list is under Player obtains.

**Since 7 Oct 2026 (Q-005):** lock 12; releases postcard H6, the transition tickets and the journal. ~~H1, hnefatafl board, 16 dark pieces, 6 light pieces, king, museum ticket and fixed-piece challenge rules.~~

Lock as recorded: Four-digit lock on the pouch holding H6, the transition tickets and the journal (since 7 Oct 2026; was the board-kit pouch). Old page status: Five-perch conversion approved · path-only card on the luggage-tag sheet, test print pending.

## Design notes (PZ-012: Mechanism approved · player card built, 28 Sept 2026)

**HRAFN selects five perches and four flight digits.**

**Harald map fixed, 29 Sept 2026.** A reviewer spotted two rune stems in column E: the real F at E3 and a decoy at E7. Because RAVEN selects whole columns, that let players read HRAFN or HRALN. The decoy moved one column right to **I7** (not a RAVEN column), the fix the 22 Sept review had already proposed but never applied to the production map. Now R6, A10, V9, E3 and N2 are the only stems in the R, A, V, E and N columns; the builder asserts this. Route, answer (HRAFN → 2648) and the board back are unchanged. Rebuilt `Trail_Map_4_Harald_Print.pdf` and `_ANSWER.pdf`.

**29 Sept 2026 (user):** H5 now writes the word in capitals — “A RAVEN followed me the whole time!” — instead of underlining it. Same selector, more visible.

**29 Sept 2026 (user):** the card is now path only — the title, instruction lines, four answer boxes and raven emblem are removed — and it prints on coloured paper on the same Letter page as the two luggage tags. To suit coloured paper nothing is filled white: each flight stops at the perch outline and breaks around its digit. Graph enlarged (3.4 in wide, digits 11 pt); still a 4 × 3 in cut with crop marks. Print file: `output/docx/Print_LuggageTags.docx`. The stand-alone `PrintTest_RavenFlights.docx` is retired.

**Player card built, 28 Sept 2026:** 4 × 3 in, single-sided (size chosen by the user; the review's working size was half-Letter). Approved graph; no route or answer marked. *(Originally also had the title and clue, four blank answer boxes and a small raven emblem; removed 29 Sept 2026, see the note above.)* Source `Props/RavenFlights/build_raven_flights_pdf.py` (checks that HRAFN reads 2648 before building; the sheet itself is built by `Props/build_luggage_tag_inserts_pdf.py`); PDF [View PDF](../Web/pdf/Raven_Flights_Card_Print.pdf) (card alone). Not yet printed or tested on a player.
H4/H5 and the corrected map still decode HRAFN. Follow H–R–A–F–N on the new flight card: 2, 6, 4, 8. One four-digit lock directly secures H1, the board, pieces, ticket and challenge rules. Release the perch card with H4/H5 after SOLE, outside that pouch. **Superseded, 23 Sept 2026 (old page PC-18):** 2648 now opens the pouch with H2, H3 and HD. The hnefatafl pouch opens with MEAD. The perch card arrives with H4/H5 after the comb (BOOK), not directly after SOLE. No cryptex or key. See PP-038 and Approved changes.

**Superseded specification · before 22 September 2026**

PZ-012 Mechanism decided, 17 Sept 2026

The cryptex answer, and what opening it releases.

`HRAFN` fits a five-ring cryptex. It was also briefly assigned to the word lock, but that lock is now a physical 4-letter lock (see PZ-010), so `HRAFN` (5 letters) only fits the cryptex.
**Delivery decided:** the rune stick and museum label are dropped. The five branch-rune stems live on Harald's own trail map instead, at grid cells `G6, A10, I9, C3, F2`, among seven meaningless decoy stems elsewhere on the sheet. Postcard **H4** carries the decode key (the three rune groups, and that left branches count the group while right branches count the position within it). Postcard **H5** carries the reading order: the word `RAVEN` set apart in its text. Harald's sheet is relettered on its grid band only — `A, C, E, I, K, N, R, T, V` in place of the shared `A–I` run — so the five real cells fall under columns spelling `RAVEN` (`R6, A10, V9, E3, N2`). Reading them in that literal order gives `H, R, A, F, N`. Full mechanism and the worked example: [Props & specs].
**H4 and H5 built, 17 Sept 2026:** both cards' messages, Fun Facts and the puzzle content (H4's hand-copied rune key, H5's underlined `raven`) are done, front and back — see the Postcard system tab.
**Still open:** which container this feeds (Q-001).
