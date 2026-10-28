---
id: PP-026
title: Treasure tally
type: prop
# idea | candidate | decided | built | parked
status: decided
# physical | printed | digital
form: printed
# make | buy | print | 3d-print
source: print
# The play-test page shows the body's "## Player sees" section, or this prop's image asset.
# Where the player gets it: start (in the backpack) or the puzzle whose lock releases it, e.g. PZ-004
found_in: PZ-005
envelope: PZ-005
# Physical pocket/container or location; availability remains in found_in above.
container: Envelope 7
after_game: return
# Any related record IDs, e.g. [PZ-002, Q-004]
links: []
# Set to an ID when this record is replaced. It then moves to the Parked tab.
superseded_by:
tags: [old-PR-24]
---

## Design notes (PP-026: Decided design · print test open)

**Four-wheel treasure tally chosen (25 Sept 2026).**

The user chose wheels over a calculator so the numeral shapes can be controlled. Mechanism: the free Printables *4-digit counter* by BMdesign (reference file `Props/SoleTally/reference/4-digit_counter.3mf`); its base and end caps are used as-is. Only the counter ring is replaced: `Props/SoleTally/sole_tally_ring.scad` fills the reference digits and cuts strict seven-segment digits 0–9 (0.55 mm deep), plus a flush inlay part for a second colour. Reason: the reference 7 has a slanted stroke that does not read as L upside down. Rebuild with `python build_sole_tally.py`; `SOLE_ring_check.png` shows 3705 turned 180° reading SOLE. Still open: colour method (the recorded Prusa i3 MK3S+ is single-extruder and the digits sit on the vertical faces, so a layer colour swap will not work; without a multi-material unit, print the body alone and fill the 0.55 mm recesses with paint or wax); print test (fit, click feel, legibility at 5.6 × 3.4 mm); Printables licence check before any sharing, and a Norse-styled look if wanted.

## Starting state

### 19 October 2026 paper slider prototype

Designer requested a home-printer paper version, approved the slider direction and requested Word templates plus illustrated instructions. This is the current paper prototype; the earlier 3D-print files are retained as an alternative. No puzzle wording, coin values or answer changed.

- Print templates: `Print/Print_Paper_Treasure_Tally.docx`, two single-sided Letter pages. Page 1 on tan cardstock: front, backing and ten rails; page 2 on light green or white cardstock: four complete strips. Black ink only, no background fill. Both pages have a 1-inch calibration line; print at 100%, one page per sheet.
- Maker guide: `Print/Paper_Treasure_Tally_Illustrated_Instructions.docx`, three pages with seven deterministic assembly diagrams. Includes print/cut steps, rail layout, side section, strip placement, paper-clip retention, reset and a clearly marked maker-only solution check. Do not pack the guide with player materials.
- Geometry: 6 × 2.5 inch sleeve; four 8 inch strips, each 0.75 inch wide with 1.15 inch end tabs; four 0.9 inch channels separated by five rails, each made of two cardstock layers. Digit pitch 0.55 inches; windows 0.58 × 0.5 inches. At each extreme digit setting, the end tab remains 0.075 inches clear of the sleeve. The shorter sleeve replaces the visual mockup's 4-inch height so all ten digits can be selected with captive tabs.
- Four small paper clips grip the front, slider and backing at the lower edge after setting the total; remove clips to adjust. This avoids relying on untested cardstock friction to hold the reveal. Strips extend beyond the sleeve and must be stored flat; the concept image understates their length.
- Builder: `Props/SoleTally/build_paper_slider.py`. Does not use the third-party counter geometry or AI-generated template artwork. Uses explicit seven-segment shapes; assertions verify channel clearance, end-tab clearance, digit spacing and the exact 3705 → SOLE rotation.
- QA: both template pages and all three instruction pages exported through Microsoft Word and visually inspected. Standard renderer unavailable because LibreOffice is absent; Word export succeeded. Working diagrams, PDFs, page renders and geometry check JSON: `C:\EscapeBackpack\output\paper-tally`. Physical cutting accuracy, stock/tape thickness, sliding friction, clip grip and durability remain untested. Dry-fit the assembly before permanent gluing.

Not recorded yet.

## Reset

### 19 October 2026 compact paper version

Designer found the eight-inch strips too tall and requested a smaller version while retaining readability. Created `Print/Print_Paper_Treasure_Tally_Compact.docx` (2 Letter pages) and `Print/Paper_Treasure_Tally_Illustrated_Instructions_Compact.docx` (3 pages). Earlier files retained for comparison. Build with `Props/SoleTally/build_paper_slider.py --compact`.

Compact strips are **6 inches long (25% shorter)**. Digits are drawn **0.3 inches / 7.62 mm tall**, with 0.4 inch pitch. The sleeve and all rail pieces shrink to **6 × 2 inches**; windows are 0.58 × 0.38 inches. Strip width, channel width and end-tab width are unchanged; end tabs are 0.125 inches tall. The exact 0.075 inch end-tab clearance remains at both extreme settings. Use the two compact template pages together; the original taller sleeve cannot be used with the shorter strips. Heading remains 17 pt and instruction 11 pt.

Geometry and rotation checks pass, including neighbour-digit exclusion. All five final Word pages exported and visually inspected. Standard renderer still unavailable (no LibreOffice); Microsoft Word export succeeded. QA at `C:\EscapeBackpack\output\paper-tally-compact`. Physical readability, motion, clip grip and thinner-tab durability remain untested.

Paper version: remove the four paper clips, set all four sliders to 0000, then reattach the clips and store flat. Earlier 3D version: turn all four wheels to 0000.

## Replacement

### 19 October 2026 envelope width correction

Designer clarified that the current small envelope measures **6.7 × 4.5 inches**, and correctly proposed keeping six-inch sliders while narrowing the viewing sleeve to four inches. Implemented as the current compact layout: **4 × 2 inch sleeve**, **6 inch strips**, **4 × 6 inch stored footprint at 0000**. Mixed digit settings extend farther; reset to 0000 before packing. Actual envelope opening/internal clearance and clip thickness still require a physical check.

Current Word files are `Print/Print_Paper_Treasure_Tally_Compact_4x6_Envelope.docx` and `Print/Paper_Treasure_Tally_Illustrated_Instructions_Compact_4x6_Envelope.docx`. All pieces are revised together: strip width 0.55 inches, channel width 0.65 inches, rail width 0.25 inches, end-tab width 0.85 inches, windows 0.38 × 0.38 inches. Digit height stays 0.3 inches / 7.62 mm; pitch, total strip length and 0.075 inch extreme-setting tab clearance unchanged. Build with `build_paper_slider.py --compact`. Do not mix previous wider parts with this version.

Both template pages and all three instruction pages exported through Word and visually checked. Digital assertions check strip/rail clearance, caps within the sleeve width, full travel, stored footprint and the reveal. The earlier compact Word file was open/locked, so revised files use new explicit envelope-size names; older compact documents retained, with safety copies in `C:\EscapeBackpack\Norse_Archive\Print\Tally_Compact_Before_4inch_Width`. Physical motion, readability and envelope fit remain untested.

Not recorded yet.
