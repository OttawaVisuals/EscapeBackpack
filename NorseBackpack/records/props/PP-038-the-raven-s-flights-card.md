---
id: PP-038
title: The raven's flights card
type: prop
# idea | candidate | decided | built | parked
status: decided
# physical | printed | digital
form: printed
# make | buy | print | 3d-print
source: print
# The play-test page shows the body's "## Player sees" section, or this prop's image asset.
# Where the player gets it: start (in the backpack) or the puzzle whose lock releases it, e.g. PZ-004
found_in: PZ-008
envelope: PZ-008
# Physical pocket/container or location; availability remains in found_in above.
container: Envelope 11
after_game: return
# Any related record IDs, e.g. [PZ-002, Q-004]
links: []
# Set to an ID when this record is replaced. It then moves to the Parked tab.
superseded_by:
tags: [old-PR-26]
---

## Design notes (PP-038: To print and test)

**Produce The raven’s flights player card.**

The eight-perch, twelve-edge network and 2648 code are approved. Print the player view only, with four blank answer boxes, no HRAFN or answer overlay. Proposed half-Letter size needs proof. Release inside G7, before G8. Exact edges and the accepted visual are in Approved changes.

## Starting state

Not recorded yet.

## Reset

Not recorded yet.

## Replacement

Not recorded yet.

**20 Oct 2026 (designer): production print size** — Postcard 4 × 6 in (was 4 × 3). Decided in Q-052 (standard print sizes); not rebuilt yet.

**20 Oct 2026 (designer): production size decided** — Raven's path card → business card 3.5 × 2 in (was 4 × 3). See Q-052.

**20 Oct 2026 (Claude, designer's request): rebuilt at business-card size, 3.5 × 2 in, one side.** `Props/RavenFlights/build_raven_flights_pdf.py` now draws the same eight perches and twelve flights to fill the card inside a 0.125 in print-shop safe zone, with separate horizontal and vertical scales (an affine stretch, so no flight crosses another and every perch keeps its place in the layout). Text unchanged: flight digits Cinzel 11 pt, perch letters Cinzel Bold 12 pt. Perch rings 0.28 in across (were 0.32). The gap around each digit on the three short vertical flights (H–O 7, R–A 6, T–N 1) was narrowed so their line segments stay visible. HRAFN → 2648 check passes; PDF checked: one page, exactly 3.5 × 2 in, all 12 digits present, content 0.125 in from every edge. No background, as before (made for coloured paper; for stock business-card printing it prints on white unless a tint is added).
- Files: `Print/_pdf_source/Raven_Flights_Card_Print.pdf` (exact size), `Props/RavenFlights/Raven_Flights_Card_preview.png`, new home-print sheet **`Print/Print_RavenFlights_Card.docx`** (the card at 100 % with corner crop marks). The card is no longer printed from `Print/Print_LuggageTags.docx` (the tags are parked, PP-023); that sheet still shows the old 4 × 3 card and should not be used for it.
- The 4 × 3 version (preview, PDF, builder) is archived at `Norse_Archive/NorseBackpack/Props/RavenFlights/Before_Business_Card_20261020/`.
- Not done: paper test; the digital game's copy (`Digital/build_raven2_assets.py`) not rebuilt (digital follows the physical game).
