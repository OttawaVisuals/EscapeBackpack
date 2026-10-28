---
id: PP-030
title: Aud's trail map (The Island Settlement)
type: prop
# idea | candidate | decided | built | parked
status: decided
# physical | printed | digital
form: printed
# make | buy | print | 3d-print
source: print
# The play-test page shows the body's "## Player sees" section, or this prop's image asset.
# Where the player gets it: start (in the backpack) or the puzzle whose lock releases it, e.g. PZ-004
found_in: PZ-004
envelope: PZ-004
# Physical pocket/container or location; availability remains in found_in above.
container: Envelope 4
after_game: return
reset_name: Map: The Island Settlement
# Any related record IDs, e.g. [PZ-002, Q-004]
links: []
# Set to an ID when this record is replaced. It then moves to the Parked tab.
superseded_by:
tags: []
---

Aud's laminated journey map: a single portrait sheet, symbols not to scale. See the treasure route and coin tally puzzles. Print file: `Web/pdf/Trail_Map_3_Aud_Print.pdf`.

**14 Oct 2026 (designer, Q-052):** maps are **plain paper, not laminated**. They travel flat in 9 × 12 in envelopes (PR-007). Older mentions of lamination describe the earlier format.

## Icon concepts — 16 Oct 2026

Designer approved generating a comparison sheet while keeping the counting mechanic. Generated `Art/MapIcons/Aud_Icon_Concepts_v1.png`: bridge, ford, gate, well, chapel and ruin in purple and ivory. Concept only; no map symbols replaced. Small previews are not calibrated print-size proofs. Print legibility and route alignment remain untested.

Exact ImageGen prompt:

```text
Use case: stylized-concept
Asset type: icon concept comparison sheet for the printed Norse backpack treasure map.
Primary request: Create ONE cohesive sheet showing six NEW illustrated map symbols, in a clean 3-column by 2-row layout. Top row BRIDGE, FORD, GATE. Bottom row WELL, CHAPEL, RUIN. Each cell contains one large icon and the same icon repeated much smaller below it to assess small-size clarity, then its label. Large and small symbols must match.
Style: simple confident hand-drawn cartographic silhouettes, restrained vintage Nordic field-guide illustration. Flat muted dark purple #614773 outlines and pale warm ivory #F4EEDD interiors on a plain warm ivory sheet. Strong clean contours, very few interior marks, no shading, texture, gradients, decorative frames, elaborate engraving, perspective scenes or photorealism. Consistent slight elevated three-quarter viewpoint for landmarks. Counting icons bridge/ford/gate slightly bolder. All symbols must remain recognisable at roughly 5–7 mm print size; the displayed sheet is a concept proof, not a calibrated print master.
Subjects:
BRIDGE: short timber bridge, two clear side parapets, just four broad cross-planks. A short faint teal water line passes underneath across the deck direction; no roof.
FORD: no bridge or structure. A short row of five broad irregular stepping stones crosses a short faint teal strip of water. Very distinct silhouette from bridge.
GATE: two sturdy posts with one simple timber gate visibly swung open; two very short barrier stubs establish a clear opening. One diagonal brace, no tiny pickets.
WELL: low round stone rim, two posts supporting a small pitched roof, unmistakable well opening. No tiny stonework.
CHAPEL: intact compact simple building with pitched roof, dark doorway and small prominent cross above its roof. No grand church or elaborate tower.
RUIN: broken low masonry walls with irregular tops and one partial doorway, visibly roofless. No cross, no intact building outline. Distinct from chapel.
Text: only the six uppercase labels BRIDGE, FORD, GATE, WELL, CHAPEL, RUIN in small clear dark typography.
Composition: generous equal spacing, no touching or overlapping cells, plain background, no extra map or decorative objects. Aim for practical readable game map icons, not logo badges.
```

## Additional perspective icons — 16 Oct 2026

V10 addresses seven designer PDF comments: new native-pose bridge views keep posts upright at annotated near-vertical/positive-slope crossings; shallow-wall gates use a new upright open-gate view. No whole-image rotation at those sites. All five fords enlarged to 18pt, with road/path ink clipped underneath so water remains visible. Source JSON/marker assignments retained. Renderer `render_crossings_v10.py`; method and exact prompts `CROSSINGS_V10_NOTES.md`; revised map and seven-region before/after review under `render_full_map_v10/`. Physical proof/route solution still outstanding.

