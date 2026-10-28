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
envelope: PZ-010
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
**Fit risk carried over from PP-024:** that ticket found even a 2 in-wide card couldn't hold two legible columns of its 26-row A–Z index and had to drop to one column once the real front art fixed the physical size. This ticket's back needs two columns of 15 rows each at 2 × 3 in — smaller than L'Anse's card, but fewer, shorter rows. First build renders cleanly (row height ≈ 8.6 pt at 300 dpi) but has not been proof-printed at true size; treat it the way PP-024 treats its own duplex printing (PP-024) — parked until a real print is checked, not assumed to work from the PDF alone. **Updated, 26 Sept 2026:** the same PrintTest top-zone fix now exists for this ticket too, as `NorseBackpack/Print/PrintTest_RouenTicket.docx` (built by the same `NorseBackpack/Props/build_ticket_print_test_docx.py`, rotated 90° landscape, printed height only 2 in). Untested — check registration on the first printed sheet before trusting it. **Rebuilt, 27 Sept 2026:** `build_ticket_print_test_docx.py` now uses the postcard settings confirmed on the L1/L2 print test — absolute positioning (no table), back mirrored from the right page edge for the long-edge flip, no back-page shift, and a 1.5 mm bleed on the back only (made by repeating each edge’s own pixels, since ticket backs are not one flat colour). It also now writes `NorseBackpack/Print/PrintTest_HnefataflTicket.docx`. Not yet printed. **29 Sept 2026:** the user will re-print it.


