# Aud draft style proof — 16 Oct 2026

## Outputs
- `render_baseline/Aud_Style_Draft.pdf`: one-page letter-size proof.
- `render_baseline/style-preview.png`: rendered preview, beside the unchanged `baseline.png`.
- `render_style_test.py`: isolated renderer; run with Python from any working directory. Uses the existing map builder and source PNG assets. It writes the intermediate PDF under `render_style/`.

## Method and checks
The 20-feature draft JSON is loaded explicitly. Feature coordinates, paths, smoothing flags and width classes are unchanged. Existing crossing_angles is reused without modification. Crossings draw last; the layer is clipped to the map frame and remains under normal stop dots and labels. Legend entries are selected from the draft's present kinds and use the proof's own drawing routines.

Draft and live renderer hashes were checked before/after generation; both unchanged. Final PDF rendered and the entire page visually inspected. Poppler emitted Symbol/ArialUnicode fallback warnings, but labels were readable. No physical print test.

The live builder's automatically added cache/decoy marks are suppressed for this scratch proof because they are not in the supplied JSON. The base coastline, towns, compass and journey stamp still come from the existing builder.

## What needs refinement
- This is a first renderer translation of the approved concept style, not a pixel-identical transfer. Trees, marsh, hedge and crossings use scalable drawn primitives; the landing, village, farm, mill and cave use the generated PNGs. Chapel and ruin are simplified perspective drawings because separate PNGs are not available.
- Landmark size classes are preserved. At these small sizes, fine PNG detail becomes faint; test at 100% on paper before choosing larger symbols.
- The uppermost landmarks have little clearance to the map frame; positions were not moved.
- Texture density is restrained to keep yellow visible. Wood/marsh extents are conveyed by texture rather than filled survey polygons. Some grid lines pass across small trees because the existing builder draws the grid after the feature layer.
- Perspective bridges/gate are provisional renderer approximations; their direction follows existing crossing_angles. Final custom orientations remain a separate design pass.
- The draft contains no stone wall, ford, moor or footpath, so those styles cannot be assessed here.
- No additional texture tile was required for this first proof. Separate transparent chapel/ruin and orientation-specific crossing PNGs would be needed for a fully image-based treatment.

