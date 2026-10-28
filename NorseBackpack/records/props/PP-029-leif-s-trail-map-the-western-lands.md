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
envelope: PZ-009
# Physical pocket/container or location; availability remains in found_in above.
container: Envelope 6
after_game: return
reset_name: Map: The Western Lands
# Any related record IDs, e.g. [PZ-002, Q-004]
links: []
# Set to an ID when this record is replaced. It then moves to the Parked tab.
superseded_by:
tags: [old-PR-13]
---

Leif's laminated North Atlantic sea chart with seven animal vignettes. Print file: `Web/pdf/Trail_Map_1_Leif_Print.pdf`.

**14 Oct 2026 (designer, Q-052):** maps are **plain paper, not laminated**. They travel flat in 9 × 12 in envelopes (PR-007). Older mentions of lamination describe the earlier format.

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

**17 Oct 2026 (designer, Leif cleanup draft):** requested darker animals, clearer Labrador/Newfoundland labels, and the same larger transparent title-band symbol as Rollo/Aud. Separate player/answer PDFs in `NorseBackpack/Print/_pdf_source/Leif_Cleanup_Draft/`; live PDFs unchanged. Builder: `TravelMap/Drafts/build_leif_cleanup.py`. Seven animals increased from 0.62 to 0.82 opacity; animal artwork and boxes unchanged (wolf remains A6). Makkovik, Rigolet and Cartwright labels east of dots; Corner Brook/Gander labels raised above their dots. Blue longship cutout generated with built-in image_gen; asset and exact prompt at `TravelMap/Drafts/Leif_Longship_Transparent_v1.png` and `_prompt.txt`. Checks: 18 place labels retained, no collision drops; text-content and geometry assertions; rendered player/answer inspection (Rigolet revised after first render overlapped Labrador caption). Physical print/player test remains outstanding.

**17 Oct 2026 (designer): cleanup draft adopted into the live print and answer PDFs** (`TravelMap/Drafts/build_leif_cleanup.py`; old copies in `C:\EscapeBackpack\Norse_Snapshots\Norse_2026-10-17_PreReadability\`; `build_trail_maps_pdf.py` carries a note that running it would overwrite them). Page images and web copies rebuilt. Not paper-tested. Darker animals, adjusted town labels, larger transparent longship on the title band.

**20 Oct 2026 (designer): production maps become half-letter, 5.5 × 8.5 in** (14 pt card flyers), carried in **6 × 9 in clasp envelopes**. The bottom title strip is removed and the trail icon (stamp) moves onto the map itself, so the map can use more of the card. **The prototype keeps the current Letter prints**; production files are separate. Codex will redo Aud's map at the new size. Consequences: the ruler (PP-025) must be rebuilt to the production Rollo map's scale; Harald's back (board note) fits at its current size, so the Oslo-ticket grid can stay. Supersedes the 8 × 10 idea above. See Q-049.


## 20 Oct 2026: Matching half-Letter professional-print proof (Codex)
Leif proof now matches the Aud half-Letter direction: 5.5 × 8.5 in trim, 0.125 in bleed, bottom title removed, longship identifier in the upper-right panel, 7.2 pt town names and 6.8 pt grid references. All 18 town names and 11 map-art placements retained; animal artwork centers remain in their original grid squares. Separate review files only; Letter prototype and answer master unchanged.
Builder: TravelMap/build_other_half_letter_proofs.py. Files and review PNGs: C:/EscapeBackpack/output/other-maps-half-letter/. All_Maps_5.5x8.5_Print_Test_Pack.pdf includes all four fronts, Harald reverse and the matching ruler. Print the combined review pack single-sided at 100% / Actual size; separate Harald Letter test can be printed duplex, long edge. Native PDFs, safe area, source hashes and visual details checked. Design proof only; physical readability/player test outstanding.