V9 full-layout proof from designer's new 102-feature JSON, preserved as `TravelMap/Drafts/aud_features_full_2026-10-16.json`. Marker mapping: `coin1` camel; `Coincorretc` exact ticket Fehu rune; `Coin2` ticket fleur-de-lis. Symbols at source positions; labels/correctness not printed. All approved terrain/landmark styling applied, standalone well/ford/wall assets added. Renderer `render_full_map_v9.py`; PDF/PNG and validation in `render_full_map_v9/`; method/prompts in `FULL_MAP_V9_NOTES.md`. Shore attachment and small edge-artwork fits remain renderer overrides. Live files unchanged. Full route/ticket counting NOT revalidated; earlier 521 is not assumed for this layout.

V8 dry-ditch treatment approved: rough earth banks, shaded recessed bed and sparse grass replace technical ticks. Existing path and bridge retained; detail reduced near crossing; matching legend. Isolated `render_ditch_v8.py`; method in `DITCH_V8_NOTES.md`; outputs `render_baseline/Aud_Ditch_Draft_v8.pdf` and `Aud_Ditch_Detail_v8.pdf` plus PNGs. Other v7 styling retained. Draft/live hashes unchanged; print test outstanding.

V7: designer approved landing size and requested matching chapel, ruin, village, cave, mill and farm. All six now use the landing's actual visible width (about 25.69pt), preserving aspect ratios and positions. Isolated `render_landmarks_v7.py`; output `render_baseline/Aud_Landmarks_Draft_v7.pdf` / `landmarks-map-v7.png`; method in `LANDMARKS_V7_NOTES.md`. Bounds checked, label reservations enlarged, draft/live source hashes unchanged. Other v6 styling retained; no paper test.

V6 landing update requested: larger artwork, boat on water. New `Aud_Landing_Shore_v6.png`; exact prompt and placement method in `TravelMap/Drafts/LANDING_V6_NOTES.md`. Isolated `render_landing_v6.py` attaches jetty at existing coastline vertex (220.38,752.98), southwest of the inland JSON port, with boat on sea side; JSON unchanged. Artwork targets 26pt width, fitted below frame. Bay caption moved into clear water in scratch config; matching legend. Outputs `render_baseline/Aud_Landing_Draft_v6.pdf` and `Aud_Landing_Detail_v6.pdf` plus PNGs. Six hull samples checked on sea and rendered proof inspected. This draft override is not an approved live route change; physical test outstanding.

V5 field-only update requested: light wheat tone, curved paired furrows, illustrated dry grass along the boundary, farmhouse clearance. V4 hedge/gate and other artwork retained. Source `TravelMap/Drafts/render_field_v5.py`; method and exact grass-asset prompt in `TravelMap/Drafts/FIELD_V5_NOTES.md`. Outputs `render_baseline/Aud_Field_Draft_v5.pdf` and `Aud_Field_Detail_v5.pdf` plus PNGs. Geometry/live files unchanged; print test outstanding.

V4 hedge/gate-only refinement requested: connected tangent-aligned leafy hedge, clear passage, new open two-rail gate placed with no shear. Other v3 styling retained. Isolated source `TravelMap/Drafts/render_hedge_gate_v4.py`; exact ImageGen prompts and limits in `TravelMap/Drafts/HEDGE_GATE_V4_NOTES.md`. Outputs `render_baseline/Aud_Hedge_Gate_Draft_v4.pdf` and `Aud_Hedge_Gate_Detail_v4.pdf` plus PNGs. Gate anchor unchanged, artwork fitted below frame. Draft/live files unchanged; no paper test.

V3 designer correction: mix tree species, enrich river/terrain, put grid underneath artwork, correct distorted bridge, enlarge non-bridge icons 30%. Implemented in isolated `TravelMap/Drafts/render_terrain_v3.py`. New birch, conifer and river-bridge assets; exact prompts/method in `TravelMap/Drafts/TERRAIN_V3_NOTES.md`. Outputs `render_baseline/Aud_Style_Draft_v3.pdf` and `Aud_Style_Comparison_v3.pdf` plus PNGs. Icon dimensions 1.3x, bridge deck span unchanged; bridge placement now rigid rotation/uniform scale, no shear. Grid reordered in memory only. Draft/live source hashes unchanged; paper test outstanding.

Full-style v2 proof requested after the designer rejected mixed PNG landmarks and basic drawn substitutes. New individual ImageGen assets: chapel, ruin, two bridge views, gate, tree, hedge bush and marsh reeds. Exact prompts in `Art/MapIcons/FULL_STYLE_GENERATION.md`. `TravelMap/Drafts/render_full_style.py` uses illustrated assets for every landmark/crossing and for wood/hedge/marsh; road/water/field/ditch paths remain deterministic strokes tied to the JSON. Outputs beside the baseline: `Aud_Full_Style_Draft_v2.pdf`, `full-style-preview-v2.png`, `Aud_Full_Style_Comparison_v2.pdf`, `full-style-comparison-v2.png`. Draft and live source hashes checked unchanged; no live integration. Crossing illustrations use perspective placement transforms, not an altered crossing_angles algorithm. Physical print test outstanding.

