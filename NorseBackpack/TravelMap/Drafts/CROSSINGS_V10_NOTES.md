# Aud crossing corrections v10 — 16 Oct 2026

## Scope
Address seven PDF comments on v9. All 102 JSON features and ticket-marker assignments retained. Live map sources unchanged.

Outputs:
- render_full_map_v10/Aud_Full_Map_v10.pdf and PNG.
- render_full_map_v10/Aud_Crossing_Review_v10.pdf: before/after for all seven annotated regions.
- render_crossings_v10.py and crossing_changes.json document each changed crossing.

## Perspective fix
Previously the entire bridge/gate illustration rotated, tilting upright posts. New assets follow explicit pose-guide PNGs from make_crossing_guides_v10.py, with posts vertical and decks at 90, 75 and 14 degrees. Annotated bridges select the nearest matching native pose and use uniform scaling only, with no image rotation or shear. The native-pose alignment can differ a few degrees from the exact road segment but falls within the deck width.

The six shallow-wall gates use a new approximately 10-degree open-gate illustration. Small vertical perspective corrections align the post bases to individual barriers while keeping vertical posts vertical. No whole-image rotation is used for these gates. The steep gate already approved at the top is retained. Unannotated bridge directions retain their v9 artwork.

## Ford fix
All five fords use 18pt-wide stepping stones, versus 13pt in v9. Roads/paths/tracks are clipped out of an 8.5pt-radius crossing area while being drawn. This removes only road ink and preserves water/terrain underneath. Stones draw last with other crossings. Geometry and crossing counts do not change.

## Checks and limits
Asserted that all annotated bridge/gate sites use new upright assets and all five fords use enlarged stones/road exclusion. Existing v9 checks retain 102 features, correct marker set, shoreline checks and unchanged source hashes. Final map and review PDFs rendered and visually inspected. Poppler fallback-font warnings persisted; labels readable. Route/counting solution and physical print proof remain unverified.

## Exact ImageGen prompts
Built-in ImageGen, separate call per variant. First reference is the pose guide under crossing_guides_v10; second reference is Art/MapIcons/Aud_Icon_Concepts_v1.png. Actual transparency requested; copied without pixel edits.

Shared prompt:
```text
Create ONE isolated illustrated map icon using image 1 as a STRICT GEOMETRY AND POSE GUIDE and image 2 as STYLE REFERENCE ONLY. Preserve the exact positions of every post base, every upright vertical post, the ground footprint and deck/leaf direction from image 1. Do NOT copy the isometric direction from image 2. Replace guide shapes with confident vintage hand-drawn cartographic illustration: dark muted purple #614773 outlines, opaque warm ivory #F4EEDD interiors, restrained woodgrain strokes, four or five broad planks, squat posts with small top faces and simple rails. Keep all posts VERTICALLY UPRIGHT on the page as in the guide. No whole-image rotation, leaning posts, elongated narrow catwalk, extra objects, water, ground, scenery, labels, border, shadows, glow or gradients. Actual TRANSPARENT background outside the icon. Keep the guide's canvas and footprint composition so its geometry remains usable at this orientation. Subject: 
```

Append each subject:
### Aud_Bridge_Upright_90_v10.png
Pose reference: Bridge_90.png

a short wooden bridge whose deck travel direction is vertical on the page, far end at TOP and near end at BOTTOM

### Aud_Bridge_Upright_75_v10.png
Pose reference: Bridge_75.png

a short wooden bridge whose deck travels steeply from BOTTOM LEFT to TOP RIGHT at 75 degrees

### Aud_Bridge_Upright_14_v10.png
Pose reference: Bridge_14.png

a short wooden bridge whose deck travels shallowly from BOTTOM LEFT to TOP RIGHT at 14 degrees

### Aud_Gate_Upright_10_v10.png
Pose reference: Gate_10.png

a two-post OPEN wooden field gate whose hinge and latch post bases follow a shallow BOTTOM LEFT to TOP RIGHT wall direction, with a broad two-rail gate leaf swung open toward the viewer

