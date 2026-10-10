---
id: Q-018
title: Six of Harald's fronts (H2–H6, HD) didn't match the series' title-band layout — the title 
type: question
# open | answered | parked
status: answered
# Records this question is about, e.g. [PZ-003]
about: []
# Leave empty while open
answer: Fixed
# Any related record IDs, e.g. [PZ-002, Q-004]
links: []
# Set to an ID when this record is replaced. It then moves to the Parked tab.
superseded_by:
tags: [old-PC-19]
---

Status on the old page: **Fixed**

**Found while syncing this session's new artwork into the page.** Every other built front (`L1`–`LD`, `R1`–`RD`, `A1`–`AD`, and Harald's own `H1` Oslo) reserves the lower ~20% of the card as a completely blank deep-navy panel, with the place name and country drawn into that empty panel afterward — that's the standard Q-012 fixes for all eighteen cards. `H2`–`H6` and `HD` were generated full-bleed with the title and subtitle baked directly onto the illustration itself; their own generation prompts said *"the title band will be added separately,"* but that compositing step never ran.
**Fixed, same session:** `build_postcard_front_images.py` now paints the missing band itself for exactly these six (a new `NEEDS_BAND` set, checked by output filename) — a solid deep-navy rectangle over the lower 20%, plus the thin warm-cream divider line sampled from the already-correct cards' own bands, then the existing title/subtitle drawing code runs on top exactly as it does for the other sixteen. Rebuilt from each card's own clean `Illustration_v1.png` (which never had a baked title), not by patching over the broken `_Front.png`, so there's no leftover double-text artifact. The sixteen already-correct fronts were not touched — confirmed by hash before/after.
**Title layout standardized, 26 Sept 2026 (Codex visual review, item 3):** all 22 fronts now use one 84 px Cinzel ExtraBold title size, a shared baseline at y=962 and a 23 px subtitle baseline at y=1012 on the 1500 × 1050 artwork. Tracking is 4 px and horizontal centring uses the actual ink bounds. Accented glyphs share the same baseline instead of being individually top-aligned. This clears the divider on Bjarnarhöfn and Walcheren and makes placement consistent across the deck. Existing illustration sources, band textures, place names, card size and postcard backs are preserved. This supersedes the earlier title positioning; the six-card band repair above remains in use. Source: `Postcards/build_postcard_front_images.py`. Front PNGs, individual and Letter PDFs, existing four-up sheets, full-deck preview and the eleven preferred Word print pairs are refreshed together. Print-size proof remains a physical check.

PZ

### Puzzles and clues