Draft renderer style proof built against `TravelMap/Drafts/aud_features_draft_2026-10-16.json` (20 features), following its accompanying CODEX_BRIEF. Outputs: `TravelMap/Drafts/render_baseline/Aud_Style_Draft.pdf` and `style-preview.png`; source: `TravelMap/Drafts/render_style_test.py`. Geometry and live renderer unchanged. New PNG landmarks combined with procedural terrain and provisional perspective crossing/chapel/ruin drawings. Review limitations in `TravelMap/Drafts/STYLE_TEST_NOTES.md`; not approved for the live map or paper-tested.

Terrain proposal requested on the yellow map background: `Art/MapIcons/Aud_Terrain_Concepts_Yellow_v1.png` shows wall, river/stream, wood, hedge, field, marsh, moor, road/path. Stronger greens, teal and stone tones proposed for contrast. Exact prompt in `Art/MapIcons/GENERATION.md`. Concept only, map unchanged, print-size readability untested.

Landing variant with a moored boat generated at the designer's request: `Art/MapIcons/Aud_Landing_Boat_v2.png`. Original retained. Exact edit prompt in `Art/MapIcons/GENERATION.md`. Map unchanged; preview checked, soft halo persists and print-size readability untested.

Designer prefers perspective symbols, retaining the counting mechanic. Generate bridge/ford/gate orientations to fit the revised map as needed. Seven separate PNGs generated in `Art/MapIcons/`: landing, standing stone, village, cave, farm, mill and cairn (`Aud_<name>_v1.png`). Exact shared prompt and per-icon subjects are recorded in `Art/MapIcons/GENERATION.md`. No map changes. Generated previews visually inspected; soft edge halos remain and print-size legibility is untested.

## Starting state

Not recorded yet.

## Reset

Not recorded yet.

## Replacement

Not recorded yet.


## V11 water, forest layering and legend refinement - 16 Oct 2026

Designer requested four changes on v10. Isolated `TravelMap/Drafts/render_refinements_v11.py` renders river/stream banks together, then fills together, opening internal joins; nine coast/lake mouths use short flared colour transitions. Roads now precede wood canopy artwork, with countable crossings still drawn last. The standing stone at (430.82,189.82) is displayed 8pt left at (422.82,189.82), without altering JSON. Right-column legend landmark artwork is larger (horizontal scale 1.18 and vertical scale 1.0 instead of 0.62), with wider label clearance and row spacing.

Outputs: `TravelMap/Drafts/render_full_map_v11/Aud_Full_Map_v11.pdf` and `Aud_Changes_Review_v11.pdf`, with PNG previews and validation logs. All 102 source features, 12 bridges, 5 fords, 7 gates and three ticket markers retained; live sources and input JSON hash-checked unchanged. This is a visual draft; paper counting/print checks remain outstanding. No new AI-generated assets.

## V12 corrections after v11 review - 16 Oct 2026

Designer rejected v11 water fades. V12 uses the sea's existing solid fill (#DCE7E4) for rivers, streams and lakes, with solid open mouths and bank outlines; no gradients. Bridge/ford/gate legend symbols now use the same enlarged scale as the other point symbols. Gate (465.4,513.12) has a horizontal barrier; its adjacent wall is locally levelled to meet it. All stone walls use larger 17 x 7pt clusters at 8pt spacing, smooth tangent connections and gate gaps (previously 12 x 4.3pt at 5.5pt spacing). Only the marked southeastern wood polygon uses a denser 12pt tree grid (other woods retain 15pt); mixed species, landmark clearance and trees-over-roads layering remain.

Isolated renderer `TravelMap/Drafts/render_corrections_v12.py`; outputs under `render_full_map_v12/`: full map and five-region before/after review PDFs, PNGs, source hashes and style log. V11 retained. Source JSON/live renderer unchanged; 102 features and counting symbols retained. Paper hand-walk/print legibility remain untested.

V12 gate QA: the native Gate_Open_v4 asset has horizontal rails, so this one site uses it unrotated at 18 x 12pt, replacing the steep open leaf in the v10 perspective asset. Other crossing poses retained.

