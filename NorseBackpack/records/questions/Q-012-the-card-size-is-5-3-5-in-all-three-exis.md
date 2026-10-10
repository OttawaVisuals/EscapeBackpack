---
id: Q-012
title: The card size is 5 × 3.5 in. All three existing front illustrations now match it; the 02/0
type: question
# open | answered | parked
status: answered
# Records this question is about, e.g. [PZ-003]
about: []
# Leave empty while open
answer: Decided · 5 × 3.5 in
# Any related record IDs, e.g. [PZ-002, Q-004]
links: []
# Set to an ID when this record is replaced. It then moves to the Parked tab.
superseded_by:
tags: [old-PC-13]
---

Status on the old page: **Decided · 5 × 3.5 in**

**Decided:5 × 3.5 in** (360 × 252 pt, 10:7) is the standard for all eighteen cards.
**Front artwork done:** cards L1–L3 were reframed from 1536 × 1024 to exactly 1500 × 1050 by taking the same exact-ratio crop (38 px from each side, 2 px from the bottom, preserving the top row) and applying one uniform scale. Nothing was stretched. Cards L2 and L3 received the identical centred horizontal crop, so their mirrored cloud-fleck positions stayed in register.
**Join re-proofed:** the rebuilt 4× seam proof still reads `1576`; `build_topedge_test_sheet.py` now uses 300 dpi and a true 5 in strip, and its PDF was regenerated.
**Still to do:** `build_postcard_collection.py` remains at 1536 × 1024 on a 6 × 4 in page, so cards L2 and L3 are not fully converted until its `SIZE` and `PAGE` change together and the collection outputs are rebuilt.
**Superseded:** the earlier state had all three fronts at 3:2 and the join proof at 256 dpi. The choice between resizing 02/03 and enlarging card L1 was resolved in favour of the 5 × 3.5 in standard.
