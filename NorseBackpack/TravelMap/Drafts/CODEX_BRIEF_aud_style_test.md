# Codex brief: Aud map style test (16 Oct 2026)

Test run on a **draft** map. Nothing here is the live puzzle map.

## Input
- `TravelMap/Drafts/aud_features_draft_2026-10-16.json`: 20 features, page points, y up, 612 x 792. It only covers the top part of the sheet (y about 460 to 775).
- The style mock-ups the designer made (area fills and line textures: stone wall, river and stream, wood, hedge, field, marsh, moor, road and footpath), plus the new icons.
- `TravelMap/Drafts/render_baseline/baseline.png`: how the current renderer draws the same JSON (for before and after).

## Task
Extend the **renderer**, `TravelMap/aud_layer.py` (ReportLab), so the draft is drawn in the new style. Work on a copy or in `Drafts/`; do not overwrite `aud_layer.py`'s current behaviour for the live map until the designer approves.

Render with the same call the build uses:
`aud_layer.LAYER = Path("Drafts/aud_features_draft_2026-10-16.json")` then `build_trail_maps_pdf.build("aud", ...)` with `OUT_DIR` pointed at a scratch folder.

## Rules (the puzzle depends on them)
1. **Geometry comes from the JSON only.** No feature moves, is added, is removed or changes size class. Draw it where the JSON puts it. Do not generate the map as an AI image.
2. **Bridges, fords and gates stay clear.** Players count them (bridges, fords, gates per leg). They must sit on top of any texture and stay as readable as today.
3. **Crossings stay crossings.** A road over a river is a bridge, a stream over a road a ford, a hedge or wall with a road a gate. Do not change how `crossing_angles` works.
4. **Keep the print basics:** clipped to the map area, drawn beneath the stop pins, town dots and labels, legend still built from the symbols present.
5. **Print legibility:** laminated sheet, printed at letter size. Textures must stay readable at that size and not turn the sheet dark. Say if a texture needs lightening.
6. The designer SVG (`Aud_Map_Designer.html`) stays simple; only the print renderer needs the new look.

## Return
- The scratch PDF and a PNG render of it next to `baseline.png`.
- A short list of what was hard or did not look right (textured lines are the likely trouble).
- Any texture or icon file you need as a separate transparent PNG or seamless tile that the mock-up sheet does not give.