## V13 continuous walls, shoreline topology and larger legend - 16 Oct 2026

Designer rejected the wall fragment joins and gaps at v12 river mouths. `TravelMap/Drafts/render_continuous_v13.py` replaces stamped wall clusters with a continuous vector masonry surface: a shared cap ribbon and shaded front face, irregular stone joints, clean gate openings. The wall by the chapel is levelled across the road and meets a horizontal wooden gate with posts seated at its ends. This is the v13 proposed wall treatment; review at print size before live adoption.

Water geometry now uses joined channel buffers and the actual land polygon. Bank ink is clipped to dry ground; the resulting shared land/water boundary is traced at all nine coast/lake mouths. This removes both fades and missing shoreline sections. Solid water colour and the previous tree density/layering are retained.

Legend enlarged from 160.06 x 200.08pt to 199 x 248pt, with 6.5pt labels (was 5pt), 25 x 15pt point-symbol bounds and 5pt side padding. Wood, marsh and moor have plain illustrations without sample-background rectangles. Field/lake treatments remain. The sea caption is moved beside the legend at (249,176), rotated 90 degrees, to prevent overlap. Legend bounds reserved against town labels.

Outputs under `TravelMap/Drafts/render_full_map_v13/`: `Aud_Full_Map_v13.pdf`, `Aud_Changes_Review_v13.pdf`, PNGs and validation/style logs. The before/after sheet covers the coastline, wall/gate, and full legend including terrain symbols. All 102 features, 12 bridges, 5 fords, 7 gates and ticket-marker identities retained. Live sources and JSON hash-checked unchanged. Rendered review performed; paper hand-walk/print test remains outstanding. No new AI assets.

## V14 water border consistency and natural terrain scatter - 16 Oct 2026

Designer approved water connections but requested one border colour everywhere. All coast, river, stream and lake boundaries, including legend samples, now use existing coastline grey-green #59635D. V13 solid fills and joined-mouth geometry remain.

The two moor polygons and single marsh polygon now use deterministic irregular sampling with small clusters, open gaps and spacing checks instead of rows. Existing grass/reed artwork varies in size: grass 0.7-1.65x and reeds 0.7-1.4x their previous base sizes. Full symbol bounds stay inside each area; landmark clearance is retained. No new icons. Legend examples stay simple and plain.

Isolated source `TravelMap/Drafts/render_terrain_v14.py`; outputs `render_full_map_v14/Aud_Full_Map_v14.pdf`, `Aud_Changes_Review_v14.pdf`, PNG previews and validation/style logs. All 102 features, crossing counts and ticket marker identities retained; source JSON/live files hash-checked unchanged. Visual review performed; paper print/count checks remain outstanding.

## V15 uniform water outline weight and finishing - 16 Oct 2026

Designer identified that v14's river casing was still thinner than the coast despite matching colour. V15 removes casing-width differences: one vector boundary for land minus all channels/lakes, stroked once at 0.55pt in #59635D. Lake base fill has no separate outline; legend water samples match 0.55pt. The original coastline stroke is disabled in the isolated builder to prevent double outlines.

The small land remnant below the legend is removed locally (page box 90,100 to 114,113, clipped to map). The comb's cream stamp background is removed for this draft so the existing blue title band shows through. Original postcard stamp retained. Transparent comb asset and both exact built-in ImageGen edit prompts are recorded in `TravelMap/Drafts/FINISH_V15_NOTES.md`.

Isolated renderer `TravelMap/Drafts/render_finish_v15.py`; outputs under `render_full_map_v15/`: full map, three-region review PDFs/PNGs and validation/style JSON. All 102 source features, 12 bridges/5 fords/7 gates and three ticket markers retained; v14 terrain scatter, wall and legend retained. Live source/JSON hashes checked unchanged; visual render reviewed. Physical print/count test remains outstanding.

## V15 approved; smaller print and online delivery copies - 16 Oct 2026

Designer selected v15 as the winning visual map. Full-resolution master retained (33,918,855 bytes). `TravelMap/Drafts/optimize_aud_map_v15.py` produces delivery copies under `aud_map_optimized_v15/`: print 300dpi PDF 908,594 bytes (97.32% smaller); web 200dpi PDF 762,687 bytes (97.75% smaller); online display WebP 616,636 bytes at 2400 x 3106 pixels.

PDFs keep selectable text and all 751 vector paths. Only embedded image resolution is reduced to match the largest placement; colour/alpha are resampled together and compressed losslessly. Full-page/zoomed icon renders inspected; original master hash unchanged. The WebP is recommended for the game's map display and the PDF for downloads/printing. Physical print test remains outstanding. No live generator integration, website rewiring or publishing in this pass. Delivery README and compression_report.json record the repeatable method and exact sizes.

