---
id: PP-024
title: Viking Museum of Brattahlíð ticket
type: prop
# idea | candidate | decided | built | parked
status: decided
# physical | printed | digital
form: printed
# make | buy | print | 3d-print
source: print
# The play-test page shows the body's "## Player sees" section, or this prop's image asset.
# Where the player gets it: start (in the backpack) or the puzzle whose lock releases it, e.g. PZ-004
found_in: PZ-009
envelope: PZ-009
# Physical pocket/container or location; availability remains in found_in above.
container: Envelope 6
after_game: return
# Any related record IDs, e.g. [PZ-002, Q-004]
links: []
# Set to an ID when this record is replaced. It then moves to the Parked tab.
superseded_by:
tags: [old-PZ-12, old-PR-17]
---

**11 Oct 2026 (PR-007):** the backpack is now a box, and pockets and pouches are envelopes. Where this record mentions the bag, a pocket, a pouch or a lock, that is the earlier format; the `container` field gives the envelope.

## Design notes (PP-024: Decided)

**The museum ticket: a fictional museum, and the A–Z index on its back.**

**The museum is invented** — the **Viking Museum of Brattahlíð** — so nothing is printed under a real institution’s name. **Renamed, 28 Sept 2026** (was the Viking Museum of L’Anse aux Meadows): the user asked for the ticket to carry the same place as card LD, the card that points to it, so the link between them is not confusing. Front art `Museum_Ticket_Front_300dpi_v5_transparent.png` redraws only the two title lines (Constantia Bold, condensed) with `Props/MuseumTicket/rename_ticket_header.py`; the map art, the back and its A–Z index are unchanged, so the BEAR → 3212 lookup is unchanged. v4 is kept. Front is an ordinary admission ticket for that museum; back is a full A–Z visitor index, one exhibit name per letter, with a room number next to each. Only 13 letters are load-bearing for the current beast set (A, B, C, D, E, F, H, L, N, O, R, S, W); the other 13 exist purely as camouflage so the list doesn’t read as suspiciously short.
**Full index:** A Arrival Hall 1 · B Boat Shed 3 · C Compass Room 3 · D Dye Vats 4 · E Excavation Pit 2 · F Forge 5 · G Great Hall 8 · H Hearth House 5 · I Iron Bog 2 · J Jarl’s Quarters 7 · K Keel Yard 3 · L Longhouse 6 · M Midden 4 · N Navigation Room 3 · O Ocean Gallery 8 · P Palisade 9 · Q Quay 3 · R Rune Stone 2 · S Sod House 4 · T Tool Shed 5 · U Upper Meadow 9 · V Visitor Centre 1 · W Weaving Hut 4 · X X Marks the Site 2 · Y Yarn Room 4 · Z Zooarchaeology Lab 9.
**Resulting beast codes** (letter digits read in word order): BEAR 3212 (live until 16 Oct 2026, F1 pointer) · **WOLF 4865** (live since 16 Oct 2026, A6 pointer, PZ-005) · SEAL 4216 · ORCA 8231 · LOON 6883 · HARE 5122 · DEER 4222. No collision with any other code in the game (`1021`, `1972`, `231`, `582`, `427`, `2468`).
**Two minor notes, not blockers:** DEER lands on three repeated digits (4-2-2-2) — fine for a padlock, worth a rounder fallback only if DEER ever replaces BEAR as the live pointer; and no letter maps to `0`, so no code drawn from this index can ever contain a `0` — invisible to players.

## Design notes (PP-024: To re-print, 29 Sept 2026)

**Museum ticket (PP-024) needs proper duplex printing — home manual duplex can't hold registration.**

