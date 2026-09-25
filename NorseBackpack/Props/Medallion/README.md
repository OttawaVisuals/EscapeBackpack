# Norse keepsake — one-piece medallion v2

**Print file: [Norse_Medallion_OnePiece_v2.stl](STL/Norse_Medallion_OnePiece_v2.stl).** One connected solid; no glue or assembly. Import at 100%, in millimetres.

## Size and orientation

- Diameter: 50 mm. Total thickness: 4.4 mm.
- Print as supplied: engraved lettering/compass **down**, detailed raven crest **up**.
- Body: 3.8 mm. Crest: 0.6 mm raised above it.
- Back text and compass: 0.4 mm recessed. Same filament as the body.
- All lettering stays inside the engraved border, with at least 1.21 mm clearance. The back is mirrored in the build coordinates so it reads correctly when the coin is turned over.

## Starting print setup

Recorded printer: Prusa i3 MK3S+, stock 0.4 mm nozzle.

Use 0.20 mm layer height **including the first layer**: 19 body layers, then 3 crest layers. Keep supports and raft off for this design. Use the printer profile and temperature appropriate to your actual filament; no material has been specified, so this package contains STL geometry rather than machine G-code.

**Optional second colour:** in PrusaSlicer, add a colour change immediately before the first crest layer, layer 20 / Z = 4.00 mm with the settings above. The body finishes at Z = 3.80 mm. Only the crest and its surrounding ornaments are above that height; the coin rim stays the body colour. A single-filament print needs no pause. Changing colours requires one manual filament swap during the same print job.

[Prusa's colour-change instructions](https://help.prusa3d.com/article/color-change_1687) explain the layer-slider action and M600 pause. The STL itself does not contain the pause or colours.

## Detail and limits

The crest is traced from a new detailed mask based on the selected right-hand raven/shield concept. It retains layered neck, wing and tail feathers, beak, eye, shield and four ornaments. Fine feather channels are widened by 0.16 mm; two tiny isolated fragments that cannot contain a 0.4 mm line are removed. This is a flat 0.6 mm relief translation of the concept, not a recreation of its metallic texture or sculpted shading.

The compass uses shallow outline engraving to keep underside bridge spans short. Physical printing is still needed to check underside letter counters, first-layer spread, bridging and the smallest feather tips. Do not scale this model down before checking those details.

## Files and rebuilding

- `Medallion_v2_Preview.png`: exact profile geometry shown from both sides; colours are illustrative.
- `Crest_Relief_v2.svg`, `Back_Engraving_v2.svg`: profiles at actual 50 mm canvas size; back SVG reads normally.
- `build_medallion_v2.py`: editable source. Run `python build_medallion_v2.py` to rebuild the STL, profiles, preview and geometry report. Requires numpy, Pillow, opencv, matplotlib and Shapely 2.1+. Font outlines use Windows Arial Bold.
- `Inspect_Mesh_v2.scad`: opens the exported STL in OpenSCAD; set `PART="back"` to turn it over.
- `sources/`: selected reference sheets and generated crest mask. The selected design is the right coin in each reference sheet.
- `crest_prompt.txt`: exact prompt used with the built-in ImageGen tool.
- `geometry_report_v2.json`, `mesh_check_v2.json`: measured dimensions/clearances and mesh checks.
- `Superseded_v1/`: rejected glue-together prototype retained only as history. Do not print those halves for the current design.

No physical print or printer-profile slicing has been completed for v2.
