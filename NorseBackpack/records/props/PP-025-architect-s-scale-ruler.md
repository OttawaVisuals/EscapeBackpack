---
id: PP-025
title: Architect's scale ruler
type: prop
# idea | candidate | decided | built | parked
status: decided
# physical | printed | digital
form: printed
# make | buy | print | 3d-print
source: print
# The play-test page shows the body's "## Player sees" section, or this prop's image asset.
# Where the player gets it: start (in the backpack) or the puzzle whose lock releases it, e.g. PZ-004
found_in: PZ-007
envelope: PZ-007
# Physical pocket/container or location; availability remains in found_in above.
container: Envelope 9
after_game: return
# Any related record IDs, e.g. [PZ-002, Q-004]
links: []
# Set to an ID when this record is replaced. It then moves to the Parked tab.
superseded_by:
tags: []
---

**15 Oct 2026 (designer, playtest feedback): ruler redesigned, not built.** A printed cardboard or heavy-paper card, about 150 × 30 mm (not set), with a scale printed along each long edge. Edges are picture rebuses, not "1:125": **LONGSHIP** (long + sheep, the correct edge for PZ-011) and **SPEAR** (pear + S, a decoy), on one face for now; a back face with more edges may be added later. The scales are free: marks are numbered in plain units (10, 20, 30…) with half-ticks, spaced so the PZ-011 distance lands exactly on a numbered mark on the LONGSHIP edge and between marks on the others. Print at 100% with a 50 mm check bar on the print sheet; print a clear 0 line so the cut edge need not be accurate. The words LONGSHIP and SPEAR are also on Liv's notes card (PP-048). Digital ruler (Q-044, `Digital/assets/Ruler_Face_*.svg`) not yet updated. Replaces the 14 Oct note below, which is kept as history.

**Mock-up built 15 Oct 2026** (`Props/LivRuler/build_ruler_pdf.py`; print PDF `NorseBackpack/Print/_pdf_source/Liv_Ruler_Print.pdf`, Letter page with corner marks and a 50 mm print-check bar; preview `Props/LivRuler/Liv_Ruler_Preview.png`). Card 160 × 36 mm, one face, "LIV'S RULER" between the two edges. Whole ticks only (no minor ticks), numbers every 10 units, a heavier 0 line 8 mm in from the left end. **LONGSHIP (top)**: 8.31 mm per 10 units, marks 0 to 130, so the 100 mark is 83.126 mm from 0, the Châlus to Saint-Clair dot distance. **SPEAR (bottom)**: 11.08 mm per 10 units, marks 0 to 100, the same distance reads 75, 5.5 mm from both the 70 and 80 marks. The rebus pictures (long arrow + sheep, pear + S) are rough vector placeholders, not final art. **Codex icons, 15 Oct 2026:** `Rebus_Pear_Bayeux_Pencil_Draft_v1.png` and `Rebus_S_Bayeux_Pencil_Draft_v1.png` (in `Postcards/RebusIcons/`) are in the ruler as the SPEAR edge, trimmed by `Props/LivRuler/prepare_icons.py` into `Props/LivRuler/Icons/`. `Rebus_Sheep_Bayeux_Pencil_Draft_v1.png` is also in the ruler. **Still missing: the "long" drawing.** Codex's batch of 15 Oct has misnamed files: `Rebus_Cross_...` shows a teacup, `Rebus_Bow_...` a cross, `Rebus_Lightning_...` a bow, and `Rebus_Long_...` a lightning bolt (the Bayeux cross + bow + lightning set shifted by one). The LONGSHIP edge uses my placeholder arrow until a real "long" drawing arrives. The Codex prompts are not recorded here yet. **Restyle, 15 Oct 2026 (designer):** forest green background (`#1E4A38`) with cream ticks and numbers, the game's raven crest (`Art/FinalPuzzle/Family_Symbol_Raven_Crest_v1.png`) in the middle band instead of "LIV'S RULER", and the rebus pictures tucked into the right-hand corners (7.5 mm tall) so the scales can run longer (LONGSHIP to 140, SPEAR to 110). Card now 160 × 40 mm. **Real "long" drawing arrived, 15 Oct 2026:** Codex renamed its files and re-made the long one: `Postcards/RebusIcons/Rebus_Long_Marker_Pencil.png` is now a double-headed arrow with end bars. `prepare_icons.py` uses the new names (`Rebus_Pear_Pencil`, `Rebus_Letter_S_Pencil`, `Rebus_Sheep_Pencil`, `Rebus_Long_Marker_Pencil`), recolours the arrow cream (it is dark line art with no fill, so it vanished on the green) and thickens it to about 0.4 mm. **Later the same day** Codex re-made the long arrow with a light fill and a dark pencil outline, matching the other icons, so the cream recolour and thickening were dropped (`TINT_CREAM` is empty in `prepare_icons.py`) and the file is used as delivered. All four rebus pictures on the ruler are now Codex art; the Codex prompts are still not recorded here.