The ticket's flat background fill was dropped from both faces to save ink and let a 176 g/m² cream/tan cardstock supply the tint directly: the front's illustrated ground colour was colour-keyed to transparent in `Museum_Ticket_Front_300dpi_v3_transparent.png`, and the back's script-drawn `PAPER` fill was removed in `NorseBackpack/Props/MuseumTicket/build_museum_ticket_pdf.py` (the header band stays a filled dark green on both).
**Test print showed an angled front/back registration drift** — top edge lined up, bottom drifted roughly 1 mm on a alignment test sheet, and the actual ticket sheet drifted more, varying with how the paper was hand-fed back through the printer. This is paper-feed skew from manual flip-and-reinsert duplexing, not a file issue — the build script places front and back at the identical page coordinates. ~~Decided: print via a shop with true duplex equipment (or the printer's own auto-duplex unit, if it has one) rather than home manual duplex.~~ **Untested alternative added, 26 Sept 2026:** `NorseBackpack/Props/build_ticket_print_test_docx.py` applies the postcard PrintTest fix (Q-027 — keep everything in the reliable top zone of the page, flip top-to-bottom, print again) to this ticket. Rotated 90° landscape, its printed height is only 2 in, well inside the zone. Writes `NorseBackpack/Print/PrintTest_MuseumTicket.docx`, rasterized straight from `Museum_Ticket_Print.pdf` at 300dpi so it can never drift from the production build. **Carries over the postcard fix’s 1.5mm back-page shift unverified** — this ticket's cardstock (176 g/m²) differs from the postcard stock, so re-check on the first printed sheet rather than trusting the number. If it holds registration, this replaces the shop-print decision above; if not, the shop remains the fallback. `NorseBackpack/Print/_pdf_source/Museum_Ticket_Print.pdf` is already sized to the trimmed 2 × 5.5 in card if a shop route is still needed — no bleed is included, so confirm whether the shop's cutter needs a trim margin. **Rebuilt, 27 Sept 2026:** `build_ticket_print_test_docx.py` now uses the postcard settings confirmed on the L1/L2 print test — absolute positioning (no table), back mirrored from the right page edge for the long-edge flip, no back-page shift, and a 1.5 mm bleed on the back only (made by repeating each edge’s own pixels, since ticket backs are not one flat colour). It also now writes `NorseBackpack/Print/PrintTest_HnefataflTicket.docx`. Not yet printed. **29 Sept 2026:** the user will re-print it.

![Viking Museum of Brattahlíð ticket, front](Props/_Renders/Museum_Ticket_Front.png)Front

![Viking Museum of Brattahlíð ticket, back](Props/_Renders/Museum_Ticket_Back.png)Back

## Starting state

### 19 October 2026 tan paper Word variant

Designer requested a Word print file for tan paper. `Print/Brattahlid_Museum_Ticket_Tan_Paper.docx` contains the current adopted 3.5 × 6 inch ticket, front and back only, on two Letter pages. Created by `Props/build_tan_museum_docx.py` directly from the live PDF; all text and map image bytes preserved. Removes the cream page fill, alternating index row fills and solid green title band; title becomes dark green on bare paper. A PDF colour-key mask removes pale cream map-ground pixels (R 240–255, G 235–255, B 215–240); darker paths, water, trees, buildings and all nine numbered sites remain. Some illustration colour remains intentionally. No AI regeneration.

Uses the existing ticket print placement and rotations: front 0.6 inches from left, 0.3 from top, rotated clockwise; back mirrored from right with opposite rotation for the existing manual-flip method. Fine front outline is the trim guide. Source files retained; this is a separate coloured-stock variant. Verified both pages via Microsoft Word export and visual review; text extraction identical to source, dimensions unchanged. Standard renderer unavailable because LibreOffice is absent. Physical tan-stock contrast and duplex alignment remain untested. Print at 100%, one page per sheet; page 1 front, page 2 back.

Not recorded yet.

## Reset

Not recorded yet.

## Replacement

Not recorded yet.


## 17 Oct 2026: Museum index readability draft (Codex)

**Superseded in part by the designer feedback below.**

Designer requested the same readability treatment as the Rouen draft. Proposed ticket: **3.5 x 6 in**, with an **11 pt** A-Z index, **11.5 pt room numbers**, pale alternate rows and separated gallery/room columns. All 26 letters, gallery names and room values are imported from the current builder; WOLF still gives **4865**. The front uses Cinzel headings, cream/forest-green/rust museum styling and the existing illustrated visitor map, with every numbered building retained. Its baked header is clipped only during PDF layout; the source image is unchanged.

Review and print pack pages **1-2**. The taller ticket has nominal clearance in a 4.5 x 6.7 in envelope; physical fit remains untested. Layout and text bounds checked; no index entry changed. This is a proposed replacement, not an adoption of a new live size.


Shared source: `Props/ReadabilityDrafts/build_readability_drafts.py`. Outputs at repository root: `NorseBackpack/Print/_pdf_source/Readability_Redesign_Drafts/Readability_Drafts_Review.pdf` and `NorseBackpack/Print/_pdf_source/Readability_Redesign_Drafts/Readability_Drafts_Letter_Print.pdf`. These are separate review/print drafts; live sources, print masters, website copies and print-test DOCX files are unchanged. No new AI artwork was generated. Print the Letter pack at 100%, long-edge duplex. Paper readability, envelope fit and printer registration have not been tested.


## 17 Oct 2026: Designer correction - full-width Brattahlid map

The designer accepts the larger index but finds the narrow map strip on the front awkward. The ticket stays **3.5 x 6 in**, with the accepted reverse unchanged. The front now has a 96 pt dark-green museum heading/admission band and a **full-width 252 x 336 pt illustration**, without stretching or cropping. The map was recomposed through the built-in image generation tool in a 3:4 aspect ratio, retaining all nine numbered sites, the entrance, parking, north arrow, paths, shoreline and established green/rust style. It is the fictional museum illustration, not the puzzle's geographic trail map. No extra serial number. All nine markers 1-9 visually verified once each.

Source asset: `Props/ReadabilityDrafts/Brattahlid_Map_Wide_v1.png`; exact prompt also saved at `Props/ReadabilityDrafts/Brattahlid_Map_Wide_v1_prompt.txt`. Edit reference: `Props/MuseumTicket/Museum_Ticket_Front_300dpi_v5_transparent.png`. Review/Letter pages **1-2**. **Designer approved the full-width map on 17 Oct: "Good for the museum map, let's keep that."** This is the selected front design; accepted index unchanged. Retained unchanged in the review/print pack while Liv's note is revised; production masters have not yet been replaced.

**Exact built-in image-generation prompt:**

```text
Edit target: the attached Viking Museum of Brattahlid ticket illustration. Recompose ONLY its illustrated visitor map into a broader 3:4 portrait illustration that can fill the entire width of a new ticket. No ticket header, no footer, no admission text, no museum title, no border. Preserve the original hand-drawn flat illustrated style: forest green outlines, rust-orange timber roofs, sage water at the right edge, cream paper-colour ground approximately #F5EFDF, winding pale tan footpaths, turf and timber Viking museum buildings, shrubs, north arrow and entrance parking. Retain exactly nine rust circular location markers labelled 1 through 9, each numeral exactly once: 1 entrance/visitor centre at the bottom; 2 excavation site upper left; 3 boat shed and dock by the water upper right; 4 round turf hut left middle; 5 forge middle right; 6 longhouse centre; 7 turf house right; 8 large longhouse lower right; 9 small uppermost fenced chapel. Spread the locations across the width in a balanced, broader park layout with clear connecting paths; do not simply stretch the narrow original. All nine sites must fit completely. Paths are scenery, not a maze. Map illustration must fill the canvas edge to edge with modest breathing room, no narrow central strip. Only numerals 1-9 and north-arrow N are allowed. In particular omit the original No. 084726 serial number. Opaque cream background. Output one finished flat illustration, no mockup.
```

**17 Oct 2026 (designer): readability redesign adopted into the live print files** by `Props/ReadabilityDrafts/adopt_to_live.py` (old PDFs kept in `C:\EscapeBackpack\Norse_Snapshots\Norse_2026-10-17_PreReadability\`; the old builder is marked superseded for print). Brattahlid ticket is now 3.5 × 6 in: full-width illustrated museum map front, visitor index 11 pt. Page images and web copies rebuilt. Not paper-tested.

**20 Oct 2026 (designer): production print size** — Postcard 4 × 6 in (was 3.5 × 6). Decided in Q-052 (standard print sizes); not rebuilt yet. **Reopened later on 20 Oct** (designer: museum tickets smaller and all one size; travel tickets smaller, cheap and all one size); see Q-052.
## 20 October 2026 adopted 2 by 6 inch prototype
- Designer requested all museum tickets redesigned at 2 × 6 inches. Current builder: Props/build_museum_bookmarks.py. Brattahlíð uses the existing tall nine-site illustration at native 2-inch width, clipped at PDF placement to exclude the old baked header and serial/footer. All nine numbered sites remain visible; new typeset title/admission footer. No new generated artwork.
- Reverse reflowed to a single A–Z index with 9.5–10 pt gallery names, all original letter/name/room mappings preserved (WOLF → 4865 checked).
- Current Word: Print/Print_Museum_Brattahlid_2x6.docx, two Letter pages for front/back. Existing PrintTest_MuseumTicket.docx and Brattahlid_Museum_Ticket_Tan_Paper.docx refreshed as compatibility copies. Stable source/Letter PDFs replaced at exact 144 × 432 pt trim. Use tan stock, actual size, duplex long edge; calibration ruler/crop marks provided.
- Both Word pages visually inspected after Microsoft Word export. Physical readability and duplex alignment untested. Previous masters/previews archived in Norse_Archive/NorseBackpack/Props/MuseumBookmarks/Before_2x6_20261020/.


**20 Oct 2026 (designer): cut border** - Added a continuous cut line at the exact 2 x 6 inch outer edge on both faces and the Letter print sheets. Existing decorative frame retained. Current 2x6 Word file and compatibility copies rebuilt; all eight Word-exported museum pages inspected. Print at Actual size, long-edge duplex; physical alignment remains untested.

**20 Oct 2026 (designer): horizontal two-copy Word sheets** - Removed all external print instructions, heading and ruler. Letter sheets now contain two identical 6 x 2 inch horizontal tickets, x1.25 inches, top edges 0.5 and 2.75 inches. Page 1 fronts, page 2 matching backs rotated oppositely for long-edge duplex; cut borders and original card content preserved. Current named Word and compatibility copies rebuilt; all eight Word-exported pages inspected. Physical duplex test still required.

**20 Oct 2026: mixed pairs clarified** - Home-print set is now Print_Museums_Aud_Rouen_2x6.docx plus Print_Museums_Oslo_Brattahlid_2x6.docx in Print/. Each gives one of each named museum, two horizontal fronts near top and corresponding backs on page 2. Cut borders retained; no extra text. All four Word-exported pages inspected; physical duplex alignment untested.

**20 Oct 2026: paired-file cut borders front only** - Both Print_Museums_*_2x6.docx paired files now show outer cut borders on page 1 only. Page 2 retains decorative frames, with outer cut lines removed; artwork scale and registration unchanged. All four Word-exported pages visually inspected; physical duplex test remains open.