**17 Oct 2026 (designer):** the Aud map now prints in the v15 style (see PZ-006); the files are in `TravelMap/Drafts/aud_map_optimized_v15/` (print 300 dpi PDF, web 200 dpi PDF, a 2400 px WebP for the online game). The legend no longer has a Marker row; the three coin marks are icons that match Aud's ticket.

**17 Oct 2026 (designer, title-band cleanup):** requested the same treatment as Rollo: remove the cream stamp backing and perforated border, show blue through the pillar artwork, enlarge within the band. Separate player/answer drafts saved in `NorseBackpack/Print/_pdf_source/Aud_Stamp_Cleanup_Draft/`; live PDFs unchanged. Reproducible builder `TravelMap/Drafts/build_aud_stamp_cleanup.py` replaces only the title-band image in the approved current PDFs, preserving v15. Transparent asset and exact built-in image_gen prompt: `TravelMap/Drafts/Aud_Pillars_Transparent_v1.png` and `_prompt.txt`. Both pages rendered and inspected; all text preserved and map above the title band verified pixel-identical at 144 dpi. Physical print not tested.

**17 Oct 2026 (designer): Aud cleanup not adopted yet; the pillars title-band draft is rejected** (Aud's stamp, postcards and ticket use the comb). New draft with the comb on the title band: `NorseBackpack/Print/_pdf_source/Aud_Comb_Titleband_Draft/` (`TravelMap/Drafts/build_aud_stamp_cleanup.py`, art `Aud_Comb_Titleband_v1.png`, a crop of `Aud_Comb_Ink_v15_final.png`, the same transparent comb ink as the live stamp, so no new image generation). Live Aud v15 map unchanged; awaiting the designer's review.

**17 Oct 2026 (designer): comb title-band draft adopted** into the live Aud print and answer PDFs (map above the band and all text unchanged, v15 kept; old copies in `C:\EscapeBackpack\Norse_Snapshots\Norse_2026-10-17_PreReadability\`). Page images and web copies rebuilt. `build_trail_maps_pdf.py aud` still keeps the live file in place.

**17 Oct 2026 (folder cleanup):** the v1–v13 draft renders (`TravelMap/Drafts/render_baseline/`, `render_style*/`, `render_*_v4`–`v8/`, `render_full_map_v9`–`v13/`, `crossing_guides_v10/`), most of `render_full_map_v14/` and the two `old_style_2026-10-16` PDFs moved to `C:\EscapeBackpack\Norse_Archive\TravelMap\Drafts\` (outside the repository; see its README). Paths to those files earlier in this record now point there. The live v15 files did not move.

**20 Oct 2026 (designer): production maps become half-letter, 5.5 × 8.5 in** (14 pt card flyers), carried in **6 × 9 in clasp envelopes**. The bottom title strip is removed and the trail icon (stamp) moves onto the map itself, so the map can use more of the card. **The prototype keeps the current Letter prints**; production files are separate. Codex will redo Aud's map at the new size. Consequences: the ruler (PP-025) must be rebuilt to the production Rollo map's scale; Harald's back (board note) fits at its current size, so the Oslo-ticket grid can stay. Supersedes the 8 × 10 idea above. See Q-049.

## 20 Oct 2026: Half-Letter professional-print concept (Codex)
Separate review proof requested by the designer, not an adopted replacement. Supplied Newprint template has 5.5 × 8.5 in trim, 5.75 × 8.75 in media/bleed (0.125 in on every side), plus a 0.125 in internal safe zone. `TravelMap/build_aud_half_letter_proof.py` writes to `C:/EscapeBackpack/output/aud-half-letter/`: clean PrintShop proof with matching TrimBox/BleedBox, trimmed PDF/PNG, and Actual-size Letter test with one-inch bar.

Bottom title strip removed; matching comb moved into the legend header. Map positions reflowed into a taller schematic frame; original pictograms preserve aspect ratio and relative placement, with crossing orientation adapted to the frame. Town names reset to 7.2 pt, legend to 6.5 pt, grid to 6.8 pt. All 11 towns / 25 key entries retained; source JSON has 102 features, including 12 bridges, 5 fords, 7 gates. Original Letter map hash checked unchanged. Full-page and detail renders inspected. Paper legibility/countability and final route tracing remain untested; print `Aud_Map_5.5x8.5_Letter_Test.pdf` at 100% / Actual size before adoption. The prototype's Letter masters are unchanged.
