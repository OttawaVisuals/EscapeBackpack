---
id: Q-014
title: Re-render or reframe the three existing fronts at true size.
type: question
# open | answered | parked
status: answered
# Records this question is about, e.g. [PZ-003]
about: []
# Leave empty while open
answer: Done
# Any related record IDs, e.g. [PZ-002, Q-004]
links: []
# Set to an ID when this record is replaced. It then moves to the Parked tab.
superseded_by:
tags: [old-PC-11]
---

Status on the old page: **Done**

**Artwork complete:** all three illustration sources and generated fronts are exactly 1500 × 1050. The guarded front builder and card L1 PDF builder both pass. The deterministic exact-ratio reframe removes the former 5% print stretch without inventing scenery; cards L2/L3 use the same symmetric horizontal crop and the refreshed seam proof reads `1576`.
**Remaining production step:** change `SIZE` and `PAGE` together in `build_postcard_collection.py`, then rebuild and inspect cards L2/L3 and the full collection PDF. **Done, checked 25 Sept 2026:** `build_postcard_collection.py` now uses SIZE 1500 × 1050 and a 5 × 3.5 in PAGE, and the collection PDF holds all 22 cards.
