---
id: Q-044
title: Digital ruler: which six scales, and how to measure a diagonal?
type: question
# open | answered | parked
status: open
# Records this question is about, e.g. [PZ-003]
about: [PZ-008, PZ-013]
# Leave empty while open
answer:
# Any related record IDs, e.g. [PZ-002, Q-004]
links: []
# Set to an ID when this record is replaced. It then moves to the Parked tab.
superseded_by:
tags: [old-DG-07]
---

Status on the old page: **Open**

The digital ruler (`Digital/build_ruler_svg.py`) assumes a 30 cm triangular metric ruler with 1:20/1:25, 1:50/1:75 and 1:100/1:125 on its three faces; confirm against the physical ruler and change `FACES` if it differs. **Diagonal solved 1 Oct 2026:** the ruler turns to any angle about its 0 mark (drag the brass knob at its far end; Shift for 15° steps; [ and ] for 1°, with Shift 0.1°), and the toolbar shows its angle. Still open: the scales.

Before production · moved from the Design spec, 17 Sept 2026

### What has to be prototyped

Physical tests that no amount of design work can settle. Two of the four below were written before later decisions and are marked accordingly.

#### Test The final map mechanic

**Partly superseded (PZ-013):** the format is decided — four laminated wet-erase letter sheets, drawn on with a marker. Pinning and the transparent overlay are out; the stops cluster too tightly to pin (Rouen and Roumare sit 0.13 in apart on a letter sheet). **Still to test:** digit legibility at true print size. The family **9** is already flagged as the riskiest shape, and 18 cards makes the footprint question sharper.

#### Dropped Red filter print fidelity

**Dropped, 25 Sept 2026:** the red filter has no job in old page PC-18 (old page PR-03).

Print a test sheet and check that the noise wash genuinely hides the hidden layer at arm's length and genuinely reveals it under the filter.

#### Test Tafl solution uniqueness

**Done (PZ-008):** exhaustive search over the 11×11 layout confirms exactly one *three*-move escape, F6 → H6 → H11 → K11. The four-move wording here predates that decision. **Still to test:** that the hidden-strip offset reads through the real ticket stock.

#### Passed, 29 Sept 2026 Branch rune legibility

Carve or print at final size and confirm the tally strokes are countable with the magnifier and genuinely ambiguous without it.

Observation · moved from the Design spec, 17 Sept 2026

### Leif’s trail is already complete

**Observation worth recording.** All three existing postcards are stops on Leif's trail: postcard L1 is L'Anse aux Meadows, L2 is Battle Harbour, Labrador (Markland) and L3 is Baffin Island (Helluland) — postcard order now genuinely matches the `leif` route order used in the Travel routes tab (renumbered so this holds, after the trail itself was flipped so L'Anse aux Meadows comes first). The built cards therefore already form one complete trail, the one drawing the digit **1**. Useful if intentional: the postcards teach the mechanic on the simplest trail and the map extends it to the other three.

Not required · old page HI-05 dropped 26 Sept 2026 · moved from the Design spec, 17 Sept 2026

### Historical claims needing verification

**Dropped, 26 Sept 2026:** the user decided source-checking these isn't needed — it's a game. Kept below for reference; none of it blocks printing. ~~None of the following has been source-checked. Each is used somewhere in this page and must be confirmed, corrected or dropped before it reaches a prop.~~

- Younger Futhark group membership and ordering as given in the table, and the branch-rune convention of left = group, right = position.
- That no complete Viking-Age hnefatafl ruleset survives, and that the fullest surviving record is Linnaeus's 1732 account of Sami tablut.
- "Hrafn" as the Old Norse for raven, and its five-rune Younger Futhark spelling.
- Jötunvillur as a real and still contested Norse cipher.
- Viking-Age folding balances and cubo-octahedral weights in trade contexts.
- Combs as a common Viking find.
- Carved rune-message sticks (rúnakefli) from Bergen.
- Cistercian numerals as 13th-century monastic notation, if that option is taken up.
