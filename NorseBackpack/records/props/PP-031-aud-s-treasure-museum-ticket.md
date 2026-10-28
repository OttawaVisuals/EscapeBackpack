---
id: PP-031
title: Aud's Treasure Museum ticket
type: prop
# idea | candidate | decided | built | parked
status: decided
# physical | printed | digital
form: printed
# make | buy | print | 3d-print
source: print
# The play-test page shows the body's "## Player sees" section, or this prop's image asset.
# Where the player gets it: start (in the backpack) or the puzzle whose lock releases it, e.g. PZ-004
found_in: PZ-004
envelope: PZ-004
# Physical pocket/container or location; availability remains in found_in above.
container: Envelope 4
after_game: return
# Any related record IDs, e.g. [PZ-002, Q-004]
links: []
# Set to an ID when this record is replaced. It then moves to the Parked tab.
superseded_by:
tags: []
---

Aud's Treasure Museum ticket. Front carries "The Coin Room" merchant's key; back lists the six route directions. Builder: `Props/AudTicket/build_aud_ticket_pdf.py` (page 3 is the answer copy and is not packed).

## Starting state

### 19 October 2026 tan paper Word variant

Designer requested a Word print file for tan paper. `Print/Aud_Museum_Ticket_Tan_Paper.docx` contains the adopted 3.5 × 6 inch ticket, front and back only, on two Letter pages. `Props/build_tan_museum_docx.py` removes the flat cream page fills directly from the live PDF and preserves all text, coin artwork, rarity colours, group symbols, values and route directions. The designer answer page is excluded. No AI artwork regeneration; original masters retained.

Matches the existing ticket print placement/rotations, with a fine front trim outline. Verified both pages through Microsoft Word PDF export and visual review; text extraction identical to source, dimensions unchanged. Standard renderer unavailable because LibreOffice is absent. Physical contrast and duplex registration on tan stock remain untested. Print at 100%, one page per sheet; page 1 front, page 2 back, using the existing manual ticket flip.

Not recorded yet.

## Reset

Not recorded yet.

## Replacement

Not recorded yet.


## 17 Oct 2026: Aud ticket readability draft (Codex)

Designer requested the same readability treatment as the Rouen draft. Proposed ticket: **3.5 x 6 in**. All six route directions are printed verbatim at **11.5 pt**, with 14.5 pt leading, distinct numbered blocks and separating rules. No tally boxes, worked example or solution was added to the player face. The front also grows: **10.5 pt coin names, 11.5 pt values**, 27 pt coin pictures and larger group emblems. Seven coins, their ordering, pictures, rarity colours, three group emblems and values come directly from the live builder. Route answer **532**, selected coin total **3705** and SOLE mechanism unchanged.

Review and print pack pages **3-4**. Existing answer-copy PDF remains the designer reference and was not changed. All directions and values verified; the draft has not been walked against the physical map. Proposed replacement only.


Shared source: `Props/ReadabilityDrafts/build_readability_drafts.py`. Outputs at repository root: `NorseBackpack/Print/_pdf_source/Readability_Redesign_Drafts/Readability_Drafts_Review.pdf` and `NorseBackpack/Print/_pdf_source/Readability_Redesign_Drafts/Readability_Drafts_Letter_Print.pdf`. These are separate review/print drafts; live sources, print masters, website copies and print-test DOCX files are unchanged. No new AI artwork was generated. Print the Letter pack at 100%, long-edge duplex. Paper readability, envelope fit and printer registration have not been tested.


**17 Oct 2026, designer feedback:** Aud draft accepted as a design; both faces unchanged in the corrected draft pack. Still a separate draft, not yet copied to live print/web outputs.

**17 Oct 2026 (designer): readability redesign adopted into the live print files** by `Props/ReadabilityDrafts/adopt_to_live.py` (old PDFs kept in `C:\EscapeBackpack\Norse_Snapshots\Norse_2026-10-17_PreReadability\`; the old builder is marked superseded for print). Aud ticket is now 3.5 × 6 in: coin room, 11.5 pt directions; the old designer answer-copy page stays as page 3 (old 3 × 4 in size, old layout). Page images and web copies rebuilt. Not paper-tested.

**20 Oct 2026 (designer): production print size** — Postcard 4 × 6 in (was 3.5 × 6). Decided in Q-052 (standard print sizes); not rebuilt yet. **Reopened later on 20 Oct** (designer: museum tickets smaller and all one size; travel tickets smaller, cheap and all one size); see Q-052.
## 20 October 2026 adopted 2 by 6 inch prototype
- Designer adopted the 2 × 6 inch museum format. Built by Props/build_museum_bookmarks.py. Coin key reflowed with each name/value on two lines beside its original coin image, retaining all seven labels/values, rare/common artwork and camel/fleur/fehu groups. Reused embedded original coin images without redrawing them.
- Reverse preserves all six current direction strings, 11.5 pt body text, clear numbered paragraphs. No answer copy included in the two-page player PDF or Word export; previous designer answer page retained in the archived original PDF.
- Current Word: Print/Print_Museum_Aud_2x6.docx. Existing PrintTest_AudTicket.docx and Aud_Museum_Ticket_Tan_Paper.docx refreshed. Source/Letter PDF paths stable, 144 × 432 pt trim, tan-stock background unprinted, duplex long edge at 100% with crop marks/ruler.
- Both Word pages inspected; all original labels/values/directions verified. Physical reading/alignment untested. Old masters in Norse_Archive/NorseBackpack/Props/MuseumBookmarks/Before_2x6_20261020/.


**20 Oct 2026 (designer): cut border** - Added a continuous cut line at the exact 2 x 6 inch outer edge on both faces and the Letter print sheets. Existing decorative frame retained. Current 2x6 Word file and compatibility copies rebuilt; all eight Word-exported museum pages inspected. Print at Actual size, long-edge duplex; physical alignment remains untested.

**20 Oct 2026 (designer): horizontal two-copy Word sheets** - Removed all external print instructions, heading and ruler. Letter sheets now contain two identical 6 x 2 inch horizontal tickets, x1.25 inches, top edges 0.5 and 2.75 inches. Page 1 fronts, page 2 matching backs rotated oppositely for long-edge duplex; cut borders and original card content preserved. Current named Word and compatibility copies rebuilt; all eight Word-exported pages inspected. Physical duplex test still required.

**20 Oct 2026: mixed pairs clarified** - Home-print set is now Print_Museums_Aud_Rouen_2x6.docx plus Print_Museums_Oslo_Brattahlid_2x6.docx in Print/. Each gives one of each named museum, two horizontal fronts near top and corresponding backs on page 2. Cut borders retained; no extra text. All four Word-exported pages inspected; physical duplex alignment untested.

**20 Oct 2026: paired-file cut borders front only** - Both Print_Museums_*_2x6.docx paired files now show outer cut borders on page 1 only. Page 2 retains decorative frames, with outer cut lines removed; artwork scale and registration unchanged. All four Word-exported pages visually inspected; physical duplex test remains open.
