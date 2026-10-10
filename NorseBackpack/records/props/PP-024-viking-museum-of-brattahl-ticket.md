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
# Physical pocket/container or location; availability remains in found_in above.
container: Large pouch, in the main compartment (lock 6)
after_game: return
# Any related record IDs, e.g. [PZ-002, Q-004]
links: []
# Set to an ID when this record is replaced. It then moves to the Parked tab.
superseded_by:
tags: [old-PZ-12, old-PR-17]
---

## Design notes (PP-024: Decided)

**The museum ticket: a fictional museum, and the A–Z index on its back.**

**The museum is invented** — the **Viking Museum of Brattahlíð** — so nothing is printed under a real institution’s name. **Renamed, 28 Sept 2026** (was the Viking Museum of L’Anse aux Meadows): the user asked for the ticket to carry the same place as card LD, the card that points to it, so the link between them is not confusing. Front art `Museum_Ticket_Front_300dpi_v5_transparent.png` redraws only the two title lines (Constantia Bold, condensed) with `Props/MuseumTicket/rename_ticket_header.py`; the map art, the back and its A–Z index are unchanged, so the BEAR → 3212 lookup is unchanged. v4 is kept. Front is an ordinary admission ticket for that museum; back is a full A–Z visitor index, one exhibit name per letter, with a room number next to each. Only 13 letters are load-bearing for the current beast set (A, B, C, D, E, F, H, L, N, O, R, S, W); the other 13 exist purely as camouflage so the list doesn’t read as suspiciously short.
**Full index:** A Arrival Hall 1 · B Boat Shed 3 · C Compass Room 3 · D Dye Vats 4 · E Excavation Pit 2 · F Forge 5 · G Great Hall 8 · H Hearth House 5 · I Iron Bog 2 · J Jarl’s Quarters 7 · K Keel Yard 3 · L Longhouse 6 · M Midden 4 · N Navigation Room 3 · O Ocean Gallery 8 · P Palisade 9 · Q Quay 3 · R Rune Stone 2 · S Sod House 4 · T Tool Shed 5 · U Upper Meadow 9 · V Visitor Centre 1 · W Weaving Hut 4 · X X Marks the Site 2 · Y Yarn Room 4 · Z Zooarchaeology Lab 9.
**Resulting beast codes** (letter digits read in word order): **BEAR 3212** (currently live, per old page PZ-10’s F1 pointer) · WOLF 4865 · SEAL 4216 · ORCA 8231 · LOON 6883 · HARE 5122 · DEER 4222. No collision with any other code in the game (`1021`, `1972`, `231`, `582`, `427`, `2468`).
**Two minor notes, not blockers:** DEER lands on three repeated digits (4-2-2-2) — fine for a padlock, worth a rounder fallback only if DEER ever replaces BEAR as the live pointer; and no letter maps to `0`, so no code drawn from this index can ever contain a `0` — invisible to players.

## Design notes (PP-024: To re-print, 29 Sept 2026)

**Museum ticket (PP-024) needs proper duplex printing — home manual duplex can't hold registration.**

The ticket's flat background fill was dropped from both faces to save ink and let a 176 g/m² cream/tan cardstock supply the tint directly: the front's illustrated ground colour was colour-keyed to transparent in `Museum_Ticket_Front_300dpi_v3_transparent.png`, and the back's script-drawn `PAPER` fill was removed in `NorseBackpack/Props/MuseumTicket/build_museum_ticket_pdf.py` (the header band stays a filled dark green on both).
**Test print showed an angled front/back registration drift** — top edge lined up, bottom drifted roughly 1 mm on a alignment test sheet, and the actual ticket sheet drifted more, varying with how the paper was hand-fed back through the printer. This is paper-feed skew from manual flip-and-reinsert duplexing, not a file issue — the build script places front and back at the identical page coordinates. ~~Decided: print via a shop with true duplex equipment (or the printer's own auto-duplex unit, if it has one) rather than home manual duplex.~~ **Untested alternative added, 26 Sept 2026:** `NorseBackpack/Props/build_ticket_print_test_docx.py` applies the postcard PrintTest fix (Q-027 — keep everything in the reliable top zone of the page, flip top-to-bottom, print again) to this ticket. Rotated 90° landscape, its printed height is only 2 in, well inside the zone. Writes `output/docx/PrintTest_MuseumTicket.docx`, rasterized straight from `Museum_Ticket_Print.pdf` at 300dpi so it can never drift from the production build. **Carries over the postcard fix’s 1.5mm back-page shift unverified** — this ticket's cardstock (176 g/m²) differs from the postcard stock, so re-check on the first printed sheet rather than trusting the number. If it holds registration, this replaces the shop-print decision above; if not, the shop remains the fallback. `output/pdf/Museum_Ticket_Print.pdf` is already sized to the trimmed 2 × 5.5 in card if a shop route is still needed — no bleed is included, so confirm whether the shop's cutter needs a trim margin. **Rebuilt, 27 Sept 2026:** `build_ticket_print_test_docx.py` now uses the postcard settings confirmed on the L1/L2 print test — absolute positioning (no table), back mirrored from the right page edge for the long-edge flip, no back-page shift, and a 1.5 mm bleed on the back only (made by repeating each edge’s own pixels, since ticket backs are not one flat colour). It also now writes `output/docx/PrintTest_HnefataflTicket.docx`. Not yet printed. **29 Sept 2026:** the user will re-print it.

![Viking Museum of Brattahlíð ticket, front](Props/_Renders/Museum_Ticket_Front.png)Front

![Viking Museum of Brattahlíð ticket, back](Props/_Renders/Museum_Ticket_Back.png)Back

## Starting state

Not recorded yet.

## Reset

Not recorded yet.

## Replacement

Not recorded yet.