**11 Oct 2026 (playtest 1 feedback, built same day):** **cut to 11 word pairs and re-jumbled.** Several pairs sat on the same row (sheep/mutton, fight/combat, deer/venison, cow/beef), so the matching solved itself. Kept: the six map pairs (fight/combat, hen/poultry, inn/tavern, folk/people, cow/beef, woodland/forest) plus five fillers (sheep/mutton, deer/venison, fire/flame, freedom/liberty, snake/serpent). Dropped: table/board, vision/sight, escape/flee, assemble/gather. Tags now run 1–11 and A–K (J, K past the map's last column). Every pair sits at least two rows apart and neither column's tags run in order. Load-bearing tags unchanged, so the code is still 1486. Rebuilt PDF, print-test docx and `Rouen_Ticket_*_300dpi.png`.

## 17 Oct 2026: Codex readability redesign draft

The designer found the enlarged type in the 2 x 3 in layout unsatisfactory and authorized a fresh layout, including a different ticket size. **Separate review draft, not yet adopted:** 3.5 x 5.5 in portrait, with 12 pt words, 11.5 pt tags, an 11 pt matching instruction, 19 pt row spacing and two clearly separated columns. The dimensions leave nominal room in the proposed 4.5 x 6.7 in small envelopes; actual envelope fit and printing have not been tested.

The front retains the existing castle line illustration and Cinzel museum lettering, now with an architectural arch backdrop and a bilingual dark-green admission panel. Cream paper, forest-green ink and darker rust accents keep it in the existing museum-ticket family. The back gains Saxon/Norman column headings and separate high-contrast tags in IBM Plex Mono (distinguishable I and 1); ordinary word text remains Helvetica. No new clue-bearing serial numbers, dates or iconography. The exact 11 pairs, both shuffled orders and all tags are imported from the live builder. Puzzle coordinates I6, F7, A3, B9 and answer 1486 remain unchanged.

Source: `Props/RouenTicket/build_rouen_ticket_redesign.py`. Existing builder, live print/web PDFs, PNGs and print-test DOCX are unchanged. No new AI image was generated; the castle asset is reused through the live builder's existing recolouring function.

- Ticket: `NorseBackpack/Print/_pdf_source/Rouen_Redesign_Draft/Rouen_Ticket_Redesign.pdf` (repository-root path; two ticket-sized pages).
- Print sheet: `NorseBackpack/Print/_pdf_source/Rouen_Redesign_Draft/Rouen_Ticket_Redesign_Letter.pdf` (two centred US Letter pages, crop marks, 100% printing, long-edge duplex).
- Preview: `NorseBackpack/Print/_pdf_source/Rouen_Redesign_Draft/Rouen_Ticket_Redesign_Preview.png`.

Both PDFs rendered and all four pages visually checked. Word widths and solution coordinates checked at build time. Physical readability, printer registration and envelope fit still need a paper check. The earlier 17 Oct enlargement note describes the live version; this draft is the proposed replacement.

## Starting state

Not recorded yet.

## Reset

Not recorded yet.

## Replacement

Not recorded yet.

**17 Oct 2026 (designer, Q-063): word list enlarged.** The back's word pairs and tags went from 5.6–5.8 pt to **10 pt**, and the instruction from 4.6 pt to 7 pt on two lines (header 54 pt tall, was 46). The ticket stays 2 × 3 in and 11 rows (row pitch about 12.5 pt); no redesign was needed. Tags, word order and answers unchanged. Print PDFs, page images and web copies rebuilt; render checked. Not paper-tested.

**17 Oct 2026 (designer): readability redesign adopted into the live print files** by `Props/ReadabilityDrafts/adopt_to_live.py` (old PDFs kept in `C:\EscapeBackpack\Norse_Snapshots\Norse_2026-10-17_PreReadability\`; the old builder is marked superseded for print). The Codex redesign (3.5 × 5.5 in, 12 pt words, 11.5 pt tags) replaces my 10 pt 2 × 3 in version above; word pairs and tags unchanged.

**20 Oct 2026 (designer): production print size** — Postcard 4 × 6 in (was 3.5 × 5.5). Decided in Q-052 (standard print sizes); not rebuilt yet. **Reopened later on 20 Oct** (designer: museum tickets smaller and all one size; travel tickets smaller, cheap and all one size); see Q-052.
## 20 October 2026 adopted 2 by 6 inch prototype
- Designer adopted 2 × 6 inch museum tickets. Reflowed by Props/build_museum_bookmarks.py, retaining the original castle art and heritage typography. Reverse stacks Saxon and Norman lists vertically to retain 12 pt puzzle words in the narrow format. Both lists retain their original independent shuffled order and every word/tag mapping.
- Checked fight/combat → I6, folk/people → F7, hen/poultry → A3, inn/tavern → B9. No puzzle mechanism or answer change.
- Current Word: Print/Print_Museum_Rouen_2x6.docx; PrintTest_RouenTicket.docx refreshed as compatibility copy. Stable source/Letter PDFs now 144 × 432 pt trim. Two aligned Letter faces, tan stock, actual size, duplex long edge, crop marks and one-inch ruler. Both Word pages visually inspected; physical readability/alignment untested. Previous masters archived under Norse_Archive/NorseBackpack/Props/MuseumBookmarks/Before_2x6_20261020/.


**20 Oct 2026 (designer): cut border** - Added a continuous cut line at the exact 2 x 6 inch outer edge on both faces and the Letter print sheets. Existing decorative frame retained. Current 2x6 Word file and compatibility copies rebuilt; all eight Word-exported museum pages inspected. Print at Actual size, long-edge duplex; physical alignment remains untested.

**20 Oct 2026 (designer): horizontal two-copy Word sheets** - Removed all external print instructions, heading and ruler. Letter sheets now contain two identical 6 x 2 inch horizontal tickets, x1.25 inches, top edges 0.5 and 2.75 inches. Page 1 fronts, page 2 matching backs rotated oppositely for long-edge duplex; cut borders and original card content preserved. Current named Word and compatibility copies rebuilt; all eight Word-exported pages inspected. Physical duplex test still required.

**20 Oct 2026: mixed pairs clarified** - Home-print set is now Print_Museums_Aud_Rouen_2x6.docx plus Print_Museums_Oslo_Brattahlid_2x6.docx in Print/. Each gives one of each named museum, two horizontal fronts near top and corresponding backs on page 2. Cut borders retained; no extra text. All four Word-exported pages inspected; physical duplex alignment untested.

**20 Oct 2026 (designer): Saxon list in number order** - First matching-game list now runs 1 fire, 2 cow, 3 hen, 4 sheep, 5 snake, 6 fight, 7 folk, 8 freedom, 9 inn, 10 woodland, 11 deer. Norman list remains shuffled with unchanged tags; all answer mappings retained. Authoritative SAXON data updated in Props/RouenTicket/build_rouen_ticket_pdf.py; rebuilt through current Props/build_museum_bookmarks.py. Rouen source/Letter PDF, named Word/compatibility copy, Aud-Rouen pair and web copies/previews refreshed. Word exports visually checked. Prior masters/Word/previews archived under Before_Rouen_Number_Order_20261020/.

**20 Oct 2026: paired-file cut borders front only** - Both Print_Museums_*_2x6.docx paired files now show outer cut borders on page 1 only. Page 2 retains decorative frames, with outer cut lines removed; artwork scale and registration unchanged. All four Word-exported pages visually inspected; physical duplex test remains open.
