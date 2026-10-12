---
id: PP-033
title: Musée Ducal de Rouen ticket
type: prop
# idea | candidate | decided | built | parked
status: decided
# physical | printed | digital
form: printed
# make | buy | print | 3d-print
source: print
# The play-test page shows the body's "## Player sees" section, or this prop's image asset.
# Where the player gets it: start (in the backpack) or the puzzle whose lock releases it, e.g. PZ-004
found_in: PZ-010
# Physical pocket/container or location; availability remains in found_in above.
container: Envelope 8
after_game: return
# Any related record IDs, e.g. [PZ-002, Q-004]
links: []
# Set to an ID when this record is replaced. It then moves to the Parked tab.
superseded_by:
tags: [old-PR-18]
---

**11 Oct 2026 (PR-007):** the backpack is now a box, and pockets and pouches are envelopes. Where this record mentions the bag, a pocket, a pouch or a lock, that is the earlier format; the `container` field gives the envelope.

## Design notes (PP-033: To re-print, 29 Sept 2026)

**The Musée Ducal de Rouen ticket (PZ-007), at 2 × 3 in.**

Built by `Props/RouenTicket/build_rouen_ticket_pdf.py`, following PP-024's museum ticket conventions (Cinzel headers, `#283B34`/`#B56A2A`/`#EFE3C4` ink/rust/paper palette) rather than introducing a new type system. Both faces are drawn with ReportLab — there is no single baked full-bleed front image this time, since Codex supplied only a standalone castle line icon (`TravelMap/Art/Rollo_Chateau_Robert_Le_Diable_Line_v1.png`, black ink, true alpha) rather than a complete ticket design. The build recolours that icon from black to the shared ink green in memory at build time, rather than saving a second permanent asset file.
**Fit risk carried over from PP-024:** that ticket found even a 2 in-wide card couldn't hold two legible columns of its 26-row A–Z index and had to drop to one column once the real front art fixed the physical size. This ticket's back needs two columns of 15 rows each at 2 × 3 in — smaller than L'Anse's card, but fewer, shorter rows. First build renders cleanly (row height ≈ 8.6 pt at 300 dpi) but has not been proof-printed at true size; treat it the way PP-024 treats its own duplex printing (PP-024) — parked until a real print is checked, not assumed to work from the PDF alone. **Updated, 26 Sept 2026:** the same PrintTest top-zone fix now exists for this ticket too, as `output/docx/PrintTest_RouenTicket.docx` (built by the same `NorseBackpack/Props/build_ticket_print_test_docx.py`, rotated 90° landscape, printed height only 2 in). Untested — check registration on the first printed sheet before trusting it. **Rebuilt, 27 Sept 2026:** `build_ticket_print_test_docx.py` now uses the postcard settings confirmed on the L1/L2 print test — absolute positioning (no table), back mirrored from the right page edge for the long-edge flip, no back-page shift, and a 1.5 mm bleed on the back only (made by repeating each edge’s own pixels, since ticket backs are not one flat colour). It also now writes `output/docx/PrintTest_HnefataflTicket.docx`. Not yet printed. **29 Sept 2026:** the user will re-print it.


**11 Oct 2026 (playtest 1 feedback, built same day):** **cut to 11 word pairs and re-jumbled.** Several pairs sat on the same row (sheep/mutton, fight/combat, deer/venison, cow/beef), so the matching solved itself. Kept: the six map pairs (fight/combat, hen/poultry, inn/tavern, folk/people, cow/beef, woodland/forest) plus five fillers (sheep/mutton, deer/venison, fire/flame, freedom/liberty, snake/serpent). Dropped: table/board, vision/sight, escape/flee, assemble/gather. Tags now run 1–11 and A–K (J, K past the map's last column). Every pair sits at least two rows apart and neither column's tags run in order. Load-bearing tags unchanged, so the code is still 1486. Rebuilt PDF, print-test docx and `Rouen_Ticket_*_300dpi.png`.

## Starting state

Not recorded yet.

## Reset

Not recorded yet.

## Replacement

Not recorded yet.