**Fixes, 15 Oct 2026 (designer):** the SPEAR edge is now printed turned 180°, so when the ruler is flipped to use it the numbers and pictures are upright and its 0 is on the left (its 0 sits at the right-hand end in the card's normal orientation). The two pictures are in reading order S then pear (S + pear = SPEAR); before they were pear then S. **Raven contrast addressed, 15 Oct 2026:** a light ivory one-colour version is saved as `Props/LivRuler/Family_Symbol_Raven_Crest_Light_v1.png` and used by `prepare_icons.py`; the PDF preview has been rebuilt. The generated art keeps the full crest, including its small longship. **Not done:** the 83.126 mm is calculated from the map code (`pt()` on Rollo's sheet), not measured on a printed sheet; no paper print test; PZ-011's code (now 100 on this ruler) and the lock are not re-set yet, and R5 still carries the old SCALE 1:125 rebus.

**Longship removed from the raven, 15 Oct 2026 (designer):** Codex redrew `Props/LivRuler/Family_Symbol_Raven_Crest_Light_v1.png` (overwritten in place, not saved as v2) without the small longship, which might have hinted at the LONGSHIP edge. It also dropped the compass wheel, which the brief had asked to keep; the result is a single raven in a knotwork ring and reads well on the green. The exact prompt for this edit was not passed to me; the prompt below is for the earlier version that still had the ship.

