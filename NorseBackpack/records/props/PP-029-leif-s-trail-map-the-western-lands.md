---
id: PP-029
title: Leif's trail map (The Western Lands)
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
# Any related record IDs, e.g. [PZ-002, Q-004]
links: []
# Set to an ID when this record is replaced. It then moves to the Parked tab.
superseded_by:
tags: [old-PR-13]
---

Leif's laminated North Atlantic sea chart with seven animal vignettes. Print file: `Web/pdf/Trail_Map_1_Leif_Print.pdf`.

## Design notes (PP-029: Decided)

**Leif’s frame panned east one grid column.**

**Same scale, different window.** Requested as “the map moves one column left”: shift the lon window (was −69.8..−49.5) east by exactly one Q-024 grid column (2.94°) to −63.56..−37.06. Trims the empty Nunavik/Ungava Bay/Québec mass on the west and brings Greenland’s full coast into view — a pan, not a zoom; the scale bar is unchanged in km-per-inch.
**Iceland was tried and dropped.** At this scale Iceland’s coast sits 15.5° past even the shifted east edge — no single-column move reaches it. A separate, tighter frame (−65.5..−23.0) was built to test showing just its western tip: it works geometrically (stops safe, no leak), but was not adopted — the user asked for Frame B’s scale specifically, not a rescale.
**A real bug, caught by trying the literal ask.** The stops-in-frame guard checks a stop’s raw longitude against the frame’s nominal bounds. Qikiqtarjuaq (67.6°N) sits just outside those bounds after the shift and the guard correctly refused to build — but the guard was wrong to refuse: a conic projection’s meridians converge toward the pole, so the point’s actual *projected* position lands 1.83 in inside the printed map, verified by projecting it before trusting either the assertion or its relaxation. **Both frame guards were rewritten** to check the projected page position against the printed map area instead of the raw coordinate against the frame’s lon/lat box — the real question was always where the point lands on paper, not whether its coordinate reads as inside a rectangle that never gets drawn.
**The pan itself still cost one region label a collision**, unrelated to the guard question: HELLULAND’s label had to move (was 68.2,−68.6, now on-land at 68.5,−70.0) because its old position collided with Qikiqtarjuaq’s own label after the reframe — found by the stop-collision guard added in the grid session, which is exactly the case it exists for.
**Bonus, not designed for:** Brattahlíð / Qassiarsuk — Erik the Red’s estate, where Leif historically sailed from — is already in the research corpus and now falls inside the frame, so it labels for free as a decoy.

## Starting state

Not recorded yet.

## Reset

Not recorded yet.

## Replacement

Not recorded yet.
