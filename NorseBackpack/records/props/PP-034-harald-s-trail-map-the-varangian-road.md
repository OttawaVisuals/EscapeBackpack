---
id: PP-034
title: Harald's trail map (The Varangian Road)
type: prop
# idea | candidate | decided | built | parked
status: decided
# physical | printed | digital
form: printed
# make | buy | print | 3d-print
source: print
# The play-test page shows the body's "## Player sees" section, or this prop's image asset.
# Where the player gets it: start (in the backpack) or the puzzle whose lock releases it, e.g. PZ-004
found_in: PZ-011
envelope: PZ-011
# Physical pocket/container or location; availability remains in found_in above.
container: Envelope 10
after_game: return
reset_name: Map: The Varangian Road
# Any related record IDs, e.g. [PZ-002, Q-004]
links: []
# Set to an ID when this record is replaced. It then moves to the Parked tab.
superseded_by:
tags: [old-PR-04]
---

Harald's laminated map: front carries the branch-rune columns; back carries the hnefatafl board setup (stain over columns I–K). Print file: `Web/pdf/Trail_Map_4_Harald_Print.pdf`.

**14 Oct 2026 (designer, Q-052):** maps are **plain paper, not laminated**. They travel flat in 9 × 12 in envelopes (PR-007). Older mentions of lamination describe the earlier format. Printed on both sides: without a laminate, check on the chosen paper that neither face shows through enough to confuse the other (PP-036).

## Design notes (PP-034: Passed, 29 Sept 2026)

**Branch-rune legibility at final carved or printed size.**

The tally strokes must be countable with the magnifier and genuinely ambiguous without it. **Passed, 29 Sept 2026:** the user checked it at final size and it reads as intended.

## Starting state

Not recorded yet.

## Reset

Not recorded yet.

## Replacement

Not recorded yet.

**17 Oct 2026 (designer, PZ-008):** Harald's map now carries the hand-drawn hnefatafl shield icon (Codex) at grid square **I11** (the 4th column letter in A C E I K N R T V, row 11 counted from the top), drawn by `TravelMap/build_trail_maps_pdf.py` (harald config), in the print and answer PDFs. It marks the square of the last black move (I9-I11); it has no label, and the same icon is on the Hnefatafl Museum ticket (PP-036). The back page (board setup) still shows the old layout until the PZ-008 build. Web copies rebuilt.

**17 Oct 2026 (designer, PZ-008):** the shield icon moved from I11 to **I10** (the last black move is now K10-I10). Print and answer PDFs, page images and web copies rebuilt.

**17 Oct 2026 (designer, PZ-008):** page 2 of Harald's map (the board-setup back) is rebuilt from the new layout: 14 dark and 6 light visible in columns A to H, pencil arrows numbered 1 and 2 (E1-E6, H2-H5; placeholder pencil lines drawn in code, Codex may redraw), and Liv's smudge note with the move-3 riddle. The page is taller (bottom margin 130 pt). The shield icon is at I10.

**17 Oct 2026 (designer, Q-060):** base-map pass applied to Harald's sheet: single names (Staraya Ladoga, Novgorod, Constantinople, Solund), Denmark and Sweden dots dropped, bolder dots and names. Icon, stems and grid unchanged. Rebuilt.

**17 Oct 2026 (designer, Harald cleanup draft):** approved a larger transparent axe on the blue title band, larger/darker reverse-side instructions, and pencil-style numbered move arrows. Designer explicitly accepts the existing final digit 2; no route change requested. Separate two-page player/answer PDFs and page previews at `NorseBackpack/Print/_pdf_source/Harald_Cleanup_Draft/`; live outputs unchanged. Builder: `TravelMap/Drafts/build_harald_cleanup.py`. Front is patched only at the stamp, with text preserved and map above the title band pixel-identical at 144 dpi. Back reuses canonical board/stain/pieces, moves and note wording; captions 10.5 pt and note 11 pt in dark ink, arrows use lighter uneven pencil strokes and hand-drawn number rings. All four rendered pages inspected. Transparent axe made using built-in image_gen; exact prompt and asset at `TravelMap/Drafts/Harald_Axe_Transparent_v1_prompt.txt` and `.png`. Physical print test outstanding.

**17 Oct 2026 (designer correction, Harald reverse):** draft reverse is white for printing (including the board panel; the stain retains its natural tint). Ticket transfer includes I/J/K headings and both K11/K1 corner diamonds, so the draft smear now extends above/below the grid and leaves only faint dragged traces of those marks. Clean headings stop at H. Reuses canonical grid and visible pieces. Both draft PDFs rebuilt; reverse pages match, paper background verified white, reverse visually inspected, front-map pixel comparison and note-wording assertions pass. Ticket artwork unchanged.

**17 Oct 2026 (designer): cleanup draft adopted into the live print and answer PDFs** (`TravelMap/Drafts/build_harald_cleanup.py`; old copies in `C:\EscapeBackpack\Norse_Snapshots\Norse_2026-10-17_PreReadability\`; `build_trail_maps_pdf.py` carries a note that running it would overwrite them). Page images and web copies rebuilt. Not paper-tested. Larger transparent axe on the title band, larger and darker reverse note and captions, pencil-style arrows, white reverse, extended smudge. Route and the 2 unchanged.

**20 Oct 2026 (designer): production maps become half-letter, 5.5 × 8.5 in** (14 pt card flyers), carried in **6 × 9 in clasp envelopes**. The bottom title strip is removed and the trail icon (stamp) moves onto the map itself, so the map can use more of the card. **The prototype keeps the current Letter prints**; production files are separate. Codex will redo Aud's map at the new size. Consequences: the ruler (PP-025) must be rebuilt to the production Rollo map's scale; Harald's back (board note) fits at its current size, so the Oslo-ticket grid can stay. Supersedes the 8 × 10 idea above. See Q-049.


## 20 Oct 2026: Matching half-Letter professional-print proof (Codex)
Harald proof now matches the Aud half-Letter direction: 5.5 × 8.5 in trim, 0.125 in bleed, bottom title removed, axe identifier in the upper-right panel, 7.2 pt town names and 6.8 pt grid references. All 14 town names retained. A,C,E,I,K,N,R,T,V column labels preserved; all 12 branch-rune stems independently checked in their original cells. Labels avoid the rune symbols. Print-shop PDF has two pages; the original reverse board/note fits at 100%, retaining its font sizes and ticket-matching scale. Letter prototype and answer master unchanged.
Builder: TravelMap/build_other_half_letter_proofs.py. Files and review PNGs: C:/EscapeBackpack/output/other-maps-half-letter/. All_Maps_5.5x8.5_Print_Test_Pack.pdf includes all four fronts, Harald reverse and the matching ruler. Print the combined review pack single-sided at 100% / Actual size; separate Harald Letter test can be printed duplex, long edge. Native PDFs, safe area, source hashes and visual details checked. Design proof only; physical readability/player test outstanding.
