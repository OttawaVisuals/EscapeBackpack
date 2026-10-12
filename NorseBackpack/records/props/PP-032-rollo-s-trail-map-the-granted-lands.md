---
id: PP-032
title: Rollo's trail map (The Granted Lands)
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
reset_name: Map: The Granted Lands
# Any related record IDs, e.g. [PZ-002, Q-004]
links: []
# Set to an ID when this record is replaced. It then moves to the Parked tab.
superseded_by:
tags: []
---

Rollo's laminated map with the six word icons and the story icons used by the rebus distance. Print file: `Web/pdf/Trail_Map_2_Rollo_Print.pdf`.


**11 Oct 2026 (playtest 1 feedback, built same day):** **Walcheren added to the sheet.** Players looked for the RD decoy and it was not there: `stops.js` files it as an “Island anchor”, which `load_corpus()` skips. New `decoy_towns` entry in the Rollo config (51.53, 3.55, the `stops.js` coordinate), placed right after the stops so a collision cannot drop it; a dropped decoy label is now reported like a dropped stop. No other label was lost (31 labels). Wider map rework is Q-053.

## Starting state

Not recorded yet.

## Reset

Not recorded yet.

## Replacement

Not recorded yet.
