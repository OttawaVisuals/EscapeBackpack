---
id: PP-036
title: Hnefatafl Museum ticket, Oslo
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
# Any related record IDs, e.g. [PZ-002, Q-004]
links: []
# Set to an ID when this record is replaced. It then moves to the Parked tab.
superseded_by:
tags: [old-PR-09]
---

## Design notes (PP-036: Artwork approved · print test open)

**Does the mirrored wet-ticket transfer read through the paper and align with the board?**

**Approved, 25 Sept 2026:** handwritten board, retained organic smudge, “ticket was still wet” note and matching mirrored ticket reverse. [Current previews and all five PDFs] are built. This supersedes the old “map not built / artwork unfinished” status and glue explanation.
Print Harald's two-sided map and the ticket at **100% / actual size**, with no fit-to-page scaling. Hold the ticket to the light: the reflected I–K strip must become readable and align with the map's 0.4-inch grid. The transfer area must have no conflicting print on the opposite face; choose stock that allows read-through. Check that the smudge looks convincing and leaves enough grid visible to align it.
Test the map on the intended stock and laminate: neither its front reference grid nor its back setup should ghost through enough to confuse the other face. Digital geometry is checked; **physical print, read-through and laminate tests remain open**.


**11 Oct 2026 (playtest 1 feedback, built same day):** **front mini-board replaced.** The 5×5 board with king and four dark pieces was read as a setup to copy. It is now a three-square strip, dark · light (struck out) · dark, captioned “trapped between two: captured”, illustrating the capture rule (chosen in chat over removing it or a king drawing). Built in `Props/Hnefatafl/build_ticket_pdf.py`; render and print-test docx rebuilt.

## 16 Oct 2026: ticket reverse transfer texture

**Approved by the designer, 16 Oct 2026:** `Props/Hnefatafl/Hnefatafl_Ticket_Back_Smudged_v2.png` is the selected ticket reverse design. Strong sideways ink dragging, patchy grid transfer and smears around the three dark pieces and two orange diamonds make the drawing look transferred from the map back. Grid cells and piece positions remain readable. Exact built-in ImageGen prompt and method: `Props/Hnefatafl/TICKET_TRANSFER_SMUDGE_v2.md`. Asset AS-051 points to the approved artwork.

V1 was too subtle and is superseded by v2; both earlier artwork versions are retained as references. **Print integration remains pending:** the PDF builder and existing print PDFs still use the earlier artwork. Preserve the shared 0.4-inch grid when integrating; exact registration with the map and physical read-through remain untested.

## Starting state

Not recorded yet.

## Reset

Not recorded yet.

## Replacement

Not recorded yet.


**16 Oct 2026 (designer):** rules panel on the ticket front gains: “The king is captured only when dark pieces surround him on all four sides (the board edge counts).” Reason: the existing “trap an enemy piece between two of your own” could be read as the king dying with two. Rules text set slightly smaller and tighter to fit; print PDFs and web copies rebuilt, render checked. The board tool already worked this way; the solver now counts the edge too.

**17 Oct 2026 (designer):** the ticket front now shows the hand-drawn hnefatafl shield icon (Codex, `Props/Hnefatafl/Hnefatafl_Shield_Icon_HandDrawn_v1.png`, 36 pt, centred under the subtitle) so players link the same icon on Harald's map to this game. No caption on purpose (the designer wants Liv's text to stay vague about it). The capture strip and its caption moved 15 pt lower to make room; the rules text is unchanged. Print PDFs and web copies rebuilt, render checked.

**17 Oct 2026 (designer, PZ-008):** built for the 2134 design: the mirrored strip on the back now shows the five hidden pieces I6, I8, I9, K4 and K10 (K8 gone) from the new `board_layout.py`; the rules say “Dark pieces start around the edges, move first and try to trap him.” The Codex smudged versions of the strip (`Hnefatafl_Ticket_Back_Smudged_v1/v2.png`) show the OLD pieces and must be redone before they replace the vector strip. Print PDFs and web copies rebuilt.

**17 Oct 2026 (2134 smudge revision, Codex):** created `Props/Hnefatafl/Hnefatafl_Ticket_Back_Smudged_2134_v1.png` from the clean 2134 strip, using the older v2 strictly as a texture reference. Visually checked all five hatched pieces (left column rows 2/8; right column rows 3/4/6 from top), two left corner diamonds, eleven rows and three columns. Prompt/method in `Props/Hnefatafl/TICKET_TRANSFER_SMUDGE_2134_v1.md`. New artwork awaits review; earlier v2 remains a style reference with obsolete pieces. Print integration and precise registration/read-through remain pending.

