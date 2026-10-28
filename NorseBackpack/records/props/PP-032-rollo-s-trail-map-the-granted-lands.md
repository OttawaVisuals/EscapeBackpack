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
envelope: PZ-010
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

**14 Oct 2026 (designer, Q-052):** maps are **plain paper, not laminated**. They travel flat in 9 × 12 in envelopes (PR-007). Older mentions of lamination describe the earlier format.


**11 Oct 2026 (playtest 1 feedback, built same day):** **Walcheren added to the sheet.** Players looked for the RD decoy and it was not there: `stops.js` files it as an “Island anchor”, which `load_corpus()` skips. New `decoy_towns` entry in the Rollo config (51.53, 3.55, the `stops.js` coordinate), placed right after the stops so a collision cannot drop it; a dropped decoy label is now reported like a dropped stop. No other label was lost (31 labels). Wider map rework is Q-053.

## Starting state

Not recorded yet.

## Reset

Not recorded yet.

## Replacement

Not recorded yet.

**16 Oct 2026 (designer, Q-060):** base-map pass on Rollo's sheet: Portsmouth and Saint-Malo dropped (both plot in the sea; Portsmouth 19 pt from Winchester), Walcheren kept (decoy card RD), the six icon towns kept (leader lines), bolder dots and names (`bold_towns`), and “Roumare forest” given a fixed label spot below Rouen (the bigger labels left no free one). Icons and grid unchanged. PDFs and web copies rebuilt. The map lies flat, so envelope 8 needs the large envelope (Q-049).


**17 Oct 2026 (Codex, designer requested cleanup version):** separate review draft at `NorseBackpack/Print/_pdf_source/Rollo_Cleanup_Draft/Trail_Map_2_Rollo_Print.pdf`, with a matching answer PDF. Builder: `TravelMap/Drafts/build_rollo_cleanup.py`. Existing artwork increased from 0.62 to 0.96 opacity; Rouen label moved east; Roumare forest label moved southwest with a fine solid leader; Normandy caption moved below the town names. All town dots, art boxes, grid cells, page size and projection preserved. Both PDFs rendered and visually checked; all 29 place labels retained, no dropped labels reported. Live print/web PDFs and their builder unchanged. Physical print and ruler test still needed; draft not adopted.

**17 Oct 2026 (designer, draft title band):** requested the same blue background behind the journey symbol and a larger fit. Draft now uses `TravelMap/Drafts/Rollo_Comet_Transparent_v1.png` (built-in image_gen background-removal edit; exact prompt in sibling `_prompt.txt`), placed directly on the existing blue title band, 40.64 pt high with 6 pt right inset. Player/answer drafts and previews rebuilt and visually checked; no adoption into live PDFs. Shared builder now supports optional stamp path/height/inset settings; all default values retain the previous layout.

**17 Oct 2026 (designer): cleanup draft adopted into the live print and answer PDFs** (`TravelMap/Drafts/build_rollo_cleanup.py`; old copies in `C:\EscapeBackpack\Norse_Snapshots\Norse_2026-10-17_PreReadability\`; `build_trail_maps_pdf.py` carries a note that running it would overwrite them). Page images and web copies rebuilt. Not paper-tested. Cleaner icons and labels, larger comet on the title band.

**20 Oct 2026 (designer): production maps become half-letter, 5.5 × 8.5 in** (14 pt card flyers), carried in **6 × 9 in clasp envelopes**. The bottom title strip is removed and the trail icon (stamp) moves onto the map itself, so the map can use more of the card. **The prototype keeps the current Letter prints**; production files are separate. Codex will redo Aud's map at the new size. Consequences: the ruler (PP-025) must be rebuilt to the production Rollo map's scale; Harald's back (board note) fits at its current size, so the Oslo-ticket grid can stay. Supersedes the 8 × 10 idea above. See Q-049.


## 20 Oct 2026: Matching half-Letter professional-print proof (Codex)
Rollo proof now matches the Aud half-Letter direction: 5.5 × 8.5 in trim, 0.125 in bleed, bottom title removed, comet identifier in the upper-right panel, 7.2 pt town names and 6.8 pt grid references. All 29 town names and 13 pictograms retained. Independent PDF dot measurements give Châlus–Saint-Clair-sur-Epte about 71.329 mm, matched by the included production-proof ruler at LONGSHIP 120 (SPEAR 75). Use that ruler only with these resized maps. Letter prototype, its ruler and answer master unchanged.
Builder: TravelMap/build_other_half_letter_proofs.py. Files and review PNGs: C:/EscapeBackpack/output/other-maps-half-letter/. All_Maps_5.5x8.5_Print_Test_Pack.pdf includes all four fronts, Harald reverse and the matching ruler. Print the combined review pack single-sided at 100% / Actual size; separate Harald Letter test can be printed duplex, long edge. Native PDFs, safe area, source hashes and visual details checked. Design proof only; physical readability/player test outstanding.