Exact generation prompt for the earlier light raven art (with the ship): “Edit this family raven crest into a single-colour light ivory version for use as a small central icon on a dark forest-green printed ruler. Preserve the overall crest composition and recognizable raven, circular knotwork frame, compass rose, and small longship. Recolour every visible element to one consistent warm ivory/cream (#EFE3C4), including the outlines and fine details; remove all dark green, black, orange, and other colours. Keep the background fully transparent. Maintain the established detailed engraved/embroidered Norse illustration style, with dark-green transparency between the ivory strokes so the green card shows through. Simplify only tiny textures that would merge at 12 mm print size; keep the raven silhouette and eye clear. No new elements, no text, no shadow, no glow, no backing disc.”

**Edit, 15 Oct 2026 (designer):** removed the small longship, sail, dragon prows and waves from the lower-left interior. The knotwork ring now continues behind that area, with transparent open space inside. The raven, compass wheel and single ivory colour are retained. Updated asset and ruler preview.

Exact edit prompt: “Edit this light ivory raven crest. Remove only the small longship in the lower-left interior, including its sail, dragon prows, and waves. Continue the existing circular knotwork frame naturally behind the removed ship and leave the remaining inner area open and transparent so the composition stays balanced. Preserve everything else exactly: the raven, compass wheel, outer knotwork ring, single warm ivory colour (#EFE3C4), fully transparent background, engraved line style, and line weight. Do not alter or simplify any other part. No new elements, text, shadow, glow, or backing disc.”

**14 Oct 2026 (designer):** the ruler becomes a **printed cardboard ruler**, shorter than 30 cm, so it fits an envelope and the box (Q-049, Q-052). It keeps the 1:25 and 1:125 scales. Length not set. The only distance measured with it, Châlus to Saint-Clair-sur-Epte on Rollo's map (PZ-011), is about 84 mm between the two icon centres in `TravelMap/build_trail_maps_pdf.py` (10.5 m at 1:125; the code 104 means about 83 mm dot to dot). Calculated from the file, not measured on a print. A 15 cm ruler would cover it and fit a postcard-size envelope (suggestion, not decided).

**11 Oct 2026 (PR-007):** the backpack is now a box, and pockets and pouches are envelopes. Where this record mentions the bag, a pocket, a pouch or a lock, that is the earlier format; the `container` field gives the envelope.

Architect's scale ruler carrying both 1:25 and 1:125. Loose in the main compartment from lock 1; first needed by the rebus distance. Whether it is bought or made is not recorded.

## Starting state

Not recorded yet.

## Reset

Not recorded yet.

## Replacement

Not recorded yet.

**15 Oct 2026 (Codex):** revised the light crest at the designer's request to remove the compass wheel as well as the previously removed longship. The raven and knotwork border remain; the cleared area is transparent. Prompt: “Edit this exact image. Remove only the compass wheel behind the raven, including all its spokes, outer circle, center, and decorative tips. Fill the cleared space with fully transparent background, keeping the composition balanced and open. Preserve the raven and the entire surrounding interlaced knotwork border exactly as they are. Keep the same engraved pencil-drawn linework, line weight, warm ivory (#EFE3C4) only, and fully transparent background. No wheel, no ship, no added elements, no text, no shadow, no glow, and no backing disc.”

**16 Oct 2026 (designer):** the ruler moves from envelope 4 to **envelope 9** (with R3, R4, R5), since it is only used for PZ-011. It was recorded in envelope 4 by mistake of order, not by design. Opened by 1486 (PZ-007).

**20 Oct 2026 (designer): production size decided** — ruler → bookmark 2 × 6 in (card is 160 × 40 mm now; scales need about 125 mm; not rebuilt). See Q-052.

**20 Oct 2026 (Claude, designer's request): rebuilt as a 2 × 6 in bookmark (152.4 × 50.8 mm), one side.** Scales unchanged: LONGSHIP 6.927 mm per 10 units with the Châlus to Saint-Clair distance on the **120** mark (measured in the PDF: 83.126 mm from the 0 line), SPEAR 11.08 mm per 10 units (the same distance reads 75, 5.5 mm from 70 and 80), ranges still LONGSHIP 0–150 and SPEAR 0–110, 0 line 8 mm in, SPEAR edge turned 180°. Changes: the rebus pictures are right-aligned inside the 0.125 in safe zone (LONGSHIP pictures 119.8–148.9 mm, SPEAR 136.0–148.9 mm, each clear of the last number); the extra height gives larger numbers (Cinzel Bold 7.4 pt, were 6.4), longer ticks (5 mm, 0 line 7 mm) and a larger raven crest (19 mm); green background with 0.125 in bleed, ticks run 1.5 mm into it so a slightly-off cut never leaves a gap. No content added or removed.
- Files: home-print sheet `Print/_pdf_source/Liv_Ruler_Print.pdf` and `Print/Print_LivRuler.docx` (Letter, corner marks beyond the bleed, 50 mm check bar); **new print-shop file `Print/_pdf_source/Liv_Ruler_2x6_PrintShop.pdf`** (6.25 × 2.25 in: trim + bleed, no marks); preview `Props/LivRuler/Liv_Ruler_Preview.png`.
- The 160 × 40 mm version (preview, PDF, Word sheet, builder) is archived at `Norse_Archive/NorseBackpack/Props/LivRuler/Before_Bookmark_20261020/`.
- Not done: paper test (print at 100 %, check the 50 mm bar, then lay the ruler on Rollo's map); digital ruler (Q-044) unchanged.

**20 Oct 2026 (designer):** production maps become 5.5 × 8.5 in, so the ruler needs a production version scaled to the new Rollo map (Q-049). The current 2 × 6 ruler stays for the prototype.

## 20 Oct 2026: Ruler matched to the half-Letter map proof (Codex)
Separate production-design proof built with the other map proofs. Rollo's new Châlus–Saint-Clair-sur-Epte dot distance measures 71.3284 mm in the final PDF; the ruler PDF's 0 to 120 LONGSHIP ticks measure 71.3285 mm. SPEAR still reads 75. Trim stays 2 × 6 in, with 0.125 in bleed; numbers and rebus artwork retained. Files under C:/EscapeBackpack/output/other-maps-half-letter/: Ruler_For_HalfLetter_Maps_PrintShop_Proof.pdf and Ruler_For_HalfLetter_Maps_Letter_Test.pdf. Builder TravelMap/build_other_half_letter_proofs.py imports the existing ruler builder and changes distances/output paths in memory only. Existing prototype ruler and Word master unchanged. Use this ruler with the resized proof map only. PDF measurements and visual layout checked; physical printing and player test outstanding.