**17 Oct 2026 (designer, Codex):** the ticket back now prints Codex's wet-ink transfer of the strip for the 2134 layout, `Props/Hnefatafl/Hnefatafl_Ticket_Back_Smudged_2134_v1.png` (887 x 1774 px = the whole card, made from `Hnefatafl_Ticket_Back_Clean_2134.png` with the old smudge as style; prompt and notes in `TICKET_TRANSFER_SMUDGE_2134_v1.md` and `CODEX_BRIEF_ticket_strip_2134.md`). Checked by pixel count: exactly five dark squares, at K10, K4, I9, I8 and I6, nothing on K8, the two corner diamonds kept, and each square's centre within 2 to 4 px (about 0.5 mm at print size) of the clean drawing. `build_ticket_pdf.py` uses the image when the file exists (delete it to fall back to the clean vector strip). Print PDFs, page images and web copies rebuilt. **Still open:** the physical read-through test (hold the ticket to the light over the map's grid) and a print on the real stock; the picture is generated, not pixel-identical, so the grid may sit a hair off.

**20 Oct 2026 (designer): production print size** — Bookmark 2 × 6 in (was about 2.6 × 5.2). Decided in Q-052 (standard print sizes); not rebuilt yet. **Reopened later on 20 Oct** (designer: museum tickets smaller and all one size; travel tickets smaller, cheap and all one size); see Q-052.
## 20 October 2026 adopted 2 by 6 inch prototype
- Designer requested museum tickets at 2 × 6 inches. Front reflowed by Props/build_museum_bookmarks.py: same shield, three-square capture example and all current rules, now 9.2 pt body text. New source supersedes older layout builder for print.
- Reverse preserves the adopted 2134 wet-transfer artwork as original PDF/image bytes, clipped/repositioned without scale change (translation only, -21.5,+29 pt). The nominal 0.4-inch cell pitch still matches the CURRENT Letter map-back master. Five pieces/corner diamonds retained. This version must not be mixed with the separate resized half-Letter production proofs, which have their own scale.
- Current Word: Print/Print_Museum_Oslo_2x6.docx; PrintTest_HnefataflTicket.docx refreshed. Stable source/Letter PDFs now 144 × 432 pt trim; original reverse stored as Props/MuseumBookmarks/Sources/Oslo_Original_Reverse.pdf for reproducibility. Original texture retains its baked paper tone; other substrate areas are unprinted.
- Both Word pages visually inspected after Microsoft Word export; rules, source-image hashes and translation-only transform verified. Physical registration/read-through and duplex alignment still untested. Earlier masters archived under Norse_Archive/NorseBackpack/Props/MuseumBookmarks/Before_2x6_20261020/.


**20 Oct 2026 (designer): cut border** - Added a continuous cut line at the exact 2 x 6 inch outer edge on both faces and the Letter print sheets. Existing decorative frame retained. Current 2x6 Word file and compatibility copies rebuilt; all eight Word-exported museum pages inspected. Print at Actual size, long-edge duplex; physical alignment remains untested.
**20 Oct 2026: white Oslo background** - Supersedes the baked-paper-tone note above. A PDF colour-key transparency mask removes the beige paper from the original reverse image; blank areas now render white. Embedded image bytes, translation-only placement, grid scale and five piece positions retained. Print Oslo on white stock. Prior masters and Word files archived in Norse_Archive/NorseBackpack/Props/MuseumBookmarks/Before_CutBorder_White_Oslo_20261020/.

**20 Oct 2026 (designer): horizontal two-copy Word sheets** - Removed all external print instructions, heading and ruler. Letter sheets now contain two identical 6 x 2 inch horizontal tickets, x1.25 inches, top edges 0.5 and 2.75 inches. Page 1 fronts, page 2 matching backs rotated oppositely for long-edge duplex; cut borders and original card content preserved. Current named Word and compatibility copies rebuilt; all eight Word-exported pages inspected. Physical duplex test still required.

**20 Oct 2026: mixed pairs clarified** - Home-print set is now Print_Museums_Aud_Rouen_2x6.docx plus Print_Museums_Oslo_Brattahlid_2x6.docx in Print/. Each gives one of each named museum, two horizontal fronts near top and corresponding backs on page 2. Cut borders retained; no extra text. All four Word-exported pages inspected; physical duplex alignment untested.

**20 Oct 2026: paired-file cut borders front only** - Both Print_Museums_*_2x6.docx paired files now show outer cut borders on page 1 only. Page 2 retains decorative frames, with outer cut lines removed; artwork scale and registration unchanged. All four Word-exported pages visually inspected; physical duplex test remains open.
