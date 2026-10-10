---
id: PP-026
title: Treasure tally (four-wheel counter)
type: prop
# idea | candidate | decided | built | parked
status: decided
# physical | printed | digital
form: physical
# make | buy | print | 3d-print
source: 3d-print
# The play-test page shows the body's "## Player sees" section, or this prop's image asset.
# Where the player gets it: start (in the backpack) or the puzzle whose lock releases it, e.g. PZ-004
found_in: PZ-005
# Physical pocket/container or location; availability remains in found_in above.
container: Inside lockable pocket 1 (lock 7)
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

Not recorded yet.

## Reset

Turn all four wheels back to 0000.

## Replacement

Not recorded yet.
